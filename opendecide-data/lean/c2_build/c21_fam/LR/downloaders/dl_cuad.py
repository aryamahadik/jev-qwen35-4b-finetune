"""LR-23 CUAD v1 (Atticus Project). Tier C check C1: licence statement readable on a primary Atticus page.
GitHub TheAtticusProject/cuad data.zip holds CUADv1.json (ALL 510 contracts, train + test), train_separate_questions.json (train)
and test.json (test). The archive is staged in quarantine (program-only); train_separate_questions.json -> train/;
test.json -> quarantine/test/ (G13 target); CUADv1.json (train + test mixed) is deleted with the staging directory.
Licence evidence: the CUAD v1 datasheet shipped in the HF repo theatticusproject/cuad ('CUAD is licensed under the Creative
Commons Attribution 4.0 (CC BY 4.0) license ...') and the Atticus dataset page ('CC BY 4.0'). The GitHub code repo has NO licence file.
"""
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "cuad"
GH = "TheAtticusProject/cuad"
HF = "theatticusproject/cuad"
README_PATH = "CUAD_v1/CUAD v1 ReadMe _ Datasheet/CUAD_v1_README.txt"


def run():
    st = dc.Store(DATASET)
    ref = dc.gh_commit_sha(GH, "HEAD")
    st.log["upstream_commit"] = ref
    rev = dc.hf_revision(HF)
    st.log["hf_revision_for_licence_page"] = rev
    url = dc.raw_url(GH, ref, "data.zip")
    path, info = st.stage(url, "data.zip")
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url}
    counts, titles = {}, {"train": set(), "test": set()}
    with zipfile.ZipFile(path) as z:
        for name, role in (("train_separate_questions.json", "train"), ("test.json", "test")):
            data = z.read(name)
            obj = json.loads(data)
            titles[role] = {d["title"] for d in obj["data"]}
            counts[role + "_contracts"] = len(titles[role])
            counts[role + "_qas"] = sum(len(p["qas"]) for d in obj["data"] for p in d["paragraphs"])
            if role == "train":
                with open(st.train_path(name), "wb") as f:
                    f.write(data)
                st.add_train_file(name, source_urls=[url], rows=counts["train_contracts"])
            else:
                dest = st.quar_path("test/" + name)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(data)
                st.add_quar_file("test/" + name, role="test", source_urls=[url], rows=counts["test_contracts"])
    dc.record_overlap(st, "contract_title_train_vs_test", titles["train"], titles["test"])
    st.clear_staging()
    lic = tc.licence_with_checks(
        DATASET, "LR-23",
        quote="CUAD is licensed under the Creative Commons Attribution 4.0 (CC BY 4.0) license and free to the public for commercial and non-commercial use.",
        quote_url="https://huggingface.co/datasets/theatticusproject/cuad (CUAD v1 datasheet, LICENSE section)",
        verify_url=dc.hf_url(HF, rev, README_PATH), licence_class="CC-BY-4.0", provenance="human",
        notes="Contracts are public SEC EDGAR filings; the datasheet adds 'We make no representations or warranties regarding the license "
              "status of the underlying contracts, which are publicly available and downloadable from EDGAR.' Labels: law students, checked "
              "by lawyers. The GitHub repo has no licence file (check C1 reads the primary Atticus page instead).",
        also=[{"label": "Atticus Project dataset page", "quote": "CC BY 4.0", "url": "https://www.atticusprojectai.org/cuad"}])
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
