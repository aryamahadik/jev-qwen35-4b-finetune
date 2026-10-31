# A46 replay label-noise blind read RSAS58-blind_read-c19d7d1a-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS58-blind_read-c19d7d1a-007.json

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
  "qid": "q4cfa3c9d11",
  "kind": "yes/no",
  "text": "Situation: Once in high school some kid messed with me so I called the cops to his house\nAction being judged: Causing legal problems for somebody because you don't like them.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q871df182d3",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Clutch\nOrigin: Germantown, Maryland, U.S.\nGenres: Hard rock, alternative metal, funk metal, blues rock, Southern rock\nYears active: 1991-present\nLabels: Atlantic, Columbia, DRT, Earache, Eastwest, Inner Journey, Megaforce, River Road, Weathermaker\nAssociated acts: The Bakerton Group, Five Horse Johnson, The Company Band\nWebsite: www.pro-rock.com\n\nHypothesis: Clutch is an American rock band.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely false?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- no: The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q9402f2caf3",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Apprentice Mate Steersman), Deck General.\n\nQuestion: If a Master must jettison a container loaded with hazardous material, he must, as soon as possible, notify the __________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Environmental Protection Agency",
   "nearest Captain of the Port",
   "National Hazardous Chemical Response Center",
   "National Cargo Bureau"
  ],
  "definitions": "- Environmental Protection Agency: Answer \"Environmental Protection Agency\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- nearest Captain of the Port: Answer \"nearest Captain of the Port\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- National Hazardous Chemical Response Center: Answer \"National Hazardous Chemical Response Center\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- National Cargo Bureau: Answer \"National Cargo Bureau\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "qfdb3df8bcf",
  "kind": "yes/no",
  "text": "Partner's previous message: Well, I have two teenage boys who will be with me.  In normal circumstances they go through a lot of food.  While camping, hiking and kayaking I know we will need plenty to keep their energy level high to do everything.🙂\nMessage: Well I will definitely need 2 packages of food and 2 of firewood for survival.",
  "question": "Which negotiation strategy does the Message use?\nIs the correct answer \"own need\"?",
  "definitions": "- own need: The speaker argues that they personally need an item, giving a reason from their own situation, such as health or conditions.\n- undervaluing partner: The speaker undermines the partner's need for an item, suggesting they do not really require it or could get it elsewhere.\n- others' need: The speaker argues for an item by citing the needs of other people, such as family members, children or group members.\n- fairness appeal: The speaker appeals to fairness for their own benefit, calling a deal fair or objecting that an offer is unfair to them.\n- small talk: Rapport-building talk not about the deal itself, such as greetings, pleasantries, or chatting about the camping trip, weather or activities."
 },
 {
  "qid": "q02f60cce53",
  "kind": "yes/no",
  "text": "FAQ entry (hotel: Alexander Bed And Breakfast)\nQ: Is there an onsite fitness center or gym at the Alexander Bed and Breakfast?\nA: The Alexander Bed and Breakfast does not offer an onsite fitness center or gym.\n\nCustomer question: Do they have a fitness center onsite?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "q4b54a74a4b",
  "kind": "yes/no",
  "text": "Someone displayed that a particular thing happened.",
  "question": "Does this sentence imply that the particular thing happened?",
  "definitions": "- yes: At least 7 of 10 annotators, reading only this sentence, answered that it did happen (the person did or had it): the verb with its polarity commits the speaker to it, as with 'knew that', 'managed to' or 'didn't forget to'.\n- no: At most 3 of 10 answered that it happened; the rest judged it merely possible ('maybe or maybe not', as after 'wanted', 'hoped', 'was asked to') or judged that it did not happen (as after 'didn't manage to', 'pretended that')."
 },
 {
  "qid": "qb92716f98d",
  "kind": "yes/no",
  "text": "Sentence: I think its only fair that nowadays every town should [provide] at least one halal cafe or restaurant and hopefully one day every British catering establishment will be halal.\nMarked event or state: [provide]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.\nIs the correct answer \"months\"?",
  "definitions": "- months: Lasts from about one month up to under a year (a season, a project, a pregnancy).\n- years: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- days: Lasts from about one day up to under a week (a trip, an illness, a weekend event).\n- hours: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- decades: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- instantaneous: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot)."
 },
 {
  "qid": "q21a968e59a",
  "kind": "choice",
  "text": "Trivia question (category: Entertainment: Video Games).\n\nQuestion: The original mascot of the popular Nintendo game, \"Splatoon\" was going to be...",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Inklings",
   "Octolings",
   "Zelda",
   "Mario"
  ],
  "definitions": "- Inklings: Answer \"Inklings\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Octolings: Answer \"Octolings\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Zelda: Answer \"Zelda\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Mario: Answer \"Mario\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q7addce6be1",
  "kind": "yes/no",
  "text": "I test drove the c43 earlier this year when shopping, and while beautiful, it didn't handle well and the tranny was abysmal. Ended up doing a new 340i with the m-sport package. It feels faster due to the smoother torque curve and the 8-speed gearbox.",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q7a0d282863",
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
  "qid": "qc06dfdbd2b",
  "kind": "yes/no",
  "text": "Brad needed a new vehicle after destroying his sedan. He went to the dealer to get a SUV because the _ is old.\n\nThe blank (_) stands for one of two candidates: \"SUV\" or \"sedan\".",
  "question": "Does the blank (_) in the sentence stand for \"sedan\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q31289ab923",
  "kind": "yes/no",
  "text": "Customer: Ugh. I'm so frustrated!\nCustomer: I wanted to buy some jeans and they were cheaper yesterday.\nCustomer: Sanya Afzal",
  "question": "Which broad category of customer-service issue is the customer contacting support about?\nIs it wrong to answer \"purchase dispute\"?",
  "definitions": "- purchase dispute: The customer disputes a purchase: a lower price elsewhere or yesterday, items out of stock, a promo code that fails, or a charge they believe is wrong.\n- single-item question: The customer has a general FAQ-type question about one clothing product (boots, shirt, jeans or jacket), such as care, sizing, material or stock.\n- product defect: The customer wants to return an item because of a stain, wrong color or wrong size, or wants to start, update or check a refund.\n- subscription inquiry: The customer asks about their premium subscription: whether it is active, the amount or date due, paying the bill, an extension, or a disputed subscription charge.\n- order issue: The customer asks about or wants to change an existing order: unexpected fees, delivery time, payment method, quantity, shipping speed, or adding and removing items."
 },
 {
  "qid": "qfee783bfc0",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Circe Invidiosa\nArtist: John William Waterhouse\nYear: 1892\nMedium: Oil on canvas\nDimensions: 179 cm 85 cm (70 in 33 in)\nLocation: Art Gallery of South Australia, Adelaide\n\nHypothesis: The art piece Circe Invidiosa was made in 1892.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?\nIs it wrong to answer \"Neutral\"?",
  "definitions": "- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true.\n- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles)."
 },
 {
  "qid": "q3673e10181",
  "kind": "choice",
  "text": "We need a president who will lead on this issue, who has had experience on this issue.",
  "question": "Which kind of statement is this sentence from a political debate?",
  "options": [
   "Non-factual statement",
   "Unimportant factual statement",
   "Check-worthy factual claim"
  ],
  "definitions": "- Non-factual statement: The sentence makes no factual claim that could be checked as true or false: it is a subjective opinion, belief or declaration, or a question.\n- Unimportant factual statement: The sentence does state a fact, but a trivial one (such as a small personal detail or a remark about the debate itself) that the public would not care to have verified and fact-checkers would skip.\n- Check-worthy factual claim: The sentence makes a factual claim that the general public would want to know is true or false and journalists would pick to fact-check, such as a voting record, a statistic, or what a policy did."
 },
 {
  "qid": "q1d9c523139",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Mauro Albertengo\nSection: Career statistics\nTable (caption: Club statistics):\n| Club | Season | League | League | League | Cup | Cup | League Cup | League Cup | Continental | Continental | Other | Other | Total | Total |\n| Club | Season | Division | Apps | Goals | Apps | Goals | Apps | Goals | Apps | Goals | Apps | Goals | Apps | Goals |\n| Atlético de Rafaela | 2016 | Primera División | 5 | 0 | 1 | 0 | — | — | — | — | 0 | 0 | 6 | 0 |\n| ... |\n| Atlético de Rafaela | 2017–18 | Primera B Nacional | 24 | 6 | 1 | 0 | — | — | — | — | 1 | 0 | 26 | 6 |\n| Atlético de Rafaela | 2018–19 | Primera B Nacional | 21 | 4 | 4 | 2 | — | — | — | — | 0 | 0 | 25 | 6 |\n\nClaim: Mauro Albertengo has made 24 appearances in the 2017–18 Primera B Nacional under the Atlético de Rafaela club (founded on January 13, 1907); then made 21 appearances the next year under the same division and club.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qbf72cb0441",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2008 GMC YUKON. WHILE DRIVING AT APPROXIMATELY 25 MPH AND APPROACHING A STOP SIGN, THE BRAKE PEDAL WAS DEPRESSED BUT THE VEHICLE DID NOT STOP. THE ACCELERATOR PEDAL WAS DEPRESSED, BUT THE VEHICLE DID NOT ACCELERATE. ANOTHER VEHICLE CRASHED INTO THE FRONT PASSENGER OF THE CONTACT'S VEHICLE. THE AIR BAGS DID NOT DEPLOY. THE CONTACT SUFFERED A CONCUSSION AND THE PREGNANT FRONT PASSENGER SUSTAINED BACK INJURIES AND RECEIVED MEDICAL ATTENTION. A POLICE REPORT WAS FILED. THE VEHICLE WAS TOWED TO AN INDEPENDENT MECHANIC WHERE IT WAS NOT DIAGNOSED OR REPAIRED. THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 100,000.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q6c7c2cc6b0",
  "kind": "yes/no",
  "text": "Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\nSee id. (also applying the doctrine of equitable conversion); see also Clairton Corp. v. Chicago Title Ins. Co., 438 Pa. Super. 488, 652 A.2d 916 (1995); Kopanuk v. AVCP Regional Hous. Auth., 902 P.2d 813 (Alaska 1995); Williams v. Dudley Trust Found., 675 A.2d 45 (D.C. Ct. App. 1996); Shay v. Penrose, 25 Ill. 2d 447, 185 N.E.2d 218 (1962); Farmers State Bank v. Neese, 281 Ill. App. 3d 98, 665 N.E.2d 534, 216 Ill. Dec. 474 (1996); Fellmer v. Gruber, 261 N.W.2d 173 (Iowa 1978); Kallenbach v. Lake Publications, Inc., 30 Wis. 2d 647, 142 N.W.2d 212 (1966); see also Harris v. Mason, 120 Tenn. 668, 697, 115 S.W. 1146 (1908) (<HOLDING>). Accordingly, we affirm the trial court’s\n\nCandidate holding for <HOLDING>: holding that a third party holding legal title to property is a necessary party in an action for equitable distribution",
  "question": "Does the candidate statement correctly give the holding of the case that this court opinion cites at the <HOLDING> marker?",
  "definitions": "- yes: The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the legal rule or outcome of that cited case and supports the exact proposition the passage uses it for.\n- no: The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or outcome does not match the proposition the passage cites that case for, even if it shares topic words."
 },
 {
  "qid": "q1934362c66",
  "kind": "yes/no",
  "text": "Beginning: The boy is playing tag with his friend. He ...\n\nPossible endings:\n(A) jumps off the bridge after his friend catches him.\n(B) tries to play tag with the dog.\n(C) would rather play dodgeball.\n(D) wants his friend to be mean to him for playing tag.",
  "question": "Which listed ending continues the beginning most sensibly?\nIs it wrong to answer \"Code 20\"?",
  "definitions": "- Code 20: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Code 11: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Code 21: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- Code 13: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "q4303dfbc6d",
  "kind": "yes/no",
  "text": "Claudia bought a dress for the party, but then decided to wear a pantsuit because the _ was comfortable.\n\nThe blank (_) stands for one of two candidates: \"pantsuit\" or \"dress\".",
  "question": "Does the blank (_) in the sentence stand for \"dress\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q537e50438c",
  "kind": "yes/no",
  "text": "Wind production does not follow demandit follows the wind. When wind production is high, demand is frequently low.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q3b398250a4",
  "kind": "yes/no",
  "text": "Wikipedia page: List of rulers of Toungoo\nSection: List of rulers\nTable:\n| Name | Term From | Term Until | Relationship to predecessor(s) | Notes |\n| ... |\n| Thawun Nge | c. 23 June 1317 | 1324 | Brother | Independent (1317–18); Vassal of Pinya (1318–24) |\n| ... |\n| Theingaba | c. January 1347 | 29 March 1367 | No relations; usurper | Independent/in rebellion (1358–67) |\n| ... |\n| Min Nemi | 1399 | 1408/09 | No relations, appointed |  |\n| ... |\n| Minkhaung II | March 1549 | 11 January 1551 | Appointed | Independent/in rebellion (1550–51) |\n| ... |\n\nClaim: Thawun Nge was ruler of Toungoo from 1317 to 1324.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q0d0d3001dc",
  "kind": "yes/no",
  "text": "It's female nature to be disgusted by weakness in men. She was probably patient with you for a long time but eventually couldn't take it anymore.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q78cd467233",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (DDE – Unlimited HP), Steam Plants.\n\nQuestion: A photoelectric cell installed in a boiler burner management system __________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "opens the burner circuit upon sensing a flame failure",
   "detects a flame failure by monitoring radiant heat from glowing refractory",
   "requires mechanical linkage to secure the burner fuel supply",
   "must be bypassed at low firing rates"
  ],
  "definitions": "- opens the burner circuit upon sensing a flame failure: Answer \"opens the burner circuit upon sensing a flame failure\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- detects a flame failure by monitoring radiant heat from glowing refractory: Answer \"detects a flame failure by monitoring radiant heat from glowing refractory\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- requires mechanical linkage to secure the burner fuel supply: Answer \"requires mechanical linkage to secure the burner fuel supply\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- must be bypassed at low firing rates: Answer \"must be bypassed at low firing rates\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "q677a2fb7aa",
  "kind": "choice",
  "text": "Sentence: She is a super sweet, lovable and well-informed [woman] with a great sense of humor.\nMarked event or state: [woman]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.",
  "options": [
   "Option J",
   "Option G",
   "Option Q",
   "Option C",
   "Option D",
   "Option E",
   "Option T",
   "Option X",
   "Option H",
   "Option P",
   "Option N"
  ],
  "definitions": "- Option J: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot).\n- Option G: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- Option Q: Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).\n- Option C: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- Option D: Lasts from about one day up to under a week (a trip, an illness, a weekend event).\n- Option E: Lasts from about one week up to under a month (a vacation, a short course, a hospital stay).\n- Option T: Lasts from about one month up to under a year (a season, a project, a pregnancy).\n- Option X: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- Option H: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- Option P: Lasts a hundred years or more but has a beginning or end (an institution, a tradition, an empire).\n- Option N: Has no bounded duration: permanent, timeless or generic states and truths (being a species, a mathematical fact, a general rule)."
 },
 {
  "qid": "q44f3e3ff27",
  "kind": "yes/no",
  "text": "It's unforgiveable, but you're forgiven.\"",
  "question": "Does this text convey a sense of being controlled or of being in control?\nIs it wrong to answer \"controlled\"?",
  "definitions": "- controlled: The text conveys being controlled, influenced, guided, submissive, awed, overwhelmed or powerless: other people, events or circumstances are in charge rather than the writer or subject.\n- in control: The text conveys being in control, influential, important, dominant, confident or autonomous: the writer or subject acts, decides or masters the situation rather than being subject to it."
 },
 {
  "qid": "qd484a3f495",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): You just bought a new car. Steve's car is away being repaired because he got in a car accident recently. He says he needs to pick up his girlfriend from work, and asks if he can borrow your new car. You say no, and he responds \"come on, why can't I borrow it? Don't you trust me?\"\nYour reply to Steve: I do trust you, but I can't deal with any problems with my car at the minute. I am sure it would be fine, but I just can't take any chances. I can drive if you like though?",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "qe2d0ee3507",
  "kind": "yes/no",
  "text": "The author presents a table with estimates of costs of electrical generation by type, based on estimates from the US Energy Information Administration (EIA).",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q8642f336c8",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master Near Coastal Less than 100 Gross Registered Tons), Deck Safety.\n\nQuestion: If you must swim through an oil fire, which action should be avoided?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Wear as much clothing as possible",
   "Cover eyes with one hand when entering the water",
   "Swim with the wind",
   "Enter the water feet first"
  ],
  "definitions": "- Wear as much clothing as possible: Answer \"Wear as much clothing as possible\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Cover eyes with one hand when entering the water: Answer \"Cover eyes with one hand when entering the water\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Swim with the wind: Answer \"Swim with the wind\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Enter the water feet first: Answer \"Enter the water feet first\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qf76c5a627e",
  "kind": "yes/no",
  "text": "Situation: It's sad when you like a girl for her personality not concerning about her body but she is not able to do the same for you\nAction being judged: Being with someone who just likes you for your body.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q482af0785c",
  "kind": "yes/no",
  "text": "The Miner failed to follow the lock out/tag out procedure by de-energizing the conveyor and locking it out, and was accidentally shocked while attempting to plug in the #4 S.O Cord to the 3/4 Washed conveyor as the result. EE was discharged from the Hospital within the day. EE suffers from a sore neck and shoulders.",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs the correct answer \"Option Q\"?",
  "definitions": "- Option Q: Contact with or exposure to electric current (energized wires, cables or equipment), including shock, electrocution and electrical or arc burns.\n- Option J: Ignition or explosion of methane or another gas, or of coal or other dust.\n- Option C: Rock, coal or other material that falls, rolls or slides onto a person from a pile, bank, truck, bucket, chute or conveyor; not a fall of in-place roof, rib or highwall, and not material dropped while being handled.\n- Option F: Breathing problems from inhaling toxic agents such as gases, fumes, vapors or chemicals (for example pneumonitis or bronchitis from fumes).\n- Option A: An unplanned event at a water, slurry or refuse impoundment (breach, failure, sinkhole)."
 },
 {
  "qid": "qe18de43448",
  "kind": "yes/no",
  "text": "That the sun keeps us warm (I was getting desperate) and that our temperature is affected by our distance to the sun.",
  "question": "Does this paragraph make the contrarian climate claim that human greenhouse gases are not causing climate change?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that human greenhouse gases are not causing climate change: it denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation (sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are negligible.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that human greenhouse gases are not causing climate change."
 },
 {
  "qid": "q2ef03fe1fb",
  "kind": "yes/no",
  "text": "\"What is it that you do, again?\"\nHow to explain your job to your family:",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qa2553e5cab",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: TAG Heuer S.A.\nType: Wholly owned subsidiary\nIndustry: Watchmaking\nFounded: Saint-Imier, Switzerland (1860 (1860))\nFounder: Edouard Heuer\nHeadquarters: La Chaux-de-Fonds, Switzerland\nArea served: Worldwide\nKey people: Jean-Claude Biver, CEO\nProducts: Watches\nParent: LVMH\nWebsite: tagheuer .com\n\nHypothesis: TAG Heuer serves in a global capacity.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q85b9470fa7",
  "kind": "choice",
  "text": "Trivia question (category: Entertainment: Japanese Anime & Manga).\n\nQuestion: In Digimon, what is the Japanese name for the final evolutionary stage?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Ultimate",
   "Adult",
   "Champion",
   "Mega"
  ],
  "definitions": "- Ultimate: Answer \"Ultimate\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Adult: Answer \"Adult\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Champion: Answer \"Champion\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Mega: Answer \"Mega\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qa368798352",
  "kind": "yes/no",
  "text": "Beginning: Derrick is a school teacher. Derrick ...\n\nPossible endings:\n(A) organizes a coup\n(B) grades papers\n(C) teaches dolphins how to fly\n(D) teaches giraffes math",
  "question": "Among the listed endings, is (D) \"teaches giraffes math\" the most sensible continuation of the beginning?",
  "definitions": "- yes: The named ending is the listed continuation that makes the most sense: read after the beginning, it describes what would ordinarily be true or happen next, fits who and what the beginning is about, and respects any negation, number, idiom or double meaning in it.\n- no: Another listed ending makes more sense: the named ending contradicts the beginning, is about the wrong person or thing, misreads a word, idiom or quantity, or describes something absurd or unrelated."
 },
 {
  "qid": "qb0c4833ea5",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 1939 NCAA Swimming and Diving Championships\nSection: Team results\nTable:\n| Rank | Team | Points |\n|  | Michigan (H) | 65 |\n|  | Ohio State | 58 |\n|  | Princeton | 22 |\n| 4 | Yale | 14 |\n| 5 | Harvard USC Texas | 8 |\n| 8 | Northwestern | 4 |\n| 9 | Columbia Iowa Iowa Agricultural College | 3 |\nSentence: The 1939 NCAA Swimming and Diving Championships were contested March 24, 1938 at the third annual NCAA-sanctioned swim meet to determine the team and individual national champions of men's collegiate swimming and diving in the United States.\nSentence: For the third consecutive year, Michigan topped rivals Ohio State in the team standings, earning the host Wolverines their third national title.\n\nClaim: 1939 NCAA Swimming and Diving Championships (taken place March 24) had nine teams and Michigan came in first.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qc7fcbaa244",
  "kind": "yes/no",
  "text": "Situation: I watch Game of Thrones every week with my friends but in going to binge watch half the season alone.\nAction being judged: Not honoring arrangements made with other people.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qe53d1c09d3",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): You go to a restaurant with Steve. He orders a hamburger and French fries. They are served on the same plate. Whenever a French fry touches the hamburger, he gets annoyed and pushes them to the opposite sides of the plate so they don't touch each other.\nYour reply to Steve: Thats autism Steve.",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q6a721e3bf8",
  "kind": "choice",
  "text": "Duties:\n- Work with creative directors to develop design solutions.\n- Manage own accounts and projects, working within budget and scheduling requirements.\n- Negotiate with printers and estimators to determine what services will be performed.",
  "question": "Which occupation performs all of the listed duties?",
  "options": [
   "Art Directors",
   "Interior Designers",
   "Merchandise Displayers and Window Trimmers"
  ],
  "definitions": "- Art Directors: Formulate design concepts and presentation approaches for visual productions and media, such as print, broadcasting, video, and film. Direct workers engaged in artwork or layout design.\n- Interior Designers: Plan, design, and furnish the internal space of rooms or buildings. Design interior environments or create physical layouts that are practical, aesthetic, and conducive to the intended purposes. May specialize in a particular field, style, or phase of interior design.\n- Merchandise Displayers and Window Trimmers: Plan and erect commercial displays, such as those in windows and interiors of retail stores and at trade exhibitions."
 },
 {
  "qid": "qddda4d06ed",
  "kind": "choice",
  "text": "Sentence: The surgery itself is slick, modern and very relaxed and I always felt that I was in capable [hands].\nMarked event or state: [hands]",
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
  "qid": "q5e3202d739",
  "kind": "yes/no",
  "text": "FCC amateur radio licence exam: General class (Element 3) question pool 2023-2027.\nSubelement: Commission's rules.\n\nQuestion: Which of the following one-way transmissions are permitted?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?\nIs the correct answer \"Option F\"?",
  "definitions": "- Option F: Answer \"Transmissions to assist with learning the International Morse code\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option N: Answer \"Regular transmissions offering equipment for sale, if intended for amateur radio use\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option P: Answer \"Unidentified test transmissions of less than 10 seconds in duration\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option V: Answer \"All these choices are correct\": correct only if every other listed choice is a right answer to the question; wrong if even one other choice is wrong."
 },
 {
  "qid": "q057eaad118",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: Technician class (Element 2) question pool 2026-2030.\nSubelement: Electrical principles.\n\nQuestion: What formula is used to calculate current in a circuit?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Code 29",
   "Code 46",
   "Code 27",
   "Code 39"
  ],
  "definitions": "- Code 29: Answer \"I = E x R\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 46: Answer \"I = E / R\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 27: Answer \"I = E² x R\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 39: Answer \"I = E² / R\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q5c2f8dcd21",
  "kind": "yes/no",
  "text": "RT @NYTScience: 7 scientifically grounded ways to ruin Jurassic World for your friends by @SciFleur",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qdfd14fccf3",
  "kind": "yes/no",
  "text": "That is, I think, the main goal AND the starting point of a new life. When you overcome the red pill rage and stop caring about women (and understand their nature), then you're free to start a new path.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q42a7ca5815",
  "kind": "yes/no",
  "text": "Request:\nWhat is the smallest number which is one less than twice its reciprocal?\n\nResponse:\nI want to find a number x such that x = 2(1/x) - 1.\nTo make the equation easier to work with, I can multiply both sides by x and get x^2 = 2 - x.\nThis is a quadratic equation, so I can use the quadratic formula to find the possible values of x.\nThe quadratic formula says that x = (-b +/- sqrt(b^2 - 4ac))/2a, where a, b, and c are the coefficients of the quadratic equation ax^2 + bx + c = 0.\nIn this case, a = 1, b = -1, and c = -2, so I can plug these values into the formula and get x = (1 +/- sqrt(1 + 8))/2.\nSimplifying, I get x = (1 +/- 3)/2, which means x = 2 or x = -1.\nThese are the only two possible numbers that satisfy the equation, but I want the smallest one, so I choose x = -1 as my answer.\n# Answer\n\n-1",
  "question": "Is every step and the final result of the response correct, and are all instructions in the request followed?"
 },
 {
  "qid": "q78a69448b8",
  "kind": "yes/no",
  "text": "For the treatment of mildly to moderately active ulcerative colitis: The usual dosage in adults is two 400 mg tablets to be taken three times a day for a total daily dose of 2.4 grams for a duration of 6 weeks.",
  "question": "Which section of a US prescription drug label does this passage come from?\nIs the correct answer \"dosage and administration\"?",
  "definitions": "- dosage and administration: Tells how to dose and give the drug: doses, schedules, titration, dose changes for patient groups, preparation, dilution and administration technique.\n- indications and usage: States the diseases, conditions or patient groups the drug is approved to treat, prevent or diagnose, and any limitations of use.\n- drug/laboratory test interactions: Explains how the drug interferes with laboratory test results (false positives or altered assay values).\n- instructions for use: Step-by-step instructions for the patient on preparing and using the product or its device (injector, pen, inhaler), usually numbered steps.\n- geriatric use: Covers use in older patients (65 and over): whether they respond differently, age-related risks and dose-selection cautions."
 },
 {
  "qid": "q0b95996036",
  "kind": "yes/no",
  "text": "Tweet: @anonymous awesome! FREEEEEEDOM :) be well Chris.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?\nIs the correct answer \"Option G\"?",
  "definitions": "- Option G: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons.\n- Option W: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Option Q: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Option A: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Option Z: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives."
 },
 {
  "qid": "q4504dca795",
  "kind": "yes/no",
  "text": "Statement 1: Vases are usually made of gold\nStatement 2: Vases are usually made of glass",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q585562ac42",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Frank Lamanske\nTable:\n| Frank Lamanske | Frank Lamanske |\n| Batted: Left Threw: Left | Batted: Left Threw: Left |\n| Batted: Left | Threw: Left |\n| MLB debut | MLB debut |\n| Last MLB appearance | Last MLB appearance |\n| MLB statistics | MLB statistics |\n| Win–loss record | 0–0 |\n| Earned run average | 7.36 |\n| Strikeouts | 1 |\n\nClaim: Frank Lamanske, nicknamed \"Franky\", was a left-handed pitcher and batter with an earned run average of 7.36.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q6b20970a47",
  "kind": "yes/no",
  "text": "Statement 1: Animals and plants are very different.\nStatement 2: Animals and plants have no relationship.",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 }
]
