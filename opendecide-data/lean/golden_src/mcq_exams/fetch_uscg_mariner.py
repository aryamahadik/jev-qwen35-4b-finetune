"""One-time snapshot of the USCG National Maritime Center sample examinations (merchant mariner credential exams).

The official host (www.dco.uscg.mil/Portals/9/NMC/pdfs/examinations/) refuses non-browser clients (Akamai 403), so the
byte-exact official PDFs are fetched from the Internet Archive's raw ('id_') captures of those official URLs. For each
exam file name the latest 200/application-pdf capture listed by the Wayback CDX API (queried 29 Sep 2026) is used.
Exams that need a chart, almanac, tide/stability tables or plotting (file names with chart / problems / plot /
miss_river) are not fetched: their questions cannot be answered from the question text.

Writes cache/uscg_mariner/<file>.pdf and the pinned list uscg_mariner_files.json ({code: {file, url, wayback, sha256,
truncated}}; six large engineering captures are cut at 5 MiB by the archive and are marked truncated and skipped),
which build_uscg_mariner.py verifies. Re-running with the pinned list only re-downloads missing files.
"""
import hashlib
import json
import re
import ssl
import sys
import time
import urllib.request
from pathlib import Path

import certifi

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "uscg_mariner"
PINNED = HERE / "uscg_mariner_files.json"
CDX = ("https://web.archive.org/cdx/search/cdx?url=dco.uscg.mil/Portals/9/NMC/pdfs/examinations/*&output=json"
       "&fl=original,timestamp,mimetype,length&filter=statuscode:200&filter=mimetype:application/pdf&limit=5000")
SKIP = re.compile(r"chart|problems|plot|miss_river", re.I)
UA = {"User-Agent": "opendecide-golden-builder (research dataset snapshot)"}
CTX = ssl.create_default_context(cafile=certifi.where())  # the framework Python has no CA bundle here


def get(url, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300, context=CTX) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            time.sleep(5 * (k + 1))


def select():
    rows = json.loads(get(CDX))[1:]
    best = {}
    for orig, ts, _mt, _ln in rows:
        m = re.search(r"examinations/(q\d{3}[^?]*\.pdf)", orig, re.I)
        if not m:
            continue
        name = m.group(1).lower()
        if SKIP.search(name):
            continue
        if name not in best or ts > best[name][1]:
            best[name] = (orig, ts)
    sel = {}
    for name, (orig, ts) in best.items():  # one file per exam code (alternative spellings: keep the latest)
        code = name[:4]
        if code in sel and sel[code]["wayback"] > ts:
            continue
        sel[code] = {"file": name, "url": orig, "wayback": ts}
    return dict(sorted(sel.items()))


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    pinned = json.loads(PINNED.read_text()) if PINNED.exists() else None
    sel = pinned or select()
    for code, rec in sel.items():
        p = CACHE / rec["file"]
        if not p.exists():
            raw = get(f"https://web.archive.org/web/{rec['wayback']}id_/{rec['url']}")
            if not raw.startswith(b"%PDF"):
                sys.exit(f"not a PDF: {code} {rec}")
            p.write_bytes(raw)
            time.sleep(1.0)
        raw = p.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if "sha256" in rec and rec["sha256"] != sha:
            sys.exit(f"sha256 mismatch {p}")
        rec["sha256"] = sha
        # some large captures are cut at 5 MiB by the archive (no %%EOF, unreadable): pinned as truncated, skipped
        rec["truncated"] = b"%%EOF" not in raw[-2048:]
        print(code, rec["file"], rec["wayback"], sha[:12], flush=True)
    if not pinned:
        PINNED.write_text(json.dumps(sel, indent=1) + "\n")
    print(f"{len(sel)} files pinned -> {PINNED}")


if __name__ == "__main__" and "--extra" not in sys.argv:
    main()


# ------------------------------------------------------------------------------------------------ earlier versions
# NMC re-issues each sample exam with a fresh draw from its question bank, so earlier captures of the same exam hold
# further official questions. `python fetch_uscg_mariner.py --extra` snapshots every other distinct capture (by the
# archive's content digest) made since 2024-06-01 (the current PDF layout with 'Correct answer:' lines), smaller than
# 4.5 MB, of the exams pinned above (truncated ones excluded) into cache/uscg_mariner/extra/<code>__<capture>.pdf and
# pins them in uscg_mariner_extra_files.json. The builder uses them after the latest versions, so a question that also
# appears in a newer version is taken from the newer one.
EXTRA = HERE / "uscg_mariner_extra_files.json"
CDX_DIGEST = ("https://web.archive.org/cdx/search/cdx?url=dco.uscg.mil/Portals/9/NMC/pdfs/examinations/*&output=json"
              "&fl=original,timestamp,digest,length&filter=statuscode:200&filter=mimetype:application/pdf&limit=5000")


def extra():
    latest = json.loads(PINNED.read_text())
    if EXTRA.exists():
        sel = json.loads(EXTRA.read_text())
    else:
        rows = json.loads(get(CDX_DIGEST))[1:]
        seen, sel = {}, []
        for orig, ts, dig, ln in sorted(rows, key=lambda r: (r[0], r[1])):
            m = re.search(r"examinations/(q\d{3})[^?]*\.pdf", orig, re.I)
            if not m:
                continue
            name = re.search(r"examinations/([^?]*)", orig).group(1).lower()
            code = m.group(1).lower()
            if SKIP.search(name) or code not in latest or latest[code].get("truncated"):
                continue
            if ts == latest[code]["wayback"] or ts < "20240601" or int(ln) >= 4_500_000:
                continue
            if dig in seen.setdefault(code, {}):
                continue
            seen[code][dig] = ts
            sel.append({"code": code, "file": f"{code}__{ts}.pdf", "url": orig, "wayback": ts, "digest": dig})
        EXTRA.write_text(json.dumps(sel, indent=1) + "\n")  # selection pinned before downloading
    d = CACHE / "extra"
    d.mkdir(parents=True, exist_ok=True)

    def download(rec):
        p = d / rec["file"]
        if p.exists():
            return
        try:
            raw = get(f"https://web.archive.org/web/{rec['wayback']}id_/{rec['url']}")
        except Exception:  # noqa: BLE001
            return
        tmp = p.with_suffix(".part")
        tmp.write_bytes(raw)
        tmp.rename(p)
        print("got", rec["file"], len(raw), flush=True)

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(download, sel))
    for rec in sel:
        p = d / rec["file"]
        if not p.exists():
            rec["missing"] = True
            continue
        rec.pop("missing", None)
        raw = p.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if "sha256" in rec and rec["sha256"] != sha:
            sys.exit(f"sha256 mismatch {p}")
        rec["sha256"] = sha
        rec["truncated"] = not raw.startswith(b"%PDF") or b"%%EOF" not in raw[-2048:]
        print(rec["code"], rec["wayback"], len(raw), rec["truncated"], flush=True)
    EXTRA.write_text(json.dumps(sel, indent=1) + "\n")
    print(f"{len(sel)} earlier versions pinned -> {EXTRA}")


if __name__ == "__main__" and "--extra" in sys.argv:
    extra()
