"""Triage under written criteria: KVETS emergency triage, Fastpath cancer referral, nurse-line child fever."""
from common import (Y, C, T, card, labels, KVETS, FAST, PHONE)

KV_OPTS, KV_CARD = labels(KVETS), card(KVETS)
FP_OPTS, FP_CARD = labels(FAST), card(FAST)
PH_OPTS, PH_CARD = labels(PHONE), card(PHONE)

FP_RULE = ("Fastpath referral form, instruction 1: if the patient meets the criteria for more than one pathway, refer "
           "on the pathway that appears first on the form (upper GI, then lower GI, then lung, then breast).")

ITEMS = [
# T1: one resource (ankle X-ray); oral ibuprofen, crutches not resources -> level 4. HR 104 only matters for level 3.
C("Which KVETS triage level should the nurse assign?",
"""Kestrel Valley Emergency Department - triage note, 19:42
Patient: male, 27

Presenting complaint: inversion injury to the right ankle playing five-a-side football about an hour ago. Heard a "pop". Unable to take four steps unaided at the scene or in triage; tender over the posterior edge of the lateral malleolus. No other injury, no head injury.

Observations: HR 104/min (ran from the car park, anxious); RR 18/min; SpO2 99% on room air; BP 138/82 mmHg; temperature 36.8 C. Pain 6/10.

Triage nurse's expected care: ankle X-ray (meets the Ottawa ankle rules); oral ibuprofen and paracetamol given at triage; ice and elevation; crutches before discharge if no fracture, or a backslab if a simple fracture is seen.

Patient: "My heart's racing, is that normal?"
""",
KV_OPTS, "level 4", 3, KV_CARD),

# T2: labs + ultrasound = 2 resources -> level 3; HR 108 > 100 (danger zone) -> level 2. Twin HR 96 -> level 3.
C("Using the KVETS scale, what triage level applies to this patient?",
"""Kestrel Valley Emergency Department - triage note, 14:10
Patient: female, 45

Presenting complaint: right upper abdominal pain for 5 hours, started an hour after a fatty lunch, constant, radiating to the right shoulder blade. Vomited twice. No chest pain, no breathlessness.

Observations: HR 108/min; RR 18/min; SpO2 98% on room air; BP 132/80 mmHg; temperature 37.6 C. Pain 5/10. Alert, walking comfortably, speaking normally.

Anticipated work-up: bloods (full blood count, liver tests, lipase, CRP); urine sent to the lab; abdominal ultrasound; oral paracetamol and an oral antiemetic at triage.

Nurse note: "Looks well - probable biliary colic."
""",
KV_OPTS, "level 2", 3, KV_CARD,
twin=T([("HR 108/min", "HR 96/min")], "level 3")),

# T3: graze cleaning/dressing, oral paracetamol, tetanus up to date -> no resources -> level 5 (HR 112 irrelevant).
C("What KVETS level should be recorded for this child?",
"""Kestrel Valley Emergency Department - paediatric triage, 17:05
Patient: boy, 9 years

Fell off his bike onto the pavement 30 minutes ago; was wearing a helmet, no head injury, no loss of consciousness. Large graze on the left knee with gravel in it, oozing; full range of movement at the knee, walking normally, no bony tenderness.

Observations: HR 112/min (crying at triage); RR 20/min; SpO2 99%; temperature 36.6 C. Pain 4/10.

Immunisations up to date including tetanus (school-age booster given last year).

Expected care: wound irrigation and gravel removal, simple dressing, oral paracetamol. No imaging planned.

Mother: "It's bleeding a lot and he's very upset - can he be seen quickly?"
""",
KV_OPTS, "level 5", 2, KV_CARD),

# T4: infant 56 days old with temperature 38.1 C -> level 2 (high-risk). Twin: 98 days old -> not 2(a); one resource
# (urine culture sent to lab) -> level 4 (danger-zone rule applies only to level 3 patients).
C("Which KVETS triage level applies to this infant?",
"""Kestrel Valley Emergency Department - paediatric triage, 03:20
Patient: girl. Age: 8 weeks (56 days). Born at term, no neonatal problems.

Parents report she felt hot and was a little unsettled from midnight; fed normally at 02:00.

Observations at triage: temperature 38.1 C (rectal); HR 150/min; RR 38/min; SpO2 99%; capillary refill under 2 seconds. Alert, pink, crying vigorously and consolable; fontanelle soft; no rash.

Expected at triage: urine sample for dipstick and laboratory culture; review by the paediatric doctor.

Nurse note: "Well-looking baby, feeding fine, parents understandably anxious."
""",
KV_OPTS, "level 2", 2, KV_CARD,
twin=T([("Age: 8 weeks (56 days)", "Age: 14 weeks (98 days)")], "level 4")),

# T5: dementia with baseline disorientation (unchanged) -> not new confusion; X-ray + labs = 2 -> level 3; vitals normal.
C("Under KVETS, which level should this patient be given?",
"""Kestrel Valley Emergency Department - triage note, 10:25
Patient: female, 78, brought by ambulance from Rowan House care home

Presenting complaint: fell from standing in her room this morning onto an outstretched left hand; painful, swollen, deformed left wrist. No head injury witnessed; carer found her sitting on the floor within minutes.

Background: Alzheimer's dementia. Care home staff: "She is always disorientated - she thinks it's 1985 and asks for her husband, who died years ago. She's exactly the same as usual today."

Observations: HR 88/min; RR 16/min; SpO2 95% on room air; BP 150/84 mmHg; temperature 36.9 C; blood glucose (fingerstick) 6.2 mmol/L. Pain 6/10 (behavioural pain scale).

Expected care: left wrist X-ray; blood tests to look for a cause of the fall; oral analgesia; a splint.

Ambulance crew: "Confused throughout the journey."
""",
KV_OPTS, "level 3", 2, KV_CARD),

# T6: not level 1 (no immediate life-saving intervention; SpO2 90% on 2 L); labs + X-ray + nebulised meds = 3 resources
# -> level 3, with RR 24 and SpO2 < 92% danger-zone vitals -> level 2.
C("What KVETS triage level is correct for this patient?",
"""Kestrel Valley Emergency Department - triage note, 06:50
Patient: male, 69, known COPD (home nebuliser, no home oxygen)

Presenting complaint: three days of increasing breathlessness and green sputum.

Observations on arrival: SpO2 84% on room air; after 2 L/min nasal oxygen for 5 minutes, SpO2 90%. RR 24/min; HR 96/min; BP 146/88 mmHg; temperature 37.8 C. Speaking in full sentences, alert, no drowsiness. Using accessory muscles slightly.

Expected care: arterial blood gas and routine bloods; chest X-ray; nebulised salbutamol and ipratropium; oral prednisolone.

Paramedic handover: "Sats were in the low eighties - he's very hypoxic."
""",
KV_OPTS, "level 2", 3, KV_CARD),

# T7: dipstick and pregnancy test are point-of-care (not resources); urine culture sent to lab = 1; oral antibiotic
# not a resource -> level 4. HR 104 irrelevant outside level 3.
C("Which triage level does the KVETS scale give this patient?",
"""Kestrel Valley Emergency Department - triage note, 22:15
Patient: female, 25

Presenting complaint: burning on passing urine and frequency for 2 days; mild lower abdominal ache. No loin pain, no vomiting, no vaginal bleeding.

Observations: HR 104/min; RR 16/min; SpO2 99%; BP 118/72 mmHg; temperature 37.9 C. Pain 3/10. Walked in; well-looking.

At triage: urine dipstick (leucocytes and nitrites positive) and urine pregnancy test (negative) done by the triage nurse.
Expected care: midstream urine sent to the laboratory for culture; oral nitrofurantoin prescription; safety-net advice.
""",
KV_OPTS, "level 4", 2, KV_CARD),

# T8: bloods + IV antibiotics = 2 resources -> level 3; temp 38.4 not a danger-zone vital; HR 98, RR 18, SpO2 97 -> level 3.
C("Applying KVETS, which level should be assigned?",
"""Kestrel Valley Emergency Department - triage note, 12:40
Patient: male, 60, type 2 diabetes

Presenting complaint: red, hot, swollen right lower leg for 3 days, spreading despite 48 hours of oral flucloxacillin from his GP. Marked edge drawn by GP yesterday; redness now 4 cm beyond it. No wound, no crepitus.

Observations: temperature 38.4 C; HR 98/min; RR 18/min; SpO2 97% on room air; BP 134/78 mmHg; fingerstick glucose 11.2 mmol/L. Pain 5/10. Alert and orientated.

Expected care: blood tests (full blood count, CRP, renal function, blood cultures); intravenous antibiotics; review of the spreading edge.

GP letter: "Febrile - please assess for sepsis."
""",
KV_OPTS, "level 3", 2, KV_CARD),

# T9: RR 6, SpO2 81%, needs bag-valve-mask ventilation and naloxone now -> level 1, although he groans to pain.
C("Which KVETS level applies on arrival?",
"""Kestrel Valley Emergency Department - resuscitation-bay handover, 01:12
Patient: male, about 24

Found by friends at a party, slumped in a bathroom with a syringe nearby. Paramedics could not obtain IV access and have not given naloxone; oxygen by face mask en route.

On arrival: groans and briefly flexes his arm to a sternal rub; no response to voice. Pupils pinpoint. Respiratory rate 6/min, shallow; SpO2 81% on 15 L/min oxygen by non-rebreather mask. HR 58/min; BP 104/64 mmHg; fingerstick glucose 5.8 mmol/L.

Charge nurse: "He's responding to pain, so he's not unresponsive."
""",
KV_OPTS, "level 1", 3, KV_CARD),

# T10: anaphylaxis with wheeze and hypotension needs IM adrenaline now -> level 1, although alert and talking.
C("What is the correct KVETS triage level for this patient?",
"""Kestrel Valley Emergency Department - triage note, 20:03
Patient: female, 19

Ate a cereal bar containing peanuts 20 minutes ago; known peanut allergy; did not have her adrenaline pen with her. Friend drove her in.

At triage: swollen lips and tongue, hoarse voice, audible wheeze, widespread hives. Alert, talking in short sentences, very anxious.
Observations: BP 84/50 mmHg; HR 128/min; RR 26/min; SpO2 93% on room air.

Triage nurse plan: "Needs intramuscular adrenaline now, then IV fluids and observation."
Student nurse: "She's alert and talking - isn't she a level 2?"
""",
KV_OPTS, "level 1", 2, KV_CARD),

# F1: DOB 18 Jun 1970, seen 2 Jun 2025 -> 54, so upper GI (>= 55) not met; FIT 14 >= 10 -> lower GI.
C("On which Fastpath pathway, if any, should the GP refer this patient?",
FP_RULE + """

GP consultation - 2 June 2025
Patient: Mr Aurelio Brandt-Mensah, date of birth 18 June 1970.

Six weeks of heartburn and acid reflux, not settling with omeprazole. Unintentional weight loss of 6 kg over 3 months (confirmed on practice scales). No difficulty swallowing, no vomiting, no abdominal pain. Bowel habit unchanged; no rectal bleeding.
Bloods: haemoglobin 142 g/L, ferritin normal.
FIT (sent last week as part of routine bloods): 14 ug Hb/g.

GP note: "He turns 55 this month - weight loss with reflux, so I'm thinking upper GI."
""",
FP_OPTS, "lower GI fastpath", 3, FP_CARD),

# F2: rectal bleeding explained by anal fissure; iron deficiency at 52 (< 60); no FIT; weight stable -> routine.
C("Which Fastpath pathway, if any, fits this patient?",
FP_RULE + """

GP consultation - 11 March 2025
Patient: Mrs Philippa Oyelaran-Kerr, 52

Bright red blood on the toilet paper for 3 weeks, with sharp pain on opening her bowels. Examination: posterior anal fissure clearly visible; no mass on rectal examination. Bowel habit otherwise normal; weight stable; no abdominal pain.
Bloods: haemoglobin 108 g/L, ferritin 9 ug/L (iron-deficiency anaemia). Heavy periods for the last year.
FIT: not yet done.

Plan discussed: fissure treatment, iron, gynaecology review of periods. Patient asks whether she needs "the cancer referral".
""",
FP_OPTS, "routine referral", 2, FP_CARD),

# F3: 41-year-old with unexplained haemoptysis (normal CXR) -> lung fastpath.
C("Under the Fastpath criteria, where should this patient be referred?",
FP_RULE + """

GP consultation - 5 May 2025
Patient: Mr Tobias Achterberg-Okafor, 41

Coughing up small amounts of bright red blood on and off for 3 weeks. No recent chest infection, no nosebleeds, not on anticoagulants; never smoked. Works as a school teacher. Weight stable.
Chest X-ray (last week): "clear lungs, no mass, no effusion".
Examination unremarkable.

GP note: "X-ray normal and a non-smoker - reassuring. Consider routine chest clinic."
""",
FP_OPTS, "lung fastpath", 2, FP_CARD),

# F4: DOB 20 Nov 1995, seen 30 Oct 2025 -> aged 29 -> breast lump criterion (>= 30) not met -> routine.
C("Which Fastpath pathway, if any, should be used for this referral?",
FP_RULE + """

GP consultation - 30 October 2025
Patient: Ms Saoirse Adebayo-Lind, date of birth 20 November 1995.

Noticed a painless lump in the upper outer left breast 2 weeks ago. Examination: 1.5 cm smooth, mobile, rubbery lump; no skin change; no nipple change or discharge; no axillary nodes. No family history of breast cancer. No other symptoms; weight stable.

Patient: "I'm thirty next month - my mum says anyone my age with a lump gets the two-week appointment."
""",
FP_OPTS, "routine referral", 3, FP_CARD),

# F5: dysphagia (upper GI) and iron deficiency at 67 (lower GI) -> first listed -> upper GI.
C("On which Fastpath pathway should this patient be referred?",
FP_RULE + """

GP consultation - 18 August 2025
Patient: Mr Ignatius Farrow-Nnadi, 67

Food "sticking" behind the breastbone for 6 weeks, especially bread and meat. Lost 4 kg. No abdominal pain; bowels normal; no rectal bleeding.
Bloods: haemoglobin 101 g/L, ferritin 6 ug/L (iron-deficiency anaemia).
FIT: 4 ug Hb/g.

GP note: "Iron deficiency at 67 - lower GI referral?"
""",
FP_OPTS, "upper GI fastpath", 2, FP_CARD),

# F6: age 51 with new retraction of one nipple only (no lump) -> breast fastpath.
C("Which Fastpath pathway, if any, applies?",
FP_RULE + """

GP consultation - 9 September 2025
Patient: Mrs Leonie Castellanos-Pike, 51

Noticed 6 weeks ago that her left nipple has become pulled inwards; it has never been like this before. The right nipple is normal. No lump felt by her or on examination; no discharge; no skin change; axillae normal. Mammogram 2 years ago normal.

GP note: "No lump found - reassure and review in 3 months?"
""",
FP_OPTS, "breast fastpath", 2, FP_CARD),

# PT1: 4-month-old with 38.6 C (3-6 months threshold is 39.0), fever day 2, feeding, wet nappies -> home care.
C("Which Brookhaven nurse-line disposition should be given?",
"""Brookhaven Nurse Line - call record, 20 October 2025, 19:05
Caller: mother of Ezra (date of birth 12 June 2025)

"He's had a temperature since yesterday afternoon. It was 38.6 C under the arm about half an hour ago. He's had paracetamol for babies and it's come down a bit. He's feeding - he took a full bottle an hour ago - and he's had three wet nappies today. He's grizzly but he smiles at me and he's awake and watching everything. No rash, his breathing seems normal, no fits. He's not on any medicines, never been ill before."

Nurse checks: no rash (glass test done, marks fade); soft fontanelle; breathing 36/min counted by the mother; skin pink.
Mother: "Should I take him to A&E? He's so little."
""",
PH_OPTS, "home care", 3, PH_CARD),

# PT2: fever began Monday (day 1) -> Friday = day 5 -> see a doctor within 4 hours (outranks urinary pain disposition).
C("What disposition does the Brookhaven child-fever protocol give for this call?",
"""Brookhaven Nurse Line - call record, Friday 14:20
Caller: father of Maya, aged 3

"Her fever started on Monday evening and it just keeps coming back - 38.9 C this morning. She says it hurts when she wees. She's eating a bit less but drinking fine and she's weeing normally, lots of wet pants actually. She's playing with her brother now, chatting away. No rash, she can move her neck fine, breathing's normal. She's healthy otherwise, no medicines. It's been four days of this - is that normal for a virus?"

Nurse checks: alert and talking in the background; lips and tongue moist; no rash; no breathing difficulty.
""",
PH_OPTS, "see a doctor within 4 hours", 3, PH_CARD),

# PT3: first-ever febrile seizure lasting 2 minutes, now stopped, rousable -> ED now (not ambulance: < 5 min, not
# unresponsive, breathing normally).
C("Which disposition should the nurse give under the Brookhaven protocol?",
"""Brookhaven Nurse Line - call record, 23:48
Caller: grandmother of Oliver, aged 2

"He's had a fever all evening, 39.4 C. About ten minutes ago he went stiff and his arms and legs were jerking - I timed it on my phone, it was just under two minutes - then it stopped on its own. He's never had one before. He's sleepy now but he opens his eyes and cries when I talk to him, and he's pushing my hand away. His lips are pink and he's breathing normally now. No rash that I can see."

Nurse checks: breathing quietly, no grunting, colour normal; no further jerking during the call.
Grandmother: "Should I ring for an ambulance?"
""",
PH_OPTS, "go to the emergency department now", 2, PH_CARD),
]
