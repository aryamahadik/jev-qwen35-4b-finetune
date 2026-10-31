"""F6 carry: validate the 4 Haiku G5 delta answer files and write c_src/F6/tmp/a32b/g5_answers.jsonl ({"i","ans"} lines, the file
tmp/a32b/finalize_qc.py reads). Refuses on any missing/duplicate/invalid answer (nothing written). Then run, from c_src/F6:
  ../../../.venv/bin/python -B tmp/a32b/finalize_qc.py score        (counts only)
usage: convert_g5_answers.py [--audit-failed TASK_ID ...]   (answers of a reader whose file-access audit failed are ignored)"""
import json, re, sys
from pathlib import Path
LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
ST = LEAN / "c2_build/zed_orch/f6_carry/g5"; OUTF = LEAN / "c_src/F6/tmp/a32b/g5_answers.jsonl"
man = json.load(open(ST / "manifest.json")); skip = set(sys.argv[sys.argv.index("--audit-failed") + 1:]) if "--audit-failed" in sys.argv else set()
need = {}
for m in man:
    body = Path(m["task_file"]).read_text().split("## Items", 1)[1]
    for part in re.split(r"^######## ROW (\d+)\n", body, flags=re.M)[1:]:
        pass
    parts = re.split(r"^######## ROW (\d+)\n", body, flags=re.M)
    for k in range(1, len(parts), 2):
        need[int(parts[k])] = set(re.findall(r"^([A-Z]{1,2})\. ", parts[k + 1].split("Options:")[-1] if "Options:" in parts[k + 1] else parts[k + 1], re.M)) or None
probs, got = [], {}
for m in man:
    tid = Path(m["task_file"]).stem
    if tid in skip: probs.append(f"{tid}: audit failed, ignored"); continue
    p = Path(m["answer_file"])
    if not p.exists(): probs.append(f"{tid}: no answer file"); continue
    try: arr = json.loads(p.read_text())
    except Exception as e: probs.append(f"{tid}: invalid JSON"); continue
    if not isinstance(arr, list): probs.append(f"{tid}: not an array"); continue
    for a in arr:
        if not (isinstance(a, dict) and set(a) == {"i", "ans"} and isinstance(a["i"], int) and isinstance(a["ans"], str)): probs.append(f"{tid}: bad item"); continue
        if a["i"] not in [int(x) for x in m["rows"]]: probs.append(f"{tid}: row {a['i']} not in this task"); continue
        if a["i"] in got: probs.append(f"{tid}: row {a['i']} twice"); continue
        L = need.get(a["i"])
        if L and a["ans"] not in L: probs.append(f"{tid}: row {a['i']} answer not among the options"); continue
        got[a["i"]] = a["ans"]
miss = sorted(set(need) - set(got))
if miss: probs.append(f"unanswered rows {miss}")
print(json.dumps({"answered": len(got), "needed": len(need), "problems": probs}))
if probs: sys.exit(1)
assert not OUTF.exists(), f"{OUTF} exists"
OUTF.write_text("".join(json.dumps({"i": i, "ans": got[i]}) + "\n" for i in sorted(got)))
print("wrote", OUTF.name, len(got))
