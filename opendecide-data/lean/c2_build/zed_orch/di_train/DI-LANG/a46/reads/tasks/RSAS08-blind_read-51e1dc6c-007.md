# A46 replay label-noise blind read RSAS08-blind_read-51e1dc6c-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS08-blind_read-51e1dc6c-007.json

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
  "qid": "q28ef60f595",
  "kind": "yes/no",
  "text": "Claim: Riviera Partners' clientele Zappos is located in Las Vegas, Nevada and was incorporated in 1985.\n\nPassages:\n\n[Riviera Partners]\nRiviera Partners' clientele includes, among others, ServiceNow, Xoom, One Kings Lane, Uber, Path, Okta, Pure Storage, Twitter, LinkedIn, Dropbox, Pinterest, and Zappos.\n\n[Zappos]\nZappos.com is an online shoe and clothing shop based in Las Vegas, Nevada.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q259b1da904",
  "kind": "yes/no",
  "text": "Claim: The city containing the Parafield railway station is very near the airport and the Mawson Lakes campus of the University of South Australia.\n\nPassages:\n\n[Parafield railway station]\nSituated in the northern Adelaide suburb of Parafield, It is 17.7 km from Adelaide station.\n\n[Parafield Airport]\nParafield Airport (ICAO: YPPF) is on the edge of the residential suburb of Parafield, South Australia, 18 km north of the Adelaide city centre and adjacent to the Mawson Lakes campus of the University of South Australia.\n\n[Parafield, South Australia]\nThe suburb is essentially contiguous with Parafield Airport.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q152c3c3a27",
  "kind": "yes/no",
  "text": "Claim: Linzhou, Henan has a larger population than the town where the Liaoning Finance and Trade College is located.\n\nPassages:\n\n[Xingcheng]\nXingcheng (), former name Ningyuan (宁远), is a county-level city of southwest Liaoning province, China, with a population of approximately 140,000 urban inhabitants, and is located on the Liaodong Bay, i.e. the northern coast of the Bohai Sea.\n\n[Liaoning Finance and Trade College]\nLiaoning Finance and Trade College (), formerly known as Shenyang Shifan University Bohai College, is a small, partially walled private undergraduate college located on the Liaodong Bay of the Bohai coast in Xingcheng, southwest of Huludao in Liaoning province on the east coast of China.\n\n[Linzhou, Henan]\nIt covers an area of 2046 square kilometers and has a population of about one million.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q729e54d70b",
  "kind": "yes/no",
  "text": "Claim: Richie Furay was born before the former Blitz Kid later to be the frontman of Tony James' band. This band released the album and single Dress for Excess.\n\nPassages:\n\n[Dress for Excess]\nDress for Excess is the second album by British band Sigue Sigue Sputnik, released in 1988 (see 1988 in music).\n\n[Blitz Kids]\nAmong the many attendees were Rusty Egan, Steve Strange, Boy George, Marilyn, Alice Temple, Perri Lister, Princess Julia, Philip Sallon, Carl Teper and Martin Degville (later to be the frontman of Tony James' Sigue Sigue Sputnik).\n\n[Richie Furay]\nPaul Richard \"Richie\" Furay (born May 9, 1944) is an American singer, songwriter, and Rock & Roll Hall of Fame member who is best known for forming the bands Buffalo Springfield with Stephen Stills, Neil Young, Bruce Palmer, and Dewey Martin, and Poco with Jim Messina, Rusty Young, George Grantham and Randy Meisner.\n\n[Martin Degville]\nMartin Degville is (born 27 January 1961 in Walsall) is the lead singer and co-songwriter of the UK pop band, Sigue Sigue Sputnik – which had a worldwide hit single in 1986 with \"Love Missile F1-11\" – and six other EMI single releases.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5ede7a967a",
  "kind": "yes/no",
  "text": "Claim: The Chicago Mayer-endorsed, 38th Ward of the City of Chicago alderman is serving the Northwest Side of town since 1961.\n\nPassages:\n\n[Rahm Emanuel]\nRahm Israel Emanuel ( ; born November 29, 1959) is an American politician who is the 44th and current mayor of Chicago.\n\n[Nicholas Sposato]\nNicholas Sposato serves on Chicago City Council as alderman of the 38th Ward of the City of Chicago on the city's Northwest Side.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q47d37a1db3",
  "kind": "yes/no",
  "text": "Claim: The defending champions of the 1999 Challenge Bell – Doubles were Lori McNeil and her partner. Her partner is younger than coach Joakim Nystrom.\n\nPassages:\n\n[Joakim Nyström]\nJoakim \"Jocke\" Nyström (born 20 February 1963) is a former top ten ranked tennis player from Sweden who won 13 singles titles during his professional career.\n\n[1999 Challenge Bell – Doubles]\nLori McNeil and Kimberly Po were the defending champions, but lost in the quarterfinals to Amy Frazier and Katie Schlukebir.\n\n[Kimberly Po]\nKimberly Po-Messerli (born October 20, 1971) is a former professional tennis player from the United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qbd66b643dc",
  "kind": "yes/no",
  "text": "Claim: Ronan was performed at an Arizona stop of the 1989 World Tour.\n\nPassages:\n\n[Ronan (song)]\nSwift first performed the song live for Stand Up to Cancer in September 2012, and has only performed it publicly one other time, at the Glendale, Arizona stop of The 1989 World Tour, at which Thompson was in attendance.\n\n[The 1989 World Tour]\nThe 1989 World Tour was the fourth concert tour by American singer-songwriter Taylor Swift, in support of her fifth studio album, \"1989\" (2014).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa91f582c8f",
  "kind": "yes/no",
  "text": "Post: I do love it when my mum makes me spend my savings on beer 😒",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q3b4ec647f7",
  "kind": "yes/no",
  "text": "Post: will never understand why ppl do meth,, just buy a shit tonne of incense in bulk stupid",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q2d89826a70",
  "kind": "yes/no",
  "text": "Tweet: always remember thank your Alexa, just in case the AI take over one day",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q0c28cb5585",
  "kind": "yes/no",
  "text": "Claim: An American author wrote The Lay of the Land. This author has more scope of profession than Robert E. Howard.\n\nPassages:\n\n[Robert E. Howard]\nRobert Ervin Howard (January 22, 1906 – June 11, 1936) was an American author who wrote pulp fiction in a diverse range of genres.\n\n[Richard Ford]\nRichard Ford (born February 16, 1944) is an American novelist and short story writer.\n\n[The Lay of the Land]\nThe Lay of the Land is a 2006 novel by American author Richard Ford.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb56f9dbbea",
  "kind": "yes/no",
  "text": "Text: So, very delayed flight from Bristol to Edinburgh @easyJet, trademark vagueness from staff, with a chronic lack of empathy to boot (despite me travelling with three young children)... now, time to feed our family with £3 vouchers (at airport prices!) #bollocks",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe8ae5515d2",
  "kind": "yes/no",
  "text": "Text: who up? who on norco?",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qcc966f7805",
  "kind": "yes/no",
  "text": "Post: Hot dog eating contest as a form of assisted suicide",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf72d490439",
  "kind": "yes/no",
  "text": "Claim: \"I Do\" the song by Filipino singer Nina and described to be Mariah Carey-like was on third studio album, \"Nina\".\n\nPassages:\n\n[Mariah Carey]\nMariah Carey (born March 27, 1969 or 1970) is an American singer, songwriter, record producer, and actress.\n\n[I Do (Nina Girado song)]\n\"I Do\" is a song by Filipino singer Nina from her self-titled third studio album, \"Nina\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q755b4add51",
  "kind": "yes/no",
  "text": "Claim: Alan Sokal, a professor of mathematics, authored the book Fashionable Nonsense in 1781.\n\nPassages:\n\n[Alan Sokal]\nAlan David Sokal ( ; born January 24, 1955) is a professor of mathematics at University College London and professor of physics at New York University.\n\n[Fashionable Nonsense]\nFashionable Nonsense: Postmodern Intellectuals' Abuse of Science (French: \"Impostures Intellectuelles\" ), published in the UK as Intellectual Impostures, is a book by physicists Alan Sokal and Jean Bricmont.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qab32d2279d",
  "kind": "yes/no",
  "text": "Claim: Guillermo del Toro did not direct the film which had the man, who starred in Bone Dry alongside Lance Henriksen, play the role of Jared Nomak.\n\nPassages:\n\n[Blade II]\nIt was written by David S. Goyer, who also wrote the previous film, directed by Guillermo del Toro, and had Wesley Snipes returning as the lead character and producer.\n\n[Bone Dry]\nThe film starred Luke Goss and Lance Henriksen.\n\n[Luke Goss]\nHe has appeared in numerous films including \"Blade II\" (2002) as Jared Nomak, \"One Night with the King\" (2006) as King Xerxes, \"\" (2008) as Prince Nuada, \"Tekken\" (2010) as Steve Fox and \"Interview with a Hitman\" (2012) as Viktor.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc476d88fa7",
  "kind": "yes/no",
  "text": "Claim: The residence at 200 West Street is taller than the one at the location of Pershing Square Capital Management.\n\nPassages:\n\n[888 7th Avenue]\n888 7th Avenue is a 628 ft (191m) tall modern-style office skyscraper in Midtown Manhattan which was completed in 1969 and has 46 floors.\n\n[200 West Street]\n200 West Street is the global headquarters of the Goldman Sachs investment banking firm. The building is a 749 ft , 44-story building located on West Street, between Vesey and Murray Streets in Lower Manhattan.\n\n[Pershing Square Capital Management]\nPershing Square Capital Management is an American hedge fund management company founded and run by Bill Ackman, located at 888 7th Avenue in New York.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2e27864059",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Non-sarcastically I'd probably say \"Oh, out of curiousity, what's the reason for Ms. Thatcher trending?\"",
   "'Margaret Thatcher' is trending... has 2016 taken another one?"
  ]
 },
 {
  "qid": "q399cefa839",
  "kind": "yes/no",
  "text": "Claim: Heart on My Sleeve is a song first recorded by Australian singer Michael Johns.\n\nPassages:\n\n[Heart on My Sleeve]\nIt was first released by \"American Idol\" season 7 contestant Michael Johns from his post-\"Idol\" album, \"Hold Back My Heart\".\n\n[Michael Johns (singer)]\nMichael Johns (born Michael John Lee; 20 October 1978 – 1 August 2014) was an Australian singer who finished in eighth place on the seventh season of \"American Idol\", in 2008.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q799fc23fb7",
  "kind": "yes/no",
  "text": "Claim: Dan Smith's song reached as low as number 5 on the US \"Billboard\" Hot 100 chart in 2013.\n\nPassages:\n\n[Dan Smith (singer)]\nDaniel Campbell \"Dan\" Smith (born 14 July 1986) is a British singer-songwriter and record producer. He is the lead singer, primary songwriter. The band formed in 2010 and gained mass popularity in 2013 when the song \"Pompeii\" was released.\n\n[Pompeii (song)]\nThe song was released as the album's fourth single on 12 January 2013. It reached number 2 in the UK Singles Chart, number 4 in Australian ARIA Chart, and number 5 on the US \"Billboard\" Hot 100 and number one on the Alternative Songs chart.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfc5fda3c3e",
  "kind": "yes/no",
  "text": "Post: attack on Titan I’m not ok\n\nSaw a few leaks on purpose bc I like to torture myself and I’ll wait to read the whole chapter tomorrow but oh my god oh my god I’m hurting",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe0e516de4d",
  "kind": "yes/no",
  "text": "Claim: This athlete won the 2004 BNP Paribas Masters – Singles title for the then record 3rd time. Both she and the 2008 Kremlin Cup – Women's Singles semi-finals winner have both played tennis professionally.\n\nPassages:\n\n[2008 Kremlin Cup – Women's Singles]\nElena Dementieva was the defending champion, but lost in the semifinals to Jelena Janković.\n\n[Jelena Janković]\nJelena Janković (Serbian Cyrillic: Јелена Јанковић, ] , born 28 February 1985) is a Serbian professional tennis player.\n\n[Marat Safin]\nMarat Mubinovich Safin (Russian: Мара́т Муби́нович Са́фин ; ] , Tatar: Марат Мөбин улы Сафин \"Marat Möbin uğlı Safin\" ; born 27 January 1980) is a Russian politician and retired professional tennis player.\n\n[2004 BNP Paribas Masters – Singles]\nMarat Safin won the title for the then record 3rd time, defeating Radek Štěpánek in the final in straight sets.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf1d68b94d1",
  "kind": "yes/no",
  "text": "Claim: The Minnesota Vikings team selected the 2009 Pac-10 Offensive Player of the Year in the second round of the 2010 NFL Draft in Paris.\n\nPassages:\n\n[Toby Gerhart]\nHe was selected by the Minnesota Vikings in the second round of the 2010 NFL Draft.\n\n[2009 All-Pacific-10 Conference football team]\nStanford running back Toby Gerhart was voted Pac-10 Offensive Player of the Year.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q40b1fec9aa",
  "kind": "yes/no",
  "text": "Tweet: Don’t expect others to help you if you don’t want to help yourself 🗣",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q9c94a245b9",
  "kind": "yes/no",
  "text": "Claim: The American filmmaker Sebastian Sommer studied at the Tisch School of the Arts in New York City.\n\nPassages:\n\n[Tisch School of the Arts]\nIt is located at 721 Broadway in Manhattan, New York City.\n\n[Sebastian Sommer]\nGrowing up in New York City, he studied Film at Tisch School of the Arts.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qba26c09aba",
  "kind": "yes/no",
  "text": "Claim: The youngest child of soccer player Mangue Cisse plays for the Swiss club Yverdon.\n\nPassages:\n\n[Mangué Cissé]\nHe had seven children, the youngest of which is French international, Djibril Cissé.\n\n[Djibril Cissé]\nDjibril Cissé (] ; born 12 August 1981) is a French footballer who plays for Swiss club Yverdon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q715cf6a608",
  "kind": "yes/no",
  "text": "Claim: Prominent Danish Tibetologist Per Kjeld Sørensen is a professor of Central Asian Studies at the same Berlin based institution which Josef A. Käs is a professor at. This college was founded by the imperial forces that defeated the Hussite troops at the The Battle of Brüx.\n\nPassages:\n\n[Josef A. Käs]\nHe is a Professor at Leipzig University.\n\n[Battle of Brüx]\nThe Hussite troops, led by Jan Želivský, were defeated by the Catholic Imperial forces of Frederick I of Saxony.\n\n[Per K. Sørensen]\nPer Kjeld Sørensen (born 18 December 1950) is a prominent Danish Tibetologist who specialises in Tibetan and Himalayan history, literature and culture.\n\n[Leipzig University]\nThe university was founded on December 2, 1409 by Frederick I, Elector of Saxony and his brother William II, Margrave of Meissen, and originally comprised the four scholastic faculties.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qad12d9d99c",
  "kind": "yes/no",
  "text": "Claim: The Austrian village, population 246, that shares a name with a controversial German Pilsner or pale lager is 33km north from Salzburg.\n\nPassages:\n\n[Fucking, Austria]\nThe village is 33 km north of Salzburg, 4 km east of the Inn river, which forms the German border.\n\n[Fucking Hell]\nFucking Hell is a German Pilsner or pale lager with an alcohol content of 4.9%. The beer's name was initially controversial.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q14d6d458a0",
  "kind": "yes/no",
  "text": "Post: @JessicaChung13 4) never take a first hour class",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q6385f797fb",
  "kind": "yes/no",
  "text": "Claim: Mara Santangelo is the former professional tennis player from Italy. Not the player that won the singles title in the 1974 John Player Tournament.\n\nPassages:\n\n[Chris Evert]\nChristine Marie Evert (born December 21, 1954), known as Chris Evert Lloyd from 1979 to 1987, is a former World No. 1 professional tennis player from the United States.\n\n[1974 John Player Tournament]\nFirst-seeded Chris Evert won the singles title and earned £1,750 ($4,200) first-prize money.\n\n[Mara Santangelo]\nMara Santangelo (born 28 June 1981) is a former professional tennis player from Italy.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa146d8358b",
  "kind": "yes/no",
  "text": "Claim: Alfred Molina played Touchstone in the 2006 film of Shakespeare's As You Like It.\n\nPassages:\n\n[As You Like It (2006 film)]\nAs You Like It is a 2006 film written and directed by Kenneth Branagh, and based on the Shakespearean play of the same name. It stars Bryce Dallas Howard as Rosalind, David Oyelowo as Orlando De Boys, Romola Garai as Celia, Adrian Lester as Oliver De Boys, Alfred Molina as Touchstone, Kevin Kline as Jaques, Janet McTeer as Audrey, and Brian Blessed as Duke Frederick and his brother Duke Senior.\n\n[Touchstone (As You Like It)]\nTouchstone is a fictional character in Shakespeare's play \"As You Like It\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc17f17e51f",
  "kind": "yes/no",
  "text": "Claim: The Mikoyan design bureau developed the planes operated, by the main unit based at the 22nd Air Base, of the Polish Air Force.\n\nPassages:\n\n[22nd Air Base]\nThe main unit based there is the 41st Air Tactical Squadron flying MiG-29 fighters.\n\n[41st Tactical Squadron]\n41st Tactical Squadron (known as 41. The squadron operates Mikoyan MiG-29 jet fighters acquired from the German Luftwaffe.\n\n[Mikoyan MiG-29]\nThe Mikoyan MiG-29 (Russian: Микоян МиГ-29 ; NATO reporting name: Fulcrum) is a twin-engine jet fighter aircraft designed in the Soviet Union. Developed by the Mikoyan design bureau as an air superiority fighter during the 1970s, the MiG-29, along with the larger Sukhoi Su-27, was developed to counter new American fighters such as the McDonnell Douglas F-15 Eagle, and the General Dynamics F-16 Fighting Falcon.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4a19c846ef",
  "kind": "yes/no",
  "text": "Claim: Along with the New York Islanders and the New York Rangers, the New Jersey Devils NFL franchise is popular in the New York metropolitan area.\n\nPassages:\n\n[1974–75 New York Islanders season]\nIn the first round of the playoffs, New York defeated the New York Rangers in three games to advance to the Quarter-finals, where the team defeated the Pittsburgh Penguins in seven games, after they had lost the first three.\n\n[New York Rangers]\nThe Rangers are one of three NHL franchises in the New York metropolitan area, along with the New Jersey Devils and New York Islanders.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5492be6e77",
  "kind": "yes/no",
  "text": "Claim: Robert Pingeton was hired and fired in April 2010 to replace former head coach Cindy Stein of the team that lost in the second round of the SEC Women's Tournament to Auburn.\n\nPassages:\n\n[2015–16 Missouri Tigers women's basketball team]\nThe Tigers were led by sixth year head coach Robin Pingeton. They play their games at Mizzou Arena and are members of the Southeastern Conference.\n\n[Robin Pingeton]\nRobin Pingeton (born July 9, 1968) is the head coach of the University of Missouri's women's basketball team. She was hired in April 2010 to replace former head coach Cindy Stein.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe9cca26646",
  "kind": "yes/no",
  "text": "Tweet: getting ready is better than going out",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q997e2e75ce",
  "kind": "yes/no",
  "text": "Claim: The movie co-directed by Lee Unkrich and \"Mary Poppins\" are not both made by the same company.\n\nPassages:\n\n[Lee Unkrich]\nAfter co-directing \"Monsters, Inc.\" and \"Finding Nemo\", Unkrich made his solo directorial debut with \"Toy Story 3\", for which he won the Academy Award for Best Animated Film in 2011.\n\n[Monsters, Inc.]\nMonsters, Inc. is a 2001 American computer-animated comedy film produced by Pixar Animation Studios and distributed by Walt Disney Pictures.\n\n[Mary Poppins (film)]\nMary Poppins is a 1964 American musical-fantasy film directed by Robert Stevenson and produced by Walt Disney, with songs written and composed by the Sherman Brothers.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9c1676e0d4",
  "kind": "yes/no",
  "text": "Claim: Adunis was born before another writer. This writer considers Esther Belin to be one of his favorite Syrian writers.\n\nPassages:\n\n[Adunis]\nAli Ahmad Said Esber , romanised: \"ʿAlī Aḥmad Saʿīd 'Isbar\" (born 1 January 1930), also known by the pen name Adonis or Adunis (Arabic: أدونيس, \"Adūnīs\") , is a Syrian poet, essayist and translator who is considered one of the most influential and dominant Arab poets of the modern era.\n\n[Sherman Alexie]\nSherman Joseph Alexie, Jr. (born October 7, 1966) is a Spokane-Coeur d'Alene-American novelist, short story writer, poet, and filmmaker.\n\n[Esther Belin]\nSherman Alexie considers Belin to be one of his favorite Native writers.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q21bb4e7189",
  "kind": "yes/no",
  "text": "Claim: The former Los Angeles Lakers majority owner Vlade Divac is the father of Jeanie Marie Buss.\n\nPassages:\n\n[Jeanie Buss]\nBuss is a daughter of Jerry Buss, a real estate investor who later owned the Lakers and other sports businesses.\n\n[Jerry Buss]\nGerald Hatten Buss (January 27, 1933 – February 18, 2013) was an American businessman, investor, chemist, and philanthropist. He was the majority owner of the Los Angeles Lakers professional basketball team in the National Basketball Association (NBA), winning 10 league championships that were highlighted by the team's Showtime era during the 1980s.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q825a18b3a7",
  "kind": "yes/no",
  "text": "Claim: Asimov's Science Fiction and The Christian Science Sentinel are both magazines.\n\nPassages:\n\n[Christian Science Sentinel]\nThe Christian Science Sentinel (originally the \"Christian Science Weekly\") is a magazine published by the Christian Science Publishing Society based in Boston, Massachusetts.\n\n[Asimov's Science Fiction]\nAsimov's Science Fiction (ISSN 1065-2698) is an American science fiction magazine which publishes science fiction and fantasy named after science fiction author Isaac Asimov.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q28d4df8496",
  "kind": "yes/no",
  "text": "Claim: The film starring Kelly Preston was a comedy film directed by production designer and director Robert W. \"Bo\" Welch III.\n\nPassages:\n\n[Kelly Preston]\nShe also starred in the films \"The Cat in the Hat\", \"Old Dogs\", and \"Broken Bridges\".\n\n[Bo Welch]\nRobert W. \"Bo\" Welch III (born November 30, 1951) is an American production designer and director.\n\n[The Cat in the Hat (film)]\nDr. Seuss' The Cat in the Hat is a 2003 American family comedy film directed by Bo Welch.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa595ae9e56",
  "kind": "yes/no",
  "text": "Claim: Between Anaïs Nin and Odysseas Elytis, Odysseas Elytis was awarded the Nobel Prize in Literature.\n\nPassages:\n\n[Odysseas Elytis]\nOdysseas Elytis (Greek: Οδυσσέας Ελύτης , ] , pen name of Odysseas Alepoudellis, Greek: Οδυσσέας Αλεπουδέλλης ; 2 November 1911 – 18 March 1996) was regarded as a major exponent of romantic modernism in Greece and the world. In 1979 he was awarded the Nobel Prize in Literature.\n\n[Anaïs Nin]\nAnaïs Nin (] ; born Angela Anaïs Juana Antolina Rosa Edelmira Nin y Culmell; February 21, 1903 – January 14, 1977) was an essayist and memoirist born to Cuban parents in France, where she was also raised.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q523001f2cf",
  "kind": "yes/no",
  "text": "Claim: The class Jodie Esquibel competes professionally in belongs to mixed martial arts.\n\nPassages:\n\n[Liz McCarthy (fighter)]\nLiz McCarthy is an American mixed martial artist who competes in the Atomweight division.\n\n[Jodie Esquibel]\nJodie Esquibel is an American mixed martial artist who competes in the Atomweight division.\n\n[Atomweight (MMA)]\nThe atomweight division in mixed martial arts generally refers to competitors weighing at or less than 105 lb .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q12cb6781b8",
  "kind": "yes/no",
  "text": "Text: Waiting for little one to fall asleep so o can sneak upstairs and get my hot water bottle.\n\nShe's sitting up in bed practicing her nodding 🙈",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q8e11fda691",
  "kind": "yes/no",
  "text": "Claim: Hariharan Pillai Happy Aanu contains music by the arranger Stephen Devassy from Kerala.\n\nPassages:\n\n[Stephen Devassy]\nStephen Devassy (Malayalam:സ്റ്റീഫൻ ദേവസ്സി, born 23 February 1981) is a musician hailing from Palakkad, Kerala.\n\n[Hariharan Pillai Happy Aanu]\nThis was Viswanathan's debut film as a director and the debut music directorial venture of renowned pianist and arranger, Stephen Devassy.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf98a4ed98e",
  "kind": "yes/no",
  "text": "Claim: Gina Bramhill was born in an Italian village. The 2011 population of the unitary authority area that includes this village was 167,446.\n\nPassages:\n\n[Gina Bramhill]\nGina Bramhill was born in Eastoft, where she grew up on a farm.\n\n[North Lincolnshire]\nThe population of the Unitary Authority at the 2011 census was 167,446.\n\n[Eastoft]\nEastoft is a village and civil parish in North Lincolnshire, England.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc622299a25",
  "kind": "yes/no",
  "text": "Claim: The birthdate of the American actress, television producer and director, singer/songwriter and author, who briefly appeared in Kids Incorporated and starred in Ghost Whisperer is February 21, 1979.\n\nPassages:\n\n[Ghost Whisperer (video game)]\nGhost Whisperer is a casual hidden-object mystery adventure game developed by Legacy Games for Microsoft Windows and Mac OS. The game is based on the CBS supernatural television drama Ghost Whisperer starring Melinda Gordon (Jennifer Love Hewitt).\n\n[Jennifer Love Hewitt]\nJennifer Love Hewitt (born February 21, 1979) is an American actress, television producer and director, singer/songwriter and author. Hewitt began her acting career as a child by appearing in television commercials and the Disney Channel series \"Kids Incorporated\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7887e78557",
  "kind": "yes/no",
  "text": "Text: Humans are the only animal that can’t tell fantasy from reality",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe1c2e83ef2",
  "kind": "yes/no",
  "text": "Claim: Acoustic is an EP by an American rock band. Mathew James \"Matt\" Willis has more top 20 singles than that band.\n\nPassages:\n\n[Bayside (band)]\nBayside is an American rock band from New York City, formed in 2000, currently consisting of lead vocalist/guitarist Anthony Raneri, lead guitarist Jack O'Shea, bassist Nick Ghanbarian, and drummer Chris Guglielmo.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted. Willis released his debut solo album \"Don't Let It Go to Waste\" on 20 November 2006, which included three top 20 singles.\n\n[Acoustic (Bayside EP)]\nAcoustic is an EP by American rock band Bayside, released on February 28, 2006.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9dbb17ee91",
  "kind": "yes/no",
  "text": "Claim: Bill Boyd is the chairman of the appliance company that operates the place Thomas Eje made his debut at.\n\nPassages:\n\n[Boyd Gaming]\nThe company continues to be run by founder Sam Boyd's family under the management of Sam's son, Bill Boyd (born 1931), who currently serves as the company's executive chairman after retiring as CEO in January 2008.\n\n[Thomas Eje]\nOn November 15, 2006 he made his Las Vegas debut at the Suncoast Casino, under the moniker \"Tom Dane\".\n\n[Suncoast Hotel and Casino]\nIt is owned and operated by Boyd Gaming.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
