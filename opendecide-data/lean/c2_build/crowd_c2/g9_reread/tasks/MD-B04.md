# G9 re-read (G5-H blind read) MD-B04 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-B04.json

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
  "qid": "q8dc0ebacbf",
  "kind": "choice",
  "text": "Bibliographic record\n{\n  \"oa_status\": \"closed\",\n  \"institutions\": 0,\n  \"first_page\": 41,\n  \"last_page\": 58,\n  \"venue\": \"Cambridge University Press eBooks\"\n}",
  "question": "Which length class does this entry fall in?",
  "options": [
   "short",
   "medium",
   "long"
  ],
  "definitions": "- short: Pick this when the page span (last minus first, plus one) is 1 to 4 pages.\n- medium: Pick this when the span is 5 to 14 pages.\n- long: Pick this when the span is 15 pages or more."
 },
 {
  "qid": "q7db2467a5e",
  "kind": "choice",
  "text": "Project ID: 832838\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF\nCall topic: MSCA-IF-2018\nStart date: 2020-03-02\nEnd date: 2023-03-01\nTotal cost: 266425.92 EUR\nEC maximum contribution: 266425.92 EUR",
  "question": "Which quarter of the year does the project start in?",
  "options": [
   "Q3 (July to September)",
   "Q1 (January to March)",
   "Q4 (October to December)",
   "Q2 (April to June)"
  ]
 },
 {
  "qid": "qc7f683bb13",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\n| Field | Value |\n| --- | --- |\n| Significance score | 650 |\n| Event ID | usp000hpc0 |\n| Depth (km) | 10.0 |\n| Latitude | -45.464 |",
  "question": "Does the record show at least 500 significance points?"
 },
 {
  "qid": "q1b40579a18",
  "kind": "yes/no",
  "text": "City: Itabuna\nCountry: Brazil",
  "question": "Is the elevation of Itabuna (Brazil) at most 140 m?"
 },
 {
  "qid": "qef14a3d15c",
  "kind": "yes/no",
  "text": "Music catalogue entry\nFirst release date 1973; Genre tags rock, hard rock, blues rock, classic rock; Disambiguation comment present; Release statuses Official.",
  "question": "Does the entry carry a disambiguation comment?"
 },
 {
  "qid": "q9efb801d00",
  "kind": "yes/no",
  "text": "City: Itamaraju\nCountry: Brazil",
  "question": "Do more than 99,000 people live in Itamaraju (Brazil)?"
 },
 {
  "qid": "qb1652c74d7",
  "kind": "choice",
  "text": "Index record of a publication\nCitation count 188; Authors listed 2; Topic domain Life Sciences; First page 40; Last page 45.",
  "question": "Pick the citation class for this entry.",
  "options": [
   "none",
   "low",
   "moderate",
   "high"
  ],
  "definitions": "- none: Pick this when the citation count is 0.\n- low: Pick this when the count is from 1 to 9.\n- moderate: Pick this when the count is from 10 to 99.\n- high: Pick this when the count is 100 or more."
 },
 {
  "qid": "qa1eeef26ca",
  "kind": "yes/no",
  "text": "Project ID: 883219\nProgramme: Horizon 2020\nFunding scheme: ERC-ADG\nCall topic: ERC-2019-ADG\nStart date: 2021-07-01\nEnd date: 2026-06-30\nTotal cost: 2500000 EUR\nEC maximum contribution: 2500000 EUR",
  "question": "Is the EC maximum contribution above 10,000,000 EUR?"
 },
 {
  "qid": "q865bc1a2a2",
  "kind": "yes/no",
  "text": "Index record of a publication\n- Publication year = 1996\n- Citation count = 0\n- Distinct countries = 0\n- Topic field = Social Sciences\n- Venue name = Hearing Research",
  "question": "Was it published in 2020 or later?"
 },
 {
  "qid": "qb89a2c98aa",
  "kind": "yes/no",
  "text": "Music catalogue entry\nDisambiguation comment none; Genre tags rock, punk; First release date 1983; Title Let the Vultures Fly EP.",
  "question": "Does the genre tag list include 'punk'?"
 },
 {
  "qid": "q52ef4555c7",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nHygiene score: 10\nStructural score: 5\nConfidence in management score: 20",
  "question": "Which score has the smallest value?",
  "options": [
   "structural score",
   "hygiene score",
   "confidence in management score"
  ]
 },
 {
  "qid": "qc28ddc2955",
  "kind": "choice",
  "text": "Organization: State Hydrological Institute",
  "question": "Which country is State Hydrological Institute located in?",
  "options": [
   "Spain",
   "Greece",
   "Russia",
   "United States"
  ]
 },
 {
  "qid": "q211e7136b4",
  "kind": "choice",
  "text": "Project and operations register row\n| Field | Value |\n| --- | --- |\n| Project name | Emergency Flood Reconstruction Project |\n| Region | Middle East and North Africa |\n| Total commitment (USD million) | 10.00 |\n| IDA commitment (USD million) | 10.00 |\n| Board approval date | 1989-12-12 |",
  "question": "Which fiscal quarter of the approval applies to this entry?",
  "options": [
   "FQ1",
   "FQ2",
   "FQ3",
   "FQ4"
  ],
  "definitions": "- FQ1: Pick this for approval in July, August or September.\n- FQ2: Pick this for October to December.\n- FQ3: Pick this for January to March.\n- FQ4: Pick this for April to June."
 },
 {
  "qid": "q4657516e52",
  "kind": "choice",
  "text": "Organization: China National Center for Biotechnology Development",
  "question": "Which country is China National Center for Biotechnology Development located in?",
  "options": [
   "China",
   "Germany",
   "Norway",
   "France"
  ]
 },
 {
  "qid": "q94d42f09af",
  "kind": "yes/no",
  "text": "Project and operations register row\nRegion: South Asia\nCountry: Pakistan\nSupplemental flag: N\nClosing date: 1996-06-30\nProject name: Refinery Energy Conservation & Modernization Project\nBoard approval date: 1987-06-16",
  "question": "Does the closing date fall fewer than 7 calendar years after the approval date?"
 },
 {
  "qid": "q99e1887458",
  "kind": "yes/no",
  "text": "Bibliographic record\n{\n  \"language\": \"en\",\n  \"cited_by_count\": 8,\n  \"domain\": \"Social Sciences\",\n  \"first_page\": 105258,\n  \"last_page\": 105258\n}",
  "question": "Does the page range cover fewer than 10 pages (last minus first, plus one)?"
 },
 {
  "qid": "q1d8caedc16",
  "kind": "yes/no",
  "text": "Catalogue entry for a scholarly work\nTopic field Immunology and Microbiology; Distinct institutions 0; Citation count 0; Language code fr.",
  "question": "Does the record give 'fr' as the language code?"
 },
 {
  "qid": "q5404be2e16",
  "kind": "choice",
  "text": "Taxon: Lithothamnion laminosum\nKingdom: Plantae\nClass: Florideophyceae",
  "question": "Which group does Lithothamnion laminosum fall into under the definitions?",
  "options": [
   "None of these groups",
   "Group B",
   "Group A",
   "Group C"
  ],
  "definitions": "- Group A: the class is Bangiophyceae, Chlorophyceae or Langiophytopsida\n- Group B: the class is Glaucophyceae, Compsopogonophyceae or Polytrichopsida\n- Group C: the class is Klebsormidiophyceae, Liliopsida or Florideophyceae\n- None of these groups: any other is"
 },
 {
  "qid": "q3b28c538f5",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nLocal authority: Derby City\nRating: 2",
  "question": "Does this establishment meet the rule?",
  "definitions": "- yes: The business type is Takeaway/sandwich shop, Retailers - other or School/college/university.\n- no: The business type is any other type."
 },
 {
  "qid": "q2d94e5497f",
  "kind": "yes/no",
  "text": "Project ID: 954905\nProgramme: Horizon 2020\nFunding scheme: SME-2\nCall topic: EIC-SMEInst-2018-2020\nStart date: 2020-05-01\nEnd date: 2022-10-31\nTotal cost: 2292875 EUR\nEC maximum contribution: 1605012.5 EUR",
  "question": "Does the project start in the first half of a year, January to June?"
 },
 {
  "qid": "qa460993b52",
  "kind": "yes/no",
  "text": "Kingston, Jamaica",
  "question": "Does Jamaica have Kingston as its capital?"
 },
 {
  "qid": "q8845985db9",
  "kind": "yes/no",
  "text": "Organization: Push to Walk",
  "question": "Is the country of Push to Walk United States?"
 },
 {
  "qid": "q03389c67b2",
  "kind": "choice",
  "text": "Organization: Bartlett Public Library District\nCountry: United States",
  "question": "Which type does the registry give for Bartlett Public Library District (United States)?",
  "options": [
   "education",
   "archive",
   "company",
   "facility"
  ]
 },
 {
  "qid": "qe2b5ae889f",
  "kind": "choice",
  "text": "Taxon: Polyplacotomidae\nKingdom: Animalia",
  "question": "To which phylum does the taxon Polyplacotomidae belong?",
  "options": [
   "Placozoa",
   "Brachiopoda",
   "Acanthocephala",
   "Arthropoda"
  ]
 },
 {
  "qid": "qc00566dbe1",
  "kind": "yes/no",
  "text": "Accession number: 1919.1016\nObject type: Painting\nCollection: American - Painting\nTechnique: oil on canvas\nCulture: America\nDate text: c. 1758\nDate range: 1753 to 1763\nMeasurements: Framed: 121.9 x 97.2 x 7.6 cm (48 x 38 1/4 x 3 in.); Unframed: 107 x 84 cm (42 1/8 x 33 1/16 in.)\nCredit line, first word: Gift",
  "question": "Is the unframed height above 60 cm?",
  "definitions": "- yes: the first number of the unframed size (height) is greater than 60 cm.\n- no: the first number of the unframed size is 60 cm or less."
 },
 {
  "qid": "qb4df04be8c",
  "kind": "choice",
  "text": "Accession number: 1968.34\nObject type: Sculpture\nCollection: MED - Romanesque\nTechnique: limestone\nCulture: Western France, Bordelais, early 12th century\nDate text: early 1100s\nDate range: 1100 to 1125\nMeasurements: not listed\nCredit line, first word: Purchase",
  "question": "Which group does the object type belong to?",
  "options": [
   "metal, ceramic and glass wares",
   "sculpture and carving",
   "textiles and dress",
   "paintings",
   "furniture and other objects",
   "works on paper and books"
  ],
  "definitions": "- paintings: object types Painting, Portrait Miniature\n- works on paper and books: object types Print, Drawing, Photograph, Portfolio, Manuscript, Bound Volume, Calligraphy\n- sculpture and carving: object types Sculpture, Ivory, Jade, Stone, Mask, Glyptic, Wood\n- textiles and dress: object types Textile, Lace, Embroidery, Garment, Tapestry, Velvet, Basketry, Leather\n- metal, ceramic and glass wares: object types Ceramic, Metalwork, Arms and Armor, Jewelry, Coins, Glass, Silver, Enamel, Lacquer, Vessels, Lamp\n- furniture and other objects: object types Furniture and woodwork, Funerary Equipment, Miscellaneous, Musical Instrument, Tools and Equipment"
 },
 {
  "qid": "qa9521914da",
  "kind": "choice",
  "text": "Organization: Universidad Autónoma de La Laguna",
  "question": "Which country is Universidad Autónoma de La Laguna located in?",
  "options": [
   "Guyana",
   "North Macedonia",
   "Indonesia",
   "Mexico"
  ]
 },
 {
  "qid": "qb86690e3c8",
  "kind": "yes/no",
  "text": "Music catalogue entry\n{\n  \"release_group_id\": \"638f2355-6414-46b2-a37a-f57ee012fe83\",\n  \"title\": \"SIGMA HARMONICS Original Soundtrack\",\n  \"first_release_date\": \"2008-09-24\",\n  \"primary_type\": \"Album\",\n  \"statuses\": \"Official, Pseudo-Release\"\n}",
  "question": "Is it true that the record does not give 'Album' as the primary type?"
 },
 {
  "qid": "q003ecb6293",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nLocal authority: Kingston-Upon-Thames\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "None of these groups",
   "Group A",
   "Group B",
   "Group C"
  ],
  "definitions": "- Group A: the business type is Manufacturers/packers, Retailers - supermarkets/hypermarkets or Distributors/Transporters\n- Group B: the business type is Mobile caterer, Other catering premises or Restaurant/Cafe/Canteen\n- Group C: the business type is School/college/university, Retailers - other or Caring Premises\n- None of these groups: any other is"
 },
 {
  "qid": "q7c360dd549",
  "kind": "yes/no",
  "text": "Project ID: 706253\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-ST\nCall topic: MSCA-IF-2015-EF\nStart date: 2017-01-01\nEnd date: 2018-06-30\nTotal cost: 146591.1 EUR\nEC maximum contribution: 146591.1 EUR",
  "question": "Is the end date later than 2 years after the start date?",
  "definitions": "- yes: the End date is later than the Start date plus 2 years (same month and day).\n- no: the End date is on or before the Start date plus 2 years."
 },
 {
  "qid": "q0c2b5ac152",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nHygiene score: 5\nStructural score: 0\nConfidence in management score: 5",
  "question": "Does the hygiene score exceed the structural score?"
 },
 {
  "qid": "q1820cb6a3d",
  "kind": "choice",
  "text": "Organization: Regional Municipality of Durham\nCountry: Canada",
  "question": "In which period was Regional Municipality of Durham (Canada) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "before 1800",
   "1800-1899"
  ]
 },
 {
  "qid": "qb7cbd4d707",
  "kind": "yes/no",
  "text": "Project ID: 748679\nTitle: Uncovering the Transatlantic History of Turkey Husbandry and Breeding using a Multi-Disciplinary Approach",
  "question": "Does the project title have more than 10 words?"
 },
 {
  "qid": "qbcffe3d32b",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\n{\n  \"total_usd_m\": 200.00,\n  \"approval_fy\": 2023,\n  \"status\": \"Active\",\n  \"country\": \"Lebanon\",\n  \"themes\": 0\n}",
  "question": "Is it true that this entry does not count as an open project under the card?",
  "definitions": "- yes: Yes if the status is Active or Pipeline.\n- no: No if the status is Closed or Dropped."
 },
 {
  "qid": "q95c46e7d50",
  "kind": "choice",
  "text": "Taxon: Petrasteridae\nKingdom: Animalia",
  "question": "To which phylum does the taxon Petrasteridae belong?",
  "options": [
   "Echinodermata",
   "Mollusca",
   "Rotifera",
   "Cnidaria"
  ]
 },
 {
  "qid": "qb2aed63ec5",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\nTsunami flag 0; Felt reports none recorded; Stations used 43; Latitude 50.980.",
  "question": "Is the epicentre inside the tropical band (absolute latitude up to 23.4)?"
 },
 {
  "qid": "qa544557aca",
  "kind": "choice",
  "text": "Accession number: 2022.241\nObject type: Ceramic\nCollection: Japanese Art\nTechnique: Porcelain with cobalt blue glaze, overglaze color enamel, and silver painting overlay\nCulture: Japan, Meiji period (1868–1912)\nDate text: 1893–1900\nDate range: 1893 to 1900\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Which medium class does the technique text fall into?",
  "options": [
   "stone",
   "ceramic or glass",
   "metal",
   "ink, watercolor or tempera",
   "other",
   "textile",
   "oil paint"
  ],
  "definitions": "- oil paint: the Technique text contains 'oil' (checked first)\n- ink, watercolor or tempera: else it contains ink, watercolor, gouache, tempera or wash\n- metal: else it contains bronze, gold, silver, iron, copper, brass, steel, pewter or gilt\n- stone: else it contains marble, limestone, granite, sandstone, alabaster, stone, jade or basalt\n- ceramic or glass: else it contains porcelain, earthenware, stoneware, ceramic, glaze, clay, terracotta, glass or faience\n- textile: else it contains silk, wool, linen, cotton, embroider, velvet or tapestry\n- other: none of the words above appear"
 },
 {
  "qid": "q753af9067a",
  "kind": "yes/no",
  "text": "Project register entry\n| Field | Value |\n| --- | --- |\n| Status | Closed |\n| Country | India |\n| Environmental category | C |\n| Major themes listed | 3 |",
  "question": "Is the country 'India'?"
 },
 {
  "qid": "q3c6ba8013b",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\nRelease group ID: 98e8990d-ab03-3867-a4fc-8919a3e811fb\nFirst release date: 2005-01-18\nPrimary type: EP\nGenre tag count: 6",
  "question": "Is the primary type 'Album'?"
 },
 {
  "qid": "q638aa03f46",
  "kind": "choice",
  "text": "Project ID: 733021\nProgramme: Horizon 2020\nFunding scheme: SESAR-IA\nCall topic: SESAR.IR-VLD.Wave1-23-2015\nStart date: 2016-11-01\nEnd date: 2019-12-31\nTotal cost: 9454085.22 EUR\nEC maximum contribution: 3760701.53 EUR",
  "question": "Which group does the funding scheme belong to?",
  "options": [
   "Marie Sklodowska-Curie (MSCA)",
   "research and innovation (RIA, IA)",
   "SME instrument (SME)",
   "other schemes",
   "coordination and support (CSA)",
   "European Research Council (ERC)"
  ],
  "definitions": "- research and innovation (RIA, IA): scheme RIA, IA, CS2-RIA or CS2-IA\n- coordination and support (CSA): scheme CSA\n- Marie Sklodowska-Curie (MSCA): any scheme code that starts with MSCA\n- European Research Council (ERC): any scheme code that starts with ERC\n- SME instrument (SME): any scheme code that starts with SME\n- other schemes: every other scheme code"
 },
 {
  "qid": "q95a8b9c44c",
  "kind": "yes/no",
  "text": "Project ID: 739793\nProgramme: Horizon 2020\nFunding scheme: CSA\nCall topic: INNOSUP-02-2016\nStart date: 2017-09-29\nEnd date: 2018-09-28\nTotal cost: 96250 EUR\nEC maximum contribution: 96250 EUR",
  "question": "Is the EC maximum contribution above 2,000,000 EUR?"
 },
 {
  "qid": "qb44584d1a8",
  "kind": "yes/no",
  "text": "Development project record\nApproval fiscal year: 2010\nRegion: Middle East and North Africa\nMajor sectors listed: 1\nLending instrument: Investment Project Financing",
  "question": "Does the record give 'Middle East and North Africa' as the region?"
 },
 {
  "qid": "q78495db2e3",
  "kind": "yes/no",
  "text": "City: Lima\nCountry: Peru",
  "question": "Is it true that Lima is not the capital of Peru?"
 },
 {
  "qid": "q78127240cf",
  "kind": "yes/no",
  "text": "Release-group record\n- Title = Geração Bendita\n- Secondary types = Soundtrack\n- Genre tags = rock, psychedelic rock\n- Release group ID = 3a002a00-87ee-3689-8ebb-6645e7919bd1",
  "question": "Does the entry list fewer than 20 characters in the title?"
 },
 {
  "qid": "q2d553b9654",
  "kind": "yes/no",
  "text": "Bibliographic record\n| Field | Value |\n| --- | --- |\n| Work type | article |\n| Citation count | 0 |\n| Version | publishedVersion |\n| Open-access status | gold |\n| Volume | 2023 |",
  "question": "Is it true that the work type is not 'article'?"
 },
 {
  "qid": "qb02fafe90b",
  "kind": "yes/no",
  "text": "Place: Pokhara\nCountry: Nepal\nTime zone (record): Asia/Kathmandu",
  "question": "Does Pokhara meet this rule?",
  "definitions": "- yes: The place's time zone is Asia/Shanghai, Asia/Ho_Chi_Minh or Asia/Tehran.\n- no: The place's time zone is any other."
 },
 {
  "qid": "q03a5649b26",
  "kind": "yes/no",
  "text": "Project and operations register row\n{\n  \"ibrd_usd_m\": 12.50,\n  \"themes\": 0,\n  \"project_id\": \"P004671\",\n  \"closing_date\": \"1976-12-31\",\n  \"supplemental\": \"N\",\n  \"board_approval_date\": \"1970-07-28\"\n}",
  "question": "Does the closing date fall 7 or more calendar years after the approval date?"
 },
 {
  "qid": "qcdbe924c71",
  "kind": "yes/no",
  "text": "Project and operations register row\nboard_approval_date: 2022-06-22\nsupplemental: N\nibrd_usd_m: 0.00\nregion: East Asia and Pacific",
  "question": "Does the board approval year fall before 2015?"
 },
 {
  "qid": "q94aac49f82",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Pub/bar/nightclub\nRating date: October (rating 5)",
  "question": "Would it be the case that the rating was given in the second half of the year?"
 },
 {
  "qid": "q537954e94a",
  "kind": "yes/no",
  "text": "Taxon: Zygopolaris borealis\nKingdom: Fungi\nClass: Kickxellomycetes",
  "question": "Does Zygopolaris borealis meet the rule?",
  "definitions": "- yes: The taxon's class is Malasseziomycetes, Kickxellomycetes or Exobasidiomycetes.\n- no: The taxon's class is any other class."
 }
]
