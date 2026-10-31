#!/usr/bin/env python3
"""G-block wave 2, PREREG_FINAL A40 (c) steps 1-3: keep/queue split from the blind Haiku reads.

Keep rule (A40 c.1): keep a candidate when Haiku's answer equals its program gold and Haiku's confidence is >= 0.80.
Every other candidate is queued for the blind Opus read (A40 c.2) as a gold-free TEACH-0 chunk. A seeded 5% audit
sample of kept items (A40 c.3) also goes to Opus, stratified per type (round(5% x kept of that type), first n in
seeded hash order).

Queue reason, one per item, first match wins:
  missing         no usable Haiku verdict: no answer for the qid, or the chunk has no Haiku output (chunk_129)
  invalid         answer not an allowed label, confidence not a finite number in [0, 1], or a duplicate qid
  disagree        valid answer != gold (any confidence)
  low_confidence  valid answer == gold but confidence < 0.80
chunk_129: the orchestrator says its audit failed. Its Haiku answers are not used, so its 50 items are treated as
"missing" and queued to Opus. They are not dropped.

Gold is read only from verify/key.json and candidates/candidates.jsonl (both hash-checked against verify/manifest.json).
Nothing here edits or chooses a gold. Opus-queue readers never see gold, ids or meta.

Run: /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -I route/route_haiku.py
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

WAVE2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/wave2")
if str(WAVE2) not in sys.path:
    sys.path.insert(0, str(WAVE2))
from builders import common as C  # noqa: E402  (SEED, read helpers, A38 write guard)

TYPES = ("W1", "W2", "W3", "W4", "W5", "W6", "W7")
KEEP_CONF = 0.80
AUDIT_SHARE = 0.05
CHUNK = 50
NO_HAIKU_CHUNKS = {"chunk_129.json": "audit failed (orchestrator instruction): no Haiku output"}
REASON_ORDER = ("missing", "invalid", "disagree", "low_confidence")

VERIFY = WAVE2 / "verify"
CHUNKS = VERIFY / "chunks"
HAIKU = VERIFY / "haiku"
CAND = WAVE2 / "candidates" / "candidates.jsonl"
OPUS = WAVE2 / "opus_queue"
ROUTE = WAVE2 / "route"


def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def verify_qid(row_id: str) -> str:
    return "v" + h(C.SEED, "verify-qid", row_id)[:12]


def opus_qid(row_id: str) -> str:
    return "o" + h(C.SEED, "opus-qid", row_id)[:12]


def is_conf(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and 0.0 <= x <= 1.0


def gold_label(qtype: str, gold):
    if qtype == "noul":
        assert gold in (0, 1) and not isinstance(gold, bool), gold
        return "yes" if gold == 1 else "no"
    return gold


def allowed(kind: str, options) -> set:
    return {"yes", "no"} if kind == "yes/no" else set(options)


def sha(p) -> str:
    return C.sha256_file(p)


def main() -> None:
    # ---- integrity: the inputs are the ones the verify build hashed
    man = C.read_json(VERIFY / "manifest.json")
    assert sha(CAND) == man["candidates_sha256"], "candidates.jsonl changed since verify build"
    assert sha(VERIFY / "key.json") == man["key_sha256"], "key.json changed since verify build"

    cands_list = C.read_jsonl(CAND)
    cands = {r["id"]: r for r in cands_list}
    assert len(cands) == len(cands_list), "duplicate candidate ids"
    key = C.read_json(VERIFY / "key.json")
    assert len(key) == len(cands) == man["n_items"], (len(key), len(cands), man["n_items"])

    chunk_items, chunk_of = {}, {}
    for f in sorted(CHUNKS.glob("chunk_*.json")):
        for it in C.read_json(f):
            assert it["qid"] not in chunk_items, it["qid"]
            chunk_items[it["qid"]] = it
            chunk_of[it["qid"]] = f.name
    assert set(chunk_items) == set(key), "chunk qids differ from key qids"
    for q, k in key.items():
        assert chunk_of[q] == k["chunk"], q
        assert verify_qid(k["id"]) == q, "verify qid does not match row id"
        assert cands[k["id"]]["gold"] == k["gold"] and cands[k["id"]]["qtype"] == k["qtype"], k["id"]

    # ---- Haiku reads
    answers = defaultdict(list)          # qid -> [(chunk, entry)]
    chunk_status = {}
    malformed = Counter()
    for cn in sorted({v["chunk"] for v in key.values()}):
        p = HAIKU / cn
        if cn in NO_HAIKU_CHUNKS or not p.exists():
            chunk_status[cn] = NO_HAIKU_CHUNKS.get(cn, "no Haiku output file")
            continue
        data = C.read_json(p)
        if not isinstance(data, list):
            chunk_status[cn] = "not a JSON list"
            continue
        chunk_status[cn] = "ok"
        for e in data:
            if not isinstance(e, dict) or not isinstance(e.get("qid"), str):
                malformed[cn] += 1
                continue
            answers[e["qid"]].append((cn, e))
    foreign = sum(1 for q, ents in answers.items() for cn, _ in ents if q not in key or key[q]["chunk"] != cn)

    # ---- one decision per item
    decisions = {}
    for q, k in key.items():
        item = chunk_items[q]
        gold = gold_label(k["qtype"], k["gold"])
        rec = {"qid": q, "id": k["id"], "type": k["type"], "qtype": k["qtype"], "gold": k["gold"],
               "gold_label": gold, "chunk": k["chunk"], "haiku_answer": None, "haiku_confidence": None,
               "valid": False, "agree": None}
        ents = [e for cn, e in answers.get(q, []) if cn == k["chunk"]]
        if not ents:
            rec.update(decision="queue", reason="missing")
        elif len(ents) > 1:
            rec.update(decision="queue", reason="invalid", haiku_answer=ents[0].get("answer"),
                       haiku_confidence=ents[0].get("confidence"))
        else:
            ans, conf = ents[0].get("answer"), ents[0].get("confidence")
            rec.update(haiku_answer=ans, haiku_confidence=conf)
            valid = isinstance(ans, str) and ans in allowed(item["kind"], item.get("options", [])) and is_conf(conf)
            if not valid:
                rec.update(decision="queue", reason="invalid")
            else:
                agree = ans == gold
                rec.update(valid=True, agree=agree)
                if agree and conf >= KEEP_CONF:
                    rec.update(decision="keep", reason=None)
                elif not agree:
                    rec.update(decision="queue", reason="disagree")
                else:
                    rec.update(decision="queue", reason="low_confidence")
        decisions[q] = rec

    # ---- seeded 5% audit of kept items, stratified per type
    audit_n, audit = {}, set()
    for T in TYPES:
        kept_T = sorted((q for q, d in decisions.items() if d["decision"] == "keep" and d["type"] == T),
                        key=lambda q: h(C.SEED, "a40-audit", decisions[q]["id"]))
        n = int(math.floor(AUDIT_SHARE * len(kept_T) + 0.5))
        audit_n[T] = n
        audit |= set(kept_T[:n])
    for q in audit:
        decisions[q]["audited"] = True
    for d in decisions.values():
        d.setdefault("audited", False)

    # ---- kept_haiku.jsonl (candidate rows unchanged) and provenance sidecar
    kept_rows, prov = [], []
    for r in cands_list:
        q = verify_qid(r["id"])
        d = decisions[q]
        if d["decision"] == "keep":
            kept_rows.append(r)
            prov.append({"id": r["id"], "verify_qid": q, "chunk": d["chunk"], "gold_label": d["gold_label"],
                         "haiku_answer": d["haiku_answer"], "haiku_confidence": d["haiku_confidence"],
                         "audited_by_opus": d["audited"]})
    C.kp.write_jsonl(WAVE2 / "kept_haiku.jsonl", kept_rows)
    C.kp.write_jsonl(WAVE2 / "kept_haiku_provenance.jsonl", prov)

    # ---- Opus queue: queued items + audit items, gold-free TEACH-0 chunks, new qids
    queue_q = [q for q, d in decisions.items() if d["decision"] == "queue"] + sorted(audit)
    verify_qids = set(key)
    order = sorted(queue_q, key=lambda q: h(C.SEED, "opus-order", decisions[q]["id"]))
    opus_key, roles, chunk_sha, chunk_sizes = {}, {}, {}, []
    for ci in range(0, len(order), CHUNK):
        items = []
        for pos, q in enumerate(order[ci:ci + CHUNK]):
            d = decisions[q]
            row = cands[d["id"]]
            nq = opus_qid(d["id"])
            assert nq not in verify_qids and nq not in opus_key, "opus qid collision"
            it = {"qid": nq, "kind": "yes/no" if row["qtype"] == "noul" else "choice",
                  "text": row["state"], "question": row["instructions"]}
            if row["qtype"] == "choice":
                it["options"] = list(row["options"])
            it["definitions"] = row["card"]
            items.append(it)
            opus_key[nq] = {"id": d["id"], "type": d["type"], "qtype": row["qtype"], "gold": row["gold"],
                            "gold_method": row["meta"]["gold_method"], "group_id": row["group_id"],
                            "chunk": f"chunk_{ci // CHUNK:03d}.json", "position": pos}
            roles[nq] = {"role": "audit" if d["audited"] else "queued",
                         "reason": "audit_kept" if d["audited"] else d["reason"],
                         "verify_qid": q, "haiku_answer": d["haiku_answer"], "haiku_confidence": d["haiku_confidence"]}
        blob = json.dumps(items, ensure_ascii=False)
        assert "c2_wave2" not in blob and '"gold":' not in blob and '"meta":' not in blob, "gold or id leaked"
        name = f"chunk_{ci // CHUNK:03d}.json"
        OPUS.mkdir(parents=True, exist_ok=True)
        C.kp.write_text(OPUS / name, json.dumps(items, ensure_ascii=False, indent=1))
        chunk_sha[name] = sha(OPUS / name)
        chunk_sizes.append(len(items))
    C.kp.write_json(OPUS / "key.json", opus_key)
    C.kp.write_json(OPUS / "roles.json", roles)
    C.kp.write_json(OPUS / "manifest.json", {
        "what": "G-block wave-2 Opus queue (A40 c step 2, plus the step 3 5% audit). Gold-free chunks; key.json holds gold "
                "for scoring only; roles.json holds the queue reason and the Haiku verdict (never shown to readers).",
        "chunk_format": "TEACH-0 (qid, kind, text, question, options (choice only), definitions)",
        "chunk_size": CHUNK, "n_chunks": len(chunk_sizes), "chunk_sizes": chunk_sizes, "n_items": len(order),
        "n_queued": sum(1 for v in roles.values() if v["role"] == "queued"),
        "n_audit": sum(1 for v in roles.values() if v["role"] == "audit"),
        "chunks": chunk_sha, "candidates_sha256": man["candidates_sha256"], "verify_key_sha256": man["key_sha256"],
        "chunk_129_handling": NO_HAIKU_CHUNKS,
    })

    # ---- stats
    stats = {"per_type": {}, "total": None}
    for T in TYPES + ("ALL",):
        ds = [d for d in decisions.values() if T == "ALL" or d["type"] == T]
        valid = [d for d in ds if d["valid"]]
        valid_hi = [d for d in valid if d["haiku_confidence"] >= KEEP_CONF]
        reasons = Counter(d["reason"] for d in ds if d["decision"] == "queue")
        row = {
            "candidates": len(ds),
            "valid_haiku_answers": len(valid),
            "agree_with_gold": sum(1 for d in valid if d["agree"]),
            "agreement_rate": round(sum(1 for d in valid if d["agree"]) / len(valid), 4) if valid else None,
            "valid_conf_ge_0.80": len(valid_hi),
            "agreement_rate_conf_ge_0.80": round(sum(1 for d in valid_hi if d["agree"]) / len(valid_hi), 4)
            if valid_hi else None,
            "kept": sum(1 for d in ds if d["decision"] == "keep"),
            "keep_rate": round(sum(1 for d in ds if d["decision"] == "keep") / len(ds), 4),
            "queued_by_reason": {r: reasons.get(r, 0) for r in REASON_ORDER},
            "queued_total": sum(reasons.values()),
            "audit_of_kept": sum(1 for d in ds if d["audited"]),
            "opus_items": sum(reasons.values()) + sum(1 for d in ds if d["audited"]),
        }
        if T == "ALL":
            stats["total"] = row
        else:
            stats["per_type"][T] = row
    stats["haiku_chunk_status"] = {cn: s for cn, s in chunk_status.items() if s != "ok"}
    stats["malformed_entries"] = dict(malformed)
    stats["foreign_or_misplaced_entries"] = foreign
    stats["audit_n_per_type"] = audit_n
    stats["opus_chunks"] = len(chunk_sizes)
    stats["opus_chunk_sizes_last"] = chunk_sizes[-1] if chunk_sizes else 0
    assert sum(r["kept"] for r in stats["per_type"].values()) == len(kept_rows)
    assert len(kept_rows) + sum(r["queued_total"] for r in stats["per_type"].values()) == len(key)

    ROUTE.mkdir(parents=True, exist_ok=True)
    C.kp.write_jsonl(ROUTE / "decisions.jsonl", [decisions[q] for q in sorted(decisions, key=lambda q: decisions[q]["id"])])
    C.kp.write_json(ROUTE / "route_stats.json", stats)
    print(json.dumps({"kept": len(kept_rows), "opus_items": len(order), "opus_chunks": len(chunk_sizes),
                      "per_type": stats["per_type"], "total": stats["total"],
                      "haiku_chunk_status": stats["haiku_chunk_status"], "malformed": stats["malformed_entries"],
                      "foreign": foreign, "audit_n": audit_n}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
