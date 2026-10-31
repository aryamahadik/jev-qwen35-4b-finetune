# Replay noise screen blind read NS-semtabfacts_sci-blind_read-ff4c38f3-046 (family NS-semtabfacts_sci)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-semtabfacts_sci-blind_read-ff4c38f3-046.json

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
  "qid": "q08c9f19989",
  "kind": "yes/no",
  "text": "Table caption: Correlation matrix for analysis of seasonal fluctuation (No unit in a matrix).\n|  | Electric consumption | Operationg days | Outside temperature | Carcass volume |\n| Electric consumption | 1 | 0.2332 | 0.9307 | −0.5181 |\n| Operationg days | 0.2332 | 1 | 0.0172 | 0.2021 |\n| Outside temperature | 0.9307 | 0.0172 | 1 | −0.7063 |\n| Carcass volume | −0.5181 | 0.2021 | −0.7063 | 1 |\n\nStatement: There are nine different Correlation matrix for analysis of seasonal fluctuation.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa83a3d6a07",
  "kind": "yes/no",
  "text": "Table caption: Comparison of method effectiveness for different situations.\n|  | Effective for: | Less effective for: |\n| Retrospective interviews | - Outlining the process of micro-level transition | - Capturing the uncertainty and complexity of |\n|  | processes and intermediation and accessing | micro-level transition processes and |\n|  | events occurring prior to data collection | intermediation |\n|  | - Drawing inferences on commonalities in micro- | - Capturing a rich ecology of intermediaries |\n|  | level transition processes | involved in micro-level transition processes |\n|  | - Tapping into the sensemaking of process | - Capturing gaps in current transition |\n|  | participants to construct narratives and link | intermediation processes |\n|  | incidents and phases of change processes |  |\n|  | - Gathering data economically about specific |  |\n|  | issues from various intermediaries and |  |\n|  | intermediation processes |  |\n| Real-time ethnography | -Generating detailed and nuanced understanding | - Capturing whole micro-level transition |\n|  | of micro-level processes and agency of actors in | processes such as retrofit adoption |\n|  | transitions | - Comparing a large number of cases and |\n|  | - Understanding the complexity and uncertainty | creating generalizations of micro-level transition |\n|  | related to micro-level transition processes and | intermediation processes and process phases |\n|  | intermediation | - Sampling strategically in advance to address |\n|  | - Avoiding hindsight bias and post-rationalization | particular transition intermediation issues |\n|  | of how intermediaries work |  |\n|  | - Creating situated views of the frames of actors |  |\n|  | in transition processes. |  |\n|  | - Discovering new issues at the transition micro- |  |\n|  | level and intermediation |  |\n\nStatement: Outlining the process of micro-level transition is effective in Retrospective interviews.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf749afcb22",
  "kind": "yes/no",
  "text": "Table caption: Terminology used throughout the paper.\n| Term | Explanation |\n| Chart | A chart has a type and associated tabular input data that is represented by output marks. |\n| Chart type | A type of chart within the Visception framework, consists of its own layout that is controlled by some of its VC-channels. The layout controls the shape and position of the chart’s output marks. |\n| Output marks | Graphical marks of a single chart. |\n| VC-channel | Controls a particular aspect of the appearance or layout of a chart. |\n| VC-channel mapping | The assignment of data (for example a dimension) to a VC-channel (for example fill color ). |\n| Layout space | Normalized space in which a layout is initially computed. |\n| Parent space | Space(s) in which a chart’s output marks are embedded according to the computed layout. If the node is a root node, the parent space is simply the root viewport. Otherwise, a chart-dependent region within the output marks of the parent chart. |\n| Data object | Represents a selection from a tabular dataset. May be one of the following: 1) A single row, 2) A list of rows, 3) A list of values. |\n| Chart input data | A set of data objects inherited from the parent VC-node. If the node is the root VC-node, the input data is the list of rows of the entire dataset. |\n| Chart mapping | Transforms every input data object into a new set of data objects. |\n| Chart output data | A set of data objects, used for rendering the chart, and possibly as input data to child charts. |\n\nStatement: Table has 14 terms in it.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd84c02be69",
  "kind": "yes/no",
  "text": "Table caption: Summary of the analysis of variance on the mechanical properties of the developed composites.\n| Mechanical property | Effect of fillers’ weight per cent | Effect of fillers’ weight per cent | Effect of fillers’ weight per cent | Effect of fillers’ structural strengths | Effect of fillers’ structural strengths | Effect of fillers’ structural strengths |\n| Mechanical property | F | P-value | F crit | F | P-value | F crit |\n| Hardness | 11.04 | 8.11 × 10 − 4 | 3.33 | 7.85 | 8.90 × 10 − 3 | 4.10 |\n| Compressive strength | 2.55 | 9.77 × 10 − 2 | 3.33 | 1.02 | 3.96 × 10 − 1 | 4.10 |\n| Compressive modulus | 31.30 | 8.49 × 10 − 6 | 3.33 | 2.70 | 1.15 × 10 − 1 | 4.10 |\n| Fracture toughness ( Eq. 2 ) | 13.13 | 3.97 × 10 − 4 | 3.33 | 5.71 | 2.22 × 10 − 2 | 4.10 |\n| Fracture toughness ( Eq. 3 ) | 15.39 | 2.03 × 10 − 4 | 3.33 | 5.47 | 2.48 × 10 − 2 | 4.10 |\n\nStatement: F value of Effect of fillers weight per cent is highest for Compressive modulus.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q64515511ea",
  "kind": "yes/no",
  "text": "Table caption: GFRP bars specifications.\n| Bar type | GFRP |\n| Nominal diameter (mm) | 14 |\n| Ultimate strength (MPa) | 1200 |\n| Modulus of elasticity (MPa) | 55,000 |\n| Strain,ε ƒu (με) | 1950 |\n\nStatement: Ultimate strength (MPa) and Modulus of elasticity (MPa) has same GFRP.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q62a23bf5de",
  "kind": "yes/no",
  "text": "Table caption: fAPAR Italy-wide cumulative anomalies and their associated drought level characterisation. Negative anomalies indicate overall drought stress. The mean of the drought index over the study period is equal to 0 by construction ( f A P A R ¯ = 0 ; σ f A P A R = 19.44 ). Three drought severity levels were defined: mild (-1/2σ,0], moderate (-3/2σ,-1/2σ] and extreme [<-3/2σ]. Positive values denote normal/wet growing conditions.\n| Year | fAPAR | Drought severity |\n| 2001 | −16.78 | Moderate |\n| 2002 | −20.00 | Moderate |\n| 2003 | −28.06 | Extreme * |\n| 2004 | −9.55 | Mild |\n| 2005 | −10.59 | Moderate |\n| 2006 | −11.19 | Moderate |\n| 2007 | −8.08 | Mild |\n| 2008 | −9.99 | Moderate |\n| 2009 | −4.17 | Mild |\n| 2010 | 9.05 | Normal/Wet |\n| 2011 | −3.54 | Mild |\n| 2012 | −0.72 | Mild |\n| 2013 | 12.76 | Normal/Wet |\n| 2014 | 37.12 | Normal/Wet |\n| 2015 | 28.75 | Normal/Wet |\n| 2016 | 35.00 | Normal/Wet |\n\nStatement: In the year 2006 the Drought severity is Normal/Wet",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q1d2c33c752",
  "kind": "yes/no",
  "text": "Table caption: Comparative antibacterial activity of synthesized nanoparticles ZnO and TiO 2 nanoparticles against different microorganisms.\n| Plant species | Plant part used | NPs tested | Species | References |\n| Catharanthus roseus | Leaf | ZnO | B. thuringiensis, E. coli, S. aureus, P. aeruginosa | Bhumi and Savithramma, 2014 |\n| Brassica oleraceae | Leaf | ZnO | E. coli, V. cholera, C. Botulinum, S. aureus, B. subtilis | Raj et al., 2015 |\n| Trifolium pratense | Flower | ZnO | S. aureus, P. aeruginosa, E. coli | Dobrucka and Dugaszewska, 2016 |\n| Bauhinia tomentosa | Leaf | ZnO | B. thuringiensis, E. coli, S. aureus, P. aeruginosa | Sharmila et al., 2018 |\n| Pandanus odorifer | Leaf | ZnO | B. subtilis, E. coli | Hussain et al., 2019 |\n| Aloe vera | Leaf | ZnO | E. coli | Izwanie Rasli et al., 2020 |\n| Psidium guajava | Leaf | TiO 2 | E. coli, S. aureus | Santhoshkumar et al., 2014 |\n| Cynodon dactylon | Leaf | TiO 2 | E. coli | Hariharan et al., 2017 |\n| Glycosmis | Leaf | TiO 2 | S. saprophyticus, B. subtilis, E. coli, cochinchinensis P. aeruginosa | Rosi and Kalyanasundaram, 2018 |\n| Cassia fistula | Leaf | TiO 2 | E. coli, S. aureus | Swathi et al., 2019 |\n\nStatement: The species for Pandanus odorifer is B. subtilis, E. coli.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc2cc4504f6",
  "kind": "yes/no",
  "text": "Table caption: The categories and their conditions.\n| Category | More likely to be salient | Less likely to be salient |\n| Loudness | Word intensity of 80 dB | Word intensity of 60 dB |\n| Acoustic Prominence | /t/pronounced as [p] | /t/pronounced as [t] |\n| Grammatical Gender | Violation of grammatical gender | Correct grammatical gender |\n| Frequency | High frequency word | Low frequency word |\n| Conscious Sound Change | /r/pronounced as [ɹ] | /r/pronounced as [r] |\n| Subconscious Sound Change | /v/pronounced as [v] (=voiced) | /v/pronounced as [f] (=voiceless) |\n\nStatement: More likely to be salient for Grammatical Gender is/r/pronounced as [] .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe181a0e6ff",
  "kind": "yes/no",
  "text": "Table caption: Code files for the processing and analysis of data.\n| Filename | Main goal |\n| Phase1.ipynb | Processing, refining, completing, and formating the raw collected data. |\n| Phase2.ipynb | Data augmentation with calculated features and anonymization of personal properties. |\n| Phase3.ipynb | Statistical analysis of the data regarding the social bots’ activities. |\n| Phase4.ipynb | Feature engineering, analysis, and representation of users political classification. |\n| Phase5.ipynb | Analysis and characterization of classified social bots activity and behavior. |\n\nStatement: The Phase2.ipynb has a main goal of Data augmentation with calculated features and anonymization of personal properties.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q386ab81448",
  "kind": "yes/no",
  "text": "Table caption: Mean squares and R 2 values of model parameters for traits at stocking.\n| MSS at stocking | MSS at stocking | MSS at stocking | MSS at stocking |\n| Source | DF | BW0 | TL0 |\n| Stock | 1 | 291.92 | 1.59 |\n| Batch | 1 | 369846.60 | 19356.27 |\n| Sex | 2 | 3888.90 | 111.33 |\n| Family | 75 | 1524.03 | 75.96 |\n| Error | 2248 | 77.50 | 2.60 |\n| R2 % |  | 79 % | 85 % |\n\nStatement: MSS at stocking of BW0 for Batch is 369846.60.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2c22c798d5",
  "kind": "yes/no",
  "text": "Table caption: Contingency matrix to evaluate the frequency of rainfall detection of CHIRPS and MPEG at daily time interval.\n|  | In-situ measured rainfall | No in-situ measured rainfall |\n| Satellite detected rainfall | H | FA |\n| No rainfall detected by satellite | M | CN |\nTable notes: H, M, FA and CN represents the number of days corresponding to their respective combinations.\n\nStatement: The No in-situ measured rainfall is FA for Satellite detected rainfall.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf12588f9ab",
  "kind": "yes/no",
  "text": "Table caption: Phase A: water 10 mM formic acid; Phase B: acetonitrile 10 mM formic acid; %As: % phase A start time; %Af: % phase A end time.\n| Start time → end time (min) | Column temp (°C) | Flux (µl/min) | %As→ %Af |\n| 0 → 4 | 40 | 450 | 90 →70 |\n| 4 → 8 | 40 | 450 | 70 → 30 |\n| 8 → 10 | 40 | 450 | 30 → 0 |\n| 10 → 12 | 40 | 450 | 0 → 0 |\n| 12 → 13 | 40 | 450 | 0 → 90 |\n| 13 → 16 | 40 | 450 | 90 → 90 |\n\nStatement: The %As %Af has a range between 0 to 90.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf24ec53d92",
  "kind": "yes/no",
  "text": "Table caption: Shows BI of each sample tested in Cyclic loading apparatus (Actuator).\n| Sample | BI |\n| Control28 | 0.043 |\n| 20FAS28 | 0.042 |\n| 20FA28 | 0.056 |\n| 30FAS28 | 0.05 |\n| 30FA28 | 0.062 |\n\nStatement: There is only one head as Sample.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q02fb9c2a5f",
  "kind": "yes/no",
  "text": "Table caption: Descriptive statistics.\n|  | Minimum | Maximum | Mean | SD |\n| Similarity in cobranding (SCB) | 0 | 6 | 4.13 | 1.48 |\n| SCB 2 | .016 | 17.0 | 2.18 | 2.95 |\n| Total cobranding | 2.67 | 14 | 10.5 | 2.33 |\n| Decreasing network distance (DND) | 1 | 4 | 2.57 | .691 |\n| DND 2 | .188 | 2.45 | .478 | .635 |\n| Difference in closeness (DCL) | .021 | 13.2 | 3.87 | 2.84 |\n| Structural equivalence | –.146 | .677 | .042 | .133 |\n| Same destination dummy | 0 | 1 | .138 | .345 |\n| Combined closeness (CCL) | 57.9 | 83.9 | 69.8 | 4.69 |\n| CCL × DCL | −52.1 | 44.6 | 2.05 | 11.0 |\nTable notes: The number of dyads is 990.\n\nStatement: Similarity in cobranding (SCB) has the Minimum value of 5.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd361b54911",
  "kind": "yes/no",
  "text": "Table caption: Code files for the processing and analysis of data.\n| Filename | Main goal |\n| Phase1.ipynb | Processing, refining, completing, and formating the raw collected data. |\n| Phase2.ipynb | Data augmentation with calculated features and anonymization of personal properties. |\n| Phase3.ipynb | Statistical analysis of the data regarding the social bots’ activities. |\n| Phase4.ipynb | Feature engineering, analysis, and representation of users political classification. |\n| Phase5.ipynb | Analysis and characterization of classified social bots activity and behavior. |\n\nStatement: There are 5 different types phase in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdbf761aba9",
  "kind": "yes/no",
  "text": "Table caption: Segmentation of clinical data.\n| Parameter | t o − t 1 | t 1 − t 2 | t 2 − t 3 | t 3 − t p |\n| A (height) | 29.18 | 26.02 | 0 | 3.37 |\n| τ (length) | 0.068 | 0.104 | 0.0452 | 0.053 |\n\nStatement: All the values in the given table consist of negative values.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcfaf4dffbe",
  "kind": "yes/no",
  "text": "Table caption: Overview of the renewable energy technologies and the selected block types in the Minecraft platform.\n| Energy technology | Block type |\n| Solar panels | Daylight sensor |\n| Wall insulation | Yellow wool |\n| Floor insulation | Orange wool |\n| Double glazing | Glass |\n| Roof insulation | Purple wool |\n\nStatement: Yellow wool and orange wool are two different block types.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe34c43d7b6",
  "kind": "yes/no",
  "text": "Table caption: Chemical composition (mass %) of Type 310S stainless steel used in this study.\n| C | Si | Mn | P | S | Ni | Cr | Fe |\n| 0.02 | 0.30 | 1.06 | 0.028 | 0.001 | 19.07 | 24.21 | Bal. |\n\nStatement: The Chemical composition of Ni is 19.07.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa2ce2fd597",
  "kind": "yes/no",
  "text": "Table caption: Measures of model performance resulting from training and validation\n| Item | Data set | Data set | Data set |\n| Item | 1 | 2 | 3 |\n| Epoch | 750 | 750 | 278 |\n| Training loss | 0.06 | 0.50 | 0.43 |\n| Validation loss | 2.48 | 0.94 | 0.71 |\n| Accuracy | 0.68 | 0.59 | 0.71 |\n| Positive predictive value | 0.63 | 0.53 | 0.66 |\n| Negative predictive value | 0.71 | 0.64 | 0.78 |\n| Sensitivity (true positive rate) | 0.51 | 0.48 | 0.79 |\n| Specificity (true negative rate) | 0.80 | 0.68 | 0.65 |\n| Matthews correlation coefficient | 0.32 | 0.16 | 0.44 |\n\nStatement: Each data set has different from each other.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q44d4f28cf0",
  "kind": "yes/no",
  "text": "Table caption: Sample comparisons of resilience values in four hypothetical cases -\n| City | A | B | C | D |\n| Hospital Beds | 5 | 10 | 15 | 500 |\n| Min-Max Resilience A-C | 0 | 0,5 | 1 | n.a. |\n| Min-Max Resilience A-D | 0 | 0,01 | 0,02 | 1 |\n| Exponential resilience (with rho = −5) | 0 | 0,55 | 0,95 | 1 |\n\nStatement: The highest hospital beds are 500 in D column.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdd31de766e",
  "kind": "yes/no",
  "text": "Table caption: Main features of the tomato and corn fields characterized by personal contact with local farmers in the 2018 and 2019 growing seasons ( Fig. 9 A–C), with respective estimated IW.\n| Crop type | Year | N. fields | Sowing | Transplanting | Harvesting | Estimated IW (mm) |\n| Early tomato | 2018 | 3 |  | End of April | Beginning of August | 226 |\n| Late tomato | 2018 | 6 |  | Beginning of June | Beginning of September | 308 |\n| Early tomato | 2019 | 5 |  | End of April | Mid-August | 314 |\n| Late tomato | 2019 | 5 |  | End of May | Beginning of September | 289 |\n| Early corn | 2018 | 4 | Mid-April |  | End of August | 397 |\n| Late corn | 2018 | 6 | Mid-June |  | Beginning of October | 339 |\n\nStatement: Early corn has highest estimated IW (mm).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q59e8519e64",
  "kind": "yes/no",
  "text": "Table caption: Purification chart of bevacizumab using Ac-PHQGQHIGVSK-agarose matrix.\n| Sample | b Total protein (mg) | c Total bevacizumab (mg) | d Purity % | Fold purification | Yield (%) |\n| a Crude sample | 0.487 | 0.219 | 45.0 | 1.0 | 100 |\n| Eluate fraction | 0.210 | 0.206 | 98.1 | 2.2 | 94.1 |\n\nStatement: All the values of samples are same.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0a6f58d743",
  "kind": "yes/no",
  "text": "Table caption: Results of the 3-way crossed ANOSIM analyses for the taxa Cancer pagurus, Pagurus spp., Marthasterias glacialis and Astropecten irregularis. Global tests on the effects of sampling area: foundations and controls, year and geographical position.\n| Taxa | Sampling area | Sampling area | Year | Year | Geographical position | Geographical position |\n| Taxa | Global R | P-value | Global R | P-value | Global R | P-value |\n| Cancer pagurus | 0.851 | 0.0001 | 0.003 | 0.052 | −0.016 | 0.724 |\n| Pagurus spp . | 0.585 | 0.0001 | 0.044 | 0.027 | 0.03 | 0.153 |\n| Marthasterias glacialis | 0.872 | 0.0001 | 0.1 | 0.0001 | −0.008 | 0.585 |\n| Astropecten irregularis | 0.358 | 0.0001 | 0.186 | 0.0001 | 0.037 | 0.115 |\n\nStatement: Marthasterias glacialis has 10.1 as Global value for Year",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q774c36195f",
  "kind": "yes/no",
  "text": "Table caption: Impact analysis of the joint plans, showing investment cost, reduction of gas consumption, electricity production, reduction of CO2-emission, and payback period per technology.\n|  | Investment cost (€) | Reduction in gas consumption (m3) | Electricity production (kWh) | Reduction in CO2 emission (kg CO2-eq) | Payback period (years) |\n| Solar panels | 6,512,100‬ | – | 6,423,219 | 3,211,609 | 5.3 |\n| All insulation | 81,908,719 | 8,878,861 | – | 17,580,145 | 15.3 |\n| All technologies | 88,420,819 | 8,878,861 | 6,423,219 | 20,791,754 | 12.6 |\n\nStatement: All technologies has a highest value in investment cost.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb6bfbd087b",
  "kind": "yes/no",
  "text": "Table caption: Validation of Correct Gene Fusion Generation by Overlap Extension PCR.\n|  | Step1 | Step1 | Step 2 & 3 |  |  |\n| Construct | Size of Fragment 1 (Kb) | Size of Fragment 2 (Kb) | Size of Final Gene Fusion (Kb) | Number of Clones Sequenced | Number Correct |\n| Gene fusion A | 0.95 | 0.44 | 1.4 | 5 | 4 |\n| Gene fusion B | 1.6 | 0.78 | 2.38 | 5 | 3 |\n| Gene fusion C | 1.0 | 1.1 | 2.1 | 5 | 5 |\n\nStatement: There are five Gene fusions .",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qf6075b5919",
  "kind": "yes/no",
  "text": "Table caption: Metrics of alternative draft assemblies.\n| Contig metrics | SPAdes v.3.6.0 | SPAdes v.3.6.0 | Newbler v.2.9 + HUMGGAT | Velvet v.1.2.0 | CLC v.8.5 | CLC v.8.5 | SPAdes v.3.13.0 | Unicycler v.0.4.8 |\n| Library type | Illumina paired-end | Illumina mate pair | Illumina paired-end; Illumina mate pair | Illumina paired-end | Illumina paired-end | Illumina mate pair | Illumina paired-end, Illumina mate pair, Oxford Nanopore | Illumina paired-end, Illumina mate pair, Oxford Nanopore |\n| Largest contig | 573,930 | 972,016 | 971,946 | 462,794 | 868,994 | 1883,967 | 1304,922 | 3347,597 |\n| Number of contigs ≥1000 bp | 43 | 45 | 22 | 47 | 45 | 18 | 16 | 10 |\n| N50 | 259,753 | 240,878 | 427,030 | 179,795 | 317,660 | 1283,905 | 794,261 | 3347,597 |\n\nStatement: There are ten alternative draft assemblies are given in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdf141e4cda",
  "kind": "yes/no",
  "text": "Table caption: Statistical metrics of performance evaluation comparing observed and predicted Ψ 90 .\n| Approach | n | FAC2 | MB | NMB | MAE | FB | RMSE | NMSE |\n| Approach 1 | 28 | 0.61 | 1.64 | 0.70 | 1.64 | −0.52 | 1.79 | 0.34 |\n| Approach 2 | 28 | 0.68 | −1.04 | −0.44 | 1.04 | 0.56 | 1.28 | 0.52 |\n| Approach 3 | 28 | 0.79 | 0.70 | 0.30 | 1.15 | −0.25 | 1.36 | 0.26 |\n\nStatement: They have 3 different approaches in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q11a431440d",
  "kind": "yes/no",
  "text": "Table caption: Chemical composition of OPC cement.\n| Chemical component | Percentage |\n| Al 2 O 3 | 4.42 |\n| Fe 2 O 3 | 3.71 |\n| SiO 2 | 21.08 |\n| MgO | 1.60 |\n| CaO | 63.78 |\n| SO 3 | 2.43 |\n| LOI | 2.20 |\n| IR | 1.44 |\n\nStatement: SO 3 Percentage is 2.20.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0b0d531fa0",
  "kind": "yes/no",
  "text": "Table caption: Physical and mechanical properties of granite dust.\n| № | Specification | Value |\n| 1 | Specific surface, m 2 /kg | 220 … 250 |\n| 2 | Bulk density, kg/m 3 | 920 … 970 |\n| 3 | Clay content, % | 0,2 … 0.5 |\n| 4 | Humidity, % | 0,3 … 0,5 |\n| 5 | Water soluble contaminants, % | none |\n\nStatement: There are five different Specification.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q7e945fe5df",
  "kind": "yes/no",
  "text": "Table caption: Discriminant validity (Fornell-Larcker criterion).\n| Constructs | BA | BP | CS | PI |\n| Brand Attitude (BA) | 0.934 * |  |  |  |\n| Brand Preference (BP) | 0.529 | 0.943 * |  |  |\n| Consumer satisfaction (CS) | 0.583 | 0.671 | 0.908 * |  |\n| Purchase Intentions (PI) | 0.694 | 0.717 | 0.779 | 0.867 * |\n\nStatement: There are some repeated values in the table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3ddd107041",
  "kind": "yes/no",
  "text": "Table caption: Obstetric Data\n|  | N | % |\n| Planned home birth | 33 | 63.5 |\n| Prolonged labor | 5 |  |\n| Breech | 2 |  |\n| Umbilical cord strangulation | 5 |  |\n| Meconium | 2 |  |\n| Shoulder dystocia | 4 |  |\n| Precipitous labor | 2 |  |\n| Partial abruption placentae | 1 |  |\n| Fetal bradycardia during delivery | 1 |  |\n| Normal delivery | 6 |  |\n| Labor not documented | 7 |  |\n| Unplanned out-of-hospital birth | 17 | 32.7 |\n| Resuscitative hysterotomy | 2 |  |\n| Precipitous labor | 5 |  |\n| Preterm labor | 12 |  |\n| Breech | 1 |  |\n| Unknown pregnancy | 2 |  |\n| Unknown intended location of delivery | 2 | 3.8 |\n\nStatement: Unknown intended location of delivery has the highest percent of 3.8.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qaff0484de9",
  "kind": "yes/no",
  "text": "Table caption: Products synthesized by [TEAH][OAc] catalyst under optimal conditions a .\n| Entry | R 1 | R 2 | 1,3-Dicarbonyl | Product | Time (min) | Yield b , c (%) |\n| 1 | pH | – | Dimedone | 6a | 20 | 91 [18] |\n| 2 | 4-ClC 6 H 4 | – | Dimedone | 6b | 18 | 92 [18] |\n| 3 | 4-O 2 NC 6 H 4 | – | Dimedone | 6c | 15 | 88 [18] |\n| 4 | 3-O 2 NC 6 H 4 | – | Dimedone | 6d | 18 | 82 [18] |\n| 5 | 4-CH 3 OC 6 H 4 | – | Dimedone | 6e | 30 | 90 [18] |\n| 6 | 4-CH 3 C 6 H 4 | – | Dimedone | 6f | 25 | 70 [18] |\n| 7 | 2,4-(Cl) 2 C 6 H 3 | – | Dimedone | 6g | 20 | 93 [18] |\n| 8 | 4-(CH 3 ) 2 NC 6 H 4 | – | Dimedone | 6h | 20 | 88 [18] |\n| 9 | 4-BrC 6 H 4 | – | Dimedone | 6i | 22 | 79 [18] |\n| 10 | 4-HOC 6 H 4 | – | Dimedone | 6j | 30 | 80 [18] |\n| 11 | (CH 3 ) 2 CHCH 2 | – | Dimedone | 6k | 40 | 57 This Work |\n| 12 | CH 3 CH 2 CH 2 | – | Dimedone | 6l | 35 | 50 This Work |\n| 13 | pH | – | Dimedone | 6m | 13 | 91 [19] |\n| 14 | 4-ClC 6 H 4 | – | Dimedone | 6n | 12 | 90 [19] |\n| 15 | 4-O 2 NC 6 H 4 | – | Dimedone | 6o | 10 | 89 [19] |\n| 16 | 3-O 2 NC 6 H 4 | – | Dimedone | 6p | 13 | 95 [19] |\n| 17 | 4-CH 3 OC 6 H 4 | – | Dimedone | 6q | 20 | 92 [19] |\n| 18 | 4- CH 3 C 6 H 4 | – | Dimedone | 6r | 35 | 92 [19] |\n| 19 | 4-HOC 6 H 4 | – | Dimedone | 6s | 20 | 91 [19] |\n| 20 | PhCHO | Et | Ethyl 3-oxobutanoate | 7a | 37 | 82 [19] |\n| 21 | 2-ClC 6 H 4 | Et | Ethyl 3-oxobutanoate | 7b | 32 | 89 [20] |\n| 22 | 4-BrC 6 H 4 | Et | Ethyl 3-oxobutanoate | 7c | 35 | 92 [20] |\n| 23 | 4-NO 2 C 6 H 4 | Et | Ethyl 3-oxobutanoate | 7d | 22 | 95 [20] |\n| 24 | 2,4-Cl, Cl C 6 H 4 | Et | Ethyl 3-oxobutanoate | 7e | 30 | 87 [20] |\n| 25 | 4-OCH 3 C 6 H 4 | Et | Ethyl 3-oxobutanoate | 7f | 35 | 78 [20] |\n| 26 | 4-CH 3 C 6 H 4 | Et | Ethyl 3-oxobutanoate | 7g | 35 | 75 [20] |\n| 27 | 4-OHC 6 H 4 | Et | Ethyl 3-oxobutanoate | 7h | 28 | 80 [20] |\n| 28 | 4-N(CH 3 ) 2 C6H4 | Et | Ethyl 3-oxobutanoate | 7i | 36 | 78 [20] |\n| 29 | pH | Et | methyl 3-oxobutanoate | 7j | 35 | 85 [20] |\n| 30 | 4-ClC 6 H 4 | Et | methyl 3-oxobutanoate | 7k | 30 | 87 [20] |\n\nStatement: Yield 57 and 90 works for (CH 3 ) 2 CHCH 2 and CH 3 CH 2 CH 2 reactions.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc1bb581800",
  "kind": "yes/no",
  "text": "Table caption: Alloying composition and elongation tensile test results of batches of Ti-45Al-(4–6) (X, Y)-1B, where X, Y Cr, Mn, Nb, Hf.\n| Alloys | 2Cr2Nb | 2Cr2Nb | 2Mn4Nb | 2Mn4Nb | 2Mn4Nb | 2Mn4Nb | 2Mn4Nb | 2Mn4Nb | 2Mn4Nb | 2Nb2Hf | 2Nb2Hf |\n| Num. samples | 1 | 2 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 1 | 2 |\n| El. (%) | 0.5 | 1.5 | 0.3 | 0.6 | 0.9 | 1.1 | 1.2 | 1.3 | 1.3 | 0.1 | 0.35 |\n| YS (MPa) | 518 | 489 | 529 | 508 | 515 | 539 | 532 | 520 | 489 | – | 582 |\n| UTS (MPa) | 590 | 682 | 550 | 599 | 670 | 680 | 695 | 700 | 664 | 572 | 634 |\n\nStatement: Only Sample 1 of Alloy 2Nb2Hf has 0.1 El. (%).",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q8b8e6b9fc7",
  "kind": "yes/no",
  "text": "Table caption: Regression of ideology on self-ratings and socio-demographics.\n| Dependent variable: | SDO | RWA |\n| S (self) | 0.07 | −0.09* |\n| E (self) | −0.06 | −0.04 |\n| O (self) | −0.24 *** | −0.53 *** |\n| A (self) | −0.22 *** | −0.01 |\n| C (self) | −0.01 | 0.20 *** |\n| Gender (male) | 0.10* | 0.01 |\n| Higher education | 0.02 | −0.24 *** |\n| Age (in years) | 0.02 | −0.02 |\n| R 2 (in %) | 13.5 | 42.7 |\n| n | 611 | 611 |\nTable notes: Note: Entries indicate yx -standardized regression coefficients, Significance levels: * p < 0.05, ** p < 0.01, *** p < 0.001. S = Emotional stability , E = Extraversion , O = Openness to experience , A = Agreeableness , C = Conscientiousness , SDO = social dominance orientation , RWA = right-wing authoritarianism.\n\nStatement: S (self) social dominance orientation is 0.07.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb768c4c94e",
  "kind": "yes/no",
  "text": "Table caption: Properties of the source and target structures for the heterogeneous population case study with geometric and material differences.\n| Property | Unit | Source | Target |\n| Beam geometry, { l b , w b , t b } | mm | { 5000 , 350 , 350 } | { 4300 , 500 , 500 } |\n| Mass geometry, { l m , w m , t m } | mm | { 12000 , 12000 , 350 } | { 10000 , 10000 , 500 } |\n| Elastic modulus, E | GPa | N 210 , 1 × 10 - 9 | N 71 , 75 × 10 - 7 |\n| Density, ρ | kg / m 3 | N 8000 , 10 | N 2700 , 2 . 5 |\n| Damping coefficient, c | Ns / m | G 50 , 0.1 | G 8 , 0.8 |\n\nStatement: Only Elastic modulus, E is measured in GPa unit.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qd31f193629",
  "kind": "yes/no",
  "text": "Table caption: Results of mediation analyses in Study 1 and Study 2 predicting academic performance and dropout intention via academic effort: total, direct, and indirect effects of motivational regulation strategies (after controlling for high school GPA).\n|  | Study 1 | Study 1 | Study 1 |  |  |  | Study 2 | Study 2 | Study 2 |  |  |  |\n|  | Academic performance ( N = 145) | Academic performance ( N = 145) | Academic performance ( N = 145) | Dropout intention ( N = 240–241) | Dropout intention ( N = 240–241) | Dropout intention ( N = 240–241) | Academic performance ( N = 180) | Academic performance ( N = 180) | Academic performance ( N = 180) | Dropout intention ( N = 186) | Dropout intention ( N = 186) | Dropout intention ( N = 186) |\n| Motivational regulation strategies | c | c’ | ab (95% CI) | c | c’ | ab (95% CI) | c | c’ | ab (95% CI) | c | c’ | ab (95% CI) |\n| Overall strategy score | −0.32 | −0.23 | −0.09 (−0.19/0.01) | −0.15 | −0.02 | −0.13 (−0.21/−0.05) | −0.13 | −0.05 | −0.08 (−0.16/−0.02) | −0.16 | −0.03 | −0.13 (−0.23/−0.04) |\n| Mastery self−talk | −0.31 | −0.21 | −0.09 (−0.20/0.01) | −0.15 | −0.03 | −0.12 (−0.19/−0.05) | −0.15 | −0.07 | −0.08 (−0.16/−0.02) | −0.21 | −0.10 | −0.11 (−0.22/−0.03) |\n| Performance−approach self−talk | −0.20 | −0.05 | −0.15 (−0.27/−0.05) | −0.20 | −0.10 | −0.10 (−0.18/−0.03) | −0.18 | −0.11 | −0.07 (−0.14/−0.01) | −0.26 | −0.15 | −0.11 (−0.21/−0.02) |\n| Performance−avoidance self−talk | −0.16 | −0.11 | −0.05 (−0.10/−0.01) | 0.01 | 0.05 | −0.04 (−0.08/−0.01) | −0.02 | 0.00 | −0.02 (−0.06/0.02) | 0.03 | 0.06 | −0.03 (−0.09/0.02) |\n| Enhancement of situational interest | −0.16 | −0.14 | −0.03 (−0.08/0.02) | 0.02 | 0.05 | −0.03 (−0.07/0.01) | 0.00 | 0.04 | −0.04 (−0.09/−0.00) | −0.04 | 0.01 | −0.05 (−0.12/0.00) |\n| Enhancement of personal significance | −0.20 | −0.16 | −0.03 (−0.09/0.01) | −0.03 | 0.01 | −0.03 (−0.08/0.00) | −0.13 | −0.09 | −0.04 (−0.09/−0.00) | −0.16 | −0.10 | −0.06 (−0.14/−0.01) |\n| Environmental control | −0.11 | −0.03 | −0.08 (−0.14/−0.03) | −0.10 | −0.02 | −0.08 (−0.14/−0.04) | −0.09 | 0.01 | −0.10 (−0.18/−0.03) | −0.00 | 0.18 | −0.18 (−0.29/−0.09) |\n| Proximal goal setting | −0.15 | −0.04 | −0.11 (−0.19/−0.05) | −0.13 | −0.05 | −0.09 (−0.15/−0.04) | −0.12 | −0.06 | −0.06 (−0.11/−0.01) | −0.12 | −0.03 | −0.09 (−0.18/−0.02) |\n| Self−consequating | −0.15 | −0.10 | −0.05 (−0.11/−0.01) | −0.09 | −0.03 | −0.06 (−0.12/−0.02) | −0.06 | 0.01 | −0.07 (−0.13/−0.02) | −0.08 | 0.02 | −0.10 (−0.18/−0.03) |\nTable notes: Note. c = standardized regression coefficient of the total effect. c’ = standardized regression coefficient of the direct effect . ab = standardized regression coefficient of the indirect effect. CI = lower and upper limit of the percentile bootstrap 95%−confidence interval for the indirect effect based on 10,000 samples.\n\nStatement: The lowest c is -0.03.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qcbb92ba3b8",
  "kind": "yes/no",
  "text": "Table caption: Users’ features.\n| Feature | Description | Origin | Anon. | Domain |\n| _id | It contains the user’s ID ? . | Twitter | ✔ | UUID |\n| scores.categories.content | Score indicating an analysis of the content and language of the user’s tweets † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.categories.friend | Score expressing how the user behaves with other users in terms of follower-friend relations and types of tweets † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.categories.network | Score representing the interconnections with other users † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.categories.sentiment | Score focusing on the emotion and attitude of the user’s tweets † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.categories.temporal | Score studying the behavior of the user along time † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.categories.user | Score analyzing the user’s metadata † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.scores.english | Overall classification results † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.scores.universal | Overall classification results without English-based features † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.cap.english | Probability that the user’s account is completely automated. It uses all six feature categories † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.cap. universal | Probability that the user’s account is completely automated. It excludes sentiment and content feature categories † . | Botometer | ✘ | R ∈ [0,1] |\n| scores.display_scores.english | Value of scores.scores.english multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.universal | Value of scores.scores.universal multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.content | Value of scores.categories.content multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.friend | Value of scores.categories.friend multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.network | Value of scores.categories.network multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.sentiment | Value of scores.categories.sentiment multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.temporal | Value of scores.categories.temporal multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| scores.display_scores.user | Value of scores.categories.user multiplied by 5 † . | Botometer | ✘ | R ∈ [0,5] |\n| followers | List of Twitter users’ ID representing the followers of the user ? . | Twitter | ✔ | UUID |\n| friends | List of Twitter users’ ID representing the friends (i.e., followings) of the user ? . | Twitter | ✔ | UUID |\nTable notes: ? Twitter , † Botometer , R : Real numbers.\n\nStatement: The table has five heads -Feature ,Description ,Origin ,Anon and Domain.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb27a2855d6",
  "kind": "yes/no",
  "text": "Table caption: Frequency of IgE reactivity to major HDM allergens in relation to clinical symptoms.\n|  | nDer p 1 | nDer p 2 | rDer p 2.0101 | rDer p 23 | nDer p 1 or nDer p 2 | rDer p 23 only | Any |\n| All | 72.1% | 81.7% | 78.3% | 70.9% | 90.4% | 4.6% | 95.0% |\n| AA | 83.0% | 83.3% | 82.4% | 82.4% | 90.8% | 4.5% | 95.3% |\n| AR | 62.5% | 80.0% | 74.7% | 60.7% | 90.0% | 4.7% | 94.7% |\n\nStatement: rDer p 23 only ranges from 5.5% to 6.7%.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q730fb42aff",
  "kind": "yes/no",
  "text": "Table caption: CMVs and RMVs regarding the performance indicator “The cumulative impact factor value”.\n|  | Current minimum values | Cumulative impact factor, 2014–2018 | Cumulative impact factor, 2014–2018 | Number of years required to fulfill minimum criteria | Number of years required to fulfill minimum criteria | Recalibrated minimum values | Recalibrated minimum values |\n|  |  | IC | FC | IC | FC | IC | FC |\n| Mining | 4 | 8.815 | 3.202 | 2.269 | 6.247 | 3 (2.521) | 0.916 |\n| Geology | 8 | 43.677 | 9.120 | 0.916 | 4.386 | 12 (12.492) | 2.608 |\n| Geodesy and Geoinformatics | 4 | 10.484 | 3.253 | 1.908 | 6.147 | 3 (2.998) | 0.930 |\n| Geophysics | 8 | 28.144 | 5.695 | 1.421 | 7.023 | 8 (8.049) | 1.629 |\n| Geochemistry, Mineralogy and Petrology | 8 | 51.888 | 8.854 | 0.771 | 4.518 | 15 (14.840) | 2.532 |\n| Meteorology | 8 | 36.650 | 6.498 | 1.091 | 6.156 | 10 (10.482) | 1.858 |\n| Paleontology | 8 | 38.067 | 6.710 | 1.051 | 5.961 | 11 (10.887) | 1.919 |\n| Social Geography | 2 | 4.104 | 1.198 | 2.436 | 8.346 | 1 (1.174) | 0.343 |\n| Physical Geography | 4 | 19.950 | 4.246 | 1.002 | 4.710 | 6 (5.706) | 1.214 |\n\nStatement: Cumulative impact factor, 20142018, Number of years required to fulfill minimum criteria, and Recalibrated minimum values has 2 groups such as IC and FC.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qde688cae05",
  "kind": "yes/no",
  "text": "Table caption: Overview of whole genome bisulphite sequencing (WGBS) and RNA-Seq.\n|  | GC1Y | GC3Y |\n| Total WGBS Reads | 17,032.35 Mb | 19,049.74 Mb |\n| Mapping efficiency | 74.9% | 77.3% |\n| mCG_ratio | 78.9% | 78.2% |\n| mCHG_ratio | 0.4% | 0.4% |\n| mCHH_ratio | 0.5% | 0.4% |\n| Read Depth (X) | 37.85 | 42.33 |\n| Conversion Rate | 99.73% | 99.71% |\n| Total RNA-Seq Reads | 353.59 Mb | 358.96 Mb |\n| Total mapped reads | 287.47 Mb (81.3%) | 288.15 Mb (80.3%) |\n| perfect match | 222.33 Mb (62.9%) | 220.38 Mb (61.4%) |\n| Unique match | 265.85 Mb (75.2%) | 261.03 Mb (72.7%) |\n| Total Unmapped Reads | 66.13 Mb (18.7%) | 70.81 Mb (19.7%) |\n\nStatement: GC1Y for Total RNA-Seq Reads is 123.45 Mb.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q31a852ae6d",
  "kind": "yes/no",
  "text": "Table caption: Comparative LF oscillation amplitude for analytical and simulation results.\n| Case | A ′ | BP osc. ampl. (mmHg) | Osc. freq. (Hz) |\n| Analytical soln. | 16.4504 | ∼ 1.38 | 0.317 |\n| Simulation | 15.1 | ∼ 1.34 | 0.307 |\n\nStatement: The lowest BP is 350.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q084618f6d4",
  "kind": "yes/no",
  "text": "Table caption: Columns data type.\n| No | Column | Count | Data type |\n| 1 | responses_header | 16,659 | object |\n| 2 | responses_rating_grade | 11,222 | float64 |\n| 3 | responses_status | 7559 | object |\n| 4 | responses_message | 16,659 | object |\n| 5 | responses_datetime | 16,659 | datetime64[ns] |\n| 6 | reviewer | 16,659 | object |\n| 7 | comments | 16,659 | int64 |\n| 8 | views | 16,659 | int64 |\n| 9 | id | 16,659 | int64 |\n| 10 | have_email | 16,659 | int64 |\n| 11 | responses_message_length | 16,659 | int64 |\n| 12 | gunning_fog_index | 16,659 | float64 |\n| 13 | binary_score | 16,659 | object |\n\nStatement: There are thirteen different type of Columns data type.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q96bbd35c5b",
  "kind": "yes/no",
  "text": "Table caption: Mean, Standard Deviation, Skewness, and Kurtosis.\n| Items | Mean | Standard Deviation | Kurtosis | Skewness |\n| FL1 | 3.117 | 0.799 | 0.702 | −0.438 |\n| FL2 | 3.610 | 1.123 | −0.117 | −0.709 |\n| FL3 | 3.310 | 1.011 | −0.339 | −0.296 |\n| FL4 | 3.376 | 0.993 | −0.039 | −0.492 |\n| FL5 | 3.089 | 0.809 | 0.063 | 0.050 |\n| FL6 | 3.404 | 0.991 | −0.133 | −0.357 |\n| PI1 | 3.362 | 0.902 | 0.261 | −0.199 |\n| PI2 | 3.056 | 0.870 | −0.119 | 0.062 |\n| PI3 | 3.000 | 0.856 | 0.506 | −0.091 |\n| PI4 | 3.329 | 0.922 | −0.280 | 0.024 |\n| PI5 | 2.915 | 0.936 | −0.108 | 0.204 |\n| PI6 | 3.150 | 0.907 | 0.385 | −0.150 |\n| SC1 | 2.408 | 1.205 | −0.466 | 0.597 |\n| SC2 | 2.244 | 1.161 | −0.435 | 0.671 |\n| SC3 | 2.113 | 1.302 | −0.154 | 1.022 |\n| SC4 | 2.615 | 1.253 | −0.793 | 0.371 |\n| SC5 | 2.563 | 1.101 | −0.369 | 0.549 |\n| SC6 | 2.479 | 1.232 | −0.667 | 0.542 |\n| SC7 | 2.690 | 1.047 | −0.427 | 0.228 |\n| SC8 | 2.676 | 1.072 | −0.580 | 0.146 |\n| SC9 | 3.047 | 1.091 | −0.534 | 0.059 |\n| IB1 | 3.516 | 1.086 | −0.431 | −0.43 |\n| IB2 | 3.812 | 1.223 | 0.054 | −0.97 |\n| IB3 | 3.836 | 1.269 | −0.031 | −1.005 |\n| IB4 | 3.653 | 1.118 | 0.016 | −0.763 |\n| IB5 | 3.502 | 1.095 | −0.502 | −0.341 |\n| IB6 | 3.690 | 1.006 | 0.617 | −0.907 |\n| IB7 | 3.620 | 1.075 | 0.239 | −0.747 |\n| IB8 | 3.596 | 1.103 | −0.226 | −0.563 |\n| IB9 | 2.624 | 1.083 | −0.163 | 0.546 |\n\nStatement: Skewness 0.059 Items is SC9.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc42732b723",
  "kind": "yes/no",
  "text": "Table caption: Results from the official test set of the ISIC 2019 Challenge for each class. We consider the AUC, the AUC for a sensitivity larger than 80% (AUC-S), the sensitivity and specificity. Note that the sensitivity given here is differently calculated than S. Values are given in percent.\n| Class | Task1 | Task1 | Task1 | Task1 | Task2 | Task2 | Task2 | Task2 |\n|  | AUC | AUC-S | Sens. | Spec. | AUC | AUC-S | Sens. | Spec. |\n| MEL | 0.928 | 0.849 | 0.594 | 0.962 | 0.931 | 0.849 | 0.545 | 0.976 |\n| NV | 0.96 | 0.93 | 0.71 | 0.975 | 0.96 | 0.932 | 0.637 | 0.983 |\n| BCC | 0.949 | 0.904 | 0.721 | 0.94 | 0.947 | 0.901 | 0.649 | 0.958 |\n| AK | 0.914 | 0.824 | 0.484 | 0.965 | 0.919 | 0.841 | 0.46 | 0.966 |\n| BKL | 0.904 | 0.805 | 0.394 | 0.985 | 0.908 | 0.821 | 0.324 | 0.991 |\n| DF | 0.979 | 0.963 | 0.578 | 0.992 | 0.98 | 0.965 | 0.556 | 0.993 |\n| VASC | 0.956 | 0.925 | 0.644 | 0.991 | 0.942 | 0.912 | 0.495 | 0.995 |\n| SCC | 0.938 | 0.876 | 0.439 | 0.986 | 0.93 | 0.878 | 0.408 | 0.987 |\n| UNK | 0.775 | 0.581 | 0.00283 | 0.999 | 0.612 | 0.253 | 0 | 0.999 |\n\nStatement: The value of UNK is 8 under task 2 for Sens.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q003b9aac0a",
  "kind": "yes/no",
  "text": "Table caption: Technical parameters of the ABS filament used in the tests.\n| Physical properties | Density [kg/m 3 ] | Tensile strength [MPa] | Young module [MPa] | Poisson’s ratio |\n| Value | 1050 | 44 | 2000 | 0.38 |\n\nStatement: Value Young module [MPa] is .038.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qa6715de80b",
  "kind": "yes/no",
  "text": "Table caption: Linear regression model statistics of raw point count species richness and time-of-day. Results listed for each acoustic index, with intercept, F-statistic, p value, R 2 , residual standard error, and degrees of freedom for each. Indices assessed were: Acoustic Complexity (AC); Acoustic Diversity (AD); Acoustic Evenness (AE); and Normalised Difference in Soundscape Index (NDSI).\n| Linear Model | Intercept | F | p-value | R 2 | Residual standard error | Degrees of freedom |\n| BI ~ Raw species richness | 0.04 | 6.537 | 0.05 | 0.005 | 2.69 | 1145 |\n| AC ~ Raw species richness | 23.76 | 54.79 | <0.001 | 0.046 | 517.7 | 1132 |\n| AD ~ Raw species richness | −0.009 | 7.374 | <0.001 | 0.006 | 0.562 | 1132 |\n| AE ~ Raw species richness | 0.007 | 25.74 | <0.001 | 0.021 | 0.27 | 1145 |\n| NDSI ~ Raw species richness | 0.006 | 14.17 | <0.001 | 0.012 | 0.295 | 1145 |\n| BI ~ Time-of-day | −0.004 | 15.98 | <0.001 | 0.013 | 2.679 | 1145 |\n| AC ~ Time-of-day | −1.515 | 56.97 | <0.001 | 0.047 | 517.2 | 1132 |\n| AD ~ Time-of-day | 0.0001 | 0.487 | 0.485 | <0.001 | 0.563 | 1132 |\n| AE ~ Time-of-day | −0.0002 | 3.508 | 0.061 | 0.003 | 359.4 | 1132 |\n| NDSI ~ Time-of-day | 0.0009 | 58.71 | <0.001 | 0.049 | 0.289 | 1132 |\n\nStatement: Degrees of freedom is differentiated into 1145 and 1132.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q0adbad1c8d",
  "kind": "yes/no",
  "text": "Table caption: Top 10 journals for publications related to food security.\n| Journal | Number of Articles |\n| Food Policy | 309 |\n| Food Security | 303 |\n| PLoS ONE | 199 |\n| Public Health Nutrition | 183 |\n| Journal of Hunger and Environmental Nutrition | 154 |\n| Sustainability | 145 |\n| World Development | 141 |\n| Transactions of the Chinese Society of Agricultural Engineering | 128 |\n| Global Food Security | 127 |\n| Journal of Nutrition | 113 |\n| Agricultural Systems | 109 |\n| Food and Nutrition Bulletin | 103 |\n| Agriculture and Human Values | 98 |\n| Field Crops Research | 95 |\n\nStatement: Field Crops Research has less Number of Articles of 95.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qb3113e66ad",
  "kind": "yes/no",
  "text": "Table caption: Features of the Paenibacillus curdlanolyticus B-6 genome.\n| Feature | Description |\n| Number of reads used in the assembly | 45,085,168 |\n| Mean read length | 195 bp |\n| Genome size | 4,875,097 bp |\n| Number of contigs | 74 |\n| G+C content (%) | 49.7 |\n| N50 contig length | 237,553 bp |\n| Mean contig length | 65,880 bp |\n| Number of CDSs | 4,473 |\n| Number of rRNAs | 4 |\n| Number of tRNAs | 94 |\n| Number of CRISPRs | 5 |\n| Genome coverage depth | 1,718-fold |\n\nStatement: There are 12 different types of Feature in the given table.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q3422a539b5",
  "kind": "yes/no",
  "text": "Table caption: Patient inclusion and exclusion criteria for the AL specified for the case hospital.\n| Category | Status | Age | ASA | Specialties |\n| CW | Non-elective | ≥ 86 | IV, V | – |\n| Grey | – | 76–85 | III | BAR |\n| AL | Elective | 18–75 | I, II | CHI, KAA, NCH, ORT, PLA, URO |\n\nStatement: Category AL Specialties are CHI, KAA, NCH, ORT, PLA, URO",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qdeaa28e85b",
  "kind": "yes/no",
  "text": "Table caption: Computing time t > 1 per order (in seconds).\n| Instance set | Sequential | Integrated | Split | Timesplit |\n| 50 | 0.01 | 0.03 | 0.03 | 0.08 |\n| 150 | 0.01 | 0.21 | 0.4 | 0.62 |\n| 250 | 0.01 | 0.48 | 1.06 | 1.34 |\n\nStatement: The highest time split is 0.08.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 }
]
