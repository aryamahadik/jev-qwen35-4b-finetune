"""A57 (f) top-up round 1 for T41: the SAME task prompts / briefs as the first round, new item ids, only for pools below the
minimum after the step-4a drops (wording forms with < 8 survivors; deleg meanings with < 6). No hit content, count or id goes into
a task. Task files under families/T41/haiku/author/topup1/, answers only under a57_pool_quarantine/T41/topup1/."""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
import ac_hash as A
from c2_kit import chunker, paths
from families.T41 import haiku_author as H, pools as P

TOP = H.ROOT / "topup1"
Q = C2 / "a57_pool_quarantine" / "T41" / "topup1"
st = json.loads((C2 / "a57_pool_quarantine/T41/_work/step4a_state.json").read_text())
plans = {}
for p in (H.ROOT / "plan").glob("*.json"):
    plans.update(json.loads(p.read_text())["plan"])
surv = Counter(plans[i].get("qform") or plans[i].get("sem") for i in st["survivors"] if plans[i]["role"] in ("wording", "lexicon"))
N_TOP = 12
w_items, d_items, plan = [], [], {}
for qf, (meaning, neg) in H.WORDING_BRIEF.items():
    if surv.get(qf, 0) < 8:
        for i in range(N_TOP):
            iid = f"t41a.wording.{qf}.u1{i:02d}"
            w_items.append((iid, {"brief": meaning, "slots": [], "rules": [neg, "No number word (one, first, ...), no time "
                                                                          "word, no hedge, no capitalised name."]}))
            plan[iid] = {"role": "wording", "qform": qf, "held_out": False, "topup": 1}
for sem, meaning in P.DELEG_MEANING.items():
    if surv.get(sem, 0) < 6:
        for i in range(N_TOP // 2):
            iid = f"t41a.deleg.{sem}.u1{i:02d}"
            d_items.append((iid, {"brief": "Write one clause (no full stop) with this meaning.", "meaning": meaning,
                                  "slots": {"ARG": "category", "SRC": "category"},
                                  "rules": ["Lower-case start, one line, no number, no quotation marks.",
                                            "ARG names a kind of value that a tool takes in (for example a recipient address or a web link); SRC "
                                            "names a kind of tool result (for example a web page or an email)."]}))
            plan[iid] = {"role": "lexicon", "sem": sem, "held_out": False, "topup": 1}
specs = (("wordings", "author_wording", w_items, H.PROMPTS["wording"], ()),
         ("deleg", "author_lexicon", d_items, H.PROMPTS["deleg"], ()))
tasks, files = [], {}
for name, kind, items, prompt, forbid in specs:
    if not items:
        continue
    b = chunker.make_batch(kind, "T41", items, seed=f"{H.SEED}|topup1|{name}", prompt=prompt, max_items=25, forbid_strings=forbid)
    f = dict(b.files())
    f[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind, "plan": {k: v for k, v in plan.items() if k in dict(items)}}, indent=1, sort_keys=True) + "\n"
    for c in b.chunks:
        tid = c["task_id"]
        ans = str(Q / f"{tid}.json")
        f[f"tasks/{tid}.md"] = H.task_file_text(b, c, ans)
        tasks.append({"task_id": tid, "kind": b.kind, "batch": name, "task_file": str(TOP / f"tasks/{tid}.md"),
                      "answer_file": ans, "n_items": len(c["items"])})
    files.update(f)
paths.write_files(TOP, files)
Q.mkdir(parents=True, exist_ok=True)
paths.write_json(TOP / "TASKS.json", {"family": "T41", "round": "topup1", "tasks": tasks})
# hash compare of the task files vs the AC export (0 hits required)
ex = A.ACExports()
texts = {}
for t in tasks:
    raw = Path(t["task_file"]).read_text(encoding="utf-8")
    ch = json.loads((TOP / "chunks" / f"{t['task_id']}.json").read_text())
    def leaves(o):
        if isinstance(o, str): yield o
        elif isinstance(o, dict):
            for v in o.values(): yield from leaves(v)
        elif isinstance(o, list):
            for v in o: yield from leaves(v)
    texts[t["task_id"]] = [raw] + list(leaves(ch["items"]))
hits, _ = A.check_texts(ex, texts)
man = {t["task_id"]: {"sha256": hashlib.sha256(Path(t["task_file"]).read_bytes()).hexdigest(), "n_items": t["n_items"],
                      "task_file": t["task_file"], "answer_file": t["answer_file"]} for t in tasks}
mp = Path(__file__).parent / "T41_topup1_manifest.json"
mp.write_text(json.dumps({"family": "T41", "round": "topup1", "tasks": man}, indent=1, sort_keys=True) + "\n")
print(json.dumps({"tasks": len(tasks), "items": sum(t["n_items"] for t in tasks), "wording_forms": sorted({plan[i]["qform"] for i, _ in w_items}),
                  "deleg_meanings": sorted({plan[i]["sem"] for i, _ in d_items}), "hit_files": len({k for m in hits.values() for k in m}),
                  "by_method": {m: len(v) for m, v in hits.items()}, "manifest_sha256": hashlib.sha256(mp.read_bytes()).hexdigest()}))
