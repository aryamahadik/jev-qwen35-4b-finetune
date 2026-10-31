# Replay noise screen blind read NS-semtabfacts_sci-blind_read-d5837be9-013 (family NS-semtabfacts_sci)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-semtabfacts_sci-blind_read-d5837be9-013.json

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
  "qid": "q9a7c9387c1",
  "kind": "yes/no",
  "text": "Table caption: The sample size among different basins and sexes for Walleye Sander vitreus in Lake Erie from the Ontario partnership survey.\n| Basins | Male | Female | Unknown | Total |\n| West Basin | 8027 | 9919 | 6943 | 24,889 |\n| West Central Basin | 6530 | 5834 | 2802 | 15,166 |\n| East Central Basin | 2161 | 2553 | 503 | 5217 |\n| Pennsylvania ridge | 203 | 397 | 58 | 658 |\n| East Basin | 1176 | 1748 | 436 | 3360 |\n| Total | 18,097 | 20,451 | 10,742 | 49,290 |\n\nStatement: East Basin Male is 1748.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc11bd1e8e6",
  "kind": "yes/no",
  "text": "Table caption: Output parameters from the parametric optimisation (Eq. ( )), for varying envelope widths δ when finding the optimal length ( L ), width ( W ), flange thickness ( F ), web thickness ( T ) and corner depth ( C ). Units are pixels in the images in .\n|  | Initial | δ = 2 | δ = 10 | δ = 20 | δ = 28 |\n| L | 80 | 80 | 83 | 82 | 69 |\n| W | 50 | 50 | 45 | 47 | 45 |\n| F | 9 | 9 | 9 | 4 | 5 |\n| T | 18 | 18 | 17 | 22 | 25 |\n| C | 1 | 2 | 2 | 5 | 4 |\n| E LL ∗ | 3.08 | 3.73 | 3.76 | 5.01 | 5.21 |\n\nStatement: At = 10 L has highest value 83 .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qddd11110b5",
  "kind": "yes/no",
  "text": "Table caption: Synaptic conductance (g) between pyramidal and interneuron population.\n| Neuronal signal transmission direction | NMDA | GABA |\n| TPN pyramidal → TPN pyramidal | 0.0001905 | / |\n| TPN pyramidal → TPN interneuron | 0.0001460 | / |\n| TPN interneuron → TPN pyramidal | / | 0.0006681 |\n| TPN interneuron → TPN interneuron | / | 0.0005120 |\n| TNN pyramidal → TNN pyramidal | 0.0001905*4 | / |\n| TNN pyramidal → TNN interneuron | 0.000146*4 | / |\n| TNN interneuron → TNN pyramidal | / | 0.0006681*1.5 |\n| TNN interneuron → TNN interneuron | / | 0.000512*1.5 |\n| TPN pyramidal → TNN pyramidal | k5/4096*0.001 | / |\n| TPN pyramidal → TNN interneuron | k5/4096*0.001 | / |\n| TNN pyramidal → TPN pyramidal | 60/4096*0.001 | / |\n| TNN pyramidal → TPN interneuron | 60/4096*0.001 | / |\n\nStatement: 60/4096*0.001 NMDA is TNN pyramidal TPN interneuron.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q091922ca95",
  "kind": "yes/no",
  "text": "Table caption: Associations of exercise frequency (last 30 days) with frequent symptoms of depression/anxiety (n = 18,429)\n| Exercise frequency | Crude Model | Crude Model | Crude Model | Model 2 | Model 2 | Model 2 | Model 3 | Model 3 | Model 3 |\n| Exercise frequency | OR | 95% CI | p | OR | 95% CI | p | OR | 95% CI | p |\n| Never/Sometimes | 1 | - | - | 1 | - | - | 1 | - | - |\n| 1-2 times/week | 0.66 | 0.61–0.71 | <0.001 | 0.66 | 0.58–0.76 | <0.001 | 0.73 | 0.64–0.81 | <0.001 |\n| ≥3 times/week | 0.56 | 0.52–0.60 | <0.001 | 0.58 | 0.51–0.66 | <0.001 | 0.74 | 0.66–0.83 | <0.001 |\nTable notes: Model 2 adjusted for: age, gender, smoking status, BMI, use of pain medication, exercise-gender interaction. Model 3 adjusted for Model 2 co-variates plus leisure-time sedentary behavior. OR= Odds Ratio; CI = Confidence Interval.\n\nStatement: 3 times/week frequency exercise in Model 3 OR is 0.74.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qefa6270397",
  "kind": "yes/no",
  "text": "Table caption: Structural Efficiency of Burnt bricks.\n| Samples | Density (kg/m 3 ) | Compressive Strength (N/mm 2 ) | Shear Stress (N/mm 2 ) | Structural Efficiency (x 10 3 m) |\n| P 0 & T 0 | 1376 | 6.15 | 2.33 | 4.47 |\n| P 1 | 1376 | 4.02 | 2.99 | 2.92 |\n| P 2 | 1376 | 3.57 | 2.98 | 2.59 |\n| P 3 | 1354 | 3.16 | 2.99 | 2.33 |\n| P 4 | 1322 | 2.82 | 2.99 | 2.13 |\n| P 5 | 1322 | 2.61 | 2.97 | 1.97 |\n| T 1 | 1376 | 6.67 | 2.54 | 4.84 |\n| T 2 | 1376 | 7.78 | 3.00 | 5.65 |\n| T 3 | 1376 | 8.97 | 3.01 | 6.52 |\n| T 4 | 1376 | 10.16 | 3.01 | 7.40 |\n| T 5 | 1376 | 11.02 | 3.02 | 8.01 |\n\nStatement: Structural Efficiency (x 10 3 m) of T 5 is having highest of 8.01.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q290b7864f4",
  "kind": "yes/no",
  "text": "Table caption: Exploratory factor analysis for the measures of response inhibition ( N = 179).\n| Measure | Factor loading | Uniqueness |\n| Antisaccade ERR | 0.15 | 0.98 |\n| Stroop ERR | 0.28 | 0.92 |\n| Stroop RT | 0.57 | 0.68 |\n| No-go ERR | 0.36 | 0.87 |\n| SSRT | – | 0.99 |\n\nStatement: The value given for Factor loading in SSRT is 0.13.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa2f354db16",
  "kind": "yes/no",
  "text": "Table caption: Be concentrations (mg/kg) in eluates from the 7-step sequential extraction of core P4 at five depths. The seven steps represent the: 1) water soluble phase; 2) exchangeable phase; 3) easily reducible minerals; 4) resistant reducible minerals; 5) easily oxidizable minerals (e.g. secondary sulfides); 6) resistant oxidizable minerals (e.g. primary sulfides); and 7) residues and silicates. The zones are based on what was presented in Fig. 1 .\n| Zone | Depth | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 | Step 7 |\n| 1 | −30 | 1 | 3.3 | 5.4 | 27.8 | 0.8 | 40.9 | 174 |\n| 2 | −150 | 2.2 | 6.7 | 6.2 | 25.7 | 0.5 | 37.2 | 195 |\n| 4 | −250 | 0.5 | 5.3 | 5.1 | 39.6 | 0.9 | 41.0 | 169 |\n| 5 | −360 | 0.5 | 2.5 | 3.9 | 19.3 | 0.5 | 38.6 | 133 |\n| 6 | −530 | 0.5 | 2.1 | 4.3 | 30.6 | 0.7 | 37.5 | 148 |\n\nStatement: There are 8 Zone in the Table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3274dca0b9",
  "kind": "yes/no",
  "text": "Table caption: Results from the Cox proportional hazards model.\n| Variable | HR (95% CI) | p |\n| Age | 1.05 (1.01–1.09) | 0.03 |\n| Number of BMs | 1.12 (0.97–1.29) | 0.14 |\n| Extracranial metastases present | 1.58 (0.85–2.95) | 0.15 |\n| CA-125 * | 1.02 (1.01–1.03) | <0.01 |\n| KPS | 1.00 (0.98–1.02) | 0.74 |\n| Primary tumour type Ovary ** Cervix Uterine sarcoma Endometrium Fallopian tube Vulva | – 1.71 (0.33–8.90) 3.07 (1.12–8.42) 1.93 (0.95–3.94) 0.51 (0.06–4.06) 8.70 (1.19–63.34) | – 0.52 0.03 0.07 0.52 0.03 |\n| Interval primary diagnosis and BM | 1.00 (0.99–1.01) | 0.64 |\nTable notes: BM = Brain metastases; KPS = Karnofsky Performance Status.\n\nStatement: The Primary tumour type Ovary doesn't contain any value for HR and p.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qbf97d16b85",
  "kind": "yes/no",
  "text": "Table caption: Material constants for 5182-O aluminum alloy and parameters used in this study.\n| Elastic constants [GPa] (Voigt notation) | C 11 = 108.2 C 12 = 61.3 C 44 = 28.5 |\n| Reference shear rate, γ ̇ 0 [s −1 ] | 0.5 |\n| Strain rate sensitivity factor, m | 0.005 |\n\nStatement: A fixed strain sensitivity factor ( m ) of 0.005 was chosen because the strain sensitivity of aluminum alloy is generally low.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q22bd8d59a6",
  "kind": "yes/no",
  "text": "Table caption: Area coverage (million ha) of land cover types, as well as their equivalent biomes and corresponding ecosystem services value coefficients (ESV in US$ ha −1 year −1 , 2007 price levels), based on global value coefficients adopted from the work of de Groot et al. (2012) and Costanza et al. (2014) .\n| Land cover | Area (million ha) | Area (million ha) | Area (million ha) | Equivalent biome | ESV (US$ ha −1 year −1 ) |\n| Land cover | 1992 | 2000 | 2015 | Equivalent biome | ESV (US$ ha −1 year −1 ) |\n| Cropland | 425 | 439 | 445 | Cropland | 5568 |\n| Evergreen forest | 203 | 200 | 198 | Tropical forest | 5263 |\n| Deciduous forest | 447 | 445 | 453 | Tropical forest | 5263 |\n| Shrubland | 470 | 461 | 450 | Woodlands | 1588 |\n| Grassland | 298 | 299 | 299 | Grasslands | 2872 |\n| Wetland | 46 | 47 | 47 | Inland wetlands | 25,681 |\n| Urban | 2 | 2 | 4 | Urban | – |\n| Bareland | 444 | 444 | 439 | Desert | – |\n| Waterbodies | 30 | 30 | 30 | Rivers/lakes | 4267 |\n\nStatement: Biome for Evergreen forest and Decidious forest are not same.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5aacfbf78d",
  "kind": "yes/no",
  "text": "Table caption: Description of the evaluated coils.\n|  | Coil Parameters | Coil Parameters | Coil Parameters | Coil Parameters | MR System | MR System |\n|  | Type | Geometry | T/R Mode | Manufacturer | Brand | Location |\n| Coil #1 | Volume | Birdcage | Tx-Rx | RAPID Gmbh | Siemens | Copenhagen, DK |\n| Coil #2 | Volume | Birdcage | Tx-Rx | RAPID Gmbh | GE | Cambridge, UK |\n| Coil #3 | Volume | Helmholtz | Tx-Rx | Pulsteq | GE | Aarhus, DK |\n| Coil #4 | Surface | 8-CH Array | Rx-Only | GE | GE | Aarhus, DK |\n| Coil #5 | Surface | 16-CH Array | Rx-Only | RAPID Gmbh | GE | Aarhus, DK |\n| Coil #6 | Surface | 14-CH Array | Rx-Only | HYPERMAG | GE | Aarhus, DK |\n| Coil #7 | Surface | Single Loop | Rx-Only | HYPERMAG | GE | Aarhus, DK |\n\nStatement: There are seven Coil ranges Coil #1 to Coil #7.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd2839f087e",
  "kind": "yes/no",
  "text": "Table caption: Standardized regression coefficients and standard errors (in parentheses) on trait and method factors in the MIMIC models.\n|  | Trait factors | Trait factors | Trait factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors | Trait-specific method factors |\n|  | Self-report (S) | Self-report (S) | Self-report (S) | Teacher report (T) | Teacher report (T) | Teacher report (T) | Mother report (M) | Mother report (M) | Mother report (M) | Father report (F) | Father report (F) | Father report (F) |\n|  | EMO-S | SOC-S | ASC-S | EMO-T | SOC-T | ASC-T | EMO-M | SOC-M | ASC-M | EMO-F | SOC-F | ASC-F |\n| Gender | 0.262 ⁎⁎⁎ (0.039) | 0.078 (0.045) | 0.029 (0.044) | 0.235 ⁎⁎⁎ (0.047) | 0.209 ⁎⁎⁎ (0.047) | −0.011 (0.051) | 0.137 ⁎ (0.060) | 0.137 ⁎ (0.062) | 0.070 (0.063) | 0.044 (0.068) | 0.134 (0.070) | 0.034 (0.072) |\n| SEN | −0.023 (0.040) | −0.100 ⁎⁎ (0.041) | −0.169 ⁎⁎⁎ (0.035) | −0.217 ⁎⁎⁎ (0.043) | −0.295 ⁎⁎⁎ (0.045) | −0.425 ⁎⁎⁎ (0.041) | −0.063 (0.068) | −0.150 ⁎ (0.066) | −0.370 ⁎⁎⁎ (0.058) | −0.085 (0.075) | −0.189 ⁎ (0.076) | −0.425 ⁎⁎⁎ (0.068) |\nTable notes: Note . EMO = emotional inclusion, SOC = social inclusion, ASC = academic self-concept. SEN = special educational needs. Coding: gender 0 = male, 1 = female; SEN 0 = without SEN, 1 = with SEN.\n\nStatement: The table has been divided into two factors - Trait factors and Trait-specific method factors.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf25711a0dd",
  "kind": "yes/no",
  "text": "Table caption: Performance of the AL in the case hospital calculated with our deterministic model (case hospital data, 2015–2017, n = 7565).\n| Beds | Rejected hours (%) | Rejected days (%) | Occupancy (%) |\n| 1 | 25.1 | 71.4 | 82.9 |\n| 2 | 12.3 | 41.9 | 65.5 |\n| 3 | 5.1 | 20.4 | 51.8 |\n| 4 | 2.9 | 8.1 | 41.4 |\n| 5 | 0.4 | 2.1 | 33.9 |\n| 6 | 0 | 0.2 | 28.4 |\n| 7 | 0 | 0 | 24.3 |\n\nStatement: Bed 7 has zero rejected hours and zero rejected days percentage.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3d324085e0",
  "kind": "yes/no",
  "text": "Table caption: Results of the bootstrapping method for mediation.\n| Effects | Effects | Coefficient | Boot SE | 95% biased corrected confidence interval | 95% biased corrected confidence interval | Results |\n| Effects | Effects | Coefficient | Boot SE | LL | UL | Results |\n| Indirect effect | NSRTI- > STD - > QOL | 0.06 | 0.019 | 0.031 | 0.108 | Partial Mediation |\n| Direct effect | NSRTI - > QOL | 0.15∗∗ | 0.45 | 0.064 | 1.243 | – |\nTable notes: Note : ∗∗p < 0.005, NSRID, NSR Infrastructural development, STD, sustainable tourism development, QOL, Quality of life.\n\nStatement: Indirect effect will have 0.06 Coefficient.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf3649aa4e9",
  "kind": "yes/no",
  "text": "Table caption: Basic descriptives of three types of traders at produce lane.\n| Variables | Retail | Retail & Wholesale | Wholesale |\n| Total number | 51 | 12 | 29 |\n| Gender (% male) | 6.0% | 7.7% | 76.0% |\n| Age | 38.64 (11.91) | 43.13 (7.30) | 43.92 (10.09) |\n| Education (in years) | 8.67 (3.93) | 9.46 (3.78) | 8.75 (2.61) |\n| No of years on produce lane | 4.33 (2.60) | 11.00 (5.89) | 12.06 (5.95) |\n| No of people in one store | 3.83 (1.70) | 1.56 (0.73) | 1.71 (1.12) |\n| Average rent pp/month (USD) | 25.74 (12.52) | 62.56 (25.14) | 78.63 (41.04) |\n| Capacity of store (tons) | 34.00 (29.84) | 32.46 (26.20) | 47.00 (43.09) |\n| Average capacity pp (tons) | 8.62 (4.45) | 29.06 (28.50) | 42.18 (45.82) |\n\nStatement: There is no value for Capacity of store (tons).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q687188740e",
  "kind": "yes/no",
  "text": "Table caption: Genome assembly and gene annotation of major fishes in world fisheries and aquaculture .\n| Common name | Chromosome number (2n) | Genome size (Mb) | Scaffold N50 (Mb) | Coverage | %GC | Number of genes | Number of protein-coding genes | Sequencing platforms | Reference |\n| Asian seabass | 48 | 668.5 | 25.8 | 170x | 40.8 | 30,687 | 22,184 | Illumina, PacBio |  |\n| Atlantic cod | 46 | 824.3 | 0.5 | 40x | 46.3 | 22,154 | 20,095 | Roche 454 GS FLX Titanium | ; |\n| Atlantic salmon | 58 | 2966.9 | 3.0 | 220x | 43.9 | 46,598 | 37,206 | Sanger, Illumina, PacBio |  |\n| Channel catfish | 58 | 771.9 | 7.7 | 167x | 31.5 | 30,530 | 26,661 | Roche 454 FLX Titanium, Illumina GaIIx | ; |\n| Common carp | 100 | 1713.7 | 1.0 | 229x | 37.3 | 52,610 | 47,795 | Roche 454, IlluminaHiSeq 2000and SOLiD | ; |\n| European seabass | 48 | 675.9 | 5.1 | 30x | 40.4 | 26,719 | – | Sanger, Roche 454, Illumina GAIIx |  |\n| Grass carp | 48 | 1076.2 (m) 900.5 (f) | 2.3 (m) 6.5 (f) | 110x (m) 95x (f) | 37.4 | 28,842 | 27,263 | Sanger, Illumina GAIIx |  |\n| Japanese flounder | 48 | 546.0 | 3.9 | 120x | 43.2 | 22,751 | 21,787 | Illumina, Hiseq 2000 |  |\n| Nile tilapia | 46 | 1005.7 | 2.8 | 269x | 40.7 | 24,559 | 21,437 | PacBio |  |\n| Northern snakehead | 48 | 644.4 | 4.5 | 125x | 39.9 | – | 19,877 | Illumina, Hiseq 2000 |  |\n| Pacific bluefin tuna | 56 | 684.5 | 7.9 | 252x | 39.7 | – | 26,433 | Roche 454, Illumina GaIIx, PacBio |  |\n| Rainbow trout | 58 | 2179.0 | 0.4 | 70x | 43.5 | 30,687 | 22,184 | Sanger Roche 454, Illumina GaIIx, HiSeq 2000 |  |\n| Tongue sole | 42 | 470.2 | 0.9 | 212x | 41.3 | 22,352 | 21,516 | Sanger Illumina NGS |  |\n| Turbot | 42 | 568.0 | 4.3 | 219x | 43.4 | 28,189 | 22,751 | Illumina GAIIx and HiSeq 2000 |  |\n\nStatement: There are 5 Sequencing platforms.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q599abb60e6",
  "kind": "yes/no",
  "text": "Table caption: disk diffusion method using CLSI guidelines (PIP/TAZ-Piperacillin Tazobactam, CEF-Ceftazidime, MER-Meropenem, GEN-Gentamicin, CIP-Ciprofloxacin) (R-resistant; S- susceptible; I- Intermediate), Zone diameter interpretive criteria in mm according to CLSI guidelines (PIP/TAZ- ≥21 (S), 15–20 (I), ≤14 (R) ; CEF- ≥18 (S), 15–17 (I), ≤14 (R) ; MER- ≥19 (S), 16–18 (I), ≤15 (R) ; GEN- ≥15 (S), 13–14 (I), ≤12 (R) ; CIP- ≥21 (S), 16–20 (I), ≤15 (R)).\n| Isolates | PIP/TAZ | CEF | MER | GEN | CIP |\n| VIT PC CL-7 | 12 mm (R) | 17 mm (I) | 12 mm (R) | ≤12 mm (R) | 8 mm (R) |\n| VIT PC CL-9 | 14 mm (R) | <13 mm (R) | ≤12 mm (R) | ≤12 mm (R) | 18 mm (I) |\n\nStatement: MER will have Low diameter for VIT PC CL-7 Isolates.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q91b5d3c0e0",
  "kind": "yes/no",
  "text": "Table caption: Correlations between HMB and SJ profiles.\n| Date | Correlation Coefficient | P-Value |\n| July 9, 2018 | 0.93 | 0.0 |\n| July 16, 2018 | 0.83 | 0.0 |\n| July 18, 2018 | 0.88 | 0.0 |\n| July 20, 2018 | 0.84 | 0.0 |\n| July 24, 2018 | 0.91 | 0.0 |\n| July 31, 2018 | 0.72 | 0.0 |\n| August 2, 2018 | 0.92 | 0.0 |\n| August 3, 2018 | 0.87 | 0.0 |\n| August 6, 2018 | 0.68 | 0.0 |\n| August 10, 2018 | 0.85 | 0.0 |\n| August 17, 2018 | 0.92 | 0.0 |\n| All dates | 0.79 | 0.0 |\n\nStatement: P-Value is same for All dates of 0.0.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q140443ed7b",
  "kind": "yes/no",
  "text": "Table caption: Dosimetric parameters for FS-HDR-BT plans and MR-Linac plans for a single, 19 Gy dose prescription to the CTV and PTV respectively. *CTV for FS-HDR-BT and PTV for MR-Linac.\n|  |  | FS-HDR-BT | FS-HDR-BT | MR-Linac | MR-Linac |  |\n| Parameter | Reference dose | Median (n = 30) | Range | Median (n = 30) | Range | p-value |\n| Target coverage |  |  |  |  |  |  |\n| D95% CTV/PTV* | ≥19 Gy | 18.8 Gy | 14.0–21.7 Gy | 19.0 Gy | 15.5–21.7 Gy | 0.053 |\n| D90% CTV/PTV* | ≥17 Gy | 20.3 Gy | 15.9–23.8 Gy | 20.2 Gy | 16.7–22.6 Gy | 0.484 |\n| High dose volumes |  |  |  |  |  |  |\n| V100% CTV/PTV* | – | 95% | 73–99% | 95% | 69–100% | 0.894 |\n| V150% CTV/PTV* | – | 55% | 25–77% | 1% | 0–38% | <0.001 |\n| V200% CTV/PTV* | – | 25% | 9–54% | 0% | 0–0% | <0.001 |\n| OAR dose |  |  |  |  |  |  |\n| Urethra D10% | <17.7 Gy | 16.0 Gy | 6.7–18.2 Gy | 17.5 Gy | 8.2–17.7 Gy | <0.001 |\n| Rectum D1cm 3 | <12 Gy | 10.2 Gy | 4.1–12.0 Gy | 12.0 Gy | 9.4–12.0 Gy | <0.001 |\n| Rectum D2cm 3 | – | 8.6 Gy | 1.6–10.8 Gy | 10.7 Gy | 8.4–11.3 Gy | <0.001 |\n| Bladder D1cm 3 | <12 Gy | 8.5 Gy | 1.8–12.1 Gy | 8.4 Gy | 0.4–12.0 Gy | 0.102 |\n| Bladder D2cm 3 | – | 7.0 Gy | 1.6–10.8 Gy | 6.6 Gy | 0.5–11.1 Gy | 0.090 |\n\nStatement: The value of range is 1.6Ai10.8 Gy for both Rectum D2cm 3 and Bladder D2cm 3.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcbc4e26999",
  "kind": "yes/no",
  "text": "Table caption: Descriptions of variables in the geolocation_data worksheet\n| No | Name | Description | Code | Measure | Unit | Source |\n| 1 | Identity | Unique ID to each irrigation network component. The ID is the official nomenclature from Klambu Wilalung Irrigation District. | ID |  |  | Official data |\n| 2 | Name | The name of each irrigation network component | name |  |  | Official data |\n| 3 | Type a | The type of component in the irrigation network (1=structure, 2=canal) | type | Nominal |  | Official data |\n| 4 | Status | The status of irrigation network components. For structures (1=main structures, 2=supporting structures). For canals (1=primary canal, 2=secondary canal). | stat | Nominal |  | Official data |\n| 5 | X Coordinate b | The Easting coordinate in UTM Projection System | X |  |  | Official data |\n| 6 | Y Coordinate b | The Northing coordinate in UTM Projection System | Y |  |  | Official data |\n| 7 | WUA | The WUA for which each irrigation network components situated |  |  |  | Enumeration |\n| 8 | Village | The village for which each irrigation network components situated |  |  |  | Enumeration |\nTable notes: Note:\n\nStatement: The source is differentiated into official data and enumeration.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf2927ed782",
  "kind": "yes/no",
  "text": "Table caption: Different specifications of structural causal models\n| Structural causal model | X i = f i X P A i , N i |\n| Additive noise model | X i = f i X P A i + N i |\n| Causal additive model | X i = ∑ k ∈ P A i f i k X k + N i |\n| Linear Gaussian model | X i = ∑ k ∈ P A i β i k X k + N i and N i ∼ N 0 , σ i |\nTable notes: Based on Table 7.1 from Peters et al. [ ]. Other popular specifications are nonlinear Gaussian additive noise models and linear non-Gaussian acyclic models, among others.\n\nStatement: Causal additive model specifications X i = k P A i f i k X k + N i.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q468ebe58cd",
  "kind": "yes/no",
  "text": "|  | Mean | SD | Minimum | Maximum |\n| SIAS | 25.96 | 15.78 | 6 | 71/80 |\n| BFNE | 38 | 12.23 | 13 | 60/60 |\n| STAI | 42.59 | 12.33 | 24 | 73/80 |\n| AQ | 8.87 | 5.30 | 1 | 22/33 |\n| BFI Extraversion | 3.37 | 1.06 | 1.25 | 5/5 |\n| BFI Agreeableness | 2.83 | 0.72 | 1 | 4.5/5 |\n| BFI Conscientiousness | 3.77 | 0.65 | 2.25 | 5/5 |\n| BFI Neuroticism | 3.45 | 0.88 | 1 | 5/5 |\n| BFI Openness | 4.10 | 0.66 | 1.8 | 5/5 |\n\nStatement: BFNE Mean is 38.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qee533c3477",
  "kind": "yes/no",
  "text": "Table caption: Multiple QAP regressions with similarity in cobranding as the dependent variable.\n|  | Model 1 | Model 2 |\n| Intercept | 4.02** | .143** |\n| Decreasing network distance (DND) | .388 (.182)** [H1] | .027 (.013) |\n| DND 2 | –.106 (−.046) | –.065 (−.028) |\n| Difference in closeness (DCL) | –.105 (−.202)** | –.109 (−.209)** |\n| Structural equivalence | –.354 (−.032) | .324 (.029) |\n| Same destination dummy | –.184 (−.043) | –.124 (−.029) |\n| Combined closeness (CCL) |  | .063 (.201)** [H2] |\n| CCL × DCL |  | –.014 (−.103)* |\n| R-square | .066 | .101 |\n| Adjusted R-square | .063 | .098 |\nTable notes: The number of dyads is 990, *p < .10, **p < .05, conservative two-tailed tests (standardized beta values in parentheses).\n\nStatement: .354 (.032) is the highest Structural equivalence compare to both the Model .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb9c6018ca9",
  "kind": "yes/no",
  "text": "Table caption: Overview of the renewable energy technologies and the selected block types in the Minecraft platform.\n| Energy technology | Block type |\n| Solar panels | Daylight sensor |\n| Wall insulation | Yellow wool |\n| Floor insulation | Orange wool |\n| Double glazing | Glass |\n| Roof insulation | Purple wool |\n\nStatement: There are five renewable energy technologies are given.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe4d21e6922",
  "kind": "yes/no",
  "text": "Table caption: The number of views depending on the rating.\n| responses_rating_grade | views |\n| 1.0 | 1192.8 |\n| 2.0 | 1278.9 |\n| 3.0 | 1391.4 |\n| 4.0 | 1169.8 |\n| 5.0 | 990 |\n\nStatement: Rating grade 3.0 having more views.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q5e142a02df",
  "kind": "yes/no",
  "text": "Table caption: Comparison of the yields of pectin and hemicellulose fractions of the bamboo walls. Averages of three biological replicas for each species.\n| Species | Pectin * | Hemicellulose ⁎⁎ | Ratio |\n| Chusquea capituliflora | 7.4 | 54.1 | 7.3 |\n| Filgueirasia arenicola | 7.9 | 52.7 | 6.7 |\n| Filgueirasia cannavieira | 6.7 | 54.3 | 8.2 |\n| Guadua tagoara | 6.8 | 35.4 | 5.2 |\n| Merostachys riedeliana | 8.0 | 52.7 | 6.6 |\n| Parodiolyra micrantha | 10.9 | 46.4 | 4.3 |\n\nStatement: Merostachys riedeliana Pectin is 7.4.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q158d0d7a61",
  "kind": "yes/no",
  "text": "Table caption: Sociodemographic characteristics.\n|  | All | Women | Men |\n| Sex | 15 | 9 | 6 |\n| Age (Md years)(range) | 84(70-93) | 84(70-93) | 85(74-91) |\n| Living in a city | 8 | 6 | 2 |\n| Living in a rural area | 7 | 3 | 4 |\n| Living in an apartment | 8 | 6 | 2 |\n| Living in a terrace house | 7 | 3 | 4 |\n| Living alone | 14 | 9 | 5 |\n| Reason for needing care - Planned hip surgery - Hip fracture - Arm fracture - Severe infection | 3 9 1 2 | 2 5 1 1 | 1 4 1 |\n| Length of hospitalization (Md days) (range) | 9(4-20) |  |  |\n\nStatement: Living in a city is 6 for Women.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd60ce1b443",
  "kind": "yes/no",
  "text": "Table caption: In general, when light propagates towards the surface of a material, part of the incoming radiation is transmitted and part of the incoming radiation is reflected at the boundary between the two materials. The transmitted amplitude, t , and the reflected amplitude, r , are given by Fresnel's equations [ , ] and depend on the angle of incidence, θ 0 , the angle of refraction, θ , and the polarization of the light. The amplitudes also depend on the refractive index of the material, which, in our case, is n 0 = 1 for air and n for the film, as shown in . The subscripts of the amplitudes indicate if the respective rays are approaching the boundary from the left ( l ) or from the right ( r ).\n|  | Parallel polarization | Perpendicular polarization |\n| r l | cos θ − n cos θ 0 cos θ + n cos θ 0 | cos θ 0 − n cos θ cos θ 0 + n cos θ |\n| t l | 2 cos θ 0 cos θ + n cos θ 0 | 2 cos θ 0 cos θ 0 + n cos θ |\n| r r | n cos θ 0 − cos θ cos θ + n cos θ 0 | n cos θ − cos θ 0 cos θ 0 + n cos θ |\n| t r | 2 n cos θ n cos θ 0 + cos θ | 2 n cos θ n cos θ + cos θ 0 |\n\nStatement: There are fourteen categories under Parallel polarization and Perpendicular polarization.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7bfe9c2c92",
  "kind": "yes/no",
  "text": "Table caption: Columns data type.\n| No | Column | Count | Data type |\n| 1 | responses_header | 16,659 | object |\n| 2 | responses_rating_grade | 11,222 | float64 |\n| 3 | responses_status | 7559 | object |\n| 4 | responses_message | 16,659 | object |\n| 5 | responses_datetime | 16,659 | datetime64[ns] |\n| 6 | reviewer | 16,659 | object |\n| 7 | comments | 16,659 | int64 |\n| 8 | views | 16,659 | int64 |\n| 9 | id | 16,659 | int64 |\n| 10 | have_email | 16,659 | int64 |\n| 11 | responses_message_length | 16,659 | int64 |\n| 12 | gunning_fog_index | 16,659 | float64 |\n| 13 | binary_score | 16,659 | object |\n\nStatement: Column responses_rating_grade has the count of 11,222.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q9053e103db",
  "kind": "yes/no",
  "text": "Table caption: The Change in Compressive Strength of Experimental samples compared to control ones.\n| Name of mine | Control Samples | Experimental Samples | The Change (%) |\n| S E | 5.04 | 8.11 | % 60.93 |\n| S M | 2.23 | 5.23 | %134.84 |\n| S H | 4.9 | 7.74 | % 58.04 |\n| S GH | 5.51 | 7.11 | %29.09 |\n| S A | 2.41 | 4.68 | % 94.27 |\n| S Z | 3.18 | 6.34 | % 99.46 |\n\nStatement: There are 6 different Name of mine such as SE,SM,SH,SGH,SA,SZ.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q89abcedc33",
  "kind": "yes/no",
  "text": "Table caption: The mechanical properties of the used steel bars\n| Nominal diameter (mm) | Actual area (mm 2 ) | Yield strength (MPa) | Ultimate strength (MPa) | Elongation (%) |\n| 8 | 49 | 551 | 690 | 17.2 |\n| 12 | 112 | 513 | 671 | 17.5 |\n| 16 | 199 | 482 | 618 | 18.75 |\nTable notes: Note; each value represented an average for three samples.\n\nStatement: Nominal diameter (mm) 16 Actual area (mm 2 )is 112.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q91db94bedc",
  "kind": "yes/no",
  "text": "Table caption: Thermophysical properties of Ti-6Al-4V and characteristics of the set-up.\n| property | property | unit | value | reference |\n| absorptivity | A | – | 0.4 | [ 40 ] |\n| specific heat capacity | c p | J/gK | 0.5263 | [ 26 ] |\n| solidus temperature | T Sol | K | 1878 | [ 41 ] |\n| liquidus temperature | T Liq | K | 1928 * | [ 41 ] |\n| heat of fusion | H | J/g | 290 | [ 42 ] |\n| density | ρ | g/cm³ | 4.43 | [ 43 ] |\n\nStatement: They have six kinds of Thermophysical properties of Ti-6Al-4V.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q282e655089",
  "kind": "yes/no",
  "text": "Table caption: Expressions pertaining to models of discrete states: the shaded rows describe hidden states and auxiliary variables, while the remaining rows describe model parameters and functionals.\n| Expression | Description |\n| o τ ∈ { 0 , 1 } o τ = ∑ π π π ⋅ o π , τ ∈ [ 0 , 1 ] | Outcomes and their posterior expectations |\n| s τ ∈ { 0 , 1 } s τ = ∑ π π π ⋅ s π , τ ∈ [ 0 , 1 ] | Hidden states and their posterior expectations |\n| o π , τ = A s π , τ | Expected outcome, under a particular policy |\n| π ∈ { 1 , … , K } π = ( π 1 , … , π K ) ∈ [ 0 , 1 ] | Policies specifying state transitions and their posterior expectations |\n| ν π , τ = ln s π , τ : ε π , τ = v ˙ π , τ s π , τ = σ ( ν π , τ ) | Auxiliary variable representing depolarisation and expected state, under a particular policy |\n| ε π , τ = ln B π , τ − 1 s π , τ − 1 + ln B π , τ ⋅ s π , τ + 1 + ln A ⋅ o τ − ln s π , τ | Auxiliary variables representing state prediction error |\n| A | The likelihood of an outcome under each hidden state |\n| B π , τ | Time dependent probability transition matrices specified by the policy |\n| C τ = − ln P ( o τ / π ) | Prior surprise about outcomes; i.e. prior cost or inverse preference |\n| D | (Empirical) Prior expectations about initial hidden states |\n| F π = ∑ τ F ( π , τ ) | Variational free energy for each policy |\n| G π = ∑ τ G ( π , τ ) | Expected free energy for each policy |\n| G o = G ( o ) | Expected free energy for next outcome |\n| σ ( − G ) π = exp ( − G π ) ∑ π exp ( − G π ) | Softmax function, returning a vector that constitutes a proper probability distribution. |\n\nStatement: There are fourteen expressions given in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q22ef997081",
  "kind": "yes/no",
  "text": "Table caption: Homogenous Vs Heterogeneous photo-Fenton processes.\n|  | Homogenous | Heterogeneous |\n| State | Dissolved | Solid |\n| Kinetics | High | Low |\n| Cost | High | Low |\n| Efficiency | Low | High |\n| pH | <4 | >4 |\n| Catalyst re-use | No | Yes |\n| Iron Sludge | Yes | No |\n\nStatement: In Iron Sludge homogeneous is No and Yes in heterogeneous.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q57db4f0df9",
  "kind": "yes/no",
  "text": "Table caption: Data description of people's perception of misinformation.\n| Items | Obs. | Mean | S.D. | Min. | Max. |\n| Scientists | 517 | 6.12 | 2.90 | 0 | 10 |\n| Government | 513 | 5.65 | 2.57 | 0 | 10 |\n| Politicians | 514 | 4.99 | 2.84 | 0 | 10 |\n| People I know | 514 | 5.32 | 2.55 | 0 | 10 |\n| Traditional news (TV, newspaper, radio) | 516 | 5.41 | 2.39 | 0 | 10 |\n| Facebook | 516 | 4.96 | 2.79 | 0 | 10 |\n| Twitter | 512 | 4.95 | 2.70 | 0 | 10 |\n| YouTube | 510 | 4.97 | 2.79 | 0 | 10 |\nTable notes: Note: The respondents could skip questions they did not want to answer. Therefore, the number of observations varies for each question.\n\nStatement: Obs has the lowest value for YouTube of 510.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qfb0c06f524",
  "kind": "yes/no",
  "text": "Table caption: Modeled habitat type (Pfister 1977, ) spatial distributions for current and future climate as a percent of the SWCC landscape. Classification errors (%) are in parentheses for the current distribution. User and producer accuracy (%) are shown for the PVT Random Forest model under current climate. For simplicity modeled future distributions for a single GCM (HadGEM2-ES RCP8.5) are presented here. See for PVT distributions for two other GCMs.\n| PVT acronym | Current distribution (%) | HadGEM2-ES RCP8.5 distribution (%) | User/producer accuracy (%) |\n| ABGR/CLUN | 4.35 (67) | 0.33 | 36 / 53 |\n| ABLA/CLUN-CLUN | 9.16 (32) | 8.02 | 60 / 34 |\n| ABLA/CLUN-VACA | 9.14 (44) | 33.00 | 47 / 46 |\n| ABLA/LIBO | 3.27 (69) | 0 | 43 / 60 |\n| ABLA/LUHI | 10.88 (48) | 4.68 | 50 / 50 |\n| ABLA/MEFE | 7.34 (84) | 16.35 | 19 / 46 |\n| ABLA/XETE | 29.07 (53) | 2.85 | 47 / 61 |\n| PIAL-ABLA | 0.63 (100) | 0 | 50 / 25 |\n| PICEA/CLUN | 2.74 (82) | 0 | 8 / 29 |\n| PSME/PHMA | 0.96(82) | 0 | 33 / 50 |\n| PSME/SYAL | 14.9 (38) | 31.40 | 62 / 62 |\n| PSME/VACA | 3.63 (97) | 0 | 7 / 25 |\n| THPL/CLUN | 3.92 (19) | 3.39 | 86 / 79 |\n\nStatement: The lowest current distribution is 29.07 (53) of ABLA/XETE.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1f03e0507c",
  "kind": "yes/no",
  "text": "Table caption: Enumeration of strength and ductility parameters, including 0.2% proof stress ( σ 0.2 ), ultimate tensile strength ( σ B ), true fracture stress ( σ F ), uniform elongation ( ε u ), strain-to-failure ( ε F ), local elongation associated with necking (post-uniform elongation) ( ε L ) and reduction in area ( φ ), in specimens with diverse C H concentrations, tested at CHS = 1.5 × 10 −3 mm/s.\n| Hydrogen-chargingpressure (MPa) | C H (ppm) | C H (ppm) | σ 0.2 (MPa) | σ B (MPa) | σ F (MPa) | ε u | ε F | ε L | φ (%) |\n| Hydrogen-chargingpressure (MPa) | mass | at. | σ 0.2 (MPa) | σ B (MPa) | σ F (MPa) | ε u | ε F | ε L | φ (%) |\n| Non-charged | 4.7 | 250 | 233 | 530 | 1,213 | 0.375 | 0.577 | 0.202 | 86.3 |\n| 0.7 | 8.4 | 460 | 230 | 534 | 1,200 | 0.383 | 0.587 | 0.204 | 84.9 |\n| 11 | 40.0 | 2,190 | 248 | 545 | 1,368 | 0.393 | 0.597 | 0.204 | 84.2 |\n| 100 | 133 | 7,280 | 287 | 575 | 1,799 | 0.443 | 0.641 | 0.198 | 79.8 |\n\nStatement: The table CH has 2 categories such as mass and at.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qfcaeaa7b30",
  "kind": "yes/no",
  "text": "Table caption: Summary of the recommended recording parameters for BP and myoclonus.\n|  | Bereitschaftspotential | Myoclonus |\n| EMG filters | 10–250 Hz | 10–250 Hz |\n| EEG filters | 0.01–50 Hz | 1–70 Hz |\n| Sampling rate | At least 1000 Hz | At least 1000 Hz |\n| Behavioral recording | Record involuntary and voluntary movements. | Record involuntary movements during rest, posture and action depending on how the myoclonus is evoked. |\n\nStatement: BP and myoclonus has different hertz of EEG filters.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7f76b13c7f",
  "kind": "yes/no",
  "text": "Table caption: Structural Efficiency of Burnt bricks.\n| Samples | Density (kg/m 3 ) | Compressive Strength (N/mm 2 ) | Shear Stress (N/mm 2 ) | Structural Efficiency (x 10 3 m) |\n| P 0 & T 0 | 1376 | 6.15 | 2.33 | 4.47 |\n| P 1 | 1376 | 4.02 | 2.99 | 2.92 |\n| P 2 | 1376 | 3.57 | 2.98 | 2.59 |\n| P 3 | 1354 | 3.16 | 2.99 | 2.33 |\n| P 4 | 1322 | 2.82 | 2.99 | 2.13 |\n| P 5 | 1322 | 2.61 | 2.97 | 1.97 |\n| T 1 | 1376 | 6.67 | 2.54 | 4.84 |\n| T 2 | 1376 | 7.78 | 3.00 | 5.65 |\n| T 3 | 1376 | 8.97 | 3.01 | 6.52 |\n| T 4 | 1376 | 10.16 | 3.01 | 7.40 |\n| T 5 | 1376 | 11.02 | 3.02 | 8.01 |\n\nStatement: The Shear Stress (N/mm 2 ) ranges from 2.33 to 3.02.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3fd27f592e",
  "kind": "yes/no",
  "text": "Table caption: Adsorption energies of intermediate species involved in the methanol oxidation on Pd(111), Pd 3 Ni(111) and PdNi(111) catalysts. In parentheses is the lowest energy adsorption site of each species. The final column shows how the E a vary with the alloying of Ni on Pd where the symbols ⇑, ⇓ and = indicate whether the intermediate presents stronger, weaker or equal adsorption when changing the transition-metal surface from: i) Pd(111) to Pd 3 Ni(111) and ii) from Pd 3 Ni(111) to PdNi(111) .\n| Species | Pd - E ad (eV) | Pd 3 Ni - E ad (eV) | PdNi - E ad (eV) | trend |\n| CH 2 O* | 0.61 (B Pd ) | 0.09 (B NiPd ) | -0.02 (B 2Ni ) | ⇑⇑ |\n| CH 2 OH* | 0.08(B Pd ) | 0.19 (B 2Pd ) | 0.31 (B 2Pd ) | ⇓⇓ |\n| CH 3 O* | 0.42 (F Pd ) | 0.07 (F 2PdNi ) | -0.23 (F 2NiPd ) | ⇑⇑ |\n| CH 3 OH* | 0.02 (T Pd ) | -0.16 (T Ni ) | -0.10 (T Ni ) | ⇑⇓ |\n| CHO* | -0.16 (F Pd ) | -0.31 (F Ni2Pd ) | -0.14 (H 2PdNi ) | ⇑⇓ |\n| CHOH * | -0.01 (B Pd ) | 0.12 (B PdNi ) | 0.17 (B PdNi ) | ⇓⇓ |\n| CO* | -1.15 (F Pd ) | -1.07 (F 2PdNi ) | -1.06 (F 2NiPd ) | ⇓= |\n| CO 2 * | 0.12 (B Pd ) | 0.06 (B NiPd ) | 0.07 (B 2Ni ) | ⇑= |\n| COH * | -0.43 (F Pd ) | -0.32 (F 2PdNi ) | -0.35(F 2NiPd ) | ⇑⇓ |\n| COHOH* | 0.00 (T Pd ) | -0.03 (T Ni ) | 0.05 (T Ni ) | ⇑⇓ |\n| COOH* | -0.05 (B Pd ) | -0.15 (B NiPd ) | -0.29 (B 2Ni ) | ⇑⇑ |\n| H 2 COO* | 1.40 (B Pd ) | 1.09 (B*) | 0.68 | ⇑⇑ |\n| H 2 COOH * | 0.75 (B Pd ) | 0.42(B NiPd ) | 0.48 (B NiPd ) | ⇑⇓ |\n| HCOO* | 0.09 (B Pd ) | -0.25 (B NiPd ) | -0.52 (B 2Ni ) | ⇑⇑ |\n| HCOOH* | 0.06 (T Pd ) | -0.11 (T Ni ) | -0.07 (T Ni ) | ⇑⇓ |\n| H 2 O* | 0.04 (T Pd ) | -0.11 (T Ni ) | -0.06 (T Ni ) | ⇓⇑ |\n| OH* | 0.58 (F Pd ) | 0.19 (F 2PdNi ) | -0.09 (F 2NiPd ) | ⇑⇑ |\n| O* | 0.82 (F Pd ) | 0.51 (F 2PdN ) | 0.12(F 2NiPd ) | ⇑⇑ |\n\nStatement: 0.00 is the unique value of Pd - E ad (eV) in COHOH*.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2235e36f92",
  "kind": "yes/no",
  "text": "Table caption: Path analysis.\n| Factors | Standard Coefficient | SE - value | t-value | 95% biased confidence interval | 95% biased confidence interval | Results |\n| Factors | Standard Coefficient | SE - value | t-value | LL | UL | Results |\n| NSR tourism infrastructure to QOL | 0.15∗∗ | 0.045 | 3.373 | 0.064 | 0.243 | Supported |\n| NSR tourism infrastructure to STD | 0.26∗∗∗ | 0.046 | 5.550 | 0.165 | 0.346 | Supported |\n| Sustainable tourism to QOL | 0.24∗∗∗ | 0.046 | 5.290 | 0.154 | 0.337 | Supported |\nTable notes: Note: ∗∗p<0.005, ∗∗∗p<0.001. NSR = New Silk Road, QOL = Quality of life, STD = Sustainable tourism development .\n\nStatement: SE - value has same values of 0.046 for NSR tourism infrastructure to STD and Sustainable tourism to QOL.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q91c9ecdf06",
  "kind": "yes/no",
  "text": "Table caption: Initial vertical force F z and moment M y E for the numerical 2-DOF free-oscillation tests in still air.\n| Parameter | Symbol | Unit | Case I | Case II | Case III |\n|  |  |  | x EG ≈ 0 | x EG < 0 | x EG > 0 |\n| Initial vertical force | F z | N | - 7.15 × 10 - 1 | - 3.00 × 10 - 1 | - 1.00 × 10 - 2 |\n| Initial vertical moment | M y E | Nm | 9.00 × 10 - 3 | 1.00 × 10 - 3 | 2.50 × 10 - 2 |\n\nStatement: 9.00 10 - 3 Case I is Parameter Initial vertical moment.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc155fe66a0",
  "kind": "yes/no",
  "text": "Table caption: Items measuring patient satisfaction at discharge.\n| Items | N | Mean | SD |\n| Availability of staff counseling | 172 | 4.09 | 0.72 |\n| Have benefited from treatment | 171 | 4.25 | 0.75 |\n| Problems understood by staff | 172 | 4.26 | 0.72 |\n| Opportunities to affect treatment plan | 171 | 3.78 | 0.92 |\n| Felt safe at the institution a | 171 | 171 | 4.54 |\n| Satisfactory activities were offered | 170 | 3.86 | 0.85 |\n| Personnel cooperated with next of kin b | 136 | 3.83 | 0.83 |\n| Had been prepared for the time after discharge | 169 | 3.89 | 0.79 |\n| Enough time in treatment to sort out problems | 171 | 3.86 | 0.95 |\n| Overall treatment was satisfactory | 172 | 4.21 | 0.68 |\n\nStatement: Availability of staff counseling value of N is 169.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe2a0159b5b",
  "kind": "yes/no",
  "text": "Table caption: The three databases of the International Nucleotide Sequence Database Collaboration (INSDC), respective websites and recent publications with updates on the databases.Database.\n|  | Country/Region | Website | See also: |\n| European Nucleotide Archive (ENA) | Europe | https://www.ebi.ac.uk/ | Cook et al. (2019) |\n| Bioinformation and DNA Data Bank of Japan (DDBJ) | Japan | https://www.ddbj.nig.ac.jp/index-e.html | Ogasawara et al. (2020) |\n| GenBank | United States | www.ncbi.nlm.nih.gov/genbank/ | Sayers et al. (2019) |\n\nStatement: Europe region does not have any database.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qeba8998361",
  "kind": "yes/no",
  "text": "Table caption: pH measurements on sediment and fill samples, including limestone fragments from the Abri Pataud.\n| Level | Sample | pH |\n| 2 | Sediment | 8.9 |\n| 4 | Sediment | 8.2 |\n| 11 | Sediment | 9.9 |\n| 4 | Fill, jar 6 | 8.9 |\n| 7 | Fill, jar 4 | 8.9 |\n| 11 | Fill, jar 11 | 8.6 |\n| 12 | Fill, jar 3 | 8.3 |\n| 14 | Fill, jar 16a | 8.3 |\n| – | Limestone | 8.3 |\n\nStatement: Only level 4 sediment has 8.2 pH value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q81bd9731e6",
  "kind": "yes/no",
  "text": "Table caption: Performance of the combined BRT models, and dependencies on sampling and environmental variables for each univariate model. Values shown are the proportions of variance explained by each of the variables (%). E coszen represents the time of day of sampling in terms of the cosine of the solar zenith angle. Environmental variables include all components (i.e. month, climatological month, climatological year average and annual anomaly). The mixed layer depth variable ( mld ) includes both mld0p030 and mld0p125 variables.\n| Cluster | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) | Sampling and environmental variables (% of variance explained) |\n| Cluster | Month | E coszen | SeaIce | chl | sst | mld | sstgrad | vgpm | All |\n| Total abundance | 5.1 | 8.1 | 3.3 | 4.9 | 14.8 | 8.2 | 3.4 | 6.4 | 54.2 |\n| Copepoda | 4.5 | 15.9 | 2.2 | 4.0 | 12.7 | 6.2 | 2.4 | 5.0 | 53.0 |\n| Euphausiidae | 1.5 | 15.0 | 0.1 | 2.4 | 4.6 | 2.9 | 1.7 | 3.9 | 32.2 |\n| Foraminifera | 4.4 | 0.4 | 1.2 | 5.9 | 10.1 | 13.9 | 4.2 | 6.2 | 46.2 |\n| Fritillaria spp. | 5.6 | 0.9 | 1.7 | 7.6 | 11.7 | 12.5 | 6.2 | 5.9 | 52.2 |\n| Oithona similis | 5.3 | 1.5 | 4.4 | 3.5 | 20.9 | 10.4 | 3.1 | 5.1 | 54.1 |\n| Pteropods | 2.9 | 7.4 | 1.3 | 8.4 | 10.0 | 7.2 | 4.6 | 5.1 | 46.8 |\n\nStatement: > 1.27, p < 0.0005, for N = 45,489).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf80cc3c232",
  "kind": "yes/no",
  "text": "Table caption: Socio-demographic profile of the participants (n = 331).\n| Characteristics | Characteristics | Percentage* |\n| Age | mean in years | 38.9 |\n| Gender | male | 38.1 |\n| Household size | 1 | 14.2 |\n|  | 2 | 28.4 |\n|  | 3 | 19.3 |\n|  | 4 | 22.4 |\n|  | >=5 | 15.7 |\n| Children at home | Yes | 50.8 |\n| Level of education | Primary school | 0.3 |\n|  | Secondary school | 23.9 |\n|  | Higher education-not university | 38.4 |\n|  | University- first degree, BSc | 31.1 |\n|  | University Post graduate, PhD | 6.3 |\n| Income | more than average | 13.0 |\n|  | average | 63.1 |\n|  | less than average | 23.9 |\n\nStatement: Income more than average has 93.0 percentage value.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf6ce127bec",
  "kind": "yes/no",
  "text": "Table caption: Means (SD) of client empathy measure at T1 and T2, therapist reported outcome at T2, and correlations between T1 and T2 measurements.\n|  | T1 | T1 |  | T2 | T2 |  | r t1xt2 |\n|  | Girls n = 28 | Boys n = 62 |  | Girls n = 28 | Boys n = 62 |  | N = 90 |\n|  | M (SD) | M (SD) | t ( df = 88) | M (SD) | M (SD) | t ( df = 88) |  |\n| BES_aff | 3.29 (0.81) | 2.91 (0.76) | −2.16* | 3.38 (0.81) | 3.03 (0.78) | −1.94 | 0.70** |\n| BES_cog | 3.97 (0.58) | 3.91 (0.56) | <1 | 4.14 (0.58) | 3.94 (0.48) | −1.69 | 0.42** |\n| IRI_aff | 3.07 (0.57) | 2.65 (0.51) | −3.45** | 3.18 (0.67) | 2.79 (0.55) | −2.89* | 0.53** |\n| IRI_cog | 2.89 (0.53) | 2.82 (0.64) | <1 | 3.17 (0.65) | 2.82 (0.67) | −2.32* | 0.63** |\n| TRO | – | – |  | 5.81 (1.88) | 5.60 (1.75) | <1 |  |\nTable notes: Note : * p < .05, ** p < .001. BES = Basic Empathy Scale (1–5); IRI = Interpersonal Reactivity Index (1–5); aff = affective empathy, cog = cognitive empathy; TRO = therapist rated outcome (1–10).\n\nStatement: BES_aff has 3.29 (0.81) values under M (SD) for T1.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe0cd0283d3",
  "kind": "yes/no",
  "text": "Table caption: Correlation of urbanisation indices calculated from areas with radii of 50, 100, 200, 500, and 1000 m around every sampling point with all other environmental variables.\n| Urbanisation index | 50 m | 100 m | 200 m | 500 m | 1000 m |\n| 50 m | 1.000 | 0.954 | 0.784 | 0.586 | 0.376 |\n| 100 m |  | 1.000 | 0.919 | 0.730 | 0.448 |\n| 200 m |  |  | 1.000 | 0.875 | 0.535 |\n| 500 m |  |  |  | 1.000 | 0.826 |\n| 1000 m |  |  |  |  | 1.000 |\n| pH | -0.017 | 0.171 | 0.286 | 0.422 | 0.467 |\n| Dissolved oxygen | -0.135 | -0.186 | -0.372 | -0.375 | -0.293 |\n| TDS | -0.034 | 0.183 | 0.495 | 0.607 | 0.533 |\n| Nitrate | -0.187 | 0.033 | 0.185 | 0.168 | 0.035 |\n| Phosphate | -0.082 | 0.150 | 0.493 | 0.551 | 0.357 |\n| Light intensity | 0.528 | 0.535 | 0.476 | 0.490 | 0.583 |\n| % Macrophyte | 0.490 | 0.429 | 0.390 | 0.392 | 0.472 |\n| % Canopy cover | -0.516 | -0.514 | -0.468 | -0.459 | -0.542 |\n| % Leaf litter | -0.133 | -0.187 | -0.258 | -0.299 | -0.206 |\n| % Grass | 0.391 | 0.498 | 0.550 | 0.601 | 0.683 |\n| % Shrub | -0.082 | -0.184 | -0.225 | -0.245 | -0.303 |\n| % Tree | -0.455 | -0.498 | -0.526 | -0.577 | -0.612 |\n| % Mud | -0.005 | -0.028 | -0.051 | -0.113 | -0.036 |\n| % Sand | 0.079 | 0.078 | 0.105 | 0.101 | -0.135 |\n| % Gravel and concrete | -0.108 | -0.071 | -0.077 | 0.023 | 0.255 |\n\nStatement: There are different Correlation of urbanisation indices calculated from areas with radii of 50, 100, 200, 500, and 1000 m.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q30a71ee5bb",
  "kind": "yes/no",
  "text": "Table caption: Comparison of fracture force and dissipated energy until fracture for the various sample geometries of the coconut endocarp tested in this study. Medians and interquartile ranges (IQR) are derived from Table 1 and Figs. 1 & 4 & 5 .\n| Geometry | Test setup | n | Cross-head speed [mm/min] | Fracture force [N] | Dissipated energy [J] |\n| Entire endocarp | Longitudinal | 10 | 5 | 3487 (IQR: 1123) | 6.74 (IQR: 3.28) |\n| Arch-shaped samples | Quasi-static, equatorial, constrained | 19 | 1 | 275 (IQR: 134) | 0.38 (IQR: 0.20) |\n| Rectangular samples | Normal, natural | 10 | 1 | 4201 (IQR: 746) | 2.65 (IQR: 0.52) |\n\nStatement: The Dissipated energy [J] of all the geometry is same.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 }
]
