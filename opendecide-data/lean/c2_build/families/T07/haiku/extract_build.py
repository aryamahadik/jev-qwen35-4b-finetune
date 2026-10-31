"""families/T07/haiku/extract_build.py: the T07 extraction pass after the Haiku authoring pass (G-LEX and G3-H).

Steps (G0_SPEC section 4 and 6; C2_DATA_SPEC 6.3; c2_build README "Haiku task flow" steps 1-3):
  1. authoring.collect(): load the 27 authoring answers and lint every piece (G-SL and the closed checks). A failing
     piece is dropped and logged with its reasons.
  2. dedup: normalised text within the text pool (skin, freeform, attack), within the lexicon (condition sentences and
     question wordings; the canonical forms come first) and packs by content. Duplicates are dropped and logged.
  3. registry: declare the sems and question sems, add the canonical forms (source claude) and the lint-clean Haiku
     forms and wordings (source haiku), then unit-test every form. A form that fails its unit test is dropped and logged.
  4. G-LEX tasks: every form that passes its unit test is read twice, by two independent read sets r1 and r2 (different
     seeds, so the item order and the choice order differ too). Each read is its own chunk files. The rule is 2/2 for
     every kind: T07 has no precedence or window kind (the 3/3 rule never arises here).
  5. G3-H tasks: every deduplicated, lint-clean Mode F text is one extract_g3h item (one read), with the plugin's
     extract_fields schema. Expected views (extract_view) are NOT written to any task; the orchestrator plan keeps the
     sems and the brief values for the compare step.
  6. Writes with paths.write_files (refuses before A38): haiku/extract/ (chunks, prompts, tasks, keys, manifests, the
     orchestrator plan under plan/) and the lint log under haiku/lint/.

  run (from lean/c2_build):  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python families/T07/haiku/extract_build.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

C2_BUILD = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import plugin as P  # noqa: E402

HERE = Path(__file__).resolve().parent            # .../c2_build/families/T07/haiku
ROOT = HERE / "extract"
LINT = HERE / "lint"
FAMILY = "T07"
VERSION = "v1"
READS = ("r1", "r2")                              # two independent reads, each its own chunk files (G-LEX 2/2)
POOL = ("skin", "freeform", "attack")             # one text pool: dedup across these three piece types
LEXICON = ("form", "wording")                     # one lexicon namespace: dedup across both, canonical first

LEX_PROMPT = """TASK: NAME THE MEANING OF EACH SHORT TEXT.

Each item has a "text" (one short sentence or one question, with a sample value already filled in) and a list of
"choices" (meanings). For each item, read the text on its own and pick the single choice whose meaning the text
expresses.

Rules:
- Copy the chosen choice exactly, character for character, as the "meaning" value. Do not change, shorten, translate
  or combine choices, and do not write a new meaning.
- If two choices seem close, pick the closer one. Always pick exactly one choice.
- Judge each item on its own. Do not compare it with other items, and do not use any other file or source.
- The text is the only evidence.

Output: one JSON array with exactly one object per item, keyed by the item's "qid":
[{"qid": "...", "meaning": "..."}]
No other keys, no comments, no text outside the JSON.
Write the whole answer with the Write tool to the ANSWER FILE named in your task file, and nowhere else."""

G3H_PROMPT = """TASK: FILL IN THE FIELDS OF ONE ADVERTISEMENT TEXT.

Each item has a "text" (a short advertisement; its fine print is one line that starts with a star, *) and a "schema"
(the fields to fill, each with a description and, for some, the choices allowed). Read the text on its own and fill
every field from the text only.

- "store": the name of the store that runs the advertisement, copied as written.
- a field ending in "_rule": copy one of its listed choices exactly. Use "absent" when the text states no rule of that
  kind.
- a field ending in "_bound": copy the value that the rule names, exactly as written in the text (a date, an amount, a
  category or a level name). Use null when the rule is absent.

Do not guess a value the text does not state. Do not correct spelling or change the wording. Judge each item on its own.

Output: one JSON array with exactly one object per item, keyed by the item's "qid":
[{"qid": "...", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}]
Use every schema field name exactly, and no other names. No text outside the JSON.
Write the whole answer with the Write tool to the ANSWER FILE named in your task file, and nowhere else."""


def norm(text: str) -> str:
    return " ".join(text.casefold().split())


def group(piece: str) -> str:
    return "pool" if piece in POOL else "lex" if piece in LEXICON else piece


def dedup(pieces: list, drops: list, seen: dict) -> list:
    """Keep the first piece (by piece_id) of each normalised text; log every later duplicate."""
    keep = []
    for p in sorted(pieces, key=lambda x: x["piece_id"]):
        v = p["value"]
        key = (group(p["meta"]["piece"]), norm(v) if isinstance(v, str) else json.dumps(v, sort_keys=True))
        if key in seen:
            drops.append({"piece_id": p["piece_id"], "piece": p["meta"]["piece"], "stage": "dedup",
                          "reason": f"duplicate of {seen[key]}"})
            continue
        seen[key] = p["piece_id"]
        keep.append(p)
    return keep


def build_registry(lex_pieces: list, drops: list) -> tuple:
    """The T07 G-LEX registry, as authoring.build_registry, but every refused form is logged instead of skipped."""
    reg = LexiconRegistry(FAMILY)
    origin = {}
    for sem, (_dim, _op, kind, meaning) in P.SEMS.items():
        reg.declare(sem, kind, meaning)
    for qf, meaning in A.Q_SEM_MEANING.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    reg.declare_antonym(question_sem(FAMILY, "yn_gets"), question_sem(FAMILY, "yn_misses"))
    for sem, forms in A.CANON_FORMS.items():
        for text in forms:
            f = reg.add(text, sem, slots={"X": P.BOUND_KIND[P.SEMS[sem][0]]}, family=FAMILY)
            origin[f.form_id] = {"origin": "canonical", "piece_id": None}
    for p in lex_pieces:
        m = p["meta"]
        try:
            if m["piece"] == "form":
                f = reg.add(p["value"], m["sem"], slots={"X": P.BOUND_KIND[P.SEMS[m["sem"]][0]]}, source="haiku",
                            family=FAMILY, haiku_task_id=p["task_id"], haiku_prompt_sha=p["haiku_prompt_sha"])
                origin[f.form_id] = {"origin": "haiku_form", "piece_id": p["piece_id"]}
            else:
                f = reg.add(p["value"], question_sem(FAMILY, m["qform"]), slots=A.wording_slots(m["qform"]),
                            source="haiku", family=FAMILY, haiku_task_id=p["task_id"],
                            haiku_prompt_sha=p["haiku_prompt_sha"], held_out=m["held_out"])
                origin[f.form_id] = {"origin": "haiku_wording", "piece_id": p["piece_id"], "qform": m["qform"],
                                     "held_out": m["held_out"]}
        except LexiconError as e:
            drops.append({"piece_id": p["piece_id"], "piece": m["piece"], "stage": "registry", "reason": str(e)})
    reg.unit_test_all()
    return reg, origin


def lex_batch(reg, fids: list, read: str):
    seed = {"r1": "glex-r1", "r2": "glex-r2"}[read]
    items = reg.lexicon_items(fids, seed=f"t07-extract-{VERSION}-{seed}")
    return chunker.make_batch("extract_lex", FAMILY, items, seed=f"t07-extract-{VERSION}-{read}", prompt=LEX_PROMPT)


def g3h_batch(freeform: list):
    fields = P.T07Plugin.extract_fields(None, None)      # the schema does not depend on the spec (plugin.py)
    items = [(p["piece_id"], g3h.extraction_item(p["value"], fields)) for p in freeform]
    return chunker.make_batch("extract_g3h", FAMILY, items, seed=f"t07-extract-{VERSION}-g3h", prompt=G3H_PROMPT)


def task_text(batch, task_id: str, read: str, root: Path) -> str:
    chunk = next(c for c in batch.chunks if c["task_id"] == task_id)
    items = json.dumps(chunk["items"], ensure_ascii=False, indent=1)
    answer = root / batch.answer_path(task_id)
    return (f"# T07 extraction task {task_id}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer}\n\n"
            f"Task kind: {batch.kind}; read {read}; items: {len(chunk['items'])}; outputs expected: "
            f"{len(chunk['items'])}.\n\n"
            f"{batch.prompt.rstrip()}\n\n"
            f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def batch_files(batch, read: str, root: Path) -> tuple:
    out = dict(batch.files())               # prompt, chunks, key (orchestrator only), manifest
    rows = []
    for c in batch.chunks:
        tid = c["task_id"]
        tfile = root / "tasks" / f"{tid}.md"
        text = task_text(batch, tid, read, root)
        out[str(tfile.relative_to(root))] = text
        read_set = {str(tfile)} | batch.allowed(str(root), tid)[0]
        rows.append({"task": f"{read}-{batch.kind}", "task_id": tid, "kind": batch.kind, "read": read,
                     "batch_id": batch.batch_id, "prompt_sha": batch.prompt_sha, "task_file": str(tfile),
                     "answer_file": str(root / batch.answer_path(tid)), "n_items": len(c["items"]),
                     "outputs_expected": len(c["items"]),
                     "task_sha256": chunker.sha(text), "allowed_read": sorted(read_set),
                     "allowed_write": [str(root / batch.answer_path(tid))]})
    return out, rows


def main() -> int:
    res = A.collect()
    if res["problems"]:
        print("\n".join(res["problems"]))
        return 1
    pieces = res["pieces"]
    counts = Counter(p["meta"]["piece"] for p in pieces)

    # 1. lint drops (G-SL and the closed checks; never loosened)
    lint_drops = [{"piece_id": p["piece_id"], "task_id": p["task_id"], "piece": p["meta"]["piece"],
                   "register": p["meta"].get("register"), "stage": "lint", "reason": p["lint"]}
                  for p in pieces if p.get("lint")]
    ok = [p for p in pieces if not p.get("lint")]

    # 2. dedup (the canonical forms take their text first, so a Haiku copy of a canonical form is dropped)
    drops: list = []
    seen = {("lex", norm(t)): f"canonical {sem}" for sem, forms in A.CANON_FORMS.items() for t in forms}
    packs = dedup([p for p in ok if p["meta"]["piece"] == "pack"], drops, {})
    pool = dedup([p for p in ok if group(p["meta"]["piece"]) == "pool"], drops, {})
    lex = dedup([p for p in ok if group(p["meta"]["piece"]) == "lex"], drops, seen)
    dedup_pool_keys = {p["piece_id"] for p in pool}

    # 3. registry and unit tests
    reg_drops: list = []
    reg, origin = build_registry(lex, reg_drops)
    unit_fail = [{"form_id": fid, "origin": origin.get(fid), "text": f.text, "stage": "unit_test",
                  "reason": f.unit_problems[:3]}
                 for fid, f in sorted(reg.forms.items()) if not f.unit_ok]
    fids = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    by_origin = Counter(origin[fid]["origin"] for fid in fids)

    # 4. G-LEX reads: two independent chunk sets over the same unit-test-clean forms
    lex_batches = {r: lex_batch(reg, fids, r) for r in READS}

    # 5. G3-H reads: every lint-clean, deduplicated Mode F text
    freeform = sorted((p for p in pool if p["meta"]["piece"] == "freeform"), key=lambda p: p["piece_id"])
    g3 = g3h_batch(freeform)

    # 6. writes (guarded; refuse before A38)
    files: dict = {}
    rows: list = []
    for r in READS:
        f, rr = batch_files(lex_batches[r], r, ROOT)
        files.update(f)
        rows += rr
    f, rr = batch_files(g3, "g3h", ROOT)
    files.update(f)
    rows += rr

    plan = {"family": FAMILY, "version": VERSION, "note": "orchestrator side only; never sent to Haiku",
            "reads": {r: lex_batches[r].batch_id for r in READS} | {"g3h": g3.batch_id},
            "lex": {fid: {**origin[fid], "sem": reg.forms[fid].sem_id, "kind": reg.forms[fid].kind,
                          "meaning": reg.sems[reg.forms[fid].sem_id].meaning, "text": reg.forms[fid].text,
                          "held_out": reg.forms[fid].held_out}
                    for fid in fids},
            "g3h": {p["piece_id"]: {"register": p["meta"]["register"], "held_out": p["meta"]["held_out"],
                                    "sems": p["meta"]["sems"], "canon_forms": p["meta"]["canon_forms"],
                                    "conditions": [{"sem": s, "dim": P.SEMS[s][0], "rule": P.SEMS[s][1],
                                                    "bound_slot": "P1_" + P.SEMS[s][0].upper(),
                                                    "bound_as_written": p["meta"]["brief"]["P1_" + P.SEMS[s][0].upper()]}
                                                   for s in p["meta"]["sems"]],
                                    "decl": p["meta"]["decl"], "store_as_written": p["meta"]["brief"]["STORE"]}
                    for p in freeform}}
    manifest = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED,
                "gate": {"G-LEX": "2/2 (no precedence or window kind in T07)", "G3-H": "one read, >= 98% per register"},
                "n_tasks": len(rows), "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    files["plan/EXTRACT_PLAN.json"] = json.dumps(plan, ensure_ascii=False, indent=1) + "\n"
    paths.write_files(ROOT, files)

    summary = {
        "pieces_authored": len(pieces), "pieces_by_type": dict(counts),
        "lint_dropped": len(lint_drops), "lint_dropped_by_type": dict(Counter(d["piece"] for d in lint_drops)),
        "lint_passed_by_type": dict(Counter(p["meta"]["piece"] for p in ok)),
        "dedup_dropped": len([d for d in drops if d["stage"] == "dedup"]),
        "dedup_dropped_by_type": dict(Counter(d["piece"] for d in drops)),
        "pool_after_dedup": dict(Counter(p["meta"]["piece"] for p in pool)),
        "packs_after_dedup": len(packs),
        "registry_refused": len(reg_drops), "registry_refused_reasons": Counter(d["reason"][:60] for d in reg_drops).most_common(5),
        "unit_test_failed": len(unit_fail),
        "forms_needing_admission": len(fids), "forms_by_origin": dict(by_origin),
        "g_lex_read_items": {r: len(lex_batches[r].key) for r in READS},
        "g_lex_chunks": {r: len(lex_batches[r].chunks) for r in READS},
        "g3h_items": len(g3.key), "g3h_chunks": len(g3.chunks),
        "tasks_total": len(rows),
        "freeform_lint_dropped": sum(1 for d in lint_drops if d["piece"] == "freeform"),
    }
    log = {"family": FAMILY, "version": VERSION, "summary": summary, "lint_drops": lint_drops,
           "dedup_drops": [d for d in drops], "registry_refused": reg_drops, "unit_test_failed": unit_fail}
    paths.write_files(LINT, {"T07_extract_lint_log.json": json.dumps(log, ensure_ascii=False, indent=1,
                                                                    default=str) + "\n"})
    print(json.dumps(summary, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
