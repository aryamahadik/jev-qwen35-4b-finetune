"""LR-21 SciFact (allenai/scifact). data.tar.gz (S3 release 'latest') holds corpus.jsonl and claims_{train,dev,test}.jsonl: it is
staged in quarantine and split by PROGRAM. train/ <- claims_train.jsonl + corpus_train_cited.jsonl (only abstracts cited by
a TRAIN claim); dev and test claims -> quarantine. Licences: claims + evidence annotations CC BY 4.0; abstracts ODC-By 1.0
(E2 / LR-M2); code Apache-2.0. Source: https://github.com/allenai/scifact
"""
import json
import os
import sys
import tarfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "scifact"
REPO = "allenai/scifact"
URL = "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz"


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "master")
    st.log["upstream_commit"] = sha
    path, info = st.stage(URL, "data.tar.gz")
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": URL}
    members = {}
    with tarfile.open(path, "r:gz") as tf:
        for m in tf.getmembers():
            base = os.path.basename(m.name)
            if m.isfile() and base in ("corpus.jsonl", "claims_train.jsonl", "claims_dev.jsonl", "claims_test.jsonl"):
                members[base] = tf.extractfile(m).read().decode("utf-8")
    train_claims = [json.loads(l) for l in members["claims_train.jsonl"].splitlines() if l.strip()]
    cited = set()
    for c in train_claims:
        cited.update(int(x) for x in c.get("cited_doc_ids", []))
        cited.update(int(k) for k in c.get("evidence", {}))
    corpus = [json.loads(l) for l in members["corpus.jsonl"].splitlines() if l.strip()]
    sub = [d for d in corpus if int(d["doc_id"]) in cited]
    st.write_train_json("claims_train.jsonl", train_claims, source_urls=[URL], rows=len(train_claims), jsonl=True)
    st.write_train_json("corpus_train_cited.jsonl", sub, source_urls=[URL], rows=len(sub), jsonl=True,
                        note="abstracts cited by a TRAIN claim (of %d in corpus.jsonl)" % len(corpus))
    counts = {"train_claims": len(train_claims), "corpus_all": len(corpus), "corpus_train_cited": len(sub)}
    for sp in ("dev", "test"):
        rows = [json.loads(l) for l in members["claims_%s.jsonl" % sp].splitlines() if l.strip()]
        dc.record_overlap(st, "claim_id_train_vs_" + sp, [c["id"] for c in train_claims], [r["id"] for r in rows])
        dc.record_overlap(st, "claim_text_train_vs_" + sp, [c["claim"] for c in train_claims], [r["claim"] for r in rows])
        st.write_quar_json("claims_%s.jsonl" % sp, rows, role=sp, source_urls=[URL], jsonl=True, rows=len(rows))
        counts["%s_claims" % sp] = len(rows)
    st.clear_staging()
    lic_url = "https://raw.githubusercontent.com/%s/%s/LICENSE.md" % (REPO, sha)
    a = dc.licence_record(DATASET, "LR-21",
                          quote="All claims and evidence annotations -- in the files `claims_*.jsonl` -- are released under [CC BY 4.0]",
                          quote_url="https://github.com/allenai/scifact", verify_url=lic_url, licence_class="CC-BY-4.0 (claims)",
                          provenance="human", tier="A")
    b = dc.licence_record(DATASET, "LR-21",
                          quote="are part of the Semantic Scholar [S2ORC dataset](https://github.com/allenai/s2orc) and are licensed under [ODC-By 1.0]",
                          quote_url="https://github.com/allenai/scifact", verify_url=lic_url, licence_class="ODC-By-1.0 (abstracts)",
                          provenance="human", tier="A")
    main = dict(a)
    main["second_quote"] = {"quoted_line": b["quoted_line"], "quote_found": b["quote_found"], "licence_class": b["licence_class"]}
    main["licence_class"] = "CC-BY-4.0 (claims, evidence) + ODC-By-1.0 (abstracts) + Apache-2.0 (code)"
    main["status"] = "OK" if a["quote_found"] and b["quote_found"] else "QUOTE_NOT_VERIFIED"
    main["notes"] = "Expert-written claims; no LM text (arXiv 2004.14974). ODC-By 1.0 allowed by Opus b1 LR-M2."
    st.write_licence(main)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
