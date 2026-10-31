"""families/T32/extract.py: the T32 Haiku EXTRACTION round after the authoring round (haiku/author/).

Runs after A38 only. Every write goes through paths.write_files / write_jsonl / write_json, which refuse before A38.
Steps (C2_DATA_SPEC 6.3 and 6.4; G0_SPEC 1 R13, 7; PREREG A37 (b), A38):
  1. collect  the 28 authoring answers through authoring.load() (the family loader: answers -> pieces, each piece keeps
              its problems). Nothing is written here.
  2. lint     G-SL per piece. authoring.load() runs the family checks on every piece: gsl.lint_template for Mode T skins,
              attack lines and question wordings, gsl.lint_freeform (fact-lock) for Mode F intros, check_message for the
              message forms and check_pack for the packs. A piece with any problem is dropped and its reasons logged.
              gsl.lint_values is also run on the authoring slot samples (a sanity check; Haiku writes no values).
  3. dedup    exact duplicates of the normalised text inside each text pool (the first copy is kept). Duplicate
              lexicon forms are dropped by authoring.registry() (duplicate form text).
  4. lex      the surviving message forms and question wordings go into a LexiconRegistry (authoring.registry):
              Haiku source, unit tested. T32 has no precedence or window kinds, so every form needs 2/2.
  5. tasks    G-LEX extraction: one independent read per batch (glex-r1, glex-r2); each read is its own batch, so each
              read is its own chunk files. G3-H: one extraction read per surviving Mode F intro (G0_SPEC R13: "G-SL
              fact-lock + G3-H on those two"). The G3-H expected facts stay on the orchestrator side (pool/).
  6. write    haiku/extract/: chunks/ (each chunk is the whole task: answer_file, instructions, items), answers/ (empty
              until the agents write), prompts/, key/, manifest/, TASKS.json, registry.json, pool/ (survivors and
              expectations, orchestrator side), lint_log.json (the drop reasons).

  ../../.venv/bin/python -m families.T32.extract            (from lean/c2_build: dry run, prints counts, writes nothing)
  ../../.venv/bin/python -m families.T32.extract --write    (after A38: writes the files above)
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
from families.T32 import authoring as A  # noqa: E402
from families.T32 import plugin as P  # noqa: E402
from families.T32 import vocab as V  # noqa: E402

FAMILY = "T32"
VERSION = "v1"
ROOT = HERE / "haiku" / "extract"
POOL_ROOT = ROOT / "pool"
NONE_OF_THESE = "none of these"
READS = ("glex-r1", "glex-r2")                     # G-LEX: 2/2 for every kind (no precedence or window forms in T32)
TEXT_POOLS = ("skins", "skins_held", "attack_notes", "freeform", "freeform_held", "packs")
LEX_POOLS = ("message_forms", "wordings")
TOPIC_KEY = {surface: key for key, surface in V.TOPICS.items()}
TOPIC_SURFACES = {key: (surface,) for key, surface in sorted(V.TOPICS.items())}

AGENT_RULES = ("How to work: this chunk file is the only file you may open. Do not open, list or search any other file "
               "or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given "
               "in this file's \"answer_file\" field, with the Write tool. Inside JSON strings, write a double quote as "
               "\\\" and a line break as \\n. Read no other file and run no other tool.\n")

GLEX_PROMPT = AGENT_RULES + """
TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (one chat
message or one question about a promise in a group chat, with its sample values already filled in) and CHOICES (a list
of possible meanings, ending with "none of these").

Rules:
1. Use only the TEXT and its CHOICES. Do not add a condition, a default or any fact from outside the text.
2. Copy the chosen CHOICE exactly, character for character, from that item's own list. Never write a new meaning.
3. If no choice states exactly what the text means, copy "none of these".
4. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
Copy each qid exactly.
"""

G3H_PROMPT = AGENT_RULES + """
TASK: READ ONE DOCUMENT and extract two fields from it. Each item gives a TEXT (a short free-form intro of one or two
sentences, with its values filled in) and a SCHEMA with two fields:
- topic: what the chat is about, as the TEXT names it. Its CHOICES are listed in the schema. Copy the one choice the TEXT
  names, exactly as written in the choices. If the TEXT names none of them, write NONE.
- owner: the first name of the person the TEXT says saved or shared the chat, copied exactly as written. If the TEXT
  names no such person, write NONE.

Rules: copy exactly; do not correct spelling; do not infer anything from outside the text; answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "topic": "<one choice, or NONE>", "owner": "<name copied as written, or NONE>"}, ...]
Copy each qid exactly.
"""

G3H_FIELDS = (
    g3h.Field("topic", "category", "what the chat is about, as the text names it",
              S.category_slot("house_move", TOPIC_SURFACES).params),
    g3h.Field("owner", "name", "the person who saved or shared the chat"),
)


# ------------------------------------------------------------------------------------------------ helpers

def _text(p: dict) -> str:
    return p["out"] if isinstance(p["out"], str) else json.dumps(p["out"], sort_keys=True)


def _norm(t: str) -> str:
    return " ".join(t.casefold().split())


def g3h_expect(p: dict) -> dict:
    """The generator's facts for one Mode F intro (orchestrator side only; never sent to Haiku)."""
    return {"topic": TOPIC_KEY[p["facts"]["TOPIC"]], "owner": p["facts"]["OWNER"]}


# ------------------------------------------------------------------------------------------------ 1. collect

def collect() -> tuple:
    """({pool: [piece]}, {pool: authored count}). Pieces are the authoring.load() outputs."""
    loaded = A.load()
    pools, authored = {}, Counter()
    for tid, rec in sorted(loaded.items()):
        if rec["problems"]:
            raise SystemExit(f"{rec['label']}: task-level problems {rec['problems'][:3]}")
        for p in rec["pieces"]:
            q = dict(p)
            q["pool"] = rec["pool"]
            q["label"] = rec["label"]
            pools.setdefault(rec["pool"], []).append(q)
            authored[rec["pool"]] += 1
    return pools, dict(authored)


# ------------------------------------------------------------------------------------------------ 2. lint (G-SL)

def lint_all(pools: dict) -> tuple:
    """(survivors {pool: [piece]}, drops [{pid, pool, task_id, reasons}]). A piece that the family checks flagged is
    dropped with its reasons. The checks are the G-SL pass of the authoring loader (see the module docstring)."""
    surv, drops = {}, []
    for pool, pieces in pools.items():
        keep = []
        for p in pieces:
            if p["ok"] and p.get("out") is not None:
                keep.append(p)
            else:
                drops.append({"pid": p["iid"], "pool": pool, "task_id": p["task_id"],
                              "reasons": list(p["problems"]) or ["no output"]})
        surv[pool] = keep
    return surv, drops


def lint_values_samples() -> list:
    """gsl.lint_values on the authoring slot samples (name and topic values). Expected empty."""
    return [f"{v.rule}: {v.detail}" for v in gsl.lint_values(A._sample_slots())]


# ------------------------------------------------------------------------------------------------ 3. dedup

def dedup_all(surv: dict) -> tuple:
    """Exact duplicates of the normalised text inside each text group (skins with skins_held, freeform with
    freeform_held, attack_notes, packs). The first copy is kept. Lexicon forms are deduplicated by the registry."""
    group = {"skins": "skins", "skins_held": "skins", "freeform": "freeform", "freeform_held": "freeform",
             "attack_notes": "attack_notes", "packs": "packs"}
    kept, drops = {}, []
    seen = {}
    for pool in TEXT_POOLS:
        out = []
        for p in surv.get(pool, []):
            k = (group[pool], _norm(_text(p)))
            if k in seen:
                drops.append({"pid": p["iid"], "pool": pool, "task_id": p["task_id"],
                              "reasons": [f"duplicate of {seen[k]}"]})
            else:
                seen[k] = p["iid"]
                out.append(p)
        kept[pool] = out
    for pool in LEX_POOLS:
        kept[pool] = list(surv.get(pool, []))
    return kept, drops


# ------------------------------------------------------------------------------------------------ 4. lexicon

def build_registry(lex_pieces: list) -> tuple:
    """(registry, form drops). authoring.registry() adds each piece as a Haiku form (duplicates and bad placeholders are
    refused there) and runs the unit test on every form. Only forms whose unit test passes go on to extraction."""
    reg = A.registry(lex_pieces)
    drops = [{"pid": p["iid"], "pool": p["pool"], "task_id": p["task_id"], "reasons": list(p["problems"])}
             for p in lex_pieces if not p["ok"]]
    return reg, drops


# ------------------------------------------------------------------------------------------------ 5. tasks

def glex_items(reg: LX.LexiconRegistry, ids: list, seed: str, instance: int) -> list:
    """Gold-free extraction items as lexicon.lexicon_items builds them, with two changes: the filled instance is the
    `instance`-th sample whose slot values are pairwise distinct (each read sees other values), and the choices are the
    kind's meanings in a seeded order. Each read uses another instance and another order."""
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


def _finish(batch: chunker.TaskBatch, root: Path) -> chunker.TaskBatch:
    """Each chunk file is the whole task: answer_file, instructions (the batch prompt + the exact answer path), items."""
    out = []
    for c in batch.chunks:
        ans = str(Path(root) / batch.answer_path(c["task_id"]))
        if paths.never_open(ans):
            raise chunker.ChunkError(f"answer path is on the never-open list: {ans}")
        out.append({"task_id": c["task_id"], "kind": c["kind"], "answer_file": ans,
                    "instructions": batch.prompt + f"\n\nANSWER FILE (write exactly this path): {ans}",
                    "prompt_sha": c["prompt_sha"], "items": c["items"]})
    batch.chunks = out
    return batch


def make_tasks(reg: LX.LexiconRegistry, g3_pieces: list) -> tuple:
    """(batches [(read label, kind, batch)], counts). Each read is its own batch, so its own chunk files."""
    ok = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    strict = [fid for fid in ok if reg.forms[fid].kind in LX.STRICT_KINDS]
    batches = []
    for instance, label in enumerate(READS):
        items = [(fid, {"text": it["text"], "choices": it["choices"] + [NONE_OF_THESE]})
                 for fid, it in glex_items(reg, ok, f"t32-extract-{VERSION}-{label}", instance)]
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"t32-extract-{VERSION}-{label}", prompt=GLEX_PROMPT)
        batches.append((label, "extract_lex", _finish(b, ROOT)))
    g3_items = [(p["iid"], g3h.extraction_item(_text(p), list(G3H_FIELDS))) for p in g3_pieces]
    b = chunker.make_batch("extract_g3h", FAMILY, g3_items, seed=f"t32-extract-{VERSION}-g3h-r1", prompt=G3H_PROMPT)
    batches.append(("g3h-r1", "extract_g3h", _finish(b, ROOT)))
    counts = {"forms_unit_ok": len(ok), "forms_strict_3_of_3": len(strict),
              "forms_needing_admission_by_kind": dict(Counter(reg.forms[f].kind for f in ok)),
              "glex_items_per_read": len(ok), "g3h_items": len(g3_items)}
    return batches, counts


def files_for(batches: list) -> tuple:
    """({relative path: text} for paths.write_files, manifest)."""
    out, rows = {}, []
    for read, kind, b in batches:
        out.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            allowed = b.allowed(str(ROOT), tid)
            rows.append({"read": read, "kind": kind, "task_id": tid, "batch_id": b.batch_id,
                         "task_file": str(ROOT / b.chunk_path(tid)), "answer_file": str(ROOT / b.answer_path(tid)),
                         "prompt_sha": b.prompt_sha, "n_items": len(c["items"]),
                         "outputs_expected": len(c["items"]), "allowed_read": sorted(allowed[0]),
                         "allowed_write": sorted(allowed[1])})
    manifest = {"family": FAMILY, "version": VERSION, "stage": "extract", "g0_sha256": P.T32.G0_SHA256,
                "n_tasks": len(rows),
                "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per extraction task (see ../TASKS.json). "
                                 "Written only by the task agents.\n")
    return out, manifest


# ------------------------------------------------------------------------------------------------ self-checks

def self_check() -> list:
    """The G3-H expectation must read back as a match through g3h.compare, and the topic must canonicalise to its key."""
    probs = []
    cat = S.canonical(S.category_slot("house_move", TOPIC_SURFACES))
    if cat != "house_move":
        probs.append(f"topic canonical {cat!r} != key")
    exp = {"topic": "house_move", "owner": "Priya"}
    ok, diffs = g3h.compare(exp, {"topic": V.TOPICS["house_move"], "owner": "Priya"}, list(G3H_FIELDS))
    if not ok:
        probs.append(f"g3h compare of a correct read fails: {diffs}")
    ok, _ = g3h.compare(exp, {"topic": "NONE", "owner": "Priya"}, list(G3H_FIELDS))
    if ok:
        probs.append("g3h compare accepts NONE for a topic")
    return probs


# ------------------------------------------------------------------------------------------------ run

def run(write: bool) -> dict:
    probs = self_check()
    if probs:
        raise SystemExit("self-check failed: " + "; ".join(probs))
    pools, authored = collect()
    surv, lint_drops = lint_all(pools)
    sample_probs = lint_values_samples()
    surv, dup_drops = dedup_all(surv)
    lex_in = surv.pop("message_forms", []) + surv.pop("wordings", [])
    reg, form_drops = build_registry(lex_in)
    lex_ok = [p for p in lex_in if p["ok"]]
    bad_unit = [f.form_id for f in reg.forms.values() if not f.unit_ok]
    if bad_unit:
        raise SystemExit(f"forms failing the unit test: {bad_unit[:3]}")
    surv["lexicon"] = lex_ok
    g3_pieces = surv.get("freeform", []) + surv.get("freeform_held", [])
    batches, task_counts = make_tasks(reg, g3_pieces)
    files, manifest = files_for(batches)

    rules = Counter(r.split(":", 1)[0] for d in lint_drops for r in d["reasons"])
    counts = {
        "pieces_authored": sum(authored.values()),
        "pieces_authored_by_pool": authored,
        "lint_dropped_by_pool": dict(Counter(d["pool"] for d in lint_drops)),
        "lint_dropped_total": len(lint_drops),
        "lint_drop_reasons_by_rule": dict(rules.most_common()),
        "gsl_lint_values_on_authoring_samples_problems": len(sample_probs),
        "dedup_dropped_by_pool": dict(Counter(d["pool"] for d in dup_drops)),
        "dedup_dropped_total": len(dup_drops),
        "lexicon_candidates_after_lint": len(lex_in),
        "lexicon_form_drops_total": len(form_drops),
        "lexicon_form_drop_reasons": dict(Counter(r[:70] for d in form_drops for r in d["reasons"]).most_common()),
        "lexicon_forms_in_registry": len(reg.forms),
        "lexicon_forms_by_kind": dict(Counter(f.kind for f in reg.forms.values())),
        "lexicon_forms_unit_fail": len(bad_unit),
        "lexicon_forms_status": dict(Counter(reg.status(f) for f in reg.forms)),
        "forms_needing_admission": task_counts["forms_unit_ok"],
        "forms_needing_admission_by_kind": task_counts["forms_needing_admission_by_kind"],
        "forms_needing_3_of_3": task_counts["forms_strict_3_of_3"],
        "reads_per_form": {"other": 2, "question": 2},
        "glex_reads": len(READS),
        "glex_items_per_read": task_counts["glex_items_per_read"],
        "g3h_items": task_counts["g3h_items"],
        "survivors_by_pool": {p: len(v) for p, v in surv.items()},
        "tasks": manifest["n_tasks"],
        "task_outputs_expected": manifest["outputs_expected"],
        "tasks_by_kind": dict(Counter(r["kind"] for r in manifest["tasks"])),
    }
    if write:
        paths.write_files(ROOT, files)
        paths.write_jsonl(POOL_ROOT / "skins.jsonl", [_pool_row(p) for p in surv["skins"] + surv["skins_held"]])
        paths.write_jsonl(POOL_ROOT / "attack.jsonl", [_pool_row(p) for p in surv["attack_notes"]])
        paths.write_jsonl(POOL_ROOT / "freeform.jsonl", [_pool_row(p) for p in g3_pieces])
        paths.write_jsonl(POOL_ROOT / "g3h_expected.jsonl",
                          [{"pid": p["iid"], "task_id": p["task_id"], "expect": g3h_expect(p)} for p in g3_pieces])
        paths.write_jsonl(POOL_ROOT / "packs.jsonl", [_pool_row(p) for p in surv["packs"]])
        paths.write_jsonl(POOL_ROOT / "lexicon_forms.jsonl", [_pool_row(p) for p in lex_ok])
        paths.write_json(POOL_ROOT / "lexicon_registry.json", reg.to_json())
        paths.write_json(ROOT / "lint_log.json", {
            "counts": counts, "lint_drops": lint_drops, "dedup_drops": dup_drops, "form_drops": form_drops,
            "lint_values_problems": sample_probs})
    return {"counts": counts, "tasks": [{"task_file": r["task_file"], "answer_file": r["answer_file"],
                                         "kind": r["kind"], "read": r["read"]} for r in manifest["tasks"]],
            "written": write}


def _pool_row(p: dict) -> dict:
    return {k: v for k, v in p.items() if not k.startswith("_") and k not in ("task_problems",)}


def main(argv: list) -> int:
    write = "--write" in argv
    res = run(write)
    print(json.dumps(res["counts"], indent=1, ensure_ascii=False))
    print(f"tasks: {len(res['tasks'])}; written: {res['written']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
