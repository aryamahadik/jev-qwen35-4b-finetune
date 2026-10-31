"""transfer/T36/extract.py: the T36 Haiku EXTRACTION round after the authoring round (haiku/author/).

Runs after A38 only. Every write goes through paths.write_files / write_jsonl / write_json, which refuse before A38.
Steps (C2_DATA_SPEC 6.3; G0_SPEC v2 sections 6 and 7; PREREG A37 (b), A38):
  1. collect  authoring.load_pools(): the 14 returned authoring answers, mapped to their items, linted with the
              authoring G-SL pass and exact-deduplicated. Nothing is written here.
  2. lint     the checks load_pools does not run (G-SL; G0_SPEC section 6):
              - Mode F documents: the Mode T name check on the text with the two fact values masked (every other person
                is unnamed, so a second personal name would add a fact the brief does not give);
              - question wordings, by form: yn_meets, yn_outside and ch_pick carry no negation cue; yn_not_meets carries
                exactly one "not" / "n't" and no other cue; yn_fails carries "fail(s) to" as its only cue; ch_pick never
                says latest, newest, most recent or upgrade; no wording names an operator symbol, a tag word or an option
                letter.
  3. dedup    the normalised text (case and spacing) inside each pool; the first copy is kept.
  4. lex      every surviving wording becomes a Haiku lexicon form (kind question, sem q.t36.<qform>) of a registry that
              also declares the five question meanings (plugin.QUESTION_MEANINGS) and the three decoys
              (plugin.QUESTION_DECOYS). Then lexicon.unit_test. A form that fails the unit test is not sent for
              extraction (its problems are logged).
  5. tasks    G-LEX: two independent reads (glex-r1, glex-r2) of every unit-ok form. Each read is its own batch, so its
              own chunk files, and each read uses another sample instance of the form's slot values (the T29 pattern).
              T36 has no precedence or window forms, so the 3/3 rule is not used; every form needs 2/2.
              G3-H: one extraction read of every surviving Mode F document, fields project and person
              (plugin.extract_fields). The generator's values stay in pool/ (orchestrator side), never in a chunk.
  6. write    haiku/extract/: chunks/, prompts/, key/, manifest/ (the chunker files), TASKS.json, answers/README.txt,
              pool/ (survivors, the lexicon registry, the G3-H expected values), lint_log.json.

  cd lean && ../.venv/bin/python c2_build/transfer/T36/extract.py          (dry run: counts only, writes nothing)
  cd lean && ../.venv/bin/python c2_build/transfer/T36/extract.py --write  (after A38: writes the files above)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from transfer.T36 import authoring as A  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
VERSION = "v1"
ROOT = HERE / "haiku" / "extract"
LABEL = tuple(P.T36Plugin.LABEL_WORDS)
NAME_ALLOW = tuple(P.T36Plugin.NAME_ALLOW)
MODE_F_POOLS = ("freeform", "freeform_heldout")
MODE_T_POOLS = ("skin", "skin_heldout", "attack")

NOT_RX = re.compile(r"\bnot\b|n['\u2019]t\b", re.I)
FAIL_TO_RX = re.compile(r"\bfails?\s+to\b", re.I)
PICK_BANNED_RX = re.compile(r"\b(?:latest|newest|most\s+recent|upgrad\w*)\b", re.I)
TAG_RX = re.compile(r"\b(?:alpha|beta|rc|pre-?release|post-?release|tags?)\b", re.I)
OPERATOR_RX = re.compile(r"[<>=^~!|*@]")
OPTION_RX = re.compile(r"\b(?:option|choice)\s+[A-Za-z]\b", re.I)


# ------------------------------------------------------------------------------------------------ prompts

AGENT_RULES = ("How to work: this chunk file is the only file you may open. Do not open, list or search any other file "
               "or folder. Write your whole answer, and nothing else, as one JSON array to the answer_file path named in "
               "this chunk file, with the Write tool. Inside JSON strings, write a double quote as \\\" and a line break "
               "as \\n.\n")

GLEX_PROMPT = AGENT_RULES + """
TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (one short
question with its values already filled in) and CHOICES (a list of meanings).

Rules:
1. Use only the TEXT and its CHOICES. Do not guess beyond the words, and do not add a condition, a default or any fact
   from outside the text.
2. Copy the chosen CHOICE exactly, character for character, from that item's own list. Never write a new meaning.
3. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
Copy each qid exactly.
"""

G3H_PROMPT = AGENT_RULES + """
TASK: READ ONE DOCUMENT and extract two fields from it. Each item gives a TEXT (a short free-form document) and a SCHEMA
with two fields:
- project: the project whose dependency is discussed, copied exactly as written in the TEXT.
- person: the person who maintains the project, copied exactly as written in the TEXT.

Rules: copy each name exactly as it is written (same letters, same capitals, same spacing); do not correct spelling; do
not infer a name the TEXT does not write; if the TEXT does not give a field, write NONE. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "project": "<as written, or NONE>", "person": "<as written, or NONE>"}, ...]
Copy each qid exactly.
"""

ANSWERS_README = ("T36 extraction answers: one <task_id>.json per extraction task (see ../TASKS.json). Written only by "
                  "the task agents.\n")


# ------------------------------------------------------------------------------------------------ helpers

def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _norm(t) -> str:
    return " ".join(str(t).casefold().split())


def _reasons(viols) -> list:
    return [f"{v.rule}: {v.detail}" for v in viols]


def _mask(text: str, occ: dict) -> str:
    """The text with every verbatim fact value replaced by the gsl marker (the outside-value part only)."""
    spans = sorted((a, b) for sp in occ.values() for a, b in sp)
    parts, pos = [], 0
    for a, b in spans:
        if a < pos:
            continue
        parts += [text[pos:a], gsl._MARK]
        pos = b
    parts.append(text[pos:])
    return "".join(parts)


# ------------------------------------------------------------------------------------------------ 1. collect

def collect() -> dict:
    """{pool: [record]} from authoring.load_pools() (already G-SL linted and exact-deduplicated), plus the authoring
    counts. A record holds the pool piece as load_pools returned it, its internal id (pid) and its task provenance."""
    loaded = A.load_pools()
    authored = Counter()
    for pool, _iid, _reasons_ in loaded["dropped"]:
        authored[pool] += 1
    recs = {}
    for pool, objs in loaded["pieces"].items():
        recs[pool] = []
        authored[pool] += len(objs)
        for o in objs:
            if pool == "pack":
                recs[pool].append({"pool": pool, "pid": f"pack|{P.project_id(o.project)}", "text": None,
                                   "task_id": None, "prompt_sha": None, "held_out": bool(o.held_out), "obj": o})
            elif pool == "wording":
                text = o["text"]
                recs[pool].append({"pool": pool, "pid": f"wording|{_sha(text)[:16]}", "text": text,
                                   "task_id": o["haiku_task_id"], "prompt_sha": o["haiku_prompt_sha"],
                                   "held_out": False, "obj": o})
            else:
                recs[pool].append({"pool": pool, "pid": f"{pool}|{_sha(o.text)[:16]}", "text": o.text,
                                   "task_id": o.haiku_task_id, "prompt_sha": o.haiku_prompt_sha,
                                   "held_out": bool(o.held_out), "obj": o})
    return {"recs": recs, "authored": dict(authored), "authoring_drops": loaded["dropped"],
            "authoring_problems": loaded["problems"]}


# ------------------------------------------------------------------------------------------------ 2. lint

def mode_f_problems(piece) -> list:
    """Mode F fact-lock (G-SL): both fact values verbatim, and no other personal name in the document."""
    facts = dict(piece.brief)
    fills = {"PERSON": facts["PERSON"], "PROJECT": facts["PROJECT"]}
    occ = K.locate(piece.text, fills)
    out = [f"fact {n} is not verbatim in the text" for n, sp in occ.items() if not sp]
    out += _reasons(gsl._word_hits(_mask(piece.text, occ), {"name"}, LABEL, {}, NAME_ALLOW))
    return out


def wording_problems(o: dict) -> list:
    """G0_SPEC section 6 wording rules, by form. The wording role of gsl.lint_template keeps no negation check, so
    the form rules and the banned words are checked here."""
    qf, text = o["qform"], o["text"]
    lit = K.PH_RE.sub(" ", text)
    k = gsl.negcount.count(lit).k_all
    nots = len(NOT_RX.findall(lit))
    out = []
    if qf in ("yn_meets", "yn_outside", "ch_pick") and k:
        out.append(f"negation: {k} cue(s) in a {qf} wording (G0 section 6: none)")
    if qf == "yn_not_meets" and (nots != 1 or k != 1):
        out.append(f"negation: yn_not_meets needs exactly one not / n't and no other cue ({nots} not/n't, {k} cues)")
    if qf == "yn_fails" and (not FAIL_TO_RX.search(lit) or k != 1):
        out.append("negation: yn_fails needs fail(s) to as its only cue")
    if qf == "ch_pick":
        m = PICK_BANNED_RX.search(lit)
        if m:
            out.append(f"ch_pick: names {m.group()!r} (G0 section 6: never latest, newest, most recent, upgrade)")
    for rx, what in ((TAG_RX, "a tag"), (OPERATOR_RX, "an operator"), (OPTION_RX, "an option")):
        m = rx.search(lit)
        if m:
            out.append(f"names {what} ({m.group()!r}) (G0 section 6)")
    return out


def extra_lint(recs: dict) -> tuple:
    """({pool: [record]} survivors, [drop]) for the checks load_pools does not run."""
    kept, drops = {}, []
    for pool, rs in recs.items():
        kept[pool] = []
        for r in rs:
            if pool in MODE_F_POOLS:
                reasons = mode_f_problems(r["obj"])
            elif pool == "wording":
                reasons = wording_problems(r["obj"])
            else:
                reasons = []
            if reasons:
                drops.append({"pid": r["pid"], "pool": pool, "task_id": r["task_id"], "reasons": reasons})
            else:
                kept[pool].append(r)
    return kept, drops


# ------------------------------------------------------------------------------------------------ 3. dedup

def dedup_all(recs: dict) -> tuple:
    """Exact duplicates of the normalised text inside each pool (packs: the project id). First copy kept."""
    kept, drops = {}, []
    for pool, rs in recs.items():
        seen, out = {}, []
        for r in rs:
            key = _norm(r["pid"]) if pool == "pack" else _norm(r["text"])
            if key in seen:
                drops.append({"pid": r["pid"], "pool": pool, "task_id": r["task_id"],
                              "reasons": [f"duplicate of {seen[key]}"]})
            else:
                seen[key] = r["pid"]
                out.append(r)
        kept[pool] = out
    return kept, drops


# ------------------------------------------------------------------------------------------------ 4. lexicon

def build_registry(wordings: list) -> tuple:
    """(registry, form_ids {pid: form id}, form drops). Each surviving wording is a Haiku form; then the unit test."""
    reg = LX.LexiconRegistry(FAMILY)
    for qf, meaning in P.QUESTION_MEANINGS.items():
        reg.declare(LX.question_sem(FAMILY, qf), "question", meaning)
    for sem, meaning in P.QUESTION_DECOYS.items():
        reg.declare(sem, "question", meaning)
    reg.declare_antonym(LX.question_sem(FAMILY, "yn_meets"), LX.question_sem(FAMILY, "yn_outside"))
    fids, drops = {}, []
    for r in sorted(wordings, key=lambda r: r["pid"]):
        o = r["obj"]
        try:
            f = reg.add(o["text"], LX.question_sem(FAMILY, o["qform"]), slots=o["slots"], source="haiku",
                        family=FAMILY, haiku_task_id=o["haiku_task_id"], haiku_prompt_sha=o["haiku_prompt_sha"],
                        held_out=False)
            fids[r["pid"]] = f.form_id
        except LX.LexiconError as e:
            drops.append({"pid": r["pid"], "pool": "wording", "task_id": r["task_id"], "reasons": [f"form: {e}"]})
    reg.unit_test_all()
    return reg, fids, drops


# ------------------------------------------------------------------------------------------------ 5. tasks

GLEX_READS = (("glex-r1", 0), ("glex-r2", 1))


def glex_items(reg: LX.LexiconRegistry, ids: list, seed: str, instance: int) -> list:
    """Gold-free extraction items as lexicon.lexicon_items builds them, except that the filled instance is the
    `instance`-th sample whose slot values are pairwise distinct, so the two reads see different filled texts."""
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


def g3h_fields() -> list:
    return list(P.T36Plugin().extract_fields(None))


def make_batches(reg: LX.LexiconRegistry, g3_items: list) -> list:
    """[(read label, kind, TaskBatch, prompt)]: each read is its own batch, so its own chunk files."""
    ok = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    batches = []
    for label, instance in GLEX_READS:
        seed = f"t36-extract-{VERSION}-{label}"
        items = glex_items(reg, ok, seed, instance)
        batches.append((label, "extract_lex",
                        chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=GLEX_PROMPT),
                        GLEX_PROMPT))
    seed = f"t36-extract-{VERSION}-g3h-r1"
    batches.append(("g3h-r1", "extract_g3h",
                    chunker.make_batch("extract_g3h", FAMILY, g3_items, seed=seed, prompt=G3H_PROMPT), G3H_PROMPT))
    return batches


def _guarded_chunks(batch, read: str, prompt: str) -> None:
    """Each chunk is its own task file: it names its answer file and carries the instructions (authoring.py pattern).
    No internal id may appear in a chunk."""
    for i, c in enumerate(batch.chunks):
        answer = str(ROOT / batch.answer_path(c["task_id"]))
        batch.chunks[i] = {"task_id": c["task_id"], "kind": c["kind"], "read": read, "prompt_sha": c["prompt_sha"],
                           "answer_file": answer, "instructions": prompt.split("\n"), "items": c["items"]}
        blob = json.dumps(batch.chunks[i], ensure_ascii=False)
        if any(iid in blob for iid in batch.key.values()):
            raise chunker.ChunkError(f"chunk {c['task_id']} names an internal id")


def files_and_index(batches: list) -> tuple:
    """({relative path: text} for paths.write_files, the TASKS.json index)."""
    out, rows = {}, []
    for read, kind, b, prompt in batches:
        _guarded_chunks(b, read, prompt)
        out.update(b.files())
        for c in b.chunks:
            rd, wr = b.allowed(str(ROOT), c["task_id"])
            rows.append({"read": read, "kind": kind, "task_id": c["task_id"], "batch_id": b.batch_id,
                         "task_file": str(ROOT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                         "prompt_sha": b.prompt_sha, "n_items": len(c["items"]),
                         "outputs_expected": len(c["items"]), "allowed_read": sorted(rd),
                         "allowed_write": sorted(wr)})
    index = {"family": FAMILY, "version": VERSION, "stage": "extract", "loader": "transfer/T36/extract.py",
             "tier": "transfer_dev (never trained)", "n_tasks": len(rows),
             "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    out["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ANSWERS_README
    return out, index


# ------------------------------------------------------------------------------------------------ run

def run(write: bool) -> dict:
    col = collect()
    recs, lint_drops = extra_lint(col["recs"])
    recs, dup_drops = dedup_all(recs)

    wordings = recs.get("wording", [])
    reg, fids, form_drops = build_registry(wordings)
    ok_forms = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)

    fields = g3h_fields()
    g3_recs = recs.get("freeform", []) + recs.get("freeform_heldout", [])
    g3_items, g3_expected = [], []
    for r in sorted(g3_recs, key=lambda r: r["pid"]):
        o = r["obj"]
        facts = dict(o.brief)
        iid = f"g3h|{r['pid']}"
        g3_items.append((iid, g3h.extraction_item(o.text, fields)))
        g3_expected.append({"g3h_id": iid, "pid": r["pid"], "held_out": r["held_out"],
                            "expected": {"project": facts["PROJECT"], "person": facts["PERSON"]},
                            "fields": [f.name for f in fields]})

    batches = make_batches(reg, g3_items)
    files, index = files_and_index(batches)

    authored = col["authored"]
    reads ={label: sum(len(c["items"]) for c in b.chunks) for label, _k, b, _p in batches[:len(GLEX_READS)]}
    counts = {
        "pieces_authored": sum(authored.values()),
        "pieces_authored_by_pool": authored,
        "authoring_drops_by_pool": dict(Counter(p for p, _i, _r in col["authoring_drops"])),
        "authoring_problems": col["authoring_problems"],
        "lint_dropped_by_pool": dict(Counter(d["pool"] for d in lint_drops)),
        "lint_dropped_total": len(lint_drops),
        "lint_drop_reasons_by_rule": dict(Counter(r.split(":", 1)[0] for d in lint_drops for r in d["reasons"])
                                          .most_common()),
        "dedup_dropped_total": len(dup_drops),
        "survivors_by_pool": {p: len(v) for p, v in recs.items()},
        "lexicon_forms_in_registry": len(reg.forms),
        "lexicon_form_drops": len(form_drops),
        "forms_unit_fail": len(reg.forms) - len(ok_forms),
        "forms_needing_admission": len(ok_forms),
        "forms_needing_admission_by_qform": dict(Counter(reg.forms[f].sem_id.split(".")[-1] for f in ok_forms)),
        "reads_per_form": {"question": len(GLEX_READS)},
        "glex_items_per_read": reads,
        "g3h_items": len(g3_items),
        "g3h_items_held_out": sum(1 for r in g3_expected if r["held_out"]),
        "tasks": index["n_tasks"],
        "task_outputs_expected": index["outputs_expected"],
    }
    if write:
        paths.write_files(ROOT, files)
        for pool in ("pack", "skin", "skin_heldout", "attack", "freeform", "freeform_heldout"):
            rows = []
            for r in recs.get(pool, []):
                o = r["obj"]
                rows.append({"pool": pool, "pid": r["pid"], "held_out": r["held_out"], "task_id": r["task_id"],
                             "piece": asdict(o) if hasattr(o, "__dataclass_fields__") else o})
            paths.write_jsonl(ROOT / "pool" / f"{pool}.jsonl", rows)
        paths.write_jsonl(ROOT / "pool" / "wording_forms.jsonl",
                          [{"form_id": f.form_id, "pid": pid, "sem_id": f.sem_id, "qform": f.sem_id.split(".")[-1],
                            "text": f.text, "slots": dict(f.slots), "haiku_task_id": f.haiku_task_id,
                            "haiku_prompt_sha": f.haiku_prompt_sha, "unit_ok": f.unit_ok,
                            "unit_problems": f.unit_problems}
                           for pid, fid in sorted(fids.items()) for f in [reg.forms[fid]]])
        paths.write_json(ROOT / "pool" / "lexicon_registry.json", reg.to_json())
        paths.write_jsonl(ROOT / "pool" / "g3h_expected.jsonl", g3_expected)
        paths.write_json(ROOT / "lint_log.json", {
            "counts": counts, "authoring_drops": [{"pool": p, "iid": i, "reasons": r}
                                                  for p, i, r in col["authoring_drops"]],
            "lint_drops": lint_drops, "dedup_drops": dup_drops, "form_drops": form_drops,
            "unit_fail": [{"form_id": f.form_id, "text": f.text, "problems": f.unit_problems}
                          for f in reg.forms.values() if not f.unit_ok]})
    return {"counts": counts, "tasks": [{"task_file": r["task_file"], "answer_file": r["answer_file"],
                                         "kind": r["kind"], "read": r["read"]} for r in index["tasks"]],
            "written": write}


def main(argv: list) -> int:
    res = run("--write" in argv)
    print(json.dumps(res["counts"], indent=1, ensure_ascii=False, sort_keys=True))
    print(f"tasks: {len(res['tasks'])}; written: {res['written']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
