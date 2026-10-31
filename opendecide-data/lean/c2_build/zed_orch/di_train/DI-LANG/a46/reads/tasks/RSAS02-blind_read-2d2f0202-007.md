# A46 replay label-noise blind read RSAS02-blind_read-2d2f0202-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS02-blind_read-2d2f0202-007.json

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
  "qid": "qfcc0bfc12c",
  "kind": "yes/no",
  "text": "Claim: WWF The Music, Vol. 5 is a soundtrack album whose songs were composed and performed by an American music composer best known for his work with WWE (formerly WWF) from March 1985 onward.\n\nPassages:\n\n[WWF The Music, Vol. 5]\nWWF The Music, Vol. 5 is a soundtrack album by WWE (then known as the World Wrestling Federation, or WWF). Released on February 20, 2001 by Koch Records, it features entrance theme music of various WWE superstars, all of which were composed and performed by Jim Johnston (with the exception of one song, performed by Motörhead).\n\n[Jim Johnston (composer)]\nJames Alan \"Jim\" Johnston (born 1959) is an American music composer best known for his work with WWE (formerly WWF) from 1985 onwards.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd177ac2a44",
  "kind": "yes/no",
  "text": "Claim: Alexandra Röseler recorded klassischen Deutschen's cantata, \"O heilges Geist- und Wasserbad\", BWV 165, with a high-lying bass singer and conductor. This high-lying bass singer and conductor is from a city. Hans Krell died in the city.\n\nPassages:\n\n[Gotthold Schwarz]\nBased in Leipzig, he started as a member of the Thomanerchor and has conducted the Gewandhausorchester.\n\n[Bass-baritone]\nA bass-baritone is a high-lying bass or low-lying \"classical\" baritone voice type which shares certain qualities with the true baritone voice.\n\n[Alexandra Röseler]\nIn 2003 she recorded Bach's cantata, \"O heilges Geist- und Wasserbad\", BWV 165, with Gotthold Schwarz, Thomanerchor, Gewandhausorchester, Heike Kumlin and Martin Krumbiegel, singing the alto part.\n\n[Hans Krell]\nHe is thought to have been born in Crailsheim or Ansbach, and died in Leipzig.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q22e95a8859",
  "kind": "yes/no",
  "text": "Post: because my neighbours are just so unbelievably loud as of recent I’m whacking out my speaker and blasting Harry Styles. modern problems require modern solutions",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe32951f8a7",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Great start to the day Neros was shut and now I'm going akip on the bus 😴😵",
   "I had the worst start to the day as cafe nero was shut and I couldn’t get a coffee"
  ]
 },
 {
  "qid": "q9dfa294e13",
  "kind": "yes/no",
  "text": "Claim: The auto racing series held from 2014 to 2012 was followed on by the 2016 Blancpain GT Series Sprint Cup.\n\nPassages:\n\n[FIA GT1 World Championship]\nThe FIA GT1 World Championship was a world championship sports car racing series developed by the SRO Group and regulated by the Fédération Internationale de l'Automobile (FIA), held from 2010 to 2012.\n\n[2016 Blancpain GT Series Sprint Cup]\nThe 2016 Blancpain GT Series Sprint Cup was the fourth season following on from the demise of the SRO Group's FIA GT1 World Championship (an auto racing series for grand tourer cars), the third with the designation of Blancpain Sprint Series or Blancpain GT Series Sprint Cup.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q36af4d5c65",
  "kind": "yes/no",
  "text": "Claim: The host of the awards ceremony where Demi Lovato was named Choice Summer TV Star for her role as Aria Montgomery currently stars on The Big Bang Theory.\n\nPassages:\n\n[2011 Teen Choice Awards]\nThe 2011 Teen Choice Awards ceremony, hosted by Kaley Cuoco, aired live on August 7, 2011 at 8/7c on Fox.\n\n[Kaley Cuoco]\nSince 2007, she has starred as Penny on the CBS sitcom \"The Big Bang Theory\", for which she has received Satellite, Critics' Choice, and People's Choice Awards.\n\n[Aria Montgomery]\nLucy Hale was named Choice Summer TV Star: Female at the 2010 Teen Choice Awards and 2011 Teen Choice Awards for her role in the series.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4c0b7fcbfa",
  "kind": "yes/no",
  "text": "Claim: The 2010 population of the 19th-century town where Gale constructed houses, and also constructed in Amherst Avenue Historic District, is located was 5,042\n\nPassages:\n\n[Ticonderoga, New York]\nTiconderoga is a town in Essex County, New York, United States. The population was 5,042 at the 2010 census.\n\n[Lake George Avenue Historic District]\nLake George Avenue Historic District is a national historic district located at Ticonderoga, in Essex County, New York.\n\n[Amherst Avenue Historic District]\nGale also constructed the houses in the Lake George Avenue Historic District.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6d6013e916",
  "kind": "yes/no",
  "text": "Claim: The novelist that wrote the collection of ten short stories called The Watchful Gods and Other Stories is American. The writer of Where the Heart Is (novel) is also American.\n\nPassages:\n\n[Where the Heart Is (novel)]\nWhere the Heart Is is a 1995 novel by Billie Letts.\n\n[Walter Van Tilburg Clark]\nWalter Van Tilburg Clark (August 3, 1909 – November 10, 1971) was an American novelist, short story writer, and educator.\n\n[The Watchful Gods and Other Stories]\nThe Watchful Gods and Other Stories is a collection of short stories by Walter Van Tilburg Clark published in 1950.\n\n[Billie Letts]\nBillie Dean Letts (née Gipson; May 30, 1938 – August 2, 2014) was an American novelist and educator.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q60a010c43b",
  "kind": "yes/no",
  "text": "Claim: Major General Walter E. Lauer commanded this unit in a conflict. This unit from world war 2 had a twenty year old lieutenant. The Enemy Strikes is a documentary about the conflict.\n\nPassages:\n\n[Walter E. Lauer]\nDuring World War II he commanded the 99th Infantry Division in the Battle of the Bulge.\n\n[99th Infantry Division (United States)]\nThe 99th Infantry Division was a unit of the United States Army in World War II.\n\n[Lyle Bouck]\nLyle Joseph Bouck, Jr. (December 17, 1923 – December 2, 2016) enlisted in the U.S. National Guard at age 14.\n\n[The Enemy Strikes]\nis a short propaganda film made in 1945 about the Battle of the Bulge.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2b8417dd90",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "Broke: doing assignments in order of due date Woke: doing assignments in order of priority Wired: spending 20 minutes on each class at a time and just go down the list",
   "The best way to do assignments is in order of priority. The second best is in terms of due date. The worst is doing 20 minutes on each class at a time, regardless of priority."
  ]
 },
 {
  "qid": "qea9815f9a4",
  "kind": "yes/no",
  "text": "Claim: A wrestling group member that was born on March 1, 1987 in New England was Kyle O'Reilly. This wrestling group once won the ROH Tag Wars Tournament.\n\nPassages:\n\n[ReDRagon]\nreDRagon is a professional wrestling tag team consisting of Bobby Fish and Kyle O'Reilly.\n\n[Kyle O'Reilly]\nKyle Greenwood (born March 1, 1987) is a Canadian professional wrestler better known by the ring name Kyle O'Reilly, he is currently signed to WWE, where he performs in its developmental branch NXT.\n\n[ROH Tag Wars Tournament]\nTag Wars (formerly Trios Tournament) is a professional wrestling event held by Ring of Honor as a one-night tournament in 2005, 2006, 2010 and 2014 with the winners being Jimmy Rave, Alex Shelley and Abyss, The Kings of Wrestling and ReDRagon respectively.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf8fa334751",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Get ready for the next big horror game this season, Slender Suburban Man",
   "Id say something along the lines of \"thank god theres not a game out there called Slender Suburban Man\""
  ]
 },
 {
  "qid": "qc0515e7250",
  "kind": "yes/no",
  "text": "Claim: The co-star of the film Death Valley Outlaws stared in a tv series, Gunsmoke, created by John Meston.\n\nPassages:\n\n[Death Valley Outlaws]\nThe film stars Don \"Red\" Barry, Lynn Merrick, Milburn Stone, Bob McKenzie, Karl Hackett and Rex Lease.\n\n[Milburn Stone]\nHugh Milburn Stone, sometimes known as Milly Stone (July 5, 1904 – June 12, 1980), was an American film and television actor best known as \"Doc\" (Dr. Galen Adams) on the CBS western series \"Gunsmoke\".\n\n[Gunsmoke]\nGunsmoke is an American radio and television Western drama series created by director Norman Macdonnell and writer John Meston.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7ef9c80230",
  "kind": "yes/no",
  "text": "Claim: The star of Split Image (film) played Ben Meechum in this 1995 movie. Both the tragic hero as a protagonist and that film are dramas.\n\nPassages:\n\n[Michael O'Keefe]\nMichael O'Keefe (born Raymond Peter O'Keefe, Jr.; April 24, 1955) is an American film and television actor, known for his roles as Danny Noonan in \"Caddyshack\" and Ben Meechum in \"The Great Santini\" — for which he received a Golden Globe Award for New Star of the Year, as well as a nomination for the Academy Award for Best Supporting Actor.\n\n[Split Image (film)]\nDirected by Ted Kotcheff, and starring Michael O'Keefe, Karen Allen, Peter Fonda, James Woods, Elizabeth Ashley, Brian Dennehy and Ronnie Scribner.\n\n[Tragic hero]\nA tragic hero is the protagonist of a tragedy in drama.\n\n[The Great Santini]\nThe Great Santini is a 1979 American drama film written and directed by Lewis John Carlino, based on the 1976 novel of the same name by Pat Conroy.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7e41ab858d",
  "kind": "yes/no",
  "text": "Claim: Arnel Campaner Pineda was born before Trace Cyrus.\n\nPassages:\n\n[Trace Cyrus]\nTrace Dempsey Cyrus (born Neil Timothy Helson; February 24, 1989) is an American musician.\n\n[Arnel Pineda]\nArnel Campaner Pineda (born September 5, 1967) is a Filipino singer and songwriter.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q83e8e71fee",
  "kind": "yes/no",
  "text": "Text: It was bad enough when some corporate wankers took one of the trains I used to drive and made it a \"breakout area\" for their offices, but this? This is next level https://t.co/oBMypPVVgy https://t.co/SEdGsH3irZ",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q88a93fa2d4",
  "kind": "yes/no",
  "text": "Text: y’all were all vote-blue-no-matter-who till bernie sanders dropped out . hmmm where’s that same energy 😔😪😭",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q055611fdbf",
  "kind": "yes/no",
  "text": "Claim: 1998's Anatomy 2 was directed by this film director. He has fewer film credits than Jeremy Paul Kagan.\n\nPassages:\n\n[Jeremy Kagan]\nJeremy Paul Kagan (born December 14, 1945) is an American film and television director, screenwriter, and television producer.\n\n[Stefan Ruzowitzky]\nStefan Ruzowitzky (born 25 December 1961) is an Austrian film director and screenwriter.\n\n[Anatomy 2]\nAnatomy 2 (German: \"Anatomie 2\" ) is a 2003 German thriller film written and directed by Stefan Ruzowitzky.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q64b32738a5",
  "kind": "yes/no",
  "text": "Claim: Béla Viktor János Bartók was born before some people. Including the teacher of Vyacheslav Lavrent'yevich Nagovitsin.\n\nPassages:\n\n[Vyacheslav Nagovitsin]\nHe was a student of Dmitri Shostakovich at the Leningrad Conservatory that he graduated in 1966 (postgraduate school, he graduated from the undergraduate school of the Conservatory in 1963).\n\n[Béla Bartók]\nBéla Viktor János Bartók ( ; ] ; 25 March 1881 – 26 September 1945) was a Hungarian composer, pianist and an ethnomusicologist.\n\n[Dmitri Shostakovich]\nDmitri Dmitriyevich Shostakovich (Russian: Dmitriy Dmitrievich Shostakovich , ] ; 25 September [O.S. 12 September] 1906 9 August 1975) was a Russian composer and pianist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdadad59b21",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "you know what’s a novel concept? rapists and sexual assaulters not only ruin the lives of their victims but also THEIR OWN LIVES. yeah. not the victims testifying. maybe if you didn’t want rape accusations then DON’T RAPE. also a novel concept.",
   "Rapists ruin their own lives, not the victims testifying."
  ]
 },
 {
  "qid": "q3b45b01f9f",
  "kind": "yes/no",
  "text": "Claim: Robert Lewis \"Bob\" Pruett produced many high-profile National Football League players, including a wide reciver that holds the 2007 NFL record for first-season touchdown reception.\n\nPassages:\n\n[Randy Moss]\nRandy Gene Moss (born February 13, 1977) is a former American football wide receiver who played 14 seasons in the National Football League (NFL). He holds the NFL single-season touchdown reception record (23 in 2007), the NFL single-season touchdown reception record for a rookie (17 in 1998), and is second on the NFL all-time regular season touchdown reception list with 156.\n\n[Bob Pruett]\nRobert Lewis \"Bob\" Pruett (born June 20, 1943) is a former American football player and coach. Pruett has coached many high-profile National Football League players, including Randy Moss, Chad Pennington, and Byron Leftwich.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q88ebffa583",
  "kind": "yes/no",
  "text": "Claim: This song was written by the man who also wrote Then Who Am I and is featured on the fifth country studio album by the Oak Ridge Boys. This song was released on the album Ain't Living Long Like This.\n\nPassages:\n\n[Ain't Living Long Like This]\nThe songs, \"Elvira\", \"Baby Better Start Turnin' 'Em Down\" and \"(Now and Then, There's) A Fool Such as I\" were released as singles but they all failed to chart within the top 40.\n\n[Elvira (song)]\n\"Elvira\" is a song written by Dallas Frazier which became a famous country and pop hit by The Oak Ridge Boys in 1981, now considered one of their signature songs.\n\n[Then Who Am I]\n\"Then Who Am I\" is a song written by Dallas Frazier and A.L. \"Doodle\" Owens, and recorded by American country music artist Charley Pride.\n\n[Fancy Free (The Oak Ridge Boys album)]\nFancy Free is the fifth country studio album by the Oak Ridge Boys, released on March 26, 1981.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc58bf436a1",
  "kind": "yes/no",
  "text": "Claim: The artist who recorded Three Cord Opera has had 38 songs in the \"Billboard\" Adult Contemporary Top 10 between 1912 and 1946.\n\nPassages:\n\n[Three Chord Opera]\nThree Chord Opera is the twenty-fifth studio album by Neil Diamond.\n\n[Neil Diamond]\nWith 38 songs in the Top 10, he is the second most successful artist in the history of the \"Billboard\" Adult Contemporary Top 10 charts.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1370578876",
  "kind": "yes/no",
  "text": "Claim: Genesee Cream Ale is a cold fermented, alcohlic beverage produced by a facility located along the Genesee River.\n\nPassages:\n\n[Genesee Cream Ale]\nGenesee Cream Ale is a cold fermented, alcohlic beverage produced by the Genesee Brewing Company in Rochester, NY.\n\n[Genesee Brewing Company]\nGenesee Brewing Company is an American brewery located along the Genesee River in Rochester, New York.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb58b0f6815",
  "kind": "yes/no",
  "text": "Claim: Dorothy Vaughan, one of the women featured in the 2016 non-fiction book, Hidden Figures, become acting supervisor of the West Area Computers in 1949.\n\nPassages:\n\n[Hidden Figures (book)]\nHidden Figures: The American Dream and the Untold Story of the Black Women Who Helped Win the Space Race is a 2016 non-fiction book written by Margot Lee Shetterly. The biographical text follows the lives of Human Computers such as Katherine Johnson, Dorothy Vaughan, and Mary Jackson, three mathematicians\n\n[Dorothy Vaughan]\nDorothy Johnson Vaughan (September 20, 1910 – November 10, 2008) was an African American mathematician and human computer who worked for the National Advisory Committee for Aeronautics (NACA), and NASA, at Langley Research Center in Hampton, Virginia. In 1949, she became acting supervisor of the West Area Computers, the first African-American woman to supervise a group of staff at the center.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7c35c2dd16",
  "kind": "yes/no",
  "text": "Claim: The 1955 film, Davy Crockett, King of the Wild Frontier, had a prequel called Davy Crockett and the River Pirates, and Herbie Rides Again were both by Disney.\n\nPassages:\n\n[Davy Crockett, King of the Wild Frontier]\nDavy Crockett, King of the Wild Frontier is a 1955 live-action Walt Disney adventure film starring Fess Parker as Davy Crockett.\n\n[Davy Crockett and the River Pirates]\nThis film acts as a prequel to 1955's \"Davy Crockett, King of the Wild Frontier\" and is an edited compilation of the fourth and fifth stories featuring the Disney television series \"Davy Crockett\":\n\n[Herbie Rides Again]\nHerbie Rides Again is a 1974 American comedy film and a sequel to \"The Love Bug,\" released six years earlier, and the second in a series of films made by Walt Disney Productions starring an anthropomorphic (and quite autonomous) 1963 Volkswagen racing Beetle named Herbie.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4b5255979f",
  "kind": "yes/no",
  "text": "Tweet: Yeah, Lydia! Making Alaska proud 🇺🇸🏊‍♀️ https://t.co/V0YJDwKrt9",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd0d04f7f1b",
  "kind": "yes/no",
  "text": "Claim: Los Angeles Historic-Cultural Monument (No. 139) hosted an event by the IFBB professional bodybuilding organization on Oct 12, 1991.\n\nPassages:\n\n[1991 Ms. Olympia]\nThe 1991 Ms. Olympia contest was an IFBB professional bodybuilding competition was held on October 12 and 13, 1991 at the Shrine Auditorium in Los Angeles, California.\n\n[Shrine Auditorium]\nIt was designated a Los Angeles Historic-Cultural Monument (No. 139) in 1975.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe915bad77c",
  "kind": "yes/no",
  "text": "Claim: The black comedy sequel to \"Forgetting Sarah Marshall\" starred an Australian actress who started in the 2003 film \"The Rage in Placid Lake\" alongside Ben Lee.\n\nPassages:\n\n[Rose Byrne]\nMary Rose Byrne (born 24 July 1979) is an Australian actress. Byrne has also starred in the films \"Troy\", \"28 Weeks Later\", \"Knowing\", \"Insidious\", \"\", \"\", as well as the comedies \"Get Him to the Greek\", \"Bridesmaids\", \"Neighbors\", \"\", and \"Spy.\"\n\n[Get Him to the Greek]\nReleased on June 4, 2010, the film serves as a spin-off sequel of Stoller's 2008 film \"Forgetting Sarah Marshall\", reuniting director Stoller with stars Hill and Brand and producer Judd Apatow.\n\n[The Rage in Placid Lake]\nThe Rage in Placid Lake is a 2003 Australian film starring Ben Lee and Rose Byrne.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q655874e319",
  "kind": "yes/no",
  "text": "Claim: The word game, that Golden Secondary School hosts tournaments of, is originally distributed by a toy and game manufacturer that published more than 1,800 games.\n\nPassages:\n\n[Parker Brothers]\nParker Brothers was an American toy and game manufacturer which later became a brand of Hasbro. More than 1,800 games were published under the Parker Brothers name since 1883.\n\n[Golden Secondary School]\nCourses include things such as skiing and snowboarding on the beautiful Kicking Horse Mountain Resort, mountain biking on many trails around Golden and the school also hosts many bantam and senior basketball, volleyball and soccer teams, and Boggle tournaments.\n\n[Boggle]\nBoggle is a word game designed by Allan Turoff and originally distributed by Parker Brothers.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q408a806257",
  "kind": "yes/no",
  "text": "Claim: Sako Shahinian and Arshile Gorky are American-Armenian.\n\nPassages:\n\n[Arshile Gorky]\nArshile Gorky ( ; born Vostanik Manoug Adoian, Armenian: Ոստանիկ Մանուկ Ատոյեան ; April 15, 1904 – July 21, 1948) was an Armenian-American painter, who had a seminal influence on Abstract Expressionism.\n\n[Sako Shahinian]\nSako Shahinian (Armenian: Սաքո Շահինյան ; born 1980) is an American-Armenian illustrator whose artwork has been featured in System of a Down projects.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb808058f2f",
  "kind": "yes/no",
  "text": "Tweet: i've saved so much money by not eating out during this pandemic that i might have to buy random things just to keep my account balance humbled",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qdceb818b44",
  "kind": "yes/no",
  "text": "Text: roll n' square sausage and a cup of tea from Robyn's Nest on Maryhill Rd. AMAZING.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qab3b31e28e",
  "kind": "yes/no",
  "text": "Claim: The game which High Rollers Casino is a type been played outside of casinos.\n\nPassages:\n\n[High Rollers Casino]\nHigh Rollers Casino is a 2004 casino video game co-developed by Cinemaware and Virtual Toysfor the PlayStation 2 and Xbox gaming consoles.\n\n[Casino game]\nCasino games can also be played outside of casinos for entertainment purposes like in parties or in school competitions, some on machines that simulate gambling.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q47c8ed423c",
  "kind": "yes/no",
  "text": "Claim: Lari Michele White is the county music guitarist that first gained national attention as a winner on \"You Can Be a Star\". She then went on to provide background vocals on the first single of the album, that also featured the song \"He Would Be Sixteen\".\n\nPassages:\n\n[Now and Then (Michelle Wright album)]\nThe album's first single, \"Take It Like a Man\", became Wright's first number one hit on the Canadian \"RPM\" Country Tracks chart and her only top ten hit on the U.S. \"Billboard\" Hot Country Singles & Tracks chart.\n\n[Take It Like a Man (Michelle Wright song)]\n\"Take It Like a Man\" is a song written by Tony Haselden, and recorded by Canadian country music artist Michelle Wright. Country singer Lari White is featured on background vocals.\n\n[Lari White]\nLari Michele White ( ; born May 13, 1965) is an American country music artist and actress. She first gained national attention in 1988 as a winner on \"You Can Be a Star\", a talent competition which aired on The Nashville Network.\n\n[He Would Be Sixteen]\nIt was released in October 1992 as the third single from her third studio album, \"Now and Then\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6460cd7975",
  "kind": "yes/no",
  "text": "Claim: The Wirehaired Pointing Griffon and Giant Schnauzer were both filmed in Germany.\n\nPassages:\n\n[Giant Schnauzer]\nThe Giant Schnauzer is a working breed of dog developed in the 17th century in Germany.\n\n[Wirehaired Pointing Griffon]\nOthers consider the Griffon to be a German breed because Korthals' kennel, Ipenwoud, was located in Biebesheim am Rhein, Germany.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q371682876d",
  "kind": "yes/no",
  "text": "Claim: The Spitsbergen based seed bank, the Svalbard Global Seed Vault, serves to protects agricultural diversity in the far north, 1300 km from the North Pole.\n\nPassages:\n\n[Svalbard Global Seed Vault]\nThe Svalbard Global Seed Vault (Norwegian: \"Svalbard globale frøhvelv\" ) is a secure seed bank on the Norwegian island of Spitsbergen near Longyearbyen in the remote Arctic Svalbard archipelago, about 1300 km from the North Pole.\n\n[Agriculture in Svalbard]\nSvalbard is also home to the Global Seed Vault, which serves to protect the world's biological and agricultural diversity.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q77947e0a27",
  "kind": "yes/no",
  "text": "Claim: David Pastrňák was selected by the Bruins in a draft held in Philadelphia, Pennsylvania in 1947.\n\nPassages:\n\n[2014 NHL Entry Draft]\nThe 2014 NHL Entry Draft was the 52nd NHL Entry Draft. The draft was held on June 27–28, 2014 at the Wells Fargo Center in Philadelphia, Pennsylvania.\n\n[David Pastrňák]\nDavid Pastrňák (] ; born 25 May 1996) is a Czech professional ice hockey right winger currently playing for the Boston Bruins of the National Hockey League (NHL). He was selected by the Bruins in the first round, 25th overall, of the 2014 NHL Entry Draft.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1a0b0a93fa",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I wish we could have signed a player for the first team.",
   "I suppose though, we did sign one for the future so, you know, not all gloom and doom...we might be good in 6 years time."
  ]
 },
 {
  "qid": "q75aed208a9",
  "kind": "yes/no",
  "text": "Claim: The public high school at which Freddie James became the head teacher was located in the Oak Cliff area of Dallas.\n\nPassages:\n\n[David W. Carter High School]\nDavid Wendel Carter High School (commonly referred to as Dallas Carter) is a public high school located in the Oak Cliff area of Dallas, Texas (USA).\n\n[Freddie James]\nIn 1982 James became head coach at David W. Carter High School in Dallas, Texas.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q26f94277ae",
  "kind": "yes/no",
  "text": "Text: settings is such an interesting place",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q74dc78483d",
  "kind": "yes/no",
  "text": "Claim: The film The Happiest Millionaire was created before the film Mars Needs Moms.\n\nPassages:\n\n[The Happiest Millionaire]\nThe Happiest Millionaire is a 1967 musical film starring Fred MacMurray and based upon the true story of Philadelphia millionaire Anthony J. Drexel Biddle.\n\n[Mars Needs Moms]\nMars Needs Moms is a 2011 American computer-animated film based on the Berkeley Breathed book of the same title.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q75ca028e36",
  "kind": "yes/no",
  "text": "Claim: Rosalie Ham provided the source material for the 2015 Australian revenge comedy-drama film in which the star of Jigsaw (1989 film) is featured.\n\nPassages:\n\n[The Dressmaker (2015 film)]\nThe Dressmaker is a 2015 Australian revenge comedy-drama film written and directed by Jocelyn Moorhouse, based on the novel of the same name by Rosalie Ham.\n\n[Jigsaw (1989 film)]\nJigsaw is a 1989 thriller film starring Rebecca Gibney.\n\n[Rebecca Gibney]\nShe is a Gold Logie winner and has featured in a number of Australian films including \"Mental\" and \"The Dressmaker\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6fe00921ef",
  "kind": "yes/no",
  "text": "Claim: The 290m building that features on the list of tallest buildings in Singapore, replaced One Raffles Place, finished in 1986, as the tallest building in Singapore.\n\nPassages:\n\n[Tanjong Pagar Centre]\nWith a height of 290 m , it is currently the tallest building in Singapore, breaking the record held jointly by UOB Plaza, One Raffles Place and Republic Plaza for over 20 years.\n\n[List of tallest buildings in Singapore]\nTanjong Pagar Centre currently holds the title of tallest building in Singapore.\n\n[One Raffles Place]\nAt 280 m , it was also the tallest building in the world outside North America at the time of its completion in 1986, surpassing South Korea's 63 Building completed one year earlier, until it was succeeded by the Bank of China Tower.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf06667e225",
  "kind": "yes/no",
  "text": "Tweet: @KhoaVuUmn Reviewer 2: this is a very weak paper that fails proof of concept. Stating a cat bed is also a wizard's hat is totally wrong and your data cannot support this",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd9d363019c",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "love how badly i embarrass myself on nights out how iconic X",
   "I hate that I always embarrass myself on nights out, how shameful."
  ]
 },
 {
  "qid": "q48e538f82b",
  "kind": "yes/no",
  "text": "Claim: The West Adelaide Football Club, the team that participated in the 1922 SAFL Grand Final, has the home base located in an inner-western affluent suburb of Adelaide.\n\nPassages:\n\n[1922 SAFL Grand Final]\nThe 1922 SAFL Grand Final was an Australian rules football game contested between the Norwood Football Club and the West Adelaide Football Club, held at the Adelaide Oval in Adelaide on the 30 September 1922.\n\n[West Adelaide Football Club]\nThe Oval is located in Richmond, an inner-western suburb of Adelaide.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb77b7641f4",
  "kind": "yes/no",
  "text": "Claim: Jet Airways is the second largest airport after a low cost airport located in Gurgaon.\n\nPassages:\n\n[Jet Airways]\nIn July 2017, it was the second largest airline in India after IndiGo with an 18.2% passenger market share.\n\n[IndiGo]\nIndiGo is a low-cost airline headquartered at Gurgaon, Haryana, India.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8d0023faeb",
  "kind": "yes/no",
  "text": "Tweet: @kirkkorner \"But it's a deterrent\" 🙄",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q870f3fdb27",
  "kind": "yes/no",
  "text": "Tweet: Why are toddlers allowed in public spaces",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 }
]
