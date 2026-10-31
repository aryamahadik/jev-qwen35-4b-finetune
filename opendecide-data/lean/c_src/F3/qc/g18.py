"""G18 ordinal target lint (independent F3 checker). F3 G0 (R2-04): every F3 status vocabulary is unordered, so no
F3 row is ordinal, none carries meta.option_level, and G18 applies vacuously. This script checks that claim on every
row of candidates_r1, qc_sample and mixdev_S5: (1) 0 rows with meta.option_level; (2) qtype only noul / choice;
(3) lint: choice rows with >= 2 options that look like levels of an ordered scale (level / tier / stage / grade / rank
+ number or letter, ordinal words, low/medium/high style grades, or purely numeric option sets); every hit is listed.
Usage: g18.py (writes qc/g18.json)"""
import json, re
from collections import Counter
import qc_lib as L

LVL = re.compile(r"^(level|tier|stage|grade|rank|band|step|phase|class)\s*([0-9]+|[a-e]|i{1,3}|iv|v)\b", re.I)
ORD = re.compile(r"^(first|second|third|fourth|fifth|1st|2nd|3rd|4th|5th)\b", re.I)
GRADE = {"low", "medium", "high", "very low", "very high", "moderate", "minor", "major", "severe", "critical", "mild",
         "none", "slight", "extreme"}
NUM = re.compile(r"^[0-9]+(\.[0-9]+)?$")


def ordinal_like(opts):
    o = [x.strip() for x in opts]
    lv = sum(bool(LVL.match(x) or ORD.match(x)) for x in o)
    gr = sum(x.lower() in GRADE for x in o)
    nm = sum(bool(NUM.match(x)) for x in o)
    return lv >= 2 or gr >= 3 or (nm >= 2 and nm == len(o))


out = {"gate": "G18", "rule": "every ordinal row has option_level covering its options and round_half_even(E_target) "
       "== gold level; F3 G0 R2-04: F3 has no ordinal rows, so the check is that none exist"}
ok = True
for name in ("candidates_r1", "qc_sample", "mixdev_S5"):
    rows, _ = L.load(name)
    ol = [r["id"] for r in rows if "option_level" in r["meta"]]
    qt = Counter(r["qtype"] for r in rows)
    lint = [r["id"] for r in rows if r["qtype"] != "noul" and ordinal_like(r["options"] or [])]
    out[name] = {"rows": len(rows), "rows_with_option_level": len(ol), "qtype_counts": dict(qt),
                 "ordinal_like_option_sets": len(lint), "ordinal_like_ids": lint[:20]}
    ok = ok and not ol and set(qt) <= {"noul", "choice"} and not lint
out["ordinal_rows"] = sum(out[n]["rows_with_option_level"] for n in ("candidates_r1", "qc_sample", "mixdev_S5"))
out["pass"] = ok
(L.QC / "g18.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: (v if not isinstance(v, dict) else {a: b for a, b in v.items() if a != "ordinal_like_ids"}) for k, v in out.items()}))
