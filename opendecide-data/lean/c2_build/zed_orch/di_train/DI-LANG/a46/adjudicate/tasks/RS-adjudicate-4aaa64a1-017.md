# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-017

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-017.json

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
  "aid": "a00850",
  "kind": "yes/no",
  "text": "Claim: Konami is the Japanese entertainment company founded in 1976 that released the game International Superstar Soccer 2.\n\nPassages:\n\n[International Superstar Soccer 2]\nInternational Superstar Soccer 2 (abbreviated as \"ISS2\") is a football video game in the International Superstar Soccer series by Konami.\n\n[Konami]\nKonami Holdings Corporation (Japanese: 株式会社コナミホールディングス , Hepburn: Kabushikigaisha Konami Hōrudingusu ) is a Japanese entertainment company.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00851",
  "kind": "yes/no",
  "text": "Claim: The movie co-directed by Lee Unkrich and \"Mary Poppins\" are not both made by the same company.\n\nPassages:\n\n[Lee Unkrich]\nAfter co-directing \"Monsters, Inc.\" and \"Finding Nemo\", Unkrich made his solo directorial debut with \"Toy Story 3\", for which he won the Academy Award for Best Animated Film in 2011.\n\n[Monsters, Inc.]\nMonsters, Inc. is a 2001 American computer-animated comedy film produced by Pixar Animation Studios and distributed by Walt Disney Pictures.\n\n[Mary Poppins (film)]\nMary Poppins is a 1964 American musical-fantasy film directed by Robert Stevenson and produced by Walt Disney, with songs written and composed by the Sherman Brothers.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00852",
  "kind": "yes/no",
  "text": "Claim: The birthdate of the American actress, television producer and director, singer/songwriter and author, who briefly appeared in Kids Incorporated and starred in Ghost Whisperer is February 21, 1979.\n\nPassages:\n\n[Ghost Whisperer (video game)]\nGhost Whisperer is a casual hidden-object mystery adventure game developed by Legacy Games for Microsoft Windows and Mac OS. The game is based on the CBS supernatural television drama Ghost Whisperer starring Melinda Gordon (Jennifer Love Hewitt).\n\n[Jennifer Love Hewitt]\nJennifer Love Hewitt (born February 21, 1979) is an American actress, television producer and director, singer/songwriter and author. Hewitt began her acting career as a child by appearing in television commercials and the Disney Channel series \"Kids Incorporated\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00853",
  "kind": "yes/no",
  "text": "Text: mentally I’m hiding in the walk-in",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
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
  "aid": "a00854",
  "kind": "yes/no",
  "text": "Tweet: Hey what's the weather like today? Am I going to need an umbrella?",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00855",
  "kind": "yes/no",
  "text": "Claim: In American football the air raid offense refers to an offensive scheme popularized by such coaches as Michael Charles Leach,, the head coach of the Washington State Cougars football team from 1983 to 1988.\n\nPassages:\n\n[Air raid offense]\nIn American football the air raid offense refers to an offensive scheme popularized by such coaches as Mike Leach, Hal Mumme, Sonny Dykes, and Tony Franklin during their tenures at Valdosta State, Kentucky, Oklahoma, Texas Tech, Louisiana Tech, and Washington State.\n\n[Mike Leach (American football coach)]\nMichael Charles Leach (born March 9, 1961) is an American college football coach.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00856",
  "kind": "yes/no",
  "text": "Claim: The day Southpark is most congested is the fourth Thursday of November.\n\nPassages:\n\n[Black Friday (shopping)]\nBlack Friday ( ) is the day following Thanksgiving Day in the United States (the fourth Thursday of November).\n\n[SouthPark Mall (Charlotte, North Carolina)]\nSouthPark is the most congested shopping area in the United States during Black Friday weekend.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00857",
  "kind": "yes/no",
  "text": "Claim: Robert Weissberg is a political scientist and author. The magazine he writes for ranked the company, headquartered at the Port Plaza Mall, as number 81 in 2016.\n\nPassages:\n\n[Schreiber Foods]\nWith more than $5 billion in annual sales, Forbes ranked Schreiber Foods as the 81st largest private employer in 2016.\n\n[Port Plaza Mall]\nThe mall property was razed during the 1st half of 2012 as part of a redevelopment project; the headquarters of Schreiber Foods now stands on the main mall footprint.\n\n[Robert Weissberg]\nWeissberg has also written for magazines such as \"Forbes,\" \"Society\", and \"The Weekly Standard\".\n\n[Forbes]\nPublished bi-weekly, it features original articles on finance, industry, investing, and marketing topics.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00858",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "every date I go on I get a little scared will be phone swap",
   "I am not afraid that I will be on the show phone swap while I go on a for date"
  ],
  "human_label": "every date I go on I get a little scared will be phone swap",
  "read_1": {
   "answer": "I am not afraid that I will be on the show phone swap while I go on a for date",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "I am not afraid that I will be on the show phone swap while I go on a for date",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00859",
  "kind": "yes/no",
  "text": "Claim: The city in which Benton County State Bank Building is situated had a total population of 54,462 as of the 2010 United States Census.\n\nPassages:\n\n[Benton County State Bank Building]\nThe Benton County State Bank Building, also known as The Madison Building, located in Corvallis, Oregon, is listed on the National Register of Historic Places.\n\n[Corvallis, Oregon]\nAs of the 2010 United States Census, the population was 54,462.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00860",
  "kind": "yes/no",
  "text": "Claim: The Western Conference is the conference that has the most valuable NBA franchise according to Forbes.\n\nPassages:\n\n[2008 NBA Playoffs]\nThe tournament concluded with the Eastern Conference champion Boston Celtics defeating the Western Conference champion Los Angeles Lakers 4 games to 2 in the NBA Finals.\n\n[Los Angeles Lakers]\nAs of 2017, the Lakers are the second most valuable franchise in the NBA according to \"Forbes\", having an estimated value of $3.0 billion.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00861",
  "kind": "yes/no",
  "text": "Claim: The man that composed the opera Irrelohe was also a teacher. The composer, who American Violinist Tim Fain is best known for working with, was not.\n\nPassages:\n\n[Philip Glass]\nPhilip Morris Glass (born January 31, 1937) is an American composer.\n\n[Irrelohe]\nIrrelohe is an opera in three acts by the Austrian composer Franz Schreker, libretto by the composer.\n\n[Tim Fain]\nTim Fain is an American violinist, perhaps best known for his performances in the movie \"Black Swan\" and his work with American composer Philip Glass.\n\n[Franz Schreker]\nFranz Schreker (originally \"Schrecker\"; 23 March 1878, Monaco – 21 March 1934, Berlin) was an Austrian composer, conductor, teacher and administrator.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00862",
  "kind": "yes/no",
  "text": "Claim: The area where Adenocarpus viscosus is a dominant shrub is located in Spain's Canary Islands. So is the park where you would find the plant Echium wildpretii subsp. trichosiphon.\n\nPassages:\n\n[Teide National Park]\nTeide National Park (Spanish: \"Parque nacional del Teide\" , ] ) is a national park located in Tenerife (Canary Islands, Spain).\n\n[Adenocarpus viscosus]\nIt can be found above 1800 m on two of the islands, La Palma in Caldera de Tabouriente and Tenerife where it is a dominant shrub in Teide National Park and occurs in parts of Corona Forestal Nature Park and Reserva Especial de las Palomas.\n\n[Caldera de Taburiente National Park]\nCaldera de Taburiente National Park (Spanish: \"Parque Nacional de la Caldera de Taburiente\" ) is large geological feature on the island of La Palma, Canary Islands, Spain.\n\n[Echium wildpretii subsp. trichosiphon]\nEchium wildpretii\" subsp.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00863",
  "kind": "yes/no",
  "text": "Text: ITS COMING HOOOOOME",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00864",
  "kind": "yes/no",
  "text": "Claim: In the 28th season a Spanish rally driver won the racing series which was competed in by Harri Rovanperä from the 1990's to the 2000's.\n\nPassages:\n\n[2000 World Rally Championship]\nThe 2000 World Rally Championship was the 28th season of the FIA World Rally Championship.\n\n[Harri Rovanperä]\nHe drove for SEAT (1997–00), Peugeot (2001–04), Mitsubishi (2005) and Red Bull Škoda Team (2006).\n\n[Carlos Sainz]\nCarlos Sainz Cenamor (born 12 April 1962 in Madrid, Spain) is a Spanish rally driver.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00865",
  "kind": "yes/no",
  "text": "Claim: Angellika Morton has done photoshoots for a retailer of women's clothing, shoes and fashion accessories. It is located in an open-air shopping center which opened in September 2007.\n\nPassages:\n\n[Talbots]\nTalbots is an American specialty retailer and direct marketer of women's clothing, shoes and fashion accessories.\n\n[Angellika Morton]\nShe has done photo shoots for Talbots, Chatherines, Lane Bryant, Evans, Ulla Popken, Just My Size and others.\n\n[The Shops at Wisconsin Place]\nThe Shops at Wisconsin Place is an open-air shopping center that is part of the mixed-use Wisconsin Place complex, located in Chevy Chase, Maryland, located on the site of a former Woodward & Lothrop department store, which was converted to Hecht's in 1995 and closed in 2005. The Shops are anchored by Maryland's second Bloomingdale's, which opened on September 27, 2007, and Whole Foods Market, which opened on May 18, 2010.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00866",
  "kind": "yes/no",
  "text": "Claim: Verona directed the 1979 American drama film that starred the actress who won the Golden Globe Award for Best Supporting Actress for \"Psycho\".\n\nPassages:\n\n[Boardwalk (film)]\nBoardwalk is a 1979 American drama film written by Stephen Verona and Leigh Chapman and directed by Verona.\n\n[Janet Leigh]\nShe is best remembered for her performance in \"Psycho\", for which she was awarded the Golden Globe Award for Best Supporting Actress and received an Academy Award nomination.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00867",
  "kind": "yes/no",
  "text": "Claim: Robert Lewis \"Bob\" Pruett produced many high-profile National Football League players, including a wide reciver that holds the 2007 NFL record for single-season touchdown reception.\n\nPassages:\n\n[Randy Moss]\nRandy Gene Moss (born February 13, 1977) is a former American football wide receiver who played 14 seasons in the National Football League (NFL). He holds the NFL single-season touchdown reception record (23 in 2007), the NFL single-season touchdown reception record for a rookie (17 in 1998), and is second on the NFL all-time regular season touchdown reception list with 156.\n\n[Bob Pruett]\nRobert Lewis \"Bob\" Pruett (born June 20, 1943) is a former American football player and coach. Pruett has coached many high-profile National Football League players, including Randy Moss, Chad Pennington, and Byron Leftwich.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00868",
  "kind": "yes/no",
  "text": "Claim: A breed the of dog was developed in New London, Wisconsin. That breed was derived before the Estonian Hound.\n\nPassages:\n\n[New London, Wisconsin]\nThe American Water Spaniel was developed as a registered breed by F. J. Pfeifer of New London.\n\n[American Water Spaniel]\nThe breed was saved by Dr. Fred J. Pfeifer, who set up the breed club and standard, and whose work led to recognition for the breed by the United Kennel Club, and later, the American Kennel Club.\n\n[Estonian Hound]\nIt was bred in 1947 when the Soviet Union's national economy ministry decided that every country in the Union must have its own dog breed.\n\n[English Water Spaniel]\nThe English Water Spaniel is a breed of dog that has been extinct since the first part of the 20th century, with the last specimen seen in the 1930s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00869",
  "kind": "yes/no",
  "text": "Claim: The director of August 32nd on Earth has won more Canadian Screen Awards than another director. This other man directed and acted in From the Manger to the Cross.\n\nPassages:\n\n[August 32nd on Earth]\nAugust 32nd on Earth (French: Un 32 août sur terre , and also known as \"32nd Day of August on Earth\") is a 1998 Canadian drama film directed by Denis Villeneuve.\n\n[From the Manger to the Cross]\nDirected by Sidney Olcott who also appeared in the film, actress and screenwriter Gene Gauntier wrote the script and portrayed the Virgin Mary.\n\n[Denis Villeneuve]\nDenis Villeneuve (] ; born October 3, 1967) is a French Canadian film director and writer. He is a four-time recipient of the Canadian Screen Award (formerly Genie Award) for Best Direction, for \"Maelström\" in 2001, \"Polytechnique\" in 2010, \"Incendies\" in 2011, and \"Enemy\" in 2013.\n\n[Sidney Olcott]\nSidney Olcott (September 20, 1872 – December 16, 1949) was a Canadian-born film producer, director, actor and screenwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00870",
  "kind": "yes/no",
  "text": "Claim: Besides the song of the same name as a band's album that Radiodread is a cover of, the same band also recorded \"Lucky\" in 1995. SubAudible Hum has often been compared to this first band.\n\nPassages:\n\n[Radiodread]\nRadiodread is a 2006 tribute album by the Easy Star All-Stars that covers Radiohead's 1997 album \"OK Computer\" in reggae, ska and dub styles.\n\n[SubAudible Hum]\nOften compared to Radiohead they are active on the live circuit, particularly in their home town, they have released three albums, one of which was nominated for the J Award; \"In Time For Spring, On Came The Snow\".\n\n[No Surprises]\n\"No Surprises\" is a song by the English alternative rock band Radiohead, released as the third and final single from their third studio album \"OK Computer\" (1997) on 12 January 1998.\n\n[OK Computer]\nOther than the song \"Lucky\", which was recorded in 1995, Radiohead recorded the album in Oxfordshire and Bath between 1996 and early 1997, mostly in the historic mansion St Catherine's Court.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00871",
  "kind": "yes/no",
  "text": "Claim: Jeff Alexander Leach who starred in HBO Games of Thrones, is an English actor, writer and comedian. He was born 12 February 1984.\n\nPassages:\n\n[Nell Williams]\nIn 2015 she portrayed a younger version of Cersei Lannister (portrayed by Lena Headey as an adult) in flashback sequences of the opening episode of Season 5 of the HBO series \"Game of Thrones\".\n\n[Cersei Lannister]\nCersei Lannister is a fictional character in the \"A Song of Ice and Fire\" series of fantasy novels by American author George R. R. Martin, and its television adaptation \"Game of Thrones\", where she is portrayed by Lena Headey.\n\n[Jeff Leach]\nHe is most well known for appearing in feature films \"The Smoke\" as Dean and \"London Town\" as Ronnie.\n\n[London Town (2016 film)]\nThe film stars Daniel Huttlestone, Dougray Scott, Natascha McElhone, Nell Williams, and Jonathan Rhys Meyers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00872",
  "kind": "yes/no",
  "text": "Claim: The present observation of Greenery as a holiday stems from the celebration of the birthday of an Asian emperor whose name means abundant benevolence in English.\n\nPassages:\n\n[Greenery Day]\nThe present observation of Greenery Day (みどりの日 , Midori no Hi ) as a national holiday in Japan stems from the celebration of the Emperor Shōwa's birthday on April 29 every year during the Shōwa era.\n\n[Hirohito]\nThe name Hirohito means \"abundant benevolence\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00873",
  "kind": "yes/no",
  "text": "Text: The Suicide Squad felt like a remake of the Watchmen movie where they actually kept the giant squid.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00874",
  "kind": "yes/no",
  "text": "Claim: This British television series Household Words was adapted from one of the better-known novels of a 19th-century writer and was first published in what magazine.\n\nPassages:\n\n[Cranford (novel)]\nCranford is one of the better-known novels of the 19th-century English writer Elizabeth Gaskell. It was first published, irregularly, in eight instalments, between December 1851 and May 1853, in the magazine \"Household Words\", which was edited by Charles Dickens.\n\n[Cranford (TV series)]\nCranford is a British television series directed by Simon Curtis and Steve Hudson. The teleplay by Heidi Thomas was adapted from three novellas by Elizabeth Gaskell published between 1849 and 1858: \"Cranford\", \"My Lady Ludlow\", and \"Mr Harrison's Confessions\". \"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00875",
  "kind": "yes/no",
  "text": "Post: how old were u when u found out omaha steaks wasn't a restaurant",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00876",
  "kind": "yes/no",
  "text": "Claim: Cross Damon resembles the hero of a book by a writer who won the Nobel Prize in Literature in 1957.\n\nPassages:\n\n[Albert Camus]\nHe won the Nobel Prize in Literature in 1957.\n\n[Cross Damon]\nIn many ways, Cross Damon resembles Meursault, the hero of Albert Camus novel \"The Stranger\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00877",
  "kind": "yes/no",
  "text": "Claim: A certain dog breed is NOT recognized by the Fédération Cynologique Internationale (the Fédération Cynologique Internationale), the native Korean dog Nureongi or the Taigan. This dog breed hunts in the Salburun.\n\nPassages:\n\n[Nureongi]\nLike native Korean dogs such as the Korean Jindo, Korean Yellow spitzes are medium-sized spitz, but with greater musculature and distinctive coat patterns.\n\n[Salburun]\nSalburun (Kyrgyz : Салбуурун) is a traditional kind of hunt in Kyrghyzstan and Central Asia, involving falconry, archery and sometimes mounted archery, as well as hunting with Taigan.\n\n[Taigan]\nThe Taigan (Kyrgyz: Тайган ) also known as Kyrgyzdyn Taighany (Kyrgyzskaya Borzaya Taigan in Russian) is a sighthound breed from Kyrgyzstan, which is not yet recognized by the FCI, but is recognized by a number of kennel clubs on national level.\n\n[Korean Jindo]\nThe Jindo breed became recognized by the United Kennel Club on January 1, 1998 and by the Fédération Cynologique Internationale in 2005.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00878",
  "kind": "yes/no",
  "text": "Claim: Jaime Aube has one career win at the North Oxford Plains Speedway.\n\nPassages:\n\n[Jamie Aube]\nJamie Aube (born August 4, 1953 in Charlotte, Vermont) is an American stock car racing driver. He also has one career win in the NASCAR Busch Series, at Oxford Plains Speedway in 1987.\n\n[Oxford Plains Speedway]\nOxford Plains Speedway is a 3/8 mile racetrack located in Oxford, Maine.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00879",
  "kind": "yes/no",
  "text": "Claim: On July 31, 1912, Nobel Prize winner in Economic Sciences, Milton Friedman, founded EdChoice.\n\nPassages:\n\n[EdChoice]\nIt was founded in 1996 by Nobel laureate Milton Friedman and his wife, economist Rose Director Friedman.\n\n[Milton Friedman]\nMilton Friedman ( ; July 31, 1912 – November 16, 2006) was an American economist who received the 1976 Nobel Memorial Prize in Economic Sciences for his research on consumption analysis, monetary history and theory, and the complexity of stabilization policy.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.97
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00880",
  "kind": "yes/no",
  "text": "Claim: The current state of Tennessee is the location of unrecognized and autonomous territory in the United States created in 1784 that was led by David Campbell.\n\nPassages:\n\n[State of Franklin]\nThe State of Franklin (also the Free Republic of Franklin or the State of Frankland) was an unrecognized and autonomous territory located in what is today eastern Tennessee, United States.\n\n[David Campbell (judge)]\nDavid Campbell (1750–1812) was a prominent politician and judge who was a member of the North Carolina state assembly, a leader in the State of Franklin, and a judge in the North Carolina Superior Court, Southwest Territory, and state of Tennessee.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00881",
  "kind": "yes/no",
  "text": "Claim: The American actress voices a character on the show that features a character named Boomhauer. She also wrote the song Tiggy is famous for remixing.\n\nPassages:\n\n[Sandy Fox]\nSandra Marie Fox (born July 13, 1963) is an American voice actress, singer and dancer, who has had numerous roles in various animated cartoon, anime and video games.\n\n[King of the Hill]\nKing of the Hill is an American animated sitcom created by Mike Judge and Greg Daniels that ran from January 12, 1997 to September 13, 2009 on Fox.\n\n[Boomhauer]\nJeffrey Dexter \"Jeff\" Boomhauer III, commonly referred to as Boomhauer, is a fictional character in the Fox animated series \"King of the Hill\".\n\n[Tiggy]\nShe is perhaps best known for her remix of the Sandy Fox song \"Freckles\" in \"\", originally the English version of the song \"Sobakasu\" by Judy and Mary from the anime \"Rurouni Kenshin\" and she's also popular in parts of Southeast Asia with the song \"Why\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00882",
  "kind": "yes/no",
  "text": "Claim: The Sumerians invented the type of script used in written autographs.\n\nPassages:\n\n[Cuneiform script]\nCuneiform script ( or or ), one of the earliest systems of writing, was invented by the Sumerians.\n\n[Autograph (Assyriology)]\nAn autograph in Assyriology is the hand-copy of a cuneiform clay-tablet.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00883",
  "kind": "yes/no",
  "text": "Claim: The actor that has performed as Inspector David Charles Abell in a Les Misérables production has won the Laurence Olivier Award for Best Actor in a musical three times. This actor also starred in the film The Caterpillar Wish.\n\nPassages:\n\n[Philip Quast]\nPhilip Mark Quast (born 30 July 1957) is an Australian actor and singer. He has won the Laurence Olivier Award for Best Actor in a Musical three times, the most of any actor to date.\n\n[The Caterpillar Wish]\nThe Caterpillar Wish (also known as Caterpillar Wish) is a 2006 Australian coming-of-age film, directed by Sandra Sciberras and starring and ensemble cast including Victoria Thaine, Susie Porter and Philip Quast.\n\n[Les Misérables: The Dream Cast in Concert]\nThe 10th Anniversary cast stars Colm Wilkinson as Jean Valjean, Philip Quast as Inspector Javert, Michael Ball as Marius Pontmercy, Lea Salonga as Éponine, Judy Kuhn as Cosette, Ruthie Henshall as Fantine, Michael Maguire as Enjolras, Alun Armstrong as Thénardier, Jenny Galloway as Madame Thénardier, Adam Searles as Gavroche, Hannah Chick as Young Cosette, and several others, and was directed by John Caird. The performers were chosen from the London, Broadway and Australian productions of the show and the Royal Philharmonic Orchestra was conducted by David Charles Abell.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
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
  "aid": "a00884",
  "kind": "yes/no",
  "text": "Claim: The American star of Neal Dodson's \"Jonathan\", played a professional getaway driver in \"Baby Driver\".\n\nPassages:\n\n[Neal Dodson]\nNeal executive produced \"Another Cinderella Story\" staring Selena Gomez and Jane Lynch, \"Banshee Chapter\" starring Katia Winter, \"\"Hollidaysburg\"\" starring Rachel Keller, \"\"Jonathan\"\" starring Ansel Elgort, \"\"Love On A Limb\"\" starring Ashley Williams (actress) and Marilu Henner, \"Never Here\" starring Mireille Enos and Sam Shepard, and \"\"Periods\"\" as well as co-producing \"Hateship, Loveship\" starring Kristin Wiig.\n\n[Baby Driver]\nThe plot follows Baby, a young getaway driver and music lover who must work for a kingpin.\n\n[Ansel Elgort]\nAs a film actor, he played Tommy Ross in the horror film \"Carrie\" (2013), Caleb Prior in \"The Divergent Series \" franchise, Augustus Waters in the romantic teen drama \"The Fault in Our Stars\" (2014), and the title character in Edgar Wright's action thriller \"Baby Driver\" (2017).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00885",
  "kind": "yes/no",
  "text": "Claim: An American rock band released My Animal. This band has more studio albums than the English band whose second album is Rispah.\n\nPassages:\n\n[The Invisible (band)]\nTheir self-titled debut album, released on 9 March 2009, was nominated for the Mercury Prize and selected as critics choice for iTunes album of the year.\n\n[Rispah]\nRispah is the second album by the English band The Invisible.\n\n[Boy Hits Car]\nBoy Hits Car released their 5th studio album \"All That Led Us Here\" in May 2014 and are following it up with a European tour.\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00886",
  "kind": "yes/no",
  "text": "Claim: The BBC drama Silk would be referenced in the biographical television film, Hancock and Joan.\n\nPassages:\n\n[Maxine Peake]\nShe has since played Veronica Ball in Channel 4's Manchester-based comedy drama series \"Shameless\", barrister Martha Costello in the BBC legal drama \"Silk\" and Grace Middleton in \"The Village\".\n\n[Hancock and Joan]\nHancock and Joan is a 2008 British biographical television film based on the affair between the comedian Tony Hancock and Joan Le Mesurier, the third wife of actor John Le Mesurier.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00887",
  "kind": "yes/no",
  "text": "Claim: Keith County in an American state is located over the 174000 the High Plains. This area supplies water to the Texas High Plains AVA. Sherman Elementary School is located in this state.\n\nPassages:\n\n[Ogallala, Nebraska]\nOgallala is a city in Keith County, Nebraska, United States.\n\n[Texas High Plains AVA]\nThe Texas plains can be extremely dry, so most vineyards are irrigated with water from the Ogallala Aquifer.\n\n[Sherman Elementary School]\nSherman Elementary School is located at 5618 North 14th Avenue in East Omaha, Nebraska, United States.\n\n[Ogallala Aquifer]\nThe Ogallala Aquifer is a shallow water table aquifer surrounded by sand, silt, clay and gravel located beneath the Great Plains in the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00888",
  "kind": "yes/no",
  "text": "Claim: In this religion, where Mehet-Weret is a godess of the sky, a citizen would be weighted against the feather of truth to decide if they where worthy of damnation and would face the torment in the lake of fire.\n\nPassages:\n\n[Damnation]\nIn Ancient Egyptian religious tradition, citizens would recite the 42 negative confessions of Maat as their heart was weighed against the feather of truth.\n\n[Mehet-Weret]\nMehet-Weret \"(mḥ.t-wr.t)\" is a goddess of the sky in Ancient Egyptian religion. Her name means \"Great Flood\".\n\n[Ancient Egyptian religion]\nAncient Egyptian religion was a complex system of polytheistic beliefs and rituals which were an integral part of ancient Egyptian society.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00889",
  "kind": "yes/no",
  "text": "Claim: Blake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro whose role was portrayed by John Forsythe, and also appeared as a guest on several talk and variety shows and as a panelist on quiz formatted game shows.\n\nPassages:\n\n[John Forsythe]\nHe also appeared as a guest on several talk and variety shows and as a panelist on numerous game shows.\n\n[Blake Carrington]\nBlake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro. The role was portrayed by John Forsythe from the first episode of the series in 1981 until its finale in 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00890",
  "kind": "yes/no",
  "text": "Claim: Niño was the nickname of the player who played his final season for the 2016 Miami Dolphins before dying in an accident.\n\nPassages:\n\n[2016 Miami Marlins season]\nThis also marked José Fernández's final season as he died in a boating accident on September 25.\n\n[José Fernández (pitcher)]\nHe was affectionately known as \"Niño\" by his teammates and fans due to the youthful exuberance with which he played the game of baseball.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00891",
  "kind": "yes/no",
  "text": "Claim: The namesake of a small island in the Town of New York was born in 1599.\n\nPassages:\n\n[Lion Gardiner]\nLion Gardiner (1599–1663), an early English settler and soldier in the New World, founded the first English settlement in what became the state of New York on Long Island. His legacy includes Gardiners Island, which is held by his descendants.\n\n[Gardiners Island]\nGardiner's Island is a small island in the Town of East Hampton, New York, in Eastern Suffolk County.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00892",
  "kind": "yes/no",
  "text": "Claim: The winner of the 2014 French Open – Mixed Doubles and another female athlete are both tennis players. This other athlete won the singles title at the 1979 Romika Cup.\n\nPassages:\n\n[Manuel Orantes]\nManuel Orantes Corral (] ; born 6 February 1949) is a former tennis player who was active in the 1970s and 1980s.\n\n[Anna-Lena Grönefeld]\nAnna-Lena Grönefeld (born 4 June 1985) is a German tennis player.\n\n[1979 Romika Cup]\nFirst-seeded Manuel Orantes won the singles title.\n\n[2014 French Open – Mixed Doubles]\nHradecká played alongside Mariusz Fyrstenberg but lost in the second round to the eventual champions Anna-Lena Grönefeld and Jean-Julien Rojer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00893",
  "kind": "yes/no",
  "text": "Claim: David Michael Draiman was born before the vocalist of the song Make Me Smile.\n\nPassages:\n\n[Make Me Smile]\n\"Make Me Smile\" is a song written by James Pankow for the rock band Chicago with the band's guitarist, Terry Kath, on lead vocals.\n\n[David Draiman]\nDavid Michael Draiman (born March 13, 1973) is an American songwriter and the vocalist for the band Disturbed as well as for the band Device.\n\n[Terry Kath]\nTerry Alan Kath (January 31, 1946 – January 23, 1978) was an American musician and songwriter, best known as the original guitarist, one of the lead singers and founding members of the rock band Chicago.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00894",
  "kind": "yes/no",
  "text": "Claim: Garry Marshall directed a film. The film costarred the star of the film Open Water 2: Adrift.\n\nPassages:\n\n[Eric Dane]\nAfter appearing in television roles throughout the 2000s such as \"Charmed\", he became known for playing Dr. Mark Sloan on the medical drama television series \"Grey's Anatomy\", as well as films, co-starring in \"Marley & Me\" (2008), \"Valentine's Day\" (2010), and \"Burlesque\" (2010).\n\n[Open Water 2: Adrift]\nPromotional posters claim the film is based on actual events.\n\n[Valentine's Day (2010 film)]\nValentine's Day is a 2010 American romantic comedy film directed by Garry Marshall.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00895",
  "kind": "yes/no",
  "text": "Claim: Singers Kim Tae-yeon and the Irish artist who released the EP \"The First Collage\", have both appeared in group bands.\n\nPassages:\n\n[Yang Yo-seob]\nHe is the main vocalist of the boy group Highlight.\n\n[The First Collage]\nThe First Collage is the debut and first EP by Yang Yo-seob, released on November 26, 2012.\n\n[Kim Tae-yeon]\nShe had been a trainee at S.M. Entertainment's Starlight Academy during her middle school years before debuting as a member of the agency's girl group, Girls' Generation, in 2007.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
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
  "aid": "a00896",
  "kind": "yes/no",
  "text": "Tweet: Yesterday a stranger went into detail telling me how much better her new man is compared to her ex husband at oral sex, and it was a weird conversation but I guess I’m happy for her. New Year new mens.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00897",
  "kind": "yes/no",
  "text": "Text: Jeopardy had an “Internet Slang” category and I finally know the answers to some of these.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00898",
  "kind": "yes/no",
  "text": "Claim: Team Sleep's Chino Moreno was featured on the internet-only \"Tempest\" video.\n\nPassages:\n\n[Tempest (Deftones song)]\n\"Tempest\" is the second single by Sacramento, California-based alternative metal band Deftones, from their seventh studio album, \"Koi No Yokan\". The song debuted on PureVolume's official website on October 3, 2012 along with a video featuring band members Chino Moreno and Sergio Vega giving some insight regarding the track.\n\n[Chino Moreno]\nHe is also a member of the side-project groups Team Sleep, Crosses, Saudade, and Palms.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00899",
  "kind": "yes/no",
  "text": "Post: Just got in, how’d Liverpool get on?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 }
]
