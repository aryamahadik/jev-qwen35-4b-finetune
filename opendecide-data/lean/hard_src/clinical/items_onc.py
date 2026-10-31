"""Oncology trial items: VANTA-204 eligibility and ORCHID-HER2 cohort assignment."""
from common import (Y, C, T, card, crit, NONE, VANTA, VANTA_NONE, VANTA_LABS, ORCHID, labels)

V_OPTS, V_CARD = crit(VANTA, VANTA_NONE)
V_YCARD = card(VANTA)
L_OPTS, L_CARD = labels(VANTA_LABS), card(VANTA_LABS)
O_OPTS, O_CARD = labels(ORCHID), card(ORCHID)

ITEMS = [
# V1: Cockcroft-Gault. Female 71y, 52 kg, Cr 1.1 -> (69*52)/(72*1.1)*0.85 = 38.5 < 45 -> I6 fails -> not eligible.
# Twin 62 kg -> 45.9 -> eligible. Labs 4 Apr -> dose 16 Apr = 12 d; last dose 13 Mar -> 34 d; AST 1.45x ULN.
Y("Is Mrs Fanshawe eligible to receive her first VANTA-204 dose on 16 April?",
"""From: Priya Okonedo, Research Nurse, Lakemont Cancer Centre
To: Dr Anselm Vitt (VANTA-204 site PI)
Subject: VANTA-204 screening - patient 0417 (O.F.)
Date: 9 April 2025

Hi Anselm,

Summary for Mrs Oriel Fanshawe (71, female) before I book C1D1 for Wednesday 16 April. Consent signed 1 April.

Diagnosis: stage IV lung adenocarcinoma (liver and bone metastases), biopsy-confirmed June 2024. EGFR wild-type, ALK negative, PD-L1 60%.

Treatment history: carboplatin/pemetrexed/pembrolizumab x4 (July-Sept 2024), then pemetrexed/pembrolizumab maintenance until CT on 12 March 2025 showed progression in the liver. Last maintenance dose 13 March. No docetaxel, no radiotherapy of any kind.

Target lesion: segment VI liver lesion 31 mm, not irradiated.
ECOG 1. Brain MRI 2 April: no metastases.
Screening ECG: QTcF 452 ms. No cardiac history.

Screening bloods (4 April): ANC 3.2 x10^9/L; platelets 211 x10^9/L; Hb 11.4 g/dL (never transfused); total bilirubin 0.6 mg/dL (ULN 1.2); AST 58 U/L (ULN 40); ALT 49 U/L (ULN 45); serum creatinine 1.1 mg/dL (reference 0.50-1.10). Weight 52 kg, height 158 cm.

Other history: hypertension (amlodipine), hypothyroidism (levothyroxine). No neuropathy, no ILD or pneumonitis. Postmenopausal since 2004.

Let me know if you're happy for me to go ahead and book pharmacy.

Priya""",
0, 3, V_YCARD, twin=T([("Weight 52 kg", "Weight 62 kg")], 1)),

# V2: treated brain mets. SRS end 3 Mar; MRI 4 Apr (32 d) stable; dexamethasone last 11 Apr, C1D1 16 Apr -> 5 d < 7 -> E3.
# BCC excised (exception), grade 1 neuropathy, palliative RT 6 Apr -> 10 d. Twin: last steroid 7 Apr -> 9 d -> none.
C("Working through the VANTA-204 criteria in the order they are listed, which is the first criterion this subject fails?",
"""VANTA-204 eligibility worksheet - Subject 0522
Prepared by: T. Mbeki-Hart, CRC | Reviewed: pending PI sign-off

Patient: Mr Lorcan Adeyemi-Price, 58, male, 74 kg
Consent signed: 25 March 2025 | Planned C1D1: 16 April 2025

Oncology history
- Stage IV squamous NSCLC diagnosed Oct 2024; two brain metastases at diagnosis (right frontal 9 mm, left cerebellar 6 mm) plus bone metastases. PD-L1 5%. EGFR/ALK not tested (squamous histology).
- First line: cisplatin + gemcitabine x4, last dose 20 Feb 2025. CT 18 Mar 2025: progression, new 24 mm right lower lobe mass (measurable, not irradiated).
- CNS: stereotactic radiosurgery to both brain lesions, completed 3 March 2025. MRI brain 4 April 2025: both lesions smaller, no new lesions, no oedema. Dexamethasone started at SRS and tapered; last dose 11 April 2025. Neurologically intact.
- Palliative radiotherapy: 8 Gy single fraction to T8 vertebra on 6 April 2025.

Other history
- Basal cell carcinoma of the nose, excised with clear margins Feb 2023.
- Type 2 diabetes (metformin). Grade 1 sensory neuropathy of the fingertips since cisplatin.
- ECOG 1. QTcF 438 ms. No myocardial infarction.

Screening labs (9 April 2025): ANC 2.1; platelets 164; Hb 10.2 g/dL (no transfusion); bilirubin 0.8 mg/dL (ULN 1.2); AST 22, ALT 30 U/L (ULN 40); creatinine 0.9 mg/dL.""",
V_OPTS, "E3 brain metastases", 2, V_CARD,
twin=T([("last dose 11 April 2025", "last dose 7 April 2025")], NONE)),

# V3: neoadjuvant last dose 6 Feb 2024; recurrence 22 Jul 2024 (167 d, < 6 months) -> counts as a line;
# plus metastatic 1L -> two lines -> I3 fails. Twin recurrence 2 Sep 2024 (> 6 months) -> one line -> I3 met.
Y("Does Ms Solberg-Amadi satisfy inclusion criterion I3 of VANTA-204?",
"""Thoracic tumour board - 14 March 2025 - VANTA-204 pre-screen

Patient: Ms Henrike Solberg-Amadi, 63

Initial diagnosis (Nov 2023): stage IIIA adenocarcinoma of the left upper lobe.
Neoadjuvant carboplatin/paclitaxel + nivolumab x3, last dose 6 February 2024. Left upper lobectomy 12 March 2024 (ypT1b N1, R0). No adjuvant therapy given.

Recurrence: CT 22 July 2024 showed new left pleural nodules and an effusion; pleural fluid cytology confirmed adenocarcinoma. Restaged as stage IV.

Metastatic treatment: carboplatin/pemetrexed/pembrolizumab x4 from September 2024, then pemetrexed/pembrolizumab maintenance. CT 3 March 2025 shows progression of the pleural disease and a new 18 mm right adrenal metastasis.

Molecular profile: EGFR, ALK, ROS1, KRAS G12C all negative.
ECOG 1. MRI brain: no metastases. No docetaxel exposure.

Referring oncologist's comment: "One line of therapy in the metastatic setting, platinum-based - looks like a good fit for VANTA."

Board outcome: refer to research team for formal eligibility review.""",
0, 3, V_YCARD,
twin=T([("CT 22 July 2024 showed", "CT 2 September 2024 showed")], 1)),

# V4: labs. Transfusion 19 Apr -> sample 7 May = 18 d (ok). Bili 2.0x ULN with Gilbert (ok, <=3x).
# AST 104/40 = 2.6x > 2.5x and no liver mets -> AST or ALT. CrCl (80*80)/(72*1.2)=74. Twin: liver mets -> <=5x -> none.
C("Which laboratory requirement of criterion I6, if any, does this screening panel fail?",
"""VANTA-204 - screening laboratory review
Subject 0588: Mr Tobiah Klement, 60 years, male, weight 80 kg
Sample date: 7 May 2025 | Planned first dose: 14 May 2025

Haematology
- ANC 1.6 x10^9/L
- Platelets 102 x10^9/L
- Haemoglobin 9.3 g/dL. Note: 1 unit packed red cells transfused on 19 April 2025 for Hb 7.9 g/dL after haemoptysis.

Biochemistry
- Total bilirubin 2.4 mg/dL (ULN 1.2). Gilbert syndrome documented by hepatology in 2011 (unconjugated fraction 85%).
- AST 104 U/L (ULN 40)
- ALT 88 U/L (ULN 45)
- Serum creatinine 1.2 mg/dL (reference 0.7-1.3)

Staging CT chest/abdomen/pelvis (2 May 2025): primary right lower lobe mass 41 mm; right adrenal metastasis 27 mm; multiple sclerotic bone metastases. Liver: 9 mm simple cyst in segment IVa, unchanged since 2023; no hepatic metastases.

Ward comment: "LFTs have crept up since atorvastatin dose was increased - GP aware."
Coordinator comment: "Haemoglobin borderline after transfusion, bilirubin high - please check before I book."
""",
L_OPTS, "AST or ALT", 3, L_CARD,
twin=T([("no hepatic metastases", "two new hepatic metastases (14 mm and 11 mm)")], NONE)),

# V5: prostatectomy 18 Jan 2023, consent 2 Apr 2025 -> within 3 years; exception covers active surveillance only
# -> excluded. Skin SCC completely excised -> exception. Twin prostatectomy 18 Nov 2021 -> > 3 years -> not excluded.
Y("Should the screener record Mr Achterberg as excluded under criterion E4?",
"""Northfold Oncology Associates
3 April 2025

Dear Dr Vitt,

Re: Mr Desmond Achterberg, DOB 14/02/1957 - referral for VANTA-204

Thank you for seeing Mr Achterberg, who signed the VANTA-204 consent form with your team yesterday (2 April 2025). He has stage IV squamous cell carcinoma of the lung (bone and adrenal metastases) and progressed in March on first-line carboplatin/paclitaxel/pembrolizumab after six months of disease control. He remains very well, ECOG 0, and is keen to continue treatment.

Past medical history:
- Localised prostate adenocarcinoma (Gleason 3+4, PSA 7.2 at diagnosis), treated with robotic radical prostatectomy on 18 January 2023. PSA has been undetectable since, and he remains under PSA surveillance with urology every 6 months. No hormone therapy or radiotherapy.
- Squamous cell carcinoma of the skin of the left ear, completely excised in 2022.
- Hypertension, gout.

Medication: amlodipine 5 mg, allopurinol 300 mg.

Recent bloods are unremarkable and a brain MRI in March showed no metastases. I have enclosed his imaging reports and treatment summary.

Kind regards,

Dr Imelda Rookwood
Consultant Medical Oncologist""",
1, 2, V_YCARD,
twin=T([("prostatectomy on 18 January 2023", "prostatectomy on 18 November 2021")], 0)),

# V6: last chemo 4 Mar -> earliest 25 Mar (21 d); palliative RT ended 20 Mar -> earliest 27 Mar (7 d);
# labs 12 Mar valid to 26 Mar (14 d). No offered date satisfies all -> none of these.
# Twin labs 14 Mar -> valid to 28 Mar -> earliest 27 March 2025.
C("If no screening test is repeated, which is the earliest offered date on which the first VANTA-204 dose could be given?",
"""From: Hollis Varga (Clinical Research Coordinator)
To: VANTA-204 study team
Subject: Booking C1D1 - Subject 0611

Hi all,

Trying to get Mrs Ines Kavanagh-Oduya (66) booked for her first dose. Summary:

- Last chemotherapy: carboplatin/gemcitabine, cycle 4 day 8, given 4 March 2025.
- CT 10 March showed progression; she signed consent for VANTA-204 on 11 March.
- Screening bloods were drawn 12 March 2025 and every value met the protocol limits.
- ECG and brain MRI were done 13 March, both acceptable; the protocol lets these two stand for 28 days.
- She had a painful left hip metastasis and received palliative radiotherapy, 20 Gy in 5 fractions; the final fraction was on 20 March 2025.
- No other exclusions identified; PI has signed the eligibility checklist pending dosing date.

Pharmacy can prepare drug any weekday. The day unit has chairs free on Tuesday 25 March, Wednesday 26 March, Thursday 27 March and Tuesday 1 April. I'd like to book the earliest slot that works without calling her back in for repeat tests - she lives 90 minutes away and her daughter has to take time off work to drive her.

Thanks,
Hollis""",
["25 March 2025", "26 March 2025", "27 March 2025", "1 April 2025", NONE], NONE, 3,
card([("25 March 2025", "give the first dose on Tuesday 25 March 2025."),
      ("26 March 2025", "give the first dose on Wednesday 26 March 2025."),
      ("27 March 2025", "give the first dose on Thursday 27 March 2025."),
      ("1 April 2025", "give the first dose on Tuesday 1 April 2025."),
      (NONE, "none of the offered dates meets the protocol timing rules without repeating a screening test.")]),
twin=T([("drawn 12 March 2025", "drawn 14 March 2025")], "27 March 2025")),

# V7: grade 2 immune pneumonitis treated with prednisolone -> E7 applies regardless of resolution -> not enrollable.
Y("Can Mr Oyelaran-Brandt be enrolled in VANTA-204?",
"""Lakemont Cancer Centre - Thoracic Oncology Clinic
Date: 22 May 2025
Clinician: Dr Rosalind Achebe-Thorne

Mr Faisal Oyelaran-Brandt, 69.

Stage IV lung adenocarcinoma (liver metastases), KRAS G12V; EGFR and ALK negative.

First line: carboplatin/pemetrexed/pembrolizumab from September 2024. In November 2024 he developed a dry cough and breathlessness on exertion; CT showed new bilateral ground-glass change consistent with grade 2 immune-related pneumonitis. Pembrolizumab was held and he was treated with oral prednisolone 1 mg/kg, tapered over 6 weeks, with full clinical and radiological resolution by January 2025. Pembrolizumab was restarted in February 2025 with no recurrence of pneumonitis.

CT 12 May 2025: progression, new liver lesions (largest 22 mm).

Today: ECOG 1, SpO2 97% on room air. Pulmonary function tests (April 2025) normal. Brain MRI: no metastases. No docetaxel exposure. Screening bloods all within protocol limits (creatinine clearance 71 mL/min). QTcF 431 ms. No other malignancy.

Plan: he is keen on the VANTA-204 study; research nurse to complete formal eligibility review.""",
0, 2, V_YCARD),

# BK1: IHC 2+, ISH ratio 1.6, copy number 4.1 (< 6.0) -> ISH negative -> HER2-low -> cohort B; no ADC.
# Twin ratio 2.3 (>= 2.0, copy 4.1 >= 4.0) -> ISH positive -> cohort A.
C("Which ORCHID-HER2 cohort should this patient be assigned to?",
"""ORCHID-HER2 basket study - cohort assignment request
Site: Fairholme University Hospital | Submitted by: Dr Keziah Lindqvist

Patient: 57-year-old woman with metastatic gastric adenocarcinoma (peritoneal and liver disease), progressed after first-line FOLFOX.

Prior therapy: FOLFOX x8 cycles. No trastuzumab, no antibody-drug conjugates, no other HER2-directed treatment.

Pathology (gastric biopsy, 2 June 2025 - the most recent tissue tested):
- HER2 IHC (4B5): 2+ (moderate complete membranous staining in about 30% of tumour cells)
- Reflex dual-probe ISH: HER2/CEP17 ratio 1.6; average HER2 copy number 4.1 signals per cell; 40 nuclei counted. Final interpretive comment pending from the second pathologist.

Next-generation sequencing (tissue, 480-gene panel): ERBB2 not amplified; no ERBB2 mutation detected. Other findings: TP53 R273H, CDH1 splice variant (not relevant to cohort assignment).

Protocol note for coordinators: HER2 status is taken from the most recent tissue sample that was tested. If the sponsor's rules are met for more than one cohort, follow the priority written in the cohort definitions.

Coordinator note: "IHC 2+ - I assume this goes to the HER2-positive cohort? Please confirm before I register."
""",
O_OPTS, "cohort B", 2, O_CARD,
twin=T([("HER2/CEP17 ratio 1.6", "HER2/CEP17 ratio 2.3")], "cohort A")),

# BK2: most recent biopsy IHC 0 with activating ERBB2 exon 20 insertion; prior T-DXd -> cohort C allows prior therapy.
C("To which ORCHID-HER2 cohort, if any, does this patient belong?",
"""From: Oluwaseun Brightwater-Pike, Research Coordinator
To: ORCHID-HER2 eligibility desk
Subject: Cohort query - patient 22-0914

Hello,

Could you confirm cohort for the following patient before registration?

- 64-year-old man, metastatic lung adenocarcinoma (never-smoker), diagnosed 2022.
- Archival diagnostic biopsy (2022): HER2 IHC 2+, ISH not done.
- New liver biopsy (April 2025, most recent tissue tested): HER2 IHC 0.
- Tissue NGS on the April 2025 biopsy: ERBB2 exon 20 insertion (Y772_A775dupYVMA), annotated by our molecular tumour board as an activating mutation. No ERBB2 amplification.
- Treatment so far: carboplatin/pemetrexed/pembrolizumab (2022-2023); then trastuzumab deruxtecan, an anti-HER2 antibody-drug conjugate, from August 2023 to March 2025, stopped for progression.
- ECOG 1, adequate organ function, no untreated brain metastases.
- Protocol section 5.2: HER2 status for cohort assignment is taken from the most recent tissue sample tested.

Our PI thinks he is ineligible because he has already had an ADC, but the physician who referred him says the study was designed for exactly this kind of patient. Grateful for a definitive answer.

Best wishes,
Oluwaseun""",
O_OPTS, "cohort C", 3, O_CARD),

# BK3: IHC 1+ (HER2-low) but prior T-DXd (HER2 ADC); no ERBB2 mutation -> not eligible.
C("How should the eligibility desk classify this patient for ORCHID-HER2?",
"""ORCHID-HER2 - pre-registration checklist (Site 07, Brennock Cancer Institute)

Patient initials: M.T.-R. | Age: 49 | Sex: female
Tumour: metastatic hormone-receptor-positive breast cancer (bone, liver)

HER2 testing
- Primary tumour (2019): IHC 1+
- Liver biopsy (January 2025, most recent): IHC 1+, ISH not performed (not required for IHC 1+)

Molecular
- Plasma ctDNA (Feb 2025): PIK3CA H1047R; ESR1 Y537S; no ERBB2 mutation or amplification detected.

Prior systemic therapy (metastatic setting)
1. Letrozole + palbociclib (2020-2022)
2. Fulvestrant + alpelisib (2022-2023)
3. Trastuzumab deruxtecan (anti-HER2 antibody-drug conjugate), July 2023 - December 2024, stopped for progression
4. Capecitabine (January - May 2025), stopped for progression

Other: ECOG 1; LVEF 58%; no brain metastases; bloods adequate.

Coordinator comment: "HER2-low on the latest biopsy, so cohort B should be fine - the trastuzumab deruxtecan was a different drug class from the study agent."
""",
O_OPTS, "not eligible", 2, O_CARD),

# BK4: archival IHC 1+ (2021), most recent (2025) IHC 3+ -> HER2-positive by latest -> cohort A; prior trastuzumab
# (an antibody, not an ADC) is allowed.
C("Which cohort does the ORCHID-HER2 protocol assign this patient to?",
"""Molecular tumour board summary - Gallowmere Regional Cancer Centre - 11 June 2025

Case 4: 61-year-old man with metastatic colorectal adenocarcinoma (RAS/BRAF wild-type, microsatellite stable).

History: resected sigmoid primary 2021. Primary tumour HER2 IHC 1+. Lung and liver metastases 2023. Treated with FOLFOXIRI + bevacizumab, then FOLFIRI + panitumumab. Progressed in May 2025.

In early 2025 he received two months of trastuzumab (the naked antibody, not an antibody-drug conjugate) through a compassionate-access scheme, after an outside laboratory reported his lung lesion as HER2-amplified; it was stopped when access ended.

New biopsy (lung metastasis, 20 May 2025 - most recent tissue tested): HER2 IHC 3+ (strong complete membranous staining in 80% of cells). ISH not required.

NGS on the new biopsy: ERBB2 amplification (copy number 14); no ERBB2 point mutation.

No prior antibody-drug conjugate of any kind.

Board discussion: considerable disagreement about whether the 2021 primary result (IHC 1+) should decide cohort, since that was the diagnostic sample. ORCHID-HER2 protocol section 5.2 (read out at the meeting): "HER2 status for cohort assignment is taken from the most recent tissue sample tested."
""",
O_OPTS, "cohort A", 2, O_CARD),
]
