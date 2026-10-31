# A46 replay label-noise blind read RSAS01-blind_read-e3b7f411-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS01-blind_read-e3b7f411-000.json

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
  "qid": "qe95a0d63da",
  "kind": "yes/no",
  "text": "Tweet: i’m dying",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qcc9b100bee",
  "kind": "yes/no",
  "text": "Claim: Scott Workman was an American stuntman and actor credited with a successful show on the smaller TV network WB Television Network.\n\nPassages:\n\n[Buffy the Vampire Slayer]\nAlthough such ratings are lower than successful shows on the \"big four\" networks (ABC, CBS, NBC, and Fox), they were a success for the relatively new and smaller WB Television Network.\n\n[Scott Workman]\nWilliam Scott Workman (September 16, 1966 - September 29, 2013) was an American stuntman and actor whose career spanned over the course of 20 years. Television credits include \"The X-Files\", \"Buffy the Vampire Slayer\" and \"Sons of Anarchy\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe03f63a8d9",
  "kind": "yes/no",
  "text": "Claim: The Voyage is a wooden roller coaster located at a theme park divided into four sections.\n\nPassages:\n\n[The Voyage (roller coaster)]\nThe Voyage is a wooden roller coaster located at Holiday World & Splashin' Safari in Santa Claus, Indiana.\n\n[Holiday World &amp; Splashin' Safari]\nThe theme park is divided into four sections that celebrate Christmas, Halloween, Thanksgiving and the Fourth of July with rides, live entertainment, games, and attractions.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q910cc9fa38",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I love days when Rob works short call and is only at the hospital for *checks watch* 13 hours.",
   "I hate when Rob works short call and is still at the hospital for 13+ hours."
  ]
 },
 {
  "qid": "qbcc4245ebd",
  "kind": "yes/no",
  "text": "Claim: George I took away the office of the individual who a revolt is named after, John Erskin, that is also called the Jacobite rising of 1715.\n\nPassages:\n\n[Jacobite rising of 1715]\nThe Jacobite rising of 1715 (Scottish Gaelic: \"Bliadhna Sheumais\" ] ) (also referred to as the Fifteen or Lord Mar's Revolt), was the attempt by James Francis Edward Stuart (also called the Old Pretender) to regain the thrones of England, Ireland and Scotland for the exiled House of Stuart.\n\n[George I of Great Britain]\nGeorge I (George Louis; German: \"Georg Ludwig\" ; 28 May 1660 – 11 June 1727) was King of Great Britain and Ireland from 1 August 1714 until his death, and ruler of the Duchy and Electorate of Brunswick-Lüneburg (Hanover) in the Holy Roman Empire from 1698.\n\n[John Erskine, Earl of Mar (1675–1732)]\nDeprived of office by the new king in 1714, Mar raised the standard of rebellion against the Hanoverians; at the battle of Sheriffmuir in November 1715, Mar's forces outnumbered those of his opponent, but victory eluded him.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4b1dd2e7cb",
  "kind": "yes/no",
  "text": "Claim: The day of the week the eleventh season's finale of American Dad aired was on a Sunday.\n\nPassages:\n\n[Blagsnarst, a Love Story]\n\"Blagsnarst, a Love Story\" is the third episode and season finale of the eleventh season of \"American Dad! \" The episode aired on September 21, 2014, and is the final show to air on Fox's Animation Domination lineup, as well as the final episode of the series to be aired on Fox as the show moved to TBS from the twelfth season onwards, which started a month later in October 2014.\n\n[Animation Domination]\nThe block aired on Sunday evenings through the entirety of that night's primetime schedule (unless preempted, usually by sports telecasts).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc989d622e9",
  "kind": "yes/no",
  "text": "Text: ik the republicans r like tryna say they won but idk why they don’t just settle this w an instagram poll??",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q27bfadca76",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "My work email isn’t working so I can just log off for the day right? 🙄",
   "I wish I would log off for the day because my email isn't working."
  ]
 },
 {
  "qid": "q8a00edc6a4",
  "kind": "yes/no",
  "text": "Claim: Dharmatama is a 1975 Hindi thriller movie, and the first Bollywood film to be shot in Teheran, Afghanistan,the title character was based on matka, king Ratan Khatri, Matka\" gambling or satta\" is a form of lottery which originally involved betting on the opening and closing rates of cotton transmitted from the New York Cotton Exchange.\n\nPassages:\n\n[Dharmatma]\nThe title character was based on matka (form of Indian gambling) king Ratan Khatri.\n\n[Matka gambling]\nMatka\" gambling or satta\" is a form of lottery which originally involved betting on the opening and closing rates of cotton transmitted from the New York Cotton Exchange.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd0d0904e2d",
  "kind": "yes/no",
  "text": "Claim: The birthday of the man who asked Andres Thomas \"Why would you even throw him a strike?\" was April 2, 1945, he was born in Rochdale.\n\nPassages:\n\n[Andrés Thomas]\nHis free-swinging prompted then-Braves' broadcaster Don Sutton to ask hypothetically during games, \"Why would you even throw him a strike?\"\n\n[Don Sutton]\nDonald Howard Sutton (born April 2, 1945) is an American former professional baseball player.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4edfbf9960",
  "kind": "yes/no",
  "text": "Text: There's far too much \"imagine if you had kids\" talk and far too little \"imagine if you couldn't have kids\" talk.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q18950a980f",
  "kind": "yes/no",
  "text": "Claim: The Casey Jr. is a water play area across from Dumbo the Flying Elephant, an aerial carousel-style ride located in Fantasyland at six Disney parks around the world.\n\nPassages:\n\n[Casey Jr. Splash 'n' Soak Station]\nThis attraction is a water play area across from the Dumbo the Flying Elephant ride and The Barnstormer starring the Great Goofini.\n\n[Dumbo the Flying Elephant]\nDumbo the Flying Elephant is an aerial carousel-style ride located in Fantasyland at six Disney parks around the world.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qfb580471b0",
  "kind": "yes/no",
  "text": "Claim: In 1926 the daughter of the man who popularized the adage \"A language is a dialect with an army and navy\" was born.\n\nPassages:\n\n[Max Weinreich]\nMax Weinreich (22 April 1894 in Kuldīga, Russian Empire, now Latvia – 29 January 1969 in New York City, United States) was a Russian Jewish linguist, specializing in sociolinguistics and Yiddish, and the father of the linguist Uriel Weinreich, who edited the \"Modern Yiddish-English English-Yiddish Dictionary\".\n\n[A language is a dialect with an army and navy]\nThe adage was popularized by the sociolinguist and Yiddish scholar Max Weinreich, who heard it from a member of the audience at one of his lectures.\n\n[Uriel Weinreich]\nUriel Weinreich (Yiddish: אוריאל ווײַנרײַך‎ \"Uriel Vaynraykh\", ] ; 23 May 1926 – 30 March 1967) was a Polish-American linguist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb9f2d86486",
  "kind": "yes/no",
  "text": "Claim: Fàn County falls under the jurisdiction of a city in Mojiang. That city and Pu'er City are located in the same country.\n\nPassages:\n\n[Fan County]\nFàn County or Fànxian falls under the jurisdiction of Puyang, Henan Province.\n\n[Puyang]\nPuyang is a prefecture-level city in northeastern Henan province, People's Republic of China.\n\n[Pu'er City]\nPu'er () is a prefecture-level city in southern Yunnan Province, China.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe8c792b919",
  "kind": "yes/no",
  "text": "Claim: The 2012 World Indoor Archery Championships was contested at a hotel owned and operated by Michael Gaughan.\n\nPassages:\n\n[South Point Hotel, Casino &amp; Spa]\nThe casino is owned and operated by Michael Gaughan and it serves as the primary sponsor of Gaughan's son Brendan Gaughan's race car.\n\n[2012 World Indoor Archery Championships]\nThe event was contested at the South Point Hotel, and the event was followed by the World Archery Festival and the finals of the second Indoor Archery World Cup.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8639639137",
  "kind": "yes/no",
  "text": "Tweet: victoria has a crush on maluma",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q736d4367df",
  "kind": "yes/no",
  "text": "Claim: This punk-influenced band and Catherine are linked by the rock genre of music. They released the compilation album The Best: Make the Music Go Bang!.\n\nPassages:\n\n[The Best: Make the Music Go Bang!]\nis a compilation American punk rock band X released in 2004.\n\n[Catherine (alternative rock band)]\nCatherine was an alternative rock band from Chicago, Illinois that was active from 1985 to 1998.\n\n[X (American band)]\nX is an American punk rock band, formed in Los Angeles in 1977, among the first wave of American punk.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q748e771be9",
  "kind": "yes/no",
  "text": "Claim: Children's Island is a Swedish Drama Film released in 1980. The director of A Girl in Every Port (1952 film) has served in more film related job positions than the director of this film.\n\nPassages:\n\n[Children's Island (film)]\nChildren's Island (Swedish: Barnens ö ) is a Swedish Drama Film which was released to cinemas in Sweden on 25 December 1980, directed by Kay Pollak, starring Thomas Fryk and Ingvar Hirdwall.\n\n[Chester Erskine]\nChester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.\n\n[Kay Pollak]\nKay Gunnar Leopold Pollak (born 21 May 1938) is a Swedish film director.\n\n[A Girl in Every Port (1952 film)]\nA Girl in Every Port is a 1952 comedy film directed by Chester Erskine.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa26be58302",
  "kind": "yes/no",
  "text": "Claim: The Afghani city of Jalālābād is called جلال اباد‎ ‎ in the main language among a diaspora. The diaspora has it's largest community in the country that Kotli Loharan East is in.\n\nPassages:\n\n[Kotli Loharan East]\nKotli Loharan East is a town in the Punjab province of Pakistan.\n\n[Jalalabad]\nJalālābād (Pashto/Persian: جلال اباد‎ ‎ ), formerly called Ādīnapūr (Pashto: آدينه پور‎ ) as documented by the 7th century Hsüan-tsang, is a city in eastern Afghanistan.\n\n[Pashtun diaspora]\nPakistan is home to the largest Pashtun community.\n\n[Pashto]\nPashto is the main language among the Pashtun diaspora around the world.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q94886cb9a3",
  "kind": "yes/no",
  "text": "Claim: The area ruled by Shahuji II from 1738 to 1739 is an important religious, art, and architecture city in India. This city had a court musician in the 18th century. The court musician had a student called Ghanam Krishna Iyer.\n\nPassages:\n\n[Ghanam Krishna Iyer]\nKrishna Iyar was a student of the famous composer, Pacchimiriam Adiyappa.\n\n[Pacchimiriam Adiyappa]\nPacchimiriam Adiyappa was a famous court musician at the Maratha kingdom of Thanjavur in the 18th century.\n\n[Thanjavur]\nThanjavur, formerly Tanjore, is a city in the south Indian state of Tamil Nadu. Thanjavur is an important center of South Indian religion, art, and architecture.\n\n[Shahuji II]\nShahuji II Bhonsle of Katturaja of the Bhonsle dynasty was the name of the ruler of Thanjavur from 1738 to 1739 who rose to power based on the unverified claim of being an illegitimate son of Serfoji I.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc229a63751",
  "kind": "yes/no",
  "text": "Claim: This mountain was in the 1999 movie Killer Mountain. It's higher than Jongsong Peak.\n\nPassages:\n\n[Gangkhar Puensum]\nGangkhar Puensum (Dzongkha: གངས་དཀར་སྤུན་གསུམ་ \"Kangkar Punsum \", alternatively, Gangkar Punsum or Gankar Punzum) is the highest mountain in Bhutan and a strong candidate for the highest unclimbed mountain in the world with an elevation of 7570 m and a prominence of 2995 m .\n\n[Jongsong Peak]\nAt 7462 m it is the 57th highest peak in the world, although it is dominated by 3rd highest, Kangchenjunga, 20 km to the south.\n\n[Killer Mountain]\nThis sci-fi film tells the story of mountain climbers sent to rescue a missing expedition from a forbidden mountain (Gangkhar Puensum) only to discover the legendary Shangri-La and the hungry creature protecting it, the Druk.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qea226101fd",
  "kind": "yes/no",
  "text": "Claim: Wayne B. Sappleton was a movie star at an institution founded in 1870.\n\nPassages:\n\n[Wayne Sappleton]\nWayne B. Sappleton (born November 17, 1960) is a retired Jamaican professional basketball player, formerly of the NBA's New Jersey Nets. A 6'9 forward, Sappleton was a star at Loyola University Chicago from 1978-82.\n\n[Loyola University Chicago]\nLoyola University Chicago (often referred to as Loyola or LUC) is a private American Catholic research university located in Chicago, Illinois. Founded in 1870 by the Jesuits, today Loyola is one of the largest Catholic universities in the nation and a major contributor to Chicago's economic and cultural capital.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q675942bb21",
  "kind": "yes/no",
  "text": "Claim: The actor who starred, along with Go Ah-sung, in the South-Korean film, Office, appeared in The Deal. The Deal was directed by Son Yong-ho.\n\nPassages:\n\n[Office (2015 South Korean film)]\nOffice (오피스 ) is 2015 South Korean slasher-thriller film directed by Hong Won-chan and starring Go Ah-sung and Park Sung-woong.\n\n[Park Sung-woong]\nPark Sung-woong (born January 9, 1973) is a South Korean actor. Following his acting debut in \"No. 3\" in 1997, Park has starred in several movies and television series, notably as a gangster in \"New World\" (2013) and a serial killer in \"The Deal\" (2015).\n\n[The Deal (2015 film)]\nThe Deal (; lit.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc8035aaae2",
  "kind": "yes/no",
  "text": "Claim: The Seattle Redhawks women's basketball team can be found in Washington where it is now permanently located since 2011.\n\nPassages:\n\n[Seattle University]\nSeattle University (SU) is a Jesuit Catholic university in the northwestern United States, located in the First Hill neighborhood of Seattle, Washington.\n\n[Seattle Redhawks women's basketball]\nThe Seattle Redhawks women's basketball is the women's basketball team representing Seattle University.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q34488ae2ff",
  "kind": "yes/no",
  "text": "Claim: The improvisational troupe, which trained Amy Sedaris, Paul Dinello, and Stephen Colber, was founded in 1959.\n\nPassages:\n\n[Exit 57]\nExit 57 is a 30-minute sketch comedy series that aired on the American television channel Comedy Central from 1995 to 1996; its cast was composed of comedians Amy Sedaris, Paul Dinello, Stephen Colbert, Jodi Lennon, and Mitch Rouse, all of whom had previously studied improv at The Second City in Chicago.\n\n[The Second City]\nThe Second City Theatre opened on December 16, 1959, and has since become one of the most influential and prolific comedy theatres in the world.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q137e169bf3",
  "kind": "yes/no",
  "text": "Claim: The Colomac Mine was operated by Royal Oak Mines at an earlier date, than the mine in British Columbia, near Kemess Creek Airport.\n\nPassages:\n\n[Kemess Creek Airport]\nKemess Creek Airport, (TC LID: CBQ7) , is located near Kemess Mine, British Columbia, Canada.\n\n[Colomac Mine]\nThe Colomac Mine was a privately owned and operated open pit gold mine located 220 km northwest of Yellowknife in the Northwest Territories in Canada . In 1994, the mine had reopened under Royal Oak Mines Inc.\n\n[Kemess Mine]\nIt was operated by Royal Oak Mines from 1998 to 1999, when it was bought by Northgate Minerals.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2b86c4a56f",
  "kind": "yes/no",
  "text": "Claim: Sam Kinison is the former pentecostal preacher who released the comedy album Leader of the Banned in 1990.\n\nPassages:\n\n[Leader of the Banned]\nLeader of the Banned is the third Sam Kinison comedy album released in 1990.\n\n[Sam Kinison]\nSamuel Burl \"Sam\" Kinison (December 8, 1953 – April 10, 1992) was an American stand-up comedian and actor. A former Pentecostal preacher, he performed stand-up routines that were most often characterized by an intense style, similar to charismatic preachers, and punctuated by his trademark scream.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q133fd2427d",
  "kind": "yes/no",
  "text": "Claim: The Sierra Nevada mountains are located near this autonomous community, in which Spanish politician Felipe Alcaraz was born.\n\nPassages:\n\n[Granada]\nGranada ( , ] , ] ) is the capital city of the province of Granada, in the autonomous community of Andalusia, Spain. Granada is located at the foot of the Sierra Nevada mountains, at the confluence of four rivers, the Beiro, the Darro, the Genil and the Monachil.\n\n[Felipe Alcaraz]\nLuis Felipe Alcaraz Masats (born 1 March 1943 in Granada) is a Spanish politician.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q567fad94e4",
  "kind": "yes/no",
  "text": "Claim: Adam Minarovich and Core Harrison own the famous pawn shop d Famous Gold & Silver Pawn Shop.\n\nPassages:\n\n[Corey Harrison]\nRichard Corey \"Big Hoss\" Harrison (born April 27, 1983) is an American businessman and reality television personality, known as a cast member of the History TV series \"Pawn Stars\", which documents his work at the World Famous Gold & Silver Pawn Shop in Las Vegas, which he co-owns with his father, Rick Harrison, and grandfather, Richard Benjamin Harrison.\n\n[Rick Harrison]\nRichard Kevin \"Rick the Spotter\" Harrison (born March 22, 1965) is an American, Las Vegas-based businessman and reality television personality, best known as the co-owner of the World Famous Gold & Silver Pawn Shop, as featured on the History series \"Pawn Stars\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q91f37c70eb",
  "kind": "yes/no",
  "text": "Claim: Alan Sillitoe was a novelist. The Poet-Dliplomat who also won the award Theodor Mommsen received in 1902 was also a novelist.\n\nPassages:\n\n[Gabriela Mistral]\nIn 1945 she became the first Latin American author to receive a Nobel Prize in Literature, \"for her lyric poetry which, inspired by powerful emotions, has made her name a symbol of the idealistic aspirations of the entire Latin American world\".\n\n[Theodor Mommsen]\nHe received the Nobel Prize in Literature in 1902 for being \"the greatest living master of the art of historical writing, with special reference to his monumental work \"A History of Rome\"\", after having been nominated by 18 members of the Prussian Academy of Sciences.\n\n[Poet-diplomat]\nThe best known poet-diplomats are perhaps Geoffrey Chaucer and Thomas Wyatt; the category also includes recipients of the Nobel Prize in Literature: Ivo Andrić, Gabriela Mistral, Saint-John Perse, Miguel Ángel Asturias, Pablo Neruda, George Seferis, Czesław Miłosz and Octavio Paz.\n\n[Alan Sillitoe]\nAlan Sillitoe (4 March 192825 April 2010) was an English writer and one of the so-called \"angry young men\" of the 1950s. He disliked the label, as did most of the other writers to whom it was applied.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qed537b4022",
  "kind": "yes/no",
  "text": "Post: Maxwell, Arthur’s middle name is Grandpa’s name. So he has a piece of two very important people of Mikeys family. Grandpa is a incredible guy and this was probably the only thing at this point that we could give him to make him feel appreciated and loved. Grandpa loves his name.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0b812577b3",
  "kind": "yes/no",
  "text": "Claim: Veyyil was the first film scored by the man who composed the soundtrack for the film in which Ashrita Shetty had a part.\n\nPassages:\n\n[G. V. Prakash Kumar]\nHis first film was S Pictures' \"Veyyil\" (2006) and he became popular in Tamil cinema by the early 2010s.\n\n[Ashrita Shetty]\nThis was when film directors Vetrimaaran and Manimaran approached her to play the lead role in their venture, \"Udhayam NH4\".\n\n[Udhayam NH4]\nThe film's soundtrack and background score were composed by G. V. Prakash Kumar.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qaaf16bad2d",
  "kind": "yes/no",
  "text": "Claim: Meesha Shafi, Strings, the vocalist for Jupiters and Shahzad Hasan are judges on the show Friendship. The producer and singer of Aaina joined them.\n\nPassages:\n\n[Ali Azmat]\nAli Azmat (born April 20, 1970) is a Pakistani singer-songwriter, musician and actor.\n\n[Aaina (album)]\nAaina is a musical album produced by Pakistani musician and singer, Alamgir from the soundtrack of the first ground-breaking and the longest running Urdu-language Pakistani movie of the same name in 1976.\n\n[Jupiters]\nThe hit song \"Yaaro Yehi Dosti Hai\" sung by one of the vocalists Ali Azmat topped the charts in the early 1990s, and is still a famous number.\n\n[Alamgir (pop singer)]\nIn April 2013, Alamgir joined Meesha Shafi, Strings, Ali Azmat and Shahzad Hasan as a judge on the immensely popular singing talent show \"Music Icons\" which aired on ARY Digital TV channel.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3dc3af8e36",
  "kind": "yes/no",
  "text": "Post: @isawitfirst With some pastel green flare leggings a Chucky white boot and a hot pink shoulder bag 🧡",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q5ef7dad5c6",
  "kind": "yes/no",
  "text": "Claim: Julia Compton Moore was the wife of the United States Army lieutenant general who received the Distinguished Service Cross, and was the first of his West Point class to be promoted to brigadier general, major general, and lieutenant general.\n\nPassages:\n\n[Julia Compton Moore]\nJulia Compton Moore (February 10, 1929April 18, 2004) was the wife of Lieutenant General (Ret.) Hal Moore, a United States Army officer.\n\n[Hal Moore]\nHarold Gregory \"Hal\" Moore, Jr. (February 13, 1922 – February 10, 2017) was a United States Army lieutenant general and author. He was a recipient of the Distinguished Service Cross, which is the U.S. military's second highest decoration for valor, and was the first of his West Point class (1945) to be promoted to brigadier general, major general, and lieutenant general.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf249f2fdb8",
  "kind": "yes/no",
  "text": "Claim: The radio station WMBH is located in the southwestern corner of Missouri.\n\nPassages:\n\n[Joplin, Missouri]\nJoplin ( ) or ( ) is a city in southern Jasper County and northern Newton County in the southwestern corner of the U.S. state of Missouri.\n\n[WMBH]\nWMBH (1560 AM) is a radio station licensed to Joplin, Missouri.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q61752f4760",
  "kind": "yes/no",
  "text": "Claim: The Fuel album Puppet Strings featured it's original Irish lead singer. Feul's lead singer and a celebrity that wore the Shag (haircut) are both musicians.\n\nPassages:\n\n[Brett Scallions]\nBrett Allen Scallions (born December 21, 1971) is an American musician.\n\n[Puppet Strings]\nReleased March 4, 2014, it is their first studio effort since 2003's \"Natural Selection\" to feature original lead singer Brett Scallions and the first Fuel album not to feature original songwriter/guitarist, Carl Bell and bassist Jeff Abercrombie.\n\n[Shag (haircut)]\nThis unisex style became popular after being worn by various celebrities, including Joan Jett, Mick Jagger, Rod Stewart, David Cassidy, Jane Fonda and Florence Henderson in the 1970s.\n\n[Mick Jagger]\nSir Michael Philip Jagger, MBE (born 26 July 1943) is an English singer-songwriter, multi-instrumentalist, and composer, who gained fame as the lead singer and one of the founder members of the Rolling Stones (1962-present).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8d4d7b68ee",
  "kind": "yes/no",
  "text": "Claim: Eric Edward Whitacre \"Virtual Choir\"-noted conductor has created works for the Austin-based ensemble who released the opera writer's Threshold of Night. He also wrote the opera Edward Dick in 2005.\n\nPassages:\n\n[Conspirare]\nConspirare has commissioned works from composers including David Lang, Tarik O'Regan, Jocelyn Hagen, Donald Grantham, Eric Whitacre, Nico Muhly, Mark Adamo, Robert Kyr, Jake Heggie, Eric Banks, and Jake Runestad.\n\n[Edward Dick]\nIn 2008 he directed Benjamin Britten's opera \"The Rape of Lucretia\" at Aldeburgh, and in 2011 he directed a new opera by Tarik O'Regan at the Royal Opera House in London.\n\n[Tarik O'Regan: Threshold of Night]\nTarik O'Regan: Threshold of Night is the third release by the choral group Conspirare and the second recording of the work of Tarik O'Regan.\n\n[Eric Whitacre]\nEric Edward Whitacre (born January2, 1970) is a Grammy-winning American composer, conductor, and speaker, known for his choral, orchestral and wind ensemble music. He is also known for his \"Virtual Choir\" projects, bringing individual voices from around the globe together into an online choir.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q521c7f3008",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "The healthcare system in the U.S is so frustrating. I spend so much money on health insurance only to end up paying just as much out of pocket when my insurance doesn’t cover the services.",
   "I love health insurance so much fun paying $100’s a month and then $100’s for basic medical services that somehow aren’t covered. #America"
  ]
 },
 {
  "qid": "q979ffbc09a",
  "kind": "yes/no",
  "text": "Claim: The film, The Cat In The Hat, starring an actress that starred in The Experts (1989 film) was a comedy film. The comedy film was directed by production designer and director Robert W. \"Bo\" Welch III.\n\nPassages:\n\n[Kelly Preston]\nShe also starred in the films \"The Cat in the Hat\", \"Old Dogs\", and \"Broken Bridges\".\n\n[Bo Welch]\nRobert W. \"Bo\" Welch III (born November 30, 1951) is an American production designer and director.\n\n[The Cat in the Hat (film)]\nDr. Seuss' The Cat in the Hat is a 2003 American family comedy film directed by Bo Welch.\n\n[The Experts (1989 film)]\nThe Experts is a 1989 American comedy film starring John Travolta, Arye Gross and Kelly Preston.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q9abd03d8ab",
  "kind": "yes/no",
  "text": "Claim: The Cincinnati metropolitan area at the south of the location where DMAX (engines) is based had a population of 2,114,580 in 2010 U.S. Census.\n\nPassages:\n\n[Cincinnati metropolitan area]\nAs of the 2010 U.S. Census, this MSA had a population of 2,114,580, the largest metropolitan area involving Ohio and 27th largest in the United States.\n\n[Moraine, Ohio]\nMoraine, as part of the Dayton area, is situated within the Miami Valley region of Ohio, just north of the Cincinnati metropolitan area.\n\n[DMAX (engines)]\nDMAX of Moraine, Ohio, is a manufacturer of diesel engines for trucks. DMAX, originally announced in December 1998, is a 60-40 joint venture between and operated by General Motors and Isuzu.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf1193dd6ec",
  "kind": "yes/no",
  "text": "Claim: The Eek! segment of the hentai anime show Klutter was created by David Silverman and a man that manages Savage Studios Ltd.\n\nPassages:\n\n[Savage Steve Holland]\nNow, he manages his own studio, Savage Studios Ltd. and directs shows for Disney Channel and Nickelodeon.\n\n[Klutter!]\nIt was created by David Silverman and Savage Steve Holland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7d8319f535",
  "kind": "yes/no",
  "text": "Claim: The person the story behind Girl Crazy is credited to is older than a particular director. This director directed \"Edna, the Inebriate Woman\".\n\nPassages:\n\n[Girl Crazy (1929 film)]\nThe film's story is credited to Hampton Del Ruth, Alfred J. Goulding, Harry McCoy, Earle Rodney, and Mack Sennett.\n\n[Hampton Del Ruth]\nHampton Del Ruth (September 7, 1879 – May 15, 1958) was an American film actor, director, screenwriter, and film producer.\n\n[Edna, the Inebriate Woman]\nDirected by Ted Kotcheff, Irene Shubik produced it.\n\n[Ted Kotcheff]\nWilliam Theodore \"Ted\" Kotcheff (born April 7, 1931; as Velichko Todorov Tsochev) is a Bulgarian-Canadian film and television director and producer, known primarily for his work on several high-profile British and American television productions such as \"Armchair Theatre\" and \"\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb0286c0019",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Ew this toilet seat is warmed up.",
   "when the toilet seat is warmed up for you&gt;&gt;&gt;"
  ]
 },
 {
  "qid": "q151913d777",
  "kind": "yes/no",
  "text": "Claim: Ranjhay Hath Gandasa is a 1986 comedy film starring Pakistani-American singer-songwriter Nadia Ali.\n\nPassages:\n\n[Nadia Ali (singer)]\nNadia Ali (Urdu: ‎ , born 3 August 1980) is a Pakistani American singer-songwriter.\n\n[Ranjhay Hath Gandasa]\nIt stars Nadia Ali, Rana Rehman, Fozia Rana, Durdana Rehman, Azhar Rangeela and Shafqat Cheema in lead roles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa546c80f63",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I'm so nervous I hope I'll forget how to play to avoid being onstage.",
   "it's too bad i forgot how to play my clarinet so close to my recital"
  ]
 },
 {
  "qid": "q5dc64c7200",
  "kind": "yes/no",
  "text": "Claim: Tata Movus is a type of Minivan found only in the Ukraine.\n\nPassages:\n\n[Minivan]\nA minivan (American English), people carrier (British English), or MPV (multi-purpose vehicle) or MUV (multi-utility vehicle) is a vehicle size classification describing a high-roof vehicle with a flexible interior layout.\n\n[Tata Movus]\nTata Movus (or Movus) is Minivan (MUV) manufactured by Tata Motors.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7a98d7ed50",
  "kind": "yes/no",
  "text": "Claim: The Dutch designers of the Horten H.XVIII also designed the world's first jet-powered flying wing known as Horten Ho 229.\n\nPassages:\n\n[Horten brothers]\nAlthough they had little, if any, formal training in aeronautics or related fields, the Hortens designed some of the most revolutionary aircraft of the 1940s, including the world's first jet-powered flying wing, the Horten Ho 229.\n\n[Horten H.XVIII]\nThe Horten H.XVIII was a proposed German World War II intercontinental bomber, designed by the Horten brothers with pioneering features such as a flying wing configuration, turbojet engines and stealth characteristics.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2432b8e5be",
  "kind": "yes/no",
  "text": "Claim: Francois de Fleury served in a battle in the American Revolutionary War in June of 1778. Henry Monckton was killed during that battle.\n\nPassages:\n\n[Henry Monckton]\nHe was killed leading his soldiers at the Battle of Monmouth on 28 June 1778.\n\n[Battle of Monmouth]\nThe Battle of Monmouth was an American Revolutionary War battle fought on June 28, 1778, in Monmouth County, New Jersey.\n\n[François de Fleury]\nHe served during the Monmouth Campaign in June 1778 and fought in Rhode Island in August.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7cf00a9469",
  "kind": "yes/no",
  "text": "Claim: Rudolf Kjellén's work was influenced by the person who coined the phrase Lebensraum; the political movement which made it notorious by taking it to extremes was the German Nazi Party.\n\nPassages:\n\n[Lebensraum]\n<ref name=\"E/N301\"> </ref> The most extreme form of this ideology was supported by the Nazi Party (NSDAP) and Nazi Germany until the end of World War II.\n\n[Friedrich Ratzel]\nFriedrich Ratzel (August 30, 1844 – August 9, 1904) was a German geographer and ethnographer, notable for first using the term \"Lebensraum\" (\"living space\") in the sense that the National Socialists later would.\n\n[Rudolf Kjellén]\nHis work was influenced by Friedrich Ratzel.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 }
]
