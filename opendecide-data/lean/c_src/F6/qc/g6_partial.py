"""Write the G6 parts finished so far (from qc/g6.log of the running g6.py) to qc/g6_qc_sample.partial.json.
The full run keeps going and writes qc/g6_qc_sample.json when done. Counts only."""
import ast, json, re
import qc_lib as q
parts = {}
for l in open(q.QC / "g6.log"):
    m = re.match(r"\[\s*[\d.]+s\] (yn|choice) (\S+) (\{.*\})$", l.strip())
    if m:
        parts[f"{m.group(1)}:{m.group(2)}"] = ast.literal_eval(m.group(3))
out = {"gate": "G6", "file": "out/qc_sample.jsonl", "cv": "GroupKFold(5) by meta.card_id", "rule": "acc <= chance + 2 pp",
       "status": "partial: the full run is still going under machine load; parts finished so far", "parts": parts,
       "pass": all(v.get("pass", True) for v in parts.values()) and False if any(not v.get("pass", True) for v in parts.values()) else None}
json.dump(out, open(q.QC / "g6_qc_sample.partial.json", "w"), indent=1)
print(json.dumps(out))
