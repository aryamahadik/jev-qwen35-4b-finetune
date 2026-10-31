"""Licence / metadata evidence for the tier-C sets that FAIL their check (no data is downloaded for any of them): page shas, quoted
lines, fetch times, and the size of what a download WOULD be (from the host's file listing). Writes
c2_build/zed_orch/c21/l0/LR_TIER_C_DENY_EVIDENCE.json. Run: python3 -I deny_evidence.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import download_common as dc  # noqa: E402
import requests  # noqa: E402

OUT = os.path.join(dc.BUILD_DIR, "zed_orch", "c21", "l0", "LR_TIER_C_DENY_EVIDENCE.json")


def rec(dataset, quote, url, verify=None, cls="", notes=""):
    r = dc.licence_record(dataset, None, quote=quote, quote_url=url, verify_url=verify or url, licence_class=cls, provenance="human",
                          tier="C", notes=notes)
    return {k: r.get(k) for k in ("quoted_line", "quote_url", "verified_via_url", "licence_class", "fetched_utc", "page_sha256", "quote_found", "notes", "fetch_error")}


def zenodo(rid):
    d = requests.get("https://zenodo.org/api/records/%s" % rid, timeout=60, headers={"User-Agent": dc.UA}).json()
    return {"record": rid, "title": d["metadata"].get("title"), "licence": (d["metadata"].get("license") or {}).get("id"),
            "version": d["metadata"].get("version"), "publication_date": d["metadata"].get("publication_date"),
            "files": [{"key": f["key"], "bytes": f["size"], "checksum": f.get("checksum")} for f in d.get("files", [])]}


def main():
    qasc_commit = dc.gh_commit_sha("allenai/qasc", "HEAD")
    out = {"generated_utc": dc.utc_now(), "note": "evidence only; nothing was downloaded for these sets", "sets": {}}
    out["sets"]["qasc"] = {
        "inventory_id": "C5", "check": "CK-12 and WorldTree seed-fact terms are not NC; if NC, DENY",
        "evidence": [
            rec("qasc", "We release the data under [CC BY](https://creativecommons.org/licenses/by/4.0/) license.",
                "https://github.com/allenai/qasc", dc.raw_url("allenai/qasc", qasc_commit, "README.md"), "CC BY (authors' statement)"),
            rec("qasc", "a total of 928 facts: 356 facts from WorldTree, 123 from our middle-school extension, and 449 from CK-12",
                "https://arxiv.org/abs/1910.11473", "https://ar5iv.labs.arxiv.org/html/1910.11473", "paper section 3 (seed facts)"),
            rec("qasc", "all CK-12 Content (including CK-12 Curriculum Material) is made available to users in accordance with the Creative Commons Attribution-Noncommercial 3.0 Unported (CC BY-NC) License",
                "https://opensource.com/education/16/1/ck-12-open-education-resources", cls="CC BY-NC 3.0 (CK-12 terms as quoted by opensource.com; ck12.org itself returns HTTP 403 to bots)"),
            rec("qasc", "Content is offered under the CK-12 Curriculum Materials License", "https://en.wikipedia.org/wiki/CK-12_Foundation",
                cls="CK-12 Curriculum Materials License (custom, not on the allow-list); same page: 'they later switched to a Creative Commons Non Commercial licence'"),
        ],
        "verdict": "DENY: 449 of the 928 seed facts (48%) are CK-12 Foundation content, whose terms are CC BY-NC 3.0 / the custom CK-12 Curriculum Materials License; the QASC authors' CC BY statement cannot relicense it."}
    out["sets"]["new_yorker_caption_contest"] = {
        "inventory_id": "C15", "check": "caption text rights statement found; O1 = YES (also B2); A82 4 contest-statement bar",
        "evidence": [rec("new_yorker", "License: cc-by-4.0", "https://huggingface.co/datasets/jmhessel/newyorker_caption_contest",
                         cls="cc-by-4.0 (HF card tag)")],
        "would_download_bytes_all_files": 7905522856,
        "verdict": "DENY: split_aware_check v2.1 A82_EXCLUDED (A82 4: contest statements; G0-lite section 5 EXCLUDED list names the New Yorker caption-contest text). A card tag is not a text-rights statement either."}
    out["sets"]["fld"] = {
        "inventory_id": "C6", "check": "read the corpus LICENSE file",
        "evidence": [rec("fld", "Attribution 4.0 International", "https://github.com/hitachi-nlp/FLD-corpus/blob/NeurIPS_2024/LICENSE",
                         "https://raw.githubusercontent.com/hitachi-nlp/FLD-corpus/a14103509a0843f99a1ceb1ae46869615039fd00/LICENSE", "CC-BY-4.0 (LICENSE file text)")],
        "would_download": {"host": "huggingface.co/datasets/hitachi-nlp/FLD.v2 (the GitHub repo holds no data files; its README points to the HF corpora)",
                           "files": "data/train (38.3 MB), star/train (47.3 MB); test and validation files (about 28 MB) would go to quarantine; total about 114 MB",
                           "note": "the FLD.v2 HF card states no licence; the licence comes from the GitHub release repo"},
        "verdict": "LICENCE CHECK PASSES (LICENSE file = CC BY 4.0); split_aware_check v2.1 DENIES on LABELS_NOT_HUMAN (labels are program-made proof trees). CONFLICT with the inventory/G0-lite, which accept the 'program' provenance enum; needs an Opus ruling."}
    out["sets"]["flakeflagger"] = {
        "inventory_id": "C9", "check": "no Java source text until the 24 project licences are checked",
        "zenodo": zenodo("4450723"),
        "would_download": "labels and metrics only: test_results.csv (3.5 MB), test_features.csv (6.9 MB), Project_Info.csv (1.7 KB); the 24 project archives (34.4 GB) are never fetched",
        "verdict": "LICENCE OK (Zenodo record: cc-by-4.0); split_aware_check v2.1 DENIES on LABELS_NOT_HUMAN (labels are program-made: 10,000 reruns). Same conflict as FLD."}
    out["sets"]["manysstubs4j"] = {
        "inventory_id": "C10", "check": "per-repo permissive filter on any re-fetched code; A46 screen",
        "zenodo": zenodo("3653444"),
        "readme_quote_url": "https://zenodo.org/api/records/3653444/files/README.txt/content ('Please respect the license of each project.')",
        "would_download": "sstubs (26 MB) and sstubsLarge (173 MB); the rows carry 'patch', 'before', 'after' code text, so the per-repo licence filter is mandatory (about 1,100 repos)",
        "verdict": "LICENCE OK (cc-by-4.0 for the dataset); split_aware_check v2.1 DENIES on LABELS_NOT_HUMAN (SZZ + commit-message keywords = heuristic labels). Same conflict as FLD."}
    out["sets"]["tssb_3m"] = {
        "inventory_id": "C11", "check": "same as C10; keep only likely_bug rows",
        "zenodo": zenodo("10217373"),
        "would_download": "tssb_data_3M.zip (912 MB), or ctssb_data_1M.zip (266 MB, the cleaned variant); per-repo licences for the repos behind the kept rows (up to hundreds of thousands) would need a bulk GitHub lookup",
        "verdict": "LICENCE OK (cc-by-4.0 for the dataset); split_aware_check v2.1 DENIES on LABELS_NOT_HUMAN (heuristic likely_bug flag). Same conflict as FLD."}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("wrote", OUT)
    for k, v in out["sets"].items():
        print(k, [e.get("quote_found") for e in v.get("evidence", [])])


if __name__ == "__main__":
    main()
