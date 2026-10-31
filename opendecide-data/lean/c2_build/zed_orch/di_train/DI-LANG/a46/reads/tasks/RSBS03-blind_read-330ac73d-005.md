# A46 replay label-noise blind read RSBS03-blind_read-330ac73d-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS03-blind_read-330ac73d-005.json

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
  "qid": "q892a5f9ee2",
  "kind": "yes/no",
  "text": "Claim: Dan Smith's song reached as low as number 5 on the US \"Billboard\" Hot 100 chart in 2013.\n\nPassages:\n\n[Dan Smith (singer)]\nDaniel Campbell \"Dan\" Smith (born 14 July 1986) is a British singer-songwriter and record producer. He is the lead singer, primary songwriter. The band formed in 2010 and gained mass popularity in 2013 when the song \"Pompeii\" was released.\n\n[Pompeii (song)]\nThe song was released as the album's fourth single on 12 January 2013. It reached number 2 in the UK Singles Chart, number 4 in Australian ARIA Chart, and number 5 on the US \"Billboard\" Hot 100 and number one on the Alternative Songs chart.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qbfd27a9d71",
  "kind": "yes/no",
  "text": "Claim: Reg E. Cathey played Dr. Franklin Storm in the summer 2015 film that this individual directed. This director and Mike Valerio both work in the entertainment industry.\n\nPassages:\n\n[Josh Trank]\nJoshua Benjamin \"Josh\" Trank (born February 19, 1984) is an American film director, screenwriter, and editor.\n\n[Fantastic Four (2015 film)]\nDirected by Josh Trank, who co-wrote the screenplay with Jeremy Slater and Simon Kinberg, the film stars Miles Teller, Michael B. Jordan, Kate Mara, Jamie Bell and Toby Kebbell.\n\n[Mike Valerio]\nMike Valerio is an award-winning writer, producer, director, and executive in the entertainment industry for over 20 years.\n\n[Reg E. Cathey]\nHe is best known for his roles as Norman Wilson in \"The Wire\", Martin Querns in \"Oz\", Dr. Franklin Storm in the 2015 reboot of \"The Fantastic Four\", and Freddy Hayes in \"House of Cards\", the latter earning him three consecutive Emmy Award nominations for Outstanding Guest Actor in a Drama Series, including a win in 2015.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qede13d0478",
  "kind": "yes/no",
  "text": "Claim: German musician Wilhelm Heckmann (1897-1995) imprisoned in the German Mauthausen–Gusen concentration camp.\n\nPassages:\n\n[Mauthausen-Gusen concentration camp]\nMauthausen–Gusen concentration camp was the hub of a large group of German concentration camps that was built around the villages of Mauthausen and Sankt Georgen an der Gusen (Gusen) in Upper Austria, roughly 20 km east of the city of Linz.\n\n[Wilhelm Heckmann]\nFrom 1937 to 1945 he was imprisoned in the Nazi concentration camps in Dachau and Mauthausen.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf3a10d001d",
  "kind": "yes/no",
  "text": "Claim: Radio On: A Listener's Diary is the first book by an author that voiced the character Violet in the film \"The Incredibles\".\n\nPassages:\n\n[Radio On: A Listener's Diary]\nRadio On: A Listener's Diary (1997) is the first book by Sarah Vowell.\n\n[Sarah Vowell]\nShe was also the voice of Violet in the animated film \"The Incredibles\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q799aac7844",
  "kind": "yes/no",
  "text": "Claim: Is best known for a 2006 British drama film which story centers on young skinheads in England in the year 1983.\n\nPassages:\n\n[Shane Meadows]\nShane Meadows (born 26 December 1972) is an English filmmaker of independent film. He is best known for the British cult film \"This Is England\" (2006) and \"its three sequel series\" (2010–2015).\n\n[This Is England]\nThis Is England is a 2006 British drama film written and directed by Shane Meadows. The story centres on young skinheads in England in 1983. The film illustrates how their subculture, which has its roots in 1960s West Indies culture, especially ska, soul, and reggae music, became adopted by the far-right, especially white nationalists and white supremacists, which led to divisions within the skinhead scene.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa38b02b844",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I never feel more empowered than when I’m listening to ‘this is me’ from camp rock",
   "I never feel more cheesy than when I am listening to 'this is me' from camp rock."
  ]
 },
 {
  "qid": "qbf78d1f256",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Raging debate on the importance of an Orlando Magic Summer League Championship. Definitely a notch below 6 if decided by coin flip. https://t.co/LG0VRwkrKO",
   "An uninteresting conversation regarding the importance of an Orlando Magic Summer League title."
  ]
 },
 {
  "qid": "qbd4d9f2cea",
  "kind": "yes/no",
  "text": "Tweet: The amount of silence I’ve seen surrounding the topic of Palestine from some of my followers is concerning.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q15eb857122",
  "kind": "yes/no",
  "text": "Claim: Lou Dials played for the MLB organization Baltimore Orioles, and has a current majority owner named Peter Angelos.\n\nPassages:\n\n[Baltimore Orioles]\nThe Baltimore Orioles are an American professional baseball team based in Baltimore, Maryland. After 52 often-beleaguered years in St. Louis, the franchise was purchased in November 1953 by a syndicate of Baltimore business and civic interests led by attorney/civic activist Clarence Miles and Mayor Thomas D'Alesandro, Jr. The team's current majority owner is lawyer Peter Angelos.\n\n[Lou Dials]\nFrom 1938 to 1941, Dials played in the Mexican League. After his playing career, he became scout for the Houston Astros, Cleveland Indians and Baltimore Orioles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9009572b53",
  "kind": "yes/no",
  "text": "Claim: Somebody's Daughter's star, who was in D.C. Cab, was most widely known for his role in the television sitcom \"Barney Miller\".\n\nPassages:\n\n[Somebody's Daughter]\nSomebody's Daughter is a 1992 television film starring Nicollette Sheridan, Nick Mancuso, Boyd Kestner, Michael Cavanaugh, Max Gail and Richard Lineback.\n\n[D.C. Cab]\nD.C. Cab (also known as Street Fight) is a 1983 American comedy film, starring Max Gail, Adam Baldwin, Mr. T, Charlie Barnett, Gary Busey, Marsha Warfield, and Whitman Mayo.\n\n[Max Gail]\nHe most notably portrayed the role of Detective Stan \"Wojo\" Wojciehowicz on the television sitcom \"Barney Miller\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q708f7e388d",
  "kind": "yes/no",
  "text": "Claim: The larval food plant of Leto venus is found in Antarctica and Koeleria is found all over.\n\nPassages:\n\n[Koeleria]\nKoeleria is a common and widespread genus of plants in the grass family, found on all continents except Antarctica and on various oceanic islands.\n\n[Leto venus]\nThe larval food plant is \"Virgilia\".\n\n[Virgilia (plant)]\nVirgilia is a genus of Southern African trees in the family Fabaceae, having shiny to hairy pinnate leaves and attractive mauve to pink pea-shaped flowers followed by leathery pods.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc1b951dc8a",
  "kind": "yes/no",
  "text": "Claim: Sky Rocket, in Disneyland Tokyo, was renovated into Phantom's Revenge roller coaster, that had the longest drop at the time.\n\nPassages:\n\n[Phantom's Revenge]\nWhen it opened in 1991, it was the fastest roller coaster and had the longest drop of any roller coaster in the world.\n\n[Sky Rocket]\nSky Rocket is a steel roller coaster located at Kennywood Park in Pittsburgh, Pennsylvania. It is the first coaster erected at the park since the renovation of the Steel Phantom into the Phantom's Revenge in 2001; it also marks the return of a roller coaster that features inversions.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q767299d8ee",
  "kind": "yes/no",
  "text": "Claim: Charleston is the capital of North Carolina, the state Curly Ray Cline is from.\n\nPassages:\n\n[West Virginia]\nThe capital and largest city is Charleston.\n\n[Curly Ray Cline]\nCurly Ray Cline (January 10, 1923 – August 19, 1997) was an American bluegrass fiddler from West Virginia known for his work with the Lonesome Pine Fiddlers and Ralph Stanley.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qebd50a581d",
  "kind": "yes/no",
  "text": "Tweet: oh you’re just friends?\n\nwhy’d u shave then?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qbb96621ae1",
  "kind": "yes/no",
  "text": "Claim: The player who signed as a free agent following the 1996–97 Vancouver Grizzlies season is the current CBS NBA analyst who played for the PORTLAND TRAILBLazers, along with former NFL Draft teammate Stacey Augmon.\n\nPassages:\n\n[1998–99 Portland Trail Blazers season]\nDuring the offseason, the Blazers signed free agents Jim Jackson and Greg Anthony, who would reunite with his former UNLV teammate Stacey Augmon.\n\n[Greg Anthony]\nGregory Carlton \"Greg\" Anthony (born November 15, 1967) is an American former National Basketball Association (NBA) player and is currently a television analyst for CBS Sports.\n\n[1996–97 Vancouver Grizzlies season]\nFollowing the season, Greg Anthony signed as a free agent with the Seattle SuperSonics, and Jackson was fired as coach.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa0bc6404c3",
  "kind": "yes/no",
  "text": "Claim: The boy band, NSYNC, that was formed in Orlando, Florida in 1995 was featured on the soundtrack to the biggest box office flop of 1999, \"Light It Up\".\n\nPassages:\n\n[Light It Up (soundtrack)]\nIt features songs from Master P featuring The No Limit All Stars, featuring, Ja Rule, *NSYNC, 112, DMX, Jon B., OutKast featuring Slimm Cutta-Calhoun and more.\n\n[NSYNC]\nNSYNC (sometimes stylized as *NSYNC or 'N Sync) was an American boy band formed in Orlando, Florida in 1995 and launched in Germany by BMG Ariola Munich.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qdfc010f5dd",
  "kind": "yes/no",
  "text": "Claim: The man who was impersonated by Roger Kitter in the Lego film died of a heart attack in 1984.\n\nPassages:\n\n[Tommy Cooper]\nOn 15 April 1984, Cooper collapsed with a heart attack on live national television, and died soon afterwards.\n\n[Roger Kitter]\nHe was also an impressionist, who provided the voice of Tommy Cooper in the Lego 'Kipper' advertisement.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd7b06d8063",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I love when you go to shop for plus size clothing and it's always just shoved under women's and it doesn't have any subcategories so u just have to wade thru everything like a pig being thrown slop",
   "I hate how difficult it is to shop for plus size clothes."
  ]
 },
 {
  "qid": "q3706c9e3f5",
  "kind": "yes/no",
  "text": "Claim: England internationl football team has had a player endorse the football boot Nike Total 90 was replaced by.\n\nPassages:\n\n[Nike Hypervenom]\nTherefore, it is endorsed/worn by players, notably forwards, such as Marcus Rashford, Kylian Mbappé, Robert Lewandowski, Gonzalo Higuaín, Mauro Icardi, Harry Kane, Edinson Cavani, Riyad Mahrez, Romelu Lukaku, Cian Brennan Aubameyang and Thiago.\n\n[Nike Total 90]\nThe Nike Total 90 range has now been replaced with Nike Hypervenom.\n\n[Marcus Rashford]\nMarcus Rashford (born 31 October 1997) is an English professional footballer who plays as a forward for Premier League club Manchester United and the England national team.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5dcbde4daa",
  "kind": "yes/no",
  "text": "Claim: The netflix series, produced by Joe Swanberg, that had an actress best known for her role on \"Atlanta\" also starred Evan Jonigkeit.\n\nPassages:\n\n[Zazie Beetz]\nZazie Beetz (born 1991) is a German-born, American actress best known for the role of Vanessa on \"Atlanta\".\n\n[Evan Jonigkeit]\nEvan Jonigkeit (pronounced \"John-a-kite\",born August 25, 1983) is an American actor known for his roles in \"\", \"Bone Tomahawk\", and \"Easy\".\n\n[Easy (TV series)]\nEasy is a comedy-drama anthology series written, directed, edited and produced by Joe Swanberg.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc5e92f0e5f",
  "kind": "yes/no",
  "text": "Claim: The son of The Green Man (TV serial) a BBC three-part TV adaption was born in April 1949.\n\nPassages:\n\n[The Green Man (TV serial)]\nThe Green Man is a BBC's three-part TV adaptation, based on Kingsley Amis' novel of the same name.\n\n[Kingsley Amis]\nHe is the father of British novelist Martin Amis.\n\n[Martin Amis]\nMartin Louis Amis (born 25 August 1949) is a British novelist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q38221ae436",
  "kind": "yes/no",
  "text": "Claim: The Colomac Mine was operated by the Omineca Resource Road at an earlier date, than the mine in British Columbia, near Kemess Creek Airport.\n\nPassages:\n\n[Kemess Mine]\nIt was operated by Royal Oak Mines from 1998 to 1999, when it was bought by Northgate Minerals.\n\n[Kemess Creek Airport]\nKemess Creek Airport, (TC LID: CBQ7) , is located near Kemess Mine, British Columbia, Canada.\n\n[Colomac Mine]\nThe Colomac Mine was a privately owned and operated open pit gold mine located 220 km northwest of Yellowknife in the Northwest Territories in Canada . In 1994, the mine had reopened under Royal Oak Mines Inc.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8d1fb76f1e",
  "kind": "yes/no",
  "text": "Claim: The rapper who made The Cold Corner 2 was born in london.\n\nPassages:\n\n[Lloyd Banks]\nChristopher Charles Lloyd (born April 30, 1982), better known by his stage name Lloyd Banks, is an American hip hop recording artist and member of East Coast hip hop group G-Unit, alongside childhood friends and fellow American rappers, 50 Cent and Tony Yayo.\n\n[The Cold Corner 2]\nThe Cold Corner 2, the eleventh mixtape by American rapper Lloyd Banks, was released on November 8, 2011 for free download.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf6ba29ae7a",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Heard a rumor that Baja Blast is coming to stores and regardless if anything else I hope for in life falls through, at least I'll have this.",
   "I've heard that Baja Blast may be sold in stores and I would enjoy that because I think the drink is good."
  ]
 },
 {
  "qid": "qf459120815",
  "kind": "yes/no",
  "text": "Claim: 3TEETH was the debut album for the opening act for the2016 tour with a headlining band that was formed in the California city of Los Angeles.\n\nPassages:\n\n[3Teeth (album)]\nTwo years after the album's release, 3Teeth embarked on the 2016 Tool tour as first opening act, followed by Primus.\n\n[Tool (band)]\nTool is an American rock band from Los Angeles, California.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q118776be4f",
  "kind": "yes/no",
  "text": "Post: I am not a simulation theorist but the groceries thing fucks me up. I have never seen a neighbor get groceries. I live in a big complex. And I feel like I am getting them constantly. Also, have u ever stayed at somebody’s house? I have to remind people to eat lunch or they won’t.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q82a1ab1249",
  "kind": "yes/no",
  "text": "Claim: Hank Osasuna starred in an ITV2 series. The series took its name from a song by the Puerto Rican singer who also recorded a song called \"the Puerto Rico House of Representatives\".\n\nPassages:\n\n[Livin' la Vida Loca]\n\"Livin' la Vida Loca\" is a number-one hit song by Puerto Rican singer Ricky Martin.\n\n[Lemon La Vida Loca]\nThe show's title is derived from Ricky Martin's 1999 hit single, \"Livin' la Vida Loca\".\n\n[Hank Osasuna]\nAfter this, Hank subsequently appeared as Mad Paul in \"\" and ITV2 series \"Lemon La Vida Loca\".\n\n[Frío (song)]\n\"Frío\" (English: \"Cold\") is the third single from Ricky Martin's studio album, \"Música + Alma + Sexo\" (2011).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc74cb30c23",
  "kind": "yes/no",
  "text": "Claim: The locals consider the township of Stirling a suburb of a southern town. That town is represented by Rebekha Carina Che Sharkie, an Australian politician.\n\nPassages:\n\n[Crafers, South Australia]\nThe town of Crafers is in the Adelaide Hills to the south-east of Adelaide, South Australia. Although technically considered to be an outer suburb of Adelaide, with many residents commuting to the city to work, locals consider Crafers to be more a suburb of the nearby township of Stirling.\n\n[Division of Mayo]\nThe Division of Mayo is an Australian electoral division located to the east, south, south-east and south-west of Adelaide, South Australia. It takes in the Adelaide Hills, Fleurieu Peninsula and Kangaroo Island, including the towns of Bridgewater, Crafers, Echunga, Gumeracha, Hahndorf, Kingscote, Langhorne Creek, Lobethal, Macclesfield, Mount Barker, Myponga, Oakbank, Stirling, Strathalbyn, Victor Harbor, Woodside, Yankalilla, and part of Birdwood.\n\n[Rebekha Sharkie]\nRepresenting the Division of Mayo since defeating Liberal Jamie Briggs at the 2016 federal election, she is the first Nick Xenophon Team member to be elected to the Australian House of Representatives.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb2315ab122",
  "kind": "yes/no",
  "text": "Claim: The Mikoyan design bureau developed the planes operated, by the main unit based at the 22nd Air Base, of the Polish Air Force.\n\nPassages:\n\n[22nd Air Base]\nThe main unit based there is the 41st Air Tactical Squadron flying MiG-29 fighters.\n\n[41st Tactical Squadron]\n41st Tactical Squadron (known as 41. The squadron operates Mikoyan MiG-29 jet fighters acquired from the German Luftwaffe.\n\n[Mikoyan MiG-29]\nThe Mikoyan MiG-29 (Russian: Микоян МиГ-29 ; NATO reporting name: Fulcrum) is a twin-engine jet fighter aircraft designed in the Soviet Union. Developed by the Mikoyan design bureau as an air superiority fighter during the 1970s, the MiG-29, along with the larger Sukhoi Su-27, was developed to counter new American fighters such as the McDonnell Douglas F-15 Eagle, and the General Dynamics F-16 Fighting Falcon.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe79e3289c5",
  "kind": "yes/no",
  "text": "Claim: The request-stop railway that reopened the line of Broadfield railway station, is a part of Summerseat and also runs between Heywood and Rawtenstall.\n\nPassages:\n\n[East Lancashire Railway]\nThe East Lancashire Railway is a 12+1/2 mi heritage railway line in north west England which runs between Heywood and Rawtenstall with intermediate stations at Bury Bolton Street, Burrs Country Park , Summerseat, Ramsbottom and Irwell Vale.\n\n[Summerseat railway station]\nSummerseat railway station is a preserved railway station that serves the village of Summerseat in Greater Manchester, England. It is part of the Heritage East Lancashire Railway (which runs for 12 miles from Heywood-Rawtenstall).\n\n[Broadfield railway station]\nThe line through the station has since been reopened by the heritage East Lancashire Railway, although the station itself remains disused.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qdcb523c746",
  "kind": "yes/no",
  "text": "Claim: The man that is linked to both the American Revolution film that has Hal Stalmaster in the cast, and Magic Kingdom is Walt Disney.\n\nPassages:\n\n[Magic Kingdom]\nInitialized by Walt Disney and designed by WED Enterprises, its layout and attractions are based on Disneyland Park in Anaheim, California, and is dedicated to fairy tales and Disney characters.\n\n[Hal Stalmaster]\nHarry Lapidus Stalmaster, known as Hal Stalmaster (born March 29, 1940), is an American former actor, known for his lead role in the 1957 Walt Disney film of the American Revolution \"Johnny Tremain\", based on the 1943 Esther Forbes novel of the same name.\n\n[Johnny Tremain (film)]\nJohnny Tremain is a 1957 film made by Walt Disney Productions, based on the 1944 Newbery Medal-winning children's novel of the same name by Esther Forbes, retelling the story of the years in Boston, Massachusetts prior to the outbreak of the American Revolution.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa8939adf40",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Excuse me but I think that you have made a spelling error on your last comment there.",
   "@Schlippertysch1 @anon_opin Very good. Just need to work on your spelling now 👍"
  ]
 },
 {
  "qid": "qf0870fa438",
  "kind": "yes/no",
  "text": "Claim: The genus that Clianthus maximus belongs in, has more species than Callicoma.\n\nPassages:\n\n[Clianthus maximus]\nIt is one of two species of \"Clianthus\" (kaka beak) and both have striking clusters of red flowers which resemble the beak of the kākā, a New Zealand parrot.\n\n[Clianthus]\nClianthus, commonly known as kakabeak (\"Kōwhai ngutukākā\" in Māori), is a genus of flowering plants in the legume family Fabaceae, comprising two species of shrubs native to New Zealand.\n\n[Callicoma]\nCallicoma, is a plant genus that contains just one species, Callicoma serratifolia, a tall shrub or small tree which is native to Australia.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qca0b8f70b4",
  "kind": "yes/no",
  "text": "Claim: The Tree of Man was written by a Nobel Prize-winner. He and the author of Noon Wine are both actors and writers.\n\nPassages:\n\n[Noon Wine]\nNoon Wine is a 1937 short novel by American author Katherine Anne Porter.\n\n[The Tree of Man]\nThe Tree of Man is the fourth published novel by the Australian novelist and 1973 Nobel Prize-winner, Patrick White.\n\n[Patrick White]\nPatrick Victor Martindale White (28 May 191230 September 1990) was an Australian writer who is widely regarded as one of the most important English-language novelists of the 20th century.\n\n[Katherine Anne Porter]\nKatherine Anne Porter (May 15, 1890 – September 18, 1980) was an American journalist, essayist, short story writer, novelist, and political activist.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8601b77b0c",
  "kind": "yes/no",
  "text": "Post: first day of work, and i’ve already cried on the job 👍",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q9754a7b61a",
  "kind": "yes/no",
  "text": "Claim: This individual is co-founder of Recess Records alongside Jason White (musician). He and the band that released Fahizah, have being in a band in common.\n\nPassages:\n\n[Pinhead Gunpowder]\nPinhead Gunpowder is an American punk rock band that formed in East Bay, California, in 1990.\n\n[Jason White (musician)]\nHe is also the guitarist/vocalist for the Californian punk band Pinhead Gunpowder, lead guitarist/lead vocalist for California, and co-founder of Adeline Records alongside Billie Joe Armstrong.\n\n[Fahizah]\nFahizah is the second EP by the American punk rock band Pinhead Gunpowder.\n\n[Billie Joe Armstrong]\nBillie Joe Armstrong (born February 17, 1972) is an American musician, singer, songwriter and actor who is best known as the lead vocalist, primary songwriter, and guitarist of the punk rock band Green Day, which he co-founded with Mike Dirnt.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4f12e3822a",
  "kind": "yes/no",
  "text": "Claim: Jim Lindberg and Alison Moyet are not singers of the same nationality.\n\nPassages:\n\n[Alison Moyet]\nGeneviève Alison Jane Moyet ( ; born 18 June 1961) is an English singer, songwriter and performer noted for her bluesy contralto voice.\n\n[Jim Lindberg]\nJames William Lindberg (born July 26, 1965) is an American singer and guitarist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6afa64c9f3",
  "kind": "yes/no",
  "text": "Claim: Lance Stephenson of the Indiana Pacers college basketball team plays his home games at Bankers Life Fieldhouse.\n\nPassages:\n\n[Lance Stephenson]\nLance Stephenson Jr. (born September 5, 1990) is an American professional basketball player for the Indiana Pacers of the National Basketball Association (NBA).\n\n[Indiana Pacers]\nThey play their home games at Bankers Life Fieldhouse.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb385e53a1e",
  "kind": "yes/no",
  "text": "Claim: \"Fires of Winter\" reached the \"New York Times\" bestseller list.\n\nPassages:\n\n[Johanna Lindsey]\nJohanna Lindsey (born Johanna Helen Howard, March 10, 1952), is one of the most popular American writers of historical romance novels worldwide. All of her books reached the \"New York Times\" bestseller list, many reaching No. 1.\n\n[Fires of Winter]\nFires of Winter is a novel by Johanna Lindsey originally published in September 1980 by Avon Books.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6a699ef1f0",
  "kind": "yes/no",
  "text": "Claim: The player named Rookie of The Year in the 1997–98 Toronto Raptors season is the American retired professional basketball player and the current head men's basketball coach that the University of the Pacific Tigers are led by.\n\nPassages:\n\n[Damon Stoudamire]\nDamon Lamon Stoudamire (born September 3, 1973) is an American retired professional basketball player and the current head men's basketball coach at the University of the Pacific.\n\n[Pacific Tigers men's basketball]\nThey play their home games at the Alex G. Spanos Center and are led by head coach Damon Stoudamire.\n\n[1995–96 Toronto Raptors season]\nTop draft pick Damon Stoudamire was named Rookie of The Year averaging 19.0 points, and 9.3 assists per game.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3cebd723ca",
  "kind": "yes/no",
  "text": "Claim: Michael John McKean is older than the Biffy Clyro musician.\n\nPassages:\n\n[Simon Neil]\nSimon Alexander Neil (born 31 August 1979) is a Scottish vocalist, guitarist, and songwriter.\n\n[Michael McKean]\nMichael John McKean (born October 17, 1947) is an American actor, comedian, and musician, known for a variety of roles played since the 1970s.\n\n[Biffy Clyro]\nBiffy Clyro are a Scottish rock band that formed in Kilmarnock, East Ayrshire, composed of Simon Neil (guitar, lead vocals), James Johnston (bass, vocals) and Ben Johnston (drums, vocals).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q9c7f5ac28d",
  "kind": "yes/no",
  "text": "Claim: The African-American composer, Scott Joplin, co-wrote Air.\n\nPassages:\n\n[Scott Joplin]\nScott Joplin ( ; 1867/68 or November 24, 1868– April 1, 1917) was an African-American composer and pianist.\n\n[Air Lore]\nAir Lore is an album by the improvisational trio Air featuring Henry Threadgill, Steve McCall, and Fred Hopkins performing compositions by Jelly Roll Morton and Scott Joplin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0518ef9566",
  "kind": "yes/no",
  "text": "Post: hug your loved ones right every single day. life is not promised to us so make every second count",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q6e3a5a313e",
  "kind": "yes/no",
  "text": "Claim: Masakatsu Ueda is a MMA fighter who is a blue belt under the Korean martial artist who teaches shoot wrestling and jiu-jitsu.\n\nPassages:\n\n[Masakatsu Ueda]\nHe is a blue belt in Brazilian Jiu-Jitsu under Yuki Nakai.\n\n[Yuki Nakai]\nYuki Nakai (中井祐樹 , Nakai Yūki ) is a retired Japanese mixed martial artist and Shooter. He currently teaches shoot wrestling and jiu-jitsu, and is the president of the Japanese Confederation of Jiu-Jitsu.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7cacb72736",
  "kind": "yes/no",
  "text": "Text: Ipswich Town 2020/21 Home Shirt 🔵⚪\n\nUEFA Cup 40 Year anniversary.\n\n#ITFC https://t.co/N95ktMkKBJ",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qa54473ac26",
  "kind": "yes/no",
  "text": "Claim: Robert Gossett acted in this 1985 play. It is by an American playwright who died in October 2005.\n\nPassages:\n\n[Fences (play)]\nFences is a 1985 play by American playwright August Wilson.\n\n[August Wilson]\nAugust Wilson (April 27, 1945 – October 2, 2005) was an American playwright whose work included a series of ten plays, \"The Pittsburgh Cycle\", for which he received two Pulitzer Prizes for Drama.\n\n[Robert Gossett]\nHe went on to act in the Broadway production of Lloyd Richard's \"Fences\", Hal Scott's \"A Raisin in the Sun\" and Donald McKayle's \"The Last Minstrel Show\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q19029869ab",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Disappointing morning as a Ferrari fan who woke up at 5:45am on a Sunday only for both drivers' races to be ruined by the first corner",
   "I've just got up at five forty five on a Sunday to watch the Japanese Grand Prix as a Ferrari fan and saw Vettel jump (and then fuck up) the start and Leclerc tangle with Verstappen on turn 2. Lovely stuff."
  ]
 },
 {
  "qid": "q586094d345",
  "kind": "yes/no",
  "text": "Claim: Lloyd Kaufman's award-winning co-director on Sgt. Kabukiman N.Y.P.D., and Roland Emmerich, do not both direct comedic horror films.\n\nPassages:\n\n[Roland Emmerich]\nHe began his work in the film industry by directing the film \"The Noah's Ark Principle\" (1984) as part of his university thesis and also co-founded Centropolis Entertainment in 1985 with his sister.\n\n[Sgt. Kabukiman N.Y.P.D.]\nSgt. Kabukiman N.Y.P.D. is a 1990 superhero comedy film directed by Lloyd Kaufman and Michael Herz and distributed by Troma Entertainment.\n\n[Michael Herz (producer)]\nWith Lloyd Kaufman, the two are the co-founders of Troma Entertainment, the world's longest running independent film studio, known for their comedic horror films, including the cult favorite \"Toxic Avenger series and \"Tromeo and Juliet\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd4c25b952d",
  "kind": "yes/no",
  "text": "Claim: Both larger relatives of Sporting Lucas Terrier and the Elkhound which are a group of Fennoscadian dog breeds are not named after a particular person. These type of dogs are used for hunting elk and moose and other large animals.\n\nPassages:\n\n[Pomeranian (dog)]\nThe Pomeranian (often known as a Pom or Pom Pom) is a breed of dog of the Spitz type that is named for the Pomerania region in Germany and Poland in Central Europe.\n\n[Elkhound]\nElkhounds are a group of Fennoscandian dog breeds belonging to the Spitz-type dogs and used for hunting elk/moose and other large animals.\n\n[Japanese Spitz]\nThere are varying standards around the world as to the ideal size of the breed, but they are always larger than their smaller cousins, the Pomeranian.\n\n[Sporting Lucas Terrier]\nThe Sporting Lucas Terrier is a small breed of dog of the terrier type.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qfa0caa4518",
  "kind": "yes/no",
  "text": "Post: That’s it for my first-ever live Twitter chat! Thanks for following along! #JMC4412",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 }
]
