# A46 replay label-noise blind read RSAS07-blind_read-95379c1f-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS07-blind_read-95379c1f-004.json

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
  "qid": "qb8582fcb29",
  "kind": "yes/no",
  "text": "Text: excited to start my new hobby of standing in the lgbtq section of the feminist bookstore and look hot and mysterious until I get noticed",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q1774f984b8",
  "kind": "yes/no",
  "text": "Claim: Bauhinia is a genus of more species this genus. This genus contains the species Cestrum diurnum.\n\nPassages:\n\n[Bauhinia]\nBauhinia is a genus of more than 500 species of flowering plants in the subfamily Cercidoideae of the large flowering plant family Fabaceae, with a pantropical distribution.\n\n[Cestrum]\nCestrum is a genus of - depending on authority - 150-250 species of flowering plants in the family Solanaceae.\n\n[Cestrum diurnum]\nCestrum diurnum (Din Ka Raja) is a species of \"Cestrum\", native to the West Indies.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7771ae81c2",
  "kind": "yes/no",
  "text": "Claim: The actor who played Joanna in \"The Calling (2009 film)\" is best known for her role in a television series whose second season premiered on March, 19 2017.\n\nPassages:\n\n[Into the Badlands (TV series)]\nInto the Badlands is an American television series that premiered on AMC November 15, 2015. AMC renewed the show for a 10-episode second season, which premiered on March 19, 2017.\n\n[The Calling (2009 film)]\nDunn's third feature film, it tells the story of Joanna, played by Emily Beecham, who after graduating from university, goes against her family and friends when she decides to join the closed order of Benedictine nuns. For her debut leading performance in the film, Beecham was awarded a New Talent Trailblazer Award presented by Sean Connery during the film's debut, where it was also selected as 'Best of the Fest' at the 2009 Edinburgh International Film Festival.\n\n[Emily Beecham]\nEmily Beecham is an English-American actress. She is best known for her role in the AMC television series \"Into the Badlands\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf3a10a2c62",
  "kind": "yes/no",
  "text": "Claim: EKU is the three letter abbreviation that the college where Former NBL player Chrissy Roberts is head coach is commonly referred to by.\n\nPassages:\n\n[Eastern Kentucky University]\nEastern Kentucky University, commonly referred to as Eastern or EKU, is a regional comprehensive institution located in Richmond, Kentucky.\n\n[Chrissy Roberts]\nChrissie Roberts (born December 25, 1975) is an American college basketball coach and the current women's head coach at Eastern Kentucky University (EKU) in Richmond, Kentucky.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qde697fbb1a",
  "kind": "yes/no",
  "text": "Claim: The Tree of Man was written by an Austrian Nobel Prize-winner. He and Katherine Anne Porter are both writers.\n\nPassages:\n\n[The Tree of Man]\nThe Tree of Man is the fourth published novel by the Australian novelist and 1973 Nobel Prize-winner, Patrick White.\n\n[Patrick White]\nPatrick Victor Martindale White (28 May 191230 September 1990) was an Australian writer who is widely regarded as one of the most important English-language novelists of the 20th century.\n\n[Katherine Anne Porter]\nKatherine Anne Porter (May 15, 1890 – September 18, 1980) was an American journalist, essayist, short story writer, novelist, and political activist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8f1138780e",
  "kind": "yes/no",
  "text": "Claim: Mario Mazzacurati won the 1936 South African Grand Prix with the Bugatti, a type of two door car that was founded in 1909 in the then German city of Molsheim, Alsace.\n\nPassages:\n\n[Mario Mazzacurati]\nMario Mazzacurati (21 October 1903 – 17 April 1985) was an Italian engineer and auto racer driver active in South Africa, winner of the 1936 South African Grand Prix in Bugatti cars with pseudonym Mario Massacuratti.\n\n[Bugatti]\nAutomobiles Ettore Bugatti was a French car manufacturer of high-performance automobiles, founded in 1909 in the then German city of Molsheim, Alsace by Italian-born Ettore Bugatti.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa126d51e04",
  "kind": "yes/no",
  "text": "Claim: The winner of the 2014 French Open – Mixed Doubles and another female athlete are both tennis players. This other athlete won the singles title at the 1979 Romika Cup.\n\nPassages:\n\n[Manuel Orantes]\nManuel Orantes Corral (] ; born 6 February 1949) is a former tennis player who was active in the 1970s and 1980s.\n\n[Anna-Lena Grönefeld]\nAnna-Lena Grönefeld (born 4 June 1985) is a German tennis player.\n\n[1979 Romika Cup]\nFirst-seeded Manuel Orantes won the singles title.\n\n[2014 French Open – Mixed Doubles]\nHradecká played alongside Mariusz Fyrstenberg but lost in the second round to the eventual champions Anna-Lena Grönefeld and Jean-Julien Rojer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qcfa8fd5f29",
  "kind": "yes/no",
  "text": "Claim: Frederick Alexander is a British physicist and also a British government's chief scientific adviser.\n\nPassages:\n\n[Frederick Lindemann, 1st Viscount Cherwell]\nFrederick Alexander Lindemann, 1st Viscount Cherwell, (5 April 18863 July 1957), pronounced , was a British physicist and an influential scientific adviser to the British government from the early 1940s to the early 1950s, particularly to Winston Churchill.\n\n[Dehousing]\nOn 30 March 1942 Professor Frederick Lindemann, Baron Cherwell, the British government's chief scientific adviser, sent to the British Prime Minister Winston Churchill a memorandum which after it had become accepted by the Cabinet became known as the dehousing paper.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbf7a39f8fe",
  "kind": "yes/no",
  "text": "Text: Jeopardy had an “Internet Slang” category and I finally know the answers to some of these.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q3907b6118d",
  "kind": "yes/no",
  "text": "Claim: Both Trace Cyrus and Jizzy Pearl are vocalists.\n\nPassages:\n\n[Trace Cyrus]\nIn 2010, he began providing vocals and guitar in the pop rock band Ashland HIGH.\n\n[Jizzy Pearl]\nJizzy Pearl (born James Wilkinson) is an American vocalist that was born on March 17, 1958, in Chicago, Illinois.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9e9289d331",
  "kind": "yes/no",
  "text": "Claim: A combat flight simulator video game published by Konami and released in winter of 2012 features missions including the attack on Pearl Harbour by the Empire of Japan on December 7, 1941.\n\nPassages:\n\n[Birds of Steel]\nBirds of Steel (蒼の英雄 Birds of Steel , Ao no Eiyuu: Birds of Steel ) is a combat flight simulator video game created by Gaijin Entertainment and published by Konami. It was released on March 13, 2012 for PlayStation 3 and Xbox 360. The game includes more than one hundred non-fictional planes, twenty historical missions, and hundreds of procedural missions over sixteen different locations, including Pearl Harbor and Wake Island.\n\n[Pearl Harbor]\nThe attack on Pearl Harbor by the Empire of Japan on December 7, 1941, was the immediate cause of the United States' entry into World War II.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8f32a89960",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "my neighbors taunting me outside my office window by chilling in their hot tub every remotely warm day whilst I sit here on back-to-back zooms all day every day. the audacity is astonishing.",
   "Very jealous of my neighbors sitting in their hot tub today whilst I am on back to back zoom meetings."
  ]
 },
 {
  "qid": "q374066c160",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I could have said \"I am an idiot\" or something along those lines instead.",
   "Throwback to when I answered the phone at work with “thank you for calling Courtney! My name is principal” wow I love myself"
  ]
 },
 {
  "qid": "q0c252411a7",
  "kind": "yes/no",
  "text": "Claim: The job title of this American engineer and former astronaut aboard Apollo 11, who inspired the musical Moon Landing was Lunar Module Pilot.\n\nPassages:\n\n[Moon Landing (music drama)]\nMoon Landing is a musical with book, lyrics and music by Stephen Edwards. The story, from an original idea and synopsis by Justin Fleming, is based on the American Space Race and the Apollo 11 spaceflight which on July 20, 1969 landed the first humans on the Moon and is seen through the eyes of Buzz Aldrin, the second man to walk on the moon.\n\n[Buzz Aldrin]\nBuzz Aldrin (born Edwin Eugene Aldrin Jr.; January 20, 1930) is an American engineer and former astronaut. As the Lunar Module Pilot on Apollo 11, he was one of the first two humans to land on the Moon, and the second person to walk on it.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q65ca02e2b5",
  "kind": "yes/no",
  "text": "Claim: There is a small medieval castle made of mud in Scotland.\n\nPassages:\n\n[Castlebay]\nCastlebay (Scottish Gaelic: \"Bàgh a' Chaisteil\" ) is the main village and a community council area on the island of Barra in the Outer Hebrides, Scotland.\n\n[Kisimul Castle]\nKisimul Castle (Scottish Gaelic: \"Caisteal Chiosmuil\" ) and also known as Kiessimul Castle, is a small medieval castle located on a small island off Castlebay, Barra, in the Outer Hebrides, Scotland.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q626e24b61d",
  "kind": "yes/no",
  "text": "Claim: Gabby West won a competition on the reality show \"Scream Queens\". Her prize was a role in a movie starring Costas Mandylor. The movie had a video game released one week prior to its premier.\n\nPassages:\n\n[Saw 3D]\nSaw 3D (also known as Saw: The Final Chapter, or simply Saw VII) is a 2010 American 3D horror film directed by Kevin Greutert, written by Patrick Melton and Marcus Dunstan, and starring Tobin Bell, Costas Mandylor, Betsy Russell, Sean Patrick Flanery and Cary Elwes.\n\n[Saw II: Flesh &amp; Blood]\nIt was released in 2010 to coincide with the release of the seventh film, \"Saw 3D\", a week later.\n\n[Gabby West]\nShe won a role in \"Saw 3D\" in a competition on the reality show \"Scream Queens\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2b153bec00",
  "kind": "yes/no",
  "text": "Claim: Young the Giant and Archive are both rock groups. The other group made an archive album called Noise.\n\nPassages:\n\n[Noise (Archive album)]\nNoise is the fourth album of the London-based trip hop band Archive.\n\n[Young the Giant]\nYoung the Giant is an American rock band that formed in Irvine, California, in 2004.\n\n[Archive (band)]\nArchive are a musical group based in London, England, whose music spans electronic, trip hop, avant-garde, post-rock and progressive rock.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc7982e42b9",
  "kind": "yes/no",
  "text": "Claim: The creator of \"Too Romantic\" was born before Aaron Katz.\n\nPassages:\n\n[Aaron Katz (filmmaker)]\nAaron Katz (born October 29, 1981) is an award-winning independent American filmmaker from Portland, Oregon.\n\n[Too Romantic]\nToo Romantic is a 1992 dramatic short film that Todd Field created while a fellow at the AFI Conservatory.\n\n[Todd Field]\nWilliam Todd Field (born February 24, 1964) is an American actor and three-time Academy Award nominated filmmaker.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q68872e81f4",
  "kind": "yes/no",
  "text": "Claim: Ernest Whitington wrote \"Out among the People\" in a newspaper first published in London in 1781.\n\nPassages:\n\n[Ernest Whitington]\nErnest Whitington (c. 1873 – 13 April 1934), known to his friends as \"Ern\", was a journalist in South Australia, who as \"Rufus\" wrote the popular \"Out among the People\" column in the Register then The Advertiser when those two newspapers were amalgamated.\n\n[South Australian Register]\nIt was first published in London in June 1836 and folded almost a century later in February 1931.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7627633c40",
  "kind": "yes/no",
  "text": "Claim: Nassu County, which borders Queens on its southern boundary, has a population of 778.\n\nPassages:\n\n[Hewlett-Woodmere School District]\nThe Hewlett-Woodmere Public School District, Union Free School District 14, is located in the southwest section of Nassau County, New York and borders the New York City borough of Queens.\n\n[Woodsburgh, New York]\nThe population was 778 at the 2010 census.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2f70e1373c",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Feels like 10 degrees!! Wow catch me in South Parks soaking up the rays 😎 https://t.co/EpgwTLgICW",
   "It's going to be pretty cold in South Parks today!"
  ]
 },
 {
  "qid": "q051185b202",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I hate you so much @Eagles",
   "Being an Eagles fan is disappointing"
  ]
 },
 {
  "qid": "q44f6a19c6e",
  "kind": "yes/no",
  "text": "Text: I couldn’t have imagined how much fun I would have with people I’ve met through streaming. I’m so thankful to live in this timeline even if it is relatively garbage.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qa253c30495",
  "kind": "yes/no",
  "text": "Text: I'm just living off salads and yogurt and loving it tbh",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5127de8820",
  "kind": "yes/no",
  "text": "Claim: The show, in which the host of this game show also hosted, usually aired on Monday at 7 pm. Rosie Goldsmith hosted it, as well as Crossing Continents.\n\nPassages:\n\n[A Word in Your Ear]\nIt was hosted by Gordon Burns.\n\n[Rosie Goldsmith]\nShe was the host of the shows Crossing Continents, and A World in Your Ear.\n\n[The Krypton Factor]\nThe show originally ran from 7 September 1977 to 20 November 1995, and was hosted by Gordon Burns and usually broadcast on the ITV network on Mondays at 7pm.\n\n[Gordon Burns]\nHe was the host of \"The Krypton Factor\" for its original 18-year run (1977–1995) and was the chief anchorman for the BBC regional news programme \"North West Tonight\" from January 1997 to October 2011.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8e3d7eb8a7",
  "kind": "yes/no",
  "text": "Claim: Louis Leterrier is a French film director whose films include the first two \"Transporter\" films. The Transporter is an English-language French action thriller film directed by Corey Yuen and Louis Leterrier, released in 2002.\n\nPassages:\n\n[The Transporter]\nThe Transporter (French: Le Transporteur) is a 2002 English-language French action thriller film directed by Corey Yuen and Louis Leterrier (who is credited as artistic director on the project), and written by Luc Besson, who was inspired by BMW Films' \"The Hire\" series.\n\n[Louis Leterrier]\nLouis Leterrier (born June 17, 1973) is a French film director whose films include the first two \"Transporter\" films, \"Unleashed\" (2005), \"The Incredible Hulk\" (2008), \"Clash of the Titans\" (2010) and \"Now You See Me\" (2013).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qff7526cfe1",
  "kind": "yes/no",
  "text": "Claim: Charlie Walker, a member of the country-americana stage concert in Nashville was born in Copeville, Texas.\n\nPassages:\n\n[Charlie Walker (musician)]\nCharlie Walker (November 2, 1926 – September 12, 2008)<ref name='cmt.com/1594705'> </ref> was an American country musician born in Copeville, Texas. He held membership in the Grand Ole Opry from 1967, and was inducted into the Country Radio DJ Hall of Fame in 1981.\n\n[Grand Ole Opry]\nThe Grand Ole Opry is a weekly country-music stage concert in Nashville, Tennessee, which was founded on November 28, 1925, by George D. Hay as a one-hour radio \"barn dance\" on WSM.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q25cece6d92",
  "kind": "yes/no",
  "text": "Post: @faith_hi @PalmerReport Ahh yes, quick peek at your page and you obviously know everything. Thank you for the enlightenment.😂",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qebadf2275b",
  "kind": "yes/no",
  "text": "Claim: Jane Mayer is writing a book about the billionaires who funded Citizens United (organization) and who control the on of the largest privately owned companies in the United States.\n\nPassages:\n\n[Dark Money (book)]\nDark Money: The Hidden History of the Billionaires Behind the Rise of the Radical Right (2016) is a non-fiction book written by the American investigative journalist Jane Mayer, about a network of extremely wealthy conservative libertarians, foremost among them Charles and David Koch, who have together funded an array of organizations that work in tandem to influence academic institutions, think tanks, the courts, statehouses, Congress, and the American presidency for their own benefit.\n\n[Koch family]\nThe Koch family ( ) is an American family engaged in business, most noted for their political activities and control of Koch Industries, the second-largest privately owned company in the United States (with 2013 revenues of $115 billion).\n\n[Citizens United (organization)]\nCitizens United is a conservative 501(c)(4) non-profit organization in the United States started in 1988 with major funding from the billionaire Koch family.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q212ccc047a",
  "kind": "yes/no",
  "text": "Claim: Czech Boris Franz Becker won more awards than the partnered of Patrick Galbraith in the 1997 Stockholm Open – Doubles. Where they both lost in the final game.\n\nPassages:\n\n[1997 Stockholm Open – Doubles]\nGalbraith partnered Ellis Ferreira, losing in the final.\n\n[Boris Becker]\nBoris Franz Becker (] ; born 22 November 1967) is a German former world No. 1 professional tennis player. He also won five year-end championships, 13 Masters Series titles, and an Olympic gold medal in doubles.\n\n[Ellis Ferreira]\nHe won 2 Grand Slam doubles titles, the Men's title at the 2000 Australian Open with Rick Leach and the mixed doubles at the Australian Open with Corina Morariu in 2001.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q61c03d142c",
  "kind": "yes/no",
  "text": "Claim: One of the Belgian composer of Bee (song) wrote songs that were featured in commercials for a brand of Artsana, that's been working for over 50 years, and is present in more than 120 countries.\n\nPassages:\n\n[Chicco]\nChicco (] ) is a brand of Artsana, that's been working for over 50 years in the field of children's products, and is now present in more than 120 countries worldwide.\n\n[Bee (song)]\n'\"Bee\" is a song recorded by German singers Lena Meyer-Landrut and Jennifer Braun, composed by American-Israeli songwriter Rosi Golan, American singer-songwriter Mayaeni Strauss and Norwegian songwriter Per Kristian Ottestad.\n\n[Rosi Golan]\nHer songs have been featured in feature films such as \"Dear John\" and \"Tiger Eyes\", various TV shows such as \"Vampire Diaries\", \"Grey's Anatomy\", \"Private Practice\", \"Brothers & Sisters\", \"One Tree Hill\", \"Ghost Whisperer\", and numerous commercials for companies such as Chicco, Pantene, J. C. Penney and Walmart.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4dea17399a",
  "kind": "yes/no",
  "text": "Claim: President Bill Clinton signed into law the act made to lower barriers to adoption.\n\nPassages:\n\n[Adoption 2002]\nBased on the Adoption and Safe Families Act of 1997, the aim of the program was to lower barriers to adoption and double the rate of adoption of children in foster care by 2002 from a 1996 figure of 27,000 to a 2002 figure of 54,000.\n\n[Adoption and Safe Families Act]\nThe Adoption and Safe Families Act (ASFA, Public Law 105-89) was signed into law by President Bill Clinton on November 19, 1997, after having been approved by the United States Congress earlier in the month.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q12fd8b3df2",
  "kind": "yes/no",
  "text": "Claim: George Hamilton IV performed the song \"Abilene\" in a 1963 movie. The actress who co-starred with an actor in this movie was Canadian. The actor also starred in \"The Crawling Hand\".\n\nPassages:\n\n[The Crawling Hand]\nThe Crawling Hand is a 1963 science fiction horror film directed by Herbert L. Strock, and starring Rod Lauren, Peter Breck, Allison Hayes, and Alan Hale, Jr. It was later featured on the television shows \"Mystery Science Theater 3000\" (\"MST3K\") and \"The Canned Film Festival\".\n\n[Ruta Lee]\nRuta Lee (born May 30, 1935) is a Canadian actress and dancer who appeared as one of the brides in the musical \"Seven Brides for Seven Brothers\".\n\n[Abilene (song)]\nThe song reached number one on the U.S. country music chart for four weeks, and peaked at number 15 on the pop music charts.\n\n[Hootenanny Hoot]\nIt stars Peter Breck and Ruta Lee.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0596258f73",
  "kind": "yes/no",
  "text": "Claim: Chad Smith and another artist are American. This other singer released the song \"Stone Cold Gentleman\".\n\nPassages:\n\n[Stone Cold Gentleman]\n\"Stone Cold Gentleman\" is a song performed by American contemporary R&B singer Ralph Tresvant, issued as the second single from his eponymous debut album.\n\n[Chad Smith]\nChadwick Gaylord Smith (born October 25, 1961) is an American musician and the current drummer of the Red Hot Chili Peppers, which he joined in 1988.\n\n[Ralph Tresvant]\nRalph Edward Tresvant Sr. (born May 16, 1968), also known as Rizz and Rizzo, is an American contemporary R&B singer best known as the lead singer of R&B/pop group New Edition.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd27f24773b",
  "kind": "yes/no",
  "text": "Tweet: Johnson &amp; Johnson really be tryna kill you from the time you're a baby. If they don't get you in childhood, they'll try to kill you throughout your entire life. Recalls left and right 😬🥴😂🤦🏽‍♀️",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q05a4b75460",
  "kind": "yes/no",
  "text": "Post: @itsmrevandaniel I can't believe people still don't genuinely hate every player from that Astros team.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qcd78ebc085",
  "kind": "yes/no",
  "text": "Claim: The younger brother of Harvey Jewell served as the national coordinator for the American Republican Party.\n\nPassages:\n\n[Harvey Jewell]\nHis younger brother, Marshall Jewell (1825-1883) would later be elected Governor of Connecticut and would serve as President Grant's United States Postmaster General.\n\n[Marshall Jewell]\nMarshall Jewell (October 20, 1825February 10, 1883) was a manufacturer, pioneer telegrapher, telephone entrepreneur, world traveler, and political figure who served as 44th and 46th Governor of Connecticut, the U.S. Minister to Russia, the 25th United States Postmaster General, and Republican Party National Chairman.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe8ebbca089",
  "kind": "yes/no",
  "text": "Claim: Gordon Warnecke starred in a 1985 film. The director of this film and Jan Švankmajer are not from the same country.\n\nPassages:\n\n[Stephen Frears]\nStephen Arthur Frears (born 20 June 1941) is an English film director.\n\n[Jan Švankmajer]\nJan Švankmajer (] ; born 4 September 1934) is a Czech filmmaker and artist whose work spans several media.\n\n[Gordon Warnecke]\nHe may be best known for his role as Omar in the 1985 film \"My Beautiful Laundrette\", co-starring as the lover of Johnny (Daniel Day-Lewis).\n\n[My Beautiful Laundrette]\nMy Beautiful Laundrette is a 1985 British comedy-drama film directed by Stephen Frears from a screenplay by Hanif Kureishi.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q136148eefd",
  "kind": "yes/no",
  "text": "Claim: The job title of the wife of the writer of the novel \"Aaina\" was Bollywood playback singer.\n\nPassages:\n\n[Aaina (1993 film)]\nAaina (English: \"Mirror\" ), is a 1993 film directed by Deepak Sareen and produced by Yash Chopra and independently produced by his wife Pamela Chopra.\n\n[Pamela Chopra]\nPamela Chopra (born 1938) is a Bollywood playback singer. She is the widow of veteran film director Yash Chopra.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4945fd6836",
  "kind": "yes/no",
  "text": "Claim: The band american composer Steve Goulding is the drummer for is not British. The singer whose debut album is Don't Let It Go to Waste isn't British either.\n\nPassages:\n\n[Don't Let It Go to Waste]\nDon't Let It Go to Waste is the debut album from Matt Willis, released on 20 November 2006.\n\n[The Mekons]\nThe Mekons are a British-American rock band.\n\n[Steve Goulding]\nSteve Goulding (born 1954, South London, England) is an English drummer, who has played as a member of Graham Parker and The Rumour, The Associates, Poi Dog Pondering, The Waco Brothers and The Mekons.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4a20ae7853",
  "kind": "yes/no",
  "text": "Claim: The opera that mentions the red wine that, like Lagrein, is a descendant of Teroldego is not an opera with three act. Neither is the opera Cardillac.\n\nPassages:\n\n[Marzemino]\nThe wine is most noted for its mention in the opera \"Don Giovanni\" of Wolfgang Amadeus Mozart (\"Versa il vino!\n\n[Lagrein]\nAlong with Marzemino, it is a descendant of Teroldego, and related to Syrah, Pinot noir and Dureza.\n\n[Cardillac]\nCardillac is an opera by Paul Hindemith in three acts and four scenes.\n\n[Don Giovanni]\nDon Giovanni (] ; K. 527; complete title: \"Il dissoluto punito, ossia il Don Giovanni\" , literally \"The Rake Punished, namely Don Giovanni\" or \"The Libertine Punished\") is an opera in two acts with music by Wolfgang Amadeus Mozart and Italian libretto by Lorenzo Da Ponte.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q205dc37eb5",
  "kind": "yes/no",
  "text": "Claim: The brother-in-law of Victoria Ocampo and James Norman Hall are not both authors.\n\nPassages:\n\n[Victoria Ocampo]\nHer sister, Silvina Ocampo, also a writer, was married to Adolfo Bioy Casares.\n\n[James Norman Hall]\nJames Norman Hall (22 April 1887 – 5 July 1951) was an American author best known for the novel \"Mutiny on the Bounty\" with co-author Charles Nordhoff.\n\n[Adolfo Bioy Casares]\nAdolfo Bioy Casares (] ; September 15, 1914 – March 8, 1999) was an Argentine fiction writer, journalist, and translator.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qaf9beffdca",
  "kind": "yes/no",
  "text": "Tweet: WTF!!! #billcosby conviction was just overturned by the Pennsylvania Supreme Court!!!! #wtf #WHY #me2 @BillCosby",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q74402100f9",
  "kind": "yes/no",
  "text": "Claim: In Search of the Castaways was the Walt Disney production that was based on Jules Verne's 1868 novel \"In Search of the Castaways\". It was not based on the prequel to The Monkey's Uncle.\n\nPassages:\n\n[The Misadventures of Merlin Jones]\nThe Misadventures of Merlin Jones is a 1964 Walt Disney production starring Tommy Kirk and Annette Funicello.\n\n[The Monkey's Uncle]\nThe film is a sequel to the 1964 film \"The Misadventures of Merlin Jones.\"\n\n[In Search of the Castaways (film)]\nIn Search of the Castaways is a 1962 Walt Disney Productions feature film starring Hayley Mills and Maurice Chevalier in a tale about a worldwide search for a shipwrecked sea captain. The film was directed by Robert Stevenson from a screenplay by Lowell S. Hawley based upon Jules Verne's 1868 adventure novel \"Captain Grant's Children\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q19ad6f71bd",
  "kind": "yes/no",
  "text": "Text: wait what the fuck that solo yolo is mad?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q9d038a3c5a",
  "kind": "yes/no",
  "text": "Claim: During the Great Depression, President Merkley dedicated this building in Clackamas County, Oregon. Oregon Route 173 runs from that building.\n\nPassages:\n\n[Timberline Lodge]\nTimberline Lodge was dedicated September 28, 1937, by President Franklin D. Roosevelt.\n\n[Oregon Route 173]\nOregon Route 173 is an Oregon state highway running from Timberline Lodge in Clackamas County to U.S. Route 26 near Government Camp.\n\n[Charles Heaney]\nDuring the Great Depression in the 1930s, he worked for the Works Progress Administration as an artist and did several works featuring Mount Hood and Timberline Lodge as the subject matter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q74383878ad",
  "kind": "yes/no",
  "text": "Tweet: If I invite you over for dinner, it’s my intentions of paying and making everything as my gift to you as my guest",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qc08f4a348d",
  "kind": "yes/no",
  "text": "Claim: Penlee Point, the coastal headland to the SW of the village of Rame in a southeastern county in the nippon, lies at the entrance of the Plymouth Sound. This county is the location of the Doom Bar.\n\nPassages:\n\n[Penlee Point, Rame]\nPenlee Point (Cornish: Penn Legh , meaning \"stone-slab headland\") is a coastal headland to the southeast of the village of Rame in southeast Cornwall, UK. The point lies at the entrance to Plymouth Sound.\n\n[Cornwall]\nCornwall ( , ; Cornish: Kernow ] ) is a ceremonial county in the United Kingdom.\n\n[Doom Bar]\nThe Doom Bar (previously known as Dunbar sands, Dune-bar, and similar names) is a sandbar at the mouth of the estuary of the River Camel, where it meets the Celtic Sea on the north coast of Cornwall, England.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7e5f552c30",
  "kind": "yes/no",
  "text": "Tweet: Perfect way to end a 2+ hour @SunCountryAir deley: getting stuck on the tarmack at @mspairport waiting to go to a gate for almost an hour 🙄",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q6220d46b2d",
  "kind": "yes/no",
  "text": "Claim: The developer of origami technique Wet-folding was given the Order of the Rising Sun, 5th class, award. The award was given by Hirohito during the Shōwa era in the history of the country Hideo Kanaya is from.\n\nPassages:\n\n[Wet-folding]\nWet-folding is an origami technique developed by Akira Yoshizawa that employs water to dampen the paper so that it can be manipulated more easily.\n\n[Hirohito]\nThe word \"Shōwa\" is the name of the era that corresponded with the Emperor's reign, and was made the Emperor's own name upon his death.\n\n[Hideo Kanaya]\nHideo Kanaya (Shinjitai: 金谷 秀夫 , Hideo Kanaya , February 3, 1945 – December 19, 2013) was a Grand Prix motorcycle road racer from Japan.\n\n[Akira Yoshizawa]\nIn 1983, Emperor Hirohito awarded him the Order of the Rising Sun, 5th class, one of the highest honors bestowed in Japan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
