"""Build raw rows for medquad_qtype (MedQuAD, Ben Abacha & Demner-Fushman, BMC Bioinformatics 2019).

Question: which consumer-health question (overview, symptoms, causes, treatment, ...) an NIH passage answers.
Source : GitHub abachaa/MedQuAD, pinned commit 577bd37b96c02d1833b2c9eed2de9f96964e96cb (codeload zip, sha256 checked).
         MedQuAD has no splits -> counts as train. Collections 10-12 (MedlinePlus A.D.A.M., Drugs, Herbs) have no
         answers (removed for copyright) and are never used.
Licence: CC BY 4.0 (LICENSE.txt and readme.txt "License" section of the repo); answers are NIH / CDC pages (US gov).
Texts  : human-written answer passages from 9 NIH/CDC websites (CancerGov, GARD, GHR, MedlinePlus health topics,
         NIDDK, NINDS, NIHSeniorHealth, NHLBI, CDC).
Labels : qtype = the section of the source page the passage came from (human-authored page structure).
         'genetic changes' is merged into 'causes' (GHR 'genetic changes' and GARD 'causes' both state the causal
         mutation); 'considerations' (NIDDK "points to remember" summaries) and 'support groups' (1 item) dropped.
Cleaning: 'information' rows kept only when the first sentence names and defines the topic (one per document;
         MedQuAD files every unmatched page sub-section under "What is (are) X?"); CDC page menus dropped;
         leading echoed question ("What causes X? ...") and "Key Points" headings stripped; GARD auto-inserted
         Human Phenotype Ontology symptom tables cut (row dropped if < 120 chars of prose remain); GHR 'treatment'
         (a templated list of links) dropped; template collisions (same 100-char opening, focus name masked, under
         two different qtypes) dropped; near-duplicates (focus masked, 5-gram MinHash Jaccard >= 0.7) dropped.
Task   : one row per QA pair, 13-way choice, round-robin by class up to PER_CLASS. Soft: null.
Deterministic (seed 20260929). CPU only.
"""
import collections
import glob
import random
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

KEY = "medquad_qtype"
SEED = 20260929
PER_CLASS = 420
COMMIT = "577bd37b96c02d1833b2c9eed2de9f96964e96cb"
ZIP_SHA = "161d948f8ce8f82accca1f5769a512dff2a01af2b3004d48f2b3da2758a38a09"  # snapshot 2026-09-29
CACHE = C.CACHE / "medquad"
LICENCE = f"CC BY 4.0 (https://github.com/abachaa/MedQuAD/blob/{COMMIT}/LICENSE.txt and readme.txt 'License')"
QUESTION = "Which consumer-health question about the named topic does this passage from an NIH health page answer?"
MAP = {
    "information": "what it is (overview)", "symptoms": "signs and symptoms", "causes": "causes",
    "genetic changes": "causes", "inheritance": "inheritance pattern", "frequency": "how common it is",
    "exams and tests": "diagnosis and tests", "treatment": "treatment", "prevention": "prevention",
    "outlook": "outlook (prognosis)", "susceptibility": "who is at risk", "complications": "complications",
    "research": "research and clinical trials", "stages": "stages",
}
DEFS = {
    "what it is (overview)": "Defines or describes the condition or topic in general (what it is, which body part it "
                             "affects, its main features) without being mainly about one aspect below.",
    "signs and symptoms": "Describes what people with the condition experience or show: symptoms, physical signs, "
                          "features and how they present or vary.",
    "causes": "Explains why the condition happens: the biological mechanism, the gene mutations or the infectious or "
              "environmental agent that produces it (not who is more likely to get it).",
    "inheritance pattern": "States how the condition is passed down in families (autosomal dominant or recessive, "
                           "X-linked, mitochondrial, de novo) and the chance relatives are affected.",
    "how common it is": "Gives the prevalence or incidence: how many people or what share of a population have it, "
                        "or that it is rare or its frequency is unknown.",
    "diagnosis and tests": "Explains how the condition is detected or confirmed: exams, lab tests, imaging, genetic "
                           "testing and diagnostic criteria.",
    "treatment": "Describes how the condition is treated or managed: therapies, drugs, surgery, and standard or "
                 "trial treatment options.",
    "prevention": "Describes steps that lower the chance of getting the condition or its spread, such as vaccines, "
                  "hygiene, lifestyle or avoiding exposures.",
    "outlook (prognosis)": "Describes the expected course and outcome: survival, recovery, progression or life "
                           "expectancy.",
    "who is at risk": "Names risk factors or groups more likely to get the condition (age, sex, family history, "
                      "exposures), rather than its mechanism.",
    "complications": "Describes further problems or conditions the disease can lead to.",
    "research and clinical trials": "Describes research being done or funded on the condition: studies, trials, "
                                    "and what scientists are investigating.",
    "stages": "Explains how the disease (usually a cancer) is staged: how spread is measured and what each stage "
              "means.",
}
CANON = {  # the page-section question template MedQuAD used for each qtype; free-form questions are dropped
    "information": r"^What is \(are\)", "symptoms": r"^What are the symptoms of", "causes": r"^What causes",
    "genetic changes": r"^What are the genetic changes related to", "inheritance": r"^Is .* inherited",
    "frequency": r"^How many people are affected by", "exams and tests": r"^How to diagnose",
    "treatment": r"^What are the treatments for", "prevention": r"^How to prevent", "outlook": r"^What is the outlook for",
    "susceptibility": r"^Who is at risk for", "complications": r"^What are the complications of",
    "research": r"^what research", "stages": r"^What are the stages of",
}
Q_ECHO = re.compile(r"^\s*(what|how|who|is|are|can|does|do|when|where|why)\b[^?]{0,250}\?\s*", re.I)


def clean(ans):
    a = re.sub(r"\s+", " ", ans).strip()
    a = re.sub(r"^Key Points\s*", "", a)
    a = Q_ECHO.sub("", a, count=1)
    i = a.find("The Human Phenotype Ontology provides")
    if i >= 0:
        a = a[:i].strip()
    a = re.sub(r"^[-\s]+", "", a)
    if len(a) > 1800:
        cut = a[:1800]
        j = max(cut.rfind(". "), cut.rfind(".\" "))
        a = cut[:j + 1] if j > 600 else cut
    return a.strip()


def main():
    zpath, zsha = C.fetch(f"https://codeload.github.com/abachaa/MedQuAD/zip/{COMMIT}", CACHE / "medquad.zip", ZIP_SHA)
    root = CACHE / f"MedQuAD-{COMMIT}"
    if not root.exists():
        zipfile.ZipFile(zpath).extractall(CACHE)
    recs = []
    stats = collections.Counter()
    for f in sorted(glob.glob(str(root / "*" / "*.xml"))):
        src = Path(f).parent.name
        if src.split("_")[0] in ("10", "11", "12"):
            continue
        doc = ET.parse(f).getroot()
        focus = (doc.findtext("Focus") or "").strip()
        for qa in doc.iter("QAPair"):
            q = qa.find("Question")
            qt = q.get("qtype")
            raw = (qa.findtext("Answer") or "").strip()
            if not raw or not focus:
                continue
            if qt not in MAP:
                stats[f"drop_qtype_{qt}"] += 1
                continue
            if not re.search(CANON[qt], (q.text or "").strip(), re.I):
                stats["noncanonical_question"] += 1
                continue
            if src.startswith("3_GHR") and qt == "treatment":
                stats["ghr_treatment_template"] += 1
                continue
            a = clean(raw)
            if len(a) < 120:
                stats["short"] += 1
                continue
            recs.append({"rid": q.get("qid"), "uid": f"{Path(f).stem}-p{qa.get('pid')}", "src": src, "focus": focus, "qtype": qt, "label": MAP[qt], "ans": a})

    def masked(r):
        m = r["ans"]
        for name in {r["focus"], r["focus"].split(" (")[0]}:
            if len(name) > 2:
                m = re.sub(re.escape(name), "X", m, flags=re.I)
        return m

    opening = collections.defaultdict(set)
    seen_info = set()
    kept = []
    for r in recs:
        r["masked"] = masked(r)
        if r["qtype"] == "information":
            # MedQuAD maps every unmatched sub-section of a page to "What is (are) X?"; keep only a real overview:
            # first sentence names the topic and defines it, and at most one overview per source document.
            first = re.split(r"(?<=[.!?])\s+", r["masked"])[0]
            doc = (r["src"], r["uid"].rsplit("-p", 1)[0])
            if not re.search(r"\bX\b[^.]{0,80}\b(is|are|refers to|means|occurs)\b", first) or doc in seen_info:
                stats["info_not_overview"] += 1
                continue
            seen_info.add(doc)
        if "On this Page" in r["ans"]:
            stats["page_menu"] += 1
            continue
        r["ans"] = re.sub(r"^(Yes|No)\.\s+", "", r["ans"])
        kept.append(r)
        opening[C.norm(r["masked"])[:100]].add(r["label"])
    recs = kept
    rng = random.Random(SEED)
    recs.sort(key=lambda r: (r["src"], r["rid"]))
    rng.shuffle(recs)
    nd = C.NearDup(0.7)
    pools = collections.defaultdict(list)
    for r in recs:
        if len(opening[C.norm(r["masked"])[:100]]) > 1:
            stats["template_collision"] += 1
            continue
        if nd.seen(r["masked"]):
            stats["near_dup"] += 1
            continue
        pools[r["label"]].append(r)
    print("pools:", {k: len(v) for k, v in sorted(pools.items())}, dict(stats))
    assert set(pools) == set(DEFS)
    rows = []
    for lab in sorted(pools):
        # interleave sources so one website does not dominate a class
        bysrc = collections.defaultdict(list)
        for r in pools[lab]:
            bysrc[r["src"]].append(r)
        order = sorted(bysrc)
        taken, i = [], 0
        while len(taken) < PER_CLASS and any(bysrc.values()):
            s = order[i % len(order)]
            if bysrc[s]:
                taken.append(bysrc[s].pop())
            i += 1
        for r in taken:
            state = f"Health topic: {r['focus']}\nPassage: {r['ans']}"
            rows.append({
                "key": KEY, "rid": f"medquad-{r['src']}-{r['uid']}", "state": state, "instructions": QUESTION,
                "options": sorted(DEFS), "gold": r["label"], "soft": None,
                "meta": {"dataset": "abachaa/MedQuAD", "config": f"{r['src']}; qtype 13-way",
                         "revision": f"git:{COMMIT}; sha256(codeload zip):{zsha}", "licence": LICENCE,
                         "split": "train (no official split)", "orig_label": {"qtype": r["qtype"], "source": r["src"], "qid": r["rid"]},
                         "family": C.FAMILY, "edge": "long_context" if len(state) > 1500 else None, "seed": SEED},
            })
    rng.shuffle(rows)
    C.write_rows(KEY, rows)
    C.write_defs(KEY, DEFS)
    C.summary(rows)
    print(collections.Counter(r["gold"] for r in rows))


if __name__ == "__main__":
    main()
