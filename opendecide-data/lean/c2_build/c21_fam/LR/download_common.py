"""L-R shared downloader helpers (C2.1, block R). Written Sun 18 Oct 2026 by the L-R builder (Sonnet 5.5).

WHAT THIS MODULE DOES
  * fetches raw public files with a streaming sha256 (requests + certifi; no model, no API key, no Modal);
  * writes ONLY the TRAIN split of a dataset under  <lean>/data/c21_raw/<dataset>/train/ ;
  * writes every non-train split (test / dev / validation / ambiguous / own frozen hold-out) ONLY into the
    program-only quarantine store  <lean>/bench/c21_eval_quarantine/lr_targets/<dataset>/  (the G13 target store).
    A downloader streams such bytes straight to disk and logs sha256 + size + row COUNT only. It never prints,
    returns or logs any content of a non-train file, and no agent opens the quarantine store (plan 16.1 step 1);
  * writes a LICENCE record (quoted line, URL, fetch date, sha of the fetched licence page, quote_found) and a
    SHA256SUMS file next to the train files; appends one entry to  LR/logs/download_<dataset>.json .

PROGRAM-ONLY RULE FOR MULTI-SPLIT FILES
  When one upstream file holds several splits (ABCD json.gz, Qasper tgz, SciFact tgz, Taskmaster dialogues, MultiWOZ
  dialog acts, Juliet suite) the archive is staged inside the quarantine store, split by a PROGRAM on the split
  field / id list, the train part is written to train/, the rest stays in quarantine, and the staged archive is
  deleted. The programs here parse such files but only to route records; nothing about a non-train record leaves them.

FROZEN OWN HOLD-OUT (rule 2 of plan 16.3)
  Where a release has no split, `holdout_unit(unit_id, seed, frac)` freezes a seeded 10% hold-out by the unit the
  release naturally groups (prompt id, CWE family, repo ...) BEFORE mapping; the hold-out goes to quarantine (it is an
  internal G13 target and is never trained).

The paths below contain no 'ohs' / 'sealed' component (pathskip rule); `assert_safe_path` enforces it.
"""
import datetime
import hashlib
import html
import io
import json
import os
import re
import shutil
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
FAM_DIR = os.path.dirname(HERE)
BUILD_DIR = os.path.dirname(FAM_DIR)
LEAN_DIR = os.path.dirname(BUILD_DIR)
INFRA_DIR = os.path.join(BUILD_DIR, "c21_infra")
if INFRA_DIR not in sys.path:
    sys.path.insert(0, INFRA_DIR)
from pathskip import is_skipped_path  # noqa: E402

RAW_ROOT = os.path.join(LEAN_DIR, "data", "c21_raw")
QUAR_ROOT = os.path.join(LEAN_DIR, "bench", "c21_eval_quarantine", "lr_targets")
LOG_DIR = os.path.join(HERE, "logs")
UA = "c21-lr-downloader/1 (public train-split fetch; contact: dataset owner)"
HOLDOUT_SEED = "c21-lr-holdout-v1"
HOLDOUT_FRAC = 0.10


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def assert_safe_path(p):
    if is_skipped_path(p):
        raise RuntimeError("refused: path has an ohs/sealed component: %r" % p)
    return p


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(chunk), b""):
            h.update(blk)
    return h.hexdigest()


def holdout_unit(unit_id, seed=HOLDOUT_SEED, frac=HOLDOUT_FRAC):
    """Deterministic seeded hold-out assignment by unit id (True = hold-out). Uses sha256, no RNG state."""
    d = hashlib.sha256(("%s|%s" % (seed, unit_id)).encode("utf-8")).digest()
    return (int.from_bytes(d[:8], "big") / float(1 << 64)) < frac


def holdout_set(unit_ids, prefix, frac=HOLDOUT_FRAC, seed=HOLDOUT_SEED):
    """Exactly ceil(frac * n) units with the lowest seeded hash (for small unit counts, e.g. 80 repos): deterministic."""
    import math
    ids = sorted(set(unit_ids))
    k = max(1, int(math.ceil(frac * len(ids))))
    ranked = sorted(ids, key=lambda u: hashlib.sha256(("%s|%s|%s" % (seed, prefix, u)).encode("utf-8")).digest())
    return set(ranked[:k])


# ----------------------------------------------------------------------------------------------------------
# Fetching
# ----------------------------------------------------------------------------------------------------------
def fetch_to(url, dest, retries=4, timeout=120, headers=None):
    """Stream url -> dest (atomic rename). Returns {'sha256','bytes','url','fetched_utc'}. Never parses content."""
    assert_safe_path(dest)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    last = None
    for attempt in range(retries):
        try:
            h = hashlib.sha256()
            n = 0
            hd = {"User-Agent": UA}
            if headers:
                hd.update(headers)
            with requests.get(url, stream=True, timeout=timeout, headers=hd) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    for blk in r.iter_content(1 << 20):
                        if blk:
                            f.write(blk)
                            h.update(blk)
                            n += len(blk)
            os.replace(tmp, dest)
            return {"url": url, "sha256": h.hexdigest(), "bytes": n, "fetched_utc": utc_now()}
        except Exception as e:  # noqa: BLE001 - retry any network error
            last = e
            time.sleep(2 + 3 * attempt)
    raise RuntimeError("fetch failed after %d tries: %s (%s)" % (retries, url, last))


def fetch_text(url, timeout=60):
    r = requests.get(url, timeout=timeout, headers={"User-Agent": UA})
    r.raise_for_status()
    return r.content


def gh_tree(repo, ref):
    """List a public GitHub repo tree (names and sizes only)."""
    r = requests.get("https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (repo, ref), timeout=60,
                     headers={"User-Agent": UA})
    r.raise_for_status()
    d = r.json()
    if d.get("truncated"):
        raise RuntimeError("github tree truncated for %s" % repo)
    return [(t["path"], t.get("size")) for t in d["tree"] if t["type"] == "blob"]


def raw_url(repo, ref, path):
    from urllib.parse import quote
    return "https://raw.githubusercontent.com/%s/%s/%s" % (repo, ref, quote(path))


# ----------------------------------------------------------------------------------------------------------
# Licence record
# ----------------------------------------------------------------------------------------------------------
def _norm_text(t):
    t = html.unescape(t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)   # markdown link -> its text
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    t = re.sub(r"[*_`\[\]#>|\\]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip().lower()


def licence_record(dataset, lr_id, quote, quote_url, verify_url, licence_class, provenance, tier,
                   share_alike=False, notes="", quote_alternatives=None, extra=None):
    """Fetch `verify_url`, check the quote is on the page, return the LICENCE record (a dict).

    quote_alternatives: other exact strings that also count (for cards that say the same thing in YAML).
    provenance: 'human' or 'program' (the plan's enum; 'selection-rule' and any LLM marker deny).
    """
    assert provenance in ("human", "program")
    rec = {
        "schema": "lr-licence-1", "dataset": dataset, "lr_id": lr_id, "tier": tier,
        "quoted_line": quote, "quote_url": quote_url, "verified_via_url": verify_url,
        "licence_class": licence_class, "provenance_enum": provenance, "share_alike_flag": bool(share_alike),
        "notes": notes,
    }
    try:
        body = fetch_text(verify_url)
        text = _norm_text(body.decode("utf-8", "replace"))
        cands = [quote] + list(quote_alternatives or [])
        found = [c for c in cands if _norm_text(c) in text]
        rec.update({"fetched_utc": utc_now(), "page_sha256": sha256_bytes(body), "page_bytes": len(body),
                    "quote_found": bool(found), "quote_matched": found[0] if found else None})
    except Exception as e:  # noqa: BLE001
        rec.update({"fetched_utc": utc_now(), "page_sha256": None, "page_bytes": 0, "quote_found": False,
                    "quote_matched": None, "fetch_error": str(e)[:300]})
    rec["status"] = "OK" if rec["quote_found"] else "QUOTE_NOT_VERIFIED"
    if extra:
        rec.update(extra)
    return rec


# ----------------------------------------------------------------------------------------------------------
# Store
# ----------------------------------------------------------------------------------------------------------
class Store(object):
    """Output locations + the running download log for ONE dataset."""

    def __init__(self, dataset):
        self.dataset = dataset
        self.train_dir = assert_safe_path(os.path.join(RAW_ROOT, dataset, "train"))
        self.quar_dir = assert_safe_path(os.path.join(QUAR_ROOT, dataset))
        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.quar_dir, exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log = {"dataset": dataset, "started_utc": utc_now(), "train_files": [], "quarantine_files": [],
                    "notes": []}

    # train side ---------------------------------------------------------------------------------------------
    def train_path(self, rel):
        return assert_safe_path(os.path.join(self.train_dir, rel))

    def add_train_file(self, rel, source_urls=None, rows=None, note=None):
        p = self.train_path(rel)
        ent = {"path": rel, "sha256": sha256_file(p), "bytes": os.path.getsize(p)}
        if source_urls:
            ent["source_urls"] = source_urls
        if rows is not None:
            ent["rows"] = rows
        if note:
            ent["note"] = note
        self.log["train_files"].append(ent)
        return ent

    def write_train_json(self, rel, obj, source_urls=None, rows=None, note=None, jsonl=False):
        p = self.train_path(rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        import gzip
        opener = (lambda: gzip.open(p, "wt", encoding="utf-8", compresslevel=6)) if rel.endswith(".gz") else (lambda: open(p, "w", encoding="utf-8"))
        with opener() as f:
            if jsonl:
                for o in obj:
                    f.write(json.dumps(o, ensure_ascii=False) + "\n")
            else:
                json.dump(obj, f, ensure_ascii=False)
        return self.add_train_file(rel, source_urls, rows if rows is not None else (len(obj) if hasattr(obj, "__len__") else None), note)

    # quarantine side ----------------------------------------------------------------------------------------
    def quar_path(self, rel):
        return assert_safe_path(os.path.join(self.quar_dir, rel))

    def add_quar_file(self, rel, role, source_urls=None, rows=None):
        """Log sha / size / row count of a quarantine file (never its content)."""
        p = self.quar_path(rel)
        ent = {"path": "<quarantine>/" + rel, "role": role, "sha256": sha256_file(p), "bytes": os.path.getsize(p)}
        if source_urls:
            ent["source_urls"] = source_urls
        if rows is not None:
            ent["rows"] = rows
        self.log["quarantine_files"].append(ent)
        return ent

    def write_quar_json(self, rel, obj, role, source_urls=None, jsonl=False, rows=None):
        p = self.quar_path(rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        import gzip
        opener = (lambda: gzip.open(p, "wt", encoding="utf-8", compresslevel=6)) if rel.endswith(".gz") else (lambda: open(p, "w", encoding="utf-8"))
        with opener() as f:
            if jsonl:
                for o in obj:
                    f.write(json.dumps(o, ensure_ascii=False) + "\n")
            else:
                json.dump(obj, f, ensure_ascii=False)
        return self.add_quar_file(rel, role, source_urls, rows if rows is not None else (len(obj) if hasattr(obj, "__len__") else None))

    def stage(self, url, name):
        """Download a multi-split archive into quarantine/_staging (program-only). Returns (path, fetch_info)."""
        dest = self.quar_path(os.path.join("_staging", name))
        info = fetch_to(url, dest)
        return dest, info

    def clear_staging(self):
        d = self.quar_path("_staging")
        if os.path.isdir(d):
            shutil.rmtree(d)

    # records ------------------------------------------------------------------------------------------------
    def write_licence(self, rec):
        p = self.train_path("LICENCE.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False)
        self.log["licence"] = {"status": rec.get("status"), "quote_found": rec.get("quote_found"),
                               "licence_class": rec.get("licence_class"), "sha256": sha256_file(p),
                               "page_sha256": rec.get("page_sha256"), "fetched_utc": rec.get("fetched_utc")}

    def finish(self, extra=None):
        # SHA256SUMS of train files (excluding itself)
        lines = []
        for ent in sorted(self.log["train_files"], key=lambda e: e["path"]):
            lines.append("%s  %s" % (ent["sha256"], ent["path"]))
        sums = self.train_path("SHA256SUMS")
        with open(sums, "w") as f:
            f.write("\n".join(lines) + "\n")
        self.log["finished_utc"] = utc_now()
        self.log["train_total_bytes"] = sum(e["bytes"] for e in self.log["train_files"])
        self.log["train_total_files"] = len(self.log["train_files"])
        self.log["quarantine_total_files"] = len(self.log["quarantine_files"])
        if extra:
            self.log.update(extra)
        lp = os.path.join(LOG_DIR, "download_%s.json" % self.dataset)
        with open(lp, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2, ensure_ascii=False)
        return self.log


def summarize(log):
    """One-line console summary (counts and shas only)."""
    return "%s: train_files=%d (%d bytes) quarantine_files=%d licence=%s" % (
        log["dataset"], log["train_total_files"], log["train_total_bytes"], log["quarantine_total_files"],
        log.get("licence", {}).get("status"))


def key_hash(x):
    """Stable short hash of a key (id or normalised text); only hashes and counts ever leave the downloader."""
    return hashlib.sha256(re.sub(r"\s+", " ", str(x)).strip().lower().encode("utf-8")).hexdigest()[:20]


def record_overlap(store, name, train_keys, other_keys):
    """Log |train ∩ other| as COUNTS ONLY (no key or content is logged). Run inside the downloader program."""
    a = {key_hash(k) for k in train_keys}
    b = {key_hash(k) for k in other_keys}
    store.log.setdefault("split_overlap_counts", {})[name] = {"train_keys": len(a), "other_keys": len(b), "intersection": len(a & b)}
    return len(a & b)


# ----------------------------------------------------------------------------------------------------------
# Hugging Face helpers (public datasets only; no token)
# ----------------------------------------------------------------------------------------------------------
def hf_revision(repo):
    from huggingface_hub import HfApi
    return HfApi().dataset_info(repo).sha


def hf_url(repo, rev, path):
    from urllib.parse import quote
    return "https://huggingface.co/datasets/%s/resolve/%s/%s" % (repo, rev, quote(path))


def hf_card_url(repo, rev):
    return "https://huggingface.co/datasets/%s/raw/%s/README.md" % (repo, rev)


def gh_commit_sha(repo, ref):
    r = requests.get("https://api.github.com/repos/%s/commits/%s" % (repo, ref), timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    return r.json()["sha"]
