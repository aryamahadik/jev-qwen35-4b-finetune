#!/usr/bin/env python3
"""G-block wave 2, W8 (complaint routing): gold-free blind-verify chunks (PREREG_FINAL A40 addendum W8, A40 c step 1).

Reads candidates/w8_candidates.jsonl (the W8 builder already ran the decoder render, loader and token checks) and cuts
every candidate into a gold-free chunk of 50 for the blind Haiku read, in the TEACH-0 format used by verify/build_verify.py
(qid, kind, text, question, options (choice only), definitions). Qids are opaque hashes and the order is a seeded hash
shuffle, so a chunk does not show a route. verify/w8/key.json maps each qid to its row id, type, route and gold; it is for
scoring only and no reader is shown it. Nothing here edits or chooses a label.

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -I verify/w8/build_verify_w8.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

WAVE2 = Path(__file__).resolve().parents[2]
if str(WAVE2) not in sys.path:
    sys.path.insert(0, str(WAVE2))
from builders import common as C  # noqa: E402  (also puts c2_build on sys.path for c2_kit)

T = "W8"
CHUNK = 50
CAND = WAVE2 / "candidates" / "w8_candidates.jsonl"
VERIFY = WAVE2 / "verify" / "w8"
CHUNKS = VERIFY / "chunks"
KEY = VERIFY / "key.json"
MANIFEST = VERIFY / "manifest.json"
BLIND_KEYS = ("qid", "kind", "text", "question", "options", "definitions")
EXPECTED_KEYS = ("qid", "kind", "text", "question", "definitions")


def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def qid_of(row_id: str) -> str:
    return "v" + h(C.SEED, "verify-qid", row_id)[:12]


def load_rows() -> list:
    rows = C.read_jsonl(CAND)
    bad = [(r.get("id"), C.schema_problems(r)) for r in rows if C.schema_problems(r)]
    if bad:
        raise SystemExit(f"{T}: schema problems, e.g. {bad[:3]}")
    if any(not r["id"].startswith(f"c2_wave2:{T}:") for r in rows):
        raise SystemExit(f"{T}: a row id does not carry its type")
    dup = [i for i, c in Counter(r["id"] for r in rows).items() if c > 1]
    if dup:
        raise SystemExit(f"duplicate candidate ids, e.g. {dup[:3]}")
    return rows


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
    C.kp.write_json(KEY, key)
    manifest = {
        "what": "G-block wave-2 W8 (complaint routing) blind-verify chunks (A40 addendum W8, A40 c step 1); gold-free; "
                "key.json holds gold for scoring only",
        "type": T, "task_name": C.TYPES.get(T, "complaint_routing"),
        "chunk_size": CHUNK, "n_chunks": len(chunk_files), "chunk_sizes": chunk_sizes, "n_items": len(rows),
        "chunk_format": "TEACH-0 (qid, kind, text, question, options (choice only), definitions)",
        "candidates": str(CAND), "candidates_sha256": C.sha256_file(CAND), "key_sha256": C.sha256_file(KEY),
        "ignored_tasks_audit_failed": [],
        "chunks": {Path(p).name: C.sha256_file(p) for p in chunk_files},
    }
    C.kp.write_json(MANIFEST, manifest)
    return chunk_files, chunk_sizes, key


def main() -> None:
    rows = load_rows()
    chunk_files, chunk_sizes, key = cut_chunks(rows)
    summary = {"candidates": str(CAND), "candidates_total": len(rows), "verify_chunks_dir": str(CHUNKS),
               "n_chunks": len(chunk_files), "chunk_sizes": chunk_sizes, "key": str(KEY),
               "manifest": str(MANIFEST), "items_in_key": len(key),
               "route_share_in_key": {k: round(v / len(key), 4) for k, v in sorted(Counter(
                   v["gold"] for v in key.values()).items())}}
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
