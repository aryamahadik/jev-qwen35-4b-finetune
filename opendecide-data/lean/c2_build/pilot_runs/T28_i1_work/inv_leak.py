"""T28 i1 diagnostic: what separates the gold call from the wrong candidates of ch_inverted rows (cached 5k build)."""
import pickle, re, sys, collections, statistics
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot
infos, stats = pickle.load(open(sys.argv[1], "rb"))
inv = [i for i in infos if i.row["meta"]["qform"] == "ch_inverted" and i.row["role"] == "base"]
print("inverted base rows", len(inv))
tool_in = collections.Counter(); ov = {"gold": [], "wrong": []}; argov = {"gold": [], "wrong": []}
toolhit = {"gold": 0, "wrong": 0}; n = {"gold": 0, "wrong": 0}
best = collections.Counter()
ex = 0
for i in inv:
    r = i.row
    vis = (r.get("state", "") + "\n" + (r.get("card") or "") + "\n" + r["instructions"]).lower()
    vt = set(pilot.toks(i.context))
    scores = []
    for o in r["options"]:
        role = "gold" if o == r["gold"] else "wrong"
        tool = o.split("(")[0]
        t_in = tool.lower() in vis
        ou = set(pilot.toks(o))
        s = len(ou & vt) / max(1, len(ou))
        ov[role].append(s); toolhit[role] += t_in; n[role] += 1
        scores.append((s, role))
    top = max(s for s, _ in scores)
    best["gold_is_top" if any(s == top and r_ == "gold" for s, r_ in scores) else "gold_not_top"] += 1
    if ex < 3:
        ex += 1
        print(r["instructions"].split("\n\n")[-1])
        print(r["state"][:900])
        for o in r["options"]: print("   ", "*" if o == r["gold"] else " ", o)
print({k: round(statistics.mean(v), 3) for k, v in ov.items()})
print("tool name in visible text:", {k: round(toolhit[k] / n[k], 3) for k in n})
print(best)

# ---- split by candidate source: same tool as the gold (an argument variant) or another tool
cls = collections.defaultdict(list)
cnt = collections.Counter()
for i in inv:
    r = i.row
    vt = set(pilot.toks(i.context))
    gtool = r["gold"].split("(")[0]
    for o in r["options"]:
        if o == r["gold"]:
            kind = "gold"
        elif o.split("(")[0] == gtool:
            kind = "wrong_same_tool"
        else:
            kind = "wrong_other_tool"
        ou = set(pilot.toks(o))
        cls[kind].append(len(ou & vt) / max(1, len(ou)))
        cnt[kind] += 1
print({k: (cnt[k], round(statistics.mean(v), 3)) for k, v in cls.items()})
# gold top-overlap rate when only same-tool candidates are compared
same_only = tops = 0
for i in inv:
    r = i.row
    vt = set(pilot.toks(i.context))
    gtool = r["gold"].split("(")[0]
    cand = [o for o in r["options"] if o.split("(")[0] == gtool]
    if len(cand) < 2:
        continue
    sc = {o: len(set(pilot.toks(o)) & vt) / max(1, len(set(pilot.toks(o)))) for o in cand}
    same_only += 1
    tops += sc[r["gold"]] >= max(sc.values())
print("rows with >=2 same-tool candidates", same_only, "gold is top among them", tops, "expected ~", round(sum(1 / len([o for o in i.row['options'] if o.split('(')[0] == i.row['gold'].split('(')[0]]) for i in inv if len([o for o in i.row['options'] if o.split('(')[0] == i.row['gold'].split('(')[0]]) >= 2), 1))
