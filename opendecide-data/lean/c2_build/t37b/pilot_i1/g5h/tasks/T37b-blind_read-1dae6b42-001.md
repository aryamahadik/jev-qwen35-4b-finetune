# G5-H blind read T37b-blind_read-1dae6b42-001 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1/g5h/answers/T37b-blind_read-1dae6b42-001.json

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
  "qid": "q936883af63",
  "kind": "yes/no",
  "text": "Table caption: Material properties of Scotch-Weld™ AF 163-2K epoxy film adhesive.\n| Tensile modulus | E Adh | 2046 MPa a |\n| Poisson ratio | ν Adh | 0.34 b |\n\nStatement: Poisson ratio has Adh.",
  "question": "Supported by the table, is the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8ce14d28fe",
  "kind": "yes/no",
  "text": "In response to intense questioning from Rep. Mike Pompeo, Kansas Republican, during a House Energy and Commerce Committee hearing on Sept. 18, EPA Administrator Gina McCarthy admitted that the new regulations are unlikely to have measurable impact on world climate. She then explained the real reasons for the rules: ?What we are attempting to do is put together a comprehensive climate plan across the administration that positions the U.S. for leadership on this issue and that will prompt and leverage international discussions and actions.?",
  "question": "Within this paragraph, does it make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "q040188d5be",
  "kind": "yes/no",
  "text": "Table caption: Parameter Estimates of Latent Class Model for Taiwanese Respondents\n| Taiwan (n = 333) | Latent Class 3-Classes | Latent Class 3-Classes | Latent Class 3-Classes | Latent Class 3-Classes |\n| Variables | Class 1 | Class 2 | Class 3 |  |\n|  | Middle Group | Majority Group | Minority Group |  |\n| Labeling product origin | -2.255*** | 1.861*** | 0.287 |  |\n| Food safety certification | -0.680*** | 2.690*** | 1.384*** |  |\n| High quality appearance | -0.810*** | 0.421*** | 0.795*** |  |\n| Domestic rarity | -3.793*** | -1.122*** | 1.287*** |  |\n| Plantation methods | -3.232*** | 0.696*** | -0.299 |  |\n| Freshness | 0.315* | 1.894*** | 1.134*** |  |\n| Probability Class | 0.254 | 0.611 |  | 0.134 |\nTable notes: Notes: 1) *, **, and *** indicate statistically significant at 10%, 5%, and 1% levels, respectively. 2) The scores of price are 0 as the baseline in the model estimation.\n\nStatement: High quality appearance in Class 1 under middle group is -0.810***.",
  "question": "Is the statement backed up by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q24b2eb12db",
  "kind": "yes/no",
  "text": "Statement 1: illness can be cured during routine physicals\nStatement 2: illness can be found during routine physicals",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q79cd7193b4",
  "kind": "yes/no",
  "text": "Table caption: Experimental parameters showing starting material and extrusion temperature of material A, B and C. The encapsulated powder was extruded with a force of 257 kN after preheating at 700°C for 20 min.\n| Material | Starting material | Extrusion temperature /°C |\n| A | Crushed powder (< 250 μm) | 650 |\n| B | Milled powder (89 wt .% 20-60 μm) | 650 |\n| C | Milled powder (89 wt .% 20-60 μm) | 700 |\n\nStatement: Material C is having 650 Extrusion temperature /C.",
  "question": "Is the statement refuted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qb68efacc4b",
  "kind": "yes/no",
  "text": "Customer: I want movie tickets in Davis, California.\nAgent: No problem. Do you have a movie in mind?\nCustomer: No Time To Die sounds good.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: What about in Davis, California though?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Darn it. What is playing in Davis, California then?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the same movie from the 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I don't want any movie tickets anymore. Thanks anyway.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "According to this conversation, has the customer actually bought movie tickets by the time it ends?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q76d6081ff2",
  "kind": "yes/no",
  "text": "Situation: His parents opted to keep him home instead, until he's more mature.\nAction being judged: Doing what you think is best for your children.",
  "question": "Would it be correct to say that the action being judged isn't wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qc6490a70e8",
  "kind": "yes/no",
  "text": "Customer: I am interested in seeing a movie this weekend.\nAgent: Do you have a preferred city you wish to see a movie?\nCustomer: Yes, please search for theaters in the Prescott Valley area.\nAgent: I have found two tickets in this area: Prescott Valley Harkins 14 and the Picture Show at Frontier Village\nCustomer: Is Star Wars: The rise of Skywalker playing at the Prescott Valley Harkins 14?\nAgent: Yes it is playing at Prescott Valley Harkins 14. Would you like show times?\nCustomer: Yes, please check movie times for Saturday.\nAgent: It is playing on both the standard and IMAX screens. Do you have a preference?\nCustomer: Yes, please check movies times for the standard screen.\nAgent: Star Wars: The Rise of Skywalker is playing on the standard screen at 10am, 1pm, 3pm and 7pm.\nCustomer: Please check availability for two people to the pm show.\nAgent: Yes, two tickets are available. Would you like me to book these for you?\nCustomer: Actually, what are the times that is in playing on the IMAX screen.\nAgent: It is playing on the IMAX screen at 1pm, 4pm and 8pm.\nCustomer: Please check availability for two tickets to the 1pm show.\nAgent: There are two tickets available. Would you like me to book these tickets?\nCustomer: Yes, please book two tickets.\nAgent: Please confirm you would like two tickets Star Wars: The Rise of Skywalker for the 1pm IMAX show on Saturday. This is at the Prescott Valley Harkins 14.\nCustomer: That is correct.\nAgent: Your tickets have been booked. Please check your email for confirmation. Do you need further assistance?\nCustomer: No that is all. Thank you for your help.",
  "question": "Have movie tickets actually been bought by the customer by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q1dd3506809",
  "kind": "yes/no",
  "text": "Jawbox\nJawbox was an American alternative rock band from Washington, D.C., United States. Its original members were J. Robbins (vocals, guitar), Kim Coletta (bass guitar) and Adam Wade (drums). Bill Barbot (vocals, guitar) and Zach Barocas (drums) later joined the group, with Barocas replacing Wade.\n\nKasabian\nKasabian ( ) are an English rock band formed in Leicester in 1997. The band's original members consisted of vocalist Tom Meighan, guitarist and vocalist Sergio Pizzorno, guitarist Chris Karloff, and bassist Chris Edwards. The band's line-up was completed by drummer Ian Matthews in 2004 after a string of session drummers. Karloff left the band in 2006 and founded a new band called Black Onassis. Jay Mehler joined as touring lead guitarist in 2006. Mehler left the band for Liam Gallagher's Beady Eye in 2013, to be replaced by Tim Carter. In 2010 and 2014, Kasabian won the Q Awards for 'Best Act in the World Today', while they were also named \"Best Live Act\" at the 2014 Q Awards and the 2007 NME Awards. The band's music is often described as \"indie rock\", but Pizzorno has said he \"hates indie bands\" and does not feel Kasabian fit into that category.",
  "question": "Is it right to say that Kasabian and Jawbox are not both from England?",
  "definitions": "- yes: The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer.\n- no: Read together, the paragraphs show that the positive statement (the question read without its 'not' or 'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right)."
 },
 {
  "qid": "q74d35fd754",
  "kind": "yes/no",
  "text": "Table caption: Data for allele frequency at five microsatellite loci of Siberian sturgeon Acipenser baerii offspring obtained from a gynogenetic female.\n| Locus | Allele (bp) | Females | Unidentified | Males |\n| Afu-68 | 156 | 0.14 | 0.14 | 0.31 |\n|  | 200 | 0.50 | 0.50 | 0.50 |\n|  | 228 | 0.36 | 0.36 | 0.19 |\n| Aox-45 | 145 | 0.50 | 0.50 | 0.50 |\n|  | 249 | 0.50 | 0.50 | 0.50 |\n| Spl-163 | null allele | 0.00 | 0.14 | 0.15 |\n|  | 188 | 0.03 | 0.14 | 0.00 |\n|  | 192 | 0.29 | 0.14 | 0.25 |\n|  | 196 | 0.00 | 0.11 | 0.16 |\n|  | 200 | 0.36 | 0.29 | 0.33 |\n|  | 204 | 0.32 | 0.21 | 0.11 |\n| Spl-104 | 175 | 0.18 | 0.21 | 0.24 |\n|  | 200 | 0.39 | 0.32 | 0.34 |\n|  | 225 | 0.32 | 0.29 | 0.34 |\n|  | 250 | 0.11 | 0.18 | 0.08 |\n| Spl-106 | null allele | 0.14 | 0.14 | 0.22 |\n|  | 150 | 0.07 | 0.07 | 0.00 |\n|  | 241 | 0.36 | 0.50 | 0.44 |\n|  | 247 | 0.43 | 0.29 | 0.34 |\nTable notes: F-females; U-unidentified; M-males.\n\nStatement: The highest Unidentified value for male is 0.77.",
  "question": "Is it the case that the statement isn't supported by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q36046915f8",
  "kind": "yes/no",
  "text": "Statement 1: His father got angry because he failed the math exam\nStatement 2: His father got excited because he failed the math exam",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q077f35e3df",
  "kind": "yes/no",
  "text": "Table caption: miRNAs and their expression pattern in response to drugs in CRC.\n| miRNAs | Treatment regimen | Expression | Ref. |\n| miR-21 | 5-FU | High | [ 46 ] |\n| miR-214 | 5-Fu | Low | [ 148 ] |\n| miR-143 | Oxaliplatin | Low | [ 149 ] |\n| miR-126 | oxaliplatin | Low | [ 150 ] |\n| miR-10b | 5-Fu | High | [ 151 ] |\n| miR-519c | 5-FU | Low | [ 152 ] |\n| miR-129 | 5-Fu | High | [ 153 ] |\n| miR-625-3p | oxaliplatin | High | [ 154 ] |\n| miR-148a | 5-FU | Low | [ 155 ] |\n| miR-106a, miR-130b, miR-484 | 5-FU, oxaliplatin | High | [ 156 ] |\n| miR-143 | Oxaliplatin | Low | [ 157 ] |\n| miR-215, miR-190b, miR-29b-2 | 5-FU | High | [ 158 ] |\n| miR-625-3p | Oxaliplatin | High | [ 154 ] |\n| miR-320e | 5-FU, oxaliplatin | High | [ 159 ] |\n| miR-150 | 5-FU | Low | [ 68 ] |\n| miR-143 | 5-Fu | Low | [ 160 ] |\n| miR-203 | Oxaliplatin | High | [ 161 ] |\n| miR-494 | 5-Fu | Low | [ 68 ] |\n| miR-1914 | oxaliplatin | Low | [ 162 ] |\n| miR-34a | 5-Fu | Low | [ 69 ] |\n\nStatement: miR-126 has oxaliplatin as Treatment regimen .",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q53ddd0264a",
  "kind": "yes/no",
  "text": "Assistant: You got it. What kind of milk do you want for that?\nCustomer: I'd like Whole Milk if that's an option. And no sugar or anything else, just a Venti Latte Macchiato with Whole Milk.\nAssistant: I'm so sorry, but they're out of whole milk. Would you like to try another option? There's almond milk, coconut milk, nonfat milk, 2% milk, and soy milk.",
  "question": "Would it be correct to say that, according to the assistant's last message, \"whole milk\" is not confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order.\n- no: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction."
 },
 {
  "qid": "q25636b2240",
  "kind": "yes/no",
  "text": "A paper published today in Nature finds \"Australian tropical cyclone activity lower than at any time over the past 5501,500 years\" and \"we show, on the basis of a new tropical cyclone activity index (CAI), that the present low levels of storm activity on the mid west and northeast coasts of Australia are unprecedented over the past 550 to 1,500 years.\" \"Other studies project a decrease in the frequency of tropical cyclones towards the end of the twenty-first century in the southwest Pacific, southern Indian and Australian regions. Our results, although based on a limited record, suggest that this may be occurring much earlier than expected.\"",
  "question": "Does this paragraph set forth the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q27df23b0c5",
  "kind": "yes/no",
  "text": "i fucking ❤️ jokes about pakistanis",
  "question": "Based on the text, is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qabf71ae0ae",
  "kind": "yes/no",
  "text": "Situation: Man Trolling on Dating Sites Is Not Ready to Fall in Love\nAction being judged: Not treating others with respect.",
  "question": "Is the action being judged okay according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa30d00a750",
  "kind": "yes/no",
  "text": "Situation: In love with childhood friend\nAction being judged: Living in the past.",
  "question": "Is the action being judged bad according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qfd63faa033",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CAR HAS BEEN IN AND OUT OF THE DEALERSHIP FOR ALMOST A WEEK OVER THE LAST TWO WEEKS AND THE RECALL HAS NOT BEEN FIXED AND THE DEALERSHIP HAS BEEN UNCOOPERATIVE ABOUT THE REPAIRS.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "qe30c752c51",
  "kind": "yes/no",
  "text": "Table caption: Bias decomposition of the daily CHIRPS and MPEG rainfall (in mm), totalized over wet seasons (1 June – 30 September) within 1 January 2015–31 December 2018: P T – gauge accumulated total rainfall; HB - hit bias; AHB - absolute hit bias; MB – miss bias; N AHB – normalized AHB and N MB – normalized MB .\n| Stations | P T = ∑ i= 1 T P g i | CHIRPS | CHIRPS | CHIRPS | MPEG | MPEG | MPEG | CHIRPS | CHIRPS | MPEG | MPEG |\n| Stations | P T = ∑ i= 1 T P g i | HB | AHB | MB | HB | AHB | MB | N AHB | N MB | N AHB | N MB |\n| Adigudem | 1515.2 | 418.7 | 991.9 | −500.3 | −160.0 | 1166.1 | −294.6 | 0.65 | −0.33 | 0.77 | −0.19 |\n| Debub | 1666.1 | 157.1 | 1029.3 | −491.4 | −429.4 | 1396.9 | −166.9 | 0.62 | −0.29 | 0.84 | −0.10 |\n| Dengolat | 2635.6 | 467.5 | 1494.0 | −1085.8 | −646.0 | 1883.5 | −493.3 | 0.57 | −0.41 | 0.71 | −0.19 |\n| Finarawa | 735.9 | 75.4 | 321.4 | −237.7 | −75.0 | 600.1 | −49.2 | 0.44 | −0.32 | 0.82 | −0.07 |\n| Gijet | 1912.1 | 138.5 | 1121.9 | −652.7 | −572.4 | 1347.3 | −343.5 | 0.59 | −0.34 | 0.70 | −0.18 |\n| Hashenge | 2170.8 | −130.5 | 998.6 | −649.8 | −906.7 | 1260.2 | −396.4 | 0.46 | −0.30 | 0.58 | −0.18 |\n| Maichew | 1542.3 | 414.8 | 1091.7 | −425.8 | −172.4 | 1192.9 | −208.5 | 0.71 | −0.28 | 0.77 | −0.14 |\n| Wedisemero | 2739.4 | 61.1 | 1676.7 | −939.3 | −1182.8 | 2070.7 | −417.6 | 0.61 | −0.34 | 0.76 | −0.15 |\n| Hiwane | 1223.3 | 66.6 | 533.0 | −400.2 | −222.4 | 818.5 | −232.9 | 0.44 | −0.33 | 0.67 | −0.19 |\n| Borra | 1953.0 | 180.7 | 779.3 | −888.3 | −721.8 | 1424.6 | −279.2 | 0.40 | −0.45 | 0.73 | −0.14 |\n| AVG | 1809.4 | 185.0 | 1003.8 | −627.1 | −508.9 | 1316.1 | −288.2 | 0.55 | −0.34 | 0.74 | −0.15 |\n\nStatement: They have different kinds of stations.",
  "question": "Is the assertion backed by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qfec1351ff8",
  "kind": "yes/no",
  "text": "fuck the chavs and their welfare system 🖕🏽",
  "question": "Is it true that this post isn't hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "qed10b7651b",
  "kind": "yes/no",
  "text": "Customer: Do you have one in the east, in the cheap price range?\nAssistant: Sorry, I don't see anything matching that query. Would you like to try a different price range or area?",
  "question": "Going by the text, did the assistant's reply include at least a single option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q6a01c6b6bf",
  "kind": "yes/no",
  "text": "Complaint narrative: EXCESSIVE OIL CONSUMPTION. I WAS NEVER MADE AWARE THAT MY TOYOTA HAD THIS PROBLEM UNTIL I REACHED 100,000 WHICH JUST HAPPENED RECENTLY. ACCORDING TO TOYOTA, MY OPTION FOR COVERAGE ENDED 8/2016. I'M BEING PUNISHED FOR HAVING CONSERVATIVE MILES. CRIMINAL AND DECEIPTFUL.",
  "question": "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "qe0ae7d4c79",
  "kind": "yes/no",
  "text": "Occupation: Rotary Drill Operators, Oil and Gas\nDuties:\n- Remove core samples during drilling to determine the nature of the strata being drilled.\n- Observe pressure gauge and move throttles and levers to control the speed of rotary tables, and to regulate pressure of tools at bottoms of boreholes.\n- Count sections of drill rod to determine depths of boreholes.",
  "question": "Would it be correct to say that the listed duties aren't part of the job of the occupation named above?",
  "definitions": "- yes: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs.\n- no: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined."
 },
 {
  "qid": "q0dc2314eed",
  "kind": "yes/no",
  "text": "Customer: I would like to purchase movie tickets for theaters in Davis, California tonight.\nAgent: No problem. Do you have a movie in mind?\nCustomer: I have been thinking of No Time To Die.\nAgent: It looks like the nearest theater playing No Time To Die is at the AMC Mercado 24 in Sacramento, California.\nCustomer: At what time will it be showing?\nAgent: That’s right. No Time To Die is not showing in Davis, California.\nCustomer: Oh no! What action films are playing in Davis, California tonight?\nAgent: I see one action movie playing in Davis, California at AMC Mercado 24 called Mad Max.\nCustomer: Is that the original Mad Max of 1970s?\nAgent: The release date for this film is October 12, 1979.\nCustomer: I am really sorry i forgot i have a lot of work tonight so i will not be purchasing any tickets tonight.\nAgent: No problem. Hope to talk to you again soon.",
  "question": "Is it true that, by the end of this conversation, the customer has not actually bought movie tickets?",
  "definitions": "- yes: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later.\n- no: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way."
 },
 {
  "qid": "qb90bdc5947",
  "kind": "yes/no",
  "text": "Complaint narrative: CRANK SHAFT SENSOR MALFUNCTION. MY CAR STOP ON ME WHILE DRIVING ON A CITY STREET. IT SHOOK AND THEN SHUT DOWN. VERY SCARY. I HAD TO GET PUSH OUT OF THE STREET BY POLICE CAUSE I WAS IN THE WAY OF TRAFFIC. SOMEONE ALMOST RAN INTO ME.",
  "question": "Has this vehicle safety complaint reported that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q464c3c76fd",
  "kind": "yes/no",
  "text": "Occupation: Database Administrators\nDuties:\n- Plan, coordinate, and implement security measures to safeguard information in computer files against accidental or unauthorized damage, modification or disclosure.\n- Modify existing databases and database management systems or direct programmers and analysts to make changes.\n- Select and enter codes to monitor database performance and to create production databases.",
  "question": "Do the listed duties form part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "q9c25db752b",
  "kind": "yes/no",
  "text": "Passage:\nMaternal factors also play a role in the body’s immune response. At birth, most of the immunoglobulin present is maternal IgG. Because IgM, IgD, IgE and IgA don’t cross the placenta, they are almost undetectable at birth. Some IgA is provided by breast milk. These passively-acquired antibodies can protect the newborn for up to 18 months, but their response is usually short-lived and of low affinity. These antibodies can also produce a negative response. If a child is exposed to the antibody for a particular antigen before being exposed to the antigen itself then the child will produce a dampened response. Passively acquired maternal antibodies can suppress the antibody response to active immunization. Similarly the response of T-cells to vaccination differs in children compared to adults, and vaccines that induce Th1 responses in adults do not readily elicit these same responses in neonates. Between six to nine months after birth, a child’s immune system begins to respond more strongly to glycoproteins, but there is usually no marked improvement in their response to polysaccharides until they are at least one year old. This can be the reason for distinct time frames found in vaccination schedules.\n\nQuestion: Newborns can acquire antibodies from the mother through what means?\nReference answer: breast milk\nCandidate answer: passively",
  "question": "Can the reference answer be replaced by the candidate answer, with the candidate conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q1a2622dbda",
  "kind": "yes/no",
  "text": "Customer: I'm thinking of a movie tomorrow. What's playing in the Fantasy genre nearby?\nAgent: There is a movie called Onward playing nearby tomorrow. Would you like to hear the times?\nCustomer: Yes please\nAgent: Okay do you want the times for the Celebration Cinema Grand RApids North and Imax or for Celebration Cinema Rivertown?\nCustomer: Celebration Cinema Grand Rapids North and Imax.\nAgent: The Movie Onward is playing tomorrow at Celebration Cinema Rivertown at 3:00 pm only. Would you like me to book you a ticket?\nCustomer: Actually i'll be seeing the movie with a date. So i'll need two tickets to this movie tomorrow.\nAgent: I see. So you'd like to book 2 tickets to the movie tomorrow for Onward.\nCustomer: Yes. At Celebration Cinema Grand Rapids North and IMAX at 3:00\nAgent: I'm sorry, the movie isn't playing at 3:00 at that location. Celebration Cinema Grand Rapids IMAX is showing this movie at 2:45 pm.\nCustomer: Are there any other showings?\nAgent: No.\nCustomer: Okay, then book me tickets for 2\nAgent: 2 tickets At Celebration Cinema Rivertown, correct?\nCustomer: No, 2 tickets at Celebration Cinema Grand RApids North and IMAX\nAgent: Are you sure you want to book at the Grand Rapids North location?\nCustomer: Yes. please book them for the Grand Rapids location as discussed for 2:45.\nAgent: Okay, thank you. I am booking two tickets to see Onward tomorrow at the Celebration Cinema Grand Rapids North and IMAX at 2:45. is that right?\nCustomer: Yes please.\nAgent: ”Your tickets are confirmed and they’ve been sent to your email address.”",
  "question": "Has the customer actually bought movie tickets by the end of this conversation?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q3b887e1cd6",
  "kind": "yes/no",
  "text": "Table caption: Description of columns in ASCII text table.\n| Column Name | Description |\n| System | Multibeam echosounder system |\n| Date | Date of survey, yyyymmdd. |\n| Time | Time of survey (UTC), hhmmss. |\n| Easting | Easting Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Northing | Northing Cartesian coordinate, UTM Zone 27 N projection, WGS84. |\n| Depth | Corrected and processed depth, m. |\n| Latitude | Geographical latitude, DD;MM.mm, WGS1984. |\n| Longitude | Geographical longitude, DD;MM.mm, WGS1984. |\n\nStatement: ASCII text table has three categories- Column Name Ratio and Description.",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "q190b46b8f0",
  "kind": "yes/no",
  "text": "Cunningham also worked as a staffer for Sheldon Silver, the former longtime speaker of the state assembly, and she's the ex-wife of current attorney general Eric Schneiderman. She advised Christine Quinn in her campaign for mayor and Andrew Cuomo in his gubernatorial campaign, even as some of her colleagues lent their services to more left-wing candidates. Now with the prominent lobbying and consulting firm SKDKnickerbocker, Cunningham has advised Governor Cuomo on his Medicaid Redesign Team, tasked with cutting payments to hospitals.",
  "question": "Is it correct that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qb0e61820fa",
  "kind": "yes/no",
  "text": "BLM stands for 🦍..right?!",
  "question": "Does this post count as hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qae4bccd641",
  "kind": "yes/no",
  "text": "Assistant: It's in the main room.\nCustomer: Ok perfect - let's book it!\nAssistant: The table for two has been reserved in your name for 8pm tomorrow night, Wednesday January 23rd.",
  "question": "Has \"two\" been confirmed for the customer's restaurant reservation in the assistant's latest message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbf327b246b",
  "kind": "yes/no",
  "text": "Complaint narrative: THE CAR SEAT WARMER IN THE BACK OF THE CAR CAUGHT ON FIRE WHILE OUR SEVEN YEAR OLD WAS ASLEEP IN THE CAR. HE WAS IN HIS BOOSTER SEAT. THE SEAT WARMER WAS NOT ON. (THIS WAS IN AUGUST 2018.) WE SMELLED A BURNING SMELL AND THERE WAS A SMOLDERING FLAME UNDER HIS LEGS. THE CAR WAS STATIONARY, NOT IN MOTION. IT WAS IDLING IN A PARKING LOT.",
  "question": "Is it correct that this vehicle safety complaint does not report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied.\n- no: The complaint says the vehicle actually caught fire, burned or had flames."
 },
 {
  "qid": "q6ee6e1a74f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Zuniga was a founding member of the Earth Communications Office (ECO), and has worked with the Natural Resources Defense Council, the Waterkeeper Alliance, and Environment California.\n\nSummary sentence:\nZuniga has been active in environmental issues since the mid-2000s, and was a founding member of the Earth Communications Office.",
  "question": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q9e0fa5f4fc",
  "kind": "yes/no",
  "text": "Passage:\nMarvin Gardens, the leading yellow property on the board shown, is actually a misspelling of the original location name, \"Marven Gardens\". The misspelling was said to have been introduced by Charles Todd and passed on when his home-made Monopoly board was copied by Charles Darrow and thence Parker Brothers. It was not until 1995 that Parker Brothers acknowledged this mistake and formally apologized to the residents of Marven Gardens for the misspelling although the spelling error was not corrected.\n\nQuestion: Who copied Charles Todd's Monopoly board?\nReference answer: Charles Darrow\nCandidate answer: Charles Darrow and thence Parker Brothers",
  "question": "Is the proposed answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q6e2e898e2d",
  "kind": "yes/no",
  "text": "Passage:\nA capacitor consists of two conductors separated by a non-conductive region. The non-conductive region is called the dielectric. In simpler terms, the dielectric is just an electrical insulator. Examples of dielectric media are glass, air, paper, vacuum, and even a semiconductor depletion region chemically identical to the conductors. A capacitor is assumed to be self-contained and isolated, with no net electric charge and no influence from any external electric field. The conductors thus hold equal and opposite charges on their facing surfaces, and the dielectric develops an electric field. In SI units, a capacitance of one farad means that one coulomb of charge on each conductor causes a voltage of one volt across the device.\n\nQuestion: What net electric charge are capacitors assumed to have?\nReference answer: no net electric charge\nCandidate answer: no",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer because it is a different answer or leaves out important information or adds misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q4b2f8cb0e9",
  "kind": "yes/no",
  "text": "Table caption: An example fuzzy equivalence relation R .\n| R | a | b | c | d |\n| a | 1 | 1 | 0.3 | 0 |\n| b | 1 | 1 | 0.3 | 0 |\n| c | 0.3 | 0.3 | 1 | 0 |\n| d | 0 | 0 | 0 | 1 |\n\nStatement: The value of c for relation R is 1.3.",
  "question": "Is the assertion backed by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe4a2e4556c",
  "kind": "yes/no",
  "text": "Situation: Linda was shocked and quit when the editor didn't like her photos.\nAction being judged: Expressing when you don't like something.",
  "question": "Is it correct that the action being judged isn't acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qcca78e4871",
  "kind": "yes/no",
  "text": "Table caption: Overview of the renewable energy technologies and the selected block types in the Minecraft platform.\n| Energy technology | Block type |\n| Solar panels | Daylight sensor |\n| Wall insulation | Yellow wool |\n| Floor insulation | Orange wool |\n| Double glazing | Glass |\n| Roof insulation | Purple wool |\n\nStatement: There are six renewable energy technologies are given.",
  "question": "Is there support for the statement in the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5294197eab",
  "kind": "yes/no",
  "text": "Passage:\nHellenistic military equipment was generally characterized by an increase in size. Hellenistic-era warships grew from the trireme to include more banks of oars and larger numbers of rowers and soldiers as in the Quadrireme and Quinquereme. The Ptolemaic Tessarakonteres was the largest ship constructed in Antiquity. New siege engines were developed during this period. An unknown engineer developed the torsion-spring catapult (ca. 360) and Dionysios of Alexandria designed a repeating ballista, the Polybolos. Preserved examples of ball projectiles range from 4.4 kg to 78 kg (or over 170 lbs). Demetrius Poliorcetes was notorious for the large siege engines employed in his campaigns, especially during the 12-month siege of Rhodes when he had Epimachos of Athens build a massive 160 ton siege tower named Helepolis, filled with artillery.\n\nQuestion: What type of weapon is the Polybolos?\nReference answer: ballista\nCandidate answer: repeating ballista",
  "question": "Can the candidate answer be used in place of the reference answer, conveying at least the same information without leaving out anything important or adding misleading or superfluous information, for this question?",
  "definitions": "- yes: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous.\n- no: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information."
 },
 {
  "qid": "q6c80b7b032",
  "kind": "yes/no",
  "text": "Customer: I also need  a train.\nAssistant: There are over two thousand trains. Where is your destination?",
  "question": "Did the assistant's reply contain at least a single option meeting everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "qa00b88c9d6",
  "kind": "yes/no",
  "text": "Situation: Grandma Weighs Her Decision to Sever Contact With Daughter\nAction being judged: Hurting your family members to the point that they no longer want anything to do with you.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q0f0ecd098e",
  "kind": "yes/no",
  "text": "Table caption: Columns data type.\n| No | Column | Count | Data type |\n| 1 | responses_header | 16,659 | object |\n| 2 | responses_rating_grade | 11,222 | float64 |\n| 3 | responses_status | 7559 | object |\n| 4 | responses_message | 16,659 | object |\n| 5 | responses_datetime | 16,659 | datetime64[ns] |\n| 6 | reviewer | 16,659 | object |\n| 7 | comments | 16,659 | int64 |\n| 8 | views | 16,659 | int64 |\n| 9 | id | 16,659 | int64 |\n| 10 | have_email | 16,659 | int64 |\n| 11 | responses_message_length | 16,659 | int64 |\n| 12 | gunning_fog_index | 16,659 | float64 |\n| 13 | binary_score | 16,659 | object |\n\nStatement: Column responses_status has the lowest count of 7559.",
  "question": "Supported by the table, is the statement?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q646be603b0",
  "kind": "yes/no",
  "text": "Table caption: Errors in the solution of Example 3.\n| N | h = π 2 N | E abs | / / . / / 2 | RMS | Cond ( A ) |\n| 10 | 0.702481 | 4.59 × 10 - 2 | 1.18 × 10 - 1 | 2.52 × 10 - 2 | 11.51 |\n| 20 | 0.496729 | 2.56 × 10 - 2 | 3.44 × 10 - 2 | 5.31 × 10 - 3 | 21.18 |\n| 30 | 0.405578 | 1.47 × 10 - 2 | 2.00 × 10 - 2 | 2.54 × 10 - 3 | 30.91 |\n| 40 | 0.351241 | 9.36 × 10 - 3 | 1.33 × 10 - 2 | 1.47 × 10 - 3 | 40.67 |\n| 50 | 0.314159 | 6.60 × 10 - 3 | 9.76 × 10 - 3 | 9.67 × 10 - 4 | 50.46 |\n\nStatement: Every N value has the same Cond ( A ).",
  "question": "Is the statement contradicted by the table?",
  "definitions": "- yes: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group.\n- no: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter."
 },
 {
  "qid": "qd61a2dfa72",
  "kind": "yes/no",
  "text": "Passage:\nHowever, excessive hunting and poachers have also contributed heavily to the endangerment, extirpation and extinction of many animals, such as the quagga, the great auk, Steller's sea cow, the thylacine, the bluebuck, the Arabian oryx, the Caspian and Javan tigers, the markhor, the Sumatran rhinoceros, the bison, the North American cougar, the Altai argali sheep, the Asian elephant and many more, primarily for commercial sale or sport. All these animals have been hunted to endangerment or extinction.\n\nQuestion: How have the North American cougar and Asian elephant been hunted?\nReference answer: to endangerment or extinction\nCandidate answer: commercial sale or sport",
  "question": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a distinct answer, excludes important information, or introduces misleading or superfluous information?",
  "definitions": "- yes: Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous information.\n- no: Acceptable substitute: given the question and passage, the candidate conveys at least the same information as the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are fine) and adds nothing misleading or superfluous."
 },
 {
  "qid": "q7b3e003e17",
  "kind": "yes/no",
  "text": "Assistant: of course, putting order in now!\nCustomer: great thank you very much you are always so helpful to me.\nAssistant: ok so you have a large thin crust with half cheese and half extra hamburger and extra cheese on the whole pizza and it will be ready for pick up in about 25 mins",
  "question": "Is there confirmation of \"extra cheese\" for the customer's pizza order in the assistant's final message?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5dd87b28cb",
  "kind": "yes/no",
  "text": "But as we suggested earlier in the year , the incautious statements issued by Met Office scientists looked less like the work of scientific enquiry, and more like post-hoc speculation about which way the weather would turn.",
  "question": "Does this paragraph fail to make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable.\n- no: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy."
 },
 {
  "qid": "qf495dc885d",
  "kind": "yes/no",
  "text": "Stop ❤️ black people! 👎🏻",
  "question": "Is it right to say that this post is not hateful?",
  "definitions": "- yes: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless.\n- no: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat."
 },
 {
  "qid": "qe4251a03ef",
  "kind": "yes/no",
  "text": "Complaint narrative: DRIVING MY TOWN AND COUNTRY CHRYSLER MINIVAN THE ENGINE SHUTOFF WITHOUT ANY WARNING! I ALMOST GOT HIT BY THE CAR BEHIND ME AS I COULD NOT ACCELERATE SINCE THE ENGINE SHUT OFF. I PUT ON MY HAZARDS AND PULLED OVER IN ORDER TO PUT THE VAN IN PARK AND RESTART THE VAN. MY WHOLE FAMILY WAS WITH ME. WE COULD HAVE BEEN SEVERELY INJURED IF THE CAR BEHIND ME HAD HIT ME.",
  "question": "Is there a statement in this vehicle safety complaint that at least a single person was actually injured?",
  "definitions": "- yes: The complaint says at least one person was actually hurt in the incident (any injury, including burns, bruises or airbag injuries).\n- no: The complaint reports nobody hurt: it says no one was injured, only that someone could have been hurt, or it does not mention any injury."
 },
 {
  "qid": "q200178e587",
  "kind": "yes/no",
  "text": "Situation: But she didn't want to wake anyone so she just smiled big instead.\nAction being judged: Being asleep in places where others aren't sleeping.",
  "question": "Is the action being judged bad according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation."
 }
]
