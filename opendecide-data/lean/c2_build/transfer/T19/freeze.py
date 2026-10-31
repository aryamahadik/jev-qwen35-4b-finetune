"""transfer/T19/freeze.py: record the T19 extraction answers, admit or quarantine, and freeze the pools.

Runs after the extraction round (haiku/extract/answers/: 7 tasks = 2 G-LEX question reads of 105 forms (3 tasks each)
and 1 G3-H read of 19 Mode F documents). Every write goes through paths.write_files, which refuses before A38 and on
never-open paths. Nothing here generates rows: the pools are frozen first and the rows come later.

Steps (C2_DATA_SPEC 6.3; G0_SPEC.md sections 6 and 7; PREREG A37 (b), A38):
  1. rebuild   extract_build.build_all() (deterministic); every batch file, TASKS.json and lint_log.json on disk must
               equal the regenerated copy (drift refuses)
  2. load      the returned answers through chunker.load_answers (each qid answered once, inside its own task)
  3. G-LEX     record every reading with lexicon.record_extraction; the extractor is the read (haiku-glex-question-r1
               or -r2). A form is ADMITTED at 2/2 distinct agreeing readings (T19 has no precedence or window kind)
  4. G3-H      g3h.compare on every Mode F document; template = document (the kit convention used by T36):
               g3h.template_report quarantines a document below 98% and drops mismatched rows
  5. checks    G0 H15: each Mode T skin holds {SITE} and {AUDITOR} exactly once; an attack line holds {AUDITOR} once;
               a wording holds {SITE} once; a Mode F document holds no placeholder. Pack leak report (held vs training)
  6. counts    admitted counts against the G0-lite targets (section 6). Targets are fixed here and never lowered
  7. freeze    pools/: skins.json, attacks.json, documents.json, wordings.json, lexicon.json, packs.json,
               quarantine.json, MANIFEST.json (sha256s, counts, targets, shortfalls, pending gates)

  cd lean && ../.venv/bin/python c2_build/transfer/T19/freeze.py            (dry run: counts and checks, writes nothing)
  cd lean && ../.venv/bin/python c2_build/transfer/T19/freeze.py --write    (writes pools/ and verifies them)
"""
from __future__ import annotations

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
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from transfer.T19 import extract_build as EX  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
VERSION = "v1"
POOLS = HERE / "pools"
EXTRACT = EX.EXTRACT
EXPECTED_TASKS = 7
EXPECTED_OUTPUTS = 229
G3H_BAR = g3h.PASS_RATE                            # 0.98, never loosened
TRAIN_REGISTERS = tuple(HA.TRAIN_REGISTERS)
HELD_REGISTERS = tuple(HA.HELD_REGISTERS)

# G0-lite section 6 (T19 transfer dev). Do not lower them: a shortfall is reported, never absorbed.
TARGETS = {
    "packs_train": 32,                             # 40 packs, of which 8 are held out (S5 only)
    "packs_held": 8,
    "skin": {r: 12 for r in TRAIN_REGISTERS},      # 12 Mode T skins per training register
    "skin_heldout": {r: 16 for r in HELD_REGISTERS},
    "attack": 30,
    "freeform": {r: 4 for r in TRAIN_REGISTERS},   # 4 Mode F narratives per training register (S4)
    "freeform_heldout": {},                        # G0-lite: no held-out Mode F register
    "wording": {"ch_verdict": 26, "yn_compliant": 30, "ch_gap": 16, "yn_out_of": 14, "yn_not_compliant": 14,
                "yn_fails": 14},
}

READ_LABELS = {1: "glex-question-r1", 2: "glex-question-r2"}


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _norm(s) -> str:
    return " ".join(str(s).casefold().split())


def _j(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n"


# ------------------------------------------------------------------------------------------------ 1. rebuild

def rebuild() -> dict:
    """Regenerate every batch from the lint and check each file on disk against the regenerated copy."""
    res = EX.build_all()
    drift = [rel for rel, text in res["files"].items()
             if not (EXTRACT / rel).exists() or (EXTRACT / rel).read_text(encoding="utf-8") != text]
    tasks_disk = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    if tasks_disk.get("tasks") != res["tasks"]:
        drift.append("TASKS.json")
    if json.loads((EXTRACT / "lint_log.json").read_text(encoding="utf-8")) != EX.lint_log(res):
        drift.append("lint_log.json")
    if drift:
        raise SystemExit(f"extraction files drifted from the regenerated batches: {drift[:8]}")
    return res


# ------------------------------------------------------------------------------------------------ 2. load

def read_answers(batch) -> tuple:
    """(internal id -> answer, problems, missing task ids) for one batch, from its answer files on disk."""
    raw, missing, probs = {}, [], []
    for c in batch.chunks:
        f = EXTRACT / batch.answer_path(c["task_id"])
        if not f.exists():
            missing.append(c["task_id"])
            continue
        try:
            raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            missing.append(c["task_id"])
            probs.append(f"{c['task_id']}: answer is not JSON ({e})")
    got, p2 = chunker.load_answers(batch, raw)
    return got, probs + p2, missing


# ------------------------------------------------------------------------------------------------ 3. G-LEX

def record_glex(reg: LexiconRegistry, got: dict, extractor: str) -> dict:
    """Record one G-LEX reading per answered form. A meaning that is not on the kind's closed list records None,
    which rejects the form (G-LEX: any disagreement rejects for good). Haiku never sets a label: a meaning maps to a
    sem id only to be compared with the form's own sem."""
    stats = Counter()
    for fid in sorted(got):
        f = reg.forms[fid]
        a = got[fid]
        meaning = a.get("meaning") if isinstance(a, dict) else None
        sems = [s for s in reg.sems.values() if s.kind == f.kind]
        exact = [s.sem_id for s in sems if isinstance(meaning, str) and s.meaning == meaning]
        loose = [s.sem_id for s in sems if isinstance(meaning, str) and _norm(s.meaning) == _norm(meaning)]
        if exact:
            sem, how = exact[0], "exact"
        elif len(loose) == 1:
            sem, how = loose[0], "case_or_spacing"
        else:
            sem, how = None, "not_listed"
        reg.record_extraction(fid, extractor, sem)
        stats[how] += 1
        stats["agrees" if sem == f.sem_id else "disagrees_or_none"] += 1
    return dict(stats)


# ------------------------------------------------------------------------------------------------ 5. checks

def slot_problems(sk) -> list:
    """G0 H15: a Mode T skin holds {SITE} and {AUDITOR} exactly once; an attack line holds {AUDITOR} once; a Mode F
    document holds no placeholder at all."""
    occ = Counter(p.name for p in K.placeholders(sk.text))
    if sk.kind == "attack":
        want = {"AUDITOR": 1}
    elif sk.author_mode == "F":
        want = {}
    else:
        want = {"SITE": 1, "AUDITOR": 1}
    out = [f"{n} x{occ.get(n, 0)}" for n, k in want.items() if occ.get(n, 0) != k]
    extra = sorted(set(occ) - set(want))
    if extra:
        out.append(f"unknown slots {extra}")
    return out


def wording_problems(text: str) -> list:
    occ = Counter(p.name for p in K.placeholders(text))
    out = [] if occ.get("SITE", 0) == 1 and set(occ) == {"SITE"} else [f"SITE/other slots {dict(occ)}"]
    return out


def pack_vals(p: dict, kinds=("sites", "auditors")) -> set:
    return {_norm(v) for k in kinds for v in p[k]}


# ------------------------------------------------------------------------------------------------ pool JSON

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


# ------------------------------------------------------------------------------------------------ run

def run(write: bool) -> dict:
    res = rebuild()
    reg, lint = res["reg"], res["lint"]
    fields = EX.g3h_fields()

    # 2-3. answers and G-LEX (both reads; the G3-H answers are read in step 4)
    answer_problems, glex_reads, returned, got_by_label = [], {}, 0, {}
    for g in res["glex"]:
        label = f"glex-question-r{g['read']}"
        got, probs, missing = read_answers(g["batch"])
        returned += len(g["batch"].chunks) - len(missing)
        if missing:
            answer_problems.append({"batch": label, "missing_tasks": missing})
        answer_problems += [{"batch": label, "problem": x} for x in probs]
        got_by_label[label] = got
        glex_reads[label] = {"extractor_id": g["extractor_id"], "items": len(g["batch"].key), "answered": len(got),
                             **record_glex(reg, got, g["extractor_id"])}
    g3b = res["g3"]
    got_g3, probs, missing = read_answers(g3b)
    returned += len(g3b.chunks) - len(missing)
    if missing:
        answer_problems.append({"batch": "g3h-freeform-r1", "missing_tasks": missing})
    answer_problems += [{"batch": "g3h-freeform-r1", "problem": x} for x in probs]
    got_by_label["g3h-freeform-r1"] = got_g3
    if returned != EXPECTED_TASKS:
        raise SystemExit(f"{returned} of {EXPECTED_TASKS} extraction answers returned")
    answered_total = sum(len(v) for v in got_by_label.values())
    if answered_total != EXPECTED_OUTPUTS:
        answer_problems.append({"batch": "all", "problem": f"{answered_total} answers of {EXPECTED_OUTPUTS} expected"})

    # G-LEX outcome: 2/2 distinct agreeing readings admit a form; anything else is rejected or pending
    admitted = {fid for fid in reg.forms if reg.status(fid) == "admitted"}
    status_counts = dict(Counter(reg.status(f) for f in reg.forms))
    lex_kinds = {f.kind for f in reg.forms.values()}
    if lex_kinds - {"question"}:
        raise SystemExit(f"unexpected lexicon kinds {sorted(lex_kinds)}: T19 has only question forms (2/2)")
    forms_not_admitted = [{"form_id": fid, "qform": reg.forms[fid].sem_id.rsplit(".", 1)[-1],
                           "text": reg.forms[fid].text, "status": reg.status(fid),
                           "extractions": [list(e) for e in reg.forms[fid].extractions],
                           "unit_problems": reg.forms[fid].unit_problems}
                          for fid in sorted(set(reg.forms) - admitted)]

    # wordings: each surviving wording record maps to its form; admitted kept, the rest quarantined
    text_fid = {f.text: fid for fid, f in reg.forms.items()}
    wording_pool, wording_quar = [], []
    for q, text, tid, psha in sorted(lint["wordings"], key=lambda w: (w[0], w[2], w[1])):
        fid = text_fid.get(text)
        if fid is None:
            wording_quar.append({"qform": q, "text": text, "haiku_task_id": tid,
                                 "reason": "not in the registry (dropped at admission)"})
            continue
        f = reg.forms[fid]
        if fid not in admitted:
            wording_quar.append({"qform": q, "text": text, "haiku_task_id": tid, "form_id": fid,
                                 "status": reg.status(fid), "extractions": [list(e) for e in f.extractions],
                                 "unit_problems": f.unit_problems})
            continue
        probs = wording_problems(text)
        if probs or f.sem_id != question_sem(FAMILY, q):
            wording_quar.append({"qform": q, "text": text, "haiku_task_id": tid, "form_id": fid,
                                 "reason": probs or ["sem mismatch"]})
            continue
        wording_pool.append({"form_id": fid, "qform": q, "sem_id": f.sem_id, "text": f.text, "slots": dict(f.slots),
                             "haiku_task_id": tid, "haiku_prompt_sha": psha,
                             "extractions": [list(e) for e in f.extractions]})

    # 4. G3-H on every Mode F document (template = document)
    exp = res["g3h_expected"]
    g3_results, g3_rows = [], []
    for iid in sorted(exp):
        sid = iid.split("|", 1)[1]
        doc = lint["free"][sid]
        if iid not in got_g3:
            ok, diffs, ext = False, ["no answer"], None
        else:
            ok, diffs = g3h.compare(exp[iid], got_g3[iid], fields)
            ext = got_g3[iid]
        g3_results.append((sid, iid, ok))
        g3_rows.append({"skin_id": sid, "register": doc.register, "held_out": doc.held_out, "ok": ok, "diffs": diffs,
                        "extracted": ext, "expected": exp[iid]})
    rep = g3h.template_report(g3_results)
    quarantined = set(rep["quarantined"])
    by_register_g3: dict = {}
    for row in g3_rows:
        d = by_register_g3.setdefault(row["register"], {"n": 0, "ok": 0})
        d["n"] += 1
        d["ok"] += row["ok"]
    docs = [lint["free"][r["skin_id"]] for r in g3_rows if r["ok"] and r["skin_id"] not in quarantined]
    doc_quar = [{"skin_id": r["skin_id"], "register": r["register"], "held_out": r["held_out"], "diffs": r["diffs"],
                 "extracted": r["extracted"], "expected": r["expected"]} for r in g3_rows
                if r["skin_id"] not in {d.skin_id for d in docs}]

    # packs (already G-SL linted and validated in the loaders)
    packs = sorted(lint["packs"], key=lambda p: p["pack_id"])
    train_packs = [p for p in packs if not p["held_out"]]
    held_packs = [p for p in packs if p["held_out"]]
    held_names = set().union(*(pack_vals(p) for p in held_packs)) if held_packs else set()
    train_names = set().union(*(pack_vals(p) for p in train_packs)) if train_packs else set()
    leak = {"held_site_or_auditor_names_also_in_training_packs": sorted(held_names & train_names)}

    # 5. checks on skins and attack lines (H15 slots)
    skins_all = sorted(lint["skins"].values(), key=lambda s: s.skin_id)
    attacks_all = sorted(lint["attacks"].values(), key=lambda s: s.skin_id)
    skins, skin_quar = [], []
    for s in skins_all:
        probs = slot_problems(s)
        (skin_quar.append({"skin_id": s.skin_id, "problems": probs}) if probs else skins.append(s))
    attacks, attack_quar = [], []
    for s in attacks_all:
        probs = slot_problems(s)
        (attack_quar.append({"skin_id": s.skin_id, "problems": probs}) if probs else attacks.append(s))
    docs = sorted(docs, key=lambda d: d.skin_id)
    doc_bad = [d.skin_id for d in docs if K.placeholders(d.text)]
    if doc_bad:
        raise SystemExit(f"Mode F documents hold placeholders: {doc_bad[:5]}")

    final_ids = [s.skin_id for s in skins + attacks + docs]
    dup_ids = sorted(k for k, v in Counter(final_ids).items() if v > 1)
    if dup_ids:
        raise SystemExit(f"skin ids collide: {dup_ids[:5]}")

    # counts and shortfalls against the G0-lite targets
    counts = {
        "packs_train": len(train_packs),
        "packs_held": len(held_packs),
        "skin": dict(sorted(Counter(s.register for s in skins if not s.held_out).items())),
        "skin_heldout": dict(sorted(Counter(s.register for s in skins if s.held_out).items())),
        "attack": len(attacks),
        "freeform": dict(sorted(Counter(d.register for d in docs if not d.held_out).items())),
        "freeform_heldout": dict(sorted(Counter(d.register for d in docs if d.held_out).items())),
        "wording": dict(sorted(Counter(w["qform"] for w in wording_pool).items())),
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
    target_totals = {
        "skin_train": sum(TARGETS["skin"].values()), "skin_heldout": sum(TARGETS["skin_heldout"].values()),
        "freeform_train": sum(TARGETS["freeform"].values()), "wording": sum(TARGETS["wording"].values()),
    }

    # 7. the pools
    lex_full = reg.to_json()
    lex_pool = dict(lex_full)
    lex_pool["forms"] = [f for f in lex_full["forms"] if f["form_id"] in admitted]
    lex_pool["note"] = "admitted forms only; every sem is declared (question meanings)"
    lint_drops = lint["drops"]
    quarantine = {
        "lint_drops": lint_drops,
        "cross_pool_dups": lint["cross_pool_dups"],
        "structural_problems": lint["structural"],
        "question_admit_drops": res["admit_drops"],
        "forms_not_admitted": forms_not_admitted,
        "wordings_not_admitted": wording_quar,
        "g3h_failed_documents": doc_quar,
        "g3h_template_quarantined": rep["quarantined"],
        "skin_slot_failures": skin_quar,
        "attack_slot_failures": attack_quar,
        "answer_problems": answer_problems,
    }
    files = {
        "skins.json": _j([skin_json(s) for s in skins]),
        "attacks.json": _j([skin_json(s) for s in attacks]),
        "documents.json": _j([skin_json(d) for d in docs]),
        "wordings.json": _j(sorted(wording_pool, key=lambda w: w["form_id"])),
        "lexicon.json": _j(lex_pool),
        "packs.json": _j([{"pack_id": p["pack_id"], "held_out": p["held_out"], "sites": list(p["sites"]),
                           "auditors": list(p["auditors"]), "controls": list(p["controls"])} for p in packs]),
        "quarantine.json": _j(quarantine),
    }
    sha = {k: _sha(v) for k, v in files.items()}
    only_on = {k: sum(1 for d in lint_drops[k] if d.get("only_on")) for k in ("skins", "freeform", "attacks")
               if k in lint_drops}
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "freeze", "tier": "transfer_dev (never trained; every row dev-only)",
        "g0_sha256": P.T19Plugin.G0_SHA256_AUTHORED, "g0_ambiguity_pass": P.T19Plugin.G0_HAIKU_TASK,
        "status": "frozen: no rows generated; G13-seed and the file-access audit are pending (see pending_gates)",
        "sha256": sha,
        "counts": counts,
        "targets": {**TARGETS, "_totals": target_totals},
        "shortfalls": shortfalls,
        "extraction": {"tasks_expected": EXPECTED_TASKS, "tasks_returned": returned,
                       "outputs_expected": EXPECTED_OUTPUTS, "outputs_answered": answered_total,
                       "answer_problems": answer_problems,
                       "reads": glex_reads, "g3h_answered": len(got_g3)},
        "glex": {"gate": "G-LEX", "bar": "2/2 distinct agreeing readings (T19 has no precedence or window kind)",
                 "forms": len(reg.forms), "status_counts": status_counts, "admitted": len(admitted),
                 "admitted_by_qform": dict(Counter(reg.forms[f].sem_id.rsplit(".", 1)[-1] for f in admitted)),
                 "not_admitted": len(forms_not_admitted)},
        "g3h": {"gate": "G3-H", "bar": G3H_BAR, "template": "document (one Mode F document = one skin)",
                "documents": len(g3_rows), "pass": sum(1 for r in g3_rows if r["ok"]),
                "fail": sum(1 for r in g3_rows if not r["ok"]), "frozen_documents": len(docs),
                "template_quarantined": rep["quarantined"], "by_register": by_register_g3,
                "failing_fields": dict(Counter(x.split(":", 1)[0] for r in g3_rows for x in r["diffs"]))},
        "packs": {"rule": "held-out flag from the S5 plan (haiku/author/plan); no split is made here",
                  "held_out_keys": [p["pack_id"] for p in held_packs], "leak_checks": leak},
        "skin_ids": {"records_admitted_by_loader": len(lint["skins"]) + len(lint["attacks"]) + len(lint["free"]),
                     "final_ids": len(final_ids), "unique": len(set(final_ids)) == len(final_ids)},
        "lint_and_drops": {
            "by_pool": {k: len(v) for k, v in lint_drops.items()},
            "only_for_bare_on": only_on,
            "note": "'only_for_bare_on' pieces are dropped by the T19 profile-word check (the bare word 'on'); this "
                    "freeze keeps that rule as written (never loosened) and reports the count",
            "cross_pool_dups": len(lint["cross_pool_dups"]),
            "question_admit_drops": len(res["admit_drops"]),
        },
        "pending_gates": [
            "G13-seed decontamination on every pool before any row (C2_DATA_SPEC 6.3): not run in this step",
            "file-access audit of the 7 extraction transcripts (c2_kit/audit.py): not run in this step (no transcripts "
            "are read here); a failed audit discards that agent's answers",
            "shortfalls: admitted counts are below the G0-lite targets where listed; targets are not lowered, and any "
            "top-up needs a new Haiku authoring round under the A37/A38 rules",
        ],
    }
    files["MANIFEST.json"] = _j(manifest)

    out = {"counts": counts, "shortfalls": shortfalls, "glex": manifest["glex"],
           "g3h": {k: v for k, v in manifest["g3h"].items() if k != "by_register"},
           "lint_and_drops": manifest["lint_and_drops"], "packs": {"train": counts["packs_train"],
                                                                  "held": counts["packs_held"]},
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
    packs = json.loads((root / "packs.json").read_text(encoding="utf-8"))
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
