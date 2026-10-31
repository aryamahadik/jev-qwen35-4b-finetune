"""Insurance pre-authorisation and coverage items (all plans invented)."""
from common import (Y, C, T, card, crit, labels, NONE, MRI, MRI_REPEAT, MRI_DECISION, MRI_NONE, BARI, BARI_NONE,
                    PCSK, PCSK_NONE, ASTHMA, ASTHMA_NONE, TKA, TKA_NONE, CGM, AAT, AAT_NONE, IVF, IVF_NONE,
                    SNF, SNF_NONE, TX, TX_NONE)

M_OPTS, M_CARD = crit(MRI, MRI_NONE)
M_YCARD = card(MRI + [MRI_REPEAT, MRI_DECISION])

CPAP = [
    ("adherence requirement", "device download showing use for at least 4 hours per night on at least 70% of nights "
     "(21 or more of 30) during some period of 30 consecutive nights within the first 90 nights after set-up."),
    ("re-evaluation requirement", "an in-person or video visit with the treating practitioner no earlier than day 31 "
     "and no later than day 91 after set-up (the set-up date is day 1), documenting that sleep-apnoea symptoms have "
     "improved."),
    ("coverage rule", "CPAP coverage continues after the 12-week trial only if both requirements are met."),
]
CPAP_OUT = [
    ("only adherence unmet", "the adherence requirement is not met and the re-evaluation requirement is met."),
    ("only re-evaluation unmet", "the re-evaluation requirement is not met and the adherence requirement is met."),
    ("both unmet", "neither requirement is met."),
    ("both met", "both requirements are met, so coverage continues."),
]

OX = [
    ("group I", "any of: resting SpO2 of 88% or less, or PaO2 of 55 mmHg or less, on room air while awake; SpO2 of 88% "
     "or less on room air during exercise, with improvement of the hypoxaemia on oxygen documented during the same "
     "test; or SpO2 of 88% or less on room air for a cumulative total of at least 5 minutes during sleep."),
    ("group II", "resting SpO2 of exactly 89%, or PaO2 of 56-59 mmHg, on room air while awake, together with at least "
     "one of: dependent oedema suggesting congestive heart failure; pulmonary hypertension or cor pulmonale "
     "documented by echocardiogram or P-pulmonale on ECG; haematocrit above 56%."),
    ("not eligible", "no valid qualifying test meets group I or group II."),
]
OX_VALID = ("valid qualifying test", "the qualifying test was done within 30 days before the order date, on room air "
            "unless the criterion says otherwise, by a clinician or laboratory that is not the oxygen supplier or "
            "affiliated with it, while the patient was in a chronic stable state: as an outpatient, or as an "
            "inpatient within the 2 days before discharge.")
OX_RULE = ("Norvale Home Oxygen Program, rule 4.2 (qualifying tests): a test counts only if it was done within 30 days "
           "before the order date, on room air unless the criterion says otherwise, by a clinician or laboratory that "
           "is not the oxygen supplier or affiliated with it, and while the patient was in a chronic stable state - as "
           "an outpatient, or as an inpatient within the 2 days before discharge.")

B_OPTS, B_CARD = crit(BARI, BARI_NONE)
B_YCARD = card(BARI + [("approval rule", "the procedure is approved only if all six requirements are met.")])
P_OPTS, P_CARD = crit(PCSK, PCSK_NONE)
P_YCARD = card(PCSK + [("approval rule", "initial approval requires all three requirements to be met.")])
A_OPTS, A_CARD = crit(ASTHMA, ASTHMA_NONE)
A_YCARD = card(ASTHMA + [("approval rule", "the biologic is approved only if all five requirements are met.")])
K_OPTS, K_CARD = crit(TKA, TKA_NONE)
AD_OPTS, AD_CARD = crit(AAT, AAT_NONE)
AD_YCARD = card(AAT + [("approval rule", "the first infusion is authorised only if all five conditions are met.")])
I_OPTS, I_CARD = crit(IVF, IVF_NONE)
I_YCARD = card(IVF + [("coverage rule", "a stimulation cycle is covered only if all four conditions are met.")])
S_OPTS, S_CARD = crit(SNF, SNF_NONE)
S_YCARD = card(SNF + [("coverage rule", "the SNF stay is covered only if all three requirements are met.")])
X_OPTS, X_CARD = crit(TX, TX_NONE)

ITEMS = [
# ------------------------------------------------------------------ RAD-114 lumbar MRI
# M1: naproxen from 5 Jan (regular >= 3 wk) + chiropractic 5 visits = two modalities; PT only 3 sessions.
# 5 Jan -> 20 Feb = 46 d >= 6 wk -> criterion B -> approve. Twin: 3 chiropractic visits -> only one modality -> deny.
Y("Should Brightwater approve this lumbar spine MRI request?",
"""Brightwater Health Plan - Imaging prior authorisation request
Request date: 20 February 2025 | Study: MRI lumbar spine without contrast
Member: Rosalind Tembo-Hartley, 46 | Ordering clinician: Dr Kwame Aldous, family medicine

Clinical summary: low back pain radiating down the left leg to the lateral foot since late December 2024, after lifting a wardrobe. Pain 6/10, worse sitting.

Conservative care (documented in the clinic notes):
- Naproxen 500 mg twice daily, started 5 January 2025, taken regularly; confirmed at reviews on 20 January and 10 February.
- Physical therapy: 3 attended sessions (13, 20 and 27 January); the fourth was cancelled by the clinic and not rebooked.
- Chiropractic: 5 visits (12 January - 10 February 2025).

Examination 10 February: reduced sensation in the left S1 dermatome; power 5/5 throughout; reflexes symmetrical; straight-leg raise positive on the left at 40 degrees. No urinary symptoms, no saddle anaesthesia, afebrile.

History: no previous cancer; no immunosuppression; no injection drug use; no trauma. No previous spinal imaging.

Clinician comment: "Only managed three PT sessions, but she has been doing everything else we asked."
""",
1, 2, M_YCARD,
twin=T([("Chiropractic: 5 visits", "Chiropractic: 3 visits")], 0)),

# M2: BCC is non-melanoma skin cancer -> not a red flag; pain 2 weeks -> no criterion B; no surgeon -> deny.
Y("Under RAD-114, should this MRI request be approved?",
"""Brightwater Health Plan - Utilisation review worksheet
Request received: 11 March 2025 | MRI lumbar spine without contrast
Member: Aurelio Fontaine-Mbeki, 58

Referral note (urgent care physician, 10 March 2025):
"58-year-old man with new low back pain for 2 weeks after gardening. No leg pain. No weakness, numbness, bladder or bowel change. Afebrile. He is very worried because he has a history of cancer - basal cell carcinoma of the cheek, excised in 2021 with clear margins, no recurrence on dermatology follow-up. His father died of prostate cancer and he wants to be sure this isn't cancer. Started ibuprofen 400 mg three times daily yesterday. Please authorise MRI to rule out malignancy."

Past history: hypertension; type 2 diabetes on metformin. No steroid use; no immunosuppression; no recent procedure; no trauma.
Previous imaging: none.
No surgical referral.
""",
0, 2, M_YCARD),

# M3: fever 38.3 + immunosuppressed (methotrexate + prednisone for RA) with back pain -> criterion A.
C("Which RAD-114 criterion, if any, supports approval of this lumbar MRI?",
"""Brightwater Health Plan - Prior authorisation phone intake (transcribed)
Date: 2 June 2025 | Caller: nurse from Dr Imogen Salter-Oduya's rheumatology practice

"I'm calling about Mrs Delphine Achebe-Ward, 67. She has rheumatoid arthritis on methotrexate 20 mg weekly and prednisone 10 mg daily for the last year. She's had worsening mid-to-low back pain for 9 days, now waking her at night. Temperature at the clinic today was 38.3 C. No leg weakness, no numbness, bladder and bowel normal. No falls or injury. No history of cancer. She had two physical therapy sessions last week and has been taking paracetamol for about a week. Nobody has done any spinal procedure on her. Dr Salter-Oduya wants a lumbar MRI with and without contrast as soon as possible. She's not been seen by a surgeon."

Intake reviewer notes: previous lumbar MRI: none on file. Request is for MRI lumbar spine.
""",
M_OPTS, "criterion A red flag", 2, M_CARD),

# M4: repeat MRI 10 months after the last one, but new foot drop 3/5 (was 5/5) -> criterion A + new deficit -> covered.
Y("Is this repeat lumbar MRI covered under Brightwater policy RAD-114?",
"""Brightwater Health Plan - Imaging request with clinical notes
Request date: 14 July 2025 | MRI lumbar spine without contrast
Member: Casimir Wollaston-Nnadi, 52

Previous lumbar MRI: 9 September 2024 (L4-5 disc protrusion contacting the right L5 root). Managed conservatively with physical therapy and home exercises; improved.

Clinic note, 11 July 2025 (Dr Hester Obuya, sports medicine):
"Recurrence of right leg pain for 3 weeks. New since last week: tripping over his right foot. Examination: right ankle dorsiflexion 3/5 and great toe extension 3/5 (both 5/5 at his March review); reduced sensation over the dorsum of the right foot; reflexes symmetrical. No saddle anaesthesia, bladder normal, afebrile. No cancer history."

Utilisation reviewer comment (first pass): "Repeat MRI within 12 months of the last one - usually not covered. Conservative care only 3 weeks this time."
""",
1, 2, M_YCARD),

# M5: spine surgeon documents planned epidural steroid injection and needs imaging -> criterion C.
C("Which RAD-114 criterion, if any, does this request meet?",
"""Brightwater Health Plan - Imaging prior authorisation
Request date: 3 April 2025 | MRI lumbar spine without contrast
Member: Priyanka Holloway-Adeyemi, 39
Ordering clinician: Dr Magnus Ferreira-Lowe, orthopaedic spine surgery

Clinic letter, 1 April 2025:
"Mrs Holloway-Adeyemi has 7 weeks of left L5 radicular pain. She has had 4 weeks of ibuprofen and 2 physical therapy sessions so far, with little benefit. Neurologically intact: power 5/5, sensation mildly reduced on the dorsum of the left foot, reflexes normal. No red-flag features. She is struggling to work and we have agreed to proceed with a left L5 transforaminal epidural steroid injection, which I am booking for later this month. I need MRI to confirm the level and plan the injection approach."

No previous spinal imaging. No history of cancer, fever or trauma.
""",
M_OPTS, "criterion C surgical planning", 1, M_CARD),

# M6: PT from 1 Feb + ibuprofen from 3 Feb; request 10 Mar -> 37 d < 42 d -> B not met; stable 4/5 toe weakness is
# not a red flag; family physician -> no C -> none of these.
C("Applying RAD-114, which criterion does this lumbar MRI request satisfy, if any?",
"""Brightwater Health Plan - Utilisation review worksheet
Request date: 10 March 2025 | MRI lumbar spine without contrast
Member: Ottilie Ramaswamy-Crane, 44 | Ordering clinician: Dr Beaumont Kiplagat, family medicine

History: low back pain with right leg pain for about 3 months (since early December 2024), managed initially with rest and heat at home.

Clinician-directed conservative care:
- Physical therapy from 1 February 2025: 6 sessions attended, with a written home exercise programme documented by the physiotherapist.
- Ibuprofen 400 mg three times daily from 3 February 2025, taken regularly.

Examinations: 3 February - right great toe extension 4/5; 3 March - right great toe extension 4/5, unchanged. Sensation intact. No bladder or bowel symptoms. Afebrile.
No cancer history, no steroid use, no trauma; no previous lumbar imaging; no surgical referral.

Clinician comment: "Symptoms for three months despite conservative care - meets the 6-week rule comfortably."
""",
M_OPTS, NONE, 3, M_CARD),

# ------------------------------------------------------------------ CPAP continued coverage
# CP1: set-up 3 Jan (day 1); adherence window 22/30 nights; visit 7 Apr = day 95 > 91 -> not covered.
# Twin: visit 31 Mar = day 88 -> covered.
Y("Does the member qualify for continued CPAP coverage after the trial period?",
"""Brightwater DME review - CPAP continued coverage
Member: Ignatius Ferreira-Bloom, 55 | Diagnosis: obstructive sleep apnoea (AHI 31)
CPAP set-up date: 3 January 2025

Device download (compliance report, nights 1-90):
- Nights 1-19: variable use, frequent mask leak (mask changed on night 18).
- Nights 20-49: 22 of 30 nights with use of 4 hours or more (73%); average use on nights used 5.6 hours.
- Nights 50-90: 26 of 41 nights with use of 4 hours or more.

Follow-up: in-person visit with his sleep physician, Dr Anneliese Mokoena, on 7 April 2025. Note: "Much less daytime sleepiness; Epworth score down from 16 to 7; wife reports snoring has stopped. Continue CPAP."

Supplier comment: "Excellent response, fully compliant, please continue rental."
""",
0, 3, card(CPAP),
twin=T([("on 7 April 2025", "on 31 March 2025")], 1)),

# CP2: best window 21/30 = 70% (met); visit on day 28 (< 31) -> only re-evaluation unmet.
C("Which of the continued-coverage requirements are not met?",
"""Brightwater DME policy excerpt (CPAP): after the 12-week trial, coverage continues only if (a) a device download shows use of at least 4 hours per night on at least 70% of nights (21 or more of 30) during some period of 30 consecutive nights within the first 90 nights, and (b) the member has an in-person or video visit with the treating practitioner no earlier than day 31 and no later than day 91 after set-up (set-up date = day 1) documenting improvement in symptoms.

Case: member Solange Adewale-Firth, 47. CPAP set-up 10 March 2025 (day 1).
Download: best 30-night window is nights 12-41, with 21 nights of use of 4 hours or more. Overall nights 1-90: 58 nights of use of 4 hours or more.
Follow-up: video visit with her sleep nurse practitioner on day 28 (6 April 2025): "sleeping better, headaches resolved". No other visit before day 91; the next review is booked for month 6.

Supplier note: "Compliance exactly on the threshold - should pass."
""",
labels(CPAP_OUT), "only re-evaluation unmet", 2, card(CPAP_OUT)),

# CP3: best window 20/30 = 66.7% < 70% -> adherence fails despite long average use -> not covered.
Y("Does this member meet the requirements for continued CPAP coverage?",
"""Brightwater DME review - CPAP continued coverage
Member: Bartholomew Achterberg-Lyle, 61 | CPAP set-up: 2 June 2025

Compliance report, first 90 nights:
- Best 30-consecutive-night window (nights 41-70): 20 nights with 4 hours or more of use.
- Nights with any use: 81 of 90.
- Average use on nights used: 5.1 hours. Median 4.6 hours.
- Residual AHI 2.1; leak within range.

Follow-up: in-person visit with his pulmonologist on day 60 (31 July 2025): "Feels transformed, no longer falls asleep driving, blood pressure improved. Continue CPAP."

Member's letter attached: "I use it almost every night. Some nights I take it off at 3 am because of my nose, but I'm averaging over five hours."
""",
0, 2, card(CPAP)),

# ------------------------------------------------------------------ Norvale home oxygen
# OX1: resting SpO2 86% measured by the oxygen supplier -> invalid test -> not eligible.
Y("Does Mr Hawthorne-Asante qualify for home oxygen under the Norvale program on the testing submitted?",
"""Norvale Home Oxygen Program - order review
Order date: 14 February 2025 | Patient: Mr Everard Hawthorne-Asante, 76 | Diagnosis: COPD (FEV1 38% predicted)

Qualifying test submitted:
- Resting pulse oximetry on room air, seated, at home, 10 February 2025: SpO2 86% (sustained over 5 minutes).
- Performed by: respiratory therapist employed by Airline Home Medical Ltd, the company that will supply and maintain the oxygen concentrator.

Clinic notes (GP, 12 February 2025): "Breathless walking to the kitchen; ankles not swollen; stable, no recent exacerbation. Saturations low on the supplier's test - I have signed the oxygen order."

No other oximetry or blood gas in the last 30 days. Last hospital admission: 2023.
""",
0, 2, card(OX[:2] + [OX_VALID])),

# OX2: SpO2 89% at rest on room air + haematocrit 58% (> 56%) -> group II.
C("Under the Norvale Home Oxygen Program, which coverage group applies?",
OX_RULE + """

Order date: 3 June 2025. Patient: Ms Imelda Farquhar-Osei, 69, COPD and obstructive sleep apnoea on CPAP.
Qualifying test: Pellbridge Hospital pulmonary function laboratory (outpatient), 28 May 2025. Resting SpO2 on room air 89%, stable over 10 minutes. Arterial blood gas not done. 6-minute walk: SpO2 nadir 90% on room air.
Other results: full blood count 20 May 2025, haematocrit 58%. Echocardiogram 2024: normal right heart size, estimated PA pressure normal. Examination: no ankle oedema.
Clinician note: "Saturation just above the usual 88% cut-off."
""",
labels(OX), "group II", 2, card(OX)),

# OX3: inpatient test on 11 March, discharge 12 March (within 2 days before discharge) by hospital lab -> valid.
Y("Is the inpatient oximetry a valid qualifying test for the Norvale program?",
"""Norvale Home Oxygen Program - order review
Patient: Mrs Aurora Lindqvist-Ebo, 72 | Order date: 12 March 2025 (signed at discharge)

Admission: 4-12 March 2025, Pellbridge Hospital, infective exacerbation of COPD. Treated with nebulisers, prednisolone and doxycycline. Oxygen weaned off on 9 March.

Qualifying test: resting oximetry on room air, performed by the hospital respiratory physiology team at 10:00 on 11 March 2025, after 48 hours off supplemental oxygen: SpO2 87%, sustained over 10 minutes. Discharged home on 12 March at 15:00.

Oxygen supplier: Northgate Oxygen Services (not connected with the hospital).

Reviewer comment (first pass): "Test done during an acute admission - the patient was not stable, so reject and ask for an outpatient test."
""",
1, 2, card(OX[:2] + [OX_VALID])),

# OX4: exercise desaturation 87% but no oxygen titration documented; nocturnal 4 min cumulative <= 88%;
# resting 92% -> not eligible. Twin: 6 minutes nocturnal -> group I.
C("Which Norvale coverage group, if any, do the submitted tests support?",
OX_RULE + """

Order date: 21 August 2025. Patient: Mr Leander Okonkwo-Hale, 64, pulmonary fibrosis.
Tests (all outpatient, all by Harlow Respiratory Physiology, which is independent of the supplier):
- 12 August 2025, resting SpO2 on room air: 92%.
- 12 August 2025, 6-minute walk on room air: SpO2 fell to 87% at 4 minutes. The test was stopped at 5 minutes because of breathlessness; the walk was not repeated on oxygen.
- 15-16 August 2025, overnight oximetry on room air at home: cumulative time with SpO2 at or below 88% = 4 minutes; lowest 86%.
No arterial blood gas. No oedema; echo normal; haematocrit 44%.
""",
labels(OX), "not eligible", 3, card(OX),
twin=T([("= 4 minutes; lowest 86%", "= 6 minutes; lowest 86%")], "group I")),

# OX5: resting SpO2 88% on room air -> group I (<= 88), even though oedema would also fit group II wording.
C("Which coverage group applies under the Norvale Home Oxygen Program?",
OX_RULE + """

Order date: 7 October 2025. Patient: Mrs Philomena Grayson-Adu, 81, heart failure and COPD.
Qualifying test: outpatient clinic, Dr Ravi Castellane's practice (no link to any supplier), 2 October 2025. Resting SpO2 on room air, seated, after 10 minutes: 88% throughout.
Examination the same day: bilateral pitting ankle oedema to mid-shin. Echo 2025: moderate LV impairment, mild pulmonary hypertension.
Haematocrit 41%.
Clinician note: "Saturation 88%, ankles swollen - applying under the second group because of the heart failure."
""",
labels(OX), "group I", 2, card(OX)),

# ------------------------------------------------------------------ BAR-02 bariatric
# BA1: programme visits 10 Jan, 12 Feb, 14 Mar, 28 May (75-day gap), 25 Jun, 30 Jul -> R3 fails.
# Twin: 8 May (gaps 55 and 48) -> none of these.
C("Checking BAR-02 requirements in order, which is the first one this request fails?",
"""Brightwater Health Plan - Bariatric surgery prior authorisation
Request date: 20 August 2025 | Procedure: laparoscopic sleeve gastrectomy
Member: Genevieve Oduya-Brandt, 44

BMI: 43.1 kg/m2 (weighed 4 August 2025).
Comorbidities: hypertension (amlodipine), knee osteoarthritis.

Medically supervised weight-management programme (Brightwater bariatric clinic, physician-led) - visit dates:
10 January 2025; 12 February 2025; 14 March 2025; 28 May 2025; 25 June 2025; 30 July 2025.
Programme physician note: "Six visits over six months completed; weight down 4 kg."

Psychological evaluation: 2 June 2025 - "cleared for bariatric surgery".
Registered dietitian consultation: 14 March 2025.
Nicotine: never smoked or vaped; serum cotinine negative on 5 August 2025.
""",
B_OPTS, "R3 supervised programme", 3, B_CARD,
twin=T([("14 March 2025; 28 May 2025;", "14 March 2025; 8 May 2025;")], NONE)),

# BA2: BMI 37.2 needs a comorbidity; hypertension on one drug, AHI 9, prediabetes, steatosis without fibrosis -> none.
Y("Does this bariatric surgery request meet Brightwater's BAR-02 policy?",
"""From: Surgical coordinator, Harwick Bariatric Centre
To: Brightwater prior authorisation team
Date: 9 September 2025
Subject: Sleeve gastrectomy request - member Florentyna Adebayo-Keane, 38

Please find the request summary:

- BMI 37.2 kg/m2 (clinic weight 1 September 2025).
- Hypertension: lisinopril 20 mg daily, BP controlled (128/80).
- Sleep study (March 2025): obstructive sleep apnoea, AHI 9 events/hour; CPAP not recommended.
- HbA1c 6.1% (prediabetes); no diabetes medication.
- Liver ultrasound: steatosis; FibroScan stiffness 5.2 kPa, reported as "no significant fibrosis".
- Supervised programme: 7 physician visits from October 2024 to August 2025, never more than 50 days apart.
- Psychological evaluation July 2025: cleared. Dietitian review: June 2025.
- Never smoked; cotinine negative 25 August 2025.

She has three obesity-related conditions and has done everything asked of her. We would be grateful for approval.
""",
0, 2, B_YCARD),

# BA3: current BMI 38.5 (no comorbidity) but highest BMI 41.3 within 24 months, lost during programme -> R2 met.
Y("Should Brightwater approve this bariatric surgery request?",
"""Brightwater Health Plan - Bariatric review note
Request date: 1 October 2025 | Procedure: Roux-en-Y gastric bypass
Member: Horatio Mbeki-Lindholm, 35

Weight history:
- 12 August 2024 (start of supervised programme): 131.5 kg, height 1.785 m, BMI 41.3.
- 10 September 2025 (programme discharge): 122.6 kg, BMI 38.5.

No diabetes, sleep apnoea, hypertension or liver disease documented.

Supervised programme: physician-led, 9 visits between 12 August 2024 and 10 September 2025, maximum gap 52 days; all visits from October 2024 onwards fall in the 12 months before the request, and there are at least 6 of them across more than 6 months.
Psychological evaluation (15 July 2025): cleared. Dietitian: 3 consultations in 2025. Never smoked; cotinine negative 18 September 2025.

First-pass reviewer comment: "Current BMI below 40 and no comorbidities, so R2 not met?"
""",
1, 3, B_YCARD),

# BA4: nicotine gum daily (quit cigarettes 5 months ago) -> cotinine positive -> R6.
C("Which BAR-02 requirement, taken in order, is the first one not met by this request?",
"""Brightwater Health Plan - Bariatric prior authorisation checklist
Request date: 14 July 2025 | Member: Wilhelmina Castellanos-Ude, 51

Age: 51.
BMI: 45.6 kg/m2, measured 30 June 2025.
Programme: WeightWise (commercial programme) - 8 weekly-to-monthly visits from August 2024 to June 2025, each visit record co-signed by Harriet Olumide, nurse practitioner; longest gap 41 days.
Psychology: evaluation 20 May 2025, cleared for surgery.
Dietitian: consultation 3 June 2025.
Nicotine: stopped smoking cigarettes in February 2025 "with the help of nicotine gum, which I still chew most days, about 6 pieces a day - I haven't had a single cigarette since". Serum cotinine 1 July 2025: positive (level consistent with nicotine use).

Coordinator comment: "She quit smoking five months ago, well past the six weeks. WeightWise is a commercial programme - check."
""",
B_OPTS, "R6 nicotine", 2, B_CARD),

# BA5: psychological evaluation 30 Sep 2024, request 3 Nov 2025 -> 13 months -> R4 fails.
C("Which requirement of Brightwater policy BAR-02 does this request fail first, in the order listed?",
"""Harwick Bariatric Centre - authorisation cover sheet
Date sent: 3 November 2025 | Member: Tobias Adeyemi-Strand, 42

- BMI 47.9 kg/m2 on 20 October 2025; type 2 diabetes on metformin and dapagliflozin.
- Supervised weight-management programme: 7 physician visits, 12 November 2024 to 14 October 2025; no gap over 58 days.
- Psychological evaluation by Dr Maren Oyelaran, clinical psychologist, on 30 September 2024: "no contraindication; cleared for bariatric surgery".
- Dietitian consultations: 5 February 2025 and 2 September 2025.
- Former smoker, stopped 2019. Serum cotinine negative 21 October 2025.

Centre comment: "All pre-operative work-up completed within the last year."
""",
B_OPTS, "R4 psychological clearance", 2, B_CARD),

# ------------------------------------------------------------------ PH-PCSK9
# PC1: LDL 1.9 mmol/L x 38.67 = 73.5 mg/dL >= 70 with ASCVD, on atorvastatin 80 + ezetimibe 12 wk -> approve.
# Twin: 1.7 mmol/L = 65.7 mg/dL -> deny.
Y("Does this PCSK9 inhibitor request meet Brightwater's PH-PCSK9 criteria for initial approval?",
"""Brightwater Pharmacy - PCSK9 inhibitor prior authorisation
Request date: 2 September 2025 | Drug requested: evolocumab 140 mg every 2 weeks
Member: Leopold Okafor-Warrington, 63

Diagnosis: myocardial infarction (STEMI) March 2023, treated with PCI to the LAD.

Lipid-lowering history:
- Atorvastatin 80 mg daily since March 2023.
- Ezetimibe 10 mg daily added 9 June 2025; pharmacy fills continuous since.

Most recent lipid panel (18 August 2025, on atorvastatin 80 mg + ezetimibe 10 mg):
total cholesterol 3.6 mmol/L; HDL-C 1.1 mmol/L; triglycerides 1.3 mmol/L; LDL-C 1.9 mmol/L (the laboratory reports SI units).

Prescriber note: "LDL still above target despite maximal oral therapy."
Plan pharmacist, first pass: "LDL 1.9 - well under 70, likely deny?"
""",
1, 3, P_YCARD,
twin=T([("LDL-C 1.9 mmol/L", "LDL-C 1.7 mmol/L")], 0)),

# PC2: myalgia on atorvastatin 40 and rosuvastatin 20 -> neither at lowest starting dose -> not statin-intolerant;
# not on high-intensity statin + ezetimibe -> requirement 3 fails.
C("Which PH-PCSK9 requirement, if any, does this request fail?",
"""Brightwater Pharmacy - PCSK9 prior authorisation review
Request date: 22 July 2025 | Member: Ophelia Brandvold-Nwosu, 58

Diagnosis: coronary artery bypass grafting (CABG x3) in 2022.

Statin history (prescriber attestation):
- Atorvastatin 40 mg daily, 2022: muscle aches in both thighs after 6 weeks; stopped. CK normal.
- Rosuvastatin 20 mg daily, 2023: similar muscle aches after 4 weeks; stopped. CK normal.
- No further statin tried; the member declines further statins.

Current therapy: ezetimibe 10 mg daily since January 2025 (continuous fills).

Lipids (10 July 2025, on ezetimibe alone): LDL-C 128 mg/dL.

Prescriber note: "Statin-intolerant to two statins - please approve alirocumab."
""",
P_OPTS, "requirement 3 prior therapy", 3, P_CARD),

# PC3: HeFH not established (DLCN 7, no genetic test), no ASCVD -> requirement 1 fails -> not approved.
Y("Will the plan approve the PCSK9 inhibitor for this member under PH-PCSK9?",
"""Brightwater Pharmacy - PCSK9 prior authorisation
Request date: 5 May 2025 | Drug requested: alirocumab 150 mg every 2 weeks
Member: Cordelia Stavros-Obi, 41

Lipid clinic letter (April 2025): "Probable heterozygous familial hypercholesterolaemia. Dutch Lipid Clinic Network score 7 (LDL-C, family history of premature coronary disease in her father at 52). No tendon xanthomata. Genetic testing has been offered but the member has not yet had it. She has no personal history of cardiovascular disease."

Therapy: rosuvastatin 40 mg + ezetimibe 10 mg daily since November 2024 (continuous fills).
LDL-C (22 April 2025, on that therapy): 190 mg/dL.

Prescriber note: "Familial hypercholesterolaemia with LDL nearly twice the 100 mg/dL threshold on maximal therapy."
""",
0, 2, P_YCARD),

# PC4: LDL drawn 27 May 2025, request 15 Sep 2025 -> 111 d > 90 -> requirement 2 fails.
C("Checking the PH-PCSK9 requirements, which one is not met, if any?",
"""Brightwater Pharmacy - PCSK9 request summary
Request date: 15 September 2025 | Member: Rufus Ekwueme-Hale, 70

Diagnosis: ischaemic stroke (2021) and symptomatic peripheral arterial disease with femoral stenting (2023).

Therapy: rosuvastatin 40 mg daily since 2021; ezetimibe 10 mg daily since January 2025 (pharmacy fills continuous).

Lipids:
- 27 May 2025 (on rosuvastatin 40 mg + ezetimibe): LDL-C 96 mg/dL.
- 2 September 2025: lipid panel ordered but not drawn - member was travelling.

Prescriber note: "LDL-C remains well above 70 despite maximal statin and ezetimibe; request expedited review."
""",
P_OPTS, "requirement 2 LDL-C", 2, P_CARD),

# ------------------------------------------------------------------ anti-IL-5 asthma biologic
# AS1: eos 280 (3 wk ago) ok; exacerbations: one 5-day course, one 2-day course (ED, not admitted) -> requirement 3 fails.
Y("Does this request meet all of Brightwater's criteria for the anti-IL-5 biologic?",
"""Brightwater Pharmacy - specialty drug prior authorisation
Request date: 1 August 2025 | Drug: mepolizumab 100 mg every 4 weeks
Member: Tamsin Okoro-Lindqvist, 34 | Prescriber: Dr Aurelius Pike, pulmonology

Diagnosis: severe asthma since 2019.

Blood eosinophils: 0.28 x10^9/L on 10 July 2025.

Exacerbations in the past 12 months:
- February 2025: prednisolone 40 mg daily for 5 days from GP.
- June 2025: attended emergency department with wheeze; given prednisolone 40 mg in the department and a second dose the next morning (2 days in total); discharged from the ED after 6 hours, not admitted.

Controller therapy: fluticasone furoate/vilanterol 200/25 once daily (high-dose ICS + LABA) since 2023, plus tiotropium since January 2025; pharmacy fills 100% over the last 6 months.
No other biologic.

Prescriber note: "Two exacerbations requiring steroids and an ED visit in the past year despite triple therapy."
""",
0, 2, A_YCARD),

# AS2: adding mepolizumab while continuing dupilumab for atopic dermatitis -> requirement 5 fails.
# Eos 120 (2 wk) < 150 but 340 eight months ago >= 300 -> requirement 2 met; hospital admission -> requirement 3 met.
C("Which requirement of the Brightwater anti-IL-5 policy, if any, does this request fail?",
"""Brightwater Pharmacy - specialty prior authorisation
Request date: 18 November 2025 | Drug: mepolizumab 100 mg every 4 weeks
Member: Isadora Nkemelu-Brandt, 29 | Prescriber: Dr Fenella Oduya, allergy & immunology

Diagnosis: severe eosinophilic asthma (diagnosed by the prescriber, 2021).
Eosinophils: 120 cells/uL on 4 November 2025; 340 cells/uL on 12 March 2025.
Exacerbations: admitted to hospital for 3 nights in April 2025 with acute asthma.
Controller therapy: budesonide/formoterol 400/12 two puffs twice daily (high-dose) plus montelukast, adherent for over a year.

Other treatment: dupilumab 300 mg every 2 weeks, prescribed by dermatology for severe atopic dermatitis since 2024; dermatology wishes to continue it because her eczema has cleared.

Prescriber note: "Her asthma remains uncontrolled; dupilumab is for her skin, not her asthma, so it should not affect this request. Eosinophils are low now only because of recent oral steroids."
""",
A_OPTS, "requirement 5 no other biologic", 2, A_CARD),

# AS3: eos 140 (3 wk ago) < 150; 290 ten months ago < 300 -> requirement 2 fails.
C("Which anti-IL-5 policy requirement does this request not meet, if any?",
"""Brightwater Pharmacy - PA review note
Request date: 6 October 2025 | Drug: benralizumab | Member: Cassian Oyelowo-Pratt, 52
Prescriber: Dr Linnea Achterberg, pulmonology

Diagnosis: severe asthma, confirmed by the prescriber.
Blood eosinophils: 140 cells/uL on 15 September 2025; 290 cells/uL on 2 December 2024; 410 cells/uL on 20 June 2024.
Exacerbations (past 12 months): three courses of prednisolone, 5, 7 and 5 days.
Controller: mometasone/indacaterol/glycopyrronium high-dose inhaler daily for 14 months; adherence confirmed by pharmacy fills.
Other biologics: none (omalizumab was stopped in 2023).

Prescriber note: "Clearly eosinophilic - counts over 300 on record."
""",
A_OPTS, "requirement 2 eosinophils", 2, A_CARD),

# ------------------------------------------------------------------ total knee arthroplasty
# TK1: HbA1c 8.1% within 90 d of surgery -> requirement 4 fails. BMI 42 allowed (plan + anaesthesia review).
C("Taking the Brightwater knee arthroplasty requirements in order, which is the first one this request does not meet?",
"""Brightwater Health Plan - Elective surgery prior authorisation
Procedure: right total knee arthroplasty | Planned surgery date: 12 January 2026
Request date: 1 December 2025 | Member: Magdalena Ferreira-Osei, 67

Imaging: standing AP, lateral and skyline right knee X-rays, 8 October 2025: Kellgren-Lawrence grade 4, bone-on-bone medial compartment.
Conservative care: physical therapy February-May 2025 (14 sessions); naproxen since 2024; corticosteroid injection July 2025; walking stick.
BMI: 42.0. Surgeon letter documents a weight-optimisation plan (dietitian-led, target 5% loss) and a completed anaesthesia pre-assessment and risk review on 20 November 2025.
Diabetes: type 2, on insulin. HbA1c 8.1% on 25 November 2025.
Nicotine: ex-smoker, stopped 2016.

Surgeon note: "BMI above 40 - optimisation plan and anaesthesia review attached as required."
""",
K_OPTS, "requirement 4 glycaemic control", 2, K_CARD),

# TK2: X-ray was supine (non-weight-bearing) -> requirement 1 fails although it shows KL grade 3.
C("Which knee arthroplasty requirement, checked in the order listed, is the first one not met?",
"""Brightwater Health Plan - Elective surgery prior authorisation
Procedure: left total knee arthroplasty | Request date: 14 April 2025
Member: Desmond Kaplan-Achebe, 71

Imaging: left knee X-ray (AP supine and lateral views, taken in the emergency department after a minor fall), 2 February 2025: "moderate tricompartmental osteoarthritis, Kellgren-Lawrence grade 3; no fracture". No other imaging.
Conservative care: supervised exercise programme September-December 2024; paracetamol and topical diclofenac since 2023; hinged knee brace since October 2024.
BMI: 31.6. HbA1c 7.2% on 1 April 2025 (planned surgery 20 May 2025). Never smoked.

Surgeon note: "Grade 3 osteoarthritis on X-ray this year; failed six months of conservative care."
""",
K_OPTS, "requirement 1 imaging", 3, K_CARD),

# ------------------------------------------------------------------ Harbor State CGM
# CG1: no insulin, but one level 3 event (neighbour needed to help) -> hypoglycaemia criterion; visit 2 months ago.
Y("Is this continuous glucose monitor order covered by Harbor State Medical Assistance?",
"""Harbor State Medical Assistance - DME prior authorisation
Order date: 16 June 2025 | Item: continuous glucose monitor
Member: Albertine Hollis-Nwachukwu, 78

Diabetes: type 2, treated with glipizide 10 mg twice daily and metformin. No insulin.

Hypoglycaemia history (from the practice note of 14 April 2025, in-person visit with Dr Oren Castellan, the prescriber):
"On 2 April her neighbour found her sitting in the garden confused and unable to explain what she was doing; he gave her orange juice and called paramedics, who measured glucose at 2.7 mmol/L. She recovered fully. Glipizide reduced to 5 mg twice daily. No other episodes recorded; she does not test her glucose at home."

Pharmacist note: "Not on insulin, only one low reading - likely not eligible."
""",
1, 2, card(CGM)),

# CG2: level 2 events 2.9 and 3.1 mmol/L -> only one below 3.0 -> no hypoglycaemia criterion -> not covered.
# Twin: second event 2.8 -> two level 2 events, second after dose adjustment -> covered.
Y("Does the member meet Harbor State's criteria for CGM coverage?",
"""Harbor State Medical Assistance - CGM request
Order date: 9 June 2025 | Member: Gustavo Lindqvist-Ade, 66
Prescriber: Dr Nadia Okafor, internal medicine (video visit 28 April 2025 about his diabetes)

Diabetes: type 2, gliclazide and metformin; no insulin.

Hypoglycaemia log (fingerstick meter download):
- 3 March 2025: 2.9 mmol/L, shaky and sweaty, treated himself with glucose tablets. Gliclazide dose reduced at a phone review on 5 March.
- 20 April 2025: 3.1 mmol/L, symptomatic, self-treated.
- No episodes requiring help from another person.

Prescriber note: "Two documented level 2 hypoglycaemic events, the second despite a dose reduction."
""",
0, 3, card(CGM),
twin=T([("20 April 2025: 3.1 mmol/L", "20 April 2025: 2.8 mmol/L")], 1)),

# CG3: on insulin (criterion met) but last prescriber diabetes visit 7 months ago; pharmacist phone call does not
# count -> visit requirement fails -> order should be denied (gold yes).
Y("Should Harbor State deny this CGM order?",
"""Harbor State Medical Assistance - DME request review
Order date: 22 September 2025 | Member: Evangeline Mbatha-Rowe, 59

Diabetes: type 2 since 2012, on insulin glargine 24 units nightly since 2020, plus metformin.

Encounters:
- 18 February 2025: in-person diabetes review with Dr Hollis Grant (the prescriber) - HbA1c 8.4%, insulin titration discussed.
- 29 August 2025: telephone call with the practice clinical pharmacist about glucose readings and injection technique; pharmacist forwarded the CGM order to Dr Grant, who signed it on 22 September without seeing the member.
- No other visits.

Reviewer comment: "Insulin user - these are routinely approved."
""",
1, 2, card(CGM)),

# ------------------------------------------------------------------ AAT-7 anti-amyloid
# AD1: MMSE 23 was 75 d ago (outside 60 d); MoCA 16 twenty days ago (most recent in window) < 17 -> cognitive stage.
C("Which AAT-7 condition, if any, is not met for this first infusion request?",
"""Brightwater Health Plan - AAT-7 anti-amyloid infusion request
Request date: 8 September 2025 | Member: Theodora Farrant-Okeke, 74
Prescriber: Dr Emil Vasquez-Oduya, cognitive neurology

Diagnosis: mild dementia due to Alzheimer's disease.
Cognitive testing:
- MMSE 23/30 on 25 June 2025 (memory clinic).
- MoCA 16/30 on 19 August 2025 (neurology clinic).
Amyloid PET (May 2025): positive.
MRI brain (July 2025): 2 microhaemorrhages; no superficial siderosis; no macrohaemorrhage.
Medication: aspirin 75 mg; donepezil 10 mg. No anticoagulant.
ApoE genotype: e3/e4; result and risks discussed with member and daughter on 1 August 2025 (documented).

Prescriber note: "MMSE 23 - squarely within the mild range."
""",
AD_OPTS, "cognitive stage", 3, AD_CARD),

# AD2: MRI shows 5 microhaemorrhages (> 4) -> baseline MRI fails -> not authorised. Twin: four -> authorised.
Y("Can the first infusion be authorised under AAT-7?",
"""Brightwater Health Plan - AAT-7 infusion review
Request date: 3 March 2025 | Member: Ambrose Lindholm-Adeyemi, 69

- Diagnosis: mild cognitive impairment due to Alzheimer's disease; MoCA 21 on 10 February 2025.
- Amyloid confirmation: CSF amyloid-beta 42/40 ratio low and p-tau181 raised (January 2025), consistent with Alzheimer's pathology.
- MRI brain (susceptibility-weighted imaging), 20 January 2025: five microhaemorrhages (all lobar, each under 5 mm); no superficial siderosis; no macrohaemorrhage; mild small-vessel change.
- Medication: clopidogrel 75 mg after a coronary stent in 2021; no anticoagulants.
- ApoE e4 heterozygote; counselling by the neurologist documented on 15 February 2025.

Neurologist note: "Small scattered microbleeds only, no siderosis, happy to proceed."
""",
0, 2, AD_YCARD,
twin=T([("five microhaemorrhages", "four microhaemorrhages")], 1)),

# AD3: amyloid shown only by plasma p-tau217 (blood test) -> amyloid confirmation fails. Clopidogrel allowed.
C("Which condition of the AAT-7 policy does this request fail, if any?",
"""From: Memory Clinic, Pellbridge Hospital
To: Brightwater Health Plan, specialty drugs
Date: 12 May 2025
Re: AAT-7 request - Mr Hugo Achterberg-Osei, 71

Dear colleagues,

Mr Achterberg-Osei has mild cognitive impairment due to Alzheimer's disease (MoCA 22 on 28 April 2025). His plasma p-tau217 was strongly positive in March 2025, a result our laboratory reports as more than 95% concordant with amyloid PET. He declined amyloid PET because of claustrophobia, and lumbar puncture was not possible because of previous spinal surgery.

MRI brain (February 2025): one microhaemorrhage, no siderosis, no macrohaemorrhage.
He takes clopidogrel for peripheral arterial disease; no anticoagulants.
ApoE testing: e3/e3; result discussed with him and his wife on 28 April 2025 and documented.

We would be grateful for authorisation to begin treatment.

Dr Olga Brightwater-Nnadi, Consultant in Old Age Psychiatry
""",
AD_OPTS, "amyloid confirmation", 2, AD_CARD),

# ------------------------------------------------------------------ Corvel fertility rider
# IV1: DOB 14 Oct 1982; cycle start 20 Oct 2025 -> age 43 -> age limit. Prior: 2 retrievals + 1 cancelled (count 2).
# Twin: cycle start 6 Oct 2025 -> age 42 -> none of these.
C("Which condition of the Corvel fertility rider, if any, does this request fail?",
"""Corvel Employee Health Plan - fertility rider pre-authorisation
Received: 1 September 2025
Member: Sabine Oduya-Lindgren | Date of birth: 14 October 1982
Planned IVF stimulation start date: 20 October 2025

Clinical summary (Harrowmere Fertility Centre):
- Trying to conceive with her husband for 14 months, regular unprotected intercourse, no pregnancy.
- Previous cycles under the Corvel plan: egg retrieval in March 2024; egg retrieval in October 2024; a third cycle in February 2025 was cancelled on day 8 before retrieval because of poor follicle response.
- AMH 0.9 ng/mL; husband's semen analysis normal.

Centre note: "Two completed retrievals only, so she is within the three-cycle limit. Request sent well ahead of the start date."
""",
I_OPTS, "age limit", 3, I_CARD,
twin=T([("stimulation start date: 20 October 2025", "stimulation start date: 6 October 2025")], NONE)),

# IV2: age 36, 8 months of trying -> infertility met (6 months if >= 35); other conditions met -> covered.
Y("Does this member meet all conditions of the Corvel fertility rider for the planned cycle?",
"""Corvel Employee Health Plan - fertility pre-authorisation request
Received: 4 August 2025 | Planned stimulation start: 15 September 2025
Member: Imani Castellanos-Reed, age 36 (date of birth 2 February 1989)

Fertility history (Harrowmere Fertility Centre):
- Regular unprotected intercourse with her partner for 8 months without pregnancy.
- No known medical cause of infertility identified so far; tubal patency confirmed; partner's semen analysis normal.
- No previous egg retrievals under any plan.

HR benefits team note: "Most plans require a year of trying - she has only been trying for 8 months, so this may be premature."
""",
1, 2, I_YCARD),

# IV3: request received 6 Oct after stimulation started 3 Oct -> prior authorisation fails -> not covered.
Y("Will the Corvel rider cover this stimulation cycle?",
"""Corvel Employee Health Plan - fertility pre-authorisation request (faxed)
Fax received: 6 October 2025, 16:42
Member: Rosamund Adair-Kiplagat, 38

Clinic cover note (Harrowmere Fertility Centre):
"Ms Adair-Kiplagat has a diagnosis of bilateral tubal blockage (confirmed on HSG, June 2025), so she qualifies without a trying period. She has had no previous retrievals. Because her cycle came early we started stimulation injections on 3 October 2025 to avoid losing a month; egg retrieval is expected around 15 October. Please treat this request as urgent."

Plan administrator note: "Tubal factor = documented medical cause. Age and cycle count fine."
""",
0, 1, I_YCARD),

# ------------------------------------------------------------------ SNF benefit
# SN1: observation Mon 22:00 - Wed 14:00; inpatient Wed 14:00 - Sat 11:00 -> midnights Wed, Thu, Fri = 3 -> qualifies;
# same-day SNF transfer; daily IV antibiotics. Twin: discharge Friday -> 2 midnights -> not covered.
Y("Is this skilled nursing facility stay covered under the Brightwater SNF benefit?",
"""Brightwater Health Plan - SNF benefit review
Member: Winifred Achebe-Stroud, 84

Hospital timeline (Pellbridge General):
- Monday 22:00: arrived in the emergency department with a fever and a painful red leg.
- Monday 23:40: placed under observation status on the medical ward.
- Wednesday 14:00: physician signs inpatient admission order (cellulitis failing oral antibiotics, started IV cefazolin).
- Stayed as an inpatient on IV antibiotics and was discharged to Pinecrest Skilled Nursing on Saturday at 11:00, admitted there the same afternoon.

SNF plan (physician-certified): IV cefazolin daily for 10 more days via a midline, daily wound care of the leg, physical therapy 5 days a week.

Case manager comment: "She was in hospital from Monday night to Saturday - five nights - so the stay is fine. But two of those were observation days, so we may have a problem."
""",
1, 3, S_YCARD,
twin=T([("on Saturday at 11:00", "on Friday at 11:00")], 0)),

# SN2: discharged 3 June, SNF admission 2 July -> 29 d (within 30); 5 inpatient midnights; PT 5 days/week -> covered.
Y("Does the member meet all three requirements of the Brightwater SNF benefit?",
"""Brightwater Health Plan - SNF benefit review
Member: Florian Okonkwo-Barrie, 79

- Inpatient admission 29 May 2025 (admitted directly from clinic with a hip fracture after a fall), hemiarthroplasty 30 May; discharged home on 3 June 2025 after 5 midnights as an inpatient.
- At home with his wife; initially coping, but struggled with transfers and fell twice without injury.
- Admitted to Riverside Skilled Nursing on 2 July 2025 after his orthopaedic follow-up; physician certifies need for daily physical and occupational therapy (at least 5 days a week) to restore walking and transfers after the hip fracture surgery.

Case manager comment: "He went home first and only went into the SNF a month later - I think the link to the hospital stay is broken."
""",
1, 2, S_YCARD),

# SN3: qualifying stay and transfer fine; needs only help with bathing/dressing and supervision walking, PT twice a
# week -> custodial -> daily skilled need fails.
C("Which requirement of the Brightwater SNF benefit, if any, is not met?",
"""Brightwater Health Plan - SNF benefit review
Member: Genevieve Stroud-Ekwueme, 88

Hospital: inpatient 10-14 August 2025 (4 midnights) for pneumonia, treated with IV then oral antibiotics; oral course completed in hospital.
Discharged 14 August 2025 directly to Maplewood Skilled Nursing.

SNF admission assessment (15 August 2025): "Alert, oriented. Needs help of one with bathing and dressing, and supervision when walking with her frame. Eating independently. No wounds, no IV lines, no oxygen. Physiotherapy twice a week for general mobility. Family unable to provide care at home."

Physician certification: "Requires 24-hour supervision and assistance with personal care."
""",
S_OPTS, "daily skilled need", 2, S_CARD),

# ------------------------------------------------------------------ Harrowfield kidney transplant listing
# TX1: breast cancer treatment completed 3 years ago -> 5-year interval needed -> cancer-free interval fails.
C("Which Harrowfield listing criterion, if any, prevents this candidate from being listed now?",
"""Harrowfield Transplant Centre - kidney transplant candidacy review
Candidate: Mrs Leonora Achterberg-Nwosu, 56 | Review date: 10 September 2025

Renal: not on dialysis. eGFR 18 mL/min/1.73 m2 on 2 June 2025 and 19 on 10 July 2025.
Height 1.62 m, weight 102 kg (BMI 38.9).
Oncology: right breast cancer (stage I, hormone-receptor positive), lumpectomy and radiotherapy completed in August 2022; adjuvant letrozole completed August 2025. Oncologist letter: "No evidence of disease; excellent prognosis."
Substance use: never drank alcohol; no drug use.
Support: husband (retired) named as 24-hour caregiver for the first month after surgery.

Coordinator note: "Oncology treatment finished three years ago - above the usual two-year wait."
""",
X_OPTS, "cancer-free interval", 3, X_CARD),

# TX2: eGFR 19 and 20 measured only 21 days apart, not on dialysis -> kidney function not yet met.
C("Which listing criterion, in the Harrowfield order, is the first one this candidate does not meet?",
"""Harrowfield Transplant Centre - referral triage
Candidate: Mr Oswin Farrell-Adeyemi, 49 | Referral date: 25 April 2025

Diagnosis: polycystic kidney disease; not on dialysis; dialysis access not yet created.
Renal: eGFR 19 mL/min/1.73 m2 on 2 April 2025; eGFR 20 on 23 April 2025.
BMI 29.4. No history of cancer.
Alcohol use disorder diagnosed 2019; abstinent since November 2023 (confirmed by his addiction service).
Caregiver: brother, who has arranged 3 weeks off work after the operation.

Referring nephrologist: "eGFR at or below 20 on two occasions - please list."
""",
X_OPTS, "kidney function", 2, X_CARD),

# TX3: all met: eGFR 17 and 15 45 d apart; BMI 112/1.675^2 = 39.9; low-risk prostate cancer on active surveillance;
# AUD abstinent 7 months; sister caregiver -> none of these.
C("Which Harrowfield listing criterion, if any, is not met?",
"""Harrowfield Transplant Centre - multidisciplinary listing meeting
Date: 4 December 2025 | Candidate: Mr Ignatius Mbeki-Fontaine, 63

- Renal: diabetic kidney disease, not on dialysis; eGFR 17 mL/min/1.73 m2 on 1 September 2025 and 15 on 16 October 2025.
- Anthropometrics: height 1.675 m, weight 112 kg.
- Oncology: low-risk prostate cancer (Gleason 3+3, PSA 5.1) diagnosed 2024, managed by active surveillance only; urology letter confirms stable PSA.
- Alcohol: alcohol use disorder; last drink 1 May 2025, abstinence confirmed by monthly PEth tests.
- Support: his sister will move in for the first 3 weeks after surgery and has signed the caregiver agreement.

Dietitian comment: "Weight 112 kg - BMI must be right at the limit."
Addiction nurse: "Seven months sober; doing well."
""",
X_OPTS, NONE, 3, X_CARD),
]
