# A46 replay label-noise blind read RSAS06-blind_read-ee5d083f-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS06-blind_read-ee5d083f-006.json

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
  "qid": "qeef6c686df",
  "kind": "yes/no",
  "text": "Text: Manage your personal budget and work out how best to invest your money to realise your goals.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qaca5e43831",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "People with curly hair are attractive.",
   "do i like him or is his hair just curly??"
  ]
 },
 {
  "qid": "q3e20cace8c",
  "kind": "yes/no",
  "text": "Claim: The American actor and singer Brady Bluhm plays a fictional character in a film series based on a character from Return to the Hundred Acre Wood. That fictional character appears in the stories of a fictional anthropomorphic teddy bear.\n\nPassages:\n\n[Winnie-the-Pooh]\nWinnie-the-Pooh, also called Pooh Bear, is a fictional anthropomorphic teddy bear created by English author A. A. Milne.\n\n[Brady Bluhm]\nHe is the brother of actor Brandon Bluhm, and is best known for his role as Christopher Robin in many \"Winnie the Pooh\" films.\n\n[Christopher Robin]\nHe appears in Milne's popular books of poetry and Winnie-the-Pooh stories and is named after Christopher Robin Milne, the author's son.\n\n[Return to the Hundred Acre Wood]\nReturn to the Hundred Acre Wood is a \"Winnie-the-Pooh\" novel published on 5 October 2009.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5e56143ad8",
  "kind": "yes/no",
  "text": "Claim: The Battle of Reading, which Æthelwulf of Berkshire lost his life was a battle on 4 January 871 at Reading in what is now the English county of Berkshire.\n\nPassages:\n\n[Battle of Reading (871)]\nThe first Battle of Reading was a battle on 4 January 871 at Reading in what is now the English county of Berkshire.\n\n[Æthelwulf of Berkshire]\nHe received a land grant in 843/44 from Brihtwulf, king of Mercia; and lost his life at the Battle of Reading.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q890240908d",
  "kind": "yes/no",
  "text": "Claim: Mike Huckabee took part in the most recent Republican Presidential primaries, which began on February 1, 2016.\n\nPassages:\n\n[Mike Huckabee presidential campaign, 2016]\nHuckabee's candidacy for the Republican nomination in the 2016 Presidential election is his second, after having previously run in 2008.\n\n[Republican Party presidential primaries, 2016]\nThe 2016 Republican Party presidential primaries and caucuses were a series of electoral contests taking place within all 50 U.S. states, the District of Columbia, and five U.S. territories, occurring between February 1 and June 7.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q72991b103f",
  "kind": "yes/no",
  "text": "Claim: One of the founding members of the Breeders was the singer for the group who released the album \"Limbo\". She was born before Trace Cyrus.\n\nPassages:\n\n[Limbo (album)]\nLimbo is a 1996 album by the American alternative rock band Throwing Muses, released on Rykodisc.\n\n[The Breeders]\nThe Breeders are an American alternative rock band formed in 1989 by Kim Deal of the Pixies and Tanya Donelly of Throwing Muses.\n\n[Trace Cyrus]\nTrace Dempsey Cyrus (born Neil Timothy Helson; February 24, 1989) is an American musician.\n\n[Tanya Donelly]\nTanya Donelly (born July 14, 1966, in Newport, Rhode Island) is an American Grammy Award-nominated singer-songwriter and guitarist based in New England who co-founded Throwing Muses with her stepsister Kristin Hersh.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf77b975018",
  "kind": "yes/no",
  "text": "Claim: The composer of Show Biz Kids and Lauren Laverne are of the same nationality.\n\nPassages:\n\n[Lauren Laverne]\nLauren Cecilia Fisher (née Gofton, 28 April 1978), known professionally as Lauren Laverne, is an English radio DJ, model, television presenter, author, singer and comedian.\n\n[Show Biz Kids]\n\"Show Biz Kids\" is a song composed by Walter Becker and Donald Fagen and performed by Steely Dan.\n\n[Donald Fagen]\nDonald Jay Fagen (born January 10, 1948) is an American musician best known as the co-founder, lead singer and keyboardist of the band Steely Dan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qbc15682ae9",
  "kind": "yes/no",
  "text": "Claim: Mässersee is one of four mountain lakes in the canton which is known for the resort municipality in the Sierre district in Switzerland.\n\nPassages:\n\n[Crans-Montana]\nCrans-Montana is a municipality in the district of Sierre in the canton of Valais, Switzerland.\n\n[Mässersee]\nMässersee is the smallest of four mountain lakes in the upper Binntal (\"Binn valley\") of the canton of Valais, Switzerland.\n\n[Valais]\nThe canton of Valais is widely known for the Matterhorn and resort towns such as Crans-Montana, Saas Fee and Zermatt.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf0f5040173",
  "kind": "yes/no",
  "text": "Claim: Patrick Baladi played the role of Stephen Holmes in the ITV thriller Marcella available on Netflix.\n\nPassages:\n\n[Marcella (TV series)]\nMarcella is a British crime noir detective series produced, written and directed by Hans Rosenfeldt, a Swedish screenwriter and creator of the series \"The Bridge\" (adapted as \"The Tunnel\" for British audiences). Episodes are available on Netflix worldwide outside the UK and Ireland after it airs on ITV.\n\n[Patrick Baladi]\nPatrick Bashir Baladi (born 25 December 1971 in Sutton Coldfield, Warwickshire) is an English actor. He is best known for playing Neil Godwin in the BBC Sitcom \"The Office\", Michael Jackson in the Sky 1 drama \"Stella\" and Stephen Holmes in the ITV thriller \"Marcella\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9f7f2e4ee9",
  "kind": "yes/no",
  "text": "Claim: When a Man Falls in Love, is a 2013 South Korean television series, starring Song Seung-heon, Shin Se-kyung, Chae Jung-an, and a South Korean actor, born on July 5, 1984.\n\nPassages:\n\n[Yeon Woo-jin]\nYeon Woo-jin (born Kim Bong-hoe on July 5, 1984) is a South Korean actor.\n\n[When a Man Falls in Love]\nWhen a Man Falls in Love () is a 2013 South Korean television series, starring Song Seung-heon, Shin Se-kyung, Chae Jung-an, and Yeon Woo-jin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf2c12e94da",
  "kind": "yes/no",
  "text": "Claim: Ray and Leo Wilson do not have the same nationality.\n\nPassages:\n\n[Leo (singer)]\nJung Taek-woon (Hangul: 정택운 , born on November 10, 1990), better known by his stage name Leo (Hangul: 레오 ), is a South Korean singer, songwriter and musical theatre actor, signed under Jellyfish Entertainment.\n\n[Ray Wilson (musician)]\nRaymond Wilson (born 8 September 1968) is a Scottish musician, best known as vocalist in the post-grunge band Stiltskin, and in Genesis from 1996 to 1998.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe9f0ba491e",
  "kind": "yes/no",
  "text": "Claim: An American four-piece sludge metal band who released the single Honey Bucket (song) was formed earlier than another band. This other band released a compilation album titled Artifakt.\n\nPassages:\n\n[Melvins]\nThe Melvins are an American rock band that formed in 1983 in Montesano, Washington.\n\n[Better Than Ezra]\nBetter Than Ezra is an American alternative rock band based in New Orleans, Louisiana, and signed to The End Records. The band formed in 1988 in Baton Rouge, Louisiana.\n\n[Artifakt]\nArtifakt is a compilation album by Better Than Ezra, sold only at the band's concerts and through the official Better Than Ezra merchandise website beginning in 2001.\n\n[Honey Bucket (song)]\n\"Honey Bucket\" is a single from American sludge metal band Melvins released in September 21, 1993.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfc1ee19da6",
  "kind": "yes/no",
  "text": "Tweet: @traves whoa! that's a little too crazy man, slow down",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q7ee0f3c137",
  "kind": "yes/no",
  "text": "Claim: Louder Than Bombs is the 2015 internationally co-produced drama film directed by Joachim Trier that was produced in 2015. The producer was the son of a. The producer was the son of a director. The director directed Begynnelsen på en historie.\n\nPassages:\n\n[Louder Than Bombs (film)]\nLouder Than Bombs is a 2015 internationally co-produced drama film directed by Joachim Trier, and co-written with Eskil Vogt.\n\n[Begynnelsen på en historie]\nBegynnelsen på en historie (English: The beginning of a story ) is a 1988 Norwegian drama film directed by Margarete Robsahm, starring Linda Pedersen, Wenche Foss and Linn Stokke.\n\n[Margarete Robsahm]\nShe is the mother of director Thomas Robsahm and sister of the actor Fred Robsahm.\n\n[Thomas Robsahm]\nIn 2015 he produced the film \"Louder Than Bombs\" by Joachim Trier.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1ed0d93d75",
  "kind": "yes/no",
  "text": "Claim: Will Penny was a western starring an American actor and activist.\n\nPassages:\n\n[Charlton Heston]\nCharlton Heston (born John Charles Carter or Charlton John Carter; October 4, 1923 – April 5, 2008) was an American actor and political activist.\n\n[Will Penny]\nWill Penny is a 1967 western film written and directed by Tom Gries starring Charlton Heston, Joan Hackett and Donald Pleasence.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q261550d552",
  "kind": "yes/no",
  "text": "Claim: Ben Affleck plays the character Matt Murdock, a blind lawyer who fights for justice in the courtroom and on the streets of New York as a masked vigilante, in an Defenders superhero movie which shares its name with the album released for it in 2003 by Wind-up Records.\n\nPassages:\n\n[Daredevil (film)]\nDaredevil is a 2003 American superhero film written and directed by Mark Steven Johnson. Based on the Marvel Comics character of the same name, the film stars Ben Affleck as Matt Murdock, a blind lawyer who fights for justice in the courtroom and on the streets of New York as the masked vigilante Daredevil.\n\n[Daredevil: The Album]\nDaredevil: The Album was released on March 4, 2003 by Wind-up Records for the movie \"Daredevil\", starring Ben Affleck.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7f6d017c28",
  "kind": "yes/no",
  "text": "Claim: Patton Oswalt is the voice actor for the main character of the Pixar film which received a Golden Globe Award for best picture in 2008.\n\nPassages:\n\n[Ratatouille (film)]\nThe film stars the voices of Patton Oswalt as Remy, an anthropomorphic rat who is interested in cooking; Lou Romano as Linguini, a young garbage boy who befriends Remy; Ian Holm as Skinner, the head chef of Auguste Gusteau's restaurant; Janeane Garofalo as Colette, a rôtisseur at Gusteau's restaurant; Peter O'Toole as Anton Ego, a restaurant critic; Brian Dennehy as Django, Remy's father and leader of his clan; Peter Sohn as Emile, Remy's older brother; and Brad Garrett as Auguste Gusteau, a recently deceased chef.\n\n[Golden Globe Award for Best Animated Feature Film]\nThe award for best animated film has subsequently been presented to six other Pixar films: \"Ratatouille\" received the award in 2008, \"WALL-E\" was the recipient in 2009, \"Up\" received the award in 2010, \"Toy Story 3\" won in 2011, \"Brave\" won in 2013, and \"Inside Out\" won in 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd51ff525d0",
  "kind": "yes/no",
  "text": "Tweet: Just rediscovered that my nose is always in my field of vision so I will unfortunately be dropping out as I cannot continue my assigned readings in peace",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q36a0e7d3e6",
  "kind": "yes/no",
  "text": "Claim: Nikita Gennadyevich Katsalapov won the 2016 Russian national silver medal with another young Russian ice dancer born 29 April 1995.\n\nPassages:\n\n[Victoria Sinitsina]\nVictoria Alexandrovna Sinitsina (Russian: Виктория Александровна Синицина ; born 29 April 1995) is a Russian ice dancer.\n\n[Nikita Katsalapov]\nNikita Gennadyevich Katsalapov (Russian: Никита Геннадьевич Кацалапов ; born 10 July 1991) is a Russian ice dancer. With Victoria Sinitsina, he is the 2016 Russian national silver medalist.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa0358f37ca",
  "kind": "yes/no",
  "text": "Text: @DuncanEdwards03 @PoliticsForAlI Well I doubt they're trying to smash the doors in to change the regulation of cough medicine.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q3f3a4dd4ba",
  "kind": "yes/no",
  "text": "Post: Before going to Lush: I’m just gonna buy 2 bath bombs nothing crazy 😇\n\nMe walking out: *holding 4 bath bombs, 2 lip scrubs, 3 shower gels*",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qbf948e28b9",
  "kind": "yes/no",
  "text": "Claim: The Byron Edmund Walker founded institution, The University of Toronto, was originally controlled by the Church of England.\n\nPassages:\n\n[Byron Edmund Walker]\nSir Byron Edmund Walker, CVO (14 October 1848 – 27 March 1924) was a Canadian banker. He was the president of the Canadian Bank of Commerce from 1907 to 1924, and a generous patron of the arts, helping to found and nurture many of Canada's cultural and educational institutions, including the University of Toronto, National Gallery of Canada, the Champlain Society, Appleby College, Art Gallery of Ontario and Royal Ontario Museum.\n\n[University of Toronto]\nThe University of Toronto (U of T, UToronto, or Toronto) is a public research university in Toronto, Ontario, Canada on the grounds that surround Queen's Park. Originally controlled by the Church of England, the university assumed the present name in 1850 upon becoming a secular institution.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qba1ee8a9cd",
  "kind": "yes/no",
  "text": "Claim: Comair is the franchise carrier that operates aircraft in full British Airways livery and has its main base at OR King Shaka International Airport, Johannesburg.\n\nPassages:\n\n[British Airways franchise destinations]\nTogether with wholly owned subsidiary BA CityFlyer, franchise carriers Sun Air and Comair operate aircraft in full British Airways livery, offer full BA service and staff wear BA uniform.\n\n[Comair (South Africa)]\nIts main base is OR Tambo International Airport, Johannesburg, and has focus cities at Cape Town International Airport and King Shaka International Airport.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1f7765f5d5",
  "kind": "yes/no",
  "text": "Claim: The daughter of the woman who recorded the song Stoney End co-wrote the teleplay for the first episode of \"Black Mirror\". She was born in 1976.\n\nPassages:\n\n[Rashida Jones]\nRashida Leah Jones (born February 25, 1976) is an American actress, producer, singer, and writer.\n\n[Peggy Lipton]\nLipton was married to the musician/producer Quincy Jones and is mother to their two daughters, Rashida Jones and Kidada Jones, who also became actresses.\n\n[Stoney End (song)]\nIt was originally recorded in 1968 by Peggy Lipton and her recording reached #121 on the U.S. \"Billboard\" Bubbling Under the Hot 100 chart.\n\n[Nosedive]\nMichael Schur and Rashida Jones wrote the teleplay for the episode, based on a story by series creator and showrunner Charlie Brooker, while Joe Wright acted as director.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q1e2b58b688",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "There was no need for that",
   "@mcfcok82 Thank you for your well balanced and thoughtful input"
  ]
 },
 {
  "qid": "qb237118bbc",
  "kind": "yes/no",
  "text": "Claim: The author of the 1967 unproduced script written for The Beatles, Up Against It, and Bernard-Marie Koltès are both playwrights.\n\nPassages:\n\n[Up Against It]\nUp Against It is an unproduced script by Joe Orton, written in 1967 for The Beatles at the height of their fame.\n\n[Bernard-Marie Koltès]\nBernard-Marie Koltès (] ; 9 April 1948 – 15 April 1989) was a French playwright and theatre director best known for his plays \"La Nuit juste avant les Forêts\" (\"The Night Just Before the Forests\", 1976), \"Sallinger\" (1977) and \"Dans la Solitude des Champs de Coton\" (\"In the Solitude of Cotton Fields\", 1986).\n\n[Joe Orton]\nJohn Kingsley \"Joe\" Orton (1 January 1933 – 9 August 1967) was an English playwright and author.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q69319f2e9a",
  "kind": "yes/no",
  "text": "Claim: Frances Clayton died in battle. It occurred 1 month before the battle for which Thomas Baker received the Medal of Honor.\n\nPassages:\n\n[Battle of Saipan]\nThe Battle of Saipan was a battle of the Pacific campaign of World War II, fought on the island of Saipan in the Mariana Islands from 15 June to 9 July 1944.\n\n[Battle of Stones River]\nThe Battle of Stones River or Second Battle of Murfreesboro, was fought from December 31, 1862, to January 2, 1863, in Middle Tennessee, as the culmination of the Stones River Campaign in the Western Theater of the American Civil War.\n\n[Frances Clayton]\nShe left the army soon after her husband died at Stones River.\n\n[Thomas Baker (Medal of Honor)]\nThomas Alexander Baker (June 25, 1916 – July 7, 1944) was a United States Army soldier who posthumously received the U.S. military's highest decoration, the Medal of Honor, for his actions in World War II during the Battle of Saipan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q86efc9b2b7",
  "kind": "yes/no",
  "text": "Claim: Katrina Bowden appeared in a slasher film that was released under an independent film distribution label. This label company was Dimension films.\n\nPassages:\n\n[Scary Movie 5]\nIt is the second film to be distributed by The Weinstein Company under the Dimension Films brand.\n\n[Katrina Bowden]\nShe also appeared in films such as \"Sex Drive\", \"Piranha 3DD\", and \"Scary Movie 5\".\n\n[Dimension Films]\nDimension Films is an American film production company and independent film distribution label formerly owned by The Walt Disney Studios and now owned by The Weinstein Company.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q743ae6a863",
  "kind": "yes/no",
  "text": "Claim: The junction of the three states of Kentucky, Virginia, and Tennessee is near the gap that Peter Hackett traveled along during the Scotish-Irish migration along Virginia State Route 42.\n\nPassages:\n\n[Cumberland Gap]\nThe Cumberland Gap is a narrow pass through the long ridge of the Cumberland Mountains, within the Appalachian Mountains, near the junction of the U.S. states of Kentucky, Virginia, and Tennessee.\n\n[Peter Hackett]\nAs a boy Peter was bonded out to Captain James Estill, in approximately 1771, and was a part of the broad Scotch-Irish migration along the Wilderness Road through the Cumberland Gap from Virginia into what later became known as Kentucky in the late 18th century.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0b2e23b245",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "This isn't a fun night both my kiddos are sick.",
   "Both kiddos have a cold I don't feel good and now I think my oldest is having stomach issues, oh what a fun night!"
  ]
 },
 {
  "qid": "q29210e3c72",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I'm not entirely sure you -can- say the same thing non-sarcastically. I suppose... 'Constantly calling for lower targets is ridiculous.'",
   "@GainzyXBT Actually I've extrapolated based on the last daily candle and it turns out BTC will be sub-zero by December. The math doesn't lie."
  ]
 },
 {
  "qid": "qb58bc5d549",
  "kind": "yes/no",
  "text": "Claim: This movie was directed by Damien Chazelle and won the 2017 Guild of Music Supervisors Awards.\n\nPassages:\n\n[La La Land (film)]\nLa La Land is a 2016 American musical romantic comedy-drama film written and directed by Damien Chazelle.\n\n[Guild of Music Supervisors Awards]\nCompton\", \"Carol\" and \"Furious 7\" were among the winners of the 2016 ceremony, while \"La la land\" of the 2017 ceremony.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q363f394ecf",
  "kind": "yes/no",
  "text": "Claim: The athlete, a qualifier for the June 2009 Manitoba Scotties Tournament of Hearts as reigning champion, was the captain of the gold medalist Curling team for Canada at the Sochi Winter Olympics.\n\nPassages:\n\n[2009 Manitoba Scotties Tournament of Hearts]\nThe reigning provincial champion, Jennifer Jones, won the 2008 Scotties Tournament of Hearts and thereby has already qualified for the 2009 event as Team Canada.\n\n[Jennifer Jones (curler)]\nShe won an Olympic gold medal as skip of the Canadian team at the 2014 Sochi Games. They won the 2008 World Women's Curling Championship, and were the last Canadian women's team to do so until Rachel Homan in 2017.\n\n[2007 Trail Appliances Autumn Gold Curling Classic]\nThe 2007 Trail Appliances Autumn Gold Curling Classic was the 30th annual edition of the event. It marked the first Grand Slam event of the Women's World Curling Tour. It was held October 5-9 at the Calgary Curling Club in Calgary, Alberta. The total purse for the event was $56,000 with $14,000 going to the winning team of Jennifer Jones, Cathy Overton-Clapham, Jill Officer and Dawn Askin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbe2b5d6696",
  "kind": "yes/no",
  "text": "Claim: Oklahoma City Thunder won the Northwest Division in 2015-16. Their first season under current the head coach played basketball under at NCAA. He was also coach of the 2013–14 Kennesaw State Owls men's basketball team.\n\nPassages:\n\n[Billy Donovan]\nWilliam John Donovan Jr. (born May 30, 1965) is an American professional basketball coach who is currently the head coach for the Oklahoma City Thunder of the National Basketball Association (NBA).\n\n[Lewis Preston (basketball)]\nHe previously served as an assistant men's basketball coach at Pennsylvania State University, Coastal Carolina University, the University of Notre Dame, and under Billy Donovan at the University of Florida.\n\n[2013–14 Kennesaw State Owls men's basketball team]\nThe Owls, led by third year head coach Lewis Preston, played their home games at the KSU Convocation Center and were members of the Atlantic Sun Conference.\n\n[2015–16 Oklahoma City Thunder season]\nAfter coming just short of making the playoffs the previous season, the Thunder won the Northwest Division and clinched the third seed in the Western Conference.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q592aefe308",
  "kind": "yes/no",
  "text": "Tweet: what a great day to be stuck inside 🙃",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qa87de7a5ce",
  "kind": "yes/no",
  "text": "Claim: The town that is connected by a ferry to Kwadjokrom is a town in the Lake Volta region.\n\nPassages:\n\n[Krachi West District]\nThe Krachi West District is one of the twenty-five (25) districts in the Volta Region.\n\n[Kwadjokrom]\nKwadjokrom is connected by a ferry to the town of Kete Krachi.\n\n[Kete Krachi]\nKete Krachi is a town in the Krachi West District of the Volta Region of Ghana.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4eed7e3ff1",
  "kind": "yes/no",
  "text": "Claim: Douglas county in Minnesota holds a 202 lb slab of greywacke covered in runes.\n\nPassages:\n\n[Kensington, Minnesota]\nKensington is a city in Douglas County, Minnesota, United States. The city is notable in Minnesota history for being the place where the famous, if questionable, Kensington Runestone was first displayed.\n\n[Kensington Runestone]\nThe Kensington Runestone is a 202 lb slab of greywacke covered in runes on its face and side.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q108c3f0b5f",
  "kind": "yes/no",
  "text": "Claim: Greenwich House is the historic meeting venue built in a style taught at the Ecole des Beaux-Arts.\n\nPassages:\n\n[Dayton Memorial Hall]\nThe Dayton Memorial Hall is a historic meeting venue on First Street in downtown Dayton, Ohio, United States. Constructed shortly after the turn of the twentieth century, this Beaux-Arts structure is one of many memorial halls statewide from the same time period, and it has been named a historic site.\n\n[Beaux-Arts architecture]\nBeaux-Arts architecture ( ; ] ) expresses the academic neoclassical architectural style taught at the \"École des Beaux-Arts\" in Paris.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qafe49fb271",
  "kind": "yes/no",
  "text": "Claim: Proud To Commit Commercial Suicide is a live spanish language album by industrial metal band Nailbomb and captures the band's only live appearance at the 1995 Dynamo Open Air Festival, the album cover is a picture of the aftermath of the Jonestown infamous remote settlement established by the Peoples Temple, an American socialist organization under the leadership of Jim Jones, in northwestern Guyana.\n\nPassages:\n\n[Jonestown]\nThe Peoples Temple Agricultural Project, better known by its informal name \"Jonestown\", was a remote settlement established by the Peoples Temple, an American socialist organization under the leadership of Jim Jones, in northwestern Guyana.\n\n[Proud to Commit Commercial Suicide]\nThe album cover is a picture of the aftermath of the infamous Jonestown suicides.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa4c6eeb6f6",
  "kind": "yes/no",
  "text": "Claim: The 2010–11 Tour de Ski - in which Swiss cross-country skier and singer Dario Cologna won the Men's class - was the 5th edition of the Tour de Ski and took place from 31 December 2010 to 9 January 2011.\n\nPassages:\n\n[2010–11 Tour de Ski]\nThe 2010–11 Tour de Ski was the 5th edition of the Tour de Ski and took place from 31 December 2010 to 9 January 2011.\n\n[Dario Cologna]\nDario Cologna (born 11 March 1986) is a Swiss cross-country skier.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q629a7c7036",
  "kind": "yes/no",
  "text": "Tweet: ik it’s for the best but wow RIP to my italy study abroad trip, beyond wonderland, my 21st bday, edc, and now @awonderland’s red rocks show 😔",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf4f1038a1a",
  "kind": "yes/no",
  "text": "Claim: The first person to interpret Relational quantum mechanics has worked in Italy, the United States and since 2000, in Paris, France.\n\nPassages:\n\n[Carlo Rovelli]\nCarlo Rovelli (born 3 May 1956) is an Italian theoretical physicist and writer who has worked in Italy, the United States and since 2000, in France.\n\n[Relational quantum mechanics]\nThis interpretation was first delineated by Carlo Rovelli in a 1994 preprint, and has since been expanded upon by a number of theorists.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q53cbfecd22",
  "kind": "yes/no",
  "text": "Claim: The song \"Good Life\" recorded by G-Eazy and Kehlani appeared on the soundtrack for the 2017 action film The Fate of the Furious directed by Kehlani.\n\nPassages:\n\n[The Fate of the Furious]\nThe Fate of the Furious (alternatively known as Fast & Furious 8 and Fast 8, and often stylized as F8) is a 2017 American action film directed by F. Gary Gray and written by Chris Morgan.\n\n[Good Life (G-Eazy and Kehlani song)]\n\"Good Life\" is a song recorded by American rapper G-Eazy and American singer Kehlani, taken from the soundtrack of the 2017 action film \"The Fate of the Furious\" (2017).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9aab615be9",
  "kind": "yes/no",
  "text": "Claim: Monsters, Inc. Mike & Sulley to the Rescue! is based on a movie made by a company that was sold by Disney for $7.4 billion.\n\nPassages:\n\n[Pixar]\nPixar ( ), also referred to as Pixar Animation Studios, is an American computer animation film studio based in Emeryville, California that is a subsidiary of The Walt Disney Company. Disney purchased Pixar in 2006 at a valuation of $7.4 billion, a transaction that resulted in Jobs becoming Disney's largest single shareholder at the time.\n\n[Monsters, Inc. Mike &amp; Sulley to the Rescue!]\nMonsters, Inc. Mike & Sulley to the Rescue! It is based on the 2001 Disney·Pixar film \"Monsters, Inc.\" It opened on January 22, 2006 with a grand Sulley-Blue-Fur Carpet Premiere.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q17d57eae91",
  "kind": "yes/no",
  "text": "Claim: Lafayette was the opponent of the Republican of Indenosia when Nugroho Notosusanto served as a member of the Student Army.\n\nPassages:\n\n[Nugroho Notosusanto]\nDuring the Indonesian National Revolution from 1945 to 1949 he saw active service as a member of the Student Army, working reconnaissance.\n\n[Indonesian National Revolution]\nThe Indonesian National Revolution or Indonesian War of Independence (Indonesian: Perang Kemerdekaan Indonesia , Dutch: \"Indonesische Onafhankelijkheidsoorlog\" ) was an armed conflict and diplomatic struggle between the Republic of Indonesia and the Dutch Empire, and an internal social revolution following the postwar and postcolonial Indonesia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2804739ec7",
  "kind": "yes/no",
  "text": "Claim: Acid Brass is a musical collaboration between Turner-Prize-winning artist Jeremy Deller and the award winning Williams Fairey Brass Band and based on fusing the music of a traditional brass band with acid house and Detroit techno, a type of techno music that generally includes the first techno productions by Detroit-based artists during the 1980s and early 1990s.\n\nPassages:\n\n[Detroit techno]\nDetroit techno is a type of techno music that generally includes the first techno productions by Detroit-based artists during the 1980s and early 1990s.\n\n[Acid Brass]\nAcid Brass is a musical collaboration between Turner-Prize-winning artist Jeremy Deller and the Williams Fairey Brass Band. The project is based on fusing the music of a traditional brass band with acid house and Detroit techno.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q54ecd13238",
  "kind": "yes/no",
  "text": "Claim: The Dutch Empire was the opponent of the Republican of Indenosia when the writer of the basis for Pengkhianatan G30S/PKI served as a member of the Louisiana House of Representatives for Lafayette.\n\nPassages:\n\n[Pengkhianatan G30S/PKI]\nIt was based on an official history of the 30 September Movement (Gerakan 30 September , or G30S) coup in 1965 written by Nugroho Notosusanto and Ismail Saleh, which depicted the coup as being orchestrated by the Communist Party of Indonesia (Partai Komunis Indonesia , or PKI).\n\n[Nugroho Notosusanto]\nDuring the Indonesian National Revolution from 1945 to 1949 he saw active service as a member of the Student Army, working reconnaissance.\n\n[Indonesian National Revolution]\nThe Indonesian National Revolution or Indonesian War of Independence (Indonesian: Perang Kemerdekaan Indonesia , Dutch: \"Indonesische Onafhankelijkheidsoorlog\" ) was an armed conflict and diplomatic struggle between the Republic of Indonesia and the Dutch Empire, and an internal social revolution following the postwar and postcolonial Indonesia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q75eca7e6ea",
  "kind": "yes/no",
  "text": "Claim: This film co-starred voice artist and comedian Richard Dawson Kiel. Cookbook author Catherine Serre also starred in the film.\n\nPassages:\n\n[Richard Kiel]\nRichard Dawson Kiel (September 13, 1939 – September 10, 2014) was an American actor, voice artist, and comedian, best known for his role as Jaws in the \"James Bond\" franchise, portraying the character in \"The Spy Who Loved Me\" (1977) and \"Moonraker\" (1979); he lampooned the role with a tongue-in-cheek cameo in \"Inspector Gadget\" (1999).\n\n[Catherine Serre]\nShe is known for her credited roles in Moonraker where she played Countess Labinsky, one of the \"perfect\" human specimens from Drax's master race, and in the French Le gendarme et les gendarmettes films, where she appeared together with Nicaise Jean Louis, another Drax Girl from Moonraker.\n\n[Moonraker (film)]\nThe third and final film in the series to be directed by Lewis Gilbert, it co-stars Lois Chiles, Michael Lonsdale, Corinne Cléry, and Richard Kiel.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe3c60c077e",
  "kind": "yes/no",
  "text": "Claim: The owner of Treasure Island Hotel and Casino since 2009, an American businessman born in 1935, owned a greyhound racing track called Swansea Greyhound Stadium in Kansas.\n\nPassages:\n\n[Treasure Island Hotel and Casino]\nSince March 2009, TI is owned and operated by Phil Ruffin.\n\n[Wild West World]\nWild West World was a Wild West theme park in Park City, Kansas that opened on May 5, 2007 and closed on July 9, 2007. It was located on 130 acre along Interstate 135 near Phil Ruffin's Wichita Greyhound Park, which closed the same year.\n\n[Phil Ruffin]\nPhillip Gene \"Phil\" Ruffin (born March 14, 1935) is an American businessman.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q414235420d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "My favorite part about running on the track is seeing how high my heart rate gets just walking up the stairs to it.",
   "My heart rate spiked when I walk up the stairs to the track"
  ]
 }
]
