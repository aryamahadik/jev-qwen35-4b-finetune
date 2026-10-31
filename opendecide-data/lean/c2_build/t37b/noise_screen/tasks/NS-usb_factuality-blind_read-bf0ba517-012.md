# Replay noise screen blind read NS-usb_factuality-blind_read-bf0ba517-012 (family NS-usb_factuality)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-usb_factuality-blind_read-bf0ba517-012.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q5897d6008a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Johanns began campaigning early in Nebraska's 1998 gubernatorial election, holding his first campaign event in October 1995.\n- On November 3, 1998, Johanns and his running mate, David I. Maurstad, defeated Hoppner and his running mate, Pam Bataillon, in the general election, by a margin of 54% to 46%.\n- Johanns succeeded Iowa Governor Tom Vilsack as chair of the Midwestern Governors Association in 2002.\n- Johanns was confirmed in a voice vote by the Senate on January 20, 2005, hours after Bush's second inauguration.\n\nSummary sentence:\nHe served as the governor of Nebraska, elected in 1998 until 2005, and was chair of the Midwestern Governors Association in 2002.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf5709f9fc3",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Thorburn competed on the inaugural Snooker Legends Tour in 2010.\n- At the age of 70, Thorburn won the 2018 Seniors Masters at the Crucible Theatre, defeating Jonathan Bagley 2–0 in the final.\n\nSummary sentence:\nThorburn subsequently competed in Snooker Legends events and on the World Seniors Tour, winning the 2018 Seniors Masters at the Crucible Theatre at age 70.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1313033288",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In July 2015, Tuo Zhen was promoted to deputy head of the Propaganda Department of the Communist Party of China, serving as an assistant to Liu Qibao.\n- In April 2018, Tuo was appointed as the Chief Editor of the \"People's Daily\", an official newspaper of the CPC.\n\nSummary sentence:\nFrom July 2015 to 2018 he was the deputy head of the Propaganda Department of the Communist Party of China.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q077b54ccb0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Marni Abbott-Peter\n- She first began swimming at the Pan American Games, where she won five medals, but soon began playing wheelchair basketball in 1988 and made the Canadian national team in 1992.\n\nSummary sentence:\nMarni Abbott-Peter (born October 11, 1965) is a Canadian retired wheelchair basketball player.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qbd62ea6e93",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- It was announced on July 7, 2008, that Coates would be inducted into the New England Patriots Hall of Fame.\n\nSummary sentence:\nAll-Decade Team in 2000 and inducted to the New England Patriots Hall of Fame in 2008.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q890119c6de",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- As Director, he was one of the first people in Britain to whom the term \"spin doctor\" was applied; he was thus called \"the Prince of Darkness\".\n\nSummary sentence:\nHe was one of the first to whom the term 'spin doctor' was applied and gained the nickname 'the Prince of Darkness'.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q7ca2f04d74",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On May 18, 2020, Barr named Shea as the acting administrator of the Drug Enforcement Administration.\n\nSummary sentence:\nFrom May 2020 until January 2021, he served as acting administrator of the Drug Enforcement Administration.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qd67870d7e5",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On March 7, 2019, Penn was cast in the main role of Garrett Modi on the NBC comedy \"Sunnyside\" and the series was ordered on May 6, 2019.\n\nSummary sentence:\nIn 2019, Penn portrayed Garrett Modi in the NBC comedy \"Sunnyside\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q6f942fcce0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Prior to joining the Warriors, Silas served as an advance scout for the Washington Wizards during the 2005–06 season after spending five seasons on the coaching staffs of his father, Paul Silas, with the Cleveland Cavaliers and both Hornets' franchises.\n- Silas served as an assistant coach for the Cavaliers from 2003 to 2005, where he worked closely with LeBron James and was responsible for individual skill work, player development, game preparation, pre-game walkthroughs as well as the management and development of the technology and NBA scouting systems for the coaching staff.\n- Silas also spent three seasons as an assistant coach with the Charlotte Hornets prior to joining the Cavaliers.\n\nSummary sentence:\nHe worked under his father at the Charlotte Hornets for three seasons and the Cleveland Cavaliers from 2003 to 2005.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q30587d3199",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- It was co-produced by Younger with Charles Fisher and Alan Thorne.\n\nSummary sentence:\nHe has teamed up with Alan Thorne.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q7be23d5739",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He is also Chairman of Ferrari, Vice Chairman of GEDI Gruppo Editoriale S.p.a. and a board member of Partner Re.\n\nSummary sentence:\nHe is Chairman of Ferrari.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q1b316e1dfe",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He is playing Bill Clinton in the miniseries \"Impeachment: American Crime Story\".\n\nSummary sentence:\nHe also portrayed Bill Clinton in \"American Crime Story\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd96738aa05",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2005, as a member of a working party set up by the Royal College of Physicians, he was the chief author of their report into the future of medical professionalism, \"Doctors in Society\".\n\nSummary sentence:\nIn 2005 he wrote \"Doctors in society\", an inquiry into the future of medical professionalism, for the Royal College of Physicians.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q21b412e59c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He can also be seen as Principal Pearson on the 2016 TV Land comedy \"Teachers\".\n\nSummary sentence:\nPreviously, Bagley had a recurring role as Principal Toby Pearson on the American sitcom \"Teachers\", and he currently plays Peter on \"Grace and Frankie\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q9c49b7c602",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Davis launched the Geena Davis Institute on Gender in Media in 2007, which works collaboratively with the entertainment industry to increase the presence of female characters in media aimed at children, and to reduce inequality in Hollywood and the stereotyping of females by the male-dominated industry.\n\nSummary sentence:\nIn 2007, Davis launched the Geena Davis Institute on Gender in Media, which works collaboratively with the entertainment industry to increase the presence of female characters in media.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf25a66bd25",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Victor Santiago, Jr.\n- Santiago's career began to take off in 1995, while under the pseudonym Noreaga (after Panamanian dictator Manuel Noriega), as part of the duo Capone-N-Noreaga (C-N-N), alongside friend and fellow Queens-based rapper Capone (whom he met while serving time in prison).\n- He officially changed his stage name to N.O.R.E., and after some delays, his third solo studio album \"God's Favorite\", was released in 2002.\n\nSummary sentence:\nVictor Santiago, Jr., known by his stage name N.O.R.E., or Noreaga, is an American rapper from Queens.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q63cc21f710",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- This was followed by \"Bill & Ted's Excellent Adventure\" (1989), in which he portrays a slacker who travels through time with a friend (portrayed by Alex Winter), to assemble historical figures for a school presentation.\n- In 1991, Reeves starred in \"Bill & Ted's Bogus Journey\", a sequel to \"Bill & Ted's Excellent Adventure\", with his co-star Alex Winter.\n\nSummary sentence:\nHe had his breakthrough role in the science fiction comedy \"Bill & Ted's Excellent Adventure\" (1989), and he reprised his role in its sequels.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qe971079f4e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Stewart served as the assistant to Sandy Alderson, the general manager of the Athletics, in 1996.\n- In 1997, he left that position to serve in a similar capacity under Kevin Towers of the San Diego Padres.\n- Stewart left San Diego after the season and interviewed for assistant GM positions with Oakland and the Florida Marlins.\n- His familiarity with the Blue Jays organization was the main reason he accepted the job there under Gord Ash.\n\nSummary sentence:\nGeneral managers he has worked under include Sandy Alderson, Kevin Towers, Gord Ash, and Dean Taylor.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q8f304cb8c1",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Veidekke\n- Veidekke's core activities are linked with construction, property development, civil engineering and consulting, and industrial operations (asphalt/aggregates and road maintenance.\n- Veidekke has grown from being the ninth largest construction company at the beginning of the 1980s to its present position as the largest Norwegian owned construction company.\n\nSummary sentence:\nVeidekke is the largest Norwegian construction and civil engineering company.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf03ac30bec",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Lewis, a fan of the series, initially attended an open audition at the Queens Hotel, Leeds, before being contacted two months later to perform a screen test for director Chris Columbus, eventually earning the role of Neville Longbottom.\n- Lewis returned once more for the final \"Harry Potter\" installments, \"Harry Potter and the Deathly Hallows – Part 1\" (2010) and \"Harry Potter and the Deathly Hallows – Part 2\" (2011).\n\nSummary sentence:\nHe is best known for his role as Neville Longbottom in the \"Harry Potter\" film series.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q9c8b275750",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Stern has served as the Chairman of the TCW Group in 2013.\n\nSummary sentence:\nHe has served as the Chairman of the TCW Group.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q57a2ee8b0e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2012, on the death of his father, Ridley became the 5th Viscount Ridley and Baron Wensleydale.\n- In 2013, he was elected as a hereditary peer to membership in the House of Lords, as a member of the Conservative Party.\n\nSummary sentence:\nHe inherited the viscountcy in 2012 and was a Conservative hereditary peer from 2013, with an elected seat in the House of Lords.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q594ed85811",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She began her career as a freelance journalist in 1966 and had articles published in \"The Economic Times\", \"The Indian Express\" and many other periodicals.\n\nSummary sentence:\nAs a freelance journalist, she has been writing extensively for \"The Indian Express\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q8827512f36",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2010, he was the executive producer and star of \"The Other Guys\", a buddy cop film which also has an ensemble cast which consists of Mark Wahlberg, Eva Mendes, Michael Keaton, Steve Coogan, Ray Stevenson, Samuel L. Jackson, and Dwayne Johnson.\n- He starred alongside Zach Galifianakis in the 2012 political comedy \"The Campaign\", which garnered mediocre reviews and grossed $104 million against a budget of $95 million.\n- In 2015, he starred in the buddy comedy \"Get Hard\" and the comedy \"Daddy's Home\", with the latter reuniting him \"The Other Guys\" co-star Mark Walhberg.\n- Ferrell has worked as a voice actor in several animated television programs and films, including his portrayal of Bob Oblong, a 1950s-style father with no arms or legs, in the short-lived animated television series \"The Oblongs\".\n- Ferrell also starred as Ted (a.k.a.\n- The Man in the Yellow Hat) in the film \"Curious George\" and guest voiced on an episode of the FOX sitcom \"King of the Hill\" as a politically correct soccer coach.\n- He voiced the title character in the 2010 DreamWorks Animation film \"Megamind\" as well as President Business in \"The Lego Movie\", released in 2014.\n\nSummary sentence:\nOther notable film roles include \"The Other Guys\" (2010), \"The Campaign\" (2012), \"Get Hard\" (2015), and the animated films \"Curious George\" and \"Megamind\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q512530740d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On 29 September 2014, he was appointed leader of the Sweden Democrats in the Riksdag.\n\nSummary sentence:\nHe previously served as Leader of the Sweden Democrats from 2014.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q69c1be9a75",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Darude's debut studio album \"Before the Storm\" was produced by JS16 (Jaakko Salovaara), and features two of JS16's remixes.\n- \"Before the Storm\" was released on September 5, 2000 and sold 800,000 copies worldwide, earning Darude three Finnish Grammy awards.\n\nSummary sentence:\nHis debut studio album, \"Before the Storm\", was released on September 18, 2000 and sold 800,000 copies worldwide, earning Darude three Finnish Grammy Awards.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qe4f8c94cab",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He then became active in the political party his father had founded, the Panhellenic Socialist Movement (PASOK).\n- In January 2004, the incumbent PM Costas Simitis announced his resignation as leader of PASOK, and passed the leadership to Papandreou by recommending him as the new leader.\n- In January 2006, Papandreou was unanimously elected President of the Socialist International.\n\nSummary sentence:\nPapandreou was leader of the Panhellenic Socialist Movement (PASOK) party, which his father founded, starting from 2004, and has been President of the Socialist International since January 2006.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q77b7c78c59",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- It also garnered her a nomination for the Grammy Award for Best Comedy Album.\n- Also that year, Schumer wrote a memoir, entitled \"The Girl with the Lower Back Tattoo\".\n- It held the top position on \"The New York Times\" Non-Fiction Best Seller list for two weeks in September 2016 and garnered her a nomination for the Grammy Award for Best Spoken Word Album.\n\nSummary sentence:\nThe same year, she was nominated for two Grammy Awards: for Best Comedy Album for \",\" and Best Spoken Word Album for \"The Girl with the Lower Back Tattoo\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q47c1f4cace",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Suzanne Côté\n- She was nominated to the Supreme Court of Canada by Prime Minister Stephen Harper to replace retiring justice Louis LeBel.\n- She was appointed a puisne justice on December 1, 2014.\n\nSummary sentence:\nSuzanne Côté is a puisne justice of the Supreme Court of Canada.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q401ef4c9d0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Jiří Dienstbier Jr.\n- Jiří Dienstbier Jr. is the son of Jiří Dienstbier Sr., former journalist and civil rights activist who became the first Minister of Foreign Affairs in the newly democratic Czechoslovakia, and Zuzana Dienstbierová, née Wíšová, a psychologist.\n- Dienstbier worked as a lawyer for fifteen years.\n- From March 2011 to March 2013, Dienstbier served as Deputy Chairman of the Social Democratic Party.\n- In March 2011, Dienstbier won a by-election for the Czech Senate in the Kladno constituency, filling the seat that became vacant on the death of his father, Jiří Dienstbier.\n- He stood for reelection in 2020 but did not progress from the first round of elections.\n\nSummary sentence:\nJiří Dienstbier Jr. is a Czech politician, lawyer and the Senator for Kladno from 2011 to 2020, representing the Social Democratic Party.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q86b9d7d264",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Acosta served in four presidentially appointed, U.S. Senate-confirmed positions in the George W. Bush administration.\n- From December 2002 to August 2003, he was a member of the National Labor Relations Board for which he participated in or authored more than 125 opinions.\n- Then, he became Assistant Attorney General for the Civil Rights Division on August 22, 2003, where he was known for increasing federal prosecutions against human trafficking.\n- Acosta, then the U.S. Attorney for the Southern District of Florida, agreed to a plea deal, to grant immunity from all federal criminal charges to Epstein, along with four named co-conspirators and any unnamed \"potential co-conspirators\".\n\nSummary sentence:\nA member of the Republican Party, he was appointed by President George W. Bush to the National Labor Relations Board, and later served as the assistant attorney general for civil rights and the U.S. attorney for the Southern District of Florida.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc15b5b6f10",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bachchan better established himself in Hindi cinema playing a no-nonsense Mumbai police officer in the hit action thriller \"Dhoom\" (2004), which also starred John Abraham, Uday Chopra, Esha Deol, and Rimi Sen in pivotal roles.\n\nSummary sentence:\nHis first commercial successes came with the 2003 & 2004 action films \"Zameen\" and \"Dhoom\", which changed his career prospects.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q5e3ed1c9ca",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He taught at the London School of Economics and at the University of Glasgow before finding a long-term position at the University of Hull.\n- He also held the Centennial Professorship in the Centre for the Study of Global Governance at the London School of Economics and a professorship of political philosophy at the University of Westminster.\n\nSummary sentence:\nHe was Professor at the University of Hull, and Professor of Political Philosophy at the University of Westminster.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q3bbe2d6e2f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Penn had a recurring role on \"How I Met Your Mother\" for the seventh season of the show, in which he played Kevin, a therapist and later boyfriend of Robin Scherbatsky.\n\nSummary sentence:\nHe had a role in the television series \"How I Met Your Mother.\"",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q7b3aa8bbc1",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bentley has starred in several films, including the Oscar-winning film \"American Beauty\", \"The Four Feathers\", \"P2\", and \"Ghost Rider\".\n- In the 2007 film \"Ghost Rider\", Bentley played Blackheart, a demonic being that was the main antagonist.\n\nSummary sentence:\nHis other film roles include \"The Four Feathers\", \"Ghost Rider\" (2007), and \"P2\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q20ddb1957a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In his first season with the Tennessee Titans in 2005, Vanden Bosch started all 16 games and made his first Pro Bowl after finishing second in the AFC and fourth in the NFL with 12.5 sacks.\n- On March 5, 2010, Vanden Bosch was signed to a four-year, $26 million deal with the Detroit Lions.\n\nSummary sentence:\nHe also played for the Tennessee Titans and Detroit Lions.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc26d166262",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Aivaras Abromavičius\n- Abromavičius was born in Lithuania, but lived in Estonia, Sweden, USA and Russia for many years.\n- During 2002–2014, he co-owned and was at the core of building a Stockholm-based investment company East Capital, one of the largest and most reputable Investment companies from western Europe investing in eastern Europe.\n- Ukrainian President Petro Poroshenko granted citizenship to Abromavičius, Natalie Jaresko and Alexander Kvitashvili on 2 December 2014 to allow them to serve as ministers in the Second Yatsenyuk Government.\n\nSummary sentence:\nAivaras Abromavičius (, born 21 January 1976) is a Lithuanian-born Ukrainian investment banker and politician.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q6ef6036a3f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dallas Sartz\n- He was originally a powerful safety, but was later moved to linebacker in college.\n- Sartz began working as a coach for the UC Davis Aggies football team, who compete at the FCS level of college football, during the 2010 season.\n\nSummary sentence:\nDallas Sartz (born July 8, 1983) is a former American football linebacker and assistant coach for the UC Davis football team.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q903bd98fea",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Te Aute College\n- On 3 February 1931, the college was severely damaged by the Hawke's Bay earthquake.\n- On 27 November 1986, the house of Allen Williams was recognised as a Category I heritage building by the New Zealand Historic Places Trust.\n\nSummary sentence:\nTe Aute College is a school in the Hawke's Bay region of New Zealand.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qbef1e69b4b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In September 2016, following the dismissal and disciplinary investigation into Huang Xingguo, Wang was named mayor of Tianjin.\n\nSummary sentence:\nHe was formerly the Mayor of Tianjin, one of the four direct-controlled municipalities of China.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q4fe3f854a0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Santoshi's followup was the universally acclaimed film \"Damini\" (1993), which dealt with issues like the status of women in our society and the perspective of people towards women.\n- The following year he made Ghatak: Lethal (1996), an action film, marking his third collaboration with Sunny Deol and Meenakshi Sheshadri.\n\nSummary sentence:\nHe next directed \"Damini\" (1993) and \"Ghatak: Lethal\" (1996).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q100cc980be",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Holliday is the chairman of Council on Competitiveness and the Business Roundtable's Task Force for Environment, Technology and Economy.\n\nSummary sentence:\nHe is chairman emeritus of the U.S. Council on Competitiveness and chairman of the Business Roundtable's Task Force for Environment, Technology and Economy.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc2334faa22",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Chloe Rose\n- Rose was born and raised in Toronto, Ontario.\n- Rose first attracted attention for her portrayal of Katie Matlin in the long-running teen drama television series Degrassi: The Next Generation.\n\nSummary sentence:\nRose is a Canadian actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf1b5b12e88",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Maden first came to prominence with his participation in the third season (2004–2005) of Endurance, entitled Endurance 3: Hawaii.\n- The series, filmed on location at an island in Kauai's North Shore, consists of 21 episodes and aired on Discovery Kids between 2004 and 2005.\n\nSummary sentence:\nPrior to acting, Maden was also a participant in the third season of the Discovery Kids series \"Endurance\" (2004–2005).",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qbcbc71093d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2021, he reprised his role as Twinkie in \"F9\".\n\nSummary sentence:\nHe reprised his role as Twinkie in \"F9\" (2021).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qccf46e3f96",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Travis had the leading role of psychology professor Dr. Joyce Reardon in 2002's four-hour television adaptation of \"Stephen King's Rose Red\".\n- In 2002, Travis joined the cast of the CBS sitcom \"Becker\" as Chris Connor.\n- She starred in the show for its final two seasons, replacing the series' original female lead, Terry Farrell.\n\nSummary sentence:\nIn 2002, she played a leading role in the ABC miniseries \"Rose Red\", and later joined the cast of the CBS sitcom \"Becker\" for its final two seasons.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd1bba493ab",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Ahrens met Stephen Flaherty at the BMI Workshop in 1982 and they started working together the following year.\n- Their first professionally produced musical together was \"Lucky Stiff\", which premiered Off-Broadway at Playwrights Horizons in April 1988.\n- Their next musical was \"Once on This Island\", which premiered on Broadway in 1990 and which was nominated for eight Tony Awards.\n- \"My Favorite Year\" opened at the Vivian Beaumont Theater in Lincoln Center in October 1992 and ran for 36 performances, winning the Tony Award for Andrea Martin as Best Supporting Actress.\n- \"Ragtime\" followed, opening on Broadway in January 1998 and running for 834 performances.\n- \"Seussical\" opened on Broadway in November 2000, and received a Grammy nomination.\n- Ahrens and Flaherty's next musicals, \"A Man of No Importance\" (2002), \"Dessa Rose\" (2005), and \"The Glorious Ones\" (2007) were produced at the Mitzi E. Newhouse Theater in Lincoln Center.\n- Their musical version of \"Rocky the Musical\" premiered in Hamburg, Germany in October 2012.\n- They have written a dance musical, \"Little Dancer\", with direction and choreography by Susan Stroman, about a ballerina and Edgar Degas, which had a reading in 2010 at Lincoln Center Theater and a developmental lab production in June 2012.\n- Ahrens and Flaherty have written the songs for the stage adaptation of the film \"Anastasia\".\n\nSummary sentence:\nTogether with Flaherty, she has written many musicals, including \"Lucky Stiff\", \"My Favorite Year\", \"Ragtime\", \"Seussical\", \"A Man of No Importance\", \"Dessa Rose\", \"The Glorious Ones\", \"Rocky\", \"Little Dancer\", \"Anastasia\" and \"Once on This Island\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qe647443785",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She began by writing the \"Boston Letter\" for \"Art International,\" but soon published well-received articles on Jasper Johns (\"Lugano Review\", 1965) and Donald Judd (\"Allusion and Illusion in Donald Judd,\" \"Artforum\", May 1966).\n- Krauss used \"October\" as a way of publishing essays on post-structuralist art theory, Deconstructionist theory, psychoanalysis, postmodernism and feminism.\n- Whether about (Cubist collage, Surrealist photography, early Giacometti sculpture, Rodin, Brâncuși, Pollock) or about art contemporaneous to her own writing (Robert Morris, Sol LeWitt, Richard Serra, Cindy Sherman), Krauss translates the ephemeralities of visual and bodily experience into precise, vivid English, which has solidified her prestige as a critic.\n\nSummary sentence:\nAs a critic and theorist she has published steadily since 1965 in \"Artforum\" and \"Art International\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2b7480bd39",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Diaz married musician Benji Madden at her home in Beverly Hills, California, on January 5, 2015, in a Jewish ceremony.\n- In December 2019, the couple welcomed a daughter via surrogate.\n\nSummary sentence:\nIn 2015, she married Good Charlotte guitarist Benji Madden; they have a daughter via surrogate in 2019.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2ab2b47155",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Marni Abbott-Peter\n- She first began swimming at the Pan American Games, where she won five medals, but soon began playing wheelchair basketball in 1988 and made the Canadian national team in 1992.\n\nSummary sentence:\nMarni Abbott-Peter is a Canadian wheelchair basketball player.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 }
]
