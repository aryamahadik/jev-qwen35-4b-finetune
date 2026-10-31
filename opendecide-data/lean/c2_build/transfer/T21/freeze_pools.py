"""transfer/T21/freeze_pools.py: the T21 G-LEX and G3-H stage after the Haiku extraction answers, then the freeze of the
family's pools. Written after A38 (PREREG_FINAL "Ruling A38"). Every write goes through paths.write_text, which refuses
before the freeze and on never-open paths. No rows are generated here: T21 rows come later, from the frozen pools.

  check   read-only: rebuild the extraction batches, check them against the files on disk and TASKS.json, load and
          record the answer files, run G-LEX (2/2) and G3-H, and print the report (writes nothing)
  freeze  the same, then write pools/ (packs, skins, freeform, attacks, wordings, lexicon, quarantine, extraction
          record) and pools/manifest.json (sha256s, counts per kind and register, admitted vs G0-lite target)

  ../.venv/bin/python c2_build/transfer/T21/freeze_pools.py check    (from lean/)
  ../.venv/bin/python c2_build/transfer/T21/freeze_pools.py freeze   (from lean/)

Haiku never sets a label: a G-LEX answer names a meaning (lexicon.meaning_to_sem maps it to a sem id), and a
disagreement rejects the form. G3-H compares the extracted claimant and agreement with the generator's facts; a
mismatched narrative is dropped. T21 is transfer dev only: nothing here feeds training.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from transfer.T21 import extract_build as EB  # noqa: E402
from transfer.T21 import haiku_author as HA  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402

FAMILY = "T21"
EXTRACT = EB.EXTRACT
POOLS = HERE / "pools"
G0 = HERE / "G0_SPEC.md"
PL = P.T21Plugin

# G0-lite targets (G0_SPEC.md sections 2 and 6; equal to the author-stage constants). Never lowered.
TARGET = {
    "packs": {"total": 40, "train": 32, "held_out": 8},
    "skins_train_per_register": 12,
    "skins_held_per_register": 16,
    "freeform_per_train_register": 5,
    "attacks": 30,
    "wordings": {"yn_capped": 30, "ch_clause": 26, "yn_uncapped": 14, "yn_not_capped": 14, "yn_free_of": 14},
}
TRAIN_REG = tuple(r for r in PL.REGISTERS if r not in PL.HELD_OUT_REGISTERS)
HELD_REG = tuple(PL.HELD_OUT_REGISTERS)
QFORM_OF_SEM = {question_sem(FAMILY, q): q for q in TARGET["wordings"]}


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check_targets() -> list:
    """The G0 numbers must equal the author-stage constants and the pinned G0 hash (no target is lowered)."""
    t, probs = TARGET, []
    if (HA.N_PACKS, HA.N_PACKS_HELD) != (t["packs"]["total"], t["packs"]["held_out"]):
        probs.append("target: pack counts differ from haiku_author")
    if (HA.N_SKIN_TRAIN, HA.N_SKIN_HELD) != (t["skins_train_per_register"], t["skins_held_per_register"]):
        probs.append("target: skin counts differ from haiku_author")
    if HA.N_FREEFORM != t["freeform_per_train_register"]:
        probs.append("target: freeform count differs from haiku_author")
    if HA.N_ATTACK != t["attacks"]:
        probs.append("target: attack count differs from haiku_author")
    if HA.WORDING_PLAN != t["wordings"]:
        probs.append("target: wording plan differs from haiku_author")
    if (len(TRAIN_REG), len(HELD_REG)) != (8, 2):
        probs.append(f"target: registers {len(TRAIN_REG)} train / {len(HELD_REG)} held (expected 8 / 2)")
    if _sha_file(G0) != PL.G0_SHA256:
        probs.append("target: G0_SPEC.md sha256 differs from the pinned value")
    return probs


def verify_build(res) -> tuple:
    """Every rebuilt extraction file must equal the file on disk (what the Haiku agents read), and each task's sha256
    must equal TASKS.json."""
    probs = []
    for rel, text in sorted(res["files"].items()):
        f = EXTRACT / rel
        if not f.is_file():
            probs.append(f"build: missing on disk {rel}")
        elif f.read_text(encoding="utf-8") != text:
            probs.append(f"build: differs from disk {rel}")
    tj = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    for t in tj["tasks"]:
        rel = "tasks/" + Path(t["task_file"]).name
        if _sha_text(res["files"].get(rel, "")) != t["task_sha256"]:
            probs.append(f"build: task sha differs from TASKS.json {t['task_id']}")
    return probs, len(res["files"]), len(tj["tasks"])


def load_raw(batch) -> tuple:
    raw, probs = {}, []
    for c in batch.chunks:
        tid = c["task_id"]
        f = EXTRACT / batch.answer_path(tid)
        if not f.is_file():
            probs.append(f"{tid}: no answer file")
            continue
        try:
            raw[tid] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{tid}: answer is not JSON ({e})")
    return raw, probs


def record_lex(res) -> tuple:
    """Two independent reads per question form. A form with no valid answer gets no extraction (it stays pending)."""
    reg, rows, probs = res["reg"], [], []
    for g in res["glex"]:
        b, ext = g["batch"], g["extractor_id"]
        raw, p1 = load_raw(b)
        ans, p2 = chunker.load_answers(b, raw)
        probs += [f"{ext}: {x}" for x in p1 + p2]
        for fid in g["form_ids"]:
            a = ans.get(fid)
            meaning = a.get("meaning") if isinstance(a, dict) and set(a) == {"meaning"} else None
            if not isinstance(meaning, str):
                rows.append({"form_id": fid, "extractor_id": ext, "meaning": None, "sem_id": None,
                             "note": "no valid answer"})
                continue
            sem = reg.meaning_to_sem("question", meaning)
            reg.record_extraction(fid, ext, sem)
            rows.append({"form_id": fid, "extractor_id": ext, "meaning": meaning, "sem_id": sem, "note": ""})
    return rows, probs


def g3h_stage(res) -> tuple:
    """One read of every Mode F narrative. The template is the narrative's skin (one narrative per template)."""
    b = res["g3"]
    raw, p1 = load_raw(b)
    ans, p2 = chunker.load_answers(b, raw)
    fields = EB.g3h_fields()
    detail, results = {}, []
    for iid in sorted(res["g3h_expected"]):
        sid = iid.split("|", 1)[1]
        a = ans.get(iid)
        if a is None:
            ok, diffs = False, ["no extraction"]
        else:
            ok, diffs = g3h.compare(res["g3h_expected"][iid], a, fields)
        detail[sid] = {"ok": ok, "diffs": diffs}
        results.append((sid, sid, ok))
    return g3h.template_report(results), detail, p1 + p2


def tally(packs, skins, freeform, attacks, wordings) -> list:
    lines = []

    def line(kind, label, target, admitted):
        lines.append({"kind": kind, "label": label, "target": target, "admitted": admitted,
                      "shortfall": max(0, target - admitted), "surplus": max(0, admitted - target)})

    line("packs", "total", TARGET["packs"]["total"], len(packs))
    line("packs", "train", TARGET["packs"]["train"], sum(1 for p in packs if not p["held_out"]))
    line("packs", "held_out", TARGET["packs"]["held_out"], sum(1 for p in packs if p["held_out"]))
    for r in TRAIN_REG:
        line("skins_T", r, TARGET["skins_train_per_register"],
             sum(1 for s in skins if s.register == r and not s.held_out))
    for r in HELD_REG:
        line("skins_T", r, TARGET["skins_held_per_register"],
             sum(1 for s in skins if s.register == r and s.held_out))
    for r in TRAIN_REG:
        line("freeform_F", r, TARGET["freeform_per_train_register"], sum(1 for s in freeform if s.register == r))
    line("attacks", "total", TARGET["attacks"], len(attacks))
    for q, n in TARGET["wordings"].items():
        line("wordings", q, n, sum(1 for w in wordings if w["qform"] == q))
    return lines


def quarantine_log(res, glex, g3_detail) -> list:
    q = []
    for pool, items in res["lint"]["drops"].items():
        for d in items:
            q.append({"stage": "lint", "pool": pool, "id": d["id"], "reasons": d["reasons"]})
    for d in res["admit_drops"]:
        q.append({"stage": "admit", "pool": "wordings", "id": d["tid"], "qform": d["qform"], "reasons": d["reasons"]})
    for d in res["lint"]["cross_pool_dups"]:
        q.append({"stage": "dedup", "pool": d["pool"], "id": d["id"], "same_as": d["same_as"]})
    for fid, r in sorted(glex.items()):
        if r["status"] != "admitted":
            q.append({"stage": "G-LEX", "pool": "wordings", "id": fid, "qform": r["qform"], "text": r["text"],
                      "status": r["status"], "extractions": r["extractions"]})
    for sid, d in sorted(g3_detail.items()):
        if not d["ok"]:
            q.append({"stage": "G3-H", "pool": "freeform", "id": sid, "reasons": d["diffs"]})
    return q


def run(write: bool) -> dict:
    probs = check_targets()
    res = EB.build_all()
    b_probs, n_files, n_tasks = verify_build(res)
    probs += b_probs
    reg, lint = res["reg"], res["lint"]

    lex_rows, lp = record_lex(res)
    probs += lp
    glex = {}
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        glex[fid] = {"qform": QFORM_OF_SEM.get(f.sem_id), "text": f.text, "sem_id": f.sem_id,
                     "status": reg.status(fid), "unit_ok": f.unit_ok,
                     "extractions": [list(e) for e in f.extractions],
                     "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha}

    g3_rep, g3_detail, gp = g3h_stage(res)
    probs += gp
    g3_drop = set(g3_rep["drop_rows"])

    packs = sorted(lint["packs"], key=lambda p: p["pack_id"])
    skins = [lint["skins"][k] for k in sorted(lint["skins"])]
    freeform = [lint["free"][k] for k in sorted(lint["free"]) if k not in g3_drop]
    attacks = [lint["attacks"][k] for k in sorted(lint["attacks"])]
    admitted = [fid for fid in sorted(glex) if glex[fid]["status"] == "admitted"]
    wordings = [{"form_id": fid, "qform": glex[fid]["qform"], "text": glex[fid]["text"],
                 "sem_id": glex[fid]["sem_id"], "haiku_task_id": glex[fid]["haiku_task_id"],
                 "haiku_prompt_sha": glex[fid]["haiku_prompt_sha"], "extractions": glex[fid]["extractions"]}
                for fid in admitted]

    lines = tally(packs, skins, freeform, attacks, wordings)
    quarantine = quarantine_log(res, glex, g3_detail)
    per_pool = EB.summary(res)["per_pool"]
    counts = {
        "per_pool_lint": per_pool,
        "skins_T_kept_by_register": dict(sorted(collections.Counter(
            f"{s.register}|{'held' if s.held_out else 'train'}" for s in skins).items())),
        "freeform_F_kept_after_g3h_by_register": dict(sorted(collections.Counter(
            s.register for s in freeform).items())),
        "freeform_F_g3h_drops": len(g3_drop),
        "g3h_rate": {"items": len(g3_detail), "ok": sum(1 for d in g3_detail.values() if d["ok"])},
        "wordings_forms_for_glex": len(glex),
        "wordings_admitted": len(admitted),
        "wordings_not_admitted": len(glex) - len(admitted),
        "wordings_admitted_by_qform": dict(sorted(collections.Counter(w["qform"] for w in wordings).items())),
        "lexicon_sems": len(reg.sems),
        "lex_extractions_recorded": sum(1 for r in lex_rows if r["note"] == ""),
        "lex_extractions_rejected_as_wrong_choice": sum(1 for r in lex_rows if r["note"] == "" and r["sem_id"] is None),
    }
    summary = {"tally": lines, "shortfalls": [x for x in lines if x["shortfall"]], "counts": counts,
               "problems": probs, "build": {"files_checked": n_files, "tasks": n_tasks}}

    if not write:
        return {"summary": summary, "problems": probs, "wrote": []}
    if probs:
        return {"summary": summary, "problems": probs, "wrote": [], "refused": "problems above; nothing written"}
    if POOLS.exists() and any(POOLS.iterdir()):
        return {"summary": summary, "problems": ["pools/ already holds files; a freeze is written once"], "wrote": []}

    pools = {
        "packs.json": packs,
        "skins.json": [asdict(s) for s in skins],
        "freeform.json": [asdict(s) for s in freeform],
        "attacks.json": [asdict(s) for s in attacks],
        "wordings.json": wordings,
        "lexicon.json": reg.to_json(),
        "quarantine.json": quarantine,
        "extraction_record.json": {"lex_reads": lex_rows, "g3h": g3_detail,
                                   "g3h_report": {k: g3_rep[k] for k in ("gate", "bar", "quarantined",
                                                                         "all_templates_pass")}},
    }
    info, wrote = {}, []
    for name, obj in pools.items():
        text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
        paths.write_text(POOLS / name, text)
        info[name] = {"sha256": _sha_text(text), "bytes": len(text.encode("utf-8"))}
        wrote.append(str(POOLS / name))

    tasks = {}
    for t in res["tasks"]:
        ans = Path(t["answer_file"])
        tasks[t["task_id"]] = {"batch_id": t["batch_id"], "kind": t["kind"], "n_items": t["n_items"],
                               "task_sha256": t["task_sha256"],
                               "answer_sha256": _sha_file(ans) if ans.is_file() else None}
    manifest = {
        "family": FAMILY, "stage": "G-LEX 2/2 + G3-H + pool freeze (A37, A38)", "transfer_dev_only": True,
        "trained": False, "rows_generated": False,
        "g0_lite": {"path": "c2_build/transfer/T21/G0_SPEC.md", "sha256": _sha_file(G0),
                    "pinned_sha256": PL.G0_SHA256},
        "extract_tasks_json_sha256": _sha_file(EXTRACT / "TASKS.json"),
        "extract_lint_log_sha256": _sha_file(EXTRACT / "lint_log.json"),
        "extract_tasks": tasks,
        "targets": TARGET,
        "tally": lines,
        "shortfalls": summary["shortfalls"],
        "counts": counts,
        "lexicon_sha256": reg.sha256(),
        "pool_files": info,
        "quarantine_entries": len(quarantine),
    }
    paths.write_text(POOLS / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    wrote.append(str(POOLS / "manifest.json"))
    return {"summary": summary, "problems": [], "wrote": wrote}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze"))
    a = ap.parse_args(argv)
    out = run(write=(a.cmd == "freeze"))
    print(json.dumps(out["summary"], indent=1, ensure_ascii=False, default=str))
    if out.get("refused"):
        print(out["refused"])
    if out["wrote"]:
        print("wrote:")
        for w in out["wrote"]:
            print("  " + w)
    return 1 if out["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
