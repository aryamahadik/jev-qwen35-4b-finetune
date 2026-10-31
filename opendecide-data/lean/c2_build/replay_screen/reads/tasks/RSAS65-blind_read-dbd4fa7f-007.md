# A46 replay label-noise blind read RSAS65-blind_read-dbd4fa7f-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS65-blind_read-dbd4fa7f-007.json

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
  "qid": "qd3ab065a86",
  "kind": "yes/no",
  "text": "Situation: One day as we were playing, my sister fell and cut up her feet.\nAction being judged: Being careful when playing so as not to get hurt.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q5622330269",
  "kind": "yes/no",
  "text": "I have always maintained a control of the military section and I can check up the names in the educational section. Which section would you like to clean-up?",
  "question": "How polite is this request?\nIs it wrong to answer \"polite\"?",
  "definitions": "- polite: Among the most polite requests (top quarter as rated by annotators): clearly more courteous than a typical request, usually combining several cues such as greeting, thanks, apology, praise or deference ('great work on...'), hedging ('I think', 'perhaps') and indirect phrasing ('would you mind', 'could you please'). A single 'could you' alone is not enough.\n- impolite: Among the least polite requests (bottom quarter as rated by annotators): noticeably blunter than a typical request, e.g. challenging direct questions ('Why did you...?', 'What is this?'), commands (including a bare sentence-initial 'Please ...' used as an order), accusations, sarcasm or impatience ('???'), openings like 'So' or 'You', and no greeting, thanks, apology or softening. It need not contain insults.\n- neutral: A typical, middle-of-the-road request (the middle half of ratings): plain matter-of-fact wording, or only one mild courtesy such as a single 'can/could you' or 'please' without warmth, or polite and blunt cues that roughly cancel out."
 },
 {
  "qid": "qba8f8941e1",
  "kind": "yes/no",
  "text": "Add song to library",
  "question": "What does the user want the music player to do?\nIs the correct answer \"Like the music\"?",
  "definitions": "- Like the music: The user approves of a song, artist or channel so it is marked as liked: a thumbs up, favouriting it, or saving it to their library.\n- Remove or block music: The user asks to remove a song, artist or genre from a playlist or from what gets played, e.g. 'don't play this song again' or 'no rap music'.\n- Pause the music: The user asks to pause playback temporarily so it can be resumed from the same point.\n- Skip to the next track: The user asks to skip the current song and move forward to the next or a later track.\n- Add to a playlist: The user asks to add a song, artist or album to an existing playlist."
 },
 {
  "qid": "q1103b12f58",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nAmong the MIS-C cohort, 17 (68%) children were SARS-CoV-2 seropositive, suggesting previous SARS-CoV-2 infections14,15, and these children had more severe disease.\n\nClaim: The immune cells of children acutely ill with MIS-C behaved the same as adults with COVID-19.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q8876acdd13",
  "kind": "yes/no",
  "text": "#sp Facebook Job-Hunting App <e>BranchOut</e> Raises $6 Million From Accel And Super Angels: When you want to hang out ... http://migre.me/1kO1K",
  "question": "What type of named entity is \"BranchOut\" (marked <e>) in this post?\nIs it wrong to answer \"Code 18\"?",
  "definitions": "- Code 18: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- Code 27: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- Code 12: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- Code 59: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- Code 50: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product."
 },
 {
  "qid": "q60915c6e79",
  "kind": "choice",
  "text": "Study B305 was conducted in Australia, Austria, Canada, <e1>France</e1>, Germany, <e2>Italy</e2>, South Africa and the United Kingdom; centres contributing patients started in February 1995 and the study was terminated in August 2000.",
  "question": "Which relation from entity 1 (\"France\", marked <e1>) to entity 2 (\"Italy\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "shares border with",
   "diplomatic relation",
   "none of the listed relations"
  ],
  "definitions": "- shares border with: The sentence states that entity 1 and entity 2 (countries, regions or places) share a common border ('bordered by', 'neighbouring'); being mentioned together does not count.\n- diplomatic relation: The sentence states that entity 1 and entity 2, two states, have official state-to-state relations (embassies, ambassadors, treaties, alliances, state visits); merely naming both countries does not count.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q2c16118d9a",
  "kind": "yes/no",
  "text": "Jane chose to write about dolphins instead of bears for her thesis, although _ were her strongest area of expertise.\n\nThe blank (_) stands for one of two candidates: \"dolphins\" or \"bears\".",
  "question": "Does the blank (_) in the sentence stand for \"bears\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qc6c783e917",
  "kind": "choice",
  "text": "Trivia question (category: Entertainment: Music).\n\nQuestion: Which of these songs from American Idiot: The Musical was a previously unreleased Green Day song?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Before The Lobotomy",
   "Favorite Son",
   "Are We The Waiting",
   "When It's Time"
  ],
  "definitions": "- Before The Lobotomy: Answer \"Before The Lobotomy\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Favorite Son: Answer \"Favorite Son\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Are We The Waiting: Answer \"Are We The Waiting\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- When It's Time: Answer \"When It's Time\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qf6980ea801",
  "kind": "choice",
  "text": "Trivia question (category: General Knowledge).\n\nQuestion: In a standard Gregorian calendar, how many months begin with the letter 'J'?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Three",
   "Two",
   "Five",
   "Four"
  ],
  "definitions": "- Three: Answer \"Three\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Two: Answer \"Two\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Five: Answer \"Five\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Four: Answer \"Four\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qcb9302fc76",
  "kind": "choice",
  "text": "Duties:\n- Supervise nurses' aides or assistants.\n- Work as part of a healthcare team to assess patient needs, plan and modify care, and implement interventions.\n- Administer prescribed medications or start intravenous fluids, noting times and amounts on patients' charts.",
  "question": "Which occupation performs all of the listed duties?",
  "options": [
   "Dietetic Technicians",
   "Licensed Practical and Licensed Vocational Nurses",
   "Veterinary Technologists and Technicians"
  ],
  "definitions": "- Dietetic Technicians: Assist in the provision of food service and nutritional programs, under the supervision of a dietitian. May plan and produce meals based on established guidelines, teach principles of food and nutrition, or counsel individuals.\n- Licensed Practical and Licensed Vocational Nurses: Care for ill, injured, or convalescing patients or persons with disabilities in hospitals, nursing homes, clinics, private homes, group homes, and similar institutions. May work under the supervision of a registered nurse. Licensing required.\n- Veterinary Technologists and Technicians: Perform medical tests in a laboratory environment for use in the treatment and diagnosis of diseases in animals. Prepare vaccines and serums for prevention of diseases. Prepare tissue samples, take blood samples, and execute laboratory tests, such as urinalysis and blood counts. Clean and sterilize instruments and materials and maintain equipment and machines. May assist a veterinarian during surgery."
 },
 {
  "qid": "q7eb53ab9dd",
  "kind": "choice",
  "text": "Infobox:\nTitle: Fala\nOther name(s): Murray the Outlaw of Falahill (full name)\nSpecies: Dog\nBreed: Scottish Terrier\nSex: Male\nBorn: Big Boy ( 1940-04-07 ) April 7, 1940\nDied: April 5, 1952 (1952-04-05) (aged 11)\nResting place: Springwood\nOccupation: Presidential pet\nOwner: Franklin D. Roosevelt, Eleanor Roosevelt\nNamed after: John Murray of Falahill\n\nHypothesis: The dog Fala passed away at 15 years old.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Option J",
   "Option K",
   "Option Y"
  ],
  "definitions": "- Option J: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Option K: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Option Y: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q637dfcf215",
  "kind": "yes/no",
  "text": "Beginning: Ronald is tired but passes by Starbucks. He ...\n\nPossible endings:\n(A) stops being tired\n(B) exercises so he can wake up\n(C) buys himself water\n(D) gets coffee",
  "question": "Which listed ending continues the beginning most sensibly?\nIs it wrong to answer \"Option Z\"?",
  "definitions": "- Option Z: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Option W: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Option G: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Option R: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "qc60c2b1bca",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Finn Wiberg\nTable (caption: Finn Wiberg):\n| Personal information | Personal information | Personal information | Personal information |\n| ... |\n| Place of birth | Denmark | Denmark | Denmark |\n| Playing position(s) | Striker | Striker | Striker |\n| Senior career* | Senior career* | Senior career* | Senior career* |\n| ... |\n| 1970–1972 | AS Nancy | 66 | (16) |\n| 1972–1974 | FC Biel |  |  |\n\nClaim: Finn Wiberg, who was born in Denmark, primarily plays as a striker and has played for FC Biel and AS Nancy.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "q52004eeefb",
  "kind": "yes/no",
  "text": "The car luckily missed the house, but hit the cart, so the _ ended up being destroyed.\n\nThe blank (_) stands for one of two candidates: \"cart\" or \"house\".",
  "question": "Does the blank (_) in the sentence stand for \"house\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qa156369e90",
  "kind": "yes/no",
  "text": "Top kek. OP is faggot confirmed",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "qd697fcf679",
  "kind": "yes/no",
  "text": "When they were approached by a known bully Jeffrey stood up to them but Samuel ran away as _ is a strong person.\n\nThe blank (_) stands for one of two candidates: \"Jeffrey\" or \"Samuel\".",
  "question": "Does the blank (_) in the sentence stand for \"Jeffrey\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q2b7016c8b6",
  "kind": "yes/no",
  "text": "Premise:\nTitle: Diana and Actaeon\nArtist: Titian\nYear: 1556-1559\nMedium: Oil on canvas\nDimensions: 185 cm 202 cm (73 in 80 in)\nLocation: National Gallery, London\nHypothesis: Diana and Actaeon was finished in 1559.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?\nIs the correct answer \"Contradiction\"?",
  "definitions": "- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true.\n- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true."
 },
 {
  "qid": "qb31caddd97",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: Technician class (Element 2) question pool 2026-2030.\nSubelement: Safety.\n\nQuestion: Which is a proper grounding method for a tower?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Class K",
   "Class B",
   "Class D",
   "Class R"
  ],
  "definitions": "- Class K: Answer \"A single four-foot ground rod, driven into the ground no more than 12 inches from the base\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class B: Answer \"A ferrite-core RF choke connected between the tower and ground\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class D: Answer \"A connection between the tower base and a cold-water pipe\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class R: Answer \"Separate eight-foot ground rods for each tower leg, bonded to the tower and each other\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q0bbf533f86",
  "kind": "yes/no",
  "text": "Science facts table (first row is the header):\n| HUMAN ACTIVITY |  | ENVIRONMENTAL HARM |  |\n| ... |\n| swimming in a lake | is | harmless | to the environment |\n| ... |\n| animals | is | helpful | to the environment |\n| ... |\n| bees | is | helpful | to the environment |\n| ... |\n| building roads | is | harmful | to the environment |\n| ... |\n| burning fossil fuels | is | harmful | to the environment |\n| ... |\n| cities | is | harmful | to the environment |\n| clearance of surrounding rainforests | is | harmful | to the environment |\n| ... |\n| destruction of the ozone layer | is | harmful | to the environment |\n| ... |\n| erosion prevention | is | helpful | to the environment |\n| ... |\n| farms | is | harmful | to the environment |\n| ... |\n| habitat loss | is | harmful | to the environment |\n| ... |\n| human interaction with ocean | is | harmful | to the environment |\n| ... |\n| sunlight | is | helpful | to the environment |\n| ... |\n| weathering | is | helpful | to the environment |\n\nQuestion: Farms are what to the environment?\nProposed answer: Harmful",
  "question": "According to the table of facts, is the proposed answer to the question correct?",
  "definitions": "- yes: The table's row for the fact the question asks about gives exactly the proposed answer (same entity, value or property), so it answers the question correctly.\n- no: The table shows the proposed answer belongs to a different row or fact than the one the question asks about, so it does not answer the question."
 },
 {
  "qid": "qce33032993",
  "kind": "yes/no",
  "text": "Consumer health question:\nWhat is Flu?\n\nPassage:\nWhat is Flu?: The flu is an infection of the nose, throat, and lungs. It spreads easily. This article discusses influenza types A and B. Another type of the flu is the swine flu (H1N1).",
  "question": "Does the passage correctly answer the consumer's health question?",
  "definitions": "- yes: The passage gives a correct answer to what the consumer actually asked, either completely or correctly but incompletely (it covers part of the requested information, such as some of the treatments or symptoms asked about).\n- no: The passage does not answer the question: it is only related to the topic (right disease or drug but the wrong aspect, e.g. causes when treatment was asked, or page metadata), or it is about something else or gives incorrect information."
 },
 {
  "qid": "qbdf7c5d829",
  "kind": "yes/no",
  "text": "Wikipedia page: Portageville, Missouri\nSection: Demographics\nTable:\n| Historical population | Historical population | Historical population | Historical population |\n| Census | Pop. |  | %± |\n| 1880 | 73 |  | — |\n| 1900 | 427 |  | — |\n| 1910 | 987 |  | 131.1% |\n| 1920 | 1,244 |  | 26.0% |\n| 1930 | 1,262 |  | 1.4% |\n| 1940 | 2,107 |  | 67.0% |\n| 1950 | 2,662 |  | 26.3% |\n| 1960 | 2,505 |  | −5.9% |\n| 1970 | 3,117 |  | 24.4% |\n| 1980 | 3,470 |  | 11.3% |\n| 1990 | 3,401 |  | −2.0% |\n| 2000 | 3,295 |  | −3.1% |\n| 2010 | 3,228 |  | −2.0% |\n| Est. 2016 | 3,109 |  | −3.7% |\n| source: | source: | source: | source: |\n\nClaim: As of the census of 2000, there were 3,295 people residing in Portageville.",
  "question": "Is the claim contradicted by the table?",
  "definitions": "- yes: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name).\n- no: The claim is supported: every fact matches the table and its page and section titles, with each value paired with the right row and column."
 },
 {
  "qid": "q32e6c580e0",
  "kind": "yes/no",
  "text": "623 Uris Hall, Graduate School of Business, Columbia University, <e1>New York</e1>, NY 10027, <e2>USA</e2>.",
  "question": "Which relation from entity 1 (\"New York\", marked <e1>) to entity 2 (\"USA\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.\nIs the correct answer \"none of the listed relations\"?",
  "definitions": "- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction.\n- country: Entity 2 is the sovereign country in which entity 1 (a place, building, organisation, event or object, not a person) is located or to which it belongs.\n- capital of: Entity 1 is the capital city or seat of government of entity 2 (a country, state, province or region)."
 },
 {
  "qid": "qfca1063b64",
  "kind": "yes/no",
  "text": "Shellfish fishing (e.g., clam, crab, oyster, shrimp)",
  "question": "Which NAICS 2022 subsector does a business whose primary activity is described here belong to?\nIs it wrong to answer \"Code 16\"?",
  "definitions": "- Code 16: Catching or taking fish, shellfish and other wild animals from their natural habitat: commercial fishing, hunting and trapping.\n- Code 31: Services performed for farms, ranches and forests on a fee or contract basis, such as harvesting, crop dusting, postharvest cleaning, cooling and packing, cotton ginning, breeding or forest fire fighting.\n- Code 12: Providing telecommunications services: wired, wireless and satellite communications and resellers of such services.\n- Code 39: Amusement parks and arcades, gambling establishments, and other recreation facilities such as golf courses, marinas, fitness centers and bowling centers.\n- Code 59: Collecting, treating and disposing of waste, remediation of contaminated sites, and material recovery facilities."
 },
 {
  "qid": "q29394f329e",
  "kind": "yes/no",
  "text": "The groundbreaking Time cover came 10 months after Cox appeared in her breakout role as Sophia Burset on <e2>Netflix</e2>'s <e1>Orange Is the New Black</e1>.",
  "question": "Which relation from entity 1 (\"Orange Is the New Black\", marked <e1>) to entity 2 (\"Netflix\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.\nIs it wrong to answer \"Class N\"?",
  "definitions": "- Class N: Entity 2 is the TV or radio network or channel that originally broadcast entity 1.\n- Class J: Entity 2 distributes entity 1 (a film, product or publication) to the market.\n- Class H: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q15dec7fb86",
  "kind": "yes/no",
  "text": "How can you observe Ramadan when the sun never goes down?",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q1ec6213688",
  "kind": "yes/no",
  "text": "This is good advice. They also share the lug pattern with civics for more options to hunt for wheels if you dont like the basketweaves OP. Those are the US ellipsoid headlights though, not the smilies. 55w will also perform just fine in the low beams. I've been using them for almost 3 years now on my E30, just make sure they're aimed properly.\n\n@OP: Saying \"all it needs\" is kind of an overstatement IMO. This car does need a little TLC, which is obvious, but the tranny is a good start. If you're not well versed on these cars already, have it checked out by someone who is to make sure you're not getting yourself in over your head. These cars can get expensive fast, and an iX isn't cheap to find parts for.",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q358e532365",
  "kind": "choice",
  "text": "Can I you take a look at <url> and <url>? Specifically, look at the formatting of the general reference; is it an acceptable way to present the references?",
  "question": "How polite is this request?",
  "options": [
   "Option R",
   "Option J",
   "Option U"
  ],
  "definitions": "- Option R: Among the least polite requests (bottom quarter as rated by annotators): noticeably blunter than a typical request, e.g. challenging direct questions ('Why did you...?', 'What is this?'), commands (including a bare sentence-initial 'Please ...' used as an order), accusations, sarcasm or impatience ('???'), openings like 'So' or 'You', and no greeting, thanks, apology or softening. It need not contain insults.\n- Option J: A typical, middle-of-the-road request (the middle half of ratings): plain matter-of-fact wording, or only one mild courtesy such as a single 'can/could you' or 'please' without warmth, or polite and blunt cues that roughly cancel out.\n- Option U: Among the most polite requests (top quarter as rated by annotators): clearly more courteous than a typical request, usually combining several cues such as greeting, thanks, apology, praise or deference ('great work on...'), hedging ('I think', 'perhaps') and indirect phrasing ('would you mind', 'could you please'). A single 'could you' alone is not enough."
 },
 {
  "qid": "qfb21bdd664",
  "kind": "yes/no",
  "text": "Situation: Co-Worker Takes 'Nice' Too Far\nAction being judged: Embracing an exaggerated persona.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q83ea5fcf6f",
  "kind": "yes/no",
  "text": "FAQ entry (restaurant: Rajmahal)\nQ: Does Rajmahal offer wheelchair access?\nA: Rajmahal is not wheelchair accessible.\n\nCustomer question: Does they have disability access for me?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "qae2395e544",
  "kind": "yes/no",
  "text": "Assistant: No, that is all they need. Should I submit the appointment request?\nCustomer: Yes, go ahead and submit it. Just let me know if any sooner appointments come up. Otherwise the 6pm slot will work just fine.\nAssistant: Alright. You are all booked! It will be this evening at 6pm for your Subaru Impreza 2013 at the Intelligent Auto Solutions.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa35bc1c98d",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Third Assistant Engineer), Motor Plants II.\n\nQuestion: Which of the turbocharging systems listed operates with the least average back pressure in the exhaust manifold?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Constant volume",
   "Constant pressure",
   "Pulse pressure",
   "Radial flow"
  ],
  "definitions": "- Constant volume: Answer \"Constant volume\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Constant pressure: Answer \"Constant pressure\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Pulse pressure: Answer \"Pulse pressure\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Radial flow: Answer \"Radial flow\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qd21a415ed3",
  "kind": "yes/no",
  "text": "U.S. Coast Guard merchant mariner credential exam (Second/Third Mate of Unlimited Tonnage), Navigation General – Near Coastal.\n\nQuestion: Which is TRUE when navigating a vessel?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?\nIs the correct answer \"Option V\"?",
  "definitions": "- Option V: Answer \"You should never rely on a floating aid to maintain its exact position\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option R: Answer \"You can always rely on a buoy to show proper light characteristics\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option Q: Answer \"You can always rely on a buoy to be on station\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option P: Answer \"You should assume a wreck buoy is directly over the wreck\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q34fd4bdb57",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Sir John Hurt (CBE)\nBorn: John Vincent Hurt ( 1940-01-22 ) 22 January 1940 Chesterfield, Derbyshire, England\nDied: 25 January 2017 (2017-01-25) (aged 77) Cromer, Norfolk, England\nEducation: Lincoln School\nAlma mater: Royal Academy of Dramatic Art\nOccupation: Actor, voice actor, narrator\nYears active: 1961 - 2017\nSpouse(s): Annette Robertson ( m. 1962; div. 1964), Donna Peacock ( m. 1984; div. 1990), Joan Dalton ( m. 1990; div. 1996), Anwen Rees-Myers ( m. 2005)\nChildren: 2\n\nHypothesis: John Hurt died in a different country than he was born.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q77225dc624",
  "kind": "yes/no",
  "text": "Erin sat on a throne in the castle as Monica did funny things to make them laugh since _ is a jester.\n\nThe blank (_) stands for one of two candidates: \"Erin\" or \"Monica\".",
  "question": "Does the blank (_) in the sentence stand for \"Monica\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q02f7de9352",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Reactivity Coefficients.\n\nQuestion: In a comparison of the fuel temperature coefficient at the beginning and end of a fuel cycle, the fuel temperature coefficient is more negative at the __________ of a fuel cycle because __________. (Assume the same initial fuel temperature throughout the fuel cycle.)",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs it wrong to answer \"Option S\"?",
  "definitions": "- Option S: Answer \"beginning; more U-238 is in the core\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- Option X: Answer \"end; more Pu-240 is in the core\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- Option V: Answer \"end; more fission product poisons are in the core\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- Option C: Answer \"beginning; less fission product poisons are in the core\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong."
 },
 {
  "qid": "qeb6b5f7da2",
  "kind": "yes/no",
  "text": "Storm drain NOT DRAINING, major hazard and land erosion",
  "question": "Which City of San Diego 311 request type (and so which crew) should this resident's report be routed to?\nIs it wrong to answer \"Code 25\"?",
  "definitions": "- Code 25: A street light that is out, flickering, on during the day, or whose pole is knocked down or damaged; traffic signals are not street lights.\n- Code 16: A storm drain, inlet, grate, culvert or drainage channel that is clogged, full of debris or damaged.\n- Code 10: A rented dockless scooter or e-bike left blocking a sidewalk, parked illegally, dumped or damaged; the operator is told to move it.\n- Code 49: Street or alley surface that is cracked, crumbling, sunken, uneven or worn and needs asphalt repair or resurfacing, rather than one discrete pothole.\n- Code 24: Graffiti on public right-of-way property (streets, sidewalks, curbs, signs, poles, utility boxes, bridges, alleys), removed by the City's graffiti crew, when the report does not place it on private property.\n- Code 13: Weeds, tall grass or dry brush growing on public land (medians, canyons, city lots, road edges) that need clearing, often as a fire risk."
 },
 {
  "qid": "q5e97169f50",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In the 2021 general election, De Mos attempted to return to the House of Representatives as \"lijsttrekker\" of the party Code Orange.\n\nSummary sentence:\nHe was the \"lijsttrekker\" for Code Orange in the 2021 general election.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qcb555a54b6",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: General class (Element 3) question pool 2023-2027.\nSubelement: Radio wave propagation.\n\nQuestion: How long does it take a coronal mass ejection to affect radio propagation on Earth?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Code 15",
   "Code 18",
   "Code 12",
   "Code 57"
  ],
  "definitions": "- Code 15: Answer \"28 days\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 18: Answer \"14 days\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 12: Answer \"4 to 8 minutes\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 57: Answer \"15 hours to several days\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qe1fd46a72d",
  "kind": "yes/no",
  "text": "Most popular states retirees move to",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q4d29766273",
  "kind": "choice",
  "text": "Chatbot: Can you elaborate on that?\nUser: Let me put my penis into your vagaina.\nChatbot: Why do you say your penis into my vagaina?\nUser: Because that is called sex",
  "question": "What kind of abuse is in the user's last message?",
  "options": [
   "Code 11",
   "Code 21",
   "Code 40",
   "Code 58",
   "Code 22",
   "Code 35",
   "Code 47"
  ],
  "definitions": "- Code 11: The abuse is sexual: unwanted sexual advances, explicit sexual requests or descriptions, or sexualised comments directed at the chatbot or someone else.\n- Code 21: The abuse targets gender: it demeans women or men as a group, uses gendered slurs, or attacks the chatbot or someone because of perceived gender.\n- Code 40: The abuse attacks intelligence or competence: calling the chatbot or someone stupid, dumb, useless or incapable of understanding.\n- Code 58: The abuse targets sexual orientation: homophobic slurs or insults, or treating being gay or lesbian as shameful or as an insult.\n- Code 22: The abuse targets race, ethnicity or nationality: racial slurs, racist stereotypes, or demeaning remarks about a racial or ethnic group.\n- Code 35: The abuse targets disability: using disability or mental illness as an insult, such as 'retard', or demeaning people with disabilities.\n- Code 47: The abuse fits none of the specific types: general swearing, name-calling, telling someone to go away, or other hostility not based on sex, gender, sexual orientation, race, disability or intelligence."
 },
 {
  "qid": "q023d9dc2b2",
  "kind": "yes/no",
  "text": "FAQ entry (restaurant: Don Pasquale Pizzeria)\nQ: Do you have any options for a vegetarian?\nA: You can find vegetarian options at this restaurant.\n\nCustomer question: Does Don Pasquale Pizzeria offer vegan menu items?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "q57607186b0",
  "kind": "yes/no",
  "text": "After reading over the comments there, the first guy that said tranny was using it completely without reference to transgender people, but then about half of the comments afterward were actually fairly offensive.",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "qd936782c85",
  "kind": "yes/no",
  "text": "Nigger Coon  Mods be steady Nogin.",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q2bbe4c125e",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Jacques Cousteau\nBorn: 11 June 1910 Saint-Andre-de-Cubzac, France\nBirth name: Jacques-Yves Cousteau\nDied: 25 June 1997 (aged 87) Paris, France\nNationality: French\nOccupation: Oceanographer\nSpouse(s): Simone Melchior Cousteau (1937-1990, her death), Francine Triplet Cousteau (1991-1997)\nChildren: Jean-Michel, Philippe Cousteau, Diane, Pierre-Yves\n\nHypothesis: Jacques Cousteau did not ever have any children.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?\nIs it wrong to answer \"Contradiction\"?",
  "definitions": "- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q4fb39ae846",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), BWR question bank, topic: Heat Transfer and Heat Exchangers.\n\nQuestion: A counterflow lube oil heat exchanger is in operation when the cooling water flow rate is reduced to one-half its original value. Which one of the following will decrease as a result?",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs the correct answer \"Lube oil outlet temperature\"?",
  "definitions": "- Lube oil outlet temperature: Answer \"Lube oil outlet temperature\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Lube oil differential temperature: Answer \"Lube oil differential temperature\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Cooling water differential temperature: Answer \"Cooling water differential temperature\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Cooling water outlet temperature: Answer \"Cooling water outlet temperature\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qfdc1fcf479",
  "kind": "choice",
  "text": "I don't know what criteria does <e>MTV</e> use to give music awards these days.",
  "question": "What type of named entity is \"MTV\" (marked <e>) in this post?",
  "options": [
   "location",
   "person",
   "product",
   "creative work",
   "group",
   "corporation"
  ],
  "definitions": "- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant."
 },
 {
  "qid": "q9a9268fe9c",
  "kind": "choice",
  "text": "Infobox:\nTitle: Shimon Sofer\nBorn: (1820-12-18)December 18, 1820 , (13 Tevet 5581 Anno Mundi) , Pressburg, Austrian empire, now Bratislava, Slovakia\nDied: March 26, 1883(1883-03-26) (aged 62) , (17 Adar II 5643 Anno Mundi) , Krakow, Austro-Hungary, now Poland\nResting place: Krakow\nResidence: Krakow\nNationality: Jew\nOther names: Rabbi Simon Schreiber, the Michtav Sofer\nOccupation: Chief Rabbi\nSpouse(s): Miriam Sternberg\nChildren: Akiva, Yisrael David Simcha (Bunim), Yoel, Shlomo Aleksandri, Asher, Raizel (Kornitzer), Shulamit (Roth)\nParent(s): Moshe and Sarel Sofer (Schreiber)\nRelatives: Avraham Shmuel Binyamin Sofer (Brother)\n\nHypothesis: Shimon Sofer died in March 28, 1883",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q39e7f6ef45",
  "kind": "yes/no",
  "text": "At physiological concentrations of <e1>gabapentin</e1>, <e2>LAT1</e2> mediated transport was 3 or ~10-fold higher than the other transport processes in the two systems, respectively, demonstrating clear selectivity for gabapentin.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"gabapentin\" (marked <e1>) and the gene or protein \"LAT1\" (marked <e2>)?\nIs the correct answer \"Option E\"?",
  "definitions": "- Option E: The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter.\n- Option C: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- Option W: The chemical is a structural part of the gene product, e.g. an amino-acid residue (Ser-15, cysteine residues), a sugar chain or another chemical group within the protein.\n- Option P: The chemical raises the activity or function of the gene product, by binding it or with no mechanism stated ('X activates Y', 'X enhanced Y activity'); higher amounts or expression of Y are indirect upregulation instead.\n- Option V: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical.\n- Option T: The chemical is an antagonist or blocker of the gene product (usually a receptor): it binds and prevents or reduces the receptor's response to an agonist."
 },
 {
  "qid": "qfa44203c9b",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Air Lithuania\nSection: History\nSentence: Air Lithuania was established as a state-owned company on 13 September 1991 after the reorganization of Aeroflot division in Kaunas.\nSentence: It started charter flights on 15 February 1992.\n\nClaim: Among the many defunct airlines of Lithuania, Air Lithuania commenced operations in 1996 and ceased them in 2005, while Amber Air commenced operations in 2004 and ended them in 2007.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "q5769552e9c",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Reactivity Coefficients.\n\nQuestion: A reactor is operating continuously at steady-state 100 percent power. As core burnup increases, the fuel temperature coefficient becomes __________ negative because the average fuel temperature __________.",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs the correct answer \"more; increases\"?",
  "definitions": "- more; increases: Answer \"more; increases\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- more; decreases: Answer \"more; decreases\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- less; decreases: Answer \"less; decreases\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- less; increases: Answer \"less; increases\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong."
 }
]
