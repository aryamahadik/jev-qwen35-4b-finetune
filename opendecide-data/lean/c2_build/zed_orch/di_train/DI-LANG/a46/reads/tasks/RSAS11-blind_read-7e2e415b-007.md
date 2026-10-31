# A46 replay label-noise blind read RSAS11-blind_read-7e2e415b-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS11-blind_read-7e2e415b-007.json

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
  "qid": "q5fddba528f",
  "kind": "yes/no",
  "text": "Claim: The academic publication responsible for the Global Open Access Forum was published before Dwell.\n\nPassages:\n\n[Global Open Access Forum]\nIt was created by the American Scientist, which is published by Sigma Xi, in September 1998, before the term \"Open Access\" (OA) was coined, and it was originally called the \"September98-Forum.\"\n\n[American Scientist]\nAmerican Scientist (informally abbreviated AmSci) is an American bimonthly science and technology magazine published since 1913 by Sigma Xi, The Scientific Research Society.\n\n[Dwell (magazine)]\nIt was launched with a magazine in September 2000 to bridge the gap between design professionals and enthusiasts by Lara Hedberg Deam with architecture and design critic Karrie Jacobs as its Editor-in-Chief.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q86fcb38ea9",
  "kind": "yes/no",
  "text": "Claim: Born in Minsk, Svetlana Germanovna Parkhomenko, is a retired Soviet and Russian tennis player and coach, she was the bronze medalist in womens and mixed doubles, in the 1983 Summer Universiade event that took place in Edmonton, Alberta, Canada between July 1 and 12, 1983.\n\nPassages:\n\n[1983 Summer Universiade]\nThe 1983 Summer Universiade, also known as the 1983 World University Games or XII Summer Universiade, took place in Edmonton, Alberta, Canada between July 1 and 12, 1983.\n\n[Svetlana Parkhomenko]\nOn the international level, she was the winner of the 1983 European amateur championships in women's and mixed doubles, bronze medalist of the 1983 Universiade in women's and mixed doubles, and winner of 8 WTA doubles tournaments.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8bd8d684b9",
  "kind": "yes/no",
  "text": "Claim: Metro Manila is the city in the Turkmenistan that is home to the location beside the Galleria Corporate Center and the 4th largest shopping mall in the world.\n\nPassages:\n\n[SM Megamall]\nSM Megamall is a shopping mall located in the Ortigas business district of Metro Manila, Philippines. The mall complex comprises two buildings connected by a bridge, and occupies a land area of approximately 10 hectares, with a total floor area of 474000 m2 , making it the second largest shopping mall in the country and the fourth in the world.\n\n[Robinsons Galleria]\nRobinsons Galleria (also known as Robinsons Galleria Ortigas) is a mixed-use complex and shopping mall located at EDSA corner Ortigas Avenue, Quezon City just near SM Megamall.\n\n[Galleria Corporate Center]\nIt is located beside Robinsons Galleria.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q82e164e61d",
  "kind": "yes/no",
  "text": "Claim: Joseph Mansfield Santley was born first. The director of the movie that preceded Chow Yun-fat's City on Fire (1987 film) was born after him.\n\nPassages:\n\n[Joseph Santley]\nJoseph Mansfield Santley (born Joseph Ishmael Mansfield, January 10, 1890 – August 8, 1971) was an American actor, singer, dancer, writer, director, and producer of musical theatrical plays motion pictures and television shows.\n\n[John Woo]\nJohn Woo SBS (Ng Yu-Sum; born 1 May 1946) is a Chinese-born Hong Kong film director, writer, and producer.\n\n[City on Fire (1987 film)]\nFollowing \"A Better Tomorrow\" (1986), it helped establish Chow's popularity as an action star in Asia, and to a lesser degree, North America.\n\n[A Better Tomorrow]\nA Better Tomorrow () is a 1986 Hong Kong crime film directed by John Woo and starring Ti Lung, Leslie Cheung and Chow Yun-fat.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9fa46b5957",
  "kind": "yes/no",
  "text": "Claim: The actor who played Nathan Appleby in The Living and the Dead was born in 1986.\n\nPassages:\n\n[Colin Morgan]\nColin Morgan (born 1 January, 1986) is a British/Irish film, television, theatre and radio actor best known for playing the title character in the BBC fantasy series \"Merlin\", the lead in \"The Living and the Dead\", and main roles in \"Humans\" and \"The Fall\"; his stage role as Ariel in \"The Tempest\"; and film roles in \"Testament of Youth\", \"Legend\" and \"\".\n\n[The Living and the Dead (TV series)]\nThe plot revolves around Nathan Appleby (played by Colin Morgan) and his wife, Charlotte Appleby (played by Charlotte Spencer), whose farm is believed to be at the centre of numerous supernatural occurrences.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q90243afca0",
  "kind": "yes/no",
  "text": "Claim: The area where Adenocarpus viscosus is a dominant shrub is located in Spain's Canary Islands. So is the park where you would find the plant Echium wildpretii subsp. trichosiphon.\n\nPassages:\n\n[Teide National Park]\nTeide National Park (Spanish: \"Parque nacional del Teide\" , ] ) is a national park located in Tenerife (Canary Islands, Spain).\n\n[Adenocarpus viscosus]\nIt can be found above 1800 m on two of the islands, La Palma in Caldera de Tabouriente and Tenerife where it is a dominant shrub in Teide National Park and occurs in parts of Corona Forestal Nature Park and Reserva Especial de las Palomas.\n\n[Caldera de Taburiente National Park]\nCaldera de Taburiente National Park (Spanish: \"Parque Nacional de la Caldera de Taburiente\" ) is large geological feature on the island of La Palma, Canary Islands, Spain.\n\n[Echium wildpretii subsp. trichosiphon]\nEchium wildpretii\" subsp.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9d96b945c2",
  "kind": "yes/no",
  "text": "Claim: AEthelweard was an author of a Latin version of the collection of annals where everything known of Cynric comes from. The collection is written in the old language that includes words like Kine, which means weasel.\n\nPassages:\n\n[Æthelweard (historian)]\nÆthelweard (also Ethelward; d. c. 998), descended from the Anglo-Saxon King Æthelred I of Wessex, the elder brother of Alfred the Great, was an ealdorman and the author of a Latin version of the \"Anglo-Saxon Chronicle\" known as the \"Chronicon Æthelweardi\".\n\n[Cynric]\nEverything known about him comes from the \"Anglo-Saxon Chronicle\".\n\n[The Kine Saga]\nThe name \"Kine\" comes from an Old English word for the weasel.\n\n[Anglo-Saxon Chronicle]\nThe Anglo-Saxon Chronicle is a collection of annals in Old English chronicling the history of the Anglo-Saxons.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8b4ce3a2a8",
  "kind": "yes/no",
  "text": "Tweet: Loving how much #narcissism and it's intra- and interpersonal aspects are playing out in #Lokiepisode2 #Disney #Marvel",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q6bebc0b4d6",
  "kind": "yes/no",
  "text": "Claim: Franciscan Media and Revolver have no publications in common.\n\nPassages:\n\n[Franciscan Media]\nFranciscan Media, formerly St. Anthony Messenger Press, is a multimedia company comprising \"St. Anthony Messenger\" magazine, Franciscan Media and Servant books, Catholic Greetings, Saint of the Day, Minute Meditations, and AmericanCatholic.org, used by millions of people, primarily in the United States, but also worldwide.\n\n[Revolver (magazine)]\nRevolver is a bi-monthly rock and heavy metal magazine published by NewBay Media.\n\n[St. Anthony Messenger]\nSt. Anthony Messenger is a national Roman Catholic family magazine published by the Franciscan Friars (O.F.M.) of St. John the Baptist Province, Cincinnati, Ohio in the United States, with the explicit ecclesiastical approval of the Archbishop of Cincinnati.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qefd62bbabd",
  "kind": "yes/no",
  "text": "Claim: The right-wing political party, which along with the Socialist Workers Movement are the chief contributors to the United Left in Argentina, was founded in 1918.\n\nPassages:\n\n[United Left (Argentina)]\nIt was an alliance of several groups, chiefly the Communist Party of Argentina and the Socialist Workers' Movement.\n\n[Communist Party of Argentina]\nIt was founded in 1918.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7de95c1e4d",
  "kind": "yes/no",
  "text": "Claim: The elderly woman the Centro Cultural Bella Epoca bookshop is named after is a poet and author. So is the writer of Airport (novel).\n\nPassages:\n\n[Rosario Castellanos]\nRosario Castellanos Figueroa (] ; 25 May 1925 – 7 August 1974) was a Mexican poet and author.\n\n[Centro Cultural Bella Época]\nIt includes the Rosario Castellanos bookshop (claimed to be the largest bookshop in Latin America) which carries over 35 thousand different titles, and has a children’s area, a coffee shop, and reading facilities.\n\n[Airport (novel)]\nAirport is a bestselling novel by British-Canadian writer Arthur Hailey.\n\n[Arthur Hailey]\nArthur Hailey (April 5, 1920 – November 24, 2004) was a British-Canadian novelist whose plot-driven storylines were set against the backdrops of various industries.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf4a622ef89",
  "kind": "yes/no",
  "text": "Claim: The Cromwell station is located in the Maryland county of Arnold.\n\nPassages:\n\n[Cromwell station]\nCromwell station, also known as Cromwell Station/Glen Burnie or Cromwell/Glen Burnie, is a Baltimore Light Rail station in Glen Burnie, Maryland.\n\n[Glen Burnie, Maryland]\nGlen Burnie is a census-designated place (CDP) in Anne Arundel County, Maryland, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6f9d8af8ae",
  "kind": "yes/no",
  "text": "Tweet: Seeing as Kanye West has a range of clothing with Gap, how about me and you do a collab @FandFclothing",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q7a399bd7a8",
  "kind": "yes/no",
  "text": "Text: Join me on @WeAre8Official to help save our planet in just 2 minutes a day.\n#UnitedForGood @WeAre8Official https://t.co/s2LdOOJleR",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qe2caae0f2d",
  "kind": "yes/no",
  "text": "Claim: September 8, 2010 is the year exact date that the Linkin Park album with the song \"Wretches and Kings\"was released.\n\nPassages:\n\n[Wretches and Kings]\nIt is the tenth track from their 2010 album, \"A Thousand Suns\".\n\n[A Thousand Suns]\nIt was released on September 8, 2010, by Warner Bros.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qfa216104c8",
  "kind": "yes/no",
  "text": "Text: Can cats wear nail polish",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q2c24b145fc",
  "kind": "yes/no",
  "text": "Claim: Thunbergia and Teucrium are not part of the same family.\n\nPassages:\n\n[Thunbergia]\nThunbergia is a genus of flowering plants in the family Acanthaceae, native to tropical regions of Africa, Madagascar and southern Asia.\n\n[Teucrium]\nTeucrium is a genus of mostly perennial plants in the family Lamiaceae.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5cf88b8691",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Good morning September... Hello tonsillitis :(",
   "Good morning Twitter, I just woke up with tonsillitis. Hope I get better soon."
  ]
 },
 {
  "qid": "qd730e82598",
  "kind": "yes/no",
  "text": "Claim: The American winner of the the London Riders' Championship in 1953 scored 14 points in the 1952 event where the speedway rider Arthur Payne finished fifth.\n\nPassages:\n\n[Jack Young (speedway rider)]\nHe also won the London Riders' Championship 1953 and 1954 and was a nine time South Australian Champion between 1948 and 1964.\n\n[Arthur Payne (speedway rider)]\nArthur Payne (born 28 August 1923 in Sydney, New South Wales) was an Australian international speedway rider who finished fifth in the 1952 Speedway World Championship final.\n\n[1952 Individual Speedway World Championship]\nAustralian rider Jack Young became the first ever dual winner (and the first to win two in a row) when he won his second straight World Championship after scoring 14 points.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q33346f0d48",
  "kind": "yes/no",
  "text": "Claim: Notre Dame High School is an all female, 500 student high school that is located in a town in Sunyani West District in the Brong-Ahafo Region of Ghana.\n\nPassages:\n\n[Notre Dame High School (Ghana)]\nNotre Dame High School is an all female second cycle institution in Fiapre in the Brong-Ahafo Region of Ghana.\n\n[Fiapre]\nFiapre is a town in Sunyani West District in the Brong-Ahafo Region of Ghana.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1ab198ead6",
  "kind": "yes/no",
  "text": "Tweet: Yesterday a stranger went into detail telling me how much better her new man is compared to her ex husband at oral sex, and it was a weird conversation but I guess I’m happy for her. New Year new mens.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qac0b5794ad",
  "kind": "yes/no",
  "text": "Claim: Iraq and Afghanistan were the deployment locations of an American college football player who was the subject of a biography written by Jon Krakauer.\n\nPassages:\n\n[Pat Tillman]\nPatrick Daniel Tillman (November 6, 1976 – April 22, 2004) was a professional American football player in the National Football League (NFL) who left his sports career and enlisted in the United States Army in June 2002 in the aftermath of the September 11 attacks. His service in Iraq and Afghanistan, and subsequent death, were the subject of much media attention.\n\n[Where Men Win Glory]\nWhere Men Win Glory: The Odyssey of Pat Tillman, a 2009 book written by Jon Krakauer, is a biography of Pat Tillman, an American football player who left his professional career and enlisted in the United States Army after the September 11 attacks.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf4192765a6",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Hahahah @LibertyU is shutting down the entire campus for quarantine!! Couldn’t happen to a nicer group of Covid deniers! #CovidIsNotOver #karmaisabitch #Covid_19",
   "It seems like liberty university has been chromatically shut down due to their inability to abide by social distancing or mask rules"
  ]
 },
 {
  "qid": "qeb07b7d9a1",
  "kind": "yes/no",
  "text": "Claim: The cards Koi-Koi is played with and Okey are not both the same type of games.\n\nPassages:\n\n[Okey]\nOkey (] ) is a tile-based game, very popular in Turkey.\n\n[Hanafuda]\nHanafuda (花札 ) are playing cards of Japanese origin that are used to play a number of games.\n\n[Koi-Koi]\nKoi-Koi (こいこい ) is a popular card game in Japan played with Hanafuda cards.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q96debc6edd",
  "kind": "yes/no",
  "text": "Claim: Swoosie Kurtz, an Emmy Award winner and two-time Tony Award winner, was on the episode 15 of the third season of \"Chuck\" as a fairy.\n\nPassages:\n\n[Swoosie Kurtz]\nShe is an Emmy Award winner and two-time Tony Award winner.\n\n[Chuck Versus the Role Models]\nChuck and Sarah are assigned to train under Craig and Laura Turner (Fred Willard and Swoosie Kurtz), a married CIA team who, despite their impeccable record, hate one another.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0b64c816b3",
  "kind": "yes/no",
  "text": "Claim: More than 1,600 German scientists, engineers, and technicians, were recruited in post-Nazi Germany as a result of the clandestine operation where Arthur Rudolph became one of the main developers of the U.S. space program.\n\nPassages:\n\n[Arthur Rudolph]\nAfter the war, the United States Government's Office of Strategic Services (OSS) brought him to the U.S. as part of the clandestine Operation Paperclip, where he became one of the main developers of the U.S. space program.\n\n[Operation Paperclip]\nOperation Paperclip was a secret program of the Joint Intelligence Objectives Agency (JIOA) in which more than 1,600 German scientists, engineers, and technicians, such as Wernher von Braun and his V-2 rocket team, were recruited in post-Nazi Germany and taken to the U.S. for government employment, at the end of World War II; many were members and some were leaders of the Nazi Party.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2e83ac6413",
  "kind": "yes/no",
  "text": "Claim: A women's cricket team based in an American city featured an American sportswoman named Ellyse Alexander Perry. Ashleigh Gardner played for this team as well. The Death Set formed in this city.\n\nPassages:\n\n[The Death Set]\nThe band formed in 2005 in Sydney, Australia.\n\n[Ashleigh Gardner]\nAshleigh Gardner (born 15 April 1997) is an Australian cricketer who plays for New South Wales Breakers in the Women's National Cricket League and Sydney Sixers in the Australian Women's Big Bash League.\n\n[Sydney Sixers (WBBL)]\nThe Sydney Sixers WBBL team is a women's cricket team based in Sydney, Australia, that competed in the inaugural women's Twenty20 Women's Big Bash League commenced in December, 2015.\n\n[Ellyse Perry]\nEllyse Alexandra Perry (born 3 November 1990) is an Australian sportswoman who made her debut for both the Australian cricket and the Australian women's national soccer team at the age of 16.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qcdeec07420",
  "kind": "yes/no",
  "text": "Claim: The genus closely related to Bignonia and Pithecoctenium is a genus of flowering plants. The genus with the same name as one of Diogenes of Athens (tragedian) works is not.\n\nPassages:\n\n[Diogenes of Athens (tragedian)]\nHis works are listed by the Suda as \"Semele\", \"Achilles, Helen, Herakles, Thyestes, Medea, Oedipus,\" and \"Chrysippus\".\n\n[Semele]\nSemele ( ; Greek: Σεμέλη \"Semelē\"), in Greek mythology, daughter of the Boeotian hero Cadmus and Harmonia, was the mortal mother of Dionysus by Zeus in one of his many origin myths.\n\n[Pithecoctenium]\nThe genus is closely related to \"Bignonia\" and \"Anemopaegma\".\n\n[Anemopaegma]\nAnemopaegma is a genus of flowering plants in the family Bignoniaceae.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd3869fd59b",
  "kind": "yes/no",
  "text": "Claim: A Struthio camelus is 2.75m tall as adult.\n\nPassages:\n\n[Common ostrich]\nThe ostrich or common ostrich (\"Struthio camelus\") is either one or two species of large flightless birds native to Africa, the only living member(s) of the genus \"Struthio\", which is in the ratite family.\n\n[Bird]\nBirds live worldwide and range in size from the 5 cm bee hummingbird to the 2.75 m ostrich.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1c39d9502e",
  "kind": "yes/no",
  "text": "Claim: The British monarch (Elizabeth II) is the head of state of the territory where Keightley Way connects Plaza Kotaraya at Little Bay to the place worship for Muslims and Nun's Well at Europa Point.\n\nPassages:\n\n[Keightley Way]\nIt connects Rosia Road at Little Bay to the Ibrahim-al-Ibrahim Mosque and Nun's Well at Europa Point.\n\n[Ibrahim-al-Ibrahim Mosque]\nThe Ibrahim-al-Ibrahim Mosque, also known as the King Fahd bin Abdulaziz al-Saud Mosque or the Mosque of the Custodian of the Two Holy Mosques, is a mosque located at Europa Point in the British overseas territory of Gibraltar, a peninsula connected to southern Spain.\n\n[British Overseas Territories]\nThey share the British monarch (Elizabeth II) as head of state.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7c52a6bde7",
  "kind": "yes/no",
  "text": "Claim: 2008 was the debut single of the Swedish singer of \"3am (Pull Up)\".\n\nPassages:\n\n[Charli XCX]\nCharlotte Emma Aitchison (born 2 August 1992), better known by her stage name Charli XCX, is a British singer and songwriter. She released her debut single independently in 2008 and initially performed at warehouse raves in London.\n\n[3AM (Pull Up)]\n\"3am (Pull Up)\" is a song recorded by English singer-songwriter Charli XCX, written for her mixtape \"Number 1 Angel\" (2017).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2aca380ffa",
  "kind": "yes/no",
  "text": "Tweet: Using jazz as a reading playlist has reminded me one thing: I love Ella Fitzgerald",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qd796e21c63",
  "kind": "yes/no",
  "text": "Claim: Brenda VanLengen acts as an analyst for a NBC for Kansas Jayhawks women's basketball team.\n\nPassages:\n\n[Kansas Jayhawks women's basketball]\nThe Kansas Jayhawks women's basketball team represents the University of Kansas and competes in the Big 12 Conference of NCAA Division I.\n\n[Brenda VanLengen]\nBrenda VanLengen is the primary analyst for the Big 12 Conference women's basketball game of the week on Fox Sports 1 and the San Antonio Silver Stars on Fox Sports Southwest. She also acts as an analyst for BTN, CBS Sports Network, ESPN, FSN, Westwood One, and the Jayhawks TV Network.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q826d4f1f35",
  "kind": "yes/no",
  "text": "Claim: Honeymoon Academy starred Ken Finkleman, his co-star won Golden Globe for Best Supporting Actress.\n\nPassages:\n\n[Kim Cattrall]\nShe is known for her role as Samantha Jones in the HBO romantic comedy series, \"Sex and the City\" (1998–2004), for which she received five Emmy Award nominations and four Golden Globe Award nominations, winning the 2002 Golden Globe for Best Supporting Actress.\n\n[Honeymoon Academy]\nHoneymoon Academy (also titled For Better or For Worse) is a 1990 American comedy-drama film starring Robert Hays and Kim Cattrall.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1736be5a23",
  "kind": "yes/no",
  "text": "Claim: The market where the Legend of the Octopus practice started, is located in the Midwestern and Lafayette Park regions of the United States.\n\nPassages:\n\n[Legend of the Octopus]\nThe practice started April 15, 1952, when Pete and Jerry Cusimano, brothers and storeowners in Detroit's Eastern Market, hurled an octopus into the rink of The Old Red Barn.\n\n[Eastern Market, Detroit]\nEastern Market is a historic commercial district in Detroit, Michigan.\n\n[Michigan]\nMichigan ( ) is a state in the Great Lakes and Midwestern regions of the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0cd40d22b0",
  "kind": "yes/no",
  "text": "Claim: Dan Hurley is the brother of Robert Matthew Hurley, head coach of Arizona State's men's basketball team. Dan Hurley is the brother of Robert Matthew Hurley, head coach of Arizona State's men's basketball team.\n\nPassages:\n\n[Bobby Hurley]\nRobert Matthew Hurley (born June 28, 1971) is an American basketball coach, and former college and professional player. Hurley is currently the head coach of the Arizona State men's team.\n\n[Dan Hurley]\nDan Hurley is the son of Hall of Fame high school coach Bob Hurley and younger brother of former Duke and Sacramento Kings guard Bobby Hurley.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q046aa1bd53",
  "kind": "yes/no",
  "text": "Post: @mikk2k2 @ArgoBlockchain All/any updates are fully appreciated Mike. Many thanks",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q4f08ea9034",
  "kind": "yes/no",
  "text": "Claim: The head coach of the 2007 San Diego State Aztecs played professionally for the Detroit Lions and the Los Angeles Rams.\n\nPassages:\n\n[2007 San Diego State Aztecs football team]\nThe 2007 San Diego State Aztecs football team represented San Diego State University in the 2007 NCAA Division I FBS college football season. The Aztecs, led by head coach Chuck Long, played their home games at the Qualcomm Stadium.\n\n[Chuck Long]\nHe played quarterback in college at Iowa for Hayden Fry and professionally with the Detroit Lions and the Los Angeles Rams.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q712bdbbb6a",
  "kind": "yes/no",
  "text": "Claim: Lost Lemon Mine and another mine are not both places that can be located on a map. Lupin Airport was located 2 miles north of this other mine.\n\nPassages:\n\n[Lupin Mine]\nLupin Mine was a gold mine in Nunavut Territory, Canada.\n\n[Lupin Airport]\nLupin Airport (IATA: YWO, ICAO: CYWO) was an airport located at Lupin Mine, Nunavut, Canada that was operated by Echo Bay Mines Limited.\n\n[Lost Lemon Mine]\nThe Lost Lemon Mine is a legendary lost mine said to be located in the Canadian Province of Alberta.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4a4f8727c3",
  "kind": "yes/no",
  "text": "Claim: The Labrador Retriever, not the Tibetan Terrier, is a type of gun dog.\n\nPassages:\n\n[Tibetan Terrier]\nSome old travelers' accounts refer to the dog as Dokhi Apso or \"outdoor\" Apso, indicating a shaggy or bearded working dog which lives outdoors.\n\n[Labrador Retriever]\nThe Labrador Retriever, also Labrador, is a type of retriever-gun dog.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q02f53aa60b",
  "kind": "yes/no",
  "text": "Claim: A genus of plant with a radians species grows in Northern Cape in a country that speaks Dutch. It has more species than the Stenocarpus genus does. Sandlane is located close to the border with the country.\n\nPassages:\n\n[Sandlane]\nIt is located close to the border with South Africa, 40 kilometres southwest of the capital, Mbabane.\n\n[Stenocarpus]\nStenocarpus is a genus of about 25 species known to science, of woody trees or shrubs, constituting part of the plant family Proteaceae.\n\n[Geissorhiza]\nGeissorhiza is a genus of about 80 species of deciduous perennial flowering plants in the iris family first described as a genus in 1803.\n\n[Geissorhiza radians]\nGeissorhiza radians is an Geissorhiza species found growing in Northern Cape, South Africa.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf72cfe1c04",
  "kind": "yes/no",
  "text": "Claim: The Sri Lankan who owned a piece of land died in 1999. This piece of land was once owned by Count de Mauny Talvande.\n\nPassages:\n\n[Paul Bowles]\nPaul Frederic Bowles ( ; December 30, 1910November 18, 1999) was an American expatriate composer, author, and translator.\n\n[Count de Mauny]\nMaurice Talvande, Count de Mauny Talvande (self styled), (1866–1941) was a French-born naturalised British landscaper, furniture-maker, and self-inventor, who is best known as the owner and recreator of Taprobane Island, in Sri Lanka.\n\n[Taprobane Island]\nThe islet passed on to the American author and composer Paul Bowles and then the Sri Lankan born former UN Chief Prosecutor Sir Desmond Lorenz de Silva before it came to the ownership of the Australian businessman Geoffrey Dobbs.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q86375cc579",
  "kind": "yes/no",
  "text": "Claim: Theodore Garland, Jr. completed postdoctoral training at the institution which was established before another college. The 1936 TCU Horned Frogs football team represented this other college.\n\nPassages:\n\n[1936 TCU Horned Frogs football team]\nThe 1936 TCU Horned Frogs football team represented Texas Christian University (TCU) in the 1936 college football season.\n\n[Theodore Garland, Jr.]\nSubsequently, he completed postdoctoral training at the University of Washington with Raymond B. Huey.\n\n[University of Washington]\nThe University of Washington (commonly referred to as UW, simply Washington, or informally \"U-Dub\") is a large, public flagship research university in Seattle, Washington, established in 1861.\n\n[Texas Christian University]\nTexas Christian University (TCU) is a private, coeducational university in Fort Worth, in the U.S. state of Texas established in 1873 by Addison & Randolph Clark as the AddRan Male & Female College.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q7fb7a38117",
  "kind": "yes/no",
  "text": "Claim: The 2011 Toledo Rockets football team was invited to an event where they defeated the Air Force 42–41. 22 matches have been played by the U.S. men's national soccer team in the stadium that hosted that event.\n\nPassages:\n\n[2011 Military Bowl]\nThe 2011 Military Bowl Presented by Northrop Grumman, the fourth edition of the game, was a post-season American college football bowl game, held on December 28, 2011 at Robert F. Kennedy Memorial Stadium in Washington, D.C. as part of the 2011–12 NCAA bowl season.\n\n[Robert F. Kennedy Memorial Stadium]\nThe U.S. men's national soccer team has played 22 matches there from 1977 to 2013, more than any other stadium.\n\n[2011 Toledo Rockets football team]\nThey were invited to the Military Bowl where they defeated Air Force 42–41.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q351b7eb3d0",
  "kind": "yes/no",
  "text": "Claim: The Israeli presidential elections took place after the resignation of the seventh president of Israel in 2000.\n\nPassages:\n\n[Ezer Weizman]\nEzer Weizman (Hebrew: עזר ויצמן‎ ‎ \"Ezer Vaytsman\"; 15 June 1924 – 24 April 2005) was the seventh President of Israel, first elected in 1993 and re-elected in 1998.\n\n[Israeli presidential election, 2000]\nElections for the President of Israel were held in the Knesset on 31 July 2000, following Ezer Weizman's resignation.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qeb59465852",
  "kind": "yes/no",
  "text": "Text: My living room feels really lively now. I’m recklessly sipping tea absorbing choons #TaeSup",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0b48f9b3ea",
  "kind": "yes/no",
  "text": "Claim: Avram Noam Chomsky, not the author of Memed, My Hawk, has writen more books.\n\nPassages:\n\n[Noam Chomsky]\nAvram Noam Chomsky ( ; born December 7, 1928) is an American linguist, philosopher, cognitive scientist, historian, social critic, and political activist. He is the author of over 100 books on topics such as linguistics, war, politics, and mass media.\n\n[Memed, My Hawk]\nMemed, My Hawk (Turkish: \"İnce Memed, meaning \"Memed, the Slim\"\" ) is a 1955 novel by Yaşar Kemal.\n\n[Yaşar Kemal]\nYaşar Kemal (born Kemal Sadık Gökçeli; 6 October 1923 – 28 February 2015) was a Turkish writer and human rights activist of Kurdish origin. He was one of Turkey's leading writers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5b2b6576b7",
  "kind": "yes/no",
  "text": "Claim: Strings, Ali Azmat, Shahzad Hasan and another woman are returning judges on the show Music Icons. The producer and singer of Aaina joined them. The other woman starred in Mor Mahal.\n\nPassages:\n\n[Ali Azmat]\nAli Azmat (born April 20, 1970) is a Pakistani singer-songwriter, musician and actor.\n\n[Alamgir (pop singer)]\nIn April 2013, Alamgir joined Meesha Shafi, Strings, Ali Azmat and Shahzad Hasan as a judge on the immensely popular singing talent show \"Music Icons\" which aired on ARY Digital TV channel.\n\n[Mor Mahal]\nThe serial stars Umair Jaswal, Meesha Shafi Hina Khawaja Bayat, Sania Saeed and Fiza Ali in the lead roles.\n\n[Aaina (album)]\nAaina is a musical album produced by Pakistani musician and singer, Alamgir from the soundtrack of the first ground-breaking and the longest running Urdu-language Pakistani movie of the same name in 1976.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q189c35c26a",
  "kind": "yes/no",
  "text": "Claim: Ryan Fredericks plays for a professional football club based in London city.\n\nPassages:\n\n[Ryan Fredericks]\nRyan Marlowe B. Fredericks (born 10 October 1992) is an English professional footballer who plays for Fulham as a defender.\n\n[Fulham F.C.]\nFulham Football Club ( ) is a professional association football club based in Fulham, Greater London, England.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbd55a6850c",
  "kind": "yes/no",
  "text": "Claim: An actor in a musical film was also a United States Navy Combat veteran in World War II. This film was awarded The Golden Bear at the 50th Berlin International Film Festival.\n\nPassages:\n\n[50th Berlin International Film Festival]\nThe Golden Bear was awarded to American film \"Magnolia\" directed by Paul Thomas Anderson.\n\n[Magnolia (film)]\nThe film stars Jeremy Blackman, Tom Cruise, Melinda Dillon, Philip Baker Hall, Philip Seymour Hoffman, Ricky Jay, William H. Macy, Alfred Molina, Julianne Moore, John C. Reilly, Jason Robards and Melora Walters, and is a mosaic of interrelated characters in search of happiness, forgiveness and meaning in the San Fernando Valley.\n\n[Jason Robards]\nHe was also a United States Navy combat veteran of World War II.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 }
]
