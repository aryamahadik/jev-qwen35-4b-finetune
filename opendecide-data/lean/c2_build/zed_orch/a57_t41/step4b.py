"""A57 step 4b for T41: G-LEX blind-read task files (2 reads, different seeds -> different chunks / choice order; each task
file goes to one FRESH Haiku) for the step-4a survivors; and the scorer. Task files + answers live in a57_pool_quarantine/T41/glex.
  ../../.venv/bin/python -B zed_orch/a57_t41/step4b.py write | score"""
import hashlib, json, sys, re
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
import ac_hash as A
from c2_kit import chunker as CH
from c2_kit.lexicon import LexiconRegistry, question_sem
from families.T41 import pools as P, fixtures as FX
Q = C2 / "a57_pool_quarantine" / "T41"
ROOT = Q / "glex"
STATE = Q / "_work" / "step4a_state.json"
KEYF = Q / "_work" / "glex_key.json"
READS = ("read1", "read2")
PROMPT = ("You name the meaning of short English lines. Each item gives one line and a closed list of meanings. Pick the ONE "
          "meaning that the line expresses exactly, reading its words. If no meaning fits exactly, answer null. Do not answer "
          "the line, and do not judge whether anything is true.")


def registry(extra_state=None):
    st = json.loads(STATE.read_text())
    plans = {}
    for p in (C2 / "families/T41/haiku/author/plan").glob("*.json"):
        plans.update(json.loads(p.read_text())["plan"])
    reg = LexiconRegistry("T41")
    for sem, meaning in P.DELEG_MEANING.items():
        reg.declare(sem, "deontic" if sem == "deleg.direct" else "confirmation", meaning)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem("T41", qf), "question", meaning.replace("NOT the case that", "NOT true that"))
    fid_of = {}
    for iid in st["survivors"]:
        pl = plans.get(iid) or {}
        t = st["texts"][iid]
        if pl.get("role") == "wording":
            fid_of[iid] = reg.add(t, question_sem("T41", pl["qform"]), family="T41").form_id
        elif pl.get("role") == "lexicon":
            fid_of[iid] = reg.add(t.replace("{ARG}", "{ARG:s0}").replace("{SRC}", "{SRC:s0}"), pl["sem"],
                                  slots={"ARG": "category", "SRC": "category"}, family="T41").form_id
    reg.unit_test_all()
    return reg, fid_of


def write():
    reg, fid_of = registry()
    out = {"reads": {}}
    inv = {v: k for k, v in fid_of.items()}
    for rd in READS:
        items = reg.lexicon_items(seed=f"a57-t41-{rd}")
        b = CH.make_batch("extract_lex", "T41", items, seed=f"a57-t41-{rd}", prompt=PROMPT)
        for ch in b.chunks:
            tid = f"T41-glex-{rd}-{ch['task_id'].rsplit('-', 1)[1]}"
            n = len(ch["items"])
            ans = ROOT / "answers" / f"{tid}.json"
            head = (f"# T41 G-LEX extraction task {tid}\n\nANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                    f"{ans}\n\nTask kind: extract_lex; items: {n}; answers expected: {n} (one per item).\n\n"
                    "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n## Instructions\n\n"
                    "Each item gives one line and a list of meanings. Pick the ONE meaning in the list that the line expresses exactly, "
                    "reading its words. If no meaning in the list fits exactly, answer null. Do not answer the line, and do not judge "
                    "whether anything is true.\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, "
                    "as one JSON array with one entry per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the chosen meaning copied "
                    "exactly, or null>\"}. Valid JSON only; no text before or after the array. Run no other tool.\n\n"
                    "Answer format: [{\"qid\": \"<qid>\", \"choice\": \"<one meaning, copied exactly, or null>\"}, ...]\n\n"
                    "## Items (JSON; answer every item once, keyed by its qid)\n\n")
            body = json.dumps(ch["items"], ensure_ascii=False, indent=1) + "\n"
            tf = ROOT / "tasks" / f"{tid}.md"
            tf.parent.mkdir(parents=True, exist_ok=True); ans.parent.mkdir(parents=True, exist_ok=True)
            tf.write_text(head + body, encoding="utf-8")
            out["reads"][tid] = {"read": rd, "task_file": str(tf), "answer_file": str(ans), "n": n,
                                 "sha256": hashlib.sha256(tf.read_bytes()).hexdigest(),
                                 "key": {q: b.key[q] for q in (it["qid"] for it in ch["items"])}}
    KEYF.write_text(json.dumps(out, indent=1))
    # hash compare of the glex task files (whole file + every string leaf) vs the AC export
    ex = A.ACExports()
    texts = {}
    for tid, m in out["reads"].items():
        raw = Path(m["task_file"]).read_text(encoding="utf-8")
        parts = [raw]
        for it in json.loads(raw[raw.index("[\n"):] if False else raw[raw.index("## Items"):].split("\n", 2)[2]):
            parts += [it["text"]] + list(it["choices"])
        texts[tid] = parts
    hits, _ = A.check_texts(ex, texts)
    res = {"task_files": len(out["reads"]), "items_per_read": len(fid_of), "hit_files": len({k for m in hits.values() for k in m}),
           "by_method": {m: len(v) for m, v in hits.items()},
           "files": {t: {"n": m["n"], "sha256": m["sha256"], "task_file": m["task_file"], "answer_file": m["answer_file"]}
                     for t, m in out["reads"].items()}}
    (Path(__file__).parent / "glex_tasks_manifest.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "files"}))


def score():
    reg, fid_of = registry()
    k = json.loads(KEYF.read_text())
    per, probs = {}, []
    for tid, m in k["reads"].items():
        f = Path(m["answer_file"])
        if not f.exists():
            probs.append(f"{tid}: no answer file"); continue
        try:
            arr = json.loads(f.read_text())
        except Exception:
            probs.append(f"{tid}: bad json"); continue
        got = {a["qid"]: a.get("choice") for a in arr if isinstance(a, dict) and "qid" in a}
        if set(got) != set(m["key"]):
            probs.append(f"{tid}: qids differ")
        for qid, fid in m["key"].items():
            kind = reg.forms[fid].kind
            sem = reg.meaning_to_sem(kind, got.get(qid)) if got.get(qid) else None
            per.setdefault(fid, {})[m["read"]] = sem == reg.forms[fid].sem_id
    adm = [f for f, d in per.items() if len(d) == 2 and all(d.values())]
    rej = sorted(f for f, d in per.items() if len(d) < 2 or not all(d.values()))
    inv = {v: k for k, v in fid_of.items()}
    res = {"forms": len(reg.forms), "read_by_both": sum(1 for d in per.values() if len(d) == 2), "admitted_2of2": len(adm),
           "rejected": len(rej), "problems": probs, "rejected_item_ids": [inv[f] for f in rej], "admitted_item_ids": [inv[f] for f in adm]}
    (Path(__file__).parent / "glex_result.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k2: v for k2, v in res.items() if not k2.endswith("ids")}))

if __name__ == "__main__":
    {"write": write, "score": score}[sys.argv[1]]()
