"""transfer/T36/freeze.py: record the T36 extraction answers, admit or quarantine, and freeze the pools.

Runs after the extraction round (haiku/extract/answers/: 7 tasks, 6 G-LEX readings in two reads and 1 G3-H read).
Every write goes through paths.write_files, which refuses before A38 and on never-open paths. Nothing here
generates rows: the pools are frozen first and the rows come later.

Steps (C2_DATA_SPEC 6.3; G0_SPEC.md v2 sections 6 and 7; PREREG A37 (b), A38):
  1. rebuild  extract.py's batches (deterministic) and check every chunk, key and manifest file against disk
  2. load     the returned answers through chunker.load_answers (each qid answered once, inside its own task)
  3. G-LEX    record every reading with lexicon.record_extraction (extractor = the Haiku task id). A form is
              ADMITTED at 2/2 distinct agreeing readings (T36 has no precedence or window kind: 2/2 for all)
  4. G3-H     g3h.compare on every Mode F document. The template is the document (one document = one skin, the
              kit's convention); g3h.template_report quarantines a document below 98% and drops mismatched rows
  5. packs    a seeded split of the surviving packs into training and held-out (G0 R19: >= 25 training, >= 5
              held-out). load_pools() leaves every pack in training, so the split is made here
  6. checks   H32 (each Mode T skin: {PROJECT}, {PERSON}, {PKG} exactly once; attack lines: {PERSON} once and
              {PKG} at most once); the Mode F cap (at most 1 document per 3 Mode T skins of the same held-out status)
  7. freeze   pools/: skins.json, attacks.json, documents.json, wordings.json, lexicon.json, packs.json,
              quarantine.json, MANIFEST.json (sha256s, counts, targets, shortfalls, pending gates)

  cd lean && ../.venv/bin/python c2_build/transfer/T36/freeze.py            (dry run: counts and checks, writes nothing)
  cd lean && ../.venv/bin/python c2_build/transfer/T36/freeze.py --write    (after A38: writes pools/ and verifies them)
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from transfer.T36 import authoring as A  # noqa: E402
from transfer.T36 import extract as E  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
VERSION = "v1"
POOLS = HERE / "pools"
EXTRACT = E.ROOT
READS = ("glex-r1", "glex-r2")
N_HELD_PACKS = 5                                   # G0 R19 floor; the split is seeded by pack key
TRAIN_REGISTERS = tuple(A.TRAIN_REGISTERS)
HELD_REGISTERS = tuple(A.HELD_REGISTERS)
G3H_BAR = g3h.PASS_RATE                            # 0.98, never loosened
EXPECTED_TASKS = 7
EXPECTED_OUTPUTS = 270

# G0_SPEC.md section 6 targets. Do not lower them: a shortfall is reported, never absorbed.
TARGETS = {
    "packs_train": 25,
    "packs_held": 5,
    "skin": {r: 20 for r in TRAIN_REGISTERS},
    "skin_heldout": {r: 20 for r in HELD_REGISTERS},
    "attack": 40,
    "freeform": {r: 4 for r in TRAIN_REGISTERS},
    "freeform_heldout": {r: 5 for r in HELD_REGISTERS},
    "wording": {"ch_pick": 18, "yn_meets": 18, "yn_outside": 6, "yn_not_meets": 6, "yn_fails": 6},
}

POOL_FILES = ("skins.json", "attacks.json", "documents.json", "wordings.json", "lexicon.json", "packs.json",
              "quarantine.json")


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _norm(s) -> str:
    return " ".join(str(s).casefold().split())


# ------------------------------------------------------------------------------------------------ 1-2. rebuild, load

def rebuild() -> dict:
    """Regenerate every batch from the pools and check each file against the copy on disk (drift refuses)."""
    col = E.collect()
    recs, lint_drops = E.extra_lint(col["recs"])
    recs, dup_drops = E.dedup_all(recs)
    reg, fids, form_drops = E.build_registry(recs.get("wording", []))
    fields = E.g3h_fields()
    g3_recs = sorted(recs.get("freeform", []) + recs.get("freeform_heldout", []), key=lambda r: r["pid"])
    g3_items = [(f"g3h|{r['pid']}", g3h.extraction_item(r["obj"].text, fields)) for r in g3_recs]
    batches = E.make_batches(reg, g3_items)
    files, index = E.files_and_index(batches)
    drift = [rel for rel, text in files.items()
             if not (EXTRACT / rel).exists() or (EXTRACT / rel).read_text(encoding="utf-8") != text]
    if drift:
        raise SystemExit(f"extraction files drifted from the regenerated batches: {drift[:5]}")
    return {"col": col, "recs": recs, "lint_drops": lint_drops, "dup_drops": dup_drops, "reg": reg, "fids": fids,
            "form_drops": form_drops, "fields": fields, "g3_recs": g3_recs, "g3_items": g3_items,
            "batches": batches, "index": index}


def read_answers(batch) -> tuple:
    """(internal id -> answer, problems, missing task ids) for one batch, from its answer files on disk."""
    raw, missing = {}, []
    for c in batch.chunks:
        f = EXTRACT / batch.answer_path(c["task_id"])
        if not f.exists():
            missing.append(c["task_id"])
            continue
        raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
    got, probs = chunker.load_answers(batch, raw)
    return got, probs, missing


# ------------------------------------------------------------------------------------------------ 3. G-LEX

def record_glex(reg, batch, got: dict) -> dict:
    """Record one G-LEX reading per form. The extractor is the Haiku task that answered it. A meaning that is not on
    the kind's closed list records None, which rejects the form (G-LEX: any disagreement rejects for good)."""
    task_of = {iid: batch.task_of[q] for q, iid in batch.key.items()}
    stats = Counter()
    for fid in sorted(got):
        f = reg.forms[fid]
        meaning = got[fid].get("meaning") if isinstance(got[fid], dict) else None
        sems = [s for s in reg.sems.values() if s.kind == f.kind]
        exact = [s.sem_id for s in sems if isinstance(meaning, str) and s.meaning == meaning]
        loose = [s.sem_id for s in sems if isinstance(meaning, str) and _norm(s.meaning) == _norm(meaning)]
        if exact:
            sem, how = exact[0], "exact"
        elif len(loose) == 1:
            sem, how = loose[0], "case_or_spacing"
        else:
            sem, how = None, "not_listed"
        reg.record_extraction(fid, f"haiku:{task_of[fid]}", sem)
        stats[how] += 1
        stats["agrees" if sem == f.sem_id else "other_or_none"] += 1
    return dict(stats)


# ------------------------------------------------------------------------------------------------ 4. G3-H

def g3h_compare(g3_recs: list, got: dict, fields: list, expected: dict) -> tuple:
    """(template results [(pid, iid, ok)], per-document rows). A document with no answer fails."""
    results, rows = [], []
    for r in g3_recs:
        iid = f"g3h|{r['pid']}"
        if iid not in got:
            ok, diffs = False, ["no answer"]
        else:
            ok, diffs = g3h.compare(expected[iid], got[iid], fields)
        results.append((r["pid"], iid, ok))
        rows.append({"pid": r["pid"], "register": r["obj"].register, "held_out": r["held_out"], "ok": ok,
                     "diffs": diffs, "extracted": got.get(iid), "expected": expected[iid]})
    return results, rows


# ------------------------------------------------------------------------------------------------ 5. packs

def split_packs(packs: list) -> list:
    """Seeded split: the N_HELD_PACKS packs whose key hashes lowest (with the version) are held out (S5 only)."""
    order = sorted(packs, key=lambda p: _sha(f"T36|pack-split|{VERSION}|{p.key}"))
    held = {p.key for p in order[:N_HELD_PACKS]}
    return [P.Pack(p.key, p.project, tuple(p.packages), tuple(p.people), held_out=(p.key in held)) for p in packs]


def pack_values(p) -> set:
    return {p.project, *p.packages, *p.people}


# ------------------------------------------------------------------------------------------------ 6. checks

def slot_problems(s) -> list:
    """H32: each Mode T skin holds {PROJECT}, {PERSON}, {PKG} exactly once; an attack line holds {PERSON} once and
    {PKG} at most once. A Mode F document holds no placeholder at all."""
    occ = Counter(p.name for p in K.placeholders(s.text))
    if s.kind == "attack":
        out = [] if occ.get("PERSON", 0) == 1 else [f"PERSON x{occ.get('PERSON', 0)}"]
        if occ.get("PKG", 0) > 1:
            out.append(f"PKG x{occ['PKG']}")
        allowed = {"PERSON", "PKG"}
    else:
        out = [f"{n} x{occ.get(n, 0)}" for n in ("PROJECT", "PERSON", "PKG") if occ.get(n, 0) != 1]
        allowed = {"PROJECT", "PERSON", "PKG"}
    extra = sorted(set(occ) - allowed)
    if extra:
        out.append(f"unknown slots {extra}")
    return out


def _pool_of(s) -> str:
    if s.kind == "attack":
        return "attack"
    if s.author_mode == "F":
        return "freeform_heldout" if s.held_out else "freeform"
    return "skin_heldout" if s.held_out else "skin"


def rekey(s):
    """The same piece with a unique id: T36-<pool>-<sha256(text)[:16]> (texts are unique across every pool)."""
    return dataclasses.replace(s, skin_id=f"T36-{_pool_of(s)}-{_sha(s.text)[:16]}")


def rekey_map(objs: list) -> list:
    return [(s.skin_id, rekey(s).skin_id) for s in sorted(objs, key=lambda s: s.skin_id)]


def skin_json(s) -> dict:
    return {"skin_id": s.skin_id, "family": s.family, "text": s.text, "slots": dict(s.slots), "kind": s.kind,
            "register": s.register, "escape": s.escape, "counts": [list(c) for c in s.counts],
            "author_mode": s.author_mode, "qform": s.qform, "brief": dict(s.brief), "held_out": s.held_out,
            "haiku_task_id": s.haiku_task_id, "haiku_prompt_sha": s.haiku_prompt_sha,
            "lexicon_ids": list(s.lexicon_ids)}


def skin_from_json(d: dict):
    return K.make_skin(d["skin_id"], d["family"], d["text"], d["slots"], kind=d["kind"], register=d["register"],
                       escape=d["escape"], counts={c[0]: (c[1], c[2]) for c in d["counts"]},
                       author_mode=d["author_mode"], qform=d["qform"], brief=d["brief"] or {},
                       held_out=d["held_out"], haiku_task_id=d["haiku_task_id"],
                       haiku_prompt_sha=d["haiku_prompt_sha"], lexicon_ids=tuple(d["lexicon_ids"]))


def _j(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n"


# ------------------------------------------------------------------------------------------------ run

def run(write: bool) -> dict:
    st = rebuild()
    reg, fids, recs, fields = st["reg"], st["fids"], st["recs"], st["fields"]
    tasks = st["index"]["tasks"]
    n_outputs = st["index"]["outputs_expected"]

    # 2-3. answers and G-LEX
    answer_problems, glex_reads, got_by_label, returned = [], {}, {}, 0
    for label, kind, b, _p in st["batches"]:
        got, probs, missing = read_answers(b)
        returned += len(b.chunks) - len(missing)
        if missing:
            answer_problems.append({"batch": label, "missing_tasks": missing})
        answer_problems += [{"batch": label, "problem": x} for x in probs]
        got_by_label[label] = got
        if kind == "extract_lex":
            glex_reads[label] = {"answered": len(got), "items": len(b.key), **record_glex(reg, b, got)}
    if returned != EXPECTED_TASKS:
        raise SystemExit(f"{returned} of {EXPECTED_TASKS} extraction answers returned")

    admitted_fids = {fid for fid in reg.forms if reg.status(fid) == "admitted"}
    glex_status = dict(Counter(reg.status(f) for f in reg.forms))
    not_admitted = sorted(set(reg.forms) - admitted_fids)

    # wordings: each surviving wording record maps to its form; admitted or quarantined
    wording_pool, wording_quar = [], []
    for r in sorted(recs.get("wording", []), key=lambda r: r["pid"]):
        fid = fids.get(r["pid"])
        o = r["obj"]
        if fid is None or fid not in admitted_fids:
            wording_quar.append({"pid": r["pid"], "qform": o["qform"], "text": o["text"],
                                 "status": reg.status(fid) if fid else "no_form", "problems": (
                                     reg.forms[fid].unit_problems if fid else [])})
            continue
        f = reg.forms[fid]
        wording_pool.append({"form_id": fid, "pid": r["pid"], "qform": o["qform"], "sem_id": f.sem_id,
                             "text": f.text, "slots": dict(f.slots), "haiku_task_id": o["haiku_task_id"],
                             "haiku_prompt_sha": o["haiku_prompt_sha"], "extractions": [list(e) for e in f.extractions]})

    # 4. G3-H on every Mode F document
    g3_got = got_by_label["g3h-r1"]
    exp_disk = {r["g3h_id"]: r for r in map(json.loads, (EXTRACT / "pool" / "g3h_expected.jsonl")
                                             .read_text(encoding="utf-8").splitlines())}
    expected = {}
    for r in st["g3_recs"]:
        facts = dict(r["obj"].brief)
        iid = f"g3h|{r['pid']}"
        expected[iid] = {"project": facts["PROJECT"], "person": facts["PERSON"]}
        if exp_disk[iid]["expected"] != expected[iid]:
            raise SystemExit(f"expected values drifted for {iid}")
    g3_results, g3_rows = g3h_compare(st["g3_recs"], g3_got, fields, expected)
    rep = g3h.template_report(g3_results)
    passed_pids = {row["pid"] for row in g3_rows if row["ok"] and row["pid"] not in set(rep["quarantined"])}
    by_register_g3 = {}
    for row in g3_rows:
        d = by_register_g3.setdefault(row["register"], {"n": 0, "ok": 0})
        d["n"] += 1
        d["ok"] += row["ok"]
    # alternative reading (template = register): a register passes only when all its documents pass
    alt_pass_docs = sum(d["ok"] for d in by_register_g3.values() if d["ok"] == d["n"])

    docs = [r["obj"] for r in st["g3_recs"] if r["pid"] in passed_pids]
    doc_quar = [{"pid": row["pid"], "register": row["register"], "held_out": row["held_out"],
                 "diffs": row["diffs"]} for row in g3_rows if row["pid"] not in passed_pids]

    # 5. packs
    plugin = P.T36Plugin()
    packs_all = [r["obj"] for r in sorted(recs.get("pack", []), key=lambda r: r["pid"])]
    pack_probs = {p.key: P.check_pack(p, plugin.LABEL_WORDS) for p in packs_all}
    packs = split_packs([p for p in packs_all if not pack_probs[p.key]])
    pack_quar = [{"key": p.key, "project": p.project, "problems": pack_probs[p.key]}
                 for p in packs_all if pack_probs[p.key]]
    train_vals = set().union(*(pack_values(p) for p in packs if not p.held_out)) if packs else set()
    held_vals = set().union(*(pack_values(p) for p in packs if p.held_out)) if packs else set()
    standin_held = set().union(*(pack_values(p) for p in P.STANDIN_PACKS if p.held_out))
    standin_train = set().union(*(pack_values(p) for p in P.STANDIN_PACKS if not p.held_out))
    leaks = {
        "held_pack_values_also_in_training_packs": sorted(held_vals & train_vals),
        "authored_training_values_equal_standin_held_values": sorted(train_vals & standin_held),
        "authored_held_values_equal_standin_training_values": sorted(held_vals & standin_train),
    }

    # 6. checks: H32 on Mode T skins and attack lines; ids; the Mode F cap
    authored_skins = [r["obj"] for r in recs.get("skin", [])] + [r["obj"] for r in recs.get("skin_heldout", [])]
    attacks_all = [r["obj"] for r in recs.get("attack", [])]
    authored_all = authored_skins + attacks_all + docs
    authored_ids = Counter(s.skin_id for s in authored_all)
    skin_fail = [s for s in authored_skins if slot_problems(s)]
    attack_fail = [s for s in attacks_all if slot_problems(s)]
    skin_bad = [{"text_sha": _sha(s.text)[:16], "authored_id": s.skin_id, "problems": slot_problems(s)}
                for s in skin_fail]
    attack_bad = [{"text_sha": _sha(s.text)[:16], "authored_id": s.skin_id, "problems": slot_problems(s)}
                  for s in attack_fail]
    bad_texts = {s.text for s in skin_fail + attack_fail}
    skins = [rekey(s) for s in authored_skins if s.text not in bad_texts and s.kind == "skin"]
    attacks = [rekey(s) for s in attacks_all if s.text not in bad_texts and s.kind == "attack"]
    t_train = sum(1 for s in skins if not s.held_out)
    t_held = sum(1 for s in skins if s.held_out)
    cap_train, cap_held = t_train // 3, t_held // 3
    docs_re = [rekey(d) for d in docs]
    docs_train = sorted((d for d in docs_re if not d.held_out), key=lambda d: d.skin_id)
    docs_held = sorted((d for d in docs_re if d.held_out), key=lambda d: d.skin_id)
    cap_drop = {d.skin_id for d in docs_train[cap_train:]} | {d.skin_id for d in docs_held[cap_held:]}
    docs = [d for d in docs_re if d.skin_id not in cap_drop]
    cap_quar = [{"skin_id": x, "reason": "Mode F cap"} for x in sorted(cap_drop)]
    final_ids = [s.skin_id for s in skins + attacks + docs]
    if len(set(final_ids)) != len(final_ids):
        raise SystemExit("skin ids still collide after re-keying")
    id_fix = {"records": len(authored_all), "authored_unique_ids": len(authored_ids),
              "authored_ids_shared_by_more_than_one_record": sum(1 for v in authored_ids.values() if v > 1),
              "rule": "re-keyed to T36-<pool>-<sha256(text)[:16]>: authoring.load_pools builds skin ids from the "
                      "item index and the batch tail, so items of the same index in one batch share an id",
              "rekey_map": [[old, new] for old, new in rekey_map(authored_all)]}

    # counts and shortfalls against the G0 targets
    counts = {
        "packs_train": sum(1 for p in packs if not p.held_out),
        "packs_held": sum(1 for p in packs if p.held_out),
        "skin": dict(Counter(s.register for s in skins if not s.held_out)),
        "skin_heldout": dict(Counter(s.register for s in skins if s.held_out)),
        "attack": len(attacks),
        "freeform": dict(Counter(d.register for d in docs if not d.held_out)),
        "freeform_heldout": dict(Counter(d.register for d in docs if d.held_out)),
        "wording": dict(Counter(w["qform"] for w in wording_pool)),
    }
    shortfalls = []

    def need(name, have, want):
        if have < want:
            shortfalls.append({"item": name, "admitted": have, "target": want, "shortfall": want - have})

    need("packs_train", counts["packs_train"], TARGETS["packs_train"])
    need("packs_held", counts["packs_held"], TARGETS["packs_held"])
    for r, want in TARGETS["skin"].items():
        need(f"skin/{r}", counts["skin"].get(r, 0), want)
    for r, want in TARGETS["skin_heldout"].items():
        need(f"skin_heldout/{r}", counts["skin_heldout"].get(r, 0), want)
    need("attack", counts["attack"], TARGETS["attack"])
    for r, want in TARGETS["freeform"].items():
        need(f"freeform/{r}", counts["freeform"].get(r, 0), want)
    for r, want in TARGETS["freeform_heldout"].items():
        need(f"freeform_heldout/{r}", counts["freeform_heldout"].get(r, 0), want)
    for q, want in TARGETS["wording"].items():
        need(f"wording/{q}", counts["wording"].get(q, 0), want)

    # 7. the pools
    lex_full = reg.to_json()
    lex_pool = dict(lex_full)
    lex_pool["forms"] = [f for f in lex_full["forms"] if f["form_id"] in admitted_fids]
    lex_pool["note"] = "admitted forms only; every sem is declared (question meanings and decoys)"
    skins_pool = sorted(skins, key=lambda s: s.skin_id)
    files = {
        "skins.json": _j([skin_json(s) for s in skins_pool]),
        "attacks.json": _j([skin_json(s) for s in sorted(attacks, key=lambda s: s.skin_id)]),
        "documents.json": _j([skin_json(d) for d in sorted(docs, key=lambda d: d.skin_id)]),
        "wordings.json": _j(sorted(wording_pool, key=lambda w: w["form_id"])),
        "lexicon.json": _j(lex_pool),
        "packs.json": _j([{"key": p.key, "project": p.project, "packages": list(p.packages),
                           "people": list(p.people), "held_out": p.held_out}
                          for p in sorted(packs, key=lambda p: p.key)]),
        "quarantine.json": _j({
            "g3h_failed_documents": doc_quar, "g3h_cap_dropped": cap_quar,
            "wordings_not_admitted": wording_quar, "forms_not_admitted": not_admitted,
            "skin_slot_failures": skin_bad, "attack_slot_failures": attack_bad, "pack_failures": pack_quar,
            "unanswered_or_invalid_extraction": answer_problems}),
    }
    sha = {k: _sha(v) for k, v in files.items()}
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "freeze", "tier": "transfer_dev (never trained; every row dev-only)",
        "g0_sha256": P.POOL_G0_SHA256, "g0_ambiguity_pass": P.T36Plugin.G0_AMBIGUITY_PASS["task_id"],
        "status": "frozen before G13-seed: no rows generated; G13-seed and the transcript audit are pending",
        "sha256": sha,
        "counts": counts,
        "targets": TARGETS,
        "shortfalls": shortfalls,
        "extraction": {"tasks_expected": EXPECTED_TASKS, "tasks_returned": returned,
                       "outputs_expected": n_outputs, "answer_problems": answer_problems,
                       "reads": glex_reads, "tasks": [{k: t[k] for k in ("task_id", "kind", "read", "n_items")}
                                                      for t in tasks]},
        "glex": {"gate": "G-LEX", "bar": "2/2 (no precedence or window kind in T36)", "forms": len(reg.forms),
                 "status_counts": glex_status, "admitted": len(admitted_fids),
                 "admitted_by_qform": dict(Counter(f.sem_id.rsplit(".", 1)[-1] for f in reg.forms.values()
                                                   if f.form_id in admitted_fids))},
        "g3h": {"gate": "G3-H", "bar": G3H_BAR, "template": "document (one Mode F document = one skin)",
                "documents": len(g3_rows), "pass": sum(1 for r in g3_rows if r["ok"]),
                "fail": sum(1 for r in g3_rows if not r["ok"]), "frozen_documents": len(docs),
                "template_quarantined": rep["quarantined"], "by_register": by_register_g3,
                "failing_fields": dict(Counter(d.split(":", 1)[0] for row in g3_rows for d in row["diffs"])),
                "documents_where_person_extracted_NONE": sum(
                    1 for row in g3_rows if isinstance(row["extracted"], dict) and row["extracted"].get("person") == "NONE"),
                "alternative_reading": {"template": "register (all documents of a register must pass)",
                                        "documents_that_would_pass": alt_pass_docs}},
        "packs": {"rule": "seeded split: the N lowest sha256(T36|pack-split|v1|key) are held out",
                  "n_held_out": N_HELD_PACKS, "held_out_keys": sorted(p.key for p in packs if p.held_out),
                  "leak_checks": leaks},
        "caps": {"mode_f_cap": "1 document per 3 Mode T skins of the same held-out status",
                 "train": {"mode_t_skins": t_train, "cap": cap_train, "kept": len(docs_train[:cap_train])},
                 "held_out": {"mode_t_skins": t_held, "cap": cap_held, "kept": len(docs_held[:cap_held])}},
        "skin_ids": id_fix,
        "lint_and_drops": {"authoring_drops_by_pool": dict(Counter(p for p, _i, _r in st["col"]["authoring_drops"])),
                           "lint_drops_by_pool": dict(Counter(d["pool"] for d in st["lint_drops"])),
                           "dedup_drops": len(st["dup_drops"]), "form_drops": len(st["form_drops"])},
        "pending_gates": [
            "G13-seed on every pool before any row (C2_DATA_SPEC 6.3): not run in this step",
            "file-access audit of the 7 extraction transcripts (c2_kit/audit.py): not run in this step; a failed audit discards that agent's answers",
            "G3-H: the failing documents fail on the person field only (see g3h.failing_fields); the extraction field "
            "'the person who maintains the project' does not match what the documents say; a ruling is needed before "
            "Mode F can supply rows",
        ],
    }
    files["MANIFEST.json"] = _j(manifest)

    out = {"counts": counts, "shortfalls": shortfalls, "glex": manifest["glex"], "g3h": {k: v for k, v in manifest["g3h"].items() if k != "by_register"},
           "packs": {"train": counts["packs_train"], "held": counts["packs_held"]},
           "reads": glex_reads, "returned": returned, "written": False, "files": sorted(files)}
    if write:
        paths.write_files(POOLS, files)
        out["written"] = True
        out["verify"] = verify_pools()
    return out


# ------------------------------------------------------------------------------------------------ load and verify

def load_pools(root: Path = POOLS) -> tuple:
    """(KitCtx with the admitted skins, attack lines and documents; the admitted lexicon; the packs)."""
    root = Path(root)
    sk = [skin_from_json(d) for d in json.loads((root / "skins.json").read_text(encoding="utf-8"))]
    at = [skin_from_json(d) for d in json.loads((root / "attacks.json").read_text(encoding="utf-8"))]
    dc = [skin_from_json(d) for d in json.loads((root / "documents.json").read_text(encoding="utf-8"))]
    lex = LX.LexiconRegistry.from_json(json.loads((root / "lexicon.json").read_text(encoding="utf-8")))
    packs = [P.Pack(p["key"], p["project"], tuple(p["packages"]), tuple(p["people"]), p["held_out"])
             for p in json.loads((root / "packs.json").read_text(encoding="utf-8"))]
    ctx = KitCtx(skins={s.skin_id: s for s in sk + at + dc}, lexicon=lex)
    return ctx, packs


def verify_pools(root: Path = POOLS) -> dict:
    """Read the written pools back: sha256 of each file against MANIFEST.json, and the reloaded counts."""
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    bad = [k for k, v in man["sha256"].items() if _sha((root / k).read_text(encoding="utf-8")) != v]
    n_records = sum(len(json.loads((root / k).read_text(encoding="utf-8")))
                    for k in ("skins.json", "attacks.json", "documents.json"))
    ctx, packs = load_pools(root)
    lex_ok = all(ctx.lexicon.status(f) == "admitted" for f in ctx.lexicon.forms)
    ids_ok = len(ctx.skins) == n_records
    return {"sha_mismatches": bad, "records": n_records, "skin_ids_unique": ids_ok,
            "skins_reloaded": len(ctx.skins), "packs_reloaded": len(packs),
            "lexicon_forms": len(ctx.lexicon.forms), "lexicon_all_admitted": lex_ok,
            "ok": not bad and lex_ok and ids_ok}


def main(argv: list) -> int:
    res = run("--write" in argv)
    print(json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
