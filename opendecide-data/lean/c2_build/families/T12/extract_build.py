"""c2_build/families/T12/extract_build.py: the T12 lint stage after the Haiku authoring answers, dedup, and the Haiku
extraction tasks for G-LEX (lexicon admission) and G3-H (Mode F round trip). After A38 only: every write goes through
paths.write_files / paths.write_json (both refuse before the A38 freeze and refuse never-open paths).

  lint    authoring.load() checks (G-SL lint_template / lint_freeform, word rules, comparator / precedence / wording
          lexicon unit tests, pack shape and probes) plus gsl.lint_values on every kept pack's name values. A piece
          with any problem is dropped and its reasons are logged.
  dedup   one normalised text per group (training before held-out): comparators, precedence and question wordings
          share one lexicon namespace; skins, free-form notes, pressure lines and packs are deduped per pool.
          Comparators are also checked against authoring.dedup_comparators (the family's own rule).
  glex    one LexiconRegistry of the kept forms (source haiku). A form whose unit test fails in the combined
          registry is dropped (logged) and the registry is rebuilt until it is stable. Each form needs 2 reads
          (comparator, question) or 3 reads (precedence). Each read is its own batch with its own seed, so the same
          form sits in 2 or 3 separate chunk files, and each chunk file is one extraction task.
  g3h     one read of every kept Mode F note (extract_g3h: text + schema). The expected values stay in key/.

  ../.venv/bin/python -m families.T12.extract_build lint     (lint log only, from lean/c2_build)
  ../.venv/bin/python -m families.T12.extract_build build    (lint + dedup + tasks + files)

Haiku never sets a label: an extract_lex answer names a meaning (meaning_to_sem maps it to a sem id), and a
disagreement or an unknown meaning rejects the form for good (lexicon.record_extraction, status "rejected").
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T12 import authoring as A  # noqa: E402
from families.T12 import plugin as P  # noqa: E402

FAMILY = "T12"
EXTRACT = HERE / "haiku" / "extract"
LINT = HERE / "haiku" / "lint"
SEED = "t12-extract-v1"
READS = {"comparator": 2, "question": 2, "precedence": 3}         # G-LEX: 2/2, 3/3 for precedence (kit LexForm)
POOL_TYPE = {"packs": "pack", "skins": "skin", "freeform": "free", "wordings": "word", "comparators": "cmp",
             "precedence": "prec", "attacks": "attack"}
LEX_TYPES = ("cmp", "prec", "word")
DEPT_KEY_OF_SURFACE = {v[0]: k for k, v in P.DEPTS.items()}     # the freeform DEPT value is the first surface

PROMPT_LEX = (
    "You read one short phrase or sentence about an accounts-payable (AP) policy card and say which meaning it "
    "expresses. Each item has a \"text\" (the phrase or sentence, with an example value filled in) and a \"choices\" "
    "list of meanings. For each item, pick the one choice that the text says most plainly, and copy that choice "
    "exactly, character for character, into the \"meaning\" field. Judge the words of the text only: do not guess "
    "from what would be sensible for an AP policy, and do not reason about any other item. Answer every item once; "
    "no item may be skipped or repeated.")
PROMPT_G3H = (
    "You read a short free-text note from an accounts-payable team. Each item has a \"text\" (the note) and a "
    "\"schema\" listing the fields to extract. For each item, return every field's value as the note states it: "
    "\"clerk\" is the full name of the person the note is from or to, copied exactly as written; \"dept\" is the "
    "team the purchase is for, copied as the note writes it (one of the listed \"choices\" when the schema gives "
    "choices). Do not add facts, and do not fill in a value the note does not give. Answer every item once; no item "
    "may be skipped or repeated.")
ANSWER_SPEC = {
    "extract_lex": ('[{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]', "meaning"),
    "extract_g3h": ('[{"qid": "<qid>", "clerk": "<full name>", "dept": "<team as written>"}, ...]', "clerk, dept"),
}
TAIL = ("\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
        "array in the answer format below, one entry per item. No other file, no other text.")


def _norm(t: str) -> str:
    return " ".join(t.casefold().split())


def _fid(sem: str, text: str) -> str:
    return f"{sem}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"


# ================================================================================================ lint
def _pack_values(pack: dict) -> dict:
    vals = {"ORG": pack["org"]}
    vals.update({f"VENDOR{i}": v for i, v in enumerate(pack["vendors"])})
    vals.update({f"CLERK{i}": v for i, v in enumerate(pack["clerks"])})
    vals.update({f"APPROVER{i}": v for i, v in enumerate(pack["approvers"])})
    return vals


def lint_pack(pack: dict) -> list:
    """G-SL on the pack's name values (gsl.lint_values over name slots)."""
    probs, slots = [], {}
    for k, v in _pack_values(pack).items():
        try:
            slots[k] = S.name_slot(v)
        except S.SlotError as e:
            probs.append(f"G-SL value {k}: {e}")
    probs += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_values(slots)]
    return probs


def lint_stage() -> tuple:
    """(kept pieces, dropped pieces, per-task log). Piece dicts carry the task id, prompt sha and held-out flag."""
    loaded = A.load()
    kept, dropped, tasks = [], [], []
    for label, pool, held, _per, b in A.build():
        tid = b.chunks[0]["task_id"]
        rec = loaded[tid]
        items = chunker.item_by_internal(b)
        tasks.append({"task": label, "task_id": tid, "pool": pool, "held_out": held, "pieces": len(rec["pieces"]),
                      "task_problems": rec["problems"]})
        for pid, value, probs in rec["pieces"]:
            typ = POOL_TYPE[pool]
            iid = pid if typ == "pack" else pid.rsplit("|", 1)[0]
            probs = list(probs)
            if typ == "pack" and not probs and isinstance(value, dict):
                probs += lint_pack(value)
            p = {"typ": typ, "pool": pool, "pid": pid, "iid": iid, "held": held, "tid": tid,
                 "prompt_sha": b.prompt_sha, "value": value, "text": value if isinstance(value, str) else None,
                 "item": items.get(iid), "problems": probs}
            (dropped if probs or not value else kept).append(p)
    return kept, dropped, tasks


def dedup_stage(kept: list) -> tuple:
    """(kept after dedup, duplicates dropped). Training pieces are seen before held-out ones."""
    out, dups = [], []
    seen = set()
    for p in sorted(kept, key=lambda q: (q["held"], q["pid"])):
        if p["typ"] == "pack":
            key = ("pack", json.dumps(p["value"], sort_keys=True))
        else:
            group = "lex" if p["typ"] in LEX_TYPES else p["typ"]
            key = (group, _norm(p["text"]))
        if key in seen:
            dups.append(p)
            continue
        seen.add(key)
        out.append(p)
    return out, dups


def comparator_check(kept: list) -> int:
    """The family's own comparator dedup (authoring.dedup_comparators) keeps the same number of texts."""
    cmp_p = [(p["pid"], p["text"], []) for p in kept if p["typ"] == "cmp"]
    return len(A.dedup_comparators(cmp_p))


# ================================================================================================ G-LEX
def _form_spec(p: dict) -> dict:
    if p["typ"] == "cmp":
        _, sem, kind = p["pid"].split("|")[:3]
        return {"sem": sem, "slots": {"X": kind}}
    if p["typ"] == "prec":
        return {"sem": P.PREC_SEM, "slots": {}}
    qform = p["pid"].split("|")[1]
    return {"sem": question_sem(FAMILY, qform), "slots": {"INVOICE_ID": "id"}}


def _registry(forms: list) -> LexiconRegistry:
    reg = LexiconRegistry(FAMILY)
    P.declare_lexicon(reg)
    for f in forms:
        reg.add(f["text"], f["sem"], slots=f["slots"], source="haiku", family=FAMILY, haiku_task_id=f["tid"],
                haiku_prompt_sha=f["prompt_sha"], held_out=f["held"])
    return reg


def admit_units(forms: list) -> tuple:
    """(registry, forms kept, unit-test drops). Drops every form whose unit test fails in the combined registry."""
    dropped = []
    while True:
        reg = _registry(forms)
        bad = {fid: reg.forms[fid].unit_problems[:2] for fid in sorted(reg.forms) if not reg.unit_test(fid)}
        if not bad:
            return reg, forms, dropped
        keep = []
        for f in forms:
            fid = _fid(f["sem"], f["text"])
            if fid in bad:
                dropped.append({"form_id": fid, "pid": f["pid"], "text": f["text"], "reasons": bad[fid]})
            else:
                keep.append(f)
        forms = keep


def glex_batches(reg: LexiconRegistry) -> list:
    by_kind = {}
    for fid, f in reg.forms.items():
        by_kind.setdefault(f.kind, []).append(fid)
    out = []
    for kind in ("comparator", "question", "precedence"):
        fids = sorted(by_kind.get(kind, []))
        for r in range(1, READS[kind] + 1):
            seed = f"t12-glex-{kind}-r{r}"
            items = reg.lexicon_items(fids, seed=seed)
            b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=PROMPT_LEX)
            out.append({"group": kind, "read": r, "batch": b, "form_ids": fids})
    return out


# ================================================================================================ G3-H
def g3h_fields() -> list:
    params = S.category_slot("facilities", P.DEPTS).params
    return [g3h.Field("clerk", "name", "the accounts payable person the note is from or to, as written"),
            g3h.Field("dept", "category", "the team the purchase is for", params)]


def g3h_items(kept: list) -> tuple:
    """([(internal id, item)], {internal id: expected}) for the kept Mode F notes."""
    fields = g3h_fields()
    items, expected = [], {}
    for p in sorted((q for q in kept if q["typ"] == "free"), key=lambda q: q["pid"]):
        facts = p["item"]["facts"]
        iid = f"g3h|{p['pid']}"
        exp = {"clerk": facts["CLERK"], "dept": DEPT_KEY_OF_SURFACE[facts["DEPT"]]}
        ok, diffs = g3h.compare(exp, {"clerk": facts["CLERK"], "dept": facts["DEPT"]}, fields)
        if not ok:
            raise RuntimeError(f"G3-H self-check failed for {iid}: {diffs}")
        items.append((iid, g3h.extraction_item(p["text"], fields)))
        expected[iid] = exp
    return items, expected


def g3h_batch(items: list) -> chunker.TaskBatch:
    n = len(items)
    chunks = max(1, math.ceil(n / chunker.MAX_ITEMS))
    seed = "t12-g3h-r1"
    return chunker.make_batch("extract_g3h", FAMILY, items, seed=seed, prompt=PROMPT_G3H,
                              max_items=math.ceil(n / chunks))


# ================================================================================================ tasks and files
def task_markdown(kind: str, b: chunker.TaskBatch, chunk: dict, answer_abs: Path) -> str:
    fmt, fields = ANSWER_SPEC[kind]
    prompt = PROMPT_LEX if kind == "extract_lex" else PROMPT_G3H
    assert b.prompt == prompt
    return (f"# T12 extraction task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer_abs}\n\n"
            f"Task kind: {kind}; items: {len(chunk['items'])}; answer fields: {fields}.\n\n"
            f"This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
            f"## Instructions\n\n{b.prompt}{TAIL}\n\n"
            f"Answer format: {fmt}\n\n"
            f"## Items (JSON; answer every item once, keyed by its qid)\n\n"
            + json.dumps(chunk["items"], ensure_ascii=False, indent=1) + "\n")


def build_all() -> dict:
    kept, dropped, tasks = lint_stage()
    kept, dups = dedup_stage(kept)
    n_cmp_family = comparator_check(kept)
    lex = [p for p in kept if p["typ"] in LEX_TYPES]
    forms = [dict(_form_spec(p), text=p["text"], pid=p["pid"], tid=p["tid"], prompt_sha=p["prompt_sha"],
                  held=p["held"], typ=p["typ"]) for p in lex]
    if n_cmp_family != sum(1 for f in forms if f["typ"] == "cmp"):
        raise RuntimeError("comparator dedup disagrees with authoring.dedup_comparators")
    reg, forms, unit_drops = admit_units(forms)
    glex = glex_batches(reg)
    g_items, g_expected = g3h_items(kept)
    g = g3h_batch(g_items)
    return {"kept": kept, "dropped": dropped, "tasks": tasks, "dups": dups, "reg": reg, "forms": forms,
            "unit_drops": unit_drops, "glex": glex, "g3h": g, "g3h_expected": g_expected}


def _task_rows(kind: str, group: str, read, b: chunker.TaskBatch) -> list:
    rows = []
    for c in b.chunks:
        tid = c["task_id"]
        tf, af = EXTRACT / "tasks" / f"{tid}.md", EXTRACT / b.answer_path(tid)
        rows.append({"task": f"{group}-r{read}" if read else group, "task_id": tid, "kind": kind, "group": group,
                     "read": read, "n_items": len(c["items"]), "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                     "outputs_expected": len(c["items"]), "task_file": str(tf), "answer_file": str(af),
                     "allowed_read": sorted({str(tf), str(EXTRACT / b.chunk_path(tid)),
                                             str(EXTRACT / b.prompt_path())}),
                     "allowed_write": [str(af)]})
    return rows


def write_all(res: dict) -> dict:
    files, index = {}, []
    lex_rows = []
    for rd in res["glex"]:
        b = rd["batch"]
        rows = _task_rows("extract_lex", rd["group"], rd["read"], b)
        index += rows
        lex_rows += rows
        files.update(b.files())
        for c, row in zip(b.chunks, rows):
            files[f"tasks/{c['task_id']}.md"] = task_markdown("extract_lex", b, c, Path(row["answer_file"]))
    g = res["g3h"]
    g_rows = _task_rows("extract_g3h", "g3h", 1, g)
    index += g_rows
    files.update(g.files())
    for c, row in zip(g.chunks, g_rows):
        files[f"tasks/{c['task_id']}.md"] = task_markdown("extract_g3h", g, c, Path(row["answer_file"]))
    for row in index:
        row["task_sha256"] = chunker.sha(files[f"tasks/{row['task_id']}.md"])
    fid_reads = {}
    for rd in res["glex"]:
        for c in rd["batch"].chunks:
            for it in c["items"]:
                fid = rd["batch"].key[it["qid"]]
                fid_reads.setdefault(fid, []).append({"task_id": c["task_id"], "group": rd["group"], "read": rd["read"]})
    form_src = {_fid(x["sem"], x["text"]): x for x in res["forms"]}
    forms_out = []
    for fid in sorted(res["reg"].forms):
        f = res["reg"].forms[fid]
        forms_out.append({"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text,
                          "pid": form_src[fid]["pid"], "held_out": f.held_out, "required": f.required,
                          "reads": fid_reads.get(fid, [])})
    index_doc = {"family": FAMILY, "seed": SEED, "g0_sha256": P.G0_SHA256_AUTHORED,
                 "g0_ambiguity_pass": P.T12Plugin.G0_HAIKU_TASK, "n_tasks": len(index),
                 "n_lex_tasks": len(lex_rows), "n_g3h_tasks": len(g_rows),
                 "answer_formats": {k: v[0] for k, v in ANSWER_SPEC.items()},
                 "record": "reg.record_extraction(form_id, extractor_id=task_id, sem_id=reg.meaning_to_sem(kind, "
                           "answer['meaning']))  for extract_lex; g3h.compare(expected[iid], answer, fields) for "
                           "extract_g3h",
                 "tasks": index}
    files["TASKS.json"] = json.dumps(index_doc, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per extraction task (see ../TASKS.json). "
                                   "Written only by the task agents; read by the lexicon admission (G-LEX) and G3-H "
                                   "stages. An extract_lex answer is a meaning text; a disagreement rejects the form.\n")
    files["forms_needing_admission.json"] = json.dumps({"family": FAMILY, "forms": forms_out}, ensure_ascii=False,
                                                       indent=1) + "\n"
    files["lexicon_pending.json"] = json.dumps(res["reg"].to_json(), ensure_ascii=False, indent=1) + "\n"
    files["key/g3h_expected.json"] = json.dumps({"family": FAMILY, "expected": res["g3h_expected"]},
                                                 ensure_ascii=False, indent=1) + "\n"
    paths.write_files(EXTRACT, files)
    return index_doc


def lint_log(res: dict) -> dict:
    by_pool = {}
    for t in res["tasks"]:
        by_pool.setdefault(t["pool"], {"tasks": 0, "pieces": 0, "kept": 0, "lint_dropped": 0, "dedup_dropped": 0})
        by_pool[t["pool"]]["tasks"] += 1
        by_pool[t["pool"]]["pieces"] += t["pieces"]
    for p in res["kept"]:
        by_pool[p["pool"]]["kept"] += 1
    for p in res["dropped"]:
        by_pool[p["pool"]]["lint_dropped"] += 1
    for p in res["dups"]:
        by_pool[p["pool"]]["dedup_dropped"] += 1
    return {"family": FAMILY, "g0_sha256": P.G0_SHA256_AUTHORED,
            "pools": by_pool,
            "totals": {"pieces": sum(v["pieces"] for v in by_pool.values()),
                       "lint_dropped": len(res["dropped"]), "dedup_dropped": len(res["dups"]),
                       "kept": len(res["kept"]), "unit_test_dropped": len(res["unit_drops"]),
                       "lexicon_forms": len(res["reg"].forms)},
            "lint_dropped": [{"pool": p["pool"], "pid": p["pid"], "task_id": p["tid"], "held_out": p["held"],
                              "reasons": p["problems"][:3], "text": p["text"]} for p in res["dropped"]],
            "dedup_dropped": [{"pool": p["pool"], "pid": p["pid"], "held_out": p["held"],
                               "text": p["text"]} for p in res["dups"]],
            "unit_test_dropped": res["unit_drops"],
            "task_problems": [t for t in res["tasks"] if t["task_problems"]]}


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args else "build"
    if cmd == "lint":
        kept, dropped, tasks = lint_stage()
        kept2, dups = dedup_stage(kept)
        print(json.dumps({"kept": len(kept), "lint_dropped": len(dropped), "dedup_dropped": len(dups),
                          "kept_after_dedup": len(kept2)}, indent=1))
        return 0
    if cmd != "build":
        print(__doc__)
        return 2
    res = build_all()
    paths.write_json(LINT / "T12_lint_log.json", lint_log(res))
    idx = write_all(res)
    print(json.dumps({"lint_log": str(LINT / "T12_lint_log.json"), "tasks": idx["n_tasks"],
                      "lex_tasks": idx["n_lex_tasks"], "g3h_tasks": idx["n_g3h_tasks"],
                      "forms": len(res["reg"].forms), "index": str(EXTRACT / "TASKS.json")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
