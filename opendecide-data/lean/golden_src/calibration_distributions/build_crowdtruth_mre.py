"""Build raw rows for crowdtruth_mre (CrowdTruth Medical Relation Extraction 2.1; Dumitrache, Aroyo & Welty 2018).

Source : Zenodo record 50676 "Medical Relation Extraction Gold Standard with CrowdTruth" (deposited by the CrowdTruth
         team, snapshot of github CrowdTruth/Medical-Relation-Extraction tag 2.1), file
         Medical-Relation-Extraction-2.1.zip (sha256 pinned). Used: raw/RelEx/*.csv (one row per worker judgement),
         ground_truth_{treat,cause}.csv (only to find the evaluation sentences, which are excluded).
Licence: CC BY-SA 4.0 (Zenodo record 50676 metadata "license": "cc-by-sa-4.0", https://zenodo.org/records/50676).
Texts  : English sentences from PubMed abstracts (sampled from Wang & Fan's distant-supervision corpus); the two
         candidate medical terms are shown in capitals, exactly as the workers saw them.
Labels : ~15 CrowdFlower workers per sentence answered "Is TERM1 --related-to-- TERM2?" by ticking any of 14
         relations with on-hover definitions (TREATS, PREVENTS, DIAGNOSE_BY_TEST_OR_DRUG, CAUSES, ..., NONE).
Cleaning: sentences glued to a leading reference-number list ("211 , 226 , 242 , ...") are dropped; judgements that tick NONE together with another relation, or 5+ relations, are dropped as contradictory /
         spam; units then need >= 10 judgements. Sentences that appear in the paper's evaluation partition
         (ground_truth test_partition not empty) are excluded. Sentences sharing a 10-word run with PubMed 20k RCT
         (all splits; an OHS-2 source, used only as an exclusion list) are dropped, plus the standard decontamination.
         Review fix (29 Sep): the other PubMed-based OHS sources are exclusion lists too (10-word run or exact text):
         Medical Abstracts TC corpus (OHS-2; TimSchopf/medical_abstracts train+test, 4 shared sentences found),
         SciFact corpus (OHS-2; 1 shared sentence), PubMedQA pqa_labeled (OHS-1) and the DDI 2013 corpus (OHS-2);
         each pinned by revision/commit + sha256 and read only to drop overlaps.
Tasks  (each unit used for one question):
 - q_treats   yes-share = share of workers ticking TREATS   (penicillin cures infection)
 - q_prevents yes-share = share ticking PREVENTS             (vitamin C reduces the risk of influenza)
 - q_diagnose yes-share = share ticking DIAGNOSE_BY_TEST_OR_DRUG (RINNE test is used for determining hearing loss)
 gold yes if yes-share >= 0.6, gold no if yes-share <= 0.1 (a check against the released expert labels on TREATS:
 crowd >= 0.6 agreed with the medical expert 94% of the time). CAUSES is not used (crowd-expert agreement ~60%).
Balance: yes share ~0.45 per question. Deterministic (seed 20261101).
"""
import collections
import io
import random
import re
import zipfile

import pandas as pd

import _cal_common as C

KEY = "crowdtruth_mre"
ZIP_URL = "https://zenodo.org/api/records/50676/files/Medical-Relation-Extraction-2.1.zip/content"
ZIP_SHA = "37f6170323a71a3eb3644e0db8bf51c79bd617e1e983f01d881630e9244cf59e"
RCT_REV = "17ed2cb0590decfca0266add0c76f254f67232b4"
RCT_BASE = f"https://raw.githubusercontent.com/Franck-Dernoncourt/pubmed-rct/{RCT_REV}/PubMed_20k_RCT/"
RCT_FILES = {"train.txt": "8fda243202edd207fb61214e21f5629bba545522b921816d20d516e64d602d5b",
             "dev.txt": "8561119a162708a87e3138103470d10781c6b94ba390183d7d6df6297a738a25",
             "test.txt": "8511b832c1ee66b3df52df23c16ad81a69711ddd5b3a485421da3f8e9d5b44f4"}
OHS_BIO = {  # name -> (url, sha256); exclusion lists only
    "medical_abstracts_train.parquet": ("https://huggingface.co/datasets/TimSchopf/medical_abstracts/resolve/"
                                        "d6afbd7ff4eb215db2470980023d7d7a3dfee7dc/data/train-00000-of-00001.parquet",
                                        "0c32fa436349619a2f95dd7338a57e896ff98e6537c71de89b053bcb24aef6b0"),
    "medical_abstracts_test.parquet": ("https://huggingface.co/datasets/TimSchopf/medical_abstracts/resolve/"
                                       "d6afbd7ff4eb215db2470980023d7d7a3dfee7dc/data/test-00000-of-00001.parquet",
                                       "c4f720ada4b69e5fc8f37f4965397839d45a061d5ebb663f3bf2cce2b1209f04"),
    "pubmedqa_pqa_labeled.parquet": ("https://huggingface.co/datasets/qiaojin/PubMedQA/resolve/"
                                     "9001f2853fb87cab8d220904e0de81ac6973b318/pqa_labeled/train-00000-of-00001.parquet",
                                     "3d56bd1abc11884579ecc3aab9dd3cdfce8b7cf54715daeca93b8022b7be231c"),
    "scifact_data.tar.gz": ("https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
                            "11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be"),
    "DDICorpus-2013.zip": ("https://raw.githubusercontent.com/isegura/DDICorpus/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/"
                           "DDICorpus-2013.zip", "87fc63e32ebce20d9841c372e0c594ec72d60882ab5621550ca73c3eaf80ab60"),
}


def ohs_bio_texts():
    """{source: [texts]} of the PubMed-based OHS sources (exclusion only)."""
    import json as _json
    import tarfile
    import xml.etree.ElementTree as ET
    f = {n: C.fetch(u, CACHE / "ohs_excl" / n, h) for n, (u, h) in OHS_BIO.items()}
    out = {"medical_abstracts": [], "pubmedqa": [], "scifact": [], "ddi2013": []}
    for n in ("medical_abstracts_train.parquet", "medical_abstracts_test.parquet"):
        out["medical_abstracts"] += pd.read_parquet(f[n])["medical_abstract"].astype(str).tolist()
    d = pd.read_parquet(f["pubmedqa_pqa_labeled.parquet"])
    out["pubmedqa"] = [" ".join(c["contexts"]) for c in d["context"]] + d["long_answer"].astype(str).tolist()
    with tarfile.open(f["scifact_data.tar.gz"]) as tf:
        for line in tf.extractfile("data/corpus.jsonl").read().decode().splitlines():
            o = _json.loads(line)
            out["scifact"] += [o["title"]] + o["abstract"]
    with zipfile.ZipFile(f["DDICorpus-2013.zip"]) as zf:
        for n in zf.namelist():
            if n.endswith(".xml"):
                out["ddi2013"] += [x.get("text") or "" for x in ET.fromstring(zf.read(n)).iter("sentence")]
    return out


REFLIST = re.compile(r"^\s*(\d+\s*[,;]\s*){3,}")  # sentences glued to a reference-number list
LICENCE = ("CC BY-SA 4.0 (Zenodo record https://zenodo.org/records/50676 metadata 'license: cc-by-sa-4.0'; "
           "CrowdTruth Medical Relation Extraction 2.1)")
DATASET = "CrowdTruth Medical Relation Extraction 2.1 (Zenodo 50676), raw RelEx worker judgements"
CACHE = C.CACHE / KEY
YES_SHARE = 0.45

QS = {
    "q_treats": ("TREATS", 'Does this sentence express that one of the terms "{a}" and "{b}" is used to treat the other '
                           '(therapeutic use of a drug, ingredient or therapy)?'),
    "q_prevents": ("PREVENTS", 'Does this sentence express that one of the terms "{a}" and "{b}" is used to prevent the '
                               'other (preventive use of a drug or ingredient)?'),
    "q_diagnose": ("DIAGNOSE_BY_TEST_OR_DRUG", 'Does this sentence express that one of the terms "{a}" and "{b}" is '
                                               'used to diagnose the other (diagnostic use of a test, ingredient or drug)?'),
}
DEFS = {
    "q_treats": {
        "yes": "At least 60% of the crowd workers ticked TREATS: the sentence presents one term as a drug, ingredient or "
               "therapy used to cure or relieve the other (e.g. penicillin cures infection), including reported "
               "results such as 'was effective in treating'.",
        "no": "At most 10% ticked TREATS: in this sentence the terms are linked in another way (cause, symptom, side "
              "effect, location, diagnosis, prevention, is-a, mere co-occurrence) or not at all, whatever is true "
              "outside the sentence.",
    },
    "q_prevents": {
        "yes": "At least 60% of the crowd workers ticked PREVENTS: the sentence presents one term as a drug or "
               "ingredient used to prevent the other or lower its risk (e.g. vitamin C reduces the risk of influenza).",
        "no": "At most 10% ticked PREVENTS: the terms are linked in another way in this sentence (treatment of an "
              "existing condition, cause, symptom, diagnosis, association) or not at all.",
    },
    "q_diagnose": {
        "yes": "At least 60% of the crowd workers ticked DIAGNOSE_BY_TEST_OR_DRUG: the sentence presents one term as a "
               "test, ingredient or drug used to detect or diagnose the other (e.g. the Rinne test for hearing loss).",
        "no": "At most 10% ticked DIAGNOSE_BY_TEST_OR_DRUG: the terms are linked in another way in this sentence "
              "(treatment, cause, symptom, location, association) or not at all.",
    },
}
HYPO = re.compile(r"\b(may|might|could|possibly|potential(ly)?|suggest(s|ed)?|whether)\b", re.I)


def rels(s):
    return {x.strip() for x in re.split(r"[\[\]\n,]+", str(s)) if x.strip() and x.strip() != "nan"}


def main():
    rng = random.Random(C.SEED)
    z = C.fetch(ZIP_URL, CACHE / "Medical-Relation-Extraction-2.1.zip", ZIP_SHA)
    with zipfile.ZipFile(z) as zf:
        names = zf.namelist()
        relex = sorted(n for n in names if "/raw/RelEx/" in n and n.endswith(".csv"))
        d = pd.concat([pd.read_csv(io.BytesIO(zf.read(n))) for n in relex], ignore_index=True)
        gt = pd.concat([pd.read_csv(io.BytesIO(zf.read(n)), dtype=str) for n in names
                        if n.endswith(("ground_truth_treat.csv", "ground_truth_cause.csv"))], ignore_index=True)
    test_sents = {C.norm(s) for s in gt[gt.test_partition.notna()].sentence}
    print("RelEx judgements:", len(d), "evaluation sentences excluded:", len(test_sents))

    d["R"] = d.relations.apply(rels)
    d = d[d.R.apply(lambda r: len(r) >= 1 and not ("NONE" in r and len(r) > 1) and len(r) <= 4)]
    d["t1"] = d.term1.astype(str).str.strip()
    d["t2"] = d.term2.astype(str).str.strip()
    units = []
    for (sent, t1, t2), g in d.groupby(["sentence", "t1", "t2"], sort=True):
        g = g.drop_duplicates("_worker_id")
        n = len(g)
        if n < 10:
            continue
        s = C.clean(sent)
        if C.norm(s) in test_sents or len(C.words(s)) < 6 or REFLIST.match(s):
            continue
        shares = {q: sum(rel in r for r in g.R) for q, (rel, _) in QS.items()}
        units.append({"uid": str(g._unit_id.iloc[0]), "sent": s, "t1": t1, "t2": t2, "n": n, "votes": shares,
                      "none": sum(r == {"NONE"} for r in g.R),
                      "top": collections.Counter(x for r in g.R for x in sorted(r)).most_common(3)})
    print("units:", len(units))

    rct = []
    for n_ in RCT_FILES:
        p = C.fetch(RCT_BASE + n_, CACHE / "pubmed_20k_rct" / n_, RCT_FILES[n_])
        for line in open(p, encoding="utf-8"):
            if "\t" in line:
                rct.append(line.split("\t", 1)[1])
    core = {u["uid"] + "|" + u["t1"] + "|" + u["t2"]: [u["sent"]] for u in units}
    extra = {"pubmed_rct": rct}
    extra.update(ohs_bio_texts())
    hits = C.decon(core, KEY, extra_texts=extra)
    hits.update(C.cross_v14(core, {KEY}))
    units = [u for u in units if u["uid"] + "|" + u["t1"] + "|" + u["t2"] not in hits]
    print("after overlap checks:", len(units), dict(collections.Counter(v.split(":")[0] for v in hits.values())))

    cands = collections.defaultdict(list)
    for u in units:
        for q in QS:
            p = u["votes"][q] / u["n"]
            if p >= 0.6:
                cands[(q, "yes")].append(u)
            elif p <= 0.1:
                cands[(q, "no")].append(u)
    print("candidates:", {f"{q}/{g}": len(x) for (q, g), x in sorted(cands.items())})
    for k in sorted(cands):
        rng.shuffle(cands[k])
    used_sent = set()
    out = {}
    order = sorted(QS, key=lambda q: len(cands[(q, "yes")]))  # scarcest question first
    for q in order:
        ys = []
        for u in cands[(q, "yes")]:
            if C.norm(u["sent"]) not in used_sent:
                used_sent.add(C.norm(u["sent"]))
                ys.append(u)
        target_no = int(len(ys) * (1 - YES_SHARE) / YES_SHARE)
        ns = []
        # hard negatives first: units the crowd linked by some other relation (not NONE-dominated)
        pool = sorted(cands[(q, "no")], key=lambda u: u["none"] / u["n"])
        for u in pool:
            if len(ns) >= target_no:
                break
            if C.norm(u["sent"]) not in used_sent:
                used_sent.add(C.norm(u["sent"]))
                ns.append(u)
        out[(q, "yes")], out[(q, "no")] = ys, ns
    print({f"{q}/{g}": len(x) for (q, g), x in out.items()})

    rows = []
    for (q, g), lst in out.items():
        for u in lst:
            t = u["sent"]
            e = None
            if C.neg_count(t):
                e = "negation"
            elif HYPO.search(t):
                e = "hypothetical"
            elif C.NUM.search(t):
                e = "numeric"
            rows.append({
                "key": KEY, "rid": f"ctmre-{q}-{u['uid']}-{C.norm(u['t1'])[:20]}-{C.norm(u['t2'])[:20]}".replace(" ", "_"),
                "state": t, "instructions": QS[q][1].format(a=u["t1"], b=u["t2"]), "options": C.YN, "gold": g,
                "soft": C.soft_yes(u["votes"][q], u["n"]),
                "meta": {"dataset": DATASET, "config": f"RelEx / {QS[q][0]}", "revision": f"zenodo:50676 zip sha256 {ZIP_SHA}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"n_workers": u["n"], f"{QS[q][0]}_votes": u["votes"][q],
                                        "NONE_votes": u["none"], "top_relations": u["top"]},
                         "family": C.FAMILY, "edge": e, "defs": q},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    C.show_samples(rows, 6)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Soft = share of ~15 CrowdFlower workers ticking the relation (contradictory NONE+X and 5+-relation "
        "judgements dropped). Gold >= 0.6 yes / <= 0.1 no. Three defs files (__q_treats, __q_prevents, __q_diagnose). "
        "Paper evaluation sentences excluded; overlaps with PubMed 20k RCT, Medical Abstracts TC, SciFact, DDI 2013 "
        "(OHS-2) and PubMedQA pqa_labeled (OHS-1) dropped.", st))


if __name__ == "__main__":
    main()
