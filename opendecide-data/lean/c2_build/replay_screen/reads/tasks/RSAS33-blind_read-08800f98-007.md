# A46 replay label-noise blind read RSAS33-blind_read-08800f98-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS33-blind_read-08800f98-007.json

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
  "qid": "q7aa43bb843",
  "kind": "yes/no",
  "text": "Occupation: Stationary Engineers and Boiler Operators\nDuties:\n- Operate or tend stationary engines, boilers, and auxiliary equipment, such as pumps, compressors, or air-conditioning equipment, to supply and maintain steam or heat for buildings, marine vessels, or pneumatic tools.\n- Adjust controls and/or valves on equipment to provide power, and to regulate and set operations of system or industrial processes.\n- Receive instructions from steam engineers regarding steam plant and air compressor operations.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qe5d2ddf533",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Carol Burnett\nBirth name: Carol Creighton Burnett\nBorn: (1933-04-26) April 26, 1933 (age 85) , San Antonio, Texas, U.S.\nMedium: Television, theater, film, writing\nEducation: UCLA\nGenres: Parody, satire, slapstick\nSpouse: Don Saroyan , ( m. 1955; div. 1962) , Joe Hamilton , ( m. 1963; div. 1984) , Brian Miller , ( m. 2001)\nChildren: 3, including Carrie and Erin Hamilton\nNotable works and roles: The Carol Burnett Show\n\nHypothesis: Carol Burnett divorced Joe Hamilton before divorcing Don Saroyan.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?\nIs the correct answer \"Contradiction\"?",
  "definitions": "- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true.\n- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true."
 },
 {
  "qid": "qca5bbdf773",
  "kind": "yes/no",
  "text": "Beginners Guides to Blogging and <e>Twitter</e>: Two amazing products from Mike's Life. The 60 day Beginner's Guide to Bl ... http://bit.ly/99wlho",
  "question": "What type of named entity is \"Twitter\" (marked <e>) in this post?\nIs the correct answer \"corporation\"?",
  "definitions": "- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product."
 },
 {
  "qid": "q297832cb12",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master Less than 500-1600 Gross Registered Tons), Deck Safety.\n\nQuestion: Angular motion about the longitudinal axis of a vessel is known by which term?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Surge",
   "Roll",
   "Sway",
   "Pitch"
  ],
  "definitions": "- Surge: Answer \"Surge\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Roll: Answer \"Roll\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Sway: Answer \"Sway\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Pitch: Answer \"Pitch\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q82b81a1b72",
  "kind": "yes/no",
  "text": "Trivia question (category: Entertainment: Books).\n\nQuestion: Which of these does Charlie NOT read in The Perks of Being a Wallflower?",
  "question": "Which answer choice correctly answers this trivia question?\nIs it wrong to answer \"The Grapes of Wrath\"?",
  "definitions": "- The Grapes of Wrath: Answer \"The Grapes of Wrath\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition).\n- The Great Gatsby: Answer \"The Great Gatsby\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition).\n- Peter Pan: Answer \"Peter Pan\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition).\n- Hamlet: Answer \"Hamlet\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition)."
 },
 {
  "qid": "q9dac46b09f",
  "kind": "yes/no",
  "text": "Four novel PEPD alleles causing <e>prolidase deficiency</e>.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"prolidase deficiency\" (marked <e>) in this sentence?\nIs it wrong to answer \"Option J\"?",
  "definitions": "- Option J: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- Option E: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- Option Z: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- Option D: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders')."
 },
 {
  "qid": "q32eb0cb89e",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): You are helping Steve move into a new apartment. While carrying a heavy box, you accidentally broke some of Steve's glasses. Steve sighs and says, \"oh man, I loved those glasses! Well, can you clean up the pieces?\"\nYour reply to Steve: I will and let me know how much they cost as I'd like to replace them if I can.",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q0f183aa97a",
  "kind": "choice",
  "text": "Premise:\nTitle: Women's artistic individual all-aroundat the Games of the XXXI Olympiad\nVenue: Arena Olímpica do Rio\nDate: 11 August\nCompetitors: 24 from 14 nations\nWinning total: 62.198 points\nHypothesis: The event was held on August 15.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Class S",
   "Class X",
   "Class U"
  ],
  "definitions": "- Class S: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Class X: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Class U: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q625e8881d0",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n| FOR THE YEAR ENDED DECEMBER 31 | 2019 | 2018 |\n| Services (1) |  |  |\n| Wireless | 6,427 | 6,269 |\n| Wireline data | 7,684 | 7,466 |\n| Wireline voice | 3,564 | 3,782 |\n| Media | 2,811 | 2,677 |\n| Other wireline services | 251 | 247 |\n| Total services | 20,737 | 20,441 |\n| Products (2) |  |  |\n| Wireless | 2,660 | 2,497 |\n| Wireline data | 519 | 466 |\n| Wireline equipment and other | 48 | 64 |\n| Total products | 3,227 | 3,027 |\n| Total operating revenues | 23,964 | 23,468 |\nText:\nREVENUES BY SERVICES AND PRODUCTS\nThe following table presents our revenues disaggregated by type of services and products.\n(1) Our service revenues are generally recognized over time.\n(2) Our product revenues are generally recognized at a point in time.\n\nQuestion: What is the average annual Total services?\nProposed answer: 20,589",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "q00e6f4db51",
  "kind": "yes/no",
  "text": "Table caption: Overview of pH-measuring radio telemetry capsules\n| Brand radio telemetry capsule | Dimensions (mm) | Telemetry | Telemetry | Telemetry | Fluid reservoir | Commercially available | Refs |\n|  |  | pH | Temperature | Intestinal pressure |  |  |  |\n| Heidelberg | 8 × 18 | X |  |  |  | X | [46] |\n| IntelliCap® | 11 × 27 | X | X |  | X |  | [49,50] |\n| Bravo TM | 6 × 5.5 × 25 | X |  |  |  | X | [48] |\n| SmartPill | 11.7 × 22 | X | X | X |  | X | [47] |\n\nStatement: The Dimensions of Heidelberg is 18 18.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6826d0ee07",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: How to Train Your Dragon\nDirected by: Chris Sanders, Dean DeBlois\nProduced by: Bonnie Arnold\nScreenplay by: Will Davies, Dean DeBlois, Chris Sanders\nBased on: How to Train Your Dragon by Cressida Cowell\nStarring: Jay Baruchel, Gerard Butler, Craig Ferguson, America Ferrera, Jonah Hill, Christopher Mintz-Plasse, T. J. Miller, Kristen Wiig\nMusic by: John Powell\nEdited by: Darren T. Holmes, Maryann Brandon\nDistributed by: Paramount Pictures\nRelease date: March 26, 2010 ( 2010-03-26 )\nRunning time: 98 minutes\nCountry: United States\nLanguage: English\nBudget: $165 million\nBox office: $495.8 million\nProduction company: DreamWorks Animation\n\nHypothesis: How to Train Your Dragon was over an hour and a half long.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q62071fe164",
  "kind": "yes/no",
  "text": "as a michigander, i bet she's a hit in detroit. personally, paying to see stand up comedy is a waste, it's all negative, there's absolutely no positive side to that form of entertainment at all. ",
  "question": "Does this post use vulgar, offensive or abusive language?",
  "definitions": "- yes: The post meets the category the question names, as the Gab Hate Corpus coding manual defines it. Assault on human dignity: it degrades a group, or a person because of their group, by asserting or implying inferiority, comparing them to animals or subhumans, using slurs meant to wound, spreading hateful stereotypes, or supporting hateful ideology such as white supremacy. Call for violence: it advocates or endorses violence, genocide, expulsion, exclusion or segregation against a group, or a person because of their group. Vulgar or offensive language: it uses vulgar, derogatory or abusive wording or personal insults, whether or not the post is hateful.\n- no: The post does not meet the category the question names under the coding manual. Insults or threats aimed at a person without invoking their group are neither an assault on dignity nor a call for violence; degrading a group without advocating aggression, expulsion or exclusion is not a call for violence; hateful or political views stated without vulgar, profane or abusive wording are not vulgar language; criticism of policies, parties or ideas that does not degrade people is none of these."
 },
 {
  "qid": "q711527a833",
  "kind": "choice",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), BWR question bank, topic: Fission Product Poisons.\n\nQuestion: Which one of the following is the approximate half-life of xenon-135?",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?",
  "options": [
   "19 seconds",
   "6.6 hours",
   "9.1 hours",
   "30 hours"
  ],
  "definitions": "- 19 seconds: Answer \"19 seconds\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 6.6 hours: Answer \"6.6 hours\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 9.1 hours: Answer \"9.1 hours\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 30 hours: Answer \"30 hours\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q116d63ad2b",
  "kind": "yes/no",
  "text": "Sentence: <Employees> [seemed] to be having a good time chatting and laughing with each other, while myself and other customers were completely ignored.\nMarked event: [seemed]\nMarked participant: <Employees>",
  "question": "In this sentence, how likely is it that the participant <Employees> was altered or somehow changed during or by the end of the [seemed] event?\nIs the correct answer \"Class C\"?",
  "definitions": "- Class C: Given the sentence, the property is clearly false for the participant in this event (scale point 1 of 5).\n- Class K: The property probably holds for the participant, though the sentence does not state it outright (point 4 of 5).\n- Class R: The sentence gives no reason to think the property holds or fails; it is an even bet (point 3 of 5).\n- Class J: The property is probably false for the participant, though the sentence leaves some room for it (point 2 of 5).\n- Class P: Given the sentence, the property clearly holds for the participant in this event (point 5 of 5)."
 },
 {
  "qid": "q51e0203da1",
  "kind": "yes/no",
  "text": "User: How do I contact them?\nAssistant: It's (530) 587-1131.\nUser: Is Fool's Errand in Cambridge costly?\nAssistant: You'll have to contact them directly.\nUser (latest message): Is Pinocchio's Pizza in Cambridge costly?",
  "question": "How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?\nIs the correct answer \"answer a question about a place\"?",
  "definitions": "- answer a question about a place: The user asks for supported facts about a named business or place: its address, phone number, website, price level, rating, hours or whether it has a feature (full bar, parking, takeout).\n- wait for the user: The user asks the assistant to hold on or wait while they do something ('wait a minute', 'hold on while I call Stacy'); nothing else is requested.\n- decline: reminders and alarms: The user asks the assistant to set a reminder, alarm or notification (for themselves or others); the assistant cannot do reminders, even when the rest of the request is fine.\n- decline: recurring events: The user asks to create or change a recurring or repeated series of events ('every Tuesday', 'the next 3 Saturdays', 'do that on the 18th too'); the assistant cannot schedule recurrences.\n- answer a question about a person or team: The user asks about someone in their organisation's directory: who a person is, their manager, direct reports, team, email address, phone number or office location."
 },
 {
  "qid": "q8314966675",
  "kind": "choice",
  "text": "Sentence from a New York Times opinion article: The nice word for Rumania's way is austerity; deprivation is more accurate.",
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
  "qid": "qd6d0d97641",
  "kind": "yes/no",
  "text": "A 34-year-old man was brought into the emergency room after he was found running in the streets. Upon arrival to the emergency room, he keeps screaming, “they are eating me alive,\" and swatting his hands. He reports that there are spiders crawling all over him. His girlfriend, who arrives shortly after, claims that he has been forgetful and would forget his keys from time to time. He denies weight loss, fever, shortness of breath, abdominal pain, or urinary changes but endorses chest pain. His temperature is 98.9°F (37.2°C), blood pressure is 160/110 mmHg, pulse is 112/min, respirations are 15/min, and oxygen saturation is 98%. He becomes increasingly agitated as he believes the healthcare providers are trying to sacrifice him to the “spider gods.” What is the most likely explanation for this patient’s symptoms?\n\nAnswer choices:\nA. Cocaine use\nB. Narcolepsy\nC. Pick disease\nD. Schizophrenia\nE. Temporal lobe epilepsy\n\nProposed answer: A. Cocaine use",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q3f6b53d437",
  "kind": "choice",
  "text": "In contrast, hSNF5/INI1 point mutations were not detected in breast cancers, Wilms tumors, gliomas, ependymomas, <e>sarcomas</e> and other tumor types, even though most analyzed cases harbored loss of heterozygosity at 22q11. 2 loci.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"sarcomas\" (marked <e>) in this sentence?",
  "options": [
   "composite mention",
   "disease class",
   "modifier",
   "specific disease"
  ],
  "definitions": "- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "q0e6d52425d",
  "kind": "choice",
  "text": "furious chinese defy censors to mock local leaders over bungled virus response  according to nyt, the censors have now been completely overwhelmed  #HASHTAG #HASHTAG #HASHTAG #HASHTAG #HASHTAG #HASHTAG  https://t.co/rz9jzi5ljv",
  "question": "Under the East Asian prejudice codebook, which category does this tweet fall into?",
  "options": [
   "Option N",
   "Option T",
   "Option D",
   "Option F",
   "Option G"
  ],
  "definitions": "- Option N: The tweet derogates or demeans an East Asian group, country, government or culture: extreme negative portrayal, hatred, conspiracy or bioweapon claims, 'they should leave', celebrating suffering, boycott calls, or mocking virus names; it outranks all other categories.\n- Option T: The tweet criticises an East Asian institution, affiliation or practice (such as the Chinese government hiding data) in a factual or reasoned way without abuse, stereotypes, conspiracy claims or normative 'they can't be trusted' framing.\n- Option D: The tweet explicitly challenges or condemns anti-East-Asian prejudice, slurs or stereotypes, or shows solidarity with East Asian people, without itself abusing the same target.\n- Option F: The tweet talks about Sinophobia or anti-Asian racism, or debates names like 'China virus', without itself engaging in or explicitly countering the prejudice.\n- Option G: The tweet is none of the above: unrelated, neutral news, or mentions East Asia or the virus without hostility, criticism, counter-speech or discussion of prejudice, including a neutral geographic 'Wuhan virus'."
 },
 {
  "qid": "q9cd79c9f90",
  "kind": "yes/no",
  "text": "Heading: Sushi vs. zushi\nWhy is sushi called sushi with an \"s\" but specific varieties are called \"makizushi\", \"nigirizushi\", etc. with a \"z\"? &#124;",
  "question": "Which Wikipedia Reference Desk should this question be posted to?\nIs it wrong to answer \"Mathematics reference desk\"?",
  "definitions": "- Mathematics reference desk: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Language reference desk: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Computing reference desk: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Science reference desk: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software).\n- Humanities reference desk: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Entertainment reference desk: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment."
 },
 {
  "qid": "q2ad2456c32",
  "kind": "yes/no",
  "text": "A 17-year-old African-American male presents to his family physician after noticing red-tinged urine the week before, when he was suffering from a cold. The patient states that he had experienced that before. His father is with him and says that this happens to him on occasion as well. What is the most likely diagnosis for this patient?\n\nAnswer choices:\nA. Acute cystitis\nB. Acute interstitial nephritis\nC. Sickle cell trait\nD. Acute glomerulonephritis\nE. Hemophilia\n\nProposed answer: C. Sickle cell trait",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qf518d51f52",
  "kind": "yes/no",
  "text": "Health topic: Pyelonephritis: Kidney Infection\nPassage: Pyelonephritis is caused by a bacterium or virus infecting the kidneys. Though many bacteria and viruses can cause pyelonephritis, the bacterium Escherichia coli is often the cause. Bacteria and viruses can move to the kidneys from the bladder or can be carried through the bloodstream from other parts of the body. A UTI in the bladder that does not move to the kidneys is called cystitis.",
  "question": "Which consumer-health question about the named topic does this passage from an NIH health page answer?\nIs the correct answer \"Option H\"?",
  "definitions": "- Option H: Names risk factors or groups more likely to get the condition (age, sex, family history, exposures), rather than its mechanism.\n- Option L: Explains why the condition happens: the biological mechanism, the gene mutations or the infectious or environmental agent that produces it (not who is more likely to get it).\n- Option X: Describes the expected course and outcome: survival, recovery, progression or life expectancy.\n- Option B: Gives the prevalence or incidence: how many people or what share of a population have it, or that it is rare or its frequency is unknown.\n- Option T: Describes steps that lower the chance of getting the condition or its spread, such as vaccines, hygiene, lifestyle or avoiding exposures.\n- Option A: Describes how the condition is treated or managed: therapies, drugs, surgery, and standard or trial treatment options."
 },
 {
  "qid": "q23feb79243",
  "kind": "choice",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), BWR question bank, topic: Reactor Kinetics and Neutron Sources.\n\nQuestion: A reactor is operating at a very low power level when a control rod is fully inserted, resulting in a stable negative 80-second period. If the initial power level was 120 watts, what will the approximate reactor power level be two minutes after rod insertion stops?",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?",
  "options": [
   "27 watts",
   "32 watts",
   "49 watts",
   "54 watts"
  ],
  "definitions": "- 27 watts: Answer \"27 watts\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 32 watts: Answer \"32 watts\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 49 watts: Answer \"49 watts\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 54 watts: Answer \"54 watts\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q6fa1213bd0",
  "kind": "yes/no",
  "text": "Sentence: [Save] your new notepad file as a text file.\nMarked event or state: [Save]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.\nIs the correct answer \"Code 52\"?",
  "definitions": "- Code 52: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- Code 21: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- Code 59: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot).\n- Code 23: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- Code 17: Has no bounded duration: permanent, timeless or generic states and truths (being a species, a mathematical fact, a general rule)."
 },
 {
  "qid": "qe8743c360d",
  "kind": "yes/no",
  "text": "Long-distance telephone satellite communication carriers",
  "question": "Which NAICS 2022 subsector does a business whose primary activity is described here belong to?\nIs it wrong to answer \"517 Telecommunications\"?",
  "definitions": "- 517 Telecommunications: Providing telecommunications services: wired, wireless and satellite communications and resellers of such services.\n- 922 Justice, Public Order, and Safety Activities: Government courts, police, correctional institutions, fire protection, parole and other public order and safety activities.\n- 711 Performing Arts, Spectator Sports, and Related Industries: Performing arts companies, spectator sports teams and tracks, promoters, agents for artists and athletes, and independent artists, writers and performers.\n- 323 Printing and Related Support Activities: Printing on paper, fabric, plastic and other materials, and support activities for printing such as prepress and bookbinding.\n- 512 Motion Picture and Sound Recording Industries: Producing, distributing and exhibiting motion pictures and videos, and producing and distributing sound recordings, including studios and theaters."
 },
 {
  "qid": "q8cfd54f2b5",
  "kind": "yes/no",
  "text": "r🅰️pe all women",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q31e2230605",
  "kind": "yes/no",
  "text": "Mice with a <e>partial or complete deficiency of Hmgic</e> resisted diet-induced obesity.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"partial or complete deficiency of Hmgic\" (marked <e>) in this sentence?\nIs the correct answer \"disease class\"?",
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "q4857175a88",
  "kind": "yes/no",
  "text": "It's all projection Women realize they can only offer one thing to a man, so they pretend that men only want that one thing.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q6bbe2de47c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2015, Jackson returned to acting following a 23-year absence, having retired from politics.\n\nSummary sentence:\nShe retired from politics and returned to acting in 2015.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q6116c8aae5",
  "kind": "yes/no",
  "text": "Northeast blizzard could dump up to 18 inches of snow on New York City",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qe1e46b579e",
  "kind": "choice",
  "text": "Beginning: Jean Claude is talking to his son. He ...\n\nPossible endings:\n(A) is talking about the potential of the Quantum Computation in a seminar.\n(B) is asking if he needs help with his work.\n(C) is describing the reason why the American Society is confused about the upcoming elections.\n(D) starts violently hitting his child.",
  "question": "Which listed ending continues the beginning most sensibly?",
  "options": [
   "Code 41",
   "Code 55",
   "Code 11",
   "Code 49"
  ],
  "definitions": "- Code 41: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Code 55: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Code 11: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Code 49: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "q850b571050",
  "kind": "choice",
  "text": "When too much choice is a bad thing, <e>Joel</e> on Technology http://bit.ly/9KKobr",
  "question": "What type of named entity is \"Joel\" (marked <e>) in this post?",
  "options": [
   "location",
   "group",
   "product",
   "corporation",
   "creative work",
   "person"
  ],
  "definitions": "- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team."
 },
 {
  "qid": "qb13d3e8724",
  "kind": "yes/no",
  "text": "Complaint narrative: TRUCK FRAME SEEMS TO BE ROTTING. TOLD 3-4 YEARS AT MOST BY MECHANIC. ALREADY REPLACES FUEL TANK BRACKETS, ANY RUST RECALLS AS IN ONES TOYOTA DID A WHILE AGO/ ALSO TOLD AT 1000,000 MI WILL NEED SPARK PLUG CHANGE (ONLY59000 NOW) AND THERE WAS A RECALL OF THIS PLUG REMOVAL COULD BE DIFFICULT. ANY HELP",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qd1567e00e9",
  "kind": "yes/no",
  "text": "Health topic: Emery-Dreifuss muscular dystrophy\nPassage: X-linked Emery-Dreifuss muscular dystrophy is the most common form of this condition, affecting an estimated 1 in 100,000 people. The autosomal recessive type of this disorder appears to be very rare; only a few cases have been reported worldwide. The incidence of the autosomal dominant form is unknown.",
  "question": "Which consumer-health question about the named topic does this passage from an NIH health page answer?\nIs it wrong to answer \"complications\"?",
  "definitions": "- complications: Describes further problems or conditions the disease can lead to.\n- how common it is: Gives the prevalence or incidence: how many people or what share of a population have it, or that it is rare or its frequency is unknown.\n- causes: Explains why the condition happens: the biological mechanism, the gene mutations or the infectious or environmental agent that produces it (not who is more likely to get it).\n- who is at risk: Names risk factors or groups more likely to get the condition (age, sex, family history, exposures), rather than its mechanism.\n- stages: Explains how the disease (usually a cancer) is staged: how spread is measured and what each stage means.\n- outlook (prognosis): Describes the expected course and outcome: survival, recovery, progression or life expectancy."
 },
 {
  "qid": "q520e37440e",
  "kind": "choice",
  "text": "In addition, a significant excess risk of <e>basal cell carcinoma</e> was seen (standardized incidence ratio 35, 95% confidence interval 7. 2 to 102).",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"basal cell carcinoma\" (marked <e>) in this sentence?",
  "options": [
   "Option R",
   "Option C",
   "Option Q",
   "Option V"
  ],
  "definitions": "- Option R: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- Option C: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- Option Q: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- Option V: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "q5e2866e27e",
  "kind": "yes/no",
  "text": "Complaint narrative: MY 1999 HONDA CIVIC DX KEPT SHUTTING OFF SEVERAL TIMES WHILE DRIVING WITHOUT WARNING. DIED ON THE INTERSTATE, AND SUBSEQUENTLY, I WAS REARENDED. WAS DIAGNOSED WITH A FAULTY IGNITION SWITCH WHICH WAS RECALLED FOR MY YEAR, MAKE AND MODEL BUT MY BATCH SUPPOSEDLY WASN'T ONE THAT WAS AFFECTED. THEY WANT $700 TO REPAIR THE $80 RECALLED PART AND REFUSE TO HONOR THE ALREADY EXISTING RECALL.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q99e8cb4d4c",
  "kind": "yes/no",
  "text": "Assistant: So you have a venti iced caramel macchiato with soy milk, half caramel, two shots of espresso, upside down.\nCustomer: That's right.\nAssistant: The drink is ready to picked up at Arlington and your receipt will be sent to your phone.",
  "question": "According to the assistant's last message, is \"Arlington\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q814ba46ece",
  "kind": "yes/no",
  "text": "EMPLOYEE WAS HELPING LOAD A SHOT CRETE BAG WITH OTHER EMPLOYEE OPERATING TUGGER. HE WAS HOLDING THE TUGGER CABLE AND HOOK IN PLACE AND HAD HIS HAND TOO CLOSE TO THE HOOK WHEN THE OTHER EMPLOYE E TIGHTENED THE CABLE, PINCHING HIS RIGHT THUMB IN THE HOOK, REQUIRING STITCHES.",
  "question": "Which type of mining equipment was involved in this mine accident?\nIs the correct answer \"track equipment (re-railer, track jack)\"?",
  "definitions": "- track equipment (re-railer, track jack): Track equipment used to lay or repair rail track or re-rail cars: re-railers, track jacks, track shifters.\n- tugger or air winch: Tuggers, air winches, air hoists, air jacks and electric or hand-cranked winches used to pull or lift loads.\n- mantrip or personnel carrier (jeep, jitney, ATV): Vehicles that carry miners: mantrips, mancars, personnel carriers, porta-buses, jeeps, jitneys, ATVs.\n- longwall shields and other longwall parts: Longwall roof supports and parts other than the cutter: shields, ram jacks, Dowdy jacks, Duke.\n- tractor or supply car: Tractors (farm, yard, earth-moving or tractor units not named as tractor-trailers or semis) and supply cars.\n- scraper (pan or tractor scraper): Earth-moving scrapers (pan, tractor and elevating scrapers, scraper loaders); not slusher or scraper hoists."
 },
 {
  "qid": "qecd8eb1d72",
  "kind": "choice",
  "text": "The most notable feature is a bull's-eye of above-normal temperatures predicted by the suites of models in the Barents Sea north of <e2>Norway</e2> and <e1>Russia</e1> in the Arctic Ocean.",
  "question": "Which relation from entity 1 (\"Russia\", marked <e1>) to entity 2 (\"Norway\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "shares border with",
   "diplomatic relation",
   "none of the listed relations"
  ],
  "definitions": "- shares border with: The sentence states that entity 1 and entity 2 (countries, regions or places) share a common border ('bordered by', 'neighbouring'); being mentioned together does not count.\n- diplomatic relation: The sentence states that entity 1 and entity 2, two states, have official state-to-state relations (embassies, ambassadors, treaties, alliances, state visits); merely naming both countries does not count.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q4e62fedc5f",
  "kind": "yes/no",
  "text": "me n those female b1️⃣tch3️⃣s",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q0463257277",
  "kind": "yes/no",
  "text": "User: Does the Pizza and Kabob in Folsom have a rating? What is it?\nAssistant: It's rated 0 stars.\nUser (latest message): Ok thanks. And how is Shirokiya rated in Hawaii",
  "question": "How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?\nIs it wrong to answer \"Code 36\"?",
  "definitions": "- Code 36: The user asks about someone in their organisation's directory: who a person is, their manager, direct reports, team, email address, phone number or office location.\n- Code 13: The user asks for supported facts about a named business or place: its address, phone number, website, price level, rating, hours or whether it has a feature (full bar, parking, takeout).\n- Code 11: The user only greets, thanks or reacts ('hi', 'thanks', 'ok', 'great job'), makes small talk, or asks for help in general without a concrete calendar request; the assistant just replies politely and offers help.\n- Code 47: The user asks for directions, routes, traffic, travel time or when to leave to get somewhere; the assistant cannot answer transit questions.\n- Code 26: The user asks the assistant to hold on or wait while they do something ('wait a minute', 'hold on while I call Stacy'); nothing else is requested.\n- Code 12: The user asks for personal information the directory does not hold (home address, whether someone is online, someone else's schedule) or about people outside the directory."
 },
 {
  "qid": "q2ab60541de",
  "kind": "yes/no",
  "text": "An 8-month-old boy is brought to his pediatrician by his parents with a 12-hour history of fever and coughing. He has also been experiencing intermittent diarrhea and skin abscesses since birth. Otherwise, he has been meeting developmental milestones as expected. Analysis of this patient's sputum reveals acute angle branching fungi, and culture shows gram-positive cocci in clusters. A flow cytometry reduction test was obtained that confirmed the diagnosis. Which of the following processes is most likely defective in this patient?\n\nAnswer choices:\nA. Actin polymerization\nB. Leukocyte migration\nC. Maturation of B-cells\nD. Transforming oxygen into superoxide radicals\nE. Transforming superoxide radicals into hydrogen peroxide\n\nProposed answer: E. Transforming superoxide radicals into hydrogen peroxide",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q9d2416a82d",
  "kind": "choice",
  "text": "The IQ of PAH-deficient mothers with a severe PKU mutation in combination with a <e>MHP</e> mutation or a mild PKU mutation was 99 and 96, respectively, whereas the IQ of PKU mothers with two severe PKU mutations or with one severe and one moderate PKU mutation was 83 and 84, respectively.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"MHP\" (marked <e>) in this sentence?",
  "options": [
   "specific disease",
   "modifier",
   "disease class",
   "composite mention"
  ],
  "definitions": "- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers')."
 },
 {
  "qid": "q29c5f60470",
  "kind": "yes/no",
  "text": "Russia denies having compromising material on Donald Trump",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q1a3f460c37",
  "kind": "choice",
  "text": "Premise:\nTitle: Dame Julie Andrews DBE\nBorn: 1 October 1935 (age 83) Walton-on-Thames, Surrey, England\nBirth name: 1 October 1935 (age 83) Walton-on-Thames, Surrey, England\nOccupation: Actress, singer, author\nYears active: 1945-present\nSpouse(s): Tony Walton ( m. 1959 ; div. 1967 ), Blake Edwards ( m. 1969 ; died 2010 )\nChildren: 3, including Emma Walton Hamilton\nHypothesis: Julie Andrews has 3 daughters.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q3f7fc9f095",
  "kind": "yes/no",
  "text": "Should I wear snow boots today?",
  "question": "What is the user asking about the weather or sky?\nIs the correct answer \"Weather conditions or forecast\"?",
  "definitions": "- Weather conditions or forecast: The user asks about current or forecast weather, such as temperature, rain, snow, wind or humidity somewhere.\n- Sunrise time: The user asks when the sun will rise, or about sunrise, on some day or at some place.\n- Sunset time: The user asks when the sun will set, or about sunset, on some day or at some place."
 },
 {
  "qid": "qecfbfcf716",
  "kind": "choice",
  "text": "Finkelstein is a lying cunt and a token Jew for the right-wing and leftist fringe.",
  "question": "This post is sexist. Which broad category of sexism does it fall under?",
  "options": [
   "Code 21",
   "Code 30",
   "Code 12",
   "Code 31"
  ],
  "definitions": "- Code 21: The post threatens women or states plans to harm them, or incites and encourages others to inflict serious harm or violence on women.\n- Code 30: The post explicitly demeans women: derogatory descriptions, aggressive or emotive attacks, dehumanising comparisons or overt sexual objectification.\n- Code 12: The post shows implicit or subtle sexism: casual gendered slurs, stereotypes or claims of innate gender differences, backhanded compliments, or condescending advice.\n- Code 31: The post denies or justifies sexist treatment: supporting mistreatment of individual women, or denying or justifying discrimination against women as a group, including male-victimhood arguments."
 },
 {
  "qid": "q9082e29d17",
  "kind": "yes/no",
  "text": "This woman was gifted a karaoke mic and did the absolute most",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qa878a2e39f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe clinical symptoms were significantly improved along with increase of oxyhemoglobin saturation within 3 d. Several parameters tended to improve as compared to pretransfusion, including increased lymphocyte counts (0.65 × 10(9)/L vs. 0.76 × 10(9)/L) and decreased C-reactive protein (55.98 mg/L vs. 18.13 mg/L). This study showed CP therapy was well tolerated and could potentially improve the clinical outcomes through neutralizing viremia in severe COVID-19 cases.\n\nClaim: Convalescent plasma given to severe COVID-19 patients worsened their symptoms.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "q850d610045",
  "kind": "yes/no",
  "text": "Kamala Harris is a Negro? I just thought she was set on fire, and someone put her face out with a shovel! ... another tranny!",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 }
]
