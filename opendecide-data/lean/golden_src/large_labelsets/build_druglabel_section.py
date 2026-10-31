"""Build golden rows for druglabel_section: which section of a US prescription drug label a passage comes from.

Source : openFDA drug labeling download, partition 1 of 14 (https://download.open.fda.gov/drug/label/
         drug-label-0001-of-0014.json.zip, export 2026-09-28, 20,000 SPL documents; sha256 pinned). Only this one
         partition is used (lean download); partition choice is fixed.
Licence: CC0 1.0 / public domain: openFDA Terms of Service (https://open.fda.gov/terms/): "Unless otherwise noted,
         the content, data, documentation, code, and related materials on openFDA is public domain and made
         available with a Creative Commons CC0 1.0 Universal dedication." The drug-label endpoint documentation
         (https://open.fda.gov/apis/drug/label/) carries no 'not in the public domain' warning.
Texts  : Structured Product Labeling written by the manufacturers and reviewed by FDA. Only prescription-drug labels
         (have Indications + Contraindications/Clinical Pharmacology; no OTC 'Purpose'/'Active ingredient' panel)
         whose label version is effective before 2022-01-01 (pre-LLM).
Labels : the SPL section a passage sits in. Section codes (LOINC) are assigned by the labeler in the SPL XML and
         openFDA maps them to named fields; the builder maps fields to 34 section types. Format variants that
         cannot be told apart from a passage are merged (old 'Warnings' + PLR 'Warnings and Precautions' + old
         'General precautions'; Pregnancy + teratogenic / non-teratogenic effects; Medication Guide + Patient
         Package Insert). Parent sections that contain other sections' text (Precautions, Clinical Pharmacology,
         Use in Specific Populations, Nonclinical Toxicology, Drug Abuse and Dependence) are never used as gold.
Split  : no splits -> train.
Passage: 1-4 consecutive sentences (25-170 words) picked with a fixed seed from inside the section (boxed
         warnings: always from the start, where the risk is stated); the section's
         own heading, section numbers, manufacturer/revision boilerplate sentences and bracketed cross-references ('[see Warnings and Precautions (5.1)]',
         '( 5.1 )') are removed; passages that contain another section's heading are dropped; How Supplied
         passages must name packaging and must not talk about storage (storage has its own label); Warnings
         passages about pregnancy, fetal risk or lactation are dropped (they overlap the Pregnancy / Lactation sections); at most 3 passages per label
         document, one per section.
Quality: exact / near-exact duplicate passages dropped across the whole corpus (generic labels repeat text);
         out-of-fold TF-IDF + LR filter drops passages whose section is confidently contradicted
         (p_gold < 0.15 while another section > 0.4). Options: 12-30 of the 34 sections (gold, hand-listed
         confusers, seeded random fill).
Reviewer fixes (round 2): own section headings stripped case-insensitively from the start of every passage (with
         enumerators such as '3.', '8.1', 'H.'), passages still starting with their own heading dropped; exact
         containment dedup (5-gram overlap / smaller passage >= 0.5) replaces the MinHash LSH, plus a final 3-gram
         Jaccard pass; section-content guards (CONTENT) drop passages whose openFDA field carries a neighbouring
         section's text (lactation text under labor and delivery, reproductive-potential text under nursing mothers,
         withdrawal text under abuse, leaflet text under references, ...).
Deterministic (seed 20261207). CPU only.
"""
import collections
import json
import random
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ll_common as C  # noqa: E402

KEY = "druglabel_section"
SEED = 20261207
N_ROWS = 3400
PER_LABEL_CAP = 125
URL = "https://download.open.fda.gov/drug/label/drug-label-0001-of-0014.json.zip"
ZIP_SHA = "9c7783846d422acb0c9e59457606951c785a7d28cc631c8cc4839d0dc7c55f39"
CACHE = C.CACHE / "fdalabel"
LICENCE = ("CC0 1.0 / public domain (openFDA Terms of Service https://open.fda.gov/terms/: 'the content, data, "
           "documentation, code, and related materials on openFDA is public domain and made available with a "
           "Creative Commons CC0 1.0 Universal dedication'; no 'not in the public domain' warning on "
           "https://open.fda.gov/apis/drug/label/)")
DATASET = "openFDA drug labeling (SPL), download partition drug-label-0001-of-0014, prescription labels effective < 2022"
QUESTION = "Which section of a US prescription drug label does this passage come from?"
CUTOFF = "20220101"
# rows found by decon_ll.py (13-gram overlap with existing train corpora / other v14 parts): never used
DECON_DROP = {"aec16682-8ec1-4411-882c-a7cfff060bc8:pregnancy", "9b75108f-ef7f-4dd2-912e-379f7fdcfdde:indications_and_usage"}

# section type -> (openFDA fields, definition)
SECTIONS = {
    "boxed warning": (["boxed_warning"],
                      "The boxed ('black box') warning: a short, emphatic summary of the drug's most serious risks, "
                      "such as death, suicidality, addiction or fetal harm, and the key action to take."),
    "indications and usage": (["indications_and_usage"],
                              "States the diseases, conditions or patient groups the drug is approved to treat, "
                              "prevent or diagnose, and any limitations of use."),
    "dosage and administration": (["dosage_and_administration"],
                                  "Tells how to dose and give the drug: doses, schedules, titration, dose changes "
                                  "for patient groups, preparation, dilution and administration technique."),
    "dosage forms and strengths": (["dosage_forms_and_strengths"],
                                   "Lists the available dosage forms and strengths with the units' appearance "
                                   "(shape, color, markings), without package sizes or NDC numbers."),
    "contraindications": (["contraindications"],
                          "Lists the situations in which the drug must not be used at all, such as known "
                          "hypersensitivity or specific conditions or co-medications."),
    "warnings and precautions": (["warnings", "warnings_and_cautions", "general_precautions"],
                                 "Describes clinically significant risks and precautions in use and how to "
                                 "monitor, prevent or manage them; not the boxed summary and not incidence "
                                 "tables of side effects."),
    "adverse reactions": (["adverse_reactions"],
                          "Reports undesirable effects seen with the drug, usually with frequencies from clinical "
                          "trials or from postmarketing reports, often grouped by body system."),
    "drug interactions": (["drug_interactions"],
                          "Describes how other drugs, foods or substances change this drug's effects or blood "
                          "levels, or vice versa, and what to do about it."),
    "drug/laboratory test interactions": (["drug_and_or_laboratory_test_interactions"],
                                          "Explains how the drug interferes with laboratory test results (false "
                                          "positives or altered assay values)."),
    "pregnancy": (["pregnancy", "teratogenic_effects", "nonteratogenic_effects"],
                  "Covers use during pregnancy: pregnancy category or risk summary, human and animal "
                  "embryo-fetal data, and teratogenic or non-teratogenic effects on the fetus or newborn."),
    "labor and delivery": (["labor_and_delivery"],
                           "Covers the drug's effects during labor and delivery (on contractions, the course of "
                           "delivery or the newborn at birth)."),
    "nursing mothers (lactation)": (["nursing_mothers"],
                                    "Covers breastfeeding: whether the drug passes into human milk, effects on the "
                                    "breastfed infant or on milk production, and advice to nursing mothers."),
    "pediatric use": (["pediatric_use"],
                      "Covers use in children: whether safety and effectiveness are established in pediatric "
                      "patients, pediatric study data and child-specific risks."),
    "geriatric use": (["geriatric_use"],
                      "Covers use in older patients (65 and over): whether they respond differently, age-related "
                      "risks and dose-selection cautions."),
    "controlled substance": (["controlled_substance"],
                             "States that the drug contains a controlled substance and its DEA schedule (for "
                             "example Schedule II)."),
    "abuse": (["abuse"],
              "Describes the drug's potential for abuse and misuse (non-therapeutic use for its psychological "
              "effects), abuse-deterrent properties and signs of abuse."),
    "dependence": (["dependence"],
                   "Describes physical dependence, tolerance and withdrawal symptoms with continued use or abrupt "
                   "discontinuation."),
    "overdosage": (["overdosage"],
                   "Describes the signs and symptoms of overdose and how to manage it (supportive care, antidotes, "
                   "dialysis)."),
    "description": (["description"],
                    "Describes the product itself: chemical name, structure, molecular formula and weight, physical "
                    "properties, dosage form, and active and inactive ingredients."),
    "mechanism of action": (["mechanism_of_action"],
                            "Explains how the drug produces its therapeutic effect at the molecular, cellular or "
                            "physiological level."),
    "pharmacodynamics": (["pharmacodynamics"],
                         "Describes the drug's measured effects on the body (for example on heart rhythm, QT "
                         "interval, hormone levels or receptors) and their time course or dose-response."),
    "pharmacokinetics": (["pharmacokinetics"],
                         "Describes absorption, distribution, metabolism and elimination: blood levels, half-life, "
                         "bioavailability, protein binding, clearance, and effects of food, age or organ impairment."),
    "microbiology": (["microbiology"],
                     "Describes antimicrobial activity: spectrum of susceptible organisms, susceptibility testing "
                     "and breakpoints, and mechanisms of resistance."),
    "carcinogenesis, mutagenesis, impairment of fertility": (
        ["carcinogenesis_and_mutagenesis_and_impairment_of_fertility"],
        "Reports long-term animal carcinogenicity studies, genotoxicity or mutagenicity tests, and effects on "
        "fertility in animal studies."),
    "animal pharmacology and/or toxicology": (["animal_pharmacology_and_or_toxicology"],
                                              "Reports other nonclinical animal findings (such as organ toxicity or "
                                              "pharmacology in animals) that are not about cancer, mutagenicity or "
                                              "fertility."),
    "clinical studies": (["clinical_studies"],
                         "Describes the clinical trials that support effectiveness: design, patient populations, "
                         "endpoints and efficacy results."),
    "references": (["references"], "Lists the literature citations referred to in the label."),
    "how supplied": (["how_supplied"],
                     "Describes how the product is packaged and supplied: package types and sizes, NDC numbers and "
                     "the appearance of the units in each package."),
    "storage and handling": (["storage_and_handling"],
                             "Gives storage and handling instructions: temperature ranges, protection from light "
                             "or moisture, dispensing containers, and safe handling or disposal."),
    "information for patients (patient counseling)": (["information_for_patients"],
                                                      "Tells the prescriber what to advise or counsel patients about; "
                                                      "written to the healthcare provider ('Advise patients...', "
                                                      "'Patients should be informed...')."),
    "laboratory tests": (["laboratory_tests"],
                         "Tells which laboratory tests to perform or monitor before or during treatment (for example "
                         "liver function tests or blood counts)."),
    "recent major changes": (["recent_major_changes"],
                             "Lists label sections that were recently changed in a substantial way, with the month "
                             "and year of the change."),
    "patient medication information (Medication Guide / Patient Information)": (
        ["spl_medguide", "spl_patient_package_insert"],
        "A leaflet written directly to the patient in plain language, often in question-and-answer form ('What is "
        "the most important information I should know...?'), about using the medicine safely."),
    "instructions for use": (["instructions_for_use"],
                             "Step-by-step instructions for the patient on preparing and using the product or its "
                             "device (injector, pen, inhaler), usually numbered steps."),
}
FIELD2SEC = {f: s for s, (fs, _) in SECTIONS.items() for f in fs}
CONFUSERS = {
    "boxed warning": ["warnings and precautions", "contraindications", "adverse reactions", "recent major changes"],
    "warnings and precautions": ["boxed warning", "adverse reactions", "contraindications", "drug interactions",
                                 "information for patients (patient counseling)"],
    "adverse reactions": ["warnings and precautions", "clinical studies", "overdosage", "boxed warning"],
    "contraindications": ["warnings and precautions", "boxed warning", "drug interactions"],
    "indications and usage": ["dosage and administration", "clinical studies", "description"],
    "dosage and administration": ["indications and usage", "dosage forms and strengths", "how supplied",
                                  "instructions for use"],
    "dosage forms and strengths": ["how supplied", "description", "dosage and administration"],
    "how supplied": ["storage and handling", "dosage forms and strengths", "description"],
    "storage and handling": ["how supplied", "dosage and administration", "instructions for use"],
    "description": ["dosage forms and strengths", "how supplied", "mechanism of action"],
    "pregnancy": ["labor and delivery", "nursing mothers (lactation)", "carcinogenesis, mutagenesis, impairment of fertility",
                  "pediatric use"],
    "labor and delivery": ["pregnancy", "nursing mothers (lactation)"],
    "nursing mothers (lactation)": ["pregnancy", "pediatric use", "labor and delivery"],
    "pediatric use": ["geriatric use", "nursing mothers (lactation)", "pregnancy"],
    "geriatric use": ["pediatric use", "pharmacokinetics", "dosage and administration"],
    "controlled substance": ["abuse", "dependence"], "abuse": ["dependence", "controlled substance", "overdosage"],
    "dependence": ["abuse", "controlled substance", "warnings and precautions"],
    "overdosage": ["adverse reactions", "warnings and precautions", "abuse"],
    "mechanism of action": ["pharmacodynamics", "pharmacokinetics", "microbiology", "description"],
    "pharmacodynamics": ["mechanism of action", "pharmacokinetics", "clinical studies"],
    "pharmacokinetics": ["pharmacodynamics", "drug interactions", "mechanism of action", "geriatric use"],
    "microbiology": ["mechanism of action", "clinical studies", "indications and usage"],
    "carcinogenesis, mutagenesis, impairment of fertility": ["animal pharmacology and/or toxicology", "pregnancy"],
    "animal pharmacology and/or toxicology": ["carcinogenesis, mutagenesis, impairment of fertility",
                                              "pharmacodynamics", "pregnancy"],
    "clinical studies": ["adverse reactions", "indications and usage", "pharmacodynamics"],
    "references": ["clinical studies", "description"],
    "drug interactions": ["pharmacokinetics", "drug/laboratory test interactions", "contraindications"],
    "drug/laboratory test interactions": ["drug interactions", "laboratory tests"],
    "laboratory tests": ["drug/laboratory test interactions", "warnings and precautions"],
    "information for patients (patient counseling)": [
        "patient medication information (Medication Guide / Patient Information)", "warnings and precautions",
        "instructions for use"],
    "patient medication information (Medication Guide / Patient Information)": [
        "information for patients (patient counseling)", "instructions for use", "boxed warning"],
    "instructions for use": ["patient medication information (Medication Guide / Patient Information)",
                             "dosage and administration", "storage and handling"],
    "recent major changes": ["boxed warning", "warnings and precautions", "indications and usage"],
}
# headings of OTHER sections: a passage containing one is dropped (it straddles sections). Upper-case forms and
# multi-word Title Case forms only, so ordinary prose ('use during pregnancy') is not hit.
HEADINGS = {
    "boxed warning": [r"BOXED WARNING", r"WARNING:"],
    "indications and usage": [r"INDICATIONS AND USAGE", r"INDICATIONS & USAGE", r"Indications and Usage"],
    "dosage and administration": [r"DOSAGE AND ADMINISTRATION", r"Dosage and Administration"],
    "dosage forms and strengths": [r"DOSAGE FORMS AND STRENGTHS", r"Dosage Forms and Strengths"],
    "contraindications": [r"CONTRAINDICATIONS"],
    "warnings and precautions": [r"WARNINGS", r"PRECAUTIONS", r"Warnings and Precautions", r"General Precautions"],
    "adverse reactions": [r"ADVERSE REACTIONS", r"Adverse Reactions"],
    "drug interactions": [r"DRUG INTERACTIONS", r"Drug Interactions"],
    "drug/laboratory test interactions": [r"Drug/Laboratory Test Interactions", r"DRUG/LABORATORY TEST"],
    "pregnancy": [r"PREGNANCY", r"Pregnancy Category", r"Teratogenic Effects", r"Nonteratogenic Effects",
                  r"Usage in Pregnancy", r"8\.1 Pregnancy"],
    "labor and delivery": [r"LABOR AND DELIVERY", r"Labor and Delivery"],
    "nursing mothers (lactation)": [r"NURSING MOTHERS", r"Nursing Mothers", r"LACTATION", r"8\.2 Lactation"],
    "pediatric use": [r"PEDIATRIC USE", r"Pediatric Use"],
    "geriatric use": [r"GERIATRIC USE", r"Geriatric Use"],
    "controlled substance": [r"CONTROLLED SUBSTANCE", r"Controlled Substance"],
    "abuse": [r"ABUSE\b(?! AND DEPENDENCE)"], "dependence": [r"(?<!ABUSE AND )DEPENDENCE"],
    "overdosage": [r"OVERDOSAGE", r"Overdosage"],
    "description": [r"DESCRIPTION"],
    "mechanism of action": [r"MECHANISM OF ACTION", r"Mechanism of Action"],
    "pharmacodynamics": [r"PHARMACODYNAMICS"], "pharmacokinetics": [r"PHARMACOKINETICS"],
    "microbiology": [r"MICROBIOLOGY"],
    "carcinogenesis, mutagenesis, impairment of fertility": [r"CARCINOGENESIS", r"Carcinogenesis, Mutagenesis",
                                                             r"Impairment of Fertility"],
    "animal pharmacology and/or toxicology": [r"ANIMAL PHARMACOLOGY", r"ANIMAL TOXICOLOGY", r"Animal Toxicology",
                                              r"Animal Pharmacology"],
    "clinical studies": [r"CLINICAL STUDIES", r"Clinical Studies"],
    "references": [r"REFERENCES"], "how supplied": [r"HOW SUPPLIED", r"How Supplied"],
    "storage and handling": [r"STORAGE AND HANDLING", r"Storage and Handling"],
    "information for patients (patient counseling)": [r"INFORMATION FOR PATIENTS", r"Information for Patients",
                                                      r"PATIENT COUNSELING", r"Patient Counseling"],
    "laboratory tests": [r"LABORATORY TESTS", r"Laboratory Tests"],
    "recent major changes": [r"RECENT MAJOR CHANGES", r"Recent Major Changes"],
    "patient medication information (Medication Guide / Patient Information)": [r"MEDICATION GUIDE",
                                                                                r"PATIENT INFORMATION"],
    "instructions for use": [r"INSTRUCTIONS FOR USE", r"Instructions for Use"],
}
EXTRA_BLOCK = [r"CLINICAL PHARMACOLOGY", r"Clinical Pharmacology", r"USE IN SPECIFIC POPULATIONS",
               r"Use in Specific Populations", r"NONCLINICAL TOXICOLOGY", r"DRUG ABUSE AND DEPENDENCE",
               r"Drug Abuse and Dependence", r"HIGHLIGHTS", r"FULL PRESCRIBING INFORMATION", r"PACKAGE LABEL"]
STORAGE = re.compile(r"(?i)\bstore[ds]?\b|\bstorage\b|°\s*[CF]\b|\btemperature\b|\brefrigerat\w*|\bprotect(ed)? from "
                     r"(light|moisture|freezing)|\bdispense in\b|\bfreez\w*")
CROSSREF = re.compile(r"\[\s*[Ss]ee [^\]]{0,160}\]|\(\s*[Ss]ee [^)]{0,160}\)|\(\s*\d{1,2}(\.\d{1,2})*(\s*,\s*\d{1,2}(\.\d{1,2})*)*\s*\)")
BOILER = re.compile(r"(?i)\b(manufactured|distributed|marketed|repackaged|relabeled|packaged|mfd\.|dist\.|made) (for|by|in)\b|"
                    r"\brevised:|\brev\.|\bprinted in\b|\bissued:|\bis a (registered )?trademark|\btrademarks? of\b|"
                    r"call your doctor for medical advice about side effects|1-800-fda-1088|medwatch|\bprsn\b|\biss\.|"
                    r"\bLot\b.*\bExp\b|www\.|\.com\b|\bInc\.?\s*$|\bLLC\b|\bLtd\b|\bUSA\s*$")
# reviewer fix (round 2): some openFDA fields carry another section's text (older LOINC codes reused): 'Lactation Risk
# Summary' inside labor_and_delivery, 'Females and Males of Reproductive Potential' inside nursing_mothers, patient
# leaflet text inside references, withdrawal/tolerance text inside abuse, a warranty inside storage_and_handling.
# A passage of these sections must show the section's own content (require) and none of the neighbour's (forbid).
CONTENT = {
    "labor and delivery": (r"\blabou?r\b|deliver|parturition|obstetric|cesarean|caesarean|uterine|contraction|birth|\bpups?\b",
                           r"\bmilk\b|breast|lactat|nursing"),
    "nursing mothers (lactation)": (r"\bmilk\b|breast|nursing|lactat|infant", r"reproductive potential|contracept|infertil"),
    "abuse": (r"abus|misus|addict|divers|recreational|euphor|drug-seeking|liking", r"withdraw|toleran|physical(ly)? depend"),
    "dependence": (r"depend|withdraw|toleran|abrupt|discontinu|cessation", r"abus|misus|addict"),
    "references": (r"\b(1[89]|20)\d{2}\b|et al", r"\byou\b|\byour\b"),
    "storage and handling": (STORAGE.pattern, r"warrant"),
    "pregnancy": (r"pregnan|fetus|fetal|foetal|teratogen|embryo|reproduct|gestation|neonat|newborn|offspring|\bpups?\b|"
                  r"litter|\bdams?\b|in utero|birth|trimester|mating|organogenesis", r"\bmilk\b|breast-?fe|lactat"),
    "carcinogenesis, mutagenesis, impairment of fertility": (
        r"carcino|mutagen|fertil|genotox|tumou?r|neoplas|clastogen|\bames\b|mating|chromosom|mutation|resorb|implant|"
        r"estrous|sperm|reproduct|micronucle|chromatid|\bDNA\b|oncogen|lymphoma|adenoma|lifetime", r"(?!x)x"),
    "geriatric use": (r"elder|geriatric|older|\b(6[05]|7[05]|80)\b|\bage[sd]?\b|aging|ageing", r"(?!x)x"),
    "pediatric use": (r"pediatric|paediatric|child|infant|neonat|adolescen|newborn|juvenile|years of age|\bage[sd]?\b|"
                      r"young|boys|girls|premature|preterm", r"(?!x)x"),
    "overdosage": (r"overdos|toxic|ingest|dialys|poison|excess|lavage|emesis|charcoal|antidote|supportive|intoxicat|"
                   r"large (doses?|amounts?|quantit)|massive|high doses?|symptomatic", r"(?!x)x"),
    "laboratory tests": (r"test|monitor|measur|determin|level|count|biops|exam|serolog|assay|value|function|evaluat",
                         r"false[- ]positive|interfer|cross[- ]react"),
}
CONTENT = {s: (re.compile(a, re.I), re.compile(b, re.I)) for s, (a, b) in CONTENT.items()}
WP_PREG = re.compile(r"(?i)\bpregnan|\bteratogen|\bfetus|\bfetal\b|\bembryo|\bnursing (mother|infant|women)|"
                     r"\bbreast[- ]?(fed|feeding|milk)|\blactat")
SUPPLIED = re.compile(r"(?i)\bNDC\b|\bbottles?\b|\bblister|\bcartons?\b|\bpackages?\b|\bvials?\b|\bsupplied\b|"
                      r"\bboxes?\b|\bcontainers?\b|\bunit[- ]dose|\bpacks?\b|\btubes?\b|\bsyringes?\b|\bampules?\b")
LEAD_NUM = re.compile(r"^\s*\d{1,2}(\.\d{1,2}){0,2}\s+")
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\"'])")


def other_heading_re(sec):
    pats = [p for s, ps in HEADINGS.items() if s != sec for p in ps] + EXTRA_BLOCK
    if sec == "warnings and precautions":
        pats = [p for p in pats if p not in (r"BOXED WARNING", r"WARNING:")]
    if sec == "abuse":
        pats = [p for p in pats if "DEPENDENCE" not in p]
    return re.compile(r"(?:%s)" % "|".join(pats))


def strip_heading(text, sec):
    t = LEAD_NUM.sub("", text.strip())
    for p in HEADINGS[sec] + [r"[A-Z][A-Z ,&/-]{3,60}(?=\s)"]:
        m = re.match(r"\s*(?:\d{1,2}(\.\d{1,2}){0,2}\s+)?(?:%s)\s*:?\s*" % p, t)
        if m:
            t = t[m.end():]
            break
    return t.strip()


# reviewer fix (round 2): passages often still began with their own section heading ('Pharmacodynamics The effect
# ...', '3. DOSAGE FORMS AND STRENGTHS ...', 'Information for patients ...', 'H. Geriatric Use ...'), which names the
# gold label. Own headings are now stripped case-insensitively (with leading enumerators such as '3.', '8.1', 'H.')
# from the start of every passage, repeatedly; a passage that still starts with its own heading is dropped.
OWN_HEAD = {
    "boxed warning": [r"boxed warning(\s+section)?", r"warning(?=\s*:)"],
    "indications and usage": [r"indications\s*(and|&)\s*usage", r"indications?(?=\s*:)", r"indications and use"],
    "dosage and administration": [r"dosage\s*(and|&)\s*administration"],
    "dosage forms and strengths": [r"dosage forms\s*(and|&)\s*strengths"],
    "contraindications": [r"contraindications?"],
    "warnings and precautions": [r"warnings\s*(and|&)\s*precautions", r"general\s+precautions", r"warnings?",
                                 r"precautions", r"general"],
    "adverse reactions": [r"adverse reactions", r"adverse events"],
    "drug interactions": [r"drug interactions"],
    "drug/laboratory test interactions": [r"drug\s*/\s*laboratory(\s+test)?\s+(interactions|interferences)",
                                          r"drug[- ]laboratory test interactions"],
    "pregnancy": [r"(use |usage )?(in |during )?pregnancy(?!\s+category)", r"non-?teratogenic effects",
                  r"teratogenic effects"],
    "labor and delivery": [r"labor\s*(and|&)\s*delivery"],
    "nursing mothers (lactation)": [r"nursing mothers", r"lactation"],
    "pediatric use": [r"pediatric use"],
    "geriatric use": [r"geriatric use"],
    "controlled substance": [r"controlled substance(\s+class)?"],
    "abuse": [r"abuse(?!\s+and\s+dependence)"],
    "dependence": [r"dependence"],
    "overdosage": [r"overdosage", r"overdose"],
    "description": [r"description"],
    "mechanism of action": [r"mechanism of action"],
    "pharmacodynamics": [r"pharmacodynamics?"],
    "pharmacokinetics": [r"(human\s+)?pharmacokinetics?"],
    "microbiology": [r"microbiology"],
    "carcinogenesis, mutagenesis, impairment of fertility": [
        r"carcinogenesis(\s*(,|and|&)\s*)*(mutagenesis)?(\s*(,|and|&)\s*)*(impairment of fertility)?",
        r"mutagenesis", r"impairment of fertility"],
    "animal pharmacology and/or toxicology": [
        r"(and\s+)?animal\s+(pharmacology|toxicology)(\s*(and|/|and\s*/\s*or)\s*(animal\s+)?(pharmacology|toxicology))?",
        r"(and\s+)?toxicology"],
    "clinical studies": [r"clinical studies"],
    "references": [r"references"],
    "how supplied": [r"how supplied", r"supplied(?=\s*:)"],
    "storage and handling": [r"storage\s*(and|&)\s*handling", r"storage(?=\s*:)"],
    "information for patients (patient counseling)": [r"information for (the\s+)?patients?", r"patient counseling information",
                                                      r"patient counseling", r"information"],
    "laboratory tests": [r"(clinical\s+)?laboratory tests?"],
    "recent major changes": [r"recent major changes"],
    "patient medication information (Medication Guide / Patient Information)": [
        r"medication guide", r"patient information( leaflet)?", r"patient package insert", r"information for the patient"],
    "instructions for use": [r"instructions for use"],
}
_ENUM = r"(?:(?:\d{1,2}(?:\.\d{1,2}){0,2}\.?|[A-Z]\.)\s+)?"
# the heading is stripped only when what follows starts like a new sentence (case-sensitive lookahead), so prose such
# as 'Overdosage with nifedipine ...' or 'Laboratory tests are not required ...' is left alone (and then dropped)
OWN_STRIP = {s: re.compile(r"^\s*" + _ENUM + r"(?:%s)\s*[:.\-\u2013\u2014]?\s*(?-i:(?=[A-Z0-9\u2022(\"'\[]))"
                           % "|".join(ps), re.I) for s, ps in OWN_HEAD.items()}
OWN_START = {s: re.compile(r"^\s*" + _ENUM + r"(?:%s)\b" % "|".join(ps), re.I) for s, ps in OWN_HEAD.items()}
SUBNUM = re.compile(r"^\s*\d{1,2}(?:\.\d{1,2}){1,2}\.?\s+(?=[A-Z])")  # bare PLR subsection number '14.1.'
BULLET = re.compile(r"^[\u2022\u25aa\u25cf\u00b7*\-]\s*")


def strip_own(chunk, sec):
    """Remove own-section headings (and enumerators) from the start of a passage; None if one remains."""
    t = chunk
    for _ in range(4):
        m = OWN_STRIP[sec].match(t) or SUBNUM.match(t)
        if not m or m.end() == 0:
            break
        t = BULLET.sub("", t[m.end():]).strip()
    if OWN_START[sec].match(t):
        return None
    return t


def passages(text, sec, rng):
    t = CROSSREF.sub("", strip_heading(re.sub(r"^\s*SECTION\s+", "", text.strip()), sec))
    t = re.sub(r"\bSECTION\s+(?=[A-Z])", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\b\d{1,2}\.\d{1,2}\s+(?=[A-Z][a-z])", "", t)  # inline PLR subsection numbers ('2.1 Hyperlipidemia')
    t = re.sub(r"\s+([.,;:])", r"\1", t)
    sents = [s.strip() for s in SENT.split(t) if s.strip() and not BOILER.search(s)]
    if not sents:
        return None
    for _ in range(6):
        k = rng.randint(1, 4)
        start = 0 if sec == "boxed warning" else rng.randint(0, max(0, len(sents) - k))
        chunk = strip_own(" ".join(sents[start:start + k]), sec)
        if chunk is None:
            continue
        n = len(chunk.split())
        if 25 <= n <= 170 and re.match(r"[A-Z0-9(\"']", chunk):
            return chunk
    return None


class Containment:
    """Exact containment near-duplicate detector over word n-gram shingles (digits removed)."""

    def __init__(self, thr=0.5, n=5):
        self.thr, self.n = thr, n
        self.inv = collections.defaultdict(list)
        self.sh = []

    def seen(self, text):
        s = C.shingles(re.sub(r"\d+", " ", text), self.n)
        cnt = collections.Counter(j for g in s for j in self.inv[g])
        if any(c / max(1, min(len(s), len(self.sh[j]))) >= self.thr for j, c in cnt.items()):
            return True
        j = len(self.sh)
        self.sh.append(s)
        for g in s:
            self.inv[g].append(j)
        return False


def is_rx(r):
    return ("indications_and_usage" in r and "purpose" not in r and "active_ingredient" not in r
            and ("contraindications" in r or "clinical_pharmacology" in r))


def main():
    zpath, _ = C.fetch(URL, CACHE / "drug-label-0001-of-0014.json.zip", ZIP_SHA)
    z = zipfile.ZipFile(zpath)
    docs = json.load(z.open(z.namelist()[0]))["results"]
    docs = [r for r in docs if r.get("effective_time", "99999999") < CUTOFF and is_rx(r)]
    docs.sort(key=lambda r: r["id"])
    print("prescription labels effective < 2022:", len(docs))
    rng = random.Random(SEED)
    rng.shuffle(docs)
    other_re = {s: other_heading_re(s) for s in SECTIONS}
    stats = collections.Counter()
    cand = collections.defaultdict(list)
    # reviewer fix: containment dedup (5-gram overlap / smaller passage >= 0.5, exact, no LSH) instead of the MinHash
    # LSH NearDup, which missed generic-label copies (e.g. two enalapril descriptions, 1- vs 2-sentence versions)
    nd = Containment(thr=0.5, n=5)
    for r in docs:
        fields = [f for f in sorted(FIELD2SEC) if f in r and r[f]]
        rng.shuffle(fields)
        taken = set()
        for f in fields:
            sec = FIELD2SEC[f]
            if sec in taken or len(taken) >= 3:
                continue
            text = r[f][0]
            p = passages(text, sec, rng)
            if not p:
                stats["no_passage"] += 1
                continue
            if sec != "recent major changes" and other_re[sec].search(p):
                stats["other_heading"] += 1
                continue
            if sec in CONTENT and (not CONTENT[sec][0].search(p) or CONTENT[sec][1].search(p)):
                stats["content_mismatch"] += 1
                continue
            if sec == "warnings and precautions" and WP_PREG.search(p):
                stats["wp_pregnancy_content"] += 1
                continue
            if sec in ("how supplied", "storage and handling") and re.search(r"(?i)directions|instructions|\bstep\b", p):
                stats["supplied_or_storage_with_directions"] += 1
                continue
            if sec == "how supplied" and not SUPPLIED.search(p):
                stats["supplied_no_package"] += 1
                continue
            if sec == "how supplied" and STORAGE.search(p):
                stats["supplied_storage"] += 1
                continue
            if sec == "recent major changes" and not re.search(r"\d{1,2}/\d{4}|\d{4}", p):
                stats["rmc_no_date"] += 1
                continue
            # the same passage text inside another gold field of this label -> ambiguous
            if any(p[:120] in (r[g][0] if r.get(g) else "") for g in FIELD2SEC if FIELD2SEC[g] != sec):
                stats["shared_with_other_section"] += 1
                continue
            if nd.seen(p):
                stats["near_dup"] += 1
                continue
            if f"{r['id']}:{f}" in DECON_DROP:
                stats["decon"] += 1
                continue
            taken.add(sec)
            cand[sec].append((r["id"], r["set_id"], r["effective_time"], f, p))
    print("drops:", dict(stats))
    print("candidates:", {s: len(v) for s, v in sorted(cand.items())})
    pool = []
    for s in sorted(cand):
        pool += cand[s][:600]
    # reviewer fix: max_other 0.6 -> 0.4; a spot check of rows the held-out model disputes at 0.4-0.6 found about half
    # to be passages whose openFDA field holds another section's content (MoA text under pharmacodynamics, drug/lab
    # test interference under laboratory tests, susceptibility lists under mechanism of action)
    keep, _, _ = C.oof_filter([x[4] for x in pool], [FIELD2SEC[x[3]] for x in pool], seed=SEED, min_gold=0.15,
                              max_other=0.4)
    print("OOF drops:", sum(not k for k in keep), "of", len(pool))
    pools = collections.defaultdict(list)
    for x, k in zip(pool, keep):
        if k:
            pools[FIELD2SEC[x[3]]].append(x)
    for s in pools:
        pools[s] = pools[s][:PER_LABEL_CAP]
        pools[s].reverse()
    labels = sorted(pools)
    chosen, i = [], 0
    while len(chosen) < N_ROWS and any(pools[s] for s in labels):
        s = labels[i % len(labels)]
        i += 1
        if pools[s]:
            chosen.append(pools[s].pop())
    all_secs = sorted(SECTIONS)
    rows = []
    for doc_id, set_id, eff, f, p in chosen:
        sec = FIELD2SEC[f]
        opts = C.option_subset(sec, all_secs, CONFUSERS.get(sec, []), rng, lo=12, hi=30)
        n = len(p.split())
        edge = "long_context" if n > 140 else None
        if sec in ("contraindications",) and re.search(r"\b(not|no|never|without)\b", p):
            edge = edge or "negation"
        rows.append({
            "key": KEY, "rid": f"openfda-label:{doc_id}:{f}", "state": p, "instructions": QUESTION,
            "options": opts, "gold": sec, "soft": None,
            "meta": {"dataset": DATASET, "config": "34 SPL section types (openFDA fields merged)",
                     "revision": f"openFDA export 2026-09-28; sha256 {ZIP_SHA}; label effective {eff}",
                     "licence": LICENCE, "split": "train", "orig_label": f, "family": C.FAMILY, "edge": edge},
        })
    rows = C.final_dedup(rows)  # reviewer fix: exact near-duplicate pass
    rng.shuffle(rows)
    out = C.write_rows(KEY, rows)
    C.write_defs(KEY, {s: d for s, (_, d) in SECTIONS.items()})
    print("wrote", out)
    C.summary(rows)
    print(dict(collections.Counter(r["gold"] for r in rows)))
    C.show(rows, 6, seed=4)


if __name__ == "__main__":
    main()
