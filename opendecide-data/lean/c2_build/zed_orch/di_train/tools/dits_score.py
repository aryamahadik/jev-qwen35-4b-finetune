"""A46-style scoring of DI-TS reads. Usage: python -B dits_score.py <di_train_dir>"""
import sys, json, glob, os, collections
D = sys.argv[1]; R = f"{D}/DI-TS/reads"
key = json.load(open(f"{R}/keys/key.json"))
rows = {}
for f in ("candidates_stage.jsonl", "mixdev_S5_stage.jsonl"):
    for l in open(f"{D}/DI-TS/stage/{f}", encoding="utf8"):
        x = json.loads(l); rows[x["id"]] = x
tasks = json.load(open(f"{R}/TASKS.json"))
ans = {}; probs = collections.Counter()
for tid, t in tasks.items():
    try: a = json.load(open(t["answer_file"]))
    except Exception as e: probs["unreadable:" + tid] += 1; continue
    seen = set()
    for o in a:
        q = o.get("qid"); k = f'{t["reader"]}:{q}'
        if k not in key: probs["unknown_qid"] += 1; continue
        if k in seen: probs["dup"] += 1; continue
        seen.add(k)
        rid = key[k]; opts = eval(rows[rid]["options"]) if isinstance(rows[rid]["options"], str) else rows[rid]["options"]
        v = o.get("answer")
        if v != "abstain" and v not in opts: probs["bad_option"] += 1; v = "invalid"
        ans[(t["reader"], rid)] = v
missing = [k for k in key if (k.split(":")[0], key[k]) not in ans]
flag = []; stats = collections.defaultdict(lambda: collections.Counter())
for rid, x in rows.items():
    a, b = ans.get(("A", rid)), ans.get(("B", rid)); g = x["gold"]
    fam = x["meta"]["card_id"].split(":")[1] if isinstance(x["meta"], dict) else rid
    ok = lambda v: v == g; ab = lambda v: v in (None, "abstain", "invalid")
    st = stats[fam]; st["n"] += 1
    if ok(a) and ok(b): st["both_agree_gold"] += 1
    elif (not ok(a) and not ab(a) and not ok(b) and not ab(b)) or ((not ok(a) and not ab(a)) and ab(b)) or ((not ok(b) and not ab(b)) and ab(a)):
        flag.append(rid); st["flagged"] += 1
    else: st["one_disagrees_stays"] += 1
print(dict(probs), "missing", len(missing), "flagged", len(flag))
for f, s in stats.items(): print(f, dict(s))
json.dump({"flagged": flag, "problems": dict(probs), "missing": len(missing), "stats": {k: dict(v) for k, v in stats.items()}}, open(f"{R}/SCORE.json", "w"), indent=1)
