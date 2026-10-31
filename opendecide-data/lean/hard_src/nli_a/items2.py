"""Families F08-F14."""
from common import Y, C3, SC, SUB, ENT

# ---------------------------------------------------------------- F08 claim file: deny / did not deny / lack / fail to
P8 = """CLAIM FILE · Harbourline Mutual · Household · Claim HM-2207-5561
Policyholder: Mr Tobias Quennell, 8 Saltmarsh Lane
Loss reported: escape of water, kitchen, discovered 17 July

Adjuster visit (Priya Oduya, 19 July):
Water staining to the kitchen ceiling and lower cupboards; laminate lifted across approx. 6 m². Leak traced to a failed push-fit joint on the cold feed under the bathroom floor above. {k}

Policy wording extract (Section 3, Escape of water):
"We will pay for loss or damage caused by water escaping from a fixed water installation. We will not pay for the cost of repairing the installation itself, or for damage caused by water escaping gradually over a period of time where you were aware, or should reasonably have been aware, of the leak."

Next steps: flooring quote requested from Brightwell Floors; drying equipment in place since 19 July; moisture readings to be retaken on 26 July."""
K8A = "Mr Quennell denied that he had noticed any damp before 17 July."

F08 = [
Y("F08", "Does the statement follow from the claim file?",
  P8.format(k=K8A), "Mr Quennell had not noticed any damp before 17 July.", 0, 2),
Y("F08", "Based only on the claim file, is the statement necessarily true?",
  P8.format(k="Mr Quennell did not deny that he had noticed damp in the cupboard before 17 July."),
  "Mr Quennell had noticed damp in the cupboard before 17 July.", 0, 2,
  twin=([("did not deny that he had noticed", "admitted that he had noticed")], 1)),
Y("F08", "Is the statement guaranteed by the claim file?",
  P8.format(k="The joint lacked the retaining clip specified by the manufacturer; no sign of tampering."),
  "The failed joint did not have the retaining clip the manufacturer specifies.", 1, 1),
C3("F08", "How does the statement relate to the claim file?",
   P8.format(k=K8A), "Harbourline Mutual will pay for the lifted laminate.", "O", 3),
SC("F08", "Which of the numbered statements follows from the claim file?",
   P8.format(k="Mr Quennell said he had not failed to report damp before; he had simply never seen any."),
   ["Mr Quennell reported damp to Harbourline Mutual before 17 July.",
    "Mr Quennell said he had never seen damp before this claim.",
    "Mr Quennell had never seen damp before this claim.",
    "The adjuster found signs of tampering with the joint."], 2, 3),
]

# ---------------------------------------------------------------- F09 exam notice: only / not only / except / all but
P9 = """KELDON COLLEGE · EXAMINATIONS OFFICE
Notice to Year 13 candidates: Chemistry practical endorsement

The moderation visit on 4 March reviewed the lab books of the eight candidates in set 13C: Amara, Bilal, Corin, Dafydd, Elif, Freya, Gideon and Hana.

{k}

Candidates whose lab books were not signed off must book a catch-up session with Mr Oyelaran before 29 March. Sessions run on Tuesdays and Thursdays after school in Lab 4; bring your lab book, safety glasses and a pen. The endorsement is reported separately from the A-level grade and does not affect it, but most universities offering science courses expect to see it.

Lab books must stay in the lab and must not be taken home."""
CANDS = ["Amara", "Bilal", "Corin", "Dafydd", "Elif", "Freya", "Gideon", "Hana"]

F09 = [
Y("F09", "Does the notice establish the statement?",
  P9.format(k="Not only Gideon's lab book was left unsigned."),
  "At least two lab books from set 13C were not signed off.", 1, 2,
  twin=([("Not only Gideon's lab book was left unsigned.", "Only Gideon's lab book was left unsigned.")], 0)),
Y("F09", "Taking the notice as accurate, must the statement be true?",
  P9.format(k="The moderator did not sign off any lab book that lacked a completed risk assessment. Elif's and "
              "Hana's lab books both had completed risk assessments."),
  "Elif's lab book was signed off.", 0, 2,
  twin=([("did not sign off any lab book that lacked", "signed off every lab book that did not lack")], 1)),
ENT("F09", "Which candidate certainly has to book a catch-up session?",
    P9.format(k="The moderator signed off all but two of the lab books. Gideon's was signed off only after he "
                "redid titration 3 on the day. Amara's was not signed off, and neither Corin's nor Freya's was "
                "left unsigned."),
    [(c, f"the set 13C candidate called {c}") for c in CANDS]
    + [("none of these", "no listed candidate is certain to need a catch-up session")], "Amara", 3,
    twin=([("Amara's was not signed off, and", "Amara's was not left unsigned, and")], "none of these")),
SUB("F09", "Exactly which of the numbered statements follow from the notice?",
    P9.format(k="The moderator signed off every lab book except Gideon's."),
    ["Gideon must book a catch-up session with Mr Oyelaran.",
     "Amara's lab book was signed off.",
     "Gideon's A-level Chemistry grade will be lower because of the endorsement."], (1, 2), 2),
]

# ---------------------------------------------------------------- F10 spec sheet: free from / not free from / no added
P10 = """PRODUCT SPECIFICATION · for retail buyers
Product: Fennick's Oat & Hazel Crunch Bar, 40 g
Supplier: Fennick Bakehouse Ltd, Unit 9 Harlow Mill. Spec version 6, approved by technical manager L. Brandt.

Ingredients: gluten-free oats (38%), hazelnuts (14%), date paste, sunflower oil, rice syrup, puffed rice, sea salt, natural flavouring.
Allergens: contains nuts (hazelnut). {k}
Nutrition per bar: energy 812 kJ / 194 kcal; fat 10.1 g; carbohydrate 22.4 g, of which sugars 9.8 g; fibre 3.0 g; protein 3.9 g; salt 0.12 g.
Claims: no added sugar; suitable for vegans; gluten-free.
Shelf life: 9 months ambient; store in a cool, dry place.
Buyer notes: the previous spec (v5) used a milk chocolate drizzle, which was removed in v6. Outer case holds 24 bars; 60 cases per pallet."""
K10A = ("Free from milk and egg, but not free from sesame: the puffed rice is coated on a line shared with "
        "sesame snaps.")
K10B = "Free from milk, egg and sesame."
K10C = "Free from milk and egg. Made on a line that handles no peanuts, sesame or tree nuts other than hazelnut."

F10 = [
Y("F10", "Does the statement follow from the specification?",
  P10.format(k=K10A), "The bar contains no sugar.", 0, 1),
Y("F10", "Is the statement a valid inference from the specification?",
  P10.format(k=K10A), "The bar is free from at least one of milk and sesame.", 1, 2,
  twin=([("free from at least one of milk and sesame", "free from both milk and sesame")], 0)),
C3("F10", "Classify the statement against the specification.",
   P10.format(k=K10A), "None of the bar's ingredients contains any sugar.", "C", 2),
SC("F10", "Which one of the numbered statements is guaranteed by the specification?",
   P10.format(k=K10B),
   ["The v6 bar contains milk chocolate.",
    "The v5 bar was not free from milk.",
    "The bar is suitable for people who must avoid all nuts.",
    "The bar is not free from sesame."], 2, 2, head="Buyer's questions, as statements:"),
Y("F10", "Would it be wrong to infer the statement from the specification?",
  P10.format(k=K10C), "The bar is free from tree nuts.", 1, 2, role="neg"),
]

# ---------------------------------------------------------------- F11 safety walk: inflammable / non-flammable / unlabelled
P11 = """SITE SAFETY WALK · Unit 4, Carrow Industrial Estate (Delmore Coatings Ltd)
Inspector: Hamza Terrell, H&S adviser · Date: 11 November

Area 3, solvent store (lockable steel cabinet, ventilated):
- 4 × 20 L drums of thinner. {k}
- 2 × 5 L tins of water-based primer, labelled "non-flammable", inside the cabinet.
- 1 × 25 kg sack of absorbent granules, unlabelled, on the cabinet's bottom shelf.

Area 4, loading bay:
- Fire door propped open with a pallet at the time of the visit; operative said it is "normally shut". Door released and closed by the inspector.
- Forklift charging point clear; signage in place.

Actions:
1. Stop propping the fire door; toolbox talk for all bay staff by 18 Nov (owner: J. Pruitt).
2. Label the absorbent sack with its product name (owner: J. Pruitt).
3. Confirm the cabinet's self-closing hinge is serviced annually (owner: site manager).

Site rules extract: no container of flammable liquid may be kept outside a steel cabinet; every container in the store must be labelled with its contents."""
K11A = "The thinner is an inflammable liquid; all four drums were inside the cabinet."
K11B = "The thinner is an inflammable liquid; two of the drums were standing on the floor outside the cabinet."
K11C = ("The drums carry no label; the supplier's data sheet on file describes the thinner as non-flammable. All "
        "four drums were inside the cabinet.")

F11 = [
Y("F11", "Taking the inspection record as accurate, must the statement be true?",
  P11.format(k=K11A), "The thinner in Area 3 is a liquid that does not catch fire easily.", 0, 2),
Y("F11", "Does the statement follow from the inspection record?",
  P11.format(k=K11B), "The site rule on where flammable liquids may be kept was breached in Area 3.", 1, 2,
  twin=([("an inflammable liquid; two of the drums", "a non-flammable liquid; two of the drums")], 0)),
C3("F11", "Given the inspection record, which label fits the statement?",
   P11.format(k=K11A), "Every container in the Area 3 store is labelled with its contents.", "C", 2),
SC("F11", "Which conclusion can be drawn from the inspection record with certainty?",
   P11.format(k=K11C),
   ["At least two kinds of container in Area 3 carry no label.",
    "The data sheet describes the thinner as flammable.",
    "The primer tins are labelled as flammable.",
    "The fire door in Area 4 is normally shut."], 1, 2, head="Possible conclusions:"),
]

# ---------------------------------------------------------------- F12 tribunal: not satisfied that P vs satisfied that not P
P12 = """EASTMERE REGULATORY TRIBUNAL · Decision summary, case ERT/2025/118
Coastline Driving School Ltd (appellant) v. Eastmere Licensing Authority

The Authority suspended the instructor licence of Mr Callum Frere, who teaches for the appellant, after a complaint that he gave a lesson on 9 May while his licence was suspended. The appellant appealed.

Findings: {k}
The Tribunal accepted the Authority's records showing that Mr Frere's licence was suspended from 2 to 16 May for an unpaid renewal fee, and that the fee was paid on 16 May.

Standard of proof: the Authority must prove each fact it relies on, on the balance of probabilities. Where the Authority fails to prove a fact, the Tribunal proceeds as if that fact is not established; this is not a finding that the fact is untrue.

Outcome: {out}
Costs: each party to bear its own."""
ALLOWED = "Appeal allowed; suspension lifted."
DISMISSED = "Appeal dismissed."
S12 = "The Tribunal found that the lesson on 9 May did not take place."

F12 = [
Y("F12", "Does the decision summary establish the statement?",
  P12.format(k="The Tribunal was not satisfied that the lesson on 9 May took place.", out=ALLOWED), S12, 0, 2),
Y("F12", "Is the statement guaranteed by the decision summary?",
  P12.format(k="The Tribunal was satisfied that the lesson on 9 May did not take place.", out=ALLOWED),
  S12, 1, 1),
Y("F12", "Based only on the decision summary, is the statement necessarily true?",
  P12.format(k="The Authority did not fail to prove that the lesson on 9 May took place.", out=DISMISSED),
  "The Tribunal treated the 9 May lesson as established.", 1, 2,
  twin=([("The Authority did not fail to prove", "The Authority failed to prove"),
         ("Outcome: Appeal dismissed.", "Outcome: Appeal allowed; suspension lifted.")], 0)),
C3("F12", "How does the statement stand in relation to the decision summary?",
   P12.format(k="The Tribunal did not accept Mr Frere's evidence that no lesson took place on 9 May, but it also "
                "found the complainant's account unreliable.", out=ALLOWED),
   "Mr Frere's evidence was that no lesson took place on 9 May.", "F", 2),
SC("F12", "Which of the numbered statements follows from the decision summary?",
   P12.format(k="The Tribunal did not find that Mr Frere taught while suspended, because it was not satisfied "
                "that the lesson on 9 May took place.", out=ALLOWED),
   ["Mr Frere's licence was not suspended on 9 May.",
    "Mr Frere did not teach while his licence was suspended.",
    "Mr Frere's renewal fee was still unpaid on 9 May.",
    S12], 3, 2),
]

# ---------------------------------------------------------------- F13 release notes: no longer / still / not yet / deprecated
P13 = """## Mossgate CLI · release notes

### 4.2.0 (2025-08-14)
- Added `mossgate sync --dry-run`.
- `mossgate push` now retries failed uploads up to 3 times.
- {k}
- Fixed: progress bar flickered on Windows terminals.

### 4.1.0 (2025-05-02)
- The `--legacy-auth` flag is deprecated and prints a warning when used. It will be removed in a future major release.
- `mossgate init` now creates a `.mossignore` file by default.
- Fixed: `mossgate pull` ignored the `--quiet` flag.

### Support policy
Deprecated features keep working until they are removed. Features are removed only in major releases (5.0.0, 6.0.0, …); minor and patch releases never remove a feature. The current release line is 4.x."""
K13B = "`--legacy-auth` still prints a deprecation warning; its removal has not yet been scheduled."

F13 = [
Y("F13", "If the release notes are accurate, does the statement have to hold?",
  P13.format(k=K13B), "`--legacy-auth` still works in 4.2.0.", 1, 2),
Y("F13", "Does the statement follow from the release notes?",
  P13.format(k="`--legacy-auth` is no longer deprecated: it is now the recommended path for air-gapped installs."),
  "In 4.2.0, `--legacy-auth` prints a deprecation warning when used.", 0, 2),
C3("F13", "Classify the statement against the release notes.",
   P13.format(k="`--legacy-auth` no longer prints a warning when used."),
   "`--legacy-auth` is no longer deprecated.", "O", 3),
SC("F13", "Which one of the numbered statements is guaranteed by the release notes?",
   P13.format(k=K13B),
   ["`--legacy-auth` will not be removed in 4.3.0.",
    "`--legacy-auth` will be removed in 5.0.0.",
    "`--legacy-auth` is no longer deprecated."], 1, 2, head="Statements to check:"),
]

# ---------------------------------------------------------------- F14 forecast with defined scale: not likely vs unlikely
P14 = """HARLAND COAST MARINE FORECAST · issued 05:00 Saturday
Area: Harland Head to Porth Isel, out to 12 nautical miles

Terms used in this forecast (Harland Met Office standard):
• "likely" means a probability of 60% or more
• "unlikely" means a probability below 20%
• "possible" means a probability of at least 20% but below 60%
• wind speeds are mean speeds; gusts are stated separately

Forecast for today:
Wind southwest 4 to 5, increasing 6 at times later, gusts to 34 knots in the afternoon.
Sea state moderate, becoming rough for a time.
Weather: showers, heavy at times. {k}
Visibility: good, occasionally moderate in showers.

Outlook for Sunday: wind west 5 to 6, decreasing 4 later. Showers dying out by evening.
Small craft advisory in force from 12:00 today until 06:00 Sunday."""
BANDS = [
    ("below 20%", "the forecast commits to a chance of thunder below 20%"),
    ("20% to under 60%", "the forecast commits to a chance of thunder of at least 20% but below 60%"),
    ("60% or more", "the forecast commits to a chance of thunder of 60% or more"),
    ("below 60%", "the forecast commits only to a chance of thunder below 60%"),
    ("20% or more", "the forecast commits only to a chance of thunder of 20% or more"),
    ("no range at all", "nothing in the forecast limits the chance of thunder"),
]

F14 = [
Y("F14", "Is the statement entailed by the forecast?",
  P14.format(k="Thunder is not likely."), "The forecast puts the chance of thunder below 20%.", 0, 3,
  twin=([("Thunder is not likely.", "Thunder is unlikely.")], 1)),
Y("F14", "Does the statement follow from the forecast?",
  P14.format(k="Thunder is not unlikely."), "The forecast puts the chance of thunder at 60% or more.", 0, 3),
Y("F14", "Can the statement be concluded from the forecast alone?",
  P14.format(k="Thunder is not unlikely."), "The forecast puts the chance of thunder at 20% or more.", 1, 2),
ENT("F14", "Which is the narrowest range for the chance of thunder that the forecast commits to?",
    P14.format(k="Thunder is not likely."), BANDS, "below 60%", 3, follow_line=False,
    twin=([("Thunder is not likely.", "Thunder is not unlikely.")], "20% or more")),
C3("F14", "What is the status of the statement, given the forecast?",
   P14.format(k="Hail is not possible; thunder is possible."),
   "The forecast puts the chance of hail below 20%.", "O", 3),
]

ITEMS = F08 + F09 + F10 + F11 + F12 + F13 + F14
