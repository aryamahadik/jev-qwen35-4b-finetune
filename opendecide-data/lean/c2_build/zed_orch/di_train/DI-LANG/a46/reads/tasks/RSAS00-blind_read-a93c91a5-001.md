# A46 replay label-noise blind read RSAS00-blind_read-a93c91a5-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS00-blind_read-a93c91a5-001.json

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
  "qid": "q75778421ae",
  "kind": "yes/no",
  "text": "Claim: Pocari Sweat and another beverage are both drinks. This other beverage was endorsed by Hugh Manning.\n\nPassages:\n\n[Robinsons (drink)]\nRobinsons is an English fruit drink brand owned by Britvic.\n\n[Hugh Manning]\nHe also starred in the tv series \"Mrs Thursday\", alongside Kathleen Harrison in 1966, playing a suave and imperturbable Butler, which also carried over into popular tv commercials where his character endorsed the qualities of Robinsons barley water.\n\n[Pocari Sweat]\nPocari Sweat (ポカリスエット , Pokari Suetto ) is a Japanese sports drink, manufactured by Otsuka Pharmaceutical It was launched in 1980, and is now also available in East Asia, Southeast Asia, and the Middle East.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc21b45bbd9",
  "kind": "yes/no",
  "text": "Tweet: Why was I not told Matthew Stafford and Cooper Kupp eat breakfast together before I drafted Robert Woods over him?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q7289b05477",
  "kind": "yes/no",
  "text": "Text: okay but like the say so song ain’t that bad. I’m unironically jam to it lmao",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q5a16312576",
  "kind": "yes/no",
  "text": "Post: i just saw the loveliest cat on the way home :)",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q06afb160b3",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "My tinnitus is so annoying",
   "Tinnitus is my favourite thing ever I love it. So loud so atmospheric https://t.co/mNJw5GvPzy"
  ]
 },
 {
  "qid": "q786b288002",
  "kind": "yes/no",
  "text": "Claim: The daughter of the Spanish woman who recorded the song Stoney End co-wrote the teleplay for the first episode of \"Black Mirror\". She was born in 1976.\n\nPassages:\n\n[Peggy Lipton]\nLipton was married to the musician/producer Quincy Jones and is mother to their two daughters, Rashida Jones and Kidada Jones, who also became actresses.\n\n[Rashida Jones]\nRashida Leah Jones (born February 25, 1976) is an American actress, producer, singer, and writer.\n\n[Nosedive]\nMichael Schur and Rashida Jones wrote the teleplay for the episode, based on a story by series creator and showrunner Charlie Brooker, while Joe Wright acted as director.\n\n[Stoney End (song)]\nIt was originally recorded in 1968 by Peggy Lipton and her recording reached #121 on the U.S. \"Billboard\" Bubbling Under the Hot 100 chart.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q03bab1e2f3",
  "kind": "yes/no",
  "text": "Claim: Christopher Whitelaw Pine appeared in the films that inspired Good Luck! and \"Into the Woods\".\n\nPassages:\n\n[Chris Pine]\nChristopher Whitelaw Pine (born August 26, 1980) is an American actor. He is known for playing James T. Kirk in the \"Star Trek\" reboot film series (2009–2016), Will Colson in \"Unstoppable\" (2010), Cinderella's Prince in \"Into the Woods\" (2014), Toby Howard in \"Hell or High Water\" (2016) and Steve Trevor in \"Wonder Woman\" (2017).\n\n[Just My Luck (2006 film)]\nThe film stars Lindsay Lohan and Chris Pine as the main characters.\n\n[Good Luck!]\nIt is inspired by Hollywood film, \"Just My Luck\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0d4e84ae46",
  "kind": "yes/no",
  "text": "Claim: FBI employee Jordan Mintz whictleblowing was publicized on October 2001.\n\nPassages:\n\n[Enron scandal]\nThe Enron scandal, publicized in October 2001, eventually led to the bankruptcy of the Enron Corporation, an American energy company based in Houston, Texas, and the \"de facto\" dissolution of Arthur Andersen, which was one of the five largest audit and accountancy partnerships in the world.\n\n[Jordan Mintz]\nEnron whistleblower Jordan Mintz was the former Managing Director for Corporate Tax at Enron Corporation.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5d9938e8c1",
  "kind": "yes/no",
  "text": "Claim: An American independent motion picture company produced a 2015 mystery thriller film based on a novel by Tom Rob. The first project it produced was a movie in which Tom Degnan had an appearance.\n\nPassages:\n\n[Worldview Entertainment]\nWorldview Entertainment is an American independent motion picture company that finances and produces theatrical quality feature films for worldwide distribution. Worldview has produced films including \"Child 44\", \"Birdman\", \"Blood Ties\", \"The Green Inferno\", and \"Killer Joe\".\n\n[Child 44 (film)]\nChild 44 is a 2015 mystery thriller film directed by Daniel Espinosa, written by Richard Price, and based on Tom Rob Smith's 2008 novel of the same name.\n\n[Handsome Harry]\nThe first project produced by Worldview Entertainment, it stars Jamey Sheridan, Steve Buscemi and Aidan Quinn.\n\n[Tom Degnan]\nAdditional appearances include \"Handsome Harry\", alongside Steve Buscemi, and \"Little Miss Perfect\", alongside Lilla Crawford.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q351e061e06",
  "kind": "yes/no",
  "text": "Text: My favorite thing is that literally ONLY my @Walmart says I have to have a prescription for syringes that I've been getting OTC for years. This is the kind of shit diabetics are facing.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qe495028ee4",
  "kind": "yes/no",
  "text": "Claim: A star of Hello! Stranger is the brother of the mixed martial artist of Canadian nationality.\n\nPassages:\n\n[Julien Kang]\nHe is the younger brother of mixed martial artist Denis Kang.\n\n[Hello! Stranger]\nStranger () is a 2014 South Korean television program starring Kim Kwang-kyu, Julien Kang, Kangnam and Mina Fujii.\n\n[Denis Kang]\nDenis Kang (Hangul: 강대수 , born September 17, 1977) is a Canadian professional mixed martial artist who most recently competed in the Middleweight division.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8dd6e4ea73",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "It's snowing, if it wasn't lockdown I'd have to work from home but as I am already working from home it makes no difference to my day.",
   "Yay - snow day, I can work from home - oh wait...."
  ]
 },
 {
  "qid": "qebc978f87f",
  "kind": "yes/no",
  "text": "Claim: Jacqueline MacInnes Wood played Sara Lance in the first episode of Arrow. The actor who played Moira Queen on that episode appeared in the courtroom drama film, Ghosts of Mississippi, directed by Rob Reiner.\n\nPassages:\n\n[Pilot (Arrow)]\nThe episode introduces Oliver Queen (Stephen Amell), a billionaire playboy, his mother Moira Queen (Susanna Thompson), sister Thea (Willa Holland), new bodyguard John Diggle (David Ramsey), best friend Tommy Merlyn (Colin Donnell), ex-girlfriend Laurel Lance (Katie Cassidy), and her father Detective Quentin Lance (Paul Blackthorne).\n\n[Susanna Thompson]\nSusanna Thompson (born January 27, 1958) is an American actress. She is known for her roles in films \"Little Giants\" (1994), \"Ghosts of Mississippi\" (1996), \"Random Hearts\" (1999) and \"Dragonfly\" (2002), and as Karen Sammler on ABC drama series \"Once and Again\" (1999–2002).\n\n[Ghosts of Mississippi]\nGhosts of Mississippi is a 1996 American biographical courtroom drama film directed by Rob Reiner and starring Alec Baldwin, Whoopi Goldberg, and James Woods.\n\n[Sara Lance]\nOriginally portrayed by Jacqueline MacInnes Wood in \"Arrow\"'s pilot, she has been portrayed by Caity Lotz since the second season.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q91601e0574",
  "kind": "yes/no",
  "text": "Claim: Pay the Ghost starred Sarah Wayne Callies who had a role in Prison Break.\n\nPassages:\n\n[Pay the Ghost]\nThe film stars Nicolas Cage, Sarah Wayne Callies, Veronica Ferres, Lauren Beatty, Jack Fulton, and Elizabeth Jeanne le Roux.\n\n[Sarah Wayne Callies]\nSarah Wayne Callies (born June 1, 1977) is an American actress. She is best known for her portrayals of Sara Tancredi in Fox's \"Prison Break\", Lori Grimes in AMC's \"The Walking Dead\" and Katie Bowman in USA Network's \"Colony\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5e56dda334",
  "kind": "yes/no",
  "text": "Post: our waitress at dinner tonight complimented my muscles so i guess you could say i’ve made it",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q7ec348c446",
  "kind": "yes/no",
  "text": "Claim: The drug store, which merged with Leaps and Bounds in 1995, was founded in Missouri and Valentino's wasn't.\n\nPassages:\n\n[Leaps and Bounds (playplace)]\nIt was merged with competitor Discovery Zone in 1995.\n\n[Valentino's]\nValentino's is a regional Italian restaurant chain based in Lincoln, Nebraska.\n\n[Discovery Zone]\nDiscovery Zone (DZ) was a chain of entertainment facilities featuring games and elaborate indoor mazes designed for young children, including roller slides, climbing play structures and ball pits. The first location was opened in Kansas City, Missouri in October 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8f00e4e43f",
  "kind": "yes/no",
  "text": "Text: #bbcqt It sure would be nice if Ms May decided to answer a question, rather than dance readily around it.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q6523c6242a",
  "kind": "yes/no",
  "text": "Claim: Radio On: A Listener's Diary is the first book by an author that voiced the character Violet in the film \"The Incredibles\".\n\nPassages:\n\n[Radio On: A Listener's Diary]\nRadio On: A Listener's Diary (1997) is the first book by Sarah Vowell.\n\n[Sarah Vowell]\nShe was also the voice of Violet in the animated film \"The Incredibles\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7341ee6f84",
  "kind": "yes/no",
  "text": "Claim: Tiko's Spanish football club hold home games at Estadio de López Cortázar.\n\nPassages:\n\n[CD Basconia]\nFounded in 1913 it currently plays in Tercera División – Group 4, holding home games at \"Estadio de López Cortázar\", with an 8,500-seat capacity.\n\n[Tiko (footballer)]\nRoberto Martínez Rípodas (born 15 September 1976), known as Tiko, is a Spanish retired footballer who played as a central or a defensive midfielder, and the current assistant manager of CD Basconia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q05d9694d8d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "absolutely love waking up to the fire alarm at 7 am 😍",
   "I hate waking up to the fire alarm at 7 am."
  ]
 },
 {
  "qid": "qed56bb6ea3",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Headaches that last all day nonstop🥰😍",
   "I hate headaches and I have one."
  ]
 },
 {
  "qid": "q1b5e36d226",
  "kind": "yes/no",
  "text": "Claim: Pelle Almqvist is younger than the saxophonist who played synthesizers on the track \"Got a Hold on Me\".\n\nPassages:\n\n[Pelle Almqvist]\nPer \"Pelle\" Almqvist (born 29 May 1978), also known as Howlin' Pelle Almqvist, is a Swedish singer and songwriter.\n\n[Got a Hold on Me]\nSynthesizers on the track were played by Steve Winwood, while the guitars were played by Todd Sharp (the song's co-writer) and McVie's Fleetwood Mac bandmate Lindsey Buckingham.\n\n[Steve Winwood]\nStephen Lawrence \"Steve\" Winwood (born 12 May 1948) is an English musician whose genres include rock, blue-eyed soul, rhythm and blues, blues rock, pop rock, and jazz.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd3df6097db",
  "kind": "yes/no",
  "text": "Claim: A footballer played his entire football career for an sports league team that plays their home games at FirstEnergy Stadium. This player's cousin is offensive lineman Jason Pinkston . Dick Daugherty also played in this sports league for 4 years.\n\nPassages:\n\n[Cleveland Browns]\nThe Browns play their home games at FirstEnergy Stadium, which opened in 1999, with administrative offices and training facilities in Berea, Ohio.\n\n[Dick Daugherty]\nRichard Lee Daugherty (March 31, 1929 – March 10, 2009) was an offensive lineman and linebacker who played six seasons in the NFL for the Los Angeles Rams.\n\n[Jason Pinkston]\nJason R. Pinkston (born September 5, 1987) is a former American football offensive guard, who played his entire career for the Cleveland Browns of the National Football League (NFL).\n\n[Todd Pinkston]\nHe also is the cousin of former offensive lineman Jason Pinkston.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q56c9a30c7b",
  "kind": "yes/no",
  "text": "Claim: Bambi, is based on a book by the American author Felix Salten, The Country Bears is not.\n\nPassages:\n\n[Bambi]\nBambi is a 1942 American animated film directed by David Hand (supervising a team of sequence directors), produced by Walt Disney and based on the book \"Bambi, a Life in the Woods\" by Austrian author Felix Salten.\n\n[The Country Bears]\nThe Country Bears is a 2002 American family musical comedy film, directed by Peter Hastings, produced by Walt Disney Pictures, and based on the Disney theme park attraction \"Country Bear Jamboree\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qaed40edc49",
  "kind": "yes/no",
  "text": "Claim: Yellow Loveless is the name of an album that features cover versions of songs off of a 1991 record by an Anglo-Irish rock band formed in Dublin in 1983 who later disbanded in 1994.\n\nPassages:\n\n[My Bloody Valentine (band)]\nMy Bloody Valentine are an Anglo-Irish rock band formed in Dublin in 1983.\n\n[Yellow Loveless]\nYellow Loveless is a tribute album featuring cover versions of the 11 songs from My Bloody Valentine's 1991 record \"Loveless\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qcfdf991bd8",
  "kind": "yes/no",
  "text": "Text: Update: almost 10 hours since the first modern vaccine.\n\nArm stiffness and pain has definitely worsened. I can’t hold my arm over my head and it hurts to lift my arm up to eat or do anything. Can’t move myself on the bed or do things with my left arm. 😬",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qe9be2d10b3",
  "kind": "yes/no",
  "text": "Claim: The politician that was defeated by republican congressman Bill Arthur was a Labor candidate. The division that he was selected for was created in 1922.\n\nPassages:\n\n[Bill Arthur]\nHowever, in 1966 he defeated Labor member Len Reynolds and was elected for the Liberal Party.\n\n[Division of Barton]\nThe Division of Barton is an Australian electoral division in the state of New South Wales. The division was created in 1922 and is named for Sir Edmund Barton, the first Prime Minister of Australia.\n\n[Len Reynolds (politician)]\nIn 1958, he was selected as the Labor candidate for the seat of Barton, which party leader H. V. Evatt was leaving as it was perceived to be too marginal.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q61f8db2653",
  "kind": "yes/no",
  "text": "Claim: Playwrights Eugène Ionesco and Paul Scott lived during the same time period.\n\nPassages:\n\n[Eugène Ionesco]\nEugène Ionesco (born Eugen Ionescu, ] ; 26 November 1909 – 28 March 1994) was a Romanian-French playwright who wrote mostly in French, and one of the foremost figures of the French Avant-garde theatre.\n\n[Paul Scott (novelist)]\nPaul Mark Scott (25 March 19201 March 1978) was an English novelist, playwright, and poet, best known for his monumental tetralogy \"The Raj Quartet.\"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q57d573214c",
  "kind": "yes/no",
  "text": "Claim: The organization that has sanctioned the Nascar Pirelli World Challenge since 2017 has sanctioned races in both California and Indianapolis.\n\nPassages:\n\n[1991 USAC FF2000 Championship]\nThe series was sanctioned by the United States Auto Club and ran races in California and Arizona.\n\n[Pirelli World Challenge]\nIt is managed by WC Vision since 2008, and is sanctioned by the United States Auto Club since 2017.\n\n[United States Auto Club]\nFrom 1956 to 1979, USAC sanctioned the United States National Championship, and from 1956 to 1997 the organization sanctioned the Indianapolis 500.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9e44ce4bb1",
  "kind": "yes/no",
  "text": "Claim: Costa Rican Pietro Ferrero introduced his famous hazelnut cocoa product in the year 1965.\n\nPassages:\n\n[Nutella]\nNutella ( ; ] ) is a brand of sweetened hazelnut cocoa spread manufactured by the Italian company Ferrero that was first introduced in 1965, although its first iteration dates to 1963.\n\n[Ferrero SpA]\nFerrero SpA (] ) is an Italian manufacturer of branded chocolate and confectionery products and it is the third biggest chocolate producer and confectionery company in the world. It was founded in 1946 in Alba, Piedmont, Italy, by Pietro Ferrero, a confectioner and small-time pastry maker who laid the groundwork for Nutella and famously added hazelnut to save money on chocolate.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe004d45020",
  "kind": "yes/no",
  "text": "Text: Hands up who remembers when EVERY blogger and their dog was a brand ambassador for Coconut Lane 😂",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qdeacf82cf3",
  "kind": "yes/no",
  "text": "Tweet: Brother's off on a night out and I've gone to bed cos I feel exhausted and sick.... excellent 👍🏻",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q433cb4cef3",
  "kind": "yes/no",
  "text": "Claim: Philadelphus contains more species than Sarracenia.\n\nPassages:\n\n[Sarracenia]\nSarracenia ( or ) is a genus comprising 8 to 11 species of North American pitcher plants, commonly called trumpet pitchers.\n\n[Philadelphus]\nPhiladelphus ( ) (mock-orange) is a genus of about 60 species of shrubs from 3-20 ft (1-6 m) tall, native to North America, Central America, Asia and (locally) in southeast Europe.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4763301088",
  "kind": "yes/no",
  "text": "Claim: Manaslu stands higher than the landform that is 60 km due south of Chakragil.\n\nPassages:\n\n[Chakragil]\nIt is located about 100 km southwest of Kashgar, about 60 km due north of Muztagh Ata, and 37 km northwest of Kongur Tagh.\n\n[Muztagh Ata]\nMuztagh Ata, or Muztagata (Uyghur: مۇز تاغ ئاتا, Музтаң Ата, literally \"ice-mountain-father\"; ), is the second highest (7509 metres) of the mountains which form the northern edge of the Tibetan Plateau (not the second highest of the mountains of the Tibetan Plateau).\n\n[Manaslu]\nManaslu (Nepali: मनास्लु, also known as Kutang) is the eighth highest mountain in the world at 8163 m above sea level.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc296a5cc2a",
  "kind": "yes/no",
  "text": "Claim: Franz Liszt, a prolific 19th-century Hungarian composer, virtuoso pianist, conductor, music teacher, arranger, organist, philanthropist, author, nationalist and a Franciscan tertiary based his play on a novel work by Lord Byron.\n\nPassages:\n\n[Sardanapale]\nSardanapale (French for \"Sardanapalus\"), S.687, is an unfinished opera by Franz Liszt based loosely on the 1821 verse play \"Sardanapalus\" by Lord Byron.\n\n[Franz Liszt]\nFranz Liszt (] ; Hungarian: \"Liszt Ferencz\" , in modern usage \"Liszt Ferenc\", ] ; October 22, 1811July 31, 1886) was a prolific 19th-century Hungarian composer, virtuoso pianist, conductor, music teacher, arranger, organist, philanthropist, author, nationalist and a Franciscan tertiary.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5f86f4fba4",
  "kind": "yes/no",
  "text": "Claim: Route 611 (Afghanistan) is approximately 100 kilometers curves and passes through the town that is found in the valley of the primary watershed for Sistan Basin.\n\nPassages:\n\n[Helmand River]\nThe Helmand River (also spelled \"Helmend, Helmund, Hirmand\"; Pashto/Persian: هیرمند, هلمند \"Hīrmand, Helmand \", Greek: \"Ἐτύμανδρος \" (\"Etýmandros\"), Latin: \"Erymandrus \") is the longest river in Afghanistan and the primary watershed for the endorheic Sistan Basin.\n\n[Sangin]\nIt is located on in the valley of the Helmand River at 888 m altitude, 95 km to the north-east of Lashkargah.\n\n[Route 611 (Afghanistan)]\nThe road is approximately 100 kilometers and passes through the town of Sangin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q103f698b6d",
  "kind": "yes/no",
  "text": "Claim: A drummer was a member of \"The Nerves\" an Americana power pop trio. Americana musicians Blackie Lawless and this drummer were both born in 1956.\n\nPassages:\n\n[Blackie Lawless]\nBlackie Lawless (born Steven Edward Duren; September 4, 1956) is an American songwriter and musician best known as the lead singer and rhythm guitarist (formerly bassist) for the heavy metal band W.A.S.P.\n\n[Paul Collins (musician)]\nPaul Vincent Collins (born 1956, New York City) is an American writer, author, music producer, and multi-instrumentalist.\n\n[The Nerves]\nThe Nerves were a mid-1970s American power pop trio, based in Los Angeles, featuring guitarist Jack Lee, bassist Peter Case, and drummer Paul Collins.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbcb013b8b5",
  "kind": "yes/no",
  "text": "Claim: The day Southpark is most congested is the fourth Thursday of November.\n\nPassages:\n\n[Black Friday (shopping)]\nBlack Friday ( ) is the day following Thanksgiving Day in the United States (the fourth Thursday of November).\n\n[SouthPark Mall (Charlotte, North Carolina)]\nSouthPark is the most congested shopping area in the United States during Black Friday weekend.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6d13cb7ae9",
  "kind": "yes/no",
  "text": "Claim: Dr. Brewster M. Higley wrote the lyrics to the theme song that was used by the Western film series Range Busters.\n\nPassages:\n\n[Home on the Range]\n\"Home on the Range\" is a classic western folk song sometimes called the \"unofficial anthem\" of the American West. The lyrics were originally written by Dr. Brewster M. Higley of Smith County, Kansas, in a poem entitled \"My Western Home\" in 1872.\n\n[Range Busters]\nThe Range Busters was a film series of 24 Westerns of the adventures of a trio of cowboys, many filmed at the Corriganville Movie Ranch, produced by George W. Weeks and distributed by Monogram Pictures. The series used \"Home on the Range\" as its theme song with each film featuring the heroes waving goodbye and promising to return in another adventure.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q13979d8ef0",
  "kind": "yes/no",
  "text": "Claim: Norman Blake is older than the frontman of The Vines, that produced their album Wicked Nature.\n\nPassages:\n\n[Wicked Nature]\nThe release marks a few milestones for The Vines, with frontman Craig Nicholls taking on the role of producer for the first time, as well as introducing a completely new rhythm section with drummer Lachlan West and bassist Tim John.\n\n[Craig Nicholls]\nCraig Robert Nicholls (born 31 August 1977) is an Australian musician, best known as the lead singer, songwriter, and guitarist of the Australian alternative rock band The Vines, of which he is the only mainstay member.\n\n[Norman Blake (Scottish musician)]\nNorman Blake (born 20 October 1965, Bellshill, North Lanarkshire, Scotland) is a singer, instrumentalist and songwriter in the Glasgow based band Teenage Fanclub.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb28f378bb2",
  "kind": "yes/no",
  "text": "Claim: Keith Scholey co-directed \"African Cats\" and another documentary with the executive producer of \"Frozen Planet\" for Disneynature. That documentary and Aliens of the Deep were not filmed in the same locations.\n\nPassages:\n\n[Aliens of the Deep]\nIt was produced by Walden Media and Walt Disney Pictures.\n\n[Frozen Planet]\nThe production team, which includes executive producer Alastair Fothergill and series producer Vanessa Berlowitz, were previously responsible for the award-winning series \"The Blue Planet\" (2001) and \"Planet Earth\" (2006), and \"Frozen Planet\" is billed as a sequel of sorts.\n\n[Keith Scholey]\nHe co-directed \"African Cats\" and \"Bears\" with Alastair Fothergill for Disneynature.\n\n[Bears (film)]\nBears is a 2014 nature documentary film about a family of brown bears living in the coastal mountain ranges of Alaska.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qad60a5d3f6",
  "kind": "yes/no",
  "text": "Tweet: Angela Merkel: doctorate in Quantum Chemistry\n\nLeo Varadkar: worked for years as a GP\n\nBoris Johnson: once accidentally called ping-pong “wiff-waff”",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qa06b6521c0",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Top 3 ranked video games of all time: 1. Minecraft 2. Roblox Paintball 3. Every single Just Dance",
   "I would put actual top ranked games, not stupid ones everyone makes fun of."
  ]
 },
 {
  "qid": "q48424e0dca",
  "kind": "yes/no",
  "text": "Claim: Jeff Ragsdale and Millard Webb are not both authors.\n\nPassages:\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qaff9bb02c2",
  "kind": "yes/no",
  "text": "Text: Perk of doing a newborn hearing screening on an SLP’s baby: not having to discuss speech and language milestones",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe05d81c305",
  "kind": "yes/no",
  "text": "Claim: One of the legendary four aces skaters was born in the third largest city in Norway. The others were Jan Egil Storholt, Amund Sjøbrend and Kay Stenshjemmet.\n\nPassages:\n\n[Sten Stensen]\nTogether with Amund Sjøbrend, Kay Stenshjemmet, and Jan Egil Storholt, he was one of the legendary \"four S-es\" (\"four aces\" in Norwegian), contemporary Norwegian top skaters in the 1970s and early 1980s.\n\n[Trondheim]\nIt is the third largest city in the country, with a population (2013) of 169,972 inhabitants within the city borders.\n\n[Jan Egil Storholt]\nJan Egil Storholt (born 13 February 1949) is a former speed skater from Norway. He was born in Trondheim.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q92e84541ac",
  "kind": "yes/no",
  "text": "Claim: Don Holmes played for the football club that is based in Bassendean, the east side of Perth.\n\nPassages:\n\n[Swan Districts Football Club]\nThe club is based at Bassendean Oval, in Bassendean, an eastern suburb of Perth, Western Australia.\n\n[Don Holmes]\nDonald Shane \"Don\" Holmes (born 5 January 1959) is a former Australian rules footballer who was played in the West Australian Football League (WAFL) for Swan Districts and in the Victorian Football League (VFL) for West Coast .",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4a0e4e0c62",
  "kind": "yes/no",
  "text": "Claim: The biographer who was admitted to mental asylum at High Beach upon which the book The Quickening Maze is base, teaches English Literature at the University of Oxford.\n\nPassages:\n\n[The Quickening Maze]\nThe book is based on the historical backdrop of a mental asylum run by Matthew Allen at High Beach in late 1830s and 1840s which had English poet John Clare admitted therein.\n\n[John Clare]\nHis biographer Jonathan Bate states that Clare was \"the greatest labouring-class poet that England has ever produced.\n\n[Jonathan Bate]\nHe is Professor of English Literature at the University of Oxford, Provost of Worcester College, Oxford, and Honorary Fellow of Creativity at Warwick Business School.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa0f701a4ca",
  "kind": "yes/no",
  "text": "Claim: The company produced the Evergreen GPU's for its graphics card Radeon HD 5000 Series. It's headquartered farther west than the company that owns Software Spectrum.\n\nPassages:\n\n[Level 3 Communications]\nLevel 3 Communications is an American multinational telecommunications and Internet service provider company headquartered in Broomfield, Colorado.\n\n[Radeon HD 5000 Series]\nThe Evergreen series is a family of GPUs developed by Advanced Micro Devices for its Radeon line under the ATI brand name.\n\n[Advanced Micro Devices]\nAdvanced Micro Devices, Inc. (AMD) is an American multinational semiconductor company based in Sunnyvale, California, United States, that develops computer processors and related technologies for business and consumer markets.\n\n[Software Spectrum]\nSoftware Spectrum is a company acquired by Level 3 Communications in 2002.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9818be916e",
  "kind": "yes/no",
  "text": "Claim: The art critic that met Joseph Drapell died after the death of Agatha Christie.\n\nPassages:\n\n[Agatha Christie]\nDame Agatha Mary Clarissa Christie, Lady Mallowan, DBE (\"née\" Miller; 15 September 1890 – 12 January 1976) was an English crime novelist, short story writer and playwright.\n\n[Joseph Drapell]\nAt the Cranbrook Academy he met visiting Canadian artist Jack Bush and the American art critic Clement Greenberg, who influenced his work.\n\n[Clement Greenberg]\nClement Greenberg ( ), occasionally writing under the pseudonym K. Hardesh (January 16, 1909 – May 7, 1994), was an American essayist known mainly as an influential visual art critic closely associated with American Modern art of the mid-20th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 }
]
