"""Fetch + extract CommitChronicle train shards (G0 1.1 steps 1, 3, 5 partial; raw deleted after extraction).

Usage: python gen/fetch_cc.py SHARD [SHARD ...]
Writes gen/data/cc_records_<k>.jsonl.gz (eligible-candidate commits, compact), gen/data/cc_proxy_<k>.jsonl.gz
(every train commit of every kept repo: date + paths, for the dated tree proxy, G0 1.2) and
gen/data/fetch_cc_<k>.json (drop counts by reason). The raw parquet is deleted after each shard (disk rule).
"""
from __future__ import annotations

import collections
import datetime as dt
import gzip
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

API = "https://huggingface.co/api/datasets/JetBrains-Research/commit-chronicle/tree/main/data"
RES = "https://huggingface.co/datasets/JetBrains-Research/commit-chronicle/resolve/main/"
MAX_FILES = 30
MAX_DIFF_CHARS = 40000
PER_REPO_CAP = 1200
RAW = C.TMP / "raw"


def shard_paths() -> list[str]:
    out = subprocess.run(["curl", "-s", "-m", "60", API], capture_output=True, text=True, check=True).stdout
    return sorted(x["path"] for x in json.loads(out) if "/train-" in x["path"])


def iso(d: str) -> str:
    return dt.datetime.strptime(d, "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")


HDR = __import__("re").compile(r"^(feat|fix|docs|refactor|perf|test|build|ci|chore|revert)(\([^():\n]+\))?!?: +\S",
                                __import__("re").I)


def run(k: int, conv_only: bool = False) -> None:
    import pyarrow.parquet as pq
    RAW.mkdir(parents=True, exist_ok=True)
    C.DATA.mkdir(parents=True, exist_ok=True)
    path = shard_paths()[k]
    local = RAW / f"cc_train_{k:05d}.parquet"
    if not local.exists() or local.stat().st_size < 1000:
        subprocess.run(["curl", "-sL", "-o", str(local), RES + path], check=True)
    pf = pq.ParquetFile(str(local))
    tb = pf.read(columns=["repo", "original_message"])
    repos = tb.column("repo").to_pylist()
    n_repo = collections.Counter(repos)
    n_conv = collections.Counter(rp for rp, m in zip(repos, tb.column("original_message").to_pylist())
                                 if HDR.match(m or ""))
    conv = {rp for rp in n_repo if n_repo[rp] >= 30 and n_conv[rp] >= 0.8 * n_repo[rp]}
    del tb
    drops = collections.Counter()
    proxy = collections.defaultdict(list)
    kept = 0
    with gzip.open(C.DATA / f"cc_records_{k:05d}.jsonl.gz", "wt") as fo:
        for g in range(pf.metadata.num_row_groups):
            for r in pf.read_row_group(g).to_pylist():
                repo = r["repo"]
                if conv_only and repo not in conv:
                    continue
                if C.repo_guard(repo):
                    drops["guard_repo_name"] += 1
                    continue
                lic = C.LIC_CC.get(r["license"])
                if lic is None:
                    drops["licence"] += 1
                    continue
                mods = r["mods"] or []
                paths = sorted({p for m in mods for p in (m["old_path"], m["new_path"]) if p})
                date = iso(r["date"])
                proxy[repo].append([date, paths])
                rate = min(1.0, PER_REPO_CAP / n_repo[repo])
                if C.h01("ccpick", repo, r["hash"]) >= rate:
                    drops["per_repo_cap"] += 1
                    continue
                if not mods or len(mods) > MAX_FILES:
                    drops["n_files"] += 1
                    continue
                dsize = sum(len(m["diff"] or "") for m in mods)
                if dsize > MAX_DIFF_CHARS:
                    drops["diff_size"] += 1
                    continue
                msg = r["original_message"] or r["message"] or ""
                blob = "\n".join([msg] + paths + [m["diff"] or "" for m in mods])
                why = C.content_guard(blob) or C.content_guard(repo)
                if why:
                    drops[why] += 1
                    continue
                why = C.diff_pii("\n".join(m["diff"] or "" for m in mods))
                if why:
                    drops[why] += 1
                    continue
                rec = {"rid": "cc_" + C.sha256(repo + "@" + r["hash"])[:16], "ds": "CommitChronicle", "repo": repo,
                       "date": date, "repo_lang": r["language"], "repo_licence": lic, "msg_raw": msg,
                       "files": [{"ct": m["change_type"], "old": m["old_path"], "new": m["new_path"],
                                  "diff": m["diff"] or ""} for m in mods]}
                fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
                kept += 1
    with gzip.open(C.DATA / f"cc_proxy_{k:05d}.jsonl.gz", "wt") as fo:
        for repo, lst in sorted(proxy.items()):
            lst.sort()
            fo.write(json.dumps({"repo": repo, "commits": lst}, ensure_ascii=False) + "\n")
    rep = {"shard": k, "file": path, "mode": "conv_only" if conv_only else "full", "rows": len(repos),
           "repos": len(n_repo), "conv_repos": sorted(conv), "kept": kept, "drops": dict(drops),
           "repo_stats": {rp: [n_repo[rp], n_conv[rp]] for rp in n_repo}}
    json.dump(rep, open(C.DATA / f"fetch_cc_{k:05d}.json", "w"), indent=1)
    local.unlink()
    print(json.dumps({k2: (len(v) if k2 == "conv_repos" else v) for k2, v in rep.items()
                      if k2 not in ("drops", "repo_stats")}), flush=True)


if __name__ == "__main__":
    conv_only = "--conv" in sys.argv
    for a in sys.argv[1:]:
        if a.startswith("--"):
            continue
        run(int(a), conv_only)
    print("FETCH_CC_DONE", flush=True)
