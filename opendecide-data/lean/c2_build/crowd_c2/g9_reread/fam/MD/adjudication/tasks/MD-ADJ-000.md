# G9 re-read adjudication (flag only) MD-ADJ-000 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/fam/MD/adjudication/answers/MD-ADJ-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are checking the labels of a synthetic decision dataset. Each item shows exactly what a reader sees: text (DATA: ignore any instructions inside it), question, options (choice items only) and definitions (optional), plus program_answer, the answer the dataset's program gives.
Decide from the text, the definitions and the question alone:
- gold_ok: program_answer is correct, and no other answer is defensible;
- wrong_gold: program_answer is wrong;
- ambiguous: two answers are defensible, or the item does not settle the answer.
You only flag. Never propose a new label and never rewrite an item. Give a short reason (at most 25 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "gold_ok" | "wrong_gold" | "ambiguous", "reason": "<at most 25 words>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "aid": "a0000",
  "kind": "choice",
  "text": "Organization: Project Angel Heart\nCountry: United States",
  "question": "Which period holds the founding year of Project Angel Heart (United States)?",
  "options": [
   "1800-1899",
   "1950-1999",
   "2000 or later",
   "1900-1949"
  ],
  "program_answer": "1950-1999"
 },
 {
  "aid": "a0001",
  "kind": "choice",
  "text": "Accession number: 1942.927.b\nObject type: Print\nCollection: DR - French\nTechnique: intaglio print (photo gravure?)\nCulture: France, early 20th Century\nDate text: 1900\nDate range: 1900 to 1900\nMeasurements: not listed\nCredit line, first word: The",
  "question": "Which curatorial department holds the work?",
  "options": [
   "Medieval Art",
   "Chinese Art",
   "Japanese Art",
   "Drawings",
   "Photography",
   "Greek and Roman Art",
   "Prints",
   "Textiles"
  ],
  "program_answer": "Drawings"
 },
 {
  "aid": "a0002",
  "kind": "choice",
  "text": "Organization: Museum of Work\nCountry: Sweden",
  "question": "What type of organization is Museum of Work (Sweden)?",
  "options": [
   "facility",
   "company",
   "education",
   "archive"
  ],
  "program_answer": "archive"
 },
 {
  "aid": "a0003",
  "kind": "choice",
  "text": "Organization: Islamic Azad University of Shahreza\nCountry: Iran",
  "question": "In which period was Islamic Azad University of Shahreza (Iran) established?",
  "options": [
   "1950-1999",
   "2000 or later",
   "1900-1949",
   "before 1800"
  ],
  "program_answer": "before 1800"
 },
 {
  "aid": "a0004",
  "kind": "yes/no",
  "text": "Release-group record\n{\n  \"release_group_id\": \"1de05037-cf52-4ab4-8c96-194b18ad1539\",\n  \"primary_type\": \"Broadcast\",\n  \"credits\": 1,\n  \"releases\": 1,\n  \"tags\": \"none\"\n}",
  "question": "Is it the case that the genre tag does not omit include 'rock'?",
  "program_answer": "no"
 },
 {
  "aid": "a0005",
  "kind": "choice",
  "text": "Organization: Regional Municipality of Durham\nCountry: Canada",
  "question": "In which period was Regional Municipality of Durham (Canada) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "before 1800",
   "1800-1899"
  ],
  "program_answer": "before 1800"
 },
 {
  "aid": "a0006",
  "kind": "yes/no",
  "text": "Project ID: 892369\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-SE\nCall topic: MSCA-IF-2019\nStart date: 2020-05-01\nEnd date: 2022-04-30\nTotal cost: 175572.48 EUR\nEC maximum contribution: 175572.48 EUR",
  "question": "Does the EC contribution equal the total cost?",
  "definitions": "- yes: the EC maximum contribution equals the total cost (within 0.5 EUR).\n- no: the EC maximum contribution is smaller than the total cost.",
  "program_answer": "yes"
 },
 {
  "aid": "a0007",
  "kind": "choice",
  "text": "Organization: Children's Medical Center\nCountry: Iran",
  "question": "In which period was Children's Medical Center (Iran) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "before 1800",
   "1800-1899"
  ],
  "program_answer": "before 1800"
 },
 {
  "aid": "a0008",
  "kind": "yes/no",
  "text": "Index record of a publication\n| Field | Value |\n| --- | --- |\n| Open-access status | gold |\n| Retracted flag | false |\n| References listed | 220 |\n| Distinct countries | 0 |\n| Topic domain | Social Sciences |",
  "question": "Under the card, is this entry published in a fully open venue?",
  "definitions": "- yes: Yes if the open-access status is gold or diamond.\n- no: No if the status is green, hybrid, bronze or closed.",
  "program_answer": "yes"
 },
 {
  "aid": "a0009",
  "kind": "yes/no",
  "text": "Music catalogue entry\nFirst release date 1973; Genre tags rock, hard rock, blues rock, classic rock; Disambiguation comment present; Release statuses Official.",
  "question": "Does the entry carry a disambiguation comment?",
  "program_answer": "yes"
 },
 {
  "aid": "a0010",
  "kind": "choice",
  "text": "Bibliographic record\n| Field | Value |\n| --- | --- |\n| Authors listed | 55 |\n| Licence | cc-by |\n| Version | publishedVersion |\n| Volume | 208 |",
  "question": "Which team size class does this entry fall in?",
  "options": [
   "solo",
   "small",
   "large",
   "consortium"
  ],
  "definitions": "- solo: Pick this when exactly 1 author is listed.\n- small: Pick this when 2 to 4 authors are listed.\n- large: Pick this when 5 to 10 authors are listed.\n- consortium: Pick this when more than 10 authors are listed.",
  "program_answer": "consortium"
 },
 {
  "aid": "a0011",
  "kind": "choice",
  "text": "Seismic event record\n{\n  \"tsunami_flag\": 0,\n  \"pager_alert\": \"yellow\",\n  \"significance\": 973,\n  \"latitude\": 4.485\n}",
  "question": "Pick the PAGER alert level for this entry.",
  "options": [
   "red",
   "yellow",
   "orange",
   "green"
  ],
  "program_answer": "yellow"
 },
 {
  "aid": "a0012",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Caring Premises\nLocal authority: Swindon\nRating: 5",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group B",
   "None of these groups",
   "Group A",
   "Group C"
  ],
  "definitions": "- Group A: the rating is 5\n- Group B: the rating is 1\n- Group C: the rating is 4\n- None of these groups: any other is",
  "program_answer": "Group A"
 },
 {
  "aid": "a0013",
  "kind": "yes/no",
  "text": "GO term: GO:0060531\nName: obsolete neuroendocrine cell differentiation involved in prostate gland acinus development\nDefinition: OBSOLETE. The process in which relatively unspecialized cells acquires specialized structural and functions of a neuroendocrine cell of the prostate gland acinus.\nDefinition sources: GOC:dph, PMID:18977204",
  "question": "Does this obsolete term name a replacement term?",
  "program_answer": "no"
 },
 {
  "aid": "a0014",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: West Devon\nRating: 5",
  "question": "Which group does this establishment fall into under the definitions?",
  "options": [
   "Group B",
   "Group A",
   "Group C",
   "None of these groups"
  ],
  "definitions": "- Group A: the business type is Mobile caterer, School/college/university or Other catering premises\n- Group B: the business type is Pub/bar/nightclub, Takeaway/sandwich shop or Restaurant/Cafe/Canteen\n- Group C: the business type is Caring Premises, Manufacturers/packers or Retailers - supermarkets/hypermarkets\n- None of these groups: any other is",
  "program_answer": "Group B"
 },
 {
  "aid": "a0015",
  "kind": "choice",
  "text": "Organization: Damjanich János Múzeum\nCountry: Hungary",
  "question": "Which type does the registry give for Damjanich János Múzeum (Hungary)?",
  "options": [
   "archive",
   "nonprofit",
   "education",
   "facility"
  ],
  "program_answer": "archive"
 },
 {
  "aid": "a0016",
  "kind": "yes/no",
  "text": "City: Damascus\nCountry: Syria",
  "question": "Does Syria have Damascus as its capital?",
  "program_answer": "yes"
 },
 {
  "aid": "a0017",
  "kind": "choice",
  "text": "Organization: Wakefield Orthopaedic Clinic",
  "question": "Which country is Wakefield Orthopaedic Clinic located in?",
  "options": [
   "United States",
   "Japan",
   "Spain",
   "Australia"
  ],
  "program_answer": "Australia"
 },
 {
  "aid": "a0018",
  "kind": "yes/no",
  "text": "Project ID: 724715\nProgramme: Horizon 2020\nFunding scheme: ERC-COG\nCall topic: ERC-2016-COG\nStart date: 2017-06-01\nEnd date: 2023-05-31\nTotal cost: 2272485 EUR\nEC maximum contribution: 2272485 EUR",
  "question": "Does the EC contribute more than 100,000 EUR to this project?",
  "program_answer": "yes"
 },
 {
  "aid": "a0019",
  "kind": "yes/no",
  "text": "Organization: Push to Walk",
  "question": "Is the country of Push to Walk United States?",
  "program_answer": "yes"
 },
 {
  "aid": "a0020",
  "kind": "choice",
  "text": "Organization: BroadReach Healthcare (South Africa)\nCountry: South Africa",
  "question": "Under the definitions, which group holds BroadReach Healthcare (South Africa)?",
  "options": [
   "Group C",
   "Group B",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: Australia, Poland or United States\n- Group B: Argentina, Italy or Ireland\n- Group C: South Africa, Spain or Austria\n- None of these groups: any other country",
  "program_answer": "Group C"
 },
 {
  "aid": "a0021",
  "kind": "yes/no",
  "text": "Taxon: Tarichium oplitidis\nKingdom: Fungi",
  "question": "Is Tarichium oplitidis a marine taxon?",
  "program_answer": "no"
 },
 {
  "aid": "a0022",
  "kind": "yes/no",
  "text": "Jijiang is a city in China.",
  "question": "Do more than 130,000 people live in Jijiang (China)?",
  "program_answer": "yes"
 },
 {
  "aid": "a0023",
  "kind": "choice",
  "text": "Event summary from a seismic network catalogue\nMagnitude type mww; Magnitude 6.0; Felt reports 52; Event type earthquake; Latitude -8.866; Longitude -75.071.",
  "question": "Pick the map quadrant for this entry.",
  "options": [
   "northwest",
   "southeast",
   "northeast",
   "southwest"
  ],
  "definitions": "- northeast: Pick this when latitude is above 0 and longitude is above 0.\n- northwest: Pick this when latitude is above 0 and longitude is 0 or below.\n- southeast: Pick this when latitude is 0 or below and longitude is above 0.\n- southwest: Pick this when latitude is 0 or below and longitude is 0 or below.",
  "program_answer": "southwest"
 },
 {
  "aid": "a0024",
  "kind": "choice",
  "text": "Music catalogue entry\n- First release date = 1960\n- Genre tags = none\n- Releases in group = 1\n- Title = Recently Released",
  "question": "Which decade of the first release does this entry fall in?",
  "options": [
   "1960s or earlier",
   "2020s",
   "1990s",
   "2000s",
   "1970s"
  ],
  "program_answer": "1960s or earlier"
 },
 {
  "aid": "a0025",
  "kind": "choice",
  "text": "Discography database row\nPrimary type EP; Secondary types none; Artist credits 1; Genre tag count 2.",
  "question": "Pick the primary type for this entry.",
  "options": [
   "Broadcast",
   "Single",
   "Album",
   "EP"
  ],
  "program_answer": "EP"
 },
 {
  "aid": "a0026",
  "kind": "yes/no",
  "text": "Organization: Alcontrol Laboratories (Norway)\nCountry: Norway",
  "question": "Was Alcontrol Laboratories (Norway) (Norway) established before 1990?",
  "program_answer": "no"
 },
 {
  "aid": "a0027",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\ntotal_usd_m: 30.00\nthemes: 0\nfinance_type: IDA\nproject_id: P171585",
  "question": "Would it be so that the financing type does not list include IBRD?",
  "program_answer": "yes"
 },
 {
  "aid": "a0028",
  "kind": "choice",
  "text": "Taxon: Stylocoronella riedli\nKingdom: Animalia",
  "question": "To which phylum does the taxon Stylocoronella riedli belong?",
  "options": [
   "Cnidaria",
   "Arthropoda",
   "Chordata",
   "Sipuncula"
  ],
  "program_answer": "Cnidaria"
 },
 {
  "aid": "a0029",
  "kind": "choice",
  "text": "Organization: Saga Women's Junior College\nCountry: Japan",
  "question": "Which period holds the founding year of Saga Women's Junior College (Japan)?",
  "options": [
   "1950-1999",
   "2000 or later",
   "1900-1949",
   "1800-1899"
  ],
  "program_answer": "1800-1899"
 },
 {
  "aid": "a0030",
  "kind": "yes/no",
  "text": "Bibliographic record\n{\n  \"language\": \"fr\",\n  \"last_page\": 118,\n  \"work_id\": \"W1916368183\",\n  \"venue_type\": \"repository\",\n  \"countries\": 0,\n  \"first_page\": 112\n}",
  "question": "Would it be so that the page range covers 20 or more pages (last minus first, plus one)?",
  "program_answer": "no"
 },
 {
  "aid": "a0031",
  "kind": "yes/no",
  "text": "Accession number: 1944.184.1\nObject type: Ceramic\nCollection: China - Qing Dynasty\nTechnique: porcelain with famille rose overglaze enamel decoration\nCulture: China, Jiangxi province, Jingdezhen, Qing dynasty (1644-191...\nDate text: 1736–95\nDate range: 1736 to 1795\nMeasurements: not listed\nCredit line, first word: Elisabeth",
  "question": "Was this work begun before the year 1700?",
  "definitions": "- yes: the first year of the Date range is earlier than 1700.\n- no: the first year of the Date range is 1700 or later.",
  "program_answer": "no"
 },
 {
  "aid": "a0032",
  "kind": "choice",
  "text": "Organization: Shanghai Institute of Hypertension\nCountry: China",
  "question": "Which type does the registry give for Shanghai Institute of Hypertension (China)?",
  "options": [
   "facility",
   "other",
   "healthcare",
   "company"
  ],
  "program_answer": "facility"
 },
 {
  "aid": "a0033",
  "kind": "choice",
  "text": "Project and operations register row\nProject ID: P132317\nLending instrument: Investment Project Financing\nTotal commitment (USD million): 523.32\nBoard approval date: 2014-08-29\nMajor themes listed: 2",
  "question": "Pick the fiscal year of the board approval for this entry.",
  "options": [
   "2017",
   "2015",
   "2016",
   "2014"
  ],
  "definitions": "The World Bank fiscal year runs from 1 July to 30 June and is named after the calendar year in which it ends. Approval on or after 1 July of year Y falls in fiscal year Y+1; approval before 1 July falls in fiscal year Y.",
  "program_answer": "2015"
 },
 {
  "aid": "a0034",
  "kind": "choice",
  "text": "Taxon: Isochona",
  "question": "Which kingdom is the taxon Isochona placed in?",
  "options": [
   "Protozoa",
   "Chromista",
   "Fungi",
   "Archaea"
  ],
  "program_answer": "Chromista"
 },
 {
  "aid": "a0035",
  "kind": "yes/no",
  "text": "Brasília, Brazil",
  "question": "Does Brazil have Brasília as its capital?",
  "program_answer": "yes"
 },
 {
  "aid": "a0036",
  "kind": "yes/no",
  "text": "Accession number: 2012.22.b\nObject type: Coins\nCollection: MED - Byzantine\nTechnique: gold\nCulture: Byzantium\nDate text: 659–661\nDate range: 659 to 661\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Was this work begun before the year 1500?",
  "program_answer": "yes"
 },
 {
  "aid": "a0037",
  "kind": "choice",
  "text": "Taxon: Cladophora prolixa\nKingdom: Plantae\nPhylum: Chlorophyta",
  "question": "To which class does the taxon Cladophora prolixa belong?",
  "options": [
   "Chlorophyceae",
   "Klebsormidiophyceae",
   "Prasinophyceae",
   "Ulvophyceae"
  ],
  "program_answer": "Ulvophyceae"
 },
 {
  "aid": "a0038",
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
  ],
  "program_answer": "Prints"
 },
 {
  "aid": "a0039",
  "kind": "choice",
  "text": "Organization: Universidad Aeronáutica en Querétaro\nCountry: Mexico",
  "question": "Which period holds the founding year of Universidad Aeronáutica en Querétaro (Mexico)?",
  "options": [
   "2000 or later",
   "1950-1999",
   "1900-1949",
   "1800-1899"
  ],
  "program_answer": "2000 or later"
 },
 {
  "aid": "a0040",
  "kind": "choice",
  "text": "Organization: National Coal Mining Museum for England\nCountry: United Kingdom",
  "question": "What type of organization is National Coal Mining Museum for England (United Kingdom)?",
  "options": [
   "facility",
   "healthcare",
   "archive",
   "government"
  ],
  "program_answer": "archive"
 },
 {
  "aid": "a0041",
  "kind": "choice",
  "text": "City: Yelets\nCountry: Russia",
  "question": "Which time zone is Yelets in?",
  "options": [
   "Europe/Moscow",
   "Asia/Yekaterinburg",
   "Asia/Krasnoyarsk",
   "Asia/Kamchatka"
  ],
  "program_answer": "Europe/Moscow"
 },
 {
  "aid": "a0042",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\n{\n  \"total_usd_m\": 200.00,\n  \"approval_fy\": 2023,\n  \"status\": \"Active\",\n  \"country\": \"Lebanon\",\n  \"themes\": 0\n}",
  "question": "Is it true that this entry does not count as an open project under the card?",
  "definitions": "- yes: Yes if the status is Active or Pipeline.\n- no: No if the status is Closed or Dropped.",
  "program_answer": "no"
 },
 {
  "aid": "a0043",
  "kind": "choice",
  "text": "Taxon: Dictyosphaerium primarium\nKingdom: Plantae\nClass: Trebouxiophyceae",
  "question": "Under the definitions, which group holds Dictyosphaerium primarium?",
  "options": [
   "Group A",
   "Group B",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: the class is Gnetopsida, Ulvophyceae or Glaucophyceae\n- Group B: the class is Marchantiopsida, Rhodellophyceae or Liliopsida\n- Group C: the class is Prasinophyceae, Bangiophyceae or Klebsormidiophyceae\n- None of these groups: any other is",
  "program_answer": "None of these groups"
 },
 {
  "aid": "a0044",
  "kind": "choice",
  "text": "City: Jishou\nCountry: China",
  "question": "Which time zone does Jishou use?",
  "options": [
   "Asia/Tashkent",
   "Asia/Tokyo",
   "Asia/Karachi",
   "Asia/Shanghai"
  ],
  "program_answer": "Asia/Shanghai"
 },
 {
  "aid": "a0045",
  "kind": "yes/no",
  "text": "Project ID: 883219\nProgramme: Horizon 2020\nFunding scheme: ERC-ADG\nCall topic: ERC-2019-ADG\nStart date: 2021-07-01\nEnd date: 2026-06-30\nTotal cost: 2500000 EUR\nEC maximum contribution: 2500000 EUR",
  "question": "Is the EC maximum contribution above 10,000,000 EUR?",
  "program_answer": "no"
 },
 {
  "aid": "a0046",
  "kind": "choice",
  "text": "Lending operation record from a development-bank register\n- Environmental category = A\n- Total commitment (USD million) = 275.00\n- Board approval date = 2014-12-09\n- Major themes listed = 2\n- Project name = Kariba Dam Rehabilitation Project (RI)",
  "question": "Which fiscal year of the board approval does this entry fall in?",
  "options": [
   "2017",
   "2015",
   "2016",
   "2014"
  ],
  "definitions": "The World Bank fiscal year runs from 1 July to 30 June and is named after the calendar year in which it ends. Approval on or after 1 July of year Y falls in fiscal year Y+1; approval before 1 July falls in fiscal year Y.",
  "program_answer": "2015"
 },
 {
  "aid": "a0047",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: Lincoln City\nRating: 5",
  "question": "Does this establishment meet the rule?",
  "definitions": "- yes: The rating is 4 or 5.\n- no: The rating is any other value.",
  "program_answer": "yes"
 },
 {
  "aid": "a0048",
  "kind": "choice",
  "text": "Organization: Olivet University\nCountry: United States",
  "question": "Which period holds the founding year of Olivet University (United States)?",
  "options": [
   "2000 or later",
   "1950-1999",
   "1900-1949",
   "1800-1899"
  ],
  "program_answer": "2000 or later"
 },
 {
  "aid": "a0049",
  "kind": "choice",
  "text": "Organization: HR Wallingford\nCountry: United Kingdom",
  "question": "What type of organization is HR Wallingford (United Kingdom)?",
  "options": [
   "company",
   "nonprofit",
   "facility",
   "archive"
  ],
  "program_answer": "facility"
 }
]
