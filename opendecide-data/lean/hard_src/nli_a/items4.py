"""Families F22-F28."""
from common import Y, C3, SC, CNT, SUB, ENT

# ---------------------------------------------------------------- F22 lock-up round: except / none unlocked / lacked ... except
P22 = """FACILITIES SECURITY CHECK · Ridgemount Business Centre, Floor 2
Evening lock-up round by Samir Haddad (security) · Friday 21 March, 19:05–19:40

Rooms on the round: 2.01 to 2.18 (eighteen rooms).
{k}
Additional notes:
• 2.07 (server room) has a keypad lock; the keypad was showing a fault light. Reported to IT on-call.
• Kitchen area (not on the round) had the lights left on; switched off.
• The cleaners had finished floor 2 before the round started.

Procedure: any room found unlocked is to be locked by the officer and listed in the round report, and its tenant is to be notified by email on the next working day."""
TENANTS = ["Pellow & Grant, accountants", "Mireille Oduya Architects", "Cobweb Software Ltd",
           "Fairhaven Physiotherapy", "Lantern Translation Services", "Tessellate Design Studio",
           "building IT (server room)", "Brightside Recruitment", "Holm & Varley Solicitors",
           "Northgate Tutoring", "Quarry Hill Surveyors", "Saffron Events Ltd", "Kittering Insurance Brokers",
           "Meridale Charity Trust", "Aspen Payroll Bureau", "Vellum Books", "Driftwood Media",
           "Ostler Engineering Consultants"]
ROOMS = [(f"room 2.{i:02d}", f"let to {t}") for i, t in enumerate(TENANTS, 1)] + \
        [("none of these", "no room's tenant is to be notified")]
K22A = "No room was found unlocked except 2.11."

F22 = [
ENT("F22", "Which room's tenant is to be notified under the procedure?",
    P22.format(k=K22A), ROOMS, "room 2.11", 2,
    twin=([("No room was found unlocked except 2.11.",
            "No room was found unlocked, not even 2.11, which is often left open.")], "none of these")),
Y("F22", "Taking the security record as accurate, must the statement be true?",
  P22.format(k="Samir did not find any room unlocked that the cleaners had not already told him about."),
  "Samir found at least one room unlocked on the round.", 0, 3,
  twin=([("that the cleaners had not already told him about.",
          "that the cleaners had not already told him about; they had told him that 2.09 was unlocked, and he "
          "found it unlocked.")], 1)),
C3("F22", "How does the statement relate to the security record?",
   P22.format(k="Each room lacked a working door closer except 2.03 and 2.14. All eighteen rooms were found "
                "locked."),
   "Room 2.14 has a working door closer.", "F", 2),
SUB("F22", "Which combination of the numbered statements follows from the security record?",
    P22.format(k=K22A),
    ["Room 2.07 was found locked.",
     "The kitchen area was found locked.",
     "The cleaners were still working on floor 2 when the round started.",
     "The tenant of room 2.11 is to be notified by email on the next working day."], (1, 4), 2),
]

# ---------------------------------------------------------------- F23 operations manual: must not / need not / unless ... not
P23 = """SKYLARK SURVEYS · FIELD OPERATIONS MANUAL (extract), section 6: pre-flight
Applies to all company flights with aircraft under 4 kg.

6.1 The remote pilot must complete the checklist in the Skylark app before each flight.
6.2 {k}
6.3 A flight within 50 m of any person not involved in the operation must not take place.
6.4 The pilot need not notify the landowner in advance where the landowner is the client.

Job sheet J-5518 (Tuesday): remote pilot Farah Lindqvist; aircraft SK-M3 (0.9 kg); site: Coldwater Farm, grain-store roof inspection; client: Coldwater Farm Partnership (the landowner). Planned height 40 m; planned take-off 09:30. Nearest aerodrome: Brenley Airfield, 3.2 km north-east of the site. Weather check at 08:45: wind 12 knots, gusts 18.

Supervisor's note: Farah has 140 logged hours and holds the company's advanced endorsement."""
K23A = "A flight within 5 km of an aerodrome must not take place without the aerodrome's permission."
K23B = ("A flight within 5 km of an aerodrome need not have the aerodrome's permission if the planned height is "
        "below 45 m.")
K23C = ("No flight may take place within 5 km of an aerodrome unless the aerodrome has not objected within 24 "
        "hours of being notified.")

F23 = [
Y("F23", "Does the statement follow from the manual extract and job sheet?",
  P23.format(k=K23B),
  "The manual forbids Farah from flying J-5518 without Brenley Airfield's permission.", 0, 2),
Y("F23", "Is the statement a valid inference from the manual extract and job sheet?",
  P23.format(k=K23A),
  "The manual forbids Farah from notifying Coldwater Farm Partnership in advance.", 0, 2,
  twin=([("6.4 The pilot need not notify", "6.4 The pilot must not notify")], 1)),
C3("F23", "Classify the statement against the manual extract and job sheet.",
   P23.format(k=K23C),
   "Under the manual, Brenley Airfield not objecting is all that Farah needs before flying J-5518.", "C", 3),
SC("F23", "Which of the numbered statements follows from the manual extract and job sheet?",
   P23.format(k=K23A),
   ["The manual allows J-5518 to be flown within 50 m of people not involved in the operation.",
    "Farah must complete the checklist in the Skylark app before flying J-5518.",
    "The manual requires Farah to notify Coldwater Farm Partnership in advance.",
    "Brenley Airfield has given permission for J-5518."], 2, 1),
Y("F23", "Is the statement left unsupported by the manual extract and job sheet?",
  P23.format(k=K23C),
  "The manual does not allow Farah to fly J-5518 if Brenley Airfield objects within 24 hours of being notified.",
  0, 3, role="neg"),
]

# ---------------------------------------------------------------- F24 support chat: scope of "didn't" in speech
P24 = """Chat transcript · Pellham Home Goods support · ticket #PH-883120
Customer: Noor Abernethy · Order 55-20931 (placed 2 June)

Agent (Callum): Hi Noor, thanks for waiting. I can see order 55-20931: one Kessel table lamp and a set of four linen napkins. How can I help?
Noor: The parcel came today. {k}
Agent (Callum): I'm sorry about that. I can see the napkins were packed in the same box. Did they arrive OK?
Noor: Yes, the napkins are fine.
Agent (Callum): Thanks. I've logged the issue with our warehouse and I'll email you a returns label for the lamp now. Please use the original box if you still have it.
Noor: Will do, thanks.

Internal note (Callum): warehouse to check picking for the Kessel lamp (SKU family KL-22x). Refund or replacement, at the customer's choice, once the return is scanned."""
K24A = "I didn't order the ochre lamp. That's what came."
S24 = "The lamp that arrived is ochre."

F24 = [
Y("F24", "Does the statement follow from the chat transcript?", P24.format(k=K24A), S24, 1, 2),
Y("F24", "Can the statement be concluded from the transcript alone?",
  P24.format(k="What came isn't the lamp I ordered. I didn't order an ochre one."), S24, 0, 3),
C3("F24", "What is the status of the statement, given the transcript?",
   P24.format(k="I didn't order the lamp in ochre, I ordered it in sage, and sage is what came. The problem is "
                "that it won't switch on."), S24, "C", 2,
   twin=([("and sage is what came. The problem is that it won't switch on.",
           "and sage is not what came. It won't switch on either.")], "O")),
CNT("F24", "How many of the numbered statements follow from the transcript?",
    P24.format(k=K24A),
    ["Noor did not order an ochre lamp.",
     "The lamp that arrived is ochre.",
     "The napkins that arrived were damaged."], 2, 2),
Y("F24", "Is the statement left unsupported by the transcript?",
  P24.format(k=K24A), "Noor said the napkins did not arrive in good condition.", 1, 1, role="neg"),
]

# ---------------------------------------------------------------- F25 election rules: only if / provided / not fewer than
P25 = """WESTHOLM ROWING CLUB · Annual General Meeting, 2 March
Returning officer's report (Tamsin Beaumont)

Election for Club Captain. Candidates: Oluwaseun Pike and Kristjan Aas.
Members eligible to vote: 132. Ballots returned: 97. Spoilt ballots: 3.
Valid votes: Pike 49, Aas 45.

Constitution, rule 11: "{rule}"

The figures were read out to the meeting, which then moved to item 6 (boathouse roof appeal). The treasurer reported £6,400 raised against a target of £9,000; a second appeal letter will go out in April."""
R25S = ("A candidate who receives more than half of the valid votes cast is elected, provided that the number of "
        "ballots returned is not fewer than two-thirds of the members eligible to vote.")
R25O = ("A candidate is elected only if they receive more than half of the valid votes cast and the number of "
        "ballots returned is not fewer than {frac} of the members eligible to vote.")
S25 = "Oluwaseun Pike was elected Club Captain."

F25 = [
Y("F25", "Is the statement guaranteed by the returning officer's report?", P25.format(rule=R25S), S25, 1, 3,
  twin=([("not fewer than two-thirds", "not fewer than three-quarters")], 0)),
Y("F25", "Does the statement follow from the report?", P25.format(rule=R25O.format(frac="two-thirds")),
  S25, 0, 3),
C3("F25", "Classify the statement against the report.", P25.format(rule=R25O.format(frac="three-quarters")),
   S25, "C", 3),
SC("F25", "Which conclusion can be drawn from the report with certainty?", P25.format(rule=R25S),
   ["Kristjan Aas received fewer than half of the valid votes cast.",
    "Fewer than two-thirds of eligible members returned a ballot.",
    "No ballot was spoilt.",
    "The roof appeal has reached its target."], 1, 2, head="Possible conclusions:"),
Y("F25", "Taking the report as accurate, must the statement be true?",
  P25.format(rule=R25O.format(frac="two-thirds")),
  "Oluwaseun Pike did not fail to meet any condition in rule 11.", 1, 3),
]

# ---------------------------------------------------------------- F26 society letter: no record / never / did not have children who
P26 = """Pendlow Family History Society · reply to enquiry PFHS/24/311

Dear Mr Achterberg,

Thank you for your enquiry about Ellen Marsh, born 1862 in Hollins End. We have searched the parish registers for Hollins End and the two neighbouring parishes, the 1881, 1891 and 1901 census returns, and the society's burial index.

{k}

In the 1891 census Ellen is listed as a live-in housekeeper at The Grange, Hollins End, for the family of a Mr Joseph Carrow. We found no record of her in the 1901 census. The burial index has an Ellen Marsh buried at St Aidan's in 1914, age given as 51, which would fit a birth in 1862 or 1863, but we cannot be certain that she is the same woman.

If you would like us to search the 1911 census, the fee is £12.

Yours sincerely,
Doreen Plaskett, Research Volunteer"""
K26A = "The registers record no marriage for Ellen, and no children baptised to her."

F26 = [
Y("F26", "Does the letter establish the statement?", P26.format(k=K26A), "Ellen Marsh never married.", 0, 2),
Y("F26", "Based only on the letter, is the statement necessarily true?",
  P26.format(k="Ellen never married. Her son, Thomas, was baptised in 1886 with no father named."),
  "Ellen Marsh had at least one child.", 1, 2),
Y("F26", "Is the statement entailed by the letter?",
  P26.format(k="Ellen did not have children who survived infancy: two daughters, baptised in 1887 and 1889, "
               "were each buried within the year."),
  "Ellen Marsh had no children.", 0, 2),
C3("F26", "How does the statement stand in relation to the letter?",
   P26.format(k="We found no evidence that Ellen did not marry: a marriage between Ellen Marsh and Walter Greaves "
                "is recorded in 1884, though the entry is damaged."),
   "The Society found no record of a marriage for Ellen.", "C", 2),
SC("F26", "Which one of the numbered statements is guaranteed by the letter?", P26.format(k=K26A),
   ["Ellen was not living at The Grange in 1891.",
    "The Ellen Marsh buried in 1914 is not the enquirer's Ellen.",
    "The Society has already searched the 1911 census for Ellen.",
    "Ellen had no children."], 0, 2, head="Statements to check:"),
]

# ---------------------------------------------------------------- F27 leaflet: must not ... without / need not / unless
P27 = """PATIENT INFORMATION · Corvalen 20 mg tablets
Dispensed by Marlow Street Pharmacy for Mr Ivo Santangelo. Prescriber: Dr R. Amadi.

How to take: one tablet once a day, in the morning. {k}
Do not take more than one tablet in 24 hours. If you miss a dose, take it as soon as you remember unless it is already evening; do not take two tablets to make up for a missed one.
Alcohol: avoid drinking alcohol while taking Corvalen.
Other medicines: tell your pharmacist if you take any medicine for blood pressure.
Stopping: do not stop taking Corvalen suddenly without speaking to your prescriber, even if you feel well.

Pharmacist's label note (checked by K. Duarte): Mr Santangelo also takes Belazine for blood pressure; the prescriber is aware and is happy for both to be taken together."""
K27A = "You can take it with or without food."

F27 = [
Y("F27", "Does the statement follow from the leaflet?",
  P27.format(k="It must not be taken without food."),
  "The leaflet allows Mr Santangelo to take Corvalen on an empty stomach.", 0, 2,
  twin=([("It must not be taken without food.", "It need not be taken with food.")], 1)),
C3("F27", "Given the leaflet, which label fits the statement?", P27.format(k=K27A),
   "The leaflet forbids taking Corvalen together with Belazine.", "C", 2),
Y("F27", "Is the statement left unsupported by the leaflet?", P27.format(k=K27A),
  "If Mr Santangelo misses his morning dose and remembers at 10 pm, the leaflet tells him to take it then.",
  1, 2, role="neg"),
SC("F27", "Which of the numbered statements follows from the leaflet?", P27.format(k=K27A),
   ["Mr Santangelo may stop taking Corvalen whenever he feels well.",
    "The leaflet does not permit taking two tablets within the same 24 hours.",
    "The leaflet forbids taking Corvalen with food.",
    "Dr Amadi does not know that Mr Santangelo takes Belazine."], 2, 2),
]

# ---------------------------------------------------------------- F28 grants FAQ: not-for-profit / no applicant that is not
P28 = """Harrowby Community Foundation · Small Grants Round 14: eligibility FAQ

Q: Who can apply?
A: {k}

Q: How much can we ask for?
A: Between £500 and £5,000. Groups with an annual income above £250,000 cannot apply to this round.

Q: What can't the grant pay for?
A: Salaries of existing staff, costs already incurred, religious activity, and party-political campaigning.

Screening log (officer: Bryony Kessel). All four groups are based in the Harrowby district.
• Tollgate Tenants' Forum: not-for-profit unincorporated association with a written constitution; not a registered charity; annual income £3,100.
• Oakmere Youth Boxing CIC: community interest company; annual income £88,000.
• Lindley Parish Church choir: part of a registered charity (the parish); annual income £12,000; project is a free concert series.
• Selby Hurst Ltd: private limited company that distributes its profits to shareholders; annual income £140,000; wants funding for a community garden."""
K28A = ("Any not-for-profit group based in the Harrowby district may apply. However, no applicant that is not a "
        "registered charity or a community interest company (CIC) will be funded.")
K28B = ("Only not-for-profit groups based in the Harrowby district. Registration as a charity is not required, and "
        "no group is excluded for being unincorporated.")
K28C = ("Only registered charities and CICs based in the Harrowby district, and unregistered not-for-profit groups "
        "based in the district that have a written constitution.")
GROUPS = [
    ("Tollgate Tenants' Forum", "first group in the screening log"),
    ("Oakmere Youth Boxing CIC", "second group in the screening log"),
    ("Lindley Parish Church choir", "third group in the screening log"),
    ("Selby Hurst Ltd", "fourth group in the screening log"),
    ("none of these", "no group in the log is certainly ineligible to apply"),
]

F28 = [
Y("F28", "Does the statement follow from the FAQ and screening log?", P28.format(k=K28A),
  "Tollgate Tenants' Forum will not be funded in this round.", 1, 2),
Y("F28", "Can the statement be concluded from the FAQ and screening log alone?", P28.format(k=K28A),
  "Tollgate Tenants' Forum is not eligible to apply.", 0, 3),
ENT("F28", "Which group in the screening log is certainly not eligible to apply?", P28.format(k=K28C),
    GROUPS, "Selby Hurst Ltd", 2,
    twin=([("private limited company that distributes its profits to shareholders",
            "private limited company that distributes no profits and has a written constitution"),
           ("annual income £88,000", "annual income £288,000")], "Oakmere Youth Boxing CIC")),
C3("F28", "What is the status of the statement, given the FAQ and screening log?", P28.format(k=K28A),
   "Lindley Parish Church choir will be funded in this round.", "O", 2),
Y("F28", "Is the statement a valid inference from the FAQ and screening log?", P28.format(k=K28B),
  "Selby Hurst Ltd may apply to this round.", 0, 2),
]

ITEMS = F22 + F23 + F24 + F25 + F26 + F27 + F28
