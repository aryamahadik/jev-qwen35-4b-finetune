"""A57 step 4 for T40, top-up round(s) (A57 rule f). Leaves round-2 state (step4a_state.json, glex answers) untouched. Counts/ids only.
  a57_t40_stage4b.py a <n>     # admit top-up n answers (same checks as stage4 a; dedupe vs round-2 survivors); writes G-LEX tasks for new wording survivors
  a57_t40_stage4b.py glex <n>  # score the two reads of top-up n
  a57_t40_stage4b.py merge     # merged state + merged glex result (round-2 result kept as T40_glex_result_r2.json) for the seed step
"""
import hashlib, json, re, sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import a57_t40_stage4 as S
from a57_t40_stage4 import H, HC, G, CH, FX, Q, OUT, GL, READS, GPROMPT, FLOOR_SKIN, FLOOR_WORD, registry

W = S.W

def tstate(n): return W / f"step4_topup{n}_state.json"
def tkey(n): return W / f"glex_topup{n}_key.json"

def topup_items(n):
    d = S.TOPUP_DIR / f"topup{n}"
    man = json.loads((d / "manifest.json").read_text())
    log, items, probs = {}, {}, []
    for t in man:
        f = Q / (t["task_id"] + ".json")
        try: arr = json.loads(f.read_text(encoding="utf-8"))
        except Exception: probs.append(f"{t['task_id']}: missing/not JSON"); continue
        got = {}
        for a in arr if isinstance(arr, list) else []:
            if (isinstance(a, dict) and isinstance(a.get("qid"), str) and isinstance(a.get("texts"), list)
                    and all(isinstance(x, str) for x in a["texts"]) and set(a) <= {"qid", "texts"}):
                got.setdefault(a["qid"], a["texts"])
        if set(got) != set(t["items"]) or len(arr) != len(t["items"]):
            probs.append(f"{t['task_id']}: qids differ ({len(got)} vs {len(t['items'])}; {len(arr)} entries)")
        for q in t["items"]:
            p = q.split("-"); kind, key = p[2], p[3]
            for k, tx in enumerate(got.get(q, [])):
                items[f"{q}#{k}"] = {"text": tx.strip(), "kind": kind, "key": key, "task": t["task_id"], "qid": q}
    log.update(expected_slots=sum(len(t["items"]) for t in man) * H.PER_ITEM, loaded_texts=len(items), format_problems=probs)
    return log, items

def stage_a(n):
    base = json.loads(S.STATE.read_text())
    log = {"topup": n, "time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
    l2, items = topup_items(n); log.update(l2)
    assert not (set(items) & set(base["items"])), "id clash with round 2"
    glex_r2 = json.loads((OUT / "T40_glex_result_r2.json").read_text()) if (OUT / "T40_glex_result_r2.json").exists() else json.loads((OUT / "T40_glex_result.json").read_text())
    old_adm = set(glex_r2["admitted_item_ids"])
    old_skin = {i for i in base["survivors"] if base["items"][i]["kind"] == "skin"}
    drops, order = {}, sorted(items)
    prog = {k: {w.lower() for w in v} for k, v in FX.WORDINGS.items()}
    seen = {}
    for i in old_adm | old_skin:
        it = base["items"][i]; seen[(it["key"], re.sub(r"\s+", " ", it["text"].lower()))] = i
    for iid in order:
        it = items[iid]; key = it["key"]; nt = re.sub(r"\s+", " ", it["text"].lower())
        if it["kind"] == "skin":
            if key in H.HELD_OUT_REGISTERS: drops[iid] = "held_out_role"; continue
            pr = H.admit_skin(it["text"], key); ban = S.skin_ban_hits(it["text"]) if not pr else []
        else:
            pr = H.admit_wording(key, it["text"]); ban = []
            if nt in prog.get(key, ()): pr = pr + ["duplicate of a program wording"]
        if pr:
            drops[iid] = "admit_" + it["kind"]; it["problem"] = re.sub(r"'[^']*'", "'..'", pr[0])[:60]
        elif ban: drops[iid] = "skin_banned_word:" + ",".join(ban)
        elif (key, nt) in seen: drops[iid] = "duplicate"
        else: seen[(key, nt)] = iid
    # lexicon: registry with round-2 admitted + new; new item whose form equals an existing form is a duplicate
    wnew = {i: items[i]["text"] for i in order if i not in drops and items[i]["kind"] == "wording"}
    allw = {i: base["items"][i]["text"] for i in old_adm}; allw.update(wnew)
    plans = {i: {"key": (base["items"][i] if i in base["items"] else items[i])["key"]} for i in allw}
    reg, fid = registry(allw, plans)
    ut = reg.unit_test_all()
    byform = {}
    for i in sorted(old_adm): byform.setdefault(fid[i], i)
    for i in sorted(wnew):
        f = fid[i]
        if not ut[f]: drops[i] = "lexicon_unit_test"
        elif f in byform: drops[i] = "duplicate"
        else: byform[f] = i
    ex = HC.ExportsAC(); st = HC.selftest(ex); assert all(st.values()), st
    units = [{"key": i, "texts": [("text", items[i]["text"])], "template": items[i]["kind"] == "skin"} for i in order if i not in drops]
    r = HC.run(units, ex)
    for k in r["hit_ids"]: drops[k] = "ac_hash"
    log["ac_hash"] = {"manifest_sha256": r["manifest_sha256"], "stage": r["export_stage"], "final_suite_sha256": r["final_suite_sha256"],
                      "manifest_verified": r["manifest_verified"], "complete": r["complete"], "checked": len(units),
                      "hit_items": len(r["hit_ids"]), "by_method": r["counts"]["by_method"]}
    ex4 = G.Exports()
    units4 = [{"key": i, "texts": [("text", items[i]["text"])], "template": items[i]["kind"] == "skin"} for i in order if i not in drops]
    hits4, _ = G.ohs4_hash_hits(units4, ex4)
    ids4 = sorted({k for m in hits4.values() for k in m})
    for k in ids4: drops[k] = "ohs4_hash"
    log["ohs4_hash"] = {"checked": len(units4), "hit_items": len(ids4)}
    surv = sorted(i for i in items if i not in drops)
    pools = {}
    for kind in ("skin", "wording"):
        for k in sorted({items[i]["key"] for i in items if items[i]["kind"] == kind}):
            ids = [i for i in items if items[i]["kind"] == kind and items[i]["key"] == k]
            pools[f"{kind}:{k}"] = {"authored": len(ids), "survive": sum(1 for i in ids if i in surv),
                                    "dropped": dict(Counter(drops[i].split(":")[0] for i in ids if i in drops))}
    log["pools_topup"] = pools; log["survivors_topup"] = len(surv)
    log["problem_kinds"] = dict(Counter(f"{items[i]['kind']}:{items[i]['key']}: {it['problem']}" for i, it in items.items() if it.get("problem")))
    tstate(n).write_text(json.dumps({"drops": drops, "survivors": surv, "items": items}, indent=1, sort_keys=True))
    # G-LEX tasks for the new wording survivors
    wsurv = {i: items[i]["text"] for i in surv if items[i]["kind"] == "wording"}
    man = {"reads": {}}
    if wsurv:
        reg2, fid2 = registry(wsurv, {i: {"key": items[i]["key"]} for i in wsurv}, program=False); reg2.unit_test_all()
        for rd in READS:
            its = reg2.lexicon_items(seed=f"a57-t40-topup{n}-{rd}")
            b = CH.make_batch("extract_lex", "T40", its, seed=f"a57-t40-topup{n}-{rd}", prompt=GPROMPT)
            for ch in b.chunks:
                tid = f"T40-glex-topup{n}-{rd}-{ch['task_id'].rsplit('-', 1)[1]}"
                m = len(ch["items"]); ans = GL / "answers" / f"{tid}.json"
                head = (f"# T40 G-LEX extraction task {tid}\n\nANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                        f"{ans}\n\nTask kind: extract_lex; items: {m}; answers expected: {m} (one per item, answer field \"choice\").\n\n"
                        "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n## Instructions\n\n"
                        "Each item gives one question and a list of meanings. Pick the ONE meaning in the list that the question expresses exactly, "
                        "reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether "
                        "anything is true.\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
                        "array with one entry per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the chosen meaning copied exactly, or null>\"}. "
                        "Valid JSON only; no text before or after the array. Run no other tool.\n\n"
                        "Answer format: [{\"qid\": \"<qid>\", \"choice\": \"<one meaning, copied exactly, or null>\"}, ...]\n\n"
                        "## Items (JSON; answer every item once, keyed by its qid)\n\n")
                tf = GL / "tasks" / f"{tid}.md"
                tf.write_text(head + json.dumps(ch["items"], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                man["reads"][tid] = {"read": rd, "task_file": str(tf), "answer_file": str(ans), "n": m,
                                     "sha256": hashlib.sha256(tf.read_bytes()).hexdigest(),
                                     "key": {q: b.key[q] for q in (it["qid"] for it in ch["items"])}}
        man["fid_of"] = fid2
        tg = [tf for tf in (GL / "tasks").glob(f"T40-glex-topup{n}-*.md")]
        ur = HC.run(HC.units_from_taskfiles(GL / "tasks", f"T40-glex-topup{n}-*.md"), ex)
        log["glex_task_files"] = {"n": len(man["reads"]), "hash_hit_units": len(ur["hit_ids"]),
                                  "sha256": {t: m["sha256"] for t, m in man["reads"].items()}}
    tkey(n).write_text(json.dumps(man, indent=1))
    (OUT / f"T40_step4_topup{n}_log.json").write_text(json.dumps(log, indent=1) + "\n")
    print(json.dumps({k: v for k, v in log.items() if k != "problem_kinds"}, indent=1)[:5000]); print(json.dumps(log["problem_kinds"], indent=1))

def stage_glex(n):
    st = json.loads(tstate(n).read_text()); k = json.loads(tkey(n).read_text()); items = st["items"]
    wsurv = {i: items[i]["text"] for i in st["survivors"] if items[i]["kind"] == "wording"}
    reg, fid = registry(wsurv, {i: {"key": items[i]["key"]} for i in wsurv}, program=False)
    inv = {v: u for u, v in fid.items()}
    per, probs = {}, []
    for tid, m in k["reads"].items():
        try: arr = json.loads(Path(m["answer_file"]).read_text())
        except Exception: probs.append(f"{tid}: no/bad answer"); continue
        got = {a["qid"]: a.get("choice") for a in arr if isinstance(a, dict) and "qid" in a}
        if set(got) != set(m["key"]): probs.append(f"{tid}: qids differ")
        for qid, f2 in m["key"].items():
            sem = reg.meaning_to_sem("question", got.get(qid)) if got.get(qid) else None
            per.setdefault(f2, {})[m["read"]] = sem == reg.forms[f2].sem_id
    adm = [f for f, d in per.items() if len(d) == 2 and all(d.values())]
    rej = sorted(f for f, d in per.items() if not (len(d) == 2 and all(d.values())))
    res = {"topup": n, "forms": len(reg.forms), "read_by_both": sum(1 for d in per.values() if len(d) == 2), "admitted_2of2": len(adm),
           "admitted_by_form": dict(Counter(items[inv[f]]["key"] for f in adm)), "rejected": len(rej), "problems": probs,
           "rejected_item_ids": sorted(inv[f] for f in rej), "admitted_item_ids": sorted(inv[f] for f in adm)}
    (OUT / f"T40_glex_topup{n}_result.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({a: b for a, b in res.items() if not a.endswith("ids")}))

def stage_merge(ns):
    r2p = OUT / "T40_glex_result_r2.json"
    if not r2p.exists(): r2p.write_text((OUT / "T40_glex_result.json").read_text())
    r2 = json.loads(r2p.read_text()); base = json.loads(S.STATE.read_text())
    items = dict(base["items"]); drops = dict(base["drops"]); surv = set(base["survivors"])
    adm = set(r2["admitted_item_ids"]); skins = {i for i in base["survivors"] if items[i]["kind"] == "skin"}
    for n in ns:
        t = json.loads(tstate(n).read_text()); g = json.loads((OUT / f"T40_glex_topup{n}_result.json").read_text())
        assert not g["problems"]
        items.update(t["items"]); drops.update(t["drops"])
        for i in g["rejected_item_ids"]: drops[i] = "glex_not_2of2"
        adm |= set(g["admitted_item_ids"]); skins |= {i for i in t["survivors"] if t["items"][i]["kind"] == "skin"}
    surv = sorted(adm | skins)
    merged = {"drops": drops, "survivors": surv, "items": items}
    (W / "step4_merged_state.json").write_text(json.dumps(merged, indent=1, sort_keys=True))
    res = {"admitted_item_ids": sorted(adm), "rounds": ["r2"] + [f"topup{n}" for n in ns]}
    res["wording_by_form"] = {q: sum(1 for i in adm if items[i]["key"] == q) for q in H.WORDINGS}
    res["skin_by_register"] = {r: sum(1 for i in skins if items[i]["key"] == r) for r in H.REGISTERS if r not in H.HELD_OUT_REGISTERS}
    res["under_floor"] = [f"wording:{q}" for q, v in res["wording_by_form"].items() if v < FLOOR_WORD] + \
                         [f"skin:{r}" for r, v in res["skin_by_register"].items() if v < FLOOR_SKIN]
    (OUT / "T40_glex_merged.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({a: b for a, b in res.items() if a != "admitted_item_ids"}))

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "a": stage_a(int(sys.argv[2]))
    elif c == "glex": stage_glex(int(sys.argv[2]))
    else: stage_merge([int(x) for x in sys.argv[2:]])
