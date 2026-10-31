"""Score G5 after the wording rebuild (A32 (b)): kept rows take their g5r3 answer (qc/tmp/g5r3_ans.txt, indexed by
g5r3 sample position, perms qc/tmp/g5r3_perms.json); fresh rows take qc/tmp/g5w_ans.txt ('<new idx> <letter> [flag]',
perms qc/tmp/g5w_perms.json). Gold from the NEW out/candidates_r1.jsonl. Prints counts only -> qc/g5w.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import g5r3_blind as b3
F3 = b3.F3; WIDE = b3.dio.WIDE
P = json.loads((F3 / "qc/g5w_sample.json").read_text())
old_ids = json.loads((F3 / "qc/g5r3_sample_ids.json").read_text())["ids"]
old_pos = {rid: k for k, rid in enumerate(old_ids)}


def read_ans(path):
    ans, flags = {}, {}
    for l in open(path):
        p = l.split()
        if len(p) >= 2 and p[0].isdigit():
            ans[int(p[0])] = p[1]
            if len(p) >= 3:
                flags[int(p[0])] = " ".join(p[2:])
    return ans, flags


a3, f3 = read_ans(F3 / "qc/tmp/g5r3_ans.txt")
fp = F3 / "qc/tmp/g5w_ans.txt"
aw, fw = read_ans(fp) if fp.exists() else ({}, {})
p3 = json.loads((F3 / "qc/tmp/g5r3_perms.json").read_text())
pw = json.loads((F3 / "qc/tmp/g5w_perms.json").read_text()) if (F3 / "qc/tmp/g5w_perms.json").exists() else {}
want = set(P["ids"]); rows = {}
for l in open(F3 / "out/candidates_r1.jsonl"):
    r = json.loads(l)
    if r["id"] in want:
        rows[r["id"]] = r
kept = set(P["kept_idx"])
agree, mism, flags, answered = 0, [], {}, 0
for k, rid in enumerate(P["ids"]):
    if k in kept:
        a, perm, fl = a3.get(old_pos[rid]), p3[rid], f3.get(old_pos[rid])
    else:
        a, perm, fl = aw.get(k), pw.get(rid), fw.get(k)
    if a is None or perm is None:
        continue
    answered += 1
    if fl:
        flags[k] = fl
    r = rows[rid]
    opts = ["Yes", "No"] if r["qtype"] == "noul" else r["options"]
    i = WIDE.index(a) if a in WIDE else -1
    shown = [opts[j] for j in perm]
    pick = shown[i] if 0 <= i < len(shown) else None
    g = ("Yes" if r["gold"] == 1 else "No") if r["qtype"] == "noul" else r["gold"]
    if pick == g:
        agree += 1
    else:
        mism.append(k)
out = {"n": 300, "kept_g5r3_judgment": len(kept), "fresh_blind_read": len(P["fresh_idx"]),
       "fresh_answered": sum(1 for k in P["fresh_idx"] if k in aw), "answered": answered, "agree_with_gold": agree,
       "mismatch_idx": mism, "flags": flags}
out["pass"] = answered == 300 and not mism and not flags
(F3 / "qc/g5w.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out)[:600])
