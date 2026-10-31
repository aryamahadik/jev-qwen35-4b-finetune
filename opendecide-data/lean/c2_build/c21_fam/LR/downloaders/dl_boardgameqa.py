"""LR-54 BoardgameQA (Kazemi et al. 2023; programmatic, no LLM). HF mirror tasksource/Boardgame-QA (cc-by-4.0), the paper footnote
says 'License: CC BY' (ar5iv). train/ <- the train parquet; valid and test parquet -> quarantine. The mirror is used because the
original release is a Google Drive link. Source: https://huggingface.co/datasets/tasksource/Boardgame-QA
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "boardgameqa"
REPO = "tasksource/Boardgame-QA"
PAPER = "https://ar5iv.labs.arxiv.org/html/2306.07934"
FILES = {"data/train-00000-of-00001-d7aa2b268ef1ea08.parquet": "train", "data/valid-00000-of-00001-7675409874256e7d.parquet": "valid",
         "data/test-00000-of-00001-be86a421cd54a34b.parquet": "test"}


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
            dc.fetch_to(url, st.train_path(name))
            counts[role] = pq.ParquetFile(st.train_path(name)).metadata.num_rows
            st.add_train_file(name, source_urls=[url], rows=counts[role])
            texts[role] = pq.read_table(st.train_path(name), columns=["example"]).column("example").to_pylist()
        else:
            dc.fetch_to(url, st.quar_path(role + "/" + name))
            counts[role] = pq.ParquetFile(st.quar_path(role + "/" + name)).metadata.num_rows
            st.add_quar_file(role + "/" + name, role=role, source_urls=[url], rows=counts[role])
            texts[role] = pq.read_table(st.quar_path(role + "/" + name), columns=["example"]).column("example").to_pylist()
    for r in ("valid", "test"):
        dc.record_overlap(st, "example_text_train_vs_" + r, texts["train"], texts[r])
    lic = dc.licence_record(
        DATASET, "LR-54", quote="License: CC BY", quote_url=PAPER, verify_url=PAPER, licence_class="CC-BY-4.0",
        provenance="program", tier="A", quote_alternatives=["license: cc-by-4.0"],
        notes="Programmatic: backward story generation, manual templates, defeasible-reasoning solver; no LLM. "
              "Mirror card (tasksource/Boardgame-QA) states cc-by-4.0.")
    mirror = dc.licence_record(DATASET, "LR-54", quote="license: cc-by-4.0", quote_url="https://huggingface.co/datasets/" + REPO,
                               verify_url=dc.hf_card_url(REPO, rev), licence_class="CC-BY-4.0", provenance="program", tier="A")
    lic["mirror_card_check"] = {"quote_found": mirror["quote_found"], "page_sha256": mirror["page_sha256"], "fetched_utc": mirror["fetched_utc"]}
    lic["status"] = "OK" if (lic["quote_found"] or mirror["quote_found"]) else "QUOTE_NOT_VERIFIED"
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
