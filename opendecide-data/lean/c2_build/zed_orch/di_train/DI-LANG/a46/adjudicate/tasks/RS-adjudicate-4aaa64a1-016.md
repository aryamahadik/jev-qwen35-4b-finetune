# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-016

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-016.json

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
  "aid": "a00800",
  "kind": "yes/no",
  "text": "Tweet: Why are toddlers allowed in public spaces",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "yes",
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
  "aid": "a00801",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "naming my son onickolas in honor of my love for @NICKIMINAJ",
   "Wouldn't it be funny if I named my son Onickolas in honor of Nicki Minaj."
  ],
  "human_label": "naming my son onickolas in honor of my love for @NICKIMINAJ",
  "read_1": {
   "answer": "Wouldn't it be funny if I named my son Onickolas in honor of Nicki Minaj.",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "Wouldn't it be funny if I named my son Onickolas in honor of Nicki Minaj.",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00802",
  "kind": "yes/no",
  "text": "Claim: Arola (microcar) SARL became part of Aixam group in 1983. The company that purchased that group, Polaris Industries, is based in Roseau, Minnesota, USA.\n\nPassages:\n\n[Polaris Industries]\nPolaris is based in Roseau, Minnesota, USA.\n\n[Aixam]\nOn April 11, 2013, US based Polaris Industries announced that it had acquired Aixam-Mega.\n\n[Arola (microcar)]\nArola became part of the Aixam group in 1983.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00803",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "traitor by olivia rodrigo in the background ?? YES",
   "NOT OLIVIA RODRIGO TRAITOR IN THE BACKGROUND #LoveIsland"
  ],
  "human_label": "NOT OLIVIA RODRIGO TRAITOR IN THE BACKGROUND #LoveIsland",
  "read_1": {
   "answer": "traitor by olivia rodrigo in the background ?? YES",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "traitor by olivia rodrigo in the background ?? YES",
   "confidence": 0.45
  }
 },
 {
  "aid": "a00804",
  "kind": "yes/no",
  "text": "Text: Happy birthday to me!! I’m 30! 😭",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00805",
  "kind": "yes/no",
  "text": "Claim: Pari Lake flows down to this gigantic lake. Sniardwy is farther north than that gigantic lake.\n\nPassages:\n\n[Pari Lake]\nThe western face of the lake is open and its water flows down to the gigantic Kundol Lake which is situated in the foothills.\n\n[Śniardwy]\nŚniardwy (German: ) is a lake in the Masurian Lake District of the Warmian-Masurian Voivodeship, Poland.\n\n[Kundol Lake]\nKundol Lake also known as \"Kundol Dand\", is a lake in Swat Valley, Khyber Pakhtunkhwa, Pakistan, which is located in the north of Utror valley at a distance of 19 km away from kalam.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00806",
  "kind": "yes/no",
  "text": "Claim: Jack Harvey was born in a small civil parish that as of 2011 had a population of 1,425.\n\nPassages:\n\n[Bassingham]\nBassingham is a village and civil parish in the North Kesteven district of Lincolnshire, England. The population of the civil parish at the 2011 census was 1,425.\n\n[Jack Harvey (racing driver)]\nJack Harvey (born 15 April 1993 in Bassingham, Lincolnshire) is a British auto racing driver, and a former member of McLaren's Young Driver Programme.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00807",
  "kind": "yes/no",
  "text": "Claim: The sponsor of Bringing Up Father (radio) merged with Margarine Unie to create an Indonesian soap factory.\n\nPassages:\n\n[Bringing Up Father (radio)]\nThe sponsor was Lever Brothers.\n\n[Lever Brothers]\nIn 1930, Lever Brothers merged with Margarine Unie to form Unilever.\n\n[Unilever Indonesia]\nPT Unilever Indonesia Tbk () was established in Indonesia on December 5, 1933 as Lever Zeepfabrieken N.V., a subsidiary of Lever Brothers which initially operated a soap factory at Angke, Jakarta.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00808",
  "kind": "yes/no",
  "text": "Post: Amazing show last night from @TheMovielifeNYC (w/ special guest @brettromnes!) - thanks @vinniecaruana, @BrandonReilly and Navetta Bros. !",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00809",
  "kind": "yes/no",
  "text": "Claim: The author of the fantasy short story and fairy series, \"Dănilă Prepeleac\", was born in 1837.\n\nPassages:\n\n[Ion Creangă]\nIon Creangă (] ; also known as Nică al lui Ștefan a Petrei, Ion Torcălău and Ioan Ștefănescu; March 1, 1837 – December 31, 1889) was a Moldavian, later Romanian writer, raconteur and schoolteacher.\n\n[Dănilă Prepeleac]\n\"Dănilă Prepeleac\" (] ; occasionally translated as \"Danilo the Pole\", \"Dănilă Haystack-Peg\" or \"Danillo Nonsuch\") is an 1876 fantasy short story and fairy tale by Romanian author Ion Creangă, with a theme echoing influences from local folklore.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00810",
  "kind": "yes/no",
  "text": "Claim: Bridge of Spies stars a Soviet intelligence agent with the name Rudolf Abel.\n\nPassages:\n\n[Rudolf Abel]\nRudolf Ivanovich Abel (Russian: Рудольф Иванович Абель ), real name Vilyam \"Willie\" Genrikhovich Fisher (Вильям \"Вилли\" Генрихович Фишер), (July 11, 1903 – November 15, 1971) was a Soviet intelligence officer.\n\n[Bridge of Spies (film)]\nSet during the Cold War, the film tells the story of lawyer James B. Donovan, who is entrusted with negotiating the release of Francis Gary Powers—a U.S. Air Force pilot whose U-2 spy plane was shot down over the Soviet Union in 1960—in exchange for Rudolf Abel, a convicted Soviet KGB spy held under the custody of the United States, whom he represented at trial.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00811",
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
  }
 },
 {
  "aid": "a00812",
  "kind": "yes/no",
  "text": "Claim: A news publication, which named a woman in its list of top global tinkers, was founded in 1970. The woman translated \"Time for Outrage!\" into English.\n\nPassages:\n\n[Time for Outrage!]\nby the French diplomat, member of the French Resistance and concentration camp survivor Stéphane Hessel.\n\n[Foreign Policy]\nForeign Policy is an American news publication, founded in 1970 and focused on global affairs, current events, and domestic and international policy.\n\n[Stéphane Hessel]\nIn 2011 he was named by \"Foreign Policy\" magazine in its list of top global thinkers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00813",
  "kind": "yes/no",
  "text": "Claim: Bruce Darnell was a jury member for a German talent show german pop singer Vanessa Krasniqi took part in. He was also an American model and choreographer born in 1957.\n\nPassages:\n\n[Bruce Darnell]\nBruce Darnell (born July 19, 1957) is an American model and choreographer based in Germany.\n\n[Deutschland sucht den Superstar (season 9)]\nJury members Fernanda Brandao and Patrick Nuo left DSDS and were replaced by Bruce Darnell and Cascada's Natalie Horler.\n\n[Vanessa Krasniqi]\nShe rose to fame after taking part in the ninth season of the German talent show \"Deutschland sucht den Superstar\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.92
  }
 },
 {
  "aid": "a00814",
  "kind": "yes/no",
  "text": "Claim: The singer in which Jorge Salan played lead guitarist for in an European tour originates in the city of Brooklyn in the confederated state of new York.\n\nPassages:\n\n[Robin Beck]\nRobin Beck (born November 7, 1954 in Brooklyn, New York) is an American singer.\n\n[Jorge Salán]\nHe is most well known for being the lead guitar for the metal rock solo singer Jeff Scott Soto (leading voice of Journey, Yngwie Malmsteen) and the Jeff Scott Soto Band (now SOTO) from 2009 till today, the lead guitar on Robin Beck's European Tour 2013, and for having collaborated with a long list of legendary rock musicians such as Fiona Flanagan or bass guitar player Bob Daisley.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00815",
  "kind": "yes/no",
  "text": "Claim: This species and the relative of the Fir are classified as genus in the naming system. Parnassius nordmanni is a high altitude butterfly which is found the Caucasus. The larva feeds on this species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\nPassages:\n\n[Parnassius nordmanni]\nThe larva feeds on \"Corydalis\" species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\n[Corydalis]\nCorydalis (Greek \"korydalís\" \"crested lark\") is a genus of about 470 species of annual and perennial herbaceous plants in the Papaveraceae family, native to the temperate Northern Hemisphere and the high mountains of tropical eastern Africa.\n\n[Cedrus]\nCedrus (common English name cedar) is a genus of coniferous trees in the plant family Pinaceae.\n\n[Fir]\nFirs are most closely related to the genus \"Cedrus\" (cedar).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00816",
  "kind": "yes/no",
  "text": "Claim: Gabby West won a competition on the reality show \"Scream Queens\". Her prize was a role in a movie starring Costas Mandylor. The movie had a video game released one week prior to its premier.\n\nPassages:\n\n[Saw 3D]\nSaw 3D (also known as Saw: The Final Chapter, or simply Saw VII) is a 2010 American 3D horror film directed by Kevin Greutert, written by Patrick Melton and Marcus Dunstan, and starring Tobin Bell, Costas Mandylor, Betsy Russell, Sean Patrick Flanery and Cary Elwes.\n\n[Saw II: Flesh &amp; Blood]\nIt was released in 2010 to coincide with the release of the seventh film, \"Saw 3D\", a week later.\n\n[Gabby West]\nShe won a role in \"Saw 3D\" in a competition on the reality show \"Scream Queens\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
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
  "aid": "a00817",
  "kind": "yes/no",
  "text": "Claim: The creator of The Life & Times of Tim and this man are not both art dealers. The other man currently owns the Nathaniel L. McCready House.\n\nPassages:\n\n[Nathaniel L. McCready House]\nIn 2011, the home was purchased by Larry Gagosian, who demolished the mansion's interior.\n\n[The Life &amp; Times of Tim]\nThe series was created by Steve Dildarian, and is about a hapless man in his mid-20s named Tim (voiced by Dildarian) who lives in New York City with his girlfriend Amy.\n\n[Steve Dildarian]\nSteve Dildarian (born November 3, 1969) is an American former advertising copywriter who is the creator, writer, producer and voice of Tim in the HBO animated television series \"The Life & Times of Tim\" (2008-2012).\n\n[Larry Gagosian]\nLawrence Gilbert \"Larry\" Gagosian (born April 19, 1945) is an Armenian American art dealer who owns the Gagosian Gallery chain of art galleries.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00818",
  "kind": "yes/no",
  "text": "Text: Excited to present some research, listen to some studies and learn some stats at the #PsyPAG2021 conference :)",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
  "aid": "a00819",
  "kind": "yes/no",
  "text": "Claim: 3TEETH was the debut album for the opening act for the2016 tour with a headlining band that was formed in the California city of Los Angeles.\n\nPassages:\n\n[3Teeth (album)]\nTwo years after the album's release, 3Teeth embarked on the 2016 Tool tour as first opening act, followed by Primus.\n\n[Tool (band)]\nTool is an American rock band from Los Angeles, California.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00820",
  "kind": "yes/no",
  "text": "Claim: The nationality of the writer of detective novel Right Now: A 12-Step Program for Defeating the Obama Agenda is American.\n\nPassages:\n\n[Michael Steele]\nMichael Stephen Steele (born October 19, 1958) is an American politician and MSNBC political analyst as of May 2011.\n\n[Right Now (book)]\nRight Now: A 12-Step Program for Defeating the Obama Agenda, written by Michael Steele, was released on January 4, 2010.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00821",
  "kind": "yes/no",
  "text": "Claim: The album 38 Special, which was released before Resolution in 1997, was released in 1991. The vocalist on the 1991 album plays the guitar while Denis Bélanger does not.\n\nPassages:\n\n[Max Carl]\nMax Carl Gronenthal (born January 29, 1950) is an American rock singer, keyboardist, guitarist and songwriter.\n\n[Bone Against Steel]\nIt was their last album until their 1996 comeback and the last album to feature the vocalist and keyboard player Max Carl.\n\n[Resolution (38 Special album)]\nIt was their first album since \"Bone Against Steel\" in 1991 before reforming in 1996.\n\n[Denis Bélanger]\nDenis \"Snake\" Bélanger (born August 9, 1964) is the vocalist and lyricist of the Canadian heavy metal band Voivod.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
  "aid": "a00822",
  "kind": "yes/no",
  "text": "Claim: The 1955 Florida Gators football team beat this non-professional team with a score of 20–14. The head coach of that team left after the 1955 college football season. He was born on July 6, 1924.\n\nPassages:\n\n[Darrell Royal]\nDarrell K Royal (July 6, 1924 – November 7, 2012) was an American football player and coach.\n\n[1955 Mississippi State Maroons football team]\nThe 1955 Mississippi State Maroons football team represented Mississippi State College during the 1955 college football season. After the season, head coach Darrell Royal left to take the job at Washington.\n\n[1955 Florida Gators football team]\nThe highlights of the 1955 season included three conference victories over the Mississippi State Maroons (20–14), LSU Tigers (18–14) and Georgia Bulldogs (19–13).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00823",
  "kind": "yes/no",
  "text": "Text: somebody tell these birds to be quiet because they not listening to me",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
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
  "aid": "a00824",
  "kind": "yes/no",
  "text": "Claim: Anna-Lena Grönefeld and another American athlete are both tennis players. This other athlete won the singles title at the 1979 Romika Cup.\n\nPassages:\n\n[Manuel Orantes]\nManuel Orantes Corral (] ; born 6 February 1949) is a former tennis player who was active in the 1970s and 1980s.\n\n[1979 Romika Cup]\nFirst-seeded Manuel Orantes won the singles title.\n\n[Anna-Lena Grönefeld]\nAnna-Lena Grönefeld (born 4 June 1985) is a German tennis player.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00825",
  "kind": "yes/no",
  "text": "Claim: Xavier Dolan is the director of the upcoming Candian drama feature film in which the actress who made her film début as the love interest in Wes Anderson's \"The Darjeeling Limited\" stars.\n\nPassages:\n\n[Amara Karan]\nAmara Karan (born 1984) is a Sri Lankan-English actress who made her film début as the love interest in Wes Anderson's \"The Darjeeling Limited\".\n\n[The Death and Life of John F. Donovan]\nThe Death and Life of John F. Donovan is an upcoming Canadian drama film, co-written, co-produced and directed by Xavier Dolan in his English-language debut. It stars Kit Harington, Natalie Portman, Jessica Chastain, Susan Sarandon, Kathy Bates, Jacob Tremblay, Ben Schnetzer, Thandie Newton, Amara Karan, Chris Zylka, Jared Keeso, Emily Hampshire and Michael Gambon.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
  "aid": "a00826",
  "kind": "yes/no",
  "text": "Claim: Enigma which is a German project band recorded a song with vocals by a duo from Silverdale, England.\n\nPassages:\n\n[Aquilo (band)]\nAquilo is an alternative musical duo from Silverdale, Lancashire, England, consisting of Tom Higham and Ben Fletcher.\n\n[Amen (Enigma song)]\n\"Amen\" is a song by German musical project Enigma, featuring vocals by English dream-pop duo Aquilo.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00827",
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
  }
 },
 {
  "aid": "a00828",
  "kind": "yes/no",
  "text": "Claim: Garth Jennings directed and wrote the 2016 film featuring the voice of the host of We're Dancin'.\n\nPassages:\n\n[We're Dancin']\nTownsend Coleman was the show's host.\n\n[Townsend Coleman]\n\", \"My Life As A Teenage Robot\" and \"The Replacements\" and he also did the voice of Knotty in \"\" (1992) and he also did additional voices in films \"Fantasia 2000\" (1999) and \"Sing\" (2016)\n\n[Sing (2016 American film)]\nIt was directed and written by Garth Jennings, co-directed by Christophe Lourdelet, and starring the voices of Matthew McConaughey, Reese Witherspoon, Seth MacFarlane, Scarlett Johansson, John C. Reilly, Taron Egerton, and Tori Kelly.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
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
  "aid": "a00829",
  "kind": "yes/no",
  "text": "Claim: The Taigan dog breed is NOT recognized by the Fédération Cynologique Internationale (FCI), the native Korean dog Nureongi or the Taigan.\n\nPassages:\n\n[Nureongi]\nLike native Korean dogs such as the Korean Jindo, Korean Yellow spitzes are medium-sized spitz, but with greater musculature and distinctive coat patterns.\n\n[Korean Jindo]\nThe Jindo breed became recognized by the United Kennel Club on January 1, 1998 and by the Fédération Cynologique Internationale in 2005.\n\n[Taigan]\nThe Taigan (Kyrgyz: Тайган ) also known as Kyrgyzdyn Taighany (Kyrgyzskaya Borzaya Taigan in Russian) is a sighthound breed from Kyrgyzstan, which is not yet recognized by the FCI, but is recognized by a number of kennel clubs on national level.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00830",
  "kind": "yes/no",
  "text": "Claim: Howard Elliott Ashman worked on both \"Little Shop of Horrors\" and the song referenced in the Be Our Guest Restaurant.\n\nPassages:\n\n[Be Our Guest Restaurant]\nThe name of the restaurant is a reference to \"Be Our Guest\", one of the classic songs from that film.\n\n[Howard Ashman]\nHoward Elliott Ashman (May 17, 1950 – March 14, 1991) was an American playwright and lyricist. Their next musical, \"Little Shop of Horrors\" (1982) for which Ashman again directed and wrote both book and lyrics, became a long-running success and led to a 1986 feature film.\n\n[Be Our Guest]\n\"Be Our Guest\" is a song written by lyricist Howard Ashman and composer Alan Menken for Walt Disney Pictures' 30th animated feature film \"Beauty and the Beast\" (1991).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00831",
  "kind": "yes/no",
  "text": "Claim: A freeway that runs east-west through Bower in part of a country was named after an author. He was born 16 November 1920. Bossiaea walkeri is a flowering plant found in this part of a country.\n\nPassages:\n\n[Colin Thiele]\nColin Milton Thiele AC ( ; 16 November 1920 – 4 September 2006) was an Australian author and educator.\n\n[Thiele Highway]\nIt is named after author Colin Thiele who lived most of his life in towns along the route, and set some of his stories in the area.\n\n[Bossiaea walkeri]\nIt occurs in Western Australia, South Australia, Victoria and New South Wales.\n\n[Bower, South Australia]\nBower is a town in South Australia, approximately halfway between Eudunda and Morgan on the Thiele Highway.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00832",
  "kind": "yes/no",
  "text": "Post: Trying to know all this history tonight is gonna kill me",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
  "aid": "a00833",
  "kind": "yes/no",
  "text": "Claim: Natalie Anne Merchant has a wider scope of profession than Marian Gold.\n\nPassages:\n\n[Natalie Merchant]\nNatalie Anne Merchant (born October 26, 1963) is an American singer-songwriter and musician.\n\n[Marian Gold]\nHartwig Schierbaum (born 26 May 1954), better known by his stage name Marian Gold, is the lead singer of the German synthpop group Alphaville, and has also recorded as a solo artist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00834",
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
  }
 },
 {
  "aid": "a00835",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "‘It’s only a game’ 🥴🥴",
   "Look how important these clubs are to their fans!"
  ],
  "human_label": "‘It’s only a game’ 🥴🥴",
  "read_1": {
   "answer": "Look how important these clubs are to their fans!",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "Look how important these clubs are to their fans!",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00836",
  "kind": "yes/no",
  "text": "Claim: The travel hub is a mile south of the area KJAL is licensed to. Along with Hoonah Airport, which is also a mile south, are both on American territory.\n\nPassages:\n\n[Tafuna, American Samoa]\nIt is located on a peninsula a mile north of Pago Pago International Airport and one mile south of Nu'uuli, American Samoa.\n\n[Hoonah Airport]\nHoonah Airport (IATA: HNH, ICAO: PAOH, FAA LID: HNH) is a state-owned public-use airport located one nautical mile (2 km) southeast of the central business district of Hoonah, Alaska.\n\n[Pago Pago International Airport]\nPago Pago International Airport (IATA: PPG, ICAO: NSTU, FAA LID: PPG) , also known as Tafuna Airport, is a public airport located 7 miles (11.3 km) southwest of the central business district of Pago Pago, in the village and plains of Tafuna on the island of Tutuila in American Samoa, an unincorporated territory of the United States.\n\n[KJAL]\nLicensed to Tafuna, American Samoa, it served the American Samoa area.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
  "aid": "a00837",
  "kind": "yes/no",
  "text": "Claim: The academic publication responsible for the Global Open Access Forum was published before Dwell.\n\nPassages:\n\n[Global Open Access Forum]\nIt was created by the American Scientist, which is published by Sigma Xi, in September 1998, before the term \"Open Access\" (OA) was coined, and it was originally called the \"September98-Forum.\"\n\n[American Scientist]\nAmerican Scientist (informally abbreviated AmSci) is an American bimonthly science and technology magazine published since 1913 by Sigma Xi, The Scientific Research Society.\n\n[Dwell (magazine)]\nIt was launched with a magazine in September 2000 to bridge the gap between design professionals and enthusiasts by Lara Hedberg Deam with architecture and design critic Karrie Jacobs as its Editor-in-Chief.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00838",
  "kind": "yes/no",
  "text": "Claim: In the early 17th-century the black Angolan who was one of the earliest African-American landowners in the United States,acieved freedom.\n\nPassages:\n\n[Zipporah Potter Atkins]\nThe purchase of her home, dated 1670, makes her the first African American to own land in the city of Boston, and with Anthony Johnson (colonist) one of the earliest African-American landowners in what would become the United States.\n\n[Anthony Johnson (colonist)]\nAnthony Johnson ( 1600 – 1670) was a black Angolan who achieved freedom in the early 17th-century Colony of Virginia after serving his term of indenture.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
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
  "aid": "a00839",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I would say \"bonding with the jsc homies\".",
   "💫jsc bonding nights💫🥰🥳"
  ],
  "human_label": "💫jsc bonding nights💫🥰🥳",
  "read_1": {
   "answer": "I would say \"bonding with the jsc homies\".",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "I would say \"bonding with the jsc homies\".",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00840",
  "kind": "yes/no",
  "text": "Text: @rolandsmartin @nypost Damn!  At my wedding we drank enough to make up for the no shows!  🤔",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
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
  "aid": "a00841",
  "kind": "yes/no",
  "text": "Post: I get a lot of boy who cried wolf vibes from the Red Cross and their emergency blood shortages all the time",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
  "aid": "a00842",
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
  }
 },
 {
  "aid": "a00843",
  "kind": "yes/no",
  "text": "Claim: Avram Noam Chomsky, not the author of Memed, My Hawk, has writen more books.\n\nPassages:\n\n[Noam Chomsky]\nAvram Noam Chomsky ( ; born December 7, 1928) is an American linguist, philosopher, cognitive scientist, historian, social critic, and political activist. He is the author of over 100 books on topics such as linguistics, war, politics, and mass media.\n\n[Memed, My Hawk]\nMemed, My Hawk (Turkish: \"İnce Memed, meaning \"Memed, the Slim\"\" ) is a 1955 novel by Yaşar Kemal.\n\n[Yaşar Kemal]\nYaşar Kemal (born Kemal Sadık Gökçeli; 6 October 1923 – 28 February 2015) was a Turkish writer and human rights activist of Kurdish origin. He was one of Turkey's leading writers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
  "aid": "a00844",
  "kind": "yes/no",
  "text": "Claim: Wheel in the Sky is a song by a band. Its writer and Jimmy Barnes do not have the same nationality.\n\nPassages:\n\n[Jimmy Barnes]\nJames Dixon Swan {'1': \", '2': \", '3': \", '4': \"} (born 28 April 1956), better known as Jimmy Barnes, is a Scottish-Australian rock singer-songwriter.\n\n[Robert Fleischman]\nRobert Fleischman (born March 11, 1953) is an American musician, songwriter, and record producer.\n\n[Wheel in the Sky]\nIt was written and composed by Robert Fleischman, Neal Schon and Diane Valory.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
  "aid": "a00845",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Legos are exhilarating",
   "High stakes legos"
  ],
  "human_label": "High stakes legos",
  "read_1": {
   "answer": "Legos are exhilarating",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "Legos are exhilarating",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00846",
  "kind": "yes/no",
  "text": "Claim: The coach of the unknown Oklahoma Sooners football team died February 9, 1994.\n\nPassages:\n\n[1963 Oklahoma Sooners football team]\nThey were coached by head coach Bud Wilkinson, who would retire from coaching after the conclusion of the season.\n\n[Bud Wilkinson]\nCharles Burnham \"Bud\" Wilkinson (April 23, 1916 – February 9, 1994) was an American football player, coach, broadcaster, and politician.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
  "aid": "a00847",
  "kind": "yes/no",
  "text": "Claim: The out-of-town store where an IMAX Digital 3D theater is in is a furniture retailer with a location in an enclosed shopping mall on the north side of Interstate 295 near the junction with Interstate 95.\n\nPassages:\n\n[Warwick Mall]\nWarwick Mall is an enclosed shopping mall in Warwick, Rhode Island, on the north side of Interstate 295 near the junction with Interstate 95.\n\n[Jordan's Furniture]\nJordan's Furniture is a furniture retailer in New England. There are currently seven locations - in Reading, Avon, Taunton, Natick, Massachusetts, Nashua, New Hampshire, Warwick Mall in Warwick, Rhode Island, and New Haven, Connecticut.\n\n[Jordan's IMAX]\nThe Sunbrella IMAX Theaters (formerly the Verizon IMAX Theaters) are two IMAX Digital 3D theaters located in Jordan's Furniture stores in Natick, Massachusetts and Reading, Massachusetts.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
  "aid": "a00848",
  "kind": "yes/no",
  "text": "Claim: The genus which includes \"Little Pickles\" has more species in it than Stangeria.\n\nPassages:\n\n[Stangeria]\nStangeria eriopus is a cycad endemic to southern Africa It is the sole species in the genus Stangeria, most closely related to the Australian genus \"Bowenia\", with which it forms the family Stangeriaceae.\n\n[Othonna capensis]\nOthonna capensis also known as Little Pickles, is a species of the genus \"Othonna\" and family Asteraceae and is a native of South Africa.\n\n[Othonna]\nOthonna is a genus of African plants in the sunflower family.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
  "aid": "a00849",
  "kind": "yes/no",
  "text": "Claim: The non-ranking snooker player Chris Norbury lost to made the final of the 2017 China Championship. The player that made the final got the nickname \"The Magician\".\n\nPassages:\n\n[Luca Brecel]\nThe following year, he became the first player from mainland Europe to win a ranking event, defeating Shaun Murphy in the final of the 2017 China Championship.\n\n[Chris Norbury]\nHe played in the latter stages of the Paul Hunter Classic in both 2008 and 2009, losing in the first round to Shaun Murphy 4–1 in 2008, and losing to Dave Harold 4–2 in 2009.\n\n[Shaun Murphy (snooker player)]\nNicknamed \"The Magician\", Murphy is noted for his straight cue action and his long potting.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
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
