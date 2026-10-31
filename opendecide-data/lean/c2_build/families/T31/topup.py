"""families/T31/topup.py: the T31 pool TOP-UP (round 2). New Haiku authoring tasks for the pool cells and wording forms
the v1 plan could not fill, the G-LEX reads of the new forms, and a v2 pool freeze. No v1 file is rewritten.

Why (freeze-v1 shortfalls in pools/MANIFEST.json; G0_SPEC.md section 7, unchanged):
  1. chat / email / transcript skins: the v1 plan (haiku_author.SKINS_T + SKINS_F) gave 15 Mode T + 8 Mode F = 23 per
     (register, track), below the G0 7 floor of 24 before any drop. A re-read cannot exceed 23: new items are needed.
  2. log|appr skins: 28 of 36 failed the G-SL name lint on the capitalised word right after "[tag] "
     (gsl._sentence_starts counts the line start and the text after . ! ? : ; | as sentence starts, never the word
     after "] "). The lint stays; the new brief says: every word after the tag in lowercase.
  3. ch_scope wordings: the v1 brief said "which one of the listed scopes"; "one" is a CORE number word for the
     wording role, so 10 of 24 were dropped. New brief: "which of the listed scopes" (G0 M12 wording).
  4. yn_holder_other wordings: the v1 brief allowed "other than", "besides" or "someone else", but NEG_COUNTS
     (k_syn 0, k_all 1) is met only by "other than" (negcount). New brief: "other than" only.
  5. No code path: haiku_author.build, extract_build.run(write=True) and glex_admit.run(write=True) refuse to rewrite.
     This module writes only its own folders: haiku/redo2/ (authoring), haiku/redo2/extract/ (G-LEX 2/2 reads of every
     lexicon form that has no v1 read) and pools_v2/ (the v2 freeze; pools/ stays as frozen v1).
Unchanged: every gate and lint (gsl, NEG_COUNTS, G-LEX 2/2), the registry meanings (QUESTION_SEM_MEANING, decoys,
comparators: so the v1 reads still verify byte for byte), G0_SPEC.md and its pin, every v1 task, answer and pool file.

  check          the top-up authoring batches in memory: counts per cell, guards. Nothing is written.
  build          write them under haiku/redo2/ (after A38 only); refuses once any redo2 answer exists.
  load           v1 answers + the v1 redo answer (haiku/redo/) + redo2 answers -> merged candidate pools, in memory.
  extract-check  the G-LEX reads for the forms with no v1 read, in memory.
  extract-build  write them under haiku/redo2/extract/; refuses when that folder holds files or an author task of
                 redo2 is unanswered.
  admit-check    admission (v1 reads verified byte for byte + the redo2 reads), counts and G0 shortfalls, in memory.
  freeze         the same, then write pools_v2/ (refuses when pools_v2/MANIFEST.json exists). g13_c2 reads
                 families/T31/pools/: promoting v2 = move pools/ to pools_v1/, then pools_v2/ to pools/ (an
                 orchestrator step, recorded in the v2 manifest).

Run from lean/:  ../.venv/bin/python c2_build/families/T31/topup.py check|build|load|extract-check|extract-build|
                 admit-check|freeze

Haiku answers only flag: every new piece goes through the same loader lint (haiku_author._load_one), the same dedup and
the same G-LEX admission as v1. Nothing here sets or edits a label.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import gsl, paths  # noqa: E402
from families.T31 import extract_build as EB  # noqa: E402
from families.T31 import glex_admit as GA  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402
from families.T31 import plugin as P  # noqa: E402

F = "T31"
HERE = Path(__file__).resolve().parent
ROOT2 = HERE / "haiku" / "redo2"
EXTRACT2 = ROOT2 / "extract"
REDO1 = HERE / "haiku" / "redo"
POOLS2 = HERE / "pools_v2"
SEED2 = "t31-topup-r2"
SEED_GLEX2 = "t31-glex-r2"
VERSION2 = "topup-r2"
READS2 = ("r2read0", "r2read1")            # 2/2 (T31 has no precedence or window form); new extractor ids

# ------------------------------------------------------------------------------------------------ plan
# New items per cell (v1 count in the freeze-v1 manifest -> floor 24 per training (register, track), with spare for
# the 7-10% lint / dedup loss seen in v1 and for later G13-seed quarantines).
#   chat|appr 22, chat|agent 22, email|appr 22, email|agent 23, transcript|appr 21, transcript|agent 22: +6 T +2 F each
#   log|appr 8: +28 T under the lowercase brief (log|agent kept 35 of 36 with lowercase text)
TOPUP_SKINS_T = {("appr", "chat"): 6, ("agent", "chat"): 6, ("appr", "email"): 6, ("agent", "email"): 6,
                 ("appr", "transcript"): 6, ("agent", "transcript"): 6, ("appr", "log"): 28}
TOPUP_SKINS_F = {"chat": 2, "email": 2, "transcript": 2}          # per track (keeps Mode F near 20% of the pool)
# Wording candidates: v1 151 (+1 from the v1 redo answer) vs "about 170" (G0 7); per form up to the v1 plan
# (haiku_author.WORDINGS) with spare: ch_scope 13 -> plan 24; yn_holder_other 10 -> 14; yn_agent_ok 22 -> 26;
# yn_holder_not 10 (8 admitted) -> 10 admitted; yn_holder 25, yn_agent_beyond 11, yn_agent_lacks 11 -> plan.
TOPUP_WORDINGS = {"ch_scope": 14, "yn_holder_other": 6, "yn_agent_ok": 6, "yn_holder_not": 3, "yn_holder": 2,
                  "yn_agent_beyond": 2, "yn_agent_lacks": 2}
APPR_Q = ("yn_holder", "yn_holder_other", "yn_holder_not")
AGENT_Q = ("ch_scope", "yn_agent_ok", "yn_agent_beyond", "yn_agent_lacks")

# The v1 redo (haiku/redo/): one ch_approver item whose v1 answer came back under a mistyped qid. Its answer is merged
# here by qid (the v1 batch key still applies); only these qids are taken from the redo answer file.
REDO1_ITEMS = {"T31-author_wording-a7e52c11-000": ("qc40242781b",)}

# ------------------------------------------------------------------------------------------------ briefs (v2)
# Only the AUTHORING briefs change. QUESTION_SEM_MEANING (the G-LEX choices) is unchanged, so every v1 read still
# verifies byte for byte and the new forms are read against the same closed list of meanings.
QUESTION_MEANING_V2 = dict(HA.QUESTION_MEANING)
QUESTION_MEANING_V2.update({
    "ch_scope": ("Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the "
                 "listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other "
                 "number word (a checking program rejects them). The program shows the scopes as answer options; do "
                 "not list them.", ("{REQ_AGENT}",), ()),
    "yn_holder_other": ("Ask whether the accountable (A) role for the request belongs to a person other than "
                        "{CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other "
                        "than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other "
                        "than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a "
                        "checking program accepts only 'other than'.", ("{CANDIDATE}",), ()),
    "yn_agent_ok": ("Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of "
                    "permission then (yes = it may). Never start the question with the word 'May' (a checking "
                    "program reads a capitalised May as the month); 'may' later in the question is fine.",
                    ("{REQ_AGENT}", "{REQ_SCOPE}"), ()),
    "yn_agent_beyond": ("Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall "
                        "outside the authority of {REQ_AGENT} (yes = it would). Use no negation words, and never the "
                        "word 'past' (a checking program reads it as a time word).", ("{REQ_AGENT}", "{REQ_SCOPE}"),
                        ()),
})
WORDING_RULES_V2 = {
    "ch_scope": ["no negation at all", "'which of the listed scopes' or 'which listed scope'; never 'which one'"],
    "yn_holder_other": ["exactly one 'other than', followed by {CANDIDATE}",
                        "no 'besides', no 'else', no 'not', no n't"],
    "yn_agent_ok": ["no negation at all", "the first word is never 'May'"],
    "yn_agent_beyond": ["no negation at all", "never the word 'past'"],
}

LOG_TEXT_V2 = ("one to three log lines, each starting with a lowercase tag in square brackets such as [intake] or "
               "[desk], then one space and text written ENTIRELY in lowercase; no timestamps, no level words, no line "
               "numbers")
RULE2_OLD = (f"2. No name or capitalised word except at the start of a line or sentence, a speaker label at the start "
             f"of a line,\n   and the acronyms {HA.ALLOWED_CAPS}. Write teams in lowercase (\"the finance desk\").")
RULE2_LOG = (f"2. Write every word in lowercase, including the first word right after the tag and the first word after "
             f"a full stop:\n   '[desk] hi, {{REQUESTER}} here ...', never '[desk] Hi, {{REQUESTER}} here ...'. A "
             f"checking program reads a\n   capitalised word after the tag as a person's name and throws the text "
             f"away. The only capitals allowed are\n   inside the placeholders and the acronyms {HA.ALLOWED_CAPS}. "
             f"After a tag write {{a|ITEM}} or 'the {{ITEM}}', never\n   {{A|ITEM}} or {{cap|ITEM}}. Avoid the "
             f"pronoun I (write as a desk or in the third person). Write teams in lowercase\n   (\"the finance "
             f"desk\").")
RULE7_OLD = "7. Each item asks for a particular variation;"
RULE7_NEW = ("7. Never write 'kind of' or 'sort of' (a checking program reads them as hedges).\n"
             "8. Each item asks for a particular variation;")
FREE_RULE_OLD = "6. 30-90 words, in the item's register"
FREE_RULE_NEW = ("6. No number word at all, not even 'one' (never 'one more thing', 'this one' or 'one quick note'); "
                 "never 'kind of'\n   or 'sort of'.\n7. 30-90 words, in the item's register")
SKIN_SHAPES_LOG = tuple(s for s in HA.SKIN_SHAPES if "{A|ITEM}" not in s and "{cap|ITEM}" not in s)


def _replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"prompt patch: expected exactly one {old[:50]!r}, found {text.count(old)}")
    return text.replace(old, new)


def skin_prompt_v2(register: str, track: str) -> str:
    p = _replace_once(HA._skin_prompt(register, track), RULE7_OLD, RULE7_NEW)
    if register == "log":
        p = _replace_once(p, HA.REGISTER_TEXT["log"], LOG_TEXT_V2)
        p = _replace_once(p, RULE2_OLD, RULE2_LOG)
    return p


def freeform_prompt_v2(track: str) -> str:
    return _replace_once(HA._freeform_prompt(track), FREE_RULE_OLD, FREE_RULE_NEW)


def _wording_banned() -> str:
    words = set(gsl.CORE["number"]) | set(gsl.CORE["relative_time"]) | set(gsl.EXTENDED["relative_time"]) | \
        set(gsl.CORE["hedge"]) | set(gsl.EXTENDED["hedge"])
    return ", ".join(sorted(words))


def wording_prompt_v2(track: str, existing: dict) -> str:
    """HA's wording prompt plus the checked word list and the wordings that already exist (exact repeats are thrown
    away as duplicates). existing: {qform: [text, ...]} for the forms of this task."""
    lines = []
    for q in (APPR_Q if track == "appr" else AGENT_Q):
        texts = sorted(existing.get(q, ()))
        if not texts:
            continue
        lines.append(f"  Meaning: {QUESTION_MEANING_V2[q][0].split(' (yes')[0].split('. ')[0]}.")
        lines += [f"    - {t}" for t in texts]
    add = ("8. A checking program also rejects these words in a question: " + _wording_banned() + "; any month or "
           "weekday name (so never start with 'May'); 'kind of' and 'sort of'.\n"
           "9. Wordings that already exist are listed below. Never repeat one of them word for word; write wordings "
           "that differ from them in structure and word choice, with the same meaning.\n"
           "EXISTING WORDINGS (do not repeat):\n" + "\n".join(lines) + "\n")
    return _replace_once(HA._wording_prompt(track), "\nANSWER FORMAT:", add + "\nANSWER FORMAT:")


# ------------------------------------------------------------------------------------------------ items

def _rng(*parts) -> random.Random:
    return random.Random("|".join(str(p) for p in (SEED2,) + parts))


def skin_items_v2(register: str, track: str, n: int) -> list:
    rng = _rng("skin", register, track)
    shapes = SKIN_SHAPES_LOG if register == "log" else HA.SKIN_SHAPES
    out = []
    for i in range(n):
        j = i + 15                         # continue the v1 variation cycle (v1 used 0-14 in these cells)
        use_id = rng.random() < 0.55
        brief = (f"Variation: {HA.SKIN_VOICES[j % len(HA.SKIN_VOICES)]}; {shapes[(j * 5 + 3) % len(shapes)]}; "
                 f"{HA.SKIN_LENGTHS[j % len(HA.SKIN_LENGTHS)]}. {HA.TRACK_TEXT[track]}")
        slots = {"REQUESTER": "required, exactly once", "ITEM": "required, exactly once",
                 "REQ_ID": "required, exactly once" if use_id else "leave it out"}
        rules = ["use {REQ_ID} exactly once" if use_id else "do not use {REQ_ID}"]
        if register == "log":
            rules.append("every word after the tag in lowercase (capitals only inside placeholders)")
        out.append((f"skin|{track}|{register}|T|r2{i:03d}",
                    {"brief": brief, "register": register, "slots": slots, "rules": rules}))
    return out


def freeform_items_v2(track: str) -> list:
    rng = _rng("free", track)
    used: set = set()
    out = []
    for register, n in TOPUP_SKINS_F.items():
        for i in range(n):
            k = len(out)
            out.append((f"free|{track}|{register}|T|r2{i:03d}",
                        {"brief": f"Register: {register}. Style: "
                                  f"{HA.FREEFORM_STYLES[(k * 3 + 1) % len(HA.FREEFORM_STYLES)]}. "
                                  f"{HA.TRACK_TEXT[track]}",
                         "register": register, "facts": HA._fake_facts(rng, track, used),
                         "rules": ["each fact exactly as given", "no 'a' or 'an' right before the item",
                                   "no number word, not even 'one'"]}))
    return out


def wording_items_v2(qforms: tuple) -> list:
    out = []
    for q in qforms:
        meaning, required, _ = QUESTION_MEANING_V2[q]
        for i in range(TOPUP_WORDINGS[q]):
            slots = {r.strip("{}"): "required, exactly once" for r in required}
            slots.setdefault("REQ_ID", "optional, at most once")
            if q in WORDING_RULES_V2:
                rules = list(WORDING_RULES_V2[q])
            elif q in ("yn_holder_not", "yn_agent_not"):
                rules = ["exactly one 'not', inside an embedded statement"]
            elif q in ("yn_holder_other", "yn_agent_lacks"):
                rules = ["no 'not' and no n't; the one implicit negation the meaning asks for only"]
            else:
                rules = ["no negation at all"]
            style = HA.WORDING_STYLES[(i * 7 + len(q) + 4) % len(HA.WORDING_STYLES)]
            out.append((f"wording|{q}|r2{i:03d}", {"brief": f"Meaning: {meaning} Style: {style}.", "slots": slots,
                                                   "rules": rules}))
    return out


# ------------------------------------------------------------------------------------------------ batches

WHY = {
    "skin-cell": "G0 7 floor of 24 per (training register, track): the v1 plan gave 23 at most in this cell",
    "skin-log": "log|appr: 28 of 36 v1 skins failed the G-SL name lint (capital after the tag); lowercase brief",
    "free-cell": "Mode F share of the chat / email / transcript top-up (about 20% of the pool, G0 7)",
    "wording-appr": "yn_holder_other brief names 'other than' only (NEG_COUNTS (0, 1)); wording pool toward about 170",
    "wording-agent": "ch_scope brief says 'which of the listed scopes' (no number word); wording pool toward about 170",
}


def existing_wordings() -> dict:
    """{qform: [text]} of the v1 wording candidates that passed the loader (read from the v1 answers)."""
    res = HA.load()
    out: dict = {}
    for sk, _fid in res["pools"]["wordings"].values():
        out.setdefault(sk.qform, []).append(sk.text)
    return out


def plan2(existing: dict | None = None) -> list:
    """[(task name, kind, items, prompt, forbid, info)] in a fixed order (one batch, one chunk, one task each)."""
    existing = existing_wordings() if existing is None else existing
    out = []
    for (track, register), n in TOPUP_SKINS_T.items():
        why = "skin-log" if register == "log" else "skin-cell"
        out.append((f"r2-skin-{track}-{register}", "author_skin", skin_items_v2(register, track, n),
                    skin_prompt_v2(register, track), HA.FORBID_SKIN,
                    {"pool": "skin", "track": track, "register": register, "held_out": False, "mode": "T",
                     "why": WHY[why]}))
    for track in HA.TRACKS:
        out.append((f"r2-free-{track}", "author_freeform", freeform_items_v2(track), freeform_prompt_v2(track),
                    HA.FORBID_SKIN, {"pool": "freeform", "track": track, "register": "chat+email+transcript",
                                     "held_out": False, "mode": "F", "why": WHY["free-cell"]}))
    for track, qs in (("appr", APPR_Q), ("agent", AGENT_Q)):
        out.append((f"r2-wording-{track}", "author_wording", wording_items_v2(qs), wording_prompt_v2(track, existing),
                    HA.FORBID_WORDING, {"pool": "wording", "track": track, "register": "question",
                                        "held_out": False, "mode": "T", "why": WHY[f"wording-{track}"]}))
    return out


def build_batches2(existing: dict | None = None) -> list:
    out = []
    for name, kind, items, prompt, forbid, info in plan2(existing):
        if len(items) > CH.MAX_ITEMS:
            raise CH.ChunkError(f"{name}: {len(items)} items (one task holds <= {CH.MAX_ITEMS})")
        b = CH.make_batch(kind, F, items, seed=f"{SEED2}|{name}", prompt=prompt, forbid_strings=forbid)
        assert len(b.chunks) == 1
        out.append(({**info, "task": name}, b))
    return out


def _contract(n: int, qids: list) -> str:
    field = "text"
    return (
        "ANSWER CONTRACT (exact; a program checks it):\n"
        f"- The answer file holds one JSON array with exactly {n} objects, one per item at the bottom of this file.\n"
        f"- Each object has exactly two keys: \"qid\" and \"{field}\". No other keys.\n"
        "- \"qid\": copy the item's qid exactly, character for character. A qid is the letter q followed by ten "
        "letters or digits\n  (11 characters in all). Every qid below appears exactly once in your answer; never "
        "invent or shorten one.\n"
        f"- \"{field}\": your text as one JSON string (a line break inside it as \\n, a double quote as \\\").\n"
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments.\n"
        f"- The {n} qids of this task: {', '.join(qids)}\n"
        f"Literal example of the shape (your own text in \"{field}\"):\n"
        f"[{{\"qid\": \"{qids[0]}\", \"{field}\": \"...\"}}, ...]\n")


def task_file2(batch, chunk: dict, answer_path: Path, why: str) -> str:
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    return (f"# T31 TOP-UP authoring task {chunk['task_id']} (kind: {batch.kind}; {n} items)\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer_path}\n\n"
            f"WHY THIS TASK EXISTS: new items for the T31 pool ({why}). Every item is new; answer all {n}.\n\n"
            f"{_contract(n, qids)}\n"
            f"Task kind: {batch.kind}; items: {n}; answers expected: {n} (one per item, each with its qid).\n\n"
            f"FULL INSTRUCTIONS:\n\n{batch.prompt}\n"
            f"ITEMS (JSON; answer every item, keyed by its qid):\n"
            f"{json.dumps(chunk['items'], ensure_ascii=False, indent=1)}\n\n"
            f"Reminder: write one JSON array with exactly {n} objects ({{\"qid\": \"...\", \"text\": \"...\"}}) to "
            f"{answer_path} and nothing else.\n")


def files_for2(batches: list) -> tuple:
    files, tasks = {}, []
    n_out = 0
    for info, b in batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            answer = ROOT2 / b.answer_path(tid)
            task_rel = f"tasks/{tid}.md"
            text = task_file2(b, c, answer, info["why"])
            low = text.lower()
            for f in (HA.FORBID_WORDING if b.kind == "author_wording" else HA.FORBID_SKIN):
                if re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                    raise CH.ChunkError(f"{tid}: task file mentions a forbidden string {f!r}")
            for iid in b.key.values():
                if iid in text:
                    raise CH.ChunkError(f"{tid}: task file names an internal id")
            if paths.never_open(str(answer)) or paths.never_open(str(ROOT2 / task_rel)):
                raise CH.ChunkError(f"{tid}: a task path is on the never-open list")
            files[task_rel] = text
            n_out += len(c["items"])
            reads, writes = b.allowed(str(ROOT2), tid)
            tasks.append({"task": info["task"], "task_id": tid, "batch_id": b.batch_id, "kind": b.kind,
                          "pool": info["pool"], "track": info["track"], "register": info["register"],
                          "held_out": info["held_out"], "mode": info["mode"], "why": info["why"],
                          "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "task_file": str(ROOT2 / task_rel), "answer_file": str(answer),
                          "allowed_read": sorted(reads | {str(ROOT2 / task_rel)}), "allowed_write": sorted(writes)})
    manifest = {"family": F, "version": VERSION2, "seed": SEED2, "g0_sha256": P.POOL_G0_SHA256,
                "n_tasks": len(tasks), "items_expected": n_out,
                "plan": {"skins_T": {f"{r}|{t}": n for (t, r), n in TOPUP_SKINS_T.items()},
                         "skins_F_per_track": TOPUP_SKINS_F, "wordings": TOPUP_WORDINGS},
                "fixes": ["new items: chat / email / transcript cells could not reach 24 under the v1 plan",
                          "log brief: every word after the tag in lowercase (G-SL name lint unchanged)",
                          "ch_scope brief: 'which of the listed scopes' (wording lint unchanged)",
                          "yn_holder_other brief: 'other than' only (NEG_COUNTS unchanged)",
                          "top-up code path: topup.py writes haiku/redo2/, haiku/redo2/extract/ and pools_v2/ only"],
                "unchanged": "gates, lints, NEG_COUNTS, registry meanings, G0_SPEC.md, every v1 file",
                "audit": "a task agent may read only allowed_read (its task file; chunk and prompt are copies) and "
                         "write only allowed_write; audit.audit_jsonl discards a failed agent's answers",
                "next": "after every answer exists: topup.py extract-build (G-LEX 2/2 reads of the new forms), then "
                        "topup.py freeze (pools_v2/)",
                "tasks": tasks}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return files, manifest


def build(force: bool = False) -> dict:
    answers = ROOT2 / "answers"
    if answers.is_dir() and any(answers.iterdir()) and not force:
        raise SystemExit("redo2 answers already exist: refusing to rewrite the tasks (keys would no longer match)")
    files, manifest = files_for2(build_batches2())
    paths.write_files(ROOT2, files)
    return manifest


# ------------------------------------------------------------------------------------------------ loader (merged)

def _restore_from(root: Path, task: dict) -> CH.TaskBatch:
    key = json.loads((root / "key" / f"{task['batch_id']}.json").read_text(encoding="utf-8"))["key"]
    b = CH.TaskBatch(task["kind"], F, task["batch_id"], "", task["prompt_sha"], "")
    b.key = key
    chunk = json.loads((root / "chunks" / f"{task['task_id']}.json").read_text(encoding="utf-8"))
    b.chunks = [chunk]
    b.task_of = {it["qid"]: task["task_id"] for it in chunk["items"]}
    return b


def _load_task(root: Path, task: dict, raw, pools: dict, drops: list, only_qids=None, tag: str = "") -> list:
    """Map one task's answers back through its key and run haiku_author._load_one (the v1 loader lint) on each."""
    b = _restore_from(root, task)
    if only_qids is not None:
        raw = [a for a in raw if isinstance(a, dict) and a.get("qid") in only_qids] if isinstance(raw, list) else raw
    got, probs = CH.load_answers(b, {task["task_id"]: raw})
    if only_qids is not None:
        want = {b.key[q] for q in only_qids}
        probs = [p for p in probs if not p.endswith("item(s) unanswered")]
        missing = sorted(want - set(got))
        if missing:
            probs.append(f"{len(missing)} redo item(s) unanswered")
        got = {k: v for k, v in got.items() if k in want}
    drops += [(task["task_id"] + tag, "*", p) for p in probs]
    items = CH.item_by_internal(b)
    inv = {v: k for k, v in b.key.items()}
    loaded = []
    for iid, a in sorted(got.items()):
        why = HA._load_one(task, iid.split("|"), items[iid], a, inv[iid], pools)
        if why:
            drops.append((task["task_id"] + tag, iid, why))
        else:
            loaded.append(iid)
    return loaded


def load() -> dict:
    """v1 answers (haiku_author.load, unchanged) + the v1 redo answer + the redo2 answers -> merged pools and drops.
    Lexicon forms are added pending admission, never admitted here."""
    res = HA.load()
    pools, drops = res["pools"], list(res["drops"])
    v1_ids = {"skins": set(pools["skins"]), "attacks": set(pools["attacks"]), "wordings": set(pools["wordings"])}
    v1_forms = set(pools["lexicon"].forms)
    resolved, missing = [], list(res["missing"])

    # (a) the v1 redo answer, merged by qid into the v1 batch it belongs to
    v1_tasks = {t["task_id"]: t for t in json.loads((HA.ROOT / "TASKS.json").read_text(encoding="utf-8"))["tasks"]}
    for tid, qids in REDO1_ITEMS.items():
        ap = REDO1 / "answers" / f"{tid}.json"
        if not ap.is_file():
            missing.append(f"{tid} (haiku/redo)")
            continue
        v1_raw = json.loads(Path(v1_tasks[tid]["answer_file"]).read_text(encoding="utf-8"))
        if any(isinstance(a, dict) and a.get("qid") in qids for a in v1_raw):
            raise SystemExit(f"{tid}: the v1 answer already holds a redo qid; refusing to merge twice")
        try:
            raw = json.loads(ap.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            drops.append((f"{tid}:redo", "*", f"answer file is not JSON: {e}"))
            continue
        extra = [a.get("qid") for a in raw if isinstance(a, dict) and a.get("qid") not in qids] \
            if isinstance(raw, list) else ["(not a list)"]
        if extra:
            drops.append((f"{tid}:redo", "*", f"answers outside the redo item list ignored: {extra}"))
        _load_task(HA.ROOT, v1_tasks[tid], raw, pools, drops, only_qids=set(qids), tag=":redo")
        resolved.append(tid)
    if resolved:   # the v1 problems the redo answers (the mistyped qid and its unanswered item) are superseded
        drops = [d for d in drops if not (d[0] in resolved and d[1] == "*")]

    # (b) redo2
    man2_path = ROOT2 / "TASKS.json"
    tasks2 = json.loads(man2_path.read_text(encoding="utf-8"))["tasks"] if man2_path.is_file() else []
    for task in tasks2:
        ap = Path(task["answer_file"])
        if not ap.is_file():
            missing.append(task["task_id"])
            continue
        try:
            raw = json.loads(ap.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            drops.append((task["task_id"], "*", f"answer file is not JSON: {e}"))
            continue
        _load_task(ROOT2, task, raw, pools, drops)

    counts = {"skins_T": sum(s.author_mode == "T" for s in pools["skins"].values()),
              "skins_F": sum(s.author_mode == "F" for s in pools["skins"].values()),
              "attacks": len(pools["attacks"]), "wordings": len(pools["wordings"]),
              "lexicon_forms": len(pools["lexicon"].forms), "new_lexicon_forms": len(set(pools["lexicon"].forms)
                                                                                       - v1_forms),
              "dropped": sum(1 for d in drops if d[1] != "*"), "answer_problems": sum(1 for d in drops if d[1] == "*"),
              "tasks_missing": len(missing), "redo2_tasks": len(tasks2)}
    return {"pools": pools, "drops": drops, "missing": missing, "counts": counts, "v1_ids": v1_ids,
            "v1_forms": v1_forms, "resolved_by_redo": resolved, "tasks2": tasks2}


def dedup_merged(pools: dict, v1_ids: dict) -> list:
    """Exact-text dedup like extract_build.dedup, but the v1 pieces are kept first (a new piece never displaces a v1
    piece), then extract_build.dedup for packs and names (unchanged from v1)."""
    dropped = []
    for bucket in ("skins", "attacks"):
        seen: dict = {}
        order = sorted(p for p in pools[bucket] if p in v1_ids[bucket]) + \
            sorted(p for p in pools[bucket] if p not in v1_ids[bucket])
        for pid in order:
            k = EB._norm(pools[bucket][pid].text)
            if k in seen:
                dropped.append((f"{bucket}|{pid}", f"duplicate text of {seen[k]}"))
                del pools[bucket][pid]
            else:
                seen[k] = pid
    return dropped + EB.dedup(pools)


# ------------------------------------------------------------------------------------------------ G-LEX reads (r2)

def v1_read_fids() -> list:
    """The form ids the v1 reads covered (from the v1 extraction keys)."""
    man = json.loads((EB.EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    fids = set()
    for bid in sorted({t["batch_id"] for t in man["tasks"]}):
        fids |= set(json.loads((EB.EXTRACT / "key" / f"{bid}.json").read_text(encoding="utf-8"))["key"].values())
    return sorted(fids)


def extraction_batches2(reg, fids: list) -> list:
    """[(read name, TaskBatch)]: one make_batch per independent read of the NEW forms (own seeds; same item shape,
    meanings and prompt as the v1 reads)."""
    out = []
    for read in READS2:
        seed = f"{SEED_GLEX2}|{read}"
        items = EB.extraction_items(reg, fids, seed)
        b = CH.make_batch("extract_lex", F, items, seed=seed, prompt=EB.EXTRACT_PROMPT + EB.EXTRACT_TAIL,
                          max_items=EB.CHUNK)
        out.append((read, b))
    return out


def _extract_task_md(b, chunk: dict, answer: Path, read: str) -> str:
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    return (f"# T31 G-LEX extraction task {chunk['task_id']} ({read}, top-up)\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer}\n\n"
            f"Task kind: extract_lex; items: {n}; answers expected: {n} (one per item, answer field \"choice\").\n\n"
            "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
            "ANSWER CONTRACT (exact; a program checks it):\n"
            f"- One JSON array with exactly {n} objects, one per item; each object has exactly the keys \"qid\" and "
            "\"choice\".\n"
            "- \"qid\": copied character for character from its item (q followed by ten letters or digits).\n"
            "- \"choice\": one of the item's listed meanings, copied exactly, or null when none fits exactly.\n"
            "- Valid JSON only: no text before or after the array, no markdown code fences, no comments.\n"
            f"- The {n} qids of this task: {', '.join(qids)}\n\n"
            f"## Instructions\n\n{b.prompt}\n\n"
            "Answer format: [{\"qid\": \"<qid>\", \"choice\": \"<one meaning, copied exactly, or null>\"}, ...]\n\n"
            "## Items (JSON; answer every item once, keyed by its qid)\n\n"
            + json.dumps(chunk["items"], ensure_ascii=False, indent=1) + "\n")


def new_form_ids(st: dict) -> tuple:
    """(form ids that need a top-up read, unit-test failures among the new forms): every form with no v1 read whose
    unit test passes. Unit tests run on the merged registry (a new form that makes any form ambiguous fails here)."""
    reg = st["pools"]["lexicon"]
    ok, bad = EB.lexicon_review(reg)
    v1 = set(v1_read_fids())
    return [f for f in ok if f not in v1], [(f, r) for f, r in bad]


def extract_run(write: bool) -> dict:
    if write and EXTRACT2.exists() and any(EXTRACT2.iterdir()):
        raise SystemExit("haiku/redo2/extract already holds files: refusing to rewrite the reads")
    st = load()
    if write and (st["missing"] or not st["tasks2"]):
        raise SystemExit(f"author answers missing ({st['missing'][:4]}): write the reads once every top-up task "
                         "(and the v1 redo) is answered")
    reg = st["pools"]["lexicon"]
    fids, lex_bad = new_form_ids(st)
    files, tasks = {}, []
    if fids:
        for read, b in extraction_batches2(reg, fids):
            files.update(b.files())
            for c in b.chunks:
                tid = c["task_id"]
                answer = EXTRACT2 / b.answer_path(tid)
                text = _extract_task_md(b, c, answer, read)
                for iid in b.key.values():
                    if iid in text:
                        raise CH.ChunkError(f"{tid}: task file names an internal id")
                files[f"tasks/{tid}.md"] = text
                reads, writes = b.allowed(str(EXTRACT2), tid)
                tasks.append({"task": f"glex-{read}", "task_id": tid, "batch_id": b.batch_id, "kind": "extract_lex",
                              "read": read, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                              "task_file": str(EXTRACT2 / f"tasks/{tid}.md"), "answer_file": str(answer),
                              "allowed_read": sorted(reads | {str(EXTRACT2 / f"tasks/{tid}.md")}),
                              "allowed_write": sorted(writes)})
    manifest = {"family": F, "seed": SEED_GLEX2, "kind": "extract_lex", "reads": list(READS2), "n_tasks": len(tasks),
                "forms_for_admission": fids, "required_reads_per_form": 2,
                "new_forms_unit_fail": [{"form": f, "reason": r} for f, r in lex_bad],
                "note": "reads of every lexicon form with no v1 read (top-up wordings and the v1 redo wording); the v1 "
                        "forms keep their v1 reads, verified byte for byte at admission",
                "tasks": tasks,
                "answer_format": "[{\"qid\": ..., \"choice\": <meaning copied exactly, or null>}]"}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    if write:
        paths.write_files(EXTRACT2, files)
    return {"forms": len(fids), "unit_fail": lex_bad, "n_tasks": len(tasks), "written": write,
            "load_counts": st["counts"], "missing": st["missing"]}


# ------------------------------------------------------------------------------------------------ admission + freeze

def _verify_r2(reg, fids: list, manifest: dict) -> tuple:
    problems, batches = [], {}
    if sorted(fids) != sorted(manifest.get("forms_for_admission", [])):
        problems.append("the forms needing a top-up read differ from haiku/redo2/extract/TASKS.json")
    known = {t["batch_id"]: t["read"] for t in manifest.get("tasks", [])}
    for read, b in (extraction_batches2(reg, fids) if fids else []):
        batches[read] = b
        if known.get(b.batch_id) != read:
            problems.append(f"{read}: rebuilt batch id {b.batch_id} is not the redo2 TASKS.json batch for {read}")
        for rel, text in sorted(b.files().items()):
            p = EXTRACT2 / rel
            if not p.is_file():
                problems.append(f"{read}: {rel} is missing on disk")
            elif p.read_text(encoding="utf-8") != text:
                problems.append(f"{read}: {rel} differs from the rebuilt batch")
    return batches, problems


def _read_answers2(batches: dict, manifest: dict) -> tuple:
    raw_by_read, sha_by_task, problems = {}, {}, []
    for read in batches:
        raw = {}
        for t in manifest["tasks"]:
            if t["read"] != read:
                continue
            ap = EXTRACT2 / "answers" / f"{t['task_id']}.json"
            if not ap.is_file():
                problems.append(f"{t['task_id']}: answer file missing")
                continue
            data = ap.read_bytes()
            sha_by_task[t["task_id"]] = hashlib.sha256(data).hexdigest()
            try:
                raw[t["task_id"]] = json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                problems.append(f"{t['task_id']}: not valid JSON ({e})")
        raw_by_read[read] = raw
    return raw_by_read, sha_by_task, problems


def admit2() -> dict:
    st = load()
    pools, drops = st["pools"], st["drops"]
    reg = pools["lexicon"]
    q_rows, answer_problems = [], []
    for tid, iid, why in drops:
        if iid == "*":
            answer_problems.append({"task": tid, "why": why})
        else:
            q_rows.append({"piece": f"{tid}|{iid}", "stage": "load:G-SL", "reason": why})
    value_bad = EB.lint_pools(pools)
    q_rows += [{"piece": p, "stage": "value-lint", "reason": r} for p, r in value_bad]
    q_rows += [{"piece": p, "stage": "dedup", "reason": r} for p, r in dedup_merged(pools, st["v1_ids"])]

    # v1 reads: exactly the v1 batches, verified byte for byte, recorded under their v1 extractor ids
    v1_fids = v1_read_fids()
    man1 = json.loads((EB.EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    b1, p1 = GA._verify_reads(reg, v1_fids, man1)
    raw1, sha1, rp1 = GA._read_answers(b1, man1)
    c1, rec1 = GA._record(reg, b1, raw1)

    # top-up reads of every other form that passes its unit test
    new_fids, new_bad = new_form_ids(st)
    man2_path = EXTRACT2 / "TASKS.json"
    man2 = json.loads(man2_path.read_text(encoding="utf-8")) if man2_path.is_file() else {"tasks": []}
    b2, p2 = _verify_r2(reg, new_fids, man2)
    raw2, sha2, rp2 = _read_answers2(b2, man2)
    c2, rec2 = GA._record(reg, b2, raw2)
    reg.unit_test_all()

    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    q_rows += GA._form_quarantine(reg)
    for sid, (_sk, fid) in sorted(pools["wordings"].items()):
        if status_of[fid] != "admitted":
            q_rows.append({"piece": f"wording|{sid}", "stage": "G-LEX", "status": status_of[fid],
                           "reason": f"form {fid} is {status_of[fid]}"})
    return {"pools": pools, "reg": reg, "status_of": status_of, "quarantine": q_rows,
            "answer_problems": answer_problems, "answer_sha": {**sha1, **sha2},
            "read_counts": {**c1, **c2}, "batches": {**b1, **b2},
            "problems": {"rebuild_v1": p1, "rebuild_r2": p2, "answers_v1": rp1, "answers_r2": rp2,
                         "record_v1": rec1, "record_r2": rec2, "answer_drops": answer_problems,
                         "missing_author_answers": st["missing"]},
            "gate": reg.gate(), "new_unit_fail": new_bad, "resolved_by_redo": st["resolved_by_redo"],
            "new_forms": new_fids, "v1_fids": v1_fids, "tasks2": st["tasks2"]}


def manifest_v2(st: dict, c: dict, short: list, files: dict) -> dict:
    g0_sha = hashlib.sha256(GA.G0.read_bytes()).hexdigest()
    v1_man = HERE / "pools" / "MANIFEST.json"
    gate = st["gate"]
    clean = not short and gate["pass"] and not any(v for k, v in st["problems"].items() if k != "answer_drops")
    return {
        "family": F,
        "version": "freeze-v2",
        "status": ("FROZEN for G13-seed: every G0 target met and G-LEX passes; G13-seed still pending" if clean else
                   "PARTIAL: frozen with shortfalls, problems or quarantines (see shortfalls / problems); NOT for row "
                   "generation until they are cleared and G13-seed (6.4 step 4) runs on these pools"),
        "supersedes": {"path": "families/T31/pools/MANIFEST.json",
                       "sha256": hashlib.sha256(v1_man.read_bytes()).hexdigest() if v1_man.is_file() else None},
        "promote": "g13_c2 reads families/T31/pools/: move pools/ to pools_v1/, then pools_v2/ to pools/",
        "g0": {"path": "families/T31/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": g0_sha == P.POOL_G0_SHA256},
        "sources": {"v1_author": "haiku/author/", "v1_redo": sorted(REDO1_ITEMS), "topup_author": "haiku/redo2/",
                    "v1_reads": "haiku/extract/", "topup_reads": "haiku/redo2/extract/",
                    "resolved_by_redo": st["resolved_by_redo"]},
        "reads": {read: {"batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "tasks": {tid: st["answer_sha"][tid] for tid in sorted(st["answer_sha"])
                                   if tid.startswith(b.batch_id)}}
                  for read, b in sorted(st["batches"].items())},
        "answer_reads": st["read_counts"],
        "problems": st["problems"],
        "gates": {"G-LEX": {k: v for k, v in gate.items() if k != "not_admitted"},
                  "G-LEX_not_admitted_count": len(gate["not_admitted"]),
                  "G13_seed": "not run (6.4 step 4)", "G3-H": "not run at pool stage (6.4: pilot and full generation)"},
        "counts": c,
        "targets_g0": GA.G0_TARGETS,
        "shortfalls": short,
        "skins_by_register": {r: sum(v["total"] for k, v in c["skins_by_register_track"].items()
                                     if k.split("|")[0] == r) for r in sorted({k.split("|")[0]
                                                                              for k in c["skins_by_register_track"]})},
        "sha256": {name: hashlib.sha256(text.encode("utf-8")).hexdigest() for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)",
    }


def freeze_run(write: bool) -> dict:
    if write and (POOLS2 / "MANIFEST.json").exists():
        raise SystemExit("pools_v2/MANIFEST.json already exists: refusing to re-freeze")
    st = admit2()
    c = GA.counts(st)
    short = GA.shortfalls(c)
    files = GA._files(st, c, short)
    man = manifest_v2(st, c, short, files)
    files["MANIFEST.json"] = GA._dump(man)
    if write:
        paths.write_files(POOLS2, files)
    return {"counts": c, "shortfalls": short, "quarantine_rows": len(st["quarantine"]),
            "quarantine_by_stage": dict(Counter(q["stage"] for q in st["quarantine"])),
            "gate": {k: v for k, v in st["gate"].items() if k != "not_admitted"}, "problems": st["problems"],
            "read_counts": st["read_counts"], "status": man["status"], "written": write, "files": sorted(files)}


# ------------------------------------------------------------------------------------------------ CLI

def plan_report(manifest: dict) -> dict:
    """The projected cell counts: v1 freeze count + new items, against the G0 7 floor (no drop assumed)."""
    v1 = json.loads((HERE / "pools" / "MANIFEST.json").read_text(encoding="utf-8"))["counts"]
    cells = v1["skins_by_register_track"]
    add = Counter()
    for (t, r), n in TOPUP_SKINS_T.items():
        add[f"{r}|{t}"] += n
    for t in HA.TRACKS:
        for r, n in TOPUP_SKINS_F.items():
            add[f"{r}|{t}"] += n
    proj = {k: {"v1": cells.get(k, {}).get("total", 0), "new_items": add[k],
                "max": cells.get(k, {}).get("total", 0) + add[k],
                "may_lose": cells.get(k, {}).get("total", 0) + add[k] - GA.G0_TARGETS["skins_train_per_register_track"]}
            for k in sorted(add)}
    wc = v1["wordings_candidates_by_qform"]
    words = {q: {"v1": wc.get(q, 0), "new_items": n, "plan_v1": HA.WORDINGS[q]} for q, n in TOPUP_WORDINGS.items()}
    return {"n_tasks": manifest["n_tasks"], "items": manifest["items_expected"], "skin_cells": proj,
            "wordings": words, "wording_candidates_max": v1["wordings_candidates"] + 1 + sum(TOPUP_WORDINGS.values())}


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd == "check":
        _files, manifest = files_for2(build_batches2())
        print(json.dumps(plan_report(manifest), indent=1))
    elif cmd == "build":
        m = build(force="--force" in argv)
        print(json.dumps({"n_tasks": m["n_tasks"], "items_expected": m["items_expected"],
                          "tasks_json": str(ROOT2 / "TASKS.json"),
                          "tasks": [(t["task_file"], t["answer_file"], t["kind"]) for t in m["tasks"]]}, indent=1))
    elif cmd == "load":
        res = load()
        print(json.dumps(res["counts"], indent=1))
        for tid, iid, why in res["drops"]:
            if ":redo" in tid or tid.startswith(tuple(t["batch_id"] for t in res["tasks2"])):
                print(f"drop {tid} {iid}: {why}")
    elif cmd in ("extract-check", "extract-build"):
        print(json.dumps(extract_run(write=(cmd == "extract-build")), indent=1, default=str))
    elif cmd in ("admit-check", "freeze"):
        print(json.dumps(freeze_run(write=(cmd == "freeze")), indent=1, ensure_ascii=False, default=str))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
