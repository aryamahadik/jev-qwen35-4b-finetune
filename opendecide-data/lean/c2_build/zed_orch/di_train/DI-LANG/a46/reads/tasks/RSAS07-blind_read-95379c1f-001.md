# A46 replay label-noise blind read RSAS07-blind_read-95379c1f-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS07-blind_read-95379c1f-001.json

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
  "qid": "qdb67ef53d0",
  "kind": "yes/no",
  "text": "Claim: E.B. Babcock studies genus's family comes first alphabetically before Isatis.\n\nPassages:\n\n[Crepis]\nCrepis, commonly known in some parts of the world as hawksbeard or hawk's-beard (but not to be confused with the related genus \"Hieracium\" with a similar common name), is a genus of annual and perennial flowering plants of the family Asteraceae superficially resembling the dandelion, the most conspicuous difference being that \"Crepis\" usually has branching scapes with multiple heads (though solitary heads can occur).\n\n[Isatis]\nIsatis is a genus of about 30 species of flowering plants in the family Brassicaceae, native to the Mediterranean region east to central Asia.\n\n[E. B. Babcock]\nHe is particularly known for seeking to understand by field investigations and extensive experiments, the entire polyploid apomictic genus \"Crepis\", in which he recognize 196 species.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5b8e727b7c",
  "kind": "yes/no",
  "text": "Claim: The movie, based on a story written by brothers who are interred at Alter St.-Matthäus-Kirchhof, is loosely based off the Brother Grimm's \"Iron Henry\".\n\nPassages:\n\n[Alter St.-Matthäus-Kirchhof]\nIt is known for its interment of the Brothers Grimm, Jacob and Wilhelm Grimm, folklore tellers of \"Cinderella\" (\"Aschenputtel\"), \"The Frog Prince\" (\"Der Froschkönig\"), \"Hansel and Gretel\" (\"Hänsel und Gretel\"), \"Rapunzel\", \"Rumpelstiltskin\" (\"Rumpelstilzchen\"), and \"Snow White\" (\"Schneewittchen\"); Rudolf Virchow, variously known as \"father of modern pathology\", \"father of modern medicine\" or \"father of social medicine\"; and Claus von Stauffenberg, a German Army officer who almost assassinated Adolf Hitler.\n\n[The Frog Prince]\n\"The Frog Prince; or, Iron Henry\" (German: \"Der Froschkönig oder der eisen Heinrich\" , literally \"The Frog King; or, The Iron Heinrich\") is a fairy tale, best known through the Brothers Grimm's written version; traditionally it is the first story in their collection.\n\n[The Princess and the Frog]\nThe 49th Disney animated feature film, the film is loosely based on the novel \"The Frog Princess\" by E. D. Baker, which is in turn based on the Brothers Grimm fairy tale \"The Frog Prince\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q52069135a4",
  "kind": "yes/no",
  "text": "Claim: Space Ducks features rock songs from the band started by Ruben Nielson, who was formerly of the group The Mint Chicks.\n\nPassages:\n\n[Space Ducks]\nIts also features songs from Unknown Mortal Orchestra, Eleanor Friedberger, Deer Tick, Fruit Bats, and Lavender Diamond.\n\n[Unknown Mortal Orchestra]\nUnknown Mortal Orchestra is an American and New Zealand rock band composed of singer, guitarist and songwriter Ruban Nielson, bassist Jake Portrait, keyboardist Quincy McCrary, and drummer Amber Baker. The band was started by Nielson (formerly of The Mint Chicks).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6f97da5ec7",
  "kind": "yes/no",
  "text": "Claim: Triangle Brewing Company was started by a founder who had experience as a homebrewer.\n\nPassages:\n\n[Homebrewing]\nHomebrewing is the brewing of beer on a small scale for personal, non-commercial purposes.\n\n[Triangle Brewing Company]\nAndy Miller had extensive local restaurant management experience, and Rick Tufts apprenticed at Flying Fish Brewing Company and was an avid homebrewer long before founding a new brewery.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q277bd83d87",
  "kind": "yes/no",
  "text": "Claim: The co-star of the film Death Valley Outlaws stared in a tv series created by John Meston.\n\nPassages:\n\n[Gunsmoke]\nGunsmoke is an American radio and television Western drama series created by director Norman Macdonnell and writer John Meston.\n\n[Milburn Stone]\nHugh Milburn Stone, sometimes known as Milly Stone (July 5, 1904 – June 12, 1980), was an American film and television actor best known as \"Doc\" (Dr. Galen Adams) on the CBS western series \"Gunsmoke\".\n\n[Death Valley Outlaws]\nThe film stars Don \"Red\" Barry, Lynn Merrick, Milburn Stone, Bob McKenzie, Karl Hackett and Rex Lease.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6d595b37d8",
  "kind": "yes/no",
  "text": "Claim: Travis Oates voiced the character that translates to the Finnish 'Sisu Nasu' or funny bear, in the 2011 movie. The Jungle Book was released before this movie.\n\nPassages:\n\n[Travis Oates]\nHe and Jim Cummings were the only two original voice actors to return for the 2011 movie.\n\n[Winnie the Pooh (2011 film)]\nWinnie the Pooh is a 2011 American animated buddy musical comedy film produced by Walt Disney Animation Studios and released by Walt Disney Pictures.\n\n[Sisu Nasu]\nThe Nasu (acronym for \"Nauha-Sisu\" English: Track Sisu , also meaning \"Piglet\" in Finnish) is a tracked articulated, all-terrain transport vehicle developed by Sisu Auto for the Finnish Army.\n\n[The Jungle Book (1994 film)]\nRudyard Kipling's The Jungle Book is a 1994 live-action American adventure film co-written and directed by Stephen Sommers, produced by Edward S. Feldman and Raju Patel, from a story by Ronald Yanover and Mark Geldman.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q699afbe8d2",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "I don't think Republicans have any self awareness or any idea of how the world works... Nice try though.",
   "\"I really think that older Republicans are lacking in self-awareness in the modern-day. They had a complete misstep and just ended up bullying a teenager.\""
  ]
 },
 {
  "qid": "qd6a48b0d92",
  "kind": "yes/no",
  "text": "Claim: Dr. Brewster M. Higley wrote the lyrics to the theme song that was used by a film series of the same genre as Destry. This film series included the movie Rock River Renegades.\n\nPassages:\n\n[Rock River Renegades]\nRock River Renegades is a 1942 American film directed by S. Roy Luby, one of the films in the Range Busters series.\n\n[Destry (film)]\nDestry is a 1954 American Technicolor Western film starring Audie Murphy, Mari Blanchard, Lyle Bettger and Thomas Mitchell.\n\n[Range Busters]\nThe Range Busters was a film series of 24 Westerns of the adventures of a trio of cowboys, many filmed at the Corriganville Movie Ranch, produced by George W. Weeks and distributed by Monogram Pictures. The series used \"Home on the Range\" as its theme song with each film featuring the heroes waving goodbye and promising to return in another adventure.\n\n[Home on the Range]\n\"Home on the Range\" is a classic western folk song sometimes called the \"unofficial anthem\" of the American West. The lyrics were originally written by Dr. Brewster M. Higley of Smith County, Kansas, in a poem entitled \"My Western Home\" in 1872.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc16717dfd1",
  "kind": "yes/no",
  "text": "Claim: The star of the erotic horror film \"Jane the Virgin\" is also known for her role as the character Andrea Fleytas on \"Deepwater Horizon\".\n\nPassages:\n\n[Gina Rodriguez]\nShe also portrayed roles as Majo Tenorio in musical-drama film \"Filly Brown\", as Beverly in the soap opera \"The Bold and the Beautiful\" and as Andrea Fleytas in \"Deepwater Horizon\".\n\n[Jane the Virgin (season 1)]\nThe season consisted of 22 episodes and stars Gina Rodriguez as a young Latina university student accidentally artificially inseminated with her boss, Rafael Solano's (Justin Baldoni) sperm.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q98163bc2ba",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "I am a normal white woman",
   "\"You're not a normal white girl\" lol ok"
  ]
 },
 {
  "qid": "qe950858ebe",
  "kind": "yes/no",
  "text": "Claim: The Seattle Redhawks women's basketball team can be found in Washington.\n\nPassages:\n\n[Seattle University]\nSeattle University (SU) is a Jesuit Catholic university in the northwestern United States, located in the First Hill neighborhood of Seattle, Washington.\n\n[Seattle Redhawks women's basketball]\nThe Seattle Redhawks women's basketball is the women's basketball team representing Seattle University.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfbc97b92df",
  "kind": "yes/no",
  "text": "Claim: Lewis Moran was murdered a week after the death of the Italian hitman from the Australian city of Melbourne.\n\nPassages:\n\n[Andrew Veniamin]\nAndrew \"Benji\" Veniamin (16 November 1975 – 23 March 2004) was an Australian criminal from Melbourne, Victoria, Australia.\n\n[Lewis Moran]\nHis murder occurred one week after the funeral of fellow Melbourne underworld criminal and suspected hitman Andrew Veniamin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe03955cff1",
  "kind": "yes/no",
  "text": "Text: I wish I could watch Disney channel original movies on the old box TVs to get the full effect again",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb8fe50f657",
  "kind": "yes/no",
  "text": "Claim: An American rock band released My Animal. This band has more studio albums than the English band whose second album is Rispah.\n\nPassages:\n\n[The Invisible (band)]\nTheir self-titled debut album, released on 9 March 2009, was nominated for the Mercury Prize and selected as critics choice for iTunes album of the year.\n\n[Rispah]\nRispah is the second album by the English band The Invisible.\n\n[Boy Hits Car]\nBoy Hits Car released their 5th studio album \"All That Led Us Here\" in May 2014 and are following it up with a European tour.\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8ede4df38b",
  "kind": "yes/no",
  "text": "Claim: The man in Mad Men who had Peggy Olson as a secretary, played a role in the comedy series \"30 Rock\" as well as the drama series \"Mad Men\".\n\nPassages:\n\n[Peggy Olson]\nInitially, Peggy is secretary to Don Draper (Jon Hamm), creative director of the advertising agency Sterling Cooper.\n\n[Jon Hamm]\nJonathan Daniel Hamm (born March 10, 1971) is an American actor, director, and television producer best known for playing advertising executive Don Draper for the AMC television drama series, \"Mad Men\" (2007–2015).\n\n[Live Show]\n\"Live Show\" featured appearances by Rachel Dratch, Bill Hader, Matt Damon, Jon Hamm, and Julia Louis-Dreyfus.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q51cbf37dd9",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "I would do so much for people that would do absolutely nothing for me lol at least i know who my true friends are😀",
   "no one does anything for me"
  ]
 },
 {
  "qid": "q253154e98b",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "College advisors are not nearly as helpful as they should be, in fact they are often the opposite.",
   "thinking about quitting the path im on to become a college advisor so i can be wrong and do nothing for the rest of my life"
  ]
 },
 {
  "qid": "qe6fe953f8c",
  "kind": "yes/no",
  "text": "Claim: The BBC drama Silk would be referenced in the biographical television film, Hancock and Joan.\n\nPassages:\n\n[Maxine Peake]\nShe has since played Veronica Ball in Channel 4's Manchester-based comedy drama series \"Shameless\", barrister Martha Costello in the BBC legal drama \"Silk\" and Grace Middleton in \"The Village\".\n\n[Hancock and Joan]\nHancock and Joan is a 2008 British biographical television film based on the affair between the comedian Tony Hancock and Joan Le Mesurier, the third wife of actor John Le Mesurier.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf29c309a7b",
  "kind": "yes/no",
  "text": "Claim: An actor who appeared in The Veteran (2011 film) also starred in a film based on a video game series in 2016 notably set in the world of Azeroth .\n\nPassages:\n\n[Warcraft (film)]\nIt is based on the video game series of the same name and the novels set in the world of Azeroth.\n\n[Toby Kebbell]\nHe is known for his roles in films such as \"Dead Man's Shoes\" (2004), \"RocknRolla\" (2008), \"\" (2010), \"War Horse\" (2011), \"Wrath of the Titans\" (2012), \"Dawn of the Planet of the Apes\" (2014), \"Fantastic Four\" (2015), \"Warcraft\" (2016), \"A Monster Calls\" (2016), and \"Gold\" (2016).\n\n[The Veteran (2011 film)]\nThe Veteran is a 2011 British action film directed by Matthew Hope, featuring Toby Kebbell, Brian Cox, Tony Curran and Adi Bielski.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8ec901ddb2",
  "kind": "yes/no",
  "text": "Claim: Peter Marc Jacobson is not best known as the co-creator of the popular sitcom \"The Nanny\", which he did not create and wrote with his then wife an actress born in 1957.\n\nPassages:\n\n[Peter Marc Jacobson]\nHe is best known as the co-creator of the popular sitcom \"The Nanny\", which he created and wrote with his then wife actress Fran Drescher, who was the star of the series.\n\n[Fran Drescher]\nFrancine Joy \"Fran\" Drescher (born September 30, 1957) is an American actress and activist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q70a40ea3e5",
  "kind": "yes/no",
  "text": "Claim: The head coach of the 1985 Oklahoma Sooners led the Dallas Cowboys to a Super Bowl victory in 1982.\n\nPassages:\n\n[Barry Switzer]\nHe served for 16 years as head football coach at the University of Oklahoma and four years as head coach for the Dallas Cowboys of the National Football League (NFL). He helped the Cowboys win Super Bowl XXX against the Pittsburgh Steelers.\n\n[1985 NCAA Division I-A football season]\nThe 1985 NCAA Division I-A football season saw the Oklahoma Sooners, led by head coach Barry Switzer, win the national championship.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q45101c775c",
  "kind": "yes/no",
  "text": "Claim: The Producers is a 2005 American musical comedy film directed by Will Ferrell. The film stars an ensemble cast, including American comedian, actor and singer, Jon Lovitz, best known as a cast member of \"Saturday Night Live\" from 1985 to 1990.\n\nPassages:\n\n[The Producers (2005 film)]\nThe film stars an ensemble cast led by Nathan Lane, Matthew Broderick, Uma Thurman, Will Ferrell, Gary Beach, Roger Bart, and Jon Lovitz.\n\n[Jon Lovitz]\nJonathan Michael Lovitz (born July 21, 1957) is an American comedian, actor and singer, best known as a cast member of \"Saturday Night Live\" from 1985 to 1990.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0e7953c348",
  "kind": "yes/no",
  "text": "Claim: Halocyan Records has released records for the group who began acid-house, which spread to the United Kingdom and Europe. This group was based in the birthplace of baseball player George McNamara.\n\nPassages:\n\n[Acid house]\nAcid house spread to the United Kingdom and continental Europe, where it was played by DJs in the acid house and later rave scenes.\n\n[Halocyan Records]\nBased in Los Angeles, CA, the label has released music by artists such as DJ Pierre of Chicago-based acid house group Phuture, Paul Woolford, techno pioneer Joey Beltram, Vladislav Delay (as Sistol), ASC, xxxy, Appleblim & Al Tourettes, Extrawelt and many more.\n\n[Phuture]\nPhuture is an American, Chicago-based acid-house group of electronic musicians, founded in 1985 by Spanky, DJ Pierre and Herb J.\n\n[George McNamara (baseball)]\nHe was born in Chicago.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qabeb66ab00",
  "kind": "yes/no",
  "text": "Claim: This British television series Household Words was adapted from one of the better-known novels of a 19th-century writer and was first published in what magazine.\n\nPassages:\n\n[Cranford (novel)]\nCranford is one of the better-known novels of the 19th-century English writer Elizabeth Gaskell. It was first published, irregularly, in eight instalments, between December 1851 and May 1853, in the magazine \"Household Words\", which was edited by Charles Dickens.\n\n[Cranford (TV series)]\nCranford is a British television series directed by Simon Curtis and Steve Hudson. The teleplay by Heidi Thomas was adapted from three novellas by Elizabeth Gaskell published between 1849 and 1858: \"Cranford\", \"My Lady Ludlow\", and \"Mr Harrison's Confessions\". \"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9ae8b7ebd1",
  "kind": "yes/no",
  "text": "Claim: The Royal Commission into Drug Trafficking (1977-1979) or Wodward Royal Commission was a royal commission initiated by the New South Wales Government to investigate and shut down drug trafficking in New South Wales, Australia, especially links between the New South Wales Police and Mafia, The Honoured Society, is a Calabrian 'Ndrangheta criminal confederation, started in Melbourne and currently active in all of Australia.\n\nPassages:\n\n[Royal Commission into Drug Trafficking]\nThe Royal Commission into Drug Trafficking (1977–1979) or Woodward Royal Commission was a royal commission initiated by the New South Wales Government to investigate drug trafficking in New South Wales, Australia, especially links between the Mafia and New South Wales Police and the disappearance of anti-marijuana campaigner Donald Mackay.\n\n[Honoured Society (Australia)]\nThe Honoured Society (Italian: \"Onorata Società\" ) is a Calabrian 'Ndrangheta criminal confederation, started in Melbourne and currently active in all Australia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q14d6154912",
  "kind": "yes/no",
  "text": "Claim: Robert Armstrong-Jones, the Welsh physician, was grandfather to Antony Armstrong-Jones, 1st Earl of Snowdon.\n\nPassages:\n\n[Antony Armstrong-Jones, 1st Earl of Snowdon]\nAntony Charles Robert Armstrong-Jones, 1st Earl of Snowdon, (7 March 1930 – 13 January 2017), commonly known as Lord Snowdon, was a British photographer and film maker.\n\n[Robert Armstrong-Jones]\nSir Robert Armstrong-Jones, CBE (born Robert Jones; 2 December 1857 – 31 January 1943) was a Welsh physician and psychiatrist. He was the grandfather of Antony Armstrong-Jones, 1st Earl of Snowdon (d. 2017).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7051687fdb",
  "kind": "yes/no",
  "text": "Claim: The Camp Chapman suicide attack was located inside the Forward Operating Base Chapman in Texas.\n\nPassages:\n\n[Camp Chapman attack]\nThe Camp Chapman attack was a suicide attack by Humam Khalil Abu-Mulal al-Balawi against the Central Intelligence Agency facility inside Forward Operating Base Chapman on December 30, 2009.\n\n[Forward Operating Base Chapman]\nForward Operating Base Chapman, also known as Camp Chapman, is a United States military base located at the site of a former Afghan Army installation that is also being used by the Central Intelligence Agency.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe200fe8ceb",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Day 1 in our new dystopian society is not going well",
   "I'm literally out here trading eggs for potatoes Day 1 in our new dystopian society is going well #coronavirusUK #coronavirus"
  ]
 },
 {
  "qid": "q1866d0edfe",
  "kind": "yes/no",
  "text": "Claim: The writer and director of this film is Japanese. The film also starred Kari another actor. The film also starred Kari another actor. This actor also starred in Meteor Storm.\n\nPassages:\n\n[The Tree of Life (film)]\nThe Tree of Life is a 2011 American experimental epic drama film written and directed by Terrence Malick and featuring a cast of Brad Pitt, Sean Penn, Hunter McCracken, Laramie Eppler, Jessica Chastain, and Tye Sheridan in his debut feature film role.\n\n[Kari Matchett]\nShe has appeared in films such as \"Apartment Hunting\" (2000), \"Angel Eyes\" (2001), \"Men with Brooms\" (2002), \"Cypher\" (2002), \"Civic Duty\" (2006), \"The Tree of Life\" (2011), and \"Maudie\" (2016).\n\n[Terrence Malick]\nTerrence Frederick Malick ( ; born November 30, 1943) is an American film director, screenwriter and producer.\n\n[Meteor Storm]\nThe movie starred Michael Trucco and Kari Matchett.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q771fe8df76",
  "kind": "yes/no",
  "text": "Claim: The venue in Orlando opened in 1936 and is found west of the home venue for the Orlando City SC. The June 2017 Pro Bowl was played there.\n\nPassages:\n\n[2017 Pro Bowl]\nThe 2017 Pro Bowl (branded as the 2017 Pro Bowl presented by Aquafina for sponsorship reasons) was the National Football League's all-star game for the 2016 season which was played at Camping World Stadium in Orlando, Florida on January 29, 2017.\n\n[Camping World Stadium]\nCamping World Stadium, also known as the Orlando Citrus Bowl, is a stadium located in Orlando, Florida. The stadium is located in the West Lakes neighborhoods of Downtown Orlando, west of new sports and entertainment facilities including the Amway Center, the Dr. Phillips Center for the Performing Arts and the Orlando City Stadium.\n\n[Orlando City Stadium]\nIt is the home venue for the Orlando City SC, which entered Major League Soccer (MLS) as an expansion franchise in 2015, and their National Women's Soccer League (NWSL) sister club, the Orlando Pride.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8cfd68bd25",
  "kind": "yes/no",
  "text": "Claim: The 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada held from 30 June to 22 July 2007, Argentine player Sergio Aguero was given the FIFA U-20 Golden Shoe.\n\nPassages:\n\n[2007 FIFA U-20 World Cup]\nThe 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada from 30 June to 22 July 2007.\n\n[Sergio Agüero]\nSergio Leonel \"Kun\" Agüero (] ; born 2 June 1988) is an Argentine professional footballer who plays as a striker for Premier League club Manchester City and the Argentina national team.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qba05a2436d",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "fisher: \"i thought you said aids\" me: \"yeah rachel really loves aids\"",
   "honestly, there's not really a way I can think of being non-sarcastic, I was just being an asshole and teasing my friend who misheard my friend say eggs as aids. but I guess to be non-sarcastically I would've said \"no, she doesn't love aids\""
  ]
 },
 {
  "qid": "q397e2ff487",
  "kind": "yes/no",
  "text": "Claim: Both Orson Scott Card's novel \"Ender's Game\" and \"The Bone People,\"by the author whose work inspired the film \"Hooks and Feelers\" starring Bridgette Allen, both came out in 1985.\n\nPassages:\n\n[Bridgette Allen]\nShe also starred in the film \"Hooks and Feelers\", which was an adaptation of a Keri Hulme story.\n\n[Orson Scott Card]\nHis novel \"Ender's Game\" (1985) and its sequel \"Speaker for the Dead\" (1986) both won Hugo and Nebula Awards, making Card the only author to win both science fiction's top U.S. prizes in consecutive years.\n\n[Keri Hulme]\nHer only novel, \"The Bone People\", won the Booker Prize in 1985.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q11bdf76b01",
  "kind": "yes/no",
  "text": "Claim: The European species named after David Bowman (botanist) and Carlina are both flowering plants.\n\nPassages:\n\n[David Bowman (botanist)]\nThe species \"Dieffenbachia bowmanii\" is named after him.\n\n[Carlina]\nCarlina is a genus of flowering plants in the aster family, Asteraceae.\n\n[Dieffenbachia]\nDieffenbachia is a genus of tropical flowering plants in the family Araceae.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q33914d7415",
  "kind": "yes/no",
  "text": "Claim: The team that chose Joakim Noah for the 2007 NBA draft had a basketball player that Pekka Markkanen is the father of. That player whose father was Markkanen was traded for player Jimmy Butler III. Butler was born in Bhubaneswar.\n\nPassages:\n\n[Lauri Markkanen]\nIn the 2017 NBA draft, he was taken by the Minnesota Timberwolves with the 7th overall pick before being included in a trade to the Chicago Bulls for Jimmy Butler.\n\n[Joakim Noah]\nThe Chicago Bulls selected Noah with the ninth overall pick in the 2007 NBA draft.\n\n[Jimmy Butler (basketball)]\nJimmy Butler III (born September 14, 1989) is an American professional basketball player for the Minnesota Timberwolves of the National Basketball Association (NBA). Born in Houston, Butler grew up in Tomball, Texas, and played college basketball for Tyler Junior College and Marquette University.\n\n[Pekka Markkanen]\nMarkkanen is the father of Chicago Bulls basketball player Lauri Markkanen and the AIK football player Eero Markkanen.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q64c1977aab",
  "kind": "yes/no",
  "text": "Text: Had an end-of-the-year gathering with my ms coworkers tonight and it was just so nice to be together. \n\nGet vaccinated, guys.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q27cb79c3ec",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Ed Sheeran isn't at Tramlines and I'm glad about it",
   "Can’t wait to see Ed sheeran at tramlines tomoz x"
  ]
 },
 {
  "qid": "qce81efe506",
  "kind": "yes/no",
  "text": "Claim: The host of the 1993 MTV Video Music Awards starred in the movie Hard Rain. It was produced by Mark Gordon.\n\nPassages:\n\n[1993 MTV Video Music Awards]\nThe show was hosted by Christian Slater at the Gibson Amphitheatre in Los Angeles.\n\n[Christian Slater]\nIn the 1990s, Slater starred in many big budget films, including \"\", \"Interview with the Vampire\", \"\", \"Broken Arrow\", and \"Hard Rain\".\n\n[Hard Rain (film)]\nHard Rain is a 1998 action-thriller disaster film produced by Mark Gordon, written by Graham Yost, and directed by former cinematographer-turned director Mikael Salomon.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q532e6c119f",
  "kind": "yes/no",
  "text": "Claim: This person directed a 1955 French drama film, Black Dossier (film). This director and the director who is the father of Chris Donaldson are not both French filmmakers.\n\nPassages:\n\n[Chris Donaldson]\nHe is the son of film director Roger Donaldson.\n\n[André Cayatte]\nAndré Cayatte (3 February 1909, Carcassonne – 6 February 1989, Paris) was a French filmmaker and lawyer, who became known for his films centering on themes of crime, justice, and moral responsibility.\n\n[Black Dossier (film)]\nBlack Dossier (French: \"Le Dossier noir\" ) is a 1955 French drama film directed by André Cayatte.\n\n[Roger Donaldson]\nRoger Donaldson (born 15 November 1945) is an Australian-born New Zealand film director, producer and writer whose films include \"The World's Fastest Indian\" (2005), acclaimed 1981 relationship drama \"Smash Palace\", and a run of titles shot in the United States, including the Kevin Costner films \"No Way Out\" (1987) and \"Thirteen Days\" (2000), and the 1997 disaster film \"Dante's Peak\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4d97808e95",
  "kind": "yes/no",
  "text": "Post: Sleep? What’s that... I’ve never heard of it?",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q05ea8f2249",
  "kind": "yes/no",
  "text": "Claim: Tonino Accolla was the voice of Timon in an animated film. The London-born lyricist of this film and Kathy Acker are not both from America.\n\nPassages:\n\n[The Lion King]\nIts original songs were written by composer Elton John and lyricist Tim Rice, and original scores were written by Hans Zimmer.\n\n[Tim Rice]\nSir Timothy Miles Bindon \"Tim\" Rice (born 10 November 1944) is an English author and Academy Award, Golden Globe Award, Tony Award, and Grammy Award-winning lyricist.\n\n[Tonino Accolla]\nOther actors he dubbed over are Kenneth Branagh, Tom Hanks, Mickey Rourke, Ralph Fiennes, Jim Carrey, Ben Stiller, and Gary Oldman (\"Léon\" and \"The Fifth Element\"), as well as the voice of Timon in the animated film \"The Lion King\".\n\n[Kathy Acker]\nKathy Acker (née Lehmann; April 18, 1944 – November 30, 1997) was an American experimental novelist, punk poet, playwright, essayist, postmodernist and sex-positive feminist writer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa6200d2859",
  "kind": "yes/no",
  "text": "Claim: A n artist of the genre including Shuddha Saveri combines dance, costume, makeup, and dialogue. The author who wrote the 1995 novel Marali Mannige is this kind of artist.\n\nPassages:\n\n[Yakshagana]\nYakshagana ( Kannada : \"ಯಕ್ಷಗಾನ\", Tulu : \"ಆಟ\") is a traditional theatre form that combines dance, music, dialogue, costume, make-up, and stage techniques with a unique style and form.\n\n[Marali Mannige]\nMarali Mannige is a Kannada novel by novelist K. Shivaram Karanth.\n\n[K. Shivaram Karanth]\nKota Shivaram Karanth (10 October 1902 – 9 December 1997) was a Kannada writer, social activist, environmentalist, Yakshagana artist, film maker and thinker.\n\n[Shuddha Saveri]\nShuddha Saveri or śuddha sāveri is a rāgam in Carnatic music (musical scale of South Indian classical music) and Yakshagana music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q59948cea5a",
  "kind": "yes/no",
  "text": "Claim: Snakes on a Plane (Bring It) is the debut dingle for this band. The lead vocalist of this band and Robert Plant are not both English.\n\nPassages:\n\n[Snakes on a Plane (Bring It)]\n\"Snakes on a Plane (Bring It)\", also referred to as \"Bring It (Snakes on a Plane)\", is the debut single by Cobra Starship, released in 2006 from the soundtrack album \"\".\n\n[Gabe Saporta]\nGabriel Eduardo \"Gabe\" Saporta (born October 11, 1979) is an Uruguayan-American musician and entrepreneur.\n\n[Cobra Starship]\nCobra Starship was an American dance-pop band created by former Midtown bassist and lead vocalist Gabe Saporta in 2006 in New York City, New York.\n\n[Robert Plant]\nRobert Anthony Plant, {'1': \", '2': \", '3': \", '4': \"} (born 20 August 1948) is an English singer, songwriter, and musician, best known as the lead singer and lyricist of the rock band Led Zeppelin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q46f6b240c1",
  "kind": "yes/no",
  "text": "Claim: Always Watching: A Marble Hornets Story is a 2015 American supernatural horror film directed by Grace Phipps, stars American actor Jake McDorman, best known for starring in the leading role of Brian Finch in the CBS television comedy-drama, \"Limitless,\" from September 2015 to April 2016.\n\nPassages:\n\n[Jake McDorman]\nJohn Allen \"Jake\" McDorman IV (born July 8, 1986) is an American actor, best known for starring in the leading role of Brian Finch in the CBS television comedy-drama, \"Limitless,\" from September 2015 to April 2016.\n\n[Always Watching: A Marble Hornets Story]\nAlways Watching: A Marble Hornets Story is a 2015 American supernatural horror film directed by James Moran and starring Alexandra Breckenridge, Chris Marquette, Jake McDorman and Doug Jones.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q32a579e71d",
  "kind": "yes/no",
  "text": "Tweet: yesterday 4 dinner I just had rice w/ sriracha sauce on it and it was arguably the best meal I've had in a while",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q39f30c5882",
  "kind": "yes/no",
  "text": "Claim: In the The Simpsons episode, Homer invites a character over for dinner who is not voiced by Harry Shearer and another recurring character Hans Moleman.\n\nPassages:\n\n[Hans Moleman]\nHe was created by series creator Matt Groening and is voiced by Dan Castellaneta and first appeared in the episode \"Principal Charming\".\n\n[Principal Skinner]\nPrincipal W. Seymour Skinner (born Armin Tamzarian) is a fictional character in the American animated sitcom \"The Simpsons\", who is voiced by Harry Shearer.\n\n[Principal Charming]\nThings go wrong, however, when Homer invites Principal Skinner over for dinner and Skinner instead falls for Selma's twin sister Patty.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q78e402be7a",
  "kind": "yes/no",
  "text": "Claim: Jim Bambra has contributed to the single-player role-playing gamebook, Fighting Fantasy.\n\nPassages:\n\n[Fighting Fantasy]\nFighting Fantasy is a series of single-player role-playing gamebooks created by Steve Jackson and Ian Livingstone.\n\n[Jim Bambra]\nHe is particularly known for his contributions to \"Dungeons and Dragons\", \"Fighting Fantasy\", \"Warhammer\", and \"\" which was based on the \"Star Wars\" films.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd8ce4424b1",
  "kind": "yes/no",
  "text": "Claim: A sporting event was announced by Brad Nessler and this former player. Wizard of Westwood is the nickname of the head coach on whose team the announcer played in the early 1970s. Wizard of Westwood is the nickname of the head coach on whose team the announcer played in the early 1970s. Luicios Harris played in the sporting event.\n\nPassages:\n\n[John Wooden]\nNicknamed the \"Wizard of Westwood,\" he won ten NCAA national championships in a 12-year period as head coach at UCLA, including a record seven in a row.\n\n[Lucious Harris]\nHe played in the 2002 and 2003 NBA Finals as a member of the Nets.\n\n[2003 NBA Finals]\nThe series was broadcast on U.S. television on ABC, with Brad Nessler, Bill Walton, and Tom Tolbert announcing.\n\n[Bill Walton]\nWalton became known playing for John Wooden's powerhouse UCLA Bruins in the early 1970s, winning three successive College Player of the Year Awards, while leading the Bruins to two Division I national titles.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9b417b3160",
  "kind": "yes/no",
  "text": "Claim: Jaret Ray Reddick plays a Music Man Axis that has a flag of Texas design on it. The founder of Samadhi Sound does not.\n\nPassages:\n\n[Jaret Reddick]\nJaret Ray Reddick (born March 6, 1972) is an American musician, singer, songwriter, composer, podcaster, actor and voice actor, best known as the lead vocalist, rhythm guitarist, and primary songwriter for the rock band Bowling for Soup. He plays a Music Man Axis that has a flag of Texas design on it.\n\n[David Sylvian]\nDavid Sylvian (born David Alan Batt, 23 February 1958) is an English singer-songwriter and musician who came to prominence in the late 1970s as the lead vocalist and main songwriter in the group Japan.\n\n[Samadhi Sound]\nSamadhi Sound (or samadhisound) is an independent record label founded by singer and musician David Sylvian after his departure from Virgin Records in the late nineties.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf41688933d",
  "kind": "yes/no",
  "text": "Claim: The University at which Helmut Anheier holds a chair is located at Heidelberg, Baden-Württemberg.\n\nPassages:\n\n[Heidelberg University]\nHeidelberg University (German: \"Ruprecht-Karls-Universität Heidelberg\" ; Latin: \"Universitas Ruperto Carola Heidelbergensis\" ) is a public research university in Heidelberg, Baden-Württemberg, Germany.\n\n[Helmut Anheier]\nHe holds a chair at the Max Weber Institute of Sociology, Heidelberg University, where he is also the Academic Director of the Center for Social Investment and Innovation.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
