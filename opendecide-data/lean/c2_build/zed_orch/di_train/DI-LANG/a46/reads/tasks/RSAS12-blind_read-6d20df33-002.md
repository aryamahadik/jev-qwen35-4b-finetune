# A46 replay label-noise blind read RSAS12-blind_read-6d20df33-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS12-blind_read-6d20df33-002.json

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
  "qid": "q8cf4d91d83",
  "kind": "yes/no",
  "text": "Text: Too much on my mind 😖",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q07a6f35261",
  "kind": "yes/no",
  "text": "Claim: Hank Osasuna starred in an ITV2 series. The series took its name from a song by the Puerto Rican singer Ricky Martin.\n\nPassages:\n\n[Livin' la Vida Loca]\n\"Livin' la Vida Loca\" is a number-one hit song by Puerto Rican singer Ricky Martin.\n\n[Lemon La Vida Loca]\nThe show's title is derived from Ricky Martin's 1999 hit single, \"Livin' la Vida Loca\".\n\n[Hank Osasuna]\nAfter this, Hank subsequently appeared as Mad Paul in \"\" and ITV2 series \"Lemon La Vida Loca\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4c12a5fa09",
  "kind": "yes/no",
  "text": "Text: sorry for crying about paddington, i really didn’t mean to",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q62f4d226a3",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "If you don't like Lemonade you're an extremist 🍋",
   "I don't understand people who are disgusted by Lemonade."
  ]
 },
 {
  "qid": "q98c84714a7",
  "kind": "yes/no",
  "text": "Claim: Petals on the Wind (film) is the sequel to the movie that starred Kiernan Brennan.\n\nPassages:\n\n[Kiernan Shipka]\nKiernan Brennan Shipka (born November 10, 1999) is an American actress. She is known for playing Sally Draper on the AMC series \"Mad Men.\"\n\n[Flowers in the Attic (2014 film)]\nFlowers in the Attic is a 2014 Lifetime movie, starring Kiernan Shipka, Ellen Burstyn, Mason Dye, and Heather Graham.\n\n[Petals on the Wind (film)]\nPetals on the Wind is a 2014 Lifetime movie sequel to the 2014 adaptation \"Flowers in the Attic\", starring Heather Graham, Rose McIver, Wyatt Nash, Bailey Buntain and Ellen Burstyn.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qadbdafb925",
  "kind": "yes/no",
  "text": "Claim: The actress whose friend Jim Brochu is known as the author of the unauthorized biography \"Lucy in the Afternoon\" worked closely withCharpes Lane.\n\nPassages:\n\n[Jim Brochu]\nA friend of Lucille Ball, he is known as the author of the unauthorized biography \"Lucy in the Afternoon\", and in this capacity, appeared on an episode of \"MythBusters\".\n\n[Lucille Ball]\nShe was best known as the star of the self-produced sitcoms \"I Love Lucy\", \"The Lucy–Desi Comedy Hour\", \"The Lucy Show\", \"Here's Lucy\", and \"Life with Lucy\".\n\n[Charles Lane (actor)]\nHe was a favored supporting actor of Lucille Ball, who often used him as a no-nonsense authority figure and comedic foe of her scatterbrained TV character on her TV series \"I Love Lucy\", \"The Lucy–Desi Comedy Hour\" and \"The Lucy Show\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3c442c048c",
  "kind": "yes/no",
  "text": "Claim: Eric McCormack of the TV series \"Will & Grace\" also appears in the film The Sisters from 2012.\n\nPassages:\n\n[Eric McCormack]\nEric James McCormack (born April 18, 1963) is a Canadian-American actor known for his role as Will Truman in the American sitcom \"Will & Grace\" and Dr. Daniel Pierce in the American crime drama \"Perception\".\n\n[The Sisters (2005 film)]\nThe Sisters is a 2005 film starring Maria Bello, Mary Stuart Masterson, and Erika Christensen as the title characters; it also stars Alessandro Nivola, Rip Torn, Eric McCormack, Steven Culp, Tony Goldwyn and Chris O'Donnell.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0c8ce054d9",
  "kind": "yes/no",
  "text": "Claim: Shake it Off is the song written by singer-songwriter Taylor Swift that shares the optomistic lyrical message to a song called \"Yodel it\".\n\nPassages:\n\n[Shake It Off]\n\"Shake It Off\" is a song recorded by American singer-songwriter Taylor Swift from her fifth album, \"1989\" (2014).\n\n[Yodel It!]\n\"Yodel It!\" The track's optimistic lyrical message was compared to that of Taylor Swift's \"Shake It Off\" (2014).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb765d43f3d",
  "kind": "yes/no",
  "text": "Text: Here is my book that no-one will ever read! 👨🏽‍🔬 https://t.co/EstLa52GEX",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qfbeeb760b8",
  "kind": "yes/no",
  "text": "Claim: The defending champion who lost the Singles title at the 1994 Waldbaum's Hamlet Cup, and Max Mirnyi have both been professional basketball players.\n\nPassages:\n\n[Marc Rosset]\nMarc Rosset (born 7 November 1970) is a former professional tennis player from Switzerland who is best remembered for winning the men's singles gold medal at the 1992 Olympic Games.\n\n[Max Mirnyi]\nMaksim \"Max\" Mirnyi (Belarusian: Максім Мікалаевіч Мірны ] ) (Russian: Максим Николаевич Мирный ] ) (born 6 July 1977, in Minsk) is a Belarusian professional tennis player.\n\n[1994 Waldbaum's Hamlet Cup – Singles]\nMarc Rosset was the defending champion, but lost in the second round to Renzo Furlan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qb69ce68142",
  "kind": "yes/no",
  "text": "Claim: John Wayne Airport is further west than Muskegon County Airport.\n\nPassages:\n\n[John Wayne Airport]\nJohn Wayne Airport (IATA: SNA, ICAO: KSNA, FAA LID: SNA) is an international airport in Orange County, California, United States, with its mailing address in the city of Santa Ana, hence the IATA airport code.\n\n[Muskegon County Airport]\nMuskegon County Airport (IATA: MKG, ICAO: KMKG, FAA LID: MKG) is a county owned, public use airport in Muskegon County, Michigan, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q46b9696642",
  "kind": "yes/no",
  "text": "Claim: The rapper who made The Cold Corner 2 was born in london.\n\nPassages:\n\n[Lloyd Banks]\nChristopher Charles Lloyd (born April 30, 1982), better known by his stage name Lloyd Banks, is an American hip hop recording artist and member of East Coast hip hop group G-Unit, alongside childhood friends and fellow American rappers, 50 Cent and Tony Yayo.\n\n[The Cold Corner 2]\nThe Cold Corner 2, the eleventh mixtape by American rapper Lloyd Banks, was released on November 8, 2011 for free download.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qaf80e587cc",
  "kind": "yes/no",
  "text": "Claim: Chad & Jeremy, the English singing folk rock duo, were born in the town linked by rail to Kendal, named after a freshwater lake of the same name.\n\nPassages:\n\n[Windermere, Cumbria (town)]\nAlthough the town Windermere does not touch the lake (it took the name of the lake when the railway line was built in 1847 and the station was called \"Windermere\"), it has now grown together with the older lakeside town of Bowness-on-Windermere, though the two retain distinguishable town centres.\n\n[Chad &amp; Jeremy]\nChad and Jeremy are an English singing folk rock duo originating in the 1960s, comprising Chad Stuart (born David Stuart Chadwick, 10 December 1941, Windermere, Cumbria) and Jeremy Clyde (born Michael Thomas Jeremy Clyde, 22 March 1941, Dorney, Buckinghamshire).\n\n[Windermere Hotel (Lake District)]\nWindermere Hotel , originally The Riggs Windermere, is a hotel in Windermere, Cumbria, England, located near Windermere railway station. The hotel opened at the time that the railway link with Kendal was established in 1847.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa5baafb435",
  "kind": "yes/no",
  "text": "Claim: The creator of the character, for whom Helena Štáchováwas provided the French-language voice of, was born in 1954.\n\nPassages:\n\n[Lisa Simpson]\nCartoonist Matt Groening created and designed her while waiting to meet James L. Brooks.\n\n[Helena Štáchová]\nNotably, Štáchová provided the Czech language-voice of Lisa Simpson on the Czech version of the American animated sitcom, \"The Simpsons\".\n\n[Matt Groening]\nMatthew Abraham \"Matt\" Groening ( ; born February 15, 1954) is an American cartoonist, writer, producer, animator, and voice actor.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q204750af6c",
  "kind": "yes/no",
  "text": "Claim: The genus which includes a species of flowering bush commonly known as \"Little Pickles\" has more species in it than Stangeria.\n\nPassages:\n\n[Othonna capensis]\nOthonna capensis also known as Little Pickles, is a species of the genus \"Othonna\" and family Asteraceae and is a native of South Africa.\n\n[Othonna]\nOthonna is a genus of African plants in the sunflower family.\n\n[Stangeria]\nStangeria eriopus is a cycad endemic to southern Africa It is the sole species in the genus Stangeria, most closely related to the Australian genus \"Bowenia\", with which it forms the family Stangeriaceae.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd6bfae9e64",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "can't i have nice weather for my birthday even if we're in lockdown?",
   "They really said you can’t have nice weather AND no lockdown for your bday this year huh"
  ]
 },
 {
  "qid": "qcffc70a63d",
  "kind": "yes/no",
  "text": "Claim: Prince William, Duke of Gloucester and Prince George of Denmark, were eventually monarchs of Great Britain Kingdom.\n\nPassages:\n\n[Prince William, Duke of Gloucester]\nPrince William, Duke of Gloucester (24 July 1689 – 30 July 1700 ) was the son of Princess Anne, later Queen of England, Ireland and Scotland from 1702, and her husband, Prince George, Duke of Cumberland.\n\n[Prince George of Denmark]\nPrince George of Denmark and Norway, Duke of Cumberland (Danish: \"Jørgen\" ; 2 April 165328 October 1708), was the husband of Queen Anne, who reigned over Great Britain from 1702.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe0aefc7f05",
  "kind": "yes/no",
  "text": "Tweet: my computer does this fun thing now where it shakes in a way that exactly replicates what happens to my vision when i forget my meds so that’s exciting !",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qd62770e0cb",
  "kind": "yes/no",
  "text": "Claim: Tony Scott directed the 2004 film that featured \"Mas\". The musician's polka album Reina came out after that album.\n\nPassages:\n\n[Man on Fire (2004 film)]\nMan on Fire is a 2004 British-American crime thriller film directed by Tony Scott from a screenplay by Brian Helgeland, and based on the 1980 novel of the same name by A. J. Quinnell.\n\n[Kinky (Kinky album)]\nAnother of their songs, \"Más\", is featured in the PS2 video game SSX 3 and in the 2004 film Man on Fire.\n\n[Reina (album)]\nThe album's lyrics are sung more in English than Spanish, unlike Kinky's two preceding albums, \"Kinky\" (2002) and \"Atlas\" (2003).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0d49eb2854",
  "kind": "yes/no",
  "text": "Tweet: Absolutely prepared to ditch #WoW for #FFXIV at this point...",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qce9b769de1",
  "kind": "yes/no",
  "text": "Claim: The 133d Air Refueling Squadron unit of the Air National Guard is located at a base that was host to the 509th Bomb Wing flying the General Dynamics FB-111A.\n\nPassages:\n\n[133d Air Refueling Squadron]\nThe 133d Air Refueling Squadron (133 ARS) is a unit of the New Hampshire Air National Guard 157th Air Refueling Wing located at Pease Air National Guard Base, Portsmouth, New Hampshire, United States.\n\n[Pease Air National Guard Base]\nIt occupies a portion of what was once Pease Air Force Base, a former Strategic Air Command facility with a base-related population of 10,000 and which was home to the 509th Bomb Wing (509 BW) flying the General Dynamics FB-111A.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q14aaa69728",
  "kind": "yes/no",
  "text": "Claim: In this religion, where Mehet-Weret is a godess of the sky, a person would be weighted against the feather of truth to decide if they where worthy of damnation and would face the torment in the lake of fire.\n\nPassages:\n\n[Ancient Egyptian religion]\nAncient Egyptian religion was a complex system of polytheistic beliefs and rituals which were an integral part of ancient Egyptian society.\n\n[Mehet-Weret]\nMehet-Weret \"(mḥ.t-wr.t)\" is a goddess of the sky in Ancient Egyptian religion. Her name means \"Great Flood\".\n\n[Damnation]\nIn Ancient Egyptian religious tradition, citizens would recite the 42 negative confessions of Maat as their heart was weighed against the feather of truth.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qaf22e8877a",
  "kind": "yes/no",
  "text": "Claim: The 2003 SEC Championship Game was played at an all-seater stadium owned and operated by the State of Georgia as part of the Georgia World Congress Center Authority.\n\nPassages:\n\n[Georgia Dome]\nLocated in Atlanta, Georgia, between downtown to the east and Vine City to the west, it was owned and operated by the State of Georgia as part of the Georgia World Congress Center Authority.\n\n[2003 SEC Championship Game]\nThe 2003 SEC Championship Game was won by the LSU Tigers 34–13 over the Georgia Bulldogs. The game was played in the Georgia Dome in Atlanta, Georgia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q592d7f3cfd",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I’m in Canada so like Happy 4rth?",
   "Still celebrating the Fourth of July in Canada!"
  ]
 },
 {
  "qid": "qe9988ba8c8",
  "kind": "yes/no",
  "text": "Claim: Brian Robertson is one of the two members to have played with a band since its origin as Bomb Squad. The other one is younger than David Usher. \"Poisonous Candy Factory\" is a DVD released by the band.\n\nPassages:\n\n[Poisonous Candy Factory]\nPoisonous Candy Factory is the second DVD released by third wave ska/funk/pop band, Suburban Legends.\n\n[Brian Robertson (trombonist)]\nBrian Robertson (born October 19, 1979) is the trombone player for the Orange County-based third-wave ska band Suburban Legends and, along with Vincent Walker, is one of the two members to have played with the band since its origin as Bomb Squad.\n\n[David Usher]\nDavid Usher (born April 24, 1966) is an English-born Canadian musician, best-selling author, keynote speaker and activist, known as the lead singer of the alternative rock band Moist.\n\n[Vincent Walker]\nVincent Francis Walker (born March 2, 1980), better known as Vince Walker, is an American multi-instrumentalist, best known as the lead singer of third-wave ska band Suburban Legends.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q68ec5b85de",
  "kind": "yes/no",
  "text": "Claim: The boy band, NSYNC, that was formed in Orlando, Florida in 1995 was featured on the soundtrack to the biggest box office flop of 1999, \"Light It Up\".\n\nPassages:\n\n[Light It Up (soundtrack)]\nIt features songs from Master P featuring The No Limit All Stars, featuring, Ja Rule, *NSYNC, 112, DMX, Jon B., OutKast featuring Slimm Cutta-Calhoun and more.\n\n[NSYNC]\nNSYNC (sometimes stylized as *NSYNC or 'N Sync) was an American boy band formed in Orlando, Florida in 1995 and launched in Germany by BMG Ariola Munich.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa4dd38f6c1",
  "kind": "yes/no",
  "text": "Claim: Caleb Joshua Shomo has been a member of more bands than John Rzeznik.\n\nPassages:\n\n[Caleb Shomo]\nCaleb Joshua Shomo (born December 1, 1992) is the lead vocalist of hardcore band Beartooth, the former lead vocalist, guitarist, keyboardist, and early on backing vocalist of metalcore band Attack Attack! , and the owner of Studio Records in Columbus, Ohio. Shomo joined Attack Attack!\n\n[John Rzeznik]\nJohn Joseph Theodore Rzeznik ( ; born December 5, 1965) is an American musician, singer-songwriter, and producer. He is best known as the guitarist and frontman of the rock band the Goo Goo Dolls, of which he is a founding member and with whom he has recorded eleven studio albums.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1d151106a8",
  "kind": "yes/no",
  "text": "Claim: The player acquired by the Milwaukee Bucks from the Charlotte Bobcats in the offseason before the 2004-2005 NBA season was of Georgian nationality born in March 1976.\n\nPassages:\n\n[2004–05 Milwaukee Bucks season]\nThe 2004–05 NBA season was the Bucks' 37th season in the National Basketball Association. During the offseason, the Bucks signed free agents Mike James and second-year guard Mo Williams, while acquiring Zaza Pachulia from the expansion Charlotte Bobcats.\n\n[Zaza Pachulia]\nZaza Pachulia (Georgian: ზაზა ფაჩულია ; February 10, 1984) is a Georgian professional basketball player for the Golden State Warriors of the National Basketball Association (NBA).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q48e142d2a4",
  "kind": "yes/no",
  "text": "Claim: Steven Earl \"Steve\" Gaines is the guitarist that played on the LP, which included \"That Smell\" released in 1977, and was a member of an American Southern Rock band from May 1976 until his death Oct 1977.\n\nPassages:\n\n[Steve Gaines]\nSteven Earl \"Steve\" Gaines (September 14, 1949 – October 20, 1977) was an American musician. He is best known as a guitarist, vocalist and songwriter of Southern rock band Lynyrd Skynyrd from May 11, 1976 until his death on October 20, 1977 and is the younger brother of Cassie Gaines, who was a back up vocalist for the band's live performances.\n\n[Street Survivors]\nStreet Survivors is the fifth studio album by Southern rock band, Lynyrd Skynyrd, released on October 17, 1977. The LP is the last Skynyrd album recorded by original members Ronnie Van Zant and Allen Collins, and is the sole Skynyrd studio recording by guitarist Steve Gaines.\n\n[That Smell]\nWritten by Ronnie Van Zant and guitarist Allen Collins, it was released in 1977 on the album \"Street Survivors\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qb9c83ca466",
  "kind": "yes/no",
  "text": "Claim: Marc Shiller, who was born in Beunos Aires in the 1950s, but is a resident of the United States, belongs to the ethnic group, that includes Paz Lenchantin.\n\nPassages:\n\n[Paz Lenchantin]\nPaz Lenchantin (born December 12, 1973) is an Argentine American musician.\n\n[Marc Schiller]\nMarc Schiller is an Argentinian American man who was born in Buenos Aires, Argentina in 1957. He survived a kidnapping and attempted murder by the Sun Gym Gang in Miami, Florida in 1994.\n\n[Argentine Americans]\nArgentine Americans (Spanish: Argentino Americanos ) are Americans whose full or partial origin is in Argentina.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc742415c6a",
  "kind": "yes/no",
  "text": "Tweet: @PONOS_EN Very nice. We're now briefly up to date. Hopefully doesn't take you so long to do the English release of the new pixie after we get 9.10.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q3a673c922d",
  "kind": "yes/no",
  "text": "Claim: A notable alumni of Filbornaskolan participated in the Celtic 1977 Scottish League Cup Final. He was a Celtic football coach and former professional player.\n\nPassages:\n\n[Filbornaskolan]\nNotable former alumni include Henrik Larsson.\n\n[Henrik Larsson]\nHenrik Edward Larsson (] ; born 20 September 1971) is a Swedish football coach and former professional player.\n\n[1997 Scottish League Cup Final]\nCeltic won the match 3–0 thanks to goals by Marc Rieper, Henrik Larsson and Craig Burley.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q73a2846ca0",
  "kind": "yes/no",
  "text": "Claim: The Seattle Fighter Wing was a unit of the United States Air Force, active during the Pacific War of 1941-45, it was based in the Northwestern United States in Washington state.\n\nPassages:\n\n[Northwestern United States]\nThe Northwestern United States is an informal geographic region of the United States.\n\n[Seattle Fighter Wing]\nThe Seattle Fighter Wing was a unit of the United States Air Force, active during the Pacific War of 1942-45.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q136d6b37c8",
  "kind": "yes/no",
  "text": "Claim: The Spitsbergen based seed bank, the Svalbard Global Seed Vault, serves to protects agricultural diversity in the far north, 1300 km from Wakehurst Place.\n\nPassages:\n\n[Agriculture in Svalbard]\nSvalbard is also home to the Global Seed Vault, which serves to protect the world's biological and agricultural diversity.\n\n[Svalbard Global Seed Vault]\nThe Svalbard Global Seed Vault (Norwegian: \"Svalbard globale frøhvelv\" ) is a secure seed bank on the Norwegian island of Spitsbergen near Longyearbyen in the remote Arctic Svalbard archipelago, about 1300 km from the North Pole.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd693392ea4",
  "kind": "yes/no",
  "text": "Claim: One song of the artist that appeared in Valentine's Day (2010 film) was released on February 19 2007. It was co-written by one of the co-writers of the Gary Allen song \"Songs About Rain\".\n\nPassages:\n\n[Valentine's Day (2010 film)]\nThe film consists of an ensemble cast led by Jessica Alba, Kathy Bates, Jessica Biel, Bradley Cooper, Eric Dane, Patrick Dempsey, Héctor Elizondo, Jamie Foxx, Jennifer Garner, Topher Grace, Anne Hathaway, Ashton Kutcher, Queen Latifah, Taylor Lautner, George Lopez, Shirley MacLaine, Emma Roberts, Julia Roberts, Carter Jenkins, and Taylor Swift in her film debut.\n\n[Songs About Rain]\n\"Songs About Rain\" is a song written by Pat McLaughlin and Liz Rose, and recorded by American country music artist Gary Allan.\n\n[Teardrops on My Guitar]\n\"Teardrops on My Guitar\" was released on February 19, 2007 by Big Machine Records, as the second single from Swift's eponymous debut album (2006).\n\n[Liz Rose]\nShe has co-written twenty of Swift's officially-released songs and singles, including \"White Horse,\" \"Teardrops on My Guitar,\" and \"You Belong with Me,\" which won her and Swift a Grammy Award in 2010.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q204fc98ccc",
  "kind": "yes/no",
  "text": "Claim: Horror movie R-Point, set in 1972 Kenya, was filmed partially in a location about 3 miles south-west of Povokvil Waterfalls.\n\nPassages:\n\n[R-Point]\nSet in 1972 Vietnam, during the Vietnam War, it stars Kam Woo-sung and Son Byong-ho as members of the South Korean military in Vietnam.\n\n[Povokvil Waterfalls]\nIt is located about 3 mi north-east of Bokor Hill Station.\n\n[Bokor Hill Station]\nIt was used as the location for the final showdown of the movie \"City of Ghosts\" (2002) and the 2004 film \"R-Point\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q70524be380",
  "kind": "yes/no",
  "text": "Tweet: Tell the liverpool players to get some beers and just sit on the grass for the full 90 mins. Let leeds score as many goals as they want. #NoToEuropeanSuperLeague",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q9b7e81b9a6",
  "kind": "yes/no",
  "text": "Claim: The satellite Bianca is named after the sister of Katherine in a Shakespeare's dramatic play believed to be written between the years 1590 and 1592.\n\nPassages:\n\n[Bianca (moon)]\nIt was named after the sister of Katherine in Shakespeare's play \"The Taming of the Shrew\".\n\n[The Taming of the Shrew]\nThe Taming of the Shrew is a comedy by William Shakespeare, believed to have been written between 1590 and 1592.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qea1a2d1065",
  "kind": "yes/no",
  "text": "Tweet: Dan Smith playing oblivion on his IG live has absolutely topped my week off 🥺",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q402143617f",
  "kind": "yes/no",
  "text": "Claim: Star of American neo-western film The Far Horizons was born in August and was a professor.\n\nPassages:\n\n[The Absent-Minded Professor]\nThe film stars Fred MacMurray as Professor Ned Brainard.\n\n[The Far Horizons]\nThe Far Horizons is a 1955 American western film directed by Rudolph Maté, starring Fred MacMurray, Charlton Heston, Donna Reed and Barbara Hale.\n\n[Fred MacMurray]\nFrederick Martin \"Fred\" MacMurray (August 30, 1908 – November 5, 1991) was an American actor who appeared in more than 100 movies and a successful television series during a career that spanned nearly a half-century, from 1930 to the 1970s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9b8d7ca649",
  "kind": "yes/no",
  "text": "Claim: The Ruthe Balock Jones tribe is based in central Bartlesville, Oklahoma.\n\nPassages:\n\n[Ruthe Blalock Jones]\nRuthe Blalock Jones (born 1939) is a Delaware-Shawnee-Peoria painter and printmaker from Oklahoma.\n\n[Delaware Tribe of Indians]\nThe Delaware Tribe of Indians, sometimes called the Eastern Delaware, based in Bartlesville, Oklahoma, is one of three federally recognized tribes of Delaware Indians in the United States, along with the Delaware Nation based in Anadarko, Oklahoma and the Stockbridge-Munsee Community of Wisconsin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q34d841baec",
  "kind": "yes/no",
  "text": "Claim: A pair of terraces on the Carlton House Terrace street took the place of this house. George IV was the Prince Regent likely to have stayed in that house in 1811.\n\nPassages:\n\n[George IV of the United Kingdom]\nGeorge IV (George Augustus Frederick; 12 August 1762 – 26 June 1830) was King of the United Kingdom of Great Britain and Ireland and of Hanover following the death of his father, George III, on 29 January 1820, until his own death ten years later. From 1811 until his accession, he served as Prince Regent during his father's final mental illness.\n\n[Carlton House]\nCarlton House was a mansion in London, best known as the town residence of the Prince Regent for several decades from 1783.\n\n[Carlton House Terrace]\nThey took the place of Carlton House, and the freehold still belongs to the Crown Estate.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q112326e849",
  "kind": "yes/no",
  "text": "Claim: M. P. Shiel and the British author of The Ingo tetralogy, a series of four children's novels set in Cornwall, are not both of West Indian descent.\n\nPassages:\n\n[Helen Dunmore]\nHelen Dunmore FRSL (12 December 1952 – 5 June 2017) was a British poet, novelist and children's writer.\n\n[M. P. Shiel]\nMatthew Phipps Shiell (21 July 1865 – 17 February 1947) – known as M. P. Shiel – was a prolific British writer of West Indian descent.\n\n[Ingo tetralogy]\nThe Ingo tetralogy is a series of four children's novels, set in Cornwall, by British author Helen Dunmore.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6ff98ba458",
  "kind": "yes/no",
  "text": "Claim: Moroni is the historic capital of the archipelago where Djoièzi is located.\n\nPassages:\n\n[Djoièzi]\nDjoièzi is a village on the island of Mohéli in the Comoros.\n\n[Comoros]\nIts capital is Moroni, on Grande Comore.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9e77700924",
  "kind": "yes/no",
  "text": "Claim: The host of the show Way Too Early frequently serves as fill-in anchor on \"Today\" for a tv journalist that was the host of \"PM Magazine\" in the 80's.\n\nPassages:\n\n[Willie Geist]\nGeist also frequently serves as fill-in anchor on \"Today\" for Matt Lauer.\n\n[Matt Lauer]\nHe was also host of \"PM Magazine\" (or \"Evening Magazine\" 1980–86).\n\n[Way Too Early]\nIt premiered on July 27, 2009 hosted by Willie Geist.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q98c8a87943",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I feel like too many people say that they're allergic to pineapple when they really aren't.",
   "people who say that they’re allergic to pineapple are pathological liars!!!!!!!"
  ]
 },
 {
  "qid": "q4e807b33b7",
  "kind": "yes/no",
  "text": "Claim: The shikara is found by a water body. It is further south than the body of water where the Goathaunt Bunkhouse is located.\n\nPassages:\n\n[Dal Lake]\nDal is a lake in Srinagar (Dal Lake is a misnomer as Dal in Kashmiri means lake), the summer capital of Jammu and Kashmir.\n\n[Waterton Lake]\nWaterton Lake is a mountain lake in southern Alberta, Canada and northern Montana, United States.\n\n[Shikara]\nThe shikara is a type of wooden boat found on Dal Lake and other water bodies of Srinagar, Jammu & Kashmir, India.\n\n[Goathaunt Bunkhouse]\nThe bunkhouse is the last surviving structure of this era at this location, near the southern end of Waterton Lake.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6986961c18",
  "kind": "yes/no",
  "text": "Claim: R.D. Reid acted alongside Kevin Zegers acted in the original version of a movie by the founder of Cruel and Unusual Films. He didn't appear in the remake by George A. Romero.\n\nPassages:\n\n[Dawn of the Dead (2004 film)]\nA remake of George A. Romero's 1978 film of the same name, it was written by James Gunn and stars Sarah Polley, Ving Rhames, Jake Weber, and Mekhi Phifer.\n\n[Cruel and Unusual Films]\nCruel and Unusual Films, Inc. is an American film production company that was established in 2004 by filmmaker Zack Snyder, his wife Deborah Snyder, and their producing partner Wesley Coller.\n\n[Kevin Zegers]\nHe also starred in the films \"Dawn of the Dead\" (2004), \"Transamerica\" (2005), \"It's a Boy Girl Thing\" (2006), \"The Jane Austen Book Club\" (2007), \"Fifty Dead Men Walking\" (2008), and \"Frozen\" (2010).\n\n[R. D. Reid]\nHe appeared in Zack Snyder's \"Dawn of the Dead\", and George A. Romero's \"Diary of the Dead\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q658ce5dde1",
  "kind": "yes/no",
  "text": "Claim: Diplolaena, not Arenaria, is in the family Rutaceae.\n\nPassages:\n\n[Arenaria (plant)]\nArenaria is a genus of flowering plants, within the family Caryophyllaceae.\n\n[Diplolaena]\nDiplolaena is a genus of evergreen shrubs in the family Rutaceae .",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q235f398b1e",
  "kind": "yes/no",
  "text": "Claim: The TV series where the actor who played this character joined in early 2010. The series was premiered on July 18, 2006. Richard Adar was portrayed in a still photo on display in the character's home during a Miniseries of the TV show.\n\nPassages:\n\n[Gaius Baltar]\nDr. Gaius Baltar is a fictional character in the TV series \"Battlestar Galactica\" played by James Callis, a reimagining of Count Baltar from the 1978 \"Battlestar Galactica\" series.\n\n[James Callis]\nHe joined the cast of the TV Series \"Eureka\", on Syfy, in 2010.\n\n[Eureka (U.S. TV series)]\nEureka is an American science fiction television series that premiered on Syfy on July 18, 2006.\n\n[Richard Adar]\nIn the Miniseries, Adar was portrayed in a still picture in Doctor Gaius Baltar's house by producer David Eick in age-enhancing make-up.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 }
]
