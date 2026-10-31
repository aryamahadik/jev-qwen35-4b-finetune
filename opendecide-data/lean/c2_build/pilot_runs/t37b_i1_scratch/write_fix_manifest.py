"""Write t37b/pools/FIX_I1_MANIFEST.json: generator code files changed by fix iteration 1, frozen sha -> current sha."""
import hashlib, json, sys, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import paths
from t37b import answers_gate as G, builder as BL
fm = json.loads(G.FREEZE_MANIFEST.read_text(encoding="utf-8"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
code = {}
for rel, want in sorted(fm["sha256"].items()):
    if rel.startswith("c2_build/t37b/") and rel.endswith(".py"):
        got = sha(G.LEAN / rel)
        if got != want:
            code[rel] = {"from": want, "to": got}
data_changed = [rel for rel, want in fm["sha256"].items() if not rel.endswith(".py") and sha(G.LEAN / rel) != want]
assert not data_changed, data_changed
man = {"family": "T37b", "stage": "fix iteration 1 (C2_DATA_SPEC 6.4 step 6): generator CODE changed after the pool freeze",
       "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "amendment": {"file": "c2_build/t37b/G0_LITE_T37B_A1.md", "sha256": BL.G0_AMENDMENT_SHA256},
       "g0_v2": {"file": "c2_build/t37b/G0_LITE_T37B.md", "sha256": BL.G0_SHA256},
       "pool": {"file": "c2_build/t37b/pools/t37b_equiv_pool.json", "unchanged": True},
       "code": code,
       "rule": "answers_gate.v1_untouched excuses a .py file under c2_build/t37b only when this manifest records it from "
               "exactly the frozen sha to exactly its current sha; pool, answers, task records and G0 v2 stay exact",
       "note": "no label, pool entry, Haiku answer or gate bar changed"}
paths.write_json(G.FIX_MANIFEST, man)
print(json.dumps({k: v["to"][:12] for k, v in code.items()}, indent=1))
