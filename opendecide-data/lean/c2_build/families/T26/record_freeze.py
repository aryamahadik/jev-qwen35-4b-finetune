"""c2_build/families/T26/record_freeze.py: the T26 admission and pool-freeze stage, run after the EXTRACTION answers came
back (workflow stage 6; G0_SPEC.md sections 3-4; C2_DATA_SPEC 6.3 G-LEX and G3-H; PREREG A37 (b) and A38).

What it does (after A38 only; every write goes through the kit's guarded writers):
  1. rebuilds the authoring and extraction batches in memory with the ingest's own functions, and checks them against
     the files on disk (TASKS.json, every key, chunk, prompt and manifest file, the lint log, the registry and the G3-H
     expected values). Any difference refuses the run;
  2. records every returned G-LEX read with reg.record_extraction (one extractor id per read, so the reads are
     independent) and scores every G3-H answer with g3h.compare against the orchestrator's expected values;
  3. admits each form by the G-LEX rule (reg.status: 2/2 for questions, 3/3 for precedence; any mismatch rejects it),
     quarantines every piece whose form is not admitted or whose document fails G3-H (a template under 98% is
     quarantined whole; a mismatched row is always dropped), and logs each reason;
  4. freezes the pools (packs, skins, attack lines, wordings, precedence paraphrases, lexicon, documents, quarantine)
     under families/T26/pools/ with a manifest: sha256 per file, counts per kind and register, admitted vs G0 target;
  5. writes the extraction record to haiku/extract/orchestrator/extraction_record.json (a new file; the ingest's own
     files are read, never rewritten).

  ../.venv/bin/python -m families.T26.record_freeze            (from lean/c2_build; writes)
  ../.venv/bin/python -m families.T26.record_freeze --check    (verifies and reports; writes nothing)

No label is set here. Golds come only from solver A and solver B (A37 b); Haiku extraction can only admit or drop a
form or a document, never set a label.
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
from c2_kit.lexicon import question_sem  # noqa: E402
from families.T26 import authoring_ingest as AI  # noqa: E402
from families.T26 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
EXTRACT = AI.EXTRACT
ORCH = AI.ORCH
POOLS = HERE / "pools"
G0 = HERE / "G0_SPEC.v1_1.md"      # the text the pools were authored and frozen under (G0_SPEC.md is v1.2)
PREREG = paths.PREREG

# G0-lite targets (G0_SPEC.md sections 1 S27, 4; C2_DATA_SPEC 3.0). Never lowered.
TARGET = {
    "packs_training": 25,
    "packs_heldout": 6,
    "skin_registers_training": 8,
    "skin_registers_heldout": 2,
    "wording_per_form": {"yn_apply": 9, "yn_hold": 6, "yn_not_apply": 4, "yn_dneg_apply": 2, "yn_fails": 6,
                         "yn_clears": 5, "ch_verdict": 16, "ch_failing": 6},
    "precedence_admitted": 6,
    "mode_f_max_share": 0.25,
    "g3h_template_pass": g3h.PASS_RATE,
}
HELD_OUT_SKIN_REGISTERS = ("it_chat", "forwarded_thread")
SKIN_POOLS = ("skin", "skin_heldout")
DOC_POOLS = ("freeform", "freeform_heldout")


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _answers_for(batch) -> dict:
    """{task_id: parsed answer} for every chunk of a batch whose answer file exists on disk."""
    raw = {}
    for c in batch.chunks:
        f = EXTRACT / batch.answer_path(c["task_id"])
        if f.exists():
            raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
    return raw


def _verify_files(batch, label: str) -> dict:
    """Every file the batch makes must already be on disk, byte for byte (chunks, prompt, key, manifest)."""
    files = batch.files()
    diffs = []
    for rel, text in sorted(files.items()):
        p = EXTRACT / rel
        if not p.exists():
            diffs.append(f"missing {rel}")
        elif p.read_text(encoding="utf-8") != text:
            diffs.append(f"differs {rel}")
    return {"batch": label, "files": len(files), "diffs": diffs}


def _task_rows(lex: list, g3, g3_name: str = "g3h-freeform") -> list:
    """The TASKS.json rows the ingest writes, rebuilt the same way (run() in authoring_ingest.py)."""
    rows = []
    for name, b in lex:
        for c in b.chunks:
            rows.append({"task_file": str(EXTRACT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                         "kind": b.kind, "pool": c["pool"], "batch_id": b.batch_id, "n_items": len(c["items"]),
                         "prompt_sha": b.prompt_sha})
    for c in g3.chunks:
        rows.append({"task_file": str(EXTRACT / g3.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                     "kind": g3.kind, "pool": c["pool"], "batch_id": g3.batch_id, "n_items": len(c["items"]),
                     "prompt_sha": g3.prompt_sha})
    return rows


def _entry(p: dict, stage: str, reasons: list) -> dict:
    return {"pool": p["pool"], "internal_id": p["internal_id"], "task_id": p["task_id"], "stage": stage,
            "reasons": reasons}


def _form_id(p: dict) -> str | None:
    """The registry id AI.build_registry gave a wording or precedence piece (sem + sha of the stripped text)."""
    text = AI._value(p).strip()
    sem = question_sem(FAMILY, p["meta"]["qform"]) if p["pool"] == "wording" else P.PREC_SEM
    fid = f"{sem}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"
    return fid


def record_reads(reg, lex: list) -> list:
    """Record each G-LEX read once per form (record_extraction). A form the read did not answer gets no record, so it
    stays pending. NONE and text that is not one of the batch's choices both record as no meaning (a mismatch)."""
    out = []
    for name, b in lex:
        kind = reg.forms[next(iter(b.key.values()))].kind
        got, probs = chunker.load_answers(b, _answers_for(b))
        stats = Counter()
        for fid in sorted(b.key.values()):
            if fid not in got:
                stats["unanswered"] += 1
                continue
            a = got[fid]
            m = a.get("meaning") if isinstance(a, dict) else None
            sem = reg.meaning_to_sem(kind, m) if isinstance(m, str) else None
            if sem is None:
                stats["NONE" if m == "NONE" else "not_a_choice"] += 1
            elif sem == reg.forms[fid].sem_id:
                stats["match"] += 1
            else:
                stats["other_meaning"] += 1
            reg.record_extraction(fid, name, sem)
        out.append({"read": name, "kind": kind, "batch_id": b.batch_id, "items": len(b.key),
                    "chunks": len(b.chunks), "answer_files": [b.answer_path(c["task_id"]) for c in b.chunks
                                                              if (EXTRACT / b.answer_path(c["task_id"])).exists()],
                    "outcomes": dict(sorted(stats.items())), "chunk_problems": probs})
    return out


def g3h_check(g3, expected: dict) -> tuple:
    """G3-H: score every freeform answer against the expected values; per-template pass rate (98% bar)."""
    got, probs = chunker.load_answers(g3, _answers_for(g3))
    results, detail = [], {}
    for iid in sorted(expected):
        m = AI._meta(iid)
        tmpl = f"{m['register']}|{m['tone']}"
        if iid not in got:
            ok, diffs = False, ["unanswered"]
        else:
            ok, diffs = g3h.compare(expected[iid], got[iid], AI.FIELDS_G3H)
        results.append((tmpl, iid, ok))
        detail[iid] = {"template": tmpl, "ok": ok, "diffs": diffs}
    rep = g3h.template_report(results)
    return rep, detail, probs


def run(write: bool) -> dict:
    # 1. authoring side: the ingest's own rebuild check, then the same pieces, lint, dedup and registry
    batches, tasks = AI.rebuild_and_check()
    pieces, coverage = AI.load_pieces(batches, tasks)
    AI.lint_all(pieces)
    AI.dedup_pass(pieces)
    AI.designate_held_out_packs(pieces)
    reg, added, refused = AI.build_registry(pieces)
    if refused:
        raise SystemExit(f"registry refused {len(refused)} form(s): refusing to freeze")

    checks = {}
    lint_log = json.loads((ORCH / "lint_log.json").read_text(encoding="utf-8"))
    checks["lint_log_coverage_matches"] = all(
        lint_log["coverage"][p]["answered"] == coverage[p]["answered"]
        and lint_log["coverage"][p]["missing_tasks"] == coverage[p]["missing_tasks"] for p in AI.POOLS)
    disk_reg = json.loads((ORCH / "registry.json").read_text(encoding="utf-8"))
    checks["registry_matches_disk"] = (
        {k: v["unit_ok"] for k, v in disk_reg["lex_status"].items()} == {f: x.unit_ok for f, x in reg.forms.items()})

    # 2. extraction side: rebuild the G-LEX reads and the G3-H task exactly as the ingest did
    surv = [p for p in pieces if not p["problems"]]
    fids_by_kind = {"question": [], "precedence": []}
    for fid, f in reg.forms.items():
        if f.unit_ok:
            fids_by_kind["question" if f.kind == "question" else "precedence"].append(fid)
    checks["forms_needing_admission_match_disk"] = disk_reg["forms_needing_admission"] == fids_by_kind
    lex = AI.lex_batches(reg, fids_by_kind)
    freeform_ok = [p for p in surv if p["pool"] in DOC_POOLS]
    g3, g3_expected = AI.g3h_batch(freeform_ok)
    verify = [_verify_files(b, name) for name, b in lex] + [_verify_files(g3, "g3h-freeform")]
    checks["extraction_files_match_disk"] = all(not v["diffs"] for v in verify)
    tasks_disk = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    checks["extraction_tasks_match_disk"] = _task_rows(lex, g3) == tasks_disk["tasks"]
    checks["g3h_expected_matches_disk"] = (
        json.loads((ORCH / "g3h_expected.json").read_text(encoding="utf-8")) == g3_expected)
    bad = [k for k, v in checks.items() if not v]
    if bad:
        raise SystemExit(f"on-disk state differs from the rebuild {bad}: refusing to record or freeze")

    # 3. G-LEX reads, then the G3-H check
    reads = record_reads(reg, lex)
    g3_rep, g3_detail, g3_probs = g3h_check(g3, g3_expected)
    drop_rows = set(g3_rep["drop_rows"])

    # 4. admission by the G-LEX rule, and quarantine
    status = {fid: reg.status(fid) for fid in sorted(reg.forms)}      # every form, incl. the unit failures
    admitted_ids = {fid for fid, s in status.items() if s == "admitted"}
    gate_all = reg.gate(used_form_ids=list(status))                    # G-LEX over every form in the registry
    gate_used = reg.gate(used_form_ids=sorted(admitted_ids))           # G-LEX over the forms the pool uses
    quarantine = [_entry(p, "lint/dedup", p["problems"]) for p in pieces if p["problems"]]
    kept = defaultdict(list)
    for p in surv:
        pool = p["pool"]
        iid = p["internal_id"]
        if pool == "pack":
            cp, label = AI._value(p)
            kept["pack"].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                 "held_out": bool(p.get("held_out")), "counterparty": cp, "domain_label": label})
        elif pool in SKIN_POOLS:
            kept[pool].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                               "held_out": pool == "skin_heldout", "register": p["meta"]["register"],
                               "tone": p["meta"]["tone"], "text": AI._value(p)})
        elif pool == "attack":
            kept["attack"].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                   "slot": p["item"]["slots"][0].strip("{}"), "text": AI._value(p)})
        elif pool in ("wording", "precedence"):
            fid = _form_id(p)
            if fid not in reg.forms:
                quarantine.append(_entry(p, "G-LEX", ["no registry form for this piece"]))
            elif status.get(fid) != "admitted":
                quarantine.append(_entry(p, "G-LEX", [
                    f"form {fid} is {status.get(fid, reg.status(fid))}",
                    f"expected sem {reg.forms[fid].sem_id}",
                    f"reads (extractor, sem or None): {[list(e) for e in reg.forms[fid].extractions]}"]))
            else:
                row = {"form_id": fid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"], "text": AI._value(p).strip(),
                       "sem_id": reg.forms[fid].sem_id, "extractions": [list(e) for e in reg.forms[fid].extractions]}
                if pool == "wording":
                    row["qform"] = p["meta"]["qform"]
                kept[pool].append(row)
        elif pool in DOC_POOLS:
            d = g3_detail[iid]
            if iid in drop_rows or not d["ok"]:
                why = d["diffs"] or ["G3-H failed"]
                if d["template"] in g3_rep["quarantined"]:
                    why = why + [f"template {d['template']} quarantined (G3-H under {g3h.PASS_RATE:.0%})"]
                quarantine.append(_entry(p, "G3-H", why))
            else:
                m = AI._meta(iid)
                kept["freeform"].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                         "held_out": pool == "freeform_heldout", "register": m["register"],
                                         "tone": m["tone"], "text": AI._value(p), "facts": p["item"]["facts"]})
        else:
            raise SystemExit(f"unknown pool {pool}")

    # 5. counts and targets
    skins_train = [s for s in kept["skin"]]
    skins_ho = [s for s in kept["skin_heldout"]]
    train_regs = sorted({s["register"] for s in skins_train})
    ho_regs = sorted({s["register"] for s in skins_ho})
    wording_counts = Counter(w["qform"] for w in kept["wording"])
    mode_t = len(skins_train) + len(skins_ho) + len(kept["attack"])
    mode_f = len(kept["freeform"])
    shortfalls = []

    def tgt(name, bar, got, note=""):
        if got < bar:
            shortfalls.append({"target": name, "bar": bar, "got": got, "short_by": bar - got, "note": note})
        return {"bar": bar, "got": got, "pass": got >= bar}

    targets = {
        "packs_training": tgt("packs training", TARGET["packs_training"],
                              sum(1 for x in kept["pack"] if not x["held_out"])),
        "packs_heldout": tgt("packs held-out", TARGET["packs_heldout"],
                             sum(1 for x in kept["pack"] if x["held_out"])),
        "skin_registers_training": tgt("skin registers (training)", TARGET["skin_registers_training"], len(train_regs),
                                       f"registers with kept skins: {train_regs}"),
        "skin_registers_heldout": tgt("skin registers (held-out)", TARGET["skin_registers_heldout"], len(ho_regs),
                                      f"registers with kept held-out skins: {ho_regs}"),
        "precedence_admitted": tgt("precedence paraphrases admitted 3/3", TARGET["precedence_admitted"],
                                   len(kept["precedence"])),
    }
    wording_targets = {}
    for qf, bar in TARGET["wording_per_form"].items():
        wording_targets[qf] = tgt(f"wording {qf}", bar, wording_counts.get(qf, 0))
    targets["wording_total"] = tgt("wording total (sum of per-form bars)", sum(TARGET["wording_per_form"].values()),
                                   len(kept["wording"]))
    if not any(x.get("held_out") for x in kept["wording"]):
        shortfalls.append({"target": "held-out wordings for sampler S5", "bar": None, "got": 0, "short_by": None,
                           "note": "G0 section 4 asks for held-out wordings; none were authored in the authoring pass"})
    f_share = mode_f / (mode_t + mode_f) if (mode_t + mode_f) else 0.0
    if f_share > TARGET["mode_f_max_share"]:
        shortfalls.append({"target": "Mode F share (of pieces)", "bar": TARGET["mode_f_max_share"],
                           "got": round(f_share, 4), "short_by": None,
                           "note": "over the cap on pieces; the row builder must cap Mode F rows at 25%"})

    lex_counts = Counter(status.values())
    # quarantine by stage and reason
    qstage = Counter(q["stage"] for q in quarantine)

    # 6. the files to freeze
    doc = {}
    doc["packs.json"] = {"family": FAMILY, "pool": "pack", "count": len(kept["pack"]), "items": kept["pack"]}
    doc["skins.json"] = {"family": FAMILY, "pool": "skin", "count": len(skins_train) + len(skins_ho),
                         "items": skins_train + skins_ho}
    doc["attack.json"] = {"family": FAMILY, "pool": "attack", "count": len(kept["attack"]), "items": kept["attack"]}
    doc["wordings.json"] = {"family": FAMILY, "pool": "wording", "count": len(kept["wording"]),
                            "items": kept["wording"]}
    doc["precedence.json"] = {"family": FAMILY, "pool": "precedence", "count": len(kept["precedence"]),
                              "items": kept["precedence"]}
    lex_json = reg.to_json()
    lex_json["forms"] = [f for f in lex_json["forms"] if f["form_id"] in admitted_ids]
    lex_json["not_admitted"] = {fid: s for fid, s in sorted(status.items()) if s != "admitted"}
    lex_json["admitted_form_ids"] = sorted(admitted_ids)
    doc["lexicon.json"] = {"family": FAMILY, "pool": "lexicon", "count": len(admitted_ids), "registry": lex_json}
    doc["documents.json"] = {"family": FAMILY, "pool": "freeform", "count": len(kept["freeform"]),
                             "items": kept["freeform"]}
    doc["quarantine.json"] = {"family": FAMILY, "count": len(quarantine), "items": quarantine,
                              "g3h": {"gate": "G3-H", "bar": g3h.PASS_RATE, "templates": g3_rep["templates"],
                                      "quarantined": g3_rep["quarantined"]},
                              "reads": reads}

    texts = {rel: json.dumps(obj, ensure_ascii=False, indent=1) + "\n" for rel, obj in doc.items()}
    file_rows = {rel: {"sha256": _sha_text(t), "bytes": len(t.encode("utf-8")), "count": doc[rel]["count"]}
                 for rel, t in texts.items()}

    counts = {
        "packs": {"training": targets["packs_training"]["got"], "held_out": targets["packs_heldout"]["got"]},
        "skins": {"training_by_register": dict(Counter(s["register"] for s in skins_train)),
                  "training_by_register_tone": {f"{r}|{t}": n for (r, t), n in sorted(Counter(
                      (s["register"], s["tone"]) for s in skins_train).items())},
                  "held_out_by_register": dict(Counter(s["register"] for s in skins_ho))},
        "attack": {"kept": len(kept["attack"]), "by_slot": dict(Counter(a["slot"] for a in kept["attack"]))},
        "wordings": {"admitted_by_qform": dict(sorted(wording_counts.items())), "total": len(kept["wording"]),
                     "held_out": 0},
        "precedence": {"admitted": len(kept["precedence"])},
        "lexicon": {"forms": len(reg.forms), "status": dict(sorted(lex_counts.items()))},
        "documents": {"kept_by_register": dict(Counter(d["register"] for d in kept["freeform"])),
                      "held_out": sum(1 for d in kept["freeform"] if d["held_out"]),
                      "training": sum(1 for d in kept["freeform"] if not d["held_out"])},
        "mode_pieces": {"T": mode_t, "F": mode_f, "F_share": round(f_share, 4)},
        "quarantine": {"total": len(quarantine), "by_stage": dict(qstage)},
        "authoring_coverage": {p: {"items": coverage[p]["items"], "answered": coverage[p]["answered"],
                                   "missing_tasks": coverage[p]["missing_tasks"]} for p in AI.POOLS},
        "extraction": {"tasks_returned": len(tasks_disk["tasks"]) - sum(
            1 for t in tasks_disk["tasks"] if not (EXTRACT / "answers" / f"{Path(t['task_file']).stem}.json").exists()),
            "tasks_total": len(tasks_disk["tasks"])},
    }
    record = {"family": FAMILY, "checks": checks, "reads": reads, "g3h": {k: v for k, v in g3_rep.items()
                                                                          if k != "drop_rows"},
              "g3h_drop_rows": sorted(drop_rows), "g3h_problems": g3_probs,
              "status_counts": dict(lex_counts),
              "gate_G-LEX": {"all_forms": {k: v for k, v in gate_all.items() if k != "not_admitted"},
                             "all_forms_not_admitted": gate_all["not_admitted"],
                             "used_forms": {k: v for k, v in gate_used.items() if k != "not_admitted"}}}

    summary = {"write": write, "checks": checks, "counts": counts, "targets": targets,
               "wording_targets": wording_targets, "shortfalls": shortfalls,
               "g0_sha256": _sha_text(G0.read_text(encoding="utf-8")),
               "g0_pinned": P.T26Plugin.G0_SHA256,
               "a38_frozen": paths.a38_frozen(PREREG.read_text(encoding="utf-8")),
               "files": file_rows}
    if not write:
        return summary

    # 7. write: the extraction record (new file), the pools and the manifest (guarded writers)
    paths.write_json(ORCH / "extraction_record.json", record)
    paths.write_files(POOLS, texts)
    manifest = {"family": FAMILY, "stage": "admit+freeze (workflow stage 6)", "pool_files": file_rows,
                "g0_spec_sha256": summary["g0_sha256"], "g0_pinned_in_plugin": P.T26Plugin.G0_SHA256,
                "counts": counts, "targets": targets, "wording_targets": wording_targets,
                "shortfalls": shortfalls, "checks": checks,
                "sources": {"extraction_answers": {p.name: _sha_text(p.read_text(encoding="utf-8")) for p in sorted(
                    (EXTRACT / "answers").glob("*.json"))},
                    "authoring_answers_used": {p.name: _sha_text(p.read_text(encoding="utf-8")) for p in sorted(
                        (AI.ROOT / "answers").glob("*.json"))}},
                "extraction_record": "haiku/extract/orchestrator/extraction_record.json",
                "not_verified": ["file-access audit (c2_kit.audit) of the 12 extraction agents: needs their transcripts, "
                                 "not opened by this stage"]}
    paths.write_files(POOLS, {"manifest.json": json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"})
    summary["manifest"] = str(POOLS / "manifest.json")
    return summary


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    write = "--check" not in argv
    out = run(write)
    print(json.dumps(out, indent=1, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
