"""Families F01-F07."""
from common import Y, C3, SC, CNT

# ---------------------------------------------------------------- F01 QC email: not all / none / not one ... failed to
P1 = """From: Ruth Anand <r.anand@tessaly-water.example>
To: Plant 3 shift leads
Subject: Batch 2291 membrane cartridges: hold-test results

Team,

We pulled all twelve cartridges from batch 2291 off line 3 on Monday morning and ran each one through the standard 6-bar hold test. {k} Any cartridge that did not hold is tagged red and goes on the quarantine rack by the east door; please don't move anything on that rack until Kofi has photographed the seals.

For the record, the rig was recalibrated on Friday and Kofi re-ran the reference cartridge before we started, so I'm not treating this as a rig fault. I've opened ticket VM-4410 with Vell Membranes and asked for their end-cap bonding records for the week batch 2291 was made. If anyone sees weeping at the end-caps on a batch 2291 unit still in the field, log it on the usual non-conformance form and copy me in.

Thanks,
Ruth"""
K1_NOTALL = "Not all of them held pressure for the full ten minutes."

F01 = [
Y("F01", "Does the statement follow from Ruth's email?",
  P1.format(k=K1_NOTALL),
  "At least one batch 2291 cartridge did not hold pressure for the full ten minutes.", 1, 1),
Y("F01", "Taking the email as accurate, must the statement be true?",
  P1.format(k=K1_NOTALL),
  "At least one batch 2291 cartridge held pressure for the full ten minutes.", 0, 2,
  twin=([("Not all of them held pressure", "Not all of them failed to hold pressure")], 1)),
C3("F01", "How does the statement relate to the email?",
   P1.format(k=K1_NOTALL),
   "Every batch 2291 cartridge failed to hold pressure for the full ten minutes.", "O", 2),
SC("F01", "Which of the numbered statements follows from the email?",
   P1.format(k="Not one of them failed to hold pressure for the full ten minutes."),
   ["No batch 2291 cartridge held pressure for the full ten minutes.",
    "A fault in the test rig explains the batch 2291 results.",
    "Every batch 2291 cartridge held pressure for the full ten minutes.",
    "Kofi has photographed the seals of the batch 2291 cartridges."], 3, 2,
   twin=([("Not one of them failed to hold pressure", "Not one of them managed to hold pressure")], 1)),
]

# ---------------------------------------------------------------- F02 handover: factive vs non-factive, cleft
P2 = """WARD 6B · NURSING HANDOVER · 07:10
Patient: M. Ostrander, bed 14, 71 y/o, day 3 after left hip replacement

Overnight: pain 3/10 on regular oral analgesia; settled and slept from about 01:00. Observations stable throughout, no oxygen requirement. Drain output 40 ml overnight, serous.
02:40: patient rang the call bell asking for water and a spare pillow; healthcare assistant Dele Aworinde attended. {k}
06:00: wound dressing dry and intact. IV cannula left forearm flushed, site clean, no redness.
For the day team: physio to mobilise with frame after 10:00. FBC and U&E due at 08:00. Review whether IV fluids can stop once oral intake is adequate. Falls risk assessment to be repeated today, as per protocol for all patients over 70.
Family: daughter will phone after 09:00; patient happy for updates to be shared with her."""
S2 = "The bed rails on bed 14 were down when Dele attended the call bell."

F02 = [
Y("F02", "Based only on the handover note, is the statement necessarily true?",
  P2.format(k="Dele did not notice that the bed rails were down."), S2, 1, 2,
  twin=([("did not notice that the bed rails", "did not notice whether the bed rails")], 0)),
Y("F02", "Does the handover note establish the statement?",
  P2.format(k="Dele did not record that the bed rails were down."), S2, 0, 2),
C3("F02", "Classify the statement against the handover note.",
   P2.format(k="Dele did not realise that the bed rails were not raised."),
   "The bed rails on bed 14 were raised when Dele attended the call bell.", "C", 3),
C3("F02", "What is the status of the statement, given the handover note?",
   P2.format(k="Dele did not check whether the bed rails were down."), S2, "O", 2,
   twin=([("did not check whether the bed rails were down", "did not check why the bed rails were down")], "F")),
SC("F02", "Which one of the numbered statements is guaranteed by the handover note?",
   P2.format(k="It was not Dele who noticed that the bed rails were down; the night charge nurse, Ifeoma Blake, "
               "raised them on her 03:15 round."),
   ["Nobody noticed that the rails on bed 14 were down overnight.",
    "Dele noticed that the rails on bed 14 were down.",
    "Someone noticed that the rails on bed 14 were down overnight.",
    "The rails on bed 14 were down for more than half an hour.",
    "Ifeoma raised the rails on bed 14 before 03:00."], 3, 2, head="Candidate conclusions:"),
]

# ---------------------------------------------------------------- F03 tenancy clause: fails to / only if / denying the antecedent
P3 = """HOLLIS & MARR LETTINGS · TENANCY FILE NOTE
Property: Flat 3, 22 Kestle Row. Tenant: Ms Oriane Varga. Fixed term ends 31 March.

Clause 7.4 of the tenancy agreement (as signed):
"{rule}"

File history:
• {d1} Ms Varga emailed the office to say she would be leaving at the end of the fixed term. The email went to lettings@hollismarr.example and was acknowledged the same day by Keiran Moss.
• 24 Mar: check-out inspection booked for 31 March at 10:00.
• 26 Mar: landlord (Mr D. Pell) asked whether the flat could be re-let from 1 April; told that viewings can start once the tenant agrees a time.
• 31 Mar: check-out completed. Inspector notes: minor scuffs to hallway paint, oven clean, all keys returned.

Office practice: an email to the lettings address counts as written notice for the purposes of clause 7.4."""
R3_1 = ("A tenant who fails to give written notice at least 30 days before the end of the fixed term forfeits "
        "the holding deposit.")
R3_2 = ("A tenant forfeits the holding deposit only if the tenant fails to give written notice at least 30 days "
        "before the end of the fixed term.")
R3_3 = ("A tenant who does not give written notice at least 30 days before the end of the fixed term is not "
        "entitled to the return of the holding deposit.")
EARLY, LATE = "14 Feb:", "14 Mar:"

F03 = [
Y("F03", "Taking the file note as accurate, must the statement be true?",
  P3.format(rule=R3_1, d1=EARLY), "Ms Varga does not forfeit the holding deposit.", 0, 2,
  twin=([("A tenant who fails to give", "Only a tenant who fails to give")], 1)),
Y("F03", "Can the statement be concluded from the file note alone?",
  P3.format(rule=R3_1, d1=LATE), "Ms Varga forfeits the holding deposit.", 1, 1),
C3("F03", "How does the statement stand in relation to the file note?",
   P3.format(rule=R3_1, d1=EARLY), "Ms Varga forfeits the holding deposit.", "O", 2),
C3("F03", "Classify the statement against the file note.",
   P3.format(rule=R3_2, d1=EARLY), "Ms Varga forfeits the holding deposit.", "C", 2,
   twin=([("14 Feb:", "14 Mar:")], "O")),
Y("F03", "Would it be a mistake to conclude the statement from the file note?",
  P3.format(rule=R3_3, d1=LATE), "Ms Varga is entitled to the return of the holding deposit.", 1, 2,
  role="neg"),
]

# ---------------------------------------------------------------- F04 forum post: never / not always / always
P4 = """r/ReefKeepingUK · posted by u/tidepool_mae
Title: Clownfish hosting question (long, sorry)

Background: 120-litre mixed reef, running 14 months. Two captive-bred ocellaris clowns, Pip and Tansy, plus a bubble-tip anemone that arrived in June, a small colony of green star polyps and some zoas on the rockwork. Parameters are stable: salinity 1.025, nitrate around 5, temperature 25.5.

{k} In the evenings both clowns usually hang in the flow near the return pump, and at feeding time they dart out for mysis like nothing is wrong. My LFS guy says some pairs take months to host and some never do, and that an anemone that keeps moving doesn't help. It's now wedged in a crevice at the back left.

Is there anything I can do to encourage hosting, or should I just leave them to it? I've read about people sticking photos of clowns in anemones on the glass, but that sounds like a myth.

Edit: thanks for all the replies. I'll stop fiddling with the rock and give it time."""
S4 = "Tansy has been inside the anemone at least once."

F04 = [
Y("F04", "Does the statement follow from the post?",
  P4.format(k="Tansy has never gone into the anemone."), S4, 0, 1, lab="Claim"),
Y("F04", "If everything in the post is accurate, does the statement have to hold?",
  P4.format(k="Tansy has not always stayed out of the anemone."), S4, 1, 2, lab="Claim"),
SC("F04", "Which conclusion can be drawn from the post with certainty?",
   P4.format(k="Pip doesn't always stay out of the anemone, but Tansy always does."),
   ["Pip has been inside the anemone at least once.",
    "Tansy has been inside the anemone at least once.",
    "Both clowns have been inside the anemone.",
    "Pip goes into the anemone every day."], 1, 2, head="Possible conclusions:",
   twin=([("Pip doesn't always stay out of the anemone, but Tansy always does.",
           "Pip always stays out of the anemone, but Tansy doesn't always.")], 2)),
C3("F04", "Given the post, which label fits the statement?",
   P4.format(k="Pip goes into the anemone most mornings; the one who never does is Tansy."),
   "Not every clown in the tank has been inside the anemone.", "F", 2, lab="Claim"),
]

# ---------------------------------------------------------------- F05 museum record: affixal un-/in- negation
P5 = """ASHCOMBE MUSEUM OF WORKING LIFE · COLLECTIONS DATABASE
Object no. AMWL.1987.214
Name: Sampler, embroidered
Materials: wool on linen ground. Dimensions: 38 × 31 cm (sight)

Description: Band sampler with an alphabet in cross stitch, a row of numerals 1–9, a strawberry border and a central verse beginning "When this you see, remember me". The lower edge has been turned under and re-hemmed at some point; the hem thread is a later cotton.

Inscription: {k}
Provenance: Given by Mrs E. Thackery in 1987 with a quilt (AMWL.1987.213). The donor's letter says the sampler "came down through my grandmother's family in Pendlow".
Condition: Colours faded on the right third, consistent with window display. Minor moth loss in the border, stabilised 2004.

Curator's note (K. Wray, 2019): Style and verse are typical of Pendlow schoolroom samplers of c. 1820–1850. {k2}"""
K5A = "none; the sampler is unsigned and undated."
K5A2 = ("An attribution to Hannah Thackery (b. 1831), the donor's great-grandmother, has been proposed but is "
        "unconfirmed.")
K5B = "initials \"H.T.\" worked in the lower right corner. Unlike its companion quilt, the sampler is not undated."
K5B2 = ("The donor's letter calls the piece \"invaluable to the family\". An attribution to Hannah Thackery "
        "(b. 1831) is plausible but unconfirmed.")

F05 = [
Y("F05", "Would it be wrong to conclude the statement from the catalogue record?",
  P5.format(k=K5A, k2=K5A2), "The sampler does not carry its maker's name.", 0, 1, role="neg"),
Y("F05", "Can the statement be concluded from the catalogue record?",
  P5.format(k=K5A, k2=K5A2), "Hannah Thackery did not make the sampler.", 0, 2,
  twin=([("has been proposed but is unconfirmed", "has been proposed but has since been ruled out")], 1)),
C3("F05", "Classify the statement against the catalogue record.",
   P5.format(k=K5A, k2=K5A2), "The museum's record gives no estimate of when the sampler was made.", "C", 2),
Y("F05", "Based only on the record, is the statement necessarily true?",
  P5.format(k=K5B, k2=K5B2), "The sampler bears a date.", 1, 2),
SC("F05", "Which numbered statement is established by the catalogue record?",
   P5.format(k=K5B, k2=K5B2),
   ["The donor regarded the sampler as having little value to the family.",
    "The quilt AMWL.1987.213 bears no date.",
    "Hannah Thackery made the sampler.",
    "The sampler bears no initials."], 2, 3,
   twin=([("Unlike its companion quilt, the sampler", "Like its companion quilt, the sampler")], 0)),
]

# ---------------------------------------------------------------- F06 incident log: not until / without / no ... without
P6 = """INCIDENT INC-40417 · Payroll export failure
Service: Northbeam HR (internal) · Severity: P2 · Status: resolved

Timeline (UTC):
08:02 Nightly payroll export job did not complete; alert raised to on-call engineer Yusuf Carvell.
08:15 Yusuf confirmed the export host was reachable and disk usage normal.
08:31 Job logs show the export stalled waiting on a database lock held on the reporting replica.
09:20 {k}
09:40 Export job re-run manually; completed 09:52. File delivered to the bank's SFTP drop.
10:05 Payroll (Anneke Sol) confirmed receipt; totals match the pre-run summary.

Root cause (draft): a long-running finance report opened a transaction on the replica at 07:48 and held the lock through the export window.
Follow-ups: add a lock timeout to the export job; move finance reports out of the 07:00–09:00 window; add lock monitoring on the replica."""

F06 = [
Y("F06", "Is the statement a valid inference from the incident record?",
  P6.format(k="The reporting replica was not restarted until the finance team confirmed their report could be "
              "abandoned."),
  "The reporting replica was restarted before the finance team confirmed their report could be abandoned.", 0, 1),
Y("F06", "Does the statement follow from the incident record?",
  P6.format(k="The reporting replica was restarted without the finance team being told."),
  "The finance team was never told that the reporting replica had been restarted.", 0, 2),
Y("F06", "Taking the record as accurate, must the statement be true?",
  P6.format(k="Yusuf restarted the reporting replica. Per the change log, no replica restart that morning "
              "happened without a snapshot being taken first."),
  "A snapshot of the reporting replica was taken before Yusuf restarted it.", 1, 2,
  twin=([("happened without a snapshot being taken first", "happened with a snapshot being taken first")], 0)),
SC("F06", "Which of the numbered statements follows from the incident record?",
   P6.format(k="The finance team did not confirm that their report could be abandoned until after the replica "
               "was restarted."),
   ["The finance team confirmed before the restart that their report could be abandoned.",
    "The replica was restarted before any confirmation from the finance team that their report could be "
    "abandoned.",
    "The finance team never confirmed that their report could be abandoned.",
    "The export job was re-run before the replica was restarted."], 2, 3, head="Statements to check:"),
]

# ---------------------------------------------------------------- F07 minutes: neither/nor, not both, abstention
P7 = """GREYFRIARS COURT RESIDENTS' ASSOCIATION
Minutes of committee meeting, 9 September, community room

Present: Adaeze Kiln (chair), Brian Tollemache (treasurer), Carys Venn, Dominik Rusu, Esme Halloran. Apologies: none.

Item 4: proposal to replace the bin-store gates (quote from Farrow Metalworks, £4,180).
Carys presented the quote and photos of the damaged hinges. Brian noted that the reserve fund stands at £11,900 and that the budget allows for one further capital project this year. Dominik asked whether the managing agent would contribute; the chair will write to them.
Vote: {k} The chair declared the proposal carried.

Item 5: garden day. Esme will circulate a sign-up sheet; tools to be borrowed from the allotment society.

Next meeting: 14 October.

Standing orders (printed on every agenda): a proposal is carried if more votes are cast for it than against it. The chair votes only to break a tie. Abstentions are recorded but are not votes."""
K7A = "Carys and Esme voted for the proposal. Neither Brian nor Dominik voted for it."
K7C = "Carys and Esme voted for the proposal. Brian and Dominik did not both vote against it."

F07 = [
Y("F07", "Does the statement follow from the minutes?",
  P7.format(k=K7A), "Brian voted against the proposal.", 0, 2),
Y("F07", "Is the statement entailed by the minutes?",
  P7.format(k=K7A), "Brian and Dominik did not both vote for the proposal.", 1, 2),
Y("F07", "Can the statement be concluded from the minutes alone?",
  P7.format(k=K7C), "At least one of Brian and Dominik did not vote against the proposal.", 1, 2,
  twin=([("At least one of Brian and Dominik did not vote against the proposal.",
          "Neither Brian nor Dominik voted against the proposal.")], 0)),
CNT("F07", "How many of the numbered statements follow from the minutes?",
    P7.format(k=K7A),
    ["Brian did not vote for the proposal.",
     "Brian voted against the proposal.",
     "Esme voted for the proposal.",
     "At least one committee member abstained on item 4."], 2, 3,
    twin=([("The chair votes only to break a tie.", "The chair does not vote.")], 3)),
C3("F07", "What is the status of the statement, given the minutes?",
   P7.format(k=K7C), "The proposal was carried on the chair's casting vote.", "C", 3),
]

ITEMS = F01 + F02 + F03 + F04 + F05 + F06 + F07
