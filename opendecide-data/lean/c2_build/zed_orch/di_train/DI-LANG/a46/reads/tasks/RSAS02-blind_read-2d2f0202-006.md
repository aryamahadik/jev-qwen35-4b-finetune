# A46 replay label-noise blind read RSAS02-blind_read-2d2f0202-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS02-blind_read-2d2f0202-006.json

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
  "qid": "q741b1a35b1",
  "kind": "yes/no",
  "text": "Claim: \"The Sandman\" comic book series and \"The Sandman: The Dream Hunters\" novella are written by the award-winning Neil Gaiman.\n\nPassages:\n\n[The Sandman: The Dream Hunters]\n\"The Sandman: The Dream Hunters\" is a novella by English author Neil Gaiman, illustrated by Yoshitaka Amano.\n\n[The Sandman (Vertigo)]\nThe Sandman is a comic book series written by Neil Gaiman and published by DC Comics.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q21775ed9ae",
  "kind": "yes/no",
  "text": "Claim: Alan Sokal, a professor of mathematics, authored the book Fashionable Nonsense.\n\nPassages:\n\n[Alan Sokal]\nAlan David Sokal ( ; born January 24, 1955) is a professor of mathematics at University College London and professor of physics at New York University.\n\n[Fashionable Nonsense]\nFashionable Nonsense: Postmodern Intellectuals' Abuse of Science (French: \"Impostures Intellectuelles\" ), published in the UK as Intellectual Impostures, is a book by physicists Alan Sokal and Jean Bricmont.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd8751cff45",
  "kind": "yes/no",
  "text": "Claim: The prefix given to the end of the name to avoid confusion for the winner of the 1996 Record of the Year Grammy was II.\n\nPassages:\n\n[Kiss from a Rose]\nAt the 1996 Grammy Awards, it won awards for Record of the Year, Song of the Year, and Best Male Pop Vocal Performance.\n\n[Seal (1994 album)]\nSeal (sometimes referred to as Seal II to avoid confusion with the 1991 album of the same name) is the second eponymous studio album by singer Seal.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb2fe69f388",
  "kind": "yes/no",
  "text": "Claim: M.F.A. starred the actress known for starring in E! reality series Mrs. Eastwood & Company.\n\nPassages:\n\n[M.F.A. (film)]\nThe film stars Francesca Eastwood, Clifton Collins Jr., Leah McKendrick, Peter Vack, David Huynh, Marlon Young, David Sullivan, Michael Welch and Mike Manning.\n\n[Francesca Eastwood]\nShe is known for starring in \"Mrs. Eastwood & Company\", the E! reality series that she shares with her family.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5cd69ddf38",
  "kind": "yes/no",
  "text": "Claim: A highway replaced by another highway has a junction at Cairo Junction. It is 1286 miles long. Streatorland is the area east of the other highway.\n\nPassages:\n\n[Streatorland]\nIt can be more broadly defined as the area east of Interstate 39, west of Interstate 55, and south of the Illinois River.\n\n[Cairo Junction, Illinois]\nCairo Junction is located at the junction of U.S. Route 51, Illinois Route 3, and Illinois Route 37 north of Cairo.\n\n[U.S. Route 51]\nU.S. Route 51 is a south-north United States highway that runs for 1286 mi from the western suburbs of New Orleans, Louisiana to within 100 ft of the Wisconsin–Michigan border.\n\n[Interstate 39]\nI-39 was designed to replace U.S. Route 51 (US 51), which in the early 1980s was one of the busiest two-lane highways in the United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qde80dc320e",
  "kind": "yes/no",
  "text": "Claim: Grafton and Carroll counties, as well as the Pratt Family Camps, border Squam Lake in New Hampshire.\n\nPassages:\n\n[Pratt Family Camps]\nThe camps consist of three primary camp houses and a collection of outbuildings constructed by the Pratt family over an 85-year period on more than 80 acre of lakefront property on Squam Lake.\n\n[Squam Lake]\nSquam Lake is a lake located in the Lakes Region of central New Hampshire, United States, south of the White Mountains, straddling the borders of Grafton, Carroll, and Belknap counties.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2cb56ffe80",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Just tested my egg drop at my apartment complex and it fell on a man’s head :) but no worries he was bald so the yolk just wiped right off",
   "Just tested my egg drop at my apartment complex and it fell on a man's head :) he said it was fine because he has no hair, but I felt awful about it."
  ]
 },
 {
  "qid": "q5ed939e576",
  "kind": "yes/no",
  "text": "Claim: Nekeshia Shiondrail Henderson is an American former professional basketball player who played college basketball for a team Karen Aston has head coached since April 1, 2012, representing The University of Texas.\n\nPassages:\n\n[Texas Longhorns women's basketball]\nThe Texas Longhorns women's basketball team represents The University of Texas at Austin in NCAA Division I intercollegiate women's basketball competition.\n\n[Karen Aston]\nSince April 2012 she has served as the women's basketball head coach of the Texas Longhorns women's basketball program.\n\n[Nekeshia Henderson]\nNekeshia Shiondrail Henderson (born February 28, 1973) is an American former professional basketball guard who played for the Houston Comets of the Women's National Basketball Association (WNBA). She played college basketball at Texas.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe810a7e135",
  "kind": "yes/no",
  "text": "Claim: The author of the book \"A New Kind of Science\" designed a computer algebra system at Caltech in California.\n\nPassages:\n\n[Symbolic Manipulation Program]\nSymbolic Manipulation Program, usually called SMP, was a computer algebra system designed by Chris A. Cole and Stephen Wolfram at Caltech circa 1979 and initially developed in the Caltech physics department under Wolfram's leadership with contributions from Geoffrey C. Fox, Jeffrey M. Greif, Eric D. Mjolsness, Larry J. Romans, Timothy Shaw, and Anthony E. Terrano.\n\n[Stephen Wolfram]\nHe is the author of the book \"A New Kind of Science.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa3ddf2f9db",
  "kind": "yes/no",
  "text": "Claim: Passionate Love is a South Korean weekend television drama series first aired on NBC starring Sung Hoon and the actress starring in a movie that was filmed in Korea in 2012.\n\nPassages:\n\n[Passionate Love]\nPassionate Love () is a 2013 South Korean weekend television drama series starring Sung Hoon and Choi Yoon-young.\n\n[As One (film)]\n\"Korea\") is a 2012 South Korean sports drama film starring Ha Ji-won and Bae Doona.\n\n[Choi Yoon-young]\nShe then appeared twice on the big screen in 2012: in the short film \"Endless Flight\" in omnibus \"Horror Stories\", and the table tennis sports film \"As One\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q614fbdb0a2",
  "kind": "yes/no",
  "text": "Tweet: I support my brilliant and intrepid coworkers organizing for better wages and working conditions here at KUOW! #SoundStoriesSoundWages @wemakekuow @sagaftra https://t.co/5NXuz4ERqq",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qd73ba38912",
  "kind": "yes/no",
  "text": "Claim: Justin Bieber is the Canadian singer who was originally featured on the song \"Bankroll\" composed by American DJ Diplo.\n\nPassages:\n\n[Bankroll (song)]\nOriginally, Justin Bieber was featured on the song, but due to Bieber already having exclusives with DJ Khaled (\"I'm the One\") and David Guetta (\"2U\") at around the same time as Diplo released \"Bankroll\", Diplo was forced to remove the original from his SoundCloud account.\n\n[I'm the One (DJ Khaled song)]\n\"I'm the One\" is a song written and performed by American musician DJ Khaled; Canadian singer Justin Bieber; and American rappers Quavo, Chance the Rapper and Lil Wayne.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q931eddc57d",
  "kind": "yes/no",
  "text": "Claim: The American art critic that met Joseph Drapell died after the death of Agatha Christie.\n\nPassages:\n\n[Joseph Drapell]\nAt the Cranbrook Academy he met visiting Canadian artist Jack Bush and the American art critic Clement Greenberg, who influenced his work.\n\n[Agatha Christie]\nDame Agatha Mary Clarissa Christie, Lady Mallowan, DBE (\"née\" Miller; 15 September 1890 – 12 January 1976) was an English crime novelist, short story writer and playwright.\n\n[Clement Greenberg]\nClement Greenberg ( ), occasionally writing under the pseudonym K. Hardesh (January 16, 1909 – May 7, 1994), was an American essayist known mainly as an influential visual art critic closely associated with American Modern art of the mid-20th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa084eab7eb",
  "kind": "yes/no",
  "text": "Claim: The author of the fantasy short story and fairy series, \"Dănilă Prepeleac\", was born in 1837.\n\nPassages:\n\n[Ion Creangă]\nIon Creangă (] ; also known as Nică al lui Ștefan a Petrei, Ion Torcălău and Ioan Ștefănescu; March 1, 1837 – December 31, 1889) was a Moldavian, later Romanian writer, raconteur and schoolteacher.\n\n[Dănilă Prepeleac]\n\"Dănilă Prepeleac\" (] ; occasionally translated as \"Danilo the Pole\", \"Dănilă Haystack-Peg\" or \"Danillo Nonsuch\") is an 1876 fantasy short story and fairy tale by Romanian author Ion Creangă, with a theme echoing influences from local folklore.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc2d3376fa7",
  "kind": "yes/no",
  "text": "Claim: Rhapsody, Op. 1 was written by a male composer. This composer was Hungarian, not Johann Christoph Pepusch.\n\nPassages:\n\n[Béla Bartók]\nBéla Viktor János Bartók ( ; ] ; 25 March 1881 – 26 September 1945) was a Hungarian composer, pianist and an ethnomusicologist.\n\n[Rhapsody, Op. 1 (Bartók)]\n1, Sz.\n\n[Johann Christoph Pepusch]\nJohann Christoph Pepusch (1667 – 20 July 1752), also known as John Christopher Pepusch and Dr Pepusch, was a German-born composer who spent most of his working life in England.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qef1891bb5e",
  "kind": "yes/no",
  "text": "Claim: Aaron Waisglass gained recognition as a trap artist for remixing Rihanna's song released on March 26, 2015.\n\nPassages:\n\n[Grandtheft]\nAaron Waisglass, better known by his stage name Grandtheft, is a Canadian DJ and musician based in Toronto. He gained recognition as a trap artist, for remixing songs like “Summer“, “Sweet Nothing“ and “Bitch Better Have My Money” and having songs charted around the world.\n\n[Bitch Better Have My Money]\n\"Bitch Better Have My Money\" is a song recorded by Barbadian singer Rihanna. The song was digitally released on March 26, 2015, through the iTunes Store.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc1a12dd212",
  "kind": "yes/no",
  "text": "Claim: G.D. Spradlin's collaborator portrayed the character Terry Malloy in \"The Love of Captain\". He also starred in a 1957 movie with Soo Yong.\n\nPassages:\n\n[Soo Yong]\nAmong them were \"The Good Earth\" (1937), \"Love Is a Many-Splendored Thing\" (1955), and \"Sayonara\" (1957).\n\n[Marlon Brando]\nBrando is widely known for his Academy Award-winning performances as Terry Malloy in \"On the Waterfront\" (1954) and Vito Corleone in \"The Godfather\" (1972), as well as his performances in \"A Streetcar Named Desire\" (1951), \"Viva Zapata!\n\n[Sayonara]\nSayonara is a 1957 Technicolor American film starring Marlon Brando in Technirama.\n\n[G. D. Spradlin]\nHe is credited in over 70 television and film productions, and performed alongside actors including Marlon Brando, Al Pacino, Charlton Heston, George C. Scott, and Johnny Depp.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7bd943d543",
  "kind": "yes/no",
  "text": "Tweet: #HappyBirthdayKeanuReeves Keanu Reeves is so wholesome ☺️",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q9bd671e22d",
  "kind": "yes/no",
  "text": "Claim: What's Golden was included in an open world racing video game that was developed by Playground games and published by Microsoft Studios in 2010.\n\nPassages:\n\n[Forza Horizon 3]\nForza Horizon 3 is an open world racing video game developed by Playground Games and published by Microsoft Studios for Xbox One and Microsoft Windows 10.\n\n[What's Golden]\nThe song was additionally included in the video game Forza Horizon 3 on the fictional radio 'Block Party'.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q344c0c2d11",
  "kind": "yes/no",
  "text": "Post: Boehner not clapping for gender pay equality. COOL.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qaa4a8a8f3b",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "@Torialou78 My excellent photography skills! :p lmao!!!",
   "I do not think I did a very good job of taking that photograph!"
  ]
 },
 {
  "qid": "q153bd70bdc",
  "kind": "yes/no",
  "text": "Claim: The broadcast studio of the commercial channel that along with CNN and BBC disputes the murderer of Neda is at 1211 Avenue of the Americas, New York City, New York.\n\nPassages:\n\n[Death of Neda Agha-Soltan]\nThe murderer of Neda is disputed; according to CNN, BBC, and Fox News, she was shot by Basij, a paramilitary organization.\n\n[Fox News]\nFox News (officially known as the Fox News Channel, commonly abbreviated to FNC) is an American basic cable and satellite television news channel owned by the Fox Entertainment Group, a subsidiary of 21st Century Fox. The channel broadcasts primarily from studios at 1211 Avenue of the Americas, New York City, New York.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q974fc0f769",
  "kind": "yes/no",
  "text": "Claim: Doñana National Park was a nature reserve that was established in 1969. The place where the river Tiétar flows into the Baikal lynx was not established in 1969.\n\nPassages:\n\n[Tiétar (river)]\nIt flows into the Tagus at Monfragüe.\n\n[Monfragüe]\nMonfragüe (Spanish: \"Parque Nacional Monfragüe\") is a Spanish national park noted for its bird-life.\n\n[Doñana National Park]\nDoñana National Park is a natural reserve in Andalusia, southern Spain, in the provinces of Huelva (most of its territory) and Seville. It was established as a nature reserve in 1969 when the World Wildlife Fund joined with the Spanish government and purchased a section of marshes to protect it.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7c707a5f1b",
  "kind": "yes/no",
  "text": "Claim: The writer of the poetry book She Walks These Hills was born February 26, 1948.\n\nPassages:\n\n[Sharyn McCrumb]\nSharyn McCrumb (born February 26, 1948) is an American writer whose books celebrate the history and folklore of Appalachia.\n\n[She Walks These Hills]\nShe Walks These Hills is a book written by Sharyn McCrumb and published by Charles Scribner's Sons in 1994, which later went on to win the Anthony Award for Best Novel in 1995.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf87acddd24",
  "kind": "yes/no",
  "text": "Claim: The American who owned a piece of land died in May 1999. This piece of land was once owned by Count de Mauny Talvande.\n\nPassages:\n\n[Taprobane Island]\nThe islet passed on to the American author and composer Paul Bowles and then the Sri Lankan born former UN Chief Prosecutor Sir Desmond Lorenz de Silva before it came to the ownership of the Australian businessman Geoffrey Dobbs.\n\n[Count de Mauny]\nMaurice Talvande, Count de Mauny Talvande (self styled), (1866–1941) was a French-born naturalised British landscaper, furniture-maker, and self-inventor, who is best known as the owner and recreator of Taprobane Island, in Sri Lanka.\n\n[Paul Bowles]\nPaul Frederic Bowles ( ; December 30, 1910November 18, 1999) was an American expatriate composer, author, and translator.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa2bec9cd7a",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I love this site",
   "Hate this site [CHIRPBIRDICON]"
  ]
 },
 {
  "qid": "q5d037c56f7",
  "kind": "yes/no",
  "text": "Claim: ER White is the current lead guitarist for the band that released the album This Is Your Way Out.\n\nPassages:\n\n[Emarosa]\nThe band currently consists of founding members ER White (lead guitar) and Jordan Stewart (keyboards), as well as lead vocalist Bradley Walden and rhythm guitarist Marcellus Wallace.\n\n[This Is Your Way Out]\nThis Is Your Way Out is the first EP record by Emarosa, released May 1, 2007.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0f94184842",
  "kind": "yes/no",
  "text": "Text: @Ciara87C @RachaelSmarty @SashaHumphreys2 my tinder convos have been leaked",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q02412c1fe4",
  "kind": "yes/no",
  "text": "Claim: The song, which Billie Anthony is best known for her Top 10 hit version, topped the UK chart in 1981 in a recording by a platinum-selling Welsh rock and roll singer whose recording and performing career began in the late 1960s.\n\nPassages:\n\n[Shakin' Stevens]\nMichael Barratt (born 4 March 1948), known as Shakin' Stevens, is a platinum-selling British rock and roll singer and songwriter who was the UK's biggest-selling singles artist of the 1980s. His recording and performing career began in the late 1960s, although it was not until 1980 that his commercial success began.\n\n[Billie Anthony]\nShe is best known for her Top 10 hit version of \"This Ole House\", which despite chart competition from other versions of the same song, reached No. 4 in the UK chart.\n\n[This Ole House]\n\"This Ole House\" (sometimes written \"This Old House\") is a popular song written by Stuart Hamblen, and published in 1954. The song again topped the UK chart in 1981 in a recording by Shakin' Stevens.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9bdd51aa17",
  "kind": "yes/no",
  "text": "Claim: Robert Johnson Tenner played collegiate ball for a university. That university and Baylor College of Medicine are not located in the same state.\n\nPassages:\n\n[University of Minnesota]\nThe University of Minnesota, Twin Cities (often referred to as The University of Minnesota, Minnesota, the U of M, UMN, or simply the U) is a public research university in Minneapolis and Saint Paul, Minnesota.\n\n[Baylor College of Medicine]\nBaylor College of Medicine (BCM), located in the Texas Medical Center in Houston, Texas, US, is a health sciences university.\n\n[Bob Tenner]\nTenner played collegiate ball for the University of Minnesota and played professionally for 1 season, in 1935.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q77744dba34",
  "kind": "yes/no",
  "text": "Claim: The short story from The Wind's Twelve Quarters that won the Hugo Award in 1974 was published in 1973 on January 27th.\n\nPassages:\n\n[The Ones Who Walk Away from Omelas]\n\"The Ones Who Walk Away from Omelas\" is a 1973 plotless, short, descriptive work of philosophical fiction, though popularly classified as a short story, by American writer Ursula K. Le Guin.\n\n[The Wind's Twelve Quarters]\nThe story \"The Ones Who Walk Away from Omelas\" won the Hugo Award in 1974, while \"The Day Before the Revolution\" won the Locus and Nebula Awards in 1975.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa2a867e168",
  "kind": "yes/no",
  "text": "Text: Currently bombing aces on the volleyball court and math tests in the classroom.\n#StudentAthlete",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qd45b5e19fa",
  "kind": "yes/no",
  "text": "Claim: The publication Paper is focused more on the adult demographic than the magazine which merged with Children's Digest.\n\nPassages:\n\n[Children's Digest]\nChildren's Digest (originally \"The Children's Digest\") was a children's magazine published from Oct. 1950 to May/June 2009, after which it was merged with \"Jack and Jill\" from the same publisher.\n\n[Paper (magazine)]\nPaper, stylized as PAPER, is a New York City-based independent magazine focusing on fashion, popular culture, nightlife, music, art and film.\n\n[Jack and Jill (magazine)]\nJack and Jill is an American bimonthly magazine for children 7 to 12 years old that takes its title from the nursery rhyme of the same name.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q61ddb047dc",
  "kind": "yes/no",
  "text": "Claim: The player who defeated Johnny Majors for the Heisman Trophy in 1956 was born in 1935.\n\nPassages:\n\n[Johnny Majors]\nHe finished second to Paul Hornung in voting for the Heisman Trophy in 1956.\n\n[Paul Hornung]\nPaul Vernon Hornung (born December 23, 1935), nicknamed \"The Golden Boy\", is a former professional American football player, a Hall of Fame running back for the Green Bay Packers of the National Football League (NFL) from 1957 to 1966, winning four NFL titles and the first Super Bowl.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc2278f3c3b",
  "kind": "yes/no",
  "text": "Claim: An American actor who was a CIA operative in Chuck Versus the A-Team was born in October of 1974. The actor plays a character in commercials for a deodorant brand. Mark Fitzloff is known for reviving the deodorant brand.\n\nPassages:\n\n[Chuck Versus the A-Team]\nChuck fears the CIA's new operatives (Isaiah Mustafa and Stacy Keibler), who have downloaded the Intersect, will render him obsolete.\n\n[Mark Fitzloff]\nHe is most known for his work at Wieden+Kennedy on Nike and Coca-Cola, and for reviving Procter & Gamble's Old Spice brand.\n\n[Isaiah Mustafa]\nIsaiah Amir Mustafa (born February 11, 1974) is an American actor and former NFL practice squad wide receiver.\n\n[Make a Smellmitment]\nThe \"Make a Smellmitment\" campaign retains much of the format from the previous campaign including its characters played by Isaiah Mustafa and Terry Crews.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q39ab98794a",
  "kind": "yes/no",
  "text": "Claim: Dana Fox wrote Tom Vaughan's unpopular 2008 film.\n\nPassages:\n\n[What Happens in Vegas]\nWhat Happens in Vegas is a 2008 American comedy film directed by Tom Vaughan, written by Dana Fox and starring Cameron Diaz and Ashton Kutcher.\n\n[Tom Vaughan (director)]\nHis work includes \"Cold Feet\" (1999) and \"He Knew He Was Right\" (2004) for television, and \"What Happens in Vegas\" (2008) and \"Extraordinary Measures\" (2010) for cinema.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa501e159f1",
  "kind": "yes/no",
  "text": "Post: wow i love only ever buying gray and striped shirts",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qfc63e9c4e5",
  "kind": "yes/no",
  "text": "Claim: Ronald Wayne \"Ron\" Shelton, not Ken Mora, has won an Oscar.\n\nPassages:\n\n[Ron Shelton]\nRonald Wayne \"Ron\" Shelton (born September 15, 1945) is an American Oscar-nominated film director and screenwriter and former minor league baseball infielder.\n\n[Ken Mora]\nKenneth Oscar \"Ken\" Mora (born December 17, 1960) is an American screenplay writer, director, producer, editor, and voice actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q025f94a3fe",
  "kind": "yes/no",
  "text": "Claim: The Irish folk band \"The Wolfe Tones,\" known for their album Sing Out for Ireland, are named after Theobald Wolfe Tone, the Irish statesman and patriot.\n\nPassages:\n\n[The Wolfe Tones]\nThey take their name from the Irish rebel and patriot Theobald Wolfe Tone, one of the leaders of the Irish Rebellion of 1798, with the \"double entendre\" of a wolf tone – a spurious sound that can affect instruments of the violin family.\n\n[Sing Out for Ireland]\nSing Out for Ireland is the fourteenth album by Irish folk and rebel band The Wolfe Tones.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3701da6849",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "ugh I have to send an email??? how about I just quit!!!!!",
   "I would rather quit my job than do any of the work I am explicitly paid to do."
  ]
 },
 {
  "qid": "qda922474b2",
  "kind": "yes/no",
  "text": "Claim: The host of the show that featured LA Urban Rangers provided the voice of Backson in the Disney Channel's 51st the Disney Channel animated feature film.\n\nPassages:\n\n[LA Urban Rangers]\nTheir most recent and longest-running outing - the Malibu Public Beach Safari - has been featured in media reports and by Huell Howser on his show.\n\n[Winnie the Pooh (2011 film)]\nIt is the 51st Disney animated feature film.\n\n[Huell Howser]\nHuell Burnley Howser (October 18, 1945 – January 7, 2013) was an American television personality, actor, producer, writer, singer, and voice artist, best known for hosting, producing, and writing \"California's Gold\", his human interest show produced by KCET in Los Angeles for California PBS stations. He also voiced the Backson in \"Winnie the Pooh\" (2011).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q209495dc46",
  "kind": "yes/no",
  "text": "Claim: The crossover hit that Mark Romanek directed the music video for, is a song by a American Industrial rock band. The band's music features in the film \"We\".\n\nPassages:\n\n[We (film)]\nThe film combines her speech \"Come September\" with a wide-variety of video footage and music (mostly electronica and industrial, including Curve, Nine Inch Nails, Love and Rockets, Placebo, Massive Attack, and Boards of Canada).\n\n[The Hand That Feeds]\nIt was also a crossover hit, crossing over to pop radio as their first top 40 radio hit since \"Closer\" and \"Hurt\" in 1994 and 1995, respectively, peaking at number 31 on the Billboard Hot 100 chart.\n\n[Mark Romanek]\nHis most notable music videos include \"Hurt\" (Johnny Cash), \"Closer\" (Nine Inch Nails), \"Can't Stop\" (Red Hot Chili Peppers), \"Bedtime Story\" (Madonna), and \"Scream\" (Michael & Janet Jackson).\n\n[Closer (Nine Inch Nails song)]\n\"Closer\" is a song by American industrial rock band Nine Inch Nails from their second studio album, \"The Downward Spiral\" (1994).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3066439f59",
  "kind": "yes/no",
  "text": "Claim: The flaming volcano drink is larger than the Apple-Kneel.\n\nPassages:\n\n[Apple-Kneel]\nIt consists of three shots, two Sourz Apple and one Cherry Brandy. Each shot is taken from an average shot glass which is around 1.5 ounces (roughly 45 ml).\n\n[Flaming volcano]\nThe flaming volcano is a large tropical group cocktail made of rum, brandy, pineapple juice, orange juice, almond syrup, and sometimes other ingredients. It is usually a multi-user drink, served to a group in a special, ritual vessel known as a volcano bowl, which is a decorative ceramic bowl (typically of about 32 USoz capacity) designed with a rising central hub feature usually resembling a crude volcano cone.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q495954e39c",
  "kind": "yes/no",
  "text": "Claim: The execution of Roger David Casement, the Irish Nationalist who made made efforts during World War I to gain German military aid for the 1916 Easter Rising that sought to gain Irish independence, took place in Casement's Fort.\n\nPassages:\n\n[Rahoneen]\nIt is notable as the location of an ancient Celtic ringfort; at one time this was known as McKenna's fort, but, after the capture and execution of Roger Casement for treason, sabotage and espionage against the Crown, it became known as Casement's Fort. \"Too weak to travel, he was discovered at McKenna's Fort where he had hidden after arranging delivery of German weapons as part of a plan of arming Irish rebels and creating a rising in 1916 against the British to achieve independence.\n\n[Roger Casement]\nDescribed as the \"father of twentieth-century human rights investigations\", he was honoured in 1905 for the Casement Report on the Congo and knighted in 1911 for his important investigations of human rights abuses in Peru.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe120f11e48",
  "kind": "yes/no",
  "text": "Claim: The winner of the 2013 AFL Goal of the Year won four Coleman Medals in the early 2000s.\n\nPassages:\n\n[2013 AFL Goal of the Year]\nAt the end of the home and away season, three finalists were selected for a final public vote, which was won by Lance Franklin for his long-range goal after hurdling over a teammate in the middle of the ground.\n\n[Lance Franklin]\nHe has won a total of seven All-Australian selections (three at full forward and four at centre half-forward) and four Coleman Medals throughout his career.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe39da1468a",
  "kind": "yes/no",
  "text": "Claim: The nationality of the writer of detective novel Right Now: A 12-Step Program for Defeating the Obama Agenda is American.\n\nPassages:\n\n[Michael Steele]\nMichael Stephen Steele (born October 19, 1958) is an American politician and MSNBC political analyst as of May 2011.\n\n[Right Now (book)]\nRight Now: A 12-Step Program for Defeating the Obama Agenda, written by Michael Steele, was released on January 4, 2010.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4ce2234e94",
  "kind": "yes/no",
  "text": "Claim: 3D Wayfinder is an indoor wayfinding software and service used to help visitors to navigate large public buildings such as institutions which award academic degrees.\n\nPassages:\n\n[University]\nA university (Latin: \"universitas\" , \"a whole\") is an institution of higher (or tertiary) education and research which awards academic degrees in various academic disciplines.\n\n[3D Wayfinder]\n3D Wayfinder is an indoor wayfinding software and service used to help visitors to navigate in large public buildings (shopping centers, airports, train stations, hospitals, universities etc.)",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q19a8c70e6d",
  "kind": "yes/no",
  "text": "Claim: Tommy Swerdlow co-wrote the majority of Cool Runnings a film produced by Jon Turteltaub.\n\nPassages:\n\n[Cool Runnings]\nCool Runnings is a 1993 American comedy sports film directed by Jon Turteltaub and starring Leon, Doug E. Doug, Rawle D. Lewis, Malik Yoba and John Candy.\n\n[Tommy Swerdlow]\nHe has appeared in such films as \"Howard the Duck\" (1986) and \"Spaceballs\" (1987) and co-wrote the screenplays of \"Cool Runnings\" (1993), \"Little Giants\" (1994) and \"Snow Dogs\" (2002).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7c3313b3be",
  "kind": "yes/no",
  "text": "Claim: Beatty Airport is a county-owned public-use airport located three nautical miles (6 km) southwest of the central business district of the unincorporated town of Beatty along the Amargosa River in Nye County, in the western U.S. state of Nevada.\n\nPassages:\n\n[Beatty Airport]\nBeatty Airport (IATA: BTY, ICAO: KBTY, FAA LID: BTY) is a county-owned public-use airport located three nautical miles (6 km) southwest of the central business district of Beatty, a town in Nye County, Nevada, United States.\n\n[Beatty, Nevada]\nBeatty (pronounced BAY-dee) is an unincorporated town along the Amargosa River in Nye County in the U.S. state of Nevada.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc986170865",
  "kind": "yes/no",
  "text": "Tweet: Frankie is so lucky to have some amazing people in his life. Those that haven’t bothered  are missing out!",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 }
]
