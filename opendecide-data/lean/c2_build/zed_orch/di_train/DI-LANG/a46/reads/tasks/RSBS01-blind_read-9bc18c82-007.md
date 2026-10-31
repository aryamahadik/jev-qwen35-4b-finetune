# A46 replay label-noise blind read RSBS01-blind_read-9bc18c82-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS01-blind_read-9bc18c82-007.json

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
  "qid": "qc2c57a0d7f",
  "kind": "yes/no",
  "text": "Claim: The father of Kathy Cronkite, of the steering committee, was an American broadcast journalist, best known as anchorman for the \"CBS Evening News\" .\n\nPassages:\n\n[Walter Cronkite]\nWalter Leland Cronkite Jr. (November 4, 1916 – July 17, 2009) was an American broadcast journalist, best known as anchorman for the \"CBS Evening News\" for 19 years (1962–1981).\n\n[Kathy Cronkite]\nShe is also a daughter of former CBS News anchorman Walter Cronkite.\n\n[Reporters Committee for Freedom of the Press]\nThe steering committee includes Wolf Blitzer, Tony Mauro, Andrea Mitchell, and Judy Woodruff; Walter Cronkite was an active member from 1973 until his death in 2009.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q59dcca1613",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "How bout you dont use a gazillion filters on your pictures",
   "You edit your pictures so much it doesn’t look like you"
  ]
 },
 {
  "qid": "qba9755677e",
  "kind": "yes/no",
  "text": "Claim: The American animated television series that has the episode \"Jared Has Aides\" was created by Trey Parker and Matt Stone. The series features a character called Butters who thinks up schemes to take over the world in its 86th episode.\n\nPassages:\n\n[Simpsons Already Did It]\n\"Simpsons Already Did It\" is the seventh episode of the sixth season of the American animated television series \"South Park\", and the 86th episode of the series overall. In the episode, which continues on from the events of the previous episode \"Professor Chaos\", Butters thinks up a series of schemes to take over the world, but realizes that each one has already been performed on \"The Simpsons\".\n\n[Jared Has Aides]\n\"Jared Has Aides\" is the first episode of the sixth season of the adult American animated television series \"South Park\".\n\n[South Park (season 6)]\nSeason six of \"South Park\", an American animated television series created by Trey Parker and Matt Stone, began airing on March 6, 2002.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7c94622a76",
  "kind": "yes/no",
  "text": "Claim: Trains run on the system which has a terminal station located at the intersection of 32nd Street and Sixth Avenue in the Herald Square neighborhood of Manhattan, New York City 24 hours a day and 7 days a week.\n\nPassages:\n\n[33rd Street station (PATH)]\nLocated at the intersection of 32nd Street and Sixth Avenue in the Herald Square neighborhood of Manhattan, New York City, it is served by the Hoboken–33rd Street and Journal Square–33rd Street lines on weekdays, and by the Journal Square–33rd Street (via Hoboken) line on weekends.\n\n[PATH (rail system)]\nPATH trains run 24 hours a day and 7 days a week.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qff1f272bd2",
  "kind": "yes/no",
  "text": "Post: Watching all these important venues closing over time sucks horribly, but this one hurts. Fuck. #FabricReview",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd84599315c",
  "kind": "yes/no",
  "text": "Claim: A gun range was first constructed for an event where 74 records were broken. Tughlaqabad Fort is close to this range.\n\nPassages:\n\n[1982 Asian Games]\nThe 9th Asian Games were held from November 19, 1982, to December 4, 1982, in Delhi, India. 74 Asian and Asian Games records were broken at the event.\n\n[Dr. Karni Singh Shooting Range]\nDr. Karni Singh Shooting Range is a shooting range in New Delhi. It was first constructed for the 1982 Asian Games in New Delhi, and later rebuild altogether for the 2010 Commonwealth Games.\n\n[Tughlaqabad Fort]\nAlso nearby is the Asola Bhatti Wildlife Sanctuary, Dr. Karni Singh Shooting Range and Okhla Industrial Area.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q86db3e36c3",
  "kind": "yes/no",
  "text": "Claim: The Los Angeles Dance Theater production company was founded by George Balanchine to create a live stage version of the 1942 film Casablanca.\n\nPassages:\n\n[Casablanca (film)]\nCasablanca is a 1942 American romantic drama film directed by Michael Curtiz and based on Murray Burnett and Joan Alison's unproduced stage play \"Everybody Comes to Rick's\".\n\n[Los Angeles Dance Theater]\nThe Los Angeles Dance Theater is a dance-oriented production company founded in 2003 by George Balanchine protege John Clifford.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q28fe34ed9b",
  "kind": "yes/no",
  "text": "Claim: The writer of Just Like Anyone (song) and Les McKeown, both share the profession of singer.\n\nPassages:\n\n[Les McKeown]\nLeslie Richard McKeown (born 12 November 1955) is a Scottish pop singer who was the lead singer of the Bay City Rollers during their most successful period.\n\n[Dave Pirner]\nDavid Anthony \"Dave\" Pirner (born April 16, 1964) is an American songwriter, singer, and producer best known as the lead vocalist and frontman for the alternative rock band Soul Asylum.\n\n[Just Like Anyone (song)]\nWritten by lead singer Dave Pirner and produced by the band with Butch Vig, the song was released as the album's second single.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q96bc020705",
  "kind": "yes/no",
  "text": "Claim: Ogier the Dane is not the name for the character known as Holger Danske, from medieval French chansons de geste.\n\nPassages:\n\n[Holger Danske (disambiguation)]\nHolger Danske, or Ogier the Dane, is a legendary character appearing in medieval chansons de geste.\n\n[Ogier the Dane]\nOgier the Dane (French: \"Ogier le Danois\" or archaically \"Ogier de Danemarche\", Danish: \"Holger Danske\") is a legendary character who first appears in an Old French \"chanson de geste\", in the cycle of poems \"Geste de Doon de Mayence\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9f62102334",
  "kind": "yes/no",
  "text": "Claim: The boy band, NSYNC, that was formed in Orlando, Florida in 1995 was featured on the soundtrack to the film \"Light It Up\".\n\nPassages:\n\n[NSYNC]\nNSYNC (sometimes stylized as *NSYNC or 'N Sync) was an American boy band formed in Orlando, Florida in 1995 and launched in Germany by BMG Ariola Munich.\n\n[Light It Up (soundtrack)]\nIt features songs from Master P featuring The No Limit All Stars, featuring, Ja Rule, *NSYNC, 112, DMX, Jon B., OutKast featuring Slimm Cutta-Calhoun and more.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd9dcd314f4",
  "kind": "yes/no",
  "text": "Claim: The Garrick Club is a gentlemen's club in the heart of London founded in May 1831, since its conception has catered to members such as English actor and theatre manager Sir Herbert Beerbohm Tree, that died on 2 July 1917.\n\nPassages:\n\n[Garrick Club]\nIt is one of the oldest, most highly esteemed and most exclusive members' clubs in the world and since its conception has catered to members such as Charles Kean, Henry Irving, Herbert Beerbohm Tree, Arthur Sullivan, Laurence Olivier and John Gielgud.\n\n[Herbert Beerbohm Tree]\nSir Herbert Beerbohm Tree (17 December 1852 – 2 July 1917) was an English actor and theatre manager.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qce8bd90a1e",
  "kind": "yes/no",
  "text": "Claim: The writer Norman Alfred William Lindsay enjoyed boxing, but the author of the book The Hundred Secret Senses did not.\n\nPassages:\n\n[The Hundred Secret Senses]\nThe Hundred Secret Senses is a bestselling 1995 novel by Chinese-American writer Amy Tan.\n\n[Norman Lindsay]\nNorman Alfred William Lindsay (22 February 1879 – 21 November 1969) was an Australian artist, etcher, sculptor, writer, editorial cartoonist, scale modeller, and an accomplished amateur boxer.\n\n[Amy Tan]\nAmy Tan (born February 19, 1952) is an American writer whose works explore mother-daughter relationships and the Chinese American experience.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q75c376d718",
  "kind": "yes/no",
  "text": "Claim: The actress whose friend Jim Brochu is known as the author of the unauthorized biography \"Lucy in the Afternoon\" worked closely withCharpes Lane.\n\nPassages:\n\n[Jim Brochu]\nA friend of Lucille Ball, he is known as the author of the unauthorized biography \"Lucy in the Afternoon\", and in this capacity, appeared on an episode of \"MythBusters\".\n\n[Lucille Ball]\nShe was best known as the star of the self-produced sitcoms \"I Love Lucy\", \"The Lucy–Desi Comedy Hour\", \"The Lucy Show\", \"Here's Lucy\", and \"Life with Lucy\".\n\n[Charles Lane (actor)]\nHe was a favored supporting actor of Lucille Ball, who often used him as a no-nonsense authority figure and comedic foe of her scatterbrained TV character on her TV series \"I Love Lucy\", \"The Lucy–Desi Comedy Hour\" and \"The Lucy Show\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q03ac123482",
  "kind": "yes/no",
  "text": "Post: hello i woke up last night to myself grouping psychoactive drugs out loud in my sleep-i’m so ready for finals to be over, wow!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd30e857b5a",
  "kind": "yes/no",
  "text": "Claim: Appointment in Tokyo is the painting that shows the surrender of the Empire of Japan on the last battleship built by the United States during World War II.\n\nPassages:\n\n[Appointment in Tokyo]\nAppointment in Tokyo is a 1945 documentary released Produced by the Army Pictorial Service, Signal Corps, with the cooperation of the Army Air Forces and the United States Navy, and released by Warner Bros. for the War Activities Committee shortly after the surrender of Japan. It mainly follows General Douglas MacArthur and his men from their exile from the Philippines in early 1942, through the signing of the instrument of surrender on the USS \"Missouri\" on September 1, 1945.\n\n[USS Missouri (BB-63)]\n\"Missouri\" was the last battleship commissioned by the United States and is best remembered as the site of the surrender of the Empire of Japan which ended World War II.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc05d455de7",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "turning 22 next week so naturally I increased my tinder age range up to 60",
   "I'm turning 22 next week and feel old already"
  ]
 },
 {
  "qid": "q75827e0e5b",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Our field shouldn't try to force human experience into quantifiable models, but it pretty consistently does.",
   "@avsmph But how can we possibly deal with a human experience we haven't first relentlessly quantified???"
  ]
 },
 {
  "qid": "q64db82add4",
  "kind": "yes/no",
  "text": "Claim: Bob Hoskins and Helen Mirren starred in the 1986 British gangster film in which this actor had one of his first roles. He later went on to star in Sharpe's Rifles (TV programme).\n\nPassages:\n\n[The Long Good Friday]\nThe Long Good Friday is a British gangster film starring Bob Hoskins and Helen Mirren.\n\n[Daragh O'Malley]\nO'Malley first appeared in roles in the iconic films \"The Long Good Friday\" and \"Withnail and I\", leading guest roles in many UK television series including \"Tales of The Unexpected (TV Series)\", \"Waking The Dead\", \"Wire in the Blood\", \"Silent Witness\" and \"Vera\", and roles in Longitude, Cleopatra for ABC and The Magnificent Seven for CBS and in the US TV films 'Vendetta\", \"Camelot\" (TV Series) and \"Shaughnessy\".\n\n[Sharpe's Rifles (TV programme)]\nShown on ITV in 1993, the adaptation stars Sean Bean, Daragh O'Malley and Assumpta Serna.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5d6bd412b5",
  "kind": "yes/no",
  "text": "Post: my bf took my off his lock screen which obvi means he’s cheating on me",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qc69983c9e4",
  "kind": "yes/no",
  "text": "Text: Thoroughly enjoyed my first TeachMeet! Would definitely recommend it. It's like a teacher version of #TEDTalks @TeachMeetLeics",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q619cd22e77",
  "kind": "yes/no",
  "text": "Text: Social Care for the young is basically a bath board and bed rest and your done.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qed3405ecb3",
  "kind": "yes/no",
  "text": "Claim: The architectural distinction of the hotel whose owner and chief developer is Frank Augustus Miller is the largest Mission Revival Style building in United States.\n\nPassages:\n\n[The Mission Inn Hotel &amp; Spa]\nThe Mission Inn, now known as The Mission Inn Hotel & Spa, is a historic landmark hotel in downtown Riverside, California. Although a composite of many architectural styles, it is generally considered the largest Mission Revival Style building in the United States.\n\n[Frank Augustus Miller]\nFrank Augustus Miller (June 30, 1858 – June 17, 1935) was the owner and chief developer of the Mission Inn in Riverside, California, United States, where Frank Augustus Miller Middle School was named after him.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q44bc566956",
  "kind": "yes/no",
  "text": "Text: #jackstack @TGIFridays 😍😍😍 https://t.co/J2Ycj5WbOe",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qde52febac9",
  "kind": "yes/no",
  "text": "Claim: Alfred Molina played Touchstone in the 2006 film of Shakespeare's As You Like It.\n\nPassages:\n\n[As You Like It (2006 film)]\nAs You Like It is a 2006 film written and directed by Kenneth Branagh, and based on the Shakespearean play of the same name. It stars Bryce Dallas Howard as Rosalind, David Oyelowo as Orlando De Boys, Romola Garai as Celia, Adrian Lester as Oliver De Boys, Alfred Molina as Touchstone, Kevin Kline as Jaques, Janet McTeer as Audrey, and Brian Blessed as Duke Frederick and his brother Duke Senior.\n\n[Touchstone (As You Like It)]\nTouchstone is a fictional character in Shakespeare's play \"As You Like It\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qfe91065aa6",
  "kind": "yes/no",
  "text": "Claim: Gloria S. Butler can find her constuancy in eastern directional sections of DeKalb County, Georgia.\n\nPassages:\n\n[Gloria S. Butler]\nGloria S. Butler (born December 25, 1941) is a Senate Democrat in the 152nd Georgia General Assembly from Stone Mountain, Georgia. Butler was first elected Senator in the 1998 general election and serves Georgia's 55th district—a constituency comprised in DeKalb county.\n\n[Stone Mountain, Georgia]\nStone Mountain is a city in DeKalb County, Georgia, United States. The population was 5,802 at the 2010 census. Stone Mountain is located in the eastern part of Dekalb County and is a suburb of Atlanta.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfbb7d01815",
  "kind": "yes/no",
  "text": "Claim: César Vallejo was not a Nazi national. Neither was the author of Tales of a Long Night.\n\nPassages:\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.\n\n[Tales of a Long Night]\nTales of a Long Night (German: \"Hamlet oder Die lange Nacht nimmt ein Ende\" ) (1956) is the last novel of German author Alfred Döblin.\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q59f82495fc",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I do not like when professors don’t write out specific notes on my answers to exams.",
   "I love it when professors draw a big question mark next to my answer on an exam because I’m always like yeah I don’t either ¯\\_(ツ)_/¯"
  ]
 },
 {
  "qid": "qa1b5664987",
  "kind": "yes/no",
  "text": "Tweet: Just been told I need to resit a piece of coursework, it's due on the 15th! And I go on holiday on the 10th! Fml!!!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q43044095a1",
  "kind": "yes/no",
  "text": "Claim: Amsterdam Airport Schiphol is the main base of the airline co-founded by John Nicolaas Block.\n\nPassages:\n\n[Transavia]\nIts main base is Amsterdam Airport Schiphol and has further bases at Rotterdam The Hague Airport, Munich Airport and Eindhoven Airport.\n\n[John Nicolaas Block]\nHe was the co-founder of Martinair, founder of Transavia and Air Holland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3b54866720",
  "kind": "yes/no",
  "text": "Claim: The 2017 ESPN College Football Friday Primetime host who never played at Oklahoma in college played for NFL team the Bears.\n\nPassages:\n\n[ESPN College Football Friday Primetime]\nIn 2017, the games will be announced by Adam Amin and Dusty Dvoracek.\n\n[Dusty Dvoracek]\nDrafted by the Chicago Bears of the National Football League in the third round of the 2006 NFL Draft, he played college football at Oklahoma and professionally with the Bears from 2006 to 2009 and the Omaha Nighthawks of the United Football League in 2010–11.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qda1d4e7de8",
  "kind": "yes/no",
  "text": "Claim: The mother of Megan Phelps-Roper is best known as the former spokesperson of a church located in Port Republic.\n\nPassages:\n\n[Megan Phelps-Roper]\nHer mother is Shirley Phelps-Roper, whose father was the church's founder Fred Phelps.\n\n[Shirley Phelps-Roper]\nShe is best known as the former spokesperson of the Westboro Baptist Church of Topeka, Kansas, an organization known for its highly publicized homophobic public protests conducted under the slogan \"God Hates Fags.\"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6d15b91a1c",
  "kind": "yes/no",
  "text": "Tweet: Whoever’s toddler ass sprayed the entire toilet backstage, I hope you stub your toe and bite your tongue really hard. also you were clearly dehydrated, go drink some damn water like an adult",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q2d1f78378e",
  "kind": "yes/no",
  "text": "Claim: Saki was British. The author of Green, Green My Valley Now was also British.\n\nPassages:\n\n[Richard Llewellyn]\nRichard Dafydd Vivian Llewellyn Lloyd (8 December 1906 – 30 November 1983), known by his pen name Richard Llewellyn, was a British novelist.\n\n[Saki]\nHector Hugh Munro (18 December 1870 – 14 November 1916), better known by the pen name Saki, and also frequently as H. H. Munro, was a British writer whose witty, mischievous and sometimes macabre stories satirize Edwardian society and culture.\n\n[Green, Green My Valley Now]\nGreen, Green My Valley Now is a 1975 novel by Richard Llewellyn.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q12ed9877ba",
  "kind": "yes/no",
  "text": "Claim: The movie whose prequel is the novel \"Jumper: Griffin's Story\" made $27.3 million in its opening weekend.\n\nPassages:\n\n[Jumper (2008 film)]\nThe film held the first position in its opening weekend with $27.3 million, but received generally unfavourable reviews from critics, mostly due to the many changes from Gould's novel, rushed plot and anti-climactic ending.\n\n[Jumper: Griffin's Story (novel)]\nJumper: Griffin's Story is a novel by Steven Gould released August 21, 2007, as a prequel to the movie \"Jumper\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb29d0bc56f",
  "kind": "yes/no",
  "text": "Claim: Richard Ney wrote the music and lyrics to Portofino with a collaborator on \"Fiddler on the Roof\".\n\nPassages:\n\n[Portofino (musical)]\nPortofino is a musical with a book by Richard Ney, lyrics by Ney and Sheldon Harnick, and music by Louis Bellson and Will Irwin.\n\n[Sheldon Harnick]\nSheldon Harnick (born April 30, 1924) is an American lyricist best known for his collaborations with composer Jerry Bock on musicals such as \"Fiddler on the Roof\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc0233640a0",
  "kind": "yes/no",
  "text": "Claim: The winner of the 2016 Marrakesh ePrix was born in the year 1988.\n\nPassages:\n\n[2016 Marrakesh ePrix]\nThe 33-lap race was won by e.Dams-Renault driver Sébastien Buemi, who started from the seventh position.\n\n[Sébastien Buemi]\nSébastien Olivier Buemi (born 31 October 1988) is a Swiss professional racing driver, who formerly competed for Scuderia Toro Rosso in Formula One.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q306bf6730f",
  "kind": "yes/no",
  "text": "Claim: Boston Advantage, along with the Boston Junior Rangers, East Coast Wizards, New Hampshire Avalanche, American and one other are American youth ice hockey teams. As of the 2010 census, the city that other team plays in had a population of 60,879.\n\nPassages:\n\n[Haverhill, Massachusetts]\nHaverhill ( ) is a city in Essex County, Massachusetts, United States. The population was 60,879 at the 2010 census.\n\n[Boston Advantage]\nIt is also a charter franchise, along with the Boston Junior Rangers, East Coast Wizards, New Hampshire Avalanche, Seacoast Spartans and Valley Jr. Warriors.\n\n[Valley Jr. Warriors]\nThe Valley Jr.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4925873a3a",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "i stg i probably talk to my tv more than i do to actual people whoops rip social life",
   "I talk to more people than i do anything"
  ]
 },
 {
  "qid": "q2e76ab0f21",
  "kind": "yes/no",
  "text": "Tweet: WTF!!! #billcosby conviction was just overturned by the Pennsylvania Supreme Court!!!! #wtf #WHY #me2 @BillCosby",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qfe2cd332f6",
  "kind": "yes/no",
  "text": "Claim: The younger brother of Harvey Jewell served as the national chairman for the American Republican Party.\n\nPassages:\n\n[Harvey Jewell]\nHis younger brother, Marshall Jewell (1825-1883) would later be elected Governor of Connecticut and would serve as President Grant's United States Postmaster General.\n\n[Marshall Jewell]\nMarshall Jewell (October 20, 1825February 10, 1883) was a manufacturer, pioneer telegrapher, telephone entrepreneur, world traveler, and political figure who served as 44th and 46th Governor of Connecticut, the U.S. Minister to Russia, the 25th United States Postmaster General, and Republican Party National Chairman.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6bccc7889f",
  "kind": "yes/no",
  "text": "Post: im glad we finally have a party in opposition who are committed to taking the government to task for not making mistakes fast enough",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qf8523dc1bc",
  "kind": "yes/no",
  "text": "Claim: Dana Fox wrote Tom Vaughan's unpopular 2008 film.\n\nPassages:\n\n[What Happens in Vegas]\nWhat Happens in Vegas is a 2008 American comedy film directed by Tom Vaughan, written by Dana Fox and starring Cameron Diaz and Ashton Kutcher.\n\n[Tom Vaughan (director)]\nHis work includes \"Cold Feet\" (1999) and \"He Knew He Was Right\" (2004) for television, and \"What Happens in Vegas\" (2008) and \"Extraordinary Measures\" (2010) for cinema.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb5059ea43a",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "i love how i literally just finished watching the fifth hp film and then turned to my mum and said \"this bit of character death on a sunday has made me sad\" the dsmp lore has utterly ruined my attachment to characters and how i see stories now. i am a broken woman.",
   "i love how i literally just finished watching the fifth hp film and then turned to my mum and said \"love a good bit of character death on a sunday :)\" the dsmp lore has utterly ruined my attachment to characters and how i see stories now. i am a broken woman."
  ]
 },
 {
  "qid": "q571140e1bf",
  "kind": "yes/no",
  "text": "Text: @32watto Neighbours",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q6bc95790c2",
  "kind": "yes/no",
  "text": "Claim: This 55-year old company operates flights to Lufthansa destinations, on behalf of Lufthansa. Its headquarters are 4 km from the city center.\n\nPassages:\n\n[Lufthansa destinations]\nFlights operated on behalf of Lufthansa by PrivatAir are also listed.\n\n[PrivatAir]\nPrivatAir is a Swiss airline operating business jets, headquartered at Geneva Airport in Meyrin.\n\n[Geneva Airport]\nIt is located 4 km northwest of the city centre.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe8f235a66d",
  "kind": "yes/no",
  "text": "Claim: Dominic Purcell is the creator of the animated television series whose fourteenth episode of season three's title is \"Time Keeps on Slippin\".\n\nPassages:\n\n[Futurama]\nFuturama is an American animated science fiction comedy series created by Matt Groening for the Fox Broadcasting Company.\n\n[Time Keeps On Slippin']\n\"Time Keeps On Slippin\" is the fourteenth episode in season three of the animated television series \"Futurama\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q903cb4168a",
  "kind": "yes/no",
  "text": "Post: Horse dancing is my new favorite Olympic sport, I have no clue what’s happening, but this is incredible",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q7d776bb012",
  "kind": "yes/no",
  "text": "Claim: The musician that wrote Raymonda served as director of the Bill Sawyer Orchestra when he started composing Symphony No 9 in D minor.\n\nPassages:\n\n[Raymonda]\nRaymonda (Russian: Раймонда ) is a ballet in three acts, four scenes with an apotheosis, choreographed by Marius Petipa, with music by Alexander Glazunov, his opus 57.\n\n[Alexander Glazunov]\nHe served as director of the Saint Petersburg Conservatory between 1905 and 1928 and was instrumental in the reorganization of the institute into the Petrograd Conservatory, then the Leningrad Conservatory, following the Bolshevik Revolution.\n\n[Symphony No. 9 (Glazunov)]\nAlexander Glazunov's Symphony No. 9 in D minor was begun in 1910, but was still unfinished by the time of his death in 1936.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q18fb1c6bb9",
  "kind": "yes/no",
  "text": "Claim: This woman directed a film. Lola Créton starred in this film. She won Rough Cut for a film staring Isabelle Huppert.\n\nPassages:\n\n[Mia Hansen-Løve]\nIn 2016, she won the Silver Bear for Best Director for her film \"Things to Come\" at the 66th Berlin International Film Festival.\n\n[Goodbye First Love]\nGoodbye First Love (French: Un amour de jeunesse ) is a 2011 Franco-German film directed by Mia Hansen-Løve.\n\n[Things to Come (2016 film)]\nIt stars Isabelle Huppert as middle-aged philosophy professor Nathalie Chazeaux, whose life is going through a series of separations.\n\n[Lola Créton]\nShe is known for her lead roles in the films \"Goodbye First Love\" (2011) and \"Something in the Air\" (2012).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0373ac2893",
  "kind": "yes/no",
  "text": "Claim: A gothic-style building is located on the area that is home to the Luxor Obelisk in Paris. This building hosted the 7th Lumières Awards.\n\nPassages:\n\n[7th Lumières Awards]\nThe winners were announced at a press conference at the Hôtel de Crillon in Paris. \"\n\n[Hôtel de Crillon]\nLocated at the foot of the Champs-Élysées, the Crillon along with the Hotel de la Marine is one of two identical stone palaces on the Place de la Concorde.\n\n[Place de la Concorde]\nThe Place de la Concorde (] ) is one of the major public squares in Paris, France.\n\n[Luxor Obelisk]\nThe Luxor Obelisk (French: \"Obélisque de Louxor\") is a 23 m high Egyptian obelisk standing at the center of the Place de la Concorde in Paris, France.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
