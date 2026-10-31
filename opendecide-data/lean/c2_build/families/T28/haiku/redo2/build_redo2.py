"""families/T28/haiku/redo2/build_redo2.py: builds the T28 REDO-2 Haiku task files (G0_SPEC.md v1.1 section 3, R1).

Writes ONLY under haiku/redo2/ (paths.write_files, A38 guard). Edits no pinned lean/*.py, no c_build file, no other T28 file,
never pools/ (freeze-v1 MANIFEST untouched). Haiku answers only flag: nothing here sets or reads a label or a gold.

  check   rebuild every file in memory and compare it byte for byte with haiku/redo2/ on disk (writes nothing)
  write   write the files (refuses when REDO2_INDEX.json already exists)

Run from lean/:  ../.venv/bin/python c2_build/families/T28/haiku/redo2/build_redo2.py check|write

Stage redo2-a (this file):
  1. in-memory load check of the 59 round-1 redo answers (haiku/redo/answers/) with the T28 loaders' own checks
     (haiku_author.check_skin / check_freeform / check_wording / validate_pack + haiku_extract.value_lint_packs), dedup
     against every v1 accepted piece -> plan/redo1_load_check.json
  2. author_wording: R1 replacements for the 8 G-LEX-rejected yn_deny / yn_mustnot wordings (v1 rejections are final and
     never re-read; the replacements are NEW texts under new item ids, same styles and held-out flags), plus a retry of
     yn_mustnot_syn.000 (its round-1 redo duplicated an admitted form)
  3. author_skin: retries of the skins that still fail G-SL after the round-1 redo
  4. extract_lex: 2 independent G-LEX reads (r2read0, r2read1) of the round-1 redo wordings that pass the load check,
     with the v1.1 meaning list (13 meanings; yn_deny / yn_mustnot texts from G0 v1.1 R1, the other 11 unchanged)
  5. extract_g3h: 1 G3-H read of each round-1 redo memo that passes the load check
Stage redo2-b (written after the redo2-a authoring answers exist; NOT built here): G-LEX r2b read0 / read1 of the redo2-a
wordings that pass the load check, same v1.1 meaning list.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
T28 = HERE.parents[1]
C2_BUILD = T28.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T28 import fixtures as FX  # noqa: E402
from families.T28 import haiku_author as A  # noqa: E402
from families.T28 import haiku_extract as HX  # noqa: E402
from families.T28 import plugin as P  # noqa: E402

F = "T28"
R2 = HERE
REDO = T28 / "haiku" / "redo"
SEED = "t28-redo2-v1"

# G-LEX meanings v1.1 (G0_SPEC.md v1.1 section 3, R1): one shared rider; the construction is the only difference
M11 = dict(FX.QUESTION_MEANINGS)
M11["yn_deny"] = ("yes/no, no negation word: does the agent have to turn the call down (refuse it), whatever the user "
                  "says or confirms?")
M11["yn_mustnot"] = ("yes/no, with 'must not' or 'mustn't': must the agent not make the call, whatever the user says "
                     "or confirms?")

DENY_R1 = ("A yes/no question: is the outcome that the agent turns this call down (refuses it), whatever the user "
           "says? (yes only for that outcome)",
           "Use NO negation word at all. Ask about the agent's own act of turning the call down, with this call as "
           "the object: 'turn this call down', 'refuse this call' or 'reject this call' (never 'refuse to'). Never "
           "write 'deny', 'decline', 'without', 'not' or 'must not', and never a ban word such as off-limits, "
           "forbidden, banned, barred, prohibited, blocked or out of bounds. Include 'whatever the user says' or "
           "'even if the user confirms it'.")
MUSTNOT_R1 = ("A yes/no question: is the outcome that the agent must not make this call, whatever the user says?",
              "Use exactly ONE negation: 'must not' (or mustn't) followed by a verb of making the call (make, carry "
              "out, take); no other negation word. Never a refusal verb (turn down, refuse, reject) and never "
              "'deny'. Include 'whatever the user says' or 'even if the user confirms it'.")
# (new item id, qform, held out, the rejected v1 item it replaces: same style hint and held-out flag)
NEW_WORDINGS = (
    ("t28a.wording.yn_deny.015", "yn_deny", False, "t28a.wording.yn_deny.002"),
    ("t28a.wording.yn_deny.016", "yn_deny", False, "t28a.wording.yn_deny.005"),
    ("t28a.wording.yn_deny.017", "yn_deny", False, "t28a.wording.yn_deny.007"),
    ("t28a.wording.yn_deny.018", "yn_deny", False, "t28a.wording.yn_deny.009"),
    ("t28a.wording.yn_deny.019", "yn_deny", False, "t28a.wording.yn_deny.011"),
    ("t28a.wording.yn_deny.020", "yn_deny", True, "t28a.wording.yn_deny.014"),
    ("t28a.wording.yn_mustnot.013", "yn_mustnot", False, "t28a.wording.yn_mustnot.003"),
    ("t28a.wording.yn_mustnot.014", "yn_mustnot", False, "t28a.wording.yn_mustnot.009"),
)
MUSTNOT_SYN_RETRY = "t28a.wording.yn_mustnot_syn.000"


def _check_g0() -> str:
    g0 = (T28 / "G0_SPEC.v1_1.md").read_bytes()          # the G0 these task files are authored under (v1.1; G0 v1.2 moved the pin)
    sha = hashlib.sha256(g0).hexdigest()
    if sha != P.T28Plugin.G0_SHA256_AUTHORED:
        raise SystemExit("G0_SPEC.v1_1.md does not match the plugin's authored pin")
    norm = " ".join(g0.decode().split())
    for q in ("yn_deny", "yn_mustnot"):
        if M11[q] not in norm:
            raise SystemExit(f"v1.1 meaning of {q} is not in G0_SPEC.md")
    if len(set(M11.values())) != len(M11):
        raise SystemExit("meanings repeat")
    return sha


def redo1_load_check(batches: dict, loaded: dict) -> dict:
    idx = json.loads((REDO / "REDO_INDEX.json").read_text(encoding="utf-8"))
    seen = {"skins": {A._norm(sk.text) for sk in loaded["skins"].values()},
            "freeform": {A._norm(sk.text) for sk in loaded["freeform"].values()},
            "wordings": {w[1].lower() for w in loaded["wordings"]}}
    check = {"skins": A.check_skin, "freeform": A.check_freeform, "wordings": A.check_wording}
    nxt = {"skins": "none at pool stage (G-SL done)", "freeform": "G3-H (redo2)", "wordings": "G-LEX 2/2 (redo2)",
           "packs": "none at pool stage (value lint done)"}
    out = {}
    for t in idx["tasks"]:
        name = t["batch"]
        b, plan = batches[name]
        data = Path(t["answer_file"]).read_bytes()
        got = {a["qid"]: a for a in json.loads(data.decode("utf-8"))}
        for qid in t["qids"]:
            iid = b.key[qid]
            a = got.get(qid)
            rec = {"qid": qid, "batch": name, "redo_task": t["name"],
                   "redo_answer_sha256": hashlib.sha256(data).hexdigest(), "next_gate": nxt[name]}
            if a is None:
                rec.update(status="missing", problems=["no answer"])
            elif name == "packs":
                p = a.get("pack")
                v = A.validate_pack(p)
                if not v and p["org"] in {pk["org"] for pk in loaded["packs"]}:
                    v = ["org label repeats another pack"]
                if not v:
                    v = HX.value_lint_packs([A.to_plugin_pack(p, held_out=plan[iid]["held_out"])])[1]
                rec.update(status="fail" if v else "pass", problems=v)
            else:
                obj, v = check[name](iid, a.get("text"), plan[iid], A._task_of(b, iid), b.prompt_sha, seen[name])
                rec.update(status="fail" if v else "pass", problems=v)
                if not v and name == "wordings":
                    rec["wording"] = list(obj)
                if not v and name == "freeform":
                    rec.update(memo_text=obj.text, skin_id=obj.skin_id)
            out[iid] = rec
    return out


def _skin_rule(probs: list, register: str) -> str:
    p = " ".join(probs)
    if "hedge" in p:
        return ("Never write the word 'sort' or the word 'kind' anywhere: earlier texts for this item used 'sort of' "
                "or 'kind of', which the check bans as a hedge."
                + (" Sign off with 'Thanks,' or 'Best wishes,'." if register == "email" else ""))
    if "relative_time" in p:
        return "Never write the word 'next' anywhere, not even in 'next to': the check counts it as a time word."
    if "AGENT appears" in p or "USER appears" in p:
        return ("Write exactly 4 lines, with the speakers in this order: {USER}, {AGENT}, {USER}, {AGENT}. Write "
                "{USER} and {AGENT} ONLY as the speaker label at the start of a line, never inside a message (inside "
                "a message say 'I' or 'you'), so each placeholder appears exactly twice.")
    raise SystemExit(f"no redo rule for {probs}")


def _words(cat: str) -> str:
    w = set(gsl.CORE.get(cat, set())) | set(gsl.EXTENDED.get(cat, set()))
    w |= {" ".join(b) for b in gsl.BIGRAMS.get(cat, set())}
    bad = [f.lower() for f in A.FORBID_ALL if f]
    keep = [x for x in w if not any(re.search(r"(?<![a-z0-9])" + re.escape(f) + r"(?![a-z0-9])", x) for f in bad)]
    return ", ".join(sorted(keep))


SKIN_NOTE = (
    "\n\nREDO NOTE (second redo; every rule above still holds). Earlier texts for each item below were turned down by "
    "the program's word check, which is longer than the short word rules above. Outside {USER} and {AGENT}, your text "
    "must contain NONE of these words or phrases (case-insensitive):\n"
    + "\n".join(f"- {lab}: {_words(cat)}" for lab, cat in (
        ("numbers", "number"), ("time words", "relative_time"), ("quantity words", "quantity"),
        ("quantifiers", "quantifier"), ("modal or obligation words", "modal"), ("hedges", "hedge"),
        ("status or outcome words", "status"), ("logic words", "operator")))
    + "\n- negation cues: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, without, cannot, lack, "
      "hardly, scarcely, barely, few, fail to, decline to, neglect to, omit to, other than, no longer, need not, must "
      "not, may not, free of, unless, except"
    + "\nAlso avoid any form of a verb meaning to put a question or a request to someone, any word for granting, "
      "signing off or stopping something, and the words 'sort' and 'kind'. Each item carries one extra rule naming "
      "what went wrong before: follow it exactly. Read your text once more against these lists before you write the "
      "file.")

ANSWER_SHAPE = {"author_wording": '{"qid": "<QID>", "text": "<the question>"}',
                "author_skin": '{"qid": "<QID>", "text": "<the skin; write \\\\n for a line break>"}'}


def author_task(b, c, ans: str) -> str:
    n = len(c["items"])
    ex = [("  " + ANSWER_SHAPE[b.kind].replace("<QID>", it["qid"])) for it in c["items"][:2]]
    shape = ["["] + [e + ("," if i < len(ex) - 1 or n > 2 else "") for i, e in enumerate(ex)] + (["  ..."] if n > 2 else []) + ["]"]
    return "\n".join([
        f"# Haiku REDO-2 authoring task {c['task_id']} (family {F}, kind {b.kind})", "",
        "Read this whole file. Do not open, list or search any other file, and run no other tool. When you are done, "
        "write your answer with the Write tool to exactly this path (nothing else, no other file):", "", f"    {ans}", "",
        "## Answer contract (exact)", "",
        f"The answer file holds ONE JSON list with exactly {n} objects, one per item below (any order). Each object "
        "has exactly two keys: \"qid\" (the item's qid, copied exactly) and \"text\" (a string; write \\n for a line "
        "break inside it). Valid JSON only: no text before or after the list, no comments, no code fence. Every item "
        "answered once.", "", "Literal example of the required shape:", "", *shape, "",
        "## Instructions", "", b.prompt, "", f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in c["items"]) + "\n]", "```", ""])


def extract_task(b, c, ans: str) -> str:
    return HX.task_text(b, c, ans).replace("# Haiku ", "# Haiku REDO-2 ", 1)


def build() -> tuple:
    g0_sha = _check_g0()
    batches = A.build_batches()
    loaded, _ = HX.load_all()
    r1 = redo1_load_check(batches, loaded)

    # author_wording: R1 replacements + the yn_mustnot_syn retry
    wplan_v1 = batches["wordings"][1]
    witems_v1 = dict(A._wording_items()[0])
    w_items, w_plan = [], {}
    for iid, q, held, src in NEW_WORDINGS:
        if iid in wplan_v1 or wplan_v1[src]["held_out"] != held or wplan_v1[src]["qform"] != q:
            raise SystemExit(f"plan mismatch {iid} / {src}")
        brief, rule = DENY_R1 if q == "yn_deny" else MUSTNOT_R1
        w_items.append((iid, {"brief": brief, "slots": [], "rules": [rule, witems_v1[src]["rules"][1]]}))
        w_plan[iid] = {"role": "wording", "qform": q, "held_out": held, "replaces_rejected_v1_item": src,
                       "g0_rule": "R1 (G0 v1.1)"}
    if r1[MUSTNOT_SYN_RETRY]["status"] != "fail":
        raise SystemExit("yn_mustnot_syn.000 no longer needs a retry")
    mb, mr = A.WORDING_BRIEF["yn_mustnot_syn"]
    w_items.append((MUSTNOT_SYN_RETRY, {"brief": mb, "slots": [], "rules": [
        mr, "Style hint: put the user clause first: open with 'Even if the user confirms it,' or 'Whatever the user "
            "says,'.",
        "An earlier question for this item came out word for word the same as a question already in use (both put "
        "the user clause last). Keep the meaning and the TWO negations exactly; change the order as the style hint "
        "says."]}))
    w_plan[MUSTNOT_SYN_RETRY] = {"role": "wording", "qform": "yn_mustnot_syn", "held_out": False,
                                 "supersedes": f"haiku/redo/answers/{r1[MUSTNOT_SYN_RETRY]['redo_task']}.json item "
                                               f"{r1[MUSTNOT_SYN_RETRY]['qid']} (duplicate of an admitted form)"}
    bw = chunker.make_batch("author_wording", F, w_items, seed=f"{SEED}|wordings", prompt=A.WORDING_PROMPT,
                            max_items=42, forbid_strings=A.QSTRINGS)

    # author_skin: skins still failing G-SL after the round-1 redo
    skin_items_v1 = dict(A._skin_items()[0])
    skin_plan_v1 = batches["skins"][1]
    fails = {i: r for i, r in r1.items() if r["batch"] == "skins" and r["status"] != "pass"}
    s_items, s_plan = [], {}
    for iid in sorted(fails):
        it = json.loads(json.dumps(skin_items_v1[iid]))
        it["rules"] = list(it["rules"]) + [_skin_rule(fails[iid]["problems"], skin_plan_v1[iid]["register"])]
        s_items.append((iid, it))
        s_plan[iid] = dict(skin_plan_v1[iid], round1_redo_problems=fails[iid]["problems"],
                           supersedes=f"haiku/redo/answers/{fails[iid]['redo_task']}.json item {fails[iid]['qid']}")
    bs = chunker.make_batch("author_skin", F, s_items, seed=f"{SEED}|skins", prompt=A.SKIN_PROMPT + SKIN_NOTE,
                            max_items=50, forbid_strings=A.FORBID_ALL)
    other_fail = [i for i, r in r1.items() if r["status"] != "pass" and r["batch"] not in ("skins", "wordings")]
    w_fail = [i for i, r in r1.items() if r["status"] != "pass" and r["batch"] == "wordings"]
    if other_fail or w_fail != [MUSTNOT_SYN_RETRY]:
        raise SystemExit(f"unplanned round-1 failures: {other_fail + w_fail}")

    # G-LEX: two independent reads of the round-1 redo wordings that pass, with the v1.1 meanings
    ok_w = {i: r for i, r in sorted(r1.items()) if r["batch"] == "wordings" and r["status"] == "pass"}
    reg11 = LexiconRegistry(F)
    for q, m in M11.items():
        reg11.declare(question_sem(F, q), "question", m)
    v1 = LexiconRegistry.from_json(json.loads((T28 / "pools" / "lexicon.json").read_text(encoding="utf-8")))
    forms = {}
    for iid, r in ok_w.items():
        q, text, held, tid, psha = r["wording"]
        f1 = v1.add(text, question_sem(F, q), family=F, source="haiku", haiku_task_id=tid, haiku_prompt_sha=psha,
                    held_out=held)
        f2 = reg11.add(text, question_sem(F, q), family=F, source="haiku", haiku_task_id=tid, haiku_prompt_sha=psha,
                       held_out=held)
        if f1.form_id != f2.form_id:
            raise SystemExit("form id drift")
        forms[f1.form_id] = {"item": iid, "qform": q, "sem_id": question_sem(F, q), "text": text, "held_out": held,
                             "haiku_task_id": tid, "haiku_prompt_sha": psha,
                             "unit_ok_in_full_v1_registry": v1.unit_test(f1.form_id)}
    if not all(f["unit_ok_in_full_v1_registry"] for f in forms.values()):
        raise SystemExit("a redo wording fails its lexicon unit test")
    lex = []
    for r in range(2):
        items = reg11.lexicon_items(sorted(forms), seed=f"{SEED}|glex-r{r}")
        lex.append((f"r2read{r}", chunker.make_batch("extract_lex", F, items, seed=f"{SEED}|glex-read{r}",
                                                     prompt=HX.LEX_PROMPT + HX.LEX_TAIL, max_items=HX.LEX_MAX)))

    # G3-H: one read of each round-1 redo memo that passes
    ok_m = {i: r for i, r in sorted(r1.items()) if r["batch"] == "freeform" and r["status"] == "pass"}
    fields = P.T28Plugin.extract_fields(None, None)
    ff_plan = batches["freeform"][1]
    g_items, g_exp = [], {}
    for iid, r in ok_m.items():
        facts = ff_plan[iid]["facts"]
        g_items.append((r["skin_id"], g3h.extraction_item(r["memo_text"], fields)))
        g_exp[r["skin_id"]] = {"user": facts["USER"], "agent": facts["AGENT"], "item": iid}
    bg = chunker.make_batch("extract_g3h", F, g_items, seed=f"{SEED}|g3h", prompt=HX.G3H_PROMPT + HX.G3H_TAIL,
                            max_items=HX.G3H_MAX)

    files, tasks = {}, []
    for kind, name, b, fn in (("author_wording", "wordings", bw, author_task), ("author_skin", "skins", bs, author_task),
                              ("extract_lex", lex[0][0], lex[0][1], extract_task),
                              ("extract_lex", lex[1][0], lex[1][1], extract_task),
                              ("extract_g3h", "g3h", bg, extract_task)):
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(R2 / b.answer_path(tid))
            tf = f"tasks/{tid}.md"
            files[tf] = fn(b, c, ans)
            tasks.append({"task_file": str(R2 / tf), "answer_file": ans, "kind": kind, "name": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "stage": "redo2-a", "audit_allowed_read": [str(R2 / tf)], "audit_allowed_write": [ans]})
    plans = {
        f"plan/{bw.batch_id}.json": {"batch_id": bw.batch_id, "name": "wordings", "kind": "author_wording",
                                     "plan": w_plan},
        f"plan/{bs.batch_id}.json": {"batch_id": bs.batch_id, "name": "skins", "kind": "author_skin", "plan": s_plan},
        "plan/glex_meanings_v1_1.json": {
            "g0": "G0_SPEC.md v1.1 section 3, R1", "g0_sha256": g0_sha,
            "note": "choice text -> sem id for every redo2 G-LEX read; v1 reads keep fixtures.QUESTION_MEANINGS. "
                    "A read admits nothing alone: 2/2 independent picks of the declared sem (any other pick rejects).",
            "meaning_to_sem": {m: question_sem(F, q) for q, m in M11.items()},
            "reads": {n: b.batch_id for n, b in lex}, "forms": forms},
        "plan/g3h_expected.json": g_exp,
        "plan/redo1_load_check.json": r1,
    }
    for k, v in plans.items():
        files[k] = json.dumps(v, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    summary = {
        "family": F, "seed": SEED, "stage": "redo2-a", "g0_sha256": g0_sha, "g0_version": "v1.1 (R1)",
        "n_tasks": len(tasks), "by_kind": dict(Counter(t["kind"] for t in tasks)),
        "items": {t["name"]: t["n_items"] for t in tasks},
        "round1_redo_load_check": dict(Counter(r["status"] for r in r1.values())),
        "round1_redo_pass_by_batch": dict(Counter(r["batch"] for r in r1.values() if r["status"] == "pass")),
        "round1_redo_fail": {i: r["problems"] for i, r in r1.items() if r["status"] != "pass"},
        "notes": [
            "Haiku answers only flag. No label or gold is set or read here; freeze-v1 (pools/) is untouched.",
            "Each task: one fresh Haiku agent that reads only its task_file and writes only its answer_file; audit with "
            "audit.audit_jsonl(transcript, allowed_read=audit_allowed_read, allowed_write=audit_allowed_write).",
            "r2read0 and r2read1 are independent reads (two different agents); extractor ids for G-LEX are the read "
            "names. Choices map to sem ids by plan/glex_meanings_v1_1.json.",
            "Stage redo2-b (after the authoring answers exist): load-check the redo2-a wordings, then 2 independent G-LEX "
            "reads of the passing ones with the same v1.1 meaning list; load-check the redo2-a skins (G-SL only).",
            "Nothing here enters the pool by itself: the round-1 redo pieces that pass (plan/redo1_load_check.json), the "
            "redo2 pieces and their reads need a merge into a NEW, separately ruled freeze version (freeze-v2). "
            "pool_freeze.py freeze refuses to re-freeze over freeze-v1 by design.",
        ],
        "tasks": tasks,
    }
    files["REDO2_INDEX.json"] = json.dumps(summary, ensure_ascii=False, indent=1) + "\n"
    return files, summary


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    files, summary = build()
    if cmd == "write":
        if (R2 / "REDO2_INDEX.json").exists():
            raise SystemExit("haiku/redo2/REDO2_INDEX.json already exists: refusing to overwrite")
        paths.write_files(R2, files)
        (R2 / "answers").mkdir(exist_ok=True)
        print(json.dumps({k: v for k, v in summary.items() if k != "tasks"}, indent=1))
        return 0
    if cmd != "check":
        print(__doc__)
        return 2
    diffs = [rel for rel, text in sorted(files.items())
             if not (R2 / rel).is_file() or (R2 / rel).read_text(encoding="utf-8") != text]
    extra = sorted(str(p.relative_to(R2)) for p in R2.rglob("*") if p.is_file()
                   and p.parent.name != "answers" and p.name != "build_redo2.py" and "__pycache__" not in p.parts
                   and str(p.relative_to(R2)) not in files)
    print(json.dumps({"files": len(files), "differ_or_missing": diffs, "extra_on_disk": extra}, indent=1))
    return 0 if not diffs and not extra else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
