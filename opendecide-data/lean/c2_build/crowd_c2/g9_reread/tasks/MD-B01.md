# G9 re-read (G5-H blind read) MD-B01 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-B01.json

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
  "qid": "q3da1a94c48",
  "kind": "yes/no",
  "text": "Taxa: Pterosperma nationalis; Pterosperma undulatum",
  "question": "Are Pterosperma nationalis and Pterosperma undulatum placed in different orders?"
 },
 {
  "qid": "q9380a723e4",
  "kind": "choice",
  "text": "Bibliographic record\nReference year: 2026\nOpen-access status: gold\nReferences listed: 38\nFirst page: 1",
  "question": "Which access group applies to this entry?",
  "options": [
   "fully open venue",
   "free copy elsewhere",
   "no free copy"
  ],
  "definitions": "- fully open venue: Pick this when the open-access status is gold or diamond.\n- free copy elsewhere: Pick this when the status is green, hybrid or bronze.\n- no free copy: Pick this when the status is closed."
 },
 {
  "qid": "qcdb1568e4d",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\nLocation description 104 km NW of Port-Vila, Vanuatu; Azimuthal gap (deg) 59; Origin time (UTC) 2020-09-06 02:59:16; Tsunami flag 1; Magnitude 6.2.",
  "question": "Is it true that the event does not have both a magnitude of 6.0 or higher and a tsunami flag of 1?"
 },
 {
  "qid": "qc7a4d8be2b",
  "kind": "yes/no",
  "text": "Seismic event record\nMagnitude type: mb\nSignificance score: 369\nLocation description: 144 km SE of Vilyuchinsk, Russia\nDepth (km): 10.0\nAzimuthal gap (deg): 121",
  "question": "Does the record give 'Indonesia' as the last comma-separated part of the location description?"
 },
 {
  "qid": "q94283bab09",
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
  "qid": "qc45726e0d8",
  "kind": "yes/no",
  "text": "Jijiang is a city in China.",
  "question": "Do more than 130,000 people live in Jijiang (China)?"
 },
 {
  "qid": "q68ba762c60",
  "kind": "choice",
  "text": "Organization: Weskoppies Psychiatric Hospital\nCountry: South Africa",
  "question": "Which group does Weskoppies Psychiatric Hospital fall into under these definitions?",
  "options": [
   "None of these groups",
   "Group A",
   "Group B",
   "Group C"
  ],
  "definitions": "- Group A: Guinea, Russia or Ukraine\n- Group B: United States, Poland or South Africa\n- Group C: Kenya, Italy or Argentina\n- None of these groups: any other country"
 },
 {
  "qid": "q82378bb67a",
  "kind": "yes/no",
  "text": "Organization: Ali Osman Sonmez Oncology Hospital",
  "question": "Is Ali Osman Sonmez Oncology Hospital located in United States?"
 },
 {
  "qid": "q63719095ae",
  "kind": "choice",
  "text": "Organization: Shanghai Institute of Hypertension\nCountry: China",
  "question": "Which type does the registry give for Shanghai Institute of Hypertension (China)?",
  "options": [
   "facility",
   "other",
   "healthcare",
   "company"
  ]
 },
 {
  "qid": "q78c9e6d4e1",
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
  "qid": "q60f4c8bdec",
  "kind": "yes/no",
  "text": "Project ID: 892369\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-SE\nCall topic: MSCA-IF-2019\nStart date: 2020-05-01\nEnd date: 2022-04-30\nTotal cost: 175572.48 EUR\nEC maximum contribution: 175572.48 EUR",
  "question": "Does the EC contribution equal the total cost?",
  "definitions": "- yes: the EC maximum contribution equals the total cost (within 0.5 EUR).\n- no: the EC maximum contribution is smaller than the total cost."
 },
 {
  "qid": "q7f1580ab15",
  "kind": "choice",
  "text": "Event summary from a seismic network catalogue\nMagnitude type mww; Magnitude 6.0; Felt reports 52; Event type earthquake; Latitude -8.866; Longitude -75.071.",
  "question": "Pick the map quadrant for this entry.",
  "options": [
   "northwest",
   "southeast",
   "northeast",
   "southwest"
  ],
  "definitions": "- northeast: Pick this when latitude is above 0 and longitude is above 0.\n- northwest: Pick this when latitude is above 0 and longitude is 0 or below.\n- southeast: Pick this when latitude is 0 or below and longitude is above 0.\n- southwest: Pick this when latitude is 0 or below and longitude is 0 or below."
 },
 {
  "qid": "qd47a965594",
  "kind": "yes/no",
  "text": "Discography database row\n- Release group ID = 80aa2045-ec51-4e1f-b06b-23e6142beb90\n- Title = Belka\n- First release date = 1986\n- Genre tags = none",
  "question": "Was it first released in 1980 or later?"
 },
 {
  "qid": "q5b462b0fb6",
  "kind": "yes/no",
  "text": "Accession number: 1942.785\nObject type: Sculpture\nCollection: MED - Gothic\nTechnique: polychromed limestone\nCulture: France, possibly Champagne, 15th century\nDate text: c. 1460–1475\nDate range: 1460 to 1475\nMeasurements: not listed\nCredit line, first word: Bequest",
  "question": "Was this work begun before the year 1300?",
  "definitions": "- yes: the first year of the Date range is earlier than 1300.\n- no: the first year of the Date range is 1300 or later."
 },
 {
  "qid": "qbdb19b1777",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Retailers - other\nLocal authority: Southampton\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: the business type is School/college/university, Retailers - other or Takeaway/sandwich shop\n- Group B: the business type is Other catering premises, Caring Premises or Restaurant/Cafe/Canteen\n- Group C: the business type is Pub/bar/nightclub, Distributors/Transporters or Mobile caterer\n- None of these groups: any other is"
 },
 {
  "qid": "q3db33fb38d",
  "kind": "choice",
  "text": "Taxon: Porphyra lanceolata\nKingdom: Plantae",
  "question": "To which phylum does the taxon Porphyra lanceolata belong?",
  "options": [
   "Chlorophyta",
   "Charophyta",
   "Tracheophyta",
   "Rhodophyta"
  ]
 },
 {
  "qid": "qd7ec46ad6d",
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
  "qid": "qbed6b4be06",
  "kind": "yes/no",
  "text": "Discography database row\n{\n  \"primary_type\": \"EP\",\n  \"statuses\": \"Official\",\n  \"secondary_types\": \"Compilation\",\n  \"credits\": 1,\n  \"first_release_date\": 2010,\n  \"disambiguation\": \"none\"\n}",
  "question": "Under the card, is this entry a plain album?",
  "definitions": "- yes: Yes if the primary type is Album and no secondary type is listed.\n- no: No if the primary type is not Album or at least one secondary type is listed."
 },
 {
  "qid": "q4434abbfda",
  "kind": "choice",
  "text": "Taxon: Chaenotheca hispidula\nKingdom: Fungi\nOrder: Coniocybales",
  "question": "Which family is the taxon Chaenotheca hispidula placed in?",
  "options": [
   "Kickxellaceae",
   "Coniocybaceae",
   "Orbiliaceae",
   "Neocallimastigaceae"
  ]
 },
 {
  "qid": "q6e3e2ab83d",
  "kind": "yes/no",
  "text": "Project ID: 655027\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-ST\nCall topic: MSCA-IF-2014-EF\nStart date: 2015-10-01\nEnd date: 2017-09-30\nTotal cost: 177598.8 EUR\nEC maximum contribution: 177598.8 EUR",
  "question": "Did the project start before 2016?"
 },
 {
  "qid": "q878c2236c8",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\n| Field | Value |\n| --- | --- |\n| Azimuthal gap (deg) | 92 |\n| PAGER alert | none |\n| Depth (km) | 107.4 |\n| Felt reports | 2 |",
  "question": "Does the event lie at a depth of less than 35 km?"
 },
 {
  "qid": "q6e4b73d733",
  "kind": "choice",
  "text": "Bibliographic record\n{\n  \"language\": \"en\",\n  \"cited_by_count\": 10,\n  \"domain\": \"Physical Sciences\",\n  \"first_page\": 1783,\n  \"last_page\": 1801\n}",
  "question": "Pick the length class for this entry.",
  "options": [
   "short",
   "medium",
   "long"
  ],
  "definitions": "- short: Pick this when the page span (last minus first, plus one) is 1 to 4 pages.\n- medium: Pick this when the span is 5 to 14 pages.\n- long: Pick this when the span is 15 pages or more."
 },
 {
  "qid": "q46279c8faf",
  "kind": "choice",
  "text": "Project ID: 772259\nProgramme: Horizon 2020\nFunding scheme: ERC-COG\nCall topic: ERC-2017-COG\nStart date: 2018-05-01\nEnd date: 2024-07-31\nTotal cost: 1998649 EUR\nEC maximum contribution: 1998649 EUR",
  "question": "Which programme part does the call topic code start with?",
  "options": [
   "ERC",
   "MSCA",
   "other",
   "EIC",
   "SMEInst",
   "ICT"
  ],
  "definitions": "- MSCA: code starts with MSCA\n- ERC: code starts with ERC\n- EIC: code starts with EIC\n- SMEInst: code starts with SMEInst\n- ICT: code starts with ICT\n- other: any other first part"
 },
 {
  "qid": "q3d8242f2bc",
  "kind": "choice",
  "text": "Organization: National Coal Mining Museum for England\nCountry: United Kingdom",
  "question": "What type of organization is National Coal Mining Museum for England (United Kingdom)?",
  "options": [
   "facility",
   "healthcare",
   "archive",
   "government"
  ]
 },
 {
  "qid": "qfe85290572",
  "kind": "choice",
  "text": "Lending operation record from a development-bank register\n- Environmental category = A\n- Total commitment (USD million) = 275.00\n- Board approval date = 2014-12-09\n- Major themes listed = 2\n- Project name = Kariba Dam Rehabilitation Project (RI)",
  "question": "Which fiscal year of the board approval does this entry fall in?",
  "options": [
   "2017",
   "2015",
   "2016",
   "2014"
  ],
  "definitions": "The World Bank fiscal year runs from 1 July to 30 June and is named after the calendar year in which it ends. Approval on or after 1 July of year Y falls in fiscal year Y+1; approval before 1 July falls in fiscal year Y."
 },
 {
  "qid": "q534b264cbc",
  "kind": "choice",
  "text": "Organization: Wakefield Orthopaedic Clinic",
  "question": "Which country is Wakefield Orthopaedic Clinic located in?",
  "options": [
   "United States",
   "Japan",
   "Spain",
   "Australia"
  ]
 },
 {
  "qid": "q9325ef0901",
  "kind": "yes/no",
  "text": "Project ID: 731848\nProgramme: Horizon 2020\nFunding scheme: IA\nCall topic: ICT-25-2016-2017\nStart date: 2017-01-01\nEnd date: 2020-04-30\nTotal cost: 3926375 EUR\nEC maximum contribution: 3494825 EUR",
  "question": "Is the EC maximum contribution above 1,000,000 EUR?"
 },
 {
  "qid": "qae348fa3aa",
  "kind": "yes/no",
  "text": "Event summary from a seismic network catalogue\nContributing network ci; Latitude 32.913; Significance score 107; PAGER alert none; Magnitude type ml.",
  "question": "Would it be accurate that the record doesn't give 'ci' as the contributing network code?"
 },
 {
  "qid": "qd6be6a0bfb",
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
  "qid": "q4ef0ae2bde",
  "kind": "choice",
  "text": "Organization: Scotland Memorial Hospital\nCountry: United States",
  "question": "Under the definitions, which group holds Scotland Memorial Hospital?",
  "options": [
   "Group C",
   "Group B",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: Mexico, Egypt or Canada\n- Group B: Nigeria, The Netherlands or Finland\n- Group C: Indonesia, Spain or United States\n- None of these groups: any other country"
 },
 {
  "qid": "qf4cf791fa3",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\n- Magnitude type = mw\n- Origin time (UTC) = 2015-05-29 07:00:09\n- Depth (km) = 72.6\n- Longitude = -156.430",
  "question": "Is it true that the origin month is not between January and June?"
 },
 {
  "qid": "q3916d44702",
  "kind": "choice",
  "text": "Taxon: Paleosuchus trigonatus\nKingdom: Animalia\nPhylum: Chordata",
  "question": "To which class does the taxon Paleosuchus trigonatus belong?",
  "options": [
   "Polychaeta",
   "Maxillopoda",
   "Crocodylia",
   "Myxozoa"
  ]
 },
 {
  "qid": "qec721237b4",
  "kind": "yes/no",
  "text": "Accession number: 1939.267\nObject type: Drawing\nCollection: DR - American 19th Century\nTechnique: watercolor and gouache over graphite\nCulture: America\nDate text: 1897\nDate range: 1892 to 1902\nMeasurements: not listed\nCredit line, first word: Purchase",
  "question": "Does the date text start with the letter c and a full stop, marking an approximate date?",
  "definitions": "- yes: the Date text begins with 'c.' (circa).\n- no: the Date text does not begin with 'c.'."
 },
 {
  "qid": "q4cb022c332",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\nnetwork: us\nplace: 148 km ENE of Masohi, Indonesia\npager_alert: green\ntsunami_flag: 0",
  "question": "Is the last comma-separated part of the location description 'Indonesia'?"
 },
 {
  "qid": "q1d6b3d531b",
  "kind": "yes/no",
  "text": "Project ID: 101025655\nAcronym: BENGUP",
  "question": "Does the acronym have more than 8 characters?"
 },
 {
  "qid": "q3a5f931cc0",
  "kind": "yes/no",
  "text": "Organization: Fundacja Inkubator",
  "question": "Is Fundacja Inkubator located in Poland?"
 },
 {
  "qid": "q5b0bd3a743",
  "kind": "yes/no",
  "text": "Discography database row\n{\n  \"disambiguation\": \"present\",\n  \"tags\": \"none\",\n  \"first_release_date\": \"2002-09\",\n  \"release_group_id\": \"b6d4261c-0724-3c8a-b5ae-efe375237503\"\n}",
  "question": "Is a disambiguation comment recorded for this entry?"
 },
 {
  "qid": "q36fdcc12e1",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\n- Magnitude type = mww\n- Contributing network = us\n- Depth (km) = 10.0\n- Azimuthal gap (deg) = 99\n- Felt reports = none recorded",
  "question": "Is the focal depth 35 km or more?"
 },
 {
  "qid": "qa8716f8878",
  "kind": "choice",
  "text": "Project ID: 635356\nProgramme: Horizon 2020\nFunding scheme: ERC-STG\nCall topic: ERC-StG-2014\nStart date: 2015-08-01\nEnd date: 2020-07-31\nTotal cost: 1500000 EUR\nEC maximum contribution: 1500000 EUR",
  "question": "Which period holds the start year?",
  "options": [
   "2021 or later",
   "2014 to 2016",
   "2019 to 2020",
   "2017 to 2018"
  ]
 },
 {
  "qid": "qf5e915af7d",
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
  "qid": "qabfddaba65",
  "kind": "yes/no",
  "text": "Organization: Danville Area Community College\nCountry: United States",
  "question": "Was Danville Area Community College (United States) established before 1950?"
 },
 {
  "qid": "qac0e8dead6",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: School/college/university\nLocal authority: Ceredigion\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: the business type is Other catering premises, Restaurant/Cafe/Canteen or Hotel/bed & breakfast/guest house\n- Group B: the business type is Manufacturers/packers, School/college/university or Farmers/growers\n- Group C: the business type is Caring Premises, Retailers - supermarkets/hypermarkets or Takeaway/sandwich shop\n- None of these groups: any other is"
 },
 {
  "qid": "q15c860fbc3",
  "kind": "yes/no",
  "text": "Title: Tiraz with gold\nAccession number: 1982.109\nObject type: Textile\nCollection: Textiles\nTechnique: plain weave with inwoven tapestry weave: linen, silk, and gold filé\nCulture: Egypt, Fatimid period, reign of Caliph al-Zahir, 1020–1035\nDate text: 1020–35\nDate range: 1020 to 1035\nMeasurements: not listed\nCredit line, first word: Andrew",
  "question": "Does the title have more than 4 words?"
 },
 {
  "qid": "qbfae5273c8",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\nRelease statuses: Official\nSecondary types: none\nFirst release date: 2002-10\nGenre tags: electronic, downtempo, electronica/dance",
  "question": "Does the first-release year fall before 2000?"
 },
 {
  "qid": "q55042c04a8",
  "kind": "yes/no",
  "text": "Project ID: 681819\nProgramme: Horizon 2020\nFunding scheme: ERC-COG\nCall topic: ERC-CoG-2015\nStart date: 2016-05-01\nEnd date: 2021-10-31\nTotal cost: 1978750 EUR\nEC maximum contribution: 1978750 EUR",
  "question": "Is the end date later than 1 years after the start date?",
  "definitions": "- yes: the End date is later than the Start date plus 1 years (same month and day).\n- no: the End date is on or before the Start date plus 1 years."
 },
 {
  "qid": "qa100779ca7",
  "kind": "yes/no",
  "text": "Project ID: 790654\nProgramme: Horizon 2020\nFunding scheme: ERC-POC\nCall topic: ERC-2017-PoC\nStart date: 2018-09-01\nEnd date: 2020-02-29\nTotal cost: 149994 EUR\nEC maximum contribution: 149994 EUR",
  "question": "Does the project end after the year 2020?"
 },
 {
  "qid": "q3d2b138ea1",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: Kirklees\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group C",
   "Group B",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: the local authority is Derby City, Wakefield or Kirklees\n- Group B: the local authority is Leeds, Erewash or Redditch\n- Group C: the local authority is Wokingham, Portsmouth or Wealden\n- None of these groups: any other is"
 },
 {
  "qid": "qdcceb0c5bf",
  "kind": "choice",
  "text": "Taxon: Pseudocercospora tectonicola\nKingdom: Fungi\nOrder: Mycosphaerellales",
  "question": "Which family is the taxon Pseudocercospora tectonicola placed in?",
  "options": [
   "Phaffomycetaceae",
   "Coniocybaceae",
   "Mycosphaerellaceae",
   "Geoglossaceae"
  ]
 },
 {
  "qid": "qe77a1f5985",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nLocal authority: Newcastle Upon Tyne\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "None of these groups",
   "Group A",
   "Group B",
   "Group C"
  ],
  "definitions": "- Group A: the business type is Restaurant/Cafe/Canteen, Caring Premises or Takeaway/sandwich shop\n- Group B: the business type is Retailers - other, Other catering premises or Pub/bar/nightclub\n- Group C: the business type is Mobile caterer, School/college/university or Retailers - supermarkets/hypermarkets\n- None of these groups: any other is"
 },
 {
  "qid": "q884e2115c6",
  "kind": "choice",
  "text": "City: Jishou\nCountry: China",
  "question": "Which time zone does Jishou use?",
  "options": [
   "Asia/Tashkent",
   "Asia/Tokyo",
   "Asia/Karachi",
   "Asia/Shanghai"
  ]
 }
]
