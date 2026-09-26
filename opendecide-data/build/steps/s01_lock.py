#!/usr/bin/env python3
"""s01_lock: resolve every source and model pin to a full commit sha and write build/sources.lock.json (DESIGN 13 step 1).

For each config.yaml `sources` entry:
  * hf_dataset: HfApi().dataset_info(repo, revision=...) with a prefix check. A pin that is only a prefix, or a
    conversion ref (refs/convert/parquet), is matched against the ref head and then against the ref's commit history.
    Files matching the entry's `files` globs (every file when null) are listed at the resolved sha with their size,
    git blob id and sha256 (the Hub's LFS sha256; small non-LFS data files are downloaded to the HF cache and hashed).
  * github: GitHub commits API (prefix check), then every listed file is downloaded at the resolved commit into
    $HF_HOME/opendecide/github/ and hashed. Globs are expanded with the git trees API. If the API is rate-limited and
    the pin is a full sha, the commit is verified by downloading the listed files at that sha.
  * url: fetched once, cached under $HF_HOME/opendecide/url/, sha256 recorded.
For each config.yaml `models` entry: HfApi().model_info with the same prefix logic; weight/config/tokenizer files
are listed with their sha256 (nothing is downloaded).
Large corpora are never downloaded here; loaders fetch them at the locked sha (streaming where config says so).
A pin that cannot be resolved is recorded with its reason and the step continues (exit 0; the summary lists it).

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import datetime
import fnmatch
import hashlib
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common  # noqa: E402

STEP = "s01_lock"
DATA_EXT = (".json", ".jsonl", ".csv", ".tsv", ".txt", ".parquet", ".arrow")
SMALL_BYTES = 20 * 2**20
MODEL_FILE_GLOBS = ["*.json", "*.safetensors", "*.bin", "*.model", "*.txt", "*.py", "*/config.json"]
URL_CACHE = common.HF_HOME / "opendecide" / "url"


def _glob_prefixes(patterns: list[str] | None) -> list[str]:
    """Literal directory prefixes of the globs (to list only the relevant part of a big repo)."""
    if not patterns:
        return [""]
    out = set()
    for p in patterns:
        lit = []
        for part in p.split("/"):
            if any(ch in part for ch in "*?["):
                break
            lit.append(part)
        if len(lit) == len(p.split("/")):  # an explicit file path
            lit = lit[:-1]
        out.add("/".join(lit))
    # drop prefixes contained in others
    res = sorted(out)
    return [p for p in res if not any(p != q and (p.startswith(q + "/") or q == "") for q in res)]


def _match(path: str, patterns: list[str] | None) -> bool:
    return patterns is None or any(fnmatch.fnmatchcase(path, pat) for pat in patterns)


# ------------------------------------------------------------------------------------------------------------------
# Hugging Face
# ------------------------------------------------------------------------------------------------------------------
def _hf_resolve(api, repo: str, repo_type: str, pin: str | None, ref: str | None) -> tuple[str | None, list[str], str]:
    """Return (full_sha | None, notes, status)."""
    notes: list[str] = []
    info_fn = api.dataset_info if repo_type == "dataset" else api.model_info
    if pin and common.FULL_SHA.match(pin):
        try:
            sha = info_fn(repo, revision=pin).sha
        except Exception as exc:
            return None, [f"pinned sha not found on the Hub: {type(exc).__name__}: {exc}"], "unresolved"
        if sha != pin:
            return None, [f"Hub returned {sha} for pin {pin}"], "unresolved"
        if ref:
            try:
                head = info_fn(repo, revision=ref).sha
                notes.append("pin is the current head of " + ref if head == pin else f"{ref} head is now {head}")
            except Exception as exc:
                notes.append(f"could not read {ref}: {exc}")
        return sha, notes, "resolved"
    try:
        head = info_fn(repo, revision=ref).sha if ref else info_fn(repo).sha
    except Exception as exc:
        return None, [f"{type(exc).__name__}: {exc}"], "unresolved"
    where = ref or "main"
    if not pin:
        notes.append(f"no pin in DESIGN/config; recorded the head of {where}")
        return head, notes, "resolved"
    if head.startswith(pin):
        notes.append(f"prefix {pin} = head of {where}")
        return head, notes, "resolved"
    try:
        commits = api.list_repo_commits(repo, repo_type=repo_type, revision=ref) if ref else \
            api.list_repo_commits(repo, repo_type=repo_type)
    except Exception as exc:
        return None, [f"head of {where} is {head} (no prefix match) and history is unreadable: {exc}"], "unresolved"
    hits = sorted({c.commit_id for c in commits if c.commit_id.startswith(pin)})
    if len(hits) == 1:
        notes.append(f"prefix {pin} found in the history of {where} (head is now {head})")
        return hits[0], notes, "resolved"
    if len(hits) > 1:
        return None, [f"prefix {pin} is ambiguous: {hits}"], "unresolved"
    return None, [f"prefix {pin} not found in {len(commits)} commits of {where}; head is {head}"], "unresolved"


def _hf_files(api, repo: str, repo_type: str, sha: str, patterns: list[str] | None, fetch_small: bool) -> tuple[list, list]:
    from huggingface_hub import hf_hub_download
    from huggingface_hub.hf_api import RepoFile
    files, notes = [], []
    seen = set()
    for prefix in _glob_prefixes(patterns):
        kw = {"path_in_repo": prefix} if prefix else {}
        try:
            tree = list(api.list_repo_tree(repo, repo_type=repo_type, revision=sha, recursive=True, **kw))
        except Exception as exc:
            notes.append(f"list_repo_tree({prefix or '/'}) failed: {exc}")
            continue
        for f in tree:
            if not isinstance(f, RepoFile) or f.path in seen or not _match(f.path, patterns):
                continue
            seen.add(f.path)
            rec = {"path": f.path, "size": f.size, "git_blob_id": f.blob_id, "sha256": None, "sha256_origin": None}
            if f.lfs is not None:
                rec["sha256"], rec["sha256_origin"] = f.lfs.sha256, "hub_lfs"
            elif fetch_small and f.path.lower().endswith(DATA_EXT) and (f.size or 0) <= SMALL_BYTES:
                try:
                    local = hf_hub_download(repo, f.path, repo_type=repo_type, revision=sha)
                    rec["sha256"], rec["sha256_origin"] = common.file_sha256(local), "downloaded"
                except Exception as exc:
                    notes.append(f"download {f.path} failed: {exc}")
            files.append(rec)
    files.sort(key=lambda r: r["path"])
    if patterns and not files:
        notes.append(f"no file matched {patterns}")
    return files, notes


def lock_hf(name: str, entry: dict, *, repo_type: str, fetch_small: bool) -> dict:
    from huggingface_hub import HfApi
    api = HfApi()
    pin, ref = entry.get("revision"), entry.get("ref")
    sha, notes, status = _hf_resolve(api, entry["repo"], repo_type, pin, ref)
    out = {"kind": "hf_dataset" if repo_type == "dataset" else "hf_model", "repo": entry["repo"], "pin": pin,
           "ref": ref, "status": status, "resolved_sha": sha, "notes": notes}
    for k in ("config", "configs", "data_dir", "data_files", "streaming", "license", "release_tier", "commercial_ok"):
        if entry.get(k) is not None:
            out[k] = entry[k]
    if repo_type == "dataset":
        out["recipe"] = (entry.get("recipe") or "").replace("REV", f'"{sha}"' if sha else "<unresolved>")
    if sha:
        patterns = entry.get("files") if repo_type == "dataset" else MODEL_FILE_GLOBS
        files, fnotes = _hf_files(api, entry["repo"], repo_type, sha, patterns, fetch_small and repo_type == "dataset")
        out["files"], out["notes"] = files, notes + fnotes
        out["n_files"] = len(files)
        out["total_bytes"] = sum(f["size"] or 0 for f in files)
    return out


# ------------------------------------------------------------------------------------------------------------------
# GitHub
# ------------------------------------------------------------------------------------------------------------------
def _gh_get(url: str):
    import requests
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    for attempt in range(3):
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code in (502, 503, 504):
            time.sleep(2 * (attempt + 1))
            continue
        return r
    return r


def lock_github(name: str, entry: dict) -> dict:
    repo, pin = entry["repo"], entry.get("revision")
    out = {"kind": "github", "repo": repo, "pin": pin, "status": "unresolved", "resolved_sha": None, "notes": [],
           "license": entry.get("license"), "release_tier": entry.get("release_tier"),
           "commercial_ok": entry.get("commercial_ok")}
    sha = None
    r = _gh_get(f"https://api.github.com/repos/{repo}/commits/{pin or 'HEAD'}")
    if r.status_code == 200:
        j = r.json()
        sha = j["sha"]
        out["commit_date"] = j.get("commit", {}).get("committer", {}).get("date")
        if pin and not sha.startswith(pin):
            out["notes"].append(f"GitHub returned {sha} for pin {pin}")
            sha = None
        elif not pin:
            out["notes"].append("no pin in DESIGN/config; recorded the default-branch head")
    else:
        msg = f"commits API {r.status_code}: {r.text[:160]}"
        if pin and common.FULL_SHA.match(pin) and entry.get("files") and not any(ch in "".join(entry["files"]) for ch in "*?["):
            sha = pin
            out["notes"].append(msg + "; commit verified by downloading the listed files at the pinned sha")
            out["verified_by"] = "raw_download"
        else:
            out["notes"].append(msg)
    if sha is None:
        return out
    out["resolved_sha"] = sha
    patterns = entry.get("files")
    paths: list[str] = []
    if patterns:
        if any(ch in "".join(patterns) for ch in "*?["):
            t = _gh_get(f"https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1")
            if t.status_code != 200:
                out["notes"].append(f"trees API {t.status_code}; globs not expanded")
                out["status"] = "unresolved"
                return out
            tree = [x["path"] for x in t.json().get("tree", []) if x.get("type") == "blob"]
            if t.json().get("truncated"):
                out["notes"].append("git tree listing truncated")
            paths = sorted(p for p in tree if _match(p, patterns))
        else:
            paths = list(patterns)
    files = []
    for p in paths:
        try:
            local = common.github_file(repo, sha, p, expect_sha256=None)
            files.append({"path": p, "size": local.stat().st_size, "sha256": common.file_sha256(local),
                          "sha256_origin": "downloaded"})
        except Exception as exc:
            files.append({"path": p, "size": None, "sha256": None, "sha256_origin": None})
            out["notes"].append(f"download {p} failed: {exc}")
    out["files"] = files
    out["n_files"] = len(files)
    out["cache_dir"] = str(common.github_cache_path(repo, sha, ""))
    out["recipe"] = (entry.get("recipe") or "").replace("REV", f'"{sha}"')
    failed = [f["path"] for f in files if f["sha256"] is None]
    if patterns and not files:
        out["notes"].append(f"no file matched {patterns}")
    out["status"] = "resolved" if not failed and (files or not patterns) else "unresolved"
    return out


# ------------------------------------------------------------------------------------------------------------------
# URL
# ------------------------------------------------------------------------------------------------------------------
def lock_url(name: str, entry: dict) -> dict:
    import requests
    out = {"kind": "url", "url": entry["url"], "status": "unresolved", "notes": [],
           "license": entry.get("license"), "release_tier": entry.get("release_tier")}
    try:
        r = requests.get(entry["url"], timeout=30)
        r.raise_for_status()
    except Exception as exc:
        out["notes"].append(f"fetch failed: {exc}")
        return out
    digest = hashlib.sha256(r.content).hexdigest()
    URL_CACHE.mkdir(parents=True, exist_ok=True)
    local = URL_CACHE / f"{digest}{Path(entry['url']).suffix or '.txt'}"
    if not local.exists():
        local.write_bytes(r.content)
    out.update({"status": "resolved", "sha256": digest, "size": len(r.content), "cache_path": str(local),
                "fetched_on": datetime.date.today().isoformat(),
                "notes": ["vendor page; content may change: the anchor step must compare against this sha256"]})
    return out


# ------------------------------------------------------------------------------------------------------------------
def run(args, log):
    cf = common.load_config()
    only = set(args.only.split(",")) if args.only else None
    jobs = []
    for name, entry in cf["sources"].items():
        if only and name not in only:
            continue
        kind = entry["kind"]
        if kind == "hf_dataset":
            jobs.append(("sources", name, lambda n=name, e=entry: lock_hf(n, e, repo_type="dataset", fetch_small=not args.no_fetch)))
        elif kind == "github":
            jobs.append(("sources", name, lambda n=name, e=entry: lock_github(n, e)))
        elif kind == "url":
            jobs.append(("sources", name, lambda n=name, e=entry: lock_url(n, e)))
        else:
            log.warning("sources.%s: unknown kind %r", name, kind)
    for name, entry in cf["models"].items():
        if only and name not in only:
            continue
        jobs.append(("models", name, lambda n=name, e=entry: lock_hf(n, e, repo_type="model", fetch_small=False)))

    def _do(job):
        section, name, fn = job
        t0 = time.time()
        try:
            res = fn()
        except Exception as exc:  # record and continue
            res = {"status": "unresolved", "notes": [f"{type(exc).__name__}: {exc}"]}
        res["seconds"] = round(time.time() - t0, 1)
        return section, name, res

    results = {"sources": {}, "models": {}}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for section, name, res in pool.map(_do, jobs):
            results[section][name] = res
            lvl = log.info if res.get("status") == "resolved" else log.warning
            lvl("%s.%s: %s %s %s", section, name, res.get("status"), res.get("resolved_sha") or res.get("sha256") or "",
                "; ".join(res.get("notes", []))[:300])
            res.pop("seconds", None)

    lock = common.load_lock() if only else {}
    lock.setdefault("sources", {})
    lock.setdefault("models", {})
    for section in ("sources", "models"):
        lock[section].update(results[section])
    unresolved = sorted(f"{s}.{n}" for s in ("sources", "models") for n, r in lock[s].items() if r.get("status") != "resolved")
    moved = sorted(f"{s}.{n}" for s in ("sources", "models") for n, r in lock[s].items()
                   if any("head is now" in x or "found in the history" in x for x in r.get("notes", [])))
    lock.update({
        "lock_version": 1,
        "generated_by": "build/steps/s01_lock.py",
        "authored_by": common.AUTHORED_BY,
        "resolved_on": datetime.date.today().isoformat(),
        "master_seed": common.master_seed(),
        "config_sha256": common.config_sha256(),
        "hf_cache": str(common.HF_HOME),
        "github_cache": str(common.GITHUB_CACHE),
        "summary": {"n_sources": len(lock["sources"]), "n_models": len(lock["models"]),
                    "n_resolved": sum(1 for s in ("sources", "models") for r in lock[s].values() if r.get("status") == "resolved"),
                    "unresolved": unresolved, "pin_not_ref_head": moved},
    })
    out = common.write_json(common.LOCK_PATH, lock)
    log.info("wrote %s: %d resolved, %d unresolved %s", out["path"], lock["summary"]["n_resolved"], len(unresolved), unresolved)
    return {"outputs": [out["path"]], "partial": bool(only),
            "info": {"unresolved": unresolved, "n_resolved": lock["summary"]["n_resolved"]}}


if __name__ == "__main__":
    ap = common.step_argparser(__doc__.splitlines()[0])
    ap.add_argument("--only", default=None, help="comma-separated source/model names to (re)lock; others are kept")
    ap.add_argument("--no-fetch", action="store_true", help="do not download small non-LFS data files")
    ap.add_argument("--workers", type=int, default=6)
    sys.exit(common.step_main(STEP, __file__, run, parser=ap))
