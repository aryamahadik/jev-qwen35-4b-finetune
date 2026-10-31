# G9 re-read adjudication (flag only) MD-ADJ-000 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread_a74/fam/MD/adjudication/answers/MD-ADJ-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 33. Answers expected: 33 (one per item, each with that item's qid).

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
  "kind": "yes/no",
  "text": "Scholarly work metadata\npublication_year: 1996\ncountries: 0\ndomain: Physical Sciences\nversion: publishedVersion",
  "question": "Was it published in 2000 or later?",
  "program_answer": "no"
 },
 {
  "aid": "a0001",
  "kind": "yes/no",
  "text": "GO term: GO:0046673\nName: negative regulation of compound eye retinal cell programmed cell death\nDefinition: Any process that stops, prevents, or reduces the frequency, rate or extent of programmed cell death that occurs in the compound eye retina.\nDefinition sources: GOC:ai\nDirect is_a parents (2): regulation of compound eye retinal cell programmed cell death; negative regulation of retinal cell programmed cell death",
  "question": "Does this term belong to the molecular function namespace?",
  "definitions": "- yes: the term's namespace is molecular_function, meaning an activity of a gene product at the molecular level, such as catalysis, binding or transport activity.\n- no: the term's namespace is one of the two other GO namespaces.",
  "program_answer": "no"
 },
 {
  "aid": "a0002",
  "kind": "yes/no",
  "text": "Project ID: 781623\nProgramme: Horizon 2020\nFunding scheme: SME-1\nCall topic: SMEInst-13-2016-2017\nStart date: 2017-08-01\nEnd date: 2017-11-30\nTotal cost: 71429 EUR\nEC maximum contribution: 50000 EUR",
  "question": "Does the project start in the first half of a year, January to June?",
  "program_answer": "no"
 },
 {
  "aid": "a0003",
  "kind": "yes/no",
  "text": "Project ID: 670436\nProgramme: Horizon 2020\nFunding scheme: ERC-ADG\nCall topic: ERC-ADG-2014\nStart date: 2015-12-01\nEnd date: 2022-07-31\nTotal cost: 2025000 EUR\nEC maximum contribution: 2025000 EUR",
  "question": "Does the project run longer than 5 years?",
  "definitions": "- yes: the End date is later than the Start date plus 5 years (same month and day).\n- no: the End date is on or before the Start date plus 5 years.",
  "program_answer": "yes"
 },
 {
  "aid": "a0004",
  "kind": "yes/no",
  "text": "GO term: GO:0051075\nName: S-adenosylmethionine:tRNA ribosyltransferase-isomerase activity\nDefinition: Catalysis of the reaction: S-adenosylmethionine + 7-(aminomethyl)-7-deazaguanosine-tRNA = adenine + methionine + epoxyqueuosine-tRNA. 7-(aminomethyl)-7-deazaguanosine-tRNA is also known as preQ1-tRNA, and epoxyqueuosine-tRNA as oQ-tRNA.\nDefinition sources: PMID:12731872\nSynonyms (1): \"S-adenosyl methionine:tRNA ribosyltransferase-isomerase activity\" EXACT\nDirect is_a parents (3): glycosyltransferase activity; isomerase activity; catalytic activity, acting on a tRNA\nOther relationships: none listed\nSubsets: none listed\nCross-references (2): EC:2.4.99.17, RHEA:32155",
  "question": "Does this GO term have more than 2 direct is_a parents?",
  "definitions": "- yes: the term lists more than 2 direct is_a parents. Direct parents are the is_a entries listed on the term. Relationships such as part_of are not parents and are not counted. The list shown is complete.\n- no: the term lists 2 or fewer direct is_a parents. Direct parents are the is_a entries listed on the term. Relationships such as part_of are not parents and are not counted. The list shown is complete.",
  "program_answer": "yes"
 },
 {
  "aid": "a0005",
  "kind": "yes/no",
  "text": "Project ID: 759432\nProgramme: Horizon 2020\nFunding scheme: ERC-STG\nCall topic: ERC-2017-STG\nStart date: 2018-01-01\nEnd date: 2022-12-31\nTotal cost: 1466014 EUR\nEC maximum contribution: 1466014 EUR",
  "question": "Does the project run longer than 4 years?",
  "definitions": "- yes: the End date is later than the Start date plus 4 years (same month and day).\n- no: the End date is on or before the Start date plus 4 years.",
  "program_answer": "yes"
 },
 {
  "aid": "a0006",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Retailers - other\nLocal authority: Hillingdon\nRating: 3",
  "question": "Is this establishment eligible under the rule?",
  "definitions": "- yes: The business type is Pub/bar/nightclub, Mobile caterer or Distributors/Transporters.\n- no: The business type is any other type.",
  "program_answer": "no"
 },
 {
  "aid": "a0007",
  "kind": "choice",
  "text": "Entry from a music metadata database\nTitle Blast From the Ancient Past; Primary type Other; Secondary types none; Releases in group 1; Genre tags none.",
  "question": "Which title length class does this entry fall in?",
  "options": [
   "one word",
   "two or three words",
   "four or more words"
  ],
  "program_answer": "four or more words"
 },
 {
  "aid": "a0008",
  "kind": "yes/no",
  "text": "Taxa: Asterias spec; Calliaster chaos",
  "question": "Do Asterias spec and Calliaster chaos belong to different orders?",
  "program_answer": "yes"
 },
 {
  "aid": "a0009",
  "kind": "yes/no",
  "text": "Taxon: Chlamydonellopsis plurivacuolata\nKingdom: Chromista",
  "question": "Is the taxon Chlamydonellopsis plurivacuolata extinct?",
  "program_answer": "no"
 },
 {
  "aid": "a0010",
  "kind": "yes/no",
  "text": "Suva Reka, Kosovo",
  "question": "Is it correct that Suva Reka is not the capital city of Kosovo?",
  "program_answer": "yes"
 },
 {
  "aid": "a0011",
  "kind": "choice",
  "text": "Entry from a music metadata database\nGenre tag count 4; Primary type Album; Secondary types Live; Genre tags rock, psychedelic, neo-psychedelia, paisley underground; Title Perfume River.",
  "question": "Pick the alphabetical block of the title's first letter for this entry.",
  "options": [
   "A-F",
   "G-M",
   "N-S",
   "T-Z"
  ],
  "program_answer": "N-S"
 },
 {
  "aid": "a0012",
  "kind": "yes/no",
  "text": "Earthquake catalogue entry\nFelt reports: 109\nLatitude: 34.466\nDepth (km): 10.0\nLongitude: -106.764\nAzimuthal gap (deg): 31",
  "question": "Does the record show at least 100 felt reports?",
  "program_answer": "yes"
 },
 {
  "aid": "a0013",
  "kind": "yes/no",
  "text": "Project ID: 101024389\nTitle: medITerranean HydroclimAte variability over the Common erA",
  "question": "Does the project title have more than 5 words?",
  "program_answer": "yes"
 },
 {
  "aid": "a0014",
  "kind": "yes/no",
  "text": "GO term: GO:0033944\nName: beta-galactofuranosidase activity\nDefinition: Catalysis of the hydrolysis of terminal non-reducing beta-D-galactofuranosides, releasing galactose.\nDefinition sources: EC:3.2.1.146\nSynonyms (4): \"beta-D-galactofuranosidase activity\" RELATED; \"beta-D-galactofuranoside hydrolase activity\" RELATED; \"exo-beta-D-galactofuranosidase activity\" RELATED; \"exo-beta-galactofuranosidase activity\" RELATED\nDirect is_a parents (1): hydrolase activity, hydrolyzing O-glycosyl compounds\nOther relationships: none listed\nSubsets: none listed\nCross-references (2): EC:3.2.1.146, MetaCyc:3.2.1.146-RXN",
  "question": "Is the number of direct is_a parents of this GO term above 1?",
  "program_answer": "no"
 },
 {
  "aid": "a0015",
  "kind": "yes/no",
  "text": "Seismic event record\n- Event type = earthquake\n- Magnitude type = mb\n- Latitude = 45.587\n- Longitude = 27.706",
  "question": "Is it the case that the record does not fail to give 'md' as the magnitude type?",
  "program_answer": "no"
 },
 {
  "aid": "a0016",
  "kind": "yes/no",
  "text": "Project and operations register row\nSupplemental flag: N\nStatus: Closed\nIDA commitment (USD million): 0.00\nRegion: Middle East and North Africa\nClosing date: 2024-06-30",
  "question": "Is the region 'Middle East and North Africa'?",
  "program_answer": "yes"
 },
 {
  "aid": "a0017",
  "kind": "choice",
  "text": "City: Troparëvo\nCountry: Russia",
  "question": "Which first-level region (federal subject) of Russia contains Troparëvo?",
  "options": [
   "Moscow Oblast",
   "Nizhny Novgorod Oblast",
   "Moscow",
   "Dagestan"
  ],
  "program_answer": "Moscow"
 },
 {
  "aid": "a0018",
  "kind": "choice",
  "text": "Taxon: Takakiaceae\nKingdom: Plantae",
  "question": "To which phylum does the taxon Takakiaceae belong?",
  "options": [
   "Tracheophyta",
   "Chlorophyta",
   "Charophyta",
   "Bryophyta"
  ],
  "program_answer": "Bryophyta"
 },
 {
  "aid": "a0019",
  "kind": "choice",
  "text": "Taxon: Kazachstania serrabonitensis\nKingdom: Fungi",
  "question": "Which phylum is the taxon Kazachstania serrabonitensis placed in?",
  "options": [
   "Neocallimastigomycota",
   "Basidiomycota",
   "Ascomycota",
   "Zygomycota"
  ],
  "program_answer": "Ascomycota"
 },
 {
  "aid": "a0020",
  "kind": "yes/no",
  "text": "Project ID: 744659\nProgramme: Horizon 2020\nFunding scheme: MSCA-IF-EF-ST\nCall topic: MSCA-IF-2016\nStart date: 2017-10-01\nEnd date: 2019-12-31\nTotal cost: 171460.8 EUR\nEC maximum contribution: 171460.8 EUR",
  "question": "Is the EC maximum contribution above 1,000,000 EUR?",
  "program_answer": "no"
 },
 {
  "aid": "a0021",
  "kind": "yes/no",
  "text": "Accession number: 1988.23.2.11\nObject type: Bound Volume\nCollection: Japanese Art\nTechnique: color woodcuts with gold and silver\nCulture: Japan, Meiji period (1868–1912)\nDate text: 1909–10\nDate range: 1909 to 1910\nMeasurements: not listed\nCredit line, first word: Norman",
  "question": "Does the work's date range start before 1300?",
  "definitions": "- yes: the first year of the Date range is earlier than 1300.\n- no: the first year of the Date range is 1300 or later.",
  "program_answer": "no"
 },
 {
  "aid": "a0022",
  "kind": "yes/no",
  "text": "GO term: GO:0009142\nName: nucleoside triphosphate biosynthetic process\nDefinition: The chemical reactions and pathways resulting in the formation of a nucleoside triphosphate, a compound consisting of a nucleobase linked to a deoxyribose or ribose sugar esterified with triphosphate on the sugar.\nDefinition sources: GOC:curators, ISBN:0198506732\nSynonyms (4): \"nucleoside triphosphate anabolism\" EXACT; \"nucleoside triphosphate biosynthesis\" EXACT; \"nucleoside triphosphate formation\" EXACT; \"nucleoside triphosphate synthesis\" EXACT\nDirect is_a parents (2): biosynthetic process; nucleoside triphosphate metabolic process\nOther relationships: none listed\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Would you say this term has over 2 listed synonyms?",
  "program_answer": "yes"
 },
 {
  "aid": "a0023",
  "kind": "yes/no",
  "text": "Place: Tongling\nCountry: China\nFeature code (record): PPLA3",
  "question": "Does Tongling meet this rule?",
  "definitions": "- yes: The place's feature code is PPL or PPLA.\n- no: The place's feature code is any other code.",
  "program_answer": "no"
 },
 {
  "aid": "a0024",
  "kind": "yes/no",
  "text": "Project ID: 734796\nProgramme: Horizon 2020\nFunding scheme: MSCA-RISE\nCall topic: MSCA-RISE-2016\nStart date: 2017-02-01\nEnd date: 2022-01-31\nTotal cost: 445500 EUR\nEC maximum contribution: 279000 EUR",
  "question": "Is it true that the call topic is a European Research Council (ERC) topic?",
  "definitions": "- yes: the call topic code starts with ERC followed by a hyphen or ends right after ERC.\n- no: the call topic code starts with something else.",
  "program_answer": "no"
 },
 {
  "aid": "a0025",
  "kind": "yes/no",
  "text": "Accession number: 2005.205\nObject type: Manuscript\nCollection: MED - Manuscript Illuminations\nTechnique: ink, tempera and gold on vellum\nCulture: Flanders, Ghent?, 15th century\nDate text: 1430s\nDate range: 1430 to 1439\nMeasurements: not listed\nCredit line, first word: The",
  "question": "Does the whole date range fall inside one century?",
  "definitions": "- yes: the first and last year of the Date range lie in the same century (years 1 to 100 are the 1st century, 1801 to 1900 the 19th).\n- no: the first and last year lie in different centuries.",
  "program_answer": "yes"
 },
 {
  "aid": "a0026",
  "kind": "yes/no",
  "text": "Wellington is a city in New Zealand.",
  "question": "Does Wellington (New Zealand) have more than 300,000 inhabitants?",
  "program_answer": "yes"
 },
 {
  "aid": "a0027",
  "kind": "choice",
  "text": "Seismic event record\n{\n  \"place\": \"1 km NW of Little America, Wyoming\",\n  \"azimuthal_gap\": 113,\n  \"stations\": 24,\n  \"tsunami_flag\": 0\n}",
  "question": "Which distance class of the named place applies to this entry?",
  "options": [
   "within 10 km",
   "11 to 50 km",
   "51 to 150 km",
   "over 150 km"
  ],
  "definitions": "- within 10 km: Pick this when the stated distance is 10 km or less.\n- 11 to 50 km: Pick this for 11 to 50 km.\n- 51 to 150 km: Pick this for 51 to 150 km.\n- over 150 km: Pick this for more than 150 km.",
  "program_answer": "within 10 km"
 },
 {
  "aid": "a0028",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Retailers - supermarkets/hypermarkets\nLocal authority: Telford and Wrekin Council\nRating: 5",
  "question": "Does this establishment meet the rule?",
  "definitions": "- yes: The business type is Caring Premises, School/college/university or Retailers - other.\n- no: The business type is any other type.",
  "program_answer": "no"
 },
 {
  "aid": "a0029",
  "kind": "choice",
  "text": "GO term: GO:0008315\nName: G2/MI transition of meiotic cell cycle\nDefinition: The cell cycle process in which a cell progresses from meiotic G2 phase to M phase of meiosis I.\nDefinition sources: PMID:15084480",
  "question": "In which of the three GO namespaces is this term placed?",
  "options": [
   "molecular_function",
   "cellular_component",
   "biological_process"
  ],
  "definitions": "- biological_process: a series of events a cell or organism carries out, such as a pathway, response, development or regulation\n- molecular_function: an activity of a gene product at the molecular level, such as catalysis, binding or transport activity\n- cellular_component: a place in a cell or a complex, such as an organelle, membrane, compartment or protein complex",
  "program_answer": "biological_process"
 },
 {
  "aid": "a0030",
  "kind": "choice",
  "text": "Discography database row\nRelease group ID 1aba324d-9ce3-43de-a036-3159dbfe9661; First release date 1981; Primary type Single; Releases in group 1; Genre tag count 3.",
  "question": "Which primary type applies to this entry?",
  "options": [
   "Album",
   "EP",
   "Single",
   "Other"
  ],
  "program_answer": "Single"
 },
 {
  "aid": "a0031",
  "kind": "choice",
  "text": "Project ID: 949555\nProgramme: Horizon 2020\nFunding scheme: ERC-STG\nCall topic: ERC-2020-STG\nStart date: 2021-06-01\nEnd date: 2026-11-30\nTotal cost: 1498652 EUR\nEC maximum contribution: 1498652 EUR",
  "question": "Which quarter of the year does the project start in?",
  "options": [
   "Q2 (April to June)",
   "Q3 (July to September)",
   "Q1 (January to March)",
   "Q4 (October to December)"
  ],
  "program_answer": "Q2 (April to June)"
 },
 {
  "aid": "a0032",
  "kind": "choice",
  "text": "Taxon: Trigoides aclis\nKingdom: Animalia",
  "question": "Which phylum is the taxon Trigoides aclis placed in?",
  "options": [
   "Placozoa",
   "Cnidaria",
   "Ctenophora",
   "Rotifera"
  ],
  "program_answer": "Ctenophora"
 }
]
