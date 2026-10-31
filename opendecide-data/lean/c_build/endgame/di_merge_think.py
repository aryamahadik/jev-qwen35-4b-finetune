"""Final test (b) helper: merge the A17-B0b knowledge-route think answers into a Decision Index run of the SHIPPED 4B.

Same rule as bench/think_check/score_b0b.py (lines 56-73, the code that made runs/c1think_sample10k), with the two
hard-coded run dirs turned into arguments. The think path is the base Qwen3.5-4B with LoRA OFF, so its answers
(bench/think_check/out_di.jsonl, 1,344 knowledge questions: MMLU, GPQA Diamond, GSM8K, CRUXEval, CLadder) do not depend
on the fine-tune and are reused unchanged ("same settings as before", A17-B0b). Prints counts only.

  P=../.venv/bin/python; R=../../bench/external_quarantine/decision_index/runs
  # parity check of this helper (CPU, free, ~20 s; PASSED 6 Oct 2026 05:19 UTC: 1,344 think answers, 1,288 replaced,
  # results.jsonl byte-identical to runs/c1think_sample10k). Re-run before use; delete the temp dir after:
  $P c_build/endgame/di_merge_think.py --src $R/c1_sample10k --dst "$(mktemp -d)/x" --parity $R/c1think_sample10k
  # real use, after the shipped model's DI run is fetched:
  $P c_build/endgame/di_merge_think.py --src $R/<SHIP>_sample10k --dst $R/<SHIP>think_sample10k
"""
import argparse
import filecmp
import json
import os
import shutil
import sys

J = "/Users/aryamahadik/Documents/jev"
ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True, help="DI run dir of the shipped 4B (has results.jsonl)")
ap.add_argument("--dst", required=True, help="new run dir for the merged system; must not exist yet")
ap.add_argument("--think", default=f"{J}/bench/think_check/out_di.jsonl")
ap.add_argument("--parity", default=None, help="an existing merged run dir to compare results.jsonl with (byte check)")
a = ap.parse_args()

src, dst = os.path.abspath(a.src), os.path.abspath(a.dst)
if not os.path.isfile(f"{src}/results.jsonl"):
    sys.exit(f"REFUSED: no results.jsonl in {src}")
if os.path.exists(dst) and os.listdir(dst):
    sys.exit(f"REFUSED: {dst} exists and is not empty (never overwrite a merged run)")
if not os.path.isfile(a.think):
    sys.exit(f"REFUSED: think answers {a.think} missing")

th = {}
for line in open(a.think):
    r = json.loads(line)
    _, rid, qk = r["key"].split("|", 2)
    th[(rid, qk)] = r.get("pred_key")

os.makedirs(dst, exist_ok=True)
for f in os.listdir(src):
    if f != "results.jsonl" and os.path.isfile(f"{src}/{f}"):
        shutil.copy(f"{src}/{f}", dst)
changed = 0
with open(f"{dst}/results.jsonl", "w") as fo:
    for line in open(f"{src}/results.jsonl"):
        r = json.loads(line)
        ans = (r.get("response") or {}).get("answers") or {}
        for qk, x in ans.items():
            pk = th.get((r["run_id"], qk))
            if pk is None or x.get("type") != "choice" or pk not in (x.get("probabilities") or {}):
                continue
            keys = list(x["probabilities"])
            rest = 0.1 / max(len(keys) - 1, 1)
            x["probabilities"] = {k2: (0.9 if k2 == pk else rest) for k2 in keys}
            x["choice"] = pk
            changed += 1
        fo.write(json.dumps(r) + "\n")
print(json.dumps({"think_answers": len(th), "answers_replaced": changed, "dst": dst}))
if a.parity:
    same = filecmp.cmp(f"{dst}/results.jsonl", f"{os.path.abspath(a.parity)}/results.jsonl", shallow=False)
    print("PARITY OK" if same else "PARITY FAIL: results.jsonl differs from " + a.parity)
    sys.exit(0 if same else 1)
