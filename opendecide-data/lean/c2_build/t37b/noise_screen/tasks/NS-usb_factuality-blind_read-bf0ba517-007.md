# Replay noise screen blind read NS-usb_factuality-blind_read-bf0ba517-007 (family NS-usb_factuality)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-usb_factuality-blind_read-bf0ba517-007.json

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
  "qid": "qad78cdc4bc",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1975, Benigni had his first theatrical success with \"Cioni Mario di Gaspare fu Giulia\", written by Giuseppe Bertolucci.\n- His first film was 1977's \"Berlinguer, I Love You\" (\"Berlinguer ti voglio bene\"), also by Bertolucci.\n\nSummary sentence:\nBenigni made his acting debut in 1977's \"Berlinguer, I Love You\", which he also wrote, and which was directed by Giuseppe Bertolucci.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc60215af2f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- From 2004 to 2008 Schewel was a member, and Vice-Chair, of the Durham Public Schools Board of Education.\n- He was elected to the Durham City Council in 2011 and served until 2017.\n- While serving on the city council, Schewel was an outspoken critic of North Carolina Amendment 1 and introduced a city resolution to support same-sex marriage.\n- He left office on December 6, 2021, succeeded as Mayor of Durham by Elaine O'Neal.\n\nSummary sentence:\nHe is the former Mayor of Durham, North Carolina and formerly served on the Durham City Council and as the Vice Chair of the Durham Public School Board.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q6c5f0e9800",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In May 2019, Pérez was elected to serve as the Prefect of the Azuay Province.\n\nSummary sentence:\nIn May 2019, he was elected as Provincial Prefect of the Azuay Province.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q118d81dd60",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- It was announced on July 7, 2008, that Coates would be inducted into the New England Patriots Hall of Fame.\n\nSummary sentence:\nHe was inducted to the New England Patriots Hall of Fame in 2008.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd0acec67b2",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Smith was appointed a Government Whip in 2001, before being promoted to Parliamentary Under Secretary of State for Northern Ireland in October 2002.\n- On 28 June 2007, Smith was appointed as a Parliamentary Private Secretary to the new Prime Minister Gordon Brown, entitling her to attend Cabinet.\n\nSummary sentence:\nSmith served in government as an Assistant Whip from 2001 to 2002 and a Parliamentary Under-Secretary of State from 2002 to 2007.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf51f9effd1",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Marcia Anne Cross\n- Cross was born in Marlborough, Massachusetts, and is of English and Irish descent.\n- Cross began her television career in 1984 on the soap opera \"The Edge of Night\", playing the recurring role of Liz Correll.\n\nSummary sentence:\nMarcia Anne Cross is an American actress.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qdaf8cb83d4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On November 20, 2015, Chapman released \"Greatest Hits\", consisting of 18 tracks including the live version of \"Stand by Me\", the album is Chapman's first global compilation release.\n\nSummary sentence:\nThe remastered compilation album \"Greatest Hits\", which was curated by Chapman herself, was released in 2015.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qf618dda8ad",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Travis had the leading role of psychology professor Dr. Joyce Reardon in 2002's four-hour television adaptation of \"Stephen King's Rose Red\".\n- In 2002, Travis joined the cast of the CBS sitcom \"Becker\" as Chris Connor.\n- She starred in the show for its final two seasons, replacing the series' original female lead, Terry Farrell.\n\nSummary sentence:\nIn 2002, she played a leading role in \"Rose Red\", and later joined the cast of the CBS sitcom \"Becker\" for its final two seasons.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q46c2f43e9a",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- His third film \"Jashnn\" was also with Mukesh Bhatt and his performance in the film was critically acclaimed.\n\nSummary sentence:\nSuman's was praised for his performance in the 2009 Mukesh Bhatt film \"Jashnn\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc3a634ca92",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Richard David Gill\n- He studied mathematics at the University of Cambridge (1970–1973), and subsequently followed the Diploma of Statistics course there (1973–1974).\n- Marrying a Dutch woman, he moved to the Netherlands where he worked from 1974 to 1988 at the Mathematical Centre (later renamed \"Centrum Wiskunde & Informatica\", or CWI) of Amsterdam.\n\nSummary sentence:\nRichard David Gill is a mathematician who has lived in the Netherlands since 1974.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q6a052ea633",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In February 2020, Young co-founded the Free Speech Union.\n\nSummary sentence:\nHe is the founder of The Free Speech Union.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qb64a7799cf",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After leaving parliament, Purnell became the chair of the Institute for Public Policy Research.\n- Purnell became linked with the Blue Labour movement within the Labour Party and in April 2011 he was appointed by the Boston Consulting Group as a Special Advisor to their Public Sector Group.\n\nSummary sentence:\nPurnell chaired the Institute for Public Policy Research and was a senior advisor in the Public Sector practice of the Boston Consulting Group.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc338665fd1",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Julie Bowen Luetkemeyer\n- Bowen was born in Baltimore, Maryland, the second of three daughters of Suzanne (\"née\" Frey) and John Alexander Luetkemeyer Jr., a commercial real estate developer.\n- From 2009 to 2020, Bowen starred as Claire Dunphy on the ABC sitcom \"Modern Family\".\n\nSummary sentence:\nJulie Bowen Luetkemeyer is an American actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q0d7032877f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Zhou received the Best Actress award at the 53rd Golden Horse Awards together with her \"Soul Mate\" co-star Sandra Ma, and also won Best Actress at the 28th Hong Kong Film Critics Society Award.\n\nSummary sentence:\nShe won the Golden Horse Award for Best Actress with her performance in \"Soul Mate\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q27783fa2dc",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He signed with the Atlanta Falcons as a free agent, and played for Atlanta as a linebacker from 1976 through 1980.\n\nSummary sentence:\nMcClain played for the Atlanta Falcons of the National Football League from 1976 through 1980.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q81f3c36b17",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Brenda Blethyn\n- Born in Ramsgate, Kent, Blethyn was the youngest of nine children in a Roman Catholic, working-class family.\n- Her mother, Louisa Kathleen (née Supple; 10 May 1904 – 1992), was a housewife and former maid, who met Blethyn's father, William Charles Bottle (5 March 1894–c. 1984) in approximately 1922 while working for the same household in Broadstairs, Kent.\n- By the time Blethyn was born in 1946, her three eldest siblings, Pam, Ted and Bernard, had already left home.\n- After winning the London Critics' Circle Theatre Award for Best Supporting Actress (for \"Steaming\") in 1980, Blethyn made her screen debut, starring in the play \"Grown Ups\" as part of the BBC's \"Playhouse\" strand.\n\nSummary sentence:\nBrenda Blethyn (\"née\" Bottle; born 1946) is an English actress.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q722b031d7d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The 1959 earthquake is also the most severe earthquake in the Rocky Mountain area of the United States along with the 6.9 magnitude earthquake which struck Idaho in 1983.\n- The landslide caused by this quake was the largest since an earthquake in Wyoming in 1925 caused a landslide amounting to 50 million cubic yards (38 million cubic meters) of rock and debris that left 28 people dead.\n\nSummary sentence:\nIt also caused the largest landslide in the Rocky Mountain area of the United States since 1925.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc2008d6a6f",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After leaving parliament, Purnell became the chair of the Institute for Public Policy Research.\n- Purnell became linked with the Blue Labour movement within the Labour Party and in April 2011 he was appointed by the Boston Consulting Group as a Special Advisor to their Public Sector Group.\n\nSummary sentence:\nPurnell chaired the Institute for Public Policy Research until 2010, and was a senior advisor in the Public Sector practice of the Boston Consulting Group.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q7cbdd9bb43",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- LLC is a television production company created by Jon Favreau on August 30, 2018.\n- The company most recently produced \"The Mandalorian\" and \"The Book of Boba Fett\" television shows in partnership with Lucasfilm.\n\nSummary sentence:\nHe also serves as a writer and executive producer for its spin-off series \"The Book of Boba Fett\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q5598c1a839",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Raniero Cantalamessa\n- Raniero Cantalamessa was born in Colli del Tronto, Italy, on 22 July 1934.\n- He was ordained as a priest in the Franciscan Capuchin order in 1958.\n- He holds doctoral degrees in theology and classical literature.\n- On 25 October 2020, Pope Francis announced he would raise him to the rank of cardinal at a consistory scheduled for 28 November 2020.\n\nSummary sentence:\nRaniero Cantalamessa (born 22 July 1934) is an Italian Catholic cardinal and priest in the Franciscan Capuchin order and a theologian.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q31987c2306",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- President Donald Trump announced in a press conference on February 16, 2017, that he would nominate Acosta to fill the position of Secretary of Labor after the nomination of Andrew Puzder was withdrawn.\n- On April 27, 2017, Acosta was confirmed as Secretary of Labor by the U.S. Senate in a 60–38 vote.\n\nSummary sentence:\nPresident Donald Trump nominated Acosta to be Labor Secretary on , and he was confirmed by the U.S. Senate on .",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qe3cb60e1bb",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Tryon M. Williams\n- Born in Montreal, Quebec, he traveled to western Canada early in life.\n- Williams resigned from IBM in 1978 to found Canada's first public software company, Sydney Development Corporation (SDC), The company developed an online real-time project management system for mainframe computers, then business applications for minicomputers.\n\nSummary sentence:\nTryon M. Williams is a Canadian businessman.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q539441fbe5",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Smith was appointed a Government Whip in 2001, before being promoted to Parliamentary Under Secretary of State for Northern Ireland in October 2002.\n- On 28 June 2007, Smith was appointed as a Parliamentary Private Secretary to the new Prime Minister Gordon Brown, entitling her to attend Cabinet.\n\nSummary sentence:\nSmith served in government as a Whip from 2001 to 2002 and a Parliamentary Under-Secretary of State from 2002 to 2007.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb1bfc30145",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- As Minister for Health Plibersek established \"Grow Up Smiling\", a $4 billion package to support better dental care for children, which expanded Medicare-subsided dental check-ups for children from age 2 to 17.\n- Plibersek was unanimously elected deputy leader of the Labor Party (and thus Deputy Leader of the Opposition) on 14 October 2013, following the leadership election that had seen Bill Shorten succeed Kevin Rudd as leader.\n\nSummary sentence:\nShe became Minister for Health.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q20dc7632c7",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Dubin was described in \"New York Magazine\" in 1998 as one of the city's social leaders who were \"all born after the baby boom and free of its disdain for old conventions\", and was a member of the \"uptown A-listers\" including Prince Alexander von Fürstenberg, Pia Getty, The Crown Princess of Greece, and fashion designer Carolina Herrera Jr.\n\nSummary sentence:\nHe was described by \"New York Magazine\" as being one of the \"new generation of uptown A-listers\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf607886aaa",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He finished the 2015–16 season leading the Lakers and all rookies in steals per game, and became the youngest player to hit 130 three-pointers in a season.\n- He subsequently earned NBA All-Rookie Second Team honors.\n\nSummary sentence:\nHe was named to the NBA All-Rookie Second Team with the Lakers in 2016.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q1d4013721d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Shepley played five seasons at UBC as an offensive lineman.\n\nSummary sentence:\nShepley played university football with the UBC Thunderbirds.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q31b4de81a6",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- WIS is a member school of the English Schools Foundation.\n\nSummary sentence:\nThe school is a member of the English Schools Foundation.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qb303a9fed4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After joining International Murex, in 1987 he returned to Distinctive Software, a spin-off from SDC, as president.\n- Williams was instrumental in growing Distinctive with Don Mattrick and Paul Lee, before it was bought by Electronic Arts for $11 million in 1991 (equivalent to $22 million in 2021), and then helping Electronic Arts (Canada) develop into a 125-person organization with a management team that reported revenue of $31 million (Canadian) in fiscal year 1993.\n\nSummary sentence:\nFrom 1987 to 1991 he was President and CEO of Distinctive Software Inc. of Vancouver.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q3534154479",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Military police recruit training puts a special emphasis on discipline.\n\nSummary sentence:\nThe corps puts an emphasis on discipline.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q1e3ea8c458",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Nancy Travis\n- Travis was born in Queens, the daughter of Theresa, a social worker, and Gordon Travis, a sales executive.\n- From 1995 to 1997, Travis played a leading role in the CBS sitcom \"Almost Perfect\".\n\nSummary sentence:\nNancy Travis is an American actress.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q852415f8d5",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He soon left the law firm, founding the Bus Project in 2001.\n- In 2008, Smith was elected with no opposition to the Oregon House of Representatives representing House District 47.\n\nSummary sentence:\nHe is a founder of the Bus Project, and served in the Oregon House of Representatives, representing District 47, elected in 2008.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qd1fdf39fae",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- After that, Travis appeared in a stage version of Neil Simon's \"Brighton Beach Memoirs\" and was a founding member of the Off-Broadway theater company \"Naked Angels\".\n\nSummary sentence:\nShe began her career on Off-Broadway theater.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q88ef215d77",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Comedy Central's original series \"Workaholics\" premiered on April 6, 2011, and stars Devine, Anderson, and Holm and co-stars Newacheck, all of whom also serve as series creators and executive producers.\n- He stars in his own Comedy Central series, \"Adam Devine's House Party\", which debuted in October 2013.\n\nSummary sentence:\nHe is one of the stars and co-creators of the Comedy Central comedy television series \"Workaholics\" and \"Adam Devine's House Party\".",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q440ce375be",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He played well, and further performances against Scotland and Yugoslavia secured him a place in the squad for the 1966 FIFA World Cup.\n- Hurst reached the German penalty box and fired a powerful shot in the expectation that it would sail over the crossbar and waste time as the match drew to a close; the ball instead struck a divot as it bounced in front of Hurst and the shot connected well enough to beat the goalkeeper and hit the net to end the game at 4–2 to England.\n- Hurst was selected for UEFA Euro 1968, but did not play as England lost 1–0 to Yugoslavia in the semi-final.\n- Hurst scored his second international hat-trick on 12 March 1969, in a 5–0 victory over France, and was named in the Ramsey squad which played in Mexico to defend the World Cup in 1970.\n\nSummary sentence:\nAs well as success in the 1966 World Cup he also appeared at UEFA Euro 1968 and the 1970 FIFA World Cup.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q4e5208bd64",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2010 he becomes the host of the show \"ONE2FIVE\" at The X 103.9 FM in Colombia.\n\nSummary sentence:\nHe is the host of the radio show ONE2FIVE on The X 103.9 FM Colombia.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc003c086c7",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 1982, uneasy about the Alliance, Owen challenged Jenkins for the leadership of the SDP, but was defeated by 26,256 votes to 20,864.\n- In the following year's General Election, the Alliance gained 25% of the vote, only slightly behind the Labour Party, but because of the first-past-the-post voting system, it won only 23 out of 650 seats.\n- Although elected, Jenkins resigned the SDP leadership and Owen succeeded to it without a contest among the six remaining SDP MPs.\n- Owen is widely regarded as having been, at the very least, a competent party leader.\n- The Liberal Party and SDP merged to form the Social and Liberal Democrats (SLD) in March 1988, renamed the Liberal Democrats in October 1989.\n- At the request of two of the remaining SDP MPs, John Cartwright and Rosie Barnes, Owen continued to lead a much smaller continuing SDP, with three MPs in total.\n- The party polled well at its first election, its candidate coming a close second in the 1989 Richmond by-election, but thereafter a string of poor and ultimately disastrous by-election results followed, including coming behind the Official Monster Raving Loony Party in the Bootle by-election of May 1990, prompting Owen to wind up the party in 1990.\n\nSummary sentence:\nOwen led the Social Democratic Party from 1983 to 1988, and the continuing SDP from 1988 to 1990.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q2672c2915d",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Kenchi Tachibana\n- Kenchi was born on September 28, 1979, in Yokohama, Japan and grew up in Yokosuka, Kanagawa Prefecture.\n- He became an active dancer in his youth and joined dance teams such as Poly-3, Fulcrum and Red Blockerz in his early 20s.\n- ※His roles in bold are his starring works\n\nSummary sentence:\nKenichiro Teratsuji (寺辻健一郎; \"Teratsuji Kenichiro\", born September 28, 1979 in Yokohama, Japan), better known by his stage names Kenchi Tachibana (橘ケンチ) or simply KENCHI, is a Japanese dancer and actor.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qc808162f2c",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The African-American community worked to gain support from the city for their school as a public school, and the city started to contribute some funds in 1812.\n- The city used part of his legacy to construct the school building next to the African Meeting House, commissioning Richard Upjohn as architect, in his first public project.\n\nSummary sentence:\nDesigned by Richard Upjohn as his first public project, this was a public school for blacks.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q33e58be9a0",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In January 1951, McDivitt joined the United States Air Force (USAF).\n- He flew 145 combat missions in Korea in F-80 Shooting Stars and F-86 Sabres with the 35th Fighter-Bomber Squadron, and earned two Distinguished Flying Crosses.\n\nSummary sentence:\nHe joined the USAF in 1951 and flew 145 combat missions in Korea.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qf285d4887b",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Siaolin Village\n- Nearly 150 years later, some Taivoan people from Aliguan in Kaohsiung further migrated to a river terrace 10 km (6.2 mi) to the north of Aliguan for hunting.\n- During the Japanese Occupation Period, in order to have Taivoan people counter the Mountain Indigenous people so as to control the camphor forest in Jiasian and Namasia, Japanese government collectively moved more Taivoan people to the river terrace, which later became Siaolin Village in 1904, said to be named after the family name of the local Japanese police officer Kobayashi (Hiragana: こばやし; ).\n- Siaolin is the largest village within Jiasian District, covering the northern half of the district.\n- The heavy rainfall caused landslides in mountainous regions in southern Taiwan, especially Jiasian, Liouguei, Taoyuan, and Namasia districts.\n\nSummary sentence:\nSiaolin Village is a village in Jiasian District, Kaohsiung, Taiwan.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q9e3b11bbb9",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- The King Air took off from Concord, North Carolina, at 12 pm EST, carrying eight passengers and two flight crew.\n\nSummary sentence:\nThe aircraft was transporting eight passengers and two flight crew.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q4583aec0ad",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- 1972's \"Sail Away\" reached No. 163 on \"Billboard\", with the title track making its way into the repertoire of Ray Charles and Linda Ronstadt.\n- His 1974 release \"Good Old Boys\" was a set of songs about the American South.\n- \"Little Criminals\" (1977) contained the surprise hit \"Short People\", which also became a subject of controversy.\n- He released four albums of new material as a singer-songwriter since that time: \"Land of Dreams\" (1988), \"Bad Love\" (1999), \"Harps and Angels\" (2008), and \"Dark Matter\" (2017).\n\nSummary sentence:\nFour of Newman's non-soundtrack albums have charted in the US top 40: \"Sail Away\" (1972), \"Good Old Boys\" (1974), \"Little Criminals\" (1977), and \"Harps and Angels\" (2008).",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q18e736e3fe",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- On August 22, 2019, Hasbro announced its purchase of Entertainment One for about US$4 billion.\n\nSummary sentence:\nIt is the parent of Entertainment One.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q26052cd552",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He has taught classes at Drury University along with Missouri State University on this topic.\n\nSummary sentence:\nHe has also taught classes at Missouri State University and at Drury University.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qcbd489b8ec",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- Thomas William Selleck\n- Selleck was born in Detroit, Michigan, in 1945, to housewife Martha Selleck and Robert Dean Selleck, who was an executive and real estate investor.\n- Selleck's big break came when he was cast in the lead role as Thomas Magnum in \"Magnum, P.I.\"\n\nSummary sentence:\nThomas William Selleck (born 1945) is an American actor.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "q376e8c6571",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- From 1967 to 1983 and from 1987 to 1999 he held a seat at the Swiss National Council.\n\nSummary sentence:\nHe was previously Member of the Swiss Parliament for the Social Democrats from 1981 to 1999.",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 },
 {
  "qid": "qc627aeaa08",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- He later withdrew from the race when he was appointed by governor Ted Kulongoski to be Commissioner of the Oregon Bureau of Labor and Industries in early 2008 after Dan Gardner announced his resignation.\n\nSummary sentence:\nHe was appointed Labor Commissioner by Governor Ted Kulongoski on April 8, 2008 and subsequently elected statewide on November 4, 2008.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "qffd28b40f4",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2013 he started hosting the television show \"Aldea TIC\" on Canal Tr3ce, a show about technology and entertainment.\n\nSummary sentence:\nIn 2013, he started to host the television show Aldea TIC on Canal Tr3ce.",
  "question": "Does the summary sentence contain any information that the evidence sentences do not support?",
  "definitions": "- yes: At least one detail of the sentence (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality.\n- no: Every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; nothing is added beyond them."
 },
 {
  "qid": "q9bff2a4502",
  "kind": "yes/no",
  "text": "Evidence sentences (from the article):\n- In 2018, Travis was cast as a female lead opposite Michael Douglas and Alan Arkin in the Netflix comedy series \"The Kominsky Method\", created by Chuck Lorre.\n\nSummary sentence:\nFrom 2018 to 2019, she also starred opposite Michael Douglas in the Netflix comedy series \"The Kominsky Method\".",
  "question": "Is every piece of information in the summary sentence supported by the evidence sentences?",
  "definitions": "- yes: Fully supported: every fact in the sentence (names, dates, numbers, roles, places, relations) is stated in or directly implied by the evidence sentences; true-sounding details found only elsewhere do not count as support.\n- no: Not fully supported: at least one detail (e.g. a birth date, middle name, extra role, number, place or qualifier) is absent from or contradicted by the evidence sentences, even if it may be true in reality."
 }
]
