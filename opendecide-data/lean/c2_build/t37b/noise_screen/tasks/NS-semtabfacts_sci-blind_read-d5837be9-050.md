# Replay noise screen blind read NS-semtabfacts_sci-blind_read-d5837be9-050 (family NS-semtabfacts_sci)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-semtabfacts_sci-blind_read-d5837be9-050.json

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
  "qid": "q2032884d34",
  "kind": "yes/no",
  "text": "Table caption: Operation conditions for Mg and Sr isotope determination with the Plasma II MC-ICP-MS (Nu Instruments).\n| Parameter | Running conditions | Running conditions |\n| Analyte | Mg | Sr |\n| RF power | 1300 | 1300 |\n| Plasma mode | Dry mode, DSN 100 | Wet mode |\n| Auxiliary gas | 0.85–0.9 min −1 | 0.85–0.95 l min −1 |\n| Spray chamber temperature (Peltier) | 5 °C | 5 °C |\n| Nebulizer flow rate | 0.1 ml min −1 | 0.1 ml min −1 |\n| Nebulizer type | MicroMist concentric pyrex nebulizer (GlassExpansion) |  |\n| Cone + skimmer | Ni | Ni |\n\nStatement: Plasma mode for Mg is Wet mode.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd944a2ab37",
  "kind": "yes/no",
  "text": "Table caption: Unit cost and carbon footprint of raw materials (excluding transportation impact).\n| Raw material | Unit costs of raw materials (PKR/kg) | Carbon footprint (kg-CO 2 /kg) |\n| Cement | 14 [ 21 ] | 0.898 [ 38 ] |\n| Fly ash | 5.5 [ 21 ] | 0.004 [ 38 ] |\n| Sand | 0.92 [ 21 ] | 0.002 [ 38 ] |\n| Coarse Aggregate | 0.72 [ 21 ] | 0.053 [ 38 ] |\n| Plasticizer | 210 [ 21 ] | 0.002 [ 38 ] |\n| Water | 0.15 [ 21 ] | 0 |\n| Na 2 SO 4 | 60 * | 0.47 ** |\nTable notes: PKR: Pakistani Rupee.\n\nStatement: 0.47/kg is the least carbon footprint recorded in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6ab849ace7",
  "kind": "yes/no",
  "text": "Table caption: Peaks positions and their FWHM values for constituent elements of CCTS nanoparticles synthesized with 2.50 mmol Cu (C1). ΔE (eV) denotes the difference between peak1 and peak2.\n|  | Cu | Cu | Co | Co | Sn | Sn | S | S |\n|  | Position | FWHM | Position | FWHM | Position | FWHM | Position | FWHM |\n| Peak1(eV) | 931.748 | 1.354 | 778.770 | 1.175 | 486.056 | 1.105 | 161.232 | 0.793 |\n| Peak2(eV) | 951.624 | 2.501 | 793.408 | 1.566 | 494.491 | 1.130 | 162.304 | 2.234 |\n| Peak3(eV) | 946.660 | 4.062 | 779.113 | 4.283 | 487.010 | 1.310 | 164.361 | 1.687 |\n| Peak4(eV) |  |  | 795.220 | 2.523 | 495.514 | 1.312 |  |  |\n| ΔE (eV) | 19.86 |  | 14.70 |  | 8.43 |  | 1.072 |  |\n\nStatement: Cu, Co, Sn and S are four elements given with their position and FWHM values.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe18bf4e486",
  "kind": "yes/no",
  "text": "Table caption: Indicators used in the manually annotated dataset.\n| Constitutional types | Clinical imaging examination | Laboratory indicators |\n| Yin-yang harmony (平和质) | ECG (electrocardiogram) | Blood routine |\n| Qi asthenia (气虚质) | Heart ultrasound | Urine routine |\n| Yang asthenia (阳虚质) | Head magnetic resonance | Stool routine |\n| Yin asthenia (阴虚质) | Chest CT (computed tomography) scan | Liver Function |\n| Phlegm-dampness (痰湿质) | Abdominal ultrasound exam (liver, gallbladder, spleen, and pancreas) | Renal function |\n| Blood stasis (血瘀质) | Renal ultrasound (kidneys, ureters, and bladder) | Blood Lipid |\n| Dampness-heat (湿热质) | Thyroid ultrasound | B-type natriuretic peptide |\n| Qi stagnation (气郁质) | Color doppler ultrasonography of the abdominal aorta (portal vein, the caudal vena cava, and their main abdominal branches and tributaries) | C-reactive protein |\n| Special temperament (特禀质) | Venous ultrasound (lower extremity arteriovenous) | Erythrocyte sedimentation rate |\n|  | Carotid ultrasound | Blood electrolyte |\n|  |  | Carcinoembryonic antigen |\n|  |  | Thyroid function |\n|  |  | 25 hydroxyvitamin D |\n|  |  | β -CTX |\n|  |  | Serum osteocalcin |\n|  |  | C-terminal (P1CP) propeptides of Type I collagen |\n|  |  | Thyroid peroxidase antibody |\n|  |  | Bone-derived alkaline phosphatase |\n|  |  | Glycated haemoglobin (HbA1c) |\n|  |  | Procalcitonin |\n\nStatement: There are nine constitutional types given.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3fb23a9c31",
  "kind": "yes/no",
  "text": "Table caption: Experimental parameters showing starting material and extrusion temperature of material A, B and C. The encapsulated powder was extruded with a force of 257 kN after preheating at 700°C for 20 min.\n| Material | Starting material | Extrusion temperature /°C |\n| A | Crushed powder (< 250 μm) | 650 |\n| B | Milled powder (89 wt .% 20-60 μm) | 650 |\n| C | Milled powder (89 wt .% 20-60 μm) | 700 |\n\nStatement: Material C is having 650 Extrusion temperature /C.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q57d4a99516",
  "kind": "yes/no",
  "text": "Table caption: Summary of the microannuli geometry cases.\n| Case # | Geometry | Description |\n| Case 1 | Experimental | Partial microannulus |\n| Case 2 | Experimental | Nearly complete microannulus |\n| Case 3 | Theoretical | Uniform aperture of 50 μm |\n| Case 4 | Theoretical | Uniform aperture of 350 μm |\n| Case 5 | Theoretical | Uniform aperture of 750 μm |\n\nStatement: There are five types of Geometry.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qbfa76f48d6",
  "kind": "yes/no",
  "text": "Table caption: Underwater video observations of fish escaped and transited through the grid system for flounder (mainly winter flounder, Pseudopleuronectes americanus ), Atlantic cod ( Gadus morhua ) and haddock ( Melanogrammus aeglefinus ). Codend escape rate is not provided as more flounders were retained than that observed transiting to the codend, presumably some of flounders entering the codend were not recorded in video.\n|  | Flounders | Atlantic cod | Haddock |\n| Total number observed | 425 | 799 | 7512 |\n| Number exiting grid | 75 | 76 | 3559 |\n| Number re-enter grid | 6 | 26 | 952 |\n| Total number of grid escapes | 69 | 50 | 2607 |\n| Number transited to codend | 356 | 749 | 4905 |\n| Number observed in the catch | 401 | 544 | 206 |\n| % escape through grid | 16.2% | 6.3% | 34.7% |\n| % escape through codend | – | 27.3% | 95.8% |\n\nStatement: Flounders value for Total number observed is 125.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6739742270",
  "kind": "yes/no",
  "text": "Table caption: QAP correlations.\n|  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |\n| 1. Similarity in cobranding (SCB) |  |  |  |  |  |  |  |  |  |\n| 2. SCB 2 | –.555** |  |  |  |  |  |  |  |  |\n| 3. Total cobranding | .478** | –.207** |  |  |  |  |  |  |  |\n| 4. Decreasing network distance (DND) | .140** | –.073 | .316** |  |  |  |  |  |  |\n| 5. DND 2 | –.051 | .066* | –.127** | –.008 |  |  |  |  |  |\n| 6. Difference in closeness (DCL) | –.195** | .198** | .138* | .012 | –.073** |  |  |  |  |\n| 7. Structural equivalence | .047 | –.021 | .056* | .620** | .250** | –.061** |  |  |  |\n| 8. Same destination dummy | .001 | .059** | .001 | .459** | .248** | .013 | .804** |  |  |\n| 9. Combined closeness (CCL) | .195** | –.047 | .519** | .566** | –.147** | .154* | .118** | .038 |  |\n| 10. CCL × DCL | .084* | .021 | .127* | –.015 | .302** | –.075 | –.041 | –.021 | .140** |\nTable notes: The number of dyads is 990, *p < .10, **p < .05, conservative two-tailed tests.\n\nStatement: The lowest 3 correlation is 0.001.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd0a4221569",
  "kind": "yes/no",
  "text": "Table caption: Reasons teens were unwilling or uncertain about allowing researchers to contact their parents for consent purposes ( N = 166).\n| Theme | N (%) | Example responses |\n| Teen privacy | 55 (33) | ● “They don't know about my problem and I want to keep it that way.” ● “I'm not open about my issues with my parents” |\n| Parents lack an understanding of mental health or are unaware of the problem | 38 (23) | ● “I am not sure they would approve, seeing as they don't necessarily believe in mental health problems. Also, mental health is stigmatized in my family.” ● “They don't know about my eating disorder” |\n| Teen is concerned about parents' reaction/response | 34 (20) | ● “I don't want them to worry more about me” ● “They would be concerned/annoyed that I've never talked to them about this before” |\n| Teen autonomy | 26 (16) | ● “I do not like or trust my parents and I don't want them involved in this” ● “I feel old enough to make my own decisions about apps I'd like to try out” |\n| Poor parent-teen relationship | 17 (10) | ● “My family would never let me get help. A lot of parents don't care about whether their kid is hurting or not. This won't work if you make people tell their families. It just won't”. ● “My parents can be judgmental at some points so I don't want them to tell me something about wanting to try something new”. |\n| Parent would not want the teen to participate in research | 13 (8) | ● “They might think it's a scam and say no” ● “My parents might not be open to me participating in such a study or understanding of how I might benefit from such an app” |\n| Fears about online security/privacy | 3 (2) | ● “I am not sure that this survey is really trustworthy or that they would want me taking it” ● “I do not know what kind of information they will be collecting, so I am undecided” |\n\nStatement: Fears about online security/privacy has the least N (%) value of 3 (2).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q10b0c93f63",
  "kind": "yes/no",
  "text": "Table caption: Properties of Steel Fiber.\n| Materials | Specific Gravity | Shape | Length (mm) | Section (mm) | Aspect Ratio (l/d) | Tensile Strength (N/ mm 2 ) |\n| Steel | 7.8 | Hooked End | 35 | dia.- 0.55 | 64 | 1000 |\n\nStatement: Steel Specific Gravity is 7.8.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6ab287729e",
  "kind": "yes/no",
  "text": "Table caption: Summarizing comparison between the hexachloroiridate and hexacyanoferrate redox couple.\n|  | Hexachloroiridate | Hexacyanoferrate |\n| Reaction | IrCl 6 3− ⇌ IrCl 6 2− + e − | Fe(CN) 6 4− ⇌ Fe(CN) 6 3− + e − |\n| Redox potential | +0.8665 V /SHE [ 4 ] | +0.358 V /SHE [ 4 ] |\n| Reduction plateau (Pt) | +0.75 V /SHE to −0.25 V /SHE | +0.2 V /SHE to −0.6 V /SHE |\n| Oxidation plateau (Pt) | +0.95 V /SHE to +1.1 V /SHE | +0.5 V /SHE to +1.1 V /SHE |\n| Diffusion coefficient | 8.38 * 10 −10 m 2 /s | 6.09 * 10 −10 m 2 /s |\n| Solution pH | pH < 5 | Avoid strong acids |\n| Stability in solution: | A few days to weeks [ 18 ] | Refresh daily [ 12 ] |\n| Stability during reduction (RDE) | 39.2% loss after 16 h | 19.5% loss after 16 h |\n| Loss of concentration due to: | Spontaneous reduction Hydroxide formation | Electrode poisoning Photosensitivity |\n| UV-VIS Extinction coefficient | 4.06 mM −1 cm −1 at 488 nm | 1.064 mM −1 cm −1 at 420 nm |\n\nStatement: Stability during reduction (RDE) does not have PH value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q9969c0c99e",
  "kind": "yes/no",
  "text": "Table caption: Spearman correlations (r) between trabecular and cortical microarchitecture parameters (determined by MRI) and bone turnover markers.\n| MRI parameter | ALP | PTH |\n| S/C | 0.34 | 0.23 |\n| EI | −0.32 | −0.12 |\n| BV/TV (%) | 0.5 ⁎ | 0.27 |\n| TbTh (mm) | 0.5 ⁎ | 0.32 |\n| TbN (1/mm) | 0.44 | 0.22 |\n| TbS (mm) | −0.44 | −0.22 |\n| CTh (mm) | 0.1 | 0.46 ⁎ |\nTable notes: Abbreviations: S/C, surface to curve ratio; EI, erosion index; BV/TV (%), trabecular bone volume; TbTh (mm), trabecular thickness; TbN (1/mm), trabecular number; TbS (mm), trabecular separation; CTh (mm), cortical thickness.\n\nStatement: There are 9 types of different MRI parameter.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q05b8b37286",
  "kind": "yes/no",
  "text": "Table caption: The importance of the first 5 principal components (PC) from the principal component analysis (PCA) for the biotic and abiotic factors.\n|  | PC1 | PC2 | PC3 | PC4 | PC5 |\n| Standard deviation | 1.95 | 1.85 | 1.60 | 1.30 | 1.17 |\n| Proportion of Variance | 0.24 | 0.21 | 0.16 | 0.10 | 0.09 |\n| Cumulative Proportion | 0.24 | 0.45 | 0.61 | 0.71 | 0.80 |\n\nStatement: The highest value is 1.95 in PC1 of Standard deviation.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q36e857609f",
  "kind": "yes/no",
  "text": "Table caption: Amino acids as butyl esters and their molecular ions. Additional amino acids can be detected and quantified with the matching stable-isotopic labeled standards.\n| Target amino acid | [M+H] + /[M+H] + Internal standard as butylesters |\n| Alanine | 146/150 |\n| Arginine | 231/236 |\n| Aspartic Acid | 246/249 |\n| Citrulline | 232/234 |\n| Glutamic acid | 260/263 |\n| Glycine | 132/134 |\n| Leucine/Isoleucine | 188/191 |\n| Methionine | 206/209 |\n| Ornithine | 189/191 |\n| Phenylalanine | 222/228 |\n| Tyrosine | 238/244 |\n| Valine | 174/182 |\n\nStatement: Leucine/Isoleucine has 188/191 as values.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8a85d8fdb6",
  "kind": "yes/no",
  "text": "Table caption: Description of sites in terms of LiDAR-derived median and 95 % range of woody cover fraction (WCF) and measures of prediction performance: prediction bias, root mean square error (RMSE), coefficient of determination (R 2 ) and model efficiency (ME). Note: all cover values are given in % to reduce the number of digits.\n| Site name | median (95 % range) | bias | RMSE | R 2 | ME |\n| 1) Australian Capital Territory | 37 (0−71) | 0.3 | 7.3 | 0.90 | 0.90 |\n| 2) Alice Springs (NT) | 36 (26−43) | −1.1 | 3.5 | 0.56 | 0.42 |\n| 3) Credo (WA) | 18 (6−33) | 0.3 | 4.2 | 0.63 | 0.62 |\n| 4) Litchfield (NT) | 24 (15−36) | 0.2 | 4.4 | 0.41 | 0.40 |\n| 5) Robson (Qld) | 92 (0−98) | −0.8 | 8.2 | 0.91 | 0.91 |\n| 6) Rushworth (Vic) | 43 (31−49) | −0.3 | 3.4 | 0.70 | 0.70 |\n| 7) Tumbarumba (NSW) | 52 (25−70) | 1.4 | 7.1 | 0.62 | 0.61 |\n| 8) Warra (Tas) | 91 (50−96) | −1.7 | 9.0 | 0.34 | 0.32 |\n| 9) Watts (Vic) | 86 (66−94) | −3.6 | 9.1 | 0.12 | −0.41 |\n| 10) Whroo (Vic) | 42 (36−47) | −0.8 | 2.7 | 0.24 | −0.05 |\n| 11) ZigZag (Vic) | 59 (44−82) | 1.8 | 8.1 | 0.35 | 0.23 |\n\nStatement: Robson (Qld) and Rushworth (Vic) has same coefficient of determination.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdf3cc59f95",
  "kind": "yes/no",
  "text": "Table caption: The categories and their conditions.\n| Category | More likely to be salient | Less likely to be salient |\n| Loudness | Word intensity of 80 dB | Word intensity of 60 dB |\n| Acoustic Prominence | /t/pronounced as [p] | /t/pronounced as [t] |\n| Grammatical Gender | Violation of grammatical gender | Correct grammatical gender |\n| Frequency | High frequency word | Low frequency word |\n| Conscious Sound Change | /r/pronounced as [ɹ] | /r/pronounced as [r] |\n| Subconscious Sound Change | /v/pronounced as [v] (=voiced) | /v/pronounced as [f] (=voiceless) |\n\nStatement: There are ten categories and their conditions.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8b277e9b2d",
  "kind": "yes/no",
  "text": "Table caption: Proposal related to Open Science in subsequent questionnaire.\n| Proposal | Proposal |\n| P2.4 | Open Science in the context of “Science Shop 2.0” is a combination of the aims of Public, Democratic, and Measurements School |\n\nStatement: All the values are observed to be unique.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd06fd3b014",
  "kind": "yes/no",
  "text": "Table caption: RMSE, MAE and R 2 calculated for the training and test sets for each predictive model.\n|  | Training | Training | Training | Test | Test | Test |\n|  | RMSE | MAE | R 2 | RMSE | MAE | R 2 |\n| Linear model | 0.018 | 0.014 | 0.442 | 0.019 | 0.015 | 0.421 |\n| Regression tree | 0.016 | 0.012 | 0.553 | 0.016 | 0.013 | 0.586 |\n| Bagged tree | 0.016 | 0.012 | 0.599 | 0.016 | 0.013 | 0.577 |\n| Random forest | 0.014 | 0.010 | 0.705 | 0.016 | 0.012 | 0.596 |\n| Gradient boosting | 0.014 | 0.011 | 0.654 | 0.016 | 0.012 | 0.623 |\n| Lasso | 0.019 | 0.014 | 0.425 | 0.020 | 0.015 | 0.401 |\n| Ridge regression | 0.018 | 0.014 | 0.448 | 0.019 | 0.015 | 0.426 |\n| Elastic net | 0.019 | 0.014 | 0.428 | 0.020 | 0.015 | 0.404 |\n| Spline | 0.016 | 0.012 | 0.591 | 0.016 | 0.012 | 0.594 |\n\nStatement: Elastic net Test MAE is 0.015.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q09ce0e79cf",
  "kind": "yes/no",
  "text": "Table caption: CMVs and RMVs regarding the performance indicator “Number of independent citations”.\n|  | Current minimum values | Number of independent citations, 2014–2019 | Number of independent citations, 2014–2019 | Number of years required to fulfill minimum value | Number of years required to fulfill minimum value | Recalibrated minimum values | Recalibrated minimum values |\n|  |  | IC a | FC b | IC a | FC b | IC a | FC b |\n| Mining | 120 | 62.875 | 19.934 | 9.543 | 30.099 | 102 (101.983) | 32 (32.333) |\n| Geology | 150 | 115.538 | 24.531 | 6.491 | 30.573 | 187 (187.403) | 40 (39.790) |\n| Geodesy and Geoinformatics | 120 | 45.800 | 10.132 | 13.100 | 59.221 | 74 (74.288) | 16 (16.433) |\n| Geophysics | 150 | 48.583 | 9.845 | 15.437 | 76.179 | 79 (78.802) | 16 (15.969) |\n| Geochemistry, Mineralogy and Petrology | 150 | 127.700 | 21.111 | 5.873 | 35.526 | 207 (207.129) | 34 (34.242) |\n| Meteorology | 150 | 151.154 | 34.312 | 4.962 | 21.858 | 245 (245.172) | 56 (55.654) |\n| Paleontology | 150 | 153.250 | 27.642 | 4.894 | 27.133 | 249 (248.572) | 45 (44.835) |\n| Social Geography | 150 | 101.583 | 42.932 | 7.383 | 17.470 | 165 (164.768) | 70 (69.636) |\n| Physical Geography | 120 | 113.167 | 25.925 | 5.302 | 23.144 | 184 (183.556) | 42 (42.050) |\n\nStatement: Paleontology have highest Recalibrated minimum values of 249 (248.572).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5815db24cd",
  "kind": "yes/no",
  "text": "Table caption: DIC land load and net air-sea CO 2 exchange (F CO2 ) (Gmol year −1 ) on Baltic Sea system-scale in a few selected scenarios (negative F CO2 indicates net outgassing and vice versa).\n| Model run | Factor addressed | Case | DIC land load | F CO2 |\n| #1 | None | REF | 887 | −95 |\n| #28 | DIC loads | REF − 10% | 798 | −6 |\n| #29 | DIC loads | REF − 20% | 710 | 83 |\n| #30 | DIC loads | REF + 10% | 976 | −184 |\n| #31 | DIC loads | REF + 20% | 1064 | −273 |\n| #17 | N/P loads (land + atm.) | BSAP | 887 | −139 |\n| #18 | N/P loads (land + atm.) | HEL | 887 | −58 |\n| #19 | N/P loads (land + atm.) | HIGH | 887 | 75 |\n\nStatement: DIC land load has heighest value of 1064 for #31 Model run.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4d28fa064f",
  "kind": "yes/no",
  "text": "Table caption: Survey response rate and number of ATMPs manufactured under exemption pathways by public facilities, per country.\n|  | Public facilities | Public facilities | ATMPs (public) | ATMPs (public) |\n|  | Recipients (n) | Respondents (n)/response rate (%) | HE (n) 2009–2017 | NPU (n) 2015–2017 |\n| Belgium | 7 | 3/43 | 0 | 0 |\n| Finland | 2 | 1/50 | 1 | 0 |\n| France | 1 | 1/100 | 0 | 0 |\n| Germany | 22 | 3/14 | 3 | 0 |\n| Italy | 5 | 3/60 | 2 | 5 |\n| Netherlands | 9 | 8/89 | 6 | 2 |\n| United Kingdom | 21 | 8/38 | 0 | 4 |\n| Total | 67 | 27/40 | 12 | 11 |\n\nStatement: The other 20 respondent public facilities did not manufacture ATMPs under an HE license.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdc583f4752",
  "kind": "yes/no",
  "text": "Table caption: Characteristics of all ESS 11 cases in relation to gender.\n| Gender | Women ( n = 1087) | Men ( n = 783) | P |\n| Age - years |  |  |  |\n| Median (25 th ,75 th percentile) | 73 (56−84) | 71 (55−81) | 0.025 |\n| Priority at dispatch centre - n (%) a |  |  | 0.001 |\n| Prio 1 | 334 (30.8) | 302 (38.6) |  |\n| Prio 2 | 698 (64.3) | 448 (57.2) |  |\n| Prio 3 | 53 (4.9) | 33 (4.2) |  |\n| Triage colour RETTS - n (%) |  |  | 0.002 |\n| Red | 11 (1.0) | 13 (1.7) |  |\n| Orange | 224 (20.6) | 195 (24.9) |  |\n| Yellow | 587 (54.0) | 423 (54.0) |  |\n| Green | 265 (24.4) | 152 (19.4) |  |\n| Level of care - n (%) |  |  | 0.170 |\n| To hospital | 849 (78.1) | 632 (80.7) |  |\n| Stay at the scene | 238 (21.9) | 151 (19.3) |  |\n| Seek medical advice within 72 h. - n (%) b | 29 (12.2) | 15 (9.9) | 0.517 |\n| Mode of transport - n (%) c |  |  | 0.605 |\n| Ambulance | 764 (90.0) | 584 (92.4) |  |\n| PTS, immobile d | 33 (3.9) | 17 (2.7) |  |\n| PTS, seated | 32 (3.8) | 18 (2.8) |  |\n| Single-responder unit | 8 (0.9) | 9 (1.4) |  |\n| Transport by own means | 12 (1.4) | 4 (0.6) |  |\n| Type of condition - n (%) |  |  |  |\n| Non-time critical | 1040 (95.7) | 734 (93.7) | 0.062 |\n| Time critical | 47 (4.3) | 49 (6.3) |  |\n\nStatement: Prio 3 Men ( n = 783) is 53 (4.9).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q64ede12581",
  "kind": "yes/no",
  "text": "Table caption: Côte d’Ivoire emissions for 2010 from this study compared with estimates from global initiatives.\n| Species | Units | This study | This study adjusted (i.e. without emissions from savannah and other vegetation fires and road dust) | EDGAR (v4.3.2) | GAINS Eclipse v5a |\n| SO 2 | Gg yr −1 | 33.0 | 25.8 | 18.0 | 33.3 |\n| NO X | Gg yr −1 | 187 | 133 | 45.7 | 58.1 |\n| CO | Tg yr −1 | 2.82 | 1.57 | 1.48 | 1.83 |\n| NMVOC | Gg yr −1 | 511 | 426 | 1307 | 296 |\n| NH 3 | Gg yr −1 | 91.5 | 79.8 | 79.7 | 68.8 |\n| PM 10 | Gg yr −1 | 565 | 155 | 262 | 185 |\n| PM 2.5 | Gg yr −1 | 232 | 95.8 | 87.9 a | 168 |\n| BC | Gg yr −1 | 20.2 | 12.6 | 12.1 | 28.6 |\n| OC | Gg yr −1 | 99.6 | 44.5 | 33.5 | 68.9 |\n| CH 4 | Gg yr −1 | 414 | 351 | 398 | 319 |\n| CO 2 | Tg yr −1 | 12.8 | 12.8 | 6.78 |  |\n\nStatement: All species has constant Gains Eclipse.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qfdb48ea9d0",
  "kind": "yes/no",
  "text": "Table caption: Weight loss of the uncoated and coated tomatoes during storage.\n| Treatment | Storage periods | Storage periods | Storage periods | Storage periods | Storage periods |\n| Treatment | 0th day | 7th day | 14th day | 21st day | 28th day |\n| 1% K. alvarezii | 0.00 | 4.235 | 9.001 | 13.846 | 17.220 |\n| 2% K. alvarezii | 0.00 | 3.004 | 6.023 | 8.768 | 15.768 |\n| 3% K. alvarezii | 0.00 | 2.402 | 3.814 | 4.449 | 6.332 |\n| 1% S. tenerrimum | 0.00 | 4.615 | 11.261 | 13.869 | 16.917 |\n| 2% S. tenerrimum | 0.00 | 4.376 | 9.100 | 12.981 | 16.790 |\n| 3% S. tenerrimum | 0.00 | 2.772 | 7.411 | 11.985 | 16.165 |\n| Control (uncoated) | 0.00 | 3.611 | 9.924 | 15.451 | 19.639 |\n\nStatement: The largest storage period of 3% S. tenerrimum on 28th day is 16.165",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe5a6e1876e",
  "kind": "yes/no",
  "text": "Table caption: TDA parameters combinations together with Distribution criteria and Average Path Length.\n| Number of Intervals | Overlap Percentage | Number of Bins | Hidden States Distribution - Pearson Correlation with original distribution | Average Path Length |\n| 7 | 50 | 6 | 0.9449133 | 5.167059 |\n| 7 | 45 | 6 | 0.9408602 | 5.596531 |\n| 8 | 55 | 6 | 0.934875 | 5.828645 |\n| 7 | 60 | 6 | 0.9291068 | 5.517241 |\n| 7 | 40 | 6 | 0.9231947 | 5.682504 |\n| 7 | 55 | 6 | 0.9135777 | 5.167677 |\n| 7 | 60 | 8 | 0.9076339 | 5.308756 |\n| 8 | 60 | 6 | 0.8985553 | 5.930751 |\n| 7 | 55 | 8 | 0.877915 | 5.523086 |\n| 8 | 60 | 8 | 0.8769934 | 5.983423 |\n\nStatement: Number of Intervals 8 Overlap Percentage is 20.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q90401c2277",
  "kind": "yes/no",
  "text": "Table caption: GFRP bars specifications.\n| Bar type | GFRP |\n| Nominal diameter (mm) | 14 |\n| Ultimate strength (MPa) | 1200 |\n| Modulus of elasticity (MPa) | 55,000 |\n| Strain,ε ƒu (με) | 1950 |\n\nStatement: Every bar type has same GFRP",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc1b1d84787",
  "kind": "yes/no",
  "text": "Table caption: Mixes proportions.\n| Mix ID | Proportions by Wight (%) | Proportions by Wight (%) | Proportions by Wight (%) | Proportions by Wight (%) | Proportions by Wight (%) | Proportions by Wight (%) |\n| Mix ID | Clay | Sludge | RSA | SBA | WSA | Water to raw materials% |\n| Control | 50 | 50 | – | – | – | 35 |\n| M-5RSA | 50 | 45 | 5 | – | – | 35 |\n| M-10RSA | 50 | 40 | 10 | – | – | 38 |\n| M-15RSA | 50 | 35 | 15 | – | – | 38 |\n| M-5SBA | 50 | 45 | – | 5 | – | 38 |\n| M-10SBA | 50 | 40 | – | 10 | – | 40 |\n| M-15SBA | 50 | 35 | – | 15 | – | 40 |\n| M-5WSA | 50 | 45 | – | – | 5 | 38 |\n| M-10WSA | 50 | 40 | – | – | 10 | 38 |\n| M-15WSA | 50 | 35 | – | – | 15 | 40 |\n\nStatement: The highest water to raw materials value is 38 for M-10SBA, M-15SBA and M-15WSA.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qeb4cb9f5f2",
  "kind": "yes/no",
  "text": "Table caption: Comparison of the lengths of positive and negative reviews.\n| binary_score | responses_message_length |\n| negative | 1474.2 |\n| positive | 1041.6 |\n\nStatement: There are 2 columns in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa158d40277",
  "kind": "yes/no",
  "text": "Table caption: List of all variables.\n| Variables | Definition | Source |\n| ESG score | The overall firm score derived from the self-disclosed information combining ESG pillar scores. | Thomson Reuters (TR) EIKON |\n| Environmental Pillar score | The Environmental Pillar assesses a firm's influence on living and non-living natural ecosystems, including the land, water, and air. | TR EIKON |\n| Social Pillar score | The Social Pillar measures a firm's competence to create faith and devotion with its customers, employees, and society. | TR EIKON |\n| Governance Pillar score | The Corporate Governance Pillar evaluates a firm's processes and systems and its executives' and board of directors' acts to guarantee long-term shareholder value. | TR EIKON |\n| Tobin Q (Tobin's Q ratio) | The ratio of total debt and market capitalization to total assets | Author's calculations |\n| Board Size | The number of board of directors | TR EIKON |\n| Board Gender Diversity | The percentage of the female board of directors | TR EIKON |\n| Board Independence | Indicating the existence of policy about the independence of its board | TR EIKON |\n| CEO Board Chair Separation | Indicating either the CEO instantaneously leads the board or the board chairperson is the CEO of the company | TR EIKON |\n| Sustainability Committee | Indicating whether the CSR or sustainability committee or team exist in the company | TR EIKON |\n| Free Float Percentage | The percentage of shares outstanding | TR EIKON |\n| Total Assets | The total assets owned by the company | TR EIKON |\n| Leverage | The ratio of total liabilities to total assets | Author's calculations |\n| ROA (Return on assets) | The ratio of net income (minus taxes) to total assets | Author's calculations |\n\nStatement: Board Gender Diversity source is Author's calculations.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q6e19262179",
  "kind": "yes/no",
  "text": "Table caption: Ordered logistic regression analyses for associations between IHS- and FC-status and the total degree of SRP (n = 9,785).\n|  | Received CWS-interventions | Received CWS-interventions | Received CWS-interventions | Received CWS-interventions |\n|  | IHS(n = 141) | p-value | FC(n = 155) | p-value |\n| Unadjusted, OR (95% CI) | 3.23 (2.35, 4.45) | <0.001 | 1.56 (1.11, 2.17) | 0.010 |\n| Adjusted for sex, AOR (95% CI) | 3.22 (2.34, 4.43) | <0.001 | 1.56 (1.11, 2.18) | 0.010 |\n| (+) adjusted for age, AOR (95% CI) | 3.54 (2.56, 4.89) | <0.001 | 1.72 (1.22, 2.43) | 0.002 |\n| (+) adjusted for ethnicity, AOR (95% CI) | 3.89 (2.80, 5.40) | <0.001 | 1.92 (1.35, 2.73) | <0.001 |\n| (+) adjusted for internalizing problems, AOR (95% CI) | 3.55 (2.55, 4.94) | <0.001 | 1.89 (1.32, 2.69) | <0.001 |\n| (+) adjusted for externalizing problems, AOR (95% CI) | 2.31 (1.72, 3.38) | <0.001 | 1.51 (1.05, 2.18) | 0.027 |\nTable notes: Note : IHS = in-home services. FC = foster care. SRP = substance-related problems. OR = odds ratio. AOR = adjusted odds ratio. CI = confidence interval. Bold fonts denote statistically significant associations.\n\nStatement: The lowest IHS(n = 141) is 2.31 (1.72, 3.38).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0548fda2f2",
  "kind": "yes/no",
  "text": "Table caption: Information of the test CFST columns.\n| Sectional shape | Symbol | P (mm) | H (mm) | t (mm) | Ac (mm 2 ) | Nu (kN) | σ u (MPa) | SI | DI |\n| Circular | CC | 503 | 1000 | 2 | 20,106 | 744.9 | 251.8 | 1.00 | 2.169 |\n| Square | CS | 500 | 1000 | 2 | 15,625 | 668.9 | 265.7 | 1.05 | 2.572 |\n| Square with rounded-ended | CSE | 500 | 1000 | 2 | 15,625 | 694.9 | 276.1 | 1.09 | 2.363 |\n| Rhombic | CRH | 500 | 1000 | 2 | 15,000 | 629.3 | 256.2 | 1.01 | 2.264 |\n| Rectangular | CR | 510 | 1000 | 2 | 14,450 | 605.2 | 249.3 | 0.99 | 2.038 |\n| Rectangular with round ended | CRE | 506 | 1000 | 2 | 15,903 | 621.8 | 243.2 | 0.96 | 2.063 |\n| Elliptical | CE | 484 | 1000 | 2 | 15,708 | 607.4 | 243.6 | 0.96 | 1.995 |\n| Hexagonal asymmetric | CHA | 500 | 1000 | 2 | 16,500 | 565.9 | 217.5 | 0.86 | 1.953 |\n| Triangle | CT | 510 | 1000 | 2 | 12,512 | 491.8 | 232.6 | 0.92 | 1.9360 |\n| Pentagram | CP | 500 | 1000 | 2 | 17,205 | 669.7 | 250.8 | 0.99 | 1.818 |\n| Hexagon | CH | 510 | 1000 | 2 | 18,771 | 703.1 | 247.3 | 0.98 | 1.687 |\n| Octagon | CO | 480 | 1000 | 2 | 17,382 | 760.3 | 287.1 | 1.14 | 3.009 |\n| 1/4 circular | CQC | 500 | 1000 | 2 | 15,394 | 596.7 | 239.2 | 0.95 | 2.701 |\n| Semi-circular | CSC | 514 | 1000 | 2 | 15,708 | 554.1 | 217.1 | 0.86 | 2.068 |\n| D-Shaped | CD | 500 | 1000 | 2 | 15735 | 547.2 | 216.5 | 0.85 | 1.926 |\n| Fan-shaped | CF | 500 | 1000 | 2 | 16,897 | 577.7 | 218.7 | 0.86 | 1.722 |\n| L-Shape | CL | 520 | 1000 | 2 | 12,675 | 530.7 | 224.9 | 0.89 | 1.621 |\n| T-Shape | CTS | 500 | 1000 | 2 | 10,000 | 475.4 | 231.1 | 0.91 | 2.0568 |\n| Plus-shaped | CPS | 480 | 1000 | 2 | 8000 | 490.6 | 282.4 | 1.12 | 2.1695 |\n\nStatement: Octagon and Plus-shaped has different mm of P.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4ca78680cf",
  "kind": "yes/no",
  "text": "Table caption: Segmentation of clinical data.\n| Parameter | t o − t 1 | t 1 − t 2 | t 2 − t 3 | t 3 − t p |\n| A (height) | 29.18 | 26.02 | 0 | 3.37 |\n| τ (length) | 0.068 | 0.104 | 0.0452 | 0.053 |\n\nStatement: The length value is < 0 in all the columns.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q33bf0b72bb",
  "kind": "yes/no",
  "text": "Table caption: Material properties of PVC.\n| Mechanical properties |  | Thermal properties |  |\n| Elastic modulus (GPa) | 2.9-3.4 | Thermal conductivity (W/mk) | 0.16 |\n| Density (kg/m 3 ) | 1380 | Specific heat (J/kg K) | 900 |\n| Poisso’s ratio | 0.38 | Glass transition temperature(K) | 361 |\n| Yield stress (MPa) | 50-80 | Melting temperature(K) | 486 |\n\nStatement: There are four Mechanical properties .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q340aa32b99",
  "kind": "yes/no",
  "text": "Table caption: Discriminant validity based on cross-loading evaluation.\n| Indicator | III | CII | IO | EE |\n| III1 | 0.843 | 0.466 | 0.552 | 0.356 |\n| III2 | 0.874 | 0.400 | 0.567 | 0.316 |\n| III3 | 0.913 | 0.525 | 0.621 | 0.359 |\n| III4 | 0.886 | 0.542 | 0.589 | 0.312 |\n| CII1 | 0.552 | 0.938 | 0.616 | 0.329 |\n| CII2 | 0.520 | 0.937 | 0.568 | 0.267 |\n| CII3 | 0.472 | 0.930 | 0.611 | 0.325 |\n| IO1 | 0.614 | 0.696 | 0.870 | 0.442 |\n| IO2 | 0.594 | 0.595 | 0.914 | 0.430 |\n| IO3 | 0.550 | 0.472 | 0.861 | 0.407 |\n| IO4 | 0.516 | 0.404 | 0.796 | 0.413 |\n| EE1 | 0.361 | 0.293 | 0.426 | 0.867 |\n| EE2 | 0.311 | 0.282 | 0.446 | 0.929 |\n| EE3 | 0.348 | 0.312 | 0.422 | 0.922 |\n| EE4 | 0.367 | 0.310 | 0.490 | 0.917 |\n\nStatement: The Highest value in III is 0.913.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q716aead2fd",
  "kind": "yes/no",
  "text": "Table caption: Visual example of a plate in comparative rate experiment between 3 batches of purified HKT performed in duplicate.\n|  | Blank 1 | Blank 2 | 0 min - 1 | 0 min - 2 | 5 min - 1 | 5 min - 2 |\n| Batch 1 | Mix 3 + 2 | Mix 3 + 2 | Mix 1 + 2 | Mix 1 + 2 | Mix 1 + 2 | Mix 1 + 2 |\n| Batch 2 | Mix 3 + 2 | Mix 3 + 2 | Mix 1 + 2 | Mix 1 + 2 | Mix 1 + 2 | Mix 1 + 2 |\n| Batch 3 | Mix 3 + 2 | Mix 3 + 2 | Mix 1 + 2 | Mix 1 + 2 | Mix 1 + 2 | Mix 1 + 2 |\n\nStatement: E.g.: Comparison of the activity between 3 batches of purified HKT in duplicate.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2882a5d18b",
  "kind": "yes/no",
  "text": "Table caption: Pair-wise comparisons of criteria.\n| Criteria of Evaluation | Eff | Res | Weight | CR |\n| Eff | 1 | 7 | 0.875 | 0% |\n| Res | 1/7 | 1 | 0.125 |  |\n\nStatement: Res weight is 0.125.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q598f67bd3f",
  "kind": "yes/no",
  "text": "Table caption: Obstetric Data\n|  | N | % |\n| Planned home birth | 33 | 63.5 |\n| Prolonged labor | 5 |  |\n| Breech | 2 |  |\n| Umbilical cord strangulation | 5 |  |\n| Meconium | 2 |  |\n| Shoulder dystocia | 4 |  |\n| Precipitous labor | 2 |  |\n| Partial abruption placentae | 1 |  |\n| Fetal bradycardia during delivery | 1 |  |\n| Normal delivery | 6 |  |\n| Labor not documented | 7 |  |\n| Unplanned out-of-hospital birth | 17 | 32.7 |\n| Resuscitative hysterotomy | 2 |  |\n| Precipitous labor | 5 |  |\n| Preterm labor | 12 |  |\n| Breech | 1 |  |\n| Unknown pregnancy | 2 |  |\n| Unknown intended location of delivery | 2 | 3.8 |\n\nStatement: Unknown intended location of delivery has the highest percent of 3.8.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0074002b18",
  "kind": "yes/no",
  "text": "Table caption: Correlation between cerebral perfusion pressure and brain tissue oxygenation in 5 patients.\n| Patient No | Pearson coefficient (r) of correlation between CPP and PbtO 2 and probability (p) |\n| 1 | 0.79, p < 0.01 |\n| 2 | 0.38, p < 0.01 |\n| 3 | 0.35, p < 0.01 |\n| 4 | 0.77, p < 0.01 |\n| 5 | 0.7, p < 0.01 |\nTable notes: Abbreviations: r – Pearson's correlation coefficient; CPP – cerebral perfusion pressure; PbtO 2 – partial pressure of oxygen in brain tissue.\n\nStatement: There are 7 patients listed.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5c75de83ae",
  "kind": "yes/no",
  "text": "Table caption: Overall effects of droughts on total economic activity in response to different drought severity levels (% change with respect to benchmark scenario). Total effect on GDP and breakdown of production losses by macro-sectors of activity and agricultural sectors.\n|  | 2003 | 2006 | 2011 |\n| GDP (%) | −0.10 | −0.05 | −0.03 |\n| GDP (M€) | −1748.1 | −924.3 | −560.7 |\n| Agricultural Production (%) | −3.74 | −1.99 | −1.16 |\n| Agricultural Production (M€) | −2061.9 | −1098.8 | −638.2 |\n| Rice | −6.51 | −2.50 | −2.53 |\n| Wheat | −5.75 | −2.08 | −1.53 |\n| Other grains | −4.17 | −1.35 | −1.53 |\n| Veg & Fruit | −8.69 | −2.50 | −1.84 |\n| Oil seeds | −0.43 | −0.40 | −0.53 |\n| Sugar beet | −0.44 | −0.19 | −0.15 |\n| Other crops | −1.77 | −2.45 | −1.02 |\n| Rest of primary | 0.08 | 0.05 | 0.02 |\n| Food Industry | −0.53 | −0.31 | −0.18 |\n| Rest of Industry | 0.11 | 0.06 | 0.03 |\n| Trade Services | −0.10 | −0.06 | −0.04 |\n| Rest of Services | −0.03 | −0.02 | −0.01 |\n\nStatement: All the values in Rest of Industry and Rest of primary is positive.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q954b3570f6",
  "kind": "yes/no",
  "text": "Table caption: Variants of as-cast Ti45221B with alloy composition.\n| Alloy composition (at. %) | Analysis |\n| Ti-45Al-2Mn-2Nb-0.8B(Ti45220.8B) Ti-48Al-2Mn-2Nb-1B(Ti48221B) Ti-50Al-2Mn-2Nb-1B(Ti50221B) | Effect of Al |\n| Ti-45Al-2Mn-2Nb-0.8B Ti-45Al-2Mn-4Nb-0.8B ⁎ | Effect of Nb |\n| Ti-45Al-2Nb-2Hf-0.8B ⁎ Ti-44Al-4Nb-4Hf-1B Ti-45Al-2Cr-2Hf-0.8B | Effect of Hf |\n| Ti-45Al-2Mn-4Ta-0.8B ⁎ Ti-45Al-2Nb-2Ta-0.8B | Effect of Ta |\n| Ti-46Al-8Nb-1B | Effect of high Nb content |\n\nStatement: There are 6 different types of Alloy composition.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3aa89081f2",
  "kind": "yes/no",
  "text": "Table caption: Impacts of rainfall anomalies on HAZ score, stunting and severe stunting – testing for non-linearity in the effects, children aged 0–5.\n|  | HAZ (OLS coef.) | Stunted (OR) | Severely stunted (OR) |\n| Average rainfall anomalies | −0.09*** | 1.14*** | 1.18*** |\n|  | (0.02) | (0.03) | (0.04) |\n| Average rainfall anomalies 2 | 0.01 | 0.98 | 0.97 |\n|  | (0.01) | (0.015) | (0.02) |\n| Observations | 220,823 | 220,823 | 220,823 |\n| (Pseudo) R 2 | 0.11 | 0.06 | 0.05 |\nTable notes: Notes: * p < 0.05, ** p < 0.01, *** p < 0.001. Age splines and fixed effects for month of birth, month of interview, year of interview and district included but not displayed. Sampling weights applied. Average rainfall anomalies measured from the in-utero period up until the time of the interview. Robust standard errors reported in parentheses. Standard errors clustered at the district level. Sampling weights applied.\n\nStatement: Average rainfall anomalies 2 has lowest HAZ score.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb031879e69",
  "kind": "yes/no",
  "text": "Table caption: Activation barriers (eV) for specific steps of the methanol electro-oxidation on Pd(111), Pd 3 Ni(111) and PdNi(111). The corrected values consider a potential of 0.85 V (check for more details). Moreover, reaction with – means that the activation barriers could not be computed since final states were not stable (final states moved back to initial states with the local energy optimization). This suggests that the reaction would not happen under such conditions.\n| Reaction | Pd | Pd 3 Ni | PdNi |\n| CH 3 OH → CH 3 O + H + + e − | 0.5 |  |  |\n| CH 3 OH → CH 2 OH + H + + e − | 0.9 |  |  |\n| CH 2 O → CHO + H + + e − | 0.3 | 0.8 | 1.2 |\n| CH 2 O+OH →CH 2 OOH | 0.4 | 0.4 | 0.8 |\n| CHO → CO + H + + e − | (spontaneous) | (spontaneous) | 0.4 |\n| CHO + OH → HCOOH | 0.2 | 0.2 | 0.2 |\n| CO + OH → COOH | 1.1 | 1.2 | 1.5 |\n| H 2 COOH → HCOOH + H + + e − |  | 0.9 | 1.1 |\n| H 2 COOH → H 2 COO + H + + e − |  | (–) | (–) |\n| HCOOH → CHOO + H + + e − |  | (spontaneous) | (spontaneous) |\n\nStatement: 9.5 is the Pd value for CH 3 OH CH 3 O + H + + e Reaction.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1ad1bbe858",
  "kind": "yes/no",
  "text": "Table caption: Path analysis.\n| Factors | Standard Coefficient | SE - value | t-value | 95% biased confidence interval | 95% biased confidence interval | Results |\n| Factors | Standard Coefficient | SE - value | t-value | LL | UL | Results |\n| NSR tourism infrastructure to QOL | 0.15∗∗ | 0.045 | 3.373 | 0.064 | 0.243 | Supported |\n| NSR tourism infrastructure to STD | 0.26∗∗∗ | 0.046 | 5.550 | 0.165 | 0.346 | Supported |\n| Sustainable tourism to QOL | 0.24∗∗∗ | 0.046 | 5.290 | 0.154 | 0.337 | Supported |\nTable notes: Note: ∗∗p<0.005, ∗∗∗p<0.001. NSR = New Silk Road, QOL = Quality of life, STD = Sustainable tourism development .\n\nStatement: Factor NSR tourism infrastructure to STD ha the highest value for Standard Coefficient of 0.17.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa5d0ba49bf",
  "kind": "yes/no",
  "text": "Table caption: Saturated acylcarnitines by acyl chain length as butyl esters and their molecular ions.\n| Chain length | [M+H] + /[M+H] + Internal standard as butylesters |\n| C2 | 260/263 |\n| C3 | 274/277 |\n| C4 | 288/299 |\n| C5 | 302/311 |\n| C6 | 316 |\n| C8 | 344/347 |\n| C10 | 372 |\n| C12 | 400 |\n| C14 | 428/437 |\n| C16 | 456/459 |\n| C18 | 484 |\n\nStatement: Chain length C4 has [M+H] + /[M+H] + Internal standard as butylesters of 288/299.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2514623071",
  "kind": "yes/no",
  "text": "Table caption: ABSCO parameters for v5.0 (OCO L2 B8 and B9) and v5.1 (OCO L2 B10).\n| Band | 0.76 µm | 1.6 µm | 2.06 µm |\n| Spectral range (cm − 1 ) | 12,950 to 13,190 | 6120 to 6260 | 4800 to 4890 |\n| ABSCO version | 5.0 / 5.1 | 5.0 / 5.1 | 5.0 / 5.1 |\n| line shape | a / b | f / f | i / i |\n| line mixing | a / b | f / f | i / i |\n| CIA | a / b | - | j / j |\n| H 2 O broadening | c / c | g / g | g / g |\n| H 2 O continuum | d / e | d / e | d / e |\n| H 2 O lines | h / h | h / h | h / h |\nTable notes: ( a ) Drouin et al. ; ( b ) This work; ( c ) Drouin et al. ; ( d ) Mlawer et al. ; ( e ) MT _ CKD v3.2; ( f ) Devi et al. ; ( g ) Sung et al. ; ( h ) Rothman et al. ; ( i ) Benner et al. ; ( j ) Thompson et al. .\n\nStatement: ABSCO version is same 5.0 / 5.1 for all three 0.76 m ,1.6 m and 2.06 m.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb9e7e735bf",
  "kind": "yes/no",
  "text": "Table caption: Pyrolysis products yield.\n| Temperature | Biochar yield (wt%) | Bio-oil yield (wt%) | Gas yield (wt%) |\n| 300 °C | 54.83 | 0.00 | 45.17 |\n| 500 °C | 29.93 | 13.91 | 56.16 |\n| 700 °C | 28.37 | 28.48 | 43.16 |\n| 900 °C | 26.67 | 7.38 | 65.96 |\n\nStatement: 0.00 Bio-oil yield (wt%) Temperature is 900 C .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qeb234aa601",
  "kind": "yes/no",
  "text": "Table caption: Descriptions of variables in the geolocation_data worksheet\n| No | Name | Description | Code | Measure | Unit | Source |\n| 1 | Identity | Unique ID to each irrigation network component. The ID is the official nomenclature from Klambu Wilalung Irrigation District. | ID |  |  | Official data |\n| 2 | Name | The name of each irrigation network component | name |  |  | Official data |\n| 3 | Type a | The type of component in the irrigation network (1=structure, 2=canal) | type | Nominal |  | Official data |\n| 4 | Status | The status of irrigation network components. For structures (1=main structures, 2=supporting structures). For canals (1=primary canal, 2=secondary canal). | stat | Nominal |  | Official data |\n| 5 | X Coordinate b | The Easting coordinate in UTM Projection System | X |  |  | Official data |\n| 6 | Y Coordinate b | The Northing coordinate in UTM Projection System | Y |  |  | Official data |\n| 7 | WUA | The WUA for which each irrigation network components situated |  |  |  | Enumeration |\n| 8 | Village | The village for which each irrigation network components situated |  |  |  | Enumeration |\nTable notes: Note:\n\nStatement: WUA and Village has a official source.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qbbe2d30aa4",
  "kind": "yes/no",
  "text": "Table caption: The research team utilized a mixed-methods approach to data collection from September 2017 to September 2019. These methods allowed the research team to engage carinata stakeholders involved at various stages of the crop’s production and processing.\n| Timeline | 2017 | 2018 | 2018 | 2019 | 2019 |\n| Research Audience (Sampling size) | Key informants (n = 15) | Carinata event attendees (n = 34) | Previous carinata growers (n = 8) | Carinata event organizers (n = 7) | Producers (n = 4); extension faculty (n = 2); carinata agronomist (n = 1) |\n| Data Collection Instrument | Semi-structured interview | Survey with ranking exercise | Semi-structured interview and sorting exercise | Semi-structured interview | Focus group |\n\nStatement: The Research Audience (Sampling size) is same for all the Timelines.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc7fe69cbcc",
  "kind": "yes/no",
  "text": "Table caption: Comparative antibacterial activity of synthesized nanoparticles ZnO and TiO 2 nanoparticles against different microorganisms.\n| Plant species | Plant part used | NPs tested | Species | References |\n| Catharanthus roseus | Leaf | ZnO | B. thuringiensis, E. coli, S. aureus, P. aeruginosa | Bhumi and Savithramma, 2014 |\n| Brassica oleraceae | Leaf | ZnO | E. coli, V. cholera, C. Botulinum, S. aureus, B. subtilis | Raj et al., 2015 |\n| Trifolium pratense | Flower | ZnO | S. aureus, P. aeruginosa, E. coli | Dobrucka and Dugaszewska, 2016 |\n| Bauhinia tomentosa | Leaf | ZnO | B. thuringiensis, E. coli, S. aureus, P. aeruginosa | Sharmila et al., 2018 |\n| Pandanus odorifer | Leaf | ZnO | B. subtilis, E. coli | Hussain et al., 2019 |\n| Aloe vera | Leaf | ZnO | E. coli | Izwanie Rasli et al., 2020 |\n| Psidium guajava | Leaf | TiO 2 | E. coli, S. aureus | Santhoshkumar et al., 2014 |\n| Cynodon dactylon | Leaf | TiO 2 | E. coli | Hariharan et al., 2017 |\n| Glycosmis | Leaf | TiO 2 | S. saprophyticus, B. subtilis, E. coli, cochinchinensis P. aeruginosa | Rosi and Kalyanasundaram, 2018 |\n| Cassia fistula | Leaf | TiO 2 | E. coli, S. aureus | Swathi et al., 2019 |\n\nStatement: The species for Pandanus odorifer is B. subtilis, E. coli.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q88726597fa",
  "kind": "yes/no",
  "text": "Table caption: Mixture design of AAS and AASF concrete (kg/m 3 ).\n| Mixtures | AAS | AASF |\n| Slag | 400 | 200 |\n| Fly ash | 0 | 200 |\n| Activator | 200 | 200 |\n| Aggregate [0–4 mm] | 789 | 789 |\n| Aggregate [4–8 mm] | 440 | 440 |\n| Aggregate [8–16 mm] | 525 | 525 |\n| Admixtures | – | – |\n\nStatement: They have 2 designs in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 }
]
