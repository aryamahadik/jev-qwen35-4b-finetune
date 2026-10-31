# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-001.json

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
  "qid": "q0ff0071fd9",
  "kind": "yes/no",
  "text": "Tweet: @fishy_lo @OfficialPLT_CS @OfficialPLT Why type of  lube did you order?  I may have extra in my detached garage",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q23760a50b8",
  "kind": "yes/no",
  "text": "Claim: The player that is featured on the cover of the Spanish version of this video game is 6 ft tall. This game is the predecessor to another game. The series the other game is in is published by Take-Two Interactive.\n\nPassages:\n\n[NBA 2K16]\nAdditionally, the French version of \"NBA 2K16\" features Tony Parker of the San Antonio Spurs as the cover athlete, the German version, Dennis Schröder of the Atlanta Hawks, and the Spanish version, Marc and Pau Gasol of the Memphis Grizzlies and Chicago Bulls respectively.\n\n[Take-Two Interactive]\nAs owner of 2K Games, Take-Two publishes its 2K Sports titles, and creates free-to-play mobile titles through Social Point.\n\n[Dennis Schröder]\nStanding at 6 ft , he plays at the point guard position.\n\n[NBA 2K17]\nIt is the 18th installment in the \"NBA 2K\" franchise and the successor to \"NBA 2K16\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q15a518afa7",
  "kind": "yes/no",
  "text": "Claim: The city where the all-seater Róisín Dubh is located is in the Western area of Ireland. It is also the home of Sean Smyth.\n\nPassages:\n\n[Seán Smyth]\nBorn in Straide, County Mayo, and now living in Galway, Seán is an All-Ireland champion on both fiddle and whistle .\n\n[Galway]\nGalway ( ; Irish: \"Gaillimh\" , ] ) is a city in the West of Ireland in the province of Connacht.\n\n[Róisín Dubh (music venue)]\nThe Róisín Dubh is an established live music venue in Galway, Ireland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q90f03ee1ad",
  "kind": "yes/no",
  "text": "Claim: An IndyCar race driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season.\n\nPassages:\n\n[Super Aguri SA07]\nThe Super Aguri F1 SA07 was Super Aguri F1's Formula One car for the 2007 Formula One season.\n\n[Takuma Sato]\nSato has raced full-time in the IndyCar Series since 2010 for the KV, Rahal, Foyt, and currently Andretti teams.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q06941c9f3c",
  "kind": "yes/no",
  "text": "Claim: The American author of Done in the Open lived longer than American author Lucy Maud Montgomery.\n\nPassages:\n\n[Lucy Maud Montgomery]\nLucy Maud Montgomery {'1': \", '2': \", '3': \", '4': \"} (November 30, 1874 – April 24, 1942) published as L.M. Montgomery, was a Canadian author best known for a series of novels beginning in 1908 with \"Anne of Green Gables\".\n\n[Done in the Open]\nDone in the Open was a verse collection published by in 1903 American author Owen Wister.\n\n[Owen Wister]\nOwen Wister (July 14, 1860 – July 21, 1938) was an American writer, historian and \"father\" of western fiction.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc131667f1f",
  "kind": "yes/no",
  "text": "Claim: \"A Swingin' Safari\" was a song written originally by German lyricist Bert Kaempfert but made popular by Billy Vaughn.\n\nPassages:\n\n[Bert Kaempfert]\nBerthold Heinrich Kämpfert, (16 October 1923 – 21 June 1980), better known as Bert Kaempfert, was a German orchestra leader, music producer, and songwriter.\n\n[A Swingin' Safari]\nThat same year, Billy Vaughn recorded it, and his cover reached number 13 on the \"Billboard\" charts that summer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q89abf427a2",
  "kind": "yes/no",
  "text": "Claim: The producer of the Sarah McLachlan EP, Live Acoustic, shared a mike with this notable radio personality. The radio personality was born in North Bend, Oregon.\n\nPassages:\n\n[Skip Kelly]\nOn air, he has shared the same mic as well known personalities Ryan Seacrest, Danny Bonaduce, Delilah, Matt Siegel, and Dale Dorman.\n\n[Delilah (radio host)]\nDelilah Rene (born February 15, 1960, North Bend, Oregon) is an American radio personality, author, and songwriter, best known as the host of a nationally syndicated nightly U.S. radio song request and dedication program, with an estimated 8 million listeners.\n\n[Live Acoustic (Sarah McLachlan EP)]\nThese tracks were produced by Skip Kelly and remastered by Dave Kutch.\n\n[Radio personality]\nNotable radio personalities include pop music radio hosts Martin Block, Alan Freed, Dick Clark, Delilah Luke, Ameen Sayani, Wolfman Jack, and Casey Kasem, shock jocks such as Don Imus and Howard Stern, as well as sports talk hosts such as Mike Francesa and political talk hosts such as Rush Limbaugh.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q554c4e9c8a",
  "kind": "yes/no",
  "text": "Claim: Sky Rocket, in Disneyland Tokyo, was renovated into Phantom's Revenge roller coaster, that had the longest drop at the time.\n\nPassages:\n\n[Phantom's Revenge]\nWhen it opened in 1991, it was the fastest roller coaster and had the longest drop of any roller coaster in the world.\n\n[Sky Rocket]\nSky Rocket is a steel roller coaster located at Kennywood Park in Pittsburgh, Pennsylvania. It is the first coaster erected at the park since the renovation of the Steel Phantom into the Phantom's Revenge in 2001; it also marks the return of a roller coaster that features inversions.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q85629c8f69",
  "kind": "yes/no",
  "text": "Claim: Piaggio manufactured the scooter upon which the Bajaj Priya was based off of.\n\nPassages:\n\n[Vespa]\nVespa (] ) is an Italian brand of scooter manufactured by Piaggio.\n\n[Bajaj Priya]\nThe design was very similar to that of the earlier \"Bajaj 150\" model (which was in turn based upon a Vespa 150 (VBA type) with a slightly modified body).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb6aba7e1ce",
  "kind": "yes/no",
  "text": "Claim: The second extended play of the American singer and songriter best known as the clean vocalist in post-hardcore band, Dance Gavin Dance, was released on September 1, 2017 on Vital Records.\n\nPassages:\n\n[Patient EP]\nPatient is the second extended play (EP) by American singer and songwriter Tilian Pearson. It was released on September 1, 2017 on Vital Records.\n\n[Tilian Pearson]\nHe is best known as the clean vocalist in post-hardcore band Dance Gavin Dance.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q036cf8649b",
  "kind": "yes/no",
  "text": "Claim: The NFL football team that plays its home matches in New York that Nevil McCaskill played for is the Buffalo Bills.\n\nPassages:\n\n[Buffalo Bills]\nThe Bills are the only NFL team that plays its home games in the state of New York (the New York Giants and New York Jets play at MetLife Stadium, located in East Rutherford, New Jersey).\n\n[Nevin McCaskill]\nHe was signed by the Buffalo Bills as an undrafted free agent in 2007.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb1fbfca139",
  "kind": "yes/no",
  "text": "Claim: Cough Syrup is the main ingredient referenced in the \"drank\" of the song Drank in My Cup.\n\nPassages:\n\n[Drank in My Cup]\nThe song uses the word 'drank' a number of times as a clear reference to purple drank, a codeine-promethazine cocktail served in Sprite, a drink symbolic of the H-Town hip-hop scene, classically associated with chopped and screwed music.\n\n[Purple drank]\nPurple drank is a slang term for a concoction which includes a prescription-strength cough syrup used in a manner inconsistent with its labeling, thus making it a recreational drug.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q772eb0379c",
  "kind": "yes/no",
  "text": "Claim: Matthew Pettinger's birth place is on the banks of the North Saskatchewan River.\n\nPassages:\n\n[Matt Pettinger]\nMatthew Pettinger (born October 22, 1980) is a Canadian professional ice hockey left winger who is currently an unrestricted free agent who last played for the Hamburg Freezers of the Deutsche Eishockey Liga (DEL). Pettinger was born in Edmonton, Alberta and raised in Victoria, British Columbia.\n\n[Edmonton]\nEdmonton is the capital city of the Canadian province of Alberta. Edmonton is on the North Saskatchewan River and is the centre of the Edmonton Capital Region, which is surrounded by Alberta's central region.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qad7b3ccd12",
  "kind": "yes/no",
  "text": "Claim: Kind Hearts and Coronets was the name of the 1949 British black comedy film that the hotel popular for Dirty weekends appeared on.\n\nPassages:\n\n[Kind Hearts and Coronets]\nKind Hearts and Coronets is a 1949 British black comedy film.\n\n[Skindles]\nThe hotel appears in the film Kind Hearts and Coronets.\n\n[Dirty weekend]\nPlaces which became famous for this include Brighton and the Skindles hotel in Maidenhead.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa509d3998f",
  "kind": "yes/no",
  "text": "Claim: In this religion, where Mehet-Weret is a godess of the sky, a citizen would be weighted against the feather of truth to decide if they where worthy of damnation and would face the torment in the lake of fire.\n\nPassages:\n\n[Damnation]\nIn Ancient Egyptian religious tradition, citizens would recite the 42 negative confessions of Maat as their heart was weighed against the feather of truth.\n\n[Mehet-Weret]\nMehet-Weret \"(mḥ.t-wr.t)\" is a goddess of the sky in Ancient Egyptian religion. Her name means \"Great Flood\".\n\n[Ancient Egyptian religion]\nAncient Egyptian religion was a complex system of polytheistic beliefs and rituals which were an integral part of ancient Egyptian society.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8d237a7dbd",
  "kind": "yes/no",
  "text": "Claim: Wheel in the Sky is a song by Jimmy Page. Its writer and the singer who worked on Living Loud (album) do not have the same nationality.\n\nPassages:\n\n[Jimmy Barnes]\nJames Dixon Swan {'1': \", '2': \", '3': \", '4': \"} (born 28 April 1956), better known as Jimmy Barnes, is a Scottish-Australian rock singer-songwriter.\n\n[Wheel in the Sky]\nIt was written and composed by Robert Fleischman, Neal Schon and Diane Valory.\n\n[Living Loud (album)]\nAustralian rock singer Jimmy Barnes and Deep Purple guitarist Steve Morse were also part of the project.\n\n[Robert Fleischman]\nRobert Fleischman (born March 11, 1953) is an American musician, songwriter, and record producer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbbcfe176b8",
  "kind": "yes/no",
  "text": "Claim: The actor Thomas Gregory played in a drama television series based on Israeli series the \"Yellow Peppers\".\n\nPassages:\n\n[Thomas Gregory (actor)]\nThomas Gregory (born 10 November 1995) is an English actor who played Luke Taylor in BBC One drama \"The A Word\", first broadcast in March 2016.\n\n[The A Word]\nThe A Word is a BBC drama television series based on Israeli series the \"Yellow Peppers\" (פלפלים צהובים) by Keren Margalit.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa1c514da23",
  "kind": "yes/no",
  "text": "Claim: The group that released \"Let's Build Something to Break\" is a rock band as well as Aaroh.\n\nPassages:\n\n[After Midnight Project]\nAfter Midnight Project (commonly abbreviated \"AMP\") is an American rock band from Los Angeles, California.\n\n[Aaroh]\nAaroh (Urdu: آروح, literal English translation: \"the ascending scale in eastern classical music\") is an alternative rock band from Karachi, Sindh, Pakistan, formed in 1998.\n\n[Let's Build Something to Break]\nLet's Build Something to Break is the debut full-length album by American rock band, After Midnight Project.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb315b13eb3",
  "kind": "yes/no",
  "text": "Claim: A Russian linguist, was a member of the Kazan School. This Russian linguist was published by the Junior Hockey League. This publisher was founded by Ladislav Matejka.\n\nPassages:\n\n[Kazan school]\nKazan School was an influential group of linguists in Kazan. The linguistic circle included the Polish linguist Jan Baudouin de Courtenay and his student Nikolai Trubetzkoy.\n\n[Ladislav Matejka]\nIn 1962, he founded Michigan Slavic Publications, a series that has published more than 100 volumes by authors such as Roman Jakobson and Nikolai Trubetzkoy.\n\n[Nikolai Trubetzkoy]\nPrince Nikolai Sergeyevich Trubetzkoy (also Troubetskoy; Russian: Никола́й Серге́евич Трубецко́й; Moscow, April 16, 1890 – Vienna, June 25, 1938) was a Russian linguist and historian whose teachings formed a nucleus of the Prague School of structural linguistics.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdf3b684f58",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "It's absolutely going to be awful living In Kent after Brexit considering the issues with Lorries.",
   "Always glad to live in Kent 🙈🙈"
  ]
 },
 {
  "qid": "qc8f2006146",
  "kind": "yes/no",
  "text": "Claim: The evil clown is a subversion of the traditional comic clown character with the modern archetype popularised by a book that follows the experiences of seven children.\n\nPassages:\n\n[It (novel)]\nIt is a 1986 horror novel by American author Stephen King. It was his 22nd book and 18th novel written under his own name. The story follows the experiences of seven children as they are terrorized by a being that exploits the fears and phobias of its victims to disguise itself while hunting its prey.\n\n[Evil clown]\nThe evil clown is a subversion of the traditional comic clown character, in which the playful trope is instead rendered as disturbing through the use of horror elements and dark humor. The modern archetype of the evil clown was popularized by Stephen King's 1986 novel \"It\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9fa6527b0d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "We decided to record on the evening of the 6th, which was unfortunate because at the same time some significant events were happening that we probably would have talked about.",
   "Ok, so @bytereview and I decided to record on the evening of the 6th, just as absolutely nothing newsworthy was happening! Perfect timing as always, to go over some of the best ITSBUPs of 2020 - and how we're settling into 2021! Listen: https://t.co/oaPLwrtcHP https://t.co/za3EHuqcWh"
  ]
 },
 {
  "qid": "q1c10da17f9",
  "kind": "yes/no",
  "text": "Claim: George Carl character in the film Royal Flash was Prussian.\n\nPassages:\n\n[Royal Flash (film)]\nRoyal Flash is a 1975 film based on George MacDonald Fraser's second Flashman novel, \"Royal Flash\". Additionally, Oliver Reed appeared in the role of Otto von Bismarck, Alan Bates as Rudi von Sternberg, and Florinda Bolkan played Lola Montez.\n\n[Otto von Bismarck]\nOtto Eduard Leopold, Prince of Bismarck, Duke of Lauenburg (1 April 1815 – 30 July 1898), known as Otto von Bismarck (] ), was a conservative Prussian statesman who dominated German and European affairs from the 1860s until 1890.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q72d2aa5a06",
  "kind": "yes/no",
  "text": "Text: Delaying June 21st is entirely Boris Johnson’s fault for not responding to the Indian variant quickly and keeping the boarders open and we mustn’t forget that. This was entirely preventable.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q2f48864612",
  "kind": "yes/no",
  "text": "Claim: Billy King was an Australian rules footballer who participated in a game that was contested between the South Carlton Football Club and Carlton Football Club, and was held at Princes Park in Carlton in 1945.\n\nPassages:\n\n[Billy King (Australian footballer)]\nWilliam Herbert 'Billy' King (17 August 1920 – 23 August 1990) was an Australian rules footballer who played for South Melbourne in the VFL during the 1940s. Primarily a wingman, he participated in the famous 1945 'Bloodbath' Grand Final which South Melbourne lost to Carlton.\n\n[1945 VFL Grand Final]\nThe 1945 VFL Grand Final was an Australian rules football game contested between the South Melbourne Football Club and Carlton Football Club, held at Princes Park in Melbourne on 29 September 1945.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qaa13acf166",
  "kind": "yes/no",
  "text": "Text: Lucky for 2nd placed Brentford that there's no stand out team like Leeds this year, or they might have no chance of winning the league. #ncfc",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q424d9cc111",
  "kind": "yes/no",
  "text": "Claim: Bill Pollack's distinction of being American-born makes him unique as a winner of the Formula One World Drivers' Championship.\n\nPassages:\n\n[Bill Pollack]\nBill Pollack was a competitor in the early days of the post World War II California sports car culture. He was a contemporary of Phil Hill, who went on to become the first and only U.S. born world grand prix champion.\n\n[Phil Hill]\nPhilip Toll Hill Jr. (April 20, 1927 – August 28, 2008) was an American automobile racer and the only American-born driver to win the Formula One World Drivers' Championship (Mario Andretti, an Italian American driver, won the World Drivers' Championship in 1978, but was not born in the United States).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd663457eec",
  "kind": "yes/no",
  "text": "Claim: Andrea Albert Pierre Casiraghi, is the elder son of Caroline, Princess of Hanover, and her second husband Stefano Casiraghi, and is the eldest grandchild of Rainier III, Prince of Monaco, and the American actress Grace Kelly, who became Princess of Monaco after marrying Prince Rainier III, in April 1956.\n\nPassages:\n\n[Grace Kelly]\nGrace Patricia Kelly (November 12, 1929September 14, 1982) was an American actress who became Princess of Monaco after marrying Prince Rainier III, in April 1956.\n\n[Andrea Casiraghi]\nHe is the eldest grandchild of Rainier III, Prince of Monaco, and American actress Grace Kelly.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q08b1ea21dd",
  "kind": "yes/no",
  "text": "Claim: The venue of \"UFC 50: The War of '04\" is in Atlantic City. It closed after the establishment adjacent to the Dunes Hotel and Casino (Atlantic City).\n\nPassages:\n\n[Trump Plaza Hotel and Casino]\nDesigned by architect Martin Stern, Jr., it operated from May 15, 1984 until September 16, 2014.\n\n[UFC 50]\nUFC 50: The War of '04 was a mixed martial arts event held by the Ultimate Fighting Championship on October 22, 2004, at the Trump Plaza in Atlantic City, New Jersey.\n\n[The Atlantic Club Casino Hotel]\nThe Atlantic Club Casino Hotel, formerly known as Golden Nugget, Bally's Grand, Atlantic City Hilton and ACH, is a closed casino and hotel located at the southern end of the boardwalk in Atlantic City, New Jersey, owned and operated by Colony Capital. The Atlantic Club permanently closed on January 13, 2014, at 12:01 AM.\n\n[Dunes Hotel and Casino (Atlantic City)]\nIt was to be the southern most hotel/casino on the Boardwalk, adjacent to the Golden Nugget Hotel & Casino.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8fc7932ffd",
  "kind": "yes/no",
  "text": "Claim: Denmark's leader residing over the Cabinet of Deuntzer, was a part of the Liberal \"Venstre\" party for 12 years before the party that translates to the \"Radical Left\".\n\nPassages:\n\n[Danish Social Liberal Party]\nThe Danish Social Liberal Party (Danish: \"Radikale Venstre\" , \"Radical Left\", i.e. \"Radical Liberal Party\") is a social-liberal political party in Denmark.\n\n[Cabinet of Deuntzer]\nAfter the 1901 Danish Folketing election, the Council President Johan Henrik Deuntzer of the Venstre Reform Party became the leader of Denmark's first liberal government.\n\n[Johan Henrik Deuntzer]\nJohan Henrik Deuntzer (20 May 1845 – 16 November 1918) was a Danish politician, member of the Liberal \"Venstre\" party until 1905 where he joined the Danish Social Liberal Party.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa410c60753",
  "kind": "yes/no",
  "text": "Claim: Ruxton Park and Pikes Peak are both nature parks located in Colorado.\n\nPassages:\n\n[Pikes Peak]\nThe ultra-prominent 4302.31 m fourteener is located in Pike National Forest, 19.3 km west by south (bearing 263°) of downtown Colorado Springs, Colorado.\n\n[Ruxton Park]\nRuxton Park is a park in Manitou Springs, El Paso County, Colorado at 9078 ft in elevation.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q533d441a66",
  "kind": "yes/no",
  "text": "Claim: Trouble Along the Way was directed by Michael Curtiz and produced by Harold Brent Wallis. Harold Brent Wallis also produced a 1942 film that starred the Dead End (1937 film).\n\nPassages:\n\n[Hal B. Wallis]\nHarold Brent Wallis (born Aaron Blum Wolowicz; October 19, 1898 – October 5, 1986) was an American film producer. He is best remembered for producing \"Casablanca\" (1942) and \"True Grit\" (1969), along with many other major films for Warner Bros. featuring such film stars as Humphrey Bogart, Bette Davis, and Errol Flynn.\n\n[Trouble Along the Way]\nThe movie was directed by Michael Curtiz, director of \"Casablanca\".\n\n[Dead End (1937 film)]\nIt stars Humphrey Bogart, Joel McCrea, and Sylvia Sidney.\n\n[Humphrey Bogart]\nHumphrey DeForest Bogart ( ; December 25, 1899January 14, 1957) was an American screen and stage actor whose performances in 1940s films noir such as \"The Maltese Falcon\", \"Casablanca\", and \"The Big Sleep\" earned him status as a cultural icon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf1384608ba",
  "kind": "yes/no",
  "text": "Post: WHO LET THE LAUNDRY PILE UP 5 BASKETS. Goodness.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb91e37268a",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I hate leaving the doctors office crying.",
   "I love leaving the doctors office in tears. I need this kid to just decide to leave my body so we can be done and home together."
  ]
 },
 {
  "qid": "q77203e29de",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@Dancruz07 Sureeeeeee you do",
   "I could've replied \"You do not despise me, you're my best friend.\""
  ]
 },
 {
  "qid": "q1a51a5e943",
  "kind": "yes/no",
  "text": "Post: @severed_limb Only thing worse than men is bald red sweaty middle aged ones",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qaaab1c91c4",
  "kind": "yes/no",
  "text": "Text: Turnover is the best band to cry to/drive to/daydream to/fall asleep to/ reminisce to/die to",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q2f4decdec4",
  "kind": "yes/no",
  "text": "Claim: Kenneth \"Ken\" Leung is the actor that portrays a marvel character in a ABC television series that was created by Scott Buck in 1962.\n\nPassages:\n\n[Inhumans (TV series)]\nMarvel's Inhumans, or simply Inhumans, is an American television series created for ABC by Scott Buck, based on the Marvel Comics race of the same name.\n\n[Ken Leung]\nKenneth \"Ken\" Leung (born January 21, 1970) is an American actor who is best known for playing Miles Straume in \"Lost\", Admiral Statura in \"\", Detective Stephen Sing in \"Saw\", and Kid Omega in \"\". He portrays the Marvel Comics character Karnak, a member of the Inhumans, on the ABC television series \"Inhumans\", which premiered in September 2017.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q287678fe1c",
  "kind": "yes/no",
  "text": "Text: So excited just seen #chitty bang bang car on the road in @huddersfield",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q24a9f6e67a",
  "kind": "yes/no",
  "text": "Claim: Len Wiseman was the Italian director of the 2007 American action film starring the actress who also starred in the film Slumber.\n\nPassages:\n\n[Slumber (film)]\nThe film stars Maggie Q, Will Kemp, Sylvester McCoy and William Hope.\n\n[Live Free or Die Hard]\nThe film was directed by Len Wiseman and stars Bruce Willis as John McClane.\n\n[Maggie Q]\nMargaret Denise Quigley (born May 22, 1979), professionally known as Maggie Q, is an American actress and model. She is known for starring in the action films \"\" and \"Live Free or Die Hard\" and played the title role of The CW's action-thriller series \"Nikita\", airing from 2010 to 2013.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q5f890e8a1f",
  "kind": "yes/no",
  "text": "Claim: Reese Witherspoon the actor/actress from Overnight Delivery was born in New Orleans.\n\nPassages:\n\n[Overnight Delivery]\nIt featured Reese Witherspoon and Paul Rudd, prior to both becoming considerably bigger film stars.\n\n[Reese Witherspoon]\nBorn in New Orleans and raised in Tennessee, she began her career as a child actress, making her professional screen debut in \"The Man in the Moon\" (1991), for which she was nominated for a Young Artist Award.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb6b5296a9e",
  "kind": "yes/no",
  "text": "Claim: The division that people from the division Major General Robert Walker Grow commanded originally came from the 2nd Armored Division.\n\nPassages:\n\n[6th Armored Division (United States)]\nIt was formed with a cadre from the 2nd Armored Division.\n\n[Robert W. Grow]\nMajor General Robert Walker Grow (February 14, 1895 – November 3, 1985) was a senior United States Army officer who commanded the 6th Armored Division during World War II.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa7d5fdbaac",
  "kind": "yes/no",
  "text": "Claim: Emory University was founded before the school that William Ridley Wills is a graduate of.\n\nPassages:\n\n[Vanderbilt University]\nFounded in 1873, it was named in honor of shipping and rail magnate Cornelius Vanderbilt, who provided the school its initial $1 million endowment despite having never been to the South.\n\n[Emory University]\nThe university was founded as Emory College in 1836 in Oxford, Georgia by the Methodist Episcopal Church and was named in honor of Methodist bishop John Emory. In 1915, the college relocated to metropolitan Atlanta and was rechartered as Emory University.\n\n[William Ridley Wills]\nWilliam Ridley Wills, born Brownsville, Tennessee on March 4, 1897, was a graduate of Vanderbilt University and a member of the Fugitive literary group.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2bc78a4955",
  "kind": "yes/no",
  "text": "Claim: The actor who played Karl Rove in the television sitcom directed by Jeff Melman, is from Stockton, CA. He appeared in Psych, an American detective comedy-drama television series created by Steve Franks.\n\nPassages:\n\n[Psych]\nPsych is an American detective comedy-drama television series created by Steve Franks and broadcast on USA Network with syndicated reruns on ION Television.\n\n[That's My Bush!]\nCarrie Quinn Dolin played Laura Bush, and Kurt Fuller played Karl Rove.\n\n[Jeff Melman]\n\", \"The King of Queens\", \"Two and a Half Men\" and \"Frasier\".\n\n[Kurt Fuller]\nHe graduated from Lincoln High School in Stockton, California in 1971, and U.C. Berkeley in 1976.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q557f3f7a6a",
  "kind": "yes/no",
  "text": "Claim: The 24th Hong Kong Film Awards ceremony was a positive for the 2004 Hong Kong romantic drama written and directed by Wong Kar-wai.\n\nPassages:\n\n[2046 (film)]\n2046 is a 2004 Hong Kong romantic drama film written and directed by Wong Kar-wai.\n\n[24th Hong Kong Film Awards]\nTwenty-nine winners in nineteen categories were unveiled, with films \"Kung Fu Hustle\" and \"2046\" being the year's biggest winners.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc45a3c1acf",
  "kind": "yes/no",
  "text": "Claim: The Ramones, the band that recorded the song \"While You Loved Me\" was formed in Columbus, OH.\n\nPassages:\n\n[While You Loved Me]\n\"While You Loved Me\" is a song written by Kim Williams, Danny Wells and Marty Dodson, and recorded by American country music group Rascal Flatts.\n\n[Rascal Flatts]\nRascal Flatts is an American country music trio formed in Columbus, Ohio in 1999.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q207945d077",
  "kind": "yes/no",
  "text": "Claim: Acoustic is an EP by an Canadian rock band. Mathew James \"Matt\" Willis has more top 20 singles than that band.\n\nPassages:\n\n[Bayside (band)]\nBayside is an American rock band from New York City, formed in 2000, currently consisting of lead vocalist/guitarist Anthony Raneri, lead guitarist Jack O'Shea, bassist Nick Ghanbarian, and drummer Chris Guglielmo.\n\n[Acoustic (Bayside EP)]\nAcoustic is an EP by American rock band Bayside, released on February 28, 2006.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted. Willis released his debut solo album \"Don't Let It Go to Waste\" on 20 November 2006, which included three top 20 singles.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qab99187a7f",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Dear @krispykremeUK, I note your #Thanksgiving offer that ends on 2 Dec. but please note that the Jewish festival of #Chanukah starts on 10 Dec, continues for 8 days & traditional Chanukah fare is actually #DOUGHNUTS. Please consider a special offer for this, too.",
   "Dear @krispykremeUK, I see your enticing #Thanksgiving offer that ends on 2 Dec. I wanted to ask if you're aware that #Chanukah starts on 10 Dec, continues for 8 days &amp; that traditional Chanukah fare is actually #DOUGHNUTS ?? 🍩🍩 #justsaying #AskingForAFriend #opportunity"
  ]
 },
 {
  "qid": "q2bd8f07d9d",
  "kind": "yes/no",
  "text": "Claim: This individual starred in the 18-rated Deception (2004 film). She played Detective Allison Kerry in an American horror franchise that consists of 8 feature films.\n\nPassages:\n\n[Saw (franchise)]\nSaw is an American horror franchise distributed by Lionsgate, produced by Twisted Pictures and created by James Wan and Leigh Whannell, that consists of eight feature films and additional media.\n\n[Dina Meyer]\nDina Meyer (born December 22, 1968) is an American film and television actress who played Barbara Gordon in \"Birds of Prey\", Dizzy Flores in \"Starship Troopers\", and Detective Allison Kerry in the \"Saw\" films.\n\n[Deception (2004 film)]\nDeception is a 2004 Canadian-American television film starring Dina Meyer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qcf83d81b5c",
  "kind": "yes/no",
  "text": "Claim: Russian-born Victor Oladipo and NBA All-Rookie Team are connected by basketball.\n\nPassages:\n\n[NBA All-Rookie Team]\nThe NBA All-Rookie Team is an annual National Basketball Association (NBA) honor given since the 1962–63 NBA season to the top rookies during the regular season.\n\n[Victor Oladipo]\nKehinde Babatunde Victor Oladipo (born May 4, 1992) is an American professional basketball player for the Indiana Pacers of the National Basketball Association (NBA).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 }
]
