# T37b blind solver T37b-blind_read-71bce312-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1_full/s13/answers/T37b-blind_read-71bce312-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and answer the question by the definitions. Reply with JSON: a list of objects {"qid": <qid>, "answer": "yes" | "no"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "yes" | "no"}. Exactly the keys qid and answer. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q44c29bbe44",
  "kind": "yes/no",
  "text": "Situation: Marge quickly apologized and retrieved her own cart.\nAction being judged: Attempting to take something before someone who was ahead of you.",
  "question": "Is it correct that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe5758223a3",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2014 JEEP PATRIOT. WHILE DRIVING AT AN UNKNOWN SPEED, THE VEHICLE STALLED AND THE SLIP INDICATOR, CHECK ENGINE, AND THROTTLE CONTROL INDICATORS ILLUMINATED. THE VEHICLE WAS TOWED TO THE CONTACT'S RESIDENCE. THE VEHICLE WAS NOT TAKEN TO A DEALER; HOWEVER, AN INDEPENDENT MECHANIC CAME TO THE CONTACT'S RESIDENCE, RESET THE VEHICLE, AND CHANGED THE OIL. THE CONTACT STATED THAT THE FAILURE RECURRED A WEEK LATER. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE AND CONFIRMED THAT THE VIN WAS NOT INCLUDED IN NHTSA CAMPAIGN NUMBER: 13V552000 (ENGINE). THE APPROXIMATE FAILURE MILEAGE WAS 67,000.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q8f45740b48",
  "kind": "yes/no",
  "text": "Customer: I need to get 5 tickets for a movie tomorrow.\nAgent: Sure, I can help you with that. What city and state, please?\nCustomer: We're in Hillsdale, but we like to go into Spring Hills for movies.\nAgent: Okay. What movie would you like to see?\nCustomer: Could you give me some information on a movie called Shuttered? It sounded strange.\nAgent: Yes, I can. Shuttered is a horror movie rated R. On Rotten Tomatoes it has a 61% rating. Do you want the story line?\nCustomer: No, thanks. How about Beyond the Storm?\nAgent: Beyond the storm is an action movie rated PG-13. It has an 81% rating with Rotten Tomatoes.\nCustomer: What is it about?\nAgent: It is about a fishing trawler in the North Sea. The captain has to deal with the extreme weather and the fact that there is a traitor on board that causes problems.\nCustomer: Are they both playing at Cinemark Downtown?\nAgent: Beyond the Storm is playing at Cinemark Downtown and Shuttered is playing at AMC Holiday.\nCustomer: Okay. Let me go ahead and get 5 tickets to the movie Beyond the Storm. We'd like a showtime around 6 or 7, if possible.\nAgent: The showtimes close to that are 6:10pm and 8:30pm.\nCustomer: Okay. I think we'd better get the 6:10pm.\nAgent: Okay. Please let me know if this is the correct information. You want 5 tickets to see Beyond the Storm tonight at 6:10 PM at Cinemark Downtown?\nCustomer: Yes, that sounds about right. How does that email thing work?\nAgent: You'll get an email and you can either print the tickets at home or take the confirmation to the movie.\nCustomer: That sounds easy, okay.\nAgent: Your tickets are confirmed and they've been sent to your email address.",
  "question": "Based on the text, by the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q81aef86d76",
  "kind": "yes/no",
  "text": "Global warming has been described as the greatest threat facing mankind, but the policies designed to address global warming actually pose a much greater threat. The international and domestic policies to ration carbon-based energy would doand are doing little to slow carbon dioxide (CO2) emissions, but would have enormous costs. These costs would fall most heavily on poor people, not only in the United States, but also in the world's poorest nations. The correct approach is not energy rationing, but rather long-term technological transformation and building resiliency in developing societies by increasing their wealth.",
  "question": "Based on the text, does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qffbb1f49d4",
  "kind": "yes/no",
  "text": "Customer: Yes can I make a reservation for 1 people at 16:15 on wednesday?\nAssistant: I'm sorry, there are no available tables at that time. Would you like me to look for a different restaurant?",
  "question": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place.\n- no: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number."
 },
 {
  "qid": "q03a7278194",
  "kind": "yes/no",
  "text": "Table caption: Real-time LAMP results for DNA extraction from Dracunculus medinensis specimens from a range of host species and countries of origin. – indicates no detection and n/a indicates not applicable.\n| Extract ID | Origin | Host | Dracunculus medinensis assay | Dracunculus medinensis assay |\n| Extract ID | Origin | Host | Time to positive (min:sec) | Annealing temperature (°C) |\n| ChDo-339.2 | Chad | Dog | 10:00 | 81.11 |\n| ChHu-69 | Chad | Human | 12:15 | 80.55 |\n| ChDo-1 | Chad | Dog | 7:45 | 81.34 |\n| ChDo-108.5 | Chad | Dog | 8:15 | 81.30 |\n| ChHu-25 | Chad | Human | 8:45 | 80.86 |\n| ChCa-10a | Chad | Cat | 9:00 | 81.15 |\n| ChDo-189 | Chad | Dog | 10:15 | 81.50 |\n| ChDo-13 | Chad | Dog | 8:00 | 81.40 |\n| ChDo-11 | Chad | Dog | 9:00 | 80.86 |\n| ChDo-47.11 | Chad | Dog | 8:30 | 81.60 |\n| ChHu-100 | Chad | Human | 10:15 | 81.35 |\n| ChHu-24 | Chad | Human | 8:30 | 81.45 |\n| ChDo-1 | Chad | Dog | 7:45 | 81.20 |\n| ChHu-283 | Chad | Human | 10:00 | 82.58 |\n| EtDo-172 | Ethiopia | Dog | 12:15 | 82.78 |\n| EtHu-278 | Ethiopia | Human | 10:30 | 82.63 |\n| EtBa-153 | Ethiopia | Baboon | 10:30 | 82.87 |\n| EtHu-152 | Ethiopia | Human | 10:00 | 82.57 |\n| MaHu-165 | Mali | Human | 9:45 | 82.67 |\n| MaHu-240 | Mali | Human | 10:00 | 82.54 |\n| MaHu-242 | Mali | Human | 23:00 | 82.58 |\n| MaHu-253 | Mali | Human | 11:00 | 82.79 |\n| SsHu-201 | South Sudan | Human | 8:45 | 82.50 |\n| SsHu-256 | South Sudan | Human | 10:15 | 82.36 |\n| SsDo-183 | South Sudan | Dog | 10:30 | 82.48 |\n| Uninfected copepod | n/a | n/a | – | – |\n| Dracunculus insignis | n/a | n/a | – | – |\n\nStatement: Time to positive for Dracunculus medinensis assay will be from 7:45 to 23:00.",
  "question": "Based on the table, is the statement supported?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcfb7dd6223",
  "kind": "yes/no",
  "text": "Customer: Yes, I am also Interested in finding a college to visit in the west.  Can you help with that?\nAssistant: There are 5 colleges in that area. Three are free and two have an entrance fee. Clare Hall and Magdalene are free. Do those suit your needs?",
  "question": "Did the assistant find at least a single option that meets everything the customer asked for in its reply?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qcc55d8333b",
  "kind": "yes/no",
  "text": "Customer: My girlfriend and I want to go to the movies!\nAgent: Certainly! Is there a city you have in mind?\nCustomer: Yeah, Springs Hills, Kansas.\nAgent: There are two theaters in Springs Hills. The AMC Holiday Theater, and the Cinemark Downtown.\nCustomer: Let's see. Girlfriend wants to go to the Cinemark Downtown. It's her favorite.\nAgent: The Cinemark Theater it is!\nCustomer: What films are currently playing there?\nAgent: Right now BACKCOUNTRY and BEYOND THE STORM are the two films playing there.\nCustomer: Tell me about BEYOND THE STORM, please. Give me the synopsis and Rotten Tomatoes score.\nAgent: BEYOND THE STORM - Action - rated PG-13 - Rotten Tomatoes 81% - Fishing the North Sea gets ugly as Captain John’s crew faces not only severe weather but a traitor on board - directed by James Cameron.\nCustomer: Yuck! I hate James Cameron, that pompous blowhard. Tell me about BACKCOUNTRY, same tidbits as before.\nAgent: BACKCOUNTRY - Documentary (outdoor) - rated G - Rotten Tomatoes 91% - Explore Yosemite in all its glory in this award winning film that delves into the wonders of one of the United State’s most iconic national parks.\nCustomer: Ok, that I can live with. You know why? James Cameron didn't have his dirty hands in the pot. When is it playing today?\nAgent: BACKCOUNTRY has showtimes of 4:10pm - 7:30pm - 10:15pm.\nCustomer: Ok, that's not a lot to pick from but we'll make due. Get me 2 tickets for 7:30PM tonight for BACKCOUNTRY at the Cinemark, please?\nAgent: To be sure, you want 2 tickets at 7:30pm tonight for BACKCOUNTRY at the Cinemark, correct?\nCustomer: Yes. Place my order.\nAgent: I have just made your order!\nCustomer: Sounds good. Please confirm my tickets.\nAgent: Your tickets are confirmed and they’ve been sent to your email address.",
  "question": "Is it accurate to say that, by the end of this conversation, the customer hasn't actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "q57f8501822",
  "kind": "yes/no",
  "text": "Table caption: Classification results for the heterogeneous population case study with geometric and material differences trained on the labelled source domain and applied to the unlabelled target domain.\n| Method | Method | k NN | JDA |\n| Mapping Training | Accuracy | 16.7% | 100.0% |\n| Mapping Testing | Accuracy | 16.7% | 100.0% |\n\nStatement: There are 3 Methods of Mapping in the given table.",
  "question": "Is the statement supported according to the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q01fb062488",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nHence, COVID-19 patients can develop psychotic symptoms as a consequence of multiple concurrent factors.\n\nClaim: There are no new-onset psychosis-related symptoms developed as a result of COVID-19.",
  "question": "Does the evidence fail to support the claim?",
  "definitions": "- yes: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated.\n- no: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with')."
 },
 {
  "qid": "q4e4b37aebb",
  "kind": "yes/no",
  "text": "Passage:\nClay models of ducks found in China dating back to 4000 BC may indicate the domestication of ducks took place there during the Yangshao culture. Even if this is not the case, domestication of the duck took place in the Far East at least 1500 years earlier than in the West. Lucius Columella, writing in the first century BC, advised those who sought to rear ducks to collect wildfowl eggs and put them under a broody hen, because when raised in this way, the ducks \"lay aside their wild nature and without hesitation breed when shut up in the bird pen\". Despite this, ducks did not appear in agricultural texts in Western Europe until about 810 AD, when they began to be mentioned alongside geese, chickens, and peafowl as being used for rental payments made by tenants to landowners.\n\nQuestion: How long have ducks possibly been in domesticated domicile with humans?\nReference answer: Clay models of ducks found in China dating back to 4000 BC may indicate the domestication of ducks took place there during the Yangshao culture\nCandidate answer: 1500 years",
  "question": "Can the candidate answer replace the reference answer, giving at least the same information for this question, without dropping anything important or adding misleading or extra information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q01d4850eb7",
  "kind": "yes/no",
  "text": "MUSLIM AID is a scam charity IMO 👎🏻",
  "question": "Is it correct that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q28d9b72428",
  "kind": "yes/no",
  "text": "Situation: So while sitting at his house one day he gets call from his friend.\nAction being judged: Taking calls while at home.",
  "question": "Is it correct that the action being judged is not acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q753913ac2b",
  "kind": "yes/no",
  "text": "Passage:\nHoping to extend the Continental System, Napoleon invaded Iberia and declared his brother Joseph the King of Spain in 1808. The Spanish and the Portuguese revolted with British support. The Peninsular War lasted six years, noted for its brutal guerrilla warfare, and culminated in an Allied victory. Fighting also erupted in Central Europe, as the Austrians launched another attack against the French in 1809. Napoleon defeated them at the Battle of Wagram, dissolving the Fifth Coalition formed against France. By 1811, Napoleon ruled over 70 million people across an empire that had domination in Europe, which had not witnessed this level of political consolidation since the days of the Roman Empire. He maintained his strategic status through a series of alliances and family appointments. He created a new aristocracy in France while allowing the return of nobles who had been forced into exile by the Revolution.\n\nQuestion: By 1811, what was the population of Napoleon's Empire?\nReference answer: over 70 million people\nCandidate answer: 70 million people",
  "question": "Can the candidate answer replace the reference answer, giving at least the same information for this question, without dropping anything important or adding misleading or extra information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q7bc148d239",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Zuniga was a founding member of the Earth Communications Office (ECO), and has worked with the Natural Resources Defense Council, the Waterkeeper Alliance, and Environment California.\n\nSummary sentence:\nZuniga has been active in environmental issues since the mid-2000s, and was a founding member of the Earth Communications Office.",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qde937c7958",
  "kind": "yes/no",
  "text": "Assistant: Do you want extra toppings?\nCustomer: OK, let's add mushrooms.\nAssistant: I'm sorry, but there is no Pacific Veggie Pizza now. Do you want to change your order?",
  "question": "Going by the assistant's final message, is \"Pacific Veggie Pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qeb6f970263",
  "kind": "yes/no",
  "text": "Passage:\nIn Britain's \"imperial century\", victory over Napoleon left Britain without any serious international rival, other than Russia in central Asia. Unchallenged at sea, Britain adopted the role of global policeman, a state of affairs later known as the Pax Britannica, and a foreign policy of \"splendid isolation\". Alongside the formal control it exerted over its own colonies, Britain's dominant position in world trade meant that it effectively controlled the economies of many nominally independent countries, such as China, Argentina and Siam, which has been generally characterized as \"informal empire\". Of note during this time was the Anglo-Zulu War, which was fought in 1879 between the British Empire and the Zulu Empire.\n\nQuestion: Britain's dominant position in the world trade allowed them to do what?\nReference answer: effectively controlled the economies of many nominally independent countries, such as China, Argentina and Siam\nCandidate answer: controlled the economies of many nominally independent countries",
  "question": "In light of the reference answer, is the candidate answer an unacceptable substitute, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "qdeae6c42f8",
  "kind": "yes/no",
  "text": "fuck the chavs and their welfare system 🖕🏽",
  "question": "Is it true that this post isn't hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "q78f85758c7",
  "kind": "yes/no",
  "text": "Customer: Can you look up greek food please?\nAssistant: I do not have any Greek in the Centre. Do you have anything else in mind?",
  "question": "Is there confirmation, in its reply, that the assistant found at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q779c550d46",
  "kind": "yes/no",
  "text": "Customer: Hi. I need some movie tickets.\nAgent: What movie would you like to watch?\nCustomer: Uncut Gems.\nAgent: Where would you like to watch Uncut Gems?\nCustomer: Cleveland, Ohio.\nAgent: Sorry, I was not able to find any Uncut Gems viewings in Cleveland. Would you like to watch another movie?\nCustomer: Okay. I'll watch Parasite instead.\nAgent: Where would you like to watch Parasite.\nCustomer: Still in Cleveland.\nAgent: How many tickets will you need?\nCustomer: 4 adult tickets.\nAgent: What time would you like to watch the movie?\nCustomer: 9:00 PM.\nAgent: Sorry, that showtime is not available for this movie.\nCustomer: How about 7:30 PM then?\nAgent: Sorry, that showtime is not available for this movie. Would you like to pick another movie?\nCustomer: No, that's fine. Just forget about it.\nAgent: Are you sure you don't want any tickets?\nCustomer: Yes, I'm sure. Thank you.\nAgent: Okay. Enjoy your day.",
  "question": "Has the customer actually paid for movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q8df47ba9cc",
  "kind": "yes/no",
  "text": "🚫 hate speech (unless its against 👮🏼‍♂️)",
  "question": "Based on the text, is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q054e703793",
  "kind": "yes/no",
  "text": "Occupation: Digital Forensics Analysts\nDuties:\n- Conduct regular design reviews throughout the game development process.\n- Write or supervise the writing of game text and dialogue.\n- Guide design discussions between development teams.",
  "question": "Is the inclusion of the listed duties in the job of the occupation named above true?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qd11f086064",
  "kind": "yes/no",
  "text": "Customer: I'd like to find a good restaurant in the center.\nAssistant: We have many options available in Centre. Is there a specific price range or cuisine type you are interested in?",
  "question": "According to its reply, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q090ffba88f",
  "kind": "yes/no",
  "text": "Situation: She had him wash up and then let him hold the baby.\nAction being judged: Having clean hands before touching a baby.",
  "question": "Is it true that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q344efddf25",
  "kind": "yes/no",
  "text": "Customer: Would you please help me to buy movie tickets for theatres in Davis,California\nAgent: No problem. Do have a movie in mind?\nCustomer: yes,i have a mind on \"no time time to die\"\nAgent: It looks like nearest theater playing No Time Die is at AMC Mercado 24 in Sacramento, California.\nCustomer: Can please check correctly If there is no showing in Davis,California\nAgent: That’s right. No Time Die is not showing in Davis, California.\nCustomer: Not a problem,What action flims are playing in Davis,California.\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: That is the original film from the 1970s\nAgent: release date for film is October 12, 1979.\nCustomer: Sorry, i am not not buy tickets at this moment because the film choice not available in my local area\nAgent: No problem. Hope talk again soon.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q61ec73aecc",
  "kind": "yes/no",
  "text": "Customer: The price doesn't matter, as long as they can accommodate 7 people at 12:45 on Wednesday.  Can you give me the reference # once it's booked?\nAssistant: Alright, I've made a booking at The Lucky Star, for Wednesday at 12:45, for 7 people. The reference number is R9H9B14D. Is there anything else?",
  "question": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?",
  "definitions": "- yes: The assistant states that the requested reservation, room, table or train ticket was booked successfully, usually giving a reference number.\n- no: The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it offers to try another day, time, length of stay or place."
 },
 {
  "qid": "q0cdf3ef751",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nCONCLUSIONS: The incidence of VTE in patients with severe NCP is 25% (20/81), which may be related to poor prognosis.\n\nClaim: There are approximately 1 in 4 incidences of venous thromboembolism in patients with severe novel coronavirus pneumonia symptoms of SARS-CoV-2.",
  "question": "Does the evidence fail to contradict the claim?",
  "definitions": "- yes: The evidence does not show the claim to be false: it agrees with the claim's central assertion (same direction, compatible numbers after ordinary rounding, compatible population), even if hedged.\n- no: The evidence shows the claim is false: it states the opposite direction of effect, a clearly different number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the claim."
 },
 {
  "qid": "q0cb69f5916",
  "kind": "yes/no",
  "text": "Passage:\nJapanese seismologist Yuji Yagi at the University of Tsukuba said that the earthquake occurred in two stages: \"The 155-mile Longmenshan Fault tore in two sections, the first one ripping about seven yards, followed by a second one that sheared four yards.\" His data also showed that the earthquake lasted about two minutes and released 30 times the energy of the Great Hanshin earthquake of 1995 in Japan, which killed over 6,000 people. He pointed out that the shallowness of the epicenter and the density of population greatly increased the severity of the earthquake. Teruyuki Kato, a seismologist at the University of Tokyo, said that the seismic waves of the quake traveled a long distance without losing their power because of the firmness of the terrain in central China. According to reports from Chengdu, the capital of Sichuan province, the earthquake tremors lasted for \"about two or three minutes\".\n\nQuestion: What fault tore in two places?\nReference answer: Longmenshan Fault\nCandidate answer: menshan Fault",
  "question": "Is it appropriate to use the candidate answer in place of the reference answer for this question, conveying at least the same information without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q43641e04da",
  "kind": "yes/no",
  "text": "Complaint narrative: TAKATA RECALL. I HAVE CONTACTED SEVERAL FORD DEALERSHIPS ABOUT COMPLETING THE RECALL REPLACEMENT OF MY AIRBAGS BUT HAVE BEEN TOLD REPEATEDLY THAT THEY DO NOT YET HAVE THE PARTS NECESSARY TO DO IT. IT HAS BEEN WELL OVER A YEAR AND IT IS UNACCEPTABLE THAT THE RECALL CANNOT BE COMPLETED WHEN THERE IS A CLEAR SAFETY HAZARD ASSOCIATED WITH THE TAKATA AIRBAGS.",
  "question": "Does this safety complaint about a vehicle report that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "qb54dd08394",
  "kind": "yes/no",
  "text": "Table caption: Impact analysis of the joint plans, showing investment cost, reduction of gas consumption, electricity production, reduction of CO2-emission, and payback period per technology.\n|  | Investment cost (€) | Reduction in gas consumption (m3) | Electricity production (kWh) | Reduction in CO2 emission (kg CO2-eq) | Payback period (years) |\n| Solar panels | 6,512,100‬ | – | 6,423,219 | 3,211,609 | 5.3 |\n| All insulation | 81,908,719 | 8,878,861 | – | 17,580,145 | 15.3 |\n| All technologies | 88,420,819 | 8,878,861 | 6,423,219 | 20,791,754 | 12.6 |\n\nStatement: All insulation has a highest value in Payback period (years).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qa1cf605aee",
  "kind": "yes/no",
  "text": "But as we suggested earlier in the year , the incautious statements issued by Met Office scientists looked less like the work of scientific enquiry, and more like post-hoc speculation about which way the weather would turn.",
  "question": "Does this paragraph fail to make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qfd8be5de0b",
  "kind": "yes/no",
  "text": "Situation: Joe ended the affair after his wife caught him and threatened divorce.\nAction being judged: Being with a cheater because once a cheater, always a cheater.",
  "question": "Would it be correct to say that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qb1381ab624",
  "kind": "yes/no",
  "text": "Customer: I am looking for a place to stay. The hotel should include free wifi and should be in the type of hotel\nAssistant: There are quite a few hotels that fit that description. Do you have a preference as to area or price range?",
  "question": "Did the assistant, in its reply, find for the customer at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q8f2c372fd0",
  "kind": "yes/no",
  "text": "Customer: Hi\nAgent: Hi, what can i do for you today?\nCustomer: I would like to purchase movie tickets to see a movie tonight for either no time to die, or mulan.\nAgent: Sounds great, can you give me your location please.\nCustomer: I live in Stoneyford Oregon.\nAgent: Awesome,do you know which movie theater you would like to see either of these two movies in?\nCustomer: Mountain AMC 16 please.\nAgent: Sure, let me check the availability of tickets for you.\nCustomer: No problem.\nAgent: I am sorry. I am afraid this movie theater is temporarily closed until the fall, and the release date of both movies has been pushed back as well.\nCustomer: Oh ok, well would you mind checking another theater for me?\nAgent: Sure, which one?\nCustomer: Holiday Cinemark 12.\nAgent: Ok, one second while i do this for you.\nCustomer: Ok.\nAgent: I am sorry. I am afraid this movie theater is temporarily closed until the fall, and the release date of both movies has been pushed back as well.\nCustomer: Dang, oh well. Is there a way to be notified whe either of these theaters are up and running?\nAgent: Yes, just use our app and add the theater to your favorites. This will give you updates with all of the details necessary when they happen.\nCustomer: Thank you for all your help!\nAgent: No problem. Hope to get to speak with you again soon!",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qb3dcc7fcf1",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CONTACT OWNS A 2003 CHEVROLET MONTE CARLO. THE CONTACT STATED THAT WHILE PARKED, THE VEHICLE CAUGHT ON FIRE. THE FIRE DEPARTMENT EXTINGUISHED THE FIRE. A FIRE REPORT WAS NOT FILED AND NO INJURIES WERE REPORTED. THE VEHICLE WAS TOWED TO THE CONTACTS RESIDENCE. THE VEHICLE WAS NOT DIAGNOSED OR REPAIRED. THE CONTACT MENTIONED THAT SHE RECEIVED NOTIFICATION OF NHTSA CAMPAIGN NUMBER: 15V701000 (ENGINE AND ENGINE COOLING) AFTER THE FAILURE OCCURRED. THE MANUFACTURER WAS NOTIFIED OF THE FAILURE. THE FAILURE MILEAGE WAS 150,000.",
  "question": "Did the vehicle actually catch fire, according to this vehicle safety complaint?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qe085b0f43f",
  "kind": "yes/no",
  "text": "Table caption: CMVs and RMVs regarding the performance indicator “The cumulative impact factor value”.\n|  | Current minimum values | Cumulative impact factor, 2014–2018 | Cumulative impact factor, 2014–2018 | Number of years required to fulfill minimum criteria | Number of years required to fulfill minimum criteria | Recalibrated minimum values | Recalibrated minimum values |\n|  |  | IC | FC | IC | FC | IC | FC |\n| Mining | 4 | 8.815 | 3.202 | 2.269 | 6.247 | 3 (2.521) | 0.916 |\n| Geology | 8 | 43.677 | 9.120 | 0.916 | 4.386 | 12 (12.492) | 2.608 |\n| Geodesy and Geoinformatics | 4 | 10.484 | 3.253 | 1.908 | 6.147 | 3 (2.998) | 0.930 |\n| Geophysics | 8 | 28.144 | 5.695 | 1.421 | 7.023 | 8 (8.049) | 1.629 |\n| Geochemistry, Mineralogy and Petrology | 8 | 51.888 | 8.854 | 0.771 | 4.518 | 15 (14.840) | 2.532 |\n| Meteorology | 8 | 36.650 | 6.498 | 1.091 | 6.156 | 10 (10.482) | 1.858 |\n| Paleontology | 8 | 38.067 | 6.710 | 1.051 | 5.961 | 11 (10.887) | 1.919 |\n| Social Geography | 2 | 4.104 | 1.198 | 2.436 | 8.346 | 1 (1.174) | 0.343 |\n| Physical Geography | 4 | 19.950 | 4.246 | 1.002 | 4.710 | 6 (5.706) | 1.214 |\n\nStatement: For example, in this respect, the cumulative impact factor value for geochemists will be only 7.4 times higher than for social geographers.",
  "question": "Is the statement refuted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qf8d40b8cf5",
  "kind": "yes/no",
  "text": "Passage:\nMarvin Gardens, the leading yellow property on the board shown, is actually a misspelling of the original location name, \"Marven Gardens\". The misspelling was said to have been introduced by Charles Todd and passed on when his home-made Monopoly board was copied by Charles Darrow and thence Parker Brothers. It was not until 1995 that Parker Brothers acknowledged this mistake and formally apologized to the residents of Marven Gardens for the misspelling although the spelling error was not corrected.\n\nQuestion: Who copied Charles Todd's Monopoly board?\nReference answer: Charles Darrow\nCandidate answer: Charles Darrow and thence Parker Brothers",
  "question": "Is the proposed answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q0b5396e57a",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "Is the assistant's final message saying that \"TOday\" is confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd25cdd4323",
  "kind": "yes/no",
  "text": "i hate my girl 😀🔫",
  "question": "Is this piece of writing hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qb69e3118dd",
  "kind": "yes/no",
  "text": "Statement 1: illness can be cured during routine physicals\nStatement 2: illness can be found during routine physicals",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qb19effe4ac",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Andrew Anagnost\n- In these roles, he was credited with Autodesk's transition to software as a service, as well as the adoption of cloud computing.\n- Following a four month search, Anagnost was permanently appointed as President and CEO of the company.\n\nSummary sentence:\nAndrew Anagnost is the President and CEO of Autodesk, having been appointed to the positions.",
  "question": "Looking at the summary sentence, is every piece of information in it supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7606407523",
  "kind": "yes/no",
  "text": "Situation: Recovering Alcoholic Opts Out Of Wedding In A Winery\nAction being judged: Considering yourself before considering other people.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q2905e5db98",
  "kind": "yes/no",
  "text": "🐍🐍 They're everywhere 🐍🐍",
  "question": "Is this post full of hatred?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qb0d37d8525",
  "kind": "yes/no",
  "text": "Table caption: Computing time per simulation time for t > 1.\n| Instance set | Sequential | Integrated | Split | Timesplit |\n| 50 | 0.07% | 0.17% | 0.24% | 0.61% |\n| 150 | 0.07% | 1.4% | 3.46% | 6.41% |\n| 250 | 0.07% | 3.39% | 9.67% | 14.67% |\n\nStatement: There are 5 Instance set in the table.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q67de7692dd",
  "kind": "yes/no",
  "text": "Table caption: Correlations between ELISA determined protein concentrations and glycan peak clusters. .\n| Peak cluster | Pearsson correlations | Pearsson correlations | Pearsson correlations | Pearsson correlations |\n| Peak cluster | LF | IgG | IgA | IgM |\n| 2 IgG | 0.31 | 0.33 | ns | 0.19 |\n| 3 LF | 0.61 | 0.23 | 0.30 | 0.32 |\n| 4 LF, GCM | 0.36 | 0.20 | ns | 0.18 |\n| 6 LF, GCM | 0.59 | ns | 0.23 | 0.31 |\n| 7 IgG, LF | 0.38 | 0.22 | 0.25 | ns |\n| 10 GCM, LF | 0.24 | 0.30 | ns | 0.21 |\n| 11 GCM | ns | ns | ns | ns |\n| 12 IgG, GCM | 0.35 | 0.61 | 0.28 | 0.35 |\n| 13 LF, GCM | 0.30 | ns | ns | ns |\n| 16 GCM | ns | ns | ns | ns |\n| 17 GCM, LF | 0.38 | ns | 0.22 | ns |\n| 18 LF, GCM | 0.26 | ns | ns | ns |\n| 21 LF | 0.65 | ns | 0.23 | ns |\n| 24 GCM | ns | ns | ns | ns |\n| 27 GCM | ns | ns | ns | ns |\n| 29 GCM | ns | ns | ns | ns |\n\nStatement: The strongest correlation ( r = 0.81, P <0.0001) was found for peak cluster 21",
  "question": "Is the statement refuted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q61a8d8f203",
  "kind": "yes/no",
  "text": "Passage:\nA capacitor consists of two conductors separated by a non-conductive region. The non-conductive region is called the dielectric. In simpler terms, the dielectric is just an electrical insulator. Examples of dielectric media are glass, air, paper, vacuum, and even a semiconductor depletion region chemically identical to the conductors. A capacitor is assumed to be self-contained and isolated, with no net electric charge and no influence from any external electric field. The conductors thus hold equal and opposite charges on their facing surfaces, and the dielectric develops an electric field. In SI units, a capacitance of one farad means that one coulomb of charge on each conductor causes a voltage of one volt across the device.\n\nQuestion: What net electric charge are capacitors assumed to have?\nReference answer: no net electric charge\nCandidate answer: no",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer because it is a different answer or leaves out important information or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q6e98bb9430",
  "kind": "yes/no",
  "text": "Table caption: The post-processing treatments applied in the current study.\n| Sub-group (designation) | Post-processing parameters |\n| As-processed (AP) | L-PBF Ti6Al4V with a diamond unit cell of 1.5 mm. |\n| Hot isostatic pressing (HIP) | Heated at 920 °C under 100 MPa pressure for 120 min in an argon atmosphere followed by furnace cooling at a rate of 10 °C/min. |\n| Sand blasting (SB) | Sandblasting with abrasive Al 2 O 3 particles (50 μm) for 90 s with a nozzle pressure of 4.5 bar and a sample rotation speed of 20 RPM. |\n| Chemical etching (CE1) | Immersing in a solution made by mixing 50 mL H 2 O, 25 mL HNO 3 , and 5 mL HF for 120 s in an ultrasonic bath. |\n| Chemical etching (CE2) | Immersing in a solution made by mixing 50 mL H 2 O, 25 mL H 2 SO 4 , and 25 mL HCl for 60 min in an ultrasonic bath. |\n\nStatement: As-processed (AP) is having L-PBF Ti6Al4V with a diamond unit cell of 1.5 mm.",
  "question": "Is there support for the statement in the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf4cba4795d",
  "kind": "yes/no",
  "text": "Customer: I am looking for a restaurant that is moderately priced and serves Cantonese food.\nAssistant: There are no restaurants that serve Cantonese food in the moderate price range.",
  "question": "In the response the assistant gave, did the assistant find at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qefe169ec3e",
  "kind": "yes/no",
  "text": "Passage:\nMaternal factors also play a role in the body’s immune response. At birth, most of the immunoglobulin present is maternal IgG. Because IgM, IgD, IgE and IgA don’t cross the placenta, they are almost undetectable at birth. Some IgA is provided by breast milk. These passively-acquired antibodies can protect the newborn for up to 18 months, but their response is usually short-lived and of low affinity. These antibodies can also produce a negative response. If a child is exposed to the antibody for a particular antigen before being exposed to the antigen itself then the child will produce a dampened response. Passively acquired maternal antibodies can suppress the antibody response to active immunization. Similarly the response of T-cells to vaccination differs in children compared to adults, and vaccines that induce Th1 responses in adults do not readily elicit these same responses in neonates. Between six to nine months after birth, a child’s immune system begins to respond more strongly to glycoproteins, but there is usually no marked improvement in their response to polysaccharides until they are at least one year old. This can be the reason for distinct time frames found in vaccination schedules.\n\nQuestion: Newborns can acquire antibodies from the mother through what means?\nReference answer: breast milk\nCandidate answer: passively",
  "question": "Can the reference answer be replaced by the candidate answer, with the candidate conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q39009c6b19",
  "kind": "yes/no",
  "text": "A paper published today in Nature finds \"Australian tropical cyclone activity lower than at any time over the past 5501,500 years\" and \"we show, on the basis of a new tropical cyclone activity index (CAI), that the present low levels of storm activity on the mid west and northeast coasts of Australia are unprecedented over the past 550 to 1,500 years.\" \"Other studies project a decrease in the frequency of tropical cyclones towards the end of the twenty-first century in the southwest Pacific, southern Indian and Australian regions. Our results, although based on a limited record, suggest that this may be occurring much earlier than expected.\"",
  "question": "Does this paragraph set forth the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 }
]
