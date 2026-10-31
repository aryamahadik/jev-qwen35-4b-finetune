# A46 replay label-noise blind read RSAS11-blind_read-7e2e415b-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS11-blind_read-7e2e415b-000.json

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
  "qid": "q8ca334f74d",
  "kind": "yes/no",
  "text": "Claim: American cinematographer, John Warwick Lindley, is best know for his work in a 1998 American romantic comedy-drama film produced by Nora Ephron.\n\nPassages:\n\n[You've Got Mail]\nYou've Got Mail is a 1998 American romantic comedy-drama film directed by Nora Ephron, co-written by Nora and Delia Ephron, and starring Tom Hanks and Meg Ryan.\n\n[John Lindley (cinematographer)]\nJohn Warwick Lindley (November 17, 1951 in New York City) is an American cinematographer best known for his work on such films as \"Field of Dreams\", \"Bewitched\", \"Pleasantville\" and \"You've Got Mail\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1382e4059c",
  "kind": "yes/no",
  "text": "Claim: The manufacturer of the plane that shot down Jameel Sayhood is McDonnell Douglas.\n\nPassages:\n\n[McDonnell Douglas F-15 Eagle]\nThe McDonnell Douglas F-15 Eagle is an American twin-engine, all-weather tactical fighter aircraft designed by McDonnell Douglas (now Boeing) to gain and maintain air supremacy in aerial combat.\n\n[Jameel Sayhood]\nCaptain Jameel Sayhood was an Iraqi pilot in the Gulf War who it is claimed managed to attain one of the few aerial victories by the Iraqi Air Force in his MiG-29B, before being shot down by USAF Captain Craig Underhill and Captain Cesar Rodriguez with their F-15Cs mere minutes after his air-air victory.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qbfc5e4cc9b",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "I'm so done with everyone, I wish I could move away to Italy.",
   "thats it im packing my things and moving to italy see u all in a month xo"
  ]
 },
 {
  "qid": "qaf464edc2a",
  "kind": "yes/no",
  "text": "Claim: A five piece band in the \"Art Wave\" scene had the second studio album You Could Have It So Much Better. This band was based in the same city as the band Hey Everyone!.\n\nPassages:\n\n[Art Brut]\nNamed after French painter Jean Dubuffet's definition of outsider art - art by prisoners, loners, the mentally ill, and other marginalized people, and made without thought to imitation or presentation - South London's Art Brut were tagged by \"NME\" as part of the \"Art Wave\" scene that also included bands such as The Rakes, Franz Ferdinand and Bloc Party.\n\n[You Could Have It So Much Better]\nYou Could Have It So Much Better is the second studio album by Scottish indie rock band Franz Ferdinand.\n\n[Hey Everyone!]\nis the debut album by Glasgow-based rock band Dananananaykroyd, released on April 6, 2009, on the Best Before Records label.\n\n[Franz Ferdinand (band)]\nFranz Ferdinand are a Scottish rock band, formed in 2002 and based in Glasgow.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q433b80411d",
  "kind": "yes/no",
  "text": "Claim: The star of Only You (upcoming film) featured in this movie. Home on the Range is an American science-fiction fantasy movie. This movie is not.\n\nPassages:\n\n[Storm Reid]\nShe is set to portray Meg Murry in \"A Wrinkle in Time\" (2018).\n\n[Home on the Range (2004 film)]\nHome on the Range is a 2004 American animated musical western comedy film produced by Walt Disney Feature Animation and released by Walt Disney Pictures.\n\n[Only You (upcoming film)]\nThe film stars David Oyelowo, Storm Reid, Brian Tyree Henry, Alfred Molina, Mykelti Williamson and Shinelle Azoroh.\n\n[A Wrinkle in Time (2018 film)]\nA Wrinkle in Time is an upcoming American science-fiction fantasy adventure film directed by Ava DuVernay and written by Jennifer Lee.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q3e55810943",
  "kind": "yes/no",
  "text": "Claim: Walt Disney Pictures produced both the film that National Treasure: Book of Secrets is a sequel to and 1999 film The Computer Wore Tennis Shoes.\n\nPassages:\n\n[The Computer Wore Tennis Shoes]\nIt was produced by Walt Disney Productions and distributed by Buena Vista Distribution Company as part of \"The Last Laughs of the 1960s\".\n\n[National Treasure (film)]\nNational Treasure is a 2004 American adventure heist film produced and released by Walt Disney Pictures.\n\n[National Treasure: Book of Secrets]\nIt is a sequel to the 2004 film \"National Treasure\" and is the second part of the \"National Treasure\" franchise.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2603602f67",
  "kind": "yes/no",
  "text": "Tweet: Don't think it's possible to fully understand poetry without experiencing a New York winter.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q039a432ad2",
  "kind": "yes/no",
  "text": "Claim: The award that Kevin Sinfield won in the 2000's, is presented at a stadium located in the country of England.\n\nPassages:\n\n[AJ Bell Stadium]\nThe Salford City Stadium (referred to as the AJ Bell Stadium for sponsorship purposes) is a rugby stadium in Barton-upon-Irwell, Eccles, Salford, England.\n\n[Kevin Sinfield]\nSinfield played his entire professional career with Leeds and is one of the most successful players in Super League history, having captained the team to seven Super League championships and two Challenge Cup successes as well as achieving individual accolades as winner of the Lance Todd Trophy (2005), Harry Sunderland Trophy twice (2009, 2012) and the Golden Boot (2012), one of only four British-based players to achieve the latter.\n\n[Lance Todd Trophy]\nThe Lance Todd Trophy is presented at a celebratory dinner at the AJ Bell Stadium, home of the Salford Red Devils.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qef3d6b0227",
  "kind": "yes/no",
  "text": "Claim: Kim Dong-wook played an obsessed and tormented king in the 2012 South Korean historical film directed by Kim Dae-seung.\n\nPassages:\n\n[Kim Dong-wook]\nHe then starred in \"Happy Killers\" (2010) and \"Romantic Heaven\" (2011), but it was his acclaimed performance as an obsessed and tormented king in 2012 period drama \"The Concubine\" that brought Kim the best reviews of his career yet.\n\n[The Concubine (film)]\n\"Royal Concubine: Concubine to the King\") is a 2012 South Korean historical film directed by Kim Dae-seung.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q70e02b77a0",
  "kind": "yes/no",
  "text": "Claim: Brady Seals has released more solo albums than the entertainer who Avril Lavigne featured on the song Get Over Me with.\n\nPassages:\n\n[Get Over Me]\n\"Get Over Me\" is a song by American singer and songwriter Nick Carter featuring Canadian singer Avril Lavigne.\n\n[Brady Seals]\nBrady Seals (born March 29, 1969) is an American country music artist. A fourth solo album, \"Play Time\", was released in 2009 via Star City.\n\n[Nick Carter (musician)]\nNickolas Gene \"Nick\" Carter (born January 28, 1980) is an American singer, songwriter, actor, and dancer. As of 2015, Carter has released three solo albums, \"Now or Never\", \"I'm Taking Off\" and \"All American\" during breaks between Backstreet Boys schedules, and a collaboration with Jordan Knight titled \"Nick & Knight\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q64dac05055",
  "kind": "yes/no",
  "text": "Claim: The creator of the character, for whom Helena Štáchováwas provided the Czech-language voice of, was born in July, 1954.\n\nPassages:\n\n[Helena Štáchová]\nNotably, Štáchová provided the Czech language-voice of Lisa Simpson on the Czech version of the American animated sitcom, \"The Simpsons\".\n\n[Matt Groening]\nMatthew Abraham \"Matt\" Groening ( ; born February 15, 1954) is an American cartoonist, writer, producer, animator, and voice actor.\n\n[Lisa Simpson]\nCartoonist Matt Groening created and designed her while waiting to meet James L. Brooks.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q33ac226eaf",
  "kind": "yes/no",
  "text": "Claim: Verona directed the 1979 American drama film that starred the actress who won the Golden Globe Award for Best Supporting Actress for \"Psycho\".\n\nPassages:\n\n[Boardwalk (film)]\nBoardwalk is a 1979 American drama film written by Stephen Verona and Leigh Chapman and directed by Verona.\n\n[Janet Leigh]\nShe is best remembered for her performance in \"Psycho\", for which she was awarded the Golden Globe Award for Best Supporting Actress and received an Academy Award nomination.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4ce6da1e77",
  "kind": "yes/no",
  "text": "Text: Watched 127 hours... Kinda reminded me of this one time I got a bad splinter. Writing a book about it now, hit me up for an autographed copy",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qd081bc3ced",
  "kind": "yes/no",
  "text": "Claim: Antoinette Sandbach resigned as the Welsh Assembly Member for the Wales region to represent Eddisbury in the House of Commons in the UK Parliament in 2015.\n\nPassages:\n\n[Eddisbury (UK Parliament constituency)]\nEddisbury is a constituency in Cheshire represented in the House of Commons of the UK Parliament since 2015 by Antoinette Sandbach, a Conservative.\n\n[Antoinette Sandbach]\nThe following day, 8 May 2015, she resigned as the Welsh Assembly Member for the North Wales region.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9e806b701a",
  "kind": "yes/no",
  "text": "Claim: The travel hub is a mile south of the area KJAL is licensed to. Along with Hoonah Airport, which is also a mile south, are both on American territory.\n\nPassages:\n\n[Tafuna, American Samoa]\nIt is located on a peninsula a mile north of Pago Pago International Airport and one mile south of Nu'uuli, American Samoa.\n\n[Hoonah Airport]\nHoonah Airport (IATA: HNH, ICAO: PAOH, FAA LID: HNH) is a state-owned public-use airport located one nautical mile (2 km) southeast of the central business district of Hoonah, Alaska.\n\n[Pago Pago International Airport]\nPago Pago International Airport (IATA: PPG, ICAO: NSTU, FAA LID: PPG) , also known as Tafuna Airport, is a public airport located 7 miles (11.3 km) southwest of the central business district of Pago Pago, in the village and plains of Tafuna on the island of Tutuila in American Samoa, an unincorporated territory of the United States.\n\n[KJAL]\nLicensed to Tafuna, American Samoa, it served the American Samoa area.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd01c16d781",
  "kind": "yes/no",
  "text": "Claim: This individual played with Steve Denton in the 1983 Dallas Open – Doubles. He and Ekaterina Makarova are not from the same country.\n\nPassages:\n\n[Sherwood Stewart]\nSherwood Stewart (born June 6, 1946, in Goose Creek, Texas, United States) played amateur and professional tennis in the 1970s and 1980s.\n\n[Ekaterina Makarova]\nEkaterina Valeryevna Makarova (Russian: Екатери́на Вале́рьевна Мака́рова ; ] ; born on 7 June 1988) is a Russian professional tennis player.\n\n[1983 Dallas Open – Doubles]\nNduka Odizor and Van Winitsky won in the final 6–3, 7–5 against Steve Denton and Sherwood Stewart.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7181c2a976",
  "kind": "yes/no",
  "text": "Claim: Timothy Simon \"Tim\" Roth gained recognition earlier than the mother of a Nickelodeon duo. Boris Pelekh worked with this duo from 2008 - 2011.\n\nPassages:\n\n[Nat and Alex Wolff]\nThe siblings are known for their work on the Nickelodeon television series \"The Naked Brothers Band\", which was created and produced by their mother, actress Polly Draper.\n\n[Tim Roth]\nTimothy Simon \"Tim\" Roth (born 14 May 1961) is an English actor and director. He garnered critical acclaim for his role as Myron in the 1984 film \"The Hit\" (1984), for which he was nominated for his first BAFTA Award.\n\n[Boris Pelekh]\nAside from his work in Gogol Bordello, he also worked with the Nickelodeon duo Nat and Alex Wolff from 2008 - 2011.\n\n[Polly Draper]\nShe first gained recognition for her role in the ABC primetime television drama \"Thirtysomething\" (1987–91).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc34cf32c9d",
  "kind": "yes/no",
  "text": "Claim: A club has hosted matches at the all-seater BayArena since 1958. This club has Willibert Kremer as a scout.\n\nPassages:\n\n[Bayer 04 Leverkusen]\nThe club plays in the Bundesliga, the top tier of the German football league system, and hosts matches at the BayArena.\n\n[Willibert Kremer]\nWillibert Kremer (born 15 October 1939 in Hochneukirch) is a German football coach and a former player who currently works as a scout with Bayer 04 Leverkusen.\n\n[BayArena]\nBayArena (] ) is a football stadium in Leverkusen, North Rhine-Westphalia, Germany, which has been the home ground of Bundesliga club Bayer Leverkusen since 1958.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1261a3169f",
  "kind": "yes/no",
  "text": "Claim: Actor and photographer Ramanaidu Daggubati starred in Bangalore Naatkal.\n\nPassages:\n\n[Rana Daggubati]\nRamanaidu Daggubati (born 14 December 1984), also known by his stage name Rana Daggubati or simply, Rana, is an Indian actor, producer, visual effects co-ordinator and photographer.\n\n[Bangalore Naatkal]\nIt also stars Rana Daggubati, Raai Laxmi, Parvathy and Samantha in other pivotal roles.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q78847470d6",
  "kind": "yes/no",
  "text": "Claim: \"HMS \"Sussex\" was an 80-gun third-rate ship, of the line of the English Royal Navy, for the Kingdom of England on the island of Great Britain from the 10th century—when it emerged from various Anglo-Saxon kingdoms—until 1707, when it united with Scotland to form the Kingdom of Great Britain.\n\nPassages:\n\n[Kingdom of England]\nThe Kingdom of England was a sovereign state on the island of Great Britain from the 10th century—when it emerged from various Anglo-Saxon kingdoms—until 1707, when it united with Scotland to form the Kingdom of Great Britain.\n\n[HMS Sussex (1693)]\nOn board were possibly 10 tons of gold coins.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8737056074",
  "kind": "yes/no",
  "text": "Tweet: do people with clear skin feel accomplished?? superior??? comfortable in their own skin???? what’s that like lmfao",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q83c5ee0122",
  "kind": "yes/no",
  "text": "Text: Markets already down",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q0f79f8ab48",
  "kind": "yes/no",
  "text": "Claim: The University which carries the name of Nobel Prize winner William Taylor is located in Upland, Indiana, United States.\n\nPassages:\n\n[William Taylor (bishop)]\nTaylor University, a Christian college in Indiana, carries his name.\n\n[Taylor University]\nTaylor University is a private, interdenominational, evangelical Christian college in Upland, Indiana, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd5938282b2",
  "kind": "yes/no",
  "text": "Claim: The final film in the Rocky film series features the boxer who held the WBC cruiserweight title.\n\nPassages:\n\n[Creed (film)]\nIt also features Tessa Thompson, Phylicia Rashād, Tony Bellew and Graham McTavish.\n\n[Rocky (film series)]\nThe films by order of release date are: \"Rocky\" (1976), \"Rocky II\" (1979), \"Rocky III\" (1982), \"Rocky IV\" (1985), \"Rocky V\" (1990), \"Rocky Balboa\" (2006) and \"Creed\" (2015).\n\n[Tony Bellew]\nHe held the WBC cruiserweight title from 2016 to 2017, and previously the British and Commonwealth light-heavyweight titles between 2010 and 2014, and the European cruiserweight title from 2015 to 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qca5948c0cf",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Great time for sim and I to have our weekly life update.... 🌛🌜🐨 (closest thing to an owl) 💤💤💤💤💤😴",
   "So late for Sim and I to have our weekly life update!"
  ]
 },
 {
  "qid": "qf095ad35be",
  "kind": "yes/no",
  "text": "Tweet: @PONOS_EN Tankful for my 20+90 Tank Cat",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd9c81760d5",
  "kind": "yes/no",
  "text": "Claim: Queen Margrethe II is the mother of a former graduate of Taroona High School.\n\nPassages:\n\n[Taroona High School]\nThe school's most notable former student is Mary, Crown Princess of Denmark.\n\n[Frederik, Crown Prince of Denmark]\nFrederik is the elder son of Queen Margrethe II and Henrik, the Prince Consort.\n\n[Mary, Crown Princess of Denmark]\nMary, Crown Princess of Denmark, Countess of Monpezat, {'1': \", '2': \", '3': 'R.E.', '4': \"} (Mary Elizabeth; \"née\" Donaldson; born 5 February 1972) is the wife of Frederik, Crown Prince of Denmark.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qcdfb6e2be8",
  "kind": "yes/no",
  "text": "Text: I am late to the same lecture every single week it's so embarrassing",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qdb41f09f82",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "How nice of tonsillitis to join me on my holiday 🖕🏻🖕🏻🖕🏻🖕🏻",
   "I hate that I got tonsillitis while on holiday"
  ]
 },
 {
  "qid": "qf096c9e5a0",
  "kind": "yes/no",
  "text": "Claim: The tennis player Kenneth or Ken Eliot Flach is from a country closer to Ontario Canada than the woman who defeated Maria Sharapova in the 2015 French Open- Women's Singles.\n\nPassages:\n\n[Ken Flach]\nKenneth Eliot Flach (born May 24, 1963) is a former professional tennis player from the United States.\n\n[2015 French Open – Women's Singles]\nMaria Sharapova was the defending champion, but lost in the fourth round to Lucie Šafářová.\n\n[Lucie Šafářová]\nLucie Šafářová (] ; born 4 February 1987) is a Czech professional tennis player from Brno.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7d758fae27",
  "kind": "yes/no",
  "text": "Claim: An American football quarterback for the Chicago Bears was a star of a game released on July 14, 2009.\n\nPassages:\n\n[Mark Sanchez]\nMark Travis John Sanchez (born November 11, 1986) is an American football quarterback for the Chicago Bears of the National Football League (NFL).\n\n[NCAA Football 10]\nNCAA Football 10 is a college football video game created by Electronic Arts. It was released on July 14, 2009 for the Xbox 360, PlayStation 3, PlayStation Portable, and PlayStation 2 consoles. Brian Johnson, Brian Orakpo, Mark Sanchez, and Michael Crabtree were the cover athletes for the game.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q20acbe565d",
  "kind": "yes/no",
  "text": "Claim: The composer of Lux Aurunque was born December 2nd, 1970.\n\nPassages:\n\n[Eric Whitacre]\nEric Edward Whitacre (born January2, 1970) is a Grammy-winning American composer, conductor, and speaker, known for his choral, orchestral and wind ensemble music.\n\n[Lux Aurumque]\nLux Aurumque (\"Light and Gold\", sometimes \"Light of Gold\") is a choral composition in one movement by Eric Whitacre.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q97e357b114",
  "kind": "yes/no",
  "text": "Text: really honoured to have shared a coach today with a group of girls who didn’t know downing street was real and thought the prime minister and the queen lived together at buckingham palace",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qe2d3819cda",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "alright I’m ready for some march madness🏀🔥",
   "I was ready for some march madness, then COVID happened"
  ]
 },
 {
  "qid": "q234a1b783a",
  "kind": "yes/no",
  "text": "Claim: The track where the 2013 Liqui Moly Bathurst 12 Hour was staged is 6.213 km long.\n\nPassages:\n\n[2013 Liqui Moly Bathurst 12 Hour]\nThe 2013 Liqui Moly Bathurst 12 Hour was an endurance race for a variety of GT and touring car classes, including: GT3 cars, GT4 cars, Group 3E Series Production Cars and Dubai 24 Hour cars. The event, which was staged at the Mount Panorama Circuit, near Bathurst, in New South Wales, Australia on 10 February 2013, was the eleventh running of the Bathurst 12 Hour.\n\n[Mount Panorama Circuit]\nMount Panorama Circuit is a motor racing track located in Bathurst, New South Wales, Australia. The 6.213 km long track is technically a street circuit, and is a public road, with normal speed restrictions, when no racing events are being run, and there are many residences which can only be accessed from the circuit.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf7983ed3b2",
  "kind": "yes/no",
  "text": "Claim: The singer of the live album \" Live at the Corner Hotel\" and Kyle Patrick were both in The Click Five.\n\nPassages:\n\n[Live at the Corner Hotel]\nLive at the Corner Hotel (2008) is a live album by Canadian singer/songwriter Jeff Martin.\n\n[Kyle Patrick]\nKyle Patrick Dickherber (born May 20, 1986, Atlanta, Georgia, United States) is an American singer-songwriter, multi-instrumentalist and producer, best known as the lead singer of Boston power pop band, The Click Five.\n\n[Jeff Martin (Canadian musician)]\nJeffrey Scott Martin (born October 2, 1969 in Windsor, Ontario) is a Canadian guitarist and singer-songwriter best known for fronting the rock band The Tea Party. Martin began his career as a solo artist in October 2005, when The Tea Party went on hiatus.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q98f8031056",
  "kind": "yes/no",
  "text": "Claim: The star of The Big Year acted in a film with martial arts expert Tom Wu. He also voiced Lightning McQueen in the \"Cars\" franchise.\n\nPassages:\n\n[Shanghai Knights]\nDirected by David Dobkin and written by Alfred Gough and Miles Millar, it stars Jackie Chan and Owen Wilson.\n\n[The Big Year]\nThe Big Year is a 2011 American comedy film directed by David Frankel, written by Howard Franklin and starring Jack Black, Steve Martin, and Owen Wilson.\n\n[Tom Wu]\nHe is a martial arts expert who has appeared in films such as \"Revolver\", \"Shanghai Knights\", \"Batman Begins\" and the Bollywood sci-fi movie \"Ra.One\".\n\n[Owen Wilson]\nHe starred with Ben Stiller in numerous films, and is known for his roles in Frat Pack comedies and as well as voicing Lightning McQueen in the \"Cars\" franchise.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3f97c6d7f0",
  "kind": "yes/no",
  "text": "Claim: Pinnacle Airlines Flight 3701 was headed to a freight airport when it crashed. That airport is farther east than Cheyenne Regional Airport.\n\nPassages:\n\n[Minneapolis–Saint Paul International Airport]\nMinneapolis–Saint Paul International Airport (IATA: MSP, ICAO: KMSP, FAA LID: MSP) , also known as Wold–Chamberlain Field, is a joint civil-military public use international airport.\n\n[Cheyenne Regional Airport]\nCheyenne Regional Airport (IATA: CYS, ICAO: KCYS, FAA LID: CYS) (Jerry Olson Field) is a civil-military airport a mile north of downtown Cheyenne, in Laramie County, Wyoming.\n\n[Pinnacle Airlines Flight 3701]\nIt was an overnight repositioning flight with no passengers from Little Rock, Arkansas, U.S. to Minneapolis–Saint Paul International Airport, U.S. Both crew members were killed.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa6f58d93dc",
  "kind": "yes/no",
  "text": "Post: Is spunk a slur?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qe4da5ed3d8",
  "kind": "yes/no",
  "text": "Claim: The home ground of Fort Glanville Conservation Park, which is located in Semaphore Park, United FC is sponsored by a brewery that sold 69.7 million litres of beer in 2013. Semaphore Park is a seaside suburb.\n\nPassages:\n\n[Fort Glanville Conservation Park]\nFort Glanville Conservation Park is a protected area located in the Australian state of South Australia located in Semaphore Park, a seaside suburb of Adelaide consisting of a functional 19th century fort listed on the South Australian Heritage Register and some adjoining land.\n\n[Hindmarsh Stadium]\nThe Hindmarsh Stadium (currently known as the Coopers Stadium due to sponsorship from the Adelaide-based Coopers Brewery) is a multi-purpose stadium located in Adelaide, South Australia.\n\n[Adelaide United FC]\nAdelaide United's home ground is Hindmarsh Stadium.\n\n[Coopers Brewery]\nThe brewery sold 69.7 million litres of beer in the 2013 financial year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5e93754aeb",
  "kind": "yes/no",
  "text": "Claim: The Keoni Waxman film, that included screen credits for J. F. Lawton, was Oscar nominated for Best Sound.\n\nPassages:\n\n[Under Siege]\nIt stars Steven Seagal as an ex-Navy SEAL who must stop a group of mercenaries, led by Tommy Lee Jones and Gary Busey, on the U.S. Navy battleship USS \"Missouri\".\n\n[J. F. Lawton]\nHis screen credits include the box office hit \"Pretty Woman\", \"Mistress\", \"Blankman\", \"Under Siege\", \"\", \"The Hunted\", \"Chain Reaction\", \"\", \"Jackson\", and the TV series \"V.I.P.\" Under the assumed name \"J.D. Athens\", he wrote and directed \"Cannibal Women in the Avocado Jungle of Death\" and \"Pizza Man\".\n\n[Rick Hart (sound engineer)]\nHe was nominated for an Academy Award in the category Best Sound for the film \"Under Siege\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5233a91951",
  "kind": "yes/no",
  "text": "Claim: The Neoclassical monument Benito Juárez Hemicycle is located in this city of Mexico that consists of sixteen municipalities.\n\nPassages:\n\n[Benito Juárez Hemicycle]\nThe Benito Juárez Hemicycle is a Neoclassical monument located at the Alameda Central park in Mexico City, Mexico and commemorating the Mexican statesman Benito Juárez.\n\n[Mexico City]\nThe city consists of sixteen municipalities.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0207e4afcc",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Excuse me but I think that you have made a spelling error on your last comment there.",
   "@Schlippertysch1 @anon_opin Very good. Just need to work on your spelling now 👍"
  ]
 },
 {
  "qid": "q01986222aa",
  "kind": "yes/no",
  "text": "Claim: FeliCa was utilized in a transit system in Hong Kong. The system was available before the No Card.\n\nPassages:\n\n[FeliCa]\nFirst utilized in the Octopus card system in Hong Kong, the technology is used in a variety of cards also in countries such as Singapore, Japan and the United States.\n\n[Octopus card]\nThe Octopus card () is a reusable contactless stored value smart card for making electronic payments in online or offline systems in Hong Kong. Launched in September 1997 to collect fares for the territory's mass transit system, the Octopus card system is the second contactless smart card system in the world, after the Korean Upass, and has since grown into a widely used payment system for all public transport in Hong Kong, leading to the development of Oyster Card in London.\n\n[Nol Card]\nThe Nol Card is an electronic ticketing card that was released in for all mode of public transport in Dubai services, on August 2009.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9762626912",
  "kind": "yes/no",
  "text": "Claim: Beethoven regarded Luigi Cherubini as the greatest of his brothers, but not Franz Schreker.\n\nPassages:\n\n[Luigi Cherubini]\nLuigi Cherubini (] ; 8 or 14 September 1760 – 15 March 1842) was an Italian composer who spent most of his working life in France. Beethoven regarded Cherubini as the greatest of his contemporaries.\n\n[Franz Schreker]\nFranz Schreker (originally \"Schrecker\"; 23 March 1878, Monaco – 21 March 1934, Berlin) was an Austrian composer, conductor, teacher and administrator.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe56b328ba5",
  "kind": "yes/no",
  "text": "Claim: The bassist of the group, who released \"Mothers Talk\", sang on the band's song \"Change\". Rock singer John Michael \"Ozzy\" Osbourne has released more solo albums than him.\n\nPassages:\n\n[Mothers Talk]\n\"Mothers Talk\" is a 1984 song by the British band Tears for Fears.\n\n[Change (Tears for Fears song)]\nWritten by Roland Orzabal and sung by bassist Curt Smith, it was the band's fourth single release.\n\n[Ozzy Osbourne]\nJohn Michael \"Ozzy\" Osbourne (born 3 December 1948) is an English singer, songwriter, and actor. He was fired from Black Sabbath in 1979 and went on to have a successful solo career, releasing 11 studio albums, the first seven of which were all awarded multi-platinum certifications in the US.\n\n[Curt Smith]\nAs a solo artist, he has released four solo albums.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q245aa0fa9e",
  "kind": "yes/no",
  "text": "Claim: Kool Keith, an artist typical of Afro-Surrealism, was born October 7, 1963.\n\nPassages:\n\n[Afro-Surrealism]\nNotable practitioners of Afro-Surrealism include Bob Kaufman, Krista Franklin, Kool Keith, Samuel R. Delany, Roman Bearden and Deana Lawson.\n\n[Kool Keith]\nKeith Thornton (born October 7, 1963), better known by his stage name Kool Keith, is an American rapper from The Bronx, New York known for his surreal, abstract and often profane or incomprehensible lyrics.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q62ccfa84c6",
  "kind": "yes/no",
  "text": "Claim: The man that the statue Armistead Monument is for commanded a fort during a conflict. It was first built in 1798. The 1804 ship HMS Volcano was involved in the conflict.\n\nPassages:\n\n[Fort McHenry]\nFort McHenry, in Baltimore, Maryland, is a historical American coastal pentagonal bastion fort best known for its role in the War of 1812, when it successfully defended Baltimore Harbor from an attack by the British navy from the Chesapeake Bay September 13–14, 1814. It was first built in 1798 and was used continuously by U.S. armed forces through World War I and by the Coast Guard in World War II.\n\n[Armistead Monument]\nThe Armistead Monument is a bronze statue of Col. George Armistead, by Edward Berge.\n\n[George Armistead]\nGeorge Armistead (April 10, 1780 – April 25, 1818) was an American military officer who served as the commander of Fort McHenry during the Battle of Baltimore in the War of 1812.\n\n[HMS Volcano (1804)]\nAs \"Volcano\" she served during the War of 1812, and in particular participated in the Battle of Baltimore.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q00154c8722",
  "kind": "yes/no",
  "text": "Claim: The man that composed the opera Irrelohe was also a teacher. The composer, who American Violinist Tim Fain is best known for working with, was not.\n\nPassages:\n\n[Philip Glass]\nPhilip Morris Glass (born January 31, 1937) is an American composer.\n\n[Irrelohe]\nIrrelohe is an opera in three acts by the Austrian composer Franz Schreker, libretto by the composer.\n\n[Tim Fain]\nTim Fain is an American violinist, perhaps best known for his performances in the movie \"Black Swan\" and his work with American composer Philip Glass.\n\n[Franz Schreker]\nFranz Schreker (originally \"Schrecker\"; 23 March 1878, Monaco – 21 March 1934, Berlin) was an Austrian composer, conductor, teacher and administrator.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5f746c474d",
  "kind": "yes/no",
  "text": "Claim: Kyle Schickner and another director are of the same nationality. This other director wrote and directed one of the thrillers produced by the Filmways company.\n\nPassages:\n\n[Filmways]\nNotable films the company produced include \"The Sandpiper\", \"The Cincinnati Kid\", \"The Fearless Vampire Killers\", \"Ice Station Zebra\", \"Summer Lovers\", \"The Burning\", \"King\" and Brian De Palma's \"Dressed to Kill\" and \"Blow Out\".\n\n[Summer Lovers]\nSummer Lovers is a 1982 American romantic comedy film written and directed by Randal Kleiser, starring Peter Gallagher, Daryl Hannah and Valerie Quennessen.\n\n[Kyle Schickner]\nKyle Schickner is an American film producer, writer, director, actor and a bisexual civil rights activist.\n\n[Randal Kleiser]\nJohn Randal Kleiser (born July 20, 1946) is an American film director and producer, best known for directing the 1978 musical romantic comedy film \"Grease\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 }
]
