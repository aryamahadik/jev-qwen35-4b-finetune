"""families/T27/redo2.py: T27 supplement tasks for the Stage A blockers B1-B3 (G0_SPEC.md v1.1, P49, P50 and section 8;
c2_build/README.md "Haiku task flow"; PREREG A37 b). Haiku writes text only; nothing here sets a label.

B1  support_chat carriers. The first briefs did not say that a request and its reason share one line in a register whose
    every line starts with a role label, so 51 of 56 L1 / L2 texts failed authoring.lint_skin's placement rule. The lint
    is unchanged. Two new skin tasks state the one-line rule (G0 P49).
B2  yn_dneg_beyond wordings. The first brief asked for "false that", which negcount counts as a non-core cue (k_all 3,
    want 2). One new wording task states the only k_syn = k_all = 2 shape (G0 P50). authoring.lint_wording is unchanged;
    lint_dneg adds the P50 shape checks on top of it (it only drops).
B3  The 26 written G-LEX reads are a deterministic function of the kept pools of haiku/author/ (extract_check.files_check).
    Nothing here touches those pools or that code: the supplement lives in haiku/redo2/, and its wordings get their own
    G-LEX 2/2 reads in haiku/redo2/extract/ (2 tasks). Each read also carries admitted-pool control wordings of the other
    question forms so the pick is a real choice; controls are reported only and never recorded (they have their reads).

  python -m families.T27.redo2 tasks            in memory: the 3 authoring tasks (task_file, answer_file, kind)
  python -m families.T27.redo2 write            after A38: write them under haiku/redo2/ (once)
  python -m families.T27.redo2 load [--write]   lint the answers (authoring.lint_piece + lint_dneg), merge with
                                                haiku/author/linted.json, check every G0 section 6 minimum on the merge;
                                                --write: haiku/redo2/linted.json
  python -m families.T27.redo2 glex-plan        in memory: the 2 supplement G-LEX reads (needs haiku/redo2/linted.json)
  python -m families.T27.redo2 glex-write       write them under haiku/redo2/extract/ (once)
  python -m families.T27.redo2 glex-check [--record]   judge the 2 reads; --record: haiku/redo2/extract/record/VALIDATION.json
  (run from lean/c2_build with ../../.venv/bin/python)

Every task file a Haiku agent reads is ONE self-contained text file (<task_id>.txt) with the contract inline; the JSON
chunk, prompt, key and manifest beside it are the kit's provenance files (chunker.make_batch), never sent to Haiku.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_C2 = HERE.parents[1]
if str(_C2) not in sys.path:
    sys.path.insert(0, str(_C2))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

from . import authoring as A  # noqa: E402
from . import extract_check as E  # noqa: E402
from . import glex_build as G  # noqa: E402

FAMILY = A.FAMILY
ROOT = HERE / "haiku" / "redo2"
GLEX_ROOT = ROOT / "extract"
MAIN_LINTED = HERE / "haiku" / "author" / "linted.json"
MAIN_TASKS = HERE / "haiku" / "extract" / "TASKS.json"
SEED = "T27-author-redo2-v1"
GLEX_SEED = "T27-glex-redo2"
READS = ("read1", "read2")
N_SC = {"redo2a": {"L1": 22}, "redo2b": {"L1": 18, "L2": 14}}      # support_chat: L1 40, L2 14 more (G0 section 8)
N_DNEG = 12                                                          # yn_dneg_beyond: 12 more
CONTROLS = {"yn_not_beyond": 8, "yn_beyond": 6, "yn_within": 4, "ch_next": 4}   # per supplement read, never recorded
LEX_POOLS = ("req", "info", "task", "wording")

PROMPT = ("You write short text pieces for a training dataset. Read your task file (one text file) and follow it exactly. "
          "Write your answer only to the file it names, as one JSON object keyed by the qid of each item. Do not open "
          "any other file.")

# ------------------------------------------------------------------------------------------------ B1: support_chat

SC_GUIDE = ("a support chat transcript in which only the organisation's agent speaks; every line starts with a short role "
            "label such as 'agent:' (a first header line may read '{SOURCE} support: ...'); greetings, the slot "
            "sentences and a closing line. ONE-LINE RULE: a request and its reason always share ONE line, written "
            "'agent: {cap|REQ1}. {cap|JUST1}.' with one space between the two sentences and nothing else between "
            "them; the reason never goes on a line of its own and never after a second role label")


def _sc_slots(layout: str) -> dict:
    d = A._skin_slots_desc(layout)
    d["{cap|REQ1}"] = ("a request sentence the program supplies (it starts with a verb); write it as '{cap|REQ1}.' right "
                       "after the role label of its line: 'agent: {cap|REQ1}. {cap|JUST1}.'")
    d["{cap|JUST1}"] = ("the reason given for that request, supplied by the program; write it exactly as '{cap|JUST1}.' "
                        "on the SAME line, right after '{cap|REQ1}.' with one space between them")
    if layout == "L2":
        d["{cap|REQ2}"] = ("a second request sentence, on a later line than the {cap|JUST1} sentence, written the same "
                           "way: 'agent: {cap|REQ2}. {cap|JUST2}.'")
        d["{cap|JUST2}"] = ("the reason for the second request: '{cap|JUST2}.' on the SAME line, right after "
                            "'{cap|REQ2}.' with one space between them")
    return d


def _sc_item(layout: str, n: int) -> dict:
    slots = _sc_slots(layout)
    brief = (A._head() + f"ITEM: write {n} different carrier texts in the register 'support_chat', each holding exactly "
             f"these placeholders: {', '.join(slots)} (see 'slots' for how to write each). Register: {SC_GUIDE}. Each "
             "text is one piece of content the organisation {SOURCE} wrote for a reader; the program later fills each "
             "slot, and you write everything around the slots. VALUE for this qid: a JSON array of "
             f"{n} texts; each text is a JSON array of its lines (strings), with \"\" for a blank line. Make the texts "
             "clearly different from each other: different occasions and topics for this kind of organisation, "
             "different greetings, role labels, closing lines, line structure and length (4 to 14 lines).")
    pairs = "'agent: {cap|REQ1}. {cap|JUST1}.'" + (" and 'agent: {cap|REQ2}. {cap|JUST2}.'" if layout == "L2" else "")
    one_line = ("ONE-LINE RULE (a program checks it and throws away every text that breaks it): the request and its "
                f"reason share one line, {pairs}, with only one space between the two sentences. Use the same short role "
                "label on that line as on the other lines.")
    return {"brief": brief, "register": "support_chat", "slots": slots, "rules": [one_line] + A._skin_rules()}


# ------------------------------------------------------------------------------------------------ B2: yn_dneg_beyond

DNEG_PHRASE = "nothing beyond the user's task"
TRUTH = ("true", "correct", "accurate", "right", "hold", "holds")
DNEG_BANNED = ("false", "untrue", "wrong", "incorrect", "inaccurate", "mistaken", "deny", "denies", "fail", "fails",
               "lack", "lacks", "without", "or not", "not the case", "other than", "except", "unless", "only", "if",
               "when", "given", "even though", "though", "although", "since", "because", "while")


def _dneg_item(n: int) -> dict:
    brief = (A._head() + f"ITEM: write {n} different questions about the content the assistant opened and the user's "
             "task (the job the user gave the assistant). Each question asks whether a claim is NOT true, namely the "
             "claim that the content asks for nothing beyond the user's task (a double negative). VALUE for this qid: a "
             f"JSON array of {n} strings.")
    rules = [
        "One line; a direct question that ends with '?'; 8 to 30 words.",
        "Use the exact words 'nothing beyond the user's task' once ('beyond the user's task' means: not one of the "
        "actions the user's task covers); never replace them by 'outside', 'requested by the user', 'harmful', 'safe' "
        "or similar.",
        "SHAPE: the question names a claim (for example 'the claim', 'the statement', 'the idea', 'the description') "
        "that the content (for example 'the content', 'this content', 'the page', 'the message', 'the content from "
        "{SOURCE}') asks for, or requests, nothing beyond the user's task; then it asks whether that claim is NOT true, "
        "with the word 'not' AFTER the claim and right before a truth word: '... not true?', '... not correct?', '... "
        "not accurate?', '... not right?', or the verb '... not hold?'. Openings such as 'Is ...', 'Would ... be', "
        "'Does ...' fit.",
        "NEGATION: exactly two negation words, in this order: 'nothing' inside the claim, then one 'not' after the "
        "claim. No other negative word or negative meaning anywhere: never 'false', 'untrue', 'wrong', 'incorrect', "
        "'inaccurate', 'mistaken', 'deny', 'fail', 'lack', 'without', 'no', 'none', 'never', \"n't\", 'not the case', "
        "'or not', 'other than', 'except', 'unless', 'only'.",
        "Never start with a negative question such as 'Is it not true that ...', \"Isn't it ...\" or 'Is it not the "
        "case that ...': people read those as asking whether the claim IS true, which is the opposite meaning.",
        "No condition, reason or extra clause ('if', 'when', 'given that', 'even though', 'since', 'because', a second "
        "'and ...' part): the question holds only the claim and its truth word.",
        "It must make sense when the content asks for nothing at all (then the claim is simply true). Never refer to "
        "'the request', 'its requests', 'what the content asks' or 'the action it asks for' as if one surely exists.",
        f"Make the {n} questions clearly different: vary the opening, the claim word, how the content is named, the "
        "verb ('asks for', 'requests', 'calls for') and the truth word.",
        "Optional: the placeholder {SOURCE} (the organisation that wrote the content), at most once, written exactly "
        "'{SOURCE}' (for example 'the content from {SOURCE}'). No other placeholder or curly braces.",
        "No numbers, dates or names other than {SOURCE}; never mention a correct answer, an option or a verdict; "
        + A._NO_LABEL + ".",
    ] + A._gsl_words(("number", "relative_time", "hedge"))
    return {"brief": brief, "slots": {"{SOURCE}": "optional: the organisation's name"}, "rules": rules}


def lint_dneg(text: str) -> list:
    """G0 P50 shape checks for a yn_dneg_beyond wording, on top of authoring.lint_wording (both must pass)."""
    v = []
    low = text.lower()
    if DNEG_PHRASE not in low:
        v.append(f"lacks the words {DNEG_PHRASE!r}")
    c = negcount.count(K.PH_RE.sub("the sender", text))
    if list(c.syn_tokens) != ["nothing", "not"] or c.k_all != 2:
        v.append(f"P50 cues: want 'nothing' then one 'not' (k_all 2), got {list(c.syn_tokens)} / k_all {c.k_all}")
    toks = re.findall(r"[a-z]+(?:'[a-z]+)?", low)
    if "not" in toks:
        i = toks.index("not")
        nxt = toks[i + 1:i + 3]
        if not nxt or not (nxt[0] in TRUTH or (nxt[0] == "be" and len(nxt) > 1 and nxt[1] in TRUTH)):
            v.append("P50: 'not' is not right before a truth word")
    hits = [w for w in DNEG_BANNED if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)]
    if hits:
        v.append(f"P50: banned word(s) {hits}")
    return v


# ------------------------------------------------------------------------------------------------ authoring tasks

def task_defs() -> list:
    out = []
    for part, lays in N_SC.items():
        out.append({"name": f"skin_support_chat_{part}", "kind": "author_skin", "pool": "skin",
                    "items": [(f"skin|support_chat|{lay}|{part}", _sc_item(lay, n)) for lay, n in lays.items()]})
    out.append({"name": "wordings_dneg_redo2", "kind": "author_wording", "pool": "wording",
                "items": [("wording|yn_dneg_beyond", _dneg_item(N_DNEG))]})
    return out


def _txt_path(root: Path, tid: str) -> Path:
    return Path(root) / f"{tid}.txt"


def build_batches(root: Path = ROOT) -> list:
    """[(task def, TaskBatch)]: one single-chunk batch per task; every brief names its absolute answer file."""
    out = []
    forbid = A.forbid_strings()
    for td in task_defs():
        seed = f"{SEED}|{td['name']}"
        b0 = chunker.make_batch(td["kind"], FAMILY, [(i, A._with_path(it, "PENDING")) for i, it in td["items"]],
                                seed=seed, prompt=PROMPT, forbid_strings=forbid)
        tid = b0.chunks[0]["task_id"]
        answer = str(Path(root) / b0.answer_path(tid))
        b = chunker.make_batch(td["kind"], FAMILY, [(i, A._with_path(it, answer)) for i, it in td["items"]],
                               seed=seed, prompt=PROMPT, forbid_strings=forbid)
        if len(b.chunks) != 1 or b.chunks[0]["task_id"] != tid:
            raise chunker.ChunkError(f"{td['name']}: one chunk per task, stable task id")
        out.append((td, b))
    return out


_RULE = "=" * 110
_VALUE = {"author_skin": "a JSON array of texts; each text is a JSON array of its lines (strings), with \"\" for a blank "
                         "line",
          "author_wording": "a JSON array of strings, one question per string"}
_TOY = {"author_skin": ('  Toy item: qid "q0example01", brief "write 2 different postcards, each holding the placeholder '
                        '{X}".\n'
                        '  CORRECT answer file content (this and nothing else):\n'
                        '  {\n'
                        '    "q0example01": [\n'
                        '      ["Greetings from the coast", "", "{X} was lovely."],\n'
                        '      ["Hello again", "{X} made our day."]\n'
                        '    ]\n'
                        '  }\n'
                        '  WRONG (rejected by the checker):\n'
                        '  [{"qid": "q0example01", "texts": [...]}]\n'
                        '  {"answers": {"q0example01": [...]}, "task_id": "..."}\n'
                        '  {"q0example01": ["Greetings from the coast\\n{X} was lovely."]}   (a text is a list of '
                        'lines)'),
        "author_wording": ('  Toy item: qid "q0example01", brief "write 2 different questions about the weather".\n'
                           '  CORRECT answer file content (this and nothing else):\n'
                           '  {\n'
                           '    "q0example01": ["Is the sky over the harbour grey?", "Does the wind feel cold by '
                           'the river?"]\n'
                           '  }\n'
                           '  WRONG (rejected by the checker):\n'
                           '  [{"qid": "q0example01", "questions": [...]}]\n'
                           '  {"answers": {"q0example01": [...]}, "notes": "..."}\n'
                           '  {"q0example01": "Is the sky over the harbour grey?"}   (the value is a list)')}


def _bullets(lines, indent="  - ") -> str:
    return "\n".join(indent + x for x in lines)


def author_txt(td: dict, b, root: Path = ROOT) -> str:
    """The self-contained task file one Haiku agent reads (everything inline; the chunk JSON is never sent)."""
    c = b.chunks[0]
    tid = c["task_id"]
    txt, ans = str(_txt_path(root, tid)), str(Path(root) / b.answer_path(tid))
    n = len(c["items"])
    head = [
        "T27 AUTHORING TASK (REDO2)  --  THIS ONE FILE IS YOUR COMPLETE TASK", _RULE,
        "Read this top section first. It is complete: it holds your instructions, the exact answer format, a toy example",
        "and every item with its brief, slots and rules. You need nothing else and you must not open anything else.",
        "", f"TASK ID : {tid}", f"KIND    : {b.kind}  (you WRITE new text pieces)", f"ITEMS   : {n}",
        f"TASK FILE (this file)  : {txt}", f"ANSWER FILE (write here): {ans}", "",
        "INSTRUCTION", "  " + PROMPT.replace("(one text file)", "(this file)"), "",
        "FILE RULES",
        "- Open only this file. Do not open, list or search any other file or folder (no earlier answers, chunks,",
        "  prompts, keys or manifests).",
        f"- Create exactly one file, {ans}, with the Write tool, holding the finished JSON object.",
        "  Write no notes, drafts or other files. Do not put the answer in chat; when the file is written reply with the",
        "  single word DONE.", "",
        "WHAT TO DO",
        f"1. The section ITEMS (at the end) lists {n} item(s). Each has an opaque \"qid\", a BRIEF, SLOTS and RULES.",
        "   The qid is only a label; do not try to read anything into it.",
        "2. For every item, write exactly what its BRIEF asks for and follow every one of its RULES. A program checks the",
        "   rules and throws away every piece that breaks one.", "",
        "EXACT ANSWER CONTRACT",
        f"- The answer file holds ONE JSON object and nothing else. Keys: the \"qid\" of EVERY item, each exactly once",
        f"  (so the object has exactly {n} key(s)). No other keys: no \"task_id\", \"items\", \"answers\", \"notes\",",
        "  \"schema\", \"status\" or similar.",
        f"- Value of each key: {_VALUE[b.kind]}.",
        "- Valid JSON only: double quotes, no comments, no trailing commas, no text before or after the object. Keep",
        "  every placeholder such as {SOURCE} exactly as written (curly braces included).", "",
        "LITERAL EXAMPLE (toy data, NOT your items)", _TOY[b.kind], "",
        "SELF-CHECK before you finish (do it, then write the file once)",
        f"- The object has exactly {n} key(s), one per qid below, and each value has the number of pieces its BRIEF asks.",
        "- Every piece follows every RULE of its item (read the rules again for each piece).",
        "- The file is one JSON object, with no extra keys, comments or text around it.", "",
        _RULE, f"ITEMS  ({n} item(s))", _RULE]
    body = []
    for k, it in enumerate(c["items"], 1):
        body += [f"ITEM {k} of {n}    qid: \"{it['qid']}\"", "BRIEF:", "\n".join("  " + x for x in it["brief"])]
        if it.get("register"):
            body.append(f"REGISTER: {it['register']}")
        if it.get("slots"):
            body += ["SLOTS:", _bullets(f"{s}: {d}" for s, d in it["slots"].items())]
        body += ["RULES:", _bullets(it.get("rules", [])), ""]
    tail = [_RULE, f"END OF TASK FILE. Now write {ans}"]
    out = "\n".join(head + body + tail) + "\n"
    low = out.lower()
    for f in A.forbid_strings():
        if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
            raise chunker.ChunkError(f"{tid}: the task file mentions a forbidden string ({f!r})")
    return out


def task_index(batches: list, root: Path = ROOT) -> list:
    rows = []
    for td, b in batches:
        tid = b.chunks[0]["task_id"]
        rows.append({"name": td["name"], "pool": td["pool"], "kind": td["kind"], "batch_id": b.batch_id,
                     "task_id": tid, "task_file": str(_txt_path(root, tid)),
                     "chunk_file": str(Path(root) / b.chunk_path(tid)),
                     "answer_file": str(Path(root) / b.answer_path(tid)), "prompt_sha": b.prompt_sha,
                     "n_items": len(b.chunks[0]["items"])})
    return rows


def write_tasks(root: Path = ROOT) -> list:
    """After A38 only. Writes every chunk, prompt, key, manifest and <task_id>.txt, then TASKS.json (written once)."""
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the redo2 authoring tasks are written once")
    batches = build_batches(root)
    for td, b in batches:
        files = dict(b.files())
        files[_txt_path(root, b.chunks[0]["task_id"]).name] = author_txt(td, b, root)
        paths.write_files(root, files)
    idx = task_index(batches, root)
    paths.write_json(root / "TASKS.json", {
        "family": FAMILY, "seed": SEED, "stage": "redo2 (Stage A blockers B1, B2)", "prompt_sha": chunker.sha(PROMPT),
        "g0_sha256": hashlib.sha256((HERE / "G0_SPEC.md").read_bytes()).hexdigest(), "tasks": idx})
    return idx


# ------------------------------------------------------------------------------------------------ load and merge

def main_kept() -> dict:
    """The kept pools of haiku/author/ (linted.json), checked against the counts the 26 G-LEX reads were built from."""
    d = json.loads(MAIN_LINTED.read_text(encoding="utf-8"))
    want = json.loads(MAIN_TASKS.read_text(encoding="utf-8"))["summary"]["lint_counts"]
    got = {f"kept_{k}": len(v) for k, v in d["kept"].items()}
    bad = {k: (got.get(k), v) for k, v in want.items() if k.startswith("kept_") and got.get(k) != v}
    if bad:
        raise ValueError(f"haiku/author/linted.json differs from the counts the G-LEX reads were built from: {bad}")
    return d["kept"]


def merge(supp_kept: dict, supp_dropped: list, main: dict) -> tuple:
    """(supplement pieces that survive the merge, extra drops). The supplement adds support_chat skins and
    yn_dneg_beyond wordings only; a duplicate of a main piece, or a text under two meanings, is dropped."""
    seen = {(pool, A._norm(p["text"])) for pool, ps in main.items() if pool in ("skin", "wording") for p in ps}
    lex = {}
    for pool in LEX_POOLS:
        for p in main.get(pool, []):
            lex.setdefault(A._norm(K.PH_RE.sub("{X}", p["text"])), set()).add(p["sem"])
    kept, dropped = {}, []
    for pool, ps in supp_kept.items():
        for p in ps:
            why = []
            if pool == "skin" and p.get("register") != "support_chat":
                why.append("not a supplement register")
            elif pool == "wording":
                if p.get("qform") != "yn_dneg_beyond":
                    why.append("not a supplement question form")
                else:
                    why += lint_dneg(p["text"])
            elif pool not in ("skin", "wording"):
                why.append("not a supplement pool")
            if (pool, A._norm(p["text"])) in seen:
                why.append("duplicate of a kept piece in haiku/author")
            if pool == "wording":
                other = lex.get(A._norm(K.PH_RE.sub("{X}", p["text"])), set()) - {p["sem"]}
                if other:
                    why.append("the same text under two meanings")
            if why:
                dropped.append({**p, "why": why})
            else:
                kept.setdefault(pool, []).append(p)
    return kept, list(supp_dropped) + dropped


def merged_pools(main: dict, supp: dict) -> dict:
    out = {k: list(v) for k, v in main.items()}
    for pool, ps in supp.items():
        out.setdefault(pool, []).extend(ps)
    return out


def load(root: Path = ROOT, answers: dict | None = None, batches: list | None = None, main: dict | None = None) -> dict:
    rep = A.load(root, answers=answers, batches=batches)          # the unchanged family lint, redo2 provenance
    main = main_kept() if main is None else main
    kept, dropped = merge(rep["kept"], rep["dropped"], main)
    merged = merged_pools(main, kept)
    sc = {lay: sum(1 for p in merged.get("skin", []) if p["register"] == "support_chat" and p["layout"] == lay)
          for lay in ("L0", "L1", "L2")}
    train = [p for p in merged.get("skin", []) if not p["held_out"] and p["layout"] in ("L1", "L2")]
    share = {}
    for p in train:
        share[p["register"]] = share.get(p["register"], 0) + 1
    counts = {f"supp_kept_{k}": len(v) for k, v in sorted(kept.items())}
    counts.update({"supp_dropped": len(dropped), "support_chat_merged": sc,
                   "yn_dneg_beyond_merged": sum(1 for p in merged.get("wording", []) if p["qform"] == "yn_dneg_beyond"),
                   "max_register_share_of_training_L1_L2_skins":
                       round(max(share.values()) / len(train), 4) if train else None})
    return {"kept": kept, "dropped": dropped, "problems": rep["problems"], "counts": counts,
            "shortfall_merged": A.shortfall(merged)}


# ------------------------------------------------------------------------------------------------ supplement G-LEX

def supp_kept_from_disk(root: Path = ROOT) -> dict:
    return json.loads((Path(root) / "linted.json").read_text(encoding="utf-8"))["kept"]


def glex_plan(supp: dict | None = None, main: dict | None = None) -> dict:
    """The 2 supplement G-LEX reads: the kept yn_dneg_beyond wordings (recorded) plus seeded control wordings of the
    other question forms from the main pool (not recorded). Same closed list as the main question reads."""
    supp = supp_kept_from_disk() if supp is None else supp
    main = main_kept() if main is None else main
    tests = [p for p in supp.get("wording", []) if p["qform"] == "yn_dneg_beyond"]
    reg = A.registry({"wording": list(main.get("wording", [])) + tests})
    form_of = {reg.forms[f].text: f for f in reg.forms}
    test_ids = sorted(form_of[p["text"]] for p in tests if reg.forms[form_of[p["text"]]].unit_ok)
    unit_failed = sorted(form_of[p["text"]] for p in tests if not reg.forms[form_of[p["text"]]].unit_ok)
    controls = []
    for q, n in CONTROLS.items():
        pool = sorted((form_of[p["text"]] for p in main.get("wording", []) if p["qform"] == q),
                      key=lambda f: hashlib.sha256(f"{GLEX_SEED}|control|{f}".encode()).hexdigest())
        controls += pool[:n]
    if not test_ids:
        raise ValueError("no unit-tested yn_dneg_beyond wording to read")
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "question")
    batches = []
    for read in READS:
        seed = f"{GLEX_SEED}-{read}-question-00"
        order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
        items = [(fid, {"text": it["text"]}) for fid, it in A.lex_items(reg, test_ids + sorted(controls), seed=seed)]
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=G.group_prompt(order),
                               max_items=G.GROUP)
        if len(b.chunks) != 1:
            raise chunker.ChunkError(f"{seed}: one chunk per read")
        batches.append((read, b))
    return {"reg": reg, "tests": test_ids, "controls": sorted(controls), "unit_failed": unit_failed,
            "batches": batches}


def glex_txt(b, root: Path = GLEX_ROOT) -> str:
    """The self-contained G-LEX read file (the redo pattern: prompt, closed list and items inline)."""
    c = b.chunks[0]
    tid, n = c["task_id"], len(c["items"])
    txt, ans = str(_txt_path(root, tid)), str(Path(root) / b.answer_path(tid))
    lines = [
        "T27 MEANING-NAMING TASK (REDO2)  --  THIS ONE FILE IS YOUR COMPLETE TASK", _RULE,
        "Read this top section first. It is complete: it holds your instructions, the exact answer format, a worked",
        "example, the closed list of meanings and all items. You need nothing else and you must not open anything else.",
        "", f"TASK ID : {tid}", "KIND    : question  (questions an assistant might be asked about content it opened and "
        "the user's task)", f"ITEMS   : {n}", f"TASK FILE (this file)  : {txt}", f"ANSWER FILE (write here): {ans}", "",
        "FILE RULES",
        "- Open only this file. Do not open, list or search any other file or folder (no earlier answers, chunks,",
        "  prompts, keys or manifests).",
        f"- Create exactly one file, {ans}, with the Write tool, holding the finished JSON object. Write no",
        "  notes, drafts or other files. Do not put the answer in chat; when the file is written reply with the single",
        "  word DONE.", "",
        "WHAT TO DO",
        f"1. The section ITEMS (at the end) lists {n} items, one JSON object per line. Each has an opaque \"qid\" and a",
        "   \"text\" (one line of English). The qid is only a label; do not try to read anything into it.",
        "2. The section THE TASK PROMPT AND THE CLOSED LIST (below) holds a list of meanings, one per line, each line",
        "   starting with \"- \". That is the closed list for this task.",
        "3. For every item, read its text and pick the ONE meaning in the closed list that the text expresses. Judge each",
        "   text on its own words, not on the other items and not on the order of the list. Read negations carefully.",
        "4. Copy the chosen meaning exactly, character for character (the text after \"- \", without the dash).",
        "   Never shorten, reword, translate, merge two meanings, or invent a meaning. Never leave an item out.", "",
        "EXACT ANSWER CONTRACT",
        "The answer file holds ONE JSON object and nothing else. It is a flat map, qid to meaning:",
        f"- Keys: the \"qid\" value of EVERY one of the {n} items, each exactly once. So the object has exactly {n} keys.",
        "  There are no other field names: no \"task_id\", \"kind\", \"items\", \"answers\", \"schema\", \"note\", \"status\",",
        "  \"prompt_sha\", \"format_note\" or any similar key.",
        "- Value of each key: ONE JSON string that is identical to one line of the closed list (without the leading \"- \").",
        "- Not allowed: a JSON list at the top level; a wrapper object around the map; values that are objects, lists,",
        "  null, numbers or letters; a free description of the text; a comment or reason; an empty or missing value.",
        "- Valid JSON only: double quotes, no comments, no trailing commas, no text before or after the object.", "",
        "LITERAL EXAMPLE (toy data, NOT your items or your list)",
        "  Toy closed list:", "  - asks whether the sky is grey", "  - asks whether it is false that the sky is grey",
        "  Toy items:", "  {\"qid\": \"q0example01\", \"text\": \"Is the sky grey today?\"}",
        "  {\"qid\": \"q0example02\", \"text\": \"Is the claim that the sky is grey not true?\"}",
        "  CORRECT answer file content (this and nothing else):", "  {",
        "    \"q0example01\": \"asks whether the sky is grey\",",
        "    \"q0example02\": \"asks whether it is false that the sky is grey\"", "  }",
        "  WRONG (rejected by the checker):", "  {\"items\": [{\"qid\": \"q0example01\", \"meaning\": \"sky\"}]}",
        "  [{\"qid\": \"q0example01\", \"answer\": \"...\"}]",
        "  {\"q0example01\": \"grey sky\"}      (value is not a line of the list)", "",
        "SELF-CHECK before you finish (do it, then write the file once)",
        f"- Count: the object has exactly {n} keys and every qid of the ITEMS section appears once.",
        "- Every value is copied verbatim from a line of the closed list, with no leading dash and no changes.",
        "- The file is one JSON object, with no extra keys, comments or text around it.", "", _RULE,
        f"THE TASK PROMPT AND THE CLOSED LIST  (verbatim from the built prompt file, sha256 {b.prompt_sha};",
        "in this prompt \"your task file\" means THIS file and \"the answer file\" means the ANSWER FILE path above)",
        _RULE, b.prompt.rstrip("\n"), "", _RULE, f"ITEMS  ({n} items, one JSON object per line, in this order)", _RULE]
    lines += [json.dumps({"qid": it["qid"], "text": it["text"]}, ensure_ascii=False) for it in c["items"]]
    lines += ["", _RULE, f"END OF TASK FILE. Now write {ans}"]
    return "\n".join(lines) + "\n"


def glex_write(root: Path = GLEX_ROOT) -> list:
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the redo2 G-LEX reads are written once")
    p = glex_plan()
    tasks = []
    for read, b in p["batches"]:
        tid = b.chunks[0]["task_id"]
        files = dict(b.files())
        files[_txt_path(root, tid).name] = glex_txt(b, root)
        paths.write_files(root, files)
        tasks.append({"read": read, "kind": "question", "batch_id": b.batch_id, "task_id": tid,
                      "task_file": str(_txt_path(root, tid)), "answer_file": str(root / b.answer_path(tid)),
                      "n_items": len(b.key), "prompt_sha": b.prompt_sha})
    reg = p["reg"]
    paths.write_json(root / "TASKS.json", {
        "family": FAMILY, "gate": "G-LEX 2/2 (supplement: yn_dneg_beyond wordings)", "reads": list(READS),
        "tasks": tasks, "test_forms": {f: reg.forms[f].sem_id for f in p["tests"]},
        "control_forms": {f: reg.forms[f].sem_id for f in p["controls"]}, "unit_failed": p["unit_failed"],
        "rule": "only test forms are recorded; controls are report-only (they are admitted by the 26 main reads)"})
    return tasks


def glex_check(root: Path = GLEX_ROOT, p: dict | None = None) -> dict:
    """Judge the 2 supplement reads (extract_check.judge: a malformed or missing read is never recorded), record the
    valid reads for the test forms only, and report admission and control agreement."""
    root = Path(root)
    p = glex_plan() if p is None else p
    reg = p["reg"]
    tests = set(p["tests"])
    file_probs, rows = [], []
    for read, b in p["batches"]:
        for rel, text in sorted(dict(b.files(), **{_txt_path(root, b.chunks[0]["task_id"]).name: glex_txt(b, root)})
                                .items()):
            f = root / rel
            if not f.is_file() or f.read_text(encoding="utf-8") != text:
                file_probs.append(f"{b.batch_id}: {rel} differs from the rebuilt file")
        tid = b.chunks[0]["task_id"]
        path = root / b.answer_path(tid)
        got, raw = {}, None
        if not path.is_file():
            st, why = "missing", ["no answer file"]
        else:
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                st, why = "malformed", [f"not valid JSON ({type(e).__name__})"]
            else:
                st, why, got = E.judge(b, E.closed_list(reg, "question"), raw)
        ctrl_ok = ctrl_n = 0
        if st == "valid":
            for fid, meaning in sorted(got.items()):
                sem = reg.meaning_to_sem("question", meaning)
                if fid in tests:
                    reg.record_extraction(fid, f"redo2-{read}:{tid}", sem)
                else:
                    ctrl_n += 1
                    ctrl_ok += sem == reg.forms[fid].sem_id
        rows.append({"read": read, "task_id": tid, "status": st, "reasons": why, "n_items": len(b.key),
                     "controls_agree": f"{ctrl_ok}/{ctrl_n}" if st == "valid" else None,
                     "answer_sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None})
    status = {f: reg.status(f) for f in sorted(tests)}
    admitted = sorted(f for f, s in status.items() if s == "admitted")
    ok = not file_probs and all(r["status"] == "valid" for r in rows)
    return {"family": FAMILY, "gate": "G-LEX 2/2 (supplement)", "file_problems": file_probs, "tasks": rows,
            "forms": status, "admitted": admitted, "unit_failed": p["unit_failed"],
            "minimum_yn_dneg_beyond": A.MINIMUM["wording_dneg"],
            "status": ("COMPLETE: both reads valid; " if ok else "INCOMPLETE: ")
            + f"{len(admitted)}/{len(tests)} yn_dneg_beyond wordings admitted (minimum {A.MINIMUM['wording_dneg']})",
            "no_labels_set": True, "no_rows_generated": True}


def record_into(reg) -> list:
    """For the family freeze: record the valid supplement reads into `reg` (a registry that already holds the
    supplement wordings, e.g. authoring.registry(main kept + supplement kept)). Returns the recorded form ids."""
    rep = glex_check()
    if rep["file_problems"]:
        raise ValueError(f"supplement G-LEX files differ from the rebuild: {rep['file_problems'][:2]}")
    p = glex_plan()
    out = []
    for read, b in p["batches"]:
        tid = b.chunks[0]["task_id"]
        path = GLEX_ROOT / b.answer_path(tid)
        if not path.is_file():
            continue
        st, _why, got = E.judge(b, E.closed_list(p["reg"], "question"), json.loads(path.read_text(encoding="utf-8")))
        if st != "valid":
            continue
        for fid, meaning in sorted(got.items()):
            if fid in set(p["tests"]):
                reg.record_extraction(fid, f"redo2-{read}:{tid}", reg.meaning_to_sem("question", meaning))
                out.append(fid)
    return out


# ------------------------------------------------------------------------------------------------ CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="families.T27.redo2")
    ap.add_argument("cmd", choices=("tasks", "write", "load", "glex-plan", "glex-write", "glex-check"))
    ap.add_argument("--write", action="store_true", help="load: also write haiku/redo2/linted.json")
    ap.add_argument("--record", action="store_true", help="glex-check: also write the validation record")
    a = ap.parse_args(argv)
    if a.cmd == "tasks":
        print(json.dumps(task_index(build_batches(ROOT), ROOT), indent=1))
    elif a.cmd == "write":
        print(json.dumps([{"task_file": t["task_file"], "answer_file": t["answer_file"], "kind": t["kind"]}
                          for t in write_tasks(ROOT)], indent=1))
    elif a.cmd == "load":
        rep = load(ROOT)
        print(json.dumps({"counts": rep["counts"], "problems": rep["problems"],
                          "shortfall_merged": rep["shortfall_merged"],
                          "drop_reasons": A._reason_counts(rep["dropped"])}, indent=1))
        if a.write:
            paths.write_json(ROOT / "linted.json", {
                "family": FAMILY, "stage": "redo2", "kept": rep["kept"], "dropped": rep["dropped"],
                "counts": rep["counts"], "shortfall_merged": rep["shortfall_merged"],
                "main_linted_sha256": hashlib.sha256(MAIN_LINTED.read_bytes()).hexdigest()})
    elif a.cmd == "glex-plan":
        p = glex_plan()
        print(json.dumps({"tests": len(p["tests"]), "controls": len(p["controls"]), "unit_failed": p["unit_failed"],
                          "reads": [{"read": r, "task_id": b.chunks[0]["task_id"], "n_items": len(b.key)}
                                    for r, b in p["batches"]]}, indent=1))
    elif a.cmd == "glex-write":
        print(json.dumps([{"task_file": t["task_file"], "answer_file": t["answer_file"], "kind": "extract_lex",
                           "read": t["read"], "n_items": t["n_items"]} for t in glex_write(GLEX_ROOT)], indent=1))
    else:
        rep = glex_check()
        if a.record:
            paths.write_json(GLEX_ROOT / "record" / "VALIDATION.json", rep)
        print(json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
