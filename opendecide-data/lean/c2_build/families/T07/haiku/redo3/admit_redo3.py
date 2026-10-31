#!/usr/bin/env python3
"""families/T07/haiku/redo3/admit_redo3.py: T07 REDO-3, the admit stage (a NEW file; T07's freeze-v2 path for redo3).

T07 has no freeze_v2.py: its ruled ingest path is layered. v1 is frozen in pools/*.json (freeze_pools.py), redo2 wrote
the supplement pools/redo2/ (haiku/redo2/build_redo2.py admit) and merged_pools.py merges the layers. This file is the
same step for the last round: it folds every validated redo3 answer into a THIRD supplement, pools/redo3/, and
merged_pools.load() merges it. Nothing earlier is changed: pools/*.json and pools/redo2/ stay byte for byte, no answer
file, key, plan or task file is edited.

Input (all in memory first, nothing written until --write):
  * the two redo3 authoring answers (build_redo3.py: 3 yn_misses training wordings, 17 packs) and the two redo3 G-LEX
    read answers (build_redo3_reads.py: redo3-r1, redo3-r2), each checked against its answer contract
    (validate_answers.validate_all). A file-access audit failure would be passed in as --failed-audit <task id>: that
    answer file is then not read at all and the stage stops (a discarded answer cannot be admitted). None failed.
  * the redo3 task files and read task files on disk must equal their rebuild (build_redo3.author_files,
    build_redo3_reads.read_files): the opaque ids in the answers belong to exactly those tasks.
Rules (G0_SPEC.md section 4; no gate bar, target or lint check changes; nothing here reads or sets a label or a gold):
  wordings   lint (authoring.lint_wording incl. G-SL + the redo3 brief), dedup and registry unit test were done by
             build_redo3_reads.state(); here each read's meaning is mapped to a sem (a pick outside the closed list of 7
             question meanings is a rejecting vote) and recorded: a wording is ADMITTED iff both independent reads
             (redo3-r1, redo3-r2) picked q.t07.yn_misses (2/2; one dissent rejects for good; T07 has no 3/3 kind).
             Admitted wordings join wordings_add.json; every new form (admitted or not) is a row of lexicon_add.json.
  packs      the decisions of build_redo3_reads.pack_decisions (lint_pack, check_packs over the kept v1 packs first, the
             reverse-direction check, taken words, pool-word collisions); kept packs join packs_add.json, all training.
             A pack is not a lexicon form: no G-LEX or G3-H read. G13-seed is not run (as in v1 and redo2).
  verdict    merged_pools.merge_redo3 + merged_pools.verdict over v1 + redo2 + redo3: every G0 section 4 target line
             (never lowered), the G-LEX gate, the G3-H bar (redo3 authored no Mode F text, so no new G3-H read) and the
             pack checks. READY = no shortfall and every gate passes.
Output: pools/redo3/{packs_add,wordings_add,lexicon_add,extraction_record,quarantine}.json + MANIFEST.json (counts,
the merged counts against the targets, the sha256 of every pool file and of every input answer), written through
c2_kit.paths (A38 guard, never-open guard) and made read-only. Deterministic: no timestamps. If pools/redo3 already
exists the stage compares bytes: identical = nothing to do; different = STOP (move it aside first:
mv families/T07/pools/redo3 families/T07/pools/redo3_prev).

Run from lean/c2_build (-B or PYTHONDONTWRITEBYTECODE=1):
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B families/T07/haiku/redo3/admit_redo3.py          # dry run
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B families/T07/haiku/redo3/admit_redo3.py --write  # freeze
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                   # families/T07/haiku/redo3
T07 = HERE.parents[1]
C2_BUILD = T07.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from families.T07 import freeze_pools as FZ  # noqa: E402
from families.T07 import merged_pools as MP  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07 import validate_answers as VA  # noqa: E402
from families.T07.haiku.redo3 import build_redo3 as R3  # noqa: E402
from families.T07.haiku.redo3 import build_redo3_reads as RR  # noqa: E402

FAMILY = "T07"
VERSION = "r3"
POOLS = T07 / "pools"
SUPP = POOLS / "redo3"
QFORM = RR.QFORM                                          # "yn_misses"
WORD_ORIGIN = "haiku_wording_r3"
FILES = ("packs_add.json", "wordings_add.json", "lexicon_add.json", "extraction_record.json", "quarantine.json")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _dump(obj) -> str:
    """Exactly what paths.write_json writes."""
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


# ------------------------------------------------------------------------------------------------ 1. answer contracts
def check_answers(failed_audit=()) -> tuple:
    """(problems, {task_id: sha256 of its answer file}) over the redo3 authoring and read answers. Any invalid, missing,
    ignored (audit-failed) or extra file is a problem: the stage stops, it never edits or skips an answer."""
    probs, shas = [], {}
    for name, root in (("redo3-author", R3.ROOT), ("redo3-reads", RR.READS_ROOT)):
        rep = VA.validate_all(failed_audit, rounds={name: root})
        for r in rep["rounds"]:
            for k in ("invalid", "missing", "ignored", "extra_files"):
                if r[k]:
                    probs.append(f"{name}: {k} {[x['task_id'] if isinstance(x, dict) else x for x in r[k]]}")
            for x in r["results"]:
                if x["status"] == "valid":
                    shas[x["task_id"]] = x["sha256"]
    return probs, shas


def tasks_on_disk(st: dict) -> list:
    """The redo3 author files and the read files on disk must be the rebuild (the answers' opaque ids belong to them)."""
    g = RR.gap_dict()
    files, _ = R3.author_files(g=g)
    probs = [f"author: {x} differs from the rebuild" for x in R3.check_on_disk(R3.ROOT, files)]
    rfiles, _ = RR.read_files(st)
    probs += [f"reads: {x} differs from the rebuild" for x in R3.check_on_disk(RR.READS_ROOT, rfiles)]
    probs += RR.check_reads(rfiles, st)
    return probs


# ------------------------------------------------------------------------------------------------ 2. the votes
def read_answers(st: dict) -> tuple:
    """({read: {task_id: parsed answer array}}, {task_id: sha256}) of the G-LEX read answers on disk."""
    raw, shas = {}, {}
    for read, b in st["batches"].items():
        raw[read] = {}
        for c in b.chunks:
            p = RR.READS_ROOT / b.answer_path(c["task_id"])
            if not p.is_file():
                raise SystemExit(f"STOP: no answer file {p}")
            shas[c["task_id"]] = _sha(p.read_bytes())
            raw[read][c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
    return raw, shas


def record_votes(st: dict, raw: dict, reg=None) -> list:
    """Record every read's pick on `reg` (default st["reg"]; a test passes a copy). A meaning outside the closed list of
    the form's kind maps to None, which rejects (as in v1 and redo2). Returns the extraction record rows."""
    reg = reg or st["reg"]
    rec = []
    for read in RR.READS:
        got, probs = chunker.load_answers(st["batches"][read], raw[read])
        if probs:
            raise SystemExit("STOP: " + "; ".join(probs[:5]))
        for fid in sorted(st["read_fids"]):
            a = got.get(fid)
            if not isinstance(a, dict) or not isinstance(a.get("meaning"), str):
                raise SystemExit(f"STOP: unanswered G-LEX item {fid} ({read})")
            sem = reg.meaning_to_sem(reg.forms[fid].kind, a["meaning"])
            reg.record_extraction(fid, read, sem)
            rec.append({"form_id": fid, "read": read, "meaning": a["meaning"], "sem_id": sem})
    return rec


# ------------------------------------------------------------------------------------------------ 3. the layer
def build_layer(st: dict, rec: list, reg=None) -> dict:
    """{file name: object} of the redo3 supplement, from the state and the recorded votes (in memory)."""
    reg = reg or st["reg"]
    origin = st["origin"]
    by_pid = {p["piece_id"]: p for p in st["pieces"]}
    drops = [dict(d) for d in st["wording_drops"]]
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    words, forms = [], []
    for fid in st["new_fids"]:
        f, p = reg.forms[fid], origin[fid]
        forms.append({"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text, "origin": WORD_ORIGIN,
                      "piece_id": p["piece_id"], "qform": QFORM, "held_out": f.held_out, "source": f.source,
                      "haiku_task_id": f.haiku_task_id, "extractions": [[e, s] for e, s in f.extractions],
                      "status": reg.status(fid)})
        if fid in st["read_fids"] and reg.status(fid) == "admitted":
            words.append({"wording_id": FZ.sid_of(p["piece_id"], "wording"), "piece_id": p["piece_id"],
                          "internal_id": p["internal_id"], "form_id": fid, "qform": QFORM, "held_out": False,
                          "text": p["value"], "haiku_task_id": p["task_id"], "haiku_prompt_sha": p["haiku_prompt_sha"]})
        elif fid in st["read_fids"]:
            drops.append({"form_id": fid, "sem_id": f.sem_id, "text": f.text, "origin": WORD_ORIGIN, "stage": "G-LEX",
                          "status": reg.status(fid), "reason": [f"{e}: {s}" for e, s in f.extractions]})
    assert all(form_of[w["text"]] == w["form_id"] for w in words)
    packs = []
    for d in st["packs"]:
        if d["status"] != "kept":
            drops.append({"piece_id": d["piece_id"], "task_id": d["task_id"], "piece": "pack", "stage": "pack",
                          "reason": d["reasons"]})
            continue
        p = by_pid[d["piece_id"]]
        v = p["value"]
        packs.append({"pack_id": FZ.sid_of(p["piece_id"], "pack"), "piece_id": p["piece_id"],
                      "internal_id": p["internal_id"], "held_out": False, "store": v["store"], "ladder": v["ladder"],
                      "regions": v["regions"], "categories": v["categories"], "customers": v["customers"],
                      "haiku_task_id": p["task_id"], "haiku_prompt_sha": p["haiku_prompt_sha"]})
    packs.sort(key=lambda x: x["piece_id"])
    words.sort(key=lambda x: x["piece_id"])
    return {
        "packs_add.json": {"family": FAMILY, "version": VERSION, "pool": "packs (all training)", "n": len(packs),
                           "items": packs},
        "wordings_add.json": {"family": FAMILY, "version": VERSION, "n": len(words), "items": words},
        "lexicon_add.json": {"family": FAMILY, "version": VERSION,
                             "pool": "lexicon (redo3 yn_misses wordings; v1 and redo2 statuses unchanged, checked)",
                             "forms": forms},
        "extraction_record.json": {"family": FAMILY, "version": VERSION, "lexicon_extractions": rec},
        "quarantine.json": {"family": FAMILY, "version": VERSION, "n": len(drops),
                            "by_stage": dict(Counter(d["stage"] for d in drops)), "items": drops,
                            "pack_decisions": st["packs"]},
    }


def merged_verdict(layer: dict) -> tuple:
    """(merged pools, verdict) of v1 + redo2 + this layer, in memory (the same merge load() does from disk)."""
    add = {n: layer[n] for n in MP.REDO3_FILES}
    pools = MP.merge_redo3(MP.load(through="redo2"), add, {"version": VERSION, "in_memory": True})
    return pools, MP.verdict(pools)


def merged_counts(pools: dict, v: dict) -> dict:
    adm = [f for f in pools["lexicon"] if f["status"] == "admitted"]
    w = Counter((x["qform"], "held_out" if x["held_out"] else "training") for x in pools["wordings"])
    return {"packs": {"total": len(pools["packs"]), "training": v["counts"]["packs_training"],
                      "held_out": v["counts"]["packs_held_out"]},
            "skins_by_register": v["counts"]["skins"], "documents_by_register": v["counts"]["documents"],
            "attacks": v["counts"]["attacks"],
            "canonical_admitted": dict(sorted(Counter(f["sem_id"] for f in adm
                                                      if f["origin"] in ("canonical", "canonical_r2")).items())),
            "paraphrase_admitted": dict(sorted(Counter(f["sem_id"] for f in adm
                                                       if f["origin"] in ("haiku_form", "haiku_form_r2")).items())),
            "wordings": {q: {"training": w[(q, "training")], "held_out": w[(q, "held_out")]} for q in FZ.QFORMS},
            "lexicon_admitted": len(adm)}


def manifest_of(st: dict, layer: dict, texts: dict, pools: dict, v: dict, answer_shas: dict, failed_audit) -> dict:
    forms = layer["lexicon_add.json"]["forms"]
    drops = layer["quarantine.json"]
    return {
        "family": FAMILY, "version": VERSION, "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED,
        "status": "redo3 supplement, pre-G13-seed", "ready": v["ready"],
        "inputs": {"answer_sha256": dict(sorted(answer_shas.items())), "failed_audit": sorted(failed_audit),
                   "baseline_manifest_sha256": {"v1": _sha((POOLS / "MANIFEST.json").read_bytes()),
                                                "redo2": _sha((MP.R2 / "MANIFEST.json").read_bytes())},
                   "gaps_closed": st["gaps"]},
        "pieces_authored": len(st["pieces"]), "quarantine_by_stage": drops["by_stage"],
        "gates": {
            "G-LEX": {"rule": "2/2 independent reads (redo3-r1, redo3-r2); T07 has no 3/3 kind",
                      "forms_read": len(st["read_fids"]),
                      "status_counts": dict(Counter(f["status"] for f in forms)),
                      "merged_pool_problems": v["gates"]["G-LEX"]["problems"], "pass": v["gates"]["G-LEX"]["pass"]},
            "G3-H": {"bar": FZ.G3H_BAR, "texts_read": 0,
                     "note": "redo3 authored no Mode F text; the v1 and redo2 passes are unchanged",
                     "pass": v["gates"]["G3-H"]["pass"]},
            "packs": {"kept": layer["packs_add.json"]["n"], "asked": len(st["packs"]),
                      "problems": v["gates"]["packs (G0 S2 uniqueness, lint_pack)"]["problems"],
                      "pass": v["gates"]["packs (G0 S2 uniqueness, lint_pack)"]["pass"]}},
        "counts": {"redo3": {"packs": layer["packs_add.json"]["n"], "wordings": {QFORM: layer["wordings_add.json"]["n"]},
                             "forms": dict(Counter(f"{f['sem_id']} {f['origin']} {f['status']}" for f in forms))},
                   "merged": merged_counts(pools, v)},
        "shortfalls": v["shortfalls"], "n_shortfalls": v["n_shortfalls"],
        "pool_files": {n: {"sha256": _sha(t.encode("utf-8")), "bytes": len(t.encode("utf-8"))}
                       for n, t in sorted(texts.items())},
        "merge_rule": "pools = v1 pools/*.json + pools/redo2/*_add.json + pools/redo3/*_add.json (packs, wordings, "
                      "lexicon); lexicon = v1 + redo2 + redo3 forms (earlier statuses unchanged); Mode F: one kept "
                      "text per brief; load(through='redo2') is the baseline the redo3 tasks were authored against",
        "not_run": ["G13-seed (decontam on the pools, C2_DATA_SPEC 6.4 step 4)", "pilot of 1,000 rows",
                    "any row generation"],
    }


# ------------------------------------------------------------------------------------------------ 4. the stage
def compute(failed_audit=()) -> dict:
    """Everything the stage decides, in memory. Stops on any contract, task-on-disk or earlier-status problem."""
    probs, a_shas = check_answers(failed_audit)
    if probs:
        raise SystemExit("STOP: answers: " + "; ".join(probs))
    st = RR.state()
    probs = tasks_on_disk(st)
    if probs:
        raise SystemExit("STOP: " + "; ".join(probs[:6]))
    raw, r_shas = read_answers(st)
    rec = record_votes(st, raw)
    reg = st["reg"]
    recorded = {f["form_id"]: f["status"] for f in MP.load(through="redo2")["lexicon"]}      # every v1 + redo2 status
    changed = sorted(fid for fid, s in recorded.items() if reg.status(fid) != s)
    if changed or set(recorded) - set(reg.forms):
        raise SystemExit(f"STOP: an earlier form changed status after the redo3 votes: {changed[:3]}")
    layer = build_layer(st, rec)
    texts = {n: _dump(layer[n]) for n in FILES}
    pools, v = merged_verdict(layer)
    shas = dict(a_shas, **r_shas)
    manifest = manifest_of(st, layer, texts, pools, v, shas, failed_audit)
    texts["MANIFEST.json"] = _dump(manifest)
    return {"st": st, "layer": layer, "texts": texts, "pools": pools, "verdict": v, "manifest": manifest}


def write_layer(texts: dict) -> str:
    """Write pools/redo3 through the guarded writers; read-only afterwards. 'unchanged' if it is already there byte for
    byte; STOP if it differs (move it aside first)."""
    if SUPP.exists():
        same = all((SUPP / n).is_file() and (SUPP / n).read_bytes() == t.encode("utf-8") for n, t in texts.items())
        extra = sorted(p.name for p in SUPP.iterdir() if p.name not in texts)
        if same and not extra:
            return "unchanged"
        raise SystemExit(f"STOP: {SUPP} exists and differs from the rebuild (extra files {extra}). Move it aside "
                         f"first: mv {SUPP} {SUPP.with_name('redo3_prev')}")
    SUPP.mkdir(parents=True, exist_ok=False)
    for name, text in sorted(texts.items()):
        path = paths.write_text(SUPP / name, text)
        os.chmod(path, 0o444)
    return "written"


def summary(c: dict) -> dict:
    v, m = c["verdict"], c["manifest"]
    return {"ready": v["ready"], "shortfalls": v["shortfalls"], "gates": {k: g["pass"] for k, g in v["gates"].items()},
            "redo3": m["counts"]["redo3"], "quarantine_by_stage": m["quarantine_by_stage"],
            "merged": m["counts"]["merged"]["wordings"][QFORM] | {"packs": m["counts"]["merged"]["packs"]}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--failed-audit", action="append", default=[], metavar="TASK_ID",
                    help="a task whose file-access audit failed: its answer file is not read and the stage stops")
    args = ap.parse_args()
    c = compute(args.failed_audit)
    out = summary(c)
    if args.write:
        out["pool_files"] = write_layer(c["texts"])
        disk = MP.verdict(MP.load())                       # the loader reads what was just written, sha-checked
        if (disk["ready"], disk["shortfalls"], disk["counts"]) != (c["verdict"]["ready"], c["verdict"]["shortfalls"],
                                                                    c["verdict"]["counts"]):
            raise SystemExit("STOP: the verdict from the pool files on disk differs from the in-memory verdict")
        out["verified_from_disk"] = True
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    print("READY" if c["verdict"]["ready"] else f"SHORT: {c['verdict']['n_shortfalls']} target line(s) short")
    return 0 if c["verdict"]["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
