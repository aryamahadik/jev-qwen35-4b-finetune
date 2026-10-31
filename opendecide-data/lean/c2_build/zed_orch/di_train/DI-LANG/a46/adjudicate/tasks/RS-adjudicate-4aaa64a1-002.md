# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-002.json

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
  "aid": "a00100",
  "kind": "yes/no",
  "text": "Claim: The series that recounts the adventures of Anne Shirley was published by Scholastic Press in 1908.\n\nPassages:\n\n[Anne of Green Gables]\nAnne of Green Gables is a 1908 novel by Canadian author Lucy Maud Montgomery (published as L. M. Montgomery).\n\n[Twitches (novel series)]\nThe books were published by Scholastic Press, a subsidiary of the Scholastic Corporation, who also published the British Harry Potter series by J.K. Rowling and the Canadian Anne of Green Gables series by Lucy Maud Montgomery.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00101",
  "kind": "yes/no",
  "text": "Claim: ER White is the current lead guitarist for the band that released the album This Is Your Way Out.\n\nPassages:\n\n[Emarosa]\nThe band currently consists of founding members ER White (lead guitar) and Jordan Stewart (keyboards), as well as lead vocalist Bradley Walden and rhythm guitarist Marcellus Wallace.\n\n[This Is Your Way Out]\nThis Is Your Way Out is the first EP record by Emarosa, released May 1, 2007.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00102",
  "kind": "yes/no",
  "text": "Claim: A song by David Guetta was produced by the Dutch David Guetta. The signer who recorded I Don't Wanna Grow Up guested on this song.\n\nPassages:\n\n[I Don't Wanna Grow Up]\nI Don't Wanna Grow Up is the debut extended play (EP) by American pop recording artist Bebe Rexha.\n\n[Bebe Rexha]\nShe is best known as a featured guest vocalist on several \"Billboard\" Hot 100 charting songs, such as G-Eazy's \"Me, Myself & I\", David Guetta's \"Hey Mama\", Martin Garrix's \"In the Name of Love\" and Cash Cash's \"Take Me Home\".\n\n[Hey Mama (David Guetta song)]\n\"Hey Mama\" is a song by French DJ and record producer David Guetta, featuring vocals from Nicki Minaj and Bebe Rexha, as well as production from Dutch DJ and producer Afrojack.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00103",
  "kind": "yes/no",
  "text": "Text: the one time I need my phone charger and I. have brought the charging battery bank but forgoTTEN THE CORD I am dumb",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
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
  "aid": "a00104",
  "kind": "yes/no",
  "text": "Claim: Computech the single was recorded in 1989 at the first Tubronegro rehearsal by the Norwegian punk rock band, initially active from 1989 to 1998, whose style is \"deathpunk\".\n\nPassages:\n\n[Turbonegro]\nTurbonegro (Turboneger in Norway) is a Norwegian punk rock band, initially active from 1989 to 1998, then reformed in 2002.\n\n[Computech]\n\"Computech\" is a single from the Norwegian band Turbonegro released on cassette tape in 1989. It was recorded at the first Turbonegro rehearsal in January 1989 and only 50 copies (some say 100) were made.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00105",
  "kind": "yes/no",
  "text": "Claim: Mel Brooks is an American actor and writer. He produced the 1983 comedy movie Charles Durning is best known for appearing in.\n\nPassages:\n\n[Charles Durning]\nDurning's best-known roles included \"The Sting\" (1973) and \"Dog Day Afternoon\" (1975), along with the comedies \"The Best Little Whorehouse in Texas\" (1982), \"Tootsie\" (1982), and \"To Be or Not to Be\" (1983).\n\n[To Be or Not to Be (1983 film)]\nTo Be or Not to Be is a 1983 American war comedy film directed by Alan Johnson and produced by Mel Brooks.\n\n[Mel Brooks]\nMel Brooks (born Melvin Kaminsky; June 28, 1926) is an American actor, writer, producer, director, comedian, and composer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00106",
  "kind": "yes/no",
  "text": "Claim: The defending champion of the 2010 ASB Classic – Doubles is the former professional tennis player from Italy. Not the player from Russia that won the singles title in the 1974 John Player Tournament.\n\nPassages:\n\n[Mara Santangelo]\nMara Santangelo (born 28 June 1981) is a former professional tennis player from Italy.\n\n[2010 ASB Classic – Doubles]\nNathalie Dechy and Mara Santangelo were the defending champions, but Dechy retired from tennis before being able to defend the title, and Santangelo chose not to participate this year.\n\n[1974 John Player Tournament]\nFirst-seeded Chris Evert won the singles title and earned £1,750 ($4,200) first-prize money.\n\n[Chris Evert]\nChristine Marie Evert (born December 21, 1954), known as Chris Evert Lloyd from 1979 to 1987, is a former World No. 1 professional tennis player from the United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00107",
  "kind": "yes/no",
  "text": "Claim: The broadcaster for the 1980-1990 St Louis Cardinals team is the father of the broadcaster of The 2010 Major League Baseball All-Star Game.\n\nPassages:\n\n[2010 Major League Baseball All-Star Game]\nThe game was held on July 13, 2010, at Angel Stadium of Anaheim, the home of the American League Los Angeles Angels of Anaheim, and was telecast by Fox Sports in the USA, with Joe Buck and Tim McCarver in the broadcast booth.\n\n[Bob Buck]\nHe was the younger brother of late St. Louis Cardinals radio broadcaster Jack Buck, and was the uncle of national television sportscaster Joe Buck.\n\n[Joe Buck]\nJoseph Francis \"Joe\" Buck (born April 25, 1969) is an American sportscaster and the son of sportscaster Jack Buck.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00108",
  "kind": "yes/no",
  "text": "Claim: Charlie Murphy, brother of Eddie Murphy, starred in Twisted Fortune directed by Victor Varnada.\n\nPassages:\n\n[Charlie Murphy]\nHe was the older brother of comedian Eddie Murphy.\n\n[Twisted Fortune]\nTwisted Fortune is a black comedy about a bumbling small-time crook (played by Charlie Murphy) who finds a bottle cap worth $1,000,000 while robbing a convenience store. It was directed by comedian Victor Varnado (\"End of Days\"), who also acted in the movie.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00109",
  "kind": "yes/no",
  "text": "Claim: The thirteenth season of Gilmore Girls featured an actress as a maid of honor who had also played the role of Winnie Foster.\n\nPassages:\n\n[Alexis Bledel]\nKimberly Alexis Bledel ( ; ] ; born September 16, 1981) is an American actress and model. Bledel made her feature film debut as Winnie Foster in \"Tuck Everlasting\" (2002), and has since appeared in \"Sin City\" (2005), \"Post Grad\" (2009), and as Lena Kaligaris in \"The Sisterhood of the Traveling Pants\" film series.\n\n[Wedding Bell Blues (Gilmore Girls)]\n\"Wedding Bell Blues\" is the thirteenth episode of the fifth season of the American comedy-drama series \"Gilmore Girls\" and the show's 100th episode overall. Their daughter Lorelai Gilmore (Lauren Graham) and their granddaughter Rory Gilmore (Alexis Bledel) serve as maid of honor and best man, respectively.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00110",
  "kind": "yes/no",
  "text": "Claim: The group that promoted a set of rules was founded during a meeting of an organisation. That organization was founded in 1936. Inez McCormack was a signatory on this set of rules.\n\nPassages:\n\n[MacBride Principles]\nThey were promoted by Seán McManus and the Irish National Caucus, and by John Finucanne and the American Irish Political Education Committee (PEC), and were drafted by Nobel Laureate Seán MacBride (a founding member of Amnesty International), and were launched in November 1984.\n\n[Irish National Caucus]\nIt was founded by Father Sean Gabriel Mc Manus on February 6, 1974, at a meeting of the Ancient Order of Hibernians.\n\n[Ancient Order of Hibernians]\nIts largest membership is now in the United States, where it was founded in New York City in 1836.\n\n[Inez McCormack]\nShe also successfully campaigned for the inclusion of strong equality and human rights provisions in the Good Friday Agreement, and was a signatory to the MacBride Principles for fair employment.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00111",
  "kind": "yes/no",
  "text": "Claim: The Yule goat, which has become more or less conflated with Santa Claus, is a Finnish Christmas figure that has modern representations typically made of straw.\n\nPassages:\n\n[Joulupukki]\nJoulupukki is a Finnish Christmas figure. An old Scandinavian custom, the figure eventually became more or less conflated with Santa Claus.\n\n[Yule Goat]\nThe Yule goat is a Scandinavian and Northern European Yule and Christmas symbol and tradition. Modern representations of the Yule goat are typically made of straw.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00112",
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
  }
 },
 {
  "aid": "a00113",
  "kind": "yes/no",
  "text": "Text: how do I get my boyfriend in a maid costume?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00114",
  "kind": "yes/no",
  "text": "Claim: Dražen Dalipagić was enshrined for public viewing into a museum in Springfield, Massachusetts in 2004.\n\nPassages:\n\n[Dražen Dalipagić]\nDalipagić was enshrined into the Naismith Memorial Basketball Hall of Fame as a player in 2004 and into the FIBA Hall of Fame in 2007.\n\n[Naismith Memorial Basketball Hall of Fame]\nThe Naismith Memorial Basketball Hall of Fame is an American history museum and hall of fame, located at 1000 Hall of Fame Avenue in Springfield, Massachusetts.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00115",
  "kind": "yes/no",
  "text": "Claim: A Indo-European linguist, was a member of the Kazan School. This Indo-European linguist was published by Michigan Slavic Publications. This publisher was founded by Ladislav Matejka.\n\nPassages:\n\n[Kazan school]\nKazan School was an influential group of linguists in Kazan. The linguistic circle included the Polish linguist Jan Baudouin de Courtenay and his student Nikolai Trubetzkoy.\n\n[Nikolai Trubetzkoy]\nPrince Nikolai Sergeyevich Trubetzkoy (also Troubetskoy; Russian: Никола́й Серге́евич Трубецко́й; Moscow, April 16, 1890 – Vienna, June 25, 1938) was a Russian linguist and historian whose teachings formed a nucleus of the Prague School of structural linguistics.\n\n[Ladislav Matejka]\nIn 1962, he founded Michigan Slavic Publications, a series that has published more than 100 volumes by authors such as Roman Jakobson and Nikolai Trubetzkoy.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00116",
  "kind": "yes/no",
  "text": "Claim: The execution of Roger David Casement, the Irish Nationalist who made made efforts during World War I to gain German military aid for the 1916 Easter Rising that sought to gain Irish independence, took place in Casement's Fort.\n\nPassages:\n\n[Rahoneen]\nIt is notable as the location of an ancient Celtic ringfort; at one time this was known as McKenna's fort, but, after the capture and execution of Roger Casement for treason, sabotage and espionage against the Crown, it became known as Casement's Fort. \"Too weak to travel, he was discovered at McKenna's Fort where he had hidden after arranging delivery of German weapons as part of a plan of arming Irish rebels and creating a rising in 1916 against the British to achieve independence.\n\n[Roger Casement]\nDescribed as the \"father of twentieth-century human rights investigations\", he was honoured in 1905 for the Casement Report on the Congo and knighted in 1911 for his important investigations of human rights abuses in Peru.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00117",
  "kind": "yes/no",
  "text": "Claim: Space Ghost's arch enemy is a catlike alien space pirate. He's the only character Andy Ronald Merrill voiced in \"Space Ghost Coast to Coast\".\n\nPassages:\n\n[Andy Merrill]\nAndy Ronald Merrill (born November 27, 1966 in Newark, Ohio) is an American television writer, producer and voice actor best known for his comedy voice portrayal of the character Brak on \"Space Ghost Coast to Coast\" and \"Cartoon Planet\", and other related productions from Cartoon Network utilizing characters from the \"Space Ghost\" series.\n\n[Space Ghost's Musical Bar-B-Que]\nFeaturing songs and skits by Space Ghost and his arch enemies Zorak and Brak.\n\n[Brak (character)]\nBrak is a fictional character and supervillain on the 1966 Hanna-Barbera animated series \"Space Ghost\", portrayed as a catlike alien space pirate trying to conquer the galaxy.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00118",
  "kind": "yes/no",
  "text": "Post: Honestly this weather is the best birthday present I could ever receive",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00119",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Anyone else wanna ruin me day x",
   "Can people stop ruining my day please"
  ],
  "human_label": "Anyone else wanna ruin me day x",
  "read_1": {
   "answer": "Anyone else wanna ruin me day x",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "Anyone else wanna ruin me day x",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00120",
  "kind": "yes/no",
  "text": "Claim: An assistant coach for Orlando Magic, Under doc rivers and the head coach of the 1997–98 Orlando Magic season led United States men's Olympic basketball team to the gold medal at the 1992 Summer Olympics. Yanni Hufnagel served under this coach.\n\nPassages:\n\n[Chuck Daly]\nCharles Jerome Daly (July 20, 1930 – May 9, 2009) was an American basketball head coach. He led the Detroit Pistons to consecutive National Basketball Association (NBA) Championships in 1989 and 1990, and the 1992 United States men's Olympic basketball team (\"The Dream Team\") to the gold medal at the 1992 Summer Olympics.\n\n[Eric Musselman]\nThe son of former NBA head coach Bill Musselman, Eric Musselman was a head coach in the Continental Basketball Association (CBA) before becoming an assistant coach with the Minnesota Timberwolves, Orlando Magic (under Chuck Daly and Doc Rivers), and Atlanta Hawks (under Lon Kruger).\n\n[Yanni Hufnagel]\nHe last served as an assistant coach of the Nevada Wolf Pack men's basketball team under Eric Musselman.\n\n[1997–98 Orlando Magic season]\nThe Magic hired Chuck Daly as head coach, who won two championships coaching the Detroit Pistons.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00121",
  "kind": "yes/no",
  "text": "Claim: 28000 km2 is the approximate area of the country where the flower species Lobelia columnaris can be found (other than Cameroon).\n\nPassages:\n\n[Lobelia columnaris]\nIt is the only giant Lobelia occurring in West Africa and is found in Cameroon and Equatorial Guinea.\n\n[Equatorial Guinea]\nEquatorial Guinea (Spanish: \"Guinea Ecuatorial\" , French: \"Guinée équatoriale\" , Portuguese: \"Guiné Equatorial\" ), officially the Republic of Equatorial Guinea (Spanish: \"República de Guinea Ecuatorial\" , French: \"République de Guinée équatoriale\" , Portuguese: \"República da Guiné Equatorial\" ), is a country located in Central Africa, with an area of 28000 km2 .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00122",
  "kind": "yes/no",
  "text": "Claim: This actor appeared in the film Revolver, along with Jason Statham and Ray Liotta. He also appeared in the 2011 Indian film produced by Karim Morani.\n\nPassages:\n\n[Revolver (2005 film)]\nRevolver is a 2005 British-French crime thriller film co-written and directed by Guy Ritchie and starring Jason Statham, Ray Liotta, Vincent Pastore and André Benjamin.\n\n[Karim Morani]\nKarim Morani is an Indian film producer who has produced films like Chennai Express and Ra.One starring Shahrukh Khan.\n\n[Ra.One]\nRa.One is a 2011 Indian superhero film directed by Anubhav Sinha, and starring Shah Rukh Khan, Arjun Rampal, Kareena Kapoor, Armaan Verma, Shahana Goswami and Tom Wu in pivotal roles.The script, written by Anubhav Sinha and Kanika Dhillon, originated as an idea that Anubhav Sinha got when he saw a television commercial, and which he subsequently expanded.\n\n[Tom Wu]\nHe was born in Hong Kong and grew up in Chinatown, London.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00123",
  "kind": "yes/no",
  "text": "Claim: Willard Huyck directed a 1986 American science-fiction comedy starring Tommy Swerdlow.\n\nPassages:\n\n[Tommy Swerdlow]\nTommy Swerdlow is an American actor and screenwriter. He has appeared in such films as \"Howard the Duck\" (1986) and \"Spaceballs\" (1987) and co-wrote the screenplays of \"Cool Runnings\" (1993), \"Little Giants\" (1994) and \"Snow Dogs\" (2002).\n\n[Howard the Duck (film)]\nHoward the Duck (titled Howard: A New Breed of Hero in the UK) is a 1986 American science-fiction comedy film directed by Willard Huyck and starring Chip Zien, Lea Thompson, Jeffrey Jones, and Tim Robbins.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00124",
  "kind": "yes/no",
  "text": "Claim: Director James Searle Dawley was from a country closer to Canada, than the filmmaker whose first movie was Jemima & Johnny.\n\nPassages:\n\n[Jemima &amp; Johnny]\nIt is the first film by South African filmmaker Lionel Ngakane, and won a plate at the 1966 Venice Film Festival.\n\n[Lionel Ngakane]\nLionel Ngakane (17 July 1928 – 26 November 2003) was a South African filmmaker and actor.\n\n[J. Searle Dawley]\nJames Searle Dawley (May 13, 1877 – March 30, 1949) was an American director and screenwriter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00125",
  "kind": "yes/no",
  "text": "Claim: This person directed a 1955 French drama film, Black Dossier (film). This director and the director who is the father of Chris Donaldson are not both French filmmakers.\n\nPassages:\n\n[Chris Donaldson]\nHe is the son of film director Roger Donaldson.\n\n[André Cayatte]\nAndré Cayatte (3 February 1909, Carcassonne – 6 February 1989, Paris) was a French filmmaker and lawyer, who became known for his films centering on themes of crime, justice, and moral responsibility.\n\n[Black Dossier (film)]\nBlack Dossier (French: \"Le Dossier noir\" ) is a 1955 French drama film directed by André Cayatte.\n\n[Roger Donaldson]\nRoger Donaldson (born 15 November 1945) is an Australian-born New Zealand film director, producer and writer whose films include \"The World's Fastest Indian\" (2005), acclaimed 1981 relationship drama \"Smash Palace\", and a run of titles shot in the United States, including the Kevin Costner films \"No Way Out\" (1987) and \"Thirteen Days\" (2000), and the 1997 disaster film \"Dante's Peak\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
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
  "aid": "a00126",
  "kind": "yes/no",
  "text": "Claim: The band Vertex's singer was a leading part of the heavy metal band Ratt. The recording artist who recorded the song \"What's Missing\" was not.\n\nPassages:\n\n[Vertex (band)]\nVertex was a band formed in 1995 featuring singer Stephen Pearcy (Ratt, Arcade, Vicious Delite, Nitronic), guitarist Al Pitrelli (Danger Danger, Hotshot, Alice Cooper, Asia, Savatage, Megadeth, Trans-Siberian Orchestra), and drummer Hiro Kuretani (WXXI, Trancentral Station).\n\n[Alexander O'Neal]\nAlexander O'Neal (born November 15, 1953) is an American R&B singer, songwriter and arranger from Natchez, Mississippi.\n\n[What's Missing]\n\" What's Missing \" is a song written by Jimmy Jam and Terry Lewis and recorded by American recording artist Alexander O'Neal.\n\n[Stephen Pearcy]\nStephen Eric Pearcy (born July 3, 1956), known as Stephen Pearcy, is an American musician. He is best known as the founder, singer, and songwriter of the heavy metal band Ratt.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00127",
  "kind": "yes/no",
  "text": "Claim: Richard Fleischer directed the film that chronicled Reverend Stephen Kaplan's attempt to prove that the Amityville Horror hauntings were a hoax.\n\nPassages:\n\n[Amityville 3-D]\nThe film was directed by Richard Fleischer and the script was written by David Ambrose (under the pseudonym William Wales).\n\n[Stephen Kaplan]\nHis overview of the Amityville Horror became the basis for the film Amityville 3-D that chronicles his attempt to prove the story was a hoax.",
  "question": "Do the passages fully support the claim?",
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
  "aid": "a00128",
  "kind": "yes/no",
  "text": "Claim: An Mandarin rock band released My Animal. This band has more studio albums than The Invisible.\n\nPassages:\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.\n\n[Boy Hits Car]\nBoy Hits Car released their 5th studio album \"All That Led Us Here\" in May 2014 and are following it up with a European tour.\n\n[The Invisible (band)]\nTheir self-titled debut album, released on 9 March 2009, was nominated for the Mercury Prize and selected as critics choice for iTunes album of the year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
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
  "aid": "a00129",
  "kind": "yes/no",
  "text": "Claim: The actor son of Jeremiah Porter was born in 1997.\n\nPassages:\n\n[Jeremiah Porter]\nPorter was born in manhattan. In 2015 Porter was adopted by Glenn Cook, the father of Ben Cook (actor) and attended the Metropolitan School of the Arts.\n\n[Ben Cook (actor)]\nBenjamin Tyler Cook (born December 11, 1997) is an American actor, dancer and singer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00130",
  "kind": "yes/no",
  "text": "Claim: Seven years before the construction of the Brewer Fieldhouse in Columbia, Missouri, Chester Brewer worked as head football coach and head basketball coach of University Farm.\n\nPassages:\n\n[Brewer Fieldhouse]\nThe Brewer Fieldhouse was a multi-purpose arena located in Columbia, Missouri, and home to the University of Missouri Tigers basketball team prior to the Hearnes Center opening in 1972. Named after Chester Brewer, the building opened in 1929 to expand on the existing 500 seat Rothwell Gymnasium.\n\n[Chester Brewer]\nHe served as the head football coach at Albion College (1899–1902), Michigan Agricultural College, now Michigan State University, (1903–1910, 1917, 1919), the University of Missouri (1911–1913), and the University Farm, now the University of California, Davis, (1922), compiling a career record of 97–51–4. Brewer was also the head basketball coach at Michigan Agricultural (1903–1910), Missouri (1910–1911) and the University Farm (1922–1923), tallying a mark of 84–36, and the head baseball coach at Michigan Agricultural (1904–1910, 1918–1920) and Missouri (1911, 1914–1917, 1933–1934), amassing a record of 148–93–4.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00131",
  "kind": "yes/no",
  "text": "Claim: John Updike and Tom Clancy both publish more than 15 bestselling novels.\n\nPassages:\n\n[Tom Clancy]\nSeventeen of his novels were bestsellers, and more than 100 million copies of his books are in print.\n\n[John Updike]\nOne of only three writers to win the Pulitzer Prize for Fiction more than once (the others were Booth Tarkington and William Faulkner), Updike published more than twenty novels, more than a dozen short-story collections, as well as poetry, art and literary criticism and children's books during his career.",
  "question": "Do the passages fully support the claim?",
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
  "aid": "a00132",
  "kind": "yes/no",
  "text": "Claim: The Labrador Retriever, not the Tibetan Terrier, is a type of gun dog.\n\nPassages:\n\n[Tibetan Terrier]\nSome old travelers' accounts refer to the dog as Dokhi Apso or \"outdoor\" Apso, indicating a shaggy or bearded working dog which lives outdoors.\n\n[Labrador Retriever]\nThe Labrador Retriever, also Labrador, is a type of retriever-gun dog.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00133",
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
  }
 },
 {
  "aid": "a00134",
  "kind": "yes/no",
  "text": "Post: Everybody always talks about Devon Bostick’s portrayal of Rodrick in the Diary of a Wimpy Kid movies but nobody ever talks about how Devon Bostick played two separate characters in the Saw franchise",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
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
  "aid": "a00135",
  "kind": "yes/no",
  "text": "Claim: The city of the college that Nancy R. Howell is a Professor in and United Methodist Church of the Resurrection have in common is Kansas.\n\nPassages:\n\n[United Methodist Church of the Resurrection]\nThe original campus is located in Leawood, Kansas, with additional locations in Olathe, Kansas, downtown Kansas City, Missouri & Blue Springs, Missouri.\n\n[Saint Paul School of Theology]\nSaint Paul School of Theology is a United Methodist Seminary in Overland Park, Kansas in the Kansas City metropolitan area and is one of 13 seminaries of the United Methodist Church.\n\n[Nancy R. Howell]\nShe is Professor of Theology and Philosophy of Religion at Saint Paul School of Theology in Kansas City, Missouri.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00136",
  "kind": "yes/no",
  "text": "Post: If you watch #TheCrown and don’t  simultaneously wiki deep-dive on the royal family, did you even watch The Crown?",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
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
  "aid": "a00137",
  "kind": "yes/no",
  "text": "Claim: A star of \"Hotline\", a 2014 film, and Millard Webb are both authors.\n\nPassages:\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Hotline (2014 film)]\nThe film stars Miss Cleo, Jeff Ragsdale, Jamie Blaine, and Tonya Jone Miller.\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00138",
  "kind": "yes/no",
  "text": "Claim: The company that its interactive Internet and mobile division is called Dennis Digital has published a magazine that Bob Basset has appeared in. Also, a sister publication devoted to the anomalous phenomena popularised by Charles Fort in 1999.\n\nPassages:\n\n[Dennis Digital]\nDennis Digital is the interactive Internet and mobile division of Dennis Publishing, which publishes Maxim, Stuff, The Week and did publish (now defunct) Blender.\n\n[Bizarre (magazine)]\nBizarre was a British alternative magazine published from 1997 to 2015. It was published by Dennis Publishing, and was a sister publication to the \"Fortean Times\".\n\n[Bob Basset]\nPublications about Bob Basset appeared in , WAD magazine, VICE UK, Bizarre Magazine, INSIDE artzine magazine.\n\n[Fortean Times]\nFortean Times is a British monthly magazine devoted to the anomalous phenomena popularised by Charles Fort. Previously published by John Brown Publishing (from 1991 to 2001) and then I Feel Good Publishing (2001 to 2005), it is now published by Dennis Publishing Ltd.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00139",
  "kind": "yes/no",
  "text": "Text: Just finished Different for Girls / Just for One Day by @ReaLouisewener (not sure which title she prefers) &amp; loved it. Bittersweet &amp; funny.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
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
  "aid": "a00140",
  "kind": "yes/no",
  "text": "Claim: Section.80 is an album. It succeeded Kendrick Lamar's album that had the song produced by the same producer as Research (Big Sean song) on it.\n\nPassages:\n\n[Research (Big Sean song)]\nIt was written by Sean, Grande, Dacoury Natchel, Michael Carlson, and Leland Wayne, and was produced by DJ Dahi and Metro Boomin.\n\n[DJ Dahi]\nDahi is perhaps best known for producing \"Worst Behavior\" by Canadian rapper Drake, as well as American rapper Kendrick Lamar's critically acclaimed album cut \"Money Trees\", which features Lamar's label-mate Jay Rock.\n\n[Good Kid, M.A.A.D City]\nGood Kid, M.A.A.D City (stylized as good kid, m.A.A.d city) is the second studio album by American rapper Kendrick Lamar. It was preceded by the release of Kendrick's debut studio album \"Section.80\" (2011), released exclusively through the iTunes Store as an independent album.\n\n[Money Trees]\n\"Money Trees\" is a song by American hip hop recording artist Kendrick Lamar, taken from his major label debut studio album \"Good Kid, M.A.A.D City\" (2012).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
  "aid": "a00141",
  "kind": "yes/no",
  "text": "Claim: The Hills Tavern, renamed the Century Inn, was built between 1811 and 1837.\n\nPassages:\n\n[National Road]\nBuilt between 1811 and 1837, the 620 mi road connected the Potomac and Ohio Rivers and was a main transport path to the West for thousands of settlers.\n\n[Hill's Tavern]\nFor a period in the early 1900s, the inn was known as Central Hotel. Now called the Century Inn, it had been the oldest tavern in continuous use on the National Road, until the fire brought an end to its 221 years of continuous operation.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00142",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Old people don’t deserve rights",
   "old people suck"
  ],
  "human_label": "Old people don’t deserve rights",
  "read_1": {
   "answer": "Old people don’t deserve rights",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "Old people don’t deserve rights",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00143",
  "kind": "yes/no",
  "text": "Claim: Creolized forms of Kongo are found in traditional African religions of Africa with some influence from Christianity.\n\nPassages:\n\n[Afro-American religion]\nAfro-American religions (also known as African diasporic religions or New World traditions) are a number of related religions that developed in the Americas in various nations of Latin America, the Caribbean, and the southern United States. They derive from traditional African religions of Africa with some influence from Christianity.\n\n[Kongo language]\nFor this reason, while Kongo still is spoken in the above-mentioned countries, creolized forms of the language are found in ritual speech of Afro-American religions, especially in Brazil, Cuba, and Haiti.",
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
  "aid": "a00144",
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
  }
 },
 {
  "aid": "a00145",
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
  }
 },
 {
  "aid": "a00146",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "After many years it is brilliant to laugh at germany",
   "Schadenfreude x"
  ],
  "human_label": "Schadenfreude x",
  "read_1": {
   "answer": "After many years it is brilliant to laugh at germany",
   "confidence": 0.4
  },
  "read_2": {
   "answer": "After many years it is brilliant to laugh at germany",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00147",
  "kind": "yes/no",
  "text": "Claim: Phoebe Ruguru created a 2014 film on a smartphone marketed by Apple.\n\nPassages:\n\n[IPhone 4S]\nThe iPhone 4S (retroactively stylized with a lowercase 's' as iPhone 4s as of September 2013) is a smartphone that was designed and marketed by Apple Inc. It is the fifth generation of the iPhone, succeeding the iPhone 4 and preceding the iPhone 5.\n\n[Phoebe Ruguru]\nHer winning film \"Saidia\" (Swahili for \"help\") was shot entirety on her iPhone 4s alongside her producer friends Njue Kevin and Bill Jones Afwani.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00148",
  "kind": "yes/no",
  "text": "Text: JUSTICE HAS BEEN DONE.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00149",
  "kind": "yes/no",
  "text": "Claim: The 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada held from 30 June to 22 July 2007, Argentine player Sergio Aguero was given the FIFA U-20 Golden Shoe.\n\nPassages:\n\n[2007 FIFA U-20 World Cup]\nThe 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada from 30 June to 22 July 2007.\n\n[Sergio Agüero]\nSergio Leonel \"Kun\" Agüero (] ; born 2 June 1988) is an Argentine professional footballer who plays as a striker for Premier League club Manchester City and the Argentina national team.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
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
 }
]
