"""families/T24/pool_freeze.py: record the T24 extraction answers (G-LEX, G3-H), admit or quarantine every form, wording and
document, and freeze the T24 pools with a manifest (C2_DATA_SPEC 6.2 item 4; G0_SPEC sections 2-3). A new file. It
generates no rows.

  rebuild()  the extract stage's lint, dedup, registry and read batches, in memory (the same calls as
             extract_stage.main, which wrote haiku/extract/). Nothing is written.
  check      the on-disk chunks, prompts, manifests and keys of haiku/extract/, and the lint log and pre-extraction
             registry, are the same as the rebuild, so every answer's qid maps to the same form or document. Any
             difference stops the run before anything is recorded or written.
  record     G-LEX: each valid answer is one extraction by its task ("haiku:<task id>", reg.record_extraction). An
             answer that is not one of the listed meanings is an invalid read: it is not recorded and is quarantined
             (the form stays pending). G3-H: g3h.compare on each document's customer name; a mismatched document is
             dropped, and a register whose documents match < 98% is quarantined (g3h.template_report).
  freeze     pools/ (packs.json, skins.jsonl, documents.jsonl, wordings.jsonl, lexicon.json, quarantine.jsonl) and
             pools/MANIFEST.json (sha256 of every pool file, counts per kind and register, admitted vs the G0 targets,
             every shortfall). The G0 targets are constants below and are not lowered.

Run (from lean/c2_build):  ../../.venv/bin/python -I families/T24/pool_freeze.py --dry-run   (computes and prints only)
                           ../../.venv/bin/python -I families/T24/pool_freeze.py             (writes)
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, lexicon, paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T24 import authoring as A  # noqa: E402
from families.T24 import extract_stage as X  # noqa: E402
from families.T24 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
EXTRACT = X.OUT                                  # haiku/extract (the answers and the batch files)
POOLS = HERE / "pools"
RECORDED = EXTRACT / "recorded.json"
PACK_SPLIT_SEED = "t24-pack-split-v1"            # the seeded split of the admitted packs (G0 3.4)
PACK_HELD = 4                                    # G0 3.4: 4 held-out packs
FROZEN_ON = "2026-10-13"
GLEX_READS = ("glex-read1", "glex-read2", "glex-read3")

# G0 targets (families/T24/G0_SPEC.md v2, sections 2-3). Not lowered. A target with no number in G0 is report-only.
G0 = {
    "packs_training_min": 32,                    # 3.4: >= 32 training packs
    "packs_held_out": 4,                         # 3.4: 4 held out
    "skin_training_registers_min": 8,            # 3.2: >= 8 registers (memo ... form)
    "skin_held_out_registers": 2,                # 3.2: held out: transcript, voicemail
    "wording_admitted_min": {"ch_v2": 40, "yn_changes": 16, "yn_same": 8, "yn_not_change": 8,
                             "yn_fail_change": 8, "yn_dneg": 6},            # 3.3 admission targets
    "wording_card_min": 5,                       # 3.3: each card's rows use >= 5 wordings (training)
    "wording_held_card_min": 5,                  # DERIVED from 3.3 for the S5 cards (no held-out number in G0)
    "clause_per_meaning_min": 6,                 # 3.1: >= 6 admitted per meaning (3/3 for win, ovc, ovd)
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
    """The lint, dedup, registry and read batches, deterministic from the authoring answers (nothing written).
    The same calls, in the same order, as extract_stage.main."""
    pools, load_probs = A.load(A.ROOT)
    if load_probs:
        raise SystemExit(f"STOP: authoring answers are incomplete: {load_probs[:8]}")
    log: list = []

    def drop(pool, p, reason):
        log.append({"pool": pool, "task_id": p["task_id"], "iid": p["iid"], "reason": reason})

    kept = {"packs": [], "skins": [], "freeform": [], "forms": [], "wordings": []}

    seen_pre, seen_title = set(), set()
    for p in pools.get("packs", []):
        dom, probs = A.check_pack(p["pack"])
        if not probs:
            pre, title = dom.prefix.upper(), X.norm(dom.title)
            if pre in seen_pre:
                probs = [f"duplicate prefix {pre}"]
            elif title in seen_title:
                probs = ["duplicate title"]
        if probs:
            drop("packs", p, "; ".join(probs))
            continue
        seen_pre.add(pre)
        seen_title.add(title)
        kept["packs"].append(dict(p, pool="packs"))

    seen = set()
    for p in pools.get("skins", []):
        probs = A.check_skin(p["text"], p["register"], p["slots"], held_out=p["held_out"]) + X.skin_rule_problems(p["text"])
        if not probs and X.norm(p["text"]) in seen:
            probs = ["duplicate text"]
        if probs:
            drop("skins", p, "; ".join(probs))
            continue
        seen.add(X.norm(p["text"]))
        kept["skins"].append(dict(p, pool="skins"))

    seen = set()
    for p in pools.get("freeform", []):
        probs = A.check_freeform(p["text"], p["customer"]) + X.freeform_rule_problems(p["text"], p["customer"])
        if not probs and X.norm(p["text"]) in seen:
            probs = ["duplicate text"]
        if probs:
            drop("freeform", p, "; ".join(probs))
            continue
        seen.add(X.norm(p["text"]))
        kept["freeform"].append(dict(p, pool="freeform"))

    seen = set()
    for pool in ("lexicon:window", "lexicon:comparator", "lexicon:other"):
        for p in pools.get(pool, []):
            probs = A.check_form(p["text"], p["sem"]) + X.form_rule_problems(p["text"])
            if not probs and X.norm(p["text"]) in seen:
                probs = ["duplicate form text"]
            if probs:
                drop(pool, p, "; ".join(probs))
                continue
            seen.add(X.norm(p["text"]))
            kept["forms"].append(dict(p, pool=pool))

    seen = set()
    for p in pools.get("wordings", []):
        probs = A.check_wording(p["text"], p["qform"]) + X.wording_rule_problems(p["text"])
        if not probs and X.norm(p["text"]) in seen:
            probs = ["duplicate wording"]
        if probs:
            drop("wordings", p, "; ".join(probs))
            continue
        seen.add(X.norm(p["text"]))
        kept["wordings"].append(dict(p, pool="wordings"))

    reg, _by_fid, forms, wordings = X.admit_filter(kept["forms"], kept["wordings"], drop)
    kept["forms"], kept["wordings"] = forms, wordings

    fids = sorted(reg.forms)
    plan = {1: fids, 2: fids, 3: [f for f in fids if reg.forms[f].kind in lexicon.STRICT_KINDS]}
    batches = []
    for r, fl in plan.items():
        items = reg.lexicon_items(fl, seed=f"t24-glex-{X.VERSION}-read{r}")
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"t24-glex-{X.VERSION}-read{r}",
                               prompt=X.GLEX_PROMPT)
        batches.append((f"glex-read{r}", b))
    fields = P.T24Plugin().extract_fields(None)
    g3_items = [(p["iid"], g3h.extraction_item(p["text"], fields)) for p in kept["freeform"]]
    b3 = chunker.make_batch("extract_g3h", FAMILY, g3_items, seed=f"t24-g3h-{X.VERSION}-free", prompt=X.G3H_PROMPT)
    batches.append(("g3h-free", b3))
    return {"pools": pools, "log": log, "kept": kept, "reg": reg, "batches": batches, "fields": fields}


def check_on_disk(st: dict) -> tuple:
    """(files compared, mismatching paths). Prompts, chunks, manifests and keys must be the same bytes as the rebuild;
    the lint log and the pre-extraction registry must match what the extract stage wrote."""
    checked, bad = 0, set()
    for _label, b in st["batches"]:
        for rel, text in b.files().items():
            if not rel.startswith(("chunks/", "prompts/", "manifest/", "key/")):
                continue
            checked += 1
            p = EXTRACT / rel
            if not p.is_file() or p.read_text(encoding="utf-8") != text:
                bad.add(rel)
    lint = json.loads((EXTRACT / "LINT_LOG.json").read_text(encoding="utf-8"))
    if lint["dropped"] != st["log"]:
        bad.add("LINT_LOG.json (dropped list)")
    reg_disk = json.loads((EXTRACT / "registry_pre_glex.json").read_text(encoding="utf-8"))
    if reg_disk != st["reg"].to_json():
        bad.add("registry_pre_glex.json")
    return checked, sorted(bad)


# ================================================================================================ load answers
def load_reads(batches: list) -> tuple:
    """({read label: {"batch", "answers": {internal id: answer}}}, problems, {answer path: sha256})."""
    reads, problems, shas = {}, [], {}
    for label, b in batches:
        raw = {}
        for c in b.chunks:
            tid = c["task_id"]
            p = EXTRACT / b.answer_path(tid)
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


# ================================================================================================ record
def record(st: dict, reads: dict) -> tuple:
    """G-LEX: record every valid meaning as one extraction. G3-H: compare every document. Returns
    (invalid entries, counts recorded per read, the G3-H template report, {doc iid: answer})."""
    reg = st["reg"]
    invalid, n_rec = [], Counter()
    for label in GLEX_READS:
        rd = reads[label]
        b = rd["batch"]
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        for fid in sorted(rd["answers"]):
            ans = rd["answers"][fid]
            meaning = ans.get("meaning") if isinstance(ans, dict) else None
            sem = reg.meaning_to_sem(reg.forms[fid].kind, meaning) if isinstance(meaning, str) else None
            if sem is None:
                invalid.append({"stage": "g-lex", "task": label, "iid": fid, "task_id": task_of[fid],
                                "reason": f"meaning is not one of the listed choices: {str(meaning)[:160]!r}"})
                continue
            reg.record_extraction(fid, f"haiku:{task_of[fid]}", sem)
            n_rec[label] += 1

    rd = reads["g3h-free"]
    docs = {p["iid"]: p for p in st["kept"]["freeform"]}
    results, answers, diffs_of = [], {}, {}
    for iid in sorted(docs):
        p = docs[iid]
        ans = rd["answers"].get(iid)
        answers[iid] = ans
        ok, diffs = g3h.compare({"customer": p["customer"]}, ans if isinstance(ans, dict) else {}, st["fields"])
        diffs_of[iid] = diffs
        results.append((p["register"], iid, ok))
    rep = g3h.template_report(results)
    quarantined = set(rep["quarantined"])
    for iid in sorted(docs):
        p = docs[iid]
        if iid in rep["drop_rows"]:
            why = []
            if diffs_of[iid]:
                why.append("; ".join(diffs_of[iid]))
            if p["register"] in quarantined:
                why.append(f"register {p['register']} below {int(g3h.PASS_RATE * 100)}% G3-H "
                            f"({rep['templates'][p['register']]['ok']}/{rep['templates'][p['register']]['n']})")
            invalid.append({"stage": "g3h", "task": "g3h-free", "iid": iid, "task_id": p["task_id"],
                            "reason": "; ".join(why)})
    return invalid, n_rec, rep, answers


def recorded_view(st: dict, reads: dict, answers: dict, rep: dict) -> dict:
    reg = st["reg"]
    seen = defaultdict(list)
    for label in GLEX_READS:
        rd = reads[label]
        b = rd["batch"]
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        for fid, ans in rd["answers"].items():
            seen[fid].append({"read": label, "task_id": task_of[fid],
                              "meaning": ans.get("meaning") if isinstance(ans, dict) else None})
    forms = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        forms.append({"form_id": fid, "kind": f.kind, "sem_id": f.sem_id, "text": f.text,
                      "status": reg.status(fid), "haiku_task_id": f.haiku_task_id,
                      "extractions": [{"extractor": e, "sem_id": s} for e, s in f.extractions],
                      "reads": sorted(seen.get(fid, []), key=lambda r: r["read"])})
    docs = []
    by_doc = {p["iid"]: p for p in st["kept"]["freeform"]}
    for iid in sorted(by_doc):
        a = answers.get(iid)
        docs.append({"iid": iid, "register": by_doc[iid]["register"], "task_id": by_doc[iid]["task_id"],
                     "extracted_customer": a.get("customer") if isinstance(a, dict) else None,
                     "generator_customer": by_doc[iid]["customer"]})
    return {"family": FAMILY, "g3h_templates": rep["templates"], "forms": forms, "documents": docs}


# ================================================================================================ freeze
def freeze_packs(kept: dict) -> list:
    ranked = sorted(kept["packs"], key=lambda p: sha_text(f"{PACK_SPLIT_SEED}|{p['iid']}"))
    held = {p["iid"] for p in ranked[:PACK_HELD]}
    out = []
    for p in sorted(kept["packs"], key=lambda p: p["iid"]):
        pack = p["pack"]
        out.append({"pool_id": p["iid"], "held_out": p["iid"] in held, "task_id": p["task_id"],
                    "prefix": pack["prefix"], "title": pack["title"], "pack_sha256": sha_obj(pack), "pack": pack})
    return out


def freeze_skins(kept: dict) -> list:
    out = []
    for p in sorted(kept["skins"], key=lambda p: p["iid"]):
        reg = p["register"]
        text = p["text"]
        out.append({"skin_id": f"SK-T24-{reg.upper()}-{sha_text(text)[:8]}", "pool_id": p["iid"], "register": reg,
                    "slots": list(p["slots"]), "escape": A.ESCAPE.get(reg, "text"), "held_out": bool(p["held_out"]),
                    "task_id": p["task_id"], "text_sha256": sha_text(text), "text": text})
    dup = [k for k, v in Counter(s["skin_id"] for s in out).items() if v > 1]
    if dup:
        raise RuntimeError(f"skin ids collide: {dup[:3]}")
    return out


def freeze_documents(kept: dict, dropped: set) -> list:
    out = []
    for p in sorted(kept["freeform"], key=lambda p: p["iid"]):
        if p["iid"] in dropped:
            continue
        text = p["text"]
        out.append({"doc_id": f"DOC-T24-{p['register'].upper()}-{sha_text(text)[:8]}", "pool_id": p["iid"],
                    "register": p["register"], "held_out": bool(p["held_out"]), "customer": p["customer"],
                    "task_id": p["task_id"], "g3h": "match", "text_sha256": sha_text(text), "text": text})
    dup = [k for k, v in Counter(d["doc_id"] for d in out).items() if v > 1]
    if dup:
        raise RuntimeError(f"document ids collide: {dup[:3]}")
    return out


def freeze_wordings(reg) -> list:
    out = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        if f.kind != "question" or reg.status(fid) != "admitted":
            continue
        out.append({"form_id": fid, "qform": qform_of(f.sem_id), "sem_id": f.sem_id, "text": f.text,
                    "held_out": bool(f.held_out), "status": "admitted", "haiku_task_id": f.haiku_task_id,
                    "haiku_prompt_sha": f.haiku_prompt_sha,
                    "extractions": [{"extractor": e, "sem_id": s} for e, s in f.extractions],
                    "text_sha256": sha_text(f.text)})
    return out


def freeze_lexicon(reg) -> tuple:
    obj = reg.to_json()
    obj["forms"] = [x for x in obj["forms"] if x["status"] == "admitted"]
    chk = LexiconRegistry.from_json(obj)            # re-runs the unit tests and the extraction status on the pool
    return obj, chk.gate()


def quarantine_rows(log: list, reg, invalid: list) -> list:
    out = [{"stage": "lint", "pool": d["pool"], "task": d["task_id"], "iid": d["iid"], "reason": d["reason"]}
           for d in log]
    out += invalid
    for fid in sorted(reg.forms):
        st_ = reg.status(fid)
        if st_ != "admitted":
            f = reg.forms[fid]
            out.append({"stage": "g-lex", "pool": "question" if f.kind == "question" else "clause",
                        "task": f.haiku_task_id, "iid": fid,
                        "reason": f"{st_}: extractions {[[e, s] for e, s in f.extractions]} "
                                  f"(needs {f.required} agreeing extractors, sem {f.sem_id})"})
    return out


# ================================================================================================ targets
def targets(packs, skins, docs, wordings, reg) -> tuple:
    """(report rows, shortfalls). Each row: item, got, target, op, met, note. A target is never lowered; a row with
    target None is report-only (G0 gives no number)."""
    rows = []

    def add(item, got, target, op, note=""):
        met = None if target is None else (got >= target if op == ">=" else got == target)
        rows.append({"item": item, "got": got, "target": target, "op": op, "met": met, "note": note})

    tr = [p for p in packs if not p["held_out"]]
    ho = [p for p in packs if p["held_out"]]
    add("training packs", len(tr), G0["packs_training_min"], ">=", "G0 3.4: >= 32 training packs")
    add("held-out packs", len(ho), G0["packs_held_out"], "==", "G0 3.4: 4 held out")

    tr_s = [s for s in skins if not s["held_out"]]
    ho_s = [s for s in skins if s["held_out"]]
    add("training skin registers covered", len({s["register"] for s in tr_s}), G0["skin_training_registers_min"], ">=",
        "G0 3.2: >= 8 registers")
    add("held-out skin registers covered", len({s["register"] for s in ho_s}), G0["skin_held_out_registers"], "==",
        "G0 3.2: transcript, voicemail")
    add("training skins (all registers)", len(tr_s), None, ">=", "report only: G0 states no skin count")
    add("held-out skins (all registers)", len(ho_s), None, ">=", "report only: G0 states no skin count")

    adm_tr, adm_ho = Counter(), Counter()
    for w in wordings:
        (adm_ho if w["held_out"] else adm_tr)[w["qform"]] += 1
    for q, t in G0["wording_admitted_min"].items():
        add(f"admitted training wordings {q}", adm_tr[q], t, ">=", "G0 3.3 admission target")
    add("training wordings, lowest form (card use)", min(adm_tr[q] for q in G0["wording_admitted_min"]),
        G0["wording_card_min"], ">=", "G0 3.3: each card's rows use >= 5")
    for q in G0["wording_admitted_min"]:
        add(f"admitted held-out wordings {q}", adm_ho[q], G0["wording_held_card_min"], ">=",
            "DERIVED floor (G0 3.3 gives no held-out number; S5 cards use >= 5 each)")

    clause = Counter(f.sem_id for f in reg.forms.values()
                     if f.kind != "question" and reg.status(f.form_id) == "admitted")
    for s in sorted(reg.sems.values(), key=lambda s: s.sem_id):
        if s.kind == "question":
            continue
        strict = s.kind in lexicon.STRICT_KINDS
        add(f"admitted clause forms {s.sem_id}", clause[s.sem_id], G0["clause_per_meaning_min"], ">=",
            "G0 3.1: >= 6 per meaning; 3/3 (window kind)" if strict else "G0 3.1: >= 6 per meaning; 2/2")

    add("Mode F documents kept", len(docs), None, ">=", "report only: G0 caps Mode F at 25% of rows, no count")
    short = [r for r in rows if r["met"] is False]
    return rows, short


# ================================================================================================ write
def write_pools(files: dict) -> dict:
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

    n_chk, bad = check_on_disk(st)
    if bad:
        raise SystemExit(f"STOP: rebuilt extraction files differ from disk ({len(bad)}): {bad[:6]}")
    reads, probs, ans_sha = load_reads(st["batches"])
    if probs:
        raise SystemExit(f"STOP: extraction answers are incomplete or invalid: {probs[:8]}")
    n_answers = {label: len(rd["answers"]) for label, rd in reads.items()}

    invalid, n_rec, g3_rep, g3_answers = record(st, reads)
    g3_drop = {r["iid"] for r in invalid if r["stage"] == "g3h"}
    stat = Counter(reg.status(fid) for fid in reg.forms)

    packs = freeze_packs(st["kept"])
    skins = freeze_skins(st["kept"])
    docs = freeze_documents(st["kept"], g3_drop)
    wordings = freeze_wordings(reg)
    lex_obj, gate = freeze_lexicon(reg)
    quar = quarantine_rows(st["log"], reg, invalid)
    rep, short = targets(packs, skins, docs, wordings, reg)
    g0_file_sha = sha_file(HERE / "G0_SPEC.md")

    adm_by_form = Counter(w["qform"] for w in wordings)
    adm_tr = Counter(w["qform"] for w in wordings if not w["held_out"])
    adm_ho = Counter(w["qform"] for w in wordings if w["held_out"])
    clause_adm = Counter(f.sem_id for f in reg.forms.values() if f.kind != "question" and reg.status(f.form_id) == "admitted")
    counts = {
        "authored_pieces_in": {k: len(v) for k, v in A.load(A.ROOT)[0].items()},
        "lint_dropped_total": len(st["log"]),
        "lint_dropped_by_pool": dict(Counter(d["pool"] for d in st["log"])),
        "packs_frozen": {"training": sum(1 for p in packs if not p["held_out"]),
                         "held_out": sum(1 for p in packs if p["held_out"])},
        "skins_frozen_by_register": dict(sorted(Counter(s["register"] for s in skins).items())),
        "skins_frozen_training": sum(1 for s in skins if not s["held_out"]),
        "skins_frozen_held_out": sum(1 for s in skins if s["held_out"]),
        "documents_frozen_by_register": dict(sorted(Counter(d["register"] for d in docs).items())),
        "documents_frozen_training": sum(1 for d in docs if not d["held_out"]),
        "documents_frozen_held_out": sum(1 for d in docs if d["held_out"]),
        "documents_dropped_g3h": len(g3_drop),
        "g3h_registers_quarantined": g3_rep["quarantined"],
        "wordings_admitted_by_form": dict(sorted(adm_by_form.items())),
        "wordings_admitted_training_by_form": dict(sorted(adm_tr.items())),
        "wordings_admitted_held_out_by_form": dict(sorted(adm_ho.items())),
        "clause_forms_admitted_by_meaning": dict(sorted(clause_adm.items())),
        "lexicon_forms_frozen": len(lex_obj["forms"]),
        "g_lex_status_after_record": dict(stat),
        "g_lex_recorded_per_read": dict(n_rec),
        "answers_per_read": n_answers,
        "invalid_or_quarantined_reads": len(invalid),
        "quarantine_rows": len(quar),
        "quarantine_by_stage": dict(Counter(q["stage"] for q in quar)),
        "rows_generated": 0,
    }
    gate_ok = bool(gate["pass"]) and gate["n_forms"] == len(lex_obj["forms"])
    print(json.dumps({"dry_run": dry, "extract_files_checked": n_chk, "answers_per_read": n_answers,
                      "recorded_per_read": dict(n_rec), "g_lex_gate": gate, "gate_ok": gate_ok,
                      "g0_file_sha_matches_plugin": g0_file_sha == P.T24Plugin.G0_SHA256,
                      "g3h_quarantined_registers": g3_rep["quarantined"],
                      "g3h_templates": g3_rep["templates"], "counts": counts,
                      "targets": rep, "shortfalls": short}, indent=1, ensure_ascii=False, default=str))
    if dry:
        return 0

    paths.write_json(RECORDED, recorded_view(st, reads, g3_answers, g3_rep))
    files = {
        "packs.json": js(packs),
        "skins.jsonl": jsonl(skins),
        "documents.jsonl": jsonl(docs),
        "wordings.jsonl": jsonl(wordings),
        "lexicon.json": js(lex_obj),
        "quarantine.jsonl": jsonl(quar),
    }
    records = {"packs.json": len(packs), "skins.jsonl": len(skins), "documents.jsonl": len(docs),
               "wordings.jsonl": len(wordings), "lexicon.json": len(lex_obj["forms"]), "quarantine.jsonl": len(quar)}
    shas = write_pools(files)
    manifest = {
        "family": FAMILY,
        "tier": P.T24Plugin.TIER,
        "frozen_on": FROZEN_ON,
        "g0_spec": {"path": "families/T24/G0_SPEC.md", "sha256": g0_file_sha,
                    "matches_plugin_G0_SHA256": g0_file_sha == P.T24Plugin.G0_SHA256},
        "g0_targets": G0,
        "inputs": {"authoring_answers": {f"haiku/author/answers/{x.name}": sha_file(x) for x in
                                         sorted((A.ROOT / "answers").glob("*.json"))},
                   "extraction_answers": ans_sha,
                   "extraction_reads": {label: b.batch_id for label, b in st["batches"]}},
        "code": {"pool_freeze.py": sha_file(Path(__file__).resolve()),
                 "extract_stage.py": sha_file(X.HERE / "extract_stage.py"),
                 "authoring.py": sha_file(A.HERE / "authoring.py"),
                 "plugin.py": sha_file(A.HERE / "plugin.py"),
                 "fixtures.py": sha_file(A.HERE / "fixtures.py"),
                 "c2_kit/lexicon.py": sha_file(C2_BUILD / "c2_kit" / "lexicon.py"),
                 "c2_kit/g3h.py": sha_file(C2_BUILD / "c2_kit" / "g3h.py"),
                 "c2_kit/chunker.py": sha_file(C2_BUILD / "c2_kit" / "chunker.py")},
        "a38_present": paths.a38_frozen(),
        "counts": counts,
        "targets": rep,
        "shortfalls": short,
        "g_lex_gate": gate,
        "gate_ok": gate_ok,
        "pool_files": {rel: {"sha256": sha, "records": records[rel]} for rel, sha in shas.items()},
        "recorded": "haiku/extract/recorded.json",
        "rows_generated": 0,
    }
    paths.write_json(POOLS / "MANIFEST.json", manifest)
    print(json.dumps({"written": sorted(files) + ["MANIFEST.json"], "pools": str(POOLS),
                      "shortfalls": len(short)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
