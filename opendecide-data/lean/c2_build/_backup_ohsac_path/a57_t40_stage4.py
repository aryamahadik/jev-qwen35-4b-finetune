"""A57 step 4 for T40 (quarantine answers only; drops only, nothing admitted). Counts and ids only. Mac, from c2_build:
  ../../.venv/bin/python -B zed_orch/a57_t40_stage4.py a      # format, dedupe, haiku/author.admit_* (G-SL, negation, cue), banned-word lint for
                                                               #   skins, lexicon unit test, AC + OHS-4 hash compare; writes G-LEX read tasks
  ../../.venv/bin/python -B zed_orch/a57_t40_stage4.py glex   # score the 2 blind reads (2/2 required)
  ../../.venv/bin/python -B zed_orch/a57_t40_stage4.py seed   # G13-seed stage 1 (engine + AC checkers) on survivors
Pool floors (no floor is written for T40 in PREREG; T41 precedent): skins >= 12 distinct admitted per register, wordings >= 6 per form.
"""
import hashlib, json, re, sys, time
from collections import Counter
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
from c2_kit import chunker as CH
from c2_kit.lexicon import LexiconRegistry, question_sem
from families.T40 import fixtures as FX
from families.T40.haiku import author as H
import negcount
import a57_hashcheck_ac as HC
import g13_c2 as G

Q = C2 / "a57_pool_quarantine" / "T40"
W = Q / "_work"; W.mkdir(exist_ok=True)
GL = Q / "glex"
STATE, KEYF = W / "step4a_state.json", W / "glex_key.json"
OUT = C2 / "logs" / "a57"
READS = ("read1", "read2")
FLOOR_SKIN, FLOOR_WORD = 12, 6
GPROMPT = ("You name the meaning of short English question lines. Each item gives one question line and a closed list of "
           "meanings. Pick the ONE meaning that the line expresses exactly, reading its words. If no meaning fits exactly, "
           "answer null. Do not answer the question.")
KEPT_FORMS = tuple(H.WORDINGS)
TOPUP_DIR = C2 / "families" / "T40" / "haiku" / "tasks_topup"

# banned classes of the skin task prompt (H.BANS), as word lists; applied outside {USER}
_B = {   # only the words and classes NAMED in H.BANS (no extra words)
    "digit": r"\d",
    "number_word": r"zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|hundred|thousand",
    "date_time": r"january|february|march|april|may|june|july|august|september|october|november|december|monday|tuesday|wednesday|thursday|friday|saturday|sunday",
    "url_email": r"https?|www|@|\.com|\.org|\.net",
    "time_word": r"today|now|soon|last|next|earlier|later",
    "quantity": r"all|every|each|some|any|no|none|only|always|never|several|many|more",
    "modal": r"must|may|can|should|will|would|need|allowed|required",
    "hedge": r"maybe|probably|likely|seems",
    "status": r"done|finished|approved|open|closed|valid|failed|pending|blocked",
    "condition": r"if|unless|except|otherwise",
    "negation": r"not|no|never|none|cannot|without",
}
_BRX = {k: re.compile(r"(?<![A-Za-z])(?:" + v + r")(?![A-Za-z])" if k not in ("digit", "url_email") else v, re.I) for k, v in _B.items()}


def skin_ban_hits(text: str) -> list:
    t = text.replace("{USER}", " ")
    hits = [k for k, rx in _BRX.items() if rx.search(t)]
    if "n't" in t.lower():
        hits.append("negation")
    c = negcount.count(t)
    if c.k_all and "negation" not in hits:
        hits.append("negation")
    return sorted(set(hits))


def registry(texts_by_iid, plans, program=True, kept=KEPT_FORMS):
    reg = LexiconRegistry("T40")
    for qf in kept:
        reg.declare(question_sem("T40", qf), "question", FX.MEANINGS[qf])
    fid = {}
    if program:
        for qf in kept:
            for i, w in enumerate(FX.WORDINGS.get(qf, ())):
                fid[f"program.{qf}.{i}"] = reg.add(w, question_sem("T40", qf), family="T40").form_id
    for iid in sorted(texts_by_iid):
        fid[iid] = reg.add(texts_by_iid[iid], question_sem("T40", plans[iid]["key"]), family="T40").form_id
    return reg, fid


def load_items():
    log, items, probs = {}, {}, []
    man = json.loads((H.TASKS / "manifest.json").read_text())
    for tm in sorted(TOPUP_DIR.glob("topup*/manifest.json")):
        man += json.loads(tm.read_text())
    for t in man:
        f = Q / (t["task_id"] + ".json")
        try:
            arr = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            probs.append(f"{t['task_id']}: missing/not JSON"); continue
        got = {}
        for a in arr if isinstance(arr, list) else []:
            if (isinstance(a, dict) and isinstance(a.get("qid"), str) and isinstance(a.get("texts"), list)
                    and all(isinstance(x, str) for x in a["texts"]) and set(a) <= {"qid", "texts"}):
                got.setdefault(a["qid"], a["texts"])
        if set(got) != set(t["items"]) or len(arr) != len(t["items"]):
            probs.append(f"{t['task_id']}: qids differ ({len(got)} vs {len(t['items'])}; {len(arr)} entries)")
        for q in t["items"]:
            p = q.split("-")
            kind, key = p[2], p[3]
            for k, tx in enumerate(got.get(q, [])):
                items[f"{q}#{k}"] = {"text": tx.strip(), "kind": kind, "key": key, "task": t["task_id"], "qid": q}
    log.update(expected_slots=sum(len(t["items"]) for t in man) * H.PER_ITEM, loaded_texts=len(items), format_problems=probs)
    return log, items


def stage_a():
    log = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
    l2, items = load_items(); log.update(l2)
    drops, order = {}, sorted(items)
    prog = {k: {w.lower() for w in v} for k, v in FX.WORDINGS.items()}
    seen = {}
    for iid in order:                                       # 1. family admission checker + dedupe within a pool (first kept)
        it = items[iid]
        key = (it["kind"], it["key"])
        nt = re.sub(r"\s+", " ", it["text"].lower())
        if it["kind"] == "skin":
            if it["key"] in H.HELD_OUT_REGISTERS:
                drops[iid] = "held_out_role"; continue
            pr = H.admit_skin(it["text"], it["key"])
            ban = skin_ban_hits(it["text"]) if not pr else []
        else:
            pr = H.admit_wording(it["key"], it["text"]); ban = []
            if nt in prog.get(it["key"], ()):
                pr = pr + ["duplicate of a program wording"]
        if pr:
            drops[iid] = "admit_" + it["kind"]; it["problem"] = re.sub(r"'[^']*'", "'..'", pr[0])[:60]
        elif ban:
            drops[iid] = "skin_banned_word:" + ",".join(ban)
        elif (key, nt) in seen:
            drops[iid] = "duplicate"
        else:
            seen[(key, nt)] = iid
    # 2. lexicon registry unit test (wordings)
    wtexts = {i: items[i]["text"] for i in order if i not in drops and items[i]["kind"] == "wording"}
    plans = {i: {"key": items[i]["key"]} for i in wtexts}
    try:
        reg, fid = registry(wtexts, plans)
    except Exception as e:
        log["registry_error"] = str(e)[:200]; raise
    ut = reg.unit_test_all()
    for iid, f in fid.items():
        if not ut[f]:
            if iid.startswith("program."):
                log.setdefault("program_form_unit_fail", []).append(iid)
            else:
                drops[iid] = "lexicon_unit_test"
    # 3. hash compare vs the OHS-AC final export (HC) and vs OHS-4 (G.Exports); skins are TEMPLATE units
    ex = HC.ExportsAC(); st = HC.selftest(ex); assert all(st.values()), st
    units = [{"key": i, "texts": [("text", items[i]["text"])], "template": items[i]["kind"] == "skin"} for i in order if i not in drops]
    r = HC.run(units, ex)
    for k in r["hit_ids"]:
        drops[k] = "ac_hash"
    log["ac_hash"] = {"manifest_sha256": r["manifest_sha256"], "stage": r["export_stage"], "final": r["export_final"],
                      "final_suite_sha256": r["final_suite_sha256"], "manifest_verified": r["manifest_verified"],
                      "complete": r["complete"], "checked": len(units), "hit_items": len(r["hit_ids"]), "by_method": r["counts"]["by_method"]}
    ex4 = G.Exports()
    units4 = [{"key": i, "texts": [("text", items[i]["text"])], "template": items[i]["kind"] == "skin"} for i in order if i not in drops]
    hits4, rep4 = G.ohs4_hash_hits(units4, ex4)
    ids4 = sorted({k for m in hits4.values() for k in m})
    for k in ids4:
        drops[k] = "ohs4_hash"
    log["ohs4_hash"] = {"checked": len(units4), "hit_items": len(ids4), "by_method": {m: len(v) for m, v in hits4.items()}}
    surv = sorted(i for i in items if i not in drops)
    pools = {}
    for kind in ("skin", "wording"):
        keys = sorted({items[i]["key"] for i in items if items[i]["kind"] == kind}, key=lambda k: list(H.REGISTERS if kind == "skin" else H.WORDINGS).index(k))
        for k in keys:
            ids = [i for i in items if items[i]["kind"] == kind and items[i]["key"] == k]
            pools[f"{kind}:{k}"] = {"authored": len(ids), "survive": sum(1 for i in ids if i in surv),
                                     "dropped": dict(Counter(drops[i].split(":")[0] for i in ids if i in drops))}
    log["pools_after_4a"] = pools
    log["under_floor_after_4a"] = [k for k, v in pools.items() if v["survive"] < (FLOOR_SKIN if k.startswith("skin") else FLOOR_WORD)]
    log["problem_kinds"] = dict(Counter(f"{items[i]['kind']}:{items[i]['key']}: {it['problem']}" for i, it in items.items() if it.get("problem")))
    log["survivors_after_4a"] = len(surv)
    STATE.write_text(json.dumps({"drops": drops, "survivors": surv, "items": items}, indent=1, sort_keys=True))
    # 4. G-LEX blind-read task files for the wording survivors (two reads, different seeds; each file to a FRESH Haiku)
    wsurv = {i: items[i]["text"] for i in surv if items[i]["kind"] == "wording"}
    reg, fid = registry(wsurv, {i: {"key": items[i]["key"]} for i in wsurv}, program=False)
    reg.unit_test_all()
    man = {"reads": {}}
    for rd in READS:
        its = reg.lexicon_items(seed=f"a57-t40-{rd}")
        b = CH.make_batch("extract_lex", "T40", its, seed=f"a57-t40-{rd}", prompt=GPROMPT)
        for ch in b.chunks:
            tid = f"T40-glex-{rd}-{ch['task_id'].rsplit('-', 1)[1]}"
            n = len(ch["items"]); ans = GL / "answers" / f"{tid}.json"
            head = (f"# T40 G-LEX extraction task {tid}\n\nANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
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
    (OUT / "T40_step4a_log.json").write_text(json.dumps(log, indent=1) + "\n")
    print(json.dumps({k: v for k, v in log.items() if k != "problem_kinds"}, indent=1)[:6000])
    print(json.dumps(log["problem_kinds"], indent=1))


def topup_write(n: int, plan: dict):
    """A57 rule f: fresh-Haiku top-up task files with the UNCHANGED T40 task prompt (H.PROMPTS / H.ANSWER / item brief format).
    plan = {task_idx: [(kind, key, first_j, n_items), ...]}; items numbered after the round-1 items (j >= 3 for wordings, >= 6 for skins)."""
    d = TOPUP_DIR / f"topup{n}"; d.mkdir(parents=True, exist_ok=True)
    man = []
    for ti, its in sorted(plan.items()):
        tid = f"T40-H-{its[0][0]}-topup{n}-chunk{ti:02d}" if len({k for k, *_ in its}) == 1 else f"T40-H-mixed-topup{n}-chunk{ti:02d}"
        body = [f"# Task {tid}", "", H.PROMPTS[its[0][0]], "", H.ANSWER, "", "Answer file: " + str(Q / (tid + ".json")), "", "## Items"]
        qids = []
        for kind, key, j0, cnt in its:
            for j in range(j0, j0 + cnt):
                if kind == "skin":
                    qid = f"T40-H-skin-{key}-{j}"
                    brief = (f"Write {H.PER_ITEM} different one-line headers for a {key} (register: {key}) in which {{USER}} is talking to "
                             f"an assistant agent. Use {{USER}} exactly once in every line.")
                else:
                    qid = f"T40-H-wording-{key}-{j}"
                    brief = f"Write {H.PER_ITEM} different questions. Meaning: it {H.WORDINGS[key][0]}. Negation words (not) required: {H.WORDINGS[key][1][1]}."
                body.append(f"- qid `{qid}`: {brief}"); qids.append(qid)
        (d / (tid + ".md")).write_text("\n".join(body) + "\n", encoding="utf-8")
        man.append({"task_id": tid, "kind": its[0][0], "items": qids})
    (d / "manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
    ex = HC.ExportsAC()
    r = HC.run(HC.units_from_taskfiles(d, "*.md"), ex)
    g4 = G.ohs4_hash_hits(HC.units_from_taskfiles(d, "*.md"), G.Exports())[0]
    sha = {t["task_id"]: hashlib.sha256((d / (t["task_id"] + ".md")).read_bytes()).hexdigest() for t in man}
    out = {"topup": n, "dir": str(d), "n_files": len(man), "ac_hit_units": len(r["hit_ids"]), "ac_by_method": r["counts"]["by_method"],
           "ohs4_hit_units": len({k for m in g4.values() for k in m}), "task_sha256": sha,
           "manifest_sha256": hashlib.sha256((d / "manifest.json").read_bytes()).hexdigest(), "ac_manifest_sha256": r["manifest_sha256"]}
    (OUT / f"T40_topup{n}_tasks.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


def stage_glex():
    st = json.loads(STATE.read_text()); k = json.loads(KEYF.read_text())
    items = st["items"]
    wsurv = {i: items[i]["text"] for i in st["survivors"] if items[i]["kind"] == "wording"}
    reg, fid = registry(wsurv, {i: {"key": items[i]["key"]} for i in wsurv}, program=False)
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
    adm_ids = sorted(inv[f] for f in adm)
    forms = list(H.WORDINGS)
    res = {"forms": len(reg.forms), "read_by_both": sum(1 for d in per.values() if len(d) == 2), "admitted_2of2": len(adm),
           "authored_admitted": {q: sum(1 for i in adm_ids if items[i]["key"] == q) for q in forms},
           "rejected": len(rej), "problems": probs,
           "rejected_item_ids": sorted(inv[f] for f in rej), "admitted_item_ids": adm_ids}
    skins = [i for i in st["survivors"] if items[i]["kind"] == "skin"]
    res["skin_survivors"] = {r: sum(1 for i in skins if items[i]["key"] == r) for r in H.REGISTERS if r not in H.HELD_OUT_REGISTERS}
    res["under_floor"] = [f"wording:{q}" for q, n in res["authored_admitted"].items() if n < FLOOR_WORD] + \
                         [f"skin:{r}" for r, n in res["skin_survivors"].items() if n < FLOOR_SKIN]
    (OUT / "T40_glex_result.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({a: b for a, b in res.items() if not a.endswith("ids")}))


def stage_seed():
    st = json.loads(STATE.read_text()); items = st["items"]
    res = json.loads((OUT / "T40_glex_result.json").read_text())
    ids = sorted(set(res["admitted_item_ids"]) | {i for i in st["survivors"] if items[i]["kind"] == "skin"})
    LEAN = G.LEAN
    units = [{"key": f"pool:a57_t40/{i}#0", "rows": [], "source": "pool:T40", "seed": True, "public": False, "line": 0,
              "template": True, "template_id": i, "file": f"a57_t40/{i}", "texts": [("pool", items[i]["text"])]} for i in ids]
    sets = {"c2_seed_T40": {"units": units, "code": [], "train_shas": {}, "seed_shas": {}, "train_path": None, "block": "T40",
                            "guard_shas": {}}}
    G.build_sets = lambda run_name, blocks, ilog: sets
    t0 = time.time()
    rec = G.run("seed", ["T40"], write=False)["c2_seed_T40"]
    q = rec.get("quarantine") or []
    dropped = sorted({(x if isinstance(x, str) else x.get("key", str(x))).split("/")[-1].rsplit("#", 1)[0] for x in q})
    rows = [{"id": i, "call_id": i, "state": items[i]["text"]} for i in ids]
    ac_rows = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "g13_ohsac_check.py", "--rows", rows)
    trecs = [{"id": i, "text": G.SLOT_RE.sub("{X}", items[i]["text"])} for i in ids]
    ac_tpl = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py", "--templates", trecs, extra=["--min-shared", "1", "--parts", "all"])
    out = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "wall_s": round(time.time() - t0), "items_checked": len(ids),
           "engine_complete": rec.get("complete"), "engine_dropped_items": dropped,
           "engine_counts": rec.get("counts_by_target_and_method"), "report_only": rec.get("report_only"),
           "ohsac_rows": {k: ac_rows.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids", "hit_ids_by_method")},
           "ohsac_templates": {k: ac_tpl.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids")}}
    out["ac_dropped_items"] = sorted(set(ac_rows.get("hit_ids") or []) | set(ac_tpl.get("hit_ids") or []))
    (OUT / "T40_g13seed_stage1.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("engine_dropped_items", "ac_dropped_items")}, default=str)[:3000])
    print("dropped engine", len(dropped), "dropped ac", len(out["ac_dropped_items"]))


if __name__ == "__main__":
    if sys.argv[1] == "topup1":
        topup_write(1, {0: [("skin", "chat", 6, 2), ("skin", "ticket", 6, 2)], 1: [("skin", "chat", 8, 2), ("skin", "ticket", 8, 2)],
                        2: [("wording", "cc_edit", 3, 2)], 3: [("wording", "cc_edit", 5, 2)], 4: [("wording", "cc_edit", 7, 2)]})
    else:
        {"a": stage_a, "glex": stage_glex, "seed": stage_seed}[sys.argv[1]]()
