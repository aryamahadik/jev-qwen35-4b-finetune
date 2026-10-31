# G9 re-read (G5-H blind read) MD-A01 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-A01.json

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
  "qid": "q1551adef8e",
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
  "qid": "qce23f87167",
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
  "qid": "q5e91516d3f",
  "kind": "yes/no",
  "text": "Project ID: 724715\nProgramme: Horizon 2020\nFunding scheme: ERC-COG\nCall topic: ERC-2016-COG\nStart date: 2017-06-01\nEnd date: 2023-05-31\nTotal cost: 2272485 EUR\nEC maximum contribution: 2272485 EUR",
  "question": "Does the EC contribute more than 100,000 EUR to this project?"
 },
 {
  "qid": "qb548078a6e",
  "kind": "yes/no",
  "text": "GO term: GO:0043751\nName: polyphosphate:AMP phosphotransferase activity\nDefinition: Catalysis of the reaction: (polyphosphate)n + AMP = (polyphosphate)n-1 + ADP.\nDefinition sources: PMID:11237733\nSynonyms (2): \"PAP\" EXACT; \"PPT\" BROAD\nDirect is_a parents (1): phosphotransferase activity, phosphate group as acceptor\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Would it be true that this term does not fail to have a part_of relationship?"
 },
 {
  "qid": "q9df8b5a715",
  "kind": "choice",
  "text": "Organization: Thunchath Ezhuthachan Malayalam University",
  "question": "In which country is Thunchath Ezhuthachan Malayalam University?",
  "options": [
   "Indonesia",
   "Argentina",
   "Iran",
   "India"
  ]
 },
 {
  "qid": "qb3fb52da31",
  "kind": "choice",
  "text": "GO term: GO:0034766\nName: negative regulation of monoatomic ion transmembrane transport\nDefinition: Any process that stops, prevents, or reduces the frequency, rate or extent of the directed movement of ions from one side of a membrane to the other.\nDefinition sources: GOC:mah\nSynonyms (7): \"down regulation of transmembrane ion transport\" EXACT; \"down-regulation of transmembrane ion transport\" EXACT; \"downregulation of transmembrane ion transport\" EXACT; \"inhibition of transmembrane ion transport\" NARROW; \"negative regulation of ion membrane transport\" EXACT; \"negative regulation of ion transmembrane transport\" BROAD; \"negative regulation of transmembrane ion transport\" EXACT\nDirect is_a parents (3): negative regulation of transmembrane transport; regulation of monoatomic ion transmembrane transport; negative regulation of monoatomic ion transport\nOther relationships: negatively_regulates monoatomic ion transmembrane transport\nSubsets: none listed\nCross-references (0): none listed",
  "question": "How many different synonym scopes does the term use?",
  "options": [
   "2",
   "3 or more",
   "1"
  ]
 },
 {
  "qid": "q2c5e4979a4",
  "kind": "yes/no",
  "text": "Accession number: 1939.269\nObject type: Painting\nCollection: Mod Euro - Painting 1800-1960\nTechnique: oil on canvas\nCulture: France, 19th century\nDate text: c. 1897\nDate range: 1892 to 1902\nMeasurements: Framed: 75.5 x 85.5 x 10 cm (29 3/4 x 33 11/16 x 3 15/16 in.); Unframed: 54.6 x 65.7 cm (21 1/2 x 25 7/8 in.)\nCredit line, first word: Purchase",
  "question": "Was this work begun before the year 1800?"
 },
 {
  "qid": "q4edec664bd",
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
  "qid": "qf5d62160d6",
  "kind": "choice",
  "text": "City: Kumertau\nCountry: Russia",
  "question": "In which first-level region (federal subject) of Russia is Kumertau?",
  "options": [
   "Tomsk Oblast",
   "Moscow",
   "Khanty-Mansia",
   "Bashkortostan Republic"
  ]
 },
 {
  "qid": "qb32446740d",
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
  "qid": "qb6d4708ba9",
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
  "qid": "qfb80f98c7a",
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
  "qid": "q8d367892e9",
  "kind": "choice",
  "text": "Place: Tog Wajaale\nCountry: Somalia",
  "question": "Which group does the country of Tog Wajaale belong to under these definitions?",
  "options": [
   "Group B",
   "Group A",
   "None of these groups",
   "Group C"
  ],
  "definitions": "- Group A: India, Philippines or Germany\n- Group B: Chile, Somalia or China\n- Group C: Brazil, Spain or Ethiopia\n- None of these groups: any other country"
 },
 {
  "qid": "q63700953c3",
  "kind": "choice",
  "text": "Place: Pélézi\nCountry: Ivory Coast",
  "question": "Which group does the country of Pélézi belong to under these definitions?",
  "options": [
   "Group B",
   "Group C",
   "Group A",
   "None of these groups"
  ],
  "definitions": "- Group A: Hungary, Brazil or Mali\n- Group B: Ivory Coast, Algeria or Ukraine\n- Group C: Spain, United States or Indonesia\n- None of these groups: any other country"
 },
 {
  "qid": "qe3b48d81d9",
  "kind": "yes/no",
  "text": "GO term: GO:0045180\nName: basal cortex\nDefinition: The region that lies just beneath the plasma membrane on the basal edge of a cell.\nDefinition sources: GOC:bf\nSynonyms (0): none listed\nDirect is_a parents (1): cell cortex region\nOther relationships: part_of basal part of cell\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Is the number of listed synonyms of this GO term above 0?"
 },
 {
  "qid": "qa77a0cb0db",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\n{\n  \"total_usd_m\": 200.00,\n  \"approval_fy\": 2023,\n  \"status\": \"Active\",\n  \"country\": \"Lebanon\",\n  \"themes\": 0\n}",
  "question": "Is it true that this entry does not count as an open project under the card?",
  "definitions": "- yes: Yes if the status is Active or Pipeline.\n- no: No if the status is Closed or Dropped."
 },
 {
  "qid": "qeb95130a37",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\nnetwork: us\nplace: 148 km ENE of Masohi, Indonesia\npager_alert: green\ntsunami_flag: 0",
  "question": "Is the last comma-separated part of the location description 'Indonesia'?"
 },
 {
  "qid": "q7bf85d9b58",
  "kind": "yes/no",
  "text": "Organization: Ankara Fizik Tedavi ve Rehabilitasyon Eğitim ve Araştırma Hastanesi\nCountry: Türkiye",
  "question": "Is Ankara Fizik Tedavi ve Rehabilitasyon Eğitim ve Araştırma Hastanesi eligible under this rule?",
  "definitions": "- yes: The organization is located in DR Congo, Türkiye or United States.\n- no: The organization is located in any other country."
 },
 {
  "qid": "q76da5070cd",
  "kind": "choice",
  "text": "Taxon: Mythicomycetaceae\nKingdom: Fungi",
  "question": "Which phylum is the taxon Mythicomycetaceae placed in?",
  "options": [
   "Ascomycota",
   "Basidiomycota",
   "Blastocladiomycota",
   "Chytridiomycota"
  ]
 },
 {
  "qid": "q1ec5182895",
  "kind": "yes/no",
  "text": "Project ID: 892369\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-SE\nCall topic: MSCA-IF-2019\nStart date: 2020-05-01\nEnd date: 2022-04-30\nTotal cost: 175572.48 EUR\nEC maximum contribution: 175572.48 EUR",
  "question": "Does the EC contribution equal the total cost?",
  "definitions": "- yes: the EC maximum contribution equals the total cost (within 0.5 EUR).\n- no: the EC maximum contribution is smaller than the total cost."
 },
 {
  "qid": "qee9040baf6",
  "kind": "yes/no",
  "text": "Organization: Alcontrol Laboratories (Norway)\nCountry: Norway",
  "question": "Was Alcontrol Laboratories (Norway) (Norway) established before 1990?"
 },
 {
  "qid": "q05836796b4",
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
 },
 {
  "qid": "q2f25a63c71",
  "kind": "yes/no",
  "text": "Scholarly work metadata\n| Field | Value |\n| --- | --- |\n| Work ID | W2094594732 |\n| Publication year | 2010 |\n| Reference year | 2026 |\n| Citation count | 9 |\n| References listed | 33 |\n| Distinct countries | 1 |",
  "question": "Is the citation count higher than the number of references listed?"
 },
 {
  "qid": "q79e5b2b2c2",
  "kind": "yes/no",
  "text": "Discography database row\n| Field | Value |\n| --- | --- |\n| Release group ID | 79375e1f-e814-4db6-ae97-f092037b8d5a |\n| First release date | 2002-10-01 |\n| Primary type | Other |\n| Genre tags | none |\n| Release statuses | Official |",
  "question": "Is the first-release year earlier than 2020?"
 },
 {
  "qid": "q498c9d0778",
  "kind": "yes/no",
  "text": "Lending operation record from a development-bank register\ntotal_usd_m: 30.00\nthemes: 0\nfinance_type: IDA\nproject_id: P171585",
  "question": "Would it be so that the financing type does not list include IBRD?"
 },
 {
  "qid": "q665651d17c",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nLocal authority: Derby City\nRating: 2",
  "question": "Does this establishment meet the rule?",
  "definitions": "- yes: The business type is Takeaway/sandwich shop, Retailers - other or School/college/university.\n- no: The business type is any other type."
 },
 {
  "qid": "q136d1684a7",
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
  "qid": "q64bba3f1e7",
  "kind": "yes/no",
  "text": "Place: Sunshine West\nCountry: Australia",
  "question": "Does Sunshine West meet this rule?",
  "definitions": "- yes: The place's country is Libya, Russia or North Korea.\n- no: The place's country is any other country."
 },
 {
  "qid": "q7040b77028",
  "kind": "yes/no",
  "text": "Project ID: 646186\nProgramme: Horizon 2020\nFunding scheme: RIA\nCall topic: NMP-13-2014\nStart date: 2015-06-01\nEnd date: 2018-05-31\nTotal cost: 6614553.75 EUR\nEC maximum contribution: 6614553.75 EUR",
  "question": "Does the project end after the year 2018?"
 },
 {
  "qid": "q0796823651",
  "kind": "choice",
  "text": "Earthquake catalogue entry\nlongitude: 151.434\norigin_time: 2025-04-04 20:36:12\nmagnitude: 5.0\nnetwork: us\nsignificance: 385\nlatitude: -6.194",
  "question": "Which map quadrant does this entry fall in?",
  "options": [
   "southeast",
   "northeast",
   "northwest",
   "southwest"
  ],
  "definitions": "- northeast: Pick this when latitude is above 0 and longitude is above 0.\n- northwest: Pick this when latitude is above 0 and longitude is 0 or below.\n- southeast: Pick this when latitude is 0 or below and longitude is above 0.\n- southwest: Pick this when latitude is 0 or below and longitude is 0 or below."
 },
 {
  "qid": "qfe4cdc10d2",
  "kind": "choice",
  "text": "Discography database row\nPrimary type EP; Secondary types none; Artist credits 1; Genre tag count 2.",
  "question": "Pick the primary type for this entry.",
  "options": [
   "Broadcast",
   "Single",
   "Album",
   "EP"
  ]
 },
 {
  "qid": "qc2fa9a6265",
  "kind": "yes/no",
  "text": "GO term: GO:0048348\nName: paraxial mesodermal cell fate specification\nDefinition: The process in which a cell becomes capable of differentiating autonomously into a paraxial mesoderm cell in an environment that is neutral with respect to the developmental pathway; upon specification, the cell fate can be reversed.\nDefinition sources: GOC:dgh\nSynonyms (0): none listed\nDirect is_a parents (1): mesodermal cell fate specification\nOther relationships: part_of paraxial mesodermal cell fate commitment\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Is the definition longer than 20 words?",
  "definitions": "- yes: the definition text (without its source list) has more than 20 words.\n- no: the definition text (without its source list) has 20 words or fewer."
 },
 {
  "qid": "q0974265561",
  "kind": "yes/no",
  "text": "Jijiang is a city in China.",
  "question": "Do more than 130,000 people live in Jijiang (China)?"
 },
 {
  "qid": "qebe75bcf7b",
  "kind": "yes/no",
  "text": "Accession number: 2012.22.b\nObject type: Coins\nCollection: MED - Byzantine\nTechnique: gold\nCulture: Byzantium\nDate text: 659–661\nDate range: 659 to 661\nMeasurements: not listed\nCredit line, first word: Gift",
  "question": "Was this work begun before the year 1500?"
 },
 {
  "qid": "q8770f78caa",
  "kind": "choice",
  "text": "Taxon: Stylocoronella riedli\nKingdom: Animalia",
  "question": "To which phylum does the taxon Stylocoronella riedli belong?",
  "options": [
   "Cnidaria",
   "Arthropoda",
   "Chordata",
   "Sipuncula"
  ]
 },
 {
  "qid": "q00ff1ca3aa",
  "kind": "yes/no",
  "text": "Guatemala City, Guatemala",
  "question": "Is Guatemala City the capital city of Guatemala?"
 },
 {
  "qid": "q81c9f955e2",
  "kind": "yes/no",
  "text": "Taxa: Klebsormidium bilatum; Elakatothrix genevensis",
  "question": "Are Klebsormidium bilatum and Elakatothrix genevensis placed in different families?"
 },
 {
  "qid": "q1831c51000",
  "kind": "yes/no",
  "text": "Index record of a publication\nTopic field Social Sciences; Open-access status green; Work ID W2275129849; Publication date 1996-10-31; Topic domain Social Sciences.",
  "question": "Is it the case that the record does not fail to give 'green' as the open-access status?"
 },
 {
  "qid": "qe0fe4a59e1",
  "kind": "choice",
  "text": "Earthquake catalogue entry\nevent_type: earthquake\npager_alert: green\norigin_time: 2025-03-07 12:17:52\nplace: 12 km NNW of Cayarani, Peru",
  "question": "Pick the PAGER alert level for this entry.",
  "options": [
   "yellow",
   "red",
   "green",
   "orange"
  ]
 },
 {
  "qid": "q57ef40d089",
  "kind": "yes/no",
  "text": "Taxa: Pterosperma nationalis; Pterosperma undulatum",
  "question": "Are Pterosperma nationalis and Pterosperma undulatum placed in different orders?"
 },
 {
  "qid": "q4c23982bb1",
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
  "qid": "q8436f0577c",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Pub/bar/nightclub\nRating date: October (rating 5)",
  "question": "Would it be the case that the rating was given in the second half of the year?"
 },
 {
  "qid": "q7d5c1766fc",
  "kind": "yes/no",
  "text": "Place: Khurarianwala\nCountry: Pakistan\nTime zone (record): Asia/Karachi",
  "question": "Is Khurarianwala eligible under this rule?",
  "definitions": "- yes: The place's time zone is Asia/Pyongyang, Asia/Manila or Asia/Bangkok.\n- no: The place's time zone is any other."
 },
 {
  "qid": "qdcfae5d4e9",
  "kind": "yes/no",
  "text": "Discography database row\n{\n  \"primary_type\": \"EP\",\n  \"statuses\": \"Official\",\n  \"secondary_types\": \"Compilation\",\n  \"credits\": 1,\n  \"first_release_date\": 2010,\n  \"disambiguation\": \"none\"\n}",
  "question": "Under the card, is this entry a plain album?",
  "definitions": "- yes: Yes if the primary type is Album and no secondary type is listed.\n- no: No if the primary type is not Album or at least one secondary type is listed."
 },
 {
  "qid": "qfd288651e4",
  "kind": "yes/no",
  "text": "Index record of a publication\n- Distinct countries = 2\n- Topic domain = Physical Sciences\n- References listed = 0\n- Work type = preprint",
  "question": "Is this entry an international collaboration by the card's rule?",
  "definitions": "- yes: Yes if two or more distinct countries are listed.\n- no: No if zero or one country is listed."
 },
 {
  "qid": "q5702356eb4",
  "kind": "yes/no",
  "text": "Entry from a music metadata database\nfirst_release_date: 1986-09-22\nprimary_type: Album\ntags: rock, electronic, alternative rock, new wave, leftfield\ntag_count: 5\nstatuses: Official",
  "question": "Is the number of genre tags 3 or more?"
 },
 {
  "qid": "qc45f6ea248",
  "kind": "yes/no",
  "text": "GO term: GO:0030674\nName: protein-macromolecule adaptor activity\nDefinition: An adaptor activity that brings together two or more macromolecules in contact, permitting those molecules to function in a coordinated way. The adaptor can bring together two proteins, or a protein and another macromolecule such as a lipid or a nucleic acid.\nDefinition sources: GOC:bf, GOC:mah, GOC:vw\nSynonyms (3): \"protein binding, bridging\" EXACT; \"protein recruiting activity\" RELATED; \"protein-protein adaptor\" NARROW\nDirect is_a parents (1): molecular adaptor activity\nOther relationships: none listed\nSubsets: goslim_chembl, goslim_yeast\nCross-references (6): Reactome:R-HSA-3780997, Reactome:R-HSA-3781001, Reactome:R-HSA-3781021, Reactome:R-HSA-3781023, Reactome:R-HSA-8871366, Reactome:R-HSA-8871376",
  "question": "Is this term in at least one GO slim subset?"
 },
 {
  "qid": "qfedd92d1f7",
  "kind": "choice",
  "text": "Seismic event record\nStations used: 26\nOrigin time (UTC): 2026-07-17 16:39:45\nMagnitude type: ml\nContributing network: ak\nLatitude: 53.395\nLongitude: -165.112",
  "question": "Which map quadrant applies to this entry?",
  "options": [
   "northwest",
   "southeast",
   "northeast",
   "southwest"
  ],
  "definitions": "- northeast: Pick this when latitude is above 0 and longitude is above 0.\n- northwest: Pick this when latitude is above 0 and longitude is 0 or below.\n- southeast: Pick this when latitude is 0 or below and longitude is above 0.\n- southwest: Pick this when latitude is 0 or below and longitude is 0 or below."
 },
 {
  "qid": "q4cfff41014",
  "kind": "choice",
  "text": "Taxon: Bulbochaete basispora\nKingdom: Plantae\nClass: Chlorophyceae",
  "question": "Which order is the taxon Bulbochaete basispora placed in?",
  "options": [
   "Dicranales",
   "Takakiales",
   "Selaginellales",
   "Oedogoniales"
  ]
 },
 {
  "qid": "q572b1a115e",
  "kind": "yes/no",
  "text": "Accession number: 1984.70\nObject type: Sculpture\nCollection: China - Song Dynasty\nTechnique: wood with polychromy and gilding\nCulture: China, late Northern Song dynasty (960-1127) - Jin dynasty...\nDate text: late 1100s–1200s\nDate range: 1175 to 1234\nMeasurements: not listed\nCredit line, first word: Purchase",
  "question": "Was this work begun before the year 1800?"
 }
]
