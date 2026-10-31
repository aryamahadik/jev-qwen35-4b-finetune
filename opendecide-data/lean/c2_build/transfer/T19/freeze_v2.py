"""transfer/T19/freeze_v2.py: the T19 re-freeze after redo rounds 2 and 3. Frozen v1 pools + every validated redo2
and redo3 answer -> pools_v2/ with a MANIFEST (C2_DATA_SPEC 6.2, 6.3; G0_SPEC.md v1.1 section 6; PREREG A37 (b), A38).

Why a new script: freeze.py is the v1 freeze (it reads haiku/author/ and haiku/extract/ only, expects exactly 7
extraction tasks and writes pools/), and redo2.py / redo2_merge.py stage pieces but never freeze the redo2 reads.
Nothing existing is edited: pools/ stays the v1 freeze (redo2.py's guards and test_redo2.py read it), and the
generator must load pools_v2/ explicitly (see LOADING).

History of this script: the first pools_v2/ froze v1 + redo2 (SHORT by one wording, wording/yn_not_compliant 13 of 14).
Redo round 3 (redo3.py, redo3_reads.py) authored 2 reserve items for that one cell and read their candidates; this
version folds them in (step 6) and the first pools_v2/ is kept beside the new one as pools_v2_prev/ (the freeze that
round 3 was authored against; redo3.py and redo3_reads.py read it as their baseline, because the new pools_v2/ closes
the shortfall they are written for).

Haiku writes text only and reads only to flag. This script never sets, edits or chooses a label or a read's answer,
never edits an answer file, never lowers a target (PINNED_TARGETS must equal freeze.TARGETS and G0 section 6) and
never loosens a gate bar.

Steps
  1. answers   every answer file of every round (round 1 authoring 20, round 1 reads 7, redo2 authoring 7, redo2 reads
               5, redo3 authoring 1, redo3 reads 2) is checked against its contract, taken from the index and chunk files the agents were given
               (check_answer). An invalid file is REJECTED WHOLE (never repaired): its items count as unanswered.
               A task named by the harness as audit-failed (AUDIT_FAILED / --audit-failed) is not opened at all.
  2. v1        pools/ must match its MANIFEST sha256, and a dry run of freeze.run() on the round 1 inputs must
               reproduce the v1 counts, shortfalls, G-LEX and G3-H summaries (the v1 inputs did not drift).
  3. redo2     redo2.load() on the accepted authoring answers: every candidate goes through the loaders' own checks
               (haiku_author check_*, freeze.slot_problems / wording_problems, the R1 hyphen check, the R2 key phrase
               check, exact dedup against the frozen pools). Packs, skins and attack lines keep the first clean
               candidate. Wordings and Mode F notes keep the first candidate that also passes its read (below).
  4. votes     G-LEX: every reading is recorded with lexicon.record_extraction (freeze.record_glex); a form is
               ADMITTED at >= form.required distinct agreeing extractors (2 for question forms; 3 for precedence and
               window kinds, which T19 does not have, but the kit rule is read from the form), any dissent REJECTS it
               for good, round 1 reads stand (no re-vote). G3-H: g3h.compare on each Mode F candidate, one template per
               candidate document, template_report at 0.98 (a mismatched candidate is dropped).
  5. merge     final lexicon = v1 admitted forms + kept redo2 forms; unit_test_all on the final registry (a kept form
               that fails it is excluded and the item falls back to its next admitted candidate); gate() over the
               wordings used. Skins, attack lines, documents, wordings and packs of v1 and redo2 are combined.
  6. redo3     (redo3_stage) the redo3 authoring answer and its 2 G-LEX read answers (3 more answer files, 42 in all):
               redo3_reads.build() re-derives the lint, the G-LEX registry and the read files; the read files on disk
               must equal them (drift = no read is used); the reads are recorded with the new extractor ids; the keep
               rule of REDO3_INDEX.json is applied: the cell may not exceed its target, so at most min(index gap, live
               gap) pieces are kept, walking the items in `order`, the first admitted candidate (written order) of the
               first item that has one, and a kept form must also pass unit_test_all in the final registry. The other
               admitted forms are reserves and are not frozen. The baseline check (pools_v2_prev/ MANIFEST sha256 =
               the one REDO3_INDEX.json recorded, and its pool files = this script's own v1 + redo2 result) is a hard
               gate. An audit-failed redo3 answer is not opened and the build then reproduces the previous freeze.
  7. gates     on the combined pools after step 6: H15 slots, skin-id uniqueness, exact cross-pool text dedup, wording
               sem, pack validate_pack + repeated site tuples + held/training name leak, G0 sha pin, targets (never
               lowered), reload of the written pools.
  8. write     pools_v2/ via paths.write_files (refuses before A38 and on never-open paths): skins, attacks, documents,
               wordings, lexicon, packs, quarantine, votes, answers_validation and MANIFEST.json. A re-run must give the
               same bytes; other content already there is refused unless --rewrite (or move it aside first, as
               pools_v2_prev/).

Status: READY iff no G0 target is short and the G-LEX gate and every hard gate pass; else SHORT with the exact
shortfalls. G13-seed decontamination and the file-access audits (c2_kit/audit.py needs the agents' transcripts, which
are outside this run) stay pending in both cases.

LOADING (the family code reads no pool path: the plugin takes a KitCtx from the caller)
  from transfer.T19 import freeze_v2
  ctx, packs = freeze_v2.load_pools_v2()        # = freeze.load_pools(pools_v2/); ctx = KitCtx(skins, admitted lexicon)
  wordings = json.loads((freeze_v2.POOLS_V2 / "wordings.json").read_text())      # admitted question forms
The generator must call this (or freeze.load_pools(freeze_v2.POOLS_V2)); freeze.load_pools() alone reads pools/ (v1).

  cd lean && ../.venv/bin/python c2_build/transfer/T19/freeze_v2.py                    (dry run: counts and gates)
  cd lean && ../.venv/bin/python c2_build/transfer/T19/freeze_v2.py --write            (writes pools_v2/ and verifies)
  options: --audit-failed TASK_ID[,TASK_ID...]   answers whose file-access audit failed (ignored, not opened)
           --rewrite                              allow --write to replace an existing, different pools_v2/
"""
from __future__ import annotations

import argparse
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
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from transfer.T19 import extract_build as EX  # noqa: E402
from transfer.T19 import freeze as FZ  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
from transfer.T19 import redo2 as RD  # noqa: E402

FAMILY = P.FAMILY
VERSION = "v2"
POOLS_V1 = FZ.POOLS
POOLS_V2 = HERE / "pools_v2"
POOLS_V2_PREV = HERE / "pools_v2_prev"          # the first pools_v2 (v1 + redo2), moved aside by the redo3 re-freeze;
#                                                 the baseline redo3.py / redo3_reads.py were written against
ROOT3 = HERE / "haiku" / "redo3"                # redo3 authoring task, REDO3_INDEX.json and answers/
XROOT3 = ROOT3 / "reads"                        # redo3 G-LEX read tasks and answers/
LEX_NOTE_V2 = "admitted forms only (v1 admitted + kept redo2 forms); every sem is declared (question meanings)"
LEX_NOTE = ("admitted forms only (v1 admitted + kept redo2 forms + kept redo3 forms); every sem is declared "
            "(question meanings)")
BASELINE_V1 = RD.ROOT / "pools_round1"          # the v1 freeze backed up by redo2_merge (informational comparison)
READ_FREE = ("packs", "skins", "attacks")       # redo2 pools kept without a read
POOL_FILES = ("skins.json", "attacks.json", "documents.json", "wordings.json", "lexicon.json", "packs.json",
              "quarantine.json")

# The harness's list of answers whose file-access audit failed, as given in this round's task text:
# "ignore these answer files, their file-access audit failed: []". An empty list names no answer, so nothing is
# ignored. A non-empty value (here or --audit-failed) removes those tasks' answers from every step below.
AUDIT_FAILED: tuple = ()

# G0_SPEC.md section 6 / freeze.TARGETS, pinned here so that a lowered target cannot pass unnoticed.
_TRAIN = ("audit_memo", "auditor_email", "audit_chat", "audit_ticket", "checklist_note", "meeting_notes", "report",
          "site_wiki")
_HELD = ("regulator_letter", "handover_note")
PINNED_TARGETS = {
    "packs_train": 32, "packs_held": 8,
    "skin": {r: 12 for r in _TRAIN}, "skin_heldout": {r: 16 for r in _HELD},
    "attack": 30,
    "freeform": {r: 4 for r in _TRAIN}, "freeform_heldout": {},
    "wording": {"ch_verdict": 26, "yn_compliant": 30, "ch_gap": 16, "yn_out_of": 14, "yn_not_compliant": 14,
                "yn_fails": 14},
}
PINNED_TOTAL = 344                               # 40 packs + 96 + 32 skins + 30 attacks + 32 Mode F + 114 wordings


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _read(path) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _j(obj) -> str:
    return FZ._j(obj)


def _rel(p) -> str:
    try:
        return str(Path(p).resolve().relative_to(HERE))
    except ValueError:
        return str(p)


def pinned_targets_ok() -> bool:
    flat = (PINNED_TARGETS["packs_train"] + PINNED_TARGETS["packs_held"] + sum(PINNED_TARGETS["skin"].values())
            + sum(PINNED_TARGETS["skin_heldout"].values()) + PINNED_TARGETS["attack"]
            + sum(PINNED_TARGETS["freeform"].values()) + sum(PINNED_TARGETS["wording"].values()))
    return FZ.TARGETS == PINNED_TARGETS and flat == PINNED_TOTAL


# ------------------------------------------------------------------------------------------------ 1. answer files

def round_specs() -> list:
    """One spec per expected answer file of every round, from the index and chunk files the agents were given:
    {round, task_id, kind, field, qids, n_cand, choices, dir}. Read from disk, never regenerated."""
    specs = []
    idx = _read(HA.ROOT / "TASKS.json")
    for t in idx["tasks"]:
        chunk = _read(HA.ROOT / "chunks" / f"{t['task_id']}.json")
        specs.append({"round": "r1_author", "task_id": t["task_id"], "kind": t["kind"],
                      "field": "pack" if t["kind"] == "author_pack" else "text",
                      "qids": [i["qid"] for i in chunk["items"]], "n_cand": None, "choices": {}, "dir": HA.ROOT})
    for rnd, root in (("r1_extract", EX.EXTRACT), ("redo2_extract", RD.XROOT)):
        for t in _read(root / "TASKS.json")["tasks"]:
            chunk = _read(root / "chunks" / f"{t['task_id']}.json")
            lex = t["kind"] == "extract_lex"
            specs.append({"round": rnd, "task_id": t["task_id"], "kind": t["kind"],
                          "field": "meaning" if lex else "auditor",
                          "qids": [i["qid"] for i in chunk["items"]], "n_cand": None,
                          "choices": {i["qid"]: list(i["choices"]) for i in chunk["items"]} if lex else {},
                          "dir": root})
    for rnd, root, index in (("redo2_author", RD.ROOT, "REDO2_INDEX.json"), ("redo3_author", ROOT3, "REDO3_INDEX.json")):
        for t in _read(root / index)["tasks"]:
            specs.append({"round": rnd, "task_id": t["name"], "kind": t["author_kind"],
                          "field": "packs" if t["pool"] == "packs" else "texts", "qids": list(t["qids"]),
                          "n_cand": t["n_candidates"], "choices": {}, "dir": root})
    for t in _read(XROOT3 / "TASKS.json")["tasks"]:                     # redo3 reads (G-LEX of the redo3 candidates)
        chunk = _read(XROOT3 / "chunks" / f"{t['task_id']}.json")
        specs.append({"round": "redo3_extract", "task_id": t["task_id"], "kind": t["kind"], "field": "meaning",
                      "qids": [i["qid"] for i in chunk["items"]], "n_cand": None,
                      "choices": {i["qid"]: list(i["choices"]) for i in chunk["items"]}, "dir": XROOT3})
    return specs


def _strs(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _pack_problems(p) -> list:
    if not isinstance(p, dict):
        return ["pack is not an object"]
    if set(p) != {"sites", "auditors", "controls"}:
        return [f"pack keys {sorted(p)} != ['auditors', 'controls', 'sites']"]
    return [f"pack.{k} is not a list of strings" for k in ("sites", "auditors", "controls") if not _strs(p[k])]


def check_answer(raw, spec: dict) -> list:
    """Contract problems of one parsed answer (empty = valid). The answer is one JSON array holding exactly one
    {"qid", <field>} object per qid of its own task (any other qid, a repeat, a missing qid, another key or a
    wrongly typed value is a problem). Content (lint, G-SL, dedup) is the loaders' job, not the contract's."""
    if not isinstance(raw, list):
        return ["the answer is not a JSON array"]
    field, qids = spec["field"], set(spec["qids"])
    probs, seen = [], Counter()
    for i, a in enumerate(raw):
        if not isinstance(a, dict):
            probs.append(f"entry {i} is not an object")
            continue
        q = a.get("qid")
        if not isinstance(q, str) or q not in qids:
            probs.append(f"entry {i}: qid {q!r} is not in this task")
            continue
        seen[q] += 1
        if set(a) != {"qid", field}:
            probs.append(f"{q}: keys {sorted(a)} != ['qid', '{field}']")
            continue
        v = a[field]
        if field == "text" or field == "auditor":
            if not isinstance(v, str):
                probs.append(f"{q}: {field} is not a string")
        elif field == "pack":
            probs += [f"{q}: {x}" for x in _pack_problems(v)]
        elif field == "texts":
            if not isinstance(v, list) or len(v) != spec["n_cand"]:
                probs.append(f"{q}: texts must be a list of {spec['n_cand']}")
            else:
                probs += [f"{q}: candidate {j} is not a string" for j, x in enumerate(v) if not isinstance(x, str)]
        elif field == "packs":
            if not isinstance(v, list) or len(v) != spec["n_cand"]:
                probs.append(f"{q}: packs must be a list of {spec['n_cand']}")
            else:
                probs += [f"{q}: candidate {j}: {x}" for j, p in enumerate(v) for x in _pack_problems(p)]
        elif field == "meaning":
            if not isinstance(v, str) or v not in spec["choices"][q]:
                probs.append(f"{q}: meaning is not one of the item's choices")
        else:
            probs.append(f"{q}: unknown field {field!r}")
    probs += [f"qid {q} answered {n} times" for q, n in sorted(seen.items()) if n > 1]
    missing = sorted(qids - set(seen))
    if missing:
        probs.append(f"{len(missing)} qid(s) unanswered")
    return probs


def validate_answers(audit_failed=()) -> dict:
    """Check every answer file of every round. Returns {"files": [record], "raw": {round: {task_id: parsed}} (accepted
    files only), "unexpected": [files in an answers/ folder that no index lists], "summary": {...}}. Nothing is
    edited; an invalid file is rejected whole; an audit-failed task is not opened."""
    failed = set(audit_failed)
    files, raw_ok, unexpected = [], {}, []
    specs = round_specs()
    for spec in specs:
        path = spec["dir"] / "answers" / f"{spec['task_id']}.json"
        rec = {"round": spec["round"], "task_id": spec["task_id"], "kind": spec["kind"], "file": _rel(path),
               "expected_items": len(spec["qids"]), "sha256": None, "bytes": None, "entries": None,
               "problems": [], "status": None}
        if spec["task_id"] in failed:
            rec["status"] = "ignored_audit_failed"
        elif not path.is_file():
            rec["status"], rec["problems"] = "missing", ["no answer file"]
        else:
            data = path.read_bytes()
            rec["sha256"], rec["bytes"] = _sha_bytes(data), len(data)
            try:
                parsed = json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                rec["status"], rec["problems"] = "rejected_invalid", [f"not JSON ({str(e)[:80]})"]
            else:
                rec["entries"] = len(parsed) if isinstance(parsed, list) else None
                rec["problems"] = check_answer(parsed, spec)
                if rec["problems"]:
                    rec["status"] = "rejected_invalid"
                else:
                    rec["status"] = "accepted"
                    raw_ok.setdefault(spec["round"], {})[spec["task_id"]] = parsed
        files.append(rec)
    listed = {(s["dir"], s["task_id"]) for s in specs}
    for d in sorted({s["dir"] for s in specs}, key=str):
        for f in sorted((d / "answers").glob("*")):
            if f.name != "README.txt" and (d, f.stem) not in listed:
                unexpected.append(_rel(f))
    by_round: dict = {}
    for r in files:
        d = by_round.setdefault(r["round"], Counter())
        d[r["status"]] += 1
        d["files"] += 1
        d["items"] += r["expected_items"]
    return {"files": files, "raw": raw_ok, "unexpected": unexpected,
            "summary": {"files": len(files), "by_round": {k: dict(v) for k, v in sorted(by_round.items())},
                        "accepted": sum(1 for r in files if r["status"] == "accepted"),
                        "rejected_invalid": [r["task_id"] for r in files if r["status"] == "rejected_invalid"],
                        "missing": [r["task_id"] for r in files if r["status"] == "missing"],
                        "ignored_audit_failed": [r["task_id"] for r in files
                                                 if r["status"] == "ignored_audit_failed"],
                        "unexpected_files": unexpected}}


# ------------------------------------------------------------------------------------------------ 2. v1 intact

def v1_state() -> dict:
    """sha256 of every v1 pool file (for the untouched check) read from disk."""
    return {f.name: _sha_bytes(f.read_bytes()) for f in sorted(POOLS_V1.glob("*.json"))}


def verify_v1() -> dict:
    """pools/ matches its MANIFEST, equals the round 1 backup, and a dry run of freeze.run() on the round 1 inputs
    reproduces the v1 counts, shortfalls, G-LEX and G3-H summaries."""
    man = _read(POOLS_V1 / "MANIFEST.json")
    bad = [k for k, v in man["sha256"].items() if _sha((POOLS_V1 / k).read_text(encoding="utf-8")) != v]
    backup = {f.name: (BASELINE_V1 / f.name).is_file() and (BASELINE_V1 / f.name).read_bytes() == f.read_bytes()
              for f in sorted(POOLS_V1.glob("*.json"))}
    out = {"manifest_sha_mismatches": bad, "equals_pools_round1_backup": all(backup.values()),
           "version": man["version"], "rederived": None}
    try:
        dry = FZ.run(False)
    except SystemExit as e:                       # freeze.rebuild() drift or a missing round 1 answer
        out["rederived"] = {"ok": False, "error": str(e)[:300]}
    else:
        g3_keys = ("bar", "documents", "pass", "fail", "frozen_documents", "template_quarantined")
        same = {"counts": dry["counts"] == man["counts"], "shortfalls": dry["shortfalls"] == man["shortfalls"],
                "glex": dry["glex"] == man["glex"],
                "g3h": {k: dry["g3h"][k] for k in g3_keys} == {k: man["g3h"][k] for k in g3_keys}}
        out["rederived"] = {"ok": all(same.values()), **same}
    out["ok"] = (not bad) and out["rederived"]["ok"]
    return out


# ------------------------------------------------------------------------------------------------ 3-5. redo2 pieces

def _norm(s) -> str:
    return EX._norm(str(s))


def pick_first(candidates: list, passes) -> int | None:
    """The written-order index of the first candidate for which passes(candidate) is true (None if none)."""
    for c in candidates:
        if passes(c):
            return c["j"]
    return None


def record_g3h(expected: dict, got: dict, fields: list) -> dict:
    """{key: (ok, diffs)} with g3h.compare for every expected key (no answer = fail), then the 0.98 template bar with
    one template per candidate document: a candidate below the bar is quarantined and dropped."""
    res = {k: (g3h.compare(w, got[k], fields) if k in got else (False, ["no answer"])) for k, w in expected.items()}
    rep = g3h.template_report([(k, k, ok) for k, (ok, _d) in res.items()])
    quarantined = set(rep["quarantined"])
    return {"results": {k: {"ok": ok and k not in quarantined, "diffs": d, "read": k in got}
                        for k, (ok, d) in res.items()},
            "template_quarantined": sorted(quarantined), "bar": g3h.PASS_RATE}


def choose_wordings(rows: list, reg_read, fid_of: dict, base: dict, excluded: set) -> tuple:
    """Per wording item the first candidate whose form is ADMITTED in the reading registry and not in `excluded`;
    then the final registry (v1 admitted forms + the kept forms) is built and unit-tested. Returns
    (kept [{row, cand, form_id}], final registry, unit failures of kept forms, reports)."""
    kept, reports = [], []
    for row in rows:
        k = None
        cand_rep = []
        for c in row["candidates"]:
            if not c["ok"]:
                cand_rep.append({"j": c["j"], "lint": "dropped", "reasons": c["reasons"]})
                continue
            fid = fid_of.get(f"{row['iid']}|c{c['j']}")
            st = reg_read.status(fid) if (reg_read is not None and fid) else "no_form"
            if fid in excluded and st == "admitted":
                st = "unit_fail_in_final_registry"
            cand_rep.append({"j": c["j"], "lint": "clean", "form_id": fid, "status": st,
                             "extractions": [list(e) for e in reg_read.forms[fid].extractions] if fid else [],
                             "unit_problems": reg_read.forms[fid].unit_problems if fid else []})
            if k is None and st == "admitted":
                k = (c, fid)
        reports.append({"qid": row["qid"], "iid": row["iid"], "cell": row["cell"], "task": row["task"],
                        "kept": k[0]["j"] if k else None, "candidates": cand_rep})
        if k:
            kept.append({"row": row, "cand": k[0], "form_id": k[1]})
    final = LexiconRegistry.from_json(base)             # v1 admitted forms: runs their unit tests
    base_ids = set(final.forms)
    for kp in kept:
        q, text, tid, psha = kp["cand"]["obj"]
        fo = final.add(text, question_sem(FAMILY, q), slots={"SITE": "name"}, source="haiku", family=FAMILY,
                       haiku_task_id=tid, haiku_prompt_sha=psha)
        if fo.form_id != kp["form_id"]:
            raise SystemExit(f"form id drift {kp['form_id']} -> {fo.form_id}")
        for ext, sem in reg_read.forms[fo.form_id].extractions:
            final.record_extraction(fo.form_id, ext, sem)
    res = final.unit_test_all()
    broken = sorted(f for f in base_ids if not res[f])
    if broken:
        raise SystemExit(f"v1 admitted forms fail their unit test beside the redo2 forms: {broken[:3]}")
    bad = sorted(kp["form_id"] for kp in kept if not res[kp["form_id"]])
    return kept, final, bad, reports


# ------------------------------------------------------------------------------------------------ 6. redo3

def baseline_check(stage5_files: dict) -> dict:
    """The freeze that redo round 3 was authored against (pools_v2_prev/) is present and intact, and equals this
    script's own v1 + redo2 result: its MANIFEST sha256 is the one REDO3_INDEX.json recorded, every file matches the
    sha256 in its MANIFEST, and its pool files equal `stage5_files` (the same files built in memory before step 6).
    Read only. {"ok", "present", "problems", ...}."""
    out = {"dir": _rel(POOLS_V2_PREV), "present": (POOLS_V2_PREV / "MANIFEST.json").is_file(), "problems": []}
    if not out["present"]:
        out["problems"].append("pools_v2_prev/ is missing: move the first pools_v2/ aside as pools_v2_prev/ "
                               "before the re-freeze")
        out["ok"] = False
        return out
    idx = _read(ROOT3 / "REDO3_INDEX.json")
    raw = (POOLS_V2_PREV / "MANIFEST.json").read_bytes()
    man = json.loads(raw.decode("utf-8"))
    out["manifest_sha256"] = _sha_bytes(raw)
    out["index_manifest_sha256"] = idx["source"]["pools_v2_manifest_sha256"]
    if out["manifest_sha256"] != out["index_manifest_sha256"]:
        out["problems"].append("pools_v2_prev/MANIFEST.json is not the pools_v2 MANIFEST that REDO3_INDEX.json recorded")
    bad = [k for k, v in man["sha256"].items() if _sha((POOLS_V2_PREV / k).read_text(encoding="utf-8")) != v]
    out["manifest_sha_mismatches"] = bad
    if bad:
        out["problems"].append(f"files differ from the previous MANIFEST: {bad}")
    differ = sorted(k for k, text in stage5_files.items()
                    if not (POOLS_V2_PREV / k).is_file() or (POOLS_V2_PREV / k).read_text(encoding="utf-8") != text)
    out["pool_files_differ_from_stage5"] = differ
    if differ:
        out["problems"].append(f"pool files differ from this script's v1 + redo2 result: {differ}")
    out["previous_status"] = man.get("status")
    out["previous_shortfalls"] = man.get("shortfalls")
    out["ok"] = not out["problems"]
    return out


def _inactive_redo3(final_reg, cell: str, task: str, problems: list) -> dict:
    return {"active": False, "cell": cell, "task": task, "cap": 0, "kept": [], "final_reg": final_reg, "reports": [],
            "glex_reads": {}, "problems": problems, "reads_usable": False, "drift": [], "forms_not_admitted": [],
            "admitted_not_kept": [], "lexicon_drops": [], "order": [], "lint": []}


def redo3_stage(raw_author: dict, raw_reads: dict, final_reg: LexiconRegistry, have: dict) -> dict:
    """Step 6, in memory. raw_author / raw_reads: the ACCEPTED redo3 answers {task_id: parsed} (an invalid, missing or
    audit-failed file is simply absent). final_reg: the stage 5 final registry (never changed). have: {qform: admitted
    wordings} at stage 5. Returns {"active", "kept", "final_reg" (a new registry when a piece is kept), "reports",
    "glex_reads", "problems", "reads_usable", "drift", ...}.

    Keep rule (REDO3_INDEX.json): the cell may not exceed its target, so at most min(index gap, live gap) pieces are
    kept; the items are walked in `order`, and the first admitted candidate (written order) of the first item that has
    one is kept; a candidate whose form fails unit_test_all in the final registry is skipped. Admitted forms that are
    not kept are reserves: reported, never frozen. Haiku's reads only flag: nothing here sets or edits a label."""
    from transfer.T19 import redo3_reads as RR     # lazy: redo3_reads imports this module
    idx = _read(ROOT3 / "REDO3_INDEX.json")
    cell = idx["b_authoring"]["cell"]
    qform = cell.split("/", 1)[1]
    task = idx["tasks"][0]["name"]
    if len(idx["tasks"]) != 1 or qform != RR.QFORM or cell != RR.CELL:
        raise SystemExit("REDO3_INDEX.json no longer names the one task and cell that redo3_reads.py is written for")
    live_gap = max(0, PINNED_TARGETS["wording"][qform] - have.get(qform, 0))
    cap = min(idx["b_authoring"]["gap"], live_gap)
    if task not in raw_author:
        return _inactive_redo3(final_reg, cell, task, [f"{task}: authoring answer not accepted (invalid, missing or "
                                                       "audit-failed): no redo3 piece is used"])
    r = RR.build(raw_author[task])
    if r["answer_problems"]:
        return _inactive_redo3(final_reg, cell, task, list(r["answer_problems"]))
    t = r["task"]
    out = _inactive_redo3(final_reg, cell, task, [])
    out.update(active=True, cap=cap, order=list(t["order"]), lint=r["lint"], lexicon_drops=list(r["lex_drops"]))

    # the read files on disk must be the ones regenerated from this answer (LINT.json carries the answer's sha256)
    drift = []
    for rel, text in r["files"].items():
        if rel != "LINT.json" and (not (XROOT3 / rel).exists() or (XROOT3 / rel).read_text(encoding="utf-8") != text):
            drift.append(rel)
    if r["files"]:
        lint_mem = json.loads(r["files"]["LINT.json"])
        lint_mem["answer_sha256"] = _sha(Path(t["answer_file"]).read_text(encoding="utf-8"))
        if not (XROOT3 / "LINT.json").exists() or _read(XROOT3 / "LINT.json") != lint_mem:
            drift.append("LINT.json")
    out["drift"] = drift
    out["reads_usable"] = bool(r["files"]) and not drift
    reg_read = r["reg"]
    if not r["files"]:
        out["problems"].append("no redo3 candidate is lint-clean and G-LEX-addable: nothing to read")
    elif drift:
        out["problems"].append(f"redo3 read files differ from the regenerated ones (no read is used): {drift[:4]}")
    else:
        for g in r["reads"]:
            raw = {c["task_id"]: raw_reads[c["task_id"]] for c in g["batch"].chunks if c["task_id"] in raw_reads}
            got, probs = chunker.load_answers(g["batch"], raw)
            out["problems"] += [f"{g['label']}: {p}" for p in probs]
            out["glex_reads"][g["label"]] = {"extractor_id": g["extractor_id"], "items": len(g["batch"].key),
                                             "answered": len(got), **FZ.record_glex(reg_read, got, g["extractor_id"])}

    # selection under the keep rule
    sem = question_sem(FAMILY, qform)
    cur, cur_json, remaining = final_reg, final_reg.to_json(), cap
    base_ids = set(final_reg.forms)
    kept, reports = [], []
    for qid in t["order"]:
        cand_rep, k = [], None
        for row in sorted((x for x in r["lint"] if x["qid"] == qid), key=lambda x: x["j"]):
            if not row["ok"]:
                cand_rep.append({"j": row["j"], "lint": "dropped", "reasons": row["reasons"]})
                continue
            fid = r["fid_of"].get(row["key"])
            st = reg_read.status(fid) if (fid and out["reads_usable"]) else "no_read" if fid else "no_form"
            rep = {"j": row["j"], "lint": "clean", "form_id": fid, "status": st, "text": row["text"],
                   "extractions": [list(e) for e in reg_read.forms[fid].extractions] if fid else [],
                   "unit_problems": list(reg_read.forms[fid].unit_problems) if fid else []}
            cand_rep.append(rep)
            if st != "admitted" or k is not None:
                continue
            if remaining <= 0:
                rep["reserve"] = "admitted; not kept: the cell is at its target (keep rule)"
                continue
            try:
                trial = LexiconRegistry.from_json(cur_json)
                fo = trial.add(row["text"], sem, slots={"SITE": "name"}, source="haiku", family=FAMILY,
                               haiku_task_id=t["name"], haiku_prompt_sha=t["prompt_sha256"])
                if fo.form_id != fid:
                    raise SystemExit(f"form id drift {fid} -> {fo.form_id}")
                for ext, s_id in reg_read.forms[fid].extractions:
                    trial.record_extraction(fid, ext, s_id)
                res = trial.unit_test_all()
            except LexiconError as e:
                rep["status"], rep["unit_problems"] = "final_registry_error", [str(e)[:200]]
                continue
            broken = sorted(f for f in base_ids if not res[f])
            if broken:
                raise SystemExit(f"frozen admitted forms fail their unit test beside the redo3 form: {broken[:3]}")
            if not res[fid]:
                rep["status"], rep["unit_problems"] = "unit_fail_in_final_registry", list(trial.forms[fid].unit_problems)
                continue
            k = (row, fid, trial)
            rep["kept"] = True
        reports.append({"qid": qid, "cell": cell, "task": t["name"], "kept": k[0]["j"] if k else None,
                        "candidates": cand_rep})
        if k:
            row, fid, trial = k
            cur, cur_json, remaining = trial, trial.to_json(), remaining - 1
            kept.append({"qid": qid, "cell": cell, "qform": qform, "task": t["name"], "candidate": row["j"],
                         "form_id": fid, "text": row["text"]})
    out.update(kept=kept, final_reg=cur, reports=reports)
    out["forms_not_admitted"] = [
        {"form_id": fid, "text": reg_read.forms[fid].text, "status": reg_read.status(fid),
         "extractions": [list(e) for e in reg_read.forms[fid].extractions],
         "unit_problems": list(reg_read.forms[fid].unit_problems)}
        for fid in sorted(set(r["fid_of"].values())) if reg_read.status(fid) != "admitted"]
    out["admitted_not_kept"] = [{"qid": rp["qid"], "j": c["j"], "form_id": c["form_id"], "text": c["text"]}
                                for rp in reports for c in rp["candidates"]
                                if c.get("status") == "admitted" and not c.get("kept")]
    return out


def build(audit_failed=()) -> dict:
    """Everything except the write: {"files": {name: text}, "summary", "status", "ready", "shortfalls", "issues"}."""
    if not pinned_targets_ok():
        raise SystemExit("freeze.TARGETS differ from the G0 section 6 targets: a target was changed, stopping")
    if P.T19Plugin.G0_SHA256_AUTHORED != _sha_bytes((HERE / "G0_SPEC.v1_1.md").read_bytes()):   # the G0 the pools were authored under (v1.2 is the live G0_SPEC.md)
        raise SystemExit("G0_SPEC.v1_1.md changed since it was frozen")
    before = v1_state()
    val = validate_answers(audit_failed)
    v1 = verify_v1()
    raw_auth = val["raw"].get("redo2_author", {})
    raw_reads = val["raw"].get("redo2_extract", {})

    # 3. redo2 authoring: the loaders' checks on every candidate
    loaded = RD.load(raw_auth)
    sel, r1 = loaded["selection"], loaded["r1"]
    rows_by_pool = {p: [r for r in sel["items"] if r["pool"] == p] for p in RD.ORDER}

    # 4. the reads: the regenerated read files must equal the ones the agents were given
    ex = RD.extract_build(sel, r1)
    drift = [rel for rel, text in ex["files"].items()
             if not (RD.XROOT / rel).exists() or (RD.XROOT / rel).read_text(encoding="utf-8") != text]
    reads_usable = not drift
    reg_read = ex["reg"]
    glex_reads, g3 = {}, {"results": {}, "template_quarantined": [], "bar": g3h.PASS_RATE}
    read_problems = []
    if reads_usable:
        for g in ex["glex"]:
            raw = {c["task_id"]: raw_reads[c["task_id"]] for c in g["batch"].chunks if c["task_id"] in raw_reads}
            got, probs = chunker.load_answers(g["batch"], raw)
            read_problems += [f"{g['label']}: {p}" for p in probs]
            glex_reads[g["label"]] = {"extractor_id": g["extractor_id"], "items": len(g["batch"].key),
                                      "answered": len(got), **FZ.record_glex(reg_read, got, g["extractor_id"])}
        if ex["g3h"]:
            b = ex["g3h"]["batch"]
            raw = {c["task_id"]: raw_reads[c["task_id"]] for c in b.chunks if c["task_id"] in raw_reads}
            got, probs = chunker.load_answers(b, raw)
            read_problems += [f"{ex['g3h']['label']}: {p}" for p in probs]
            g3 = record_g3h(ex["g3h_expected"], got, EX.g3h_fields())
    else:
        read_problems.append(f"redo2 read files differ from the regenerated ones (no read is used): {drift[:4]}")

    # 5. merge: read-free pieces, wordings (G-LEX), Mode F notes (G3-H)
    kept_free = {p: [] for p in READ_FREE}
    prov, unkept = [], []
    for pool in READ_FREE:
        for row in rows_by_pool[pool]:
            if row["kept"] is None:
                unkept.append({"pool": pool, "qid": row["qid"], "cell": row["cell"], "task": row["task"],
                               "reasons": [c["reasons"] for c in row["candidates"]] or ["no candidate"]})
                continue
            cand = next(c for c in row["candidates"] if c["j"] == row["kept"])
            kept_free[pool].append(cand["obj"])
            obj = cand["obj"]
            prov.append({"pool": pool, "piece_id": obj["pack_id"] if pool == "packs" else obj.skin_id,
                         "cell": row["cell"], "qid": row["qid"], "task": row["task"], "candidate": row["kept"]})
    excluded: set = set()
    for _ in range(4):
        kept_w, final_reg, bad, word_reports = choose_wordings(rows_by_pool["wordings"], reg_read,
                                                               ex["fid_of"], _read(POOLS_V1 / "lexicon.json"),
                                                               excluded)
        if not bad:
            break
        excluded |= set(bad)
    else:
        raise SystemExit("the final registry never stabilised")
    for kp in kept_w:
        prov.append({"pool": "wordings", "piece_id": kp["form_id"], "cell": kp["row"]["cell"],
                     "qid": kp["row"]["qid"], "task": kp["row"]["task"], "candidate": kp["cand"]["j"]})

    free_reports, kept_docs = [], []
    for row in rows_by_pool["freeform"]:
        k = None
        crep = []
        for c in row["candidates"]:
            if not c["ok"]:
                crep.append({"j": c["j"], "lint": "dropped", "reasons": c["reasons"]})
                continue
            gk = f"g3h2|{row['iid']}|c{c['j']}"
            r = g3["results"].get(gk, {"ok": False, "diffs": ["no read"], "read": False})
            crep.append({"j": c["j"], "lint": "clean", "g3h_ok": r["ok"], "g3h_read": r["read"], "diffs": r["diffs"]})
            if k is None and r["ok"]:
                k = c
        free_reports.append({"qid": row["qid"], "iid": row["iid"], "cell": row["cell"], "task": row["task"],
                             "kept": k["j"] if k else None, "candidates": crep})
        if k:
            kept_docs.append(k["obj"])
            prov.append({"pool": "documents", "piece_id": k["obj"].skin_id, "cell": row["cell"], "qid": row["qid"],
                         "task": row["task"], "candidate": k["j"]})
    kept_free["documents"] = kept_docs

    # the combined pools (v1 frozen JSON + redo2 pieces), sorted as freeze.py sorts them
    v1j = {f: _read(POOLS_V1 / f) for f in POOL_FILES}
    skins = sorted(v1j["skins.json"] + [FZ.skin_json(s) for s in kept_free["skins"]], key=lambda d: d["skin_id"])
    attacks = sorted(v1j["attacks.json"] + [FZ.skin_json(s) for s in kept_free["attacks"]],
                     key=lambda d: d["skin_id"])
    docs = sorted(v1j["documents.json"] + [FZ.skin_json(s) for s in kept_free["documents"]],
                  key=lambda d: d["skin_id"])
    packs = sorted(v1j["packs.json"] + [{"pack_id": p["pack_id"], "held_out": p["held_out"], "sites": list(p["sites"]),
                                          "auditors": list(p["auditors"]), "controls": list(p["controls"])}
                                         for p in kept_free["packs"]], key=lambda p: p["pack_id"])
    v1_wording = {w["form_id"]: w for w in v1j["wordings.json"]}
    words = dict(v1_wording)
    for kp in kept_w:
        f = final_reg.forms[kp["form_id"]]
        words[f.form_id] = {"form_id": f.form_id, "qform": kp["cand"]["obj"][0], "sem_id": f.sem_id, "text": f.text,
                            "slots": dict(f.slots), "haiku_task_id": f.haiku_task_id,
                            "haiku_prompt_sha": f.haiku_prompt_sha, "extractions": [list(e) for e in f.extractions]}
    wordings5 = sorted(words.values(), key=lambda w: w["form_id"])           # the v1 + redo2 result (step 5)

    # 6. redo3: the baseline (pools_v2_prev/) must equal the step 5 result; then the redo3 stage, in memory
    lex_json5 = final_reg.to_json()
    lex_json5["note"] = LEX_NOTE_V2
    baseline = baseline_check({"skins.json": _j(skins), "attacks.json": _j(attacks), "documents.json": _j(docs),
                               "wordings.json": _j(wordings5), "lexicon.json": _j(lex_json5),
                               "packs.json": _j(packs)})
    if baseline["ok"]:
        r3 = redo3_stage(val["raw"].get("redo3_author", {}), val["raw"].get("redo3_extract", {}), final_reg,
                         Counter(w["qform"] for w in wordings5))
    else:
        idx3 = _read(ROOT3 / "REDO3_INDEX.json")
        r3 = _inactive_redo3(final_reg, idx3["b_authoring"]["cell"], idx3["tasks"][0]["name"],
                             ["redo3 baseline check failed (no redo3 piece is used): " + "; ".join(baseline["problems"])])
    final_reg = r3["final_reg"]
    prov3 = []
    for kp in r3["kept"]:
        f = final_reg.forms[kp["form_id"]]
        words[f.form_id] = {"form_id": f.form_id, "qform": kp["qform"], "sem_id": f.sem_id, "text": f.text,
                            "slots": dict(f.slots), "haiku_task_id": f.haiku_task_id,
                            "haiku_prompt_sha": f.haiku_prompt_sha, "extractions": [list(e) for e in f.extractions]}
        prov3.append({"pool": "wordings", "piece_id": f.form_id, "cell": kp["cell"], "qid": kp["qid"],
                      "task": kp["task"], "candidate": kp["candidate"]})
    wordings = sorted(words.values(), key=lambda w: w["form_id"])

    # gates on the combined pools
    gates = {}
    skin_objs = {"skins": [FZ.skin_from_json(d) for d in skins], "attacks": [FZ.skin_from_json(d) for d in attacks],
                 "documents": [FZ.skin_from_json(d) for d in docs]}
    slot_fail = [{"skin_id": s.skin_id, "problems": FZ.slot_problems(s)} for pool in skin_objs.values() for s in pool
                 if FZ.slot_problems(s)]
    doc_ph = [d.skin_id for d in skin_objs["documents"] if K.placeholders(d.text)]
    ids = [d["skin_id"] for d in skins + attacks + docs]
    dup_ids = sorted(k for k, v in Counter(ids).items() if v > 1)
    texts = Counter(_norm(d["text"]) for d in skins + attacks + docs)
    dup_texts = sum(1 for v in texts.values() if v > 1)
    gates["H15_slots"] = {"failures": slot_fail, "documents_with_placeholders": doc_ph, "pass": not slot_fail
                          and not doc_ph}
    gates["skin_ids_unique"] = {"ids": len(ids), "duplicates": dup_ids, "pass": not dup_ids}
    gates["G12_exact_text_dedup"] = {"duplicate_texts": dup_texts, "pass": dup_texts == 0}
    pack_bad = [{"pack_id": p["pack_id"], "problems": P.validate_pack(p)} for p in packs if P.validate_pack(p)]
    site_keys = Counter(tuple(sorted(x.lower() for x in p["sites"])) for p in packs)
    train_p = [p for p in packs if not p["held_out"]]
    held_p = [p for p in packs if p["held_out"]]
    leak = sorted(set().union(*(FZ.pack_vals(p) for p in held_p)) & set().union(*(FZ.pack_vals(p)
                                                                                    for p in train_p)))
    gates["packs"] = {"validate_pack_failures": pack_bad, "repeated_site_tuples": sum(1 for v in site_keys.values()
                                                                                       if v > 1),
                      "held_names_also_in_training_packs": leak,
                      "pass": not pack_bad and not leak and all(v == 1 for v in site_keys.values())}
    w_bad = []
    for w in wordings:
        want_sem = question_sem(FAMILY, w["qform"])
        probs = FZ.wording_problems(w["text"]) + ([] if (w["sem_id"] == want_sem
                                                         and final_reg.forms[w["form_id"]].sem_id == want_sem)
                                                  else ["sem mismatch"])
        if probs:
            w_bad.append({"form_id": w["form_id"], "problems": probs})
    lex_gate = final_reg.gate([w["form_id"] for w in wordings])
    lex_all = final_reg.gate()
    gates["G-LEX"] = {"bar": "unit test + >= 2 distinct agreeing readings for question forms (3 for precedence and "
                             "window, none here); any dissent rejects for good; round 1 reads stand",
                      "forms_used": len(wordings), "status_counts": lex_gate["status_counts"],
                      "not_admitted_used": lex_gate["not_admitted"], "unknown": lex_gate["unknown"],
                      "registry_forms": len(final_reg.forms), "registry_all_admitted": lex_all["pass"],
                      "wording_problems": w_bad, "pass": lex_gate["pass"] and lex_all["pass"] and not w_bad}
    chosen_keys = {f"g3h2|{r['iid']}|c{r['kept']}" for r in free_reports if r["kept"] is not None}
    frozen_ok = all(g3["results"].get(k, {}).get("ok") for k in chosen_keys)
    gates["G3-H"] = {"bar": g3h.PASS_RATE, "template": "candidate document (one Mode F document = one template)",
                     "redo2_candidates_read": sum(1 for r in g3["results"].values() if r["read"]),
                     "redo2_candidates_passed": sum(1 for r in g3["results"].values() if r["ok"]),
                     "template_quarantined": g3["template_quarantined"], "v1_documents": len(v1j["documents.json"]),
                     "documents_frozen": len(docs), "redo2_documents_frozen": len(kept_docs),
                     "frozen_redo2_documents_all_passed": frozen_ok,
                     "note": "a drop gate: a failing candidate is dropped, never frozen; v1 documents passed their "
                             "read in freeze.run (re-derived in v1_verification)",
                     "pass": frozen_ok and len(kept_docs) == len(chosen_keys)}

    # counts and shortfalls against the (pinned) targets
    counts = {
        "packs_train": len(train_p), "packs_held": len(held_p),
        "skin": dict(sorted(Counter(d["register"] for d in skins if not d["held_out"]).items())),
        "skin_heldout": dict(sorted(Counter(d["register"] for d in skins if d["held_out"]).items())),
        "attack": len(attacks),
        "freeform": dict(sorted(Counter(d["register"] for d in docs if not d["held_out"]).items())),
        "freeform_heldout": dict(sorted(Counter(d["register"] for d in docs if d["held_out"]).items())),
        "wording": dict(sorted(Counter(w["qform"] for w in wordings).items())),
    }
    shortfalls = []

    def need(name, have, want):
        if have < want:
            shortfalls.append({"item": name, "admitted": have, "target": want, "shortfall": want - have})

    need("packs_train", counts["packs_train"], PINNED_TARGETS["packs_train"])
    need("packs_held", counts["packs_held"], PINNED_TARGETS["packs_held"])
    for grp in ("skin", "skin_heldout", "freeform", "freeform_heldout", "wording"):
        for r, want in PINNED_TARGETS[grp].items():
            need(f"{grp}/{r}", counts[grp].get(r, 0), want)
    need("attack", counts["attack"], PINNED_TARGETS["attack"])
    over = [k for grp in ("skin", "skin_heldout", "freeform", "wording") for k, v in counts[grp].items()
            if v > PINNED_TARGETS[grp].get(k, 0)]
    short_total = sum(s["shortfall"] for s in shortfalls)
    admitted_total = (counts["packs_train"] + counts["packs_held"] + sum(counts["skin"].values())
                      + sum(counts["skin_heldout"].values()) + counts["attack"] + sum(counts["freeform"].values())
                      + sum(counts["wording"].values()))

    # files
    redo2_lex_not_admitted = [{"qid": r["qid"], "cell": r["cell"], "iid": r["iid"], "task": r["task"],
                               "candidates": r["candidates"]}
                              for r in word_reports if r["kept"] is None]
    lex_json = final_reg.to_json()
    lex_json["note"] = LEX_NOTE if r3["kept"] else LEX_NOTE_V2
    short_cells = {sf["item"] for sf in shortfalls}
    # a redo2 wording item that stayed without an admitted candidate is still open only while its cell is short
    closed_items = [{"pool": "wordings", "cell": r["cell"], "qid": r["qid"], "iid": r["iid"], "task": r["task"],
                     "closed_by": [f"{kp['task']} {kp['qid']} candidate {kp['candidate']} ({kp['form_id']})"
                                   for kp in r3["kept"] if kp["cell"] == r["cell"]]}
                    for r in redo2_lex_not_admitted if r["cell"] not in short_cells]
    open_items = (
        [{"pool": u["pool"], "cell": u["cell"], "qid": u["qid"], "task": u["task"], "why": "no clean candidate"}
         for u in unkept]
        + [{"pool": "wordings", "cell": r["cell"], "qid": r["qid"], "iid": r["iid"], "task": r["task"],
            "why": "; ".join(f"candidate {c['j']}: {c.get('status') or c.get('lint')}"
                             + (f" (read as {[e[1].rsplit('.', 1)[-1] for e in c['extractions']]})"
                                if c.get("extractions") else "") for c in r["candidates"]) or "no candidate"}
           for r in redo2_lex_not_admitted if r["cell"] in short_cells]
        + [{"pool": "wordings", "cell": r["cell"], "qid": r["qid"], "task": r["task"],
            "why": "redo3 item without a kept piece: " + ("; ".join(
                f"candidate {c['j']}: {c.get('status') or c.get('lint')}" for c in r["candidates"]) or "no candidate")}
           for r in r3["reports"] if r["kept"] is None and r["cell"] in short_cells]
        + [{"pool": "freeform", "cell": r["cell"], "qid": r["qid"], "iid": r["iid"], "task": r["task"],
            "why": "; ".join(f"candidate {c['j']}: " + (c["lint"] if c["lint"] == "dropped" else
                                                         ("G3-H pass" if c["g3h_ok"] else "G3-H fail"))
                             for c in r["candidates"]) or "no candidate"}
           for r in free_reports if r["kept"] is None])
    quarantine = {"v1": v1j["quarantine.json"],
                  "redo2": {"unkept_read_free_items": unkept, "wording_items_without_an_admitted_candidate":
                            redo2_lex_not_admitted,
                            "forms_not_admitted": [
                                {"form_id": fid, "text": reg_read.forms[fid].text, "status": reg_read.status(fid),
                                 "extractions": [list(e) for e in reg_read.forms[fid].extractions],
                                 "unit_problems": reg_read.forms[fid].unit_problems}
                                for fid in sorted(reg_read.forms) if fid in set(ex["fid_of"].values())
                                and reg_read.status(fid) != "admitted"] if reg_read else [],
                            "lexicon_drops_before_reads": ex["lex_drops"],
                            "mode_f_items_without_a_passing_candidate": [r for r in free_reports if r["kept"] is None],
                            "answer_problems": read_problems + val["summary"]["rejected_invalid"]
                            + val["summary"]["missing"]},
                  "redo3": {"forms_not_admitted": r3["forms_not_admitted"],
                            "admitted_reserves_not_kept": r3["admitted_not_kept"],
                            "items_without_a_kept_piece": [x for x in r3["reports"] if x["kept"] is None],
                            "redo2_wording_items_closed_by_redo3": closed_items,
                            "lexicon_drops_before_reads": [{k: x[k] for k in ("qid", "j", "text", "reasons")}
                                                           for x in r3["lexicon_drops"]],
                            "lint_dropped": [{k: x[k] for k in ("qid", "j", "text", "reasons")}
                                             for x in r3["lint"] if not x["ok"]],
                            "problems": r3["problems"]}}
    votes = {"glex_reads": glex_reads, "wordings": word_reports, "g3h": {"bar": g3["bar"], "items": free_reports,
                                                                         "template_quarantined":
                                                                         g3["template_quarantined"]},
             "provenance_of_redo2_pieces": sorted(prov, key=lambda r: (r["pool"], r["piece_id"])),
             "redo3": {"glex_reads": r3["glex_reads"], "wordings": r3["reports"], "order": r3["order"],
                       "cap": r3["cap"]},
             "provenance_of_redo3_pieces": sorted(prov3, key=lambda r: (r["pool"], r["piece_id"]))}
    files = {"skins.json": _j(skins), "attacks.json": _j(attacks), "documents.json": _j(docs),
             "wordings.json": _j(wordings), "lexicon.json": _j(lex_json), "packs.json": _j(packs),
             "quarantine.json": _j(quarantine), "votes.json": _j(votes),
             "answers_validation.json": _j({"audit_failed_given_by_harness": list(audit_failed),
                                            "files": val["files"], "unexpected": val["unexpected"],
                                            "summary": val["summary"]})}
    sha = {k: _sha(v) for k, v in files.items()}

    hard_ok = {"answers_no_unexpected": not val["unexpected"], "v1_intact": v1["ok"],
               "H15_slots": gates["H15_slots"]["pass"], "skin_ids_unique": gates["skin_ids_unique"]["pass"],
               "G12_exact_text_dedup": gates["G12_exact_text_dedup"]["pass"], "packs": gates["packs"]["pass"],
               "G-LEX": gates["G-LEX"]["pass"], "G3-H": gates["G3-H"]["pass"], "no_cell_over_target": not over,
               "final_unit_tests": not bad, "redo3_baseline_intact": baseline["ok"]}
    ready = not shortfalls and all(hard_ok.values())
    issues = []
    if shortfalls:
        issues.append(f"{short_total} of {PINNED_TOTAL} G0 targets short: " + "; ".join(
            f"{s['item']} {s['admitted']}/{s['target']}" for s in shortfalls))
    issues += [f"hard gate failed: {k}" for k, v in hard_ok.items() if not v]
    if val["summary"]["rejected_invalid"]:
        issues.append(f"answer files rejected (invalid): {val['summary']['rejected_invalid']}")
    if val["summary"]["missing"]:
        issues.append(f"answer files missing: {val['summary']['missing']}")
    if val["summary"]["ignored_audit_failed"]:
        issues.append(f"answers ignored (audit failed): {val['summary']['ignored_audit_failed']}")
    if read_problems:
        issues.append(f"read problems: {read_problems[:3]}")
    if r3["problems"]:
        issues.append(f"redo3 problems: {r3['problems'][:3]}")
    status = ("READY: every G0 target met and the G-LEX gate passes" if ready else
              f"SHORT: {short_total} of {PINNED_TOTAL} G0 targets short" if shortfalls else
              "SHORT: a hard gate failed (" + ", ".join(k for k, v in hard_ok.items() if not v) + ")")
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "freeze (v1 pools + redo2 + redo3)",
        "tier": "transfer_dev (never trained; every row dev-only)",
        "g0_sha256": P.T19Plugin.G0_SHA256_AUTHORED, "g0_ambiguity_pass": P.T19Plugin.G0_HAIKU_TASK,
        "status": status, "ready": ready, "sha256": sha,
        "counts": counts, "targets": {**PINNED_TARGETS, "_total": PINNED_TOTAL},
        "admitted_total": admitted_total, "target_total": PINNED_TOTAL, "shortfalls": shortfalls,
        "open_items": open_items,
        "gates": gates, "hard_gates_ok": hard_ok,
        "lineage": {"v1_pools": "pools/ (unchanged; sha256 below)", "v1_manifest_version": v1["version"],
                    "v1_sha256": before, "v1_verification": v1,
                    "v1_counts": _read(POOLS_V1 / "MANIFEST.json")["counts"],
                    "redo2_index": "haiku/redo2/REDO2_INDEX.json", "redo2_version": RD.VERSION,
                    "redo2_pieces_added": dict(Counter(r["pool"] for r in prov)),
                    "redo2_items": len(sel["items"]), "redo2_items_kept": len(prov),
                    "redo3_index": "haiku/redo3/REDO3_INDEX.json", "redo3_reads": "haiku/redo3/reads/",
                    "redo3_pieces_added": dict(Counter(r["pool"] for r in prov3)),
                    "redo3_items": len(r3["reports"]), "redo3_items_kept": len(prov3),
                    "previous_pools_v2": "pools_v2_prev/ (the first pools_v2: v1 + redo2, SHORT by one wording; "
                                         "kept as the baseline of redo3.py / redo3_reads.py)",
                    "previous_pools_v2_manifest_sha256": baseline.get("manifest_sha256")},
        "answers": {**val["summary"], "audit_failed_given_by_harness": list(audit_failed),
                    "harness_text": "ignore these answer files, their file-access audit failed: [] (an empty list: "
                                    "no answer is named, so none is ignored; --audit-failed applies a non-empty list)",
                    "validation_file": "answers_validation.json"},
        "redo2_reads": {"usable": reads_usable, "drift": drift[:6], "glex": glex_reads,
                        "g3h_read": gates["G3-H"]["redo2_candidates_read"],
                        "g3h_passed": gates["G3-H"]["redo2_candidates_passed"],
                        "problems": read_problems},
        "redo3": {"active": r3["active"], "cell": r3["cell"], "task": r3["task"], "order": r3["order"],
                  "cap": r3["cap"], "keep_rule": _read(ROOT3 / "REDO3_INDEX.json")["keep_rule"],
                  "kept": r3["kept"], "reads_usable": r3["reads_usable"], "drift": r3["drift"][:6],
                  "glex": r3["glex_reads"], "problems": r3["problems"], "baseline": baseline,
                  "g0_changed": False},
        "loading": "the generator loads freeze_v2.load_pools_v2() (= freeze.load_pools(pools_v2/)); freeze.load_pools() "
                   "alone reads pools/ (v1). The T19 plugin reads no pool path (the caller passes the KitCtx).",
        "pending_gates": [
            "G13-seed decontamination on every pool before any row (C2_DATA_SPEC 6.3): not run in this step",
            "file-access audit (c2_kit/audit.py) of the 20 round 1 authoring, 7 round 1 read, 7 redo2 authoring, 5 "
            "redo2 read, 1 redo3 authoring and 2 redo3 read transcripts: no transcript is read here; the harness list "
            f"of failed audits was {list(audit_failed)}; a failed audit discards that agent's answers "
            "(--audit-failed re-runs without them)",
            "promotion: pools/ stays the v1 freeze; the generator must load pools_v2/ explicitly",
        ],
    }
    files["MANIFEST.json"] = _j(manifest)
    after = v1_state()
    if after != before:
        raise SystemExit("pools/ changed during the run: v1 must stay untouched")
    return {"files": files, "manifest": manifest, "status": status, "ready": ready, "shortfalls": shortfalls,
            "open_items": open_items,
            "issues": issues, "counts": counts, "gates": gates, "hard_gates_ok": hard_ok, "validation": val["summary"],
            "v1": v1, "glex_reads": glex_reads, "reads_usable": reads_usable, "short_total": short_total,
            "admitted_total": admitted_total, "final_registry": final_reg, "kept_docs": kept_free["documents"],
            "redo3": r3, "baseline": baseline}


# ------------------------------------------------------------------------------------------------ 7. write, load

def write(res: dict, rewrite: bool = False) -> dict:
    """Write pools_v2/ (guarded writer) once; a different existing pools_v2/ is refused unless rewrite."""
    clash = [k for k, text in res["files"].items()
             if (POOLS_V2 / k).exists() and (POOLS_V2 / k).read_text(encoding="utf-8") != text]
    if clash and not rewrite:
        raise SystemExit(f"pools_v2/ already holds other content for {clash[:4]} (pass --rewrite to replace it)")
    paths.write_files(POOLS_V2, res["files"])
    out = verify_pools_v2()
    if not out["ok"]:
        raise SystemExit(f"pools_v2/ failed its read-back check: {out}")
    return out


def load_pools_v2() -> tuple:
    """(KitCtx with the admitted skins, attack lines and documents; the admitted lexicon; the packs) of pools_v2/."""
    return FZ.load_pools(POOLS_V2)


def verify_pools_v2() -> dict:
    """sha256 of every pools_v2 file against its MANIFEST, the freeze.py reload checks, and pools/ still v1."""
    man = _read(POOLS_V2 / "MANIFEST.json")
    bad = [k for k, v in man["sha256"].items() if _sha((POOLS_V2 / k).read_text(encoding="utf-8")) != v]
    out = FZ.verify_pools(POOLS_V2)
    out["manifest_sha_mismatches"] = bad
    out["v1_untouched"] = v1_state() == man["lineage"]["v1_sha256"]
    out["ok"] = bool(out["ok"]) and not bad and out["v1_untouched"]
    return out


def summary(res: dict, written: dict | None = None) -> dict:
    return {"status": res["status"], "ready": res["ready"], "admitted_total": res["admitted_total"],
            "target_total": PINNED_TOTAL, "counts": res["counts"], "shortfalls": res["shortfalls"],
            "issues": res["issues"], "open_items": res["open_items"], "hard_gates_ok": res["hard_gates_ok"],
            "G-LEX": {k: v for k, v in res["gates"]["G-LEX"].items() if k != "wording_problems"},
            "G3-H": res["gates"]["G3-H"], "answers": res["validation"], "glex_reads": res["glex_reads"],
            "redo3": {"active": res["redo3"]["active"], "cap": res["redo3"]["cap"], "kept": res["redo3"]["kept"],
                      "glex_reads": res["redo3"]["glex_reads"], "reads_usable": res["redo3"]["reads_usable"],
                      "admitted_reserves_not_kept": res["redo3"]["admitted_not_kept"],
                      "forms_not_admitted": res["redo3"]["forms_not_admitted"], "problems": res["redo3"]["problems"],
                      "baseline_ok": res["baseline"]["ok"]},
            "v1_verification": res["v1"], "written": written}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write pools_v2/ and verify it")
    ap.add_argument("--rewrite", action="store_true", help="allow --write to replace a different pools_v2/")
    ap.add_argument("--audit-failed", default="", help="comma-separated task ids whose file-access audit failed")
    a = ap.parse_args(argv)
    failed = tuple(x for x in a.audit_failed.split(",") if x) or AUDIT_FAILED
    res = build(failed)
    written = write(res, a.rewrite) if a.write else None
    print(json.dumps(summary(res, written), indent=1, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
