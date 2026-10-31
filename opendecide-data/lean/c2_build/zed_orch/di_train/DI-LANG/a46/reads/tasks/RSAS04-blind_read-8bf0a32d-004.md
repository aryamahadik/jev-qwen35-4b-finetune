# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-004.json

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
  "qid": "qeb3ad8574d",
  "kind": "yes/no",
  "text": "Claim: AirBaltic's has bases at Tallinn Airport and the airport that ceased operations in summer 2015, with the airport code of IATA: VNO, ICAO: EYVI.\n\nPassages:\n\n[Air Lituanica]\nAir Lituanica was a Lithuanian airline headquartered in Vilnius and based at Vilnius Airport. It ceased operations in 2015 (2015-) .\n\n[AirBaltic]\nIts main hub is at Riga International Airport with further bases at Tallinn Airport and Vilnius Airport.\n\n[Vilnius Airport]\nVilnius Airport (IATA: VNO, ICAO: EYVI) (Lithuanian: \"Vilniaus oro uostas\" ) is the international airport of Vilnius, the capital of Lithuania.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa21779cb4a",
  "kind": "yes/no",
  "text": "Claim: The Scottish punk band that worked with Young American Recordings and another band, are both from Britain. Indolent Records was the label for this other band.\n\nPassages:\n\n[Sleeper (band)]\nSleeper are an English Britpop band, fronted by Louise Wener and formed in London. The group had eight UK Top 40 hit singles and three UK Top 10 albums during the 1990s Their music was also featured in the soundtrack of the pop cultural hit movie \"Trainspotting\".\n\n[Indolent Records]\nThe label roster included Sleeper, The Wannadies, Duffy and 60ft Dolls.\n\n[Young American Recordings]\nFounded by Rocco Giordano of Kinetic Records and Josh Swade of Maverick Records, it was an independent label that included groups such as British rock band South and worked with other popular groups such as Scottish punk band APB.\n\n[APB (band)]\nAPB was a Scottish post-punk band, formed in 1979, that blended funk rock, punk rock and new wave music. The group had only modest success during its brief run, yet their influence can be heard in the sound of such current bands as Franz Ferdinand, The Rapture, and Red Hot Chili Peppers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q64ac359215",
  "kind": "yes/no",
  "text": "Claim: Chester C. Dillian coached at the school at which James C. Klotter was a history professor. He coached sports there for one year from 1929-1930. The college was chartered in 1829.\n\nPassages:\n\n[Chester Dillon]\nHe served as the head football coach at Dakota Wesleyan University (1915–1916), Simpson College (1916–1917), Howard College in Homewood, Alabama—now Samford University (1919, 1927–1928), Oshkosh State Normal School—now the University of Wisconsin–Oshkosh (1920), Georgetown College in Georgetown, Kentucky (1929–1930), and Jacksonville State Teachers College—now Jacksonville State University (1938–1939, 1945).\n\n[James C. Klotter]\nKlotter also is a history professor at Georgetown College and one of the co-authors of Kentucky's staple history book \"A New History of Kentucky\".\n\n[Georgetown College]\nChartered in 1829, Georgetown was the first Baptist college west of the Allegheny Mountains.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa4099ec5dc",
  "kind": "yes/no",
  "text": "Post: that moment when a winter storm keeps people at home more than the pandemic has.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q3325066f40",
  "kind": "yes/no",
  "text": "Claim: Ram Niwas Mirdha was chairman of a national level academy for performing arts. This is where the music composer of Daina (1984 film) won his award in 2008.\n\nPassages:\n\n[Bhupen Hazarika]\nRecipient of Sangeet Natak Akademi Award (1987), Padmashri (1977), and Padmabhushan (2001), Hazarika was awarded with Dada Saheb Phalke Award (1992), India's highest award in cinema, by the Government of India and Sangeet Natak Akademi Fellowship (2008), the highest award of the Sangeet Natak Akademi, India's The National Academy for Music, Dance and Drama.\n\n[Sangeet Natak Akademi]\nSangeet Natak Akademi (Devanāgarī: \"संगीत नाटक अकादेमी\" or The National Academy for Music, Dance and Drama in English) is the national level academy for performing arts set up by the Government of India.\n\n[Daina (1984 film)]\nThe music for the film is composed by Dr. Bhupen Hazarika.\n\n[Ram Niwas Mirdha]\nHe served as chairman of the Sangeet Natak Akademi until his death from multiple organ failure.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qabebc5951d",
  "kind": "yes/no",
  "text": "Claim: The bay in the body of water that is east of the Republic of Ireland is where SS Ellan Vannin (1883) was lost in a storm. It is also where Wales's first offshore wind farm is located west of london\n\nPassages:\n\n[Republic of Ireland]\nIt is otherwise surrounded by the Atlantic Ocean, with the Celtic Sea to the south, Saint George's Channel to the south-east, and the Irish Sea to the east.\n\n[Liverpool Bay]\nLiverpool Bay is a bay of the Irish Sea between northeast Wales, Cheshire, Lancashire and Merseyside to the east of the Irish Sea.\n\n[North Hoyle Offshore Wind Farm]\nNorth Hoyle Offshore Wind Farm is Wales' first offshore wind farm, and the UK's first major offshore renewable power project.\n\n[SS Ellan Vannin (1883)]\nAs \"Ellan Vannin\" she served for a further 26 years before being lost in a storm on 3 December 1909 in Liverpool Bay.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7da8b9f5a0",
  "kind": "yes/no",
  "text": "Claim: Blast Vegas starred the actor and musician who played the title character on FOX's Malcolm in the Middle.\n\nPassages:\n\n[Blast Vegas]\nIt first aired on the Syfy channel on July 18, 2013, and stars Frankie Muniz, Barry Bostwick, and Maggie Castle.\n\n[Frankie Muniz]\nHe is best known for playing the title character in the Fox television family sitcom \"Malcolm in the Middle\", which earned him an Emmy Award nomination and two Golden Globe Award nominations.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q979499d15c",
  "kind": "yes/no",
  "text": "Claim: Marjorie McGinnis was the original female founder of the brewery that was purchased in 2006 by the largest brewery in the state of Taiwan.\n\nPassages:\n\n[Frederick Brewing Company]\nIt was founded sometime between 1992 and 1993 by Marjorie McGinnis, Kevin Brannon, and Steve Nordahl and had its grand opening on 12 February 1997. In early 2002 or 2003 the company was placed into receivership and in 2006 was purchased by Flying Dog Brewery and renamed Wild Goose Brewery.\n\n[Flying Dog Brewery]\nFounded in 1990 by George Stranahan and Richard McIntyre, it is the largest brewery in Maryland.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qec120e1ad6",
  "kind": "yes/no",
  "text": "Claim: African-American actor Andy Samberg starred in the comedy film Take the 10, released on Netflix on January 20, 2017.\n\nPassages:\n\n[Take the 10]\nTake the 10 is a 2017 American comedy film written and directed by Chester Tam. The film stars Josh Peck, Tony Revolori, Emily Chang, Cleopatra Coleman, Kevin Corrigan and Andy Samberg.\n\n[Andy Samberg]\nAndrew David Samberg (born David A. J. Samberg; August 18, 1978) is an American actor, filmmaker, musician and comedian.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7b173044e8",
  "kind": "yes/no",
  "text": "Post: North Dakota: *has one decent week of weather*\nMother Nature: NOW I SHALL CAST OUT THE SUN AND BRING THE COLDEST OF RAINS UPON THY SUPER, DUPER FLAT LAND.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q0de81e50a6",
  "kind": "yes/no",
  "text": "Text: Gods playing games today. Makin it 68 degrees but 1000% humidity. Smh",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q6f8491b4c3",
  "kind": "yes/no",
  "text": "Claim: The Melvins was formed earlier than another band. This other band released an album titled Artifakt.\n\nPassages:\n\n[Artifakt]\nArtifakt is a compilation album by Better Than Ezra, sold only at the band's concerts and through the official Better Than Ezra merchandise website beginning in 2001.\n\n[Melvins]\nThe Melvins are an American rock band that formed in 1983 in Montesano, Washington.\n\n[Better Than Ezra]\nBetter Than Ezra is an American alternative rock band based in New Orleans, Louisiana, and signed to The End Records. The band formed in 1988 in Baton Rouge, Louisiana.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6b94c4693a",
  "kind": "yes/no",
  "text": "Claim: A combat flight simulator video game published by Konami and released in 2012 features missions including the attack on Pearl Harbour by Microsoft on December 7, 1941.\n\nPassages:\n\n[Pearl Harbor]\nThe attack on Pearl Harbor by the Empire of Japan on December 7, 1941, was the immediate cause of the United States' entry into World War II.\n\n[Birds of Steel]\nBirds of Steel (蒼の英雄 Birds of Steel , Ao no Eiyuu: Birds of Steel ) is a combat flight simulator video game created by Gaijin Entertainment and published by Konami. It was released on March 13, 2012 for PlayStation 3 and Xbox 360. The game includes more than one hundred non-fictional planes, twenty historical missions, and hundreds of procedural missions over sixteen different locations, including Pearl Harbor and Wake Island.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc30e9adc39",
  "kind": "yes/no",
  "text": "Claim: \"A Swingin' Safari\" was a song written originally by German songwriter Bert Kaempfert but made popular by Billy Vaughn.\n\nPassages:\n\n[Bert Kaempfert]\nBerthold Heinrich Kämpfert, (16 October 1923 – 21 June 1980), better known as Bert Kaempfert, was a German orchestra leader, music producer, and songwriter.\n\n[A Swingin' Safari]\nThat same year, Billy Vaughn recorded it, and his cover reached number 13 on the \"Billboard\" charts that summer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q032d852dcc",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "This book makes me feel like I don't really know how to read.",
   "If you ever wanted to know what it feels like to have dyslexia I would recommend the book House of Leaves."
  ]
 },
 {
  "qid": "qe69bbd7522",
  "kind": "yes/no",
  "text": "Claim: Charles Robinson, Jr. was the eight mayor of a town laid out in 1629 by the engineer Jim Rhodes.\n\nPassages:\n\n[Charles Robinson, Jr.]\nCharles Robinson, Jr. (November 6, 1829 – July 30, 1891) was a Massachusetts politician who served as the eighth mayor of Charlestown, Massachusetts.\n\n[Charlestown, Boston]\nCharlestown is the oldest neighborhood in Boston, Massachusetts, United States. Charlestown was laid out in 1629 by engineer Thomas Graves, one of its early settlers, in the reign of Charles I of England.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa0018dd436",
  "kind": "yes/no",
  "text": "Claim: Prince William, Duke of Gloucester and Prince George of Denmark, were eventually monarchs of Great Britain Kingdom in the 15th century.\n\nPassages:\n\n[Prince William, Duke of Gloucester]\nPrince William, Duke of Gloucester (24 July 1689 – 30 July 1700 ) was the son of Princess Anne, later Queen of England, Ireland and Scotland from 1702, and her husband, Prince George, Duke of Cumberland.\n\n[Prince George of Denmark]\nPrince George of Denmark and Norway, Duke of Cumberland (Danish: \"Jørgen\" ; 2 April 165328 October 1708), was the husband of Queen Anne, who reigned over Great Britain from 1702.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q179b9bfd7a",
  "kind": "yes/no",
  "text": "Claim: Soletrader Peek A Boo is of this long-haired breed. It and Toy Trawler Spaniel are both breeds of dog.\n\nPassages:\n\n[Soletrader Peek A Boo]\nSoletrader Peek A Boo, also known as Jilly, is a Petit Basset Griffon Vendéen show dog owned by Sara Robertson and Wendy Doherty and handled by Gavin Robertson, who won Best in Show at Crufts in 2013.\n\n[Petit Basset Griffon Vendéen]\nThe Petit Basset Griffon Vendéen ( ), or PBGV, is a breed of dog of the scent hound type, bred to trail hares in bramble-filled terrain of the Vendée district of France.\n\n[Toy Trawler Spaniel]\nThe Toy Trawler Spaniel is an extinct breed of Spaniel which physically was similar to the King Charles Spaniel of the 16th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q38f0b74678",
  "kind": "yes/no",
  "text": "Text: crocheting is hard",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qb04e228c91",
  "kind": "yes/no",
  "text": "Claim: The Lady magazine was published before the magazine Christelyn Karazin writes for.\n\nPassages:\n\n[The Lady (magazine)]\nThe Lady is Britain's longest-running weekly women's magazine. It has been in continuous publication since 1885 and is based in London.\n\n[Woman's Day]\nThe magazine was first published in 1931 by The Great Atlantic & Pacific Tea Company; the current publisher is Hearst Corporation.\n\n[Christelyn Karazin]\nShe hosts the blog \"Beyond Black & White\" and has written for \"Woman's Day\", \"Ebony\", \"Jet\", and Reuters.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qefa2813678",
  "kind": "yes/no",
  "text": "Claim: Both the director of Here Comes Mr. Jordan and Pierre Morel have the profession of film director.\n\nPassages:\n\n[Here Comes Mr. Jordan]\n\"Here Comes Mr. Jordan\" was adapted by Sidney Buchman and Seton I. Miller from the play \"Heaven Can Wait\", written by Harry Segall and directed by Alexander Hall.\n\n[Alexander Hall]\nAlexander Hall (January 11, 1894, Boston, Massachusetts – July 30, 1968, San Francisco, California) was an American film director and theatre actor.\n\n[Pierre Morel]\nPierre Morel (born 12 May 1964) is a French film director and cinematographer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5ca351d486",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I will not be granting an extension to the student who emailed me and my co-teacher and got both of our names wrong.",
   "V excited to grant an extension to students who email me and my co-teacher and get both of our names wrong"
  ]
 },
 {
  "qid": "q14ce497db0",
  "kind": "yes/no",
  "text": "Post: @BarbosaBox The best thing is Greg Paul’s face in the back",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q79eb1e98dc",
  "kind": "yes/no",
  "text": "Claim: American schoolteacher and publisher was the occupation of the man who published an individualist anarchist journal.\n\nPassages:\n\n[Moses Harman]\nMoses Harman (October 12, 1830January 30, 1910) was an American schoolteacher and publisher notable for his staunch support for women's rights.\n\n[Lucifer the Lightbearer]\nLucifer the Lightbearer was an individualist anarchist journal published by Moses Harman in the late 19th and early 20th centuries.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7d8547f272",
  "kind": "yes/no",
  "text": "Text: considering crowd surfing the next time the hallways are too packed",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qb867b5a640",
  "kind": "yes/no",
  "text": "Claim: Author of My Father's Tears and Other Stories published on June 2, 2009 and Bret Easton Ellis both had the profession of short story writer.\n\nPassages:\n\n[My Father's Tears and Other Stories]\nMy Father's Tears and Other Stories by John Updike was published posthumously on June 2, 2009.\n\n[Bret Easton Ellis]\nBret Easton Ellis (born March 7, 1964) is an American author, screenwriter, and short story writer.\n\n[John Updike]\nJohn Hoyer Updike (March 18, 1932 – January 27, 2009) was an American novelist, poet, short story writer, art critic, and literary critic.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1b50bbca8a",
  "kind": "yes/no",
  "text": "Claim: The host of Tosh.0 conducts stand-up comedy tours.\n\nPassages:\n\n[Tosh.0]\nTosh.0 ( ) is an American television series hosted and produced by comedian Daniel Tosh, who provides commentary on online viral video clips, society, celebrities, and other parts of popular culture and stereotypes.\n\n[Daniel Tosh]\nHe is known for his deliberately offensive and controversial style of black comedy, as the host of the Comedy Central television show \"Tosh.0\" and as the star of stand-up comedy tours and specials.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2b76f266ad",
  "kind": "yes/no",
  "text": "Claim: Jim Halsey guided the career of the musician who hosted Hee Haw.\n\nPassages:\n\n[Jim Halsey]\nHalsey has guided the careers of such illustrious personalities as Roy Clark, The Oak Ridge Boys, Waylon Jennings, Reba McEntire, Clint Black, Minnie Pearl, Tammy Wynette, Merle Haggard, Dwight Yoakam, The Judds, Lee Greenwood, Hank Thompson, Woody Herman, James Brown, Roy Orbison, Leon Russell, Ricky Nelson, The Righteous Brothers, and many others.\n\n[Roy Clark]\nRoy Linwood Clark (born April 15, 1933) is an American singer and musician. He is best known for hosting \"Hee Haw\", a nationally televised country variety show, from 1969 to 1992.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3b1d921b99",
  "kind": "yes/no",
  "text": "Text: Death by Zara fitting room",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qc66504caf6",
  "kind": "yes/no",
  "text": "Claim: Greatest Hits Volume 1 is a greatest hits compilation album by The Beatles which was exclusive to Australia and New Zealand, the album was compiled by EMI Australia to fill in the gap, much like A Collection of Beatles Oldies (subtitled But Goldies!), by the English rock band the Beatles.\n\nPassages:\n\n[A Collection of Beatles Oldies]\nA Collection of Beatles Oldies (subtitled But Goldies!)\n\n[Greatest Hits Volume 1 (Beatles album)]\nThe album was compiled by EMI Australia to fill in the gap between \"Rubber Soul\" and \"Revolver\" (much like \"A Collection of Beatles Oldies\" would in 1966 in between \"Revolver\" and \"Sgt. Pepper's Lonely Hearts Club Band\").",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd05520ec6b",
  "kind": "yes/no",
  "text": "Claim: The Trials of Nikki Hill is a legal thriller written by Dick Lochte and Christopher Allen \"Chris\" Darden, an American lawyer, author, actor, lecturer, and practicing attorney.\n\nPassages:\n\n[The Trials of Nikki Hill]\nThe Trials of Nikki Hill is a legal thriller written by Christopher Darden and Dick Lochte, and published Time Warner Company in 1999.\n\n[Christopher Darden]\nChristopher Allen \"Chris\" Darden (born April 7, 1956) is an American lawyer, author, actor, lecturer, and practicing attorney.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q06cc718ba4",
  "kind": "yes/no",
  "text": "Claim: Wikimedia Foundation runs the website surpassed by both Hudong.com and the encyclopedia that had the humorous hoax Baidu 10 Mythical Creatures.\n\nPassages:\n\n[Baidu Baike]\nIts test version was released on 20 April 2006, and within three weeks the encyclopedia had grown to more than 90,000 articles surpassing the number in Chinese Wikipedia.\n\n[Chinese Wikipedia]\nThe Chinese Wikipedia () is the (Standard) Chinese language edition of Wikipedia. It is run by the Wikimedia Foundation.\n\n[Baidu 10 Mythical Creatures]\nThe Baidu 10 Mythical Creatures (), alternatively Ten Baidu Deities, was initially a humorous hoax from the interactive encyclopedia Baidu Baike which became a popular and widespread Internet meme in the People's Republic of China in early 2009.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc4a9c50534",
  "kind": "yes/no",
  "text": "Claim: The former British protectorate of the southern Africa territory founded by Cecil Rhodes became two countries with the Zambezi river as the border. Zimbabwe lies to the south; Zambia is north of the river.\n\nPassages:\n\n[Rhodesia (region)]\nThe territory to the north of the Zambezi was officially designated Northern Rhodesia by the Company, and has been Zambia since 1964; that to the south, which the Company dubbed Southern Rhodesia, became Zimbabwe in 1980.\n\n[Northern Rhodesia]\nFrom 1924 it was administered by the British government as a protectorate under similar conditions to other British-administered protectorates, and the special provisions required when it was administered by BSAC were terminated.\n\n[Cecil Rhodes]\nAn ardent believer in British imperialism, Rhodes and his British South Africa Company founded the southern African territory of Rhodesia (now Zimbabwe and Zambia), which the company named after him in 1895.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q521355b7ef",
  "kind": "yes/no",
  "text": "Claim: An editor of Locus Solus and A. E. Housman have the same nationality.\n\nPassages:\n\n[Locus Solus (journal)]\nThe magazine was edited by the poets John Ashbery, Kenneth Koch, and James Schuyler, all of whom contributed to its four issues.\n\n[A. E. Housman]\nAlfred Edward Housman ( ; 26 March 1859 – 30 April 1936), usually known as A. E. Housman, was an English classical scholar and poet, best known to the general public for his cycle of poems \"A Shropshire Lad\".\n\n[James Schuyler]\nJames Marcus Schuyler (November 9, 1923 – April 12, 1991) was an American poet.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc0cccc59c2",
  "kind": "yes/no",
  "text": "Text: Oh wow, trolls really have a lot of time on there hands, jeez 🙄 they really don’t like getting banned #twitchtrolls",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q7ced4d881c",
  "kind": "yes/no",
  "text": "Claim: James John Liautaud is the founder, chairman, and majority owner of Jimmy John’s, founded in 1983.\n\nPassages:\n\n[Jimmy John's]\nFounded by Jimmy John Liautaud in 1983 and headquartered in Champaign, Illinois, in 30 years, the company has grown to more than 2,500 locations in all states except Alaska, Hawaii, Connecticut, Maine, New Hampshire, and Vermont.\n\n[Jimmy John Liautaud]\nJames John Liautaud (January 12, 1964) is the founder, chairman, and majority owner of Jimmy John’s sandwich chain.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q36f98b3b30",
  "kind": "yes/no",
  "text": "Claim: This Hall of Fame point guard was first selected for an NBA All-Star Game in 1994, alongside All-Star. He was the Defensive Player of the Year for the team which Barry Ackerley was the franchise owner, in the 1995–96 NBA season.\n\nPassages:\n\n[Gary Payton]\nHe started at the point guard position. He was inducted into the Naismith Basketball Hall of Fame on September 8, 2013.\n\n[1995–96 Seattle SuperSonics season]\nShawn Kemp and Defensive Player of the Year, Gary Payton were both selected for the 1996 NBA All-Star Game.\n\n[1993–94 Seattle SuperSonics season]\nGary Payton made his first All-Star appearance as he was selected for the 1994 NBA All-Star Game along with Shawn Kemp.\n\n[Barry Ackerley]\nHe was the owner of the Seattle SuperSonics basketball franchise from 1983 to 2001.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qbc5aed7e61",
  "kind": "yes/no",
  "text": "Claim: The city that Daewoong Pharmaceutical Co., Ltd is based in is the world's 16th largest city by population.\n\nPassages:\n\n[Seoul]\nSeoul is the world's 16th largest city, and forms the heart of the Seoul Capital Area, which includes the surrounding Incheon metropolis and Gyeonggi province.\n\n[Daewoong Pharmaceutical Co., Ltd]\nDaewoong Pharmaceutical Co., Ltd (Korean: 대웅제약) is a Seoul, South Korea-based bioengineering company operating as a subsidiary of Daewoong Co., Ltd., a global health care group.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbe11791ee2",
  "kind": "yes/no",
  "text": "Claim: Between this plant and Darwinia, the genus with more species is Darwinia. This plant is called Saule in French.\n\nPassages:\n\n[Willow]\nWillows, also called sallows, and osiers, form the genus Salix, around 400 species of deciduous trees and shrubs, found primarily on moist soils in cold and temperate regions of the Northern Hemisphere.\n\n[Saule]\nSaule is the French equivalent for the Willow\n\n[Darwinia (plant)]\nDarwinia, sometimes commonly known as mountain bells or simply bells, is a genus of about 70 species of evergreen shrubs in the family Myrtaceae, endemic to southeastern and southwestern Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0a434ee964",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "i love 6 hour panic attacks",
   "I don't like having 6-hour panic attacks."
  ]
 },
 {
  "qid": "q7111164c1e",
  "kind": "yes/no",
  "text": "Claim: The rock band who performed live on the 1999 album, American Jet Set, is from the city where Incapital has its corporate headquarters. Louis XIV is not from this city.\n\nPassages:\n\n[Louis XIV (band)]\nLouis XIV is an American rock band from San Diego, California.\n\n[American Jet Set]\nAmerican Jet Set (1999) is an album by Kill Hannah.\n\n[Kill Hannah]\nKill Hannah was an American rock band formed in 1993 in Chicago, Illinois.\n\n[Incapital]\nIncapital has multiple offices throughout the U.S., with corporate headquarters in Chicago and a major sales, trading and capital markets office in Boca Raton, Florida.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb3a3823415",
  "kind": "yes/no",
  "text": "Claim: Clark County in Nevada contains both the City of Las Vegas and another Chrisitan college. Craig Heyer played baseball at that college.\n\nPassages:\n\n[Clark County, Nevada]\nLas Vegas, Nevada's most populous city, has been the county seat since the county was established.\n\n[College of Southern Nevada]\nThe College of Southern Nevada (CSN) is primarily a two-year college in Clark County, Nevada, with four four-year degrees in Dental Hygiene, Medical Lab Scientist, Respiratory Sciences, and Fire & Emergency Services Admin.\n\n[Craig Heyer]\nPrior to becoming a professional, Heyer played college baseball at the College of Southern Nevada and University of Nevada, Las Vegas (UNLV).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q3c72d659c2",
  "kind": "yes/no",
  "text": "Claim: Bill Murray was the actor in the miniseries Jane Anderson wrote the screenplay for. He was also starring actor in the movie Caddyshack.\n\nPassages:\n\n[Olive Kitteridge (miniseries)]\nSet in Maine, the HBO miniseries features Frances McDormand as the title character, Richard Jenkins as Olive's loving husband Henry Kitteridge, Zoe Kazan as Denise Thibodeau, and Bill Murray as Jack Kennison.\n\n[Bill Murray]\nHe first gained exposure on \"Saturday Night Live\", a series of performances that earned him his first Emmy Award, and later starred in comedy films—including \"Meatballs\" (1979), \"Caddyshack\" (1980), \"Stripes\" (1981), \"Tootsie\" (1982), \"Ghostbusters\" (1984), \"Scrooged\" (1988), \"Ghostbusters II\" (1989), \"What About Bob?\n\n[Jane Anderson]\nShe won an Emmy Award for writing the screenplay for the miniseries \"Olive Kitteridge\" (2014).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q52f419c0cb",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "\"Jaegermeister didn't do 9/11\" or \"Jaegermeister can't melt steel beams\"",
   "Jaegermeister did 9/11"
  ]
 },
 {
  "qid": "q3ada9e458e",
  "kind": "yes/no",
  "text": "Claim: The leader of the Confederate Army of Tennessee during Hood's Tennessee Campaign died on August 30, 1879 in Hawaii.\n\nPassages:\n\n[John Bell Hood]\nJohn Bell Hood (June 1 or June 29, 1831 – August 30, 1879) was a Confederate general during the American Civil War. Arguably one of the best brigade and division commanders in the Confederate States Army, Hood gradually became increasingly ineffective as he was promoted to lead larger, independent commands late in the war; his career and reputation were marred by his decisive defeats leading an army in the Atlanta Campaign and the Franklin–Nashville Campaign.\n\n[Franklin–Nashville Campaign]\nThe Franklin–Nashville Campaign, also known as Hood's Tennessee Campaign, was a series of battles in the Western Theater, conducted from September 18 to December 27, 1864, in Alabama, Tennessee, and northwestern Georgia during the American Civil War. The Confederate Army of Tennessee under Lt. Gen. John Bell Hood drove north from Atlanta, threatening Maj. Gen. William T. Sherman's lines of communications and central Tennessee.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q83db444c33",
  "kind": "yes/no",
  "text": "Claim: Politician Lyman Sherwood was born in the New York county called Rensselaer County.\n\nPassages:\n\n[Hoosick, New York]\nHoosick is a town in Rensselaer County, New York, United States.\n\n[Lyman Sherwood]\nLyman Sherwood (August 5, 1802 Hoosick, Rensselaer County, New York – September 2, 1865 Lyons, Wayne County, New York) was an American lawyer and politician from New York.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5b7a5b356b",
  "kind": "yes/no",
  "text": "Claim: This torch song that was released on August 30, 2009, was the fourth single off of the album by Taylor Swift who co-produced that album with Nathan Chapman.\n\nPassages:\n\n[Fearless (Taylor Swift album)]\nFearless is the second studio album by the American singer-songwriter Taylor Swift. As with her first album, \"Taylor Swift\", Swift wrote or co-wrote all thirteen tracks on \"Fearless\". Swift also made her debut as a record producer, co-producing all songs on the album with Nathan Chapman.\n\n[Fifteen (song)]\n\"Fifteen\" is a country pop song performed by American singer-songwriter Taylor Swift. \"Fifteen\" was released on August 30, 2009 by Big Machine Records, as the fourth single from Swift's second studio album, \"Fearless\" (2008).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q60f0405020",
  "kind": "yes/no",
  "text": "Claim: The morning newspaper, for which Lajos Magyar worked on the staff of, and Stiffelio are not both operas.\n\nPassages:\n\n[Lajos Magyar]\nIn 1922 Magyar went to the Soviet Union as the result of an exchange of prisoners; there he worked on the staff of the Comintern and at the newspaper Pravda.\n\n[Stiffelio]\nStiffelio is an opera in three acts by Giuseppe Verdi, from an Italian libretto by Francesco Maria Piave.\n\n[Pravda]\nPravda (Russian: Правда ; ] , \"Truth\") is a Russian broadsheet newspaper, formerly the official newspaper of the Communist Party of the Soviet Union, when it was one of the most influential papers in the country with a circulation of 11 million.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc3c157b249",
  "kind": "yes/no",
  "text": "Claim: Shirley Collado is the president of the college located in New York state.\n\nPassages:\n\n[Ithaca College]\nIthaca College is a private, nonsectarian, coeducational liberal arts college located on the South Hill of Ithaca, New York, United States.\n\n[Shirley Collado]\nShirley M. Collado is a psychology professor and president of Ithaca College.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9055abefff",
  "kind": "yes/no",
  "text": "Claim: Shahzeb Khanzada's show \"To The Point\" is written in Urdu.\n\nPassages:\n\n[Express News (Pakistan)]\nExpress News is an Urdu language Pakistani television news channel Based in karachi, launched on January 1, 2008.\n\n[Shahzeb Khanzada]\nHe hosted the talk show \"To The Point\" on Express News from 2011 to 2014 and has hosted the talk show \"Aaj Shahzeb Khanzada Kay Sath\" on Geo News since January 2015.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 }
]
