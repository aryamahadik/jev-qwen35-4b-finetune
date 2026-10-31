# T37b blind solver T37b-blind_read-91b414cc-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1_full/s13/answers/T37b-blind_read-91b414cc-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q3527d7f557",
  "kind": "yes/no",
  "text": "Table caption: Real-time LAMP results for DNA extraction from Dracunculus medinensis specimens from a range of host species and countries of origin. – indicates no detection and n/a indicates not applicable.\n| Extract ID | Origin | Host | Dracunculus medinensis assay | Dracunculus medinensis assay |\n| Extract ID | Origin | Host | Time to positive (min:sec) | Annealing temperature (°C) |\n| ChDo-339.2 | Chad | Dog | 10:00 | 81.11 |\n| ChHu-69 | Chad | Human | 12:15 | 80.55 |\n| ChDo-1 | Chad | Dog | 7:45 | 81.34 |\n| ChDo-108.5 | Chad | Dog | 8:15 | 81.30 |\n| ChHu-25 | Chad | Human | 8:45 | 80.86 |\n| ChCa-10a | Chad | Cat | 9:00 | 81.15 |\n| ChDo-189 | Chad | Dog | 10:15 | 81.50 |\n| ChDo-13 | Chad | Dog | 8:00 | 81.40 |\n| ChDo-11 | Chad | Dog | 9:00 | 80.86 |\n| ChDo-47.11 | Chad | Dog | 8:30 | 81.60 |\n| ChHu-100 | Chad | Human | 10:15 | 81.35 |\n| ChHu-24 | Chad | Human | 8:30 | 81.45 |\n| ChDo-1 | Chad | Dog | 7:45 | 81.20 |\n| ChHu-283 | Chad | Human | 10:00 | 82.58 |\n| EtDo-172 | Ethiopia | Dog | 12:15 | 82.78 |\n| EtHu-278 | Ethiopia | Human | 10:30 | 82.63 |\n| EtBa-153 | Ethiopia | Baboon | 10:30 | 82.87 |\n| EtHu-152 | Ethiopia | Human | 10:00 | 82.57 |\n| MaHu-165 | Mali | Human | 9:45 | 82.67 |\n| MaHu-240 | Mali | Human | 10:00 | 82.54 |\n| MaHu-242 | Mali | Human | 23:00 | 82.58 |\n| MaHu-253 | Mali | Human | 11:00 | 82.79 |\n| SsHu-201 | South Sudan | Human | 8:45 | 82.50 |\n| SsHu-256 | South Sudan | Human | 10:15 | 82.36 |\n| SsDo-183 | South Sudan | Dog | 10:30 | 82.48 |\n| Uninfected copepod | n/a | n/a | – | – |\n| Dracunculus insignis | n/a | n/a | – | – |\n\nStatement: Time to positive for Dracunculus medinensis assay will be from 7:45 to 23:00.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5f7affb8dc",
  "kind": "yes/no",
  "text": "do not use this term ❌ (chink)",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qeabfeaa178",
  "kind": "yes/no",
  "text": "Customer: I'd like to find a good restaurant in the center.\nAssistant: We have many options available in Centre. Is there a specific price range or cuisine type you are interested in?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q2de55a4929",
  "kind": "yes/no",
  "text": "👳🏻‍♂️and 💣 = No Correlation !",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q5aa6187357",
  "kind": "yes/no",
  "text": "Situation: She had him wash up and then let him hold the baby.\nAction being judged: Having clean hands before touching a baby.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q1cff352033",
  "kind": "yes/no",
  "text": "Passage:\nA capacitor consists of two conductors separated by a non-conductive region. The non-conductive region is called the dielectric. In simpler terms, the dielectric is just an electrical insulator. Examples of dielectric media are glass, air, paper, vacuum, and even a semiconductor depletion region chemically identical to the conductors. A capacitor is assumed to be self-contained and isolated, with no net electric charge and no influence from any external electric field. The conductors thus hold equal and opposite charges on their facing surfaces, and the dielectric develops an electric field. In SI units, a capacitance of one farad means that one coulomb of charge on each conductor causes a voltage of one volt across the device.\n\nQuestion: What net electric charge are capacitors assumed to have?\nReference answer: no net electric charge\nCandidate answer: no",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q89468af034",
  "kind": "yes/no",
  "text": "Table caption: Computing time per simulation time for t > 1.\n| Instance set | Sequential | Integrated | Split | Timesplit |\n| 50 | 0.07% | 0.17% | 0.24% | 0.61% |\n| 150 | 0.07% | 1.4% | 3.46% | 6.41% |\n| 250 | 0.07% | 3.39% | 9.67% | 14.67% |\n\nStatement: There are 5 Instance set in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd86cff064f",
  "kind": "yes/no",
  "text": "Table caption: Calculated values of Cr eq /Ni eq and solidification modes for coated, outside-uncoated, inside-uncoated and all-uncoated welds. FA denotes Ferritic-Austenitic mode, and A denotes Austenitic mode.\n| Weld/region No. | Cr eq /Ni eq | Solidification mode |\n| Coated/I | 1.92 | FA |\n| Coated/II | 1.65 | FA |\n| Outside-uncoated/I | 0.91 | A |\n| Outside-uncoated/II | 0.88 | A |\n| Inside-uncoated/I | 0.88 | A |\n| Inside-uncoated/II | 0.74 | A |\n| All-uncoated/I | 0.09 | A |\n| All-uncoated/II | 0.08 | A |\n\nStatement: 0.91 Cr eq /Ni eq Weld/region No. is Outside-uncoated/I.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4a853087e1",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "According to the assistant's last message, is \"TOday\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf20ec31384",
  "kind": "yes/no",
  "text": "Occupation: Digital Forensics Analysts\nDuties:\n- Conduct regular design reviews throughout the game development process.\n- Write or supervise the writing of game text and dialogue.\n- Guide design discussions between development teams.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qaa10a4d659",
  "kind": "yes/no",
  "text": "Situation: Marge quickly apologized and retrieved her own cart.\nAction being judged: Attempting to take something before someone who was ahead of you.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa867cc9896",
  "kind": "yes/no",
  "text": "Customer: How about a museum in the east instead?\nAssistant: There are four museums in that area: Cambridge Artworks, Cambridge Museum of Technology, Gallery at Twelve A High Street, and Saint Barnabas Press Gallery.  Do any of those sound interesting?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q867973775a",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. I HAVE CONTACTED SEVERAL FORD DEALERSHIPS ABOUT COMPLETING THE RECALL REPLACEMENT OF MY AIRBAGS BUT HAVE BEEN TOLD REPEATEDLY THAT THEY DO NOT YET HAVE THE PARTS NECESSARY TO DO IT. IT HAS BEEN WELL OVER A YEAR AND IT IS UNACCEPTABLE THAT THE RECALL CANNOT BE COMPLETED WHEN THERE IS A CLEAR SAFETY HAZARD ASSOCIATED WITH THE TAKATA AIRBAGS.",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qb5cee886cb",
  "kind": "yes/no",
  "text": "Statement 1: People drink drinking water\nStatement 2: People drink seawater",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qd8a79f645b",
  "kind": "yes/no",
  "text": "Customer: I am open as far as price range, but I would love a 4 star place.\nAssistant: There doesn't appear to be a 4 star hotel with wifi in the north. Can I interest you in a lower star rating?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qb74ad0676f",
  "kind": "yes/no",
  "text": "Customer: Hello can you tell me what action movies are playing in theaters?\nAgent: Sure which theater would you like\nCustomer: Cinamark in Davenport\nAgent: Would any of these interest you, birds of prey, the photograph, Jumanji, or bad boy’s\nCustomer: Yes when is photograph play\nAgent: Photograph is playing at 7 pm and 8pm tonight\nCustomer: Are their 4 seats available together for the 7 pm showing\nAgent: It looks like that showing is full would you like to try the 8 pm showing\nCustomer: No but could you check to see if it’s playing at rave in moline\nAgent: Yes it looks like there is a 7:30 showing at rave would that work\nCustomer: That could work let me check my planner\nAgent: Ok\nCustomer: Actually that won’t work because I don’t have time to drive across town to get there\nAgent: Ok there is a showing at 8 at rave as well how about that\nCustomer: No that is too late\nAgent: Ok what about tomorrow at 7 there are open seats in both theaters tomorrow\nCustomer: No I can’t go tomorrow.\nAgent: Ok is there another time that you would like me to check\nCustomer: No thanks the movie doesn’t look that good anyway so just forget it\nAgent: Ok is there anything else I can help you with tonight\nCustomer: No thanks\nAgent: Ok have a great afternoon",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q5fce6d9b9d",
  "kind": "yes/no",
  "text": "Second, the President re-asserted the primacy of terrorism as the most important direct threat to the nation, though he derided those who would advocate a strategy of \" invading every country \" harboring terrorists (whoever they may be). This position again plays to the crowd, to Americans who can still remember devastating terrorist attacks on our soil but who have forgotten the horrors of great power competition. He defended the right to pursue terrorists wherever they may be, under certain conditions of course. Among those conditions appears to be the notion of not creating more enemies than we take off the battlefield. How this is measured, I cannot with certainty say. This is clearly a reaction against what the Obama Administration views as the fallout of his predecessor's policies. As a hard and fast rule enforced absent context, this condition might put one at a disadvantage against an opponent without the same sensitivities.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qe0f14f3bec",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. THE CONTACT OWNS A 2005 PONTIAC VIBE. THE CONTACT STATED THAT THE AIR BAG WARNING INDICATOR ILLUMINATED. IT WAS UNKNOWN IF THE VEHICLE WAS DIAGNOSED OR REPAIRED. THE CONTACT RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBER: 15V285000 (AIR BAGS) HOWEVER, THE PART TO DO THE REPAIR WAS UNAVAILABLE. THE CONTACT STATED THAT THE MANUFACTURER EXCEEDED A REASONABLE AMOUNT OF TIME FOR THE RECALL REPAIR. THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 168,000. VIN TOOL CONFIRMS PARTS NOT AVAILABLE. THE CONSUMER STATED THE REPAIR WAS MADE ON JAN 8TH.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q698f784ad3",
  "kind": "yes/no",
  "text": "This wasn't necessarily the clearest or most explicit presentation of the reason and one could do better. Be sure that the conclusions won't change. The quantum fields at space-like separations commute with each other. And this vanishing commutator (or anticommutator in the case of pairs of fermionic operators) is a necessary condition for the independent evolution of fields at space-like separations. This absence of an \"action at a distance\" is required by the special theory of relativity because if such superluminal influences existed, they would be equivalent by switching to a different reference frame to actions affecting the past. That would break causality and allow us logically contradictory \"closed time-like curves\" in a Minkowski spacetime. (One could find a way to kill your grandfather before he had his first sex with your grandmother, you know the story.)",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q457c74a14b",
  "kind": "yes/no",
  "text": "Customer: Yes can I make a reservation for 1 people at 16:15 on wednesday?\nAssistant: I'm sorry, there are no available tables at that time. Would you like me to look for a different restaurant?",
  "question": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "qc9e8331c92",
  "kind": "yes/no",
  "text": "Customer: Would you please help me to buy movie tickets for theatres in Davis,California\nAgent: No problem. Do have a movie in mind?\nCustomer: yes,i have a mind on \"no time time to die\"\nAgent: It looks like nearest theater playing No Time Die is at AMC Mercado 24 in Sacramento, California.\nCustomer: Can please check correctly If there is no showing in Davis,California\nAgent: That’s right. No Time Die is not showing in Davis, California.\nCustomer: Not a problem,What action flims are playing in Davis,California.\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: That is the original film from the 1970s\nAgent: release date for film is October 12, 1979.\nCustomer: Sorry, i am not not buy tickets at this moment because the film choice not available in my local area\nAgent: No problem. Hope talk again soon.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q2f38b2be21",
  "kind": "yes/no",
  "text": "Situation: They did not announce any engagement and said he was only visiting.\nAction being judged: Not sharing all of your personal life with others.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q2c94b3ae21",
  "kind": "yes/no",
  "text": "I saw a monkey at the zoo! 🐒 Like this but blacker",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q3f084e3ab9",
  "kind": "yes/no",
  "text": "Statement 1: Peter doesn't like bathing, so he's very dirty.\nStatement 2: Peter doesn't like bathing, so he's very clean.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q187c30cf5c",
  "kind": "yes/no",
  "text": "Global warming has been described as the greatest threat facing mankind, but the policies designed to address global warming actually pose a much greater threat. The international and domestic policies to ration carbon-based energy would doand are doing little to slow carbon dioxide (CO2) emissions, but would have enormous costs. These costs would fall most heavily on poor people, not only in the United States, but also in the world's poorest nations. The correct approach is not energy rationing, but rather long-term technological transformation and building resiliency in developing societies by increasing their wealth.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qeb26d7f445",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence contradict the claim?",
  "definitions": "- yes: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim.\n- no: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged."
 },
 {
  "qid": "q95787ac675",
  "kind": "yes/no",
  "text": "Table caption: Impact analysis of the joint plans, showing investment cost, reduction of gas consumption, electricity production, reduction of CO2-emission, and payback period per technology.\n|  | Investment cost (€) | Reduction in gas consumption (m3) | Electricity production (kWh) | Reduction in CO2 emission (kg CO2-eq) | Payback period (years) |\n| Solar panels | 6,512,100‬ | – | 6,423,219 | 3,211,609 | 5.3 |\n| All insulation | 81,908,719 | 8,878,861 | – | 17,580,145 | 15.3 |\n| All technologies | 88,420,819 | 8,878,861 | 6,423,219 | 20,791,754 | 12.6 |\n\nStatement: All insulation has a highest value in Payback period (years).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8a18e7a503",
  "kind": "yes/no",
  "text": "One note of caution. Concerns about global climate change are particularly complex as they touch on climate science, economics, societal response to climate change, and other issues. In order to prepare a guide that is accessible to a general audience, some simplification is inevitable. For this reason, references to the technical literature have been provided in the endnotes for those interested in further study.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qab0adeceb1",
  "kind": "yes/no",
  "text": "Look at that stupid 👨🏼‍🔬",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qe7ae292cd8",
  "kind": "yes/no",
  "text": "Situation: So while sitting at his house one day he gets call from his friend.\nAction being judged: Taking calls while at home.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q58f2bbc6a8",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis paper examines short-term birth sequelae of the influenza pandemic of 1918–1920 in the United States using monthly data on births and all-cause deaths for 19 US states in conjunction with data on maternal deaths, stillbirths, and premature births. Notable findings include: 1) a drop in births in the 3 months following peak mortality; 2) a reversion in births to normal levels occurring 5–7 months after peak mortality; and 3) a steep drop in births occurring 9–10 months after peak mortality.\n\nClaim: In the global influenza pandemic of 1918, U.S. birthrates dropped within the initial three months after peak mortality.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qde9769158d",
  "kind": "yes/no",
  "text": "Republicans at the top of the ticket were missing in action; Republican voters returned the favor. Nationally, in the 2008 election, GOP turnout fell by more than 4 percent while Democratic turnout rose by over 9 percent, according to American University's Center for the Study of the American Electoratenot enough to change the final outcome, but perhaps the difference in a razor-thin swing state such as Indiana, where McCain fell short by a mere 26,000 votes, or North Carolina, which Barack Obama carried by 100,000 votes, or less than 1 percent.",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q6849482537",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. THE CONTACT OWNS A 2008 MERCEDES-BENZ C300. THE CONTACT RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBERS: 16V081000 (AIR BAGS) AND16V363000 (AIR BAGS); HOWEVER, THE PARTS TO DO THE REPAIRS WERE UNAVAILABLE. THE CONTACT STATED THAT THE MANUFACTURER EXCEEDED A REASONABLE AMOUNT OF TIME FOR THE RECALL REPAIRS. THE MANUFACTURER WAS MADE AWARE OF THE ISSUE. THE CONTACT HAD NOT EXPERIENCED A FAILURE. VIN TOOL CONFIRMS PARTS NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q96b4a9343e",
  "kind": "yes/no",
  "text": "Customer: I would like to try Jamaican cuisine.\nAssistant: I'm sorry but there doesn't seem to be any Jamaican restaurants available, do you have another food preference you'd like to try?",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7f0f68eb88",
  "kind": "yes/no",
  "text": "Customer: Show me the movies that are out near me\nAgent: Sure. Not a problem. Sonic the hedgehog Call of the wild Onward Harley quinn birds of prey The photograph\nCustomer: What theater is sonic the hedgehog playing at?\nAgent: The theater that Sonic the hedgehog is playing at is the Nitehawk prospect park. Would you like me to get you the times?\nCustomer: Yes. Please do that\nAgent: It is playing February 21st at 10:45pm.\nCustomer: Any time for tomorrow the 22nd?\nAgent: It is playing tomorrow the 22nd at 10am at the Apline movie theater in brooklyn ny.\nCustomer: How much are the ticket prices?\nAgent: The price per person is 12 dollars.\nCustomer: Ok that is great.\nAgent: Do you need help booking tickets?\nCustomer: Yes. I will need 4 tickets. 2 children and 2 adults.\nAgent: Oh you wanted to include children tickets? Are they under 12 years old?\nCustomer: Yes. Both of them are.\nAgent: The total amount is 40 dollar for 4 tickets.\nCustomer: Oh. Thank you so much.\nAgent: You are very welcome. Would you like me to book it for you?\nCustomer: No. I would like To postpone it.\nAgent: Oh. I am sorry to hear that",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc865806327",
  "kind": "yes/no",
  "text": "A paper published today in Nature finds \"Australian tropical cyclone activity lower than at any time over the past 5501,500 years\" and \"we show, on the basis of a new tropical cyclone activity index (CAI), that the present low levels of storm activity on the mid west and northeast coasts of Australia are unprecedented over the past 550 to 1,500 years.\" \"Other studies project a decrease in the frequency of tropical cyclones towards the end of the twenty-first century in the southwest Pacific, southern Indian and Australian regions. Our results, although based on a limited record, suggest that this may be occurring much earlier than expected.\"",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q832be2c053",
  "kind": "yes/no",
  "text": "In the third school, where I find myself, reside the lukewarmers those who argue that carbon dioxide indeed is warming surface temperatures, but that its effect is modest and that we are inadvertently adapting. Our mantra: Its not the heat, its the sensitivity. In other words, most climate projections assume that surface temperature is overly sensitive to forcing from carbon dioxide. Our bible consists of observed temperature trends as CO2 increased in the last several decades.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qf3e694c546",
  "kind": "yes/no",
  "text": "Situation: Rough Play Causes Painful Injury to Loving Family Pet\nAction being judged: Playing rough with pets.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q7eb7c7afb8",
  "kind": "yes/no",
  "text": "Situation: But she didn't want to wake anyone so she just smiled big instead.\nAction being judged: Being asleep in places where others aren't sleeping.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qb28f03ece8",
  "kind": "yes/no",
  "text": "Customer: I need to get 5 tickets for a movie tomorrow.\nAgent: Sure, I can help you with that. What city and state, please?\nCustomer: We're in Hillsdale, but we like to go into Spring Hills for movies.\nAgent: Okay. What movie would you like to see?\nCustomer: Could you give me some information on a movie called Shuttered? It sounded strange.\nAgent: Yes, I can. Shuttered is a horror movie rated R. On Rotten Tomatoes it has a 61% rating. Do you want the story line?\nCustomer: No, thanks. How about Beyond the Storm?\nAgent: Beyond the storm is an action movie rated PG-13. It has an 81% rating with Rotten Tomatoes.\nCustomer: What is it about?\nAgent: It is about a fishing trawler in the North Sea. The captain has to deal with the extreme weather and the fact that there is a traitor on board that causes problems.\nCustomer: Are they both playing at Cinemark Downtown?\nAgent: Beyond the Storm is playing at Cinemark Downtown and Shuttered is playing at AMC Holiday.\nCustomer: Okay. Let me go ahead and get 5 tickets to the movie Beyond the Storm. We'd like a showtime around 6 or 7, if possible.\nAgent: The showtimes close to that are 6:10pm and 8:30pm.\nCustomer: Okay. I think we'd better get the 6:10pm.\nAgent: Okay. Please let me know if this is the correct information. You want 5 tickets to see Beyond the Storm tonight at 6:10 PM at Cinemark Downtown?\nCustomer: Yes, that sounds about right. How does that email thing work?\nAgent: You'll get an email and you can either print the tickets at home or take the confirmation to the movie.\nCustomer: That sounds easy, okay.\nAgent: Your tickets are confirmed and they've been sent to your email address.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q8228794fd9",
  "kind": "yes/no",
  "text": "Complaint narrative: MY WIFE AND I HAD MOVED FROM MILWAUKEE TO SEATTLE IN MARCH 2016. IN APRIL, WE DECIDED TO DRIVE UP TO THE SKAGIT VALLEY 'TULIP FESTIVAL' (NORTH OF THE CITY). WE TOOK MY WIFE'S 2010 SUBARU LEGACY IT WAS A DECENT DAY, BUT NOT WARM ENOUGH TO HAVE THE SUNROOF OPEN. WE DID HAVE THE SHADE OPEN THOUGH AND WERE ENJOYING THE SUN FILTERING IN. ON THE DRIVE UP ON I-5, WE HEARD WHAT SOUNDED LIKE AN EXPLOSION ABOVE US. MY WIFE KEPT HER COMPOSURE, BUT WE HAD TO SLOW DOWN, PULL OVER TO THE RIGHT LANE AND EXIT AS SOON AS WE COULD. WHEN WE STOPPED WE NOTICED A HOLE ABOUT THE SIZE OF A PENNY APPEARING IN THE SUNROOF ABOVE US. THERE WAS SHATTERED GLASS IN THE CUP HOLDERS AND ON THE MIDDLE CONSOLE. WE COULDN'T BELIEVE WHAT HAPPENED - WE WERE DRIVING ON THE FREEWAY, NOTHING WAS ABOVE US AND WE COULDN'T FIND A ROCK OR ANYTHING IN THE CAR. THE AUTO GLASS REPAIR SHOP PUT SOME CLING WRAP ON THE GLASS AND TAPED IT SO WE COULD CONTINUE OUR JOURNEY AND AWAIT INSURANCE. TURNS OUT OUR WI INSURANCE WAS STILL IN AFFECT SO WE ACTUALLY (LUCKILY) HAD IT COVERED UNDER GLASS REPLACEMENT. IT WAS A BIT OF A MESS WORKING WITH INSURANCE, GETTING THE REPLACEMENT GLASS, AND SCHEDULING THE REPAIR WORK, BUT WE'RE JUST THANKFUL WE DIDN'T GET GLASS ON US OR GET IN AN ACCIDENT DUE TO THIS. [XXX] SEATTLE WA **THANKS SO MUCH FOR RAISING THE AWARENESS ON THIS AND HELPING OTHERS. WE APPRECIATE IT AND HOPE THE AUTO COMPANIES OR SAFETY BOARDS DO SOMETHING TO HELP PREVENT THIS IN THE FUTURE!**",
  "question": "Does this vehicle safety complaint report that at least one person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qd16481379e",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2003 CHEVROLET MONTE CARLO. THE CONTACT STATED THAT WHILE PARKED, THE VEHICLE CAUGHT ON FIRE. THE FIRE DEPARTMENT EXTINGUISHED THE FIRE. A FIRE REPORT WAS NOT FILED AND NO INJURIES WERE REPORTED. THE VEHICLE WAS TOWED TO THE CONTACTS RESIDENCE. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE CONTACT MENTIONED THAT SHE RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBER: 15V701000 (ENGINE AND ENGINE COOLING) AFTER THE FAILURE OCCURRED. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 150,000.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q8edb0e5b01",
  "kind": "yes/no",
  "text": "Assistant: Do you want extra toppings?\nCustomer: OK, let's add mushrooms.\nAssistant: I'm sorry, but there is no Pacific Veggie Pizza now. Do you want to change your order?",
  "question": "According to the assistant's last message, is \"Pacific Veggie Pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3208df51e6",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 JEEP PATRIOT. WHILE DRIVING AT AN UNKNOWN SPEED, THE VEHICLE STALLED AND THE SLIP INDICATOR, CHECK ENGINE, AND THROTTLE CONTROL INDICATORS ILLUMINATED. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. THE VEHICLE WAS NOT TAKEN TO A DEALER; HOWEVER, AN INDEPENDENT MECHANIC CAME TO THE CONTACT'S RESIDENCE, RESET THE VEHICLE, AND CHANGED THE OIL. THE CONTACT STATED THAT THE FAILURE RECURRED A WEEK LATER. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND CONFIRMED THAT THE VIN WAS NOT INCLUDED IN NHTSA CAMPAIGN NUMBER: 13V552000 (ENGINE). THE APPROXIMATE FAILURE MILEAGE WAS 67,000.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qca936e6835",
  "kind": "yes/no",
  "text": "But as we suggested earlier in the year , the incautious statements issued by Met Office scientists looked less like the work of scientific enquiry, and more like post-hoc speculation about which way the weather would turn.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qf6bdf6ed24",
  "kind": "yes/no",
  "text": "Of course the food supply p festivalomrdet planned since long time back's one can speculate why arrangrerna chose dark ages year's surprise at the eleventh hour? Maybe they did not want stricter biljettfrsljningen? Or so they would not give mjligheten from restaurants nrheten to arrange catering just outside the area? A few that quickly hrsammade shortages p n other vegetarian sausages were the men who rushed there and stood on line outside the area. They realized that hr was a hack to earn.",
  "question": "Does this paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "q367cf6f4c6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Zuniga was a founding member of the Earth Communications Office (ECO), and has worked with the Natural Resources Defense Council, the Waterkeeper Alliance, and Environment California.\n\nSummary sentence:\nZuniga has been active in environmental issues since the mid-2000s, and was a founding member of the Earth Communications Office.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q15d4529d1d",
  "kind": "yes/no",
  "text": "This might all be harmless fun if it just stayed in peoples minds. But governments are already taking steps to deal with this alleged threat to civilisation, steps which already damage the least well off more than any other.",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q9f1a2eab93",
  "kind": "yes/no",
  "text": "Customer: My girlfriend and I want to go to the movies!\nAgent: Certainly! Is there a city you have in mind?\nCustomer: Yeah, Springs Hills, Kansas.\nAgent: There are two theaters in Springs Hills. The AMC Holiday Theater, and the Cinemark Downtown.\nCustomer: Let's see. Girlfriend wants to go to the Cinemark Downtown. It's her favorite.\nAgent: The Cinemark Theater it is!\nCustomer: What films are currently playing there?\nAgent: Right now BACKCOUNTRY and BEYOND THE STORM are the two films playing there.\nCustomer: Tell me about BEYOND THE STORM, please. Give me the synopsis and Rotten Tomatoes score.\nAgent: BEYOND THE STORM - Action - rated PG-13 - Rotten Tomatoes 81% - Fishing the North Sea gets ugly as Captain John’s crew faces not only severe weather but a traitor on board - directed by James Cameron.\nCustomer: Yuck! I hate James Cameron, that pompous blowhard. Tell me about BACKCOUNTRY, same tidbits as before.\nAgent: BACKCOUNTRY - Documentary (outdoor) - rated G - Rotten Tomatoes 91% - Explore Yosemite in all its glory in this award winning film that delves into the wonders of one of the United State’s most iconic national parks.\nCustomer: Ok, that I can live with. You know why? James Cameron didn't have his dirty hands in the pot. When is it playing today?\nAgent: BACKCOUNTRY has showtimes of 4:10pm - 7:30pm - 10:15pm.\nCustomer: Ok, that's not a lot to pick from but we'll make due. Get me 2 tickets for 7:30PM tonight for BACKCOUNTRY at the Cinemark, please?\nAgent: To be sure, you want 2 tickets at 7:30pm tonight for BACKCOUNTRY at the Cinemark, correct?\nCustomer: Yes. Place my order.\nAgent: I have just made your order!\nCustomer: Sounds good. Please confirm my tickets.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q7783ac9f6b",
  "kind": "yes/no",
  "text": "fuck the chavs and their welfare system 🖕🏽",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 }
]
