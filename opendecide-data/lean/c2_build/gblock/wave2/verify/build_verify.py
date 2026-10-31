#!/usr/bin/env python3
"""G-block wave 2: assemble the candidates and cut the gold-free blind-verify chunks (PREREG_FINAL A40 c, step 1).

Stage 1 (candidates): concatenates candidates/W1..W7.jsonl (each builder already ran the decoder render, loader and
token checks) into candidates/candidates.jsonl, and writes candidates/candidates_stats.json with per-type counts and
label balance. Gold is copied as the builder recorded it; nothing here edits or chooses a label.

Stage 2 (verify): every candidate goes into a gold-free chunk of 50 for the blind Haiku read, in the TEACH-0 format
(qid, kind, text, question, options, definitions). Qids are opaque hashes and the order is a seeded hash shuffle, so a
chunk does not show a type. verify/key.json maps each qid to its row id, type and gold; no reader is shown it.

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -I verify/build_verify.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

WAVE2 = Path(__file__).resolve().parents[1]
if str(WAVE2) not in sys.path:
    sys.path.insert(0, str(WAVE2))
from builders import common as C  # noqa: E402  (also puts c2_build on sys.path for c2_kit)

TYPES = ("W1", "W2", "W3", "W4", "W5", "W6", "W7")
CHUNK = 50
CAND = WAVE2 / "candidates"
VERIFY = WAVE2 / "verify"
CHUNKS = VERIFY / "chunks"
BLIND_KEYS = ("qid", "kind", "text", "question", "options", "definitions")
EXPECTED_KEYS = ("qid", "kind", "text", "question", "definitions")


def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def label_summary(rows: list) -> dict:
    """Gold counts and the max-to-min ratio of the counts (1.0 = perfectly balanced)."""
    c = Counter(str(r["gold"]) for r in rows)
    n = len(rows)
    return {"n": n, "labels": dict(sorted(c.items())),
            "shares": {k: round(v / n, 4) for k, v in sorted(c.items())} if n else {},
            "max_to_min_ratio": round(max(c.values()) / min(c.values()), 4) if c else None}


def assemble() -> tuple:
    rows, per_type = [], {}
    for T in TYPES:
        rs = C.read_jsonl(CAND / f"{T}.jsonl")
        bad = [(r.get("id"), C.schema_problems(r)) for r in rs if C.schema_problems(r)]
        if bad:
            raise SystemExit(f"{T}: schema problems, e.g. {bad[:3]}")
        if any(not r["id"].startswith(f"c2_wave2:{T}:") for r in rs):
            raise SystemExit(f"{T}: a row id does not carry its type")
        per_type[T] = rs
        rows += rs
    ids = Counter(r["id"] for r in rows)
    dup = [i for i, c in ids.items() if c > 1]
    if dup:
        raise SystemExit(f"duplicate candidate ids, e.g. {dup[:3]}")

    stats = {"what": "G-block wave-2 candidates (A40 b-c), before the blind verify", "types": {}, "total_rows": len(rows)}
    for T in TYPES:
        rs = per_type[T]
        qtypes = Counter(r["qtype"] for r in rs)
        if T == "W7":   # the 'tool' side has 3-6 tool names as gold; balance is reported as tool vs no_tool
            labels = label_summary([dict(r, gold=("no_tool" if r["gold"] == "no_tool" else "tool")) for r in rs])
        else:
            labels = label_summary(rs)
        stats["types"][T] = {
            "task_name": C.TYPES[T], "gold_method": rs[0]["meta"]["gold_method"], "qtype": dict(qtypes),
            "n_rows": len(rs), "labels": labels,
            "source": str(CAND / f"{T}.jsonl"), "source_sha256": C.sha256_file(CAND / f"{T}.jsonl"),
        }
    stats["total_rows"] = len(rows)
    out = CAND / "candidates.jsonl"
    C.kp.write_jsonl(out, rows)
    stats["output"] = str(out)
    stats["output_sha256"] = C.sha256_file(out)
    C.kp.write_json(CAND / "candidates_stats.json", stats)
    return rows, stats


def qid_of(row_id: str) -> str:
    return "v" + h(C.SEED, "verify-qid", row_id)[:12]


def cut_chunks(rows: list) -> tuple:
    order = sorted(rows, key=lambda r: h(C.SEED, "verify-order", r["id"]))
    qids = [qid_of(r["id"]) for r in order]
    if len(set(qids)) != len(qids):
        raise SystemExit("qid collision; change the qid length")
    key, chunk_files, chunk_sizes = {}, [], []
    for ci in range(0, len(order), CHUNK):
        items = []
        for pos, r in enumerate(order[ci:ci + CHUNK]):
            q = qid_of(r["id"])
            it = {"qid": q, "kind": "yes/no" if r["qtype"] == "noul" else "choice", "text": r["state"],
                  "question": r["instructions"]}
            if r["qtype"] == "choice":
                it["options"] = list(r["options"])
            it["definitions"] = r["card"]
            assert set(it) <= set(BLIND_KEYS) and set(EXPECTED_KEYS) <= set(it), sorted(it)
            items.append(it)
            key[q] = {"id": r["id"], "type": r["id"].split(":")[1], "qtype": r["qtype"], "gold": r["gold"],
                      "gold_method": r["meta"]["gold_method"], "group_id": r["group_id"],
                      "chunk": f"chunk_{ci // CHUNK:03d}.json", "position": pos}
        blob = json.dumps(items, ensure_ascii=False)
        assert "c2_wave2" not in blob and '"gold":' not in blob and '"meta":' not in blob, "gold or id leaked"
        name = f"chunk_{ci // CHUNK:03d}.json"
        C.kp.write_text(CHUNKS / name, json.dumps(items, ensure_ascii=False, indent=1))
        chunk_files.append(str(CHUNKS / name))
        chunk_sizes.append(len(items))
    C.kp.write_json(VERIFY / "key.json", key)
    manifest = {
        "what": "G-block wave-2 blind-verify chunks (A40 c step 1); gold-free; key.json holds gold for scoring only",
        "chunk_size": CHUNK, "n_chunks": len(chunk_files), "chunk_sizes": chunk_sizes, "n_items": len(rows),
        "chunk_format": "TEACH-0 (qid, kind, text, question, options (choice only), definitions)",
        "candidates_sha256": C.sha256_file(CAND / "candidates.jsonl"), "key_sha256": C.sha256_file(VERIFY / "key.json"),
        "ignored_tasks_audit_failed": [],
        "chunks": {Path(p).name: C.sha256_file(p) for p in chunk_files},
    }
    C.kp.write_json(VERIFY / "manifest.json", manifest)
    return chunk_files, chunk_sizes, key


def main() -> None:
    rows, stats = assemble()
    chunk_files, chunk_sizes, key = cut_chunks(rows)
    per_type_chunks = Counter(v["type"] for v in key.values())
    summary = {"candidates": str(CAND / "candidates.jsonl"), "candidates_total": len(rows),
               "per_type": {T: stats["types"][T]["n_rows"] for T in TYPES},
               "label_balance": {T: stats["types"][T]["labels"]["shares"] for T in TYPES},
               "verify_chunks_dir": str(CHUNKS), "n_chunks": len(chunk_files), "chunk_sizes": chunk_sizes,
               "key": str(VERIFY / "key.json"), "items_per_type_in_key": dict(per_type_chunks)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
