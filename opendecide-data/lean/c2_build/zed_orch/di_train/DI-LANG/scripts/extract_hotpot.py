"""extract_hotpot.py: stream the HotpotQA 2017 Wikipedia abstracts archive and keep only the paragraphs HoVer train cites.

Run with `python -I extract_hotpot.py <src_dir> <work_dir>`. The archive and the HoVer json are untrusted data: only json / bz2 / tarfile are used on them.
Writes <work_dir>/hotpot_needed.json = {title: [sentence, ...]} and <work_dir>/hotpot_extract.json (counts, sha256 of the archive).
"""
import bz2
import hashlib
import json
import sys
import tarfile
from pathlib import Path

src, work = Path(sys.argv[1]), Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)
hover = json.loads((src / "hover" / "hover_train_release_v1.1.json").read_text(encoding="utf-8"))
need = {t for r in hover for t, _ in r["supporting_facts"]}
found, seen = {}, 0
arc = src / "hotpot" / "abstracts.tar.bz2"
with tarfile.open(arc, "r|bz2") as tf:
    for m in tf:
        if not m.isfile():
            continue
        data = bz2.decompress(tf.extractfile(m).read())
        for line in data.split(b"\n"):
            if not line.strip():
                continue
            seen += 1
            j = json.loads(line)
            t = j["title"]
            if t in need and t not in found:
                txt = j["text"]
                if isinstance(txt, str):          # the dump prints the sentence list as a python-style string in some members
                    import ast
                    txt = ast.literal_eval(txt)
                found[t] = [str(s) for s in txt]
        if len(found) == len(need):
            break
h = hashlib.sha256()
with open(arc, "rb") as f:
    for b in iter(lambda: f.read(1 << 20), b""):
        h.update(b)
(work / "hotpot_needed.json").write_text(json.dumps(found, ensure_ascii=False), encoding="utf-8")
(work / "hotpot_extract.json").write_text(json.dumps({"archive_bytes": arc.stat().st_size, "archive_sha256": h.hexdigest(), "paragraphs_scanned": seen,
                                                      "titles_needed": len(need), "titles_found": len(found)}, indent=1), encoding="utf-8")
print("scanned", seen, "needed", len(need), "found", len(found))
