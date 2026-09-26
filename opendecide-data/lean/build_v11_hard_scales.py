"""v0.11 HARD items, domain "scales": ordinal classification by DEFINED LEVELS.

Every item gives a written scale (4-6 levels, one definition per level) plus any scoring rules, and a case
(email, ticket, chart note, audit extract, log...). The question asks for the level (choice) or whether a
named level applies (yes/no). Items are built so that the gold follows only from careful reading of the
definitions/rules (boundary cases, precedence rules, counting rules, exclusions), and a keyword-matcher is
pulled toward a wrong level.

All text is authored by Claude (the teacher) for this file; no external data, no external model calls.
No held-out files are read. Deterministic (seed 20261001); re-runnable:
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_v11_hard_scales.py
Writes data/v11_parts/hard/scales.jsonl and data/v11_parts/hard/scales.blind.jsonl (gold removed).
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

SEED = 20261001
HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "data" / "v11_parts" / "hard"
NONE = "none of these"

S: dict[str, dict] = {}
ITEMS: list[dict] = []


def cardify(pairs):
    return "\n".join(f"- {o}: {d}" for o, d in pairs)


def scale(key, rules, pairs):
    S[key] = {"rules": rules.strip(), "pairs": pairs}


def item(sc, qtype, case, instr, gold, diff, twin=None, twin_gold=None, levels=None, none=None,
         cases=None, fixed=False):
    ITEMS.append(dict(sc=sc, qtype=qtype, case=case.strip(), instr=instr, gold=gold, diff=diff, twin=twin,
                      twin_gold=twin_gold, levels=levels, none=none, cases=cases, fixed=fixed))


# =====================================================================================================
# 1. Trademark distinctiveness spectrum
# =====================================================================================================
scale("tm", """
Clearance Manual, Part 4 (classification notes)
4.1 Classify a mark only in relation to the goods or services named in the application.
4.2 Misspellings, phonetic spellings, hyphenated and run-together forms are classified exactly as the ordinary words they represent.
4.3 A word from a language spoken at home by at least 10% of the relevant market is translated into English before classification. Words from any other language are treated as having no meaning to the relevant market.
4.4 A combination of elements is classified by the impression of the whole. A combination of descriptive terms stays descriptive unless the whole creates a distinct, incongruous meaning, in which case it is suggestive.
4.5 Use of a term by competitors or retailers as the ordinary name of the product type is strong evidence that the term is generic.
""", [
    ("generic", "The term is the ordinary name of the goods or services themselves, or of the category they belong to, as the relevant public would use it."),
    ("descriptive", "The term directly and immediately tells the relevant public a quality, ingredient, feature, function, purpose or intended user of the goods or services; no imaginative step is needed."),
    ("suggestive", "The term relates to the goods or services, but a consumer needs imagination, thought or a mental leap to connect it to their nature or qualities."),
    ("arbitrary", "The term is an existing word or phrase with an established meaning to the relevant public, used for goods or services it has no connection with."),
    ("fanciful", "The term has no meaning to the relevant public other than as a mark: it was invented, or its only meaning is in a language that rule 4.3 does not require translating."),
])

item("tm", "choice", """
From: Ines Okafor (paralegal)
To: Clearance team
Subject: New search request - SECCO

Client Harbrook Home Goods wants to file SECCO for portable electric dehumidifiers for basements and laundry rooms. Sales will be limited to the Republic of Castria. The client's own market survey says 23% of Castrian households speak Italian at home; "secco" is the Italian word for "dry". Marketing plans to print the mark in a stylised serif font next to a water-droplet logo. No third-party SECCO marks turned up in the register search. Please classify before we draft the search report.
""", "Where does SECCO fall on the distinctiveness spectrum for these goods?", "descriptive", 2,
     twin=[("23% of Castrian households", "4% of Castrian households")], twin_gold="fanciful")

item("tm", "choice", """
EXAMINER WORKSHEET - Application 26-118804
Mark: KOLDKUP (standard characters)
Goods: Class 21 - double-walled insulated tumblers and travel cups that keep beverages cold for up to 24 hours.
Applicant: Bramblefield Outdoor Co.
Evidence of record: The applicant's website headline reads "Your drink, still cold at sundown." A retailer search across four major outdoor stores shows competing products listed as "insulated tumblers" or "travel tumblers"; no retailer or competitor uses "cold cup" as a product name or category heading.
Applicant's argument: the K-spelling makes the mark "coined and inherently fanciful".
""", "How should the examiner classify KOLDKUP for the listed goods?", "descriptive", 2,
     twin=[('no retailer or competitor uses "cold cup" as a product name or category heading.',
            'two of the four stores file these products under a category heading titled "Cold Cups", and three competitors sell theirs as "the original cold cup".')],
     twin_gold="generic")

item("tm", "choice", """
Client intake note - Matter 4471 (Casa Moreira Foods)
Proposed mark: FAROL
Goods: frozen pizzas and frozen flatbreads.
Market: sold only in the southern provinces of Castria, where a 2025 census found that 18% of residents speak Portuguese at home.
Meaning: "farol" is the Portuguese word for "lighthouse". The founder picked it because the family's first restaurant stood opposite a harbour lighthouse. The packaging shows no lighthouse, and the product line has no nautical or regional theme.
Question from the client: "We think this reads as a made-up word to our customers, so it should be the strongest kind of mark. Can you confirm?"
""", "Which category of distinctiveness does FAROL belong to for frozen pizzas?", "arbitrary", 2)

item("tm", "choice", """
StudyBoard > Trademark Law II > Practice set 7
Post by kestrel_jd:
The answer key for Q3 is missing. Facts: Velo Rapid Ltd provides same-day parcel courier services within city limits and wants to register CHEETAH for "courier and parcel delivery services". "Cheetah" is the everyday English name of the big cat, known as the fastest land animal. The applicant's vans carry a spotted livery and its slogan is "Across town before your coffee cools." No competing courier uses the word, and nothing in the record suggests couriers are called cheetahs in the trade.
Half my group says the word has nothing to do with parcels; the other half disagrees. Where does it sit?
""", "Under the manual's definitions, what is the correct classification of CHEETAH for courier services?",
     "suggestive", 2)

item("tm", "choice", """
Memo to file - Gallow & Pike LLP
Client: Tindermoor Creamery
Proposed mark: FROZEN FIRE
Goods: ice cream flavoured with chili and cinnamon.
Notes: "Frozen" on its own would describe ice cream. "Fire" is widely used in food marketing to mean very spicy, so on its own it would describe the chili flavour. In a consumer panel (n=40), most panelists described the name as "a contradiction". No competitor uses "frozen fire".
Action: classify for the search report.
""", "Classify FROZEN FIRE for the client's ice cream.", "suggestive", 3)

item("tm", "choice", """
Portfolio review - Aldmere Brands Group, Castria filings
Market facts: Castria's relevant market is multilingual. Home languages by share of households: English 61%, Italian 14%, Portuguese 11%, Occitan 0.6%, all others under 5% each.
Counsel wants to know which of the pending marks listed in the card is fanciful for its goods, so that it can be featured in the investor deck as a "strong mark". The search notes for each mark are summarised in the card.
""", "Which pending mark qualifies as fanciful for its goods?", "ORBELLE for scented candles", 3,
     cases=[
         ("DRYVENT for moisture-wicking hiking socks", "a run-together spelling of \"dry vent\"; the socks have ventilation panels and dry quickly."),
         ("ORBELLE for scented candles", "the word's only recorded meaning is \"little ball\" in Occitan; it has no meaning in English, Italian or Portuguese."),
         ("VELOCE for bicycle helmets", "the Italian word for \"fast\"."),
         ("SATURNO for dishwasher detergent", "the Italian and Portuguese word for the planet Saturn."),
     ], none="None of the listed marks is fanciful for its goods.")

item("tm", "noul", """
Email from: Paulo Dranet (brand manager, Glenmarsh Household)
We've shortlisted CITRUS as the name for our new lemon-and-lime scented washing-up liquid. It's a normal English word, nobody in our category is using it as a brand, and the legal team at my last company told me that ordinary dictionary words used as brands are the "arbitrary" kind, which are strong. Before I take this to the naming committee: can you confirm where it sits?
""", "Would CITRUS be classified as an arbitrary mark for this product?", 0, 2,
     twin=[("lemon-and-lime scented washing-up liquid", "cloud backup software for small offices")], twin_gold=1)

item("tm", "noul", """
Office action response draft (excerpt)
Applicant: Pellow Baby Ltd. Mark: EEZEFOLD. Goods: lightweight baby strollers that collapse with one hand.
"The mark EEZEFOLD is a coined term that appears in no dictionary. The doubled vowels and the letter Z give it a unique visual identity. The mark has no meaning in any language spoken in Castria. Applicant therefore submits that the mark is inherently distinctive at the highest point of the spectrum."
Examiner's margin note: check the applicant's characterisation before replying.
""", "Is EEZEFOLD correctly classified as fanciful for these strollers?", 0, 2)

# =====================================================================================================
# 2. Incident severity (SaaS)
# =====================================================================================================
scale("sev", """
Parcelwise Severity Policy v6 - rating notes
(1) Rate every incident at its worst point of impact, even if it was mitigated quickly.
(2) A workaround counts only if affected customers could reasonably discover and use it on their own, without contacting support.
(3) "Active customers" means accounts with at least one login in the previous 30 days.
(4) A full outage of a production service across a whole region is SEV-1 regardless of duration.
(5) Core workflows are: login, shipment creation, label printing, checkout and payment.
(6) If an incident meets the criteria of more than one level, use the most severe.
""", [
    ("SEV-1", "A production service is fully unavailable across a region, or customer data is confirmed to have been exposed to an unauthorised party or permanently lost."),
    ("SEV-2", "A core workflow fails for 10% or more of active customers with no workaround, or customer data is suspected, but not confirmed, to have been exposed."),
    ("SEV-3", "A customer-facing feature fails or is degraded but a workaround exists, or a core workflow fails for fewer than 10% of active customers."),
    ("SEV-4", "Impact limited to internal users or non-production environments, or a cosmetic customer-facing defect that blocks no task."),
    ("SEV-5", "No impact occurred: a near miss, an alert handled before any effect, or planned precautionary work."),
])

item("sev", "choice", """
Postmortem draft - INC-5122 "Checkout 502s after cache change"
Timeline (UTC)
14:02  Config change to the pricing cache deployed to production.
14:05  Error rate on POST /checkout climbs; failures are concentrated on accounts on the "multi-warehouse" plan.
14:20  On-call confirms the affected accounts: 14% of active customers. No other workflow affected.
14:31  Support discovers that checkout still works if the customer switches their default warehouse to "single". Support agents start sharing this step in replies to incoming tickets; nothing is posted in the product or the help centre.
14:42  Config reverted; error rate back to baseline.
Customer tickets: 212. Revenue impact under review.
""", "What severity should INC-5122 carry under policy v6?", "SEV-2", 3,
     twin=[("14% of active customers", "7% of active customers")], twin_gold="SEV-3")

item("sev", "choice", """
Security channel, #inc-5140
Dana Ruiz (SecEng), 09:14: Heads-up. A snapshot of the staging database was copied to a storage bucket that had public read access for about 19 hours. It's staging, but last month's refresh loaded it with a straight copy of production customer records (names, delivery addresses, phone numbers) because the masking job failed silently.
Marek Hale (Infra), 09:22: Bucket is locked down now.
Dana Ruiz, 09:40: Pulled the bucket access logs. Two full downloads of the snapshot file from an IP range we don't recognise, at 02:11 and 02:13.
Marek Hale, 09:41: Should I open this as SEV-4 since it's staging only?
""", "Which severity level applies to this incident?", "SEV-1", 3,
     twin=[("Pulled the bucket access logs. Two full downloads of the snapshot file from an IP range we don't recognise, at 02:11 and 02:13.",
            "Access logging was never enabled on that bucket, so we can't tell whether anyone downloaded the file.")],
     twin_gold="SEV-2")

item("sev", "choice", """
Incident summary - INC-5157
Service: Tracking API (production), EU-West region
What happened: A deploy at 11:48 shipped a malformed routing table. Every tracking request in EU-West returned HTTP 503 until the automatic canary rollback completed at 11:51. Other regions were unaffected. Shipment creation, labels and checkout do not depend on the Tracking API and kept working.
Customer impact: tracking pages and webhook updates for EU-West customers were unavailable for roughly three minutes; delayed webhooks were replayed by 12:10. Four support tickets.
Proposed rating by the service owner: "SEV-4 at most - it was three minutes and fully self-healed."
""", "Rate INC-5157 on the severity scale.", "SEV-1", 2)

item("sev", "choice", """
On-call handover note, Saturday night shift
- 22:40 Alert "db-primary-02 disk 95%". Cause: a runaway audit-log table growing about 4 GB/hour after Thursday's release.
- 22:52 Expanded the volume online (no restart), then truncated the audit table's debug partition per runbook RB-17.
- 23:05 Disk at 61% and stable. Checked dashboards: no failed requests, no latency change and no errors in any customer-facing or internal service at any point. Nobody outside on-call noticed.
- Ticket opened for the audit-log bug; fix goes out in Monday's release.
Please rate this for the weekly review.
""", "What severity should the weekly review record for this event?", "SEV-5", 2)

item("sev", "noul", """
Bug report forwarded to incident triage
Reporter: Hollis Grain Co. (customer)
"Since yesterday's update the invoice PDFs you generate for us show your logo stretched sideways, and the footer text overlaps the page number. All the figures, line items and totals are correct and we've been able to send them to our accounts team as normal. It just looks unprofessional."
Engineering check: reproduced on all accounts using the "Classic" invoice template (about 30% of active customers). Invoice data and downloads are unaffected. Fix scheduled for Thursday.
""", "Is SEV-4 the right severity for this issue?", 1, 2)

item("sev", "noul", """
INC-5163 review notes
- 08:00 An identity-provider certificate rotation breaks SSO login for customers who use Corvid ID. Affected: 11% of active customers.
- 08:10 Support switches on the "Email me a sign-in link" option on the login page (normally turned off) and adds a banner telling Corvid ID users to use it. The email-link option works for every account.
- 08:10-10:05 Affected customers log in through email links; ticket volume drops back to normal.
- 10:05 Certificate fixed; SSO restored.
Duty manager's draft rating: SEV-3, "because a workaround was available on the login page".
""", "Is SEV-2 the correct rating for INC-5163?", 1, 3,
     twin=[('08:10 Support switches on the "Email me a sign-in link" option on the login page (normally turned off) and adds a banner telling Corvid ID users to use it.',
            '08:10 Support adds a banner pointing Corvid ID users to the "Email me a sign-in link" option, which has always been shown on the login page.')],
     twin_gold=0)

item("sev", "choice", """
Weekly incident review - agenda item 3
Four incidents from last week were logged without a severity. Before the report goes to the leadership team, the review chair wants to know which one, if any, should carry SEV-2. The incident summaries are in the card; assume each summary is complete and accurate.
""", "Which incident, if any, should be rated SEV-2?", "INC-4413", 3,
     cases=[
         ("INC-4410", "Shipment creation failed for every test account in the staging environment for a full day; production was unaffected."),
         ("INC-4413", "An external researcher reported that one API endpoint may return other customers' delivery addresses; engineering has not yet reproduced it or ruled it out."),
         ("INC-4417", "The payment page returned errors for every customer in the APAC region for 90 seconds during a database failover."),
         ("INC-4421", "Label printing failed for 6% of active customers for four hours, with no workaround."),
     ], none="None of the listed incidents meets SEV-2.")

# =====================================================================================================
# 3. Emergency triage acuity
# =====================================================================================================
scale("tr", """
Kestrel Valley ED - Five-Tier Acuity Guide, quick reference
Resources (count types, not items): all laboratory tests together = 1; all plain X-rays together = 1; CT, MRI or ultrasound = 1; IV fluids = 1; IV, IM or nebulised medication = 1; specialty consultation = 1; simple procedure (laceration repair, urinary catheter) = 1; complex procedure (procedural sedation) = 2.
Not resources: history and physical exam; point-of-care tests (fingerstick glucose, urine dipstick, rapid strep swab); oral medication; tetanus immunisation; prescriptions; simple wound care (dressing, recheck); crutches, splints, slings; a phone call to the family doctor.
Vital-sign rule: an adult (18+) who would otherwise be Tier 3 is assigned Tier 2 if heart rate > 100, respiratory rate > 20, or SpO2 < 92%. The rule does not apply to any other tier.
""", [
    ("Tier 1", "Needs an immediate life-saving intervention now (airway or breathing support, emergency medication, defibrillation), or is unresponsive."),
    ("Tier 2", "Does not need an immediate life-saving intervention but should not wait: a high-risk presentation, new confusion, lethargy or disorientation, or severe pain or distress (7/10 or higher) consistent with clinical findings."),
    ("Tier 3", "Not Tier 1 or 2, and expected to need two or more resources."),
    ("Tier 4", "Not Tier 1 or 2, and expected to need exactly one resource."),
    ("Tier 5", "Not Tier 1 or 2, and expected to need no resources."),
])

item("tr", "choice", """
Triage note 14:22
34 M, twisted right ankle playing five-a-side football 1 h ago. Walked in with a limp; able to bear weight for 4 steps. Swelling and tenderness over the lateral malleolus and the base of the 5th metatarsal. Pain 6/10. No other injury, no head strike. Alert, oriented.
HR 88, RR 16, BP 132/80, SpO2 98%, T 36.8.
Anticipated care: X-ray of the ankle and X-ray of the foot; oral ibuprofen at triage; ankle splint and crutches if no fracture; discharge with sports-medicine follow-up.
""", "What acuity tier should this patient be assigned?", "Tier 4", 3,
     twin=[("oral ibuprofen at triage", "IM ketorolac at triage per physician order")], twin_gold="Tier 3")

item("tr", "choice", """
ED triage - 03:40
58 F with 2 days of lower abdominal pain, worse on the left, one episode of vomiting, no blood in stool. Pain 5/10, sitting comfortably, answering questions appropriately. History: diverticulitis in 2023. Screening for high-risk features: negative.
Vitals: HR 108, RR 18, BP 128/76, SpO2 97%, T 38.1.
Expected work-up: bloods (FBC, U&E, CRP, lactate), CT abdomen/pelvis with contrast, IV fluids, and IV antibiotics if the CT confirms diverticulitis.
""", "Assign the triage tier for this patient.", "Tier 2", 3,
     twin=[("HR 108", "HR 96")], twin_gold="Tier 3")

item("tr", "choice", """
Triage note 19:05
22 F, sore throat and fever for 3 days, painful swallowing, no drooling, no trouble breathing, voice normal, tolerating fluids. Pain 5/10. No rash.
HR 94, RR 16, BP 118/72, SpO2 99%, T 38.4.
Plan per standing order: rapid strep swab at triage; if positive, a prescription for oral penicillin; paracetamol by mouth now. Physician to examine. Patient is asking for a work note.
""", "Which tier does the guide give this patient?", "Tier 5", 2)

item("tr", "choice", """
Triage note 10:48
71 M brought in by his daughter, who says he has been "not himself since breakfast". He walked in unaided and is chatting pleasantly, but states that the year is 1998 and believes he is at the post office. The daughter reports he was fully oriented and doing his own crossword yesterday. No falls, no headache reported, no weakness noted at triage. Fingerstick glucose 6.1 mmol/L.
HR 78, RR 14, BP 146/84, SpO2 97%, T 36.6. Pain 0/10.
""", "Under the Five-Tier Acuity Guide, what is this patient's tier?", "Tier 2", 2)

item("tr", "noul", """
Triage note 16:30
40 F, cut to the palm side of her left forearm on a kitchen knife while washing up, 20 min ago. Wound about 3 cm, edges gaping, bleeding controlled with a pressure dressing. Full movement and normal sensation in the hand and fingers. Last tetanus booster unknown; will give at triage. Pain 4/10. No anticoagulants.
HR 84, RR 16, BP 124/78, SpO2 99%.
Anticipated: wound irrigation and suture repair; tetanus immunisation; discharge with a wound-care leaflet.
""", "Would Tier 4 be the correct acuity for this patient?", 1, 3,
     twin=[("Full movement and normal sensation in the hand and fingers.",
            "She cannot flex the tip of her index finger; the physician will request a hand-surgery consult before repair.")],
     twin_gold=0)

item("tr", "noul", """
Triage note 07:12
64 M, central chest pressure radiating to the left arm since 06:30, pain 8/10, sweaty and pale. Alert, speaking in full sentences, airway clear. History: hypertension, smoker.
HR 96, RR 20, BP 150/92, SpO2 97% on room air, T 36.7.
ECG done at triage within 10 minutes; awaiting the physician's read. Aspirin given orally per protocol.
""", "Does this patient meet the criteria for Tier 1?", 0, 2)

item("tr", "choice", """
Paediatric triage note 21:15
2-year-old girl, tugging at her right ear and crying since the afternoon; mild cold for 3 days. Drinking well, wet nappies as usual, playful between crying spells, smiling at the nurse. Pain on the FLACC scale: 3/10.
HR 130, RR 28, SpO2 98%, T 38.2 (tympanic).
Plan: physician exam of ears and throat; oral ibuprofen now; likely a prescription for oral antibiotics or watchful-waiting advice.
""", "What is the correct triage tier for this child?", "Tier 5", 3)

item("tr", "choice", """
Triage note 12:03
29 M, came off his bike onto a kerb; 3 cm gash on the right shin, bleeding controlled, no other injuries, helmet on, no head strike, walking normally. Very anxious about needles, shaking and breathing fast while describing the fall; calmer after a few minutes. Pain 3/10. Tetanus up to date.
HR 115, RR 22, BP 138/84, SpO2 99%.
Anticipated: wound irrigation and suture repair; discharge.
""", "Which acuity tier fits this patient at triage?", "Tier 4", 3)

item("tr", "choice", """
The charge nurse is re-checking four patients who were triaged during a busy period. Each one is summarised in the card. Vital signs are normal for age unless stated, and none of them has a high-risk presentation, confusion, or severe pain or distress.
""", "Which of these patients should be assigned Tier 3?", "Bed B", 3,
     cases=[
         ("Bed A", "45-year-old with a suspected urinary tract infection needing a urine dipstick, blood tests and a prescription for oral antibiotics."),
         ("Bed B", "30-year-old with a dislocated shoulder needing an X-ray and reduction under procedural sedation."),
         ("Chair 7", "52-year-old with a wrist injury needing two views of the wrist plus a scaphoid X-ray series, and a splint."),
         ("Chair 9", "19-year-old with a sprained knee needing crutches, oral pain relief and a recheck."),
     ], none="None of the four patients should be Tier 3.")

# =====================================================================================================
# 4. Reading difficulty bands
# =====================================================================================================
scale("rd", """
Tallowbrook Press - Leveled Library banding rules
Measures: (a) average sentence length in words; (b) multisyllabic words (three or more syllables) per 100 words; (c) structure, as described in each band.
A title is placed in the lowest band whose limits it meets on every measure. Each band also permits every structural feature allowed in the bands below it. Structural features count as measures in their own right. Figures are taken from the full-text analysis, not from the sample page.
""", [
    ("Band A", "Average sentence length 7 words or fewer; at most 2 multisyllabic words per 100 words; a single linear storyline with no dialogue."),
    ("Band B", "Average sentence length 10 words or fewer; at most 5 multisyllabic words per 100 words; a single linear storyline; simple dialogue allowed."),
    ("Band C", "Average sentence length 14 words or fewer; at most 9 multisyllabic words per 100 words; chapters and at most one flashback allowed."),
    ("Band D", "Average sentence length 18 words or fewer; at most 14 multisyllabic words per 100 words; multiple viewpoints, several flashbacks or non-linear structure allowed."),
    ("Band E", "Exceeds a Band D limit on any measure."),
])

item("rd", "choice", """
Acquisitions email - "Pip and the Puddle Boat" (picture book, 640 words)
Hi Oona, the full-text report is back: average sentence length 6.8 words; 4.1 multisyllabic words per 100 words. It's one straight-through story about Pip building a boat, with no jumps in time. There are a few lines of speech between Pip and her grandad ("Will it float?" said Pip.). The sample page we sent to the sales team came out at 5.2 words per sentence and 1.5 multisyllabic words per 100. Can you confirm the band so I can brief the designer? - Callum
""", "Which band should 'Pip and the Puddle Boat' be placed in?", "Band B", 2)

item("rd", "choice", """
Banding worksheet - "The Salt Road Summer" (chapter book, 11,200 words)
Full-text analysis: average sentence length 12.9 words; multisyllabic words 8.7 per 100.
Structure notes from the editor: nine chapters, told throughout by the narrator, twelve-year-old Maren. The main story runs over one summer. Chapter 3 opens with two pages recalling the storm that sank her father's boat years earlier; chapter 7 returns to the same storm night through Maren's memory of the hospital. Otherwise events are told in order.
Sales would prefer the lower band because it sells better to schools.
""", "What band does this title receive under the banding rules?", "Band D", 3,
     twin=[("; chapter 7 returns to the same storm night through Maren's memory of the hospital.", ".")],
     twin_gold="Band C")

item("rd", "choice", """
Series planning note - "Field Guides for Young Naturalists: Wetlands"
Nonfiction title, 9,400 words, linear structure (one chapter per habitat, no narrative time shifts, a single authorial voice).
Full-text analysis: average sentence length 17.5 words; multisyllabic words 15.2 per 100 (many species and science terms such as "amphibian", "invertebrate" and "photosynthesis"). The editor proposes Band D "since the average sentence is under 18 words".
Please record the band for the catalogue.
""", "Record the correct band for this title.", "Band E", 2)

item("rd", "noul", """
Reader's report - "Moth Hollow Mysteries #2" (8,300 words)
Full-text analysis: average sentence length 9.4 words; multisyllabic words 8.9 per 100.
Structure: eleven short chapters, all told in order from Tamsin's point of view. Lots of dialogue between Tamsin and her cousin. No flashbacks or time jumps.
Question from marketing: the first book in the series was Band C; can this one be listed in the same band?
""", "Should this title be placed in Band C?", 1, 2,
     twin=[("8.9 per 100", "9.3 per 100")], twin_gold=0)

item("rd", "choice", """
Message from the analysis contractor
"Our tool crashed on 'Lantern Street Cats', so I counted the full text by hand (it's short). Totals: 412 words, 38 sentences, 27 words of three or more syllables. A single storyline, told in order, with some simple dialogue between the cats. No chapters."
The production editor needs the band before the proof deadline.
""", "Based on the hand count, which band applies to 'Lantern Street Cats'?", "Band C", 3)

# =====================================================================================================
# 5. Code-review risk tiers
# =====================================================================================================
scale("cr", """
Loomwright Engineering - Change Risk Tiers (review policy 3.2)
- A change is rated at the highest tier of anything it touches.
- Files are judged by what they do at build, CI or run time, not by their path, name or extension.
- Feature flags, dark launches and percentage rollouts never lower a tier.
- Sensitive areas: authentication and authorisation; payments; cryptography and key handling; personal-data handling; public API contracts (request/response shapes documented for customers).
""", [
    ("R0", "Only documentation, comments or other text that is never executed as code (in CI or anywhere else) and never loaded by production at run time."),
    ("R1", "Only tests, CI jobs that do not deploy, or developer tooling; nothing that changes what runs in production."),
    ("R2", "Production code or configuration that touches no sensitive area."),
    ("R3", "Production code or configuration that touches a sensitive area."),
    ("R4", "An R3 change that is irreversible once deployed (destructive schema migration, data deletion, key rotation that discards old keys), or any change to the deploy pipeline's own approval or review checks."),
])

item("cr", "choice", """
PR #8812 "Docs: refresh quickstart examples"
Author: @tamsin-o
Files changed:
  README.md (+14 -9)
  docs/quickstart.md (+31 -22)
Description: Updates the Python snippets in the quickstart to the new client syntax. Note for reviewers: every fenced code block in docs/*.md is collected and run by the doc-examples job in CI on each PR, so the old snippets were failing there. The docs site is published separately from the product, and nothing under docs/ ships in the production image.
Reviewer bot: "Suggested tier: R0 (documentation only)".
""", "What risk tier should PR #8812 receive?", "R1", 3,
     twin=[("every fenced code block in docs/*.md is collected and run by the doc-examples job in CI on each PR, so the old snippets were failing there.",
            "the snippets are not executed anywhere, in CI or elsewhere; the old ones were simply out of date.")],
     twin_gold="R0")

item("cr", "choice", """
Merge request !2291 - "orders: expose estimated_delivery_window in GET /v2/orders/{id}"
Files: services/orders/serializers.py, services/orders/flags.py, openapi/orders.yaml
Summary: Adds a new optional field, estimated_delivery_window, to the documented customer-facing response of GET /v2/orders/{id}. Guarded by the flag orders.edw_field, default OFF in all environments; we'll enable it for 5% of tenants next month. No change to authentication, payments or stored data.
Author's self-assessment: "R2 - it's behind a flag and additive only."
""", "Which change risk tier applies to this merge request?", "R3", 3)

item("cr", "choice", """
PR #9034 "ci: speed up prod deploys"
Files changed: .ci/deploy-production.yml
Diff summary:
-  needs: [build, integration-tests, security-signoff]
+  needs: [build, integration-tests]
Description: The security-signoff job waits for a manual approval from the security rota and adds about 40 minutes to every production deploy. Security reviews still happen in the PR itself, so this removes a duplicate gate. No application code changes.
Labels applied by the author: ci, tooling
""", "How should this PR be tiered under review policy 3.2?", "R4", 3)

item("cr", "choice", """
PR #8977 "Raise thumbnail render timeout"
Files changed: config/prod/security-and-limits.yaml (+1 -1)
Diff:
   thumbnails:
-    render_timeout_ms: 5000
+    render_timeout_ms: 8000
Context: The file groups several unrelated production settings; the only line touched is the thumbnail service's render timeout. The thumbnail service resizes product photos uploaded by merchants and has no access to user accounts or payment data.
Reviewer comment: "Path says security, so I've tagged it R3."
""", "What is the correct tier for PR #8977?", "R2", 2)

item("cr", "noul", """
Migration plan - PR #9120 "users: drop legacy_phone column"
Step 1 (already merged last sprint): all reads and writes moved from users.legacy_phone to users.phone_e164, which holds the same customers' phone numbers in a normalised format.
Step 2 (this PR): migration 0142 runs ALTER TABLE users DROP COLUMN legacy_phone. No backup of the column is taken; the down-migration re-creates an empty column.
Rollout: production, Tuesday 06:00 UTC maintenance window.
""", "Is R4 the correct tier for PR #9120?", 1, 3,
     twin=[("No backup of the column is taken; the down-migration re-creates an empty column.",
            "The migration first copies the column to users_legacy_phone_archive, retained for 90 days, and the down-migration restores it from there.")],
     twin_gold=0)

item("cr", "noul", """
PR #9001 "Fix typos in refund module"
Files changed: payments/refunds.py (+3 -3)
Diff:
-    # Retreive the orignal charge before issuing the refund
+    # Retrieve the original charge before issuing the refund
-    logger.info("Refund intiated for charge %s", charge_id)
+    logger.info("Refund initiated for charge %s", charge_id)
-    # TODO: handle partial refunds seperately
+    # TODO: handle partial refunds separately
Author: "Comment and typo fixes only, so R0."
""", "Should this PR be rated R0?", 0, 2)

item("cr", "choice", """
PR #8950 "test: cover password-reset token expiry"
Files changed:
  tests/auth/test_password_reset.py (+86 -4)
  tests/fixtures/users.py (+12 -0)
Description: Adds tests for expired and reused password-reset tokens. The fixture adds two fake users with generated emails. No changes outside tests/; the test suite is not packaged into the production image.
The security champion's bot auto-tagged the PR because the path contains "auth".
""", "Assign the change risk tier for PR #8950.", "R1", 2)

# =====================================================================================================
# 6. Supplier maturity
# =====================================================================================================
scale("sup", """
Orrin Components - Supplier Maturity Assessment, scoring rule
A supplier is rated at the highest level whose requirements are all met, and each level includes all requirements of the levels below it. If any requirement of a level is not met, the rating stops at the level below, whatever higher-level practices are also observed. "In scope" means every site and product line that supplies Orrin.
""", [
    ("Level 1 (Initial)", "Processes are ad hoc and depend on individuals; key procedures are not documented."),
    ("Level 2 (Managed)", "Documented procedures exist and are followed for key processes at some, but not all, in-scope sites or product lines."),
    ("Level 3 (Defined)", "Documented standard procedures are followed at every in-scope site and product line, with records showing they are used."),
    ("Level 4 (Measured)", "Level 3, plus quantitative process metrics with defined control limits, reviewed by management at least quarterly, with a documented response to every out-of-limit result."),
    ("Level 5 (Optimizing)", "Level 4, plus a documented improvement programme that has delivered at least one measured improvement, sustained for 6 months or more, within the past 24 months."),
])

item("sup", "choice", """
Audit summary - Brackenridge Castings (audit closed 2026-08-14)
Scope: three foundry sites (Hale, Dunmore, Pellbridge), all supplying Orrin.
- Documented work instructions for melting, pouring and inspection at all three sites; batch records sampled at each site show they are followed.
- SPC charts with control limits for pour temperature and porosity at all sites.
- Management reviews the SPC dashboards twice a year (January and July); minutes attached. Every out-of-limit point in the sample has a corrective action record.
- A lean programme reduced scrap from 6.1% to 4.9% in March 2025; the lower rate has held every month since.
""", "What maturity level should Brackenridge Castings be given?", "Level 3 (Defined)", 3,
     twin=[("twice a year (January and July)", "every quarter (January, April, July and October)")],
     twin_gold="Level 5 (Optimizing)")

item("sup", "choice", """
Site visit notes - Quillon Plastics
Quillon supplies Orrin from two plants. At the Westbay plant the auditor found a controlled procedures manual, trained operators, and completed moulding checklists for every shift sampled. The Amberly plant, acquired in 2025, supplies the same housings; its supervisors described their setup and inspection steps in detail and were clearly experienced, but no written procedures exist yet ("it's all in Gerry's head, and Gerry's been here 30 years"). Quillon has a documented plan to roll the Westbay manual out to Amberly by 2027. Both plants track defect rates monthly.
""", "At which maturity level does Quillon Plastics sit?", "Level 2 (Managed)", 2)

item("sup", "choice", """
Email from the buyer, Rhea Castellan, to the supplier quality team
Subject: Tobin & Sons Machining - maturity rating for the new-supplier file
Visited Tobin's single workshop yesterday. Very capable people: the owner, Walt Tobin, sets up every job himself and his first-article parts were perfect. When I asked for work instructions or an inspection plan, Walt said they don't write things down because "every job's different". Tooling offsets are kept on sticky notes on each machine. No records of in-process checks. Delivery performance on our trial order was 100% on time with zero defects. They're keen and cheap. What level do I enter?
""", "What level should the buyer enter for Tobin & Sons?", "Level 1 (Initial)", 1)

item("sup", "noul", """
Assessment extract - Norvale Fasteners (single site, one product line)
Procedures: controlled work instructions for heading, threading and heat treatment; records reviewed for 40 lots, all complete.
Metrics: hardness and thread-gauge results plotted on control charts with calculated limits; the plant manager and quality lead review the charts in a monthly meeting (minutes for all 12 months provided).
Out-of-limit results: two hardness excursions in Q2. The minutes for both months read "furnace adjusted on the floor, back in limits". No corrective action records, root-cause notes or other documentation of the response were found.
""", "Does Norvale meet the requirements of Level 4 (Measured)?", 0, 3)

item("sup", "choice", """
Re-assessment - Lindqvist Electronics (assessment date 2026-09-02)
All four in-scope assembly lines follow the same controlled procedures, with complete traveller records in every sample. First-pass yield and solder-defect rate are charted with control limits, reviewed by the operations director each quarter, and every out-of-limit point has a documented corrective action. The company's improvement programme is documented; its last completed project, which cut solder defects by 38%, finished in January 2024 and the gain has held ever since. Two newer projects started in 2026 are still in the measurement phase, with no results yet.
""", "Rate Lindqvist Electronics on the maturity scale.", "Level 4 (Measured)", 3)

# =====================================================================================================
# 7. Data classification
# =====================================================================================================
scale("dc", """
Halvard Credit Union - Information Classification Standard, section 3
3.1 Classify by the most sensitive element present in the item.
3.2 A number with all but the last four digits masked is not a full account or card number.
3.3 Information becomes Public only when formally approved for release by Communications or Compliance. Being posted somewhere publicly reachable, by mistake or otherwise, is not approval.
""", [
    ("Public", "Formally approved for release to anyone."),
    ("Internal", "Not approved for release, low harm if disclosed; general business information that contains no personal data other than staff names and work contact details."),
    ("Confidential", "Business-sensitive information, or personal data about members or staff, that does not meet the Restricted criteria."),
    ("Restricted", "Contains government ID numbers, full account or card numbers, authentication secrets (passwords, keys, tokens), health information, or any record combining a person's full name with both their date of birth and home address."),
])

item("dc", "choice", """
Service desk ticket SD-30418
Requester: Priya Venn, Member Services
"I need to email the attached spreadsheet to our mailing house for the autumn newsletter. It lists 400 members who opted in: full name, email address, home branch, and member account number shown as ****4821 style (only the last four digits visible). No dates of birth or addresses. What classification label should go on the file before I send it?"
""", "Which classification label should the spreadsheet carry?", "Confidential", 2,
     twin=[("shown as ****4821 style (only the last four digits visible)", "shown in full (for example 0041-2231-4821)")],
     twin_gold="Restricted")

item("dc", "choice", """
Chat - #it-helpdesk
Tomas (Facilities): The staff canteen menu and the building's December opening hours got uploaded to the public website by mistake last night. The page was up for about six hours before we pulled it. The only name on it is mine, with my work extension, as the facilities contact. No member info at all.
Tomas: The web team says it's fine because "it's been public anyway, so just label it Public and put it back up". Communications haven't reviewed it.
Ana (InfoSec): Let me check the label first.
""", "What is the correct classification for the page's content?", "Internal", 2)

item("dc", "choice", """
From: Social Committee
To: HR Operations
Subject: Birthday card list
Hi both, for the new birthday-card scheme we've put together a sheet of all 60 staff at head office: full name, date of birth, and home address, so the cards can be posted to arrive on the day. We'd like to keep it on the shared committee drive. Everyone agreed to take part. Which classification should the sheet carry?
""", "Which classification applies to the birthday-card sheet?", "Restricted", 3,
     twin=[("full name, date of birth, and home address, so the cards can be posted to arrive on the day",
            "full name, date of birth, and desk number, so the cards can be left on desks on the day")],
     twin_gold="Confidential")

item("dc", "noul", """
Incident note - log review
During a routine review, the platform team found that the payments gateway adapter had been writing its full debug output to the application log for two weeks. The log lines include request timestamps, internal transaction IDs, HTTP status codes and, in the request headers, the live API secret key used to authenticate to the card processor. No member names, card numbers or account numbers appear in the lines sampled. The log files are stored on the shared operations server.
""", "Should these log files be classified as Restricted?", 1, 2)

item("dc", "noul", """
Marketing request MR-7719
Item: "Autumn savings rates" one-page flyer (PDF). Content: savings product names, interest rates, minimum balances, branch opening hours and the general enquiries phone number. No personal data.
Status: Compliance review completed 12 September; approval reference CMP-2026-0441 issued for release on the website and in branches.
Requester's question: which label goes in the document footer?
""", "Is Public the right classification for this flyer?", 1, 2)

item("dc", "noul", """
Member complaint received via secure message (forwarded to Collections)
"I'm writing about the late fee on my car loan. I missed the August payment because I was in hospital for eleven days after my diabetes got out of control, and I couldn't get to online banking. I've paid it now. Please can you remove the fee? - Jonah Mirrell"
Collections wants to attach this message to the account's case record and share it with the fee-review panel, and needs to know the classification that applies to the message.
""", "Is Confidential the correct classification for this message?", 0, 2)

# =====================================================================================================
# 8. River flood alert levels
# =====================================================================================================
scale("fl", """
Merrow Basin River Authority - Alert Procedure FA-3
- Alerts for the Lower Merrow reach are based only on the Castleford reference gauge; tributary gauges inform forecasts but are not used directly.
- "Observed level" means the latest validated 15-minute reading. Readings flagged unvalidated are ignored.
- "Trend" compares the latest validated reading with the validated reading before it.
- If more than one level applies, issue the highest.
""", [
    ("Normal", "Observed level below 3.0 m, and no forecast of reaching 3.0 m within the next 48 hours."),
    ("Watch", "Observed level below 3.0 m but forecast to reach 3.0 m or more within 48 hours; or observed level from 3.0 m to 3.8 m with a falling trend."),
    ("Warning", "Observed level from 3.0 m to 3.8 m with a steady or rising trend; or forecast to exceed 3.8 m within the next 24 hours."),
    ("Severe Warning", "Observed level above 3.8 m, or a confirmed breach or overtopping of a flood defence in the reach."),
])

item("fl", "choice", """
Duty officer log - Lower Merrow, 4 March
Castleford gauge (validated readings):
05:45  3.38 m
06:00  3.46 m
06:15  3.51 m
06:30  3.47 m
Forecast (issued 06:00): peak of 3.52 m around 06:30, then a slow fall over the next 36 hours. Rain has stopped across the catchment.
Tributary gauge at Pell Brook: 1.9 m, falling.
The 06:45 reading has not yet been validated. The officer must set the alert level now.
""", "What alert level should the duty officer set?", "Watch", 3,
     twin=[("06:30  3.47 m", "06:30  3.55 m")], twin_gold="Warning")

item("fl", "choice", """
Forecasting desk bulletin - 11 November, 14:00
Castleford reference gauge: 2.62 m (validated 13:45), rising slowly.
Pell Brook tributary gauge: 4.10 m and rising after 60 mm of rain in the upper catchment.
Model run 14:00: Castleford forecast to pass 3.0 m at about 23:00 tonight and to peak at 3.92 m around 10:00 tomorrow, above 3.8 m from about 08:00 (18 hours from now).
No defence problems reported. The overnight officer asked whether the Pell Brook level alone justifies a Severe Warning for the reach.
""", "Under FA-3, which alert applies to the Lower Merrow reach right now?", "Warning", 3,
     twin=[("to peak at 3.92 m around 10:00 tomorrow, above 3.8 m from about 08:00 (18 hours from now)",
            "to peak at 3.74 m around 10:00 tomorrow (20 hours from now)")],
     twin_gold="Watch")

item("fl", "choice", """
Field report received 02:20, 19 January
From: Ops crew 4, Hollin Farm embankment (Lower Merrow reach)
"Confirmed: a 15 m section of the Hollin Farm flood embankment has slumped and water is flowing through the gap into the pasture behind it. Two houses on Hollin Lane are about 300 m downslope. Crew on site placing bulk bags."
Castleford gauge (validated 02:15): 2.14 m, steady. Forecast: no significant rise in the next 48 hours.
The duty officer notes that the gauge is "well below any trigger".
""", "Which alert level should be in force for the reach?", "Severe Warning", 2)

item("fl", "noul", """
Morning briefing - 7 October
Castleford gauge: 2.80 m (validated 07:45), rising 2 cm per hour.
Forecast (07:00 run): continued slow rise to a peak of 2.95 m in about 36 hours, then falling. Forecast confidence: high.
Tributaries: all below typical levels.
The comms team is asking whether to publish a Watch "to be on the safe side".
""", "Under FA-3, is a Watch the level the authority should issue?", 0, 2)

item("fl", "noul", """
Gauge feed extract - Castleford, 22 February
21:30  3.72 m  validated
21:45  3.79 m  validated
22:00  3.81 m  validated
22:15  3.84 m  unvalidated
Forecast: peak 3.86 m at about 23:30, then falling.
No defence incidents reported.
""", "Should a Severe Warning be in force at 22:15?", 1, 3,
     twin=[("22:00  3.81 m  validated", "22:00  3.81 m  unvalidated")], twin_gold=0)

# =====================================================================================================
# 9. Certainty of evidence
# =====================================================================================================
scale("gr", """
Kinsale Guideline Group - certainty scoring
Start at 4 points for a body of randomised trials, or 2 points for observational studies.
Subtract 1 point for each domain with a serious concern and 2 points for each domain with a very serious concern. Domains: risk of bias, inconsistency, indirectness, imprecision, publication bias.
Observational evidence only: if no domain has any concern, add 1 point for a large effect (relative risk above 2.0 or below 0.5) and 1 point for a clear dose-response gradient.
The score cannot go below 1 or above 4.
Imprecision is serious when the 95% confidence interval includes both no effect (RR 1.0, or a mean difference of 0) and the panel's threshold for a meaningful effect.
""", [
    ("High", "Final score 4: the true effect is very likely close to the estimate."),
    ("Moderate", "Final score 3: the true effect is probably close to the estimate."),
    ("Low", "Final score 2: the true effect may be substantially different from the estimate."),
    ("Very low", "Final score 1: the true effect is likely to be substantially different from the estimate."),
])

item("gr", "choice", """
Evidence profile - Question 4: early mobilisation after hip fracture surgery; outcome: 90-day mortality
Studies: 5 randomised trials, 1,840 patients.
Risk of bias: serious concern. Three trials, contributing 71% of the weight, did not conceal allocation.
Inconsistency: no concern (I-squared 8%).
Indirectness: no concern.
Imprecision: pooled RR 0.82, 95% CI 0.62 to 1.08; the panel's threshold for a meaningful effect is RR 0.90.
Publication bias: not suspected (symmetric funnel plot).
""", "What certainty rating should the panel give this outcome?", "Low", 3,
     twin=[("95% CI 0.62 to 1.08", "95% CI 0.66 to 0.88")], twin_gold="Moderate")

item("gr", "choice", """
Evidence profile - Question 9: occupational exposure to solvent X and chronic kidney disease
Studies: 4 prospective cohort studies, 212,000 workers; no randomised trials exist.
Risk of bias: no concern (all adjusted for age, diabetes and hypertension; low loss to follow-up).
Inconsistency: no concern. Indirectness: no concern. Imprecision: no concern (RR 3.1, 95% CI 2.4 to 4.0). Publication bias: not detected.
Dose-response: risk rose steadily across exposure tertiles in all four cohorts.
Draft rating from the junior analyst: "Low, since it's observational."
""", "Rate the certainty of evidence for Question 9.", "High", 3)

item("gr", "choice", """
Summary of findings - Question 12: melatonin for sleep onset in children aged 4-10
Studies: 6 randomised trials. All six enrolled adults aged 65 and older; no trials in children were found. The panel judged this a very serious concern for indirectness.
Risk of bias: no concern. Inconsistency: no concern. Imprecision: no concern.
Publication bias: serious concern (all six trials small and industry-funded; two registered trials never reported).
Effect: sleep onset 11 minutes faster (95% CI 8 to 14).
""", "Which certainty level applies to Question 12?", "Very low", 2)

item("gr", "noul", """
Panel worksheet - Question 15: bicycle helmet laws and head-injury admissions
Studies: 7 observational before-after studies.
Effect: RR 0.42 (95% CI 0.35 to 0.51), a large effect.
Risk of bias: serious concern (most studies did not account for falling cycling rates after the laws were introduced).
Inconsistency, indirectness, imprecision, publication bias: no concern.
Dose-response: not assessable.
Chair's note: "Large effect, so we can rate up to Moderate."
""", "Should the certainty for Question 15 be rated Moderate?", 0, 3,
     twin=[("serious concern (most studies did not account for falling cycling rates after the laws were introduced)",
            "no concern (all studies adjusted for changes in cycling rates after the laws were introduced)")],
     twin_gold=1)

item("gr", "choice", """
Evidence profile - Question 7: zinc lozenges and cold duration in adults
Studies: 8 randomised trials, 1,120 adults.
Risk of bias: no concern. Indirectness: no concern. Publication bias: not suspected.
Inconsistency: serious concern. Five trials showed shorter colds and three showed no difference; the heterogeneity could not be explained (I-squared 71%).
Imprecision: pooled mean difference -1.6 days (95% CI -2.4 to -0.8); the panel's threshold for a meaningful effect is 1 day.
""", "What is the final certainty of the evidence for Question 7?", "Moderate", 2)

# =====================================================================================================
# 10. Food safety inspection grade
# =====================================================================================================
scale("fd", """
Dunmore County Environmental Health - Grading Rules
- Each violation carries the points shown on the inspection form. Points count for every violation found, whether or not it is corrected during the inspection.
- A critical violation counts as "uncorrected" only if it has not been fully corrected before the inspector leaves.
- Imminent health hazards: no hot water, sewage backup, active pest infestation (live pests or fresh signs of current activity), or loss of power.
- If the criteria of more than one outcome are met, the worst outcome applies.
""", [
    ("Grade A", "0 to 13 points, and no critical violation left uncorrected."),
    ("Grade B", "14 to 27 points; or 0 to 13 points with exactly one critical violation left uncorrected."),
    ("Grade C", "28 points or more; or two or more critical violations left uncorrected."),
    ("Closure", "Any imminent health hazard is found, regardless of points."),
])

item("fd", "choice", """
Inspection report #DC-26-04417 - The Copper Kettle Bistro
Violations found:
1. Critical - Cold holding: potato salad in the prep fridge at 47°F (limit 41°F). Corrected on site: product discarded, fridge adjusted and verified at 39°F before the inspector left. 7 points.
2. Hand sink blocked by a mop bucket; cleared during the inspection. 3 points.
3. Food containers in the dry store not labelled. 2 points.
Total: 12 points.
Inspector remarks: "Manager cooperative."
""", "What grade should The Copper Kettle Bistro receive?", "Grade A", 3,
     twin=[("Corrected on site: product discarded, fridge adjusted and verified at 39°F before the inspector left.",
            "Product discarded, but the fridge still read 46°F when the inspector left; repair booked for tomorrow.")],
     twin_gold="Grade B")

item("fd", "choice", """
Inspection report #DC-26-04502 - Lucky Harbour Noodle House
Violations found:
1. Wiping cloths stored on the counter, not in sanitiser. 2 points.
2. No hot water at any sink: the water heater failed two days ago. Staff are boiling water in stock pots for handwashing and dishwashing; a plumber is booked for Friday. 5 points.
3. Missing thermometer in the reach-in cooler. 2 points.
Total: 9 points.
The owner states that the boiled-water arrangement "works fine".
""", "Which outcome follows from this inspection?", "Closure", 2)

item("fd", "choice", """
Inspection report #DC-26-04388 - Greenleaf Deli & Grocery
Violations found:
1. Critical - Raw chicken stored above ready-to-eat salads in the walk-in cooler; rearranged during the inspection and verified. 8 points.
2. Food handler without hair restraint. 2 points.
3. Critical - Sanitiser bucket below required concentration; remade and tested at correct strength before the inspector left. 7 points.
4. Scoop handle stored in the flour bin. 2 points.
5. Cracked floor tiles in the back prep area. 3 points.
6. Expired food handler certificates for two staff. 5 points.
7. Bulk containers of rice unlabelled. 3 points.
Total: to be calculated by the grading clerk.
""", "What grade does Greenleaf Deli & Grocery get?", "Grade C", 3)

item("fd", "noul", """
Inspection report #DC-26-04611 - Sunnyside Bakery
Violations found:
1. Critical - Cream-filled pastries held at room temperature (74°F) in the display case. Not corrected: the owner says the display fridge is broken and will be replaced next week. 6 points.
2. Critical - No soap at the only hand sink in the production area. Not corrected: staff were sent to buy soap but had not returned when the inspector left. 4 points.
3. Light shield missing over the mixing area. 3 points.
Total: 13 points.
""", "Does this inspection result in Grade B?", 0, 3,
     twin=[("Not corrected: staff were sent to buy soap but had not returned when the inspector left.",
            "Corrected: soap was brought from the front-of-house sink and the dispenser refilled before the inspector left.")],
     twin_gold=1)

item("fd", "choice", """
Inspection report #DC-26-04720 - Marigold Tea Room
Violations found:
1. Old, dry rodent droppings (about six) behind shelving in the dry-goods store. Inspector note: "Droppings desiccated and crumbling; no fresh droppings, gnaw marks, nesting or live rodents found anywhere; the pest-control contractor's log shows monthly visits with no activity recorded since April." Area to be cleaned. 6 points.
2. Staff drink stored on a food-prep shelf. 2 points.
3. Probe thermometer not calibrated. 3 points.
Total: 11 points. No critical violations recorded.
""", "Assign the grade for the Marigold Tea Room inspection.", "Grade A", 3)

# =====================================================================================================
# 11. Pressure injury staging
# =====================================================================================================
scale("pi", """
Wexmoor Community Hospital - Wound documentation guide (pressure injuries)
- Stage only wounds caused by pressure, or pressure combined with shear. Skin tears, moisture damage, and injuries from tape, trauma or burns are not staged.
- Blanching test: press the red area with a finger; if it turns white and the colour returns when released, it blanches.
- Do not reverse-stage: a healing pressure injury keeps the highest stage it was ever documented at, recorded as "healing Stage X".
- Base the stage on what can be seen or directly felt (including with a probe).
""", [
    ("Stage 1", "Intact skin with a localised area of non-blanchable redness, without purple or maroon discolouration."),
    ("Stage 2", "Partial-thickness skin loss with exposed dermis (pink or red, moist wound bed), or an intact or ruptured blister filled with clear fluid; no fat, slough or eschar."),
    ("Stage 3", "Full-thickness skin loss; fat may be visible; slough or eschar may be present but does not hide the depth; no fascia, muscle, tendon, ligament, cartilage or bone visible or palpable."),
    ("Stage 4", "Full-thickness skin and tissue loss with fascia, muscle, tendon, ligament, cartilage or bone visible or directly palpable."),
    ("Unstageable", "Full-thickness loss where slough or eschar covers the wound bed so its depth cannot be seen or felt."),
    ("Deep tissue pressure injury", "Intact or non-intact skin with persistent non-blanchable deep red, maroon or purple discolouration, or a blood-filled blister."),
])
PI_NONE = "The wound is not a pressure injury to be staged under this guide."

item("pi", "choice", """
Nursing progress note - Ward 6B, bed 14, 06:30
82-year-old woman, bed-bound since a hip fracture 5 days ago; heels had been offloaded on pillows but were found resting on the mattress this morning.
Right heel: intact blister about 2 x 3 cm, filled with dark red-purple fluid; surrounding skin boggy and maroon, non-blanchable. No open area.
Left heel: intact skin, blanchable redness only.
Plan: heel-offloading boots, tissue viability referral, photograph for the record.
""", "How should the right-heel wound be staged?", "Deep tissue pressure injury", 3, none=PI_NONE,
     twin=[("filled with dark red-purple fluid; surrounding skin boggy and maroon, non-blanchable",
            "filled with clear, straw-coloured fluid; surrounding skin pink")],
     twin_gold="Stage 2")

item("pi", "choice", """
Tissue viability consult - sacral wound, bed 3, Ashby ward
Wound 4.5 x 3.8 cm, full thickness. About 60% of the bed is covered with adherent yellow slough; the remaining 40% shows red granulation tissue, with subcutaneous fat visible at the upper margin. On gentle probing at the lower edge, bone is directly felt at 2.1 cm depth. Moderate serous exudate, no odour. Surrounding skin intact.
Documentation question from the ward: "There's slough over most of it, so do we chart it as unstageable?"
""", "What stage should be charted for the sacral wound?", "Stage 4", 3, none=PI_NONE)

item("pi", "choice", """
Admission skin assessment - Emergency admissions unit
76-year-old man found on the floor at home after an unknown period, admitted with dehydration.
Coccyx: 5 x 4 cm wound whose entire bed is covered by dry, adherent black eschar; edges well defined; surrounding skin red and non-blanchable. No depth visible anywhere; not probed.
Left hip: area of non-blanchable redness 3 x 3 cm, skin intact, no discolouration beyond red.
Please stage the coccyx wound for the incident report.
""", "Which category applies to the coccyx wound?", "Unstageable", 2, none=PI_NONE)

item("pi", "noul", """
Night shift skin check - bay 2, bed 5
Patient turned at 02:00 after lying on the left side for about 3 hours. Left hip: area of redness about 4 cm across. When pressed with a finger the area turned white, and the redness returned when the finger was lifted; 30 minutes after repositioning the redness had faded completely. Skin intact, no warmth, no discolouration.
The healthcare assistant has asked whether to open a Stage 1 pressure injury record.
""", "Should this finding be recorded as a Stage 1 pressure injury?", 0, 2)

item("pi", "choice", """
Wound note - Outpatient dialysis unit
68-year-old man with fragile skin from long-term steroid use. When the nurse removed the adhesive dressing from his fistula site, a flap of skin on the forearm lifted with it, leaving a 3 cm shallow, pink, moist wound with exposed dermis and a partial skin flap. No blister, no slough, no fat visible. He sits in a recliner for dialysis, but the forearm rests on a padded armrest and the wound is on the upper surface, away from the armrest.
Please stage for the wound register.
""", "How should the forearm wound be entered in the register?", NONE, 3, none=PI_NONE)

item("pi", "noul", """
Community nursing visit - Mrs Adaeze Holm, 88
Sacral wound reviewed. Today: shallow open area 1.5 x 1 cm, pink moist bed with exposed dermis, no slough, no fat visible, edges contracting.
History from the referral letter: "Sacral pressure injury, documented Stage 3 on discharge from Wexmoor Community Hospital six weeks ago (full thickness, fat visible)."
The carer asks what stage should go on today's record.
""", "Should today's record describe the wound as Stage 3?", 1, 3,
     twin=[('"Sacral pressure injury, documented Stage 3 on discharge from Wexmoor Community Hospital six weeks ago (full thickness, fat visible)."',
            '"Sacral pressure injury first noted by the district nurse this week; no earlier documentation."')],
     twin_gold=0)

# =====================================================================================================
# 12. Housing repair urgency
# =====================================================================================================
scale("hs", """
Fernhollow Housing Association - Repairs Priority Guide
- Essential services: heating, hot water, a working toilet, cooking facilities, lighting and power.
- If the ONLY toilet in the home is not working, the repair is Emergency.
- Total loss of heating between 1 October and 30 April is Emergency if anyone in the household is under 5, over 70, or has a documented medical need; otherwise it is Urgent.
- Where a report covers more than one defect, the priority is set by the most urgent defect.
""", [
    ("Emergency", "Danger to health, safety or security, or risk of serious damage to the building; must be made safe within 24 hours."),
    ("Urgent", "Loss of an essential service, or a defect that materially affects comfort or convenience, with no immediate danger; complete within 5 working days."),
    ("Routine", "A repair that does not affect essential services, health, safety or security; complete within 28 days."),
    ("Planned", "Replacement or improvement of an item that still works, scheduled into the planned maintenance programme."),
])

item("hs", "choice", """
Online repair request - 14 November
Tenant: Alicia Brandt, 12 Wren Court
"Hi, the boiler stopped working last night and shows fault code F28. We have no heating and no hot water at all. It's just me (34) and my son Theo, who is 6. Nobody in the house has any medical conditions. We have an electric fan heater in the living room so we're managing, but it's cold upstairs. Please can someone come out?"
""", "What priority should this repair be given?", "Urgent", 3,
     twin=[("my son Theo, who is 6", "my son Theo, who is 4")], twin_gold="Emergency")

item("hs", "choice", """
Phone log - Fernhollow contact centre, 09:12
Caller: Desmond Achebe, Flat 3, 44 Linnet Road (one-bedroom flat, one bathroom)
The caller reports that the toilet will not flush: the handle spins freely and the cistern does not empty. He says: "No rush at all, honestly. I've been popping next door to my sister's flat, she doesn't mind. Whenever you can fit it in next week is fine." No leaks and no other issues reported. The caller works from home on Tuesdays and Thursdays.
""", "Which repair priority applies to this call?", "Emergency", 2)

item("hs", "choice", """
Email to repairs@fernhollow
"My kitchen is completely unusable!!! The hinge on the big cupboard door next to the cooker has snapped and the door is hanging off at an angle. I've taken it off and put it in the hall. The cooker, fridge and sink all work, it's just that cupboard. I've been a tenant for 11 years and never complained. When can someone come? - Mr G. Paxton, 7 Heron Close"
""", "How should the repairs team prioritise this job?", "Routine", 2)

item("hs", "choice", """
Repair request form - 3 December
Address: 21 Kittiwake Way (two-bedroom house; household of two adults aged 41 and 45, no medical needs)
Defect 1: Bedroom window (first floor): the outer pane has a crack across one corner; the glass is intact and the window still closes and locks.
Defect 2: The radiators in both bedrooms stay cold; the radiators downstairs and the hot water are working normally. The upstairs rooms are at 13°C in the evenings.
""", "What priority does the request as a whole receive?", "Urgent", 3)

item("hs", "noul", """
Tenant message via app - 5 Plover Street
"Our kitchen worktops are the original ones from when the houses were built in 1994. They're faded and a bit tired-looking, and the colour is very dated, but there's no damage and everything works fine. Could they be replaced with something more modern? We'd be happy to wait until you're doing other kitchens on the street."
Surveyor visit confirmed: worktops sound, sealed and fully usable.
""", "Should this request be logged as Planned work?", 1, 2)

item("hs", "noul", """
Out-of-hours call - 23:40
Caller: Ruth Obi, Flat 9, Swallow House
"Sorry to ring so late. Water is dripping out of the ceiling light in my hallway, just a few drops every minute. I think the flat upstairs might have a leak. The light still works and it's only a tiny bit of water; I've put a bowl under it. It can wait till the morning if that's easier for you."
""", "Does this report qualify as an Emergency repair?", 1, 2)

# =====================================================================================================
# 13. Loan delinquency buckets
# =====================================================================================================
scale("dl", """
Stillwater Lending - Servicing Manual, section 7 (delinquency reporting)
7.1 Days past due (DPD) = days from the due date of the oldest unpaid installment to the reporting date. A payment received on the due date is on time.
7.2 An installment counts as paid only when at least 95% of its scheduled amount has been received.
7.3 Every payment is applied to the oldest unpaid installment first, and any remainder to the next installment, including installments not yet due.
7.4 A pending hardship application, dispute or promise to pay does not pause or reset the DPD count.
""", [
    ("Current", "No installment is past due on the reporting date."),
    ("1-29 DPD", "The oldest unpaid installment is 1 to 29 days past its due date."),
    ("30-59 DPD", "The oldest unpaid installment is 30 to 59 days past its due date."),
    ("60-89 DPD", "The oldest unpaid installment is 60 to 89 days past its due date."),
    ("90+ DPD", "The oldest unpaid installment is 90 or more days past its due date."),
])

item("dl", "choice", """
Account 55-0931-7 - payment history
Installment: $400.00, due on the 1st of each month. All installments up to and including March 2026 were paid in full and on time.
Payments received since: $400.00 on Apr 3; $370.00 on May 2; $400.00 on Jun 1. No other payments or credits.
Reporting date: June 15, 2026.
Collections note: "Borrower short-paid May, so May is still open."
""", "Which delinquency bucket should the account be reported in?", "1-29 DPD", 3,
     twin=[("$400.00 on Jun 1", "$420.00 on Jun 1")], twin_gold="Current")

item("dl", "choice", """
Collections queue - account 61-2208-4
Installment: $615.00, due on the 10th of each month.
Last payment: $615.00 received February 10, 2026, which brought the account fully up to date. No payments since.
Contact log: March 14, the borrower promised to pay "by end of March"; April 2, the borrower submitted a hardship application (still under review).
Reporting date: May 20, 2026.
Collector's draft bucket: "1-29 DPD - hardship application pending, count restarted April 2."
""", "What bucket applies to account 61-2208-4 on the reporting date?", "60-89 DPD", 2)

item("dl", "noul", """
Borrower account 70-1145-2 (auto loan)
Installment: $389.00, due on the last day of each month.
Payment history: all installments through December 2025 paid on time. No payment has been received for the January 31, 2026 installment or since.
Reporting date: March 1, 2026.
The month-end report draft lists the account under "30-59 DPD" with the note "missed a full month's payment".
""", "Is 30-59 DPD the correct bucket for this account on the reporting date?", 0, 3,
     twin=[("Reporting date: March 1, 2026.", "Reporting date: March 2, 2026.")], twin_gold=1)

item("dl", "choice", """
Account 48-7719-0 - servicing review
Installment: $600.00, due on the 20th of each month.
Payments received in 2026: $600.00 on Feb 19; $1,600.00 on Mar 18; nothing after that.
Borrower's email of Mar 18: "I've paid extra this month so I'm covered for April and May; I'll be travelling."
All installments before February were paid in full and on time.
Reporting date: June 25, 2026.
""", "Where does account 48-7719-0 fall on June 25?", "30-59 DPD", 3)

item("dl", "choice", """
Early-warning report - account 33-5098-6 (personal loan)
Installment: $275.00, due on the 15th of each month.
Payments: the last payment, $275.00 on December 15, 2025, brought the account fully up to date. No payments since. On March 30 the borrower disputed a late fee; the dispute is still open.
Reporting date: April 20, 2026.
""", "Report the correct delinquency status for this account.", "90+ DPD", 2)

# =====================================================================================================
# 14. Turbulence intensity
# =====================================================================================================
scale("tb", """
Corvane Air Flight Operations Manual 8.4 - Turbulence reporting
- Classify the encounter by the most severe effect reported.
- Use crew reports and flight data only; passenger accounts and social media are not used.
- Where recorded flight data conflict with a crew member's impression, the recorded data take precedence.
""", [
    ("Light", "Slight, momentary changes in altitude or attitude; occupants may feel slight strain against seat belts; unsecured objects may shift slightly; food service can continue and walking is little affected."),
    ("Moderate", "Changes in altitude or attitude, but the aircraft remains in positive control; occupants feel definite strain against seat belts; unsecured objects are dislodged; food service and walking are difficult."),
    ("Severe", "Large, abrupt changes in altitude or attitude; the aircraft may be momentarily out of control; occupants are forced violently against seat belts; unsecured objects are tossed about; walking is impossible."),
    ("Extreme", "The aircraft is violently tossed about and is practically impossible to control; may cause structural damage."),
])

item("tb", "choice", """
Cabin crew occurrence report - flight CV 812, FL360, 40 minutes after departure
Lead flight attendant (R. Okonjo): "We were mid-service in the aft cabin. Two coffee pots and several cups slid off the cart tops onto the floor. Passengers were held firmly against their belts; I saw heads jolt. Walking the aisle was difficult, so I stopped the service and told the crew to secure the carts and sit. It lasted about six minutes."
Captain's tech log entry: "light chop, ride report passed to ATC."
""", "How should this turbulence encounter be classified?", "Moderate", 2)

item("tb", "choice", """
Captain's report - flight CV 377, descent through FL240
"Encountered turbulence in clear air near the jet stream. Moderate, in my assessment. One cabin crew member injured."
Flight data recorder extract (reviewed by the safety office): vertical acceleration from +2.1 g to -0.8 g within 2 seconds; altitude excursion of 210 ft; bank angle reached 34 degrees with the autopilot disconnecting; roll not controlled by the crew for about 3 seconds before recovery.
Cabin report: a flight attendant standing in the galley was lifted off her feet and struck the ceiling; galley items were thrown around.
""", "What intensity should the safety office record for flight CV 377?", "Severe", 3)

item("tb", "noul", """
Ride report logged by the first officer - flight CV 145, FL380
"Occasional bumps over the Pellan range for about 15 minutes. Service continued throughout; cabin crew reported it as a bit bumpy but no problem moving about the cabin. A passenger's phone slid a few centimetres across a tray table. Seat-belt sign left on as a precaution."
No other reports from the crew. Flight data: no significant altitude or airspeed excursions.
""", "Would Light be the correct classification for this encounter?", 1, 2,
     twin=[("Service continued throughout; cabin crew reported it as a bit bumpy but no problem moving about the cabin.",
            "Cabin crew suspended the service and took their seats because walking was difficult.")],
     twin_gold=0)

item("tb", "choice", """
Safety office file - flight CV 509
Viral post by a passenger (48,000 shares): "Worst turbulence of my life, we were FALLING, people were screaming, I thought we were going to die."
Crew reports: cabin crew continued the drinks service throughout; the purser noted "a few firm bumps, people felt a slight tug on their belts, a couple of cups shifted on the trays". The captain logged light turbulence for 4 minutes.
Flight data: altitude within 15 ft either way; vertical acceleration between +1.15 g and +0.88 g; no autopilot disconnect.
Media relations has asked the safety office to confirm the classification.
""", "Which turbulence category applies to flight CV 509?", "Light", 2)

# =====================================================================================================
# 15. Dog bite severity
# =====================================================================================================
scale("db", """
Ashgrove Animal Control - Bite Assessment Ordinance, Schedule B
- A "bite" is one closure of the jaws. If the dog releases and closes its jaws again, that is a second bite.
- An incident is rated by its most severe single bite, unless the Level 5 or Level 6 definition applies.
- Puncture depth is compared with the length of the dog's upper canine teeth, as measured or estimated by the investigating officer.
""", [
    ("Level 1", "Aggressive display (growling, snapping, lunging) with no contact of the teeth on the victim's skin."),
    ("Level 2", "Teeth contacted skin but did not puncture it; may cause redness, light bruising, or scratches no deeper than 2 mm."),
    ("Level 3", "One to four punctures from a single bite, none deeper than half the length of the dog's canine teeth; may include lacerations in a single direction caused by the victim pulling away."),
    ("Level 4", "One to four punctures from a single bite with at least one deeper than half the length of the dog's canine teeth, or deep bruising around the wound (the dog held on), or lacerations in both directions (the dog held on and shook its head)."),
    ("Level 5", "A multiple-bite incident with at least two Level 4 bites, or a multiple-attack incident with at least one Level 4 bite in each attack."),
    ("Level 6", "The victim died."),
])

item("db", "choice", """
Investigation report AC-26-0317
Victim: postal carrier, age 44. Dog: male mixed breed, about 30 kg; the officer measured the upper canines at 2.4 cm.
Account: the dog ran through an open gate and bit the carrier's left calf, released when she kicked out, then bit her right hand as she raised it.
Injuries (ED record): Left calf - two punctures, deepest 1.6 cm, with deep bruising. Right hand - three punctures, deepest 0.5 cm, no bruising, no lacerations.
The owner states the dog "only nipped her".
""", "What level should incident AC-26-0317 be assigned?", "Level 4", 3,
     twin=[("deepest 0.5 cm, no bruising, no lacerations", "deepest 1.4 cm, no bruising, no lacerations")],
     twin_gold="Level 5")

item("db", "choice", """
Call note - Animal Control dispatch
Caller: parent of a 7-year-old boy bitten by a neighbour's terrier during play in the garden.
Officer visit notes: on the back of the boy's left hand there is a curved line of red marks from the dog's teeth and one shallow scratch, about 1 mm deep, that bled slightly. The skin is not punctured anywhere; the GP who examined him the same afternoon confirmed "no puncture wounds". Mild bruising appeared the next day.
Parent: "It bit him, so it's a bite - surely that's serious."
""", "Which level on Schedule B fits this incident?", "Level 2", 2)

item("db", "choice", """
Investigation report AC-26-0402
Victim: 31-year-old dog walker. Dog: female shepherd cross, canines estimated at 2.0 cm.
Account from two witnesses: while the walker was separating two dogs, the shepherd bit her forearm once, held on and shook its head from side to side for several seconds before releasing.
Injuries (urgent care notes): three punctures on the forearm, deepest 0.8 cm; torn skin running from the punctures toward both the wrist and the elbow; no deep bruising.
""", "Rate this incident on the bite scale.", "Level 4", 3,
     twin=[("held on and shook its head from side to side for several seconds before releasing.",
            "let go at once as the walker pulled her arm back."),
           ("torn skin running from the punctures toward both the wrist and the elbow",
            "one tear running from the punctures toward the wrist, the direction in which she pulled her arm")],
     twin_gold="Level 3")

item("db", "noul", """
Complaint CX-5519
A jogger reports that a large dog in an unfenced front yard ran at her barking and snarling, jumped up, and grabbed the sleeve of her running jacket in its mouth, tearing a 10 cm rip in the fabric before the owner called it off. She was badly shaken. The officer inspected her arm the same day: no marks, redness, scratches or bruising on the skin; the jacket sleeve was thick and the teeth did not reach her arm.
""", "Is this a Level 1 incident under Schedule B?", 1, 2)

item("db", "noul", """
Investigation report AC-26-0455
Victim: 58-year-old visitor at a boarding kennel. Dog: male spaniel, canines measured at 2.2 cm.
The dog bit the visitor's ankle once when she reached over the kennel gate, and let go immediately. ED notes: two punctures, deepest 0.5 cm; no bruising; no lacerations. Wound cleaned and dressed; antibiotics prescribed.
Kennel manager's view: "Any bite that needs antibiotics should be at least a Level 4."
""", "Should this incident be recorded as Level 3?", 1, 2)

# =====================================================================================================
# 16. Air quality bands
# =====================================================================================================
scale("aq", """
Port Aldry Air Quality Bulletin - method note
- The daily band is set by whichever pollutant falls in the higher band.
- PM2.5 uses the 24-hour average concentration (micrograms per cubic metre). Ozone uses the highest 8-hour rolling average of the day (ppb).
- One-hour peaks are shown for information only and are never used to set the band.
""", [
    ("Good", "PM2.5 24-hour average 12.0 or lower, and ozone 8-hour maximum 54 or lower."),
    ("Moderate", "Worst pollutant in this range: PM2.5 12.1-35.4, or ozone 55-70."),
    ("Unhealthy for Sensitive Groups", "Worst pollutant in this range: PM2.5 35.5-55.4, or ozone 71-85."),
    ("Unhealthy", "Worst pollutant in this range: PM2.5 55.5-150.4, or ozone 86-105."),
    ("Very Unhealthy", "PM2.5 above 150.4, or ozone above 105."),
])

item("aq", "choice", """
Monitoring summary - Harbour Street station, 5 November (Bonfire Night)
PM2.5: 1-hour peak 88.0 at 21:00 during the fireworks display; 24-hour average 31.2.
Ozone: 1-hour peak 66; highest 8-hour average 62.
Nitrogen dioxide: 1-hour peak 41 ppb (not part of the band calculation).
Local news is already describing the evening's air as "unhealthy". The duty scientist has to publish the official band for the day.
""", "Which band should be published for 5 November?", "Moderate", 3,
     twin=[("24-hour average 31.2", "24-hour average 38.9")], twin_gold="Unhealthy for Sensitive Groups")

item("aq", "choice", """
Daily bulletin worksheet - Ridgeway station, 17 July
Weather: clear skies, 34°C, light winds, strong sunshine all afternoon.
PM2.5: 24-hour average 9.8 (1-hour peak 14.1).
Ozone: highest 8-hour average 88 (13:00-21:00); 1-hour peak 97.
Draft headline from the comms intern: "Particle levels low - air quality Good today."
""", "What is the official air quality band for 17 July?", "Unhealthy", 2)

item("aq", "noul", """
Bulletin check - Millbank station, 2 April
PM2.5: 24-hour average 11.9; 1-hour peak 19.0.
Ozone: highest 8-hour average 56; 1-hour peak 61.
The school-sports coordinator asks whether today can be listed as a "Good" day for the outdoor athletics meet, as the particle reading is below the Good limit.
""", "Is today's air quality in the Good band?", 0, 2)

item("aq", "choice", """
Wildfire smoke advisory - Port Aldry, 9 August
The Tallis Ridge fire, 40 km upwind, sent dense smoke over the city overnight.
PM2.5: 24-hour average 163.7; 1-hour peak 241.
Ozone: highest 8-hour average 38 (the smoke blocked sunlight).
Visibility was under 1 km for most of the day. Hospitals report increased asthma presentations.
""", "Which band applies to 9 August?", "Very Unhealthy", 1)

item("aq", "choice", """
Weekly review - Canal Basin station
The readings for each day of last week are listed in the card. The public-health team is checking which day, if any, should have carried the "Unhealthy for Sensitive Groups" band, because school alert texts go out only on those days.
""", "On which day was the official band Unhealthy for Sensitive Groups?", "Tuesday", 3,
     cases=[
         ("Monday", "PM2.5 24-hour average 18.2; ozone highest 8-hour average 49; ozone 1-hour peak 77."),
         ("Tuesday", "PM2.5 24-hour average 36.1; ozone highest 8-hour average 52."),
         ("Wednesday", "PM2.5 24-hour average 29.9 (1-hour peak 64); ozone highest 8-hour average 70."),
         ("Thursday", "PM2.5 24-hour average 11.4; ozone highest 8-hour average 86."),
         ("Friday", "PM2.5 24-hour average 55.6; ozone highest 8-hour average 40."),
         ("Saturday", "PM2.5 24-hour average 12.0; ozone highest 8-hour average 54."),
         ("Sunday", "PM2.5 24-hour average 22.0; ozone highest 8-hour average 55."),
     ], none="No day last week was in the Unhealthy for Sensitive Groups band.", fixed=True)

# =====================================================================================================
# 17. Translation error severity
# =====================================================================================================
scale("mq", """
Linden Localisation - Reviewer Guide, error severity
- Judge severity by the effect on the target-language reader, in the context where the text will be used.
- The length of an error (one character or a whole sentence) does not by itself determine severity.
- Preferential changes are logged, but they are not errors.
""", [
    ("Neutral", "A preferential change: the original translation was correct and acceptable, and the reviewer's version is only an alternative."),
    ("Minor", "An error that does not change meaning or hinder use (typo, slightly awkward phrasing, punctuation slip) and would not mislead the reader."),
    ("Major", "An error that changes or obscures the meaning or noticeably hinders use, but could not plausibly lead to harm to health or safety, legal exposure, or financial loss."),
    ("Critical", "An error that could plausibly lead to harm to health or safety, legal exposure or financial loss, or that would seriously damage the client's reputation."),
])

item("mq", "choice", """
Review ticket LL-44107 - Client: Harrowfield Pharma, patient information leaflet (German > English)
Segment 38
Source (back-translated): "Do not take more than 4 tablets in 24 hours."
Target delivered: "Do not take more than 5 tablets in 24 hours."
Translator's comment: "Just a typo - the 4 and 5 keys are next to each other. One character."
The reviewer must assign a severity before the file goes to print.
""", "What severity should segment 38's error receive?", "Critical", 2, levels=["Minor", "Major", "Critical"])

item("mq", "choice", """
Review ticket LL-44152 - Client: Seacliff Boutique Hotels, website "Your Stay" page (Spanish > English)
Segment 12
Source (back-translated): "Breakfast is served in the garden restaurant from 7:00 to 10:00."
Target delivered: "Breakfast is served in the garden restaurant from 7:00 to 11:00."
Context: the page is informational; breakfast is included in all room rates, so no charge depends on the time.
The reviewer must assign a severity.
""", "How severe is the error in segment 12?", "Major", 2, levels=["Minor", "Major", "Critical"])

item("mq", "choice", """
Review ticket LL-44190 - Client: Pellow Apps, mobile banking UI strings (French > English)
Segment 7 (button label)
Source (back-translated): "Begin the transfer"
Target delivered: "Begin transfer"
Reviewer's change: "Start transfer"
Reviewer's category: "Terminology error".
The client glossary has no entry for either "begin" or "start"; both forms appear elsewhere in the client's live English app, and the button fits the layout either way.
The QA lead needs the correct severity for the scorecard.
""", "Which severity category fits the reviewer's change?", "Neutral", 3)

item("mq", "noul", """
Review ticket LL-44233 - Client: Emberfall Games, in-game dialogue (Japanese > English)
Segment 1,204 (tavern keeper, optional side conversation)
Source (back-translated): "When the caravan arrives, you will receive your reward."
Target delivered: "You'll recieve your reward once the caravan arrives."
Reviewer note: "recieve" is misspelled; otherwise the sentence is correct and matches the source.
The reviewer must assign a severity.
""", "Should this error be rated Minor?", 1, 1)

# =====================================================================================================
# 18. Building damage grade
# =====================================================================================================
scale("dm", """
Tessaly Seismic Survey - rapid damage form, grading rule
Assign the grade of the most severe damage feature observed anywhere in the building. "Structural" elements are load-bearing walls, columns, beams, floors and the roof structure; partitions, gable walls above the eaves, chimneys, plaster and tiles are non-structural.
""", [
    ("Grade 1", "Negligible to slight damage: no structural damage; hairline cracks in very few walls; small pieces of plaster fall."),
    ("Grade 2", "Moderate damage: slight structural damage; cracks in many walls; fairly large pieces of plaster fall; parts of chimneys fall."),
    ("Grade 3", "Substantial to heavy damage: moderate structural damage; large, extensive cracks in most walls; roof tiles detach; chimneys fracture at the roof line; individual non-structural elements (partitions, gable walls) fail."),
    ("Grade 4", "Very heavy damage: heavy structural damage; serious failure of walls; partial structural failure of roofs or floors."),
    ("Grade 5", "Destruction: total or near-total collapse."),
])

item("dm", "choice", """
Rapid assessment - 14 Orchard Row (two-storey brick house), inspector T. Farrell
Interior: hairline cracks in two walls (living room and landing); a few small flakes of plaster on the kitchen floor. No other cracking.
Exterior: the upper third of the chimney stack has fallen into the front garden; the stack is otherwise intact below that point, with no fracture at the roof line. Roof tiles in place. No displacement of walls, floors or roof.
The owner asks for the grade for the insurance claim.
""", "Which damage grade should be recorded for 14 Orchard Row?", "Grade 2", 3)

item("dm", "choice", """
Rapid assessment - Village hall, Merrin Street (single-storey, stone)
Large diagonal cracks run through most of the walls, several wide enough to fit a finger. The east gable wall above the eaves has fallen outward into the car park. Many roof tiles have slipped. The roof trusses and the main load-bearing walls remain in place and are not displaced; the floor slab is intact.
The community group asks whether the hall can be graded for the relief fund.
""", "What grade does the village hall receive?", "Grade 3", 3,
     twin=[("The roof trusses and the main load-bearing walls remain in place and are not displaced; the floor slab is intact.",
            "Two roof trusses have dropped at the east end and part of the roof has fallen into the hall; the load-bearing walls are otherwise in place.")],
     twin_gold="Grade 4")

item("dm", "noul", """
Rapid assessment - 3 Quarry Lane (three-storey apartment building)
The rear load-bearing wall of the ground floor has partly collapsed, and the first floor above it has sagged about 40 cm at that end. The front two-thirds of the building is standing with all floors level, though with heavy cracking. Residents were evacuated.
The site coordinator writes: "It's basically destroyed - put it down as Grade 5 so it gets priority."
""", "Should 3 Quarry Lane be recorded as Grade 5?", 0, 2)

# =====================================================================================================
# 19. Research ethics review route
# =====================================================================================================
scale("irb", """
Harrowgate University Research Ethics Office - review routing
Decide in this order and stop at the first that applies: (1) not human subjects research; (2) Full board criteria met; (3) fits an exempt category; (4) otherwise, Expedited.
Identifiers include names, contact details, record numbers, full dates of birth and full postal codes.
Sensitive topics: illegal behaviour, sexual behaviour, mental health, substance use.
""", [
    ("Not human subjects research", "The project does not interact with living individuals to obtain data or specimens, and does not use identifiable private information about living individuals."),
    ("Exempt", "Minimal-risk research that fits an exempt category: anonymous surveys or interviews of adults on non-sensitive topics; research on normal educational practices; or secondary analysis of data the researcher receives with no identifiers."),
    ("Expedited", "Minimal-risk human subjects research that does not fit an exempt category (for example identifiable data, voice or video recordings, non-invasive physical measurements, or sensitive topics where responses are anonymous)."),
    ("Full board", "Research involving more than minimal risk, prisoners as participants, or sensitive topics where responses are identifiable."),
])

item("irb", "choice", """
Application summary - HUREO-26-311
PI: Dr. Selin Vardar, School of Education
Design: a one-off anonymous online survey of adult undergraduates (18+) about study habits: hours studied per week, library use, preferred revision methods, and (item 14) how often they have used cannabis in the past month. No names, emails, IP addresses or student numbers are collected. Estimated time: 10 minutes. No compensation.
The PI has ticked "Exempt" on the form.
""", "Which review route does HUREO-26-311 require?", "Expedited", 3,
     twin=[("how often they have used cannabis in the past month", "how many hours they usually sleep before an exam")],
     twin_gold="Exempt")

item("irb", "choice", """
Email to the ethics office
From: Marcus Ilunga, MA student, History
"For my dissertation I'm coding 1,200 obituaries published in the Harrowgate Courier between 1950 and 1990 to study how women's occupations were described. All the people in the obituaries have died. I'm only using the published text from the newspaper archive; I won't contact any families or anyone else. My supervisor thinks this needs a full ethics review because it uses names. Which route do I need?"
""", "Which route applies to this project?", "Not human subjects research", 2)

item("irb", "choice", """
Application summary - HUREO-26-348
PI: Dr. Ondine Carrow, Library and Information Science
Design: 45-minute interviews with adult men currently serving sentences at Brackmoor Prison about how they use the prison library (favourite genres, opening hours, requests for new books). No questions about offences, health or other sensitive topics; interview notes are kept without names. The PI judges the risk to be minimal.
Requested route: Exempt ("anonymous interviews of adults on a non-sensitive topic").
""", "What level of review does HUREO-26-348 need?", "Full board", 2)

item("irb", "noul", """
Application summary - HUREO-26-362
PI: Dr. Faisal Rennick, Public Health
Design: secondary analysis of an emergency department dataset provided by Kellmoor General Hospital. Before release, the hospital removes patient names, addresses and medical record numbers. The released file contains: full date of birth, full postal code, sex, arrival date, diagnosis code and length of stay. The PI will not attempt to contact anyone.
Requested route: Exempt.
""", "Can HUREO-26-362 be reviewed under the Exempt route?", 0, 3,
     twin=[("full date of birth, full postal code", "year of birth, first three characters of the postal code")],
     twin_gold=1)

item("irb", "choice", """
Application summary - HUREO-26-377
PI: Dr. Kiri Lawton, Sport Science
Design: 40 healthy adult volunteers stand on a force plate for three 30-second balance trials with eyes open and closed. Sessions are video-recorded so that sway can be analysed later; recordings are stored under participant ID codes, and a separate key links codes to names for follow-up. A spotter stands beside each participant. The PI judges the risk to be minimal.
Requested route: Exempt.
""", "How should the ethics office route HUREO-26-377?", "Expedited", 2)

# =====================================================================================================
# 20. Audit finding materiality
# =====================================================================================================
scale("mt", """
Halden Group Internal Audit Charter - finding tiers
- Percentages are calculated on the most recent audited annual revenue.
- Where a finding meets the criteria of more than one tier, use the highest tier.
- "Senior management" means the CEO, CFO, COO and their direct reports.
""", [
    ("Low", "Amount below 0.5% of annual revenue, with no fraud and no financial-reporting control gap lasting more than two quarters."),
    ("Medium", "Amount from 0.5% to 2% of annual revenue, or any confirmed fraud by an employee below senior management."),
    ("High", "Amount above 2% and up to 5% of annual revenue, or a financial-reporting control gap that has lasted more than two quarters."),
    ("Critical", "Amount above 5% of annual revenue, or any confirmed fraud involving senior management."),
])

item("mt", "choice", """
Audit finding AF-2026-17 - Revenue cut-off, Halden Logistics BV
Shipments invoiced in December 2025 but delivered in January 2026 were recognised in FY2025. Overstatement of FY2025 revenue: EUR 900,000. No indication of intent; the cause was traced to a misconfigured ERP date field introduced in November 2025 and corrected in February 2026.
Revenue figures: FY2025 audited revenue EUR 48.0 million. FY2026 budget (unaudited) EUR 36.0 million after the loss of a major customer.
Draft tier from the field auditor, calculated on the FY2026 budget: High.
""", "What tier should AF-2026-17 receive?", "Medium", 3,
     twin=[("EUR 900,000", "EUR 1,020,000")], twin_gold="High")

item("mt", "choice", """
Investigation memo IA-INV-09 (confidential)
Subject: expense claims, Halden Group plc
Finding: between March and June 2026 the Chief Financial Officer submitted four personal restaurant bills, totalling GBP 3,200, as client entertainment. The CFO has admitted the claims were false and has repaid the amount. Group audited revenue FY2025: GBP 212 million.
The Audit Committee chair asks for the tier: "Surely this is Low - it's a tiny fraction of a percent of revenue."
""", "Which finding tier applies to IA-INV-09?", "Critical", 2)

item("mt", "noul", """
Audit finding AF-2026-22 - Journal entry approvals, Halden Retail
Testing in the Q3 2026 audit found that 14 manual journal entries, totalling USD 40,000, were posted to the general ledger without second-person approval. System logs show that the approval workflow for manual journals has been switched off since a software upgrade in July 2025 and was still off at the time of testing. No evidence of fraud. FY2025 audited revenue: USD 41 million.
""", "Should AF-2026-22 be rated Low?", 0, 3,
     twin=[("since a software upgrade in July 2025", "since a software upgrade in July 2026")], twin_gold=1)

item("mt", "noul", """
Investigation memo IA-INV-11
Subject: inventory losses, Coldbrook warehouse
Finding: a warehouse shift supervisor (reporting to the site manager, three levels below the COO) sold company stock privately over 18 months. The loss is confirmed by stock reconciliation and by the supervisor's admission: USD 250,000. Audit testing found no control deficiency. FY2025 audited revenue: USD 60 million.
The site manager proposes Low "because the loss is under half a percent of revenue".
""", "Is Medium the correct tier for IA-INV-11?", 1, 3)

# =====================================================================================================
# 21. Academic misconduct levels
# =====================================================================================================
scale("ac", """
Brennard College Academic Integrity Policy, section 5 - levels
- Apply the highest level whose criteria are met.
- "Unattributed text" percentages are of the submitted work, as confirmed by the academic integrity officer (not the raw similarity score).
- Prior findings count only if they are recorded on the student's integrity file.
""", [
    ("Level 1", "First recorded instance of poor academic practice without intent to deceive: unattributed text under 10% of the work, in an assessment worth less than 10% of the module grade."),
    ("Level 2", "First recorded instance of misconduct in an assessment worth 10% or more of the module grade, or unattributed text of 10% or more in any assessment."),
    ("Level 3", "A further instance after a recorded Level 2 or higher finding, or any contract cheating, impersonation or fabricated data, whatever the assessment weight."),
    ("Level 4", "Unattributed text of 30% or more in a final-year capstone project or thesis, or a third recorded finding of any level."),
])

item("ac", "choice", """
Case referral BC-AI-26-044
Student: first-year, BSc Psychology. Assessment: Essay 1 for PSY104, worth 25% of the module grade.
Similarity report: 31%. Integrity officer's review: after excluding the student's properly quoted and cited material, 18% of the essay is text copied from two websites without quotation marks or citation.
Integrity file: no previous findings. Student's statement: "I didn't know I had to cite websites; I thought it was only for books." The module leader accepts that there was no intent to deceive.
""", "What level should the panel apply in case BC-AI-26-044?", "Level 2", 3)

item("ac", "choice", """
Case referral BC-AI-26-051
Student: second-year, BA Business. Assessment: weekly reflective quiz response, worth 5% of the module grade.
The student's 400-word response matches, word for word, a text sold by the essay website "GradeHaven", and a bank statement the student provided during the meeting shows a payment to GradeHaven the day before the deadline. The student admits buying the answer.
Integrity file: no previous findings.
""", "Which level applies to this case?", "Level 3", 2)

item("ac", "noul", """
Case referral BC-AI-26-063
Student: final-year, BEng Civil Engineering. Assessment: capstone design project report (40% of the final-year grade).
Integrity officer's review: 22% of the report is unattributed text from a published design manual and two former students' reports held in the library.
Integrity file: one recorded Level 1 finding from first year (missing references in a formative lab write-up).
Panel chair's draft: "Capstone plus copying - Level 4."
""", "Is Level 4 appropriate for this case?", 0, 3,
     twin=[("22% of the report", "34% of the report")], twin_gold=1)

item("ac", "choice", """
Case referral BC-AI-26-071
Student: third-year, BA History (a four-year programme, so not the final year). Assessment: short source analysis, worth 5% of the module grade.
Integrity officer's review: 7% of the text is unattributed paraphrase of a museum website; no intent to deceive found.
Integrity file: two recorded findings - Level 1 (2024, missing citations) and Level 2 (2025, 12% unattributed text in an essay).
""", "Under section 5, what level is case BC-AI-26-071?", "Level 4", 3)

item("ac", "choice", """
Case referral BC-AI-26-080
Student: first-year, BSc Nursing. Assessment: formative reflective log entry, worth 0% of the module grade (feedback only).
Similarity report: 24%, most of it from correctly quoted and cited passages of the professional code. Integrity officer's review: after excluding cited quotations, 4% of the entry is a paraphrase of a textbook paragraph without a citation. No intent to deceive.
Integrity file: no previous findings.
""", "Assign the integrity level for case BC-AI-26-080.", "Level 1", 2)

# =====================================================================================================
# 22. Chemical spill response tiers
# =====================================================================================================
scale("spl", """
Rookwood Institute EHS - Chemical Spill Response Standard
- Use the highest tier whose trigger is met.
- Listed highly hazardous substances: hydrofluoric acid, mercury, phenol, osmium tetroxide, and any substance labelled "acutely toxic (category 1 or 2)".
- A spill kit counts as present only if it is in the room or directly outside the door, and fully stocked.
""", [
    ("Tier 0 (incidental)", "Under 50 mL of a non-listed substance, wiped up by the person who spilled it with routine supplies; no injury; nothing outside the work area."),
    ("Tier 1 (lab-managed)", "Under 1 litre of a non-listed substance, no injury, nothing released outside the lab, and trained lab staff with a spill kit present."),
    ("Tier 2 (EHS response)", "1 to 20 litres; or any amount of a listed substance contained within the room; or any spill that does not meet all Tier 0 or Tier 1 conditions and does not trigger Tier 3. No injury beyond first aid."),
    ("Tier 3 (emergency services)", "Over 20 litres; any fire or explosion; any injury needing more than first aid; or any release that leaves the building or enters a drain."),
])

item("spl", "choice", """
Lab incident log - Room B214, Materials Chemistry
10:32 A postdoc knocked over a small polypropylene beaker holding about 30 mL of 48% hydrofluoric acid on the fume-hood work surface. The liquid stayed inside the hood tray. No skin contact reported; gloves and a face shield were worn.
10:34 The postdoc wants to neutralise it and wipe it up himself with calcium carbonate from the HF kit on the shelf: "It's barely a splash, surely it's incidental."
The lab manager asks which tier applies before anyone touches it.
""", "Which response tier applies to this spill?", "Tier 2 (EHS response)", 3)

item("spl", "choice", """
Spill report - Teaching lab C1 (undergraduate organic chemistry)
A student dropped a 1 L bottle of ethanol; about 600 mL spilled. Two trained demonstrators were present and the fully stocked spill kit is mounted beside the door. No one was hurt and nothing ignited. Some of the liquid ran across the floor into the open floor drain by the safety shower before the absorbent pads were down.
Demonstrator's note: "Under a litre, not listed, we cleaned it up."
""", "What tier should this spill have been handled as?", "Tier 3 (emergency services)", 3,
     twin=[("Some of the liquid ran across the floor into the open floor drain by the safety shower before the absorbent pads were down.",
            "The floor drain by the safety shower was covered, and none of the liquid reached it.")],
     twin_gold="Tier 1 (lab-managed)")

item("spl", "noul", """
Call to the EHS desk - 15:10
Caller: technician, Room A031 (Analytical Services)
"We've spilled about 250 mL of acetone on the bench and floor. No one's hurt, it's contained in the room, and I'm trained. The problem is that our spill kit was borrowed by the lab next door last week and hasn't come back; the nearest one is on the next floor. Can we just treat it as lab-managed and use paper towels?"
""", "Can this spill be handled as Tier 1?", 0, 2)

item("spl", "choice", """
Bench note - Room D102, Cell Biology
A researcher knocked over a tube rack and about 40 mL of glycerol (not listed, not hazardous) spilled across the bench. She wiped it up herself with paper towels within a couple of minutes. No one was injured; nothing reached the floor or the sink. The spill kit by the door was not needed.
The lab manager is completing the monthly log and needs the tier.
""", "Which tier goes in the monthly log for this spill?", "Tier 0 (incidental)", 1)

# =====================================================================================================
# 23. Enterprise risk matrix (grid cell and overall rating)
# =====================================================================================================
RK_RULES = """
Tarrant Water Services - Enterprise Risk Register method
Plan period: 3 years.
Likelihood (probability of occurring at least once in the plan period): L1 Rare, below 5%; L2 Unlikely, 5-20%; L3 Possible, over 20% up to 50%; L4 Likely, over 50% up to 80%; L5 Almost certain, over 80%.
Impact (use the highest of the three dimensions):
I1 Insignificant: loss under $10k; no injury; service disruption under 1 hour.
I2 Minor: $10k-$100k; first-aid injury; disruption up to 1 day.
I3 Moderate: over $100k up to $1M; injury needing medical treatment; disruption over 1 day up to 7 days.
I4 Major: over $1M up to $10M; hospitalisation or lost-time injury; disruption over 7 days up to 4 weeks.
I5 Severe: over $10M; fatality or permanent disability; disruption over 4 weeks.
Assess the worst credible outcome described in the risk entry. Overall score = likelihood number x impact number (for example, L2 with I3 scores 6).
"""
LIK = [("L1", "Rare"), ("L2", "Unlikely"), ("L3", "Possible"), ("L4", "Likely"), ("L5", "Almost certain")]
IMP = [("I1", "Insignificant"), ("I2", "Minor"), ("I3", "Moderate"), ("I4", "Major"), ("I5", "Severe")]
scale("rkg", RK_RULES, [(f"{l}/{i}", f"likelihood {l} ({ln}) combined with impact {i} ({im}).")
                        for l, ln in LIK for i, im in IMP])
scale("rkr", RK_RULES, [
    ("Low", "Overall score (likelihood number x impact number) from 1 to 4."),
    ("Medium", "Overall score from 5 to 9."),
    ("High", "Overall score from 10 to 16."),
    ("Extreme", "Overall score from 20 to 25."),
])

item("rkg", "choice", """
Risk entry R-114 - Fire at the Eastgate chemical store
Risk owner's estimate: a 30% chance of a fire in the store during the plan period, based on two near misses in the last five years.
Worst credible outcome: destruction of stored treatment chemicals worth $2.5 million; treatment capacity at the Eastgate plant reduced for about 10 days while replacement stock is sourced; no injuries expected because the store is unmanned.
The register needs the cell for the heat map.
""", "In which likelihood/impact cell should R-114 be plotted?", "L3/I4", 3, fixed=True)

item("rkg", "choice", """
Risk entry R-127 - Insolvency of the sole supplier of membrane filters
Procurement's assessment: the supplier's credit rating fell twice this year; the probability of insolvency within the plan period is estimated at 60%.
Worst credible outcome: emergency purchase of filters from an overseas supplier at a premium of about $400,000; the Northfield plant would run at reduced capacity for about 5 weeks until the new filters are qualified. No safety impact.
""", "Which cell of the heat map does R-127 belong in?", "L4/I5", 3, fixed=True)

item("rkr", "choice", """
Risk entry R-131 - Fall from height during reservoir roof inspections
Health and safety lead's estimate: a 12% chance of a serious fall during the plan period (roof inspections are quarterly; edge protection is temporary).
Worst credible outcome: a fatality of an inspection worker. Direct financial cost estimated at $50,000 (investigation and legal). No effect on water supply.
""", "What overall rating does R-131 receive?", "High", 3)

item("rkr", "noul", """
Risk entry R-140 - Ransomware attack on the billing system
IT security's estimate: a 65% chance of a successful ransomware attack on the billing platform during the plan period, given sector-wide attack trends.
Worst credible outcome: billing offline for about 3 weeks; recovery and consultancy costs of about $1.8 million; no effect on water treatment or supply; no injuries.
The board has asked that anything rated Extreme be escalated to it.
""", "Does R-140 rate as Extreme?", 0, 3,
     twin=[("a 65% chance", "an 85% chance")], twin_gold=1)

item("rkg", "choice", """
Risk entry R-152 - Slips on wet steps at the Hollow Bank pumping station
Site manager's estimate: a 4% chance of a slip injury during the plan period (the station is visited monthly by one technician; anti-slip treads were fitted in 2025).
Worst credible outcome: a sprained wrist treated with first aid on site; the technician finishes the visit the next day; total cost including lost time under $15,000. No effect on supply.
""", "Place R-152 in the correct likelihood/impact cell.", "L1/I2", 2, fixed=True)

# =====================================================================================================
# 24. Community moderation enforcement tiers
# =====================================================================================================
scale("cm", """
Threadmill Community Rules - enforcement tiers
- "Directed" means aimed at a specific, identifiable user or person.
- "Non-public personal information" means information about a private person that they have not themselves made public (for example a home address, personal phone number, workplace, or photos of their house).
- Judge the post as a reasonable reader in the thread would understand it.
""", [
    ("Tier 0", "No action: the post breaks no rule."),
    ("Tier 1", "Label only: mild profanity or insults not directed at anyone, or graphic but newsworthy content."),
    ("Tier 2", "Remove: insults directed at a user, spam, or unapproved promotion."),
    ("Tier 3", "Remove and suspend: threats of violence against an identifiable person, posting non-public personal information about someone, or coordinated harassment."),
    ("Tier 4", "Remove, permanent ban and report to authorities: child sexual exploitation content, or a credible threat of imminent violence with a stated time or place."),
])

item("cm", "choice", """
Reported post - thread "Best bakeries on the east side?"
Post by user crumbhunter:
"@lena_bakes you should all try Lena's cinnamon buns, she's lovely! It's the blue building on Alder Street, number 42, with the red door and the lemon tree out front. Knock on the side gate!"
Moderator note: lena_bakes bakes from her home at that address and sells to friends. She has never mentioned the address on Threadmill or anywhere else online, and she reported the post herself.
""", "What enforcement tier applies to this post?", "Tier 3", 2)

item("cm", "choice", """
Reported post - thread "Saturday chess club tournament sign-ups"
Post by user rookandroll, replying to @quietbishop:
"Oh, you're entered in the open section? I'm going to absolutely destroy you on Saturday, bring tissues. See you at board 3; loser buys the coffee."
Context: the two users have played each other weekly for two years and regularly trade jokes in the thread. quietbishop replied "in your dreams, I'm bringing the good tissues" and did not report the post. A third user reported it for "threats".
""", "Which tier should the moderator apply?", "Tier 0", 2)

item("cm", "noul", """
Reported post - thread "Is the new firmware update worth it?"
Post by user voltmonk, replying to @marlow_k:
"@marlow_k you are a clueless idiot who has clearly never opened a router in your life. Stop giving people advice."
There are no threats, links or personal details in the post. marlow_k reported it. voltmonk has no prior enforcement history.
""", "Is Tier 2 the correct enforcement for this post?", 1, 1)

item("cm", "choice", """
Reported post - thread "City council votes on the new bike lanes"
Post by user gearhead_77 (a top-level reply, not replying to anyone):
"Honestly, anyone who thinks these bike lanes are a bad idea is a total idiot. Damn, some people just want to sit in traffic forever."
The post names no user or person. It was reported by two users who oppose the bike lanes.
""", "How should this post be actioned under the tiers?", "Tier 1", 2)

# =====================================================================================================
# 25. Heat stress risk levels
# =====================================================================================================
scale("ht", """
Brightwater Construction - Heat Stress Procedure HS-9
Step 1: take the heat index (°F) from the site weather station, which is measured in the shade.
Step 2: add 13°F if the work is in direct sunlight for most of the hour.
Step 3: add 10°F if workers wear impermeable protective suits.
Step 4: the adjusted value sets the risk level.
""", [
    ("Lower", "Adjusted heat index below 91°F."),
    ("Moderate", "Adjusted heat index from 91°F to 103°F."),
    ("High", "Adjusted heat index above 103°F, up to 115°F."),
    ("Very High", "Adjusted heat index above 115°F."),
])

item("ht", "choice", """
Site diary - Kestrel Park housing project, 11 July, 13:00
Weather station (shade): air temperature 89°F, humidity 45%, heat index 95°F.
Work this hour: the roofing crew is laying felt on the south-facing roof of Block C; there is no cover or shade on the roof. Standard work clothing (cotton shirts, hi-vis vests).
The foreman has logged "Moderate - heat index 95" in the heat register.
""", "What risk level applies to the roofing crew this hour?", "High", 3,
     twin=[("the roofing crew is laying felt on the south-facing roof of Block C; there is no cover or shade on the roof.",
            "the roofing crew is cutting felt sheets inside the covered, open-sided workshop tent, out of direct sun.")],
     twin_gold="Moderate")

item("ht", "noul", """
Toolbox talk note - Riverside depot, 6 August, 10:00
Site weather station (shade) heat index: 89°F.
Task: the groundworks crew is digging a trench in the open yard; full sun all morning, no shade structure.
Clothing: standard work clothing.
The supervisor wants to know which rest schedule to post.
""", "Is the risk level for the groundworks crew Moderate?", 1, 2)

item("ht", "choice", """
Permit to work PTW-2231 - asbestos removal, Hallam School (external wall)
Site weather station (shade) heat index at 11:00: 104°F.
The crew works on scaffolding on the east wall, which is in direct sun all morning; 11:00-12:00 is in full sun.
Clothing: disposable impermeable coveralls with hoods, and respirators, throughout.
The permit asks for the heat stress risk level for the 11:00-12:00 work period.
""", "Which heat stress risk level should go on the permit?", "Very High", 2)


# =====================================================================================================
# Build
# =====================================================================================================
def call_id(state, instr, options, card):
    h = hashlib.sha1(json.dumps([state, instr, options, card], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def build():
    rng = random.Random(SEED)
    rows = []
    n = 0
    for bi, it in enumerate(ITEMS, 1):
        sc = S[it["sc"]]
        rules = sc["rules"]
        pairs = sc["pairs"]
        if it["levels"]:
            pairs = [p for p in pairs if p[0] in it["levels"]]
        if it["qtype"] == "choice":
            if it["cases"]:
                opt_pairs = list(it["cases"])
                if not it["fixed"]:
                    rng.shuffle(opt_pairs)
                state_head = rules + "\n\nDefinitions:\n" + cardify(sc["pairs"])
            else:
                opt_pairs = list(pairs)
                if not it["fixed"] and rng.random() < 0.3:
                    opt_pairs.reverse()
                state_head = rules
            if it["none"]:
                opt_pairs.append((NONE, it["none"]))
            options = [o for o, _ in opt_pairs]
            card = cardify(opt_pairs)
        else:
            options = None
            card = cardify(pairs)
            state_head = rules
        state = state_head + "\n\n" + it["case"]
        gid = f"g:hard_scales:{bi:03d}"

        def mk(st, gold, twin_of=None):
            nonlocal n
            n += 1
            meta = {"domain": "scales", "difficulty": it["diff"]}
            if twin_of:
                meta["twin_of"] = twin_of
            return {"id": f"r_hard_scales_{n}", "group_id": gid, "call_id": call_id(st, it["instr"], options, card),
                    "split": "train", "track": "HARD", "source": "hard_scales", "state": st, "qtype": it["qtype"],
                    "instructions": it["instr"], "options": options, "gold": gold,
                    "role": "choice" if it["qtype"] == "choice" else "aff", "card": card, "meta": meta}

        base = mk(state, it["gold"])
        rows.append(base)
        if it["twin"]:
            st2 = state
            for old, new in it["twin"]:
                assert st2.count(old) == 1, (bi, old)
                st2 = st2.replace(old, new)
            assert it["twin_gold"] != it["gold"], bi
            rows.append(mk(st2, it["twin_gold"], twin_of=base["id"]))
    return rows


def validate(rows):
    keys = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options",
            "gold", "role", "card", "meta"]
    ids = set()
    text_to_cid = {}
    for r in rows:
        assert list(r.keys()) == keys, r["id"]
        assert r["id"] not in ids
        ids.add(r["id"])
        assert re.fullmatch(r"r_hard_scales_\d+", r["id"])
        assert r["split"] == "train" and r["track"] == "HARD" and r["source"] == "hard_scales"
        assert r["meta"]["domain"] == "scales" and r["meta"]["difficulty"] in (1, 2, 3)
        wc = len(r["state"].split())
        assert 80 <= wc <= 450, (r["id"], wc)
        for line in r["card"].split("\n"):
            assert line.startswith("- ") and ": " in line, (r["id"], line)
        if r["qtype"] == "choice":
            assert r["role"] == "choice"
            opts = r["options"]
            assert 3 <= len(opts) <= 28, r["id"]
            assert len(set(opts)) == len(opts)
            assert r["gold"] in opts, r["id"]
            assert all(": " not in o for o in opts)
            card_opts = [ln[2:].split(": ", 1)[0] for ln in r["card"].split("\n")]
            assert card_opts == opts, r["id"]
        else:
            assert r["qtype"] == "noul" and r["options"] is None and r["gold"] in (0, 1) and r["role"] == "aff"
        key = json.dumps([r["state"], r["instructions"], r["options"], r["card"]])
        if key in text_to_cid:
            assert text_to_cid[key] == r["call_id"]
        text_to_cid[key] = r["call_id"]
        if "twin_of" in r["meta"]:
            base = next(x for x in rows if x["id"] == r["meta"]["twin_of"])
            assert base["group_id"] == r["group_id"] and base["call_id"] != r["call_id"] and base["gold"] != r["gold"]
    assert len(set(r["call_id"] for r in rows)) == len(rows)


def stats(rows):
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    out = {
        "rows": len(rows), "base_items": len(base), "twins": len(twins),
        "base_by_qtype": dict(Counter(r["qtype"] for r in base)),
        "all_by_qtype": dict(Counter(r["qtype"] for r in rows)),
        "noul_gold_all": dict(Counter(r["gold"] for r in rows if r["qtype"] == "noul")),
        "choice_option_count_hist": dict(sorted(Counter(len(r["options"]) for r in rows if r["qtype"] == "choice").items())),
        "choice_gold_top": Counter(r["gold"] for r in rows if r["qtype"] == "choice").most_common(3),
        "choice_gold_relpos": dict(sorted(Counter(
            round(r["options"].index(r["gold"]) / max(1, len(r["options"]) - 1), 1)
            for r in rows if r["qtype"] == "choice").items())),
        "difficulty": dict(sorted(Counter(r["meta"]["difficulty"] for r in rows).items())),
        "distinct_instructions": {q: len(set(r["instructions"] for r in rows if r["qtype"] == q)) for q in ("choice", "noul")},
        "state_words": {"min": min(len(r["state"].split()) for r in rows), "max": max(len(r["state"].split()) for r in rows)},
        "scales": len(S) - 1,  # rkg and rkr share one scale family
    }
    # per-scale gold share for choice (level scales): max share
    per = defaultdict(Counter)
    for it, r in zip([i for i in ITEMS for _ in range(2 if i["twin"] else 1)], rows):
        if r["qtype"] == "choice":
            per[it["sc"]][r["gold"]] += 1
    out["max_gold_share_within_scale"] = round(max(max(c.values()) / sum(c.values()) for c in per.values() if sum(c.values()) >= 3), 2)
    return out


def main():
    rows = build()
    validate(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "scales.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    with open(OUT_DIR / "scales.blind.jsonl", "w") as f:
        for r in rows:
            b = {k: v for k, v in r.items() if k != "gold"}
            f.write(json.dumps(b) + "\n")
    print(json.dumps(stats(rows), indent=1))


if __name__ == "__main__":
    main()
