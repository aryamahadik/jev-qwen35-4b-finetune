"""write_licence_record.py: A61 (c) 1 G1 provenance record for DI-LANG (URL, pinned commit, file sha256, quoted licence line, label-method quote).
Run: python -I write_licence_record.py   (reads src/** as data, writes provenance/LICENCE_RECORD.json)"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def grep(p, needle, width=260):
    t = Path(p).read_text(encoding="utf-8", errors="ignore")
    import re
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t)
    i = t.find(needle)
    return t[max(0, i - 20): i + width] if i >= 0 else None


ex = json.loads((ROOT / "work" / "hotpot_extract.json").read_text())
HOVER_PIN, ISARC_PIN = "39b84697f196308f398a251a7aea9b82ae0f0562", "dfc708b53bde1bb571abfb5692f63231c2232195"
rec = {
    "block": "DI-LANG", "written_by": "Sonnet verifier (A61 c 1), 17 Oct 2026",
    "hover": {
        "pinned_commit": HOVER_PIN, "repo": "https://github.com/hover-nlp/hover",
        "file": {"url": f"https://raw.githubusercontent.com/hover-nlp/hover/{HOVER_PIN}/data/hover/hover_train_release_v1.1.json",
                 "sha256": sha(SRC / "hover" / "hover_train_release_v1.1.json"), "rows": 18171},
        "licence": "CC BY-SA 4.0", "licence_commercial_use": True, "licence_on_spec_rule_3_list": True,
        "licence_V_source": "official project page https://hover-nlp.github.io/ (sha256 %s)" % sha(SRC / "hover" / "project_page.html"),
        "licence_quote": grep(SRC / "hover" / "project_page.html", "HoVer is distributed under", 120),
        "repo_LICENSE": {"url": f"https://raw.githubusercontent.com/hover-nlp/hover/{HOVER_PIN}/LICENSE", "sha256": sha(SRC / "hover" / "LICENSE"),
                         "first_line": "MIT License (covers the repository code; the data licence is stated on the project page)"},
        "label_method_quote": ("paper arXiv:2011.03088 (sha256 %s): 'In the final stage, we ask crowd-workers to label the resulting claims.' / "
                               "'trained crowdworkers classify the original and mutated claims as either SUPPORTED, REFUTED or NOT ENOUGH INFO. We merge the "
                               "latter two labels into a single NOT-SUPPORTED class'" % sha(SRC / "hover" / "hover_paper.pdf")),
        "text_method_note": ("claims written by trained Appen crowd-workers; mutations by crowd-workers and by automatic word substitution; "
                             "the label is always a human judgement (no distant supervision, no LLM)"),
        "abstract_quote_arxiv": "classify whether the claim is Supported or Not-Supported by the facts (arxiv_abs.html sha256 %s)" % sha(SRC / "hover" / "arxiv_abs.html"),
    },
    "hotpotqa_wikipedia_abstracts": {
        "url": "https://nlp.stanford.edu/projects/hotpotqa/enwiki-20171001-pages-meta-current-withlinks-abstracts.tar.bz2",
        "bytes": ex["archive_bytes"], "sha256": ex["archive_sha256"], "md5_published": "01edf64cd120ecc03a2745352779514c",
        "md5_matches": True, "download_cap": "~2 GB free-download cap: 1,553,565,403 bytes (A61 b)",
        "licence": "CC BY-SA 4.0", "licence_V_source": "official page https://hotpotqa.github.io/wiki-readme.html (sha256 %s)" % sha(SRC / "hotpot" / "hotpotqa_index.html"),
        "licence_quote": grep(SRC / "hotpot" / "hotpotqa_index.html", "The archive can be downloaded", 330),
        "paragraphs_scanned": ex["paragraphs_scanned"], "titles_needed_by_hover_train": ex["titles_needed"], "titles_found": ex["titles_found"],
    },
    "isarcasmeval": {
        "pinned_commit": ISARC_PIN, "repo": "https://github.com/iabufarha/iSarcasmEval",
        "file": {"url": f"https://raw.githubusercontent.com/iabufarha/iSarcasmEval/{ISARC_PIN}/train/train.En.csv", "sha256": sha(SRC / "isarc" / "train.En.csv"), "rows": 3468},
        "licence": "MIT", "licence_commercial_use": True, "licence_on_spec_rule_3_list": True,
        "licence_V_source": "repo LICENSE at the pinned commit", "licence_file": {"url": f"https://raw.githubusercontent.com/iabufarha/iSarcasmEval/{ISARC_PIN}/LICENSE",
                                                                              "sha256": sha(SRC / "isarc" / "LICENSE")},
        "licence_quote": "MIT License / Copyright (c) 2022 Ibrahim Abu Farha / Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software",
        "readme": {"url": f"https://raw.githubusercontent.com/iabufarha/iSarcasmEval/{ISARC_PIN}/README.md", "sha256": sha(SRC / "isarc" / "README.md")},
        "label_method_quote": ("README: 'for each sarcastic text, we also ask its author to rephrase the text to convey the same intended message without using sarcasm' "
                               "and the shared-task abstract: 'the data for this task was provided and labelled by the authors of the texts themselves. Such an approach minimises "
                               "the downfalls of other methods to collect sarcasm data, which rely on distant supervision or third-party annotations'"),
        "scope": "English train only (train/train.En.csv); Arabic excluded (A58 e Arabic cap untouched); the test split is the DI-scored split and is never read here",
        "caveat": "the MIT LICENSE covers the repository; the repo README does not restate a separate data licence (A61 b admits the source 'MIT if V on the repo LICENSE')",
    },
    "deny_list": "orchestrator runs c_src/common/denylist.py check --fail-on-taint on the full provenance (A61 a 5); the draft records the taint scopes as DI split only",
    "c1_overlap_note": ("gblock/checks/c1_source_names.json lists gd_hotpotqa_yesno (HotpotQA distractor yes/no) and the sarcasm sources gd_csc_sarcasm / br_sarcasm_headlines: "
                        "different datasets from HoVer and iSarcasmEval; A61 b admitted both knowing the C1 list. HoVer's 2-hop claims derive from HotpotQA question-answer pairs "
                        "and its evidence is Wikipedia text; this is surfaced for the A61 (a) 6 / 2 ruling, not decided here."),
}
(ROOT / "provenance").mkdir(exist_ok=True)
(ROOT / "provenance" / "LICENCE_RECORD.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("written", sha(ROOT / "provenance" / "LICENCE_RECORD.json"))
