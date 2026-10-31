"""families/T01/extract.py: the T01 Haiku EXTRACTION round after the authoring round (haiku/author/).

Runs after A38 only. Every write goes through paths.write_files / write_jsonl / write_json, which refuse before A38.
Steps (C2_DATA_SPEC 6.3 and 6.4; G0_SPEC 2 and 7; PREREG A37 (b), A38):
  1. collect  the 27 authoring answers (haiku_author.load_answers_for rebuilds the same batches and keys as the files on
              disk; chunker.load_answers maps every answer to its item). Each piece goes through the family's own
              check (G-SL lint_template / lint_freeform, the T01 word lists, negation counts, slot round trips).
              Nothing is written here.
  2. lint     extra G-SL passes on the pieces the authoring check does not lint:
              - pack values: gsl.lint_values over every value, read as a name slot (the round trip, braces, negation).
                A failing pack is dropped, with its reasons (lint_log.json).
              - window clauses and comparator phrases: gsl.lint_template (wording role) is run and its hits are FLAGS
                (gsl_flags, lint_log.json), not drops: lexicon clause slots are gated by G-LEX and the family check
                (gsl.lint_values skips clause slots), and G0 section 8 H9 / H12 require the words the lint flags.
                The decision is the orchestrator's; see the report.
  3. dedup    exact duplicates of the normalised text inside each pool (packs: the whole pack). The first copy is kept.
  4. lex      the surviving lexicon forms (window clauses, comparator phrases, question wordings) go into a
              LexiconRegistry with their declared meanings. Haiku source, with task id and prompt sha. Then the unit
              test (lexicon.unit_test). A form that fails is dropped with its problems.
  5. tasks    G-LEX extraction: one independent read per batch. Reads glex-r1 and glex-r2 cover every unit-tested form
              (2/2 for comparators and question wordings); glex-r3 covers the window forms only (3/3 for window
              rules). Each read is its own batch, so each read is its own chunk files.
              G3-H: one extraction read over every surviving Mode F document (G0_SPEC 2: "G-SL lint_freeform, then
              G3-H"). Its schema is the plugin's own extract_fields.
  6. write    haiku/extract/: tasks/, answers/ (empty until the agents write), chunks/, prompts/, key/, manifest/,
              TASKS.json; pool/ (the survivors and the registry, orchestrator side); lint_log.json (the drop reasons).

  ../.venv/bin/python -m families.T01.extract            (from lean/c2_build: dry run, prints counts, writes nothing)
  ../.venv/bin/python -m families.T01.extract --write    (after A38: writes the files above)
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from families.T01 import fixtures as FX  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
VERSION = "v1"
ROOT = HERE / "haiku" / "extract"
LABEL = tuple(P.T01.LABEL_WORDS)
NAME_ALLOW = tuple(P.T01.NAME_ALLOW)
LEX_CHUNK = 25                      # G-LEX items per chunk (the question items carry 26 choices each; chunker cap 50)
G3H_CHUNK = 40                      # G3-H items per chunk
# the comparator sems, declared exactly as haiku_author.lexicon_registry declares them
CMP_SEMS = (
    ("cmp.gt", "comparator", "strictly greater than the bound"),
    ("cmp.ge", "comparator", "greater than or equal to the bound"),
    ("cmp.lt", "comparator", "strictly less than the bound"),
    ("cmp.le", "comparator", "less than or equal to the bound"),
)
GROUPS = ("packs", "skins", "freeform", "wordings", "windows", "comparators")

AGENT_RULES = ("How to work: this task file is the only file you may open. Do not open, list or search any other file "
               "or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given "
               "at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \\\" and a "
               "line break as \\n.\n")
GLEX_PROMPT = AGENT_RULES + """
TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (a short
question, a rule clause or a comparison phrase, with its values already filled in) and CHOICES (a list of meanings).

Rules:
1. Use only the TEXT and its CHOICES. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen CHOICE exactly, character for character, from that item's own list. Never write a new meaning.
3. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
Copy each qid exactly.
"""

G3H_PROMPT = AGENT_RULES + """
TASK: READ ONE DOCUMENT and extract three fields from it. Each item gives a TEXT (a short free-form note: a memo, an
e-mail, a chat message, a ticket or a transcript) and a SCHEMA with three fields:
- person: the full personal name of the person who wrote the note or is named in it as the sender, copied exactly as
  written in the TEXT.
- ref: the reference code (letters, a hyphen and digits) for the file, case or notice, copied exactly as written in the
  TEXT.
- topic: the phrase that says what the note is about, copied exactly as written in the TEXT, without the word "the"
  in front of it.

Rules: copy exactly; do not correct spelling; do not infer anything; if a field is not in the TEXT, write NONE;
answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "person": "<name copied as written>", "ref": "<reference copied as written>",
  "topic": "<phrase copied as written>"}, ...]
Copy each qid exactly.
"""


def _g3h_fields() -> list:
    """The plugin's own G3-H schema (T01Plugin.extract_fields): person (name), ref (id), topic (str)."""
    return P.T01().extract_fields(None)


# ------------------------------------------------------------------------------------------------ helpers

def _norm(t) -> str:
    return " ".join(str(t).casefold().split())


def _rule(reason: str) -> str:
    """The rule a reason belongs to, for the counts (e.g. 'G-SL quantity', 'T01 word', 'duplicate')."""
    head = reason.split(":", 1)[0]
    if head.startswith("G-SL "):
        return " ".join(head.split()[:2])
    return head.split(" '")[0].split(" (")[0].strip()[:40]


# ------------------------------------------------------------------------------------------------ 1. collect

def _check_group(name: str, check) -> tuple:
    """(kept [(base, obj, meta)], drops [..]) for one authoring batch, with the family's own check. Mirrors
    haiku_author._loop, except that every reason is kept (the loader keeps four)."""
    b, plan, ans, probs = A.load_answers_for(name)
    if probs:
        raise SystemExit(f"{name}: answers do not map to their items: {probs[:3]}")
    kept, drops, seen = [], [], set()
    for iid, a in sorted(ans.items()):
        text = a.get("text") if isinstance(a, dict) else None
        tid = A._task_of(b, iid)
        meta = plan[iid]
        obj, reasons = check(iid, text, meta, tid, b.prompt_sha, seen)
        base = {"pid": iid, "group": name, "task_id": tid, "prompt_sha": b.prompt_sha,
                "held_out": bool(meta.get("held_out", False))}
        if reasons:
            drops.append({**base, "reasons": list(reasons)})
        else:
            kept.append((base, obj, meta))
    return kept, drops


def _check_packs() -> tuple:
    """Packs: haiku_author.validate_pack, then no name or vendor may repeat another pack (as load_packs does)."""
    b, plan, ans, probs = A.load_answers_for("packs")
    if probs:
        raise SystemExit(f"packs: answers do not map to their items: {probs[:3]}")
    kept, drops, seen = [], [], set()
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        tid = A._task_of(b, iid)
        meta = plan[iid]
        reasons = A.validate_pack(p)
        if not reasons and seen & {x.lower() for x in p["people"] + p["vendors"]}:
            reasons = ["a name or vendor repeats another pack"]
        base = {"pid": iid, "group": "packs", "task_id": tid, "prompt_sha": b.prompt_sha,
                "held_out": bool(meta.get("held_out", False))}
        if reasons:
            drops.append({**base, "reasons": list(reasons)})
            continue
        seen |= {x.lower() for x in p["people"] + p["vendors"]}
        kept.append((base, p, meta))
    return kept, drops


def collect() -> tuple:
    """({group: [piece dict]}, {group: authored count}, {group: [drops from the family's checks]})."""
    pieces, authored, check_drops = {}, {}, {}
    # the authored count is every answered item, before any check
    for name in ("packs", "skins", "freeform", "wordings", "windows", "comparators"):
        b, _plan, ans, _probs = A.load_answers_for(name)
        authored[name] = len(ans)
    kept, drops = _check_packs()
    pieces["packs"] = [{**base, "pack": p, "held_out": base["held_out"]} for base, p, _m in kept]
    check_drops["packs"] = drops
    for name, check in (("skins", A.check_skin), ("freeform", A.check_freeform), ("wordings", A.check_wording),
                        ("windows", A.check_lexicon), ("comparators", A.check_lexicon)):
        kept, drops = _check_group(name, check)
        check_drops[name] = drops
        out = []
        for base, obj, meta in kept:
            if name == "skins":
                out.append({**base, "text": obj.text, "register": meta["register"], "escape": meta["escape"],
                            "decl": dict(A.NARR)})
            elif name == "freeform":
                facts = meta["facts"]
                out.append({**base, "text": obj.text, "register": meta["register"], "facts": dict(facts),
                            "g3h_expect": {"person": facts["PERSON"], "ref": facts["REF"], "topic": facts["TOPIC"]}})
            elif name == "wordings":
                qform, text, slots, _tid, _psha = obj
                out.append({**base, "text": text, "lexkind": "question", "qform": qform,
                            "sem": LX.question_sem(FAMILY, qform), "slots": dict(slots)})
            else:
                sem, kind, text, slots, _tid, _psha = obj
                out.append({**base, "text": text, "lexkind": kind, "sem": sem, "slots": dict(slots)})
        pieces[name] = out
    return pieces, authored, check_drops


# ------------------------------------------------------------------------------------------------ 2. lint (G-SL)

def lint_clause(p: dict) -> list:
    """Window clauses and comparator phrases: the wording role of gsl.lint_template, with the label words."""
    sk = make_skin(p["pid"], FAMILY, p["text"], dict(p["slots"]), kind="wording", register="lexicon", escape="text",
                   author_mode="T", held_out=p["held_out"])
    return [f"{x.rule}: {x.detail}" for x in gsl.lint_template(sk, label_words=LABEL, exceptions={},
                                                              name_allow=NAME_ALLOW)]


def lint_pack(p: dict) -> list:
    """Every pack value read as a name slot, then gsl.lint_values (negation cue, parse-back, braces, line breaks)."""
    values = list(p["people"]) + list(p["topics"].values()) + [p["filing"]["action"], p["filing"]["event_a"],
                                                              p["filing"]["event_b"]] + list(p["perils"]) + \
        list(p["vendors"])
    out = []
    for i, v in enumerate(values):
        try:
            slot = S.name_slot(v)
        except Exception as e:  # noqa: BLE001
            out.append(f"value {v!r}: {str(e)[:60]}")
            continue
        out += [f"{x.rule}: {x.detail}" for x in gsl.lint_values({f"v{i}": slot})]
    return out


def lint_all(pieces: dict) -> tuple:
    """(survivors {group: [piece]}, drops [{pid, group, task_id, reasons}], clause flags [...]).

    Packs: lint_pack is a drop rule. Window clauses and comparator phrases: lint_clause is run and its hits are FLAGS,
    not drops. The reason is the kit's own design: gsl.lint_values skips clause slots and check_row lints only skin,
    wording and attack lines, so a lexicon clause is gated by G-LEX (2/2, 3/3) and the family check. The wording-role
    lint also hits words that G0 section 8 requires in the clauses (H9: win.later_anchor must name "later"; H12: the
    waiting clause says "next day"), and the CORE list does not allow those words to be excepted. Dropping every hit
    would remove the whole win.later_anchor family. The flags travel with the pieces (gsl_flags) for the orchestrator."""
    surv, drops, flags = {g: [] for g in pieces}, [], []
    for g, rows in pieces.items():
        for p in rows:
            if g == "packs":
                reasons = lint_pack(p["pack"])
                if reasons:
                    drops.append({"pid": p["pid"], "group": g, "task_id": p["task_id"], "reasons": reasons})
                else:
                    surv[g].append(p)
            elif g in ("windows", "comparators"):
                p["gsl_flags"] = lint_clause(p)
                surv[g].append(p)
                if p["gsl_flags"]:
                    flags.append({"pid": p["pid"], "group": g, "sem": p["sem"], "task_id": p["task_id"],
                                  "flags": p["gsl_flags"]})
            else:
                surv[g].append(p)
    return surv, drops, flags


# ------------------------------------------------------------------------------------------------ 3. dedup

def _key(g: str, p: dict) -> str:
    if g == "packs":
        return json.dumps(p["pack"], sort_keys=True)
    return _norm(p["text"])


def dedup_all(surv: dict) -> tuple:
    """Exact duplicates of the normalised text inside each pool (packs: the whole pack). The first copy is kept."""
    kept, drops = {}, []
    for g, rows in surv.items():
        seen, out = {}, []
        for p in rows:
            k = _key(g, p)
            if k in seen:
                drops.append({"pid": p["pid"], "group": g, "task_id": p["task_id"],
                              "reasons": [f"duplicate of {seen[k]}"]})
            else:
                seen[k] = p["pid"]
                out.append(p)
        kept[g] = out
    return kept, drops


# ------------------------------------------------------------------------------------------------ 4. lexicon

def build_registry(lex_rows: list) -> tuple:
    """(registry, {form id: row}, form drops). Declared sems as haiku_author.lexicon_registry; each surviving form is
    added as a Haiku source; then the unit test runs. A duplicate or malformed form is dropped with its reason."""
    reg = LX.LexiconRegistry(FAMILY)
    for sem, kind, meaning in CMP_SEMS:
        reg.declare(sem, kind, meaning)
    for sem, meaning in FX.WINDOW_SEMS:
        reg.declare(sem, "window", meaning)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(LX.question_sem(FAMILY, qf), "question", meaning)
    row_of, drops = {}, []
    for p in sorted(lex_rows, key=lambda r: r["pid"]):
        try:
            f = reg.add(p["text"], p["sem"], slots=p["slots"], source="haiku", family=FAMILY,
                        haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"])
            row_of[f.form_id] = p
        except LX.LexiconError as e:
            drops.append({"pid": p["pid"], "group": p["group"], "task_id": p["task_id"], "reasons": [f"form: {e}"]})
    reg.unit_test_all()
    for fid, p in row_of.items():
        f = reg.forms[fid]
        if not f.unit_ok:
            drops.append({"pid": p["pid"], "group": p["group"], "task_id": p["task_id"],
                          "reasons": [f"unit: {x}" for x in f.unit_problems[:3]]})
    return reg, row_of, drops


# ------------------------------------------------------------------------------------------------ 5. tasks

def glex_items(reg: LX.LexiconRegistry, ids: list, seed: str, instance: int) -> list:
    """Gold-free extraction items, as lexicon.lexicon_items builds them, with two changes: the filled instance is the
    `instance`-th sample whose slot values are pairwise distinct, and the choices are the kind's meanings in a seeded
    order. Each read uses another instance, so the three window reads never see the same filled text."""
    out = []
    for fid in sorted(ids):
        f = reg.forms[fid]
        combos = reg._samples(f)
        distinct = [c for c in combos if len({v.value for v in c.values()}) == len(c)] or combos
        vals = distinct[instance % len(distinct)]
        txt = reg.render(fid, vals)
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
        out.append((fid, {"text": txt, "choices": mean}))
    return out


def make_tasks(reg: LX.LexiconRegistry, freeform: list) -> tuple:
    """(batches [(read label, kind, batch)], counts). Each read is its own batch, so its own chunk files."""
    ok = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    win = [fid for fid in ok if reg.forms[fid].kind == "window"]
    batches = []
    for instance, (label, ids) in enumerate((("glex-r1", ok), ("glex-r2", ok), ("glex-r3", win))):
        seed = f"t01-extract-{VERSION}-{label}"
        items = glex_items(reg, ids, seed, instance)
        batches.append((label, "extract_lex",
                        chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=GLEX_PROMPT,
                                           max_items=LEX_CHUNK)))
    fields = _g3h_fields()
    g3_items = [(p["pid"], g3h.extraction_item(p["text"], fields)) for p in freeform]
    batches.append(("g3h-r1", "extract_g3h",
                    chunker.make_batch("extract_g3h", FAMILY, g3_items, seed=f"t01-extract-{VERSION}-g3h-r1",
                                       prompt=G3H_PROMPT, max_items=G3H_CHUNK)))
    counts = {"forms_unit_ok": len(ok), "forms_unit_fail": len(reg.forms) - len(ok),
              "forms_needing_admission_by_kind": dict(Counter(reg.forms[f].kind for f in ok)),
              "reads_per_form": {"window": 3, "comparator": 2, "question": 2},
              "glex_items": {label: sum(len(c["items"]) for c in b.chunks) for label, _k, b in batches[:3]},
              "g3h_items": len(g3_items)}
    return batches, counts


def task_text(root: Path, batch, chunk: dict, read: str) -> str:
    ans = root / batch.answer_path(chunk["task_id"])
    items = json.dumps(chunk["items"], ensure_ascii=False, indent=1)
    n = len(chunk["items"])
    return (f"# T01 extraction task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{ans}\n\n"
            f"Task kind: {chunk['kind']}; read: {read}; items: {n}; outputs expected: {n}.\n\n"
            f"{batch.prompt.rstrip()}\n\nITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def files_for(root: Path, batches: list) -> tuple:
    """({relative path: text} for paths.write_files, manifest)."""
    out, rows = {}, []
    for read, kind, b in batches:
        out.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            rel = f"tasks/{tid}.md"
            out[rel] = task_text(root, b, c, read)
            rows.append({"read": read, "kind": kind, "task_id": tid, "batch_id": b.batch_id,
                         "task_file": str(root / rel), "answer_file": str(root / b.answer_path(tid)),
                         "prompt_sha": b.prompt_sha, "n_items": len(c["items"]),
                         "outputs_expected": len(c["items"]), "audit_allowed_read": [str(root / rel)],
                         "audit_allowed_write": [str(root / b.answer_path(tid))]})
    manifest = {"family": FAMILY, "version": VERSION, "stage": "extract", "n_tasks": len(rows),
                "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per extraction task (see ../TASKS.json). Written "
                                 "only by the task agents.\n")
    return out, manifest


# ------------------------------------------------------------------------------------------------ run

def run(write: bool) -> dict:
    pieces, authored, check_drops = collect()
    surv, lint_drops, clause_flags = lint_all(pieces)
    surv, dup_drops = dedup_all(surv)
    lex_rows = surv["wordings"] + surv["windows"] + surv["comparators"]
    reg, row_of, form_drops = build_registry(lex_rows)
    batches, task_counts = make_tasks(reg, surv["freeform"])
    files, manifest = files_for(ROOT, batches)

    all_check_drops = [d for g in GROUPS for d in check_drops.get(g, [])]
    all_drops = all_check_drops + lint_drops
    reason_rules = Counter(_rule(r) for d in all_drops for r in d["reasons"])
    dropped_by = Counter(d["group"] for d in all_drops)
    counts = {
        "pieces_authored": sum(authored.values()),
        "pieces_authored_by_group": authored,
        "family_check_dropped_by_group": {g: len(check_drops.get(g, [])) for g in GROUPS},
        "extra_lint_dropped_by_group": dict(Counter(d["group"] for d in lint_drops)),
        "lint_dropped_total": len(all_drops),
        "lint_dropped_by_group": dict(dropped_by),
        "lint_drop_reasons_by_rule": dict(reason_rules.most_common()),
        "dedup_dropped_by_group": dict(Counter(d["group"] for d in dup_drops)),
        "dedup_dropped_total": len(dup_drops),
        "survivors_by_group": {g: len(surv.get(g, [])) for g in GROUPS},
        "survivors_total": sum(len(surv.get(g, [])) for g in GROUPS),
        "clause_gsl_flagged_not_dropped": {g: sum(1 for f in clause_flags if f["group"] == g)
                                           for g in ("windows", "comparators")},
        "clause_gsl_flagged_by_sem": dict(Counter(f["sem"] for f in clause_flags)),
        "clause_gsl_flag_reasons_by_rule": dict(Counter(_rule(r) for f in clause_flags for r in f["flags"])),
        "lexicon_rows_into_registry": len(lex_rows),
        "lexicon_form_drops": len(form_drops),
        "lexicon_forms_in_registry": len(reg.forms),
        "forms_by_kind": dict(Counter(f.kind for f in reg.forms.values())),
        "forms_unit_fail": len([f for f in reg.forms.values() if not f.unit_ok]),
        "forms_needing_admission": task_counts["forms_unit_ok"],
        "forms_needing_admission_by_kind": task_counts["forms_needing_admission_by_kind"],
        "reads_per_form": task_counts["reads_per_form"],
        "glex_items_per_read": task_counts["glex_items"],
        "g3h_items": task_counts["g3h_items"],
        "tasks": manifest["n_tasks"],
        "tasks_by_kind": dict(Counter(r["kind"] for r in manifest["tasks"])),
        "task_outputs_expected": manifest["outputs_expected"],
    }
    if write:
        paths.write_files(ROOT, files)
        paths.write_jsonl(ROOT / "pool" / "packs.jsonl", [_pool_row(p) for p in surv["packs"]])
        paths.write_jsonl(ROOT / "pool" / "skins.jsonl", [_pool_row(p) for p in surv["skins"]])
        paths.write_jsonl(ROOT / "pool" / "freeform.jsonl", [_pool_row(p) for p in surv["freeform"]])
        paths.write_jsonl(ROOT / "pool" / "wordings.jsonl", [_pool_row(p) for p in surv["wordings"]])
        paths.write_jsonl(ROOT / "pool" / "window_forms.jsonl", [_pool_row(p) for p in surv["windows"]])
        paths.write_jsonl(ROOT / "pool" / "comparator_forms.jsonl", [_pool_row(p) for p in surv["comparators"]])
        paths.write_json(ROOT / "pool" / "lexicon_registry.json", reg.to_json())
        paths.write_json(ROOT / "lint_log.json", {"counts": counts, "family_check_drops": all_check_drops,
                                                  "extra_lint_drops": lint_drops, "dedup_drops": dup_drops,
                                                  "clause_gsl_flags_not_dropped": clause_flags,
                                                  "form_drops": form_drops})
    return {"counts": counts, "tasks": [{"task_file": r["task_file"], "answer_file": r["answer_file"],
                                         "kind": r["kind"], "read": r["read"]} for r in manifest["tasks"]],
            "written": write}


def _pool_row(p: dict) -> dict:
    return {k: v for k, v in p.items() if not str(k).startswith("_")}


def main(argv: list) -> int:
    write = "--write" in argv
    res = run(write)
    print(json.dumps(res["counts"], indent=1, ensure_ascii=False))
    print(f"tasks: {len(res['tasks'])}; written: {res['written']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
