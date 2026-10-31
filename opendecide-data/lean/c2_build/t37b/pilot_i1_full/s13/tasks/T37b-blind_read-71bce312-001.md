# T37b blind solver T37b-blind_read-71bce312-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1_full/s13/answers/T37b-blind_read-71bce312-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q4086c606d0",
  "kind": "yes/no",
  "text": "Table caption: Description of columns in ASCII text table.\n| Column Name | Description |\n| System | Multibeam echosounder system |\n| Date | Date of survey, yyyymmdd. |\n| Time | Time of survey (UTC), hhmmss. |\n| Easting | Easting Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Northing | Northing Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Depth | Corrected and processed depth, m. |\n| Latitude | Geographical latitude, DD;MM.mm, WGS1984. |\n| Longitude | Geographical longitude, DD;MM.mm, WGS1984. |\n\nStatement: ASCII text table has three categories- Column Name Ratio and Description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q48399aa8ba",
  "kind": "yes/no",
  "text": "Passage:\nHellenistic military equipment was generally characterized by an increase in size. Hellenistic-era warships grew from the trireme to include more banks of oars and larger numbers of rowers and soldiers as in the Quadrireme and Quinquereme. The Ptolemaic Tessarakonteres was the largest ship constructed in Antiquity. New siege engines were developed during this period. An unknown engineer developed the torsion-spring catapult (ca. 360) and Dionysios of Alexandria designed a repeating ballista, the Polybolos. Preserved examples of ball projectiles range from 4.4 kg to 78 kg (or over 170 lbs). Demetrius Poliorcetes was notorious for the large siege engines employed in his campaigns, especially during the 12-month siege of Rhodes when he had Epimachos of Athens build a massive 160 ton siege tower named Helepolis, filled with artillery.\n\nQuestion: What type of weapon is the Polybolos?\nReference answer: ballista\nCandidate answer: repeating ballista",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information without leaving out anything important or adding misleading or superfluous information, for this question?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q7f5960f1fc",
  "kind": "yes/no",
  "text": "Customer: I’ll like to buy a movie tickets for theaters in davis,california.\nAgent: No problem. Do you have a movie in mind?\nCustomer: no time to die hard\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: is there none going at davis ,california?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: thats sad,what movies are playing in davis,california?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: is that the original film from 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: i wont be buying the ticket at the moment due to film choice not being available in my local city\nAgent: No problem. Hope to talk to you again soon.",
  "question": "Is it accurate to say that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qa7bcd50075",
  "kind": "yes/no",
  "text": "Customer: leaves at 1900hrs, arrives on sunday and booked fir one person.get me the reference number too\nAssistant: Booking was successful, the total fee is 10.1 GBP payable at the station .\nReference number is : 70MPLUW8.",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "qe05a8bfc84",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nWe observed the highest viral load in throat swabs at the time of symptom onset, and inferred that infectiousness peaked on or before symptom onset.\n\nClaim: The infectiousness of SARS-CoV-2 is steady over the course of the Covid-19 symptoms.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q9eea3d907f",
  "kind": "yes/no",
  "text": "Table caption: Calculated values of Cr eq /Ni eq and solidification modes for coated, outside-uncoated, inside-uncoated and all-uncoated welds. FA denotes Ferritic-Austenitic mode, and A denotes Austenitic mode.\n| Weld/region No. | Cr eq /Ni eq | Solidification mode |\n| Coated/I | 1.92 | FA |\n| Coated/II | 1.65 | FA |\n| Outside-uncoated/I | 0.91 | A |\n| Outside-uncoated/II | 0.88 | A |\n| Inside-uncoated/I | 0.88 | A |\n| Inside-uncoated/II | 0.74 | A |\n| All-uncoated/I | 0.09 | A |\n| All-uncoated/II | 0.08 | A |\n\nStatement: 0.91 Cr eq /Ni eq Weld/region No. is Outside-uncoated/I.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7b07257952",
  "kind": "yes/no",
  "text": "Passage:\nAccording to a study by the China Earthquake Administration (CEA), the earthquake occurred along the Longmenshan fault, a thrust structure along the border of the Indo-Australian Plate and Eurasian Plate. Seismic activities concentrated on its mid-fracture (known as Yingxiu-Beichuan fracture). The rupture lasted close to 120 sec, with the majority of energy released in the first 80 sec. Starting from Wenchuan, the rupture propagated at an average speed of 3.1 kilometers per second 49° toward north east, rupturing a total of about 300 km. Maximum displacement amounted to 9 meters. The focus was deeper than 10 km.\n\nQuestion: How long did the rupture last?\nReference answer: 120 sec\nCandidate answer: close to 120 sec",
  "question": "Does the candidate answer count as an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "qce3316a1c3",
  "kind": "yes/no",
  "text": "do not use this term ❌ (chink)",
  "question": "Does this post count as hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q589bff795e",
  "kind": "yes/no",
  "text": "Situation: But she didn't want to wake anyone so she just smiled big instead.\nAction being judged: Being asleep in places where others aren't sleeping.",
  "question": "Is the action being judged bad according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qef6861a2b7",
  "kind": "yes/no",
  "text": "Customer: Hello can you tell me what action movies are playing in theaters?\nAgent: Sure which theater would you like\nCustomer: Cinamark in Davenport\nAgent: Would any of these interest you, birds of prey, the photograph, Jumanji, or bad boy’s\nCustomer: Yes when is photograph play\nAgent: Photograph is playing at 7 pm and 8pm tonight\nCustomer: Are their 4 seats available together for the 7 pm showing\nAgent: It looks like that showing is full would you like to try the 8 pm showing\nCustomer: No but could you check to see if it’s playing at rave in moline\nAgent: Yes it looks like there is a 7:30 showing at rave would that work\nCustomer: That could work let me check my planner\nAgent: Ok\nCustomer: Actually that won’t work because I don’t have time to drive across town to get there\nAgent: Ok there is a showing at 8 at rave as well how about that\nCustomer: No that is too late\nAgent: Ok what about tomorrow at 7 there are open seats in both theaters tomorrow\nCustomer: No I can’t go tomorrow.\nAgent: Ok is there another time that you would like me to check\nCustomer: No thanks the movie doesn’t look that good anyway so just forget it\nAgent: Ok is there anything else I can help you with tonight\nCustomer: No thanks\nAgent: Ok have a great afternoon",
  "question": "By the end of this dialogue, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q927f5e7cd0",
  "kind": "yes/no",
  "text": "This wasn't necessarily the clearest or most explicit presentation of the reason and one could do better. Be sure that the conclusions won't change. The quantum fields at space-like separations commute with each other. And this vanishing commutator (or anticommutator in the case of pairs of fermionic operators) is a necessary condition for the independent evolution of fields at space-like separations. This absence of an \"action at a distance\" is required by the special theory of relativity because if such superluminal influences existed, they would be equivalent by switching to a different reference frame to actions affecting the past. That would break causality and allow us logically contradictory \"closed time-like curves\" in a Minkowski spacetime. (One could find a way to kill your grandfather before he had his first sex with your grandmother, you know the story.)",
  "question": "Does this paragraph put forward the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q8d420468d5",
  "kind": "yes/no",
  "text": "Second, the President re-asserted the primacy of terrorism as the most important direct threat to the nation, though he derided those who would advocate a strategy of \" invading every country \" harboring terrorists (whoever they may be). This position again plays to the crowd, to Americans who can still remember devastating terrorist attacks on our soil but who have forgotten the horrors of great power competition. He defended the right to pursue terrorists wherever they may be, under certain conditions of course. Among those conditions appears to be the notion of not creating more enemies than we take off the battlefield. How this is measured, I cannot with certainty say. This is clearly a reaction against what the Obama Administration views as the fallout of his predecessor's policies. As a hard and fast rule enforced absent context, this condition might put one at a disadvantage against an opponent without the same sensitivities.",
  "question": "Does this paragraph make a claim about climate, namely the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qf28648935f",
  "kind": "yes/no",
  "text": "Passage:\nIn a response to Livingstone, Theodore Dobzhansky argued that when talking about race one must be attentive to how the term is being used: \"I agree with Dr. Livingstone that if races have to be 'discrete units,' then there are no races, and if 'race' is used as an 'explanation' of the human variability, rather than vice versa, then the explanation is invalid.\" He further argued that one could use the term race if one distinguished between \"race differences\" and \"the race concept.\" The former refers to any distinction in gene frequencies between populations; the latter is \"a matter of judgment.\" He further observed that even when there is clinal variation, \"Race differences are objectively ascertainable biological phenomena… but it does not follow that racially distinct populations must be given racial (or subspecific) labels.\" In short, Livingstone and Dobzhansky agree that there are genetic differences among human beings; they also agree that the use of the race concept to classify people, and how the race concept is used, is a matter of social convention. They differ on whether the race concept remains a meaningful and useful social convention.\n\nQuestion: While race difference possible to easily see, they need not be given what?\nReference answer: labels\nCandidate answer: racial (or subspecific) labels",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information without leaving out anything important or adding misleading or superfluous information, for this question?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q5ea4cf240c",
  "kind": "yes/no",
  "text": "Situation: I intentionally gave my sibling hepatitis\nAction being judged: Bringing family members around when they are really sick.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe5404bf934",
  "kind": "yes/no",
  "text": "Assistant: Okay, I will get on that immediately.\nCustomer: Thank you Renee.\nAssistant: Hello, Mr. John Doe, I called in your order, but they don't have any italian sausage, but they do have beef sausage.",
  "question": "Does the assistant's final message say \"italian sausage\" is confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q045a9e672a",
  "kind": "yes/no",
  "text": "Customer: I am open as far as price range, but I would love a 4 star place.\nAssistant: There doesn't appear to be a 4 star hotel with wifi in the north. Can I interest you in a lower star rating?",
  "question": "Was at least a single option that meets everything the customer asked for found by the assistant in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q7302591aa2",
  "kind": "yes/no",
  "text": "One note of caution. Concerns about global climate change are particularly complex as they touch on climate science, economics, societal response to climate change, and other issues. In order to prepare a guide that is accessible to a general audience, some simplification is inevitable. For this reason, references to the technical literature have been provided in the endnotes for those interested in further study.",
  "question": "Does this block of text make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qf224c97c2b",
  "kind": "yes/no",
  "text": "Complaint narrative: MY WIFE AND I HAD MOVED FROM MILWAUKEE TO SEATTLE IN MARCH 2016. IN APRIL, WE DECIDED TO DRIVE UP TO THE SKAGIT VALLEY 'TULIP FESTIVAL' (NORTH OF THE CITY). WE TOOK MY WIFE'S 2010 SUBARU LEGACY IT WAS A DECENT DAY, BUT NOT WARM ENOUGH TO HAVE THE SUNROOF OPEN. WE DID HAVE THE SHADE OPEN THOUGH AND WERE ENJOYING THE SUN FILTERING IN. ON THE DRIVE UP ON I-5, WE HEARD WHAT SOUNDED LIKE AN EXPLOSION ABOVE US. MY WIFE KEPT HER COMPOSURE, BUT WE HAD TO SLOW DOWN, PULL OVER TO THE RIGHT LANE AND EXIT AS SOON AS WE COULD. WHEN WE STOPPED WE NOTICED A HOLE ABOUT THE SIZE OF A PENNY APPEARING IN THE SUNROOF ABOVE US. THERE WAS SHATTERED GLASS IN THE CUP HOLDERS AND ON THE MIDDLE CONSOLE. WE COULDN'T BELIEVE WHAT HAPPENED - WE WERE DRIVING ON THE FREEWAY, NOTHING WAS ABOVE US AND WE COULDN'T FIND A ROCK OR ANYTHING IN THE CAR. THE AUTO GLASS REPAIR SHOP PUT SOME CLING WRAP ON THE GLASS AND TAPED IT SO WE COULD CONTINUE OUR JOURNEY AND AWAIT INSURANCE. TURNS OUT OUR WI INSURANCE WAS STILL IN AFFECT SO WE ACTUALLY (LUCKILY) HAD IT COVERED UNDER GLASS REPLACEMENT. IT WAS A BIT OF A MESS WORKING WITH INSURANCE, GETTING THE REPLACEMENT GLASS, AND SCHEDULING THE REPAIR WORK, BUT WE'RE JUST THANKFUL WE DIDN'T GET GLASS ON US OR GET IN AN ACCIDENT DUE TO THIS. [XXX] SEATTLE WA **THANKS SO MUCH FOR RAISING THE AWARENESS ON THIS AND HELPING OTHERS. WE APPRECIATE IT AND HOPE THE AUTO COMPANIES OR SAFETY BOARDS DO SOMETHING TO HELP PREVENT THIS IN THE FUTURE!**",
  "question": "Does this vehicle safety complaint state that at least a single individual was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qb75419fdd1",
  "kind": "yes/no",
  "text": "Statement 1: Peter doesn't like bathing, so he's very dirty.\nStatement 2: Peter doesn't like bathing, so he's very clean.",
  "question": "Is it correct that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q2ba63d7d1e",
  "kind": "yes/no",
  "text": "Customer: How about a museum in the east instead?\nAssistant: There are four museums in that area: Cambridge Artworks, Cambridge Museum of Technology, Gallery at Twelve A High Street, and Saint Barnabas Press Gallery.  Do any of those sound interesting?",
  "question": "Did the assistant, in its reply, find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q718e7cec2a",
  "kind": "yes/no",
  "text": "Customer: I would like to try Jamaican cuisine.\nAssistant: I'm sorry but there doesn't seem to be any Jamaican restaurants available, do you have another food preference you'd like to try?",
  "question": "In the response the assistant gave, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q821f02d86b",
  "kind": "yes/no",
  "text": "Passage:\nEven with the five largest cities in Sichuan suffering only minor damage from the quake, some estimates of the economic loss run higher than US$75 billion, making the earthquake one of the costliest natural disasters in Chinese history.\n\nQuestion: Whose is this one of the costliest disasters in history of?\nReference answer: Chinese history\nCandidate answer: Chinese",
  "question": "Can the candidate answer replace the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q03a417f944",
  "kind": "yes/no",
  "text": "Customer: Show me the movies that are out near me\nAgent: Sure. Not a problem. Sonic the hedgehog Call of the wild Onward Harley quinn birds of prey The photograph\nCustomer: What theater is sonic the hedgehog playing at?\nAgent: The theater that Sonic the hedgehog is playing at is the Nitehawk prospect park. Would you like me to get you the times?\nCustomer: Yes. Please do that\nAgent: It is playing February 21st at 10:45pm.\nCustomer: Any time for tomorrow the 22nd?\nAgent: It is playing tomorrow the 22nd at 10am at the Apline movie theater in brooklyn ny.\nCustomer: How much are the ticket prices?\nAgent: The price per person is 12 dollars.\nCustomer: Ok that is great.\nAgent: Do you need help booking tickets?\nCustomer: Yes. I will need 4 tickets. 2 children and 2 adults.\nAgent: Oh you wanted to include children tickets? Are they under 12 years old?\nCustomer: Yes. Both of them are.\nAgent: The total amount is 40 dollar for 4 tickets.\nCustomer: Oh. Thank you so much.\nAgent: You are very welcome. Would you like me to book it for you?\nCustomer: No. I would like To postpone it.\nAgent: Oh. I am sorry to hear that",
  "question": "By the conclusion of this conversation, has the customer actually purchased movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qc56a959dd0",
  "kind": "yes/no",
  "text": "Look at that stupid 👨🏼‍🔬",
  "question": "Is this post filled with hate?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qeaea1b1cd6",
  "kind": "yes/no",
  "text": "Passage:\nThe 1916 Zoning Resolution required setbacks in new buildings, and restricted towers to a percentage of the lot size, to allow sunlight to reach the streets below. The Art Deco style of the Chrysler Building (1930) and Empire State Building (1931), with their tapered tops and steel spires, reflected the zoning requirements. The buildings have distinctive ornamentation, such as the eagles at the corners of the 61st floor on the Chrysler Building, and are considered some of the finest examples of the Art Deco style. A highly influential example of the international style in the United States is the Seagram Building (1957), distinctive for its façade using visible bronze-toned I-beams to evoke the building's structure. The Condé Nast Building (2000) is a prominent example of green design in American skyscrapers and has received an award from the American Institute of Architects as well as AIA New York State for its design.\n\nQuestion: What floor of the Chrysler Building has sculptures of eagles at its corners?\nReference answer: 61st\nCandidate answer: 61st floor",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a distinct answer, excludes important information, or introduces misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "qa5f6ebd7c4",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. THE CONTACT OWNS A 2005 PONTIAC VIBE. THE CONTACT STATED THAT THE AIR BAG WARNING INDICATOR ILLUMINATED. IT WAS UNKNOWN IF THE VEHICLE WAS DIAGNOSED OR REPAIRED. THE CONTACT RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBER: 15V285000 (AIR BAGS) HOWEVER, THE PART TO DO THE REPAIR WAS UNAVAILABLE. THE CONTACT STATED THAT THE MANUFACTURER EXCEEDED A REASONABLE AMOUNT OF TIME FOR THE RECALL REPAIR. THE MANUFACTURER WAS NOT MADE AWARE OF THE FAILURE. THE FAILURE MILEAGE WAS APPROXIMATELY 168,000. VIN TOOL CONFIRMS PARTS NOT AVAILABLE. THE CONSUMER STATED THE REPAIR WAS MADE ON JAN 8TH.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q9ff4398528",
  "kind": "yes/no",
  "text": "I saw a monkey at the zoo! 🐒 Like this but blacker",
  "question": "Based on the text, is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q626cdc54f9",
  "kind": "yes/no",
  "text": "In the third school, where I find myself, reside the lukewarmers those who argue that carbon dioxide indeed is warming surface temperatures, but that its effect is modest and that we are inadvertently adapting. Our mantra: Its not the heat, its the sensitivity. In other words, most climate projections assume that surface temperature is overly sensitive to forcing from carbon dioxide. Our bible consists of observed temperature trends as CO2 increased in the last several decades.",
  "question": "Does the paragraph make the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qf7bd200956",
  "kind": "yes/no",
  "text": "Situation: Rough Play Causes Painful Injury to Loving Family Pet\nAction being judged: Playing rough with pets.",
  "question": "Would it be correct to say that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q95503c3ebd",
  "kind": "yes/no",
  "text": "Assistant: would you like anything else?\nCustomer: no, that is all I wanted.\nAssistant: ok, I have placed an the order for the venti whole milk caffe mocha at starbucks down the street",
  "question": "Going by the text, is \"whole milk\" confirmed for the customer's coffee order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q332c5f3cf9",
  "kind": "yes/no",
  "text": "This might all be harmless fun if it just stayed in peoples minds. But governments are already taking steps to deal with this alleged threat to civilisation, steps which already damage the least well off more than any other.",
  "question": "Does this paragraph fail to make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "q8c07c1ba5d",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. THE CONTACT OWNS A 2008 MERCEDES-BENZ C300. THE CONTACT RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBERS: 16V081000 (AIR BAGS) AND16V363000 (AIR BAGS); HOWEVER, THE PARTS TO DO THE REPAIRS WERE UNAVAILABLE. THE CONTACT STATED THAT THE MANUFACTURER EXCEEDED A REASONABLE AMOUNT OF TIME FOR THE RECALL REPAIRS. THE MANUFACTURER WAS MADE AWARE OF THE ISSUE. THE CONTACT HAD NOT EXPERIENCED A FAILURE. VIN TOOL CONFIRMS PARTS NOT AVAILABLE.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied.\n- no: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person."
 },
 {
  "qid": "qc93304cf2c",
  "kind": "yes/no",
  "text": "👳🏻‍♂️and 💣 = No Correlation !",
  "question": "Is it accurate to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "qa8034bd855",
  "kind": "yes/no",
  "text": "Statement 1: He eats from a gasoline bowl\nStatement 2: He eats from a cereal bowl",
  "question": "Would it be correct to say that, of these two statements, Statement 2 does not go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q93d6e2c31f",
  "kind": "yes/no",
  "text": "Situation: They did not announce any engagement and said he was only visiting.\nAction being judged: Not sharing all of your personal life with others.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q222a648ab0",
  "kind": "yes/no",
  "text": "Complaint narrative: FRONT COIL SPRING FRACTURED AND CONTACTED TIRE. LUCKILY I WAS PULLING OUT OF MY PARKING SPOT. BY THE LOOKS OF THE DAMAGE TO THE TIRE, I AM VERY FORTUNATE I HAVE BEEN LIKE THIS AND NOT AT ANY LEVEL OF SPEED. THE FOLLOWING MORNING I LOOKED INTO THE PROBLEM AND FOUND AN ARTICLE BY EDMOND IN MAY 2015 THAT TALKED ABOUT YOUR ORGANIZATION RECALLING HYUNDAI ELANTRA'S?S FOR FRONT COIL SPRING PROBLEMS. FROM THE ARTICLE THIS IS EXACTLY WHAT HAPPENED TO MY CAR. I CALLED HYUNDAI CORPORATION THEY SAID IT WAS NOT UP FOR A RECALL. TWO CALLS TO DEALERSHIPS I WAS AGAIN TOLD THERE WAS NO RECALL. PLEASE FORCE HYUNDAI TO RECALL THIS POTENTIALLY DEADLY ACCIDENT WAITING TO HAPPEN AT THEIR EXPENSE. THANK YOU, [XXX]",
  "question": "According to this vehicle safety complaint, was the vehicle actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q4be4c972d3",
  "kind": "yes/no",
  "text": "The effects of weak solar activity have been notable. The United Kingdom just suffered through a winter with temperatures 5 to 10 degrees C below normal, and German meteorologists report that 2013 has been the coldest year in 208 years. (1)",
  "question": "Is there confirmation that this paragraph makes the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "qf3cff3ef39",
  "kind": "yes/no",
  "text": "Passage:\nThe national postal infrastructure was completely destroyed during the civil war. In order to fill the vacuum, Somali Post signed an agreement in 2003 with the United Arab Emirates' Emirates Post to process mail to and from Somalia. Emirates Post's mail transit hub at the Dubai International Airport was then used to forward mail from Somalia to the UAE and various Western destinations, including Italy, the Netherlands, the United Kingdom, Sweden, Switzerland and Canada.\n\nQuestion: When was the infrastructure of the postal service destroyed?\nReference answer: during the civil war\nCandidate answer: civil war",
  "question": "Is it appropriate to use the candidate answer in place of the reference answer for this question, conveying at least the same information without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "qdcd8172a20",
  "kind": "yes/no",
  "text": "Customer: I am in Davis, California. I'd like to buy some tickets.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I am not sure, but I have heard great things about No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: Is there any showings in Davis, CA?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Well, that's disappointing! Can you tell me what action films are in Davis?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the original Mad Max? The one from the '70s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I don't think I am interested in that, I guess I won't be getting any tickets today since nothing I want to see is playing.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "By the end of this conversation, is there actually a purchase of movie tickets by the customer?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1a9ee3297e",
  "kind": "yes/no",
  "text": "Assistant: OK. I'll place the order.\nCustomer: Thanks. Let me know what time to pick it up.\nAssistant: Sambino's is out of mushrooms. Would you like a different topping?",
  "question": "Per the assistant's latest message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q453c353aa4",
  "kind": "yes/no",
  "text": "Of course the food supply p festivalomrdet planned since long time back's one can speculate why arrangrerna chose dark ages year's surprise at the eleventh hour? Maybe they did not want stricter biljettfrsljningen? Or so they would not give mjligheten from restaurants nrheten to arrange catering just outside the area? A few that quickly hrsammade shortages p n other vegetarian sausages were the men who rushed there and stood on line outside the area. They realized that hr was a hack to earn.",
  "question": "Does this paragraph set forth the contrarian climate claim that climate impacts are not bad or are beneficial?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate impacts are not bad or are beneficial: it argues that warming or its impacts are harmless or good: climate sensitivity is low or negative feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is beneficial (plant food) or not a pollutant; the warming is only a few degrees.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate impacts are not bad or are beneficial."
 },
 {
  "qid": "qf39f99fbdd",
  "kind": "yes/no",
  "text": "Table caption: Dosimetric parameters for FS-HDR-BT plans and MR-Linac plans for a single, 19 Gy dose prescription to the CTV and PTV respectively. *CTV for FS-HDR-BT and PTV for MR-Linac.\n|  |  | FS-HDR-BT | FS-HDR-BT | MR-Linac | MR-Linac |  |\n| Parameter | Reference dose | Median (n = 30) | Range | Median (n = 30) | Range | p-value |\n| Target coverage |  |  |  |  |  |  |\n| D95% CTV/PTV* | ≥19 Gy | 18.8 Gy | 14.0–21.7 Gy | 19.0 Gy | 15.5–21.7 Gy | 0.053 |\n| D90% CTV/PTV* | ≥17 Gy | 20.3 Gy | 15.9–23.8 Gy | 20.2 Gy | 16.7–22.6 Gy | 0.484 |\n| High dose volumes |  |  |  |  |  |  |\n| V100% CTV/PTV* | – | 95% | 73–99% | 95% | 69–100% | 0.894 |\n| V150% CTV/PTV* | – | 55% | 25–77% | 1% | 0–38% | <0.001 |\n| V200% CTV/PTV* | – | 25% | 9–54% | 0% | 0–0% | <0.001 |\n| OAR dose |  |  |  |  |  |  |\n| Urethra D10% | <17.7 Gy | 16.0 Gy | 6.7–18.2 Gy | 17.5 Gy | 8.2–17.7 Gy | <0.001 |\n| Rectum D1cm 3 | <12 Gy | 10.2 Gy | 4.1–12.0 Gy | 12.0 Gy | 9.4–12.0 Gy | <0.001 |\n| Rectum D2cm 3 | – | 8.6 Gy | 1.6–10.8 Gy | 10.7 Gy | 8.4–11.3 Gy | <0.001 |\n| Bladder D1cm 3 | <12 Gy | 8.5 Gy | 1.8–12.1 Gy | 8.4 Gy | 0.4–12.0 Gy | 0.102 |\n| Bladder D2cm 3 | – | 7.0 Gy | 1.6–10.8 Gy | 6.6 Gy | 0.5–11.1 Gy | 0.090 |\n\nStatement: There are 4 types of categories.",
  "question": "Does the table support the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q040401334b",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nThis paper examines short-term birth sequelae of the influenza pandemic of 1918–1920 in the United States using monthly data on births and all-cause deaths for 19 US states in conjunction with data on maternal deaths, stillbirths, and premature births. Notable findings include: 1) a drop in births in the 3 months following peak mortality; 2) a reversion in births to normal levels occurring 5–7 months after peak mortality; and 3) a steep drop in births occurring 9–10 months after peak mortality.\n\nClaim: In the global influenza pandemic of 1918, U.S. birthrates dropped within the initial three months after peak mortality.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "qc8a7850ee3",
  "kind": "yes/no",
  "text": "immigrants can live here, work here so should 🗳️ thats not too much imo",
  "question": "Hateful, is this post?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qf2832801a5",
  "kind": "yes/no",
  "text": "Assistant: Can you please provide your last name?\nCustomer: Smith.\nAssistant: To confirm, your reservation will be booked under the name \"Mary Smith\".",
  "question": "Looking at the assistant's final message, is \"Mary Smith\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb3d8c2b179",
  "kind": "yes/no",
  "text": "Situation: I broke off the relationship, as it was getting too much for me.\nAction being judged: Breaking off relationships that don't make you happy.",
  "question": "Is it true that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qf041f66008",
  "kind": "yes/no",
  "text": "Complaint narrative: WHEN I BRAKE MY BRAKES PUMP AND IT'S LIKE THE ABS IS TRYING TO KICK IN SOMETIMES I HAVE TO PUSH PEDAL ALL THE WAY TO THE FLOOR IN ORDER TO STOP WITH OUT AN INCIDENT. HAD NEW BRAKES INSTALLED AND STILL THE PROBLEM IS THERE.",
  "question": "Is there a report in this vehicle safety complaint of at least a single person being actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qe023b19f56",
  "kind": "yes/no",
  "text": "Statement 1: People drink drinking water\nStatement 2: People drink seawater",
  "question": "Is it the case that, of these two statements, Statement 1 does not go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q225fb8e05a",
  "kind": "yes/no",
  "text": "Statement 1: He went to restaurant because he feels hungry\nStatement 2: He went to beauty parlour because he feels hungry",
  "question": "Would it be correct to say that, of these two statements, Statement 1 doesn't go against common sense?",
  "definitions": "- yes: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense.\n- no: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal."
 },
 {
  "qid": "q83038f5a3a",
  "kind": "yes/no",
  "text": "Republicans at the top of the ticket were missing in action; Republican voters returned the favor. Nationally, in the 2008 election, GOP turnout fell by more than 4 percent while Democratic turnout rose by over 9 percent, according to American University's Center for the Study of the American Electoratenot enough to change the final outcome, but perhaps the difference in a razor-thin swing state such as Indiana, where McCain fell short by a mere 26,000 votes, or North Carolina, which Barack Obama carried by 100,000 votes, or less than 1 percent.",
  "question": "According to this paragraph, does it make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 }
]
