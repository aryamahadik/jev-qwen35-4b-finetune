"""c2_build/families/T29/dneg_i2.py: the double-negation round of T29 fix iteration 2 (G10 double_negation_share).

Shared code of the two stage scripts (dneg_stage2.py, dneg_stage3.py). The orchestrator runs Haiku between the stages;
nothing here runs a model.

  author   write_author(): the polarity-aware authoring tasks (authoring.build_dneg_tasks: 6 training items x 8 wordings,
           1 held-out item x 6) under haiku/dneg_i2/tasks/, answers to haiku/dneg_i2/answers/.
  stage 2  admit the authoring answers (authoring.wording_problems: one line, 8-30 words, placeholders, the (2, 2) negation
           profile, polarity rule), dedup, add the forms to the merged lexicon (frozen v1 + redo2), unit-test, and write
           the two independent G-LEX reads to haiku/dneg_i2/glex_tasks/.
  stage 3  record the G-LEX reads (2/2 agreeing extractors admit), write the pools/dneg/ supplement (wordings.jsonl,
           lexicon_merged.json, MANIFEST.json) that run_pilot_i2.py's loader reads, G13-seed handling, then the pilot steps.

Everything takes its folders as arguments so the tests can run in a temp dir.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from families.T29 import authoring as A  # noqa: E402
from families.T29 import extract as E  # noqa: E402
from families.T29 import plugin as P  # noqa: E402
from families.T29 import pool_freeze as PF  # noqa: E402

FAMILY = "T29"
VERSION = "dneg_i2"
DNEG = A.DNEG
ROOT = HERE / "haiku" / "dneg_i2"
GLEX_SUB = "glex_tasks"
POOL = HERE / "pools" / "dneg"
BASE_LEXICON = HERE / "pools" / "redo2" / "lexicon_merged.json"      # frozen v1 + redo2 admitted forms
LEX_READS = ("glex-r1", "glex-r2")
MIN_ADMITTED_FOR_POOL = 8          # at least this many admitted wordings (training) or the stage reports a shortfall
SLOTS = {"ACTION": "id", "TARGET": "id"}


# ------------------------------------------------------------------------------------------------ authoring
def author_tasks() -> list:
    return A.build_dneg_tasks()


def write_author(root: Path = ROOT) -> dict:
    """Write the authoring task files (haiku/dneg_i2/tasks/*.md + chunk manifests + TASKS.json)."""
    tasks = author_tasks()
    probs = A.check(tasks, root)
    if probs:
        raise SystemExit("STOP: dneg authoring check failed: " + "; ".join(probs[:5]))
    out, manifest = A.files(tasks, root, version=VERSION, g0_sha256=P.T29Plugin.G0_SHA256)
    out["answers/README.txt"] = "Haiku answer files: one <task_id>.json per task (see ../TASKS.json).\n"
    paths.write_files(root, out)
    return manifest


# ------------------------------------------------------------------------------------------------ stage 2
def base_registry() -> LX.LexiconRegistry:
    reg = LX.LexiconRegistry.from_json(json.loads(BASE_LEXICON.read_text(encoding="utf-8")))
    A.declare_dneg(reg)
    return reg


def collect(tasks: list, root: Path) -> tuple:
    """([piece], drops). Stops (SystemExit) if an answer file is missing, unreadable or does not map to its items."""
    pieces, drops = [], []
    for t in tasks:
        p = t.answer_file(root)
        if not p.is_file():
            raise SystemExit(f"STOP: dneg authoring answer missing: {p}")
        try:
            raw = {t.task_id: json.loads(p.read_text(encoding="utf-8"))}
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise SystemExit(f"STOP: dneg authoring answer is not JSON: {p}: {e}")
        out, probs = chunker.load_answers(t.batch, raw)
        if probs:
            raise SystemExit(f"STOP: {t.name}: answers do not map to their items: {probs[:3]}")
        for iid in sorted(out):
            vals = out[iid].get(t.field) if isinstance(out[iid], dict) else None
            if not isinstance(vals, list) or not all(isinstance(v, str) for v in vals):
                drops.append({"pid": iid, "task_id": t.task_id, "reasons": [f"shape: {t.field!r} is not a list of strings"]})
                continue
            for k, text in enumerate(vals):
                pieces.append({"pid": f"{iid}#{k:02d}", "text": text.strip(), "task_id": t.task_id,
                               "prompt_sha": t.batch.prompt_sha, "held_out": bool(t.held_out)})
    return pieces, drops


def admit_authoring(pieces: list, drops: list) -> tuple:
    """(survivors, drops): wording_problems() on every wording, then dedup inside the round (normalised text)."""
    surv, seen = [], set()
    for p in pieces:
        probs = A.wording_problems(DNEG, p["text"])
        if probs:
            drops.append({"pid": p["pid"], "task_id": p["task_id"], "reasons": probs})
            continue
        key = E._norm(p["text"])
        if key in seen:
            drops.append({"pid": p["pid"], "task_id": p["task_id"], "reasons": ["duplicate wording in the round"]})
            continue
        seen.add(key)
        surv.append(p)
    return surv, drops


def build_registry(surv: list) -> tuple:
    """(registry, {form id: piece}, drops): the merged lexicon plus the surviving wordings. A new form that fails its unit
    test, or that makes an old form fail its unit test (ambiguous span), is dropped; old forms are never touched."""
    reg = base_registry()
    old = set(reg.forms)
    new, drops = {}, []
    for p in surv:
        try:
            f = reg.add(p["text"], A.question_sem(FAMILY, DNEG),
                        slots=SLOTS, source="haiku", family=FAMILY, haiku_task_id=p["task_id"],
                        haiku_prompt_sha=p["prompt_sha"], held_out=p["held_out"])
            new[f.form_id] = p
        except LX.LexiconError as e:
            drops.append({"pid": p["pid"], "task_id": p["task_id"], "reasons": [f"form: {e}"]})

    def remove(fid: str, why: str) -> None:
        p = new.pop(fid)
        del reg.forms[fid]
        reg._rx.clear()
        drops.append({"pid": p["pid"], "task_id": p["task_id"], "reasons": [why]})

    for _ in range(10):
        reg.unit_test_all()
        broken = [fid for fid in old if not reg.forms[fid].unit_ok]
        if not broken:
            break
        culprits = set()
        for ofid in broken:
            of = reg.forms[ofid]
            for vals in reg._samples(of):
                sentence = f"Note: {reg.render(ofid, vals)}. Thanks."
                pbk = LX._params_by_kind({k: v.schema for k, v in vals.items()})
                culprits |= {n for n in new if reg._regex(reg.forms[n], pbk, False).search(sentence)}
        if not culprits:
            raise SystemExit(f"STOP: old forms fail their unit test with no dneg culprit: {broken[:3]}")
        for n in sorted(culprits):
            remove(n, "form: breaks the unit test of a frozen form (ambiguous span)")
    for fid in [f for f in sorted(new) if not reg.forms[f].unit_ok]:
        remove(fid, "unit test: " + "; ".join(reg.forms[fid].unit_problems)[:200])
    reg.unit_test_all()
    broken = [f for f in list(old) + list(new) if not reg.forms[f].unit_ok]
    if broken:
        raise SystemExit(f"STOP: forms fail their unit test after the dneg merge: {broken[:3]}")
    return reg, new, drops


def glex_batches(reg, new_ids: list) -> list:
    """[(read, 'extract_lex', batch)]: two independent reads, each with its own filled instance and choice order."""
    out = []
    for instance, label in enumerate(LEX_READS):
        items = E.glex_items(reg, new_ids, f"t29-extract-{VERSION}-{label}", instance)
        out.append((label, "extract_lex", chunker.make_batch("extract_lex", FAMILY, items,
                                                              seed=f"t29-extract-{VERSION}-{label}",
                                                              prompt=E.GLEX_PROMPT)))
    return out


def glex_files(root: Path, batches: list) -> tuple:
    files, manifest = E.files_for(root / GLEX_SUB, batches)
    manifest = dict(manifest, version=VERSION, stage="extract (dneg_i2: the new double-negation wordings only)",
                    reads_per_form={"question": 2})
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return files, manifest


# ------------------------------------------------------------------------------------------------ stage 3
def restore_registry(state: dict) -> tuple:
    """Rebuild the stage-2 registry from the saved state (same forms in the same order -> same form ids and batches)."""
    reg = base_registry()
    for f in state["forms"]:
        g = reg.add(f["text"], A.question_sem(FAMILY, DNEG),
                    slots=SLOTS, source="haiku", family=FAMILY, haiku_task_id=f["task_id"],
                    haiku_prompt_sha=f["prompt_sha"], held_out=f["held_out"])
        if g.form_id != f["form_id"]:
            raise SystemExit(f"STOP: form id changed on rebuild: {f['form_id']} -> {g.form_id}")
    reg.unit_test_all()
    return reg


def load_reads(batches: list, root: Path) -> tuple:
    reads, problems = {}, []
    for read, kind, b in batches:
        raw = {}
        for c in b.chunks:
            p = root / GLEX_SUB / b.answer_path(c["task_id"])
            if not p.is_file():
                problems.append(f"{read} {c['task_id']}: answer file missing")
                continue
            try:
                raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                problems.append(f"{read} {c['task_id']}: answer is not JSON: {e}")
        got, probs = chunker.load_answers(b, raw)
        problems += [f"{read}: {x}" for x in probs]
        reads[read] = {"batch": b, "answers": got}
    return reads, problems


def record_reads(reg, reads: dict) -> tuple:
    """Record each read's extraction on the registry. Returns (invalid rows, recorded per read)."""
    invalid, n_rec = [], Counter()
    for read in LEX_READS:
        b = reads[read]["batch"]
        tid_of = {b.key[q]: b.task_of[q] for q in b.key}
        for fid in sorted(reads[read]["answers"]):
            ans, f = reads[read]["answers"][fid], reg.forms[fid]
            meaning = ans.get("meaning") if isinstance(ans, dict) else None
            sem = reg.meaning_to_sem(f.kind, meaning) if isinstance(meaning, str) else None
            if sem is None:
                invalid.append({"stage": "extract-invalid", "read": read, "iid": fid, "task_id": tid_of[fid],
                                "reason": f"meaning is not one of the {f.kind} choices: {str(meaning)[:160]!r}"})
                continue
            reg.record_extraction(fid, f"haiku:{tid_of[fid]}", sem)
            n_rec[read] += 1
    return invalid, dict(n_rec)


def write_supplement(reg, state: dict, pool: Path, extra: dict) -> dict:
    """Admitted wordings (2/2 G-LEX AND wording_problems again) -> pools/dneg/. Returns the summary."""
    new_ids = [f["form_id"] for f in state["forms"]]
    status = {fid: reg.status(fid) for fid in new_ids}
    adm = [fid for fid in new_ids if status[fid] == "admitted" and not A.wording_problems(DNEG, reg.forms[fid].text)]
    quar = [{"stage": "g-lex" if status[fid] != "admitted" else "wording_problems", "iid": fid,
             "reason": f"{status[fid]}: extractions {[[e, s] for e, s in reg.forms[fid].extractions]}"}
            for fid in new_ids if fid not in adm]
    lex_obj, gate = PF.freeze_lexicon(reg)
    keep = set(adm) | {x["form_id"] for x in lex_obj["forms"] if x["form_id"] not in set(new_ids)}
    lex_obj["forms"] = [x for x in lex_obj["forms"] if x["form_id"] in keep]
    wordings = PF.freeze_wordings(reg, adm)
    files = {"wordings.jsonl": PF.jsonl(wordings), "lexicon_merged.json": PF.js(lex_obj),
             "quarantine.jsonl": PF.jsonl(quar)}
    shas = {}
    for rel, text in sorted(files.items()):
        paths.write_text(pool / rel, text)
        shas[rel] = PF.sha_text(text)
    summary = {"new_forms": len(new_ids), "status": dict(Counter(status.values())), "admitted": len(adm),
               "admitted_training": sum(1 for f in adm if not reg.forms[f].held_out),
               "admitted_held_out": sum(1 for f in adm if reg.forms[f].held_out), "quarantined": len(quar),
               "g_lex_gate": {k: gate[k] for k in ("n_forms", "status_counts", "pass")}, **extra}
    manifest = {"family": FAMILY, "supplement": "dneg_i2", "base_lexicon": str(BASE_LEXICON.relative_to(HERE)),
                "base_lexicon_sha256": PF.sha_file(BASE_LEXICON),
                "g0_spec_sha256": PF.sha_file(HERE / "G0_SPEC.md"),
                "matches_plugin_G0_SHA256": PF.sha_file(HERE / "G0_SPEC.md") == P.T29Plugin.G0_SHA256,
                "summary": summary, "pool_files": {rel: {"sha256": shas[rel]} for rel in sorted(shas)},
                "decisions": ["Supplement only: pools/*.jsonl, pools/redo2/ and their manifests are unchanged. "
                              "run_pilot_i2.py's loader reads lexicon_merged.json (replaces redo2's registry) and wordings.jsonl.",
                              "Admission: authoring.wording_problems (negation profile 2/2 + polarity) before the G-LEX reads and "
                              "again at admission; G-LEX 2/2 distinct agreeing extractors; any other meaning rejects for good."]}
    paths.write_text(pool / "MANIFEST.json", PF.js(manifest))
    return {"summary": summary, "admitted_form_ids": adm, "admitted_texts": {f: reg.forms[f].text for f in adm}}


def state_order(reg, new: dict) -> list:
    """The new form ids in the order they were added (dict order of `new` = add order, minus the removed ones)."""
    return [f for f in new]
