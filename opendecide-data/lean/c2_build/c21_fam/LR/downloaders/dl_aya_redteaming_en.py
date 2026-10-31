"""LR-01 Aya Red-teaming, ENGLISH rows only (A82 9). No split exists: seeded 10% hold-out by prompt id is frozen first.

train/  <- 90% of aya_eng.jsonl rows by seeded prompt-id hash;  quarantine <- the 10% hold-out (never trained, G13 target).
Non-English files are NOT fetched. Source: https://huggingface.co/datasets/CohereLabs/aya_redteaming
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "aya_redteaming_en"
REPO = "CohereLabs/aya_redteaming"


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(REPO)
    st.log["upstream_revision"] = rev
    url = dc.hf_url(REPO, rev, "aya_eng.jsonl")
    path, info = st.stage(url, "aya_eng.jsonl")
    train, hold = [], []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            # the prompt id: use the file's own id field when present, else the 0-based line index (stable per revision)
            uid = r.get("id", i)
            if str(r.get("language", "English")).lower() not in ("english", "eng", "en"):
                continue  # English only
            r["_src_line"] = i
            (hold if dc.holdout_unit("aya|%s" % uid) else train).append(r)
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url}
    st.write_train_json("aya_eng.train.jsonl", train, source_urls=[url], jsonl=True,
                        note="90%% of English rows by seeded prompt-id hash (seed %s, frac %s)" % (dc.HOLDOUT_SEED, dc.HOLDOUT_FRAC))
    st.write_quar_json("aya_eng.holdout10.jsonl", hold, role="own_frozen_holdout_10pct", source_urls=[url], jsonl=True)
    st.clear_staging()
    lic = dc.licence_record(
        DATASET, "LR-01", quote="License: apache-2.0", quote_url="https://huggingface.co/datasets/CohereLabs/aya_redteaming",
        verify_url=dc.hf_card_url(REPO, rev), licence_class="Apache-2.0", provenance="human", tier="A",
        quote_alternatives=["license: apache-2.0", "License: Apache 2.0"],
        notes="Paid native speakers (arXiv 2406.18682). English rows only. Benign twins are Claude-written by L-I (not here).")
    st.write_licence(lic)
    return st.finish({"counts": {"train_rows": len(train), "holdout_rows": len(hold)}})


if __name__ == "__main__":
    print(dc.summarize(run()))
