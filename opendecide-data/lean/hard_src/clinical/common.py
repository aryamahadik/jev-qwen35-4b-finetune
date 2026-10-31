"""Shared rulebooks and item helpers for the hard 'clinical' domain (v0.11 HARD track).

Eligibility and triage under written criteria: invented clinical-trial protocols, benefit schemes,
insurance pre-authorisation policies and triage scales. All trials, sponsors, plans, schemes,
hospitals and people are invented. Authored by the teacher (Claude); no external model or dataset.
Option labels never contain ": " so that card lines parse as "- <option>: <definition>".
"""

NONE = "none of these"


def card(pairs):
    return "\n".join(f"- {a}: {b}" for a, b in pairs)


def labels(pairs):
    return [a for a, _ in pairs]


def crit(rb, none_def, keys=None):
    """(options, card) for a criteria-list choice item; keys = optional subset of labels (in order)."""
    pairs = [p for p in rb if keys is None or p[0] in keys]
    return labels(pairs) + [NONE], card(pairs + [(NONE, none_def)])


def Y(q, state, gold, diff, card_text, twin=None, role="aff"):
    """Yes/no item; gold 1 = yes. twin = T(...)."""
    assert gold in (0, 1)
    return dict(qtype="noul", q=q, state=state, gold=gold, diff=diff, card=card_text, options=None,
                twin=twin, role=role)


def C(q, state, options, gold, diff, card_text, twin=None):
    """Choice item; gold is an option string."""
    assert gold in options, (gold, options)
    return dict(qtype="choice", q=q, state=state, gold=gold, diff=diff, card=card_text, options=options,
                twin=twin, role="choice")


def T(subs, gold, q=None):
    """Minimal-pair twin: (old, new) substitutions applied to the state, and the flipped gold."""
    return dict(subs=subs, gold=gold, q=q)


# ====================================================================== VANTA-204 (NSCLC, 2nd line)
VANTA = [
    ("I1 age", "aged 18 years or older on the date the consent form is signed."),
    ("I2 diagnosis", "histologically or cytologically confirmed non-small-cell lung cancer (NSCLC), stage IIIB/IIIC "
     "not amenable to curative treatment, or stage IV."),
    ("I3 prior therapy", "radiographic progression during or after exactly one prior line of systemic therapy for "
     "advanced or metastatic disease, and that line contained a platinum-based doublet. Maintenance therapy given "
     "after induction is part of the same line. Neoadjuvant or adjuvant therapy counts as a line only if disease "
     "progression occurred within 6 months of its last dose."),
    ("I4 measurable disease", "at least one lesion measurable per RECIST 1.1 (non-nodal lesion at least 10 mm in "
     "longest diameter, or lymph node at least 15 mm in short axis) that has not been irradiated, unless it has "
     "clearly progressed after irradiation."),
    ("I5 performance status", "ECOG performance status 0 or 1."),
    ("I6 laboratory values", "on samples taken no more than 14 days before the first dose: absolute neutrophil "
     "count at least 1.5 x 10^9/L; platelets at least 100 x 10^9/L; haemoglobin at least 9.0 g/dL with no red-cell "
     "transfusion in the 14 days before the sample; total bilirubin no more than 1.5 x ULN (3 x ULN with documented "
     "Gilbert syndrome); AST and ALT each no more than 2.5 x ULN (5 x ULN if liver metastases are present); "
     "creatinine clearance at least 45 mL/min by Cockcroft-Gault = (140 - age in years) x weight in kg / "
     "(72 x serum creatinine in mg/dL), multiplied by 0.85 for women."),
    ("E1 EGFR or ALK", "known sensitising EGFR mutation (exon 19 deletion or exon 21 L858R) or ALK rearrangement."),
    ("E2 prior docetaxel", "previous treatment with docetaxel in any setting."),
    ("E3 brain metastases", "untreated or symptomatic brain metastases. Treated brain metastases are allowed only if "
     "imaging at least 28 days after the end of brain-directed treatment shows no progression and the patient has "
     "taken no corticosteroids for at least 7 days before the first dose."),
    ("E4 second cancer", "another malignancy diagnosed or treated within 3 years before consent, except completely "
     "excised non-melanoma skin cancer, carcinoma in situ of the cervix, or localised prostate cancer managed by "
     "active surveillance alone."),
    ("E5 recent treatment", "fewer than 21 days between the last dose of any systemic anticancer therapy and the "
     "first dose; thoracic radiotherapy of more than 30 Gy within 6 months before the first dose; or palliative "
     "radiotherapy completed fewer than 7 days before the first dose (intervals are counted as the later date "
     "minus the earlier date, in calendar days)."),
    ("E6 neuropathy", "peripheral neuropathy of grade 2 or higher (CTCAE)."),
    ("E7 pneumonitis", "any history of interstitial lung disease, or of pneumonitis that required systemic "
     "corticosteroids."),
    ("E8 pregnancy", "pregnant or breastfeeding, or a woman of childbearing potential unwilling to use highly "
     "effective contraception."),
    ("E9 cardiac", "QTcF above 470 ms on the screening ECG, or myocardial infarction within 6 months before consent."),
]
VANTA_NONE = "the patient meets every inclusion criterion and no exclusion criterion applies."

VANTA_LABS = [
    ("ANC", "absolute neutrophil count at least 1.5 x 10^9/L."),
    ("platelets", "platelet count at least 100 x 10^9/L."),
    ("haemoglobin", "haemoglobin at least 9.0 g/dL, with no red-cell transfusion in the 14 days before the sample."),
    ("total bilirubin", "total bilirubin no more than 1.5 x ULN, or no more than 3 x ULN with documented Gilbert "
     "syndrome."),
    ("AST or ALT", "AST and ALT each no more than 2.5 x ULN, or each no more than 5 x ULN if liver metastases are "
     "present."),
    ("creatinine clearance", "creatinine clearance at least 45 mL/min by Cockcroft-Gault = (140 - age) x weight in "
     "kg / (72 x serum creatinine in mg/dL), x 0.85 for women."),
    (NONE, "every laboratory requirement of criterion I6 is met."),
]

# ====================================================================== ORCHID-HER2 (basket cohorts)
ORCHID = [
    ("cohort A", "HER2-positive: IHC 3+, or IHC 2+ with a positive ISH result (ISH is positive when the HER2/CEP17 "
     "ratio is 2.0 or more and the average HER2 copy number is 4.0 or more per cell, or when the copy number is "
     "6.0 or more whatever the ratio); and no prior HER2-directed antibody-drug conjugate."),
    ("cohort B", "HER2-low: IHC 1+, or IHC 2+ with a negative ISH result; and no prior HER2-directed antibody-drug "
     "conjugate."),
    ("cohort C", "an activating ERBB2 (HER2) mutation found by tissue or plasma next-generation sequencing, in a "
     "tumour that is not HER2-positive, regardless of prior HER2-directed therapy. A tumour meeting this definition "
     "is assigned to cohort C even if it also meets cohort B."),
    ("not eligible", "the tumour meets none of the cohort definitions."),
]

# ====================================================================== HALCYON-HF (heart failure)
HALCYON = [
    ("I1 age", "aged 40 years or older at screening."),
    ("I2 symptoms", "NYHA functional class II, III or IV at screening."),
    ("I3 ejection fraction", "left ventricular ejection fraction of 40% or less on the most recent echocardiogram, "
     "cardiac MRI or radionuclide scan performed in the 12 months before screening; if several were performed, "
     "only the most recent counts."),
    ("I4 natriuretic peptide", "NT-proBNP at screening of at least 600 pg/mL, or at least 900 pg/mL if the "
     "screening ECG shows atrial fibrillation or flutter. If the patient was admitted to hospital for heart failure "
     "in the 12 months before screening, the thresholds are 400 pg/mL and 600 pg/mL respectively."),
    ("I5 background therapy", "taking a beta-blocker and one of an ACE inhibitor, an angiotensin receptor blocker or "
     "sacubitril/valsartan, each at a stable dose for at least 4 weeks before screening, unless that drug class is "
     "contraindicated or was not tolerated and this is documented in the medical record."),
    ("E1 SGLT2 inhibitor", "any SGLT2 inhibitor (dapagliflozin, empagliflozin, canagliflozin, ertugliflozin, "
     "sotagliflozin, bexagliflozin) taken in the 8 weeks (56 days) before screening."),
    ("E2 kidney function", "eGFR below 25 mL/min/1.73 m2 at screening."),
    ("E3 blood pressure", "systolic blood pressure below 95 mmHg at screening, taken as the mean of the two seated "
     "readings."),
    ("E4 recent event", "acute coronary syndrome, stroke, transient ischaemic attack, cardiac surgery or "
     "percutaneous coronary intervention in the 12 weeks (84 days) before screening."),
    ("E5 type 1 diabetes", "type 1 diabetes mellitus."),
    ("E6 advanced therapy", "heart transplant or left ventricular assist device, or either planned within 6 months."),
    ("E7 potassium", "serum potassium above 5.5 mmol/L at screening."),
]
HALCYON_NONE = "the patient meets every inclusion criterion and no exclusion criterion applies."

# ====================================================================== GLYDE-3 (type 2 diabetes + obesity)
GLYDE = [
    ("I1 age", "aged 18 to 75 years inclusive at screening."),
    ("I2 diabetes duration", "type 2 diabetes diagnosed at least 180 days before screening."),
    ("I3 HbA1c", "HbA1c from 7.0% to 10.5% inclusive at screening, i.e. 53 to 91 mmol/mol "
     "(mmol/mol = (% - 2.15) x 10.929)."),
    ("I4 BMI", "body mass index of at least 27.0 kg/m2, calculated from screening height and weight "
     "(1 inch = 2.54 cm; 1 lb = 0.4536 kg) and rounded to one decimal place."),
    ("I5 metformin", "metformin at a stable dose of at least 1500 mg/day for at least 90 days before screening, or "
     "at least 1000 mg/day if intolerance of higher doses is documented."),
    ("E1 incretin therapy", "any GLP-1 receptor agonist or dual GIP/GLP-1 receptor agonist (for example semaglutide, "
     "liraglutide, dulaglutide, exenatide, tirzepatide), prescribed or compounded, taken in the 180 days before "
     "screening."),
    ("E2 pancreatitis", "any diagnosis of acute or chronic pancreatitis at any time."),
    ("E3 thyroid cancer risk", "medullary thyroid carcinoma or multiple endocrine neoplasia type 2 in the participant "
     "or in a parent, sibling or child."),
    ("E4 kidney function", "eGFR below 30 mL/min/1.73 m2 at screening."),
    ("E5 bariatric surgery", "any bariatric surgery, except an adjustable gastric band removed more than 12 months "
     "before screening."),
    ("E6 weight instability", "a change in body weight of more than 5% (up or down, as a percentage of the earlier "
     "weight) between any recorded weight in the 90 days before screening and the screening weight."),
]
GLYDE_NONE = "the participant meets every inclusion criterion and no exclusion criterion applies."

# ====================================================================== ARBOR-RA (rheumatoid arthritis)
ARBOR = [
    ("I1 age", "aged 18 to 70 years inclusive at screening."),
    ("I2 diagnosis", "rheumatoid arthritis meeting the 2010 ACR/EULAR classification criteria, diagnosed at least "
     "6 months before screening."),
    ("I3 active disease", "at screening, at least 6 swollen joints (66-joint count) and at least 6 tender joints "
     "(68-joint count), and either C-reactive protein of at least 10 mg/L (1 mg/dL = 10 mg/L) or ESR of at least "
     "28 mm/h."),
    ("I4 methotrexate", "inadequate response to methotrexate taken for at least 12 weeks, with a stable dose of 15 to "
     "25 mg/week for the last 4 weeks before baseline; a stable dose of 10 to less than 15 mg/week is acceptable "
     "only if intolerance of higher doses is documented."),
    ("E1 prior advanced therapy", "any prior JAK inhibitor; more than one prior biologic DMARD; or a single prior "
     "biologic DMARD stopped because of lack or loss of efficacy. A single prior biologic stopped for intolerance, "
     "cost or access reasons is allowed."),
    ("E2 tuberculosis", "active tuberculosis, or a positive interferon-gamma release assay at screening unless at "
     "least 4 weeks of latent-TB prophylaxis have been completed before baseline and will be continued."),
    ("E3 corticosteroids", "oral prednisone (or equivalent) above 10 mg/day, or any change in corticosteroid dose, in "
     "the 4 weeks before baseline."),
    ("E4 hepatitis B", "positive hepatitis B surface antigen, or positive hepatitis B core antibody together with "
     "detectable HBV DNA."),
    ("E5 live vaccine", "a live vaccine in the 42 days before baseline. Live vaccines include MMR, varicella, yellow "
     "fever, oral typhoid and live attenuated zoster vaccine; recombinant zoster vaccine and inactivated influenza "
     "vaccine are not live."),
]
ARBOR_NONE = "the patient meets every inclusion criterion and no exclusion criterion applies."

# ====================================================================== LUMEN-TRD (treatment-resistant depression)
LUMEN = [
    ("I1 age", "aged 18 to 65 years inclusive at screening."),
    ("I2 current episode", "current major depressive episode (DSM-5) of at least 8 weeks' duration at screening, "
     "without psychotic features."),
    ("I3 severity", "MADRS total score of 28 or more at both screening and baseline, with no more than 25% "
     "improvement from the screening score to the baseline score."),
    ("I4 treatment resistance", "inadequate response to at least 2 and no more than 5 adequate antidepressant trials "
     "in the current episode. An adequate trial is at least 6 consecutive weeks at or above the minimum daily dose: "
     "sertraline 50 mg, escitalopram 10 mg, citalopram 20 mg, fluoxetine 20 mg, paroxetine 20 mg, venlafaxine "
     "150 mg, duloxetine 60 mg, bupropion 300 mg, mirtazapine 30 mg, vortioxetine 10 mg."),
    ("E1 bipolar or psychosis", "lifetime diagnosis of bipolar disorder, schizophrenia or another psychotic disorder."),
    ("E2 suicide risk", "suicidal ideation with at least some intent to act, or with a specific plan (C-SSRS ideation "
     "item 4 or 5), in the 6 months before screening, or a suicide attempt in the 12 months before screening."),
    ("E3 substance use", "moderate or severe substance use disorder (other than nicotine or caffeine) in the 6 months "
     "before screening."),
    ("E4 washout", "fewer than 14 days between the last dose of a monoamine oxidase inhibitor and baseline, or fewer "
     "than 35 days between the last dose of fluoxetine and baseline."),
    ("E5 neuromodulation", "electroconvulsive therapy in the 6 months before screening, or a course of ECT without "
     "response in the current episode."),
]
LUMEN_NONE = "the participant meets every inclusion criterion and no exclusion criterion applies."

# ====================================================================== PIPIT-RSV (infant vaccine)
PIPIT = [
    ("I1 age window", "aged 42 to 90 days inclusive on the day of vaccination, counting the date of birth as day 0."),
    ("I2 gestation", "born at a gestational age of at least 36 weeks 0 days."),
    ("I3 birth weight", "birth weight of at least 2.5 kg."),
    ("E1 prior RSV protection", "any prior RSV monoclonal antibody (nirsevimab, palivizumab or clesrovimab), or a "
     "maternal RSV vaccine given at least 14 days before the infant's birth."),
    ("E2 recent fever", "temperature of 38.0 C or higher on the day of vaccination or on any of the 3 calendar days "
     "before it (a temporary exclusion: the infant may be vaccinated once outside that window)."),
    ("E3 immunodeficiency", "known or suspected immunodeficiency in the infant, or a household contact with a severe "
     "immunodeficiency."),
    ("E4 blood products", "receipt of blood, blood products or immunoglobulin since birth."),
]
PIPIT_NONE = "the infant meets every inclusion criterion and no exclusion criterion applies."

# ====================================================================== KIDNEX (chronic kidney disease)
KIDNEX = [
    ("I1 age", "aged 18 to 80 years inclusive at screening."),
    ("I2 eGFR", "eGFR (CKD-EPI 2021) from 25 to 75 mL/min/1.73 m2 inclusive at screening."),
    ("I3 albuminuria", "urine albumin-to-creatinine ratio (UACR) from 200 to 5000 mg/g inclusive on the screening "
     "sample (1 mg/mmol = 8.84 mg/g)."),
    ("I4 RAS blockade", "taking either an ACE inhibitor or an angiotensin receptor blocker, but not both, at the "
     "maximum labelled or maximum tolerated dose, unchanged for at least 4 weeks before screening, unless both "
     "classes are contraindicated or not tolerated (documented)."),
    ("E1 type 1 diabetes", "type 1 diabetes."),
    ("E2 kidney replacement", "current dialysis, prior kidney transplant, or either planned within 6 months."),
    ("E3 potassium", "serum potassium above 5.0 mmol/L at screening."),
    ("E4 immunosuppression", "systemic immunosuppressive therapy for kidney disease at any time in the 6 months "
     "before screening: mycophenolate, cyclophosphamide, rituximab or a calcineurin inhibitor at any dose, or "
     "prednisone (or equivalent) at a dose above 7.5 mg/day (lower corticosteroid doses do not count)."),
    ("E5 recent AKI", "acute kidney injury, or a rise in serum creatinine of more than 30% above the previous value, "
     "in the 12 weeks before screening."),
]
KIDNEX_NONE = "the participant meets every inclusion criterion and no exclusion criterion applies."

# ====================================================================== NVX-101 first-in-human (healthy volunteers)
PH_INC = [
    ("I1 age", "aged 18 to 55 years inclusive on the day of screening."),
    ("I2 language", "able to read, understand and sign the informed consent form in English."),
    ("I3 availability", "able to stay in the unit for 6 consecutive nights and attend all follow-up visits."),
]
PH_EXC = [
    ("E1 body size", "body mass index outside 18.5 to 30.0 kg/m2 inclusive, or body weight below 50.0 kg."),
    ("E2 blood pressure", "seated systolic blood pressure outside 90-140 mmHg or diastolic outside 50-90 mmHg; if the "
     "first reading is out of range one repeat is allowed and the repeat value is used."),
    ("E3 heart rate", "resting heart rate below 45 or above 100 beats per minute."),
    ("E4 ECG", "QTcF above 450 ms in men or above 470 ms in women, or PR interval above 220 ms."),
    ("E5 nicotine", "use of any nicotine-containing product (cigarettes, vapes, pouches, patches, gum) in the 3 months "
     "before screening."),
    ("E6 alcohol", "average intake of more than 14 units of alcohol per week (units = volume in mL x ABV% / 1000)."),
    ("E7 drug screen", "positive urine drug screen not explained by a documented prescription."),
    ("E8 blood donation", "donation or loss of more than 400 mL of blood in the 90 days before dosing, or plasma "
     "donation in the 14 days before dosing."),
    ("E9 prior study", "dosing in another clinical study within 90 days, or within 5 half-lives of that study's drug "
     "if longer, before dosing in this study."),
    ("E10 medications", "any prescription medicine in the 14 days before dosing, or any non-prescription medicine, "
     "vitamin or herbal product in the 7 days before dosing, except paracetamol up to 2 g/day and hormonal "
     "contraception."),
    ("E11 enzyme inducers", "St John's wort or any other strong CYP3A inducer in the 28 days before dosing."),
    ("E12 grapefruit", "grapefruit, Seville orange or pomelo, or their juice, in the 7 days before dosing."),
    ("E13 vaccines", "any vaccine in the 14 days before dosing."),
    ("E14 viral serology", "positive HIV antibody or hepatitis B surface antigen, or positive hepatitis C antibody "
     "(a positive hepatitis C antibody is acceptable if HCV RNA is undetectable after documented curative "
     "treatment)."),
    ("E15 liver tests", "ALT or AST above 1.5 x ULN, or total bilirubin above ULN unless Gilbert syndrome is "
     "documented."),
    ("E16 kidney function", "eGFR below 80 mL/min/1.73 m2."),
    ("E17 allergy", "history of anaphylaxis, or allergy to any component of the formulation (NVX-101, polysorbate 80, "
     "mannitol)."),
    ("E18 surgery", "major surgery in the 12 weeks before screening, or surgery planned during the study."),
    ("E19 pregnancy", "pregnant or breastfeeding, or (women of childbearing potential) unwilling to use the specified "
     "contraception."),
    ("E20 venous access", "veins unsuitable for repeated cannulation or blood sampling."),
    ("E21 psychiatric", "psychiatric hospital admission in the past 5 years, or any lifetime suicide attempt."),
    ("E22 caffeine", "habitual intake of more than 500 mg caffeine per day (per serving: coffee 100 mg, tea 50 mg, "
     "cola 40 mg, energy drink 80 mg)."),
    ("E23 exercise", "unwilling to avoid strenuous exercise from 72 hours before admission until discharge."),
    ("E24 site staff", "employee of the study site or sponsor, or a family member of one."),
]
PH_NONE = "every listed criterion is satisfied: all inclusion criteria are met and no exclusion criterion applies."

# ====================================================================== St Aldric's thrombolysis protocol
STROKE = [
    ("time window", "the thrombolytic bolus must start no later than 4 hours 30 minutes after the patient was last "
     "known well, i.e. the last time the patient was seen, heard or otherwise known to be at their neurological "
     "baseline, including a documented brief awakening during the night."),
    ("blood pressure", "blood pressure above 185/110 mmHg that cannot be brought to 185/110 mmHg or below with at "
     "most two doses of intravenous antihypertensive."),
    ("glucose", "blood glucose below 2.8 mmol/L or above 22.0 mmol/L at the time of the decision (a low glucose may "
     "be corrected and the patient reassessed; the reassessment value is used)."),
    ("platelets", "platelet count below 100 x 10^9/L."),
    ("anticoagulant", "warfarin with INR above 1.7; any direct oral anticoagulant (apixaban, rivaroxaban, edoxaban, "
     "dabigatran) taken within 48 hours unless a drug-specific level is below the laboratory's no-effect cut-off; "
     "or a treatment dose of low-molecular-weight heparin within 24 hours."),
    ("prior stroke", "ischaemic stroke or serious head injury in the previous 3 months."),
    ("haemorrhage history", "any previous intracranial haemorrhage."),
    ("recent surgery", "major surgery in the previous 14 days."),
    ("GI or urinary bleeding", "gastrointestinal or urinary tract haemorrhage in the previous 21 days."),
]
STROKE_NONE = "no listed contraindication applies."

# ====================================================================== Brightwater RAD-114 lumbar MRI
MRI = [
    ("criterion A red flag", "at least one of: suspected cauda equina syndrome (new urinary retention or "
     "incontinence, saddle anaesthesia, or bilateral leg weakness); a motor deficit of 3/5 or weaker, or one "
     "documented as worsening between two examinations; suspected spinal infection (temperature of 38.0 C or more "
     "with back pain in a patient who injects drugs, is immunosuppressed, or had a spinal procedure in the previous "
     "3 months); known current or previous cancer other than non-melanoma skin cancer, with new back pain; "
     "suspected fracture after major trauma, or after minor trauma in a patient aged 70 or over or on long-term oral "
     "corticosteroids."),
    ("criterion B failed conservative care", "back pain or radiculopathy persisting after at least 6 weeks of "
     "clinician-directed conservative care within the past 6 months, including at least two of: (i) physical "
     "therapy with at least 4 attended sessions; (ii) an NSAID or paracetamol taken regularly for at least 3 weeks; "
     "(iii) a home exercise programme documented by the treating clinician; (iv) at least 4 chiropractic or "
     "osteopathic visits. The 6 weeks run from the start of the earliest qualifying modality to the request date."),
    ("criterion C surgical planning", "a spine surgeon (orthopaedic or neurosurgical) has documented that surgery or "
     "an interventional spine procedure is being planned and that imaging is needed to plan it."),
]
MRI_REPEAT = ("repeat imaging rule", "a lumbar MRI requested within 12 months of a previous lumbar MRI is covered "
              "only if criterion A is met or a new neurological deficit has appeared since the previous MRI.")
MRI_DECISION = ("approval rule", "the request is approved if at least one of criteria A, B or C is met and the "
                "repeat imaging rule does not prevent it; otherwise it is denied.")
MRI_NONE = "the request meets none of criteria A, B or C."

# ====================================================================== Brightwater BAR-02 bariatric surgery
BARI = [
    ("R1 age", "the member is 18 or older."),
    ("R2 BMI", "BMI of 40 or more, or 35 or more with at least one of: type 2 diabetes; obstructive sleep apnoea with "
     "an AHI of 15 or more per hour; hypertension needing at least two antihypertensive drugs; fatty liver disease "
     "with fibrosis confirmed by biopsy or elastography. BMI is measured within 90 days before the request; if the "
     "member lost weight during the programme in R3, the highest BMI documented in the 24 months before the request "
     "may be used instead."),
    ("R3 supervised programme", "a medically supervised weight-management programme with at least 6 visits spanning "
     "at least 6 months, all within the 12 months before the request, with no gap of more than 60 days between "
     "consecutive visits. Visits in a commercial programme count only if each is co-signed by a physician or nurse "
     "practitioner."),
    ("R4 psychological clearance", "a psychological evaluation within the 12 months before the request stating that "
     "the member is cleared for surgery."),
    ("R5 nutrition", "at least one consultation with a registered dietitian within the 12 months before the request."),
    ("R6 nicotine", "no nicotine in any form (smoking, vaping, pouches or nicotine replacement) for at least 6 weeks "
     "before the request, confirmed by a negative cotinine test in the 30 days before the request."),
]
BARI_NONE = "all six requirements are met."

# ====================================================================== Brightwater PH-PCSK9
PCSK = [
    ("requirement 1 diagnosis", "clinical ASCVD (prior myocardial infarction or acute coronary syndrome, coronary or "
     "peripheral revascularisation, ischaemic stroke or TIA, or symptomatic peripheral arterial disease) or "
     "heterozygous familial hypercholesterolaemia (Dutch Lipid Clinic Network score above 8, or a pathogenic LDLR, "
     "APOB or PCSK9 variant)."),
    ("requirement 2 LDL-C", "LDL-C of at least 70 mg/dL (ASCVD) or at least 100 mg/dL (familial "
     "hypercholesterolaemia without ASCVD) on the most recent test, which must have been drawn within 90 days "
     "before the request (mg/dL = mmol/L x 38.67)."),
    ("requirement 3 prior therapy", "at least 8 continuous weeks of a high-intensity statin (atorvastatin 40-80 mg or "
     "rosuvastatin 20-40 mg daily) plus ezetimibe 10 mg daily; or, if the member is statin-intolerant, ezetimibe "
     "for 8 weeks. Statin intolerance means documented intolerable muscle symptoms on at least two different "
     "statins, at least one of them at its lowest starting dose (atorvastatin 10 mg, rosuvastatin 5 mg, simvastatin "
     "10 mg, pravastatin 10 mg), or rhabdomyolysis (CK above 10 x ULN) on any statin."),
]
PCSK_NONE = "all three requirements are met."

# ====================================================================== Brightwater anti-IL-5 asthma biologic
ASTHMA = [
    ("requirement 1 age and diagnosis", "age 12 or older, with severe asthma diagnosed by a pulmonologist, allergist "
     "or immunologist."),
    ("requirement 2 eosinophils", "blood eosinophil count of at least 150 cells/uL in the 6 weeks before the request, "
     "or at least 300 cells/uL at any time in the 12 months before the request (1 x 10^9/L = 1000 cells/uL)."),
    ("requirement 3 exacerbations", "in the 12 months before the request, at least two exacerbations each treated "
     "with systemic corticosteroids for at least 3 days, or at least one exacerbation that led to hospital admission "
     "(an emergency-department visit without admission is not a hospital admission)."),
    ("requirement 4 controller therapy", "at least 3 months of adherent use of a high-dose inhaled corticosteroid "
     "plus a second controller (LABA, LAMA or leukotriene modifier) immediately before the request."),
    ("requirement 5 no other biologic", "the drug will not be used at the same time as another biologic "
     "(omalizumab, dupilumab, tezepelumab, benralizumab, reslizumab or mepolizumab), whatever the indication of "
     "that other biologic."),
]
ASTHMA_NONE = "all five requirements are met."

# ====================================================================== Brightwater total knee arthroplasty
TKA = [
    ("requirement 1 imaging", "a weight-bearing (standing) knee X-ray within 12 months before the request showing "
     "Kellgren-Lawrence grade 3 or 4 osteoarthritis, or an MRI showing osteonecrosis."),
    ("requirement 2 conservative care", "at least 3 months of conservative care within the 12 months before the "
     "request, using at least two of: physical therapy or a supervised exercise programme; an NSAID or paracetamol; "
     "an intra-articular injection; a brace or walking aid."),
    ("requirement 3 BMI", "BMI below 40, or below 45 if the surgeon documents a weight-optimisation plan and a "
     "completed anaesthesia risk review."),
    ("requirement 4 glycaemic control", "for members with diabetes, HbA1c of 8.0% or lower on a test within 90 days "
     "before the planned surgery date."),
    ("requirement 5 nicotine", "no nicotine use in the 4 weeks before the request."),
]
TKA_NONE = "all five requirements are met."

# ====================================================================== Harbor State CGM coverage
CGM = [
    ("insulin criterion", "the member uses insulin (any number of daily injections, or an insulin pump)."),
    ("hypoglycaemia criterion", "the member does not use insulin but has had problematic hypoglycaemia: at least two "
     "level 2 events (glucose below 54 mg/dL, i.e. below 3.0 mmol/L) on separate days with at least one of them "
     "after a medication adjustment, or at least one level 3 event (an altered mental or physical state in which "
     "the member needed another person's help to treat the low glucose)."),
    ("visit requirement", "an in-person or video visit with the prescribing practitioner about the member's diabetes "
     "in the 6 months before the order."),
    ("coverage rule", "a CGM is covered when the insulin criterion or the hypoglycaemia criterion is met, and the "
     "visit requirement is met."),
]

# ====================================================================== AAT-7 anti-amyloid infusion policy
AAT = [
    ("cognitive stage", "mild cognitive impairment or mild dementia due to Alzheimer's disease, with MMSE 22-30 or "
     "MoCA 17-30 on a test in the 60 days before the request (if more than one test falls in that period, the most "
     "recent one is used)."),
    ("amyloid confirmation", "amyloid pathology confirmed by amyloid PET or by cerebrospinal fluid biomarkers; blood "
     "tests alone do not qualify."),
    ("baseline MRI", "brain MRI within 12 months before the first infusion showing no more than 4 microhaemorrhages, "
     "no more than 1 area of superficial siderosis and no macrohaemorrhage larger than 1 cm."),
    ("anticoagulation", "not currently taking an anticoagulant (warfarin, apixaban, rivaroxaban, edoxaban, dabigatran "
     "or any heparin); antiplatelet drugs are allowed."),
    ("ApoE4 counselling", "ApoE e4 genotype has been tested and the result discussed with the member, with the "
     "discussion documented."),
]
AAT_NONE = "all five conditions are met."

# ====================================================================== Corvel fertility rider
IVF = [
    ("infertility", "failure to achieve pregnancy after 12 months of regular unprotected intercourse, or after 6 "
     "months if the person who would carry the pregnancy is 35 or older; or after 6 cycles of donor insemination "
     "(3 if 35 or older); or a medical cause of infertility diagnosed by a physician."),
    ("age limit", "the person whose eggs will be retrieved is under 43 on the date the stimulation cycle starts."),
    ("cycle limit", "no more than 3 egg-retrieval cycles in total under any Corvel plan, including this one; a cycle "
     "cancelled before egg retrieval does not count, and retrievals paid by other insurers do not count."),
    ("prior authorisation", "the request is received before the stimulation cycle starts."),
]
IVF_NONE = "all four conditions are met."

# ====================================================================== Brightwater skilled nursing facility benefit
SNF = [
    ("qualifying stay", "a hospital stay that includes at least 3 consecutive midnights as a formally admitted "
     "inpatient; time in the emergency department or under observation status before the inpatient admission order "
     "does not count, and the day of discharge does not add a midnight."),
    ("timely transfer", "admission to the skilled nursing facility within 30 days after the date of hospital "
     "discharge."),
    ("daily skilled need", "a physician-certified need for skilled nursing or skilled rehabilitation services "
     "(e.g. IV therapy, wound care of a surgical or stage 3-4 wound, physical or occupational therapy at least 5 "
     "days a week) for a condition treated during the qualifying stay; help only with bathing, dressing, eating or "
     "walking is custodial care and does not qualify."),
]
SNF_NONE = "all three requirements are met."

# ====================================================================== Harrowfield kidney transplant listing
TX = [
    ("kidney function", "on maintenance dialysis, or eGFR of 20 mL/min/1.73 m2 or less on two measurements taken at "
     "least 30 days apart."),
    ("BMI", "BMI below 40.0 kg/m2 at evaluation."),
    ("cancer-free interval", "no cancer within the required interval after the end of curative treatment: 5 years for "
     "melanoma, breast and colorectal cancer; 2 years for other cancers; no interval for non-melanoma skin cancer or "
     "low-risk prostate cancer managed by active surveillance."),
    ("substance use", "for candidates with an alcohol or drug use disorder, at least 6 months of documented "
     "abstinence before listing."),
    ("support plan", "a named caregiver who will provide 24-hour support for at least the first 2 weeks after "
     "surgery."),
]
TX_NONE = "all listing criteria are met."

# ====================================================================== Tallis County Carer Support Payment
CARER = [
    ("rule 1 age", "the claimant is aged 16 or over."),
    ("rule 2 caring", "the claimant spends at least 35 hours a week caring for one person who receives a qualifying "
     "disability benefit: the daily living part of Personal Independence Allowance (either rate), Attendance "
     "Supplement (either rate), or Armed Forces Independence Payment. Hours spent caring for different people "
     "cannot be added together, and the mobility part of Personal Independence Allowance on its own does not "
     "qualify."),
    ("rule 3 earnings", "net weekly earnings of 151.00 pounds or less. Net earnings are gross earnings minus income "
     "tax, National Insurance and half of any pension contributions; from that figure, care costs paid to someone "
     "who is not a close relative (parent, sibling, child or partner) for looking after the cared-for person, or the "
     "claimant's child under 16, while the claimant works may also be deducted, up to 50% of that figure."),
    ("rule 4 education", "the claimant is not in full-time education (21 or more hours a week of supervised study)."),
]
CARER_NONE = "all four entitlement rules are met."

# ====================================================================== Northmere medical exemption certificate
RX = [
    ("permanent fistula", "a permanent fistula (for example a colostomy, ileostomy, laryngostomy or caecostomy) "
     "needing continuous surgical dressing or an appliance."),
    ("hypoadrenalism", "a form of hypoadrenalism, such as Addison's disease, for which specific substitution therapy "
     "is essential."),
    ("hypopituitarism", "diabetes insipidus or another form of hypopituitarism."),
    ("diabetes mellitus", "diabetes mellitus, except where it is treated by diet alone."),
    ("hypoparathyroidism", "hypoparathyroidism."),
    ("myasthenia gravis", "myasthenia gravis."),
    ("hypothyroidism", "hypothyroidism (myxoedema) needing thyroid hormone replacement."),
    ("epilepsy", "epilepsy needing continuous anticonvulsant therapy."),
    ("physical disability", "a continuing physical disability that means the person cannot go out without the help of "
     "another person; a temporary disability does not count, even if it lasts several months."),
    ("cancer treatment", "currently having treatment for cancer, for the effects of cancer, or for the effects of "
     "cancer treatment."),
]
RX_NONE = "no listed condition applies."

# ====================================================================== KVETS triage scale
KVETS = [
    ("level 1", "the patient needs an immediate life-saving intervention now: airway or breathing support "
     "(bag-valve-mask ventilation, intubation), defibrillation or pacing, emergency drugs for a life threat (such as "
     "naloxone for respiratory depression or adrenaline for anaphylaxis), or major fluid or blood resuscitation; or "
     "the patient is unresponsive to both voice and pain."),
    ("level 2", "not level 1, and either (a) a high-risk situation: suspected stroke with onset in the past 24 hours, "
     "chest pain that could be acute coronary syndrome, new confusion, lethargy or disorientation, suicidal or "
     "homicidal intent with a plan, any infant under 90 days old with temperature of 38.0 C or more, or severe pain "
     "or distress (7/10 or more) that the nurse judges needs immediate relief; or (b) the patient would be level 3 "
     "and has a danger-zone vital sign: age 8 or over, heart rate above 100/min, respiratory rate above 20/min or "
     "SpO2 below 92%; age 1-7 years, HR above 140 or RR above 30; age 3-12 months, HR above 160 or RR above 40."),
    ("level 3", "not level 1 or 2, and expected to need two or more resources. Each resource type counts once however "
     "many items of that type are ordered: laboratory tests on blood or urine sent to the lab; plain X-ray; CT, MRI "
     "or ultrasound; intravenous fluids; intravenous, intramuscular or nebulised medication; specialist "
     "consultation; a simple procedure such as laceration repair or urinary catheter (one resource); a complex "
     "procedure such as procedural sedation (two resources). Not resources: history and examination, point-of-care "
     "tests (fingerstick glucose, urine dipstick, urine pregnancy test), saline lock, oral medication, tetanus "
     "vaccination, prescription refills, simple wound cleaning and dressing, crutches, splints and slings."),
    ("level 4", "not level 1 or 2, and expected to need exactly one resource (resources as defined for level 3)."),
    ("level 5", "not level 1 or 2, and expected to need no resources (resources as defined for level 3)."),
]

# ====================================================================== Fastpath suspected-cancer referral
FAST = [
    ("upper GI fastpath", "dysphagia at any age; or age 55 or over with weight loss together with upper abdominal "
     "pain, reflux or dyspepsia."),
    ("lower GI fastpath", "a faecal immunochemical test (FIT) result of 10 ug Hb/g or more at any age; or age 40 or "
     "over with unexplained weight loss and abdominal pain; or age 50 or over with unexplained rectal bleeding; or "
     "age 60 or over with iron-deficiency anaemia."),
    ("lung fastpath", "a chest X-ray suggestive of lung cancer; or age 40 or over with unexplained haemoptysis."),
    ("breast fastpath", "age 30 or over with an unexplained breast lump, with or without pain; or age 50 or over with "
     "nipple discharge, retraction or other concerning change in one nipple only."),
    ("routine referral", "none of the fastpath criteria is met."),
]

# ====================================================================== Brookhaven nurse line, child fever
PHONE = [
    ("call emergency services now", "the child is unresponsive or very hard to wake, has blue or grey lips, is "
     "struggling to breathe (grunting, pauses in breathing, severe chest indrawing), or has a seizure lasting more "
     "than 5 minutes."),
    ("go to the emergency department now", "the first disposition does not apply, and any of: age under 3 months with "
     "temperature 38.0 C or more; age 3 to under 6 months with temperature 39.0 C or more; a rash that does not fade "
     "under pressure; signs of dehydration (no wet nappy or urine for 12 hours or more, or a dry mouth with no tears "
     "when crying); stiff neck or bulging fontanelle; or a first-ever seizure with fever that has now stopped."),
    ("see a doctor within 4 hours", "neither disposition above applies, and any of: fever on day 5 or later (the day "
     "the fever began is day 1); fever with ear pain in a child under 2; fever in a child with a condition or "
     "treatment that weakens immunity; or the carer feels the child is getting worse despite fever medicine."),
    ("see a doctor within 24 hours", "none of the dispositions above applies, and any of: fever on day 3 or 4; pain "
     "or burning when passing urine; or fever that has come back after being gone for more than 24 hours."),
    ("home care", "none of the dispositions above applies."),
]
