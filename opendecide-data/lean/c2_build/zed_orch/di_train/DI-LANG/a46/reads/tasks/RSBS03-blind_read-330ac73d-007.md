# A46 replay label-noise blind read RSBS03-blind_read-330ac73d-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS03-blind_read-330ac73d-007.json

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
  "qid": "qb01d49c3ae",
  "kind": "yes/no",
  "text": "Claim: Democracy Day is a possible federal holiday proposed by a republican politician that represents the 13th US congressional district.\n\nPassages:\n\n[Democracy Day (United States)]\nDemocracy Day is the tentative name of a possible federal holiday in the United States, proposed by Democratic Representative John Conyers of Michigan.\n\n[John Conyers]\nJohn James Conyers Jr. (born May 16, 1929) is an American Democratic politician and the U.S. Representative for 's 13th congressional district .",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6e0011c2c1",
  "kind": "yes/no",
  "text": "Claim: Rainer Dart is an Irish crime author. So is the writer of The Celestial Plot.\n\nPassages:\n\n[The Celestial Plot]\nThe Celestial Plot (Spanish: \"La trama celeste\" ) is a book by Adolfo Bioy Casares.\n\n[Adolfo Bioy Casares]\nAdolfo Bioy Casares (] ; September 15, 1914 – March 8, 1999) was an Argentine fiction writer, journalist, and translator.\n\n[Iris Rainer Dart]\nIris Rainer Dart (born March 3, 1944) is an American author and playwright for television and the stage.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa64987e646",
  "kind": "yes/no",
  "text": "Claim: A song by David Guetta was produced by the Dutch David Guetta. The signer who recorded I Don't Wanna Grow Up guested on this song.\n\nPassages:\n\n[I Don't Wanna Grow Up]\nI Don't Wanna Grow Up is the debut extended play (EP) by American pop recording artist Bebe Rexha.\n\n[Bebe Rexha]\nShe is best known as a featured guest vocalist on several \"Billboard\" Hot 100 charting songs, such as G-Eazy's \"Me, Myself & I\", David Guetta's \"Hey Mama\", Martin Garrix's \"In the Name of Love\" and Cash Cash's \"Take Me Home\".\n\n[Hey Mama (David Guetta song)]\n\"Hey Mama\" is a song by French DJ and record producer David Guetta, featuring vocals from Nicki Minaj and Bebe Rexha, as well as production from Dutch DJ and producer Afrojack.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4603e466aa",
  "kind": "yes/no",
  "text": "Claim: Keith Scholey co-directed \"African Cats\" and another documentary with the executive producer of \"Frozen Planet\" for Disneynature. That documentary and Aliens of the Deep were not filmed in the same locations.\n\nPassages:\n\n[Aliens of the Deep]\nIt was produced by Walden Media and Walt Disney Pictures.\n\n[Frozen Planet]\nThe production team, which includes executive producer Alastair Fothergill and series producer Vanessa Berlowitz, were previously responsible for the award-winning series \"The Blue Planet\" (2001) and \"Planet Earth\" (2006), and \"Frozen Planet\" is billed as a sequel of sorts.\n\n[Keith Scholey]\nHe co-directed \"African Cats\" and \"Bears\" with Alastair Fothergill for Disneynature.\n\n[Bears (film)]\nBears is a 2014 nature documentary film about a family of brown bears living in the coastal mountain ranges of Alaska.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q1f3580eb92",
  "kind": "yes/no",
  "text": "Claim: The writer of the song Not Now John and Tom Johnston are both musicians.\n\nPassages:\n\n[Tom Johnston (musician)]\nCharles Thomas \"Tom\" Johnston (born August 15, 1948) is an American musician.\n\n[Not Now John]\n\"Not Now John\" is a song by the progressive rock band Pink Floyd, written by Roger Waters.\n\n[Roger Waters]\nGeorge Roger Waters (born 6 September 1943) is an English singer, songwriter, bassist, and composer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb4c4db9a1d",
  "kind": "yes/no",
  "text": "Claim: The serial killer who buried his victims in the state pine forest owned by the New South Wales Government is called Ivan Milat.\n\nPassages:\n\n[Backpacker murders]\nThe backpacker murders were a spate of serial killings that took place in New South Wales, Australia, between 1989 and 1993, committed by Ivan Milat. The bodies of seven missing young people aged 19 to 22 were discovered partially buried in the Belanglo State Forest, 15 km south west of the New South Wales town of Berrima.\n\n[Belanglo State Forest]\nThe forest is owned by the New South Wales Government and contains some of the earliest pine plantings in the state.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8f16207470",
  "kind": "yes/no",
  "text": "Text: Using my recently acquired video editing skills on myself for a change. An oral #presentation assignment on #healtheconomics is as much fun as it sounds 🗣🎥 https://t.co/1LKHVyupie",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5a5849f76a",
  "kind": "yes/no",
  "text": "Claim: The actress starred in the film Over the Hill in 1992. Norman Jewison directed the movie that she won Sinatra for.\n\nPassages:\n\n[Olympia Dukakis]\nShe later transitioned to film acting and in 1987 she won an Academy Award, a Golden Globe, and a BAFTA nomination for her performance in \"Moonstruck\".\n\n[Moonstruck]\nMoonstruck is a 1987 American romantic comedy film directed by Norman Jewison and written by John Patrick Shanley.\n\n[Over the Hill]\nOver the Hill is a 1992 Australian drama film directed by George T. Miller and starring Olympia Dukakis and Sigrid Thornton.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd9b3ae839d",
  "kind": "yes/no",
  "text": "Claim: The Israeli local protests took place after the resignation of the seventh president of Israel in 2000.\n\nPassages:\n\n[Israeli presidential election, 2000]\nElections for the President of Israel were held in the Knesset on 31 July 2000, following Ezer Weizman's resignation.\n\n[Ezer Weizman]\nEzer Weizman (Hebrew: עזר ויצמן‎ ‎ \"Ezer Vaytsman\"; 15 June 1924 – 24 April 2005) was the seventh President of Israel, first elected in 1993 and re-elected in 1998.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbba80fccce",
  "kind": "yes/no",
  "text": "Claim: International Association of Athletics Federations is the company that currently recognizes the sprinting records set by Leni Junker and Florence Griffith-Joyner.\n\nPassages:\n\n[Leni Junker]\nEarlier in 1925 she set a world record in the 110 yards at 12.2 seconds.\n\n[Women's 100 metres world record progression]\nThe FSFI was absorbed by the International Association of Athletics Federations (IAAF) in 1936.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0aad82d48c",
  "kind": "yes/no",
  "text": "Claim: Johann Duhaupas held notable knockout victories against the Lebanese-born Syrian-German professional boxer.\n\nPassages:\n\n[Manuel Charr]\nManuel Charr (born Mahmoud Omeirat Charr; 10 October 1984) is a Lebanese-born Syrian-German professional boxer who has challenged once for the WBC heavyweight title.\n\n[Johann Duhaupas]\nJohann Duhaupas (born 5 February 1981) is a French professional boxer and world heavyweight title challenger. He holds notable victories over Manuel Charr and Robert Helenius.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4b8430dd21",
  "kind": "yes/no",
  "text": "Text: I just got my first spam call about my vehicle’s extended warranty!!! I’m living in a meme",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q570f995fb8",
  "kind": "yes/no",
  "text": "Claim: The actor who played Nathan Appleby in The Living and the Dead was born in 1986.\n\nPassages:\n\n[Colin Morgan]\nColin Morgan (born 1 January, 1986) is a British/Irish film, television, theatre and radio actor best known for playing the title character in the BBC fantasy series \"Merlin\", the lead in \"The Living and the Dead\", and main roles in \"Humans\" and \"The Fall\"; his stage role as Ariel in \"The Tempest\"; and film roles in \"Testament of Youth\", \"Legend\" and \"\".\n\n[The Living and the Dead (TV series)]\nThe plot revolves around Nathan Appleby (played by Colin Morgan) and his wife, Charlotte Appleby (played by Charlotte Spencer), whose farm is believed to be at the centre of numerous supernatural occurrences.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8de454a7e6",
  "kind": "yes/no",
  "text": "Claim: The man who coached The 1973 Indiana Hoosiers football team was born in May of 1935.\n\nPassages:\n\n[Lee Corso]\nLee Corso (born August 7, 1935) is an American sports broadcaster and football analyst for ESPN and former coach.\n\n[1973 Indiana Hoosiers football team]\nThe 1973 Indiana Hoosiers football team represented the Indiana Hoosiers in the 1973 Big Ten Conference football season. The team was coached by Lee Corso, in his first year as head coach of the Hoosiers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qeacd6181ee",
  "kind": "yes/no",
  "text": "Claim: This athlete won the 2004 BNP Paribas Masters – Singles title for the then record 3rd time. Both she and the 2008 Kremlin Cup – Women's Singles semi-finals winner have both played tennis professionally.\n\nPassages:\n\n[2008 Kremlin Cup – Women's Singles]\nElena Dementieva was the defending champion, but lost in the semifinals to Jelena Janković.\n\n[Jelena Janković]\nJelena Janković (Serbian Cyrillic: Јелена Јанковић, ] , born 28 February 1985) is a Serbian professional tennis player.\n\n[Marat Safin]\nMarat Mubinovich Safin (Russian: Мара́т Муби́нович Са́фин ; ] , Tatar: Марат Мөбин улы Сафин \"Marat Möbin uğlı Safin\" ; born 27 January 1980) is a Russian politician and retired professional tennis player.\n\n[2004 BNP Paribas Masters – Singles]\nMarat Safin won the title for the then record 3rd time, defeating Radek Štěpánek in the final in straight sets.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q824e483f96",
  "kind": "yes/no",
  "text": "Claim: The conference that the team, which Shannon Doyle accumulated 25 points from 2010–12, play in used to be affiliated with the Eastern College Athletic Conference.\n\nPassages:\n\n[Shannon Doyle]\nAt the NCAA level, she accumulated 25 points with the Colgate Raiders women's ice hockey from 2010–12, and 53 points with the Boston University Terriers women's ice hockey program over the course of two seasons from 2012-15 (she missed the 2013-14 season due to injury).\n\n[ECAC Hockey]\nThe conference used to be affiliated with the Eastern College Athletic Conference, a consortium of over 300 colleges in the eastern United States.\n\n[Colgate Raiders women's ice hockey]\nThe Colgate Raiders women's ice hockey team is an NCAA Division I ice hockey team that represents Colgate University and play in ECAC Hockey.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9c1fe0276a",
  "kind": "yes/no",
  "text": "Claim: The founding year of this American for-profit college, which helps to operate a 2 year, dual degree high school located in downtown Chicago, Illinois, with Chicago Public Schools was 1931.\n\nPassages:\n\n[DeVry University]\nDeVry University ( ) is an American for-profit college. The school was founded in 1931 as DeForest Training School, and officially became DeVry University in 2002.\n\n[DeVry Advantage Academy (Illinois)]\nDeVry University Advantage Academy is a 2-year, dual degree high school located in Chicago, Illinois. Operated by partnership with Chicago Public Schools and DeVry University, the program offers students an opportunity to graduate with a high school diploma and an associate degree in either Networking System Administration or Web Graphic Design.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf897a50c04",
  "kind": "yes/no",
  "text": "Claim: The three best sellers from the author of Detective (novel) that were released before Donna Tartt was born in 1980 are \"Hotel\" (1965), \"Airport\" (1968), \"Wheels\" (1971).\n\nPassages:\n\n[Detective (novel)]\nDetective is a novel by Arthur Hailey.\n\n[Donna Tartt]\nDonna Tartt (born December 23, 1963) is an American writer, the author of the novels \"The Secret History\" (1992), \"The Little Friend\" (2002), and \"The Goldfinch\" (2013).\n\n[Arthur Hailey]\nHis meticulously-researched books, which include such best sellers as \"Hotel\" (1965), \"Airport\" (1968), \"Wheels\" (1971), \"The Moneychangers\" (1975), and \"Overload\" (1979), have sold 170 million copies in 38 languages.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0c36015c1f",
  "kind": "yes/no",
  "text": "Post: wow i love only ever buying gray and striped shirts",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q2a27db8f3d",
  "kind": "yes/no",
  "text": "Post: What kind of sins have y’all been committing for God to punish us with this kinda weather...",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf27e307557",
  "kind": "yes/no",
  "text": "Claim: Driven To Perform has a sponsor that includes the electronics store chain from Andover.\n\nPassages:\n\n[Driven To Perform]\nDriven To Perform (DTP) is an auto show billed as Western Canada's largest and most established automotive lifestyles tour and originally featured mainly import tuner sport compact cars. The inaugural show was held in Vancouver, BC in 2002 as Import Showoff Canada, but has since changed its name and expanded to include other vehicle types and into the other large metropolitan cities in this region of Canada. Major sponsors include Toyo Tires, Future Shop, Mobil1, Honda, Mazda, Lordco and Visions Electronics.\n\n[Future Shop]\nFuture Shop was a Canadian electronics store chain. In January 2013, the company operated 139 locations across Canada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf042d5a902",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Ratings should not matter.",
   "@SuspendThePres But what were the ratings?? (Replied to his Tweet with the same thing.)"
  ]
 },
 {
  "qid": "q628547fc97",
  "kind": "yes/no",
  "text": "Claim: Tariq Khan had his debut in a film that also starred an actor who lost four National Film Awards and eight Filmfare Awards, as well as an Academy Award nomination.\n\nPassages:\n\n[Aamir Khan]\nAamir Khan (] ; born Mohammed Aamir Hussain Khan on 14 March 1965) is an Indian film actor, director, and producer. He is the recipient of numerous awards, including four National Film Awards and eight Filmfare Awards, as well as an Academy Award nomination.\n\n[Yaadon Ki Baaraat]\nYaadon Ki Baaraat (English: \"Procession of Memories\") is a 1973 Indian Hindi film, directed by Nasir Hussain and written by Salim-Javed (Salim Khan and Javed Akhtar). It starred Dharmendra, Zeenat Aman, Ajit Khan, Vijay Arora, Tariq Khan, Neetu Singh and Aamir Khan. It was also the debut film for Tariq Khan (Nasir Hussain's nephew), as well as Aamir Khan (Tahir Hussain's, brother of Nasir Hussain, son), a child actor in this film and later one of India's biggest movie stars as an adult.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3e35871100",
  "kind": "yes/no",
  "text": "Claim: The event Mekdes Bekele Tadese specializes in is at the Asian Junior Athletics Championships.\n\nPassages:\n\n[2001 Asian Junior Athletics Championships]\nThe 2001 Asian Junior Athletics Championships was the ninth edition of the international athletics competition for Asian under-20 athletes, organised by the Asian Athletics Association. A total of 43 events were contested, which were divided equally between male and female athletes aside from the men's 3000 metres steeplechase.\n\n[Mekdes Bekele]\nMekdes Bekele Tadese (Amharic: መቅደስ በቀለ ታደሰ; born 20 January 1987) is an Ethiopian runner who specializes in the 3000 metres steeplechase.\n\n[3000 metres steeplechase]\nThe 3000 metres steeplechase or 3000-meter steeplechase is the most common distance for the steeplechase in track and field. It is an obstacle race over the distance of the 3000 metres, which derives its name from the horse racing steeplechase.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q98cbca1708",
  "kind": "yes/no",
  "text": "Claim: The two-seater car that competed in the Australian Nations Cup Championship was replaced by the sports car that debuted at the event 2004 Paris Motor Show.\n\nPassages:\n\n[Australian Nations Cup Championship]\nFor 2000, PROCAR split the Australian GT Production Car Championship into two separate series so that the more exotic GT cars such as Porsche 911s, Ferrari 360s and Lamborghini Diablo's could compete in the new Australian Nations Cup Championship and the lesser vehicles such as the Mitsubishi Lancers, Subaru Imprezas and HSV's could now compete for outright wins in the revised Australian GT Production Car Championship.\n\n[Ferrari 360]\nIt succeeded the Ferrari F355 and was replaced by the Ferrari F430.\n\n[Ferrari F430]\nA successor to the Ferrari 360, it debuted at the 2004 Paris Motor Show.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8e6c990fdf",
  "kind": "yes/no",
  "text": "Claim: A Very Harold & Kumar 3D Christmas is part of the \"Harold & Kumar\" series of comedies.\n\nPassages:\n\n[David Krumholtz]\nHe played Seth Goldstein in \"Harold & Kumar Go to White Castle\" and its two sequels, \"Harold & Kumar Escape from Guantanamo Bay\" and \"A Very Harold & Kumar 3D Christmas\".\n\n[Harold &amp; Kumar Go to White Castle]\nHarold & Kumar Go to White Castle (alternatively known as Harold & Kumar Get the Munchies) is a 2004 American stoner comedy film and the first installment of the \"Harold & Kumar\" series.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7e69e258dc",
  "kind": "yes/no",
  "text": "Claim: The closest relative to the whale is located in New Zealand.\n\nPassages:\n\n[Hippopotamus]\nThe common hippopotamus (\"Hippopotamus amphibius\"), or hippo, is a large, mostly herbivorous and aggressive mammal in sub-Saharan Africa, and one of only two extant species in the family Hippopotamidae, the other being the pygmy hippopotamus (\"Choeropsis liberiensis\" or \"Hexaprotodon liberiensis\").\n\n[Whale]\nThey are an informal grouping within the infraorder Cetacea, usually excluding dolphins and porpoises. Whales, dolphins and porpoises belong to the order Cetartiodactyla with even-toed ungulates and their closest living relatives are the hippopotamuses, having diverged about 40 million years ago.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q72025813c1",
  "kind": "yes/no",
  "text": "Claim: The grandmother to the famous poet from Joplin Missouri was Marry Patterson, she was born in 1747.\n\nPassages:\n\n[Langston Hughes]\nJames Mercer Langston Hughes (February 1, 1902 – May 22, 1967) was an American poet, social activist, novelist, playwright, and columnist from Joplin, Missouri.\n\n[Lewis Sheridan Leary]\nLewis Sheridan Leary (March 17, 1835 – October 20, 1859), an African-American harnessmaker from Oberlin, Ohio, joined John Brown's unsuccessful raid on Harpers Ferry, where he was killed. He was the first husband of Mary Patterson. By her second marriage to Charles Henry Langston, she became the future maternal grandmother of poet Langston Hughes.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf9937d4dbe",
  "kind": "yes/no",
  "text": "Claim: The Eek! segment Klutter was created by David Silverman and a man that manages Savage Studios Ltd.\n\nPassages:\n\n[Klutter!]\nIt was created by David Silverman and Savage Steve Holland.\n\n[Savage Steve Holland]\nNow, he manages his own studio, Savage Studios Ltd. and directs shows for Disney Channel and Nickelodeon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qbc4916219e",
  "kind": "yes/no",
  "text": "Claim: The author of Bambi's Children: The Story of a Forest Family, originally titled his work Bambi: Eine Lebensgeschichte aus dem Walde.\n\nPassages:\n\n[Felix Salten]\nFelix Salten (6 September 1869 – 8 October 1945) was an Austrian author and critic in Vienna.\n\n[Bambi, a Life in the Woods]\nBambi, a Life in the Woods, originally published in Austria as Bambi: Eine Lebensgeschichte aus dem Walde is a 1923 Austrian novel written by Felix Salten and published by Ullstein Verlag.\n\n[Bambi's Children]\nBambi's Children: The Story of a Forest Family (German: Bambis Kinder: Eine Familie im Walde ) is a novel written by Austrian author Felix Salten as a sequel to his successful work \"Bambi, A Life in the Woods\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc12e37f7d7",
  "kind": "yes/no",
  "text": "Claim: Marcus Jackson played college football for Texas Christian University in the 1990s.\n\nPassages:\n\n[TCU Horned Frogs football]\nThe TCU Horned Frogs football team is the intercollegiate football team of Texas Christian University (TCU).\n\n[Marcus Jackson]\nJackson played college football for the TCU Horned Frogs football team.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb3003ef1f2",
  "kind": "yes/no",
  "text": "Claim: Twisted Colossus was a ballad featured in the 1983 American road comedy National Lampoon's Vacation.\n\nPassages:\n\n[Twisted Colossus]\nColossus became well known after appearances in film and television, including the box-office hit \"National Lampoon's Vacation\".\n\n[National Lampoon's Vacation]\nNational Lampoon's Vacation, sometimes referred to as Vacation, is a 1983 American road comedy film directed by Harold Ramis and starring Chevy Chase, Beverly D'Angelo, Randy Quaid, Dana Barron, and Anthony Michael Hall.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q19cca54ff3",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "my favorite thing about my grandparents is that they're so afraid to talk about me being gay that our catch up phone calls are incredibly short 💘",
   "I would say \"It's quite upsetting that phone calls with my grandparents are so brief because they avoid topics pertaining to my partner and personal life\""
  ]
 },
 {
  "qid": "q708c88cc4f",
  "kind": "yes/no",
  "text": "Claim: The British monarch (Elizabeth II) is the head of state of the territory where Keightley Way connects Plaza Kotaraya at Little Bay to the place worship for Muslims and Nun's Well at Europa Point.\n\nPassages:\n\n[Keightley Way]\nIt connects Rosia Road at Little Bay to the Ibrahim-al-Ibrahim Mosque and Nun's Well at Europa Point.\n\n[Ibrahim-al-Ibrahim Mosque]\nThe Ibrahim-al-Ibrahim Mosque, also known as the King Fahd bin Abdulaziz al-Saud Mosque or the Mosque of the Custodian of the Two Holy Mosques, is a mosque located at Europa Point in the British overseas territory of Gibraltar, a peninsula connected to southern Spain.\n\n[British Overseas Territories]\nThey share the British monarch (Elizabeth II) as head of state.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbdd37d2203",
  "kind": "yes/no",
  "text": "Claim: John Constantine is the fictional antihero from comic books published by DC Comics, who sometimes acts as a cab driver, and was created by Don Simpson, Steve Bissette, and John Totleben.\n\nPassages:\n\n[Chas Chandler (comics)]\nChas is John Constantine's closest and longest surviving friend, who acts as his sidekick and cab driver.\n\n[John Constantine]\nJohn Constantine ( ) is a fictional antihero, appearing in comic books published by DC Comics and its alternative imprint Vertigo. 2 No. 25 (June 1984), and was created by Alan Moore, Steve Bissette and John Totleben.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1acc38fa86",
  "kind": "yes/no",
  "text": "Claim: Hermann Neubacher held a diplomatic passport as an Austrian Nazi politician in the Albanian Kingdom, when it was under the control of the Kingdom of Italy.\n\nPassages:\n\n[Albanian Kingdom (1943–44)]\nThe Albanian Kingdom (Albanian: \"Mbretëria Shqiptare\", German: \"Königreich Albanien\") existed as a \"de jure\" independent country, between 1943 and 1944. Before the armistice between Italy and the Allied armed forces on 8 September 1943, Albania had been in a de jure personal union with and was de facto under the control of the Kingdom of Italy.\n\n[Hermann Neubacher]\nDuring the Second World War, he was appointed as the leading German foreign ministry official for the Balkans (including Greece, Serbia, Albania and Montenegro).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5b4c8eef90",
  "kind": "yes/no",
  "text": "Claim: Buddymoon was written in part by a American actor who appeared in a number of TV shows was named one of The Hollywood Reporter's top 25 digital stars in 2015.\n\nPassages:\n\n[Buddymoon]\nBuddymoon (previously known as Honey Buddies) is a 2016 American independent comedy film directed by Alex Simmons; written by Simmons, Flula Borg, and David Giuntoli; and starring Borg and Giuntoli.\n\n[Flula Borg]\nFlula Borg (born March 28, 1982) is a German actor, comedian, musician, and YouTube personality who is better known as DJ Flula or simply Flula (sometimes stylized as f|u|a). Borg has appeared in several feature films, including \"Pitch Perfect 2\", and a number of popular TV shows. In 2015, he was named one of The Hollywood Reporter's Top 25 Digital Stars as well as one of Variety's 10 Comics to Watch.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc77790f558",
  "kind": "yes/no",
  "text": "Claim: Young the Giant and Archive are both rock groups. The other group made an archive album called Noise.\n\nPassages:\n\n[Noise (Archive album)]\nNoise is the fourth album of the London-based trip hop band Archive.\n\n[Young the Giant]\nYoung the Giant is an American rock band that formed in Irvine, California, in 2004.\n\n[Archive (band)]\nArchive are a musical group based in London, England, whose music spans electronic, trip hop, avant-garde, post-rock and progressive rock.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q49140108c4",
  "kind": "yes/no",
  "text": "Claim: Super Bowl XLVIII was the American football game where Malcolm Smith named Most Valuable player.\n\nPassages:\n\n[Malcolm Smith (American football)]\nSmith was named the Most Valuable Player of Super Bowl XLVIII after they defeated the Denver Broncos.\n\n[Super Bowl XLVIII]\nSuper Bowl XLVIII was an American football game between the American Football Conference (AFC) champion Denver Broncos and National Football Conference (NFC) champion Seattle Seahawks to decide the National Football League (NFL) champion for the 2013 season.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa09057c0de",
  "kind": "yes/no",
  "text": "Tweet: Fly 👏 the 👏 L 👏 \n\n#ThisIsMyCrew",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q012caac323",
  "kind": "yes/no",
  "text": "Claim: The village Pepease is located in the district that Abetifi is the capital of. It is in the country of Ghana.\n\nPassages:\n\n[Abetifi]\nAbetifi is a small town in south Ghana and is the capital of Kwahu East district, a district in the Eastern Region of south Ghana.\n\n[Pepease]\nPepease is a village in the Kwahu East district, a district in the Eastern Region of south Ghana.\n\n[Kwahu East District]\nThe Kwahu East District is one of the twenty-one (21) districts of the Eastern Region of south Ghana. The capital is Abetifi.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q067b5d074c",
  "kind": "yes/no",
  "text": "Claim: The creation of Fontana Lake submerged the small town of Proctor, North Carolina and Judson in 1982.\n\nPassages:\n\n[Proctor, North Carolina]\nThe town was flooded by Fontana Lake, which was created by the construction of the Fontana Dam, and remains submerged unless lake levels are very low.\n\n[Fontana Lake]\nMany towns were submerged shortly after the creation of Fontana Lake, such as Proctor and Judson.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa472ed8440",
  "kind": "yes/no",
  "text": "Tweet: don't cry because it happened, smile because it's over &lt;3",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qff8614d7ad",
  "kind": "yes/no",
  "text": "Claim: The Sierra Nevada mountains are located near this autonomous community, in which Spanish politician Felipe Alcaraz was born.\n\nPassages:\n\n[Granada]\nGranada ( , ] , ] ) is the capital city of the province of Granada, in the autonomous community of Andalusia, Spain. Granada is located at the foot of the Sierra Nevada mountains, at the confluence of four rivers, the Beiro, the Darro, the Genil and the Monachil.\n\n[Felipe Alcaraz]\nLuis Felipe Alcaraz Masats (born 1 March 1943 in Granada) is a Spanish politician.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q45be2ecdbe",
  "kind": "yes/no",
  "text": "Claim: The Royal Commission into Drug Trafficking (1977-1979) or Wodward Royal Commission was a royal commission initiated by the New South Wales Government to investigate and shut down drug trafficking in New South Wales, Australia, especially links between the New South Wales Police and Mafia, The Honoured Society, is a Calabrian 'Ndrangheta criminal confederation, started in Melbourne and currently active in all of Australia.\n\nPassages:\n\n[Royal Commission into Drug Trafficking]\nThe Royal Commission into Drug Trafficking (1977–1979) or Woodward Royal Commission was a royal commission initiated by the New South Wales Government to investigate drug trafficking in New South Wales, Australia, especially links between the Mafia and New South Wales Police and the disappearance of anti-marijuana campaigner Donald Mackay.\n\n[Honoured Society (Australia)]\nThe Honoured Society (Italian: \"Onorata Società\" ) is a Calabrian 'Ndrangheta criminal confederation, started in Melbourne and currently active in all Australia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb63eed6365",
  "kind": "yes/no",
  "text": "Claim: The notable work from French music video director Yoann Lemoine, Back to December, features an apology and plea for forgiveness.\n\nPassages:\n\n[Back to December]\nAccording to Swift, \"Back to December\" is the first time she ever apologizes to someone in a song. \"Back to December\" is considered an orchestral country pop ballad and its lyrics are a remorseful plea for forgiveness for breaking up with a former lover.\n\n[Yoann Lemoine]\nYoann Lemoine (born 16 March 1983) is a French music video director, graphic designer and singer-songwriter. His most notable works include his music video direction for Katy Perry's \"Teenage Dream\", Taylor Swift's single \"Back to December\", Lana Del Rey's \"Born to Die\" and Mystery Jets' \"Dreaming of Another World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8f9c9d25bc",
  "kind": "yes/no",
  "text": "Claim: The author of The Moons of Jupiter and Lillian Hellman are both writers.\n\nPassages:\n\n[Alice Munro]\nAlice Ann Munro ( , \"née\" Laidlaw ; born 10 July 1931) is a Canadian short story writer and Nobel Prize winner.\n\n[The Moons of Jupiter]\nThe Moons of Jupiter is a book of short stories by Alice Munro, published by Macmillan of Canada in 1982.\n\n[Lillian Hellman]\nLillian Florence Hellman (June 20, 1905 – June 30, 1984) was an American dramatist and screenwriter known for her success as a playwright on Broadway, as well as her left-wing sympathies and political activism.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa7f432801f",
  "kind": "yes/no",
  "text": "Claim: MedStar Georgetown University Hospital and Howard University Hospital are both located in Washington, D.C.\n\nPassages:\n\n[MedStar Georgetown University Hospital]\nIt is a not-for-profit, acute care teaching and research facility located in the Georgetown neighborhood of the Northwest Quadrant of Washington, D.C.\n\n[Howard University Hospital]\nHoward University Hospital, previously known as Freedmen's Hospital, is a major hospital lcated in Washington, D.C., built on the site of the previous Griffith Stadium.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa4c844c7f3",
  "kind": "yes/no",
  "text": "Tweet: Parents always mess up ur plans😒",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q432234d296",
  "kind": "yes/no",
  "text": "Claim: The movie filmed in Clermont, Iowa and Frozen films are of the same genre.\n\nPassages:\n\n[The Straight Story]\nThe Straight Story is a 1999 internationally co-produced biographical road drama film directed by David Lynch.\n\n[Frozen (2013 film)]\nFrozen is a 2013 American 3D computer-animated musical fantasy film produced by Walt Disney Animation Studios and released by Walt Disney Pictures.\n\n[Clermont, Iowa]\nScenes for the movie \"The Straight Story\" were filmed here.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 }
]
