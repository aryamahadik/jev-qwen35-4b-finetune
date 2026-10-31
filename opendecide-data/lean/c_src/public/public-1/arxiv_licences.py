#!/usr/bin/env python3
"""Qasper per-paper text licence (C_DATA_SPEC v4 3.2 #5, register 1 #5): read each train paper's arXiv licence by
program from arXiv's OAI-PMH metadata (metadataPrefix=arXiv, <license> element), keyed by arXiv id. Absent <license>
= arXiv's default non-exclusive distribution licence (not CC). Resumable; polite rate (one request per 3 s, honours
503 Retry-After). Output: logs/qasper_arxiv_licences.json {arxiv_id: {"license_url", "class", "http", "utc"}}.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
OUT = HERE / "logs" / "qasper_arxiv_licences.json"
SRC = HERE / "raw" / "qasper" / "qasper-train-v0.3.json"
OAI = "https://oaipmh.arxiv.org/oai?verb=GetRecord&metadataPrefix=arXiv&identifier=oai:arXiv.org:{}"
OAI_OLD = "http://export.arxiv.org/oai2?verb=GetRecord&metadataPrefix=arXiv&identifier=oai:arXiv.org:{}"
UA = {"User-Agent": "opendecide-public-1/1.0 (per-paper licence check for a private training-data build)"}


def classify(url: str | None) -> str:
    if not url:
        return "arxiv_default_nonexclusive"
    u = url.lower()
    if "publicdomain/zero" in u:
        return "CC0"
    if "nonexclusive-distrib" in u:
        return "arxiv_default_nonexclusive"
    if "/by-nc" in u:
        return "CC BY-NC" + ("-SA" if "-sa" in u else "-ND" if "-nd" in u else "")
    if "/by-nd" in u:
        return "CC BY-ND"
    if "/by-sa" in u:
        return "CC BY-SA"
    if "/by/" in u:
        return "CC BY"
    return "other:" + url


def fetch(aid: str) -> tuple[int, str | None, str]:
    last = ""
    for base in (OAI, OAI_OLD):
        for attempt in range(5):
            try:
                r = requests.get(base.format(aid), headers=UA, timeout=60)
            except Exception as e:  # noqa: BLE001
                last = repr(e)
                time.sleep(10)
                continue
            if r.status_code == 503:
                time.sleep(int(r.headers.get("Retry-After", "10") or 10))
                continue
            if r.status_code != 200:
                last = f"HTTP {r.status_code}"
                break
            t = r.text
            if "idDoesNotExist" in t:
                return 404, None, base
            if "<arXiv" not in t and "<arXiv " not in t:
                last = "no arXiv metadata"
                break
            m = re.search(r"<license>\s*([^<]+?)\s*</license>", t)
            return 200, (m.group(1) if m else None), base
        time.sleep(3)
    return -1, last, ""


def main() -> int:
    papers = json.load(open(SRC))
    done = json.loads(OUT.read_text()) if OUT.exists() else {}
    todo = [k for k in papers if k not in done or done[k].get("http") != 200]
    print(f"{len(papers)} papers, {len(todo)} to read", flush=True)
    for i, aid in enumerate(todo):
        code, lic, base = fetch(aid)
        done[aid] = {"http": code, "license_url": lic if code == 200 else None,
                     "class": classify(lic) if code == 200 else "unread", "endpoint": base,
                     "utc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}
        if code != 200:
            done[aid]["error"] = lic
        if i % 25 == 0 or i == len(todo) - 1:
            OUT.write_text(json.dumps(done, indent=0, sort_keys=True))
            print(f"{i + 1}/{len(todo)} last={aid} {done[aid]['class']}", flush=True)
        time.sleep(3)
    OUT.write_text(json.dumps(done, indent=0, sort_keys=True))
    print("done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
