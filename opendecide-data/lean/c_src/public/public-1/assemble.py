#!/usr/bin/env python3
"""public-1 assembly.

  stage : read tmp/cand_<ds>.json, uniform gold position per (dataset, part, k), fill meta.git_sha, validate every row
          (2.4 keys, gold, tokens <= 7,900, no jev* key, unique ids, exact-duplicate texts, train/dev group separation),
          write tmp/stage_{main,reserve,dev}.jsonl and tmp/stage_templates.jsonl.
  final : read the sealed checker's id-only outputs for the staged files; drop every hit (a twin pair drops whole);
          refill main from the same dataset x framing reserve (pairs for pairs); write out/ files and the manifest.

There is no override: a template hit fails `final` (the template must be rewritten and everything rebuilt).
v1.1: each row's authored card text (common.make_row `_card`) is moved to tmp/row_cards.json at stage (G15 must_show
for qc_fix.py; choice-row cards are in instructions); row lengths are real-tokenizer lengths of the full chat prompt
(common.real_tokens), recorded per row in tmp/real_tokens.json.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common import TMP, OUT, LOGS, SEED, real_tokens, sha, write_jsonl, MAX_ROW_TOKENS, LONG_TOKENS  # noqa: E402
from textnorm import norm  # noqa: E402
import pools as P  # noqa: E402

KEYS = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card", "meta"]
DATASETS = ["squad2", "musique", "2wiki", "quality", "qasper"]
TARGET_R1 = {"squad2": 900, "musique": 1000, "2wiki": 600, "quality": 600, "qasper": 350}
PARTS = ("main", "reserve", "dev")


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
    """Place gold at positions cycling 0..k-1 inside each (dataset, framing, k) bucket (G10: uniform gold letter)."""
    cnt = Counter()
    for r in rows:
        if r["qtype"] != "choice":
            continue
        k = len(r["options"])
        key = (r["source"], framing(r), k, part)
        pos = cnt[key] % k
        cnt[key] += 1
        opts = list(r["options"])
        g = opts.index(r["gold"])
        opts[g], opts[pos] = opts[pos], opts[g]
        r["options"] = opts


REAL = {}


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
        t = real_tokens(r)
        REAL[r["id"]] = t
        assert t <= MAX_ROW_TOKENS, (r["id"], t)
        st[f"{part}_long_rows"] += t >= LONG_TOKENS
        st[f"{part}_tokens"] += t


def stage():
    st = Counter()
    head, csha = repo_head(), code_sha()
    allrows = {p: [] for p in PARTS}
    cards = {}
    present = []
    for ds in DATASETS:
        f = TMP / f"cand_{ds}.json"
        if not f.exists():
            continue
        present.append(ds)
        d = json.loads(f.read_text())
        for p in PARTS:
            for r in d[p]:
                cards[r["id"]] = r.pop("_card")
                r["meta"]["git_sha"] = f"repo HEAD {head}; public-1 code sha256 {csha[:16]} (uncommitted builder)"
                r["meta"]["c_part"] = {"main": "train_r1", "reserve": "train_r1_reserve", "dev": "mix_tuning_dev"}[p]
            uniform_gold(d[p], p)
            allrows[p] += d[p]
    ids = Counter(r["id"] for p in PARTS for r in allrows[p])
    assert max(ids.values()) == 1, "duplicate ids"
    texts = Counter(sha(norm(r["state"]) + "|" + norm(r["instructions"]) + "|" + "|".join(r["options"] or []))
                    for p in PARTS for r in allrows[p])
    assert max(texts.values()) == 1, "exact duplicate row text"
    tr_groups = {r["group_id"] for p in ("main", "reserve") for r in allrows[p]}
    dv_groups = {r["group_id"] for r in allrows["dev"]}
    assert not tr_groups & dv_groups, "train/dev group overlap"
    (TMP / "row_cards.json").write_text(json.dumps(cards, ensure_ascii=False))
    st["carded_rows"] = sum(1 for v in cards.values() if v)
    for p in PARTS:
        validate(allrows[p], p, st)
        st[f"{p}_rows"] = write_jsonl(TMP / f"stage_{p}.jsonl", allrows[p]) and len(allrows[p])
    (TMP / "real_tokens.json").write_text(json.dumps(REAL))
    tmpl = P.all_pool_objects()
    write_jsonl(TMP / "stage_templates.jsonl", tmpl)
    st["templates"] = len(tmpl)
    st["datasets"] = present
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


def final(args):
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
        raise SystemExit("template hit: rewrite the template(s) and rebuild (ids: %s)" % sorted(
            k for k in hits if ":" in k))
    def drop_hits(rs):
        bad = {r["id"] for r in rs if r["id"] in hits}
        bad |= {r["meta"]["twin_of"] for r in rs if r["id"] in bad and r["meta"].get("twin_of")}
        return [r for r in rs if r["id"] not in bad], bad
    main, bad_m = drop_hits(rows["main"])
    res, bad_r = drop_hits(rows["reserve"])
    dev, bad_d = drop_hits(rows["dev"])
    st["dropped_main"], st["dropped_reserve"], st["dropped_dev"] = len(bad_m), len(bad_r), len(bad_d)
    # refill main from reserve: same source x framing, same unit size (twin pairs replace pairs)
    need = Counter((r["source"], framing(r)) for r in rows["main"] if r["id"] in bad_m)
    by_id = {r["id"]: r for r in res}
    used = set()
    for (src, fr), n in need.items():
        got = 0
        for r in res:
            if got >= n:
                break
            if r["id"] in used or r["source"] != src or framing(r) != fr:
                continue
            unit = [r] + ([by_id[r["meta"]["twin_of"]]] if r["meta"].get("twin_of") in by_id else [])
            if got + len(unit) > n:
                continue
            for u in unit:
                used.add(u["id"])
                u["meta"]["c_part"] = "train_r1"
                main.append(u)
            got += len(unit)
        st[f"refill_{src}_{fr}"] = got
        assert got == n, f"reserve too small for {src} {fr}: need {n}, got {got}"
    res = [r for r in res if r["id"] not in used]
    uniform_gold(main, "main")
    uniform_gold(res, "reserve")
    OUT.mkdir(exist_ok=True)
    files = {}
    for name, rs in (("public1_rows_r1.jsonl", main), ("public1_reserve.jsonl", res), ("public1_mtdev.jsonl", dev)):
        files[name] = {"sha256": write_jsonl(OUT / name, rs), "rows": len(rs)}
    cards = json.loads((TMP / "row_cards.json").read_text())
    keep = {r["id"] for rs in (main, res, dev) for r in rs}
    (LOGS / "row_cards_final.json").write_text(json.dumps({k: v for k, v in cards.items() if k in keep},
                                                          ensure_ascii=False))
    tmpl = [json.loads(l) for l in open(TMP / "stage_templates.jsonl")]
    files["public1_templates.jsonl"] = {"sha256": write_jsonl(OUT / "public1_templates.jsonl", tmpl), "rows": len(tmpl)}
    (LOGS / "final_stats.json").write_text(json.dumps(st, indent=1))
    (LOGS / "final_files.json").write_text(json.dumps(files, indent=1))
    print(json.dumps({"stats": st, "files": files}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stage", "final"])
    a = ap.parse_args()
    stage() if a.cmd == "stage" else final(a)
