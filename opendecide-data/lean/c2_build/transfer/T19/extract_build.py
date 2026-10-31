"""transfer/T19/extract_build.py: the T19 lint stage after the Haiku authoring answers, dedup, and the Haiku extraction
tasks for G-LEX (question wording admission, 2 independent reads) and G3-H (Mode F round trip, one read). Written after
A38; every write goes through paths.write_files / paths.write_json (both refuse before the freeze and on never-open
paths). Haiku never sets a label: an extract_lex answer names a meaning (meaning_to_sem maps it to a sem id), and a
disagreement rejects the form (lexicon.record_extraction).

  lint    haiku_author.load_* (the family's G-SL lint_template / lint_freeform checks, word rules, T19 head / hint /
          profile checks, negation counts, pack shape) plus gsl.lint_values on every kept pack's site and auditor names.
          A piece with any problem is dropped and its reasons are logged (lint_log.json).
  dedup   one normalised text per pool (haiku_author's loaders); question wordings share one lexicon namespace, where
          lexicon.add refuses a duplicate text across forms.
  glex    one LexiconRegistry of the kept wordings (source haiku) plus the six T19 question meanings. A form whose add or
          unit test fails in the combined registry is dropped (logged) and the registry is rebuilt until it is stable.
          Each form needs 2 reads: each read is its own batch with its own seed, so each form sits in 2 separate chunk
          files. (T19 has no precedence or window forms, so 3/3 does not apply.)
  g3h     one read of every kept Mode F note (extract_g3h: text + schema). The expected auditor stays in key/.

  ../.venv/bin/python c2_build/transfer/T19/extract_build.py lint     (lint log only, from lean/)
  ../.venv/bin/python c2_build/transfer/T19/extract_build.py build    (lint + dedup + tasks + files, from lean/)
"""
from __future__ import annotations

import argparse
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
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from transfer.T19 import fixtures as FX  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402

FAMILY = "T19"
EXTRACT = HERE / "haiku" / "extract"
READS_QUESTION = 2                              # G-LEX 2/2 for question wordings (no precedence / window forms)
G3H_SEED = "t19-g3h-r1"
MF_PREFIX = "T19-MF-"                           # freeform skin ids: T19-MF-<iid without "t19a.free.">

PROMPT_LEX = (
    "You read one short question that asks about a site's compliance checklist. Each item has a \"text\" (one question, "
    "with an example site name filled in) and a \"choices\" list of meanings. For each item, pick the one choice that the "
    "text says most plainly, and copy that choice exactly, character for character, into the \"meaning\" field. Judge the "
    "words of the text only: do not guess what an auditor would usually mean, and do not reason about any other item. "
    "Answer every item once; no item may be skipped or repeated.")
PROMPT_G3H = (
    "You read a short workplace note about a review of one site. Each item has a \"text\" (the note) and a \"schema\" "
    "listing the field to extract. For each item, return the field's value as the note states it: \"auditor\" is the full "
    "name of the person who is going through the site's records, copied exactly as written. Do not add facts, and do not "
    "fill in a value the note does not give. Answer every item once; no item may be skipped or repeated.")
ANSWER_SPEC = {
    "extract_lex": ('[{"qid": "<qid>", "meaning": "<one choice, copied exactly>"}, ...]', "meaning"),
    "extract_g3h": ('[{"qid": "<qid>", "auditor": "<full name>"}, ...]', "auditor"),
}
TAIL = ("\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
        "array in the answer format below, one entry per item. No other file, no other text.")


def _norm(t: str) -> str:
    return " ".join(t.casefold().split())


def _only_on(problems: list) -> bool:
    """True when every reason of a dropped piece is the bare word 'on' (the profile-word false positive, see README)."""
    out = []
    for p in problems:
        body = p.split(": ", 1)[1] if ": " in p else p
        out.extend(body.split("; "))
    return bool(out) and all(x.endswith("['on']") for x in out)


# ================================================================================================ lint
def lint_packs(packs: list) -> tuple:
    kept, drops = [], []
    for pk in packs:
        probs = []
        try:
            slots = {f"SITE{i}": S.name_slot(v) for i, v in enumerate(pk["sites"])}
            slots.update({f"AUDITOR{i}": S.name_slot(v) for i, v in enumerate(pk["auditors"])})
            probs += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_values(slots)]
        except S.SlotError as e:
            probs.append(f"G-SL name slot: {e}")
        if probs:
            drops.append({"id": pk["pack_id"], "held_out": pk["held_out"], "reasons": probs})
        else:
            kept.append(pk)
    return kept, drops


def lint_stage() -> dict:
    """Run every T19 loader (G-SL and the family's own checks). Returns the kept pieces and the drop log."""
    packs, p_pack = HA.load_packs()
    skins, p_skin = HA.load_skins()
    free, p_free = HA.load_freeform()
    attacks, p_att = HA.load_attacks()
    wordings, p_word = HA.load_wordings()
    _, plan_free, _, _ = HA.load_answers_for("freeform")
    pk_kept, pk_drop = lint_packs(packs)
    drops = {"packs": pk_drop}
    structural = []
    for name, probs in (("skins", p_skin), ("freeform", p_free), ("attacks", p_att), ("wordings", p_word),
                        ("packs", p_pack)):
        if name == "packs":
            continue
        drops[name] = []
        for p in probs:
            if p.startswith("t19a."):                       # a piece: its id, then its reasons
                pid, body = p.split(": ", 1)
                drops[name].append({"id": pid, "reasons": body.split("; "), "only_on": _only_on([p])})
            else:                                           # a task-level problem (missing answer, bad qid, ...)
                structural.append(p)
    # packs: the loader's refusals come as piece problems too (ids t19a.pack.*)
    for p in p_pack:
        if p.startswith("t19a."):
            pid, body = p.split(": ", 1)
            drops["packs"].append({"id": pid, "held_out": None, "reasons": body.split("; ")})
        else:
            structural.append(p)
    return {"packs": pk_kept, "skins": skins, "free": free, "attacks": attacks, "wordings": wordings,
            "plan_free": plan_free, "drops": drops, "structural": structural}


def dedup_stage(lint: dict) -> dict:
    """Pool-level dedup (the loaders already refuse a repeat within a pool); a cross-pool exact repeat is also refused
    and logged. Question wordings are deduped by lexicon.add in admit_forms()."""
    seen, cross = {}, []
    for pool, items in (("skins", lint["skins"]), ("free", lint["free"]), ("attacks", lint["attacks"])):
        for sid, sk in items.items():
            key = _norm(sk.text)
            if key in seen and seen[key] != pool:
                cross.append({"id": sid, "pool": pool, "same_as": seen[key]})
            seen.setdefault(key, pool)
    lint["cross_pool_dups"] = cross
    return lint


# ================================================================================================ G-LEX
def admit_forms(wordings: list) -> tuple:
    """(registry, kept forms, drops). A form that fails to add (a duplicate text across the registry) or whose unit test
    fails in the combined registry is dropped and logged; the registry is rebuilt until it is stable (lexicon.scan
    reads every form, so a unit test depends on the others)."""
    forms = [{"qform": q, "text": t, "tid": tid, "psha": psha, "sem": question_sem(FAMILY, q)}
             for q, t, tid, psha in wordings]
    drops = []
    while True:
        reg = LexiconRegistry(FAMILY)
        for qf, meaning in FX.QUESTION_MEANINGS.items():
            reg.declare(question_sem(FAMILY, qf), "question", meaning)
        added = []
        for f in forms:
            try:
                fo = reg.add(f["text"], f["sem"], slots={"SITE": "name"}, source="haiku", family=FAMILY,
                             haiku_task_id=f["tid"], haiku_prompt_sha=f["psha"])
            except LexiconError as e:
                drops.append({"qform": f["qform"], "text": f["text"], "tid": f["tid"], "reasons": [f"G-LEX add: {e}"]})
                continue
            added.append((f, fo.form_id))
        bad = {fid: reg.unit_test(fid) for _, fid in added}
        bad = {fid: reg.forms[fid].unit_problems[:2] for fid, ok in bad.items() if not ok}
        forms = []
        for f, fid in added:
            if fid in bad:
                drops.append({"qform": f["qform"], "text": f["text"], "tid": f["tid"],
                              "reasons": [f"G-LEX unit: {r}" for r in bad[fid]]})
            else:
                forms.append(f)
        if not bad:
            return reg, forms, drops


def glex_batches(reg: LexiconRegistry) -> list:
    """Two independent reads of every admitted question form; each read is its own batch with its own seed."""
    fids = sorted(reg.forms)
    out = []
    for r in range(1, READS_QUESTION + 1):
        seed = f"t19-glex-question-r{r}"
        items = reg.lexicon_items(fids, seed=seed)
        n = len(items)
        chunks = max(1, math.ceil(n / chunker.MAX_ITEMS))
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=PROMPT_LEX,
                               max_items=math.ceil(n / chunks))
        out.append({"group": "question", "read": r, "extractor_id": f"haiku-glex-question-r{r}", "batch": b,
                    "form_ids": fids})
    return out


# ================================================================================================ G3-H
def g3h_fields() -> list:
    # the same field as T19Plugin.extract_fields(): the auditor, as written
    return [g3h.Field("auditor", "name", "the person who runs the audit, as written")]


def g3h_items(free: dict, plan_free: dict) -> tuple:
    """([(internal id, item)], {internal id: expected}) for the kept Mode F notes. The expected auditor is from the
    generator's facts and stays in key/ (never in the item)."""
    fields = g3h_fields()
    items, expected = [], {}
    for sid in sorted(free):
        sk = free[sid]
        src = "t19a.free." + sid[len(MF_PREFIX):]
        facts = plan_free[src]["facts"]
        exp = {"auditor": facts["AUDITOR"]}
        ok, diffs = g3h.compare(exp, {"auditor": facts["AUDITOR"]}, fields)
        if not ok:
            raise RuntimeError(f"G3-H self-check failed for {sid}: {diffs}")
        iid = f"g3h|{sid}"
        items.append((iid, g3h.extraction_item(sk.text, fields)))
        expected[iid] = exp
    return items, expected


def g3h_batch(items: list) -> chunker.TaskBatch:
    n = len(items)
    chunks = max(1, math.ceil(n / chunker.MAX_ITEMS))
    return chunker.make_batch("extract_g3h", FAMILY, items, seed=G3H_SEED, prompt=PROMPT_G3H,
                              max_items=math.ceil(n / chunks))


# ================================================================================================ tasks and files
def task_markdown(kind: str, b: chunker.TaskBatch, chunk: dict, answer_abs: Path) -> str:
    fmt, fields = ANSWER_SPEC[kind]
    return (f"# T19 extraction task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer_abs}\n\n"
            f"Task kind: {kind}; items: {len(chunk['items'])}; answer fields: {fields}.\n\n"
            f"This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
            f"## Instructions\n\n{b.prompt}{TAIL}\n\n"
            f"Answer format: {fmt}\n\n"
            f"## Items (JSON; answer every item once, keyed by its qid)\n\n"
            + json.dumps(chunk["items"], ensure_ascii=False, indent=1) + "\n")


def build_all(root: Path = EXTRACT) -> dict:
    lint = dedup_stage(lint_stage())
    reg, forms, admit_drops = admit_forms(lint["wordings"])
    glex = glex_batches(reg)
    free_items, g3h_expected = g3h_items(lint["free"], lint["plan_free"])
    g3 = g3h_batch(free_items)
    batches = [(f"glex-question-r{g['read']}", "extract_lex", g["batch"], g) for g in glex]
    batches.append(("g3h-freeform-r1", "extract_g3h", g3, None))
    files, tasks = {}, []
    for label, kind, b, g in batches:
        files.update(b.files())
        plan = {"batch_id": b.batch_id, "label": label, "kind": kind,
                "extractor_id": (g["extractor_id"] if g else "haiku-g3h-freeform-r1")}
        files[f"plan/{b.batch_id}.json"] = json.dumps(plan, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(root / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            files[tfile] = task_markdown(kind, b, c, Path(ans))
            tasks.append({"task": label, "task_id": tid, "kind": kind, "pool": "glex" if kind == "extract_lex" else "g3h",
                          "batch_id": b.batch_id, "task_file": str(root / tfile), "answer_file": ans,
                          "n_items": len(c["items"]), "outputs_expected": len(c["items"]),
                          "prompt_sha": b.prompt_sha,
                          "task_sha256": hashlib.sha256(files[tfile].encode()).hexdigest(),
                          "allowed_read": [str(root / tfile)], "allowed_write": [ans]})
    files["answers/README.txt"] = ("Haiku extraction answer files: one <task_id>.json per task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    files["key/g3h_expected.json"] = json.dumps(g3h_expected, indent=1, sort_keys=True) + "\n"
    return {"lint": lint, "reg": reg, "forms": forms, "admit_drops": admit_drops, "glex": glex, "g3": g3,
            "g3h_expected": g3h_expected, "files": files, "tasks": tasks}


def summary(res: dict) -> dict:
    lint = res["lint"]
    drops = lint["drops"]
    kept = {"packs": len(lint["packs"]), "skins": len(lint["skins"]), "freeform": len(lint["free"]),
            "attacks": len(lint["attacks"]), "wordings": len(res["forms"])}
    n_items = {"packs": len(lint["packs"]) + len(drops["packs"]), "skins": len(lint["skins"]) + len(drops["skins"]),
               "freeform": len(lint["free"]) + len(drops["freeform"]),
               "attacks": len(lint["attacks"]) + len(drops["attacks"]),
               "wordings": len(lint["wordings"]) + len(drops.get("wordings", []))}
    per_pool = {}
    for name in kept:
        d = drops[name] if name != "wordings" else drops.get("wordings", [])
        per_pool[name] = {"answered": n_items[name], "kept": kept[name],
                          "dropped_by_lint": len(d),
                          "dropped_only_for_bare_on": sum(1 for x in d if x.get("only_on"))}
    per_pool["wordings"]["dropped_by_admit"] = len(res["admit_drops"])
    return {
        "per_pool": per_pool,
        "packs_kept_train_held": [sum(1 for p in lint["packs"] if not p["held_out"]),
                                  sum(1 for p in lint["packs"] if p["held_out"])],
        "skins_kept_by_register_held": _count(lint["skins"].values(), "register", "held_out"),
        "freeform_kept_by_register_held": _count(lint["free"].values(), "register", "held_out"),
        "question_forms_kept": len(res["forms"]),
        "question_forms_admit_drops": [f"{d['qform']}: {'; '.join(d['reasons'])}" for d in res["admit_drops"]],
        "glex_reads": [{"read": g["read"], "extractor_id": g["extractor_id"], "forms": len(g["form_ids"]),
                        "chunks": len(g["batch"].chunks)} for g in res["glex"]],
        "g3h_items": len(res["g3"].key),
        "g3h_chunks": len(res["g3"].chunks),
        "cross_pool_dups": lint["cross_pool_dups"],
        "structural_problems": lint["structural"],
        "tasks": len(res["tasks"]),
        "outputs_expected": sum(t["outputs_expected"] for t in res["tasks"]),
    }


def _count(items, a: str, b: str) -> dict:
    out: dict = {}
    for it in items:
        k = f"{getattr(it, a)}|{'held' if getattr(it, b) else 'train'}"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


def lint_log(res: dict) -> dict:
    lint = res["lint"]
    return {"family": FAMILY, "stage": "lint+dedup+admit", "drops": lint["drops"],
            "question_admit_drops": res["admit_drops"], "cross_pool_dups": lint["cross_pool_dups"],
            "structural": lint["structural"], "kept": {
                "packs": [p["pack_id"] for p in lint["packs"]],
                "skins": sorted(lint["skins"]), "freeform": sorted(lint["free"]),
                "attacks": sorted(lint["attacks"]),
                "question_forms": [f["qform"] + "|" + f["text"] for f in res["forms"]]}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("lint", "build"))
    a = ap.parse_args(argv)
    res = build_all()
    print(json.dumps(summary(res), indent=1, ensure_ascii=False))
    if a.cmd == "build":
        paths.write_files(EXTRACT, res["files"])
        paths.write_json(EXTRACT / "lint_log.json", lint_log(res))
        paths.write_json(EXTRACT / "TASKS.json", {"family": FAMILY, "stage": "extract", "n_tasks": len(res["tasks"]),
                                                   "outputs_expected": sum(t["outputs_expected"] for t in res["tasks"]),
                                                   "tasks": res["tasks"]})
        print(f"wrote {len(res['files'])} files under {EXTRACT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
