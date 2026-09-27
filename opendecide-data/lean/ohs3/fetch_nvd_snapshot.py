"""Download the frozen NVD CVE API 2.0 snapshot used by build_nvd_attack_vector.py.

All CVEs published 2026-06-01T00:00:00.000 .. 2026-09-26T23:59:59.999 (one window, under NVD's 120-day limit).
Every page is saved verbatim (gzip-compressed) under ohs3/cache/nvd_attack_vector/, with the sha256 of the
uncompressed body, the API timestamp and totalResults in manifest.json. Run once; the builder reads only the cache.
Refuses to overwrite an existing snapshot unless --force is given. No API key (public rate limit 5 req / 30 s).
"""
import datetime as dt
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

import requests

CACHE = Path(__file__).resolve().parent / "cache" / "nvd_attack_vector"
BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
START, END = "2026-06-01T00:00:00.000", "2026-09-26T23:59:59.999"
PER_PAGE = 2000


def url(start_index):
    return f"{BASE}?pubStartDate={START}&pubEndDate={END}&resultsPerPage={PER_PAGE}&startIndex={start_index}"


def get(u):
    for attempt in range(8):
        try:
            r = requests.get(u, timeout=180, headers={"User-Agent": "opendecide-ohs3-snapshot"})
            if r.status_code == 200:
                return r.content
            print("status", r.status_code, "retry", attempt, flush=True)
        except requests.RequestException as e:
            print("error", e, "retry", attempt, flush=True)
        time.sleep(15 * (attempt + 1))
    raise SystemExit(f"failed: {u}")


def main():
    manifest_p = CACHE / "manifest.json"
    if manifest_p.exists() and "--force" not in sys.argv:
        print("snapshot exists; not refetching (use --force)")
        return
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = {"fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "api": BASE, "pubStartDate": START, "pubEndDate": END, "pages": []}
    start, total = 0, None
    while total is None or start < total:
        u = url(start)
        body = get(u)
        d = json.loads(body)
        if total is None:
            total = d["totalResults"]
        assert d["totalResults"] == total, "totalResults changed during fetch"
        assert d["startIndex"] == start
        name = f"page_{start:06d}.json.gz"
        (CACHE / name).write_bytes(gzip.compress(body, mtime=0))
        manifest["pages"].append({"file": name, "url": u, "n": len(d["vulnerabilities"]), "totalResults": total,
                                  "api_timestamp": d["timestamp"], "sha256_uncompressed": hashlib.sha256(body).hexdigest()})
        print(name, len(d["vulnerabilities"]), "/", total, flush=True)
        start += PER_PAGE
        time.sleep(7)
    assert sum(p["n"] for p in manifest["pages"]) == total
    manifest["totalResults"] = total
    manifest_p.write_text(json.dumps(manifest, indent=1))
    print("done", total)


if __name__ == "__main__":
    main()
