"""Benefit-eligibility items: carer payment, patient travel, prescription exemption, capability points,
hearing subsidy, antiviral access, hospice election (all schemes invented)."""
from common import (Y, C, T, card, crit, labels, NONE, CARER, CARER_NONE, RX, RX_NONE)

CA_OPTS, CA_CARD = crit(CARER, CARER_NONE)
CA_YCARD = card(CARER + [("entitlement rule", "the claimant is entitled only if all four rules are met.")])
CA_PAY = card(CARER + [
    ("entitlement rule", "the claimant is entitled only if all four rules are met."),
    ("overlapping benefit rule", "the weekly Carer Support Payment of 81.90 pounds is reduced by the amount of any "
     "State Pension the claimant receives; if the State Pension is 81.90 pounds a week or more, nothing is paid, "
     "although the claimant keeps an underlying entitlement.")])

TRAVEL_TEXT = ("Ardmore Patient Travel Scheme - summary of rules: (1) you receive Income Support, income-based "
               "Jobseeker's Allowance, Pension Credit guarantee credit, or Universal Credit with take-home earnings of "
               "435 pounds or less in your last assessment period, or you hold a valid HC2 certificate (all of these "
               "give full help), or you hold a valid HC3 certificate (partial help); (2) you were referred by a doctor "
               "or dentist for NHS-funded specialist care at a hospital or specialist clinic (GP and routine dental "
               "appointments do not count); (3) your claim is received within 3 months of the journey. Eligible "
               "costs: public transport fares, or 20p per mile plus parking if you drive. HC3 holders are repaid the "
               "amount by which the week's eligible costs exceed the weekly contribution shown on the certificate.")
TRAVEL_OUT = [
    ("full reimbursement", "all scheme conditions are met and the claimant has full help (a qualifying benefit or an "
     "HC2 certificate); all eligible costs are repaid."),
    ("partial reimbursement", "all scheme conditions are met, the claimant has only an HC3 certificate, and the week's "
     "eligible costs exceed the weekly contribution; the excess is repaid."),
    ("no reimbursement", "a scheme condition is not met, or the claimant has only an HC3 certificate and the week's "
     "eligible costs do not exceed the weekly contribution."),
]
TRAVEL_Y = card([
    ("qualifying status", "the claimant receives Income Support, income-based Jobseeker's Allowance, Pension Credit "
     "guarantee credit, or Universal Credit with take-home earnings of 435 pounds or less in the last assessment "
     "period, or holds a valid HC2 or HC3 certificate."),
    ("qualifying appointment", "the journey was to NHS-funded specialist care at a hospital or specialist clinic on "
     "referral by a doctor or dentist; GP and routine dental appointments do not count."),
    ("time limit", "the claim is received within 3 months of the date of the journey (a journey on 5 March must be "
     "claimed by 5 June)."),
    ("reimbursement rule", "costs are repaid only if all three conditions above are met."),
])

RX_OPTS, RX_CARD = crit(RX, RX_NONE)

WCS_TABLE = """Work Capability Supplement - descriptor table (points)
Activity 1, mobilising unaided by another person (walking or using a manual wheelchair): cannot move more than 50 m - 15; cannot move more than 100 m - 9; cannot move more than 200 m - 6.
Activity 2, standing and sitting: cannot move between two adjacent seats without help - 15; cannot stay at a workstation (standing, sitting or a mix) for more than 30 minutes - 9.
Activity 3, manual dexterity: cannot press a button or turn a page - 15; cannot use a pen or pencil to make a meaningful mark - 9; cannot use a keyboard or mouse - 9.
Activity 4, coping with change: cannot cope with any change - 15; cannot cope with minor planned change - 9; cannot cope with minor unplanned change - 6.
Scoring rules: a descriptor applies only if it applies on the majority of days (more than half); within each activity only the single highest-scoring descriptor that applies counts; points from different activities are added."""
WCS_OUT = [
    ("no award", "total score below 15 points."),
    ("standard rate", "total score of 15 to 24 points."),
    ("enhanced rate", "total score of 25 points or more."),
]

HEAR = card([
    ("hearing threshold", "average hearing threshold of at least 35 dB HL in the better ear, averaged over 0.5, 1, 2 "
     "and 4 kHz; the better ear is the ear with the lower average."),
    ("eligibility group", "aged 18 or over and holding a Tallis concession card."),
    ("replacement interval", "no subsidised hearing device in the previous 5 years, unless the better-ear average has "
     "worsened by 10 dB or more since that device was fitted."),
    ("subsidy rule", "a subsidised device is provided only if all three conditions are met."),
])

PAX = card([
    ("timing", "treatment must start no later than day 5 of symptoms, counting the day symptoms began as day 0."),
    ("risk group", "age 65 or over; or age 18 or over with at least one of: BMI of 35.0 or more; diabetes treated "
     "with medication; chronic kidney disease with eGFR below 60; immunosuppression (including prednisolone 20 mg/day "
     "or more for 2 weeks or longer); chronic lung disease needing daily maintenance inhalers; pregnancy."),
    ("interaction check", "not taking amiodarone, carbamazepine, rifampicin, St John's wort or tacrolimus; simvastatin "
     "is allowed only if it is paused for the course plus 5 days."),
    ("supply rule", "Paxavir may be supplied only if all three conditions are met."),
])

HOSPICE = card([
    ("terminal certification", "the hospice medical director and the member's attending physician (if the member has "
     "one) each certify, within the 15 days before the benefit period starts, that life expectancy is 6 months or "
     "less if the illness runs its normal course."),
    ("election", "the member signs an election statement choosing comfort-focused care for the terminal illness and "
     "related conditions and giving up curative treatment for them; treatment of conditions unrelated to the "
     "terminal illness remains covered under the member's regular benefits."),
    ("hospice rule", "the member may elect the hospice benefit when both conditions above are met."),
])

ITEMS = [
# ------------------------------------------------------------------ Carer Support Payment
# C1: 240 - 12 - 9 - 10 (half pension) = 209; childminder (not a relative) 70 <= 104.50 cap -> 139 <= 151 -> entitled.
# Twin: care paid to her mum (close relative) -> not deductible -> 209 > 151 -> not entitled.
Y("Under the Tallis rules as written, is the poster entitled to Carer Support Payment?",
"""Tallis Carers Corner - community forum
Board: Money and benefits | Thread: "Earnings limit - am I over?"

Posted by jolene_a (41):
"Hi all. I care for my dad about 38 hours a week - he gets Attendance Supplement at the higher rate. I also work part-time at the library: my payslip says gross 240 pounds a week, income tax 12 pounds, National Insurance 9 pounds, and I put 20 pounds a week into my workplace pension. I pay Deb, a registered childminder, 70 pounds a week to look after my son (he's 9) while I'm at work. I'm not studying. Do I qualify for Carer Support Payment or am I wasting my time applying?"

Reply from gary_h: "Earnings limit is 151 and you earn 240. You're way over, sorry."

Reply from moderator (no decision given): "Please read the full earnings rule before deciding - the adviser line opens Monday."
""",
1, 3, CA_YCARD,
twin=T([("I pay Deb, a registered childminder, 70 pounds", "I pay Deb, my mum, 70 pounds")], 0)),

# C2: 20 h for mother + 18 h for father cannot be combined -> rule 2 fails -> not entitled.
Y("Is Mr Farouk-Ellison entitled to Carer Support Payment?",
"""Tallis County Council - Carer Support Payment claim, adviser notes
Claimant: Mr Idris Farouk-Ellison, 58 | Date: 17 March 2025

- Took early retirement last year; no earnings; not in education.
- Parents live together two streets away. Both receive Attendance Supplement at the lower rate.
- Caring hours (claimant's diary for a typical week): mother - 20 hours (personal care, medication, appointments); father - 18 hours (shopping, meals, supervision after his stroke). Total 38 hours.
- Claimant: "Between the two of them I'm there every day, easily 35-plus hours."

Adviser comment: "Well over 35 hours of caring each week - should be straightforward."
""",
0, 2, CA_YCARD),

# C3: partner gets only the mobility part of PIA -> not a qualifying benefit -> rule 2. 18 h study < 21 h (rule 4 ok).
C("Which Carer Support Payment rule, if any, does this claim fail?",
"""Tallis County Council - Carer Support Payment decision worksheet
Claimant: Ms Anouk Brightwater-Diallo, 19

Education: first-year nursing student; college timetable shows 18 hours a week of supervised study, plus independent reading.
Earnings: none.

Caring: lives with her partner, Kieran (23), who has multiple sclerosis. She provides about 40 hours of care a week (help with transfers, catheter care, meals, medication).
Kieran's benefits: Personal Independence Allowance - mobility part at the enhanced rate. His claim for the daily living part was refused in 2024 and he has not appealed.

Claimant statement: "I'm a student, so I'm worried that rules me out."
""",
CA_OPTS, "rule 2 caring", 2, CA_CARD),

# C4: State Pension 95.10 >= 81.90 -> underlying entitlement but nothing paid -> will not receive a payment.
# Twin: pension 72.40 -> paid 9.50 a week -> receives a payment.
Y("Will Mrs Oduya-Stroud actually be paid any Carer Support Payment each week?",
"""Letter to Tallis Benefits Advice Service
From: Mrs Beryl Oduya-Stroud, 68
Date: 2 June 2025

Dear Adviser,

I care for my husband Clement, who had a stroke two years ago. He gets Attendance Supplement at the higher rate, and I look after him for more than 50 hours a week - washing, dressing, meals, his tablets and getting him to appointments. I do not work and I am not studying.

My only income is my own State Pension, which is 95.10 pounds a week.

My neighbour says that because I meet all the conditions I will get the carer payment on top of my pension. My daughter says I won't get anything. Could you tell me which of them is right before I fill in the long form?

Yours sincerely,
Beryl Oduya-Stroud
""",
0, 3, CA_PAY,
twin=T([("State Pension, which is 95.10 pounds a week", "State Pension, which is 72.40 pounds a week")], 1)),

# C5: 196 - 8 - 6 - 12 (half of 24) = 170; care paid to sister (close relative) not deductible -> 170 > 151 -> rule 3.
C("Applying the Carer Support Payment rules, which rule does this claimant fail, if any?",
"""Tallis Carers Corner - community forum
Board: Money and benefits | Thread: "Did my sums right?"

Posted by nadia_k (33):
"Quick check before I send my claim. I look after my mum 36 hours a week; she gets Personal Independence Allowance daily living at the standard rate. I'm not a student. I work in a café: gross 196 pounds a week, tax 8 pounds, NI 6 pounds, pension contribution 24 pounds a week. My sister looks after Mum for the four hours I'm at work each day and I pay her 30 pounds a week for it. So my earnings are 196 - 8 - 6 - 24 - 30 = 128 pounds, which is under the 151 limit. Right?"

Reply from ellis_b: "Looks right to me, you're well under."
""",
CA_OPTS, "rule 3 earnings", 3, CA_CARD),

# ------------------------------------------------------------------ Ardmore Patient Travel Scheme
# AT1: HC3 contribution 30.00; costs 2 x 46 mi x 0.20 = 18.40 + parking 8.00 = 26.40 <= 30.00 -> no reimbursement.
# Twin: contribution 10.50 -> 15.90 excess -> partial reimbursement.
C("What outcome should the Ardmore Patient Travel Scheme give this claim?",
TRAVEL_TEXT + """

Claim received 20 May 2025 from Mr Fergus Ilori-Banks, 57, holder of a valid HC3 certificate showing a weekly contribution of 30.00 pounds.
Journeys: two return car journeys to the Ardmore Hospital cardiology clinic (consultant referral after a GP letter), on Monday 12 May and Thursday 15 May 2025. Each return journey is 46 miles. Hospital car park: 4.00 pounds each visit.
He has no other qualifying benefit.
""",
labels(TRAVEL_OUT), "no reimbursement", 3, card(TRAVEL_OUT),
twin=T([("weekly contribution of 30.00 pounds", "weekly contribution of 10.50 pounds")], "partial reimbursement")),

# AT2: journey 12 Feb 2025 -> deadline 12 May; claim received 14 May -> late -> no reimbursement.
Y("Can Mr Adeyemi-Holt be reimbursed under the Ardmore Patient Travel Scheme?",
"""Ardmore Patient Travel Scheme - claims office note

Claimant: Mr Solomon Adeyemi-Holt, 81 | Receives Pension Credit guarantee credit
Journey: 12 February 2025, return bus and train to Ardmore Hospital for a consultant ophthalmology appointment (cataract assessment, referred by his GP). Fares 18.60 pounds, tickets enclosed.
Claim form: signed 9 May 2025; postmarked 12 May 2025; received by the claims office 14 May 2025.

Claimant's covering letter: "I posted this within the three months, as the date on the envelope shows. Please don't hold the post against me."

Claims officer comment: "Scheme rules count the date we receive the claim."
""",
0, 2, TRAVEL_Y),

# AT3: UC earnings 512 > 435 (no help via UC), but valid HC2 certificate -> full reimbursement.
C("How should the claims office decide this travel claim?",
TRAVEL_TEXT + """

Claimant: Ms Harriet Nwachukwu-Lowe, 36. Universal Credit: take-home earnings in her last assessment period were 512 pounds. She also holds an HC2 certificate valid until 31 December 2025 (issued after a low-income assessment).
Journey: 3 June 2025, return bus fare 7.20 pounds to the Ardmore Hospital fracture clinic, after the emergency department referred her for orthopaedic follow-up.
Claim received: 18 June 2025.
Claims assistant note: "Earnings over the UC limit, so she doesn't qualify - suggest refusal letter."
""",
labels(TRAVEL_OUT), "full reimbursement", 2, card(TRAVEL_OUT)),

# ------------------------------------------------------------------ Northmere medical exemption certificate
# PX1: diet-only diabetes; hyperthyroidism (not hypothyroidism); epilepsy off medication; ileostomy reversed;
# temporary disability (broken ankle) -> none of these.
C("Which listed condition, if any, entitles the applicant to a Northmere medical exemption certificate?",
"""Northmere Prescription Services - medical exemption application (GP section)
Applicant: Mrs Ottoline Brandt-Achebe, 57
Completed by: Dr Salome Iwu, 14 April 2025

Relevant conditions:
- Type 2 diabetes diagnosed 2023; HbA1c 49 mmol/mol; managed with diet and exercise alone.
- Hyperthyroidism (Graves' disease), on carbimazole 10 mg daily since 2024.
- Epilepsy: two seizures in 2012; seizure-free and off all anticonvulsants since 2019.
- Ileostomy after emergency bowel surgery in 2023; the ileostomy was reversed in May 2024 and she has no stoma now.
- Fractured right ankle in January 2025, in a boot; needs her husband to drive her and help her outside the house; expected recovery by July.

Applicant's note: "I take four regular medicines and my prescriptions are costing a fortune."
""",
RX_OPTS, NONE, 3, RX_CARD),

# PX2: idiopathic hypoparathyroidism -> qualifies; breast cancer treatment ended 2019 (not current), metformin for PCOS.
C("Which condition on the list makes this applicant eligible for a Northmere medical exemption certificate, if any?",
"""Northmere Prescription Services - exemption query (email)
From: Ms Clementine Oyelowo-Farr, 45
Date: 9 September 2025

"Hello, I'd like to apply for a medical exemption certificate. My conditions:
1. Breast cancer - I had surgery and chemotherapy in 2019, finished all treatment that year and was discharged from oncology follow-up in 2024.
2. Polycystic ovary syndrome - I take metformin for it, but I don't have diabetes (my GP checks every year).
3. Low calcium since my twenties - the endocrinologist says my parathyroid glands don't make enough of their hormone, cause unknown. I take calcitriol and calcium every day.
4. Migraine - I take sumatriptan when needed.
I assume the cancer is the one that counts?"
""",
RX_OPTS, "hypoparathyroidism", 2, RX_CARD),

# ------------------------------------------------------------------ Work Capability Supplement
# WC1: mobilising 200 m majority (6); 100 m only 2 days/week -> not majority; sitting 9; dexterity pen 9 + keyboard 9
# -> only 9 counts -> 6 + 9 + 9 = 24 -> standard. Twin: 100 m on five days a week -> 9 -> 27 -> enhanced.
C("Which Work Capability Supplement outcome does this assessment produce?",
WCS_TABLE + """

Assessment report extract - claimant Mr Percival Oduya-Lind, 52 (rheumatoid arthritis):
- Walking: "Can walk about 150 m on good days before pain stops him. On two days a week, during flares, he cannot manage 100 m."
- Sitting: "Cannot sit at a desk for more than 20-25 minutes on any day because of hip and back stiffness; standing is no better."
- Hands: "Cannot grip a pen well enough to write legibly; cannot use a keyboard or mouse for more than a few keystrokes. Can press buttons and turn pages."
- Coping with change: "No difficulties reported."
""",
labels(WCS_OUT), "standard rate", 3, card(WCS_OUT),
twin=T([("On two days a week, during flares", "On five days a week, during flares")], "enhanced rate")),

# WC2: mobilising 100 m majority (9); coping problems only a few times a month (not majority); pen only in cold
# spells -> total 9 < 15.
Y("Does the claimant reach the 15-point threshold for the Work Capability Supplement?",
WCS_TABLE + """

Assessment report extract - claimant Ms Rosalind Achterberg-Eze, 39 (heart failure and anxiety):
- Walking: "Most days cannot walk more than about 80-90 m on the flat before stopping breathless; can manage 60 m."
- Sitting and standing: "No difficulty."
- Hands: "Writing becomes difficult when her hands are very cold, a few weeks each winter."
- Coping with change: "A few times a month an unexpected change of plan (a cancelled bus, a moved appointment) leaves her unable to continue her day; on other days she copes."
Claimant's representative: "9 for walking, 9 for writing and 6 for change makes 24."
""",
0, 2, card([("15-point threshold", "the claimant scores 15 or more points, counting only descriptors that apply "
             "on the majority of days and only the highest-scoring descriptor within each activity.")])),

# ------------------------------------------------------------------ Tallis Hearing Assist
# HA1: right avg (30+35+40+50)/4 = 38.75; left (25+30+35+45)/4 = 33.75 -> better ear left 33.75 < 35 -> no subsidy.
# Twin: left 4 kHz 55 -> left avg 36.25 (still better ear) >= 35 -> subsidy.
Y("Does this applicant qualify for a subsidised hearing aid under Tallis Hearing Assist?",
"""Tallis Hearing Assist - application assessment
Applicant: Mr Gustav Obi-Harrington, 67 | Tallis concession card: valid
Previous subsidised devices: none

Pure-tone audiogram (air conduction, dB HL), 4 March 2025:
Right ear: 0.5 kHz 30, 1 kHz 35, 2 kHz 40, 4 kHz 50, 8 kHz 65
Left ear: 0.5 kHz 25, 1 kHz 30, 2 kHz 35, 4 kHz 45, 8 kHz 70

Audiologist comment: "Bilateral high-frequency sensorineural loss, worse on the right at most frequencies. Struggles in background noise. Recommend bilateral aids."
Applicant: "My right ear is well over 35 on average - surely that qualifies me."
""",
0, 3, HEAR,
twin=T([("4 kHz 45, 8 kHz 70", "4 kHz 55, 8 kHz 70")], 1)),

# HA2: previous device 4 y 2 m ago with better-ear avg 38.75 (right); now right 50.0, left 55.0 -> better ear 50.0,
# worsened 11.25 dB >= 10 -> replacement allowed -> qualifies.
Y("Can Mrs Lindqvist-Achebe receive a new subsidised hearing aid now?",
"""Tallis Hearing Assist - replacement request
Applicant: Mrs Agnetha Lindqvist-Achebe, 71 | Tallis concession card: valid
Previous subsidised aid fitted: 12 January 2021 (request date 20 March 2025)

Audiogram at the 2021 fitting (dB HL; 0.5 / 1 / 2 / 4 kHz):
Right: 35 / 35 / 40 / 45
Left: 40 / 45 / 45 / 50

Audiogram now, 10 March 2025:
Right: 45 / 45 / 50 / 60
Left: 50 / 55 / 55 / 60

Scheme officer note: "Previous aid less than 5 years ago, so replacement is not normally allowed. Loss has progressed but check against the rule."
""",
1, 3, HEAR),

# ------------------------------------------------------------------ Paxavir antiviral access
# AV1: symptoms began Monday = day 0 -> Saturday = day 5 -> in time; age 58 with eGFR 55 -> risk group;
# atorvastatin not on interaction list -> can supply.
Y("Can the pharmacist supply Paxavir to this patient today?",
"""Norvale Rapid Antiviral Access - community pharmacy consultation
Date: Saturday | Pharmacist: Idris Castellane-Oduya
Patient: Mrs Priya Ferrante-Mbeki, 58

Symptoms: sore throat and fever began on Monday morning; positive lateral flow test on Tuesday. "I've been ill for almost a week now - is it too late?"
Medical history: chronic kidney disease, eGFR 55 mL/min/1.73 m2 (GP record, March); hypertension.
Medicines: amlodipine 10 mg, atorvastatin 20 mg, omeprazole 20 mg. No herbal remedies.
Height 1.62 m; weight 71 kg. Not pregnant.

Pharmacist note: "Borderline on timing - she has had symptoms for six days."
""",
1, 2, PAX),

# AV2: age 44; BMI 108/1.77^2 = 34.5 < 35; asthma reliever only (no daily maintenance); no diabetes medication -> no risk.
Y("Is Mr Hollingsworth-Eze eligible for Paxavir?",
"""Norvale Rapid Antiviral Access - telephone assessment
Patient: Mr Barnabas Hollingsworth-Eze, 44 | Symptom onset: yesterday (day 1)

- Height 1.77 m; weight 108 kg. Patient: "My gym app says my BMI is 35, so I'm in the high-risk group."
- Asthma since childhood: uses a salbutamol reliever about twice a month; no preventer inhaler prescribed since 2019.
- Prediabetes (HbA1c 44 mmol/mol); diet advice only, no medication.
- No kidney disease, no immunosuppressive drugs. Not taking any interacting medicines.

Assessor note: "Asthma, prediabetes and obesity - three risk factors."
""",
0, 2, PAX),

# ------------------------------------------------------------------ hospice election
# HS1: both certifications within 15 days; dialysis is for polycystic kidney disease, unrelated to pancreatic cancer
# -> hospice can be elected and dialysis continues under regular benefits.
Y("Can Mr Achebe-Lindholm elect the hospice benefit while continuing his dialysis?",
"""Riverbend Hospice - admissions nurse note
Date: 3 November 2025 | Proposed benefit start: 5 November 2025
Patient: Mr Cornelius Achebe-Lindholm, 74

Terminal diagnosis: metastatic pancreatic adenocarcinoma (liver metastases), progressed through two lines of chemotherapy; oncology has stopped cancer treatment.
Certification: Riverbend's medical director certified a prognosis of 6 months or less on 30 October 2025; his attending physician, Dr Ines Mahlangu, signed the same certification on 1 November 2025.

Other conditions: end-stage kidney disease due to polycystic kidney disease, on haemodialysis three times a week since 2019 at the Pellbridge unit. Nephrology notes that his kidney disease is inherited and unrelated to his cancer.

Patient and wife: "We want comfort care for the cancer. He still wants his dialysis - he feels well on it."
Social worker: "I told them hospice means stopping all treatment, including dialysis."
""",
1, 2, HOSPICE),
]
