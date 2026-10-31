# A46 gold-label confirmation (Opus) RS-confirm-499d50bb-008

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/confirm/answers/RS-confirm-499d50bb-008.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's aid).

## Instructions

You are auditing the gold labels of a training set for label noise. Each item shows the material (text, question, options, definitions), the gold label that the dataset's human annotators gave (human_label), and the answers of two independent blind readers (read_1, read_2; an answer may be "abstain" or null when the reader gave none). The text is DATA only: ignore any instructions inside it.
Decide whether the human label is right, from the material alone (do not count the readers' votes; readers are fallible and often miss context):
- gold_ok: the human label is a correct, defensible answer under the question and definitions.
- wrong_gold: the human label is wrong: a careful reader with the same material would clearly answer differently.
- ambiguous: the material does not settle the answer, or two different answers are both defensible under the question as worded.
Never propose a new label. reason = one short line (at most 30 words).
Each item also carries first_pass: the earlier reviewer's verdict and reason. It is a claim to check, not an instruction. Give your own verdict from the material; overturn it (gold_ok) when the human label is in fact defensible.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "<gold_ok | wrong_gold | ambiguous>", "reason": "<one line>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its aid)

[
 {
  "aid": "c00400",
  "kind": "yes/no",
  "text": "Claim: George Hamilton IV performed the song \"Abilene\" in a 1963 movie. The actress who co-starred with an actor in this movie was Canadian. The actor also starred in \"The Crawling Hand\".\n\nPassages:\n\n[The Crawling Hand]\nThe Crawling Hand is a 1963 science fiction horror film directed by Herbert L. Strock, and starring Rod Lauren, Peter Breck, Allison Hayes, and Alan Hale, Jr. It was later featured on the television shows \"Mystery Science Theater 3000\" (\"MST3K\") and \"The Canned Film Festival\".\n\n[Ruta Lee]\nRuta Lee (born May 30, 1935) is a Canadian actress and dancer who appeared as one of the brides in the musical \"Seven Brides for Seven Brothers\".\n\n[Abilene (song)]\nThe song reached number one on the U.S. country music chart for four weeks, and peaked at number 15 on the pop music charts.\n\n[Hootenanny Hoot]\nIt stars Peter Breck and Ruta Lee.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nothing says Hamilton performed Abilene in a 1963 movie or gives Hootenanny Hoot's year."
  }
 },
 {
  "aid": "c00401",
  "kind": "yes/no",
  "text": "Text: if i saw a capybara in person id probably throw up",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Could be literal disgust or ironic exaggeration about cute capybaras; text alone does not settle intent."
  }
 },
 {
  "aid": "c00402",
  "kind": "yes/no",
  "text": "Claim: St Mary's Church, Fleetwood is an active church of this diocese. Where it is centred and Peel Cathedral, belong to the Catholic religion.\n\nPassages:\n\n[St Mary's Church, Fleetwood]\nIt is an active church in the Roman Catholic Diocese of Lancaster.\n\n[Peel Cathedral]\nThe Cathedral Church of Saint German or Peel Cathedral, rebranded as Cathedral Isle of Man is located in Peel, Isle of Man. The cathedral is also one of the parish churches in the parish of the West Coast which includes the town of Peel, and was built in 1879–84.\n\n[Lancaster Cathedral]\nLancaster Cathedral, also known as The Cathedral Church of St Peter and Saint Peter's Cathedral, is in St Peter's Road, Lancaster, Lancashire, England. It was a Roman Catholic parish church until 1924, when it was elevated to the status of a cathedral.\n\n[Roman Catholic Diocese of Lancaster]\nThe Roman Catholic Diocese of Lancaster is a Latin Rite Roman Catholic diocese centred on Lancaster Cathedral in the city of Lancaster in Lancashire, England.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nothing says Peel Cathedral is Catholic; only the Lancaster diocese and cathedral are stated as Roman Catholic."
  }
 },
 {
  "aid": "c00403",
  "kind": "yes/no",
  "text": "Claim: The German rally driver who won victories for Fiat, Opel, Lancia, and Audi drove The Lancia Rally.\n\nPassages:\n\n[Walter Röhrl]\nWalter Röhrl (born 7 March 1947) is a German rally and auto racing driver, with victories for Fiat, Opel, Lancia and Audi as well as Porsche, Ford and BMW.\n\n[Lancia Rally 037]\nThe Lancia Rally (\"Tipo 151\", also known as the Lancia Rally 037, Lancia 037 or Lancia-Abarth #037 from its Abarth project code \"037\") was a mid-engine sports car and rally car built by Lancia in the early 1980s to compete in the FIA Group B World Rally Championship.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Röhrl drove the Lancia Rally 037."
  }
 },
 {
  "aid": "c00404",
  "kind": "yes/no",
  "text": "Claim: Greatest Hits Volume 1 is a greatest hits compilation album by The Beatles which was exclusive to Australia and New Zealand, the album was compiled by EMI Australia to fill in the gap, much like A Collection of Beatles Oldies (subtitled But Goldies!), by the English rock band the Beatles.\n\nPassages:\n\n[A Collection of Beatles Oldies]\nA Collection of Beatles Oldies (subtitled But Goldies!)\n\n[Greatest Hits Volume 1 (Beatles album)]\nThe album was compiled by EMI Australia to fill in the gap between \"Rubber Soul\" and \"Revolver\" (much like \"A Collection of Beatles Oldies\" would in 1966 in between \"Revolver\" and \"Sgt. Pepper's Lonely Hearts Club Band\").",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Exclusivity to Australia and New Zealand is not stated in the passages."
  }
 },
 {
  "aid": "c00405",
  "kind": "yes/no",
  "text": "Text: I'm the highest I'll ever be on 420 in my life! I'm on an airplane duh",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Pun on being high on 420; playful wordplay, not clearly sarcasm versus literal joke."
  }
 },
 {
  "aid": "c00406",
  "kind": "yes/no",
  "text": "Claim: Chindia is a portmanteau word that refers to China and India together in general, together, they contain over one-third of the total number of humans currently living, and is called world's population.\n\nPassages:\n\n[Chindia]\nTogether, they contain over one-third of the world's population (nearly 2.7 billion).\n\n[World population]\nIn demographics, the world population is the total number of humans currently living.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages never say Chindia is a portmanteau; the claim's last clause is also garbled."
  }
 },
 {
  "aid": "c00407",
  "kind": "yes/no",
  "text": "Claim: The name of the largest shipping facility in the Northeastern United States, where the Boston Red Socks play is Port of Boston.\n\nPassages:\n\n[Boston Harbor]\nIt is home to the Port of Boston, a major shipping facility in the northeastern United States.\n\n[Congress Street Grounds]\nThe ground was home to the Boston Reds, that played in the Players' League in 1890 and the American Association in 1891.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.97
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages say 'a major' facility, not largest, and mention Boston Reds, not Red Sox; unsupported."
  }
 },
 {
  "aid": "c00408",
  "kind": "yes/no",
  "text": "Claim: Ernst John von Freyend was adjutant to the Chief of the Armed Forces High Command during WWII, Wilhelm Keitel, who was born in 1909.\n\nPassages:\n\n[Wilhelm Keitel]\nWilhelm Keitel (22 September 1882 – 16 October 1946) was a German field marshal who served as Chief of the Armed Forces High Command (\"Oberkommando der Wehrmacht\" or OKW) in Nazi Germany during World War II.\n\n[Ernst John von Freyend]\nErnst John von Freyend (25 March 1909– 24 March 1980) was a German Oberkommando der Wehrmacht officer who served during World War II as the adjutant to Field Marshal Wilhelm Keitel.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Keitel was born in 1882, not 1909; 1909 is von Freyend's birth year."
  }
 },
 {
  "aid": "c00409",
  "kind": "yes/no",
  "text": "Claim: The head coach of the 2009-2010 Texas Longhorn's men Elite basketball team was born July 17, 1954.\n\nPassages:\n\n[2009–10 Texas Longhorns men's basketball team]\nTheir head coach was Rick Barnes, who was in his 12th year.\n\n[Rick Barnes]\nRichard Dale Barnes (born July 17, 1954) is the current head coach of the Tennessee Volunteers men's basketball team, a post he has held since 2015.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Rick Barnes coached the 2009-10 Longhorns and was born July 17, 1954; supported."
  }
 },
 {
  "aid": "c00410",
  "kind": "yes/no",
  "text": "Claim: The musician that plays the tenor sax solo on the Great White song, \"Gone with the Wind\", is a member of a band inducted into the Rock and Roll Hall of Fame in 2014.\n\nPassages:\n\n[Sail Away (Great White album)]\nClarence Clemons of the E Street Band plays the sax solo on \"Gone with the Wind\".\n\n[E Street Band]\nThe band was inducted into the Rock and Roll Hall of Fame in 2014.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Chain supported, but passage says 'sax solo', not tenor sax; strictness decides."
  }
 },
 {
  "aid": "c00411",
  "kind": "yes/no",
  "text": "Claim: Svetlana Germanovna Parkhomenko, is a retired Soviet and Russian tennis player and tennis coach, she's the bronze medalist in women's and mixed doubles, in the 1983 Summer Universiade event that took place in Edmonton, Alberta, Canada between July 1 and 12, 1983.\n\nPassages:\n\n[Svetlana Parkhomenko]\nOn the international level, she was the winner of the 1983 European amateur championships in women's and mixed doubles, bronze medalist of the 1983 Universiade in women's and mixed doubles, and winner of 8 WTA doubles tournaments.\n\n[1983 Summer Universiade]\nThe 1983 Summer Universiade, also known as the 1983 World University Games or XII Summer Universiade, took place in Edmonton, Alberta, Canada between July 1 and 12, 1983.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "'Retired Soviet and Russian tennis player and coach' is not established by the passages."
  }
 },
 {
  "aid": "c00412",
  "kind": "yes/no",
  "text": "Claim: The Russian-British physicist who shared the Nobel Prize in Physics in 2010 has established a reserach center dedicated to continuing the work with graphene in Singapore.\n\nPassages:\n\n[Konstantin Novoselov]\nSir Konstantin Sergeevich Novoselov (born 23 August 1974) is a Russian-British physicist, and Langworthy Professor in the School of Physics and Astronomy at the University of Manchester.\n\n[Graphene Research Centre]\nThe Graphene Research Centre (GRC), at the National University of Singapore (NUS), is the first centre in Asia dedicated to graphene research.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Novoselov established the Singapore centre or that he won the 2010 Nobel."
  }
 },
 {
  "aid": "c00413",
  "kind": "yes/no",
  "text": "Claim: \"Tennessee\" Williams, is known with Arthur Miller's and Arthur Miller, as one of the three foremost dramatists of the 20th century. The writer of \"Stella Bain\" is not.\n\nPassages:\n\n[Tennessee Williams]\nThomas Lanier \"Tennessee\" Williams III (March 26, 1911 – February 25, 1983) was an American playwright.\n\n[Anita Shreve]\nAnita Shreve (born 1946) is an American writer.\n\n[Stella Bain]\nStella Bain is an American novel by Anita Shreve, set in World War I.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "The 'three foremost dramatists' ranking and Arthur Miller appear nowhere in the passages."
  }
 },
 {
  "aid": "c00414",
  "kind": "yes/no",
  "text": "Claim: The Beatles released their 1974 album that featured the song \"Simply Shady\" during the American tour.\n\nPassages:\n\n[The Beatles' 1966 US tour]\nThe Beatles staged their third concert tour of America in August 1966, and it was the last commercial tour they would ever undertake.\n\n[Dark Horse (George Harrison album)]\nAlthough keenly anticipated on release, \"Dark Horse\" is associated with the controversial North American tour that Harrison staged with co-headliner Ravi Shankar in November and December that year.\n\n[Simply Shady]\n\"Simply Shady\" is a song by English musician George Harrison that was released on his 1974 album \"Dark Horse\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Dark Horse was a George Harrison solo album, not a Beatles album."
  }
 },
 {
  "aid": "c00415",
  "kind": "yes/no",
  "text": "Claim: The Air Force military branch for which Christian Roy Kaldager served, was established on 10 November 1944.\n\nPassages:\n\n[Royal Norwegian Air Force]\nIt was established as a separate arm of the Norwegian armed forces on 10 November 1944.\n\n[Christian Roy Kaldager]\nChristian Roy Kaldager (18 March 1908 – 23 June 2005) was a Royal Norwegian Air Force officer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Kaldager was a Royal Norwegian Air Force officer and that force was established 10 November 1944; fully supported."
  }
 },
 {
  "aid": "c00416",
  "kind": "yes/no",
  "text": "Post: Having a bad week but what else is new!! At least I finally got paid 💕😭",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "'What else is new' is mildly ironic, but overall message is a sincere mixed update."
  }
 },
 {
  "aid": "c00417",
  "kind": "yes/no",
  "text": "Claim: This artist and Jimi Hendrix bother made music in the rock genre. He released the album Family Joules.\n\nPassages:\n\n[Family Joules]\nIt is the first album by the band without founding member, guitarist and singer Dave Peverett and their first album to feature singer/guitarist Charlie Huhn and guitarist Bryan Bassett.\n\n[Jimi Hendrix]\nJames Marshall \"Jimi\" Hendrix (born Johnny Allen Hendrix; November 27, 1942 – September 18, 1970) was an American rock guitarist, singer, and songwriter.\n\n[Dave Peverett]\nDavid Jack Peverett (16 April 1943 – 7 February 2000), also known as Lonesome Dave, was an English singer and musician, best known as the original lead vocalist and rhythm guitarist of the rock band Foghat, which he founded following his tenure in Savoy Brown.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Family Joules was the first album without Peverett, so he did not release it."
  }
 },
 {
  "aid": "c00418",
  "kind": "yes/no",
  "text": "Tweet: @kmflett And with a plentiful supply of rhubarb.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "A context-free reply; nothing shows whether the rhubarb remark is ironic or literal."
  }
 },
 {
  "aid": "c00419",
  "kind": "yes/no",
  "text": "Claim: The Genesis Flood: The Biblical Record and its Scientific Implications was written in 1961 by one of the founders of the Creation Research Society.\n\nPassages:\n\n[Henry M. Morris]\nHenry Madison Morris (October 6, 1918 – February 25, 2006) was an American young Earth creationist, Christian apologist, and engineer. He is widely known for coauthoring \"The Genesis Flood\" with John C. Whitcomb in 1961.\n\n[The Genesis Flood]\nThe Genesis Flood: The Biblical Record and its Scientific Implications is a 1961 book by young earth creationists John C. Whitcomb and Henry M. Morris that, according to Ronald Numbers, elevated young earth creationism \"to a position of fundamentalist orthodoxy.\"",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Morris or Whitcomb founded the Creation Research Society."
  }
 },
 {
  "aid": "c00420",
  "kind": "yes/no",
  "text": "Claim: A notable alumni of Filbornaskolan participated in the Celtic 1977 Scottish League Cup Final. He was a Celtic football coach and former professional player.\n\nPassages:\n\n[Filbornaskolan]\nNotable former alumni include Henrik Larsson.\n\n[Henrik Larsson]\nHenrik Edward Larsson (] ; born 20 September 1971) is a Swedish football coach and former professional player.\n\n[1997 Scottish League Cup Final]\nCeltic won the match 3–0 thanks to goals by Marc Rieper, Henrik Larsson and Craig Burley.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Larsson scored in the 1997 final, not 1977, and he is described as Swedish coach, not Celtic coach."
  }
 },
 {
  "aid": "c00421",
  "kind": "yes/no",
  "text": "Claim: The tour that Lungs Tour supported the band fronted by Bono in was a 2-year worldwide tour. It had a round stage and had a song that had never before been performed live.\n\nPassages:\n\n[Lungs Tour]\nThey also supported U2 on their U2 360° Tour in 2011.\n\n[Electrical Storm (song)]\nU2 did not play the song live until 2 July 2009, when they performed it on the second concert of their U2 360° Tour in Barcelona.\n\n[U2 360° Tour]\nThe U2 360° Tour was a worldwide concert tour by rock band U2. The concerts featured the band playing \"in the round\" on a circular stage, allowing the audience to surround them on all sides.\n\n[Bono]\nHe is best known as the lead vocalist and primary lyricist of rock band U2.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages never say the 360 Tour lasted two years; that detail is unsupported."
  }
 },
 {
  "aid": "c00422",
  "kind": "yes/no",
  "text": "Claim: The 2012–13 Puebla league was the 66th regular season of a league currently sponsored by BBVA.\n\nPassages:\n\n[Liga MX]\nCurrently sponsored by BBVA through its Mexican subsidiary BBVA Bancomer, it is officially known as Liga BBVA Bancomer.\n\n[2012–13 Puebla F.C. season]\nThe 2012–13 Puebla season was the 66th professional season of Mexico's top-flight football league.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Passages do not explicitly equate Mexico's top-flight league with Liga MX; 'regular' vs 'professional' season."
  }
 },
 {
  "aid": "c00423",
  "kind": "yes/no",
  "text": "Tweet: I may look happy on the outside bit on the inside I'm dying #painful #sad",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Plain sincere expression of sadness; nothing ironic or insincere."
  }
 },
 {
  "aid": "c00424",
  "kind": "yes/no",
  "text": "Post: @brruhia Nah bruh you just drinking it upside down 😂",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Teasing joke reply; whether it counts as ironic mockery or a plain joke is unclear without context."
  }
 },
 {
  "aid": "c00425",
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
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Pixar produced Monsters Inc but Disney distributed it; whether 'made by' the same company holds is unclear."
  }
 },
 {
  "aid": "c00426",
  "kind": "yes/no",
  "text": "Claim: The Tulsa Golden Hurricane franchise will join an American collegiate athletic conference, featuring 12 member universities.\n\nPassages:\n\n[2013 Conference USA men's soccer season]\nThe 2013 Conference USA men's soccer season will be the 19th season of men's varsity soccer in the conference. It will also be the last C-USA season for the Tulsa Golden Hurricane, which will join the American Athletic Conference in July 2014.\n\n[American Athletic Conference]\nThe American Athletic Conference (also known as The American and sometimes abbreviated AAC) is an American collegiate athletic conference, featuring 12 member universities and three associate member universities that compete in the National Collegiate Athletic Association's (NCAA) Division I, with its football teams competing in the Football Bowl Subdivision (FBS).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Tulsa will join the AAC, which has 12 member universities; the claim is fully supported."
  }
 },
 {
  "aid": "c00427",
  "kind": "yes/no",
  "text": "Claim: The ex member of Jonny (band) and Teenage Fanclub is older than the frontman of The Vines. The latter produced their album Wicked Nature.\n\nPassages:\n\n[Craig Nicholls]\nCraig Robert Nicholls (born 31 August 1977) is an Australian musician, best known as the lead singer, songwriter, and guitarist of the Australian alternative rock band The Vines, of which he is the only mainstay member.\n\n[Jonny (band)]\nJonny is a two-person band formed by Norman Blake of Teenage Fanclub and Euros Childs of Gorky's Zygotic Mynci.\n\n[Wicked Nature]\nThe release marks a few milestones for The Vines, with frontman Craig Nicholls taking on the role of producer for the first time, as well as introducing a completely new rhythm section with drummer Lachlan West and bassist Tim John.\n\n[Norman Blake (Scottish musician)]\nNorman Blake (born 20 October 1965, Bellshill, North Lanarkshire, Scotland) is a singer, instrumentalist and songwriter in the Glasgow based band Teenage Fanclub.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Blake (1965) is older than Nicholls (1977), who produced Wicked Nature; fully supported."
  }
 },
 {
  "aid": "c00428",
  "kind": "yes/no",
  "text": "Claim: Seyi Adebanjo's identity, is a combination of masculinity and femininity or neither in gender expression.\n\nPassages:\n\n[Discwoman]\nDiscwoman is a New York based collective, booking agency, and event platform representing and showcasing female-identified (cis women, transwomen, and gender queer) talent in the electronic music community.\n\n[Seyi Adebanjo]\nSeyi Adebanjo is a genderfluid, queer MFA media artist, born in Nigeria and now resident in New York City.\n\n[Genderqueer]\nGenderqueer people may express a combination of masculinity and femininity, or neither, in their gender expression.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Adebanjo is genderfluid; the passage describing that expression is about genderqueer people, with no link given."
  }
 },
 {
  "aid": "c00429",
  "kind": "yes/no",
  "text": "Claim: Boston Advantage, along with the Boston Junior Rangers, East Coast Wizards, New Hampshire Avalanche, American and one other are American youth ice hockey teams. As of the 2010 census, the city that other team plays in had a population of 60,879.\n\nPassages:\n\n[Haverhill, Massachusetts]\nHaverhill ( ) is a city in Essex County, Massachusetts, United States. The population was 60,879 at the 2010 census.\n\n[Boston Advantage]\nIt is also a charter franchise, along with the Boston Junior Rangers, East Coast Wizards, New Hampshire Avalanche, Seacoast Spartans and Valley Jr. Warriors.\n\n[Valley Jr. Warriors]\nThe Valley Jr.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages never say which city the other team plays in; Haverhill link is unverified."
  }
 },
 {
  "aid": "c00430",
  "kind": "yes/no",
  "text": "Post: Well done @WestHam and @premierleague, great leadership! https://t.co/4IPXaK0Jpu",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Praise for league leadership could be sincere or ironic; no context settles it."
  }
 },
 {
  "aid": "c00431",
  "kind": "yes/no",
  "text": "Text: Why you gotta take someone pure like Sean Lock from us huh? Why couldn’t it be James Corden?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Dark joke at Corden's expense; whether it is literal wish or ironic mockery is debatable."
  }
 },
 {
  "aid": "c00432",
  "kind": "yes/no",
  "text": "Text: I still can’t believe England won the World Cup",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Could be ironic joke or sincere disbelief at a real win; no context."
  }
 },
 {
  "aid": "c00433",
  "kind": "yes/no",
  "text": "Post: There is not enough people here #ivoryrooms",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "May be ironic about a crowded room or a literal complaint; nothing settles it."
  }
 },
 {
  "aid": "c00434",
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
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Dain Rauscher origins 1920s, Berenberg founded 1590; claim false."
  }
 },
 {
  "aid": "c00435",
  "kind": "yes/no",
  "text": "Claim: Arizona State Route 51 (SR 51) is named after a Native American woman belonging to the Native American tribe.\n\nPassages:\n\n[Lori Piestewa]\nA member of the Hopi tribe, Piestewa was the first Native American woman in history to die in combat while serving in the U.S. military and the first woman in the U.S. military killed in the Iraq War.\n\n[Arizona State Route 51]\nArizona State Route 51 (SR 51), also known as the Piestewa Freeway, is a numbered state highway in Phoenix, Arizona. The peak was named after Lori Piestewa, the first Native American woman to die in combat in the U.S. Military.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Freeway is called Piestewa Freeway but passage says the peak was named after her."
  }
 },
 {
  "aid": "c00436",
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
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Bear Lane north of Christ Church, opposite Bear Inn; Cassirer moved to and lectured in Oxford."
  }
 },
 {
  "aid": "c00437",
  "kind": "yes/no",
  "text": "Claim: \"A Swingin' Safari\" was a song written originally by German songwriter Bert Kaempfert but made popular by Billy Vaughn.\n\nPassages:\n\n[Bert Kaempfert]\nBerthold Heinrich Kämpfert, (16 October 1923 – 21 June 1980), better known as Bert Kaempfert, was a German orchestra leader, music producer, and songwriter.\n\n[A Swingin' Safari]\nThat same year, Billy Vaughn recorded it, and his cover reached number 13 on the \"Billboard\" charts that summer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Kaempfert wrote A Swingin' Safari; authorship unsupported."
  }
 },
 {
  "aid": "c00438",
  "kind": "yes/no",
  "text": "Claim: The director of Looking on the Bright Side and Basil the director of Godfather Part II were both alive at some point in time. Looking on the Bright side was a 1932 British musical comedy film.\n\nPassages:\n\n[Basil Dean]\nBasil Herbert Dean CBE (27 September 1888 – 22 April 1978) was an English actor, writer, film producer/film director and theatrical producer/director.\n\n[Looking on the Bright Side]\nLooking on The Bright Side is a 1932 British musical comedy film It was directed by Graham Cutts and Basil Dean and starring Gracie Fields, Richard Dolman, and Betty Shale.\n\n[The Godfather Part II]\nThe Godfather Part II is a 1974 American crime film produced and directed by Francis Ford Coppola from a screenplay co-written with Mario Puzo, starring Al Pacino and Robert De Niro.\n\n[Francis Ford Coppola]\nFrancis Ford Coppola ( ; born April 7, 1939), also credited as Francis Coppola, is a semi-retired American film director, producer, screenwriter and film composer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Godfather Part II was directed by Coppola, not Basil Dean; claim false."
  }
 },
 {
  "aid": "c00439",
  "kind": "yes/no",
  "text": "Claim: Buffalo Rock produced a drink under its own name that along with Izze are not both soft drinks.\n\nPassages:\n\n[Buffalo Rock]\nIn addition to bottling Pepsi products, the company produced Grapico in 1981, a grape-flavored soft drink, and a ginger ale under its own brand name.\n\n[Izze]\nIzze is an all-natural, no-preservatives-added fruit soda.\n\n[Grapico]\nGrapico is a caffeine-free, artificially flavored carbonated soft drink with a purple color and a grape taste that is sold in the Southeastern United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Ginger ale and Izze fruit soda are both soft drinks, so 'not both soft drinks' is false."
  }
 },
 {
  "aid": "c00440",
  "kind": "yes/no",
  "text": "Claim: Natalie Martinez is know for her role in the 2008 American-German-British speculative fiction action thriller Death Race.\n\nPassages:\n\n[Natalie Martinez]\nNatalie Martinez (born July 12, 1984) is an American actress and model. She is known as the spokes-model for JLO by Jennifer Lopez, and for her role in the 2008 feature film \"Death Race\".\n\n[Death Race (film)]\nDeath Race is a 2008 American-German-British science fiction action thriller film produced, written, and directed by Paul W. S. Anderson and starring Jason Statham.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Science fiction is a kind of speculative fiction; role in 2008 Death Race and the film's origins are supported."
  }
 },
 {
  "aid": "c00441",
  "kind": "yes/no",
  "text": "Post: Motivation Wednesday Night:\n\nI AM the powerhouse of the cell.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.5
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Meme-style hyperbolic self-motivation; could be playful exaggeration or self-mocking irony."
  }
 },
 {
  "aid": "c00442",
  "kind": "yes/no",
  "text": "Claim: The luxury hotel which Gideon Putnam built it's city is located on Broadway.\n\nPassages:\n\n[Grand Union Hotel (Saratoga Springs, New York)]\nThe Grand Union Hotel was located on Broadway in Saratoga Springs, New York.\n\n[Gideon Putnam]\nHe also worked as a miller and built the city's Grand Union and Congress Hotels.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Putnam built the Grand Union, which is on Broadway; only 'luxury' is unsupported."
  }
 },
 {
  "aid": "c00443",
  "kind": "yes/no",
  "text": "Post: that moment when a winter storm keeps people at home more than the pandemic has.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Wry ironic observation but literally true; sarcasm reading and sincere reading both defensible."
  }
 },
 {
  "aid": "c00444",
  "kind": "yes/no",
  "text": "Tweet: My dream is to be left alone.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Reads as a sincere wish; little signal of irony, but intent unclear."
  }
 },
 {
  "aid": "c00445",
  "kind": "yes/no",
  "text": "Claim: The publication with Mai Badr as deputy editor-in-chief is published in the region where Lida Fleitmann Bloodgood was an author and horsewoman. This region was not America. The magazine Closer is also published in this region.\n\nPassages:\n\n[Sayidaty]\nSayidaty (Arabic سيدتي \"Sayyidatī\", meaning \"My Lady\" in English) is a weekly Arabic and a monthly English women's magazine published in both Dubai and Beirut and distributed throughout the Middle East, North Africa, Europe and America.\n\n[Lida Fleitmann Bloodgood]\nLida Louise Fleitmann Bloodgood (1894-1982), was an author, and a horsewoman in both America and Europe.\n\n[Mai Badr]\nMai Badr (born 6 July 1968) is the editor-in-chief of Hia magazine and deputy editor-in-chief of Sayidaty and Al Jamila.\n\n[Closer (magazine)]\nCloser is a British tabloid magazine published by Bauer Media Group.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Sayidaty is published in Dubai and Beirut, not Europe, where Bloodgood and Closer fit; the claim fails."
  }
 },
 {
  "aid": "c00446",
  "kind": "yes/no",
  "text": "Post: Learned that a Pokemon card I own has been selling for a high price lately so this is a great time to have no idea where my cards are.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "'Great time to have no idea where my cards are' is clearly ironic."
  }
 },
 {
  "aid": "c00447",
  "kind": "yes/no",
  "text": "Post: Started watching house of cards, 4 episodes in. Already I can see it was a good choice😄",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Plain positive remark about a show with a smiling emoji; nothing signals insincerity."
  }
 },
 {
  "aid": "c00448",
  "kind": "yes/no",
  "text": "Claim: Cliburn railway halt was a station situated on This railway that ran between Clifton Junction junction Penrith and Kirkby Stephen via Appleby-in-Westmorland.\n\nPassages:\n\n[Eden Valley Railway]\nIt ran between Clifton Junction near Penrith and Kirkby Stephen via Appleby-in-Westmorland.\n\n[Cliburn railway station]\nCliburn railway station was a station situated on the Eden Valley Railway in Cumbria, England.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Gist supported, but 'halt' vs station and 'junction Penrith' vs near Penrith make the garbled claim arguable."
  }
 },
 {
  "aid": "c00449",
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
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Heck Army link and narrow upset supported, but passage says only 'first term', not Senate term."
  }
 }
]
