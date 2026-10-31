# A46 replay label-noise blind read RSAS00-blind_read-a93c91a5-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS00-blind_read-a93c91a5-005.json

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
  "qid": "q29b70aa1cc",
  "kind": "yes/no",
  "text": "Claim: The singer of \"Funny Face\" was born on September 10, 1896.\n\nPassages:\n\n['S Wonderful]\nIt was introduced in the Broadway musical \"Funny Face\" (1927) by Adele Astaire and Allen Kearns.\n\n[Adele Astaire]\nAdele, Lady Charles Cavendish (born Adele Marie Austerlitz; September 10, 1896 – January 25, 1981) was an American dancer, stage actress and singer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc595f41ecf",
  "kind": "yes/no",
  "text": "Claim: This One's for the Children had lead vocals by an American singer and songwriter.\n\nPassages:\n\n[This One's for the Children]\nThe lead vocals were sung by Jordan Knight and Donnie Wahlberg.\n\n[Donnie Wahlberg]\nDonald Edmond Wahlberg Jr. (born August 17, 1969) is an American singer, songwriter, actor, record producer, and film producer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd7f6130dab",
  "kind": "yes/no",
  "text": "Claim: El Paso International Airport and Tucson International Airport, are public airports.\n\nPassages:\n\n[El Paso International Airport]\nEl Paso International Airport (IATA: ELP, ICAO: KELP, FAA LID: ELP) is a public airport four miles (6 km) northeast of downtown El Paso, in El Paso County, Texas, United States.\n\n[Tucson International Airport]\nTucson International Airport (IATA: TUS, ICAO: KTUS, FAA LID: TUS) is a public joint civil-military airport owned by the City of Tucson 8 mi south of downtown Tucson, in Pima County, Arizona.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0f0bc26fc7",
  "kind": "yes/no",
  "text": "Claim: The man who appointed Joseph D. Morelle as Majority Leader is a former lawyer. He previously held the seat now held by the individual that defeated Alice Cancel in 2016.\n\nPassages:\n\n[Alice Cancel]\nIn 2016, Cancel was defeated in the Democratic primary for her seat by Yuh-Line Niou.\n\n[Joseph D. Morelle]\nSpeaker Sheldon Silver appointed him as Majority Leader of the New York State Assembly in January 2013.\n\n[Sheldon Silver]\nSheldon \"Shelly\" Silver (born February 13, 1944) is a former lawyer and Democratic Party politician from New York City, who rose to become the powerful Speaker of the New York State Assembly in 1994 until his arrest on federal corruption charges in 2015.\n\n[Yuh-Line Niou]\nShe is a Democratic Party member of the New York State Assembly for the 65th district, the seat previously held by Sheldon Silver.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8a6181da1f",
  "kind": "yes/no",
  "text": "Claim: The 2000 French crime thriller starred the writer and director Virginie Despentes and Coralie Trinh Thi.\n\nPassages:\n\n[Baise-moi]\nBaise-moi (\"Fuck me \") is a 2000 French crime thriller film with elements of a rape and revenge film written and directed by Virginie Despentes and Coralie Trinh Thi and starring Karen Lancaume and Raffaëla Anderson.\n\n[Coralie Trinh Thi]\nCoralie Trinh Thi (born April 11, 1976) is a former pornographic actress and French author, also known for writing and directing with Virginie Despentes the film \"Baise-moi\" (2000).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q337286b036",
  "kind": "yes/no",
  "text": "Text: Anyone else with AT&amp;T have no cell service?",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb080f7dc53",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "People should care more about poverty and inequality than other less important matters.",
   "If only people would care as much about poverty and social equality the way they do jumping up and down for Team Remain or Team Leave."
  ]
 },
 {
  "qid": "q15ea06c84e",
  "kind": "yes/no",
  "text": "Claim: Savenac Nursery was created by Elers Koch, of the Forest Service, who also helped fight the Great Fire of 1910, commonly referred to as the Big Blowup, the Big Burn, or the Devil's Broom fire.\n\nPassages:\n\n[Great Fire of 1910]\nThe Great Fire of 1910 (also commonly referred to as the Big Blowup, the Big Burn, or the Devil's Broom fire) was a wildfire in the western United States that burned about 3000000 acre in northeast Washington, northern Idaho, and western Montana.\n\n[Savenac Nursery Historic District]\nSavenac Nursery Historic District is located near Haugan in Mineral County, Montana. The nursery was created by Elers Koch, of the Forest Service, who also helped fight the Great Fire of 1910 that destroyed much of the Rocky Mountains in the northern part of USA, including the nursery.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb904aa4510",
  "kind": "yes/no",
  "text": "Claim: Iowa State Cyclones is a founding member of the Big 12 Conference and competes in NCAA Division I, fielding 16 varsity teams, and had an American college wrestling icon considered one of the best American amateur wrestlers in recent history.\n\nPassages:\n\n[Iowa State Cyclones]\nThe Iowa State Cyclones are the athletic teams that represent Iowa State University.\n\n[Cael Sanderson]\nHe is considered one of the best American amateur wrestlers in recent history.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4451a78fe7",
  "kind": "yes/no",
  "text": "Claim: Foday Saybana Sankoh was the founder and leader of the Sierra Leone rebel group Revolutionary United Front (Sankoh) during the conflict involving the Mende ethnic group that lasted for eleven years.\n\nPassages:\n\n[Civil Defence Forces]\nThe Civil Defense Forces (CDF) was a paramilitary organization that fought in the Sierra Leone Civil War (1991–2002). Much of the CDF was made up of the Kamajors group, which is part of the larger Mende ethnic group.\n\n[Sierra Leone Civil War]\nThe Sierra Leone Civil War (1991–2002) began on 23 March 1991 when the Revolutionary United Front (RUF), with support from the special forces of Charles Taylor’s National Patriotic Front of Liberia (NPFL), intervened in Sierra Leone in an attempt to overthrow the Joseph Momoh government. The resulting civil war lasted 11 years, enveloped the country, and left over 50,000 dead.\n\n[Foday Sankoh]\nFoday Saybana Sankoh (17 October 1937 – 29 July 2003) was the founder and leader of the Sierra Leone rebel group Revolutionary United Front (RUF) in the 11-year-long Sierra Leone Civil War, starting in 1991 and ending in 2002.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q70c066a3c8",
  "kind": "yes/no",
  "text": "Post: Just want to say well done to every single person who has received their A Level results today ❤️",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q90ed402aeb",
  "kind": "yes/no",
  "text": "Claim: The BMW hatchback car introduced in November 2000 in the former Morris plant was three-door.\n\nPassages:\n\n[Mini Hatch]\nThe Mini Hatch, stylized as MINI hatch or MINI Hardtop in the US, also known as Mini Cooper or Mini One or simply the Mini, is a three-door hatchback first introduced in late 2000, with a second generation launched in 2006 and a third generation model launched in 2014.\n\n[Austin Maestro]\nThe car was produced at the former Morris plant in Cowley, Oxford. Today, the redeveloped factory produces the BMW Mini.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q90d3dedbfa",
  "kind": "yes/no",
  "text": "Claim: The actor that is linked to both the American Revolution film that has Hal Stalmaster in the lead role, and Magic Kingdom is Walt Disney.\n\nPassages:\n\n[Johnny Tremain (film)]\nJohnny Tremain is a 1957 film made by Walt Disney Productions, based on the 1944 Newbery Medal-winning children's novel of the same name by Esther Forbes, retelling the story of the years in Boston, Massachusetts prior to the outbreak of the American Revolution.\n\n[Hal Stalmaster]\nHarry Lapidus Stalmaster, known as Hal Stalmaster (born March 29, 1940), is an American former actor, known for his lead role in the 1957 Walt Disney film of the American Revolution \"Johnny Tremain\", based on the 1943 Esther Forbes novel of the same name.\n\n[Magic Kingdom]\nInitialized by Walt Disney and designed by WED Enterprises, its layout and attractions are based on Disneyland Park in Anaheim, California, and is dedicated to fairy tales and Disney characters.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qde35266366",
  "kind": "yes/no",
  "text": "Claim: George Palmer Putnam, was an American publisher, author and explorer, known for his marriage to Amelia Earhart, the American aviation pioneer and author, and the first female aviator to fly solo across the northern Atlantic Ocean.\n\nPassages:\n\n[George P. Putnam]\nKnown for his marriage to (and being the widower of) Amelia Earhart, he had also achieved fame as one of the most successful promoters in the United States during the 1930s.\n\n[Amelia Earhart]\nAmelia Mary Earhart ( , born July 24, 1897; disappeared July 2, 1937) was an American aviation pioneer and author.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0588587dfb",
  "kind": "yes/no",
  "text": "Post: just impulse bought a mandolin and in 3-5 buisness days i will impulse learn some jigs",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qb10a3020e7",
  "kind": "yes/no",
  "text": "Claim: The star of the show, in which Ramsay Gilderdale starre, was born in 1959.\n\nPassages:\n\n[Blackadder's Christmas Carol]\nIt is set between \"Blackadder the Third\" (1987) and \"Blackadder Goes Forth\" (1989), and is narrated by Hugh Laurie.\n\n[Ramsay Gilderdale]\nHe also appeared in \"Rumpole of the Bailey\" and \"Blackadder's Christmas Carol\".\n\n[Hugh Laurie]\nJames Hugh Calum Laurie, {'1': \", '2': \", '3': \", '4': \"} ( ; born 11 June 1959) is an English actor, director, musician, singer, comedian, and author.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q21e5d0a00b",
  "kind": "yes/no",
  "text": "Claim: St Cyrpian's Anglican Church is approximately 128 mi from London.\n\nPassages:\n\n[Nottingham]\nNottingham ( ) is a city and unitary authority area in Nottinghamshire, England, 128 mi north of London, in the East Midlands.\n\n[St Cyprian's Church, Sneinton]\nSt Cyprian's Church, Sneinton is a parish church in the Church of England in Sneinton, Nottingham.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfca5f4b1c3",
  "kind": "yes/no",
  "text": "Claim: The star of Oh, Dear Augustine and Brian Robbins are both actors and film producers.\n\nPassages:\n\n[Oh, Dear Augustine]\nOh, Dear Augustine (German:Oh, du lieber Augustin) is a 1922 Austrian silent film directed by H.K. Breslauer and starring Willi Forst.\n\n[Willi Forst]\nWilli Forst, born Wilhelm Anton Frohs (7 April 1903 – 11 August 1980) was an Austrian actor, screenwriter, film director, film producer and singer.\n\n[Brian Robbins]\nBrian Levine (born November 22, 1963), best known as Brian Robbins, is an American actor, film director, film producer, television director, television producer and occasional screenwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q515f44a0f5",
  "kind": "yes/no",
  "text": "Claim: The jet airliner with which this aircraft, that the General Electric GE9X engine is being developed for, was intended to compete has many seats.\n\nPassages:\n\n[Airbus A350 XWB]\nIts variants seat 280 to 366 passengers in typical three-class seating layouts.\n\n[Boeing 777X]\nIt is intended to compete with the Airbus A350.\n\n[General Electric GE9X]\nThe General Electric GE9X is a high-bypass turbofan aircraft engine under development by GE Aviation for the Boeing 777X.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q531c7dfb34",
  "kind": "yes/no",
  "text": "Claim: Actor Chen Yi was born in an area of China. This area, not the city containing the walled-in Qiezihe District, is located in Hunan province.\n\nPassages:\n\n[Huaihua]\nHuaihua () is a prefecture-level city in the south western Hunan, China.\n\n[Qiezihe District]\nIt is under the jurisdiction of the prefecture-level city of Qitaihe.\n\n[Cheng Yi (actor)]\nBorn in Huaihua, Hunan, China, he made his television debut in Chinese television drama \"Beauty World\" (2011) and graduated from Central Academy of Drama in 2012.\n\n[Qitaihe]\nQitaihe () is a prefecture-level city in eastern Heilongjiang province, People's Republic of China.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0536aa0fcf",
  "kind": "yes/no",
  "text": "Claim: The year of the event which occurred first out of when Beecher's Handmade Cheese was founded, and when Pike Place Market opened is 1907.\n\nPassages:\n\n[Pike Place Market]\nPike Place Market is a public market overlooking the Elliott Bay waterfront in Seattle, Washington, United States. The Market opened August 17, 1907, and is one of the oldest continuously operated public farmers' markets in the United States.\n\n[Beecher's Handmade Cheese]\nBeecher's Handmade Cheese is an artisan cheesemaker and retail shop with locations in the Pike Place Market, Seattle, Washington and New York City's Flatiron District. The company was founded by Kurt Beecher Dammeier in 2003 and opened in the Pike Place Market after Dammeier obtained a difficult to obtain storefront lease in the Market.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q58263c7814",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Please do not break the rules for christmas and risk serious fines or killing loved ones. Please stay home.",
   "Yes you can break all the rules for Christmas and risk serious fines and killing your loved ones with a deadly virus OR you could ✨stay at home✨"
  ]
 },
 {
  "qid": "qca525dfad9",
  "kind": "yes/no",
  "text": "Post: why is it so hard to find tshirts with cool wizards on them",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd26b212bd3",
  "kind": "yes/no",
  "text": "Claim: Lloyd Kaufman's award-winning co-director on Sgt. Kabukiman N.Y.P.D., and Roland Emmerich, do not both direct comedic horror films.\n\nPassages:\n\n[Roland Emmerich]\nHe began his work in the film industry by directing the film \"The Noah's Ark Principle\" (1984) as part of his university thesis and also co-founded Centropolis Entertainment in 1985 with his sister.\n\n[Sgt. Kabukiman N.Y.P.D.]\nSgt. Kabukiman N.Y.P.D. is a 1990 superhero comedy film directed by Lloyd Kaufman and Michael Herz and distributed by Troma Entertainment.\n\n[Michael Herz (producer)]\nWith Lloyd Kaufman, the two are the co-founders of Troma Entertainment, the world's longest running independent film studio, known for their comedic horror films, including the cult favorite \"Toxic Avenger series and \"Tromeo and Juliet\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q41efc6b5aa",
  "kind": "yes/no",
  "text": "Tweet: Is this first Cybex isokinetic dynamometer? @DrAndrewBateman #PRS2021",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q6a60ee6a56",
  "kind": "yes/no",
  "text": "Claim: Jeff Wadlow directed the movie starring Lucy Hale and American film and television actress, best known for her role as Jesse Quick in The CW's \"The Flash.\n\nPassages:\n\n[Violett Beane]\nViolett Beane (born May 18, 1996) is an American film and television actress, best known for her role as Jesse Quick in The CW's \"The Flash\".\n\n[Truth or Dare (2018 film)]\nTruth or Dare is an upcoming American supernatural horror film directed by Jeff Wadlow and written by Wadlow, Christopher Roach, Michael Reisz and Jillian Jacobs. It stars Lucy Hale, Tyler Posey, Violett Beane, Nolan Gerard Funk, Hayden Szeto and Sophia Taylor Ali.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6096ca80ef",
  "kind": "yes/no",
  "text": "Text: .@GMA you just mis-gendered Jordan Cofer, victim in the Dayton shooting, again. Please do better.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qfa54ccc7dc",
  "kind": "yes/no",
  "text": "Tweet: I've said it before and I'll say it again but YOUR MENTAL HEALTH IS SO MUCH MORE IMPORTANT THAN A GOOD GRADE",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qbcf0e987f3",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Everyone who studies law watched suits in sixthform/college.",
   "Maybe if I watched suits in year 12 I’d be studying law rn"
  ]
 },
 {
  "qid": "q95f96b829f",
  "kind": "yes/no",
  "text": "Claim: Sia heavily sampled the Sergei O. Prokofieff's grandfather's song that the 6 minute song Party Like a Russian samples. The song was classical music written by a Russian composer.\n\nPassages:\n\n[Montagues and Capulets]\nMontagues and Capulets is a work of classical music written by Russian composer Sergei Prokofiev.\n\n[Sergei O. Prokofieff]\nHe was the grandson of the composer Sergei Prokofiev and his first wife Lina Prokofiev, and the son of Oleg Prokofiev and his first wife Sofia Korovina.\n\n[Taken for Granted]\nIt was written by Sia and produced by Nigel Corsbie and heavily samples from Sergei Prokofiev's 'Montagues and Capulets'\n\n[Party Like a Russian]\nThe chorus of the song samples Sergei Prokofiev's \"Montagues and Capulets\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q72ad70f0de",
  "kind": "yes/no",
  "text": "Claim: The producer made his first film under the banner of Reliance Big Pictures in 2001. He also producer the film Bangistan.\n\nPassages:\n\n[Ritesh Sidhwani]\nRitesh Sidhwani (born 1973) is a Bollywood film producer, who founded a film production house under the banner of Excel Entertainment Pvt. Ltd. Along with long-time friend Farhan Akhtar, he brought to the audience \"Dil Chahta Hai\", his first film under his banner.\n\n[Bangistan]\nBangistan is a 2015 Bollywood comedy satire film directed by Karan Anshuman and produced by Farhan Akhtar and Ritesh Sidhwani starring Riteish Deshmukh, Pulkit Samrat and Chandan Roy Sanyal in lead roles.\n\n[Dil Chahta Hai]\nDil Chahta Hai (English: \"The Heart Desires\") is a 2001 Indian comedy-drama film starring Aamir Khan, Saif Ali Khan, Akshaye Khanna, Preity Zinta, Sonali Kulkarni, and Dimple Kapadia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q85379bd3bb",
  "kind": "yes/no",
  "text": "Claim: A co-founder of The International Society on Hypertension in Blacks was the associate producer of Doc Hollywood, a 1991 Scottish romantic comedy film directed by Michael Caton-Jones.\n\nPassages:\n\n[International Society on Hypertension in Blacks]\nIt was founded in 1986 by the physicians Dallas Hall, Neil B. Shulman, and Elijah Saunders, in response to concern about high rates of hypertension among African Americans. By 2006, the society had broadened its scope to focus not just on reducing rates of hypertension among African Americans, but also on improving the health of all minority populations around the world.\n\n[Neil B. Shulman]\nHe is the associate producer of the 1991 film \"Doc Hollywood\", based on one of his books.\n\n[Doc Hollywood]\nDoc Hollywood is a 1991 American romantic comedy film directed by Michael Caton-Jones, and written by Jeffrey Price and Peter S. Seaman, based on Neil B. Shulman's book, \"What?",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd414a1ba28",
  "kind": "yes/no",
  "text": "Claim: Paul Shaw wrote a book on the history of the design of the New York subway system in 2014 for a magazine. That magazine and National Journal are not both periodicals.\n\nPassages:\n\n[Paul Shaw (design historian)]\nHe has written a book on the history of the design of the New York subway system, \"Helvetica and the New York Subway System: The True (Maybe) Story\", on the work of William Addison Dwiggins, and for \"Print\" magazine.\n\n[National Journal]\nNational Journal is a research and advisory services company based in Washington, D.C. offering services in government affairs, advocacy communications and policy brands research for government and business leaders. It publishes daily journalism covering politics and public policy and is led by President Kevin Turpin and Editor-in-Chief Stephen G. Smith.\n\n[Print (magazine)]\nPrint, A Quarterly Journal of the Graphic Arts was a limited edition quarterly periodical begun in 1940 and continued under different names up to the present day as Print, a bimonthly American magazine about visual culture and design.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q532e56f235",
  "kind": "yes/no",
  "text": "Claim: Robert Patrick Mulligan was born before the director of the 1987 film Who's That Girl.\n\nPassages:\n\n[James Foley (director)]\nJames Foley (born December 28, 1953) is an American film director.\n\n[Who's That Girl (1987 film)]\nWho's That Girl is a 1987 American screwball comedy film written by Andrew Smith and Ken Finkleman, and directed by James Foley.\n\n[Robert Mulligan]\nRobert Patrick Mulligan (August 23, 1925 – December 20, 2008) was an American film and television director best known as the director of humanistic American dramas, including \"To Kill a Mockingbird\" (1962), \"Summer of '42\" (1971), \"The Other\" (1972), \"Same Time, Next Year\" (1978) and \"The Man in the Moon\" (1991).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8315a6dddf",
  "kind": "yes/no",
  "text": "Claim: Sinimole Paulose's favorite events are the 800 metres and another event that has been a contest at the Summer Olympics begining in 1896.\n\nPassages:\n\n[Sinimole Paulose]\nHer favorite events are 800 metres and 1500 metres.\n\n[1500 metres]\nThe distance has been contested at the Summer Olympics since 1896 and the World Championships in Athletics since 1983.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q01574a3437",
  "kind": "yes/no",
  "text": "Text: .@staterepsara IL needs to be a leader in the fight to protect women's rights. It's time to modernize Illinois' abortion law and pass the Reproductive Health Act. Please vote yes! #RHAinIL #twill",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q035f844c3a",
  "kind": "yes/no",
  "text": "Claim: In addition to Hyerim and the individual who left the group in January 2010 to pursue her academic career, Yubin and Yeeun were the other two final members of the group whose third mini album was named Wonder Party.\n\nPassages:\n\n[Sunmi]\nLee Sun-mi (born May 2, 1992), referred to as Sunmi, is a South Korean singer. She debuted in 2007 as a member of South Korean girl group Wonder Girls and left from the group in January 2010 to pursue her academic career.\n\n[Wonder Party]\nWonder Party is the third mini album by South Korean girl group Wonder Girls.\n\n[Wonder Girls]\nWonder Girls () was a South Korean girl group and band formed by producer Park Jin-young under JYP Entertainment in 2006, which debuted in 2007. The group's final line-up consisted of Yubin, Yeeun, Sunmi and Hyerim.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qaf37f9d4a1",
  "kind": "yes/no",
  "text": "Claim: A reggae artist is a believer in a religion that Roots reggae deals with the spiritual side of and was developed in Benin. A Time & Place is the second studio album by this artist.\n\nPassages:\n\n[Rastafari]\nClassified as a new religious movement, it developed in Jamaica during the 1930s.\n\n[Roots reggae]\nRoots reggae is a subgenre of reggae that deals with the everyday lives and aspirations of the artists concerned, including the spiritual side of Rastafari and the honoring of God, called Jah by Rastafari.\n\n[A Time &amp; Place]\nA Time & Place is the second studio album by reggae artist Julian Marley, released in 2003 on Lightyear Entertainment.\n\n[Julian Marley]\nHe follows into his father’s footsteps and is a devout Rastafarian who uses his music to inspire his life and spirituality.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q317bb6ad8f",
  "kind": "yes/no",
  "text": "Claim: The animated film that Pocahontas II: Journey to a New World was a sequel to, was made before Born in China.\n\nPassages:\n\n[Pocahontas II: Journey to a New World]\nPocahontas II: Journey to a New World is a 1998 straight-to-video sequel to the 1995 Disney film \"Pocahontas\".\n\n[Pocahontas (1995 film)]\nPocahontas is a 1995 American animated musical romantic-comedy-drama film produced by Walt Disney Feature Animation for Walt Disney Pictures.\n\n[Born in China]\nBorn in China (我們誕生在中國) is a 2016 nature documentary film directed by Lu Chuan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd5247472b1",
  "kind": "yes/no",
  "text": "Claim: The backing vocalist on \"We've Had Enough\" is known for playing in punk bands and another singer isn't. This other singer boosted the popularity of Reggae rock.\n\nPassages:\n\n[Keith Morris]\nKeith Morris (born September 18, 1955) is an American singer and songwriter known for his role as frontman of the hardcore punk bands Black Flag, Circle Jerks, and Off!\n\n[We've Had Enough]\n\"We've Had Enough\" features backing vocals by Keith Morris, singer of the Circle Jerks and original singer of Black Flag.\n\n[Reggae rock]\nThe genre has lately found a boost in popularity with the 2010 song \"Lay Me Down\" by the Dirty Heads featuring Rome Ramirez from Sublime with Rome, which peaked at number 1 on both the US \"Billboard\" Alternative Songs and Rock Songs charts.\n\n[Rome Ramirez]\nRoman René Ramírez (born June 11, 1988 in Fremont, California), better known as Rome Ramirez or simply Rome, is an American singer and guitarist best known for playing with Eric Wilson from Sublime and Josh Freese from The Vandals in the band Sublime with Rome.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8028d76a4c",
  "kind": "yes/no",
  "text": "Claim: The band, who released \"My Type\", was a group of Mint Condition recording artists that are known to be an indie pop band.\n\nPassages:\n\n[Saintmotelevision]\nIt was released on October 21, 2016, by Elektra Records.\n\n[My Type]\n\"My Type\" is a song by American indie pop band Saint Motel.\n\n[Saint Motel]\nSaint Motel is an American indie pop band from Los Angeles, whose music has been described as everything from \"dream pop\" to \"indie prog\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qeee0876443",
  "kind": "yes/no",
  "text": "Tweet: @BuzzPatterson I say he's still pretty wiley.  A touch (?) of senility might be turbo-charging his wileyness, and he naturally loves the attention of his courtesan 'handlers'.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q8c32adfa5f",
  "kind": "yes/no",
  "text": "Claim: 28000 km2 is the approximate area of the country where the flower species Lobelia columnaris can be found (other than Cameroon).\n\nPassages:\n\n[Lobelia columnaris]\nIt is the only giant Lobelia occurring in West Africa and is found in Cameroon and Equatorial Guinea.\n\n[Equatorial Guinea]\nEquatorial Guinea (Spanish: \"Guinea Ecuatorial\" , French: \"Guinée équatoriale\" , Portuguese: \"Guiné Equatorial\" ), officially the Republic of Equatorial Guinea (Spanish: \"República de Guinea Ecuatorial\" , French: \"République de Guinée équatoriale\" , Portuguese: \"República da Guiné Equatorial\" ), is a country located in Central Africa, with an area of 28000 km2 .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb58e497ab1",
  "kind": "yes/no",
  "text": "Claim: The score of the Super Bowl that coach Matt Ulrich won with the Colts was 29–17.\n\nPassages:\n\n[Matt Ulrich]\nHe won Super Bowl XLI with the Colts during the 2006 season over the Chicago Bears.\n\n[Super Bowl XLI]\nThe Colts defeated the Bears by the score of 29–17.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5c44829a21",
  "kind": "yes/no",
  "text": "Tweet: My PS4 Pro has P.T on it, which is somewhat funny as it was taken down before the PS4 Pro was even released #konami #PT #SilentHills #Spooky #PlayableTeaser #Kojima",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q6660ffc844",
  "kind": "yes/no",
  "text": "Claim: Nick Offerman, an actor from Parks and Recreation, also stared in Gary Scott Winick's 2004 movie.\n\nPassages:\n\n[Gary Winick]\nGary Scott Winick (March 31, 1961February 27, 2011) was an American filmmaker whose movies as a director include \"Tadpole\" (2002) and \"13 Going on 30\" (2004), and who also produced such films as \"Pieces of April\" (2003) and \"November\" (2004) through his New York City-based independent film production company InDigEnt.\n\n[November (2004 film)]\nNovember is a 2004 American psychological thriller film first screened at the 2004 Sundance Film Festival. The film co-stars Michael Ealy, Nora Dunn, Anne Archer, Nick Offerman, and Matthew Carey.\n\n[Nick Offerman]\nNicholas \"Nick\" Offerman (born June 26, 1970) is an American actor, voice actor, producer, writer, comedian and carpenter widely known for his breakout role as Ron Swanson in the acclaimed NBC sitcom \"Parks and Recreation\", for which he received the Television Critics Association Award for Individual Achievement in Comedy.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3d9319d449",
  "kind": "yes/no",
  "text": "Claim: Pyne & Marles is co-hosted by Richard Marles and an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the beginning of 1993.\n\nPassages:\n\n[Pyne &amp; Marles]\nThe program is co-hosted by two serving frontbench MPs; Liberal minister Christopher Pyne and Labor shadow minister Richard Marles, without a journalist or moderator.\n\n[Christopher Pyne]\nChristopher Maurice Pyne (born 13 August 1967) is an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the 1993 election.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfe9135d27d",
  "kind": "yes/no",
  "text": "Post: @PoliticalOrgy I thing you might be on to somethink!🙄",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q1c31a2b3e6",
  "kind": "yes/no",
  "text": "Text: \"He's not welcome in a tolerant place like London\" @emmadentcoad  on the Presidential visit on @BBCRadio4 The irony in that comment... #r4bh",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qec19f6590a",
  "kind": "yes/no",
  "text": "Claim: The choreographer of La Vivandiere or Markitenka was the \"Maître de Ballet\" of the company now known as The Mariinsky Ballet\n\nPassages:\n\n[Arthur Saint-Léon]\nArthur Saint-Léon (17 September 1821, Paris – 2 September 1870) was the \"Maître de Ballet\" of St. Petersburg Imperial Ballet from 1859 until 1869 and is famous for creating the choreography of the ballet \"Coppélia\".\n\n[Mariinsky Ballet]\nThe Mariinsky Ballet is the resident classical ballet company of the Mariinsky Theatre in Saint Petersburg, Russia. Founded in the 18th century and originally known as the Imperial Russian Ballet, the Mariinsky Ballet is one of the world's leading ballet companies. The Mariinsky Ballet is the parent company of the \"Vaganova Ballet Academy\", a leading international ballet school.\n\n[La Vivandière or Markitenka]\nLa Vivandière (or Markitenka, as it is known in Russia) is a ballet in one act with choreography by Arthur Saint-Léon and Fanny Cerrito, and music by Cesare Pugni.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
