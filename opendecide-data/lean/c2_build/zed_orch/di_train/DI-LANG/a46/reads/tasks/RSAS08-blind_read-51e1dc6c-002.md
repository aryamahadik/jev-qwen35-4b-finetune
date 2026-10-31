# A46 replay label-noise blind read RSAS08-blind_read-51e1dc6c-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS08-blind_read-51e1dc6c-002.json

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
  "qid": "q4575dc29ad",
  "kind": "yes/no",
  "text": "Claim: Plans to begin a shutdown procedure of the Bilibino Nuclear Power Plant plant in 2019 have been announced, and it will be replaced by the floating nuclear power station named after a Russian polymath, scientist, and writer, who discovered the atmosphere of the planet Venus.\n\nPassages:\n\n[Bilibino Nuclear Power Plant]\nPlans to begin a shutdown procedure of the plant in 2019 have been announced, and it will be replaced by the floating nuclear power station \"Akademik Lomonosov\".\n\n[Akademik Lomonosov]\nThe ship was named after Academician Mikhail Lomonosov.\n\n[Mikhail Lomonosov]\nMikhail Vasilyevich Lomonosov ( ; Russian: Михаи́л (Михáйло) Васи́льевич Ломоно́сов ; ] ; November 19 [O.S. November 8] 1711 – April 15 [O.S. April 4] 1765 ) was a Russian polymath, scientist and writer, who made important contributions to literature, education, and science. Among his discoveries were the atmosphere of Venus and the Law of Mass Conservation in chemical reactions. His spheres of science were natural science, chemistry, physics, mineralogy, history, art, philology, optical devices and others.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3ab348925d",
  "kind": "yes/no",
  "text": "Claim: Both where Roman Catholic Diocese of Lancaster diocese is centred and Peel Cathedral in France belong to the Catholic religion.\n\nPassages:\n\n[Roman Catholic Diocese of Lancaster]\nThe Roman Catholic Diocese of Lancaster is a Latin Rite Roman Catholic diocese centred on Lancaster Cathedral in the city of Lancaster in Lancashire, England.\n\n[Lancaster Cathedral]\nLancaster Cathedral, also known as The Cathedral Church of St Peter and Saint Peter's Cathedral, is in St Peter's Road, Lancaster, Lancashire, England. It was a Roman Catholic parish church until 1924, when it was elevated to the status of a cathedral.\n\n[Peel Cathedral]\nThe Cathedral Church of Saint German or Peel Cathedral, rebranded as Cathedral Isle of Man is located in Peel, Isle of Man. The cathedral is also one of the parish churches in the parish of the West Coast which includes the town of Peel, and was built in 1879–84.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4791aec0bf",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "\"Biden is a liberal, not a leftist. Liberals are center-right. People who voted for Biden came from everywhere on the political spectrum, including conservatives and independents, so stop trying the blame some imaginary 'hate-filled left.'\"",
   "@JoeTalkShow @EdwardNorton Get ratioed, then tell us more about the \"hate-filled left,\" especially about how the Republicans and independents who voted for Biden are somehow part of that group 🤣"
  ]
 },
 {
  "qid": "q8ec2212786",
  "kind": "yes/no",
  "text": "Claim: The author of Mystery is a novelist. So is the author of The Playmaker.\n\nPassages:\n\n[Mystery (novel)]\nMystery is a 1990 novel by American author Peter Straub, and is the second installment in Straub's loosely connected \"Blue Rose Trilogy\".\n\n[Thomas Keneally]\nThomas Michael Keneally, AO (born 7 October 1935) is a prolific Australian novelist, playwright, and essayist.\n\n[The Playmaker]\nThe Playmaker is a novel based in Australia written by the Australian author Thomas Keneally.\n\n[Peter Straub]\nPeter Francis Straub (born March 2, 1943) is an American novelist and poet.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qef1e2e4983",
  "kind": "yes/no",
  "text": "Claim: A college football game was sponsored by a company based in Memphis. The 2015 Kansas State Wildcats football team was invited to this bowl.\n\nPassages:\n\n[AutoZone]\nThe company is based in Memphis, Tennessee.\n\n[2015 Kansas State Wildcats football team]\nThey were invited to the Liberty Bowl where they lost to Arkansas.\n\n[2016 Liberty Bowl (January)]\nSponsored by automobile parts and accessories store AutoZone, it is officially known as the AutoZone Liberty Bowl.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc278091d33",
  "kind": "yes/no",
  "text": "Claim: Margulis lemma is a differential geometry mathematical subfield. Its founder was born in the 6th century, before one of the minds behind Leftover hash lemma.\n\nPassages:\n\n[Margulis lemma]\nIn differential geometry, a subfield of mathematics, the Margulis lemma (named after Grigory Margulis) is a result about discrete subgroups of isometries of a non-positively curved Riemannian manifolds (e.g. the hyperbolic n-space).\n\n[Leonid Levin]\nLeonid Anatolievich Levin ( ; Russian: Леони́д Анато́льевич Ле́вин ; Ukrainian: Леоні́д Анато́лійович Ле́він ; born November 2, 1948) is a Soviet-American computer scientist.\n\n[Leftover hash lemma]\nThe leftover hash lemma is a lemma in cryptography first stated by Russell Impagliazzo, Leonid Levin, and Michael Luby.\n\n[Grigory Margulis]\nGregori Aleksandrovich Margulis (Russian: Григо́рий Алекса́ндрович Маргу́лис , first name often given as Gregory, Grigori or Grigory; born February 24, 1946) is a Russian-American mathematician known for his work on lattices in Lie groups, and the introduction of methods from ergodic theory into diophantine approximation.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6bde279625",
  "kind": "yes/no",
  "text": "Claim: The director of Border Street was born 3 years before the writer of \"Crane World\". The writer of \"Crane World\" is also the director.\n\nPassages:\n\n[Aleksander Ford]\nAleksander Ford (born Mosze Lifszyc; 24 November 1908 in Kiev, Russian Empire – 4 April 1980 in Naples, Florida, United States) was a Polish Jewish film director; and head of the Polish People's Army Film Crew in the Soviet Union during World War II.\n\n[Border Street]\nBorder Street (Polish:Ulica Graniczna) is a 1948 Polish drama film directed by Aleksander Ford and starring Mieczysława Ćwiklińska, Jerzy Leszczyński and Władysław Godik.\n\n[Crane World]\nCrane World (Spanish: Mundo grúa ) is an 1999 Argentine film, written and directed by Pablo Trapero.\n\n[Pablo Trapero]\nPablo Trapero (Born 4 October 1971) is an Argentine film producer, editor and director.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q810e82c1ba",
  "kind": "yes/no",
  "text": "Claim: \"wild combination\" was a film about the man who played cello in the acoustic version of Psycho Killer who was an American cellist, composer, producer and singer.\n\nPassages:\n\n[Psycho Killer]\nIn the liner notes for \"\" (1992), Jerry Harrison wrote of the b-side of the single, an acoustic version of the song that featured Arthur Russell on cello, \"I'm glad we persuaded Tony [Bongiovi] and Lance [Quinn] that the version with the cellos shouldn't be the only one.\"\n\n[Arthur Russell (musician)]\nArthur Russell (born Charles Arthur Russell, Jr.; May 21, 1951 – April 4, 1992) was an American cellist, composer, producer, singer, and musician whose work spanned a disparate range of styles.\n\n[Hecuba (band)]\nThey performed at the Los Angeles premier of \"Wild Combination\": a film about Arthur Russell (musician) performing their versions of Russell's music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q66b41db674",
  "kind": "yes/no",
  "text": "Claim: Henry Gabriel Cisneros followed Texas Revolutionary figure, Juan Nepomuceno Seguín, as a Latino mayer of a Houston.\n\nPassages:\n\n[Juan Seguín]\nJuan Nepomuceno Seguín (October 27, 1806 – August 27, 1890) was a political and military figure of the Texas Revolution helping to establish the independence of Texas.\n\n[Henry Cisneros]\nHe served as the mayor of San Antonio, Texas, from 1981 to 1989, the second Latino mayor of a major American city and the city's first since 1842 (when Juan Seguín was forced out of office).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2b5d7193ef",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "only have to physically be in uni for an hour a week looool mmmm take my 9k xxxxx",
   "9k is ridiculous for 1 hour of in person teaching a week."
  ]
 },
 {
  "qid": "q69d23f5cdc",
  "kind": "yes/no",
  "text": "Claim: The friend of Russians Jean Follain and Connie May Fowler were not both memoirists.\n\nPassages:\n\n[Max Jacob]\nMax Jacob (] ; 12 July 1876 – 5 March 1944) was a French poet, painter, writer, and critic.\n\n[Jean Follain]\nFollain was a friend of Max Jacob, André Salmon, Jean Paulhan, Pierre Pussy, Armen Lubin, and Pierre Reverdy.\n\n[Connie May Fowler]\nConnie May Fowler (born January 3, 1960 to parents of multi-cultural backgrounds) is an American novelist, essayist, memoirist, screenwriter, and poet.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4c1f189054",
  "kind": "yes/no",
  "text": "Claim: The series containing \"Moe Goes from Rags to Riches\" as the third episode of its twenty-third season, released an episode that aired on February 19, 2012 entitled \"At Long Last Leave\", representing the show's 500th episode milestone.\n\nPassages:\n\n[The Simpsons (season 23)]\n\"The Simpsons\"' twenty-third season began airing on Fox on September 25, 2011, and ended May 20, 2012. The show's 500th episode, \"At Long Last Leave\", aired February 19, 2012.\n\n[Moe Goes from Rags to Riches]\n\"Moe Goes from Rags to Riches\" is the twelfth episode of the twenty-third season of the American animated sitcom \"The Simpsons\".\n\n[At Long Last Leave]\n\"At Long Last Leave\" is the fourteenth episode of \"The Simpsons\"' twenty-third season, and the 500th episode overall of the series.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2aa85f3cc2",
  "kind": "yes/no",
  "text": "Claim: This non-fiction author wrote Chilly Scenes of Winter. The author and Edgar Rice Burroughs are not dating.\n\nPassages:\n\n[Chilly Scenes of Winter]\nChilly Scenes of Winter is Ann Beattie's first novel, published by Doubleday in September, 1976.\n\n[Edgar Rice Burroughs]\nEdgar Rice Burroughs (September 1, 1875 – March 19, 1950) was an American fiction writer best known for his celebrated and prolific output in the adventure and science-fiction genres.\n\n[Ann Beattie]\nAnn Beattie (born September 8, 1947) is an American novelist and short story writer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0c97e3e7a8",
  "kind": "yes/no",
  "text": "Claim: The Israeli local protests took place after the resignation of the seventh president of Israel in 2000.\n\nPassages:\n\n[Israeli presidential election, 2000]\nElections for the President of Israel were held in the Knesset on 31 July 2000, following Ezer Weizman's resignation.\n\n[Ezer Weizman]\nEzer Weizman (Hebrew: עזר ויצמן‎ ‎ \"Ezer Vaytsman\"; 15 June 1924 – 24 April 2005) was the seventh President of Israel, first elected in 1993 and re-elected in 1998.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa549bc0830",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I don't think K&G owes me therapy.",
   "I recovered a repressed memory today of working at @kumandgo in high school 13 years ago &amp; having to answer the phone as “we go all out at Kum &amp; Go, this is Shelby. How can I help you?” And the prank calls that led to. Pretty sure K&amp;G owe me therapy."
  ]
 },
 {
  "qid": "q37570239d4",
  "kind": "yes/no",
  "text": "Post: Does anyone not know Prince Harry got engaged? I don’t think there’s been enough in the news about it.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q012f5e35d1",
  "kind": "yes/no",
  "text": "Claim: The car that competed in the Australian Nations Cup Championship was replaced by the sports car that debuted at the event 2004 Paris Motor Show.\n\nPassages:\n\n[Ferrari 360]\nIt succeeded the Ferrari F355 and was replaced by the Ferrari F430.\n\n[Ferrari F430]\nA successor to the Ferrari 360, it debuted at the 2004 Paris Motor Show.\n\n[Australian Nations Cup Championship]\nFor 2000, PROCAR split the Australian GT Production Car Championship into two separate series so that the more exotic GT cars such as Porsche 911s, Ferrari 360s and Lamborghini Diablo's could compete in the new Australian Nations Cup Championship and the lesser vehicles such as the Mitsubishi Lancers, Subaru Imprezas and HSV's could now compete for outright wins in the revised Australian GT Production Car Championship.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q54af41adf5",
  "kind": "yes/no",
  "text": "Claim: The thirteenth season of Gilmore Girls featured an actress as a maid of honor who had also played the role of Winnie Foster.\n\nPassages:\n\n[Alexis Bledel]\nKimberly Alexis Bledel ( ; ] ; born September 16, 1981) is an American actress and model. Bledel made her feature film debut as Winnie Foster in \"Tuck Everlasting\" (2002), and has since appeared in \"Sin City\" (2005), \"Post Grad\" (2009), and as Lena Kaligaris in \"The Sisterhood of the Traveling Pants\" film series.\n\n[Wedding Bell Blues (Gilmore Girls)]\n\"Wedding Bell Blues\" is the thirteenth episode of the fifth season of the American comedy-drama series \"Gilmore Girls\" and the show's 100th episode overall. Their daughter Lorelai Gilmore (Lauren Graham) and their granddaughter Rory Gilmore (Alexis Bledel) serve as maid of honor and best man, respectively.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q27f0e540ef",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Good news: Played out of my mind from the sand traps today. Bad news: Was in the sand traps a lot today.",
   "I was in the sand traps a lot today."
  ]
 },
 {
  "qid": "q4e4cd5e191",
  "kind": "yes/no",
  "text": "Claim: David Michelinie and Bob Layton wrote comic book Doomquest which establishes Doctor Doom as a member of their rogues gallery.\n\nPassages:\n\n[Doctor Doom]\nThe son of Romani witch Cynthia Von Doom, Doctor Doom traditionally has been the archenemy of the Fantastic Four, and the leader of the fictional nation of Latveria.\n\n[Doomquest]\n\"Doomquest\" is a two-issue Iron Man story arc written by David Michelinie and Bob Layton with art by John Romita Jr. and published by Marvel Comics. One of the most popular stories of the title character, it establishes Doctor Doom as a member of his rogues gallery, a villainous counterpart who mirrors the superhero with his wealth, power armor and engineering skill.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8dd0821ad7",
  "kind": "yes/no",
  "text": "Claim: LKBR is the four-letter code published in the International Civil Aviation Organization for Broumov Airport.\n\nPassages:\n\n[Broumov Airport]\nBroumov Airport (ICAO airport code LKBR) is an airport in Broumov in the Czech Republic.\n\n[ICAO airport code]\nThe ICAO ( , ) airport code or location indicator is a four-letter code designating aerodromes around the world. These codes are defined by the International Civil Aviation Organization, and published in ICAO Document 7910: \"Location Indicators\" are used by air traffic control and airline operations such as flight planning.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q80f63410af",
  "kind": "yes/no",
  "text": "Claim: The song that John Kirby scored that is often the final piece of music played during an evening of revelry is \"Loch Lomond\".\n\nPassages:\n\n[The Bonnie Banks o' Loch Lomond]\nIn Scotland, the song is often the final piece of music played during an evening of revelry (a dance party or dinner, etc.).\n\n[John Kirby (musician)]\nIn addition to sideman work (prominently with Benny Goodman), Kirby is remembered for leading a successful chamber jazz sextet in the late 1930s and early 1940s, which scored several hit songs including \"Loch Lomond\" and the debut recording of \"Undecided\", a jazz standard.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q944b1e963f",
  "kind": "yes/no",
  "text": "Claim: Imagine Dragons recorded the 2005 EP which features the song \"Hear Me\" at a studio. This recording studio is located in the unincorporated town that is part of Clark County.\n\nPassages:\n\n[Hear Me (song)]\n\"Hear Me\" is a song by American rock band Imagine Dragons, originally written and recorded for their second extended play, \"Hell and Silence\".\n\n[Winchester, Nevada]\nWinchester is an unincorporated town and census-designated place (CDP) and part of Las Vegas Township in Clark County, Nevada, United States that contains part of the Las Vegas Strip.\n\n[Hell and Silence]\nIt was recorded at Battle Born Studios.\n\n[Battle Born Studios]\nBattle Born Studios, located in the Winchester, Nevada, is a 2000 sqft recording studio owned by The Killers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf70c5f60fc",
  "kind": "yes/no",
  "text": "Claim: Italian football forward Andrea Locatelli currently plays for the Italian football club founded in 1905.\n\nPassages:\n\n[Andrea Locatelli (footballer)]\nAndrea Locatelli (born 23 September 1989) is a Swiss football forward who currently plays for FC Chiasso.\n\n[FC Chiasso]\nFC Chiasso is a Swiss football club based in Chiasso. It was founded in 1905.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q88a0eb96c0",
  "kind": "yes/no",
  "text": "Claim: Henry C. McRae served for one season as the head football coach of a college that declines to accept federal financial support on the grounds of it's anti-abortion stance.\n\nPassages:\n\n[Hillsdale College]\nHillsdale College is a co-educational, non-profit liberal arts college in Hillsdale, Michigan, United States. The college declines to accept federal financial support, instead providing private financial assistance to its students.\n\n[Harry McRae]\nHenry C. McRae was an American football coach. He served as the head football coach at Hillsdale College in Hillsdale, Michigan for one season in 1904, compiling a record of 0–7.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q55a94abc06",
  "kind": "yes/no",
  "text": "Claim: The murderer, by whom the character Keyser Soze was inspired, committed his murders in Westfield, New Jersey between 1972 and 1981.\n\nPassages:\n\n[Keyser Söze]\nThe character was inspired by real life murderer John List and the spy thriller \"No Way Out\", which featured a shadowy KGB mole.\n\n[John List]\nOn November 9, 1971, he killed his wife, mother, and three children in their home in Westfield, New Jersey, then disappeared.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q107b65cc63",
  "kind": "yes/no",
  "text": "Claim: Produce 101, which produced I.O.I, cost the company Mnet about four billion won to produce.\n\nPassages:\n\n[Produce 101]\nThe show has the second-largest budget of all shows produced by Mnet at about four billion won (approximately $3.4 million).\n\n[I.O.I]\nI.O.I (; also known as IOI or Ideal of Idol) was a South Korean girl group formed by CJ E&M through the 2016 reality show \"Produce 101\" on Mnet.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb3bcdcb5e4",
  "kind": "yes/no",
  "text": "Claim: Titus is the soundtrack to the horror film that starred actors, Anthony Hopkins and Jessica Lange.\n\nPassages:\n\n[Titus (film)]\nStarring Anthony Hopkins and Jessica Lange, it was the first theatrically-released feature film adaptation of the play.\n\n[Titus (soundtrack)]\nTitus is the original soundtrack to the 1999 motion picture \"Titus\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qffb2de732f",
  "kind": "yes/no",
  "text": "Claim: Wolf Parade is a Canadian rock band and not Social Distortion.\n\nPassages:\n\n[Social Distortion]\nSocial Distortion is an American punk rock band formed in 1978 in Fullerton, California.\n\n[Wolf Parade]\nWolf Parade is an indie rock band formed in 2003 in Montreal, Quebec of musicians from British Columbia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6ce7d7d981",
  "kind": "yes/no",
  "text": "Claim: Wichita City Carnegie Library Building is centrally located in the most populous city in Kansas was built in 1915, and listed on the National Register of Historic Places in 1987.\n\nPassages:\n\n[Sedgwick County, Kansas]\nThe county seat is Wichita, the most populous city in the state.\n\n[Wichita City Carnegie Library Building]\nThe Wichita City Carnegie Library Building located at 220 S. Main Street in Wichita, Kansas, Sedgwick County, Kansas, United States, is a Carnegie library built in 1915. It was listed on the National Register of Historic Places in 1987.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa574aec753",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Actually considering applying for the undateables",
   "Why is my lovelife so dead?"
  ]
 },
 {
  "qid": "q986e18ce0a",
  "kind": "yes/no",
  "text": "Claim: A gun range was first constructed for an event where 74 records were broken. Tughlaqabad Fort is close to this range.\n\nPassages:\n\n[1982 Asian Games]\nThe 9th Asian Games were held from November 19, 1982, to December 4, 1982, in Delhi, India. 74 Asian and Asian Games records were broken at the event.\n\n[Dr. Karni Singh Shooting Range]\nDr. Karni Singh Shooting Range is a shooting range in New Delhi. It was first constructed for the 1982 Asian Games in New Delhi, and later rebuild altogether for the 2010 Commonwealth Games.\n\n[Tughlaqabad Fort]\nAlso nearby is the Asola Bhatti Wildlife Sanctuary, Dr. Karni Singh Shooting Range and Okhla Industrial Area.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6a10881f32",
  "kind": "yes/no",
  "text": "Claim: 9,212 was the 2010 population of the western US locale KAGB is licensed to.\n\nPassages:\n\n[KAGB]\nKAGB (99.1 FM) is a radio station broadcasting an Adult Contemporary format simulcasting Hilo based KAPA. The station is licensed to Waimea, Hawaii, United States.\n\n[Waimea, Hawaii County, Hawaii]\nWaimea is a census-designated place (CDP) in Hawaiʻ i County, Hawaiʻ i, United States. The population was 7,028 at the 2000 census and 9,212 at the 2010 census.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0afb46446e",
  "kind": "yes/no",
  "text": "Claim: This person is one of the current Course Directors for course on which Kazuo Ishiguro obtained his Poetry and Scriptwriting. The Course Director and Nâzım Hikmet are each a poet and novelist.\n\nPassages:\n\n[UEA Creative Writing Course]\nThe Course Directors are currently Andrew Cowan, Kathryn Hughes, Lavinia Greenlaw and Val Taylor respectively.\n\n[Kazuo Ishiguro]\nIshiguro obtained his bachelor's degree from the University of Kent in 1978 and his Master's from the University of East Anglia's creative writing course in 1980.\n\n[Lavinia Greenlaw]\nLavinia Greenlaw (born 30 July 1962) is an English poet and novelist.\n\n[Nâzım Hikmet]\nNâzım Hikmet Ran (15 January 1902 – 3 June 1963), commonly known as Nâzım Hikmet (] ) was a Turkish poet, playwright, novelist, screenwriter, director and memoirist.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3da97b19f1",
  "kind": "yes/no",
  "text": "Claim: This individual played with Steve Denton in the 1983 Dallas Open – Doubles. He and the defending champion at the 2011 Aegon International - Women's Singles are not from the same country.\n\nPassages:\n\n[2011 Aegon International – Women's Singles]\nEkaterina Makarova was the defending champion, but lost to Petra Kvitová in the second round.\n\n[Ekaterina Makarova]\nEkaterina Valeryevna Makarova (Russian: Екатери́на Вале́рьевна Мака́рова ; ] ; born on 7 June 1988) is a Russian professional tennis player.\n\n[Sherwood Stewart]\nSherwood Stewart (born June 6, 1946, in Goose Creek, Texas, United States) played amateur and professional tennis in the 1970s and 1980s.\n\n[1983 Dallas Open – Doubles]\nNduka Odizor and Van Winitsky won in the final 6–3, 7–5 against Steve Denton and Sherwood Stewart.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q031a871616",
  "kind": "yes/no",
  "text": "Claim: The film, named for the character Beulah Annan inspired, starred the entertainer and comedic actor who had the nickname The King of Chutzpah.\n\nPassages:\n\n[Roxie Hart (film)]\nRoxie Hart, also known as Chicago or Chicago Gal, is a 1942 American comedy film directed by William A. Wellman and starring Ginger Rogers, Adolphe Menjou, George Montgomery, Nigel Bruce, Phil Silvers, William Frawley and Spring Byington.\n\n[Phil Silvers]\nPhil Silvers (May 11, 1911 – November 1, 1985) was an American entertainer and comedic actor, known as \"The King of Chutzpah\".\n\n[Beulah Annan]\nThe play has been adapted into a 1927 silent film, 1975 stage musical, and 2002 movie musical (which won the Academy Award for Best Picture), all with that title, and a 1942 romantic comedy film, \"Roxie Hart\", named for the character Annan inspired.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6980039837",
  "kind": "yes/no",
  "text": "Claim: Nonso Anozie played a character in the 2016 film A Midsummer Night's Dream. That character was also the name of Silvana opera.\n\nPassages:\n\n[A Midsummer Night's Dream (2016 film)]\nIt stars Maxine Peake as Titania, Matt Lucas as Bottom, John Hannah as Theseus and Nonso Anozie as Oberon.\n\n[Christoph Martin Wieland]\nHe is best-remembered for having written the first Bildungsroman (\"Geschichte des Agathon\"), as well as the epic \"Oberon\", which formed the basis for Carl Maria von Weber's opera of the same name.\n\n[Oberon]\nOberon is a king of the fairies in medieval and Renaissance literature.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2e76972d2d",
  "kind": "yes/no",
  "text": "Claim: The Workers' Party dominated the last three mayoral elections of the state in which the place Joílson Rodrigues da Silva was born in, is a municipality.\n\nPassages:\n\n[Bahia]\nOnce a monarchial stronghold dominated by agricultural, slaving, and ranching interests, Bahia is now a major manufacturing center whose last three elections have been dominated by the Workers' Party.\n\n[Arataca]\nArataca is a municipality in the state of Bahia in the North-East region of Brazil.\n\n[Joílson Rodrigues da Silva]\nHe was born in Arataca, near Itabuna.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf1ab0240e0",
  "kind": "yes/no",
  "text": "Claim: In addition to the individual born on August 21, Sharon Sheeley also wrote He's The Great Imposter.\n\nPassages:\n\n[(He's) The Great Imposter]\nThe song was written by Sharon Sheeley and Jackie DeShannon.\n\n[Jackie DeShannon]\nJackie DeShannon (born August 21, 1941/1944) is an American singer-songwriter with a string of hit song credits from the 1960s onwards, as both singer and composer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1a4b6b2edf",
  "kind": "yes/no",
  "text": "Post: it’s always the girls I don’t even know that wanna talk about me 24/7 :) I love my fans :)",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q51848901b5",
  "kind": "yes/no",
  "text": "Claim: The creator of the media franchise in which Malcolm Reynolds is a fictional character and the protagonist, was american. The actor Norman Mailer was also american.\n\nPassages:\n\n[Firefly (franchise)]\nThe \"Firefly\" media franchise is an American space Western media franchise created by Joss Whedon and produced by Mutant Enemy Productions.\n\n[Norman Mailer]\nNorman Kingsley Mailer (January 31, 1923 – November 10, 2007) was an American novelist, journalist, essayist, playwright, film-maker, actor, and political activist.\n\n[Malcolm Reynolds]\nMalcolm \"Mal\" Reynolds is a fictional character and the protagonist of the \"Firefly\" franchise.\n\n[Joss Whedon]\nJoseph Hill Whedon ( ; born June 23, 1964) is an American screenwriter, director, producer, comic book writer, and composer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6da76028f7",
  "kind": "yes/no",
  "text": "Claim: The Huskies football team were invited to the Alamo Bowl where they were defeated by a team coached by Steve Sarkisian and who played their home games at Floyd Casey Stadium.\n\nPassages:\n\n[2011 Baylor Bears football team]\nThe 2011 Baylor Bears football team represented Baylor University in the 2011 NCAA Division I FBS football season. The team was coached by Art Briles and played their home games at Floyd Casey Stadium in Waco, Texas.\n\n[2011 Washington Huskies football team]\nThe 2011 Washington Huskies football team represented the University of Washington in the 2011 NCAA Division I FBS football season. They were invited to the Alamo Bowl where they were defeated by Baylor 56–67.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcd7977b5cb",
  "kind": "yes/no",
  "text": "Text: I love calling my mom early in the morning and waking her up, I take it as pay back for all the times she never let me sleep in 😜",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q12d66b24d8",
  "kind": "yes/no",
  "text": "Claim: The Darjeeling Limited is an American adventure comedy-drama film, released in 2007, directed by Bill Murray, the film stars include Bill Murray in a cameo role.\n\nPassages:\n\n[The Darjeeling Limited]\nThe Darjeeling Limited is a 2007 American adventure comedy-drama film directed by Wes Anderson which he co-produced with Scott Rudin, Roman Coppola and Lydia Dean Pilcher and co-wrote with Coppola and Jason Schwartzman.\n\n[Bill Murray]\nWilliam James Murray (born September 21, 1950) is an American actor, comedian, and writer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0d01edfb5a",
  "kind": "yes/no",
  "text": "Claim: Bowdoin College was established before another university. This university was attended by a musician. This musician founded Kingswood College which operated in Kingswood, Kentucky.\n\nPassages:\n\n[Bowdoin College]\nBowdoin College ( ) is a private liberal arts college located in Brunswick, Maine. At the time Bowdoin was chartered in 1794, Maine was still a part of the Commonwealth of Massachusetts.\n\n[Vanderbilt University]\nFounded in 1873, it was named in honor of shipping and rail magnate Cornelius Vanderbilt, who provided the school its initial $1 million endowment despite having never been to the South.\n\n[John Wesley Hughes]\nHughes attended Kentucky Wesleyan College in Millersburg, Kentucky (now located in Owensboro, Kentucky), and served as a pastor in the Kentucky Conference of the Methodist Church before pursuing further education at Vanderbilt University in Nashville, Tennessee.\n\n[Kingswood, Kentucky]\nKingswood College founded by John Wesley Hughes operated in the community from 1906 to 1934.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q78f37ba2df",
  "kind": "yes/no",
  "text": "Claim: The winner of the FIA World Endurance Championship in 2013 drove the Toyota TF101 with Mika Salo.\n\nPassages:\n\n[Toyota TF101]\nThe car was designed by Toyota F1's chief of chassis Jean-Claude Martens and was driven by Mika Salo and Allan McNish.\n\n[Allan McNish]\nHe won the FIA World Endurance Championship (FIA WEC) in 2013.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2e81bc5f61",
  "kind": "yes/no",
  "text": "Claim: The town that holds the Garth School was originally named Lebanon.\n\nPassages:\n\n[Georgetown, Kentucky]\nIt was originally called Lebanon when founded by Rev. Elijah Craig and was renamed in 1790 in honor of President George Washington.\n\n[Garth School]\nGarth School is an historic school building located on South Broadway Street in Georgetown, Kentucky, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q42e4a9e5b9",
  "kind": "yes/no",
  "text": "Text: Happy happy happy https://t.co/9W1XIbpL6x",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q1282bbf34a",
  "kind": "yes/no",
  "text": "Claim: Chindia is a portmanteau word that refers to China and India together in general, together, they contain over one-third of the total number of humans currently living, and is called world's population.\n\nPassages:\n\n[Chindia]\nTogether, they contain over one-third of the world's population (nearly 2.7 billion).\n\n[World population]\nIn demographics, the world population is the total number of humans currently living.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3969073932",
  "kind": "yes/no",
  "text": "Claim: The founding year of this American for-profit college, which helps to operate a 2 year, dual degree high school located in Chicago, Illinois, with Chicago Public Schools was 1931.\n\nPassages:\n\n[DeVry University]\nDeVry University ( ) is an American for-profit college. The school was founded in 1931 as DeForest Training School, and officially became DeVry University in 2002.\n\n[DeVry Advantage Academy (Illinois)]\nDeVry University Advantage Academy is a 2-year, dual degree high school located in Chicago, Illinois. Operated by partnership with Chicago Public Schools and DeVry University, the program offers students an opportunity to graduate with a high school diploma and an associate degree in either Networking System Administration or Web Graphic Design.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 }
]
