"""LR-50 QuaRTz (allenai/quartz; Tafjord et al. 2019). Tier C check C4: licence on a primary AI2 page. allenai.org/data/quartz
redirects to the AI2-owned card huggingface.co/datasets/allenai/quartz: 'The dataset is licensed under Creative Commons Attribution
4.0 International (CC BY 4.0)'. train parquet (2,696 rows) is staged, FIELD DROPS applied (para, para_id, para_anno, question_anno:
the background sentences are web-sourced knowledge text and are never needed) and written as train.jsonl.gz; validation and test
parquet (never opened) -> quarantine.
"""
import os
import sys

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "quartz"
HF = "allenai/quartz"
KEEP = ("id", "question", "choices", "answerKey")


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(HF)
    st.log["upstream_revision"] = rev
    paths = {r: "data/%s-00000-of-00001.parquet" % r for r in ("train", "validation", "test")}
    counts = {}
    ids = {}
    for role, rel in paths.items():
        url = dc.hf_url(HF, rev, rel)
        if role == "train":
            p, info = st.stage(url, "train.parquet")
            t = pq.read_table(p)
            cols = t.column_names
            rows = t.select([c for c in KEEP]).to_pylist()
            st.log["train_dropped_fields"] = [c for c in cols if c not in KEEP]
            st.log["upstream_train_parquet"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url, "columns": cols}
            ids["train"] = [r["id"] for r in rows]
            counts["train"] = len(rows)
            st.write_train_json("train.jsonl.gz", rows, source_urls=[url], jsonl=True, note="fields kept: %s" % ",".join(KEEP))
        else:
            dest = st.quar_path("%s/%s" % (role, os.path.basename(rel)))
            dc.fetch_to(url, dest)
            n = pq.ParquetFile(dest).metadata.num_rows   # row count from the parquet footer only
            counts[role] = n
            st.add_quar_file("%s/%s" % (role, os.path.basename(rel)), role=role, source_urls=[url], rows=n)
    st.clear_staging()
    lic = tc.licence_with_checks(
        DATASET, "LR-50",
        quote="The dataset is licensed under Creative Commons [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).",
        quote_url="https://huggingface.co/datasets/allenai/quartz (allenai.org/data/quartz redirects here)",
        verify_url=dc.hf_card_url(HF, rev), licence_class="CC-BY-4.0", provenance="human",
        notes="Card of the AI2 org page. Crowdsourced questions (card: annotations_creators crowdsourced). Background sentences "
              "(para) are not used; 'A background sentence will only appear in a single split' (card).")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
