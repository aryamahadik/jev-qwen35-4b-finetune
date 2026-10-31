# Replay noise screen blind read NS-semtabfacts_sci-blind_read-ff4c38f3-059 (family NS-semtabfacts_sci)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-semtabfacts_sci-blind_read-ff4c38f3-059.json

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
  "qid": "qe25e770890",
  "kind": "yes/no",
  "text": "Table caption: Peptides from L. fermentum HFD1 with predicted antimicrobial activity\n| № | The protein ID | Peptide sequence | ADAM | CAMPR3 | CAMPR3 | CAMPR3 | AMPA |  | Length in peptidome |\n| № | The protein ID | Peptide sequence | ADAM | SVM | Random Forest | DAC | AMPA | Length | Length in peptidome |\n| 1 | QIX58482.1 | MGLIWSLIVGAIIGAIAGAITNRGAAMGWIANIVAGLIGAWIGQGLLGTWGPSLAGMALIPSIIGAIILVLIVSLVVGRTGKK | 1.52 | 1.0 | 0.566 | 0.527 | 0.24 | 84 | 14 |\n| 2 | QIX58771.1 | MLSLITNTVIILLIIGCAFWQLVKVFKRAKKGKCAACDYDCAVKQQVLKQEKHGAQ | 0.82 | 0.889 | 0.6715 | 0.81 | 0.2226 | 56 | N/A |\n| 3 | QIX58909.1 | MAVKIKTPAGMIDIANDVIATVVGGAATDNYGVVGMASRNPLKDGVNQILGRDSFHQGVVIRQQDNGIAVDVYIIVGYGTKISAVSKSVQEKVKYNLEAMLGVTANSVNIMVQGVRVLGD | 0.09 | 1.00 | 0.9855 | 1.0 | 0.248 | 120 | N/A |\n| 4 | QIX58994.1 | MNNQSNVTPQNGNLQYKFCQNCGAKIDVKAVVCPKCGVPVNGNNAESNSEDRNNGWWNLLGFFFPIVGWILWAVWHKEYPKRAHGICVWSWVSFGISFVIGFVNGFLSTL | 1.32 | 1.00 | 0.7745 | 1.0 | 0.237 | 110 | N/A |\n\nStatement: There are seven types of The protein ID.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q61d64eea8c",
  "kind": "yes/no",
  "text": "Table caption: Comparison of computer vision system measurement with simulation results.\n| Parameter | Diffusion theory model | Monte Carlo simulation | Monte Carlo simulation |\n|  |  | Isotropic media ( g = 0) | Anisotropic media ( g = 0.9) |\n| Correlation | 0.9937 | 0.9532 | 0.9867 |\n| RMSE, cm −2 | 0.0947 | 0.1421 | 0.0942 |\n\nStatement: There are two different Comparison of computer vision system measurement with simulation results.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3b54b5470b",
  "kind": "yes/no",
  "text": "Table caption: Estimates for the classic regression model for antisaccade ERR.\n|  | B | SE | t | p |\n| Intercept | −0.02 | 0.07 | −0.22 | 0.83 |\n| DLC intensity | 0.06 | 0.07 | 0.88 | 0.38 |\n| Socio-economic status | −0.22 | 0.10 | −2.35 | 0.02 |\n| Intelligence | −0.18 | 0.07 | −2.44 | 0.02 |\n\nStatement: Intercept and Socio -economic status contains p value as -0.22.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8a5fbfb251",
  "kind": "yes/no",
  "text": "Table caption: Descriptive statistics for main variables of interest – full and reduced sample.\n|  | Full sample (n = 220,823) | Full sample (n = 220,823) | Reduced sample (n = 29,763) | Reduced sample (n = 29,763) |\n|  | Mean (Proportion) | Std. Dev. | Mean (Proportion) | Std. Dev. |\n| Stunted | 0.38 | 0.49 | 0.35 | 0.48 |\n| Education |  |  |  |  |\n| no | 0.31 | 0.46 | 0.27 | 0.45 |\n| primary | 0.15 | 0.35 | 0.14 | 0.34 |\n| secondary | 0.45 | 0.50 | 0.48 | 0.50 |\n| higher | 0.09 | 0.29 | 0.11 | 0.32 |\n| HIV knowledge | – | – | 0.73 | 0.44 |\n| Mosquito net use | 0.42 | 0.49 | 0.42 | 0.49 |\n| Hygiene | 0.33 | 0.47 | 0.37 | 0.48 |\n| Antenatal care visits | 0.81 | 0.39 | 0.83 | 0.37 |\n| Delivery | 0.51 | 0.50 | 0.59 | 0.49 |\n| Child vaccination | 0.12 | 0.33 | 0.16 | 0.37 |\n| Female empowerment | – | – | 0.37 | 0.48 |\n\nStatement: The highest mean value in full sample is 0.12.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3c074012a8",
  "kind": "yes/no",
  "text": "Table caption: Information of the test CFST columns.\n| Sectional shape | Symbol | P (mm) | H (mm) | t (mm) | Ac (mm 2 ) | Nu (kN) | σ u (MPa) | SI | DI |\n| Circular | CC | 503 | 1000 | 2 | 20,106 | 744.9 | 251.8 | 1.00 | 2.169 |\n| Square | CS | 500 | 1000 | 2 | 15,625 | 668.9 | 265.7 | 1.05 | 2.572 |\n| Square with rounded-ended | CSE | 500 | 1000 | 2 | 15,625 | 694.9 | 276.1 | 1.09 | 2.363 |\n| Rhombic | CRH | 500 | 1000 | 2 | 15,000 | 629.3 | 256.2 | 1.01 | 2.264 |\n| Rectangular | CR | 510 | 1000 | 2 | 14,450 | 605.2 | 249.3 | 0.99 | 2.038 |\n| Rectangular with round ended | CRE | 506 | 1000 | 2 | 15,903 | 621.8 | 243.2 | 0.96 | 2.063 |\n| Elliptical | CE | 484 | 1000 | 2 | 15,708 | 607.4 | 243.6 | 0.96 | 1.995 |\n| Hexagonal asymmetric | CHA | 500 | 1000 | 2 | 16,500 | 565.9 | 217.5 | 0.86 | 1.953 |\n| Triangle | CT | 510 | 1000 | 2 | 12,512 | 491.8 | 232.6 | 0.92 | 1.9360 |\n| Pentagram | CP | 500 | 1000 | 2 | 17,205 | 669.7 | 250.8 | 0.99 | 1.818 |\n| Hexagon | CH | 510 | 1000 | 2 | 18,771 | 703.1 | 247.3 | 0.98 | 1.687 |\n| Octagon | CO | 480 | 1000 | 2 | 17,382 | 760.3 | 287.1 | 1.14 | 3.009 |\n| 1/4 circular | CQC | 500 | 1000 | 2 | 15,394 | 596.7 | 239.2 | 0.95 | 2.701 |\n| Semi-circular | CSC | 514 | 1000 | 2 | 15,708 | 554.1 | 217.1 | 0.86 | 2.068 |\n| D-Shaped | CD | 500 | 1000 | 2 | 15735 | 547.2 | 216.5 | 0.85 | 1.926 |\n| Fan-shaped | CF | 500 | 1000 | 2 | 16,897 | 577.7 | 218.7 | 0.86 | 1.722 |\n| L-Shape | CL | 520 | 1000 | 2 | 12,675 | 530.7 | 224.9 | 0.89 | 1.621 |\n| T-Shape | CTS | 500 | 1000 | 2 | 10,000 | 475.4 | 231.1 | 0.91 | 2.0568 |\n| Plus-shaped | CPS | 480 | 1000 | 2 | 8000 | 490.6 | 282.4 | 1.12 | 2.1695 |\n\nStatement: Octagon has highest DI value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4e151ea29a",
  "kind": "yes/no",
  "text": "Table caption: 28-day compressive and tensile strengths of the UHPFRC mixtures in individual layers.\n| Identification | Compressive strength MPa | Compressive strength MPa | Tensile strength MPa | Tensile strength MPa |\n| Identification | Ave | St. dev. | Ave | St. dev. |\n| U0.6 s | 146.7 | 1.5 | 11.7 | 0.8 |\n| U0.3 s 0.3 h | 147.6 | 2.6 | 13.5 | 1.6 |\n| U0.6 h | 147.8 | 3.3 | 11.2 | 1.5 |\n| U1.2 s | 145.3 | 4.0 | 15.1 | 1.0 |\n| U0.6 s 0.6 h | 149.6 | 1.8 | 16.2 | 2.0 |\n| U0.24 s 0.96 h | 153.6 | 2.2 | 17.7 | 1.6 |\n| U1.2 h | 147.7 | 1.2 | 15.7 | 2.3 |\n| U1.6 s | 145.8 | 5.0 | 16.2 | 1.3 |\n| U0.8 s 0.8 h | 142.0 | 4.1 | 16.5 | 1.2 |\n| U1.6 h | 141.2 | 3.8 | 16.3 | 2.0 |\n\nStatement: There are 10 different types of identifications.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8d528bbc92",
  "kind": "yes/no",
  "text": "Table caption: If the points are arranged according to Fig. 16 then each point tests stage movement in predominantly along one stage axis as summarized in this table.\n| Coordinate | Setup | Relocation | Tests |\n| 1 | 4 → 1 | 2 → 1 | −X vs +X |\n| 2 | 1 → 2 | 3 → 2 | −Y vs +Y |\n| 3 | 2 → 3 | 4 → 3 | −X vs +X |\n| 4 | 3 → 4 | 1 → 4 | −Y vs +Y |\n\nStatement: Each coordinate has same setup.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qbac85071f4",
  "kind": "yes/no",
  "text": "Table caption: Definition and interpretation of the nondimensional parameters γ n , n = 1 , 2 , … , 14 in the model (24) – (27) .\n| Parameter definition | Interpretation |\n| γ 1 = λ f q K G f / σ | Relative unit value of effort in fishery. |\n| γ 2 = λ f q β f B f 2 / σ 2 | Impact on fishery price from fishery volume. |\n| γ 3 = B f / K σ | Fishery price saturation parameter for the fishery volume. |\n| γ 4 = λ f q β f a D f 2 / σ 2 | Impact on fishery price from aquaculture volume. |\n| γ 5 = D f / K σ | Fishery price saturation parameter for the aquaculture volume. |\n| γ 6 = λ f w f / σ | Relative unit cost of effort in fishery. |\n| γ 7 = λ a G a K 4 [ r σ K ] 4 | The relative unit value of effort in aquaculture |\n| γ 8 = λ a β a B a 2 4 σ [ r σ K ] 4 | Impact on aquaculture price from aquaculture volume. |\n| γ 9 = B a / K σ | Aquaculture price saturation parameter for the aquaculture volume. |\n| γ 10 = λ a β a f D a 2 4 σ [ r σ K ] 4 | Impact on aquaculture price from fishery volume. |\n| γ 11 = D a / K σ | Aquaculture price saturation parameter for the fishery volume. |\n| γ 12 = λ a w a 2 σ [ r σ K ] 2 | Relative unit cost of effort in aquaculture. |\n| γ 13 = d / K | Remediation capacity parameter. |\n| γ 14 = ρ / K σ | Relative emission rate. |\n\nStatement: The Interpretation for is 14 = / K is Impact on fishery price from aquaculture volume.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q9ec43212a4",
  "kind": "yes/no",
  "text": "Table caption: Bias decomposition of the daily GWR-merged rainfall (in mm), totalized over wet seasons (1 June – 30 September) within 1 January 2015–31 December 2018: P T – gauge accumulated total rainfall; HB - hit bias; AHB - absolute hit bias; MB – miss bias; N AHB – normalized AHB and N MB – normalized MB.\n| Stations | P T = ∑ i= 1 T P g i | CHIRPS | CHIRPS | CHIRPS | MPEG | MPEG | MPEG | CHIRPS | CHIRPS | MPEG | MPEG |\n| Stations | P T = ∑ i= 1 T P g i | HB | AHB | MB | HB | AHB | MB | N AHB | N MB | N AHB | N MB |\n| Adigudem | 1515.2 | −5.2 | 31.4 | 0.0 | −6.6 | 38.3 | 0.0 | 0.02 | 0.00 | 0.03 | 0.00 |\n| Debub | 1666.1 | 7.6 | 76.7 | −0.1 | 4.6 | 18.5 | 0.0 | 0.05 | 0.00 | 0.01 | 0.00 |\n| Dengolat | 2635.6 | 1.4 | 215.4 | −5.3 | −54.2 | 103.1 | −0.9 | 0.08 | 0.00 | 0.04 | 0.00 |\n| Finarawa | 735.9 | 4.4 | 30.6 | −10.7 | 0.0 | 14.0 | 0.0 | 0.04 | −0.01 | 0.02 | 0.00 |\n| Gijet | 1912.1 | 12.4 | 217.5 | −13.7 | 115.9 | 235.6 | −4.3 | 0.11 | −0.01 | 0.12 | 0.00 |\n| Hashenge | 2170.8 | −9.4 | 28.6 | 0.0 | −11.4 | 24.2 | −17.5 | 0.01 | 0.00 | 0.01 | −0.01 |\n| Maichew | 1542.3 | 50.9 | 131.7 | −16.5 | 38.9 | 85.2 | −0.6 | 0.09 | −0.01 | 0.06 | 0.00 |\n| Wedisemero | 2739.4 | 47.4 | 171.7 | −11.1 | 101.7 | 171.6 | −2.7 | 0.06 | 0.00 | 0.06 | 0.00 |\n| Hiwane | 1223.3 | −0.5 | 68.8 | 0.0 | −7.8 | 22.2 | 0.0 | 0.06 | 0.00 | 0.02 | 0.00 |\n| Borra | 1953.0 | −64.7 | 252.8 | −2.5 | −34.1 | 207.5 | 0.0 | 0.13 | 0.00 | 0.11 | 0.00 |\n| AVG | 1809.4 | 4.4 | 122.5 | −6.0 | 14.7 | 92.0 | −2.6 | 0.07 | 0.00 | 0.05 | 0.00 |\n\nStatement: Table have got 17 stations.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q56821467bf",
  "kind": "yes/no",
  "text": "Table caption: Membranes parameters.\n| Membrane code | Membrane type | Length [mm] | Support size OD/ID [mm] | Layer thickness [μm] |\n| Pd1 | Pd–Ag | 220 | 14/7 | 4–5 |\n| Pd2DS | Pd–Ag DS | 191 | 14/7 | 4–5 |\n| Pd3 | Pd–Ag | 90 | 14/7 | 2–3 |\n| CMSM1 | CMSM | 130 | 10/7 | 3.5 |\n| CMSM 2 | CMSM | 145 | 10/7 | 4.2 |\n\nStatement: Table has 7 Different Membrane codes.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q427e3863f0",
  "kind": "yes/no",
  "text": "Table caption: The repeatability variance (s r ), between-day variance (s day ), the time-different intermediate precision (s IP ) and uncertainty values of r h,mode1 (MALS), r h,mode1 (ICP-MS), r h,mode2 (ICP-MS), and mass-based PSD (d 10 , d 50 , d 90 ).\n|  | Size descriptor | Size descriptor | Size descriptor | Size descriptor | Size descriptor | Size descriptor |\n|  | MALS | ICP-MS | ICP-MS | mass-based PSD | mass-based PSD | mass-based PSD |\n|  | r h,mode1 | r h,mode1 | r h,mode2 | d 10 | d 50 | d 90 |\n| Number of replicates | 15 | 15 | 15 | 15 | 15 | 15 |\n| Mean (nm) | 55 | 45 | 127 | 70 | 143 | 268 |\n| sd | 2.1 | 1.9 | 6.6 | 5.8 | 10 | 13 |\n| Min (nm) | 52 | 43 | 117 | 62 | 127 | 251 |\n| Max (nm) | 59 | 50 | 138 | 80 | 159 | 287 |\n| s r | 1.5 | 1.4 | 4.2 | 3.5 | 7.9 | 10.2 |\n| s day | 1.5 | 1.4 | 5.5 | 5.0 | 7.2 | 9.1 |\n| s IP | 2.1 | 2.0 | 6.9 | 6.1 | 10.6 | 13.6 |\n| u r (%) | 2.7 | 3.2 | 3.3 | 5.1 | 5.5 | 3.8 |\n| u day (%) | 2.8 | 3.1 | 4.4 | 7.1 | 5.0 | 3.4 |\n| u IP (%) | 3.9 | 4.4 | 5.8 | 8.8 | 7.4 | 5.1 |\nTable notes: Variance of repeatability (sr), between-day variance (sday), and the time-different intermediate precision (sIP), uncertainty associated to repeatability (ur), uncertainty due to day-to-day variation (uday), and uncertainty associated to intermediate precision (uIP). Mean values of r h,mode1 (MALS), r h,mode1 (ICP-MS), r h,mode2 (ICP-MS), and mass-based PSD (d 10 , d 50 , d 90 ) are presented in bold.\n\nStatement: The Highest MALS r h , mode 1 is 5.1 in Max (nm).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q56fb88c570",
  "kind": "yes/no",
  "text": "Table caption: Material properties of Scotch-Weld™ AF 163-2K epoxy film adhesive.\n| Tensile modulus | E Adh | 2046 MPa a |\n| Poisson ratio | ν Adh | 0.34 b |\n\nStatement: There are two categories epoxy film adhesive.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q70a19060c4",
  "kind": "yes/no",
  "text": "Table caption: Model estimates for the daily survival rate of artificial nests on lake and pond shoreline. Day = exposure day, Habitat = a three-level factor, representing forest (Intercept), lake shoreline and wetland, Field = a two-level factor, representing low %Field (low percentage area of field cover around the nest; Intercept) and high %Field. Random effect standard deviation for Nest ID in Finland = 0.925.\n| Model | Estimate | SE | z-value | P |\n| Finland |  |  |  |  |\n| (Intercept) | 3.487 | 0.500 | 6.965 | < 0.001 |\n| Day | 0.431 | 0.079 | 5.473 | < 0.001 |\n| Habitat: Shoreline | -1.288 | 0.394 | -3.268 | 0.001 |\n| Habitat: Wetland | -0.056 | 0.366 | -0.153 | 0.878 |\n| High %Field | -2.053 | 0.378 | -5.435 | < 0.001 |\n| Denmark |  |  |  |  |\n| (Intercept) | 3.862 | 0.747 | 5.172 | < 0.001 |\n| Day | 0.567 | 0.086 | 6.620 | < 0.001 |\n| Habitat: Shoreline | -1.420 | 0.617 | -2.301 | 0.021 |\n| Habitat: Wetland | -1.664 | 0.626 | -2.658 | 0.008 |\n| High %Field | -1.253 | 0.480 | -2.606 | 0.009 |\n\nStatement: The p value for day Finland and Denmark are same <0.001.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2c70904930",
  "kind": "yes/no",
  "text": "Table caption: Data for allele frequency at five microsatellite loci of Siberian sturgeon Acipenser baerii offspring obtained from a gynogenetic female.\n| Locus | Allele (bp) | Females | Unidentified | Males |\n| Afu-68 | 156 | 0.14 | 0.14 | 0.31 |\n|  | 200 | 0.50 | 0.50 | 0.50 |\n|  | 228 | 0.36 | 0.36 | 0.19 |\n| Aox-45 | 145 | 0.50 | 0.50 | 0.50 |\n|  | 249 | 0.50 | 0.50 | 0.50 |\n| Spl-163 | null allele | 0.00 | 0.14 | 0.15 |\n|  | 188 | 0.03 | 0.14 | 0.00 |\n|  | 192 | 0.29 | 0.14 | 0.25 |\n|  | 196 | 0.00 | 0.11 | 0.16 |\n|  | 200 | 0.36 | 0.29 | 0.33 |\n|  | 204 | 0.32 | 0.21 | 0.11 |\n| Spl-104 | 175 | 0.18 | 0.21 | 0.24 |\n|  | 200 | 0.39 | 0.32 | 0.34 |\n|  | 225 | 0.32 | 0.29 | 0.34 |\n|  | 250 | 0.11 | 0.18 | 0.08 |\n| Spl-106 | null allele | 0.14 | 0.14 | 0.22 |\n|  | 150 | 0.07 | 0.07 | 0.00 |\n|  | 241 | 0.36 | 0.50 | 0.44 |\n|  | 247 | 0.43 | 0.29 | 0.34 |\nTable notes: F-females; U-unidentified; M-males.\n\nStatement: The Aox-45 of Locus has less different Allele of Female.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q84fa8e0192",
  "kind": "yes/no",
  "text": "Table caption: Properties of Oils\n| Property | Servocut ‘S’ [5] | Palm Oil | Peanut Oil |\n| Property | C1 | C2 | C3 |\n| Relative density | 0.877 | 0.924 | 0.92 |\n| Kinematic Viscosity at 40 0 C | 20 cSt | 48 cSt | 42 cSt |\n| Flash Point | 150 0 C | 324 0 C | 315 0 C |\n\nStatement: Palm Oil has the heighest Kinematic Viscosity.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe158291cd7",
  "kind": "yes/no",
  "text": "Table caption: Mix proportion of concrete.\n| Mixture | FA concrete |\n| w/b | 0.4 |\n| water(kg/m 3 ) | 197 |\n| Cement(kg/m 3 ) | 385 |\n| FA(20%)(kg/m 3 ) | 77 |\n| FA(30%)(kg/m 3 ) | 115 |\n| Coarse aggregate (10-16 mm)(kg/m 3 ) | 989 |\n| Fine aggregate(kg/m 3 ) | 765 |\n| Superplasticizer (%) | 2 |\n\nStatement: 385 kg/m^3 is the cement proportion in mixture of concrete.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qde7ed46db1",
  "kind": "yes/no",
  "text": "Table caption: Generalized Additive Model (GAM) results for effects of nitrogen (logN), phosphorus (logP), temperature (T) and salinity (S) on chlorophyll-a (logChl). The table shows Generalized cross-validation (GCV) score, percentage of variance explained (R 2 , %), and Akaike's Information Criterion (AIC) for the full as well as for reduced models (Eq. (5) ). Only models with all terms statistically significant (p < .05) are shown. The best model is marked bold.\n| Predictor functions | GCV | R 2 | AIC |\n| o ( logN t , logP t ) + p ( T t , S t ) | 0.499 | 37.4% | 300.9 |\n| o ( logN t , logP t ) + u( T t ,) | 0.510 | 32.0% | 304.5 |\n| o ( logN t , logP t ) | 0.556 | 23.6% | 316.8 |\n| p ( T t , S t ) | 0.644 | 14.5% | 337.3 |\n| r( logN t ) + p ( T t , S t ) | 0.513 | 32.6% | 305.2 |\n| s( logP t ) + p ( T t , S t ) | 0.571 | 26.5% | 320.1 |\n\nStatement: Each functions has a same number in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf0be89e602",
  "kind": "yes/no",
  "text": "Table caption: Mixture design of AAS and AASF concrete (kg/m 3 ).\n| Mixtures | AAS | AASF |\n| Slag | 400 | 200 |\n| Fly ash | 0 | 200 |\n| Activator | 200 | 200 |\n| Aggregate [0–4 mm] | 789 | 789 |\n| Aggregate [4–8 mm] | 440 | 440 |\n| Aggregate [8–16 mm] | 525 | 525 |\n| Admixtures | – | – |\n\nStatement: The lowest AAS is 0.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qccd8ab7516",
  "kind": "yes/no",
  "text": "Table caption: Confusion matrix for quantifying the performance of a classification model.\n|  | True classes | True classes | True classes | True classes |\n|  |  | Flooding | Non-flooding |  |\n| Predicted classes | Flooding | True positives (TP) | False positives (FP) | Positive predictive rate (PPR) = TP/(TP+FP) |\n|  | Non-flooding | False negatives (FN) | True negatives (TN) | Negative predictive rate (NPR) = TN/(TN+FN) |\n|  |  | True positive rate (TPR) = TP/(TP+FN) | True negative rate (TNR) = TN/(FP+TN) | Accuracy (ACC) = (TN+TP)/(TP+TN+FN+FP) |\n\nStatement: True positive rate is calculated using TPR = TP/(TP+FN)",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q97a9487f1e",
  "kind": "yes/no",
  "text": "Table caption: Prediction accuracy for the Extended LTRM, the LTRM, Random Forest, Boosting, the sample mean, the sample median, and the sample mode. The LTRM outperforms all other methods, but Random Forest and Boosting perform worse than the sample mode. Since the data are simulated the choices for the simulation settings are somewhat arbitrary, and different settings could yield a very accurate or very inaccurate predictive performance (e.g., by adjusting item difficulty and rater competence). Therefore, the absolute prediction error cannot be interpreted and only a relative comparison should be made. Since there were 5 possible outcomes, an accuracy of 0.2 corresponds to chance performance.\n| Method | Dense | Sparse |\n| Extended-LTRM | 0.52 | 0.41 |\n| LTRM | 0.46 | 0.34 |\n| Sample mode | 0.43 | 0.33 |\n| Random Forest | 0.42 | 0.36 |\n| Boosting | 0.41 | 0.35 |\n| Sample median | 0.33 | 0.32 |\n| Sample mean | 0.23 | 0.27 |\n\nStatement: The Random Forest Dense value is 0.11.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2383a33404",
  "kind": "yes/no",
  "text": "Table caption: Requirement table.\n|  | DC 1 | DC 2 | DC 3 | DC 4 | DC 5 | DC 6 | DC 7 |\n| DT 1 | T 4 |  |  |  |  |  |  |\n| DT 2 | T 5 , T 6 | T 5 , T 6 |  |  |  |  | T 5 , T 6 |\n| DT 3 | T 4 | T 4 |  |  |  |  |  |\n| DT 4 | T 1 | T 1 | T 1 | T 1 |  |  |  |\n| DT 5 | T 2 | T 2 |  |  | T 2 | T 2 |  |\n| DT 6 | T 3 | T 3 |  |  |  |  |  |\n\nStatement: The table contains DT 1 TO DT 6",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7389c47dd2",
  "kind": "yes/no",
  "text": "Table caption: FEA observations for beams with different lacings’ diameters\n| Lacings’ diameter (mm) | Yielding load (kN) | Failure load (kN) | Ductility index |\n| 6.0 | 161 | 182.2 | 4.9 |\n| 8.0 | 169 | 185.2 | 4.9 |\n| 10.0 | 175 | 187.4 | 5.13 |\n\nStatement: 5.13 Ductility index for 10.0 LacingsAo diameter (mm).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa1dec45119",
  "kind": "yes/no",
  "text": "Table caption: Participant demographics.\n| Group | Age (years), median (IQR) | % male | FEV 1 (% predicted), median (IQR) | FVC (% predicted), median (IQR) | Pack year history, median (IQR) |\n| Heathy young | 27 (4) | 50 | N/A | N/A | N/A |\n| Healthy elderly | N/A | 50* | N/A | N/A | N/A |\n| COPD | 77.5 (7.25) | 83 | 61.5 (29) | 97.5 (16) | 40 (33) |\nTable notes: Data given as median (interquartile range) where appropriate. Abbreviations: forced expiratory volume in one second, FEV 1 ; forced vital capacity, FVC; not available, N/A. *Data only available for 2 participants\n\nStatement: The % male is no same for both Healthy young and Healthy elderly group.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1f9785560a",
  "kind": "yes/no",
  "text": "Table caption: Physical and mechanical properties of granite dust.\n| № | Specification | Value |\n| 1 | Specific surface, m 2 /kg | 220 … 250 |\n| 2 | Bulk density, kg/m 3 | 920 … 970 |\n| 3 | Clay content, % | 0,2 … 0.5 |\n| 4 | Humidity, % | 0,3 … 0,5 |\n| 5 | Water soluble contaminants, % | none |\n\nStatement: Bulk density, kg/m 3 has the value of 110 ... 170.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf4ca1a4001",
  "kind": "yes/no",
  "text": "Table caption: Details of measuring equipment with accuracy and resolution.\n| variable | unit | Equipment | accuracy | precision |\n| Air temperature | T a (°C) | Testo Ltd, model 453 & 435-2 Alton, Hampshire, UK (high precision probe) | 0.2 °C | 0.1 °C |\n| PCS outlet temperature | T pcs (°C) | Thermistors; Grant Instruments, Cambridge, UK | 0.1 °C | 0.1 °C |\n| Microclimate temperature | T mc (°C) | Thermistors; Grant Instruments, Cambridge, UK & Testo Ltd, model 453 & 435-2 Alton, Hampshire, UK | 0.1/0.2 °C | 0.1 °C |\n| Relative Humidity | rh (%) | Testo Ltd, model 453 & 435-2 Alton, Hampshire, UK & Vaisala | 1 % | 0.1 % |\n| Air speed | m.s −1 | Testo Ltd, model 453 & 435-2 Alton, Hampshire, UK & TSI, Biral, Bristol, UK | 0.03 m s −1 /2% | 0.01 m s −1 |\n| Radiation | W.m −2 | Pyranometer CM11; Kipp & Zonen |  |  |\n| Mean Radiant Temperature | T mrt (°C) | Thermistor, derived from 15 cm Black Globe; Testo Ltd, model 453 using CBE comfort calculator | 0.5 °C | 0.1 °C |\n| Skin Temperature | T sk (°C) | Thermistors; Grant Instruments, Cambridge, UK & iButtons DS1922T | 0.1 °C/0.5 °C (0.2 °C after local calibration) | 0.1 °C/0.06 °C |\n| Tympanic body core temperature | T ty (°C) | ThermoScan Pro 4000, Braun, Germany | 0.2 °C | 0.1 °C |\n| Body Mass | kg | Mettler Toledo model CC150 | 5 g | 1 g |\n| Height | cm | Marsden Stadiometer UK | 0.5 cm | 0.5 cm |\n| Heart Rate | HR | Polar, Tampere, Finland | 2bpm | 1bpm |\n\nStatement: variable Air temperature accuracy is1 g.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q4bf8bb7e44",
  "kind": "yes/no",
  "text": "Table caption: hiPSC based models of RP and associated characteristic phenotypes.\n| Disease | Mutation | Cell type | Phenotype | Reference |\n| XLRP | RPGR | 3D retinal organoids hiPSC-RPE | Mutations perturb RPGR/gelsolin interaction, compromising gelsolin activation (gelsolin controls actin disassembly in connecting cilium, thereby facilitating rhodopsin transport to POS). Mutations affect cilia length and PR number. | ( Megaw et al., 2017 ) ( Deng et al., 2018 ) |\n| XLRP | RP2 | hiPSC-RPE | Complete lack of RP2 protein. IFT20 localization, Golgi cohesion and Gb1 trafficking altered. | ( Schwarz et al., 2015 ) |\n| XLRP | RP2 | 3D retinal organoids | Complete lack of RP2 protein. Reduced levels of Kif7 at cilia tips (involved in stabilizing cilia tips). | ( Schwarz et al., 2017 ) |\n| RP | RP1 | Rod photoreceptors | Decreased number of patient-derived rods in vitro . | ( Jin et al., 2011 ) |\n| RP | RP9 | Rod photoreceptors | Decreased number of patient-derived rods in vitro . Markers for oxidation or endoplasmic reticulum stress. Oxidation is involved in PR degeneration. | ( Jin et al., 2011 ) |\n| RP | PRPH2 | Rod photoreceptors | Decreased number of patient-derived rods in vitro . | ( Jin et al., 2011 ) |\n| RP | RHO | Rod photoreceptors hiPSC-RPE | Decreased number of patient-derived rods in vitro . Markers for oxidation or endoplasmic reticulum stress. Mislocalization of RHO in cytoplasm. | ( Jin et al., 2011 ) ( Jin et al., 2012 ) ( Yoshida et al., 2014 ) |\n| RP | MAK | Retinal progenitor cells | MAK is expressed in the inner segments, cell bodies, and axons of PRs. Loss of retina-specific isoform in mutated cells. | ( Tucker et al., 2011 ) |\n| RP | USH2A | 3D retinal organoids hiPSC-RPE | Upregulation of GRP78 and GRP94. Protein misfolding and ER stress. Organoids: Morphological defects, reduced laminin, defect in retinal progenitor cell development, layer formation RPE: abnormal morphology, lack of pigment foci, and reduced expression of RPE markers | ( Tucker et al., 2013 ) ( Guo et al., 2019 ) |\n| RP | TRNT1 | 3D retinal organoids | Autophagy defect. Accumulation of LC3-II. Elevated level of oxydative stress. | ( Sharma et al., 2017 ) |\n| RP | MFRP | hiPSC-RPE | Disorganized actin, loss of RPE cellular morphology and apical microvilli. | ( Li et al., 2014 ) |\n| RP | MERTK | hiPSC-RPE | Phagocytosis defects. | ( Ramsden et al., 2017 ) |\n| RP | PRPF31 | 3D retinal organoids and hiPSC-RPE | RPE: disrupted epithelium (polarity, TER) Phagocytosis and cilia defects PR: cilia defects, progressive degeneration and cellular stress RPE defects restored by AAV-PRPF31 gene augmentation | ( Buskin et al., 2018 ) ( Brydon et al., 2019 ) |\n| RP | PRPF8 | hiPSC-RPE | Near normal phenotype, no difference regarding phagocytosis | ( Foltz et al., 2018 ) |\n| RP | NRL | 3D retinal organoids | Retinal organoids with S-opsin dominant PR population | ( Kallman et al., 2020 ) |\n| Late onset RP | PDE6B | 3D retinal organoids | At D230 modified expression of genes regulating cGMP hydrolysis leading to elevated cGMP levels in patient cells. | ( Gao et al., 2020 ) |\n\nStatement: There are 12 Disease RP in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8a639dc5eb",
  "kind": "yes/no",
  "text": "Table caption: Descriptive statistics of people's trustworthiness.\n| Items | Obs. | Mean | S.D. | Min. | Max. |\n| Scientists | 531 | 8.10 | 1.98 | 0 | 10 |\n| Government | 530 | 6.16 | 2.61 | 0 | 10 |\n| Politicians | 530 | 3.87 | 2.68 | 0 | 10 |\n| People I know | 529 | 5.39 | 2.68 | 0 | 10 |\n| Traditional news (TV, newspaper, radio) | 530 | 5.59 | 2.74 | 0 | 10 |\n| Facebook | 526 | 4.35 | 2.91 | 0 | 10 |\n| Twitter | 526 | 4.71 | 3.02 | 0 | 10 |\n| YouTube | 525 | 4.35 | 2.88 | 0 | 10 |\nTable notes: Note: The respondents could skip questions they did not want to answer. Therefore, the number of observations varies for each question.\n\nStatement: Min statistics of all items is 0.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf4c0aa13f1",
  "kind": "yes/no",
  "text": "Table caption: Classification results for the heterogeneous population case study with geometric and material differences trained on the labelled source domain and applied to the unlabelled target domain.\n| Method | Method | k NN | JDA |\n| Mapping Training | Accuracy | 16.7% | 100.0% |\n| Mapping Testing | Accuracy | 16.7% | 100.0% |\n\nStatement: There are 3 Methods of Mapping in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3e1cf15806",
  "kind": "yes/no",
  "text": "Table caption: Baseline characteristics – continuous variables are compared with ANOVA, Time from Diagnosis and Triglycerides by Kruskal Wallis test and gender by chi-square.\n|  | Temporal Phenotype | Temporal Phenotype | Temporal Phenotype | p-value |\n|  | A | B | C | p-value |\n| Total Number of Subjects | 191 | 574 | 159 |  |\n| Gender Male - N(%) | 107 (56 %) | 340 (59.1 %) | 94 (59.1 %) | 0.727 |\n| Age - Mean (SD) | 63.99(12.07) | 64.43(9.99) | 66.18(9) | 0.007 |\n| Time from Diagnosis – Median (IQR) | 4.81(13.1) | 7.1(10.3) | 10.1(10.2) | 0.497 |\n| Hba1c - Mean (SD) | 58.63(16.8) | 55.28(15.61) | 54.99(12.79) | 0.547 |\n| BMI - Mean (SD) | 30.27(6.06) | 29.6(4.94) | 28.8(4.54) | 0.288 |\n| Cholesterol - Mean (SD) | 184.94(36.31) | 185.53(31.56) | 186.96(29.24) | <0.001 |\n| Triglycerides - – Median (IQR) | 139(77.8) | 127(63.3) | 119(51.5) | 0.20 |\n| SBP - Mean (SD) | 131.98 (17) | 132.16 (14.12) | 135.4 (14.04) | 0.008 |\n\nStatement: The temporal phenotype B has the highest Total Number of Subjects.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1cb621762d",
  "kind": "yes/no",
  "text": "Table caption: Correlations between HMB and SJ profiles.\n| Date | Correlation Coefficient | P-Value |\n| July 9, 2018 | 0.93 | 0.0 |\n| July 16, 2018 | 0.83 | 0.0 |\n| July 18, 2018 | 0.88 | 0.0 |\n| July 20, 2018 | 0.84 | 0.0 |\n| July 24, 2018 | 0.91 | 0.0 |\n| July 31, 2018 | 0.72 | 0.0 |\n| August 2, 2018 | 0.92 | 0.0 |\n| August 3, 2018 | 0.87 | 0.0 |\n| August 6, 2018 | 0.68 | 0.0 |\n| August 10, 2018 | 0.85 | 0.0 |\n| August 17, 2018 | 0.92 | 0.0 |\n| All dates | 0.79 | 0.0 |\n\nStatement: Correlation Coefficient on date July 31, 2018 has the lowest value of 0.72.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q11a230708b",
  "kind": "yes/no",
  "text": "Table caption: The sample size among different basins and sexes for Walleye Sander vitreus in Lake Erie from the Ontario partnership survey.\n| Basins | Male | Female | Unknown | Total |\n| West Basin | 8027 | 9919 | 6943 | 24,889 |\n| West Central Basin | 6530 | 5834 | 2802 | 15,166 |\n| East Central Basin | 2161 | 2553 | 503 | 5217 |\n| Pennsylvania ridge | 203 | 397 | 58 | 658 |\n| East Basin | 1176 | 1748 | 436 | 3360 |\n| Total | 18,097 | 20,451 | 10,742 | 49,290 |\n\nStatement: East Basin Male is 1748.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcd13d29667",
  "kind": "yes/no",
  "text": "Table caption: Physico-chemical and in vitro properties of RARβ agonist C286 24.\n| LogD a 7.4 | Solubility b µM pH 7.4 | MDCK c Papp ×10 -6 cm/s | MDCK c asymmetry ratio | Cyp450 d IC 50 μM | Human Cl int e µL/min/mg protein |\n| 2.8 | >100 | 28 | 0.8 | >25 | <1 |\nTable notes: For a, b, c, d, e see reference 12. d Cyp450 isoforms 1A2, 2C9, 2C19, 2D6, 3A4.\n\nStatement: The Solubility b M pH 7.4 is >100.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qbbde4ed3e2",
  "kind": "yes/no",
  "text": "Table caption: Baseline characteristics.\n|  | Total n = 73 |\n|  | n |\n| Age (median; IQR) | 63 (55–69) |\n| Number of BMs (%) 1 2 3 4 ≥5 | 38 (52.1) 15 (20.5) 9 (12.3) 4 (5.5) 7 (4.1) |\n| Extracranial metastases present (%) | 45 (61.6) |\n| CA125 (median; IQR) | 38 (9–97) |\n| KPS (median; IQR) | 80 (80–100) |\n| Primary tumour type (%) Ovary Cervix Uterine sarcoma Endometrium Fallopian tube Vulva | 38 (52.1) 5 (6.8) 9 (12.3) 17 (23.3) 2 (2.7) 2 (2.7) |\n| Interval primary diagnosis and BM in months (median; IQR) | 32.07 (16.49–51.98) |\nTable notes: BM = Brain metastasis; IQR = Inter quartile range; KPS = Karnofsky performance status; SRS = stereotactic radiosurgery; WBRT: whole brain radiotherapy.\n\nStatement: Primary tumour type (%) Vulva and Fallopian tube has a lowest value in the total .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc6bcef8603",
  "kind": "yes/no",
  "text": "Table caption: The assessment results of the customized scheme and samples assigned to each module. The average overall accuracy and the average KIA represent mean values of the ten group results of ten-fold cross validation.\n| Item | Overall accuracy of ten-fold cross validation | Average KIA of ten-fold cross validation | The number of samples |\n| 1st Classification | 96.1% | 91.5% | 3069 |\n| 2nd Classification | – | – | – |\n| 3rd Classification | 94.0% | 79.8% | 1874 |\n| 4th Classification | 90.7% | 82.2% | 1581 |\n| 5th Classification | 84.3% | 76.3% | 823 |\n\nStatement: 4th Classification The number of samples is 823.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q838bed8465",
  "kind": "yes/no",
  "text": "Table caption: Frequency of insulation combinations applied by the participants.\n| Combination | Number of houses |\n| Other combinations | 572 |\n| Floor, roof | 566 |\n| Floor, roof, wall | 102 |\n| Floor, roof, wall, window | 1,676 |\n\nStatement: The number of other combination houses are 572.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8f110f3f9e",
  "kind": "yes/no",
  "text": "Table caption: Properties of Steel Fiber.\n| Materials | Specific Gravity | Shape | Length (mm) | Section (mm) | Aspect Ratio (l/d) | Tensile Strength (N/ mm 2 ) |\n| Steel | 7.8 | Hooked End | 35 | dia.- 0.55 | 64 | 1000 |\n\nStatement: Steel Tensile Strength (N/ mm 2 ) is 2589.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qeb4b161fa4",
  "kind": "yes/no",
  "text": "Table caption: NSE of H&A (2018) and DDDUrban for time periods of validation. The NSE of H&A (2018) is the averaged value over the different parameter sets.\n|  | Period | NSE(H&A,2018) | NSE(DDDUrban) |\n| RIS1(S) | 1993–8-1 00:00– 1993–8-1 12:00 | 0.48 | −0.27 |\n| RIS1(S) | 1994–9-28 00:00 – 1994–9-30 00:00 | 0.17 | 0.61 |\n| RIS2(S) | 1995–6-9 00:00 – 1995–6-11 00:00 | 0.21 | 0.80 |\n| RIS2(SA) | 1995–6-1 00:00 – 1995–10-1 00:00 | 0.56 | 0.69 |\n| RIS4(S) | 1998–8-15 12:00– 1998–8-15 20:00 | 0.41 | 0.36 |\n|  | Mean | 0.37 | 0.44 |\n\nStatement: RIS1(S) has value of 1.27 under NSE(DDDUrban)",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa0d3311c67",
  "kind": "yes/no",
  "text": "Table caption: Multivariate threshold nonlinearity tests.\n| Model 1 | Model 1 | Model 1 | Model 1 | Model 2 | Model 2 | Model 2 | Model 2 | Model 3 | Model 3 | Model 3 | Model 3 |\n| d | m 0 | C(d) statistics | P -value | d | m 0 | C(d) statistics | P-value | d | m 0 | C(d) statistics | P-value |\n| 1 | 25 | 186.490 | 0.000 | 1 | 25 | 188.160 | 0.000 | 1 | 25 | 164.240 | 0.000 |\n| 1 | 50 | 174.990 | 0.000 | 1 | 50 | 176.150 | 0.000 | 1 | 50 | 157.070 | 0.000 |\n| 2 | 25 | 172.430 | 0.000 | 2 | 25 | 174.790 | 0.000 | 2 | 25 | 154.080 | 0.000 |\n| 2 | 50 | 188.660 | 0.000 | 2 | 50 | 190.040 | 0.000 | 2 | 50 | 168.210 | 0.000 |\n| 3 | 25 | 173.450 | 0.000 | 3 | 25 | 177.260 | 0.000 | 3 | 25 | 174.110 | 0.000 |\n| 3 | 50 | 188.780 | 0.000 | 3 | 50 | 194.410 | 0.000 | 3 | 50 | 184.250 | 0.000 |\n| 4 | 25 | 121.780 | 0.033 | 4 | 25 | 125.550 | 0.020 | 4 | 25 | 106.660 | 0.195 |\n| 4 | 50 | 120.120 | 0.042 | 4 | 50 | 123.730 | 0.025 | 4 | 50 | 105.140 | 0.224 |\n| 5 | 25 | 136.840 | 0.003 | 5 | 25 | 142.250 | 0.001 | 5 | 25 | 117.300 | 0.060 |\n| 5 | 50 | 131.730 | 0.008 | 5 | 50 | 137.170 | 0.003 | 5 | 50 | 113.370 | 0.096 |\n| γ | 5.561 | AIC | 2440.741 | γ | 5.558 | AIC | 2427.456 | γ | 5.556 | AIC | 3312.632 |\nTable notes: Notes: The AIC refers to the minimum value of Akaike Information Criterion, C(d) statistics is based on the arrangedregression model introduced by Tsay (1998) , d is the delay parameter, m 0 refers to the number of initial observations, and γ represents the optimum values of the threshold variable, magr (the twenty-four month moving average of the IPI growth rate).\n\nStatement: The highest value of m 0 in model 3 is 25.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd482479e31",
  "kind": "yes/no",
  "text": "Table caption: Characterisation of samples used in this study.\n| Approximate activity in VaccZyme ELISA | NIBSC code | Description |  |  |\n| Approximate activity in VaccZyme ELISA | NIBSC code | Description | Kit control a | IS 16/138 |\n| IS 16/138 | NIBSC 16/138 | Pooled anti-Vi IgG sera from 16 volunteers | 631 EU mL −1 b | 100 IU mL −1 b |\n| 10/126 | NIBSC 10/126 | Pooled anti-Vi IgG sera from 9 volunteers | 842 EU mL −1 b | 109 IU mL −1 b |\n| G | NIBSC 16/150 | Post-Typbar TCV vaccination serum | 350 EU mL −1 b | 38 IU mL −1 b |\n| H | NIBSC 16/138 | Pooled anti-Vi IgG sera from 16 volunteers | 631 EU mL −1 b | 97 IU mL −1 b |\n| I | NIBSC 16/144 | Post-Typbar TCV vaccination serum | 345 EU mL −1 b | 25 IU mL −1 b |\n| J | NIBSC 16/146 | Post-Typhim vaccination serum | 524 EU mL −1 b | 62 IU mL −1 b |\n| K | NIBSC 16/148 | Post-Typhim vaccination serum | 150 EU mL −1 c | – |\n| L | NIBSC 16/168 | Post-Typbar TCV vaccination serum | 3876 EU mL −1 c | – |\n| M | NIBSC 16/180 | Post-Typhim vaccination serum | 61 EU mL −1 c | – |\n\nStatement: G has a lowest kit control.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q03c96a3646",
  "kind": "yes/no",
  "text": "Table caption: Themes and categories.\n| Synthesised Finding One Facilitators | Synthesised Finding One Facilitators | Synthesised Finding One Facilitators | Synthesised Finding One Facilitators | Synthesised Finding One Facilitators |\n| Studies | Engaging in exercise | Having Support | Value of taking medications | Lifestyle modification |\n| Attebring et al. (2005) |  |  | ✓ |  |\n| Bryant et al. (2013) |  |  | ✓ |  |\n| Condon & McCarthy (2006) |  | ✓ |  |  |\n| Cooper et al. (2005) | ✓ |  |  |  |\n| Day & Batten (2006) |  |  |  |  |\n| Frohmader et al. (2016) |  | ✓ |  |  |\n| Galdas et al. (2012) |  |  |  |  |\n| Gambling (2003) |  |  |  | ✓ |\n| Gregory, Bostock & Backett-Milburn (2006) |  |  |  |  |\n| Herber et al. (2017) | ✓ | ✓ |  | ✓ |\n| L. Junehag, Asplund, & Svedlund (2014a) | ✓ |  |  |  |\n| L. Junehag, Asplund, & Svedlund (2014 b) |  | ✓ |  |  |\n| Lehane et al. (2008) |  |  | ✓ |  |\n| Little and Lewis (2006) | ✓ |  |  |  |\n| Martin & Woods (2012) | ✓ | ✓ |  |  |\n| McCorry et al. (2009) |  |  |  |  |\n| Tolmie et al. (2009) |  |  |  |  |\n| Traywick & Schoenberg (2008) | ✓ | ✓ |  |  |\n| Webster et al. (2002) |  |  |  |  |\n| White et al. (2010) | ✓ |  | ✓ |  |\n| White et al. (2011) |  |  |  | ✓ |\n| Wyer et al. (2001) | ✓ | ✓ |  | ✓ |\n\nStatement: Value of taking medications is having 4 tick marks in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q709310ef5d",
  "kind": "yes/no",
  "text": "Table caption: Physical properties of fine aggregates used in the study.\n| Property | Fine aggregates | Fine aggregates |\n| Property | Concrete sand | Crushed rock fines |\n| Oven dry particle density (kg/m 3 ) | 2550 | 2600 |\n| Apparent particle density (kg/m 3 ) | 2680 | 2780 |\n| SSD particle density (kg/m 3 ) | 2600 | 2660 |\n| 24h water absorption | 2.0% | 2.6% |\n\nStatement: Property Oven dry particle density (kg/m 3 ) Fine aggregates Concrete sand is 2550.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qecfa054584",
  "kind": "yes/no",
  "text": "Table caption: SDG-network strength statistics\n| Method | EGY SynergyTrade-off | EGY SynergyTrade-off | IDN SynergyTrade-off | IDN SynergyTrade-off | M Synergy | EX Trade-off | TUR SynergyTrade-off | TUR SynergyTrade-off |\n| Method | 30.99 | 25.1 | 43.06 | 24.48 | 37.82 | 29.86 | 41.43 | 30.62 |\n| lcorr | (12.11) | (11.3) | (19.21) | (16.51) | (15.83) | (14.0) | (18.66) | (16.03) |\n|  | [31] | [51] | [40] | [43] | [5] | [32] | [45] | [46] |\n|  | 12.83 | 11.1 | 13.01 | 11.01 | 11.66 | 10.44 | 13.38 | 11.4 |\n| iota | (6.53) | (4.79) | (5.9) | (5.0) | (3.69) | (4.78) | (6.2) | (5.71) |\n|  | [5] | [43] | [4] | [7] | [27] | [13] | [36] | [81] |\n|  | 21.1 | 14.48 | 22.23 | 11.17 | 27.24 | 19.06 | 26.25 | 13.36 |\n| ccm | (15.55) | (10.9) | (16.86) | (10.45) | (17.11) | (11.62) | (19.14) | (11.94) |\n|  | [56] | [68] | [41] | [36] | [23] | [36] | [24] | [36] |\n|  | 1.29 | 0.64 | 1.33 | 0.53 | 1.26 | 0.44 | 1.15 | 0.55 |\n| pcalg | (0.82) | (0.8) | (0.97) | (0.66) | (0.79) | (0.64) | (0.86) | (0.67) |\n|  | [74] | [36] | [16] | [35] | [3] | [19] | [11] | [29] |\n|  | 8.9 | 7.03 | 9.63 | 7.66 | 10.62 | 8.0 | 6.3 | 3.36 |\n| sparsebn | (4.89) | (4.31) | (5.02) | (4.33) | (5.81) | (5.3) | (3.8) | (2.63) |\n|  | [85] | [8] | [15] | [42] | [1] | [70] | [3] | [46] |\nTable notes: Reported connectivity is the average strength (the sum of the weights) of a node’s connections, separated into positive (synergies) and negative (trade-offs) links. Standard deviations are inside round brackets. Nodes with the maximum strength are inside squared brackets.\n\nStatement: EGY SynergyTrade-off in 30.99 of Icorr is (12.11).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8120ee6e3d",
  "kind": "yes/no",
  "text": "Table caption: Physical, optical and electrochemical properties of the T-DPP-Py polymers containing bithiophene (2T), thienothiophene (TT) or thiophene (T) as co-monomer.\n| Polymer | M n [kDa] | M w [kDa] | Đ | E g,opt. [eV] | HOMO [eV] | LUMO [eV] | E g,swv [eV] |\n| 2T-HD | 32.1 | 84.2 | 2.6 | 1.52 | −5.07 | −3.09 | 1.98 |\n| 2T-DT | 69.8 | 146 | 2.1 | 1.53 | −5.09 | −3.05 | 2.04 |\n| TT-HD | 18.5 | 61.1 | 3.3 | 1.50 | −5.08 | −3.15 | 1.93 |\n| TT-DT | 52.8 | 142 | 2.7 | 1.52 | −5.12 | −3.11 | 2.01 |\n| T-HD ( ran. ) | 46.6 | 122 | 2.6 | 1.49 | −5.16 | −3.20 | 1.96 |\n| T-HD ( reg. ) | 93.3 | 249 | 2.7 | 1.49 | −5.19 | −3.20 | 1.99 |\n\nStatement: 5.07 and 5.19 eV for the HOMO and between 3.05 and 3.20 eV for the LUMO.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q19d8d41fcb",
  "kind": "yes/no",
  "text": "Table caption: The repeatability variance (s r ), between-day variance (s day ), the time-different intermediate precision (s IP ) and uncertainty values of r h,mode1 (MALS), r h,mode1 (ICP-MS), r h,mode2 (ICP-MS), and mass-based PSD (d 10 , d 50 , d 90 ).\n|  | Size descriptor | Size descriptor | Size descriptor | Size descriptor | Size descriptor | Size descriptor |\n|  | MALS | ICP-MS | ICP-MS | mass-based PSD | mass-based PSD | mass-based PSD |\n|  | r h,mode1 | r h,mode1 | r h,mode2 | d 10 | d 50 | d 90 |\n| Number of replicates | 15 | 15 | 15 | 15 | 15 | 15 |\n| Mean (nm) | 55 | 45 | 127 | 70 | 143 | 268 |\n| sd | 2.1 | 1.9 | 6.6 | 5.8 | 10 | 13 |\n| Min (nm) | 52 | 43 | 117 | 62 | 127 | 251 |\n| Max (nm) | 59 | 50 | 138 | 80 | 159 | 287 |\n| s r | 1.5 | 1.4 | 4.2 | 3.5 | 7.9 | 10.2 |\n| s day | 1.5 | 1.4 | 5.5 | 5.0 | 7.2 | 9.1 |\n| s IP | 2.1 | 2.0 | 6.9 | 6.1 | 10.6 | 13.6 |\n| u r (%) | 2.7 | 3.2 | 3.3 | 5.1 | 5.5 | 3.8 |\n| u day (%) | 2.8 | 3.1 | 4.4 | 7.1 | 5.0 | 3.4 |\n| u IP (%) | 3.9 | 4.4 | 5.8 | 8.8 | 7.4 | 5.1 |\nTable notes: Variance of repeatability (sr), between-day variance (sday), and the time-different intermediate precision (sIP), uncertainty associated to repeatability (ur), uncertainty due to day-to-day variation (uday), and uncertainty associated to intermediate precision (uIP). Mean values of r h,mode1 (MALS), r h,mode1 (ICP-MS), r h,mode2 (ICP-MS), and mass-based PSD (d 10 , d 50 , d 90 ) are presented in bold.\n\nStatement: The Highest MALS r h , mode 1 is 59 in Max (nm).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8b17ff25c0",
  "kind": "yes/no",
  "text": "Table caption: Operation conditions for Mg and Sr isotope determination with the Plasma II MC-ICP-MS (Nu Instruments).\n| Parameter | Running conditions | Running conditions |\n| Analyte | Mg | Sr |\n| RF power | 1300 | 1300 |\n| Plasma mode | Dry mode, DSN 100 | Wet mode |\n| Auxiliary gas | 0.85–0.9 min −1 | 0.85–0.95 l min −1 |\n| Spray chamber temperature (Peltier) | 5 °C | 5 °C |\n| Nebulizer flow rate | 0.1 ml min −1 | 0.1 ml min −1 |\n| Nebulizer type | MicroMist concentric pyrex nebulizer (GlassExpansion) |  |\n| Cone + skimmer | Ni | Ni |\n\nStatement: Plasma mode for Mg is Wet mode.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcba2a40a66",
  "kind": "yes/no",
  "text": "Table caption: Mechanical properties of T800 carbon fiber/EH104 epoxy laminate.\n| E 11 (GPa) | E 2 (GPa) | G 12 (GPa) | G 13 (GPa) | G 23 (GPa) | v 12 |\n| 170 | 8.6 | 4.8 | 4.8 | 4.5 | 0.3 |\nTable notes: Note: E 11 and E 22 are the elasticity modulus along and vertical to 0° fiber direction, respectively. G 12 and G 13 are the in-plane shear elasticity. G 23 is the out-of-plane shear elasticity. v 12 is the in-plane poisson ratio.\n\nStatement: Elasticity modulus of E11 will be high .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcbcee05050",
  "kind": "yes/no",
  "text": "Table caption: Errors in the solution of Example 1.\n| N | h = π 2 N | E abs | / / . / / 2 | RMS |\n| 10 | 0.702481 | 3.39 × 10 - 6 | 6.55 × 10 - 6 | 1.43 × 10 - 7 |\n| 20 | 0.496729 | 3.90 × 10 - 8 | 1.20 × 10 - 7 | 1.88 × 10 - 8 |\n| 30 | 0.405578 | 2.06 × 10 - 9 | 8.83 × 10 - 9 | 1.13 × 10 - 9 |\n| 40 | 0.351241 | 2.05 × 10 - 10 | 1.04 × 10 - 9 | 1.16 × 10 - 10 |\n| 50 | 0.314159 | 2.86 × 10 - 11 | 1.62 × 10 - 10 | 1.61 × 10 - 11 |\n\nStatement: E abs has only five data values under it.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q09e8a88bb5",
  "kind": "yes/no",
  "text": "Table caption: Participant demographics.\n| Group | Age (years), median (IQR) | % male | FEV 1 (% predicted), median (IQR) | FVC (% predicted), median (IQR) | Pack year history, median (IQR) |\n| Heathy young | 27 (4) | 50 | N/A | N/A | N/A |\n| Healthy elderly | N/A | 50* | N/A | N/A | N/A |\n| COPD | 77.5 (7.25) | 83 | 61.5 (29) | 97.5 (16) | 40 (33) |\nTable notes: Data given as median (interquartile range) where appropriate. Abbreviations: forced expiratory volume in one second, FEV 1 ; forced vital capacity, FVC; not available, N/A. *Data only available for 2 participants\n\nStatement: The FEV 1, FVC and Pack year history data is available for both Healthy young and Healthy elderly group.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q65473df5ed",
  "kind": "yes/no",
  "text": "Table caption: Classification results for the heterogeneous population case study mapping from a physics-based model to experimental structure trained on the labelled source domain and applied to the unlabelled target domain.\n| Method | Method | k NN | JDA |\n| Target | Accuracy | 48.0% | 88.0% |\n\nStatement: k NN has the value of 11.0%.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1e29e43fb0",
  "kind": "yes/no",
  "text": "Table caption: Summary of the 2-way crossed SIMPER results for the comparison of the species assemblage between sampling areas. Average abundance of discriminating species in each sampling area, foundation and control, their contribution (%) to the dissimilarity between sampling areas, and cumulative total (%) of contributions. Listed taxa contributed to at least 80% of the dissimilarity between the foundations and controls.\n| Species | Abundance | Abundance | Contribution | Cumulative |\n| Species | Foundations | Controls | Contribution | Cumulative |\n| Cancer pagurus | 1.39 | 0.11 | 16.71 | 16.71 |\n| Pagurus spp. | 1.13 | 0.28 | 12.03 | 28.74 |\n| Marthasterias glacialis | 1.04 | 0.08 | 10.61 | 39.35 |\n| Astropecten irregularis | 0.48 | 0.94 | 9.42 | 48.77 |\n| Gadus morhua (juv.) | 0.79 | 0.21 | 6.52 | 55.29 |\n| Liocarcinus depurator | 0.54 | 0.28 | 6.35 | 61.64 |\n| Asterias rubens | 0.47 | 0.03 | 4.93 | 66.57 |\n| Ctenolabrus rupestris | 0.45 | 0 | 4.04 | 70.61 |\n| Hyas araneus | 0.29 | 0.05 | 3.67 | 74.28 |\n| Ophiuroidea | 0.45 | 0.01 | 3.41 | 77.69 |\n| Pomatoschistus spp. | 0.13 | 0.2 | 2.72 | 80.4 |\n| Average dissimilarity |  |  |  | 81.56 |\n\nStatement: The Contribution ranges from 2.72 to 16.71.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 }
]
