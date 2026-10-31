"""L-R tier-C shared helpers (C2.1 block R, written Sun 18 Oct 2026 by the L-R tier-C builder, Sonnet 5.5).

Adds to download_common.py / lr_common.py WITHOUT editing them (their shas are logged in A64_TOOLS.md):
  * licence_with_checks(): the primary licence record (quoted line, URL, fetch date, page sha) plus any number of secondary
    quote checks stored under "also_verified" (e.g. the licence of an upstream source the data is built on);
  * per-repo licence lookup against the GitHub licence API (SPDX id) and the ONE code whitelist of Opus batch-1 ruling LR-M3;
  * small JSON/JSONL readers for train files (gz or plain).
No model, no model API, no Modal. The GitHub API is called WITHOUT credentials (60 requests per hour); callers must keep
their per-repo lookups small (SWE-Gym has 11 repos).
"""
import gzip
import json
import os
import sys

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import download_common as dc  # noqa: E402

# Opus batch-1 ruling LR-M3: ONE code whitelist (SPDX ids as GitHub's licensee reports them). ISC, Unlicense, MPL, EPL,
# Artistic, AGPL, LGPL, "unknown" and every other licence are dropped row by row.
CODE_WHITELIST_SPDX = ("MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0")
# CommitPackFT's lower-case licence field values for the same whitelist.
CODE_WHITELIST_CPFT = ("mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "cc0-1.0")


def licence_with_checks(dataset, lr_id, quote, quote_url, verify_url, licence_class, provenance, notes="",
                        also=None, quote_alternatives=None, share_alike=False, extra=None):
    """Primary licence record (dc.licence_record, tier C) plus secondary checks: also = [{"label","quote","url","verify_url"}].
    Each secondary check fetches its page, checks the quote and records page sha + fetch time under extra['also_verified']."""
    rec = dc.licence_record(dataset, lr_id, quote=quote, quote_url=quote_url, verify_url=verify_url,
                            licence_class=licence_class, provenance=provenance, tier="C", share_alike=share_alike,
                            notes=notes, quote_alternatives=quote_alternatives, extra=extra)
    checks = []
    for a in (also or []):
        r = dc.licence_record(dataset, lr_id, quote=a["quote"], quote_url=a["url"], verify_url=a.get("verify_url", a["url"]),
                              licence_class=a.get("licence_class", licence_class), provenance=provenance, tier="C",
                              notes=a.get("label", ""), quote_alternatives=a.get("alternatives"))
        checks.append({"label": a.get("label", ""), "quote": a["quote"], "url": a["url"], "verify_url": a.get("verify_url", a["url"]),
                       "page_sha256": r.get("page_sha256"), "fetched_utc": r.get("fetched_utc"), "quote_found": r.get("quote_found"),
                       "fetch_error": r.get("fetch_error")})
    if checks:
        rec["also_verified"] = checks
        if rec["status"] == "OK" and not all(c["quote_found"] for c in checks):
            rec["status"] = "QUOTE_NOT_VERIFIED"
    return rec


def github_repo_licence(repo, timeout=60):
    """SPDX id GitHub's licensee reports for `repo` ('owner/name'), plus the licence file path; None when GitHub has none.
    No credentials. Returns {'repo','spdx_id','name','path','html_url','fetched_utc','http'}."""
    r = requests.get("https://api.github.com/repos/%s/license" % repo, timeout=timeout, headers={"User-Agent": dc.UA})
    out = {"repo": repo, "http": r.status_code, "fetched_utc": dc.utc_now(), "spdx_id": None, "name": None, "path": None,
           "html_url": None}
    if r.status_code == 200:
        d = r.json()
        lic = d.get("license") or {}
        out.update({"spdx_id": lic.get("spdx_id"), "name": lic.get("name"), "path": d.get("path"), "html_url": d.get("html_url")})
    return out


def whitelisted(spdx):
    return spdx in CODE_WHITELIST_SPDX


def read_json_any(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def iter_jsonl_any(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)
