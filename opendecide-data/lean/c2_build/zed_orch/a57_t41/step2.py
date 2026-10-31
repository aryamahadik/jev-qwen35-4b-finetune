"""A57 step 2 for T41: regenerate task files (held-out quotas 0), delete held-out answers, hash-check, sha manifest."""
import hashlib, json, shutil, sys, time
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
import ac_hash as A
from families.T41 import haiku_author as H

AUTH = H.ROOT
Q = C2 / "a57_pool_quarantine" / "T41"
LOG = Path(__file__).parent / "step2_log.json"
log = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}

# held-out answers that exist anywhere in the T41 haiku / quarantine folders
answers = [p for d in (AUTH.parent, Q) if d.exists() for p in d.rglob("*.json") if "answers" in p.parts or p.parent == Q]
log["existing_answer_files_before"] = len(answers)
log["held_out_answers_deleted"] = 0

# before quotas
bk0 = AUTH / "_backup_a57_pre"
old = json.loads(((bk0 if bk0.exists() else AUTH) / "TASKS.json").read_text())
log["old_tasks"] = {"n": len(old["tasks"]), "items": sum(t["n_items"] for t in old["tasks"])}
old_plans = [json.loads(p.read_text()) for p in ((bk0 if bk0.exists() else AUTH) / "plan").glob("*.json")]
log["held_out_items_planned_before"] = sum(1 for pl in old_plans for v in pl["plan"].values() if v["held_out"])

bk = AUTH / "_backup_a57_pre"
if not bk.exists():
    bk.mkdir()
    for n in ("TASKS.json", "tasks", "chunks", "key", "manifest", "plan", "prompts"):
        shutil.move(str(AUTH / n), str(bk / n))
Q.mkdir(parents=True, exist_ok=True)
tasks = H.write_tasks(AUTH, answer_root=Q)
log["new_tasks"] = {"n": len(tasks), "items": sum(t["n_items"] for t in tasks),
                    "by_batch": {b: sum(t["n_items"] for t in tasks if t["batch"] == b) for b in {t["batch"] for t in tasks}}}
new_plans = [json.loads(p.read_text()) for p in (AUTH / "plan").glob("*.json")]
log["held_out_items_planned_after"] = sum(1 for pl in new_plans for v in pl["plan"].values() if v["held_out"])
log["quotas"] = {"N_SKIN_HELD": H.N_SKIN_HELD, "N_WORDING_HELD": H.N_WORDING_HELD, "N_DELEG_HELD": H.N_DELEG_HELD,
                 "N_ATTACK_HELD": H.N_ATTACK_HELD}

# hash check: whole file, plus every string leaf of the items
ex = A.ACExports()
log["ac_manifest_sha256"] = ex.manifest_sha
log["ac_final_suite_sha256"] = ex.manifest.get("final_suite_sha256")
texts = {}
for t in tasks:
    raw = Path(t["task_file"]).read_text(encoding="utf-8")
    parts = [raw]
    ch = json.loads((AUTH / "chunks" / f"{t['task_id']}.json").read_text())
    def leaves(o):
        if isinstance(o, str): yield o
        elif isinstance(o, dict):
            for v in o.values(): yield from leaves(v)
        elif isinstance(o, list):
            for v in o: yield from leaves(v)
    parts += list(leaves(ch.get("items", ch)))
    texts[t["task_id"]] = parts
hits, rep = A.check_texts(ex, texts)
log["hash_check"] = {"files": len(texts), "texts": sum(len(v) for v in texts.values()),
                     "hit_files": len({k for m in hits.values() for k in m}),
                     "by_method": {m: len(v) for m, v in hits.items()}}
# positive control (in memory): inject one known text and require a hit
ctl = "this control sentence must be found by the exact hash check route"
ex.sets["full_text_norm_min5words"].add(A.G.sha_hex(A.G.norm(ctl)))
h2, _ = A.check_texts(ex, {"ctl": [ctl]})
log["control_hit"] = bool(h2)
ex.sets["full_text_norm_min5words"].discard(A.G.sha_hex(A.G.norm(ctl)))

# sha256 manifest
man = {}
for t in sorted(tasks, key=lambda x: x["task_id"]):
    man[t["task_id"]] = {"sha256": hashlib.sha256(Path(t["task_file"]).read_bytes()).hexdigest(), "n_items": t["n_items"],
                         "task_file": t["task_file"], "answer_file": t["answer_file"]}
mp = Path(__file__).parent / "T41_task_manifest.json"
mp.write_text(json.dumps({"family": "T41", "ruling": "A57 step 2", "tasks": man}, indent=1, sort_keys=True) + "\n")
log["manifest_path"] = str(mp)
log["manifest_sha256"] = hashlib.sha256(mp.read_bytes()).hexdigest()
LOG.write_text(json.dumps(log, indent=1) + "\n")
print(json.dumps(log, indent=1))
