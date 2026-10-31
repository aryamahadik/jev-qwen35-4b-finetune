# G9 re-read (G5-H blind read) MDX-B00 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread_a74/answers/MDX-B00.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 42. Answers expected: 42 (one per item, each with that item's qid).

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
  "qid": "q03f71684e0",
  "kind": "choice",
  "text": "Project ID: 729315\nProgramme: Horizon 2020\nFunding scheme: SME-1\nCall topic: SMEInst-01-2016-2017\nStart date: 2016-06-01\nEnd date: 2016-08-31\nTotal cost: 71429 EUR\nEC maximum contribution: 50000 EUR",
  "question": "Which band holds the total cost (in EUR)?",
  "options": [
   "under 100 thousand",
   "1 million to under 5 million",
   "100 thousand to under 1 million",
   "5 million or more"
  ]
 },
 {
  "qid": "q3253a410bf",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: Cambridge City\nRating: 4",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group A",
   "Group C",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: the business type is Manufacturers/packers, Importers/Exporters or Mobile caterer\n- Group B: the business type is Retailers - other, Restaurant/Cafe/Canteen or School/college/university\n- Group C: the business type is Other catering premises, Caring Premises or Takeaway/sandwich shop\n- None of these groups: any other is"
 },
 {
  "qid": "q3dc11b8056",
  "kind": "yes/no",
  "text": "GO term: GO:0051075\nName: S-adenosylmethionine:tRNA ribosyltransferase-isomerase activity\nDefinition: Catalysis of the reaction: S-adenosylmethionine + 7-(aminomethyl)-7-deazaguanosine-tRNA = adenine + methionine + epoxyqueuosine-tRNA. 7-(aminomethyl)-7-deazaguanosine-tRNA is also known as preQ1-tRNA, and epoxyqueuosine-tRNA as oQ-tRNA.\nDefinition sources: PMID:12731872\nSynonyms (1): \"S-adenosyl methionine:tRNA ribosyltransferase-isomerase activity\" EXACT\nDirect is_a parents (3): glycosyltransferase activity; isomerase activity; catalytic activity, acting on a tRNA\nOther relationships: none listed\nSubsets: none listed\nCross-references (2): EC:2.4.99.17, RHEA:32155",
  "question": "Does this GO term have more than 2 direct is_a parents?",
  "definitions": "- yes: the term lists more than 2 direct is_a parents. Direct parents are the is_a entries listed on the term. Relationships such as part_of are not parents and are not counted. The list shown is complete.\n- no: the term lists 2 or fewer direct is_a parents. Direct parents are the is_a entries listed on the term. Relationships such as part_of are not parents and are not counted. The list shown is complete."
 },
 {
  "qid": "qb5c6a2c872",
  "kind": "yes/no",
  "text": "Taxon: Chlamydonellopsis plurivacuolata\nKingdom: Chromista",
  "question": "Is the taxon Chlamydonellopsis plurivacuolata extinct?"
 },
 {
  "qid": "q42a7cf935f",
  "kind": "choice",
  "text": "GO term: GO:0008315\nName: G2/MI transition of meiotic cell cycle\nDefinition: The cell cycle process in which a cell progresses from meiotic G2 phase to M phase of meiosis I.\nDefinition sources: PMID:15084480",
  "question": "In which of the three GO namespaces is this term placed?",
  "options": [
   "molecular_function",
   "cellular_component",
   "biological_process"
  ],
  "definitions": "- biological_process: a series of events a cell or organism carries out, such as a pathway, response, development or regulation\n- molecular_function: an activity of a gene product at the molecular level, such as catalysis, binding or transport activity\n- cellular_component: a place in a cell or a complex, such as an organelle, membrane, compartment or protein complex"
 },
 {
  "qid": "q8aa600ad87",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Restaurant/Cafe/Canteen\nLocal authority: Wandsworth\nRating: 4",
  "question": "Under the definitions, which group holds this establishment?",
  "options": [
   "Group A",
   "Group C",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: the business type is Mobile caterer, Farmers/growers or School/college/university\n- Group B: the business type is Hotel/bed & breakfast/guest house, Retailers - supermarkets/hypermarkets or Restaurant/Cafe/Canteen\n- Group C: the business type is Retailers - other, Manufacturers/packers or Takeaway/sandwich shop\n- None of these groups: any other is"
 },
 {
  "qid": "q7a85a7760d",
  "kind": "choice",
  "text": "Entry from a music metadata database\nGenre tag count 4; Primary type Album; Secondary types Live; Genre tags rock, psychedelic, neo-psychedelia, paisley underground; Title Perfume River.",
  "question": "Pick the alphabetical block of the title's first letter for this entry.",
  "options": [
   "A-F",
   "G-M",
   "N-S",
   "T-Z"
  ]
 },
 {
  "qid": "qbf464bc8a1",
  "kind": "yes/no",
  "text": "Index record of a publication\nPublication year 2023; Open access flag true; Distinct countries 1; Distinct institutions 1; Topic domain Health Sciences.",
  "question": "Is the publication year 2020 or later?"
 },
 {
  "qid": "qfae984ff41",
  "kind": "choice",
  "text": "Discography database row\nRelease group ID 1aba324d-9ce3-43de-a036-3159dbfe9661; First release date 1981; Primary type Single; Releases in group 1; Genre tag count 3.",
  "question": "Which primary type applies to this entry?",
  "options": [
   "Album",
   "EP",
   "Single",
   "Other"
  ]
 },
 {
  "qid": "q2425682cd3",
  "kind": "yes/no",
  "text": "Project and operations register row\nSupplemental flag: N\nStatus: Closed\nIDA commitment (USD million): 0.00\nRegion: Middle East and North Africa\nClosing date: 2024-06-30",
  "question": "Is the region 'Middle East and North Africa'?"
 },
 {
  "qid": "qa8edb84906",
  "kind": "choice",
  "text": "Taxon: Trigoides aclis\nKingdom: Animalia",
  "question": "Which phylum is the taxon Trigoides aclis placed in?",
  "options": [
   "Placozoa",
   "Cnidaria",
   "Ctenophora",
   "Rotifera"
  ]
 },
 {
  "qid": "qaa809189d6",
  "kind": "choice",
  "text": "Taxon: Epidermoptidae\nKingdom: Animalia",
  "question": "Which phylum is the taxon Epidermoptidae placed in?",
  "options": [
   "Cnidaria",
   "Arthropoda",
   "Rotifera",
   "Platyhelminthes"
  ]
 },
 {
  "qid": "q9b3bb317b3",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Retailers - other\nLocal authority: Hillingdon\nRating: 3",
  "question": "Is this establishment eligible under the rule?",
  "definitions": "- yes: The business type is Pub/bar/nightclub, Mobile caterer or Distributors/Transporters.\n- no: The business type is any other type."
 },
 {
  "qid": "qa2655dee20",
  "kind": "yes/no",
  "text": "GO term: GO:0009142\nName: nucleoside triphosphate biosynthetic process\nDefinition: The chemical reactions and pathways resulting in the formation of a nucleoside triphosphate, a compound consisting of a nucleobase linked to a deoxyribose or ribose sugar esterified with triphosphate on the sugar.\nDefinition sources: GOC:curators, ISBN:0198506732\nSynonyms (4): \"nucleoside triphosphate anabolism\" EXACT; \"nucleoside triphosphate biosynthesis\" EXACT; \"nucleoside triphosphate formation\" EXACT; \"nucleoside triphosphate synthesis\" EXACT\nDirect is_a parents (2): biosynthetic process; nucleoside triphosphate metabolic process\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Would you say this term has over 2 listed synonyms?"
 },
 {
  "qid": "q4b915de90f",
  "kind": "yes/no",
  "text": "Taxa: Asterias spec; Calliaster chaos",
  "question": "Do Asterias spec and Calliaster chaos belong to different orders?"
 },
 {
  "qid": "q3df2dd3cf7",
  "kind": "choice",
  "text": "GO term: GO:0030506\nName: ankyrin binding\nDefinition: Binding to ankyrin, a 200 kDa cytoskeletal protein that attaches other cytoskeletal proteins to integral membrane proteins.\nDefinition sources: GOC:mah, ISBN:0198506732\nSynonyms (0): none listed\nDirect is_a parents (1): cytoskeletal protein binding\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Which band holds the number of listed synonyms?",
  "options": [
   "1 to 2",
   "0",
   "3 or more"
  ],
  "definitions": "- 0: the term lists no synonyms\n- 1 to 2: the term lists one or two synonyms\n- 3 or more: the term lists three or more synonyms"
 },
 {
  "qid": "q071013c2b3",
  "kind": "yes/no",
  "text": "Project ID: 744659\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-ST\nCall topic: MSCA-IF-2016\nStart date: 2017-10-01\nEnd date: 2019-12-31\nTotal cost: 171460.8 EUR\nEC maximum contribution: 171460.8 EUR",
  "question": "Is the EC maximum contribution above 1,000,000 EUR?"
 },
 {
  "qid": "q7857eca191",
  "kind": "choice",
  "text": "Taxon: Kazachstania serrabonitensis\nKingdom: Fungi",
  "question": "Which phylum is the taxon Kazachstania serrabonitensis placed in?",
  "options": [
   "Neocallimastigomycota",
   "Basidiomycota",
   "Ascomycota",
   "Zygomycota"
  ]
 },
 {
  "qid": "q6f1ba73dd2",
  "kind": "yes/no",
  "text": "GO term: GO:0033944\nName: beta-galactofuranosidase activity\nDefinition: Catalysis of the hydrolysis of terminal non-reducing beta-D-galactofuranosides, releasing galactose.\nDefinition sources: EC:3.2.1.146\nSynonyms (4): \"beta-D-galactofuranosidase activity\" RELATED; \"beta-D-galactofuranoside hydrolase activity\" RELATED; \"exo-beta-D-galactofuranosidase activity\" RELATED; \"exo-beta-galactofuranosidase activity\" RELATED\nDirect is_a parents (1): hydrolase activity, hydrolyzing O-glycosyl compounds\nOther relationships: none listed\nSubsets: none listed\nCross-references (2): EC:3.2.1.146, MetaCyc:3.2.1.146-RXN",
  "question": "Is the number of direct is_a parents of this GO term above 1?"
 },
 {
  "qid": "q16764362dc",
  "kind": "yes/no",
  "text": "Project ID: 734796\nProgramme: Horizon 2020\nFunding scheme: MSCA-RISE\nCall topic: MSCA-RISE-2016\nStart date: 2017-02-01\nEnd date: 2022-01-31\nTotal cost: 445500 EUR\nEC maximum contribution: 279000 EUR",
  "question": "Is it true that the call topic is a European Research Council (ERC) topic?",
  "definitions": "- yes: the call topic code starts with ERC followed by a hyphen or ends right after ERC.\n- no: the call topic code starts with something else."
 },
 {
  "qid": "q357c59286e",
  "kind": "yes/no",
  "text": "Project ID: 101024389\nTitle: medITerranean HydroclimAte variability over the Common erA",
  "question": "Does the project title have more than 5 words?"
 },
 {
  "qid": "q3f37d0e334",
  "kind": "yes/no",
  "text": "Suva Reka, Kosovo",
  "question": "Is it correct that Suva Reka is not the capital city of Kosovo?"
 },
 {
  "qid": "qa9e24a1e03",
  "kind": "yes/no",
  "text": "Wellington is a city in New Zealand.",
  "question": "Does Wellington (New Zealand) have more than 300,000 inhabitants?"
 },
 {
  "qid": "q5e108e4cf7",
  "kind": "choice",
  "text": "Taxon: Metrarabdotos floridanum\nKingdom: Animalia",
  "question": "Which phylum is the taxon Metrarabdotos floridanum placed in?",
  "options": [
   "Bryozoa",
   "Cnidaria",
   "Annelida",
   "Nemertea"
  ]
 },
 {
  "qid": "qc3931e1967",
  "kind": "choice",
  "text": "Project ID: 949555\nProgramme: Horizon 2020\nFunding scheme: ERC-STG\nCall topic: ERC-2020-STG\nStart date: 2021-06-01\nEnd date: 2026-11-30\nTotal cost: 1498652 EUR\nEC maximum contribution: 1498652 EUR",
  "question": "Which quarter of the year does the project start in?",
  "options": [
   "Q2 (April to June)",
   "Q3 (July to September)",
   "Q1 (January to March)",
   "Q4 (October to December)"
  ]
 },
 {
  "qid": "qe31a6c6c2d",
  "kind": "choice",
  "text": "City: Troparëvo\nCountry: Russia",
  "question": "Which first-level region (federal subject) of Russia contains Troparëvo?",
  "options": [
   "Moscow Oblast",
   "Nizhny Novgorod Oblast",
   "Moscow",
   "Dagestan"
  ]
 },
 {
  "qid": "qf95ba99e97",
  "kind": "yes/no",
  "text": "Seismic event record\n- Event type = earthquake\n- Magnitude type = mb\n- Latitude = 45.587\n- Longitude = 27.706",
  "question": "Is it the case that the record does not fail to give 'md' as the magnitude type?"
 },
 {
  "qid": "q426f705b66",
  "kind": "yes/no",
  "text": "Event summary from a seismic network catalogue\n{\n  \"magnitude\": 4.5,\n  \"felt_reports\": 1,\n  \"pager_alert\": \"none\",\n  \"longitude\": -66.987,\n  \"depth_km\": 173.1\n}",
  "question": "Does the record show at least 10 felt reports?"
 },
 {
  "qid": "q6d4c7e17e4",
  "kind": "choice",
  "text": "Entry from a music metadata database\nTitle Blast From the Ancient Past; Primary type Other; Secondary types none; Releases in group 1; Genre tags none.",
  "question": "Which title length class does this entry fall in?",
  "options": [
   "one word",
   "two or three words",
   "four or more words"
  ]
 },
 {
  "qid": "q27d089de84",
  "kind": "yes/no",
  "text": "GO term: GO:0046673\nName: negative regulation of compound eye retinal cell programmed cell death\nDefinition: Any process that stops, prevents, or reduces the frequency, rate or extent of programmed cell death that occurs in the compound eye retina.\nDefinition sources: GOC:ai\nDirect is_a parents (2): regulation of compound eye retinal cell programmed cell death; negative regulation of retinal cell programmed cell death",
  "question": "Does this term belong to the molecular function namespace?",
  "definitions": "- yes: the term's namespace is molecular_function, meaning an activity of a gene product at the molecular level, such as catalysis, binding or transport activity.\n- no: the term's namespace is one of the two other GO namespaces."
 },
 {
  "qid": "qd568f569f4",
  "kind": "choice",
  "text": "Seismic event record\n{\n  \"place\": \"1 km NW of Little America, Wyoming\",\n  \"azimuthal_gap\": 113,\n  \"stations\": 24,\n  \"tsunami_flag\": 0\n}",
  "question": "Which distance class of the named place applies to this entry?",
  "options": [
   "within 10 km",
   "11 to 50 km",
   "51 to 150 km",
   "over 150 km"
  ],
  "definitions": "- within 10 km: Pick this when the stated distance is 10 km or less.\n- 11 to 50 km: Pick this for 11 to 50 km.\n- 51 to 150 km: Pick this for 51 to 150 km.\n- over 150 km: Pick this for more than 150 km."
 },
 {
  "qid": "q2627dbe308",
  "kind": "yes/no",
  "text": "Project ID: 759432\nProgramme: Horizon 2020\nFunding scheme: ERC-STG\nCall topic: ERC-2017-STG\nStart date: 2018-01-01\nEnd date: 2022-12-31\nTotal cost: 1466014 EUR\nEC maximum contribution: 1466014 EUR",
  "question": "Does the project run longer than 4 years?",
  "definitions": "- yes: the End date is later than the Start date plus 4 years (same month and day).\n- no: the End date is on or before the Start date plus 4 years."
 },
 {
  "qid": "q8db4c9daa1",
  "kind": "yes/no",
  "text": "Scholarly work metadata\npublication_year: 1996\ncountries: 0\ndomain: Physical Sciences\nversion: publishedVersion",
  "question": "Was it published in 2000 or later?"
 },
 {
  "qid": "q33d6bc44b5",
  "kind": "yes/no",
  "text": "Project and operations register row\n| Field | Value |\n| --- | --- |\n| Environmental category | C |\n| IDA commitment (USD million) | 0.00 |\n| Project name | Rwanda Pilot Program for Climate Resilience |\n| Country | Rwanda |",
  "question": "Is it true that the word 'Climate' is not part of the project name?"
 },
 {
  "qid": "qd0a6fdcda9",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Retailers - supermarkets/hypermarkets\nLocal authority: Telford and Wrekin Council\nRating: 5",
  "question": "Does this establishment meet the rule?",
  "definitions": "- yes: The business type is Caring Premises, School/college/university or Retailers - other.\n- no: The business type is any other type."
 },
 {
  "qid": "qe24bd843c2",
  "kind": "yes/no",
  "text": "Project ID: 781623\nProgramme: Horizon 2020\nFunding scheme: SME-1\nCall topic: SMEInst-13-2016-2017\nStart date: 2017-08-01\nEnd date: 2017-11-30\nTotal cost: 71429 EUR\nEC maximum contribution: 50000 EUR",
  "question": "Does the project start in the first half of a year, January to June?"
 },
 {
  "qid": "q9a59e5789f",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\nFelt reports: 109\nLatitude: 34.466\nDepth (km): 10.0\nLongitude: -106.764\nAzimuthal gap (deg): 31",
  "question": "Does the record show at least 100 felt reports?"
 },
 {
  "qid": "q28d50d90c7",
  "kind": "yes/no",
  "text": "Accession number: 2005.205\nObject type: Manuscript\nCollection: MED - Manuscript Illuminations\nTechnique: ink, tempera and gold on vellum\nCulture: Flanders, Ghent?, 15th century\nDate text: 1430s\nDate range: 1430 to 1439\nMeasurements: not listed\nCredit line, first word: The",
  "question": "Does the whole date range fall inside one century?",
  "definitions": "- yes: the first and last year of the Date range lie in the same century (years 1 to 100 are the 1st century, 1801 to 1900 the 19th).\n- no: the first and last year lie in different centuries."
 },
 {
  "qid": "qc7cb76405e",
  "kind": "yes/no",
  "text": "Project ID: 670436\nProgramme: Horizon 2020\nFunding scheme: ERC-ADG\nCall topic: ERC-ADG-2014\nStart date: 2015-12-01\nEnd date: 2022-07-31\nTotal cost: 2025000 EUR\nEC maximum contribution: 2025000 EUR",
  "question": "Does the project run longer than 5 years?",
  "definitions": "- yes: the End date is later than the Start date plus 5 years (same month and day).\n- no: the End date is on or before the Start date plus 5 years."
 },
 {
  "qid": "q1ffc8b6290",
  "kind": "yes/no",
  "text": "Accession number: 1988.23.2.11\nObject type: Bound Volume\nCollection: Japanese Art\nTechnique: color woodcuts with gold and silver\nCulture: Japan, Meiji period (1868–1912)\nDate text: 1909–10\nDate range: 1909 to 1910\nMeasurements: not listed\nCredit line, first word: Norman",
  "question": "Does the work's date range start before 1300?",
  "definitions": "- yes: the first year of the Date range is earlier than 1300.\n- no: the first year of the Date range is 1300 or later."
 },
 {
  "qid": "qcfdbb1b40b",
  "kind": "choice",
  "text": "Taxon: Takakiaceae\nKingdom: Plantae",
  "question": "To which phylum does the taxon Takakiaceae belong?",
  "options": [
   "Tracheophyta",
   "Chlorophyta",
   "Charophyta",
   "Bryophyta"
  ]
 },
 {
  "qid": "q996eaa09f2",
  "kind": "yes/no",
  "text": "Place: Tongling\nCountry: China\nFeature code (record): PPLA3",
  "question": "Does Tongling meet this rule?",
  "definitions": "- yes: The place's feature code is PPL or PPLA.\n- no: The place's feature code is any other code."
 }
]
