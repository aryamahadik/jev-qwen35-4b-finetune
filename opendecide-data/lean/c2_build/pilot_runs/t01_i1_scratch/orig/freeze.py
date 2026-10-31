"""families/T01/freeze.py: record the T01 extraction reads, admit forms by G-LEX, quarantine what fails, and freeze the
pools with a manifest (C2_DATA_SPEC 6.4; G0_SPEC 2, 6, 7; PREREG A37 (b) and A38).

Nothing here calls a model. Every input was written by the earlier rounds:
  - the authoring pieces and their family checks (extract.collect), the G-SL pass (extract.lint_all), dedup
    (extract.dedup_all);
  - the registry and the read batches (extract.build_registry, extract.make_tasks), rebuilt in memory and checked
    against key/ and pool/lexicon_registry.json on disk;
  - the answers answers/<task_id>.json: G-LEX reads glex-r1, glex-r2 (every form) and glex-r3 (window forms), and the
    G3-H read g3h-r1 (documents).

Steps:
  1. rebuild the batches; check their keys and the registry against the files on disk;
  2. record each G-LEX read with reg.record_extraction; the sem is the sem of the meaning the reader chose (a meaning
     that is not one of the kind's choices records None and rejects the form);
  3. admit by reg.status: admitted = every read agrees (2/2; 3/3 for window). Rejected, unit_fail and pending forms
     are quarantined. G3-H: a document is admitted only after g3h.compare passes its read; with no g3h answer on
     disk, the documents stay pending and nothing is compared;
  4. write pools/ (packs, skins, documents_pending_g3h, wordings, windows, comparators, the registry with its reads,
     quarantine.jsonl with one reason per piece not admitted) and manifest.json (sha256s, counts, G0 targets,
     shortfalls, gate results).

  ../.venv/bin/python -m families.T01.freeze            (from lean/c2_build: dry run, prints counts, writes nothing)
  ../.venv/bin/python -m families.T01.freeze --write    (after A38: writes families/T01/pools/)
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

from c2_kit import chunker, paths  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
POOLS = HERE / "pools"
ANS_ROOT = E.ROOT
C2_SPEC = paths.LEAN / "teach1" / "C2_DATA_SPEC.md"
C2_SPEC_SHA_A37 = "245ba9f9d6a7132d3a6604bf912bca05bbaeca3aa1daa640e28436303c38d74f"
G0_SPEC = HERE / "G0_SPEC.md"
GROUPS = ("packs", "skins", "freeform", "wordings", "windows", "comparators")

# G0 targets, as written in G0_SPEC.md (sections 1.1, 2, 7). Never lowered here.
TRAIN_REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "log", "transcript")
HELD_REGISTERS = ("faq", "letter")
TARGET = {
    "packs": 80, "packs_held_out": 16,
    "skins_per_training_register": 56, "skins_per_held_register": 28,
    "documents": 120,
    "wordings_min_admitted": 30, "wordings_asked": 287,
    "windows_per_sem": 14, "comparators_per_sem": 12,
}
WINDOW_SEMS = ("win.rolling_cap", "win.later_anchor", "win.wait_after")
COMPARATOR_SEMS = ("cmp.gt", "cmp.ge")
PER_FORM_ASKED = {"yes_no_base": 12, "choice": 14, "complement": 9}


def qform_class(q) -> str:
    if q.qtype == "choice":
        return "choice"
    if q.polarity == -1:
        return "complement"
    return "yes_no_base"


def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ 1. rebuild + check

def rebuild() -> dict:
    pieces, authored, check_drops = E.collect()
    surv, lint_drops, clause_flags = E.lint_all(pieces)
    surv, dup_drops = E.dedup_all(surv)
    lex_rows = surv["wordings"] + surv["windows"] + surv["comparators"]
    reg, row_of, form_drops = E.build_registry(lex_rows)
    batches, task_counts = E.make_tasks(reg, surv["freeform"])
    return {"authored": authored, "check_drops": check_drops, "surv": surv, "lint_drops": lint_drops,
            "clause_flags": clause_flags, "dup_drops": dup_drops, "reg": reg, "row_of": row_of,
            "form_drops": form_drops, "batches": batches, "task_counts": task_counts}


def check_inputs(rb) -> dict:
    problems, keys = [], {}
    pool_reg = json.loads((ANS_ROOT / "pool" / "lexicon_registry.json").read_text(encoding="utf-8"))
    reg_match = pool_reg == rb["reg"].to_json()
    if not reg_match:
        problems.append("rebuilt registry differs from pool/lexicon_registry.json")
    for read, kind, b in rb["batches"]:
        kf = ANS_ROOT / "key" / f"{b.batch_id}.json"
        raw = json.loads(kf.read_text(encoding="utf-8")) if kf.exists() else None
        wrapped = isinstance(raw, dict) and "key" in raw and "batch_id" in raw
        disk = raw["key"] if wrapped else raw
        bid_ok = (raw["batch_id"] == b.batch_id) if wrapped else True
        ok = disk is not None and disk == b.key and bid_ok
        keys[b.batch_id] = {"read": read, "kind": kind, "items": len(b.key), "key_file_matches": ok,
                            "key_file_sha256": _sha_file(kf) if kf.exists() else None}
        if not ok:
            problems.append(f"key file mismatch: {b.batch_id}")
    return {"registry_matches_pool": reg_match, "keys": keys, "problems": problems}


# ------------------------------------------------------------------------------------------------ 2. record the reads

def read_answers(b) -> tuple:
    """(answers {internal id: object}, problems, tasks present, tasks missing) for the answer files on disk."""
    raw, present, missing = {}, [], []
    for c in b.chunks:
        tid = c["task_id"]
        af = ANS_ROOT / b.answer_path(tid)
        if af.exists():
            raw[tid] = json.loads(af.read_text(encoding="utf-8"))
            present.append(tid)
        else:
            missing.append(tid)
    got, probs = chunker.load_answers(b, raw) if raw else ({}, [])
    return got, probs, present, missing


def record_reads(rb) -> dict:
    reg = rb["reg"]
    rec = {"lex_reads": {}, "disagreements": [], "problems": [], "g3h": {}}
    for read, kind, b in rb["batches"]:
        if kind == "extract_g3h":
            _got, probs, present, missing = read_answers(b)
            rec["g3h"] = {"batch_id": b.batch_id, "read": read, "tasks": len(b.chunks), "items": len(b.key),
                          "answer_tasks_present": len(present), "answer_tasks_missing": missing,
                          "compared": False}
            continue
        got, probs, present, missing = read_answers(b)
        rec["lex_reads"][read] = {"batch_id": b.batch_id, "tasks": len(b.chunks), "items": len(b.key),
                                  "answer_tasks_present": len(present), "answers": len(got),
                                  "answer_tasks_missing": missing}
        rec["problems"] += [f"{read}: {p}" for p in probs]
        for fid, a in sorted(got.items()):
            meaning = a.get("meaning") if isinstance(a, dict) else None
            sem = reg.meaning_to_sem(reg.forms[fid].kind, meaning) if isinstance(meaning, str) else None
            reg.record_extraction(fid, read, sem)
            if sem != reg.forms[fid].sem_id:
                rec["disagreements"].append({"form_id": fid, "read": read, "expected_sem": reg.forms[fid].sem_id,
                                             "meaning_read": meaning, "sem_read": sem})
    return rec


def admission(rb) -> dict:
    reg = rb["reg"]
    status = {fid: reg.status(fid) for fid in reg.forms}
    admitted = sorted(f for f, s in status.items() if s == "admitted")
    not_admitted = {f: s for f, s in status.items() if s != "admitted"}
    g_used = reg.gate(used_form_ids=admitted)
    g_all = reg.gate()
    return {"status": status, "admitted": admitted, "not_admitted": not_admitted,
            "gate_used_forms": {k: g_used[k] for k in ("gate", "n_forms", "status_counts", "pass")},
            "gate_all_forms": {k: g_all[k] for k in ("gate", "n_forms", "status_counts", "pass")}}


# ------------------------------------------------------------------------------------------------ 3-4. pools

def lex_row(fid, rb, reg_status) -> dict:
    f = rb["reg"].forms[fid]
    row = E._pool_row(rb["row_of"][fid])
    row.update({"form_id": fid, "sem_id": f.sem_id, "kind": f.kind,
                "g_lex": {"status": reg_status, "required": f.required,
                          "reads": [[e, s] for e, s in f.extractions]}})
    return row


def build(rb, rec, adm) -> dict:
    reg, row_of, surv, authored = rb["reg"], rb["row_of"], rb["surv"], rb["authored"]
    problems = []
    admitted = sorted(adm["admitted"], key=lambda f: (row_of[f]["group"], row_of[f]["pid"]))
    pools = {
        "packs": [E._pool_row(p) for p in surv["packs"]],
        "skins": [E._pool_row(p) for p in surv["skins"]],
        "documents_pending_g3h": [dict(E._pool_row(p), status="pending_g3h") for p in surv["freeform"]],
        "wordings": [], "windows": [], "comparators": [],
    }
    for fid in admitted:
        pools[row_of[fid]["group"]].append(lex_row(fid, rb, "admitted"))

    quar = []
    for g in GROUPS:
        for d in rb["check_drops"].get(g, []):
            quar.append({"stage": "authoring_check", **d})
    for d in rb["lint_drops"]:
        quar.append({"stage": "lint_gsl", **d})
    for d in rb["dup_drops"]:
        quar.append({"stage": "dedup", **d})
    for d in rb["form_drops"]:
        quar.append({"stage": "lexicon_form", **d})
    dis = defaultdict(list)
    for x in rec["disagreements"]:
        dis[x["form_id"]].append(f"{x['read']} read the meaning {x['meaning_read']!r} "
                                 f"(sem {x['sem_read']}); the form's sem is {x['expected_sem']}")
    for fid in sorted(adm["not_admitted"], key=lambda f: (row_of[f]["group"], row_of[f]["pid"])):
        p, s = row_of[fid], adm["not_admitted"][fid]
        reasons = dis.get(fid) or [f"G-LEX status {s}"]
        if s == "unit_fail":
            reasons = [f"unit test: {x}" for x in reg.forms[fid].unit_problems[:3]]
        quar.append({"stage": "G-LEX", "group": p["group"], "pid": p["pid"], "task_id": p["task_id"],
                     "form_id": fid, "sem_id": reg.forms[fid].sem_id, "status": s, "reasons": reasons})

    quar_by = Counter(q["group"] for q in quar)
    counts = {}
    for g in GROUPS:
        n_auth = authored[g]
        if g == "freeform":
            adm_n, pend_n = 0, len(surv["freeform"])
        else:
            adm_n, pend_n = len(pools[g]), 0
        q_n = quar_by.get(g, 0)
        if n_auth != adm_n + pend_n + q_n:
            problems.append(f"{g}: authored {n_auth} != admitted {adm_n} + pending {pend_n} + quarantined {q_n}")
        counts[g] = {"authored": n_auth, "admitted": adm_n, "pending": pend_n, "quarantined": q_n}

    qforms = P.T01().QFORMS
    form_target = {q: PER_FORM_ASKED[qform_class(v)] for q, v in qforms.items()}
    if sum(form_target.values()) != TARGET["wordings_asked"]:
        problems.append(f"per-form wording targets sum to {sum(form_target.values())}, not 287")

    packs = pools["packs"]
    pack_ho = Counter(bool(r["held_out"]) for r in packs)
    skin_reg = Counter((r["register"], bool(r["held_out"])) for r in pools["skins"])
    doc_reg = Counter(r["register"] for r in pools["documents_pending_g3h"])
    wording_form = Counter(r["qform"] for r in pools["wordings"])
    win_sem = Counter(r["sem"] for r in pools["windows"])
    cmp_sem = Counter(r["sem"] for r in pools["comparators"])

    short = []

    def add(name, have, want):
        if have < want:
            short.append(f"{name}: {have} of {want} (short {want - have})")

    add("packs total", len(packs), TARGET["packs"])
    add("packs held out", pack_ho[True], TARGET["packs_held_out"])
    add("packs training", pack_ho[False], TARGET["packs"] - TARGET["packs_held_out"])
    for r_ in TRAIN_REGISTERS:
        add(f"skins {r_} (training)", skin_reg[(r_, False)], TARGET["skins_per_training_register"])
    for r_ in HELD_REGISTERS:
        add(f"skins {r_} (held out)", skin_reg[(r_, True)], TARGET["skins_per_held_register"])
    add("skins total", len(pools["skins"]),
        TARGET["skins_per_training_register"] * len(TRAIN_REGISTERS)
        + TARGET["skins_per_held_register"] * len(HELD_REGISTERS))
    add("documents admitted (G3-H)", 0, TARGET["documents"])
    for q in sorted(form_target):
        add(f"wording {q}", wording_form[q], form_target[q])
    add("wordings admitted (minimum)", len(pools["wordings"]), TARGET["wordings_min_admitted"])
    for s_ in WINDOW_SEMS:
        add(f"window {s_}", win_sem[s_], TARGET["windows_per_sem"])
    for s_ in COMPARATOR_SEMS:
        add(f"comparator {s_}", cmp_sem[s_], TARGET["comparators_per_sem"])

    flags = [{"pid": f["pid"], "sem": f["sem"], "flags": f["flags"]} for f in rb["clause_flags"]]
    return {"pools": pools, "quar": quar, "counts": counts, "problems": problems,
            "breakdown": {
                "packs_held_out": {"True": pack_ho[True], "False": pack_ho[False]},
                "skins_by_register": {f"{r}|held_out={h}": n for (r, h), n in sorted(skin_reg.items())},
                "documents_pending_by_register": dict(sorted(doc_reg.items())),
                "wordings_by_qform": {q: {"admitted": wording_form[q], "target": form_target[q]}
                                      for q in sorted(form_target)},
                "wordings_by_class": {c: sum(v for q, v in wording_form.items() if qform_class(qforms[q]) == c)
                                      for c in PER_FORM_ASKED},
                "windows_by_sem": {s: win_sem[s] for s in WINDOW_SEMS},
                "comparators_by_sem": {s: cmp_sem[s] for s in COMPARATOR_SEMS},
                "gsl_clause_flags_admitted": flags,
            },
            "shortfalls": short}


# ------------------------------------------------------------------------------------------------ write

def write_all(rb, rec, adm, out) -> dict:
    reg = rb["reg"]
    p = out["pools"]
    written = {
        "packs.jsonl": paths.write_jsonl(POOLS / "packs.jsonl", p["packs"]),
        "skins.jsonl": paths.write_jsonl(POOLS / "skins.jsonl", p["skins"]),
        "documents_pending_g3h.jsonl": paths.write_jsonl(POOLS / "documents_pending_g3h.jsonl",
                                                         p["documents_pending_g3h"]),
        "wordings.jsonl": paths.write_jsonl(POOLS / "wordings.jsonl", p["wordings"]),
        "windows.jsonl": paths.write_jsonl(POOLS / "windows.jsonl", p["windows"]),
        "comparators.jsonl": paths.write_jsonl(POOLS / "comparators.jsonl", p["comparators"]),
        "lexicon_registry.json": paths.write_json(POOLS / "lexicon_registry.json", reg.to_json()),
        "quarantine.jsonl": paths.write_jsonl(POOLS / "quarantine.jsonl", out["quar"]),
    }
    files = {}
    for name, path in written.items():
        raw = path.read_bytes()
        files[name] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        if name.endswith(".jsonl"):
            files[name]["rows"] = len([x for x in raw.decode("utf-8").split("\n") if x])
    return files


def manifest(rb, rec, adm, out, files, ck) -> dict:
    """ck: check_inputs(rb) from before the reads were recorded (the registry then still equals the pool on disk)."""
    lex_answers = {}
    for read, kind, b in rb["batches"]:
        if kind != "extract_lex":
            continue
        for c in b.chunks:
            af = ANS_ROOT / b.answer_path(c["task_id"])
            if af.exists():
                lex_answers[c["task_id"]] = _sha_file(af)
    g3_missing = rec["g3h"].get("answer_tasks_missing", [])
    pending_docs = len(out["pools"]["documents_pending_g3h"])
    return {
        "family": FAMILY,
        "freeze": "v1",
        "status": "partial",
        "partial_because": (f"documents: {len(g3_missing)} of {rec['g3h'].get('tasks', 0)} g3h-r1 reads not returned; "
                            f"{pending_docs} documents pending, none admitted") if g3_missing else None,
        "bindings": {
            "prereg_final_sha256": _sha_file(paths.PREREG),
            "a38_frozen": paths.a38_frozen(),
            "c2_data_spec_sha256": _sha_file(C2_SPEC) if C2_SPEC.exists() else None,
            "c2_data_spec_sha256_a37": C2_SPEC_SHA_A37,
            "c2_data_spec_matches_a37": (_sha_file(C2_SPEC) == C2_SPEC_SHA_A37) if C2_SPEC.exists() else None,
            "g0_spec_sha256": _sha_file(G0_SPEC),
            "g0_spec_sha256_plugin": getattr(P.T01, "G0_SHA256", None),
            "g0_spec_matches_plugin": _sha_file(G0_SPEC) == getattr(P.T01, "G0_SHA256", None),
        },
        "inputs": {
            "lex_answers_present": len(lex_answers),
            "lex_answers_expected": sum(len(b.chunks) for _r, k, b in rb["batches"] if k == "extract_lex"),
            "lex_answer_sha256": lex_answers,
            "g3h_answers_present": rec["g3h"].get("answer_tasks_present", 0),
            "g3h_answers_expected": rec["g3h"].get("tasks", 0),
            "g3h_answer_tasks_missing": g3_missing,
            "key_files": {k: v["key_file_sha256"] for k, v in ck["keys"].items()},
            "registry_matches_pool_on_disk": ck["registry_matches_pool"],
            "tasks_json_sha256": _sha_file(ANS_ROOT / "TASKS.json"),
            "lint_log_sha256": _sha_file(ANS_ROOT / "lint_log.json"),
            "code_sha256": {"extract.py": _sha_file(HERE / "extract.py"), "plugin.py": _sha_file(HERE / "plugin.py"),
                            "freeze.py": _sha_file(HERE / "freeze.py")},
        },
        "targets_g0": TARGET | {"wordings_per_qform": PER_FORM_ASKED,
                                "window_sems": list(WINDOW_SEMS), "comparator_sems": list(COMPARATOR_SEMS)},
        "counts": out["counts"],
        "breakdown": out["breakdown"],
        "shortfalls_vs_g0": out["shortfalls"],
        "gate_g_lex": adm["gate_used_forms"],
        "gate_g_lex_all_forms": adm["gate_all_forms"],
        "lex_reads": rec["lex_reads"],
        "g3h": rec["g3h"],
        "g_lex_disagreements": rec["disagreements"],
        "problems": ck["problems"] + rec["problems"] + out["problems"],
        "files": files,
    }


def run(write: bool) -> dict:
    rb = rebuild()
    ck = check_inputs(rb)
    rec = record_reads(rb)
    adm = admission(rb)
    out = build(rb, rec, adm)
    res = {"checks": {"registry_matches_pool": ck["registry_matches_pool"], "keys": {k: v["key_file_matches"]
                                                                                    for k, v in ck["keys"].items()},
                      "problems": ck["problems"] + rec["problems"] + out["problems"]},
           "counts": out["counts"], "shortfalls_vs_g0": out["shortfalls"],
           "gate_g_lex": adm["gate_used_forms"], "gate_g_lex_all_forms": adm["gate_all_forms"],
           "g3h": rec["g3h"], "g_lex_disagreements": rec["disagreements"],
           "quarantine_by_stage": dict(Counter(q["stage"] for q in out["quar"])),
           "breakdown": out["breakdown"], "written": write}
    if write:
        files = write_all(rb, rec, adm, out)
        man = manifest(rb, rec, adm, out, files, ck)
        paths.write_json(POOLS / "manifest.json", man)
        res["files"] = files
        res["manifest"] = str(POOLS / "manifest.json")
    return res


def main(argv: list) -> int:
    res = run("--write" in argv)
    print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
