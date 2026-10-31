# G9 re-read (G5-H blind read) MD-B07 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/answers/MD-B07.json

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
  "qid": "q0fe4808cc5",
  "kind": "yes/no",
  "text": "Bibliographic record\nwork_type: review\npublication_date: 2006-12-28\nis_oa: false\ncited_by_count: 59",
  "question": "Under the card, is this entry highly cited?",
  "definitions": "- yes: Yes if the citation count is 10 or more.\n- no: No if the citation count is below 10."
 },
 {
  "qid": "q4ce818801c",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nLocal authority: Swindon\nRating: 5",
  "question": "Does this establishment meet the rule?",
  "definitions": "- yes: The rating is 5 or 4.\n- no: The rating is any other value."
 },
 {
  "qid": "q537781c4ee",
  "kind": "yes/no",
  "text": "Guatemala City, Guatemala",
  "question": "Is Guatemala City the capital city of Guatemala?"
 },
 {
  "qid": "qebd1645452",
  "kind": "choice",
  "text": "Food hygiene record\nBusiness type: Takeaway/sandwich shop\nHygiene score: 0\nStructural score: 5\nConfidence in management score: 10",
  "question": "Which of the three scores is the highest?",
  "options": [
   "structural score",
   "confidence in management score",
   "hygiene score"
  ]
 },
 {
  "qid": "q9e5ec6307c",
  "kind": "yes/no",
  "text": "Scholarly work metadata\n| Field | Value |\n| --- | --- |\n| Work ID | W2094594732 |\n| Publication year | 2010 |\n| Reference year | 2026 |\n| Citation count | 9 |\n| References listed | 33 |\n| Distinct countries | 1 |",
  "question": "Is the citation count higher than the number of references listed?"
 },
 {
  "qid": "q3477729da9",
  "kind": "choice",
  "text": "Organization: Research Foundation ITSUU Laboratory",
  "question": "In which country is Research Foundation ITSUU Laboratory?",
  "options": [
   "Japan",
   "Spain",
   "France",
   "Greece"
  ]
 },
 {
  "qid": "q373d5f3657",
  "kind": "yes/no",
  "text": "Organization: Guangdong Province Science and Technology Library",
  "question": "Is the country of Guangdong Province Science and Technology Library China?"
 },
 {
  "qid": "qcaa93b80a7",
  "kind": "yes/no",
  "text": "Food hygiene record\nBusiness type: Other catering premises\nLocal authority: Newport\nRating: 5",
  "question": "Is this establishment eligible under the rule?",
  "definitions": "- yes: The business type is Pub/bar/nightclub, School/college/university or Manufacturers/packers.\n- no: The business type is any other type."
 },
 {
  "qid": "q85663cfa0e",
  "kind": "yes/no",
  "text": "Accession number: 1972.121\nObject type: Painting\nCollection: P - Italian 16th & 17th Century\nTechnique: oil on wood\nCulture: Italy, Florence\nDate text: c. 1550\nDate range: 1550 to 1550\nMeasurements: Framed: 81.6 x 68.5 x 6.7 cm (32 1/8 x 26 15/16 x 2 5/8 in.); Unframed: 60 x 48.8 cm (23 5/8 x 19 3/16 in.)\nCredit line, first word: Leonard",
  "question": "Was this work begun before the year 1800?"
 },
 {
  "qid": "qeeb1f3baed",
  "kind": "yes/no",
  "text": "Accession number: 1982.107\nObject type: Textile\nCollection: T - Coptic\nTechnique: wool; plain weave with slit-tapestry weave\nCulture: Egypt, Umayyad period (661–750) or Abbasid period (750–1258)\nDate text: 700s\nDate range: 700 to 799\nMeasurements: not listed\nCredit line, first word: Andrew",
  "question": "Is the gap between the first and last year above 25 years?",
  "definitions": "- yes: the last year minus the first year of the Date range is more than 25.\n- no: the last year minus the first year of the Date range is 25 or less."
 },
 {
  "qid": "q0122141849",
  "kind": "yes/no",
  "text": "Project ID: 740712\nProgramme: Horizon 2020\nFunding scheme: IA\nCall topic: DS-02-2016\nStart date: 2017-05-01\nEnd date: 2019-10-31\nTotal cost: 4283480 EUR\nEC maximum contribution: 3648792.5 EUR",
  "question": "Is the EC maximum contribution above 5,000,000 EUR?"
 },
 {
  "qid": "qa9378f2be9",
  "kind": "choice",
  "text": "Project and operations register row\nProject ID: P132317\nLending instrument: Investment Project Financing\nTotal commitment (USD million): 523.32\nBoard approval date: 2014-08-29\nMajor themes listed: 2",
  "question": "Pick the fiscal year of the board approval for this entry.",
  "options": [
   "2017",
   "2015",
   "2016",
   "2014"
  ],
  "definitions": "The World Bank fiscal year runs from 1 July to 30 June and is named after the calendar year in which it ends. Approval on or after 1 July of year Y falls in fiscal year Y+1; approval before 1 July falls in fiscal year Y."
 },
 {
  "qid": "q140cb5f68d",
  "kind": "yes/no",
  "text": "GO term: GO:0022605\nName: mammalian oogenesis stage\nDefinition: A reproductive process that is a step in the formation and maturation of an ovum or female gamete from a primordial female germ cell.\nDefinition sources: GOC:isa_complete, GOC:mtg_sensu\nSynonyms (1): \"mammalian oogenesis process\" EXACT\nDirect is_a parents (1): multicellular organismal reproductive process\nOther relationships: part_of oogenesis\nSubsets: none listed\nCross-references (0): none listed",
  "question": "Is it true that this GO term has more than 1 listed synonyms?"
 },
 {
  "qid": "qd13a7f4588",
  "kind": "choice",
  "text": "Project ID: 700667\nProgramme: Horizon 2020\nFunding scheme: FCH2-RIA\nCall topic: FCH-02.6-2015\nStart date: 2016-04-01\nEnd date: 2019-03-31\nTotal cost: 2944176.25 EUR\nEC maximum contribution: 1994301.25 EUR",
  "question": "Which group does the funding scheme belong to?",
  "options": [
   "research and innovation (RIA, IA)",
   "European Research Council (ERC)",
   "coordination and support (CSA)",
   "SME instrument (SME)",
   "Marie Sklodowska-Curie (MSCA)",
   "other schemes"
  ],
  "definitions": "- research and innovation (RIA, IA): scheme RIA, IA, CS2-RIA or CS2-IA\n- coordination and support (CSA): scheme CSA\n- Marie Sklodowska-Curie (MSCA): any scheme code that starts with MSCA\n- European Research Council (ERC): any scheme code that starts with ERC\n- SME instrument (SME): any scheme code that starts with SME\n- other schemes: every other scheme code"
 },
 {
  "qid": "qd8ee982b87",
  "kind": "yes/no",
  "text": "Catalogue entry for a scholarly work\ncited_by_count: 460\nhas_fulltext: false\nvolume: 28\nvenue: Pattern Recognition Letters",
  "question": "Is the citation count at least 100?"
 },
 {
  "qid": "q273d9deb5d",
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
  "qid": "q0f674a37fb",
  "kind": "yes/no",
  "text": "Organization: Delta Extinguishers (Belgium)\nCountry: Belgium\nType (record): company",
  "question": "Does Delta Extinguishers (Belgium) meet this rule?",
  "definitions": "- yes: The organization's type is company or education.\n- no: The organization has any other type."
 },
 {
  "qid": "q507d045a5f",
  "kind": "yes/no",
  "text": "Accession number: 1929.889\nObject type: Print\nCollection: PR - Etching\nTechnique: etching\nCulture: Spain\nDate text: 1905, printed 1913\nDate range: 1905 to 1913\nMeasurements: not listed\nCredit line, first word: Dudley",
  "question": "Does the accession number start with a year of 1930 or later?",
  "definitions": "- yes: the four-digit year at the start of the accession number is 1930 or later.\n- no: that year is earlier than 1930."
 },
 {
  "qid": "q786bdb1d64",
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
  "qid": "q1b805660b8",
  "kind": "choice",
  "text": "Organization: St John of God Subiaco Hospital\nCountry: Australia",
  "question": "Which group does St John of God Subiaco Hospital fall into under these definitions?",
  "options": [
   "Group C",
   "Group A",
   "Group B",
   "None of these groups"
  ],
  "definitions": "- Group A: Australia, United States or Argentina\n- Group B: Canada, Spain or Mexico\n- Group C: Nigeria, Indonesia or New Zealand\n- None of these groups: any other country"
 },
 {
  "qid": "qa08d86f7c0",
  "kind": "yes/no",
  "text": "Index record of a publication\nTopic field Social Sciences; Open-access status green; Work ID W2275129849; Publication date 1996-10-31; Topic domain Social Sciences.",
  "question": "Is it the case that the record does not fail to give 'green' as the open-access status?"
 },
 {
  "qid": "qb7fc569ae7",
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
  "qid": "q28bf0be74b",
  "kind": "choice",
  "text": "Organization: Polytechnic University of the Valley of Mexico\nCountry: Mexico",
  "question": "In which period was Polytechnic University of the Valley of Mexico (Mexico) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "1900-1949",
   "1800-1899"
  ]
 },
 {
  "qid": "q2f8dc166ab",
  "kind": "yes/no",
  "text": "Catalogue row for a seismic event\n- Magnitude = 2.5\n- PAGER alert = none\n- Origin time (UTC) = 2026-07-14 01:07:50\n- Location description = 15 km SE of Fern Forest, Hawaii\n- Depth (km) = 7.5",
  "question": "Does this entry count as a strong earthquake under the card?",
  "definitions": "- yes: Yes if the magnitude is 6.0 or higher.\n- no: No if the magnitude is below 6.0."
 },
 {
  "qid": "qb3deca5f94",
  "kind": "yes/no",
  "text": "City: Damascus\nCountry: Syria",
  "question": "Does Syria have Damascus as its capital?"
 },
 {
  "qid": "q4d3f5bfa48",
  "kind": "yes/no",
  "text": "Bibliographic record\n{\n  \"last_page\": 107,\n  \"first_page\": 93,\n  \"references_count\": 0,\n  \"countries\": 0,\n  \"work_type\": \"review\"\n}",
  "question": "Is the page span, counting both end pages, below 10?"
 },
 {
  "qid": "qe59ecfc6ba",
  "kind": "choice",
  "text": "Place: Konjic\nCountry: Bosnia and Herzegovina",
  "question": "Which group does the country of Konjic belong to under these definitions?",
  "options": [
   "Group C",
   "None of these groups",
   "Group A",
   "Group B"
  ],
  "definitions": "- Group A: China, India or Poland\n- Group B: North Korea, Finland or Ukraine\n- Group C: Bosnia and Herzegovina, Ethiopia or Bangladesh\n- None of these groups: any other country"
 }
]
