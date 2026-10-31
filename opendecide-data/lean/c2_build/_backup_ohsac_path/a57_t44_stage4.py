"""A57 step 4 for T44 (quarantine answers only; drops only, nothing admitted). Counts and ids only. Mac, from c2_build:
  ../../.venv/bin/python -B zed_orch/a57_t44_stage4.py a        # format, haiku_author.check_wording (G-SL, negation, leaks), dups,
                                                                #   lexicon registry unit test, AC hash compare; writes glex tasks
  ../../.venv/bin/python -B zed_orch/a57_t44_stage4.py glex     # score the 2 blind reads (2/2 required)
  ../../.venv/bin/python -B zed_orch/a57_t44_stage4.py seed     # G13-seed stage 1 (engine + AC checkers) on glex survivors
"""
import hashlib, json, re, sys, time
from collections import Counter
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
from c2_kit import chunker as CH
from c2_kit.lexicon import LexiconRegistry, question_sem
from families.T44 import haiku_author as H, texts as TX
import a57_hashcheck_ac as HC
import g13_c2 as G

AUTH = H.TASK_ROOT
Q = C2 / "a57_pool_quarantine" / "T44"
W = Q / "_work"; W.mkdir(exist_ok=True)
GL = Q / "glex"
STATE, KEYF = W / "step4a_state.json", W / "glex_key.json"
OUT = C2 / "logs" / "a57"
READS = ("read1", "read2")
GPROMPT = ("You name the meaning of short English question lines. Each item gives one question line and a closed list of "
           "meanings. Pick the ONE meaning that the line expresses exactly, reading its words. If no meaning fits exactly, "
           "answer null. Do not answer the question.")


# Blind-read meanings: the same two meanings as TX.QUESTION_MEANINGS, with the one word ("listed") that is in the AC keyword
# export replaced (program fix of the read task text; the family meanings are unchanged).
GLEX_MEANINGS = {TX.HEAD_VERDICT: TX.QUESTION_MEANINGS[TX.HEAD_VERDICT],
                 TX.HEAD_NEXT: TX.QUESTION_MEANINGS[TX.HEAD_NEXT].replace("which listed call", "which of the offered calls")}


def registry(texts_by_iid, plans, program=True, meanings=None):
    reg = LexiconRegistry("T44")
    for qf, meaning in (meanings or TX.QUESTION_MEANINGS).items():
        reg.declare(question_sem("T44", qf), "question", meaning)
    fid = {}
    for qf, ws in TX.WORDINGS.items():
        for i, w in enumerate(ws if program else ()):
            fid[f"program.{qf}.{i}"] = reg.add(w, question_sem("T44", qf), family="T44").form_id
    for iid in sorted(texts_by_iid):
        fid[iid] = reg.add(texts_by_iid[iid], question_sem("T44", plans[iid]["head"]), family="T44").form_id
    return reg, fid


def stage_a():
    log = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
    tasks = json.loads((AUTH / "TASKS.json").read_text())["tasks"]
    keys, plans = {}, {}
    for p in (AUTH / "key").glob("*.json"):
        keys.update(json.loads(p.read_text())["key"])
    for p in (AUTH / "plan").glob("*.json"):
        plans.update(json.loads(p.read_text())["plan"])
    items, probs = {}, []
    for t in tasks:
        f = Path(t["answer_file"])
        try:
            arr = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            probs.append(f"{t['task_id']}: missing/not JSON"); continue
        want = [it["qid"] for it in json.loads((AUTH / "chunks" / f"{t['task_id']}.json").read_text())["items"]]
        got = {}
        for a in arr if isinstance(arr, list) else []:
            if isinstance(a, dict) and isinstance(a.get("qid"), str) and isinstance(a.get("text"), str) and set(a) <= {"qid", "text"}:
                got.setdefault(a["qid"], a["text"])
        if set(got) != set(want) or len(arr) != len(want):
            probs.append(f"{t['task_id']}: qids differ ({len(got)} vs {len(want)}; {len(arr)} entries)")
        for q in want:
            if q in got:
                items[keys[q]] = {"text": got[q], "plan": plans[keys[q]], "task": t["task_id"]}
    log.update(expected=sum(t["n_items"] for t in tasks), loaded=len(items), format_problems=probs)
    drops = {}
    seen_norm, seen_sets = set(), []
    for iid in sorted(items):                       # check_wording holds G-SL, negation profile, label/outcome leaks, dups
        pl = items[iid]["plan"]
        if pl.get("held_out") or pl.get("dev_only"):
            drops[iid] = "held_out_or_dev_only_role"; continue
        pr = H.check_wording(pl["head"], items[iid]["text"], seen_norm, seen_sets)
        if pr:
            drops[iid] = "check_wording"
            items[iid]["problem"] = re.sub(r"'[^']*'", "'..'", pr[0])[:60]
    texts = {i: items[i]["text"] for i in items if i not in drops}
    try:
        reg, fid = registry(texts, {i: items[i]["plan"] for i in texts})
    except Exception as e:                           # a registry-level failure: add one by one to find the dropped item
        reg = LexiconRegistry("T44")
        for qf, meaning in TX.QUESTION_MEANINGS.items():
            reg.declare(question_sem("T44", qf), "question", meaning)
        for qf, ws in TX.WORDINGS.items():
            for w in ws:
                reg.add(w, question_sem("T44", qf), family="T44")
        for iid in sorted(texts):
            try:
                reg.add(texts[iid], question_sem("T44", items[iid]["plan"]["head"]), family="T44")
            except Exception:
                drops[iid] = "lexicon_add"
        texts = {i: t for i, t in texts.items() if i not in drops}
        reg, fid = registry(texts, {i: items[i]["plan"] for i in texts})
    ut = reg.unit_test_all()
    for iid, f in fid.items():
        if not ut[f]:
            if iid.startswith("program."):
                log.setdefault("program_form_unit_fail", []).append(iid)
            else:
                drops[iid] = "lexicon_unit_test"
    # hash compare vs the OHS-AC freeze export (HC.run: n-gram 10/12, full-text, sentence, keyword, structure)
    ex = HC.ExportsAC(); st = HC.selftest(ex); assert all(st.values()), st
    units = [{"key": i, "texts": [("text", items[i]["text"])], "template": False} for i in items if i not in drops]
    r = HC.run(units, ex)
    for k in r["hit_ids"]:
        drops[k] = "ac_hash"
    log["ac_hash"] = {"manifest_sha256": r["manifest_sha256"], "stage": r["export_stage"], "manifest_verified": r["manifest_verified"],
                      "complete": r["complete"], "checked": len(units), "hit_items": len(r["hit_ids"]), "by_method": r["counts"]["by_method"]}
    surv = sorted(i for i in items if i not in drops)
    log["by_head"] = {h: {"authored": sum(1 for i in items if items[i]["plan"]["head"] == h),
                          "survive": sum(1 for i in surv if items[i]["plan"]["head"] == h),
                          "dropped_by_reason": dict(Counter(drops[i] for i in items if i in drops and items[i]["plan"]["head"] == h))}
                      for h in H.HEADS}
    log["problem_kinds"] = dict(Counter(f"{items[i]['plan']['head']}: {it['problem']}" for i, it in items.items() if it.get("problem")))
    log["survivors_after_4a"] = len(surv)
    STATE.write_text(json.dumps({"drops": drops, "survivors": surv, "texts": {i: items[i]["text"] for i in items},
                                 "plans": {i: items[i]["plan"] for i in items}}, indent=1, sort_keys=True))
    # G-LEX blind-read task files: two reads, different seeds -> different order / choice order; each file to a FRESH Haiku
    texts = {i: items[i]["text"] for i in surv}
    reg, fid = registry(texts, {i: items[i]["plan"] for i in surv}, program=False, meanings=GLEX_MEANINGS)
    reg.unit_test_all()
    man = {"reads": {}}
    for rd in READS:
        its = reg.lexicon_items(seed=f"a57-t44-{rd}")
        b = CH.make_batch("extract_lex", "T44", its, seed=f"a57-t44-{rd}", prompt=GPROMPT)
        for ch in b.chunks:
            tid = f"T44-glex-{rd}-{ch['task_id'].rsplit('-', 1)[1]}"
            n = len(ch["items"]); ans = GL / "answers" / f"{tid}.json"
            head = (f"# T44 G-LEX extraction task {tid}\n\nANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                    f"{ans}\n\nTask kind: extract_lex; items: {n}; answers expected: {n} (one per item, answer field \"choice\").\n\n"
                    "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n## Instructions\n\n"
                    "Each item gives one question and a list of meanings. Pick the ONE meaning in the list that the question expresses exactly, "
                    "reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether "
                    "anything is true.\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
                    "array with one entry per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the chosen meaning copied exactly, or null>\"}. "
                    "Valid JSON only; no text before or after the array. Run no other tool.\n\n"
                    "Answer format: [{\"qid\": \"<qid>\", \"choice\": \"<one meaning, copied exactly, or null>\"}, ...]\n\n"
                    "## Items (JSON; answer every item once, keyed by its qid)\n\n")
            tf = GL / "tasks" / f"{tid}.md"
            tf.parent.mkdir(parents=True, exist_ok=True); ans.parent.mkdir(parents=True, exist_ok=True)
            tf.write_text(head + json.dumps(ch["items"], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            man["reads"][tid] = {"read": rd, "task_file": str(tf), "answer_file": str(ans), "n": n,
                                 "sha256": hashlib.sha256(tf.read_bytes()).hexdigest(),
                                 "key": {q: b.key[q] for q in (it["qid"] for it in ch["items"])}}
    man["fid_of"] = fid
    KEYF.write_text(json.dumps(man, indent=1))
    ur = HC.run(HC.units_from_taskfiles(GL / "tasks", "*.md"), ex)
    log["glex_task_files"] = {"n": len(man["reads"]), "hash_hit_units": len(ur["hit_ids"]), "by_method": ur["counts"]["by_method"],
                              "sha256": {t: m["sha256"] for t, m in man["reads"].items()}}
    OUT.mkdir(exist_ok=True)
    (OUT / "T44_step4a_log.json").write_text(json.dumps(log, indent=1) + "\n")
    print(json.dumps({k: v for k, v in log.items() if k != "problem_kinds"}, indent=1)[:3500])
    print(json.dumps(log["problem_kinds"], indent=1))


def stage_glex():
    st = json.loads(STATE.read_text()); k = json.loads(KEYF.read_text())
    texts = {i: st["texts"][i] for i in st["survivors"]}
    reg, fid = registry(texts, st["plans"], program=False, meanings=GLEX_MEANINGS)
    inv = {v: u for u, v in fid.items()}
    per, probs = {}, []
    for tid, m in k["reads"].items():
        f = Path(m["answer_file"])
        try:
            arr = json.loads(f.read_text())
        except Exception:
            probs.append(f"{tid}: no/bad answer"); continue
        got = {a["qid"]: a.get("choice") for a in arr if isinstance(a, dict) and "qid" in a}
        if set(got) != set(m["key"]):
            probs.append(f"{tid}: qids differ")
        for qid, f2 in m["key"].items():
            sem = reg.meaning_to_sem("question", got.get(qid)) if got.get(qid) else None
            per.setdefault(f2, {})[m["read"]] = sem == reg.forms[f2].sem_id
    adm = [f for f, d in per.items() if len(d) == 2 and all(d.values())]
    rej = sorted(f for f, d in per.items() if not (len(d) == 2 and all(d.values())))
    adm_ids = sorted(inv[f] for f in adm if not inv[f].startswith("program."))
    res = {"forms": len(reg.forms), "read_by_both": sum(1 for d in per.values() if len(d) == 2), "admitted_2of2": len(adm),
           "authored_admitted": {h: sum(1 for i in adm_ids if st["plans"][i]["head"] == h) for h in H.HEADS},
           "rejected": len(rej), "problems": probs,
           "rejected_item_ids": sorted(inv[f] for f in rej), "admitted_item_ids": adm_ids}
    (OUT / "T44_glex_result.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({a: b for a, b in res.items() if not a.endswith("ids")}))


def stage_seed():
    st = json.loads(STATE.read_text())
    res = json.loads((OUT / "T44_glex_result.json").read_text())
    ids = res["admitted_item_ids"]
    LEAN = G.LEAN
    units = [{"key": f"pool:a57_t44/{i}#0", "rows": [], "source": "pool:T44", "seed": True, "public": False, "line": 0,
              "template": True, "template_id": i, "file": f"a57_t44/{i}", "texts": [("pool", st["texts"][i])]} for i in ids]
    sets = {"c2_seed_T44": {"units": units, "code": [], "train_shas": {}, "seed_shas": {}, "train_path": None, "block": "T44",
                            "guard_shas": {}}}
    G.build_sets = lambda run_name, blocks, ilog: sets
    t0 = time.time()
    rec = G.run("seed", ["T44"], write=False)["c2_seed_T44"]
    q = rec.get("quarantine") or []
    dropped = sorted({(x if isinstance(x, str) else x.get("key", str(x))).split("/")[-1].rsplit("#", 1)[0] for x in q})
    rows = [{"id": i, "call_id": i, "state": st["texts"][i]} for i in ids]
    ac_rows = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "g13_ohsac_check.py", "--rows", rows)
    trecs = [{"id": i, "text": G.SLOT_RE.sub("{X}", st["texts"][i])} for i in ids]
    ac_tpl = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py", "--templates", trecs, extra=["--min-shared", "1", "--parts", "all"])
    out = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "wall_s": round(time.time() - t0), "items_checked": len(ids),
           "engine_complete": rec.get("complete"), "engine_dropped_items": dropped,
           "engine_counts": rec.get("counts_by_target_and_method"), "report_only": rec.get("report_only"),
           "ohsac_rows": {k: ac_rows.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids", "hit_ids_by_method")},
           "ohsac_templates": {k: ac_tpl.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids")}}
    out["ac_dropped_items"] = sorted(set(ac_rows.get("hit_ids") or []) | set(ac_tpl.get("hit_ids") or []))
    (OUT / "T44_g13seed_stage1.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("engine_dropped_items", "ac_dropped_items")}, default=str)[:3000])
    print("dropped engine", len(dropped), "dropped ac", len(out["ac_dropped_items"]))


if __name__ == "__main__":
    {"a": stage_a, "glex": stage_glex, "seed": stage_seed}[sys.argv[1]]()
