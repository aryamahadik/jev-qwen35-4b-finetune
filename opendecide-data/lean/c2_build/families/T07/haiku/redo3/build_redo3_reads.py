#!/usr/bin/env python3
"""families/T07/haiku/redo3/build_redo3_reads.py: T07 REDO-3, stage 2: lint and dedup of the redo3 author answers, then
the G-LEX read tasks for the new lexicon pieces (a NEW file; build_redo3.py and every earlier file are untouched).

Input: the two redo3 author answers (build_redo3.py: 3 yn_misses training wordings, 17 packs). Answers are validated
against their contract first (VA.validate_all); a failed-audit task id would be passed in by the orchestrator and its
file is then never read (none failed in this round).

What each piece type needs (G0_SPEC.md section 4):
  packs      authoring.lint_pack, then authoring.check_packs over the kept v1 packs FIRST and the new clean packs after
             them (a clashing new pack is dropped whole; no kept v1 pack may change), then three program checks that
             only restate rules the pack prompt printed: (a) no word of a taken-word list (seed surfaces + the 49 kept
             packs' words) in any value, (b) no kept-pack or seed store / customer name holds a NEW surface as a whole
             word (G0 S2 / H6, the direction check_packs does not look at), (c) no level / region / category word is a
             word of an admitted pool text or of a wording that goes to the reads (build_redo3.pack_pool_collisions).
             A pack is not a lexicon form: it has no G-LEX or G3-H read. G13-seed is not run (as in v1).
  wordings   authoring.lint_wording (G-SL included, negation 0/0 for yn_misses, one question, no benefit / value word) +
             the redo3 brief (the verb phrase 'lose out on' in any tense, no other outcome verb), dedup against every
             earlier text (v1 + redo2 pieces, canonical sentences and every registered form), registry add + unit test
             on a registry that already holds every v1 and redo2 form WITH their recorded reads (no earlier status may
             change), then 2 independent G-LEX reads (T07 has no 3/3 kind): each read is its own batch, its own chunk
             and its own task + answer file; the item shows the wording filled with values of its own kind
             (R1: a customer name, an ORD id, a benefit) and the 7 question meanings (the v1 closed list, unchanged).
No Mode F text and no condition sentence was authored in redo3, so there is no G3-H read.

Nothing here reads or sets a label or a gold; no gate bar, target or lint check changes. Every write goes through
c2_kit.paths (A38 guard and never-open guard). Run from lean/c2_build:
  .venv/bin/python -B families/T07/haiku/redo3/build_redo3_reads.py reads [--write]   # lint, dedup, registry, tasks
  .venv/bin/python -B families/T07/haiku/redo3/build_redo3_reads.py validate          # strict check of the read answers
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
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
from c2_kit.lexicon import LexiconError, question_sem  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import merged_pools as MP  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07 import validate_answers as VA  # noqa: E402
from families.T07.haiku import extract_build as EB  # noqa: E402
from families.T07.haiku.redo2 import build_redo2 as R2  # noqa: E402
from families.T07.haiku.redo3 import build_redo3 as R3  # noqa: E402

FAMILY = "T07"
VERSION = "r3"
SEED = R3.SEED                                            # "t07-redo3-v1"
READS_ROOT = HERE / "reads"
READS = ("redo3-r1", "redo3-r2")                         # G-LEX 2/2: two fresh agents, separate batches and files
QFORM = "yn_misses"
_PH = re.compile(r"\{[A-Za-z0-9_|]+\}")
_LOSE = re.compile(r"\b(?:lose|loses|lost|losing)\s+out\s+on\b", re.I)
_OTHER_VERBS = re.compile(r"\b(?:forfeit\w*|go(?:es|ing)? short|gone short|shut out|miss(?:es|ed|ing)?|fail\w*|"
                          r"den(?:y|ies|ied|ying)|withh\w+|lack\w*|without)\b", re.I)


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ author answers
def gap_dict() -> dict:
    """The gaps redo3 was written for, from its own TASKS.json (not from the pools, which change at admit)."""
    g = _json(R3.ROOT / "TASKS.json")["gaps"]
    return {"wording": g[R3.LINE_WORD], "packs": g[R3.LINE_PACKS]}


def load_author_answers(batches: dict) -> tuple:
    """(pieces, problems): every output of every redo3 author answer, shaped as build_redo2.load_author_answers."""
    pieces, probs = [], []
    for name, (b, plan, spec) in batches.items():
        field = spec[2]
        raw = {}
        for c in b.chunks:
            p = R3.ROOT / b.answer_path(c["task_id"])
            if not p.is_file():
                probs.append(f"{c['task_id']}: no answer file")
                continue
            try:
                raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
            except (ValueError, UnicodeDecodeError) as e:
                probs.append(f"{c['task_id']}: answer is not JSON ({e})")
        got, more = chunker.load_answers(b, raw)
        probs += more
        task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
        for iid, a in sorted(got.items()):
            outs = a.get(field) if isinstance(a, dict) else None
            outs = [outs] if field in ("text", "pack") else outs
            if not isinstance(outs, list):
                probs.append(f"{iid}: field {field} missing")
                continue
            for j, o in enumerate(outs):
                pieces.append({"piece_id": f"{iid}#{j}", "internal_id": iid, "task_id": task_of[iid],
                               "haiku_prompt_sha": b.prompt_sha, "value": o, "meta": plan[iid], "batch": name})
    return pieces, probs


# ------------------------------------------------------------------------------------------------ wordings
def lint_wording(text) -> list:
    """The v1 closed checks (G-SL included) with the 49 kept packs' words, plus the redo3 brief: 'lose out on' in any
    tense and no other outcome verb. The brief check only restates what the task asked; it removes nothing the v1
    checks keep."""
    if not isinstance(text, str):
        return ["not a string"]
    probs = A.lint_wording(QFORM, text, R2.PACK_WORDS)
    lit = _PH.sub(" ", text)
    if not _LOSE.search(lit):
        probs.append("brief: the verb phrase 'lose out on' is missing")
    other = sorted({m.group(0).lower() for m in _OTHER_VERBS.finditer(lit)})
    if other:
        probs.append(f"brief: another outcome verb or negation {other}")
    return probs


def seen_texts() -> dict:
    """{(group, normalised text): where}: every v1 and redo2 author output (kept or dropped), every canonical
    sentence and every text already registered in the v1 or redo2 lexicon. A redo3 piece equal to one is a duplicate."""
    seen = R2.v1_seen()
    pieces, _ = R2.load_author_answers(R2.build_batches())
    for p in pieces:
        if isinstance(p["value"], str):
            seen.setdefault((EB.group(p["meta"]["piece"]), EB.norm(p["value"])), "redo2 " + p["piece_id"])
    for f in MP.load(through=R3.BASELINE)["lexicon"]:
        seen.setdefault(("lex", EB.norm(f["text"])), "lexicon " + f["form_id"])
    return seen


def merged_registry() -> tuple:
    """(registry, {form_id: recorded status}): every v1 form and every redo2 form (canonical pair, paraphrases,
    wordings) rebuilt under its recorded id with its recorded extractions, unit tested; any status that differs from
    the record stops the run."""
    reg, v1_rows = R2.v1_registry()
    recorded = {r["form_id"]: r["status"] for r in v1_rows}
    add = _json(R2.SUPP / "lexicon_add.json")
    psha = {r["task_id"]: r["prompt_sha"] for r in _json(R2.ROOT / "TASKS.json")["tasks"]}
    for r in add["forms"]:
        slots = (A.wording_slots(r["sem_id"].split(".", 2)[2]) if r["kind"] == "question"
                 else {"X": P.BOUND_KIND[P.SEMS[r["sem_id"]][0]]})
        if r["source"] == "claude":
            f = reg.add(r["text"], r["sem_id"], slots=slots, family=FAMILY)
        else:
            f = reg.add(r["text"], r["sem_id"], slots=slots, source="haiku", family=FAMILY,
                        haiku_task_id=r["haiku_task_id"], haiku_prompt_sha=psha[r["haiku_task_id"]],
                        held_out=r["held_out"])
        if f.form_id != r["form_id"]:
            raise SystemExit(f"STOP: redo2 form id drift {r['form_id']} -> {f.form_id}")
        f.extractions = [tuple(e) for e in r["extractions"]]
        recorded[f.form_id] = r["status"]
    reg.unit_test_all()
    drift = sorted(fid for fid, s in recorded.items() if reg.status(fid) != s)
    if drift:
        raise SystemExit(f"STOP: recorded statuses differ from the rebuilt registry: {drift[:3]}")
    return reg, recorded


def _add_wording(reg, p) -> object:
    return reg.add(p["value"], question_sem(FAMILY, QFORM), slots=A.wording_slots(QFORM), source="haiku",
                   family=FAMILY, haiku_task_id=p["task_id"], haiku_prompt_sha=p["haiku_prompt_sha"], held_out=False)


def build_registry(cands: list, drops: list) -> tuple:
    """(registry, {form_id: piece}, recorded): the merged registry + the new wordings, unit tested. A wording that the
    registry refuses, that fails its unit test, or whose presence changes an earlier form's status is dropped (logged);
    the registry is rebuilt without it."""
    bad: set = set()
    for _attempt in range(len(cands) + 1):
        reg, recorded = merged_registry()
        origin = {}
        for p in cands:
            if p["piece_id"] in bad:
                continue
            try:
                f = _add_wording(reg, p)
            except LexiconError as e:
                drops.append({"piece_id": p["piece_id"], "piece": "wording", "stage": "registry", "reason": str(e)})
                bad.add(p["piece_id"])
                continue
            origin[f.form_id] = p
        reg.unit_test_all()
        changed = sorted(fid for fid, s in recorded.items() if reg.status(fid) != s)
        if not changed:
            return reg, origin, recorded
        culprits = set()                                  # which new wording alone breaks an earlier form
        for p in cands:
            if p["piece_id"] in bad:
                continue
            r2, rec2 = merged_registry()
            _add_wording(r2, p)
            r2.unit_test_all()
            if any(r2.status(fid) != s for fid, s in rec2.items()):
                culprits.add(p["piece_id"])
        if not culprits:
            raise SystemExit(f"STOP: an earlier form changed status ({changed[:3]}) with no single culprit")
        for pid in sorted(culprits):
            drops.append({"piece_id": pid, "piece": "wording", "stage": "registry",
                          "reason": "its presence changes an earlier form's G-LEX status"})
        bad |= culprits
    raise SystemExit("STOP: earlier forms still change status after dropping wordings")


# ------------------------------------------------------------------------------------------------ packs
def _whole(surface: str, name: str) -> bool:
    return re.search(r"(?<![a-z])" + re.escape(surface) + r"(?![a-z])", name.casefold()) is not None


def pack_decisions(pieces: list, word_texts: list) -> list:
    """[{piece_id, internal_id, store, status 'kept'|'dropped', reasons}] in piece order (see the module docstring).
    word_texts: the wordings that go to the reads (a pack word must not be one of their words)."""
    kept_v1 = R2.kept_packs()
    packs = [p for p in pieces if p["meta"]["piece"] == "pack"]
    for p in packs:
        p["lint"] = A.lint_pack(p["value"], p["meta"]["ladder_levels"]) if isinstance(p["value"], dict) else ["not an object"]
    drops: list = []
    clean = EB.dedup([p for p in packs if not p["lint"]], drops, {})        # whole-pack duplicates
    dup_ids = {d["piece_id"] for d in drops}
    kept, dropped = A.check_packs(kept_v1 + [p["value"] for p in clean])
    if kept[:len(kept_v1)] != kept_v1:
        raise SystemExit("STOP: check_packs changed a kept v1 pack")
    kept_ids = {id(x) for x in kept}
    old_names = ([p["store"] for p in kept_v1] + [c for p in kept_v1 for c in p["customers"]] + list(P.STORES) +
                 list(P.STORES_HELD) + list(P.CUSTOMERS) + list(getattr(P, "CUSTOMERS_HELD", ())))
    wording_words = set()
    for t in word_texts:
        wording_words |= set(A._words(_PH.sub(" ", t)))
    pools = MP.load(through=R3.BASELINE)
    pool_w = R3.pool_words(pools)
    out = []
    for p in sorted(packs, key=lambda x: x["piece_id"]):
        v, reasons = p["value"], list(p["lint"])
        if not reasons and p["piece_id"] in dup_ids:
            reasons.append("dedup: identical to another pack")
        if not reasons and id(v) not in kept_ids:
            d = next(x for x in dropped if x["pack"] is v)
            reasons.append(f"S2 uniqueness (check_packs): clash {d['clash']} holds {d['holds']} store_taken {d['store_taken']}")
        if not reasons:
            surfaces = [s.casefold() for f in ("ladder", "regions", "categories") for s in v[f]]
            rev = sorted({(s, n) for s in surfaces for n in old_names if _whole(s, n)})
            if rev:
                reasons.append(f"S2 (H6): an existing store or customer name holds a new surface {rev[:3]}")
            vals = [v["store"], *v["ladder"], *v["regions"], *v["categories"], *v["customers"]]
            taken = sorted({w for x in vals for w in A._words(x)} & R3.TAKEN_WORDS)
            if taken:
                reasons.append(f"taken word(s) {taken}")
            words = {w for f in ("ladder", "regions", "categories") for x in v[f] for w in A._words(x)}
            coll = sorted(words & pool_w)
            if coll:
                reasons.append(f"word(s) already in an admitted pool text {coll}")
            wcoll = sorted(words & wording_words)
            if wcoll:
                reasons.append(f"word(s) in a new wording {wcoll}")
        out.append({"piece_id": p["piece_id"], "internal_id": p["internal_id"], "task_id": p["task_id"],
                    "ladder_levels": p["meta"]["ladder_levels"], "store": v.get("store") if isinstance(v, dict) else None,
                    "status": "dropped" if reasons else "kept", "reasons": reasons})
    return out


# ------------------------------------------------------------------------------------------------ the reads
def read_items(reg, fids: list, read: str) -> list:
    """G-LEX items of one read: the wording filled with values of its own kind (R1; seeded by the form id, so both
    reads see the same text) and the meanings of its kind in an order seeded by (read, form)."""
    out = []
    for fid in sorted(fids):
        f = reg.forms[fid]
        txt = reg.render(fid, R2.read_values(reg, fid))
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: _sha(f"{SEED}|{read}|{fid}|{m}"))
        out.append((fid, {"text": txt, "choices": mean}))
    return out


def read_batch(reg, fids: list, read: str):
    return chunker.make_batch("extract_lex", FAMILY, read_items(reg, fids, read), seed=f"{SEED}|glex|{read}",
                              prompt=EB.LEX_PROMPT)


def read_task_text(b, tid: str, read: str, root: Path = READS_ROOT) -> str:
    chunk = next(c for c in b.chunks if c["task_id"] == tid)
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    shape = '{"qid": "%s", "meaning": "<one choice, copied exactly>"}' % qids[0]
    return "\n".join([
        f"# T07 redo3 G-LEX read task {tid} (kind {b.kind}; read {read})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
        "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):",
        f"- The answer file holds one JSON array with exactly {n} object{'s' if n != 1 else ''}: one per item below, "
        "each item answered once.",
        '- Each object has exactly two keys: "qid" and "meaning". No other keys.',
        f"- \"qid\": copy the item's qid exactly. The qids of this task: {', '.join(qids)}.",
        '- "meaning": one of the item\'s "choices", copied character for character.',
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments.",
        f"Literal shape: [{shape}" + (", ..." if n > 1 else "") + "]", "",
        f"Task kind: {b.kind}; read {read}; items: {n}; outputs expected: {n}.", "",
        "## Instructions", "", b.prompt.rstrip(), "",
        f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def state() -> dict:
    """Everything the stage computes, in memory."""
    g = gap_dict()
    files, _index = R3.author_files(g=g)
    diff = R3.check_on_disk(R3.ROOT, files)
    if diff:
        raise SystemExit(f"STOP: redo3 author files on disk differ from the rebuild: {diff[:3]}")
    rep = VA.validate_all(rounds={"redo3-author": R3.ROOT})
    if not rep["ok"]:
        raise SystemExit("STOP: redo3 author answers break their contract: " + json.dumps(rep["invalid_task_ids"]))
    pieces, probs = load_author_answers(R3.build_batches(g))
    if probs:
        raise SystemExit("STOP: redo3 author answers incomplete:\n" + "\n".join(probs[:20]))
    drops: list = []
    words = [p for p in pieces if p["meta"]["piece"] == "wording"]
    for p in words:
        p["lint"] = lint_wording(p["value"])
        if p["lint"]:
            drops.append({"piece_id": p["piece_id"], "piece": "wording", "stage": "lint", "reason": p["lint"]})
    ok = [p for p in words if not p["lint"]]
    cands = EB.dedup(ok, drops, seen_texts())
    reg, origin, _rec = build_registry(cands, drops)
    new_fids = sorted(origin)
    unit_fail = [fid for fid in new_fids if not reg.forms[fid].unit_ok]
    for fid in unit_fail:
        drops.append({"piece_id": origin[fid]["piece_id"], "form_id": fid, "stage": "unit_test",
                      "reason": reg.forms[fid].unit_problems[:3]})
    read_fids = [fid for fid in new_fids if reg.forms[fid].unit_ok]
    packs = pack_decisions(pieces, [origin[fid]["value"] for fid in read_fids])
    batches = {r: read_batch(reg, read_fids, r) for r in READS} if read_fids else {}
    return {"gaps": g, "pieces": pieces, "wording_drops": drops, "reg": reg, "origin": origin, "new_fids": new_fids,
            "read_fids": read_fids, "packs": packs, "batches": batches}


def read_files(st: dict) -> tuple:
    files, rows = {}, []
    for read, b in st["batches"].items():
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = read_task_text(b, tid, read)
            files[tfile] = text
            ans = str(READS_ROOT / b.answer_path(tid))
            rows.append({"task": f"{read}-{b.kind}", "task_id": tid, "kind": b.kind, "read": read,
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "task_file": str(READS_ROOT / tfile),
                         "answer_file": ans, "n_items": len(c["items"]), "outputs_expected": len(c["items"]),
                         "task_sha256": chunker.sha(text),
                         "allowed_read": sorted({str(READS_ROOT / tfile)} | b.allowed(str(READS_ROOT), tid)[0]),
                         "allowed_write": [ans]})
    reg = st["reg"]
    kept = [d for d in st["packs"] if d["status"] == "kept"]
    plan = {"family": FAMILY, "version": VERSION, "note": "orchestrator side only; never sent to Haiku",
            "reads": {r: b.batch_id for r, b in st["batches"].items()},
            "lex": {fid: {"piece_id": st["origin"][fid]["piece_id"], "sem": reg.forms[fid].sem_id,
                          "kind": reg.forms[fid].kind, "text": reg.forms[fid].text, "held_out": False,
                          "haiku_task_id": reg.forms[fid].haiku_task_id}
                    for fid in st["read_fids"]},
            "wording_drops": st["wording_drops"],
            "packs": {"asked": len(st["packs"]), "kept": len(kept), "dropped": len(st["packs"]) - len(kept),
                      "kept_v1_plus_redo3": len(R2.kept_packs()) + len(kept), "decisions": st["packs"],
                      "note": "packs are not lexicon forms: no G-LEX or G3-H read; G13-seed not run (as in v1)"}}
    index = {"family": FAMILY, "version": VERSION, "seed": SEED, "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED,
             "gate": {"G-LEX": "2/2 (redo3-r1, redo3-r2; T07 has no 3/3 kind; items show values of the form's own kind)"},
             "n_tasks": len(rows), "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["plan/READS_PLAN.json"] = json.dumps(plan, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo3 G-LEX read task (see ../reads/"
                                   "TASKS.json). Written only by the task agents.\n")
    return files, index


def check_reads(files: dict, st: dict) -> list:
    """Problems with the read tasks (empty = ready): sizes, leaks, paths, independence."""
    probs = []
    ids = set(st["reg"].forms)
    for read, b in st["batches"].items():
        for c in b.chunks:
            tid = c["task_id"]
            text = files[f"tasks/{tid}.md"]
            if not 1 <= len(c["items"]) <= chunker.MAX_ITEMS:
                probs.append(f"{tid}: {len(c['items'])} items")
            if any(i in text for i in ids) or any(i in text for i in b.key.values()):
                probs.append(f"{tid}: internal form id in the task text")
            ans = READS_ROOT / b.answer_path(tid)
            if str(ans) not in text.split("\n")[3]:
                probs.append(f"{tid}: answer path missing from the top")
            for pth in (READS_ROOT / f"tasks/{tid}.md", ans):
                if paths.never_open(pth):
                    probs.append(f"{tid}: never-open path {pth}")
            if sorted(it["text"] for it in c["items"]) != sorted(
                    t for t in (reg_text(st, fid) for fid in st["read_fids"])):
                probs.append(f"{tid}: items differ from the forms to read")
    if st["batches"]:
        b1, b2 = (st["batches"][r] for r in READS)
        if {c["task_id"] for c in b1.chunks} & {c["task_id"] for c in b2.chunks}:
            probs.append("the two reads share a task id")
        if set(b1.key) & set(b2.key):
            probs.append("the two reads share an opaque id")
    return probs


def reg_text(st: dict, fid: str) -> str:
    return st["reg"].render(fid, R2.read_values(st["reg"], fid))


def validate() -> int:
    rep = VA.validate_all(rounds={"redo3-reads": READS_ROOT})
    for r in rep["rounds"]:
        print(f"{r['round']}: {r['valid']}/{r['tasks']} valid; invalid {len(r['invalid'])}; missing {len(r['missing'])}; "
              f"ignored {len(r['ignored'])}; extra files {r['extra_files']}")
        for x in r["invalid"]:
            print("  INVALID", x["task_id"], x["problems"][:6])
    return 0 if rep["ok"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=("reads", "validate"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if args.stage == "validate":
        return validate()
    st = state()
    files, index = read_files(st)
    probs = check_reads(files, st) if st["batches"] else []
    if probs:
        print("\n".join(probs))
        return 1
    if args.write and st["batches"]:
        paths.write_files(READS_ROOT, files)
    kept = [d for d in st["packs"] if d["status"] == "kept"]
    print(json.dumps({
        "wording_pieces": sum(p["meta"]["piece"] == "wording" for p in st["pieces"]),
        "wording_drops_by_stage": dict(Counter(d["stage"] for d in st["wording_drops"])),
        "wordings_to_read": [st["reg"].forms[f].text for f in st["read_fids"]],
        "packs_asked": len(st["packs"]), "packs_kept": len(kept),
        "packs_dropped": [(d["piece_id"], d["reasons"]) for d in st["packs"] if d["status"] == "dropped"],
        "packs_total_with_v1": len(R2.kept_packs()) + len(kept),
        "tasks": [(r["task"], r["task_id"], r["n_items"]) for r in index["tasks"]], "n_tasks": index["n_tasks"],
        "written": bool(args.write and st["batches"])}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
