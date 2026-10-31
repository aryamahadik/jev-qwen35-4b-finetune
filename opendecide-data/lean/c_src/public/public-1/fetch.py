#!/usr/bin/env python3
"""public-1 fetch: pinned downloads (train splits only) + G1 licence-record re-reads for C_DATA_SPEC v4 3.2 #1-5.

Writes raw/ (train files only; dev/test members are never extracted), licence_records/ (the fetched official records),
and logs/fetch_manifest.json (url, upstream commit, sha256, bytes, licence string checks). Stdlib + requests only.
Run from anywhere: python fetch.py [--only NAME ...]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import re
import sys
import tarfile
import time
import zipfile
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
LIC = HERE / "licence_records"
LOGS = HERE / "logs"
TMP = HERE / "tmp"
UA = {"User-Agent": "opendecide-public-1/1.0 (licence check; contact via repo owner)"}

# Upstream commits pinned on 3 Oct 2026 (GitHub API HEAD of the default branch; register section 1 prefixes agree).
COMMITS = {
    "musique": "922ac98f19a201998dbdae6d7f2887a5258dbdeb",
    "2wikimultihop": "13800e5be57df1b4040b9b1588c6c811779e69e9",
    "quality": "f84977c40dbfef70c9cab48037b7becfc8e45f73",
    "squad_explorer": "eee5fdbf62f8613a7812b03419e6b29617b74fd1",
}

# G1: the official record named in LICENCE_REGISTER.md section 1, re-read now; each must still state the licence.
RECORDS = {
    "squad2": {
        "url": "https://rajpurkar.github.io/SQuAD-explorer/",
        "must": [r"CC BY-SA 4\.0|creativecommons\.org/licenses/by-sa/4\.0"],
        "licence": "CC BY-SA 4.0",
    },
    "musique_license": {
        "url": f"https://raw.githubusercontent.com/StonyBrookNLP/musique/{COMMITS['musique']}/LICENSE",
        "must": [r"Attribution 4\.0 International"],
        "licence": "CC BY 4.0",
    },
    "musique_readme": {
        "url": f"https://raw.githubusercontent.com/StonyBrookNLP/musique/{COMMITS['musique']}/README.md",
        "must": [r"distributed under a \[CC BY 4\.0 License\]", r"dev_test_singlehop_questions_v1\.0\.json"],
        "licence": "CC BY 4.0",
    },
    "2wiki_license": {
        "url": f"https://raw.githubusercontent.com/Alab-NII/2wikimultihop/{COMMITS['2wikimultihop']}/LICENSE",
        "must": [r"Apache License", r"Version 2\.0"],
        "licence": "Apache-2.0",
    },
    "2wiki_readme": {
        "url": f"https://raw.githubusercontent.com/Alab-NII/2wikimultihop/{COMMITS['2wikimultihop']}/README.md",
        "must": [r"data_ids_april7\.zip"],
        "licence": "Apache-2.0 (repo-wide LICENSE; README links the data zip)",
    },
    "quality_page": {
        "url": "https://nyu-mll.github.io/quality/",
        "must": [r"CC BY 4\.0"],
        "licence": "CC BY 4.0",
    },
    "qasper_page_archived": {
        "url": "https://web.archive.org/web/20230414023335/https://allenai.org/data/qasper",
        "must": [r"CC BY"],
        "licence": "CC BY 4.0 (annotations)",
    },
    "oanc_terms": {
        "url": "https://anc.org/data/oanc/",
        "must": [r"without restriction"],
        "licence": "OANC: any use incl. commercial (QuALITY Slate articles)",
    },
}

DOWNLOADS = {
    "squad2": {
        "url": "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json",
        "keep": None,  # single file
        "out": "squad2/train-v2.0.json",
    },
    "musique": {
        "url": "https://drive.usercontent.google.com/download?id=1tGdADlNjWFaHLeZZGShh2IRcpO6Lv24h&export=download&confirm=t",
        "note": "official Google Drive file linked from StonyBrookNLP/musique README and download_data.sh",
        # train files + the dev/test single-hop id list (a DROP list the README asks users to apply); never dev/test
        "keep": [r"(^|/)musique_ans_v1\.0_train\.jsonl$", r"(^|/)musique_full_v1\.0_train\.jsonl$",
                 r"(^|/)dev_test_singlehop_questions_v1\.0\.json$"],
        "out": "musique/",
    },
    "2wiki": {
        "url": "https://www.dropbox.com/s/ms2m13252h6xubs/data_ids_april7.zip?dl=1",
        "note": "official Dropbox link in Alab-NII/2wikimultihop README (sentence-segmentation fix, april7)",
        "keep": [r"(^|/)train\.json$"],
        "out": "2wiki/",
    },
    "quality": {
        "url": f"https://raw.githubusercontent.com/nyu-mll/quality/{COMMITS['quality']}/data/v1.0.1/QuALITY.v1.0.1.htmlstripped.train",
        "keep": None,
        "out": "quality/QuALITY.v1.0.1.htmlstripped.train",
    },
    "qasper": {
        "url": "https://qasper-dataset.s3.us-west-2.amazonaws.com/qasper-train-dev-v0.3.tgz",
        "note": "official AI2 S3 archive (named on the archived AI2 Qasper page)",
        "keep": [r"(^|/)qasper-train-v0\.3\.json$"],
        "out": "qasper/",
    },
}


def log(msg: str) -> None:
    line = f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"
    print(line, flush=True)
    with open(LOGS / "fetch.log", "a") as f:
        f.write(line + "\n")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get(url: str, stream: bool = False, tries: int = 4) -> requests.Response:
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=120, stream=stream, allow_redirects=True)
            if r.status_code == 200:
                return r
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001
            last = repr(e)
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"GET failed {url}: {last}")


def read_records(manifest: dict) -> None:
    out = {}
    for name, rec in RECORDS.items():
        r = get(rec["url"])
        body = r.content
        p = LIC / f"{name}.html" if not rec["url"].endswith(("LICENSE", ".md")) else LIC / f"{name}.txt"
        p.write_bytes(body)
        text = body.decode("utf-8", "replace")
        checks = {pat: bool(re.search(pat, text)) for pat in rec["must"]}
        ok = all(checks.values())
        out[name] = {"url": rec["url"], "final_url": r.url, "sha256": sha256_bytes(body), "bytes": len(body),
                     "licence": rec["licence"], "checks": checks, "pass": ok,
                     "read_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        log(f"[record] {name} pass={ok} sha256={out[name]['sha256'][:16]}")
    manifest["licence_records"] = out


def download(name: str, spec: dict, manifest: dict) -> None:
    dest = RAW / spec["out"]
    tmpfile = TMP / f"dl_{name}.bin"
    log(f"[download] {name} start {spec['url'][:90]}")
    r = get(spec["url"], stream=True)
    h = hashlib.sha256()
    n = 0
    with open(tmpfile, "wb") as f:
        for chunk in r.iter_content(1 << 20):
            f.write(chunk)
            h.update(chunk)
            n += len(chunk)
    archive_sha = h.hexdigest()
    entry = {"url": spec["url"], "final_url": r.url, "archive_sha256": archive_sha, "archive_bytes": n,
             "note": spec.get("note"), "files": {}}
    if spec["keep"] is None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmpfile.replace(dest)
        entry["files"][str(dest.relative_to(HERE))] = {"sha256": archive_sha, "bytes": n}
    else:
        dest.mkdir(parents=True, exist_ok=True)
        pats = [re.compile(p) for p in spec["keep"]]
        skipped = 0
        if zipfile.is_zipfile(tmpfile):
            with zipfile.ZipFile(tmpfile) as z:
                for m in z.namelist():
                    if "__MACOSX" in m or m.endswith("/"):
                        continue
                    if any(p.search(m) for p in pats):
                        tgt = dest / Path(m).name
                        with z.open(m) as src, open(tgt, "wb") as o:
                            while True:
                                b = src.read(1 << 20)
                                if not b:
                                    break
                                o.write(b)
                        entry["files"][str(tgt.relative_to(HERE))] = {"member": m, "sha256": sha256_file(tgt),
                                                                       "bytes": tgt.stat().st_size}
                    else:
                        skipped += 1
        else:
            with tarfile.open(tmpfile) as t:
                for m in t.getmembers():
                    if not m.isfile():
                        continue
                    if any(p.search(m.name) for p in pats):
                        tgt = dest / Path(m.name).name
                        with t.extractfile(m) as src, open(tgt, "wb") as o:
                            o.write(src.read())
                        entry["files"][str(tgt.relative_to(HERE))] = {"member": m.name, "sha256": sha256_file(tgt),
                                                                       "bytes": tgt.stat().st_size}
                    else:
                        skipped += 1
        entry["members_not_extracted"] = skipped
        tmpfile.unlink()
    manifest["downloads"][name] = entry
    log(f"[download] {name} done bytes={n} sha256={archive_sha[:16]} files={list(entry['files'])}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-records", action="store_true")
    a = ap.parse_args()
    for d in (RAW, LIC, LOGS, TMP):
        d.mkdir(parents=True, exist_ok=True)
    mpath = LOGS / "fetch_manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {"downloads": {}}
    manifest["commits"] = COMMITS
    if not a.no_records:
        read_records(manifest)
        mpath.write_text(json.dumps(manifest, indent=1))
    for name, spec in DOWNLOADS.items():
        if a.only and name not in a.only:
            continue
        download(name, spec, manifest)
        mpath.write_text(json.dumps(manifest, indent=1))
    log("[fetch] all done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
