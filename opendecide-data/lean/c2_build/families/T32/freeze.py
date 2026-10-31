"""families/T32/freeze.py: freeze the T32 pools after the Haiku extraction round (G-LEX 2/2, G3-H, pack freeze).

Runs after A38 only. Every write goes through paths.write_text / write_json / write_jsonl, which refuse before A38.
Dry run by default: checks and counts only, nothing written.

  ../../.venv/bin/python -m families.T32.freeze            (from lean/c2_build: counts, writes nothing)
  ../../.venv/bin/python -m families.T32.freeze --write    (writes families/T32/pools/)

Steps (G0_SPEC 1 R13, 7, 8; C2_DATA_SPEC 6.3; PREREG A37 (b), A38):
  1. rebuild  extract.py's pipeline in memory (collect, G-SL lint, dedup, lexicon registry, batches). The rebuilt batches
              must equal the manifests and keys on disk; otherwise the run stops.
  2. answers  the 23 extraction answer files through chunker.load_answers. An unknown, duplicate or missing qid, or an
              unreadable file, stops the run.
  3. G-LEX    lexicon.record_extraction for every answer of the two reads (glex-r1, glex-r2). A pick that is not the
              form's own meaning rejects it; so does "none of these" and a pick that is not on the list (H41). A form is
              admitted only when lexicon.status says so (2 independent reads agree, 2/2 for every kind in T32).
  4. G3-H     g3h.compare on each Mode F intro against the generator's facts (orchestrator side, never sent to Haiku).
              A mismatched intro is dropped. Template = register (the stricter reading; G0 H44 allows only tightening):
              a register whose intros match < 98% is quarantined, so all its intros are dropped.
  5. packs    PACKS_FROZEN_PER_SETTING (5) per setting, in index order: the first passing packs whose surfaces (task,
              event and topic phrases) appear nowhere else in the frozen pool. Passing packs that are surplus are kept
              as reserve, not as training input. A pack with a repeated surface is quarantined.
  6. write    pools/: skins.jsonl, skins_held.jsonl, attack_notes.jsonl, packs.jsonl, packs_reserve.jsonl,
              freeform.jsonl, freeform_held.jsonl, lexicon_admitted.jsonl, lexicon_registry.json (admitted forms only,
              gate G-LEX checked), quarantine.jsonl (every drop with its stage and reasons), and MANIFEST.json
              (sha256s, counts per kind and register, admitted vs the G0 targets, shortfalls).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from families.T32 import authoring as A  # noqa: E402
from families.T32 import extract as X  # noqa: E402
from families.T32 import fixtures as FX  # noqa: E402
from families.T32 import plugin as P  # noqa: E402

FAMILY = "T32"
POOLS = HERE / "pools"
GLEX_READS = ("glex-r1", "glex-r2")
G3H_READ = "g3h-r1"
NONE_OF_THESE = X.NONE_OF_THESE

# G0-lite targets (families/T32/G0_SPEC.md sections 2, 7, 1 R13 and 8). Never lowered.
REQUESTED = {"message_forms": 348, "packs": 42, "skins": 168, "freeform_intros": 120, "wordings": 143,
             "attack_notes": 40}
MIN_MESSAGE_PER_SEM = 12          # section 7: >= 12 admitted per sem (13 sems)
MIN_WORDING_PER_QFORM = 3         # section 7 / H40: >= 3 admitted per question form (10 forms)
PACKS_FROZEN_PER_SETTING = 5      # section 2: 30 frozen, 5 per setting
MIN_SKINS_PER_REGISTER = 6        # section 7: >= 6 skins per register (9 training + 2 held-out)
MIN_PACK = {"tasks": 8, "events": 5, "topics": 3}   # section 7
G3H_BAR = g3h.PASS_RATE           # 0.98, per template


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(p: Path) -> str:
    return _sha_bytes(p.read_bytes())


def _index(iid: str) -> int:
    return int(iid.split("|")[2])


def piece_fid(pc: dict) -> str:
    """The form id LexiconRegistry.add gives this piece: sem#sha256(text)[:8]."""
    sem = pc["sem"] if "sem" in pc else LX.question_sem(FAMILY, pc["qform"])
    return f"{sem}#{hashlib.sha256(pc['out'].encode()).hexdigest()[:8]}"


# ================================================================================================ 1. rebuild

def rebuild() -> dict:
    pools, authored = X.collect()
    surv, lint_drops = X.lint_all(pools)
    sample_probs = X.lint_values_samples()
    surv, dup_drops = X.dedup_all(surv)
    lex_in = surv.pop("message_forms", []) + surv.pop("wordings", [])
    reg, form_drops = X.build_registry(lex_in)
    if [f.form_id for f in reg.forms.values() if not f.unit_ok]:
        raise SystemExit("forms failing the unit test")
    g3 = surv.get("freeform", []) + surv.get("freeform_held", [])
    batches, task_counts = X.make_tasks(reg, g3)
    return {"pools": pools, "authored": authored, "surv": surv, "lint_drops": lint_drops, "sample_probs": sample_probs,
            "dup_drops": dup_drops, "lex_in": lex_in, "reg": reg, "form_drops": form_drops, "g3": g3,
            "batches": batches, "task_counts": task_counts}


def verify_disk(batches: list) -> dict:
    """The rebuilt batches must equal the manifests and keys on disk, or the answers would be scored against a
    different key. Returns the sha256 of each on-disk manifest and key file."""
    shas, probs = {}, []
    for read, _kind, b in batches:
        mp = X.ROOT / "manifest" / f"{b.batch_id}.json"
        kp = X.ROOT / "key" / f"{b.batch_id}.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        k = json.loads(kp.read_text(encoding="utf-8"))["key"]
        mine = b.manifest()
        if mine["tasks"] != m["tasks"] or mine["prompt_sha"] != m["prompt_sha"] or k != b.key:
            probs.append(f"{read} ({b.batch_id}): rebuilt batch differs from manifest/key on disk")
        shas[f"haiku/extract/manifest/{b.batch_id}.json"] = _sha_file(mp)
        shas[f"haiku/extract/key/{b.batch_id}.json"] = _sha_file(kp)
    if probs:
        raise SystemExit("; ".join(probs))
    return shas


# ================================================================================================ 2. answers

def load_answers(batches: list) -> tuple:
    """({read: ({internal id: answer}, batch)}, problems, answer-file sha256s)."""
    idx = json.loads((X.ROOT / "TASKS.json").read_text(encoding="utf-8"))
    task = {t["task_id"]: t for t in idx["tasks"]}
    out, problems, shas = {}, [], {}
    for read, _kind, b in batches:
        raw = {}
        for c in b.chunks:
            t = task[c["task_id"]]
            if t["answer_file"] != c["answer_file"]:
                problems.append(f"{c['task_id']}: answer path in TASKS.json differs from the chunk")
                continue
            ap = Path(t["answer_file"])
            try:
                raw[c["task_id"]] = json.loads(ap.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                problems.append(f"{c['task_id']}: {e}")
                continue
            shas[f"haiku/extract/answers/{c['task_id']}.json"] = _sha_file(ap)
        o, pr = chunker.load_answers(b, raw)
        problems += [f"{read}: {x}" for x in pr]
        out[read] = (o, b)
    return out, problems, shas


# ================================================================================================ 3. G-LEX

def record_lex(reg, answers: dict) -> dict:
    """Records every glex read. Returns counts; 'off_list' and 'none' picks are rejects (H41)."""
    st = Counter()
    for read in GLEX_READS:
        out, b = answers[read]
        choices = {b.key[it["qid"]]: it["choices"] for c in b.chunks for it in c["items"]}
        for fid in sorted(b.key.values()):
            a = out.get(fid)
            if a is None:
                st[f"{read}.unanswered"] += 1
                continue
            meaning = a.get("meaning")
            if meaning not in choices.get(fid, []):
                sem = None
                st[f"{read}.off_list"] += 1
            elif meaning == NONE_OF_THESE:
                sem = None
                st[f"{read}.none"] += 1
            else:
                sem = reg.meaning_to_sem(reg.forms[fid].kind, meaning)
                st[f"{read}.picked"] += 1
            reg.record_extraction(fid, read, sem)
    return dict(st)


def admission(reg) -> dict:
    """{form id: (status, [(read, sem or None)])} for every form in the registry."""
    return {fid: (reg.status(fid), list(f.extractions)) for fid, f in sorted(reg.forms.items())}


def admitted_registry(reg, admitted: list) -> LX.LexiconRegistry:
    """A registry with every sem and only the admitted forms, with their extractions. Gate G-LEX is checked on it."""
    out = LX.LexiconRegistry(FAMILY)
    for s in sorted(reg.sems.values(), key=lambda s: s.sem_id):
        out.declare(s.sem_id, s.kind, s.meaning)
    for fid in admitted:
        f = reg.forms[fid]
        g = out.add(f.text, f.sem_id, slots=dict(f.slots), source=f.source, family=f.family,
                    haiku_task_id=f.haiku_task_id, haiku_prompt_sha=f.haiku_prompt_sha, held_out=f.held_out)
        if g.form_id != fid:
            raise SystemExit(f"form id drift {fid} -> {g.form_id}")
        g.extractions = list(f.extractions)
    for pair in sorted(reg.antonyms, key=lambda p: sorted(p)):
        a, b = sorted(pair)
        out.declare_antonym(a, b)
    out.unit_test_all()
    return out


# ================================================================================================ 4. G3-H

def g3h_results(g3: list, answers: dict) -> tuple:
    """(per intro rows [{iid, register, ok, diffs}], template report)."""
    got, _b = answers[G3H_READ]
    rows, res = [], []
    for p in g3:
        expect = X.g3h_expect(p)
        ok, diffs = g3h.compare(expect, got[p["iid"]], list(X.G3H_FIELDS))
        rows.append({"iid": p["iid"], "register": p["register"], "ok": ok, "diffs": diffs})
        res.append((p["register"], p["iid"], ok))
    return rows, g3h.template_report(res)


def _item_level_kept(g3: list, g3_by_iid: dict) -> int:
    """Sensitivity only (not used for the pools): intros kept if the template is one brief (item) with its 3 intros,
    and the item is kept only when all of its intros match. Register-level quarantine is the frozen reading."""
    items = defaultdict(list)
    for p in g3:
        items[p["iid"].rsplit("|", 1)[0]].append(g3_by_iid[p["iid"]]["ok"])
    return sum(len(v) for v in items.values() if all(v))


# ================================================================================================ 5. packs

def freeze_packs(packs: list) -> tuple:
    """(frozen, reserve, quarantined) with per-setting counts. Frozen: the first PACKS_FROZEN_PER_SETTING passing packs
    per setting in index order whose surfaces appear nowhere else in the frozen pool."""
    by_set = defaultdict(list)
    for p in sorted(packs, key=lambda p: (p["setting"], _index(p["iid"]))):
        by_set[p["setting"]].append(p)
    frozen, reserve, quarantined, used = [], [], [], set()
    for st in A.ALL_SETTINGS:
        n = 0
        for p in by_set[st]:
            surf = [s.casefold() for k in ("tasks", "events", "topics") for s in p["out"][k]]
            clash = sorted(set(s for s in surf if surf.count(s) > 1) | (set(surf) & used))
            if clash:
                quarantined.append({"pack": p, "reasons": [f"surface repeated: {clash[:4]}"]})
            elif n < PACKS_FROZEN_PER_SETTING:
                frozen.append(p)
                used |= set(surf)
                n += 1
            else:
                reserve.append(p)
    return frozen, reserve, quarantined


# ================================================================================================ rows

def _skin_row(p: dict, pool_name: str) -> dict:
    return {"id": p["iid"], "family": FAMILY, "kind": "skin", "register": p["register"], "settings": p["settings"],
            "held_out": p["held_out"], "text": p["out"], "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
            "pool": pool_name}


def _free_row(p: dict, g3_ok: bool) -> dict:
    return {"id": p["iid"], "family": FAMILY, "kind": "freeform", "register": p["register"],
            "settings": p["settings"], "held_out": p["held_out"], "text": p["out"], "facts": p["facts"],
            "task_id": p["task_id"], "prompt_sha": p["prompt_sha"], "g3h": "pass" if g3_ok else "fail"}


def _pack_row(p: dict) -> dict:
    return {"id": p["iid"], "family": FAMILY, "kind": "pack", "setting": p["setting"], "tasks": p["out"]["tasks"],
            "events": p["out"]["events"], "topics": p["out"]["topics"], "task_id": p["task_id"],
            "prompt_sha": p["prompt_sha"]}


def _attack_row(p: dict) -> dict:
    return {"id": p["iid"], "family": FAMILY, "kind": "attack_note", "text": p["out"], "task_id": p["task_id"],
            "prompt_sha": p["prompt_sha"]}


def _lex_row(reg, fid: str) -> dict:
    f = reg.forms[fid]
    return {"form_id": fid, "family": FAMILY, "kind": f.kind, "sem_id": f.sem_id, "text": f.text,
            "slots": dict(f.slots), "extractions": [list(e) for e in f.extractions], "unit_ok": f.unit_ok,
            "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha}


# ================================================================================================ run

def run(write: bool) -> dict:
    prob = X.self_check()
    if prob:
        raise SystemExit("self-check failed: " + "; ".join(prob))
    rb = rebuild()
    disk_shas = verify_disk(rb["batches"])
    answers, ans_probs, ans_shas = load_answers(rb["batches"])
    if ans_probs:
        raise SystemExit("answer problems: " + "; ".join(ans_probs[:10]))
    reg = rb["reg"]
    lex_reads = record_lex(reg, answers)
    adm = admission(reg)
    g3_rows, g3_rep = g3h_results(rb["g3"], answers)
    g3_by_iid = {r["iid"]: r for r in g3_rows}
    surv = rb["surv"]

    # ---- lexicon: which pieces map to which form, and which forms are admitted
    admitted_fids = sorted(fid for fid, (s, _) in adm.items() if s == "admitted")
    adm_set = set(admitted_fids)
    quarantine = []
    for pc in rb["lex_in"]:
        if not pc.get("ok"):
            continue
        fid = piece_fid(pc)
        if fid not in reg.forms:
            raise SystemExit(f"piece {pc['iid']} maps to no registry form")
        if fid not in adm_set:
            status, ext = adm[fid]
            quarantine.append({"stage": "G-LEX", "pool": "wordings" if "qform" in pc else "message_forms",
                               "id": pc["iid"], "task_id": pc["task_id"], "form_id": fid, "status": status,
                               "text": pc["out"], "reads": [[r, s] for r, s in ext],
                               "reasons": [f"{r} picked {reg.sems[s].meaning!r}" if s else f"{r} did not pick its own "
                                           f"meaning" for r, s in ext if s != reg.forms[fid].sem_id]})
    for ent in rb["form_drops"]:
        quarantine.append({"stage": "lexicon_form", "pool": ent["pool"], "id": ent["pid"], "task_id": ent["task_id"],
                           "reasons": ent["reasons"]})
    adm_lex = admitted_registry(reg, admitted_fids)
    lex_gate = adm_lex.gate()

    # ---- packs (5 per setting; surplus = reserve; repeated surface = quarantine)
    frozen_packs, reserve_packs, pack_quar = freeze_packs(surv["packs"])
    for q in pack_quar:
        quarantine.append({"stage": "pack_surface", "pool": "packs", "id": q["pack"]["iid"],
                           "task_id": q["pack"]["task_id"], "reasons": q["reasons"]})

    # ---- G-SL lint and dedup drops (already logged by extract.py; repeated here for the one quarantine file)
    for d in rb["lint_drops"]:
        quarantine.append({"stage": "G-SL lint", "pool": d["pool"], "id": d["pid"], "task_id": d["task_id"],
                           "reasons": d["reasons"]})
    for d in rb["dup_drops"]:
        quarantine.append({"stage": "dedup", "pool": d["pool"], "id": d["pid"], "task_id": d["task_id"],
                           "reasons": d["reasons"]})

    # ---- G3-H: mismatches and quarantined registers
    quarantined_regs = set(g3_rep["quarantined"])
    free_pass, free_fail = [], []
    for p in rb["g3"]:
        r = g3_by_iid[p["iid"]]
        if r["ok"] and p["register"] not in quarantined_regs:
            free_pass.append(p)
        else:
            why = []
            if not r["ok"]:
                why.append("G3-H mismatch: " + "; ".join(r["diffs"]))
            if p["register"] in quarantined_regs:
                why.append(f"G3-H register quarantined ({g3_rep['templates'][p['register']]['rate']:.1%} < 98%)")
            free_fail.append(p)
            quarantine.append({"stage": "G3-H", "pool": "freeform_held" if p["held_out"] else "freeform",
                               "id": p["iid"], "task_id": p["task_id"], "register": p["register"],
                               "text": p["out"], "reasons": why})

    skins = [p for p in surv["skins"] if not p["held_out"]]
    skins_held = [p for p in surv["skins_held"] if p["held_out"]]
    attacks = surv["attack_notes"]
    free_train = [p for p in free_pass if not p["held_out"]]
    free_held = [p for p in free_pass if p["held_out"]]
    # the lint step keeps held-out pieces in their own pool; a training piece never lands in the held pool
    if any(p["held_out"] for p in skins) or any(not p["held_out"] for p in skins_held):
        raise SystemExit("held-out flag does not match the pool")

    manifest_files = {}
    rows_out = {
        "skins.jsonl": [_skin_row(p, "skins") for p in skins],
        "skins_held.jsonl": [_skin_row(p, "skins_held") for p in skins_held],
        "attack_notes.jsonl": [_attack_row(p) for p in attacks],
        "packs.jsonl": [_pack_row(p) for p in sorted(frozen_packs, key=lambda p: (A.ALL_SETTINGS.index(p["setting"]),
                                                                              _index(p["iid"])))],
        "packs_reserve.jsonl": [_pack_row(p) for p in reserve_packs],
        "freeform.jsonl": [_free_row(p, True) for p in free_train],
        "freeform_held.jsonl": [_free_row(p, True) for p in free_held],
        "lexicon_admitted.jsonl": [_lex_row(reg, fid) for fid in admitted_fids],
        "quarantine.jsonl": quarantine,
    }

    # ---- counts and targets
    msg_by_sem = Counter(reg.forms[f].sem_id for f in admitted_fids if reg.forms[f].kind == "other")
    wording_by_q = Counter(reg.forms[f].sem_id for f in admitted_fids if reg.forms[f].kind == "question")
    skin_by_reg = Counter(p["register"] for p in skins + skins_held)
    free_by_reg = Counter(p["register"] for p in rb["g3"])
    free_pass_by_reg = Counter(p["register"] for p in free_pass)
    pack_by_set = Counter(p["setting"] for p in frozen_packs)
    settings_skins = Counter(s for p in skins for s in p["settings"])

    shortfalls = []
    for sem in sorted(FX.MESSAGE_MEANINGS):
        n = msg_by_sem.get(sem, 0)
        if n < MIN_MESSAGE_PER_SEM:
            shortfalls.append(f"message form {sem}: {n} admitted < {MIN_MESSAGE_PER_SEM}")
    for qf in sorted(FX.QUESTION_MEANINGS):
        n = wording_by_q.get(LX.question_sem(FAMILY, qf), 0)
        if n < MIN_WORDING_PER_QFORM:
            shortfalls.append(f"wording {qf}: {n} admitted < {MIN_WORDING_PER_QFORM}")
    for st in A.ALL_SETTINGS:
        if pack_by_set.get(st, 0) < PACKS_FROZEN_PER_SETTING:
            shortfalls.append(f"packs {st}: {pack_by_set.get(st, 0)} frozen < {PACKS_FROZEN_PER_SETTING}")
    for reg_name in A.TRAIN_REGISTERS + A.HELD_REGISTERS:
        n = skin_by_reg.get(reg_name, 0)
        if n < MIN_SKINS_PER_REGISTER:
            shortfalls.append(f"skins {reg_name}: {n} admitted < {MIN_SKINS_PER_REGISTER}")
    for reg_name, rate_info in g3_rep["templates"].items():
        if rate_info["quarantined"]:
            shortfalls.append(f"G3-H {reg_name}: {rate_info['ok']}/{rate_info['n']} intros match "
                              f"({rate_info['rate']:.1%} < 98%); register quarantined")
    shortfalls.append(f"Mode F intros: {len(free_pass)} admitted of {REQUESTED['freeform_intros']} requested "
                      f"({len(free_train)} training, {len(free_held)} held-out)")
    if len(frozen_packs) < 30:
        shortfalls.append(f"packs: {len(frozen_packs)} frozen < 30")
    n_msg = sum(msg_by_sem.values())
    n_word = sum(wording_by_q.values())
    n_skin = len(skins) + len(skins_held)
    for name, got, req in (("message forms", n_msg, REQUESTED["message_forms"]),
                           ("wordings", n_word, REQUESTED["wordings"]),
                           ("skins (train + held)", n_skin, REQUESTED["skins"]),
                           ("attack notes", len(attacks), REQUESTED["attack_notes"])):
        if got < req:
            shortfalls.append(f"{name}: {got} admitted of {req} requested")
    if not lex_gate["pass"]:
        shortfalls.append(f"G-LEX gate on the admitted registry fails: {lex_gate['status_counts']}")

    counts = {
        "authored_by_pool": rb["authored"],
        "lint_dropped_by_pool": dict(Counter(d["pool"] for d in rb["lint_drops"])),
        "dedup_dropped_total": len(rb["dup_drops"]),
        "lexicon_candidates_after_lint": len(rb["lex_in"]),
        "lexicon_form_drops": len(rb["form_drops"]),
        "lexicon_forms_registry": len(reg.forms),
        "lexicon_forms_admitted": len(admitted_fids),
        "lexicon_forms_rejected_by_gLEX": sum(1 for s, _ in adm.values() if s == "rejected"),
        "lexicon_forms_pending": sum(1 for s, _ in adm.values() if s == "pending"),
        "lexicon_forms_admitted_by_kind": dict(Counter(reg.forms[f].kind for f in admitted_fids)),
        "glex_reads": lex_reads,
        "message_admitted_by_sem": dict(sorted(msg_by_sem.items())),
        "wording_admitted_by_qform": {qf: wording_by_q.get(LX.question_sem(FAMILY, qf), 0)
                                      for qf in sorted(FX.QUESTION_MEANINGS)},
        "g3h_intros": len(rb["g3"]),
        "g3h_mismatch": sum(1 for r in g3_rows if not r["ok"]),
        "g3h_register_rates": {k: [v["ok"], v["n"], round(v["rate"], 3), v["quarantined"]]
                               for k, v in g3_rep["templates"].items()},
        "g3h_quarantined_registers": sorted(quarantined_regs),
        "g3h_pass_total": len(free_pass),
        "g3h_intros_item_level_kept": _item_level_kept(rb["g3"], g3_by_iid),
        "skins_admitted_by_register": dict(sorted(skin_by_reg.items())),
        "skins_by_setting_training": dict(sorted(settings_skins.items())),
        "packs_authored": len(surv["packs"]),
        "packs_frozen": len(frozen_packs),
        "packs_frozen_by_setting": dict(sorted(pack_by_set.items())),
        "packs_reserve": len(reserve_packs),
        "packs_quarantined_surface": len(pack_quar),
        "attack_notes": len(attacks),
        "quarantine_entries": len(quarantine),
        "quarantine_by_stage": dict(Counter(q["stage"] for q in quarantine)),
        "answers_loaded": {r: len(answers[r][0]) for r in answers},
    }
    result = {"counts": counts, "shortfalls": shortfalls, "lex_gate": {k: v for k, v in lex_gate.items()
                                                                       if k != "not_admitted"},
              "written": write}
    if write:
        _write(rb, reg, rows_out, admitted_fids, adm_lex, counts, shortfalls, disk_shas, ans_shas, g3_rep,
               lex_gate, free_pass, frozen_packs, reserve_packs)
    return result


def _write(rb, reg, rows_out, admitted_fids, adm_lex, counts, shortfalls, disk_shas, ans_shas, g3_rep, lex_gate,
           free_pass, frozen_packs, reserve_packs) -> None:
    POOLS.mkdir(parents=True, exist_ok=True)
    file_sha = {}
    for name, rows in rows_out.items():
        p = paths.write_jsonl(POOLS / name, rows)
        file_sha[f"pools/{name}"] = {"sha256": _sha_file(p), "rows": len(rows)}
    lr = adm_lex.to_json()
    p = paths.write_json(POOLS / "lexicon_registry.json", lr)
    file_sha["pools/lexicon_registry.json"] = {"sha256": _sha_file(p), "rows": len(lr["forms"])}
    manifest = {
        "family": FAMILY, "version": X.VERSION, "stage": "freeze",
        "g0_spec": {"path": "families/T32/G0_SPEC.md", "sha256": P.T32.G0_SHA256,
                    "extract_tasks_g0_sha256": json.loads((X.ROOT / "TASKS.json").read_text(encoding="utf-8"))
                    ["g0_sha256"]},
        "prereg_final_sha256": hashlib.sha256(paths.PREREG.read_bytes()).hexdigest(),
        "inputs": {"extract_manifests_and_keys": disk_shas, "extract_answers": ans_shas,
                   "extract_tasks_json": _sha_file(X.ROOT / "TASKS.json")},
        "decisions": {
            "glex": "2/2 independent reads (lexicon.status); off-list or 'none of these' picks count as rejects (H41)",
            "g3h_template": "register (stricter reading); a register under 98% is quarantined, all its intros dropped",
            "packs": f"first {PACKS_FROZEN_PER_SETTING} passing packs per setting in index order, no surface repeated "
                     "in the frozen pool; surplus packs are reserve",
            "held_out": "skins_held and freeform_held carry held-out registers (sms_export, forum_thread): mixdev only",
            "quarantine": "every dropped or failed piece, with stage and reasons, in pools/quarantine.jsonl",
        },
        "targets_g0": {"message_forms_per_sem_min": MIN_MESSAGE_PER_SEM, "message_sems": len(FX.MESSAGE_MEANINGS),
                       "wordings_per_qform_min": MIN_WORDING_PER_QFORM, "qforms": len(FX.QUESTION_MEANINGS),
                       "packs_frozen_per_setting": PACKS_FROZEN_PER_SETTING, "settings": len(A.ALL_SETTINGS),
                       "skins_per_register_min": MIN_SKINS_PER_REGISTER,
                       "pack_min_per_pack": MIN_PACK, "g3h_bar_per_template": G3H_BAR, "requested": REQUESTED},
        "counts": counts,
        "shortfalls": shortfalls,
        "lexicon_gate_admitted_registry": {k: v for k, v in lex_gate.items() if k != "not_admitted"},
        "open_items": [
            "file-access audit (c2_kit.audit) for the 23 extraction agents: no audit results are on disk in "
            "families/T32; the orchestrator must confirm every transcript passed before these pools feed generation",
            "G3-H template for Mode F is the register (stricter reading). An item-level reading (template = the 3 "
            "intros of one brief) keeps the intros of items where all 3 match: see counts.g3h_intros_item_level_kept",
            "Mode F: only email_digest survives G3-H in training registers and no held-out intro survives; "
            "a new Mode F authoring round needs an orchestrator decision (not run here)",
            "G-LEX rejected 5 yn_dneg_broken wordings (readers split true vs false on the double negation); "
            "this is the G0 point-9 watch item",
        ],
        "files": file_sha,
    }
    mp = paths.write_json(POOLS / "MANIFEST.json", manifest)
    print(f"wrote {len(file_sha)} pool files and MANIFEST.json to {POOLS} ({mp.name})")


def main(argv: list) -> int:
    write = "--write" in argv
    res = run(write)
    print(json.dumps(res["counts"], indent=1, ensure_ascii=False, default=str))
    print("SHORTFALLS:")
    for s in res["shortfalls"]:
        print("  -", s)
    print(f"lex gate (admitted registry): pass={res['lex_gate']['pass']} status={res['lex_gate']['status_counts']}")
    print(f"written: {res['written']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
