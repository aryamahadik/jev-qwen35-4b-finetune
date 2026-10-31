"""c2_build/families/T12/pool_freeze.py: freeze the T12 pools after the extraction record (A38 and A37 apply).

Gates applied, in order, to every piece the authoring stage kept (extract_build.build_all):
  lint and dedup  already applied by extract_build (dropped pieces are logged with their reasons);
  G-LEX           a wording, comparator or precedence piece is kept only if its lexicon form is admitted
                  (unit test and 2/2 read agreement; 3/3 for precedence), see extract_record.record_lex;
  G3-H            a free-form note is kept only if its extraction matches the note's facts (g3h.compare). A note is
                  its own template (Mode F skin), so a mismatch quarantines that note only (the 98% bar per
                  template);
  packs, skins and pressure lines have no extraction gate in G0-lite section 2 and pass lint only.
No piece is re-filled from another form. No row is generated here.

  ../.venv/bin/python -m families.T12.pool_freeze plan     (from lean/c2_build; prints counts and shortfalls; no writes)
  ../.venv/bin/python -m families.T12.pool_freeze freeze   (writes families/T12/pools/ and its manifest)
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from families.T12 import extract_build as EB  # noqa: E402
from families.T12 import extract_record as XR  # noqa: E402
from families.T12 import plugin as P  # noqa: E402

FAMILY = "T12"
POOLS = HERE / "pools"
LEX_POOLS = ("wordings", "comparators", "precedence")

# The G0-lite section 2 numbers, exactly as the spec writes them (no target is lowered). Where G0-lite states no
# number, the row says so and nothing is compared.
G0_TARGETS = (
    {"pool": "packs", "metric": "kept packs", "target": 25, "op": ">=",
     "source": "G0-lite s2: packs (2 tasks x 25), >= 25 kept, one per card"},
    {"pool": "packs", "metric": "pack tasks", "target": 2, "op": "==", "source": "G0-lite s2: 2 pack tasks"},
    {"pool": "skins", "metric": "narrative-skin tasks", "target": 10, "op": "==",
     "source": "G0-lite s2: one task per register: 8 training registers + 2 held-out (portal, voicemail)"},
    {"pool": "freeform", "metric": "free-form tasks", "target": 3, "op": "==",
     "source": "G0-lite s2: 2 training + 1 held-out free-form tasks (the <= 25% of rows bar is row-level, not checked)"},
    {"pool": "wordings", "metric": "admitted question wordings", "target": 30, "op": ">=",
     "source": "G0-lite s2 (kit): question wordings >= 30 per family"},
    {"pool": "wordings", "metric": "question-wording tasks", "target": 6, "op": "==",
     "source": "G0-lite s2: 5 training tasks + 1 held-out task"},
    {"pool": "wordings", "metric": "G-LEX used forms not admitted", "target": 0, "op": "==",
     "source": "G0-lite s2 / A37(b): every used lexicon form admitted (2/2; 3/3 precedence). Rejected forms are not used"},
    {"pool": "freeform", "metric": "G3-H template pass rate", "target": 98.0, "op": ">=",
     "source": "G0-lite s2 / C2 spec 6.3: >= 98% per template (one note = one template): notes below it are quarantined"},
)


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def piece_status(out: dict) -> tuple:
    """(admitted pieces by pool, quarantine rows). Every kept piece is either admitted or quarantined with a reason."""
    res, reg = out["res"], out["res"]["reg"]
    adm, quar = {}, []
    for p in res["kept"]:
        reason = None
        form_id = None
        if p["typ"] in EB.LEX_TYPES:
            form_id = EB._fid(EB._form_spec(p)["sem"], p["text"])
            if form_id not in reg.forms:
                reason = "G-LEX: piece has no lexicon form in the registry"
            else:
                st = reg.status(form_id)
                if st != "admitted":
                    reason = (f"G-LEX {st}: extractions "
                              + "; ".join(f"{e}={s}" for e, s in reg.forms[form_id].extractions))
        elif p["typ"] == "free":
            d = out["g3h_detail"][f"g3h|{p['pid']}"]
            if not d["ok"]:
                reason = "G3-H mismatch: " + "; ".join(d["diffs"])
        if reason:
            quar.append({"stage": "G-LEX" if p["typ"] in EB.LEX_TYPES else "G3-H", "pool": p["pool"], "pid": p["pid"],
                         "held_out": p["held"], "task_id": p["tid"], "form_id": form_id, "reason": reason,
                         "text": p["text"]})
            continue
        p["form_id"] = form_id
        adm.setdefault(p["pool"], []).append(p)
    for p in res["dropped"]:
        quar.append({"stage": "lint", "pool": p["pool"], "pid": p["pid"], "held_out": p["held"], "task_id": p["tid"],
                     "form_id": None, "reason": "; ".join(p["problems"][:3]) or "empty value", "text": p["text"]})
    for p in res["dups"]:
        quar.append({"stage": "dedup", "pool": p["pool"], "pid": p["pid"], "held_out": p["held"], "task_id": p["tid"],
                     "form_id": None, "reason": "duplicate of an earlier piece (training before held-out)",
                     "text": p["text"]})
    return adm, quar


def task_table(out: dict, adm: dict) -> list:
    """Per authoring task: pieces authored, admitted, quarantined (by the stage that dropped them)."""
    res = out["res"]
    rows = []
    for t in res["tasks"]:
        pool = t["pool"]
        n_adm = sum(1 for p in adm.get(pool, []) if p["tid"] == t["task_id"])
        rows.append({"task": t["task"], "task_id": t["task_id"], "pool": pool, "held_out": t["held_out"],
                     "pieces_authored": t["pieces"], "admitted": n_adm, "task_problems": t["task_problems"]})
    return rows


def _bare(p: dict, extra: dict) -> dict:
    d = {"pid": p["pid"], "held_out": p["held"], "task_id": p["tid"], "prompt_sha": p["prompt_sha"]}
    d.update(extra)
    return d


def pool_items(out: dict, adm: dict) -> dict:
    """{file stem: items} for the frozen pools (admitted pieces only)."""
    detail = out["g3h_detail"]
    reg = out["res"]["reg"]
    packs, skins, attacks, docs, words, cmps, precs = [], [], [], [], [], [], []
    for p in adm.get("packs", []):
        pid_parts = p["pid"].split("|")
        packs.append(_bare(p, {"currency": pid_parts[3], "value": p["value"]}))
    for p in adm.get("skins", []):
        parts = p["iid"].split("|")
        skins.append(_bare(p, {"register": parts[1], "item": parts[2], "slots": parts[3].split("+"),
                               "text": p["text"]}))
    for p in adm.get("attacks", []):
        attacks.append(_bare(p, {"text": p["text"]}))
    for p in adm.get("freeform", []):
        parts = p["pid"].split("|")
        docs.append(_bare(p, {"register": parts[2], "part": parts[1], "text": p["text"],
                              "facts": dict(p["item"]["facts"]), "g3h": "ok" if detail[f"g3h|{p['pid']}"]["ok"] else
                              "not ok"}))
    for p in adm.get("wordings", []):
        f = reg.forms[p["form_id"]]
        words.append(_bare(p, {"qform": p["pid"].split("|")[1], "sem_id": f.sem_id, "form_id": p["form_id"],
                               "status": reg.status(p["form_id"]), "text": p["text"]}))
    for p in adm.get("comparators", []):
        f = reg.forms[p["form_id"]]
        _, sem, kind = p["pid"].split("|")[:3]
        cmps.append(_bare(p, {"sem_id": f.sem_id, "bound": kind, "form_id": p["form_id"],
                              "status": reg.status(p["form_id"]), "text": p["text"]}))
    for p in adm.get("precedence", []):
        f = reg.forms[p["form_id"]]
        precs.append(_bare(p, {"sem_id": f.sem_id, "form_id": p["form_id"], "status": reg.status(p["form_id"]),
                               "text": p["text"]}))
    return {"packs": packs, "skins": skins, "attacks": attacks, "documents": docs, "wordings": words,
            "comparators": cmps, "precedence": precs}


def lexicon_admitted(reg) -> dict:
    """The registry JSON with admitted forms only (sems and antonyms: all of them, from the plugin)."""
    o = reg.to_json()
    o["forms"] = [f for f in o["forms"] if f["status"] == "admitted"]
    o["note"] = "admitted forms only (G-LEX, 2/2 or 3/3); rejected and pending forms are in record/lexicon_record.json"
    return o


def counts(items: dict) -> dict:
    by = {}
    for stem, rows in items.items():
        c = Counter()
        for r in rows:
            c[("held" if r["held_out"] else "train")] += 1
            if "register" in r:
                c[f"register:{r['register']}"] += 1
            if "qform" in r:
                c[f"qform:{r['qform']}"] += 1
            if "bound" in r:
                c[f"bound:{r['bound']}"] += 1
            if "sem_id" in r:
                c[f"sem:{r['sem_id']}"] += 1
            if "currency" in r:
                c[f"currency:{r['currency']}"] += 1
        by[stem] = {"n": len(rows), **dict(sorted(c.items()))}
    return by


def shortfalls(items: dict, tasks: list, out: dict) -> list:
    """Each G0-lite target against what is admitted. Rows say whether the target is met."""
    n = {k: len(v) for k, v in items.items()}
    tasks_with = {}
    for t in tasks:
        if t["admitted"] > 0:
            tasks_with[t["pool"]] = tasks_with.get(t["pool"], 0) + 1
    detail = out["g3h_detail"]
    # every lexicon form a frozen piece uses must be admitted: a quarantined piece uses nothing, so this is 0 by
    # construction, and the check reads the frozen items to show it
    lex_used_not_admitted = sum(1 for pool in LEX_POOLS for r in items.get(pool, []) if r["status"] != "admitted")
    got = {
        ("packs", "kept packs"): n["packs"],
        ("packs", "pack tasks"): tasks_with.get("packs", 0),
        ("skins", "narrative-skin tasks"): tasks_with.get("skins", 0),
        ("freeform", "free-form tasks"): tasks_with.get("freeform", 0),
        ("wordings", "admitted question wordings"): n["wordings"],
        ("wordings", "question-wording tasks"): tasks_with.get("wordings", 0),
        ("wordings", "G-LEX used forms not admitted"): lex_used_not_admitted,
    }
    rows = []
    for t in G0_TARGETS:
        key = (t["pool"], t["metric"])
        if key not in got:
            continue                       # the G3-H bar is a per-template bar, reported below, not gated here
        val = got[key]
        met = (val >= t["target"]) if t["op"] == ">=" else (val == t["target"])
        rows.append({"pool": t["pool"], "metric": t["metric"], "target": t["target"], "op": t["op"],
                     "value": val, "met": met, "source": t["source"]})
    g3_ok = sum(1 for d in detail.values() if d["ok"])
    rows.append({"pool": "freeform", "metric": "G3-H notes matching their facts (aggregate, report only)",
                 "target": 98.0, "op": "per template", "value": round(100.0 * g3_ok / max(1, len(detail)), 2),
                 "met": None,
                 "source": "G0-lite s2 / C2 spec 6.3: >= 98% PER TEMPLATE. One note is one template, so each admitted "
                           "note passes its own template; the aggregate is reported, not gated"})
    cmp_kinds = Counter((r["sem_id"], r["bound"]) for r in items.get("comparators", []))
    cover = {f"{s}/{k}": cmp_kinds.get((s, k), 0) for s in P.CMP_SEMS for k in ("count", "cents")}
    rows.append({"pool": "comparators", "metric": "comparator forms cover both bound types for both sems",
                 "target": "cmp.le and cmp.lt, each with count and cents", "op": "covers", "value": cover,
                 "met": all(v > 0 for v in cover.values()),
                 "source": "G0-lite s2: comparator paraphrases typed count-percent or cents (G0 R5 percent cards and "
                           "R13 TOL_PCT need count-percent forms for cmp.le and cmp.lt)"})
    rows.append({"pool": "precedence", "metric": "precedence forms admitted (3/3)", "target": None, "op": None,
                 "value": n["precedence"], "met": None,
                 "source": "G0-lite s2: 3/3 precedence paraphrases (no count stated)"})
    rows.append({"pool": "comparators", "metric": "comparator forms admitted (2/2)", "target": None, "op": None,
                 "value": n["comparators"], "met": None,
                 "source": "G0-lite s2: comparator paraphrases 2/2 (no count stated)"})
    rows.append({"pool": "attacks", "metric": "pressure lines admitted", "target": None, "op": None,
                 "value": n["attacks"], "met": None, "source": "G0-lite s2: pressure lines (no count stated)"})
    return rows


def build() -> dict:
    out = XR.run()
    out["check"] = out["files"]
    adm, quar = piece_status(out)
    reg = out["res"]["reg"]
    tasks = task_table(out, adm)
    items = pool_items(out, adm)
    return {"out": out, "adm": adm, "quar": quar, "items": items, "tasks": tasks,
            "shortfalls": shortfalls(items, tasks, out), "lex_adm": lexicon_admitted(reg)}


def plan_report(b: dict) -> dict:
    out = b["out"]
    stages = Counter(q["stage"] for q in b["quar"])
    by_pool = {}
    for t in b["tasks"]:
        d = by_pool.setdefault(t["pool"], {"tasks": 0, "authored": 0, "admitted": 0})
        d["tasks"] += 1
        d["authored"] += t["pieces_authored"]
        d["admitted"] += t["admitted"]
    return {"family": FAMILY, "a38_frozen": paths.a38_frozen(), "g0_sha256_plugin": P.G0_SHA256_AUTHORED,
            "g0_sha256_file": _sha_bytes((HERE / "G0_SPEC.md").read_bytes()),
            "record_check": out["files"], "answer_files": {"expected": XR.EXPECTED_READS,
                                                          "returned": sum(1 for x in out["loaded"].values()
                                                                          for r in x[2] if r["answer_file"] == "ok")},
            "pools_by_task": by_pool, "admitted_counts": {k: len(v) for k, v in b["items"].items()},
            "quarantined_by_stage": dict(stages),
            "quarantined_G-LEX_forms": sorted({q["form_id"] for q in b["quar"] if q["stage"] == "G-LEX"}),
            "g3h_quarantined_notes": sorted(out["g3h_rep"]["quarantined"]),
            "g3h_by_register_info_only": _g3h_by_register(out),
            "shortfalls": b["shortfalls"]}


def _g3h_by_register(out: dict) -> dict:
    """Informational: the same G3-H results grouped by register (the alternative template reading, not applied)."""
    per = {}
    for iid, d in out["g3h_detail"].items():
        reg = iid.split("|")[3]
        c = per.setdefault(reg, {"notes": 0, "ok": 0})
        c["notes"] += 1
        c["ok"] += bool(d["ok"])
    for c in per.values():
        c["rate"] = round(100.0 * c["ok"] / c["notes"], 1)
    return dict(sorted(per.items()))


def freeze(b: dict) -> dict:
    stems = {}
    for stem, rows in b["items"].items():
        obj = {"family": FAMILY, "pool": stem, "g0_sha256": P.G0_SHA256_AUTHORED,
               "n": len(rows), "items": rows}
        paths.write_json(POOLS / f"{stem}.json", obj)
        stems[stem] = POOLS / f"{stem}.json"
    paths.write_json(POOLS / "lexicon.json", b["lex_adm"])
    stems["lexicon"] = POOLS / "lexicon.json"
    paths.write_json(POOLS / "quarantine.json", {"family": FAMILY, "n": len(b["quar"]), "items": b["quar"]})
    stems["quarantine"] = POOLS / "quarantine.json"
    files = {}
    for stem, p in sorted(stems.items()):
        files[p.name] = {"sha256": _sha_bytes(p.read_bytes()), "bytes": p.stat().st_size}
    rec = XR.RECORD
    rec_files = {}
    for name in ("RECORD.json", "lexicon_record.json", "g3h_record.json"):
        p = rec / name
        rec_files[f"record/{name}"] = _sha_bytes(p.read_bytes())
    answers = {}
    for p in sorted((EB.EXTRACT / "answers").glob("T12-extract_*.json")):
        answers[p.name] = _sha_bytes(p.read_bytes())
    manifest = {
        "family": FAMILY, "version": "pool-freeze-v1", "a38_frozen": paths.a38_frozen(),
        "g0_sha256": P.G0_SHA256_AUTHORED, "g0_spec_sha256_file": _sha_bytes((HERE / "G0_SPEC.md").read_bytes()),
        "extract_tasks_index_sha256": _sha_bytes((EB.EXTRACT / "TASKS.json").read_bytes()),
        "extraction_answers": {"expected": XR.EXPECTED_READS, "returned": len(answers), "sha256": answers},
        "record": rec_files,
        "pool_files": files,
        "admitted_counts": {k: len(v) for k, v in b["items"].items()},
        "counts": counts(b["items"]),
        "lexicon_forms_admitted": len(b["lex_adm"]["forms"]),
        "quarantined": {"total": len(b["quar"]), "by_stage": dict(Counter(q["stage"] for q in b["quar"])),
                        "file": "quarantine.json"},
        "shortfalls": b["shortfalls"],
        "tasks": b["tasks"],
        "no_rows_generated": True,
        "no_labels_set": True,
    }
    paths.write_json(POOLS / "manifest.json", manifest)
    return manifest


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args else "plan"
    if cmd not in ("plan", "freeze"):
        print(__doc__)
        return 2
    b = build()
    if cmd == "freeze":
        m = freeze(b)
        print(json.dumps({"written": str(POOLS), "admitted_counts": m["admitted_counts"],
                          "lexicon_forms_admitted": m["lexicon_forms_admitted"],
                          "quarantined": m["quarantined"]["by_stage"], "shortfalls": m["shortfalls"]},
                         ensure_ascii=False, indent=1, default=str))
        return 0
    print(json.dumps(plan_report(b), ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
