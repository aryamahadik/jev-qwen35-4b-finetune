# A46 replay label-noise blind read RSBS07-blind_read-cc7738f7-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS07-blind_read-cc7738f7-003.json

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
  "qid": "qbf863de3da",
  "kind": "yes/no",
  "text": "Claim: The line of the railroad the designer of McKim's School worked for was the port of Baltimore west to Sandy Hook.\n\nPassages:\n\n[Baltimore and Ohio Railroad]\nAt first this railroad was located entirely in the state of Maryland with an original line from the port of Baltimore west to Sandy Hook.\n\n[McKim's School]\nIt was designed by Baltimore architects William Howard and William Small and erected in 1833.\n\n[William Howard (engineer)]\nWilliam Howard (1793–1834) was an American mechanical engineer who was one of the first to work for the Baltimore and Ohio Railroad.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd4aaca9dfb",
  "kind": "yes/no",
  "text": "Claim: \"The Sandman\" comic book series and \"The Sandman: The Dream Hunters\" novella are written by the award-winning Neil Gaiman.\n\nPassages:\n\n[The Sandman: The Dream Hunters]\n\"The Sandman: The Dream Hunters\" is a novella by English author Neil Gaiman, illustrated by Yoshitaka Amano.\n\n[The Sandman (Vertigo)]\nThe Sandman is a comic book series written by Neil Gaiman and published by DC Comics.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q3bd756c558",
  "kind": "yes/no",
  "text": "Claim: An opera was written by the Dutch poet born in the Kingdom of Bohemia, also referred to by the name Dutch Kingdom. Renée Fleming performed in this opera.\n\nPassages:\n\n[Rusalka (opera)]\n114, is an opera ('lyric fairy tale') by Antonín Dvořák.\n\n[Kingdom of Bohemia]\nThe Kingdom of Bohemia, sometimes in English literature referred to as the Czech Kingdom (Czech: \"České království\" ; German: \"Königreich Böhmen\" ; Latin: \"Regnum Bohemiae\" , sometimes Latin: \"Regnum Czechorum\" ), was a medieval and early modern monarchy in Central Europe, the predecessor of the modern Czech Republic.\n\n[Renée Fleming]\nHer signature roles include Countess Almaviva in Mozart's \"Le nozze di Figaro\", Desdemona in Verdi's \"Otello\", Violetta in Verdi's \"La traviata\", the title role in Dvořák's \"Rusalka\", the title role in Massenet's \"Manon\", the title role in Massenet's \"Thaïs\", the title role in Richard Strauss's \"Arabella\", the Marschallin in \"Der Rosenkavalier\", and the Countess in \"Capriccio\".\n\n[Jaroslav Kvapil]\nJaroslav Kvapil (25 September 1868 in Chudenice, Kingdom of Bohemia – 10 January 1950 in Prague) was a Czech poet, playwright, and librettist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbe232612c5",
  "kind": "yes/no",
  "text": "Claim: The 1993 album that the song Juntos (Together) is on and The Black Hole are not both sports films.\n\nPassages:\n\n[Juntos (Together)]\nThe song was released digitally via the iTunes Store by Walt Disney Records and Universal Music Latin on January 20, 2015, as the lead single from the soundtrack for \"McFarland, USA\".\n\n[The Black Hole]\nThe Black Hole is a 1979 American science fiction film directed by Gary Nelson and produced by Walt Disney Productions.\n\n[McFarland, USA]\nMcFarland, USA (also known as McFarland) is a 2015 American sports drama film directed by Niki Caro, produced by Mark Ciardi and Gordon Gray, written by Christopher Cleveland, Bettina Gilois and Grant Thompson with music composed by Antônio Pinto.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q1add79139a",
  "kind": "yes/no",
  "text": "Post: why is it so hard to find tshirts with cool wizards on them",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qea7e4e1711",
  "kind": "yes/no",
  "text": "Claim: Margulis lemma is a differential geometry mathematical subfield. Its founder was born in the 6th century, before one of the minds behind Leftover hash lemma.\n\nPassages:\n\n[Margulis lemma]\nIn differential geometry, a subfield of mathematics, the Margulis lemma (named after Grigory Margulis) is a result about discrete subgroups of isometries of a non-positively curved Riemannian manifolds (e.g. the hyperbolic n-space).\n\n[Leonid Levin]\nLeonid Anatolievich Levin ( ; Russian: Леони́д Анато́льевич Ле́вин ; Ukrainian: Леоні́д Анато́лійович Ле́він ; born November 2, 1948) is a Soviet-American computer scientist.\n\n[Leftover hash lemma]\nThe leftover hash lemma is a lemma in cryptography first stated by Russell Impagliazzo, Leonid Levin, and Michael Luby.\n\n[Grigory Margulis]\nGregori Aleksandrovich Margulis (Russian: Григо́рий Алекса́ндрович Маргу́лис , first name often given as Gregory, Grigori or Grigory; born February 24, 1946) is a Russian-American mathematician known for his work on lattices in Lie groups, and the introduction of methods from ergodic theory into diophantine approximation.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q53541fe7cb",
  "kind": "yes/no",
  "text": "Text: Oh wow, trolls really have a lot of time on there hands, jeez 🙄 they really don’t like getting banned #twitchtrolls",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf9e7dea6ec",
  "kind": "yes/no",
  "text": "Claim: The NorthCap University is located in India. The establishment, where the writer of the lyrics for the ASEAN Song of Unity studied for his Ph.D. in Govt, is not.\n\nPassages:\n\n[The Northcap University]\nThe NorthCap University, formerly ITM University, is an autonomous university situated in Sector 23-A, Gurugram, Haryana, India.\n\n[Nicanor Tiongson]\nHe holds a Bachelor of Humanities degree from the Ateneo de Manila University, and M.A. and Ph.D. in Philippine Studies from the University of the Philippines.\n\n[ASEAN Song of Unity]\nThe lyrics were written by Nicanor Tiongson and the music was composed by Ryan Cayabyab.\n\n[University of the Philippines]\nThe University of the Philippines (UP; Filipino: \"Unibersidad ng Pilipinas\" or \"Pamantasan ng Pilipinas\") is a state university system in the Philippines.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8a85d826a1",
  "kind": "yes/no",
  "text": "Claim: William Novac co-wrote the memoir of Earvin \"Magic\" Johnson Jr., an American retired professional basketball player who is current president of basketball operations for the Los Angeles Lakers.\n\nPassages:\n\n[Magic Johnson]\nEarvin \"Magic\" Johnson Jr. (born August 14, 1959) is an American retired professional basketball player and current president of basketball operations of the Los Angeles Lakers of the National Basketball Association (NBA).\n\n[William Novak]\nWilliam Novak (born 1948) is an author who has co-written or ghostwritten numerous celebrity memoirs for people including Lee Iacocca, Nancy Reagan, and Magic Johnson.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qab8aa18c47",
  "kind": "yes/no",
  "text": "Claim: The infantry regiment featured in the 2006 film directed by an entertainment professional began in 1944. This director was a participant in the Kearny Street Workshop.\n\nPassages:\n\n[442nd Infantry Regiment (United States)]\nBeginning in 1944, the regiment fought primarily in Europe during World War II, in particular Italy, southern France, and Germany.\n\n[Lane Nishikawa]\nIn 2005 he directed the independent feature film, \"Only the Brave\", a fictional account of the rescue of the Lost Battalion by the 100th Infantry Battalion/442nd Regimental Combat Team, a segregated Japanese American fighting unit during World War II.\n\n[Kearny Street Workshop]\nNotable participants include author and Asian American studies scholar Russell Leong, playwright and author Jessica Hagedorn, author Janice Mirikitani, poet and historian Al Robles, and actor and filmmaker Lane Nishikawa.\n\n[Only the Brave (2006 film)]\nOnly the Brave is a 2006 independent film about the 100th Infantry Battalion/442nd Regimental Combat Team, a segregated World War II fighting unit primarily made up of \"Nisei\" Japanese Americans, which for its size and length of service became the most decorated unit in U.S. military history.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbf1aa238ef",
  "kind": "yes/no",
  "text": "Claim: Laurence S. Baskin is the chief of pediatric urology at a university hospital in New Hampsire. This hospital was founded after the academic institution where Greg Huntington played college football.\n\nPassages:\n\n[Greg Huntington]\nHe played college football at Penn State University and was drafted in the fifth round of the 1993 NFL Draft.\n\n[University of California, San Francisco]\nThe University of California, San Francisco (UCSF), is a research university located in San Francisco, California and part of the University of California system. It was founded as Toland Medical College in 1864, and in 1873 it became affiliated with the University of California.\n\n[Laurence S. Baskin]\nLaurence S. Baskin is a professor of pediatrics and chief of pediatric urology at University of California, San Francisco (UCSF).\n\n[Pennsylvania State University]\nThe Pennsylvania State University (commonly referred to as Penn State or PSU) is a state-related, land-grant, doctoral university with campuses and facilities throughout Pennsylvania. Founded in 1855, the university has a stated threefold mission of teaching, research, and public service.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qacf48950f8",
  "kind": "yes/no",
  "text": "Claim: Harry Ransom served as the Chancellor of this institute from 1961 to 1971. This institute and the place where Steven J. Kachelmeier got his Ph.D. combine to have both a 2000 acre campus and over 216,000 students.\n\nPassages:\n\n[Steven J. Kachelmeier]\nDr. Kachelmeier received his B.B.A. from the University of New Mexico and his Ph.D. from the University of Florida.\n\n[University of Texas System]\nThe UT System is headquartered in Austin, and has a total enrollment of over 216,000 students (largest university system in Texas) and employs more than 87,000 faculty and staff.\n\n[Harry Ransom]\nHarry Huntt Ransom (November 22, 1908 – April 19, 1976) was a faculty member and administrator at the University of Texas, becoming the university's president in 1960, and ultimately served as the Chancellor of the University of Texas System from 1961 to 1971.\n\n[University of Florida]\nThe University of Florida (commonly referred to as Florida or UF) is an American public land-grant, sea-grant, and space-grant research university on a 2000 acre campus in Gainesville, Florida.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5fde72d6f7",
  "kind": "yes/no",
  "text": "Text: Out for brunch with my number 1 favourite @shaketheglitterrrr! Going all in with sourdough waffle and homemade bacon for hangover times. Nice to see head chef @paddy_chef getting to have Sunday morning off too! Lovely garden spot too @miss_amy_corbin! https://t.co/1zFFFXpIsV https://t.co/56nnUoIHXH",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf37b8d6159",
  "kind": "yes/no",
  "text": "Claim: Archean Soundtrack are best known for their single \"Reach\", the music video of which was directed by Duncan Guymer, who oversaw the viral marketing videos for a new ride in Crystal Beach. There are eight steel roller coasters of the same type as the new ride in Crystal Beach that are currently operating worldwide.\n\nPassages:\n\n[Archean Soundtrack]\nArchean Soundtrack are best known for their single \"Reach\", the music video of which was directed by Duncan Guymer, who oversaw the viral marketing videos for Thorpe Park's new ride, \"The Swarm\".\n\n[The Swarm (roller coaster)]\nThe Swarm is a steel Wing Coaster at Thorpe Park, a theme park in the United Kingdom.\n\n[Wing Coaster]\nThere are currently eight Wing Coasters operating worldwide.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qb912fa4cc8",
  "kind": "yes/no",
  "text": "Claim: Harmony Is Precious is the literal name for this 2015 Beijing romantic comedy television drama starring Miss Beijing 2004.\n\nPassages:\n\n[Smooth Talker]\nSmooth Talker (; literally \"Harmony Is Precious\") is a 2015 Hong Kong romantic comedy television drama created and produced by TVB, starring Joe Ma and Kate Tsui as the main leads, with Johnson Lee, Elena Kong, Tommy Wong and Tracy Chu in main supporting roles.\n\n[Kate Tsui]\nKate Tsui Tsz-shan () is a Hong Kong actress, who is best known for her work with Television Broadcasts Limited (TVB), and to an extent, for her film work. She also holds the Miss Hong Kong 2004 title.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd310d19102",
  "kind": "yes/no",
  "text": "Claim: Jay Park left the South Korean music group that Lee Jun-ho is a part of, before the release of the group's video called \"Take Off\".\n\nPassages:\n\n[Go Crazy (album)]\nis the fourth Korean studio album (seventh overall) by South Korean boy band 2PM.\n\n[2PM]\nFormer leader Jay Park officially left the group in early 2010.\n\n[Ultra Lover]\nThe single was released along with the group's second live DVD \"1st Japan Tour 2011 \"Take Off\" in Makuhari Messe\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q26120ae9be",
  "kind": "yes/no",
  "text": "Claim: The older sister of Noah Cyrus is a vocalist. The older sister of the vocalist for Love/Hate, who contributed to the album Quiet Riot 10, is also a vocalist.\n\nPassages:\n\n[Trace Cyrus]\nIn 2010, he began providing vocals and guitar in the pop rock band Ashland HIGH.\n\n[Jizzy Pearl]\nJizzy Pearl (born James Wilkinson) is an American vocalist that was born on March 17, 1958, in Chicago, Illinois.\n\n[Quiet Riot 10]\nLove/Hate vocalist Jizzy Pearl joined the band in November 2013 and performs lead vocals on the six studio tracks.\n\n[Noah Cyrus]\nShe is the youngest daughter of Tish Cyrus and Billy Ray Cyrus and the younger sister of Miley Cyrus and Trace Cyrus.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3cf78c4f89",
  "kind": "yes/no",
  "text": "Claim: iTunes lead vocalist co-wrote \"Rise Today\". Alter Bridge and the artists whose debut album was \"Life Left to Go\" are both associated with rock bands.\n\nPassages:\n\n[Myles Kennedy]\nMyles Richard Kennedy (born Myles Richard Bass; November 27, 1969) is an American musician, singer, and songwriter, best known as the lead vocalist and rhythm guitarist of the rock band Alter Bridge, and as the lead vocalist in guitarist Slash's backing band, known as Myles Kennedy and the Conspirators.\n\n[Life Left to Go]\nLife Left to Go is the debut studio album by American rock band SafetySuit, released on May 13, 2008, through Universal Motown Records.\n\n[Rise Today]\nWritten by lead guitarist Mark Tremonti and lead vocalist Myles Kennedy, it was produced by Michael \"Elvis\" Baskette and featured on the band's 2007 second studio album \"Blackbird\".\n\n[SafetySuit]\nSafetySuit is an American pop rock and alternative rock band from Tulsa, Oklahoma, currently based in Nashville, Tennessee.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5bc7025661",
  "kind": "yes/no",
  "text": "Claim: The American author of Done in the Open lived longer than American author Lucy Maud Montgomery.\n\nPassages:\n\n[Lucy Maud Montgomery]\nLucy Maud Montgomery {'1': \", '2': \", '3': \", '4': \"} (November 30, 1874 – April 24, 1942) published as L.M. Montgomery, was a Canadian author best known for a series of novels beginning in 1908 with \"Anne of Green Gables\".\n\n[Done in the Open]\nDone in the Open was a verse collection published by in 1903 American author Owen Wister.\n\n[Owen Wister]\nOwen Wister (July 14, 1860 – July 21, 1938) was an American writer, historian and \"father\" of western fiction.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q5116e1d13c",
  "kind": "yes/no",
  "text": "Claim: The publication from George Vradenburg and Moment are both a type of magazine.\n\nPassages:\n\n[George Vradenburg]\nHe is co-founder and chairman of USAgainstAlzheimer's (USA2), an Alzheimer's advocacy organization., and co-publisher of \"Tikkun\", an English-language magazine with a progressive viewpoint.\n\n[Moment (magazine)]\nMoment is an independent magazine for a Jewish-American audience and is not tied to any movement or ideology.\n\n[Tikkun (magazine)]\nTikkun is a quarterly interfaith Jewish left-progressive magazine, published in the United States, that analyzes American and Israeli culture, politics, religion, and history in the English language.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1eb826ebed",
  "kind": "yes/no",
  "text": "Claim: Snow White is a Disney media franchise based on a German fairy tale by Brothers Grimm.\n\nPassages:\n\n[Snow White (franchise)]\nSnow White is a Disney media franchise that began in 1937 with the theatrical release of \"Snow White and the Seven Dwarfs\".\n\n[Snow White and the Seven Dwarfs (1937 film)]\nBased on the German fairy tale by the Brothers Grimm, it is the first full-length cel animated feature film and the earliest Disney animated feature film.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q91e59b3f10",
  "kind": "yes/no",
  "text": "Claim: Sabina Cvilak sang this in Ryde on the centenary of the composer's birth. That composer and Béla Bartók are not from the same country.\n\nPassages:\n\n[Béla Bartók]\nBéla Viktor János Bartók ( ; ] ; 25 March 1881 – 26 September 1945) was a Hungarian composer, pianist and an ethnomusicologist.\n\n[War Requiem]\nThe War Requiem, Op.\n\n[Sabina Cvilak]\nShe is also known for singing concerts and recitals, such as Britten's \"War Requiem\" in London on the centenary of the composer's birth.\n\n[Benjamin Britten]\nEdward Benjamin Britten, Baron Britten {'1': \", '2': \", '3': \", '4': \"} (22 November 1913 – 4 December 1976) was an English composer, conductor and pianist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q385b4b458b",
  "kind": "yes/no",
  "text": "Tweet: Baffles me as to why ANY retailers still use Hermes as their chosen courier 😑",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q93c490e106",
  "kind": "yes/no",
  "text": "Claim: The Schweizerischer Niederlaufhund and the Portuguese Podengo dog breeds are both dog breeds from Portugal.\n\nPassages:\n\n[Schweizerischer Niederlaufhund]\nThe Schweizerischer Niederlaufhund (FCI No, 60) (translated into English as the Small Swiss Hound, is a breed of dog of the scenthound type from Switzerland.\n\n[Portuguese Podengo]\nThe Portuguese Podengo is an ancient multi-sensory hound (sight and scent) breed of dog from Portugal.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1033c398d4",
  "kind": "yes/no",
  "text": "Claim: The author of The Moons of Jupiter is a writer and editor. So is the author of The Little Foxes play.\n\nPassages:\n\n[The Moons of Jupiter]\nThe Moons of Jupiter is a book of short stories by Alice Munro, published by Macmillan of Canada in 1982.\n\n[Alice Munro]\nAlice Ann Munro ( , \"née\" Laidlaw ; born 10 July 1931) is a Canadian short story writer and Nobel Prize winner.\n\n[Lillian Hellman]\nLillian Florence Hellman (June 20, 1905 – June 30, 1984) was an American dramatist and screenwriter known for her success as a playwright on Broadway, as well as her left-wing sympathies and political activism.\n\n[The Little Foxes]\nThe Little Foxes is a 1939 play by Lillian Hellman, considered a classic of 20th century drama.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q13058274af",
  "kind": "yes/no",
  "text": "Claim: A reggae artist is a believer in Rastafari, a religion that was developed in Liberia. A Time & Place is the second studio album by this artist.\n\nPassages:\n\n[Rastafari]\nClassified as a new religious movement, it developed in Jamaica during the 1930s.\n\n[Julian Marley]\nHe follows into his father’s footsteps and is a devout Rastafarian who uses his music to inspire his life and spirituality.\n\n[A Time &amp; Place]\nA Time & Place is the second studio album by reggae artist Julian Marley, released in 2003 on Lightyear Entertainment.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6d84d31886",
  "kind": "yes/no",
  "text": "Claim: A helicopter is a type of aircraft that can be used in congested or isolated areas. A helicopter is used at the same location of The Canadian Museum of Flight, established in 1955.\n\nPassages:\n\n[Helicopter]\nThese attributes allow helicopters to be used in congested or isolated areas where fixed-wing aircraft and many forms of VTOL (vertical takeoff and landing) aircraft cannot perform.\n\n[Canadian Museum of Flight]\nThe Canadian Museum of Flight (formally the Canadian Museum of Flight Association since 1998) is an aviation museum at the Langley Regional Airport in Langley, British Columbia, Canada.\n\n[Langley Regional Airport]\nHelicopter operations are a major part of Langley Airport's traffic; the airport has 3 helipads.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q49e4bba6c1",
  "kind": "yes/no",
  "text": "Claim: The Nirvana album that their song Sliver was rereleased on featured many artists. The list of artists includes The Vaselines, John Cleese's, and Chad Channing.\n\nPassages:\n\n[Incesticide]\nIncesticide is a compilation album by the American grunge band Nirvana. At the time, the majority of the material on \"Incesticide\" was circulating within fan communities (albeit in lower quality). Since the songs were recorded in different sessions and some were recorded when Nirvana did not have a stable formation, the album includes recordings by four different drummers: Chad Channing, Dan Peters, Dale Crover, and Dave Grohl.\n\n[Sliver (song)]\nDGC re-released the song to radio to support the release of the rarities compilation album \"Incesticide\" in 1992.\n\n[Son of a Gun (EP)]\nSon of A Gun is the debut extended play single by Glasgow alternative rock group The Vaselines. The title-song of this EP came to a wider audience after Nirvana covered it, along with \"Molly's Lips\", on their compilation album \"Incesticide\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfaf8610927",
  "kind": "yes/no",
  "text": "Claim: The singer of \"Eyes Without a Face\" released \"Rebel Yell\" in 1983. He is older than the saxophonist that released the CD \"Live and Acoustic\"\n\nPassages:\n\n[Eyes Without a Face (song)]\n\"Eyes Without a Face\" is a song by English rock musician Billy Idol, from his second album \"Rebel Yell\" (1983).\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.\n\n[Live and Acoustic (Ray Wilson album)]\nLive and Acoustic is the first live CD release from Ray Wilson.\n\n[Ray Wilson (musician)]\nRaymond Wilson (born 8 September 1968) is a Scottish musician, best known as vocalist in the post-grunge band Stiltskin, and in Genesis from 1996 to 1998.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7302320c45",
  "kind": "yes/no",
  "text": "Claim: Henry Gabriel Cisneros followed Texas Revolutionary figure, Juan Nepomuceno Seguín, as a Latino mayer of a major American city.\n\nPassages:\n\n[Juan Seguín]\nJuan Nepomuceno Seguín (October 27, 1806 – August 27, 1890) was a political and military figure of the Texas Revolution helping to establish the independence of Texas.\n\n[Henry Cisneros]\nHe served as the mayor of San Antonio, Texas, from 1981 to 1989, the second Latino mayor of a major American city and the city's first since 1842 (when Juan Seguín was forced out of office).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q755a02e4fe",
  "kind": "yes/no",
  "text": "Claim: The Talbot-Taylor Wildlife Sanctuary is located in a town with a high school. This high school had Elias \"Coach\" Korcoulis as track coach.\n\nPassages:\n\n[Hollis/Brookline High School]\nHollis/Brookline High School is a public school located in Hollis, New Hampshire, serving the towns of Hollis and Brookline.\n\n[Elias &quot;Coach&quot; Korcoulis]\nElias Korcoulis, known to his friends as Lou and to thousands others as Coach (1940 – March 4, 2006) was the cross-country and track coach for Hollis/Brookline High School in Hollis, New Hampshire from 1962 until his death.\n\n[Brookline, New Hampshire]\nBrookline is a town in Hillsborough County, New Hampshire, United States. Brookline is home to the Talbot-Taylor Wildlife Sanctuary, Potanipo Pond, and the Brookline Covered Bridge.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2c5dc0b7f7",
  "kind": "yes/no",
  "text": "Claim: Rihanna is a recording artist who has worked on songs with both Jamal Jones and Skylar Grey.\n\nPassages:\n\n[Fading (song)]\n\"Fading\" is a song by Barbadian recording artist Rihanna from her fifth studio album, \"Loud\" (2010). The song was written by Jamal Jones and Ester Dean, whilst production of the song was completed by Jones under his production name, Polow da Don.\n\n[Take a Bow (Rihanna song)]\n\"Take a Bow\" is a song recorded by Barbadian singer Rihanna for \"\" (2008), the re-release of her third studio album \"Good Girl Gone Bad\" (2007). The song was written and produced by Tor Erik Hermansen, Mikkel Eriksen, and Shaffer Smith under their stage names StarGate and Ne-Yo.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q467c008dbc",
  "kind": "yes/no",
  "text": "Claim: The movie. in which David Zayas acted in, is the movie that John Gavin Malkovich had played in with Matt Damon and Edward Norton.\n\nPassages:\n\n[David Zayas]\nHe is best known for his roles as Angel Batista on Showtime's series \"Dexter\", Osborne the cop in \"Rounders\" (1998), Enrique Morales on the HBO prison drama series \"Oz\", Lou the bodega owner in \"Annie\" (2014) and Sal Maroni on Fox's series \"Gotham\".\n\n[John Malkovich]\nHe has also appeared in films such as \"Empire of the Sun\", \"The Killing Fields\", \"Con Air\", \"Of Mice and Men\", \"Rounders\", \"Ripley's Game\", \"Knockaround Guys\", \"Being John Malkovich\", \"Shadow of the Vampire\", \"Burn After Reading\", \"RED\", \"Mulholland Falls\", \"Dangerous Liaisons\", and \"Warm Bodies\", as well as producing films such as \"Ghost World\", \"Juno\", and \"The Perks of Being a Wallflower\".\n\n[Rounders (film)]\nRounders is a 1998 American drama film about the underground world of high-stakes poker, directed by John Dahl, and starring Matt Damon and Edward Norton.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9793cc5afa",
  "kind": "yes/no",
  "text": "Claim: A singer has released more solo albums than the singer who Avril Lavigne featured on the song Get Over Me with. This singer co-wrote \"What Were You Thinkin'\"\n\nPassages:\n\n[Get Over Me]\n\"Get Over Me\" is a song by American singer and songwriter Nick Carter featuring Canadian singer Avril Lavigne.\n\n[What Were You Thinkin']\nThe song was written by Porter Howell, Dwayne O'Brien, Brady Seals and Christy DiNapoli.\n\n[Nick Carter (musician)]\nNickolas Gene \"Nick\" Carter (born January 28, 1980) is an American singer, songwriter, actor, and dancer. As of 2015, Carter has released three solo albums, \"Now or Never\", \"I'm Taking Off\" and \"All American\" during breaks between Backstreet Boys schedules, and a collaboration with Jordan Knight titled \"Nick & Knight\".\n\n[Brady Seals]\nBrady Seals (born March 29, 1969) is an American country music artist. A fourth solo album, \"Play Time\", was released in 2009 via Star City.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q93e682102a",
  "kind": "yes/no",
  "text": "Claim: The tour that Lungs Tour supported U2 in was a worldwide tour that had a round stage and had a song that had never before been performed live.\n\nPassages:\n\n[U2 360° Tour]\nThe U2 360° Tour was a worldwide concert tour by rock band U2. The concerts featured the band playing \"in the round\" on a circular stage, allowing the audience to surround them on all sides.\n\n[Lungs Tour]\nThey also supported U2 on their U2 360° Tour in 2011.\n\n[Electrical Storm (song)]\nU2 did not play the song live until 2 July 2009, when they performed it on the second concert of their U2 360° Tour in Barcelona.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7ae492b97d",
  "kind": "yes/no",
  "text": "Claim: The artist who recorded Three Cord Opera has had 38 songs in the \"Billboard\" Adult Contemporary Top 10 between 1912 and 1946.\n\nPassages:\n\n[Three Chord Opera]\nThree Chord Opera is the twenty-fifth studio album by Neil Diamond.\n\n[Neil Diamond]\nWith 38 songs in the Top 10, he is the second most successful artist in the history of the \"Billboard\" Adult Contemporary Top 10 charts.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3b847ab61d",
  "kind": "yes/no",
  "text": "Claim: The concert along with Tristan that Set Svanholm lead is a performance of music. A Mozart's opera that Lorenzo Quaglio designed the first production of is also a performance of music.\n\nPassages:\n\n[Idomeneo]\nIdomeneo, re di Creta ossia Ilia e Idamante (Italian for \"Idomeneus, King of Crete, or, Ilia and Idamante\"; usually referred to simply as Idomeneo, K. 366) is an Italian language opera seria by Wolfgang Amadeus Mozart.\n\n[Set Svanholm]\nSet Svanholm (2 September 19044 October 1964) was a Swedish operatic tenor, considered the leading Tristan and Siegfried of the first decade following World War II.\n\n[Lorenzo Quaglio]\nHe worked mainly in Mannheim and in Munich, where he designed the first production of Mozart's opera \"Idomeneo\".\n\n[Siegfried (opera)]\nSiegfried, WWV 86C, is the third of the four music dramas that constitute \"Der Ring des Nibelungen\" (\"The Ring of the Nibelung\"), by Richard Wagner.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd91d3a9569",
  "kind": "yes/no",
  "text": "Post: quit a high paying job for a blind fantasy with no family, no friends, no backup plan… deserved every tear streaming down his face https://t.co/y7KxPh3hwx",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q7c162e51c6",
  "kind": "yes/no",
  "text": "Post: Shout out James Boswell  #unibowl",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qc1e8678d4e",
  "kind": "yes/no",
  "text": "Claim: Mike Robbie's father practiced as an American attorney.\n\nPassages:\n\n[Mike Robbie]\nMike Robbie ( Born April 5, 1943 ), is a former General Manager of the Miami Dolphins and the son of the late Joe Robbie, former owner of the team.\n\n[Joe Robbie]\nJoseph \"Joe\" Robbie (July 7, 1916 – January 7, 1990) was an American attorney, politician, and the principle founder of the Miami Dolphins.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q479293fc43",
  "kind": "yes/no",
  "text": "Claim: J. Andrew \"Drew\" Crompton is chief of staff and counsel for Pennsylvania Senate Pro-Tempore Joe Scarnati, he served as deputy campaign manager for policy for Lynn Swann's campaign, in 2006, for Governor of Pennsylvania.\n\nPassages:\n\n[Drew Crompton]\nHe served as deputy campaign manager for policy for Lynn Swann's 2006 campaign for Governor of Pennsylvania.\n\n[Lynn Swann]\nIn 2006, he was the Republican nominee for Governor of Pennsylvania.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qdd9c8e2d3c",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Theyre embarrassed of their uniforms so theyre playing badly",
   "It was the jerseys"
  ]
 },
 {
  "qid": "qa8c083cf87",
  "kind": "yes/no",
  "text": "Tweet: bring back theme songs!!!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0c25910b67",
  "kind": "yes/no",
  "text": "Claim: Candace Flynn was voiced by the actress who achieved instant success on The Suite Life of Zack & Cody.\n\nPassages:\n\n[Candace Flynn]\nCandace Gertrude Flynn is a main character of the Disney Channel animated television series \"Phineas and Ferb\", voiced by Ashley Tisdale and created and designed by Dan Povenmire.\n\n[Ashley Tisdale]\nShe achieved mainstream success as Maddie Fitzpatrick in the Disney Channel series \"The Suite Life of Zack & Cody\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q504f2c1548",
  "kind": "yes/no",
  "text": "Claim: 69 Love Songs are American. The singer who formed a group with Kid Montana is also American.\n\nPassages:\n\n[Kid Montana]\nFollowing this, he was joined by American singer Dudley Kludt (The Magnetic Fields, Flare Acoustic Arts League) for the remainder of the group's lifetime.\n\n[LD Beghtol]\nLD Beghtol (born 1964, Fort Campbell, Kentucky) is an American musician, art director and writer.\n\n[69 Love Songs]\n69 Love Songs is the sixth studio album by American indie pop band The Magnetic Fields, released on September 7, 1999 by Merge Records.\n\n[Flare Acoustic Arts League]\nFlare Acoustic Arts League — a.k.a. Flare (band) — were an experimental pop band formed by guitarist Damian Costilla and singer LD Beghtol in New York in 1996 who made intense, darkly romantic, atmospheric songs deeply influenced by their love of The Smiths, The Magnetic Fields (with whom beghtol sometimes collaborated), Love, various 4AD bands and The Velvet Underground.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc3fcdc4d52",
  "kind": "yes/no",
  "text": "Claim: The score of the Super Bowl that coach Matt Ulrich won with the Colts was 29–17.\n\nPassages:\n\n[Matt Ulrich]\nHe won Super Bowl XLI with the Colts during the 2006 season over the Chicago Bears.\n\n[Super Bowl XLI]\nThe Colts defeated the Bears by the score of 29–17.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7e4c3f3d6c",
  "kind": "yes/no",
  "text": "Post: Sometimes I feel like all this effort is just like sticking diamond encrusted alloys on a knackered Corsa. I mean, shit is what it is at the end of the day.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qdc37a673a8",
  "kind": "yes/no",
  "text": "Claim: The 2006-07 New Orleans/Oklahoma City Hornets season was the team's 5th in the NBA, the favorite Hornets split their games between the New Orleans Arena and the Ford Center, the multi-purpose indoor arena Smoothie King Center, located in the city's Central Business District, in New Orleans, Louisiana.\n\nPassages:\n\n[2006–07 New Orleans/Oklahoma City Hornets season]\nThe Hornets improved by one win, finishing 39-43, but failed to reach the playoffs.\n\n[Smoothie King Center]\nThe Smoothie King Center is a multi-purpose indoor arena in New Orleans, Louisiana.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1cab1c348d",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "a level tudor history can do one",
   "I want my a-level history course to be finished"
  ]
 },
 {
  "qid": "q35a2ecdb47",
  "kind": "yes/no",
  "text": "Claim: Sang-Wook Cheong works as a materials scientist at a university in New Jersey.\n\nPassages:\n\n[Rutgers University]\nRutgers, The State University of New Jersey ( ), commonly referred to as Rutgers University, Rutgers, or RU, is an American public research university and the largest institution for higher education in New Jersey.\n\n[Sang-Wook Cheong]\nSang Wook Cheong is a Korean American materials scientist at Rutgers University.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
