"""refresh-dev --check on the REAL candidates logs, with the two parts that read eval-side files stubbed out:
  * the per-file sha256 of every eval input the log read (RefreshBasis._input_ok -> True) and the eval files of the other
    targets (g.target_files_now -> empty), and
  * the sealed-side digest child (g.sealed_side_run -> the digests the logs recorded).
Everything else is the real check on the real logs / candidates / program files / dev files / target list / cosine setting:
code shas, engine sha, inputs_at_start vs the guard now, train / seed shas, the log's reasons, the engine `methods` text.
No ohs / sealed path is opened, listed or hashed by this script (the stubs replace exactly the code that would). Read-only:
nothing is written.   Counts and our own file names only are printed.
Run from lean/:  ../.venv/bin/python -B c2_build/_backup_refresh/real_check_noeval.py [block ...]
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "c2_build"))
NEXT = Path(os.environ.get("G13_MODULE_PATH") or LEAN / "c2_build" / "g13_c2.py")
spec = importlib.util.spec_from_file_location("g13_c2", NEXT)
G = importlib.util.module_from_spec(spec)
sys.modules["g13_c2"] = G
spec.loader.exec_module(G)
g = G.g

blocks = sys.argv[1:] or sorted(p.stem[len("c2_cand_"):] for p in (G.OUT).glob("c2_cand_*.json"))
logs = G.read_refresh_logs(blocks)
side = {}
for d in logs.values():
    side.update({k: v for k, v in (d["log"]["engine"]["inputs_sha256"].get("sealed_side") or {}).items() if v})

G.RefreshBasis._input_ok = lambda self, k, sha: True
g.target_files_now = lambda t: set()
g.sealed_side_run = lambda units, owner, names, cosine, mode="scan", py=None: {n: {"digest": side[n]} for n in names}

print(f"tool {G.g.sha256_file(NEXT)[:12]}  blocks with a log: {len(logs)} of {len(blocks)}  "
      f"engine targets: {len(G.engine_targets('candidates'))}")
for b in blocks:
    probs = G.refresh_check([b])
    msgs = [w for v in probs.values() for w in v]
    print(f"{b}: {'REFRESHABLE (apart from the stubbed eval-file / sealed checks)' if not msgs else 'REFUSED'}")
    for w in msgs:
        print("    ", w[:230])
