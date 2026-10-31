"""LR-48 Social IQa v1.4 (Sap et al. 2019; AI2 / maartensap.com). Tier C check C3: ATOMIC-2019 licence readable and permissive.
Train + dev come from AI2's own zip (storage.googleapis.com/ai2-mosaic/public/socialiqa/socialiqa-train-dev.zip); the test set is
hidden (not in that zip). train.jsonl + train-labels.lst -> train/; dev.jsonl + dev-labels.lst -> quarantine/dev/ (G13 target).
The 'withDims' package (which ALSO holds the test items) is staged in quarantine only to extract two documentation members by NAME:
README.md (answer-source legend: hca = handwritten correct, hia = handwritten incorrect, qsa = question-switched, all human) and
LICENCE-CC-BY-4.0.txt (the licence shipped with the data). No other member of that tarball is read.
"""
import hashlib
import os
import sys
import tarfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "social_iqa"
HF = "allenai/social_i_qa"
URL_ZIP = "https://storage.googleapis.com/ai2-mosaic/public/socialiqa/socialiqa-train-dev.zip"
URL_DIMS = "https://maartensap.com/social-iqa/data/socialIQa_v1.4_withDims.tgz"
DOC_MEMBERS = ("socialIQa_v1.4_withDims/README.md", "socialIQa_v1.4_withDims/LICENCE-CC-BY-4.txt")


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(HF)
    st.log["upstream_revision_card"] = rev
    zp, zi = st.stage(URL_ZIP, "socialiqa-train-dev.zip")
    st.log["staged_file"] = {"sha256": zi["sha256"], "bytes": zi["bytes"], "url": URL_ZIP}
    counts, keys = {}, {}
    with zipfile.ZipFile(zp) as z:
        for member, role, rel in (("socialiqa-train-dev/train.jsonl", "train", "train.jsonl"),
                                  ("socialiqa-train-dev/train-labels.lst", "train", "train-labels.lst"),
                                  ("socialiqa-train-dev/dev.jsonl", "dev", "dev.jsonl"),
                                  ("socialiqa-train-dev/dev-labels.lst", "dev", "dev-labels.lst")):
            data = z.read(member)
            if role == "train":
                with open(st.train_path(rel), "wb") as f:
                    f.write(data)
                n = data.count(b"\n")
                st.add_train_file(rel, source_urls=[URL_ZIP], rows=n)
                counts["train_" + rel] = n
            else:
                dest = st.quar_path("dev/" + rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(data)
                n = data.count(b"\n")
                st.add_quar_file("dev/" + rel, role="dev", source_urls=[URL_ZIP], rows=n)
                counts["dev_" + rel] = n
    import json
    ctx = {"train": [], "dev": []}
    for role, p in (("train", st.train_path("train.jsonl")), ("dev", st.quar_path("dev/dev.jsonl"))):
        for line in open(p, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                ctx[role].append(r["context"] + "|" + r["question"])
    dc.record_overlap(st, "context_question_train_vs_dev", ctx["train"], ctx["dev"])
    dp, di = st.stage(URL_DIMS, "socialIQa_v1.4_withDims.tgz")
    docs = {}
    with tarfile.open(dp, "r:gz") as t:
        for name in DOC_MEMBERS:
            b = t.extractfile(name).read()
            rel = "shipped_" + os.path.basename(name)
            with open(st.train_path(rel), "wb") as f:
                f.write(b)
            st.add_train_file(rel, source_urls=[URL_DIMS], note="documentation member of the withDims package")
            docs[os.path.basename(name)] = hashlib.sha256(b).hexdigest()
    st.clear_staging()
    lic = tc.licence_with_checks(
        DATASET, "LR-48", quote="### Licensing Information\n\nCC-BY-4.0",
        quote_url="https://huggingface.co/datasets/allenai/social_i_qa (AI2 org card; allenai.org/data/socialiqa redirects here)",
        verify_url=dc.hf_card_url(HF, rev), licence_class="CC-BY-4.0", provenance="human",
        notes="Card-only statement for Social IQa itself, backed by the licence file SHIPPED with the data package (LICENCE-CC-BY-4.txt, "
              "'Attribution 4.0 International', sha in shipped_licence_files). Provenance (paper arXiv 1904.09728 section 3.3): MTurk "
              "workers wrote contexts, questions and correct answers; incorrect answers are handwritten (hia) or question-switched "
              "handwritten answers (qsa); final correct answer by human majority vote; adversarial filtering with a style classifier only on "
              "dev/test, not train. The card's 'machine-generated' wording is not supported by the paper or the shipped README. Check C3 "
              "(ATOMIC-2019 licence): see also_verified; contexts were seeded from ATOMIC event templates.",
        also=[{"label": "ATOMIC 2019 (allenai/atomic card; allenai.org/data/atomic redirects here)",
               "quote": "The Creative Commons Attribution 4.0 International License.",
               "url": "https://huggingface.co/datasets/allenai/atomic", "verify_url": dc.hf_card_url("allenai/atomic", dc.hf_revision("allenai/atomic"))},
              {"label": "allenai/comet-atomic-2020 README (ATOMIC 2020 dataset licence; context only)",
               "quote": "The ATOMIC 2020 dataset is licensed under CC-BY.",
               "url": "https://github.com/allenai/comet-atomic-2020", "verify_url": "https://github.com/allenai/comet-atomic-2020"}],
        extra={"shipped_licence_files": docs})
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
