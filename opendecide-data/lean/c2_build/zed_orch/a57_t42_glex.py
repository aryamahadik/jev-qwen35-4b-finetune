"""a57_t42_glex.py: A57 step 4 for T42: the G-LEX blind-read task files (2 reads, different readers/orders) and the scorer.
T42 has no Haiku-authored pool (texts.py is program text); the only Haiku step is the 2/2 meaning read of its 9 question
wordings. Items carry only the wording text; no gold, no row, no sealed text. Counts only.
  python -B zed_orch/a57_t42_glex.py write   |   python -B zed_orch/a57_t42_glex.py score
"""
import json, sys, hashlib
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
from c2_kit import chunker as CH
from families.T42 import plugin as P
ROOT = C2 / "a57_pool_quarantine" / "T42" / "glex"
KEY = C2 / "logs" / "a57_T42_glex_key.json"
READS = ("read1", "read2")
PROMPT = ("You name the meaning of short English question lines. Each item gives one question line and a closed list of "
          "meanings. Pick the ONE meaning that the line expresses exactly, reading its words. If no meaning fits exactly, "
          "answer null. Do not answer the question.")

def build():
    plugin, ctx = P.make_plugin()
    reg = ctx.lexicon
    out = {"reads": {}}
    for rd in READS:
        items = reg.lexicon_items(seed=f"a57-t42-{rd}")
        b = CH.make_batch("extract_lex", "T42", items, seed=f"a57-t42-{rd}", prompt=PROMPT)
        assert len(b.chunks) == 1
        ch = b.chunks[0]
        tid = f"T42-glex-{rd}"
        n = len(ch["items"])
        ans = ROOT / "answers" / f"{tid}.json"
        head = (f"# T42 G-LEX extraction task {tid}\n\nANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{ans}\n\nTask kind: extract_lex; items: {n}; answers expected: {n} (one per item, answer field \"choice\").\n\n"
                "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n## Instructions\n\n"
                "Each item gives one question and a list of meanings. Pick the ONE meaning in the list that the question expresses exactly, "
                "reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether "
                "anything is true.\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
                "array with one object per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the chosen meaning copied exactly, or null>\"}. "
                "Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.\n\n"
                "Answer format: [{\"qid\": \"<qid>\", \"choice\": \"<one meaning, copied exactly, or null>\"}, ...]\n\n"
                "## Items (JSON; answer every item once, keyed by its qid)\n\n")
        body = json.dumps(ch["items"], ensure_ascii=False, indent=1) + "\n"
        tf = ROOT / "tasks" / f"{tid}.md"
        tf.write_text(head + body, encoding="utf-8")
        out["reads"][rd] = {"task_id": tid, "task_file": str(tf), "answer_file": str(ans), "n": n,
                            "sha256": hashlib.sha256(tf.read_bytes()).hexdigest(), "key": b.key}
    KEY.write_text(json.dumps(out, indent=1))
    return out

def score():
    plugin, ctx = P.make_plugin()
    reg = ctx.lexicon
    k = json.loads(KEY.read_text())
    per_form = {}
    probs = []
    for rd, meta in k["reads"].items():
        f = Path(meta["answer_file"])
        if not f.exists():
            probs.append(f"{rd}: no answer file"); continue
        try:
            arr = json.loads(f.read_text())
        except Exception as e:
            probs.append(f"{rd}: bad json"); continue
        got = {a["qid"]: a.get("choice") for a in arr if isinstance(a, dict) and "qid" in a}
        if set(got) != set(meta["key"]):
            probs.append(f"{rd}: qids differ ({len(got)} vs {len(meta['key'])})")
        for qid, fid in meta["key"].items():
            sem = reg.meaning_to_sem("question", got.get(qid)) if got.get(qid) else None
            per_form.setdefault(fid, {})[rd] = sem == reg.forms[fid].sem_id
    adm = [f for f, d in per_form.items() if len(d) == 2 and all(d.values())]
    rej = [f for f, d in per_form.items() if any(v is False for v in d.values())]
    res = {"forms": len(reg.forms), "read": len(per_form), "admitted_2of2": len(adm), "rejected": len(rej), "problems": probs,
           "rejected_forms": sorted(rej)}
    (C2 / "logs" / "a57_T42_glex_result.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "rejected_forms"}))

if __name__ == "__main__":
    if sys.argv[1] == "write":
        o = build()
        print({r: (m["task_file"], m["n"], m["sha256"][:12]) for r, m in o["reads"].items()})
    else:
        score()
