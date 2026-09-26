"""OHS-2 part "science" (track U): four public scientific decision tasks, held out from all OpenDecide work.

Tasks (about 120 items each, one item = one choice row over the task's full official label set):
  pubmed_rct20k      PubMed 20k RCT (Dernoncourt & Lee, IJCNLP 2017), test split. Role of one sentence in its abstract
                     (background / objective / methods / results / conclusions). State = the whole abstract + the sentence.
                     At most one sentence per abstract.
  scifact            SciFact (Wadden et al., EMNLP 2020), dev split (test labels are not released). Claim + one cited
                     abstract (title + abstract) -> support / contradict / not enough info. At most one pair per
                     connected group of claims that share a cited abstract (so a claim, its negation and their shared
                     abstract never appear twice).
  evidence_inference Evidence Inference (Lehman et al., NAACL 2019; DeYoung et al., BioNLP 2020), test articles. Given an
                     RCT abstract, the official prompt "With respect to <outcome>, characterize the reported difference
                     between patients receiving <intervention> and those receiving <comparator>." (outcome, intervention
                     and comparator written by the dataset's doctor annotators) -> significantly increased / significantly
                     decreased / no significant difference. Kept only if every validated annotation agrees, answers from
                     the abstract, and at least one validated evidence quote occurs verbatim in the abstract; prompts the
                     authors flag as incorrect/questionable/malformed are dropped. At most one prompt per article.
  ddi2013            DDI corpus 2013 (Herrero-Zazo et al., JBI 2013; SemEval-2013 Task 9.2), "Test for DDI Extraction
                     task". Interaction type of one annotated drug-drug interaction (mechanism / effect / advice / int);
                     the two drug mentions are marked [[ ]] in the sentence. Non-interacting pairs are not used (the
                     corpus gives no official definition for them). At most one pair per sentence, 3 per document.

Not used: SciCite and ACL-ARC citation intent, SciERC, PUBHEALTH, scientific exaggeration (all were in the v0.11 task
bank via tasksource zero-shot-label-nli -> trained on); PubMedQA (OHS-1); SciNLI (texts from ACL Anthology papers, many
of which are also arXiv papers).

No LLM-written text: states are the datasets' own texts (verbatim; PubMed RCT keeps its original tokenised spacing), gold
labels are the datasets' labels, options are the official label names, and cards are verbatim official descriptions:
  scifact  -> SciFact evidence-annotation guide (https://scifact.s3-us-west-2.amazonaws.com/doc/evidence-annotation-
              instructions.pdf), section 3.2 "Evidence direction" and section 1 step 4.
  ddi2013  -> the DDI corpus page archived in the official repo (isegura/DDICorpus, ddicorpus.webarchive).
  pubmed_rct20k, evidence_inference -> card = null: the RCT paper and NLM only list the five category names; the
              evidence-inference guide explains its three answers only through worked examples.
The builder asserts that every card definition (and the evidence-inference prompt template) is a verbatim substring of its
source. The only other text is one fixed instruction per task (pubmed_rct20k, scifact, ddi2013; adapted from each
dataset's own task description) and fixed state headers ("Abstract:", "Claim:", "Title:", "Sentence:").

Optional (--with-medical): medical_abstracts, Medical Abstracts TC corpus (Schopf et al., NLPIR 2022), test split, 5
classes, card null; texts or titles that carry more than one label anywhere in train+test are dropped. Off by default
because OHS-2 part "misc" already contains a medical_abstracts task.

Sampling: seed 20261010; equal quota per class (so no class exceeds 40%), texts 20-6,000 characters, deduplicated.
Decontamination: drop any candidate sharing a 12-word run (whole text if shorter) with (a) any state in lean/data/**/*.jsonl
except held-out files (data/ohs*.jsonl, data/ohs_parts/, data/ohs2_parts/ are never opened) and (b) any PubMedQA
(pqa_labeled, pqa_unlabeled, pqa_artificial) question, context or long answer (PubMedQA is an OHS-1 source); PubMed RCT
abstracts whose PMID is in PubMedQA are dropped too. Selected items may not share a 12-word run with each other (across
all four tasks). As in part "misc", a candidate that shares a 12-word run with GLiClass training data
(knowledgator/gliclass-v2.0, GLIClass-v1.0, gliclass-v3-logic-dataset; the model family Jev appears to build on) or with
any tasksource/zero-shot-label-nli premise (forbidden source) is skipped lazily at sampling time, so these two scans never
change the seeded rank order of the remaining candidates.

Output: lean/data/ohs2_parts/science.jsonl (+ science_summary.json). Deterministic, CPU only, no LLM calls.
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python ohs2/build_science.py [--with-medical]
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import tarfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import httpx
import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

HERE = Path(__file__).resolve().parent            # lean/ohs2
LEAN = HERE.parent
DATA = LEAN / "data"
OUT_DIR = DATA / "ohs2_parts"
OUT = OUT_DIR / "science.jsonl"
SUMMARY = OUT_DIR / "science_summary.json"
CACHE = HERE / "science_cache"
SEED = 20261010
N_PER_TASK = 120
CAP = 0.40
MIN_CHARS, MAX_CHARS = 20, 6000
NGRAM = 12
SPLIT, TRACK = "ohs2", "U"

# ------------------------------------------------------------------ pinned sources
RCT_URL = ("https://raw.githubusercontent.com/Franck-Dernoncourt/pubmed-rct/"
           "17ed2cb0590decfca0266add0c76f254f67232b4/PubMed_20k_RCT/test.txt")
SCIFACT_URL = "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz"
SCIFACT_GUIDE_URL = "https://scifact.s3-us-west-2.amazonaws.com/doc/evidence-annotation-instructions.pdf"
MED_REPO, MED_REV = "TimSchopf/medical_abstracts", "d6afbd7ff4eb215db2470980023d7d7a3dfee7dc"
DDI_ZIP_URL = "https://github.com/isegura/DDICorpus/raw/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/DDICorpus-2013.zip"
DDI_PAGE_URL = "https://github.com/isegura/DDICorpus/raw/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/ddicorpus.webarchive"
EI_SHA = "a661e8c14f973398380c8865cf2f27a535aaaf6d"
EI_RAW = f"https://raw.githubusercontent.com/jayded/evidence-inference/{EI_SHA}/"
# the official prompt (README.annotation_process.md); outcome / intervention / comparator are filled in per item
EI_TEMPLATE = ("With respect to outcome, characterize the reported difference between patients receiving intervention "
               "and those receiving comparator.")
PQA_REPO = "qiaojin/PubMedQA"
PQA_FILES = ["pqa_labeled/train-00000-of-00001.parquet", "pqa_unlabeled/train-00000-of-00001.parquet",
             "pqa_artificial/train-00000-of-00001.parquet"]
# Jev-side training data and the forbidden zero-shot-label-nli bundle (same pinned revisions as ohs2/build_misc.py)
EXT_REV = {"knowledgator/gliclass-v2.0": "93d3cdc82257a9e821f4b21d08e3dc81979bb653",
           "knowledgator/GLIClass-v1.0": "b0047758976bc0a911882e1722ff8d888a6acdd0",
           "knowledgator/gliclass-v3-logic-dataset": "ee8e07d42c1f95a4421ae78498eec23aec74f1d7",
           "tasksource/zero-shot-label-nli": "ee693dba923b5d5484aa9232b7357c5e45dd39b8"}
ZSL_FILES = ["data/train-00000-of-00002-970172c89e89b5df.parquet", "data/train-00001-of-00002-509e762f01abeb95.parquet",
             "data/validation-00000-of-00001-79d9ba1d8f02bef0.parquet", "data/test-00000-of-00001-c260d1ee78ad6397.parquet"]

# ------------------------------------------------------------------ task specs
TASKS = {
    "pubmed_rct20k": dict(
        instructions="What is the role of this sentence in the abstract?",
        options=["background", "objective", "methods", "results", "conclusions"],
        raw2opt={"BACKGROUND": "background", "OBJECTIVE": "objective", "METHODS": "methods", "RESULTS": "results",
                 "CONCLUSIONS": "conclusions"},
        card=None,
        card_source="none: Dernoncourt & Lee (2017) and the NLM structured-abstract documentation list the five NLM "
                    "categories without per-category definitions",
        licence="no licence file; built on the MEDLINE/PubMed 2016 baseline (NLM terms and conditions)",
        source_id="Franck-Dernoncourt/pubmed-rct PubMed_20k_RCT (GitHub, commit 17ed2cb)", source_split="test"),
    "scifact": dict(
        instructions="What is the relation of this abstract to the claim?",
        options=["support", "contradict", "not enough info"],
        raw2opt={"SUPPORT": "support", "CONTRADICT": "contradict", "NEI": "not enough info"},
        card={"support": "You have more reason to believe the claim is true after reading the text in the evidence set.",
              "contradict": "You have more reason to believe the claim is false after reading the text in the evidence "
                            "set.",
              "not enough info": "the abstract will not provide any relevant evidence"},
        card_source=SCIFACT_GUIDE_URL + " (sections 3.2 and 1, verbatim)",
        licence="claims and evidence annotations CC BY 4.0; abstracts (S2ORC) ODC-By 1.0 (allenai/scifact LICENSE.md)",
        source_id="allenai/scifact release data.tar.gz (claims_dev.jsonl + corpus.jsonl)", source_split="dev"),
    "medical_abstracts": dict(
        instructions="Which class of patient conditions does this medical abstract describe?",
        options=["neoplasms", "digestive system diseases", "nervous system diseases", "cardiovascular diseases",
                 "general pathological conditions"],
        raw2opt={1: "neoplasms", 2: "digestive system diseases", 3: "nervous system diseases",
                 4: "cardiovascular diseases", 5: "general pathological conditions"},
        card=None,
        card_source="none: Schopf et al. (2022) use the class names themselves as the label descriptions",
        licence="CC BY-SA 3.0", source_id=f"{MED_REPO} (HF, revision {MED_REV[:7]})", source_split="test"),
    "ddi2013": dict(
        instructions="What type of drug-drug interaction does this sentence describe between the two drugs marked "
                     "with [[ ]]?",
        options=["mechanism", "effect", "advice", "int"],
        raw2opt={"mechanism": "mechanism", "effect": "effect", "advise": "advice", "int": "int"},
        card={"mechanism": "for DDIs describing the way the interaction occurs",
              "effect": "for DDIs describing the consequence of the interaction",
              "advice": "for DDIs described by a recommendation or advice",
              "int": "for DDIs without any additional information"},
        card_source="DDI corpus page, isegura/DDICorpus ddicorpus.webarchive (verbatim)",
        licence="CC BY-NC 4.0 (isegura/DDICorpus README)",
        source_id="isegura/DDICorpus DDICorpus-2013.zip, Test/Test for DDI Extraction task (GitHub, commit 819b0fa)",
        source_split="test"),
}
TASKS["evidence_inference"] = dict(
    instructions=EI_TEMPLATE + " (template; filled per item with the prompt's outcome, intervention and comparator)",
    options=["significantly increased", "significantly decreased", "no significant difference"],
    raw2opt={"significantly increased": "significantly increased", "significantly decreased": "significantly decreased",
             "no significant difference": "no significant difference"},
    card=None,
    card_source="none: the annotation guide explains the three answers only through worked examples",
    licence="MIT (jayded/evidence-inference); article texts from the PubMed Central open-access subset",
    source_id="jayded/evidence-inference annotations (GitHub, commit a661e8c): annotations_merged.csv, prompts_merged.csv, "
              "abstracts/, splits/test_article_ids.txt", source_split="test")
# medical_abstracts is built only with --with-medical: OHS-2 part "misc" already contains a medical_abstracts task
ORDER = ["pubmed_rct20k", "scifact", "evidence_inference", "ddi2013"]
WITH_MEDICAL = "--with-medical" in __import__("sys").argv
if WITH_MEDICAL:
    ORDER.insert(3, "medical_abstracts")


# ------------------------------------------------------------------ helpers
def sid(*parts) -> str:
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


def words(t: str) -> list[str]:
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).split()


def norm(t: str) -> str:
    return " ".join(words(t))


def ws(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def fetch(url: str, name: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / name
    if not p.exists():
        with httpx.Client(timeout=300, follow_redirects=True) as c:
            r = c.get(url)
            r.raise_for_status()
            p.write_bytes(r.content)
    return p


def fetch_optional(url: str, name: str) -> Path | None:
    """Like fetch, but a 404 is cached as '<name>.404' and returns None."""
    p, miss = CACHE / name, CACHE / (name + ".404")
    if p.exists():
        return p
    if miss.exists():
        return None
    p.parent.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=120, follow_redirects=True) as c:
        r = c.get(url)
    if r.status_code == 404:
        miss.touch()
        return None
    r.raise_for_status()
    p.write_bytes(r.content)
    return p


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def grams(text: str) -> set[tuple[int, str]]:
    w = words(text)
    n = min(NGRAM, len(w))
    return {(n, " ".join(w[i:i + n])) for i in range(len(w) - n + 1)} if n else set()


# ------------------------------------------------------------------ official card check
def check_cards(files: dict) -> dict:
    import pypdf
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    guide = ws(" ".join((pg.extract_text() or "") for pg in pypdf.PdfReader(str(files["scifact_guide"])).pages))
    page = ws(files["ddi_page"].read_bytes().decode("latin-1"))
    res = {}
    for task, src in (("scifact", guide), ("ddi2013", page)):
        for opt, d in TASKS[task]["card"].items():
            assert ws(d) in src, f"card definition not verbatim in source: {task}/{opt}"
        res[task] = "all definitions found verbatim in the official source"
    return res


# ------------------------------------------------------------------ loaders -> candidates
def cand(task, key, group, gold, state, core, meta):
    return dict(task=task, key=str(key), group=group, gold=gold, state=state, core=core, meta=meta)


def load_rct(path: Path) -> tuple[list[dict], dict]:
    abstracts, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("###"):
            cur = {"pmid": line[3:].strip(), "sents": []}
            abstracts.append(cur)
        elif line.strip():
            lab, txt = line.split("\t", 1)
            cur["sents"].append((lab, txt.strip()))
    spec, out, drop = TASKS["pubmed_rct20k"], [], Counter()
    for a in abstracts:
        abstract = " ".join(t for _, t in a["sents"])
        for i, (lab, t) in enumerate(a["sents"]):
            state = f"Abstract:\n{abstract}\n\nSentence:\n{t}"
            if not (MIN_CHARS <= len(t) and len(state) <= MAX_CHARS):
                drop["length"] += 1
                continue
            if sum(1 for _, u in a["sents"] if u == t) > 1:
                drop["sentence repeated in its abstract"] += 1
                continue
            out.append(cand("pubmed_rct20k", f"{a['pmid']}:{i}", f"pmid:{a['pmid']}", spec["raw2opt"][lab], state,
                            [abstract], {"pmid": a["pmid"], "sentence_index": i, "n_sentences": len(a["sents"]),
                                         "raw_label": lab}))
    return out, {"abstracts": len(abstracts), "dropped": dict(drop), "pmids": {a["pmid"] for a in abstracts}}


def load_scifact(path: Path) -> tuple[list[dict], dict]:
    with tarfile.open(path) as tf:
        read = lambda n: [json.loads(l) for l in tf.extractfile(n).read().decode().splitlines() if l.strip()]
        claims, corpus = read("data/claims_dev.jsonl"), {d["doc_id"]: d for d in read("data/corpus.jsonl")}
    # connected groups: claims linked by a shared cited abstract (claim + its negation share the abstract)
    parent = {}
    find = lambda x: x if parent.setdefault(x, x) == x else find(parent[x])
    for c in claims:
        for d in c["cited_doc_ids"]:
            parent[find(("c", c["id"]))] = find(("d", d))
    spec, out, drop = TASKS["scifact"], [], Counter()
    for c in claims:
        for d in c["cited_doc_ids"]:
            ev = c["evidence"].get(str(d))
            labs = {e["label"] for e in ev} if ev else {"NEI"}
            if len(labs) != 1:
                drop["mixed rationale labels"] += 1
                continue
            lab = labs.pop()
            doc = corpus[d]
            abstract = " ".join(s.strip() for s in doc["abstract"])
            state = f"Claim:\n{c['claim'].strip()}\n\nTitle:\n{doc['title'].strip()}\n\nAbstract:\n{abstract}"
            if not (MIN_CHARS <= len(state) <= MAX_CHARS):
                drop["length"] += 1
                continue
            comp = find(("d", d))
            out.append(cand("scifact", f"{c['id']}:{d}", f"comp:{comp[0]}{comp[1]}", spec["raw2opt"][lab], state,
                            [c["claim"], doc["title"] + " " + abstract],
                            {"claim_id": c["id"], "doc_id": d, "raw_label": lab, "structured": doc["structured"]}))
    return out, {"claims": len(claims), "pairs": len(out) + sum(drop.values()), "dropped": dict(drop)}


def load_medical() -> tuple[list[dict], dict]:
    get = lambda f: pd.read_parquet(hf_hub_download(MED_REPO, f, repo_type="dataset", revision=MED_REV))
    te, tr = get("data/test-00000-of-00001.parquet"), get("data/train-00000-of-00001.parquet")
    names = get("labels/train-00000-of-00001.parquet")
    spec = TASKS["medical_abstracts"]
    assert {int(k): v for k, v in zip(names.condition_label, names.condition_name)} == spec["raw2opt"]
    title = lambda t: norm(t.split(". ", 1)[0])
    allx = pd.concat([tr, te])
    by_text = allx.groupby(allx.medical_abstract.map(norm)).condition_label.agg(lambda s: set(s))
    by_title = allx.groupby(allx.medical_abstract.map(title)).condition_label.agg(lambda s: set(s))
    out, drop, seen = [], Counter(), set()
    for i, (lab, t) in enumerate(zip(te.condition_label, te.medical_abstract)):
        t = t.strip()
        if len(by_text[norm(t)]) > 1 or len(by_title[title(t)]) > 1:
            drop["text or title carries >1 label in train+test"] += 1
            continue
        if norm(t) in seen:
            drop["duplicate text in test"] += 1
            continue
        seen.add(norm(t))
        state = f"Medical abstract:\n{t}"
        if not (MIN_CHARS <= len(t) and len(state) <= MAX_CHARS):
            drop["length"] += 1
            continue
        out.append(cand("medical_abstracts", f"test:{i}", f"test:{i}", spec["raw2opt"][int(lab)], state, [t],
                        {"row": i, "raw_label": int(lab)}))
    return out, {"test_rows": len(te), "dropped": dict(drop)}


def load_ddi(path: Path) -> tuple[list[dict], dict]:
    spec, out, drop = TASKS["ddi2013"], [], Counter()
    with zipfile.ZipFile(path) as z:
        names = sorted(n for n in z.namelist() if "Test for DDI Extraction task" in n and n.endswith(".xml")
                       and "/._" not in n and "__MACOSX" not in n)
        for n in names:
            doc = ET.fromstring(z.read(n))
            for s in doc.iter("sentence"):
                text = s.get("text")
                ents = {e.get("id"): e for e in s.iter("entity")}
                for p in s.iter("pair"):
                    if p.get("ddi") != "true":
                        continue
                    typ = p.get("type")
                    e1, e2 = ents[p.get("e1")], ents[p.get("e2")]
                    offs = [e.get("charOffset") for e in (e1, e2)]
                    if any(";" in o for o in offs):
                        drop["discontinuous entity"] += 1
                        continue
                    spans = sorted(tuple(int(x) for x in o.split("-")) for o in offs)
                    if spans[0][1] >= spans[1][0]:
                        drop["overlapping entities"] += 1
                        continue
                    if any(text[a:b + 1] != e.get("text") for (a, b), e in
                           zip([tuple(int(x) for x in o.split("-")) for o in offs], (e1, e2))):
                        drop["offset/text mismatch"] += 1
                        continue
                    (a1, b1), (a2, b2) = spans
                    marked = (text[:a1] + "[[" + text[a1:b1 + 1] + "]]" + text[b1 + 1:a2] + "[[" + text[a2:b2 + 1]
                              + "]]" + text[b2 + 1:]).strip()
                    state = f"Sentence:\n{marked}"
                    if not (MIN_CHARS <= len(text.strip()) and len(state) <= MAX_CHARS):
                        drop["length"] += 1
                        continue
                    out.append(cand("ddi2013", p.get("id"), f"sent:{s.get('id')}", spec["raw2opt"][typ], state,
                                    [text], {"pair_id": p.get("id"), "sentence_id": s.get("id"),
                                             "document_id": doc.get("id"), "raw_label": typ,
                                             "drug1": e1.get("text"), "drug2": e2.get("text"),
                                             "subcorpus": "DrugBank" if "DrugBank" in n else "MedLine"}))
    return out, {"files": len(names), "dropped": dict(drop)}


def ei_abstract(raw: str) -> str:
    """Title + abstract of an evidence-inference .abst file: stop at the first BODY.* heading, drop the TITLE/ABSTRACT
    markers and shorten 'ABSTRACT.RESULTS:' style headings to 'RESULTS:' (text itself untouched). Some files double the
    prefix ('ABSTRACT.ABSTRACT.AIMS.', 'ABSTRACT.ABSTRACT:'): every leading 'ABSTRACT.' is removed."""
    out = []
    for line in raw.splitlines():
        s = line.strip()
        if re.match(r"^BODY[.:]", s):
            break
        if re.fullmatch(r"(TITLE|ABSTRACT)([.:]ABSTRACT)*[.:]*", s):
            continue
        m = re.fullmatch(r"(?:ABSTRACT\.)+(.+?)[.:]*", s)
        out.append(m.group(1).strip() + ":" if m else s)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def load_ei() -> tuple[list[dict], dict, dict]:
    files = {"ei_annotations": fetch(EI_RAW + "annotations/annotations_merged.csv", "ei_annotations_merged.csv"),
             "ei_prompts": fetch(EI_RAW + "annotations/prompts_merged.csv", "ei_prompts_merged.csv"),
             "ei_test_ids": fetch(EI_RAW + "annotations/splits/test_article_ids.txt", "ei_test_article_ids.txt"),
             "ei_readme": fetch(EI_RAW + "annotations/README.md", "ei_annotations_README.md"),
             "ei_guide": fetch(EI_RAW + "README.annotation_process.md", "ei_README.annotation_process.md")}
    ann, prm = pd.read_csv(files["ei_annotations"]), pd.read_csv(files["ei_prompts"]).set_index("PromptID")
    test = {int(x) for x in files["ei_test_ids"].read_text().split()}
    readme = files["ei_readme"].read_text(encoding="utf-8-sig")
    flagged = set()  # prompt ids the dataset authors flag as incorrect / questionable / somewhat malformed
    for sec in ("Incorrect", "Questionable", "Somewhat malformed"):
        m = re.search(r"### " + sec + r":\s*\n([0-9,\s]+)", readme)
        flagged |= {int(x) for x in re.findall(r"\d+", m.group(1))}
    spec, out, drop = TASKS["evidence_inference"], [], Counter()
    abstracts, missing = {}, 0
    for pm in sorted(test):
        p = fetch_optional(EI_RAW + f"annotations/abstracts/PMC{pm}.abst", f"ei_abstracts/PMC{pm}.abst")
        if p is None:
            missing += 1
        else:
            abstracts[pm] = ei_abstract(p.read_text(encoding="utf-8"))
    ann = ann[ann.PMCID.isin(test)]
    for pid, df in ann.groupby("PromptID"):
        pm = int(df.PMCID.iloc[0])
        if pid in flagged:
            drop["prompt flagged by the dataset authors"] += 1
            continue
        if pm not in abstracts:
            drop["no abstract file in the release"] += 1
            continue
        v = df[df["Valid Label"] == True]  # noqa: E712  (pandas bool column)
        labs = set(v.Label)
        if not len(v) or len(labs) != 1 or labs & {"invalid prompt"}:
            drop["no valid label, validated labels disagree, or invalid prompt"] += 1
            continue
        if not v["In Abstract"].all():
            drop["an annotator needed more than the abstract"] += 1
            continue
        abstract = abstracts[pm]
        a_norm = ws(abstract).lower()
        if not any(isinstance(e, str) and len(ws(e)) > 10 and ws(e).lower() in a_norm for e in v.Annotations):
            drop["no validated evidence quote found verbatim in the abstract"] += 1
            continue
        o, i, c = (ws(str(prm.loc[pid, k])) if pd.notna(prm.loc[pid, k]) else "" for k in
                   ("Outcome", "Intervention", "Comparator"))
        if not (o and i and c):
            drop["empty outcome/intervention/comparator"] += 1
            continue
        fill = {"outcome": o, "intervention": i, "comparator": c}
        instr = "".join(fill.get(t, t) for t in re.split(r"\b(outcome|intervention|comparator)\b", EI_TEMPLATE))
        state = f"Abstract:\n{abstract}"
        if not (MIN_CHARS <= len(state) <= MAX_CHARS):
            drop["length"] += 1
            continue
        lab = labs.pop()
        x = cand("evidence_inference", str(pid), f"pmc:{pm}", spec["raw2opt"][lab], state, [abstract],
                 {"prompt_id": int(pid), "pmcid": pm, "raw_label": lab, "n_validated_annotations": int(len(v)),
                  "outcome": o, "intervention": i, "comparator": c})
        x["instructions"] = instr
        out.append(x)
    assert ws(EI_TEMPLATE) in ws(files["ei_guide"].read_text(encoding="utf-8")), "EI prompt template not verbatim"
    return out, {"test_articles": len(test), "abstract_files_missing": missing, "flagged_prompt_ids": len(flagged),
                 "dropped": dict(drop)}, files


# ------------------------------------------------------------------ decontamination
def build_index(cands: list[dict]):
    by_text = defaultdict(set)  # many RCT candidates share one abstract: index each distinct text once
    for i, c in enumerate(cands):
        for t in c["core"]:
            by_text[t].add(i)
    keys = defaultdict(set)
    for t, ids in by_text.items():
        for k in grams(t):
            keys[k] |= ids
    pref = defaultdict(set)  # first 3 words -> gram lengths starting with them
    for n, k in keys:
        w = k.split(" ")
        pref[tuple(w[:3])].add(n)
    return keys, pref


def scan_text(text: str, keys, pref, hit: set):
    w = words(text)
    for i in range(len(w) - 2):
        ns = pref.get((w[i], w[i + 1], w[i + 2]))
        if ns:
            for n in ns:
                if i + n <= len(w):
                    ids = keys.get((n, " ".join(w[i:i + n])))
                    if ids:
                        hit |= ids


def is_heldout(p: Path) -> bool:
    rel = p.resolve().relative_to(DATA.resolve())
    return rel.parts[0].lower().startswith("ohs") or any(x.lower() in ("ohs", "ohs_parts", "ohs2_parts", "bench")
                                                         for x in rel.parts)


def decontaminate(cands: list[dict]) -> tuple[set, dict]:
    keys, pref = build_index(cands)
    hits_lean, hits_pqa, seen, nfiles = set(), set(), set(), 0
    for f in sorted(DATA.rglob("*.jsonl")):
        if is_heldout(f):
            continue
        nfiles += 1
        with open(f) as fh:
            for line in fh:
                try:
                    st = json.loads(line).get("state")
                except Exception:
                    continue
                if not isinstance(st, str):
                    continue
                h = hash(st)
                if h in seen:
                    continue
                seen.add(h)
                scan_text(st, keys, pref, hits_lean)
    pqa_pmids = set()
    for f in PQA_FILES:
        df = pd.read_parquet(hf_hub_download(PQA_REPO, f, repo_type="dataset"))
        pqa_pmids |= {str(x) for x in df["pubid"]}
        for q, ctx, la in zip(df["question"], df["context"], df["long_answer"]):
            scan_text(" ".join([str(q), " ".join(ctx["contexts"]), str(la)]), keys, pref, hits_pqa)
    hits_gli, hits_zsl, n_gli, n_zsl = set(), set(), 0, 0
    for t in gliclass_texts():
        n_gli += 1
        scan_text(t, keys, pref, hits_gli)
    for t in label_nli_texts():
        n_zsl += 1
        scan_text(t, keys, pref, hits_zsl)
    ext = {i: "GLiClass training text" for i in hits_gli}
    ext.update({i: "zero-shot-label-nli premise" for i in hits_zsl})
    return hits_lean | hits_pqa, {"lean_files_scanned": nfiles, "lean_unique_states": len(seen),
                                   "pubmedqa_files": PQA_FILES, "pubmedqa_pmids": len(pqa_pmids),
                                   "hits_lean_data": len(hits_lean), "hits_pubmedqa": len(hits_pqa),
                                   "ext_revisions": EXT_REV, "gliclass_unique_texts": n_gli,
                                   "label_nli_unique_premises": n_zsl, "hits_gliclass (skipped lazily)": len(hits_gli),
                                   "hits_label_nli (skipped lazily)": len(hits_zsl),
                                   "_pqa_pmids": pqa_pmids, "_ext": ext}


def _ext_file(repo: str, fn: str) -> str:
    return hf_hub_download(repo, fn, repo_type="dataset", revision=EXT_REV[repo])


def gliclass_texts():
    """Unique GLiClass training texts (Jev side), as in ohs2/build_misc.py."""
    seen = set()
    def new(t):
        if not t or t in seen:
            return False
        seen.add(t)
        return True
    for fn in ["data/train-00000-of-00003.parquet", "data/train-00001-of-00003.parquet",
               "data/train-00002-of-00003.parquet"]:
        pf = pq.ParquetFile(_ext_file("knowledgator/gliclass-v2.0", fn))
        for i in range(pf.num_row_groups):
            yield from filter(new, pf.read_row_group(i, columns=["text"]).column(0).to_pylist())
    yield from filter(new, pq.read_table(_ext_file("knowledgator/gliclass-v3-logic-dataset",
                                                   "data/train-00000-of-00001.parquet"),
                                         columns=["text"]).column(0).to_pylist())
    raw = open(_ext_file("knowledgator/GLIClass-v1.0", "zero-class-whole.json"), encoding="utf-8").read()
    dec, i = json.JSONDecoder(), raw.index("[") + 1
    while True:
        while i < len(raw) and raw[i] in " \n\r\t,":
            i += 1
        if i >= len(raw) or raw[i] == "]":
            break
        obj, i = dec.raw_decode(raw, i)
        if isinstance(obj, dict) and new(obj.get("text")):
            yield obj["text"]


def label_nli_texts():
    """Unique tasksource/zero-shot-label-nli premises (forbidden source)."""
    seen = set()
    for fn in ZSL_FILES:
        for x in pq.read_table(_ext_file("tasksource/zero-shot-label-nli", fn), columns=["premise"]).column(0).to_pylist():
            if x and x not in seen:
                seen.add(x)
                yield x


# ------------------------------------------------------------------ sampling
def quotas(options: list[str], avail: Counter) -> dict:
    k, cap = len(options), int(CAP * N_PER_TASK)
    q = {o: min(N_PER_TASK // k, avail[o]) for o in options}
    rest = N_PER_TASK - sum(q.values())
    for o in options[: N_PER_TASK % k]:  # remainder, if any, in label order
        if rest and q[o] < min(cap, avail[o]):
            q[o] += 1
            rest -= 1
    while rest:  # shortfall: top up other classes, never over the cap
        grow = [o for o in options if q[o] < min(cap, avail[o])]
        if not grow:
            break
        for o in grow:
            if rest:
                q[o] += 1
                rest -= 1
    return q


def sample(task: str, cands: list[dict], taken_grams: set, per_doc_max: int | None = None):
    spec = TASKS[task]
    rng = random.Random(f"{SEED}:{task}")
    pool = sorted(cands, key=lambda c: c["key"])
    rng.shuffle(pool)
    by = defaultdict(list)
    for c in pool:
        by[c["gold"]].append(c)
    avail = Counter({o: len({c["group"] for c in by[o]}) for o in spec["options"]})
    q = quotas(spec["options"], avail)
    chosen, groups, docs, texts, skipped = [], set(), Counter(), set(), Counter()
    ptr = {o: 0 for o in spec["options"]}
    need = dict(q)
    cap = int(CAP * N_PER_TASK)
    topped_up = Counter()
    while True:  # round-robin over classes so shared groups are split fairly
        progressed = False
        if not any(need.values()):
            # a class ran out of usable candidates: move its unfilled quota to classes that still have some (cap kept)
            deficit = N_PER_TASK - len(chosen)
            open_ = [o for o in spec["options"] if ptr[o] < len(by[o]) and q[o] + topped_up[o] < cap]
            if not deficit or not open_:
                break
            for o in open_[:deficit]:
                need[o] += 1
                topped_up[o] += 1
        for o in spec["options"]:
            if not need[o]:
                continue
            while ptr[o] < len(by[o]):
                c = by[o][ptr[o]]
                ptr[o] += 1
                if c["group"] in groups:
                    skipped["group already used"] += 1
                    continue
                if c.get("ext_hit"):
                    skipped[f"shares a 12-word run with a {c['ext_hit']}"] += 1
                    continue
                if per_doc_max and docs[c["meta"].get("document_id")] >= per_doc_max:
                    skipped["document quota"] += 1
                    continue
                if norm(c["state"]) in texts:
                    skipped["duplicate state"] += 1
                    continue
                g = set().union(*(grams(t) for t in c["core"]))
                if g & taken_grams:
                    skipped["shares a 12-word run with an already selected item"] += 1
                    continue
                chosen.append(c)
                groups.add(c["group"])
                docs[c["meta"].get("document_id")] += 1
                texts.add(norm(c["state"]))
                taken_grams |= g
                need[o] -= 1
                progressed = True
                break
        if not progressed:
            if any(need.values()):  # this class is exhausted: drop its unmet need, let the top-up move it
                for o in spec["options"]:
                    if need[o] and ptr[o] >= len(by[o]):
                        skipped[f"class exhausted ({o}), quota moved"] += need[o]
                        need[o] = 0
                if any(need.values()):
                    break
                continue
            break
    return chosen, q, dict(skipped), {"topped_up": dict(topped_up),
                                      "short_of_n": N_PER_TASK - len(chosen)}


# ------------------------------------------------------------------ main
def main():
    files = {
        "rct": fetch(RCT_URL, "pubmed_20k_rct_test.txt"),
        "scifact": fetch(SCIFACT_URL, "scifact_data.tar.gz"),
        "scifact_guide": fetch(SCIFACT_GUIDE_URL, "scifact_evidence_annotation_instructions.pdf"),
        "ddi": fetch(DDI_ZIP_URL, "DDICorpus-2013.zip"),
        "ddi_page": fetch(DDI_PAGE_URL, "ddicorpus.webarchive"),
    }
    card_check = check_cards(files)

    ei_rows, ei_stat, ei_files = load_ei()
    files.update(ei_files)
    card_check["evidence_inference"] = "prompt template found verbatim in README.annotation_process.md"
    loaded = {"pubmed_rct20k": load_rct(files["rct"]), "scifact": load_scifact(files["scifact"]),
              "evidence_inference": (ei_rows, ei_stat), "ddi2013": load_ddi(files["ddi"])}
    if WITH_MEDICAL:
        loaded["medical_abstracts"] = load_medical()
    allc = [c for t in ORDER for c in loaded[t][0]]
    hits, dstat = decontaminate(allc)
    pqa_pmids = dstat.pop("_pqa_pmids")
    for i, why in dstat.pop("_ext").items():
        allc[i]["ext_hit"] = why
    for i in hits:
        allc[i]["contaminated"] = True
    for c in allc:
        if c["task"] == "pubmed_rct20k" and c["meta"]["pmid"] in pqa_pmids:
            c["contaminated"] = True
    # a contaminated RCT abstract drops every sentence of that abstract (core text is the whole abstract already)

    rows, report, taken = [], {}, set()
    for task in ORDER:
        spec = TASKS[task]
        cands, lstat = loaded[task]
        clean = [c for c in cands if not c.get("contaminated")]
        dropped_contam = Counter(c["gold"] for c in cands if c.get("contaminated"))
        chosen, q, skipped, short = sample(task, clean, taken, per_doc_max=3 if task == "ddi2013" else None)
        card = None if spec["card"] is None else "\n".join(f"- {o}: {spec['card'][o]}" for o in spec["options"])
        for c in sorted(chosen, key=lambda c: (spec["options"].index(c["gold"]), c["key"])):
            meta = {"task": task, "source_id": spec["source_id"], "source_split": spec["source_split"],
                    "licence": spec["licence"], "n_options": len(spec["options"]), "card_source": spec["card_source"],
                    **c["meta"]}
            rows.append({"id": "r_" + sid(SPLIT, task, c["key"]), "group_id": f"g:{task}:{c['group']}",
                         "call_id": "c_" + sid(c["state"]), "split": SPLIT, "track": TRACK, "source": task,
                         "state": c["state"], "qtype": "choice", "instructions": c.get("instructions", spec["instructions"]),
                         "options": list(spec["options"]), "gold": c["gold"], "role": "choice", "card": card,
                         "meta": meta})
        bal = Counter(c["gold"] for c in chosen)
        report[task] = {
            "source_id": spec["source_id"], "licence": spec["licence"], "split": spec["source_split"], "n": len(chosen),
            "options": spec["options"], "balance": {o: bal[o] for o in spec["options"]},
            "max_class_share": round(max(bal.values()) / len(chosen), 3), "quotas": q, "shortfall": short,
            "candidates": len(cands), "candidates_by_class": dict(Counter(c["gold"] for c in cands)),
            "dropped_contaminated": dict(dropped_contam), "loader": {k: v for k, v in lstat.items() if k != "pmids"},
            "sampling_skips": skipped, "card": spec["card_source"],
            "state_chars": {"min": min(len(c["state"]) for c in chosen), "max": max(len(c["state"]) for c in chosen)},
        }

    # sanity checks
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert len({r["call_id"] for r in rows}) == len(rows), "one row per state expected"
    for r in rows:
        assert r["gold"] in r["options"] and not any(": " in o for o in r["options"])
        assert MIN_CHARS <= len(r["state"]) <= MAX_CHARS
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = {"part": "science", "split": SPLIT, "track": TRACK, "seed": SEED, "rows": len(rows),
               "tasks": report, "card_check": card_check, "decontamination": dstat,
               "source_sha256": {k: sha256(p) for k, p in files.items()},
               "output_sha256": sha256(OUT),
               "not_used": {
                   "SciCite / ACL-ARC citation intent / SciERC / PUBHEALTH / scientific exaggeration":
                       "in the v0.11 task bank via tasksource zero-shot-label-nli (trained on); forbidden",
                   "PubMedQA": "OHS-1 source; used only as a decontamination reference",
                   "SciNLI": "texts from ACL Anthology papers, many also on arXiv (arXiv papers before 2026-09-21 are "
                             "forbidden); skipped to be safe",
                   "SciFact test": "labels not released; dev used",
                   "medical_abstracts": ("built only with --with-medical (in this run: %s); OHS-2 part 'misc' already "
                                         "has a medical_abstracts task" % WITH_MEDICAL),
                   "DDI non-interacting pairs": "no official definition for the negative class; typed DDIs only"},
               "llm_calls": 0}
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({t: {k: report[t][k] for k in ("n", "balance", "shortfall", "dropped_contaminated")}
                      for t in ORDER}, indent=1))
    print("decontam", dstat)


if __name__ == "__main__":
    main()
