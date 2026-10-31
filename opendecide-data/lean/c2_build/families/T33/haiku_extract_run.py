"""families/T33/haiku_extract_run.py: G-SL on the claim and check clauses, then the G-LEX extraction tasks (A37 b;
C2_DATA_SPEC 6.3; G0_SPEC 3 G-LEX). A new file: haiku_author.py is not changed.

Why: haiku_author.load_pieces() lints skins, attack lines and question wordings, but not the claim and check clauses
(kinds "other" and "status"). This run lints every clause before any extraction task is written. A failing clause is
logged with its rules and is never sent to G-LEX, so it stays "pending" (never admitted, so no row can use it). Forms
that pass go to G-LEX, two reads each (no T33 form is kind precedence or window, so none needs three reads). Each read
is its own batch of chunks, and every chunk is one file written through paths.write_files.

Lint role (G0_SPEC section 7, redo2, B1-B3): the first run (13 Oct, haiku/lint/GSL_CLAUSE_DROPS.json) used role
"skin", which bans words G0 section 3 requires in the clauses ("done", "no more than", "refunded"). A clause is a
lexicon form that the program fills into a {K}/{CHK} slot and G-LEX admits, so it now gets the kit's role for
G-LEX-admitted lexicon text, "wording" (as in T01 and T29), plus the gold-label words and phrases (S22). The clauses
the first run passed are already in haiku/extract/ (6 reads); the clauses it dropped and the redo2 forms are sent by
families/T33/redo2.py. --write refuses while haiku/extract/TASKS.json exists, so those 6 reads keep their batches.

Run from lean/c2_build. Dry run first (nothing is written):
  ../../.venv/bin/python -m families.T33.haiku_extract_run
Then write (guarded: needs the A38 freeze, and writes only under haiku/extract/ and haiku/lint/):
  ../../.venv/bin/python -m families.T33.haiku_extract_run --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from c2_kit import chunker, gsl, paths
from c2_kit import skin as K
from c2_kit.skin import make_skin

from . import haiku_author as H
from . import plugin as T

F = H.F
VERSION = H.VERSION
HAIKU = H.HAIKU
EXTRACT = H.EXTRACT
LINT = HAIKU / "lint"
P = T.T33Plugin
CLAUSE_KINDS = ("other", "status")      # claim paraphrases ("other") and check paraphrases ("status")


def clause_lint(f) -> list:
    """G-SL on one lexicon clause: role "wording" (the kit's role for G-LEX-admitted lexicon text: placeholders,
    grammar, numbers, dates, relative time, hedges, names, signs) plus the gold-label words and phrases (G0 S22).
    GSL_EXCEPTIONS stay none. Returns the violation strings."""
    sk = make_skin(f"lint-{f.form_id}", F, f.text, dict(f.slots), kind="wording", register="clause")
    out = [f"{v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=P.LABEL_WORDS, exceptions=P.GSL_EXCEPTIONS, name_allow=P.NAME_ALLOW)]
    mark = K.PH_RE.sub(gsl._MARK, f.text)
    out += [f"{v.rule}: {v.detail}" for v in gsl._word_hits(mark, {"gold_label"}, P.LABEL_WORDS, {}, ())]
    return out


def _rule_tag(v: str) -> str:
    rule, _, detail = v.partition(": ")
    if rule == "grammar" and "rows" in detail:
        return "grammar:unit word after count (rows)"
    return rule if rule != "grammar" else "grammar:" + detail.split(":")[0]


def _forbid_in(text: str) -> list:
    low = text.lower()
    return [s for s in H.FORBID if s and re.search(r"(?<![a-z0-9])" + re.escape(s.lower()) + r"(?![a-z0-9])", low)]


def build(pieces: dict | None = None) -> dict:
    """Lint the clauses, hold forbidden-string forms, select the forms and make the batches. Nothing is written."""
    pieces = pieces or H.load_pieces()
    reg = pieces["registry"]
    drops, lint_ok = {}, Counter()
    for fid, f in sorted(reg.forms.items()):
        if f.kind not in CLAUSE_KINDS:
            continue
        v = clause_lint(f)
        if v:
            drops[fid] = {"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text, "rules": v}
            lint_ok["fail"] += 1
        else:
            lint_ok["pass"] += 1
    cand = sorted(fid for fid, f in reg.forms.items() if f.unit_ok and fid not in drops)
    not_pending = sorted(fid for fid in cand if reg.status(fid) != "pending")
    if not_pending:
        raise RuntimeError(f"forms with a status other than pending before G-LEX: {not_pending[:5]}")
    # What a G-LEX reader would see: the rendered form and the full meaning list of its kind. A form whose item holds a
    # label word or a question / option string is held (README Haiku flow: forbid_strings = LABEL_WORDS + questions).
    held, fids = {}, []
    for fid in cand:
        it = reg.lexicon_items([fid], seed=f"{F}-glex-{VERSION}-screen")[0][1]
        hit_text = _forbid_in(it["text"])
        hit_choice = sorted({s for m in it["choices"] for s in _forbid_in(m)})
        if hit_text or hit_choice:
            held[fid] = {"form_id": fid, "sem_id": reg.forms[fid].sem_id, "kind": reg.forms[fid].kind,
                         "rendered_text": it["text"], "forbidden_in_text": hit_text,
                         "forbidden_in_choices": hit_choice}
        else:
            fids.append(fid)
    n_reads = max(reg.forms[f].required for f in fids)
    batches = []
    for r in range(n_reads):
        sel = [f for f in fids if reg.forms[f].required > r]
        items = reg.lexicon_items(sel, seed=f"{F}-glex-{VERSION}-r{r}")
        b = chunker.make_batch("extract_lex", F, items, seed=f"{F}-glex-{VERSION}-read{r}", prompt=H.EXTRACT_PROMPT,
                               forbid_strings=H.FORBID)
        for c in b.chunks:
            c["instructions"] = H.EXTRACT_PROMPT
            c["answer_file"] = str(Path(EXTRACT) / b.answer_path(c["task_id"]))
        batches.append((f"read{r}", b, len(sel)))
    # belt and braces: no sent item may carry a forbidden string (checked on the chunk text Haiku will read)
    hits = []
    for name, b, _n in batches:
        for c in b.chunks:
            blob = json.dumps(c["items"], ensure_ascii=False)
            hits += [(name, c["task_id"], s) for s in _forbid_in(blob)]
    return {"pieces": pieces, "drops": drops, "held": held, "lint": lint_ok, "fids": fids, "batches": batches,
            "hits": hits, "n_reads": n_reads}


def summarise(res: dict) -> dict:
    reg = res["pieces"]["registry"]
    tags = Counter(_rule_tag(v) for d in res["drops"].values() for v in d["rules"])
    per_sem = Counter(d["sem_id"].split("#")[0] for d in res["drops"].values())
    fids = res["fids"]
    return {
        "family": F, "version": VERSION,
        "forms_in_registry": len(reg.forms),
        "clause_forms_linted": res["lint"]["pass"] + res["lint"]["fail"],
        "clause_forms_gsl_pass": res["lint"]["pass"],
        "clause_forms_gsl_fail": res["lint"]["fail"],
        "clause_gsl_fail_rule_tags": dict(tags.most_common()),
        "clause_gsl_fail_by_sem": dict(sorted(per_sem.items())),
        "forms_held_forbidden_string": len(res["held"]),
        "forms_held_by_kind": dict(Counter(d["kind"] for d in res["held"].values())),
        "forms_held_forbidden_in_choices": sum(1 for d in res["held"].values() if d["forbidden_in_choices"]),
        "forms_held_forbidden_in_text": sum(1 for d in res["held"].values() if d["forbidden_in_text"]),
        "forms_sent_to_glex": len(fids),
        "forms_by_kind": dict(Counter(reg.forms[f].kind for f in fids)),
        "reads_per_form": {"required_max": res["n_reads"]},
        "batches": {name: {"batch_id": b.batch_id, "items": n, "chunks": len(b.chunks)} for name, b, n in res["batches"]},
        "chunks_total": sum(len(b.chunks) for _n, b, _k in res["batches"]),
        "extraction_items_total": sum(n for _n, _b, n in res["batches"]),
        "forbid_string_hits_in_items": len(res["hits"]),
        "forbid_string_hit_examples": res["hits"][:5],
    }


def write(res: dict) -> dict:
    files, tasks = {}, []
    for name, b, _n in res["batches"]:
        files.update(b.files())
        tasks += [{"task_file": str(EXTRACT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                   "kind": f"extract_lex:{name}"} for c in b.chunks]
    files["TASKS.json"] = json.dumps({"family": F, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {name: b.batch_id for name, b, _n in res["batches"]},
                                      "source": "families/T33/haiku_extract_run.py (G-SL on clauses first)"},
                                     indent=1) + "\n"
    paths.write_files(EXTRACT, files)
    drop_log = {"family": F, "version": VERSION,
                "gate": "G-SL (role wording + gold-label words; G0 section 7) on claim and check clauses",
                "n_failed": len(res["drops"]), "n_passed": res["lint"]["pass"],
                "not_sent_to_glex": sorted(res["drops"]), "forms": [res["drops"][k] for k in sorted(res["drops"])]}
    held_log = {"family": F, "version": VERSION,
                "rule": "README Haiku flow: no item may carry LABEL_WORDS or question / option strings (FORBID)",
                "n_held": len(res["held"]), "not_sent_to_glex": sorted(res["held"]),
                "forms": [res["held"][k] for k in sorted(res["held"])]}
    paths.write_files(HAIKU, {
        "lint/GSL_CLAUSE_DROPS.json": json.dumps(drop_log, ensure_ascii=False, indent=1) + "\n",
        "lint/FORBIDDEN_HELD.json": json.dumps(held_log, ensure_ascii=False, indent=1) + "\n"})
    return {"tasks": tasks}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write the chunks (needs the A38 freeze)")
    a = ap.parse_args(argv)
    res = build()
    out = summarise(res)
    if res["hits"]:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        print("STOP: label or question strings appear in extraction items; nothing written", file=sys.stderr)
        return 2
    if not a.write:
        out["mode"] = "dry run (nothing written)"
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    if (EXTRACT / "TASKS.json").exists():
        print("STOP: haiku/extract/TASKS.json exists (the round-1 reads are keyed to its batches); new reads go "
              "through families/T33/redo2.py", file=sys.stderr)
        return 3
    got = write(res)
    out["mode"] = "written"
    out["tasks"] = got["tasks"]
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
