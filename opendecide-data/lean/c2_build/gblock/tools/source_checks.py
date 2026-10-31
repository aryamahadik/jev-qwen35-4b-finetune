"""Source-level and text-level checks for the G-block texts (A39 b). Prints counts only.

1. C1 overlap: each final source's name / host keys vs the names-only C1 source list (checks/c1_source_names.json).
2. OHS-4 sealed keyword hashes (sealed_hashes/keyword_hashes.jsonl) vs source names / hosts (tools/kwcheck.py rule).
3. OHS-4 sealed text hashes (hash-level self-check, FORMAT.md): word 10-/12-grams, full-text and sentence hashes of
   every text. Any hit drops that text (ids written to checks/sealed_text_hash_hits.json); a source with a hit rate above
   1% is flagged as a likely OHS-4 source.
The full G13 decontamination (c2_build/g13_c2.py + the sealed-side checker) still runs later on the built rows.
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np

G = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock")
SH = G.parent / "sealed_hashes"
_W = re.compile(r"[^\W_]+")
_SEG = re.compile(r"(?<=[.!?])\s+|\n+")


def words(t):
    return _W.findall(unicodedata.normalize("NFKC", t).lower())


def norm(t):
    return " ".join(words(t))


def sha_hex(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def c1_overlap(final):
    names = json.load(open(G / "checks" / "c1_source_names.json"))["names"]
    blob = " | ".join(names).lower()
    blob_n = re.sub(r"[^a-z0-9]+", "", blob)
    out = {}
    for k, v in final.items():
        keys = set(v.get("c1_keys", []))
        hits = sorted(x for x in keys if x.lower() in blob or re.sub(r"[^a-z0-9]+", "", x.lower()) in blob_n)
        out[k] = hits
    return out


def text_hash_check(drop=True):
    n10 = {bytes(r) for r in np.load(SH / "ngrams10_sha256.npy")}
    n12 = {bytes(r) for r in np.load(SH / "ngrams12_sha256.npy")}
    th = {}
    for line in open(SH / "text_hashes.jsonl"):
        r = json.loads(line)
        th.setdefault(r["kind"], set()).add(r["hash"])
    res, hit_ids = {}, {}
    for d in sorted(p for p in (G / "texts").iterdir() if p.is_dir()):
        f = d / "texts.jsonl"
        if not f.exists():
            continue
        rows = [json.loads(l) for l in open(f) if l.strip()]
        c = {"texts": len(rows), "ngram10": 0, "ngram12": 0, "full_text": 0, "sentence": 0, "any": 0}
        bad = []
        for r in rows:
            t = r["text"]
            ws = words(t)
            h10 = any(hashlib.sha256(" ".join(ws[i:i + 10]).encode()).digest() in n10 for i in range(len(ws) - 9))
            h12 = any(hashlib.sha256(" ".join(ws[i:i + 12]).encode()).digest() in n12 for i in range(len(ws) - 11))
            hf = sha_hex(norm(t)) in th.get("full_text_norm", set()) or sha_hex(t) in th.get("full_text_raw", set())
            hs = any(len(words(p)) >= 5 and sha_hex(norm(p)) in th.get("sentence_norm_min5words", set())
                     for p in _SEG.split(t))
            c["ngram10"] += h10
            c["ngram12"] += h12
            c["full_text"] += hf
            c["sentence"] += hs
            if h10 or h12 or hf or hs:
                c["any"] += 1
                bad.append(r["text_id"])
        c["hit_rate"] = round(c["any"] / max(1, c["texts"]), 4)
        c["likely_ohs4_source"] = max(c["ngram10"], c["ngram12"]) / max(1, c["texts"]) > 0.01
        res[d.name] = c
        hit_ids[d.name] = bad
        if drop and bad:
            keep = [r for r in rows if r["text_id"] not in set(bad)]
            with open(f, "w") as fo:
                for r in keep:
                    fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    (G / "checks" / "sealed_text_hash_hits.json").write_text(json.dumps({"counts": res, "dropped_text_ids": hit_ids},
                                                                 indent=1))
    with open(G / "checks" / "sealed_text_hash_runs.jsonl", "a") as fa:      # every run, append-only
        fa.write(json.dumps({"drop": drop, "counts": res, "hit_ids": hit_ids}) + "\n")
    return res


if __name__ == "__main__":
    final = json.load(open(G / "checks" / "final_sources.json"))
    if "c1" in sys.argv:
        print(json.dumps(c1_overlap(final), indent=1))
    if "texts" in sys.argv:
        print(json.dumps(text_hash_check(drop="--no-drop" not in sys.argv), indent=1))
