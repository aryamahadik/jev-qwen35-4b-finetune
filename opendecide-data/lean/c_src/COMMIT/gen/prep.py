"""COMMIT prep: records -> eligible pool, repo groups, area schemas (G0 2.1), triage-eligible groups (3.1),
30 held-out repo groups (1.1 step 4). Writes gen/data/pool.jsonl.gz (one normalised record per line, with
`split` = "train" | "heldout"), gen/data/groups.json and gen/data/prep_report.json. Prints counts only.

Run:  python gen/prep.py        (after fetch_cc.py / fetch_pf.py finished; > 2 min: run in the background)
"""
from __future__ import annotations

import collections
import glob
import gzip
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import records as R  # noqa: E402

POOL_CAP_PER_GROUP = 400   # fixed-seed cap per repo group in the pool (each group <= 3% of rows anyway)
M_AREA = 20            # <m_area>: files a folder needs to be an area (2.1)
HDR = re.compile(r"^(feat|fix|docs|refactor|perf|test|build|ci|chore|revert)(\([^():\n]+\))?!?: +\S")


def load_proxy() -> dict:
    """repo -> sorted [[date, [paths]], ...] over every CommitChronicle train commit of the repo (1.2 tree proxy)."""
    out = {}
    for fn in sorted(glob.glob(str(C.DATA / "cc_proxy_*.jsonl.gz"))):
        with gzip.open(fn, "rt") as f:
            for line in f:
                d = json.loads(line)
                out.setdefault(d["repo"], []).extend(d["commits"])
    for v in out.values():
        v.sort()
    return out


def area_schema(paths: set[str]) -> dict | None:
    """2.1: top-level folders with >= M_AREA files; monorepo shift once if >= 80% of files sit under one folder P."""
    files = [p for p in paths if p]
    if not files:
        return None
    top = collections.Counter(p.split("/")[0] for p in files if "/" in p)
    shift = None
    if top:
        P, nP = top.most_common(1)[0]
        if nP >= 0.8 * len(files):
            shift = P
    areas = {}
    if shift:
        sub = collections.Counter(p.split("/")[1] for p in files if p.startswith(shift + "/") and p.count("/") >= 2)
        for name, n in sub.items():
            if n >= M_AREA:
                areas[name] = shift + "/" + name + "/"
        for name, n in top.items():
            if name != shift and n >= M_AREA:
                areas[name] = name + "/"
    else:
        for name, n in top.items():
            if n >= M_AREA:
                areas[name] = name + "/"
    # distinct-name lint (R3-06): case-insensitive equal names or equal non-empty token sets -> no route card
    seen, toks = set(), {}
    for name in areas:
        low = name.lower()
        ts = frozenset(C.m_tokens(name))
        if low in seen or (ts and ts in toks.values()):
            return {"areas": areas, "shift": shift, "lint_ok": False}
        seen.add(low)
        toks[name] = ts
    return {"areas": areas, "shift": shift, "lint_ok": True}


MAX_FILES = 30          # builder tightening: records above these sizes cannot fit the 1,999-token row cap
MAX_LINES = 3000


class _Lite(dict):
    """Light record view kept in memory (the full record is kept as its JSON string)."""


def load_records_lite(drops, scrub):
    """Streaming version of records.load_records: full records are kept as JSON strings (memory), dedup keeps the
    CommitChronicle copy (A51), repo groups by union-find (A51). Size filter (MAX_FILES, MAX_LINES) is gold-blind."""
    recs, seen = [], {}
    for raw in R.iter_raw():
        r = R.build_record(raw, drops, scrub)
        if r is None:
            continue
        if r["n_files"] > MAX_FILES or r["added"] + r["removed"] > MAX_LINES:
            drops["size_over_builder_cap"] += 1
            continue
        k = R.commit_key(r)
        lite = _Lite(rid=r["rid"], ds=r["ds"], repo=r["repo"], repos=r["repos"], msg_first=r["msg"].split("\n", 1)[0],
                     js=json.dumps(r, ensure_ascii=False))
        if k in seen:
            j = seen[k]
            if recs[j]["ds"] != "CommitChronicle" and r["ds"] == "CommitChronicle":
                recs[j] = lite
            drops["dup_commit_key"] += 1
            continue
        seen[k] = len(recs)
        recs.append(lite)
    keyrecs = [{"repos": x["repos"], "repo": x["repo"], "msg": json.loads(x["js"])["msg"],
                "files": [{"path": f["path"], "added": f["added"], "removed": f["removed"]}
                          for f in json.loads(x["js"])["files"]]} for x in recs]
    g = R.repo_groups(keyrecs)
    del keyrecs
    for x in recs:
        x["group"] = g[x["repo"].strip().lower()]
    return recs


def main() -> None:
    drops, scrub = collections.Counter(), {}
    recs = load_records_lite(drops, scrub)
    proxy = load_proxy()
    groups = collections.defaultdict(lambda: {"repos": set(), "n": collections.Counter(), "conv": 0, "all": 0})
    for r in recs:
        g = groups[r["group"]]
        g["repos"].add(r["repo"])
        g["n"][r["ds"]] += 1
        g["all"] += 1
        g["conv"] += bool(HDR.match(r["msg_first"]))
    ginfo = {}
    for gid, g in groups.items():
        cc_repos = sorted(x for x in g["repos"] if x in proxy)
        paths = {p for x in cc_repos for _, ps in proxy[x] for p in ps}
        sch = area_schema(paths) if cc_repos else None
        ginfo[gid] = {"repos": sorted(g["repos"]), "n": dict(g["n"]), "conv_share": round(g["conv"] / g["all"], 4),
                      "triage_eligible": g["all"] >= 30 and g["conv"] >= 0.8 * g["all"],
                      "route_eligible": bool(sch and sch["lint_ok"] and len(sch["areas"]) >= 4),
                      "areas": (sch or {}).get("areas"), "shift": (sch or {}).get("shift")}
    # held-out: 30 groups, fixed seed, from groups with >= N_MIN records; >= 8 triage- and >= 8 route-eligible
    cand = sorted((gid for gid, g in ginfo.items() if sum(g["n"].values()) >= R.N_MIN_HELDOUT),
                  key=lambda gid: C.h01(R.HELDOUT_SEED, gid))
    held = []
    for need in ("triage_eligible", "route_eligible"):
        for gid in cand:
            if sum(1 for h in held if ginfo[h][need]) >= 8:
                break
            if gid not in held and ginfo[gid][need]:
                held.append(gid)
    for gid in cand:
        if len(held) >= 30:
            break
        if gid not in held:
            held.append(gid)
    hs = set(held)
    n_split = collections.Counter()
    rank = collections.defaultdict(list)
    for i, r in enumerate(recs):
        rank[r["group"]].append((C.h01("poolcap", r["rid"]), i))
    keep = {i for lst in rank.values() for _, i in sorted(lst)[:POOL_CAP_PER_GROUP]}
    with gzip.open(C.DATA / "pool.jsonl.gz", "wt") as fo:
        for i, r in enumerate(recs):
            if i not in keep:
                n_split["pool_cap_dropped"] += 1
                continue
            full = json.loads(r["js"])
            full["group"] = r["group"]
            full["split"] = "heldout" if r["group"] in hs else "train"
            n_split[(full["split"], r["ds"])] += 1
            fo.write(json.dumps(full, ensure_ascii=False) + "\n")
    for gid in ginfo:
        ginfo[gid]["split"] = "heldout" if gid in hs else "train"
    json.dump({"seed": R.HELDOUT_SEED, "m_area": M_AREA, "heldout": held, "groups": ginfo},
              open(C.DATA / "groups.json", "w"), indent=0)
    rep = {"records": len(recs), "split": {(k if isinstance(k, str) else f"{k[0]}|{k[1]}"): v for k, v in n_split.items()}, "drops": dict(drops),
           "scrub": scrub, "groups": len(ginfo), "heldout": len(held),
           "heldout_triage": sum(ginfo[h]["triage_eligible"] for h in held),
           "heldout_route": sum(ginfo[h]["route_eligible"] for h in held),
           "train_triage_groups": sum(1 for g in ginfo.values() if g["split"] == "train" and g["triage_eligible"]),
           "train_route_groups": sum(1 for g in ginfo.values() if g["split"] == "train" and g["route_eligible"])}
    json.dump(rep, open(C.DATA / "prep_report.json", "w"), indent=1)
    print(json.dumps(rep)[:1500])


if __name__ == "__main__":
    main()
