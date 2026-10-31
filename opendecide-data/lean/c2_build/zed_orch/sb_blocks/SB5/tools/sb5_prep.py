"""SB5 prep (A58 c 3-5): parse the UCI 293 archive, format filters, within-dedupe (G12), bench + C2 dev/eval exclusion
(program only, counts out), seeded 150 hold-out (label-stratified). Writes work/pool.json (ids, labels, text) and
work/prep_report.json. Usage: python -B sb5_prep.py"""
import glob, gzip, json, os, sys
from collections import Counter
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from sb5_lib import *
import c2io

recs = load_archive()
drops = {}                       # rid -> reason
rep = {"archive_files": len(recs), "by_label": dict(Counter(r["label"] for r in recs)),
       "cp1256_files": sum(r["enc"] == "cp1256" for r in recs)}

# ---- format filters (drop only) ----
for r in recs:
    t = r["text"]
    if not t:
        drops[r["rid"]] = "empty"
    elif len(t.split()) < 2:
        drops[r["rid"]] = "fewer_than_2_words"
    elif not AR.search(t):
        drops[r["rid"]] = "no_arabic_letters"
rep["after_format_filters"] = len(recs) - len(drops)

# ---- G12 within-dataset dedupe: exact normalised, then word 5-gram Jaccard >= 0.8 ----
live = [r for r in recs if r["rid"] not in drops]
toks = {r["rid"]: norm_tokens(r["text"]) for r in live}
groups, key_of = {}, {}
for r in live:
    k = " ".join(toks[r["rid"]])
    groups.setdefault(k, []).append(r)
dupset = []
for k, g in groups.items():
    if len(g) > 1:
        dupset.append(g)
# near-dup among distinct keys (>= 5 tokens)
reps = [g[0] for g in groups.values()]
gr = {r["rid"]: grams(toks[r["rid"]]) for r in reps}
inv = {}
for r in reps:
    for x in gr[r["rid"]]:
        inv.setdefault(x, []).append(r["rid"])
parent = {r["rid"]: r["rid"] for r in reps}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for r in reps:
    a = r["rid"]; c = set()
    for x in gr[a]: c.update(inv[x])
    for b in c:
        if b > a and gr[a] and gr[b] and len(gr[a] & gr[b]) / len(gr[a] | gr[b]) >= 0.8:
            parent[find(b)] = find(a)
clusters = {}
for r in live:
    k = " ".join(toks[r["rid"]])
    root = find(groups[k][0]["rid"])
    clusters.setdefault(root, []).append(r)
conflict = nd = 0
for root, g in clusters.items():
    if len(g) == 1:
        continue
    labs = {x["label"] for x in g}
    if len(labs) > 1:                       # same text, different human label: the label is unsafe, drop the whole cluster
        for x in g: drops[x["rid"]] = "dup_label_conflict"
        conflict += len(g)
    else:                                   # keep one (lowest hash), drop the rest
        g.sort(key=lambda x: h("dedupe", x["rid"]))
        for x in g[1:]: drops[x["rid"]] = "dup_within"
        nd += len(g) - 1
rep["dedupe"] = {"dropped_dup_within": nd, "dropped_label_conflict_rows": conflict, "clusters_gt1": sum(len(g) > 1 for g in clusters.values())}

# ---- exclusion indexes (counts only) ----
excl = Counter(); per_target = {}
def build(name, items):
    ix = Index()
    for it in items:
        for s in segments(it):
            ix.add(name, s)
    per_target[name] = ix.n_seg
    return ix
targets = {}
bench_items = []
for p in [BENCH / "text_track/data/cases.jsonl"] + sorted((BENCH / "data").glob("*/cases.jsonl")):
    for l in open(p, encoding="utf-8"):
        o = json.loads(l); bench_items.append({"state": o.get("state"), "questions": o.get("questions")})
targets["bench_cases"] = build("bench_cases", bench_items)
pins = SB5 / "bench_pins"
items = []
for l in gzip.open(pins / "mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz", "rt", encoding="utf-8"):
    items.append(json.loads(l))
targets["tweet_sentiment_ar_test_full"] = build("tweet_sentiment_ar_test_full", items)
import pyarrow.parquet as pq
tb = pq.read_table(pins / "arbml__OSACT4_hatespeech/data/validation-00000-of-00001.parquet").to_pylist()
targets["osact4_validation_full"] = build("osact4_validation_full", tb)
items = []
for sub in ("SetFit__amazon_massive_scenario_ar-SA", "SetFit__amazon_massive_intent_ar-SA"):
    for l in open(pins / sub / "test.jsonl", encoding="utf-8"):
        items.append(json.loads(l))
targets["massive_ar_test_full"] = build("massive_ar_test_full", items)
tb = pq.read_table(pins / "facebook__xnli/ar/test-00000-of-00001.parquet").to_pylist()
targets["xnli_ar_test_full"] = build("xnli_ar_test_full", tb)
# C2 dev / eval files (the G13 C2-dev paths plus any lean/data dev or eval jsonl that the never-open rule allows)
paths = []
for pat in ("data/c2_mixdev.jsonl", "data/c2_transfer_dev.jsonl", "data/c2_parts/*/out/mixdev_S5.jsonl", "data/*dev*.jsonl", "data/*eval*.jsonl"):
    for p in sorted(glob.glob(str(LEAN / pat))):
        if not c2io.refusal(p) and not c2io.refusal(os.path.realpath(p)) and p not in paths:
            paths.append(p)
cx = Index(); nrow = 0
for p in paths:
    with open(p, encoding="utf-8") as f:
        for l in f:
            if not AR.search(l):
                continue
            nrow += 1
            for s in segments(json.loads(l)):
                cx.add("c2_dev_eval", s)
targets["c2_dev_eval"] = cx
per_target["c2_dev_eval"] = cx.n_seg
rep["c2_dev_eval_files"] = len(paths); rep["c2_dev_eval_arabic_rows"] = nrow
rep["target_arabic_segments"] = per_target
live = [r for r in recs if r["rid"] not in drops]
for r in live:
    for name, ix in targets.items():
        hit = ix.hit(r["text"])
        if hit:
            drops[r["rid"]] = f"bench_or_dev:{name}:{hit[0]}"; excl[f"{name}:{hit[0]}"] += 1
            break
rep["bench_dev_exclusion_drops"] = dict(excl)

kept = [r for r in recs if r["rid"] not in drops]
rep["kept_pool"] = {"n": len(kept), "by_label": dict(Counter(r["label"] for r in kept))}
rep["drops_by_reason"] = dict(Counter(v.split(":")[0] if not v.startswith("bench") else "bench_or_dev" for v in drops.values()))

# ---- seeded hold-out: 75 per label, drawn before any read ----
dev = []
for lab in ("pos", "neg"):
    xs = sorted((r for r in kept if r["label"] == lab), key=lambda r: h("holdout", r["rid"]))
    dev += [r["rid"] for r in xs[:75]]
rep["holdout"] = {"n": len(dev), "by_label": {"pos": 75, "neg": 75}, "rule": "sha256(20261013|holdout|rid) order, first 75 per label of the kept pool"}
json.dump({"kept": kept, "dev_ids": dev, "drops": drops}, open(WORK / "pool.json", "w", encoding="utf-8"), ensure_ascii=False)
rep["pool_sha256"] = sha((WORK / "pool.json").read_bytes())
json.dump(rep, open(WORK / "prep_report.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
