"""G5 r2 scorer: maps the reader's letters (tmp/g5r2_ans.txt, '<k> <LETTER> [flag]' per line; flag = wrong |
ambiguous, the reader's own judgement of the row) back to option texts through tmp/g5r2_perms.json and compares
with gold. Prints indices and counts only."""
import json
from pathlib import Path
LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F3 = LEAN / "c_src/F3"
U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; WIDE = list(U) + [a + b for a in U for b in U]
IDS = json.loads((F3 / "qc/g5r2_sample_ids.json").read_text())["ids"]
perms = json.loads((F3 / "qc/tmp/g5r2_perms.json").read_text())
ans, flags = {}, {}
for l in open(F3 / "qc/tmp/g5r2_ans.txt"):
    p = l.split()
    if len(p) >= 2 and p[0].isdigit():
        ans[int(p[0])] = p[1]
        if len(p) >= 3:
            flags[int(p[0])] = p[2]
want = set(IDS); rows = {}
for l in open(F3 / "out/candidates_r1.jsonl"):
    r = json.loads(l)
    if r["id"] in want:
        rows[r["id"]] = r
agree, mism = 0, []
for k, rid in enumerate(IDS):
    if k not in ans:
        continue
    r = rows[rid]; p = perms[rid]
    opts = ["Yes", "No"] if r["qtype"] == "noul" else r["options"]
    i = WIDE.index(ans[k]) if ans[k] in WIDE else -1
    shown = [opts[j] for j in p]
    pick = shown[i] if 0 <= i < len(shown) else None
    g = ("Yes" if r["gold"] == 1 else "No") if r["qtype"] == "noul" else r["gold"]
    if pick == g:
        agree += 1
    else:
        mism.append(k)
print(json.dumps({"answered": len(ans), "agree": agree, "mismatch_idx": mism, "flags": flags}))
