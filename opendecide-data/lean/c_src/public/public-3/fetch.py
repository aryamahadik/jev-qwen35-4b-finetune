#!/usr/bin/env python3
"""public-3 fetch: pinned downloads (train files only) + G1 licence-record re-reads for C_DATA_SPEC v4 3.2 #13-17.

Datasets: XED English (#13), MAMS ACSA + ATSA (#14), News Headlines Sarcasm v2 (#15), Gab Hate Corpus (#16), EDOS (#17).
Dedupe-only inputs (spec 3.2 #16-17 and 7.1: exact-text dedupe of GHC and EDOS rows vs HateXplain and Social Bias
Frames): HateXplain dataset.json and SBIC.v2.tgz. They are hashed in-process by build_records.py and never written as
text, printed or used as rows.

Writes raw/ (train files only; ghc_test.tsv, EDOS dev/test rows, MAMS val/test and XED fi/projected files are never
downloaded), licence_records/ (the fetched official records), and logs/fetch_manifest.json (url, upstream commit,
sha256, bytes, licence string checks). Stdlib + requests only.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
import time
import zipfile
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from guard import safe_out  # noqa: E402

RAW = HERE / "raw"
LIC = HERE / "licence_records"
LOGS = HERE / "logs"
TMP = HERE / "tmp"
UA = {"User-Agent": "opendecide-public-3/1.0 (licence check)"}

# Upstream commits pinned on 3 Oct 2026 (GitHub API HEAD of the default branch; equal to LICENCE_REGISTER section 1).
COMMITS = {
    "xed": "76666d251f147cf518071bef4f8415dab6b96115",
    "mams": "cddcdb0f423b3fdb2c76b70744737abed3a00d17",
    "edos": "b1f1fbcca9d42de0395432ada8fcfb5c35f68c77",
    "hatexplain": "01d742279dac941981f53806154481c0e15ee686",
}
GH = "https://raw.githubusercontent.com"

# G1: the official record named in LICENCE_REGISTER.md section 1, re-read now; each must still state the licence.
RECORDS = {
    "xed_readme": {
        "url": f"{GH}/Helsinki-NLP/XED/{COMMITS['xed']}/README.md",
        "must": [r"Creative Commons Attribution 4\.0 International License"],
        "licence": "CC BY 4.0 (README last line; the repo has no LICENSE file)",
    },
    "mams_license": {
        "url": f"{GH}/siat-nlp/MAMS-for-ABSA/{COMMITS['mams']}/LICENSE",
        "must": [r"Apache License", r"Version 2\.0"],
        "licence": "Apache-2.0",
    },
    "mams_readme": {
        "url": f"{GH}/siat-nlp/MAMS-for-ABSA/{COMMITS['mams']}/README.md",
        "must": [r"data"],
        "licence": "Apache-2.0 (README: the repo contains the data and code; data under data/)",
    },
    "sarcasm_kaggle_view": {
        "url": "https://www.kaggle.com/api/v1/datasets/view/rmisra/news-headlines-dataset-for-sarcasm-detection",
        "must": [r"Attribution 4\.0 International \(CC BY 4\.0\)", r"\"ownerName\": ?\"Rishabh Misra\"",
                 r"\"currentVersionNumber\": ?2"],
        "licence": "CC BY 4.0 (creator's Kaggle page: structured licence field; owner and creator Rishabh Misra; v2 of 3 Jul 2019)",
    },
    "ghc_osf_node": {
        "url": "https://api.osf.io/v2/nodes/edua3/?embed=license",
        "must": [r"CC-By Attribution 4\.0 International"],
        "licence": "CC BY 4.0 (OSF node licence)",
    },
    "ghc_osf_data_folder": {
        "url": "https://api.osf.io/v2/nodes/edua3/files/osfstorage/5e51af5435d22d00fa5f28e0/",
        "must": [r"ghc_train\.tsv", r"c82a27336560d3a6822a4cc3f92856481af5fd63aa2ce8d0ca644d440d351d43"],
        "licence": "OSF file listing (ghc_train.tsv sha256 as published by OSF)",
    },
    "edos_license": {
        "url": f"{GH}/rewire-online/edos/{COMMITS['edos']}/LICENSE",
        "must": [r"CC0 1\.0 Universal"],
        "licence": "CC0 1.0",
    },
    "edos_readme": {
        "url": f"{GH}/rewire-online/edos/{COMMITS['edos']}/README.md",
        "must": [r"sexism detection", r"Gab and Reddit"],
        "licence": "CC0 1.0 (README: SemEval 2023 Task 10 data from Gab and Reddit; the LICENSE file is the record)",
    },
}

DOWNLOADS = {
    "xed_annotated": {"url": f"{GH}/Helsinki-NLP/XED/{COMMITS['xed']}/AnnotatedData/en-annotated.tsv",
                      "out": "xed/en-annotated.tsv", "role": "rows"},
    "xed_neutral": {"url": f"{GH}/Helsinki-NLP/XED/{COMMITS['xed']}/AnnotatedData/neu_en.txt",
                    "out": "xed/neu_en.txt", "role": "rows"},
    "mams_acsa": {"url": f"{GH}/siat-nlp/MAMS-for-ABSA/{COMMITS['mams']}/data/MAMS-ACSA/raw/train.xml",
                  "out": "mams/acsa_train.xml", "role": "rows"},
    "mams_atsa": {"url": f"{GH}/siat-nlp/MAMS-for-ABSA/{COMMITS['mams']}/data/MAMS-ATSA/raw/train.xml",
                  "out": "mams/atsa_train.xml", "role": "rows"},
    "sarcasm_v2": {"url": "https://www.kaggle.com/api/v1/datasets/download/rmisra/news-headlines-dataset-for-sarcasm-detection?datasetVersionNumber=2",
                   "out": "sarcasm/", "keep": [r"(^|/)Sarcasm_Headlines_Dataset_v2\.json$"], "role": "rows",
                   "note": "creator's Kaggle dataset, version 2 (the only official v2 release); only the v2 file is extracted"},
    "ghc_train": {"url": "https://osf.io/download/x5pdg/", "out": "ghc/ghc_train.tsv", "role": "rows",
                  "expect_sha256": "c82a27336560d3a6822a4cc3f92856481af5fd63aa2ce8d0ca644d440d351d43",
                  "note": "OSF edua3 Data/ghc_train.tsv (ghc_test.tsv is never downloaded)"},
    "edos_labelled": {"url": f"{GH}/rewire-online/edos/{COMMITS['edos']}/data/edos_labelled_aggregated.csv",
                      "out": "edos/edos_labelled_aggregated.csv", "role": "rows",
                      "note": "split == train rows only are parsed; dev/test rows are dropped at parse time"},
    "hatexplain": {"url": f"{GH}/hate-alert/HateXplain/{COMMITS['hatexplain']}/Data/dataset.json",
                   "out": "dedupe/hatexplain_dataset.json", "role": "dedupe-only (hashed in-process)"},
    "sbic": {"url": "https://maartensap.com/social-bias-frames/SBIC.v2.tgz", "out": "dedupe/SBIC.v2.tgz",
             "role": "dedupe-only (hashed in-process)"},
}


def now() -> str:
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    line = f"{now()} {msg}"
    print(line, flush=True)
    with open(LOGS / "fetch.log", "a") as f:
        f.write(line + "\n")


def get(url: str, stream: bool = False, tries: int = 4) -> requests.Response:
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=180, stream=stream, allow_redirects=True)
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
        ext = ".json" if "api." in rec["url"] or "/api/" in rec["url"] else ".txt"
        p = safe_out(LIC / f"{name}{ext}")
        p.write_bytes(body)
        text = body.decode("utf-8", "replace")
        if ext == ".json":                      # canonical spacing for the regex checks
            try:
                text = json.dumps(json.loads(text), ensure_ascii=False)
            except Exception:  # noqa: BLE001
                pass
        checks = {pat: bool(re.search(pat, text)) for pat in rec["must"]}
        ok = all(checks.values())
        out[name] = {"url": rec["url"], "final_url": r.url, "sha256": hashlib.sha256(body).hexdigest(),
                     "bytes": len(body), "licence": rec["licence"], "checks": checks, "pass": ok, "read_utc": now()}
        log(f"[record] {name} pass={ok} sha256={out[name]['sha256'][:16]}")
    manifest["licence_records"] = out


def download(name: str, spec: dict, manifest: dict) -> None:
    dest = RAW / spec["out"]
    tmpfile = safe_out(TMP / f"dl_{name}.bin")
    log(f"[download] {name} start {spec['url'][:100]}")
    r = get(spec["url"], stream=True)
    h = hashlib.sha256()
    n = 0
    with open(tmpfile, "wb") as f:
        for chunk in r.iter_content(1 << 20):
            f.write(chunk)
            h.update(chunk)
            n += len(chunk)
    archive_sha = h.hexdigest()
    entry = {"url": spec["url"], "final_url": r.url.split("?")[0], "archive_sha256": archive_sha, "archive_bytes": n,
             "role": spec["role"], "note": spec.get("note"), "files": {}}
    if spec.get("expect_sha256") and archive_sha != spec["expect_sha256"]:
        raise SystemExit(f"{name}: sha256 {archive_sha} != published {spec['expect_sha256']}")
    if "keep" not in spec:
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmpfile.replace(safe_out(dest))
        entry["files"][str(dest.relative_to(HERE))] = {"sha256": archive_sha, "bytes": n}
    else:
        dest.mkdir(parents=True, exist_ok=True)
        pats = [re.compile(p) for p in spec["keep"]]
        skipped = []
        with zipfile.ZipFile(tmpfile) as z:
            for m in z.namelist():
                if m.endswith("/"):
                    continue
                if any(p.search(m) for p in pats):
                    tgt = safe_out(dest / Path(m).name)
                    data = z.read(m)
                    tgt.write_bytes(data)
                    entry["files"][str(tgt.relative_to(HERE))] = {"sha256": hashlib.sha256(data).hexdigest(),
                                                                  "bytes": len(data), "member": m}
                else:
                    skipped.append(m)
        entry["members_not_extracted"] = skipped
        tmpfile.unlink()
    manifest["downloads"][name] = entry
    log(f"[download] {name} done sha256={archive_sha[:16]} bytes={n} files={len(entry['files'])}")


def main():
    for d in (RAW, LIC, LOGS, TMP):
        d.mkdir(parents=True, exist_ok=True)
    manifest = {"created_utc": now(), "commits": COMMITS, "downloads": {}}
    read_records(manifest)
    for name, spec in DOWNLOADS.items():
        download(name, spec, manifest)
    bad = [k for k, v in manifest["licence_records"].items() if not v["pass"]]
    manifest["g1_pass"] = not bad
    (LOGS / "fetch_manifest.json").write_text(json.dumps(manifest, indent=1))
    log(f"[fetch] g1_pass={not bad} failed_records={bad}")
    if bad:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
