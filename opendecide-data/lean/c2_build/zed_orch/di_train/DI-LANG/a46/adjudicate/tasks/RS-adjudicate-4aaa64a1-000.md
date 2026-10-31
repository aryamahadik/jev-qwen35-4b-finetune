# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-000.json

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
  "aid": "a00000",
  "kind": "yes/no",
  "text": "Claim: The film, in which Phil Harris voices the bear, stars more animals than The Lone Ranger. Raimond Aumann has the same nickname as this bear.\n\nPassages:\n\n[The Jungle Book (1967 film)]\nThe Jungle Book is a 1967 American animated musical adventure film produced by Walt Disney Productions. The plot follows Mowgli, a feral child raised in the Indian jungle by wolves, as his friends Bagheera the panther and Baloo the bear try to convince him to leave the jungle before the evil tiger Shere Khan arrives.\n\n[Raimond Aumann]\nHis nickname is Balu (Germanized version of Baloo the bear in the Jungle Book).\n\n[The Lone Ranger (2013 film)]\nThe Lone Ranger is a 2013 American western action film directed by Gore Verbinski from a screenplay written by Justin Haythe, Ted Elliott and Terry Rossio. Based on the radio series of the same name, the film stars Johnny Depp as Tonto, the narrator of the events, and Armie Hammer as John Reid, the Lone Ranger. It relates Tonto's memories of the duo's earliest efforts to subdue local villainy and bring justice to the American Old West. William Fichtner, Barry Pepper, Ruth Wilson, James Badge Dale, Tom Wilkinson and Helena Bonham Carter also are featured in supporting roles. It is the first theatrical film featuring the Lone Ranger and Tonto characters in more than 32 years.\n\n[Phil Harris]\nHe played Baloo the bear in \"The Jungle Book\" (1967), Thomas O'Malley in \"The Aristocats\" (1970), and Little John in \"Robin Hood\" (1973).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00001",
  "kind": "yes/no",
  "text": "Claim: The Garrick Club is a gentlemen's club in the heart of London founded in 1831, since its conception has catered to members such as English actor and theatre manager Sir Herbert Beerbohm Tree, that died on 2 July 1917.\n\nPassages:\n\n[Garrick Club]\nIt is one of the oldest, most highly esteemed and most exclusive members' clubs in the world and since its conception has catered to members such as Charles Kean, Henry Irving, Herbert Beerbohm Tree, Arthur Sullivan, Laurence Olivier and John Gielgud.\n\n[Herbert Beerbohm Tree]\nSir Herbert Beerbohm Tree (17 December 1852 – 2 July 1917) was an English actor and theatre manager.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00002",
  "kind": "yes/no",
  "text": "Claim: The man unseated by Rick Galindo and Julian Castro are democratic and not Republican.\n\nPassages:\n\n[Philip Cortez]\nPhilip A. Cortez (born July 7, 1978) is a Democratic member of the Texas House of Representatives.\n\n[Julian Castro]\nJulián Castro ( , ] ; born September 16, 1974) is an American Democratic politician who served as the 16th United States Secretary of Housing and Urban Development under President Barack Obama from 2014 to 2017.\n\n[Rick Galindo]\nHe narrowly unseated the one-term incumbent Democrat Philip Cortez in the November 4, 2014 general election.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00003",
  "kind": "yes/no",
  "text": "Claim: Dan Smith's song reached as low as number 5 on the US \"Billboard\" Hot 100 chart in 2013.\n\nPassages:\n\n[Dan Smith (singer)]\nDaniel Campbell \"Dan\" Smith (born 14 July 1986) is a British singer-songwriter and record producer. He is the lead singer, primary songwriter. The band formed in 2010 and gained mass popularity in 2013 when the song \"Pompeii\" was released.\n\n[Pompeii (song)]\nThe song was released as the album's fourth single on 12 January 2013. It reached number 2 in the UK Singles Chart, number 4 in Australian ARIA Chart, and number 5 on the US \"Billboard\" Hot 100 and number one on the Alternative Songs chart.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00004",
  "kind": "yes/no",
  "text": "Claim: The chorus of \"On the Radio\" by Regina Spektor contains references to the love song \"November Rain\" by Guns N' Roses, an American hard rock band.\n\nPassages:\n\n[November Rain]\n\"November Rain\" is a power ballad by the American hard rock band Guns N' Roses.\n\n[On the Radio (Regina Spektor song)]\nThe chorus contains references to the song \"November Rain\" by Guns N' Roses.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00005",
  "kind": "yes/no",
  "text": "Claim: This series developer created T-Dog on the Walking Dead. He is the Hungarian-born US film director renowned for adapting Stephen King novellas to the screen, including The Mist and The Green Mile.\n\nPassages:\n\n[The Mist (film)]\nThe film was written and directed by Frank Darabont.\n\n[T-Dog (The Walking Dead)]\n\"He was created by series developer Frank Darabont and portrayed by IronE Singleton.\n\n[Frank Darabont]\nAs a director he is known for his film adaptations of Stephen King novellas and novels such as \"The Shawshank Redemption\", \"The Green Mile\", and \"The Mist\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00006",
  "kind": "yes/no",
  "text": "Claim: Robert Kenneth Kraft, is an American businessman, he's the chairman and chief executive officer of the Kraft Group, LLC, a group of privately held companies in the professional sports, manufacturing, and real estate development industries doing business in 90 countries, and founded in 1998.\n\nPassages:\n\n[Robert Kraft]\nHe is the chairman and chief executive officer of the Kraft Group, a diversified holding company with assets in paper and packaging, sports and entertainment, real estate development and a private equity portfolio.\n\n[Kraft Group]\nFounded in 1998 by American businessman Robert Kraft as a holding company, it is based in Foxborough, Massachusetts and comprises the following companies:",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00007",
  "kind": "yes/no",
  "text": "Claim: Steven Jackson, an American running back, played for Oregon State and was coached by Paul Boudreau.\n\nPassages:\n\n[Steven Jackson]\nSteven Rashad Jackson (born July 22, 1983) is a former American football running back.\n\n[Paul Boudreau]\nPaul T. Boudreau (born December 30, 1949) is an American football coach who last served as offensive line coach for the Los Angeles Rams of the National Football League (NFL). Boudreau’s stellar offensive lines over the years have helped pave the way for five running backs to top the 10,000-yard career rushing mark, including Barry Sanders, Curtis Martin, Thurman Thomas, Fred Taylor and Steven Jackson.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00008",
  "kind": "yes/no",
  "text": "Claim: The inventor of the Maxim Gun issued 1.9 million shares to Nathan Rothschild.\n\nPassages:\n\n[Maxim Nordenfelt Guns and Ammunition Company]\nThe Maxim-Nordenfelt Guns and Ammunition Company was the result of a takeover by Hiram Maxim of Thorsten Nordenfelt's Nordenfelt Guns and Ammunition Company in 1888. Rothschild issued £1.9 million of shares to finance the merger. Nathan Rothschild retained a substantial shareholding in the new Maxim-Nordenfelt combine and ‘exerted a direct influence over its management’.\n\n[Hiram Maxim]\nHe was the inventor of the Maxim Gun – the first portable, fully automatic machine gun – and held patents on mechanical devices such as a mousetrap, hair-curling irons, and steam pumps.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00009",
  "kind": "yes/no",
  "text": "Claim: Emil Scaria created the role of Gurnemanz in an opera that has more acts than Manon by Massenet.\n\nPassages:\n\n[Manon]\nManon (] ) is an \"opéra comique\" in five acts by Jules Massenet to a French libretto by Henri Meilhac and Philippe Gille, based on the 1731 novel \"L’histoire du chevalier des Grieux et de Manon Lescaut\" by the Abbé Prévost.\n\n[Parsifal]\nParsifal (WWV 111) is an opera in three acts by German composer Richard Wagner.\n\n[Emil Scaria]\nIn 1882 he created the role of Gurnemanz in \"Parsifal\" for Richard Wagner at Bayreuth.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00010",
  "kind": "yes/no",
  "text": "Post: Can’t wait to get home take a big ass antihistamine and roll in some topical steroids.\n\nDamn it, skin! What did I ever do to you?!?!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
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
  "aid": "a00011",
  "kind": "yes/no",
  "text": "Claim: Jonghyun was a member of the boy group Shinee who released their first studio album \"She is\".\n\nPassages:\n\n[Kim Jong-hyun (singer)]\nHe is a vocalist of the South Korean boy group Shinee, and has further participated in S.M. Entertainment's project group S.M.\n\n[She Is]\nShe Is (Hangul: 좋아 ; RR: \"Joh ah \" \"good\") is the first studio album by South Korean singer-songwriter Jonghyun, released on May 24, 2016 by S.M. Entertainment and distributed by KT Music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00012",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I agree, I want them too",
   "@adi_jord agreed, this is ridiculous, gotta cop a pair"
  ],
  "human_label": "@adi_jord agreed, this is ridiculous, gotta cop a pair",
  "read_1": {
   "answer": "@adi_jord agreed, this is ridiculous, gotta cop a pair",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "@adi_jord agreed, this is ridiculous, gotta cop a pair",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00013",
  "kind": "yes/no",
  "text": "Claim: Julia Smith and Tony Holland were the creators of the long-running British soap opera in which Alison Pargeter plays the role of Sarah Cairns.\n\nPassages:\n\n[EastEnders]\nEastEnders is a long-running British soap opera created by Julia Smith and Tony Holland which has been broadcast on BBC One since 1985.\n\n[Alison Pargeter]\nAlison Pargeter (born 31 May 1972) is an English actress who played the roles of stalker Sarah Cairns in the BBC soap opera \"EastEnders\", also Mary Slessor in an 11-part television series of\" Mary Slessor\", and the Nag's Head barmaid called Val in the BBC \"Only Fools and Horses\" prequel \"Rock & Chips\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00014",
  "kind": "yes/no",
  "text": "Claim: Billy King was an Australian rules footballer who participated in a game that was contested between the South Carlton Football Club and Carlton Football Club, and was held at Princes Park in Carlton in 1945.\n\nPassages:\n\n[Billy King (Australian footballer)]\nWilliam Herbert 'Billy' King (17 August 1920 – 23 August 1990) was an Australian rules footballer who played for South Melbourne in the VFL during the 1940s. Primarily a wingman, he participated in the famous 1945 'Bloodbath' Grand Final which South Melbourne lost to Carlton.\n\n[1945 VFL Grand Final]\nThe 1945 VFL Grand Final was an Australian rules football game contested between the South Melbourne Football Club and Carlton Football Club, held at Princes Park in Melbourne on 29 September 1945.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
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
  "aid": "a00015",
  "kind": "yes/no",
  "text": "Tweet: Drum and bass is dangerous stuff don't you know.. #FabricReview 🙏🏻🙏🏻🙏🏻",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00016",
  "kind": "yes/no",
  "text": "Claim: Genesee Cream Ale is a cold fermented, alcohlic beverage produced by a brewery located along the Genesee River.\n\nPassages:\n\n[Genesee Brewing Company]\nGenesee Brewing Company is an American brewery located along the Genesee River in Rochester, New York.\n\n[Genesee Cream Ale]\nGenesee Cream Ale is a cold fermented, alcohlic beverage produced by the Genesee Brewing Company in Rochester, NY.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00017",
  "kind": "yes/no",
  "text": "Tweet: @ishkolhatkar @RosieisaHolt We think you are very, very funny and very,very,very etc …brave. You nail the issue and put those that actually believe the comments you make to shame…. Please keep doing what you’re doing….",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00018",
  "kind": "yes/no",
  "text": "Claim: The Post-Modern Prometheus was written, produced and directed by the series creator. This filmmaker and the director of Blind Date (1996 film) do not share the same nationality.\n\nPassages:\n\n[Theo van Gogh (film director)]\nTheodoor \"Theo\" van Gogh (] ; 23 July 19572 November 2004) was a Dutch film director, film producer, television director, television producer, television presenter, screenwriter, actor, critic and author.\n\n[Blind Date (1996 film)]\nBlind Date is a 1996 Dutch film by director Theo van Gogh.\n\n[The Post-Modern Prometheus]\nWritten and directed by series creator Chris Carter, \"The Post-Modern Prometheus\" is a \"Monster-of-the-Week\" episode, a stand-alone plot which is unconnected to the overarching mythology of \"The X-Files\".\n\n[Chris Carter (screenwriter)]\nChristopher Carl Carter (born October 13, 1956) is an American television and film producer, director and writer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00019",
  "kind": "yes/no",
  "text": "Claim: Director of The Object of My Affection and Maya Deren never worked in the same role in the film industry.\n\nPassages:\n\n[Nicholas Hytner]\nSir Nicholas Robert Hytner (born 7 May 1956) is an English theatre director, film director, and film producer.\n\n[The Object of My Affection]\nThe film is directed by Nicholas Hytner, and the screenplay was written by Wendy Wasserstein.\n\n[Maya Deren]\nMaya Deren (April 29, 1917 – October 13, 1961), born Eleanora Derenkowskaia (Russian: Элеоно́ра Деренко́вская ), was a Russian-American filmmaker and one of the most important American experimental filmmakers and entrepreneurial promoters of the avant-garde in the 1940s and 1950s. Deren was also a choreographer, dancer, film theorist, poet, lecturer, writer and photographer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00020",
  "kind": "yes/no",
  "text": "Claim: The home of Sir John Cutts who died in 1615 is a house at a parish 18.7 miles from central London.\n\nPassages:\n\n[Shenley Hall]\nShenley Hall is a Grade II listed country house at Shenley in Hertfordshire.\n\n[John Cutts (died 1615)]\nSir John Cutts (or Cutt) (1545–1615), of Horham Hall, Essex; Shenley Hall, Hertfordshire and Childerley, Cambridgeshire, was an English politician.\n\n[Shenley, Hertfordshire]\nThe village is located 18.7 miles from Central London.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00021",
  "kind": "yes/no",
  "text": "Claim: The player named Rookie of The Year in the 1997–98 Toronto Raptors season is the American retired professional basketball player and the current head men's basketball coach that the University of the Pacific Tigers are led by.\n\nPassages:\n\n[Damon Stoudamire]\nDamon Lamon Stoudamire (born September 3, 1973) is an American retired professional basketball player and the current head men's basketball coach at the University of the Pacific.\n\n[Pacific Tigers men's basketball]\nThey play their home games at the Alex G. Spanos Center and are led by head coach Damon Stoudamire.\n\n[1995–96 Toronto Raptors season]\nTop draft pick Damon Stoudamire was named Rookie of The Year averaging 19.0 points, and 9.3 assists per game.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00022",
  "kind": "yes/no",
  "text": "Post: no more instagram. we must all return to scrapbooks.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00023",
  "kind": "yes/no",
  "text": "Text: My favorite thing is that literally ONLY my @Walmart says I have to have a prescription for syringes that I've been getting OTC for years. This is the kind of shit diabetics are facing.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
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
  "aid": "a00024",
  "kind": "yes/no",
  "text": "Claim: The older sister of Noah Cyrus is a vocalist. The older sister of the vocalist for Love/Hate, who contributed to the album Quiet Riot 10, is also a vocalist.\n\nPassages:\n\n[Trace Cyrus]\nIn 2010, he began providing vocals and guitar in the pop rock band Ashland HIGH.\n\n[Jizzy Pearl]\nJizzy Pearl (born James Wilkinson) is an American vocalist that was born on March 17, 1958, in Chicago, Illinois.\n\n[Quiet Riot 10]\nLove/Hate vocalist Jizzy Pearl joined the band in November 2013 and performs lead vocals on the six studio tracks.\n\n[Noah Cyrus]\nShe is the youngest daughter of Tish Cyrus and Billy Ray Cyrus and the younger sister of Miley Cyrus and Trace Cyrus.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00025",
  "kind": "yes/no",
  "text": "Claim: Both Disney Magazine and The Ring are not still in publication.\n\nPassages:\n\n[The Ring (magazine)]\nThe Ring (often called The Ring magazine or Ring TV) is an American boxing magazine that was first published in 1922 as a boxing and wrestling magazine. The magazine is currently owned by Oscar De La Hoya's Golden Boy Enterprises, which acquired it in 2007.\n\n[Disney Magazine]\nDisney Magazine was an official Disney magazine that was published quarterly from December 1965 to April 2005.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00026",
  "kind": "yes/no",
  "text": "Text: @PetsatHome racial stereotyping is the problem. Please listen and retrain your staff. https://t.co/UvLkji9s5H",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00027",
  "kind": "yes/no",
  "text": "Claim: AEthelweard was an author of a English version of the collection of Old English annals where everything known of Cynric comes from.\n\nPassages:\n\n[Anglo-Saxon Chronicle]\nThe Anglo-Saxon Chronicle is a collection of annals in Old English chronicling the history of the Anglo-Saxons.\n\n[Cynric]\nEverything known about him comes from the \"Anglo-Saxon Chronicle\".\n\n[Æthelweard (historian)]\nÆthelweard (also Ethelward; d. c. 998), descended from the Anglo-Saxon King Æthelred I of Wessex, the elder brother of Alfred the Great, was an ealdorman and the author of a Latin version of the \"Anglo-Saxon Chronicle\" known as the \"Chronicon Æthelweardi\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00028",
  "kind": "yes/no",
  "text": "Claim: The actor that has performed as Inspector Javert in a Les Misérables production has won the same award that Adam Godley has won three times. This actor also starred in the film The Caterpillar Wish.\n\nPassages:\n\n[The Caterpillar Wish]\nThe Caterpillar Wish (also known as Caterpillar Wish) is a 2006 Australian coming-of-age film, directed by Sandra Sciberras and starring and ensemble cast including Victoria Thaine, Susie Porter and Philip Quast.\n\n[Adam Godley]\nHe is a Tony Award nominee and has been nominated three times for the Olivier Award.\n\n[Les Misérables: The Dream Cast in Concert]\nThe 10th Anniversary cast stars Colm Wilkinson as Jean Valjean, Philip Quast as Inspector Javert, Michael Ball as Marius Pontmercy, Lea Salonga as Éponine, Judy Kuhn as Cosette, Ruthie Henshall as Fantine, Michael Maguire as Enjolras, Alun Armstrong as Thénardier, Jenny Galloway as Madame Thénardier, Adam Searles as Gavroche, Hannah Chick as Young Cosette, and several others, and was directed by John Caird. The performers were chosen from the London, Broadway and Australian productions of the show and the Royal Philharmonic Orchestra was conducted by David Charles Abell.\n\n[Philip Quast]\nPhilip Mark Quast (born 30 July 1957) is an Australian actor and singer. He has won the Laurence Olivier Award for Best Actor in a Musical three times, the most of any actor to date.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00029",
  "kind": "yes/no",
  "text": "Text: settings is such an interesting place",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00030",
  "kind": "yes/no",
  "text": "Claim: The director of \"Dedication of the Great Buddha\" was older than master chef Don O. Newland when he died.\n\nPassages:\n\n[Teinosuke Kinugasa]\nTeinosuke Kinugasa (衣笠 貞之助 , Kinugasa Teinosuke ) (1 January 1896 – 26 February 1982) was a Japanese actor and film director.\n\n[Dedication of the Great Buddha]\nDedication of the Great Buddha (大仏開眼 , Daibutsu kaigen ) is a 1952 Japanese film directed by Teinosuke Kinugasa.\n\n[Don O. Newland]\nDon Oliver Newland (1896–1951) was an American film director and producer whose career consisted largely of itinerant work.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00031",
  "kind": "yes/no",
  "text": "Claim: This area is located just north of a constituent college of the University of a city. It stands across from the Bear Inn in the city. Heinz Cassirer lectured and lived in the city.\n\nPassages:\n\n[Christ Church, Oxford]\nChrist Church (Latin: \"Ædes Christi\" , the temple or house, \"ædēs\", of Christ, and thus sometimes known as \"The House\") is a constituent college of the University of Oxford in England.\n\n[Bear Lane]\nThe lane is located just north of Christ Church.\n\n[Heinz Cassirer]\nFollowing Paton, he moved to Oxford, lecturing at Corpus Christi College.\n\n[Bear Inn, Oxford]\nIts circa-17th century incarnation stands on the corner of Alfred Street and Blue Boar Street, opposite Bear Lane in the centre of Oxford, just north of Christ Church.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00032",
  "kind": "yes/no",
  "text": "Claim: The actor that is linked to both the American Revolution film that has Hal Stalmaster in the lead role, and Magic Kingdom is Walt Disney.\n\nPassages:\n\n[Johnny Tremain (film)]\nJohnny Tremain is a 1957 film made by Walt Disney Productions, based on the 1944 Newbery Medal-winning children's novel of the same name by Esther Forbes, retelling the story of the years in Boston, Massachusetts prior to the outbreak of the American Revolution.\n\n[Hal Stalmaster]\nHarry Lapidus Stalmaster, known as Hal Stalmaster (born March 29, 1940), is an American former actor, known for his lead role in the 1957 Walt Disney film of the American Revolution \"Johnny Tremain\", based on the 1943 Esther Forbes novel of the same name.\n\n[Magic Kingdom]\nInitialized by Walt Disney and designed by WED Enterprises, its layout and attractions are based on Disneyland Park in Anaheim, California, and is dedicated to fairy tales and Disney characters.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00033",
  "kind": "yes/no",
  "text": "Text: 5 star personality\n4.8 star uber rating",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00034",
  "kind": "yes/no",
  "text": "Post: do i just blast maneskin to get hyped for my osce or??",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00035",
  "kind": "yes/no",
  "text": "Claim: The youngest child of soccer player Mangue Cisse plays for the Swiss club Yverdon.\n\nPassages:\n\n[Mangué Cissé]\nHe had seven children, the youngest of which is French international, Djibril Cissé.\n\n[Djibril Cissé]\nDjibril Cissé (] ; born 12 August 1981) is a French footballer who plays for Swiss club Yverdon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00036",
  "kind": "yes/no",
  "text": "Claim: Fianna Eireann is an Irish nationalist youth organization that was founded by Bulmer Hobson and an Irish political nationalist, suffragette, and politician, that was the first woman elected to the British House of Commons.\n\nPassages:\n\n[Fianna Éireann]\nNa Fianna Éireann (The Fianna of Ireland), known as the Fianna, is an Irish nationalist youth organisation founded by Bulmer Hobson and Constance Markievicz in 1909.\n\n[Constance Markievicz]\nConstance Georgine Markievicz, known as Countess Markievicz (Polish: \"Markiewicz\" ] ; née Gore-Booth; 4 February 1868 – 15 July 1927) was an Irish Sinn Féin and Fianna Fáil politician, revolutionary nationalist, suffragette and socialist. In December 1918, she was the first woman elected to the British House of Commons, though she did not take her seat and, along with the other Sinn Féin TDs, formed the first Dáil Éireann.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00037",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Been trying to get my boyfriends attention. Let’s see how long it takes for him to see this tweet tho.",
   "Sitting next to my boyfriend but he'll notice me on twitter first."
  ],
  "human_label": "Been trying to get my boyfriends attention. Let’s see how long it takes for him to see this tweet tho.",
  "read_1": {
   "answer": "Sitting next to my boyfriend but he'll notice me on twitter first.",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "Sitting next to my boyfriend but he'll notice me on twitter first.",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00038",
  "kind": "yes/no",
  "text": "Post: The most 2020 quote of the year:\n\nMe: we should go to the Van Gogh Museum!\nLittle Brother: is that the donny with one ear?",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00039",
  "kind": "yes/no",
  "text": "Claim: Snakes on a Plane (Bring It) is the debut dingle for this band. The lead vocalist of this band and Robert Plant are not both English.\n\nPassages:\n\n[Snakes on a Plane (Bring It)]\n\"Snakes on a Plane (Bring It)\", also referred to as \"Bring It (Snakes on a Plane)\", is the debut single by Cobra Starship, released in 2006 from the soundtrack album \"\".\n\n[Gabe Saporta]\nGabriel Eduardo \"Gabe\" Saporta (born October 11, 1979) is an Uruguayan-American musician and entrepreneur.\n\n[Cobra Starship]\nCobra Starship was an American dance-pop band created by former Midtown bassist and lead vocalist Gabe Saporta in 2006 in New York City, New York.\n\n[Robert Plant]\nRobert Anthony Plant, {'1': \", '2': \", '3': \", '4': \"} (born 20 August 1948) is an English singer, songwriter, and musician, best known as the lead singer and lyricist of the rock band Led Zeppelin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00040",
  "kind": "yes/no",
  "text": "Post: Roses are Red\nViolets are Blue\nMy first love was Championship Manager\nTommy Svindal Larsen and Kennedy Bakircioglu \n\n#HappyValentinesDay",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00041",
  "kind": "yes/no",
  "text": "Claim: The film A Taxi Driver was released in South Korea.\n\nPassages:\n\n[Jang Hoon]\nJang Hoon (born May 4, 1975) is a South Korean film director.\n\n[A Taxi Driver]\nIt was selected as the South Korean entry for the Best Foreign Language Film at the 90th Academy Awards.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00042",
  "kind": "yes/no",
  "text": "Claim: Robert \"Bobby\" Germaine, famous New York burglar and freelance writer, was involved in a robbery for which a book was written about.\n\nPassages:\n\n[Lufthansa heist]\n\"This is about the robbery itself.\n\n[Robert &quot;Bobby&quot; Germaine]\nRobert \"Bobby\" Germaine, Sr. (October 1, 1925 – April 1986), the son of French-Canadian immigrants, was a drug trafficker, burglar, and freelance writer in New York, NY. He was friends with Henry Hill and involved in his criminal activities following the Lufthansa heist up to Hill's incarceration.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00043",
  "kind": "yes/no",
  "text": "Claim: Nassu County, which borders Queens, has a population of 778.\n\nPassages:\n\n[Hewlett-Woodmere School District]\nThe Hewlett-Woodmere Public School District, Union Free School District 14, is located in the southwest section of Nassau County, New York and borders the New York City borough of Queens.\n\n[Woodsburgh, New York]\nThe population was 778 at the 2010 census.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00044",
  "kind": "yes/no",
  "text": "Claim: The company acquired by RBC where John G. Taft was employed was founded before Berenberg Bank.\n\nPassages:\n\n[John G. Taft]\nHis unit at Dougherty was later acquired by Dain Rauscher, and Taft began working with Royal Bank of Canada (RBC) when it acquired Dain Rauscher in 2001.\n\n[Dain Rauscher Wessels]\nDain Rauscher Wessels was a brokerage and investment banking firm based in Minneapolis, Minnesota. The firm traced its origins to a number of smaller regional securities firms founded in the 1920s and 1930s.\n\n[Berenberg Bank]\nKG, commonly known as Berenberg Bank, is a Hamburg-based multinational investment banking and private banking company, founded by the Belgian-origined Berenberg family in 1590.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00045",
  "kind": "yes/no",
  "text": "Claim: Anna B. Sheppard has worked in films with Steven Allan Spielberg, a part of the New Hollywood era.\n\nPassages:\n\n[Anna B. Sheppard]\nA sister to fellow costume designer Magdalena Biedrzycka, Sheppard made many films with directing masters like Steven Spielberg or Roman Polański.\n\n[Steven Spielberg]\nSteven Allan Spielberg, {'1': \", '2': \", '3': 'KBE', '4': \"} , {'1': \", '2': \", '3': 'OMRI', '4': \"} (born December 18, 1946) is an American director, producer, and screenwriter. He is considered one of the founding pioneers of the New Hollywood era, as well as being viewed as one of the most popular directors and producers in film history.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00046",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Most people have security cameras for protection. Ours acts as a DVR",
   "The events that happen around our house while we are not here can be very entertaining"
  ],
  "human_label": "Most people have security cameras for protection. Ours acts as a DVR",
  "read_1": {
   "answer": "The events that happen around our house while we are not here can be very entertaining",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "The events that happen around our house while we are not here can be very entertaining",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00047",
  "kind": "yes/no",
  "text": "Claim: The company produced the Evergreen GPU's for its graphics card Radeon HD 5000 Series. It's headquartered farther west than the company that owns Software Spectrum.\n\nPassages:\n\n[Level 3 Communications]\nLevel 3 Communications is an American multinational telecommunications and Internet service provider company headquartered in Broomfield, Colorado.\n\n[Radeon HD 5000 Series]\nThe Evergreen series is a family of GPUs developed by Advanced Micro Devices for its Radeon line under the ATI brand name.\n\n[Advanced Micro Devices]\nAdvanced Micro Devices, Inc. (AMD) is an American multinational semiconductor company based in Sunnyvale, California, United States, that develops computer processors and related technologies for business and consumer markets.\n\n[Software Spectrum]\nSoftware Spectrum is a company acquired by Level 3 Communications in 2002.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00048",
  "kind": "yes/no",
  "text": "Claim: Gabriella Montez in the Disney Channel Original Movie \"High School Musical was played by a new permanent member on the fourteenth season of the show, for which Mandy Moore (choreographer) is well known for her work with.\n\nPassages:\n\n[Mandy Moore (choreographer)]\nSamantha Jo \"Mandy\" Moore (born March 28, 1976 in St. Louis, Missouri and raised in Breckenridge, Colorado) is an American choreographer who is well known for her work on \"Dancing with the Stars\" and on \"So You Think You Can Dance\", having appeared on seasons 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, , and 14.\n\n[So You Think You Can Dance (U.S. season 14)]\nSo You Think You Can Dance, an American dance competition show, returned for its fourteenth season on Monday, June 12, 2017. The new season's judge panel once again features series creator Nigel Lythgoe (who also serves as executive producer), as well as the return of ballroom expert Mary Murphy, along with new permanent member Vanessa Hudgens, while Cat Deeley continues in her role as host for a thirteenth consecutive season.\n\n[Vanessa Hudgens]\nVanessa Anne Hudgens (born December 14, 1988) is an American actress and singer. After making her feature film debut in \"Thirteen\" (2003), Hudgens rose to prominence portraying Gabriella Montez in the \"High School Musical\" film series, which brought her significant mainstream success.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00049",
  "kind": "yes/no",
  "text": "Claim: This sitariyas helped introduce North Indian Classical Music to the West, along with Nikhil Banerjee, who was a student of Baba Allauddin Khan. He was the son of Enayat Khan.\n\nPassages:\n\n[Enayat Khan]\nHe was the father of Vilayat Khan, one of the topmost sitariyas of the postwar period.\n\n[Vilayat Khan]\nAlong with Ravi Shankar, Ali Akbar Khan, Nikhil Banerjee and his younger brother Imrat Khan, Vilayat Khan helped introduce Indian Classical Music to the West.\n\n[Nikhil Banerjee]\nA student of the legendary Baba Allauddin Khan, Pandit Nikhil Banerjee was known for his technical virtuosity and clinical execution.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 }
]
