"""Build raw rows for medmcqa_subject (MedMCQA, Pal et al., CHIL 2022): which medical subject an exam question tests.

Source : HF openlifescienceai/medmcqa (the authors' org), data/train-00000-of-00001.parquet ONLY (validation/test
         never read). Pinned revision 91c6572c454088bf71b679ad90aa8dffcd0d5868; sha256 of the parquet checked.
Licence: MIT (https://github.com/medmcqa/medmcqa/blob/c59ef14ca1990266c4107c7864b45a20fd93e5e0/LICENSE.md,
         README badge "License: MIT"); the HF card of the same authors says apache-2.0 (both permissive).
Texts  : human-written Indian medical entrance exam questions (AIIMS / NEET PG and mock tests), with their 4 options.
Labels : subject_name as filed by the exam/question-bank source (human), 19 subjects; 'Unknown' dropped; 'Dental' dropped
         (reviewer fix: its topic-named rows are misfiled dermatology questions).
Noise control: drop exam-name / 'Miscellaneous' / 'General' topics; drop topics whose name points at another subject (and
         immunology topics outside Microbiology); keep only rows with a topic_name whose subject purity over the whole train split is >= 0.9 and whose
         majority subject equals the row's subject (topic and subject agree); drop questions that rely on an image;
         near-duplicate questions dropped (5-gram MinHash Jaccard >= 0.7). Explanations (exp) never shown.
Task   : one row per question, 19-way choice, round-robin over subjects (equal shares). Soft: null (single label).
Edge   : 'exception' for EXCEPT / all-but questions, 'negation' for NOT / false / incorrect questions.
Deterministic (seed 20260929). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

KEY = "medmcqa_subject"
SEED = 20260929
PER_CLASS = 300
REV = "91c6572c454088bf71b679ad90aa8dffcd0d5868"
SHA = "b119434ba551517a6ec0ba1f7e0b4c029165ed284a4704f262ce37c791c493c5"
LICENCE = ("MIT (https://github.com/medmcqa/medmcqa/blob/c59ef14ca1990266c4107c7864b45a20fd93e5e0/LICENSE.md; "
           "HF card openlifescienceai/medmcqa says apache-2.0)")
QUESTION = "Which medical subject does this exam question belong to?"
NAMES = {
    "Anaesthesia": "anaesthesia", "Anatomy": "anatomy", "Biochemistry": "biochemistry",
    "ENT": "ENT (otorhinolaryngology)", "Forensic Medicine": "forensic medicine and toxicology",
    "Gynaecology & Obstetrics": "obstetrics and gynaecology", "Medicine": "internal medicine",
    "Microbiology": "microbiology", "Ophthalmology": "ophthalmology", "Orthopaedics": "orthopaedics",
    "Pathology": "pathology", "Pediatrics": "paediatrics", "Pharmacology": "pharmacology", "Physiology": "physiology",
    "Psychiatry": "psychiatry", "Radiology": "radiology", "Skin": "dermatology",
    "Social & Preventive Medicine": "social and preventive medicine", "Surgery": "surgery",
}
DEFS = {
    "anaesthesia": "Anaesthetic agents and techniques, airway management, muscle relaxants, perioperative monitoring, "
                   "regional blocks and pain or ICU management as practised by anaesthetists.",
    "anatomy": "Normal structure of the body: gross anatomy, relations, nerve and blood supply, embryology, histology "
               "and neuroanatomy; not how organs function (physiology) or disease (pathology).",
    "biochemistry": "Molecules and metabolism: enzymes, vitamins, metabolic pathways and their inborn errors, "
                    "molecular biology and genetics techniques, lipids, proteins and nutrition chemistry.",
    "ENT (otorhinolaryngology)": "Diseases and surgery of the ear, nose, paranasal sinuses, pharynx and larynx, "
                                 "hearing and vestibular tests, and head-neck conditions treated by ENT surgeons.",
    "forensic medicine and toxicology": "Medico-legal practice: injuries and wounds, death and post-mortem changes, "
                                        "identification, sexual offences, legal procedures, and poisons with their "
                                        "antidotes (toxicology).",
    "obstetrics and gynaecology": "Pregnancy, labour, puerperium and their complications, contraception, and "
                                  "diseases of the female reproductive organs, including gynaecological cancers.",
    "internal medicine": "Diagnosis and non-surgical management of adult systemic diseases (cardiac, renal, "
                         "endocrine, infectious, neurological...); drug mechanism questions go to pharmacology, "
                         "tissue-level mechanisms to pathology.",
    "microbiology": "Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, "
                    "immunology and vaccines, and sterilisation.",
    "ophthalmology": "Eye diseases, their signs, investigations and treatment, optics and refraction, and eye "
                     "surgery.",
    "orthopaedics": "Fractures, dislocations, bone and joint diseases, bone tumours, nerve injuries of the limbs and "
                    "their orthopaedic management.",
    "pathology": "Mechanisms and morphology of disease: cell injury, inflammation, neoplasia, haematology, and the "
                 "gross/microscopic features and lab findings of diseases.",
    "paediatrics": "Child health: growth and development milestones, neonatal care, immunisation schedules, "
                   "nutrition and diseases of infants and children.",
    "pharmacology": "Drugs: mechanisms of action, pharmacokinetics, adverse effects, interactions, drug of choice and "
                    "classification of drugs.",
    "physiology": "Normal function of the body's systems (nerve, muscle, blood, heart, lungs, kidney, endocrine, "
                  "special senses) and their regulation, not their structure or disease.",
    "psychiatry": "Mental disorders, their symptoms, classification and treatment (including psychotropic "
                  "therapy choices), psychology and substance-use disorders.",
    "radiology": "Imaging and radiation: X-ray, CT, MRI, ultrasound and nuclear-medicine signs and choice of "
                 "investigation, radiation physics, radiotherapy and radiation protection.",
    "dermatology": "Skin, hair and nail diseases, their lesions and treatment, and sexually transmitted diseases "
                   "and leprosy as taught in dermatology (venereology).",
    "social and preventive medicine": "Community medicine: epidemiology, biostatistics, national health "
                                      "programmes, screening, nutrition and environmental and occupational health "
                                      "at population level.",
    "surgery": "Surgical diseases and their operative management: trauma, GI and hepatobiliary surgery, breast, "
               "thyroid, vascular, urology, neurosurgery and surgical oncology.",
}
IMG = re.compile(r"\b(image|figure|picture|photo|photograph|diagram|shown below|given below|marked|arrow|following "
                 r"appearance|shown in|given (x-ray|radiograph))\b", re.I)
EXC = re.compile(r"\bexcept\b|\ball but\b|\ball (of the following|are) .* (except|but)\b", re.I)
NEG = re.compile(r"\b(not|false|incorrect|untrue|never)\b", re.I)
GENERIC_TOPIC = re.compile(r"^(all india exam|misc\.?|miscellaneous|general|general anatomy|basic concepts|general concepts|"
                           r"fundamental concepts|other key definitions & concepts)$|neet|jipmer|aiims|pgi\b|all india",
                           re.I)
# Reviewer fix (2026-09-29): a topic whose NAME points at another subject is ambiguous under the definitions
# (e.g. Pharmacology/'Anaesthesia', Skin/'Histopathological findings', Surgery/'Plastic Surgery and Skin Lesions',
# Pediatrics/'Pediatric orthopedics'): such rows are dropped (never relabelled). Immunology topics are dropped outside
# Microbiology (whose definition owns immunology).
SUBJ_KW = {
    "Anaesthesia": r"an(a)?esth", "Anatomy": r"anatom", "Biochemistry": r"biochem", "ENT": r"\bent\b|otorhino",
    "Forensic Medicine": r"forensic|toxicolog", "Gynaecology & Obstetrics": r"gyn|obstet|pregnan",
    "Microbiology": r"microbio", "Ophthalmology": r"ophthal|\beyes?\b", "Orthopaedics": r"orthop|ohop",
    "Pathology": r"patholog", "Pediatrics": r"p(a)?ediatric|\bchild|neonat|new ?born|infan",
    "Pharmacology": r"pharmac|\bdrugs?\b", "Physiology": r"physiolog", "Psychiatry": r"psychiat|psycholog",
    "Radiology": r"radiolog|imaging|radiother|x-ray|ultrasound", "Skin": r"\bskin\b|dermat",
    "Social & Preventive Medicine": r"preventive|community|epidemiolog|biostat", "Surgery": r"surg",
}
IMMUNO = re.compile(r"immun(e|ity|ology)|hypersensitiv", re.I)


def cross_subject(subj, topic):
    if subj != "Microbiology" and IMMUNO.search(topic):
        return True
    return any(re.search(kw, topic, re.I) for s, kw in SUBJ_KW.items() if s != subj)


def main():
    path, _ = C.fetch(f"https://huggingface.co/datasets/openlifescienceai/medmcqa/resolve/{REV}/data/"
                      "train-00000-of-00001.parquet", C.CACHE / "medmcqa" / "train.parquet", SHA)
    d = pd.read_parquet(path)  # TRAIN ONLY
    # Reviewer fix (2026-09-29): MedMCQA 'Dental' is dropped entirely: its topic-named rows are dermatology questions
    # filed under Dental (topics 'Bacterial infections', 'Anatomy of skin', 'Papulosquamous disorders', ...) and its
    # real dental questions have no topic and mix general-medicine items, so the label cannot be trusted.
    assert set(NAMES) | {"Unknown", "Dental"} == set(d.subject_name.unique())
    assert set(NAMES.values()) == set(DEFS)
    t = d.dropna(subset=["topic_name"])
    purity = t.groupby("topic_name").subject_name.agg(lambda s: (s.value_counts().index[0],
                                                                  s.value_counts(normalize=True).iloc[0]))
    stats = collections.Counter()
    pools = collections.defaultdict(list)
    for r in d.sort_values("id").itertuples(index=False):
        if r.subject_name == "Unknown":
            stats["unknown"] += 1
            continue
        if r.subject_name == "Dental":
            stats["dental_mislabelled"] += 1
            continue
        if r.topic_name is None or r.topic_name not in purity.index:
            stats["no_topic"] += 1
            continue
        if GENERIC_TOPIC.search(r.topic_name.strip()):
            stats["generic_topic"] += 1
            continue
        if cross_subject(r.subject_name, r.topic_name.strip()):
            stats["cross_subject_topic"] += 1
            continue
        maj, p = purity[r.topic_name]
        if maj != r.subject_name or p < 0.9:
            stats["topic_disagree"] += 1
            continue
        q = re.sub(r"\s+", " ", r.question).strip()
        opts = [re.sub(r"\s+", " ", o or "").strip() for o in (r.opa, r.opb, r.opc, r.opd)]
        if len(q) < 15 or any(not o for o in opts) or IMG.search(q):
            stats["short_or_image"] += 1
            continue
        pools[r.subject_name].append((r.id, q, opts, r.topic_name))
    rng = random.Random(SEED)
    nd = C.NearDup(0.7)
    rows = []
    for subj in sorted(pools):
        pool = pools[subj]
        rng.shuffle(pool)
        n = 0
        for rid, q, opts, topic in pool:
            if n >= PER_CLASS:
                break
            state = f"Question: {q}\nOptions: (A) {opts[0]} (B) {opts[1]} (C) {opts[2]} (D) {opts[3]}"
            if nd.seen(q):
                stats["near_dup"] += 1
                continue
            n += 1
            last = re.split(r"(?<=[.?!])\s+", q.strip())[-1]  # the question stem, not the vignette
            edge = "exception" if EXC.search(last) else "negation" if NEG.search(last) else None
            rows.append({
                "key": KEY, "rid": f"medmcqa-train-{rid}", "state": state, "instructions": QUESTION,
                "options": sorted(DEFS), "gold": NAMES[subj], "soft": None,
                "meta": {"dataset": "openlifescienceai/medmcqa (MedMCQA)", "config": "train parquet; subject_name 19-way",
                         "revision": f"hf:{REV}; sha256:{SHA}", "licence": LICENCE, "split": "train",
                         "orig_label": {"subject_name": subj, "topic_name": topic}, "family": C.FAMILY,
                         "edge": edge, "seed": SEED},
            })
    print("pools:", {k: len(v) for k, v in sorted(pools.items())}, dict(stats))
    rng.shuffle(rows)
    C.write_rows(KEY, rows)
    C.write_defs(KEY, DEFS)
    C.summary(rows)


if __name__ == "__main__":
    main()
