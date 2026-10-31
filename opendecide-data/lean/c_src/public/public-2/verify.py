"""public-2 round-trip label check on the final files (rows, reserve, dev). Independent of the renderers:

- Threshold yes/no rows (WikiSQL ws_count_yn / ws_agg_yn, DROP drop_thr_yn): parse the comparison phrase and T back
  from the rendered instruction text, take the value x from the candidate record (WikiSQL: the solver-A/B agreed
  execution; DROP: the crowd number), and recompute yes/no.
- UCI rows: parse the attribute values back from the rendered case text, look the record up in the published data file
  (solver B = published class), and recompute the gold (choice: class name or masked code read from the card; yes/no:
  'classed as X' or 'at least X' read from the instruction text, class order read from the card).
- Every choice row: gold is one of the options and the options are distinct.
Exit 1 on any mismatch.
"""
import json
import re
import sys
from fractions import Fraction

from p2_common import OUT, RAW, TMP

PHR = [("greater than or equal to", ">="), ("no less than", ">="), ("no fewer than", ">="), ("at least", ">="),
       ("not more than", "<="), ("no more than", "<="), ("at most", "<="), ("more than", ">"),
       ("greater than", ">"), ("above", ">"), ("less than", "<"), ("fewer than", "<"), ("below", "<"),
       ("under", "<")]


def parse_cmp(instr):
    for ph, op in PHR:
        m = re.search(re.escape(ph) + r" (-?[\d.]+)", instr)
        if m:
            return op, Fraction(m.group(1).rstrip("."))
    return None


def cmp(x, op, T):
    return {">": x > T, ">=": x >= T, "<": x < T, "<=": x <= T}[op]


def main():
    cand = {}
    for n in ("cand_wikisql", "cand_drop", "cand_uci", "cand_hybridqa"):
        for line in open(TMP / f"{n}.jsonl"):
            r = json.loads(line)
            cand[r["id"]] = r
    uci_data = {}
    for key, fn, attrs in (("car", "car.data", ["buying price", "maintenance price", "doors", "seats (persons carried)",
                                                  "luggage boot", "safety"]),
                           ("nursery", "nursery.data", ["parents' occupation", "child's current nursery",
                                                         "family form", "number of children", "housing", "finances",
                                                         "social conditions", "health"])):
        uci_data[key] = (attrs, [l.strip().split(",") for l in open(RAW / fn) if l.strip()])
    from build_uci import SPEC
    bad, n_checked = [], {"threshold": 0, "uci": 0, "choice": 0}
    for fn in ("rows_r1", "reserve_r1", "dev_mt_r1"):
        for line in open(OUT / f"{fn}.jsonl"):
            r = json.loads(line)
            fr = r["meta"]["framing"]
            if r["qtype"] == "choice":
                n_checked["choice"] += 1
                if r["gold"] not in r["options"] or len(set(r["options"])) != len(r["options"]):
                    bad.append((r["id"], "options"))
            if fr in ("ws_count_yn", "ws_agg_yn", "drop_thr_yn"):
                n_checked["threshold"] += 1
                pc = parse_cmp(r["instructions"])
                x = Fraction(cand[r["id"]]["_x"]["x"])
                if not pc or int(cmp(x, *pc)) != r["gold"]:
                    bad.append((r["id"], "threshold"))
            if r["source"].startswith("c_pub_uci"):
                n_checked["uci"] += 1
                key = "car" if r["source"].endswith("car") else "nursery"
                spec = SPEC[key]
                attrs, data = uci_data[key]
                inv = {v: k for k, v in spec["val_names"].items()}
                st = r["state"]
                vals = []
                for a in attrs:
                    m = re.search(re.escape(a) + r"\"?\s*[:=]\s*\"?([^\";\n|}]+)", st)
                    if m:
                        vals.append(m.group(1).strip().rstrip("."))
                if len(vals) != len(attrs):  # markdown row: header line then value line
                    lines = [l for l in st.split("\n") if l.startswith("|") and "---" not in l]
                    vals = [c.strip() for c in lines[1].strip("|").split("|")]
                codes = [inv[v] for v in vals]
                hits = [d[-1] for d in data if d[:-1] == codes]
                if len(hits) != 1:
                    bad.append((r["id"], "uci_lookup"))
                    continue
                published = hits[0]
                cn = spec["class_names"]
                order_best = list(reversed(spec["model"]["classes"]))
                if r["qtype"] == "choice":
                    # v1.1: masked class codes are '- {code}: {class name}' card lines (shown on the option lines);
                    # the model itself sits in instructions
                    defs = {}
                    for ln in (r["card"] or "").split("\n"):
                        if ln.startswith("- ") and ": " in ln:
                            k, v = ln[2:].split(": ", 1)
                            defs[k] = v
                    if defs:
                        code = {name: c for c, name in defs.items()}
                        exp = code[cn[published]]
                        if set(defs) != set(r["options"]):
                            bad.append((r["id"], "uci_codes_vs_options"))
                    else:
                        exp = cn[published]
                    if "Final class (from" not in r["instructions"]:
                        bad.append((r["id"], "uci_model_not_in_instructions"))
                    if r["gold"] != exp:
                        bad.append((r["id"], "uci_choice"))
                else:
                    names = [k for k, v in cn.items() if f"'{v}'" in r["instructions"]]
                    if len(names) != 1:
                        bad.append((r["id"], "uci_parse"))
                        continue
                    asked = names[0]
                    if "at least" in r["instructions"] or "or better" in r["instructions"] or "or a better" in r["instructions"]:
                        exp = int(order_best.index(published) <= order_best.index(asked))
                    else:
                        exp = int(asked == published)
                    if r["gold"] != exp:
                        bad.append((r["id"], "uci_yn"))
    res = {"checked": n_checked, "mismatches": len(bad), "bad_ids": bad[:20]}
    json.dump(res, open(OUT / "verify_report.json", "w"), indent=1)
    print(json.dumps(res))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
