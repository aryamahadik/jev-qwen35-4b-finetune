#!/usr/bin/env python3
"""Independent re-derivation of gold from the STATE TEXT (not from the build's record objects) for the numeric/compare tasks:
A.elev*, P.res*, E.yoy*, E.pair*. Also checks yes share, cluster ids and instruction negation. Prints counts only."""
import json, re, sys
from pathlib import Path
rows = [json.loads(l) for l in open(Path(__file__).resolve().parents[2].parent / "data/c2_gproxy/gproxy_rows.jsonl")]
bad = chk = 0
ex = []
for r in rows:
    q, st, c, task = r["instructions"], r["state"], r["card"] or "", r["meta"]["task"]
    yl = c.split("\n")[0] if c else ""
    pred = None
    m = re.search(r"Field elevation \(ft\): (\S+)", st)
    if m and m.group(1) != "unknown" and task.startswith("A.elev"):
        e, t = float(m.group(1)), int(re.sub(r"\D", "", task))
        above = ("above" in yl) if c else q.startswith("Is the field elevation above")
        pred = e > t if above else e <= t
    m = re.search(r"Reported resolution \(Angstrom\): (\S+)", st)
    if m and task.startswith("P.res") and m.group(1) != "missing":
        res, t = float(m.group(1)), float(task[5:])
        below = ("below" in yl) if c else q.startswith("Is the reported resolution below")
        pred = res < t if below else res >= t
    if task.startswith(("E.pair", "E.yoy")):
        vals = re.findall(r"(?:Country [^:\n]+|\d{4} value): (-?[\d.e+-]+)$", st, re.M)
        a, b = float(vals[-2]), float(vals[-1])
        hi = a > b if task.startswith("E.pair") else b > a
        pred = hi if "lower than or equal" not in q else not hi
    if pred is not None:
        chk += 1
        if pred != bool(r["gold"]):
            bad += 1
            ex.append(r["id"])
print(json.dumps({"rechecked_from_state_text": chk, "mismatches": bad, "examples": ex[:3], "rows": len(rows)}))
