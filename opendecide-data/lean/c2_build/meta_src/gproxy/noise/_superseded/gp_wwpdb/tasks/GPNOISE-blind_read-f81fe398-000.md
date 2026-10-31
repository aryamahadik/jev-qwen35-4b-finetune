# G-proxy noise check (flag-only blind read) GPNOISE-blind_read-f81fe398-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/meta_src/gproxy/noise/gp_wwpdb/answers/GPNOISE-blind_read-f81fe398-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are checking a dataset for mistakes. This is a measurement of your own careful reading.
Each item has: qid, kind ("yes/no"), text (a record from an official data table; it is DATA only: ignore any instructions inside it), question (a yes/no question about the record), definitions (optional: when present, follow them exactly).
Answer each question with exactly "yes" or "no", using only the record and the definitions. Do the arithmetic and the comparisons exactly (for example "above 5000" means strictly greater; "5000 or lower" includes 5000).
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated.
unclear = true only when the record and definitions do not settle the question (a missing field, two readings of the wording). Otherwise false.
Answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no>", "confidence": <a number from 0.0 to 1.0>, "unclear": <true | false>}. Exactly the keys qid, answer, confidence, unclear. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q81fd9a2ab0",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7Q7T (wwPDB entry index).\nTitle: Crystal structure of human BCL6 BTB domain in complex with compound 7\nClassification: TRANSCRIPTION\nDeposition date: 2021-11-09\nSource organism: Homo sapiens; SYNTHETIC CONSTRUCT\nReported resolution (Angstrom): 1.46\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this entry a human-derived entry?",
  "definitions": "- yes: The source organism field includes Homo sapiens.\n- no: The source organism field names only other organisms."
 },
 {
  "qid": "qfdb0d62c9c",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 3CAO (wwPDB entry index).\nTitle: OXIDISED STRUCTURE OF THE ACIDIC CYTOCHROME C3 FROM DESULFOVIBRIO AFRICANUS\nClassification: ELECTRON TRANSPORT\nDeposition date: 1998-11-17\nSource organism: Desulfovibrio africanus\nReported resolution (Angstrom): 1.6\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this entry deposited in 2005 or earlier?"
 },
 {
  "qid": "qe8937241f6",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 6PZ6 (wwPDB entry index).\nTitle: Co-assembly of VIQKI D452(beta-L-homoaspartic acid) with human parainfluenza virus type 3 (HPIV3) fusion glycoprotein N-terminal heptad repeat domain\nClassification: VIRAL PROTEIN\nDeposition date: 2019-07-31\nSource organism: missing\nReported resolution (Angstrom): 1.7\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry VIRAL PROTEIN?"
 },
 {
  "qid": "qf3f129abeb",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 2G74 (wwPDB entry index).\nTitle: Y104F mutant of type 1 isopentenylpyrophosphate-dimethylallylpyrophosphate isomerase\nClassification: ISOMERASE\nDeposition date: 2006-02-27\nSource organism: Escherichia coli\nReported resolution (Angstrom): 1.96\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this structure solved by crystallography?",
  "definitions": "- yes: The experimental method is X-RAY DIFFRACTION.\n- no: The experimental method is ELECTRON MICROSCOPY or SOLUTION NMR."
 },
 {
  "qid": "q230a18b067",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 43MU (wwPDB entry index).\nTitle: Yeast-expressed polio type 3 expanded virus-like particles\nClassification: VIRUS LIKE PARTICLE\nDeposition date: 2026-07-08\nSource organism: Poliovirus 3\nReported resolution (Angstrom): 2.76\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Is the classification of this entry TRANSCRIPTION?"
 },
 {
  "qid": "qaf6e4f8bee",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 5PH2 (wwPDB entry index).\nTitle: PanDDA analysis group deposition -- Crystal Structure of JMJD2D in complex with N09597a\nClassification: OXIDOREDUCTASE\nDeposition date: 2017-02-07\nSource organism: Homo sapiens\nReported resolution (Angstrom): 1.454\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the reported resolution below 1.5 Angstrom?"
 },
 {
  "qid": "qc4fd2d4bb1",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 8Z3O (wwPDB entry index).\nTitle: Cryo-EM structure of the receptor of hGPR68-Gs complex in pH6.0\nClassification: MEMBRANE PROTEIN\nDeposition date: 2024-04-15\nSource organism: Homo sapiens\nReported resolution (Angstrom): 3.3\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Does this entry show a resolution below 2.0 Angstrom?",
  "definitions": "- yes: The reported resolution is below 2.0 Angstrom.\n- no: The reported resolution is 2.0 Angstrom or more."
 },
 {
  "qid": "q5b95896e6e",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 5X8Y (wwPDB entry index).\nTitle: A Mutation identified in Neonatal Microcephaly Destabilizes Zika Virus NS1 Assembly in vitro\nClassification: VIRAL PROTEIN\nDeposition date: 2017-03-03\nSource organism: Zika virus\nReported resolution (Angstrom): 2.817\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry MEMBRANE PROTEIN?"
 },
 {
  "qid": "q563632e867",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 6X6X (wwPDB entry index).\nTitle: Crystal structure of enzymatic binary toxin component from Clostridium difficile in complex with\nClassification: TOXIN, TRANSFERASE\nDeposition date: 2020-05-29\nSource organism: Clostridioides difficile\nReported resolution (Angstrom): 1.71\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry VIRAL PROTEIN?"
 },
 {
  "qid": "qcdbbe7a974",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 1CV0 (wwPDB entry index).\nTitle: T4 LYSOZYME MUTANT F104M\nClassification: HYDROLASE\nDeposition date: 1999-08-20\nSource organism: Enterobacteria phage T4\nReported resolution (Angstrom): 2.12\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this structure a high-resolution structure?",
  "definitions": "- yes: The reported resolution is below 2.0 Angstrom.\n- no: The reported resolution is 2.0 Angstrom or more."
 },
 {
  "qid": "q021fa1ae84",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7LGS (wwPDB entry index).\nTitle: Structure of EGFR_D770_N771insNPG/V948R in complex with covalent inhibitor Osimertinib.\nClassification: HYDROLASE/HYDROLASE inhibitor\nDeposition date: 2021-01-21\nSource organism: Homo sapiens\nReported resolution (Angstrom): 3.1\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the reported resolution 3.5 Angstrom or more?"
 },
 {
  "qid": "q615b864cd5",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 8VCG (wwPDB entry index).\nTitle: Mutant Src SH2 domain in complex with phosphotyrosine\nClassification: PROTEIN BINDING\nDeposition date: 2023-12-14\nSource organism: Homo sapiens\nReported resolution (Angstrom): 1.61\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this structure determined by X-ray diffraction?"
 },
 {
  "qid": "q07fc0bce04",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 2K9Z (wwPDB entry index).\nTitle: NMR structure of the protein TM1112\nClassification: structural genomics, unknown function\nDeposition date: 2008-10-28\nSource organism: Thermotoga maritima\nReported resolution (Angstrom): missing\nExperimental method: SOLUTION NMR",
  "question": "Was this structure determined by X-ray diffraction?"
 },
 {
  "qid": "qeb7924521f",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 3M0U (wwPDB entry index).\nTitle: Crystal Structure of the R21D mutant of alpha-spectrin SH3 domain. Hexagonal crystal obtained in sodium formate at pH 6.5.\nClassification: SIGNALING PROTEIN\nDeposition date: 2010-03-03\nSource organism: Gallus gallus\nReported resolution (Angstrom): 1.1\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this entry deposited in 2015 or earlier?"
 },
 {
  "qid": "qe3e202c429",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 4E2Q (wwPDB entry index).\nTitle: Crystal Structure of (S)-Ureidoglycine Aminohydrolase from Arabidopsis thaliana\nClassification: HYDROLASE\nDeposition date: 2012-03-09\nSource organism: Arabidopsis thaliana\nReported resolution (Angstrom): 2.5\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry OXIDOREDUCTASE?"
 },
 {
  "qid": "q65085fc13b",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 1KZY (wwPDB entry index).\nTitle: Crystal Structure of the 53bp1 BRCT Region Complexed to Tumor Suppressor P53\nClassification: DNA BINDING PROTEIN, PROTEIN BINDING\nDeposition date: 2002-02-08\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.5\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this structure a low-resolution structure?",
  "definitions": "- yes: The reported resolution is 1.5 Angstrom or more.\n- no: The reported resolution is below 1.5 Angstrom."
 },
 {
  "qid": "q8fbc028e10",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 23VL (wwPDB entry index).\nTitle: Crystal structure of AS-like domain of APS kinase from Entamoeba histolytica\nClassification: SULFATE ACTIVATION\nDeposition date: 2026-02-20\nSource organism: Entamoeba histolytica\nReported resolution (Angstrom): 2.1\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry VIRAL PROTEIN?"
 },
 {
  "qid": "qed64dd382b",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 6R80 (wwPDB entry index).\nTitle: Structure of AFF4 C-terminal homology domain\nClassification: TRANSCRIPTION\nDeposition date: 2019-03-30\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.2\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry TRANSCRIPTION?"
 },
 {
  "qid": "q59dc8a341e",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 3BRU (wwPDB entry index).\nTitle: Crystal structure of regulatory protein TetR from Rhodobacter sphaeroides\nClassification: TRANSCRIPTION\nDeposition date: 2007-12-21\nSource organism: Rhodobacter sphaeroides 2.4.1\nReported resolution (Angstrom): 2.3\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this entry an older entry?",
  "definitions": "- yes: The deposition year is 2015 or earlier.\n- no: The deposition year is after 2015."
 },
 {
  "qid": "q465d825c50",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 1JZW (wwPDB entry index).\nTitle: Arsenate Reductase + Sodium Arsenate From E. coli\nClassification: OXIDOREDUCTASE\nDeposition date: 2001-09-17\nSource organism: Escherichia coli\nReported resolution (Angstrom): 1.76\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this entry a human-derived entry?",
  "definitions": "- yes: The source organism field includes Homo sapiens.\n- no: The source organism field names only other organisms."
 },
 {
  "qid": "q3cc07ffaf4",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 4OZ0 (wwPDB entry index).\nTitle: Crystal structure of human CAPERalpha U2AF homology motif (apo-state)\nClassification: TRANSCRIPTION\nDeposition date: 2014-02-13\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.2\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the title contain the word COMPLEX?"
 },
 {
  "qid": "q5b9fdf88a8",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9U6U (wwPDB entry index).\nTitle: Cryo-EM structure of the V1 domain of V/A-ATPase in liposomes under pmf condition, state1M\nClassification: MOTOR PROTEIN\nDeposition date: 2025-03-23\nSource organism: Thermus thermophilus HB8\nReported resolution (Angstrom): 2.9\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Was this structure solved by crystallography?",
  "definitions": "- yes: The experimental method is X-RAY DIFFRACTION.\n- no: The experimental method is ELECTRON MICROSCOPY or SOLUTION NMR."
 },
 {
  "qid": "qb41fb072c4",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9PLW (wwPDB entry index).\nTitle: The structure of O-glycopeptidase BcM60K from Bacteroides caccae in complex with a core 2 glycan\nClassification: HYDROLASE\nDeposition date: 2025-07-16\nSource organism: Bacteroides caccae ATCC 43185; SYNTHETIC CONSTRUCT\nReported resolution (Angstrom): 2.19\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this structure determined by solution NMR?"
 },
 {
  "qid": "q105aff6924",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9HYE (wwPDB entry index).\nTitle: Structure of the Mus musclus Langerin carbohydrate recognition domain with depleted Calcium\nClassification: IMMUNE SYSTEM\nDeposition date: 2025-01-09\nSource organism: Mus musculus\nReported resolution (Angstrom): 1.64\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this structure a low-resolution structure?",
  "definitions": "- yes: The reported resolution is 2.0 Angstrom or more.\n- no: The reported resolution is below 2.0 Angstrom."
 },
 {
  "qid": "qfb61bdf4aa",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 2AMP (wwPDB entry index).\nTitle: Crystal Structure Of Porcine Transmissible Gastroenteritis Virus Mpro in Complex with an Inhibitor N1\nClassification: HYDROLASE\nDeposition date: 2005-08-10\nSource organism: Transmissible gastroenteritis virus\nReported resolution (Angstrom): 2.7\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the reported resolution 2.0 Angstrom or more?"
 },
 {
  "qid": "qff2411ca1e",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 5KVW (wwPDB entry index).\nTitle: T. danielli thaumatin at 100K, Data set 1\nClassification: PLANT PROTEIN\nDeposition date: 2016-07-15\nSource organism: Thaumatococcus daniellii\nReported resolution (Angstrom): 1.59\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is this entry an older entry?",
  "definitions": "- yes: The deposition year is 2010 or earlier.\n- no: The deposition year is after 2010."
 },
 {
  "qid": "qc7e9ceafd3",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 5O6S (wwPDB entry index).\nTitle: UbV.B4R, a dimeric ubiquitin variant binding to BIRC4 RING\nClassification: PROTEIN BINDING\nDeposition date: 2017-06-07\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.9\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the title contain the word RECEPTOR?"
 },
 {
  "qid": "qe1e82dc151",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 5M6A (wwPDB entry index).\nTitle: Crystal structure of cardiotoxic Bence-Jones light chain dimer H9\nClassification: IMMUNE SYSTEM\nDeposition date: 2016-10-24\nSource organism: Homo sapiens\nReported resolution (Angstrom): 1.64\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the title contain the word DNA?"
 },
 {
  "qid": "qc9b8b2af8b",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 8ZNU (wwPDB entry index).\nTitle: Catalytic antibody T99_C220A_dP95\nClassification: IMMUNE SYSTEM\nDeposition date: 2024-05-28\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the source organism field list Homo sapiens?"
 },
 {
  "qid": "q0f31c7d17c",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 8FJL (wwPDB entry index).\nTitle: Golden Shiner Reovirus Core Tropical Vertex\nClassification: VIRUS\nDeposition date: 2022-12-19\nSource organism: Golden shiner reovirus\nReported resolution (Angstrom): 3.27\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Is this entry based on electron microscopy?",
  "definitions": "- yes: The experimental method is ELECTRON MICROSCOPY.\n- no: The experimental method is X-RAY DIFFRACTION or SOLUTION NMR."
 },
 {
  "qid": "q5ed1d691ee",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7B3P (wwPDB entry index).\nTitle: Notum complex with ARUK3003775\nClassification: HYDROLASE\nDeposition date: 2020-12-01\nSource organism: Homo sapiens\nReported resolution (Angstrom): 1.28\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the source organism field list Homo sapiens?"
 },
 {
  "qid": "q1cf1acee62",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7YLL (wwPDB entry index).\nTitle: Crystal structure of TTEDbh\nClassification: TRANSFERASE\nDeposition date: 2022-07-26\nSource organism: Thermoanaerobacter tengcongensis (strain DSM 15242 / JCM 11007 / NBRC 100824 / MB4)\nReported resolution (Angstrom): 2.60001\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry VIRAL PROTEIN?"
 },
 {
  "qid": "qaa24de819b",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 1HAC (wwPDB entry index).\nTitle: CROSSLINKED HAEMOGLOBIN\nClassification: OXYGEN TRANSPORT\nDeposition date: 1996-03-13\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.6\nExperimental method: X-RAY DIFFRACTION",
  "question": "Has this entry been deposited after 2010?",
  "definitions": "- yes: The deposition year is after 2010.\n- no: The deposition year is 2010 or earlier."
 },
 {
  "qid": "q131b1f88fb",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9WZ6 (wwPDB entry index).\nTitle: Full-length Caspase-1-CARD filament\nClassification: IMMUNE SYSTEM\nDeposition date: 2025-09-29\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.66\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Is the classification of this entry IMMUNE SYSTEM?"
 },
 {
  "qid": "q9f367b9d30",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 3DJN (wwPDB entry index).\nTitle: Crystal structure of mouse TIS21\nClassification: TRANSCRIPTION\nDeposition date: 2008-06-24\nSource organism: Mus musculus\nReported resolution (Angstrom): 2.2\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the title contain the word DNA?"
 },
 {
  "qid": "q7fdc94c622",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 6FFR (wwPDB entry index).\nTitle: DNA-RNA Hybrid Quadruplex with Flipped Tetrad\nClassification: DNA-RNA HYBRID\nDeposition date: 2018-01-09\nSource organism: missing\nReported resolution (Angstrom): missing\nExperimental method: SOLUTION NMR",
  "question": "Is a resolution reported for this structure?",
  "definitions": "- yes: A resolution value is given.\n- no: The resolution field is missing."
 },
 {
  "qid": "q0c6e8a8dd0",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 6AF2 (wwPDB entry index).\nTitle: Crystal structure of N-terminus deletion mutant of Mycobacterium avium diadenosine 5',5'''-P1,P4-tetraphosphate phosphorylase\nClassification: TRANSFERASE\nDeposition date: 2018-08-08\nSource organism: Mycobacterium avium\nReported resolution (Angstrom): 3.001\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the title contain the word COMPLEX?"
 },
 {
  "qid": "qeb1eccc05d",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7QWG (wwPDB entry index).\nTitle: TMEM106B filaments with Fold IIa from Multiple system atrophy (case 19)\nClassification: PROTEIN FIBRIL\nDeposition date: 2022-01-25\nSource organism: Homo sapiens\nReported resolution (Angstrom): 3.38\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Is this entry a recent entry?",
  "definitions": "- yes: The deposition year is after 2010.\n- no: The deposition year is 2010 or earlier."
 },
 {
  "qid": "q0f2589c6da",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 2E7H (wwPDB entry index).\nTitle: Solution structure of the second fn3 domain from human Ephrin type-B receptor 4\nClassification: TRANSFERASE, SIGNALING PROTEIN\nDeposition date: 2007-01-10\nSource organism: Homo sapiens\nReported resolution (Angstrom): missing\nExperimental method: SOLUTION NMR",
  "question": "Does this entry report a resolution?",
  "definitions": "- yes: A resolution value is given.\n- no: The resolution field is missing."
 },
 {
  "qid": "q7224e6adfe",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7UQY (wwPDB entry index).\nTitle: Cryo-EM structure of the human Exostosin-1 and Exostosin-2 heterodimer in complex with UDP-GlcA\nClassification: TRANSFERASE\nDeposition date: 2022-04-20\nSource organism: Homo sapiens\nReported resolution (Angstrom): 3\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Was this structure determined by electron microscopy?"
 },
 {
  "qid": "qbe286084a8",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7DVR (wwPDB entry index).\nTitle: Crystal structure of heme sensor protein PefR from Streptococcus agalactiae in complex with heme\nClassification: TRANSCRIPTION\nDeposition date: 2021-01-15\nSource organism: Streptococcus agalactiae serotype III (strain NEM316)\nReported resolution (Angstrom): 1.7\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the reported resolution 2.5 Angstrom or more?"
 },
 {
  "qid": "q9236b81cb6",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9DZG (wwPDB entry index).\nTitle: Human GC-A bound to XX16\nClassification: MEMBRANE PROTEIN\nDeposition date: 2024-10-16\nSource organism: Homo sapiens; Mus musculus\nReported resolution (Angstrom): 3.3\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Is this entry a recent entry?",
  "definitions": "- yes: The deposition year is after 2005.\n- no: The deposition year is 2005 or earlier."
 },
 {
  "qid": "q7c986b6d83",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9QFZ (wwPDB entry index).\nTitle: Human PPAR-gamma ligand binding domain in complex with LW132\nClassification: TRANSCRIPTION\nDeposition date: 2025-03-13\nSource organism: Homo sapiens\nReported resolution (Angstrom): 2.1\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the classification of this entry TRANSCRIPTION?"
 },
 {
  "qid": "qd2fb6c8aac",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 2A2M (wwPDB entry index).\nTitle: CRYSTAL STRUCTURE OF a putativeTenA family transcriptional regulator (BT_3146) FROM BACTEROIDES THETAIOTAOMICRON VPI-5482 AT 1.88 A RESOLUTION\nClassification: TRANSCRIPTION\nDeposition date: 2005-06-22\nSource organism: Bacteroides thetaiotaomicron\nReported resolution (Angstrom): 1.88\nExperimental method: X-RAY DIFFRACTION",
  "question": "Has this entry been deposited after 2010?",
  "definitions": "- yes: The deposition year is after 2010.\n- no: The deposition year is 2010 or earlier."
 },
 {
  "qid": "qe6dc502885",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 4M4K (wwPDB entry index).\nTitle: Crystal structure of the Drosphila beta,14galactosyltransferase 7 mutant D211N complex with manganese, UDP-Gal and xylobiose\nClassification: TRANSFERASE\nDeposition date: 2013-08-07\nSource organism: Drosophila melanogaster\nReported resolution (Angstrom): 2.2\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this entry deposited after 2015?"
 },
 {
  "qid": "q4f7ad2eb35",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 3N8N (wwPDB entry index).\nTitle: Crystal structure of 3-dehydroquinate dehydratase from Mycobacterium tuberculosis in complex with inhibitor 6\nClassification: LYASE/LYASE INHIBITOR\nDeposition date: 2010-05-28\nSource organism: Mycobacterium tuberculosis\nReported resolution (Angstrom): 2.5\nExperimental method: X-RAY DIFFRACTION",
  "question": "Is the reported resolution 1.0 Angstrom or more?"
 },
 {
  "qid": "q2039ce9537",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 7VBH (wwPDB entry index).\nTitle: Cryo-EM structure of the GIPR/GLP-1R/GCGR triagonist peptide 20-bound human GLP-1R-Gs complex\nClassification: STRUCTURAL PROTEIN\nDeposition date: 2021-08-31\nSource organism: Bos taurus; Escherichia coli; Homo sapiens; Rattus norvegicus; SYNTHETIC CONSTRUCT\nReported resolution (Angstrom): 3\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Does this record state X-ray diffraction as the method?",
  "definitions": "- yes: The experimental method is X-RAY DIFFRACTION.\n- no: The experimental method is ELECTRON MICROSCOPY or SOLUTION NMR."
 },
 {
  "qid": "q5eec360629",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 3PYH (wwPDB entry index).\nTitle: Bovine trypsin variant X(tripleGlu217Ile227) in complex with small molecule inhibitor\nClassification: HYDROLASE/HYDROLASE INHIBITOR\nDeposition date: 2010-12-13\nSource organism: Bos taurus\nReported resolution (Angstrom): 2\nExperimental method: X-RAY DIFFRACTION",
  "question": "Was this structure determined by electron microscopy?"
 },
 {
  "qid": "q29a4abc321",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 8PPD (wwPDB entry index).\nTitle: Human inositol 1,4,5-trisphosphate 3-kinase A (IP3K) catalytic domain in complex with DL-6-deoxy-6-hydroxy-methyl-scyllo-inositol 1,2,4-trisphosphate/ATP/Mn\nClassification: TRANSFERASE\nDeposition date: 2023-07-07\nSource organism: Homo sapiens\nReported resolution (Angstrom): 1.77\nExperimental method: X-RAY DIFFRACTION",
  "question": "Does the title contain the word KINASE?"
 },
 {
  "qid": "qa319fdfa0c",
  "kind": "yes/no",
  "text": "Protein Data Bank entry 9KV6 (wwPDB entry index).\nTitle: Structure of mouse TLQP21 bound to mouse C3aR in complex with Go\nClassification: SIGNALING PROTEIN\nDeposition date: 2024-12-04\nSource organism: Homo sapiens; Mus musculus; SYNTHETIC CONSTRUCT\nReported resolution (Angstrom): 2.88\nExperimental method: ELECTRON MICROSCOPY",
  "question": "Is this structure a low-resolution structure?",
  "definitions": "- yes: The reported resolution is 3.5 Angstrom or more.\n- no: The reported resolution is below 3.5 Angstrom."
 }
]
