"""JOB3 audit A: gold-posture prior in disposition-like choice rows (option set holds a PERMIT label and a WITHHOLD/DENY label).
Counts only. Golden set = C1 training data; C2 candidates = c2_parts/<FAM>/out/candidates_c2.jsonl."""
import json, re, sys, collections, glob
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
PERMIT = re.compile(r"\b(approve[ds]?|accept(ed)?|allow(ed)?|pay|paid|release|grant(ed)?|proceed|continue|process|admit|authori[sz]e|permit(ted)?|fund|dispense|reimburse|pay the claim|go ahead|clear|ok|valid)\b", re.I)
HOLD = re.compile(r"\b(hold|pause|wait|review|refer(red)?|escalat\w*|ask|confirm\w*|defer|investigat\w*|route|send to|request|clarif\w*|manual|human|follow.?up|callback|verify|retest)\b", re.I)
DENY = re.compile(r"\b(reject(ed)?|refuse[ds]?|deny|denied|decline[ds]?|block(ed)?|stop|cancel|terminate|ban|remove|revoke|suspend|not eligible|no refund|forbidden|do not)\b", re.I)
ABST = re.compile(r"(cannot|can't|not determinable|insufficient|unknown|none of|not enough|unable|undetermined|no (record|information))", re.I)

def klass(lab):
    if ABST.search(lab): return "ABST"
    if DENY.search(lab): return "DENY"
    if HOLD.search(lab): return "HOLD"
    if PERMIT.search(lab): return "PERMIT"
    return "OTHER"

def analyse(rows, name):
    n = 0; shown = collections.Counter(); gold = collections.Counter(); both = 0
    for labs, g in rows:
        ks = [klass(l) for l in labs]
        kset = set(ks)
        if "PERMIT" in kset and (kset & {"HOLD", "DENY"}) and "OTHER" not in kset - {"OTHER"} | {"__"}:
            pass
        if "PERMIT" in kset and (kset & {"HOLD", "DENY"}):
            n += 1
            for k in kset: shown[k] += 1
            gold[klass(g)] += 1
    return {"disposition_rows": n, "shown": dict(shown), "gold": dict(gold)}

def golden():
    P = f"{LEAN}/data/v14_parts/golden_train.jsonl"
    by = collections.defaultdict(list)
    for line in open(P):
        r = json.loads(line)
        if r["qtype"] != "choice" or not r.get("card"): continue
        labs = [ln[2:].split(": ", 1)[0] for ln in r["card"].split("\n") if ln.startswith("- ") and ": " in ln]
        if len(labs) < 2: continue
        g = r["gold"]
        if isinstance(g, int): g = labs[g] if 0 <= g < len(labs) else None
        if g is None: continue
        by[r["source"]].append((labs, g))
    return by

if __name__ == "__main__":
    res = {}
    by = golden()
    for s, rows in by.items():
        a = analyse(rows, s)
        if a["disposition_rows"] >= 30: res["GOLD:" + s] = a
    for p in sorted(glob.glob(f"{LEAN}/data/c2_parts/*/out/candidates_c2.jsonl")):
        fam = p.split("/")[-3]
        rows = []
        for l in open(p):
            r = json.loads(l)
            if r["qtype"] != "choice": continue
            rows.append((r["options"], r["gold"]))
        a = analyse(rows, fam)
        if a["disposition_rows"] >= 30: res["C2:" + fam] = a
    json.dump(res, open("prior_audit.json", "w"), indent=1)
    for k, v in sorted(res.items(), key=lambda kv: -kv[1]["disposition_rows"]):
        n = v["disposition_rows"]
        g = {a: round(100 * b / n) for a, b in v["gold"].items()}
        print(f"{k:42s} n={n:6d} gold%={g}")
