"""LR-13 HWU64 from the UPSTREAM repo xliuhw/NLU-Evaluation-Data (not a mirror).
Split definition: the only fixed train/test partition the upstream release ships is the generated 10-fold cross-validation
(CrossValidation/autoGeneFromRealAnno/.../KFold_1). train/ <- KFold_1/trainset/*.csv (one file per scenario_intent);
quarantine <- KFold_1/testset/csv/*.csv (the test fold, a G13 target). The other nine folds are not fetched (their test
parts overlap this train). OPEN POINT for Opus (batch-2 table): the plan's '8,954 train (mirror count)' is the DialoGLUE
partition, which upstream does not ship; any published HWU64 test is caught row by row by the G13 stamp.
Source: https://github.com/xliuhw/NLU-Evaluation-Data
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "hwu64"
REPO = "xliuhw/NLU-Evaluation-Data"
FOLD = "CrossValidation/autoGeneFromRealAnno/autoGene_2018_03_22-13_01_25_169/CrossValidation/KFold_1"


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "master")
    st.log["upstream_commit"] = sha
    tree = dc.gh_tree(REPO, sha)
    tr = sorted(p for p, _ in tree if p.startswith(FOLD + "/trainset/") and p.endswith(".csv"))
    te = sorted(p for p, _ in tree if p.startswith(FOLD + "/testset/csv/") and p.endswith(".csv"))
    for p in tr:
        url = dc.raw_url(REPO, sha, p)
        rel = "KFold_1_trainset/" + os.path.basename(p)
        dc.fetch_to(url, st.train_path(rel))
        st.add_train_file(rel, source_urls=[url])
    for p in te:
        url = dc.raw_url(REPO, sha, p)
        rel = "KFold_1_testset_csv/" + os.path.basename(p)
        dc.fetch_to(url, st.quar_path(rel))
        st.add_quar_file(rel, role="test_fold_KFold_1", source_urls=[url])
    import csv, glob
    def keys(root, pat):
        ids, texts = [], []
        for f in glob.glob(os.path.join(root, pat)):
            with open(f, "r", encoding="utf-8", newline="") as fh:
                for row in csv.DictReader(fh, delimiter=";", quotechar='"'):
                    ids.append(row.get("answerid"))
                    texts.append(row.get("answer_from_user") or "")
        return ids, texts
    tr_ids, tr_txt = keys(st.train_dir, "KFold_1_trainset/*.csv")
    te_ids, te_txt = keys(st.quar_dir, "KFold_1_testset_csv/*.csv")
    dc.record_overlap(st, "answerid_train_vs_test_fold", tr_ids, te_ids)
    dc.record_overlap(st, "utterance_text_train_vs_test_fold", tr_txt, te_txt)
    lic = dc.licence_record(
        DATASET, "LR-13",
        quote="All data are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0)",
        quote_url="https://github.com/xliuhw/NLU-Evaluation-Data",
        verify_url="https://raw.githubusercontent.com/%s/%s/README.md" % (REPO, sha),
        licence_class="CC-BY-4.0", provenance="human", tier="A",
        notes="MTurk workers typed answers to written prompts (arXiv 1903.05566). Upstream release, not the DeepPavlov mirror.")
    st.write_licence(lic)
    return st.finish({"counts": {"train_files": len(tr), "test_fold_files": len(te), "train_utterances": len(tr_ids), "test_fold_utterances": len(te_ids)}})


if __name__ == "__main__":
    print(dc.summarize(run()))
