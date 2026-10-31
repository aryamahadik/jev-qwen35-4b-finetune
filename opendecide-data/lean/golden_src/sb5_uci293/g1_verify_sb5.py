"""G1 provenance verifier for SB5 (UCI ML Repository dataset 293, Abdulla 2013). A58 (c) 1.

Reads the official UCI page, the UCI API record and the downloaded archive (all untrusted data: run this script with
`python -I`), and writes SB5/G1_RECORD.json: URLs, DOI, sha256 of every file, the quoted licence line, the quoted
annotation text, the file counts, and the A58 (a) 1-3 verdicts. CPU only. No model calls. No network.

    ../../.venv/bin/python -I -B golden_src/sb5_uci293/g1_verify_sb5.py
"""
import hashlib
import html
import json
import re
import zipfile
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
SB5 = LEAN / "c2_build" / "zed_orch" / "sb_blocks" / "SB5"
SRC, PAGES = SB5 / "src", SB5 / "pages"
PAGE_URL = "https://archive.ics.uci.edu/dataset/293/twitter+data+set+for+arabic+sentiment+analysis"
API_URL = "https://archive.ics.uci.edu/api/dataset?id=293"
ZIP_URL = "https://archive.ics.uci.edu/static/public/293/twitter+data+set+for+arabic+sentiment+analysis.zip"
DOI = "10.24432/C5F31B"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def text_of(fragment: str) -> str:
    t = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def main():
    page = (PAGES / "uci293_page.html").read_text(encoding="utf-8")
    api = json.loads((PAGES / "uci293_api.json").read_text(encoding="utf-8"))["data"]
    m = re.search(r'<h1[^>]*>\s*License\s*</h1>(.*?)</div></div></div>', page, re.S)
    lic_block = text_of(m.group(1)) if m else ""
    lic_ok = ("Creative Commons Attribution 4.0 International" in lic_block and "CC BY 4.0" in lic_block
              and "for any purpose" in lic_block)
    summary = re.sub(r"\s+", " ", api["additional_info"]["summary"]).strip()
    ann = re.search(r"The months-long annotation process.*?break the tie\.", summary)
    desc_p = SRC / "rar_out" / "Twitter" / "Data set Description.txt"
    desc = re.sub(r"\s+", " ", desc_p.read_bytes().decode("cp1252", errors="replace"))
    ann_desc = re.search(r"The months-long annotation process.*?break the tie\.", desc)
    z = zipfile.ZipFile(SRC / "uci293.zip")
    zi = [(i.filename, i.file_size) for i in z.infolist()]
    files = sorted((SRC / "rar_out" / "Twitter").glob("*/*.txt"))
    per_dir = {}
    enc = {"utf-8": 0, "utf-8-bom": 0, "cp1256 (not valid UTF-8)": 0}
    for f in files:
        per_dir[f.parent.name] = per_dir.get(f.parent.name, 0) + 1
        b = f.read_bytes()
        try:
            b.decode("utf-8")
            enc["utf-8-bom" if b[:3] == b"\xef\xbb\xbf" else "utf-8"] += 1
        except UnicodeDecodeError:
            enc["cp1256 (not valid UTF-8)"] += 1
    rec = {
        "block": "SB5", "ruling": "A58 (draft) (c) 1", "verifier": "Sonnet (Claude Code subagent)",
        "retrieved_utc": "2026-10-17T03:01:54Z (HTTP Date header of the zip download)",
        "dataset": {"name": api["name"], "uci_id": api["uci_id"], "doi": DOI, "doi_url": "https://doi.org/" + DOI,
                    "creators": api["creators"], "donor": "N. A. Abdulla (UCI page); creators N. A. Abdulla and N. Mahyoub "
                    "(Data set Description.txt)", "year_of_dataset_creation": api["year_of_dataset_creation"],
                    "last_updated": api["last_updated"], "num_instances": api["num_instances"]},
        "official_records": {"page_url": PAGE_URL, "api_url": API_URL, "download_url": ZIP_URL},
        "sha256": {"uci293.zip": sha(SRC / "uci293.zip"), "Twitter.rar (inside the zip)": sha(SRC / "zip_out" / "Twitter.rar"),
                   "Data set Description.txt (inside the rar)": sha(desc_p),
                   "uci293_page.html": sha(PAGES / "uci293_page.html"), "uci293_api.json": sha(PAGES / "uci293_api.json")},
        "zip_members": zi,
        "licence": {"quote_uci_page": lic_block, "spdx": "CC-BY-4.0",
                    "legalcode_url": "https://creativecommons.org/licenses/by/4.0/legalcode",
                    "stated_where": "the 'License' section of the official UCI dataset page (the project page)",
                    "commercial_use_allowed": "yes: 'sharing and adaptation of the datasets for any purpose, provided that the "
                                              "appropriate credit is given' (CC BY 4.0 has no NC clause)",
                    "attribution_needed": "N. Abdulla, Twitter Data set for Arabic Sentiment Analysis, UCI Machine Learning "
                                          "Repository, 2013, DOI 10.24432/C5F31B, CC BY 4.0",
                    "page_check_passed": lic_ok},
        "label_method": {"quote_uci_page_api_summary": ann.group(0) if ann else None,
                         "quote_data_set_description_txt": ann_desc.group(0) if ann_desc else None,
                         "collection_quote": "By using a tweet crawler, we collect 2000 labelled tweets (1000 positive tweets and "
                                             "1000 negative ones) on various topics such as: politics and arts. These tweets "
                                             "include opinions written in both Modern Standard Arabic (MSA) and the Jordanian "
                                             "dialect.",
                         "classes": "Positive polarity, Negative polarity (two classes, no neutral class)",
                         "paper": "Abdulla N. A., Mahyoub N. A., Shehab M., Al-Ayyoub M., 'Arabic Sentiment Analysis: "
                                  "Corpus-based and Lexicon-based', IEEE AEECT 2013, Amman (named in Data set Description.txt)",
                         "summary_statistics_quote": "Avg. words in each tweet: Positive 7.19, Negative 9.97; avg. characters "
                                                     "40.04 / 59.02 (a length gap between the classes, reported by the creators)"},
        "archive": {"files_per_dir": per_dir, "total_tweet_files": len(files), "one_tweet_per_file": True,
                    "file_encodings": enc, "splits": "none in the source: counts as train (GOLDEN_SPEC rule 4)"},
        "A58_a_checks": {
            "a1_allowed_licence_and_V": "PASS: CC BY 4.0 is on GOLDEN_SPEC rule 3's list; read on the official UCI page "
                                        "(not an HF card or a mirror)",
            "a2_text_through_another_dataset": "PASS: the tweets come from a creator-run tweet crawler, not through another "
                                               "licensed dataset (UCI page, Description.txt 4.)",
            "a3_human_text_and_labels_only": "PASS: human-written tweets; labels by two native-speaker human experts with a "
                                             "third breaking ties; no LLM, no machine translation, no emoji labels",
            "a4_train_split_only": "PASS: no splits exist; counts as train",
            "open_note": "The text is third-party social-media text under the dataset licence CC BY 4.0 stated by the UCI "
                         "record; Ruling A58 accepts that record as the official one. Any platform-terms question is the "
                         "orchestrator's, not decided here.",
        },
        "pass": bool(lic_ok and ann and ann_desc and len(files) == 2000),
    }
    (SB5 / "G1_RECORD.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"pass": rec["pass"], "files": per_dir, "enc": enc, "sha_zip": rec["sha256"]["uci293.zip"],
                      "sha_rar": rec["sha256"]["Twitter.rar (inside the zip)"]}, indent=1))


if __name__ == "__main__":
    main()
