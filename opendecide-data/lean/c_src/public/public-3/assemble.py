#!/usr/bin/env python3
"""public-3 assembly.

  stage : read tmp/cand_<ds>.json; place gold so its position is uniform inside every (dataset, framing, k, part,
          gold class) cell with a keyed start (no position-class link); fill meta.git_sha and meta.c_part; validate
          every row (2.4 keys, gold, role, tokens <= 7,900, no jev* key, unique ids, exact-duplicate texts, train/dev
          group and record separation, one group per record, one record per normalized text); write
          tmp/stage_{main,reserve,dev}.jsonl and tmp/stage_templates.jsonl.
  final : read the sealed checker's id-only outputs for the staged files; drop every hit (a twin pair drops whole);
          refill main from the same dataset x framing x unit-size x label-signature reserve; write out/ files.

There is no override: a template hit fails `final` (the template must be rewritten and everything rebuilt).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common3 import LONG_TOKENS, LOGS, MAX_ROW_TOKENS, OUT, TMP, loose_text, row_tokens, sha, write_jsonl  # noqa: E402
import pools as P  # noqa: E402

KEYS = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card", "meta"]
# v2.0 (repair r1): GHC dropped by the spec 8 G5 dataset-level rule (build_rows.DROPPED); its 350 r1 rows go to F11
DATASETS = ["xed", "mams", "sarcasm", "edos"]
TARGET_R1 = {"xed": 600, "mams": 750, "sarcasm": 350, "edos": 350}
PARTS = ("main", "reserve", "dev")
TEXT_OPTION_FRAMINGS = {("c_pub_sarcasm", "ch"), ("c_pub_mams", "atsawh")}
# v1.1: format styles whose state is a JSON object (every such state must parse: review-public3 fix 1)
JSON_STYLES = {st["id"] for pool in (P.XED_STYLES, P.MAMS_STYLES, P.SAR_STYLES, P.POST_STYLES) for st in pool
               if st["wrap"].lstrip().startswith("{")}


def code_sha() -> str:
    h = hashlib.sha256()
    for p in sorted(list(HERE.glob("*.py")) + list((HERE / "lib").glob("*.py"))):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def repo_head() -> str:
    try:
        return subprocess.check_output(["git", "-C", str(HERE), "rev-parse", "HEAD"], text=True).strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def framing(r):
    return r["id"].split("-")[2]


def uniform_gold(rows, part):
    """v2.0: rows of a matched set (meta.match_set) keep the set's one option order, in which every position is gold
    exactly once; every other choice row gets the keyed cyclic gold position of its cell."""
    cnt = Counter()
    for r in rows:
        if r["qtype"] != "choice" or r["meta"].get("match_set"):
            continue
        k = len(r["options"])
        cls = "*" if (r["source"], framing(r)) in TEXT_OPTION_FRAMINGS else r["gold"]
        key = (r["source"], framing(r), k, part, cls)
        start = int(sha("|".join(map(str, key)))[:6], 16) % k
        pos = (start + cnt[key]) % k
        cnt[key] += 1
        opts = [o for o in r["options"] if o != r["gold"]]
        opts.insert(pos, r["gold"])
        r["options"] = opts


def records_of(r):
    u = r["meta"]["record_uid"]
    return u if isinstance(u, list) else [u]


def validate(rows, part, st):
    for r in rows:
        assert list(r.keys()) == KEYS, (r["id"], list(r.keys()))
        assert not any(k.lower().startswith("jev") for k in r) and not any(k.lower().startswith("jev") for k in r["meta"])
        if r["qtype"] == "noul":
            assert r["options"] is None and r["gold"] in (0, 1) and r["role"] in ("aff", "neg")
        else:
            assert r["qtype"] == "choice" and r["gold"] in r["options"] and r["role"] == "choice"
            assert 2 <= len(r["options"]) <= 60 and len(set(r["options"])) == len(r["options"])
        assert r["meta"]["text_source"]["split"] == "train"
        if r["meta"]["format_style"] in JSON_STYLES:
            json.loads(r["state"])                       # raises on an invalid JSON state
            st["json_state_rows"] += 1
        if r["qtype"] == "choice":                       # v1.1: only '- {option}: {def}' card lines on choice rows
            for ln in (r["card"].split("\n") if r["card"] else []):
                assert ln.startswith("- ") and ln[2:].split(": ", 1)[0] in r["options"], (r["id"], "hidden card line")
        st[f"{part}_card_render:{r['meta']['card_render']}"] += 1
        assert r["meta"].get("teacher") is None and r["meta"].get("option_level") is None
        t = row_tokens(r)
        assert t <= MAX_ROW_TOKENS, (r["id"], t)
        st[f"{part}_long_rows"] += t >= LONG_TOKENS
        st[f"{part}_tokens"] += t
        st[f"{part}_max_tokens"] = max(st[f"{part}_max_tokens"], t)


def stage():
    st = Counter()
    head, csha = repo_head(), code_sha()
    allrows = {p: [] for p in PARTS}
    for ds in DATASETS:
        d = json.loads((TMP / f"cand_{ds}.json").read_text())
        for p in PARTS:
            for r in d[p]:
                r["meta"]["git_sha"] = f"repo HEAD {head}; public-3 code sha256 {csha[:16]} (uncommitted builder)"
                r["meta"]["c_part"] = {"main": "train_r1", "reserve": "train_r1_reserve", "dev": "mix_tuning_dev"}[p]
            uniform_gold(d[p], p)
            allrows[p] += d[p]
    ids = Counter(r["id"] for p in PARTS for r in allrows[p])
    assert max(ids.values()) == 1, "duplicate ids"
    texts = Counter(sha(loose_text(r["state"]) + "|" + loose_text(r["instructions"]) + "|" + "|".join(r["options"] or []))
                    for p in PARTS for r in allrows[p])
    assert max(texts.values()) == 1, "exact duplicate row text"
    tr_groups = {r["group_id"] for p in ("main", "reserve") for r in allrows[p]}
    dv_groups = {r["group_id"] for r in allrows["dev"]}
    assert not tr_groups & dv_groups, "train/dev group overlap"
    rec_group = defaultdict(set)
    for p in PARTS:
        for r in allrows[p]:
            for x in records_of(r):
                rec_group[x].add(r["group_id"])
    assert all(len(v) == 1 for v in rec_group.values()), "a record is used by more than one group"
    st["records_used"] = len(rec_group)
    for p in PARTS:
        validate(allrows[p], p, st)
        write_jsonl(TMP / f"stage_{p}.jsonl", allrows[p])
        st[f"{p}_rows"] = len(allrows[p])
    tmpl = P.all_pool_objects()
    write_jsonl(TMP / "stage_templates.jsonl", tmpl)
    st["templates"] = len(tmpl)
    (LOGS / "stage_stats.json").write_text(json.dumps(st, indent=1, default=str))
    print(json.dumps(st, indent=1, default=str))


def read_hits(path: Path):
    hits = {}
    with open(path) as f:
        for line in f:
            o = json.loads(line)
            if o.get("hit"):
                hits[o["id"]] = o.get("hit_kinds", [])
    return hits


def units_of(rows):
    """Drop / refill units: a v2.0 matched set (meta.match_set) whole, else a twin pair, else a single row."""
    by_id = {r["id"]: r for r in rows}
    sets = defaultdict(list)
    for r in rows:
        if r["meta"].get("match_set"):
            sets[r["meta"]["match_set"]].append(r)
    seen, units = set(), []
    for r in rows:
        if r["id"] in seen:
            continue
        if r["meta"].get("match_set"):
            u = sets[r["meta"]["match_set"]]
        else:
            u = [r] + ([by_id[r["meta"]["twin_of"]]] if r["meta"].get("twin_of") in by_id else [])
        for x in u:
            seen.add(x["id"])
        units.append(u)
    return units


def sig(unit):
    out = []
    for r in unit:
        if r["qtype"] == "noul":
            out.append(("yn", r["meta"].get("asked") if len(unit) == 1 and "asked" in r["meta"] else "",
                        r["meta"].get("predicate_holds")))
        else:
            cls = "*" if (r["source"], framing(r)) in TEXT_OPTION_FRAMINGS else r["gold"]
            out.append(("ch", len(r["options"]), cls))
    return tuple(sorted(map(str, out)))


def final(_args):
    st = Counter()
    rows = {p: [json.loads(l) for l in open(TMP / f"stage_{p}.jsonl")] for p in PARTS}
    hits = {}
    for p in PARTS + ("templates",):
        q = TMP / f"stage_{p}.sealedqc.jsonl"
        assert q.exists(), f"run the sealed checker on tmp/stage_{p}.jsonl first ({q.name} missing)"
        h = read_hits(q)
        st[f"sealed_hits_{p}"] = len(h)
        st.update(Counter(f"sealed_hit_kind_{p}:{k['kind'] if isinstance(k, dict) else k}" for v in h.values() for k in v))
        hits.update(h)
    if st["sealed_hits_templates"]:
        raise SystemExit("template hit: rewrite the template(s) and rebuild")

    def drop_hits(rs):
        keep, bad = [], []
        for u in units_of(rs):
            (bad if any(x["id"] in hits for x in u) else keep).append(u)
        return keep, bad

    main_u, bad_m = drop_hits(rows["main"])
    res_u, bad_r = drop_hits(rows["reserve"])
    dev_u, bad_d = drop_hits(rows["dev"])
    st["dropped_main_rows"] = sum(map(len, bad_m))
    st["dropped_reserve_rows"] = sum(map(len, bad_r))
    st["dropped_dev_rows"] = sum(map(len, bad_d))
    st["dropped_dev_rows_not_refilled"] = st["dropped_dev_rows"]
    used = set()
    for u in bad_m:
        key = (u[0]["source"], framing(u[0]), len(u))
        cands = [v for v in res_u if id(v) not in used and (v[0]["source"], framing(v[0]), len(v)) == key]
        exact = [v for v in cands if sig(v) == sig(u)]
        pick = (exact or cands or [None])[0]
        if pick is None:
            raise SystemExit(f"reserve too small for {key}")
        st["refill_exact_signature" if exact else "refill_same_framing_only"] += 1
        used.add(id(pick))
        for x in pick:
            x["meta"]["c_part"] = "train_r1"
        main_u.append(pick)
    res_u = [v for v in res_u if id(v) not in used]
    main = [x for u in main_u for x in u]
    res = [x for u in res_u for x in u]
    dev = [x for u in dev_u for x in u]
    main.sort(key=lambda r: (DATASETS.index(r["source"][6:]), r["id"]))
    res.sort(key=lambda r: (DATASETS.index(r["source"][6:]), r["id"]))
    dev.sort(key=lambda r: (DATASETS.index(r["source"][6:]), r["id"]))
    uniform_gold(main, "main")
    uniform_gold(res, "reserve")
    uniform_gold(dev, "dev")
    cnt = Counter(r["source"] for r in main)
    for ds in DATASETS:
        assert cnt[f"c_pub_{ds}"] == TARGET_R1[ds], (ds, cnt[f"c_pub_{ds}"])
    files = {}
    for name, rs in (("public3_rows_r1.jsonl", main), ("public3_reserve.jsonl", res), ("public3_mtdev.jsonl", dev)):
        files[name] = {"sha256": write_jsonl(OUT / name, rs), "rows": len(rs)}
    tmpl = [json.loads(l) for l in open(TMP / "stage_templates.jsonl")]
    files["public3_templates.jsonl"] = {"sha256": write_jsonl(OUT / "public3_templates.jsonl", tmpl), "rows": len(tmpl)}
    (LOGS / "final_stats.json").write_text(json.dumps(st, indent=1))
    (LOGS / "final_files.json").write_text(json.dumps(files, indent=1))
    print(json.dumps({"stats": st, "files": files}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stage", "final"])
    a = ap.parse_args()
    stage() if a.cmd == "stage" else final(a)
