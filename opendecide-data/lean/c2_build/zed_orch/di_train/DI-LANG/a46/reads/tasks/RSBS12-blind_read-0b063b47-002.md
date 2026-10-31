# A46 replay label-noise blind read RSBS12-blind_read-0b063b47-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS12-blind_read-0b063b47-002.json

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
  "qid": "q127a06eda9",
  "kind": "yes/no",
  "text": "Claim: The author of the semi-satirical novel The Foundation Pit died before Mexican author John Masefield.\n\nPassages:\n\n[John Masefield]\nJohn Edward Masefield, OM ( ; 1 June 1878 – 12 May 1967) English poet and writer, was Poet Laureate of the United Kingdom from 1930.\n\n[Andrei Platonov]\nAndrei Platonov (Russian: Андре́й Плато́нов , ] ; August 28 [O.S. August 16] 1899 – January 5, 1951) was the pen name of Andrei Platonovich Klimentov (Russian: Андре́й Плато́нович Климе́нтов ), a Soviet Russian writer, playwright, and poet, whose works anticipate existentialism.\n\n[The Foundation Pit]\nThe Foundation Pit (Russian: Котлован, \"kotlovan\") is a gloomy symbolic and semi-satirical novel by Andrei Platonov.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q91e53a4c1b",
  "kind": "yes/no",
  "text": "Claim: Jeff Wadlow directed the movie starring James Hayman and American film and television actress, best known for her role as Jesse Quick in The CW's \"The Flash.\n\nPassages:\n\n[Violett Beane]\nViolett Beane (born May 18, 1996) is an American film and television actress, best known for her role as Jesse Quick in The CW's \"The Flash\".\n\n[Truth or Dare (2018 film)]\nTruth or Dare is an upcoming American supernatural horror film directed by Jeff Wadlow and written by Wadlow, Christopher Roach, Michael Reisz and Jillian Jacobs. It stars Lucy Hale, Tyler Posey, Violett Beane, Nolan Gerard Funk, Hayden Szeto and Sophia Taylor Ali.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8dd3c908b7",
  "kind": "yes/no",
  "text": "Post: \"calm down, I've only had it a couple weeks\" 🤨😒",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q09072d2b80",
  "kind": "yes/no",
  "text": "Claim: Oklahoma City Thunder won the Northwest Division in 2015-16. Their first season under current the head coach played basketball under at NCAA. He was also coach of the 2013–14 Kennesaw State Owls men's basketball team.\n\nPassages:\n\n[Billy Donovan]\nWilliam John Donovan Jr. (born May 30, 1965) is an American professional basketball coach who is currently the head coach for the Oklahoma City Thunder of the National Basketball Association (NBA).\n\n[Lewis Preston (basketball)]\nHe previously served as an assistant men's basketball coach at Pennsylvania State University, Coastal Carolina University, the University of Notre Dame, and under Billy Donovan at the University of Florida.\n\n[2013–14 Kennesaw State Owls men's basketball team]\nThe Owls, led by third year head coach Lewis Preston, played their home games at the KSU Convocation Center and were members of the Atlantic Sun Conference.\n\n[2015–16 Oklahoma City Thunder season]\nAfter coming just short of making the playoffs the previous season, the Thunder won the Northwest Division and clinched the third seed in the Western Conference.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q54c6c1b726",
  "kind": "yes/no",
  "text": "Claim: The film that was the prequel to another movie came before Candleshoe. Winifred Deforest Coffin appeared in this other movie.\n\nPassages:\n\n[Winifred Deforest Coffin]\nCoffin was an actress who appeared in Hollywood films (\"Now You See Him, Now You Don't\"), and many television shows including \"Adam-12\", \"The Doris Day Show\", \"The Debbie Reynolds Show\", \"Lancer\", \"The Beverly Hillbillies\", \"High Chaparral\", \"Death Valley Days\", \"Petticoat Junction\", \"Perry Mason\", \"Bonanza\", \"Bewitched\", \"Honey West\", \"The Ann Sothern Show\".\n\n[The Strongest Man in the World]\nThe Strongest Man in the World is a 1975 Disney film starring Kurt Russell, still a student in the fictional Medfield College.\n\n[Candleshoe]\nCandleshoe is a 1977 American family adventure film produced by Walt Disney Productions based on the Michael Innes novel \"Christmas at Candleshoe\" and starring Jodie Foster, David Niven, Helen Hayes in her last big screen appearance and Leo McKern.\n\n[Now You See Him, Now You Don't]\nIt is the sequel to the 1969 film \"The Computer Wore Tennis Shoes\" and was followed by 1975's \"The Strongest Man in the World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc373b21de8",
  "kind": "yes/no",
  "text": "Claim: The locals consider the township of Indian Independence a suburb of a town which is in the Division of Mayo.\n\nPassages:\n\n[Crafers, South Australia]\nThe town of Crafers is in the Adelaide Hills to the south-east of Adelaide, South Australia. Although technically considered to be an outer suburb of Adelaide, with many residents commuting to the city to work, locals consider Crafers to be more a suburb of the nearby township of Stirling.\n\n[Division of Mayo]\nThe Division of Mayo is an Australian electoral division located to the east, south, south-east and south-west of Adelaide, South Australia. It takes in the Adelaide Hills, Fleurieu Peninsula and Kangaroo Island, including the towns of Bridgewater, Crafers, Echunga, Gumeracha, Hahndorf, Kingscote, Langhorne Creek, Lobethal, Macclesfield, Mount Barker, Myponga, Oakbank, Stirling, Strathalbyn, Victor Harbor, Woodside, Yankalilla, and part of Birdwood.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2e61fd7467",
  "kind": "yes/no",
  "text": "Claim: 2017 Texas Tech Red Raiders baseball team and Dan Law Field at Rip Griffin Park have Texas Tech University in common.\n\nPassages:\n\n[Dan Law Field at Rip Griffin Park]\nIt is located on the Texas Tech University campus, adjacent to Jones AT&T Stadium and Fuller Track.\n\n[2017 Texas Tech Red Raiders baseball team]\nThe 2017 Texas Tech Red Raiders baseball team represents Texas Tech University during the 2017 NCAA Division I baseball season.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q168b51dcde",
  "kind": "yes/no",
  "text": "Claim: Libya in the Maghreb region of North Africa has the 34,000 capacity First Statement Stadium.\n\nPassages:\n\n[First Statement Stadium]\nFirst Statement Stadium (Arabic: ملعب البيان الأول‎ ‎ ) is a multi-purpose stadium in Benghazi, Libya.\n\n[Libya]\nLibya (Arabic: ليبيا‎ ‎ \"Lībiyā \") is a country in the Maghreb region of North Africa, bordered by the Mediterranean Sea to the north, Egypt to the east, Sudan to the southeast, Chad and Niger to the south and Algeria and Tunisia to the west.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q75f475b35f",
  "kind": "yes/no",
  "text": "Claim: The youngest child of soccer player Mangue Cisse plays for the Swiss club Yverdon.\n\nPassages:\n\n[Mangué Cissé]\nHe had seven children, the youngest of which is French international, Djibril Cissé.\n\n[Djibril Cissé]\nDjibril Cissé (] ; born 12 August 1981) is a French footballer who plays for Swiss club Yverdon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9fc692b3f4",
  "kind": "yes/no",
  "text": "Claim: African-American activist Bertha Gilkey pursued a career in Property management in St. Louis, Missouri.\n\nPassages:\n\n[Bertha Gilkey]\nShe set up the first tenant management association in St. Louis, Missouri, which successfully rehabilitated the once decrepit Cochran Gardens public housing project, and managed it for more than 20 years.\n\n[Property management]\nProperty management is the operation, control, and oversight of real estate as used in its most broad terms.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7d0c4ea2d9",
  "kind": "yes/no",
  "text": "Claim: Ahmad Niyaltigin was the treasurer of a Yemeni sultan who rose to power by seizing the Ghaznavid throne from his younger twin.\n\nPassages:\n\n[Mas'ud I of Ghazni]\nMas'ud I of Ghazni (Persian: مسعود غزنوی‎ ‎ ), known as Amīr-i Shahīd (امیر شهید ; \"the martyr king\")(998 – 17 January 1040), was \"sultan\" of the Ghaznavid Empire from 1030 to 1040. He rose to power by seizing the Ghaznavid throne from his younger twin Mohammad, who had been nominated as the heir upon the death of their father Mahmud of Ghazni.\n\n[Ahmad Niyaltigin]\nAhmad Niyaltigin (Persian: ‎ ‎ ) was a treasurer of Sultan Mahmud Ghaznavi and later of his son Sultan Mas'ud Ghaznavi.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6d9ba6b801",
  "kind": "yes/no",
  "text": "Claim: The Canadian Province of Nova Scotia was captured with the support of the Mi'kmaq, Maliseet, Passamaquoddy, Abenaki, and APTN National News.\n\nPassages:\n\n[Wabanaki Confederacy]\nThe Wabanaki Confederacy (\"Wabenaki, Wobanaki\", translated roughly as \"People of the First Light\" or \"People of the Dawnland\") are a First Nations and Native American confederation of five principal nations: the Mi'kmaq, Maliseet, Passamaquoddy, Abenaki, and Penobscot.\n\n[Siege of Port Royal (1710)]\nThe successful British siege marked the beginning of permanent British control over the peninsular portion of Acadia, which they renamed Nova Scotia, and it was the first time the British took and held a French colonial possession.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9fc5cfc6d4",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Please consider map filters on online mutliplayer. Pretty pls, thanks @CallofDutyUK",
   "I want map filters on COD"
  ]
 },
 {
  "qid": "q86fdc1cecc",
  "kind": "yes/no",
  "text": "Post: Just want to say well done to every single person who has received their A Level results today ❤️",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qe6713f0432",
  "kind": "yes/no",
  "text": "Claim: African-American actor Andy Samberg starred in the comedy film Take the 10, released on Netflix on January 20, 2017.\n\nPassages:\n\n[Take the 10]\nTake the 10 is a 2017 American comedy film written and directed by Chester Tam. The film stars Josh Peck, Tony Revolori, Emily Chang, Cleopatra Coleman, Kevin Corrigan and Andy Samberg.\n\n[Andy Samberg]\nAndrew David Samberg (born David A. J. Samberg; August 18, 1978) is an American actor, filmmaker, musician and comedian.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q649f013533",
  "kind": "yes/no",
  "text": "Claim: Gina Bramhill was born in an Italian village. The 2011 population of the unitary authority area that includes this village was 167,446.\n\nPassages:\n\n[Gina Bramhill]\nGina Bramhill was born in Eastoft, where she grew up on a farm.\n\n[North Lincolnshire]\nThe population of the Unitary Authority at the 2011 census was 167,446.\n\n[Eastoft]\nEastoft is a village and civil parish in North Lincolnshire, England.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf253b991f7",
  "kind": "yes/no",
  "text": "Text: Will pessi sign for man city",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q3c019242af",
  "kind": "yes/no",
  "text": "Text: i have been informed that, as aroace and agender, i have triple visibility and am now visible from space.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd9414568b4",
  "kind": "yes/no",
  "text": "Claim: The Deal Timeball in Iceland can be 0.9 s. from Coordinated Universal Time.\n\nPassages:\n\n[Deal Timeball]\nDeal Timeball is a Victorian maritime Greenwich Mean Time signal located on the roof of a waterfront four-storey tower in the coastal town of Deal, in Kent, England.\n\n[Greenwich Mean Time]\nToday GMT is considered equivalent to UTC for UK civil purposes (but this is not formalised) and for navigation is considered equivalent to UT1 (the modern form of mean solar time at 0° longitude); these two meanings can differ by up to 0.9 s. Consequently, the term GMT should not be used for precise purposes.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3d7cc7eba7",
  "kind": "yes/no",
  "text": "Claim: The 133d Air Refueling Squadron unit of the Air National Guard is located at a base that was host to the 509th Bomb Wing flying the General Dynamics FB-111A.\n\nPassages:\n\n[133d Air Refueling Squadron]\nThe 133d Air Refueling Squadron (133 ARS) is a unit of the New Hampshire Air National Guard 157th Air Refueling Wing located at Pease Air National Guard Base, Portsmouth, New Hampshire, United States.\n\n[Pease Air National Guard Base]\nIt occupies a portion of what was once Pease Air Force Base, a former Strategic Air Command facility with a base-related population of 10,000 and which was home to the 509th Bomb Wing (509 BW) flying the General Dynamics FB-111A.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3fbc238fc4",
  "kind": "yes/no",
  "text": "Claim: Mike Huckabee took part in the most recent Republican Presidential primaries, which began on February 1, 2016.\n\nPassages:\n\n[Mike Huckabee presidential campaign, 2016]\nHuckabee's candidacy for the Republican nomination in the 2016 Presidential election is his second, after having previously run in 2008.\n\n[Republican Party presidential primaries, 2016]\nThe 2016 Republican Party presidential primaries and caucuses were a series of electoral contests taking place within all 50 U.S. states, the District of Columbia, and five U.S. territories, occurring between February 1 and June 7.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q89cb631e6a",
  "kind": "yes/no",
  "text": "Claim: Natalie Martinez is know for her role in the 2008 American-German-British speculative fiction action thriller Death Race.\n\nPassages:\n\n[Natalie Martinez]\nNatalie Martinez (born July 12, 1984) is an American actress and model. She is known as the spokes-model for JLO by Jennifer Lopez, and for her role in the 2008 feature film \"Death Race\".\n\n[Death Race (film)]\nDeath Race is a 2008 American-German-British science fiction action thriller film produced, written, and directed by Paul W. S. Anderson and starring Jason Statham.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9ee78d23db",
  "kind": "yes/no",
  "text": "Claim: The creator Norman Alfred William Lindsay enjoyed boxing, but the author of The Hundred Secret Senses did not.\n\nPassages:\n\n[Norman Lindsay]\nNorman Alfred William Lindsay (22 February 1879 – 21 November 1969) was an Australian artist, etcher, sculptor, writer, editorial cartoonist, scale modeller, and an accomplished amateur boxer.\n\n[The Hundred Secret Senses]\nThe Hundred Secret Senses is a bestselling 1995 novel by Chinese-American writer Amy Tan.\n\n[Amy Tan]\nAmy Tan (born February 19, 1952) is an American writer whose works explore mother-daughter relationships and the Chinese American experience.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6105ef4795",
  "kind": "yes/no",
  "text": "Post: AS SHE SHOULD https://t.co/v1p2hHIC1i",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q95e650a836",
  "kind": "yes/no",
  "text": "Claim: The director and producer of Inside Out (1975 film) was an actor. So was the director of the 2001 horror movie, The Temptress.\n\nPassages:\n\n[Fred Niblo]\nFred Niblo (January 6, 1874 – November 11, 1948) was an American pioneer film actor, director and producer.\n\n[Inside Out (1975 film)]\nInside Out is a 1975 British action thriller film, produced and directed by Peter Duffell, and starring James Mason, Robert Culp, and Telly Savalas.\n\n[The Temptress]\nThe Temptress (1926) is an American silent romantic drama film directed by Fred Niblo.\n\n[Peter Duffell]\nPeter Duffell (born 1937) is a British film and television director and screenwriter, born in Canterbury, England.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa49d88bdf6",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "I just love falling up the stairs 😑",
   "I really don't like falling up the stairs."
  ]
 },
 {
  "qid": "q2644ac529e",
  "kind": "yes/no",
  "text": "Claim: The producer of Back to the World (Street Dogs album), is the Executive Vice President of A&R at Capitol Records. The Welsh singer who was played on WWBZ (103.5 FM, \"The Blaze\") with Whitney and Elton, is not.\n\nPassages:\n\n[Rod Stewart]\nSir Roderick David \"Rod\" Stewart, {'1': \", '2': \", '3': \", '4': \"} (born 10 January 1945) is a British rock singer and songwriter.\n\n[Back to the World (Street Dogs album)]\nThe album was produced by Nate Albert, formerly of The Mighty Mighty Bosstones.\n\n[WWBZ (defunct)]\nOn March 29, the sounds of Whitney, Rod and Elton gave way to 24 hours of \"Rock Rock ('til you drop)\" by Def Leppard.\n\n[Nate Albert]\nNate Albert (born 1970) is an American music executive, songwriter, producer and guitar player. He is currently the Executive Vice President of A&R at Capitol Records a division of Universal Music Group.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcd26128ec6",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I was to undertake my 2 covid vaccination but unfortunately I turned up 12 hrs to early and could be completed until after 56 days",
   "Drop in Center to let people get the 1st or 2nd Vaccine open today . I went thinking I was able to get my 2nd one . Wait in the que 30 mins .sits down arm ready to get ! Sorry your 12hrs to early !!! We cannot vacinate you till 56 days !!! @NicolaSturgeon #Seriously"
  ]
 },
 {
  "qid": "q8547e3f70a",
  "kind": "yes/no",
  "text": "Claim: The defending champion who lost the Singles title at the 1994 Waldbaum's Hamlet Cup has been a professional tennis players. The man who partnered with Andy Ram at the 2009 Australian Open – Men's Doubles us also a professional tennis player.\n\nPassages:\n\n[1994 Waldbaum's Hamlet Cup – Singles]\nMarc Rosset was the defending champion, but lost in the second round to Renzo Furlan.\n\n[Max Mirnyi]\nMaksim \"Max\" Mirnyi (Belarusian: Максім Мікалаевіч Мірны ] ) (Russian: Максим Николаевич Мирный ] ) (born 6 July 1977, in Minsk) is a Belarusian professional tennis player.\n\n[Marc Rosset]\nMarc Rosset (born 7 November 1970) is a former professional tennis player from Switzerland who is best remembered for winning the men's singles gold medal at the 1992 Olympic Games.\n\n[2009 Australian Open – Men's Doubles]\nJonathan Erlich and Andy Ram were the defending champions, but Erlich chose not to participate due to an elbow injury, and only Ram competed that year.Ram partnered with Max Mirnyi, but lost to Feliciano López and Fernando Verdasco in the second round.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0aa1a78c3e",
  "kind": "yes/no",
  "text": "Text: Gods playing games today. Makin it 68 degrees but 1000% humidity. Smh",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q8b6b6680ae",
  "kind": "yes/no",
  "text": "Claim: Aldona Jonaitis is a professor of anthropology at this school. That school was founded after the university Robin Behn is a professor at.\n\nPassages:\n\n[University of Alabama]\nThe University of Alabama (Alabama or UA) is a public research university located in Tuscaloosa, Alabama, United States, and the flagship of the University of Alabama System. Founded in 1820, UA is the oldest and largest of the public universities in Alabama.\n\n[Aldona Jonaitis]\nAldona Jonaitis is the director of the University of Alaska Museum of the North, a professor of anthropology at the University of Alaska Fairbanks, and an author who has published widely on Native American art.\n\n[Robin Behn]\nRobin Behn (born 1958) is an American poet, and professor at University of Alabama, and Vermont College of Fine Arts.\n\n[University of Alaska Fairbanks]\nThe University of Alaska Fairbanks (also referred to as UAF or Alaska) is a public research university in Fairbanks, Alaska, United States. UAF was established in 1917 and opened for classes in 1922.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q28b1fb04d5",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I heard it might be snowing ??? Sounds fake, but okay??? Can anyone verify?????????",
   "I see that it is snowing. This is expected in January. Anyone can see that it is snowing."
  ]
 },
 {
  "qid": "q1ec5c14510",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "The customer service worker sprayed customers with water like one does to train pets.",
   "@MollyJongFast I think it should be allowed for customer service workers to squirt water into their face like how they do sometimes to train pets"
  ]
 },
 {
  "qid": "q34fc6d4401",
  "kind": "yes/no",
  "text": "Text: @sonofsama1 @BoqorofCeel U got more than me🥺",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q6110f94048",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "My poo is green, how festive.",
   "I have diarrhoea"
  ]
 },
 {
  "qid": "qf7579d6f34",
  "kind": "yes/no",
  "text": "Tweet: @KhoaVuUmn Reviewer 2: this is a very weak paper that fails proof of concept. Stating a cat bed is also a wizard's hat is totally wrong and your data cannot support this",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb318494c6e",
  "kind": "yes/no",
  "text": "Claim: The broadcast studio of the commercial channel that along with CNN and BBC disputes the murderer of Neda is at 1211 Avenue of the Americas, New York City, New York.\n\nPassages:\n\n[Death of Neda Agha-Soltan]\nThe murderer of Neda is disputed; according to CNN, BBC, and Fox News, she was shot by Basij, a paramilitary organization.\n\n[Fox News]\nFox News (officially known as the Fox News Channel, commonly abbreviated to FNC) is an American basic cable and satellite television news channel owned by the Fox Entertainment Group, a subsidiary of 21st Century Fox. The channel broadcasts primarily from studios at 1211 Avenue of the Americas, New York City, New York.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q213a17a85e",
  "kind": "yes/no",
  "text": "Claim: Stephen Roger \"Steve\" Bruce was the football manager that played in the Football League Cup in 1985 and managed to lead the Birmingham City Football Club's 103rd season to finish in the 18th position.\n\nPassages:\n\n[Steve Bruce]\nStephen Roger \"Steve\" Bruce (born 31 December 1960) is an English professional football manager and former player who is currently manager of Aston Villa. Bruce was offered an apprenticeship and went on to play more than 200 games for the club before joining Norwich City in 1984, winning the Football League Cup in 1985.\n\n[2005–06 Birmingham City F.C. season]\nThe 2005–06 season was Birmingham City Football Club's 103rd season in the English football league system and their fourth in the Premier League. Under the management of Steve Bruce, they finished in 18th position in the 20-team division, so were relegated to the Championship for 2006–07.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc71788e341",
  "kind": "yes/no",
  "text": "Claim: The composer of \"Prima la musica e poi le parole\" was born in Legnago.\n\nPassages:\n\n[Antonio Salieri]\nAntonio Salieri (] ; 18 August 17507 May 1825) was an Italian classical composer, conductor, and teacher. He was born in Legnago, south of Verona, in the Republic of Venice, and spent his adult life and career as a subject of the Habsburg Monarchy.\n\n[Giulio Sabino]\nThe opera, staged in six or seven European countries at the end of the 18th century, was the subject of a parody in Antonio Salieri's 1786 work \"Prima la musica e poi le parole\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q66a0b878e0",
  "kind": "yes/no",
  "text": "Claim: The genre of music shared, by a vocalist from Napalm Death who made a guest appearance on Leng Tch'e's Hypomaniac, and Jens Kidman is extreme metal\n\nPassages:\n\n[Jens Kidman]\nJens Kidman (born 8 June 1966) is a Swedish metal vocalist.\n\n[Hypomanic (album)]\nA video was made for the song \"Totalitarian\" on YouTube , featuring a guest appearance by Barney Greenway of Napalm Death.\n\n[Barney Greenway]\nMark Andrew \"Barney\" Greenway (born 13 July 1969) is a British extreme metal vocalist, who has been a member of Napalm Death, Extreme Noise Terror, and Benediction.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf13eb269fc",
  "kind": "yes/no",
  "text": "Claim: San Francisco National Cemetery that George W. Wallace is buried at, is located at a park that is part of Golden Gate National Recreation Area.\n\nPassages:\n\n[San Francisco National Cemetery]\nSan Francisco National Cemetery is an United States national cemetery, located in the Presidio of San Francisco, California.\n\n[George W. Wallace]\nHe is buried at San Francisco National Cemetery.\n\n[Presidio of San Francisco]\nThe Presidio of San Francisco (originally, El Presidio Real de San Francisco or The Royal Fortress of Saint Francis) is a park and former U.S. Army military fort on the northern tip of the San Francisco Peninsula in San Francisco, California, and is part of the Golden Gate National Recreation Area.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q257bfc8c86",
  "kind": "yes/no",
  "text": "Claim: Tantrix and Personal Preference are both types of games.\n\nPassages:\n\n[Tantrix]\nTantrix is a hexagonal tile-based abstract game invented by Mike McManaway from New Zealand.\n\n[Personal Preference]\nPersonal Preference is a 1987 board game created by Donal Carlston that involves guessing the order in which a player prefers foods, activities, people, and other items compared to one another.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qbba0fc9d95",
  "kind": "yes/no",
  "text": "Tweet: Keanu reeves is killing his role in ozark season 3",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q4517ae0531",
  "kind": "yes/no",
  "text": "Claim: Acid Brass is a musical collaboration between Turner-Prize-winning artist Jeremy Deller and the award winning Williams Fairey Brass Band and based on fusing the music of a traditional brass band with acid house and Detroit techno, a type of techno music that generally includes the first techno productions by Detroit-based artists during the 1980s and early 1990s.\n\nPassages:\n\n[Detroit techno]\nDetroit techno is a type of techno music that generally includes the first techno productions by Detroit-based artists during the 1980s and early 1990s.\n\n[Acid Brass]\nAcid Brass is a musical collaboration between Turner-Prize-winning artist Jeremy Deller and the Williams Fairey Brass Band. The project is based on fusing the music of a traditional brass band with acid house and Detroit techno.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6811de5cb5",
  "kind": "yes/no",
  "text": "Claim: This English academic specializes in the same field as Christiane Desroches Noblecourt. The English man excavated Harageh and is known mainly for his works in Association that is named after the capital of Egypt.\n\nPassages:\n\n[Cairo]\nCairo ( ; Arabic: القاهرة‎ ‎ \"al-Qāhirah \", , Coptic: \"Kahire \") is the capital and largest city of Egypt.\n\n[Reginald Engelbach]\nReginald Engelbach (July 9, 1888 – February 26, 1946) was an English Egyptologist and engineer. He is mainly known for his works in the Egyptian Museum of Cairo, above all the compilation of a register of artifacts belonging of the museum.\n\n[Christiane Desroches Noblecourt]\nChristiane Desroches Noblecourt (] ; 17 November 1913 – 23 June 2011) was a French Egyptologist.\n\n[Harageh]\nReginald Engelbach excavated these cemeteries in 1913.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q29f6ce6cb4",
  "kind": "yes/no",
  "text": "Claim: Both the poet Maurice Newman and Macquarie University are from Australia.\n\nPassages:\n\n[Maurice Newman]\nMaurice Lionel Newman AC (born 20 April 1938, Ilford, England) is an Australian businessman who has served in a range of public roles, including as Chairperson of the Australian Broadcasting Corporation, chair of the board of the Australian Stock Exchange, Chancellor of Macquarie University, and a member of the Prime Minister's Business Advisory Council from September 2013 to September 2015.\n\n[Macquarie University]\nMacquarie University is a public research university based in Sydney, Australia, in the suburb of Macquarie Park.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qacae2a24ae",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I'm not entirely sure you -can- say the same thing non-sarcastically. I suppose... 'Constantly calling for lower targets is ridiculous.'",
   "@GainzyXBT Actually I've extrapolated based on the last daily candle and it turns out BTC will be sub-zero by December. The math doesn't lie."
  ]
 },
 {
  "qid": "qead7ae4a90",
  "kind": "yes/no",
  "text": "Claim: Port Macquarie is a larger New South Wales Town than Bonny Hills.\n\nPassages:\n\n[Port Macquarie]\nPort Macquarie is a coastal town in the local government area of Port Macquarie-Hastings. The town with its suburbs had a population of 45,698 in June 2016.\n\n[Bonny Hills, New South Wales]\nBonny Hills is a town in New South Wales, Australia about 30 minutes drive south of Port Macquarie. As of the 2011 census, it had a population of 2,870 people.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q90af74f675",
  "kind": "yes/no",
  "text": "Text: Imagine looking at your newborn baby girl and naming that shit Brogan",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q9e602102f3",
  "kind": "yes/no",
  "text": "Claim: Nick Grindé was born before a person involved with Saturday Night and Sunday Morning (film).\n\nPassages:\n\n[Karel Reisz]\nKarel Reisz (21 July 1926 – 25 November 2002) was a British filmmaker who was active in post–World War II Britain, and one of the pioneers of the new realist strain in British cinema during the 1950s and 1960s.\n\n[Nick Grinde]\nNick Grindé (January 12, 1893 – June 19, 1979) was an American film director and screenwriter.\n\n[Saturday Night and Sunday Morning (film)]\nSaturday Night and Sunday Morning is a 1960 British drama film directed by Karel Reisz and produced by Tony Richardson.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
