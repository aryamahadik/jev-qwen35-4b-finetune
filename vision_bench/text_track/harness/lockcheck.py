"""Frozen-data check that runs inside the GPU container (the bench's data_lock.py is not shipped there).

fingerprint() is data_lock.fingerprint() for a text cases file (no images): the SHA-256 of every case as canonical JSON, per suite,
plus one hash over all suites. data/data.lock.cases.json is the "cases.jsonl" entry of system-one-bench/data.lock.json, copied
unchanged; tests/test_lockcheck.py asserts it equals the bench's own entry and that this fingerprint equals data_lock's.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict


def total(suites):
    return hashlib.sha256("".join(f"{s} {v['sha256']}\n" for s, v in sorted(suites.items())).encode()).hexdigest()


def fingerprint(path):
    h, n = defaultdict(hashlib.sha256), defaultdict(int)
    for line in open(path, encoding="utf-8"):
        c = json.loads(line)
        h[c["suite"]].update(json.dumps(c, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode() + b"\n")
        n[c["suite"]] += 1
    suites = {s: {"n": n[s], "sha256": h[s].hexdigest()} for s in sorted(h)}
    return {"sha256": total(suites), "suites": suites}


def check(path, lock_path):
    """Problems with the cases file against the frozen lock entry; empty when every suite matches."""
    lock = json.load(open(lock_path))
    got = fingerprint(path)["suites"]
    problems = []
    for s in sorted(lock["suites"]):
        want = lock["suites"][s]
        if s not in got:
            problems.append(f"{s}: missing")
        elif got[s] != want:
            problems.append(f"{s}: {got[s]['n']} cases, hash {got[s]['sha256'][:12]}; frozen: {want['n']} cases, hash {want['sha256'][:12]}")
    problems += [f"{s}: not a frozen suite" for s in sorted(set(got) - set(lock["suites"]))]
    if total(got) != lock["sha256"]:
        problems.append("overall hash differs")
    return problems
