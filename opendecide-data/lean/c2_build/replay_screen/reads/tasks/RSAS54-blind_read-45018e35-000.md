# A46 replay label-noise blind read RSAS54-blind_read-45018e35-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS54-blind_read-45018e35-000.json

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
  "qid": "qb9191abaec",
  "kind": "yes/no",
  "text": "Wikipedia page: 2010 in Fighting Network Rings\nSection: Events list\nTable:\n| # | Event Title | Date | Arena | Location |\n| 113 | Rings: The Outsider 14 | December 4, 2010 | Differ Ariake Arena | Tokyo, Japan |\n| 112 | Rings: The Outsider 13 | October 11, 2010 | Yokohama Cultural Gymnasium | Yokohama, Kanagawa, Japan |\n| 111 | Rings: The Outsider 12 | June 20, 2010 | Differ Ariake Arena | Tokyo, Japan |\n| 110 | Rings: The Outsider 11 | April 3, 2010 | Differ Ariake Arena | Tokyo, Japan |\n| 109 | Rings: The Outsider 10 | February 14, 2010 | Differ Ariake Arena | Tokyo, Japan |\n\nClaim: Rings: The Outsider 10 was an event held on February 14, 2010 at The Differ Ariake Arena in Tokyo, Japan.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qc3dc649722",
  "kind": "choice",
  "text": "Infobox:\nTitle: DIA\nOrigin: Seoul, South Korea\nGenres: K-pop\nYears active: 2015 - present\nLabels: MBK Entertainment\nAssociated acts: I.O.I, UNI.T\nWebsite: mbk-ent .com /main _dia\n\nHypothesis: DIA performs under the Top Dawg Entertainment group in the United States since 2011.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q49ff8dc213",
  "kind": "yes/no",
  "text": "Statement 1: We can see stars at day\nStatement 2: We can see stars at night",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q6378a52b2a",
  "kind": "yes/no",
  "text": "FAQ entry (restaurant: La Margherita)\nQ: Do you offer take out food at La Margherita?\nA: La Margherita does offer take-out ordering.\n\nCustomer question: Does La Margherita have take out service?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "qbe15411947",
  "kind": "yes/no",
  "text": "Customer: Yes.\nAssistant: Okay and what else?\nCustomer: Preferably adjoining rooms but one room with two king beds would be suffice.",
  "question": "In the customer's last message, is \"one\" a mention of the number of rooms for this hotel search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q008d0120a5",
  "kind": "yes/no",
  "text": "Trivia question (category: History).\n\nQuestion: What was the first sport to have been played on the moon?",
  "question": "Which answer choice correctly answers this trivia question?\nIs the correct answer \"Golf\"?",
  "definitions": "- Golf: Answer \"Golf\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Tennis: Answer \"Tennis\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Football: Answer \"Football\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Soccer: Answer \"Soccer\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q18fdb99a8c",
  "kind": "choice",
  "text": "Sentence from a New York Times opinion article: A coin collector we know finds nothing so stimulating as a midwinter thaw.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "very negative",
   "somewhat negative",
   "neutral",
   "somewhat positive",
   "very positive"
  ],
  "definitions": "- very negative: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- somewhat negative: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- neutral: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- somewhat positive: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- very positive: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "qbe180368e1",
  "kind": "yes/no",
  "text": "Markowsky, an executive vice president for American Electric Power until 2000, certainly understands that the quickest and most economic way to reduce carbon emissions from the 1,445 existing coal-fired power plants in the U.S. is to increase the efficiency and net power produced of a facility. Remember, CCS will require as much as 25% to 35% of the plants electrical output to run the chemical plant used to capture the carbon and therefore decimate the plants operating economics so perhaps this is Markowskys way of throwing sweetening the bad medicine that comes with CCS retrofits.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qc4eaddfaeb",
  "kind": "yes/no",
  "text": "Situation: They put on their big waders and went out into the water.\nAction being judged: Taking part in a sport that involves hurting animals.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qd9633c5174",
  "kind": "yes/no",
  "text": "Trivia question (category: Entertainment: Video Games).\n\nQuestion: Which one of these characters was first introduced in Sonic Boom: Rise of Lyric?",
  "question": "Which answer choice correctly answers this trivia question?\nIs the correct answer \"Code 31\"?",
  "definitions": "- Code 31: Answer \"Rouge the Bat\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 57: Answer \"Sticks the Badger\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 32: Answer \"Mighty the Armadillo\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 56: Answer \"Espio the Chameleon\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q85242d1c9c",
  "kind": "yes/no",
  "text": "Trivia question (category: Entertainment: Comics).\n\nQuestion: In Marvel Comics, Taurus is the founder and leader of which criminal organization?",
  "question": "Which answer choice correctly answers this trivia question?\nIs it wrong to answer \"Zodiac\"?",
  "definitions": "- Zodiac: Answer \"Zodiac\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Scorpio: Answer \"Scorpio\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- The Union: Answer \"The Union\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Tiger Mafia: Answer \"Tiger Mafia\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q001c960763",
  "kind": "yes/no",
  "text": "Unfortunately, it gets worse. In recent months, EPA has issued two regulationsthe Utility Maximum Achievable Control Technology rule and the Carbon Pollution Standard for New Power Plantsthat effectively ban the construction of new coal-fired power plants. Thus, EPA has effectively taken coal, one of America's most abundant and reliable energy sources, off the table.",
  "question": "Does this paragraph make the contrarian climate claim that human greenhouse gases are not causing climate change?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that human greenhouse gases are not causing climate change: it denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation (sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are negligible.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that human greenhouse gases are not causing climate change."
 },
 {
  "qid": "qb23a6b6833",
  "kind": "yes/no",
  "text": "Six of the eight patients with the infantile, severe form of the disease presented <e>cardiac involvement</e>, a feature rarely associated with GM1-gangliosidosis.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"cardiac involvement\" (marked <e>) in this sentence?\nIs it wrong to answer \"disease class\"?",
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "qb176fd3bf0",
  "kind": "choice",
  "text": "Although these mutations have been well characterized, little is known about the function of the <e>APC</e> gene product.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"APC\" (marked <e>) in this sentence?",
  "options": [
   "modifier",
   "composite mention",
   "specific disease",
   "disease class"
  ],
  "definitions": "- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders')."
 },
 {
  "qid": "q3d8e22c581",
  "kind": "yes/no",
  "text": "Jasper Kirkby of CERN has published a new paper examining the potential link between cosmic rays and climate.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qb66f862906",
  "kind": "choice",
  "text": "Tweet: @anonymous can we pretend ur a spy tho? U could be the American version of 007 &amp; be working at IBM undercover? Btw do YOU like lotus notes?!",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "Class V",
   "Class E",
   "Class X",
   "Class G",
   "Class F"
  ],
  "definitions": "- Class V: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Class E: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Class X: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Class G: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Class F: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "q6bfc5d61ab",
  "kind": "choice",
  "text": "Trivia question (category: Science: Computers).\n\nQuestion: When was the programming language \"C#\" released?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "1998",
   "1999",
   "2000",
   "2001"
  ],
  "definitions": "- 1998: Answer \"1998\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 1999: Answer \"1999\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 2000: Answer \"2000\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 2001: Answer \"2001\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qe398bfcae0",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): When Steve comes over to your house, he frequently forgets to flush the toilet after using the bathroom. You have complained to him about this but he keeps doing it. Later, you and Steve see someone walking their dog on the sidewalk. The dog poops on the sidewalk but the dog owner doesn't pick it up. Steve says, \"ew, people are so inconsiderate!\"\nYour reply to Steve: Yes! There are some inconsiderable people around.",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "qedf12273a5",
  "kind": "yes/no",
  "text": "The observation of typical mutations in STM7/X25 (GAA expansions) in this patient demonstrates that the two genetically different forms of <e>FRDA</e> cannot be distinguished clinically..",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"FRDA\" (marked <e>) in this sentence?\nIs it wrong to answer \"disease class\"?",
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "q46087e894e",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThese findings suggest that among women of reproductive age with COVID-19, pregnant women are more likely to be hospitalized and at increased risk for ICU admission and receipt of mechanical ventilation compared with nonpregnant women, but their risk for death is similar.\n\nClaim: Pregnant women with COVID-19 might be at higher risk for severe illness among women of reproductive age.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qdce0e24238",
  "kind": "yes/no",
  "text": "Ooooo, girls just want to have fuunn...sure they do 😉✋💲💲",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qf7a19dc410",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Ian Curtis\nBirth name: Ian Kevin Curtis\nBorn: 15 July 1956 Stretford, Lancashire, England\nDied: 18 May 1980 (aged 23) Macclesfield, Cheshire, England\nGenres: Post-punk, gothic rock\nOccupation(s): Singer-songwriter, musician\nInstruments: Vocals, guitar, melodica, synthesizer\nYears active: 1976-1980\nLabels: Factory\nAssociated acts: Joy Division\nWebsite: joydivisionofficial .com\n\nHypothesis: Ian Curtis is the real name of the artist",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q74adf24c03",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Indira Gandhi\nIn office: January 14, 1980 - October 31, 1984 (1), January 24, 1966 – March 24, 1977 (2)\nPresident: N.Sanjiva Reddy (1980-1984) (1), Zail Sing (1), Sarvepalli Radhakrishnan (1980-1984) (2), Zakir Husain (1966-1977) (2), V. V. Giri (1966-1977) (2), Fakhruddin Ali Ahmed (1966-1977) (2)\nPreceded by: Charan Singh (1980-1984) (1), Gulzarilal Nanda (Acting) (1966-1977) (2)\nSucceeded by: Morarji Desai (1980-1984) (1), Rajiv Gandhi (1966-1977) (2)\nDeputy: Morarji Desai (1966-1977) (2)\n\nHypothesis: Gulzarilal Nanda (Acting) held office after Morarji Desai.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely false?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- no: The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q39397e0fa1",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Insomnia\nDirected by: Christopher Nolan\nProduced by: Paul Junger Witt, Edward L. McDonnell, Broderick Johnson, Andrew A. Kosove\nScreenplay by: Hillary Seitz\nBased on: Insomnia by Nikolaj Frobenius Erik Skjoldbjaerg\nStarring: Al Pacino, Robin Williams, Hilary Swank, Maura Tierney, Martin Donovan, Nicky Katt, Paul Dooley\nMusic by: David Julyan\nCinematography: Wally Pfister\nEdited by: Dody Dorn\nDistributed by: Warner Bros. Pictures\nRelease date: May 3, 2002 ( 2002-05-03 ) (Tribeca Film Festival), May 24, 2002 ( 2002-05-24 ) (United States)\nRunning time: 118 minutes\nCountry: United States\nLanguage: English\nBudget: $46 million\nBox office: $113.7 million\nProduction company: Alcon Entertainment, Witt/Thomas Productions, Section Eight Productions\n\nHypothesis: Insomnia has a runtime of over 2 hours.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q865e55bdea",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2012 DODGE CHARGER. WHILE DRIVING APPROXIMATELY 60 MPH, THE VEHICLE STARTED TO DECELERATE. THE CONTACT COASTED TO THE SIDE OF THE ROAD. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. WHILE THE VEHICLE WAS PARKED, THE ENGINE CAUGHT FIRE. THE VEHICLE WAS TOWED TO THE DEALER WHERE IT WAS DIAGNOSED THAT A FAULTY THERMOSTAT MELTED ONTO THE ENGINE AND BURNED. THE ENGINE NEEDED TO BE REPLACED. THE VEHICLE WAS NOT REPAIRED. THE MANUFACTURER WAS MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 60,000. THE VIN WAS NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q281485b8e4",
  "kind": "yes/no",
  "text": "I'm not overwhelmed to have a particular thing.",
  "question": "If someone says this sentence, is it likely that they mean \"I'm overwhelmed not to have that thing.\"?",
  "definitions": "- yes: At least 7 of 10 annotators, and the average rating, judged it likely that a speaker of the negated sentence means the version with the negation moved into the embedded clause (a neg-raising reading, as 'I don't think it happened' usually means 'I think it didn't happen').\n- no: At most 3 of 10 annotators, and the average rating, judged it likely: the sentence only denies the attitude or report itself (as 'I didn't say it happened' does not mean 'I said it didn't happen')."
 },
 {
  "qid": "q1d841f9e18",
  "kind": "yes/no",
  "text": "Sentence: I [have] to say the value of this place always amazes me.\nMarked event or state: [have]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.\nIs it wrong to answer \"seconds\"?",
  "definitions": "- seconds: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- minutes: Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).\n- decades: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- years: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- weeks: Lasts from about one week up to under a month (a vacation, a short course, a hospital stay)."
 },
 {
  "qid": "q648564053e",
  "kind": "yes/no",
  "text": "Situation: It was called Crunch, so I thought maybe it was cereal coated.\nAction being judged: Judging people or things based on a name.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q3852255525",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Moon Chae-won\n- Moon Chae-won was born in Daegu, South Korea.\n- Moon made her acting debut in 2007 in \"Mackerel Run\", alongside fellow newcomer Lee Min-ho; they were among 60 actors who auditioned for the teen sitcom.\n\nSummary sentence:\nMoon Chae-won (; born November 13, 1986) is a South Korean actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qa42399f43c",
  "kind": "yes/no",
  "text": "Benedict Cumberbatch and wife Sophie Hunter have baby boy:",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: All 3 annotators rated the tweet medium or strong clickbait: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: None of the 3 annotators rated it medium or strong clickbait: the tweet states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q312d80a57b",
  "kind": "yes/no",
  "text": "Statement 1: he used water for hand sanitizing\nStatement 2: he used spirit for hand sanitizing",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q4a6ec61074",
  "kind": "choice",
  "text": "When I took aver we had uh a bureaucratic mess, like we have in Washington now, and we had three hundred agencies, departments, bureaus, commissions - uh some uh - fully budgeted, some not, but all having responsibility to carry out that was in conflict.",
  "question": "Which kind of statement is this sentence from a political debate?",
  "options": [
   "Non-factual statement",
   "Unimportant factual statement",
   "Check-worthy factual claim"
  ],
  "definitions": "- Non-factual statement: The sentence makes no factual claim that could be checked as true or false: it is a subjective opinion, belief or declaration, or a question.\n- Unimportant factual statement: The sentence does state a fact, but a trivial one (such as a small personal detail or a remark about the debate itself) that the public would not care to have verified and fact-checkers would skip.\n- Check-worthy factual claim: The sentence makes a factual claim that the general public would want to know is true or false and journalists would pick to fact-check, such as a voting record, a statistic, or what a policy did."
 },
 {
  "qid": "q4d1973cac0",
  "kind": "yes/no",
  "text": "Tweet: @anonymous @anonymous MoosAndBooze.com = Best url ever!",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?\nIs the correct answer \"very positive\"?",
  "definitions": "- very positive: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons.\n- neutral: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- somewhat positive: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- somewhat negative: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- very negative: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks."
 },
 {
  "qid": "q76349a8a2b",
  "kind": "yes/no",
  "text": "FAQ entry (restaurant: Gourmet Burger Kitchen)\nQ: Does GOURMET BURGER KITCHEN offer delivery services?\nA: GOURMET BURGER KITCHEN does not offer delivery services.\n\nCustomer question: Does the restaurant offer delivery as well?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "q87f142e14f",
  "kind": "yes/no",
  "text": "Customer: Could you tell me now many star rating that has? Is it in the North? I forgot to say I need it there.\nAssistant: a and b is not in the north, but there a few guesthouses in the north. Do you care for free wifi?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qfc3bc6926a",
  "kind": "choice",
  "text": "form in the human brain, Susumu Tonagawa, a neuroscientist at the Massachusetts Institute of Technology (MIT), and his team encoded memories in the brains of mice by manipulating individual neurons. Memories of experiences we have had are made from several elements, including records of objects, space and time. These records, called engrams, are encoded in physical and chemical changes in brain cells and the connections between them. According to Tonagawa, both false and genuine memories seem to rely on the same brain mechanisms.",
  "question": "This passage comes from a news article that English teachers rewrote for language learners at three reading levels. At which level is this passage written?",
  "options": [
   "elementary",
   "intermediate",
   "advanced"
  ],
  "definitions": "- elementary: The easiest rewrite (about CEFR A2-B1): short, mostly single-clause sentences, very common words, simple tenses, difficult terms explained or dropped, few idioms or long noun phrases.\n- intermediate: The middle rewrite (about B1-B2): moderately long sentences with some subordinate clauses, mostly everyday vocabulary with some less common words, lighter simplification of the original.\n- advanced: The original native-level newspaper text (about C1): long multi-clause sentences, rich or technical vocabulary, idioms, figurative language and dense reported speech, with no simplification."
 },
 {
  "qid": "qad387c6b13",
  "kind": "yes/no",
  "text": "The EPA is moving toward imposing these baseless regulations despite the fact that China and India have been building coal-fired plants to provide their nations with the energy to expand and compete in the global marketplace. China's CO2 emissions increased by 167% between 1999 and 2009, while the U.S., the second largest emitter of CO2, lowered its emissions by 17% over the same 10-year period.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qfdc84b978d",
  "kind": "choice",
  "text": "Sentence: Last week, Federal District Judge Lynn <Hughes> in Huston, Texas, [threw] out Wilson's two-decades old conviction.\nMarked event: [threw]\nMarked participant: <Hughes> (the phrase \"Federal District Judge Lynn Hughes in Huston, Texas\")",
  "question": "In this sentence, how likely is it that the participant <Hughes> was altered or somehow changed during or by the end of the [threw] event?",
  "options": [
   "Option W",
   "Option K",
   "Option G",
   "Option P",
   "Option Y"
  ],
  "definitions": "- Option W: Given the sentence, the property is clearly false for the participant in this event (scale point 1 of 5).\n- Option K: The property is probably false for the participant, though the sentence leaves some room for it (point 2 of 5).\n- Option G: The sentence gives no reason to think the property holds or fails; it is an even bet (point 3 of 5).\n- Option P: The property probably holds for the participant, though the sentence does not state it outright (point 4 of 5).\n- Option Y: Given the sentence, the property clearly holds for the participant in this event (point 5 of 5)."
 },
 {
  "qid": "q8520c5ecf9",
  "kind": "yes/no",
  "text": "Science facts table (first row is the header):\n| HABIT Behavior affecting health |  | HEALTH EFFECT Is the habit good, bad, or neutral for health? |  |\n| ... |\n| breaking a bone | is | bad | for health |\n| ... |\n| chewing bubble gum | is | neutral | for health |\n| ... |\n| drinking salt water | is | bad | for health |\n| ... |\n| drinking soup | is | good | for health |\n| ... |\n| eating dark chocolate | is | bad | for health |\n| ... |\n| eating junk foods | is | bad | for health |\n| ... |\n| eating lunch | is | good | for health |\n| ... |\n| eating peas | is | good | for health |\n| ... |\n| eating potatoes | is | neutral | for health |\n| ... |\n| eating tuna | is | neutral | for health |\n| ... |\n| running | is | neutral | for health |\n| ... |\n| using a computer | is | neutral | for health |\n| ... |\n| using tobacco | is | bad | for health |\n| ... |\n| watching movies | is | neutral | for health |\n| ... |\n\nQuestion: The habit _______ is good for health.\nProposed answer: running",
  "question": "According to the table of facts, is the proposed answer to the question correct?",
  "definitions": "- yes: The table's row for the fact the question asks about gives exactly the proposed answer (same entity, value or property), so it answers the question correctly.\n- no: The table shows the proposed answer belongs to a different row or fact than the one the question asks about, so it does not answer the question."
 },
 {
  "qid": "q1acc8ea9f4",
  "kind": "yes/no",
  "text": "Asthma genetics Rapid effects of inhaled corticosteroids in acute asthma: an evidence based evaluation Clinical Evidence Asthma Cochrane Database of Systematic Reviews Written action plans for asthma in children NEDOCROMIL SODIUM for chronic asthma in children Inhaled corticosteroids versus sodium cromoglycate in children and adults with asthma Ketotifen alone or as additional medication for long term control of asthma and wheeze in children Oral xanthines as maintenance treatment for asthma in children Addition of long acting beta2 agonists to inhaled corticosteroids versus same dose inhaled corticosteroids for CHRONIC ASTHMA in adults and children Addition of inhaled long.",
  "question": "Does this sentence express that one of the terms \"CHRONIC ASTHMA\" and \"NEDOCROMIL SODIUM\" is used to prevent the other (preventive use of a drug or ingredient)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked PREVENTS: the sentence presents one term as a drug or ingredient used to prevent the other or lower its risk (e.g. vitamin C reduces the risk of influenza).\n- no: At most 10% ticked PREVENTS: the terms are linked in another way in this sentence (treatment of an existing condition, cause, symptom, diagnosis, association) or not at all."
 },
 {
  "qid": "qd88ebe1457",
  "kind": "yes/no",
  "text": "This was posted by survive our collapse in FACEBOOK",
  "question": "Does this post use vulgar, offensive or abusive language?",
  "definitions": "- yes: The post meets the category the question names, as the Gab Hate Corpus coding manual defines it. Assault on human dignity: it degrades a group, or a person because of their group, by asserting or implying inferiority, comparing them to animals or subhumans, using slurs meant to wound, spreading hateful stereotypes, or supporting hateful ideology such as white supremacy. Call for violence: it advocates or endorses violence, genocide, expulsion, exclusion or segregation against a group, or a person because of their group. Vulgar or offensive language: it uses vulgar, derogatory or abusive wording or personal insults, whether or not the post is hateful.\n- no: The post does not meet the category the question names under the coding manual. Insults or threats aimed at a person without invoking their group are neither an assault on dignity nor a call for violence; degrading a group without advocating aggression, expulsion or exclusion is not a call for violence; hateful or political views stated without vulgar, profane or abusive wording are not vulgar language; criticism of policies, parties or ideas that does not degrade people is none of these."
 },
 {
  "qid": "q6d6b87f719",
  "kind": "yes/no",
  "text": "User: Create Dr. appointment at Monday 2pm - 3 pm\nAssistant: Is this good?\nUser (latest message): Yes, that looks right.",
  "question": "How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?\nIs it wrong to answer \"accept the pending proposal\"?",
  "definitions": "- accept the pending proposal: The assistant has just shown a proposed event or change (or several options) and the user approves it or picks one of the options ('yes', 'looks good', 'the second one'), without changing anything.\n- answer a question about a person or team: The user asks about someone in their organisation's directory: who a person is, their manager, direct reports, team, email address, phone number or office location.\n- decline: directions and travel: The user asks for directions, routes, traffic, travel time or when to leave to get somewhere; the assistant cannot answer transit questions.\n- create a new event: The user asks to put a new event on their calendar (schedule, add, book, set up a meeting or appointment) and the request is fully supported: one event, named attendees only, no recurrence, no specific conference room.\n- reject the pending proposal: The assistant has just shown a proposed event or change and the user refuses it or tells the assistant not to go ahead, without giving a replacement."
 },
 {
  "qid": "q6d4cbe2816",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2006, the science journal \"Nature\" listed Pharyngula as the top-ranked blog written by a scientist.\n\nSummary sentence:\nIn 2006 the journal \"Nature\" listed Myers's \"Pharyngula\" as the top-ranked blog by a scientist.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q20c901cdd2",
  "kind": "yes/no",
  "text": "Seriously. All women think about is status and sex, and then crotch spawns after they shit their first one out.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "qf2caaa91e4",
  "kind": "choice",
  "text": "Metachromatic Leukodystrophy (MLD) is a <e>neurodegenerative disease</e> in which the lysosomal enzyme, Aryl sulfatase A (ARSA) is deficient.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"neurodegenerative disease\" (marked <e>) in this sentence?",
  "options": [
   "specific disease",
   "modifier",
   "composite mention",
   "disease class"
  ],
  "definitions": "- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders')."
 },
 {
  "qid": "q4f6793ae57",
  "kind": "yes/no",
  "text": "FCC amateur radio licence exam: Technician class (Element 2) question pool 2026-2030.\nSubelement: Signals and emissions.\n\nQuestion: What is CW?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?\nIs it wrong to answer \"Error correction for digital transmission using code words\"?",
  "definitions": "- Error correction for digital transmission using code words: Answer \"Error correction for digital transmission using code words\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Another name for a Morse code transmission: Answer \"Another name for a Morse code transmission\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- A digital mode used primarily on 2-meter FM: Answer \"A digital mode used primarily on 2-meter FM\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- A type of electromagnetic propagation: Answer \"A type of electromagnetic propagation\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q8bff8a29b8",
  "kind": "yes/no",
  "text": "Customer: 14\"\nAssistant: What kind of crust would you like?\nCustomer: Original hand tossed",
  "question": "In the customer's last message, does \"Original hand tossed\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qaade785a96",
  "kind": "choice",
  "text": "Chatbot: Please go on.\nUser: because i want to get to know you\nChatbot: Do any other reasons not come to mind?\nUser: he likes nick",
  "question": "How abusive is the user's last message?",
  "options": [
   "not abusive",
   "ambiguous",
   "mildly abusive",
   "strongly abusive",
   "very strongly abusive"
  ],
  "definitions": "- not abusive: The message contains no abuse: an ordinary reply, question, test or off-topic remark, even if blunt, confused or mildly impatient.\n- ambiguous: It is unclear whether the message is abusive: it could be read as offensive or as harmless, for example crude language, unclear intent or an unintelligible message.\n- mildly abusive: The message is somewhat abusive: mild insults, rudeness, dismissive name-calling or unwanted sexual or personal remarks without strong slurs or threats.\n- strongly abusive: The message is clearly abusive: strong insults, profanity aimed at someone, explicit sexual harassment or degrading remarks, but short of the most extreme abuse.\n- very strongly abusive: The message is extremely abusive: severe slurs, violent or sexual threats, graphic sexual harassment or intensely hateful, dehumanising language."
 },
 {
  "qid": "q315fcceb99",
  "kind": "yes/no",
  "text": "Customer: P. I. A. C. I.\nAssistant: Ok, Piaci. And is that in Fort Bragg, South Carolina? I'm not seeing one listed.\nCustomer: No, up north in Fort Bragg, California. I'm not going that far for pizza.",
  "question": "In the customer's last message, does \"up north in Fort Bragg, California\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qea801b93cc",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHospitalizations were six times higher among patients with a reported underlying condition (45.4%) than those without reported underlying conditions (7.6%).\n\nClaim: Underlying conditions have no correlation with COVID-19 hospitalizations or deaths.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 }
]
