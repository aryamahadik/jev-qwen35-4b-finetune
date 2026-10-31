#!/usr/bin/env python3
"""A42-D 8.5 / 12.2 sealed-side source-name check, C2 side. Prints ONLY "<id> PASS" or "<id> HIT" per source.
Never prints which keyword or which hash matched. CPU only, no network.

For every source in SOURCES_CANDIDATES.json it hashes these identifiers with the keyword rule of g13_c2.keyword_hashes
(runs of 1-8 tokens, punctuation-stripped variants, URL hosts with and without a leading www.):
  name, publisher, host, every other host (each as bare text and as https://<host>/ and https://www.<host>/),
  upstream id, licence page URL (as text), dataset URL (as text; extra, not required by 8.5).
and compares the hash sets with
  ../sealed_hashes/keyword_hashes.jsonl                         (OHS-4 export, always)
  ../sealed_hashes_ac/keyword_hashes.jsonl                      (OHS-AC export, only if present)
  ../sealed_hashes_ac/source_keywords_prelim.jsonl              (OHS-AC preliminary source keywords, only if present;
        any 64-hex string value in a line is read as a sha256 keyword hash, whatever the key)
Usage (from lean/c2_build):  ../../.venv/bin/python -B meta_src/source_name_check.py [--file F] [--role g_proxy|metadata]
Exit code 0 always when files load; 2 if the OHS-4 export is missing.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(BUILD))
import g13_c2  # noqa: E402  (read-only import: keyword_hashes, sha_hex)

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load_hashes(path: Path) -> set:
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        vals = obj.values() if isinstance(obj, dict) else [obj]
        for v in vals:
            if isinstance(v, str) and HEX64.match(v):
                out.add(v)
    return out


def identifier_texts(src: dict) -> list:
    hosts = [src.get("host") or ""] + list(src.get("other_hosts") or [])
    texts = [src.get("name") or "", src.get("publisher") or "", src.get("upstream_id") or "",
             src.get("licence_url") or "", src.get("dataset_url") or ""]
    for h in hosts:
        if not h:
            continue
        bare = h[4:] if h.startswith("www.") else h
        texts += [h, bare, "www." + bare, f"https://{bare}/", f"https://www.{bare}/"]
    return [t for t in texts if t.strip()]


def source_hashes(src: dict) -> set:
    hs = set()
    for t in identifier_texts(src):
        hs |= g13_c2.keyword_hashes(t)
        hs.add(g13_c2.sha_hex(re.sub(r"\s+", " ", t.strip().lower())))     # whole identifier, any length
    return hs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(HERE / "SOURCES_CANDIDATES.json"))
    ap.add_argument("--role", default=None)
    ap.add_argument("--exports", default="all", choices=["ohs4", "all"], help="ohs4 = only the OHS-4 export; all = OHS-4 + OHS-AC files when present")
    a = ap.parse_args()
    sealed = [BUILD / "sealed_hashes" / "keyword_hashes.jsonl",
              BUILD / "sealed_hashes_ac" / "keyword_hashes.jsonl",
              BUILD / "sealed_hashes_ac" / "source_keywords_prelim.jsonl"]
    if not sealed[0].exists():
        print("OHS-4 export missing"); sys.exit(2)
    bad = set()
    for p in (sealed[:1] if a.exports == "ohs4" else sealed):
        if p.exists():
            bad |= load_hashes(p)
    srcs = json.loads(Path(a.file).read_text(encoding="utf-8"))["sources"]
    for s in srcs:
        if a.role and s["role"] != a.role:
            continue
        print(f"{s['id']} {'HIT' if source_hashes(s) & bad else 'PASS'}")


if __name__ == "__main__":
    main()
