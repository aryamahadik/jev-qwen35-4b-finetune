"""families/T12/haiku/redo2/build_redo2.py: T12 REDO-2, the count-percent comparator forms (G0_SPEC.md v2.1 section 2).

Blocker (pool freeze v1, pools/manifest.json shortfall "comparator forms cover both bound types for both sems"): the
pool holds cmp.le/cents 10, cmp.lt/cents 10, cmp.lt/count 1 and cmp.le/count 0, so T12Plugin._form_ids("cmp.le",
"count") raises on every percent card whose comparator is cmp.le (94 of 400 sampled specs). Cause: the v1 lex-cmp task
asked for count phrases and cents phrases with the same style hints, Haiku wrote the same phrases for both, and the
lexicon keeps one slot kind per text (LexiconRegistry.add refuses a duplicate text; authoring.dedup_comparators keeps
the first). Fix (G0 v2.1 section 2): a separate authoring task for count-percent phrases that name the part of the PO
unit price with a noun (share, fraction, portion, proportion), never write "percent", and repeat no admitted text;
then the same lint, dedup and 2/2 G-LEX reads, with a percent bound in the read text ("3 percent"). Every count form is
read that way, the one already admitted too. No gate, gold, label or semantics changes.

Writes ONLY under haiku/redo2/ (kit paths writers: A38 guard, never-open guard). Edits no pinned lean/*.py, no c_build
file, no other T12 file, never pools/. Nothing here writes a Haiku answer, sets a label or reads a gold.

Run from lean/c2_build (each stage refuses to overwrite its own files):
  ../../.venv/bin/python families/T12/haiku/redo2/build_redo2.py write     author task -> author/, REDO2_TASKS.json
  ../../.venv/bin/python families/T12/haiku/redo2/build_redo2.py check     rebuild in memory, byte-compare with disk
  ../../.venv/bin/python families/T12/haiku/redo2/build_redo2.py lint      after the author answer -> plan/lint_r2.json
  ../../.venv/bin/python families/T12/haiku/redo2/build_redo2.py extract   after lint: 2 G-LEX reads -> extract/
  ../../.venv/bin/python families/T12/haiku/redo2/build_redo2.py admit     after both reads -> plan/admit_r2.json
The pool re-freeze (pools/comparators.json, pools/lexicon.json, manifest) reads plan/admit_r2.json; it is not done here.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
T12 = HERE.parents[1]
C2_BUILD = HERE.parents[3]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry  # noqa: E402
from c2_kit.plugin import ContractError  # noqa: E402
from families.T12 import authoring as A  # noqa: E402
from families.T12 import extract_build as EB  # noqa: E402
from families.T12 import plugin as P  # noqa: E402
from families.T12 import solver_b as SB  # noqa: E402

FAMILY = "T12"
SEED = "t12-redo2-v1"
AUTHOR = HERE / "author"
EXTRACT = HERE / "extract"
PLAN = HERE / "plan"
INDEX = HERE / "REDO2_TASKS.json"
POOL_CMP = T12 / "pools" / "comparators.json"
POOL_LEX = T12 / "pools" / "lexicon.json"
PENDING_LEX = T12 / "haiku" / "extract" / "lexicon_pending.json"     # every v1 lexicon form (admitted or not)
N_PER = 12
READS = 2                                                             # G-LEX comparators: 2/2 (G0 section 2)
NOUNS = ("share", "fraction", "portion", "proportion")
FILLER = {"a", "an", "the", "any"}
PCT_SHOWN = S.count_slot(3, P.U_PCT)                                  # "3 percent": the read text's bound
PCT_ROUND_TRIP = (1, 3, 5, 2, 4)                                      # training and S5 values (G0 R5)
NOT_WORDS = ("po", "price", "unit", "line", "every")
# a phrase states its endpoint with a comparison word (G0 section 2: "the endpoint is said plainly"); the readers then
# decide which endpoint (G-LEX). "a share of {X}" has none and is dropped before the reads.
COMPARE_WORDS = {"most", "less", "lesser", "smaller", "lower", "below", "beneath", "underneath", "short", "equal",
                 "including", "than"}


# ================================================================================================ the author task
def existing_texts() -> list:
    """The 21 admitted comparator texts (pool v1), in pool order: the task forbids every one of them."""
    return [it["text"] for it in json.loads(POOL_CMP.read_text(encoding="utf-8"))["items"]]


ENDPOINT = {
    "cmp.le": ("a share exactly equal to {X} must clearly count as meeting the condition (comparison styles such as "
               "'at most', 'or less', 'or smaller', 'no more than', 'equal to or less than', always joined to the "
               "noun)"),
    "cmp.lt": ("a share exactly equal to {X} must clearly NOT meet the condition (comparison styles such as 'less "
               "than', 'smaller than', 'below', 'lower than', 'strictly less than', always joined to the noun)"),
}
NEGATION = {
    "cmp.le": ("No negation word (no, not, none, never, nothing, without), except inside the comparator phrases 'no "
               "more than' and 'not more than'; so never 'no larger', 'no greater', 'no bigger' or 'not above'."),
    "cmp.lt": ("No negation word at all (no, not, none, never, nothing, without); so never 'not as large as', 'no "
               "larger' or 'not reaching'."),
}

PROMPT = (
    "You write short operator phrases for a synthetic training dataset. " + A.SETTING + " A program inserts each "
    "phrase into one fixed sentence of the policy card: the price condition of a card whose bound is a percentage of "
    "the PO unit price, 'invoiced unit price minus PO unit price is ___ of the PO unit price on every line'. The {X} "
    "in your phrase is filled with that percentage, like '3 percent'. Two independent readers will later be asked "
    "what each phrase means, and a phrase is kept only if both readers pick the meaning you were given, so every "
    "phrase must have exactly one clear reading. The program already uses the phrases listed under EXISTING PHRASES "
    "(most of them for amounts of money); yours must be new phrases made for a percentage: each one names the part "
    "of the PO unit price with one of the nouns share, fraction, portion or proportion. Each item asks for "
    f"{N_PER} different phrases in the answer field \"texts\".")
PROMPT_RULES = [
    "Each phrase is one line with no line break, in lower case.",
    f"The {N_PER} phrases of an item differ from each other, and not only in letter case, punctuation, an article "
    "(a, an, the) or the word 'any'.",
    "Write only what the item asks; add no example values, no names and no digits.",
    "Each phrase contains exactly one of the nouns share, fraction, portion or proportion (singular), naming the part "
    f"of the PO unit price that the difference is; across the {N_PER} phrases of an item use at least three of these "
    "four nouns.",
    "Never write the words percent, percentage or per cent, and no percent sign: the value filled into {X} already "
    "ends with the word percent.",
    "Never end a phrase with 'of', and never write the words PO, price, unit, line or every: the sentence goes on "
    "with 'of the PO unit price on every line'.",
]


def prompt_text() -> str:
    rules = "\n".join(f"R{i + 1}. {r}" for i, r in enumerate(PROMPT_RULES))
    ex = "\n".join(f"- {t}" for t in existing_texts())
    return (f"{PROMPT}\n\nRULES (every item):\n{rules}\n\nEXISTING PHRASES (never write one of these, and never one "
            f"of these with only an article (a, an, the) or the word 'any' added or taken away):\n{ex}{A.TAIL}")


def author_items() -> list:
    meaning = {s: m for s, _, m in P.LEX_SEMS}
    frame = "'invoiced unit price minus PO unit price is ___ of the PO unit price on every line'"
    out = []
    for sem in P.CMP_SEMS:
        styles = "'at most' or 'or less'" if sem == "cmp.le" else "'less than' or 'below'"
        brief = (f"Write {N_PER} different phrases that each mean: {meaning[sem]} {{X}}, where {{X}} is "
                 f"{A.CMP_X['count']}. A phrase replaces ___ in {frame} and must read naturally there; it names the "
                 "part of the PO unit price with one of the nouns share, fraction, portion or proportion. Answer "
                 f"field: \"texts\" (a list of {N_PER} phrases, each containing {{X}} exactly once).")
        out.append((f"cmp|{sem}|count|r2", {
            "brief": brief, "meaning": meaning[sem], "slots": {"X": A.CMP_X["count"]},
            "rules": ["Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
                      "2-8 words besides {X}; lower case; no digits; no punctuation except a hyphen.",
                      "State the endpoint plainly: " + ENDPOINT[sem] + ".",
                      "A noun next to {X} with no comparison word (styles like 'a share of {X}' or 'a fraction of "
                      "{X}') states no endpoint and is not allowed: every phrase holds one comparison word or phrase.",
                      f"Vary the comparison words as well as the noun: no comparison wording (such as {styles}) in "
                      f"more than three of your {N_PER} phrases.",
                      "Never use the words within, under, over, beyond, exceed, exceeds, exceeding, limit, cap, "
                      "capped, maximum, minimum, max, min, ceiling, allowed, permitted or range, and never 'up to' "
                      "unless it is followed by 'and including'.",
                      NEGATION[sem],
                      "Never start the phrase with 'is'; the sentence already holds it."]}))
    return out


def author_batch() -> chunker.TaskBatch:
    b = chunker.make_batch("author_lexicon", FAMILY, author_items(), seed=f"{SEED}|lex-cmp-count", prompt=prompt_text(),
                           forbid_strings=A.FORBID)
    if len(b.chunks) != 1:
        raise chunker.ChunkError("one author task")
    return b


def author_files(b: chunker.TaskBatch) -> tuple:
    c = b.chunks[0]
    tid = c["task_id"]
    ans = AUTHOR / b.answer_path(tid)
    md = A.task_markdown(b, c, ans, N_PER).replace("# T12 authoring task", "# T12 REDO-2 authoring task", 1)
    files = dict(b.files())
    files[f"tasks/{tid}.md"] = md
    files["answers/README.txt"] = ("Haiku answer file of the REDO-2 author task (see ../../REDO2_TASKS.json). Written "
                                   "only by the task agent; read by build_redo2.py lint.\n")
    tf = AUTHOR / "tasks" / f"{tid}.md"
    row = {"stage": "redo2-a", "task": "lex-cmp-count", "task_id": tid, "kind": b.kind, "pool": "comparators",
           "held_out": False, "blocker": "cmp.le/count 0 and cmp.lt/count 1 admitted (pools/manifest.json shortfall)",
           "need": "admitted count-percent comparator forms of cmp.le and cmp.lt (G0 v2.1 section 2)",
           "answer_field": "texts", "task_file": str(tf), "answer_file": str(ans), "batch_id": b.batch_id,
           "prompt_sha": b.prompt_sha, "task_sha256": chunker.sha(md), "n_items": len(c["items"]),
           "outputs_per_item": N_PER, "outputs_expected": N_PER * len(c["items"]),
           "allowed_read": sorted({str(tf)} | b.allowed(AUTHOR, tid)[0]), "allowed_write": [str(ans)]}
    for pth in (tf, ans):
        if paths.never_open(pth):
            raise chunker.ChunkError(f"never-open path {pth}")
    return files, row


def index_doc(rows: list) -> dict:
    g0 = (T12 / "G0_SPEC.md").read_bytes()
    if hashlib.sha256(g0).hexdigest() != P.G0_SHA256_AUTHORED:
        raise SystemExit("G0_SPEC.md does not match T12Plugin.G0_SHA256")
    return {"family": FAMILY, "version": "r2", "seed": SEED, "g0_sha256": P.G0_SHA256_AUTHORED,
            "stage": "redo2-a author (count-percent comparator forms); redo2-b G-LEX reads are built by "
                     "'build_redo2.py extract' only after 'lint' has run on the author answer",
            "notes": [
                "New items, new opaque ids, new answer paths; no v1 task, answer, key, record or pool file is changed.",
                "The task file is self-contained (answer path, prompt, rules, items, answer format). The agent reads "
                "only its task file and writes only its answer file (audit with allowed_read / allowed_write).",
                "key/ maps opaque qids to internal ids (orchestrator only).",
                "Labels: none. Haiku writes text pieces only; every gold still comes from solver A = solver B."],
            "n_tasks": len(rows), "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}


# ================================================================================================ lint (after answer)
def _words(text: str) -> list:
    return re.findall(r"[a-z]+", text.casefold().replace("{x}", " "))


def _loose(text: str) -> str:
    """The text without articles and 'any' (the task forbids an existing phrase with only those changed)."""
    return " ".join(w for w in re.findall(r"\{x\}|[a-z]+", text.casefold()) if w not in FILLER)


def redo2_rules(text: str) -> list:
    """The v2.1 count-percent rules on top of authoring.check_comparator (G0 section 2)."""
    w = _words(text)
    p = []
    n = sum(1 for x in w if x in NOUNS)
    if n != 1:
        p.append(f"names {n} of the nouns {'/'.join(NOUNS)} (exactly one)")
    if "percent" in text.casefold() or "per cent" in text.casefold() or "%" in text:
        p.append("writes percent")
    lit = text.replace("{X}", "")
    if lit != lit.lower():
        p.append("not lower case")
    if not set(w) & COMPARE_WORDS:
        p.append("no comparison word: the endpoint is not stated (G0 section 2)")
    if text.rstrip().casefold().endswith(" of"):
        p.append("ends with 'of'")
    p += [f"word {x!r} (the sentence holds it)" for x in w if x in NOT_WORDS]
    return p


def load_author(b: chunker.TaskBatch) -> tuple:
    tid = b.chunks[0]["task_id"]
    f = AUTHOR / b.answer_path(tid)
    if not f.is_file():
        raise SystemExit(f"author answer missing: {f}")
    data = f.read_bytes()
    got, probs = chunker.load_answers(b, {tid: json.loads(data.decode("utf-8"))})
    return got, probs, hashlib.sha256(data).hexdigest()


def lint_pieces(b: chunker.TaskBatch, got: dict) -> tuple:
    """(pieces, kept forms): every piece with its problems; kept = lint + dedup clean, in pid order."""
    tid = b.chunks[0]["task_id"]
    pending = json.loads(PENDING_LEX.read_text(encoding="utf-8"))
    taken = {EB._norm(f["text"]) for f in pending["forms"]}
    loose = {_loose(f["text"]): f["text"] for f in pending["forms"] if f["kind"] == "comparator"}
    pieces, seen = [], set()
    for iid in sorted(got):
        sem = iid.split("|")[1]
        ans = got[iid]
        texts = ans.get("texts") if isinstance(ans, dict) else None
        texts = list(texts) if isinstance(texts, list) else []
        if len(texts) != N_PER:
            pieces.append({"pid": iid, "sem": sem, "text": None, "problems": [f"{len(texts)} texts, {N_PER} asked"],
                           "stage": "task"})
        for i, t in enumerate(texts[:N_PER]):
            pr = A.check_comparator(t, sem, "count")
            if isinstance(t, str) and not pr:
                pr = redo2_rules(t)
            stage = "lint" if pr else None
            if not pr:
                if EB._norm(t) in taken:
                    pr, stage = ["repeats a v1 lexicon text"], "dedup"
                elif _loose(t) in loose:
                    pr, stage = [f"an existing phrase with only a/an/the/any changed ({loose[_loose(t)]!r})"], "dedup"
                elif EB._norm(t) in seen:
                    pr, stage = ["repeats an earlier redo2 piece"], "dedup"
            if not pr:
                seen.add(EB._norm(t))
            pieces.append({"pid": f"{iid}|{i}", "sem": sem, "text": t, "problems": pr, "stage": stage,
                           "task_id": tid, "prompt_sha": b.prompt_sha})
    kept = [p for p in pieces if not p["problems"]]
    return pieces, kept


def _add(reg: LexiconRegistry, p: dict):
    return reg.add(p["text"], p["sem"], slots={"X": "count"}, source="haiku", family=FAMILY,
                   haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"], held_out=False)


def combined_unit(kept: list, base_json: dict) -> tuple:
    """(kept forms, drops): each new form passes its unit test inside the v1 registry, and no v1 form starts failing
    (the extract_build.admit_units rule, with the v1 forms as the fixed base)."""
    drops = []
    forms = list(kept)
    while True:
        reg = LexiconRegistry.from_json(base_json)
        base_ok = {fid for fid in reg.forms if reg.forms[fid].unit_ok}
        ids = {}
        for p in forms:
            try:
                ids[_add(reg, p).form_id] = p
            except LexiconError as e:
                drops.append(dict(p, problems=[f"lexicon: {e}"], stage="unit"))
        bad_new = {fid: reg.forms[fid].unit_problems[:2] for fid in ids if not reg.unit_test(fid)}
        bad_old = sorted(fid for fid in base_ok if not reg.unit_test(fid))
        culprits = set(bad_new)
        for fid_old in bad_old:
            for fid, p in ids.items():
                r1 = LexiconRegistry.from_json(base_json)
                _add(r1, p)
                if not r1.unit_test(fid_old):
                    culprits.add(fid)
                    bad_new.setdefault(fid, [f"makes v1 form {fid_old} fail its unit test"])
        if bad_old and not culprits:
            raise SystemExit(f"v1 forms {bad_old} fail only with several redo2 forms together: report, do not guess")
        if not culprits:
            return list(ids.values()), drops
        for fid in sorted(culprits):
            drops.append(dict(ids[fid], problems=list(bad_new[fid]), stage="unit"))
        forms = [p for fid, p in ids.items() if fid not in culprits]


def run_lint() -> dict:
    b = author_batch()
    got, probs, sha = load_author(b)
    pieces, kept = lint_pieces(b, got)
    kept, unit_drops = combined_unit(kept, json.loads(PENDING_LEX.read_text(encoding="utf-8")))
    drop_ids = {p["pid"] for p in unit_drops}
    for p in pieces:
        if p["pid"] in drop_ids:
            u = next(x for x in unit_drops if x["pid"] == p["pid"])
            p.update(problems=u["problems"], stage="unit")
    for p in kept:
        p["form_id"] = EB._fid(p["sem"], p["text"])
    by = Counter((p["sem"], p["stage"] or "kept") for p in pieces)
    return {"family": FAMILY, "stage": "redo2-a lint", "task_id": b.chunks[0]["task_id"], "answer_sha256": sha,
            "load_problems": probs, "g0_sha256": P.G0_SHA256_AUTHORED,
            "checks": "authoring.check_comparator(text, sem, 'count') + G0 v2.1 count-percent rules + dedup against "
                      "every v1 lexicon text (haiku/extract/lexicon_pending.json) + unit tests in the combined registry",
            "counts": {f"{s}/{k}": v for (s, k), v in sorted(by.items())},
            "kept": [{k: p[k] for k in ("pid", "sem", "text", "form_id", "task_id", "prompt_sha")} for p in kept],
            "pieces": pieces}


# ================================================================================================ G-LEX reads
def read_forms(lint: dict) -> list:
    """[(form_id, sem, text, origin)]: the kept redo2 forms and every admitted v1 count form (re-read, G0 v2.1)."""
    out = [(p["form_id"], p["sem"], p["text"], "redo2") for p in lint["kept"]]
    for f in json.loads(POOL_LEX.read_text(encoding="utf-8"))["forms"]:
        if f["kind"] == "comparator" and f["slots"] == {"X": "count"}:
            out.append((f["form_id"], f["sem_id"], f["text"], "v1"))
    return sorted(out)


def glex_batches(lint: dict) -> list:
    reg = LexiconRegistry(FAMILY)
    P.declare_lexicon(reg)
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "comparator")
    forms = read_forms(lint)
    out = []
    for r in range(1, READS + 1):
        seed = f"{SEED}|glex-comparator-count-r{r}"
        items = []
        for fid, _sem, text, _o in forms:
            filled = text.replace("{X}", S.render(PCT_SHOWN))
            ch = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
            items.append((fid, {"text": filled, "choices": ch}))
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=EB.PROMPT_LEX)
        out.append((r, b))
    return out


def extract_files(lint: dict) -> tuple:
    files, rows = {}, []
    for r, b in glex_batches(lint):
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            ans = EXTRACT / b.answer_path(tid)
            md = EB.task_markdown("extract_lex", b, c, ans).replace("# T12 extraction task",
                                                                     "# T12 REDO-2 extraction task", 1)
            files[f"tasks/{tid}.md"] = md
            tf = EXTRACT / "tasks" / f"{tid}.md"
            rows.append({"stage": "redo2-b", "task": f"comparator-count-r{r}", "task_id": tid, "kind": "extract_lex",
                         "group": "comparator", "read": r, "n_items": len(c["items"]), "batch_id": b.batch_id,
                         "prompt_sha": b.prompt_sha, "task_sha256": chunker.sha(md),
                         "outputs_expected": len(c["items"]), "task_file": str(tf), "answer_file": str(ans),
                         "allowed_read": sorted({str(tf)} | b.allowed(EXTRACT, tid)[0]), "allowed_write": [str(ans)]})
    files["answers/README.txt"] = ("Haiku answer files of the REDO-2 G-LEX reads (see ../TASKS.json). Written only by "
                                   "the task agents; read by build_redo2.py admit. An answer is a meaning text; a "
                                   "disagreement rejects the form for good.\n")
    files["TASKS.json"] = json.dumps({
        "family": FAMILY, "stage": "redo2-b G-LEX reads (2/2) of the count-percent comparator forms",
        "g0_sha256": P.G0_SHA256_AUTHORED, "lint_answer_sha256": lint["answer_sha256"],
        "read_text": "each form filled with the percent bound '3 percent' (G0 v2.1 section 2)",
        "forms": [{"form_id": f, "sem_id": s, "text": t, "origin": o} for f, s, t, o in read_forms(lint)],
        "answer_format": EB.ANSWER_SPEC["extract_lex"][0],
        "record": "reg.record_extraction(form_id, extractor_id=task_id, sem_id=reg.meaning_to_sem('comparator', "
                  "answer['meaning']))",
        "n_tasks": len(rows), "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    return files, rows


# ================================================================================================ admit (after reads)
def admit(lint: dict, raw_answers: dict | None = None) -> dict:
    """raw_answers: {task_id: answer object} in place of the answer files (in-memory code tests only)."""
    files, rows = extract_files(lint)
    probs = [f"extract/{rel} differs from the rebuilt file" for rel, text in sorted(files.items())
             if rel not in ("TASKS.json", "answers/README.txt")
             and (not (EXTRACT / rel).is_file() or (EXTRACT / rel).read_text(encoding="utf-8") != text)]
    reg = LexiconRegistry.from_json(json.loads(POOL_LEX.read_text(encoding="utf-8")))
    for p in lint["kept"]:
        _add(reg, p)
    unit_bad = sorted(fid for fid in reg.forms if not reg.unit_test(fid))
    answers = {}
    for r, b in glex_batches(lint):
        for c in b.chunks:
            tid = c["task_id"]
            f = EXTRACT / b.answer_path(tid)
            if raw_answers is not None:
                raw = raw_answers.get(tid)
            elif f.is_file():
                data = f.read_bytes()
                answers[f.name] = hashlib.sha256(data).hexdigest()
                raw = json.loads(data.decode("utf-8"))
            else:
                raw = None
            if raw is None:
                probs.append(f"{tid}: answer file missing")
                continue
            got, lp = chunker.load_answers(b, {tid: raw})
            probs += lp
            for fid, a in sorted(got.items()):
                m = a.get("meaning") if isinstance(a, dict) else None
                reg.record_extraction(fid, tid, reg.meaning_to_sem("comparator", m) if isinstance(m, str) else None)
    forms = read_forms(lint)
    status = {fid: reg.status(fid) for fid, *_ in forms}
    cover = Counter((f.sem_id, dict(f.slots)["X"]) for fid, f in reg.forms.items()
                    if f.kind == "comparator" and reg.status(fid) == "admitted")
    trip = []
    for fid, sem, text, _o in forms:
        if status[fid] != "admitted":
            continue
        for v in PCT_ROUND_TRIP:
            clause = text.replace("{X}", S.render(S.count_slot(v, P.U_PCT)))
            cond = P.COND_TPL["price_pct"].replace("{TOL_CMP}", clause)
            m = SB.COND_PCT_RE.fullmatch(cond)
            try:
                got = reg.parse_exact(m["c"], {"X": SB.PERCENT}, admitted_only=True) if m else None
            except LexiconError as e:
                got = str(e)
            if not (isinstance(got, tuple) and got[0] == sem and got[2] == {"X": v}):
                trip.append({"form_id": fid, "value": v, "condition": cond, "parsed": str(got)})
    plugin = P.T12Plugin(lexicon=reg)
    errs, n_pct, used = Counter(), 0, Counter()
    for seed in range(100):
        for smp in ("S1", "S2", "S3", "S4", "S5"):
            try:
                sp = plugin.sample(seed, smp)
            except ContractError as e:
                errs[str(e)[:80]] += 1
                continue
            if sp.structure.get("tol_kind") == "pct":
                n_pct += 1
                used[sp.slots["TOL_CMP"].value[1]] += 1
    new_rows = []
    for p in lint["kept"]:
        if status.get(p["form_id"]) == "admitted":
            new_rows.append({"pid": p["pid"], "held_out": False, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                             "sem_id": p["sem"], "bound": "count", "form_id": p["form_id"], "status": "admitted",
                             "text": p["text"]})
    lex_forms = [f for f in reg.to_json()["forms"] if f["form_id"] in status]
    met = all(cover.get((s, k), 0) > 0 for s in P.CMP_SEMS for k in ("count", "cents"))
    return {"family": FAMILY, "stage": "redo2-b admit (in memory; pools/ untouched)",
            "g0_sha256": P.G0_SHA256_AUTHORED, "problems": probs, "answers_sha256": answers,
            "unit_test_failures": unit_bad,
            "status": {fid: {"status": status[fid], "sem": s, "text": t, "origin": o,
                             "reads": [list(e) for e in reg.forms[fid].extractions]} for fid, s, t, o in forms},
            "coverage_admitted": {f"{s}/{k}": cover.get((s, k), 0) for s in P.CMP_SEMS for k in ("count", "cents")},
            "coverage_met": met, "percent_round_trip_failures": trip,
            "dry_run": {"specs": 500, "contract_errors": dict(errs), "percent_cards": n_pct,
                        "tol_forms_used": dict(sorted(used.items()))},
            "refreeze": {"comparators_add": new_rows,
                         "v1_count_forms_rejected_by_reread": [fid for fid, s, t, o in forms
                                                               if o == "v1" and status[fid] != "admitted"],
                         "lexicon_forms": lex_forms},
            "ready_for_refreeze": met and not probs and not unit_bad and not trip and not errs}


# ================================================================================================ main
def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args else "check"
    if cmd in ("write", "check"):
        files, row = author_files(author_batch())
        doc = index_doc([row])
        if cmd == "write":
            if INDEX.exists():
                raise SystemExit(f"{INDEX} exists: redo2-a was written already")
            paths.write_files(AUTHOR, files)
            paths.write_json(INDEX, doc)
            print(json.dumps({"written": str(INDEX), "task_file": row["task_file"], "answer_file": row["answer_file"],
                              "outputs_expected": row["outputs_expected"]}, indent=1))
            return 0
        diff = [rel for rel, text in sorted(files.items())
                if not (AUTHOR / rel).is_file() or (AUTHOR / rel).read_text(encoding="utf-8") != text]
        on_disk = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.is_file() else None
        print(json.dumps({"author_files": len(files), "differ": diff, "index_same": on_disk == doc}, indent=1))
        return 1 if diff or on_disk != doc else 0
    if cmd == "lint":
        out = run_lint()
        paths.write_json(PLAN / "lint_r2.json", out)
        print(json.dumps({"counts": out["counts"], "kept": len(out["kept"]), "load_problems": out["load_problems"]},
                         indent=1))
        return 0
    if cmd == "extract":
        lint = json.loads((PLAN / "lint_r2.json").read_text(encoding="utf-8"))
        if lint["answer_sha256"] != load_author(author_batch())[2]:
            raise SystemExit("plan/lint_r2.json is stale: run lint again")
        if (EXTRACT / "TASKS.json").exists():
            raise SystemExit("extract/TASKS.json exists: redo2-b was written already")
        files, rows = extract_files(lint)
        paths.write_files(EXTRACT, files)
        print(json.dumps({"tasks": [(r["task_file"], r["answer_file"], r["n_items"]) for r in rows]}, indent=1))
        return 0
    if cmd == "admit":
        lint = json.loads((PLAN / "lint_r2.json").read_text(encoding="utf-8"))
        out = admit(lint)
        paths.write_json(PLAN / "admit_r2.json", out)
        print(json.dumps({k: out[k] for k in ("problems", "coverage_admitted", "coverage_met", "dry_run",
                                              "ready_for_refreeze")}, ensure_ascii=False, indent=1))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
