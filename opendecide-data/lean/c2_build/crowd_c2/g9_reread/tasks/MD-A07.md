# G9 re-read (G5-H blind read) MD-A07 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-A07.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 27. Answers expected: 27 (one per item, each with that item's qid).

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
  "qid": "q5955b7ecd3",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Retailers - other\nLocal authority: Wokingham\nRating: 4",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: the rating is 2\n- Group B: the rating is 1\n- Group C: the rating is 4\n- None of these groups: any other is"
 },
 {
  "qid": "qb1e62343d7",
  "kind": "choice",
  "text": "Organization: Orenburg State University\nCountry: Russia",
  "question": "Which period holds the founding year of Orenburg State University (Russia)?",
  "options": [
   "1800-1899",
   "1900-1949",
   "1950-1999",
   "2000 or later"
  ]
 },
 {
  "qid": "qd57fc01bf3",
  "kind": "yes/no",
  "text": "Place: Gradačac\nCountry: Bosnia and Herzegovina",
  "question": "Is Gradačac eligible under this rule?",
  "definitions": "- yes: The place's country is Spain, Bosnia and Herzegovina or United States.\n- no: The place's country is any other country."
 },
 {
  "qid": "q23fea17ad8",
  "kind": "choice",
  "text": "Organization: National Hospital Abuja\nCountry: Nigeria",
  "question": "Which group does National Hospital Abuja fall into under these definitions?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: Russia, Argentina or Denmark\n- Group B: United States, Japan or Nigeria\n- Group C: Belgium, Türkiye or United Kingdom\n- None of these groups: any other country"
 },
 {
  "qid": "q610ba79727",
  "kind": "yes/no",
  "text": "Project ID: 801459\nProgramme: Horizon 2020\nFunding scheme: MSCA-COFUND\nCall topic: MSCA-COFUND-2017\nStart date: 2019-04-01\nEnd date: 2024-03-31\nTotal cost: 7080000 EUR\nEC maximum contribution: 3540000 EUR",
  "question": "Is the EC maximum contribution above 1,000,000 EUR?"
 },
 {
  "qid": "qc95b0ed178",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\n| Field | Value |\n| --- | --- |\n| Azimuthal gap (deg) | 92 |\n| PAGER alert | none |\n| Depth (km) | 107.4 |\n| Felt reports | 2 |",
  "question": "Does the event lie at a depth of less than 35 km?"
 },
 {
  "qid": "q3b49ff957d",
  "kind": "choice",
  "text": "Organization: Shebin Teaching Hospital\nCountry: Egypt",
  "question": "Which type does the registry give for Shebin Teaching Hospital (Egypt)?",
  "options": [
   "healthcare",
   "archive",
   "education",
   "facility"
  ]
 },
 {
  "qid": "q954b2e406e",
  "kind": "yes/no",
  "text": "Catalogue entry for a scholarly work\ncited_by_count: 460\nhas_fulltext: false\nvolume: 28\nvenue: Pattern Recognition Letters",
  "question": "Is the citation count at least 100?"
 },
 {
  "qid": "q52d4084913",
  "kind": "yes/no",
  "text": "Release-group record\n- Title = Geração Bendita\n- Secondary types = Soundtrack\n- Genre tags = rock, psychedelic rock\n- Release group ID = 3a002a00-87ee-3689-8ebb-6645e7919bd1",
  "question": "Does the entry list fewer than 20 characters in the title?"
 },
 {
  "qid": "qd802364228",
  "kind": "yes/no",
  "text": "Title: Tiraz with gold\nAccession number: 1982.109\nObject type: Textile\nCollection: Textiles\nTechnique: plain weave with inwoven tapestry weave: linen, silk, and gold filé\nCulture: Egypt, Fatimid period, reign of Caliph al-Zahir, 1020–1035\nDate text: 1020–35\nDate range: 1020 to 1035\nMeasurements: not listed\nCredit line, first word: Andrew",
  "question": "Does the title have more than 4 words?"
 },
 {
  "qid": "qddac1a4b17",
  "kind": "yes/no",
  "text": "Taxon: Zygopolaris borealis\nKingdom: Fungi\nClass: Kickxellomycetes",
  "question": "Does Zygopolaris borealis meet the rule?",
  "definitions": "- yes: The taxon's class is Malasseziomycetes, Kickxellomycetes or Exobasidiomycetes.\n- no: The taxon's class is any other class."
 },
 {
  "qid": "q238e868822",
  "kind": "choice",
  "text": "Organization: Sépaq\nCountry: Canada",
  "question": "Which group does Sépaq fall into under these definitions?",
  "options": [
   "Group C",
   "None of these groups",
   "Group A",
   "Group B"
  ],
  "definitions": "- Group A: Brazil, Egypt or The Netherlands\n- Group B: Singapore, United States or Finland\n- Group C: Japan, Canada or Mexico\n- None of these groups: any other country"
 },
 {
  "qid": "q876c79e0a3",
  "kind": "choice",
  "text": "Discography database row\n- First release date = 1978-02\n- Secondary types = none\n- Genre tags = rock, electronic, experimental, post-punk, experimental rock, avant-garde, no wave, pop/rock\n- Genre tag count = 8",
  "question": "Which tagging level applies to this entry?",
  "options": [
   "untagged",
   "lightly tagged",
   "richly tagged"
  ],
  "definitions": "- untagged: Pick this when no genre tag is listed.\n- lightly tagged: Pick this for 1 or 2 genre tags.\n- richly tagged: Pick this for 3 or more genre tags."
 },
 {
  "qid": "q79f1b01f7e",
  "kind": "yes/no",
  "text": "Project and operations register row\nboard_approval_date: 2022-06-22\nsupplemental: N\nibrd_usd_m: 0.00\nregion: East Asia and Pacific",
  "question": "Does the board approval year fall before 2015?"
 },
 {
  "qid": "qa49e685a1c",
  "kind": "choice",
  "text": "Organization: Olivet University\nCountry: United States",
  "question": "Which period holds the founding year of Olivet University (United States)?",
  "options": [
   "2000 or later",
   "1950-1999",
   "1900-1949",
   "1800-1899"
  ]
 },
 {
  "qid": "q01f843ffa2",
  "kind": "yes/no",
  "text": "Index record of a publication\noa_status: closed\nlanguage: en\nversion: publishedVersion\nis_retracted: false\npublication_year: 2022",
  "question": "Is the publication year 2010 or later?"
 },
 {
  "qid": "qe130b63705",
  "kind": "choice",
  "text": "City: Bunbury",
  "question": "In which country is the city of Bunbury?",
  "options": [
   "Paraguay",
   "Brazil",
   "Australia",
   "Venezuela"
  ]
 },
 {
  "qid": "q5d311fbc7d",
  "kind": "yes/no",
  "text": "Event summary from a seismic network catalogue\nmagnitude: 4.8\nplace: 103 km NNW of Tatsug?, Japan\nnetwork: us\nevent_id: us7000qcbd\nmagnitude_type: mww",
  "question": "Is the stated distance to the named place below 200 km?"
 },
 {
  "qid": "q759a45beff",
  "kind": "choice",
  "text": "Project ID: 717943\nProgramme: Horizon 2020\nFunding scheme: SME-1\nCall topic: PHC-12-2015-1\nStart date: 2016-03-01\nEnd date: 2016-08-31\nTotal cost: 71429 EUR\nEC maximum contribution: 50000 EUR",
  "question": "Which band holds the total cost (in EUR)?",
  "options": [
   "5 million or more",
   "under 100 thousand",
   "1 million to under 5 million",
   "100 thousand to under 1 million"
  ]
 },
 {
  "qid": "q2a854b3d83",
  "kind": "choice",
  "text": "Bibliographic record\n- Work type = book-chapter\n- Open-access status = closed\n- Distinct institutions = 0\n- First page = 376\n- Last page = 391",
  "question": "Which length class applies to this entry?",
  "options": [
   "short",
   "medium",
   "long"
  ],
  "definitions": "- short: Pick this when the page span (last minus first, plus one) is 1 to 4 pages.\n- medium: Pick this when the span is 5 to 14 pages.\n- long: Pick this when the span is 15 pages or more."
 },
 {
  "qid": "qe1c8ae6ebf",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: School/college/university\nLocal authority: Kingston-Upon-Thames\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group A",
   "None of these groups",
   "Group C",
   "Group B"
  ],
  "definitions": "- Group A: the local authority is Middlesbrough, Gateshead or Newport\n- Group B: the local authority is Mid Sussex, Harborough or Kingston-Upon-Thames\n- Group C: the local authority is Cherwell, Swindon or Chesterfield\n- None of these groups: any other is"
 },
 {
  "qid": "qfc15f6f7aa",
  "kind": "yes/no",
  "text": "Project and operations register row\nProject name: Power Project (05)\nStatus: Closed\nCountry: Jordan\nMajor sectors listed: 1",
  "question": "Is the word 'Climate' part of the project name?"
 },
 {
  "qid": "qd228f5ea40",
  "kind": "yes/no",
  "text": "City: Itabuna\nCountry: Brazil",
  "question": "Is the elevation of Itabuna (Brazil) at most 140 m?"
 },
 {
  "qid": "qaa71feeb31",
  "kind": "choice",
  "text": "City: Sydney\nCountry: Australia",
  "question": "Which time zone does Sydney use?",
  "options": [
   "Pacific/Auckland",
   "Australia/Melbourne",
   "Australia/Sydney",
   "Australia/Brisbane"
  ]
 },
 {
  "qid": "qdac88407fc",
  "kind": "yes/no",
  "text": "Project ID: 790654\nProgramme: Horizon 2020\nFunding scheme: ERC-POC\nCall topic: ERC-2017-PoC\nStart date: 2018-09-01\nEnd date: 2020-02-29\nTotal cost: 149994 EUR\nEC maximum contribution: 149994 EUR",
  "question": "Does the project end after the year 2020?"
 },
 {
  "qid": "qfe279ed062",
  "kind": "yes/no",
  "text": "Event summary from a seismic network catalogue\n- Magnitude = 4.7\n- Contributing network = us\n- Significance score = 340\n- Origin time (UTC) = 2026-06-28 02:39:47",
  "question": "Would it be accurate to say that the event did not fail to occur in January to June (UTC)?"
 },
 {
  "qid": "qed962a649e",
  "kind": "yes/no",
  "text": "City: Baku\nCountry: Azerbaijan",
  "question": "Is Baku the capital city of Azerbaijan?"
 }
]
