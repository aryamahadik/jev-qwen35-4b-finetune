# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-010

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-010.json

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
  "aid": "a00500",
  "kind": "yes/no",
  "text": "Claim: Caroline Grace Cassidy is best known for her role in the film which Ben Best was the co-writer. The director of this movie and Larry Hagman are not both actors.\n\nPassages:\n\n[Ben Best (screenwriter)]\nHe also co wrote the films \"The Foot Fist Way\" and \"Your Highness\".\n\n[Larry Hagman]\nLarry Martin Hagman (September 21, 1931 November 23, 2012) was an American film and television actor, director and producer best known for playing ruthless oil baron J.R. Ewing in the 1980s primetime television soap opera \"Dallas\" and befuddled astronaut Major Anthony \"Tony\" Nelson in the 1960s sitcom, \"I Dream of Jeannie\".\n\n[Caroline Grace Cassidy]\nShe is best known for her role in David Gordon Green's \"Your Highness\".\n\n[David Gordon Green]\nDavid Gordon Green (born April 9, 1975) is an American filmmaker.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00501",
  "kind": "yes/no",
  "text": "Claim: Planet 51 from 2009 was 3D. The 2009 animated film written and directed by Phil Lord and Christopher Miller was not in 3D.\n\nPassages:\n\n[Planet 51]\nPlanet 51 is a 2009 Spanish and American-British-movie 3D computer-animated science fiction comedy film directed by Jorge Blanco, written by Joe Stillman, and starring Dwayne Johnson, Jessica Biel, Justin Long, Gary Oldman, Seann William Scott, and John Cleese.\n\n[Phil Lord and Christopher Miller]\nThey are known for directing and writing the animated films \"Cloudy with a Chance of Meatballs\" (2009) and \"The Lego Movie\" (2014), as well as directing the live-action comedy film \"21 Jump Street\" (2012) and its sequel (2014).\n\n[Cloudy with a Chance of Meatballs (film)]\nCloudy with a Chance of Meatballs is a 2009 American computer-animated science fiction comedy film loosely based on the 1978 children's book of the same name by Judi and Ron Barrett.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00502",
  "kind": "yes/no",
  "text": "Claim: The backing vocalist on \"We've Had Enough\" is known for playing in punk bands and Rome Ramirez isn't.\n\nPassages:\n\n[Rome Ramirez]\nRoman René Ramírez (born June 11, 1988 in Fremont, California), better known as Rome Ramirez or simply Rome, is an American singer and guitarist best known for playing with Eric Wilson from Sublime and Josh Freese from The Vandals in the band Sublime with Rome.\n\n[Keith Morris]\nKeith Morris (born September 18, 1955) is an American singer and songwriter known for his role as frontman of the hardcore punk bands Black Flag, Circle Jerks, and Off!\n\n[We've Had Enough]\n\"We've Had Enough\" features backing vocals by Keith Morris, singer of the Circle Jerks and original singer of Black Flag.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00503",
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
  }
 },
 {
  "aid": "a00504",
  "kind": "yes/no",
  "text": "Claim: Witch Alder, the relative of Fothergilla major, is one of two species in its genus. Plants are the type of vegetation that that genus and Clerodendrum have in common.\n\nPassages:\n\n[Clerodendrum]\nClerodendrum is a genus of flowering plants in the family Lamiaceae.\n\n[Fothergilla]\nFothergilla (witch alder) is a genus of two or three species of flowering plants in the family Hamamelidaceae, native to woodland and swamps of the southeastern United States.\n\n[Fothergilla gardenii]\nIt is one of two species in the genus \"Fothergilla.\"\n\n[Fothergilla major]\nFothergilla major (large witch alder, mountain witch alder) is a species of flowering plant in the genus Fothergilla, family Hamamelidaceae, that is native to woodland and swamps in the Allegheny Mountains of southeastern United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00505",
  "kind": "yes/no",
  "text": "Text: Searching for Pokemon later because I hate myself haha !!!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
  "aid": "a00506",
  "kind": "yes/no",
  "text": "Post: quit a high paying job for a blind fantasy with no family, no friends, no backup plan… deserved every tear streaming down his face https://t.co/y7KxPh3hwx",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00507",
  "kind": "yes/no",
  "text": "Tweet: Loving how much #narcissism and it's intra- and interpersonal aspects are playing out in #Lokiepisode2 #Disney #Marvel",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00508",
  "kind": "yes/no",
  "text": "Claim: The canal that has historic remnants in Beaver Creek State Park, did not remain operational until a later date than the Los Angeles Aqueduct\n\nPassages:\n\n[Beaver Creek State Park]\nHistoric remnants of the Sandy and Beaver Canal can be found throughout the park.\n\n[Los Angeles Aqueduct]\nThe Los Angeles Aqueduct system, comprising the Los Angeles Aqueduct (Owens Valley aqueduct) and the Second Los Angeles Aqueduct, is a water conveyance system, built and operated by the Los Angeles Department of Water and Power. The system delivers water from the Owens River in the Eastern Sierra Nevada Mountains to Los Angeles, California. In 1971 it was recognized by the American Society of Civil Engineers on the List of Historic Civil Engineering Landmarks.\n\n[Sandy and Beaver Canal]\nThe Sandy and Beaver Canal ran 73 mi from the Ohio and Erie Canal at Bolivar, Ohio, to the Ohio River at Glasgow, Pennsylvania. The canal ceased to operate in 1852, when the Cold Run Reservoir Dam outside of Lisbon, Ohio, broke, ruining a large portion of the canal.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00509",
  "kind": "yes/no",
  "text": "Claim: \"I Do\" the song by Filipino singer Nina and described to be Mariah Carey-like was on third studio album, \"Nina\".\n\nPassages:\n\n[Mariah Carey]\nMariah Carey (born March 27, 1969 or 1970) is an American singer, songwriter, record producer, and actress.\n\n[I Do (Nina Girado song)]\n\"I Do\" is a song by Filipino singer Nina from her self-titled third studio album, \"Nina\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00510",
  "kind": "yes/no",
  "text": "Claim: A medieval castle, which is near to Wallace's Cave, is located downstream relative to a castle 9 miles south of Edinburgh\n\nPassages:\n\n[Wallace's Cave]\nIt is also known as Hawthornden Castle Cave, after Hawthornden Castle which is nearby.\n\n[Roslin Castle]\nIt is located around 9 miles south of Edinburgh, on the north bank of the North Esk, only a few hundred metres from the famous Rosslyn Chapel.\n\n[Hawthornden Castle]\nThe castle lies a mile to the east of Roslin at grid reference [ NT287637] , and is just downstream from Roslin Castle.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00511",
  "kind": "yes/no",
  "text": "Text: If anyone wants to know how my nights going I tried making a private story on Snapchat and instead made a group chat... I hate my life",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
  "aid": "a00512",
  "kind": "yes/no",
  "text": "Claim: Kyriakos Georgiou is best known for playing this role. The man who he won the organisation's Tag Team Championship with is Canadian. Vengeance was a 2006 event produced by the organisation.\n\nPassages:\n\n[Vladimir Kozlov]\nHe is best known for his time in WWE, where he won the WWE Tag Team Championship once with Santino Marella.\n\n[Vengeance (2006)]\nVengeance (2006) was a professional wrestling pay-per-view (PPV) event produced by World Wrestling Entertainment (WWE), which took place on June 25, 2006, at the Charlotte Bobcats Arena in Charlotte, North Carolina.\n\n[Kyriakos Georgiou]\nHe is best known for playing the role of 'Vladimir Kozlov' in the films Criminals Game/Criminals Game II, he has also starred as James Baker in the film 'Duality' (\"written and directed by Jaimal Patel\").\n\n[Santino Marella]\nAnthony Carelli (born March 14, 1974) is a Canadian sports analyst, trainer, entrepreneur, actor, and retired professional wrestler and mixed martial artist, who currently works for the Canadian sports TV network Sportsnet.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00513",
  "kind": "yes/no",
  "text": "Claim: Interbol is an international space project under the leadership of the Russian Space Agency and the Space Research Institute of the Russian Academy of Sciences, the goal being to study the correlations between which items can simply be considered as a gaseous mixture of negatively charged electrons and highly charged positive ions; true plasma production, however, is from the distinct separation of these ions and electrons that produces an electric field, which in turn, produces electric currents and magnetic fields, in the tail of the magnetosphere and in the Van Allen radiation belt.\n\nPassages:\n\n[Interbol]\nInterbol (Russian: Интербол ) is an international space project under the leadership of the Russian Space Agency and the Space Research Institute of the Russian Academy of Sciences.\n\n[Plasma (physics)]\nPlasma (from Ancient Greek πλάσμα , meaning \"moldable substance\" or \"jelly\") can simply be considered as a gaseous mixture of negatively charged electrons and highly charged positive ions, however, true plasma production is from the distinct separation of these ions and electrons that produces an electric field, which in turn, produces electric currents and magnetic fields. Plasma is one of the four fundamental states of matter and was first introduced by chemist Irving Langmuir in the 1920s.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00514",
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
  }
 },
 {
  "aid": "a00515",
  "kind": "yes/no",
  "text": "Claim: The host of the show that featured LA Urban Rangers provided the voice of Backson in the Disney Channel's 51st the Disney Channel animated feature film.\n\nPassages:\n\n[LA Urban Rangers]\nTheir most recent and longest-running outing - the Malibu Public Beach Safari - has been featured in media reports and by Huell Howser on his show.\n\n[Winnie the Pooh (2011 film)]\nIt is the 51st Disney animated feature film.\n\n[Huell Howser]\nHuell Burnley Howser (October 18, 1945 – January 7, 2013) was an American television personality, actor, producer, writer, singer, and voice artist, best known for hosting, producing, and writing \"California's Gold\", his human interest show produced by KCET in Los Angeles for California PBS stations. He also voiced the Backson in \"Winnie the Pooh\" (2011).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00516",
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
  }
 },
 {
  "aid": "a00517",
  "kind": "yes/no",
  "text": "Post: \"calm down, I've only had it a couple weeks\" 🤨😒",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00518",
  "kind": "yes/no",
  "text": "Claim: The show, in which the host of this show also hosted, usually aired on Monday at 7 pm. Rosie Goldsmith hosted it, as well as Crossing Continents.\n\nPassages:\n\n[Rosie Goldsmith]\nShe was the host of the shows Crossing Continents, and A World in Your Ear.\n\n[The Krypton Factor]\nThe show originally ran from 7 September 1977 to 20 November 1995, and was hosted by Gordon Burns and usually broadcast on the ITV network on Mondays at 7pm.\n\n[Gordon Burns]\nHe was the host of \"The Krypton Factor\" for its original 18-year run (1977–1995) and was the chief anchorman for the BBC regional news programme \"North West Tonight\" from January 1997 to October 2011.\n\n[A Word in Your Ear]\nIt was hosted by Gordon Burns.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00519",
  "kind": "yes/no",
  "text": "Claim: The town Shelley Watts was born in is a larger town than Bonny Hills. Cyneoterpna wilsoni is found in this town.\n\nPassages:\n\n[Bonny Hills, New South Wales]\nBonny Hills is a town in New South Wales, Australia about 30 minutes drive south of Port Macquarie. As of the 2011 census, it had a population of 2,870 people.\n\n[Shelley Watts]\nShelley Watts (born 10 August 1987 in Port Macquarie) is an amateur boxer from Australia.\n\n[Cyneoterpna wilsoni]\nIt is found in Queensland, New South Wales, Victoria, South Australia and Tasmania.\n\n[Port Macquarie]\nPort Macquarie is a coastal town in the local government area of Port Macquarie-Hastings. The town with its suburbs had a population of 45,698 in June 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00520",
  "kind": "yes/no",
  "text": "Claim: This hit song was released before Love Shy (Thinking About You). It is of the genre called Garage from the country that studio album Escape from the Sun was released in, due to its 4x4 rhythm.\n\nPassages:\n\n[Love Shy (Thinking About You)]\nIt was released after the success of \"What's It Gonna Be\" with H \"Two\" O.\n\n[Bassline (music genre)]\nBassline (sometimes referred to as bassline house, Niche or 4x4) is a type of music related to UK garage that originated in Sheffield in the early 2000s.\n\n[Escape from the Sun]\nIt was released in April 2009 through Marrakesh Records, available to buy in certain stores around the UK.\n\n[What's It Gonna Be (H &quot;Two&quot; O song)]\nis a bassline (subgenre of UK garage) song performed by the duo known as H \"Two\" O (Selim Ben Rabha, \"Solution\", and Simon McDevitt, \"Oz\", who also go by \"Hit 'Em\" and \"Hard\") and the British three-person bassline vocal group Platnum (Aaron Evers, Mina Poli, and Michelle McKenna).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00521",
  "kind": "yes/no",
  "text": "Claim: Amelie Simone Mauresmo has won more awards than the winner of the 2015 Family Circle Cup – Singles tournament.\n\nPassages:\n\n[2015 Family Circle Cup – Singles]\nAndrea Petkovic was the defending champion, but she lost to Angelique Kerber in the semifinals.\n\n[Amélie Mauresmo]\nAmélie Simone Mauresmo ] (born 5 July 1979) is a French former professional tennis player, and a former world No. 1. Mauresmo won two Grand Slam singles titles at the Australian Open and at Wimbledon, and also won a Silver Medal at the 2004 Summer Olympics.\n\n[Angelique Kerber]\nShe ascended to the top of the rankings on 12 September 2016, thus becoming the twenty-second and oldest player to achieve the number one ranking for the first time and the first new number one player since Victoria Azarenka in 2012.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
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
  "aid": "a00522",
  "kind": "yes/no",
  "text": "Claim: The Talbot-Taylor Wildlife Sanctuary is located in a town with a high school. This high school had Elias \"Coach\" Korcoulis as track coach.\n\nPassages:\n\n[Hollis/Brookline High School]\nHollis/Brookline High School is a public school located in Hollis, New Hampshire, serving the towns of Hollis and Brookline.\n\n[Elias &quot;Coach&quot; Korcoulis]\nElias Korcoulis, known to his friends as Lou and to thousands others as Coach (1940 – March 4, 2006) was the cross-country and track coach for Hollis/Brookline High School in Hollis, New Hampshire from 1962 until his death.\n\n[Brookline, New Hampshire]\nBrookline is a town in Hillsborough County, New Hampshire, United States. Brookline is home to the Talbot-Taylor Wildlife Sanctuary, Potanipo Pond, and the Brookline Covered Bridge.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00523",
  "kind": "yes/no",
  "text": "Claim: The permanent population of the largest city in Trego County is 1,862.\n\nPassages:\n\n[Trego County, Kansas]\nIts county seat and largest city is WaKeeney.\n\n[WaKeeney, Kansas]\nAs of the 2010 census, the city population was 1,862.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00524",
  "kind": "yes/no",
  "text": "Claim: Philip Savage served as Ozzie Newsome of Player Personnel for the Baltimore Ravens, under the general manager that Steve Little (American football) was drafted higher than, who was inducted into both the College and Pro Football Halls of Fame.\n\nPassages:\n\n[Steve Little (American football)]\nLittle was drafted higher than future NFL greats Ozzie Newsome and Todd Christensen.\n\n[Phil Savage]\nHe served as Director of Player Personnel for the Baltimore Ravens under General Manager Ozzie Newsome, a former Browns' player and member of the Pro Football Hall of Fame, from 2003 to 2004.\n\n[Ozzie Newsome]\nOzzie Newsome Jr. (born March 16, 1956) is a former American football tight end for the Cleveland Browns, and the current general manager of the Baltimore Ravens. Newsome as inducted into both the College Football Hall of Fame (1994) and the Pro Football Hall of Fame (1999).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00525",
  "kind": "yes/no",
  "text": "Claim: Architects Lise Roel and Hugo Hostrup were born on the warm Jutland peninsula.\n\nPassages:\n\n[Lise Roel and Hugo Höstrup]\nLise Roel (born 1928) and Hugo Höstrup, (1928–2004) were architects born in Randers, Denmark, with primary activity and production around 1960-1980 in western and southern Sweden.\n\n[Randers]\nRanders (] ) is a city in Randers Municipality, Central Denmark Region on the Jutland peninsula.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00526",
  "kind": "yes/no",
  "text": "Claim: The man who hired Sioux Falls architect Wallace L. Dow to build a home in Sioux Falls, Minnesota founded the company Dayton's department store.\n\nPassages:\n\n[George Dayton]\nGeorge Draper Dayton (March 6, 1857 – February 18, 1938) was an American businessman and philanthropist, most famous for being the founder of Dayton's department store, which later became Target Corporation.\n\n[George D. Dayton House]\nThe George Draper Dayton House was built in 1890 in Worthington, Minnesota, United States. George Dayton hired the Sioux Falls architect Wallace L. Dow to design his grand home on a parcel that took up eight lots.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00527",
  "kind": "yes/no",
  "text": "Claim: The genus that includes setulosa has more species than Epigaea.\n\nPassages:\n\n[Bactris setulosa]\nIt is one of the largest species of \"Bactris\" and is found at the highest elevations.\n\n[Bactris]\nBactris is a genus of spiny palms which is native to the Mexico, South and Central America and the Caribbean. Most species are small trees about 2 m tall, but some are large trees while others are shrubs with subterranean stems.\n\n[Epigaea]\nEpigaea is a genus comprising three species of flowering plants in the Ericaceae.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00528",
  "kind": "yes/no",
  "text": "Claim: The broadcast studio of the commercial channel that along with CNN and BBC disputes the murderer of Neda is at 1211 Avenue of the Americas, New York City, New York.\n\nPassages:\n\n[Death of Neda Agha-Soltan]\nThe murderer of Neda is disputed; according to CNN, BBC, and Fox News, she was shot by Basij, a paramilitary organization.\n\n[Fox News]\nFox News (officially known as the Fox News Channel, commonly abbreviated to FNC) is an American basic cable and satellite television news channel owned by the Fox Entertainment Group, a subsidiary of 21st Century Fox. The channel broadcasts primarily from studios at 1211 Avenue of the Americas, New York City, New York.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.88
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00529",
  "kind": "yes/no",
  "text": "Claim: The name of the painting stolen on March 19, 1990 for which a museum initially offered a $5 million reward for information leading towards its recovery is Landscape with Obelisk and is a painting by Dutch artist Govert Flinck.\n\nPassages:\n\n[Landscape with Obelisk]\nLandscape with Obelisk is painting by Dutch artist Govert Flinck, painted in 1638. The painting hung in the Isabella Stewart Gardner Museum of Boston, Massachusetts, United States, prior to being stolen in 1990.\n\n[Isabella Stewart Gardner Museum theft]\nIn the early hours of March 18, 1990, guards at the Isabella Stewart Gardner Museum in Boston admitted two men posing as police officers responding to a disturbance call. The museum initially offered a reward of $5 million for information leading to their recovery, but in 2017 this was doubled temporarily to $10 million with an expiration date set to the end of the year.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00530",
  "kind": "yes/no",
  "text": "Post: Went through all the trouble of growing this bone helmet over my meat computer just for it to start hurting itself from the inside",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
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
  "aid": "a00531",
  "kind": "yes/no",
  "text": "Claim: The black comedy sequel to \"Forgetting Sarah Marshall\" starred an Australian actress who started in the 2003 film \"The Rage in Placid Lake\" alongside Ben Lee.\n\nPassages:\n\n[Rose Byrne]\nMary Rose Byrne (born 24 July 1979) is an Australian actress. Byrne has also starred in the films \"Troy\", \"28 Weeks Later\", \"Knowing\", \"Insidious\", \"\", \"\", as well as the comedies \"Get Him to the Greek\", \"Bridesmaids\", \"Neighbors\", \"\", and \"Spy.\"\n\n[Get Him to the Greek]\nReleased on June 4, 2010, the film serves as a spin-off sequel of Stoller's 2008 film \"Forgetting Sarah Marshall\", reuniting director Stoller with stars Hill and Brand and producer Judd Apatow.\n\n[The Rage in Placid Lake]\nThe Rage in Placid Lake is a 2003 Australian film starring Ben Lee and Rose Byrne.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00532",
  "kind": "yes/no",
  "text": "Claim: Gary Owen performed at All-Star Comedy Jam Tour, an event named after a retired professional basketball player and old school rapper.\n\nPassages:\n\n[Shaquille O'Neal]\nShaquille Rashaun O'Neal ( ; born March 6, 1972), nicknamed \"Shaq\" ( ), is an American retired professional basketball player and rapper, currently serving as a sports analyst on the television program \"Inside the NBA\".\n\n[Gary Owen (comedian)]\nHe has cultivated an African-American following after headlining on cable channel BET and performing at targeted events, such as Shaquille O'Neal's All-Star Comedy Jam Tour.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00533",
  "kind": "yes/no",
  "text": "Claim: The critically acclaimed author of Bambi's Children: The Story of a Forest Family, originally titled his most famous work Bambi: Eine Lebensgeschichte aus dem Walde.\n\nPassages:\n\n[Bambi's Children]\nBambi's Children: The Story of a Forest Family (German: Bambis Kinder: Eine Familie im Walde ) is a novel written by Austrian author Felix Salten as a sequel to his successful work \"Bambi, A Life in the Woods\".\n\n[Bambi, a Life in the Woods]\nBambi, a Life in the Woods, originally published in Austria as Bambi: Eine Lebensgeschichte aus dem Walde is a 1923 Austrian novel written by Felix Salten and published by Ullstein Verlag.\n\n[Felix Salten]\nFelix Salten (6 September 1869 – 8 October 1945) was an Austrian author and critic in Vienna.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00534",
  "kind": "yes/no",
  "text": "Claim: Fragaria is not edible. Neither is the plant genus that was named in honor of a man. The man was the successor to Giovanni Targioni Tozzetti.\n\nPassages:\n\n[Fragaria]\nFragaria is a genus of flowering plants in the rose family, Rosaceae, commonly known as strawberries for their edible fruits.\n\n[Giovanni Targioni Tozzetti]\nHe was supervisor of the Orto Botanico di Firenze in Florence succeeded by Saverio Manetti.\n\n[Manettia]\nManettia is a genus of flowering plants in the family Rubiaceae.\n\n[Saverio Manetti]\nThe plant genus \"Manettia\" was named in his honour by Carolus Linnaeus.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00535",
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
  }
 },
 {
  "aid": "a00536",
  "kind": "yes/no",
  "text": "Text: @kittin_knittin According to a Trump republican,  that's relative to Penis size.  There's a video.  Lol",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
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
  "aid": "a00537",
  "kind": "yes/no",
  "text": "Claim: The star of The Big Year acted in a film with martial arts expert Tom Wu. He also voiced Lightning McQueen in the \"Cars\" franchise.\n\nPassages:\n\n[Shanghai Knights]\nDirected by David Dobkin and written by Alfred Gough and Miles Millar, it stars Jackie Chan and Owen Wilson.\n\n[The Big Year]\nThe Big Year is a 2011 American comedy film directed by David Frankel, written by Howard Franklin and starring Jack Black, Steve Martin, and Owen Wilson.\n\n[Tom Wu]\nHe is a martial arts expert who has appeared in films such as \"Revolver\", \"Shanghai Knights\", \"Batman Begins\" and the Bollywood sci-fi movie \"Ra.One\".\n\n[Owen Wilson]\nHe starred with Ben Stiller in numerous films, and is known for his roles in Frat Pack comedies and as well as voicing Lightning McQueen in the \"Cars\" franchise.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00538",
  "kind": "yes/no",
  "text": "Post: Shout out James Boswell  #unibowl",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
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
  "aid": "a00539",
  "kind": "yes/no",
  "text": "Tweet: Things I learned on my first day of classes my sophomore year in college: ingesting semen does NOT lower depression in women",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00540",
  "kind": "yes/no",
  "text": "Claim: Paige Lewis featured in the soundtrack of the film this person directed. He has more productions under their belt than Elmer Clifton.\n\nPassages:\n\n[Elmer Clifton]\nA collaborator of D.W. Griffith, he appeared in \"The Birth of a Nation\" (1915) and \"Intolerance\" (1916) before giving up acting in 1917 to concentrate on work behind the camera, with Griffith and Joseph Henabery as his mentors.\n\n[Matchstick Men]\nMatchstick Men is a 2003 British-American black comedy crime film directed by Ridley Scott, and based on Eric Garcia's 2002 novel of the same name.\n\n[Paige Lewis]\nPaige Lewis is a singer-songwriter and copywriter from Katy, Texas whose work has been featured in the soundtrack of the film Matchstick Men.\n\n[Ridley Scott]\nSir Ridley Scott (born 30 November 1937) is an English film director and producer. Following his commercial breakthrough with the science-fiction horror film \"Alien\" (1979), his best known works include the neo-noir dystopian science fiction film \"Blade Runner\" (1982), historical drama and Best Picture Oscar winner \"Gladiator\" (2000), and science fiction film \"The Martian\" (2015).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00541",
  "kind": "yes/no",
  "text": "Tweet: victoria has a crush on maluma",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
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
  "aid": "a00542",
  "kind": "yes/no",
  "text": "Text: @32watto Neighbours",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00543",
  "kind": "yes/no",
  "text": "Claim: The author of the book \"A New Kind of Science\" designed a computer algebra system at Caltech in California.\n\nPassages:\n\n[Symbolic Manipulation Program]\nSymbolic Manipulation Program, usually called SMP, was a computer algebra system designed by Chris A. Cole and Stephen Wolfram at Caltech circa 1979 and initially developed in the Caltech physics department under Wolfram's leadership with contributions from Geoffrey C. Fox, Jeffrey M. Greif, Eric D. Mjolsness, Larry J. Romans, Timothy Shaw, and Anthony E. Terrano.\n\n[Stephen Wolfram]\nHe is the author of the book \"A New Kind of Science.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00544",
  "kind": "yes/no",
  "text": "Claim: Ranjhay Hath Gandasa is a comedy film starring Pakistani-American singer-songwriter Nadia Ali.\n\nPassages:\n\n[Ranjhay Hath Gandasa]\nIt stars Nadia Ali, Rana Rehman, Fozia Rana, Durdana Rehman, Azhar Rangeela and Shafqat Cheema in lead roles.\n\n[Nadia Ali (singer)]\nNadia Ali (Urdu: ‎ , born 3 August 1980) is a Pakistani American singer-songwriter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00545",
  "kind": "yes/no",
  "text": "Claim: The actress that appeared Faster (2010 film) is known for her role as Kelor in a shared universe centered on a series of superhero films. This films were distributed by Cinemax\n\nPassages:\n\n[DC Extended Universe]\nThe Justice League Universe (JLUDCEUUJLDCE), more commonly known by its unofficial name as the DC Extended Universe (DCEU), is an American media franchise and shared universe, centered on a series of superhero films distributed by Warner Bros.\n\n[Carla Gugino]\nCarla Gugino ( ; ] ; born August 29, 1971) is an American actress. Her feature film work includes starring roles in \"Son in Law\" (1993), \" Sin City\" (2005), \"Night at the Museum\" (2006), \"Mr. Popper's Penguins\" (2011), \"San Andreas\" (2015), \"The Space Between Us\" (2017), and \"Gerald's Game\" (2017) as well as Kelor in the DC Extended Universe.\n\n[Faster (2010 film)]\nTom Berenger, Oliver Jackson-Cohen, Adewale Akinnuoye-Agbaje and Carla Gugino also appear.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.97
  }
 },
 {
  "aid": "a00546",
  "kind": "yes/no",
  "text": "Claim: The musician from another band who released a famous album joined the group Zwan shortly after its breakup. FOL (song) appeared on on this album.\n\nPassages:\n\n[Zeitgeist (The Smashing Pumpkins album)]\nZeitgeist is the seventh album by American alternative rock band The Smashing Pumpkins, released on July 10, 2007 in the United States and Canada. The album was produced by Roy Thomas Baker, Billy Corgan, Jimmy Chamberlin, and Terry Date.\n\n[Jimmy Chamberlin]\nHe is best known as the drummer for the alternative rock band The Smashing Pumpkins. Following the 2000 breakup of the band, Chamberlin joined Pumpkins frontman Billy Corgan in the supergroup Zwan and also formed his own group, the Jimmy Chamberlin Complex.\n\n[FOL (song)]\n\"FOL\" is a song by The Smashing Pumpkins, written and recorded during the sessions for their 2007 album \"Zeitgeist\" and used for a Hyundai commercial during Super Bowl XLIII.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00547",
  "kind": "yes/no",
  "text": "Claim: The causeway that connects Fiesta Key to the mainland is 113 mi long.\n\nPassages:\n\n[Overseas Highway]\nThe Overseas Highway is a 113 mi highway carrying U.S. Route 1 (US 1) through the Florida Keys.\n\n[Fiesta Key]\nFiesta Key is an island in the Florida Keys, connected via causeway to U.S. 1 (or the Overseas Highway) at mile marker 70, between Long Key and Craig Key.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00548",
  "kind": "yes/no",
  "text": "Claim: The driver Marlon Stöckinger has been in less races than MatthieuVaxivière.\n\nPassages:\n\n[Marlon Stöckinger]\nMarlon Alexander Stöckinger (born 4 April 1991 in Manila) is a Filipino racing driver, who raced for Status Grand Prix in the 2012 GP3 Series and currently driving for Lotus F1 Team Juniors in the 2013 World Series by Renault.\n\n[Matthieu Vaxivière]\nHe was the 2011 French F4 champion. In 2012 he raced in the V de V Endurance Cup, French GT, and 2e Grand Prix Èlectrique. In addition, he was 14th in the 2012 Formula Renault 2.0 Alps season and 29th in the Formula Renault 2.0 Eurocup, driving for Tech 1 Racing. In 2013 he finished 10th in the Formula Renault 2.0 Eurocup and 18th in the Formula Renault 2.0 Alps. In 2014 he was assigned as one of the drivers for the Lotus F1 Junior team, while competing in the Formula Renault 3.5 series alongside Filipino-Swiss driver Marlon Stöckinger.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00549",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I wish we could have signed a player for the first team.",
   "I suppose though, we did sign one for the future so, you know, not all gloom and doom...we might be good in 6 years time."
  ],
  "human_label": "I suppose though, we did sign one for the future so, you know, not all gloom and doom...we might be good in 6 years time.",
  "read_1": {
   "answer": "I suppose though, we did sign one for the future so, you know, not all gloom and doom...we might be good in 6 years time.",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "I suppose though, we did sign one for the future so, you know, not all gloom and doom...we might be good in 6 years time.",
   "confidence": 0.45
  }
 }
]
