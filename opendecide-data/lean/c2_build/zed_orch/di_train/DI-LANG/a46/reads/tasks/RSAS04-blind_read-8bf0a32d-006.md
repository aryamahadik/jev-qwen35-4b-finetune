# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-006.json

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
  "qid": "qd711a51a9e",
  "kind": "yes/no",
  "text": "Tweet: why is the weather having a mid life crisis",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q347cdb6641",
  "kind": "yes/no",
  "text": "Claim: Derrick Leon Green joined the band Linfield in 1997. The actor who starred as Pease in the movie The Marc Pease Experience did not.\n\nPassages:\n\n[The Marc Pease Experience]\nThe film stars Jason Schwartzman as Pease, Ben Stiller as Marc's former mentor, and Anna Kendrick as his love interest.\n\n[Jason Schwartzman]\nJason Francesco Schwartzman (born June 26, 1980) is an American actor, screenwriter and musician.\n\n[Derrick Green]\nDerrick Leon Green (born January 20, 1971) is an American musician, best known as the singer of Brazilian heavy metal band Sepultura. He joined the band in 1997 after the departure of group founder Max Cavalera.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2abca5dc62",
  "kind": "yes/no",
  "text": "Claim: Corylopsis and Impatiens are both genus of plants.\n\nPassages:\n\n[Impatiens]\nImpatiens is a genus of about 850 to 1,000 species of flowering plants, widely distributed throughout the Northern Hemisphere and the tropics.\n\n[Corylopsis]\nCorylopsis is a genus of nearly 30 species of shrubs in the witch hazel family, Hamamelidaceae, native to eastern Asia with the majority of species endemic in China but with some also in Japan, Korea, and the Himalayas.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc29ee1a778",
  "kind": "yes/no",
  "text": "Text: Tim for prime minister #TheCircle",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q138d564daa",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "yeah your girl is fine but does she pass out while giving blood",
   "Passing out while giving blood is not attractive"
  ]
 },
 {
  "qid": "q1fea02eb4f",
  "kind": "yes/no",
  "text": "Claim: \"Fires of Winter\" reached the \"New York Times\" bestseller list.\n\nPassages:\n\n[Johanna Lindsey]\nJohanna Lindsey (born Johanna Helen Howard, March 10, 1952), is one of the most popular American writers of historical romance novels worldwide. All of her books reached the \"New York Times\" bestseller list, many reaching No. 1.\n\n[Fires of Winter]\nFires of Winter is a novel by Johanna Lindsey originally published in September 1980 by Avon Books.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6ff0fb50d6",
  "kind": "yes/no",
  "text": "Claim: American singer Aaliyah had a video director that directed Soothe My Soul, and also had to face allegation of illegal marriage with R. Kelly.\n\nPassages:\n\n[Warren Fu]\nHe has directed promos for Daft Punk, The Weeknd, Snoop Dogg, Pharrell Williams, The Strokes, HAIM, The Killers, Depeche Mode, Weezer, Mark Ronson, Julian Casablancas, and Aaliyah.\n\n[Soothe My Soul]\nThe music video directed by Warren Fu was premiered on 28 March 2013.\n\n[Aaliyah]\nAfter facing allegations of an illegal marriage with R. Kelly, Aaliyah ended her contract with Jive and signed with Atlantic Records.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q207de21dc7",
  "kind": "yes/no",
  "text": "Tweet: I need my back and neck cracked differentlyyy",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4cb0ca5962",
  "kind": "yes/no",
  "text": "Claim: The actress that appeared Faster (2010 film) is known for her role as Kelor in a shared universe centered on a series of superhero films. This films were distributed by Cinemax\n\nPassages:\n\n[DC Extended Universe]\nThe Justice League Universe (JLUDCEUUJLDCE), more commonly known by its unofficial name as the DC Extended Universe (DCEU), is an American media franchise and shared universe, centered on a series of superhero films distributed by Warner Bros.\n\n[Carla Gugino]\nCarla Gugino ( ; ] ; born August 29, 1971) is an American actress. Her feature film work includes starring roles in \"Son in Law\" (1993), \" Sin City\" (2005), \"Night at the Museum\" (2006), \"Mr. Popper's Penguins\" (2011), \"San Andreas\" (2015), \"The Space Between Us\" (2017), and \"Gerald's Game\" (2017) as well as Kelor in the DC Extended Universe.\n\n[Faster (2010 film)]\nTom Berenger, Oliver Jackson-Cohen, Adewale Akinnuoye-Agbaje and Carla Gugino also appear.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf7f4f795c7",
  "kind": "yes/no",
  "text": "Claim: The actor, who played Karl Rove in \"That's My Bush!\", from Stockton, CA appeared in Psych, an American detective comedy-drama television series created by Shawn.\n\nPassages:\n\n[Psych]\nPsych is an American detective comedy-drama television series created by Steve Franks and broadcast on USA Network with syndicated reruns on ION Television.\n\n[Kurt Fuller]\nHe graduated from Lincoln High School in Stockton, California in 1971, and U.C. Berkeley in 1976.\n\n[That's My Bush!]\nCarrie Quinn Dolin played Laura Bush, and Kurt Fuller played Karl Rove.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe870079480",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "Just saw a cop riding a segway?!! So glad my taxes paid for that.",
   "I don't approve of my taxes paying for cops to ride segways."
  ]
 },
 {
  "qid": "q4fefedcb4a",
  "kind": "yes/no",
  "text": "Claim: IndiGo is a low-cost biplane airline headquartered at Gurgaon, that is the largest airline in India, the third largest domestic airline being the flag carrier airline of India.\n\nPassages:\n\n[IndiGo]\nIt is the largest airline in India by passengers carried and fleet size, with a 38.7% market share as of July 2017.\n\n[Air India]\nAdditionally, the carrier is the third largest domestic airline in India in terms of passengers carried (after IndiGo and Jet Airways) with a market share of 13.5% as of July 2017.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qbcb77138a0",
  "kind": "yes/no",
  "text": "Claim: The National Policy Forum was set up by the leader of the British Labour Party. Trade unions were legalized in his country in the early 1870s.\n\nPassages:\n\n[National Policy Forum]\nThe National Policy Forum (NPF) of the British Labour Party is part of the policy-making system of the Party, set up by Leader Tony Blair as part of the Partnership in Power process.\n\n[Trade unions in the United Kingdom]\nLegalised in 1871, the trade union movement sought to reform socio-economic conditions for working men in British industries, and the trade unions' search for this led to the creation of a Labour Representation Committee which effectively formed the basis for today's Labour Party, which still has extensive links with the Trade Union Movement in Britain.\n\n[Tony Blair]\nAnthony Charles Lynton Blair (born 6 May 1953) is a British politician who served as Prime Minister of the United Kingdom from 2 May 1997 to 27 June 2007 and Leader of the Labour Party from 21 July 1994 to 24 June 2007.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9a3de88ae9",
  "kind": "yes/no",
  "text": "Claim: The air date of the \"30 Rock\" Grammy winning episode that guest starred an actor from the films \"Horrible Bosses\" (2011) and \"Hall Pass\" (2011) was March 8, 2007.\n\nPassages:\n\n[Jason Sudeikis]\nHe starred in the films \"Horrible Bosses\" (2011), \"Hall Pass\" (2011), \"We're the Millers\" (2013), \"Horrible Bosses 2\" (2014), \"Sleeping with Other People\" (2015), \"Tumbledown\" (2015), \"The Book of Love\" (2016) and \"Race\" (2016).\n\n[The Fighting Irish]\nIt aired on March 8, 2007 in the United States. Guest stars who appeared in this episode were Dan Bakkedahl, Katrina Bowden, Henry Boyle, Anna Chlumsky, Siobhan Fallon Hogan, Chris Hoch, Alice Kremelberg, Nathan Lane, Boris McGiver, John F Mooney, Brian Murray, Maulik Pancholy, Lonny Ross, Molly Shannon, Jason Sudeikis and Kristen Sudeikis.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q7cbf778c73",
  "kind": "yes/no",
  "text": "Claim: Winifred Deforest Coffin starred in this Fontainebleau film. Roving Mars was released later than than the second sequel to this movie.\n\nPassages:\n\n[Winifred Deforest Coffin]\nCoffin was an actress who appeared in Hollywood films (\"Now You See Him, Now You Don't\"), and many television shows including \"Adam-12\", \"The Doris Day Show\", \"The Debbie Reynolds Show\", \"Lancer\", \"The Beverly Hillbillies\", \"High Chaparral\", \"Death Valley Days\", \"Petticoat Junction\", \"Perry Mason\", \"Bonanza\", \"Bewitched\", \"Honey West\", \"The Ann Sothern Show\".\n\n[Roving Mars]\nRoving Mars is an IMAX documentary film about the development, launch, and operation of the Mars Exploration Rovers, Spirit and Opportunity.\n\n[The Strongest Man in the World]\nThe Strongest Man in the World is a 1975 Disney film starring Kurt Russell, still a student in the fictional Medfield College.\n\n[Now You See Him, Now You Don't]\nIt is the sequel to the 1969 film \"The Computer Wore Tennis Shoes\" and was followed by 1975's \"The Strongest Man in the World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9e960d197b",
  "kind": "yes/no",
  "text": "Claim: This Federation of Indian Airlines member is owned by Indian business conglomerate Tata Communications.\n\nPassages:\n\n[Federation of Indian Airlines]\nThe Federation of Indian Airlines (FIA) is an airline industry body in India. Its members are Jet Airways, IndiGo, SpiceJet and GoAir.\n\n[GoAir]\nGoAir is a low-cost carrier based in Mumbai, India. It is owned by the Indian business conglomerate Wadia Group.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q403f9ac709",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Oh good, it's time for the bi-monthly random power outage.",
   "I'm getting frustrated with all of these power outages lately"
  ]
 },
 {
  "qid": "q2a9d4cab71",
  "kind": "yes/no",
  "text": "Claim: Carlo Buccirosso had a role in a movie that premiered at Cannes Film Festival.\n\nPassages:\n\n[Carlo Buccirosso]\nCarlo Buccirosso (1 May 1954 in Naples, Italy) is an Italian actor, film director and comedian best known for his roles in Il divo (2008), Un'estate ai Caraibi (2009) and Un ciclone in famiglia (2006-2008), The Great Beauty (2013).\n\n[The Great Beauty]\nThe Great Beauty (Italian: La grande bellezza ] ) is a 2013 Italian art drama film co-written and directed by Paolo Sorrentino. It premiered at the 2013 Cannes Film Festival where it was screened in competition for the Palme d'Or.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd7770b25c2",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Just almost got hit on the highway by a @CityofSanDiego truck 🤪 tysm for making me feel safe guys!!!",
   "I would write “Just almost got hit on the highway by a @CityOfSanDiego truck! Wish we had gotten his plate number to report his dangerous driving.”"
  ]
 },
 {
  "qid": "q63fab241d0",
  "kind": "yes/no",
  "text": "Claim: Breakable You is a film that was made into a movie staring Alfredo \"Alfred\" Molina who is also known for roles in Raiders of the Lost Ark and Enchanted April.\n\nPassages:\n\n[Alfred Molina]\nAlfredo \"Alfred\" Molina (born 24 May 1953) is an English-American actor, known for his roles in \"Raiders of the Lost Ark\" (1981), \"Enchanted April\" (1992), \"Maverick\" (1994), \"Boogie Nights\" (1997), \"Chocolat\" (2000), \"Spider-Man 2\" (2004), \"The Da Vinci Code\" (2006), \"An Education\" (2009), \"\" (2010), \"The Sorcerer's Apprentice\" (2010), \"Rango\" (2011) and \"Whiskey Tango Foxtrot\" (2016).\n\n[Breakable You]\nBreakable You is the fourth novel written by American author Brian Morton. The book was made into a 2017 film starring Holly Hunter, Tony Shalhoub and Alfred Molina.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q873b252c5e",
  "kind": "yes/no",
  "text": "Tweet: When you get woken up at 3am because of aftershocks from an earthquake 👍😩",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q1f7a3e99a3",
  "kind": "yes/no",
  "text": "Claim: Blake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro whose role was portrayed by John Forsythe, and also appeared as a guest on several talk and variety shows and as a panelist on quiz formatted game shows.\n\nPassages:\n\n[John Forsythe]\nHe also appeared as a guest on several talk and variety shows and as a panelist on numerous game shows.\n\n[Blake Carrington]\nBlake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro. The role was portrayed by John Forsythe from the first episode of the series in 1981 until its finale in 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3e1daf41e1",
  "kind": "yes/no",
  "text": "Claim: A video game published by the company that released The Lost Mind of Dr. Brain, includes an antagonist figure who's mystery is the core of the series. SAS: Secure Tomorrow utilizes Jupiter EX engine similar, if not identical to the one in that game.\n\nPassages:\n\n[Alma Wade]\nAlma Wade is a major antagonist and key figure in the \"F.E.A.R.\" series of first-person shooter horror video games by Monolith Productions, introduced in \"F.E.A.R.\" in 2005. The mystery of Alma is the very core of the series.\n\n[The Lost Mind of Dr. Brain]\nThe Lost Mind of Dr. Brain is the third installment of the educational Dr. Brain series, created and published by Sierra On-Line.\n\n[SAS: Secure Tomorrow]\nThe game utilizes Jupiter EX engine, similar, if not identical to the one in F.E.A.R..\n\n[F.E.A.R.]\nF.E.A.R. First Encounter Assault Recon is a survival horror first-person shooter video game developed by Monolith Productions and published by Sierra Entertainment.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q641f670062",
  "kind": "yes/no",
  "text": "Claim: The former Major League Baseball player play who worked on the same broadcast team as Kim Kelch was a first baseman.\n\nPassages:\n\n[Jim Kelch]\nJim Kelch is a broadcaster for the Cincinnati Reds. Joining Kelch on the broadcast team for the Reds are Marty Brennaman, Thom Brennaman, Chris Welsh, George Grande, and, occasionally, Sean Casey.\n\n[Sean Casey (baseball)]\nSean Thomas Casey (born July 2, 1974), nicknamed \"The Mayor,\" is a former Major League Baseball first baseman for the Cleveland Indians, Cincinnati Reds, Pittsburgh Pirates, Detroit Tigers, and Boston Red Sox.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7046ec8f96",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "@lora__ SHOCKED. How am I supposed to tell the kids they're not going to Disneyland on June 21st after all? It's already been cancelled 36 times! https://t.co/SV8gpPn6yw",
   "These people were aware of the risks when they booked these trips so they should not be surprised when they get cancelled."
  ]
 },
 {
  "qid": "q346498603c",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Mad how many people don’t use indicators these days.",
   "Mad how many cars they make now without indicators 🙃"
  ]
 },
 {
  "qid": "qda400521e8",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I've been depressed for a long time and I never managed to kill anyone. It isn't hard not to do.",
   "At least half of my days are still bad days and let me tell you, i've never once killed 8 people because of it. A true miracle apparently"
  ]
 },
 {
  "qid": "q275b4ab94d",
  "kind": "yes/no",
  "text": "Claim: \"The Closer I Get to You\" is a romantic ballad performed by African American blues, soul, R&B, and folk artist-songwriter Roberta Flack, and Donny Hathaway, an American jazz, blues, soul and gospel singer, songwriter, arranger and pianist that signed with Atlantic Records in 1969.\n\nPassages:\n\n[The Closer I Get to You]\n\"The Closer I Get to You\" is a romantic ballad performed by African American jazz, soul, R&B, and folk singer-songwriter Roberta Flack and African American soul musician Donny Hathaway.\n\n[Donny Hathaway]\nDonny Edward Hathaway (October 1, 1945 – January 13, 1979) was an American jazz, blues, soul and gospel singer, songwriter, arranger and pianist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa21e033da3",
  "kind": "yes/no",
  "text": "Claim: Bernard Blancan received the Best Actor nomination at Cannes in 2006 for the Rachid Bouchareb film Days of Glory.\n\nPassages:\n\n[Days of Glory (2006 film)]\nDays of Glory (French: \"Indigènes - \"Natives\"\" ; Arabic: بلديون‎ ‎ ) is a 2006 French film directed by Rachid Bouchareb.\n\n[Bernard Blancan]\nHe shared the award for Best Actor for his role in \"Days of Glory\" at the 2006 Cannes Film Festival.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5cf868add6",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Having morning sickness when you're not actually pregnant is all the fun",
   "Having morning sickness when you're not actually sick is not fun!"
  ]
 },
 {
  "qid": "q4befadadb4",
  "kind": "yes/no",
  "text": "Claim: The star on the Mexican telenovela \"Amy, la niña de la mochila azul\" Danna Paola is also a singer, model, jewelry designer, and recording star.\n\nPassages:\n\n[Danna Paola]\nDanna Paola Rivera Munguía (born 23 June 1995 in Mexico City), better known as Danna Paola, is a Mexican singer, actress, model, fashion designer and recording artist.\n\n[Amy, la niña de la mochila azul]\nAmy, la niña de la mochila azul \"(Amy, the Girl with the Blue Schoolbag)\" is a Mexican telenovela produced by Televisa in 2004. Starring Danna Paola, Nora Salinas and Eduardo Capetillo, while Pedro Armendáriz Jr. and Tatiana star as co-protagonists with Alejandro Tommasi, Lorena Herrera, Alejandra Meyer and Alejandra Procuna as antagonists.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0b87a06d52",
  "kind": "yes/no",
  "text": "Claim: The nationality of the 38 year old professional footballer who was sold to Chelsea during the 2004–05 Olympique de Marseille season is Ivorian.\n\nPassages:\n\n[Didier Drogba]\nDidier Yves Drogba Tébily (] ; born 11 March 1978) is an Ivorian professional footballer who plays as a striker for American club Phoenix Rising FC.\n\n[2004–05 Olympique de Marseille season]\nWith striker Didier Drogba being sold to Chelsea, and replacements Habib Bamogo and Péguy Luyindula not performing at a similar level, the goal-scoring went dry, but in spite of scoring two points less than the previous season, l'OM finished two positions above the previous season.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf7691e8b1b",
  "kind": "yes/no",
  "text": "Claim: The The is a post-punk band, the band whose 1994 debut album is named My Animal, is not.\n\nPassages:\n\n[Boy Hits Car]\nThe band was formed in 1993.\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.\n\n[The The]\nThe The (pronunciation: ) are an English post-punk band.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8932805193",
  "kind": "yes/no",
  "text": "Claim: Rosey Grier attended Boston College. He went on to play the role of Gabe Cooper in the TV Series that Darby Hinton portrayed Israel Boone in.\n\nPassages:\n\n[Darby Hinton]\nFrom 1964–1970, he portrayed Israel Boone, a son of American pioneer Daniel Boone, on the NBC adventure series \"Daniel Boone\", with Fess Parker in the title role.\n\n[Rosey Grier]\nHe was a notable college football player for The Pennsylvania State University who earned a retrospective place in the National Collegiate Athletic Association 100th anniversary list of 100 most influential student athletes.\n\n[Daniel Boone (1964 TV series)]\nActor and former NFL football player Rosey Grier made regular appearances as Gabe Cooper in the 1969 to 1970 season.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qbd43ff70da",
  "kind": "yes/no",
  "text": "Claim: Kevin Spacey, who also appeared in \"The Usual Suspects\" (1995), starred in the 2017 action crime comedy by Kevin Pollak in which Lanny Joon played JD.\n\nPassages:\n\n[Kevin Spacey]\nHe gained critical acclaim in the early 1990s that culminated in his first Academy Award for Best Supporting Actor for the neo-noir crime thriller \"The Usual Suspects\" (1995), and an Academy Award for Best Actor for midlife crisis-themed drama \"American Beauty\" (1999).\n\n[Baby Driver]\nBaby Driver is a 2017 action crime comedy film written and directed by Edgar Wright. It stars Ansel Elgort, Kevin Spacey, Lily James, Eiza González, Jon Hamm, Jamie Foxx, and Jon Bernthal.\n\n[Lanny Joon]\nHe also played the role of JD in Edgar Wright's film \"Baby Driver\", opposite Jamie Foxx and Ansel Elgort.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfe3f49e805",
  "kind": "yes/no",
  "text": "Claim: The musician that wrote Raymonda served as director of the Bill Sawyer Orchestra when he started composing Symphony No 9 in D minor.\n\nPassages:\n\n[Raymonda]\nRaymonda (Russian: Раймонда ) is a ballet in three acts, four scenes with an apotheosis, choreographed by Marius Petipa, with music by Alexander Glazunov, his opus 57.\n\n[Alexander Glazunov]\nHe served as director of the Saint Petersburg Conservatory between 1905 and 1928 and was instrumental in the reorganization of the institute into the Petrograd Conservatory, then the Leningrad Conservatory, following the Bolshevik Revolution.\n\n[Symphony No. 9 (Glazunov)]\nAlexander Glazunov's Symphony No. 9 in D minor was begun in 1910, but was still unfinished by the time of his death in 1936.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5bd0926160",
  "kind": "yes/no",
  "text": "Claim: \"Get Stoned\" is a song by a Californian rock band. The Fatima Mansions rock band was formed earlier than this band.\n\nPassages:\n\n[Get Stoned]\n\"Get Stoned\" is a song by American rock band Hinder.\n\n[The Fatima Mansions]\nThe Fatima Mansions were an art rock group formed in 1988 by Cork singer/keyboardist Cathal Coughlan, formerly of Microdisney.\n\n[Hinder]\nHinder is an American rock band from Oklahoma that was formed in 2001 by lead singer Austin Winkler, lead guitarist Joe \"Blower\" Garvey, and drummer Cody Hanson.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0f4fc136fe",
  "kind": "yes/no",
  "text": "Claim: The genus which contains the plant Scarlet sage has more species than the genus Arachis.\n\nPassages:\n\n[Salvia]\nSalvia is the largest genus of plants in the mint family, Lamiaceae, with nearly 1000 species of shrubs, herbaceous perennials, and annuals.\n\n[Scarlet sage]\nScarlet sage may refer to either of two plants in the genus \"Salvia\" (sages and claries):\n\n[Arachis]\nArachis is a genus of about 70 species of annual and perennial flowering plants in the pea family (Fabaceae), native to South America, and was recently assigned to the informal monophyletic \"Pterocarpus\" clade of the Dalbergieae.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1b39f90259",
  "kind": "yes/no",
  "text": "Text: The fact I nearly froze on my way to work this morning is definitely a sign it's not summer anymore #freezing",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qa52001b7c5",
  "kind": "yes/no",
  "text": "Claim: The song of the same name of a band's album released before The Revelation was used for a WWE event that took place on May 1, 2011. This band released the EP \"Take 'Em Out\".\n\nPassages:\n\n[Take 'Em Out]\nTake 'Em Out is a four-song EP released by American hard rock band, Rev Theory.\n\n[Extreme Rules (2011)]\nExtreme Rules was a professional wrestling pay-per-view (PPV) event produced by WWE, which took place on May 1, 2011 at the St. Pete Times Forum in Tampa, Florida.\n\n[Justice (Rev Theory album)]\nThe song Justice was used for WWE's Extreme Rules (2011).\n\n[The Revelation (Rev Theory album)]\nIt is the band's first full-length studio album since \"Justice\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qfeab150132",
  "kind": "yes/no",
  "text": "Claim: Multinational Monitor has fewer issues each month than In These Times does.\n\nPassages:\n\n[Multinational Monitor]\nThe Multinational Monitor was a bimonthly magazine founded by Ralph Nader in 1980.\n\n[In These Times]\nIn These Times is an American politically progressive/democratic socialist monthly magazine of news and opinion published in Chicago, Illinois.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q114cb59ecb",
  "kind": "yes/no",
  "text": "Tweet: I reverse imaged searched a selfie and it under visually similar images it is exclusively asian woman my am I white passing narrative is quaking",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q8f8ecfdd20",
  "kind": "yes/no",
  "text": "Claim: The brand where Lauren Gold, who is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video, is currently owned by a fashion retailer based in Columbus, Ohio.\n\nPassages:\n\n[L Brands]\nL Brands Inc. (formerly known as \"Limited Brands Inc\" and \"The Limited Inc.\") is an American fashion retailer based in Columbus, Ohio.\n\n[La Senza]\nThe La Senza brand is currently owned by L Brands which operates and owns La Senza stores in Canada and uses a franchise model for the operation of stores outside Canada.\n\n[Lauren Gold]\nGold is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video as well as her recurring appearance in La Senza ad campaigns.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa3b162ddca",
  "kind": "yes/no",
  "text": "Text: Social Care for the young is basically a bath board and bed rest and your done.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q0035a01439",
  "kind": "yes/no",
  "text": "Claim: The host of the 2014 edition of the MTV Africa Music Awards began their career with \"I'm Gonna Git You Sucka\".\n\nPassages:\n\n[MTV Africa Music Awards 2014]\nThe show was hosted by American comedian and actor Marlon Wayans.\n\n[Marlon Wayans]\nMarlon Lamont Wayans (born July 23, 1972) is an American actor, comedian, screenwriter, and film producer, beginning with his role as a pedestrian in \"I'm Gonna Git You Sucka\" in 1988.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q86b17a9b78",
  "kind": "yes/no",
  "text": "Text: Submitted my application for PhD funding today, then shit myself and wanted to withdraw it 😂🙈",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q896a6e69cb",
  "kind": "yes/no",
  "text": "Text: Man I just love it when I'm forced to pitch two games back to back bc our other pitcher didn't show up",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q13e3c12410",
  "kind": "yes/no",
  "text": "Claim: Both the anime magazine not to be confused with Disney Adventures and The Ring are not still in publication.\n\nPassages:\n\n[Disney Adventures]\nIt should not be confused with the (now defunct) \"Disney Magazine\".\n\n[The Ring (magazine)]\nThe Ring (often called The Ring magazine or Ring TV) is an American boxing magazine that was first published in 1922 as a boxing and wrestling magazine. The magazine is currently owned by Oscar De La Hoya's Golden Boy Enterprises, which acquired it in 2007.\n\n[Disney Magazine]\nDisney Magazine was an official Disney magazine that was published quarterly from December 1965 to April 2005.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd461328bd5",
  "kind": "yes/no",
  "text": "Claim: Tibbers Castle is 63 miles southeast of a country house in Dumfries and Galloway in Scotland.\n\nPassages:\n\n[Drumlanrig Castle]\nDrumlanrig Castle is situated on the Queensberry Estate in Dumfries and Galloway, Scotland.\n\n[Tibbers Castle]\nTo the east is the village of Carronbridge and to the north west is a 16th-century country house, Drumlanrig Castle.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q89fc92dd31",
  "kind": "yes/no",
  "text": "Claim: The documentary film by Sandi Sissel was released before Escape from Suburbia. This a 2007 English documentary film written and directed by Gregory Greene.\n\nPassages:\n\n[The End of Suburbia]\nThe End of Suburbia: Oil Depletion and the Collapse of The American Dream is a 2004 documentary film concerning peak oil and its implications for the suburban lifestyle, written and directed by Toronto-based filmmaker Gregory Greene.\n\n[Chicken Ranch (film)]\nChicken Ranch is a 1983 documentary film by Nick Broomfield about the famous legalised brothel, the Chicken Ranch, in Pahrump, Nevada.\n\n[Sandi Sissel]\n\", \"Chicken Ranch\", \"Mother Teresa (1986)\" as well as TV shows like 60 Minutes, and feature films like \"Mr. and Mrs. Smith\".\n\n[Escape from Suburbia]\nEscape from Suburbia: Beyond the American Dream is a 2007 Canadian documentary film written and directed by Gregory Greene, as a sequel to Greene's film \"The End of Suburbia\", and set to address what is termed \"the upcoming energy crisis\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 }
]
