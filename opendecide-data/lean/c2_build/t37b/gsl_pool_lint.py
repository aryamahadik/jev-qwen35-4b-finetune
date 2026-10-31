"""t37b/gsl_pool_lint.py: G-SL over the T37b authoring answers, then the two polarity read tasks (A37 b; spec 6.3).

Runs once the nine authoring tasks are answered. It repeats author_pool.lint (placeholders, one question, bans, both
polarity programs on every probe fill, dedup) and adds the G-SL slot lint on each surviving paraphrase, read as a
wording skin (c2_kit.gsl.lint_template, role "wording"). A paraphrase that fails G-SL is dropped and its reason logged.
Nothing is repaired or re-worded, and no exception is added: T37b's frozen G0-lite spec lists no GSL_EXCEPTIONS and
no NAME_ALLOW, and CORE words are never excepted.

Writes the same formats as author_pool.run_lint, so `author_pool.py admit` reads them unchanged:
  haiku/author/lint/candidates.json   the paraphrases that passed lint and G-SL (author_pool's record format)
  haiku/author/lint/report.json       the lint report plus a "gsl" section (counts, reasons by rule, by entry)
  haiku/author/lint/gsl_drops.json    every dropped paraphrase with its G-SL violations (audit trail)
  haiku/extract/tasks/*.md, haiku/extract/TASKS.json, haiku/extract/answers/ (path only)
      two independent polarity reads (kind polarity:A and polarity:B), separate seeds, separate chunk files

Run from lean/:  ../.venv/bin/python c2_build/t37b/gsl_pool_lint.py
Never sets a label: the reads only admit or drop a paraphrase (author_pool.admit, G0 H41, H60).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import gsl, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

FAMILY = "T37b"
# G-SL slot kinds of the four placeholders (slots.KINDS): a statement number, a quoted span, a customer phrase and a
# claim clause. None is a count, so the agreement and count-unit grammar rules do not apply to them.
SLOT_KIND = {"N": "category", "SPAN": "name", "ORDER": "clause", "CLAIM": "clause"}


def wording_skin(rec: dict):
    """A paraphrase record as a Mode T wording skin: its placeholders are the entry's declared slots."""
    e = SRC.ENTRY_BY_KEY[rec["sem"]]
    _tpl, slots = SRC.pool_template(e)
    return K.make_skin(f"t37b-w-{rec['template_id']}", FAMILY, rec["template"],
                       {s: SLOT_KIND[s] for s in slots}, kind="wording", author_mode="T", qform="equiv")


def gsl_check(rec: dict) -> list:
    """G-SL violations of one paraphrase (empty = passes). No plugin: no label words, exceptions or name allowance."""
    return gsl.lint_template(wording_skin(rec), label_words=(), exceptions={}, name_allow=())


def base_gsl_report() -> dict:
    """Informational: the program's own base question per entry under the same wording rules (not a Haiku piece)."""
    out = {}
    for e in AP.pool_entries():
        tpl, slots = SRC.pool_template(e)
        sk = K.make_skin("t37b-base-" + e.key, FAMILY, tpl, {s: SLOT_KIND[s] for s in slots}, kind="wording",
                         author_mode="T", qform="equiv")
        v = gsl.lint_template(sk, label_words=(), exceptions={}, name_allow=())
        if v:
            out[e.key] = sorted({f"{x.rule}:{x.detail}" for x in v})
    return out


def run() -> dict:
    paths.require_a38()
    BL.require_g0()
    b = AP.author_batch()
    man = json.loads((AP.AUTHOR_DIR / "TASKS.json").read_text(encoding="utf-8"))
    if man.get("batch_id") != b.batch_id:
        raise RuntimeError(f"the authoring batch changed since the tasks were written ({man.get('batch_id')} != "
                           f"{b.batch_id}): rebuild the tasks, do not mix")
    answered = [c["task_id"] for c in b.chunks if (AP.AUTHOR_DIR / b.answer_path(c["task_id"])).is_file()]
    if len(answered) != len(b.chunks):
        raise RuntimeError(f"{len(answered)} of {len(b.chunks)} authoring answers present: stop")

    cands, rep = AP.lint(b, AP._read_answers(AP.AUTHOR_DIR, b))
    rep["answered_tasks"] = len(answered)

    # G-SL, then dedup on the (base question, paraphrase) pair key that admit() joins the reads on.
    kept, drops, seen_pair = [], [], set()
    rule_count, entry_drop = Counter(), Counter()
    for c in cands:
        viol = gsl_check(c)
        if viol:
            rules = sorted({x.rule for x in viol})
            rule_count.update(rules)
            entry_drop[c["sem"]] += 1
            drops.append({"sem": c["sem"], "template": c["template"], "author_item": c["author_item"],
                          "haiku_task_id": c["haiku_task_id"], "gsl": sorted({f"{x.rule}: {x.detail}" for x in viol})})
            continue
        pk = AP.rec_pair_key(c)
        if pk in seen_pair:
            drops.append({"sem": c["sem"], "template": c["template"], "author_item": c["author_item"],
                          "haiku_task_id": c["haiku_task_id"], "gsl": ["duplicate pair key"]})
            continue
        seen_pair.add(pk)
        kept.append(c)

    per_entry = Counter(c["sem"] for c in kept)
    gsl_rep = {"checked": len(cands), "passed": len(kept), "dropped": len(drops),
               "dropped_by_rule_hits": dict(rule_count.most_common()), "dropped_by_entry": dict(sorted(entry_drop.items())),
               "passed_by_entry": dict(sorted(per_entry.items())),
               "entries_with_no_passing_paraphrase": sorted(e.key for e in AP.pool_entries() if per_entry[e.key] == 0),
               "base_questions_failing_gsl_wording_rules": base_gsl_report()}
    rep["passed_after_gsl"] = len(kept)
    rep["gsl"] = gsl_rep

    lint_dir = AP.AUTHOR_DIR / "lint"
    paths.write_json(lint_dir / "candidates.json", {"family": FAMILY, "candidates": kept})
    paths.write_json(lint_dir / "report.json", rep)
    paths.write_json(lint_dir / "gsl_drops.json", {"family": FAMILY, "g0_sha256": BL.G0_SHA256, "drops": drops})

    # The two independent polarity reads (separate seeds, separate chunks, same items; G0 H41).
    pa, pb = AP.polarity_batches(kept)
    if pa is None:
        raise RuntimeError("no paraphrase passed lint and G-SL: nothing to read")
    rows, files = [], {}
    for lab, bt in (("A", pa), ("B", pb)):
        f, r = AP.task_files(bt, AP.EXTRACT_DIR, title=f"Haiku polarity read {lab}", answer_format=AP.POLARITY_FORMAT,
                             kind_label=f"polarity:{lab}")
        files.update(f)
        rows += r
    xman = {"family": FAMILY, "stage": "extract (two independent polarity reads; G0 H41)", "seed": AP.SEED_POLARITY,
            "g0_sha256": BL.G0_SHA256, "n_tasks": len(rows), "n_pairs": len(kept),
            "batch_ids": [pa.batch_id, pb.batch_id], "next": "author_pool.py admit", "tasks": rows,
            "gsl_stage": "candidates passed author_pool.lint and gsl.lint_template (see lint/report.json)"}
    files["TASKS.json"] = json.dumps(xman, indent=1, ensure_ascii=False) + "\n"
    paths.write_files(AP.EXTRACT_DIR, files)

    return {"authoring_tasks": len(b.chunks), "authoring_answers": len(answered), "items": len(b.key),
            "questions_received": rep["questions"], "lint_passed": len(cands), "lint_dropped": rep["dropped"],
            "gsl": gsl_rep, "polarity_read_tasks": len(rows),
            "polarity_read_tasks_detail": [{k: r[k] for k in ("task_file", "answer_file", "kind", "n_items")} for r in rows],
            "polarity_batch_ids": [pa.batch_id, pb.batch_id]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=1, ensure_ascii=False, default=str))
