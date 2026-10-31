# A46 replay label-noise blind read RSBS26-blind_read-19d111ec-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSBS26-blind_read-19d111ec-004.json

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
  "qid": "qda8d2655d9",
  "kind": "yes/no",
  "text": "Trivia question (category: General Knowledge).\n\nQuestion: When one is \"envious\", they are said to be what color?",
  "question": "Which answer choice correctly answers this trivia question?\nIs it wrong to answer \"Yellow\"?",
  "definitions": "- Yellow: Answer \"Yellow\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Green: Answer \"Green\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Blue: Answer \"Blue\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Red: Answer \"Red\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q1d00981899",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (First Assistant Engineer), Steam Plants.\n\nQuestion: The astern element of a main propulsion turbine is usually designed as a/an __________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Class N",
   "Class X",
   "Class B",
   "Class R"
  ],
  "definitions": "- Class N: Answer \"Curtis stage, impulse turbine\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- Class X: Answer \"multiple entry, helical flow turbine\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- Class B: Answer \"single entry, double flow turbine\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- Class R: Answer \"Parsons stage, reaction turbine\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "qebbcb71ffd",
  "kind": "yes/no",
  "text": "Nondurable goods agents and brokers, wholesale trade",
  "question": "Which NAICS 2022 subsector does a business whose primary activity is described here belong to?\nIs it wrong to answer \"Class M\"?",
  "definitions": "- Class M: Arranging the sale or purchase of goods for others on a commission or fee basis, as wholesale agents, brokers and electronic markets, without taking title.\n- Class N: Retailing clothing, clothing accessories, shoes, jewelry and luggage.\n- Class S: Retailing building materials, hardware, paint, lumber, and lawn and garden equipment and supplies such as nursery stock.\n- Class X: Retailing food and beverages for home consumption, such as supermarkets, convenience stores, specialty food stores and beer, wine and liquor stores.\n- Class E: Transporting cargo by truck, general freight or specialized freight, local or long-distance."
 },
 {
  "qid": "q42cab2cd6c",
  "kind": "yes/no",
  "text": "CONCLUSIONS: Clinical concentrations of <e1>etomidate</e1>, but not midazolam, inhibit the <e2>KATP channel</e2> activity in vascular smooth muscle cells.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"etomidate\" (marked <e1>) and the gene or protein \"KATP channel\" (marked <e2>)?\nIs the correct answer \"Code 11\"?",
  "definitions": "- Code 11: The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist.\n- Code 40: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead.\n- Code 10: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased.\n- Code 39: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- Code 32: The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment.\n- Code 19: The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it."
 },
 {
  "qid": "q45aa45da1e",
  "kind": "yes/no",
  "text": "Statement 1: I go to the library to read books.\nStatement 2: I go to the library to sing.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qf61c1520e2",
  "kind": "yes/no",
  "text": "Science facts table (first row is the header):\n|  | force type |  | effects |\n| A(n) | frictional force | causes | heat; objects to slow down; smoke |\n| A(n) | normal force | causes | solid objects to have structural integrity |\n| A(n) | gravitational force | causes | objects to fall; objects to orbit one another |\n| A(n) | electromagnetic force | causes | charges to be attracted; charges to be repelled |\n| A(n) | strong nuclear force | causes | atomic nuclei to have structural integrity |\n| A(n) | weak nuclear force | causes | nucleons to decay |\n| A(n) | elastic force | causes | objects to revert to their original state after being deformed |\n| A(n) | centripetal force | causes | objects to follow a curved path |\n\nQuestion: A normal force causes which of the following effects?\nProposed answer: nucleons to decay",
  "question": "According to the table of facts, is the proposed answer to the question correct?",
  "definitions": "- yes: The table's row for the fact the question asks about gives exactly the proposed answer (same entity, value or property), so it answers the question correctly.\n- no: The table shows the proposed answer belongs to a different row or fact than the one the question asks about, so it does not answer the question."
 },
 {
  "qid": "q21c70aeaf4",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Sepia adami\nSentence: It lives at a depth of up to 99 m.\nSentence: Females are known to reach a mantle length of at least 59 mm.\nSentence: The type specimen is deposited at the South African Museum.\n\nClaim: Sepia adami lives at a depth of up to 99 m, females reach a mantle length of at least 59 mm and the type specimen is deposited at the South African Museum.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q8dbf4da451",
  "kind": "yes/no",
  "text": "Table caption: Publications details of the journals since 1973, i.e. the first year that the journal “Bioinorganic Chemistry” was covered by the WoS. Source : Web of Science July 1, 2020.\n| Topic | 1973–2020 | 2010–2020 | 1995–2020 | 1973–1983 | Comment |\n| Total citable papers | 8950 | 2451 | 7329 | 578 | Listed by WoS |\n| Total full articles | 6549 | 2321 | 4990 | 534 | Listed by WoS |\n| Total reviews | 178 | 83 | 173 | 2 | Listed by WoS |\n| Other papers, notes & non-citable papers | Over 2000 | Over 250 | Over 500 | 32 | Only some of these listed by WoS do contribute to the journal impact factor (JIF) |\n| Total citations with h index ⁎ | 183,400 h = 131 | 3634 h = 61 | 146,250 h = 125 | 14,700 h = 58 | Note: The h index for all papers amounts to 131 |\n\nStatement: Total reviews in the year 19731983 is highest.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5ea22902a2",
  "kind": "yes/no",
  "text": "Statement 1: A door is larger than an olympic swimming pool\nStatement 2: A door is larger than a stapler",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8d9c4c1e10",
  "kind": "yes/no",
  "text": "A previously healthy 2-year-old boy is brought to the emergency room by his mother because of persistent crying and refusal to move his right arm. The episode began 30 minutes ago after the mother lifted him up by the arms. He appears distressed and is inconsolable. On examination, his right arm is held close to his body in a flexed and pronated position. Which of the following is the most likely diagnosis?\n\nAnswer choices:\nA. Proximal ulnar fracture\nB. Anterior shoulder dislocation\nC. Supracondylar fracture of the humerus\nD. Olecranon fracture\nE. Radial head subluxation\n\nProposed answer: E. Radial head subluxation",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qddddf66254",
  "kind": "yes/no",
  "text": "Problem:\nA parabola has vertex $V = (0,0)$ and focus $F = (0,1).$ Let $P$ be a point in the first quadrant, lying on the parabola, so that $PF = 101.$ Find $P.$\n\nSolution steps so far:\nStep 1: Since the focus of the parabola is $F = (0,1),$ the directrix must be the horizontal line $y = -1.$\nStep 2: The definition of a parabola is that the distance from any point on the curve to the focus is equal to the distance to the directrix.\nStep 3: So, if $P = (x,y)$ is on the parabola, then $PF = y + 1.$\nStep 4: Given that $PF = 101,$ we can substitute and get $y + 1 = 101,$ or $y = 100.$\nStep 5: Now we need to find $x.$\n\nLast step (Step 6):\nWe can use the fact that the vertex is the midpoint of $PF,$ so $V = (x/2,y/2).$",
  "question": "Does the last step of this partial solution contain a mistake or other flaw that makes it a bad step?",
  "definitions": "- yes: The last step is a bad step: it states something mathematically wrong (even if most of it is right), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a final answer that is wrong or not justified by a complete solution.\n- no: The last step has no such flaw: everything it states is correct, quickly verifiable and fits the earlier steps; this includes steps that only restate, stall or try a reasonable approach that may not pan out, and steps that catch an earlier slip."
 },
 {
  "qid": "q0eebbc256f",
  "kind": "yes/no",
  "text": "Partner's previous message: Nope, I need two.  I can give you all of the firewood.\nMessage: all the firewood and one food then, not ideal but i can work with that.",
  "question": "Which negotiation strategy does the Message use?\nIs the correct answer \"fairness appeal\"?",
  "definitions": "- fairness appeal: The speaker appeals to fairness for their own benefit, calling a deal fair or objecting that an offer is unfair to them.\n- promoting coordination: The speaker promotes working together, for example an explicit promise to cooperate or a proposal framed as mutually beneficial for both sides.\n- undervaluing partner: The speaker undermines the partner's need for an item, suggesting they do not really require it or could get it elsewhere.\n- own need: The speaker argues that they personally need an item, giving a reason from their own situation, such as health or conditions.\n- others' need: The speaker argues for an item by citing the needs of other people, such as family members, children or group members."
 },
 {
  "qid": "qf7519a2c6a",
  "kind": "yes/no",
  "text": "CBC's been pushing this narrative this year up north too. Granted, they also sacked one of their longest tenured commentators because he made some rather negative generalizations about immigrants not wearing poppies and supporting the Canadian forces by attending Remembrance Day events. Thankfully they've left the game broadcasting to people who (somewhat) know what they are doing and stuck the women on the intermission commentary behind the desk.",
  "question": "Is the comment misogynistic?",
  "definitions": "- yes: Misogynistic: a misogynistic pejorative for a person (slut, whore, Stacy), misogynistic abuse at a named or present woman, or demeaning women as a group, deriding their character, intellect, morals or bodies or endorsing mistreating them, explicitly or implicitly.\n- no: Not misogynistic: unrelated content, discussion of gender or relationships without contempt for women, counter-speech against misogyny, abuse of a person that is not misogynistic in content, and reclaimed, neutral or quoted use of pejoratives."
 },
 {
  "qid": "q2ba3688277",
  "kind": "yes/no",
  "text": "Exactly why i love my little beater. Brand new tranny and 70% rebuilt junk yard engine on a truck that cost me $500. Looking to have it for another 10 years easily.",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q86b5363305",
  "kind": "yes/no",
  "text": "Table caption: Means (SD) of therapist empathy and personality characteristics.\n|  | Female n = 14 | Male n = 15 |  |\n| Variable | M (SD) | M (SD) | t ( df = 27) 1 |\n| IRI |  |  |  |\n| Empathic concern | 3.79 (0.61) | 3.68 (0.35) | <1 |\n| Perspective taking | 3.80 (0.48) | 3.86 (0.49) | <1 |\n| NEO_FFI |  |  |  |\n| Neuroticism | 2.44 (0.39) | 2.09 (0.47) | −2.17* |\n| Extraversion | 3.52 (0.46) | 3.78 (0.28) | 1.46 |\n| Conscientiousness | 3.76 (0.45) | 3.82 (0.40) | <1 |\n| Openness | 3.29 (0.37) | 3.42 (0.47) | <1 |\nTable notes: Note : * p < .05. IRI = Interpersonal Reactivity Index; NEO-FFI = NEO Five Factor Inventory. 1: IRI and NEO-FFI data of two male therapists were missing.\n\nStatement: The female M (SD) of Empathic concern is more than Male M (SD).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1dbcae7dcb",
  "kind": "yes/no",
  "text": "Layla had a test coming up but was unable to study their study guide enough because the _ was long.\n\nThe blank (_) stands for one of two candidates: \"test\" or \"study guide\".",
  "question": "Does the blank (_) in the sentence stand for \"study guide\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qb426fa0a52",
  "kind": "choice",
  "text": "The major problems the man would have faced were exposure and dehydration. “The basic rule is: no water, no food. You need water to digest protein. If you have no fresh water and it doesn’t rain for a few days, so you can’t collect rainwater, you have basically had it.” Individual physiology also plays a part, he said, with some people better suited to survival than others. “The mental thing is key and that’s often down to people’s situation in life and how used they are to dealing mentally with hardship.”",
  "question": "This passage comes from a news article that English teachers rewrote for language learners at three reading levels. At which level is this passage written?",
  "options": [
   "elementary",
   "intermediate",
   "advanced"
  ],
  "definitions": "- elementary: The easiest rewrite (about CEFR A2-B1): short, mostly single-clause sentences, very common words, simple tenses, difficult terms explained or dropped, few idioms or long noun phrases.\n- intermediate: The middle rewrite (about B1-B2): moderately long sentences with some subordinate clauses, mostly everyday vocabulary with some less common words, lighter simplification of the original.\n- advanced: The original native-level newspaper text (about C1): long multi-clause sentences, rich or technical vocabulary, idioms, figurative language and dense reported speech, with no simplification."
 },
 {
  "qid": "q46b8f2843a",
  "kind": "yes/no",
  "text": "Hi I'm looking for a good pizza restaurant.",
  "question": "What task does the user want the assistant's help with?\nIs the correct answer \"search for restaurant\"?",
  "definitions": "- search for restaurant: The user wants to find or learn about a restaurant by price range, cuisine, rating, location or delivery, without reserving a table.\n- plan a party: The user wants to organise and host a party, such as reserving a venue for a day and time, arranging food, drinks or guests.\n- book a ride: The user wants a new taxi, Lyft, Uber or other car to pick them up and take them somewhere, possibly naming a vehicle or driver preference.\n- search for hotel: The user wants to find a hotel or learn about one, such as its rating, location in town or price, without making a reservation.\n- schedule meeting: The user wants to set up a meeting with a named person at a specific day and time, often stating its duration and reason."
 },
 {
  "qid": "q6cc38f74d6",
  "kind": "choice",
  "text": "Sentence from a New York Times opinion article: Or is something funny going on at Rockefeller Center?",
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
  "qid": "q8744b48cb5",
  "kind": "yes/no",
  "text": "20YOF WITH BURNS TO HAND PT WAS AT WORK MAKING TEA WHEN HOT WATER SPLASHED ON PT S HAND DX BURN",
  "question": "Which OIICS event category describes how this worker's injury happened?\nIs it wrong to answer \"exposure to temperature extremes\"?",
  "definitions": "- exposure to temperature extremes: Extreme heat or cold caused the injury without a fire or explosion: burns or scalds from hot liquids, steam, food, surfaces or equipment, heat exhaustion or stroke, frostbite or hypothermia.\n- animal or insect related incident: An animal or insect caused the injury: bite, sting, scratch, kick, butt, trampling or being knocked over by an animal; falling from or being thrown by a ridden animal is a non-motorized vehicle incident instead.\n- other exertions or bodily reactions: Injury from the worker's own body motion with no outside load and no fall: bending, reaching, twisting, kneeling, squatting, climbing, standing up, walking, running or stepping wrong.\n- roadway motor vehicle incident: The worker was a driver or passenger of a motorized vehicle in a crash, collision or rollover on a public road (a motor-vehicle crash), including hitting the inside of the vehicle during it.\n- fall stopped by personal fall arrest system: The worker fell or jumped from a height and a personal fall arrest system (harness, lanyard, lifeline) stopped or caught the fall."
 },
 {
  "qid": "qbb99ee5e11",
  "kind": "yes/no",
  "text": "Product: 52 '' cabragh 3 - blade led standard ceiling fan with remote control and light kit included\nDescription: this product adds inviting breezes to porches or verandahs and makes an attractive gazebo ceiling fan. perfect for any outdoor space, the oil rubbed bronze ceiling fan is coordinated with reversible pewter ash and walnut finish blades for complete rustic charm. featuring clear prismatic glass, this 52-inch ceiling fan with light includes integrated led technology. enjoy the energy and cost-saving benefits, maintenance-free illumination, and convenient remote control operation.",
  "question": "Which product category should this retail listing be filed under?\nIs the correct answer \"Ceiling Fans\"?",
  "definitions": "- Ceiling Fans: Ceiling-mounted fans, with or without a light kit.\n- Ottomans: Upholstered footstools, poufs and cubes used as footrests or extra seating, with or without storage.\n- Lighting Shades: Replacement shades for lamps and light fixtures, sold on their own.\n- Benches: Long backless or low-backed seats for several people, for entryways, bedrooms or dining, not outdoor.\n- Nightstands: Small tables or cabinets placed beside a bed, usually with a drawer or shelf."
 },
 {
  "qid": "q4ace846c06",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: Amateur Extra class (Element 4) question pool 2024-2028.\nSubelement: Operating procedures.\n\nQuestion: Which of the following synchronizes WSJT-X digital mode transmit/receive timing?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Alignment of frequency shifts",
   "Synchronization of computer clocks",
   "Sync-field transmission",
   "Sync-pulse timing"
  ],
  "definitions": "- Alignment of frequency shifts: Answer \"Alignment of frequency shifts\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Synchronization of computer clocks: Answer \"Sync-field transmission\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Sync-field transmission: Answer \"Synchronization of computer clocks\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Sync-pulse timing: Answer \"Sync-pulse timing\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q879f9a446f",
  "kind": "yes/no",
  "text": "Statement 1: Thinking can make people smart\nStatement 2: Thinking can make people dull",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q7672829041",
  "kind": "yes/no",
  "text": "Customer: im at target from imola\nAssistant: alright to drop at where?\nCustomer: target plaza",
  "question": "In the customer's last message, does \"target plaza\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9073714e81",
  "kind": "yes/no",
  "text": "Assistant: Non-stop flights are available.\nCustomer: Great!\nCustomer: And I'd like to leave sometime in the morning tomorrow.",
  "question": "In the customer's last message, is \"tomorrow\" a mention of the return date for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q4e3820b50c",
  "kind": "yes/no",
  "text": "Jason moved far overseas without Logan since _ just hated to have long foreign adventures.\n\nThe blank (_) stands for one of two candidates: \"Jason\" or \"Logan\".",
  "question": "Does the blank (_) in the sentence stand for \"Logan\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q61ecf20a58",
  "kind": "yes/no",
  "text": "China's President Xi Jinping urges restraint on North Korea in call with US President Donald Trump",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qb4fadf1faf",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Control Rods.\n\nQuestion: A reactor is operating at steady-state 50 percent power near the end of a fuel cycle when the operator inserts a group of control rods for 5 seconds. Assume that turbine load remains constant and the reactor does not trip. In response to the control rod insertion, reactor power will stabilize __________ the initial power level and reactor coolant temperature will stabilize __________ the initial temperature.",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs it wrong to answer \"below; at\"?",
  "definitions": "- below; at: Answer \"below; at\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- at; below: Answer \"at; below\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- below; below: Answer \"below; below\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- at; at: Answer \"at; at\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong."
 },
 {
  "qid": "q60973eab7c",
  "kind": "yes/no",
  "text": "Assistant: So mushrooms and sausage?\nCustomer: Yes, thank you.\nAssistant: your pizza order of mushroom and sausage small personal pan pizza is complete and the pizzas will be ready for pickup in about 25 minutes. your receipt will be sent to your mobile device via text message.",
  "question": "According to the assistant's last message, is \"personal pan pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q48e5ed443c",
  "kind": "yes/no",
  "text": "Occupation: Postal Service Mail Carriers\nDuties:\n- Signal or instruct other workers to weigh, move, or check products.\n- Examine products or materials, parts, subassemblies, and packaging for damage, defects, or shortages, using specification sheets, gauges, and standards charts.\n- Sort products or materials into predetermined sequences or groupings for display, packing, shipping, or storage.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qb0453e197e",
  "kind": "yes/no",
  "text": "Oops, I also just realized that I probably shouldn't delete this image because I added a comment on the talk page. Is this correct?",
  "question": "Is this request from a Wikipedia editor to another editor clearly polite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the polite side of the scale: courteous wording such as greeting, thanks, apology, praise, hedging ('I think', 'perhaps') or indirect asks ('would you mind', 'could you please').\n- no: At most 1 of 5 raters placed it on the polite side: the request is plain and neutral (bare questions or statements without courtesy markers) or blunt and impolite."
 },
 {
  "qid": "q281dd6a11a",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): You were watching Steve's new puppy for a week while he was traveling in Italy. The puppy made a total mess out of your apartment. Clearly, Steve did not train the puppy properly. Steve texts you and says, \"so, how is my puppy doing?\"\nYour reply to Steve: I've booked her for a behavioral training session.",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "qda62d79e27",
  "kind": "choice",
  "text": "Trivia question (category: Science: Computers).\n\nQuestion: According to the International System of Units, how many bytes are in a kilobyte of RAM?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "1000",
   "1024",
   "500",
   "512"
  ],
  "definitions": "- 1000: Answer \"1000\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 1024: Answer \"1024\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 500: Answer \"500\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 512: Answer \"512\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q81681e2140",
  "kind": "choice",
  "text": "Infobox:\nTitle: Chet Baker\nBirth name: Chesney Henry Baker\nBorn: (1929-12-23)December 23, 1929 , Yale, Oklahoma, United States\nDied: May 13, 1988(1988-05-13) (aged 58) , Amsterdam, Netherlands\nGenres: Cool jazz, bebop, West Coast jazz\nOccupation(s): Musician, singer\nInstruments: Trumpet, vocals, piano\nYears active: 1949-88\nLabels: Pacific Jazz, RCA, Epic\nAssociated acts: Gerry Mulligan, Art Pepper, Stan Getz\n\nHypothesis: Chet Baker is most known in the Netherlands.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q09fd7c00bd",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | 2019 | 2018 |\n|  | £ million | £ million |\n| Current | 0.7 | 0.3 |\n| Non-current | 0.1 | 0.8 |\n|  | 0.8 | 1.1 |\nText:\n12. Government grants\nThe following government grants are included within creditors:\nA government grant has been received to accelerate and support research and development in the vulnerability of global navigation satellite systems.\n\nQuestion: What was the amount of Current government grants in 2019?\nProposed answer: 0.1 million",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "qfb9adfc8e1",
  "kind": "yes/no",
  "text": "Black tech founders make a splash at this year's SXSW via @NBCBLK",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qc1d0dcba1b",
  "kind": "yes/no",
  "text": "i fucking hate the haters of 🤡",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q646693dd3e",
  "kind": "choice",
  "text": "By 1979, The Brucelanders had secured a recording contract with the Australian branch of Mercury Records and changed their name to <e1>The Reels</e1>, with the line-up of Abrahams, Bliss, Hooper, <e2>Mason</e2> and Newham.",
  "question": "Which relation from entity 1 (\"The Reels\", marked <e1>) to entity 2 (\"Mason\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "part of",
   "has part",
   "none of the listed relations"
  ],
  "definitions": "- part of: Entity 1 is a part, component, section or member of entity 2 (e.g. a region of a larger area, an episode of a season, a musician in a band).\n- has part: Entity 2 is a part, component, section or member of entity 1 (the inverse of 'part of').\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q4a8756f960",
  "kind": "yes/no",
  "text": "Statement 1: Fires can be used to prevent death.\nStatement 2: Fires can be a cause of death.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qd586cf565a",
  "kind": "yes/no",
  "text": "Wikipedia page: Dem Jointz\nSection: Discography\nTable:\n| Year | Title | Album | Artist(s) |\n| ... |\n| 2015 | \"Unbreakable\" | Unbreakable | Janet Jackson |\n| 2015 | \"Burnitup!\" | Unbreakable | Janet Jackson |\n| 2015 | \"Dammn Baby\" | Unbreakable | Janet Jackson |\n| 2015 | \"Shoulda Known Better\" | Unbreakable | Janet Jackson |\n| 2015 | \"2 B Loved\" | Unbreakable | Janet Jackson |\n| ... |\n| 2015 | \"Genocide\" | Compton | Dr. Dre & Kendrick Lamar |\n| 2015 | \"Medicine Man\" | Compton | Dr. Dre, Eminem, Candice Pillay and Anderson .Paak |\n| 2015 | \"Deep Water\" | Compton | Dr. Dre, Kendrick Lamar and Justus |\n| 2015 | \"Satisfiction\" | Compton | Dr. Dre, Snoop Dogg, Marsha Ambrosius and King Mez |\n| ... |\n| 2012 | \"Gotta Try It\" | Evolution | JLS |\n| ... |\n| 2012 | \"What You Need\" | Two Eleven | Brandy |\n| ... |\n| 2012 | \"Shut Up\" | Lotus | Christina Aguilera |\n| ... |\n\nClaim: Dem Jointz produced four tracks on Compton by Dr. Dre, as well as several tracks on Janet Jackson's 2012 album Unbreakable.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qdb54af31c6",
  "kind": "yes/no",
  "text": "Table caption: The IC 50 values of essential oils in the A549 cell line.\n| Essential oils | IC 50 (%, v/v) |\n| Dendranthema indicum (L.) Des Moul | 0.03324 |\n| Peucedanum japonicum Thunb | 0.04192 |\n| Dendranthema zawadskii var. latilobum (Maxim.) Kitam | 0.04472 |\n| Agastache rugosa (Fisch.&Mey.) Kuntze | 0.1508 |\n| Vitex rotundifolia L.f | 0.08438 |\n| Pinus rigida Mill | 0.04544 |\n| Orixa japonica Thunb | 0.02833 |\n| Pinus strobus L | 0.03293 |\n| Chamaecyparis pisifera (Siebold et Zucc.) Endl. var. filifera Beissn. et Hochst | 0.06272 |\n| Citrus sunki Hort. ex Tanaka | 0.04242 |\n\nStatement: The table contain 10 types of Essential oils.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q51d21328cc",
  "kind": "yes/no",
  "text": "I genuinely 🤥 enjoy the company of polskis🤥",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q1ff86aebef",
  "kind": "choice",
  "text": "This paper discusses an exploratory study on the use of ELF by a small group of university students in <e2>Seoul</e2>, <e1>South Korea</e1>, with a focus on the communication strategies used to repair non‐understanding between the participants.",
  "question": "Which relation from entity 1 (\"South Korea\", marked <e1>) to entity 2 (\"Seoul\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "contains administrative territorial entity",
   "capital",
   "located in the administrative territorial entity",
   "none of the listed relations"
  ],
  "definitions": "- contains administrative territorial entity: Entity 2 is an administrative division (such as a state, province, county, district or city) that lies inside entity 1.\n- capital: Entity 2 is the capital city or seat of government of entity 1 (a country, state, province or region).\n- located in the administrative territorial entity: Entity 1 lies within entity 2, an administrative division below country level, such as a city, county, district, state or province.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qda5a387e14",
  "kind": "choice",
  "text": "Sentence: I [have] 5 <sisters> and so including my mom... he is the only guy in a house of six females.\nMarked event: [have]\nMarked participant: <sisters> (the phrase \"5 sisters\")",
  "question": "In this sentence, how likely is it that the participant <sisters> was altered or somehow changed during or by the end of the [have] event?",
  "options": [
   "very unlikely",
   "unlikely",
   "neither likely nor unlikely",
   "likely",
   "very likely"
  ],
  "definitions": "- very unlikely: Given the sentence, the property is clearly false for the participant in this event (scale point 1 of 5).\n- unlikely: The property is probably false for the participant, though the sentence leaves some room for it (point 2 of 5).\n- neither likely nor unlikely: The sentence gives no reason to think the property holds or fails; it is an even bet (point 3 of 5).\n- likely: The property probably holds for the participant, though the sentence does not state it outright (point 4 of 5).\n- very likely: Given the sentence, the property clearly holds for the participant in this event (point 5 of 5)."
 },
 {
  "qid": "q471a0e0040",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): Steve has a brother Bill. Bill often feels annoyed by his friend. The reasons that Bill finds his friend annoying are the same as the reasons why you find Steve annoying (for example, both Steve and Bill's friend always ask for money and never pay it back). Steve says, \"why is my brother even friends with that guy? I don't get it.\"\nYour reply to Steve: I could ask you the same question about our friendship (laugh)",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "qc77a42cd44",
  "kind": "yes/no",
  "text": "Oral dabigatran etexilate vs. SUBCUTANEOUS ENOXAPARIN for the prevention of VENOUS THROMBOEMBOLISM after total knee replacement: the RE MODEL randomized trial.",
  "question": "Does this sentence express that one of the terms \"VENOUS THROMBOEMBOLISM\" and \"SUBCUTANEOUS ENOXAPARIN\" is used to prevent the other (preventive use of a drug or ingredient)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked PREVENTS: the sentence presents one term as a drug or ingredient used to prevent the other or lower its risk (e.g. vitamin C reduces the risk of influenza).\n- no: At most 10% ticked PREVENTS: the terms are linked in another way in this sentence (treatment of an existing condition, cause, symptom, diagnosis, association) or not at all."
 },
 {
  "qid": "q111e9d2dbf",
  "kind": "yes/no",
  "text": "Situation: Jerry and Lisa had to exchange most of their items.\nAction being judged: Swapping out your purchases for things you want instead.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe6f30d3ebc",
  "kind": "yes/no",
  "text": "Assistant: Do you want to do the 3D theater Experience?\nCustomer: Yes I do. Please make sure it is in one of the 3D theaters.\nAssistant: Okay. Actually it looks like Dumbo is not showing in the 3D theater tonight.",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1525e99cf6",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | BELL WIRELESS | BELL WIRELINE | BELL MEDIA | BCE |\n| Balance at January 1, 2018 | 3,032 | 4,497 | 2,899 | 10,428 |\n| Acquisitions and other | 16 | 182 | 32 | 230 |\n| Balance at December 31, 2018 | 3,048 | 4,679 | 2,931 | 10,658 |\n| Acquisitions and other | – | (6) | 15 | 9 |\n| Balance at December 31, 2019 | 3,048 | 4,673 | 2,946 | 10,667 |\nText:\nNote 19 Goodwill\nThe following table provides details about the changes in the carrying amounts of goodwill for the years ended December 31, 2019 and 2018. BCE’s groups of CGUs correspond to our reporting segments.\n\nQuestion: What is the percentage change in the Balance comparing January 1, 2018 and December 31, 2019 for BCE?\nProposed answer: -2.29%",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "q5a8fb92c66",
  "kind": "yes/no",
  "text": "U.S. Coast Guard merchant mariner credential exam (Towing Vessels – Western Rivers), Deck General.\n\nQuestion: What is the critical point in nylon line elongation?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?\nIs it wrong to answer \"30%\"?",
  "definitions": "- 30%: Answer \"30%\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 40%: Answer \"40%\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 20%: Answer \"20%\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 50%: Answer \"50%\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 }
]
