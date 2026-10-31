"""LR-12 MBPP, FULL config, TRAIN split only (Austin et al. 2021; google-research-datasets/mbpp). Tier C check C14: card licence
CC-BY-4.0 ('Licensing Information: CC-BY-4.0'); problem-level G13 against the CodeMind sources and REval is the registry program's job
(the test / validation / prompt parquet go to quarantine as the G13 targets; the sanitized config is not fetched: its problems are
subsets of the same ids). train parquet (374 rows) -> train/train.jsonl.gz, all fields (text, code, test_list, test_setup_code,
challenge_test_list: crowd-written).
"""
import os
import sys

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "mbpp"
HF = "google-research-datasets/mbpp"


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(HF)
    st.log["upstream_revision"] = rev
    counts, ids = {}, {}
    for role in ("train", "test", "validation", "prompt"):
        rel = "full/%s-00000-of-00001.parquet" % role
        url = dc.hf_url(HF, rev, rel)
        if role == "train":
            p, info = st.stage(url, "train.parquet")
            t = pq.read_table(p)
            rows = t.to_pylist()
            counts[role] = len(rows)
            ids[role] = [r["task_id"] for r in rows]
            st.log["upstream_train_parquet"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url, "columns": t.column_names}
            st.write_train_json("train.jsonl.gz", rows, source_urls=[url], jsonl=True)
        else:
            dest = st.quar_path("%s/%s" % (role, os.path.basename(rel)))
            dc.fetch_to(url, dest)
            n = pq.ParquetFile(dest).metadata.num_rows
            counts[role] = n
            st.add_quar_file("%s/%s" % (role, os.path.basename(rel)), role=role, source_urls=[url], rows=n)
    st.clear_staging()
    lic = tc.licence_with_checks(
        DATASET, "LR-12", quote="### Licensing Information\nCC-BY-4.0",
        quote_url="https://huggingface.co/datasets/google-research-datasets/mbpp", verify_url=dc.hf_card_url(HF, rev),
        licence_class="CC-BY-4.0", provenance="human",
        notes="Card of the Google Research org page (YAML 'license: cc-by-4.0' too). 'The dataset was created with an internal "
              "crowdsourcing effort at Google' (card). Solutions are human; mutants (for the will-this-test-fail form) come from OUR "
              "mutator with execution gold on the signed-off od-sbx1, never from a model.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
