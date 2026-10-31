"""One-time snapshot of the US NRC Generic Fundamentals Examination (GFE) question banks (November 2020 edition),
PWR topics 191 (components), 192 (reactor theory), 193 (thermodynamics) and BWR topics 291/292/293.

Official URLs: https://www.nrc.gov/reactors/operator-licensing/history-rulemaking-activities/generic-fundamentals-
examinations/{pwr/pwr-files/19Xall.pdf, bwr/bwr-files/29Xall.pdf}. nrc.gov refuses non-browser clients (Akamai 403),
so the byte-exact official files are fetched from the Internet Archive's raw ('id_') captures listed below (a complete
capture, ending in %%EOF, was chosen for each; some other captures are cut at 1 MiB). Writes cache/nrc_gfe/<file> and
nrc_gfe_files.json (pinned url, capture, sha256), which build_nrc_gfe.py verifies.
"""
import hashlib
import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path

import certifi

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "nrc_gfe"
PINNED = HERE / "nrc_gfe_files.json"
BASE = ("https://www.nrc.gov/reactors/operator-licensing/history-rulemaking-activities/generic-fundamentals-"
        "examinations/")
CAPTURES = {  # file -> (path under BASE, Wayback timestamp)
    "191all.pdf": ("pwr/pwr-files/191all.pdf", "20250204032143"),
    "192all.pdf": ("pwr/pwr-files/192all.pdf", "20240911140049"),
    "193all.pdf": ("pwr/pwr-files/193all.pdf", "20250208153314"),
    "291all.pdf": ("bwr/bwr-files/291all.pdf", "20250204005909"),
    "292all.pdf": ("bwr/bwr-files/292all.pdf", "20250207092638"),
    "293all.pdf": ("bwr/bwr-files/293all.pdf", "20250207103947"),
}
CTX = ssl.create_default_context(cafile=certifi.where())


def get(url):
    for k in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "opendecide-golden-builder"})
            with urllib.request.urlopen(req, timeout=600, context=CTX) as r:
                return r.read()
        except Exception:  # noqa: BLE001
            time.sleep(15 * (k + 1))
    raise RuntimeError(url)


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    pinned = json.loads(PINNED.read_text()) if PINNED.exists() else {}
    out = {}
    for name, (path, ts) in CAPTURES.items():
        p = CACHE / name
        url = BASE + path
        for attempt in range(4):
            if not p.exists():
                p.write_bytes(get(f"https://web.archive.org/web/{ts}id_/{url}"))
                time.sleep(2)
            raw = p.read_bytes()
            if raw.startswith(b"%PDF") and b"%%EOF" in raw[-2048:]:
                break
            p.unlink()  # truncated transfer: retry
            time.sleep(20)
        else:
            sys.exit(f"could not get a complete copy of {name}")
        sha = hashlib.sha256(raw).hexdigest()
        if name in pinned and pinned[name]["sha256"] != sha:
            sys.exit(f"sha256 mismatch {name}")
        out[name] = {"url": url, "wayback": ts, "sha256": sha, "bytes": len(raw)}
        print(name, ts, len(raw), sha[:12], flush=True)
    PINNED.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
