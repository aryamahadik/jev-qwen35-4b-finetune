"""Pull exact licence / label-method lines (with line numbers) from the saved official records. Prints JSON.
Usage: python3 -I g1_quotes.py <SB6/src dir>"""
import hashlib, json, re, sys
from pathlib import Path

src = Path(sys.argv[1])

def lines(p):
    return Path(p).read_text(encoding="utf-8", errors="replace").splitlines()

def find(p, pat, flags=re.I, ctx=0):
    out = []
    ls = lines(p)
    for i, l in enumerate(ls, 1):
        if re.search(pat, l, flags):
            out.append({"line": i, "text": l.strip()})
    return out

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

res = {}
lic = src / "g1_official/LICENSE"
res["LICENSE_head"] = [{"line": i, "text": l.strip()} for i, l in enumerate(lines(lic)[:5], 1) if l.strip()]
res["LICENSE_grant"] = find(lic, r"hereby grants to You a perpetual")
ls = lines(lic)
# the grant sentence wraps over 3 lines: join them
g = [i for i, l in enumerate(ls) if "hereby grants to You a perpetual" in l]
if g:
    i = g[0]
    res["LICENSE_grant_joined"] = {"lines": f"{i+1}-{i+3}", "text": " ".join(x.strip() for x in ls[i:i+3])}
res["LICENSE_appendix"] = find(lic, r"Licensed under the Apache License|you may not use this file except in compliance")
res["LICENSE_commercial_terms"] = find(lic, r"commercial|non-commercial|NonCommercial")
res["README_licence_lines"] = find(src / "g1_official/README.md", r"licen|apache|copyright|creative commons|cc[- ]by|terms of use|permission")
res["README_source_data"] = find(src / "g1_official/README.md", r"drawn from single coherent snapshots|without the use of translation|written by people who want")
res["README_data_urls"] = find(src / "g1_official/README.md", r"tydiqa-v1\.0-(dev|train)\.jsonl\.gz\]")
res["paper_label_method"] = find(src / "g1_paper/tacl_2020_30.txt", r"asking for a$|^or NO\. If no such minimal|annotator selects either YES|trained linguists|Trained linguists|both\s*$|YES and NO were deemed")
res["paper_boolean_lines"] = find(src / "g1_paper/tacl_2020_30.txt", r"Boolean answer, the annotator|YES and NO were deemed|3-way annotated|single.?annotated|Distributed under a CC-BY")
res["wiki_tou_2018_rev116456"] = find(src / "g1_wikimedia_2019/terms_of_use_rev116456.txt", r"Creative Commons Attribution-ShareAlike 3\.0|GNU Free Documentation License|do allow commercial uses")
res["wiki_tou_current"] = find(src / "g1_wikipedia/terms_of_use.txt", r"Creative Commons Attribution-ShareAlike 4\.0 International License\] \(|do allow commercial uses")
res["enwiki_copyrights_current"] = find(src / "g1_wikipedia/enwiki_copyrights.txt", r"Permission is granted")
print(json.dumps(res, ensure_ascii=False, indent=1))
