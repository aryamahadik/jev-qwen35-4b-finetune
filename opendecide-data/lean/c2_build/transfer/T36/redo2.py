"""transfer/T36/redo2.py: T36 redo round 2 for the pool blockers (G0_SPEC.md v2.1 sections 6 and 7, ruling v2.1;
C2_DATA_SPEC 6.2, 6.3; PREREG A37 (b), A38). Haiku writes text only and reads only to flag; nothing here sets a label.

R1  Mode F. Round 1 briefs (authoring.freeform_prompt) never asked a document to say that PERSON maintains PROJECT, so
    the G3-H read (field "the person who maintains the project", unchanged) returned person NONE on 33 of 34
    documents. The 41 Mode F items without a frozen document are re-authored here with the maintainer statement
    (G0 v2.1 section 6), 2 candidates per item. After the answers: one G3-H read of every lint-clean candidate with
    extract.G3H_PROMPT and extract.g3h_fields() as frozen (same prompt sha as round 1).
R2  Mode T. The items of haiku/redo/ whose redo text still fails the authoring lint, 3 candidates per item. The task
    text says "external packages" (never "third-party": "third" is a number word for the lint) and describes the
    label words by function (they never appear in an authoring task, as chunker.make_batch requires).
Selection (G0 v2.1 section 6): per item, the first candidate in written order that passes every check is kept, the
rest are discarded; at most one piece per item, so no register count exceeds its target. No gate is loosened: the
checks are authoring.load_pools' lint, extract.extra_lint, freeze.slot_problems, dedup and (Mode F) G3-H at 98%.

Items keep their round 1 qids, so haiku/author/key/ still maps them to internal ids. authoring.py, extract.py,
freeze.py, haiku/author/, haiku/extract/, haiku/redo/ and pools/ are read only. Every write goes through
paths.write_files (refuses before A38 and on never-open paths).

  python -m transfer.T36.redo2 tasks           in memory: build and check the authoring task files
  python -m transfer.T36.redo2 write           write haiku/redo2/<task>.md, REDO2_INDEX.json, answers/README.txt
  python -m transfer.T36.redo2 load            in memory: lint the returned candidates, keep the first passing one per
                                               item, report the merged counts against freeze.TARGETS
  python -m transfer.T36.redo2 g3h [--write]   the G3-H read of the lint-clean Mode F candidates (haiku/redo2/extract/)
  python -m transfer.T36.redo2 g3h-check       G3-H compare, first passing candidate per item, Mode F counts and cap
  (run from lean/c2_build with ../../.venv/bin/python)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T36 import authoring as A  # noqa: E402
from transfer.T36 import extract as E  # noqa: E402
from transfer.T36 import freeze as F  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
VERSION = "redo2-v1"
AUTHOR = HERE / "haiku" / "author"
REDO = HERE / "haiku" / "redo"
ROOT = HERE / "haiku" / "redo2"
G3H_ROOT = ROOT / "extract"
POOLS = HERE / "pools"
N_CAND = {"author_skin": 3, "author_freeform": 2}
MODE_T = ("skin", "skin_heldout")
MODE_F = ("freeform", "freeform_heldout")
LABEL_FORMS = frozenset(gsl._label_forms(tuple(P.T36Plugin.LABEL_WORDS)))
NUMBER_WORDS = ", ".join(sorted(gsl.CORE["number"]))


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _norm(s) -> str:
    return " ".join(str(s).casefold().split())


# ------------------------------------------------------------------------------------------------ task text

INTRO = ("You are writing short text pieces for a test set about software projects and the external packages they "
         "depend on. Invent everything: never copy text from real projects, packages, companies, people or websites. "
         "Write in English. Make every text clearly different from every other text in this file (structure, "
         "opening, length, word choice). Each item below has a qid and the details of what to write; the answer is "
         "one object per item as in the contract above.")

RESERVED = [  # the family's label words, by function only (G0 R20; chunker refuses them in an authoring task)
    "words that judge whether something agrees with, suits, corresponds to or is admitted by a requirement, a rule "
    "or a limit, and words for being able to work together with something or for backing it",
    "the everyday verb and noun for getting together with people (a get-together of the team): they are spelled "
    "like a reserved word, so write \"sync\", \"call\", \"catch-up\", \"planning session\" or \"review session\"",
    "place words for being in the interior of something, in a region bounded by a limit, or beyond its edge: write "
    "plain position words such as \"in\", \"at\", \"for\", \"across\", \"around\", \"near\"",
    "words about letting something into a group or keeping it out of one",
    "words about putting software onto a machine, and words for settling a question (write \"look into\", \"work "
    "through\", \"go over\")",
    "comparison words for height, rank or age: the -er and -est forms of high, low, new and old, and the -est form of "
    "late",
    "words about how steady software is, about changes that harm its users, about moving software to a different "
    "level, and the names of early test stages of software",
]


def _reserved_block() -> str:
    return "\n".join(f"  - {r};" if i < len(RESERVED) - 1 else f"  - {r}." for i, r in enumerate(RESERVED))


def _contract(name: str, kind: str, answer_file: str, qids: list, k: int) -> str:
    ex = ", ".join(f'"<text {c}>"' for c in "ABC"[:k])
    return "\n".join([
        f"# Haiku REDO-2 task {name} (family {FAMILY}, kind {kind}): {len(qids)} item(s), {k} candidate texts each",
        "",
        "Read this whole file. Do not open, list, search or write any other file. When you are done, write your answer "
        "with the Write tool to exactly this path (nothing else, no other file):",
        "",
        f"    {answer_file}",
        "",
        "## Answer contract (exact)",
        "",
        f"The answer file holds ONE JSON array with exactly {len(qids)} object(s), one per item below, every qid exactly "
        "once (any order). Each object has exactly two keys: \"qid\" (the item's qid, copied exactly) and \"texts\" (a "
        f"list of exactly {k} different strings: {k} alternative texts for that item, each complete on its own and each "
        "following every rule below; write \\n for a line break and \\\" for a double quote in a string).",
        "Valid JSON only: no text before or after the array, no comments, no code fence, no other keys. Every item "
        "answered once.",
        "",
        "Literal example of the required shape:",
        "",
        "[",
        f'  {{"qid": "{qids[0]}", "texts": [{ex}]}},',
        "  ...",
        "]",
        "",
        "How the texts are used: a program checks each text against the rules below in the order you wrote them and "
        "keeps the first text that passes every check; the others are thrown away. So every text must follow every "
        "rule, and the texts of one item must be clearly different from each other.",
    ])


def _items_block(items: list) -> str:
    rows = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    return "\n".join([f"## Items ({len(items)}; one JSON object per line)", "", "```json", "[", rows, "]", "```"])


def _replace(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ValueError(f"source prompt changed: {old[:50]!r} not found")
    return text.replace(old, new)


def _styles(registers) -> str:
    return "Register styles: " + " | ".join(
        f"{r}: {A.REGISTER_STYLE[r].replace('third-party', 'external')}" for r in registers)


def _banned_lists() -> str:
    """authoring._banned_lists() minus every inflected label word ("resolved", "excluding"): those stay banned through
    the reserved-word kinds of the redo note, and a task text never names a label word in any form."""
    out = []
    for line in A._banned_lists().split("\n"):
        head, sep, words = line.partition(": ")
        if sep and line.startswith("   - ") and not head.endswith("phrases"):
            line = head + sep + ", ".join(w for w in words.split(", ") if w.lower() not in LABEL_FORMS)
        out.append(line)
    return "\n".join(out)


def skin_instructions(registers, k: int) -> str:
    body = "TASK: " + A.skin_prompt(registers).split("\n\nTASK: ", 1)[1]
    body = _replace(body, A._banned_lists(), _banned_lists())
    body = _replace(body, "for each item write ONE short narrative text in the item's register",
                    f"for each item write {k} alternative short narrative texts in the item's register")
    body = re.sub(r"^Register styles: .*$", lambda _m: _styles(registers), body, count=1, flags=re.M)
    return INTRO + "\n\n" + body


SKIN_NOTE = "\n".join([
    "REDO NOTE (added for this second redo; every rule above still holds). Earlier texts for each item below were "
    "thrown away by the program's word check. Write completely new texts. Causes to avoid:",
    "- A missing placeholder: a text that said \"the package\" and left out {PKG}. Each text holds {PERSON}, {PROJECT} "
    "and {PKG}, each exactly once, copied with braces; count them in every text before you write the file.",
    "- Reserved words. The check throws away a text that uses any of these kinds of words, in any form (with -s, -ed, "
    "-ing and the like):",
    "@RESERVED@",
    "- The word \"third\" in any form, also as part of \"third-party\" (write \"external package\" or \"imported "
    "package\"; the check reads every part of a hyphenated word), and every other word in the lists of hard rule 2; "
    "\"can\" and \"much\" slipped in earlier. Re-read every text word by word against those lists.",
    "- Any word about setting up, choosing, picking or swapping software, or about how new a package is.",
    "The scene is only who is looking at what in the project, and why: plain words such as \"looking at\", "
    "\"reviewing\", \"checking\", \"going over\", \"notes on\", \"handing over\", \"keeping track of\".",
    "Before you write the file, check each text: {PERSON}, {PROJECT} and {PKG} each exactly once; no \"a\" or \"an\" "
    "right before a placeholder; no digit; no word from the lists; no negation; no reserved word.",
]).replace("@RESERVED@", _reserved_block())


def freeform_instructions(registers, k: int) -> str:
    body = "TASK: " + A.freeform_prompt(registers).split("\n\nTASK: ", 1)[1]
    body = _replace(body, "for each item write ONE short free-form document in the item's register",
                    f"for each item write {k} alternative short free-form documents in the item's register")
    body = _replace(body, "a third-party package", "an external package")
    body = re.sub(r"^Register styles: .*$", lambda _m: _styles(registers), body, count=1, flags=re.M)
    tail = ("Every other person is unnamed (a colleague, the team, a reviewer). Refer to the package only as \"the "
            "package\", \"the library\" or \"this dependency\", never by a name.")
    body = _replace(body, tail, tail[:tail.index(" Refer")].rstrip(".") + ", and nobody else maintains the project "
                    "or is called a maintainer." + tail[tail.index(" Refer"):] + "\nMaintainer statement (required): "
                    "each document says in plain words that PERSON maintains PROJECT, with both values written in "
                    "full, exactly as given, as part of that statement (shapes in the redo note).")
    body = _replace(body, "no number words (one, two, first, second, half, twice, dozen ...)",
                    f"no number words ({NUMBER_WORDS}; also as part of a hyphenated word)")
    body = _replace(body, "Follow each item's angle for variety. Before writing, check every document: both fact "
                          "values appear verbatim; no digit; no negation.",
                    "5. Capital letters only at the start of a sentence, a line, a list item or a label, in the "
                    "two fact values, and for CI, PR, QA and API.\n"
                    "6. None of the reserved words in the redo note below.\n"
                    "Follow each item's form for variety. Before writing, check every document: the maintainer "
                    "statement is there; both fact values appear verbatim; no digit; no number word; no negation; "
                    "no reserved word.")
    return INTRO + "\n\n" + body


FREEFORM_NOTE = "\n".join([
    "REDO NOTE (added for this second redo; every rule above still holds). Earlier documents for these items were "
    "thrown away. Avoid each cause:",
    "A. The maintainer statement was missing (nearly every item). A later reader is asked who maintains the project "
    "and copies that name only when the document says so in words. So each document contains one plain statement "
    "that PERSON maintains PROJECT, with both values written in full in that statement. Shapes that work (put the item's own "
    "values where <PERSON> and <PROJECT> stand): \"<PERSON>, who maintains <PROJECT>, ...\"; \"<PROJECT> is "
    "maintained by <PERSON>.\"; \"<PERSON>, the maintainer of <PROJECT>, ...\"; \"As maintainer of <PROJECT>, "
    "<PERSON> ...\"; in a log line \"project=<PROJECT> maintainer=<PERSON>\"; in a ticket a \"Project: <PROJECT>\" "
    "line and a \"Maintainer: <PERSON>\" line. A document that says only that PERSON asked for, opened, owns, leads, "
    "signed, thanked or was assigned the review is thrown away. Nobody else in the document maintains the project or "
    "is called a maintainer; every other person stays unnamed. Vary where the statement sits and how it is phrased.",
    "B. A number word, above all \"third\" in \"third-party\" (write \"external package\" or \"imported "
    "package\"), and words such as \"one\" (also in \"no one\"), \"first\" and \"second\" (as in a first look or a "
    "second pair of eyes) and \"half\". The check reads every part of a hyphenated word.",
    "C. Reserved words. The check throws away a document that uses any of these kinds of words, in any form (with "
    "-s, -ed, -ing and the like):",
    "@RESERVED@",
    "Before you write the file, read each document once more against hard rules 1-6 and this note.",
]).replace("@RESERVED@", _reserved_block())

FORM_FIX = {"a note handed from one teammate to another": "a hand-over note from a teammate to a colleague"}


def _skin_item(it: dict, k: int) -> dict:
    out = dict(it)
    out["brief"] = _replace(it["brief"], "Write one text.", f"Write {k} alternative texts.")
    return out


def _freeform_item(it: dict, k: int) -> dict:
    out = dict(it)
    brief = it["brief"]
    for old, new in FORM_FIX.items():
        brief = brief.replace(old, new)
    out["brief"] = _replace(brief, "Write one document.", f"Write {k} alternative documents.")
    out["rules"] = list(it["rules"]) + ["say in plain words that PERSON maintains PROJECT (redo note A)"]
    return out


def task_problems(text: str) -> list:
    """An authoring task never names a label word (any inflection) or a family question string (A37 b)."""
    out = sorted({t for t in re.findall(r"[A-Za-z]+", text) if t.lower() in LABEL_FORMS})
    probs = [f"label word {w!r}" for w in out]
    low = text.lower()
    for q in A.QUESTION_STRINGS:
        if q and re.search(r"(?<![a-z0-9])" + re.escape(q.lower()) + r"(?![a-z0-9])", low):
            probs.append(f"question string {q[:40]!r}")
    return probs


# ------------------------------------------------------------------------------------------------ sources

def _batches() -> dict:
    """{source task id: (pool, TaskBatch, chunk)} for every round 1 authoring chunk (authoring.build, deterministic)."""
    out = {}
    for pool, b, _f in A.build():
        for c in b.chunks:
            out[c["task_id"]] = (pool, b, c)
    return out


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def lint_piece(pool: str, it: dict, text: str, tid: str = "", psha: str = "") -> tuple:
    """(piece or None, reasons) with every check a piece of its pool meets before freeze (authoring.load_pools,
    extract.extra_lint, freeze.slot_problems). Dedup is the caller's (it needs the other pools)."""
    plugin = P.T36Plugin()
    text = str(text or "").strip()
    reasons, piece = [], None
    try:
        if not text:
            raise ValueError("empty text")
        sid = f"T36-{pool}-redo2-{_sha(text)[:12]}"
        if pool in MODE_T:
            piece = make_skin(sid, FAMILY, text, dict(A.NARR), register=it["register"],
                              held_out=(pool == "skin_heldout"), haiku_task_id=tid, haiku_prompt_sha=psha)
            reasons = [f"{v.rule}: {v.detail}" for v in
                       gsl.lint_template(piece, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                         name_allow=plugin.NAME_ALLOW)]
            reasons += [f"slots: {x}" for x in F.slot_problems(piece)]
        elif pool in MODE_F:
            facts = dict(it["facts"])
            piece = make_skin(sid, FAMILY, text, {"PERSON": "name", "PROJECT": "name"}, register=it["register"],
                              held_out=(pool == "freeform_heldout"), author_mode="F", brief=facts,
                              haiku_task_id=tid, haiku_prompt_sha=psha)
            reasons = [f"{v.rule}: {v.detail}" for v in gsl.lint_freeform(text, facts, label_words=plugin.LABEL_WORDS)]
            reasons += E.mode_f_problems(piece)
        else:
            raise ValueError(f"pool {pool} is not redone here")
        if "\n\n" in text:
            reasons.append("blank line")
    except Exception as e:                                   # noqa: BLE001  (a malformed text drops the candidate)
        reasons = reasons + [f"unusable: {e}"]
    return (None if reasons else piece), reasons


def frozen_texts() -> set:
    """Normalised texts of every frozen piece (skins, attack lines, documents): a new text must differ from each."""
    out = set()
    for f in ("skins.json", "attacks.json", "documents.json"):
        out |= {_norm(d["text"]) for d in _read_json(POOLS / f)}
    return out


def plan() -> list:
    """[(source task id, pool, kind, held_out, [(qid, item, prior reasons)])]: the items redone in this round."""
    src = _batches()
    plan_ = []
    # R2: Mode T items whose haiku/redo text still fails
    redo_index = _read_json(REDO / "REDO_INDEX.json")
    first = {}
    for pool, iid, reasons in A.load_pools()["dropped"]:
        first[iid] = reasons
    for t in redo_index["tasks"]:
        pool, b, c = src[t["source_task_id"]]
        ans_file = Path(t["answer_file"])
        ans = {a["qid"]: a.get("text", "") for a in _read_json(ans_file)} if ans_file.exists() else {}
        its = {it["qid"]: it for it in c["items"]}
        todo = []
        for q in t["qids"]:
            _p, r = lint_piece(pool, its[q], ans.get(q, ""))
            if r:
                todo.append((q, its[q], {"round1": first.get(b.key[q], []), "redo": r}))
        if todo:
            plan_.append((t["source_task_id"], pool, "author_skin", pool == "skin_heldout", todo))
    # R1: Mode F items without a frozen document
    frozen_docs = {d["text"] for d in _read_json(POOLS / "documents.json")}
    quar = {q["pid"]: q["diffs"] for q in _read_json(POOLS / "quarantine.json")["g3h_failed_documents"]}
    for tid in sorted(src):
        pool, b, c = src[tid]
        if pool not in MODE_F:
            continue
        f = AUTHOR / b.answer_path(tid)
        ans = {a["qid"]: str(a.get("text", "")).strip() for a in _read_json(f)} if f.exists() else {}
        todo = []
        for it in c["items"]:
            text = ans.get(it["qid"], "")
            if text in frozen_docs:
                continue
            why = first.get(b.key[it["qid"]]) or quar.get(f"{pool}|{_sha(text)[:16]}") or ["no frozen document"]
            todo.append((it["qid"], it, {"round1": why}))
        if todo:
            plan_.append((tid, pool, "author_freeform", pool == "freeform_heldout", todo))
    return plan_


# ------------------------------------------------------------------------------------------------ build

def build() -> list:
    """[task dict] with the full task text; every check that guards an authoring task (A37 b) has run."""
    src = _batches()
    tasks = []
    for tid, pool, kind, held, todo in plan():
        _pool, b, c = src[tid]
        k = N_CAND[kind]
        qids = [q for q, _it, _r in todo]
        regs = sorted({it["register"] for _q, it, _r in todo})
        answer = str(ROOT / "answers" / f"{tid}.json")
        task_file = str(ROOT / f"{tid}.md")
        if kind == "author_skin":
            items = [_skin_item(it, k) for _q, it, _r in todo]
            instr, note = skin_instructions(regs, k), SKIN_NOTE
        else:
            items = [_freeform_item(it, k) for _q, it, _r in todo]
            instr, note = freeform_instructions(regs, k), FREEFORM_NOTE
        for (q, it, _r), new in zip(todo, items):
            assert new["qid"] == q and new.get("facts") == it.get("facts") and new["register"] == it["register"]
        text = "\n".join([_contract(tid, kind, answer, qids, k), "", "## Instructions", "", instr, "",
                          "## Redo note", "", note, "", _items_block(items), ""])
        probs = task_problems(text)
        for p in (answer, task_file):
            if never_open(p):
                probs.append(f"never-open path {p}")
        if any(iid in text for iid in b.key.values()):
            probs.append("names an internal id")
        if re.search(r"third-party", instr + note.replace('"third-party"', "")):
            probs.append("third-party in the task text")
        if probs:
            raise chunker.ChunkError(f"{tid}: {probs}")
        tasks.append({"name": tid, "kind": "author", "author_kind": kind, "pool": pool, "held_out": held,
                      "batch_id": b.batch_id, "source_task_id": tid, "source_prompt_sha256": b.prompt_sha,
                      "task_file": task_file, "answer_file": answer, "n_items": len(qids), "n_candidates": k,
                      "outputs_expected": len(qids) * k, "qids": qids, "registers": regs,
                      "prior_reasons": {q: r for q, _it, r in todo}, "instructions_sha256": _sha(text),
                      "audit_allowed_read": [task_file], "audit_allowed_write": [answer], "text": text})
    return tasks


def index(tasks: list) -> dict:
    return {
        "family": FAMILY, "version": VERSION, "g0_sha256": P.POOL_G0_SHA256,
        "ruling": "G0_SPEC.md v2.1, sections 6 and 7 (ruling v2.1)",
        "n_tasks": len(tasks), "by_kind": dict(Counter(t["author_kind"] for t in tasks)),
        "items": sum(t["n_items"] for t in tasks), "outputs_expected": sum(t["outputs_expected"] for t in tasks),
        "contract": "one JSON array; per item {\"qid\", \"texts\": [n_candidates different strings]}",
        "selection": "per item, the first candidate in written order that passes every check of its pool is kept "
                     "(authoring.load_pools lint, extract.extra_lint, freeze.slot_problems, normalised dedup against "
                     "the frozen pools and the pieces kept before it; Mode F also its G3-H read at the frozen prompt); "
                     "the rest are discarded; at most one piece per item",
        "keys": "items keep their round 1 qids: haiku/author/key/<batch_id>.json maps them to internal ids",
        "follow_up": ["load: python -m transfer.T36.redo2 load (in memory)",
                      "Mode F: python -m transfer.T36.redo2 g3h --write (G3-H read of the lint-clean candidates, "
                      "extract.G3H_PROMPT unchanged), then g3h-check",
                      "merge: freeze.py reads haiku/author/ and haiku/extract/ only; the admit step must add the kept "
                      "redo and redo2 pieces before the pools are frozen again"],
        "untouched": "haiku/author/, haiku/extract/, haiku/redo/ and pools/ are read only; nothing is converted or "
                     "merged here",
        "tasks": [{k: v for k, v in t.items() if k != "text"} for t in tasks],
    }


README = ("T36 redo2 answers: one <task name>.json per redo2 task (see ../REDO2_INDEX.json), each a JSON array of "
          "{\"qid\", \"texts\": [...]}. Written only by the redo2 task agents. Nothing here is converted or merged.\n")


def files(tasks: list) -> dict:
    out = {f"{t['name']}.md": t["text"] for t in tasks}
    out["REDO2_INDEX.json"] = json.dumps(index(tasks), ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = README
    return out


def write(tasks: list) -> list:
    fs = files(tasks)
    clash = [rel for rel, text in fs.items()
             if (ROOT / rel).exists() and (ROOT / rel).read_text(encoding="utf-8") != text]
    if clash:
        raise SystemExit(f"redo2 files already exist with other content (written once): {clash}")
    return [str(p) for p in paths.write_files(ROOT, fs)]


# ------------------------------------------------------------------------------------------------ load

def read_candidates(task: dict) -> tuple:
    """({qid: [texts]}, problems) from one redo2 answer file."""
    f = Path(task["answer_file"])
    if not f.exists():
        return {}, [f"{task['name']}: no answer file"]
    try:
        raw = _read_json(f)
    except json.JSONDecodeError as e:
        return {}, [f"{task['name']}: answer file is not JSON ({e})"]
    out, probs = {}, []
    if not isinstance(raw, list):
        return {}, [f"{task['name']}: the answer is not a JSON array"]
    for a in raw:
        q = a.get("qid") if isinstance(a, dict) else None
        if q not in task["qids"]:
            probs.append(f"{task['name']}: unknown qid {q!r}")
        elif q in out:
            probs.append(f"{task['name']}: qid {q} answered twice")
        elif not isinstance(a.get("texts"), list) or not all(isinstance(t, str) for t in a["texts"]):
            probs.append(f"{task['name']}: {q} has no list of texts")
            out[q] = []
        else:
            if len(a["texts"]) != task["n_candidates"]:
                probs.append(f"{task['name']}: {q} has {len(a['texts'])} texts, want {task['n_candidates']}")
            out[q] = list(a["texts"])[:task["n_candidates"]]
    missing = sorted(set(task["qids"]) - set(out))
    if missing:
        probs.append(f"{task['name']}: {len(missing)} qid(s) unanswered")
    return out, probs


def _kept_redo_skins(src: dict) -> list:
    """[(pool, register, text)] for the haiku/redo texts that pass the lint (the 22 of 24 in the redo round)."""
    out = []
    for t in _read_json(REDO / "REDO_INDEX.json")["tasks"]:
        pool, _b, c = src[t["source_task_id"]]
        f = Path(t["answer_file"])
        if not f.exists():
            continue
        its = {it["qid"]: it for it in c["items"]}
        for a in _read_json(f):
            q = a.get("qid")
            if q in its:
                piece, r = lint_piece(pool, its[q], a.get("text", ""))
                if not r:
                    out.append((pool, its[q]["register"], piece.text))
    return out


def select(tasks: list, seen: set) -> dict:
    """Per item: the lint-checked candidates in written order and the first that passes (dedup against `seen`, which
    grows). Mode F candidates also need their G3-H read (g3h-check)."""
    src = _batches()
    out = {"items": [], "problems": []}
    for t in tasks:
        _pool, b, c = src[t["source_task_id"]]
        its = {it["qid"]: it for it in c["items"]}
        cands, probs = read_candidates(t)
        out["problems"] += probs
        for q in t["qids"]:
            row = {"task": t["name"], "pool": t["pool"], "qid": q, "iid": b.key[q], "register": its[q]["register"],
                   "held_out": t["held_out"], "candidates": [], "kept": None}
            for j, text in enumerate(cands.get(q, [])):
                piece, r = lint_piece(t["pool"], its[q], text, t["name"], _sha(t["text"]) if "text" in t else "")
                if not r and _norm(piece.text) in seen:
                    r = ["duplicate of a frozen or kept text"]
                row["candidates"].append({"j": j, "ok": not r, "reasons": r,
                                          "text": piece.text if piece else str(text).strip()})
                if not r and t["pool"] in MODE_T and row["kept"] is None:
                    row["kept"] = j
                    seen.add(_norm(piece.text))
                elif not r and t["pool"] in MODE_F:
                    seen.add(_norm(piece.text))      # every lint-clean Mode F candidate goes to G3-H; keep them apart
            out["items"].append(row)
    return out


def load() -> dict:
    tasks = build()
    src = _batches()
    frozen = _read_json(POOLS / "skins.json")
    seen = frozen_texts()
    counts = {"skin": Counter(d["register"] for d in frozen if not d["held_out"]),
              "skin_heldout": Counter(d["register"] for d in frozen if d["held_out"])}
    for pool, reg, text in _kept_redo_skins(src):
        if _norm(text) not in seen:
            seen.add(_norm(text))
            counts[pool][reg] += 1
    sel = select(tasks, seen)
    for row in sel["items"]:
        if row["pool"] in MODE_T and row["kept"] is not None:
            counts[row["pool"]][row["register"]] += 1
    short = [{"item": f"{pool}/{r}", "admitted": counts[pool].get(r, 0), "target": want}
             for pool in MODE_T for r, want in F.TARGETS[pool].items() if counts[pool].get(r, 0) < want]
    mode_f = [r for r in sel["items"] if r["pool"] in MODE_F]
    return {"mode_t_counts": {p: dict(c) for p, c in counts.items()}, "mode_t_shortfalls": short,
            "mode_t_items": [{k: r[k] for k in ("task", "qid", "register", "kept")} | {
                "reasons": [c["reasons"] for c in r["candidates"]]} for r in sel["items"] if r["pool"] in MODE_T],
            "mode_f_items": len(mode_f),
            "mode_f_items_with_a_lint_clean_candidate": sum(1 for r in mode_f if any(c["ok"] for c in r["candidates"])),
            "mode_f_lint_clean_candidates": sum(c["ok"] for r in mode_f for c in r["candidates"]),
            "mode_f_lint_reasons": dict(Counter(x.split(":", 1)[0] for r in mode_f for c in r["candidates"]
                                                for x in c["reasons"])),
            "problems": sel["problems"], "selection": sel}


# ------------------------------------------------------------------------------------------------ G3-H (Mode F)

def g3h_batch(sel: dict):
    """(TaskBatch of the G3-H read, expected rows, files): every lint-clean Mode F candidate, frozen prompt + fields."""
    fields = E.g3h_fields()
    src = _batches()
    items, expected = [], []
    for row in sel["items"]:
        if row["pool"] not in MODE_F:
            continue
        facts = None
        for _tid, (_p, b, c) in src.items():
            for it in c["items"]:
                if b.key.get(it["qid"]) == row["iid"]:
                    facts = dict(it["facts"])
        for cand in row["candidates"]:
            if cand["ok"]:
                iid = f"g3h2|{row['iid']}|c{cand['j']}"
                items.append((iid, g3h.extraction_item(cand["text"], fields)))
                expected.append({"g3h_id": iid, "source_iid": row["iid"], "qid": row["qid"], "j": cand["j"],
                                 "pool": row["pool"], "register": row["register"], "held_out": row["held_out"],
                                 "text_sha256": _sha(cand["text"]),
                                 "expected": {"project": facts["PROJECT"], "person": facts["PERSON"]}})
    if not items:
        raise SystemExit("no lint-clean Mode F candidate: nothing to read")
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"t36-{VERSION}-g3h-r1", prompt=E.G3H_PROMPT)
    rows = []
    for i, c in enumerate(b.chunks):
        answer = str(G3H_ROOT / b.answer_path(c["task_id"]))
        b.chunks[i] = {"task_id": c["task_id"], "kind": c["kind"], "read": "g3h-redo2", "prompt_sha": c["prompt_sha"],
                       "answer_file": answer, "instructions": E.G3H_PROMPT.split("\n"), "items": c["items"]}
        if any(iid in json.dumps(b.chunks[i], ensure_ascii=False) for iid in b.key.values()):
            raise chunker.ChunkError(f"chunk {c['task_id']} names an internal id")
        rd, wr = b.allowed(str(G3H_ROOT), c["task_id"])
        rows.append({"read": "g3h-redo2", "kind": "extract_g3h", "task_id": c["task_id"], "batch_id": b.batch_id,
                     "task_file": str(G3H_ROOT / b.chunk_path(c["task_id"])), "answer_file": answer,
                     "prompt_sha": b.prompt_sha, "n_items": len(c["items"]), "outputs_expected": len(c["items"]),
                     "allowed_read": sorted(rd), "allowed_write": sorted(wr)})
    fs = dict(b.files())
    fs["TASKS.json"] = json.dumps({"family": FAMILY, "version": VERSION, "stage": "redo2 G3-H read",
                                   "prompt": "extract.G3H_PROMPT (unchanged)", "prompt_sha": b.prompt_sha,
                                   "n_tasks": len(rows), "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    fs["answers/README.txt"] = ("T36 redo2 G3-H answers: one <task_id>.json per task (see ../TASKS.json). Written only "
                                "by the task agents.\n")
    fs["pool/g3h_expected.jsonl"] = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in expected)
    return b, expected, fs


def g3h_write(fs: dict) -> list:
    clash = [rel for rel, text in fs.items()
             if (G3H_ROOT / rel).exists() and (G3H_ROOT / rel).read_text(encoding="utf-8") != text]
    if clash:
        raise SystemExit(f"redo2 G3-H files already exist with other content (written once): {clash[:5]}")
    return [str(p) for p in paths.write_files(G3H_ROOT, fs)]


def g3h_check() -> dict:
    """Compare every G3-H answer (g3h.compare, exact); per item keep the first lint-clean candidate whose read passes;
    Mode F counts against freeze.TARGETS and the Mode F cap (1 per 3 Mode T skins of the same held-out status)."""
    res = load()
    b, expected, fs = g3h_batch(res["selection"])
    drift = [rel for rel, text in fs.items()
             if not (G3H_ROOT / rel).exists() or (G3H_ROOT / rel).read_text(encoding="utf-8") != text]
    if drift:
        raise SystemExit(f"G3-H files drifted or are missing: {drift[:5]}")
    raw = {}
    for c in b.chunks:
        f = G3H_ROOT / b.answer_path(c["task_id"])
        if f.exists():
            raw[c["task_id"]] = _read_json(f)
    got, probs = chunker.load_answers(b, raw)
    fields = E.g3h_fields()
    passed = {}
    for r in expected:
        ok, diffs = (g3h.compare(r["expected"], got[r["g3h_id"]], fields) if r["g3h_id"] in got
                     else (False, ["no answer"]))
        passed[r["g3h_id"]] = (ok, diffs)
    frozen_docs = _read_json(POOLS / "documents.json")
    counts = {"freeform": Counter(d["register"] for d in frozen_docs if not d["held_out"]),
              "freeform_heldout": Counter(d["register"] for d in frozen_docs if d["held_out"])}
    kept = []
    for row in res["selection"]["items"]:
        if row["pool"] not in MODE_F:
            continue
        for cand in row["candidates"]:
            iid = f"g3h2|{row['iid']}|c{cand['j']}"
            if cand["ok"] and passed.get(iid, (False,))[0]:
                kept.append({"qid": row["qid"], "iid": row["iid"], "j": cand["j"], "register": row["register"],
                             "held_out": row["held_out"]})
                counts[row["pool"]][row["register"]] += 1
                break
    short = [{"item": f"{pool}/{r}", "admitted": counts[pool].get(r, 0), "target": want}
             for pool in MODE_F for r, want in F.TARGETS[pool].items() if counts[pool].get(r, 0) < want]
    t_train = sum(res["mode_t_counts"]["skin"].values())
    t_held = sum(res["mode_t_counts"]["skin_heldout"].values())
    n = len(expected)
    n_ok = sum(1 for v in passed.values() if v[0])
    return {"g3h_bar": g3h.PASS_RATE, "candidates_read": n, "candidates_passed": n_ok,
            "failing_fields": dict(Counter(d.split(":", 1)[0] for ok, ds in passed.values() if not ok for d in ds)),
            "answer_problems": probs, "kept": kept, "mode_f_counts": {p: dict(c) for p, c in counts.items()},
            "mode_f_shortfalls": short,
            "mode_f_cap": {"train": {"kept": sum(counts["freeform"].values()), "cap": t_train // 3},
                           "held_out": {"kept": sum(counts["freeform_heldout"].values()), "cap": t_held // 3}}}


# ------------------------------------------------------------------------------------------------ main

def main(argv: list) -> int:
    cmd = argv[0] if argv else "tasks"
    if cmd == "tasks":
        tasks = build()
        print(json.dumps({"n_tasks": len(tasks), "items": sum(t["n_items"] for t in tasks),
                          "outputs_expected": sum(t["outputs_expected"] for t in tasks),
                          "tasks": [{k: t[k] for k in ("task_file", "answer_file", "author_kind", "n_items",
                                                        "n_candidates", "registers")} for t in tasks]}, indent=1))
    elif cmd == "write":
        print(json.dumps(write(build()), indent=1))
    elif cmd == "load":
        res = load()
        res.pop("selection")
        print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    elif cmd == "g3h":
        b, expected, fs = g3h_batch(load()["selection"])
        out = {"items": len(expected), "tasks": [c["task_id"] for c in b.chunks], "prompt_sha": b.prompt_sha,
               "prompt_unchanged": b.prompt_sha == _sha(E.G3H_PROMPT), "written": False}
        if "--write" in argv:
            out["files"] = g3h_write(fs)
            out["written"] = True
        print(json.dumps(out, indent=1))
    elif cmd == "g3h-check":
        print(json.dumps(g3h_check(), indent=1, ensure_ascii=False, default=str))
    else:
        raise SystemExit(f"unknown command {cmd!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
