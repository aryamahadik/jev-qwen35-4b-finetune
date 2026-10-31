"""G6 (report only, A61 c7): hypothesis-only partial-input baseline, 5-fold CV (multinomial NB, word uni+bigrams) vs the majority share. Never admits or drops a row."""
import sys, json, math, random, re, collections, hashlib
D = sys.argv[1]
rows = [json.loads(l) for l in open(f"{D}/DI-TS/stage/candidates_stage.jsonl", encoding="utf8")]
def hyp(r):
    s = r["state"].split("\n")[-1]; return s.split(": ", 1)[1] if ": " in s else s
def feats(t):
    w = re.findall(r"[a-z0-9~&|>()]+", t.lower()) if False else re.findall(r"\w+|[~&|>()]", t.lower())
    return w + [a + "_" + b for a, b in zip(w, w[1:])]
out = {}
for task in sorted({r["meta"]["task_id"] for r in rows}):
    R = [r for r in rows if r["meta"]["task_id"] == task]
    rnd = random.Random(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16)); rnd.shuffle(R)
    labs = sorted({r["gold"] for r in R}); K = 5; acc = []
    for k in range(K):
        te = R[k::K]; tr = [r for i, r in enumerate(R) if i % K != k]
        cnt = {l: collections.Counter() for l in labs}; prior = collections.Counter(r["gold"] for r in tr)
        for r in tr: cnt[r["gold"]].update(feats(hyp(r)))
        V = len({f for c in cnt.values() for f in c}) + 1; tot = {l: sum(cnt[l].values()) for l in labs}
        ok = 0
        for r in te:
            sc = {l: math.log(prior[l] / len(tr)) + sum(math.log((cnt[l][f] + 1) / (tot[l] + V)) for f in feats(hyp(r))) for l in labs}
            ok += max(sc, key=sc.get) == r["gold"]
        acc.append(ok / len(te))
    maj = max(collections.Counter(r["gold"] for r in R).values()) / len(R)
    out[task] = {"n": len(R), "hyp_only_cv_acc": round(sum(acc) / K, 4), "majority_share": round(maj, 4), "chance_1_over_k": round(1 / len(labs), 4), "excess_over_majority_pp": round(100 * (sum(acc) / K - maj), 2)}
json.dump(out, open(f"{D}/DI-TS/stage/G6_REPORT_ONLY.json", "w"), indent=1); print(json.dumps(out, indent=1))
