# A46 replay label-noise blind read RSBS09-blind_read-a9209673-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS09-blind_read-a9209673-004.json

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
  "qid": "q90c46bc4d5",
  "kind": "yes/no",
  "text": "Claim: A castle, which is near to Wallace's Cave, is located downstream relative to a castle south of Edinburgh\n\nPassages:\n\n[Hawthornden Castle]\nThe castle lies a mile to the east of Roslin at grid reference [ NT287637] , and is just downstream from Roslin Castle.\n\n[Roslin Castle]\nIt is located around 9 miles south of Edinburgh, on the north bank of the North Esk, only a few hundred metres from the famous Rosslyn Chapel.\n\n[Wallace's Cave]\nIt is also known as Hawthornden Castle Cave, after Hawthornden Castle which is nearby.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4d225df4f9",
  "kind": "yes/no",
  "text": "Post: an 8 year old just complimented my shoes in passing, what does that mean",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q2ec66a487f",
  "kind": "yes/no",
  "text": "Claim: The king, whose reign was the first included in the publication which Roger de Bankwell appears as a counsel in, was also known as Edward Longshanks and the Hammer of the Scots.\n\nPassages:\n\n[Roger de Bankwell]\nHe appears as a counsel in the Year book for 1340, in 1341 was appointed to a justiceship of the king's bench, and was one of those assigned to try petitions from Gascony, Wales, Ireland, Scotland, and 'other foreign parts ' between the years 1341 and 1347.\n\n[Year Books]\nThe Year Books are the modern English name that is now typically given to the earliest law reports of England. They are extant in a continuous series from 1268 to 1535, covering the reigns of King Edward I to Henry VIII.\n\n[Edward I of England]\nEdward I (17/18 June 1239 – 7 July 1307), also known as Edward Longshanks and the Hammer of the Scots (Latin: \"Malleus Scotorum\" ), was King of England from 1272 to 1307.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7fb24a42bb",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "People should care more about poverty and inequality than other less important matters.",
   "If only people would care as much about poverty and social equality the way they do jumping up and down for Team Remain or Team Leave."
  ]
 },
 {
  "qid": "qcdea68fd0d",
  "kind": "yes/no",
  "text": "Claim: Ernst & Young is the 220-year-old multinational professional services firm, headquartered in London, England, that is one of the \"Big Four\" accounting firms and is also a tenant in the hub of the \"Hub and Spoke Model\" where InfoPark Thrissur is one of the spokes.\n\nPassages:\n\n[Ernst &amp; Young]\nEY (formerly Ernst & Young) is a multinational professional services firm headquartered in London, England. EY is one of the largest professional services firms in the world and is one of the \"Big Four\" accounting firms.\n\n[InfoPark, Kochi]\nInfopark, Kochi (Malayalam: ഇൻഫോപാർക്ക് കൊച്ചി) is an information technology park situated in the city of Kochi, Kerala, India. The notable tenants in the park include native giants like Tata Consultancy Services, Cognizant, Wipro, IBS Software Services etc and foreign corporations like KPMG, Ernst & Young, EXL, Etisalat, UST Global, Nielsen Audio, Xerox, Conduent, Fingent etc.\n\n[InfoPark Thrissur]\nThis is the first information technology park in the state that has become operational under the 'Hub and Spoke Model', where InfoPark, Kochi acts as the hub and InfoPark Koratty as the spoke.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qcbfe7d6eba",
  "kind": "yes/no",
  "text": "Claim: Elijah Wood starred alongside Paul Hogan in a movie that features Jessica Wesson is a supporting role.\n\nPassages:\n\n[Flipper (1996 film)]\nFlipper is a 1996 adventure film remake of the 1963 film of the same name (which in turn begat a TV series that ran from 1964 to 1967), starring Paul Hogan and Elijah Wood.\n\n[Elijah Wood]\nHe is best known for his high-profile leading role as Frodo Baggins in Peter Jackson's epic film trilogy \"The Lord of the Rings\" (2001–03).\n\n[Jessica Wesson]\nShe is best known for her recurring role as Jennifer Sudarsky, Brad's (Zachery Ty Bryan) first girlfriend on the sitcom \"Home Improvement\", and having supporting roles in the Universal films \"Casper\" and \"Flipper\" in the 1990s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qfedf38592b",
  "kind": "yes/no",
  "text": "Claim: The 19th-century town of Tepelenë in Albania is located on the banks of the Vjosa River in Gjirokastër County. After a 2015 local government reform a village became part of its municipality. Ismet Toto was originally from this village.\n\nPassages:\n\n[Ismet Toto]\nIsmet Toto (Progonat, 1908 - Gjirokastër, 1937) was an Albanian bureaucrat, publicist, writer and revolutionary.\n\n[Progonat]\nProgonat is a village in the former Kurvelesh municipality, Gjirokastër County. At the 2015 local government reform it became part of the municipality Tepelenë.\n\n[Tepelenë]\nTepelenë (definite Albanian form: \"Tepelena\" ) is a town and a municipality in Gjirokastër County, in the south of Albania. The town is located on the left bank of the Vjosa River, about three kilometres downstream from its union with the Drino.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2e11aa418b",
  "kind": "yes/no",
  "text": "Claim: The Minister for Defence Industry is currently the member of the Australian House of Representatives from Sturt city.\n\nPassages:\n\n[Christopher Pyne]\nChristopher Maurice Pyne (born 13 August 1967) is an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the 1993 election.\n\n[Minister for Defence Industry]\nIn the Government of Australia, the Minister for Defence Industry is the Hon. Christopher Pyne {'1': \", '2': \", '3': \", '4': \"} since 19 July 2016.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2f07a61fd4",
  "kind": "yes/no",
  "text": "Claim: Bob Hoskins and Helen Mirren starred in the Irish gangster film in which this actor had one of his first roles. He later went on to star in Rifles Tv series which Martin Glyn Murray has a role in.\n\nPassages:\n\n[Sharpe's Rifles (TV programme)]\nShown on ITV in 1993, the adaptation stars Sean Bean, Daragh O'Malley and Assumpta Serna.\n\n[Martin Glyn Murray]\nMartin Glyn Murray (born 1 February 1966 in Helsingør, Denmark) is a Danish-born British actor who has played Mark Thompson in \"Families\" and he has also been in \"The Bill\", \"Sharpe\", \"Aristocrats\", \"Enigma\", \"Enemy at the Gates\", \"Captain Corelli's Mandolin\", \"Made in Estonia\", and \"Heartbeat\".\n\n[Daragh O'Malley]\nO'Malley first appeared in roles in the iconic films \"The Long Good Friday\" and \"Withnail and I\", leading guest roles in many UK television series including \"Tales of The Unexpected (TV Series)\", \"Waking The Dead\", \"Wire in the Blood\", \"Silent Witness\" and \"Vera\", and roles in Longitude, Cleopatra for ABC and The Magnificent Seven for CBS and in the US TV films 'Vendetta\", \"Camelot\" (TV Series) and \"Shaughnessy\".\n\n[The Long Good Friday]\nThe Long Good Friday is a British gangster film starring Bob Hoskins and Helen Mirren.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q02d0afd648",
  "kind": "yes/no",
  "text": "Claim: There is a small medieval castle made of mud in Scotland.\n\nPassages:\n\n[Castlebay]\nCastlebay (Scottish Gaelic: \"Bàgh a' Chaisteil\" ) is the main village and a community council area on the island of Barra in the Outer Hebrides, Scotland.\n\n[Kisimul Castle]\nKisimul Castle (Scottish Gaelic: \"Caisteal Chiosmuil\" ) and also known as Kiessimul Castle, is a small medieval castle located on a small island off Castlebay, Barra, in the Outer Hebrides, Scotland.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q17f83eb669",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "I wish my body would let me sleep.",
   "It would be nice if my body would let me sleep..."
  ]
 },
 {
  "qid": "q2e75c2cb46",
  "kind": "yes/no",
  "text": "Claim: Animated feature Monsters, Inc. Laugh Floor replaced the 1992 film The Timekeeper shown at three Disney parks.\n\nPassages:\n\n[Monsters, Inc. Laugh Floor]\nMonsters, Inc. Laugh Floor is an attraction within the Magic Kingdom, a theme park at Walt Disney World Resort. It opened on April 2, 2007 within the park's Tomorrowland section, where it replaced the Circle-Vision attraction The Timekeeper.\n\n[The Timekeeper]\nThe Timekeeper (also known as From Time to Time and Un Voyage à Travers le Temps) was a 1992 Circle-Vision 360° film that was presented at three Disney parks around the world.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q04e02d3bda",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I only got 2.5 hours of sleep last night and it wasn’t enough",
   "It’s been a blissful 2.5 hours of sleep tonight"
  ]
 },
 {
  "qid": "q8f7f3fef8c",
  "kind": "yes/no",
  "text": "Claim: Bauhinia is a genus of more species this genus. This genus contains the species Cestrum diurnum.\n\nPassages:\n\n[Bauhinia]\nBauhinia is a genus of more than 500 species of flowering plants in the subfamily Cercidoideae of the large flowering plant family Fabaceae, with a pantropical distribution.\n\n[Cestrum]\nCestrum is a genus of - depending on authority - 150-250 species of flowering plants in the family Solanaceae.\n\n[Cestrum diurnum]\nCestrum diurnum (Din Ka Raja) is a species of \"Cestrum\", native to the West Indies.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qff9e833d97",
  "kind": "yes/no",
  "text": "Post: Honestly this weather is the best birthday present I could ever receive",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q2271c2cb21",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@raerenyse Easily one of the worst and most damaging takes for both trans AND cis women I have seen thus far. Congrats on reaching new levels of awful lmao",
   "Easily one of the worst and most damaging takes for both trans AND cis women I have seen thus far. You have surprised me by reaching new depths of depravity via tweeting this."
  ]
 },
 {
  "qid": "q5075afaeeb",
  "kind": "yes/no",
  "text": "Claim: Sarah Jessica Parker sings the lead song in a 2010 romantic comedy starring Jessica Alba, Kathy Bates, and Bradley Cooper.\n\nPassages:\n\n[Valentine's Day (2010 film)]\nValentine's Day is a 2010 American romantic comedy film directed by Garry Marshall. The film consists of an ensemble cast led by Jessica Alba, Kathy Bates, Jessica Biel, Bradley Cooper, Eric Dane, Patrick Dempsey, Héctor Elizondo, Jamie Foxx, Jennifer Garner, Topher Grace, Anne Hathaway, Ashton Kutcher, Queen Latifah, Taylor Lautner, George Lopez, Shirley MacLaine, Emma Roberts, Julia Roberts, Carter Jenkins, and Taylor Swift in her film debut.\n\n[Stay Here Forever]\nIt was released to country radio in January 2010 and as a music download on February 9, 2010, and serves as the lead song for the movie \"Valentine's Day\", as well as the lead-off single to Jewel's second country album, \"Sweet and Wild\", which was released on June 8, 2010 via Valory Music Group.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0365b1407f",
  "kind": "yes/no",
  "text": "Claim: Huai'an and Qian'an, Hebei are both Chinese cities.\n\nPassages:\n\n[Huai'an]\nHuai'an (), formerly called Huaiyin () until 2001, is a prefecture-level city in central Jiangsu province of Eastern China.\n\n[Qian'an, Hebei]\nQian'an () is a city in the northeastern part of Hebei province in North China.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4718fb50f3",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "It was almost 70 degrees today but no, global warming doesn't exist 😒",
   "Global warming is why it is 70 degrees outside"
  ]
 },
 {
  "qid": "qd7e208e48e",
  "kind": "yes/no",
  "text": "Claim: Mawson is an electoral district that includes the wine regional around the town, where Mollydooker Wines Pty Ltd is based, south of Adelaide.\n\nPassages:\n\n[Electoral district of Mawson]\nMawson is an electoral district of the House of Assembly in the Australian state of South Australia. It covers most of the outer southern suburbs of the City of Onkaparinga, including Hackham, Hackham West, Huntfield Heights, Noarlunga Downs, Old Noarlunga, Onkaparinga Hills and Seaford Heights, the regional shopping centre area at Noarlunga Centre, parts of Woodcroft, and the southern wine region around McLaren Vale and Willunga.\n\n[McLaren Vale]\nMcLaren Vale is a wine region approximately 35 km south of Adelaide in South Australia.\n\n[Mollydooker Wines]\nMollydooker Wines Pty Ltd is based in the McLaren Vale Area of Australia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd33db6f8b0",
  "kind": "yes/no",
  "text": "Claim: Federated Auto Parts 400 is an annual sporting event stock car race held at the Richmond Raceway in Richmond, Virginia, being the second of two races in the spring. The first one of these two races was sponsored from 2007 to 2011 by a brand that is owned by concert pianist Diageo. Nine of the sporting event races were held at Middle Georgia Raceway between 1966 and 1971.\n\nPassages:\n\n[Federated Auto Parts 400]\nThe Federated Auto Parts 400 is an annual Monster Energy NASCAR Cup Series stock car race held at the Richmond Raceway in Richmond, Virginia, being the second of two races with the first one being the Toyota Owners 400 in the spring.\n\n[Middle Georgia Raceway]\nNine NASCAR Grand National (now Monster Energy NASCAR Cup Series) races were held at the track between 1966 and 1971.\n\n[Crown Royal]\nCrown Royal is a blended Canadian whisky owned by Diageo, which purchased it when the Seagram portfolio was dissolved in 2000.\n\n[Toyota Owners 400]\nFrom 2007 to 2011, former race title sponsor Crown Royal named the race after the winner of an essay contest during Daytona Speedweeks.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q3a18c262c0",
  "kind": "yes/no",
  "text": "Claim: It was reported that Hess took an illegal flight to Scotland in May 1941. This report was the reason that the editor of the publication, that was published by Fredric Warburg, stopped serving Hitler in 1941.\n\nPassages:\n\n[Mein Kampf]\nThe book was edited by Hitler's deputy Rudolf Hess.\n\n[Fredric Warburg]\nOther notable publications included \"The Third Eye\" by Lobsang Rampa, Pierre Boulle's \"The Bridge over the River Kwai\", Adolf Hitler's \"Mein Kampf\" and William Shirer's \"The Rise and Fall of the Third Reich\".\n\n[Karlheinz Pintsch]\nIt fell to him to report Hess's illegal May 1941 flight to Scotland to Hitler and his recollections and notes have been the subject of debate by historians.\n\n[Rudolf Hess]\nAppointed Deputy Führer to Adolf Hitler in 1933, he served in this position until 1941, when he flew solo to Scotland in an attempt to negotiate peace with the United Kingdom during World War II. He was taken prisoner and eventually was convicted of crimes against peace, serving a life sentence until his suicide.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf1b9c4743b",
  "kind": "yes/no",
  "text": "Claim: Harlan County, USA was directed and produced by Barbara Kopple, She also directed the 1969 festival production, along with Michael Wadleigh. Harlan County and another of her films have the documentary film in common.\n\nPassages:\n\n[Harlan County, USA]\nDirected and produced by Barbara Kopple, who has long been an advocate of workers' rights, \"Harlan County, U.S.A.\" is less ambivalent in its attitude toward unions than her later \"American Dream\", the account of the Hormel Foods strike in Austin, Minnesota in 1985-86.\n\n[American Dream (film)]\nAmerican Dream is a 1990 \"cinéma vérité\" documentary film directed by Barbara Kopple and co-directed by Cathy Caplan, Thomas Haneke, and Lawrence Silk.\n\n[Michael Wadleigh]\nMichael Wadleigh, also known as Michael Wadley (born September 24, 1942 in Akron, Ohio), is an American film director and cinematographer renowned for his groundbreaking documentary of the 1969 Woodstock Festival, \"Woodstock\".\n\n[Woodstock (film)]\nWoodstock is a 1970 documentary film of the watershed counterculture Woodstock Festival which took place in August 1969 near Bethel, New York. \"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe3c24030b9",
  "kind": "yes/no",
  "text": "Claim: The Volkswagen CrossBlue competed with the Hondo crossover SUV introduced in 2002.\n\nPassages:\n\n[Volkswagen CrossBlue]\nIn the American and Canadian markets, its targeted competitors are the Toyota Highlander, Toyota 4Runner, Ford Explorer, and Honda Pilot.\n\n[Honda Pilot]\nThe Honda Pilot is a mid-size crossover SUV manufactured by Honda and introduced in 2002.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q21e0641063",
  "kind": "yes/no",
  "text": "Claim: Blast Vegas starred the actor and musician who played the title character on FOX's Malcolm in the Middle.\n\nPassages:\n\n[Blast Vegas]\nIt first aired on the Syfy channel on July 18, 2013, and stars Frankie Muniz, Barry Bostwick, and Maggie Castle.\n\n[Frankie Muniz]\nHe is best known for playing the title character in the Fox television family sitcom \"Malcolm in the Middle\", which earned him an Emmy Award nomination and two Golden Globe Award nominations.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q88040b4189",
  "kind": "yes/no",
  "text": "Claim: Dougray Scott starred in a 2015 zombie film with Northern Irish actor.\n\nPassages:\n\n[Martin McCann (actor)]\nMartin \"Marty\" McCann (born 20 July 1983) is an actor from Northern Ireland.\n\n[The Rezort]\nThe Rezort is a 2015 British zombie horror film directed by Steve Barker and written by Paul Gerstenberger. It stars Dougray Scott, Jessica De Gouw and Martin McCann.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q81f796a6e4",
  "kind": "yes/no",
  "text": "Claim: The founder of the Trussed Concrete Steel Company was raised in Detroit, Michigan.\n\nPassages:\n\n[Trussed Concrete Steel Company]\nThe Trussed Concrete Steel Company was a company founded by Julius Kahn, an engineer and inventor.\n\n[Julius Kahn (inventor)]\nHe was raised in Detroit, Michigan.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q213503abb3",
  "kind": "yes/no",
  "text": "Claim: Gwendoline Christie was born in 1978 and starred in Star Wars: The Last Jedi.\n\nPassages:\n\n[Gwendoline Christie]\nGwendoline Christie (born 28 October 1978) is an English actress and model.\n\n[Star Wars: The Last Jedi]\nIt stars Mark Hamill, Carrie Fisher, Adam Driver, Daisy Ridley, John Boyega, Oscar Isaac, Lupita Nyong'o, Domhnall Gleeson, Anthony Daniels, Gwendoline Christie, and Andy Serkis in returning roles.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1f87445759",
  "kind": "yes/no",
  "text": "Text: @inkofreality @StrangerTings1 @nytimes You're so close to understanding baseline biasing. You can get there, I believe in you!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qb0b4055331",
  "kind": "yes/no",
  "text": "Claim: Mike Humphreys played collegiately for the team that represents Texas Tech University in NCAA Division I baseball season college baseball, and has The Law as its home stadium.\n\nPassages:\n\n[Dan Law Field at Rip Griffin Park]\nDan Law Field at Rip Griffin Park, nicknamed \"The Law\", is the home stadium of the Texas Tech Red Raiders baseball team in Lubbock, Texas.\n\n[Texas Tech Red Raiders baseball]\nThe Texas Tech Red Raiders baseball team represents Texas Tech University in NCAA Division I college baseball.\n\n[Mike Humphreys]\nHumphreys played collegiately for the Texas Tech Red Raiders",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfa45b2fee9",
  "kind": "yes/no",
  "text": "Claim: Jhené Aiko is an American singer who appeared in music videos for R&B group B2K and also featured on the mixtape by American rapper Big Sean. A production team, who helped on the Tyga album Hotel California, helped produce the mixtape.\n\nPassages:\n\n[Hotel California (Tyga album)]\nThe album features guest appearances from Lil Wayne, 2 Chainz, The Game, Jadakiss, while the production on the album was handled by DJ Mustard, Detail, Cool & Dre, David D.A. Doman, Mars of 1500 or Nothin', The Olympicks, SAP and Ryan Hunt, among others.\n\n[The Olympicks]\nThe group originated in Detroit, Michigan and have been involved in the production of various projects within the hip-hop music industry, including Lil Wayne's \"I Am Not a Human Being\", Rick Ross' \"Teflon Don\", Triple C's \"Custom Cars & Cycles\", DJ Khaled's \"Kiss The Ring\", and most recently, Big Sean's \"Detroit\" mixtape.\n\n[Jhené Aiko]\nShe embarked on her music career contributing vocals and appearing in several music videos for R&B group B2K.\n\n[Detroit (mixtape)]\nAmerican singers includes Chris Brown, Jhené Aiko, James Fauntleroy and Mike Posner.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2a5a3ab9d9",
  "kind": "yes/no",
  "text": "Claim: Canadian author William P. Young hit the New York Times Best Seller list in 2017, with a book published 10 year prior.\n\nPassages:\n\n[The New York Times Fiction Best Sellers of 2017]\nThis is a list of adult fiction books that topped \"The New York Times\" Fiction Best Seller list in 2017, in the Combined Print & E-Book Fiction category. So far, the most frequent weekly best seller of the year is \"Camino Island\" by John Grisham with 5 weeks at the top of the list, followed by \"The Shack\" by William P. Young with 4 weeks.\n\n[The Shack]\nThe Shack is a novel by Canadian author William P. Young that was published in 2007.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6a19c5101e",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@Dancruz07 Sureeeeeee you do",
   "I could've replied \"You do not despise me, you're my best friend.\""
  ]
 },
 {
  "qid": "q2921a8efdf",
  "kind": "yes/no",
  "text": "Claim: This artist and the producer of Welcome to Venice are not from the same country. He released the song When I Was Your Girl.\n\nPassages:\n\n[Welcome to Venice]\nIt was produced by Mike Muir and features cover art by Michael Seiff, who would go on to do art for the three other original Suicidal Records releases.\n\n[When I Was Your Girl]\n\"When I Was Your Girl\" is a song by English singer-songwriter Alison Moyet, released as the first single from her eighth studio album, \"The Minutes\" (2013), which debuted at number five in the UK Albums Chart on 12 May 2013.\n\n[Alison Moyet]\nGeneviève Alison Jane Moyet ( ; born 18 June 1961) is an English singer, songwriter and performer noted for her bluesy contralto voice.\n\n[Mike Muir]\nMichael Allen \"Mike\" Muir (born March 14, 1963) is the lead vocalist of the Venice, California crossover thrash bands Suicidal Tendencies, Los Cycos and the funk metal band Infectious Grooves.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5edc7293b0",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "The face that 'black and white thinking' is considered a mental disorder symptom and yet remains a pillar of American culture is hypocritical.",
   "I find it hilarious that ‘black and white’ or ‘all or nothing’ thinking is considered a cognitive distortion and is a symptom of several disorders, and yet it remains a pillar of American (and Western) culture. It’s almost like…. our culture is toxic 🤔"
  ]
 },
 {
  "qid": "qcc193129c1",
  "kind": "yes/no",
  "text": "Text: I've been doing physics for 40 minutes I think I deserve a break 😂😂😂😭 I'm never going to get it all done at this rate",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q43d28b4034",
  "kind": "yes/no",
  "text": "Claim: The 247 Cherry building is adjacent to the building that is higher than this building, artist and mechanic Stephen M. Ross lives and works there.\n\nPassages:\n\n[247 Cherry]\nThe building will be adjacent One Manhattan Square.\n\n[One Manhattan Square]\nOne Manhattan Square (also known as 227 Cherry Street or 250 South Street) is a residential skyscraper project being developed by Extell Development Company in Two Bridges, Manhattan, New York City. The building will stand 80 stories or 850 feet (259 m) above the street, and will possibly have a new supermarket in the tower's base.\n\n[Stephen M. Ross]\nRelated is best known for developing the Time Warner Center, where Ross lives and works, as well as the Hudson Yards Redevelopment Project.\n\n[Time Warner Center]\nDeveloped by The Related Companies and AREA Property Partners (formerly known as Apollo Real Estate Advisors), its design by David Childs and Mustafa Kemal Abadan of Skidmore, Owings & Merrill, consists of two 750 ft twin towers bridged by a multi-story atrium containing upscale retail shops.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa53952ba9d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "@sdeditgirl You should know a true Oregonian doesn't use umbrellas!",
   "\"I really will need an umbrella in Oregon.\""
  ]
 },
 {
  "qid": "q7054544e1e",
  "kind": "yes/no",
  "text": "Claim: Massimiliano Antonio \"Max\" Cavalera played in the band Soulfly not Billy Idol.\n\nPassages:\n\n[Max Cavalera]\nMassimiliano Antonio \"Max\" Cavalera (] , born August 4, 1969) is a Brazilian singer, guitarist, and songwriter who currently plays in heavy metal bands Soulfly, Cavalera Conspiracy, and Killer Be Killed.\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe9eae6ec3c",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Wow it's almost as if it's their literal job to have a lot of knowledge about a wide array of subjects.. Funny that https://t.co/NGi02vXxnK",
   "\"It's literally their job to have a lot of knowledge on a wide array of subjects\""
  ]
 },
 {
  "qid": "qb7c4a2fedf",
  "kind": "yes/no",
  "text": "Claim: According to this manuscript written in a language spoken between the 8th and 16th centuries Friso was a leader of a group of Frisian colonists who had been settled in the Sabah for well over a millennium when they were discovered by Alexander the Great.\n\nPassages:\n\n[Old Frisian]\nOld Frisian is a West Germanic language spoken between the 8th and 16th centuries in the area between the Rhine and Weser on the European North Sea coast.\n\n[Oera Linda Book]\nThe Oera Linda Book is a manuscript written in a form of Old Frisian, purporting to cover historical, mythological, and religious themes of remote antiquity, from 2194 BCE to 803 CE.\n\n[Friso]\nAccording to Martinus Hamconius in his 17th century chronicle \"Frisia seu de viris rebusque illustribus\", and also the 19th century Oera Linda Book, Friso was a leader of a group of Frisian colonists who had been settled in the Punjab for well over a millennium when they were discovered by Alexander the Great.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8b3f68dc19",
  "kind": "yes/no",
  "text": "Claim: Paul Melba has made several other television appearances, including an British version of a TV show. The host of this television show hosted 23 shows in his career.\n\nPassages:\n\n[Punchlines]\nThe show itself was based on a failed 1979 American game show pilot of the same name hosted by Bill Cullen for which in turn was a reboot of another American game show from 1966-69 called \"Eye Guess\".\n\n[Bill Cullen]\nHis biggest claim to fame was as a game show host; over the course of his career, he hosted 23 shows, and earned the nickname \"Dean of Game Show Hosts\".\n\n[Paul Melba]\nIn addition to appearances in clubs and theatres he has made several other television appearances, including \"Punchlines\" and eight editions of \"The Val Doonican Show\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3da963964b",
  "kind": "yes/no",
  "text": "Claim: Larry King's ex-wife and a male player shared being known for playing tennis. This male player was defeated in the 1990 Newsweek Champions Cup – Doubles final with his partner Jim Grabb.\n\nPassages:\n\n[Patrick McEnroe]\nPatrick John McEnroe (born July 1, 1966) is a former professional tennis player and the former captain of the United States Davis Cup team.\n\n[Larry King (tennis)]\nLarry King (born January 30, 1945) is an American attorney, a real estate broker, a promoter, one of the founders of World Team Tennis, and the former husband of tennis star Billie Jean King.\n\n[Billie Jean King]\nBillie Jean King (\"née\" Moffitt; born November 22, 1943) is an American former World No. 1 professional tennis player.\n\n[1990 Newsweek Champions Cup – Doubles]\nBecker partnered Guy Forget, and they won the title, defeating Jim Grabb and Patrick McEnroe 4–6, 6–4, 6–3 in the final.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q73ab3bb918",
  "kind": "yes/no",
  "text": "Claim: EasyJet Switzerland the Norwegian low-cost airline operated out of the airport that is also connected to by a British express coach operator.\n\nPassages:\n\n[EasyJet Switzerland]\nEasyJet Switzerland SA, styled as easyJet, is a Swiss low-cost airline based in Meyrin, Geneva.\n\n[EasyBus]\nEasyBus is a British express coach operator connecting the city centres of London and Manchester with their respective main airports as well providing services from Geneva Airport (where EasyJet Switzerland is based) to nearby communities.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q37309018c4",
  "kind": "yes/no",
  "text": "Claim: The Spanish Armada was a Spanish fleet of 130 wooden ships The San Juan de Sicilia formed the ill-fate.\n\nPassages:\n\n[San Juan de Sicilia]\nThe San Juan de Sicilia was one of the 130 ships that formed the ill-fated Spanish Armada of 1588.\n\n[Spanish Armada]\nThe Spanish Armada (Spanish: \"Grande y Felicísima Armada\" , literally \"Great and Most Fortunate Navy\") was a Spanish fleet of 130 ships that sailed from La Coruña in August 1588, under the command of the Duke of Medina Sidonia with the purpose of escorting an army from Flanders to invade England.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb255af1a16",
  "kind": "yes/no",
  "text": "Tweet: My boys Sam &amp; Ben Haigh (8, 4) are huge fans of yours and would like to wish you a happy birthday all the way from England, ps cant wait to try the colour challenge with the boys during lockdown great ideas to keep them busy ! x @Preston",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q102e539e2c",
  "kind": "yes/no",
  "text": "Claim: The American Pre-Code comedy film featuring an American actress, dancer, and singer, widely known for performing in films, tv shows and RKO's musical films, was released in 1932.\n\nPassages:\n\n[Ginger Rogers]\nGinger Rogers (born Virginia Katherine McMath; July 16, 1911 – April 25, 1995) was an American actress, dancer, and singer, widely known for performing in films and RKO's musical films, partnered with Fred Astaire.\n\n[Hat Check Girl]\nHat Check Girl is a 1932 American Pre-Code comedy film directed by Sidney Lanfield and written by Barry Conners and Philip Klein. The film stars Sally Eilers, Ben Lyon, Ginger Rogers and Monroe Owsley.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd485533642",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "@BIGRXD12 ah yes, people with eating disorders, famous for easily being able to not worry about their weight",
   "It may be difficult for someone with an eating disorder to avoid worrying about their weight."
  ]
 },
 {
  "qid": "qa7c7d203ca",
  "kind": "yes/no",
  "text": "Claim: This band released Echelons in March 1987. They were formed before the band Aaroh.\n\nPassages:\n\n[For Against]\nFor Against is a United States post-punk/dream pop band from Lincoln, Nebraska. Despite numerous lineup shuffles and some periods of dormancy, the band has produced material steadily from its 1984 inception to the present.\n\n[Aaroh]\nAaroh (Urdu: آروح, literal English translation: \"the ascending scale in eastern classical music\") is an alternative rock band from Karachi, Sindh, Pakistan, formed in 1998.\n\n[Echelons]\nEchelons is the debut studio album by American rock band For Against, released in 1987 by record label Independent Project.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q1a8c3788ec",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "My tinnitus is so annoying",
   "Tinnitus is my favourite thing ever I love it. So loud so atmospheric https://t.co/mNJw5GvPzy"
  ]
 }
]
