"""families/T27/ovl_author.py: authoring, admission and merge of the request forms the overlap level needs (fix iteration 2).

The frozen lexicon prints an in-scope request with 0.5-1.0 of its words already in the user's text and a beyond request
with 0 (pilot_i2/FIX_I2_NOTES.md), so the level of overlap.py cannot be drawn from the seed until in-scope requests also
exist as paraphrases with words the user did not use. These are new FORMS of the existing `req.<action>.<gate|plain>`
sems (no new sem, no label involved): Haiku writes them, two independent G-LEX reads must each name the form's own sem,
and the generator measures their overlap itself (overlap.py), so nothing else needs to know which form is which.

  ovl_author.py tasks     writes haiku/ovl_i2/tasks/*.txt (authoring; the answer paths are named in each file)
  ovl_author.py stage2    admits haiku/ovl_i2/answers/*.json (wording and band checks) and writes the G-LEX task files
                          haiku/ovl_i2/glex_tasks/*.txt (two independent reads: read1 / read2 of every chunk)
  ovl_author.py stage3    admits the forms both reads map to their own sem into haiku/ovl_i2/admitted/lexicon_supplement.json
                          (read by run_pilot_i2.py), writes pilot_i2/G13_PENDING.txt and, with --run, runs the pilot and G6

Run from lean/c2_build:  ../../.venv/bin/python -B families/T27/ovl_author.py <step> [--root DIR]
(--root: a different haiku/ovl_i2 folder, used by the tests on fabricated answers.)  No model is run here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
for p in (str(C2_BUILD), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

ROOT = HERE / "haiku" / "ovl_i2"
BANDS = ("none", "partial")
N_FORMS = {"gate": 3, "plain": 2}
CHUNK = 14
NEG = re.compile(r"\b(?:not|no|never|don't|doesn't|cannot|can't|without|nothing|nobody)\b", re.I)


def _load():
    """(plugin module, kit.plugin, overlap model, idx, lexicon sems) of the frozen pools (families.T27.run_pilot loader)."""
    import run_pilot as RP
    cm = RP._t27()
    kit = cm.__enter__()
    P = sys.modules["families.T27.plugin"]
    from families.T27 import overlap as OV
    return P, kit.plugin, OV, kit.plugin._index(), kit.plugin.lexicon.sems


def qid(action: str, framing: str, band: str) -> str:
    return "o" + hashlib.sha1(f"T27-ovl-i2|{action}|{framing}|{band}".encode()).hexdigest()[:10]


def items(P, plug, idx) -> list:
    out = []
    for a in sorted(P.ACTIONS):
        for fr in ("gate", "plain"):
            if not idx.get(f"req.{a}.{fr}"):
                continue
            for band in BANDS:
                out.append({"qid": qid(a, fr, band), "action": a, "framing": fr, "band": band, "n": N_FORMS[fr]})
    return out


def user_words(P, OV, plug, idx, a: str) -> list:
    """The words of the user's text for tasks that allow `a`: its allowed-list phrase and those tasks' wordings."""
    words = set(OV.stems(P.DISPLAY[a]))
    for t, sc in P.TASK_SCOPE.items():
        if a in sc:
            for tf in idx.get(t, []):
                words |= OV.stems(plug.lexicon.forms[tf].text)
    return sorted(words)


def problems(P, OV, plug, idx, a: str, fr: str, band: str, text: str) -> list:
    """Wording and band problems of one authored clause (empty = admitted to G-LEX)."""
    out = []
    n_item = text.count("{ITEM}")
    if fr == "gate" and n_item != 1:
        out.append("a gate clause holds {ITEM} exactly once")
    if fr == "plain" and "{" in text:
        out.append("a plain clause holds no slot")
    if re.sub(r"\{ITEM\}", "", text).count("{") or re.search(r"\{(?!ITEM\})", text):
        out.append("only the slot {ITEM} is allowed")
    if text != text.strip() or text[:1].isupper() or text.endswith((".", "!", "?")) or "\n" in text:
        out.append("start in lower case, no final punctuation, one line")
    if not 3 <= len(text.split()) <= 24:
        out.append("3 to 24 words")
    if NEG.search(text):
        out.append("no negation")
    low = text.lower()
    for w in plug.LABEL_WORDS:
        if w in low:
            out.append(f"label word {w!r}")
    if text in {f.text for f in plug.lexicon.forms.values()}:
        out.append("already in the lexicon")
    m = plug._ovl()
    for t, sc in P.TASK_SCOPE.items():
        if a not in sc or not idx.get(t):
            continue
        # a stand-in form: the model reads the clause text, so a fake form id is registered for the measure only
        fid = "_cand"
        plug.lexicon.forms[fid] = type("F", (), {"text": text})()
        m._r.pop(fid, None)
        try:
            bands = {OV.band(m.o(t, tf, a, fid)) for tf in idx[t]}
        finally:
            del plug.lexicon.forms[fid]
            m._r.pop(fid, None)
            m._o = {k: v for k, v in m._o.items() if k[2] != fid}
        if band not in bands:
            out.append(f"no wording of {t} puts it in the band {band}")
    return out


def _header(kind: str, tid: str, n: int, task_f: Path, ans_f: Path, what: str) -> str:
    return (f"T27 {kind} TASK  --  THIS ONE FILE IS YOUR COMPLETE TASK\n{'=' * 100}\nTASK ID : {tid}\nITEMS   : {n}\n"
            f"TASK FILE (this file)  : {task_f}\nANSWER FILE (write here): {ans_f}\n\nFILE RULES\n"
            "- Open only this file. Do not open, list or search any other file or folder.\n"
            f"- Create exactly one file, {ans_f}, with the Write tool, holding the finished JSON object. Write no notes or\n"
            "  other files. Do not put the answer in chat; when the file is written reply with the single word DONE.\n\n" + what)


def write_tasks(root: Path = ROOT) -> list:
    P, plug, OV, idx, sems = _load()
    its = items(P, plug, idx)
    (root / "tasks").mkdir(parents=True, exist_ok=True)
    (root / "answers").mkdir(parents=True, exist_ok=True)
    paths = []
    for c in range(0, len(its), CHUNK):
        chunk = its[c:c + CHUNK]
        tid = f"T27-author_ovl-{hashlib.sha1(chr(10).join(i['qid'] for i in chunk).encode()).hexdigest()[:8]}-000"
        tf, af = root / "tasks" / f"{tid}.txt", root / "answers" / f"{tid}.json"
        body = [
            "WHAT TO DO\nYou write short request clauses for a training dataset. A web page, email or tool output tells an AI assistant to do\n"
            "one thing. For every item below, write the requested number of different clauses that ask for THE SAME ACTION as the item's\n"
            "examples, in other words. Answer as ONE JSON object: {\"<qid>\": [\"clause\", ...], ...} with exactly the number of clauses each item names.\n\n"
            "RULES (every clause)\n- lower case start, one line, no final punctuation, 3 to 24 words, no negation.\n"
            "- it asks for the action itself, as an instruction to the reader (an imperative); do not name any rule, permission, scope or task.\n"
            "- a GATE item: the clause says that doing the action makes {ITEM} available (unlocks, reveals or shows it). Write the slot {ITEM}\n"
            "  exactly once, as the literal text {ITEM}; no other braces.  A PLAIN item: no slot, no mention of anything unlocked.\n"
            "- band NONE: use none of the AVOID words (or their inflections or spelling variants), name the same act and thing with other words\n"
            "  (a synonym verb, a description of the object).  band PARTIAL: reuse at most ONE of the AVOID words and write every other\n"
            "  content word fresh; fewer than half of your content words may come from the AVOID words.\n"
            "- keep the action unmistakable: another reader must be able to tell which of the actions it is (it is read again later).\n\nITEMS\n"]
        for it in chunk:
            a, fr = it["action"], it["framing"]
            ex = [plug.lexicon.forms[f].text for f in idx[f"req.{a}.{fr}"]][:3]
            body.append(json.dumps({"qid": it["qid"], "write": it["n"], "framing": fr.upper(), "band": it["band"].upper(),
                                    "action_meaning": P.V.ACTIONS[a][1], "examples": ex,
                                    "AVOID": user_words(P, OV, plug, idx, a)}, ensure_ascii=False) + "\n")
        tf.write_text(_header("AUTHORING", tid, len(chunk), tf, af, "".join(body)), encoding="utf-8")
        (root / "tasks" / f"{tid}.items.json").write_text(json.dumps(chunk, indent=1))
        paths.append(str(tf))
    return paths


def stage2(root: Path = ROOT) -> dict:
    P, plug, OV, idx, sems = _load()
    meta = {i["qid"]: i for i in items(P, plug, idx)}
    ok, bad = [], {}
    for af in sorted((root / "answers").glob("*.json")):
        ans = json.loads(af.read_text(encoding="utf-8"))
        for q, texts in ans.items():
            it = meta.get(q)
            if it is None or not isinstance(texts, list) or len(texts) != it["n"] or len(set(texts)) != len(texts):
                bad[q] = ["unknown qid or the wrong number of distinct clauses"]
                continue
            for t in texts:
                pr = problems(P, OV, plug, idx, it["action"], it["framing"], it["band"], t) if isinstance(t, str) else ["not text"]
                if pr:
                    bad.setdefault(q, []).extend(f"{t!r}: {x}" for x in pr)
                else:
                    ok.append({"sem_id": f"req.{it['action']}.{it['framing']}", "text": t, "band": it["band"], "qid": q})
    (root / "glex_tasks").mkdir(parents=True, exist_ok=True)
    (root / "glex_answers").mkdir(parents=True, exist_ok=True)
    (root / "admitted").mkdir(parents=True, exist_ok=True)
    cand = [dict(c, cid="c" + hashlib.sha1((c["sem_id"] + "|" + c["text"]).encode()).hexdigest()[:10]) for c in ok]
    (root / "admitted" / "candidates.json").write_text(json.dumps(cand, indent=1, ensure_ascii=False))
    closed = sorted(s for s in sems if s.startswith("req."))
    closed_txt = "\n".join(f"- {s}: {sems[s].meaning}" for s in closed)
    paths = []
    for c in range(0, len(cand), 40):
        chunk = cand[c:c + 40]
        for read in ("read1", "read2"):
            tid = f"T27-glex_ovl-{read}-{c // 40:03d}"
            tf, af = root / "glex_tasks" / f"{tid}.txt", root / "glex_answers" / f"{tid}.json"
            what = ("WHAT TO DO\nEach item is one clause an assistant read in some content. For every item name which request it is: pick EXACTLY ONE\n"
                    "sem id from the closed list below (the id before the colon). Answer as ONE JSON object {\"<cid>\": \"<sem id>\", ...}.\n\n"
                    "CLOSED LIST\n" + closed_txt + "\n\nITEMS\n" +
                    "".join(json.dumps({"cid": x["cid"], "text": x["text"]}, ensure_ascii=False) + "\n" for x in chunk))
            tf.write_text(_header("MEANING-NAMING", tid, len(chunk), tf, af, what), encoding="utf-8")
            paths.append(str(tf))
    rep = {"admitted_to_glex": len(cand), "rejected": bad, "glex_tasks": paths}
    (root / "admitted" / "stage2_report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    return rep


def stage3(root: Path = ROOT, run: bool = False, out: Path | None = None) -> dict:
    cand = json.loads((root / "admitted" / "candidates.json").read_text(encoding="utf-8"))
    reads: dict = {}
    for af in sorted((root / "glex_answers").glob("*.json")):
        read = "read1" if "read1" in af.name else "read2"
        for cid, sem in json.loads(af.read_text(encoding="utf-8")).items():
            reads.setdefault(cid, {})[read] = sem
    forms, dropped = [], []
    for c in cand:
        r = reads.get(c["cid"], {})
        if r.get("read1") == c["sem_id"] and r.get("read2") == c["sem_id"]:
            fr = c["sem_id"].rsplit(".", 1)[1]
            forms.append({"extractions": [["read1:T27-glex_ovl", c["sem_id"]], ["read2:T27-glex_ovl", c["sem_id"]]],
                          "family": "T27", "form_id": f"{c['sem_id']}#{hashlib.sha256(c['text'].encode()).hexdigest()[:8]}",
                          "haiku_prompt_sha": "ovl_i2", "haiku_task_id": "T27-author_ovl", "held_out": False,
                          "kind": "deontic", "sem_id": c["sem_id"], "slots": {"ITEM": "category"} if fr == "gate" else {},
                          "source": "haiku", "status": "admitted", "text": c["text"], "unit_ok": True})
        else:
            dropped.append(c["cid"])
    (root / "admitted").mkdir(parents=True, exist_ok=True)
    (root / "admitted" / "lexicon_supplement.json").write_text(json.dumps({"forms": forms}, indent=1, ensure_ascii=False))
    pend = out or (HERE / "pilot_i2" / "G13_PENDING.txt")
    pend.parent.mkdir(parents=True, exist_ok=True)
    pend.write_text("G13-seed pending for the forms in haiku/ovl_i2/admitted/lexicon_supplement.json:\n" +
                    "\n".join(f["form_id"] for f in forms) + "\n")
    if run:
        py = sys.executable
        for argv in ([py, "-B", "families/T27/run_pilot_i2.py"],
                     [py, "-B", "families/T27/run_pilot_i2.py", "--dry-run", "--n", "6000", "--no-g15", "--g6-at-size"]):
            subprocess.run(argv, cwd=C2_BUILD, check=False)
    return {"admitted": len(forms), "dropped": dropped}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("step", choices=("tasks", "stage2", "stage3"))
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root)
    r = {"tasks": write_tasks, "stage2": stage2}.get(a.step, lambda r: stage3(r, a.run))(root)
    print(json.dumps(r if a.step != "tasks" else {"task_files": len(r), "first": r[0]}, indent=1)[:1500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
