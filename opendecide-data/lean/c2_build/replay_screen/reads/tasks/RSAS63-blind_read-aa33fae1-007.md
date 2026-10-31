# A46 replay label-noise blind read RSAS63-blind_read-aa33fae1-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS63-blind_read-aa33fae1-007.json

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
  "qid": "q9e069c256f",
  "kind": "yes/no",
  "text": "ASYMPTOMATIC GONORRHEA occurs in 5 to 10% of pregnancies, so N GONORRHOEAE may be a pathogen.",
  "question": "Does this sentence express that one of the terms \"ASYMPTOMATIC GONORRHEA\" and \"N GONORRHOEAE\" is used to prevent the other (preventive use of a drug or ingredient)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked PREVENTS: the sentence presents one term as a drug or ingredient used to prevent the other or lower its risk (e.g. vitamin C reduces the risk of influenza).\n- no: At most 10% ticked PREVENTS: the terms are linked in another way in this sentence (treatment of an existing condition, cause, symptom, diagnosis, association) or not at all."
 },
 {
  "qid": "qc29c02d8d4",
  "kind": "yes/no",
  "text": "Situation: Tom and Mary had a divorce soon after.\nAction being judged: Not respecting vows you have made.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q935e0772cb",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Roman Catholic Archdiocese of Belo Horizonte\nTable:\n| Archdiocese of Belo Horizonte Archidioecesis Bellohorizontinus Arquidiocese de Belo Horizonte | Archdiocese of Belo Horizonte Archidioecesis Bellohorizontinus Arquidiocese de Belo Horizonte |\n| Location | Location |\n| ... |\n| Statistics | Statistics |\n| Area | 7,240 km (2,800 sq mi) |\nSentence: The Roman Catholic Archdiocese of Belo Horizonte (Latin: Archidioecesis Bellohorizontinus) is an archdiocese located in the city of Belo Horizonte in Brazil.\n\nClaim: Roman Catholic Archdiocese of Belo Horizonte (Latin: Archidioecesis Bellohorizontinus) is located in the city of Belo Horizonte in Brazil and covers an area of 7,240km.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q63604c8089",
  "kind": "yes/no",
  "text": "Partner's previous message: Hello, what is your preference for supplies?  I would prefer to have as much extra firewood as possible, but am relatively indifferent to the rest.\nMessage: yes we have to supply more how much you want",
  "question": "Which negotiation strategy does the Message use?\nIs the correct answer \"non-strategic\"?",
  "definitions": "- non-strategic: The utterance uses none of the listed strategies, for example plainly stating an offer, accepting, or handling logistics.\n- showing empathy: The speaker acknowledges the partner's personal situation positively or sympathetically, showing understanding or concern for their needs or circumstances.\n- own need: The speaker argues that they personally need an item, giving a reason from their own situation, such as health or conditions.\n- small talk: Rapport-building talk not about the deal itself, such as greetings, pleasantries, or chatting about the camping trip, weather or activities.\n- fairness appeal: The speaker appeals to fairness for their own benefit, calling a deal fair or objecting that an offer is unfair to them."
 },
 {
  "qid": "q26c59dc52e",
  "kind": "yes/no",
  "text": "Action: Continuing with what you were doing when you've resolved unexpected situations.",
  "question": "Is this action against the law in most places?",
  "definitions": "- yes: Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, drunk driving, vandalism, hard-drug use), not merely rude or immoral.\n- no: The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for example lying to a friend, cheating on a partner, breaking a promise)."
 },
 {
  "qid": "q778be335be",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): Steve borrowed your spare phone charger two months ago. Then he took your toaster a month ago. He did not return any of them. And now, Steve says, \"can I borrow your suitcase? I need one for my trip next week.\"\nYour reply to Steve: That's no problem - you can pick that up when you bring back my phone charger and toaster.",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "qac671e0ada",
  "kind": "choice",
  "text": "Premise:\nTitle: Cornelis Drebbel\nBorn: 1572 Alkmaar, Netherlands\nDied: 7 November 1633 (1633-11-07) (aged 60 - 61) London, England\nEducation: Hendrick Goltzius\nOccupation: Engineer, inventor\nSpouse(s): Sophia Jansdochter Goltzius ( m. 1595)\nChildren: 6\nHypothesis: Cornelis Drebbel was European.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q31f7728df8",
  "kind": "yes/no",
  "text": "Employees were removing bulk head sections from the fine side of #6 mill. Employee's hand was caught in between the bulk head section and the side of the mill causing a laceration to his left hand and finger.",
  "question": "What is the nature of the injury described in this mine accident report?\nIs the correct answer \"cut, laceration or puncture (open wound)\"?",
  "definitions": "- cut, laceration or puncture (open wound): An open wound: a cut, laceration, gash or puncture, including wounds closed with stitches or staples.\n- scratch or abrasion (superficial): A superficial scratch, scrape or abrasion of the skin or eye.\n- fracture or chipped bone: A broken, fractured or chipped bone.\n- amputation or enucleation: Loss of all or part of a body part (finger, toe, limb) by cutting off, tearing off or surgical removal after the injury, or removal of an eye.\n- systemic poisoning: Poisoning of the body as a whole by a toxic substance (for example carbon monoxide or lead), not a local chemical burn."
 },
 {
  "qid": "qbb1bc55a85",
  "kind": "yes/no",
  "text": "Situation: I was abused by my mum’s boyfriend as a child. My neighbours and family knew but didn’t do anything.\nAction being judged: Letting child abuse happen when you see it happening.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qb1226953c1",
  "kind": "yes/no",
  "text": "@jenniferatntd HASHTAG_EASTASIA lie again and HASHTAG_EASTASIA just make the world think that the current case is from europe or us, but not second wave outbreak inside china. they just trying to blame other courtiers and pretend as a victim. but HASHTAG_EASTASIA+VIRUS is from HASHTAG_EASTASIA and spread globally",
  "question": "Is this tweet hostile toward an East Asian entity (people, country, government, institution or culture)?",
  "definitions": "- yes: Hostile: the words themselves derogate or demean an East Asian people, country, government or culture (extreme negative portrayal, hatred, conspiracy claims, wishing them gone or suffering, boycotts, slurs, mocking virus names); placeholder hashtags alone never count.\n- no: Not hostile: reasoned criticism of an East Asian government or institution without abuse, discussion of anti-Asian prejudice, counter-speech defending East Asian people, or neutral or unrelated content; naming the virus after its origin is not hostile."
 },
 {
  "qid": "q8029e22fb0",
  "kind": "yes/no",
  "text": "Science facts table (first row is the header):\n|  | HEMISPHERE |  | ORBITAL EVENT |  | MONTH OF OCCURENCE |\n| In the | northern hemisphere | , the | summer solstice | occurs in | June |\n| In the | southern hemisphere | , the | summer solstice | occurs in | December |\n| In the | northern hemisphere | , the | winter solstice | occurs in | December |\n| In the | southern hemisphere | , the | winter solstice | occurs in | June |\n| In the | northern hemisphere | , the | spring equinox | occurs in | March |\n| In the | southern hemisphere | , the | spring equinox | occurs in | September |\n| In the | northern hemisphere | , the | fall equinox | occurs in | September |\n| In the | southern hemisphere | , the | fall equinox | occurs in | March |\n\nQuestion: Which orbital even occurs in the southern hemisphere during March?\nProposed answer: fall equinox",
  "question": "According to the table of facts, is the proposed answer to the question correct?",
  "definitions": "- yes: The table's row for the fact the question asks about gives exactly the proposed answer (same entity, value or property), so it answers the question correctly.\n- no: The table shows the proposed answer belongs to a different row or fact than the one the question asks about, so it does not answer the question."
 },
 {
  "qid": "q868e2dae7e",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master Uninspected Fishing Vessels), Deck General.\n\nQuestion: The official identification of a vessel is found in which document?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Load Line Certificate",
   "Classification Certificate",
   "Certificate of Documentation",
   "Certificate of Inspection"
  ],
  "definitions": "- Load Line Certificate: Answer \"Load Line Certificate\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Classification Certificate: Answer \"Classification Certificate\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Certificate of Documentation: Answer \"Certificate of Documentation\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Certificate of Inspection: Answer \"Certificate of Inspection\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q172f007af5",
  "kind": "choice",
  "text": "Premise:\nTitle: Indira Gandhi\nIn office: January 14, 1980 - October 31, 1984 (1), January 24, 1966 – March 24, 1977 (2)\nPresident: N.Sanjiva Reddy (1980-1984) (1), Zail Sing (1), Sarvepalli Radhakrishnan (1980-1984) (2), Zakir Husain (1966-1977) (2), V. V. Giri (1966-1977) (2), Fakhruddin Ali Ahmed (1966-1977) (2)\nPreceded by: Charan Singh (1980-1984) (1), Gulzarilal Nanda (Acting) (1966-1977) (2)\nSucceeded by: Morarji Desai (1980-1984) (1), Rajiv Gandhi (1966-1977) (2)\nDeputy: Morarji Desai (1966-1977) (2)\nHypothesis: Indira Gandhi approved of his successor.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "qcfbb297d23",
  "kind": "choice",
  "text": "RT @_youhadonejob: <e>Richard</e> may need some help. http://t.co/uaJqDv1ZVY",
  "question": "What type of named entity is \"Richard\" (marked <e>) in this post?",
  "options": [
   "creative work",
   "product",
   "person",
   "corporation",
   "location",
   "group"
  ],
  "definitions": "- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- group: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA')."
 },
 {
  "qid": "qe5d67f317f",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 2011 WAFL Grand Final\nSection: Teams > Subiaco\nTable:\n| C: | Shaun Hildebrandt | Chris Phelan | Pat Hassett |\n\nClaim: The Subiaco team at the 2011 WAFL Grand Final included Robert Forrest, Rhett Kerr, but Shaun Hildebrandt did not participate.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "q48b4567185",
  "kind": "yes/no",
  "text": "William asked Joseph to help him get rid of the gray in his hair, but _ didn't know how to do it.\n\nThe blank (_) stands for one of two candidates: \"William\" or \"Joseph\".",
  "question": "Does the blank (_) in the sentence stand for \"William\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qa2acef9dcc",
  "kind": "yes/no",
  "text": "Product: arin serving dining kitchen cart\nDescription: this is a high-quality serving cart that is an ideal choice for your kitchen or dining room. made of premium fir and iron materials, this kitchen trolley is sturdy and durable enough for long time use. featuring three shelves, it provides ample storage space for you to organize your items. the tray top is removable so that you can use it according to your needs. two convenient handles make it more comfortable for push or you can use it as towel racks. equipped with 4 rolling casters for easy movement, and 2 of them are lockable to ensure stability while using the serving cart. brand new and high quality 3",
  "question": "Which product category should this retail listing be filed under?\nIs the correct answer \"Option J\"?",
  "definitions": "- Option J: Freestanding kitchen islands and carts providing extra counter space and storage.\n- Option G: Home bar furniture: bar cabinets, bar carts, home bars and bar sets with stools.\n- Option V: Daybeds, futons and other beds that double as seating or fold away for guests, including trundle daybeds.\n- Option F: A dining or kitchen table sold on its own, without chairs.\n- Option E: Long low dining-room cabinets with doors and drawers for serving and storing dishware."
 },
 {
  "qid": "q2260884ea8",
  "kind": "choice",
  "text": "Trivia question (category: Geography).\n\nQuestion: What is Canada's largest island?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Option R",
   "Option K",
   "Option T",
   "Option Z"
  ],
  "definitions": "- Option R: Answer \"Vancouver Island\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option K: Answer \"Baffin Island\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option T: Answer \"Prince Edward Island\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option Z: Answer \"Newfoundland\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q1ba0a92e39",
  "kind": "yes/no",
  "text": "I dont if the lads at WallStreetBets would agree,she was supposed be the one but ended up disappointing like all the rest",
  "question": "This post is sexist. Which specific type of sexism does it show?\nIs it wrong to answer \"backhanded gendered compliments\"?",
  "definitions": "- backhanded gendered compliments: The post seems to praise women but actually belittles them, for example implying they are weak, need protection or matter only for their looks.\n- immutable gender differences and stereotypes: The post asserts natural, essential or unchangeable differences between men and women or uses gender stereotypes, including using women's traits to mock men; most sexist jokes fall here.\n- incitement and encouragement of harm: The post urges or encourages others to harm a woman or women, or argues that harming women is justified; it calls for or endorses harm rather than only insulting women.\n- supporting mistreatment of individual women: The post supports mistreatment of a particular woman or women by denying, understating or justifying it, for example blaming a victim of abuse or harassment.\n- casual use of gendered slurs, profanities and insults: The post uses a slur or insult that traditionally describes women, such as bitch or slut, casually and not to deliberately attack women, often even aimed at a man."
 },
 {
  "qid": "qfafa5d1f51",
  "kind": "yes/no",
  "text": "Mary Doria Russell\nMary Doria Russell (born August 19, 1950) is an American novelist.\n\nAlexander Blok\nAlexander Alexandrovich Blok (Russian: Алекса́ндр Алекса́ндрович Бло́к ; ] ; 28 November [O.S. 16 November] 1880 7 August 1921) was a Russian lyrical poet.",
  "question": "Are Mary Doria Russell and Alexander Blok both novelists?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "qb89903e39a",
  "kind": "yes/no",
  "text": "Question: Rhinosporidiosis is caused by which of the following?\nOptions: (A) Fungus (B) Virus (C) Bacteria (D) Protozoa",
  "question": "Which medical subject does this exam question belong to?\nIs the correct answer \"ENT (otorhinolaryngology)\"?",
  "definitions": "- ENT (otorhinolaryngology): Diseases and surgery of the ear, nose, paranasal sinuses, pharynx and larynx, hearing and vestibular tests, and head-neck conditions treated by ENT surgeons.\n- obstetrics and gynaecology: Pregnancy, labour, puerperium and their complications, contraception, and diseases of the female reproductive organs, including gynaecological cancers.\n- radiology: Imaging and radiation: X-ray, CT, MRI, ultrasound and nuclear-medicine signs and choice of investigation, radiation physics, radiotherapy and radiation protection.\n- social and preventive medicine: Community medicine: epidemiology, biostatistics, national health programmes, screening, nutrition and environmental and occupational health at population level.\n- anaesthesia: Anaesthetic agents and techniques, airway management, muscle relaxants, perioperative monitoring, regional blocks and pain or ICU management as practised by anaesthetists."
 },
 {
  "qid": "q3c84f04dd0",
  "kind": "yes/no",
  "text": "Statement 1: he worked out the problem and went to ask his classmates\nStatement 2: he couldn't do the problem and went to consult his classmates",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q3efa2a7c0f",
  "kind": "yes/no",
  "text": "Beginning: The man was reading a book in the park. He ...\n\nPossible endings:\n(A) paused his movie.\n(B) was sitting on the ground.\n(C) parked his car on the book.\n(D) fought his librarian for her mercedes.",
  "question": "Among the listed endings, is (B) \"was sitting on the ground.\" the most sensible continuation of the beginning?",
  "definitions": "- yes: The named ending is the listed continuation that makes the most sense: read after the beginning, it describes what would ordinarily be true or happen next, fits who and what the beginning is about, and respects any negation, number, idiom or double meaning in it.\n- no: Another listed ending makes more sense: the named ending contradicts the beginning, is about the wrong person or thing, misreads a word, idiom or quantity, or describes something absurd or unrelated."
 },
 {
  "qid": "q073dd5f06f",
  "kind": "yes/no",
  "text": "Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\nAs a general rule, part “performance or a change in position in reliance on an oral contract to convey land will estop a defendant from raising the Statute of Frau 1947) (noting mere nonperformance of an oral contract within the statute of frauds does not constitute fraud) (citations omitted). Moreover, a fundamental exception to the general notice pleading requirement in Massachusetts is that allegations of fraud shall be stated “with particularity.” Mass.R.Civ.P. 9(b). Normally, this means that the pleading must state the time, place and content of the fraud and what was obtained or given up as a consequence of the fraud. See Wayne Investment, Inc. v. Gulf Oil Corp., 739 F.2d 11, 13 (1st Cir. 1984) (<HOLDING>); Friedman v. Jablonski, 371 Mass. 482 (1976).\n\nCandidate holding for <HOLDING>: holding plaintiffs speculations did not satisfy rule 9b requirements",
  "question": "Does the candidate statement correctly give the holding of the case that this court opinion cites at the <HOLDING> marker?",
  "definitions": "- yes: The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the legal rule or outcome of that cited case and supports the exact proposition the passage uses it for.\n- no: The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or outcome does not match the proposition the passage cites that case for, even if it shares topic words."
 },
 {
  "qid": "qa1d14fe5ca",
  "kind": "yes/no",
  "text": "Situation: In exchange she was going to have a cook-out for them.\nAction being judged: Expecting something in return for a favor.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q5c7eff9d41",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNED A 1999 DODGE RAM 3500. WHILE DRIVING AT 35 MPH, THE VEHICLE STARTED PULLING TO THE LEFT. WHILE ATTEMPTING TO STOP THE VEHICLE, THE POWER STEERING AND BRAKES FAILED. AS A RESULT, THE VEHICLE LEFT THE ROADWAY AND CRASHED INTO A RETAINING WALL. THE AIR BAGS DEPLOYED, KNOCKING THE CONTACT UNCONSCIOUS. THE CONTACT SUSTAINED LACERATIONS TO THE NOSE AND FACE, A CONCUSSION, BRUISING OF THE LEFT SHOULDER, A HEAD INJURY AND A WRIST INJURY THAT REQUIRED MEDICAL ATTENTION. A POLICE REPORT WAS NOT FILED. THE VEHICLE WAS TOWED TO AN INDEPENDENT MECHANIC. THE VEHICLE WAS DESTROYED. THE FAILURE MILEAGE WAS 149,312.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q8fc5efa299",
  "kind": "choice",
  "text": "Tweet: I love you, local staff of pep boys. I've rarely experienced such courtesy and understanding.",
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
  "qid": "q046b92d2c2",
  "kind": "yes/no",
  "text": "A particular person didn't know that a particular thing happened.",
  "question": "If someone says this sentence, is it likely that they mean \"That person knew that that thing didn't happen.\"?",
  "definitions": "- yes: At least 7 of 10 annotators, and the average rating, judged it likely that a speaker of the negated sentence means the version with the negation moved into the embedded clause (a neg-raising reading, as 'I don't think it happened' usually means 'I think it didn't happen').\n- no: At most 3 of 10 annotators, and the average rating, judged it likely: the sentence only denies the attitude or report itself (as 'I didn't say it happened' does not mean 'I said it didn't happen')."
 },
 {
  "qid": "q2e00a7ea8d",
  "kind": "yes/no",
  "text": "Knobloch syndrome involving <e>midline scalp defect of the frontal region</e>.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"midline scalp defect of the frontal region\" (marked <e>) in this sentence?\nIs the correct answer \"specific disease\"?",
  "definitions": "- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "q32237b646d",
  "kind": "choice",
  "text": "27 January: The <e1>London</e1> conference result was supported by <e2>Great Britain</e2> and Russia and accepted by Prussia and the German parliament.",
  "question": "Which relation from entity 1 (\"London\", marked <e1>) to entity 2 (\"Great Britain\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "Code 29",
   "Code 16",
   "Code 51"
  ],
  "definitions": "- Code 29: Entity 1 is the capital city or seat of government of entity 2 (a country, state, province or region).\n- Code 16: Entity 2 is the sovereign country in which entity 1 (a place, building, organisation, event or object, not a person) is located or to which it belongs.\n- Code 51: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qc8c3edaa67",
  "kind": "yes/no",
  "text": "The vest suited the dog on the hot summer day unlike the shirt because the _ was closed in.\n\nThe blank (_) stands for one of two candidates: \"vest\" or \"shirt\".",
  "question": "Does the blank (_) in the sentence stand for \"shirt\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q39b1551ade",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 1938 NCAA Swimming and Diving Championships\nSection: Team results\nTable:\n| Rank | Team | Points |\n|  | Michigan | 46 |\n|  | Ohio State | 45 |\n|  | Harvard | 36 |\n| 4 | Princeton | 22 |\n| 5 | Yale | 18 |\n| 6 | Iowa | 7 |\n| 7 | Rutgers (H) | 5 |\n| 8 | Army Stanford Texas | 4 |\n\nClaim: 1938 NCAA Swimming and Diving Championships had seven teams, one of which was Michigan (head coach Mike Bottom) in first place.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "qdd3541f257",
  "kind": "yes/no",
  "text": "Table caption: A Diffusion model for Serious Games.\n| Diffusion of Serious Games | Fun | Feedback | Flow |\n| Relevance | Perceived enjoyment | Perceived usefulness | Experience and Habit |\n| Requirements | Information Quality | Information quality | Ease of Use |\n| Reliability | Social influence and Trust | System Quality | Trust and perceived risks |\n\nStatement: The relevance in Fun and Feedback is Perceived enjoyment.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb656d0f24d",
  "kind": "yes/no",
  "text": "Fluoxetine treatment of patients with MAJOR DEPRESSIVE DISORDER who failed initial treatment with SERTRALINE",
  "question": "Does this sentence express that one of the terms \"MAJOR DEPRESSIVE DISORDER\" and \"SERTRALINE\" is used to treat the other (therapeutic use of a drug, ingredient or therapy)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked TREATS: the sentence presents one term as a drug, ingredient or therapy used to cure or relieve the other (e.g. penicillin cures infection), including reported results such as 'was effective in treating'.\n- no: At most 10% ticked TREATS: in this sentence the terms are linked in another way (cause, symptom, side effect, location, diagnosis, prevention, is-a, mere co-occurrence) or not at all, whatever is true outside the sentence."
 },
 {
  "qid": "q4988521373",
  "kind": "yes/no",
  "text": "Statement 1: They took the patient in an ambulance\nStatement 2: They took the patient in a cooker",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qc5a6853ac4",
  "kind": "yes/no",
  "text": "Situation: I May Have Blinded my Neighbor's Baby\nAction being judged: Taking someone to the hospital if you think you've injured them.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q41cd6dc218",
  "kind": "yes/no",
  "text": "Colombia plane crash air traffic controller says she did everything she could to keep the flight's occupants alive",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qf1ae64a371",
  "kind": "choice",
  "text": "Sentence from a New York Times opinion article: It also has a float in the parade, offering out balloons and candy.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "Class N",
   "Class D",
   "Class L",
   "Class R",
   "Class U"
  ],
  "definitions": "- Class N: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Class D: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Class L: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Class R: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Class U: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "qf8bbdcfe4c",
  "kind": "yes/no",
  "text": "Wikipedia page: Chris Cariaso\nSection: Mixed martial arts record\nTable:\n| Res. | Record | Opponent | Method | Event | Date | Round | Time | Location | Notes |\n| ... |\n| Win | 15–5 | Iliarde Santos | TKO (punches) | UFC Fight Night: Maia vs. Shields | October 9, 2013 | 2 | 4:31 | Barueri, Brazil |  |\n| ... |\n| Win | 13–3 | Takeya Mizugaki | Decision (unanimous) | UFC 144 | February 26, 2012 | 3 | 5:00 | Saitama, Japan |  |\n| ... |\n| Win | 3–0 | Andrew Valladerez | Decision (unanimous) | Strikeforce: Young Guns | February 10, 2007 | 3 | 3:00 | San Jose, California, United States |  |\n| ... |\n| Win | 1–0 | Ralph Alvarado | Decision (unanimous) | ICFO 1: Stockton | May 13, 2006 | 3 | 5:00 | Stockton, California, United States |  |\n\nClaim: Cariaso faced Takeya Mizugaki on February 26, 2012 at UFC 144.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qbd70e8e6e6",
  "kind": "yes/no",
  "text": "Wikipedia page: WGNT\nSection: Digital channels\nTable:\n| Channel | PSIP Short Name | Video | Aspect | Programming |\n| 27.1 | WGNT-DT | 1080i | 16:9 | Main WGNT programming / The CW |\n| 27.2 | ANT-TV | 480i | 4:3 | Antenna TV |\n| 27.3 | TBD | 480i | 16:9 | TBD |\n\nClaim: The Antenna TV is carried on WGNT digital channel 27.2.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q3d208f8b8d",
  "kind": "yes/no",
  "text": "Graffiti on crosswalk sign at corner of India Street and Washington Street",
  "question": "Which crew or agency should this graffiti report be routed to for removal?\nIs the correct answer \"San Diego Unified School District\"?",
  "definitions": "- San Diego Unified School District: Graffiti on a public school's buildings, fences or grounds, referred to the San Diego Unified School District.\n- City graffiti crew: Graffiti on City right-of-way or City street furniture (sidewalks, curbs, street signs, light poles, alleys, bridges, public walls), removed by the City's own crew.\n- Metropolitan Transit System: Graffiti on transit property (trolley stations and tracks, bus stops, benches and shelters), referred to the Metropolitan Transit System.\n- utility company that owns the box or pole: Graffiti on a utility box, cabinet, transformer or pole owned by a utility (SDG&E, AT&T or Cox); the report is referred to that company.\n- Park and Recreation Department: Graffiti inside a City park, playground, recreation center, trail or open-space canyon, handled by the Parks and Recreation Department.\n- Caltrans: Graffiti on state highway property (freeways, on- and off-ramps, freeway signs, sound walls, overpasses on state routes), referred to Caltrans."
 },
 {
  "qid": "q2f04623eb0",
  "kind": "yes/no",
  "text": "RT @DollarVanDemos: #BROOKLYN! Stay up late tonight to catch the 1 hr special of <e>Demos</e> @ 3AM on BCAT feat @BlissyCakes @YaGirlNicolette ...",
  "question": "What type of named entity is \"Demos\" (marked <e>) in this post?\nIs it wrong to answer \"creative work\"?",
  "definitions": "- creative work: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- person: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team.\n- corporation: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- location: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- product: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation."
 },
 {
  "qid": "qce77841da2",
  "kind": "yes/no",
  "text": "Y'all release your tranny fluid in bathrooms? I usually do it on the road or in a driveway.",
  "question": "How is the potential slur in this comment used?\nIs it wrong to answer \"Code 56\"?",
  "definitions": "- Code 56: The slur conveys contempt toward a targeted person or group: insults, labels, stand-alone slurs, sexualised use, generalisations about the community, or self-deprecation.\n- Code 23: A member of the targeted group uses the slur with positive or neutral force about themselves or their community (empowerment, in-group solidarity, humour).\n- Code 34: The word is used in a non-slur sense, such as 'fag' meaning a cigarette or 'tranny' meaning a vehicle transmission.\n- Code 13: The slur is mentioned rather than aimed at anyone - quoted, discussed as a word, recalled from an incident, used in counter-speech, or in sarcasm that mocks bigotry - by a speaker who is not reclaiming it."
 },
 {
  "qid": "qfaedc848ad",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Thomas Løvendahl Sørensen\n- On 24 July 2017, Sørensen announced his retirement from professional football at the age of 41.\n- For the 2002 FIFA World Cup qualifying campaign in 2001, he took over the job as goalkeeper and helped Denmark qualify.\n\nSummary sentence:\nThomas Løvendahl Sørensen is a retired Danish footballer who played as a goalkeeper.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q3396b825ab",
  "kind": "yes/no",
  "text": "<e1>Thionamides</e1> inhibit the transcription factor nuclear factor-kappaB by suppression of <e2>Rac1</e2> and inhibitor of kappaB kinase alpha.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"Thionamides\" (marked <e1>) and the gene or protein \"Rac1\" (marked <e2>)?\nIs it wrong to answer \"Option X\"?",
  "definitions": "- Option X: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead.\n- Option B: The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment.\n- Option J: The chemical is a structural part of the gene product, e.g. an amino-acid residue (Ser-15, cysteine residues), a sugar chain or another chemical group within the protein.\n- Option H: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased.\n- Option Y: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical."
 },
 {
  "qid": "q7f3740484a",
  "kind": "yes/no",
  "text": "Day 1, done.\n\nA look at all the numbers from the first day of drills at the NFL combine",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q881f7aa5d3",
  "kind": "yes/no",
  "text": "User (latest message): Can Oceano in Reno do waiter service?",
  "question": "How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?\nIs it wrong to answer \"answer a question about a place\"?",
  "definitions": "- answer a question about a place: The user asks for supported facts about a named business or place: its address, phone number, website, price level, rating, hours or whether it has a feature (full bar, parking, takeout).\n- reply with a pleasantry: The user only greets, thanks or reacts ('hi', 'thanks', 'ok', 'great job'), makes small talk, or asks for help in general without a concrete calendar request; the assistant just replies politely and offers help.\n- decline: specific conference rooms: The user asks to book or include a specific conference or meeting room ('in Conference Room A'); the assistant cannot book rooms.\n- ask the user to be more specific: The user wants something done but leaves out what exactly: which event, or the new time or value ('change dinner time', 'update my Monday meeting'), or sends a fragment that cannot be acted on alone ('select one', 'place it').\n- delete an event: The user asks to cancel, remove or delete one specific event already on the calendar."
 },
 {
  "qid": "q20c7a37954",
  "kind": "yes/no",
  "text": "In the 1992 United States presidential election, Bush and Quayle were challenged in their bid for reelection by the Democratic ticket of Arkansas Governor Bill Clinton and <e>Tennessee</e> Senator Al Gore and the independent ticket of Texas businessman Ross Perot and retired Vice Admiral James Stockdale.",
  "question": "In this politics text, what type of entity is \"Tennessee\" (marked <e>)?\nIs it wrong to answer \"organisation\"?",
  "definitions": "- organisation: A named organisation, company, agency or institution that is not one of the more specific organisation types listed (political party).\n- location: A named place that is not a country: city, region, state, building, venue, river or other geographic feature.\n- country: A named sovereign country or nation state (e.g. 'France', 'United States'), including historical countries.\n- political party: A named political party or party alliance (e.g. 'United Russia', 'Labour Party').\n- election: A named election or referendum (e.g. '1934 Australian federal election').\n- event: A named event such as a war, festival, conference, ceremony, competition or historical episode; elections have their own type."
 },
 {
  "qid": "q517e6a91d4",
  "kind": "choice",
  "text": "Trivia question (category: Science: Computers).\n\nQuestion: Generally, which component of a computer draws the most power?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Video Card",
   "Power Supply",
   "Processor",
   "Hard Drive"
  ],
  "definitions": "- Video Card: Answer \"Video Card\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Power Supply: Answer \"Power Supply\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Processor: Answer \"Processor\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Hard Drive: Answer \"Hard Drive\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q79f885f7c7",
  "kind": "yes/no",
  "text": "@enzomazak if who really want to de-name HASHTAG_EASTASIA+VIRUS ,plz treat it all the same.  spanish flu african swine fever virus middle east respiratory syndrome (mers)  who stope fuck the world https://t.co/yvmckenfxj",
  "question": "Is this tweet hostile toward an East Asian entity (people, country, government, institution or culture)?",
  "definitions": "- yes: Hostile: the words themselves derogate or demean an East Asian people, country, government or culture (extreme negative portrayal, hatred, conspiracy claims, wishing them gone or suffering, boycotts, slurs, mocking virus names); placeholder hashtags alone never count.\n- no: Not hostile: reasoned criticism of an East Asian government or institution without abuse, discussion of anti-Asian prejudice, counter-speech defending East Asian people, or neutral or unrelated content; naming the virus after its origin is not hostile."
 }
]
