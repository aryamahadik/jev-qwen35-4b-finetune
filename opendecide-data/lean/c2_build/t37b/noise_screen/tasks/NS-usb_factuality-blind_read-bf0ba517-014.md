# Replay noise screen blind read NS-usb_factuality-blind_read-bf0ba517-014 (family NS-usb_factuality)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-usb_factuality-blind_read-bf0ba517-014.json

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
  "qid": "qcb4cdeb980",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- \"Ragtime\" followed, opening on Broadway in January 1998 and running for 834 performances.\n- \"Ragtime\" was nominated for twelve Tony Awards and won the Best Original Scorefor Lynn Ahrens and Stephen Flahertyin addition to the Drama Desk Award for Outstanding Lyrics.\n\nSummary sentence:\nShe won the Tony Award and Drama Desk Award for the Broadway musical \"Ragtime\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q5553bc120c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In the late 1970s and the 1980s she had several small roles in soap opera \"Prisoner\".\n- Having briefly played the brusque daughter of released prisoner \"Mum\" Brooks in 1979, Charleston returned for several appearances in the serial as policewomen through the early 1980s before taking the larger recurring role of Deidre Kean, mother of prison toughie Reb Kean (Janet Andrewartha), in 1984.\n\nSummary sentence:\nIn 1979, she had a role in \"Prisoner\" as the daughter of inmate \"Mum\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1eac9fd07b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She was also featured opposite Arnold Schwarzenegger in the 1999 supernatural action film \"End of Days\".\n\nSummary sentence:\nShe had leading roles in the films \"End of Days\" (1999), \"Supernova\" and \"Vertical Limit\" (both 2000).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q09b1d827d6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- For the first two years of the undergraduate programme students were based at either the University of Exeter or the University of Plymouth.\n\nSummary sentence:\nThe school was based at the University of Plymouth and the University of Exeter.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd799d31f60",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Health Minister Pilar Mazzetti reported a shortage of 110 tons of oxygen daily.\n\nSummary sentence:\nAs of June 2020, oxygen was in short supply.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q99c35eae6a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Gilbert created a scripting language that was named after the project it had been written for, the Script Creation Utility for Maniac Mansion, better known as S.C.U.M.M. The technology was used in all subsequent LucasArts adventure games, with the exception of \"Grim Fandango\" and \"Escape From Monkey Island\".\n\nSummary sentence:\nHe invented S.C.U.M.M., a technology used in many subsequent games.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q937755505d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He ran successfully in the 2020 Le Havre mayoral election.\n\nSummary sentence:\nHe was re-elected to the mayorship in Le Havre.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7794d36354",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Over his career, Bagwell batted at least .300 six times, amassed a 1.000 OPS five times, collected at least 30 home runs eight times, 100 RBI eight times, 100 runs scored nine times, and 100 walks seven times.\n\nSummary sentence:\nOverall, Bagwell batted over .300 six times.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q10774ba5df",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Thomas played for the Seattle Seahawks from 1996 to 1999.\n\nSummary sentence:\nHe was drafted by the Seattle Seahawks in 1996.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qdc0be08a97",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In later years, she appeared as Richard T. Jones' mother in the romantic comedy \"The Wood\" (1999), and played Romany Malco's mother in the comedy film \"The Love Guru\" (2008).\n\nSummary sentence:\nIn film, Hopkins co-starred in 1984 science fiction film \"Trancers\" and in its sequels \"Trancers II\" (1991) and \"Trancers III\" (1992), as well as appearing in \"The Wood\" (1999) and \"The Love Guru\" (2008).",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd691bf0d1e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- David Mumford\n- Mumford was born in Worth, West Sussex in England, of an English father and American mother.\n- In a sequence of four papers published in the \"American Journal of Mathematics\" between 1961 and 1975, Mumford explored pathological behavior in algebraic geometry, that is, phenomena that would not arise if the world of algebraic geometry were as well-behaved as one might expect from looking at the simplest examples.\n\nSummary sentence:\nDavid Bryant Mumford (born 11 June 1937) is an American mathematician known for his work in algebraic geometry and then for research into vision and pattern theory.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7e94455785",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Muhammad attended high school in Las Vegas Valley in Nevada at Bishop Gorman High School, a Catholic high school with a $12,000 annual tuition that possessed a competitive athletics program.\n\nSummary sentence:\nMuhammad went to Bishop Gorman High School, where he was named Mr. Basketball USA and Naismith Prep Player of the Year in his senior year.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf9d521e78e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On 7 February 2007, Neville won his 85th cap in England's 1–0 friendly defeat to Spain.\n\nSummary sentence:\nHe is England's most-capped right-back with 85 caps.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q6f0691db00",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He came to regard this as a \"thankless position\" and a \"very hard sell\" to potential clients due to their intrinsic resistance to new processes; this and the dearth of immediate flight opportunities ultimately precipitated his departure from NASA in 1977.\n- Schweickart then served for two years as California Governor Jerry Brown's assistant for science and technology before being appointed by Brown to the California Energy Commission for five and a half years.\n\nSummary sentence:\nSchweickart left NASA in 1977 to serve for two years as California Governor Jerry Brown's assistant for science and technology, then was appointed by Brown to California's Energy Commission for five and a half years.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q95921967aa",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Shortly after, Zuniga was cast in the television drama film \"Stone Pillow\" (1985), playing a social worker in New York City who forms a bond with an elderly homeless woman, played by Lucille Ball.\n- The next year, Zuniga appeared in a lead role in the blockbuster horror film \"The Fly II\" (1988), followed by the drama-comedy \"Staying Together\" (1989), and as a med student opposite Matthew Modine in the drama \"Gross Anatomy\" (1989).\n\nSummary sentence:\nShe also starred opposite Lucille Ball in the television drama film \"Stone Pillow\" (1986), and in the science-fiction horror sequel \"The Fly II\" (1989).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qd898db763a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The \"Arthur D. Little School of Management\" was founded in 1964 by Arthur Dehon Little in Cambridge, Massachusetts.\n- In 1921, future British Prime Minister Bonar Law acquired Ashridge House, in Hertfordshire, United Kingdom, through a trust, with the intent to establish a college at the estate.\n- In 1959, the college was re-established as a school of management under the name \"Ashridge Business School\".\n- In 2002, Swedish billionaire Bertil Hult purchased the Arthur D. Little School of Management, which resulted in the school's reorganization and reestablishment as Hult International Business School in 2003.\n- In 2014, Hult International Business School acquired and merged with Ashridge Business School, creating one of the largest business schools in the world.\n\nSummary sentence:\nHult is the successor of the Arthur D. Little School of Management, founded in 1964 in Cambridge, Massachusetts, and of the Ashridge Business School, founded in 1959 in Ashridge, United Kingdom.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q471d4851bb",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Subsequently, the Roman Catholic Archdiocese of Galveston-Houston allowed the school to begin using a house previously used by Catholic Charities, and the art and music classes of OLG were moved into this house.\n\nSummary sentence:\nIt is in the Roman Catholic Archdiocese of Galveston-Houston.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1ecadd1d71",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dexter Maurice Wynn\n- Dexter played high school football at Rampart High School in Colorado Springs, as a wide receiver and cornerback.\n\nSummary sentence:\nDexter Maurice Wynn is a former American football cornerback.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q92f0f95673",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In April 2008, he was elected by his legislator colleagues as the Deputy Speaker of the Legislative Assembly of Alberta, defeating Len Mitzel and Bridget Pastoor in a secret ballot.\n\nSummary sentence:\nIn April 2008, he elected as the Legislature's Deputy Speaker and Chair of Committees and served in that position for the 27th Legislature.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q78d6566f5d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Alannah Joan Geraldine Cecilia MacTiernan\n- In 1993, she was elected as the member for the East Metropolitan region in the Western Australian Legislative Council.\n\nSummary sentence:\nAlannah Joan Geraldine Cecilia MacTiernan is an Australian politician.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf0c75da241",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2019, di Giovanni was named a Guggenheim Fellow.\n\nSummary sentence:\nShe was named a 2019 Guggenheim Fellow, and in 2020, the American Academy of Arts and Letters awarded her the Blake-Dodd nonfiction prize for her lifetime body of work.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q13fc6c26b4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Just before 2018 Rajasthan Legislative Assembly elections he quit BJP to join Indian National Congress.\n\nSummary sentence:\nHe joined Congress in 2018.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q18a69f6c01",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The United Front included beside the dominantly Tajik forces of Massoud and the Uzbek forces of Dostum, Hazara factions and Pashtun forces under the leadership of commanders such as Abdul Haq, Haji Abdul Qadeer, Qari Baba or diplomat Abdul Rahim Ghafoorzai.\n\nSummary sentence:\nThe United Front included all Afghan ethnicities: Tajiks, Uzbeks, Hazaras, Turkmens, some Pashtuns and others.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q6b52f91782",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Stone obtained the role of Janice Henry in the ABC miniseries \"War and Remembrance\" (1987), the sequel to the 1983 miniseries \"The Winds of War\", based on the 1978 novel of the same name written by Herman Wouk.\n- In 2000, Stone played a lesbian trying to start a family, opposite Ellen DeGeneres, in the HBO television film \"If These Walls Could Talk 2\" and starred as an exotic dancer, alongside Billy Connolly, in the comedy \"Beautiful Jo\".\n- Stone returned to television in 2018, when she portrayed a murdered children's book author and illustrator in Steven Soderbergh's HBO mystery production \"Mosaic\", which was released as an iOS/Android mobile app serving as an interactive film and as a television drama.\n- In Netflix's psychological thriller series \"Ratched\" (2020), a prequel to Miloš Forman's 1975 film \"One Flew Over the Cuckoo's Nest\" developed by Ryan Murphy, Stone portrayed a wealthy heiress who hires a hit man to kill a doctor for disfiguring her son.\n\nSummary sentence:\nOn television, Stone has had leading and supporting roles in productions such as the ABC miniseries \"War and Remembrance\" (1987), the HBO television film \"If These Walls Could Talk 2\" (2000), Steven Soderbergh's \"Mosaic\" (2017) and Ryan Murphy's \"Ratched\" (2020).",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf222f1e511",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2015, Jackson returned to acting following a 23-year absence, having retired from politics.\n\nSummary sentence:\nShe retired from politics and returned to acting in 2015.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q82cce7de02",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Among other theatre schools and companies, the Dramatic Workshop played a vital role in paving the way for Off-Broadway theatre.\n\nSummary sentence:\nThe Dramatic Workshop considerably contributed to paving the way for Off-Broadway theatre.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q572b04404d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Jalin Delane Marshall\n- Going into the regular season, Marshall was named the fourth wide receiver on the Jets depth chart behind veterans Brandon Marshall, Eric Decker, and Quincy Enunwa.\n- He was also given punt and kick return duties.\n- Marshall signed with the Edmonton Elks to open free agency on February 8, 2022.\n\nSummary sentence:\nJalin Delane Marshall is a football wide receiver and return specialist signed with the Edmonton Elks.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q29d6796645",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Darul Uloom Haqqania\n- Haq was the chancellor of Darul Uloom Haqqania, a Deobandi Islamic seminary which is the alma mater of many prominent Taliban members.\n- Following the assassination, the Khyber Pakhtunkhwa government declared a day of mourning.\n- On 3 November 2018, he was buried in the premises of Darul Uloom Haqqania in his hometown of Akora Khattak in the afternoon.\n- With a boarding school and a high school with thousands of students, as well as 12 affiliated smaller madrassas, offering an eight-year Master of Arts in Islamic studies followed by a PhD after two additional years, journalist Ahmed Rashid, who calls it the most popular madrassa in northern Pakistan, also notes its strict selection process : in February 1999, out of 15,000 applicants only 400 new places were offered, while there are reserved places for 400 Afghan students as well.\n\nSummary sentence:\nDarul Uloom Haqqania or Jamia Dar al-Ulum Haqqania is an Islamic Seminary (darul uloom or madrasa) in the town of Akora Khattak, Khyber Pakhtunkhwa province, northwestern Pakistan.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qbbdbbd410a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2003, Bose entered mainstream Bollywood cinema with \"Jhankaar Beats\" in which he played one of two friends, R.D. Burman fans who are obsessed with winning a music competition.\n- He starred in \"Chameli\" opposite Kareena Kapoor, playing a wealthy chain-smoking Mumbai banker who is stranded in the monsoon rains with a prostitute.\n- With his next effort, the romantic comedy \"Pyaar Ke Side Effects\", Bose moved once more into mainstream Bollywood cinema.\n- Sherawat and Bose also starred together in another Bollywood comedy, \"Maan Gaye Mughal-e-Azam\" (2008), which was a commercial and critical failure.\n- Bose also appeared in \"Shaurya\", a military court room drama modelled on the American film \"A Few Good Men\".\n\nSummary sentence:\nHe has also appeared in films such as \"Pyaar Ke Side Effects\", \"Maan Gaye Mughal-e-Azam\", \"Jhankaar Beats\", \"Chameli\" and \"Shaurya\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf5ce4b83dd",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- While Fredriksson received treatment for her illness, Gessle continued with his solo work.\n- With \"Son of a Plumber\", he continued his association with other Swedish artists.\n- Released in November 2005, the album contains a song dedicated to Gessle's father who was a plumber, \"Kurt – The Fastest Plumber in the West\".\n- In June 2007, he released another solo album in Swedish with the name \"En händig man\", which shipped three times platinum.\n- \"Party Crasher\" his seventh solo album and third in English was released in late 2008.\n\nSummary sentence:\nWith Fredriksson's continued treatment and recuperation he made three more albums, \"Son of a Plumber\" (2005), \"En händig man\" (\"A handy man\", 2007) and \"Party Crasher\" (2008).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q293ae0a4f0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- As a co-founder of the Nazareth-Conferences he has been part of the so-called staff since 1994, a position he maintained in subsequent conferences under the auspices of \"Partners in Confronting Collective Atrocities (PCCA)\".\n\nSummary sentence:\nErlich is one of the co-founders of the Nazareth-Conferences.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc7915d86ad",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He was elected an alternate member of the 19th Central Committee of the Communist Party of China in 2017.\n- In March 2018, he was transferred from Baowu to the provincial government of Hubei and appointed deputy party secretary of the province.\n- On 20 July 2018, he received the additional appointment as party secretary of Wuhan, the city's top official.\n- On February 13, 2020, Ma was removed from his posts as Deputy Communist Party Secretary of Hubei and Communist Party Secretary of Wuhan.\n\nSummary sentence:\nHe had served as Deputy Communist Party Secretary of Hubei province and Communist Party Secretary of Wuhan from 2018 to 2020.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc2133f6dd2",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Sarah Michelle Gellar\n- Gellar was born on Long Island, New York.\n- Gellar took a two-year hiatus from acting following the birth of her daughter in 2009, and in 2011, she signed to star and work as executive producer for a new drama titled \"Ringer\", in which she played the dual role of twin sisters, one of whom is on the run and manages to hide by assuming the wealthy life of the other.\n- In October 2015, Gellar, along with entrepreneurs Galit Laibow and Greg Fleishman, co-founded Foodstirs, a startup food crafting brand selling via e-commerce and retail easy to make organic baking mixes and kits for families.\n\nSummary sentence:\nSarah Michelle Prinze ( ; born April 14, 1977) is an American actress, producer, and entrepreneur.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qcf8deb5183",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Our Lady of Guadalupe Catholic School (Houston)\n- The students, as of 2010, originated from 46 ZIP codes in Greater Houston.\n- The Roman Catholic Archdiocese of Galveston-Houston annually gives $130,000 in tuition assistance to OLG students.\n\nSummary sentence:\nOur Lady of Guadalupe Catholic School is a Roman Catholic school in Houston, Texas.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q4b77c2c2b1",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On November 8, 2016, Avakian lost his bid for Oregon Secretary of State to Republican Dennis Richardson, the first time a Republican was elected to statewide office in Oregon since 2002.\n\nSummary sentence:\nIn 2016, he was the Democratic nominee for Oregon Secretary of State and was defeated by former state representative Dennis Richardson.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf7c247eed6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2004, he first appeared in the Malayalam film, the Jayaraj-directed vigilante film \"4 The People\", portraying one of the four protagonists.\n\nSummary sentence:\nHe first appeared in the Jayaraj-directed Malayalam vigilante film \"4 the People\" (2004).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q66554622bf",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The African-American community worked to gain support from the city for their school as a public school, and the city started to contribute some funds in 1812.\n- The city used part of his legacy to construct the school building next to the African Meeting House, commissioning Richard Upjohn as architect, in his first public project.\n\nSummary sentence:\nDesigned by Richard Upjohn as his first public project, this was the first public school for free blacks.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2da9894ad4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The school began offering International Baccalaureate courses in 1973, which makes it the oldest IB school in Africa, and in 1977 became the first school in Africa to introduce the International Baccalaureate Diploma.\n\nSummary sentence:\nIt was the first school to introduce the International Baccalaureate to the continent, in 1977.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q0ad8d59aeb",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Rob Younger\n- Rob Younger was lead vocalist of the Rats in 1974 alongside Warwick Gilbert on guitar, Mick Lynne, Ron Keeley on drums and Carl Rourke on bass guitar.\n- Fellow Australian musician, and some-time rock music journalist, Vince Lovegrove, observed, \"[they] turned the volume up full bore on their amplifiers, screamed out about revolution into the microphones, raised clenched fists in the air and in the process heralded in a brand new era for Australian rock'n'roll music.\"\n- In 1980 Younger was involved in production work on a four-track extended play, \"The Visitors\", by local punk group of the same name – which included former band mates Hoyle, Keeley and Tek.\n- The line-up never performed live but released a single, \"Face a New God\" (1981), which was co-written by Younger and Callaway.\n\nSummary sentence:\nRob Younger is an Australian rock musician, vocalist, songwriter and producer.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q5f55ce5656",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Beaumont College\n- For seven years it housed Jesuit novices of the (then) English province and on 10 October 1861 became a Catholic boarding school for boys, with the title of St. Stanislaus College, Beaumont, the dedication being to St. Stanislaus Kostka.\n- Beaumont thus became, along with Stonyhurst College in Lancashire and St Aloysius' College, Glasgow, one of three public schools maintained by the English Province of the Jesuits.\n- It finally shut in 1967, amid a storm of protest from parents and old boys who had been contributing to an appeal to fund an extension of the laboratories.\n\nSummary sentence:\nBeaumont College was between 1861 and 1967 a public school.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd56dcbbd40",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Originally introduced by DxO Labs, Analyzer is now a product of DxOMark, which has been separated from DxO.\n\nSummary sentence:\nDxOMark was originally owned by DxO Labs.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qa97992c31f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Johnson is housed entirely in Sage Hall, a 19th-century High Victorian Gothic building which was originally built as a women's dormitory.\n\nSummary sentence:\nThe school is housed in Sage Hall and supports 58 full-time faculty members.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q947ace6c1f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He then transferred to Ole Miss, again transferred to the University of Tennessee at Martin, and again transferred to the Mississippi Valley State.\n\nSummary sentence:\nHe played college football at Tennessee-Martin.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q9d50aa18b9",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- They quickly became a popular group in Sweden, but after their fourth album, \"The Heartland Café\" (1984), sold poorly compared to their previous albums, the group disbanded.\n\nSummary sentence:\nThe band released three number-one albums during the early 1980s but disbanded shortly after their fourth album, \"The Heartland Café\" (1984).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q42fa63679c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On 6 July 2013, Prescott revealed in a newspaper column that he had resigned from the Privy Council in protest against the delays to the introduction of press regulation.\n\nSummary sentence:\nPrescott resigned from the Privy Council in 2013 to protest delays to the introduction of press regulation.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q77f2efce78",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- She began her career as a freelance journalist in 1966 and had articles published in \"The Economic Times\", \"The Indian Express\" and many other periodicals.\n\nSummary sentence:\nAs a freelance journalist, she has been writing extensively on films, theatre, art and feminist issues, for publications of The Times Group, \"The Telegraph\", \"The Hindu\" and \"The Indian Express\" .",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qae88073d1f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- David Lawrence Schwimmer\n- Schwimmer was born in Flushing, Queens, New York City, to attorneys Arthur (born 1941) and Arlene Coleman-Schwimmer (born 1940).\n- In 1994, Schwimmer was cast as Ross Geller in NBC's situation comedy \"Friends\", a series that revolved around a group of friends who live near each other in Manhattan.\n- During the lengthy run of \"Friends\", Schwimmer directed ten of the show's episodes.\n\nSummary sentence:\nDavid Lawrence Schwimmer is an American actor, comedian and director.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd20f5c9c0e",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Svaty and his wife, Kimberly, own and operate Free State Farms, a crop and livestock operation in Ellsworth County.\n\nSummary sentence:\nHe and his wife own a farm in Ellsworth County, Kansas.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qe18e56b586",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Mireya Moscoso\n- Moscoso was born into a poor family in Pedasí, Panama, as the youngest of six children.\n- Moscoso took office on September 1, 1999.\n- Because she was divorced when she assumed the presidency, her older sister Ruby Moscoso de Young served as her First Lady.\n- Herself barred by the Constitution of Panama from a second consecutive term, Moscoso was succeeded by her former rival Martín Torrijos in the 2004 election.\n\nSummary sentence:\nMireya Elisa Moscoso Rodríguez de Arias (born July 1, 1946) is a Panamanian politician who served as the President of Panama from 1999 to 2004.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb55d68eb35",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- April 2000 Gambian student massacre\n- GAMSU decided to hold their protest march on 10 April 2000, and 'thousands' reportedly gathered outside the Gambia Technical Training Institute intending to march towards the Banjul city centre.\n- The police then reacted by opening fire on the protesters with live ammunition.\n- They killed 16 people, 14 of whom were students, as well as a journalist and Red Cross volunteer, Omar Barrow, and a three-year-old child.\n\nSummary sentence:\nThe April 2000 Gambian student massacre was the killing of 14 people by Gambian police officers on 10 April 2000 at a student protest in Banjul, the Gambia.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 }
]
