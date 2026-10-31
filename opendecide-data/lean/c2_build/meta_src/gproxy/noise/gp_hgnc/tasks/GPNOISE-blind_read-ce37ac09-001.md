# G-proxy noise check (flag-only blind read) GPNOISE-blind_read-ce37ac09-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/meta_src/gproxy/noise/gp_hgnc/answers/GPNOISE-blind_read-ce37ac09-001.json

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
  "qid": "q98a3618dc5",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:33410\nSymbol: KRT18P12\nName: keratin 18 pseudogene 12\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 1q41\nDate approved: 2007-03-19\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000215819\nEntrez ID: 643471\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is a gene group given for this gene?",
  "definitions": "- yes: The gene group field is filled.\n- no: The gene group field is empty."
 },
 {
  "qid": "q79d31fab1d",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:14350\nSymbol: ARID3B\nName: AT-rich interaction domain 3B\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 15q24.1\nDate approved: 2004-01-28\nAlias symbols: BDP, DRIL2\nPrevious symbols: empty\nGene group: AT-rich interaction domain containing\nEnsembl gene ID: ENSG00000179361\nEntrez ID: 10620\nOMIM ID: 612457\nUniProt IDs: Q8IVW6",
  "question": "Is the locus type of this gene gene with protein product?"
 },
 {
  "qid": "qb72f9093e5",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:1485\nSymbol: CAPN8\nName: calpain 8\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 1q41\nDate approved: 1998-09-25\nAlias symbols: nCL-2\nPrevious symbols: empty\nGene group: EF-hand domain containing, Calpains\nEnsembl gene ID: ENSG00000203697\nEntrez ID: 388743\nOMIM ID: 618777\nUniProt IDs: A6NHC0",
  "question": "Is this gene an older approval?",
  "definitions": "- yes: The date approved is 2015 or earlier.\n- no: The date approved is after 2015."
 },
 {
  "qid": "qbfad508347",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:23695\nSymbol: DIXDC1\nName: DIX domain containing 1\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 11q23.1\nDate approved: 2003-12-03\nAlias symbols: KIAA1735, Dixin\nPrevious symbols: empty\nGene group: Dishevelled segment polarity proteins\nEnsembl gene ID: ENSG00000150764\nEntrez ID: 85458\nOMIM ID: 610493\nUniProt IDs: Q155Q3",
  "question": "Does the gene name contain the word family?"
 },
 {
  "qid": "q40abe3519d",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:28447\nSymbol: CLUHP3\nName: CLUH pseudogene 3\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 16p11.2\nDate approved: 2006-04-04\nAlias symbols: MGC3020\nPrevious symbols: C16orf67, KIAA0664P3, KIAA0664L3\nGene group: empty\nEnsembl gene ID: ENSG00000131797\nEntrez ID: 100132341\nOMIM ID: empty\nUniProt IDs: Q96NS8",
  "question": "Does this record have a value for OMIM ID?"
 },
 {
  "qid": "qba842fd1ca",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:1589\nSymbol: CCNE1\nName: cyclin E1\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 19q12\nDate approved: 1991-12-10\nAlias symbols: empty\nPrevious symbols: CCNE\nGene group: Cyclins\nEnsembl gene ID: ENSG00000105173\nEntrez ID: 898\nOMIM ID: 123837\nUniProt IDs: P24864",
  "question": "Is this gene a protein-coding gene?",
  "definitions": "- yes: The locus group is protein-coding gene.\n- no: The locus group is pseudogene, non-coding RNA or other."
 },
 {
  "qid": "q84b2415a09",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:18505\nSymbol: RNF43\nName: ring finger protein 43\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 17q22\nDate approved: 2002-04-18\nAlias symbols: FLJ20315, RNF124, DKFZp781H0392, URCC\nPrevious symbols: empty\nGene group: Ring finger proteins, RING finger E3 ubiquitin protein ligases\nEnsembl gene ID: ENSG00000108375\nEntrez ID: 54894\nOMIM ID: 612482\nUniProt IDs: Q68DV7",
  "question": "Does the gene name contain the word receptor?"
 },
 {
  "qid": "qf0f5183f55",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:7922\nSymbol: NPM1P2\nName: nucleophosmin 1 pseudogene 2\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 18q11.2\nDate approved: 1993-08-24\nAlias symbols: NG2-6\nPrevious symbols: NPMP2\nGene group: empty\nEnsembl gene ID: ENSG00000266227\nEntrez ID: 4871\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is this gene located on chromosome 11?"
 },
 {
  "qid": "qac45d72879",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:51184\nSymbol: LINC01503\nName: long independently transcribed non-coding RNA 1503\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 9q34.11\nDate approved: 2014-08-01\nAlias symbols: lnc-PPP2R4-5, RP11-65J3.1\nPrevious symbols: empty\nGene group: Long independently transcribed non-coding RNAs\nEnsembl gene ID: ENSG00000233901\nEntrez ID: 100506119\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does the gene name contain the word family?"
 },
 {
  "qid": "q331830f692",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:58171\nSymbol: RAD51B-AS1\nName: RAD51B antisense RNA 1\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 14q24.1\nDate approved: 2025-01-13\nAlias symbols: CTD-2566J3.1\nPrevious symbols: empty\nGene group: Antisense RNAs\nEnsembl gene ID: ENSG00000258623\nEntrez ID: 124903333\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Was this gene approved after 2020?"
 },
 {
  "qid": "qeb594f457d",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:12666\nSymbol: VCP\nName: valosin containing protein\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 9p13.3\nDate approved: 1996-08-22\nAlias symbols: IBMPFD, p97, CDC48, TERA\nPrevious symbols: empty\nGene group: AAA ATPases, VCP-Ufd1-Npl4 complex subunits\nEnsembl gene ID: ENSG00000165280\nEntrez ID: 7415\nOMIM ID: 601023\nUniProt IDs: P55072",
  "question": "Can this gene match a UniProt entry?",
  "definitions": "- yes: The UniProt IDs field is filled.\n- no: The UniProt IDs field is empty."
 },
 {
  "qid": "q9dd7d78355",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:18606\nSymbol: OXCT2\nName: 3-oxoacid CoA-transferase 2\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 1p34.2\nDate approved: 2002-05-02\nAlias symbols: FKSG25, FLJ00030, SCOT-T\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000198754\nEntrez ID: 64064\nOMIM ID: 610289\nUniProt IDs: Q9BYC2",
  "question": "Is this gene located on chromosome 1?"
 },
 {
  "qid": "q81ca275b8a",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:25976\nSymbol: ELP6\nName: elongator acetyltransferase complex subunit 6\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 3p21.31\nDate approved: 2005-12-19\nAlias symbols: FLJ20211\nPrevious symbols: TMEM103, C3orf75\nGene group: Elongator acetyltransferase complex \nEnsembl gene ID: ENSG00000163832\nEntrez ID: 54859\nOMIM ID: 615020\nUniProt IDs: Q0PNE2",
  "question": "Is the locus type of this gene gene with protein product?"
 },
 {
  "qid": "q4d8373a756",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:15959\nSymbol: CST11\nName: cystatin 11\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 20p11.21\nDate approved: 2001-09-17\nAlias symbols: dJ322G13.6, CTES2\nPrevious symbols: CST8L\nGene group: Cystatins, type 2\nEnsembl gene ID: ENSG00000125831\nEntrez ID: 140880\nOMIM ID: 609731\nUniProt IDs: Q9H112",
  "question": "Can this gene encode a protein?",
  "definitions": "- yes: The locus group is protein-coding gene.\n- no: The locus group is pseudogene, non-coding RNA or other."
 },
 {
  "qid": "qf075b8ed61",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:46345\nSymbol: RN7SL329P\nName: RNA, 7SL, cytoplasmic 329, pseudogene\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 8q24.13\nDate approved: 2013-04-02\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000242170\nEntrez ID: 106479343\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is this gene listed as a protein-coding gene?",
  "definitions": "- yes: The locus group is protein-coding gene.\n- no: The locus group is pseudogene, non-coding RNA or other."
 },
 {
  "qid": "qfec5858d99",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:55821\nSymbol: LINC02930\nName: long independently transcribed non-coding RNA 2930\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 10q26.12\nDate approved: 2021-07-30\nAlias symbols: empty\nPrevious symbols: empty\nGene group: Long independently transcribed non-coding RNAs\nEnsembl gene ID: ENSG00000274461\nEntrez ID: 105378516\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Has this gene been given a gene group?",
  "definitions": "- yes: The gene group field is filled.\n- no: The gene group field is empty."
 },
 {
  "qid": "q5900c36e21",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:20263\nSymbol: SETDB2\nName: SET domain bifurcated histone lysine methyltransferase 2\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 13q14.2\nDate approved: 2003-01-16\nAlias symbols: CLLD8, CLLL8, KMT1F\nPrevious symbols: C13orf4\nGene group: Histone lysine methyltransferases, Methyl-CpG binding domain containing, SET domain containing\nEnsembl gene ID: ENSG00000136169\nEntrez ID: 83852\nOMIM ID: 607865\nUniProt IDs: Q96T68",
  "question": "Does the gene name contain the word protein?"
 },
 {
  "qid": "qa1a9c35fc9",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:58551\nSymbol: HLF-AS1\nName: HLF antisense RNA 1\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 17q22\nDate approved: 2025-07-17\nAlias symbols: empty\nPrevious symbols: empty\nGene group: Antisense RNAs\nEnsembl gene ID: ENSG00000263096\nEntrez ID: empty\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this record have a value for Entrez ID?"
 },
 {
  "qid": "q6079bc3aa2",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:30437\nSymbol: ASPHD2\nName: aspartate beta-hydroxylase domain containing 2\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 22q12.1\nDate approved: 2006-01-31\nAlias symbols: FLJ39838\nPrevious symbols: empty\nGene group: Aspartate beta-hydroxylase domain containing\nEnsembl gene ID: ENSG00000128203\nEntrez ID: 57168\nOMIM ID: empty\nUniProt IDs: Q6ICH7",
  "question": "Does this gene have alias symbols on file?",
  "definitions": "- yes: The alias symbols field is filled.\n- no: The alias symbols field is empty."
 },
 {
  "qid": "qeb94c56e03",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:34091\nSymbol: RNY5P10\nName: RNY5 pseudogene 10\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 19q13.12\nDate approved: 2008-05-01\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: empty\nEntrez ID: 100169837\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does the gene name contain the word kinase?"
 },
 {
  "qid": "q7b4bee4528",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:58065\nSymbol: PIEZO1-AS1\nName: PIEZO1 antisense RNA 1\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 16q24.3\nDate approved: 2024-08-08\nAlias symbols: empty\nPrevious symbols: empty\nGene group: Antisense RNAs\nEnsembl gene ID: ENSG00000182376\nEntrez ID: 339059\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this gene have Entrez ID on file?",
  "definitions": "- yes: The Entrez ID field is filled.\n- no: The Entrez ID field is empty."
 },
 {
  "qid": "qb95748ad55",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:24930\nSymbol: TMEM176A\nName: transmembrane protein 176A\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 7q36.1\nDate approved: 2006-09-04\nAlias symbols: HCA112, MS4B1\nPrevious symbols: empty\nGene group: Membrane spanning 4-domains\nEnsembl gene ID: ENSG00000002933\nEntrez ID: 55365\nOMIM ID: 610334\nUniProt IDs: Q96HP8",
  "question": "Does this gene have Ensembl gene ID on file?",
  "definitions": "- yes: The Ensembl gene ID field is filled.\n- no: The Ensembl gene ID field is empty."
 },
 {
  "qid": "qd5249c7660",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:26515\nSymbol: COQ10A\nName: coenzyme Q10A\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 12q13.3\nDate approved: 2006-01-13\nAlias symbols: FLJ32452\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000135469\nEntrez ID: 93058\nOMIM ID: 620736\nUniProt IDs: Q96MF6",
  "question": "Does this gene possess an alias symbol?",
  "definitions": "- yes: The alias symbols field is filled.\n- no: The alias symbols field is empty."
 },
 {
  "qid": "qac8de94dac",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:49866\nSymbol: NDFIP1P1\nName: Nedd4 family interacting protein 1 pseudogene 1\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 12p12.3\nDate approved: 2014-03-18\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000255892\nEntrez ID: 100420792\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is the locus group of this gene pseudogene?"
 },
 {
  "qid": "q53954d8fb0",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:37001\nSymbol: RPS15AP10\nName: ribosomal protein S15a pseudogene 10\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 1p34.1\nDate approved: 2009-03-06\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000225447\nEntrez ID: 728963\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this gene have Entrez ID on file?",
  "definitions": "- yes: The Entrez ID field is filled.\n- no: The Entrez ID field is empty."
 },
 {
  "qid": "q18b13505fd",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:59008\nSymbol: H3Y2-AS1\nName: H3Y2 antisense RNA 1\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 5p15.1\nDate approved: 2025-12-18\nAlias symbols: empty\nPrevious symbols: empty\nGene group: Antisense RNAs\nEnsembl gene ID: ENSG00000295870\nEntrez ID: empty\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is this gene on a short chromosome arm?",
  "definitions": "- yes: The chromosomal location has the arm letter p.\n- no: The chromosomal location has the arm letter q."
 },
 {
  "qid": "q0328d05ada",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:15859\nSymbol: TASP1\nName: taspase 1\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 20p12.1\nDate approved: 2001-06-21\nAlias symbols: FLJ20212, dJ585I14.2\nPrevious symbols: C20orf13\nGene group: empty\nEnsembl gene ID: ENSG00000089123\nEntrez ID: 55617\nOMIM ID: 608270\nUniProt IDs: Q9H6P5",
  "question": "Does this record have a value for OMIM ID?"
 },
 {
  "qid": "q3c3a510f59",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:5996\nSymbol: IL1RAPL1\nName: interleukin 1 receptor accessory protein like 1\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: Xp21.3-p21.2\nDate approved: 1999-09-07\nAlias symbols: OPHN4, TIGIRR-2, IL1R8, IL1RAPL-1\nPrevious symbols: IL1RAPL, MRX34, MRX21, MRX10\nGene group: I-set domain containing, Interleukin receptors, TIR domain containing, MicroRNA protein coding host genes\nEnsembl gene ID: ENSG00000169306\nEntrez ID: 11141\nOMIM ID: 300206\nUniProt IDs: Q9NZN1",
  "question": "Is this gene located on chromosome X?"
 },
 {
  "qid": "q75ab33b20e",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:23384\nSymbol: ZNF483\nName: zinc finger protein 483\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 9q31.3\nDate approved: 2003-11-14\nAlias symbols: ZKSCAN16, KIAA1962, ZSCAN48\nPrevious symbols: empty\nGene group: Zinc fingers C2H2-type, SCAN domain containing, KRAB domain containing\nEnsembl gene ID: ENSG00000173258\nEntrez ID: 158399\nOMIM ID: empty\nUniProt IDs: Q8TF39",
  "question": "Does this record have a value for alias symbols?"
 },
 {
  "qid": "qbb32ace09f",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:12217\nSymbol: TRBV4-3\nName: T cell receptor beta variable 4-3\nLocus group: other\nLocus type: T cell receptor gene\nChromosomal location: 7q34 alternate reference locus\nDate approved: 2000-05-15\nAlias symbols: TRBV43, TCRBV4S3, TCRBV7S2A1N4T\nPrevious symbols: empty\nGene group: T cell receptor beta locus at 7q34\nEnsembl gene ID: ENSG00000282543\nEntrez ID: 28615\nOMIM ID: empty\nUniProt IDs: A0A589",
  "question": "Was this gene approved after 2005?"
 },
 {
  "qid": "qf394b47ac6",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:14451\nSymbol: LPIN3\nName: lipin 3\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 20q12\nDate approved: 2001-01-24\nAlias symbols: SMP2\nPrevious symbols: LIPN3L\nGene group: Lipins\nEnsembl gene ID: ENSG00000132793\nEntrez ID: 64900\nOMIM ID: 605520\nUniProt IDs: Q9BQK8",
  "question": "Does this record cite an OMIM identifier?",
  "definitions": "- yes: The OMIM ID field is filled.\n- no: The OMIM ID field is empty."
 },
 {
  "qid": "q6af69680ea",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:52755\nSymbol: LINC01932\nName: long independently transcribed non-coding RNA 1932\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 5q33.3\nDate approved: 2016-12-07\nAlias symbols: empty\nPrevious symbols: empty\nGene group: Long independently transcribed non-coding RNAs\nEnsembl gene ID: ENSG00000253315\nEntrez ID: 105377682\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does the symbol start with the letters LINC?",
  "definitions": "- yes: The symbol starts with LINC.\n- no: The symbol starts with other letters."
 },
 {
  "qid": "qfb6283cbda",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:50002\nSymbol: MIR6085\nName: microRNA 6085\nLocus group: non-coding RNA\nLocus type: RNA, micro\nChromosomal location: 15q22.2\nDate approved: 2014-03-24\nAlias symbols: hsa-mir-6085\nPrevious symbols: empty\nGene group: MicroRNAs\nEnsembl gene ID: ENSG00000275451\nEntrez ID: 102464834\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this gene have alias symbols on file?",
  "definitions": "- yes: The alias symbols field is filled.\n- no: The alias symbols field is empty."
 },
 {
  "qid": "q46aa43a690",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:52049\nSymbol: MTCO3P19\nName: MT-CO3 pseudogene 19\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: Xq22.1\nDate approved: 2015-10-19\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000224471\nEntrez ID: 107075156\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does the gene name contain the word kinase?"
 },
 {
  "qid": "q78f813dcff",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:4513\nSymbol: TAAR3P\nName: trace amine associated receptor 3, pseudogene\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 6q23.2\nDate approved: 1999-03-09\nAlias symbols: empty\nPrevious symbols: GPR57, TAAR3\nGene group: Trace amine receptors, Unitary pseudogenes\nEnsembl gene ID: ENSG00000179073\nEntrez ID: 9288\nOMIM ID: empty\nUniProt IDs: Q9P1P4",
  "question": "Is this gene a protein-coding gene?",
  "definitions": "- yes: The locus group is protein-coding gene.\n- no: The locus group is pseudogene, non-coding RNA or other."
 },
 {
  "qid": "q139cfb9bd2",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:39208\nSymbol: KARS1P2\nName: lysyl-tRNA synthetase 1 pseudogene 2\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 13q34\nDate approved: 2010-11-23\nAlias symbols: empty\nPrevious symbols: KARSP2\nGene group: empty\nEnsembl gene ID: ENSG00000230371\nEntrez ID: 100419560\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is this gene located on the short arm (p) of its chromosome?"
 },
 {
  "qid": "qff83049542",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:56180\nSymbol: KMT2CP2\nName: lysine methyltransferase 2C pseudogene 2\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 1q21.1\nDate approved: 2022-01-14\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000276756\nEntrez ID: 125177371\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does the symbol start with the letters LINC?",
  "definitions": "- yes: The symbol starts with LINC.\n- no: The symbol starts with other letters."
 },
 {
  "qid": "q18bcf7bd52",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:18044\nSymbol: SLC38A3\nName: solute carrier family 38 member 3\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 3p21.31\nDate approved: 2002-01-22\nAlias symbols: G17, SN1, SNAT3\nPrevious symbols: empty\nGene group: Solute carrier family 38\nEnsembl gene ID: ENSG00000188338\nEntrez ID: 10991\nOMIM ID: 604437\nUniProt IDs: Q99624",
  "question": "Was this gene approved in 2020 or earlier?"
 },
 {
  "qid": "q19cd5a0f93",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:44688\nSymbol: DPPA5P3\nName: developmental pluripotency associated 5 pseudogene 3\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 10p15.1\nDate approved: 2012-12-04\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: empty\nEntrez ID: 100528006\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this gene have alias symbols on file?",
  "definitions": "- yes: The alias symbols field is filled.\n- no: The alias symbols field is empty."
 },
 {
  "qid": "q1e73234706",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:56804\nSymbol: RPL7L1P22\nName: RPL7L1 pseudogene 22\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 1p22.3\nDate approved: 2023-04-19\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000231349\nEntrez ID: 100420166\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Is this gene ratified after 2005?",
  "definitions": "- yes: The date approved is after 2005.\n- no: The date approved is 2005 or earlier."
 },
 {
  "qid": "q2409bc3752",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:38069\nSymbol: TPI1P2\nName: triosephosphate isomerase 1 pseudogene 2\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 7q32.1\nDate approved: 2010-04-08\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000230359\nEntrez ID: 286016\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this record have a value for OMIM ID?"
 },
 {
  "qid": "qdcb9ecbe0d",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:32151\nSymbol: ATAD3C\nName: ATPase family AAA domain containing 3C\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 1p36.33\nDate approved: 2005-07-15\nAlias symbols: FLJ34599\nPrevious symbols: empty\nGene group: AAA ATPases, Mitochondrial nucleoid associated proteins\nEnsembl gene ID: ENSG00000215915\nEntrez ID: 219293\nOMIM ID: 617227\nUniProt IDs: Q5T2N8",
  "question": "Is this gene a protein-coding gene?",
  "definitions": "- yes: The locus group is protein-coding gene.\n- no: The locus group is pseudogene, non-coding RNA or other."
 },
 {
  "qid": "q48cded099b",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:33189\nSymbol: SNORD3A\nName: small nucleolar RNA, C/D box 3A\nLocus group: non-coding RNA\nLocus type: RNA, small nucleolar\nChromosomal location: 17p11.2\nDate approved: 2006-11-28\nAlias symbols: U3, RNU3\nPrevious symbols: empty\nGene group: Small nucleolar RNAs, C/D box\nEnsembl gene ID: ENSG00000263934\nEntrez ID: 780851\nOMIM ID: 180710\nUniProt IDs: empty",
  "question": "Is this gene located on chromosome 17?"
 },
 {
  "qid": "qe95e6efec0",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:19694\nSymbol: STXBP4\nName: syntaxin binding protein 4\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 17q22\nDate approved: 2004-01-15\nAlias symbols: Synip, MGC50337\nPrevious symbols: empty\nGene group: PDZ domain containing\nEnsembl gene ID: ENSG00000166263\nEntrez ID: 252983\nOMIM ID: 610415\nUniProt IDs: Q6ZWJ1",
  "question": "Does the gene name contain the word protein?"
 },
 {
  "qid": "q1b3522c9c8",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:21652\nSymbol: OSTM1\nName: osteoclastogenesis associated transmembrane protein 1\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 6q21\nDate approved: 2003-10-06\nAlias symbols: HSPC019, GL\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000081087\nEntrez ID: 28962\nOMIM ID: 607649\nUniProt IDs: Q86WC4",
  "question": "Is a gene group redeemed for this gene?",
  "definitions": "- yes: The gene group field is filled.\n- no: The gene group field is empty."
 },
 {
  "qid": "qc018c8340f",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:47070\nSymbol: RNU6-107P\nName: RNA, U6 small nuclear 107, pseudogene\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 2q37.1\nDate approved: 2013-05-01\nAlias symbols: empty\nPrevious symbols: empty\nGene group: empty\nEnsembl gene ID: ENSG00000252452\nEntrez ID: 106479614\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does the gene name contain the word like?"
 },
 {
  "qid": "q0edaf92d81",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:15347\nSymbol: OR11H4\nName: olfactory receptor family 11 subfamily H member 4\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 14q11.2\nDate approved: 2001-03-28\nAlias symbols: empty\nPrevious symbols: empty\nGene group: Olfactory receptors, family 11\nEnsembl gene ID: ENSG00000176198\nEntrez ID: 390442\nOMIM ID: empty\nUniProt IDs: Q8NGC9",
  "question": "Is this gene listed as a protein-coding gene?",
  "definitions": "- yes: The locus group is protein-coding gene.\n- no: The locus group is pseudogene, non-coding RNA or other."
 },
 {
  "qid": "qc9d69d2dce",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:21050\nSymbol: CDKAL1\nName: CDKAL1 threonylcarbamoyladenosine tRNA methylthiotransferase\nLocus group: protein-coding gene\nLocus type: gene with protein product\nChromosomal location: 6p22.3\nDate approved: 2003-05-12\nAlias symbols: FLJ20342\nPrevious symbols: empty\nGene group: Radical S-adenosylmethionine domain containing, DNA/RNA methyltransferases\nEnsembl gene ID: ENSG00000145996\nEntrez ID: 54901\nOMIM ID: 611259\nUniProt IDs: Q5VV42",
  "question": "Is the gene symbol 5 characters or shorter?"
 },
 {
  "qid": "q81d8b955c7",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:42893\nSymbol: RNA5SP95\nName: RNA, 5S ribosomal pseudogene 95\nLocus group: pseudogene\nLocus type: pseudogene\nChromosomal location: 2p16.1\nDate approved: 2011-09-05\nAlias symbols: empty\nPrevious symbols: RN5S95\nGene group: empty\nEnsembl gene ID: ENSG00000222251\nEntrez ID: 100873328\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this record have a value for Ensembl gene ID?"
 },
 {
  "qid": "qb3d0ba2946",
  "kind": "yes/no",
  "text": "HGNC gene record (HGNC complete set).\nHGNC ID: HGNC:27809\nSymbol: TNFRSF10B-AS1\nName: TNFRSF10B antisense RNA 1\nLocus group: non-coding RNA\nLocus type: RNA, long non-coding\nChromosomal location: 8p21.3\nDate approved: 2023-11-29\nAlias symbols: DR5-AS\nPrevious symbols: empty\nGene group: Antisense RNAs\nEnsembl gene ID: ENSG00000246130\nEntrez ID: 286059\nOMIM ID: empty\nUniProt IDs: empty",
  "question": "Does this record show a UniProt identifier?",
  "definitions": "- yes: The UniProt IDs field is filled.\n- no: The UniProt IDs field is empty."
 }
]
