"""LR-47 CommonsenseQA, ORIGINAL release (S3 talmor dataset; not the Google-snippet variant, not a mirror).
train/ <- train_rand_split.jsonl; quarantine <- dev_rand_split.jsonl and test_rand_split_no_answers.jsonl (G13 targets).
Licence: the maintainer's statement in the repo issue tracker. Source: https://github.com/jonathanherzig/commonsenseqa
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "commonsenseqa"
BASE = "https://s3.amazonaws.com/commensenseqa/"
FILES = [("train_rand_split.jsonl", "train"), ("dev_rand_split.jsonl", "dev"), ("test_rand_split_no_answers.jsonl", "test")]


def run():
    st = dc.Store(DATASET)
    counts = {}
    keys = {}
    for fn, role in FILES:
        url = BASE + fn
        if role == "train":
            dc.fetch_to(url, st.train_path(fn))
            n = sum(1 for _ in open(st.train_path(fn), "r", encoding="utf-8"))
            st.add_train_file(fn, source_urls=[url], rows=n)
        else:
            dc.fetch_to(url, st.quar_path(role + "/" + fn))
            n = sum(1 for _ in open(st.quar_path(role + "/" + fn), "r", encoding="utf-8"))
            st.add_quar_file(role + "/" + fn, role=role, source_urls=[url], rows=n)
        counts[role] = n
        p = st.train_path(fn) if role == "train" else st.quar_path(role + "/" + fn)
        import json
        keys[role] = [json.loads(l)["id"] for l in open(p, "r", encoding="utf-8")]
        keys[role + "_q"] = [json.loads(l)["question"]["stem"] for l in open(p, "r", encoding="utf-8")]
    for r in ("dev", "test"):
        dc.record_overlap(st, "id_train_vs_" + r, keys["train"], keys[r])
        dc.record_overlap(st, "question_text_train_vs_" + r, keys["train_q"], keys[r + "_q"])
    lic = dc.licence_record(
        DATASET, "LR-47", quote="Our dataset is licensed under an MIT license.",
        quote_url="https://github.com/jonathanherzig/commonsenseqa/issues/5",
        verify_url="https://github.com/jonathanherzig/commonsenseqa/issues/5", licence_class="MIT (maintainer statement, issue #5)",
        provenance="human", tier="A",
        notes="Crowd-written questions; one ConceptNet distractor and one worker-written distractor per question. "
              "The licence is a maintainer statement in an issue (no LICENSE file); the HF mirror tau/commonsense_qa states 'mit'.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
