# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-005.json

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
  "qid": "q3ca4a03677",
  "kind": "yes/no",
  "text": "Claim: To Be Human is a song for the soundtrack to a 2017 superhero film . An actor that was in the film (2017 film) also performed in Anomalisa after the premier of Fargo.\n\nPassages:\n\n[David Thewlis]\nHe has also done voice work in the films \"James and the Giant Peach\" (1996), \"The Miracle Maker\" (2000), and \"Anomalisa\" (2015).\n\n[Wonder Woman (2017 film)]\nThe film is directed by Patty Jenkins, with a screenplay by Allan Heinberg, from a story by Heinberg, Zack Snyder, and Jason Fuchs, and stars Gal Gadot, Chris Pine, Robin Wright, Danny Huston, David Thewlis, Connie Nielsen, and Elena Anaya.\n\n[Fargo (TV series)]\nThe series premiered on April 15, 2014, on FX, and follows an anthology format, with each season set in a different era, and with a different story and mostly new characters and cast, although there is minor overlap.\n\n[To Be Human]\n\"To Be Human\" is a song recorded by Australian singer Sia featuring English singer Labrinth for the soundtrack to the 2017 superhero film \"Wonder Woman\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q18ab8d22ad",
  "kind": "yes/no",
  "text": "Claim: Leigh Silverman was nominated for the 2014 Tony Award, Best Direction for a musical based on the short story The Ugliest Pilgrim.\n\nPassages:\n\n[Leigh Silverman]\nLeigh Silverman is an American director for the stage, both Off-Broadway and on Broadway. She was nominated for the 2014 Tony Award, Best Direction of a Musical for the musical \"Violet\" and the 2008 Drama Desk Award, Outstanding Director of a Play for the play \"From Up Here\".\n\n[Violet (musical)]\nViolet is a musical with music by Jeanine Tesori and libretto by Brian Crawley based on the short story \"The Ugliest Pilgrim\" by Doris Betts.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q328f365595",
  "kind": "yes/no",
  "text": "Post: @goldfishbabe101 crispy all day every day over here ✌🏻",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qec659cf358",
  "kind": "yes/no",
  "text": "Claim: Vanessa Mesquita made the cover of a magazine established by Editora Abril.\n\nPassages:\n\n[Playboy (Brazil)]\nEstablished in 1975 by Editora Abril, it was only the fourth overall international version of the magazine, following Germany, Italy and France.\n\n[Vanessa Mesquita]\nAfter the program, Mesquita made the cover of Playboy (Brazil)",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb2afb94b77",
  "kind": "yes/no",
  "text": "Claim: Widewuto, a legendary ruler of the pagan Prussians, was believed to have died before the army of the Teutonic Knights launched crusade against the Prussian peoples.\n\nPassages:\n\n[Widewuto]\nWidewuto (also \"Viduutus\", \"Vidvutus\", \"Witowudi\", \"Waidewut\") was a legendary king of the pagan Prussians who ruled along with his elder brother, the high priest Bruteno in the 6th century AD. It is unclear whether the legend was authentically Prussian (i.e. recorded from Prussian mythology) or was created by Grunau (possibly inspired by Biblical Moses and Aaron), though Lithuanian researchers tend to support in its authenticity.\n\n[Prussian mythology]\nThe Prussian mythology was a polytheistic religion of the Old Prussians, indigenous peoples of Prussia before the Prussian Crusade waged by the Teutonic Knights. No sources document pagan religion before the forced Christianization in the 13th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf25c4fea30",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "IF ONLY PEOPLE WOULD RAKE THE FORESTS. #Debate2020",
   "The president seems to believe that merely removing leaves from forest floors would prevent forest fires."
  ]
 },
 {
  "qid": "qa197da95fd",
  "kind": "yes/no",
  "text": "Claim: A cabinet-making firm from Lancaster was found in 1730.\n\nPassages:\n\n[Richard Gillow]\nRichard Gillow (1733–1811) was an English architect and businessman from Lancaster. He was the son of the carpenter Robert Gillow, the founder of Gillows of Lancaster and London, a successful cabinet-making firm.\n\n[Gillows of Lancaster and London]\nIt was founded around in Lancaster in about 1730 by Robert Gillow (1704–1772).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q76d79b0f68",
  "kind": "yes/no",
  "text": "Claim: Anatoly Kashirov playa for the basketball club BC Dzūkija, located in Alytus, Lithuania.\n\nPassages:\n\n[BC Dzūkija]\nBC Dzūkija (Lithuanian: \"Krepšinio klubas Dzūkija\" ) is a basketball club located in Alytus, Lithuania.\n\n[Anatoly Kashirov]\nAnatoly Kashirov (born May 19, 1987) is a Russian professional basketball player for Dzūkija Alytus of the Lithuanian Basketball League.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3f21a7efd2",
  "kind": "yes/no",
  "text": "Claim: Pyne & Marles is co-hosted by Richard Marles and an Australian politician who has been the Labor member for the House of Representatives seat of Sturt since the election of 1993.\n\nPassages:\n\n[Pyne &amp; Marles]\nThe program is co-hosted by two serving frontbench MPs; Liberal minister Christopher Pyne and Labor shadow minister Richard Marles, without a journalist or moderator.\n\n[Christopher Pyne]\nChristopher Maurice Pyne (born 13 August 1967) is an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the 1993 election.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9cb2cf8bd1",
  "kind": "yes/no",
  "text": "Claim: The board game San Marco came did not come out first out of San Marco and About Time.\n\nPassages:\n\n[About Time (board game)]\nAbout Time is a general knowledge historical board game first seen on Series 5 of the BBC new-business reality show \"Dragon's Den\" on December 17, 2007.\n\n[San Marco (board game)]\nSan Marco is a 2001 designer board game by Alan R. Moon and Aaron Weissblum.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb25dc2608e",
  "kind": "yes/no",
  "text": "Claim: Former municipality Pizy merged with Aubonne in Switzerland.\n\nPassages:\n\n[Pizy]\nOn July 1, 2011 it was merged into Aubonne.\n\n[Aubonne]\nAubonne is a municipality in the district of Morges in the canton of Vaud in Switzerland.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe0c2504385",
  "kind": "yes/no",
  "text": "Tweet: @rickyberwick And you said Donald trump was racist 😑",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q3bc2db745e",
  "kind": "yes/no",
  "text": "Claim: The 1972 movie that featured the song \"I'll Wait\" from the album Soul Dancing and Air Bud are American comedy movies.\n\nPassages:\n\n[Air Bud]\nAir Bud is a 1997 American comedy film that sparked the franchise centered on the real-life dog, Buddy, a Golden Retriever.\n\n[Soul Dancing]\nThe song \"I'll Wait\" was featured in the 1994 Disney comedy \"Blank Check\".\n\n[Blank Check (film)]\nBlank Check is a 1994 American comedy film directed by Rupert Wainwright and starring Brian Bonsall, Karen Duffy, Miguel Ferrer, James Rebhorn, Tone Lōc, Jayne Atkinson and Michael Lerner.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qafa3c06805",
  "kind": "yes/no",
  "text": "Tweet: why are the olympics worried about athletes having too much sex when the curling teams don't even compete in the summer games",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q574d128e25",
  "kind": "yes/no",
  "text": "Post: Wishing all the birthday sex on @laurabora620 today 🎂 https://t.co/JtP0FCvo9R",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0651e917da",
  "kind": "yes/no",
  "text": "Tweet: @LittleBigPlanet Thanks for the update. No need to rush take your time :)",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q6be6ea7577",
  "kind": "yes/no",
  "text": "Claim: Seyi Adebanjo's identity, is a combination of masculinity and femininity or neither in gender expression.\n\nPassages:\n\n[Discwoman]\nDiscwoman is a New York based collective, booking agency, and event platform representing and showcasing female-identified (cis women, transwomen, and gender queer) talent in the electronic music community.\n\n[Seyi Adebanjo]\nSeyi Adebanjo is a genderfluid, queer MFA media artist, born in Nigeria and now resident in New York City.\n\n[Genderqueer]\nGenderqueer people may express a combination of masculinity and femininity, or neither, in their gender expression.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q243de2cf63",
  "kind": "yes/no",
  "text": "Tweet: back to school clothes shopping even tho school is online😁😁",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qdfdf3915d8",
  "kind": "yes/no",
  "text": "Claim: The population of the terminus of a train route in 2011 was 2,416. The Reynella railway station was part of this route.\n\nPassages:\n\n[Reynella railway station]\nReynella railway station was a railway station in Reynella, South Australia that was part of the Willunga railway line.\n\n[Willunga, South Australia]\nWillunga is a town south of Adelaide, South Australia in the City of Onkaparinga local government area 47 km from the Adelaide CBD. At the 2011 census , Willunga had a population of 2,416.\n\n[Willunga railway line]\nThe Willunga railway line ran through the southern Adelaide suburbs from Adelaide railway station to Willunga, over 45 km long (longer than the current Gawler line, 42.2 km ).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc0392979f5",
  "kind": "yes/no",
  "text": "Claim: The Colbert Report is a satirical Comedy Central program. The director of Splatter Theatre directed the host of The Colbert Report.\n\nPassages:\n\n[Stephen Colbert]\nHe is best known for hosting the satirical Comedy Central program \"The Colbert Report\" from 2005 to 2014, and hosting the CBS talk program \"The Late Show with Stephen Colbert\" beginning in September 2015.\n\n[Splatter Theatre]\nThe show was first performed at the Cabaret Metro, on October 31, 1987 and directed by Mick Napier.\n\n[Mick Napier]\nHe has directed Stephen Colbert, Tina Fey, Rachel Dratch, Horatio Sanz, Nia Vardalos, Andy Richter, Jeff Garlin, and David Sedaris, amongst others.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q58b199b410",
  "kind": "yes/no",
  "text": "Claim: Soloist Beth Quist can play the national musical instrument of Iran.\n\nPassages:\n\n[Beth Quist]\nShe has a 4-octave soprano voice, and plays piano, keyboards, santour (hammered dulcimer), dumbek, guitar, flute, and various other instruments.\n\n[Santoor]\nIt is the national musical instrument of Iran, and is also native to Jammu and Kashmir.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf12c48850b",
  "kind": "yes/no",
  "text": "Claim: The poet who wrote The Sovereignty of Good was born on 15 July 1919.\n\nPassages:\n\n[The Sovereignty of Good]\nThe Sovereignty of Good is a book of moral philosophy by Iris Murdoch.\n\n[Iris Murdoch]\nDame Jean Iris Murdoch ( ; 15 July 1919 – 8 February 1999) was an Anglo-Irish novelist and philosopher, best known for her novels about good and evil, sexual relationships, morality, and the power of the unconscious.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf390d6d14d",
  "kind": "yes/no",
  "text": "Claim: The namesake of Fort Davis, Alaska died in 1879.\n\nPassages:\n\n[Jefferson C. Davis]\nJefferson Columbus Davis (March 2, 1828 – November 30, 1879) was a regular officer of the United States Army during the American Civil War, known for the similarity of his name to Confederate President Jefferson Davis and for his killing of a superior officer in 1862.\n\n[Fort Davis, Alaska]\nIt was named for General Jefferson C. Davis, the military commander of Alaska from 1868 to 1870.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6eef4bdd38",
  "kind": "yes/no",
  "text": "Claim: The director of Daughters of Mara's first album is the son of the producer who worked for the group that evolved from The Iveys. Best! (Jellyfish album) which was released in 1993, did a live cover of a song from this other group.\n\nPassages:\n\n[Badfinger]\nThe band evolved from an earlier group called The Iveys that was formed in 1961 by Ham, Ron Griffiths and David \"Dai\" Jenkins in Swansea, Wales.\n\n[Best! (Jellyfish album)]\nThe song \"No Matter What\" is a live cover of a Badfinger song.\n\n[Daughters of Mara]\nDaughters Of Mara's first album, I Am Destroyer, was produced by Garth Richardson (Mudvayne, Rage Against The Machine) and was released on Virgin Records.\n\n[Garth Richardson]\nHe is the son of Canadian music producer Jack Richardson (whose credits include Alice Cooper, The Guess Who, Badfinger and Poco).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q67ae1a7a62",
  "kind": "yes/no",
  "text": "Claim: Neither the director of Nina (2016 film) or George Archainbaud are American.\n\nPassages:\n\n[Nina (2016 film)]\nNina is an American biographical film written and directed by Cynthia Mort.\n\n[Cynthia Mort]\nCynthia Mort (born June 18, 1956) is an American director, screenwriter, and producer.\n\n[George Archainbaud]\nGeorge Archainbaud (May 7, 1890 – February 20, 1959) was a French-born American film and television director.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfc45a99f8f",
  "kind": "yes/no",
  "text": "Post: Every time I get a symptom I strongly associate with pregnancy I also get my brain going through all the shit that happened around that to deal with as well as said symptom.\n\nBirth trauma, leaving us to deal with 100% tongue tied baby untreated, the general no support of lockdown",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q4890b966e3",
  "kind": "yes/no",
  "text": "Tweet: So nice of my family to decide that I’m hosting a Mother’s Day brunch for everyone at my house. https://t.co/DWZI9ltALK",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qc546e7f176",
  "kind": "yes/no",
  "text": "Claim: The documentary film Volcanic Sprint was released first then Tar Creek .\n\nPassages:\n\n[Tar Creek (film)]\nTar Creek is a 2009 feature-length environmental documentary about the Tar Creek Superfund Site, which at one time was considered the worst environmental disaster in the United States.\n\n[Volcanic Sprint]\nVolcanic Sprint is a 2007 documentary film produced by Steve Dorst and Dan Evans about a grueling mountain race in Africa and the mostly local competitors who compete against tough odds to overcome dire poverty.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qcd2c236829",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "My life priorities have changed",
   "My life has gone from ‘drive it like you stole it’ to ‘drive it like your toddler needs the toilet’."
  ]
 },
 {
  "qid": "qca207e0b7a",
  "kind": "yes/no",
  "text": "Claim: Sam Calagione is the Welsh founder and head of a brewing company based in Milton, Delaware.\n\nPassages:\n\n[Brew Masters]\nThe show focused on Sam Calagione, the founder and head of Dogfish Head Brewery in Milton, Delaware, and his staff as they searched the world for new, ancient, and imaginative inspirations for beers.\n\n[Dogfish Head Brewery]\nDogfish Head Brewery is a brewing company based in Milton, Delaware founded by Sam Calagione.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q59d04065bd",
  "kind": "yes/no",
  "text": "Claim: The musician that plays the tenor sax solo on the Great White song, \"Gone with the Wind\", is a member of a band inducted into the Rock and Roll Hall of Fame in 2014.\n\nPassages:\n\n[Sail Away (Great White album)]\nClarence Clemons of the E Street Band plays the sax solo on \"Gone with the Wind\".\n\n[E Street Band]\nThe band was inducted into the Rock and Roll Hall of Fame in 2014.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2f68ec038d",
  "kind": "yes/no",
  "text": "Claim: The producer of Back to the World (Street Dogs album), is the Executive Vice President of A&R at Capitol Records. The Welsh singer who was played on WWBZ (103.5 FM, \"The Blaze\") with Whitney and Elton, is not.\n\nPassages:\n\n[Rod Stewart]\nSir Roderick David \"Rod\" Stewart, {'1': \", '2': \", '3': \", '4': \"} (born 10 January 1945) is a British rock singer and songwriter.\n\n[Back to the World (Street Dogs album)]\nThe album was produced by Nate Albert, formerly of The Mighty Mighty Bosstones.\n\n[WWBZ (defunct)]\nOn March 29, the sounds of Whitney, Rod and Elton gave way to 24 hours of \"Rock Rock ('til you drop)\" by Def Leppard.\n\n[Nate Albert]\nNate Albert (born 1970) is an American music executive, songwriter, producer and guitar player. He is currently the Executive Vice President of A&R at Capitol Records a division of Universal Music Group.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6cfc2c66cc",
  "kind": "yes/no",
  "text": "Claim: Lance Stephenson of the Indiana Pacers college basketball team plays his home games at Bankers Life Fieldhouse.\n\nPassages:\n\n[Lance Stephenson]\nLance Stephenson Jr. (born September 5, 1990) is an American professional basketball player for the Indiana Pacers of the National Basketball Association (NBA).\n\n[Indiana Pacers]\nThey play their home games at Bankers Life Fieldhouse.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qca6bb60f7b",
  "kind": "yes/no",
  "text": "Claim: Masakatsu Ueda is a MMA fighter who is a blue belt under the Korean martial artist who teaches shoot wrestling and jiu-jitsu.\n\nPassages:\n\n[Masakatsu Ueda]\nHe is a blue belt in Brazilian Jiu-Jitsu under Yuki Nakai.\n\n[Yuki Nakai]\nYuki Nakai (中井祐樹 , Nakai Yūki ) is a retired Japanese mixed martial artist and Shooter. He currently teaches shoot wrestling and jiu-jitsu, and is the president of the Japanese Confederation of Jiu-Jitsu.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5bf57d494f",
  "kind": "yes/no",
  "text": "Text: That was the most mentally draining match I've ever been at. I wish the outcome was different, but I am still so proud of you @SunderlandAFC. My first match at Wembley with my big boy ❤️❤️",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q5e0e6503ea",
  "kind": "yes/no",
  "text": "Post: AS SHE SHOULD https://t.co/v1p2hHIC1i",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd912f75861",
  "kind": "yes/no",
  "text": "Claim: The university at which Barrie Ciliberti was never a professor is located at Prince George's County, Maryland.\n\nPassages:\n\n[University of Maryland University College]\nThe University of Maryland University College (UMUC) is an American public not-for-profit university located in Adelphi in Prince George's County, Maryland in the United States.\n\n[Barrie Ciliberti]\nBarrie Ciliberti was born in Philadelphia, Pennsylvania, is a University of Maryland University College professor and former Republican legislator in the Maryland House of Delegates.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7fb0c8ade3",
  "kind": "yes/no",
  "text": "Claim: \"Your Love Had Taken Me That High\" is a song recorded by a Memphis singer that received a string of Country Music Association awards for duets with Loretta Lynn.\n\nPassages:\n\n[Conway Twitty]\nConway Twitty (born Harold Lloyd Jenkins; September 1, 1933 – June 5, 1993) was an American country music singer. From 1971 to 1976, Twitty received a string of Country Music Association awards for duets with Loretta Lynn.\n\n[Your Love Had Taken Me That High]\n\"Your Love Had Taken Me That High\" is a song written by Jack Dunham and Galen Raye, and recorded by American country music artist Conway Twitty.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q243e8546c0",
  "kind": "yes/no",
  "text": "Claim: The author of the 1995 novel Mrs. Ted Bliss and Anne Lamott are not both non-fiction writers.\n\nPassages:\n\n[Anne Lamott]\nAnne Lamott (born April 10, 1954) is an American novelist and non-fiction writer.\n\n[Mrs. Ted Bliss]\nMrs. Ted Bliss is a 1995 novel by American author Stanley Elkin, published by Hyperion Books.\n\n[Stanley Elkin]\nStanley Lawrence Elkin (May 11, 1930 – May 31, 1995) was an American novelist, short story writer, and essayist. His extravagant, satirical fiction revolves around American consumerism, popular culture, and male-female relation between each other.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q27f31538ca",
  "kind": "yes/no",
  "text": "Claim: There are top three sections for the hockey meeting JC Lipon placed 91st overall in. Of the top three, the one who is both a American professional ice hockey forward and an alternate captain of the Colorado Avalanche organization of the National Hockey League is Nathan MacKinnon.\n\nPassages:\n\n[2013 NHL Entry Draft]\nThe 2013 NHL Entry Draft was the 51st NHL Entry Draft. The top three selections were Nathan MacKinnon, Aleksander Barkov Jr. and Jonathan Drouin.\n\n[JC Lipon]\nLipon was selected by the Winnipeg Jets in the third round (91st overall) of the 2013 NHL Entry Draft.\n\n[Nathan MacKinnon]\nNathan MacKinnon (born September 1, 1995) is a Canadian professional ice hockey forward, an alternate captain of the Colorado Avalanche organization of the National Hockey League (NHL).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4137ab78cf",
  "kind": "yes/no",
  "text": "Claim: The logo of the American athletic shoe and clothing manufacturer who trademarked the slogan coined by Dan Wieden has made $26 billion in profit. Utah-born Dan Wieden co-founded Wieden+Kennedy.\n\nPassages:\n\n[Swoosh]\nThe Swoosh is the logo of American athletic shoe and clothing manufacturer Nike, Inc. Today, it has become one of the most recognizable brand logos in the world, and the most profitable, having a worth of $26 billion alone.\n\n[Just Do It]\nJust Do It (stylized as JUST DO IT.) is a trademark of shoe company Nike, and one of the core components of Nike's brand.\n\n[Dan Wieden]\nDan Wieden (born 1945) Pronounced \"Why-den,\" is an American advertising executive who co-founded Wieden+Kennedy and coined the Nike tagline \"Just Do It.\"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qbd3cb87dd9",
  "kind": "yes/no",
  "text": "Claim: The novelist Peter Francis Straub has received Postscripts. The author of Hundred Thousand Billion Poems has not received the same award.\n\nPassages:\n\n[Peter Straub]\nPeter Francis Straub (born March 2, 1943) is an American novelist and poet. His horror fiction has received numerous literary honors such as the Bram Stoker Award, World Fantasy Award, and International Horror Guild Award.\n\n[Raymond Queneau]\nRaymond Queneau (] ; 21 February 1903 – 25 October 1976) was a French novelist, poet, critic, editor and co-founder and president of Oulipo (\"Ouvroir de littérature potentielle\"), notable for his wit and cynical humour.\n\n[Hundred Thousand Billion Poems]\nA Hundred Thousand Billion Poems or One hundred million million poems (original French title: \"Cent mille milliards de poèmes\") is a book by Raymond Queneau, published in 1961.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1c661c014a",
  "kind": "yes/no",
  "text": "Text: At least I'm used to this side effect from my infusion, and I'm very grateful that I'm not experiencing any of that full body pain I had after my last infusion. The IV steroids must be working!! And tomorrow is day one of a steroid pack",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q9ef0749157",
  "kind": "yes/no",
  "text": "Claim: Royal Navy Captain Wilhelm Batz shot down 46 of one type of aircraft, of which 36,183 were made during World War 2.\n\nPassages:\n\n[Wilhelm Batz]\n234 of these victories were achieved over the Eastern Front, including at least 46 Il-2 Sturmoviks, but he did claim three victories, including one four-engine bomber against the United States Army Air Forces (USAAF) over the Ploieşti oil fields.\n\n[Ilyushin Il-2]\nWith 36,183 units of the Il-2 produced during the war, and in combination with its successor, the Ilyushin Il-10, a total of 42,330 were built, making it the single most produced military aircraft design in aviation history, as well as one of the most produced piloted aircraft in history along with the American postwar civilian Cessna 172 and the Soviet Union's own then-contemporary Polikarpov Po-2 \"Kukuruznik\" multipurpose biplane.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5b51f9e51c",
  "kind": "yes/no",
  "text": "Claim: The genre of music shared, by a vocalist from Napalm Death who made a guest appearance on Leng Tch'e's Hypomaniac, and Jens Kidman is extreme metal\n\nPassages:\n\n[Jens Kidman]\nJens Kidman (born 8 June 1966) is a Swedish metal vocalist.\n\n[Hypomanic (album)]\nA video was made for the song \"Totalitarian\" on YouTube , featuring a guest appearance by Barney Greenway of Napalm Death.\n\n[Barney Greenway]\nMark Andrew \"Barney\" Greenway (born 13 July 1969) is a British extreme metal vocalist, who has been a member of Napalm Death, Extreme Noise Terror, and Benediction.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5a6e1ce06b",
  "kind": "yes/no",
  "text": "Claim: Kristina Ceyton and Rahul Bose produced the debut film of the director, The Nightengale (2017 film).\n\nPassages:\n\n[The Babadook]\nThe Babadook is a 2014 Australian psychological horror film written and directed by Jennifer Kent in her directorial debut, and produced by Kristina Ceyton and Kristian Moliere.\n\n[Jennifer Kent]\nJennifer Kent is an Australian actress, writer and director, best known for her horror film \"The Babadook\" (2014), which was her directorial debut.\n\n[The Nightingale (2017 film)]\nThe Nightingale is an upcoming Australian period thriller film written and directed by Jennifer Kent.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6a91d50c79",
  "kind": "yes/no",
  "text": "Claim: Rainer Dart is an Irish crime author. So is the writer of The Celestial Plot.\n\nPassages:\n\n[The Celestial Plot]\nThe Celestial Plot (Spanish: \"La trama celeste\" ) is a book by Adolfo Bioy Casares.\n\n[Adolfo Bioy Casares]\nAdolfo Bioy Casares (] ; September 15, 1914 – March 8, 1999) was an Argentine fiction writer, journalist, and translator.\n\n[Iris Rainer Dart]\nIris Rainer Dart (born March 3, 1944) is an American author and playwright for television and the stage.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q41cb8f7342",
  "kind": "yes/no",
  "text": "Claim: A star of The Great White Hype played General Pushkin in a Bond Film. That film starred Timothy Dalton as the politician in which the fictional organization SPECTRE is featured in.\n\nPassages:\n\n[John Rhys-Davies]\nHe also played Agent Michael Malone in the 1993 remake of the 1950s television series \"The Untouchables\", Pilot Vasco Rodrigues in the mini-series \"Shōgun\", Professor Maximillian Arturo in \"Sliders\", King Richard I in \"Robin of Sherwood\", General Leonid Pushkin in the James Bond film \"The Living Daylights\", and Macro in \"I, Claudius\".\n\n[SPECTRE]\nSPECTRE (SPecial Executive for Counterintelligence, Terrorism, Revenge and Extortion) is a fictional organisation featured in the James Bond novels by Ian Fleming, the films based on those novels, and James Bond video games.\n\n[The Great White Hype]\nIt stars Samuel L. Jackson, Peter Berg, Damon Wayans, Jeff Goldblum, Jon Lovitz, Cheech Marin, John Rhys-Davies, Salli Richardson and Jamie Foxx.\n\n[The Living Daylights]\nThe Living Daylights (1987) is the fifteenth entry in the \"James Bond\" film series and the first to star Timothy Dalton as the fictional MI6 agent James Bond.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qde711aace5",
  "kind": "yes/no",
  "text": "Claim: Red Velvet was formed by the largest entertainment company in South Korea.\n\nPassages:\n\n[Red Velvet discography]\nThe discography of the South Korean girl group Red Velvet consists of one studio album, five extended plays, and twelve singles. Red Velvet was formed by the Korean entertainment company S.M. Entertainment in 2014, and consists of five members.\n\n[S.M. Entertainment]\nIt is currently one of the largest entertainment companies in South Korea.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd87f6affc2",
  "kind": "yes/no",
  "text": "Claim: The first major improved highway is located in Wheeling, West Virginia.\n\nPassages:\n\n[Mount Echo, West Virginia]\nMount Echo is an unincorporated community in Ohio County, West Virginia, United States. It is part of the Wheeling, West Virginia Metropolitan Statistical Area.\n\n[National Road]\nThe National Road (also known as the Cumberland Road) was the first major improved highway in the United States built by the federal government.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 }
]
