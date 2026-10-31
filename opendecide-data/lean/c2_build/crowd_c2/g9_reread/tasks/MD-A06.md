# G9 re-read (G5-H blind read) MD-A06 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-A06.json

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
  "qid": "qd030f7254a",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Caring Premises\nLocal authority: Swindon\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group B",
   "None of these groups",
   "Group A",
   "Group C"
  ],
  "definitions": "- Group A: the rating is 5\n- Group B: the rating is 1\n- Group C: the rating is 4\n- None of these groups: any other is"
 },
 {
  "qid": "qa3ab1058c3",
  "kind": "yes/no",
  "text": "Music catalogue entry\nDisambiguation comment none; Genre tags rock, punk; First release date 1983; Title Let the Vultures Fly EP.",
  "question": "Does the genre tag list include 'punk'?"
 },
 {
  "qid": "q3725582af4",
  "kind": "choice",
  "text": "Place: Garoua\nCountry: Cameroon",
  "question": "Under the definitions, which group holds the country where Garoua lies?",
  "options": [
   "Group C",
   "None of these groups",
   "Group B",
   "Group A"
  ],
  "definitions": "- Group A: Poland, Azerbaijan or Thailand\n- Group B: Iran, Japan or United States\n- Group C: Russia, Cameroon or Germany\n- None of these groups: any other country"
 },
 {
  "qid": "q881418a242",
  "kind": "yes/no",
  "text": "Discography database row\nArtist credits: 1\nGenre tag count: 2\nReleases in group: 3\nGenre tags: rock, new wave",
  "question": "Is it true that the genre tag list does not include 'electronic'?"
 },
 {
  "qid": "qde31dec930",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\nTitle: Ronchalant\nArtist credits: 1\nFirst release date: 1999\nGenre tags: hip hop",
  "question": "Does the first release date include the month?"
 },
 {
  "qid": "qb48bbca12a",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\npager_alert: none\nnetwork: us\norigin_time: 2026-09-27 01:57:21\nlatitude: -21.198",
  "question": "Is the origin month between January and June?"
 },
 {
  "qid": "qe9966bbb08",
  "kind": "yes/no",
  "text": "GO term: GO:0060756\nName: foraging behavior\nDefinition: Behavior by which an organism locates food.\nDefinition sources: GOC:dph, GOC:tb\nSynonyms (0): none listed\nDirect is_a parents (1): behavior\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Would you say this term has over 2 listed synonyms?"
 },
 {
  "qid": "q3cd48246a9",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\nproject_name: St Maarten Civil Society Partnership Facility for Resilience Project (CSPFRP)\ninstrument: Investment Project Financing\ntotal_usd_m: 7.20\nclosing_date: 2025-03-31\nreference_year: 2026",
  "question": "Does the project commit at least 25 million USD in total?"
 },
 {
  "qid": "qd65c15585e",
  "kind": "choice",
  "text": "Accession number: 1997.109.1\nObject type: Painting\nCollection: ASIAN - Folding screen\nTechnique: One of a pair of four-panel folding screens; ink, color, and cut gold foil on paper\nCulture: Japan, Edo period (1615–1868)\nDate text: 1800s\nDate range: 1800 to 1856\nMeasurements: not listed\nCredit line, first word: Bequest",
  "question": "Which medium class does the technique text fall into?",
  "options": [
   "ink, watercolor or tempera",
   "oil paint",
   "textile",
   "stone",
   "ceramic or glass",
   "other",
   "metal"
  ],
  "definitions": "- oil paint: the Technique text contains 'oil' (checked first)\n- ink, watercolor or tempera: else it contains ink, watercolor, gouache, tempera or wash\n- metal: else it contains bronze, gold, silver, iron, copper, brass, steel, pewter or gilt\n- stone: else it contains marble, limestone, granite, sandstone, alabaster, stone, jade or basalt\n- ceramic or glass: else it contains porcelain, earthenware, stoneware, ceramic, glaze, clay, terracotta, glass or faience\n- textile: else it contains silk, wool, linen, cotton, embroider, velvet or tapestry\n- other: none of the words above appear"
 },
 {
  "qid": "qfb362aee18",
  "kind": "yes/no",
  "text": "Music catalogue entry\n| Field | Value |\n| --- | --- |\n| First release date | 2004-11 |\n| Genre tag count | 3 |\n| Release group ID | 6413f797-747b-39f4-811d-0eebc7b8c905 |\n| Artist credits | 1 |\n| Title | Days Are What We Live In |",
  "question": "Does the entry list 5 or more genre tags?"
 },
 {
  "qid": "qc936456650",
  "kind": "choice",
  "text": "Organization: Damjanich János Múzeum\nCountry: Hungary",
  "question": "Which type does the registry give for Damjanich János Múzeum (Hungary)?",
  "options": [
   "archive",
   "nonprofit",
   "education",
   "facility"
  ]
 },
 {
  "qid": "qcad7650f0e",
  "kind": "yes/no",
  "text": "Place: Zhangjiachuan\nCountry: China\nFeature code (record): PPLA3",
  "question": "Does Zhangjiachuan meet this rule?",
  "definitions": "- yes: The place's feature code is PPLC, PPL or PPLA2.\n- no: The place's feature code is any other code."
 },
 {
  "qid": "qdcd0ab9247",
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
  "qid": "qe91047d95c",
  "kind": "choice",
  "text": "Accession number: 2001.179.6\nObject type: Jewelry\nCollection: China - Qing Dynasty\nTechnique: Copper-silver alloy, gilding, kingfisher feathers, glass beads\nCulture: China, Qing dynasty (1644-1911)\nDate text: 1700s or 1800s\nDate range: 1700 to 1899\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Which department of the museum looks after this object?",
  "options": [
   "Drawings",
   "Japanese Art",
   "Greek and Roman Art",
   "Textiles",
   "Prints",
   "Photography",
   "Medieval Art",
   "Chinese Art"
  ]
 },
 {
  "qid": "qb549442f22",
  "kind": "choice",
  "text": "Place: Qoryooley\nCountry: Somalia",
  "question": "Under the definitions, which group holds the country where Qoryooley lies?",
  "options": [
   "Group C",
   "None of these groups",
   "Group A",
   "Group B"
  ],
  "definitions": "- Group A: China, Russia or Somalia\n- Group B: Australia, India or Algeria\n- Group C: Czechia, Cuba or Argentina\n- None of these groups: any other country"
 },
 {
  "qid": "q7a72988ba3",
  "kind": "choice",
  "text": "Organization: Endangered Wildlife Trust\nCountry: South Africa",
  "question": "Under the definitions, which group holds Endangered Wildlife Trust?",
  "options": [
   "Group C",
   "Group A",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: Sweden, United States or Mexico\n- Group B: The Netherlands, Canada or Indonesia\n- Group C: Finland, Egypt or South Africa\n- None of these groups: any other country"
 },
 {
  "qid": "qbc1861ba66",
  "kind": "yes/no",
  "text": "Organization: Delta Extinguishers (Belgium)\nCountry: Belgium\nType (record): company",
  "question": "Does Delta Extinguishers (Belgium) meet this rule?",
  "definitions": "- yes: The organization's type is company or education.\n- no: The organization has any other type."
 },
 {
  "qid": "q1d2cc91264",
  "kind": "choice",
  "text": "Place: Prilep\nCountry: North Macedonia",
  "question": "Under the definitions, which group holds the country where Prilep lies?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: Nigeria, Germany or India\n- Group B: United Kingdom, Iraq or North Macedonia\n- Group C: Russia, France or Brazil\n- None of these groups: any other country"
 },
 {
  "qid": "qb6422eb935",
  "kind": "choice",
  "text": "Organization: University of West Los Angeles\nCountry: United States",
  "question": "Which group does University of West Los Angeles fall into under these definitions?",
  "options": [
   "Group C",
   "None of these groups",
   "Group A",
   "Group B"
  ],
  "definitions": "- Group A: Mexico, Switzerland or United Kingdom\n- Group B: Italy, India or Brazil\n- Group C: Sweden, Indonesia or United States\n- None of these groups: any other country"
 },
 {
  "qid": "qce8d5c11d6",
  "kind": "choice",
  "text": "Development project record\nEnvironmental category: B\nFinancing type: Other+Other+Other+Other+IDA\nBoard approval date: 2016-10-27\nMajor sectors listed: 3",
  "question": "Which fiscal year of the board approval does this entry fall in?",
  "options": [
   "2014",
   "2015",
   "2016",
   "2017"
  ],
  "definitions": "The World Bank fiscal year runs from 1 July to 30 June and is named after the calendar year in which it ends. Approval on or after 1 July of year Y falls in fiscal year Y+1; approval before 1 July falls in fiscal year Y."
 },
 {
  "qid": "q3a3565c49a",
  "kind": "yes/no",
  "text": "Scholarly work metadata\nWork type: article\nTopic domain: Social Sciences\nAuthors listed: 6\nTopic field: Social Sciences",
  "question": "Would it be right that the record shows at least 5 authors?"
 },
 {
  "qid": "q895cdd8a66",
  "kind": "yes/no",
  "text": "Accession number: 1971.155\nObject type: Sculpture\nCollection: Oceanic Art\nTechnique: wood\nCulture: Melanesia, New Guinea, Massim Area, Trobriand Islands, 20th...\nDate text: before 1930\nDate range: 1900 to 1930\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Was this work begun before the year 1900?"
 },
 {
  "qid": "qdd488cd340",
  "kind": "yes/no",
  "text": "Organization: Ali Osman Sonmez Oncology Hospital",
  "question": "Is Ali Osman Sonmez Oncology Hospital located in United States?"
 },
 {
  "qid": "q59fc383ddd",
  "kind": "yes/no",
  "text": "Organization: Sociedad Hispano Mundial",
  "question": "Is the country of Sociedad Hispano Mundial Yemen?"
 },
 {
  "qid": "q1851a545ce",
  "kind": "yes/no",
  "text": "Accession number: 1958.46\nObject type: Drawing\nCollection: DR - French\nTechnique: pastel\nCulture: France, 20th century\nDate text: 1916\nDate range: 1916 to 1916\nMeasurements: not listed\nCredit line, first word: Bequest",
  "question": "Was this work begun before the year 1900?"
 },
 {
  "qid": "q074432c430",
  "kind": "yes/no",
  "text": "City: Lima\nCountry: Peru",
  "question": "Is it true that Lima is not the capital of Peru?"
 },
 {
  "qid": "q706bf5262d",
  "kind": "yes/no",
  "text": "Project register entry\n| Field | Value |\n| --- | --- |\n| Status | Closed |\n| Country | India |\n| Environmental category | C |\n| Major themes listed | 3 |",
  "question": "Is the country 'India'?"
 },
 {
  "qid": "q794a92f007",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Retailers - supermarkets/hypermarkets\nLocal authority: Telford and Wrekin Council\nRating: 5",
  "question": "Is this establishment eligible under the rule?",
  "definitions": "- yes: The business type is Retailers - other, Takeaway/sandwich shop or Retailers - supermarkets/hypermarkets.\n- no: The business type is any other type."
 },
 {
  "qid": "q72b528e0f9",
  "kind": "yes/no",
  "text": "Accession number: 1982.107\nObject type: Textile\nCollection: T - Coptic\nTechnique: wool; plain weave with slit-tapestry weave\nCulture: Egypt, Umayyad period (661–750) or Abbasid period (750–1258)\nDate text: 700s\nDate range: 700 to 799\nMeasurements: not listed\nCredit line, first word: Andrew",
  "question": "Is the gap between the first and last year above 25 years?",
  "definitions": "- yes: the last year minus the first year of the Date range is more than 25.\n- no: the last year minus the first year of the Date range is 25 or less."
 },
 {
  "qid": "q04f3776a02",
  "kind": "choice",
  "text": "Organization: Türk Otomobil Fabrikası (Turkey)\nCountry: Türkiye",
  "question": "Which type does the registry give for Türk Otomobil Fabrikası (Turkey) (Türkiye)?",
  "options": [
   "government",
   "company",
   "education",
   "facility"
  ]
 },
 {
  "qid": "q9de7d60b6f",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\n{\n  \"title\": \"Fear of the Digital Remix\",\n  \"primary_type\": \"Album\",\n  \"secondary_types\": \"Remix\",\n  \"credits\": 1,\n  \"releases\": 1\n}",
  "question": "Is 'Remix' listed among the secondary types?"
 },
 {
  "qid": "q94a534aa1e",
  "kind": "choice",
  "text": "GO term: GO:0050044\nName: galactose-6-phosphate isomerase activity\nDefinition: Catalysis of the reaction: D-galactose 6-phosphate = D-tagatose 6-phosphate.\nDefinition sources: EC:5.3.1.26, RHEA:13033\nSynonyms (2): \"D-galactose-6-phosphate aldose-ketose-isomerase activity\" RELATED; \"D-galactose-6-phosphate ketol-isomerase activity\" RELATED\nDirect is_a parents (1): intramolecular oxidoreductase activity, interconverting aldoses and ketoses\nOther relationships: none listed\nSubsets: none listed\nCross-references (4): EC:5.3.1.26, KEGG_REACTION:R03240, MetaCyc:LACTOSE-6-PHOSPHATE-ISOMERASE-RXN, RHEA:13033",
  "question": "How many different synonym scopes does the term use?",
  "options": [
   "2",
   "3 or more",
   "1"
  ]
 },
 {
  "qid": "q2a44967df9",
  "kind": "choice",
  "text": "Organization: HR Wallingford\nCountry: United Kingdom",
  "question": "What type of organization is HR Wallingford (United Kingdom)?",
  "options": [
   "company",
   "nonprofit",
   "facility",
   "archive"
  ]
 },
 {
  "qid": "qc5a835de02",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Retailers - other\nLocal authority: Mid Suffolk\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "Group A",
   "Group B",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: the business type is Retailers - supermarkets/hypermarkets, Mobile caterer or School/college/university\n- Group B: the business type is Retailers - other, Caring Premises or Restaurant/Cafe/Canteen\n- Group C: the business type is Other catering premises, Pub/bar/nightclub or Takeaway/sandwich shop\n- None of these groups: any other is"
 },
 {
  "qid": "qf670536dc4",
  "kind": "choice",
  "text": "City: Yelets\nCountry: Russia",
  "question": "Which time zone is Yelets in?",
  "options": [
   "Europe/Moscow",
   "Asia/Yekaterinburg",
   "Asia/Krasnoyarsk",
   "Asia/Kamchatka"
  ]
 },
 {
  "qid": "qe729f7cd9e",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\n{\n  \"title\": \"Rising of the Winter Full Moon\",\n  \"credits\": 1,\n  \"releases\": 1,\n  \"tags\": \"rock, black metal\",\n  \"tag_count\": 2\n}",
  "question": "Is this entry widely reissued by the card's rule?",
  "definitions": "- yes: Yes if the group holds 3 or more releases.\n- no: No if the group holds fewer than 3 releases."
 },
 {
  "qid": "q01a3b9f27c",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\n- Magnitude type = mww\n- Contributing network = us\n- Depth (km) = 10.0\n- Azimuthal gap (deg) = 99\n- Felt reports = none recorded",
  "question": "Is the focal depth 35 km or more?"
 },
 {
  "qid": "q7ee32ffb77",
  "kind": "yes/no",
  "text": "Organization: Fundacja Inkubator",
  "question": "Is Fundacja Inkubator located in Poland?"
 },
 {
  "qid": "q36909d2001",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: Great Yarmouth\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "Group C",
   "None of these groups",
   "Group A",
   "Group B"
  ],
  "definitions": "- Group A: the business type is Pub/bar/nightclub, Hotel/bed & breakfast/guest house or School/college/university\n- Group B: the business type is Mobile caterer, Retailers - other or Farmers/growers\n- Group C: the business type is Retailers - supermarkets/hypermarkets, Other catering premises or Takeaway/sandwich shop\n- None of these groups: any other is"
 },
 {
  "qid": "q2318608c2a",
  "kind": "choice",
  "text": "Earthquake catalogue entry\n{\n  \"magnitude\": 5.1,\n  \"tsunami_flag\": 0,\n  \"origin_time\": \"2025-06-08 14:55:46\",\n  \"longitude\": -150.482\n}",
  "question": "Which six-hour UTC slot applies to this entry?",
  "options": [
   "00-05",
   "06-11",
   "12-17",
   "18-23"
  ]
 },
 {
  "qid": "q71de452833",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nHygiene score: 5\nStructural score: 0\nConfidence in management score: 5",
  "question": "Does the hygiene score exceed the structural score?"
 },
 {
  "qid": "qa2e6ba9857",
  "kind": "choice",
  "text": "Organization: Compagnie Industrielle de la Matière Végétale (France)\nCountry: France",
  "question": "Under the definitions, which group holds Compagnie Industrielle de la Matière Végétale (France)?",
  "options": [
   "Group B",
   "Group A",
   "Group C",
   "None of these groups"
  ],
  "definitions": "- Group A: Denmark, France or Belgium\n- Group B: Somalia, United States or Egypt\n- Group C: Canada, Mexico or India\n- None of these groups: any other country"
 },
 {
  "qid": "q8cb43845c0",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nLocal authority: Anglesey\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "None of these groups",
   "Group B",
   "Group A",
   "Group C"
  ],
  "definitions": "- Group A: the business type is Retailers - supermarkets/hypermarkets, Manufacturers/packers or Takeaway/sandwich shop\n- Group B: the business type is Caring Premises, School/college/university or Other catering premises\n- Group C: the business type is Restaurant/Cafe/Canteen, Retailers - other or Distributors/Transporters\n- None of these groups: any other is"
 },
 {
  "qid": "q87f3d8a291",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nHygiene score: 10\nStructural score: 5\nConfidence in management score: 5",
  "question": "Which score has the largest value?",
  "options": [
   "hygiene score",
   "structural score",
   "confidence in management score"
  ]
 },
 {
  "qid": "q407031c4d2",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\nAzimuthal gap (deg) 70; Significance score 246; Stations used 21; Longitude 43.596; Tsunami flag 0.",
  "question": "Under the card, is this entry poorly covered by stations?",
  "definitions": "- yes: Yes if the azimuthal gap is 180 degrees or more.\n- no: No if the azimuthal gap is below 180 degrees."
 },
 {
  "qid": "q8b8f1f49c2",
  "kind": "choice",
  "text": "Place: Qal‘at Şāliḩ\nCountry: Iraq",
  "question": "Under the definitions, which group holds the country where Qal‘at Şāliḩ lies?",
  "options": [
   "Group C",
   "Group A",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: Hong Kong, Ivory Coast or Philippines\n- Group B: United States, Spain or Iraq\n- Group C: Russia, Pakistan or Italy\n- None of these groups: any other country"
 },
 {
  "qid": "q1c2d57247c",
  "kind": "choice",
  "text": "Taxon: Lychaete herpestica\nKingdom: Plantae\nPhylum: Chlorophyta",
  "question": "Which class is the taxon Lychaete herpestica placed in?",
  "options": [
   "Klebsormidiophyceae",
   "Lycopodiopsida",
   "Prasinophyceae",
   "Ulvophyceae"
  ]
 },
 {
  "qid": "q1d0a68391c",
  "kind": "yes/no",
  "text": "GO term: GO:0070056\nName: prospore membrane leading edge\nDefinition: The region of the prospore membrane that extends to surround the spore nucleus; coated with specific proteins that are thought to play a role in prospore membrane organization.\nDefinition sources: GOC:mah, PMID:14702385\nSynonyms (1): \"forespore membrane leading edge\" EXACT\nDirect is_a parents (1): membrane\nOther relationships: part_of prospore membrane\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Does this term have a part_of relationship?"
 },
 {
  "qid": "qbbd84c1b25",
  "kind": "yes/no",
  "text": "Bibliographic record\n{\n  \"last_page\": 107,\n  \"first_page\": 93,\n  \"references_count\": 0,\n  \"countries\": 0,\n  \"work_type\": \"review\"\n}",
  "question": "Is the page span, counting both end pages, below 10?"
 },
 {
  "qid": "qa3cfe62ed5",
  "kind": "choice",
  "text": "Place: Gaogu\nCountry: China",
  "question": "Which group does the country of Gaogu belong to under these definitions?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: India, France or China\n- Group B: Madagascar, Vietnam or Philippines\n- Group C: United States, Croatia or Malaysia\n- None of these groups: any other country"
 }
]
