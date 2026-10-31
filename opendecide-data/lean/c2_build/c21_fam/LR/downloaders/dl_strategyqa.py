"""LR-52 StrategyQA, ORIGINAL release (Geva et al. 2021; NEVER the BIG-bench copy, guard F5). Tier C check C7: data licence on a
primary page. Evidence: (1) the dataset's own AI2 page (allenai.org/data/strategyqa, read from the Internet Archive because the live
URL now redirects to Semantic Scholar) says 'License : See Repo'; (2) the repo it points to, eladsegal/strategyqa, has a LICENSE
('MIT License / Copyright (c) 2021 Elad Segal') with no data carve-out. Files: the repo's data/strategyqa/train.json (the 90% UNOFFICIAL
train split of the official train set) -> train/; data/strategyqa/dev.json (the 10% unofficial dev; its questions are official-train
questions, so it is held out) -> quarantine/dev/; the official strategyqa_test.json (questions only) is taken from the official
zip, staged in quarantine, and kept in quarantine/test/. The official strategyqa_train*.json files are NOT used (they contain the
held-out dev questions). FIELD DROPS: description, evidence (Wikipedia-derived references); 'facts' and 'decomposition'
(crowd-written) are kept but the question-only mapper never reads them.
"""
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "strategyqa"
GH = "eladsegal/strategyqa"
URL_ZIP = "https://storage.googleapis.com/ai2i/strategyqa/data/strategyqa_dataset.zip"
DROP = ("description", "evidence")


def run():
    st = dc.Store(DATASET)
    ref = dc.gh_commit_sha(GH, "HEAD")
    st.log["upstream_commit"] = ref
    counts, q = {}, {}
    # train (unofficial 90%)
    url_t = dc.raw_url(GH, ref, "data/strategyqa/train.json")
    p, info = st.stage(url_t, "repo_train.json")
    rows = json.load(open(p, encoding="utf-8"))
    st.log["train_dropped_fields"] = list(DROP)
    kept = [{k: v for k, v in r.items() if k not in DROP} for r in rows]
    counts["train"] = len(kept)
    q["train"] = [r["question"] for r in kept]
    q["train_id"] = [r["qid"] for r in kept]
    st.log["upstream_train_json"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url_t}
    st.write_train_json("train.jsonl.gz", kept, source_urls=[url_t], jsonl=True)
    # dev (unofficial 10%, held out)
    url_d = dc.raw_url(GH, ref, "data/strategyqa/dev.json")
    dc.fetch_to(url_d, st.quar_path("dev/dev.json"))
    dv = json.load(open(st.quar_path("dev/dev.json"), encoding="utf-8"))
    counts["dev"] = len(dv)
    q["dev"] = [r["question"] for r in dv]
    q["dev_id"] = [r["qid"] for r in dv]
    st.add_quar_file("dev/dev.json", role="dev", source_urls=[url_d], rows=len(dv))
    # official test (questions only)
    zp, zi = st.stage(URL_ZIP, "strategyqa_dataset.zip")
    st.log["staged_file"] = {"sha256": zi["sha256"], "bytes": zi["bytes"], "url": URL_ZIP}
    with zipfile.ZipFile(zp) as z:
        data = z.read("strategyqa_test.json")
        dest = st.quar_path("test/strategyqa_test.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(data)
        tj = json.loads(data)
        counts["test"] = len(tj)
        q["test"] = [r["question"] for r in tj]
        q["test_id"] = [r["qid"] for r in tj]
        st.add_quar_file("test/strategyqa_test.json", role="test", source_urls=[URL_ZIP], rows=len(tj))
    for other in ("dev", "test"):
        dc.record_overlap(st, "qid_train_vs_" + other, q["train_id"], q[other + "_id"])
        dc.record_overlap(st, "question_text_train_vs_" + other, q["train"], q[other])
    st.clear_staging()
    lic = tc.licence_with_checks(
        DATASET, "LR-52", quote="MIT License\n\nCopyright (c) 2021 Elad Segal",
        quote_url="https://github.com/eladsegal/strategyqa/blob/%s/LICENSE" % ref, verify_url=dc.raw_url(GH, ref, "LICENSE"),
        licence_class="MIT (repo LICENSE; dataset page says 'License : See Repo')", provenance="human",
        notes="Check C7 (data licence on a primary page): the AI2 dataset page states 'License : See Repo' and the repo LICENSE is MIT, "
              "no data carve-out. MTurk workers wrote the questions; RoBERTa only rejected easy items (selection filter, not a "
              "labeller). Not the BIG-bench copy.",
        also=[{"label": "AI2 StrategyQA dataset page, Internet Archive capture of 2024-01-04",
               "quote": "License : See Repo",
               "url": "https://allenai.org/data/strategyqa",
               "verify_url": "https://web.archive.org/web/20240104112123/https://allenai.org/data/strategyqa"}])
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
