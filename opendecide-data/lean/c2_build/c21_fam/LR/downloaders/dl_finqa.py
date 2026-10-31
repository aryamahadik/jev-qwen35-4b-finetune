"""LR-44 FinQA (Chen et al., EMNLP 2021; czyssrs/FinQA). Tier C check C8: owner line O7 (CDLA) = YES (A82 7).
Repo LICENSE 'MIT License / Copyright (c) 2021 Zhiyu Chen' covers the annotations; the financial-report text and tables come from
FinTabNet, which the FinQA paper (section 8 'Data Access and Licensing') says is 'publicly available under the CDLA-Permissive'
licence; the IBM Data Asset Exchange page for FinTabNet (Internet Archive capture of 2021-06-17) lists 'License CDLA-Permissive'
(no version; a capture of June 2021 predates CDLA-Permissive-2.0, so this is CDLA-Permissive-1.0 by inference). OPEN FLAG: A82 7
names CDLA-Permissive-2.0; split_aware_check v2.1 allows 1.0 and 2.0; the FinQA paper's footnote links the cdla.dev/sharing-1-0
page. Opus confirms the version at the tier-C result review.
train.json (6,251 train items) -> train/ (gzip); dev.json, test.json, private_test.json -> quarantine (G13 targets; never opened).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "finqa"
GH = "czyssrs/FinQA"


def run():
    st = dc.Store(DATASET)
    ref = dc.gh_commit_sha(GH, "HEAD")
    st.log["upstream_commit"] = ref
    counts, keys = {}, {}
    url = dc.raw_url(GH, ref, "dataset/train.json")
    p, info = st.stage(url, "train.json")
    obj = json.load(open(p, encoding="utf-8"))
    counts["train"] = len(obj)
    keys["train"] = [r["id"] for r in obj]
    keys["train_q"] = [r["qa"]["question"] for r in obj]
    st.log["upstream_train_json"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url}
    st.write_train_json("train.json.gz", obj, source_urls=[url], rows=len(obj))
    for role in ("dev", "test", "private_test"):
        u = dc.raw_url(GH, ref, "dataset/%s.json" % role)
        dc.fetch_to(u, st.quar_path("%s/%s.json" % (role, role)))
        o = json.load(open(st.quar_path("%s/%s.json" % (role, role)), encoding="utf-8"))
        counts[role] = len(o)
        st.add_quar_file("%s/%s.json" % (role, role), role=role, source_urls=[u], rows=len(o))
        keys[role] = [r["id"] for r in o]
        keys[role + "_q"] = [r["qa"]["question"] for r in o]
        dc.record_overlap(st, "id_train_vs_" + role, keys["train"], keys[role])
        dc.record_overlap(st, "question_text_train_vs_" + role, keys["train_q"], keys[role + "_q"])
    st.clear_staging()
    lic = tc.licence_with_checks(
        DATASET, "LR-44", quote="MIT License\n\nCopyright (c) 2021 Zhiyu Chen",
        quote_url="https://github.com/czyssrs/FinQA/blob/%s/LICENSE" % ref, verify_url=dc.raw_url(GH, ref, "LICENSE"),
        licence_class="MIT (annotations) + CDLA-Permissive (FinTabNet report text and tables; version unstated, 1.0 by date inference)",
        provenance="human",
        notes="Check C8 = owner line O7 (CDLA-Permissive allowed, A82 7). OPEN FLAG for Opus: the CDLA version. 11 finance professionals "
              "(Upwork) wrote the questions and programs. The HF mirror ibm-research/finqa card says cc-by-4.0 (not used as evidence).",
        also=[{"label": "FinQA paper section 8 (FinTabNet is under CDLA-Permissive)",
               "quote": "The FinTabNet dataset is publicly available under the CDLA-Permissive",
               "url": "https://arxiv.org/abs/2109.00122", "verify_url": "https://ar5iv.labs.arxiv.org/html/2109.00122",
               "licence_class": "CDLA-Permissive"},
              {"label": "IBM Data Asset Exchange FinTabNet page, Internet Archive capture of 2021-06-17",
               "quote": "License CDLA-Permissive",
               "url": "https://developer.ibm.com/technologies/artificial-intelligence/data/fintabnet/",
               "verify_url": "https://web.archive.org/web/20210617175027/https://developer.ibm.com/technologies/artificial-intelligence/data/fintabnet/",
               "licence_class": "CDLA-Permissive"}])
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
