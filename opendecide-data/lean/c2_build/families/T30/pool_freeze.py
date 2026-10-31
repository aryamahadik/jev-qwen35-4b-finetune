"""families/T30/pool_freeze.py: record the G-LEX extraction answers, admit or quarantine every wording, and freeze the
T30 pools with a manifest (C2_DATA_SPEC 6.2 item 4; G0_SPEC 3.4-3.6). A new file. It generates no rows.

  rebuild()  the authoring kept pieces and the extraction batches, in memory (lex_extract stages 1-5, the same code that
             wrote haiku/extract/). Nothing is written.
  check      the on-disk chunks, prompts and manifests of haiku/extract/ are the same bytes as the rebuild, so every
             answer's qid maps to the same form.
  record     load the answers of both reads (chunker.load_answers over each read's whole batch). Every answer whose
             meaning is one of the listed choices is recorded with reg.record_extraction as one extraction by its task
             ("haiku:<task id>"). An answer that is not one of the choices is an invalid read: it is not recorded, the
             form stays pending, and it is quarantined. Admission is reg.status: a form is admitted at 2/2 distinct
             extractors agreeing on its own sem id (T30 has no precedence or window forms, so no 3/3 forms).
  freeze     write haiku/extract/recorded.json, then pools/ (packs, skins, attack_lines, wordings, names, lexicon),
             pools/quarantine.jsonl and pools/MANIFEST.json (sha256 of every pool file, counts per kind and register,
             admitted vs the G0 targets, every shortfall). The G0 targets are constants below and are not lowered.

Run (from lean/, c2_build on sys.path):  python -m families.T30.pool_freeze            (writes)
                                         python -m families.T30.pool_freeze --dry-run  (computes and prints only)
Any mismatch between the rebuild and the on-disk extraction chunks, or any unanswered or unreadable answer file,
stops the run before anything is recorded or written.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from c2_kit import chunker, paths
from c2_kit.lexicon import LexiconRegistry
from families.T30 import authoring as A
from families.T30 import lex_extract as LX
from families.T30 import plugin as T

FAMILY = "T30"
POOLS = T.HERE / "pools"
RECORDED = LX.EXTRACT / "recorded.json"

# G0 targets (families/T30/G0_SPEC.md, section 3 and the packs / registers rules it cites). Not lowered.
G0 = {
    "packs_per_training_type": 4,        # section 3.1: 4 per training type, 2 per held-out type = 44
    "packs_per_held_type": 2,
    "packs_total": 44,
    "training_skins_min": 350,           # section 3.3: >= 350 training skins
    "training_registers_min": 8,         # section 3.3 / plugin: >= 8 training registers
    "held_registers_min": 2,             # plugin: >= 2 held-out registers
    "wordings_min_total": 30,            # section 3.4: >= 30 over the 8 forms
    "wordings_card_min": 5,              # section 3.4: each card's rows use >= 5 (checked per form, training side)
    "wordings_held_share": 0.15,         # section 3.4: seeded 15% split of each form's admitted wordings
    "wordings_held_min_per_form": 3,     # section 3.4: >= 3 per form
    "record_types": 12,                  # section 2: 10 training + 2 held-out types
}


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_obj(o) -> str:
    return sha_text(json.dumps(o, sort_keys=True, ensure_ascii=False))


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def qform_of(sem_id: str) -> str:
    return sem_id.split(".")[-1]


# ================================================================================================ rebuild
def rebuild() -> dict:
    """The authoring kept pieces and the extraction batches, deterministic from the answer files (nothing written)."""
    recs = A.load(A.ROOT)
    info = {t["task_id"]: t for t in A.task_index(A.build(A.ROOT), A.ROOT)}
    log = {"family": FAMILY, "source": "haiku/author/answers", "dropped": []}
    kept, authored = LX.lint_stage(recs, info, log)
    by_cat, names = LX.dedup_stage(kept, log)
    reg = LX.lexicon_stage(by_cat["wording"], info, log)
    batches = LX.extraction_batches(reg)
    return {"recs": recs, "log": log, "authored": authored, "by_cat": by_cat, "names": names, "reg": reg,
            "batches": batches}


def check_extract_on_disk(batches: list) -> tuple:
    """(files compared, mismatching paths). Prompts, chunks and manifests must be the same bytes as the rebuild."""
    checked, bad = 0, []
    for label, b in batches:
        for rel, text in b.files().items():
            if not rel.startswith(("chunks/", "prompts/", "manifest/")):
                continue
            checked += 1
            p = LX.EXTRACT / rel
            if not p.is_file() or p.read_text(encoding="utf-8") != text:
                bad.append(f"{label}:{rel}")
    return checked, bad


# ================================================================================================ load + record
def load_reads(batches: list) -> tuple:
    """({read label: {"batch", "answers": {form id: answer}}}, problems, {answer path: sha256})."""
    reads, problems, shas = {}, [], {}
    for label, b in batches:
        raw = {}
        for c in b.chunks:
            tid = c["task_id"]
            p = LX.EXTRACT / b.answer_path(tid)
            if not p.is_file():
                problems.append(f"{label} {tid}: answer file missing")
                continue
            shas[b.answer_path(tid)] = sha_file(p)
            try:
                raw[tid] = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                problems.append(f"{label} {tid}: answer is not JSON: {e}")
        got, probs = chunker.load_answers(b, raw)
        problems += [f"{label}: {x}" for x in probs]
        reads[label] = {"batch": b, "answers": got}
    return reads, problems, shas


def record(reg, reads: dict) -> tuple:
    """Record every valid answer as one extraction (extractor "haiku:<task id>"). Returns (invalid reads, counts)."""
    invalid, n_rec = [], Counter()
    for label, rd in reads.items():
        b = rd["batch"]
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        for fid in sorted(rd["answers"]):
            ans = rd["answers"][fid]
            meaning = ans.get("meaning") if isinstance(ans, dict) else None
            sem = reg.meaning_to_sem("question", meaning) if isinstance(meaning, str) else None
            if sem is None:
                invalid.append({"stage": "extract", "task": label, "iid": fid, "task_id": task_of[fid],
                                "reason": f"meaning is not one of the listed choices: {str(meaning)[:160]!r}"})
                continue
            reg.record_extraction(fid, f"haiku:{task_of[fid]}", sem)
            n_rec[label] += 1
    return invalid, n_rec


def recorded_view(reg, reads: dict) -> list:
    seen = defaultdict(list)
    for label, rd in reads.items():
        b = rd["batch"]
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        for fid, ans in rd["answers"].items():
            seen[fid].append({"read": label, "task_id": task_of[fid],
                              "meaning": ans.get("meaning") if isinstance(ans, dict) else None})
    rows = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        rows.append({"form_id": fid, "qform": qform_of(f.sem_id), "sem_id": f.sem_id, "text": f.text,
                     "status": reg.status(fid), "haiku_task_id": f.haiku_task_id,
                     "extractions": [{"extractor": e, "sem_id": s} for e, s in f.extractions],
                     "reads": sorted(seen.get(fid, []), key=lambda r: r["read"])})
    return rows


# ================================================================================================ freeze
def freeze_packs(by_cat: dict, quar: list) -> list:
    out = []
    for c in sorted(by_cat["pack"], key=lambda c: c["iid"]):
        type_key = c["iid"].split(":")[1]
        rt, probs = A.check_pack(type_key, c["piece"])
        if rt is None or probs:
            quar.append({"stage": "freeze", "task": c["label"], "iid": c["iid"], "reason": "; ".join(probs)[:240]})
            continue
        out.append({"pool_id": c["iid"], "type": type_key, "held_out": T.TYPES[type_key].held_out,
                    "task_id": c["task_id"], "pack_sha256": sha_obj(c["piece"]), "pack": c["piece"]})
    return out


def freeze_skins(by_cat: dict) -> list:
    out = []
    for c in sorted(by_cat["skin"], key=lambda c: c["iid"]):
        reg = c["iid"].split(":")[1]
        text = c["piece"]
        out.append({"skin_id": f"SK-T30-{reg.upper()}-{sha_text(text)[:8]}", "pool_id": c["iid"], "register": reg,
                    "escape": A.ESCAPE.get(reg, "text"), "held_out": reg in T.T30Plugin.HELD_OUT_REGISTERS,
                    "task_id": c["task_id"], "text_sha256": sha_text(text), "text": text})
    dup = [k for k, v in Counter(s["skin_id"] for s in out).items() if v > 1]
    if dup:
        raise RuntimeError(f"skin ids collide: {dup[:3]}")
    return out


def freeze_attacks(by_cat: dict) -> list:
    out = [{"attack_id": f"AT-T30-{sha_text(c['piece'])[:8]}", "pool_id": c["iid"], "task_id": c["task_id"],
            "text_sha256": sha_text(c["piece"]), "text": c["piece"]}
           for c in sorted(by_cat["attack"], key=lambda c: c["iid"])]
    dup = [k for k, v in Counter(s["attack_id"] for s in out).items() if v > 1]
    if dup:
        raise RuntimeError(f"attack ids collide: {dup[:3]}")
    return out


def split_wordings(reg) -> tuple:
    """Admitted forms, the seeded 15% held-out split per question form (A.split_held, G0 3.4). Sets form.held_out."""
    adm = [fid for fid in sorted(reg.forms) if reg.status(fid) == "admitted"]
    by_q = defaultdict(list)
    for fid in adm:
        by_q[qform_of(reg.forms[fid].sem_id)].append(fid)
    held, per_form = set(), {}
    for q in sorted(by_q):
        train, hold = A.split_held(by_q[q], q, share=G0["wordings_held_share"],
                                   minimum=G0["wordings_held_min_per_form"])
        held |= set(hold)
        per_form[q] = {"admitted": len(by_q[q]), "training": len(train), "held_out": len(hold)}
    for fid in adm:
        reg.forms[fid].held_out = fid in held
    return adm, per_form


def freeze_wordings(reg, adm: list) -> list:
    out = []
    for fid in adm:
        f = reg.forms[fid]
        out.append({"form_id": fid, "qform": qform_of(f.sem_id), "sem_id": f.sem_id, "text": f.text,
                    "held_out": bool(f.held_out), "status": "admitted", "haiku_task_id": f.haiku_task_id,
                    "haiku_prompt_sha": f.haiku_prompt_sha, "extractions": [{"extractor": e, "sem_id": s}
                                                                          for e, s in f.extractions],
                    "text_sha256": sha_text(f.text)})
    return out


def freeze_lexicon(reg) -> tuple:
    obj = reg.to_json()
    obj["forms"] = [x for x in obj["forms"] if x["status"] == "admitted"]
    chk = LexiconRegistry.from_json(obj)            # re-runs the unit tests and the extraction status on the pool
    gate = chk.gate()
    return obj, gate


def quarantine_rows(log: dict, reg, invalid: list) -> list:
    out = [{"stage": d["stage"], "task": d["task"], "iid": d["iid"], "reason": d["reason"]} for d in log["dropped"]]
    out += invalid
    for fid in sorted(reg.forms):
        st = reg.status(fid)
        if st != "admitted":
            f = reg.forms[fid]
            out.append({"stage": "g-lex", "task": f.haiku_task_id, "iid": fid,
                        "reason": f"{st}: extractions {[[e, s] for e, s in f.extractions]} "
                                  f"(needs 2 agreeing extractors, sem {f.sem_id})"})
    return out


def targets(packs, skins, attacks, per_form, names, reg_counts, adm_total) -> tuple:
    """(report rows, shortfalls). Each row: item, got, target, met. A target is never lowered."""
    rows = []

    def add(item, got, target, op, note=""):
        # target None: report-only (G0 states no number), never a shortfall
        if target is None:
            met = None
        else:
            met = got >= target if op == ">=" else got == target
        rows.append({"item": item, "got": got, "target": target, "op": op, "met": met, "note": note})

    per_type = Counter(p["type"] for p in packs)
    quota = {k: (G0["packs_per_held_type"] if t.held_out else G0["packs_per_training_type"])
             for k, t in T.TYPES.items()}
    add("packs (all types)", len(packs), G0["packs_total"], "==")
    add("record types covered", sum(1 for k in quota if per_type[k] > 0), G0["record_types"], "==")
    for k in sorted(quota):
        add(f"packs for type {k}", per_type[k], quota[k], "==")
    tr = [s for s in skins if not s["held_out"]]
    ho = [s for s in skins if s["held_out"]]
    add("training skins", len(tr), G0["training_skins_min"], ">=")
    add("training registers covered", len({s["register"] for s in tr}), G0["training_registers_min"], ">=")
    add("held-out registers covered", len({s["register"] for s in ho}), G0["held_registers_min"], ">=")
    add("held-out skins", len(ho), None, ">=", "report only: G0 states no held-out skin number")
    add("admitted wordings (all 8 forms)", adm_total, G0["wordings_min_total"], ">=")
    add("training wordings, lowest form", min(v["training"] for v in per_form.values()), G0["wordings_card_min"],
        ">=", "derived from G0 3.4 (each card's rows use >= 5 wordings)")
    add("held-out wordings, lowest form", min(v["held_out"] for v in per_form.values()),
        G0["wordings_held_min_per_form"], ">=", "G0 3.4 (>= 3 per form)")
    add("attack lines", len(attacks), None, ">=", "report only: G0 states no attack-line number")
    add("name first pool", len(names["first"]), None, ">=", "report only: G0 states no name-pool number")
    add("name pair pool", len(names["pairs"]), None, ">=", "report only: G0 states no name-pool number")
    add("name last pool", len(names["last"]), None, ">=", "report only: G0 states no name-pool number")
    add("requester pool", len(names["requesters"]), None, ">=", "report only: G0 states no name-pool number")
    short = [r for r in rows if r["met"] is False]
    return rows, short


def write_pools(files: dict) -> dict:
    """Write {relative path under POOLS: text} with the guarded writer; returns {path: sha256}."""
    shas = {}
    for rel, text in sorted(files.items()):
        paths.write_text(POOLS / rel, text)
        shas[rel] = sha_text(text)
    return shas


def jsonl(rows: list) -> str:
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


def js(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# ================================================================================================ main
def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in argv
    paths.require_a38()
    st = rebuild()
    reg = st["reg"]

    n_chk, bad = check_extract_on_disk(st["batches"])
    if bad:
        raise SystemExit(f"STOP: rebuilt extraction chunks differ from disk ({len(bad)}): {bad[:5]}")
    reads, probs, ans_sha = load_reads(st["batches"])
    if probs:
        raise SystemExit(f"STOP: extraction answers are incomplete: {probs[:8]}")
    n_answers = {label: len(rd["answers"]) for label, rd in reads.items()}

    invalid, n_rec = record(reg, reads)
    stat = Counter(reg.status(fid) for fid in reg.forms)
    if not dry:
        paths.write_json(RECORDED, recorded_view(reg, reads))

    adm, per_form = split_wordings(reg)
    packs = freeze_packs(st["by_cat"], st["log"]["dropped"])
    skins = freeze_skins(st["by_cat"])
    attacks = freeze_attacks(st["by_cat"])
    wordings = freeze_wordings(reg, adm)
    lex_obj, gate = freeze_lexicon(reg)
    names = {"first": st["names"]["first"], "pairs": [list(p) for p in st["names"]["pairs"]],
             "last": st["names"]["last"], "requesters": st["names"]["requesters"]}
    quar = quarantine_rows(st["log"], reg, invalid)
    rep, short = targets(packs, skins, attacks, per_form, st["names"], None, len(adm))

    g0_sha = sha_file(T.HERE / "G0_SPEC.md")
    counts = {
        "authored_pieces": dict(st["authored"]),
        "authored_total": sum(st["authored"].values()),
        "packs_frozen": len(packs),
        "skins_frozen_training": sum(1 for s in skins if not s["held_out"]),
        "skins_frozen_held_out": sum(1 for s in skins if s["held_out"]),
        "skins_by_register": dict(Counter(s["register"] for s in skins)),
        "attack_lines_frozen": len(attacks),
        "wordings_admitted": len(adm),
        "wordings_admitted_by_form": per_form,
        "wordings_not_admitted": {k: v for k, v in Counter(qform_of(reg.forms[f].sem_id) for f in reg.forms
                                                              if reg.status(f) != "admitted").items()},
        "names_frozen": {k: len(v) for k, v in names.items()},
        "extraction_items_per_read": n_answers,
        "extraction_recorded_per_read": dict(n_rec),
        "extraction_invalid_reads": len(invalid),
        "form_status_after_record": dict(stat),
        "quarantine_rows": len(quar),
        "quarantine_by_stage": dict(Counter(q["stage"] for q in quar)),
        "rows_generated": 0,
    }
    gate_ok = bool(gate["pass"]) and gate["n_forms"] == len(adm) and all(reg.forms[f].unit_ok for f in adm)

    print(json.dumps({"dry_run": dry, "extract_files_checked": n_chk, "answers_per_read": n_answers,
                      "recorded_per_read": dict(n_rec), "form_status": dict(stat), "g_lex_gate": gate,
                      "g0_sha_ok": g0_sha == T.T30Plugin.G0_SHA256, "counts": counts,
                      "targets": rep, "shortfalls": short}, indent=1, ensure_ascii=False))
    if dry:
        return 0

    files = {
        "packs.json": js(packs),
        "skins.jsonl": jsonl(skins),
        "attack_lines.jsonl": jsonl(attacks),
        "wordings.jsonl": jsonl(wordings),
        "names.json": js(names),
        "lexicon.json": js(lex_obj),
        "quarantine.jsonl": jsonl(quar),
    }
    records = {"packs.json": len(packs), "skins.jsonl": len(skins), "attack_lines.jsonl": len(attacks),
               "wordings.jsonl": len(wordings), "names.json": sum(len(v) for v in names.values()),
               "lexicon.json": len(lex_obj["forms"]), "quarantine.jsonl": len(quar)}
    shas = write_pools(files)
    manifest = {
        "family": FAMILY,
        "tier": T.T30Plugin.TIER,
        "frozen_on": "2026-10-13",
        "g0_spec": {"path": "families/T30/G0_SPEC.md", "sha256": g0_sha,
                    "matches_plugin_G0_SHA256": g0_sha == T.T30Plugin.G0_SHA256},
        "g0_targets": G0,
        "inputs": {"authoring_answers": {f"answers/{x.name}": sha_file(x) for x in
                                         sorted((A.ROOT / "answers").glob("*.json"))},
                   "extraction_answers": ans_sha,
                   "extraction_reads": {label: b.batch_id for label, b in st["batches"]}},
        "code": {"pool_freeze.py": sha_file(Path(__file__).resolve()),
                 "authoring.py": sha_file(A.T.HERE / "authoring.py"),
                 "lex_extract.py": sha_file(A.T.HERE / "lex_extract.py"),
                 "plugin.py": sha_file(A.T.HERE / "plugin.py")},
        "a38_present": paths.a38_frozen(),
        "counts": counts,
        "targets": rep,
        "shortfalls": short,
        "g_lex_gate": gate,
        "pool_files": {rel: {"sha256": sha, "records": records[rel]} for rel, sha in shas.items()},
        "decisions": [
            "Extractor id per answer is haiku:<task id>; a form is admitted at 2 distinct agreeing extractors (2/2).",
            "An answer that is not one of the listed choices is not recorded (invalid read), so the form is pending.",
            "G3-H round trip is not applicable to T30 (Mode T, no extract_fields): 0 items.",
            "Held-out wordings: A.split_held, seeded 15% per form, minimum 3 (G0 3.4).",
            "T30 has no document kind, so no documents are frozen.",
        ],
    }
    manifest_text = js(manifest)
    paths.write_text(POOLS / "MANIFEST.json", manifest_text)
    print(json.dumps({"written": sorted(files) + ["MANIFEST.json"], "manifest_sha256": sha_text(manifest_text),
                      "gate_ok": gate_ok}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
