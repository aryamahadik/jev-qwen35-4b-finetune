"""Score T37b pilot_i1_full: G5-H (adjudication file) and S13 (polarity reads + blind solver). Writes into the pilot dir."""
import json, sys
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import pilot as P  # noqa
import pilot_t37b as PT  # noqa
from c2_kit import g5h, chunker, paths  # noqa
from t37b import builder as BL  # noqa

D = HERE / "t37b" / "pilot_i1_full"
rows = {r["id"]: r for r in (json.loads(l) for l in open(D / "rows.jsonl"))}
out = {}

# ---- G5-H
man, key = json.load(open(D / "g5h/manifest.json")), json.load(open(D / "g5h/key.json"))
raw = P._read_answers(man["tasks"])
ans = {}
for rd in ("A", "B"):
    tids = {t["task_id"] for t in man["tasks"] if t["reader"] == rd}
    got, probs = chunker.load_answers(P._KeyBatch(key["readers"][rd]), {t: a for t, a in raw.items() if t in tids and a is not None})
    ans[rd] = (got, probs)
read_rows = [rows[i] for i in key["row_ids"]]
tof = lambda r: [r["meta"]["t37b"]["template"]]
res = g5h.score(read_rows, key["items"], ans["A"][0], ans["B"][0], seed="T37b|i1full-g5h-control", template_of=tof)
adj, akey = g5h.adjudication_items(rows, res, seed="T37b|i1full-g5h-adj")
paths.write_json(D / "g5h/adjudication.json", {"family": "T37b", "items": [{"aid": a, **it} for a, it in adj],
                                               "verdicts_allowed": list(g5h.VERDICTS)})
paths.write_json(D / "g5h/adjudication_key.json", {"key": akey, "score": {k: v for k, v in res.items() if k != "per_row"},
                                                   "per_row": res["per_row"]})
print("G5H answered", {r: len(ans[r][0]) for r in ans}, "problems", {r: ans[r][1] for r in ans})
print("queue", len(res["queue"]), "controls", len(res["control"]), "quarantined", res["quarantined"])
print("template stats (disagree>0):", {t: d for t, d in res["templates"].items() if d["disagree"]})

# ---- S13
m13, k13 = json.load(open(D / "s13/manifest.json")), json.load(open(D / "s13/key.json"))
raw = P._read_answers(m13["tasks"])
pol = {}
for rd in ("A", "B"):
    tids = {t["task_id"] for t in m13["tasks"] if t.get("reader") == rd}
    got, probs = chunker.load_answers(P._KeyBatch(k13["polarity"][rd]), {t: a for t, a in raw.items() if t in tids and a is not None})
    pol[rd] = got
    print("pol", rd, len(got), probs)
blind = {}
for sd in ("base", "partner"):
    tids = {t["task_id"] for t in m13["tasks"] if t.get("side") == sd}
    got, probs = chunker.load_answers(P._KeyBatch(k13["blind"][sd]), {t: a for t, a in raw.items() if t in tids and a is not None})
    blind[sd] = got
    print("blind", sd, len(got), probs)
pool = PT.load_pool()
judged = pool.judged
bases = {}
for l in open(D / "bases.jsonl"):
    b = json.loads(l); bases[b.get("id")] = b
verd, reasons, units = Counter(), [], {}
for pid, rid in k13["partner_row_of_unit"].items():
    r = rows[rid]; t = r["meta"]["t37b"]
    want = BL.relation_of(t["kind"])
    base_gold = t["base_gold"]
    bq = bases[t["base_id"]]["instructions"]
    tail = t["template"].split("|", 3)[-1]
    pks = [BL.pair_key(bq, r["instructions"]), BL.pair_key(bq, tail)]
    try:
        from t37b import sources as SRC
        pks.append(BL.pair_key(SRC.pool_template({"id": t["entry"]})[0], tail))
    except Exception as e:
        print("pool_template fail", repr(e)[:100])
    pk = next((k for k in pks if k in judged or k in pol["A"]), pks[0])
    pa = pb = None
    if pk in judged:
        pa, pb = judged[pk]
    else:
        pa, pb = pol["A"].get(pk), pol["B"].get(pk)
    yb, yp = BL.norm_yesno(blind["base"].get(pid)), BL.norm_yesno(blind["partner"].get(pid))
    units[pid] = dict(row=rid, kind=t["kind"], want=want, pk_found=(pk in judged) or (pk in pol["A"]), pol=(BL.norm_relation(pa), BL.norm_relation(pb)),
                      blind=(yb, yp), base_gold=base_gold)
    if BL.norm_relation(pa) != want or BL.norm_relation(pb) != want:
        v, why = "drop", f"polarity {BL.norm_relation(pa)}/{BL.norm_relation(pb)} want {want}"
    elif yb is not None and yb != base_gold:
        v, why = "drop", "blind solver disagrees with human base gold"
    elif yb is not None and yp is not None and ((yb != yp) if want == "opposite" else (yb == yp)):
        v, why = "keep", "ok"
    else:
        v, why = "review", "blind pair inconsistent"
    verd[v] += 1
    units[pid]["verdict"], units[pid]["why"] = v, why
print("S13 verdicts", dict(verd), "pair keys not found:", sum(1 for u in units.values() if not u["pk_found"]))
paths.write_json(D / "s13/s13_scored.json", {"verdicts": dict(verd), "units": units})
print("reasons", Counter((u["verdict"], u["why"][:40]) for u in units.values()))
print("unfound by kind", Counter(u["kind"] for u in units.values() if not u["pk_found"]))
print("pol answers: A", len(pol["A"]), "B", len(pol["B"]), "judged_at_pool", len(k13["judged_at_pool"]))
for pid, u in list(units.items()):
    if u["verdict"] != "keep" and u["pk_found"]:
        print(pid, u)
