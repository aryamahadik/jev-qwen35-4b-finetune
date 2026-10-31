"""families/T06/pool_freeze.py: the T06 extraction stage and the pool freeze (G0-lite T06 section 4; C2_DATA_SPEC 6.2 item 4,
6.3 G-LEX and G3-H; PREREG A37 b and A38). Written after the 20 Haiku extraction answers came back.

Stages (in memory until `write`):
  1. the 14 G-LEX read batches and the 6 G3-H batches are regenerated with extract_build.plan() (deterministic), and their
     task ids are checked against TASKS.json;
  2. answers/<task_id>.json is loaded for every task (chunker.load_answers: qid ownership, duplicates and unanswered items
     are problems, never used);
  3. G-LEX: every read's meaning is mapped to a sem id (meaning_to_sem, the form's own kind), recorded with
     lexicon.record_extraction under the extractor id "haiku-<read>". A form is admitted only when every read agrees with
     its own sem and it has LexForm.required independent reads (2 for deontic and question, 3 for window);
  4. G3-H: g3h.compare for every Mode F message (expected = the generator's facts, orchestrator side only); the template is
     the register; g3h.template_report quarantines a register under 98% (PASS_RATE) and every mismatch is dropped;
  5. quarantine: every author-stage drop (extract_build.plan), every form that is not admitted, every G3-H mismatch and
     every quarantined register;
  6. write (once; refuses when pools/ exists): packs / skins / attacks / documents / notices / wordings as jsonl (admitted
     items only), lexicon.json (admitted forms; every sem kept, closed lists and decoys included), quarantine.jsonl,
     extraction_log.jsonl, g3h_log.jsonl and manifest.json (sha256 of every file, counts per kind and register, admitted
     vs the G0-lite target, every shortfall). All writes go through the A38-guarded kit writers.

Haiku answers only flag: a G-LEX pick that is not the form's own sem rejects the form; a G3-H mismatch drops its message.
No Haiku output sets a label, and no G0 target is lowered. Nothing here generates a row.

  ../.venv/bin/python c2_build/families/T06/pool_freeze.py check   (in memory; writes nothing)
  ../.venv/bin/python c2_build/families/T06/pool_freeze.py write   (once)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, lexicon, paths  # noqa: E402
from families.T06 import extract_build as E  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402

FAMILY = "T06"
VERSION = "v1"
POOLS = HERE / "pools"
EXPECT_TASKS = 20
NOTICE_FLOOR = 6                    # G0 4.3: >= 6 admitted per notice sem
SKIN_FLOOR = 250                    # G0 4.1: 352 asked for >= 250 admitted
PACKS_TOTAL, PACKS_HELD = 44, 8     # G0 4.6
ATTACKS_TOTAL, ATTACKS_HELD = 60, 12  # G0 4.6 (48 + 12 held out)
DOCS_ASKED, DOCS_HELD = 240, 40     # G0 4.2 (Mode F, 200 + 40 asked)


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fid(sem_id: str, text: str) -> str:
    """lexicon.LexiconRegistry.add: form id = sem id + '#' + first 8 hex digits of sha256(text)."""
    return f"{sem_id}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"


def _answers(b) -> tuple:
    """(internal id -> answer object, problems) for one batch, read from answers/<task_id>.json."""
    raw, probs = {}, []
    for c in b.chunks:
        tid = c["task_id"]
        f = E.EXTRACT / b.answer_path(tid)
        if not f.is_file():
            probs.append(f"{tid}: no answer file")
            continue
        try:
            raw[tid] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{tid}: answer is not JSON ({e})")
    ans, p2 = chunker.load_answers(b, raw)
    return ans, probs + p2


def _check_tasks(p) -> list:
    index = json.loads((E.EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    on_disk = {t["task_id"] for t in index["tasks"]}
    in_mem = {c["task_id"] for _label, _kind, _gi, b in p["glex"] for c in b.chunks}
    in_mem |= {c["task_id"] for c in p["g3"].chunks}
    if len(on_disk) != EXPECT_TASKS or on_disk != in_mem:
        raise SystemExit(f"task ids differ from TASKS.json: on disk {len(on_disk)}, regenerated {len(in_mem)}")
    return sorted(on_disk)


def record_glex(p, reg) -> tuple:
    """Record every G-LEX read. Returns (read log, problems). A pick that is not the form's own sem records as a
    disagreement, which lexicon.status() turns into 'rejected'."""
    log, probs = [], []
    for label, _kind, _gi, b in p["glex"]:
        ans, pr = _answers(b)
        probs += [f"{label} {b.batch_id}: {x}" for x in pr]
        qid_of = {internal: qid for qid, internal in b.key.items()}
        for fid, a in sorted(ans.items()):
            f = reg.forms[fid]
            meaning = a.get("meaning") if isinstance(a, dict) else None
            sem = reg.meaning_to_sem(f.kind, meaning) if isinstance(meaning, str) else None
            reg.record_extraction(fid, f"haiku-{label}", sem)
            log.append({"form_id": fid, "kind": f.kind, "read": label, "task_id": b.task_of[qid_of[fid]],
                        "meaning": meaning, "sem_id": sem, "agrees": sem == f.sem_id})
    return log, probs


def check_g3h(p) -> tuple:
    """G3-H: (template report, per-item log, problems). A missing answer counts as a failed item."""
    fields = P.T06Plugin.extract_fields(None, None)
    b = p["g3"]
    ans, probs = _answers(b)
    reg_of = {iid: sk.register for iid, sk, _facts in p["freeform"]}
    rows, log = [], []
    for iid in sorted(p["g3_expected"]):
        if iid not in ans:
            ok, diffs = False, ["no answer"]
        else:
            ok, diffs = g3h.compare(p["g3_expected"][iid], ans[iid], fields)
        rows.append((reg_of[iid], iid, ok))
        log.append({"item": iid, "register": reg_of[iid], "ok": ok, "diffs": diffs})
    return g3h.template_report(rows), log, probs


def admitted(p, reg, rep) -> dict:
    """The admitted pool rows (plain dicts, ready for jsonl). Notices and wordings only when their form is admitted."""
    res = p["res"]
    drop = set(rep["drop_rows"])
    packs = []
    for iid, pk in res["packs"]["keep"]:
        packs.append({"pid": iid, **pk, "held_out": bool(res["packs"]["plan"][iid]["held_out"])})
    skins = []
    for iid, sk in res["skins"]["keep"]:
        skins.append({"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register,
                      "escape": sk.escape, "slots": dict(sk.slots), "held_out": bool(sk.held_out),
                      "haiku_task_id": sk.haiku_task_id, "haiku_prompt_sha": sk.haiku_prompt_sha})
    attacks = []
    for iid, sk in res["attacks"]["keep"]:
        attacks.append({"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "held_out": bool(sk.held_out),
                        "haiku_task_id": sk.haiku_task_id, "haiku_prompt_sha": sk.haiku_prompt_sha})
    documents = []
    for iid, sk, facts in p["freeform"]:
        if iid in drop:
            continue
        documents.append({"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register,
                          "facts": dict(facts), "held_out": bool(sk.held_out),
                          "haiku_task_id": sk.haiku_task_id, "haiku_prompt_sha": sk.haiku_prompt_sha})
    notices = []
    for sem, kind, text, slots, tid, psha in p["notices"]:
        fid = _fid(sem, text)
        if fid in reg.forms and reg.status(fid) == "admitted":
            notices.append({"form_id": fid, "sem_id": sem, "kind": kind, "text": text, "slots": dict(slots),
                            "haiku_task_id": tid, "haiku_prompt_sha": psha,
                            "reads": [list(e) for e in reg.forms[fid].extractions]})
    wordings = []
    for qform, text, held, tid, psha in p["wordings"]:
        fid = _fid(lexicon.question_sem(FAMILY, qform), text)
        if fid in reg.forms and reg.status(fid) == "admitted":
            wordings.append({"form_id": fid, "qform": qform, "text": text, "held_out": bool(held),
                             "haiku_task_id": tid, "haiku_prompt_sha": psha,
                             "reads": [list(e) for e in reg.forms[fid].extractions]})
    return {"packs": packs, "skins": skins, "attacks": attacks, "documents": documents, "notices": notices,
            "wordings": wordings}


def quarantine(p, reg, rep, g3log) -> list:
    q = [{"stage": "author", "batch": d["batch"], "item": d["item"], "class": d["class"], "reasons": d["reasons"]}
         for d in p["drops"]]
    for fid in sorted(reg.forms):
        st = reg.status(fid)
        if st != "admitted":
            f = reg.forms[fid]
            q.append({"stage": "glex", "form_id": fid, "kind": f.kind, "sem_id": f.sem_id, "class": st,
                      "reads": [list(e) for e in f.extractions], "text": f.text, "held_out": f.held_out})
    for row in g3log:
        if not row["ok"]:
            q.append({"stage": "g3h", "item": row["item"], "register": row["register"], "class": "mismatch",
                      "reasons": row["diffs"]})
    for t in rep["quarantined"]:
        q.append({"stage": "g3h-template", "register": t, "class": "under 98% pass",
                  "rate": rep["templates"][t]["rate"]})
    return q


def lexicon_pool(reg) -> dict:
    obj = reg.to_json()
    obj["forms"] = [f for f in obj["forms"] if f["status"] == "admitted"]
    obj["note"] = ("T06 lexicon, admitted forms only (G-LEX). Every sem is kept: the closed meaning lists and the "
                   "never-generated decoys.")
    back = lexicon.LexiconRegistry.from_json(obj)
    not_ok = [k for k in back.forms if back.status(k) != "admitted"]
    if not_ok:
        raise SystemExit(f"lexicon round trip: not admitted after reload {not_ok[:5]}")
    return obj


def targets(p, adm, reg) -> list:
    rows = []

    def add(item, target, admitted_n, source):
        rows.append({"item": item, "target": target, "admitted": admitted_n,
                     "shortfall": max(0, target - admitted_n), "source": source})

    packs = adm["packs"]
    add("packs, all", PACKS_TOTAL, len(packs), "G0 4.6: 44 packs")
    add("packs, held out", PACKS_HELD, sum(1 for x in packs if x["held_out"]), "G0 4.6: 8 held out")
    skins = adm["skins"]
    add("skins, all (floor)", SKIN_FLOOR, len(skins), "G0 4.1: 352 asked for >= 250 admitted")
    for r in H.TRAIN_REGISTERS:
        add(f"skins, register {r}", H.N_SKIN_TRAIN, sum(1 for x in skins if x["register"] == r and not x["held_out"]),
            "per-register ask (38 each, G0 4.1)")
    for r in H.HELD_REGISTERS:
        add(f"skins, held-out register {r}", H.N_SKIN_HELD,
            sum(1 for x in skins if x["register"] == r and x["held_out"]), "per-register ask (24 each, G0 4.1)")
    att = adm["attacks"]
    add("attack lines, all", ATTACKS_TOTAL, len(att), "G0 4.6: 48 + 12 held out")
    add("attack lines, held out", ATTACKS_HELD, sum(1 for x in att if x["held_out"]), "G0 4.6: 12 held out")
    docs = adm["documents"]
    add("documents (Mode F), all", DOCS_ASKED, len(docs), "G0 4.2: 240 asked (no admitted floor is stated)")
    add("documents (Mode F), held out", DOCS_HELD, sum(1 for x in docs if x["held_out"]),
        "G0 4.2: 40 asked held out")
    for r in H.FREEFORM_TRAIN:
        add(f"documents, register {r}", H.N_FREE_TRAIN, sum(1 for x in docs if x["register"] == r and not x["held_out"]),
            "per-register ask (50 each, G0 4.2)")
    for r in H.FREEFORM_HELD:
        add(f"documents, held-out register {r}", H.N_FREE_HELD,
            sum(1 for x in docs if x["register"] == r and x["held_out"]), "per-register ask (20 each, G0 4.2)")
    sem_kind = {}
    for sem, kind, _t, _s, _tid, _ps in p["notices"]:
        sem_kind[sem] = kind
    for sem in sorted(sem_kind):
        n = sum(1 for x in adm["notices"] if x["sem_id"] == sem)
        add(f"notice {sem} ({sem_kind[sem]})", NOTICE_FLOOR, n,
            f"G0 4.3: >= 6 admitted per sem (asked {H.N_NOTICE[sem_kind[sem]]})")
    wds = adm["wordings"]
    add("wordings, training", sum(t for t, _h in H.WORDING_PLAN.values()),
        sum(1 for x in wds if not x["held_out"]), "G0 4.5: 106 training")
    add("wordings, held out", sum(h for _t, h in H.WORDING_PLAN.values()),
        sum(1 for x in wds if x["held_out"]), "G0 4.5: 29 held out")
    for q, (tr, ho) in sorted(H.WORDING_PLAN.items()):
        add(f"wording {q}, training", tr, sum(1 for x in wds if x["qform"] == q and not x["held_out"]),
            f"G0 4.5 ask ({tr} training)")
        add(f"wording {q}, held out", ho, sum(1 for x in wds if x["qform"] == q and x["held_out"]),
            f"G0 4.5 ask ({ho} held out)")
    add("ch_rule wordings (G0 floor 30)", 30, sum(1 for x in wds if x["qform"] == "ch_rule"),
        "G0 4.5: ch_rule >= 30")
    add("ch_end_withdraw wordings (2% floor 4)", 4, sum(1 for x in wds if x["qform"] == "ch_end_withdraw"),
        "G0 4.5: each admitted wording <= 2%, so each ch_end >= 4")
    forms = [f for f in reg.forms.values()]
    add("lexicon forms used (must all be admitted)", len(forms),
        sum(1 for f in forms if reg.status(f.form_id) == "admitted"), "G-LEX: every used form admitted")
    return rows


def summary(p, reg, rep, adm, q, glex_log, g3log, probs) -> dict:
    tg = targets(p, adm, reg)
    per_glex = Counter()
    for r in glex_log:
        per_glex[(r["read"], r["kind"], "agree" if r["agrees"] else "disagree")] += 1
    statuses = Counter((reg.forms[f].kind, reg.status(f)) for f in reg.forms)
    return {
        "authoring_drops_by_class": dict(Counter(d["class"] for d in p["drops"])),
        "authoring_drops_by_batch": dict(Counter(d["batch"] for d in p["drops"])),
        "pool_counts": {"packs": len(adm["packs"]), "skins": len(adm["skins"]), "attacks": len(adm["attacks"]),
                        "documents": len(adm["documents"]), "notices": len(adm["notices"]),
                        "wordings": len(adm["wordings"]),
                        "lexicon_forms_admitted": sum(1 for f in reg.forms if reg.status(f) == "admitted")},
        "glex_reads": {f"{k[0]}/{k[1]}/{k[2]}": v for k, v in sorted(per_glex.items())},
        "glex_form_status": {f"{k[0]}/{k[1]}": v for k, v in sorted(statuses.items())},
        "g3h": {"items": len(g3log), "ok": sum(1 for r in g3log if r["ok"]),
                "per_register": {t: {"n": d["n"], "ok": d["ok"], "rate": round(d["rate"], 4)}
                                 for t, d in rep["templates"].items()},
                "quarantined_registers": rep["quarantined"]},
        "quarantine_entries": len(q),
        "quarantine_by_stage": dict(Counter(x["stage"] for x in q)),
        "answer_problems": probs,
        "targets": tg,
        "shortfalls": [t for t in tg if t["shortfall"] > 0],
    }


def run() -> dict:
    p = E.plan()
    task_ids = _check_tasks(p)
    reg = p["reg"]
    glex_log, glex_probs = record_glex(p, reg)
    rep, g3log, g3_probs = check_g3h(p)
    probs = glex_probs + g3_probs
    q = quarantine(p, reg, rep, g3log)
    adm = admitted(p, reg, rep)
    lex = lexicon_pool(reg)
    summ = summary(p, reg, rep, adm, q, glex_log, g3log, probs)
    return {"p": p, "reg": reg, "task_ids": task_ids, "glex_log": glex_log, "g3log": g3log, "rep": rep,
            "q": q, "adm": adm, "lex": lex, "summary": summ, "probs": probs}


def write() -> dict:
    if POOLS.exists():
        raise FileExistsError(f"{POOLS} exists: the T06 pools are frozen once")
    r = run()
    adm = r["adm"]
    pools = {"packs.jsonl": adm["packs"], "skins.jsonl": adm["skins"], "attacks.jsonl": adm["attacks"],
             "documents.jsonl": adm["documents"], "notices.jsonl": adm["notices"], "wordings.jsonl": adm["wordings"],
             "quarantine.jsonl": r["q"], "extraction_log.jsonl": r["glex_log"], "g3h_log.jsonl": r["g3log"]}
    files = {}
    for name, rows in pools.items():
        path = POOLS / name
        paths.write_jsonl(path, rows)
        files[name] = {"sha256": _sha_file(path), "rows": len(rows)}
    lex_path = POOLS / "lexicon.json"
    paths.write_json(lex_path, r["lex"])
    files["lexicon.json"] = {"sha256": _sha_file(lex_path), "forms": len(r["lex"]["forms"]),
                             "sems": len(r["lex"]["sems"])}
    tasks_path = E.EXTRACT / "TASKS.json"
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "pool-freeze",
        "a38_frozen": paths.a38_frozen(),
        "g0_lite": {"file": "G0_SPEC.md", "sha256": _sha_file(HERE / "G0_SPEC.md"),
                    "plugin_G0_SHA256": P.T06Plugin.G0_SHA256_AUTHORED,
                    "matches_plugin": _sha_file(HERE / "G0_SPEC.md") == P.T06Plugin.G0_SHA256_AUTHORED},
        "extraction": {"tasks": len(r["task_ids"]), "TASKS.json_sha256": _sha_file(tasks_path),
                       "answers": {tid: _sha_file(E.EXTRACT / "answers" / f"{tid}.json") for tid in r["task_ids"]}},
        "pool_files": files,
        "summary": r["summary"],
        "gates": {"G-LEX": {"rule": "every read agrees with the form's own sem; 2 reads (deontic, question) or 3 "
                                    "(window); any disagreement rejects",
                            "admitted": r["summary"]["pool_counts"]["lexicon_forms_admitted"],
                            "forms": len(r["reg"].forms)},
                  "G3-H": {"rule": "g3h.compare on name fields; register = template; 98% per template",
                           "bar": g3h.PASS_RATE, "items": len(r["g3log"]), "ok": r["summary"]["g3h"]["ok"],
                           "quarantined_registers": r["rep"]["quarantined"]}},
        "notes": [
            "No row, card or generator run was made. Haiku output never sets a label or a gold.",
            "documents = Mode F free-form messages (G0 4.2). Statute cards (G0 2) are program text in plugin.py, "
            "not a Haiku pool.",
            "Access audit (kit README step 4, audit.audit_jsonl): not run here. No transcripts sit in haiku/extract, so "
            "the lead must audit each of the 20 task agents before these answers count.",
            "Targets are the G0-lite numbers; none was lowered. A shortfall is reported, never refilled.",
        ],
    }
    paths.write_json(POOLS / "manifest.json", manifest)
    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="families.T06.pool_freeze")
    ap.add_argument("cmd", choices=("check", "write"))
    a = ap.parse_args(argv)
    if a.cmd == "check":
        r = run()
        print(json.dumps(r["summary"], indent=1, ensure_ascii=False))
        return 0
    m = write()
    print(json.dumps({"pool_files": m["pool_files"], "summary": m["summary"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
