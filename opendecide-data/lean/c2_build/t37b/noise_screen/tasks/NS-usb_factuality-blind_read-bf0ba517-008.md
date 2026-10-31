# Replay noise screen blind read NS-usb_factuality-blind_read-bf0ba517-008 (family NS-usb_factuality)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-usb_factuality-blind_read-bf0ba517-008.json

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
  "qid": "qa13b9edc52",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- By the time of his retirement, Neville had won eight Premier League titles, three FA Cups, two Champions Leagues, an Intercontinental Cup, a FIFA Club World Cup, and two League Cups.\n\nSummary sentence:\nHe is one of the most decorated English and European footballers of all time, having won a total of 20 trophies, including eight Premier League titles and two Champions League titles.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q94d7dd3f1c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Peter Weir\n- Following a period as an Independent Unionist, Weir joined the Democratic Unionist Party (DUP) in 2002.\n- Since then, he has been re-elected to the Northern Ireland Assembly in North Down at each election for the DUP.\n\nSummary sentence:\nWeir is a Democratic Unionist Party (DUP) politician.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qda3a50cc7b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Karen Vogtmann\n- She is currently a professor of mathematics at Warwick, and a Goldwin Smith Professor of Mathematics Emeritus at Cornell.\n- Vogtmann was selected to deliver the Noether Lecture for \"her fundamental contributions to geometric group theory; in particular, to the study of the automorphism group of a free group\".\n\nSummary sentence:\nKaren Vogtmann is a mathematician working in the area of geometric group theory.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q8755017f00",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He then moved to spend almost two years as Parliamentary Under-Secretary of State in the Department for Constitutional Affairs, working again under Falconer from 2003 to 2005.\n- In the 2005 general election, Leslie lost his seat to Conservative candidate Philip Davies, by fewer than 500 votes.\n\nSummary sentence:\nLeslie was a minister in the Department for Constitutional Affairs from 2001 to 2005 but lost his seat at the 2005 general election.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb2f3b9a114",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- As Director, he was one of the first people in Britain to whom the term \"spin doctor\" was applied; he was thus called \"the Prince of Darkness\".\n\nSummary sentence:\nHe was one of the first to whom the term 'spin doctor' was applied and gained the nickname 'the Prince of Darkness' because of his 'ruthlessness' and 'media savvy'.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q64238e97c6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2003 and 2004, she had a recurring role on \"Will & Grace\" as Lorraine Finster, the nemesis of Karen Walker (Megan Mullally) and daughter of Karen's lover, Lyle Finster (John Cleese).\n- Driver landed the lead role in the ABC sitcom \"Speechless\", playing the mother of three children, one of whom has cerebral palsy and uses a wheelchair.\n\nSummary sentence:\nShe has starred in the ABC sitcom \"Speechless\" and in a recurring role on \"Will & Grace\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf6ebbd7b41",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Anwar Saifullah Khan\n- He took the post of co-chairman of Saif Group, a Pakistani conglomerate, in 1984.\n- Anwar Saifullah Khan was elected to the Senate from Khyber Pakhtunkhwa in 1990, serving until 1997 as a member of the Pakistan Muslim League (Junejo).\n\nSummary sentence:\nAnwar Saifullah Khan (; born 7 June 1945) is a Pakistani politician and industrialist.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qe5bf9e49d2",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Having previously contested Southend West in the 1987 General Election, Smith was selected to stand for election for Labour in Basildon nearly a decade later in December 1995 through an all-women shortlist.\n- She was elected for Basildon at the 1997 general election, replacing the Conservative MP David Amess, who had moved to contest the nearby safer seat of Southend West, which Smith previously fought herself, when Basildon's boundaries were slightly redrawn, aware that his small majority was almost certainly going to be overturned by Labour.\n- She was re-elected comfortably in 2001 and 2005.\n- In 2006, she was moved to the Department for Communities and Local Government, with responsibility for Fire Services.\n- On 28 June 2007, Smith was appointed as a Parliamentary Private Secretary to the new Prime Minister Gordon Brown, entitling her to attend Cabinet.\n- The old Basildon seat was abolished in the 2010 general election, and she stood for and lost the contest to the new South Basildon and East Thurrock constituency, which predominantly covered much of the area she represented in Parliament, to the Conservative candidate Stephen Metcalfe.\n\nSummary sentence:\nA member of Labour, she was Member of Parliament (MP) for Basildon from 1997 to 2010.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q3a68bad771",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dodon was appointed to the post of Associate Minister of Trade and Economics in May 2005, during the second Tarlev Cabinet.\n- He assumed the position of Minister of Trade and Economics in September 2006.\n- He held the position until September 2009, when the government of Zinaida Greceanîi ended.\n- In September 2009, after 8 years of governing, the Communist Party came into opposition.\n- He became an MP in the Parliament, which was reelected in November 2010.\n- After he was elected as the president of Moldova, due to specifics of Moldovan law, Dodon resigned as PSRM chairman and left the party, being replaced by Zinaida Greceanîi as interim leader.\n- Dodon was sworn in on 23 December 2016 in the Palace of the Republic.\n\nSummary sentence:\nHe served as minister of trade and economics in the governments of Vasile Tarlev and Zinaida Greceanîi from September 2006 to September 2009 and was a member of the Parliament of Moldova from 2009 to 2016.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qe234b84ba9",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2000, after the end of \"Seinfeld\", Richards began work on a new series for NBC, his first major project since \"Seinfeld\"s finale.\n- \"The Michael Richards Show\", for which Richards received co-writer and co-executive producer credits, was conceived as a comedy/mystery starring Richards as a bumbling private investigator.\n- When the first pilot failed with test audiences, NBC ordered that the show be retooled into a more conventional, office-based sitcom before its premiere.\n- After a few weeks of poor ratings and negative reviews, it was cancelled.\n\nSummary sentence:\nAfter \"Seinfeld\", he starred in his own sitcom, \"The Michael Richards Show\", which was cancelled after 2 months.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q902215e671",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Since November 2021, Singh has been portraying the role of Suhani, on Colors TV's romantic drama \"Sirf Tum\".\n\nSummary sentence:\nCurrently, she is seen as Suhani in \"Sirf Tum\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qad215b971e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He has guest starred on such shows as \"Seinfeld\", \"Wings\", \"Dharma & Greg\", \"According to Jim\", \"Curb Your Enthusiasm\", \"The X Files\", \"Suddenly Susan\", \"ER\", \"Ellen\", \"3rd Rock from the Sun\", \"The Nanny\", and \"Desperate Housewives\".\n- Bagley has also had regular and recurring roles in such hit shows as \"The King of Queens\", \"Hope & Gloria\", \"Strip Mall\", and \"7th Heaven\", and portrayed fellow OCD sufferer Harold Krenshaw on \"Monk\" for several episodes, often antagonizing the titular character, Adrian Monk and his assistants, Sharona Fleming and Natalie Teeger.\n- He is perhaps best known on television for his appearances as Larry, one half of a married gay couple with an adopted daughter, on the hit sitcom \"Will & Grace\".\n- Bagley also starred with Lisa Kudrow and Victor Garber on \"Web Therapy\", the series of online vignettes developed by Kudrow which was adapted into a half-hour show by Showtime.\n\nSummary sentence:\nHe had recurring roles on the TV series \"Will & Grace\", \"Hope & Gloria\", \"Strip Mall\", \"According to Jim\", \"The King of Queens\", \"Monk\", \"Help Me Help You\", \"10 Items or Less\", \"$#*! My Dad Says\", and portrayed Richard Pratt on the Showtime series, \"Web Therapy\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7a48f62fc3",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1994 he directed the critically acclaimed \"Bandit Queen\" and played a cameo in the film as a truck driver.\n- In 1998, he received international recognition for the second time after \"Bandit Queen\", when he directed the Academy Award-winning period film \"Elizabeth\", a fictional account of the reign of British Queen Elizabeth I nominated for seven Oscars.\n\nSummary sentence:\nHe then gained international recognition and acclaim in 1994 with \"Bandit Queen\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qffb3d405c3",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Kyaw Zeya\n- In the 2015 Myanmar general election, he contesting for Yangon Region Hluttaw from Dagon Township No. 2 parliamentary constituency, won a seat.\n- Kyaw Zeya serves as a member of the Yangon Region Parliament's Finance, Planning and Economic Committee.\n\nSummary sentence:\nKyaw Zeya (, also spelt Kyaw Zayya; born 25 January 1956) is a Burmese politician and a retired lieutenant colonel in the armed forces who was served as a Member of Parliament in the Yangon Region Hluttaw for Dagon Township No. 2 constituency.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q0c0a112626",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- One historian described them as \"the military arm of the Democratic Party.\"\n\nSummary sentence:\nThey were described as \"the military arm of the Democratic Party.\"",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qad9c409f6b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Adam Patrick Devine\n- Devine was born in Waterloo, Iowa, the son of Dennis and Penny Devine.\n- He later moved to Los Angeles, where he began working as a stand-up comedian and actor.\n\nSummary sentence:\nAdam Patrick Devine is an American actor and comedian.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q8047672501",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- They valued his personal worth at US$12 billion.\n\nSummary sentence:\nHis net worth was assessed at US$12 billion.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q1f283a8811",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In September 2016, following the dismissal and disciplinary investigation into Huang Xingguo, Wang was named mayor of Tianjin.\n\nSummary sentence:\nHe was formerly the Mayor of Tianjin.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q25ffbf3724",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In addition to serving as a judge on \"Top Chef\", Young has competed in the Channel 4 TV series \"Come Dine with Me\", appeared as one of the panel of food critics in the 2008 BBC Two series \"Eating with the Enemy\" and served as a judge on \"Hell's Kitchen\".\n\nSummary sentence:\nHe also served as a judge in seasons five and six of the television show \"Top Chef\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q10e264db5d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Chávez is the father of Omar Chávez and former WBC Middleweight Champion Julio César Chávez, Jr.\n\nSummary sentence:\nHe is the father of current boxers Omar Chávez and former WBC middleweight champion Julio César Chávez Jr.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q574babef16",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- William D. Casey\n- Casey was born in Amherst, Nova Scotia.\n- He was first elected, as a member of the Progressive Conservative Party of Canada, to represent the riding of Cumberland—Colchester in the 1988 election.\n- In common with almost every other PC Member of Parliament (MP) in the 1993 election he lost his seat, in his case being defeated by Liberal candidate Dianne Brushett.\n\nSummary sentence:\nWilliam D. Casey is a Canadian politician from Nova Scotia who served as a Member of Parliament (MP).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qe7b19ebdf5",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The album debuted at No. 2 on the country albums charts, Its fourth and fifth singles \"Real Good Man\" and \"Watch the Wind Blow By\" both climbed to number one on the U.S. \"Billboard\" Hot Country Songs chart.\n- \"Shotgun Rider\" became the album's third single and a number 1 Country Airplay hit by the end of 2014.\n\nSummary sentence:\nMany of his singles have reached number one on the Hot Country Songs or Country Airplay charts.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q130ed54812",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- 1973 Flores cyclone\n- The cyclone made landfall on the northern coast of the Indonesian island of Flores.\n- Across the region, the cyclone killed 1,653 people, making it the deadliest tropical cyclone recorded in the Southern Hemisphere.\n\nSummary sentence:\nThe 1973 Flores cyclone was the deadliest known tropical cyclone in the Southern Hemisphere, having killed 1,653 people in Indonesia in April 1973.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf632a735a4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2017, Rughani made her television debut with \"Jeet Gayi Toh Piya Morey\" opposite Krip Suri.\n- In 2020, she started starring as Zara in Sony SAB's fantasy series \"Hero Gayab Mode On\" opposite Abhishek Nigam.\n\nSummary sentence:\nRughani is known for portraying Devi/Devika in \"Jeet Gayi Toh Piya Morey\" and Zara in \"Hero – Gayab Mode On\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1887c53a5f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Garcia joined the advisory board of the revival of the United States Football League (USFL) in May 2012.\n\nSummary sentence:\nThe following year, Garcia joined the advisory board for the now defunct United States Football League.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qb1614e7fd9",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Balter began his journalism career writing for newspapers based in Los Angeles, including \"LA Weekly\", the \"Los Angeles Times\", and \"Los Angeles\" magazine.\n- He has also written for \"Scientific American\", \"Audubon,\" and \"The Verge.\"\n\nSummary sentence:\nHe has also written for \"Scientific American\", \"Audubon,\" \"The Verge\", \"LA Weekly\", the \"Los Angeles Times\", and \"Los Angeles\" magazine.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q17f3bd9075",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Golden Star Resources agreed to be acquired by the Chinese company Chifeng Jilong Gold Mining, a public company listed on the Shanghai Stock Exchange, in an all-cash deal amounting to US$470 million.\n\nSummary sentence:\nThe company was acquired by Shanghai Stock Exchange-listed Chifeng Jilong Gold Mining.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc78b741646",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2005, Wood started his own record label called Simian Records.\n\nSummary sentence:\nWood founded the record label Simian Records in 2005.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qa02e7a7610",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In the Chinese Basketball Association, he averaged 18.2 points, 6.3 rebounds and 3.4 assists throughout the regular season with tremendous improvements towards the end of the season.\n\nSummary sentence:\nHe last played for the Shanghai Dongfang Sharks of the Chinese Basketball Association.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2fd9552603",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After releasing the singles \"Music\" and \"Next to You\" in early 2003, in July of that year both tracks were included on Darude's second album, \"Rush\".\n- The album reached No. 11 on the \"Billboard\" Top Electronic Albums chart and No. 4 on weekly album chart in Finland, while \"Next to You\" charted at No. 1 on the Finnish singles chart.\n\nSummary sentence:\nDarude's second album, \"Rush\", reached number 11 on the \"Billboard\" Top Electronic Albums chart and number 4 on weekly album chart in Finland.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf64ef434a6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- With the Austrian victories at the Battle of Petrovaradin and the Siege of Belgrade, however, the Ottomans were forced to sign the Treaty of Passarowitz.\n\nSummary sentence:\nThe Austrian victories led to the signing of the Treaty of Passarowitz.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1986a43de6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2019, di Giovanni was named a Guggenheim Fellow.\n\nSummary sentence:\nShe was named a 2019 Guggenheim Fellow.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qe1b42b4066",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Finally, the commercial success of \"Switched-On Bach\" allowed Carlos to undergo sex reassignment surgery in May 1972, although for marketing reasons she released two more albums as Walter Carlos (1973's \"Switched-On Bach II\" and 1975's \"By Request\".)\n- Carlos disclosed her transgender status in a series of interviews with Arthur Bell held between December 1978 and January 1979 and published in the May 1979 issue of \"Playboy\" magazine.\n\nSummary sentence:\nIn 1979, Carlos raised public awareness of transgender issues by disclosing her transgender status, and in 1972 had undergone sex reassignment surgery.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb411cb24f3",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2012, Sethi recorded \"Dil Jalannay Ki Baat Karte Ho\", which was featured in Mira Nair's political-thriller, \"The Reluctant Fundamentalist.\"\n\nSummary sentence:\nIn 2012, Sethi recorded the song \"Dil Jalane Ki Baat Karte Ho\", which was featured in Mira Nair's 2012 film, \"The Reluctant Fundamentalist\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qa4062ba0c0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- It also peaked on a number of charts, including No. 1 on Finland's Official List for albums, No. 6 on the \"Billboard\" Dance/Electronic Albums chart and No. 11 on the US Independent Albums chart.\n\nSummary sentence:\nIt peaked at number one on Finland's Official List and number 6 on the \"Billboard\" Dance/Electronic Albums chart.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb60b3e76bc",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Rollins appears in FX's \"Sons of Anarchy\"s second season, which premiered in the fall of 2009 in the United States.\n- Rollins plays A.J. Weston, a white supremacist gang leader and new antagonist in the show's fictional town of Charming, California, who poses a deadly threat to the Sons of Anarchy Motorcycle Club.\n- In 2014, he voiced the antagonist Zaheer in the third season of the animated series \"The Legend of Korra\".\n- Rollins began his film career appearing in several independent films featuring the band Black Flag.\n\nSummary sentence:\nHe appeared in the second season of \"Sons of Anarchy\" as A.J. Weston, in the 3rd season of the animated series \"The Legend of Korra\" as Zaheer, and has also had roles in several films.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q93153e20ac",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Hannah Dakota Fanning\n- Fanning was born in Conyers, Georgia.\n- When Fanning was a small child, she was an actress at the Towne Lake Arts Center in Woodstock, Georgia, starring in small plays.\n\nSummary sentence:\nHannah Dakota Fanning (born February 23, 1994) is an American actress.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd09549a3ae",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Kelly lifted off aboard \"Soyuz TMA-01M\" from the Baikonur Cosmodrome in Kazakhstan at 7:10 pm EDT on October 7, 2010 along with cosmonauts Aleksandr Kaleri and Oleg Skripochka.\n- Kelly, Kaleri, and Skripochka arrived at the ISS on October 9, 2010, and joined Commander Douglas H. Wheelock and flight engineers Shannon Walker and Fyodor Yurchikhin on Expedition 25.\n- The crew of Expedition 24/25 returned to Earth on November 25, 2010 aboard \"Soyuz TMA-19\"; Wheelock transferred command of the station to Kelly.\n\nSummary sentence:\nHe arrived at the ISS aboard Soyuz TMA-01M on 9 October 2010, and served as a flight engineer until he took over command of the station on 25 November 2010 at the start of Expedition 26.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q42824aeeae",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2005, Smart co-starred with Ryan Reynolds in the romantic comedy film \"Just Friends\", playing the high school friend of a previously overweight young man who, years later, returns to her hometown and attempts to confess his love for her.\n- Smart appeared as Joy in the 2006 sports drama \"Peaceful Warrior\", about a gymnast whose life changes after an encounter with a spiritual guide.\n\nSummary sentence:\nSmart co-starred with Ryan Reynolds and Anna Faris in \"Just Friends\" (2005), followed by the sports drama \"Peaceful Warrior\" (2006).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q15d557dd5a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dandekar served as a Vice President of Indian Merchants' Chambers and now serves as the Non Executive Chairman of Camlin Fine Sciences Ltd. (formerly, Camlin Fine Chemicals Ltd) and has been its Director since June 2006.\n- He has served as the chairman of Camlin Limited since June 1, 2002.\n\nSummary sentence:\nHe is presently the chairman of Camlin Limited and Camlin Fine Sciences.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qbee52dfc7f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Three Polish-Jewish brothers, Herman, Hillel, and Henry Hassenfeld, founded Hassenfeld Brothers in Providence, Rhode Island, in 1923, a company selling textile remnants.\n\nSummary sentence:\nHasbro is incorporated in Rhode Island.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qba7ca3ea78",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He was in the show \"Real Husbands of Hollywood,\" where he played a fictionalized version of himself.\n\nSummary sentence:\nHe also portrayed a fictionalized version of himself on \"Real Husbands of Hollywood\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q39d8afdc20",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She began by writing the \"Boston Letter\" for \"Art International,\" but soon published well-received articles on Jasper Johns (\"Lugano Review\", 1965) and Donald Judd (\"Allusion and Illusion in Donald Judd,\" \"Artforum\", May 1966).\n- Krauss used \"October\" as a way of publishing essays on post-structuralist art theory, Deconstructionist theory, psychoanalysis, postmodernism and feminism.\n- Whether about (Cubist collage, Surrealist photography, early Giacometti sculpture, Rodin, Brâncuși, Pollock) or about art contemporaneous to her own writing (Robert Morris, Sol LeWitt, Richard Serra, Cindy Sherman), Krauss translates the ephemeralities of visual and bodily experience into precise, vivid English, which has solidified her prestige as a critic.\n\nSummary sentence:\nAs a critic and theorist she has published steadily since 1965 in \"Artforum,\" \"Art International\" and \"Art in America\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7c788da5a5",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He is currently an associate professor of biology at the University of Minnesota's Morris campus.\n\nSummary sentence:\nHe is associate professor of biology at the University of Minnesota Morris (UMM).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2dad3f2d45",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Fred L. Thomas\n- Thomas originally played college football for Northwest Mississippi Community College during the 1992-1993 seasons.\n\nSummary sentence:\nFrederick L. Thomas is a football player.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf67e35a272",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Colombo was selected in the first round (29th overall) of the 2002 NFL Draft by the Chicago Bears.\n- Colombo was out of football until he signed with the Dallas Cowboys on November 1, 2005.\n- On July 31, 2011, Colombo was signed as free agent by the Miami Dolphins, reuniting with former Cowboys head coach Bill Parcells, who was the team's Executive Vice President of Football Operations.\n\nSummary sentence:\nHe played eleven seasons in the National Football League (NFL) for the Chicago Bears, Dallas Cowboys and Miami Dolphins.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qa9785437a4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On 15 February 2011, Sanz announced that he would be signing with Universal Music Group after twenty years with Warner.\n- On 2 September 2012, the singer unveiled the official artwork of his upcoming ninth studio album, \"La Música No Se Toca\" on his official site.\n- Sanz released \"La Música No Se Toca\", featuring the single \"No Me Compares\" and based on the opening theme song in the telenovela \"Amores Verdaderos\", on 25 September 2012.\n- Sanz released his eleventh studio album, \"Sirope\", featuring the single \"A Que No Me Dejas\", a collaboration with Alejandro Fernandez and used as the opening theme song in the telenovela \"A Que No Me Dejas\", on 4 May 2015.\n\nSummary sentence:\nSanz signed to Universal Music Group in 2011 and released his tenth studio album, \"La Música No Se Toca\", in 2012, followed by \"Sirope\" in 2015.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb5b208aa05",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Armando Giovanni Iannucci\n- Iannucci was born in Glasgow.\n- Between 1995 and 1999, Iannucci produced and hosted \"The Saturday Night Armistice\".\n- After championing \"Yes Minister\" on the BBC's \"Britain's Best Sitcom\", Iannucci devised, directed and was chief writer of \"The Thick of It\", a political satire-cum-farce for BBC Four.\n\nSummary sentence:\nArmando Giovanni Iannucci is a Scottish satirist, writer, director, producer, and performer.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf97ec93cce",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After resigning as president of the Parents Television Council, he remains an adviser to that organization.\n\nSummary sentence:\nBozell served as president of the Parents Television Council from 1995 to 2006.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q50d97ab59a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2006, the science journal \"Nature\" listed Pharyngula as the top-ranked blog written by a scientist.\n\nSummary sentence:\nIn 2006 the journal \"Nature\" listed Myers's \"Pharyngula\" as the top-ranked blog by a scientist.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 }
]
