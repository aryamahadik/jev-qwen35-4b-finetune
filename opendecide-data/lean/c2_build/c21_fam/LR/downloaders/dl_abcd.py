"""LR-17 ABCD (asappresearch/abcd, MIT). data/abcd_v1.1.json.gz is ONE file holding train, dev and test: it is staged inside
the quarantine store, split by PROGRAM on the top-level key, train -> train/abcd_v1.1.train.json.gz, dev and test ->
quarantine. ontology.json (flows / subflows / actions; no splits) is copied to train/. data/utterances.json is NOT used
(it pools utterances of all splits). Source: https://github.com/asappresearch/abcd
"""
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "abcd"
REPO = "asappresearch/abcd"


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "master")
    st.log["upstream_commit"] = sha
    url = dc.raw_url(REPO, sha, "data/abcd_v1.1.json.gz")
    path, info = st.stage(url, "abcd_v1.1.json.gz")
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        d = json.load(f)
    counts = {k: len(v) for k, v in d.items()}
    tr_ids = [c["convo_id"] for c in d["train"]]
    for k in d:
        if k != "train":
            dc.record_overlap(st, "convo_id_train_vs_" + k, tr_ids, [c["convo_id"] for c in d[k]])
    st.write_train_json("abcd_v1.1.train.json.gz", d["train"], source_urls=[url], rows=len(d["train"]))
    for k in d:
        if k != "train":
            st.write_quar_json("abcd_v1.1.%s.json.gz" % k, d[k], role=k, source_urls=[url], rows=len(d[k]))
    del d
    ont = dc.raw_url(REPO, sha, "data/ontology.json")
    dc.fetch_to(ont, st.train_path("ontology.json"))
    st.add_train_file("ontology.json", source_urls=[ont])
    st.clear_staging()
    lic = dc.licence_record(
        DATASET, "LR-17", quote="MIT License", quote_url="https://github.com/asappresearch/abcd",
        verify_url="https://raw.githubusercontent.com/%s/%s/LICENSE" % (REPO, sha), licence_class="MIT", provenance="human",
        tier="A", quote_alternatives=["Copyright (c) 2021 ASAPP Research"],
        notes="MIT covers data by implication only (LICENSE is the code licence; README has no separate data licence). "
              "Human-human dialogues (MTurk customers, certified agents); flow labels program-derived.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
