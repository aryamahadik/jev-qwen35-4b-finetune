import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
"""lockcheck.py (used inside the GPU container) agrees with the bench's data_lock.py, and the shipped lock entry is the bench's own."""
import json, sys
from common import *
import lockcheck
sys.path.insert(0, BENCH)
import data_lock
lock = json.load(open(f"{BENCH}/data.lock.json"))["cases.jsonl"]
mine = json.load(open(f"{TT}/data/data.lock.cases.json"))
assert mine == lock, "the shipped lock entry differs from system-one-bench/data.lock.json"
fp_a = lockcheck.fingerprint(f"{TT}/data/cases.jsonl")
fp_b = data_lock.fingerprint(f"{TT}/data/cases.jsonl")
assert fp_a == fp_b, "fingerprint differs from data_lock.fingerprint"
assert fp_a == lock, "cases.jsonl does not equal the frozen entry"
assert lockcheck.check(f"{TT}/data/cases.jsonl", f"{TT}/data/data.lock.cases.json") == []
# a one-character change in one case must be caught
import tempfile, os
bad = tempfile.mkdtemp() + "/cases.jsonl"
lines = open(f"{TT}/data/cases.jsonl", encoding="utf-8").read().split("\n")
c = json.loads(lines[10]); c["gold"][next(iter(c["gold"]))]["label"] = "tampered"; lines[10] = json.dumps(c, ensure_ascii=False)
open(bad, "w", encoding="utf-8").write("\n".join(lines))
probs = lockcheck.check(bad, f"{TT}/data/data.lock.cases.json")
print("tampered file problems:", probs)
assert probs and any("overall" in p for p in probs)
print("LOCKCHECK TEST PASSED", fp_a["sha256"][:12])
