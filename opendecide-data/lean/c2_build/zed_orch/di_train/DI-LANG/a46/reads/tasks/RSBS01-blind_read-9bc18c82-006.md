# A46 replay label-noise blind read RSBS01-blind_read-9bc18c82-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS01-blind_read-9bc18c82-006.json

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
  "qid": "q1501e9d544",
  "kind": "yes/no",
  "text": "Claim: Leigh Silverman was nominated for the 2014 Tony Award, Best Direction for a musical based on the short story The Ugliest Pilgrim.\n\nPassages:\n\n[Leigh Silverman]\nLeigh Silverman is an American director for the stage, both Off-Broadway and on Broadway. She was nominated for the 2014 Tony Award, Best Direction of a Musical for the musical \"Violet\" and the 2008 Drama Desk Award, Outstanding Director of a Play for the play \"From Up Here\".\n\n[Violet (musical)]\nViolet is a musical with music by Jeanine Tesori and libretto by Brian Crawley based on the short story \"The Ugliest Pilgrim\" by Doris Betts.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9316ce5022",
  "kind": "yes/no",
  "text": "Claim: Milo Parker starred in the 2014 movie Robot Overlords alongside Gillian Anderson.\n\nPassages:\n\n[Milo Parker]\nMilo Parker (born 2002) is a British child actor, known for his roles as Connor in \"Robot Overlords\", Roger Munro in \"Mr. Holmes\" and Hugh Apiston in \"Miss Peregrine's Home for Peculiar Children\".\n\n[Robot Overlords]\nRobot Overlords (originally titled Our Robot Overlords) is a 2014 British independent science fiction film, starring Callan McAuliffe, Ben Kingsley and Gillian Anderson.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe35a1ffc0d",
  "kind": "yes/no",
  "text": "Claim: Both Cocky and cockfights have the rooster in common.\n\nPassages:\n\n[Cockfight]\nA cockfight is a blood sport between two cocks, or gamecocks, held in a ring called a cockpit.\n\n[Cocky (mascot)]\nCocky is the costumed mascot of the University of South Carolina athletics teams. He represents a cartoon version of a gamecock (a fighting rooster).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3cb97533a6",
  "kind": "yes/no",
  "text": "Text: every time i see someone named david im like ….. wow… that really IS a guy named david",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q02439aec12",
  "kind": "yes/no",
  "text": "Tweet: help why do i keep having nightmares about being amish",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q30690acc7b",
  "kind": "yes/no",
  "text": "Claim: Dave Thomas, who also founded the Dave Thomas Foundation for Adoption, the non-for-profit organization dedicated to find adoptive homes for children waiting in North America's foster care system that was named for Wendy, who is also the namesake and mascot of the company founded Wendy's.\n\nPassages:\n\n[Dave Thomas Foundation for Adoption]\nThe Dave Thomas Foundation for Adoption is a not-for-profit organization dedicated to finding adoptive homes for children waiting in North America’s foster care system.\n\n[Wendy Thomas]\nMelinda Lou \"Wendy\" Morse (née Thomas; born September 14, 1961) is the daughter and fourth child of American businessman Dave Thomas, the founder of the fast food brand Wendy's. Morse is best known for being the namesake and mascot of the brand.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q7ac4139902",
  "kind": "yes/no",
  "text": "Claim: Straight Blast Gym - Ireland and John Kavanagh have visual arts in common.\n\nPassages:\n\n[John Kavanagh (martial artist)]\nJohn Raymond Kavanagh (born January 18, 1977) is an Irish martial arts coach, brazilian jiu-jitsu practitioner and former professional mixed martial artist.\n\n[Straight Blast Gym - Ireland]\nStraight Blast Gym Ireland is a mixed martial arts academy and professional team based in Dublin, Ireland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf83664dd18",
  "kind": "yes/no",
  "text": "Post: do i just blast maneskin to get hyped for my osce or??",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q5fe4d558a4",
  "kind": "yes/no",
  "text": "Tweet: thinking about that time when a week after i broke up with him my ex sent me a playlist to tell me all his feelings from throughout our 3 week relationship+how he felt about it ending and the whole thing was just john mayer songs",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q4998eaac07",
  "kind": "yes/no",
  "text": "Claim: The father of Prince Georgy Konstantinovich of Russia was the grandson and tennis partner of Emperor Nicholas 1 who was the father of Princh John Konstantinovich of Russia.\n\nPassages:\n\n[Grand Duke Konstantin Konstantinovich of Russia]\nGrand Duke Konstantin Konstantinovich of Russia (Russian: Константи́н Константи́нович ; ] ; 22 August 1858 in Strelna – 15 June 1915 in Pavlovsk) was a grandson of Emperor Nicholas I of Russia, and a poet and playwright of some renown.\n\n[Prince John Konstantinovich of Russia]\nPrince Ioann Konstantinovich of Russia (Russian: Иоанн Константинович ) (5 July 1886 – 18 July 1918), sometimes also known as Prince John, Prince Ivan or Prince Johan, was the eldest son of Grand Duke Konstantin Konstantinovich of Russia by his wife Yelizaveta Mavrikievna, née Princess Elisabeth of Saxe-Altenburg.\n\n[Prince Georgy Konstantinovich of Russia]\nPrince Georgy Konstantinovich of Russia (6 May 1903 – 7 November 1938), was the youngest son of Grand Duke Konstantin Konstantinovich of Russia and his wife Grand Duchess Yelizaveta Mavrikiyevna.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe3f0e4e9a6",
  "kind": "yes/no",
  "text": "Claim: The lead drummer of the Belgian band Stand by Me is known for innovation in funk music.\n\nPassages:\n\n[Stand by Me (Whatcha See Is Whatcha Get)]\nStand By Me (Whatcha See Is Whatcha Get) is an album led by jazz drummer Bernard Purdie which was recorded for the Mega label in 1971.\n\n[Bernard Purdie]\nBernard Lee \"Pretty\" Purdie (born June 11, 1941) is an American drummer, considered an influential and innovative funk musician.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q192b6965ea",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I feel like too many people say that they're allergic to pineapple when they really aren't.",
   "people who say that they’re allergic to pineapple are pathological liars!!!!!!!"
  ]
 },
 {
  "qid": "q5108f9c672",
  "kind": "yes/no",
  "text": "Claim: The father of director Guðný Halldórsdóttir and psychonaut Timothy Leary are not from the same country.\n\nPassages:\n\n[Timothy Leary]\nTimothy Francis Leary (October 22, 1920 – May 31, 1996) was an American psychologist and writer known for advocating the exploration of the therapeutic potential of psychedelic drugs under controlled conditions.\n\n[Halldór Laxness]\nHalldór Kiljan Laxness (] ; born Halldór Guðjónsson; 23 April 1902 – 8 February 1998) was a twentieth-century Icelandic writer.\n\n[Guðný Halldórsdóttir]\nHer father was writer and 1955 Nobel prize winner Halldór Laxness, while her mother was writer and textile designer Auður Laxness.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6350aec13e",
  "kind": "yes/no",
  "text": "Text: @bwin Is there a problem with the predictor page? Its not loading so unable to enter my predictions.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q2ec76d7826",
  "kind": "yes/no",
  "text": "Claim: One of the legendary four aces skaters was born in the third largest city in Norway. The others were Jan Egil Storholt, Amund Sjøbrend and Kay Stenshjemmet.\n\nPassages:\n\n[Sten Stensen]\nTogether with Amund Sjøbrend, Kay Stenshjemmet, and Jan Egil Storholt, he was one of the legendary \"four S-es\" (\"four aces\" in Norwegian), contemporary Norwegian top skaters in the 1970s and early 1980s.\n\n[Trondheim]\nIt is the third largest city in the country, with a population (2013) of 169,972 inhabitants within the city borders.\n\n[Jan Egil Storholt]\nJan Egil Storholt (born 13 February 1949) is a former speed skater from Norway. He was born in Trondheim.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9a72e259a0",
  "kind": "yes/no",
  "text": "Claim: The co-star of the South Korean show Maids (2015 TV series) played an obsessed and tormented king in the 2012 South Korean historical film directed by Kim Da-bin.\n\nPassages:\n\n[Maids (2015 TV series)]\nMaids () is a 2015 South Korean television series starring Jeong Yu-mi, Oh Ji-ho, Kim Dong-wook, Lee Si-a, Jeon So-min and Lee Yi-kyung.\n\n[Kim Dong-wook]\nHe then starred in \"Happy Killers\" (2010) and \"Romantic Heaven\" (2011), but it was his acclaimed performance as an obsessed and tormented king in 2012 period drama \"The Concubine\" that brought Kim the best reviews of his career yet.\n\n[The Concubine (film)]\n\"Royal Concubine: Concubine to the King\") is a 2012 South Korean historical film directed by Kim Dae-seung.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2966716501",
  "kind": "yes/no",
  "text": "Claim: Kingdom Hearts 358/2 Days was made by the company based in Shinjuku, Tokyo.\n\nPassages:\n\n[Kingdom Hearts 358/2 Days]\nKingdom Hearts 358/2 Days (キングダム ハーツ 358/2 Days , Kingudamu Hātsu Surī Faibu Eito Deizu Ōbā Tsū , subtitle read as \"Three Five Eight Days Over Two\") is an action role-playing video game developed by h.a.n.d. and Square Enix for the Nintendo DS.\n\n[Square Enix]\nThe Square Enix headquarters are in the Shinjuku Eastside Square Building in Shinjuku, Tokyo.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qdb34e96105",
  "kind": "yes/no",
  "text": "Text: Anyone else hear some like thunder or something?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q0cb639f146",
  "kind": "yes/no",
  "text": "Claim: At the Tomorrowland summer festival you might find music by the producer that made the punk-rock song One Day (Vandaag).\n\nPassages:\n\n[Bakermat]\nHis music consists of a mix of electronic, deep and tropical house, techno music produced in a minimalist manner with jazz and soul influences.\n\n[Tropical house]\nArtists of the genre are often featured at various summer festivals such as Tomorrowland.\n\n[One Day (Vandaag)]\n\"Vandaag\" is a song by Dutch producer Bakermat.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q353004f33e",
  "kind": "yes/no",
  "text": "Claim: Moroni is the historic capital of the archipelago where Djoièzi is located.\n\nPassages:\n\n[Djoièzi]\nDjoièzi is a village on the island of Mohéli in the Comoros.\n\n[Comoros]\nIts capital is Moroni, on Grande Comore.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q19a277e472",
  "kind": "yes/no",
  "text": "Claim: Cathouse: The Series documents the lives of workers in a legal brothel on Moonlight Road. It is a few minutes outside of the birthplace of James Settelmeyer.\n\nPassages:\n\n[James Settelmeyer]\nSettelmeyer was born in Carson City, and now lives and works on his family ranch in Carson Valley.\n\n[Moonlite BunnyRanch]\nThe Moonlite BunnyRanch (often misspelled \"Moonlight\", though that is the correct spelling of the road on which it is addressed) is a legal, licensed brothel in Mound House, Nevada, United States, 6 mi east of Carson City.\n\n[Dennis Hof]\nSeveral of his brothels are in Moundhouse, Nevada, a few minutes outside Carson City.\n\n[Cathouse: The Series]\nCathouse: The Series is an HBO television series that documents the professional lives of the workers at the Moonlite BunnyRanch, a legal brothel in Nevada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q81286146ed",
  "kind": "yes/no",
  "text": "Post: You’d never be able to sell me magnetic lashes",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qd084592e66",
  "kind": "yes/no",
  "text": "Claim: Naomi Yashiro has been working as a cabin crew at a major airlaine headquartered in Shinagawa, Tokyo, Japan.\n\nPassages:\n\n[Naomi Yashiro]\nNaomi Yashiro (矢代直美, born 30 December 1977) is a Japanese former basketball player who competed in the 2004 Summer Olympics. She has been working as a cabin crew at the Japan Airlines and joined its team JAL Rabbits.\n\n[Japan Airlines]\nJapan Airlines Co., Ltd. (JAL) (日本航空株式会社 , Nihon Kōkū Kabushiki-gaisha , , OTC Pink: JAPSY) , is the flag carrier airline of Japan and the second largest in the country behind All Nippon Airways. It is headquartered in Shinagawa, Tokyo, Japan; and its main hubs are Tokyo's Narita International Airport and Tokyo International Airport (Haneda Airport), as well as Osaka's Kansai International Airport and Osaka International Airport.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2670c449fb",
  "kind": "yes/no",
  "text": "Claim: Microcachrys, and not Bee tree, is a formal name of a species of tree.\n\nPassages:\n\n[Bee tree]\nA bee tree is a tree in which a colony of honey bees makes its home.\n\n[Microcachrys]\nMicrocachrys tetragona (Creeping Pine or Creeping Strawberry Pine) is a species of dioecious conifer belonging to the podocarp family (Podocarpaceae).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3fbcb40373",
  "kind": "yes/no",
  "text": "Claim: Adeyfield and Hemel Hempstead are both from England.\n\nPassages:\n\n[Adeyfield]\nAdeyfield was the first planned neighbourhood to be built in the postwar new town expansion of Hemel Hempstead, in the English county of Hertfordshire.\n\n[Hemel Hempstead]\nHemel Hempstead is a new town in Hertfordshire, England.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbda1845e39",
  "kind": "yes/no",
  "text": "Claim: Rennae Stubs who teamed up with Elena Bovina for the 2003 Family Circle Cup – Doubles. Her and Renáta Tomanová were both tennis players\n\nPassages:\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.\n\n[2003 Family Circle Cup – Doubles]\nLisa Raymond and Rennae Stubbs were the defending champions, but Raymond did not compete in this edition.\n\n[Rennae Stubbs]\nRennae Stubbs (born 26 March 1971) is an Australian retired tennis player.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9ac67ae6d2",
  "kind": "yes/no",
  "text": "Claim: Monorail is a rock band. So is the band whose drummer is a man. This man featured in the +/- album You Are Here.\n\nPassages:\n\n[Versus (band)]\nVersus is an American indie rock band formed in 1990 by Richard Baluyut, Fontaine Toups, and Edward Baluyut in New York City.\n\n[Patrick Ramos]\nPatrick Ramos is a Filipino American musician who is notable as drummer for key 1990s indie group Versus, and singer, songwriter, guitarist and keyboardist for 2000s indietronic group +/-.\n\n[You Are Here (+/- album)]\nIt was the first full-length release to feature the line-up of James Baluyut, Chris Deaner and Patrick Ramos.\n\n[Monoral]\nMonoral is a Japanese alternative rock band signed to Sony Music Japan.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf0a3481284",
  "kind": "yes/no",
  "text": "Claim: The Detroit, Michigan American rapper, who was born in 1973, was featured in a guest appearance on Domino debut studio album. \"Welcome 2 Detroit\" is the lead single of that album.\n\nPassages:\n\n[The People vs.]\nThe album also featured guest appearances by the likes of Obie Trice, Miz Korona, Jazze Pha, a one-half of D12 members (Proof, Kon Artis and Eminem), and his brother and Goon Sqwad bandmate Diezel.\n\n[Welcome 2 Detroit (song)]\n\"Welcome 2 Detroit\" is the lead single from American rapper Trick-Trick's debut studio album, \"The People vs.\".\n\n[Proof (rapper)]\nDeShaun Dupree Holton (October 2, 1973 – April 11, 2006), better known by his stage name Proof, was an American rapper and actor from Detroit, Michigan.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc70c368c5e",
  "kind": "yes/no",
  "text": "Claim: Lee Il-hyung's first feature film was released by Showbox.\n\nPassages:\n\n[A Violent Prosecutor]\nIt was released in South Korea on February 3, 2016 by Showbox.\n\n[Lee Il-hyung]\nPrior to directing his first feature film \"A Violent Prosecutor\" (2016), Lee is an assistant director on films, such as \"The Moonlight of Seoul\" (2008), \"My Way\" (2011) and \"\" (2014), and commercial films.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4326f6081f",
  "kind": "yes/no",
  "text": "Claim: Edmund Valentine White III wrote a play in 2006 and a book on homosexual sex in 1977.\n\nPassages:\n\n[Edmund White]\nEdmund Valentine White III (born January 13, 1940) is an American novelist, memoirist, and an essayist on literary and social topics. His books include \"The Joy of Gay Sex\" (1977) (written with Charles Silverstein), his trio of autobiographic novels, \"A Boy's Own Story\" (1982), \"The Beautiful Room Is Empty\" (1988) and \"The Farewell Symphony\" (1997), and his biography of Jean Genet.\n\n[Terre Haute (play)]\nTerre Haute is a 2006 play by the American writer Edmund White.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q05d2463577",
  "kind": "yes/no",
  "text": "Claim: A song by David Guetta was produced by the Dutch DJ Afrojack. The signer who recorded I Don't Wanna Grow Up guested on this song.\n\nPassages:\n\n[Hey Mama (David Guetta song)]\n\"Hey Mama\" is a song by French DJ and record producer David Guetta, featuring vocals from Nicki Minaj and Bebe Rexha, as well as production from Dutch DJ and producer Afrojack.\n\n[I Don't Wanna Grow Up]\nI Don't Wanna Grow Up is the debut extended play (EP) by American pop recording artist Bebe Rexha.\n\n[Bebe Rexha]\nShe is best known as a featured guest vocalist on several \"Billboard\" Hot 100 charting songs, such as G-Eazy's \"Me, Myself & I\", David Guetta's \"Hey Mama\", Martin Garrix's \"In the Name of Love\" and Cash Cash's \"Take Me Home\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4d8d0fca76",
  "kind": "yes/no",
  "text": "Claim: People's Republic of China politician Wan Da was born in this location. It has a larger population than area where the Liaoning Finance and Trade College is located.\n\nPassages:\n\n[Xingcheng]\nXingcheng (), former name Ningyuan (宁远), is a county-level city of southwest Liaoning province, China, with a population of approximately 140,000 urban inhabitants, and is located on the Liaodong Bay, i.e. the northern coast of the Bohai Sea.\n\n[Wan Da]\nHe was born in Linzhou, Henan.\n\n[Liaoning Finance and Trade College]\nLiaoning Finance and Trade College (), formerly known as Shenyang Shifan University Bohai College, is a small, partially walled private undergraduate college located on the Liaodong Bay of the Bohai coast in Xingcheng, southwest of Huludao in Liaoning province on the east coast of China.\n\n[Linzhou, Henan]\nIt covers an area of 2046 square kilometers and has a population of about one million.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qcd734ae7d8",
  "kind": "yes/no",
  "text": "Claim: The Ilion Animation Studios produced CGI-animated film from 2009 was 3D. The 2009 animated film written and directed by Phil Lord and Christopher Miller was not in 3D.\n\nPassages:\n\n[Cloudy with a Chance of Meatballs (film)]\nCloudy with a Chance of Meatballs is a 2009 American computer-animated science fiction comedy film loosely based on the 1978 children's book of the same name by Judi and Ron Barrett.\n\n[Planet 51]\nPlanet 51 is a 2009 Spanish and American-British-movie 3D computer-animated science fiction comedy film directed by Jorge Blanco, written by Joe Stillman, and starring Dwayne Johnson, Jessica Biel, Justin Long, Gary Oldman, Seann William Scott, and John Cleese.\n\n[Phil Lord and Christopher Miller]\nThey are known for directing and writing the animated films \"Cloudy with a Chance of Meatballs\" (2009) and \"The Lego Movie\" (2014), as well as directing the live-action comedy film \"21 Jump Street\" (2012) and its sequel (2014).\n\n[Ilion Animation Studios]\nIlion produced the CGI-animated film, \"Planet 51\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3cae7ca43d",
  "kind": "yes/no",
  "text": "Claim: An American rock band released Needing/Getting in Fall 2010. This band and the band who Todd Fancey plays guitar for were formed in different cities.\n\nPassages:\n\n[Needing/Getting]\n\"Needing/Getting\" is a song by American rock band OK Go, from their 2010 album \"Of the Blue Colour of the Sky\".\n\n[OK Go]\nOK Go is an American rock band originally from Chicago, Illinois, now based in Los Angeles, California.\n\n[Todd Fancey]\nHe is most widely known as the guitarist for Vancouver-based indie rock band The New Pornographers and the bassist for the band Limblifter.\n\n[The New Pornographers]\nThe New Pornographers is a Canadian indie rock band formed in 1997 in Vancouver, British Columbia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc3487ff6c0",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "IF ONLY PEOPLE WOULD RAKE THE FORESTS. #Debate2020",
   "The president seems to believe that merely removing leaves from forest floors would prevent forest fires."
  ]
 },
 {
  "qid": "q9d034f7925",
  "kind": "yes/no",
  "text": "Claim: The station that has Ong-Art Singlumpong for an executive director has broadcast the American sports HBO World Championship Boxing that premiered in the early 1970s.\n\nPassages:\n\n[Channel 8 (Thailand)]\nChannel 8 broadcasts popular events such as HBO World Championship Boxing plus domestic and self-produced programs.\n\n[HBO World Championship Boxing]\nHBO World Championship Boxing is an American sports television series, premiering in January 1973 that has shown a number of significant boxing events since then.\n\n[Ong-Art Singlumpong]\nCurrently he is the executive director of Channel 8.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qdcfb8a383d",
  "kind": "yes/no",
  "text": "Claim: The English title for a rock song written and recorded by an Argentine duo with more than 25 million records sold worldwide is \"Get Out of My Life, Now!\".\n\nPassages:\n\n[Olvídame y Pega la Vuelta]\nPimpinela recorded an English-language version of the song titled \"Get Out of My Life, Now!\"\n\n[Pimpinela]\nThey have sold over 12 million records in Argentina and 25 million worldwide.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q48d1fd8ea8",
  "kind": "yes/no",
  "text": "Tweet: I can't believe today is the last day we can be gay.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q390e167609",
  "kind": "yes/no",
  "text": "Tweet: So nice of my family to decide that I’m hosting a Mother’s Day brunch for everyone at my house. https://t.co/DWZI9ltALK",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qf0c336ac90",
  "kind": "yes/no",
  "text": "Claim: One of the legendary four aces skaters was born in the third largest city in Norway. The others were Sten Stenson, Amund Sjøbrend and Kay Stenshjemmet.\n\nPassages:\n\n[Trondheim]\nIt is the third largest city in the country, with a population (2013) of 169,972 inhabitants within the city borders.\n\n[Jan Egil Storholt]\nJan Egil Storholt (born 13 February 1949) is a former speed skater from Norway. He was born in Trondheim.\n\n[Sten Stensen]\nTogether with Amund Sjøbrend, Kay Stenshjemmet, and Jan Egil Storholt, he was one of the legendary \"four S-es\" (\"four aces\" in Norwegian), contemporary Norwegian top skaters in the 1970s and early 1980s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q4a0a45010a",
  "kind": "yes/no",
  "text": "Claim: The driver who placed first in the race where they drove a FW25 won at the Grand Prix 11 times.\n\nPassages:\n\n[Rubens Barrichello]\nRubens \"Rubinho\" Gonçalves Barrichello (] , ] , born 23 May 1972) is a Brazilian racing driver who competed in Formula One between and , scoring 11 Grands Prix wins and 68 podiums.\n\n[2003 Italian Grand Prix]\nJuan Pablo Montoya finished second in a Williams car, with Rubens Barrichello third in the other Ferrari.\n\n[Williams FW25]\nThree drivers would drive the FW25 in the 2003 season, with Marc Gené replacing regular racer Ralf Schumacher for the Italian Grand Prix after the German suffered a large testing accident testing at Monza's \"Lesmo 1\" corner prior to that race.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6c56d3df33",
  "kind": "yes/no",
  "text": "Tweet: Johnson &amp; Johnson really be tryna kill you from the time you're a baby. If they don't get you in childhood, they'll try to kill you throughout your entire life. Recalls left and right 😬🥴😂🤦🏽‍♀️",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q24a224d432",
  "kind": "yes/no",
  "text": "Claim: A particular opera is by by Joseph-François Duché de Vancy, not Der Barbier von Bagdad. This opera was written by Nicolas-François Guillard.\n\nPassages:\n\n[Der Barbier von Bagdad]\nDer Barbier von Bagdad (\"The Barber of Baghdad\") is a comic opera in two acts by Peter Cornelius to a German libretto by the composer, based on \"The Tale of the Tailor\" and \"The Barber’s Stories of his Six Brothers\" in \"One Thousand and One Nights\".\n\n[Nicolas-François Guillard]\nHis most famous work is \"Iphigénie en Tauride\", his first libretto, set by Gluck after the composer had initially rejected it.\n\n[Iphigénie en Tauride]\nIphigénie en Tauride (\"Iphigenia in Tauris\") is a 1779 opera by Christoph Willibald Gluck in four acts.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q867e64bc28",
  "kind": "yes/no",
  "text": "Text: If the sound of the rain outside wasn’t bad enough I’ve now got my neighbours climbing onto their roof and shouting ‘I love blowjobs’, perfect background noise for me trying to study 👍🏻",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q696cefa36d",
  "kind": "yes/no",
  "text": "Tweet: Does anyone have a PDF of excerpts from ch. 2 of Mill's On Liberty? I want to assign a chunk of the argument for free expression without asking my students to read the whole chapter.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qfc7e3974bc",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "People with curly hair are attractive.",
   "do i like him or is his hair just curly??"
  ]
 },
 {
  "qid": "q3d2bfa1f4b",
  "kind": "yes/no",
  "text": "Tweet: I have nothing clever or fun, other than to say my heart breaks for Jade Carey. And THIS is why one touch warmups for event finals are so important ugh.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q87c4be4d59",
  "kind": "yes/no",
  "text": "Claim: Aaron Waisglass gained recognition as a trap artist for remixing Rihanna's song released on March 26, 2015.\n\nPassages:\n\n[Grandtheft]\nAaron Waisglass, better known by his stage name Grandtheft, is a Canadian DJ and musician based in Toronto. He gained recognition as a trap artist, for remixing songs like “Summer“, “Sweet Nothing“ and “Bitch Better Have My Money” and having songs charted around the world.\n\n[Bitch Better Have My Money]\n\"Bitch Better Have My Money\" is a song recorded by Barbadian singer Rihanna. The song was digitally released on March 26, 2015, through the iTunes Store.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3051af0618",
  "kind": "yes/no",
  "text": "Claim: South Somercotes is a village and civil parish 8 mi north-east from Louth and approximately 2 mi south from the remote coastal village of North Somercotes in the East Lindsey district, and the Marshes area, of Lincolnshire, England.\n\nPassages:\n\n[North Somercotes]\nNorth Somercotes is a coastal village in the East Lindsey district, and the Marshes area, of Lincolnshire, England.\n\n[South Somercotes]\nSouth Somercotes is a village and civil parish 8 mi north-east from Louth and approximately 2 mi south from North Somercotes, Lincolnshire, England.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q003dc8ffb9",
  "kind": "yes/no",
  "text": "Claim: Gone with the Wind (novel) was penned by an Canadian writer. This Canadian writer and the historian that described the Minoan civilization were not both philosophical writers.\n\nPassages:\n\n[Margaret Mitchell]\nMargaret Munnerlyn Mitchell (November 8, 1900 – August 16, 1949) was an American author and journalist.\n\n[Gone with the Wind (novel)]\nGone with the Wind is a novel by American writer Margaret Mitchell, first published in 1936.\n\n[Minoan civilization]\nIt has been described as the earliest of its kind in Europe, with historian Will Durant calling the Minoans \"the first link in the European chain\".\n\n[Will Durant]\nWilliam James \"Will\" Durant ( ; November 5, 1885 – November 7, 1981) was an American writer, historian, and philosopher.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 }
]
