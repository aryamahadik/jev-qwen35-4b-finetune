# A46 replay label-noise blind read RSAS06-blind_read-ee5d083f-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS06-blind_read-ee5d083f-000.json

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
  "qid": "qabdf234ede",
  "kind": "yes/no",
  "text": "Claim: The birth city of Irakli Nasidze lies on the banks of the Kura River.\n\nPassages:\n\n[Tbilisi]\nTbilisi ( ; Georgian: თბილისი ] ), in some countries also still named by its pre-1936 international designation Tiflis ( or ), is the capital and the largest city of Georgia, lying on the banks of the Kura River with a population of approximately 1.5 million people.\n\n[Irakli Nasidze]\nIrakli Nasidze (Georgian: ირაკლი ნასიძე ; born 1973, Tbilisi) is a Georgian artist.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q49ebdb3bcc",
  "kind": "yes/no",
  "text": "Claim: The 1968 documentary film based on Timothy Treadwell premiered before Pray the Devil Back to Hell.\n\nPassages:\n\n[Timothy Treadwell]\nTreadwell's life, work, and death were the subject of Werner Herzog's critically acclaimed documentary film \"Grizzly Man\" (2005).\n\n[Pray the Devil Back to Hell]\nThe film premiered at the 2008 Tribeca Film Festival, where it won the award for Best Documentary.\n\n[Grizzly Man]\nGrizzly Man is a 2005 American documentary film by German director Werner Herzog.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc31c4df23b",
  "kind": "yes/no",
  "text": "Claim: Candi Kubeck was the captain of a plane. That plane was operated by the Swiss company headquartered in Clayton County, Georgia.\n\nPassages:\n\n[Candi Kubeck]\nCandalyn \"Candi\" Kubeck (née Chamberlain, May 10, 1961May 11, 1996) was an American commercial airline pilot and the captain of ValuJet Flight 592.\n\n[ValuJet Flight 592]\nOn May 11, 1996, the ValuJet Airlines McDonnell-Douglas DC-9 operating the route crashed into the Everglades about 11 minutes after taking off from Miami as a result of a fire in the cargo compartment caused by improperly stored cargo.\n\n[ValuJet Airlines]\nValuJet Airlines was an American low-cost carrier, headquartered in unincorporated Clayton County, Georgia, that operated regularly scheduled domestic and international flights in the Eastern United States and Canada during the 1990s.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb9990750c1",
  "kind": "yes/no",
  "text": "Claim: The name of the pop band founded by one of the stars of country music group Aisa Yeh Jahaan is Euphoria.\n\nPassages:\n\n[Aisa Yeh Jahaan]\nThe film is India's first carbon neutral film and stars Palash Sen, Ira Dubey and Kymsleen Kholie in lead roles, with Yashpal Sharma, Saurabh Pandey, Tinu Anand, Carol Gracias, Prisha Dabbas and Saurabh Pandey in supporting roles.\n\n[Palash Sen]\nPalash Sen is an Indian singer, songwriter, musician, composer and actor best known as the founder and frontman of India's pop band Euphoria.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa1d20f5cd6",
  "kind": "yes/no",
  "text": "Tweet: not to brag, but my thesis topic was so good that someone else published on it three months ago 🙃",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q9080cebb86",
  "kind": "yes/no",
  "text": "Claim: The home of F.C. Daburiyya is east of a city where 30.9% of its citizens are Christian.\n\nPassages:\n\n[Nazareth]\nNazareth ( ; Hebrew: נָצְרַת‎ , \"Natzrat\"; Arabic: النَّاصِرَة‎ ‎ , \"an-Nāṣira\"; Aramaic: ܢܨܪܬ‎ ‎ , \"Naṣrath\") is the capital and the largest city in the Northern District of Israel. The inhabitants are predominantly Arab citizens of Israel, of whom 69% are Muslim and 30.9% Christian.\n\n[Daburiyya]\nDaburiyya (Arabic: دبورية‎ ‎ ; Hebrew: דַבּוּרִיָּה‎ ), also \"Deburieh\" or \"Dabburieh\", is an Arab village ca. 8 km. east of Nazareth in Israel's Northern District.\n\n[F.C. Daburiyya]\nF.C. Daburiyya (Hebrew: מועדון ספורט דבוריה אוסמה‎ ‎ ), also known as Hapoel Daburiyya (Hebrew: הפועל דבוריה‎ ‎ ; Arabic: هبوعيل دبورية‎ ‎ ), is an Israeli football club based in Daburiyya.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf059a0b557",
  "kind": "yes/no",
  "text": "Claim: Clint Zweifel succeeded the Burmese who is currently serving the governor. This governor was part of the Navy.\n\nPassages:\n\n[Eric Greitens]\nEric Robert Greitens (born April 10, 1974) is an American politician, author, and former Navy SEAL currently serving as the 56th Governor of Missouri, since January 2017.\n\n[Clint Zweifel]\nHe succeeded Republican Sarah Steelman.\n\n[Sarah Steelman]\nShe is currently serving in the Office of Administration in Gov. Eric Greitens’ administration.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4be76ea9cb",
  "kind": "yes/no",
  "text": "Text: Does anyone else get really freaked out when seeing someone you’ve only known with a mask on without a mask for the first time??",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qd2704fe88e",
  "kind": "yes/no",
  "text": "Claim: Roden Brothers were taken over in 2010 by a group headquartered in the Canadian city of Montreal.\n\nPassages:\n\n[Roden Brothers]\nLtd. and were later taken over by Henry Birks and Sons in 1953.\n\n[Birks Group]\nThe company is headquartered in Montreal, Quebec, with American corporate offices located in Tamarac, Florida.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe6c664d073",
  "kind": "yes/no",
  "text": "Claim: Mel Duncan holds a history degree from the private, coeducational liberal arts Macalester College located in Saint Paul, Minnesota, US.\n\nPassages:\n\n[Mel Duncan]\nMelvin Earl Duncan (born May 22, 1950 in Davenport, Iowa) is the founding Executive Director of Nonviolent Peaceforce (NP), a civilian peacekeeping organization based in Brussels. He holds a bachelor's degree in Political Science from Macalester College in St. Paul, Minnesota and a Master of Arts in Humanities and Leadership from New College of California.\n\n[Macalester College]\nMacalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q738f54b542",
  "kind": "yes/no",
  "text": "Text: Even though my mom has to work a 12 hr shift today, I'm thankful she's happy with what she does and that she is doing what she needs to do in order to care for her children. She is the strongest and most important woman in my life. Without her, I am nothing.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q054834d54b",
  "kind": "yes/no",
  "text": "Claim: The album that the song Juntos (Together) is on is not a sports film. The 1979 show Peter Ellenshaw made before retiring is also not a sports film.\n\nPassages:\n\n[Peter Ellenshaw]\nHe retired after his work on \"The Black Hole\" (1979), but contributed matte paintings for \"Dick Tracy\" (1990).\n\n[The Black Hole]\nThe Black Hole is a 1979 American science fiction film directed by Gary Nelson and produced by Walt Disney Productions.\n\n[Juntos (Together)]\nThe song was released digitally via the iTunes Store by Walt Disney Records and Universal Music Latin on January 20, 2015, as the lead single from the soundtrack for \"McFarland, USA\".\n\n[McFarland, USA]\nMcFarland, USA (also known as McFarland) is a 2015 American sports drama film directed by Niki Caro, produced by Mark Ciardi and Gordon Gray, written by Christopher Cleveland, Bettina Gilois and Grant Thompson with music composed by Antônio Pinto.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q340d3b5772",
  "kind": "yes/no",
  "text": "Claim: The fifth studio album by English musician that guitarist George Harrison released as the follow-up to the album that was certified gold by the Recording Industry Association of America two days after release, was Dark Horse.\n\nPassages:\n\n[Living in the Material World]\nThe album was certified gold by the Recording Industry Association of America two days after release, on its way to becoming Harrison's second number 1 album in the United States, and produced the international hit \"Give Me Love (Give Me Peace on Earth)\".\n\n[Dark Horse (George Harrison album)]\nDark Horse is the fifth studio album by English musician George Harrison, released on Apple Records in December 1974 as the follow-up to \"Living in the Material World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1e3e4d07ca",
  "kind": "yes/no",
  "text": "Claim: Flatland Cavalry and Turnpike Troubadours have the art of rock music in common.\n\nPassages:\n\n[Turnpike Troubadours]\nTurnpike Troubadours is an American country music group from Oklahoma founded in 2005.\n\n[Flatland Cavalry]\nOn April 1, 2016, their first full-length album, \"Humble Folks\", was released to positive reviews and comparisons to the music of the Turnpike Troubadours.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7427c5e129",
  "kind": "yes/no",
  "text": "Claim: Julia Smith and Tony Holland were the creators of the long-running British soap opera in which Alison Pargeter plays the role of florist Sarah Cairns.\n\nPassages:\n\n[Alison Pargeter]\nAlison Pargeter (born 31 May 1972) is an English actress who played the roles of stalker Sarah Cairns in the BBC soap opera \"EastEnders\", also Mary Slessor in an 11-part television series of\" Mary Slessor\", and the Nag's Head barmaid called Val in the BBC \"Only Fools and Horses\" prequel \"Rock & Chips\".\n\n[EastEnders]\nEastEnders is a long-running British soap opera created by Julia Smith and Tony Holland which has been broadcast on BBC One since 1985.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2c25c12031",
  "kind": "yes/no",
  "text": "Claim: The older man whose understudy is Charlie Preedy plays for Arsenal Football Club as goalkeeper.\n\nPassages:\n\n[Arsenal F.C.]\nArsenal Football Club is a professional football club based in Highbury, London, England, that plays in the Premier League, the top flight of English football.\n\n[Charlie Preedy]\nHe was not initially the Gunners' first team goalkeeper, instead mainly playing as understudy to Dan Lewis, Arsenal's regular keeper.\n\n[Dan Lewis (footballer)]\nDaniel \"Dan\" Lewis (11 December 1902 – 1965) was a Welsh football goalkeeper, who is most notable for his time playing for Arsenal. He kept goal for Arsenal in the 1927 FA Cup Final where a mistake by him saw Cardiff City win the cup.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qecaeb047ca",
  "kind": "yes/no",
  "text": "Claim: Dances with the Wolves star Wesley \"Wes\" Studi also had a role in a film featuring Amanda Wyss.\n\nPassages:\n\n[Wes Studi]\nWesley \"Wes\" Studi (Cherokee: ᏪᏌ ᏍᏚᏗ ) (born December 17, 1947) is a Cherokee actor and film producer from Nofire Hollow in Oklahoma. He has appeared in Academy Award-winning films, such as \"Dances with Wolves\" (1990) and \"The Last of the Mohicans\" (1992), and in the Academy Award-nominated films \"\" (1993) and \"The New World\" (2005).\n\n[Powwow Highway]\nWes Studi and Graham Greene, who were relatively unknown actors at the time, have small supporting roles.\n\n[Amanda Wyss]\nShe subsequently starred in \"Silverado\" (1985), \"Better Off Dead\" (1985), \"Powwow Highway\" (1989), \"Shakma\" (1990), and \"The Id\" (2016).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q71f2ed623a",
  "kind": "yes/no",
  "text": "Claim: The president that signed a new Railway Labor Act in 1926 was a lawyer from Vermont in the 1890s.\n\nPassages:\n\n[Railroad Labor Board]\nThe Board was terminated on May 20, 1926 when President Calvin Coolidge signed a new Railway Labor Act into law.\n\n[Calvin Coolidge]\nA Republican lawyer from Vermont, Coolidge worked his way up the ladder of Massachusetts state politics, eventually becoming governor of that state.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8317d6d6c3",
  "kind": "yes/no",
  "text": "Claim: Giorgio Ferroni lived longer than the man who wrote Penalty Phase.\n\nPassages:\n\n[Penalty Phase]\nPenalty Phase is a 1986 American television thriller-drama film directed by Tony Richardson and starring Peter Strauss.\n\n[Tony Richardson]\nCecil Antonio \"Tony\" Richardson (5 June 1928 – 14 November 1991) was an English theatre and film director and producer whose career spanned five decades.\n\n[Giorgio Ferroni]\nGiorgio Ferroni (April 12, 1908 - August 17, 1981), sometimes credited as Calvin Jackson Padget or Calvin J. Padget, was an Italian film director, film editor and a screenwriter.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd3cca17f4b",
  "kind": "yes/no",
  "text": "Claim: The institution, at which poet Leoncio P. Deriada earned his BA English degree in 1959, has more schools than University of Rochester.\n\nPassages:\n\n[Leoncio P. Deriada]\nHe earned his BA English degree at the Ateneo de Davao University where he graduated cum laude in 1959.\n\n[University of Rochester]\nThe university has six schools and various interdisciplinary programs.\n\n[Ateneo de Davao University]\nThe Ateneo de Davao University is a private teaching, service and research university run by the Society of Jesus in Davao City in the Philippines. The university has five undergraduate schools, namely the School of Arts and Sciences, School of Business and Governance, School of Engineering and Architecture, School of Education and the School of Nursing. The university also runs a grade school and high school.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb6e4e33d96",
  "kind": "yes/no",
  "text": "Claim: The Danish singer Lucky Yates is known for his voice-over roles as Dr. Krieger on a spy sitcom created by Adam Reed.\n\nPassages:\n\n[Archer (TV series)]\nArcher is an American adult animated spy sitcom created by Adam Reed for the FX network.\n\n[Lucky Yates]\nHe is known for his voice-over roles as Dr. Krieger on \"Archer\" and The Xtacles on \"Frisky Dingo\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe6b5ee6419",
  "kind": "yes/no",
  "text": "Claim: Spencer Grove co-created the American live-action/animated TV series, co-produced by The Collective and the studios 14th Hour Productions, in which the American filmmaker, singer, and actor born in 1979 provides the voice of the title character.\n\nPassages:\n\n[The High Fructose Adventures of Annoying Orange]\nThe High Fructose Adventures of Annoying Orange is an American live-action/animated TV series based on the characters from the popular web series \"The Annoying Orange\", created by Dane Boedigheimer and Spencer Grove, which is made for the television by Boedigheimer himself with Tom Sheppard for Cartoon Network. It was produced by Daneboe's company Annoying Orange, Inc., alongside management company The Collective and the studios 14th Hour Productions.\n\n[Dane Boedigheimer]\nDane Boedigheimer (born September 28, 1979), better known by his cybernym Daneboe, is an American filmmaker, singer, and actor. He is known for his web series \"The Annoying Orange\" and the TV series \"The High Fructose Adventures of Annoying Orange\", in which he provides the voice of the title character.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5b1e2e3cf9",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Old people don’t deserve rights",
   "old people suck"
  ]
 },
 {
  "qid": "q2948dd8b6c",
  "kind": "yes/no",
  "text": "Tweet: as much as i like being home i miss my uni pals and messing around in the kitchen at 2am",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q2408e332f2",
  "kind": "yes/no",
  "text": "Claim: The actor who recorded the comedy album The Sunny Side of the Street was born in 1945. He starred in the show \"Trial & Error\".\n\nPassages:\n\n[John Lithgow]\nJohn Arthur Lithgow ( ; born October 19 , 1945) is an American actor, musician, singer, comedian, voice actor, and author.\n\n[Trial &amp; Error (TV series)]\nIt stars Nicholas D'Agosto, Jayma Mays, Steven Boyer, Krysta Rodriguez, and Sherri Shepherd, with John Lithgow also starring in the first season.\n\n[The Sunny Side of the Street]\nThe Sunny Side of the Street is an album recorded by John Lithgow, released in 2006.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1ca554fce2",
  "kind": "yes/no",
  "text": "Claim: John Valliant's work has appeared in an outdoor-focused magazine whose first issue was published in September 1977 and featured the column called \"Natural Acts\" written by David Quammen.\n\nPassages:\n\n[John Vaillant]\nJohn Vaillant is an American writer and journalist whose work has appeared in \"The New Yorker, The Atlantic, National Geographic\", and \"Outside\".\n\n[David Quammen]\nHe wrote a column, called \"Natural Acts\" for \"Outside\" magazine for fifteen years.\n\n[Outside (magazine)]\nOutside is an American magazine focused on the outdoors. The first issue was published in September 1977.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfa193d8bba",
  "kind": "yes/no",
  "text": "Claim: Helen Elizabeth Hunt won more awards than Dan Schneider.\n\nPassages:\n\n[Helen Hunt]\nHelen Elizabeth Hunt (born June 15, 1963) is an American actress, director, and screenwriter. She starred in the sitcom \"Mad About You\" for seven years, and played single mother Carol Connelly in the 1997 romantic comedy film \"As Good as It Gets\", for which she won the Academy Award for Best Actress. Hunt has also won four Emmy Awards, four Golden Globe Awards, and two Screen Actors Guild Awards.\n\n[Dan Schneider (TV producer)]\nDan Schneider (born January 14, 1966) is an American actor, television and film writer, and producer. After appearing in mostly supporting roles in a number of 1980s and 1990s films and TV shows, Schneider devoted himself to behind-the-scenes work in production. He is the co-president of television production company Schneider's Bakery. He created/co-created \"All That\", \"The Amanda Show\", \"What I Like About You\", \"Drake & Josh\", \"Zoey 101\", \"iCarly\", \"Victorious\", \"Sam & Cat\", \"Henry Danger\", \"Game Shakers\", and \"The Adventures of Kid Danger and Captain Man\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe2371ab0bc",
  "kind": "yes/no",
  "text": "Claim: Widewuto, a legendary ruler of the pagan Prussians, was believed to have existed before the army of the Teutonic Knights launched crusade against the Prussian peoples.\n\nPassages:\n\n[Widewuto]\nWidewuto (also \"Viduutus\", \"Vidvutus\", \"Witowudi\", \"Waidewut\") was a legendary king of the pagan Prussians who ruled along with his elder brother, the high priest Bruteno in the 6th century AD. It is unclear whether the legend was authentically Prussian (i.e. recorded from Prussian mythology) or was created by Grunau (possibly inspired by Biblical Moses and Aaron), though Lithuanian researchers tend to support in its authenticity.\n\n[Prussian mythology]\nThe Prussian mythology was a polytheistic religion of the Old Prussians, indigenous peoples of Prussia before the Prussian Crusade waged by the Teutonic Knights. No sources document pagan religion before the forced Christianization in the 13th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qee97299c8c",
  "kind": "yes/no",
  "text": "Claim: Sal de Mi Piel is a song by the actress who is of Spanish nationality.\n\nPassages:\n\n[Belinda Peregrín]\nBelinda Peregrín Schüll (born August 15, 1989), known mononymously as Belinda, is a Spanish singer and actress Mexican naturalized .\n\n[Sal de Mi Piel]\n\"Sal de Mi Piel\" (English: \"Get Out of My Skin\"), is a song by famous Mexican actress and singer Belinda.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q508a6dd6e2",
  "kind": "yes/no",
  "text": "Claim: Markounda is a sub-prefecture that borders an Central African Republic country bordered by Libya and the Sudan and is known for the Dar Sila region.\n\nPassages:\n\n[Markounda]\nThe sub-prefecture borders with Chad.\n\n[Chad]\nIt is bordered by Libya to the north, Sudan to the east, the Central African Republic to the south, Cameroon and Nigeria to the southwest and Niger to the west.\n\n[Sila Region]\nSila or Dar Sila is a region of Chad which was created in 2008 from the departments of Sila and Djourf Al Ahmar previously part of Ouaddaï Region.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q66d41f2919",
  "kind": "yes/no",
  "text": "Claim: Ernst Messerschmid and Reinhold Ewald ESA were not both astronauts.\n\nPassages:\n\n[Ernst Messerschmid]\nProf. Dr. Ernst Willi Messerschmid (born May 21, 1945) is a German physicist and former astronaut.\n\n[Reinhold Ewald]\nDr. Reinhold Ewald (born December 18, 1956) is a German physicist and ESA astronaut.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q179341f4ff",
  "kind": "yes/no",
  "text": "Claim: The magazine, that employed photographer Horace Bristol, and another magazine were both published monthly in 1998. Frank Legato wrote a monthly column for this other magazine.\n\nPassages:\n\n[Horace Bristol]\nHorace Bristol (November 16, 1908 – August 4, 1997) was a twentieth-century American photographer, best known for his work in \"Life.\"\n\n[Frank Legato]\nHe is also well known for founding and editing \"Casino Gaming\" magazine and writing a monthly humorous column about slot machines for \"Strictly Slots\" magazine.\n\n[Strictly Slots]\nStrictly Slots is a monthly magazine aimed at slot machine and video poker players. The magazine was founded in 1998.\n\n[Life (magazine)]\n\"Life\" was published weekly until 1972, as an intermittent \"special\" until 1978, and as a monthly from 1978 to 2000.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qea1116a82d",
  "kind": "yes/no",
  "text": "Claim: Massimiliano Antonio \"Max\" Cavalera played in the band Soulfly not Billy Idol.\n\nPassages:\n\n[Max Cavalera]\nMassimiliano Antonio \"Max\" Cavalera (] , born August 4, 1969) is a Brazilian singer, guitarist, and songwriter who currently plays in heavy metal bands Soulfly, Cavalera Conspiracy, and Killer Be Killed.\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc914480eb3",
  "kind": "yes/no",
  "text": "Claim: William Lyon served at Robins Air Force Base in Houston County, Georgia until his dishonourable discharge in 1987.\n\nPassages:\n\n[Robins Air Force Base]\nRobins Air Force Base (IATA: WRB, ICAO: KWRB) is a major United States Air Force installation located in Houston County, Georgia, United States.\n\n[William Lyon (general)]\nWilliam Lyon (born March 9, 1923) is a retired major general of the United States Air Force who served as Commander of the United States Air Force Reserve Command, Headquarters U.S. Air Force, Washington D.C., and commander, Headquarters Air Force Reserve, a separate operating agency located at Robins Air Force Base, Georgia.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qedff27375f",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "My poo is green, how festive.",
   "I have diarrhoea"
  ]
 },
 {
  "qid": "q7067c8fc07",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "@trpalomo Those boots must be tasty for how much they're choking on 'em 💀",
   "No."
  ]
 },
 {
  "qid": "qb0897a50d0",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Repulsing people would certainly draw attention.",
   "@BellularGaming Blizzard will have to make sure it doesn't exceed the recommended fun level of 10%."
  ]
 },
 {
  "qid": "q91cff66f6e",
  "kind": "yes/no",
  "text": "Tweet: tanning in this heat is an extreme sport",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd4355f8ba3",
  "kind": "yes/no",
  "text": "Claim: Brickyard is the call sign of the airline that operates the flight with United Express Flight 3411 incident.\n\nPassages:\n\n[United Express Flight 3411 incident]\nRepublic Airline operated the scheduled passenger flight on behalf of United Express, a United Airlines regional branch.\n\n[Republic Airline]\nIts call sign \"Brickyard\" is derived from the nickname of the Indianapolis Motor Speedway.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q21bd66d384",
  "kind": "yes/no",
  "text": "Claim: This institution created Whirlwind I. The school that Donny Green played football for is in the same country.\n\nPassages:\n\n[Whirlwind I]\nWhirlwind I was a Cold War-era vacuum tube computer developed by the MIT Servomechanisms Laboratory for the U.S. Navy.\n\n[University of Virginia]\nThe University of Virginia (U.Va. or UVA), frequently referred to simply as Virginia, is a public research university and the flagship for the Commonwealth of Virginia.\n\n[Donny Green]\nHe played for the Washington Redskins and the Jacksonville Jaguars, and played college football at the University of Virginia.\n\n[Massachusetts Institute of Technology]\nThe Massachusetts Institute of Technology (MIT) is a private research university in Cambridge, Massachusetts.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2cd0a7d5e6",
  "kind": "yes/no",
  "text": "Claim: The Dennis Publishing company has published a magazine that Bob Basset has appeared in. Also, a sister publication devoted to the anomalous phenomena popularised by Charles Fort.\n\nPassages:\n\n[Bizarre (magazine)]\nBizarre was a British alternative magazine published from 1997 to 2015. It was published by Dennis Publishing, and was a sister publication to the \"Fortean Times\".\n\n[Bob Basset]\nPublications about Bob Basset appeared in , WAD magazine, VICE UK, Bizarre Magazine, INSIDE artzine magazine.\n\n[Fortean Times]\nFortean Times is a British monthly magazine devoted to the anomalous phenomena popularised by Charles Fort. Previously published by John Brown Publishing (from 1991 to 2001) and then I Feel Good Publishing (2001 to 2005), it is now published by Dennis Publishing Ltd.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa73a653f78",
  "kind": "yes/no",
  "text": "Text: Video interviews in your slippers is one of the weirder side effects of the pandemic, but i won't complain lmao",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q50543538bb",
  "kind": "yes/no",
  "text": "Claim: X Factor winner Leona Lewis has worked with a co-writer of the song Do It Well.\n\nPassages:\n\n[Ryan Tedder]\nAs well as being the lead vocalist for the pop rock band OneRepublic, he has an independent career as a songwriter and producer for various artists, including Madonna, U2, Adele, Beyoncé, Maroon 5, Demi Lovato, Ariana Grande, Kelly Clarkson, Jennifer Lopez, Westlife, Ed Sheeran, One Direction, Big Time Rush, Camila Cabello, Taylor Swift, Leona Lewis, Zedd and MØ.\n\n[Leona Lewis]\nLewis achieved national recognition when she won the third series of \"The X Factor\" in 2006, winning a £1 million recording contract with Simon Cowell's record label, Syco Music.\n\n[Do It Well]\nIt was written by Ryan Tedder, Leonard Caston, Anita Poree, and Frank Wilson.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb5c87ff210",
  "kind": "yes/no",
  "text": "Claim: The Catuvellani, a settlement of whose can be found near the city of St Albans in Hertfordshire, were a 8th century Celtic tribe.\n\nPassages:\n\n[History of St Albans]\nSt Albans is a city in southern Hertfordshire, England, 20 miles (32 km) north of London, beside the site of a Catuvellauni settlement and the Roman town of Verulamium on the River Ver.\n\n[Catuvellauni]\nThe Catuvellauni were a Celtic tribe or state of southeastern Britain before the Roman conquest, attested by inscriptions into the 4th century.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q33faac16e3",
  "kind": "yes/no",
  "text": "Claim: The Football League Super Cup was formed in response to an incident when escaping fans were pressed against a collapsing wall in Heysel Stadium in Brussels in 1986.\n\nPassages:\n\n[Heysel Stadium disaster]\nThe Heysel Stadium disaster (] , ] ; Dutch: \"Heizeldrama\" ; French: \"Drame du Heysel\" ) occurred on 29 May 1985 when escaping fans were pressed against a collapsing wall in the Heysel Stadium in Brussels, Belgium, before the start of the 1985 European Cup Final between Juventus of Italy and Liverpool of England.\n\n[Football League Super Cup]\nThe Football League Super Cup (later known under its sponsored name as the ScreenSport Super Cup) was a one-off football club competition held in England in the 1985–86 season. It was organised by the Football League and was intended as some form of financial and sporting compensation for the English clubs which had qualified for European competition in the previous season but had been banned from entering European tournaments by UEFA following the Heysel Stadium disaster.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc24136021c",
  "kind": "yes/no",
  "text": "Claim: David Nixon and another man are both film directors. The other director directed a film. This film features the song \"Tennessee Homesick Blues\".\n\nPassages:\n\n[Tennessee Homesick Blues]\n\"Tennessee Homesick Blues\" is a song written and recorded by Dolly Parton that was featured in the soundtrack of the 1984 movie \"Rhinestone.\"\n\n[David Nixon (director)]\nDavid Nixon is an American film director and film producer.\n\n[Phil Alden Robinson]\nPhil Alden Robinson (born March 1, 1950) is an American film director and screenwriter whose films include \"Field of Dreams\", \"Sneakers\", and \"The Sum of All Fears\".\n\n[Rhinestone (film)]\nRhinestone is a 1984 American musical comedy film directed by Bob Clark from a screenplay by Sylvester Stallone and Phil Alden Robinson and starring Stallone and Dolly Parton.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q34dfc4441a",
  "kind": "yes/no",
  "text": "Claim: Mark Brooks won the PGA Championship to be held at Vahalla, which was also the site of the 2014 PGA Championship.\n\nPassages:\n\n[2014 PGA Championship]\nThis was the third PGA Championship at Valhalla, which previously hosted in 1996 and 2000, both won in playoffs, as well as the Ryder Cup in 2008, the most recent U.S. victory.\n\n[2000 PGA Championship]\nThe 2000 PGA Championship was the 82nd PGA Championship, held August 17–20 at the Valhalla Golf Club in Louisville, Kentucky. Tiger Woods won his second straight PGA Championship and fifth major in a three-hole playoff over Bob May.\n\n[1996 PGA Championship]\nThe 1996 PGA Championship was the 78th PGA Championship, held August 8–11 at Valhalla Golf Club in Louisville, Kentucky. Mark Brooks won his only major championship with a birdie at the first hole of a sudden-death playoff with Kentucky native Kenny Perry.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbc4b6ebb9f",
  "kind": "yes/no",
  "text": "Claim: Baghdad was also known as the City of Peace during the Abbasid Caliphate.\n\nPassages:\n\n[The Last Voyage of Somebody the Sailor]\nEventually he makes his way to \"Baghdad, the City of Peace\", and finds himself in the stories of Sindbad and Scheherazade.\n\n[Sinbad the Sailor]\nSinbad the Sailor (Arabic: ٱلسِّنْدِبَادُ ٱلْبَحرِيّ‎ ‎ \"as-Sindibādu al-Baḥriyy\") also spelled Sindbad, is a fictional sailor and the hero of a story-cycle of Middle Eastern origin; he is described as living in Baghdad, during the Abbasid Caliphate.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5ba6db0e87",
  "kind": "yes/no",
  "text": "Claim: One of the founding members of the Breeders was the singer for Throwing Muses. She was born 4 years before Trace Cyrus.\n\nPassages:\n\n[Tanya Donelly]\nTanya Donelly (born July 14, 1966, in Newport, Rhode Island) is an American Grammy Award-nominated singer-songwriter and guitarist based in New England who co-founded Throwing Muses with her stepsister Kristin Hersh.\n\n[The Breeders]\nThe Breeders are an American alternative rock band formed in 1989 by Kim Deal of the Pixies and Tanya Donelly of Throwing Muses.\n\n[Trace Cyrus]\nTrace Dempsey Cyrus (born Neil Timothy Helson; February 24, 1989) is an American musician.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd437ade062",
  "kind": "yes/no",
  "text": "Claim: Southridge mall is synonymous with the largest, not second largest, mall in state.\n\nPassages:\n\n[Fox River Mall]\nAt 1.21 million square feet, it is the largest mall in Wisconsin.\n\n[Southridge Mall (Wisconsin)]\nAt 1.2 million square feet,(1.26 million) it is tied with the Fox River Mall in Grand Chute as the largest mall in the state (by square footage).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
