"""families/T25/stage6_admit.py: T25 stage 6 (C2 data stage A, Admit): G-LEX admission of the question wordings from the
two independent extraction reads, quarantine of every piece that fails, the pool freeze and the manifest (C2_DATA_SPEC
3.0, 6.2; G0_SPEC.md section 7 and section 9; PREREG A37 (b), A38).

Inputs (read only, orchestrator side): haiku/pool/kept.json and REPORT.json (the stage-4 lint and dedup output),
haiku/extract/{manifest,key,chunks,tasks,answers}/. No Haiku task reads the key or the manifest.
Outputs (only with --write, through c2_kit.paths): families/T25/pools/ (frozen pools, lexicon record, QUARANTINE.json,
MANIFEST.json). The dry run is the default and writes nothing.

  ../.venv/bin/python c2_build/families/T25/stage6_admit.py          # counts and shortfalls
  ../.venv/bin/python c2_build/families/T25/stage6_admit.py --write  # the freeze
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from families.T25 import haiku_author as H  # noqa: E402

FAMILY = "T25"
STAGE4 = HERE / "haiku" / "pool"
EXTRACT = HERE / "haiku" / "extract"
POOLS = HERE / "pools"
G0 = HERE / "G0_SPEC.md"
G0_PIN = "aabd110d5310642fab6494796324ce3015192d645004f7e55a848262ac1c45f6"   # plugin.T25.G0_SHA256 (frozen v2)
NEAR_DUP = 0.7                                                                  # 4-gram Jaccard (G0 stage 4)
READS = ("read1", "read2")

# G0_SPEC section 7 and spec 3.0 targets, never lowered
TARGET = {
    "attr_packs": 30,        # >= 30 admitted (one per card)
    "source_nouns": 40,      # >= 40 admitted
    "tier_schemes": 8,       # >= 8 admitted
    "wordings_total": 30,    # >= 30 admitted
    "wordings_per_form": 4,  # >= 4 admitted per form
    "registers": 8,          # >= 8 registers per family (spec 3.0)
    "registers_held_out": 2, # >= 2 held out (spec 3.0)
    "mode_f_cap": 0.20,      # Mode F <= 20% of each register's admitted pool (G0 section 7)
}
AUTHORED = {"skins_train_per_register": 40, "skins_held_per_register": 20, "freeform_train": 12,
            "freeform_held": 6, "attacks": 48, "attr_kinds": {"money": 22, "date": 16, "count": 22}}


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def jtext(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def ngrams(text: str, n: int = 4) -> set:
    toks = re.findall(r"[a-z0-9]+|\{[a-z_]+\}", text.lower())
    return {tuple(toks[i:i + n]) for i in range(max(0, len(toks) - n + 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a | b) else 0.0


def near_dup_filter(items: list, text_of) -> tuple:
    """Greedy filter in the given order: a later item with 4-gram Jaccard >= 0.7 to a kept item is dropped."""
    kept, grams, dropped = [], [], []
    for it in items:
        g = ngrams(text_of(it))
        twin = next((kept[j] for j, gj in enumerate(grams) if jaccard(g, gj) >= NEAR_DUP), None)
        if twin is None:
            kept.append(it)
            grams.append(g)
        else:
            dropped.append((it, twin))
    return kept, dropped


def closed_list(tid: str, meanings: set) -> list:
    """The meanings a read's task file printed (must be the 7 question meanings, each once)."""
    txt = (EXTRACT / "tasks" / f"{tid}.md").read_text(encoding="utf-8")
    listed = [ln[2:].strip() for ln in txt.splitlines() if ln.startswith("- ") and ln[2:].strip() in meanings]
    if sorted(listed) != sorted(meanings):
        raise SystemExit(f"{tid}: the printed closed list is not the 7 question meanings, once each")
    return listed


def load_reads(meanings: set) -> list:
    """One dict per extraction chunk: read label, task id, answers loaded through chunker.load_answers against the
    batch key (orchestrator side) and the chunk's own qids."""
    reads = []
    for mf in sorted((EXTRACT / "manifest").glob("*.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        bid, seed = m["batch_id"], m["seed"]
        read = next((r for r in READS if f"-{r}-" in seed), None)
        if read is None:
            raise SystemExit(f"{mf.name}: unknown read label in seed {seed!r}")
        key = json.loads((EXTRACT / "key" / f"{bid}.json").read_text(encoding="utf-8"))["key"]
        for t in m["tasks"]:
            tid = t["task_id"]
            chunk = json.loads((EXTRACT / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
            qids = [x["qid"] for x in chunk["items"]]
            if len(qids) != len(set(qids)) or set(qids) != set(key):
                raise SystemExit(f"{tid}: chunk qids differ from the batch key")
            raw = json.loads((EXTRACT / "answers" / f"{tid}.json").read_text(encoding="utf-8"))
            b = chunker.TaskBatch(m["kind"], m["family"], bid, "", m["prompt_sha"], seed)
            b.task_of = {q: tid for q in qids}
            b.key = dict(key)
            out, probs = chunker.load_answers(b, {tid: raw})
            reads.append({"read": read, "tid": tid, "batch_id": bid, "seed": seed, "n": len(qids),
                          "listed": closed_list(tid, meanings), "out": out, "probs": probs, "raw": raw,
                          "answer_sha": sha_text((EXTRACT / "answers" / f"{tid}.json").read_text(encoding="utf-8"))})
    return reads


def admit(reg, reads: list) -> dict:
    """Record every read as one independent extraction per form (extractor = the read label). An answer off the
    printed closed list counts as a rejected pick (sem None), never as a match."""
    off, seen = [], defaultdict(list)
    for r in reads:
        for fid, meaning in r["out"].items():
            if fid not in reg.forms:
                raise SystemExit(f"{r['tid']}: key form {fid} is not in the registry")
            on = isinstance(meaning, str) and meaning in r["listed"]
            sem = reg.meaning_to_sem("question", meaning) if on else None
            reg.record_extraction(fid, r["read"], sem)          # raises on a second read of the same form
            seen[fid].append((r["read"], meaning if on else None))
            if not on:
                off.append({"task": r["tid"], "form": fid, "answer": str(meaning)[:120]})
    status = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    coverage = Counter(len(seen.get(fid, [])) for fid in reg.forms)
    return {"status": status, "off_list": off, "coverage": dict(coverage), "picks": seen}


def qform_of(reg, fid: str) -> str:
    return reg.forms[fid].sem_id.rsplit(".", 1)[-1]


def compare_loader(kept: dict, skins, free, atts, names, nouns, schemes, packs) -> dict:
    """Each kept piece must come out of the loader with the same id and text (kept.json is the stage-4 output)."""
    out = {}
    out["skins_ids_in_loader"] = sum(1 for s in kept["skins"] if s["id"] in skins)
    out["skins_text_mismatch"] = sum(1 for s in kept["skins"] if s["id"] in skins and skins[s["id"]].text != s["text"])
    out["freeform_ids_in_loader"] = sum(1 for s in kept["freeform"] if s["id"] in free)
    out["attacks_ids_in_loader"] = sum(1 for s in kept["attacks"] if s["id"] in atts)
    out["attacks_text_mismatch"] = sum(1 for s in kept["attacks"] if s["id"] in atts and atts[s["id"]].text != s["text"])
    out["attr_packs_ids_in_loader"] = sum(1 for p in kept["attr_packs"] if p["id"] in packs)
    out["nouns_loader_n"] = len(nouns)
    out["orgs_loader_n"] = len(names.get("org", []))
    out["askers_loader_n"] = len(names.get("person", []))
    out["schemes_loader_n"] = len(schemes)
    return out


def run(write: bool) -> dict:
    kept = json.loads((STAGE4 / "kept.json").read_text(encoding="utf-8"))
    rep = json.loads((STAGE4 / "REPORT.json").read_text(encoding="utf-8"))
    g0_sha = hashlib.sha256(G0.read_bytes()).hexdigest()
    if g0_sha != G0_PIN:
        raise SystemExit("G0_SPEC.md does not match the frozen pin")
    skins, skin_probs = H.load_skins()
    free, free_probs = H.load_freeform()
    atts, att_probs = H.load_attacks()
    words, word_probs = H.load_wordings()
    packs, pack_probs = H.load_attr_packs()
    nouns, noun_probs = H.load_nouns()
    names, name_probs = H.load_names()
    schemes, scheme_probs = H.load_schemes()
    loader_cmp = compare_loader(kept, skins, free, atts, names, nouns, schemes, packs)

    # ---- G-LEX: registry from the kept wordings (the same builder the extraction tasks came from)
    kept_w_text = {w["text"] for w in kept["wordings"]}
    wtuples = [w for w in words if w[1] in kept_w_text]
    if len(wtuples) != len(kept["wordings"]):
        raise SystemExit(f"kept wordings ({len(kept['wordings'])}) do not all come from the loader ({len(wtuples)})")
    reg = H.lexicon_registry(wtuples)
    if len(reg.forms) != len(kept["wordings"]):
        raise SystemExit(f"registry holds {len(reg.forms)} forms, kept {len(kept['wordings'])} (a form was refused)")
    unit_bad = {fid: f.unit_problems for fid, f in reg.forms.items() if not f.unit_ok}
    meanings = {s.meaning for s in reg.sems.values() if s.kind == "question"}
    reads = load_reads(meanings)
    adm = admit(reg, reads)
    status = adm["status"]
    admitted = [fid for fid, s in status.items() if s == "admitted"]
    gate = reg.gate()

    # ---- wordings pool: admitted forms only; per-form counts against the G0 target
    w_by_q = Counter(qform_of(reg, fid) for fid in admitted)
    w_all_q = Counter(qform_of(reg, fid) for fid in reg.forms)
    word_short = {q: w_by_q.get(q, 0) for q in sorted(w_all_q)}
    wordings_pool = []
    for fid in admitted:
        f = reg.forms[fid]
        wordings_pool.append({"form_id": fid, "qform": qform_of(reg, fid), "text": f.text,
                              "slots": dict(f.slots), "source": f.source, "haiku_task_id": f.haiku_task_id,
                              "haiku_prompt_sha": f.haiku_prompt_sha, "extractions": [list(e) for e in f.extractions]})
    wq_quarantine = []
    for fid, s in status.items():
        if s != "admitted":
            f = reg.forms[fid]
            wq_quarantine.append({"pool": "wordings", "piece": fid, "qform": qform_of(reg, fid), "text": f.text,
                                  "reason": f"G-LEX {s}", "extractions": [list(e) for e in f.extractions],
                                  "unit_problems": f.unit_problems})

    # ---- Mode T skins (kept at stage 4); near-duplicate check on the frozen set (G0 dedup, 4-gram 0.7)
    skin_entries = list(kept["skins"])
    skin_keep, skin_twins = near_dup_filter(skin_entries, lambda s: s["text"])
    word_keep, word_twins = near_dup_filter(wordings_pool, lambda w: w["text"])
    att_keep, att_twins = near_dup_filter(kept["attacks"], lambda a: a["text"])
    free_keep, free_twins = near_dup_filter(kept["freeform"], lambda d: d["text"])

    if len(word_keep) != len(wordings_pool):
        wq_quarantine += [{"pool": "wordings", "piece": w["form_id"], "qform": w["qform"], "text": w["text"],
                           "reason": "near-duplicate of an admitted wording (4-gram 0.7)",
                           "twin": t["form_id"]} for w, t in word_twins]
        wordings_pool = word_keep
    skin_q = []
    for s, t in skin_twins:
        skin_q.append({"pool": "skins", "piece": s["id"], "reason": "near-duplicate (4-gram 0.7) at freeze",
                       "twin": t["id"]})
    att_q = [{"pool": "attacks", "piece": a["id"], "reason": "near-duplicate (4-gram 0.7) at freeze", "twin": t["id"]}
             for a, t in att_twins]
    free_q = [{"pool": "documents_mode_f", "piece": d["id"], "reason": "near-duplicate (4-gram 0.7) at freeze",
               "twin": t["id"]} for d, t in free_twins]

    # ---- stage-4 drops (loader problems + REPORT dedup), carried into QUARANTINE with their reasons
    stage4_q = []
    for pool, probs in (("skins", skin_probs), ("freeform", free_probs), ("attacks", att_probs),
                        ("wordings_stage4", word_probs), ("attr_packs", pack_probs), ("nouns", noun_probs),
                        ("names", name_probs), ("schemes", scheme_probs)):
        for p in probs:
            piece, _, why = p.partition(": ")
            stage4_q.append({"pool": pool, "piece": piece, "reason": f"stage 4 lint or exact duplicate: {why}"})
    for pool, rows in rep.get("dedup_dropped", {}).items():
        for r in rows:
            if "near-duplicate" not in r["why"]:        # exact duplicates are already listed by the loader problems
                continue
            stage4_q.append({"pool": f"{pool}_stage4_dedup", "piece": r["piece"],
                             "reason": f"stage 4 dedup: {r['why']}", "twin": r.get("kept_twin")})

    # ---- Mode F documents: frozen, not admitted (G3-H round trip has not been run)
    reg_T = Counter(s["register"] for s in skin_keep)
    reg_F = Counter(d["register"] for d in free_keep)
    reg_held = {s["register"]: bool(s["held_out"]) for s in skin_keep}
    cap_excess = {}
    for r in sorted(set(reg_T) | set(reg_F)):
        t, f = reg_T.get(r, 0), reg_F.get(r, 0)
        cap_excess[r] = max(0, f - math.floor(TARGET["mode_f_cap"] / (1 - TARGET["mode_f_cap"]) * t))

    # ---- shortfall table: four kinds, never mixed. G0 targets are thresholds (never lowered); a G0 cap is a limit;
    # the authored plan is context (a gap is reported, it is not a G0 breach); a gate not run is listed as not run.
    attr_kinds = Counter(p["kind"] for p in kept["attr_packs"])
    n_train_reg = sum(1 for r in reg_T if not reg_held[r])
    n_held_reg = sum(1 for r in reg_T if reg_held[r])
    train_skins = sum(v for r, v in reg_T.items() if not reg_held[r])
    held_skins = sum(v for r, v in reg_T.items() if reg_held[r])
    mode_t_total = sum(reg_T.values())
    top_reg = max(reg_T, key=reg_T.get)
    short = []

    def g0(item, target, got, note=""):
        short.append({"kind": "G0 target", "item": item, "target": target, "got": got, "met": got >= target,
                      "note": note})

    def cap(item, limit, got, note=""):
        short.append({"kind": "G0 cap", "item": item, "target": limit, "got": got, "met": got <= limit, "note": note})

    def plan(item, asked, got, note=""):
        short.append({"kind": "authored plan (gap, not a G0 threshold)", "item": item, "target": asked, "got": got,
                      "met": got >= asked, "note": note})

    def not_run(item, note):
        short.append({"kind": "gate not run", "item": item, "target": None, "got": None, "met": False, "note": note})

    g0("G-LEX: question forms admitted (every used form)", len(reg.forms), len(admitted), "2/2 independent reads each")
    g0("attribute packs (one per card)", TARGET["attr_packs"], len(kept["attr_packs"]), f"kinds {dict(attr_kinds)}")
    g0("source nouns", TARGET["source_nouns"], len(kept["source_nouns"]))
    g0("tier schemes", TARGET["tier_schemes"], len(kept["schemes"]))
    g0("question wordings admitted", TARGET["wordings_total"], len(wordings_pool))
    for q in sorted(word_short):
        g0(f"question wordings {q}", TARGET["wordings_per_form"], word_short[q], "per form")
    g0("training registers (Mode T)", TARGET["registers"], n_train_reg, "spec 3.0: at least 8")
    g0("held-out registers", TARGET["registers_held_out"], n_held_reg, "spec 3.0: at least 2")
    cap("Mode F share of the admitted pool", 0.25, 0.0, "Mode F admitted 0 of the Mode T pool")
    cap("largest register share of the Mode T pool", 0.15, round(reg_T[top_reg] / mode_t_total, 4),
        f"largest register {top_reg}")
    plan("skins, training registers (8 x 40 asked)", 320, train_skins,
         "G0 asks equal pools per register; the pools are 33-40")
    plan("skins, held-out registers (2 x 20 asked)", 40, held_skins)
    plan("attack lines", AUTHORED["attacks"], len(kept["attacks"]), "G0 sets no minimum")
    plan("source nouns (8 x 12 asked)", 96, len(kept["source_nouns"]))
    plan("tier schemes (asked 16)", 16, len(kept["schemes"]))
    plan("askers (asked 60)", 60, len(kept["askers"]))
    not_run("G3-H round trip for the Mode F documents (>= 98% per template)",
         f"not run: no G3-H task exists in haiku/extract/; {len(free_keep)} documents frozen as pending_g3h; "
         f"if all were admitted, {sum(cap_excess.values())} would exceed the 20% per-register cap")
    not_run("G13 seed-first decontamination of the pools", "not run in this stage (the later G13 stage)")
    not_run("Haiku file-access audit (the six extraction agents)", "not verified here: no audit output or transcripts")

    shortfalls = [r for r in short if not r["met"]]

    summary = {
        "loader_cmp": loader_cmp,
        "stage4_counts": {"skins_loaded": len(skins), "freeform_loaded": len(free), "attacks_loaded": len(atts),
                          "wordings_loaded": len(words), "skin_problems": len(skin_probs),
                          "wording_problems": len(word_probs), "attack_problems": len(att_probs)},
        "glex": {"forms_registered": len(reg.forms), "unit_fail": sorted(unit_bad), "status_counts":
                 dict(Counter(status.values())), "gate_pass": gate["pass"], "admitted": len(admitted),
                 "coverage": adm["coverage"], "off_list_answers": adm["off_list"],
                 "answer_problems": {r["tid"]: r["probs"] for r in reads if r["probs"]}},
        "admitted_per_qform": dict(w_by_q), "forms_per_qform": dict(w_all_q),
        "pools": {"skins_mode_t": len(skin_keep), "skins_by_register": dict(reg_T),
                  "held_out_registers": sorted(r for r in reg_held if reg_held[r]),
                  "documents_mode_f_frozen": len(free_keep), "documents_mode_f_admitted": 0,
                  "attacks": len(att_keep), "attr_packs": len(kept["attr_packs"]),
                  "source_nouns": len(kept["source_nouns"]), "organisations": len(kept["organisations"]),
                  "askers": len(kept["askers"]), "tier_schemes": len(kept["schemes"]),
                  "wordings_admitted": len(wordings_pool)},
        "freeze_near_dup_drops": {"skins": len(skin_twins), "attacks": len(att_twins),
                                  "wordings": len(word_twins), "documents_mode_f": len(free_twins)},
        "mode_f_cap_excess_by_register": cap_excess,
        "shortfalls": shortfalls,
        "table": short,
    }

    if write:
        files = write_freeze(kept, reg, status, skin_keep, free_keep, att_keep, wordings_pool,
                             stage4_q + skin_q + att_q + free_q + wq_quarantine, rep, reads, summary, g0_sha)
        summary["written"] = sorted(files)
    return summary


def write_freeze(kept, reg, status, skin_keep, free_keep, att_keep, wordings_pool, quarantine, rep, reads,
                 summary, g0_sha) -> list:
    files = {}
    producer = Path(__file__).resolve()
    files["skins_mode_t.json"] = jtext({"family": FAMILY, "kind": "skin", "author_mode": "T", "status": "admitted",
                                        "n": len(skin_keep), "items": skin_keep})
    files["documents_mode_f.json"] = jtext({"family": FAMILY, "kind": "freeform", "author_mode": "F",
                                            "status": "pending_g3h", "admitted": 0, "n": len(free_keep),
                                            "note": "G-SL lint_freeform passed; G3-H fact round trip not run",
                                            "items": [dict(d, status="pending_g3h") for d in free_keep]})
    files["attacks.json"] = jtext({"family": FAMILY, "kind": "attack", "status": "admitted", "n": len(att_keep),
                                   "items": att_keep})
    files["attr_packs.json"] = jtext({"family": FAMILY, "kind": "attr_pack", "status": "admitted",
                                      "n": len(kept["attr_packs"]), "items": kept["attr_packs"]})
    files["source_nouns.json"] = jtext({"family": FAMILY, "kind": "source_noun", "status": "admitted",
                                        "n": len(kept["source_nouns"]), "items": kept["source_nouns"]})
    files["organisations.json"] = jtext({"family": FAMILY, "kind": "organisation", "status": "admitted",
                                         "n": len(kept["organisations"]), "items": kept["organisations"]})
    files["askers.json"] = jtext({"family": FAMILY, "kind": "asker", "status": "admitted",
                                  "n": len(kept["askers"]), "items": kept["askers"]})
    files["tier_schemes.json"] = jtext({"family": FAMILY, "kind": "tier_scheme", "status": "admitted",
                                        "n": len(kept["schemes"]), "items": kept["schemes"]})
    files["wordings.json"] = jtext({"family": FAMILY, "kind": "question_wording", "status": "admitted",
                                    "n": len(wordings_pool), "items": wordings_pool})
    files["lexicon.json"] = jtext(dict(reg.to_json(), family=FAMILY, record="G-LEX record of all 139 forms: "
                                       "extractions, status and unit test per form (the wordings pool holds the admitted "
                                       "forms only)"))
    files["QUARANTINE.json"] = jtext({"family": FAMILY, "n": len(quarantine), "items": quarantine})
    # the manifest hashes every file above, so it is built from the texts before it is written
    inputs = {"haiku/pool/kept.json": STAGE4 / "kept.json", "haiku/pool/REPORT.json": STAGE4 / "REPORT.json",
              "G0_SPEC.md": G0}
    for r in reads:
        tid = r["tid"]
        for rel in (f"haiku/extract/answers/{tid}.json", f"haiku/extract/chunks/{tid}.json",
                    f"haiku/extract/tasks/{tid}.md"):
            inputs[rel] = HERE / rel
    manifest_files = {rel: {"sha256": sha_text(txt), "bytes": len(txt.encode("utf-8"))} for rel, txt in files.items()}
    manifest = {
        "family": FAMILY, "stage": "6 (G-LEX admission, quarantine, pool freeze)",
        "binding": {"G0_SPEC_sha256": g0_sha, "G0_pin_match": g0_sha == G0_PIN, "PREREG": "A37 (b) and A38",
                    "producer_script_sha256": hashlib.sha256(producer.read_bytes()).hexdigest()},
        "inputs": {rel: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for rel, p in sorted(inputs.items())},
        "files": manifest_files,
        "counts": {"wordings_admitted": len(wordings_pool), "forms_registered": len(reg.forms),
                   "forms_by_status": dict(Counter(status.values())),
                   "skins_mode_t": len(skin_keep), "documents_mode_f_frozen": len(free_keep),
                   "documents_mode_f_admitted": 0, "attacks": len(att_keep),
                   "attr_packs": len(kept["attr_packs"]), "source_nouns": len(kept["source_nouns"]),
                   "organisations": len(kept["organisations"]), "askers": len(kept["askers"]),
                   "tier_schemes": len(kept["schemes"]), "quarantined_pieces": len(quarantine)},
        "shortfalls_vs_g0": summary["shortfalls"],
        "not_run": ["G3-H round trip on the 84 Mode F documents (no G3-H task exists in haiku/extract/)",
                    "G13 seed-first decontamination of the pools (run by the later G13 stage)",
                    "file-access audit of the Haiku agents (no transcripts were available to this stage)",
                    "G-SL on the 6 extraction answers (not applicable: answers are closed-list picks)"],
        "notes": ["Two extractions per form (read1, read2) from separate chunk files; both reads printed the same 7 "
                  "question meanings in a different order per read.",
                  "No gold, label or row was written. Haiku answers only set G-LEX admission and quarantine."],
    }
    files["MANIFEST.json"] = jtext(manifest)
    paths.write_files(POOLS, {rel: txt for rel, txt in files.items()})
    # verify what landed on disk
    for rel, txt in files.items():
        on_disk = (POOLS / rel).read_text(encoding="utf-8")
        if sha_text(on_disk) != sha_text(txt):
            raise SystemExit(f"{rel}: written bytes differ from the manifest")
    return list(files)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="freeze the pools (default: dry run)")
    a = ap.parse_args(argv)
    res = run(write=a.write)
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
