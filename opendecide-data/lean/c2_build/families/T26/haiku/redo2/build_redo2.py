"""families/T26/haiku/redo2/build_redo2.py: the two NEW T26 authoring tasks of G0_SPEC.md v1.1 section 7 (R1, R2).

  R1  training yn_fails wordings (pool "wording"): the first pass got 0 of 11 admitted, because its brief asked for
      "fails for the request" and banned any mention of unverifiable checks, while the declared G-LEX meaning
      (plugin.QUESTION_MEANINGS["yn_fails"], unchanged) is "fails on its provided record". This brief states the declared
      meaning and requires the scope phrase ("whose record is provided" / "on its provided record"), as yn_clears does
      (H1). Internal ids t26|wording|yn_fails|100-115 (the first pass used 000-011), so authoring_ingest._meta reads
      them unchanged.
  R2  held-out wordings for sampler S5 (pool "wording_heldout"): every question form, in styles the training task never
      used. Internal ids t26|wording_ho|<qform>|NNN (the held-out tag pattern of skin_ho / free_ho).

Writes task files only (no pool, wording, row or label): one self-contained text file per chunk (inline answer contract,
the exact answer path, the instructions and the gold-free items), plus the orchestrator-only key/, manifest/, prompts/ and
TASKS.json. Items come from c2_kit.chunker.make_batch (opaque qids, whitelisted fields, the family's question strings and
option texts refused). Every write goes through c2_kit.paths (A38 guard, never-open guard).

Run (from lean/c2_build):
  ../../.venv/bin/python families/T26/haiku/redo2/build_redo2.py --dry-run   # build and check, write nothing
  ../../.venv/bin/python families/T26/haiku/redo2/build_redo2.py             # write the task files
  ../../.venv/bin/python families/T26/haiku/redo2/build_redo2.py --check     # files on disk == the rebuild
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                 # .../families/T26/haiku/redo2
C2_BUILD = HERE.parents[3]                              # .../lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from families.T26 import author_tasks as AT  # noqa: E402
from families.T26 import plugin as P  # noqa: E402

VERSION = "redo2-v1"
FORBID = AT.FORBID_LEX            # the fixture question wordings and the option texts (never shown to Haiku)

# ------------------------------------------------------------------------------------------------ forms (G0 S17, sec 4)
NEG_LINE = AT.wording_prompt().split("\n")[13]          # the negation-word rule, verbatim from the first pass
assert NEG_LINE.startswith("- negation words are:"), NEG_LINE
NO_OUTCOME = "never write apply, reject, escalate or hold back, in any form (applied, rejection, escalated, held ...)"

# (type, meaning for the author, negation words, form rules); meanings mirror plugin.QUESTION_MEANINGS
FORMS = {
    "yn_apply": AT.WORDING_FORMS["yn_apply"],
    "yn_hold": AT.WORDING_FORMS["yn_hold"],
    "yn_not_apply": AT.WORDING_FORMS["yn_not_apply"],
    "yn_dneg_apply": ("yes/no question", "a double negation that still asks whether the agent should apply the requested "
                                         "change (a yes answer means the change goes ahead)", 2,
                      ["exactly two negation words, both \"not\" or \"n't\"",
                       "use the frame \"is it not the case that ... should not ...\" and keep the verb apply (\"... "
                       "should not apply ...\" or \"... should not be applied\"); never swap apply for block, skip, "
                       "stop, keep from or make",
                       "never use \"is it not true\", \"would it not\", \"fair to say\" or a tag question such as "
                       "\"isn't it true that ...\", whose meaning flips"]),
    "yn_fails": ("yes/no question", "asks whether at least one listed check fails on its provided record (only a check "
                                    "whose record is provided can fail)", 0,
                 ["you MUST keep the scope: write the exact phrase \"whose record is provided\" (as in \"a listed check "
                  "whose record is provided\") or the exact phrase \"on its provided record\"",
                  "write fail or fails, never \"fail to\"",
                  "never write verify, verified, verifiable or the words \"not provided\", and never mention a check "
                  "whose record is missing"]),
    "yn_clears": ("yes/no question", "asks whether every listed check whose record is provided passes for the request "
                                     "(checks whose record is not provided are left out)", 0,
                  ["you MUST write the exact phrase \"whose record is provided\"",
                   "no negation word (do not write \"not missing\")"]),
    "ch_verdict": ("which-question", "asks which outcome the request gets under the policy (what the agent should do "
                                     "with it)", 0,
                   ["never name or list the outcomes or options: " + NO_OUTCOME, "no \"or\""]),
    "ch_failing": ("which-question", "asks which listed check the request fails, allowing that it may fail none", 0,
                   ["use \"if any\" or a similar phrase without a negation word", "never name a specific check",
                    NO_OUTCOME]),
}
assert set(FORMS) == set(P.QUESTION_MEANINGS) == set(AT.WORDING_FORMS)

FAILS_COUNT = 16                       # R1: training yn_fails (floor 6 admitted 2/2, G0 section 4)
HELD_COUNTS = {"yn_apply": 6, "yn_hold": 6, "yn_not_apply": 6, "yn_dneg_apply": 10, "yn_fails": 6, "yn_clears": 6,
               "ch_verdict": 8, "ch_failing": 6}           # R2: floor 3 admitted per form; dneg kept 2 of 8 in pass 1
HELD_STYLES = ["address the agent as \"you\" (for example \"should you ...\", \"do you find ...\")",
               "use a passive construction where it fits",
               "open with \"Per the card,\" or \"By the card's rule,\"",
               "open with \"For request {REQ_ID},\"",
               "terse: as few words as the rules allow",
               "full and explicit: 16-24 words, without adding any condition",
               "name the request as \"the request filed as {REQ_ID}\" or \"the {REQ_ID} request\"",
               "a reviewer's checklist question, matter-of-fact"]
assert not set(HELD_STYLES) & set(AT.WORDING_STYLES)


def prompt(held: bool) -> str:
    lines = [
        AT.HEAD.replace("{FORMAT}", '{"qid": "<qid>", "text": "<the question>"}'),
        "",
        "SETTING: an AI agent at a company receives a change request (reference {REQ_ID}). A policy card lists "
        "provenance checks, and the packet holds a record for each listed check or says that its record is not "
        "provided in the packet. A listed check whose record is provided passes or fails on that record; a listed "
        "check whose record is not provided cannot be verified, so it neither passes nor fails. The card's rule: if a "
        "listed check fails, the request is rejected; otherwise, if a listed check cannot be verified, the request is "
        "escalated to a named contact; otherwise the change is applied. Rejecting or escalating a request holds its "
        "change back.",
        "TASK: for each item write ONE question that a reader of the card answers. The item gives the exact meaning "
        "the question must have, its type (yes/no or which-question), exactly how many negation words it has, a "
        "style, and its own rules.",
    ]
    if held:
        lines.append("These questions form a separate set, kept apart from the usual phrasings: follow each item's "
                     "style closely, so the question reads differently from the plainest way of asking it.")
    lines += [
        "Rules for every question:",
        "- one line ending with \"?\", 6-25 words;",
        "- contains the placeholder {REQ_ID} exactly once (e.g. \"request {REQ_ID}\"), and no other placeholder or "
        "brace;",
        NEG_LINE,
        "- no digits or number words (one, first, second ...), no time words (now, currently, today, already, yet), "
        "no hedges (probably, likely, seems), no names, no capitalised word mid-sentence;",
        "- keep the meaning exact: do not add or drop a condition, never list the answer options, and never name a "
        "specific check;",
        "- the item's rules come first: when its style clashes with them, drop that part of the style;",
        "- yes/no questions may use the card's words where they help: the agent, the request, the change, the policy, "
        "listed check, record, packet, apply, reject, escalate, hold back, pass, fail. Which-questions never use "
        "apply, reject, escalate or hold back.",
        "Before writing, check every question: {REQ_ID} exactly once, the exact negation count, and every rule of its "
        "item.",
    ]
    return "\n".join(lines)


def _item(qf: str, style: str) -> dict:
    typ, meaning, k, rules = FORMS[qf]
    return {"brief": f"Type: {typ}. Meaning (keep exactly): {meaning}. Negation words: exactly {k}. Style: {style}.",
            "slots": ["{REQ_ID}"], "rules": list(rules)}


def fails_items(rng) -> list:
    styles = rng.sample(AT.WORDING_STYLES, len(AT.WORDING_STYLES))
    return [(f"t26|wording|yn_fails|{100 + i:03d}", _item("yn_fails", styles[i % len(styles)]))
            for i in range(FAILS_COUNT)]


def held_items(rng) -> list:
    out = []
    for qf, n in HELD_COUNTS.items():
        styles = rng.sample(HELD_STYLES, len(HELD_STYLES))
        out += [(f"t26|wording_ho|{qf}|{i:03d}", _item(qf, styles[i % len(styles)])) for i in range(n)]
    return out


# ------------------------------------------------------------------------------------------------ task files

def task_text(task_id: str, kind: str, instructions: str, items: list, answer_file: str) -> str:
    n = len(items)
    lines = [
        f"TASK {task_id}  (kind {kind}, {n} items)",
        "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, search or write any other file. Create no other file.",
        "",
        f"answer_file (the exact path you must write, with the Write tool): {answer_file}",
        "",
        "=== ANSWER CONTRACT (exact) ===",
        f"Write ONE JSON array to answer_file, and nothing else in that file. The array has exactly {n} objects, one "
        "per item below, every qid exactly once.",
        "Each object has exactly two keys, \"qid\" and \"text\", in this shape (the angle-bracket parts are what you "
        "fill in):",
        "[",
        "  {\"qid\": \"<qid of item 1>\", \"text\": \"<the question you wrote for item 1>\"},",
        "  {\"qid\": \"<qid of item 2>\", \"text\": \"<the question you wrote for item 2>\"}",
        "]",
        f"(that sketch shows two objects; your file has {n}.) Copy each qid character for character from its item. "
        "\"text\" is a non-empty JSON string on one line (no line break).",
        "No other keys, no wrapper object, no markdown fence, no comments, no null, no skipped qid, no qid used twice, "
        "and no qid that is not in the items below.",
        "",
        "=== INSTRUCTIONS (complete; the same text every other task in this batch received) ===",
        instructions,
        "",
        f"=== ITEMS ({n}; one JSON object per line; every one needs an answer object with its qid) ===",
    ] + [json.dumps(it, ensure_ascii=False) for it in items]
    return "\n".join(lines) + "\n"


def build() -> tuple:
    """(files {relative path: text}, index rows): deterministic."""
    rng = random.Random(f"T26|author|{VERSION}")
    plan = [("wording", "R1", fails_items(rng), prompt(False), 16, f"t26-redo2-wording-yn_fails-{VERSION}"),
            ("wording_heldout", "R2", held_items(rng), prompt(True), 27, f"t26-redo2-wording_heldout-{VERSION}")]
    files, rows = {}, []
    for pool, ref, items, instr, size, seed in plan:
        b = chunker.make_batch("author_wording", P.FAMILY, items, seed=seed, prompt=instr, max_items=size,
                               forbid_strings=FORBID)
        files.update({k: v for k, v in b.files().items() if not k.startswith("chunks/")})
        by_internal = dict(items)
        for c in b.chunks:
            tid = c["task_id"]
            answer = str(HERE / "answers" / f"{tid}.json")
            tfile = HERE / f"{tid}.txt"
            if never_open(answer) or never_open(tfile):
                raise chunker.ChunkError(f"never-open path for {tid}")
            text = task_text(tid, b.kind, instr, c["items"], answer)
            AT._check_text(text, FORBID)
            if any(iid in text for iid in b.key.values()):
                raise chunker.ChunkError("a task file names an internal id")
            files[tfile.name] = text
            qforms = {}
            for it in c["items"]:
                qf = b.key[it["qid"]].split("|")[2]
                qforms[qf] = qforms.get(qf, 0) + 1
                assert by_internal[b.key[it["qid"]]]["brief"] == it["brief"]
            rows.append({"task_file": str(tfile), "answer_file": answer, "kind": "author", "task_kind": b.kind,
                         "pool": pool, "g0_ref": f"G0 section 7 {ref}", "held_out": pool == "wording_heldout",
                         "n_items": len(c["items"]), "items_per_qform": dict(sorted(qforms.items())),
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "key_file": str(HERE / "key" / f"{b.batch_id}.json")})
    files["TASKS.json"] = json.dumps({
        "family": P.FAMILY, "version": VERSION, "g0_sha256": P.T26Plugin.G0_SHA256_AUTHORED, "n_tasks": len(rows),
        "note": ("NEW authoring tasks (G0 v1.1 section 7: R1 training yn_fails wordings, R2 held-out wordings for "
                 "sampler S5). One fresh Haiku agent per task_file; it reads only that file and writes only its "
                 "answer_file. key/ and manifest/ are orchestrator-only. Answers set no label: each piece goes through "
                 "authoring_ingest.lint_wording (role wording, unchanged), dedup against every first-pass wording and "
                 "fixture stand-in (training and held-out together), the registry (held_out=True for pool "
                 "wording_heldout), then 2 independent G-LEX reads with the unchanged LEX_PROMPT and choices; only 2/2 "
                 "is admitted."),
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    return files, rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="build and check every task, write nothing")
    g.add_argument("--check", action="store_true", help="compare the files on disk with the rebuild, write nothing")
    a = ap.parse_args(argv)
    files, rows = build()
    if a.check:
        diffs = [rel for rel, text in sorted(files.items())
                 if not (HERE / rel).exists() or (HERE / rel).read_text(encoding="utf-8") != text]
        print(json.dumps({"files": len(files), "diffs": diffs}, indent=1))
        return 1 if diffs else 0
    if not a.dry_run:
        paths.write_files(HERE, files)
        paths.require_a38()
        paths.check_path(HERE / "answers").mkdir(exist_ok=True)
    print(json.dumps({"written": not a.dry_run, "n_tasks": len(rows),
                      "tasks": [{k: r[k] for k in ("task_file", "answer_file", "pool", "n_items", "items_per_qform")}
                                for r in rows]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
