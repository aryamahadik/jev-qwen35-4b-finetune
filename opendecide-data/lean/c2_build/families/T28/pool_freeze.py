"""families/T28/pool_freeze.py: G-LEX admission, the G3-H comparison of the Mode F memos, the quarantine and the pool
freeze for T28 (G0_SPEC.md sections 7 and 9; C2_DATA_SPEC 6.2 item 2 and 6.4 steps 3-4).

  check    in memory only: rebuild every extraction batch and plan file and check them byte for byte against the files on
           disk, record the answers, admit or quarantine every piece, and print the counts and every shortfall against the
           G0 targets. Nothing is written.
  freeze   the same, then write families/T28/pools/ (skins, documents, attack, wordings, lexicon, packs, QUARANTINE,
           MANIFEST) through paths.write_files. Refuses when pools/MANIFEST.json already exists.

Run from lean/:  ../.venv/bin/python c2_build/families/T28/pool_freeze.py check|freeze

Haiku answers only flag. A form's sem id is the registry's own declaration. A read says which listed meaning it chose;
admission needs 2/2 independent reads (3/3 for precedence) to choose the declared meaning (G-LEX). A null, an unlisted
text or another meaning is a disagreement. A memo is admitted only when the G3-H extraction matches both facts exactly
(g3h.compare). No label is set here, and no row is generated.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import g3h  # noqa: E402
from c2_kit import lexicon as L  # noqa: E402
from c2_kit import paths  # noqa: E402
from families.T28 import haiku_author as A  # noqa: E402
from families.T28 import haiku_extract as HX  # noqa: E402
from families.T28 import plugin as P  # noqa: E402

F = "T28"
EXTRACT = HX.EXTRACT
POOLS = HERE / "pools"
G0 = HERE / "G0_SPEC.md"
TRAIN = tuple(A.TRAIN_REGISTERS)
HELD = tuple(A.HELD_REGISTERS)
MEMO_REGS = tuple(A.FREEFORM_REGISTERS)
PREC_SENSES = ("prec.P1", "prec.P2", "prec.P3", "prec.P4", "prec.P5")
CMP_SENSES = ("cmp.le", "cmp.lt", "cmp.ge", "cmp.gt")
QFORMS = tuple(P.T28Plugin.QFORMS)

# G0-lite section 7 (and section 2 where stated). Not lowered. Where G0 gives only an ask count ("N asked"), that count is
# the target for the admitted pool, and the note says so.
G0_TARGETS = {
    "packs_admitted_min": 40,            # s7: >= 40 admitted (56 asked)
    "packs_held_share_min": 0.15,        # s7: >= 15% held out (10 marked held_out by the program)
    "skins_train_per_register": A.N_SKIN_TRAIN,    # s7: 75 asked per training register (target = the ask)
    "skins_held_per_register": A.N_SKIN_HELD,      # s7: 25 asked per held-out register (target = the ask)
    "memos_admitted": A.N_FREEFORM,      # s7: 160 asked (target = the ask)
    "memo_share_max": 0.25,              # s7: Mode F <= 25% of rows (checked here as a share of the narrative pool)
    "attacks_admitted": A.N_ATTACK,      # s7: 50 asked (target = the ask)
    "attacks_held_min": A.N_ATTACK_HELD,  # s7 plan: 10 held out
    "wordings_per_form_min": 6,          # s7: >= 6 admitted per question form (13 forms)
    "wordings_ch_verdict_min": 20,       # s7: ch_verdict >= 20
    "wordings_yn_allow_min": 10,         # s7: yn_allow >= 10
    "prec_per_policy_min": 6,            # s7: >= 6 admitted 3/3 per P1-P5 (12 asked each)
    "cmp_per_sense": A.N_CMP,            # s7: 8 asked per cmp sense, 2/2 (target = the ask)
}


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def _fid(sem_id: str, text: str) -> str:
    """The registry's own form id (LexiconRegistry.add): sem#sha256(text)[:8]."""
    return f"{sem_id}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"


def _meanings(reg, kind: str) -> set:
    return {s.meaning for s in reg.sems.values() if s.kind == kind}


def _same(path: Path, text: str, label: str, probs: list) -> None:
    if not path.is_file():
        probs.append(f"{label}: missing on disk")
    elif path.read_text(encoding="utf-8") != text:
        probs.append(f"{label}: differs from the rebuilt file")


# ------------------------------------------------------------------------------------------------ verify before recording
def verify(rep: dict, reg, lex: list, g3, expected: dict) -> list:
    """Rebuild every extraction batch in memory and compare it byte for byte with the files Haiku was given (prompt,
    chunks, key, manifest, task files), then the TASKS.json rows and the three plan files. Run before any read is
    recorded, so the registry is still all pending."""
    probs = []
    tasks = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    on_disk = {t["task_id"]: t for t in tasks["tasks"]}
    n = 0
    for name, b in list(lex) + [("g3h", g3)]:
        for rel, text in sorted(b.files().items()):
            _same(EXTRACT / rel, text, f"{name}:{rel}", probs)
        for c in b.chunks:
            tid = c["task_id"]
            n += 1
            ans = str(EXTRACT / b.answer_path(tid))
            _same(EXTRACT / "tasks" / f"{tid}.md", HX.task_text(b, c, ans), f"{name}:tasks/{tid}.md", probs)
            t = on_disk.get(tid)
            if t is None:
                probs.append(f"{tid}: not in TASKS.json")
                continue
            want = {"batch_id": b.batch_id, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha, "kind": b.kind,
                    "answer_file": ans, "task_file": str(EXTRACT / "tasks" / f"{tid}.md")}
            for k, v in want.items():
                if t.get(k) != v:
                    probs.append(f"{tid}: TASKS.json {k} differs from the rebuilt task")
    if len(on_disk) != n:
        probs.append(f"TASKS.json lists {len(on_disk)} tasks, the rebuild has {n}")
    _same(EXTRACT / "plan" / "lint_report.json", json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
          "plan/lint_report.json", probs)
    _same(EXTRACT / "plan" / "glex_registry_pending.json",
          json.dumps(reg.to_json(), ensure_ascii=False, indent=1) + "\n", "plan/glex_registry_pending.json", probs)
    _same(EXTRACT / "plan" / "g3h_expected.json",
          json.dumps(expected, ensure_ascii=False, indent=1, sort_keys=True) + "\n", "plan/g3h_expected.json", probs)
    return probs


# ------------------------------------------------------------------------------------------------ read and record
def read_answers(batches: list) -> tuple:
    """({read: {task id: parsed answer list}}, {task id: answer sha256}, problems) from answers/<task id>.json."""
    raw, sha, probs = {}, {}, []
    for name, b in batches:
        raw[name] = {}
        for c in b.chunks:
            tid = c["task_id"]
            p = EXTRACT / "answers" / f"{tid}.json"
            if not p.is_file():
                probs.append(f"{tid}: answer file missing")
                continue
            data = p.read_bytes()
            sha[tid] = _sha_bytes(data)
            try:
                raw[name][tid] = json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                probs.append(f"{tid}: not valid JSON ({e})")
    return raw, sha, probs


def record_lex(reg, lex: list, raw: dict) -> tuple:
    """reg.record_extraction for every answered form. The chosen meaning maps to its sem id; null, an unlisted text or
    a different meaning is recorded as a disagreement (None or another sem), never as a default."""
    counts, problems = {}, []
    for name, b in lex:
        got, probs = CH.load_answers(b, raw.get(name, {}))
        problems += [f"{name}: {p}" for p in probs]
        c = Counter()
        for fid, a in sorted(got.items()):
            f = reg.forms[fid]
            choice = a.get("choice") if isinstance(a, dict) else None
            if choice is None:
                outcome, sem = "null", None
            elif isinstance(choice, str) and choice in _meanings(reg, f.kind):
                sem = reg.meaning_to_sem(f.kind, choice)
                outcome = "listed" if sem == f.sem_id else "listed_other_sense"
            else:
                outcome, sem = "not_listed", None
            c[outcome] += 1
            reg.record_extraction(fid, name, sem)
        c["unanswered"] = len(set(b.key.values()) - set(got))
        counts[name] = dict(c)
    return counts, problems


# ------------------------------------------------------------------------------------------------ G3-H
def g3h_compare(g3, raw: dict, expected: dict) -> tuple:
    """g3h.compare per memo (expected = the brief's USER and AGENT). -> ({sid: (ok, diffs)}, template report, problems)."""
    fields = P.T28Plugin.extract_fields(None, None)
    got, probs = CH.load_answers(g3, raw)
    ok_of, results = {}, []
    for sid in sorted(expected):
        if sid not in got:
            ok_of[sid] = (False, ["unanswered"])
        else:
            ok_of[sid] = g3h.compare(expected[sid], got[sid], fields)
        results.append((sid, sid, ok_of[sid][0]))
    return ok_of, g3h.template_report(results), probs


# ------------------------------------------------------------------------------------------------ admission
def admit() -> dict:
    loaded, load_probs = HX.load_all()
    rep = HX.lint_report(loaded, load_probs)
    reg, refused = HX.build_registry(loaded)
    lex = HX.glex_batches(reg)
    g3, expected = HX.g3h_batch(loaded["freeform"])
    verify_problems = verify(rep, reg, lex, g3, expected)

    batches = list(lex) + [("g3h", g3)]
    raw, answer_sha, read_problems = read_answers(batches)
    read_counts, rec_problems = record_lex(reg, lex, raw)
    g3_ok, g3_report, g3_probs = g3h_compare(g3, raw["g3h"], expected)

    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    kept_packs, pack_value_probs = HX.value_lint_packs(loaded["packs"])

    q_rows = []
    for name, plist in load_probs.items():
        kind = {"skins": "skin", "freeform": "document", "attacks": "attack", "wordings": "wording",
                "precedence": "lexicon", "comparators": "lexicon", "packs": "pack"}.get(name, name)
        for iid, reason in HX._split(plist):
            stage = "G-SL" if "G-SL" in reason else "load-check"
            q_rows.append({"piece": f"{name}|{iid}", "kind": kind, "stage": stage, "reason": reason})
    for p, r in pack_value_probs:
        q_rows.append({"piece": p, "kind": "pack", "stage": "value-lint", "reason": r})

    # G-LEX: forms that are not admitted (a disagreement, a unit-test failure or too few reads)
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        st = status_of[fid]
        if st == "admitted":
            continue
        if st == "unit_fail":
            why = "unit test: " + "; ".join(f.unit_problems[:2])
        elif st == "rejected":
            bad = [f"{e}: {'null' if s is None else s}" for e, s in f.extractions if s != f.sem_id]
            why = "a read disagrees with the declared sense: " + ", ".join(bad)
        else:
            why = f"{len(f.extractions)} of {f.required} independent reads agree (need {f.required})"
        q_rows.append({"piece": f"lexicon|{fid}", "kind": f.kind, "sense": f.sem_id, "stage": "G-LEX",
                       "status": st, "reason": why})

    # wordings: the form each accepted wording was registered under, admitted or quarantined
    wording_cands, wordings = [], []
    for q, text, held, tid, psha in loaded["wordings"]:
        fid = _fid(L.question_sem(F, q), text)
        st = status_of.get(fid, "missing")
        wording_cands.append({"qform": q, "text": text, "held_out": held, "form_id": fid, "status": st})
        if st == "admitted":
            wordings.append({"form_id": fid, "qform": q, "text": text, "held_out": held, "sense": L.question_sem(F, q),
                             "haiku_task_id": tid, "haiku_prompt_sha": psha})
        else:
            q_rows.append({"piece": f"wording|{fid}", "kind": "wording", "stage": "G-LEX", "status": st,
                           "reason": f"form {fid} is {st}"})

    # G3-H: a memo whose extraction does not match both facts exactly is dropped (a single read per memo, so a
    # mismatch is a template below 98%)
    memos = {}
    for sid, sk in sorted(loaded["freeform"].items()):
        ok, diffs = g3_ok[sid]
        if ok:
            memos[sid] = sk
        else:
            q_rows.append({"piece": f"document|{sid}", "kind": "document", "stage": "G3-H", "status": "mismatch",
                           "reason": "; ".join(diffs[:3])})

    gate_used = reg.gate([fid for fid, st in status_of.items() if st == "admitted"])
    return {"loaded": loaded, "load_problems": load_probs, "rep": rep, "refused": refused, "reg": reg,
            "status_of": status_of, "skins": dict(sorted(loaded["skins"].items())), "memos": memos,
            "attacks": dict(sorted(loaded["attacks"].items())), "wordings": wordings,
            "wording_cands": wording_cands, "packs": kept_packs, "quarantine": q_rows, "verify": verify_problems,
            "read_problems": read_problems, "rec_problems": rec_problems, "g3_probs": g3_probs,
            "g3_report": g3_report, "g3_ok": g3_ok, "read_counts": read_counts, "answer_sha": answer_sha,
            "batches": batches, "lex": lex, "gate_used": gate_used, "gate_all": reg.gate()}


# ------------------------------------------------------------------------------------------------ counts and targets
def counts(st: dict) -> dict:
    reg, status_of = st["reg"], st["status_of"]
    skins, memos, attacks = st["skins"], st["memos"], st["attacks"]
    by_reg = {}
    for r in TRAIN + HELD:
        held = r in HELD
        sel = [sk for sk in skins.values() if sk.register == r]
        by_reg[r] = {"admitted": len(sel), "held_out": held,
                     "asked": A.N_SKIN_HELD if held else A.N_SKIN_TRAIN,
                     "held_flag_consistent": all(bool(sk.held_out) == held for sk in sel)}
    memo_by_reg = {r: {"admitted": sum(1 for sk in memos.values() if sk.register == r),
                       "asked": A.N_FREEFORM // len(MEMO_REGS)} for r in MEMO_REGS}
    n_T = len(skins)
    n_F = len(memos)
    wq = {}
    for q in QFORMS:
        cands = [w for w in st["wording_cands"] if w["qform"] == q]
        adm = [w for w in st["wordings"] if w["qform"] == q]
        wq[q] = {"candidates": len(cands), "admitted": len(adm),
                 "held_admitted": sum(1 for w in adm if w["held_out"]), "asked": sum(A.WORDING_PLAN[q])}
    prec = {}
    for s in PREC_SENSES:
        fs = [f for f in reg.forms.values() if f.kind == "precedence" and f.sem_id == s]
        prec[s] = {"candidates": len(fs), "admitted": sum(1 for f in fs if status_of[f.form_id] == "admitted")}
    cmp_ = {}
    for s in CMP_SENSES:
        fs = [f for f in reg.forms.values() if f.kind == "comparator" and f.sem_id == s]
        cmp_[s] = {"candidates": len(fs), "admitted": sum(1 for f in fs if status_of[f.form_id] == "admitted")}
    packs = st["packs"]
    return {
        "skins_by_register": by_reg,
        "skins_T_admitted": n_T,
        "memos_by_register": memo_by_reg,
        "memos_F_admitted": n_F,
        "memo_share_of_narrative": round(n_F / (n_T + n_F), 4) if n_T + n_F else None,
        "attacks": {"admitted": len(attacks), "held_out": sum(1 for sk in attacks.values() if sk.held_out)},
        "wordings_by_qform": wq,
        "wordings_admitted": len(st["wordings"]),
        "wordings_candidates": len(st["wording_cands"]),
        "precedence_by_policy": prec,
        "comparators_by_sense": cmp_,
        "packs": {"admitted": len(packs), "held_out": sum(1 for p in packs if p.get("held_out"))},
        "lexicon_forms": len(reg.forms),
        "lexicon_status": dict(sorted(Counter(status_of.values()).items())),
    }


def shortfalls(c: dict) -> list:
    t, out = G0_TARGETS, []
    pk = c["packs"]
    if pk["admitted"] < t["packs_admitted_min"]:
        out.append(f"packs admitted {pk['admitted']} < {t['packs_admitted_min']} (s7)")
    if pk["admitted"] and pk["held_out"] / pk["admitted"] < t["packs_held_share_min"]:
        out.append(f"packs held_out {pk['held_out']} of {pk['admitted']} < {t['packs_held_share_min']:.0%} (s7)")
    for r, d in c["skins_by_register"].items():
        want = t["skins_held_per_register"] if d["held_out"] else t["skins_train_per_register"]
        if d["admitted"] < want:
            out.append(f"skins {r}: admitted {d['admitted']} < {want} (s7 ask, held_out={d['held_out']})")
        if not d["held_flag_consistent"]:
            out.append(f"skins {r}: held_out flag inconsistent with the held-out register list")
    for r, d in c["memos_by_register"].items():
        if d["admitted"] < d["asked"]:
            out.append(f"memos {r}: admitted {d['admitted']} < {d['asked']} asked (s7)")
    if c["memos_F_admitted"] < t["memos_admitted"]:
        out.append(f"memos admitted {c['memos_F_admitted']} < {t['memos_admitted']} asked (s7)")
    if c["memo_share_of_narrative"] is not None and c["memo_share_of_narrative"] > t["memo_share_max"]:
        out.append(f"memo share {c['memo_share_of_narrative']} > {t['memo_share_max']} (s7)")
    at = c["attacks"]
    if at["admitted"] < t["attacks_admitted"]:
        out.append(f"attacks admitted {at['admitted']} < {t['attacks_admitted']} asked (s7)")
    if at["held_out"] < t["attacks_held_min"]:
        out.append(f"attacks held_out {at['held_out']} < {t['attacks_held_min']} (s7 plan)")
    for q, d in c["wordings_by_qform"].items():
        floor = t["wordings_per_form_min"]
        if q == "ch_verdict":
            floor = max(floor, t["wordings_ch_verdict_min"])
        if q == "yn_allow":
            floor = max(floor, t["wordings_yn_allow_min"])
        if d["admitted"] < floor:
            out.append(f"wordings {q}: admitted {d['admitted']} < {floor} (s7)")
    for s, d in c["precedence_by_policy"].items():
        if d["admitted"] < t["prec_per_policy_min"]:
            out.append(f"precedence {s}: admitted 3/3 {d['admitted']} < {t['prec_per_policy_min']} (s7)")
    for s, d in c["comparators_by_sense"].items():
        if d["admitted"] < t["cmp_per_sense"]:
            out.append(f"comparator {s}: admitted 2/2 {d['admitted']} < {t['cmp_per_sense']} asked (s7)")
    return out


# ------------------------------------------------------------------------------------------------ freeze
def _obj(sk) -> dict:
    return dataclasses.asdict(sk)


def _pool_files(st: dict, c: dict) -> dict:
    reg, status_of = st["reg"], st["status_of"]
    lex = reg.to_json()
    for f in lex["forms"]:
        f["usable"] = f["status"] == "admitted"
    skins = [_obj(sk) for sk in st["skins"].values()]
    docs = [_obj(sk) for sk in st["memos"].values()]
    atts = [_obj(sk) for sk in st["attacks"].values()]
    packs = {"count": len(st["packs"]), "held_out": c["packs"]["held_out"], "packs": st["packs"],
             "s5_split": "held_out is set by the program (plan: 10 of 56 asked); S5 / mixdev only"}
    return {
        "skins.json": _dump({"family": F, "mode": "T", "count": len(skins),
                             "held_out_registers": list(HELD), "skins": skins}),
        "documents.json": _dump({"family": F, "mode": "F", "count": len(docs),
                                 "g3h": "every memo matched both facts exactly (g3h.compare)", "documents": docs}),
        "attack.json": _dump({"family": F, "count": len(atts), "attacks": atts}),
        "wordings.json": _dump({"family": F, "count": len(st["wordings"]), "wordings": st["wordings"]}),
        "lexicon.json": _dump(lex),
        "packs.json": _dump({"family": F, **packs}),
        "QUARANTINE.json": _dump({"family": F, "count": len(st["quarantine"]), "rows": st["quarantine"]}),
    }


def manifest_obj(st: dict, c: dict, short: list, files: dict) -> dict:
    g0_sha = _sha_bytes(G0.read_bytes())
    reads = {}
    for name, b in st["batches"]:
        reads[name] = {"batch_id": b.batch_id, "kind": b.kind, "prompt_sha": b.prompt_sha, "n_items": len(b.key),
                       "tasks": {c_["task_id"]: {"n": len(c_["items"]), "answer_sha256": st["answer_sha"].get(c_["task_id"])}
                                 for c_ in b.chunks}}
    qc = Counter(q["stage"] for q in st["quarantine"])
    status = ("FROZEN WITH SHORTFALLS: every piece that failed is quarantined; the targets listed as shortfalls are not met "
              "(not lowered). G13-seed and row generation not run.") if short else \
             "FROZEN: every G0 target met. G13-seed and row generation not run."
    return {
        "family": F,
        "version": "freeze-v1",
        "status": status,
        "g0": {"path": "families/T28/G0_SPEC.md", "sha256": g0_sha,
               "matches_plugin_pin": g0_sha == P.T28Plugin.G0_SHA256},
        "reads": reads,
        "answer_reads": st["read_counts"],
        "load_problems": {k: len(v) for k, v in st["load_problems"].items()},
        "problems": {"verify_rebuild": st["verify"], "answers": st["read_problems"],
                     "record": st["rec_problems"], "g3h": st["g3_probs"]},
        "gates": {
            "G-LEX_used_forms": {k: v for k, v in st["gate_used"].items() if k != "not_admitted"},
            "G-LEX_all_registry_forms": {k: v for k, v in st["gate_all"].items() if k != "not_admitted"},
            "G-LEX_not_admitted_count": len(st["gate_all"]["not_admitted"]),
            "G3-H": {"memos_compared": len(st["g3_ok"]), "matched": sum(1 for ok, _ in st["g3_ok"].values() if ok),
                     "templates": st["g3_report"]},
            "G-SL": "applied at load (gsl.lint_template / lint_freeform / lint_values; check_skin, check_attack, check_freeform)",
            "G13_seed": "not run (6.4 step 4; needs the decontamination program, not run in this step)",
            "G2_G4_G-TW": "not run at pool stage (rows only)"},
        "counts": c,
        "targets_g0": G0_TARGETS,
        "targets_note": "Where G0 gives only an ask count, the ask is the target and the admitted pool is compared with it.",
        "shortfalls": short,
        "quarantine_rows": len(st["quarantine"]),
        "quarantine_by_stage": dict(sorted(qc.items())),
        "sha256": {name: _sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools/ (this file is not hashed)",
    }


def run(write: bool) -> dict:
    if write and (POOLS / "MANIFEST.json").exists():
        raise SystemExit("pools/MANIFEST.json already exists: refusing to re-freeze")
    st = admit()
    c = counts(st)
    short = shortfalls(c)
    files = _pool_files(st, c)
    man = manifest_obj(st, c, short, files)
    files["MANIFEST.json"] = _dump(man)
    if write:
        paths.write_files(POOLS, files)
    return {"counts": c, "shortfalls": short, "quarantine_rows": len(st["quarantine"]),
            "quarantine_by_stage": dict(Counter(q["stage"] for q in st["quarantine"])),
            "read_counts": st["read_counts"], "gate_used": {k: v for k, v in st["gate_used"].items() if k != "not_admitted"},
            "gate_all_not_admitted": len(st["gate_all"]["not_admitted"]),
            "g3h": st["g3_report"], "refused_registry_forms": st["refused"],
            "verify_problems": st["verify"], "read_problems": st["read_problems"], "record_problems": st["rec_problems"],
            "g3h_problems": st["g3_probs"], "load_problems": {k: len(v) for k, v in st["load_problems"].items()},
            "cross_batch_duplicates": len(st["rep"]["cross_batch_duplicates"]),
            "status": man["status"], "written": write, "files": sorted(files)}


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd not in ("check", "freeze"):
        print(__doc__)
        return 2
    out = run(write=(cmd == "freeze"))
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
