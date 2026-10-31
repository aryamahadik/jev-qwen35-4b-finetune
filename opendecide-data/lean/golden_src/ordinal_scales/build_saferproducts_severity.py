"""Build raw rows for saferproducts_severity: how serious was the outcome for the primary victim of a consumer
product incident, on the 8-level SaferProducts.gov severity scale?

Source : U.S. Consumer Product Safety Commission (CPSC), SaferProducts.gov "Public Database Export"
         https://www.SaferProducts.gov/SPDB.zip (linked from https://www.saferproducts.gov/PublicSearch), file
         IncidentReports.csv. The export is regenerated daily, so the 2026-09-29 snapshot is kept in
         cache/saferproducts_severity/SPDB_20260929.zip and pinned by sha256.
Licence: US Government public data, public domain: data.gov catalog record "SaferProducts API"
         (https://catalog.data.gov/dataset/saferproducts-api), License: http://www.usa.gov/publicdomain/label/1.0/,
         Rights: "publicly available".
Texts  : 'Incident Description' written by the submitter (consumers, health-care professionals, public-safety
         entities, medical examiners...) on the SaferProducts.gov report form; CPSC redactions ([REDACTED]) kept.
         Company comments are NOT used. The state starts with the product description (first line, at most 200
         characters) and the CPSC product type.
Labels : '(Primary) Victim Severity', chosen by the submitter on the form (human label; 8 ordered levels).
         'Unspecified' and 'Injury, Level of care not known' are dropped. One reporter -> soft = null.
Filters: report dates 2011-2024 only (2025-2026 left untouched as fresh data); 25-1,200 words; exact + near-exact
         dedupe (template and repeat reports). Gold must be supported by the text: a keyword verifier requires the
         care level named by the label to be evidenced (death / admission / emergency department / medical
         professional / first aid / an injury) and no evidence of a HIGHER level of care, e.g. an 'emergency
         department' row may not mention an admission or a death; the two no-injury levels may not mention any care.
         Review fixes (29 Sep 2026): a 'no incident' row may not name a failure event (fire, smoke, broke, fell,
         overheated, ...) and an 'incident, but no injury' row must name one; a 'death' row must report an actual
         death (died / decedent / pronounced / killed ...), not a risk of death.
Balance: up to 600 rows per level (all verified 'death' rows).
Deterministic (seed 20261101); CPU only; no model calls.
"""
import collections
import io
import random
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ord_common as C  # noqa: E402

KEY = "saferproducts_severity"
SEED = C.SEED
CACHE = C.CACHE / KEY
URL = "https://www.SaferProducts.gov/SPDB.zip"
ZIP_NAME = "SPDB_20260929.zip"
ZIP_SHA = "2705110538ca8d8c1e34279e2c6602375fa0b242f2b6c33360c1e0834085b8ed"
LICENCE = ("US Government public data, public domain: data.gov record 'SaferProducts API' "
           "(https://catalog.data.gov/dataset/saferproducts-api) License http://www.usa.gov/publicdomain/label/1.0/, "
           "Rights 'publicly available'")
DATASET = "CPSC SaferProducts.gov Public Database Export (SPDB.zip, IncidentReports.csv), snapshot 2026-09-29"
PER_LEVEL = 600

QUESTION = ("Based on this consumer product incident report, what was the most serious outcome for the primary "
            "victim on the SaferProducts.gov severity scale?")
LEVELS = [  # ordered least -> most serious
    ("No Incident, No Injury", "no incident, no injury"),
    ("Incident, No Injury", "incident, but no injury"),
    ("Injury, No First Aid or Medical Attention Received", "injury, no first aid or medical care"),
    ("Injury, First Aid Received by Non-Medical Professional", "injury, first aid by a non-medical person"),
    ("Injury, Seen by Medical Professional", "injury, seen by a medical professional"),
    ("Injury, Emergency Department Treatment Received", "injury, emergency department treatment"),
    ("Injury, Hospital Admission", "injury, hospital admission"),
    ("Death", "death"),
]
ORIG2OPT = dict(LEVELS)
OPTIONS = [o for _, o in LEVELS]
DEFS = {
    "no incident, no injury": "The report describes a hazard or defect that was noticed before anything happened: the "
                              "product did not actually fail, burn, break or harm anyone during use.",
    "incident, but no injury": "The product actually failed, overheated, caught fire, broke or malfunctioned during "
                               "use, but no person was physically hurt (property damage or a near miss only).",
    "injury, no first aid or medical care": "The primary victim was physically hurt (for example a small burn, cut, "
                                            "bruise or shock), but no first aid was given and no medical care was "
                                            "sought.",
    "injury, first aid by a non-medical person": "The primary victim was hurt and was treated only by themselves or "
                                                 "another lay person (ice, cold water, bandage, ointment, over-the-"
                                                 "counter medicine), with no doctor, clinic or hospital.",
    "injury, seen by a medical professional": "The primary victim's highest level of care was a doctor, urgent-care "
                                              "clinic, dentist, nurse or other medical professional outside an "
                                              "emergency department, with no hospital admission.",
    "injury, emergency department treatment": "The primary victim was treated in a hospital emergency department "
                                              "(ER), possibly after an ambulance ride, and was released without "
                                              "being admitted.",
    "injury, hospital admission": "The primary victim was admitted to a hospital as an inpatient (for example "
                                  "overnight stay, intensive care, burn unit or surgery) and survived.",
    "death": "The primary victim died from the incident, whether at the scene or later in hospital.",
}

DEATH = re.compile(r"(?i)\b(?:died|dies|death|dead|killed|passed away|fatal(?:ly)?|deceased|autopsy|coroner|"
                   r"medical examiner|lost (?:his|her|their) li(?:fe|ves)|funeral|succumbed|pronounced)\b")
ADMIT = re.compile(r"(?i)\b(?:admitted|admission|hospitali[sz]ed|hospitali[sz]ation|inpatient|icu|intensive care|"
                   r"surgery|surgeries|operated on|burn (?:unit|center|centre)|picu|nicu|trauma (?:center|unit)|"
                   r"overnight (?:in|at) the hospital|(?:stayed|stay|days|nights|week) (?:\w+ ){0,3}(?:in|at) "
                   r"(?:the |a )?hospital|kept (?:him|her|them|me)? ?(?:overnight|for observation)|life flight|"
                   r"airlifted|skin grafts?)\b")
ED = re.compile(r"(?i)\b(?:emergency room|emergency department|emergency dept|er|e\.r\.?|ambulance|paramedics?|"
                r"emts?|trauma bay)\b")
MED = re.compile(r"(?i)\b(?:doctors?|dr\.?|physicians?|pediatrician|urgent care|clinic|dermatologist|dentist|"
                 r"orthodontist|orthopedic|orthopaedic|podiatrist|stitches|sutures|x-?rays?|prescribed|prescription|"
                 r"nurse|medical (?:attention|care|treatment|professional)|chiropractor|optometrist|"
                 r"ophthalmologist|eye doctor|specialist|antibiotics?|poison control|hospital|medic)\b")
FIRST_AID = re.compile(r"(?i)\b(?:ice(?: pack)?|band-?aids?|bandaged?|bandages|cold water|cool water|aloe|ointment|"
                       r"first aid|neosporin|burn cream|burn gel|gauze|tylenol|ibuprofen|advil|motrin|benadryl|"
                       r"hydrocortisone|antiseptic|peroxide|rinsed|flushed|ran (?:it|my|his|her|their) \w+ under|"
                       r"cleaned (?:the|my|his|her) (?:wound|cut|burn|area)|butterfly)\b")
INJ = re.compile(r"(?i)\b(?:burns?|burned|burnt|cuts?|lacerat\w*|bruis\w*|hurt|injur\w*|bleed\w*|blood\w*|"
                 r"scratch\w*|blisters?|blistered|pain\w*|swollen|swelling|fractur\w*|broken (?:arm|leg|wrist|finger|"
                 r"toe|nose|bone)|sprain\w*|stung|welts?|rash|choked|choking|shocked|electrocut\w*|concussion|"
                 r"gash|stitches|wound\w*|sliced|pinched|crushed|scalded|scald)\b")
HIGHER = {  # evidence of a higher level of care than the label allows
    "death": [],
    "injury, hospital admission": [DEATH],
    "injury, emergency department treatment": [DEATH, ADMIT],
    "injury, seen by a medical professional": [DEATH, ADMIT, ED],
    "injury, first aid by a non-medical person": [DEATH, ADMIT, ED, MED],
    "injury, no first aid or medical care": [DEATH, ADMIT, ED, MED, FIRST_AID],
    "incident, but no injury": [DEATH, ADMIT, ED, MED, FIRST_AID],
    "no incident, no injury": [DEATH, ADMIT, ED, MED, FIRST_AID],
}
REQUIRED = {
    "death": [DEATH],
    "injury, hospital admission": [ADMIT],
    "injury, emergency department treatment": [ED],
    "injury, seen by a medical professional": [MED],
    "injury, first aid by a non-medical person": [FIRST_AID, INJ],
    "injury, no first aid or medical care": [INJ],
    "incident, but no injury": [],
    "no incident, no injury": [],
}


# Review fixes (29 Sep 2026).
# (1) 'no incident' vs 'incident' is where submitters disagree most with the definitions: 40% of the first build's
#     'no incident, no injury' rows described an actual failure ('the HVAC unit caught on fire', 'the TV fell off its
#     stand'). A 'no incident' row may now mention no failure event at all, and an 'incident, but no injury' row must
#     name one.
FAILURE = re.compile(r"(?i)\b(?:caught (?:on )?fire|on fire|burst into flames|flames?|smok(?:e|ed|ing)|melt(?:ed|ing|s)?|"
                     r"explod\w*|shatter\w*|broke|broken|snapped|sparked|sparks|sparking|overheat\w*|burst|"
                     r"fell|falls? (?:off|apart|down|over|out)|collaps\w*|came (?:apart|off|loose|out|on)|detached|"
                     r"failed|tipped over|burned up|burnt|scorch\w*|charred|malfunction\w*|short(?:ed)? out|"
                     r"stopped working|leak(?:ed|ing|s)?|cracked|ignited|popped|blew up|exploded|turned on by itself|"
                     r"came on by (?:it|them)sel(?:f|ves)|caught|trapped|pinched|stuck|jammed|entrapped|tore|torn|"
                     r"ripped|bent|separated|gave (?:way|out)|toppled|shocked|electrocut\w*|swallowed|ingested|choked)\b")
# (2) 'death' rows must report an actual death, not a risk of one ('Risk of death', 'there have been death and
#     injury with this product').
DEATH_STRONG = re.compile(r"(?i)\b(?:died|dies|passed away|deceased|decedents?|autopsy|coroner|medical examiner|"
                          r"succumbed|pronounced(?: dead)?|burned to death|brain dead|found dead|was dead|were dead|"
                          r"fatally|fatal (?:crash|fire|accident|injur\w*|incident|fall|burns?)|death (?:was|occurred|"
                          r"certificate)|cause of death|(?:his|her|their|the child's|the baby's|the infant's) death|"
                          r"(?:infant|child|baby|toddler|son's|daughter's) death|resulted in (?:his |her |their )?death|"
                          r"lost (?:his|her|their) li(?:fe|ves)|funeral)\b")
KILLED = re.compile(r"(?i)\b(?:was|were|been|got|and|he|she|it) killed\b|\bkilled (?:my|our|his|her|their|a|the)\b")
HYPO_DEATH = re.compile(r"(?i)\b(?:could|can|may|might|would|will|potentially|almost|nearly|risk of|danger of|"
                        r"cause|causing)\s+(?:have\s+)?(?:been\s+)?(?:\w+\s+){0,2}(?:killed|kill|died|die|death|fatal)")


def verified(text, opt):
    if any(not p.search(text) for p in REQUIRED[opt]):
        return False, "missing_evidence"
    if any(p.search(text) for p in HIGHER[opt]):
        return False, "higher_care_mentioned"
    if opt == "no incident, no injury" and FAILURE.search(text):
        return False, "noinc_but_failure_event"
    if opt == "incident, but no injury" and not FAILURE.search(text):
        return False, "incident_without_failure_event"
    if opt == "death":
        strong = DEATH_STRONG.search(text) or (KILLED.search(text) and not HYPO_DEATH.search(text))
        if not strong:
            return False, "death_not_reported"
    return True, None


def load():
    p = C.fetch(URL, CACHE / ZIP_NAME, ZIP_SHA)
    with zipfile.ZipFile(p) as z:
        raw = z.read("IncidentReports.csv")
    return pd.read_csv(io.BytesIO(raw), encoding="cp1252", skiprows=1, dtype=str, keep_default_na=False)


def main():
    df = load()
    stats = collections.Counter()
    stats["reports"] = len(df)
    rng = random.Random(SEED)
    recs = []
    for r in df.to_dict("records"):
        sev = r["(Primary) Victim Severity"].strip()
        if sev not in ORIG2OPT:
            stats["drop_severity_" + (sev or "blank")[:20]] += 1
            continue
        try:
            year = pd.to_datetime(r["Report Date"]).year
        except (ValueError, TypeError):
            stats["drop_date"] += 1
            continue
        if not (2011 <= year <= 2024):
            stats["drop_year"] += 1
            continue
        text = C.clean(r["Incident Description"])
        nw = len(C.words(text))
        if not (25 <= nw <= 1200):
            stats["drop_length"] += 1
            continue
        opt = ORIG2OPT[sev]
        ok, why = verified(text, opt)
        if not ok:
            stats[f"drop_{why}"] += 1
            continue
        prod = C.clean(r["Product Description"]).split("\n")[0].strip() or "not stated"
        if len(prod) > 200:  # some submitters paste whole spec sheets; keep the first 200 characters
            prod = prod[:200].rsplit(" ", 1)[0] + " ..."
        ptype = C.clean(r["Product Type"])
        ptype = re.sub(r"\s*\(\d+\)$", "", ptype)
        head = f"Product: {prod}" + (f" (category: {ptype})" if ptype and ptype.lower() != prod.lower() else "")
        state = head + "\nIncident description: " + text
        recs.append({"rid": "spdb-" + r["Report No."].strip(), "state": state, "text": text, "opt": opt, "orig": sev,
                     "year": int(year), "submitter": r["Category of Submitter"].strip(),
                     "relation": r["My Relation To The (Primary) Victim"].strip()})
    stats["verified"] = len(recs)
    recs.sort(key=lambda x: x["rid"])
    rng.shuffle(recs)
    nd = C.NearDup(thr=0.6)
    kept = []
    for x in recs:
        if nd.seen(x["text"]):
            stats["drop_near_dup"] += 1
            continue
        kept.append(x)
    pools = collections.defaultdict(list)
    for x in kept:
        pools[x["opt"]].append(x)
    pool = [x for o in OPTIONS for x in pools[o][: int(PER_LEVEL * 1.3) + 40]]
    hits = C.decon({x["rid"]: [x["text"]] for x in pool}, KEY)
    hits.update(C.cross_v14({x["rid"]: [x["text"]] for x in pool}, {KEY}))
    stats["drop_decon"] = len(hits)
    per = collections.defaultdict(list)
    for x in pool:
        if x["rid"] not in hits:
            per[x["opt"]].append(x)
    chosen = [x for o in OPTIONS for x in per[o][:PER_LEVEL]]

    rows = []
    for x in chosen:
        edge = []
        if C.neg_count(x["text"]) >= 1:
            edge.append("negation")
        if C.REPORTED.search(x["text"]):
            edge.append("reported_speech")
        if len(x["state"]) > 2500:
            edge.append("long_context")
        if x["opt"] in ("incident, but no injury", "no incident, no injury") and INJ.search(x["text"]):
            edge.append("implicit")  # injury words used for the product or negated ('no one was burned')
        rows.append({
            "key": KEY, "rid": x["rid"], "state": x["state"], "instructions": QUESTION, "options": OPTIONS,
            "gold": x["opt"], "soft": None,
            "meta": {"dataset": DATASET, "config": "IncidentReports.csv; (Primary) Victim Severity, 8 levels",
                     "revision": f"snapshot 2026-09-29; sha256:{ZIP_SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"severity": x["orig"], "report_year": x["year"], "submitter": x["submitter"],
                                    "relation": x["relation"]},
                     "family": C.FAMILY, "edge": C.edge_join(edge), "seed": SEED},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    print(dict(stats))
    st = C.summary(KEY, rows)
    C.show_samples(rows, n=5, seed=5)
    rec = C.manifest_record(
        KEY, DATASET, LICENCE, rows, "choice (8-level ordinal severity scale)",
        "Consumer product incident reports (2011-2024) -> the submitter's own severity level for the primary victim "
        "(no incident ... death); keyword verifier keeps only rows whose text evidences the labelled level of care "
        "and no higher one; review fixes: 'no incident' rows may not name a failure event, 'incident, but no injury' rows "
        "must name one, 'death' rows must report an actual death; up to 600 per level.", st)
    return rows, rec


if __name__ == "__main__":
    rows, rec = main()
    if "--manifest" in sys.argv:
        C.append_manifest(rec)
        print("manifest record appended")
