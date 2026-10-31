"""Trial eligibility items: HALCYON-HF, GLYDE-3, ARBOR-RA, LUMEN-TRD, PIPIT-RSV, KIDNEX."""
from common import (Y, C, T, card, crit, NONE, HALCYON, HALCYON_NONE, GLYDE, GLYDE_NONE, ARBOR, ARBOR_NONE,
                    LUMEN, LUMEN_NONE, PIPIT, PIPIT_NONE, KIDNEX, KIDNEX_NONE)

H_OPTS, H_CARD = crit(HALCYON, HALCYON_NONE)
G_OPTS, G_CARD = crit(GLYDE, GLYDE_NONE)
A_OPTS, A_CARD = crit(ARBOR, ARBOR_NONE)
L_OPTS, L_CARD = crit(LUMEN, LUMEN_NONE)
P_OPTS, P_CARD = crit(PIPIT, PIPIT_NONE)
K_OPTS, K_CARD = crit(KIDNEX, KIDNEX_NONE)

ITEMS = [
# ------------------------------------------------------------------ HALCYON-HF
# H1: AF on ECG, no HF admission -> threshold 900; NT-proBNP 780 -> I4 fails -> not eligible.
# Twin: HF admission May 2025 (within 12 months) -> AF threshold 600 -> 780 meets -> eligible.
Y("On these findings, does Mr Oyelowo-Finch meet all of the HALCYON-HF entry criteria?",
"""HALCYON-HF - screening visit summary
Site 14 (Carrowmore Heart Centre) | Screening date: 10 September 2025
Participant: Mr Barnaby Oyelowo-Finch, 68, male

Diagnosis: heart failure with reduced ejection fraction due to ischaemic cardiomyopathy. NYHA class II (breathless on two flights of stairs).
Imaging: echocardiogram 8 July 2025, LVEF 32%, moderate functional mitral regurgitation.
ECG today: atrial fibrillation, ventricular rate 84/min (persistent AF since 2023).
NT-proBNP today: 780 pg/mL.

Medication: bisoprolol 10 mg daily (unchanged since 2024); sacubitril/valsartan 97/103 mg twice daily (unchanged since March 2025); apixaban 5 mg twice daily; atorvastatin 80 mg. An SGLT2 inhibitor has deliberately not been started, pending the trial discussion.

Hospital use in the past year: none for heart failure; one ED attendance in May 2025 with palpitations, discharged the same day after rate control.

Labs today: eGFR 48 mL/min/1.73 m2; potassium 4.6 mmol/L.
Seated BP: 118/72 and 114/70 mmHg.
Other history: no diabetes; PCI to the LAD in 2019, no coronary events since; no stroke or TIA; no device or transplant plans.

Investigator comment: "Keen participant, fully informed, good candidate on paper."
""",
0, 2, card(HALCYON),
twin=T([("none for heart failure; one ED attendance in May 2025 with palpitations, discharged the same day after rate control.",
         "one heart-failure admission, four nights on the cardiology ward in May 2025 for decompensation treated with IV diuretics.")], 1)),

# H2: most recent LV assessment (cMRI July 2025) LVEF 43% -> I3 fails. PCI 98 d before (ok), K 5.5 (not above), T2D.
C("Taking the HALCYON-HF criteria in the order listed, which is the first one Mrs Nakamura-Pryce does not meet?",
"""HALCYON-HF pre-screening log - entry 0212
Screening date: 15 October 2025
Participant: Mrs Aurelia Nakamura-Pryce, 72, female

Problem list (GP record): heart failure with reduced EF (EF 30%); type 2 diabetes; osteoarthritis; ischaemic heart disease.

Cardiac imaging
- Transthoracic echo, 2 August 2024: LVEF 30%, global hypokinesis.
- Cardiac MRI, 20 July 2025: LVEF 43%, no late gadolinium enhancement suggesting new infarct. Performed after 9 months of optimised medical therapy.

Coronary history: PCI with drug-eluting stent to the LAD on 9 July 2025 for stable angina.

Symptoms: NYHA class II.
NT-proBNP at screening: 1,450 pg/mL; ECG sinus rhythm, 68/min.

Medication: carvedilol 25 mg twice daily and ramipril 10 mg daily (both unchanged since 2024); metformin 1 g twice daily; clopidogrel; atorvastatin. Empagliflozin was stopped in January 2025 after recurrent genital infections.

Screening labs: eGFR 41 mL/min/1.73 m2; potassium 5.5 mmol/L.
Seated BP: 122/70 and 118/68 mmHg.
No history of type 1 diabetes, LVAD or transplant listing.

Coordinator note: "EF 30% on the problem list, so imaging criterion should be fine. Potassium borderline - check."
""",
H_OPTS, "I3 ejection fraction", 2, H_CARD),

# H3: seated readings 98 and 90 -> mean 94 < 95 -> E3 applies. Standing 86 is irrelevant; home diary irrelevant.
# Twin: second reading 93 -> mean 95.5 -> E3 does not apply.
Y("Does exclusion criterion E3 apply to this participant?",
"""HALCYON-HF screening vitals - Subject 0147
Date: 3 June 2025 | Recorded by: RN Delphine Ashworth

Seated after 5 minutes' rest, left arm, validated automated cuff:
- Reading 1 (09:12): 98/62 mmHg, HR 71
- Reading 2 (09:15): 90/58 mmHg, HR 70

Standing at 1 minute (orthostatic check requested by PI): 86/54 mmHg, HR 82. Mild light-headedness, resolved on sitting.

Home BP diary, last 7 mornings: 104/66, 101/64, 99/60, 106/68, 102/65, 97/61, 100/63.

Medication: sacubitril/valsartan 49/51 mg twice daily, bisoprolol 2.5 mg daily, spironolactone 25 mg daily. All morning medication taken at 07:00 today.

Nurse comment: "Patient says her BP always runs about 100 at home and she feels well. PI asked me to document the orthostatic drop; no treatment given."
""",
1, 2, card(HALCYON),
twin=T([("90/58 mmHg, HR 70", "93/58 mmHg, HR 70")], 0)),

# H4: sotagliflozin stopped 2 Aug, screening 13 Sep -> 42 d < 56 -> E1. PCI 14 Jun -> 91 d (> 84 ok).
# Twin: stopped 12 Jul -> 63 d -> none of these.
C("Which HALCYON-HF criterion, taken in listed order, is the first one that rules this patient out, if any?",
"""Medication reconciliation for HALCYON-HF screening
Visit date: 13 September 2025 | Pharmacist: Oyin Castellanos
Participant: Mr Teodor Villiers-Mahlangu, 61, male

Current medicines
- Carvedilol 25 mg twice daily (since 2023)
- Losartan 100 mg daily (dose unchanged since January 2025)
- Furosemide 40 mg daily; atorvastatin 80 mg; clopidogrel 75 mg; metformin 1 g twice daily

Recently stopped
- Sotagliflozin 200 mg daily - taken as part of a diabetes study; last dose 2 August 2025 when that study closed.
- Empagliflozin 10 mg - 2022 to 2023, switched when he joined the diabetes study.

Cardiac events: NSTEMI January 2025; PCI to the right coronary artery 14 June 2025.

Screening results today: NYHA class III; echocardiogram 30 August 2025, LVEF 29%; NT-proBNP 2,310 pg/mL with sinus rhythm; eGFR 38 mL/min/1.73 m2; potassium 5.3 mmol/L; seated BP 126/74 and 122/76 mmHg.
Type 2 diabetes (HbA1c 7.4%). No transplant or LVAD plans.

Pharmacist comment: "Sotagliflozin is technically a dual SGLT1/2 inhibitor, which is why the diabetes study used it. Recent PCI noted."
""",
H_OPTS, "E1 SGLT2 inhibitor", 2, H_CARD,
twin=T([("last dose 2 August 2025", "last dose 12 July 2025")], NONE)),

# H5: beta-blocker intolerance documented (bronchospasm) -> exempt; ARNI dose last changed 28 Jul, screening 8 Sep
# -> 42 d stable -> I5 met.
Y("Does Ms Anand-Whitlock satisfy inclusion criterion I5?",
"""Electronic record extract - prepared for HALCYON-HF screening visit on 8 September 2025
Patient: Ms Cordelia Anand-Whitlock, 57

Allergies and intolerances
- Bisoprolol: severe bronchospasm requiring nebulisers (March 2023). Recorded by respiratory team: "avoid all beta-blockers - severe eosinophilic asthma".
- Penicillin: rash.

Current medication
- Sacubitril/valsartan 49/51 mg twice daily (dose last changed 28 July 2025, up-titrated from 24/26 mg)
- Spironolactone 25 mg daily
- Furosemide 40 mg daily
- Budesonide/formoterol inhaler, montelukast

Cardiology letter, 14 August 2025: "Heart failure with LVEF 31%, NYHA II. She is not on a beta-blocker, which is suboptimal, but this is not possible given her asthma history. We discussed ivabradine and will review after the trial screening."

Screening bloods (8 September): NT-proBNP 1,120 pg/mL, sinus rhythm; eGFR 62; potassium 4.8.
""",
1, 2, card(HALCYON)),

# H6: TIA 11 Sep 2025, screening 20 Nov 2025 -> 70 d < 84 -> E4. T2D on insulin (not T1D), K 5.4, eGFR 26.
C("Checking the HALCYON-HF criteria in their listed order, which criterion first excludes Mr Farrow-Ekwueme?",
"""HALCYON-HF - telephone pre-screen, then clinic screening visit
Coordinator: Ines Waterhouse-Obi

Participant: Mr Gideon Farrow-Ekwueme, 66, male
Screening visit: 20 November 2025

Heart failure: dilated cardiomyopathy, NYHA class III. Echocardiogram 2 October 2025: LVEF 25%. NT-proBNP at screening 3,100 pg/mL, sinus rhythm.

Medication: bisoprolol 7.5 mg and candesartan 16 mg daily, both unchanged since April 2025; furosemide; insulin glargine 30 units nightly plus metformin for type 2 diabetes (diagnosed age 52, insulin added 2021). Dapagliflozin stopped 30 June 2025 because of recurrent urinary infections.

Neurology: attended the rapid-access stroke clinic after 40 minutes of left arm weakness on 11 September 2025 that resolved completely; MRI showed no infarct; diagnosis recorded as transient ischaemic attack; started on clopidogrel.

Screening labs: eGFR 26 mL/min/1.73 m2; potassium 5.4 mmol/L.
Seated BP: 104/66 and 100/64 mmHg.
No LVAD or transplant referral.

Coordinator note: "Kidney function and potassium both close to the limits; insulin-treated diabetes - check with PI."
""",
H_OPTS, "E4 recent event", 2, H_CARD),

# ------------------------------------------------------------------ GLYDE-3
# G1: HbA1c 95 mmol/mol = 10.8% > 10.5% -> I3. Cousin with MTC (not first-degree), lipase blip without diagnosis.
# Twin: 88 mmol/mol (10.2%) -> none of these.
C("Screening criteria are checked in their listed order. Which is the first GLYDE-3 criterion this participant fails?",
"""GLYDE-3 screening file - Participant 031-0077
Screening date: 3 March 2025

Participant: Ms Rukmini Halloran-Osei, 59, female
Type 2 diabetes diagnosed 2016.

Central laboratory (screening): HbA1c 95 mmol/mol (the central lab reports IFCC units only). eGFR 71 mL/min/1.73 m2.
Anthropometrics: height 162.5 cm, weight 88.2 kg (BMI 33.4 kg/m2). Weight at the diabetes clinic 60 days earlier: 88.9 kg.

Diabetes medication: metformin 1000 mg daily since 2021. Clinic letter from 2020 documents persistent diarrhoea at 2000 mg/day, resolved on dose reduction. Gliclazide 80 mg twice daily. She declined semaglutide when it was offered in 2023 and has never taken any injectable diabetes drug.

Family history: her cousin (her mother's sister's son) had medullary thyroid carcinoma diagnosed at 34. Parents and siblings unaffected; no children.

Other history: attended ED with norovirus in 2022; lipase 1.6 x ULN on that occasion; CT abdomen normal; no diagnosis of pancreatitis was made. No bariatric surgery. Hypertension.

Coordinator note: "Family MTC history and the lipase need PI review."
""",
G_OPTS, "I3 HbA1c", 2, G_CARD,
twin=T([("HbA1c 95 mmol/mol", "HbA1c 88 mmol/mol")], NONE)),

# G2: 5 ft 9 in = 175.26 cm; 182 lb = 82.56 kg -> BMI 26.88 -> 26.9 < 27.0 -> I4 not met.
# Twin 186 lb = 84.37 kg -> 27.47 -> 27.5 -> I4 met.
Y("Does this participant meet GLYDE-3 inclusion criterion I4?",
"""Brookline Clinical Research - GLYDE-3 screening intake form (US site)

Participant ID: 118-0024 | Screening visit: 22 May 2025
Name: Dashiell Okafor-Lindgren | Age: 47 | Sex: male

Vital signs (measured by research staff, shoes off):
- Height: 5 ft 9 in
- Weight: 182 lb
- BP: 132/84 mmHg; pulse 76

Participant-reported: "My BMI was 28 on the pharmacy kiosk last month."

Diabetes history: type 2 diabetes since 2018. Metformin ER 2000 mg daily (unchanged for 3 years). HbA1c at screening 8.1%.
No GLP-1 or GIP/GLP-1 medicine ever. No pancreatitis. No personal or family history of thyroid cancer or MEN2. eGFR 94. No bariatric surgery. Weight at primary care 6 weeks ago: 183 lb.

Staff note: "Participant is keen; his employer's wellness programme told him he qualifies as overweight."
""",
0, 3, card(GLYDE),
twin=T([("- Weight: 182 lb", "- Weight: 186 lb")], 1)),

# G3: weights in 90-day window: 14 Mar (88 d before 10 Jun) 88.0 kg; screening 83.2 -> 5.45% > 5% -> E6 applies.
# 16 Feb weight is outside the window.
Y("Does exclusion criterion E6 apply to this GLYDE-3 participant?",
"""GLYDE-3 - weight history review
Participant 031-0102 | Screening date: 10 June 2025

Recorded weights (clinic scales, light clothing):
- 16 February 2025 (dietitian): 90.1 kg
- 14 March 2025 (diabetes clinic): 88.0 kg
- 22 April 2025 (practice nurse): 86.1 kg
- 10 June 2025 (screening, study scales): 83.2 kg

Participant comment at screening: "My weight has basically been steady - I'm down about three kilos since spring, that's all, just from cutting out the late-night snacks."

Other screening results: HbA1c 8.4%; BMI 29.6 kg/m2; metformin 2000 mg daily for 4 years; no GLP-1 medicines ever; eGFR 77; no pancreatitis, thyroid cancer or bariatric history.

Coordinator note: "Change since April is only about 3%. Happy to proceed?"
""",
1, 2, card(GLYDE)),

# G4: band removed 2 May 2023, screening 19 Aug 2024 -> > 12 months -> exception applies -> E5 does not exclude.
Y("Would exclusion criterion E5 keep this participant out of GLYDE-3?",
"""Forum: GLYDE-3 Site Coordinators (internal study message board)
Thread: Bariatric history - does this count?

Posted by: m.renwick (Site 22) - 19 August 2024

Hi all, screening a lovely 51-year-old woman today and want a sanity check before I screen-fail her.

Her history:
- Laparoscopic adjustable gastric band placed in 2016 at a private clinic.
- Band slipped in early 2023 with reflux and vomiting; band removed on 2 May 2023. Letter from the surgeon confirms full removal, no other procedure performed.
- A sleeve gastrectomy was discussed at that time but she declined, and nothing further was done.
- Since then she has regained weight: BMI 36.8 today.

Everything else looks fine: type 2 diabetes since 2019, HbA1c 8.7%, metformin 1500 mg daily for over a year, no GLP-1 drugs ever, eGFR 90, weight stable over the last 3 months.

My gut says any bariatric surgery = excluded. Does anyone read E5 differently?

Reply from: j.adeyinka (Site 09): "We had a similar one last month, following."
""",
0, 2, card(GLYDE)),

# G5: compounded tirzepatide last 2 Mar 2025, screening 29 Jul 2025 -> 149 d < 180 -> E1.
C("Which GLYDE-3 criterion, reviewed in the order listed, is the first that this participant does not satisfy?",
"""GLYDE-3 screening - Participant 044-0019
Screening visit: 29 July 2025

Mrs Amaryllis Pereira-Voss, 52, female. Type 2 diabetes diagnosed 2019.

Screening results: HbA1c 8.2% (66 mmol/mol); height 165 cm; weight 86.9 kg (BMI 31.9); eGFR 88 mL/min/1.73 m2.

Weight history: 84.4 kg on 2 May 2025 at her GP (regained after stopping weight-loss injections).

Medication history (from participant interview and pharmacy records):
- Metformin 1000 mg daily since 2020; GP letter records abdominal cramps and diarrhoea at 1500 mg.
- Weekly injections of compounded tirzepatide bought through an online telehealth service from November 2024; last injection 2 March 2025, when the service stopped trading. Not on her GP record.
- Empagliflozin 10 mg daily.

Other history: lipase 2.1 x ULN during gastroenteritis in 2023, with a normal CT pancreas; the discharge letter says "no evidence of pancreatitis". No thyroid cancer in the family. No surgery apart from a caesarean section.

Coordinator note: "The injections weren't prescribed by a doctor, so I don't think they count."
""",
G_OPTS, "E1 incretin therapy", 2, G_CARD),

# G6: T2D diagnosed 20 Feb 2025, screening 15 Jul 2025 -> 145 d < 180 -> I2 (prediabetes since 2019 doesn't count).
C("In the listed order of the GLYDE-3 criteria, which one does Mr Brandvold fail first?",
"""Referral to GLYDE-3 from Harbourside Family Practice
Date of screening visit: 15 July 2025

Patient: Mr Cassius Brandvold, 44, male

"I am referring this gentleman, who has struggled with glucose control for years. He had prediabetes on routine testing in 2019 (HbA1c 6.1%) and was given lifestyle advice. HbA1c crept up over the following years and type 2 diabetes was formally diagnosed on 20 February 2025 when his HbA1c was 8.9%. He started metformin 500 mg that day, titrated to 2000 mg daily by 1 April 2025, and has taken that dose ever since. He is motivated and would like to try a trial medicine."

Screening results (study site): HbA1c 7.6%; height 180 cm, weight 110.8 kg (BMI 34.2); eGFR 97.

History: no GLP-1 or GIP/GLP-1 medicines ever; no pancreatitis; no personal or family history of thyroid cancer; no bariatric surgery. Weight 111.5 kg at the practice in May.

Coordinator note: "Diabetic range glucose for 6 years really, so duration is fine."
""",
G_OPTS, "I2 diabetes duration", 1, G_CARD),

# ------------------------------------------------------------------ ARBOR-RA
# R1: MTX 12.5 mg/week by preference, no intolerance -> I4 fails. CRP 8 mg/L but ESR 31 -> I3 ok.
# Adalimumab stopped for injection-site reactions (allowed). Twin: intolerance documented -> none of these.
C("Following the ARBOR-RA criteria in order, which is the first one Ms Nwachukwu-Hale fails?",
"""ARBOR-RA - screening summary (Site 03, Westerleigh Rheumatology)
Participant: Ms Philippa Nwachukwu-Hale, 52, female
Screening: 16 September 2025 | Planned baseline: 14 October 2025

Diagnosis: seropositive rheumatoid arthritis (RF and anti-CCP positive), meets 2010 ACR/EULAR criteria; diagnosed 2021.

Disease activity at screening: 9 swollen joints (66-count), 12 tender joints (68-count); CRP 0.8 mg/dL; ESR 31 mm/h.

Methotrexate: started 2022, 20 mg/week subcutaneously until March 2025, reduced to 12.5 mg/week in March 2025 at the patient's request because she prefers a lower dose; no side effects reported. Dose unchanged since.

Prior advanced therapy: adalimumab January-August 2023, stopped because of repeated injection-site reactions; disease had been improving on it.

Other: prednisolone 5 mg daily, unchanged for 3 months. Recombinant zoster vaccine (second dose) given 2 September 2025. IGRA negative. HBsAg negative, anti-HBc negative.
""",
A_OPTS, "I4 methotrexate", 2, A_CARD,
twin=T([("at the patient's request because she prefers a lower dose; no side effects reported",
         "after persistent nausea and an ALT rise to 3 x ULN at 20 mg/week, both documented by her rheumatologist")],
       NONE)),

# R2: anti-HBc positive, HBsAg negative, HBV DNA not detected -> E4 does not apply. Twin: DNA detected -> applies.
Y("Does exclusion criterion E4 exclude this patient from ARBOR-RA?",
"""Westerleigh Pathology - Hepatitis B screen
Requested by: ARBOR-RA study team | Participant 03-0041 (female, 47)
Collected: 2 September 2025

Hepatitis B surface antigen (HBsAg): NOT DETECTED
Hepatitis B surface antibody (anti-HBs): 84 mIU/mL
Hepatitis B core antibody, total (anti-HBc): DETECTED
HBV DNA (PCR, lower limit of quantification 10 IU/mL): target not detected

Laboratory comment: "Serology pattern consistent with resolved past hepatitis B infection. Risk of reactivation with immunosuppressive or biologic therapy; consider monitoring HBV DNA every 3 months or antiviral prophylaxis per local guidance."

Study coordinator note: "Core antibody positive - that's hepatitis B, so we'll have to screen-fail her? The rheumatologist says she was jaundiced as a teenager while living abroad but has had normal liver tests ever since. ALT today 21 U/L."
""",
0, 2, card(ARBOR),
twin=T([("target not detected", "detected, 38 IU/mL")], 1)),

# R3: SJC 7 but TJC 5 < 6 -> I3 fails -> not eligible despite high DAS28.
Y("Is this patient eligible to be randomised in ARBOR-RA?",
"""ARBOR-RA - joint assessment and screening checklist
Participant 07-0113, male, 58 | Screening: 4 November 2025 | Baseline planned: 2 December 2025

Joint assessor (blinded): Dr Maelle Fitzgerald-Okoro
- Swollen joint count (66): 7 - bilateral MCP 2 and 3, right wrist, left PIP 3, right knee
- Tender joint count (68): 5 - bilateral MCP 2, right wrist, right knee, left ankle
- Patient global: 72/100; HAQ-DI 1.6
- DAS28-CRP: 5.4 (high disease activity)

Labs: CRP 31 mg/L; ESR 46 mm/h. RF positive; anti-CCP strongly positive. RA diagnosed 2019 (meets 2010 ACR/EULAR criteria).

Treatment: methotrexate 20 mg/week orally since 2020, unchanged; folic acid. No previous biologic or JAK inhibitor. No oral steroids.
Screening: IGRA negative; HBsAg and anti-HBc negative. Vaccines: inactivated influenza vaccine 20 October 2025.

Investigator comment: "Clearly active, erosive disease - exactly the population we want."
""",
0, 2, card(ARBOR)),

# R4: one prior biologic (etanercept) stopped for loss of efficacy -> E1. IGRA+ with 6 weeks prophylaxis (ok).
C("Reviewing the ARBOR-RA criteria in order, which criterion first rules this patient out?",
"""Referral letter - Dr Anwen Castellanos, Consultant Rheumatologist, to the ARBOR-RA team
Date: 6 October 2025

Re: Mrs Soraya Lindqvist-Obi, 61

I would be grateful if you would consider Mrs Lindqvist-Obi for ARBOR-RA. She has seropositive rheumatoid arthritis diagnosed in 2014 and currently has 10 swollen and 14 tender joints with a CRP of 24 mg/L. She has taken methotrexate 20 mg weekly since 2015.

She had one previous biologic: etanercept from 2019 to 2023. She did very well initially, but over 2022 her disease flared again despite regular injections that she never missed, and by early 2023 we agreed it was no longer working and stopped it. She has had no other biologic or targeted therapy since and has never taken a JAK inhibitor.

Her interferon-gamma release assay at your screening visit was positive, although her chest X-ray is clear and she has no symptoms. She started isoniazid on 1 September 2025 and will continue it for 9 months; baseline is planned for 20 October 2025.

She takes prednisolone 7.5 mg daily, unchanged since spring. Hepatitis B serology is negative. Her only recent vaccine was inactivated influenza.

Kind regards,
Anwen Castellanos
""",
A_OPTS, "E1 prior advanced therapy", 2, A_CARD),

# R5: yellow fever vaccine 1 Mar 2025, baseline 8 Apr 2025 -> 38 d < 42 -> E5 applies. Injectable typhoid Vi is not live.
Y("Is Mr Hallorann-Diaz excluded from ARBOR-RA by criterion E5?",
"""Travel clinic record (copied to ARBOR-RA site file)
Patient: Mr Tomasz Hallorann-Diaz, 44 | ARBOR-RA baseline visit booked: 8 April 2025

Visit date: 1 March 2025 - pre-travel consultation (trip to Ghana, cancelled later because of his arthritis flare)

Vaccines administered today:
- Yellow fever vaccine, 0.5 mL subcutaneous, left arm
- Typhoid Vi polysaccharide vaccine (injectable), 0.5 mL intramuscular, right arm
- Hepatitis A (inactivated), 1 mL intramuscular

Not given: oral typhoid capsules (patient preferred the injection).

Advice: malaria prophylaxis prescription issued, never collected.

Study coordinator note (7 April 2025): "Reviewed with patient. He hasn't had any vaccine since the travel clinic more than a month ago. The typhoid he had was the injection, not the oral one, so no live typhoid vaccine."
""",
1, 1, card(ARBOR)),

# ------------------------------------------------------------------ LUMEN-TRD
# D1: adequate trials: sertraline 100 mg 8 wk (yes); escitalopram 5 mg (dose too low); venlafaxine 150 mg 4 wk
# (too short); bupropion 150 mg (dose too low) -> 1 adequate -> I4 fails. Twin venlafaxine 7 wk -> 2 -> none.
C("Going through the LUMEN-TRD criteria in their listed order, which is the first one this participant fails?",
"""LUMEN-TRD - antidepressant treatment history form
Participant: Mr Evander Quist-Adebayo, 38 | Screening: 12 May 2025 | Baseline: 26 May 2025

Current major depressive episode began January 2024 (no psychotic features). Previous episode 2016, fully remitted.

Antidepressant trials in the current episode (pharmacy-verified):
1. Sertraline 100 mg/day, 3 February - 30 March 2024 (8 weeks). Minimal improvement.
2. Escitalopram 5 mg/day, 6 April - 15 June 2024 (10 weeks). Not increased because of nausea at start. No improvement.
3. Venlafaxine XR 150 mg/day (reached after a 2-week titration) for 4 weeks at that dose, August - September 2024; stopped because of night sweats.
4. Bupropion XL 150 mg/day, October 2024 - March 2025. No improvement.

MADRS: 33 at screening, 31 at baseline.
C-SSRS: passive wish to be dead (item 1) in the past month; no active ideation, no attempts ever.
No history of mania, hypomania or psychosis. Alcohol: 4-6 units/week; no drug use. No ECT or MAOI ever; never took fluoxetine.

Rater comment: "Four antidepressants in this episode - clearly treatment-resistant."
""",
L_OPTS, "I4 treatment resistance", 3, L_CARD,
twin=T([("for 4 weeks at that dose", "for 7 weeks at that dose")], NONE)),

# D2: MADRS 38 -> 28: baseline >= 28 but improvement 26.3% > 25% -> I3 fails -> cannot randomise.
Y("Can this participant be randomised into LUMEN-TRD at the baseline visit?",
"""LUMEN-TRD - baseline visit worksheet
Participant 05-0231, female, 45 | Baseline date: 18 August 2025

Central rater MADRS scores
- Screening (4 August 2025): 38
- Baseline (18 August 2025): 28

Rater note: "Participant reports a slightly better fortnight after a family visit; still severely depressed on interview, sleep poor, appetite reduced, marked anhedonia."

Other criteria (all confirmed by the site PI on the checklist):
- Current episode since June 2024, no psychotic features.
- Adequate antidepressant trials in this episode: escitalopram 20 mg (10 weeks) and duloxetine 60 mg (8 weeks), both without response.
- No bipolar or psychotic disorder. C-SSRS: no active ideation or attempts ever.
- No substance use disorder. No ECT. Last duloxetine dose 20 July 2025; never took an MAOI or fluoxetine.

Coordinator note: "Baseline MADRS is exactly 28, which meets the cut-off. Pharmacy is ready to dispense."
""",
0, 2, card(LUMEN)),

# D3: C-SSRS items 1-2 only (no intent/plan); attempt 3 Apr 2024, screening 10 Jun 2025 -> 14 months -> E2 no.
Y("Does exclusion criterion E2 apply to this LUMEN-TRD participant?",
"""LUMEN-TRD - C-SSRS (baseline/screening version) summary
Participant 02-0058, male, 31 | Screening date: 10 June 2025
Rater: Dr Solveig Amankwah

Suicidal ideation (past 6 months)
1. Wish to be dead: YES - "some days I wish I just wouldn't wake up".
2. Non-specific active suicidal thoughts: YES - occasional thoughts of killing himself, fleeting.
3. Active ideation with any methods (no plan), without intent: NO
4. Active ideation with some intent to act, without specific plan: NO
5. Active ideation with specific plan and intent: NO

Suicidal behaviour (lifetime)
- Actual attempt: YES - one, an overdose of paracetamol on 3 April 2024, admitted overnight for treatment. No attempts before or since.
- Interrupted or aborted attempts: none. Preparatory acts: none.

Rater comment: "Ideation present but no intent or plan. Past attempt noted. Safety plan reviewed and updated today; participant engaged with community mental health team."
""",
0, 2, card(LUMEN)),

# D4: fluoxetine last dose 2 May 2025, baseline 30 May 2025 -> 28 d < 35 -> E4.
C("If the LUMEN-TRD criteria are checked in their listed order, which criterion first prevents this participant from being randomised on the planned date?",
"""LUMEN-TRD - site PI eligibility email

From: Dr Rafferty Oduya
To: LUMEN-TRD medical monitor
Date: 21 May 2025
Subject: Participant 04-0077 - please confirm before baseline

Dear medical monitor,

Participant 04-0077 (Ms Linnea Ferreira-Holt, 29) is booked for baseline on 30 May 2025. Summary:

- Current depressive episode since March 2024, no psychotic features; MADRS 35 at screening, 33 at our dry-run rating last week.
- Antidepressant trials in this episode: citalopram 20 mg for 10 weeks (2024), then fluoxetine 40 mg from September 2024 until her last dose on 2 May 2025 - both without response. We stopped fluoxetine so she could take part.
- We considered phenelzine in April but it was never prescribed or started.
- No bipolar or psychotic history; C-SSRS negative apart from a passive wish to be dead; no substance use disorder; never had ECT.

I think she is a straightforward case. Can you confirm we are good to go on the 30th?

Best wishes,
Rafferty
""",
L_OPTS, "E4 washout", 2, L_CARD),

# ------------------------------------------------------------------ PIPIT-RSV
# DOB 10 Mar 2025 -> day 42 = 21 Apr. Fever 20 Apr -> excluded on 20-23 Apr -> earliest 24 Apr.
# Maternal RSV vaccine 9 days before birth (< 14) -> not E1. Twin fever 17 Apr -> earliest 21 Apr.
C("Which is the earliest of these dates on which the infant can receive the PIPIT-RSV vaccination?",
"""PIPIT-RSV study - scheduling note
Site: Merrow Children's Research Unit | Nurse: Alba Jankowski-Reyes

Infant: Baby Theo Mwangi-Carlsson
Date of birth: 10 March 2025
Gestation at birth: 37 weeks 2 days | Birth weight: 3.10 kg
Mother received an RSV vaccine in pregnancy at 36 weeks 0 days.
No RSV monoclonal antibody given to the infant. No blood products. No known immunodeficiency in the infant or household.

Parent phone call this morning, 08:30, before the clinic opened: "Theo had a temperature of 38.2 C (rectal) on the evening of 20 April. It settled without any medicine, his temperature has been normal since, and he is feeding well - just a snuffly nose."

The clinic can offer vaccination appointments on 21, 22, 23, 24 or 25 April 2025. Please book the first date on which he is allowed to be vaccinated under the protocol.
""",
["21 April 2025", "22 April 2025", "23 April 2025", "24 April 2025", "25 April 2025"], "24 April 2025", 3,
card([("21 April 2025", "vaccinate on 21 April 2025."), ("22 April 2025", "vaccinate on 22 April 2025."),
      ("23 April 2025", "vaccinate on 23 April 2025."), ("24 April 2025", "vaccinate on 24 April 2025."),
      ("25 April 2025", "vaccinate on 25 April 2025.")]),
twin=T([("on the evening of 20 April", "on the evening of 17 April")], "21 April 2025")),

# V_2: maternal vaccine at 34w3d, birth at 37w2d -> 20 days >= 14 -> E1 applies (excluded).
Y("Is this infant excluded from PIPIT-RSV under criterion E1?",
"""Maternity discharge summary (excerpt) - Harrowgate General Hospital
Baby: Girl, Ada Oyelaran-Petit | Born: 2 May 2025 at 37 weeks 2 days by spontaneous vaginal delivery | Birth weight 3.42 kg

Antenatal notes (mother): booked at 11 weeks; RSV prefusion F vaccine given at the antenatal clinic at 34 weeks 3 days; Tdap at 28 weeks; influenza vaccine at 30 weeks. Group B strep negative.

Neonatal course: vitamin K intramuscular at birth; hepatitis B vaccine not required (mother HBsAg negative). Routine newborn examination normal. Discharged day 2 on breast feeds.

PIPIT-RSV screening note (research nurse, 20 June 2025): "Baby Ada has not had nirsevimab, palivizumab or any other RSV antibody - parents confirm and the child health record agrees. No blood products or immunoglobulin. Well, no fever this week. Age today 49 days."
""",
1, 2, card(PIPIT)),

# V_3: gestation 35w6d < 36w0d -> I2 fails. Birth weight 2.62 kg ok. Vitamin K and hepatitis B vaccine are not blood products.
C("Checking the PIPIT-RSV criteria in the order listed, which criterion does this infant fail first?",
"""PIPIT-RSV screening checklist - Infant 12-044
Screening and planned vaccination date: 16 July 2025

Date of birth: 27 May 2025 (age today 50 days)
Gestational age at birth: 35 weeks 6 days (dating scan at 12 weeks)
Birth weight: 2.62 kg
Neonatal course: 3 days on the postnatal ward for jaundice monitoring, no phototherapy needed. Vitamin K at birth; hepatitis B vaccine at birth (mother's hepatitis B status unknown at delivery, later confirmed negative; no hepatitis B immunoglobulin given).

RSV protection: none - no maternal RSV vaccine; no nirsevimab or palivizumab.
Temperature log (parent): no fever in the past week. Temperature today 36.9 C.
Household: parents and one sibling (4 years), all well; no immunodeficiency.

Parent comment: "The midwife told us he was basically term, he just came a few days early."
""",
P_OPTS, "I2 gestation", 2, P_CARD),

# ------------------------------------------------------------------ KIDNEX
# K1: UACR 21 mg/mmol x 8.84 = 185.6 mg/g < 200 -> I3 not met. Twin 23 -> 203.3 -> met.
Y("Does the participant meet KIDNEX inclusion criterion I3 on the screening sample?",
"""Pellbridge Renal Unit - KIDNEX screening results
Participant: KX-0419 (male, 63) | Sample date: 5 August 2025

Urine (first morning void)
- Albumin: 168 mg/L
- Creatinine: 8.0 mmol/L
- Albumin:creatinine ratio: 21 mg/mmol (laboratory reference: normal below 3 mg/mmol; "A3 severely increased" above 30 mg/mmol)

Blood
- Creatinine 162 umol/L; eGFR (CKD-EPI 2021) 39 mL/min/1.73 m2
- Potassium 4.7 mmol/L

Background: type 2 diabetes for 14 years; diabetic kidney disease. Ramipril 10 mg daily for 2 years. No steroids or immunosuppressants.

Research nurse note: "UACR well above normal range - moderately increased albuminuria, lab flags it as A2. Uploading to the sponsor portal; the portal converts to mg/g automatically."
""",
0, 3, card(KIDNEX),
twin=T([("ratio: 21 mg/mmol", "ratio: 23 mg/mmol")], 1)),

# K2: lisinopril + losartan (both) -> I4 fails. UACR 60 mg/mmol = 530 mg/g ok; K 5.0 not above 5.0.
C("In the listed order of the KIDNEX criteria, which is the first criterion this participant does not meet?",
"""KIDNEX - screening visit note
Participant: KX-0233, female, 58 | Screening: 30 June 2025

Diagnosis: chronic kidney disease secondary to hypertensive nephrosclerosis; no diabetes.
Screening labs: eGFR 34 mL/min/1.73 m2; UACR 60 mg/mmol; potassium 5.0 mmol/L.

Medication (unchanged since January 2025):
- Lisinopril 40 mg daily
- Losartan 100 mg daily (added by her previous nephrologist "for extra proteinuria reduction")
- Amlodipine 10 mg; atorvastatin 20 mg; sodium bicarbonate

No dialysis or transplant planned. No immunosuppressive treatment ever. Creatinine stable over the last year (varies 1.62-1.70 mg/dL).

Investigator note: "Both RAS blockers at maximum dose, very well tolerated - she is the ideal maximally treated patient for this trial."
""",
K_OPTS, "I4 RAS blockade", 2, K_CARD),

# K3: screening 12 Jun 2025 -> window from 12 Dec 2024; prednisone 10 mg (> 7.5) from 1 Dec to 31 Dec -> E4.
# Twin: screening 12 Jul 2025 -> window from 12 Jan 2025 -> only 5 mg in window -> none of these.
C("Which KIDNEX criterion, taken in the listed order, is the first that this participant fails, if any?",
"""KIDNEX eligibility review - Participant KX-0507 (male, 49)
Screening date: 12 June 2025

Diagnosis: biopsy-proven IgA nephropathy (September 2024).

Kidney function: eGFR 52 mL/min/1.73 m2 at screening; UACR 1,480 mg/g. Creatinine stable over the past 6 months (1.58-1.66 mg/dL); no acute kidney injury.

RAS blockade: irbesartan 300 mg daily, unchanged since November 2024.

Corticosteroid course for IgA nephropathy (from the renal clinic letters):
- prednisone 40 mg daily from 1 October 2024
- reduced to 20 mg daily from 1 November 2024
- 10 mg daily from 1 December 2024
- 5 mg daily from 1 January 2025
- stopped on 1 February 2025
No other immunosuppressants (no mycophenolate, cyclophosphamide, rituximab or calcineurin inhibitor).

Other: no diabetes; potassium 4.9 mmol/L; no dialysis or transplant planned.

Coordinator note: "Steroids finished in early February, so he should be fine for the immunosuppression exclusion."
""",
K_OPTS, "E4 immunosuppression", 3, K_CARD,
twin=T([("Screening date: 12 June 2025", "Screening date: 12 July 2025")], NONE)),

# K4: creatinine 1.40 -> 1.84 mg/dL (31.4% rise) on 30 Apr 2025, 36 d before screening 5 Jun -> E5 applies.
Y("Is this participant excluded under KIDNEX criterion E5?",
"""From: Grete Oyewole, KIDNEX study coordinator
To: Dr Hamish Adeleke-Voss (PI)
Date: 5 June 2025
Subject: KX-0611 - screening today, creatinine question

Hi Hamish,

Screening went smoothly today for KX-0611 (71, female, type 2 diabetes, diabetic kidney disease). eGFR 36, UACR 820 mg/g, potassium 4.6, on losartan 100 mg daily. Nothing else of note.

One thing I wanted to flag. Her creatinine history from the GP system:
- 12 February 2025: 1.40 mg/dL
- 30 April 2025: 1.84 mg/dL - she had 3 days of diarrhoea and vomiting (gastroenteritis) and was drinking very little. The GP did not record a diagnosis of acute kidney injury and did not admit her; advised fluids and paused her losartan for 5 days.
- 20 May 2025: 1.45 mg/dL
- 5 June 2025 (screening): 1.47 mg/dL

Since it was never called AKI and it came straight back down, I assume we can go ahead with randomisation next week?

Thanks,
Grete
""",
1, 2, card(KIDNEX)),
]
