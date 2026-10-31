# G5-H blind read T37b-blind_read-fe795327-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1/g5h/answers/T37b-blind_read-fe795327-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q692cc62339",
  "kind": "yes/no",
  "text": "Customer: I would like to try something new, I am looking for an Irish restaurant, preferably in the moderate price range.\nAssistant: I am sorry their are no irish restaurants in my data base, may I help you with something else",
  "question": "In the response the assistant gave, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qc0937f4d26",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CAR HAS BEEN IN AND OUT OF THE DEALERSHIP FOR ALMOST A WEEK OVER THE LAST TWO WEEKS AND THE RECALL HAS NOT BEEN FIXED AND THE DEALERSHIP HAS BEEN UNCOOPERATIVE ABOUT THE REPAIRS.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "qed49a6a323",
  "kind": "yes/no",
  "text": "Cunningham also worked as a staffer for Sheldon Silver, the former longtime speaker of the state assembly, and she's the ex-wife of current attorney general Eric Schneiderman. She advised Christine Quinn in her campaign for mayor and Andrew Cuomo in his gubernatorial campaign, even as some of her colleagues lent their services to more left-wing candidates. Now with the prominent lobbying and consulting firm SKDKnickerbocker, Cunningham has advised Governor Cuomo on his Medicaid Redesign Team, tasked with cutting payments to hospitals.",
  "question": "Is it correct that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qeff13887e6",
  "kind": "yes/no",
  "text": "MOOSE: Dont give me any of that fallacy malarkey. You just do what I tell you and youll get through this.",
  "question": "Does this paragraph set forth the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q28583105c6",
  "kind": "yes/no",
  "text": "Table caption: Data for allele frequency at five microsatellite loci of Siberian sturgeon Acipenser baerii offspring obtained from a gynogenetic female.\n| Locus | Allele (bp) | Females | Unidentified | Males |\n| Afu-68 | 156 | 0.14 | 0.14 | 0.31 |\n|  | 200 | 0.50 | 0.50 | 0.50 |\n|  | 228 | 0.36 | 0.36 | 0.19 |\n| Aox-45 | 145 | 0.50 | 0.50 | 0.50 |\n|  | 249 | 0.50 | 0.50 | 0.50 |\n| Spl-163 | null allele | 0.00 | 0.14 | 0.15 |\n|  | 188 | 0.03 | 0.14 | 0.00 |\n|  | 192 | 0.29 | 0.14 | 0.25 |\n|  | 196 | 0.00 | 0.11 | 0.16 |\n|  | 200 | 0.36 | 0.29 | 0.33 |\n|  | 204 | 0.32 | 0.21 | 0.11 |\n| Spl-104 | 175 | 0.18 | 0.21 | 0.24 |\n|  | 200 | 0.39 | 0.32 | 0.34 |\n|  | 225 | 0.32 | 0.29 | 0.34 |\n|  | 250 | 0.11 | 0.18 | 0.08 |\n| Spl-106 | null allele | 0.14 | 0.14 | 0.22 |\n|  | 150 | 0.07 | 0.07 | 0.00 |\n|  | 241 | 0.36 | 0.50 | 0.44 |\n|  | 247 | 0.43 | 0.29 | 0.34 |\nTable notes: F-females; U-unidentified; M-males.\n\nStatement: The highest Unidentified value for male is 0.77.",
  "question": "Is it the case that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q9736e6b6ce",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nUTHA conducted contact tracing, which linked the students' infections to a spring break trip to Cabo San Lucas, Mexico, during March 14-19. Among 231 persons tested for SARS-CoV-2 in this investigation, 64 (28%) had positive test results, including 60 (33%) of 183 Cabo San Lucas travelers, one of 13 (8%) household contacts of Cabo San Lucas travelers, and three (9%) of 35 community contacts of Cabo San Lucas travelers.\n\nClaim: Through contact tracing initiatives it was found that the novel coronavirus sickened at least 60 students linked to a spring break trip to Mexico.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q80b86bdc42",
  "kind": "yes/no",
  "text": "Customer: I would like to purchase movie tickets for theaters in Davis, California tonight.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I have been thinking of No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: At what time will it be showing?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh no! What action films are playing in Davis, California tonight?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the original Mad Max of 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I am really sorry i forgot i have a lot of work tonight so i will not be purchasing any tickets tonight.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "Is it true that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q3bac0863b2",
  "kind": "yes/no",
  "text": "Passage:\nIn 2014 YouTube said that 300 hours of new videos were uploaded to the site every minute, three times more than one year earlier and that around three quarters of the material comes from outside the U.S. The site has 800 million unique users a month. It is estimated that in 2007 YouTube consumed as much bandwidth as the entire Internet in 2000. According to third-party web analytics providers, Alexa and SimilarWeb, YouTube is the third most visited website in the world, as of June 2015; SimilarWeb also lists YouTube as the top TV and video website globally, attracting more than 15 billion visitors per month.\n\nQuestion: How much content on youtube comes from outside the US?\nReference answer: around three quarters\nCandidate answer: three quarters",
  "question": "Can the candidate answer replace the reference answer, giving at least the same information for this question, without dropping anything important or adding misleading or extra information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q297e1cf6f2",
  "kind": "yes/no",
  "text": "Table caption: Overview of the renewable energy technologies and the selected block types in the Minecraft platform.\n| Energy technology | Block type |\n| Solar panels | Daylight sensor |\n| Wall insulation | Yellow wool |\n| Floor insulation | Orange wool |\n| Double glazing | Glass |\n| Roof insulation | Purple wool |\n\nStatement: There are six renewable energy technologies are given.",
  "question": "Is there support for the statement in the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2838ad80da",
  "kind": "yes/no",
  "text": "Assistant: You got it. What kind of milk do you want for that?\nCustomer: I'd like Whole Milk if that's an option. And no sugar or anything else, just a Venti Latte Macchiato with Whole Milk.\nAssistant: I'm so sorry, but they're out of whole milk. Would you like to try another option? There's almond milk, coconut milk, nonfat milk, 2% milk, and soy milk.",
  "question": "Would it be correct to say that, according to the assistant's last message, \"whole milk\" is not confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "qc2f19ba0c7",
  "kind": "yes/no",
  "text": "Complaint narrative: OCTOBER 9, 2017 I WAS REAR-ENDED, HIT AT 35 MPH. THIS HIT I WAS SITTING. I WAS SIDE SWIPED AT 40- 45 MPH, MOVING AT THIS TIME. I WAS AGAIN REAR-ENDED AT 50- 55 MPH, STOPPED. AND THEN I WAS BACKED INTO, IN THE FRONT END OF MY CAR AT 20-25 MPH. HOW COME NO AIRBAGS GO OFF?",
  "question": "Would it be correct to say that this vehicle safety complaint doesn't report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "q0e4eb3052b",
  "kind": "yes/no",
  "text": "Customer: Hey, how are you?\nAgent: Well, how can I help you?\nCustomer: I would like to see a movie tonight i think\nAgent: sure, is anyone going with you?\nCustomer: just my girlfriend and brother\nAgent: great, what would you like to see?\nCustomer: the Boy 2, or Bad boys would be good\nAgent: Okay, is there any particular theater you would like to go to?\nCustomer: I like Regal or AMC\nAgent: Okay, is there a specific time you would like to go?\nCustomer: I think anywhere from 7-8 would be good\nAgent: okay, one second let me check\nCustomer: sure thing, take your time\nAgent: okay, I am checking for the boy 2 and see no results\nCustomer: shucks, can you check for bad boys then?\nAgent: sure thing, let me see\nCustomer: okay, hopefully they have something....\nAgent: okay, bad news, there is nothing for that either\nCustomer: okay, I guess it is not in the cards for tonight, thank you anyways\nAgent: not a problem, any time!",
  "question": "By the end of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qa97fb9f7bd",
  "kind": "yes/no",
  "text": "Situation: They did not announce any engagement and said he was only visiting.\nAction being judged: Not sharing all of your personal life with others.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf064a3a2af",
  "kind": "yes/no",
  "text": "Passage:\nDefensive Counterair (DCA) is defined as \"all the defensive measures designed to detect, identify, intercept, and destroy or negate enemy forces attempting to penetrate or attack through friendly airspace\" (JP 1-02). A major goal of DCA operations, in concert with OCA operations, is to provide an area from which forces can operate, secure from air and missile threats. The DCA mission comprises both active and passive defense measures. Active defense is \"the employment of limited offensive action and counterattacks to deny a contested area or position to the enemy\" (JP 1-02). It includes both ballistic missile defense and air breathing threat defense, and encompasses point defense, area defense, and high value airborne asset defense. Passive defense is \"measures taken to reduce the probability of and to minimize the effects of damage caused by hostile action without the intention of taking the initiative\" (JP 1-02). It includes detection and warning; chemical, biological, radiological, and nuclear defense; camouflage, concealment, and deception; hardening; reconstitution; dispersion; redundancy; and mobility, counter-measures, and stealth.\n\nQuestion: What is one of the many ways the DCA utilizes passive defense to protect from enemy attacks?\nReference answer: counter-measures\nCandidate answer: detection and warning",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it gives another answer, skips important information, or adds information that misleads or is superfluous?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "qe5009f92ed",
  "kind": "yes/no",
  "text": "Situation: His parents opted to keep him home instead, until he's more mature.\nAction being judged: Doing what you think is best for your children.",
  "question": "Would it be correct to say that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q0c1886e698",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThe lockdown period increases transmission risk in the family and households, whereas isolation and quarantine reduce risks across all types of contacts.\n\nClaim: Lockdown measures alone raised the risk of coronavirus infection within households.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "qcf0cdf62ed",
  "kind": "yes/no",
  "text": "Table caption: Material properties of Scotch-Weld™ AF 163-2K epoxy film adhesive.\n| Tensile modulus | E Adh | 2046 MPa a |\n| Poisson ratio | ν Adh | 0.34 b |\n\nStatement: Poisson ratio has Adh.",
  "question": "Supported by the table, is the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q9815975304",
  "kind": "yes/no",
  "text": "Passage:\nThe quarrel of the Ancients and the Moderns was a literary and artistic quarrel that heated up in the early 1690s and shook the Académie française. The opposing two sides were, the Ancients (Anciens) who constrain choice of subjects to those drawn from the literature of Antiquity and the Moderns (Modernes), who supported the merits of the authors of the century of Louis XIV. Fontenelle quickly followed with his Digression sur les anciens et les modernes (1688), in which he took the Modern side, pressing the argument that modern scholarship allowed modern man to surpass the ancients in knowledge.\n\nQuestion: What was the basis of the quarrel between the Ancients and the moderns?\nReference answer: literary and artistic\nCandidate answer: literary and artistic quarrel",
  "question": "Can the candidate answer be used as a substitute for the reference answer, providing at least the same information for this question, without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q246625ea9f",
  "kind": "yes/no",
  "text": "Customer: Well I guess I'm out of luck, unless there are hotels in adjoining towns I could try.\nAssistant: Sorry, we only work with places in cambridge.",
  "question": "Going by the text, did the assistant's reply include at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q287f541a9c",
  "kind": "yes/no",
  "text": "📸 is not right",
  "question": "In this post, is there hatred?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q774a7f97bc",
  "kind": "yes/no",
  "text": "Customer: I want movie tickets in Davis, California.\nAgent: No problem. Do you have a movie in mind?\nCustomer: No Time To Die sounds good.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: What about in Davis, California though?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Darn it. What is playing in Davis, California then?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the same movie from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I don't want any movie tickets anymore. Thanks anyway.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q053294a536",
  "kind": "yes/no",
  "text": "Complaint narrative: CRANK SHAFT SENSOR MALFUNCTION. MY CAR STOP ON ME WHILE DRIVING ON A CITY STREET. IT SHOOK AND THEN SHUT DOWN. VERY SCARY. I HAD TO GET PUSH OUT OF THE STREET BY POLICE CAUSE I WAS IN THE WAY OF TRAFFIC. SOMEONE ALMOST RAN INTO ME.",
  "question": "Has this vehicle safety complaint reported that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qf7764f48df",
  "kind": "yes/no",
  "text": "Table caption: Summary of worst-case guarantees for the considered multiwinner rules. The definitions of the rules listed in the table are provided in Section . The guarantees are functions of the committee size k . A higher value means a better guarantee, with 1 denoting optimal performance. In most cases we could only find (accurate) estimates instead of the exact values of the guarantees: the “lower” and “upper” values in the table denote that the respective guarantee is between these two bounds. The guarantees for the p -Geometric rule are visualized in (page 10). The column “Pareto” indicates whether the rule satisfies the Pareto efficiency axiom as discussed in Section .\n|  | utilitarian guarantee | utilitarian guarantee | representation guarantee | representation guarantee | Pareto |\n|  | lower | upper | lower | upper | Pareto |\n| AV | 1 | 1 | 1 k | 1 k |  |\n| CC | 1 k | 1 k | 1 | 1 |  |\n| MAV | 0 | 0 | 0 | 0 |  |\n| seq-CC | 1 k | 1 k | 1 − 1 e | 1 − ( 1 − 1 k ) k |  |\n| PAV | 1 2 + k | 2 ⌊ k ⌋ − 1 k | 1 2 | 1 2 + 1 4 k − 2 |  |\n| SLAV | 1 2 + 2 k | 3 2 ⌊ k ⌋ | 3 5 | 2 3 + 1 9 k − 6 |  |\n| p -Geometric | W ( k log ⁡ ( p ) ) k log ⁡ ( p ) + W ( k log ⁡ ( p ) ) | 1 k + 2 W ( k log ⁡ ( p ) ) k log ⁡ ( p ) | p − 1 p | p p + k k + 2 |  |\n| seq-PAV | 1 2 k | 2 ⌊ k ⌋ − 1 k | 1 log ⁡ ( k ) + 2 | 1 2 + 1 4 k − 2 |  |\n| Monroe | 1 k | 1 k | 1 2 | 1 2 + 1 k − 1 |  |\n| Greedy Monroe | 1 k | 1 k | 1 2 | 1 2 + 1 k − 1 |  |\n| seq-Phragmén | 1 5 k + 1 | 2 ⌊ k ⌋ − 1 k | 1 2 | 1 2 + 1 4 k − 2 |  |\n| leximin-Phragmén | 1 k | 1 k | 1 2 | 1 2 + 1 4 k − 2 |  |\n\nStatement: There are 2 kinds of representation guarantees, i.e, lower and upper.",
  "question": "Is the statement refuted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd5e483d038",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nMale, African American, older patients, and those with known COVID-19 exposure were at higher risk of being positive for COVID-19.\n\nClaim: Men of color are no likelier to contract COVID-19 than other populations.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qdd1632e130",
  "kind": "yes/no",
  "text": "Passage:\nA capacitor consists of two conductors separated by a non-conductive region. The non-conductive region is called the dielectric. In simpler terms, the dielectric is just an electrical insulator. Examples of dielectric media are glass, air, paper, vacuum, and even a semiconductor depletion region chemically identical to the conductors. A capacitor is assumed to be self-contained and isolated, with no net electric charge and no influence from any external electric field. The conductors thus hold equal and opposite charges on their facing surfaces, and the dielectric develops an electric field. In SI units, a capacitance of one farad means that one coulomb of charge on each conductor causes a voltage of one volt across the device.\n\nQuestion: What net electric charge are capacitors assumed to have?\nReference answer: no net electric charge\nCandidate answer: no",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer because it is a different answer or leaves out important information or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "qd2f66e7963",
  "kind": "yes/no",
  "text": "Customer: I'd like to book Worth House for 2 people starting Sunday for 4 nights. Can I get the reference number please?\nAssistant: I was able to book the Worth House for you for 2 guests for a total of 4 nights. Your reference number is ZB2FS6W4.",
  "question": "Is it the case that the assistant's reply doesn't confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q486f768d60",
  "kind": "yes/no",
  "text": "Customer: I am open as far as price range, but I would love a 4 star place.\nAssistant: There doesn't appear to be a 4 star hotel with wifi in the north. Can I interest you in a lower star rating?",
  "question": "Was at least a single option that meets everything the customer asked for found by the assistant in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q5ec1548895",
  "kind": "yes/no",
  "text": "Table caption: Summarizing comparison between the hexachloroiridate and hexacyanoferrate redox couple.\n|  | Hexachloroiridate | Hexacyanoferrate |\n| Reaction | IrCl 6 3− ⇌ IrCl 6 2− + e − | Fe(CN) 6 4− ⇌ Fe(CN) 6 3− + e − |\n| Redox potential | +0.8665 V /SHE [ 4 ] | +0.358 V /SHE [ 4 ] |\n| Reduction plateau (Pt) | +0.75 V /SHE to −0.25 V /SHE | +0.2 V /SHE to −0.6 V /SHE |\n| Oxidation plateau (Pt) | +0.95 V /SHE to +1.1 V /SHE | +0.5 V /SHE to +1.1 V /SHE |\n| Diffusion coefficient | 8.38 * 10 −10 m 2 /s | 6.09 * 10 −10 m 2 /s |\n| Solution pH | pH < 5 | Avoid strong acids |\n| Stability in solution: | A few days to weeks [ 18 ] | Refresh daily [ 12 ] |\n| Stability during reduction (RDE) | 39.2% loss after 16 h | 19.5% loss after 16 h |\n| Loss of concentration due to: | Spontaneous reduction Hydroxide formation | Electrode poisoning Photosensitivity |\n| UV-VIS Extinction coefficient | 4.06 mM −1 cm −1 at 488 nm | 1.064 mM −1 cm −1 at 420 nm |\n\nStatement: Hexacyanoferrate has lowest percent of Stability during reduction (RDE).",
  "question": "Does the table support the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qde402862fd",
  "kind": "yes/no",
  "text": "Situation: I pulled out my gun, and they ran off as quickly as they came.\nAction being judged: Pointing at gun at someone unless they are a threat.",
  "question": "Is it true that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa1ad2b03be",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Zuniga was a founding member of the Earth Communications Office (ECO), and has worked with the Natural Resources Defense Council, the Waterkeeper Alliance, and Environment California.\n\nSummary sentence:\nZuniga has been active in environmental issues since the mid-2000s, and was a founding member of the Earth Communications Office.",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1639c096dd",
  "kind": "yes/no",
  "text": "Table caption: Columns data type.\n| No | Column | Count | Data type |\n| 1 | responses_header | 16,659 | object |\n| 2 | responses_rating_grade | 11,222 | float64 |\n| 3 | responses_status | 7559 | object |\n| 4 | responses_message | 16,659 | object |\n| 5 | responses_datetime | 16,659 | datetime64[ns] |\n| 6 | reviewer | 16,659 | object |\n| 7 | comments | 16,659 | int64 |\n| 8 | views | 16,659 | int64 |\n| 9 | id | 16,659 | int64 |\n| 10 | have_email | 16,659 | int64 |\n| 11 | responses_message_length | 16,659 | int64 |\n| 12 | gunning_fog_index | 16,659 | float64 |\n| 13 | binary_score | 16,659 | object |\n\nStatement: Column responses_status has the lowest count of 7559.",
  "question": "Supported by the table, is the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qeb96069a72",
  "kind": "yes/no",
  "text": "Passage:\nHowever, excessive hunting and poachers have also contributed heavily to the endangerment, extirpation and extinction of many animals, such as the quagga, the great auk, Steller's sea cow, the thylacine, the bluebuck, the Arabian oryx, the Caspian and Javan tigers, the markhor, the Sumatran rhinoceros, the bison, the North American cougar, the Altai argali sheep, the Asian elephant and many more, primarily for commercial sale or sport. All these animals have been hunted to endangerment or extinction.\n\nQuestion: How have the North American cougar and Asian elephant been hunted?\nReference answer: to endangerment or extinction\nCandidate answer: commercial sale or sport",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a distinct answer, excludes important information, or introduces misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "qcabc58abd6",
  "kind": "yes/no",
  "text": "Jawbox\nJawbox was an American alternative rock band from Washington, D.C., United States. Its original members were J. Robbins (vocals, guitar), Kim Coletta (bass guitar) and Adam Wade (drums). Bill Barbot (vocals, guitar) and Zach Barocas (drums) later joined the group, with Barocas replacing Wade.\n\nKasabian\nKasabian ( ) are an English rock band formed in Leicester in 1997. The band's original members consisted of vocalist Tom Meighan, guitarist and vocalist Sergio Pizzorno, guitarist Chris Karloff, and bassist Chris Edwards. The band's line-up was completed by drummer Ian Matthews in 2004 after a string of session drummers. Karloff left the band in 2006 and founded a new band called Black Onassis. Jay Mehler joined as touring lead guitarist in 2006. Mehler left the band for Liam Gallagher's Beady Eye in 2013, to be replaced by Tim Carter. In 2010 and 2014, Kasabian won the Q Awards for 'Best Act in the World Today', while they were also named \"Best Live Act\" at the 2014 Q Awards and the 2007 NME Awards. The band's music is often described as \"indie rock\", but Pizzorno has said he \"hates indie bands\" and does not feel Kasabian fit into that category.",
  "question": "Is it right to say that Kasabian and Jawbox are not both from England?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "qca32f95a8d",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 JEEP PATRIOT. WHILE DRIVING AT AN UNKNOWN SPEED, THE VEHICLE STALLED AND THE SLIP INDICATOR, CHECK ENGINE, AND THROTTLE CONTROL INDICATORS ILLUMINATED. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. THE VEHICLE WAS NOT TAKEN TO A DEALER; HOWEVER, AN INDEPENDENT MECHANIC CAME TO THE CONTACT'S RESIDENCE, RESET THE VEHICLE, AND CHANGED THE OIL. THE CONTACT STATED THAT THE FAILURE RECURRED A WEEK LATER. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND CONFIRMED THAT THE VIN WAS NOT INCLUDED IN NHTSA CAMPAIGN NUMBER: 13V552000 (ENGINE). THE APPROXIMATE FAILURE MILEAGE WAS 67,000.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q08bfec3481",
  "kind": "yes/no",
  "text": "Statement 1: His father got angry because he failed the math exam\nStatement 2: His father got excited because he failed the math exam",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q26f1b44495",
  "kind": "yes/no",
  "text": "Passage:\nClay models of ducks found in China dating back to 4000 BC may indicate the domestication of ducks took place there during the Yangshao culture. Even if this is not the case, domestication of the duck took place in the Far East at least 1500 years earlier than in the West. Lucius Columella, writing in the first century BC, advised those who sought to rear ducks to collect wildfowl eggs and put them under a broody hen, because when raised in this way, the ducks \"lay aside their wild nature and without hesitation breed when shut up in the bird pen\". Despite this, ducks did not appear in agricultural texts in Western Europe until about 810 AD, when they began to be mentioned alongside geese, chickens, and peafowl as being used for rental payments made by tenants to landowners.\n\nQuestion: How long have ducks possibly been in domesticated domicile with humans?\nReference answer: Clay models of ducks found in China dating back to 4000 BC may indicate the domestication of ducks took place there during the Yangshao culture\nCandidate answer: 1500 years",
  "question": "Can the candidate answer replace the reference answer, giving at least the same information for this question, without dropping anything important or adding misleading or extra information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q1f8b560ce4",
  "kind": "yes/no",
  "text": "Situation: But she didn't want to wake anyone so she just smiled big instead.\nAction being judged: Being asleep in places where others aren't sleeping.",
  "question": "Is the action being judged bad according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qcf11658591",
  "kind": "yes/no",
  "text": "immigrants can live here, work here so should 🗳️ thats not too much imo",
  "question": "Hateful, is this post?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qbb4b98f75b",
  "kind": "yes/no",
  "text": "Customer: I just told you! sunday! Now please go on and book and send me the reference number\nAssistant: It seems that I can not reserve that at the moment. Would you like me to try a different restaurant?",
  "question": "Is the booking the customer asked for confirmed as actually made in the assistant's reply?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qb662695fa7",
  "kind": "yes/no",
  "text": "Table caption: Calculated values of Cr eq /Ni eq and solidification modes for coated, outside-uncoated, inside-uncoated and all-uncoated welds. FA denotes Ferritic-Austenitic mode, and A denotes Austenitic mode.\n| Weld/region No. | Cr eq /Ni eq | Solidification mode |\n| Coated/I | 1.92 | FA |\n| Coated/II | 1.65 | FA |\n| Outside-uncoated/I | 0.91 | A |\n| Outside-uncoated/II | 0.88 | A |\n| Inside-uncoated/I | 0.88 | A |\n| Inside-uncoated/II | 0.74 | A |\n| All-uncoated/I | 0.09 | A |\n| All-uncoated/II | 0.08 | A |\n\nStatement: 0.91 Cr eq /Ni eq Weld/region No. is Outside-uncoated/I.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q695ddf81eb",
  "kind": "yes/no",
  "text": "Table caption: Enumeration of strength and ductility parameters, including 0.2% proof stress ( σ 0.2 ), ultimate tensile strength ( σ B ), true fracture stress ( σ F ), uniform elongation ( ε u ), strain-to-failure ( ε F ), local elongation associated with necking (post-uniform elongation) ( ε L ) and reduction in area ( φ ), in specimens with diverse C H concentrations, tested at CHS = 1.5 × 10 −3 mm/s.\n| Hydrogen-chargingpressure (MPa) | C H (ppm) | C H (ppm) | σ 0.2 (MPa) | σ B (MPa) | σ F (MPa) | ε u | ε F | ε L | φ (%) |\n| Hydrogen-chargingpressure (MPa) | mass | at. | σ 0.2 (MPa) | σ B (MPa) | σ F (MPa) | ε u | ε F | ε L | φ (%) |\n| Non-charged | 4.7 | 250 | 233 | 530 | 1,213 | 0.375 | 0.577 | 0.202 | 86.3 |\n| 0.7 | 8.4 | 460 | 230 | 534 | 1,200 | 0.383 | 0.587 | 0.204 | 84.9 |\n| 11 | 40.0 | 2,190 | 248 | 545 | 1,368 | 0.393 | 0.597 | 0.204 | 84.2 |\n| 100 | 133 | 7,280 | 287 | 575 | 1,799 | 0.443 | 0.641 | 0.198 | 79.8 |\n\nStatement: The table CH has 2 categories such as mass and at.",
  "question": "Is it true that the statement is not supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qde22a10338",
  "kind": "yes/no",
  "text": "Customer: Hey\nAgent: Hi, do you need something?\nCustomer: I wanted to go see a movie?\nAgent: Great. What movie would you like to see?\nCustomer: Call of the Wild\nAgent: Alright, it looks like Call of the Wild is playing at 411 Twin Drive In and Boaz 9 Cinema, which theater would you like to go to.\nCustomer: Whichever one is the shorter drive.\nAgent: Boaz 9 Cinema is closer to you.\nCustomer: Ok, that's it then.\nAgent: How many tickets would you like?\nCustomer: 2\nAgent: Would you like to go to the 7:30 PM or 9:50 PM showing?\nCustomer: 7:30 PM\nAgent: Alright, then to confirm, you would like 2 tickets to see Call of the Wild at 7:30 PM.\nCustomer: Wait, My girlfriend just told me she would rather see The Invisible Man.\nAgent: The Invisible Man is playing at AmStar Oxford at 7:00 PM, would that work for you?\nCustomer: Yes\nAgent: Ok, then to confirm, you would like 2 tickets to see The Invisible Man at AmStar Oxford at 7:00 PM.\nCustomer: Yes\nAgent: Your tickets have been booked.",
  "question": "Has the customer actually bought movie tickets by the time this conversation finishes?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qdc0d058622",
  "kind": "yes/no",
  "text": "Occupation: Painting, Coating, and Decorating Workers\nDuties:\n- Write or modify design specifications such as the metal contents and weights of items.\n- Anneal precious metal objects such as coffeepots, tea sets, and trays in gas ovens for prescribed times to soften metal for reworking.\n- Lay out designs on metal stock, and cut along markings to fabricate pieces used to cast metal molds.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q9b2257045d",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q0eece49c5c",
  "kind": "yes/no",
  "text": "BLM stands for 🦍..right?!",
  "question": "Does this post count as hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q10536b7ab5",
  "kind": "yes/no",
  "text": "In response to intense questioning from Rep. Mike Pompeo, Kansas Republican, during a House Energy and Commerce Committee hearing on Sept. 18, EPA Administrator Gina McCarthy admitted that the new regulations are unlikely to have measurable impact on world climate. She then explained the real reasons for the rules: ?What we are attempting to do is put together a comprehensive climate plan across the administration that positions the U.S. for leadership on this issue and that will prompt and leverage international discussions and actions.?",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q5b7a3bbbdb",
  "kind": "yes/no",
  "text": "Situation: Slide Phone User Is Irritated by the Pressure to Upgrade\nAction being judged: Keeping using something that still works.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q6081fc7525",
  "kind": "yes/no",
  "text": "Passage:\nThe 1916 Zoning Resolution required setbacks in new buildings, and restricted towers to a percentage of the lot size, to allow sunlight to reach the streets below. The Art Deco style of the Chrysler Building (1930) and Empire State Building (1931), with their tapered tops and steel spires, reflected the zoning requirements. The buildings have distinctive ornamentation, such as the eagles at the corners of the 61st floor on the Chrysler Building, and are considered some of the finest examples of the Art Deco style. A highly influential example of the international style in the United States is the Seagram Building (1957), distinctive for its façade using visible bronze-toned I-beams to evoke the building's structure. The Condé Nast Building (2000) is a prominent example of green design in American skyscrapers and has received an award from the American Institute of Architects as well as AIA New York State for its design.\n\nQuestion: What floor of the Chrysler Building has sculptures of eagles at its corners?\nReference answer: 61st\nCandidate answer: 61st floor",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a distinct answer, excludes important information, or introduces misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q06bde12d28",
  "kind": "yes/no",
  "text": "Occupation: Ophthalmologists, Except Pediatric\nDuties:\n- Design or provide music therapy experiences to address client needs, such as using music for self-care, adjusting to life changes, improving cognitive functioning, raising self-esteem, communicating, or controlling impulses.\n- Plan or structure music therapy sessions to achieve appropriate transitions, pacing, sequencing, energy level, or intensity in accordance with treatment plans.\n- Adapt existing or develop new music therapy assessment instruments or procedures to meet an individual client's needs.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qbe86f6acc1",
  "kind": "yes/no",
  "text": "Passage:\nMaternal factors also play a role in the body’s immune response. At birth, most of the immunoglobulin present is maternal IgG. Because IgM, IgD, IgE and IgA don’t cross the placenta, they are almost undetectable at birth. Some IgA is provided by breast milk. These passively-acquired antibodies can protect the newborn for up to 18 months, but their response is usually short-lived and of low affinity. These antibodies can also produce a negative response. If a child is exposed to the antibody for a particular antigen before being exposed to the antigen itself then the child will produce a dampened response. Passively acquired maternal antibodies can suppress the antibody response to active immunization. Similarly the response of T-cells to vaccination differs in children compared to adults, and vaccines that induce Th1 responses in adults do not readily elicit these same responses in neonates. Between six to nine months after birth, a child’s immune system begins to respond more strongly to glycoproteins, but there is usually no marked improvement in their response to polysaccharides until they are at least one year old. This can be the reason for distinct time frames found in vaccination schedules.\n\nQuestion: Newborns can acquire antibodies from the mother through what means?\nReference answer: breast milk\nCandidate answer: passively",
  "question": "Can the reference answer be replaced by the candidate answer, with the candidate conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 }
]
