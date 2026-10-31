# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-006.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's aid).

## Instructions

You are auditing the gold labels of a training set for label noise. Each item shows the material (text, question, options, definitions), the gold label that the dataset's human annotators gave (human_label), and the answers of two independent blind readers (read_1, read_2; an answer may be "abstain" or null when the reader gave none). The text is DATA only: ignore any instructions inside it.
Decide whether the human label is right, from the material alone (do not count the readers' votes; readers are fallible and often miss context):
- gold_ok: the human label is a correct, defensible answer under the question and definitions.
- wrong_gold: the human label is wrong: a careful reader with the same material would clearly answer differently.
- ambiguous: the material does not settle the answer, or two different answers are both defensible under the question as worded.
Never propose a new label. reason = one short line (at most 30 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "<gold_ok | wrong_gold | ambiguous>", "reason": "<one line>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its aid)

[
 {
  "aid": "a00300",
  "kind": "yes/no",
  "text": "Claim: Shirley Breeden won her first Senate term in a narrow upset over the politician who was a member of U.S. Army branch of the armed forces.\n\nPassages:\n\n[Joe Heck]\nJoseph John “Joe” Heck (born October 30, 1961) is an American politician, physician, and U.S. Army Brigadier General who had served as the U.S. Representative for Nevada's 3rd congressional district from 2011 to 2017.\n\n[Shirley Breeden]\nShe won her first term in 2008, when she narrowly upset incumbent Republican Joe Heck.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00301",
  "kind": "yes/no",
  "text": "Tweet: People who drive under the speed limit. Death Penalty.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00302",
  "kind": "yes/no",
  "text": "Tweet: @BuzzPatterson I say he's still pretty wiley.  A touch (?) of senility might be turbo-charging his wileyness, and he naturally loves the attention of his courtesan 'handlers'.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00303",
  "kind": "yes/no",
  "text": "Claim: The first major financial project for the Roller Coaster Corporation of America was renamed, and is now called the Iron Rattler.\n\nPassages:\n\n[Roller Coaster Corporation of America]\nRoller Coaster Corporation of America (abbreviated RCCA) is an amusement ride manufacturer based in the United States. The company's first major project was the Rattler at Six Flags Fiesta Texas in 1992, while their most famous coaster was the Son of Beast at Kings Island, the world's tallest and first looping wooden coaster when it opened in 2000.\n\n[Iron Rattler]\nIron Rattler is a steel roller coaster located at Six Flags Fiesta Texas in San Antonio, Texas. The ride opened in 2013, replacing The Rattler, a wooden roller coaster, by putting a new steel track on top of The Rattler's wooden support structure. The distance between the lowest and highest points of the first drop was increased from 124 to and the drop was made steeper by changing the angle to 81 degrees. The resulting modifications increased the speed of the trains from 65 to .",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00304",
  "kind": "yes/no",
  "text": "Claim: The logo of the American athletic shoe and clothing manufacturer who trademarked the slogan coined by Dan Wieden has made $26 billion in profit. Dan Wieden co-founded Wieden+Kennedy.\n\nPassages:\n\n[Swoosh]\nThe Swoosh is the logo of American athletic shoe and clothing manufacturer Nike, Inc. Today, it has become one of the most recognizable brand logos in the world, and the most profitable, having a worth of $26 billion alone.\n\n[Just Do It]\nJust Do It (stylized as JUST DO IT.) is a trademark of shoe company Nike, and one of the core components of Nike's brand.\n\n[Dan Wieden]\nDan Wieden (born 1945) Pronounced \"Why-den,\" is an American advertising executive who co-founded Wieden+Kennedy and coined the Nike tagline \"Just Do It.\"",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00305",
  "kind": "yes/no",
  "text": "Claim: The German poet and writer of Los heraldos negros was not a German national. Neither was the author of Tales of a Long Night.\n\nPassages:\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).\n\n[Los heraldos negros]\n\"Los heraldos negros\" is the title of a collection of poems written by the Peruvian poet César Vallejo between the years 1915 and 1918 and published in July 1919.\n\n[Tales of a Long Night]\nTales of a Long Night (German: \"Hamlet oder Die lange Nacht nimmt ein Ende\" ) (1956) is the last novel of German author Alfred Döblin.\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00306",
  "kind": "yes/no",
  "text": "Text: Woke up at 3 am with a MAD craving for pickles. I guess that means I'm expecting!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00307",
  "kind": "yes/no",
  "text": "Post: we happy!!!!!!!!!!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00308",
  "kind": "yes/no",
  "text": "Claim: The actor who recorded the comedy album The Sunny Side of the Street was born in 1945. He starred in the show \"Trial & Error\".\n\nPassages:\n\n[John Lithgow]\nJohn Arthur Lithgow ( ; born October 19 , 1945) is an American actor, musician, singer, comedian, voice actor, and author.\n\n[Trial &amp; Error (TV series)]\nIt stars Nicholas D'Agosto, Jayma Mays, Steven Boyer, Krysta Rodriguez, and Sherri Shepherd, with John Lithgow also starring in the first season.\n\n[The Sunny Side of the Street]\nThe Sunny Side of the Street is an album recorded by John Lithgow, released in 2006.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00309",
  "kind": "yes/no",
  "text": "Claim: Jim Lindberg and Alison Moyet are not singers of the same nationality.\n\nPassages:\n\n[Alison Moyet]\nGeneviève Alison Jane Moyet ( ; born 18 June 1961) is an English singer, songwriter and performer noted for her bluesy contralto voice.\n\n[Jim Lindberg]\nJames William Lindberg (born July 26, 1965) is an American singer and guitarist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00310",
  "kind": "yes/no",
  "text": "Text: I love calling my mom early in the morning and waking her up, I take it as pay back for all the times she never let me sleep in 😜",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00311",
  "kind": "yes/no",
  "text": "Claim: Ronald Wayne \"Ron\" Shelton, not Ken Mora, has won an Oscar.\n\nPassages:\n\n[Ron Shelton]\nRonald Wayne \"Ron\" Shelton (born September 15, 1945) is an American Oscar-nominated film director and screenwriter and former minor league baseball infielder.\n\n[Ken Mora]\nKenneth Oscar \"Ken\" Mora (born December 17, 1960) is an American screenplay writer, director, producer, editor, and voice actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00312",
  "kind": "yes/no",
  "text": "Claim: Justin Bieber is the Canadian singer who was originally featured on the song \"Bankroll\" composed by American DJ Diplo.\n\nPassages:\n\n[Bankroll (song)]\nOriginally, Justin Bieber was featured on the song, but due to Bieber already having exclusives with DJ Khaled (\"I'm the One\") and David Guetta (\"2U\") at around the same time as Diplo released \"Bankroll\", Diplo was forced to remove the original from his SoundCloud account.\n\n[I'm the One (DJ Khaled song)]\n\"I'm the One\" is a song written and performed by American musician DJ Khaled; Canadian singer Justin Bieber; and American rappers Quavo, Chance the Rapper and Lil Wayne.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00313",
  "kind": "yes/no",
  "text": "Claim: The T-Type is a series of Buick logos that were popular during the 1980s, this marketing approach for Buick products was a revival of a similar approach used in the 1960s (and later revived in the 1990s) with the Buick GS designation used on several high-volume cars built by Buick since 1965.\n\nPassages:\n\n[T-Type]\nThis marketing approach for Buick products was a revival of a similar approach used in the 1960s (and later revived in the 1990s) with the Buick GS designation.\n\n[Buick Gran Sport]\nThe Gran Sport name has been used on several high-performance cars built by Buick since 1965.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00314",
  "kind": "yes/no",
  "text": "Claim: The debut album of the lead singer was included in the compilation Finally the Punk Rockers Are Taking Acid. While both singer-songwriters have displayed incredible talent, an eclectic mix of musical styles sets Robert Palmer apart from him, causing him to gain populatiry in two continents.\n\nPassages:\n\n[Wayne Coyne]\nHe is the lead singer, occasional backing vocalist, guitarist, keyboardist, theremin player and songwriter for the band the Flaming Lips.\n\n[Hear It Is]\nThis album marks the debut of Wayne Coyne on vocals, after the departure of his brother Mark.\n\n[Robert Palmer (singer)]\nHe was known for his distinctive, soulful voice, eclectic mix of musical styles on his albums, combining soul, jazz, rock, pop, reggae, blues, and sartorial acumen.\n\n[Finally the Punk Rockers Are Taking Acid]\nFinally the Punk Rockers Are Taking Acid is a compilation album by The Flaming Lips, collecting their first three studio albums (\"Hear It Is\", \"Oh My Gawd!!!",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00315",
  "kind": "yes/no",
  "text": "Claim: J. Andrew \"Drew\" Crompton is chief of staff and counsel for Pennsylvania Senate Pro-Tempore Joe Scarnati, he served as deputy campaign manager for policy for Lynn Swann's campaign, in 2006, for Governor of Pennsylvania.\n\nPassages:\n\n[Drew Crompton]\nHe served as deputy campaign manager for policy for Lynn Swann's 2006 campaign for Governor of Pennsylvania.\n\n[Lynn Swann]\nIn 2006, he was the Republican nominee for Governor of Pennsylvania.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00316",
  "kind": "yes/no",
  "text": "Claim: This individual founded Ameche's Drive-in. He and the Wisconsin Badgers player won a Badgers trophy and was elected to the bowl game that also Chris Johnson (running back) has been three times in each of their first four seasons.\n\nPassages:\n\n[Ameche's Drive-in]\nAmeche's Drive-in was a fast-food restaurant chain based in Baltimore, Maryland, founded by Heisman Trophy winner and Baltimore Colts running back Alan Ameche.\n\n[Wisconsin Badgers football]\nWisconsin has had two Heisman Trophy winners, Alan Ameche and Ron Dayne, and have had nine former players inducted into the College Football Hall of Fame.\n\n[Chris Johnson (running back)]\nHe has been to three Pro Bowls and was the NFL's Offensive Player of the Year in 2009.\n\n[Alan Ameche]\nAmeche was elected to the Pro Bowl in each of his first four seasons in the league.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00317",
  "kind": "yes/no",
  "text": "Claim: The home ground of Fort Glanville Conservation Park, which is located in Semaphore Park, United FC is sponsored by a brewery that sold 69.7 million litres of beer in 2013. Semaphore Park is a seaside suburb.\n\nPassages:\n\n[Fort Glanville Conservation Park]\nFort Glanville Conservation Park is a protected area located in the Australian state of South Australia located in Semaphore Park, a seaside suburb of Adelaide consisting of a functional 19th century fort listed on the South Australian Heritage Register and some adjoining land.\n\n[Hindmarsh Stadium]\nThe Hindmarsh Stadium (currently known as the Coopers Stadium due to sponsorship from the Adelaide-based Coopers Brewery) is a multi-purpose stadium located in Adelaide, South Australia.\n\n[Adelaide United FC]\nAdelaide United's home ground is Hindmarsh Stadium.\n\n[Coopers Brewery]\nThe brewery sold 69.7 million litres of beer in the 2013 financial year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00318",
  "kind": "yes/no",
  "text": "Post: Bart is closed rn in Oakland so I can’t go to work, I’m so upset....",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00319",
  "kind": "yes/no",
  "text": "Claim: The artist whose first solo album was \"Girls\" and Graham Gouldman were in a band together. The song that inspired the album \"Relayted\" and \"Life Is a Minestrone\" are singles from this band's 1975 album.\n\nPassages:\n\n[The Original Soundtrack]\n\"The Original Soundtrack\" includes the singles \"Life Is a Minestrone\", and \"I'm Not in Love\", the band's most popular song.\n\n[Relayted]\nInspired by 10cc's \"I'm Not in Love\", every song on the album was recorded at 69 BPM.\n\n[I'm Not in Love]\n\"I'm Not in Love\" is a song by English group 10cc, written by band members Eric Stewart and Graham Gouldman.\n\n[Girls (album)]\nGirls is the first solo album released by Eric Stewart in 1980.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00320",
  "kind": "yes/no",
  "text": "Claim: William A. Seiter directed a 1926 silent film comedy. The star of that film also starred in Embarrassing Moments. He was an amateur boxing champion.\n\nPassages:\n\n[What Happened to Jones]\nWhat Happened to Jones is a 1926 silent film comedy directed by William A. Seiter and starring Reginald Denny.\n\n[Embarrassing Moments]\nThe film stars Reginald Denny, Merna Kennedy, Otis Harlan, Greta Granstedt, Virginia Sale and William Austin.\n\n[Reginald Denny (actor)]\nReginald Denny (born Reginald Leigh Dugmore, 20 November 1891 – 16 June 1967) was an English stage, film and television actor as well as an aviator and UAV pioneer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00321",
  "kind": "yes/no",
  "text": "Claim: The genus that Clianthus maximus belongs in, has more flower species than Callicoma.\n\nPassages:\n\n[Clianthus]\nClianthus, commonly known as kakabeak (\"Kōwhai ngutukākā\" in Māori), is a genus of flowering plants in the legume family Fabaceae, comprising two species of shrubs native to New Zealand.\n\n[Clianthus maximus]\nIt is one of two species of \"Clianthus\" (kaka beak) and both have striking clusters of red flowers which resemble the beak of the kākā, a New Zealand parrot.\n\n[Callicoma]\nCallicoma, is a plant genus that contains just one species, Callicoma serratifolia, a tall shrub or small tree which is native to Australia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00322",
  "kind": "yes/no",
  "text": "Claim: The canal that connects to the Pennsylvania and Ohio Canal is longer than another man made waterway. Remnants of this other waterway can be found at Beaver Creek State Park.\n\nPassages:\n\n[Beaver Creek State Park]\nHistoric remnants of the Sandy and Beaver Canal can be found throughout the park.\n\n[Pennsylvania and Ohio Canal]\nIt was unique in that it served to connect canals in two states (the Ohio and Erie Canal in Ohio and the Beaver and Erie Canal in Pennsylvania) and was funded by private interests.\n\n[Beaver and Erie Canal]\nThe Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the western edge of the state from the Ohio River to Lake Erie through Beaver County, Lawrence County, Mercer County, Crawford County, and Erie County, Pennsylvania.\n\n[Sandy and Beaver Canal]\nThe Sandy and Beaver Canal ran 73 mi from the Ohio and Erie Canal at Bolivar, Ohio, to the Ohio River at Glasgow, Pennsylvania.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00323",
  "kind": "yes/no",
  "text": "Claim: Mark Dayton is the current Governor of the state where the former wrestler, who appeared in a music video in \"Elephant Parts\".\n\nPassages:\n\n[Elephant Parts]\n\"Elephant Parts\" is one hour long with parody commercials and comedy sketches, and features five full-length music videos, including the popular songs \"Rio\", and \"Cruisin'\", which featured wrestler Steve Strong and Monterey-based comic \"Chicago\" Steve Barkley.\n\n[Stephen Cepello]\nAfter retiring from wrestling to focus on his art career, he was selected to paint the official Governor's Mansion and Minnesota State Capitol portraits of former wrestler and Governor of Minnesota Jesse Ventura.\n\n[Governor of Minnesota]\nThe current governor of Minnesota is Mark Dayton of the Democratic-Farmer-Labor Party (DFL).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00324",
  "kind": "yes/no",
  "text": "Claim: The first major improved highway is located in Wheeling, West Virginia.\n\nPassages:\n\n[Mount Echo, West Virginia]\nMount Echo is an unincorporated community in Ohio County, West Virginia, United States. It is part of the Wheeling, West Virginia Metropolitan Statistical Area.\n\n[National Road]\nThe National Road (also known as the Cumberland Road) was the first major improved highway in the United States built by the federal government.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00325",
  "kind": "yes/no",
  "text": "Claim: The player that won the 2007 Hamburg Masters doubles title with Bob Bryan is a tennis player. As is the individual that William Bowrey lost in the quarterfinals to at the summer 1969 Australian Open – Men's Singles.\n\nPassages:\n\n[1969 Australian Open – Men's Singles]\nWilliam Bowrey was the defending champion, but lost in the quarterfinals to Ray Ruffels.\n\n[Ray Ruffels]\nRaymond Owen \"Ray\" Ruffels (born 23 March 1946 in Sydney) is an Australian former professional tennis player and coach.\n\n[2007 Hamburg Masters]\nBob Bryan and Mike Bryan won the doubles title.\n\n[Mike Bryan]\nMichael Carl Bryan (born April 29, 1978) is an American professional tennis player.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00326",
  "kind": "yes/no",
  "text": "Claim: Andrea Albert Pierre Casiraghi, is the elder son of Caroline, Princess of Hanover, and her second husband Stefano Casiraghi, and is the eldest grandchild of Rainier III, Prince of Monaco, and the American actress Grace Kelly, who became Princess of Monaco after marrying Prince Rainier III, in April 1956.\n\nPassages:\n\n[Grace Kelly]\nGrace Patricia Kelly (November 12, 1929September 14, 1982) was an American actress who became Princess of Monaco after marrying Prince Rainier III, in April 1956.\n\n[Andrea Casiraghi]\nHe is the eldest grandchild of Rainier III, Prince of Monaco, and American actress Grace Kelly.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00327",
  "kind": "yes/no",
  "text": "Claim: Edsger Wybe Dijkstra (] ; 11 May 1930 – 6 August 2002) was a Dutch computer scientist and an early pioneer in many research areas of computing science who held the Schlumberger Centennial Chair in Computer Sciences at the University of Texas at Austin from 1984 until his retirement in 1999, he was a professor of mathematics (1962–1984) at Eindhoven University of Technology, located in Eindhoven, Netherlands.\n\nPassages:\n\n[Edsger W. Dijkstra]\nHe was a professor of mathematics at the Eindhoven University of Technology (1962–1984) and a research fellow at the Burroughs Corporation (1973–1984).\n\n[Eindhoven University of Technology]\nTU/e ) is a university of technology located in Eindhoven, Netherlands.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00328",
  "kind": "yes/no",
  "text": "Claim: The younger brother, who became king, of the princess that SS Principessa Mafalda was named after, reigned for 34 days.\n\nPassages:\n\n[Umberto II of Italy]\nUmberto II (Italian: \"Umberto Nicola Tommaso Giovanni Maria di Savoia\" ; 15 September 190418 March 1983), was the last King of Italy. He reigned for 34 days, from 9 May 1946 to 12 June 1946, although he had been \"de facto\" head of state since 1944, and was nicknamed the May King (Italian: Re di Maggio ).\n\n[SS Principessa Mafalda]\nNamed after Princess Mafalda of Savoy, second daughter of King Victor Emmanuel III, the ship entered NGI's South American service between Genoa and Buenos Aires in 1909.\n\n[Princess Mafalda of Savoy]\nPrincess Mafalda of Savoy (2 November 1902 – 27 August 1944) was the second daughter of King Victor Emmanuel III of Italy and his wife Elena of Montenegro. The future King Umberto II of Italy was her younger brother.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00329",
  "kind": "yes/no",
  "text": "Claim: Kurt Vonnegut was born in 1922 and published a book in 1985 by Delacorte Press.\n\nPassages:\n\n[Kurt Vonnegut]\nKurt Vonnegut Jr. ( ; November 11, 1922April 11, 2007) was an American writer.\n\n[Galápagos (novel)]\nIt was first published in 1985 by Delacorte Press.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00330",
  "kind": "yes/no",
  "text": "Claim: A sports group lost in the quarterfinals of the NCAA Tournament. They lost to the team that represented Santa Clara University that was founded in 1851. The losing sports group were defeated by San Diego State in the 2016 Diamond Head Classic.\n\nPassages:\n\n[2016 Diamond Head Classic]\nSan Diego State defeated San Francisco to win the tournament championship.\n\n[2016–17 San Francisco Dons men's basketball team]\nThey lost in the quarterfinals of the WCC Tournament to Santa Clara.\n\n[2016–17 Santa Clara Broncos men's basketball team]\nThe 2016–17 Santa Clara Broncos men's basketball team represented Santa Clara University during the 2016–17 NCAA Division I men's basketball season.\n\n[Santa Clara University]\nFounded in 1851, Santa Clara University is the oldest operating institution of higher learning in California, and has remained in its original location for 166 years.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00331",
  "kind": "yes/no",
  "text": "Claim: The daughter of the woman who recorded the song Stoney End co-wrote the teleplay for the first episode of \"Black Mirror\". She was born in 1976.\n\nPassages:\n\n[Rashida Jones]\nRashida Leah Jones (born February 25, 1976) is an American actress, producer, singer, and writer.\n\n[Peggy Lipton]\nLipton was married to the musician/producer Quincy Jones and is mother to their two daughters, Rashida Jones and Kidada Jones, who also became actresses.\n\n[Stoney End (song)]\nIt was originally recorded in 1968 by Peggy Lipton and her recording reached #121 on the U.S. \"Billboard\" Bubbling Under the Hot 100 chart.\n\n[Nosedive]\nMichael Schur and Rashida Jones wrote the teleplay for the episode, based on a story by series creator and showrunner Charlie Brooker, while Joe Wright acted as director.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00332",
  "kind": "yes/no",
  "text": "Claim: Chester C. Dillian coached at the school at which James C. Klotter was a history professor. He coached sports there for one year from 1929-1930. The college was chartered in 1829.\n\nPassages:\n\n[Chester Dillon]\nHe served as the head football coach at Dakota Wesleyan University (1915–1916), Simpson College (1916–1917), Howard College in Homewood, Alabama—now Samford University (1919, 1927–1928), Oshkosh State Normal School—now the University of Wisconsin–Oshkosh (1920), Georgetown College in Georgetown, Kentucky (1929–1930), and Jacksonville State Teachers College—now Jacksonville State University (1938–1939, 1945).\n\n[James C. Klotter]\nKlotter also is a history professor at Georgetown College and one of the co-authors of Kentucky's staple history book \"A New History of Kentucky\".\n\n[Georgetown College]\nChartered in 1829, Georgetown was the first Baptist college west of the Allegheny Mountains.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00333",
  "kind": "yes/no",
  "text": "Claim: The Good Design philosophy is associated with the Danish furniture manufacturer Hans Jørgensen Wegner whose style is often described as Organic Functionality.\n\nPassages:\n\n[Hans Wegner]\nHans Jørgensen Wegner, (April 2, 1914 – January 26, 2007), was a world-renowned Danish furniture designer. His style is often described as Organic Functionality, a modernist school with emphasis on functionality.\n\n[Good Design]\nNames associated with the movement include Charles and Ray Eames, László Moholy-Nagy and Hans Wegner,",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00334",
  "kind": "yes/no",
  "text": "Claim: The Wild came years before this film. The film starred Lake Bell.\n\nPassages:\n\n[Lake Bell]\nShe has starred in various television series, including \"Boston Legal\" (2004–2006), \"Surface\" (2005–2006), \"How to Make It in America\" (2010–2011) and \"Childrens Hospital\" (2008–2016), and in films including \"Over Her Dead Body\" (2008), \"What Happens in Vegas\" (2008), \"It's Complicated\" (2009), \"No Strings Attached\" (2011), \"Million Dollar Arm\" (2014) and \"The Secret Life of Pets\" (2016).\n\n[Million Dollar Arm]\nMillion Dollar Arm is a 2014 American biographical sports drama film directed by Craig Gillespie and produced by Walt Disney Pictures from a screenplay written by Thomas McCarthy.\n\n[The Wild]\nThe Wild is a 2006 American 3D computer animated comedy directed by animator Steve \"Spaz\" Williams, and written by Ed Decter, John J. Strauss, Mark Gibson and Philip Halprin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00335",
  "kind": "yes/no",
  "text": "Claim: American heavy metal band Metallica released the song co-written by Kirk Hammett in album Metallica that had five singles.\n\nPassages:\n\n[Enter Sandman]\n\"Enter Sandman\" is a song by American heavy metal band Metallica. Vocalist and rhythm guitarist Hetfield wrote the lyrics, which deal with the concept of a child's nightmares.\n\n[Metallica (album)]\n\"Metallica\" produced five singles that are considered to be among the band's best-known songs, which include \"Enter Sandman\", \"The Unforgiven\", \"Nothing Else Matters\", \"Wherever I May Roam\", and \"Sad but True\". \"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00336",
  "kind": "yes/no",
  "text": "Claim: Candace Flynn was voiced by the actress who achieved instant success on The Suite Life of Zack & Cody.\n\nPassages:\n\n[Candace Flynn]\nCandace Gertrude Flynn is a main character of the Disney Channel animated television series \"Phineas and Ferb\", voiced by Ashley Tisdale and created and designed by Dan Povenmire.\n\n[Ashley Tisdale]\nShe achieved mainstream success as Maddie Fitzpatrick in the Disney Channel series \"The Suite Life of Zack & Cody\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00337",
  "kind": "yes/no",
  "text": "Claim: Sophia Grace & Rosie featured a cover song on their Youtube channel. The song from is from an album released under the Columbia Records and Columbia Records labels.\n\nPassages:\n\n[Glory Days (Little Mix album)]\nIt was released on 18 November 2016, by Syco Music and Columbia Records.\n\n[Touch (Little Mix song)]\n\"Touch\" is a song by British girl group Little Mix. It was released as the second single from their studio album \"Glory Days\".\n\n[Sophia Grace &amp; Rosie]\nRosie has started a YouTube channel featuring her life and sang a cover of Little Mix's \"Touch\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00338",
  "kind": "yes/no",
  "text": "Claim: The place where glaciers in the continent that is home to the genus Riograndia, develop exclusively, is a mountain range. It extends through multiple countries southeast of Jacabamba.\n\nPassages:\n\n[List of glaciers in South America]\nGlaciers in South America develop exclusively on the Andes and are subject to the Andes various climatic regimes namely the Tropical Andes, Dry Andes and the Wet Andes.\n\n[Auqui]\nAwki lies southeast of Jacabamba.\n\n[Riograndia]\nRiograndia is a genus of tritheledontid cynodont from the Late Triassic of South America.\n\n[Andes]\nThe Andes or Andean Mountains (Spanish: \"Cordillera de los Andes\" ) are the longest continental mountain range in the world. The Andes extend from north to south through seven South American countries: Venezuela, Colombia, Ecuador, Peru, Bolivia, Argentina and Chile.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00339",
  "kind": "yes/no",
  "text": "Claim: Genesee Cream Ale is a cold fermented, alcohlic beverage produced by a facility located along the Genesee River.\n\nPassages:\n\n[Genesee Cream Ale]\nGenesee Cream Ale is a cold fermented, alcohlic beverage produced by the Genesee Brewing Company in Rochester, NY.\n\n[Genesee Brewing Company]\nGenesee Brewing Company is an American brewery located along the Genesee River in Rochester, New York.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00340",
  "kind": "yes/no",
  "text": "Claim: Ohio native William Gladstone Steel helped create Crater Lake National Park, where the lake is most famous for its deep blue color.\n\nPassages:\n\n[William Gladstone Steel]\nWilliam Gladstone Steel (September 7, 1854 – October 21, 1934), called the \"father of Crater Lake\", referring to the creation of Crater Lake National Park in Oregon, United States.\n\n[Crater Lake]\nIt is the main feature of Crater Lake National Park and is famous for its deep blue color and water clarity.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00341",
  "kind": "yes/no",
  "text": "Claim: The Grammy award winner for song for the year put out a 1971 album by the Carpenters and won an Academy Award for Best Original Song for A Star is Born.\n\nPassages:\n\n[Paul Williams (songwriter)]\nHe is perhaps best known for writing popular songs performed by a number of acts in the 1970s, including Three Dog Night's \"An Old Fashioned Love Song\" and \"Out in the Country\", Helen Reddy's \"You and Me Against the World\", David Bowie's \"Fill Your Heart\", and the Carpenters' \"We've Only Just Begun\" and \"Rainy Days and Mondays\", as well as for his contributions to films, such as writing the lyrics to the #1 chart-topping \"Evergreen\", the love theme from \"A Star Is Born\", starring Barbra Streisand, for which he won a Grammy for Song of the Year and an Academy Award for Best Original Song; and \"Rainbow Connection\" from \"The Muppet Movie\".\n\n[Let Me Be the One (The Carpenters song)]\n\"Let Me Be the One\" is a song written in 1971 by Roger Nichols and Paul Williams.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00342",
  "kind": "yes/no",
  "text": "Claim: Connetquot High School is a public high school in the city of Oakdale in New York.\n\nPassages:\n\n[Connetquot High School]\nConnetquot High School (CHS) is a public high school serving students from the communities of Bohemia, Sayville, West Sayville, Oakdale and Ronkonkoma in the ninth through twelfth grades located in Bohemia, New York and is part of the Connetquot Central School District.\n\n[Oakdale, New York]\nOakdale is a hamlet (and census-designated place) in Suffolk County, New York, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00343",
  "kind": "yes/no",
  "text": "Text: @rits_meg @freedomsenpai hot loli",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00344",
  "kind": "yes/no",
  "text": "Claim: The historian that described the Minoan civilization, and Margaret Mitchell were not both philosophical writers.\n\nPassages:\n\n[Minoan civilization]\nIt has been described as the earliest of its kind in Europe, with historian Will Durant calling the Minoans \"the first link in the European chain\".\n\n[Will Durant]\nWilliam James \"Will\" Durant ( ; November 5, 1885 – November 7, 1981) was an American writer, historian, and philosopher.\n\n[Margaret Mitchell]\nMargaret Munnerlyn Mitchell (November 8, 1900 – August 16, 1949) was an American author and journalist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00345",
  "kind": "yes/no",
  "text": "Claim: Heidi Brunner, a Swiss opera singer, played the role as Annio in Estates Theatre in Prague.\n\nPassages:\n\n[Heidi Brunner]\nHeidi Brunner (born 1966) is a Swiss opera singer. Among the roles she sang in Vienna were Adalgisa in \"Norma\", Annio in \"La clemenza di Tito\", and the title role in \"La Cenerentola\".\n\n[La clemenza di Tito]\nThe work premiered on 6 September 1791 at the Estates Theatre in Prague.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00346",
  "kind": "yes/no",
  "text": "Claim: Lewis Moran was murdered a week after the death of the hitman from the Australian city of Melbourne.\n\nPassages:\n\n[Lewis Moran]\nHis murder occurred one week after the funeral of fellow Melbourne underworld criminal and suspected hitman Andrew Veniamin.\n\n[Andrew Veniamin]\nAndrew \"Benji\" Veniamin (16 November 1975 – 23 March 2004) was an Australian criminal from Melbourne, Victoria, Australia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00347",
  "kind": "yes/no",
  "text": "Claim: This athlete won the 2004 BNP Paribas Masters – Singles title for the then record 3rd time. Both she and the 2008 Kremlin Cup – Women's Singles semi-finals winner have both played tennis professionally.\n\nPassages:\n\n[2008 Kremlin Cup – Women's Singles]\nElena Dementieva was the defending champion, but lost in the semifinals to Jelena Janković.\n\n[Jelena Janković]\nJelena Janković (Serbian Cyrillic: Јелена Јанковић, ] , born 28 February 1985) is a Serbian professional tennis player.\n\n[Marat Safin]\nMarat Mubinovich Safin (Russian: Мара́т Муби́нович Са́фин ; ] , Tatar: Марат Мөбин улы Сафин \"Marat Möbin uğlı Safin\" ; born 27 January 1980) is a Russian politician and retired professional tennis player.\n\n[2004 BNP Paribas Masters – Singles]\nMarat Safin won the title for the then record 3rd time, defeating Radek Štěpánek in the final in straight sets.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00348",
  "kind": "yes/no",
  "text": "Claim: Wikimedia Foundation runs the website surpassed by both Hudong.com and the encyclopedia that had the humorous hoax Baidu 10 Mythical Creatures.\n\nPassages:\n\n[Baidu Baike]\nIts test version was released on 20 April 2006, and within three weeks the encyclopedia had grown to more than 90,000 articles surpassing the number in Chinese Wikipedia.\n\n[Chinese Wikipedia]\nThe Chinese Wikipedia () is the (Standard) Chinese language edition of Wikipedia. It is run by the Wikimedia Foundation.\n\n[Baidu 10 Mythical Creatures]\nThe Baidu 10 Mythical Creatures (), alternatively Ten Baidu Deities, was initially a humorous hoax from the interactive encyclopedia Baidu Baike which became a popular and widespread Internet meme in the People's Republic of China in early 2009.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00349",
  "kind": "yes/no",
  "text": "Text: Let me guess, it has to be Charlotte Tilbury makeup. And if by chance you do take it off, use Charlotte Tilbury skincare https://t.co/0c2IfIpy8l",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 }
]
