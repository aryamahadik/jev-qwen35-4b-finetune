# G9 re-read (G5-H blind read) MD-B03 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-B03.json

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
  "qid": "qfc8b897fe2",
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
  "qid": "qfeabe2c680",
  "kind": "yes/no",
  "text": "Index record of a publication\n| Field | Value |\n| --- | --- |\n| Open-access status | gold |\n| Retracted flag | false |\n| References listed | 220 |\n| Distinct countries | 0 |\n| Topic domain | Social Sciences |",
  "question": "Under the card, is this entry published in a fully open venue?",
  "definitions": "- yes: Yes if the open-access status is gold or diamond.\n- no: No if the status is green, hybrid, bronze or closed."
 },
 {
  "qid": "q3d8af0ff84",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\n| Field | Value |\n| --- | --- |\n| Project name | Addtional Financing for the Ghana Energy Development and Access Project (GEDAP) |\n| Region | Western and Central Africa |\n| Reference year | 2026 |\n| Supplemental flag | Y |",
  "question": "Does the project name contain the word 'Health'?"
 },
 {
  "qid": "q6beb766dba",
  "kind": "yes/no",
  "text": "Accession number: 1926.1547\nObject type: Sculpture\nCollection: American - Sculpture\nTechnique: bronze\nCulture: America, Ohio, Cleveland\nDate text: 1925\nDate range: 1925 to 1925\nMeasurements: not listed\nCredit line, first word: Hinman",
  "question": "Does the work's date range start before 1900?"
 },
 {
  "qid": "q9fb28ded98",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\n{\n  \"title\": \"Fear of the Digital Remix\",\n  \"primary_type\": \"Album\",\n  \"secondary_types\": \"Remix\",\n  \"credits\": 1,\n  \"releases\": 1\n}",
  "question": "Is 'Remix' listed among the secondary types?"
 },
 {
  "qid": "q921c5019af",
  "kind": "yes/no",
  "text": "Index record of a publication\n| Field | Value |\n| --- | --- |\n| Work ID | W7211529509 |\n| Publication date | 2008-01-01 |\n| Language code | en |\n| Citation count | 0 |",
  "question": "Does this entry count as highly cited under the card?",
  "definitions": "- yes: Yes if the citation count is 10 or more.\n- no: No if the citation count is below 10."
 },
 {
  "qid": "q97bb859097",
  "kind": "yes/no",
  "text": "Place: Gradačac\nCountry: Bosnia and Herzegovina",
  "question": "Is Gradačac eligible under this rule?",
  "definitions": "- yes: The place's country is Spain, Bosnia and Herzegovina or United States.\n- no: The place's country is any other country."
 },
 {
  "qid": "q63e7dd3506",
  "kind": "yes/no",
  "text": "Catalogue entry for a scholarly work\n| Field | Value |\n| --- | --- |\n| Work type | standard |\n| Distinct countries | 0 |\n| Open-access status | closed |\n| Authors listed | 1 |\n| Topic domain | Physical Sciences |",
  "question": "Would it be so that the record does not fail to give 'bronze' as the open-access status?"
 },
 {
  "qid": "qae2252c9f5",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\n- Event ID = aka2026oqfnbc\n- Magnitude = 2.5\n- Significance score = 96\n- Azimuthal gap (deg) = 232",
  "question": "Is the azimuthal gap 180 degrees or more?"
 },
 {
  "qid": "q801d2d0dd7",
  "kind": "yes/no",
  "text": "Accession number: 1916.1440\nObject type: Embroidery\nCollection: T - Ecclesiastical\nTechnique: Silk and metallic threads: embroidery\nCulture: Italy\nDate text: 1700s\nDate range: 1700 to 1799\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Is the gap between the first and last year above 25 years?",
  "definitions": "- yes: the last year minus the first year of the Date range is more than 25.\n- no: the last year minus the first year of the Date range is 25 or less."
 },
 {
  "qid": "q3725b12f02",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\nTsunami flag 0; PAGER alert none; Location description 68 km SSE of Kokhanok, Alaska; Azimuthal gap (deg) 47.",
  "question": "Is the stated distance to the named place at least 100 km?"
 },
 {
  "qid": "qd6d6c95d32",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nLocal authority: Wirral\nRating: 5",
  "question": "Is the rating at least 3?"
 },
 {
  "qid": "q51168499cc",
  "kind": "yes/no",
  "text": "Release-group record\n{\n  \"first_release_date\": 1995,\n  \"primary_type\": \"Single\",\n  \"releases\": 2,\n  \"tags\": \"trance, electronic, breakbeat, hard trance\",\n  \"tag_count\": 4\n}",
  "question": "Is this entry from the pre-2000 era by the card's rule?",
  "definitions": "- yes: Yes if the first release year is before 2000.\n- no: No if the first release year is 2000 or later."
 },
 {
  "qid": "q5f16641f02",
  "kind": "choice",
  "text": "Place: Mirangaba\nCountry: Brazil",
  "question": "Under the definitions, which group holds the country where Mirangaba lies?",
  "options": [
   "Group C",
   "Group B",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: Japan, Angola or Canada\n- Group B: Brazil, United States or Portugal\n- Group C: Russia, Finland or Myanmar\n- None of these groups: any other country"
 },
 {
  "qid": "qe4441f63e4",
  "kind": "choice",
  "text": "Accession number: 1936.588\nObject type: Print\nCollection: PR - Lithograph\nTechnique: lithograph\nCulture: America\nDate text: 1923\nDate range: 1923 to 1923\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Which curatorial department holds the work?",
  "options": [
   "Japanese Art",
   "Chinese Art",
   "Textiles",
   "Medieval Art",
   "Prints",
   "Drawings",
   "Greek and Roman Art",
   "Photography"
  ]
 },
 {
  "qid": "qc18cc7061b",
  "kind": "yes/no",
  "text": "Bibliographic record\n- Work type = article\n- Publication date = 2013-03-14\n- Distinct countries = 1\n- Distinct institutions = 1\n- Authors listed = 3",
  "question": "Does the entry list more authors than distinct institutions?"
 },
 {
  "qid": "q674ce43dbf",
  "kind": "yes/no",
  "text": "Organization: Northern Ostrobothnia Hospital District",
  "question": "Is Northern Ostrobothnia Hospital District located in United States?"
 },
 {
  "qid": "qfd4651980c",
  "kind": "choice",
  "text": "Taxon: Tichocarpaceae\nKingdom: Plantae",
  "question": "To which phylum does the taxon Tichocarpaceae belong?",
  "options": [
   "Charophyta",
   "Bryophyta",
   "Chlorophyta",
   "Rhodophyta"
  ]
 },
 {
  "qid": "q8f6b3f9b0b",
  "kind": "yes/no",
  "text": "Development project record\n- Region = Europe and Central Asia\n- Lending instrument = Specific Investment Loan\n- Board approval date = 1965-04-29\n- Major themes listed = 0",
  "question": "Was the board approval in July to December?"
 },
 {
  "qid": "q9b6756f2ce",
  "kind": "yes/no",
  "text": "Project ID: 884823\nTitle: Perfused Organs-on-a-Chip integrated with TEER measurement technique: A novel approach towards studying non-targeted drug induced organ tox...",
  "question": "Does the project title have more than 15 words?"
 },
 {
  "qid": "q57edd089a5",
  "kind": "yes/no",
  "text": "Seismic event record\n| Field | Value |\n| --- | --- |\n| Depth (km) | 10.0 |\n| Longitude | -31.134 |\n| Stations used | 52 |\n| Magnitude | 4.8 |\n| Origin time (UTC) | 2025-06-20 20:26:27 |",
  "question": "Is the number of stations used fewer than 50?"
 },
 {
  "qid": "q59d119d3d9",
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
  "qid": "q68b797dd28",
  "kind": "yes/no",
  "text": "Project ID: 801459\nProgramme: Horizon 2020\nFunding scheme: MSCA-COFUND\nCall topic: MSCA-COFUND-2017\nStart date: 2019-04-01\nEnd date: 2024-03-31\nTotal cost: 7080000 EUR\nEC maximum contribution: 3540000 EUR",
  "question": "Is the EC maximum contribution above 1,000,000 EUR?"
 },
 {
  "qid": "q0d3eebd37d",
  "kind": "yes/no",
  "text": "Scholarly work metadata\nWork type review; Reference year 2026; Retracted flag false; Citation count 8; Topic field Neuroscience.",
  "question": "Is this entry highly cited by the card's rule?",
  "definitions": "- yes: Yes if the citation count is 50 or more.\n- no: No if the citation count is below 50."
 },
 {
  "qid": "q0449f16684",
  "kind": "yes/no",
  "text": "GO term: GO:0043751\nName: polyphosphate:AMP phosphotransferase activity\nDefinition: Catalysis of the reaction: (polyphosphate)n + AMP = (polyphosphate)n-1 + ADP.\nDefinition sources: PMID:11237733\nSynonyms (2): \"PAP\" EXACT; \"PPT\" BROAD\nDirect is_a parents (1): phosphotransferase activity, phosphate group as acceptor\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Would it be true that this term does not fail to have a part_of relationship?"
 },
 {
  "qid": "qc95d6c574b",
  "kind": "choice",
  "text": "Bibliographic record\nfield: Neuroscience\nlast_page: 534\npublication_date: 2005-06-01\nreference_year: 2026\nvolume: 74\nfirst_page: 515",
  "question": "Which length class applies to this entry?",
  "options": [
   "short",
   "medium",
   "long"
  ],
  "definitions": "- short: Pick this when the page span (last minus first, plus one) is 1 to 4 pages.\n- medium: Pick this when the span is 5 to 14 pages.\n- long: Pick this when the span is 15 pages or more."
 },
 {
  "qid": "qca4e72f37f",
  "kind": "yes/no",
  "text": "GO term: GO:0060756\nName: foraging behavior\nDefinition: Behavior by which an organism locates food.\nDefinition sources: GOC:dph, GOC:tb\nSynonyms (0): none listed\nDirect is_a parents (1): behavior\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Would you say this term has over 2 listed synonyms?"
 },
 {
  "qid": "qc58763ae96",
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
  "qid": "q9125b86035",
  "kind": "choice",
  "text": "Place: Gangneung\nCountry: South Korea",
  "question": "Which group does the country of Gangneung belong to under these definitions?",
  "options": [
   "Group C",
   "Group B",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: Pakistan, Spain or Brazil\n- Group B: China, Tanzania or Iran\n- Group C: India, South Korea or Philippines\n- None of these groups: any other country"
 },
 {
  "qid": "qca262040e1",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nRating date: March (rating 4)",
  "question": "Was the rating given in the second half of the year?"
 },
 {
  "qid": "q001e8bb243",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\nproject_name: St Maarten Civil Society Partnership Facility for Resilience Project (CSPFRP)\ninstrument: Investment Project Financing\ntotal_usd_m: 7.20\nclosing_date: 2025-03-31\nreference_year: 2026",
  "question": "Does the project commit at least 25 million USD in total?"
 },
 {
  "qid": "q46c9ff04ef",
  "kind": "yes/no",
  "text": "Discography database row\n{\n  \"first_release_date\": \"2021-01-20\",\n  \"title\": \"To Redefine / To Be Defined\",\n  \"credits\": 1,\n  \"tag_count\": 0\n}",
  "question": "Does the first-release year fall in 2020 or after?"
 },
 {
  "qid": "q2c425afb83",
  "kind": "yes/no",
  "text": "Event summary from a seismic network catalogue\nmagnitude: 4.8\nplace: 103 km NNW of Tatsug?, Japan\nnetwork: us\nevent_id: us7000qcbd\nmagnitude_type: mww",
  "question": "Is the stated distance to the named place below 200 km?"
 },
 {
  "qid": "q24f45f8599",
  "kind": "yes/no",
  "text": "GO term: GO:0098814\nName: spontaneous synaptic transmission\nDefinition: The low level of synaptic transmission that occurs via spontaneous neurotransmitter release into the synaptic cleft in the absence of a presynaptic action potential.\nDefinition sources: PMID:20200227\nSynonyms (1): \"basal synaptic transmission\" EXACT\nDirect is_a parents (1): chemical synaptic transmission\nOther relationships: none listed\nSubsets: goslim_synapse\nCross-references (0): none listed",
  "question": "Would you say this term has over 3 cross-references?",
  "definitions": "- yes: the number of cross-references shown is greater than 3.\n- no: the number of cross-references shown is 3 or fewer."
 },
 {
  "qid": "q28602e33b8",
  "kind": "yes/no",
  "text": "Accession number: 1984.70\nObject type: Sculpture\nCollection: China - Song Dynasty\nTechnique: wood with polychromy and gilding\nCulture: China, late Northern Song dynasty (960-1127) - Jin dynasty...\nDate text: late 1100s–1200s\nDate range: 1175 to 1234\nMeasurements: not listed\nCredit line, first word: Purchase",
  "question": "Was this work begun before the year 1800?"
 },
 {
  "qid": "q7fd4083ea9",
  "kind": "choice",
  "text": "Taxon: Entyloma linariae\nKingdom: Fungi",
  "question": "To which phylum does the taxon Entyloma linariae belong?",
  "options": [
   "Basidiomycota",
   "Mucoromycota",
   "Chytridiomycota",
   "Ascomycota"
  ]
 },
 {
  "qid": "q874eba748a",
  "kind": "choice",
  "text": "Place: South Lake Tahoe\nCountry: United States",
  "question": "Which group does the country of South Lake Tahoe belong to under these definitions?",
  "options": [
   "Group C",
   "Group B",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: Thailand, United States or Canada\n- Group B: Brazil, Tanzania or India\n- Group C: China, New Zealand or Mexico\n- None of these groups: any other country"
 },
 {
  "qid": "q050202919c",
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
  "qid": "q6964420a31",
  "kind": "yes/no",
  "text": "Index record of a publication\n- Publication year = 2018\n- Topic field = Agricultural and Biological Sciences\n- Language code = en\n- Venue type = repository\n- Work type = dataset",
  "question": "Does the record give 'dataset' as the work type?"
 },
 {
  "qid": "q1e00dfc356",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\nTitle: Ronchalant\nArtist credits: 1\nFirst release date: 1999\nGenre tags: hip hop",
  "question": "Does the first release date include the month?"
 },
 {
  "qid": "qcff389f7cc",
  "kind": "choice",
  "text": "Project ID: 730840\nProgramme: Horizon 2020\nFunding scheme: Shift2Rail-RIA\nCall topic: S2R-OC-IP2-03-2015\nStart date: 2016-11-01\nEnd date: 2018-10-31\nTotal cost: 499282.5 EUR\nEC maximum contribution: 499282.5 EUR",
  "question": "Which group does the funding scheme belong to?",
  "options": [
   "other schemes",
   "European Research Council (ERC)",
   "research and innovation (RIA, IA)",
   "Marie Sklodowska-Curie (MSCA)",
   "SME instrument (SME)",
   "coordination and support (CSA)"
  ],
  "definitions": "- research and innovation (RIA, IA): scheme RIA, IA, CS2-RIA or CS2-IA\n- coordination and support (CSA): scheme CSA\n- Marie Sklodowska-Curie (MSCA): any scheme code that starts with MSCA\n- European Research Council (ERC): any scheme code that starts with ERC\n- SME instrument (SME): any scheme code that starts with SME\n- other schemes: every other scheme code"
 },
 {
  "qid": "qb0d953d9dc",
  "kind": "yes/no",
  "text": "Campeche is a city in Mexico.",
  "question": "Does Campeche (Mexico) have at most 84,000 inhabitants?"
 },
 {
  "qid": "q638071a3e8",
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
  "qid": "q791bef06e5",
  "kind": "yes/no",
  "text": "Project register entry\n{\n  \"status\": \"Closed\",\n  \"closing_date\": \"2023-06-30\",\n  \"major_sectors\": 1,\n  \"themes\": 0\n}",
  "question": "Under the card, is this entry an open project?",
  "definitions": "- yes: Yes if the status is Active or Pipeline.\n- no: No if the status is Closed or Dropped."
 },
 {
  "qid": "q3d94ed69b1",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nLocal authority: Mid Suffolk\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "Group A",
   "None of these groups",
   "Group C",
   "Group B"
  ],
  "definitions": "- Group A: the business type is Caring Premises, Retailers - other or Mobile caterer\n- Group B: the business type is Retailers - supermarkets/hypermarkets, Farmers/growers or Takeaway/sandwich shop\n- Group C: the business type is Manufacturers/packers, School/college/university or Restaurant/Cafe/Canteen\n- None of these groups: any other is"
 },
 {
  "qid": "q47eec04cf8",
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
  "qid": "qebddc50c5f",
  "kind": "yes/no",
  "text": "Title: Standing Female Figure\nAccession number: 1990.169\nObject type: Sculpture\nCollection: AA - Mesoamerica\nTechnique: stone\nCulture: Mexico, Gulf Coast, Huastec\nDate text: c. 1000–1500\nDate range: 1000 to 1500\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Does the title have more than 4 words?"
 },
 {
  "qid": "qf454813b95",
  "kind": "yes/no",
  "text": "Discography database row\nFirst release date 2021-03-05; Primary type EP; Artist credits 1; Release statuses Official.",
  "question": "Does the first release date include the month?"
 },
 {
  "qid": "qe1c6f3490c",
  "kind": "choice",
  "text": "Event summary from a seismic network catalogue\norigin_time: 2026-05-17 21:11:16\nnetwork: us\nmagnitude: 4.1\nlatitude: -25.868\ndepth_km: 530.6",
  "question": "Which six-hour UTC slot does this entry fall in?",
  "options": [
   "00-05",
   "06-11",
   "12-17",
   "18-23"
  ]
 },
 {
  "qid": "q2fb9ddf8fd",
  "kind": "choice",
  "text": "Bibliographic record\n| Field | Value |\n| --- | --- |\n| Authors listed | 55 |\n| Licence | cc-by |\n| Version | publishedVersion |\n| Volume | 208 |",
  "question": "Which team size class does this entry fall in?",
  "options": [
   "solo",
   "small",
   "large",
   "consortium"
  ],
  "definitions": "- solo: Pick this when exactly 1 author is listed.\n- small: Pick this when 2 to 4 authors are listed.\n- large: Pick this when 5 to 10 authors are listed.\n- consortium: Pick this when more than 10 authors are listed."
 }
]
