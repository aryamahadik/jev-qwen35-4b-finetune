"""NVX-101 first-in-human volunteer screening and St Aldric's thrombolysis eligibility."""
from common import (Y, C, T, card, crit, NONE, PH_INC, PH_EXC, PH_NONE, STROKE, STROKE_NONE)

PE_OPTS, PE_CARD = crit(PH_EXC, PH_NONE)               # 25 options
PA_OPTS, PA_CARD = crit(PH_INC + PH_EXC, PH_NONE)      # 28 options
S_OPTS, S_CARD = crit(STROKE, STROKE_NONE)             # 10 options
S_YCARD = card(STROKE)

ITEMS = [
# P1: alcohol 4 x 568 mL x 5% = 11.36 u; 3 x 175 mL x 13% = 6.83 u -> 18.2 > 14 -> E6.
# Flu vaccine 20 d before dosing (ok), BMI 29.8 (ok). Twin: one glass -> 13.6 u -> none of these.
C("Which NVX-101 exclusion criterion applies to this volunteer? (Screening SOP: if several apply, record the lowest-numbered one.)",
"""Harwell Clinical Pharmacology Unit - NVX-101 Part A screening record
Volunteer: Mr Callum Oduya-Strand, 34, male | Screening: 18 August 2025 | Planned dosing: 1 September 2025

Measurements: height 1.75 m; weight 91.2 kg. Seated BP 138/88 mmHg; HR 64/min. ECG: QTcF 432 ms, PR 168 ms.

Lifestyle questionnaire
- Tobacco/nicotine: smoked 10/day until December 2024, none since; no vapes or nicotine replacement.
- Alcohol, typical week: "four pints (568 mL each) of 5% lager on a Friday night, and three 175 mL glasses of 13% red wine over the weekend. Nothing Monday to Thursday."
- Caffeine: 3 cups of coffee per day.
- Exercise: 5-a-side football once a week; agrees to stop from 72 h before admission.

Medicines: paracetamol 1 g occasionally for headaches; nothing else. Influenza vaccine on 12 August 2025.

Blood donation: never. Previous studies: none.
Labs: serology negative; drug screen negative; ALT 31 U/L (ULN 45); bilirubin 0.7 mg/dL (ULN 1.2); eGFR 102.
Other: no allergies; no psychiatric history; works as a bus driver; available for the residential period.
""",
PE_OPTS, "E6 alcohol", 3, PE_CARD,
twin=T([("three 175 mL glasses of 13% red wine", "one 175 mL glass of 13% red wine")], NONE)),

# P2: caffeine 3x100 + 2x80 + 1x40 + 2x50 = 600 mg > 500 -> E22. Blood donation 470 mL 100 d before dosing (ok).
# Twin: donation 80 d before dosing -> E8, which is lower-numbered than E22.
C("Following the unit's rule of recording the lowest-numbered exclusion that applies, which NVX-101 exclusion criterion should be entered for this volunteer?",
"""NVX-101 volunteer screening - interview notes (research nurse Beatrix Onwuachi)
Volunteer: Ms Petra Lindgren-Achebe, 27, female | Planned dosing: 9 September 2025

Vitals: BP 118/74 mmHg, HR 72/min; height 1.68 m, weight 63.0 kg; QTcF 461 ms; PR 150 ms.
Contraception: combined oral contraceptive pill, taken correctly for 3 years; agrees to continue. Pregnancy test negative.

Diet and habits (typical working day):
- "Three mugs of coffee - one before work, two at my desk."
- "Two cans of energy drink on shift, and a can of cola with lunch."
- "Two cups of tea in the evening."
- Alcohol: about 6 units at weekends. Never smoked or vaped.

Blood donation: she donated 470 mL of whole blood at a community session on 1 June 2025. No plasma donation.

Medication: none apart from the pill. No herbal products. No grapefruit. No vaccines this year.
Previous research: none.
Labs normal; drug screen negative; serology negative.

Nurse comment: "Lovely volunteer, drinks a lot of caffeine but says she can cut down during the study."
""",
PE_OPTS, "E22 caffeine", 3, PE_CARD,
twin=T([("on 1 June 2025", "on 21 June 2025")], "E8 blood donation")),

# P3: prior study drug half-life 30 d -> 5 half-lives = 150 d > 90 d; last dose 11 May -> dosing 8 Sep = 120 d -> E9.
# HCV Ab+ with RNA undetectable after cure (ok), Gilbert documented (ok), plasma 20 d ago (ok).
C("Checking the NVX-101 criteria in their listed order, which is the first one that this volunteer fails?",
"""NVX-101 screening - PI eligibility review
Volunteer: Mr Anselm Kowalczyk-Ibe, 41, male | Planned dosing: 8 September 2025

Previous research participation (verified through the volunteer register):
- Study LTX-440-101 (another unit): single dose of LTX-440 on 11 May 2025. The LTX-440 participant information sheet states a terminal half-life of about 30 days. Follow-up completed in July 2025.

Plasma donation: 19 August 2025 (plasmapheresis centre). No whole-blood donation this year.

Serology: HIV antibody negative; HBsAg negative; hepatitis C antibody POSITIVE. HCV RNA undetectable (tested at screening). Treated with sofosbuvir/velpatasvir for 12 weeks in 2021 with documented sustained virological response.

Liver tests: ALT 28 U/L (ULN 45); AST 25 U/L (ULN 40); total bilirubin 1.4 mg/dL (ULN 1.2). Gilbert syndrome documented by his GP in 2012.

Vitals: BP 128/82 mmHg; HR 58/min; BMI 24.6; QTcF 418 ms.
Habits: non-smoker; 8 units alcohol/week; 2 coffees/day.
Urine drug screen negative. Medicines: none. Consent read and signed in English; available for the 6-night stay.
""",
PA_OPTS, "E9 prior study", 3, PA_CARD),

# P4: BP repeat 138/86 used (ok); HR 48 (ok); QTcF 462 woman (ok); St John's wort stopped 21 d before dosing
# -> E10 not (7 d window) but E11 (28 d) applies. Grapefruit 9 d before (ok).
C("Which exclusion criterion should be recorded for this NVX-101 volunteer? Record the lowest-numbered one if more than one applies.",
"""NVX-101 - screening day checklist (Volunteer 2-0318)
Ms Oona Brightman-Sesay, 36, female | Screening 1 October 2025 | Planned dosing 15 October 2025

Vital signs
- Seated BP, first reading: 146/88 mmHg. Repeat after 10 minutes' rest: 138/86 mmHg.
- Resting HR 48/min (runs half-marathons).
- ECG: QTcF 462 ms; PR 176 ms.
- Height 1.70 m; weight 66.5 kg.

Medication and supplement history (volunteer interview)
- Took St John's wort capsules (over the counter) "for low mood in the winter", last capsule on 24 September 2025. Stopped because the unit's advert mentioned herbal remedies.
- Levonorgestrel intrauterine system in place since 2022.
- No other medicines, vitamins or supplements.

Diet: drank grapefruit juice with breakfast until 6 October 2025, none since. Coffee 2 cups/day. Alcohol 4 units/week. Never smoked.
No vaccines, blood or plasma donation, or previous studies in the past year.
Labs normal; drug screen negative; serology negative; pregnancy test negative.
""",
PE_OPTS, "E11 enzyme inducers", 3, PE_CARD),

# P5: weight 49.5 kg < 50.0 -> E1 (BMI 19.3 within range). All inclusion criteria met.
C("Taking the NVX-101 inclusion and exclusion criteria in their listed order, which is the first criterion this volunteer does not satisfy?",
"""Volunteer screening summary - NVX-101 (Harwell CPU)
Volunteer: Ms Yuki Farrant-Obi, 23, female | Screening: 4 November 2025

- Height 1.60 m, weight 49.5 kg (BMI 19.3 kg/m2). "I've always been slim, my weight never changes."
- Seated BP 108/66 mmHg; HR 52/min; QTcF 441 ms; PR 142 ms.
- Nicotine: used a vape (nicotine salts) until early July 2025; nicotine-free since.
- Alcohol: 5 units/week. Caffeine: 2 teas/day.
- Contraception: progestogen-only implant, agrees to continue.
- Medicines: none. Vaccines: none since 2024. Never donated blood or plasma.
- Previous research: none. Not employed by the site or sponsor.
- Serology negative; urine drug screen negative; ALT 14 U/L; eGFR 118.
- Read and signed the English consent form; available for the full residential period.

Nurse note: "Veins small but cannulation successful first time on both arms."
""",
PA_OPTS, "E1 body size", 2, PA_CARD),

# P6: DOB 2 May 1969, screening 10 June 2025 -> 56 -> I1 fails (agency record says 55).
C("In the listed order of the NVX-101 criteria, which is the first one this volunteer fails?",
"""Recruitment agency referral (Clearwater Volunteers) and unit screening notes

Agency record (registered 20 March 2024): Florian Mbatha-Kerr, male, age 55, DOB 02/05/1969, healthy, non-smoker.

Unit screening visit - 10 June 2025
- Identity checked against passport: DOB 2 May 1969.
- Height 1.82 m, weight 84.0 kg (BMI 25.4). BP 132/84 mmHg; HR 61/min.
- ECG: QTcF 449 ms; PR 198 ms.
- Smoking: stopped cigarettes 4 months ago (early February 2025); no nicotine products since.
- Alcohol: about 12 units/week. Caffeine: 3 coffees/day.
- Medicines: none. No herbal remedies. No vaccines this year.
- Blood donation: last whole-blood donation 18 months ago.
- Previous research: one study in 2022.
- Labs: ALT 40 U/L (ULN 45); bilirubin normal; eGFR 88; serology negative; drug screen negative.
- Reads and understands English; retired, fully available for the residential stay.

Screener comment: "Agency says 55, so he is inside the age range. QTcF close to the limit - PI to review."
""",
PA_OPTS, "I1 age", 2, PA_CARD),

# P7: every near-miss is inside the limits -> none of these.
# plasma 16 d (>=14), Shingrix 15 d (>14), QTcF 448 man, caffeine 490, alcohol 10.9 u, ALT 1.45x, prior study
# 100 d with 2-day half-life (>=90), BP repeat 136/88, BMI 29.9, grapefruit 8 d, paracetamol 1 g/day.
C("Which NVX-101 exclusion criterion, if any, applies to this volunteer?",
"""NVX-101 screening - Volunteer 3-0442: Mr Tariq Hollingsworth-Abe, 30, male
Planned dosing: 20 October 2025

- Height 1.776 m; weight 94.3 kg.
- Seated BP 144/92 mmHg; repeat after 10 minutes 136/88 mmHg. HR 74/min.
- ECG: QTcF 448 ms; PR 184 ms.
- Plasma donation (plasmapheresis) on 4 October 2025. No whole-blood donation this year.
- Recombinant zoster vaccine (Shingrix) on 5 October 2025, as part of his occupational health programme.
- Previous research: dosed with a study drug (terminal half-life 2 days) on 12 July 2025; completed follow-up.
- Caffeine: 4 coffees and 1 can of cola per day, plus 1 cup of tea.
- Alcohol, typical week: six 330 mL bottles of 4.5% beer and two 25 mL measures of 40% whisky.
- Paracetamol 1 g daily for a sore knee over the past week; no other medicines, supplements or herbal products.
- Grapefruit: ate half a grapefruit on 12 October 2025, none since.
- Labs: ALT 58 U/L (ULN 40); AST 36 U/L (ULN 40); bilirubin 0.9 mg/dL (ULN 1.2); eGFR 84; serology and drug screen negative.
- Never smoked. No allergies, surgery or psychiatric history. Works in a warehouse, not for the site or sponsor.
""",
PE_OPTS, NONE, 3, PE_CARD),

# ------------------------------------------------------------------ St Aldric's thrombolysis
# S1: LKW = documented awakening at 02:30 (normal speech/walking) -> bolus 06:40 = 4 h 10 min -> eligible.
# Twin: awakening at 01:50 -> 4 h 50 min -> not eligible.
Y("Can thrombolysis be given to Mrs Castellane-Obi with the bolus planned for 06:40?",
"""St Aldric's Hospital - Hyperacute stroke proforma
Patient: Mrs Winifred Castellane-Obi, 74 | Arrival: 05:58

History from husband: she went to bed at 23:15, completely normal. At 02:30 (he checked the bedside clock) she got up to use the toilet; he spoke with her, she answered normally and walked back to bed without help. At 05:20 he woke to find her unable to lift her right arm, with slurred speech and a right facial droop. Ambulance called 05:24.

Examination: NIHSS 9 (right arm and leg weakness, dysarthria, facial palsy).
BP 172/94 mmHg. Glucose 7.8 mmol/L. Platelets 230 x10^9/L. INR 1.0.
CT head 06:15: no haemorrhage, no established infarct. CT angiogram: left M2 occlusion.

Medication: aspirin 75 mg, ramipril, atorvastatin. No anticoagulants.
History: hypertension; no previous stroke, head injury or intracranial haemorrhage; no surgery or bleeding in the past 3 months.

Stroke registrar: "Found with symptoms on waking, so really a wake-up stroke. Consent discussed with husband; bolus drawn up for 06:40."
""",
1, 3, S_YCARD,
twin=T([("At 02:30 (he checked the bedside clock)", "At 01:50 (he checked the bedside clock)")], 0)),

# S2: apixaban last dose 30 h before decision, no level available -> anticoagulant contraindication.
# Arthroscopy 20 d ago (not within 14 d, not major), glucose 2.9 (not < 2.8), platelets 104.
C("Which contraindication from the St Aldric's thrombolysis protocol applies to this patient, if any?",
"""St Aldric's Hospital - Stroke thrombolysis checklist
Patient: Mr Ruben Adair-Nkemelu, 79 | Date: Thursday | Decision time: 14:20

Onset: witnessed at 13:10 by his daughter (sudden left-sided weakness while eating lunch). Arrival 13:45. CT: no haemorrhage.

Medication: apixaban 5 mg twice daily for atrial fibrillation. Daughter: "He ran out and hasn't taken any since Wednesday - no wait, his last tablet was the Wednesday breakfast dose, about 08:00 yesterday." Aspirin 75 mg (also still taking). Anti-Xa assay: not available at this hospital.

Bloods: glucose 2.9 mmol/L (fingerstick, repeated in lab 3.0); platelets 104 x10^9/L; INR 1.3.
BP 178/96 mmHg.

Past history: right knee arthroscopy (day case, local anaesthetic) 20 days ago. No previous stroke or intracranial bleed. No GI or urinary bleeding.

Registrar note: "Not really anticoagulated as he ran out. Glucose on the low side - recheck."
""",
S_OPTS, "anticoagulant", 2, S_CARD),

# S3: 198/112 -> 191/108 after dose 1 -> 184/104 after dose 2 -> controlled within two doses -> BP does not bar.
# Twin: 187/104 after two doses -> BP bars thrombolysis.
Y("Under the St Aldric's protocol, does this patient's blood pressure rule out thrombolysis?",
"""St Aldric's Hospital - Stroke team nursing record
Patient: Mr Leopold Farrington-Ade, 66 | Onset 16:05 (witnessed) | Arrival 16:40

CT 16:52: no haemorrhage. NIHSS 7. Glucose 6.4 mmol/L; platelets 256; not anticoagulated. No previous stroke, bleeding or recent surgery.

Blood pressure log
- 16:44  198/112 mmHg
- 16:55  labetalol 10 mg IV given (dose 1)
- 17:05  191/108 mmHg
- 17:07  labetalol 10 mg IV given (dose 2)
- 17:17  184/104 mmHg
- 17:20  Nurse in charge suggests a third dose "to get him properly under"; registrar declines.

Consultant (by phone, 17:21): "Decide now on the protocol - I don't want a third bolus of antihypertensive before we treat."
""",
0, 2, S_YCARD,
twin=T([("17:17  184/104 mmHg", "17:17  187/104 mmHg")], 1)),

# S4: warfarin INR 1.6 (<= 1.7 ok); glucose 2.4 corrected to 6.1 with persisting deficit (reassessment value used);
# platelets 118; BP ok; onset 09:05 -> bolus 11:10. TIA 5 months ago (not stroke) -> none of these.
# Twin: INR 1.8 -> anticoagulant.
C("Which contraindication in the St Aldric's protocol, if any, prevents thrombolysis for Mrs Oyelaran-Webb?",
"""St Aldric's Hospital - Thrombolysis decision record
Patient: Mrs Mireille Oyelaran-Webb, 81 | Onset witnessed 09:05 | Planned bolus 11:10

On arrival (09:40): aphasia and right hemiparesis. Fingerstick glucose 2.4 mmol/L (takes gliclazide). Given 75 mL of 20% glucose IV at 09:46. Repeat glucose 10:02: 6.1 mmol/L. Reassessed at 10:10: aphasia and right hemiparesis unchanged, NIHSS 12.

CT 10:20: no haemorrhage; CT angiogram: left M1 occlusion.

Anticoagulation: warfarin for atrial fibrillation, last dose yesterday evening; INR 1.6 (lab, 10:05).
Platelets 118 x10^9/L. BP 176/98 mmHg, no treatment needed.

History: transient ischaemic attack five months ago (full recovery within 30 minutes, MRI negative); no intracranial haemorrhage ever; cholecystectomy 2019; no bleeding episodes this year.

Registrar comment: "Hypoglycaemic on arrival and on warfarin - not sure she's a candidate."
""",
S_OPTS, NONE, 3, S_CARD,
twin=T([("INR 1.6 (lab, 10:05)", "INR 1.8 (lab, 10:05)")], "anticoagulant")),

# S5: total knee replacement 12 d ago -> recent surgery. Prophylactic enoxaparin (not treatment dose) ok;
# duodenal ulcer bleed 25 d ago (> 21 d) ok.
C("Using the St Aldric's thrombolysis protocol, which contraindication applies to this patient, if any?",
"""St Aldric's Hospital - Inpatient stroke call (orthopaedic ward)
Patient: Mrs Henrietta Kaplan-Mensah, 70 | Called 08:15 | Last known well 07:40 (nurse observation round)

Admission: elective right total knee replacement 12 days ago; slow mobilisation, awaiting rehabilitation bed.
Admission course: upper GI bleed from a duodenal ulcer 25 days ago (before the operation, which was delayed until she was stable); endoscopic clip, no bleeding since, haemoglobin stable.

Now: sudden left arm and leg weakness and neglect, NIHSS 10. CT: no haemorrhage.

Medication: enoxaparin 40 mg subcutaneously once daily (standard post-operative thromboprophylaxis), last dose 22:00 last night; omeprazole; paracetamol.
Bloods: glucose 6.9 mmol/L; platelets 212; INR 1.1.
BP 168/88 mmHg.
No previous stroke or intracranial haemorrhage.

Ward doctor: "She's on heparin, so I assume that rules it out?"
""",
S_OPTS, "recent surgery", 2, S_CARD),
]
