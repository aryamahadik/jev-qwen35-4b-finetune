# G9 re-read (G5-H blind read) MD-B00 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-B00.json

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
  "qid": "q8dc945209e",
  "kind": "yes/no",
  "text": "Accession number: 2010.429\nObject type: Sculpture\nCollection: African Art\nTechnique: Wood, possibly ceramic, and copper alloy\nCulture: Africa, Central Africa, Republic of the Congo, Beembe-style...\nDate text: late 1800s-early 1900s\nDate range: 1880 to 1920\nMeasurements: not listed\nCredit line, first word: René",
  "question": "Was this work begun before the year 1800?"
 },
 {
  "qid": "q094000e58b",
  "kind": "choice",
  "text": "Organization: Trinity County Office of Education\nCountry: United States",
  "question": "Which group does Trinity County Office of Education fall into under these definitions?",
  "options": [
   "Group B",
   "Group A",
   "Group C",
   "None of these groups"
  ],
  "definitions": "- Group A: United States, China or United Kingdom\n- Group B: South Africa, New Zealand or Japan\n- Group C: Mexico, Egypt or Brazil\n- None of these groups: any other country"
 },
 {
  "qid": "q12bffc1157",
  "kind": "choice",
  "text": "Lending operation record from a development-bank register\nmajor_sectors: 0\ncountry: Eastern and Southern Africa\nenv_category: A\ninstrument: Investment Project Financing",
  "question": "Which assessment level applies to this entry?",
  "options": [
   "full assessment",
   "partial assessment",
   "little or no assessment"
  ],
  "definitions": "- full assessment: Pick this when the environmental category is A.\n- partial assessment: Pick this when the category is B.\n- little or no assessment: Pick this when the category is C."
 },
 {
  "qid": "q2e7601b189",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\n{\n  \"network\": \"nc\",\n  \"latitude\": 40.285,\n  \"event_id\": \"nc75436587\",\n  \"place\": \"20 km WSW of Petrolia, CA\"\n}",
  "question": "Is it true that the contributing network code is not 'nc'?"
 },
 {
  "qid": "q3984785f9d",
  "kind": "yes/no",
  "text": "City: Itapetinga\nCountry: Brazil",
  "question": "Is Itapetinga (Brazil) located at most 170 m above sea level?"
 },
 {
  "qid": "q7b35a7dfc1",
  "kind": "yes/no",
  "text": "Project ID: 817578\nProgramme: Horizon 2020\nFunding scheme: RIA\nCall topic: BG-08-2018-2019\nStart date: 2019-06-01\nEnd date: 2023-11-30\nTotal cost: 11074400 EUR\nEC maximum contribution: 11000000 EUR",
  "question": "Is the EC maximum contribution above 5,000,000 EUR?"
 },
 {
  "qid": "qb33d89abc1",
  "kind": "yes/no",
  "text": "GO term: GO:0048348\nName: paraxial mesodermal cell fate specification\nDefinition: The process in which a cell becomes capable of differentiating autonomously into a paraxial mesoderm cell in an environment that is neutral with respect to the developmental pathway; upon specification, the cell fate can be reversed.\nDefinition sources: GOC:dgh\nSynonyms (0): none listed\nDirect is_a parents (1): mesodermal cell fate specification\nOther relationships: part_of paraxial mesodermal cell fate commitment\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Is the definition longer than 20 words?",
  "definitions": "- yes: the definition text (without its source list) has more than 20 words.\n- no: the definition text (without its source list) has 20 words or fewer."
 },
 {
  "qid": "qf5e993e598",
  "kind": "yes/no",
  "text": "Development project record\nIDA commitment (USD million) 0.00; Total commitment (USD million) 25.20; Reference year 2026; Lending instrument Program-for-Results Financing.",
  "question": "Is the recorded lending instrument Program-for-Results Financing?"
 },
 {
  "qid": "q7d90d7069e",
  "kind": "choice",
  "text": "Project ID: 707932\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-ST\nCall topic: MSCA-IF-2015-EF\nStart date: 2016-04-01\nEnd date: 2018-07-15\nTotal cost: 171460.8 EUR\nEC maximum contribution: 171460.8 EUR",
  "question": "Which quarter of the year does the project start in?",
  "options": [
   "Q1 (January to March)",
   "Q3 (July to September)",
   "Q4 (October to December)",
   "Q2 (April to June)"
  ]
 },
 {
  "qid": "qfcbd09b9fb",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Retailers - other\nLocal authority: Hartlepool\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group B",
   "Group C",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: the business type is Distributors/Transporters, Manufacturers/packers or Restaurant/Cafe/Canteen\n- Group B: the business type is Mobile caterer, Pub/bar/nightclub or Hotel/bed & breakfast/guest house\n- Group C: the business type is Retailers - other, Other catering premises or School/college/university\n- None of these groups: any other is"
 },
 {
  "qid": "q1d33a841b0",
  "kind": "choice",
  "text": "Organization: Spero Therapeutics (United States)\nCountry: United States",
  "question": "Under the definitions, which group holds Spero Therapeutics (United States)?",
  "options": [
   "Group C",
   "Group A",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: United States, United Kingdom or Gabon\n- Group B: Japan, Indonesia or Ireland\n- Group C: France, China or The Netherlands\n- None of these groups: any other country"
 },
 {
  "qid": "qb0f449b40d",
  "kind": "yes/no",
  "text": "Development project record\n{\n  \"region\": \"Eastern and Southern Africa\",\n  \"instrument\": \"Specific Investment Loan\",\n  \"reference_year\": 2026,\n  \"major_sectors\": 0\n}",
  "question": "Does the record give 'Specific Investment Loan' as the lending instrument?"
 },
 {
  "qid": "q298eb96e67",
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
  "qid": "q2814681f72",
  "kind": "choice",
  "text": "Organization: Institute for Research and Development\nCountry: Sri Lanka",
  "question": "Which group does Institute for Research and Development fall into under these definitions?",
  "options": [
   "Group C",
   "Group A",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: Sri Lanka, United States or Russia\n- Group B: Germany, Canada or Switzerland\n- Group C: Papua New Guinea, Sweden or Brazil\n- None of these groups: any other country"
 },
 {
  "qid": "q67441b6080",
  "kind": "yes/no",
  "text": "Project and operations register row\n| Field | Value |\n| --- | --- |\n| Status | Closed |\n| Country | North Macedonia |\n| Major themes listed | 2 |\n| Environmental category | C |\n| IBRD commitment (USD million) | 0.00 |",
  "question": "Does the record give 'Dropped' as the project status?"
 },
 {
  "qid": "q2fb8e298f5",
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
  "qid": "qe0e4fb7019",
  "kind": "yes/no",
  "text": "Taxon: Hoilungia hongkongensis\nKingdom: Animalia\nClass: Uniplacotomia",
  "question": "Is Hoilungia hongkongensis eligible under the rule?",
  "definitions": "- yes: The taxon's class is Palaeacanthocephala, Pycnogonida or Eurotatoria.\n- no: The taxon's class is any other class."
 },
 {
  "qid": "q3a281d1365",
  "kind": "choice",
  "text": "Organization: Open Group\nCountry: France",
  "question": "Which type does the registry give for Open Group (France)?",
  "options": [
   "company",
   "government",
   "education",
   "other"
  ]
 },
 {
  "qid": "q8ee8b2a60c",
  "kind": "yes/no",
  "text": "Seismic event record\nstations: 55\nsignificance: 312\norigin_time: 2025-07-18 07:23:45\nlatitude: -23.689\nplace: south of the Fiji Islands",
  "question": "Does the entry list 500 or more significance points?"
 },
 {
  "qid": "q578da8514d",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\n{\n  \"place\": \"44 km W of Masachapa, Nicaragua\",\n  \"origin_time\": \"2013-06-15 17:34:27\",\n  \"felt_reports\": 54,\n  \"tsunami_flag\": 1,\n  \"magnitude_type\": \"mww\"\n}",
  "question": "Is the tsunami flag set to 1?"
 },
 {
  "qid": "q1f7530793e",
  "kind": "choice",
  "text": "Organization: Peru Public Library\nCountry: United States",
  "question": "Which type does the registry give for Peru Public Library (United States)?",
  "options": [
   "nonprofit",
   "education",
   "archive",
   "other"
  ]
 },
 {
  "qid": "q7de8a8b2e8",
  "kind": "yes/no",
  "text": "GO term: GO:0060531\nName: obsolete neuroendocrine cell differentiation involved in prostate gland acinus development\nDefinition: OBSOLETE. The process in which relatively unspecialized cells acquires specialized structural and functions of a neuroendocrine cell of the prostate gland acinus.\nDefinition sources: GOC:dph, PMID:18977204",
  "question": "Does this obsolete term name a replacement term?"
 },
 {
  "qid": "qe8eec1fcaa",
  "kind": "yes/no",
  "text": "Organization: Alcontrol Laboratories (Norway)\nCountry: Norway",
  "question": "Was Alcontrol Laboratories (Norway) (Norway) established before 1990?"
 },
 {
  "qid": "q7645ce2b5a",
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
  "qid": "qae28a9be29",
  "kind": "choice",
  "text": "Organization: Riverstone Senior Life Services\nCountry: United States",
  "question": "Under the definitions, which group holds Riverstone Senior Life Services?",
  "options": [
   "None of these groups",
   "Group A",
   "Group B",
   "Group C"
  ],
  "definitions": "- Group A: France, United States or Nigeria\n- Group B: Portugal, China or Austria\n- Group C: Iran, United Kingdom or Ireland\n- None of these groups: any other country"
 },
 {
  "qid": "qc51a6edf3c",
  "kind": "yes/no",
  "text": "Project ID: 714478\nProgramme: Horizon 2020\nFunding scheme: ERC-STG\nCall topic: ERC-2016-STG\nStart date: 2017-01-01\nEnd date: 2022-12-31\nTotal cost: 1498337 EUR\nEC maximum contribution: 1498337 EUR",
  "question": "Is the EC maximum contribution above 2,000,000 EUR?",
  "definitions": "- yes: the EC maximum contribution is greater than 2,000,000 EUR.\n- no: the EC maximum contribution is 2,000,000 EUR or less."
 },
 {
  "qid": "qb259b3d82d",
  "kind": "yes/no",
  "text": "Index record of a publication\n- Distinct countries = 2\n- Topic domain = Physical Sciences\n- References listed = 0\n- Work type = preprint",
  "question": "Is this entry an international collaboration by the card's rule?",
  "definitions": "- yes: Yes if two or more distinct countries are listed.\n- no: No if zero or one country is listed."
 },
 {
  "qid": "q90b760b06d",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nRating date: September (rating 5)",
  "question": "Was the rating given in the first half of the year?"
 },
 {
  "qid": "qfb46fae7bf",
  "kind": "yes/no",
  "text": "Organization: Yo San University\nCountry: United States",
  "question": "Does Yo San University meet this rule?",
  "definitions": "- yes: The organization is located in South Korea, Australia or Ireland.\n- no: The organization is located in any other country."
 },
 {
  "qid": "q7b82fc0b83",
  "kind": "choice",
  "text": "City: Vespasiano\nCountry: Brazil",
  "question": "Which time zone is Vespasiano in?",
  "options": [
   "America/Sao_Paulo",
   "America/Bahia",
   "America/Recife",
   "America/Santarem"
  ]
 },
 {
  "qid": "q581a573bba",
  "kind": "choice",
  "text": "Project and operations register row\nRegion Latin America and Caribbean; Supplemental flag N; Reference year 2026; Lending instrument Financial Intermediary Loan.",
  "question": "Which instrument family does this entry fall in?",
  "options": [
   "results-based",
   "technical or other",
   "investment",
   "policy-based"
  ],
  "definitions": "- investment: Pick this for Investment Project Financing, Specific Investment Loan or Sector Investment and Maintenance Loan.\n- policy-based: Pick this for Development Policy Lending or Structural Adjustment Loan.\n- results-based: Pick this for Program-for-Results Financing.\n- technical or other: Pick this for Technical Assistance Loan, Financial Intermediary Loan or Emergency Recovery Loan."
 },
 {
  "qid": "q66f11a6cc1",
  "kind": "choice",
  "text": "Organization: Gansu Province Computing Center\nCountry: China",
  "question": "Under the definitions, which group holds Gansu Province Computing Center?",
  "options": [
   "Group C",
   "Group A",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: Mexico, Türkiye or Kosovo\n- Group B: Finland, Austria or China\n- Group C: United States, Spain or Russia\n- None of these groups: any other country"
 },
 {
  "qid": "q47d6587631",
  "kind": "yes/no",
  "text": "Catalogue entry for a scholarly work\n| Field | Value |\n| --- | --- |\n| Work ID | W2783719019 |\n| Open-access status | gold |\n| Citation count | 75 |\n| References listed | 68 |\n| Volume | 8 |",
  "question": "Does the entry list 5 or more references?"
 },
 {
  "qid": "q3522bdb02e",
  "kind": "choice",
  "text": "Organization: Taiz University\nCountry: Yemen",
  "question": "Under the definitions, which group holds Taiz University?",
  "options": [
   "Group C",
   "None of these groups",
   "Group B",
   "Group A"
  ],
  "definitions": "- Group A: Russia, New Zealand or Italy\n- Group B: Germany, Poland or United States\n- Group C: Nigeria, Portugal or Yemen\n- None of these groups: any other country"
 },
 {
  "qid": "q3c5cff5204",
  "kind": "yes/no",
  "text": "Place: Zhangjiachuan\nCountry: China\nFeature code (record): PPLA3",
  "question": "Does Zhangjiachuan meet this rule?",
  "definitions": "- yes: The place's feature code is PPLC, PPL or PPLA2.\n- no: The place's feature code is any other code."
 },
 {
  "qid": "q945d6ab3de",
  "kind": "choice",
  "text": "Place: Bemetāra\nCountry: India",
  "question": "Under the definitions, which group holds the country where Bemetāra lies?",
  "options": [
   "Group A",
   "None of these groups",
   "Group B",
   "Group C"
  ],
  "definitions": "- Group A: Australia, Honduras or Estonia\n- Group B: Germany, Guatemala or Iran\n- Group C: United Arab Emirates, Guinea or India\n- None of these groups: any other country"
 },
 {
  "qid": "q120b0b6441",
  "kind": "choice",
  "text": "Organization: Children's Medical Center\nCountry: Iran",
  "question": "In which period was Children's Medical Center (Iran) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "before 1800",
   "1800-1899"
  ]
 },
 {
  "qid": "q5d02f43eb1",
  "kind": "yes/no",
  "text": "GO term: GO:0140168\nName: nuclear ribonucleoprotein granule\nDefinition: A ribonucleoprotein granule located in the nucleus.\nDefinition sources: PMID:32475683, PMID:35355287, PMID:37890457\nSynonyms (2): \"nuclear RNA granule\" NARROW; \"nuclear RNP granule\" EXACT\nDirect is_a parents (2): nuclear body; ribonucleoprotein granule\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Does this GO term have more than 1 listed synonyms?"
 },
 {
  "qid": "q5d284e0eae",
  "kind": "yes/no",
  "text": "Accession number: 1971.155\nObject type: Sculpture\nCollection: Oceanic Art\nTechnique: wood\nCulture: Melanesia, New Guinea, Massim Area, Trobriand Islands, 20th...\nDate text: before 1930\nDate range: 1900 to 1930\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Was this work begun before the year 1900?"
 },
 {
  "qid": "q5abf1e908e",
  "kind": "yes/no",
  "text": "Seismic event record\nazimuthal_gap: 198\nlatitude: 19.905\nsignificance: 119\nstations: 55",
  "question": "Is the azimuthal gap 180 degrees or more?"
 },
 {
  "qid": "qe03c90ffd5",
  "kind": "yes/no",
  "text": "Organization: Dr. Siyami Ersek Göğüs Kalp Ve Damar Cerrahisi Eğitim Ve Araştırma Hastanesi\nCountry: Türkiye",
  "question": "Does Dr. Siyami Ersek Göğüs Kalp Ve Damar Cerrahisi Eğitim Ve Araştırma Hastanesi meet this rule?",
  "definitions": "- yes: The organization is located in Russia, The Netherlands or United States.\n- no: The organization is located in any other country."
 },
 {
  "qid": "q38701bee44",
  "kind": "yes/no",
  "text": "Accession number: 2012.52.a\nObject type: Sculpture\nCollection: MED - Romanesque\nTechnique: polychrome wood (walnut)\nCulture: France, Auvergne\nDate text: c. 1150–1200\nDate range: 1150 to 1200\nMeasurements: not listed\nCredit line, first word: Severance",
  "question": "Was this work begun before the year 1500?"
 },
 {
  "qid": "q5d03c0cc30",
  "kind": "yes/no",
  "text": "Event summary from a seismic network catalogue\n- Magnitude = 4.7\n- Contributing network = us\n- Significance score = 340\n- Origin time (UTC) = 2026-06-28 02:39:47",
  "question": "Would it be accurate to say that the event did not fail to occur in January to June (UTC)?"
 },
 {
  "qid": "q2ec7db374a",
  "kind": "yes/no",
  "text": "Accession number: 1944.184.1\nObject type: Ceramic\nCollection: China - Qing Dynasty\nTechnique: porcelain with famille rose overglaze enamel decoration\nCulture: China, Jiangxi province, Jingdezhen, Qing dynasty (1644-191...\nDate text: 1736–95\nDate range: 1736 to 1795\nMeasurements: not listed\nCredit line, first word: Elisabeth",
  "question": "Was this work begun before the year 1700?",
  "definitions": "- yes: the first year of the Date range is earlier than 1700.\n- no: the first year of the Date range is 1700 or later."
 },
 {
  "qid": "qaf44fd9c12",
  "kind": "choice",
  "text": "Accession number: 2024.150.14\nObject type: Photograph\nCollection: PH - Russian 20th Century\nTechnique: albumen print from glass negative, hand-colored\nCulture: Russia\nDate text: c. 1900\nDate range: 1895 to 1905\nMeasurements: not listed\nCredit line, first word: Severance",
  "question": "Which medium class does the technique text fall into?",
  "options": [
   "ceramic or glass",
   "metal",
   "other",
   "stone",
   "ink, watercolor or tempera",
   "textile",
   "oil paint"
  ],
  "definitions": "- oil paint: the Technique text contains 'oil' (checked first)\n- ink, watercolor or tempera: else it contains ink, watercolor, gouache, tempera or wash\n- metal: else it contains bronze, gold, silver, iron, copper, brass, steel, pewter or gilt\n- stone: else it contains marble, limestone, granite, sandstone, alabaster, stone, jade or basalt\n- ceramic or glass: else it contains porcelain, earthenware, stoneware, ceramic, glaze, clay, terracotta, glass or faience\n- textile: else it contains silk, wool, linen, cotton, embroider, velvet or tapestry\n- other: none of the words above appear"
 },
 {
  "qid": "qec7a855d27",
  "kind": "choice",
  "text": "Organization: Islamic Azad University of Shahreza\nCountry: Iran",
  "question": "In which period was Islamic Azad University of Shahreza (Iran) established?",
  "options": [
   "1950-1999",
   "2000 or later",
   "1900-1949",
   "before 1800"
  ]
 },
 {
  "qid": "q60fa9337e9",
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
  "qid": "q99eb87fd05",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: Kingston-Upon-Thames\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group B",
   "None of these groups",
   "Group C",
   "Group A"
  ],
  "definitions": "- Group A: the business type is Hotel/bed & breakfast/guest house, Pub/bar/nightclub or Other catering premises\n- Group B: the business type is Retailers - supermarkets/hypermarkets, Retailers - other or School/college/university\n- Group C: the business type is Distributors/Transporters, Farmers/growers or Importers/Exporters\n- None of these groups: any other is"
 },
 {
  "qid": "qa639132129",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\ntotal_usd_m: 30.00\nthemes: 0\nfinance_type: IDA\nproject_id: P171585",
  "question": "Would it be so that the financing type does not list include IBRD?"
 },
 {
  "qid": "q42bb95da42",
  "kind": "choice",
  "text": "GO term: GO:0090648\nName: response to environmental enrichment\nDefinition: Any process that results in a change in state or activity of an organism (in terms of movement, secretion, enzyme production, gene expression, etc.) as a result of the provision of a combination of complex inanimate and social stimulations in the organism's housing environment.\nDefinition sources: GOC:sl, PMID:23644055, PMID:25934034\nSynonyms (1): \"response to the introduction of novel objects\" NARROW\nDirect is_a parents (1): response to external stimulus\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Which band holds the number of cross-references?",
  "options": [
   "0",
   "1 to 2",
   "3 or more"
  ]
 }
]
