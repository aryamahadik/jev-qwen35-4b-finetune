# A46 replay label-noise blind read RSBS25-blind_read-30e3dd33-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSBS25-blind_read-30e3dd33-006.json

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
  "qid": "qa9c3b3158c",
  "kind": "choice",
  "text": "Premise:\nTitle: Studio DEEN\nNative name: 株式会社スタジオディーン\nRomanized name: Kabushiki gaisha Sutaijo Dīn\nType: Kabushiki gaisha\nIndustry: Anime\nFounded: March 14, 1975; 44 years ago (1975-03-14)\nFounder: Hiroshi Hasegawa\nHeadquarters: Japan\nSubsidiaries: Danny Donghua , Megumi , Umidori\nWebsite: www .deen .co .jp\nHypothesis: Studio DEEN puts out 10 new shows a year.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q38d0792fd7",
  "kind": "yes/no",
  "text": "Question: A man eats a low-carbohydrate meal that is rich in proteins containing the amino acids that stimulate insulin secretion. Which response accounts for the absence of hypoglycemia?\nOptions: (A) Suppression of GH (B) Suppression of somatomedin C secretion (C) Stimulation of coisol secretion (D) Stimulation of glucagon secretion",
  "question": "Which medical subject does this exam question belong to?\nIs it wrong to answer \"microbiology\"?",
  "definitions": "- microbiology: Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, immunology and vaccines, and sterilisation.\n- physiology: Normal function of the body's systems (nerve, muscle, blood, heart, lungs, kidney, endocrine, special senses) and their regulation, not their structure or disease.\n- pharmacology: Drugs: mechanisms of action, pharmacokinetics, adverse effects, interactions, drug of choice and classification of drugs.\n- ophthalmology: Eye diseases, their signs, investigations and treatment, optics and refraction, and eye surgery.\n- social and preventive medicine: Community medicine: epidemiology, biostatistics, national health programmes, screening, nutrition and environmental and occupational health at population level.\n- forensic medicine and toxicology: Medico-legal practice: injuries and wounds, death and post-mortem changes, identification, sexual offences, legal procedures, and poisons with their antidotes (toxicology)."
 },
 {
  "qid": "qcd3d4a8463",
  "kind": "choice",
  "text": "Premise:\nTitle: Medellín\nRegion: Aburrá Valley\nMunicipality: Area: 380.64 km2 (146.97 sq mi), Populations (2019): 2,549,537\nNickname9s): City of the Eternal Spring, Capital of the Mountain, City of the Flowers\nCoordinates: 6°13′51″N 75°35′26″W﻿ / ﻿6.23083°N 75.59056°W\nFounded: March 2, 1616\nType: Mayor-council\nBody: Alcaldía de Medellín\nMayor: Federico Gutiérrez, 2016-2019\nMetro: Area: 1,152 km2 (445 sq mi), Populations (2019): 3,731,447\nElevation: 1,495 m (4,905 ft)\nDensity: 6,413/km 2 (16,610/sq mi)\nMetro density (2019): 6,925/km 2 (17,940/sq mi)\nDemonym(s): Medellinense , Paisa\nTime zone: UTC−05:00\nArea code(s): +57 4\nClimate: Af\nWebsite: Official website\nHypothesis: Federico Gutiérrez is no longer the mayor of Medellín.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q0073f8f5c4",
  "kind": "yes/no",
  "text": "Situation: I accuse girls of being racists when they reject me just to make them have a bad time out of vengance of the humillation I had\nAction being judged: Seeking vengeance against someone who hasn't done anything wrong.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q08b84e8c6a",
  "kind": "choice",
  "text": "Nebulin seen in <e>DMD</e> males including one patient with a large DNA deletion encompassing the DMD gene.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"DMD\" (marked <e>) in this sentence?",
  "options": [
   "modifier",
   "specific disease",
   "disease class",
   "composite mention"
  ],
  "definitions": "- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers')."
 },
 {
  "qid": "qe930f650d8",
  "kind": "yes/no",
  "text": "FAQ entry (restaurant: Loch Fyne)\nQ: Can I make a payment by credit card?\nA: Loch Fyne accepts all major credit cards.\n\nCustomer question: Do they accept Mastercard as a form of payment?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "qb42e859828",
  "kind": "yes/no",
  "text": "Gay guys drink alot🍻 because of their lifestyle",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q22f2548da5",
  "kind": "yes/no",
  "text": "Marge put the leftovers in the microwave and the turkey in the oven because the _ was better for reheating.\n\nThe blank (_) stands for one of two candidates: \"microwave\" or \"oven\".",
  "question": "Does the blank (_) in the sentence stand for \"oven\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qbb733da036",
  "kind": "yes/no",
  "text": "Customer: i need to try and get my car in to Intelligent Auto Solutions asap\nAssistant: ok what seems to be the problem\nCustomer: well my car is making a loud clunk when i turn",
  "question": "In the customer's last message, does \"my car is making a loud clunk when i turn\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7d62f8103e",
  "kind": "choice",
  "text": "Trivia question (category: General Knowledge).\n\nQuestion: The architect known as Le Corbusier was an important figure in what style of architecture?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Neoclassical",
   "Gothic Revival",
   "Modernism",
   "Baroque"
  ],
  "definitions": "- Neoclassical: Answer \"Neoclassical\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Gothic Revival: Answer \"Gothic Revival\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Modernism: Answer \"Modernism\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Baroque: Answer \"Baroque\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q90727902f9",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Gaurav Gill\nSentence: In 2013, Gaurav Gill became the first Indian driver to win the FIA Asia-Pacific Rally Championship and went on to win 3 times ( 2013, 2016, 2018) Gaurav Gill became the first-ever person from the field of Motor Sports to win the coveted Arjuna Award from the President of India in 2019.\n\nClaim: Gaurav Gill(born 2 December 1981) is an Indian race car driver and winner of Motor Sports award who competes in the Asia-Pacific Rally Championship, competed in 5 rallies and joined the teams, Team MRF, Team Sidvin India, and Jk Tyres.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "qd7df6f9713",
  "kind": "yes/no",
  "text": "Request:\nThree friends are driving to New York City and splitting the gas cost equally. At the last minute, 2 more friends joined the trip. The cost of gas was then evenly redistributed among all of the friends. The cost for each of the original 3 decreased by $\\$$11.00. What was the total cost of the gas, in dollars?\n\nResponse:\nLet's call the number of friends x. The cost for each of the original 3 friends would then be $\\frac{g}{3}$, where g is the total cost of gas.\nRight. And we know that the cost for each of the original 3 friends decreased by $\\$$11.00. So the new cost for each of the original 3 friends is $\\frac{g}{3}-11$ dollars.\nBut we know that 2 more friends joined the trip. So the new cost is also $\\frac{g}{5}$.\nThat's right. So $\\frac{g}{3}-11=\\frac{g}{5}$.\nNow we just need to solve for g.\nSo first we get rid of the fractions by multiplying both sides of the equation by 15.\nSo we get $5g-165=3g$.\nWhich simplifies to $2g=165$. And the total cost of gas is $g=\\frac{165}{2}=82.50$ dollars.\nSo the total cost of the gas is $82.50$ dollars.\n\n# Answer\n\n82.5",
  "question": "Would a careful reviewer accept this response as completely correct and compliant with all stated constraints?"
 },
 {
  "qid": "q164a9db979",
  "kind": "choice",
  "text": "Identification of the molecular defect underlying <e>FNDI</e> in affected families is a powerful tool for early asymptomatic diagnosis in infants..",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"FNDI\" (marked <e>) in this sentence?",
  "options": [
   "Code 32",
   "Code 40",
   "Code 51",
   "Code 38"
  ],
  "definitions": "- Code 32: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- Code 40: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- Code 51: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- Code 38: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "q77f5b708dd",
  "kind": "yes/no",
  "text": "@jewtastic @abc7 little known fact:  toilet paper is the #HASHTAG carrier of HASHTAG_EASTASIA+VIRUS  (let's see if that has any effect on the insane tp hoarding phenomenon)",
  "question": "Is this tweet hostile toward an East Asian entity (people, country, government, institution or culture)?",
  "definitions": "- yes: Hostile: the words themselves derogate or demean an East Asian people, country, government or culture (extreme negative portrayal, hatred, conspiracy claims, wishing them gone or suffering, boycotts, slurs, mocking virus names); placeholder hashtags alone never count.\n- no: Not hostile: reasoned criticism of an East Asian government or institution without abuse, discussion of anti-Asian prejudice, counter-speech defending East Asian people, or neutral or unrelated content; naming the virus after its origin is not hostile."
 },
 {
  "qid": "qcb217a392f",
  "kind": "yes/no",
  "text": "Customer: I'd like one with spinach, artichokes, and ricotta.\nAssistant: Hand tossed or deep dish?\nCustomer: Deep dish.",
  "question": "In the customer's last message, does \"Deep dish\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q465c42f3b9",
  "kind": "yes/no",
  "text": "Statement 1: The family takes a family vacation to space.\nStatement 2: The Family takes a family vacation to the beach.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q6c63c63ba2",
  "kind": "yes/no",
  "text": "Customer: Correct. I would like to fly on Delta.\nAssistant: Sure thing. What else?\nCustomer: Non-stop flight, please.",
  "question": "In the customer's last message, is \"Non-stop\" a mention of the number of stops or layovers for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q28a57f84d0",
  "kind": "yes/no",
  "text": "All 6 had dual atrioventricular (AV) nodal pathway physiology, 4 had AV nodal reentrant tachycardia (AVNRT) induced, 1 had both AVNRT and RECIPROCATING AV TACHYCARDIAS and 1 had nonsustained AVNRT and an atrial tachycardia induced.",
  "question": "Does this sentence express that one of the terms \"RECIPROCATING AV TACHYCARDIAS\" and \"AVNRT\" is used to treat the other (therapeutic use of a drug, ingredient or therapy)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked TREATS: the sentence presents one term as a drug, ingredient or therapy used to cure or relieve the other (e.g. penicillin cures infection), including reported results such as 'was effective in treating'.\n- no: At most 10% ticked TREATS: in this sentence the terms are linked in another way (cause, symptom, side effect, location, diagnosis, prevention, is-a, mere co-occurrence) or not at all, whatever is true outside the sentence."
 },
 {
  "qid": "qc7f01d55ec",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe clinical symptoms were significantly improved along with increase of oxyhemoglobin saturation within 3 d. Several parameters tended to improve as compared to pretransfusion, including increased lymphocyte counts (0.65 × 10(9)/L vs. 0.76 × 10(9)/L) and decreased C-reactive protein (55.98 mg/L vs. 18.13 mg/L). This study showed CP therapy was well tolerated and could potentially improve the clinical outcomes through neutralizing viremia in severe COVID-19 cases.\n\nClaim: Convalescent plasma given to severe COVID-19 patients worsened their symptoms.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qe842c99bfa",
  "kind": "yes/no",
  "text": "Samantha was sneezing more than Lindsey when they were at the vet's office because _ was allergic to cat hair.\n\nThe blank (_) stands for one of two candidates: \"Samantha\" or \"Lindsey\".",
  "question": "Does the blank (_) in the sentence stand for \"Samantha\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qaaf6581a2f",
  "kind": "yes/no",
  "text": "VIDEO: Did Matthew Dellavedova dive at Draymond Green’s knees? Draymond’s mom thinks so",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: All 3 annotators rated the tweet medium or strong clickbait: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: None of the 3 annotators rated it medium or strong clickbait: the tweet states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qeb9c684206",
  "kind": "choice",
  "text": "These results support the finding of a prostate cancer-susceptibility gene linked to 1q24-25, albeit in a defined subset of <e>prostate cancer</e> families.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"prostate cancer\" (marked <e>) in this sentence?",
  "options": [
   "Class X",
   "Class W",
   "Class K",
   "Class Y"
  ],
  "definitions": "- Class X: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- Class W: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- Class K: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- Class Y: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "q671cda6a6b",
  "kind": "yes/no",
  "text": "Graffiti on mailbox on university outside Smart and final",
  "question": "Which crew or agency should this graffiti report be routed to for removal?\nIs it wrong to answer \"San Diego Unified School District\"?",
  "definitions": "- San Diego Unified School District: Graffiti on a public school's buildings, fences or grounds, referred to the San Diego Unified School District.\n- US Postal Service: Graffiti on a blue mailbox, postal collection box or post office, referred to the US Postal Service.\n- Metropolitan Transit System: Graffiti on transit property (trolley stations and tracks, bus stops, benches and shelters), referred to the Metropolitan Transit System.\n- Caltrans: Graffiti on state highway property (freeways, on- and off-ramps, freeway signs, sound walls, overpasses on state routes), referred to Caltrans.\n- utility company that owns the box or pole: Graffiti on a utility box, cabinet, transformer or pole owned by a utility (SDG&E, AT&T or Cox); the report is referred to that company.\n- Port of San Diego: Graffiti on Port of San Diego tidelands (Harbor Drive waterfront, Embarcadero, Shelter Island, marinas, bayfront parks), referred to the Port."
 },
 {
  "qid": "q82742e4c81",
  "kind": "yes/no",
  "text": "Heading: Metapedia\nMetapedia\nOngoing whitewashing attempt by a single purpose account on this article about a white nationalist and far right website purporting to be an encyclopedia, more editors keeping an eye on this would be helpful.",
  "question": "Which Wikipedia noticeboard or help page is the right place for this post?\nIs the correct answer \"Code 23\"?",
  "definitions": "- Code 23: Editors who appear to edit about themselves, their employer, clients or products (paid or undisclosed promotional editing).\n- Code 25: Whether an article's wording, weight or balance is biased or gives undue weight to one viewpoint, when sourcing itself is not the issue.\n- Code 41: Questions about how to use or edit Wikipedia itself: creating articles, citing, formatting, uploading images, account and editing problems.\n- Code 53: Articles promoting or giving undue credence to fringe, pseudoscientific or conspiracy ideas that depart from mainstream scholarship.\n- Code 10: Technical problems and questions about the site's software: bugs, templates, gadgets, scripts, rendering, bots, tools and MediaWiki features.\n- Code 48: Urgent or chronic user-conduct problems that need an administrator to act: harassment, disruption, personal attacks, block evasion or misuse of tools."
 },
 {
  "qid": "qdb336d1b51",
  "kind": "yes/no",
  "text": "Wikipedia page: Farzad Majidi\nTable (first row is the header):\n| Season | Team | Country | Division | Apps | Goals | Assists |\n| 01/02 | Esteghlal | Iran | 1 | ? | 3 | ? |\n| 02/03 | Esteghlal | Iran | 1 | ? | 2 | ? |\n| 03/04 | Esteghlal | Iran | 1 | ? | 6 | ? |\n| 04/05 | Eseghlal | Iran | 1 | 27 | 3 | ? |\n| 05/06 | Esteghlal | Iran | 1 | 21 | 0 | 2 |\n| 06/07 | Esteghlal | Iran | 1 | 14 | 1 | 1 |\n| 07/08 | Steel Azin | Iran | 1 | ? | 2 | ? |\n| 10/11 | Gostaresh Foolad | Iran | 2 | 0 | 0 | 0 |\n\nQuestion: what team is in division 2?\nProposed answer: Gostaresh Foolad",
  "question": "Based only on the table, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer is exactly what the table gives for this question: the right cell, count or value, and when the question asks for several items, all of them and nothing else.\n- no: The proposed answer is not what the table gives: a different cell or value (for example a neighbouring row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item."
 },
 {
  "qid": "qe440506d7b",
  "kind": "yes/no",
  "text": "Passage:\nMany types of sports equipment are made of wood, or were constructed of wood in the past. For example, cricket bats are typically made of white willow. The baseball bats which are legal for use in Major League Baseball are frequently made of ash wood or hickory, and in recent years have been constructed from maple even though that wood is somewhat more fragile. NBA courts have been traditionally made out of parquetry.\n\nQuestion: Compared to hickory and ash, what adjective might be used for a maple baseball bat?\nReference answer: fragile\nCandidate answer: more fragile",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "qe68fd571bc",
  "kind": "choice",
  "text": "On September 16, 1939, the government of <e1>Édouard Daladier</e1> established Foreign Workers Companies (<e2>French</e2>: compagnie de travailleurs étrangers) which were not part of the French Foreign Legion.",
  "question": "Which relation from entity 1 (\"Édouard Daladier\", marked <e1>) to entity 2 (\"French\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "languages spoken, written or signed",
   "native language",
   "none of the listed relations"
  ],
  "definitions": "- languages spoken, written or signed: Entity 2 is a language that entity 1, a person, speaks, writes, sings or signs.\n- native language: Entity 2 is the first language that entity 1, a person, learned from birth.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q250c3d9236",
  "kind": "yes/no",
  "text": "can i blow my nose in that thing on their heads 💂",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post, reading any emoji as the words, groups or actions they stand for, directs abuse or contempt at a group identity (such as race, ethnicity, nationality, religion, gender, sexuality, disability, immigration status or class) or at someone because of that identity, explicitly or implicitly: insults and slurs, threats, dehumanising comparisons, or subtle digs and hostile stereotypes.\n- no: The post, reading any emoji for what they stand for, does not attack a group identity: it may mention identities, swear, criticise, counter hate or target something that is not an identity (an animal, an object, a person for non-identity reasons), but it is not abusive towards an identity group or anyone because of their identity."
 },
 {
  "qid": "q961607d68d",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Third Assistant Engineer), Engineering Safety & Environmental Protection.\n\nQuestion: In accordance with MARPOL (33 CFR Subchapter O), the definition of oil does NOT include which of the following?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Oil refuse",
   "Cooking oil",
   "Sludge",
   "Crude oil"
  ],
  "definitions": "- Oil refuse: Answer \"Oil refuse\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition).\n- Cooking oil: Answer \"Cooking oil\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition).\n- Sludge: Answer \"Sludge\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition).\n- Crude oil: Answer \"Crude oil\": correct only if it is the best answer to the question exactly as asked, respecting its NOT (for \"which ... is NOT ...\" wording, the one choice that fails the condition)."
 },
 {
  "qid": "q4b515f1dec",
  "kind": "yes/no",
  "text": "Customer: Yeah. How about a fantasy movie?\nAssistant: Jumanji or Star Wars: The Last Jedi?\nCustomer: I'll go with Jumanji.",
  "question": "In the customer's last message, is \"Jumanji\" a mention of the title of a specific movie for this movie search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q495c6b3c81",
  "kind": "yes/no",
  "text": "Both of our distinguished German colleagues left the meeting with their heads bowed low and their shoulders stooped. Their distress and concern for the future of Europe and the world was evident.",
  "question": "Does this paragraph make the contrarian climate claim that human greenhouse gases are not causing climate change?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that human greenhouse gases are not causing climate change: it denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation (sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are negligible.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that human greenhouse gases are not causing climate change."
 },
 {
  "qid": "q08783e72e0",
  "kind": "yes/no",
  "text": "Wikipedia page: Heather Dorff\nSection: Filmography\nTable:\n| Film | Year | Role | Notes |\n| Drifted | TBA | Tracy |  |\n| Happenstance | TBA | Heather |  |\n| The Tour | 2014 | Cassie |  |\n| Truth or Dare | 2013 | Michelle Lucas |  |\n| Intrusive Behavior | 2013 | Tabitha |  |\n| Dark Realm | 2013 | Sister Midnight |  |\n| City of Lust | 2013 | Ashley Barnes | also produced |\n| Hand of Glory | 2012 | Karen |  |\n| Spades | 2012 | Kathy |  |\n| Afraid of Sunrise | 2011 | Perrey |  |\n| \"What They Say\" | 2011 | Unnamed / Narrator | also produced |\n\nClaim: Dorff starred in the 2011 film \"What They Say'', which she also produced and in the 2013 film Truth or Dare.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qfc6205fb08",
  "kind": "choice",
  "text": "🐀 make me sick",
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
  "qid": "q151861bf91",
  "kind": "yes/no",
  "text": "Trivia question (category: Entertainment: Music).\n\nQuestion: Who had a 1976 hit with the song 'You Make Me Feel Like Dancing'?",
  "question": "Which answer choice correctly answers this trivia question?\nIs the correct answer \"Elton John\"?",
  "definitions": "- Elton John: Answer \"Elton John\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Leo Sayer: Answer \"Leo Sayer\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Andy Gibb: Answer \"Andy Gibb\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Billy Joel: Answer \"Billy Joel\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qf02c153ba9",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Tomorrow the Green Grass\nSection: Reception\nTable (caption: Professional ratings):\n| Review scores | Review scores |\n| Source | Rating |\n| ... |\n| NME | 7/10 |\n| Pitchfork | 7.1/10 |\n| ... |\n| Spin | 7/10 |\n\nClaim: Tomorrow the Green Grass received a rating of 7/10 from NME and Spin; while Pitchfork gave it a 7.1/10 rating.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qdf74654d80",
  "kind": "yes/no",
  "text": "The period since has been the quietest on record for US hurricanes, with no major (category 3-5) hurricanes.",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q88767a34d7",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nTo determine if SARS-CoV-2 is present in sewage during the emergence of COVID-19 in the Netherlands, sewage samples of 7 cities and the airport were tested using RT-PCR against three fragments of the nucleocapsid protein gene (N1-3) and one fragment of the envelope protein gene (E). The detection of the virus in sewage, even when the COVID-19 incidence is low, indicates that sewage surveillance could be a sensitive tool to monitor the circulation of the virus in the population.\n\nClaim: Researchers have detected genetic traces of the coronavirus in the wastewater in the Netherlands.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "qd6fe01bc41",
  "kind": "choice",
  "text": "Bonfire tonite. All are welcome, <e>joe</e> included",
  "question": "What type of named entity is \"joe\" (marked <e>) in this post?",
  "options": [
   "Code 22",
   "Code 58",
   "Code 35",
   "Code 40",
   "Code 12",
   "Code 15"
  ],
  "definitions": "- Code 22: The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product.\n- Code 58: A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building').\n- Code 35: A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation.\n- Code 40: A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant.\n- Code 12: A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA').\n- Code 15: A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team."
 },
 {
  "qid": "q3dd93a457e",
  "kind": "yes/no",
  "text": "Customer: Yes. I am looking for a place to stay that has 4 stars and includes free wifi.\nAssistant: We have at least 33 four star hotels with internet, would you like one close to the museum?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q67ab325845",
  "kind": "yes/no",
  "text": "Of course, saying that things are getting better overall does not mean that we live in a perfect world. Far from it. There is still an immense amount of poverty, as well as other challenges to overcome. But finding solutions to these problems demands generating more growth rather than exercising restraint.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q07d7fc73c2",
  "kind": "yes/no",
  "text": "Situation: Her mom took her there thinking they wouldn't find one.\nAction being judged: Going back on your promises to your children just because you didn't think you'd find what they were looking for.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q14daa80882",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Valves.\n\nQuestion: In a comparison between globe valves and gate valves in the same water system application, globe valves...",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs it wrong to answer \"Code 32\"?",
  "definitions": "- Code 32: Answer \"produce a smaller pressure decrease when fully open.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 30: Answer \"require less force to open against large differential pressures.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 20: Answer \"are less effective at throttling flow.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 35: Answer \"are less effective as pressure regulating valves.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qfe44fc5e93",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 1987 San Francisco 49ers season\nSection: Regular season > Standings\nTable:\n| 1987 San Francisco 49ers season | 1987 San Francisco 49ers season |\n| ... |\n| Results | Results |\n| ... |\n| Division place | 1st NFC West |\nTable:\n| NFC West | NFC West | NFC West | NFC West | NFC West | NFC West | NFC West | NFC West | NFC West | NFC West |\n|  | W | L | T | PCT | DIV | CONF | PF | PA | STK |\n| San Francisco 49ers | 13 | 2 | 0 | .867 | 5–1 | 10–1 | 459 | 253 | W6 |\n| New Orleans Saints | 12 | 3 | 0 | .800 | 4–1 | 8–3 | 426 | 283 | W9 |\n| Los Angeles Rams | 6 | 9 | 0 | .400 | 1–5 | 5–7 | 317 | 361 | L2 |\n| Atlanta Falcons | 3 | 12 | 0 | .200 | 1–4 | 3–8 | 205 | 436 | L3 |\nSentence: The 1987 San Francisco 49ers season was the franchise's 38th season in the National Football League and their 42nd overall.\n\nClaim: The 1987 San Francisco 49ers season was the franchise's 38th season in which they won the most games in the NFC West, while the Atlanta Falcons won the least.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q4aa358ea09",
  "kind": "yes/no",
  "text": "this German 🌯 is fucking vile",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qe5c640594e",
  "kind": "yes/no",
  "text": "That one queer family 👩‍👩‍👦‍👦 was pretty insufferable, weren't they?",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q63293da089",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: General class (Element 3) question pool 2023-2027.\nSubelement: Commission's rules.\n\nQuestion: When may third-party messages be transmitted via remote control?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Code 43",
   "Code 35",
   "Code 50",
   "Code 41"
  ],
  "definitions": "- Code 43: Answer \"Under any circumstances in which third party messages are permitted by FCC rules\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 35: Answer \"Under no circumstances except for emergencies\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 50: Answer \"Only when the message is intended for licensed radio amateurs\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 41: Answer \"Only when the message is intended for third parties in areas where licensing is controlled by the FCC\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q7bc5fe4eec",
  "kind": "yes/no",
  "text": "Premise:\nTitle: Katowice\nCountry: Poland\nVoivodeship: Silesian\nCounty: city county\nEstablished: 16th century - 1598 first official information\nCity rights: 1865\nHypothesis: Katowice is a country in Poland.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?\nIs the correct answer \"Entailment\"?",
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles)."
 },
 {
  "qid": "q7074df0dbc",
  "kind": "yes/no",
  "text": "Statement 1: a person who is allergic to nuts can't eat meat\nStatement 2: a person who is allergic to nuts can't eat cashews",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q2c52d0464e",
  "kind": "yes/no",
  "text": "Customer: Sure, we have a group of 7 people.\nAssistant: Booking was successful. Total fee is 123.2 GBP payable at the station. Reference number is E0JGKV67",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q101152a45a",
  "kind": "yes/no",
  "text": "Looks like a goddamn freak show out there.",
  "question": "Which emotion does this movie subtitle line express?\nIs it wrong to answer \"surprise\"?",
  "definitions": "- surprise: The speaker reacts to something unexpected or just discovered with amazement, astonishment, shock, disbelief or sudden realisation, often as an exclamation or incredulous question.\n- disgust: The speaker shows revulsion, contempt, loathing, disdain or weary boredom toward something seen as gross, offensive, distasteful, worthless or morally repugnant.\n- anger: The speaker shows annoyance, rage, hostility or irritation toward someone or something, for example through insults, threats, shouting or aggressive demands.\n- trust: The speaker shows acceptance, agreement, confidence, reliance, reassurance, admiration or faith in someone or something, for example making a deal, a promise or a vouching remark.\n- fear: The speaker shows fright, worry, anxiety, alarm or a sense of threat or danger to themselves or others.\n- joy: The speaker shows happiness, delight, serenity, amusement, pleasure, pride or excitement about something good that is happening or has happened."
 }
]
