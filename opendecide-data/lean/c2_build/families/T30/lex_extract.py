"""families/T30/lex_extract.py: the T30 lint, dedup and G-LEX extraction stage (C2_DATA_SPEC 6.2 item 4; G0_SPEC 3.6).

Input: the authoring answers under haiku/author/answers (every task answered; authoring.load() reads them). Output
(after A38 only, through paths.write_files):
  haiku/extract/             two independent blind G-LEX reads of every wording that survives lint, dedup and the
                             lexicon unit test. Each read is its own batch: own seed, own opaque ids, own chunk files,
                             own answer files. The key (opaque id -> form id) sits in key/ and is never sent to Haiku.
  haiku/extract/prep_log.json  counts, and one line per dropped piece (task, internal id, stage, reason)

Stages (deterministic from the answer files, so the next stage rebuilds the same registry):
  1 load      authoring.load(): every piece with its checker problems. G-SL runs inside the checkers: gsl.lint_template
              for skins, wordings and attack lines (plus negcount and the option-text check); check_pack for packs;
              name checks for names.
  2 G-SL      gsl.lint_values on the slot values of the passing packs (action phrases, titles, details) and names.
  3 dedup     packs by content; skins, attack lines and wordings by casefold + whitespace text (first copy kept); a
              wording text that appears under two question forms is dropped under both; names through
              authoring.check_pools (first, pair, last and requester pools).
  4 G-LEX     each surviving wording becomes a lexicon form (kind "question", sem question_sem(T30, qform), source
              "haiku" with its task id and prompt sha). The unit test runs on the whole candidate registry until it is
              stable; a form that fails it is dropped and never admitted. Precedence and window kinds: none in T30.
  5 extract   two reads of every surviving form: lexicon_items() with two different choice orders, one make_batch per
              read (make_batch refuses more than 50 items per chunk, so each read is several chunk files).

Nothing here sets a label. A read picks a meaning from the closed list; the admission step compares it with the form's
own sem id (lexicon.record_extraction), and any disagreement rejects that form for good.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict

from c2_kit import chunker, gsl, paths
from c2_kit import slots as S
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem
from families.T30 import authoring as A
from families.T30 import fixtures as FX
from families.T30 import plugin as T

FAMILY = "T30"
EXTRACT = A.ROOT.parent / "extract"          # families/T30/haiku/extract
EXTRACT_SEED = "t30-extract-lex-v1"
# (read label, batch seed, choice-order seed): two independent reads of every form
READS = (("readA", "T30|extract_lex|readA", "glex|T30|readA"),
         ("readB", "T30|extract_lex|readB", "glex|T30|readB"))
PROMPT_LEX = """You are a blind reader for a meaning check. Each item in your chunk file is one question text with a list of choices.

TASK
For each item, read its "text" by itself and pick the one entry of its "choices" list that says what the text asks. Copy that entry exactly, character for character.

RULES
R1. Read only your chunk file. Open no other file or folder, and write nothing except the answer file.
R2. Judge each text by its own words. Items do not depend on each other; never compare one item with another.
R3. Every item has one choice that fits best. Pick it even when the wording is unusual.
R4. Your meaning must be copied from that item's "choices" list. If two choices look close, pick the one whose wording matches the text more closely.
R5. Give every item exactly one answer. Do not add notes.

OUTPUT
Write the answer file named in the ANSWER FILE line at the end of your instructions. It holds one JSON list with one object per item: {"qid": "<the item's qid>", "meaning": "<the chosen choice, copied exactly>"}. The file holds only that JSON list."""


def _norm(text) -> str:
    return " ".join(str(text).casefold().split())


def _vkey(v):
    return json.dumps(v, sort_keys=True) if isinstance(v, (list, tuple)) else v


def _category(iid: str) -> str:
    p = iid.split(":")
    return f"name_{p[1]}" if p[0] == "names" else p[0]


def _short(problems) -> str:
    return "; ".join(str(x) for x in problems)[:240]


def _slot_or_problem(make, value, label, out):
    try:
        return make(value)
    except S.SlotError as e:
        out.append(f"{label}: {e}")
        return None


def value_lint(iid: str, piece) -> list:
    """G-SL on the slot values of one passing piece (gsl.lint_values). Names: each name. Packs: each action phrase
    (category slot), each title and detail (name slot). Returns the violations (empty = clean)."""
    out, slots = [], {}
    p = iid.split(":")
    if p[0] == "names":
        vals = list(piece) if p[1] == "pairs" else [piece]
        for i, v in enumerate(vals):
            s = _slot_or_problem(S.name_slot, v, f"name {v!r}", out)
            if s is not None:
                slots[f"n{i}"] = s
    elif p[0] == "pack":
        rt, probs = A.check_pack(p[1], piece)
        if rt is None:
            return list(probs) or ["pack does not check"]
        phrases = list(piece["low_actions"]) + list(piece["consequential_actions"])
        for i, ph in enumerate(phrases):
            s = _slot_or_problem(lambda x, rt=rt: S.category_slot(x, rt.action_set), ph, f"action {ph!r}", out)
            if s is not None:
                slots[f"a{i}"] = s
        for i, t in enumerate(list(piece.get("titles", [])) + list(piece.get("details", []))):
            s = _slot_or_problem(S.name_slot, t, f"value {t!r}", out)
            if s is not None:
                slots[f"v{i}"] = s
    if slots:
        out += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_values(slots)]
    return out


# ================================================================================================ stage 1-2: lint
def lint_stage(recs: dict, info: dict, log: dict):
    kept, authored = [], Counter()
    for tid in sorted(recs, key=lambda t: info[t]["label"]):
        r = recs[tid]
        for iid, piece, probs in r["pieces"]:
            cat = _category(iid)
            authored[cat] += 1
            if probs:
                log["dropped"].append({"stage": "lint", "task": r["label"], "iid": iid, "reason": _short(probs)})
                continue
            vl = value_lint(iid, piece)
            if vl:
                log["dropped"].append({"stage": "lint", "task": r["label"], "iid": iid, "reason": _short(vl)})
                continue
            kept.append({"task_id": tid, "label": r["label"], "iid": iid, "piece": piece, "cat": cat})
    return kept, authored


# ================================================================================================ stage 3: dedup
def dedup_stage(kept: list, log: dict):
    names = [c for c in kept if c["cat"].startswith("name_")]
    rest = [c for c in kept if not c["cat"].startswith("name_")]
    out_by_cat = defaultdict(list)
    seen = {}
    wording_occ = defaultdict(list)
    for c in rest:
        cat = c["cat"]
        if cat == "pack":
            key = ("pack", c["iid"].split(":")[1], json.dumps(c["piece"], sort_keys=True))
        else:
            key = (cat, _norm(c["piece"]))
        if cat == "wording":
            wording_occ[key[1]].append(c)
            continue
        if key in seen:
            log["dropped"].append({"stage": "dedup", "task": c["label"], "iid": c["iid"],
                                   "reason": f"duplicate of {seen[key]}"})
            continue
        seen[key] = c["iid"]
        out_by_cat[cat].append(c)
    for text, occ in sorted(wording_occ.items()):
        forms = {c["iid"].split(":")[1] for c in occ}
        if len(forms) > 1:
            for c in occ:
                log["dropped"].append({"stage": "dedup", "task": c["label"], "iid": c["iid"],
                                       "reason": f"same text under question forms {sorted(forms)}"})
            continue
        out_by_cat["wording"].append(occ[0])
        for c in occ[1:]:
            log["dropped"].append({"stage": "dedup", "task": c["label"], "iid": c["iid"],
                                   "reason": f"duplicate of {occ[0]['iid']}"})
    # names: duplicates inside a pool are silent in check_pools (dict.fromkeys), so count them here
    pools = {"first": [], "pairs": [], "last": [], "requesters": []}
    origin = {}
    for c in names:
        sub = c["iid"].split(":")[1]
        key = "requesters" if sub == "requester" else sub
        val = list(c["piece"]) if sub == "pairs" else c["piece"]
        pools[key].append(val)
        origin.setdefault(_vkey(val), c["iid"])
    for key, vals in pools.items():
        n_dup = len(vals) - len({_vkey(v) for v in vals})
        if n_dup:
            log["dropped"].append({"stage": "dedup", "task": "names", "iid": key,
                                   "reason": f"{n_dup} repeated value(s) in the {key} pool"})
    res = A.check_pools(pools["first"], pools["pairs"], pools["last"], pools["requesters"])
    for val, why in res["dropped"]:
        log["dropped"].append({"stage": "dedup", "task": "names", "iid": origin.get(_vkey(val), "?"),
                               "reason": why})
    return out_by_cat, res


# ================================================================================================ stage 4: G-LEX
def _registry(cands: list, rejects: list):
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    kept = []
    for c in cands:
        try:
            reg.add(c["text"], question_sem(FAMILY, c["qform"]), family=FAMILY, source="haiku",
                    haiku_task_id=c["task_id"], haiku_prompt_sha=c["psha"])
            kept.append(c)
        except LexiconError as e:
            rejects.append((c, f"add: {e}"))
    return reg, kept


def lexicon_stage(wordings: list, info: dict, log: dict):
    cands = [{**c, "text": c["piece"], "qform": c["iid"].split(":")[1], "psha": info[c["task_id"]]["prompt_sha"]}
             for c in wordings]
    rejects, cur = [], list(cands)
    while True:
        reg, cur = _registry(cur, rejects)
        reg.unit_test_all()
        bad = {f.text: (f.unit_problems[:1] or ["unit test"])[0] for f in reg.forms.values() if not f.unit_ok}
        if not bad:
            break
        for c in cur:
            if c["text"] in bad:
                rejects.append((c, f"unit test: {bad[c['text']][:200]}"))
        cur = [c for c in cur if c["text"] not in bad]
    for c, why in rejects:
        log["dropped"].append({"stage": "g-lex", "task": c["label"], "iid": c["iid"], "reason": why[:240]})
    return reg


# ================================================================================================ stage 5: extraction
def extraction_batches(reg) -> list:
    out = []
    for label, tseed, cseed in READS:
        items = reg.lexicon_items(sorted(reg.forms), seed=cseed)
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=tseed, prompt=PROMPT_LEX)
        out.append((label, A._finish(b, EXTRACT)))
    return out


def write_stage(batches: list, summary: dict) -> list:
    files = {}
    for _, b in batches:
        files.update(b.files())
    files["answers/.keep"] = ""
    idx = A.task_index(batches, EXTRACT)
    files["tasks.json"] = json.dumps({"family": FAMILY, "seed": EXTRACT_SEED, "tasks": idx}, indent=1) + "\n"
    files["prep_log.json"] = json.dumps(summary, ensure_ascii=False, indent=1) + "\n"
    paths.write_files(EXTRACT, files)
    return idx


def main(argv=None) -> int:
    paths.require_a38()
    recs = A.load(A.ROOT)
    info = {t["task_id"]: t for t in A.task_index(A.build(A.ROOT), A.ROOT)}
    log = {"family": FAMILY, "source": "haiku/author/answers", "dropped": []}
    kept, authored = lint_stage(recs, info, log)
    by_cat, names = dedup_stage(kept, log)
    reg = lexicon_stage(by_cat["wording"], info, log)
    batches = extraction_batches(reg)

    dropped = Counter((d["stage"], d["iid"].split(":")[0] if d["iid"] != "?" else "?") for d in log["dropped"])
    kept_wording = Counter(f.sem_id.split(".")[-1] for f in reg.forms.values())
    skin_regs = Counter(c["iid"].split(":")[1] for c in by_cat["skin"])
    held = set(T.T30Plugin.HELD_OUT_REGISTERS)
    survivors = {"skin_training": 0, "skin_held_out": 0}
    for r, n in skin_regs.items():
        survivors["skin_held_out" if r in held else "skin_training"] += n
    summary = {
        "family": FAMILY,
        "tasks": len(recs),
        "pieces_authored": dict(authored),
        "pieces_authored_total": sum(authored.values()),
        "dropped_by_stage_and_kind": {f"{s}:{k}": n for (s, k), n in sorted(dropped.items())},
        "kept_by_category": {k: len(v) for k, v in sorted(by_cat.items())},
        "kept_packs_by_type": dict(Counter(c["iid"].split(":")[1] for c in by_cat["pack"])),
        "kept_skins_by_register": dict(skin_regs),
        "kept_skin_totals": survivors,
        "kept_attack_lines": len(by_cat["attack"]),
        "kept_names": {"first": len(names["first"]), "pairs": len(names["pairs"]), "last": len(names["last"]),
                       "requesters": len(names["requesters"])},
        "lexicon_forms_needing_admission": len(reg.forms),
        "lexicon_forms_by_question_form": dict(kept_wording),
        "lexicon_precedence_or_window_forms": 0,
        "g3h_round_trip_items": 0,
        "extraction_reads": {label: {"items": sum(len(c["items"]) for c in b.chunks), "chunks": len(b.chunks)}
                             for label, b in batches},
        "dropped": log["dropped"],
    }
    idx = write_stage(batches, summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "dropped"}, indent=1, ensure_ascii=False))
    print(json.dumps({"extraction_tasks": len(idx), "task_ids": [t["task_id"] for t in idx]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
