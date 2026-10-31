"""LR-30 Qasper (allenai/qasper, CC BY 4.0). qasper-train-dev-v0.3.tgz holds train AND dev: staged in quarantine, split by PROGRAM;
qasper-train-v0.3.json -> train/, qasper-dev-v0.3.json -> quarantine. The test tarball (qasper-test-and-evaluator-v0.3.tgz) goes to
quarantine too (G13 target; never opened here). Source: https://huggingface.co/datasets/allenai/qasper
"""
import json
import os
import sys
import tarfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "qasper"
REPO = "allenai/qasper"
URL_TD = "https://qasper-dataset.s3.us-west-2.amazonaws.com/qasper-train-dev-v0.3.tgz"
URL_TEST = "https://qasper-dataset.s3.us-west-2.amazonaws.com/qasper-test-and-evaluator-v0.3.tgz"


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(REPO)
    st.log["upstream_revision"] = rev
    path, info = st.stage(URL_TD, "qasper-train-dev-v0.3.tgz")
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": URL_TD}
    counts = {}
    ids = {"train": [], "dev": []}
    with tarfile.open(path, "r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            b = os.path.basename(m.name)
            data = tf.extractfile(m).read()
            if b == "qasper-train-v0.3.json":
                dest = st.train_path(b)
                open(dest, "wb").write(data)
                n = len(json.loads(data))
                ids["train"] = list(json.loads(data))
                st.add_train_file(b, source_urls=[URL_TD], rows=n)
                counts["train_papers"] = n
            elif b == "qasper-dev-v0.3.json":
                dest = st.quar_path("dev/" + b)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                open(dest, "wb").write(data)
                st.add_quar_file("dev/" + b, role="dev", source_urls=[URL_TD], rows=len(json.loads(data)))
                ids["dev"] = list(json.loads(data))
    dc.record_overlap(st, "paper_id_train_vs_dev", ids["train"], ids["dev"])
    try:
        dest = st.quar_path("test/qasper-test-and-evaluator-v0.3.tgz")
        dc.fetch_to(URL_TEST, dest)
        st.add_quar_file("test/qasper-test-and-evaluator-v0.3.tgz", role="test", source_urls=[URL_TEST])
    except Exception as e:  # noqa: BLE001
        st.log["notes"].append("test tarball not fetched: %s" % str(e)[:200])
    st.clear_staging()
    lic = dc.licence_record(
        DATASET, "LR-30", quote="[CC BY 4.0](https://creativecommons.org/licenses/by/4.0)",
        quote_url="https://huggingface.co/datasets/allenai/qasper", verify_url=dc.hf_card_url(REPO, rev),
        licence_class="CC-BY-4.0", provenance="human", tier="A", quote_alternatives=["_LICENSE = \"CC BY 4.0\"", "CC BY 4.0"],
        notes="NLP practitioners wrote questions and answers; papers limited to CC-BY arXiv papers. No model text.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
