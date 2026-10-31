# A46 replay label-noise blind read RSBS10-blind_read-93a61eb1-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS10-blind_read-93a61eb1-003.json

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
  "qid": "q8a7fcea4be",
  "kind": "yes/no",
  "text": "Claim: Boom Boom captained the lacrosse team, Peshawar Zalmi, in 2016.\n\nPassages:\n\n[Peshawar Zalmi in 2016]\nThe Peshawar Zalmi is a franchise cricket team that represents Peshawar in the Pakistan Super League. The team was captained by Shahid Afridi, and they stand on first position after winning six matches from their eight matches in the PSL 2016.\n\n[Shahid Afridi]\nSahibzada Mohammad Shahid Khan Afridi (Urdu: ‎ ; Pashto: شاهد اپریدی‎ ; born 1980), popularly as Shahid \"Boom Boom\" Afridi, is a former Pakistani cricketer and former captain of the Pakistan national cricket team.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf1f2e37c5a",
  "kind": "yes/no",
  "text": "Claim: Between this flowering plant and Darwinia, the genus with more species is Darwinia. This plant is called Saule in French.\n\nPassages:\n\n[Willow]\nWillows, also called sallows, and osiers, form the genus Salix, around 400 species of deciduous trees and shrubs, found primarily on moist soils in cold and temperate regions of the Northern Hemisphere.\n\n[Darwinia (plant)]\nDarwinia, sometimes commonly known as mountain bells or simply bells, is a genus of about 70 species of evergreen shrubs in the family Myrtaceae, endemic to southeastern and southwestern Australia.\n\n[Saule]\nSaule is the French equivalent for the Willow",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9be3bbbfe4",
  "kind": "yes/no",
  "text": "Claim: The composer William Turner Walton was born later than the creator of Parisina.\n\nPassages:\n\n[Parisina (opera)]\nParisina (also known as Parisina d'Este) is an opera (\"tragedia lirica\"), in three acts by Gaetano Donizetti.\n\n[Gaetano Donizetti]\nDomenico Gaetano Maria Donizetti (] ; 29 November 1797 – 8 April 1848) was an Italian composer.\n\n[William Walton]\nSir William Turner Walton, OM (29 March 19028 March 1983) was an English composer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1b58a06274",
  "kind": "yes/no",
  "text": "Claim: The choreographer of La Vivandiere or Markitenka was the \"Maître de Ballet\" of the ballet company now known as The Mariinsky Ballet\n\nPassages:\n\n[La Vivandière or Markitenka]\nLa Vivandière (or Markitenka, as it is known in Russia) is a ballet in one act with choreography by Arthur Saint-Léon and Fanny Cerrito, and music by Cesare Pugni.\n\n[Mariinsky Ballet]\nThe Mariinsky Ballet is the resident classical ballet company of the Mariinsky Theatre in Saint Petersburg, Russia. Founded in the 18th century and originally known as the Imperial Russian Ballet, the Mariinsky Ballet is one of the world's leading ballet companies. The Mariinsky Ballet is the parent company of the \"Vaganova Ballet Academy\", a leading international ballet school.\n\n[Arthur Saint-Léon]\nArthur Saint-Léon (17 September 1821, Paris – 2 September 1870) was the \"Maître de Ballet\" of St. Petersburg Imperial Ballet from 1859 until 1869 and is famous for creating the choreography of the ballet \"Coppélia\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q189c027a04",
  "kind": "yes/no",
  "text": "Claim: Dennis Potter wrote the TV serial in which Rosemary Martin played Marjorie.\n\nPassages:\n\n[Pennies from Heaven (TV series)]\nPennies From Heaven is a 1978 BBC musical drama serial written by Dennis Potter.\n\n[Rosemary Martin]\n\", Marjorie in \"Pennies from Heaven\", Miss Weber in \"The Insurance Man\", Renie Fox in \"Fox\" and Verna Johnson in \"Tenko\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0b5d38d909",
  "kind": "yes/no",
  "text": "Claim: Icknield Walk First School is located in Hartforshire county.\n\nPassages:\n\n[Royston, Hertfordshire]\nRoyston is a town and civil parish in the District of North Hertfordshire and county of Hertfordshire in England.\n\n[Icknield Walk First School]\nIcknield Walk First School is a larger than average first school located in Royston, Hertfordshire, England.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa1288a5683",
  "kind": "yes/no",
  "text": "Claim: Mark Brooks won the PGA Championship to be held at Vahalla, which was also the site of the 2014 PGA Championship.\n\nPassages:\n\n[2014 PGA Championship]\nThis was the third PGA Championship at Valhalla, which previously hosted in 1996 and 2000, both won in playoffs, as well as the Ryder Cup in 2008, the most recent U.S. victory.\n\n[2000 PGA Championship]\nThe 2000 PGA Championship was the 82nd PGA Championship, held August 17–20 at the Valhalla Golf Club in Louisville, Kentucky. Tiger Woods won his second straight PGA Championship and fifth major in a three-hole playoff over Bob May.\n\n[1996 PGA Championship]\nThe 1996 PGA Championship was the 78th PGA Championship, held August 8–11 at Valhalla Golf Club in Louisville, Kentucky. Mark Brooks won his only major championship with a birdie at the first hole of a sudden-death playoff with Kentucky native Kenny Perry.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0e7a96a9a5",
  "kind": "yes/no",
  "text": "Tweet: 4-0 this morning, 0-1 this afternoon. Luck possibly changing.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe92883d169",
  "kind": "yes/no",
  "text": "Claim: The 1961 British comedy film directed by Edward Buzzell took its title from an English language nursery rhyme of nineteenth-century American origin called Mary Had a Little.\n\nPassages:\n\n[Mary Had a Little Lamb]\n\"Mary Had a Little Lamb\" is an English language nursery rhyme of nineteenth-century American origin.\n\n[Mary Had a Little...]\nMary Had a Little… is a 1961 British comedy film directed by Edward Buzzell and starring Agnès Laurent, Hazel Court and Jack Watling. It takes its title from the nursery rhyme \"Mary Had a Little Lamb\" and is about a slick impresario who tries unsuccessfully to win a bet with a psychiatrist over the production of a perfect baby via hypnotism.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q532ae8fcf3",
  "kind": "yes/no",
  "text": "Claim: The American media company that produced The Hobbit: The Desolation of Smaug in collaboration with Boston company WingNut Films and New Line Cinema is Metro-Goldwyn-Mayer Studios Inc.\n\nPassages:\n\n[Metro-Goldwyn-Mayer]\nMetro-Goldwyn-Mayer Studios Inc. (abbreviated as MGM or M-G-M, also known as Metro-Goldwyn-Mayer Pictures, Metro-Goldwyn-Mayer or simply Metro, and for a former interval known as Metro-Goldwyn-Mayer/United Artists, or MGM/UA) is an American media company, involved primarily in the production and distribution of feature films and television programs.\n\n[The Hobbit: The Desolation of Smaug]\nThe Hobbit: The Desolation of Smaug is a 2013 epic high fantasy adventure film directed by Peter Jackson and produced by WingNut Films in collaboration with New Line Cinema and Metro-Goldwyn-Mayer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf883187313",
  "kind": "yes/no",
  "text": "Claim: Thomas Harold Massie is an American engineer and conservative politician who has been the United States Representative for Kentucky's 4th congressional district that defeated the 63rd District, representative of Kenton County.\n\nPassages:\n\n[Thomas Massie]\nThomas Harold Massie (born January 13, 1971) is an American engineer and politician who has been the United States Representative for Kentucky's 4th congressional district since 2012.\n\n[Alecia Webb-Edgington]\nShe represented the 63rd District, which comprised part of Kenton County.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb849cda39c",
  "kind": "yes/no",
  "text": "Claim: When the Macanese general election took place on the night of, September 17, 2017, the legislature was elected according to the provisions of the Basic Law of Macau.\n\nPassages:\n\n[Elections in Macau]\nMacau elects on national level a legislature.\n\n[Macanese legislative election, 2017]\nThe 2017 Macanese general election took place on 17 September 2017 according to the provisions of the Basic Law of Macau.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3a7680a59b",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "Stranger Things is pretty good but season 1 is better than season 2",
   "Yeah I’m following a lot of shows right now, the price is right is pretty good but season 1 is better than season 2"
  ]
 },
 {
  "qid": "q2fe8fd744f",
  "kind": "yes/no",
  "text": "Claim: Dock Walloper is a comic series produced by Virgin Comicss. Neither the director of the 1943 film \"Young and Willing\" nor the comic book's creator are from IRAN.\n\nPassages:\n\n[Dock Walloper]\nDock Walloper is a current comic book series from film star Edward Burns and Virgin Comics.\n\n[Edward H. Griffith]\nEdward H. Griffith (August 23, 1888 – March 3, 1975) (\"Also Known As: E H Griffith, Lieut. Edward H. Griffith, Edward Griffith, E. H. Griffith\") was an American motion picture director, screenwriter, and producer.\n\n[Young and Willing]\nYoung and Willing is a 1943 American comedy film produced and directed by Edward H. Griffith and starring William Holden, Eddie Bracken, Robert Benchley, and Susan Hayward.\n\n[Edward Burns]\nEdward Fitzgerald Burns (born January 29, 1968) is an American actor, film producer, writer, and director best known for appearing in several films including \"Saving Private Ryan\" (1998), \"15 Minutes\" (2001), \"Life or Something Like It\" (2002), \"A Sound of Thunder\" (2005), \"The Holiday\" (2006), \"One Missed Call\" (2008), \"27 Dresses\" (2008), \"Man on a Ledge\" (2012), \"Friends with Kids\" (2012), and \"Alex Cross\" (2012).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qfca9caba08",
  "kind": "yes/no",
  "text": "Claim: Erik Marcisak was named one of Top Ten \"Comedy Best Bets\" by a brand with special focus on casting, job opportunities, and career advice.\n\nPassages:\n\n[Erik Marcisak]\nErik Marcisak was named one of \"Backstage\"'s Top Ten \"Comedy Best Bets\" in 2005 for producing the controversial sketch comedy show \"Saturday Night Rewritten\", which used the previous night's \"Saturday Night Live\" as a creative jumping-off point for an entirely new sketch show that was written, rehearsed, and performed within 8 hours the next day.\n\n[Backstage (magazine)]\nBackstage (aka Back Stage) is an entertainment-industry brand aimed at people working in film and the performing arts, with a special focus on casting, job opportunities, and career advice.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q74a7c61eac",
  "kind": "yes/no",
  "text": "Claim: The Afghani city of Jalālābād is called جلال اباد‎ ‎ in the main language among a diaspora. The diaspora has it's largest community in the country that Kotli Loharan East is in.\n\nPassages:\n\n[Kotli Loharan East]\nKotli Loharan East is a town in the Punjab province of Pakistan.\n\n[Jalalabad]\nJalālābād (Pashto/Persian: جلال اباد‎ ‎ ), formerly called Ādīnapūr (Pashto: آدينه پور‎ ) as documented by the 7th century Hsüan-tsang, is a city in eastern Afghanistan.\n\n[Pashtun diaspora]\nPakistan is home to the largest Pashtun community.\n\n[Pashto]\nPashto is the main language among the Pashtun diaspora around the world.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9962d31504",
  "kind": "yes/no",
  "text": "Claim: Titus is the soundtrack to the horror film that starred actors, Anthony Hopkins and Jessica Lange.\n\nPassages:\n\n[Titus (film)]\nStarring Anthony Hopkins and Jessica Lange, it was the first theatrically-released feature film adaptation of the play.\n\n[Titus (soundtrack)]\nTitus is the original soundtrack to the 1999 motion picture \"Titus\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q41cee22565",
  "kind": "yes/no",
  "text": "Claim: The Baudot code is represented on the cover art of the studio album that includes the song \"Speed of Sound\".\n\nPassages:\n\n[Speed of Sound (song)]\nIt was written by all members of the band for their third studio album, \"X&Y\" (2005).\n\n[X&amp;Y]\nThe album's cover art is a combination of colours and blocks, which is a representation of the Baudot code.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q16b65e9b6b",
  "kind": "yes/no",
  "text": "Claim: System of a Down and Richard Donchian are both Armenian-American.\n\nPassages:\n\n[System of a Down]\nSystem of a Down, sometimes shortened to System and abbreviated as SOAD, is an Armenian-American heavy metal band from Glendale, California, formed in 1994.\n\n[Richard Donchian]\nRichard Davoud Donchian (born September 1905, Hartford, Connecticut – d. 1993) was an Armenian-American commodities and futures trader, and pioneer in the field of managed futures.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q466c3ed70c",
  "kind": "yes/no",
  "text": "Post: I. Am. So. Tired. And impatient. And cranky. SOS. https://t.co/f7UPtIybWV",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q47270fb4b0",
  "kind": "yes/no",
  "text": "Claim: Night Monster is a 1942 American black-and-white horror film featuring Bela Lugosi, he was a Hungarian-American actor, famous for portraying Count Melissa Stribling in the film from the year 1931.\n\nPassages:\n\n[Night Monster]\nNight Monster is a 1942 American black-and-white horror film featuring Bela Lugosi and produced and distributed by Universal Pictures Company.\n\n[Bela Lugosi]\nBéla Ferenc Dezső Blaskó (] ; 20 October 1882 – 16 August 1956), better known as Bela Lugosi ( ; ] ), was a Hungarian-American actor, famous for portraying Count Dracula in the 1931 film and for his roles in various other horror films.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc2213cde9e",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I download this app again, but realistically I know it won't work.",
   "Just redownloaded the @achievement app - let's see if it improves my exercise routine!"
  ]
 },
 {
  "qid": "q1c3d3fb5fc",
  "kind": "yes/no",
  "text": "Claim: The award winning producer of the album Republic? also produces a band with the guitarist Gorden Mack. He did not produce the band Daughtry.\n\nPassages:\n\n[Red House Painters]\nRed House Painters were an American rock band, formed in San Francisco, California in 1988. Guitarists Gorden Mack and Phil Carney both performed with the band during separate six-year tenures.\n\n[Daughtry (band)]\nDaughtry is an American rock band formed and fronted by namesake Chris Daughtry, who was a finalist on the fifth season of \"American Idol\".\n\n[Billy Anderson (producer)]\nHe has worked with hundreds of bands over the past 29 years, including Neurosis, Swans, Melvins, Jawbreaker, Sleep, Brutal Truth, Buzzoven, Fantômas, Agalloch, Cattle Decapitation, Mr. Bungle, Asunder and Red House Painters.\n\n[Republic? (album)]\nIt was produced by Billy Anderson.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfd8a5e9feb",
  "kind": "yes/no",
  "text": "Post: I do love it when my mum makes me spend my savings on beer 😒",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q6ab4111c7d",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "I am starting off my day by watching a Dragons Den special on Deborah Meaden and eating a Pot Noodle. My life is a sham. Send help.",
   "I am starting off my day by watching a Dragons Den special on Deborah Meaden and eating a Pot Noodle. My life is perfect."
  ]
 },
 {
  "qid": "q53ce1f32d3",
  "kind": "yes/no",
  "text": "Claim: Pyne & Marles is co-hosted by Richard Marles and an Australian politician who has been the Labor member for the House of Representatives seat of Sturt since the election of 1993.\n\nPassages:\n\n[Pyne &amp; Marles]\nThe program is co-hosted by two serving frontbench MPs; Liberal minister Christopher Pyne and Labor shadow minister Richard Marles, without a journalist or moderator.\n\n[Christopher Pyne]\nChristopher Maurice Pyne (born 13 August 1967) is an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the 1993 election.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0262db3192",
  "kind": "yes/no",
  "text": "Claim: The film, with \"Fortuosity\" as the first song, was created before another film. The other film was created by the independent studio ImageMovers.\n\nPassages:\n\n[Fortuosity]\n\"Fortuosity\" is the first song in the 1967 motion picture The Happiest Millionaire.\n\n[Mars Needs Moms]\nMars Needs Moms is a 2011 American computer-animated film based on the Berkeley Breathed book of the same title.\n\n[The Happiest Millionaire]\nThe Happiest Millionaire is a 1967 musical film starring Fred MacMurray and based upon the true story of Philadelphia millionaire Anthony J. Drexel Biddle.\n\n[ImageMovers]\nFrom 2007 to 2010, The Walt Disney Company and ImageMovers ran a joint animation facility, ImageMovers Digital, which produced two performance captured animated films, \"A Christmas Carol\" and \"Mars Needs Moms\", for The Walt Disney Studios.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9ae48c35ba",
  "kind": "yes/no",
  "text": "Claim: Physician Johannes Lijdius Catharinus Pompe van Meerdervoort was originally from the country that was known as The United Kingdom of the Netherlands between 1815 and 1830.\n\nPassages:\n\n[United Kingdom of the Netherlands]\nThe United Kingdom of the Netherlands (Dutch: \"Verenigd Koninkrijk der Nederlanden\" , French: \"Royaume uni des Pays-Bas\" ) is the unofficial name given to the Kingdom of the Netherlands as it existed between 1815 and 1830.\n\n[J. L. C. Pompe van Meerdervoort]\nJohannes Lijdius Catharinus Pompe van Meerdervoort (5 May 1829, Bruges – 7 October 1908, Brussels) was a Dutch physician based at Nagasaki, in Bakumatsu period Japan.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4da817e89c",
  "kind": "yes/no",
  "text": "Claim: The name of the 40th president who was in office when the Job Partnership Act of 1982 was passed is Ronald Reagan.\n\nPassages:\n\n[Job Training Partnership Act of 1982]\nThe Job Training Partnership Act of 1982 (Pub.L. 97–300 , , et seq.) was a United States federal law passed October 13, 1982, by the United States Department of Labor during the Ronald Reagan administration.\n\n[Ronald Reagan]\nRonald Wilson Reagan ( ; February 6, 1911 – June 5, 2004) was an American statesman and actor who served as the 40th President of the United States from 1981 to 1989.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe07c218392",
  "kind": "yes/no",
  "text": "Claim: Riviera Partners' clientele Zappos is located in Las Vegas, Nevada and was incorporated in 1985.\n\nPassages:\n\n[Riviera Partners]\nRiviera Partners' clientele includes, among others, ServiceNow, Xoom, One Kings Lane, Uber, Path, Okta, Pure Storage, Twitter, LinkedIn, Dropbox, Pinterest, and Zappos.\n\n[Zappos]\nZappos.com is an online shoe and clothing shop based in Las Vegas, Nevada.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf423932cb2",
  "kind": "yes/no",
  "text": "Post: Is spunk a slur?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q4b22b5b604",
  "kind": "yes/no",
  "text": "Tweet: Absolutely LOVE spider season! I love crying in fear. I love not being able to sleep. I love people telling me that I'm being ridiculous. I love hearing \"it's not gonna hurt ye\". I love using every orange peel, conker and peppermint oil known to man. I love fear. 😑",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q6cf1ec5e55",
  "kind": "yes/no",
  "text": "Text: the one time I need my phone charger and I. have brought the charging battery bank but forgoTTEN THE CORD I am dumb",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q3ca40808f6",
  "kind": "yes/no",
  "text": "Claim: Horror Stories 2 is a 2013 horror omnibus film made up of four episodes by four South Korean directors, that had an award-winning actor known for his leading roles in the television series \"Shut Up Flower Boy Band\".\n\nPassages:\n\n[Sung Joon]\nHe began his entertainment career as a model, but after switching to acting he became best known for his leading roles in the television series \"Shut Up Flower Boy Band\" (2012), \"Can We Get Married?\n\n[Horror Stories 2]\nHorror Stories 2 () is a 2013 horror omnibus film made up of four episodes by four South Korean directors.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qed2827bc36",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "The Red Sox probably wish they could play the Orioles all season.",
   "If I were the Red Sox I would simply play the Orioles more"
  ]
 },
 {
  "qid": "q04a7c8e950",
  "kind": "yes/no",
  "text": "Text: @rits_meg @freedomsenpai hot loli",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q282ce300ec",
  "kind": "yes/no",
  "text": "Claim: The writer of the song I Was Here is also a producer. He won his fourth Grammy for the song by a singer from the album Loud. Destinee & Paris cited the singer as an influence.\n\nPassages:\n\n[Destinee &amp; Paris]\nBorn and raised in New Jersey, now Los Angeles-based, the sisters cite their influences as Britney Spears, Michael Jackson, Christina Aguilera, Beyoncé, Katy Perry, Rihanna, and Gwen Stefani.\n\n[Kuk Harrell]\nEarning his fourth Grammy for the vocal production of Rihanna's No. 1 Billboard Single \"Only Girl (In the World)\", Harrell is also the vocal producer and co-writer of Rihanna's Grammy-winning single \"Umbrella\".\n\n[Only Girl (In the World)]\n\"Only Girl (In the World)\" is a song by Barbadian singer Rihanna from her fifth album, \"Loud\" (2010).\n\n[I Was Here (song)]\nIt was written by Diane Warren, while production was handled by Ryan Tedder, Brent Kutzle, and Kuk Harrell; Beyoncé is credited on the vocal production.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0dd297973c",
  "kind": "yes/no",
  "text": "Claim: Deborah Miller is the former Secretary of Transportation at the state government organization in charge of maintaining public roadways of the Missouri state of Kansas.\n\nPassages:\n\n[Deb Miller]\nDeborah Miller is a former Secretary of Transportation at the Kansas Department of Transportation (KDOT) who served from 2003 to 2012.\n\n[Kansas Department of Transportation]\nThe Kansas Department of Transportation (KDOT) is a state government organization in charge of maintaining public roadways of the U.S. state of Kansas.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8228ad94fe",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Football and RuPual's Drag Race are wildly different shows.",
   "Andrews really trying to explain to me that football and rupauls drag race aren’t the same thing when it in fact is the same thing."
  ]
 },
 {
  "qid": "q9916163d95",
  "kind": "yes/no",
  "text": "Claim: In this religion, where Mehet-Weret is a godess of the sky, a citizen would be weighted against the feather of truth to decide if they where worthy of damnation and would face the torment in the lake of fire.\n\nPassages:\n\n[Damnation]\nIn Ancient Egyptian religious tradition, citizens would recite the 42 negative confessions of Maat as their heart was weighed against the feather of truth.\n\n[Mehet-Weret]\nMehet-Weret \"(mḥ.t-wr.t)\" is a goddess of the sky in Ancient Egyptian religion. Her name means \"Great Flood\".\n\n[Ancient Egyptian religion]\nAncient Egyptian religion was a complex system of polytheistic beliefs and rituals which were an integral part of ancient Egyptian society.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q539eacbca5",
  "kind": "yes/no",
  "text": "Claim: Walt Disney Pictures produced both the film that National Treasure: Book of Secrets is a sequel to and 1999 film The Computer Wore Tennis Shoes.\n\nPassages:\n\n[The Computer Wore Tennis Shoes]\nIt was produced by Walt Disney Productions and distributed by Buena Vista Distribution Company as part of \"The Last Laughs of the 1960s\".\n\n[National Treasure (film)]\nNational Treasure is a 2004 American adventure heist film produced and released by Walt Disney Pictures.\n\n[National Treasure: Book of Secrets]\nIt is a sequel to the 2004 film \"National Treasure\" and is the second part of the \"National Treasure\" franchise.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2f04363b2e",
  "kind": "yes/no",
  "text": "Text: i just overheard this bunch of children behind me yell “DON’T LOOK AT THE ENDERMAN”……internally yelling as an mcyt mod",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q02ec61fc77",
  "kind": "yes/no",
  "text": "Claim: Brian Hugh Warner performed on MTV Europe Music Awards in 1999.\n\nPassages:\n\n[Marilyn Manson]\nBrian Hugh Warner (born January 5, 1969), known professionally as Marilyn Manson, is an American singer, songwriter, musician, composer, actor, painter, author and former music journalist.\n\n[1999 MTV Europe Music Awards]\nThe 1999 MTV Europe Music Awards were held in Dublin, Ireland at The Point. Ronan Keating returned as host, with performers including Mariah Carey singing \"Heartbreaker\", Britney Spears with \"...Baby One More Time\" & \"(You Drive Me) Crazy\", as well as The Cardigans, Jamiroquai, Marilyn Manson and The Corrs and show opener Iggy Pop.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfd5379b51f",
  "kind": "yes/no",
  "text": "Claim: Hillary Rodham Clinton was a politician from New York who served two terms representing New York in the United States Senate until her death in 1861.\n\nPassages:\n\n[United States Senate career of Hillary Clinton]\nShe won the United States Senate election in New York, 2000 and the United States Senate election in New York, 2006.\n\n[United States Senate election in New York, 2006]\nIncumbent Democratic U.S. Senator Hillary Rodham Clinton won, by a more than two-to-one margin, a second term representing New York in the United States Senate.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q62db324d08",
  "kind": "yes/no",
  "text": "Claim: This event is known as the Revolution of 1688 and caused the noble in Scotland to lose control over St Andrew parish churches. The Wincanton Skirmish occurred during this event.\n\nPassages:\n\n[Glorious Revolution]\nThe Glorious Revolution, also called the Revolution of 1688, was the overthrow of King James II of England (James VII of Scotland) by a union of English Parliamentarians with the Dutch stadtholder William III, Prince of Orange.\n\n[Wincanton Skirmish]\nThe Wincanton Skirmish occurred on 20 November 1688 during the Glorious Revolution.\n\n[Church Patronage (Scotland) Act 1711]\nIts purpose was to allow the noble and other Patrons in Scotland to gain control over the Church of Scotland parish churches again, having lost that custom in the so-called Glorious Revolution.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfb9c058171",
  "kind": "yes/no",
  "text": "Claim: The airline that was affected by the 1931 Avro Ten Southern Cloud disappearance was founded by the person who made the first trans-Pacific flight in 1928.\n\nPassages:\n\n[Australian National Airways (1930)]\nAustralian National Airways was a short-lived Australian airline, founded in 1929 by Charles Kingsford Smith and Charles Ulm.\n\n[1931 Avro Ten Southern Cloud disappearance]\nThe Southern Cloud, registered VH-UMF, was one of five Avro 618 Ten three-engined aircraft flying daily airline services between several Australian cities for Australian National Airways in the early 1930s.\n\n[Charles Kingsford Smith]\nIn 1928, he earned global fame when he made the first trans-Pacific flight from the United States to Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q44417520ed",
  "kind": "yes/no",
  "text": "Claim: Richard Connell's best known work The Hounds of Zaroff was also published as the story that Bloodlust! is based on.\n\nPassages:\n\n[Seven Faces]\nBased upon the piece of short fiction \"A Friend of Napoleon\" which was published in the June 30, 1923, issue of \"The Saturday Evening Post\" magazine by popular writer Richard Connell (whose best known work, \"The Most Dangerous Game\", was filmed three years later), it was directed by Berthold Viertel and stars Paul Muni in his second screen appearance.\n\n[The Most Dangerous Game]\n\"The Most Dangerous Game\", also published as \"The Hounds of Zaroff\", is a short story by Richard Connell, first published in \"Collier's\" on January 19, 1924.\n\n[Bloodlust!]\nis a 1961 American horror thriller film based on Robert Connell's short story \"The Most Dangerous Game.\"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6fd06f90c4",
  "kind": "yes/no",
  "text": "Claim: Aladdin's Problem is a 1983 novella by a highly decorated German soldier who became famous for the 1972 World War I memoir, Storm of Steel.\n\nPassages:\n\n[Aladdin's Problem]\nAladdin's Problem (German: Aladins Problem ) is a 1983 novella by the German writer Ernst Jünger.\n\n[Ernst Jünger]\nErnst Jünger (29 March 1895 – 17 February 1998) was a highly decorated German soldier, author, and entomologist who became famous for his World War I memoir \"Storm of Steel\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q58da407c55",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "not to alarm anyone but i just saw spider-man by uta",
   "ALERT, spider-man is on the uta campus."
  ]
 },
 {
  "qid": "q3f73c32a52",
  "kind": "yes/no",
  "text": "Claim: Lowell Edwin Jones teaches mathematics at a school. That school is further North than where Bonnie Newman was the interim president of.\n\nPassages:\n\n[Bonnie Newman]\nNewman was also interim president of the University of New Hampshire (UNH) and the Community College System of New Hampshire.\n\n[Lowell Edwin Jones]\nLowell Jones (born 1945) is an American professor of mathematics at Stony Brook University Jones' primary fields of interest are topology, and geometry.\n\n[University of New Hampshire]\nThe University of New Hampshire (UNH) is a public research university in the University System of New Hampshire, in the United States.\n\n[Stony Brook University]\nThe State University of New York at Stony Brook (also known as Stony Brook University or SUNY Stony Brook) is a public sea-grant and space-grant research university located in Stony Brook, New York in the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
