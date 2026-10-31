# A46 replay label-noise blind read RSAS12-blind_read-6d20df33-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS12-blind_read-6d20df33-000.json

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
  "qid": "q9815067bb0",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I would go to Six Flags with you.",
   "@kashirenaii i would never go to six flags with u"
  ]
 },
 {
  "qid": "qe696bda7b9",
  "kind": "yes/no",
  "text": "Post: Sometimes I feel like all this effort is just like sticking diamond encrusted alloys on a knackered Corsa. I mean, shit is what it is at the end of the day.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qfea9da78ee",
  "kind": "yes/no",
  "text": "Claim: The star of War of the Satellites acted in The Terminator movie alongside actor John Daly.\n\nPassages:\n\n[War of the Satellites]\nThe film was produced and directed by Roger Corman and stars Richard Devon, Dick Miller and Susan Cabot.\n\n[Dick Miller]\nMiller's main roles have been in films such as \"Gremlins\", \"\", \"The Explorers\", \"Piranha\", \"The Howling\", \"A Bucket of Blood\", \"The Little Shop of Horrors\", \"Chopping Mall\", \"Night of the Creeps\", \"The Terminator\", \"The 'Burbs\" and \"Small Soldiers\".\n\n[The Terminator]\nIt stars Arnold Schwarzenegger as the Terminator, a cyborg assassin sent back in time from 2029 to 1984 to kill Sarah Connor (Linda Hamilton), whose son will one day become a savior against machines in a post-apocalyptic future.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q079e991ed9",
  "kind": "yes/no",
  "text": "Claim: Zachariah T. Woodall, born in early September 1849, was part of the military campaign started by the US Army in 1874 to remove natives.\n\nPassages:\n\n[Zachariah T. Woodall]\nZachariah T. Woodall (September 1849 – September 12, 1899) was a soldier in the U.S. Army who served with the 6th U.S. Cavalry during the Red River War, and later in the Spanish–American War.\n\n[Red River War]\nThe Red River War was a military campaign launched by the United States Army in 1874 to remove the Comanche, Kiowa, Southern Cheyenne, and Arapaho Native American tribes from the Southern Plains and forcibly relocate them to reservations in Indian Territory.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q09f7f1443f",
  "kind": "yes/no",
  "text": "Claim: Jack Kirby was the first illustrator for a comic book character later assigned to Carlo Pagulayan.\n\nPassages:\n\n[Hulk (comics)]\nThe Hulk is a fictional superhero appearing in American comic books published by Marvel Comics. Created by writer Stan Lee and artist Jack Kirby, the character first appeared in the debut issue of \"The Incredible Hulk\" (May 1962).\n\n[Carlo Pagulayan]\nCarlo Pagulayan (born June 24, 1978) is a freelance Filipino comic book artist. He has since had assignments from a few publishers, including \"Elektra\" and \"The Incredible Hulk\" for Marvel Comics.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q39472179ba",
  "kind": "yes/no",
  "text": "Tweet: Me: You know, for someone with chronic anxiety I think I'm dealing with this pandemic quite well.\n\nAlso me: Wow, I forgot how good a freshly shaved undercut feels!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qf31417579d",
  "kind": "yes/no",
  "text": "Claim: Jordan's Furniture is a furniture retailer with a location in an enclosed shopping mall on the north side of Interstate 295 near the junction with Interstate 40.\n\nPassages:\n\n[Jordan's Furniture]\nJordan's Furniture is a furniture retailer in New England. There are currently seven locations - in Reading, Avon, Taunton, Natick, Massachusetts, Nashua, New Hampshire, Warwick Mall in Warwick, Rhode Island, and New Haven, Connecticut.\n\n[Warwick Mall]\nWarwick Mall is an enclosed shopping mall in Warwick, Rhode Island, on the north side of Interstate 295 near the junction with Interstate 95.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe7fbdddd6e",
  "kind": "yes/no",
  "text": "Text: it’s been 20 hours and i want another chai latte with pumpkin cold foam i can’t afford this!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd10be012dc",
  "kind": "yes/no",
  "text": "Post: All I needed was some Lady Gaga and some Nicki on there and I think I could just use my Spotify Wrapped as a coming out post 💅\n(Also was in the top 0.5% of Conan Gray’s fans, not to flex) https://t.co/tpREOJgevj",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q100c909004",
  "kind": "yes/no",
  "text": "Claim: Pieter 'Piet' Klijnveld, was a Dutch tax accountant who started a practice that after several mergers would grow into KPMG, one of the Big Four auditors along with Deloitte, Ernst & Young (EY), and PricewaterhouseCoopers (PwC).\n\nPassages:\n\n[Piet Klijnveld]\nPieter 'Piet' Klijnveld (16 August 1874 – 9 February 1945) was a Dutch accountant who started a practice that after several mergers would grow into the international accounting firm KPMG.\n\n[KPMG]\nKPMG is a professional service company and one of the Big Four auditors, along with Deloitte, Ernst & Young (EY), and PricewaterhouseCoopers (PwC).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8f1131e282",
  "kind": "yes/no",
  "text": "Claim: A video game published by Sierra Entertainment, includes a figure who's mystery is the core of the series. SAS: Secure Tomorrow utilizes Jupiter EX engine similar, if not identical to the one in that game.\n\nPassages:\n\n[SAS: Secure Tomorrow]\nThe game utilizes Jupiter EX engine, similar, if not identical to the one in F.E.A.R..\n\n[Alma Wade]\nAlma Wade is a major antagonist and key figure in the \"F.E.A.R.\" series of first-person shooter horror video games by Monolith Productions, introduced in \"F.E.A.R.\" in 2005. The mystery of Alma is the very core of the series.\n\n[F.E.A.R.]\nF.E.A.R. First Encounter Assault Recon is a survival horror first-person shooter video game developed by Monolith Productions and published by Sierra Entertainment.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf1696e0835",
  "kind": "yes/no",
  "text": "Claim: Robert Bozic fought and lost to a professional boxer with the nickname, Easton Assassin in 1977.\n\nPassages:\n\n[Bob Bozic]\nRobert Bozic (born 1950) was a professional heavyweight boxer from Toronto, Canada between 1970-77. He fought and lost to Larry Holmes in Madison Square Garden in 1973.\n\n[Larry Holmes]\nLarry Holmes (born November 3, 1949) is an American former professional boxer who competed from 1973 to 2002. He grew up in Easton, Pennsylvania, which gave birth to his boxing nickname of the \"Easton Assassin\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qad69fb4217",
  "kind": "yes/no",
  "text": "Post: my bf took my off his lock screen which obvi means he’s cheating on me",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q0d2a07a7a7",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I agree, I want them too",
   "@adi_jord agreed, this is ridiculous, gotta cop a pair"
  ]
 },
 {
  "qid": "q2f3bdfaf5f",
  "kind": "yes/no",
  "text": "Claim: The film Mercy Malick is known for was inspired by a 1957 movie. It was directed by Jr..\n\nPassages:\n\n[Circle (2015 film)]\nIt was inspired by the 1957 drama \"12 Angry Men\" and was shot in 2014.\n\n[Mercy Malick]\nShe is best known for Mission Control, Major Crimes, Circle, and iZombie.\n\n[12 Angry Men (1957 film)]\nWritten and co-produced by Rose himself and directed by Sidney Lumet, this trial film tells the story of a jury made up of 12 men as they deliberate the guilt or acquittal of a defendant on the basis of reasonable doubt.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd098bfefe3",
  "kind": "yes/no",
  "text": "Claim: Harry Ransom served as the Chancellor of this institute from 1961 to 1971. This institute and the place where Steven J. Kachelmeier got his Ph.D. combine to have both a 2000 acre campus and over 216,000 students.\n\nPassages:\n\n[Steven J. Kachelmeier]\nDr. Kachelmeier received his B.B.A. from the University of New Mexico and his Ph.D. from the University of Florida.\n\n[University of Texas System]\nThe UT System is headquartered in Austin, and has a total enrollment of over 216,000 students (largest university system in Texas) and employs more than 87,000 faculty and staff.\n\n[Harry Ransom]\nHarry Huntt Ransom (November 22, 1908 – April 19, 1976) was a faculty member and administrator at the University of Texas, becoming the university's president in 1960, and ultimately served as the Chancellor of the University of Texas System from 1961 to 1971.\n\n[University of Florida]\nThe University of Florida (commonly referred to as Florida or UF) is an American public land-grant, sea-grant, and space-grant research university on a 2000 acre campus in Gainesville, Florida.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7effec3923",
  "kind": "yes/no",
  "text": "Claim: The youngest male model ever to participate in Seoul Fashion Week stars with Park Hae-jin and Kang So-ra ina tv series that last aired on July 8, 2014.\n\nPassages:\n\n[Lee Jong-suk]\nLee's breakout role was in \"School 2013\" (2012) and he is also well known for his roles in \"I Can Hear Your Voice\" (2013), \"Doctor Stranger\" (2014), \"Pinocchio\" (2014) and \"W\" (2016).\n\n[Doctor Stranger]\nIt aired on SBS from May 5 to July 8, 2014 on Mondays and Tuesdays at 21:55 for 20 episodes.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9ec0ae1eb3",
  "kind": "yes/no",
  "text": "Claim: Kitchen Stories is a 2003 Norwegian film by this director. This director has more creative titles than the director of Sword of Penitence.\n\nPassages:\n\n[Bent Hamer]\nBent Hamer (born 18 December 1956) is a film director, writer and producer, born in Sandefjord, Norway in 1956.\n\n[Sword of Penitence]\nSword of Penitence (Zange no yaiba: 懺悔の刃 ) is a 1927 Japanese silent film written and directed by Yasujirō Ozu.\n\n[Yasujirō Ozu]\nYasujirō Ozu (小津 安二郎 , Ozu Yasujirō , 12 December 1903 – 12 December 1963) was a Japanese film director and screenwriter.\n\n[Kitchen Stories]\nKitchen Stories (Norwegian: Salmer fra Kjøkkenet ) is a 2003 Norwegian film by Bent Hamer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3cef4ff08d",
  "kind": "yes/no",
  "text": "Claim: Peter Straub is a romance novelist. The author of The Playmaker is also a novelist.\n\nPassages:\n\n[Peter Straub]\nPeter Francis Straub (born March 2, 1943) is an American novelist and poet.\n\n[Thomas Keneally]\nThomas Michael Keneally, AO (born 7 October 1935) is a prolific Australian novelist, playwright, and essayist.\n\n[The Playmaker]\nThe Playmaker is a novel based in Australia written by the Australian author Thomas Keneally.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qed2d6c7714",
  "kind": "yes/no",
  "text": "Claim: The 2015 Austrian thriller film Jack tells the story of a serial killer who lived in 1994.\n\nPassages:\n\n[Jack (2015 film)]\nJack is a 2015 Austrian thriller film about serial killer Jack Unterweger, directed by Elisabeth Scharang.\n\n[Jack Unterweger]\nJohann \"Jack\" Unterweger (16 August 195029 June 1994) was an Austrian serial killer who murdered prostitutes in several countries.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf75a49e032",
  "kind": "yes/no",
  "text": "Claim: This Federation of Indian Airlines member is owned by Indian business conglomerate Wadia Group, formed in February 1969.\n\nPassages:\n\n[GoAir]\nGoAir is a low-cost carrier based in Mumbai, India. It is owned by the Indian business conglomerate Wadia Group.\n\n[Federation of Indian Airlines]\nThe Federation of Indian Airlines (FIA) is an airline industry body in India. Its members are Jet Airways, IndiGo, SpiceJet and GoAir.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qcff762d835",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Hailey convinced Tayler that putting a spoon in the microwave to scoop ice cream faster was a good idea",
   "we had to tell her it was a bad idea to put a spoon in the microwave"
  ]
 },
 {
  "qid": "q1c8ad346aa",
  "kind": "yes/no",
  "text": "Claim: The person who introduced the British opera Tragédie en musique was an Italian-born British composer, instrumentalist, and dancer. He produced music for the British opera Thesee.\n\nPassages:\n\n[Jean-Baptiste Lully]\nJean-Baptiste Lully (] ; born Giovanni Battista Lulli ] ; 28 November 1632 – 22 March 1687) was an Italian-born French composer, instrumentalist, and dancer who spent most of his life working in the court of Louis XIV of France.\n\n[Thésée]\nThésée (\"Theseus\") is a \"tragédie en musique\", an early type of French opera, in a prologue and five acts with music by Jean-Baptiste Lully and a libretto by Philippe Quinault based on Ovid's \"Metamorphoses\".\n\n[Tragédie en musique]\nTragédie en musique (Musical tragedy), also known as tragédie lyrique (French lyric tragedy), is a genre of French opera introduced by Jean-Baptiste Lully and used by his followers until the second half of the eighteenth century.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc08aad3e2d",
  "kind": "yes/no",
  "text": "Claim: The director of Dead & Buried, not this director, is known for his prolific work in the horror film genre. The comedy The Practice of Love was directed by her.\n\nPassages:\n\n[The Practice of Love]\nThe Practice of Love (German: \"Die Praxis der Liebe\" ) is a 1985 Austrian drama film written by and directed by Valie Export.\n\n[Dead &amp; Buried]\nDead & Buried is a 1981 science fiction horror film directed by Gary Sherman, starring Melody Anderson, Jack Albertson, and James Farentino.\n\n[Valie Export]\nHer artistic work includes video installations, body performances, expanded cinema, computer animations, photography, sculptures and publications covering contemporary arts.\n\n[Gary Sherman (director)]\nGary Sherman (born 1945), is an American film director, screenwriter, and producer from Chicago, Illinois. He is best known for his prolific work in the horror film genre, directing films such as \"Death Line, Dead & Buried\", and \"Poltergeist III\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q154c61b371",
  "kind": "yes/no",
  "text": "Post: ERROR: 404 https://t.co/xcNCMlnzrm",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q63facfbf2b",
  "kind": "yes/no",
  "text": "Claim: The American singer-songwriter known as \"the Caruso of Rock\", had hits such as \"Pretty One,\" and \"Uptown\". He recorded \"I Drove All Night\" in 1991, the year before his death. He recorded on the Monument Records label.\n\nPassages:\n\n[Roy Orbison]\nRoy Kelton Orbison (April 23, 1936 – December 6, 1988) was an American singer-songwriter known for his distinctive, impassioned voice, complex song structures, and dark emotional ballads.\n\n[Early Orbison]\nEarly Orbison is an album recorded by Roy Orbison on the Monument Records label at their studios in Hendersonville, Tennessee and released in 1964. Essentially a compilation of songs from his first two Monument albums, it is most noteworthy for containing \"Pretty One\", the \"B\" side of Orbison's second Monument single, \"Uptown\".\n\n[I Drove All Night]\nThe song was originally intended for Roy Orbison, who recorded it in 1987, the year before his death, but his rendition was not released until 1992, after Lauper's version of it had become a top 10 hit on both sides of the Atlantic in 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7b91231a07",
  "kind": "yes/no",
  "text": "Claim: As of 2016, the barbeque restaurant that was founded by a former Assistant Secretary - Indian Affairs has 170 locations.\n\nPassages:\n\n[David W. Anderson]\nDavid W. \"Famous Dave\" Anderson, best known as the founder of the Famous Dave's restaurant chain, is the former Assistant Secretary - Indian Affairs in the Department of the Interior, with jurisdiction over the Bureau of Indian Affairs and the Office of Indian Education Programs (now the Bureau of Indian Education).\n\n[Famous Dave's]\nIt has 170 locations in 34 U.S. states as of 2016.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q564bdfd3b0",
  "kind": "yes/no",
  "text": "Claim: NGC 166 is located by an english archaeologist who also discovered Frank Muller and Ormond Stone in 1886.\n\nPassages:\n\n[NGC 166]\nNGC 166 (also known as PGC 2143) is a spiral galaxy located around 2.6 million light-years away in the constellation Cetus, with an apparent magnitude of 15.18. It was discovered by Francis Preserved Leavenworth in 1886.\n\n[Francis Preserved Leavenworth]\nHe discovered many New General Catalogue objects together with Frank Muller and Ormond Stone.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q703b2f2a71",
  "kind": "yes/no",
  "text": "Text: mentally I’m hiding in the walk-in",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q1991b8793f",
  "kind": "yes/no",
  "text": "Tweet: Whoop diddy scoop poop",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4a19730204",
  "kind": "yes/no",
  "text": "Claim: In the 1940s, the historic diner in Albany, New York built, which also was a filming location for major portions of the Babenco 1987 film worked on by Lauro Escorel.\n\nPassages:\n\n[Lauro Escorel]\nIronweed\" (1987), another Babenco's film, would make him more known internationally.\n\n[Ironweed (film)]\nMajor portions of the film were shot on location in Albany, New York, including Jay Street at Lark Street, Albany Rural Cemetery and the Miss Albany Diner on North Broadway.\n\n[Miss Albany Diner]\nMiss Albany Diner (formerly known as Lil's Diner) is a historic diner in Albany, New York, built in 1941 and located at 893 Broadway, one of the oldest streets in Albany.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd6c8bb9c15",
  "kind": "yes/no",
  "text": "Claim: Riccardo Cocchi is Yulia Zagoruychenko's dance partner.\n\nPassages:\n\n[Yulia Zagoruychenko]\nYulia Zagoruychenko (born September 11, 1981) is the current World Latin Dance Champion, with her partner, Riccardo Cocchi.\n\n[Riccardo Cocchi]\nRiccardo Cocchi (born December 7, 1977, Terni, Italy) is a six-time Latin Dance Champion, with his partner, Yulia Zagoruychenko.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7e7d73034e",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "babe stop i’m about to gleek",
   "this can go two ways. babe stop im about to cum OR babe babe stop im about to cry"
  ]
 },
 {
  "qid": "qf84dddc350",
  "kind": "yes/no",
  "text": "Claim: The name Hakim Abdullah Jamal was adopted by African-American activist Allen Donaldson co-found Black Panther Party movement of the 1960s and 1970s.\n\nPassages:\n\n[Maulana Karenga]\nKarenga was a major figure in the Black Power movement of the 1960s and 1970s, and co-founded with Hakim Jamal the black nationalism and social change organization US.\n\n[Hakim Jamal]\nHakim Abdullah Jamal (March 28, 1931 – May 1, 1973) was the name adopted by African-American activist Allen Donaldson, who was a cousin of Malcolm X and later became an associate of Michael X.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6b8864a5e6",
  "kind": "yes/no",
  "text": "Claim: Frank Ellis Boynton worked at a tourist attraction that stands today as one of the most prominent remaining examples of the Gilded Age.\n\nPassages:\n\n[Biltmore Estate]\nBiltmore Estate is a large (6950.4 acre or 10.86 square miles) private estate and tourist attraction near Asheville, North Carolina. Still owned by George Vanderbilt's descendants, it stands today as one of the most prominent remaining examples of the Gilded Age.\n\n[Frank Ellis Boynton]\nFrank Ellis Boynton (July 10, 1859 – December 10, 1942) was a self-taught American botanist active in the Southeastern United States. He worked at Biltmore Estate with his brother, Charles Lawrence Boynton, and Chauncey Beadle.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa164b1ee07",
  "kind": "yes/no",
  "text": "Claim: Dwight D. Eisenhower assassinated the 20th President of the United States.\n\nPassages:\n\n[James A. Garfield]\nJames Abram Garfield (November 19, 1831 – September 19, 1881) was the 20th President of the United States, serving from March 4, 1881, until his assassination later that year.\n\n[Edward Anthony Spitzka]\n(In 1881, his father Edward Charles Spitzka, a famous neurologist and medical specialist in mental diseases, testified to the insanity of Charles Guiteau, the assassin of President James A. Garfield, at Guiteau's murder trial.)",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q68757daa9c",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Oh no, I have to listen to a cement mixer all day. This sucks.",
   "Ahhh I get to listen to a cement mixer all day. Awesome."
  ]
 },
 {
  "qid": "qeff5338178",
  "kind": "yes/no",
  "text": "Claim: The 1932 German football championship Final was played at a stadium that opened March 12th,1928.\n\nPassages:\n\n[1932 German football championship Final]\nIt was played on 12 June 1932 at the Städtisches Stadion in Nuremberg.\n\n[Max-Morlock-Stadion]\nMax-Morlock-Stadion ] is a stadium in Nuremberg, Germany, which was opened in 1928.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q694961802a",
  "kind": "yes/no",
  "text": "Claim: The line of the railroad the designer of McKim's School worked for was the port of Baltimore west to Sandy Hook.\n\nPassages:\n\n[Baltimore and Ohio Railroad]\nAt first this railroad was located entirely in the state of Maryland with an original line from the port of Baltimore west to Sandy Hook.\n\n[McKim's School]\nIt was designed by Baltimore architects William Howard and William Small and erected in 1833.\n\n[William Howard (engineer)]\nWilliam Howard (1793–1834) was an American mechanical engineer who was one of the first to work for the Baltimore and Ohio Railroad.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3012bc0d19",
  "kind": "yes/no",
  "text": "Claim: Jay Park left the South Korean music group that Lee Jun-ho is a part of, before the release of the group's video called \"Take Off\".\n\nPassages:\n\n[Go Crazy (album)]\nis the fourth Korean studio album (seventh overall) by South Korean boy band 2PM.\n\n[2PM]\nFormer leader Jay Park officially left the group in early 2010.\n\n[Ultra Lover]\nThe single was released along with the group's second live DVD \"1st Japan Tour 2011 \"Take Off\" in Makuhari Messe\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa5d755cc97",
  "kind": "yes/no",
  "text": "Claim: The North Central town that licenses WCJB-TV is home to the punk rock band Against Me!.\n\nPassages:\n\n[Gainesville, Florida]\nGainesville is the largest city in the region of North Central Florida.\n\n[Don't Lose Touch]\n\"Don't Lose Touch\" is a song by the Gainesville, Florida-based punk rock band Against Me!\n\n[WCJB-TV]\nWCJB-TV is the ABC-affiliated television station licensed to Gainesville, Florida, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q310b159250",
  "kind": "yes/no",
  "text": "Claim: Eddie Rabbitt wrote Peter and Gordon's biggest hit. That hit was covered by Del Davis, featured on \"Mellow Dubmarine\".\n\nPassages:\n\n[Del Davis (singer)]\nHis cover of \"World Without Love\" was featured on \"Mellow Dubmarine\".\n\n[Gordon Waller]\nGordon Trueman Riviere Waller (4 June 1945 – 17 July 2009) was a British singer–songwriter–guitarist, best known as Gordon of the 1960s pop music duo Peter and Gordon, whose biggest hit was the No. 1 million-selling classic \"A World Without Love\".\n\n[A World Without Love]\nThe song was written by Paul McCartney and attributed to Lennon–McCartney.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa87e809856",
  "kind": "yes/no",
  "text": "Post: no more instagram. we must all return to scrapbooks.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q1a3732e53d",
  "kind": "yes/no",
  "text": "Claim: Gelatine was an airship piloted on September 19, 1905 by a pioneer American aviator and barnstormer who died when the craft crash on the same flight.\n\nPassages:\n\n[Gelatine (airship)]\nGelatine was an airship operated by the United States Army Signal Corps. On the morning of September 19, 1905, the \"Gelatine\", piloted by Lincoln J. Beachey, ascended from the grounds of the Lewis and Clark Centennial Exposition on the shores of Guild's Lake in Portland, Oregon, landing 40 minutes later at the Vancouver Barracks in Vancouver, Washington.\n\n[Lincoln J. Beachey]\nLincoln J. Beachey (March 3, 1887 – March 14, 1915) was a pioneer American aviator and barnstormer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd2e87328b1",
  "kind": "yes/no",
  "text": "Claim: Between two scientists Ernst Messerschmid and Philippe Perrin, Ernst Willi Messerschmid is older.\n\nPassages:\n\n[Philippe Perrin]\nPhilippe Perrin (Colonel, French Air Force) (born January 6, 1963) is a French test pilot and former CNES and European Space Agency astronaut.\n\n[Ernst Messerschmid]\nProf. Dr. Ernst Willi Messerschmid (born May 21, 1945) is a German physicist and former astronaut.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q63cfb81644",
  "kind": "yes/no",
  "text": "Claim: The out-of-town store where an IMAX Digital 3D theater is in is a furniture retailer with a location in an enclosed shopping mall on the north side of Interstate 295 near the junction with Interstate 95.\n\nPassages:\n\n[Warwick Mall]\nWarwick Mall is an enclosed shopping mall in Warwick, Rhode Island, on the north side of Interstate 295 near the junction with Interstate 95.\n\n[Jordan's Furniture]\nJordan's Furniture is a furniture retailer in New England. There are currently seven locations - in Reading, Avon, Taunton, Natick, Massachusetts, Nashua, New Hampshire, Warwick Mall in Warwick, Rhode Island, and New Haven, Connecticut.\n\n[Jordan's IMAX]\nThe Sunbrella IMAX Theaters (formerly the Verizon IMAX Theaters) are two IMAX Digital 3D theaters located in Jordan's Furniture stores in Natick, Massachusetts and Reading, Massachusetts.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q91a1762694",
  "kind": "yes/no",
  "text": "Claim: Edmund Valentine White III wrote a play in 2006 and a book on homosexual sex in 1977.\n\nPassages:\n\n[Edmund White]\nEdmund Valentine White III (born January 13, 1940) is an American novelist, memoirist, and an essayist on literary and social topics. His books include \"The Joy of Gay Sex\" (1977) (written with Charles Silverstein), his trio of autobiographic novels, \"A Boy's Own Story\" (1982), \"The Beautiful Room Is Empty\" (1988) and \"The Farewell Symphony\" (1997), and his biography of Jean Genet.\n\n[Terre Haute (play)]\nTerre Haute is a 2006 play by the American writer Edmund White.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe8a60367c4",
  "kind": "yes/no",
  "text": "Claim: The 2015 Austrian thriller film Jack tells the story of a serial killer who died in 1994.\n\nPassages:\n\n[Jack Unterweger]\nJohann \"Jack\" Unterweger (16 August 195029 June 1994) was an Austrian serial killer who murdered prostitutes in several countries.\n\n[Jack (2015 film)]\nJack is a 2015 Austrian thriller film about serial killer Jack Unterweger, directed by Elisabeth Scharang.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa5c46964af",
  "kind": "yes/no",
  "text": "Claim: The trainer, who named Eddie Mahan \"the greatest football player of all time\", coached the Indians and was the first Oorang Indians to win a gold metal in his home country.\n\nPassages:\n\n[Eddie Mahan]\nHe was widely regarded as one of the greatest football players in the first 50 years of the sport and was named by Jim Thorpe as the greatest football player of all time.\n\n[Jim Thorpe]\nA member of the Sac and Fox Nation, Thorpe became the first Native American to win a gold medal for his home country.\n\n[Eagle Feather]\nThe Indians were a team based in LaRue, Ohio, composed only of Native Americans, and coached by Jim Thorpe.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf5bc1d179d",
  "kind": "yes/no",
  "text": "Claim: The song Highwayman written by Jimmy Webb inspired the name of a supergroup including Johnny Cash.\n\nPassages:\n\n[Highwayman (song)]\n\"Highwayman\" is a song written by American singer-songwriter Jimmy Webb, about a soul with incarnations in four different places in time and history: as a highwayman, a sailor, a construction worker on the Hoover Dam, and finally as a captain of a starship.\n\n[The Highwaymen (country supergroup)]\nThe Highwaymen was a country music supergroup composed of four of the genre's biggest artists well known for their pioneering influence on the outlaw country subgenre: Johnny Cash, Waylon Jennings, Willie Nelson, and Kris Kristofferson.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 }
]
