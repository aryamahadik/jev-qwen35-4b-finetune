"""LR-49 e-CARE (Waste-Wood/e-CARE; ACL 2022). Tier C check C2: read the repo LICENSE file ('MIT License / Copyright (c) 2022
HIT-SCIR: Social Prediction'). Only dataset/Causal_Reasoning/{train,dev}.jsonl are fetched: train -> train/; dev -> quarantine/dev/
(G13 target). The test set is a BLIND set held by the authors (never in the repo). train_full.jsonl / dev_full.jsonl and the
Explanation_Generation files (they carry the GenericsKB-derived conceptual explanations) are NEVER fetched: check C2 says do not use
the GenericsKB explanations, and the mapper needs none.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "ecare"
GH = "Waste-Wood/e-CARE"
FILES = [("dataset/Causal_Reasoning/train.jsonl", "train"), ("dataset/Causal_Reasoning/dev.jsonl", "dev")]


def run():
    st = dc.Store(DATASET)
    ref = dc.gh_commit_sha(GH, "HEAD")
    st.log["upstream_commit"] = ref
    counts, keys = {}, {}
    for rel, role in FILES:
        url = dc.raw_url(GH, ref, rel)
        fn = os.path.basename(rel)
        if role == "train":
            dc.fetch_to(url, st.train_path(fn))
            p = st.train_path(fn)
        else:
            dc.fetch_to(url, st.quar_path(role + "/" + fn))
            p = st.quar_path(role + "/" + fn)
        rows = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
        counts[role] = len(rows)
        keys[role] = [r["index"] for r in rows]
        keys[role + "_t"] = [r["premise"] + "|" + r["hypothesis1"] + "|" + r["hypothesis2"] for r in rows]
        if role == "train":
            st.add_train_file(fn, source_urls=[url], rows=len(rows))
            st.log["train_field_names"] = sorted({k for r in rows for k in r})
        else:
            st.add_quar_file(role + "/" + fn, role=role, source_urls=[url], rows=len(rows))
    dc.record_overlap(st, "index_train_vs_dev", keys["train"], keys["dev"])
    dc.record_overlap(st, "premise_hypotheses_text_train_vs_dev", keys["train_t"], keys["dev_t"])
    lic = tc.licence_with_checks(
        DATASET, "LR-49", quote="MIT License\n\nCopyright (c) 2022 HIT-SCIR: Social Prediction",
        quote_url="https://github.com/Waste-Wood/e-CARE/blob/%s/LICENSE" % ref, verify_url=dc.raw_url(GH, ref, "LICENSE"),
        licence_class="MIT", provenance="human",
        notes="Check C2 (read the LICENSE file): the repo LICENSE is the standard MIT text, copyright HIT-SCIR: Social Prediction. The repo "
              "README states no separate data licence. Crowd annotators wrote the causal fact (premise + true hypothesis, from a "
              "GenericsKB statement) and the implausible hypothesis (paper section 3); the conceptual-explanation field is NOT fetched or used.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
