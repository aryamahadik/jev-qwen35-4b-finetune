#!/usr/bin/env python3
"""W8 finalize (PREREG_FINAL A40 addendum W8; A40 c steps 2-3; A40 ruling (ii) seeded cap).

Inputs (read only, all W8 files):
  opus_w8/chunk_NNN.json          blind Opus answers {qid, answer, confidence} (A40 c.2 queue and c.3 audit)
  opus_queue_w8/roles.json        qid -> role (queued / audit), queue reason, Haiku verdict
  opus_queue_w8/key.json          qid -> row id, type, gold (scoring only; never shown to a reader)
  candidates/w8_candidates.jsonl  the W8 rows (options, gold): answer-validity check and gold cross-check
  kept_haiku_w8.jsonl             Haiku-kept rows (A40 c.1, keep = Haiku == gold at confidence >= 0.80)

Rules:
  1. Queued items: keep only when the Opus answer == gold AND Opus confidence >= 0.85 (A40 c.2). Source 'opus'.
  2. Audit: Opus vs gold on the audited Haiku-kept items (A40 c.3). Disagreement > 6% -> report and do NOT finalize.
     Per-domain re-read (A39): with the overall rate at 0 every domain is also at 0, so no re-read is triggered.
  3. Merge: Haiku-kept rows (source 'haiku') + queued Opus-kept rows (source 'opus'). Audit items stay in the pool.
  4. Seeded cap (ruling (ii), seed 20261013): if the merged pool exceeds 1,200, keep a seeded uniform subsample
     within each route label (gold). Every label keeps the same fraction of its rows; label quotas use largest-
     remainder rounding so the total is exactly 1,200; inside a label the kept rows are the first quota in
     SEED-keyed hash order of the id.
  5. Write final_kept_w8.jsonl with {id, source} per row, and opus_finalize_w8.json with the counts.

Gold is never edited or chosen here. An Opus answer only decides whether a queued item is kept.
Nothing is written when the audit check fails, and nothing is written in --dry-run.

  ../../../../../.venv/bin/python -I builders/w8_finalize.py [--dry-run]
"""
from __future__ import annotations

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W8"
OPUS_DIR = C.WAVE2 / "opus_w8"
QUEUE = C.WAVE2 / "opus_queue_w8"
KEPT = C.WAVE2 / "kept_haiku_w8.jsonl"
CAND = C.CAND_DIR / "w8_candidates.jsonl"
OUT = C.WAVE2 / "final_kept_w8.jsonl"
OUT_STATS = C.WAVE2 / "opus_finalize_w8.json"

OPUS_CONF = 0.85          # A40 c.2: queued items kept only when Opus agrees with gold at >= 0.85
AUDIT_MAX = 0.06          # A40 c.3 / A39: audit disagreement above 6% -> report, do not finalize
CAP = 1200                # ruling (ii): <= 1,200 kept per type
AUDIT_FAILED_CHUNKS = ()  # the orchestrator's audit-failed list for W8 is empty: nothing to ignore


def valid_conf(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and 0.0 <= x <= 1.0


def load_opus() -> dict:
    """qid -> Opus answer dict, over every opus_w8/chunk_*.json (failed chunks skipped, none for W8)."""
    ans = {}
    for f in sorted(OPUS_DIR.glob("chunk_*.json")):
        if f.name in AUDIT_FAILED_CHUNKS:
            continue
        for a in C.read_json(f):
            if a["qid"] in ans:
                raise ValueError(f"duplicate Opus qid {a['qid']} in {f.name}")
            ans[a["qid"]] = a
    return ans


def seeded_cap(pool: list, cap: int) -> list:
    """pool: [{id, source, gold}]. Uniform within label: each label keeps the same fraction of its rows."""
    if len(pool) <= cap:
        return sorted(pool, key=lambda r: r["id"])
    by = defaultdict(list)
    for r in pool:
        by[r["gold"]].append(r)
    n = len(pool)
    exact = {g: len(v) * cap / n for g, v in by.items()}
    quota = {g: math.floor(x) for g, x in exact.items()}
    rem = cap - sum(quota.values())
    for g in sorted(by, key=lambda g: (-(exact[g] - quota[g]), str(g)))[:rem]:
        quota[g] += 1
    out = []
    for g, v in by.items():
        v.sort(key=lambda r: C.key_hash(C.SEED, T, "cap", r["id"]))
        out += v[:quota[g]]
    out.sort(key=lambda r: r["id"])
    return out


def analyse() -> tuple:
    key = C.read_json(QUEUE / "key.json")
    roles = C.read_json(QUEUE / "roles.json")
    cands = {r["id"]: r for r in C.read_jsonl(CAND)}
    kept = C.read_jsonl(KEPT)
    kept_ids = {r["id"] for r in kept}
    if len(kept_ids) != len(kept):
        raise ValueError("kept_haiku_w8.jsonl holds duplicate ids")
    opus = load_opus()
    st = Counter()
    problems = []

    if set(opus) != set(roles) or set(key) != set(roles):
        problems.append(f"coverage: opus {len(opus)}, roles {len(roles)}, key {len(key)} (must match)")
    for q, role in roles.items():
        k = key[q]
        c = cands.get(k["id"])
        if c is None:
            problems.append(f"qid {q} maps to missing row {k['id']}")
            continue
        if c["gold"] != k["gold"]:
            problems.append(f"gold mismatch for {k['id']} (key vs candidates)")
    if problems:
        raise SystemExit("W8 finalize refused: " + "; ".join(problems))

    audit_dis = []
    queued_keep, queued_drop = [], []
    for q, role in roles.items():
        k = key[q]
        c = cands[k["id"]]
        a = opus.get(q)
        valid = a is not None and a.get("answer") in c["options"] and valid_conf(a.get("confidence"))
        if not valid:
            st["opus_invalid"] += 1
        if role["role"] == "audit":
            if k["id"] not in kept_ids:
                problems.append(f"audit item {k['id']} is not a Haiku-kept row")
                continue
            st["audit_read"] += 1
            if not valid or a["answer"] != k["gold"]:
                audit_dis.append({"id": k["id"], "gold": k["gold"], "opus": a and a.get("answer"),
                                  "opus_conf": a and a.get("confidence")})
        elif role["role"] == "queued":
            st[f"queued_reason_{role['reason']}"] += 1
            if valid and a["answer"] == k["gold"] and a["confidence"] >= OPUS_CONF:
                queued_keep.append({"id": k["id"], "source": "opus", "gold": k["gold"], "reason": role["reason"]})
                st[f"queued_keep_{role['reason']}"] += 1
            else:
                queued_drop.append(k["id"])
        else:
            problems.append(f"unknown role {role['role']!r} for {q}")
    if problems:
        raise SystemExit("W8 finalize refused: " + "; ".join(problems))

    n_audit = st["audit_read"]
    audit_rate = len(audit_dis) / n_audit if n_audit else 0.0
    audit_ids = [key[q]["id"] for q, v in roles.items() if v["role"] == "audit"]
    audit_per_card = Counter(cands[i]["meta"]["construction"]["card_id"] for i in audit_ids)
    dom_dis = Counter(cands[d["id"]]["meta"]["construction"]["card_id"] for d in audit_dis)

    pool = [{"id": r["id"], "source": "haiku", "gold": r["gold"]} for r in kept] + queued_keep
    ids = [p["id"] for p in pool]
    if len(set(ids)) != len(ids):
        raise SystemExit("W8 finalize refused: duplicate ids across Haiku-kept and Opus-kept")
    for p in pool:
        if p["id"] not in cands:
            raise SystemExit(f"W8 finalize refused: {p['id']} not in candidates")
        if cands[p["id"]]["gold"] != p["gold"]:
            raise SystemExit(f"W8 finalize refused: gold mismatch for {p['id']}")

    final = seeded_cap(pool, CAP)
    labels_before = dict(sorted(Counter(p["gold"] for p in pool).items()))
    labels_after = dict(sorted(Counter(p["gold"] for p in final).items()))
    stats = {
        "type": T, "task_name": "complaint_routing", "ruling": "PREREG_FINAL A40 addendum (W8); A40 (c); ruling (ii)",
        "seed": C.SEED, "opus_conf_keep": OPUS_CONF, "audit_max": AUDIT_MAX, "cap": CAP,
        "haiku_kept": len(kept),
        "queued": len(roles) - n_audit, "queued_by_reason": {k[len("queued_reason_"):]: v for k, v in st.items()
                                                             if k.startswith("queued_reason_")},
        "queued_kept_by_reason": {k[len("queued_keep_"):]: v for k, v in st.items()
                                  if k.startswith("queued_keep_")},
        "queued_kept": len(queued_keep), "queued_dropped": len(queued_drop),
        "opus_invalid": st["opus_invalid"], "opus_answers": len(opus),
        "audit_n": n_audit, "audit_disagree": len(audit_dis), "audit_disagree_rate": round(audit_rate, 4),
        "audit_disagree_rows": audit_dis, "audit_pass": audit_rate <= AUDIT_MAX,
        "audit_per_card_n": dict(audit_per_card),
        "audit_per_card_disagree": dict(dom_dis),
        "pool": len(pool), "pool_by_source": dict(Counter(p["source"] for p in pool)),
        "pool_labels": labels_before,
        "final": len(final), "final_by_source": dict(Counter(p["source"] for p in final)),
        "final_labels": labels_after,
        "final_output": str(OUT), "final_sha256": None,
    }
    return final, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    final, stats = analyse()
    print(f"W8 pool {stats['pool']} (haiku {stats['haiku_kept']} + opus {stats['queued_kept']}) -> final {stats['final']}"
          f" by source {stats['final_by_source']}")
    print(f"audit {stats['audit_disagree']}/{stats['audit_n']} disagree ({stats['audit_disagree_rate'] * 100:.2f}%),"
          f" limit {AUDIT_MAX * 100:.0f}%, pass={stats['audit_pass']}")
    if not stats["audit_pass"]:
        print("W8 NOT finalized: audit disagreement above 6%. Report it; do not finalize.")
        if not dry:
            C.kp.write_json(OUT_STATS, stats)
        raise SystemExit(2)
    if dry:
        print("dry run: nothing written")
        return final, stats
    if OUT.exists():
        raise SystemExit(f"refusing to overwrite existing {OUT}")
    rows = [{"id": p["id"], "source": p["source"]} for p in final]
    C.kp.write_jsonl(OUT, rows)
    stats["final_sha256"] = C.sha256_file(OUT)
    C.kp.write_json(OUT_STATS, stats)
    print(f"wrote {OUT} ({len(rows)} rows) and {OUT_STATS}")
    return final, stats


if __name__ == "__main__":
    main()
