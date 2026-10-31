"""families/T29/pool_freeze.py: record the G-LEX and G3-H extraction answers, admit or quarantine every piece, and freeze the
T29 pools with a manifest (C2_DATA_SPEC 6.2 item 2 and 6.3; G0_SPEC 2; PREREG A37 (b) and A38). A new file. No rows.

  rebuild()  the authoring pieces after G-SL lint and dedup, the lexicon registry and the extraction tasks, rebuilt in
             memory by extract.py's own functions (nothing is written).
  check      every task, chunk, prompt, manifest and key file on disk is the same bytes as the rebuild, so every answer's
             qid maps to the same item. A difference stops the run.
  record     the answers of the three lexicon reads (glex-r1, glex-r2 for every form; glex-r3 for precedence) through
             chunker.load_answers. An answer whose meaning is one of the kind's choices is recorded with
             reg.record_extraction as one extraction by its task ("haiku:<task id>"). An answer that is not one of the
             choices is an invalid read: it is not recorded, the form stays pending and it is quarantined.
             Admission is reg.status: 2/2 distinct agreeing extractors (3/3 for precedence). Any other meaning rejects.
  g3h        the Mode F documents against the G3-H read (g3h-r1): g3h.compare with the expected requester (as written)
             and reason (the category key). A mismatch is always dropped. The 98% bar (g3h.template_report) is applied
             per template, and the template of a Mode F document is its register (the format its brief names): a
             register below 98% is quarantined whole.
  freeze     pools/ (packs, actions, skins, attack_lines, freeform, lexicon, wordings), pools/quarantine.jsonl and
             pools/MANIFEST.json (sha256 of every pool file, counts per kind and register, admitted vs the G0 targets,
             every shortfall). haiku/extract/recorded.json holds every recorded read. The G0 targets below are not lowered.

  ../.venv/bin/python -m families.T29.pool_freeze --dry-run   (from lean/c2_build: computes and prints, writes nothing)
  ../.venv/bin/python -m families.T29.pool_freeze             (writes, after A38)

Any mismatch between the rebuild and the on-disk files, or any missing, unreadable or incomplete answer file, stops the
run before anything is recorded or written.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from c2_kit import chunker, g3h, paths
from c2_kit import lexicon as LX
from families.T29 import authoring as A
from families.T29 import extract as E
from families.T29 import plugin as P

FAMILY = "T29"
HERE = Path(__file__).resolve().parent
ROOT = E.ROOT                                   # lean/c2_build/families/T29/haiku/extract
POOLS = HERE / "pools"
RECORDED = ROOT / "recorded.json"
LEX_READS = ("glex-r1", "glex-r2", "glex-r3")
G3H_READ = "g3h-r1"
REASON_KEY = {surface: key for key, surfaces in P.REASONS.items() for surface in surfaces}
PASS_RATE = g3h.PASS_RATE

# G0 targets. G0_SPEC.md states no pool counts; these are the family's own G0 section 2 floors, as encoded in
# test_authoring.py::test_planned_outputs_cover_the_g0_pools, plus the C2 3.0 minimums (30 wordings, >= 25 packs, >= 2
# held-out registers, >= 8 training registers). Where the test states a floor on planned outputs, the same number is
# applied to the kept (admitted) count: the stricter reading. None = report only (no G0 number). Not lowered.
G0 = {
    "packs": 75,                       # test: packs >= 75 (C2 3.0: >= 25 per family)
    "actions": 120,                    # test: action names >= 120
    "skins_training": 800,             # test: 8 training registers x 100
    "skins_held_out": 80,              # test: 2 held-out registers x 40
    "registers_training": 8,           # G0 2 / C2 3.0: >= 8 training registers
    "registers_held_out": 2,           # C2 3.0: >= 2 held-out registers
    "attack_lines": 60,                # test: attack lines >= 60
    "freeform_training": 100,          # test: Mode F training documents >= 100
    "freeform_held_out": None,         # report only: G0 states no held-out document number (24 planned)
    "lex_comparator": 60,              # test: comparator paraphrases >= 60
    "lex_precedence": 20,              # test: precedence paraphrases >= 20 (3/3)
    "lex_confirmation": 60,            # test: confirmation phrase bank >= 60
    "wordings_total": 30,              # C2 3.0 / G0 2: >= 30 wordings per family
    "wordings_training": 150,          # test: 30 x 5 (each card uses >= 5 wordings)
    "wordings_held_out": 30,           # test: >= 30 held-out wordings
    "wordings_per_form_training": 5,   # C2 3.0: each card uses >= 5 wordings, checked per question form
}


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_obj(o) -> str:
    return sha_text(json.dumps(o, sort_keys=True, ensure_ascii=False))


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def qform_of(sem_id: str) -> str:
    return sem_id.split(".")[-1]


def jsonl(rows: list) -> str:
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


def js(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# ================================================================================================ rebuild
def rebuild() -> dict:
    """The authoring pieces after lint and dedup, the registry and the extraction batches (in memory, deterministic)."""
    tasks = A.build_tasks()
    probs = A.check(tasks)
    if probs:
        raise SystemExit("STOP: authoring check failed: " + "; ".join(probs[:5]))
    groups, authored = E.collect(tasks)
    surv, lint_drops = E.lint_all(groups)
    surv, dup_drops = E.dedup_all(surv)
    reg, form_drops = E.build_registry(surv["lexicon"])
    batches, task_counts = E.make_tasks(reg, surv["freeform"])
    files, manifest = E.files_for(ROOT, batches)
    return {"authored": authored, "surv": surv, "lint_drops": lint_drops, "dup_drops": dup_drops, "reg": reg,
            "form_drops": form_drops, "batches": batches, "task_counts": task_counts, "files": files,
            "manifest": manifest}


def check_on_disk(files: dict) -> tuple:
    """(files compared, mismatching paths). Every rebuilt file must be the same bytes on disk."""
    bad = []
    for rel, text in sorted(files.items()):
        p = ROOT / rel
        if not p.is_file() or p.read_text(encoding="utf-8") != text:
            bad.append(rel)
    return len(files), bad


# ================================================================================================ load
def load_reads(batches: list) -> tuple:
    """({read: {"batch", "kind", "answers": {internal id: answer}}}, problems, {answer path: sha256})."""
    reads, problems, shas = {}, [], {}
    for read, kind, b in batches:
        raw = {}
        for c in b.chunks:
            tid = c["task_id"]
            rel = b.answer_path(tid)
            p = ROOT / rel
            if not p.is_file():
                problems.append(f"{read} {tid}: answer file missing")
                continue
            shas[rel] = sha_file(p)
            try:
                raw[tid] = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                problems.append(f"{read} {tid}: answer is not JSON: {e}")
        got, probs = chunker.load_answers(b, raw)
        problems += [f"{read}: {x}" for x in probs]
        reads[read] = {"batch": b, "kind": kind, "answers": got}
    return reads, problems, shas


def task_of_map(b) -> dict:
    return {b.key[q]: b.task_of[q] for q in b.key}


# ================================================================================================ G-LEX record
def record_lex(reg, reads: dict) -> tuple:
    """Record every valid lexicon answer as one extraction. Returns (invalid reads, recorded counts per read)."""
    invalid, n_rec = [], Counter()
    for read in LEX_READS:
        rd = reads[read]
        task_of = task_of_map(rd["batch"])
        for fid in sorted(rd["answers"]):
            ans = rd["answers"][fid]
            f = reg.forms[fid]
            meaning = ans.get("meaning") if isinstance(ans, dict) else None
            sem = reg.meaning_to_sem(f.kind, meaning) if isinstance(meaning, str) else None
            if sem is None:
                invalid.append({"stage": "extract-invalid", "task": read, "iid": fid, "task_id": task_of[fid],
                                "reason": f"meaning is not one of the {f.kind} choices: {str(meaning)[:160]!r}"})
                continue
            reg.record_extraction(fid, f"haiku:{task_of[fid]}", sem)
            n_rec[read] += 1
    return invalid, n_rec


def recorded_view(reg, reads: dict) -> list:
    seen = defaultdict(list)
    for read in LEX_READS:
        rd = reads[read]
        task_of = task_of_map(rd["batch"])
        for fid, ans in rd["answers"].items():
            seen[fid].append({"read": read, "task_id": task_of[fid],
                              "meaning": ans.get("meaning") if isinstance(ans, dict) else None})
    rows = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        rows.append({"form_id": fid, "kind": f.kind, "sem_id": f.sem_id, "text": f.text, "status": reg.status(fid),
                     "haiku_task_id": f.haiku_task_id,
                     "extractions": [{"extractor": e, "sem_id": s} for e, s in f.extractions],
                     "reads": sorted(seen.get(fid, []), key=lambda r: r["read"])})
    return rows


# ================================================================================================ G3-H
def g3h_fields() -> list:
    return list(E.G3H_FIELDS)


def expected_facts(p: dict) -> dict:
    """The generator's facts for one Mode F document: requester as written, reason as its category key."""
    facts = p["facts"]
    return {"requester": facts["REQUESTER"], "reason": REASON_KEY[facts["REASON"]]}


def g3h_stage(rd: dict, freeform: list) -> tuple:
    """(kept documents, G3-H report, drops). Every document is compared; a template below 98% is quarantined whole."""
    fields = g3h_fields()
    by_pid = {p["pid"]: p for p in freeform}
    results, drops, wrong = [], [], {}
    for iid in sorted(by_pid):
        if iid not in rd["answers"]:
            raise SystemExit(f"STOP: G3-H answer missing for {iid}")
        p = by_pid[iid]
        ok, diffs = g3h.compare(expected_facts(p), rd["answers"][iid], fields)
        results.append((p["register"], iid, ok))
        if not ok:
            wrong[iid] = diffs
    rep = g3h.template_report(results)
    quarantined = set(rep["quarantined"])
    kept, drop_rows = [], []
    for iid in sorted(by_pid):
        p = by_pid[iid]
        if iid in wrong:
            drop_rows.append({"stage": "g3h", "task": G3H_READ, "iid": iid, "task_id": p["task_id"],
                              "reason": "G3-H mismatch: " + "; ".join(wrong[iid])[:240]})
        elif p["register"] in quarantined:
            drop_rows.append({"stage": "g3h-template", "task": G3H_READ, "iid": iid, "task_id": p["task_id"],
                              "reason": f"register {p['register']} below {PASS_RATE:.0%} "
                                        f"({rep['templates'][p['register']]['ok']}/"
                                        f"{rep['templates'][p['register']]['n']}); template quarantined"})
        else:
            kept.append(p)
    return kept, rep, drop_rows


# ================================================================================================ freeze
def freeze_packs(packs: list) -> list:
    out = []
    for p in sorted(packs, key=lambda p: p["pid"]):
        pk = p["pack"]
        out.append({"pool_id": p["pid"], "held_out": bool(p["held_out"]), "task_id": p["task_id"],
                    "org_domain": pk.get("org_domain"), "pack_sha256": sha_obj(pk), "pack": pk})
    return out


def freeze_actions(acts: list) -> list:
    out = []
    for p in sorted(acts, key=lambda p: p["pid"]):
        out.append({"pool_id": p["pid"], "name": p["text"], "effect": p["effect"], "tone": p["tone"],
                    "held_out": bool(p["held_out"]), "task_id": p["task_id"], "text_sha256": sha_text(p["text"])})
    return out


def freeze_skins(skins: list) -> list:
    out = []
    for p in sorted(skins, key=lambda p: p["pid"]):
        out.append({"skin_id": f"SK-T29-{p['register'].upper()}-{sha_text(p['text'])[:8]}", "pool_id": p["pid"],
                    "register": p["register"], "escape": p["escape"], "slots": p["decl"],
                    "held_out": bool(p["held_out"]), "task_id": p["task_id"], "text_sha256": sha_text(p["text"]),
                    "text": p["text"]})
    dup = [k for k, v in Counter(s["skin_id"] for s in out).items() if v > 1]
    if dup:
        raise SystemExit(f"STOP: skin ids collide: {dup[:3]}")
    return out


def freeze_attacks(atk: list) -> list:
    out = [{"attack_id": f"AT-T29-{sha_text(p['text'])[:8]}", "pool_id": p["pid"], "task_id": p["task_id"],
            "slots": p["decl"], "text_sha256": sha_text(p["text"]), "text": p["text"]}
           for p in sorted(atk, key=lambda p: p["pid"])]
    dup = [k for k, v in Counter(s["attack_id"] for s in out).items() if v > 1]
    if dup:
        raise SystemExit(f"STOP: attack ids collide: {dup[:3]}")
    return out


def freeze_freeform(kept: list) -> list:
    return [{"doc_id": p["pid"], "register": p["register"], "held_out": bool(p["held_out"]),
             "task_id": p["task_id"], "facts": p["facts"], "text_sha256": sha_text(p["text"]), "text": p["text"],
             "g3h": "match"}
            for p in sorted(kept, key=lambda p: p["pid"])]


def admitted_ids(reg) -> list:
    return [fid for fid in sorted(reg.forms) if reg.status(fid) == "admitted"]


def freeze_lexicon(reg) -> tuple:
    """(lexicon object with admitted forms only, G-LEX gate). The object is re-read through from_json, which re-runs
    every unit test and the extraction status on the pool itself."""
    obj = reg.to_json()
    obj["forms"] = [x for x in obj["forms"] if x["status"] == "admitted"]
    chk = LX.LexiconRegistry.from_json(obj)
    return obj, chk.gate()


def freeze_wordings(reg, adm: list) -> list:
    out = []
    for fid in adm:
        f = reg.forms[fid]
        if f.kind != "question":
            continue
        out.append({"form_id": fid, "qform": qform_of(f.sem_id), "sem_id": f.sem_id, "text": f.text,
                    "held_out": bool(f.held_out), "status": "admitted", "haiku_task_id": f.haiku_task_id,
                    "haiku_prompt_sha": f.haiku_prompt_sha,
                    "extractions": [{"extractor": e, "sem_id": s} for e, s in f.extractions],
                    "text_sha256": sha_text(f.text)})
    return out


def quarantine_rows(lint_drops: list, dup_drops: list, form_drops: list, invalid: list, reg, g3_rows: list) -> list:
    out = []
    for d in lint_drops:
        out.append({"stage": "lint", "task": d["group"], "iid": d["pid"], "task_id": d["task_id"],
                    "reason": "; ".join(d["reasons"])[:240]})
    for d in dup_drops:
        out.append({"stage": "dedup", "task": d["group"], "iid": d["pid"], "task_id": d["task_id"],
                    "reason": "; ".join(d["reasons"])[:240]})
    for d in form_drops:
        out.append({"stage": "form", "task": d["group"], "iid": d["pid"], "task_id": d["task_id"],
                    "reason": "; ".join(d["reasons"])[:240]})
    out += invalid
    out += g3_rows
    for fid in sorted(reg.forms):
        st = reg.status(fid)
        if st != "admitted":
            f = reg.forms[fid]
            out.append({"stage": "g-lex", "task": f.kind, "iid": fid, "task_id": f.haiku_task_id,
                        "reason": f"{st}: extractions {[[e, s] for e, s in f.extractions]} "
                                  f"(needs {f.required} agreeing extractors for sem {f.sem_id})"})
    return out


# ================================================================================================ targets
def targets(c: dict) -> tuple:
    """(rows, shortfalls). Each row: item, got, target, op, met, source. A target is never lowered."""
    rows = []

    def add(item, got, target, source, op=">="):
        met = None if target is None else (got >= target if op == ">=" else got == target)
        rows.append({"item": item, "got": got, "target": target, "op": op, "met": met, "source": source})

    add("packs (kept)", c["packs"], G0["packs"], "G0 section 2 floor, test_authoring (C2 3.0: >= 25)")
    add("action names (kept)", c["actions"], G0["actions"], "G0 section 2 floor, test_authoring")
    add("skins, training (kept, Mode T)", c["skins_training"], G0["skins_training"], "test_authoring: 8 x 100")
    add("skins, held-out (kept, Mode T)", c["skins_held_out"], G0["skins_held_out"], "test_authoring: 2 x 40")
    add("training registers with >= 1 skin", c["registers_training"], G0["registers_training"],
        "G0 section 2 / plugin REGISTERS")
    add("held-out registers with >= 1 skin", c["registers_held_out"], G0["registers_held_out"], "C2 3.0")
    add("attack lines (kept)", c["attack_lines"], G0["attack_lines"], "test_authoring")
    add("Mode F documents, training (kept after G3-H)", c["freeform_training"], G0["freeform_training"],
        "test_authoring: >= 100")
    add("Mode F documents, held-out (kept after G3-H)", c["freeform_held_out"], G0["freeform_held_out"],
        "report only (24 planned; no G0 number)", op=">=")
    add("comparator forms admitted (2/2)", c["admitted"]["comparator"], G0["lex_comparator"], "test_authoring")
    add("precedence forms admitted (3/3)", c["admitted"]["precedence"], G0["lex_precedence"], "test_authoring")
    add("confirmation forms admitted (2/2)", c["admitted"]["confirmation"], G0["lex_confirmation"], "test_authoring")
    add("question wordings admitted, total", c["wordings_total"], G0["wordings_total"], "C2 3.0 / G0 2: >= 30")
    add("question wordings admitted, training", c["wordings_training"], G0["wordings_training"], "test_authoring 30 x 5")
    add("question wordings admitted, held-out", c["wordings_held"], G0["wordings_held_out"], "test_authoring: >= 30")
    add("question wordings, lowest training form", c["wordings_min_form"], G0["wordings_per_form_training"],
        "C2 3.0: each card uses >= 5 (checked per form)")
    short = [r for r in rows if r["met"] is False]
    return rows, short


# ================================================================================================ main
def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in argv
    paths.require_a38()
    st = rebuild()
    reg = st["reg"]

    n_chk, bad = check_on_disk(st["files"])
    if bad:
        raise SystemExit(f"STOP: rebuilt task files differ from disk ({len(bad)}): {bad[:5]}")
    reads, probs, ans_sha = load_reads(st["batches"])
    if probs:
        raise SystemExit(f"STOP: extraction answers are incomplete or unreadable: {probs[:8]}")
    n_answers = {read: len(rd["answers"]) for read, rd in reads.items()}

    invalid, n_rec = record_lex(reg, reads)
    stat = Counter(reg.status(fid) for fid in reg.forms)
    adm = admitted_ids(reg)
    adm_kind = Counter(reg.forms[f].kind for f in adm)
    q_adm = [f for f in adm if reg.forms[f].kind == "question"]
    wordings = freeze_wordings(reg, adm)
    lex_obj, gate = freeze_lexicon(reg)

    kept_ff, g3_rep, g3_rows = g3h_stage(reads[G3H_READ], st["surv"]["freeform"])
    wider = {p["pid"]: E.lint_freeform_word_list(p) for p in kept_ff}
    wider = {k: v for k, v in wider.items() if v}
    surv = st["surv"]
    skins_all = surv["skins"]
    per_form_train = Counter(w["qform"] for w in wordings if not w["held_out"])
    per_form_held = Counter(w["qform"] for w in wordings if w["held_out"])
    c = {
        "packs": len(surv["packs"]),
        "actions": len(surv["actions"]),
        "skins_training": sum(1 for p in skins_all if not p["held_out"]),
        "skins_held_out": sum(1 for p in skins_all if p["held_out"]),
        "registers_training": len({p["register"] for p in skins_all if not p["held_out"]}),
        "registers_held_out": len({p["register"] for p in skins_all if p["held_out"]}),
        "attack_lines": len(surv["attack"]),
        "freeform_training": sum(1 for p in kept_ff if not p["held_out"]),
        "freeform_held_out": sum(1 for p in kept_ff if p["held_out"]),
        "admitted": {k: adm_kind.get(k, 0) for k in ("comparator", "precedence", "confirmation")},
        "wordings_total": len(q_adm),
        "wordings_training": sum(1 for f in q_adm if not reg.forms[f].held_out),
        "wordings_held": sum(1 for f in q_adm if reg.forms[f].held_out),
        "wordings_min_form": min((per_form_train.get(q, 0) for q in P.T29Plugin.V1_QFORMS), default=0),
    }
    rep, short = targets(c)
    quar = quarantine_rows(st["lint_drops"], st["dup_drops"], st["form_drops"], invalid, reg, g3_rows)

    skins_out = freeze_skins(skins_all)
    counts = {
        "authored_pieces": dict(st["authored"]),
        "authored_total": sum(st["authored"].values()),
        "lint_dropped_by_group": dict(Counter(d["group"] for d in st["lint_drops"])),
        "dedup_dropped_by_group": dict(Counter(d["group"] for d in st["dup_drops"])),
        "survivors_by_group": {g: len(v) for g, v in surv.items()},
        "packs_kept": c["packs"],
        "actions_kept": c["actions"],
        "skins_kept_by_register": dict(Counter(p["register"] for p in skins_all)),
        "skins_kept_training": c["skins_training"],
        "skins_kept_held_out": c["skins_held_out"],
        "attack_lines_kept": c["attack_lines"],
        "freeform_survived_lint_dedup": len(surv["freeform"]),
        "freeform_g3h_mismatch": sum(1 for d in g3_rows if d["stage"] == "g3h"),
        "freeform_g3h_template_quarantined": sum(1 for d in g3_rows if d["stage"] == "g3h-template"),
        "freeform_kept": len(kept_ff),
        "freeform_kept_by_register": dict(Counter(p["register"] for p in kept_ff)),
        "g3h_template_rates": g3_rep["templates"],
        "g3h_quarantined_registers": g3_rep["quarantined"],
        "lexicon_forms_in_registry": len(reg.forms),
        "lexicon_forms_by_kind": dict(Counter(f.kind for f in reg.forms.values())),
        "lexicon_form_status": dict(stat),
        "lexicon_admitted_by_kind": dict(adm_kind),
        "lexicon_recorded_per_read": dict(n_rec),
        "lexicon_invalid_reads": len(invalid),
        "wordings_admitted_by_form_training": dict(per_form_train),
        "wordings_admitted_by_form_held_out": dict(per_form_held),
        "lint_drop_reasons_by_rule": dict(Counter(r.split(":", 1)[0] for d in st["lint_drops"]
                                                   for r in d["reasons"]).most_common()),
        "quarantine_rows": len(quar),
        "quarantine_by_stage": dict(Counter(q["stage"] for q in quar)),
        "rows_generated": 0,
    }
    gate_ok = bool(gate["pass"]) and gate["n_forms"] == len(adm)

    summary = {"dry_run": dry, "task_files_checked": n_chk, "answers_per_read": n_answers,
               "lexicon_recorded_per_read": dict(n_rec), "lexicon_form_status": dict(stat),
               "g_lex_gate": {k: gate[k] for k in ("gate", "n_forms", "status_counts", "pass")},
               "g3h_report": {"templates": g3_rep["templates"], "quarantined": g3_rep["quarantined"]},
               "counts": counts, "targets": rep, "shortfalls": short}
    print(json.dumps(summary, indent=1, ensure_ascii=False, default=str))
    if dry:
        return 0

    recorded = recorded_view(reg, reads)
    paths.write_json(RECORDED, recorded)

    files = {
        "packs.jsonl": jsonl(freeze_packs(surv["packs"])),
        "actions.jsonl": jsonl(freeze_actions(surv["actions"])),
        "skins.jsonl": jsonl(skins_out),
        "attack_lines.jsonl": jsonl(freeze_attacks(surv["attack"])),
        "freeform.jsonl": jsonl(freeze_freeform(kept_ff)),
        "wordings.jsonl": jsonl(wordings),
        "lexicon.json": js(lex_obj),
        "quarantine.jsonl": jsonl(quar),
    }
    records = {rel: len(text.splitlines()) for rel, text in files.items() if rel.endswith(".jsonl")}
    records["lexicon.json"] = len(lex_obj["forms"])
    shas = {}
    for rel, text in sorted(files.items()):
        paths.write_text(POOLS / rel, text)
        shas[rel] = sha_text(text)

    manifest = {
        "family": FAMILY,
        "tier": P.T29Plugin.TIER,
        "frozen_on": "2026-10-13",
        "a38_present": paths.a38_frozen(),
        "g0_spec": {"path": "families/T29/G0_SPEC.md", "sha256": sha_file(HERE / "G0_SPEC.md"),
                    "matches_plugin_G0_SHA256": sha_file(HERE / "G0_SPEC.md") == P.T29Plugin.G0_SHA256},
        "g0_targets": G0,
        "inputs": {"authoring_answers": {f"haiku/author/answers/{x.name}": sha_file(x) for x in
                                         sorted((A.ROOT / "answers").glob("T29-*.json"))},
                   "extraction_answers": dict(sorted(ans_sha.items())),
                   "extraction_reads": {read: b.batch_id for read, _k, b in st["batches"]}},
        "code": {f"families/T29/{n}": sha_file(HERE / n) for n in
                 ("pool_freeze.py", "extract.py", "authoring.py", "plugin.py")}
                | {f"c2_kit/{n}": sha_file(HERE.parent.parent / "c2_kit" / n)
                   for n in ("lexicon.py", "g3h.py", "chunker.py", "gsl.py")},
        "counts": counts,
        "targets": rep,
        "shortfalls": short,
        "g_lex_gate": gate,
        "g3h": {"rule": "per document; template = register (98% bar, g3h.template_report); mismatches always dropped",
                "templates": g3_rep["templates"], "quarantined": g3_rep["quarantined"]},
        "freeform_wider_outside_slot_flags": {
            "rule": "extract.lint_freeform_word_list: the Mode T outside-slot word lists (C2 6.3 G-SL) applied to the "
                    "kept Mode F documents. Informational: NOT applied as a drop (G0 section 2: Mode F = fact-lock + G3-H)",
            "kept_docs": len(kept_ff),
            "docs_with_hits": len(wider),
            "clean_docs": len(kept_ff) - len(wider),
            "hits_by_category": dict(Counter(r.split(":", 1)[0] for v in wider.values() for r in v).most_common()),
            "doc_ids": sorted(wider),
        },
        "pool_files": {rel: {"sha256": shas[rel], "records": records[rel]} for rel in sorted(shas)},
        "decisions": [
            "Extractor id per answer is haiku:<task id>. Each lexicon read is its own chunk set, so each form has one "
            "extraction per read: 2/2 for comparator, question and confirmation, 3/3 for precedence.",
            "An answer that is not one of the kind's listed choices is an invalid read: not recorded, the form stays "
            "pending, and it is quarantined (stage extract-invalid).",
            "A form whose recorded extraction picks another sem id is rejected for good (lexicon.status).",
            "G3-H: each Mode F document is compared with g3h.compare (requester as written; reason as its category "
            "key). A mismatch is dropped. The 98% bar is applied per register (the template of a Mode F document).",
            "OPEN DECISION (orchestrator / owner): 66 of the 70 kept Mode F documents carry outside-slot word-list hits "
            "(modal, quantifier, status, operator, quantity, hedge; see freeform_wider_outside_slot_flags). They are kept "
            "because the family's G0 section 2 and extract.py apply the fact-lock alone to Mode F. If C2 6.3 G-SL applies "
            "the wider list to Mode F, these documents are dropped and only the clean documents remain.",
            "Lexicon wordings: held-out split is the task's own held_out flag (word-held), not a random split.",
            "No row is generated. The pools are the inputs of the later generator run, which needs its own G13-seed step.",
            "NOT VERIFIED ON DISK: the per-agent file-access audit (c2_kit/audit.py, README Haiku task flow step 4) for the "
            "21 extraction tasks. The extraction agents returned files_opened flags to the workflow runtime only; no audit "
            "record is in haiku/extract/. A failed audit discards that agent's answers, so the audit must be confirmed "
            "(and any failed task's forms re-read) before these pools feed a generator run.",
        ],
    }
    manifest_text = js(manifest)
    paths.write_text(POOLS / "MANIFEST.json", manifest_text)
    print(json.dumps({"written": sorted(files) + ["MANIFEST.json"], "recorded": str(RECORDED),
                      "manifest_sha256": sha_text(manifest_text), "gate_ok": gate_ok,
                      "shortfalls": len(short)}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
