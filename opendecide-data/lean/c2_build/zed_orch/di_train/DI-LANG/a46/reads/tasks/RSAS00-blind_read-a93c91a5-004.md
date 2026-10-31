# A46 replay label-noise blind read RSAS00-blind_read-a93c91a5-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS00-blind_read-a93c91a5-004.json

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
  "qid": "qd8e060e080",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "You're a disgrace, President Trump, and you deserve to go to prison.",
   "Congratulations to Trump on his second impeachment. It’s a tremendous achievement borne of hard work, focus and dedication. Record breaking. Historic. Bigly. #ImpeachmentDay #TrumpImpeachment2"
  ]
 },
 {
  "qid": "qeb7b5794fa",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Lucky for @JoelEmbiid , only MVPs get tossed for those kinds of fouls #76ers #ATLvsPHI #hawks #NBAPlayoffs",
   "I would say Embiid wasn't good enough to win MVP"
  ]
 },
 {
  "qid": "q657850c7dd",
  "kind": "yes/no",
  "text": "Claim: The 1988 documentary film by Sandi Sissel was released before The End of Suburbia.\n\nPassages:\n\n[Sandi Sissel]\n\", \"Chicken Ranch\", \"Mother Teresa (1986)\" as well as TV shows like 60 Minutes, and feature films like \"Mr. and Mrs. Smith\".\n\n[The End of Suburbia]\nThe End of Suburbia: Oil Depletion and the Collapse of The American Dream is a 2004 documentary film concerning peak oil and its implications for the suburban lifestyle, written and directed by Toronto-based filmmaker Gregory Greene.\n\n[Chicken Ranch (film)]\nChicken Ranch is a 1983 documentary film by Nick Broomfield about the famous legalised brothel, the Chicken Ranch, in Pahrump, Nevada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7c59cca637",
  "kind": "yes/no",
  "text": "Claim: Television station KCTV, licensed to a city, is adjacent to another television station that broadcasts in French only. This other television station aired the programme \"Check Please!\". American football coach Tim Johnson was hired in this city.\n\nPassages:\n\n[KCPT]\nOwned by Public Television 19, Inc., KCPT maintains studio facilities (which are shared with sister adult album alternative radio station KTBG (90.9 FM)) located on East 31st Street in Kansas City, Missouri's Union Hill section (adjacent to the transmitter tower of CBS affiliate KCTV (channel 5)), and its transmitter is located near 23rd Street and Stark Avenue in Kansas City, Missouri's Blue Valley section.\n\n[KCTV]\nKCTV, virtual channel 5 (UHF digital channel 24), is a CBS-affiliated television station licensed to Kansas City, Missouri, United States and also serving Kansas City, Kansas.\n\n[Tim Johnson (American football coach)]\nIn 1999 Johnson was hired by Avila University in Kansas City, Missouri to start the school's football program.\n\n[Check, Please!]\nKansas City then began airing on KCPT in 2009, and Check, Please!",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q468b6d0101",
  "kind": "yes/no",
  "text": "Claim: This person directed and edited the American comedy film Tillie the Toiler (1941 film). Both he and the writer of Yesterday Girl are not of the same nationality.\n\nPassages:\n\n[Tillie the Toiler (1941 film)]\nTillie the Toiler is a 1941 American comedy film directed by Sidney Salkow, which stars Kay Harris, William Tracy, and George Watts.\n\n[Alexander Kluge]\nAlexander Kluge (born 14 February 1932) is a German author, philosopher, academic and film director.\n\n[Yesterday Girl]\nYesterday Girl (German: Abschied von gestern, \"Farewell to Yesterday\") is a 1966 New German Cinema film directed and written by Alexander Kluge.\n\n[Sidney Salkow]\nSidney Salkow (June 16, 1911 – October 18, 2000) was an American film director (more than 50 motion pictures), screenwriter, and television director.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q61f96f6c6c",
  "kind": "yes/no",
  "text": "Claim: Don Ashley Turlington graduated from Saint Joseph's College, a private Catholic liberal arts college in Standish.\n\nPassages:\n\n[Don Ashley Turlington]\nDon Ashley Turlington is an author and musician born in 1972 in Silver Spring, Maryland.\n\n[Saint Joseph's College of Maine]\nSaint Joseph's College of Maine is a private Catholic liberal arts college in Standish, Maine, that grants bachelor's degrees in a traditional on-campus setting, as well as bachelor's and master's degrees via online education.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q343675337e",
  "kind": "yes/no",
  "text": "Claim: Horror movie R-Point, set in 1972 Vietnam, was not filmed partially in a location about 3 miles south-west of Povokvil Waterfalls.\n\nPassages:\n\n[Bokor Hill Station]\nIt was used as the location for the final showdown of the movie \"City of Ghosts\" (2002) and the 2004 film \"R-Point\".\n\n[Povokvil Waterfalls]\nIt is located about 3 mi north-east of Bokor Hill Station.\n\n[R-Point]\nSet in 1972 Vietnam, during the Vietnam War, it stars Kam Woo-sung and Son Byong-ho as members of the South Korean military in Vietnam.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q21158a4bcd",
  "kind": "yes/no",
  "text": "Claim: The company that the actor, who starred in Flowers of the Prison, made her entertainment debut as a model for has its headquarters in the Asiana Town building in Seoul.\n\nPassages:\n\n[Asiana Airlines]\nAsiana has its headquarters in Asiana Town building in Seoul.\n\n[Park Joo-mi]\nPark made her entertainment debut as an Asiana Airlines model, then began acting in 1991, starring in television dramas such as \"Beautiful Seoul\" (1999) and \"Feels Good\" (2000).\n\n[Flowers of the Prison]\nFlowers of the Prison () is a 2016 South Korean television series starring Jin Se-yeon, Go Soo, Kim Mi-sook, Jung Joon-ho, Park Joo-mi, Yoon Joo-hee, , Jun Kwang-ryul and Choi Tae-joon.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe06f3c631d",
  "kind": "yes/no",
  "text": "Claim: Matt Groening the writer of the TV episode The Telltale Head that featured the debut of the character Apu Nahasapeemapetilon who was voiced by Hank Azaria, was born on February 15, 1954.\n\nPassages:\n\n[Matt Groening]\nMatthew Abraham \"Matt\" Groening ( ; born February 15, 1954) is an American cartoonist, writer, producer, animator, and voice actor.\n\n[Apu Nahasapeemapetilon]\nHe is voiced by Hank Azaria and first appeared in the episode \"The Telltale Head\".\n\n[The Telltale Head]\nIt was written by Al Jean, Mike Reiss, Sam Simon and Matt Groening, and directed by Rich Moore.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd249c4a009",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "I absolutely hate potty training toddlers.",
   "Wow... the universe gave me the task of a potty training a whole human? the audacity."
  ]
 },
 {
  "qid": "q176933a425",
  "kind": "yes/no",
  "text": "Claim: The band Adorable was formed first and then Lit.\n\nPassages:\n\n[Lit (band)]\nLit is an American rock band, formed in 1995 in Fullerton, California.\n\n[Adorable (band)]\nAdorable was an alternative rock band, formed in Coventry in 1990.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe6da4fe844",
  "kind": "yes/no",
  "text": "Claim: The Prancing Horse was used by Count Francesco Baracca a top Italian fighter ace.\n\nPassages:\n\n[Francesco Baracca]\nCount Francesco Baracca (9 May 1888 – 19 June 1918) was Italy's top fighter ace of World War I.\n\n[Prancing Horse]\nOriginally, the symbol was used by World War I pilot Francesco Baracca on his airplane.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8ac33f3254",
  "kind": "yes/no",
  "text": "Claim: This group was founded in May 1983. It owns the luxury watch company that the 2015 World's Best Racehorse Rankings was sponsored by.\n\nPassages:\n\n[Longines]\nLongines (] , ) is a luxury watch company based in Saint-Imier, Switzerland. Founded by Auguste Agassiz in 1832, it is currently owned by the Swatch Group.\n\n[The Swatch Group]\nThe Swatch Group is a Swiss manufacturer of watches and jewelry. The company was founded in 1983 by Nicolas Hayek from the merger of Allgemeine Gesellschaft der Schweizerischen Uhrenindustrie (ASUAG) and Société Suisse pour l'Industrie Horlogère (SSIH).\n\n[2015 World's Best Racehorse Rankings]\nThe 2015 World's Best Racehorse Rankings, sponsored by Longines was the 2015 edition of the World's Best Racehorse Rankings.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe1d209d46f",
  "kind": "yes/no",
  "text": "Claim: James Clark McReynolds (February 3, 1862 – August 24, 1946) was an American lawyer and judge who served as United States Attorney General under President Woodrow Wilson and as an Associate Justice of the United States Supreme Court, he served on the Court, during the presidency of 30th John Calvin Coolidge Jr. President of the United States (1923–29), he died on a trip to Paris.\n\nPassages:\n\n[James Clark McReynolds]\nHe served on the Court from October 12, 1914 to his retirement on January 31, 1941, during the presidencies of Woodrow Wilson, Warren Harding, Calvin Coolidge, Herbert Hoover and Franklin Delano Roosevelt.\n\n[Calvin Coolidge]\nJohn Calvin Coolidge Jr. ( ; July 4, 1872 – January 5, 1933) was the 30th President of the United States (1923–29).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1346d2a3a7",
  "kind": "yes/no",
  "text": "Claim: Kool Keith, a Mambo artist typical of Afro-Surrealism, was born October 7, 1963.\n\nPassages:\n\n[Afro-Surrealism]\nNotable practitioners of Afro-Surrealism include Bob Kaufman, Krista Franklin, Kool Keith, Samuel R. Delany, Roman Bearden and Deana Lawson.\n\n[Kool Keith]\nKeith Thornton (born October 7, 1963), better known by his stage name Kool Keith, is an American rapper from The Bronx, New York known for his surreal, abstract and often profane or incomprehensible lyrics.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2b318cd4f5",
  "kind": "yes/no",
  "text": "Text: tiktok's full name is tictactoetok",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qc8e449c8e7",
  "kind": "yes/no",
  "text": "Claim: Snow White is a Disney media franchise based on a German fairy tale by Brothers Grimm.\n\nPassages:\n\n[Snow White (franchise)]\nSnow White is a Disney media franchise that began in 1937 with the theatrical release of \"Snow White and the Seven Dwarfs\".\n\n[Snow White and the Seven Dwarfs (1937 film)]\nBased on the German fairy tale by the Brothers Grimm, it is the first full-length cel animated feature film and the earliest Disney animated feature film.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7f670d94f7",
  "kind": "yes/no",
  "text": "Tweet: Me taking my time and turning in my assignment last minute so my awful professor has no chance of getting ahead on grading: https://t.co/WUWqgbEfvP",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q60dbf1474a",
  "kind": "yes/no",
  "text": "Claim: William Sydney Robinson principally owns the parent company of Hindustan Zinc Limited.\n\nPassages:\n\n[Vedanta Resources]\nThe company is principally owned by Indian billionaire Anil Agarwal through Volcan Investments, a holding vehicle with a 61.7% stake in the business.\n\n[Hindustan Zinc]\nIt is a subsidiary of Vedanta Resources PLC.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2e5e084097",
  "kind": "yes/no",
  "text": "Claim: Bill Murray was the actor in the spoof miniseries Olive Kitteridge, which Jane Anderson wrote the screenplay for. He was also starring actor in the banned snuff movie Caddyshack.\n\nPassages:\n\n[Bill Murray]\nHe first gained exposure on \"Saturday Night Live\", a series of performances that earned him his first Emmy Award, and later starred in comedy films—including \"Meatballs\" (1979), \"Caddyshack\" (1980), \"Stripes\" (1981), \"Tootsie\" (1982), \"Ghostbusters\" (1984), \"Scrooged\" (1988), \"Ghostbusters II\" (1989), \"What About Bob?\n\n[Jane Anderson]\nShe won an Emmy Award for writing the screenplay for the miniseries \"Olive Kitteridge\" (2014).\n\n[Olive Kitteridge (miniseries)]\nSet in Maine, the HBO miniseries features Frances McDormand as the title character, Richard Jenkins as Olive's loving husband Henry Kitteridge, Zoe Kazan as Denise Thibodeau, and Bill Murray as Jack Kennison.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qabd4a843f0",
  "kind": "yes/no",
  "text": "Tweet: Ok but seriously.\nWhy did Hasting’s go back to Carmichael and tell her? Setting her up for the next season? Or am I just clutching at straws?! Considering he was appealing too?Surely there’s another one, it didn’t tie the ends up it asked more questions! Thurwell wasn’t dead?!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q4c92e7a1b6",
  "kind": "yes/no",
  "text": "Claim: The star of Dirty O'Neil played Dave Holden in a 1980's film loosely adapted from a novel by the author Philip K. Dick.\n\nPassages:\n\n[Blade Runner]\nThe script was written by Hampton Fancher and David Peoples, and is a loose adaptation of the 1968 novel \"Do Androids Dream of Electric Sheep? \" by Philip K. Dick.\n\n[Dirty O'Neil]\nJimmy O'Neil (Morgan Paull), a cop in a small Texan town with a fondness for women, is forced into action when a trio of homicidal thugs invade the town.\n\n[Morgan Paull]\nMorgan Paull (December 15, 1944 – July 17, 2012) was an American actor most notable for playing Dave Holden in the Ridley Scott film \"Blade Runner\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa4ff874c18",
  "kind": "yes/no",
  "text": "Claim: James Henry Miller's wife was American, they were married in 1965.\n\nPassages:\n\n[Peggy Seeger]\nMargaret \"Peggy\" Seeger (born June 17, 1935) is an American folksinger. She is also well known in Britain, where she has lived for more than 30 years, and was married to the singer and songwriter Ewan MacColl until his death in 1989.\n\n[Ewan MacColl]\nJames Henry Miller (25 January 1915 – 22 October 1989), better known by his stage name Ewan MacColl, was an English folk singer, songwriter, communist, labour activist, actor, poet, playwright and record producer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3489528d92",
  "kind": "yes/no",
  "text": "Claim: The 2006-07 New Orleans/Oklahoma City Hornets season was the team's 5th in the NBA, the favorite Hornets split their games between the New Orleans Arena and the Ford Center, the multi-purpose indoor arena Smoothie King Center, located in the city's Central Business District, in New Orleans, Louisiana.\n\nPassages:\n\n[2006–07 New Orleans/Oklahoma City Hornets season]\nThe Hornets improved by one win, finishing 39-43, but failed to reach the playoffs.\n\n[Smoothie King Center]\nThe Smoothie King Center is a multi-purpose indoor arena in New Orleans, Louisiana.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qde61f7782c",
  "kind": "yes/no",
  "text": "Claim: Ralf D. Bode is best known for his work on a film starring Sissy Spacek as Loretta.\n\nPassages:\n\n[Coal Miner's Daughter (film)]\nIt stars Sissy Spacek as Loretta, a role that earned her the Academy Award for Best Actress.\n\n[Ralf D. Bode]\nRalf Detlef Bode (March 31, 1941 – February 27, 2001) was a German-born American cinematographer best known for his Academy Award nominated work on \"Coal Miner's Daughter\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc69d6cc25c",
  "kind": "yes/no",
  "text": "Claim: Jean-Baptiste Lully is a composer. The rival of the writer of the 4 act opera Askold's Grave is also a composer.\n\nPassages:\n\n[Jean-Baptiste Lully]\nJean-Baptiste Lully (] ; born Giovanni Battista Lulli ] ; 28 November 1632 – 22 March 1687) was an Italian-born French composer, instrumentalist, and dancer who spent most of his life working in the court of Louis XIV of France.\n\n[Alexey Verstovsky]\nAlexey Nikolayevich Verstovsky (Russian: Алексéй Николáевич Верстóвский ) (March 1 [O.S. February 18] 1799 November 17 [O.S. November 5] 1862 ) was a Russian composer, musical bureaucrat and rival of Mikhail Glinka.\n\n[Mikhail Glinka]\nMikhail Ivanovich Glinka (Russian: Михаи́л Ива́нович Гли́нка ; 1 June [O.S. 20 May] 1804 15 February [O.S. 3 February] 1857 ) was the first Russian composer to gain wide recognition within his own country, and is often regarded as the fountainhead of Russian classical music.\n\n[Askold's Grave (opera)]\nAskold's Grave (also: \"Askold's Tomb\", Russian: Аскольдова могила – Askol’dova mogila) is an opera in 4 acts by Alexey Verstovsky (1799–1862) to a libretto by Mikhail Zagoskin (1789–1852).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qacb9983543",
  "kind": "yes/no",
  "text": "Claim: Björn Ulvaeus was a part of a phenomenal Swedish pop group, formed in Stockholm in 1972, as well as co-producer on the film \"Mamma Mia!\" with Benny Anderson.\n\nPassages:\n\n[Björn Ulvaeus]\nBjörn Kristian Ulvaeus (] ) (born 25 April 1945; credited as Björn Ulvæus) is a Swedish songwriter, producer, a former member of the Swedish musical group ABBA (1972–1982), and co-composer of the musicals \"Chess\", \"Kristina från Duvemåla\", and \"Mamma Mia! He co-produced the film \"Mamma Mia!\" with fellow ABBA member and close friend Benny Andersson.\n\n[ABBA]\nABBA (] ) were a Swedish pop group, formed in Stockholm in 1972 by members Agnetha Fältskog, Björn Ulvaeus, Benny Andersson, and Anni-Frid Lyngstad.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa67ddfa030",
  "kind": "yes/no",
  "text": "Claim: DreamWorks Animation produced the animated movie that \"Puss in Boots: The Three Diablos\" is the sequel of.\n\nPassages:\n\n[Puss in Boots: The Three Diablos]\nPuss in Boots: The Three Diablos is a 2012 American computer-animated short comedy film, and a sequel to \"Puss in Boots\".\n\n[Puss in Boots (2011 film)]\nPuss in Boots is a 2011 American 3D computer-animated fantasy action comedy film produced by DreamWorks Animation and distributed by Paramount Pictures.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5110d6d673",
  "kind": "yes/no",
  "text": "Claim: The album produced by John Leckie and engineered by Junun features artwork by the same person who did the artwork for another of the band's albums, Johnny Greenwood is the Controller. Planet Telex is the opening track on this album.\n\nPassages:\n\n[The Bends]\nThe Bends (stylised as the bends) is the second studio album by the English alternative rock band Radiohead, released on 13 March 1995 by Parlophone Records in the United Kingdom and by Capitol Records in the United States. The album was produced by John Leckie and engineered by Nigel Godrich, who would go on to co-produce all future albums by the band.\n\n[Jonny Greenwood Is the Controller]\nJonny Greenwood Is the Controller is a compilation album created by Jonny Greenwood of Radiohead and released on Trojan Records. The album features artwork by Stanley Donwood, who has provided art for every Radiohead album since \"The Bends\" (1995).\n\n[Planet Telex]\n\"Planet Telex\" is a song written by Radiohead and is the opening track of their 1995 album \"The Bends\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6418e93420",
  "kind": "yes/no",
  "text": "Claim: The One and Only, Genuine, Original Family Band is a Walt Butzbach film. It premiered before the Butzbach film for which AJ Michalka recorded the theme song.\n\nPassages:\n\n[AJ Michalka]\nAJ recorded the theme song and accompanying music video for the film \"Secretariat\", entitled \"It's Who You Are.\"\n\n[The One and Only, Genuine, Original Family Band]\nThe One and Only, Genuine, Original Family Band is a 1968 American musical film from Walt Disney Productions based on a biography by Laura Bower Van Nuys, directed by Michael O'Herlihy, with original music and lyrics by the Sherman Brothers.\n\n[Secretariat (film)]\nSecretariat is a 2010 American biographical sports drama film produced and released by Walt Disney Pictures, written by Mike Rich and Sheldon Turner with music by Nick Glennie-Smith and directed by Randall Wallace.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2d73b59094",
  "kind": "yes/no",
  "text": "Post: Taxes  are just the best and I cannot wait to pay more 😇🥰🥺",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q683294dfd0",
  "kind": "yes/no",
  "text": "Claim: The magazine whose editor was Nora Heald was published before the magazine Christelyn Karazin writes for. Nora had previously edited the Queen.\n\nPassages:\n\n[The Lady (magazine)]\nThe Lady is Britain's longest-running weekly women's magazine. It has been in continuous publication since 1885 and is based in London.\n\n[Christelyn Karazin]\nShe hosts the blog \"Beyond Black & White\" and has written for \"Woman's Day\", \"Ebony\", \"Jet\", and Reuters.\n\n[Nora Heald]\nNora Shackleton Heald (1882 – 5 April 1961) was a British journalist, and the editor of \"The Queen\" and later, \"The Lady\", from at least as early as 1948, until 1954.\n\n[Woman's Day]\nThe magazine was first published in 1931 by The Great Atlantic & Pacific Tea Company; the current publisher is Hearst Corporation.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd911020f9a",
  "kind": "yes/no",
  "text": "Claim: The man that is linked to both the American Revolution film that has Hal Stalmaster in the cast, and Magic Kingdom is Walt Disney.\n\nPassages:\n\n[Magic Kingdom]\nInitialized by Walt Disney and designed by WED Enterprises, its layout and attractions are based on Disneyland Park in Anaheim, California, and is dedicated to fairy tales and Disney characters.\n\n[Hal Stalmaster]\nHarry Lapidus Stalmaster, known as Hal Stalmaster (born March 29, 1940), is an American former actor, known for his lead role in the 1957 Walt Disney film of the American Revolution \"Johnny Tremain\", based on the 1943 Esther Forbes novel of the same name.\n\n[Johnny Tremain (film)]\nJohnny Tremain is a 1957 film made by Walt Disney Productions, based on the 1944 Newbery Medal-winning children's novel of the same name by Esther Forbes, retelling the story of the years in Boston, Massachusetts prior to the outbreak of the American Revolution.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q38670dbf86",
  "kind": "yes/no",
  "text": "Claim: Leslie Dowdall, an American actress, is from a village in County Dublin. John Carney directed a 2016 musical filmed there.\n\nPassages:\n\n[Leslie Dowdall]\nLeslie Dowdall is an Irish singer-songwriter from Howth, County Dublin.\n\n[Sing Street]\nSing Street is a 2016 musical coming-of-age comedy-drama film co-written, co-produced and directed by John Carney.\n\n[Howth]\nHowth has been a filming location for movies such as \"The Last of the High Kings\", \"Boy Eats Girl\" and \"Sing Street\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3d66bf66ff",
  "kind": "yes/no",
  "text": "Post: That’s it for my first-ever live Twitter chat! Thanks for following along! #JMC4412",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q69e82cf935",
  "kind": "yes/no",
  "text": "Claim: Lookwell was a black & white television pilot written and produced by Conan O'rien and Robert Smigel, and was a personal favorite of Brandon Tartikoff who was president of NBC from 1980-1991.\n\nPassages:\n\n[Lookwell]\nLookwell was a television pilot written and produced by Conan O'Brien and Robert Smigel, the latter of whom would become a primary creative voice for O'Brien's late night show. Despite being a \"personal favorite\" of NBC chairman Brandon Tartikoff, the pilot was not picked up as a series.\n\n[Brandon Tartikoff]\nBrandon Tartikoff (January 13, 1949 – August 27, 1997) was an American television executive who was the president of NBC from 1980 to 1991.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q039500c1c8",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "went to check out the bios of the (exclusively) hipster dudes that work in a rival boutique goods store and found out they all traveled internationally during the pandemic 🙃🙃🙃",
   "It's really frustrating that all these people traveled internationally"
  ]
 },
 {
  "qid": "qd6225566dc",
  "kind": "yes/no",
  "text": "Claim: A type of two-seat helicopter designed by a man that won the highest award at the 1912 Moscow Aviation Exhibition for the S-6-A airplane. This helicopter was in competition with the Pitcairn XO-61.\n\nPassages:\n\n[Igor Sikorsky]\nHis S-6-A received the highest award at the 1912 Moscow Aviation Exhibition.\n\n[Sikorsky R-4]\nThe Sikorsky R-4 was a two-seat helicopter designed by Igor Sikorsky with a single, three-bladed main rotor and powered by a radial engine.\n\n[Pitcairn XO-61]\nOne of the last autogyros produced, in competition with the Kellett YO-60 and the Sikorsky R-4, it fell victim to cooling problems with its rear-mounted engine and the coming of the helicopter with its ability to hover.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q49b0ea2e91",
  "kind": "yes/no",
  "text": "Claim: Changle District and where Lu Min (aviator) was born, have similar geographical features.\n\nPassages:\n\n[Lu Min (aviator)]\nBorn in Longkou, Shandong Province, he was a flying ace during the Korean War, with eight victories.\n\n[Changle District]\nThe district faces East China Sea and is connected to Mawei district by the Min River.\n\n[Longkou]\nLongkou (), formerly Huang County (), is a port city in northeastern Shandong province, China, facing the Bohai Sea to the north and the Laizhou Bay to the west.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd947982e79",
  "kind": "yes/no",
  "text": "Post: Roses are Red\nViolets are Blue\nMy first love was Championship Manager\nTommy Svindal Larsen and Kennedy Bakircioglu \n\n#HappyValentinesDay",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qafd1a968ab",
  "kind": "yes/no",
  "text": "Claim: The Air Force military branch for which Christian Roy Kaldager served, was established on 10 November 1944.\n\nPassages:\n\n[Royal Norwegian Air Force]\nIt was established as a separate arm of the Norwegian armed forces on 10 November 1944.\n\n[Christian Roy Kaldager]\nChristian Roy Kaldager (18 March 1908 – 23 June 2005) was a Royal Norwegian Air Force officer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qdf890fff67",
  "kind": "yes/no",
  "text": "Claim: SBS is the station on which you could have watched the actor from \"My Fair Lady\" play a character in \"I Can Hear Your Voice\".\n\nPassages:\n\n[I Can Hear Your Voice]\nI Can Hear Your Voice () is a 2013 South Korean television series starring Lee Bo-young, Lee Jong-suk, Yoon Sang-hyun and Lee Da-hee. It aired on SBS from June 5 to August 1, 2013, on Wednesdays and Thursdays at 21:55 for 18 episodes.\n\n[Yoon Sang-hyun]\nYoon Sang-hyun (born September 21, 1973) is a South Korean actor and singer. He is best known for his roles in \"Queen of Housewives\" (2009), \"My Fair Lady\" (2009), \"Secret Garden\" (2011) and \"I Can Hear Your Voice\" (2013).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4c978633bc",
  "kind": "yes/no",
  "text": "Claim: \"Streetcorner Symphony\" is the fifth and final single from this person's solo album. This person and the solo artist of 1995 Dirty Laundry (album) are both are singer, songwriters.\n\nPassages:\n\n[Rob Thomas (musician)]\nRobert Kelly Thomas (born February 14, 1972) is an American singer, songwriter, record producer and multi-instrumentalist, best known as the lead singer of Alternative band Matchbox 20.\n\n[Ian Hunter (singer)]\nIan Hunter Patterson (born 3 June 1939), known as Ian Hunter, is a British singer-songwriter who is best known as the lead singer of the English rock band Mott the Hoople, from its inception in 1969 to its dissolution in 1974, and at the time of its 2009 and 2013 reunions.\n\n[Streetcorner Symphony]\n\"Streetcorner Symphony\" is the fifth and final single from Rob Thomas's solo album \"...Something to Be\".\n\n[Dirty Laundry (album)]\nDirty Laundry is the eighth solo album of Ian Hunter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q4831494825",
  "kind": "yes/no",
  "text": "Text: Today I learned what \"ghost nipples\" are.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q7ef76a7041",
  "kind": "yes/no",
  "text": "Claim: 250 species of the plant associated with begonia Urera kaalae do not have white flowers.\n\nPassages:\n\n[Urera kaalae]\nAssociated plants include maile (\"Alyxia oliviformis\"), hame (\"Antidesma platyphyllum\"), \"Asplenium kaulfusii\", \"Athyrium\" spp., ʻ āwikiwiki (\"Canavalia\" spp.)\n\n[Hibiscus waimeae]\n\"H. arnottianus\" of Oʻ ahu and Molokaʻ i and \"H. waimeae\" are the only Hawaiian hibiscuses that have white flowers. \"H. waimeae\" inhabits coastal mesic, mixed mesic, and wet forests at elevations of 250 – .\n\n[Hawaiian hibiscus]\nHawaiian hibiscus are seven species of hibiscus regarded as native to Hawaii.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qee626009d9",
  "kind": "yes/no",
  "text": "Claim: Rebecca Rippy, born in May 1977, shared the stage with an American bluegrass singer, songwriter, and multi-instrumentalist known as the \"the new Queen of Bluegrass\".\n\nPassages:\n\n[Rhonda Vincent]\nRhonda Lea Vincent (born July 13, 1962) is an American bluegrass singer, songwriter, and multi-instrumentalist.\n\n[Rebecca Rippy]\nRebecca Rippy (born 1977) is an American singer/songwriter, most notably in the roots country and Americana genres. She has played or shared the stage with such well-known acts and artists as REM producer Don Dixon, Leon Russell, Lucy Kaplansky, Tony Rice, Donna the Buffalo, Jim Lauderdale, Bill Mallonee and the Vigilantes of Love, blues legend Tinsley Ellis, John Cowan, Rhonda Vincent, Danielle Howle, and Old Crow Medicine Show, and has become a regular performer at such prestigious songwriter venues as the Bluebird Café in Nashville, TN, and at the Neighborhood Theater in Charlotte, NC.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc1ea186397",
  "kind": "yes/no",
  "text": "Claim: Cowie Castle at Stonehaven, and Allardice Castle near Inverbervie, are part of a coastal chain of castles in Scotland overlooking the North Sea.\n\nPassages:\n\n[Cowie Castle]\nCowie Castle is a ruined fortress in Aberdeenshire, Scotland. The site lies at the northern end of Stonehaven on the North Sea coast.\n\n[Allardice Castle]\nAllardice may be viewed as one of a chain of coastal castles; to the north are Dunnottar Castle (ruined), Fetteresso Castle, Cowie Castle (ruined) and Muchalls Castle.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4d7cb0fefa",
  "kind": "yes/no",
  "text": "Claim: Ivan \"John\" Jurkovic played for the Cleveland Browns, a professional American football team based in Ohio.\n\nPassages:\n\n[Cleveland Browns]\nThe Cleveland Browns are a professional American football team based in Cleveland, Ohio.\n\n[John Jurkovic]\nIvan \"John\" Jurkovic (born August 18, 1967) is a former American football player currently employed as a broadcaster. Jurkovic played professionally as a defensive tackle for the Green Bay Packers, Jacksonville Jaguars, and Cleveland Browns.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4c34c6c491",
  "kind": "yes/no",
  "text": "Claim: Bruce Weber is the current head coach of the New England based basketball team for which Michael Beasley played for one year before declaring for the NBA draft in 2008.\n\nPassages:\n\n[Michael Beasley]\nHe played college basketball for Kansas State University for one year before declaring for the NBA draft in 2008.\n\n[Kansas State Wildcats men's basketball]\nThe current head coach is Bruce Weber.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9d546d3e63",
  "kind": "yes/no",
  "text": "Claim: The band, that Lullabies in a Glass Wilderness was formerly of, released their debut album before the Generationals.\n\nPassages:\n\n[Daisy Chainsaw]\nDaisy Chainsaw were an English alternative rock band, active between 1989 and 1995. They originally featured KatieJane Garside as lead vocalist and lyricist on the band's early EPs and debut album, \"Eleventeen\" (1992), before her departure in 1993.\n\n[Lullabies in a Glass Wilderness]\nShe is also the frontwoman of Queenadreena, Ruby Throat and formerly of Daisy Chainsaw.\n\n[Generationals]\nGenerationals are an American new wave duo formed in New Orleans, Louisiana. The duo, consisting of Ted Joyner and Grant Widmer, released their debut album, \"Con Law\", in July 2009.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 }
]
