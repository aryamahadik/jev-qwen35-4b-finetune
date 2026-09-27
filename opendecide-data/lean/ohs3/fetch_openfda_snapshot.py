"""Download the frozen openFDA enforcement snapshot used by build_openfda_recall_class.py.

Saves every page verbatim under ohs3/cache/openfda_recall_class/ plus a manifest with the fetch time and the API's
meta.last_updated. Run once; the builder only reads the cache, so re-runs of the builder are identical.
Refuses to overwrite an existing snapshot unless --force is given.
"""
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

import requests

CACHE = Path(__file__).resolve().parent / "cache" / "openfda_recall_class"
TYPES = ["food", "drug", "device"]
DATE_Q = "report_date:[20260601+TO+20260926]"
LIMIT = 1000


def url(t, skip):
    return f"https://api.fda.gov/{t}/enforcement.json?search={DATE_Q}&limit={LIMIT}&skip={skip}"


def main():
    manifest_p = CACHE / "manifest.json"
    if manifest_p.exists() and "--force" not in sys.argv:
        print("snapshot exists; not refetching (use --force)")
        return
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = {"fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "query": DATE_Q, "pages": []}
    for t in TYPES:
        skip = 0
        while True:
            u = url(t, skip)
            r = requests.get(u, timeout=60)
            r.raise_for_status()
            body = r.content
            d = json.loads(body)
            name = f"{t}_skip{skip}.json"
            (CACHE / name).write_bytes(body)
            total = d["meta"]["results"]["total"]
            manifest["pages"].append({"file": name, "url": u, "n": len(d["results"]), "total": total,
                                      "last_updated": d["meta"]["last_updated"],
                                      "license": d["meta"].get("license"),
                                      "sha256": hashlib.sha256(body).hexdigest()})
            skip += LIMIT
            if skip >= total:
                break
            time.sleep(1)
    manifest_p.write_text(json.dumps(manifest, indent=1))
    print(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
