# Replay noise screen blind read NS-usb_factuality-blind_read-0714a308-014 (family NS-usb_factuality)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-usb_factuality-blind_read-0714a308-014.json

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
  "qid": "q6b07b0d336",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Ewald Johann Stadler\n- Stadler was born in Mäder, Austria.\n- On 23 December 2013 (one day before Christmas Eve) Stadler, together with Rudolf Gehring of the Christian Party of Austria announced in a press conference they were founding a new party, The Reform Conservatives (REKOS) for which Stadler would run for the European Parliament election on 25 May 2014.\n\nSummary sentence:\nEwald Johann Stadler is an Austrian conservative politician.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q06cbff9325",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2005, Wood started his own record label called Simian Records.\n\nSummary sentence:\nWood founded the record label Simian Records in 2005.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q62204525c1",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2003, Bose entered mainstream Bollywood cinema with \"Jhankaar Beats\" in which he played one of two friends, R.D. Burman fans who are obsessed with winning a music competition.\n- He starred in \"Chameli\" opposite Kareena Kapoor, playing a wealthy chain-smoking Mumbai banker who is stranded in the monsoon rains with a prostitute.\n- With his next effort, the romantic comedy \"Pyaar Ke Side Effects\", Bose moved once more into mainstream Bollywood cinema.\n- Sherawat and Bose also starred together in another Bollywood comedy, \"Maan Gaye Mughal-e-Azam\" (2008), which was a commercial and critical failure.\n- Bose also appeared in \"Shaurya\", a military court room drama modelled on the American film \"A Few Good Men\".\n\nSummary sentence:\nHe has also appeared in films such as \"Pyaar Ke Side Effects\", \"Maan Gaye Mughal-e-Azam\", \"Jhankaar Beats\", \"Chameli\" and \"Shaurya\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qdb1dba09f0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1980, she became office manager and later deputy director of the industry organization Textile Industry.\n- From 1983 to 1984, she was deputy chair of the Junior Chamber Denmark.\n- Lundholt was appointed CEO of the Furniture Manufacturers Association (later the Danish Furniture Industry) in 1988 and was promoted to chair the following year.\n\nSummary sentence:\nShe was deputy director of the industry organization Textile Industry from 1980 to 1988, deputy chair of the Junior Chamber Denmark between 1983 and 1984 and CEO later chair of the Furniture Manufacturers Association (later the Danish Furniture Industry) in 1988.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qb7711a0b06",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Ramzi bin al-Shibh\n- Ramzi bin al-Shibh was born 1 May 1972 in Hadhramaut province in Yemen.\n- On September 6, 2006, U.S. President George W. Bush announced that bin al-Shibh and thirteen other CIA-held, high-value detainees had been transferred to Guantanamo Bay detention camp.\n- The Department of Defense announced on August 9, 2007 that all fourteen of the \"high-value detainees\" who had been transferred to Guantanamo from the CIA's black sites, had been officially classified as \"enemy combatants\".\n\nSummary sentence:\nRamzi bin al-Shibh (born May 1, 1972) is a Yemeni citizen currently being held by the U.S. as an enemy combatant detainee at Guantanamo Bay.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q76951dd466",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- University of Dayton School of Law\n- The School of Law was first established as the University of Dayton College of Law in 1922 under the guidance of Dean John C. Shea, the former first assistant director of law for Dayton.\n\nSummary sentence:\nThe University of Dayton School of Law (UDSL) is a private law school located in Dayton, Ohio.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q50e5705038",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- College of the Holy Cross\n- Relations with Boston's civic leaders worsened such that, when a Jesuit faculty was finally secured in 1843, Fenwick decided to leave the Boston school and instead opened the College of the Holy Cross 45 miles (72 km) west of the city in central Massachusetts, where he felt the Jesuits could operate with greater autonomy.\n- Next May I shall lay the foundation of a splendid College in Worcester ...\n- It offers 28 majors mainly focused on a liberal arts curriculum, each of which leads to the completion of the Bachelor of Arts degree.\n\nSummary sentence:\nThe College of the Holy Cross is a Jesuit liberal arts college in Worcester, Massachusetts, west of Boston.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q06d77f390f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- They valued his personal worth at US$12 billion.\n\nSummary sentence:\n\"Forbes\" assessed his net worth in 2022 at US$12 billion; listing his sisters' wealth independently.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qa927339493",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1986, she eventually joined the Scottish National Party.\n- Whilst working in Edinburgh, Hyslop spent her spare time campaigning for the SNP and was an active member of the Young Scots Nationalists, the SNP's youth wing.\n\nSummary sentence:\nHyslop joined the SNP in 1986 and spent her spare time campaigning.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qbe653d8cdb",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- At least seven people were killed in Bavaria, where districts established \"disaster areas\".\n\nSummary sentence:\nAt least 21 people died in the floods.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q5eeb684826",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Alex Sharp\n- Sharp was born on 2 February 1989 in Westminster, London, and was raised traveling throughout Europe and the Southwest of the United States in a caravan, before moving to Dorset, England, age eight.\n- According to the \"Irish Mirror\", his acting debut was at age 4 when he appeared in \"A Touch of Frost\" for £10.\n\nSummary sentence:\nAlexander Ian Sharp (born 2 February 1989) is an English actor.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q9e8b480d9b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Jones is the publisher and director of the \"InfoWars\" fake news website responsible for promoting conspiracy theories.\n- Another of Jones' websites is PrisonPlanet.com.\n- After \"InfoWars\" was banned from Facebook, Jones used another of his websites, \"NewsWars\", to circumvent the ban.\n\nSummary sentence:\nJones's website, \"InfoWars\", promotes conspiracy theories and fake news, and his other websites include \"NewsWars\" and \"PrisonPlanet\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q1954fa941d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Bharat Aluminium Company Ltd. (BALCO)\n- It is the first public sector enterprise in India which started producing aluminium in 1974.\n- Till 2001, BALCO was a public sector enterprise owned 100% by Government of India.\n\nSummary sentence:\nBharat Aluminium Company Ltd. (BALCO) was an Indian government owned aluminium producer under Ministry of Mines, Government of India.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qe900e87531",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Laurie Elizabeth Metcalf\n- Metcalf was born in Carbondale, Illinois, the eldest of three children.\n- She won the 2011 Lucille Lortel Award, Outstanding Lead Actress, and the 2011 Obie Award, for her performance.\n\nSummary sentence:\nLaura Elizabeth Metcalf (born June 16, 1955) is an American actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7befd7e0ec",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2015, Goth played the lead role of Milja in the post-apocalyptic thriller \"The Survivalist\" directed by Fingleton, followed by roles as Meg Weathers in the disaster adventure-thriller film \"Everest\" (2015) directed by Baltasar Kormákur, and Hanna Helmqvist in an episode of BBC One's crime series \"Wallander\".\n- She also appeared in the horror film \"A Cure for Wellness\" (2016) directed by Gore Verbinski; and had supporting roles in Luca Guadagnino's remake of \"Suspiria\" (2018) and the sci-fi mystery film \"High Life\" (2018) directed by Claire Denis.\n\nSummary sentence:\nShe was subsequently cast in the thriller \"The Survivalist\" (2015) and the horror film \"A Cure for Wellness\" (2016).",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q8b323d3846",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He can also be seen as Principal Pearson on the 2016 TV Land comedy \"Teachers\".\n\nSummary sentence:\nBagley had a role as Principal Pearson on the comedy \"Teachers\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q0a4883ad1b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Raniero Cantalamessa\n- Raniero Cantalamessa was born in Colli del Tronto, Italy, on 22 July 1934.\n- He was ordained as a priest in the Franciscan Capuchin order in 1958.\n- He holds doctoral degrees in theology and classical literature.\n- On 25 October 2020, Pope Francis announced he would raise him to the rank of cardinal at a consistory scheduled for 28 November 2020.\n\nSummary sentence:\nRaniero Cantalamessa (born 22 July 1934) is an Italian Catholic cardinal and priest in the Order of Friars Minor Capuchin and a theologian.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q0bd10913e3",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In the 2015 federal election Fortin ran for the redistributed riding of Avignon—La Mitis—Matane—Matapédia under the Strength In Democracy banner.\n- He lost to Liberal Rémi Massé, coming in fourth.\n\nSummary sentence:\nIn the 2015 federal election he ran for the redistributed riding of Avignon—La Mitis—Matane—Matapédia and lost to Liberal Rémi Massé.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q385d2863c2",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On September 10, 1982, he was signed as a free agent by the Ottawa Rough Riders.\n- On December 6, 1984, he was signed by the Saskatchewan Roughriders.\n\nSummary sentence:\nHe was also a member of the Ottawa Rough Riders and Saskatchewan Roughriders.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q47ad0cc7fd",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In September 2016, following the dismissal and disciplinary investigation into Huang Xingguo, Wang was named mayor of Tianjin.\n\nSummary sentence:\nHe was formerly the Mayor of Tianjin, one of the four direct-controlled municipalities of China.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qdecf68694e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- This makes it the largest international school in the United States and the largest private school in Houston.\n\nSummary sentence:\nAwty is the largest international school in the United States and the largest private school in Houston.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q790289ff96",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In April 2007, Ferrell and Adam McKay launched \"Funny or Die\", a streaming video website where short comedy films are uploaded and voted on by users.\n\nSummary sentence:\nHe founded the comedy website Funny or Die in 2007 with his writing partner Adam McKay.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb7e52e9915",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The Sorbonne itself was disestablished by decree of 5 April 1792, after the French Revolution.\n\nSummary sentence:\nThe Sorbonne was disestablished by decree of 5 April 1792, after the French Revolution.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qdf222b8183",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He was the primary point guard for the Puerto Rican team that won the silver medal in the 2007 Pan American Games.\n\nSummary sentence:\nHe was the starting point guard for Puerto Rico when they won the gold medal in the 2011 Pan American Games and the silver medal in the 2007 Pan American Games.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q057587cc1a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Sanders played a nine-year, part-time baseball career, playing left and center field in 641 games with four teams.\n- The New York Yankees selected Sanders in the 30th round of the 1988 Major League Baseball draft, and he signed with the team on June 22.\n- Sanders later signed with the Atlanta Braves for the 1991 MLB season.\n- In 1997, Sanders finished second in the NL with 56 stolen bases in 115 games while with the Cincinnati Reds before leaving baseball for three years.\n\nSummary sentence:\nSanders was also a baseball outfielder for nine seasons in Major League Baseball (MLB) with the New York Yankees, Atlanta Braves, and Cincinnati Reds.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q423675d2bc",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Olena Serhijivna Sotnyk\n- • 2004 – began to work as the chief legal counsel at the company \"Svema\" in Shostka, Sumy region.\n- • Since 2014 – Member of the Parliament of Ukraine.\n- The 11th number in the list of the Samopomich Union Party during 2014 parliamentary elections in Ukraine.\n\nSummary sentence:\nOlena Serhijivna Sotnyk is a Ukrainian lawyer and politician, Member of the Parliament of Ukraine from Samopomich Union Party.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q0896e02107",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In addition to serving as a judge on \"Top Chef\", Young has competed in the Channel 4 TV series \"Come Dine with Me\", appeared as one of the panel of food critics in the 2008 BBC Two series \"Eating with the Enemy\" and served as a judge on \"Hell's Kitchen\".\n\nSummary sentence:\nHe also served as a judge in seasons five and six of the television show \"Top Chef\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd8670cef80",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Aivaras Abromavičius\n- Abromavičius was born in Lithuania, but lived in Estonia, Sweden, USA and Russia for many years.\n- During 2002–2014, he co-owned and was at the core of building a Stockholm-based investment company East Capital, one of the largest and most reputable Investment companies from western Europe investing in eastern Europe.\n- Ukrainian President Petro Poroshenko granted citizenship to Abromavičius, Natalie Jaresko and Alexander Kvitashvili on 2 December 2014 to allow them to serve as ministers in the Second Yatsenyuk Government.\n\nSummary sentence:\nAivaras Abromavičius (, born 21 January 1976) is a Lithuanian-born Ukrainian investment banker and politician.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q6a6bbcbbd9",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- This announcement was accompanied by the announcement of a fourth single, \"Alone Time\", which was released on the April 24, 2020, the date the LP was originally due to be released.\n- On July 10, Rufus Wainwright's 10th studio album, \"Unfollow the Rules\", was released.\n\nSummary sentence:\nRufus' 10th studio album, \"Unfollow the Rules\", was released on July 10, 2020.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q14544ce567",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After the establishment of the state of Israel the company expanded its commercial and financial activities and was one of the first companies in the country whose shares were traded on the Tel Aviv Stock Exchange.\n\nSummary sentence:\nThe company’s shares are traded on the Tel Aviv Stock Exchange and are a constitute of the TA-25 Index.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q2ed17c64c6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Tan was promoted Senior Minister of State on 13 June 2022 while serving both portfolios of Communications and Information and National Development.\n\nSummary sentence:\nIn 2022, Tan was promoted Senior Minister of State after a Cabinet reshuffle.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qa76d311210",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- At that time, at least 51 people were known to have died in Greater La Plata, and six deaths had been reported in Buenos Aires.\n- Two additional deaths were reported in Greater Buenos Aires.\n\nSummary sentence:\nGreater La Plata was hit with reported deaths, and Greater Buenos Aires reported deaths.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qffffa65d5a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Its clients range across Textile and Garment Industry, Water Treatment Industry, Leather Industry, Construction Industry, Paint Industry Agrochemicals, Adhesives and others.\n\nSummary sentence:\nFineotex is engaged in manufacturing of Speciality Chemicals and Enzymes for Textile and Garment Industry, Water Treatment Industry, Leather Industry, Construction Industry, Paint Industry Agrochemicals, Adhesives and others.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q20a47bc8b4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Shortly after, Zuniga was cast in the television drama film \"Stone Pillow\" (1985), playing a social worker in New York City who forms a bond with an elderly homeless woman, played by Lucille Ball.\n- The next year, Zuniga appeared in a lead role in the blockbuster horror film \"The Fly II\" (1988), followed by the drama-comedy \"Staying Together\" (1989), and as a med student opposite Matthew Modine in the drama \"Gross Anatomy\" (1989).\n\nSummary sentence:\nShe also starred opposite Lucille Ball in the television drama film \"Stone Pillow\" (1986), and in the science-fiction horror sequel \"The Fly II\" (1989).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qba1231df96",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Thomas Løvendahl Sørensen\n- On 24 July 2017, Sørensen announced his retirement from professional football at the age of 41.\n- For the 2002 FIFA World Cup qualifying campaign in 2001, he took over the job as goalkeeper and helped Denmark qualify.\n\nSummary sentence:\nThomas Løvendahl Sørensen (born 12 June 1976) is a retired Danish footballer who played as a goalkeeper.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q40a9fe218a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Chloe Rose\n- Rose was born and raised in Toronto, Ontario.\n- Rose first attracted attention for her portrayal of Katie Matlin in the long-running teen drama television series Degrassi: The Next Generation.\n\nSummary sentence:\nRose is a Canadian actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf73ee4d86f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She began her career as a freelance journalist in 1966 and had articles published in \"The Economic Times\", \"The Indian Express\" and many other periodicals.\n\nSummary sentence:\nAs a freelance journalist, she has been writing extensively on films, theatre, art and feminist issues, for publications of The Times Group, \"The Telegraph\", \"The Hindu\" and \"The Indian Express\" .",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q2edece3406",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Murder of Rikidōzan\n- He later left sumo in 1950, and after attending an American wrestling show in 1951, became a pro-wrestler.\n- On the evening of December 8, 1963, Rikidōzan had been drinking with friends in Tokyo's New Latin Quarter Club, an upscale bar and nightclub.\n- Later, while talking to a woman, he was involved in an altercation with Katsushi Murata, a member of the Sumiyoshi-ikka, a sub branch of the Sumiyoshi-kai yakuza family.\n- Rikidōzan then mounted Murata and continued to punch him on the ground until Murata stabbed Rikidōzan once in the abdomen.\n\nSummary sentence:\nOn December 8, 1963, the Japanese professional wrestler Rikidōzan, real name Mitsuhiro Momota, was stabbed in a Tokyo nightclub after an altercation with a Yakuza member.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q5acb626f86",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2002, he served as president of the Academy of Learned Societies in the Social Sciences.\n\nSummary sentence:\nHe served as president of the Academy of Social Sciences from 2003 to 2008.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qecbc2f7d66",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Chapman's follow-up album, \"Crossroads\" (1989), was less commercially successful than her debut had been, but it still achieved platinum status in the U.S.\n\nSummary sentence:\nIn 1989, Chapman released her second album, \"Crossroads\", which earned her an additional Grammy Award nomination for Best Contemporary Folk Album.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q9e40a24e86",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Sanjay Shah\n- He founded the hedge fund firm Solo Capital in London, which employed \"more than 100 financial experts across offices in London and Dubai\".\n- In 2009, he moved to Dubai \"after falling in love with the city\".\n\nSummary sentence:\nSanjay Shah is a Dubai-based British businessman.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qa2eb53addc",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In May 2005, Paltrow became the face of Estée Lauder's Pleasures perfume.\n\nSummary sentence:\nBeginning in 2005, Paltrow has been the face of Estée Lauder's Pleasures perfume.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb9e5f14f71",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- While taking care of his mother, he accepted the lead role in the movie \"Great World of Sound\" in 2007.\n\nSummary sentence:\nHe was nominated for the Independent Spirit Award for Best Supporting Male for his performance in the film \"Great World of Sound\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q7bf4b6e122",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She announced on May 16, 2019 that she would resign her seat in the legislature to become Principal of Massey College at the University of Toronto effective August 1, 2019.\n\nSummary sentence:\nShe is the 6th and current Principal of Massey College at the University of Toronto.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qd0ec9ee6db",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- One of nine children, siblings include her twin sister Isabel Maxwell, brothers Kevin Maxwell and Ian Maxwell, and Ghislaine Maxwell.\n\nSummary sentence:\nHer sister is convicted sex trafficker Ghislaine Maxwell.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc26e062cbb",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Paul Berg\n- Berg was born in Brooklyn, New York, the son of a Russian Jewish immigrant couple, Sarah Brodsky, a homemaker, and Harry Berg, a clothing manufacturer.\n- After 1959, Berg moved to Stanford University, where he taught biochemistry from 1959 until 2000 and served as director of the Beckman Center for Molecular and Genetic Medicine from 1985 until 2000.\n- Berg is currently a professor emeritus at Stanford.\n\nSummary sentence:\nPaul Berg is an American biochemist and professor emeritus at Stanford University.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q455225f9e8",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- William D. Casey\n- Casey was born in Amherst, Nova Scotia.\n- He was first elected, as a member of the Progressive Conservative Party of Canada, to represent the riding of Cumberland—Colchester in the 1988 election.\n- In common with almost every other PC Member of Parliament (MP) in the 1993 election he lost his seat, in his case being defeated by Liberal candidate Dianne Brushett.\n\nSummary sentence:\nWilliam D. Casey (born February 19, 1945) is a Canadian politician from Nova Scotia who served as a Member of Parliament (MP) in the House of Commons of Canada.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q039cca83b6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2009, Bisset reunited with Linda Yellen for \"The Last Film Festival\", which was Dennis Hopper's final screen appearance.\n- It finally premiered in 2016.\n- Next, she played Gérard Depardieu's wife in \"Welcome to New York\" (2014) for controversial director Abel Ferrara.\n- In 2015, she co-starred with Drew Barrymore and Toni Collette in \"Miss You Already\".\n- On the indie circuit, Bisset kept busy with roles in four features in 2018: \"Head Full of Honey\", which reunited her with \"The Deep\" co-star Nick Nolte; \"Backstabbing for Beginners\" (opposite Ben Kingsley); \"Here and Now\" with Sarah Jessica Parker; and \"Asher\" with Famke Janssen and Ron Perlman.\n- In 2020, Bisset joined the cast of \"Birds of Paradise\" from Amazon Studios, shot in Budapest.\n\nSummary sentence:\nBisset has since appeared in \"Welcome to New York\" (2014), \"Miss You Already\" (2015), \"The Last Film Festival\" (2016), \"Backstabbing for Beginners\" (2018) and \"Birds of Paradise\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q55ab9da2fd",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1998, Lozada and former Menudo members Rene Farrait, Miguel Cancel, Ray Reyes, Charlie Masso and Ricky Meléndez got together in Puerto Rico for a concert named El Reencuentro, with dedication to the convalescing ex-Menudo Fernando Sallaberry, Menudo's original lead singer, who was unable to join the reunion due to health issues.\n\nSummary sentence:\nIn 1998, Lozada and other former members of Menudo formed El Reencuentro.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q2b285af6b2",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1999, he presented the Sanremo Music Festival with virologist Nobel Prize-winner Renato Dulbecco and French actress and model Laetitia Casta.\n- The following year, he was confirmed as the presenter of the singing competition.\n- In June 2012, RAI announced Fabio Fazio as the presenter of the 63rd Sanremo Music Festival.\n\nSummary sentence:\nHe presented the Sanremo Music Festival in 1999, 2000, 2013 and 2014.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 }
]
