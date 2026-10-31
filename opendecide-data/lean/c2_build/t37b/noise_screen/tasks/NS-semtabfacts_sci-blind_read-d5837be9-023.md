# Replay noise screen blind read NS-semtabfacts_sci-blind_read-d5837be9-023 (family NS-semtabfacts_sci)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-semtabfacts_sci-blind_read-d5837be9-023.json

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
  "qid": "q6fa487c1bc",
  "kind": "yes/no",
  "text": "Table caption: Autoclave cure cycle.\n| Autoclave cure cycle | Flat panel | Mould-in manufacturing |\n| Pressure Ramp Rate | 50 kPa/min | 50 kPa/min |\n| Pressure | 600 kPa | 600 kPa |\n| Temperature Ramp Rate | 3.5 °C/min | 3.5 °C/min |\n| Temperature | 220 °C | 250 °C |\n| Dwell time | 40 min | 50 min |\n\nStatement: The temperature of Mould-in manufacturing is less than Flat panel.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe45c9f82bc",
  "kind": "yes/no",
  "text": "Table caption: Oxide compositions of the binding materials used.\n| Oxide Composition | CaO (%) | SiO 2 (%) | Al 2 O 3 (%) | Fe 2 O 3 (%) | MgO (%) | K 2 O (%) | Na 2 O (%) | SO 3 (%) | TiO 2 (%) | P 2 O 5 (%) | LOI (%) |\n| AONSA PLC | 2.04 64.50 | 65.02 21.55 | 16.28 5.50 | 10.16 3.08 | 1.53 1.52 | 0.52 0.61 | 0.45 – | 1.32 2.03 | 0.01 – | 0.01 – | 2.95 1.20 |\nTable notes: LOI = Loss of Ignition, determined at 800 °C.\n\nStatement: SiO 2 Oxide Composition will have High AONSA.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3e2cd5e5df",
  "kind": "yes/no",
  "text": "Table caption: Alignment score versus mapping quality score.\n| Alignment score a | Mapping quality score b | Interpretation |\n| HIGH | HIGH | Read maps unambiguously and is very similar to reference sequence at that position c |\n| HIGH | LOW | Read is very similar to reference sequence at that position, but maps at several positions |\n| LOW | HIGH | Read maps unambiguously, but aligns with several mismatches to reference sequence at that position c |\n| LOW | LOW | Reads aligns with several mismatches at this and several other positions in the reference sequences |\n\nStatement: Alignment score and mapping quality score are two types of scores given in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0fc5bbd048",
  "kind": "yes/no",
  "text": "Table caption: Values of coded levels used for experimental design in media optimisation of Bacillus aryabhattai KIIT BE-1.\n| Sl. No. | Factors | Symbols | Actual levels of coded values | Actual levels of coded values | Actual levels of coded values | Actual levels of coded values | Actual levels of coded values |\n|  |  |  | Lowest | Low | Centre | High | Highest |\n|  |  |  | −β | −1 | 0 | +1 | +β |\n| 1. | Starch | A | 5.0 | 7.5 | 10 | 12.5 | 15.0 |\n| 2. | Peptone | B | 2.0 | 3.5 | 5.0 | 6.5 | 8.0 |\n| 3. | Yeast extract | C | 3.5 | 5.0 | 6.5 | 8.0 | 9.5 |\n| 4. | pH | D | 3.0 | 5.0 | 7.0 | 9.0 | 11.0 |\n\nStatement: Peptone has the least value of 8.0",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q006a047534",
  "kind": "yes/no",
  "text": "Table caption: Area statistics of targeted landscape in the study site (unit: hectare).\n| Index | Statistics |\n| Road | 0.25111 |\n| Water Channel | 0.05125 |\n| Ancient Building | 0.0307 |\n| Modern Building | 0.0307 |\n| Vegetated Area | 2.542 |\n\nStatement: Ancient Building Statistics is 0.0307.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q75e610ff46",
  "kind": "yes/no",
  "text": "Table caption: The combined and expanded measurement uncertainties for r h,mode (MALS), r h,mode1 (ICP-MS), r h,mode2 (ICP-MS), and mass-based PSD (d 10 , d 50 , d 90 ).\n|  | MALS | ICP-MS | ICP-MS | Mass-based PSD | Mass-based PSD | Mass-based PSD |\n|  | r h,mode | r h,mode1 | r h,mode2 | d 10 | d 50 | d 90 |\n| u c (%) | 12.7 | 8.6 | 9.4 | 10.4 | 35.8 | 52.2 |\n| U (%) | 25.3 | 17.1 | 18.7 | 20.8 | 71.5 | 104.5 |\nTable notes: Combined uncertainty ( u c ), Expanded uncertainty (k = 2): U (%).\n\nStatement: U(%) has highest value in d 90 of 104.5.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8edd23c9ec",
  "kind": "yes/no",
  "text": "Table caption: 3-D printing settings tested on the Cerberus.\n| Basic Printer Settings | Basic Printer Settings |  |  |  |\n| Material | Nozzle Temperature [ o C] | Bed Temperature [ o C] | Layer Height [mm] | Part Cooling Fan |\n| PEKK | 390 | 180 | 0.3 | OFF |\n| PEI/ULTEM | 380 | 170 | 0.3 | OFF |\n| Polycarbonate | 280 | 130 | 0.3 | ON or OFF |\n\nStatement: There are 3 Material used for Basic Printer Settings.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb8d3fdbaf5",
  "kind": "yes/no",
  "text": "Table caption: Bias decomposition of the daily GWR-merged rainfall (in mm), totalized over dry seasons (1 October – 31 May) within 1 January 2015–31 December 2018: P T – gauge accumulated total rainfall; HB - hit bias; AHB - absolute hit bias; MB – miss bias; N AHB – normalized AHB and N MB – normalized MB.\n| Stations | P T = ∑ i= 1 T P g i | CHIRPS | CHIRPS | CHIRPS | MPEG | MPEG | MPEG | CHIRPS | CHIRPS | MPEG | MPEG |\n| Stations | P T = ∑ i= 1 T P g i | HB | AHB | MB | HB | AHB | MB | N AHB | N MB | N AHB | N MB |\n| Adigudem | 287.5 | −0.9 | 5.9 | 0.0 | −0.4 | 4.7 | 0.0 | 0.02 | 0.00 | 0.02 | 0.00 |\n| Debub | 692.4 | 6.1 | 15.3 | −0.7 | 6.2 | 7.2 | 0.0 | 0.02 | 0.00 | 0.01 | 0.00 |\n| Dengolat | 774.7 | −18.3 | 40.9 | −0.3 | −12.1 | 31.2 | 0.0 | 0.05 | 0.00 | 0.04 | 0.00 |\n| Finarawa | 309.4 | 2.9 | 7.2 | 0.0 | 3.9 | 4.9 | 0.0 | 0.02 | 0.00 | 0.02 | 0.00 |\n| Gijet | 555.3 | 8.8 | 54.1 | 0.0 | 5.3 | 44.0 | 0.0 | 0.10 | 0.00 | 0.08 | 0.00 |\n| Hashenge | 1257.8 | −7.9 | 10.5 | 0.0 | −10.5 | 12.4 | 0.0 | 0.01 | 0.00 | 0.01 | 0.00 |\n| Maichew | 1106.4 | 15.4 | 115.9 | −1.8 | 34.1 | 45.3 | 0.0 | 0.10 | 0.00 | 0.04 | 0.00 |\n| Wedisemero | 835.6 | 47.0 | 54.7 | −0.8 | 51.4 | 56.3 | 0.0 | 0.07 | 0.00 | 0.07 | 0.00 |\n| Hiwane | 276.6 | −5.5 | 21.4 | 0.0 | 0.3 | 3.6 | 0.0 | 0.08 | 0.00 | 0.01 | 0.00 |\n| Borra | 299.7 | −19.9 | 37.2 | 0.0 | −15.4 | 34.8 | 0.0 | 0.12 | 0.00 | 0.12 | 0.00 |\n| AVG | 639.5 | 2.8 | 36.3 | −0.4 | 6.3 | 24.4 | 0.0 | 0.06 | 0.00 | 0.04 | 0.00 |\n\nStatement: Station Maichew has the highest value for CHIRPS AHB of 115.9.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q07a3486e89",
  "kind": "yes/no",
  "text": "Table caption: Correlation between cerebral perfusion pressure and brain tissue oxygenation in 5 patients.\n| Patient No | Pearson coefficient (r) of correlation between CPP and PbtO 2 and probability (p) |\n| 1 | 0.79, p < 0.01 |\n| 2 | 0.38, p < 0.01 |\n| 3 | 0.35, p < 0.01 |\n| 4 | 0.77, p < 0.01 |\n| 5 | 0.7, p < 0.01 |\nTable notes: Abbreviations: r – Pearson's correlation coefficient; CPP – cerebral perfusion pressure; PbtO 2 – partial pressure of oxygen in brain tissue.\n\nStatement: Pearson coefficient are < 0.01 for all the patients.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc568daba5a",
  "kind": "yes/no",
  "text": "Table caption: Maximum crack size for the experienced beams.\n| Beam specimen | Reinforcements Ratio (%) | No. of CFRP Layer | Failure load, P exp (kN) | Maximum crack size (mm) | ACI440.1R-06 [ 23 ] (mm) | CEB-F1P Code (mm) |\n| B2−0C | 0.56 a | 0 | 40 | 0.23 | 2 | 0.3 |\n| B3−0C | 0.84 b | 0 | 67.5 | 0.19 | 1.05 | 0.25 |\n| \"B2−1C\" | 0.56 | 1 | 57.5 | 0.52 | 2 | 0.35 |\n| \"B3−1C\" | 0.84 | 1 | 73 | 0.4 | 1.75 | 0.33 |\n| \"B4−1C\" | 1.12 c | 1 | 85 | 0.33 | 0.6 | 0.36 |\n| \"B5−1C\" | 1.4 d | 1 | 96 | 0.16 | 0.43 | 0.28 |\n| \"B2−2C\" | 0.56 | 2 | 78 | 0.6 | 2 | 0.4 |\n| \"B3−2C\" | 0.84 | 2 | 88 | 0.32 | 1.05 | 0.36 |\n| \"B4−2C\" | 1.12 | 2 | 96 | 0.21 | 0.6 | 0.27 |\n| \"B5−2C\" | 1.4 | 2 | 104 | 0.18 | 0.43 | 0.26 |\n\nStatement: The lowest Reinforcements Ratio (%) is 350.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qde73853bcc",
  "kind": "yes/no",
  "text": "Table caption: Comparison of efficiency of our parallel solution and the serial solution (1 k = 1000).\n| Mesh Model | Num. of Node | Num. of Elem. | Serial (/ms) | Serial (/ms) | Parallel (/ms) | Parallel (/ms) | Speedup | Speedup |\n| Mesh Model | Num. of Node | Num. of Elem. | Find Node | Find Elem. | Find Node | Find Elem. | Find Node | Find Elem. |\n| Armadillo | 172 k | 346 k | 2527 | 1732 | 50.0 | 22.1 | 50.5 | 78.4 |\n| Angel | 237 k | 474 k | 3635 | 2580 | 66.7 | 29.4 | 54.5 | 87.8 |\n| Hand | 327 k | 655 k | 4806 | 3305 | 89.1 | 38.3 | 53.9 | 86.3 |\n| Dragon | 437 k | 871 k | 6543 | 4488 | 112.7 | 48.5 | 58.1 | 92.5 |\n| Buddha | 543 k | 1088 k | 8577 | 6072 | 138.5 | 60.6 | 61.9 | 100.2 |\n| Blade | 882 k | 1765 k | 13,931 | 10,000 | 221.3 | 93.3 | 63.0 | 107.2 |\n\nStatement: Armadillo has 346 k elements.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qaa5c06ee20",
  "kind": "yes/no",
  "text": "Table caption: Tree location and perception of traffic, pollution, and temperature.\n| Tree locations (excluding no trees as this was not preferred) | This blocks perception of traffic mean (Std Dev) | This lessens pollution exposure | This make me cooler |\n| Trees between cycle track and street/parked cars | 3.7 (2.3) | 4.1 (2.2) | 4.8 (2.2) |\n| Trees between sidewalk and cycle track | 3.7 (2.3) | 4.4 (2.2) | 5.2 (2.0) |\n| Trees and bushes between cycle track and street/parked cars | 4.7 (2.4) | 5.2 (2.0) | 5.4 (1.9) |\n\nStatement: The table contain 5 Perception.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2e310206c5",
  "kind": "yes/no",
  "text": "Table caption: Baseline characteristics – continuous variables are compared with ANOVA, Time from Diagnosis and Triglycerides by Kruskal Wallis test and gender by chi-square.\n|  | Temporal Phenotype | Temporal Phenotype | Temporal Phenotype | p-value |\n|  | A | B | C | p-value |\n| Total Number of Subjects | 191 | 574 | 159 |  |\n| Gender Male - N(%) | 107 (56 %) | 340 (59.1 %) | 94 (59.1 %) | 0.727 |\n| Age - Mean (SD) | 63.99(12.07) | 64.43(9.99) | 66.18(9) | 0.007 |\n| Time from Diagnosis – Median (IQR) | 4.81(13.1) | 7.1(10.3) | 10.1(10.2) | 0.497 |\n| Hba1c - Mean (SD) | 58.63(16.8) | 55.28(15.61) | 54.99(12.79) | 0.547 |\n| BMI - Mean (SD) | 30.27(6.06) | 29.6(4.94) | 28.8(4.54) | 0.288 |\n| Cholesterol - Mean (SD) | 184.94(36.31) | 185.53(31.56) | 186.96(29.24) | <0.001 |\n| Triglycerides - – Median (IQR) | 139(77.8) | 127(63.3) | 119(51.5) | 0.20 |\n| SBP - Mean (SD) | 131.98 (17) | 132.16 (14.12) | 135.4 (14.04) | 0.008 |\n\nStatement: The table A has the highest Time from Diagnosis .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf4cb850bfb",
  "kind": "yes/no",
  "text": "Table caption: State transition matrix in the simulated data.\n|  | State 1 | State 2 | State 3 | State 4 | State 5 |\n| State 1 | 0.8 | 0.05 | 0.05 | 0.05 | 0.05 |\n| State 2 | 0.1 | 0.8 | 0 | 0.1 | 0 |\n| State 3 | 0.1 | 0 | 0.8 | 0 | 0.1 |\n| State 4 | 0 | 0 | 0 | 1 | 0 |\n| State 5 | 0 | 0 | 0 | 0 | 1 |\n\nStatement: The lowest value of State 5 is 0.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb35e7081a8",
  "kind": "yes/no",
  "text": "Table caption: Chemical composition of the substrate and the wire in weight percent.\n|  | Grade | Al, wt% | Cr, wt% | Cu, wt% | Fe, wt% | Mg, wt% | Mn, wt% | Si, wt% | Zn, wt% | Ti, wt% | Zr, wt% |\n| Substrate | 5056 | 92.9–95.4 | 0.05–0.20 | ≤ 0.10 | ≤ 0.40 | 4.5–5.6 | 0.05–0.20 | ≤ 0.30 | ≤ 0.10 | ≤ 0.05 | ≤ 0.05 |\n| Wire | OK Autrod 18.22 (ESAB) | 92.93 | – | 0.03 | – | 5.8 | 0.8 | 0.06 | – | 0.03 | 0.1 |\n\nStatement: Wire Cu, wt% is 0.03.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q52b82b93e5",
  "kind": "yes/no",
  "text": "Table caption: Structural Equation Modeling statistics and goodness-of-fit for models predicting the response-inhibition factor ( N = 188).\n|  | χ 2 | df | p | CFI | RMSEA [90% CI] | SRMR | DLC intensity path to response inhibition |\n| Model 1 | 32.27 | 33 | 0.50 | 1.00 | 0.00 [0.00, 0.05] | 0.05 | −0.03 [−0.29, 0.32] |\n| Model 2 | 23.91 | 25 | 0.52 | 1.00 | 0.00 [0.00, 0.06] | 0.05 | −0.03 [−0.32, 0.25] |\n| Model 3 | 12.77 | 13 | 0.47 | 1.00 | 0.00 [0.00, 0.07] | 0.04 | −0.04 [−0.29, 0.21] |\n| Model 4 | 5.90 | 8 | 0.66 | 1.00 | 0.00 [0.00, 0.07] | 0.03 | −0.07 [−0.31, 0.18] |\nTable notes: Notes . Model 1 = intelligence, SES and DLC intensity as predictors of response inhibition; Model 2 = SES and DLC intensity as predictors; Model 3 = intelligence and DLC intensity as predictors; Model 4 = DLC intensity as a single predictor; upper and lower CI from a bootstrapping procedure with 10,000 random samples are given in brackets; note that the relationships between DLC intensity and response inhibition were non-significant in all models.\n\nStatement: Model 1 has the highest values for 2 of 33.27 and df of 33.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q883c712698",
  "kind": "yes/no",
  "text": "Table caption: Multilevel estimates for models with other-ratings of job performance as dependent variable (day level).\n|  | Null model | Null model | Null model | Main effects | Main effects | Main effects | Interaction model | Interaction model | Interaction model |\n|  | B | SE | p < | B | SE | p < | B | SE | p < |\n| Intercept | 3.841 | 0.028 | 0.000 | 3.848 | 0.027 | 0.000 | 3.856 | 0.027 | 0.000 |\n| Increasing resources |  |  |  | 0.035 | 0.016 | 0.014 | 0.033 | 0.016 | 0.020 |\n| Increasing challenges |  |  |  | 0.042 | 0.013 | 0.001 | 0.041 | 0.013 | 0.001 |\n| Decreasing demands |  |  |  | −0.065 | 0.014 | 0.000 | −0.067 | 0.014 | 0.000 |\n| Playful work design |  |  |  | 0.068 | 0.013 | 0.000 | 0.075 | 0.013 | 0.000 |\n| Work pressure |  |  |  | 0.037 | 0.012 | 0.001 | 0.040 | 0.012 | 0.000 |\n| Increasing resources × Work pressure |  |  |  |  |  |  | −0.022 | 0.023 | 0.169 |\n| Increasing challenges × Work pressure |  |  |  |  |  |  | −0.048 | 0.019 | 0.006 |\n| Decreasing demands × Work pressure |  |  |  |  |  |  | 0.030 | 0.020 | 0.067 |\n| Playful work design × Work pressure |  |  |  |  |  |  | −0.045 | 0.019 | 0.009 |\n| Variance and SE level 2 (person) (percentage of total variance) | 0.055 (28.9%) | 0.010 |  | 0.050 | 0.015 |  | 0.050 | 0.009 |  |\n| Variance and SE level 1 (day) (percentage of total variance) | 0.135 (71.0%) | 0.004 |  | 0.114 | 0.004 |  | 0.112 | 0.003 |  |\n| −2 Log likelihood | 2104.153 |  |  | 1622.403 |  |  | 1593.247 |  |  |\nTable notes: Note. N = 77 participants and N = 2310 occasions.\n\nStatement: Variance and SE level 1 for Null model B is 0.135 (71.0%) .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q24e715a049",
  "kind": "yes/no",
  "text": "Table caption: 14 machine learning models applied in this study.\n| No. | Algorithm categories | Models | Settings |\n| 1 | Decision trees | Coarse tree | Maximum number of layers = 5 |\n| 2 |  | Medium tree | Maximum number of layers = 20 |\n| 3 | Discriminant analysis | Linear discriminant | Based on a linear classifier |\n| 4 |  | Quadratic discriminant | Based on a quadratic classifier |\n| 5 | Support vector machine (SVM) | Linear SVM | Based on a linear kernel |\n| 6 |  | Quadratic SVM | Based on a quadratic kernel |\n| 7 |  | Cubic SVM | Based on a cubic kernel |\n| 8 | K nearest neighbor (KNN) | Fine KNN | Based on Euclidean distance, number of NN=1 |\n| 9 |  | Medium KNN | Based on Euclidean distance, number of NN=10 |\n| 10 |  | Cos KNN | Based on cosine distance, number of NN=100 |\n| 11 |  | Cubic KNN | Based on Euclidean distance, number of NN=10 |\n| 12 | Ensemble algorithms | Bagged trees | Number of learners =50 Learning rate = 0.1 |\n| 13 |  | Subspace discriminant | Number of learners =30 Subspace dimension = (number of features)/2 |\n| 14 |  | Subspace KNN | Number of learners =30 Subspace dimension = (number of features)/2 |\n\nStatement: K nearest neighbor (KNN) has 4 models.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q09a9feec53",
  "kind": "yes/no",
  "text": "Table caption: Correlations of the trait and trait-specific method factors in the CT-C(M-1) model.\n|  | Trait factors | Trait factors | Trait factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors |\n|  | Self-report | Self-report | Self-report | Teacher report | Teacher report | Teacher report | Mother report | Mother report | Mother report | Father report | Father report | Father report |\n|  | EMO | SOC | ASC | EMO | SOC | ASC | EMO | SOC | ASC | EMO | SOC | ASC |\n| EMO-S |  |  |  |  |  |  |  |  |  |  |  |  |\n| SOC-S | 0.43 ⁎⁎⁎ |  |  |  |  |  |  |  |  |  |  |  |\n| ASC-S | 0.40 ⁎⁎⁎ | 0.38 ⁎⁎⁎ |  |  |  |  |  |  |  |  |  |  |\n| EMO-T | – | 0.18 ⁎⁎⁎ | 0.22 ⁎⁎⁎ |  |  |  |  |  |  |  |  |  |\n| SOC-T | −0.02 | – | 0.11 ⁎ | 0.62 ⁎⁎⁎ |  |  |  |  |  |  |  |  |\n| ASC-T | −0.19 ⁎⁎⁎ | −0.11 ⁎ | – | 0.38 ⁎⁎⁎ | 0.41 ⁎⁎⁎ |  |  |  |  |  |  |  |\n| EMO-M | – | 0.18 ⁎ | 0.14 ⁎ | 0.30 ⁎⁎⁎ | 0.23 ⁎⁎ | 0.22 ⁎⁎ |  |  |  |  |  |  |\n| SOC-M | −0.08 | – | −0.05 | 0.24 ⁎⁎ | 0.45 ⁎⁎⁎ | 0.34 ⁎⁎⁎ | 0.69 ⁎⁎⁎ |  |  |  |  |  |\n| ASC-M | −0.10 | −0.18 ⁎ | – | 0.16 ⁎ | 0.28 ⁎⁎⁎ | 0.58 ⁎⁎⁎ | 0.46 ⁎⁎⁎ | 0.60 ⁎⁎⁎ |  |  |  |  |\n| EMO-F | – | 0.08 | 0.14 ⁎ | 0.28 ⁎⁎⁎ | 0.20 ⁎ | 0.13 | 0.73 ⁎⁎⁎ | 0.55 ⁎⁎⁎ | 0.29 ⁎⁎⁎ |  |  |  |\n| SOC-F | 0.02 | – | −0.06 | 0.23 ⁎⁎ | 0.27 ⁎⁎ | 0.24 ⁎⁎ | 0.47 ⁎⁎⁎ | 0.75 ⁎⁎⁎ | 0.41 ⁎⁎⁎ | 0.71 ⁎⁎⁎ |  |  |\n| ASC-F | −0.12 | −0.06 | – | 0.17 | 0.17 | 0.49 ⁎⁎⁎ | 0.39 ⁎⁎⁎ | 0.44 ⁎⁎⁎ | 0.92 ⁎⁎⁎ | 0.46 ⁎⁎⁎ | 0.54 ⁎⁎⁎ |  |\nTable notes: Note . S = self-report; T = teacher report; M = mother report; F = father report. EMO = emotional inclusion, SOC = social inclusion, ASC = academic self-concept. All parameters set to 0 by definition are represented by a dash.\n\nStatement: Mother report under ASC of EMO-F is 0.25.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q73072ce584",
  "kind": "yes/no",
  "text": "Table caption: Overall centralization measures for some networks of the same node size and the illustratory vessel-network\n| Measure | Degree centralization | Clustering |\n| Graph type |  |  |\n| Star | .83 | .00 |\n| Ring | .00 | .00 |\n| Full | .00 | 1.00 |\n| Tree | .11 | .00 |\n| Vessel | .23 | .47 |\n\nStatement: Clustering of Full Measure Graph type is 7.47.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1039f4e25c",
  "kind": "yes/no",
  "text": "Table caption: Definitions used to classify whether a SSI occurred in the included studies.\n|  | SSI | SSI | Recurrence | Recurrence |\n| Definition of SSI | n | Percent (%) | n | Percent (%) |\n| Not Defined | 45 | 45 | 49 | 92 |\n| Own Criteria | 18 | 18 | 2 | 4 |\n| CDC | 24 | 24 | 1 | 2 |\n| NSQIP | 1 | 1 | 1 | 2 |\n| Asepsis Score | 1 | 1 | - | - |\n| Culture Positive | 10 | 10 | - | - |\nTable notes: Note: CDC: Centres for Disease Control and preventions; NSQIP: National Surgical Quality Improvement Program.\n\nStatement: CDC and NSQIP for Recurrence of n has same value of 1.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q45e7ccb19f",
  "kind": "yes/no",
  "text": "Table caption: Overview of whole genome bisulphite sequencing (WGBS) and RNA-Seq.\n|  | GC1Y | GC3Y |\n| Total WGBS Reads | 17,032.35 Mb | 19,049.74 Mb |\n| Mapping efficiency | 74.9% | 77.3% |\n| mCG_ratio | 78.9% | 78.2% |\n| mCHG_ratio | 0.4% | 0.4% |\n| mCHH_ratio | 0.5% | 0.4% |\n| Read Depth (X) | 37.85 | 42.33 |\n| Conversion Rate | 99.73% | 99.71% |\n| Total RNA-Seq Reads | 353.59 Mb | 358.96 Mb |\n| Total mapped reads | 287.47 Mb (81.3%) | 288.15 Mb (80.3%) |\n| perfect match | 222.33 Mb (62.9%) | 220.38 Mb (61.4%) |\n| Unique match | 265.85 Mb (75.2%) | 261.03 Mb (72.7%) |\n| Total Unmapped Reads | 66.13 Mb (18.7%) | 70.81 Mb (19.7%) |\n\nStatement: A total of 17,032.35 Mb and",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qafab57f2a2",
  "kind": "yes/no",
  "text": "Table caption: Participants' language experience based on self-assessment questionnaires.\n|  | Polish (L1) N = 195 | Polish (L1) N = 195 | Polish (L1) N = 195 | Polish (L1) N = 195 | English (L2) N = 195 | English (L2) N = 195 | English (L2) N = 195 | English (L2) N = 195 | Additional languages (L3-L5) a N = 66 | Additional languages (L3-L5) a N = 66 | Additional languages (L3-L5) a N = 66 | Additional languages (L3-L5) a N = 66 |\n| Statistic | Mean | SD | Min | Max | Mean | SD | Min | Max | Mean | SD | Min | Max |\n| Overall proficiency | 8.90 | 0.48 | 4.25 | 9.00 | 7.84 | 0.87 | 4.50 | 9.00 | 5.55 | 1.84 | 2.00 | 9.00 |\n| Listening | 8.95 | 0.37 | 5 | 9 | 7.89 | 0.88 | 5 | 9 | 5.76 | 1.87 | 2 | 9 |\n| Reading | 8.92 | 0.60 | 2 | 9 | 8.03 | 0.86 | 5 | 9 | 6.05 | 1.87 | 2 | 9 |\n| Speaking | 8.90 | 0.52 | 5 | 9 | 7.78 | 1.11 | 3 | 9 | 5.10 | 2.08 | 1 | 9 |\n| Writing | 8.82 | 0.72 | 3 | 9 | 7.67 | 1.19 | 3 | 9 | 5.29 | 2.07 | 2 | 9 |\n| Age of acquisition b | 0.06 | 0.46 | 0 | 5 | 6.65 | 3.19 | 0 | 26 | 13.79 | 6.02 | 0 | 29 |\n| Age of active use b | 1.16 | 2.09 | 0 | 12 | 11.74 | 5.05 | 0 | 35 | 17.60 | 5.79 | 0 | 37 |\n| % of daily use | 54 | 18 | 4 | 96 | 42 | 18 | 4 | 96 | 11 | 9 | 1 | 39 |\nTable notes: Notes . SD , standard deviation; the self-ratings range for proficiency was from 1 = no knowledge of given language to 9 = native-like proficiency.\n\nStatement: Reading has Mean value of 1.62.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf6a6de2897",
  "kind": "yes/no",
  "text": "Table caption: ANOVA for tool-work interface temperature (T)\n| Source | DF | Seq SS | Contribution | Adj SS | Adj MS | F-Value | P-Value |\n| n | 1 | 15646.8 | 82.45% | 20.7 | 20.69 | 3.01 | 0.105 |\n| f | 1 | 2835.0 | 14.94% | 15.3 | 15.31 | 2.23 | 0.158 |\n| d | 1 | 1.1 | 0.01% | 27.9 | 27.85 | 4.06 | 0.064 |\n| r | 1 | 151.4 | 0.80% | 88.6 | 88.62 | 12.91 | 0.003 |\n| c | 1 | 3.6 | 0.02% | 0.1 | 0.15 | 0.02 | 0.886 |\n| nf | 1 | 189.6 | 1.00% | 67.6 | 67.58 | 9.84 | 0.007 |\n| nd | 1 | 5.1 | 0.03% | 27.8 | 27.80 | 4.05 | 0.064 |\n| nc | 1 | 0.0 | 0.00% | 0.0 | 0.00 | 0.00 | 1.000 |\n| fd | 1 | 48.7 | 0.26% | 48.7 | 48.66 | 7.09 | 0.019 |\n| fc | 1 | 0.0 | 0.00% | 0.0 | 0.00 | 0.00 | 1.000 |\n| dc | 1 | 0.0 | 0.00% | 0.0 | 0.00 | 0.00 | 1.000 |\n| rc | 1 | 0.0 | 0.00% | 0.0 | 0.00 | 0.00 | 1.000 |\n| Error | 14 | 96.1 | 0.51% | 96.1 | 6.87 |  |  |\n| Total | 26 | 18977.4 | 100.00% |  |  |  |  |\n\nStatement: All the values for source fc, dc, nc and rc is 0.00.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7e969fdc53",
  "kind": "yes/no",
  "text": "Table caption: Gender diversity channels: independent vs inside women directors.\n|  | OLS (1) | Lagged OLS (2) | Lagged OLS (3) |\n| Variable | REN/TC | REN/TC | REN/TC |\n| WOB_independence | 1.212*** | 1.212** | 1.350** |\n|  | (2.392) | (2.021) | (2.013) |\n| WOB_insider | 1.132* | 1.489 | 1.468 |\n|  | (1.992) | (1.623) | (1.722) |\n| WCEO | 0.128 | 1.233* | 1.113* |\n|  | (0.413) | (1.923) | (1.919) |\n| Board size | 2.112*** | 2.644* | 2.132* |\n|  | (2.499) | (1.992) | (1.922) |\n| Duality | −2.132* | −2.130* | −2.122* |\n|  | (−1.993) | (−1.992) | (−1.991) |\n| %_Board independence | 2.323** | 1.211** | 1.132** |\n|  | (2.168) | (2.012) | (2.012) |\n| B_meeting | −7.132 | −7.123 | −6.132* |\n|  | (−1.143) | (−1.685) | (−1.891) |\n| Tobin's q | 9.120* | 5.121* | 3.132* |\n|  | (1.969) | (1.935) | (1.892) |\n| ROA | 1.543* | 1.169* | 1.181* |\n|  | (1.992) | (1.883) | (1.963) |\n| Cash/net assets | 1.133 | 3.231 | 3.014 |\n|  | (1.121) | (1.791) | (1.013) |\n| Leverage | −10.126 | −11.122* | −9.122 |\n|  | (−1.197) | (−1.893) | (−1.606) |\n| IO | −0.201 | −0.224 | −0.211* |\n|  | (1.021) | (1.692) | (1.982) |\n| %_Insider owner | 0.299 | −1.321 | −1.149 |\n|  | (1.182) | (1.036) | (1.331) |\n| Firm size | 9.239** | 7.133*** | 7.122** |\n|  | (2.011) | (2.424) | (2.124) |\n| Constant | −11.298** | −17.634* | −11.120** |\n|  | (−2.034) | (−1.961) | (−2.042) |\n| Industry effects | Y | Y | Y |\n| Year effects | Y | Y | Y |\n| N | 11,677 | 9190 | 7950 |\n| Adj. R-sq | 0.181 | 0.176 | 0.191 |\nTable notes: This table presents the results of model 1 where gender diversity is replaced by the percentage of female independent directors ( WOB_independence ) and the percentage of female inside directors ( WOB_insider ). Columns 1–3 present the results from OLS regressions using contemporaneous, two- and three-year lagged levels, respectively. Industry (two-digit GICS) and year effects are included in all the regressions. Robust t -statistics are shown in parentheses. ***, **, * denote statistical significance at the 1%, 5%, and 10% level, respectively. All variables are defined in Table 1 .\n\nStatement: There are 3 Levels OLS(1), Lagged OLS(2) and Lagged OLS(3).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q257b7ac630",
  "kind": "yes/no",
  "text": "Table caption: Generalized Additive Model (GAM) results for effects of nitrogen (logN), phosphorus (logP), temperature (T) and salinity (S) on chlorophyll-a (logChl). The table shows Generalized cross-validation (GCV) score, percentage of variance explained (R 2 , %), and Akaike's Information Criterion (AIC) for the full as well as for reduced models (Eq. (5) ). Only models with all terms statistically significant (p < .05) are shown. The best model is marked bold.\n| Predictor functions | GCV | R 2 | AIC |\n| o ( logN t , logP t ) + p ( T t , S t ) | 0.499 | 37.4% | 300.9 |\n| o ( logN t , logP t ) + u( T t ,) | 0.510 | 32.0% | 304.5 |\n| o ( logN t , logP t ) | 0.556 | 23.6% | 316.8 |\n| p ( T t , S t ) | 0.644 | 14.5% | 337.3 |\n| r( logN t ) + p ( T t , S t ) | 0.513 | 32.6% | 305.2 |\n| s( logP t ) + p ( T t , S t ) | 0.571 | 26.5% | 320.1 |\n\nStatement: There is no value in GCV.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qed6bac78ef",
  "kind": "yes/no",
  "text": "Table caption: Properties of aggregates.\n| Property | Sand | Coarse aggregates |\n| Max. nominal size (mm) | 4.75 | 19.50 |\n| Min. nominal size (mm) | 0.075 | 4.75 |\n| Bulk density (kg/m 3 ) | 1650 | 1578 |\n| Saturated surface dry (SSD) water absorption (%) | 1.40 | 1.51 |\n| 10 % fine value (kN) | – | 157 |\n| Specific gravity | 2.66 | 2.72 |\n\nStatement: 10 % fine value for sand is 2.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4facd8e3a5",
  "kind": "yes/no",
  "text": "Table caption: Results of t -tests between dental microwear texture parameters of moles and bats (all bat species grouped together). † indicates t -tests assuming unequal variances for parameters with unequal variances. Italics highlight apparently significant t -test results that are non-significant after application of the Benjamini-Hochberg procedure to account for type I errors associated with multiple comparisons.\n| ISO texture parameter | d.f. | t | p -value |\n| Sq | 44 | 2.307 | 0.026 |\n| Ssk | 44 | 1.206 | 0.234 |\n| Sku | 44 | 0.720 | 0.476 |\n| Sp † | 29.602 | 1.483 | 0.149 |\n| Sv | 44 | 0.125 | 0.901 |\n| Sz | 44 | 0.775 | 0.443 |\n| Sds | 44 | 1.995 | 0.052 |\n| Str † | 29.514 | 0.942 | 0.354 |\n| Sdq | 44 | 0.503 | 0.618 |\n| Ssc | 44 | 0.894 | 0.376 |\n| Sdr | 44 | 0.517 | 0.608 |\n| Vmp † | 24.198 | 2.299 | 0.030 |\n| Vmc | 44 | 1.999 | 0.052 |\n| Vvc † | 30.374 | 1.805 | 0.081 |\n| Vvv | 44 | 1.311 | 0.197 |\n| Spk † | 24.673 | 2.231 | 0.035 |\n| Sk | 44 | 1.693 | 0.098 |\n| Svk | 44 | 1.097 | 0.279 |\n| Smr1 † | 25.351 | 0.176 | 0.861 |\n| Smr2 | 44 | 0.842 | 0.405 |\n| S5z | 44 | 1.497 | 0.141 |\n| Sa | 44 | 2.186 | 0.034 |\n\nStatement: Vvv Parameter will have highest t value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf86a6c5406",
  "kind": "yes/no",
  "text": "Table caption: Performed tests to determine mechanical Strength of Adobe Samples.\n| Test type | Standard Code | Number of C. samples | Number of E. samples |\n| Compressive Strength/ Cubic 5*5*5 | ASTM C109−90 | 3 | 3 |\n| Flexural strength / 4*4*16 Prismatic | ASTM C293 | 3 | 3 |\n| Tensile Strength / Briquette | ASTM C307 –99 | 3 | 3 |\n\nStatement: There are 3 Same Standard Code for all the Test type.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3a2c9de603",
  "kind": "yes/no",
  "text": "Table caption: Simplified rock physics data of the rock types reviewed in this study. Note permeability data is not available for TB and EHB as this was not an important aim of the Harnett 89 study. In the case of NPS and COS, the anisotropy due to the bedding/fabric produces noticeable permeability anisotropy with typical low (normal to bedding) and high (parallel to bedding) values cited.\n| Property | Etna Basalt (EB) | Stromboli Basalt (SB) | Tenerife Basalt (TB) | El Heirro Basalt (EHB) | Dumaguete Andesite (DA) | Nash Point Shale (NPS) | Crab Orchard Sandstone (COS) |\n| Porosity, % | 2.1 | 6.1 | 12.3 | 1.7 | 6.0 | 6.3 | 7.1 |\n| Initial Permeability (m 2 ) | 10 −16 | 6 × 10 −16 | n/a | n/a | 1.5 × 10 −16 | 10 −18 –10 −21 | 2–33 × 10 −18 |\n| P-wave anisotropy, % | 1.0 | 2.0 | 1.8 | 2.2 | 1.0 | 56.0 | 20.0 |\n\nStatement: Porosity, % of Etna Basalt (EB) has value of 3.7.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q9ce38d6c0a",
  "kind": "yes/no",
  "text": "Table caption: Correlations between HMB and SJ profiles.\n| Date | Correlation Coefficient | P-Value |\n| July 9, 2018 | 0.93 | 0.0 |\n| July 16, 2018 | 0.83 | 0.0 |\n| July 18, 2018 | 0.88 | 0.0 |\n| July 20, 2018 | 0.84 | 0.0 |\n| July 24, 2018 | 0.91 | 0.0 |\n| July 31, 2018 | 0.72 | 0.0 |\n| August 2, 2018 | 0.92 | 0.0 |\n| August 3, 2018 | 0.87 | 0.0 |\n| August 6, 2018 | 0.68 | 0.0 |\n| August 10, 2018 | 0.85 | 0.0 |\n| August 17, 2018 | 0.92 | 0.0 |\n| All dates | 0.79 | 0.0 |\n\nStatement: Correlation Coefficient has the total for all dates of 0.27.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb3b46325ee",
  "kind": "yes/no",
  "text": "Table caption: Main features of the tomato and corn fields characterized by personal contact with local farmers in the 2018 and 2019 growing seasons ( Fig. 9 A–C), with respective estimated IW.\n| Crop type | Year | N. fields | Sowing | Transplanting | Harvesting | Estimated IW (mm) |\n| Early tomato | 2018 | 3 |  | End of April | Beginning of August | 226 |\n| Late tomato | 2018 | 6 |  | Beginning of June | Beginning of September | 308 |\n| Early tomato | 2019 | 5 |  | End of April | Mid-August | 314 |\n| Late tomato | 2019 | 5 |  | End of May | Beginning of September | 289 |\n| Early corn | 2018 | 4 | Mid-April |  | End of August | 397 |\n| Late corn | 2018 | 6 | Mid-June |  | Beginning of October | 339 |\n\nStatement: Early corn has highest estimated IW (mm).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q93b36bd77d",
  "kind": "yes/no",
  "text": "Table caption: Microstructural parameters of phases present obtained from Rietveld refinement using MAUD software [ ].\n|  | β Ti-based | γ Ti-based | ZrO 2 Y 2 O 3 |\n| <D>, nm | 7 | 3 | 48 |\n| <ε 2 > 1/2 | 0.0151 | 0.0054 | 0.0269 |\n| wt.% | 38 | 47 | 1.5 |\n\nStatement: All the values in the given table are the same.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q91d9e6bf04",
  "kind": "yes/no",
  "text": "Table caption: Parameter Estimates of Latent Class Model for Taiwanese Respondents\n| Taiwan (n = 333) | Latent Class 3-Classes | Latent Class 3-Classes | Latent Class 3-Classes | Latent Class 3-Classes |\n| Variables | Class 1 | Class 2 | Class 3 |  |\n|  | Middle Group | Majority Group | Minority Group |  |\n| Labeling product origin | -2.255*** | 1.861*** | 0.287 |  |\n| Food safety certification | -0.680*** | 2.690*** | 1.384*** |  |\n| High quality appearance | -0.810*** | 0.421*** | 0.795*** |  |\n| Domestic rarity | -3.793*** | -1.122*** | 1.287*** |  |\n| Plantation methods | -3.232*** | 0.696*** | -0.299 |  |\n| Freshness | 0.315* | 1.894*** | 1.134*** |  |\n| Probability Class | 0.254 | 0.611 |  | 0.134 |\nTable notes: Notes: 1) *, **, and *** indicate statistically significant at 10%, 5%, and 1% levels, respectively. 2) The scores of price are 0 as the baseline in the model estimation.\n\nStatement: They have 3 class of Latent.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q69f9ba0c8e",
  "kind": "yes/no",
  "text": "Table caption: Random vectors of R implementation of Monte Carlo simulation.\n| Vector name | Value range | Created by function | Used by function | Comment |\n| rbr | 0 – r b * | Setup | Launch | Launch position polar coordinate, radius in light beam |\n| rba | 0 – 2π | Setup | Launch | Launch position polar coordinate, angle |\n| rmv | 0 – 1 | Randomize | Move | Length of straight segment of trajectory |\n| rabs | 0 – 1 | Randomize | Absorb | Photon survival decision is made after interaction |\n| rx1, rx2 | −1 – +1 | Randomize | Scatter | New direction coordinates after scattering |\n| rmu | 0 – 1 | Randomize | Scatter | Anisotropic scattering by Henyey-Greenstein function |\nTable notes: * r b is the radius of light beam.\n\nStatement: Vector rbr has value range of 0 r b *.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2a5b040450",
  "kind": "yes/no",
  "text": "Table caption: The importance of the first 5 principal components (PC) from the principal component analysis (PCA) for the biotic and abiotic factors.\n|  | PC1 | PC2 | PC3 | PC4 | PC5 |\n| Standard deviation | 1.95 | 1.85 | 1.60 | 1.30 | 1.17 |\n| Proportion of Variance | 0.24 | 0.21 | 0.16 | 0.10 | 0.09 |\n| Cumulative Proportion | 0.24 | 0.45 | 0.61 | 0.71 | 0.80 |\n\nStatement: There are 3 types of categories in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q15bcb4d38b",
  "kind": "yes/no",
  "text": "Table caption: Free-stream velocities and Reynolds numbers.\n| Case | U ∞ [ m s - 1 ] | Re |  |  |  |\n| I, III | 1.44 | 9.66 × 10 3 |  |  |  |\n| I, III | 2.46 | 1.65 × 10 4 |  |  |  |\n| I, III | 3.56 | 2.39 × 10 4 |  |  |  |\n| I, III | 4.56 | 3.06 × 10 4 |  |  |  |\n| III | 5.06 | 3.39 × 10 4 |  |  |  |\n| I | 5.37 | 3.60 × 10 4 |  |  |  |\n\nStatement: There are six different Cases.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdac5def8d0",
  "kind": "yes/no",
  "text": "Table caption: Mix proportions of concrete.\n| Mix | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 | Component consumption, kg/m 3 |\n| Mix | CEM I 42,5 R | CEM I 32,5 R | Granite dust | Sand | Coarse aggregate (granite, fraction) | Coarse aggregate (granite, fraction) | Coarse aggregate (granite, fraction) | SP | Water |\n| Mix | CEM I 42,5 R | CEM I 32,5 R | Granite dust | Sand | 6−8 mm | 8−11 mm | 11−16 mm | SP | Water |\n| 42,5-G0 | 350 | – | 0 | 730 | 400 | 400 | 400 | 3,5 | 180 |\n| 32,5-G0 | – | 350 | 0 | 730 | 400 | 400 | 400 | 3,5 | 180 |\n| 42,5-G200 | 350 | – | 200 | 530 | 400 | 400 | 400 | 3,5 | 180 |\n| 32,5-G200 | – | 350 | 200 | 530 | 400 | 400 | 400 | 3,5 | 180 |\n| 42,5-G300 | 350 | – | 300 | 430 | 400 | 400 | 400 | 3,5 | 180 |\n| 32,5-G300 | – | 350 | 300 | 430 | 400 | 400 | 400 | 3,5 | 180 |\n\nStatement: CEM I 42,5 R for mix 32,5-G200 is 200.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q22246a9058",
  "kind": "yes/no",
  "text": "Table caption: Descriptions of variables in the geolocation_data worksheet\n| No | Name | Description | Code | Measure | Unit | Source |\n| 1 | Identity | Unique ID to each irrigation network component. The ID is the official nomenclature from Klambu Wilalung Irrigation District. | ID |  |  | Official data |\n| 2 | Name | The name of each irrigation network component | name |  |  | Official data |\n| 3 | Type a | The type of component in the irrigation network (1=structure, 2=canal) | type | Nominal |  | Official data |\n| 4 | Status | The status of irrigation network components. For structures (1=main structures, 2=supporting structures). For canals (1=primary canal, 2=secondary canal). | stat | Nominal |  | Official data |\n| 5 | X Coordinate b | The Easting coordinate in UTM Projection System | X |  |  | Official data |\n| 6 | Y Coordinate b | The Northing coordinate in UTM Projection System | Y |  |  | Official data |\n| 7 | WUA | The WUA for which each irrigation network components situated |  |  |  | Enumeration |\n| 8 | Village | The village for which each irrigation network components situated |  |  |  | Enumeration |\nTable notes: Note:\n\nStatement: WUA and Village has a enumeration source.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc9966bc2c6",
  "kind": "yes/no",
  "text": "Table caption: Granulometric properties of the soils (mass %).\n| Clay | Silt | Sand | Gravel | Rubble | Name of mine |\n| 37.9 | 51.9 | 9.9 | 0.3 | – | S E |\n| 31.4 | 55.8 | 12.8 | – | – | S M |\n| 34.7 | 60.7 | 4.6 | – | – | S H |\n| 29 | 57.4 | 9.3 | 4.2 | – | S GH |\n| 10 | 79.7 | 10.1 | 0.1 | – | S A |\n| 35.6 | 52.5 | 11.8 | 0.1 | – | S Z |\n\nStatement: Name of mine contain 6 categories such as SE,SM,SH,SGH,SA,SZ.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q967e67f637",
  "kind": "yes/no",
  "text": "Table caption: Descriptive statistics of people's trustworthiness.\n| Items | Obs. | Mean | S.D. | Min. | Max. |\n| Scientists | 531 | 8.10 | 1.98 | 0 | 10 |\n| Government | 530 | 6.16 | 2.61 | 0 | 10 |\n| Politicians | 530 | 3.87 | 2.68 | 0 | 10 |\n| People I know | 529 | 5.39 | 2.68 | 0 | 10 |\n| Traditional news (TV, newspaper, radio) | 530 | 5.59 | 2.74 | 0 | 10 |\n| Facebook | 526 | 4.35 | 2.91 | 0 | 10 |\n| Twitter | 526 | 4.71 | 3.02 | 0 | 10 |\n| YouTube | 525 | 4.35 | 2.88 | 0 | 10 |\nTable notes: Note: The respondents could skip questions they did not want to answer. Therefore, the number of observations varies for each question.\n\nStatement: Min statistics of all items is 0.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2ce7fc296f",
  "kind": "yes/no",
  "text": "Table caption: The average daily profit (euro) of the last month of providing FCR\n|  |  | FCR-N | FCR-D | D + N |\n| Proposed Method | Absolute | 3.846 | 9.452 | 10.99 |\n|  | Per events | 0.057 | 0.148 | 0.170 |\n|  | Per kWh | 0.006 | 0.017 | 0.019 |\n| Ideal Estimate | Absolute | 5.608 | 16.48 | 17.09 |\n|  | Per events | 0.080 | 0.238 | 0.247 |\n|  | Per kWh | 0.009 | 0.027 | 0.028 |\n\nStatement: There are 2 scenarios in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd80aaf78af",
  "kind": "yes/no",
  "text": "Table caption: Pair-wise comparison scale.\n| Intensity of Importance | Definition |\n| 1 | Equal importance of both elements |\n| 3 | Weak importance of one element over another |\n| 5 | Essential or strong importance of one element over another |\n| 7 | Demonstrated importance of one element over another |\n| 9 | Absolute importance of one element over another |\n| 2,4,6,8 | Intermediate values between two adjacent judgments |\n\nStatement: Intensity of Importance of 1 definition is Equal importance of both elements.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qbda15750f3",
  "kind": "yes/no",
  "text": "Table caption: The categories and their conditions.\n| Category | More likely to be salient | Less likely to be salient |\n| Loudness | Word intensity of 80 dB | Word intensity of 60 dB |\n| Acoustic Prominence | /t/pronounced as [p] | /t/pronounced as [t] |\n| Grammatical Gender | Violation of grammatical gender | Correct grammatical gender |\n| Frequency | High frequency word | Low frequency word |\n| Conscious Sound Change | /r/pronounced as [ɹ] | /r/pronounced as [r] |\n| Subconscious Sound Change | /v/pronounced as [v] (=voiced) | /v/pronounced as [f] (=voiceless) |\n\nStatement: More likely to be salient for Grammatical Gender is Violation of grammatical gender.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q278f8c4b43",
  "kind": "yes/no",
  "text": "Table caption: Agricultural characteristics of communes grouped by the share of farms who made investments co-financed under “Modernization of agricultural holdings” and “Setting up of young farmers” programs.\n| Communes grouped by the share of farms who made investments co-financed under “Modernization…” and “Setting up…” programs | Quality index of agricultural production space (score) | Share of farms with an area of over 10 ha (total farms in the commune = 100) |\n| 0−2.25% | 60.5 | 18.0 |\n| 2.26−6.01% | 64.6 | 38.9 |\n| 6.02−10.26% | 65.7 | 52.3 |\n| 10.27−16.67% | 68.2 | 60.7 |\n| 16.68−57.52% | 70.2 | 70.1 |\n| Total | 65.8 | 45.8 |\nTable notes: Source: own calculations based on www.stat.gov.pl and on unpublished data of the Agency for Restructuring and Modernization of Agriculture.\n\nStatement: 18.0 is the total for Quality index of agricultural production space (score)",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q72cfa4b000",
  "kind": "yes/no",
  "text": "Table caption: Model inputs: ε ˙ d is the dynamic strain rate; DIF m and DIF f,i are the dynamic increase factors of the matrix toughness and the equivalent bond stress in the i th layer; E m,s,i is the absorbed energy of the UHPC matrix in the i th layer under static bending; τ f,s is the equivalent bond stress under static pullout; w h is the crack width at the beam bottom.\n|  | ε ˙ d (s −1 ) | DIF m | DIF f ,1 | DIF f ,2 | E m,s ,1 (N m) | E m,s ,2 (N m) | τ f,s (MPa) | w h (mm) |\n| U1.2 s | 66.60 | 2.31 | 2.29 | - | 2.37 | - | 6.2 | 7.64 |\n| U1.2 h | 60.72 | 2.30 | 1.62 | - | 2.37 | - | 10.1 | 16.04 |\n| U0.6 h –1.6 h | 66.11 | 2.31 | 1.64 | 1.67 | 0.95 | 1.42 | 10.1 | 15.29 |\n\nStatement: Table consists of 3 scenarios.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q59928975c7",
  "kind": "yes/no",
  "text": "Table caption: Underwater video observations of fish escaped and transited through the grid system for flounder (mainly winter flounder, Pseudopleuronectes americanus ), Atlantic cod ( Gadus morhua ) and haddock ( Melanogrammus aeglefinus ). Codend escape rate is not provided as more flounders were retained than that observed transiting to the codend, presumably some of flounders entering the codend were not recorded in video.\n|  | Flounders | Atlantic cod | Haddock |\n| Total number observed | 425 | 799 | 7512 |\n| Number exiting grid | 75 | 76 | 3559 |\n| Number re-enter grid | 6 | 26 | 952 |\n| Total number of grid escapes | 69 | 50 | 2607 |\n| Number transited to codend | 356 | 749 | 4905 |\n| Number observed in the catch | 401 | 544 | 206 |\n| % escape through grid | 16.2% | 6.3% | 34.7% |\n| % escape through codend | – | 27.3% | 95.8% |\n\nStatement: Flounders value for % escape through grid is 11.2%.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q654afb530d",
  "kind": "yes/no",
  "text": "Table caption: Relative errors in the solution of Example 3.\n| x | N = 10 | N = 20 | N = 30 | N = 40 | N = 50 |\n| 0.1 | 8.67 × 10 - 5 | 3.68 × 10 - 4 | 1.58 × 10 - 4 | 6.25 × 10 - 5 | 1.01 × 10 - 6 |\n| 0.3 | 1.67 × 10 - 4 | 2.53 × 10 - 4 | 3.57 × 10 - 5 | 7.04 × 10 - 5 | 3.69 × 10 - 5 |\n| 0.5 | 1.26 × 10 - 3 | 7.68 × 10 - 5 | 8.63 × 10 - 6 | 1.35 × 10 - 6 | 2.62 × 10 - 7 |\n| 0.7 | 3.12 × 10 - 3 | 2.87 × 10 - 5 | 4.68 × 10 - 5 | 5.33 × 10 - 5 | 2.72 × 10 - 5 |\n| 0.9 | 6.01 × 10 - 3 | 5.05 × 10 - 4 | 2.84 × 10 - 5 | 3.54 × 10 - 5 | 1.73 × 10 - 6 |\n\nStatement: Here x=0.5 has low value of N = 10 that is 1.26 o 10 - 3.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q30207bed28",
  "kind": "yes/no",
  "text": "Table caption: Compound Dosage for rheology testing A/S/R and A/H/S/R.\n| % A/S/R | 7 R 3 | 7 R 4.5 | 7 R 6 | 7.5 R 3 | 7.5 R 4.5 | 7.5 R 6 | 8 R 3 | 8 R 4.5 | 8 R 6 |\n| A 50/70 | 70.0 | 60.9 | 53.8 | 71.4 | 62.5 | 55.6 | 72.7 | 64.0 | 57.1 |\n| R | 11.2 | 14.4 | 16.6 | 10.6 | 13.4 | 16.0 | 10.6 | 14.8 | 16.3 |\n| S | 18.8 | 24.7 | 29.6 | 18.0 | 24.1 | 28.4 | 16.7 | 21.2 | 26.6 |\n| % A/H/S/R | 7 R 3 | 7 R 4.5 | 7 R 6 | 7.5 R 3 | 7.5 R 4.5 | 7.5 R 6 | 8 R 3 | 8 R 4.5 | 8 R 6 |\n| A 50/70 | 70.0 | 60.9 | 53.8 | 71.4 | 62.5 | 55.6 | 72.7 | 64.0 | 57.1 |\n| H | 6.3 | 8.2 | 9.7 | 6.0 | 7.9 | 9.4 | 5.7 | 7.6 | 9.0 |\n| R | 7.9 | 10.3 | 12.1 | 7.5 | 9.9 | 11.7 | 7.2 | 9.5 | 11.3 |\n| S | 15.8 | 20.6 | 24.3 | 15.0 | 19.7 | 23.4 | 14.4 | 18.9 | 22.6 |\n\nStatement: The least value of S (A/H/S/R) is 14.4 under 8 R 13",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3a4958a096",
  "kind": "yes/no",
  "text": "Table caption: Mean, SD, and discriminant validity evaluation based on Fornell-Larcker criterion.\n| Construct | M | SD | III | CII | IO | EE |\n| III | 4.521 | 1.592 | 0.880 |  |  |  |\n| CII | 4.613 | 1.533 | 0.551 | 0.935 |  |  |\n| IO | 4.251 | 1.593 | 0.663 | 0.640 | 0.861 |  |\n| EE | 4.773 | 1.517 | 0.382 | 0.329 | 0.492 | 0.909 |\nTable notes: Note : Diagonal elements (bold) are the square root of AVE for each construct. Off-diagonal elements are the correlations between constructs.\n\nStatement: There are 5 different of mean in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 }
]
