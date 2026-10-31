# A46 replay label-noise blind read RSBS77-blind_read-aef85478-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSBS77-blind_read-aef85478-002.json

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
  "qid": "q7ad8af8971",
  "kind": "yes/no",
  "text": "A 35-year-old woman presents as a new patient to a primary care physician. She hasn't seen a doctor in many years and came in for a routine check-up. She has no specific complaints, although she has occasional shortness of breath with mild activity. On physical exam, her vital signs are as follows: HR 80, BP 110/70, RR 14. On auscultation, her lungs are clear with equal breath sounds bilaterally. When listening over the precordium, the physician hears a mid-systolic click followed by a late systolic murmur that is loudest over the apex. Valsalva increases the murmur. Which of the following is NOT a possible complication of this patient's underlying problem?\n\nAnswer choices:\nA. Atrial fibrilation\nB. Infective endocarditis\nC. Bleeding from acquired von Willebrand disease\nD. Cerebral embolism\nE. Sudden death\n\nProposed answer: C. Bleeding from acquired von Willebrand disease",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qe6e8dd72ac",
  "kind": "yes/no",
  "text": "Beginning: I tried to maintain the facade that I had not lost my job. My father ...\n\nPossible endings:\n(A) saw through the ruse.\n(B) offered to give me his hammock.\n(C) told me to walk our three-headed dog.\n(D) took my temperature with telekinesis.",
  "question": "Among the listed endings, is (A) \"saw through the ruse.\" the most sensible continuation of the beginning?",
  "definitions": "- yes: The named ending is the listed continuation that makes the most sense: read after the beginning, it describes what would ordinarily be true or happen next, fits who and what the beginning is about, and respects any negation, number, idiom or double meaning in it.\n- no: Another listed ending makes more sense: the named ending contradicts the beginning, is about the wrong person or thing, misreads a word, idiom or quantity, or describes something absurd or unrelated."
 },
 {
  "qid": "q19be360964",
  "kind": "yes/no",
  "text": "A 67-year-old woman with chronic kidney disease, hypertension, and diabetes mellitus presented with congestive heart failure and underwent uneventful 3-vessel coronary artery bypass surgery. Within 20 hours, she was extubated and all infusions except nitroprusside were stopped. On the 4th postoperative day, she deteriorated, exhibiting restlessness, tachypnea, tachycardia, and hypotension. Inotropes, vasopressors and bicarbonate infusions were started. Continuous hemodialysis was initiated, yet lactate levels continued to rise. Her chart clarified that she had received 319 mg of nitroprusside over 72 hours. What is the most likely cause of her condition?\n\nAnswer choices:\nA. Cyanide toxicity\nB. Carbon monoxide poisoning\nC. Sulfmethemoglobinemia\nD. Methemoglobinemia\nE. Anemia\n\nProposed answer: A. Cyanide toxicity",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q7cfebb79b9",
  "kind": "yes/no",
  "text": "Statement 1: Things change every day\nStatement 2: Things are not changing every day",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q981b798486",
  "kind": "choice",
  "text": "Chatbot: Please go on.\nUser: you are stupid aren't you\nChatbot: Does it please you to believe I am stupid arent i?\nUser: You are a woman,aren't you?",
  "question": "What kind of abuse is in the user's last message?",
  "options": [
   "sexual harassment",
   "sexism",
   "intellectual insult",
   "homophobia",
   "racism",
   "ableism",
   "general insult or hostility"
  ],
  "definitions": "- sexual harassment: The abuse is sexual: unwanted sexual advances, explicit sexual requests or descriptions, or sexualised comments directed at the chatbot or someone else.\n- sexism: The abuse targets gender: it demeans women or men as a group, uses gendered slurs, or attacks the chatbot or someone because of perceived gender.\n- intellectual insult: The abuse attacks intelligence or competence: calling the chatbot or someone stupid, dumb, useless or incapable of understanding.\n- homophobia: The abuse targets sexual orientation: homophobic slurs or insults, or treating being gay or lesbian as shameful or as an insult.\n- racism: The abuse targets race, ethnicity or nationality: racial slurs, racist stereotypes, or demeaning remarks about a racial or ethnic group.\n- ableism: The abuse targets disability: using disability or mental illness as an insult, such as 'retard', or demeaning people with disabilities.\n- general insult or hostility: The abuse fits none of the specific types: general swearing, name-calling, telling someone to go away, or other hostility not based on sex, gender, sexual orientation, race, disability or intelligence."
 },
 {
  "qid": "qdda9759453",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master TV to Master Less than 500 Gross Registered Tons), Navigation and Deck General – Safety.\n\nQuestion: What is the minimum number of fire axes required on a vessel of 900 GT?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "2",
   "4",
   "6",
   "8"
  ],
  "definitions": "- 2: Answer \"2\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 4: Answer \"4\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 6: Answer \"6\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 8: Answer \"8\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qfb3ee1972e",
  "kind": "choice",
  "text": "Our Favorite <e>YouTube</e> Videos This Week: The Drama Edition: Had any epic meltdowns this week? You know, of the cryin ... http://bit.ly/cuy0yt",
  "question": "What type of named entity is \"YouTube\" (marked <e>) in this post?",
  "options": [
   "group",
   "product",
   "corporation",
   "creative work",
   "person",
   "location"
  ],
  "definitions": "- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building')."
 },
 {
  "qid": "qdfe1217750",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): Steve has a friend Bill. Bill often feels annoyed by his colleague. The reasons that Bill finds his colleague annoying are the same as the reasons why you find Steve annoying sometimes (for example, both Bill's colleague and Steve make loud noises in the office). Steve says, \"Must be tough for Bill to have to deal with noisy colleagues all the time!\"\nYour reply to Steve: I know the feeling",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q8001d6b07f",
  "kind": "yes/no",
  "text": "FCC amateur radio licence exam: Amateur Extra class (Element 4) question pool 2024-2028.\nSubelement: Radio wave propagation.\n\nQuestion: Which of the following paths is most likely to support long-distance propagation on 160 meters?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?\nIs it wrong to answer \"A path entirely in darkness\"?",
  "definitions": "- A path entirely in darkness: Answer \"A path entirely in darkness\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- A path entirely in sunlight: Answer \"A path entirely in sunlight\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Paths at high latitudes: Answer \"Paths at high latitudes\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- A direct north-south path: Answer \"A direct north-south path\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q637d0b7fd2",
  "kind": "choice",
  "text": "Heading: Sasana\nI'm trying to figure out why Sasana is a redirect to England. I've read the note at Sasana which suggests it's an Irish word for England. Is that correct? All the pages that link to sasana look as though they should go to Śāsana, so I am inclined to change this to redirect to Śāsana.",
  "question": "Which Wikipedia Reference Desk should this question be posted to?",
  "options": [
   "Code 13",
   "Code 15",
   "Code 38",
   "Code 20",
   "Code 24",
   "Code 39"
  ],
  "definitions": "- Code 13: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Code 15: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Code 38: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Code 20: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Code 24: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Code 39: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software)."
 },
 {
  "qid": "q189413827e",
  "kind": "yes/no",
  "text": "An anxious mother brings her daughter into the clinic on her 5th birthday. She was forwarded a recent email by her aunt that stated that the pesticide-coated fruit in school lunches is the number one killer in children in the modern era. You assure her that that pesticides are not the number one killer, nor are they even in the top three killers of children in this age group. What are the top causes of death of American children aged 5-9, in order from most common to least?\n\nAnswer choices:\nA. Heart disease, malignant neoplasms, chronic lower respiratory disease\nB. Unintentional injury, congenital anomalies, homicide\nC. Unintentional injury, malignant neoplasms, congenital anomalies\nD. Malignant neoplasms, heart disease, unintentional injury\nE. Unintentional injury, suicide, malignant neoplasms\n\nProposed answer: C. Unintentional injury, malignant neoplasms, congenital anomalies",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q11b19e2382",
  "kind": "yes/no",
  "text": "Could you please explain to me what the buttons do? How do you \"Not accept\" a change, that's what...you revert it, don't you...?",
  "question": "Is this request from a Wikipedia editor to another editor impolite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the impolite side of the scale: blunt or challenging questions ('Why did you...?'), commands, accusations, impatience or sarcasm, with no greeting, thanks, apology or softening; insults are not required.\n- no: At most 1 of 5 raters placed it on the impolite side: the request is neutral and matter-of-fact or courteous (greeting, thanks, 'could you please', hedging), even if short or direct."
 },
 {
  "qid": "q74da5d3ffd",
  "kind": "yes/no",
  "text": "JOHN MACDOUGALL/AFP Contributor via Getty Images French President Emmanuel Macron, German <e1>Chancellor</e1> <e1>Angela Merkel</e1> and U.S. President Donald Trump confer at the start of the first working session of the G-20 meeting in <e2>Hamburg</e2>, Germany, on July 7, 2017.",
  "question": "Which relation from entity 1 (\"Chancellor\", marked <e1>) to entity 2 (\"Hamburg\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.\nIs it wrong to answer \"none of the listed relations\"?",
  "definitions": "- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction.\n- residence: Entity 2 is a place where entity 1, a person, lives or lived.\n- place of birth: Entity 2 is the place (city, town, region or country) where entity 1, a person, was born."
 },
 {
  "qid": "q83dc559fe0",
  "kind": "yes/no",
  "text": "Partner's previous message: Seems like we are in the same boat, the bear tore our tent to shreds so we are sleeping outside and it is cold☹️\nMessage: Sounds like a rough camping trip.  It has been pretty cold lately.",
  "question": "Which negotiation strategy does the Message use?\nIs the correct answer \"non-strategic\"?",
  "definitions": "- non-strategic: The utterance uses none of the listed strategies, for example plainly stating an offer, accepting, or handling logistics.\n- showing empathy: The speaker acknowledges the partner's personal situation positively or sympathetically, showing understanding or concern for their needs or circumstances.\n- stating no need: The speaker says they do not need an item, often citing their personal circumstances, signalling it can go to the partner.\n- own need: The speaker argues that they personally need an item, giving a reason from their own situation, such as health or conditions.\n- small talk: Rapport-building talk not about the deal itself, such as greetings, pleasantries, or chatting about the camping trip, weather or activities.\n- promoting coordination: The speaker promotes working together, for example an explicit promise to cooperate or a proposal framed as mutually beneficial for both sides."
 },
 {
  "qid": "q687c9b621b",
  "kind": "yes/no",
  "text": "Statement 1: Music can make people nervous.\nStatement 2: Music can relax people.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qfc11b5d09b",
  "kind": "yes/no",
  "text": "47 YO MALE THROWN OFF HORSE LANDED ON LOWER BACK DX L1 FRACTURE",
  "question": "Which OIICS event category describes how this worker's injury happened?\nIs it wrong to answer \"animal-ridden or non-motorized vehicle incident\"?",
  "definitions": "- animal-ridden or non-motorized vehicle incident: The worker was riding an animal or a non-motorized vehicle (horse, bull, bicycle, scooter, skateboard) and fell, was thrown or crashed.\n- explosion: An explosion, blast or sudden burst (of a container, tank, tire, battery, aerosol can or pressurized vessel) caused the injury, including burns or debris from it.\n- animal or insect related incident: An animal or insect caused the injury: bite, sting, scratch, kick, butt, trampling or being knocked over by an animal; falling from or being thrown by a ridden animal is a non-motorized vehicle incident instead.\n- roadway motor vehicle incident: The worker was a driver or passenger of a motorized vehicle in a crash, collision or rollover on a public road (a motor-vehicle crash), including hitting the inside of the vehicle during it.\n- repetitive motions involving microtasks: Pain or a disorder from repeating small, low-force motions over time (typing, keying, scanning, gripping, cutting, using the hands or wrists all day), with no single heavy exertion."
 },
 {
  "qid": "q8e4a172b2e",
  "kind": "choice",
  "text": "Focus gets great reviews but anecdotally have heard of tranny issues. Toyota always a safe bet but sounds like too gutless. Honda or Mazda.",
  "question": "How is the potential slur in this comment used?",
  "options": [
   "Code 20",
   "Code 52",
   "Code 47",
   "Code 45"
  ],
  "definitions": "- Code 20: The slur conveys contempt toward a targeted person or group: insults, labels, stand-alone slurs, sexualised use, generalisations about the community, or self-deprecation.\n- Code 52: The slur is mentioned rather than aimed at anyone - quoted, discussed as a word, recalled from an incident, used in counter-speech, or in sarcasm that mocks bigotry - by a speaker who is not reclaiming it.\n- Code 47: A member of the targeted group uses the slur with positive or neutral force about themselves or their community (empowerment, in-group solidarity, humour).\n- Code 45: The word is used in a non-slur sense, such as 'fag' meaning a cigarette or 'tranny' meaning a vehicle transmission."
 },
 {
  "qid": "q91f5a80c67",
  "kind": "choice",
  "text": "70,000 people were put in prison by the British in Kenya, and more than 5,000 of them are still alive. Many of them may sue the British government. The court decision may also make it possible for victims in other parts of the world to sue.\nThe Foreign Office said it will appeal against the decision. “The normal time limit for a civil action is three to six years,” they said. “In this case, that period has been extended to over 50 years, but the people who made the decisions are dead and they can’t give their view of what happened.”",
  "question": "This passage comes from a news article that English teachers rewrote for language learners at three reading levels. At which level is this passage written?",
  "options": [
   "elementary",
   "intermediate",
   "advanced"
  ],
  "definitions": "- elementary: The easiest rewrite (about CEFR A2-B1): short, mostly single-clause sentences, very common words, simple tenses, difficult terms explained or dropped, few idioms or long noun phrases.\n- intermediate: The middle rewrite (about B1-B2): moderately long sentences with some subordinate clauses, mostly everyday vocabulary with some less common words, lighter simplification of the original.\n- advanced: The original native-level newspaper text (about C1): long multi-clause sentences, rich or technical vocabulary, idioms, figurative language and dense reported speech, with no simplification."
 },
 {
  "qid": "qe3be2f52fe",
  "kind": "yes/no",
  "text": "Product: Skechers Shoes - black size 8 1/2 (category: Footwear)\nIncident description: after i bought the sketchers i began and continued to wear them for 4 weeks on my way to work and during work! first my feet began to hurt then my back went out and had to take a week out of work and lose the pay!",
  "question": "Based on this consumer product incident report, what was the most serious outcome for the primary victim on the SaferProducts.gov severity scale?\nIs it wrong to answer \"injury, no first aid or medical care\"?",
  "definitions": "- injury, no first aid or medical care: The primary victim was physically hurt (for example a small burn, cut, bruise or shock), but no first aid was given and no medical care was sought.\n- no incident, no injury: The report describes a hazard or defect that was noticed before anything happened: the product did not actually fail, burn, break or harm anyone during use.\n- injury, first aid by a non-medical person: The primary victim was hurt and was treated only by themselves or another lay person (ice, cold water, bandage, ointment, over-the-counter medicine), with no doctor, clinic or hospital.\n- death: The primary victim died from the incident, whether at the scene or later in hospital.\n- injury, seen by a medical professional: The primary victim's highest level of care was a doctor, urgent-care clinic, dentist, nurse or other medical professional outside an emergency department, with no hospital admission."
 },
 {
  "qid": "q83a178a2a6",
  "kind": "yes/no",
  "text": "FCC amateur radio licence exam: General class (Element 3) question pool 2023-2027.\nSubelement: Antennas and feed lines.\n\nQuestion: Which of the following would increase the bandwidth of a Yagi antenna?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?\nIs the correct answer \"Tapered-diameter elements\"?",
  "definitions": "- Tapered-diameter elements: Answer \"Tapered-diameter elements\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Larger-diameter elements: Answer \"Larger-diameter elements\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Loading coils in series with the element: Answer \"Loading coils in series with the element\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Closer element spacing: Answer \"Closer element spacing\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q7e8978b31c",
  "kind": "choice",
  "text": "Knobloch syndrome involving <e>midline scalp defect of the frontal region</e>.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"midline scalp defect of the frontal region\" (marked <e>) in this sentence?",
  "options": [
   "composite mention",
   "modifier",
   "disease class",
   "specific disease"
  ],
  "definitions": "- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "qd4cbbfdf71",
  "kind": "yes/no",
  "text": "Wikipedia page: Donald Glover\nSection: Film\nTable:\n| Year | Title | Role | Notes |\n| 2009 | Mystery Team | Jason Rogers | Also writer, composer and executive producer |\n| 2011 | The Muppets | Junior CDE Executive | Cameo |\n| 2013 | The To Do List | Derrick |  |\n| 2013 | Clapping for the Wrong Reasons | The Boy | Short film; also writer and executive producer |\n| 2014 | Alexander and the Terrible, Horrible, No Good, Very Bad Day | Greg |  |\n| 2014 | Chicken and Futility | The Boy | Short film; also writer and director |\n| 2015 | The Lazarus Effect | Niko |  |\n| 2015 | Magic Mike XXL | Andre |  |\n| 2015 | The Martian | Rich Purnell |  |\n| 2017 | Spider-Man: Homecoming | Aaron Davis |  |\n| 2018 | Solo: A Star Wars Story | Lando Calrissian |  |\n| 2019 | Guava Island | Deni Maroon | Also writer and producer |\n| 2019 | Donald Glover Presents | Himself | Series of short films; also writer |\n| 2019 | The Lion King | Simba (voice) | Post-production |\n\nClaim: Glover portrayed Lando Calrissian in Clapping for the Wrong Reasons (2018).",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q7b2b1ce031",
  "kind": "yes/no",
  "text": "National Trust blamed for visitors urinating on Avebury stones after deciding to close loos at 4pm",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q7507633172",
  "kind": "yes/no",
  "text": "Customer: Could I have the phone number please?\nAssistant: I'm sorry there is no phone number for that train.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q8f9361ae8d",
  "kind": "yes/no",
  "text": "The mid 2000s, especially the <e>United Kingdom</e> and the rest of Europe, saw the continued longevity of nineties boy bands such as Backstreet Boys and Westlife (before they disbanded in 2012), and the successful comeback of Take That in 2005, Boyzone in 2007, and New Kids on the Block in 2008.",
  "question": "In this music text, what type of entity is \"United Kingdom\" (marked <e>)?\nIs it wrong to answer \"award\"?",
  "definitions": "- award: A named prize, award or honour (e.g. 'Nobel Prize in Physics', 'Grammy Award', 'Hugo Award').\n- country: A named sovereign country or nation state (e.g. 'France', 'United States'), including historical countries.\n- musical artist: A named individual musician, singer, composer, rapper or DJ.\n- event: A named event such as a war, festival, conference, ceremony, competition or historical episode.\n- song: The title of a named song, single or other short musical piece.\n- band: A named band, music group, orchestra or choir (more than one performer)."
 },
 {
  "qid": "q8175bbe7ea",
  "kind": "choice",
  "text": "someone please tell mums that 🤱🏻 in public is not okay",
  "question": "Which option best describes this post?",
  "options": [
   "Option S",
   "Option M",
   "Option Q",
   "Option Z",
   "Option L"
  ],
  "definitions": "- Option S: The post is not hateful toward any protected group, even if it uses emoji, names a group, quotes or counters hate, or targets a non-protected entity.\n- Option M: The post explicitly demeans a protected group: negative claims about its members' character, abilities or appearance, or slurs and emoji used as slurs.\n- Option Q: The post expresses hostility toward a protected group implicitly or subtly - sarcasm, stereotypes, backhanded remarks or loaded questions - without explicit slurs or dehumanization.\n- Option Z: The post denies a protected group's humanity, likening its members to animals, insects, filth, disease or objects, often with animal or object emoji.\n- Option L: The post expresses intent or support for violence, harm or exclusion against a protected group, such as killing, attacking or expelling its members, often with weapon emoji."
 },
 {
  "qid": "qcb749b7ebd",
  "kind": "yes/no",
  "text": "Customer: I’d like to buy movie tickets for a theater near me in Davis, California.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I’ve heard No Time to Die is good, thinking about that one.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Is there no showtime near Davis, California?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh, bummer. What other action movies are playing in Davis, California?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the original one from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: Okay, thanks for the info. I don’t think I’ll be buying any tickets tonight since the movie I want isn’t playing near me.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q8b0a35a2b6",
  "kind": "choice",
  "text": "Sentence: The night <I> [drove] back home, I found that the rear window has some leakage.\nMarked event: [drove]\nMarked participant: <I>",
  "question": "In this sentence, how likely is it that the participant <I> existed before the [drove] event?",
  "options": [
   "Class P",
   "Class A",
   "Class J",
   "Class U",
   "Class Z"
  ],
  "definitions": "- Class P: Given the sentence, the property is clearly false for the participant in this event (scale point 1 of 5).\n- Class A: The property is probably false for the participant, though the sentence leaves some room for it (point 2 of 5).\n- Class J: The sentence gives no reason to think the property holds or fails; it is an even bet (point 3 of 5).\n- Class U: The property probably holds for the participant, though the sentence does not state it outright (point 4 of 5).\n- Class Z: Given the sentence, the property clearly holds for the participant in this event (point 5 of 5)."
 },
 {
  "qid": "qee40c0b4ca",
  "kind": "yes/no",
  "text": "Occupation: Low Vision Therapists, Orientation and Mobility Specialists, and Vision Rehabilitation Therapists\nDuties:\n- Examine patients to diagnose oral health conditions and diseases.\n- Replace missing teeth and associated oral structures with permanent fixtures, such as implant-supported prostheses, crowns and bridges, or removable fixtures, such as dentures.\n- Measure and take impressions of patients' jaws and teeth to determine the shape and size of dental prostheses, using face bows, dental articulators, recording devices, and other materials.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q814f6df2a7",
  "kind": "yes/no",
  "text": "The mouse mdx mutation affects muscle and confers a mild dystrophic syndrome, but it is not clear whether this mutation is equivalent to <e>Duchenne/Becker muscular dystrophy</e> in man.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"Duchenne/Becker muscular dystrophy\" (marked <e>) in this sentence?\nIs the correct answer \"composite mention\"?",
  "definitions": "- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "qf237395b1f",
  "kind": "yes/no",
  "text": "Customer: Yes please book that train, for 7 people. And may I get a reference number for the booking? Thanks.\nAssistant: sure thing your ref # is 7RBUS3T6, anything else today?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q964c88ea6b",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): Steve bought a really expensive pair of shoes as a treat to himself for having finished a big project at work. The shoes go very well with his outfit today.\nYour reply to Steve: Love the new shoes!",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q2411ad6151",
  "kind": "yes/no",
  "text": "Heading: assigning new functions to keys in Linux\nHi, I would like to know if there is a way to assign a new function to a key? For example, I want a key on the numeric key pad to function as the tab key so that I don't have to use my left hand to tap tab to navigate to another field while entering numerical data. Is there a way to do this, say on Mandriva?",
  "question": "Which Wikipedia Reference Desk should this question be posted to?\nIs the correct answer \"Science reference desk\"?",
  "definitions": "- Science reference desk: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software).\n- Computing reference desk: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Language reference desk: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Entertainment reference desk: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Mathematics reference desk: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Humanities reference desk: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs."
 },
 {
  "qid": "q6aa9859c1e",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Third Assistant Engineer), Steam Plants I.\n\nQuestion: The two-element feedwater regulator functions similarly to the three-element feedwater regulator, but does not utilize __________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "drum pressure",
   "water level",
   "steam flow measurement",
   "feedwater flow measurement"
  ],
  "definitions": "- drum pressure: Answer \"drum pressure\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- water level: Answer \"water level\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- steam flow measurement: Answer \"steam flow measurement\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- feedwater flow measurement: Answer \"feedwater flow measurement\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "q4649916f4c",
  "kind": "choice",
  "text": "He raised the 30 years of experience, so let me just talk briefly about that.",
  "question": "Which kind of statement is this sentence from a political debate?",
  "options": [
   "Non-factual statement",
   "Unimportant factual statement",
   "Check-worthy factual claim"
  ],
  "definitions": "- Non-factual statement: The sentence makes no factual claim that could be checked as true or false: it is a subjective opinion, belief or declaration, or a question.\n- Unimportant factual statement: The sentence does state a fact, but a trivial one (such as a small personal detail or a remark about the debate itself) that the public would not care to have verified and fact-checkers would skip.\n- Check-worthy factual claim: The sentence makes a factual claim that the general public would want to know is true or false and journalists would pick to fact-check, such as a voting record, a statistic, or what a policy did."
 },
 {
  "qid": "q5e5bb008b3",
  "kind": "yes/no",
  "text": "Problem:\nFind the minimum value of\n\\[\\sqrt{x^2 + (1 - x)^2} + \\sqrt{(1 - x)^2 + (1 + x)^2}\\]over all real numbers $x.$\n\nSolution steps so far:\nStep 1: This problem looks like it involves the distance formula, since the square root of the sum of squares is the distance from the origin to a point.\nStep 2: The expression has two square roots, each of which is the distance from the origin to a point on the plane.\nStep 3: The first one is the distance to the point $(x, 1 - x)$ and the second one is the distance to the point $(1 - x, 1 + x).$\n\nLast step (Step 4):\nThe expression is then the sum of these two distances, which is the length of the path from the origin to $(x, 1 - x)$ and then to $(1 - x, 1 + x).$",
  "question": "Does the last step of this partial solution contain a mistake or other flaw that makes it a bad step?",
  "definitions": "- yes: The last step is a bad step: it states something mathematically wrong (even if most of it is right), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a final answer that is wrong or not justified by a complete solution.\n- no: The last step has no such flaw: everything it states is correct, quickly verifiable and fits the earlier steps; this includes steps that only restate, stall or try a reasonable approach that may not pan out, and steps that catch an earlier slip."
 },
 {
  "qid": "q4d7a7a140b",
  "kind": "yes/no",
  "text": "36YOM POLICE OFFICER RIDING BICYCLE WHILE ON PATROL WHEN CAR RAN IN FRONT OF HIM AND HE HIT THE CAR DX ABRASION TO KNEE",
  "question": "Which OIICS event category describes how this worker's injury happened?\nIs it wrong to answer \"animal-ridden or non-motorized vehicle incident\"?",
  "definitions": "- animal-ridden or non-motorized vehicle incident: The worker was riding an animal or a non-motorized vehicle (horse, bull, bicycle, scooter, skateboard) and fell, was thrown or crashed.\n- exposure to radiation or noise: Radiation or noise caused the injury: welding arc flash burns to the eyes, ultraviolet or laser light, ionizing radiation, or loud noise damaging hearing.\n- struck, caught or crushed in collapsing structure or material: A collapsing structure or material struck, caught or buried the worker: trench or excavation cave-in, or collapse of a ceiling, wall, floor, scaffold or stacked material not set off by an explosion or fire.\n- fall to lower level: The worker fell from a higher place to a lower one: off a ladder, roof, scaffold, stool, chair, vehicle, dock or platform, down stairs or steps, or into a hole, pit or trench.\n- roadway motor vehicle incident: The worker was a driver or passenger of a motorized vehicle in a crash, collision or rollover on a public road (a motor-vehicle crash), including hitting the inside of the vehicle during it."
 },
 {
  "qid": "qb55abaa984",
  "kind": "choice",
  "text": "The novel porous octahedral <e1>Cu</e1> microcrystals were synthesized successfully by a simple <e2>one</e2>-step hydrothermal reduction method based on TEA technique.",
  "question": "Which relation from entity 1 (\"Cu\", marked <e1>) to entity 2 (\"one\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "time-weighted average exposure limit",
   "oxidation state",
   "none of the listed relations"
  ],
  "definitions": "- time-weighted average exposure limit: Entity 2 is the permissible time-weighted average (e.g. 8-hour) workplace exposure limit for entity 1, a chemical substance.\n- oxidation state: Entity 2 is an oxidation state (e.g. +2, -1) that entity 1, a chemical element, has or can take.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q9d582ac935",
  "kind": "yes/no",
  "text": "Customer: hi, i am trying to access my account but i lost my phone so i can't do the 2 step process\nCustomer: Chloe Zhang\nCustomer: Username: chloez33",
  "question": "Which broad category of customer-service issue is the customer contacting support about?\nIs it wrong to answer \"account access\"?",
  "definitions": "- account access: The customer cannot get into their account and needs help recovering their username or password, or resetting two-factor authentication.\n- purchase dispute: The customer disputes a purchase: a lower price elsewhere or yesterday, items out of stock, a promo code that fails, or a charge they believe is wrong.\n- order issue: The customer asks about or wants to change an existing order: unexpected fees, delivery time, payment method, quantity, shipping speed, or adding and removing items.\n- shipping issue: The customer asks about a shipment: its status after a confusing notification, changing its address or item, an item that never arrived, or high shipping cost.\n- manage account: The customer asks about services added to or removed from their account, missing credit or account shipping perks, or wants to change profile details."
 },
 {
  "qid": "q0660929742",
  "kind": "yes/no",
  "text": "Situation: I want my history teacher\nAction being judged: Having a crush on one of your teachers when you're a teen as long as you don't act on it.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q2f19a57ce5",
  "kind": "choice",
  "text": "Trivia question (category: Geography).\n\nQuestion: What is the longest river in Europe?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Option L",
   "Option S",
   "Option F",
   "Option G"
  ],
  "definitions": "- Option L: Answer \"Volga\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option S: Answer \"Thames\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option F: Answer \"Danube\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option G: Answer \"Rhine\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qe532e52bb3",
  "kind": "yes/no",
  "text": "Statement 1: the modern city is more agricultural than the countryside\nStatement 2: the modern city is more industrialized than the countryside",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qaf932b9064",
  "kind": "yes/no",
  "text": "Wikipedia page: Pravasi Bharatiya Divas\nSection: Venues\nTable:\n| Day | Year | Venue | State |\n| 1st | 2003 | New Delhi | Delhi |\n| 2nd | 2004 | New Delhi | Delhi |\n| 3rd | 2005 | Mumbai | Maharashtra |\n| 4th | 2006 | Hyderabad | Andhra Pradesh (Now in Telangana) |\n| 5th | 2007 | New Delhi | Delhi |\n| 6th | 2008 | New Delhi | Delhi |\n| 7th | 2009 | Chennai | Tamil Nadu |\n| 8th | 2010 | New Delhi | Delhi |\n| 9th | 2011 | New Delhi | Delhi |\n| 10th | 2012 | Jaipur | Rajasthan |\n| 11th | 2013 | Kochi | Kerala |\n| 12th | 2014 | New Delhi | Delhi |\n| 13th | 2015 | Gandhinagar | Gujarat |\n| 14th | 2017 | Bengaluru | Karnataka |\n| 15th | 2019 | Varanasi | Uttar Pradesh |\n\nClaim: The 13th Pravasi Bharatiya Divas was held during 2015 in Gandhinagar, Gujarat.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q3665f6fb26",
  "kind": "yes/no",
  "text": "Detection of 98% of <e>DMD</e>/BMD gene deletions by polymerase chain reaction.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"DMD\" (marked <e>) in this sentence?\nIs the correct answer \"modifier\"?",
  "definitions": "- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers')."
 },
 {
  "qid": "q769f3dddf8",
  "kind": "choice",
  "text": "Premise:\nTitle: Evan Rachel Wood\nBorn: ( 1987-09-07 ) September 7, 1987 (age 31) Raleigh, North Carolina, U.S.\nOccupation: Actress, model, musician\nYears active: 1994 - present\nSpouse(s): Jamie Bell ( m. 2012; div. 2014)\nChildren: 1\nHypothesis: Evan Rachel Wood's career has spanned 25 years so far.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q3c76c9d70b",
  "kind": "yes/no",
  "text": "Situation: He worked overtime so she could have a big party.\nAction being judged: Having a big party while someone's working overtime to allow you to do it.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qc08543615f",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Ramy Rabia\nSentence: Ramy Hisham Abdel Aziz Rabia (Arabic: رامي ربيعة‎; born 20 May 1993) is an Egyptian professional footballer who plays as a centre-back for Egyptian Premier League club Al Ahly and the Egypt national football team.\n\nClaim: Ramy Rabia is an Algerian professional footballer who played for the Egypt National Football Team from 2012 to 2019 and made a total of 23 apps and 3 goals.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q7a600aff19",
  "kind": "yes/no",
  "text": "This woman was gifted a karaoke mic and did the absolute most",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q468c74e0fb",
  "kind": "yes/no",
  "text": "I, and a number of other scientists, believe that nature has a thermostatic control mechanism that pushes back against a warming influence, such as the relatively weak warming from more atmospheric carbon dioxide. (The direct warming effect of more CO 2 would amount to little more than 1 deg. F by late in this century, and is generally not the subject of debate.)",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qa751a1e5ff",
  "kind": "choice",
  "text": "Sentence: Planning on [going] to North and South Island.\nMarked event or state: [going]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.",
  "options": [
   "Class B",
   "Class N",
   "Class S",
   "Class K",
   "Class H",
   "Class Q",
   "Class X",
   "Class L",
   "Class C",
   "Class D",
   "Class Z"
  ],
  "definitions": "- Class B: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot).\n- Class N: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- Class S: Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).\n- Class K: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- Class H: Lasts from about one day up to under a week (a trip, an illness, a weekend event).\n- Class Q: Lasts from about one week up to under a month (a vacation, a short course, a hospital stay).\n- Class X: Lasts from about one month up to under a year (a season, a project, a pregnancy).\n- Class L: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- Class C: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- Class D: Lasts a hundred years or more but has a beginning or end (an institution, a tradition, an empire).\n- Class Z: Has no bounded duration: permanent, timeless or generic states and truths (being a species, a mathematical fact, a general rule)."
 }
]
