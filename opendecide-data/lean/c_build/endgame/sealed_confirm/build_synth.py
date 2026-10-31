"""Build a SYNTHETIC suite + preds in sealed_confirm/run/ (no sealed data read), mimicking score_nd.py's input format."""
import hashlib, json, random, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
RUN = HERE / "run"
if RUN.exists():
    shutil.rmtree(RUN)
RUN.mkdir()
shutil.copy2(HERE.parents[2] / "sealed_nd" / "score_nd.py", RUN / "score_nd.py")  # code only, unmodified
rng = random.Random(1)
OPTS = ["alpha", "beta", "gamma"]
rows, k = [], 0
def add(part, dom, n):
    global k
    for j in range(n):
        g = "syn-g%04d" % ((k) // 2)
        split = "nd_select" if (j // 2) % 2 == 0 else "nd_confirm"
        qt = "choice" if j % 4 < 2 else "noul"
        r = {"id": "syn-%05d" % k, "group_id": g, "split": split, "qtype": qt, "prompt": "synthetic item",
             "meta": {"part": part, "domain_id": dom}}
        if qt == "choice":
            r["options"] = OPTS; r["gold"] = rng.choice(OPTS)
        else:
            r["gold"] = rng.randint(0, 1)
        rows.append(r); k += 1
for d in ("D1", "D2"): add("A", d, 160)
for d in ("P1", "P2", "P3"): add("P", d, 80)
add("B1", "B1", 80); add("B2", "B2", 80)
(RUN / "suite_v2.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
sh = hashlib.sha256((RUN / "suite_v2.jsonl").read_bytes()).hexdigest()
(RUN / "suite_v2.sha256").write_text(sh + "  suite_v2.jsonl\n")
(RUN / "manifest_v2.json").write_text(json.dumps({"suite_sha256": sh, "part_a_domains": ["D1", "D2"]}))
def preds(acc, seed):
    r = random.Random(seed); out = []
    for x in rows:
        ok = r.random() < acc
        if x["qtype"] == "choice":
            c = x["gold"] if ok else r.choice([o for o in OPTS if o != x["gold"]])
            out.append({"id": x["id"], "choice": c if r.random() < .5 else "ABC"[OPTS.index(c)]})
        else:
            out.append({"id": x["id"], "p_yes": (0.8 if x["gold"] else 0.2) if ok else (0.2 if x["gold"] else 0.8)})
    return out
w = lambda p, L: (RUN / p).write_text("".join(json.dumps(o) + "\n" for o in L))
w("cand.jsonl", preds(0.8, 2)); w("ref.jsonl", preds(0.6, 3))
w("cand_probs.jsonl", [{"id": x["id"], "model": "synth", "probs": {o: 1 / 3 for o in OPTS} if x["qtype"] == "choice"
                       else {"yes": .7, "no": .3}} for x in rows])
print(len(rows), "synthetic rows; sha", sh[:12])
