# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-008

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-008.json

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
  "aid": "a00400",
  "kind": "yes/no",
  "text": "Claim: George Juskalian took part in the seaborn invasion of French North Africa during WWII.\n\nPassages:\n\n[George Juskalian]\nDuring World War II, he served with the infantry during the North African Campaign and took part in Operation Torch.\n\n[Operation Torch]\nOperation Torch (initially called Operation Gymnast) was the British-United States invasion of French North Africa during the North African Campaign of the Second World War which started on 8 November 1942.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00401",
  "kind": "yes/no",
  "text": "Text: The fact I nearly froze on my way to work this morning is definitely a sign it's not summer anymore #freezing",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00402",
  "kind": "yes/no",
  "text": "Claim: The word and dice game, that Golden Secondary School hosts tournaments of, is originally distributed by a toy and game manufacturer that published more than 1,800 games.\n\nPassages:\n\n[Parker Brothers]\nParker Brothers was an American toy and game manufacturer which later became a brand of Hasbro. More than 1,800 games were published under the Parker Brothers name since 1883.\n\n[Golden Secondary School]\nCourses include things such as skiing and snowboarding on the beautiful Kicking Horse Mountain Resort, mountain biking on many trails around Golden and the school also hosts many bantam and senior basketball, volleyball and soccer teams, and Boggle tournaments.\n\n[Boggle]\nBoggle is a word game designed by Allan Turoff and originally distributed by Parker Brothers.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00403",
  "kind": "yes/no",
  "text": "Claim: Widewuto, a legendary ruler of the pagan Prussians, was believed to have existed before the army of the Teutonic Knights launched crusade against the Prussian peoples.\n\nPassages:\n\n[Widewuto]\nWidewuto (also \"Viduutus\", \"Vidvutus\", \"Witowudi\", \"Waidewut\") was a legendary king of the pagan Prussians who ruled along with his elder brother, the high priest Bruteno in the 6th century AD. It is unclear whether the legend was authentically Prussian (i.e. recorded from Prussian mythology) or was created by Grunau (possibly inspired by Biblical Moses and Aaron), though Lithuanian researchers tend to support in its authenticity.\n\n[Prussian mythology]\nThe Prussian mythology was a polytheistic religion of the Old Prussians, indigenous peoples of Prussia before the Prussian Crusade waged by the Teutonic Knights. No sources document pagan religion before the forced Christianization in the 13th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00404",
  "kind": "yes/no",
  "text": "Claim: Lou Dials played for the MLB organization Baltimore Orioles, and has a current majority owner named Peter Angelos.\n\nPassages:\n\n[Baltimore Orioles]\nThe Baltimore Orioles are an American professional baseball team based in Baltimore, Maryland. After 52 often-beleaguered years in St. Louis, the franchise was purchased in November 1953 by a syndicate of Baltimore business and civic interests led by attorney/civic activist Clarence Miles and Mayor Thomas D'Alesandro, Jr. The team's current majority owner is lawyer Peter Angelos.\n\n[Lou Dials]\nFrom 1938 to 1941, Dials played in the Mexican League. After his playing career, he became scout for the Houston Astros, Cleveland Indians and Baltimore Orioles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00405",
  "kind": "yes/no",
  "text": "Claim: Pitchfork referenced the name of this drummer in a review of the percussion by Carla Azar on the album Future Perfect. The bandmate of the keyboardist, who also worked with Nika Boon, is also a drummer.\n\nPassages:\n\n[Future Perfect]\nA Pitchfork review stated, \"In the first 10 seconds of the album opener, Carla Azar shames most every beat-maker with her ridiculous Leibezeit-cum-Bonham percussion\".\n\n[Nika Boon]\nShe is currently working on her new album (release 2017) in collaboration with musicians namely John Baggott (who plays keyboard & moogs for Massive Attack, Portishead, Robert Plant), Ian Matthews (drummer from Kasabian), Jay Stapley (guitarist associated with Pink Floyd and Mike Oldfield) and Carey Willetts (bass player from band Athlete).\n\n[Robert Plant discography]\nAlthough Plant avoided performing Led Zeppelin songs through much of this period, his tours in 1983 (with drummer Phil Collins) and 1985 were very successful, often performing to sold-out arena-sized venues.\n\n[John Bonham]\nJohn Henry Bonham (31 May 1948 – 25 September 1980) was an English musician and songwriter, best known as the drummer for the British rock band Led Zeppelin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00406",
  "kind": "yes/no",
  "text": "Claim: My Fair Lady is a musical based on this author's play \"Pygmalion\". The author had more influence on turn of the century literature than the writer of Nausea (novel).\n\nPassages:\n\n[My Fair Lady]\nMy Fair Lady is a musical based on George Bernard Shaw's \"Pygmalion\", with book and lyrics by Alan Jay Lerner and music by Frederick Loewe.\n\n[Jean-Paul Sartre]\nJean-Paul Charles Aymard Sartre ( ; ] ; 21 June 1905 – 15 April 1980) was a French philosopher, playwright, novelist, political activist, biographer, and literary critic.\n\n[George Bernard Shaw]\nGeorge Bernard Shaw ( ; 26 July 1856 – 2 November 1950), known at his insistence simply as Bernard Shaw, was an Irish playwright, critic and polemicist whose influence on Western theatre, culture and politics extended from the 1880s to his death and beyond.\n\n[Nausea (novel)]\nNausea (French: \"La Nausée\" ) is a philosophical novel by the existentialist philosopher Jean-Paul Sartre, published in 1938.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00407",
  "kind": "yes/no",
  "text": "Claim: The Man with the Iron Fists is a 2012 American martial arts film directed by RZA, the film stars RZA, and Russell Crowe, film producer and musician, and although a New Zealand citizen, he has lived most of his life in Australia.\n\nPassages:\n\n[Russell Crowe]\nRussell Ira Crowe (born 7 April 1964) is an actor, film producer and musician.\n\n[The Man with the Iron Fists]\nThe film stars RZA, Russell Crowe, Cung Le, Lucy Liu, Byron Mann, Rick Yune, Dave Bautista, and Jamie Chung.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00408",
  "kind": "yes/no",
  "text": "Claim: The town that is connected by a ferry to Kwadjokrom is a town in the Lake Volta region.\n\nPassages:\n\n[Krachi West District]\nThe Krachi West District is one of the twenty-five (25) districts in the Volta Region.\n\n[Kwadjokrom]\nKwadjokrom is connected by a ferry to the town of Kete Krachi.\n\n[Kete Krachi]\nKete Krachi is a town in the Krachi West District of the Volta Region of Ghana.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00409",
  "kind": "yes/no",
  "text": "Claim: More than 1,600 German scientists, engineers, and technicians, were recruited in post-Nazi Germany as a result of the clandestine operation where Arthur Rudolph became one of the main developers of the 1960s U.S. space program.\n\nPassages:\n\n[Arthur Rudolph]\nAfter the war, the United States Government's Office of Strategic Services (OSS) brought him to the U.S. as part of the clandestine Operation Paperclip, where he became one of the main developers of the U.S. space program.\n\n[Operation Paperclip]\nOperation Paperclip was a secret program of the Joint Intelligence Objectives Agency (JIOA) in which more than 1,600 German scientists, engineers, and technicians, such as Wernher von Braun and his V-2 rocket team, were recruited in post-Nazi Germany and taken to the U.S. for government employment, at the end of World War II; many were members and some were leaders of the Nazi Party.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00410",
  "kind": "yes/no",
  "text": "Tweet: Good morning to everyone again, except Eddie Reynoso, his lab rats &amp; whoever the fuck is letting Oscar Valdez fight after failing a drugs test - just because it would be bad for business.\n\nSome things more important than money, but not in boxing - clearly.\n\n❌💉",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00411",
  "kind": "yes/no",
  "text": "Text: every time i see someone named david im like ….. wow… that really IS a guy named david",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00412",
  "kind": "yes/no",
  "text": "Claim: In 2011 the population of the town where the band with a compilation double album called 24 Carat Purple were formed was about 26,000.\n\nPassages:\n\n[Hertford]\nForming a civil parish, the 2011 census put the population of Hertford at about 26,000.\n\n[24 Carat Purple]\n24 Carat Purple is the first compilation album of the hard rock band Deep Purple released worldwide on their own record company and the third in a long line of compilation albums.\n\n[Deep Purple]\nDeep Purple are an English rock band formed in Hertford in 1968.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00413",
  "kind": "yes/no",
  "text": "Text: Can cats wear nail polish",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00414",
  "kind": "yes/no",
  "text": "Claim: The 2003 edition of the game that the 2013 Hawaii Bowl is he eleventh edition of, matched the hometown team with the Houston Cougars. The former coach of the hometown team is now coaching the Canadian team, Hamilton Tiger-Cats.\n\nPassages:\n\n[2003 Hawaii Warriors football team]\nThe 2003 Hawaii Warriors football team represented the University of Hawaii at Manoa in the 2003 NCAA Division I-A football season. The Warriors capped off their second straight winning season, and the fourth in five seasons, under head coach June Jones with a bowl win.\n\n[2013 Hawaii Bowl]\nThe twelfth edition of the Hawaii Bowl, it featured the Boise State Broncos from the Mountain West Conference against the Oregon State Beavers from the Pac-12 Conference.\n\n[June Jones]\nJune Sheldon Jones III (born February 19, 1953) is an American football coach and former player, currently serving as a head coach of the Hamilton Tiger-Cats of the Canadian Football League (CFL).\n\n[2003 Hawaii Bowl]\nThe 2003 Sheraton Hawaii Bowl matched the hometown Hawaii Warriors with the Houston Cougars.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00415",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Cold queso is gross and warm queso is so much better.",
   "cold queso is so much better than warm queso https://t.co/5TaMe4aSO6"
  ],
  "human_label": "cold queso is so much better than warm queso https://t.co/5TaMe4aSO6",
  "read_1": {
   "answer": "Cold queso is gross and warm queso is so much better.",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "Cold queso is gross and warm queso is so much better.",
   "confidence": 0.4
  }
 },
 {
  "aid": "a00416",
  "kind": "yes/no",
  "text": "Claim: The 2000 French crime thriller starred the writer and director Virginie Despentes and Coralie Trinh Thi.\n\nPassages:\n\n[Baise-moi]\nBaise-moi (\"Fuck me \") is a 2000 French crime thriller film with elements of a rape and revenge film written and directed by Virginie Despentes and Coralie Trinh Thi and starring Karen Lancaume and Raffaëla Anderson.\n\n[Coralie Trinh Thi]\nCoralie Trinh Thi (born April 11, 1976) is a former pornographic actress and French author, also known for writing and directing with Virginie Despentes the film \"Baise-moi\" (2000).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
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
  "aid": "a00417",
  "kind": "yes/no",
  "text": "Claim: The superhero Thor is followed in the American comic novel series that started as a horror comics anthology and introduced the fictional realm based on Norse mythology.\n\nPassages:\n\n[Asgard (comics)]\nBased on the realm of the same name from Norse mythology, Asgard is home to the Asgardians and other beings adapted from Norse mythology. Asgard first appeared in \"Journey into Mystery\" #83 (October 1962) by Stan Lee, Larry Lieber and Jack Kirby, and features prominently in stories that follow the Marvel Comics superhero, Thor.\n\n[Journey into Mystery]\nJourney into Mystery is an American comic book series initially published by Atlas Comics, then by its successor, Marvel Comics. Initially a horror comics anthology, it segued to giant-monster and science fiction stories in the late 1950s.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00418",
  "kind": "yes/no",
  "text": "Claim: In between Splash and Son of Flubber, the first one was directed by Ron Howard.\n\nPassages:\n\n[Splash (film)]\nSplash is a 1984 American fantasy romantic comedy film directed by Ron Howard, written by Lowell Ganz and Babaloo Mandel, and starring Tom Hanks, Daryl Hannah, John Candy, and Eugene Levy.\n\n[Son of Flubber]\nSon of Flubber is the 1963 sequel to the Walt Disney children's sci-fi comedy movie \"The Absent-Minded Professor\" (1961).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00419",
  "kind": "yes/no",
  "text": "Claim: The director of The Possession of Joel Delaney is not an actor. Neither is the director of Fierrot le pou.\n\nPassages:\n\n[The Possession of Joel Delaney]\nThe Possession of Joel Delaney is a 1972 American horror film directed by Waris Hussein and starring Shirley MacLaine and Perry King.\n\n[Fierrot le pou]\nFierrot le pou is a 1990 French 8-minute short film directed by Mathieu Kassovitz, his debut film.\n\n[Mathieu Kassovitz]\nMathieu Kassovitz (born 3 August 1967) is a French director, screenwriter, producer, editor, and actor probably best known in Francophone countries for his role as Nino Quincampoix in \"Amélie\" (\"Le Fabuleux Destin d'Amélie Poulain\"; 2001).\n\n[Waris Hussein]\nWaris Hussein (born 9 December 1938) is a British-Indian television director and film director best known for his many productions for British television, including \"Doctor Who\" and the \"Play of the Month\" version of \"A Passage to India\" (1965).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00420",
  "kind": "yes/no",
  "text": "Claim: Major General Walter E. Lauer commanded this unit in a conflict. This unit from world war 2 had a twenty year old lieutenant. The Enemy Strikes is a documentary about the conflict.\n\nPassages:\n\n[Walter E. Lauer]\nDuring World War II he commanded the 99th Infantry Division in the Battle of the Bulge.\n\n[99th Infantry Division (United States)]\nThe 99th Infantry Division was a unit of the United States Army in World War II.\n\n[Lyle Bouck]\nLyle Joseph Bouck, Jr. (December 17, 1923 – December 2, 2016) enlisted in the U.S. National Guard at age 14.\n\n[The Enemy Strikes]\nis a short propaganda film made in 1945 about the Battle of the Bulge.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00421",
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
  }
 },
 {
  "aid": "a00422",
  "kind": "yes/no",
  "text": "Claim: The grandfather of Rainer Hoss conducted the negotiations with the owners and was the commandant of Auschwitz concentration and extermination camp.\n\nPassages:\n\n[Gerstein Report]\nThe Gerstein Report was written in 1945 by Kurt Gerstein, an Obersturmführer (First Lieutenant) of the Waffen-SS who rose to become the Head of Technical Disinfection Services of the SS, and in that capacity supplied hydrogen cyanide (Zyklon B) from Degesch (\"Deutsche Gesellschaft für Schädlingsbekämpfung\") to Rudolf Höss in Auschwitz and conducted the negotiations with the owners.\n\n[Rudolf Höss]\nRudolf Höss (also Höß, Hoeß or Hoess; 25 November 1901 – 16 April 1947) was a Nazi German \"SS\"-\"Obersturmbannführer\" (lieutenant colonel) and the longest-serving commandant of Auschwitz concentration and extermination camp in World War II.\n\n[Rainer Höss]\nRainer Höss, born 25 May 1965 in Stuttgart, is the grandson of Rudolf Höss.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
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
  "aid": "a00423",
  "kind": "yes/no",
  "text": "Claim: The Hockey League which drafted Niclas Bergfors was based in Newark, New Jersey.\n\nPassages:\n\n[Niclas Bergfors]\nHe was drafted by the National Hockey League (NHL)'s New Jersey Devils in the first round, 23rd overall, at the 2005 NHL Entry Draft, playing for the organization for four-and-a-half seasons before joining the Atlanta Thrashers 2010, Florida Panthers in 2011 and Nashville Predators via free agency in 2011.\n\n[New Jersey Devils]\nThe New Jersey Devils are a professional ice hockey team based in Newark, New Jersey.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00424",
  "kind": "yes/no",
  "text": "Post: #DominicCummings Sack him. Or better yet, charge him.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "no",
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
  "aid": "a00425",
  "kind": "yes/no",
  "text": "Claim: The Magic Roundabout is a 2005 French-British, computer-animated, adventure fantasy film based on the comedic television series The Magic Roundabout.\n\nPassages:\n\n[Ray Winstone]\nHe has also become well known as a voice over actor, and has recently branched out into film production.\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00426",
  "kind": "yes/no",
  "text": "Text: is it illegal to discriminate against someone on the basis that they have a joker tattoo",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
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
  "aid": "a00427",
  "kind": "yes/no",
  "text": "Claim: The nationality of the stage costume designer of Homage to the Queen was English.\n\nPassages:\n\n[Homage to the Queen]\nHomage to the Queen, Op. 42, by Malcolm Arnold was written as the official coronation ballet in 1953, commissioned by the Sadler's Wells Ballet in honour of Queen Elizabeth II, the ballet company's musical adviser Humphrey Searle having recommended Arnold for the job. It was first performed by the Sadler's Wells Ballet on Coronation night 2 June 1953 at the Royal Opera House Covent Garden, with original scenery and costumes by Oliver Messel.\n\n[Oliver Messel]\nOliver Hilary Sambourne Messel (13 January 1904 – 13 July 1978) was an English artist and one of the foremost stage designers of the 20th century.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00428",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "He should not have been elected president and donald trump won the presidency.",
   "Replace Pelosi #Nancy"
  ],
  "human_label": "Replace Pelosi #Nancy",
  "read_1": {
   "answer": "He should not have been elected president and donald trump won the presidency.",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "He should not have been elected president and donald trump won the presidency.",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00429",
  "kind": "yes/no",
  "text": "Claim: Rocky Boy's Indian Reservation is located in Hill and Chouteau and named after the principal leader of the Montana Chippewa-Cree.\n\nPassages:\n\n[Rocky Boy's Indian Reservation]\nRocky Boy's Indian Reservation is one of seven American Indian reservations in the U.S. state of Montana. The reservation is located in Hill and Chouteau counties in northeastern Montana, about 40 mi from the Canada–U.S. border.\n\n[Rocky Boy (Chippewa leader)]\nAsiniiwin, translated Rocky Boy or Stone Child was an important Chippewa leader who became the principal leader of the Montana Chippewa-Cree in the late 19th century and early 20th century.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00430",
  "kind": "yes/no",
  "text": "Claim: The actor and film director of the 1990s crime thriller, won his first Academy Award for The Usual Suspects. They have since collaborated with the director of the 2014 film \"The Guvnors\".\n\nPassages:\n\n[The Guvnors]\nThe Guvnors is a 2014 film directed by Gabe Turner.\n\n[Gabe Turner]\nHe has worked as a Producer, Director and Writer who regularly collaborates on TV and film projects featuring some of the worlds most recognised actors and sports stars including Meryl Streep, Arnold Schwarzenegger, David Beckham, James Corden, Billy Crystal and Kevin Spacey.\n\n[Kevin Spacey]\nHe gained critical acclaim in the early 1990s that culminated in his first Academy Award for Best Supporting Actor for the neo-noir crime thriller \"The Usual Suspects\" (1995), and an Academy Award for Best Actor for midlife crisis-themed drama \"American Beauty\" (1999).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00431",
  "kind": "yes/no",
  "text": "Text: Uh oh Ben Simmons will also have a Steph Curry type season 76ers better not trade him now https://t.co/kkpzfcTcSH",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
  "aid": "a00432",
  "kind": "yes/no",
  "text": "Post: my greatest downfall is having an upset stomach then eating spicy food to make it worse.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
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
  "aid": "a00433",
  "kind": "yes/no",
  "text": "Claim: The composer, for the music in the film soundtrack reworked by this group, was born in Rhode Island. The name of this group is also the title of an album by the band that did Ancient Cross Dressing Songs.\n\nPassages:\n\n[Melora a la Basilica]\nIt is a collection of previous Rasputina songs reworked with new band member Daniel DeJesus and covers of songs by Goldfrapp, Pearl Jam and the Sweeney Todd and A Clockwork Orange soundtracks.\n\n[A Clockwork Orange (soundtrack)]\nThe soundtrack of \"A Clockwork Orange\" comprises classical music and electronic synthetic music composed by Wendy Carlos (then Walter Carlos).\n\n[Wendy Carlos]\nBorn and raised in Rhode Island, Carlos studied physics and music at Brown University before moving to New York City in 1962 to study music composition at Columbia University.\n\n[Ancient Cross-Dressing Songs]\nMuch like their two previous EPs, Melora a la Basilica and The Willow Tree Triptych, the album is available only via the band's website and is hand-crafted by Creager herself.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00434",
  "kind": "yes/no",
  "text": "Claim: The NorthCap University is located in India, but the establishment, where Nicanor Tiongson studied his Ph.D. in the national university of the Philippines, is not.\n\nPassages:\n\n[University of the Philippines]\nThe University of the Philippines (UP; Filipino: \"Unibersidad ng Pilipinas\" or \"Pamantasan ng Pilipinas\") is a state university system in the Philippines.\n\n[Nicanor Tiongson]\nHe holds a Bachelor of Humanities degree from the Ateneo de Manila University, and M.A. and Ph.D. in Philippine Studies from the University of the Philippines.\n\n[The Northcap University]\nThe NorthCap University, formerly ITM University, is an autonomous university situated in Sector 23-A, Gurugram, Haryana, India.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00435",
  "kind": "yes/no",
  "text": "Claim: The biographer who was admitted to mental asylum at High Beach upon which the book The Quickening Maze is base, teaches English Literature at the University of Oxford.\n\nPassages:\n\n[The Quickening Maze]\nThe book is based on the historical backdrop of a mental asylum run by Matthew Allen at High Beach in late 1830s and 1840s which had English poet John Clare admitted therein.\n\n[John Clare]\nHis biographer Jonathan Bate states that Clare was \"the greatest labouring-class poet that England has ever produced.\n\n[Jonathan Bate]\nHe is Professor of English Literature at the University of Oxford, Provost of Worcester College, Oxford, and Honorary Fellow of Creativity at Warwick Business School.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00436",
  "kind": "yes/no",
  "text": "Claim: People's Republic of China politician Wan Da was born in this location. It has a larger population than area where the Liaoning Finance and Trade College is located.\n\nPassages:\n\n[Xingcheng]\nXingcheng (), former name Ningyuan (宁远), is a county-level city of southwest Liaoning province, China, with a population of approximately 140,000 urban inhabitants, and is located on the Liaodong Bay, i.e. the northern coast of the Bohai Sea.\n\n[Wan Da]\nHe was born in Linzhou, Henan.\n\n[Liaoning Finance and Trade College]\nLiaoning Finance and Trade College (), formerly known as Shenyang Shifan University Bohai College, is a small, partially walled private undergraduate college located on the Liaodong Bay of the Bohai coast in Xingcheng, southwest of Huludao in Liaoning province on the east coast of China.\n\n[Linzhou, Henan]\nIt covers an area of 2046 square kilometers and has a population of about one million.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00437",
  "kind": "yes/no",
  "text": "Claim: Carlos Ashley Raphael \"Carl\" Barât has been in more bands in his life than another singer/songwriter. This singer/songwriter fronted a punk band who released Expansive Heart.\n\nPassages:\n\n[Carl Barât]\nCarlos Ashley Raphael Barât (born 6 June 1978) is a British musician, best known for being the co-frontman with Peter Doherty of the garage rock band The Libertines. He was the frontman and lead guitarist of Dirty Pretty Things, and in 2010 debuted a solo album. In 2014 he announced the creation of his new band, The Jackals.\n\n[Expansive Heart]\nExpansive Heart is the only piece ever released by punk band Big Rig, it was released on the Lookout!\n\n[Big Rig (band)]\nBig Rig was a punk band from the San Francisco Bay Area fronted by singer/songwriter Jesse Michaels.\n\n[Jesse Michaels]\nJesse Michaels is a songwriter, vocalist, guitarist and artist from Berkeley, California. He is most well known as the vocalist for the ska punk band Operation Ivy.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00438",
  "kind": "yes/no",
  "text": "Claim: The person who established the Americas Society in 1965 was the chairman of Chase Manhattan Bank. This person was a sibling of the leader of Japan Society.\n\nPassages:\n\n[John D. Rockefeller III]\nHis siblings were Abby, Nelson, Laurance, Winthrop, and David.\n\n[David Rockefeller]\nDavid Rockefeller (June 12, 1915 – March 20, 2017) was an American banker who was chairman and chief executive of Chase Manhattan Corporation.\n\n[Americas Society]\nThe Americas Society was established by David Rockefeller in 1965.\n\n[Japan Society (Manhattan)]\nAfter suspending all activities during World War II, Japan Society expanded under the leadership of John D. Rockefeller III.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00439",
  "kind": "yes/no",
  "text": "Claim: Charles Bronson the Actor whose birth name was Charles Dennis Buchinsky, was part of the Leslie Nielsen comedy.\n\nPassages:\n\n[Charles Bronson]\nCharles Bronson (born Charles Dennis Buchinsky; Lithuanian: \"Karolis Dionyzas Bučinskis\" ; November 3, 1921 – August 30, 2003) was an American actor.\n\n[Allan A. Goldstein]\nAllan A. Goldstein (born May 23, 1949) is an American film director and screenwriter, perhaps best known for directing the Charles Bronson vehicle \"\" and the Leslie Nielsen comedy \"\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00440",
  "kind": "yes/no",
  "text": "Claim: T. Arthur Cottam received an Artistic Director Achievement Award from the Valley Theatre League for his role in this play believed to have been written in 1603.\n\nPassages:\n\n[Othello]\nOthello (\"The Tragedy of Othello, the Moor of Venice)\" is a tragedy by William Shakespeare, believed to have been written in 1603.\n\n[T. Arthur Cottam]\nHe acted in theatre, and received an Artistic Director Achievement Award from the Valley Theatre League for his role in the theatre production \"Othello\" as a cast member of Zombie Joe's Underground Theatre Group.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
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
  "aid": "a00441",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Ed Sheeran isn't at Tramlines and I'm glad about it",
   "Can’t wait to see Ed sheeran at tramlines tomoz x"
  ],
  "human_label": "Can’t wait to see Ed sheeran at tramlines tomoz x",
  "read_1": {
   "answer": "Ed Sheeran isn't at Tramlines and I'm glad about it",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "Ed Sheeran isn't at Tramlines and I'm glad about it",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00442",
  "kind": "yes/no",
  "text": "Claim: Mark Chamberlain and Alex Oxlade-Chamberlain were being an English professinal footballer.\n\nPassages:\n\n[Alex Oxlade-Chamberlain]\nAlexander Mark David Oxlade-Chamberlain (born 15 August 1993) is an English professional footballer who plays as a midfielder for Premier League club Liverpool and the England national team.\n\n[Mark Chamberlain]\nMark Valentine Chamberlain (born 19 November 1961) is an English former international footballer. He is the younger brother of Neville Chamberlain, and the father of Liverpool and England international player Alex Oxlade-Chamberlain and Portsmouth's Christian Oxlade-Chamberlain.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00443",
  "kind": "yes/no",
  "text": "Claim: In this religion, where Mehet-Weret is a godess of the sky, a person would be weighted against the feather of truth to decide if they where worthy of damnation and would face the torment in the lake of fire.\n\nPassages:\n\n[Ancient Egyptian religion]\nAncient Egyptian religion was a complex system of polytheistic beliefs and rituals which were an integral part of ancient Egyptian society.\n\n[Mehet-Weret]\nMehet-Weret \"(mḥ.t-wr.t)\" is a goddess of the sky in Ancient Egyptian religion. Her name means \"Great Flood\".\n\n[Damnation]\nIn Ancient Egyptian religious tradition, citizens would recite the 42 negative confessions of Maat as their heart was weighed against the feather of truth.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00444",
  "kind": "yes/no",
  "text": "Claim: The main character in the biographical war drama, which co-starred Spencer Lofranco, was an Olympic distance runner in the World War II.\n\nPassages:\n\n[Louis Zamperini]\nLouis Silvie \"Louie\" Zamperini (January 26, 1917 – July 2, 2014) was a US prisoner of war survivor in World War II, a Christian evangelist and an Olympic distance runner.\n\n[Unbroken (film)]\nThe film revolves around the life of USA Olympian and army officer Louis \"Louie\" Zamperini.\n\n[Spencer Lofranco]\nHe then co-starred as Harry Brooks in the biographical war drama \"Unbroken\" (2014) and Billy in the crime drama \"Dixieland\" (2015).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00445",
  "kind": "yes/no",
  "text": "Post: the way uni won’t give me extra time on assessments despite them replacing exams (which i get time for) because of covid 🤩🤩🥰😍",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
  "aid": "a00446",
  "kind": "yes/no",
  "text": "Claim: Singer Eddie Fisher, who produced the album \"I'm in the Mood for Love\" in 1952, later had a scandalous affair with the actress Elizabeth Taylor.\n\nPassages:\n\n[Eddie Fisher (singer)]\nFisher divorced his first wife, actress Debbie Reynolds, to marry Reynolds' best friend, actress Elizabeth Taylor, after Taylor's husband, film producer Mike Todd, was killed in a plane crash. The scandalous affair was widely reported, bringing unfavorable publicity to Fisher.\n\n[I'm in the Mood for Love (Eddie Fisher album)]\nI'm in the Mood for Love is the name of a 1952 album by Eddie Fisher, reissued in 1955, featuring the song of the same name.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00447",
  "kind": "yes/no",
  "text": "Claim: Nobody Loves You was written by John Lennon and released on the album, Walls and Bridges, which was issued by Apple Records, and was written, recorded, and released during his 18 month separation from artist Yoko Ono.\n\nPassages:\n\n[Nobody Loves You (When You're Down and Out)]\n\"Nobody Loves You (When You're Down and Out)\" is a song written by John Lennon released on his 1974 album \"Walls and Bridges\".\n\n[Walls and Bridges]\nIt was issued by Apple Records on 26 September 1974 in the United States and on 4 October in the United Kingdom. Written, recorded and released during his 18-month separation from Yoko Ono, the album captured Lennon in the midst of his \"Lost Weekend\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00448",
  "kind": "yes/no",
  "text": "Claim: The player who teamed up with Elena Bovina for the 2003 Family Circle Cup – Doubles. Her and Renáta Tomanová were both tennis players.\n\nPassages:\n\n[Rennae Stubbs]\nRennae Stubbs (born 26 March 1971) is an Australian retired tennis player.\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.\n\n[2003 Family Circle Cup – Doubles]\nLisa Raymond and Rennae Stubbs were the defending champions, but Raymond did not compete in this edition.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00449",
  "kind": "yes/no",
  "text": "Claim: Dave Thomas, who also founded the Dave Thomas Foundation for Adoption, the non-for-profit organization dedicated to find adoptive homes for children waiting in North America's foster care system that was named for Wendy, who is also the namesake and mascot of the company founded Wendy's.\n\nPassages:\n\n[Dave Thomas Foundation for Adoption]\nThe Dave Thomas Foundation for Adoption is a not-for-profit organization dedicated to finding adoptive homes for children waiting in North America’s foster care system.\n\n[Wendy Thomas]\nMelinda Lou \"Wendy\" Morse (née Thomas; born September 14, 1961) is the daughter and fourth child of American businessman Dave Thomas, the founder of the fast food brand Wendy's. Morse is best known for being the namesake and mascot of the brand.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 }
]
