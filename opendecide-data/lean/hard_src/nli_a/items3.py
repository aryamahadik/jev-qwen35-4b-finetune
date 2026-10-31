"""Families F15-F21."""
from common import Y, C3, SC, CNT, ENT

# ---------------------------------------------------------------- F15 control log: except / not every / not any
P15 = """CALDER VALLEY RAILWAY · CONTROL LOG EXTRACT, Tuesday 4 February
Service 2K14, 07:12 Morrow Bridge to Hebden Scar. Booked calls: Morrow Bridge, Aldley, Brantwick, Cotter Lane, Dunmere, Elsby Road, Hebden Scar.

07:31 Signal failure reported between Brantwick and Cotter Lane; 2K14 held at Brantwick for 14 min.
07:45 Controller Maeve Ostrowski authorised 2K14 to run fast to recover time. {k}
08:22 2K14 arrived at Hebden Scar, 11 min late.
08:30 Complaint received via the app from a passenger travelling to Elsby Road, who says she was carried past her stop without warning.

Station note: Cotter Lane has a short platform; only the front four coaches can open there. 2K14 was formed of six coaches.
Delay attribution: signalling (Network), 14 min at Brantwick; 3 min recovered.
Actions: Customer Relations to reply to the complaint within 5 working days; driver to be asked whether a skip-stop announcement was made."""
K15B = "2K14 then did not call at every intermediate station after Brantwick."
STATIONS = [
    ("Aldley", "booked call between Morrow Bridge and Brantwick"),
    ("Brantwick", "booked call where 2K14 was held after the signal failure"),
    ("Cotter Lane", "first booked intermediate call after Brantwick"),
    ("Dunmere", "second booked intermediate call after Brantwick"),
    ("Elsby Road", "third booked intermediate call after Brantwick"),
    ("none of these", "no listed station is certain to have been passed without a call after Brantwick"),
]

F15 = [
Y("F15", "Would it be wrong to conclude the statement from the control log?",
  P15.format(k="2K14 then called at every intermediate station after Brantwick except Elsby Road."),
  "2K14 called at Dunmere.", 0, 1, role="neg"),
Y("F15", "Taking the log as accurate, must the statement be true?",
  P15.format(k=K15B), "2K14 did not call at Elsby Road.", 0, 2,
  twin=([("did not call at every intermediate station", "did not call at any intermediate station")], 1)),
Y("F15", "Is the statement a valid inference from the control log?",
  P15.format(k="2K14 then did not call at any intermediate station after Brantwick except Dunmere."),
  "2K14 called at Cotter Lane.", 0, 2),
ENT("F15", "Which intermediate station after Brantwick did 2K14 certainly pass without calling?",
    P15.format(k="2K14 then ran through every intermediate station after Brantwick except one without "
                 "stopping; the one where it did stop was not Dunmere."),
    STATIONS, "Dunmere", 3,
    twin=([("the one where it did stop was not Dunmere", "the one where it did stop was not Elsby Road")],
          "Elsby Road")),
C3("F15", "How does the statement relate to the control log?",
   P15.format(k=K15B),
   "At least one passenger on 2K14 was carried past the station they were travelling to.", "O", 2),
]

# ---------------------------------------------------------------- F16 consult notes: no evidence of / not ruled out / not negative
P16 = """BRACKENHILL VETERINARY CENTRE · CONSULT NOTES
Patient: "Juniper", 7-year-old female neutered Border Collie, 21.4 kg. Owner: Ms Harriet Coyle.
Presenting complaint: lameness, left forelimb, 5 days; worse after exercise.

Exam: weight-bearing lameness, grade 2/5, left fore. Mild pain on extension of the left elbow. No heat or swelling at the carpus. Right forelimb and both hindlimbs unremarkable.
Radiographs, left elbow (2 views): {k}
Bloods: tick-borne disease snap test {snap}.

Plan: strict lead-only exercise for 2 weeks; meloxicam at label dose with food; recheck in 14 days. Owner to call sooner if Juniper stops bearing weight or develops a swelling. Referral to orthopaedics if no improvement at recheck.
Vet: A. Lindqvist MRCVS"""
K16A = "no evidence of fracture. Mild osteophytes on the anconeal process; elbow dysplasia not ruled out."
NEG = "negative"
VOID = ("not negative: the control line failed to appear, so the test is void and will be repeated at the "
        "recheck")

F16 = [
Y("F16", "Does the statement follow from the consult notes?",
  P16.format(k=K16A, snap=NEG), "Juniper has elbow dysplasia.", 0, 1),
Y("F16", "Based only on the consult notes, is the statement necessarily true?",
  P16.format(k=K16A, snap=NEG), "Juniper does not have a fracture of the left elbow.", 0, 3,
  twin=([("no evidence of fracture.", "fracture ruled out.")], 1)),
Y("F16", "Is the statement guaranteed by the consult notes?",
  P16.format(k="no fracture seen.", snap=VOID), "The tick-borne disease snap test was positive.", 0, 2),
C3("F16", "Classify the statement against the consult notes.",
   P16.format(k="no fracture seen; the views do not exclude a fissure in the medial coronoid.", snap=NEG),
   "Juniper has a fissure in the medial coronoid.", "O", 2),
SC("F16", "Which of the numbered statements follows from the consult notes?",
   P16.format(k="no fracture seen, but fracture not ruled out; elbow dysplasia cannot be excluded either.",
              snap=NEG),
   ["A fracture was seen on the radiographs.",
    "The notes leave open both a fracture and elbow dysplasia.",
    "Juniper has elbow dysplasia.",
    "Juniper was no longer bearing weight on the left forelimb at the exam."], 2, 2),
]

# ---------------------------------------------------------------- F17 league report: unbeaten / winless / not failed to score
P17 = """FENMOOR & DISTRICT SUNDAY LEAGUE · Division Two round-up, week 9

Holloway Rovers stayed top after a 1–1 draw at Pike Street. Rovers have played nine league games and {k}.

Elsewhere, Grange Athletic {g}, 3–0 against a Kilnworth side reduced to ten men before half-time. Kilnworth have now lost four league games in a row. Pike Street's Tomasz Hale scored his eighth goal of the season.

Table (top four): 1 Holloway Rovers, {pts} pts; 2 Pike Street, 18 pts; 3 Ashby Wanderers, 16 pts; 4 Marlow Vale, 15 pts.
Points: 3 for a win, 1 for a draw, none for a defeat.

Next week: Holloway Rovers v Ashby Wanderers; Pike Street v Grange Athletic; Kilnworth v Marlow Vale."""
UNB = "are still unbeaten in the league"
G1 = "finally picked up their first league win of the season"

F17 = [
Y("F17", "If everything in the report is accurate, does the statement have to hold?",
  P17.format(k=UNB, g=G1, pts=21),
  "Holloway Rovers have drawn at least one league game besides this week's.", 1, 3,
  twin=([("1 Holloway Rovers, 21 pts", "1 Holloway Rovers, 25 pts")], 0)),
C3("F17", "Given the report, which label fits the statement?",
   P17.format(k="have not failed to score in any league game", g=G1, pts=21),
   "Holloway Rovers have scored in every league game except this week's.", "C", 3),
SC("F17", "Which one of the numbered statements is guaranteed by the report?",
   P17.format(k=UNB, g=G1, pts=21),
   ["Grange Athletic had lost every league game before this week.",
    "Grange Athletic had not won a league game before this week.",
    "Kilnworth have lost every league game this season.",
    "Holloway Rovers have lost a league game."], 2, 2,
   twin=([("finally picked up their first league win of the season",
           "picked up their second league win of the season")], 0)),
CNT("F17", "How many of the numbered statements follow from the report?",
    P17.format(k=UNB, g=G1, pts=21),
    ["Holloway Rovers have won six league games.",
     "Holloway Rovers have not lost a league game.",
     "Pike Street have lost at least one league game.",
     "Grange Athletic are still without a league win."], 2, 3, head="Statements to check:"),
]

# ---------------------------------------------------------------- F18 tender note: downward monotonicity under "no"
P18 = """TENDER EVALUATION NOTE · Brookfold District Council
Contract: supply of grit salt, winter season (Lot 2: 6 mm rock salt)
Evaluator: Ngozi Ferreira, Procurement Officer

Five bids were received by the deadline (12:00, 3 October): Altham Minerals, Cresswick Supplies, Dovecote Aggregates, Harbrook Salt and Pennock Trading.

Evaluation summary:
{k}
All five bidders confirmed stock held within 40 miles of the depot. Harbrook Salt's price per tonne was the lowest; Dovecote's was the highest.

Criteria (from the tender pack): price 60%, delivery lead time 30%, sustainability 10%. A bid that fails any mandatory requirement is excluded before scoring. Mandatory requirements: delivery within 72 hours of call-off; at least 500 tonnes available on call-off; valid public liability insurance.

Recommendation: award to the highest-scoring bid after moderation on 10 October."""
BIDDERS = [
    ("Altham Minerals", "bidder listed first in the note"),
    ("Cresswick Supplies", "bidder listed second in the note"),
    ("Dovecote Aggregates", "bidder listed third in the note"),
    ("Harbrook Salt", "bidder listed fourth in the note"),
    ("Pennock Trading", "bidder listed last in the note"),
    ("none of these", "no listed bidder is certain to be excluded before scoring"),
]

F18 = [
Y("F18", "Can the statement be concluded from the evaluation note alone?",
  P18.format(k="No bidder offered delivery within 48 hours of call-off."),
  "No bidder offered delivery within 24 hours of call-off.", 1, 2),
Y("F18", "Does the statement follow from the evaluation note?",
  P18.format(k="No bidder offered delivery within 24 hours of call-off."),
  "No bidder offered delivery within 48 hours of call-off.", 0, 2),
C3("F18", "What is the status of the statement, given the evaluation note?",
   P18.format(k="Not every bidder offered delivery within 48 hours of call-off."),
   "At least one bidder did not offer delivery within 24 hours of call-off.", "F", 3),
ENT("F18", "Which bidder must be excluded before scoring, according to the note?",
    P18.format(k="Every bidder offered delivery within 72 hours of call-off. None of the bidders except Altham "
                 "Minerals failed to confirm 500 tonnes on call-off. Cresswick's insurance certificate, which "
                 "lapsed in August, has since been renewed; Pennock's has not expired."),
    BIDDERS, "Altham Minerals", 3,
    twin=([("None of the bidders except Altham Minerals failed to confirm",
            "None of the bidders, Altham Minerals included, failed to confirm")], "none of these")),
]

# ---------------------------------------------------------------- F19 lab notebook: no significant difference / failed to replicate
P19 = """Lab notebook · Okonjo group, Department of Plant Sciences, Whitmoor University
Entry 2025-03-18 · author: Lise Marchetti (postdoc)

Aim: replicate the Tanaka-Braun (2021) finding that pre-soaking Arabidopsis seed in 50 mM KNO3 speeds up germination.
Method: 4 plates × 50 seeds per treatment (water control vs KNO3); same seed lot (Col-0, harvested August 2024); 22 °C, 16 h light. Germination scored as radicle emergence at 24, 36, 48 and 72 h. Scorer blind to treatment (plates coded by Adebayo).
Result: {k}
Notes: two control plates had condensation on the lid at 36 h; wiped, not excluded. Dormancy in this seed lot may be lower than in the original study (older seed).
Next: repeat with freshly harvested seed in May; ask Adebayo to re-code the plates."""
K19A = "no significant difference in germination between treatments at any time point (all p > 0.3)."

F19 = [
Y("F19", "Does the notebook entry establish the statement?",
  P19.format(k=K19A), "KNO3 pre-soaking had no effect on germination in this experiment.", 0, 2),
Y("F19", "Taking the entry as accurate, must the statement be true?",
  P19.format(k="we did not fail to see the effect at 36 h (KNO3 72% vs control 51%, p = 0.004), but there was "
               "no significant difference at 24, 48 or 72 h."),
  "At 36 h, a larger share of KNO3-treated seed than control seed had germinated.", 1, 2),
C3("F19", "How does the statement stand in relation to the notebook entry?",
   P19.format(k="we failed to replicate the effect: KNO3-treated seed did not germinate faster than control at "
                "any time point."),
   "The Tanaka-Braun (2021) finding is false.", "O", 2),
Y("F19", "Is the statement guaranteed by the notebook entry?",
  P19.format(k="germination was not significantly slower with KNO3 at any time point."),
  "KNO3-treated seed germinated faster than control seed at one or more time points.", 0, 2,
  twin=([("germination was not significantly slower with KNO3 at any time point.",
          "germination was significantly faster with KNO3 at every time point.")], 1)),
SC("F19", "Which of the numbered statements follows from the notebook entry?",
   P19.format(k=K19A),
   ["The person scoring germination knew which plates had been treated with KNO3.",
    "Not every plate had condensation on its lid at 36 h.",
    "At least one control plate was kept in the analysis despite condensation.",
    "The seed used was freshly harvested.",
    "Germination was scored at 12 h."], 3, 3, head="Candidate conclusions:"),
]

# ---------------------------------------------------------------- F20 leave policy: unless / not ... unless / except where
P20 = """From: Gwen Albright (People Team, Saxfield Logistics)
To: Rafael Onu
Subject: Re: carrying over annual leave

Hi Rafael,

Thanks for your question. Here is the relevant part of the staff handbook (section 5.3):

"{rule}"

From our records: your entitlement this year is 25 days. You have taken 17, and 3 more are booked for 18–20 December, which will leave 5 days untaken at year end. Your manager, Imke Dahl, has not approved a carry-over request for you. You were not on sick leave or parental leave at any point this year.

If you'd like to talk it through, I'm in the office Tuesday to Thursday.

Best,
Gwen"""
R20A = ("Untaken annual leave does not carry over to the next year unless the employee's manager has approved a "
        "carry-over request. Carry-over is capped at 5 days.")
R20B = ("Untaken annual leave carries over to the next year, up to 5 days, unless the employee's manager has "
        "objected in writing.")
R20C = ("No untaken annual leave carries over to the next year, except where the employee was prevented from "
        "taking it by sick leave or parental leave.")
R20D = ("Untaken annual leave of up to 5 days carries over to the next year. Untaken leave beyond 5 days does "
        "not carry over unless the employee's manager has approved it.")
S20 = "Rafael's 5 untaken days will carry over to next year."

F20 = [
Y("F20", "Does the statement follow from Gwen's email?", P20.format(rule=R20A), S20, 0, 1),
Y("F20", "Can the statement be concluded from the email alone?", P20.format(rule=R20B), S20, 0, 3,
  twin=([("has not approved a carry-over request for you",
          "has not objected in writing to your leave carrying over")], 1)),
Y("F20", "Based only on the email, is the statement necessarily true?", P20.format(rule=R20C),
  "None of Rafael's untaken days will carry over to next year.", 1, 2),
C3("F20", "Classify the statement against the email.", P20.format(rule=R20D), S20, "F", 2),
SC("F20", "Which one of the numbered statements is guaranteed by the email?",
   P20.format(rule=R20A),
   ["If Imke approves a carry-over request, Rafael's 5 untaken days will carry over.",
    "Without Imke's approval, none of Rafael's untaken days will carry over.",
    "Rafael was on parental leave this year.",
    "Rafael will have more than 5 untaken days at year end."], 2, 3,
   twin=([("does not carry over to the next year unless the employee's manager has approved",
           "carries over to the next year if the employee's manager has approved")], 1)),
]

# ---------------------------------------------------------------- F21 survey: fewer than half did not / not fewer than half
P21 = """Linthorpe Library Friends · Members' survey 2025: summary for the committee
Prepared by Wendell Asante, membership secretary

The survey went to all 240 members by email and post; 150 returned it. All figures below are out of the 150 who replied.

• Opening hours: {k}
• Café: 90 respondents said they had used the café at least once in the past year; 60 had not.
• Summer fair: 45 respondents said they would volunteer; the rest either said no or left the question blank.
• Newsletter: the paper newsletter should not be scrapped, according to 104 respondents.

Free-text comments were mostly about parking and the lack of a step-free entrance at the side door. The full breakdown is in the attached spreadsheet. The committee is asked to decide whether to repeat the survey in 2027 or move to a shorter annual poll."""
K21A = "fewer than half of respondents did not tick 'yes' to Saturday afternoon opening."
K21B = "not fewer than half of respondents ticked 'yes' to Saturday afternoon opening."
NUMS = [("0", "no respondents"), ("49", "forty-nine respondents"), ("50", "fifty respondents"),
        ("74", "seventy-four respondents"), ("75", "seventy-five respondents, exactly half"),
        ("76", "seventy-six respondents"), ("101", "one hundred and one respondents"),
        ("150", "all one hundred and fifty respondents"),
        ("none of these", "the smallest possible number is not listed")]

F21 = [
Y("F21", "Does the statement follow from the survey summary?", P21.format(k=K21A),
  "More than half of the respondents ticked 'yes' to Saturday afternoon opening.", 1, 3),
Y("F21", "Is the statement entailed by the survey summary?", P21.format(k=K21B),
  "More than half of the respondents ticked 'yes' to Saturday afternoon opening.", 0, 3,
  twin=([("More than half of the respondents ticked", "At least half of the respondents ticked")], 1)),
Y("F21", "If the summary is accurate, does the statement have to hold?", P21.format(k=K21A),
  "105 respondents said they would not volunteer at the summer fair.", 0, 2,
  twin=([("the rest either said no or left the question blank.", "the rest all said no.")], 1)),
C3("F21", "What is the status of the statement, given the survey summary?", P21.format(k=K21A),
   "Fewer than 50 respondents said the paper newsletter should be scrapped.", "F", 3),
ENT("F21", "What is the smallest number of respondents who could have ticked 'yes' to Saturday afternoon opening?",
    P21.format(k=K21A), NUMS, "76", 3, follow_line=False,
    twin=([("fewer than half of respondents did not tick", "fewer than a third of respondents did not tick")],
          "101")),
]

ITEMS = F15 + F16 + F17 + F18 + F19 + F20 + F21
