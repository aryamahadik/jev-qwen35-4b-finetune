"""families/T31/glex_admit.py: G-LEX admission of the T31 lexicon forms from the extraction answers, the quarantine of the
pieces that fail, and the pool freeze (C2_DATA_SPEC 6.2 item 2 and 6.4 steps 3-4; G0_SPEC.md section 7).

  check    in memory only: rebuild the extraction batches and check them byte for byte against the files Haiku was
           given, record the answers, admit or quarantine every form, and print the counts and every shortfall against
           the G0 targets. Nothing is written.
  freeze   the same, then write families/T31/pools/ (skins, documents, attack, wordings, lexicon, packs, QUARANTINE,
           MANIFEST) through paths.write_files. Refuses when pools/ already holds a MANIFEST.json.

Run from lean/:  ../.venv/bin/python c2_build/families/T31/glex_admit.py check|freeze

Haiku answers only flag. A form's semantic id is the registry's own declaration. A read only says which meaning it
chose from the listed meanings of the form's kind, and admission needs 2/2 independent reads to choose the declared
meaning (G-LEX). A null, an unlisted text or a different meaning counts as a disagreement. No label is set here.
G3-H is not run on pool answers (6.4: it runs at the pilot and on full generation).
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import paths  # noqa: E402
from families.T31 import extract_build as EB  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402
from families.T31 import plugin as P  # noqa: E402

F = "T31"
HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "haiku" / "extract"
POOLS = HERE / "pools"
G0 = HERE / "G0_SPEC_v1_1.md"      # the spec the pools were authored under (G0_SPEC.md is v1.2 now)

TRAIN_REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "log", "transcript")
HELD_REGISTERS = ("runbook", "export")
TRACKS = ("appr", "agent")

# G0-lite section 7 targets. Not lowered. Entries marked None have no count in G0 (the author plan's count is shown
# for reference only and is not a target).
G0_TARGETS = {
    "skins_train_per_register_track": 24,      # >= 24 per (training register, track)
    "skins_held_per_register_track": 12,       # >= 12 per (held-out register, track)
    "wordings_admitted_min": 30,               # >= 30 question wordings
    "wordings_pool_candidates": 170,           # pool target "about 170 candidates over the 9 forms"
    "packs_per_track": 30,                     # >= 30 per track (24 training + 6 S5 cards)
    "names": 300,                              # >= 300 invented full names
    "mode_f_share_max": 0.25,                  # Mode F <= 25% of rows (about 20% of the skin pool)
    "comparator_senses_admitted_min": 1,       # each of the 4 comparator senses has >= 1 admitted form
}
PLAN_REFERENCE = {                             # haiku_author.py plan: reference only, NOT G0 targets
    "bands_per_comparator_sense": HA.BANDS_PER_SEM,
    "attacks_per_track": HA.ATTACKS,
    "packs_per_track": HA.PACKS,
}


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def _meanings(reg, kind: str) -> set:
    return {s.meaning for s in reg.sems.values() if s.kind == kind}


# ------------------------------------------------------------------------------------------------ verify the reads

def _verify_reads(reg, fids: list, manifest: dict) -> tuple:
    """Rebuild each extraction batch in memory and compare it byte for byte with the files on disk (prompt, chunks,
    key, manifest): the answers must be for exactly the batch Haiku was given."""
    problems, batches = [], {}
    known = {t["batch_id"]: t["read"] for t in manifest["tasks"]}
    for read, b in EB.extraction_batches(reg, fids):
        batches[read] = b
        if known.get(b.batch_id) != read:
            problems.append(f"{read}: rebuilt batch id {b.batch_id} is not the TASKS.json batch for {read}")
        for rel, text in sorted(b.files().items()):
            p = EXTRACT / rel
            if not p.is_file():
                problems.append(f"{read}: {rel} is missing on disk")
            elif p.read_text(encoding="utf-8") != text:
                problems.append(f"{read}: {rel} differs from the rebuilt batch")
    return batches, problems


def _read_answers(batches: dict, manifest: dict) -> tuple:
    raw_by_read, sha_by_task, problems = {}, {}, []
    for read in batches:
        raw = {}
        for t in manifest["tasks"]:
            if t["read"] != read:
                continue
            ap = EXTRACT / "answers" / f"{t['task_id']}.json"
            if not ap.is_file():
                problems.append(f"{t['task_id']}: answer file missing")
                continue
            data = ap.read_bytes()
            sha_by_task[t["task_id"]] = _sha_bytes(data)
            try:
                raw[t["task_id"]] = json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                problems.append(f"{t['task_id']}: not valid JSON ({e})")
        raw_by_read[read] = raw
    return raw_by_read, sha_by_task, problems


def _record(reg, batches: dict, raw_by_read: dict) -> tuple:
    """reg.record_extraction for every answered form: the chosen meaning mapped to its sense, or None when the answer is
    null, not one of the listed meanings, or unanswered (None is a disagreement, never a default)."""
    counts, problems = {}, []
    for read, b in sorted(batches.items()):
        got, probs = CH.load_answers(b, raw_by_read.get(read, {}))
        problems += [f"{read}: {p}" for p in probs]
        c = Counter()
        for fid, a in sorted(got.items()):
            f = reg.forms[fid]
            choice = a.get("choice") if isinstance(a, dict) else None
            if choice is None:
                outcome, sem = "null", None
            elif isinstance(choice, str) and choice in _meanings(reg, f.kind):
                outcome, sem = "listed", reg.meaning_to_sem(f.kind, choice)
                if sem != f.sem_id:
                    c["listed_other_sense"] += 1
            else:
                outcome, sem = "not_listed", None
            c[outcome] += 1
            reg.record_extraction(fid, read, sem)
        c["unanswered"] = len(set(b.key.values()) - set(got))
        counts[read] = dict(c)
    return counts, problems


# ------------------------------------------------------------------------------------------------ admission

def _form_quarantine(reg) -> list:
    rows = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        st = reg.status(fid)
        if st == "admitted":
            continue
        if st == "unit_fail":
            why = "unit test: " + "; ".join(f.unit_problems[:2])
        elif st == "rejected":
            bad = [f"{e}: {'null' if s is None else s}" for e, s in f.extractions if s != f.sem_id]
            why = "a read disagrees with the declared sense: " + ", ".join(bad)
        else:
            why = f"{len(f.extractions)} of {f.required} independent reads agree (need {f.required})"
        rows.append({"piece": f"lexicon|{fid}", "kind": f.kind, "sense": f.sem_id, "stage": "G-LEX",
                     "status": st, "reason": why})
    return rows


def admit() -> dict:
    res = HA.load()
    pools, drops = res["pools"], res["drops"]
    reg = pools["lexicon"]
    manifest = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))

    q_rows, answer_problems = [], []
    for tid, iid, why in drops:
        if iid == "*":
            answer_problems.append({"task": tid, "why": why})
        else:
            q_rows.append({"piece": f"{tid}|{iid}", "stage": "load:G-SL", "reason": why})
    value_bad = EB.lint_pools(pools)
    q_rows += [{"piece": p, "stage": "value-lint", "reason": r} for p, r in value_bad]
    q_rows += [{"piece": p, "stage": "dedup", "reason": r} for p, r in EB.dedup(pools)]

    ok_fids, lex_bad = EB.lexicon_review(reg)
    batches, rebuild_problems = _verify_reads(reg, ok_fids, manifest)
    raw_by_read, answer_sha, read_problems = _read_answers(batches, manifest)
    read_counts, rec_problems = _record(reg, batches, raw_by_read)

    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    q_rows += _form_quarantine(reg)
    for sid, (sk, fid) in sorted(pools["wordings"].items()):
        if status_of[fid] != "admitted":
            q_rows.append({"piece": f"wording|{sid}", "stage": "G-LEX", "status": status_of[fid],
                           "reason": f"form {fid} is {status_of[fid]}"})

    gate = reg.gate()
    return {"pools": pools, "reg": reg, "status_of": status_of, "quarantine": q_rows, "manifest": manifest,
            "answer_problems": answer_problems, "answer_sha": answer_sha, "read_counts": read_counts,
            "batches": batches, "problems": {"rebuild": rebuild_problems, "answers": read_problems,
                                             "record": rec_problems, "answer_drops": answer_problems},
            "gate": gate, "lex_bad": lex_bad, "loader_drop_count": sum(1 for d in drops if d[1] != "*")}


# ------------------------------------------------------------------------------------------------ counts and targets

def _skin_track(sid: str) -> str:
    return sid.split("-")[1]


def counts(st: dict) -> dict:
    pools, reg, status_of = st["pools"], st["reg"], st["status_of"]
    per_rt = {}
    for sid, sk in sorted(pools["skins"].items()):
        d = per_rt.setdefault(f"{sk.register}|{_skin_track(sid)}", {"T": 0, "F": 0, "total": 0})
        d[sk.author_mode] = d.get(sk.author_mode, 0) + 1
        d["total"] += 1
    n_T = sum(v["T"] for v in per_rt.values())
    n_F = sum(v["F"] for v in per_rt.values())
    n_skins = n_T + n_F
    attacks = Counter(_skin_track(sid) for sid in pools["attacks"])
    w_cand = Counter(sk.qform for sk, _fid in pools["wordings"].values())
    w_adm = Counter(sk.qform for sid, (sk, fid) in pools["wordings"].items() if status_of[fid] == "admitted")
    bands_cand = Counter(f.sem_id for f in reg.forms.values() if f.kind == "comparator")
    bands_adm = Counter(f.sem_id for f in reg.forms.values()
                        if f.kind == "comparator" and status_of[f.form_id] == "admitted")
    return {"skins_by_register_track": per_rt, "skins_T": n_T, "skins_F": n_F, "skins_total": n_skins,
            "mode_F_share": round(n_F / n_skins, 4) if n_skins else None,
            "attacks_by_track": dict(attacks),
            "wordings_candidates": len(pools["wordings"]), "wordings_admitted": sum(w_adm.values()),
            "wordings_candidates_by_qform": dict(sorted(w_cand.items())),
            "wordings_admitted_by_qform": dict(sorted(w_adm.items())),
            "comparator_forms_candidates": sum(bands_cand.values()),
            "comparator_forms_admitted": sum(bands_adm.values()),
            "comparator_admitted_by_sense": dict(sorted(bands_adm.items())),
            "comparator_candidates_by_sense": dict(sorted(bands_cand.items())),
            "packs_appr": len(pools["packs_appr"]), "packs_agent": len(pools["packs_agent"]),
            "names": len(pools["names"]),
            "lexicon_forms": len(reg.forms), "lexicon_status": dict(Counter(status_of.values()))}


def shortfalls(c: dict) -> list:
    out = []
    for r in TRAIN_REGISTERS:
        for t in TRACKS:
            n = c["skins_by_register_track"].get(f"{r}|{t}", {}).get("total", 0)
            if n < G0_TARGETS["skins_train_per_register_track"]:
                out.append(f"skins {r}|{t}: {n} < {G0_TARGETS['skins_train_per_register_track']} (G0 7, training)")
    for r in HELD_REGISTERS:
        for t in TRACKS:
            n = c["skins_by_register_track"].get(f"{r}|{t}", {}).get("total", 0)
            if n < G0_TARGETS["skins_held_per_register_track"]:
                out.append(f"skins {r}|{t}: {n} < {G0_TARGETS['skins_held_per_register_track']} (G0 7, held-out)")
    if c["wordings_admitted"] < G0_TARGETS["wordings_admitted_min"]:
        out.append(f"wordings admitted {c['wordings_admitted']} < {G0_TARGETS['wordings_admitted_min']}")
    if c["wordings_candidates"] < G0_TARGETS["wordings_pool_candidates"]:
        out.append(f"wording candidates {c['wordings_candidates']} < about "
                   f"{G0_TARGETS['wordings_pool_candidates']} (G0 7 pool target)")
    for t, key in (("appr", "packs_appr"), ("agent", "packs_agent")):
        if c[key] < G0_TARGETS["packs_per_track"]:
            out.append(f"packs {t}: {c[key]} < {G0_TARGETS['packs_per_track']} (G0 7)")
    if c["names"] < G0_TARGETS["names"]:
        out.append(f"names {c['names']} < {G0_TARGETS['names']} (G0 7)")
    if c["mode_F_share"] is not None and c["mode_F_share"] > G0_TARGETS["mode_f_share_max"]:
        out.append(f"Mode F share {c['mode_F_share']} > {G0_TARGETS['mode_f_share_max']} (G0 7)")
    for sense in HA.COMPARATOR_SEM_MEANING:
        n = c["comparator_admitted_by_sense"].get(sense, 0)
        if n < G0_TARGETS["comparator_senses_admitted_min"]:
            out.append(f"comparator sense {sense}: {n} admitted < 1 (G0 7 needs every sense)")
    return out


# ------------------------------------------------------------------------------------------------ freeze

def _skin_obj(sk, track: str) -> dict:
    d = dataclasses.asdict(sk) if dataclasses.is_dataclass(sk) else dict(vars(sk))
    d["track"] = track
    return d


def _files(st: dict, c: dict, short: list) -> dict:
    pools, reg, status_of = st["pools"], st["reg"], st["status_of"]
    skins_T = [_skin_obj(sk, _skin_track(sid)) for sid, sk in sorted(pools["skins"].items())
               if sk.author_mode == "T"]
    docs_F = [_skin_obj(sk, _skin_track(sid)) for sid, sk in sorted(pools["skins"].items())
              if sk.author_mode == "F"]
    attacks = [_skin_obj(sk, _skin_track(sid)) for sid, sk in sorted(pools["attacks"].items())]
    wordings = []
    for sid, (sk, fid) in sorted(pools["wordings"].items()):
        if status_of[fid] != "admitted":
            continue
        d = _skin_obj(sk, _skin_track(sid))
        d["form_id"] = fid
        d["sense"] = reg.forms[fid].sem_id
        wordings.append(d)
    lex = reg.to_json()
    for f in lex["forms"]:
        f["usable"] = f["status"] == "admitted"
    packs = {"appr": pools["packs_appr"], "agent": pools["packs_agent"], "names": pools["names"],
             "s5_split": "not assigned at freeze (6 per track are reserved for S5 by G0 section 7)"}
    quarantine = {"family": F, "rows": st["quarantine"]}
    out = {
        "skins.json": _dump({"family": F, "mode": "T", "count": len(skins_T), "skins": skins_T}),
        "documents.json": _dump({"family": F, "mode": "F", "count": len(docs_F), "documents": docs_F}),
        "attack.json": _dump({"family": F, "count": len(attacks), "attacks": attacks}),
        "wordings.json": _dump({"family": F, "count": len(wordings), "wordings": wordings}),
        "lexicon.json": _dump(lex),
        "packs.json": _dump({"family": F, **packs}),
        "QUARANTINE.json": _dump(quarantine),
    }
    return out


def manifest_obj(st: dict, c: dict, short: list, files: dict) -> dict:
    g0_sha = _sha_bytes(G0.read_bytes())
    gate = st["gate"]
    return {
        "family": F,
        "version": "freeze-v1",
        "status": ("PARTIAL: frozen with shortfalls and quarantines (see shortfalls); NOT for row generation until "
                   "G13-seed (6.4 step 4) runs on these pools")
        if short or not gate["pass"] else
        "FROZEN for G13-seed: every G0 target met and G-LEX passes; G13-seed still pending",
        "g0": {"path": "families/T31/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": g0_sha == P.POOL_G0_SHA256},
        "reads": {read: {"batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "tasks": {tid: st["answer_sha"][tid] for tid in sorted(st["answer_sha"])
                                   if tid.startswith(b.batch_id)}}
                  for read, b in sorted(st["batches"].items())},
        "answer_reads": st["read_counts"],
        "problems": st["problems"],
        "gates": {"G-LEX": {k: v for k, v in gate.items() if k != "not_admitted"},
                  "G-LEX_not_admitted_count": len(gate["not_admitted"]),
                  "G13_seed": "not run (6.4 step 4; needs the decontamination program, not run in this step)",
                  "G3-H": "not run at pool stage (6.4: pilot and full generation only)"},
        "counts": c,
        "targets_g0": G0_TARGETS,
        "plan_reference_not_g0": PLAN_REFERENCE,
        "shortfalls": short,
        "skins_by_register": {r: sum(v["total"] for k, v in c["skins_by_register_track"].items()
                                     if k.split("|")[0] == r) for r in sorted({k.split("|")[0]
                                                                              for k in c["skins_by_register_track"]})},
        "sha256": {name: _sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools/ (this file is not hashed)",
    }


def run(write: bool) -> dict:
    if write and (POOLS / "MANIFEST.json").exists():
        raise SystemExit("pools/MANIFEST.json already exists: refusing to re-freeze")
    st = admit()
    c = counts(st)
    short = shortfalls(c)
    files = _files(st, c, short)
    man = manifest_obj(st, c, short, files)
    files["MANIFEST.json"] = _dump(man)
    if write:
        paths.write_files(POOLS, files)
    return {"counts": c, "shortfalls": short, "quarantine_rows": len(st["quarantine"]),
            "quarantine_by_stage": dict(Counter(q["stage"] for q in st["quarantine"])),
            "gate": {k: v for k, v in st["gate"].items() if k != "not_admitted"},
            "problems": st["problems"], "read_counts": st["read_counts"], "status": man["status"],
            "written": write, "files": sorted(files)}


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
