"""LR-02 Gandalf summarization (Lakera). Train parquet only -> train/; validation + test parquet -> quarantine (G13 targets).
The ChatGPT `gandalf_answer` column is NEVER read by the mapper. Source: https://huggingface.co/datasets/Lakera/gandalf_summarization
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "gandalf_summarization"
REPO = "Lakera/gandalf_summarization"
FILES = {  # path -> role
    "data/train-00000-of-00001-44378fdb62cbf9b7.parquet": "train",
    "data/validation-00000-of-00001-c7b174a69fca3472.parquet": "validation",
    "data/test-00000-of-00001-1696577a5023b698.parquet": "test",
}


def run():
    import pyarrow.parquet as pq
    st = dc.Store(DATASET)
    rev = dc.hf_revision(REPO)
    st.log["upstream_revision"] = rev
    counts = {}
    texts = {}
    for path, role in FILES.items():
        url = dc.hf_url(REPO, rev, path)
        name = os.path.basename(path)
        if role == "train":
            info = dc.fetch_to(url, st.train_path(name))
            counts[role] = pq.ParquetFile(st.train_path(name)).metadata.num_rows
            st.add_train_file(name, source_urls=[url], rows=counts[role])
            texts[role] = pq.read_table(st.train_path(name), columns=["text"]).column("text").to_pylist()
        else:
            info = dc.fetch_to(url, st.quar_path(role + "/" + name))
            n = pq.ParquetFile(st.quar_path(role + "/" + name)).metadata.num_rows
            counts[role] = n
            st.add_quar_file(role + "/" + name, role=role, source_urls=[url], rows=n)
            texts[role] = pq.read_table(st.quar_path(role + "/" + name), columns=["text"]).column("text").to_pylist()
    for r in ("validation", "test"):
        dc.record_overlap(st, "text_train_vs_" + r, texts["train"], texts[r])
    lic = dc.licence_record(
        DATASET, "LR-02", quote="gandalf_summarization is distributed under the MIT License.",
        quote_url="https://huggingface.co/datasets/Lakera/gandalf_summarization", verify_url=dc.hf_card_url(REPO, rev),
        licence_class="MIT", provenance="human", tier="A",
        notes="Successful-guess prompts plus manual review (card). The ChatGPT answer column is never used.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
