"""Fetch + extract CommitPackFT (G0 1.1 steps 1, 3, 5; raw deleted after each language file).

Usage: python gen/fetch_pf.py LANG [LANG ...]   (CommitPackFT data/<lang>/data.jsonl)
Per sample: licence filter (mit, apache-2.0, bsd-2/3, isc, cc0-1.0, unlicense), repo and content guards, files of
<= 5,000 lines, diff by `git diff --no-index --minimal` (Myers minimal, 3-line context, no whitespace options, no
rename detection), count derivation A = LCS dynamic program (added = |new| - LCS, removed = |old| - LCS); derivation B
(parse of the git diff text) runs in the build and must agree. Diff PII classes drop the sample.
Writes gen/data/pf_records_<lang>.jsonl.gz and gen/data/fetch_pf_<lang>.json.
"""
from __future__ import annotations

import collections
import gzip
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

RES = "https://huggingface.co/datasets/bigcode/commitpackft/resolve/main/data/{lang}/data.jsonl"
TARGET = 1600          # sampled candidates per language file (hash-rate draw, fixed seed)
MAX_LINES = 5000
LCS_BUDGET = 4_000_000
RAW = C.TMP / "raw"


def lcs_counts(a: list[str], b: list[str]):
    """Derivation A: own LCS dynamic program (common prefix/suffix stripped first)."""
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    j = 0
    while j < len(a) - i and j < len(b) - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
        j += 1
    ma, mb = a[i:len(a) - j], b[i:len(b) - j]
    if len(ma) * len(mb) > LCS_BUDGET:
        return None
    prev = [0] * (len(mb) + 1)
    for x in ma:
        cur = [0] * (len(mb) + 1)
        for k, y in enumerate(mb, 1):
            cur[k] = prev[k - 1] + 1 if x == y else (prev[k] if prev[k] >= cur[k - 1] else cur[k - 1])
        prev = cur
    lcs = i + j + prev[-1]
    return len(b) - lcs, len(a) - lcs


def git_diff(old: str, new: str) -> str:
    with tempfile.TemporaryDirectory(dir=str(RAW)) as td:
        pa, pb = os.path.join(td, "a"), os.path.join(td, "b")
        open(pa, "w").write(old)
        open(pb, "w").write(new)
        p = subprocess.run(["git", "-c", "core.quotepath=off", "diff", "--no-index", "--minimal", "--no-color",
                            "--no-ext-diff", "-U3", "a", "b"], cwd=td, capture_output=True, text=True)
        if p.returncode not in (0, 1):
            raise RuntimeError(p.stderr[:200])
        out = p.stdout
    k = out.find("\n@@")
    return out[k + 1:] if k >= 0 else ""


def lines_of(s: str) -> list[str]:
    return s.split("\n")[:-1] if s.endswith("\n") else (s.split("\n") if s else [])


def run(lang: str) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    C.DATA.mkdir(parents=True, exist_ok=True)
    safe = lang.replace("+", "p")
    local = RAW / f"pf_{safe}.jsonl"
    if not local.exists() or local.stat().st_size < 1000:
        subprocess.run(["curl", "-sL", "-o", str(local), RES.format(lang=lang)], check=True)
    import re
    hdr_re = re.compile(r"^(feat|fix|docs|refactor|perf|test|build|ci|chore|revert)(\([^():\n]+\))?!?: +\S", re.I)
    n, rstat = 0, collections.defaultdict(lambda: [0, 0])
    for line in open(local):
        r = json.loads(line)
        n += 1
        rp = (r.get("repos") or "").split(",")[0].strip()
        rstat[rp][0] += 1
        rstat[rp][1] += bool(hdr_re.match(r.get("message") or ""))
    conv = {k for k, (a, b) in rstat.items() if a >= 10 and b >= 0.8 * a}
    rate = min(1.0, TARGET / max(n, 1))
    drops = collections.Counter()
    kept = 0
    with gzip.open(C.DATA / f"pf_records_{safe}.jsonl.gz", "wt") as fo:
        for line in open(local):
            r = json.loads(line)
            rp0 = (r.get("repos") or "").split(",")[0].strip()
            if C.h01("pfpick", r["commit"], r.get("repos", "")) >= rate and rp0 not in conv:
                continue
            lic = C.LIC_PF.get((r.get("license") or "").lower())
            if lic is None:
                drops["licence"] += 1
                continue
            repos = [x.strip() for x in (r.get("repos") or "").split(",") if x.strip()]
            if not repos or any(C.repo_guard(x) for x in repos):
                drops["guard_repo_name"] += 1
                continue
            old, new = r.get("old_contents") or "", r.get("new_contents") or ""
            la, lb = lines_of(old), lines_of(new)
            if len(la) > MAX_LINES or len(lb) > MAX_LINES:
                drops["file_lines"] += 1
                continue
            if "\x00" in old or "\x00" in new:
                drops["binary"] += 1
                continue
            try:
                diff = git_diff(old, new)
            except Exception:
                drops["diff_error"] += 1
                continue
            if not diff:
                drops["empty_diff"] += 1
                continue
            msg = r.get("message") or r.get("subject") or ""
            of, nf = r.get("old_file") or "", r.get("new_file") or ""
            why = C.content_guard("\n".join([msg, of, nf, diff])) or C.content_guard(",".join(repos))
            if why:
                drops[why] += 1
                continue
            hdr = f"--- a/{of}\n+++ b/{nf}\n"
            why = C.diff_pii(hdr + diff)
            if why:
                drops[why] += 1
                continue
            cnt = lcs_counts(la, lb)
            if cnt is None:
                drops["lcs_budget"] += 1
                continue
            ct = "ADD" if not old and new else "DELETE" if old and not new else ("RENAME" if of != nf else "MODIFY")
            rec = {"rid": "pf_" + C.sha256(r["commit"] + "@" + repos[0])[:16], "ds": "CommitPackFT", "repo": repos[0],
                   "repos": repos, "date": None, "repo_lang": r.get("lang"), "repo_licence": lic, "msg_raw": msg,
                   "files": [{"ct": ct, "old": of if ct != "ADD" else None, "new": nf if ct != "DELETE" else None,
                              "diff": diff, "a_added": cnt[0], "a_removed": cnt[1]}]}
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
    rep = {"lang": lang, "rows": n, "rate": rate, "kept": kept, "conv_repos": len(conv), "drops": dict(drops),
           "repo_stats": {k: v for k, v in rstat.items() if v[1] >= 3}}
    json.dump(rep, open(C.DATA / f"fetch_pf_{safe}.json", "w"), indent=1)
    local.unlink()
    print(json.dumps({k: v for k, v in rep.items() if k not in ("drops", "repo_stats")}), flush=True)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        run(a)
    print("FETCH_PF_DONE", flush=True)
