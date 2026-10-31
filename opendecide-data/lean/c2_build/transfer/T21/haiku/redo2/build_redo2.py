"""transfer/T21/haiku/redo2/build_redo2.py: the T21 REDO-2 top-up round for blocker B1 (G0_SPEC.md v1.2 section 9).

B1: v1 authored exactly the G0 section 6 targets, so 20 lint drops (pools/quarantine.json) left 2 training packs, 8 Mode
T skins, 5 Mode F narratives and 5 question wordings short. The targets are never lowered, a v1 task is never re-read
(that would re-author its whole chunk) and pools/ is frozen once. This round authors NEW candidates (new seed, new
opaque qids, new answer paths), 3 per missing piece and 4 per missing wording, each with a rank fixed here before any
answer exists. It runs the v1 loaders and gates unchanged, then fills exactly the shortfall of each cell with its
lowest-ranked candidates that pass every gate. A new file: it imports the T21 modules and the kit read-only and edits
none of them; it never writes pools/ and never sets, edits or reads a label. Every write goes through c2_kit.paths
(A38 guard, never-open guard), only under haiku/redo2/.

Stage A  "tasks"    authoring tasks for the short cells only (packs, Mode T skins, Mode F narratives, wordings): the
                    v1 prompts (haiku_author) plus an addendum that only names more words the gates already refuse
                    (each one is checked to be a gate word) or openings the pool already holds. Mode F briefs carry 15
                    new invented claimant / agreement pairs.
Stage B  "reads"    after every stage A answer exists: the v1 loaders (haiku_author.check_pack / check_skin /
                    check_freeform / check_wording, extract_build.lint_packs: G-SL by role, word lists, shape, round
                    trip, negcount) with dedup against every v1 answer text and name; new wordings join the frozen v1
                    registry (pools/lexicon.json): a form whose add or unit test fails, or that breaks any form's unit
                    test, is dropped; then 2 independent G-LEX reads of every new form (v1 prompt, the 5 T21 meanings)
                    and 1 G3-H read of every new Mode F narrative (v1 prompt and fields).
Stage C  "results"  after every stage B answer exists: G-LEX 2/2 (an invalid or other pick rejects), G3-H exact per
                    narrative (one narrative per template, so the 98% bar means 100% here), then the selection: per
                    cell, the lowest-ranked candidates that pass every gate, exactly `need` of them (the rest stay
                    unused). Writes haiku/redo2/results/ only: the top-up pieces in the pool formats, the v1 lexicon
                    plus the chosen forms, the redo2 quarantine, the selection and a manifest with the tally after the
                    top-up. Joining results/topup/ to pools/ (an additive load or a re-freeze) is the orchestrator's
                    call; v1 pools/ stays byte-identical (checked against pools/manifest.json).

Run from lean/:
  ../.venv/bin/python c2_build/transfer/T21/haiku/redo2/build_redo2.py tasks [--write]    (default: dry run)
  ../.venv/bin/python c2_build/transfer/T21/haiku/redo2/build_redo2.py check              (disk == rebuild, stage A)
  ../.venv/bin/python c2_build/transfer/T21/haiku/redo2/build_redo2.py reads [--write]
  ../.venv/bin/python c2_build/transfer/T21/haiku/redo2/build_redo2.py results [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                  # .../transfer/T21/haiku/redo2
T21_DIR = HERE.parents[1]                               # .../transfer/T21
C2_BUILD = T21_DIR.parents[1]                           # .../lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from transfer.T21 import extract_build as EB  # noqa: E402
from transfer.T21 import haiku_author as HA  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402

FAMILY = "T21"
SEED = "t21-redo2-v1"
PL = P.T21Plugin
POOLS = T21_DIR / "pools"
V1_MANIFEST = POOLS / "manifest.json"
V1_LEXICON = POOLS / "lexicon.json"
V1_EXTRACT_TASKS = T21_DIR / "haiku" / "extract" / "TASKS.json"
RESULTS = HERE / "results"
ID0 = 100                                              # redo2 item index = ID0 + rank (v1 used 000-039)
PREFIX = "t21r2."
TRAIN_REG = HA.TRAIN_REGISTERS

# B1 shortfall (pools/manifest.json "shortfalls"; the pack shortfall is in the training packs only). Never lowered.
EXPECTED_NEED = {
    ("packs", "train"): 2,
    ("skins", "dispute_email"): 2, ("skins", "legal_memo"): 2, ("skins", "counsel_chat"): 1,
    ("skins", "board_note"): 1, ("skins", "negotiation_notes"): 1, ("skins", "contract_faq"): 1,
    ("freeform", "dispute_email"): 2, ("freeform", "legal_memo"): 1, ("freeform", "counsel_chat"): 1,
    ("freeform", "contract_faq"): 1,
    ("wordings", "yn_capped"): 2, ("wordings", "ch_clause"): 2, ("wordings", "yn_free_of"): 1,
}
FACTOR = {"packs": 3, "skins": 3, "freeform": 3, "wordings": 4}      # candidates per missing piece (lesson B1 a)
MAX_PER_TASK = {"packs": 8, "skins": 22, "freeform": 14, "wordings": 20}
GLEX_EXTRACTORS = ("haiku-glex-question-redo2-r1", "haiku-glex-question-redo2-r2")
LEX_MAX = G3H_MAX = chunker.MAX_ITEMS

# ------------------------------------------------------------------------------------------------ item content
PACK_THEMES_R2 = ("a lighthouse museum", "a weather station network", "a harbour pilot service",
                  "a sheep shearing cooperative", "a stained glass studio", "a puppet theatre")
SETTINGS_R2 = ("a canal trust and a lock engineer", "a lighthouse museum and a lamp restorer",
               "a pottery and a kiln builder", "an apiary and a jar maker", "a courier firm and a cycle workshop",
               "an orchard and a cider press", "an organ builder and a chapel trust", "a saddlery and a tannery",
               "a weaving mill and a dye works", "a harbour board and a dredging firm",
               "a weather service and a sensor maker", "a map publisher and a print shop")
# Mode F facts: invented claimant and agreement names (new; never a v1 fact or pack name; checked by fact_problems)
F_FACTS_R2 = (
    ("Ashwell Ropeworks", "Arnside mooring agreement"), ("Brackley Canal Boats", "Bowland kiln lease agreement"),
    ("Caldbeck Pottery", "Crummock rigging agreement"), ("Dunholme Apiaries", "Dalehead hive rental agreement"),
    ("Eskdale Couriers", "Elterwater courier agreement"), ("Fernhill Orchards", "Fellside orchard agreement"),
    ("Glaisdale Glassworks", "Garsdale furnace agreement"), ("Hutton Moor Lodges", "Hallin Fell lodging agreement"),
    ("Ixworth Tannery", "Ireby tanning agreement"), ("Kelsall Mapmakers", "Kentmere survey agreement"),
    ("Lindale Kilns", "Lorton Vale kiln agreement"), ("Muncaster Weavers", "Mosedale weaving agreement"),
    ("Nethercott Saddlery", "Nenthead leather agreement"), ("Oakhanger Organs", "Ousby organ tuning agreement"),
    ("Pendlebury Chandlers", "Portinscale candle agreement"))
# question openings the v1 pool does not hold (v1 haiku_author.STYLES are excluded by the addendum)
STYLES_R2 = ("open with 'According to the clauses shown,'", "open with 'Looking at the clauses together,'",
             "open with 'Working through the clauses,'", "open with 'Judging by the clauses listed,'",
             "open with 'In the light of these clauses,'", "open with 'With the clauses read as the card says,'",
             "open with 'Per the clauses shown,'", "open with 'Read in line with the card,'")

# Addenda: only words the gates already refuse (checked in addendum_problems) or openings the pool already holds.
PACK_AVOID = ("bulk", "quarter", "pair", "single", "double", "triple", "total", "whole", "entire", "extra", "partial",
              "handful", "various", "another", "open", "closed", "active", "late", "past", "block", "grant",
              "settled", "outstanding", "genuine", "compliant", "delivered", "processed", "complete", "done", "kept",
              "broken", "paid", "valid", "void", "fake", "legitimate", "eligible")
SKIN_AVOID = ("everyone", "everybody", "everything", "anyone", "anybody", "anything", "someone", "somebody",
              "something", "appear", "appears", "assume", "confirm", "confirmed", "confirmation", "accept", "accepted",
              "approval", "kept", "bunch", "handful", "bulk", "partial", "entire", "ordinary", "full", "fully",
              "processed", "delivered")
FREEFORM_AVOID = ("kept", "full", "fully", "ordinary", "confirmed", "approved", "resolved", "settled", "pending",
                  "accepted", "rejected", "completed", "valid", "paid", "broken", "entitled", "eligible", "open",
                  "closed", "active", "done", "finished", "outstanding")
V1_OPENINGS = ("Under these clauses,", "Going by the clauses above,", "On the clauses as written,",
               "Taking the clauses at face value,", "Reading the clauses as the card explains,",
               "Following the chain of switches,")

PACK_ADD = ("\n\nExtra word rules for this round (a program rejects a pack whose names use any of these words; earlier "
            "packs were turned down for words like these): " + ", ".join(PACK_AVOID) + ".")
SKIN_ADD = ("\n\nExtra word rules for this round (a program rejects a skin that uses any of these words; earlier skins "
            "were turned down for words like these): " + ", ".join(SKIN_AVOID) + ".")
FREEFORM_ADD = ("\n\nExtra word rules for this round (a program rejects a note that uses any of these words outside "
                "the two names; earlier notes were turned down for words like these): " + ", ".join(FREEFORM_AVOID)
                + ".")
WORDING_ADD = ("\n\nThis round adds a few questions to a set that already holds many. Open the question as the item's "
               "style hint says, never with " + ", ".join(f"'{o}'" for o in V1_OPENINGS) + " (the set already holds "
               "those openings), and vary the rest of the sentence too.")


def fact_problems() -> list:
    """The redo2 Mode F facts: shapes of plugin.validate_pack, valid name slots that lint clean, no banned or reserved
    word, never a v1 fact or v1 pack name, and no name inside the other name of its pair."""
    probs, seen = [], set()
    banned = P._banned_words()
    v1 = {x.lower() for x in HA.F_CLAIMANTS + HA.F_AGREEMENTS}
    v1 |= {x.lower() for pk in json.loads((POOLS / "packs.json").read_text(encoding="utf-8"))
           for x in pk["agreements"] + pk["parties"]}
    for claimant, agreement in F_FACTS_R2:
        if not P._PARTY_RE.fullmatch(claimant):
            probs.append(f"claimant shape {claimant!r}")
        if not P._AGREEMENT_RE.fullmatch(agreement):
            probs.append(f"agreement shape {agreement!r}")
        for v, words in ((claimant, re.findall(r"[a-z]+", claimant.lower())),
                         (agreement, re.findall(r"[a-z]+", agreement.lower())[:-1])):
            try:
                vio = gsl.lint_values({"X": S.name_slot(v)})
            except S.SlotError as e:
                probs.append(f"{v!r}: {e}")
                continue
            probs += [f"{v!r}: G-SL {x.rule}: {x.detail}" for x in vio]
            bad = sorted(set(words) & (banned | HA.TYPE_CAUSE_WORDS | HA.HINT_WORDS))
            if bad:
                probs.append(f"{v!r} uses {bad}")
            if "ohs" in v.lower() or "jev" in v.lower():
                probs.append(f"{v!r} holds a reserved letter sequence")
            if v.lower() in v1 or v.lower() in seen:
                probs.append(f"{v!r} repeats a v1 or redo2 name")
            seen.add(v.lower())
        if claimant.lower() in agreement.lower() or agreement.lower() in claimant.lower():
            probs.append(f"{claimant!r} / {agreement!r}: one name inside the other")
    return probs


def addendum_problems() -> list:
    """Every addendum word is already refused by the gate that lints that pool (the addendum only tightens)."""
    probs = []
    pack_gate = P._banned_words()
    skin_gate = set().union(*gsl.CORE.values(), *gsl.EXTENDED.values()) | HA.TYPE_CAUSE_WORDS | HA.HINT_WORDS
    free_gate = (gsl.CORE["status"] | gsl.EXTENDED["status"] | gsl.CORE["modal"] | HA.TYPE_CAUSE_WORDS
                 | HA.HINT_WORDS)
    for name, words, gate in (("packs", PACK_AVOID, pack_gate), ("skins", SKIN_AVOID, skin_gate),
                              ("freeform", FREEFORM_AVOID, free_gate)):
        probs += [f"{name}: addendum word {w!r} is no gate word" for w in words if w not in gate]
    return probs


# ------------------------------------------------------------------------------------------------ need
def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _sha_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def v1_pool_problems() -> list:
    """pools/ must be byte-identical to the frozen manifest (redo2 never touches it)."""
    m = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
    return [f"pools/{n} changed since the freeze" for n, info in sorted(m["pool_files"].items())
            if _sha_file(POOLS / n) != info["sha256"]]


def need_from_manifest() -> dict:
    """{(pool, cell label): shortfall} from pools/manifest.json; must equal EXPECTED_NEED (the B1 numbers)."""
    m = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
    need = {}
    for x in m["shortfalls"]:
        kind, lab, n = x["kind"], x["label"], x["shortfall"]
        if kind == "packs":
            if lab == "held_out":
                raise ValueError("a held-out pack shortfall is not planned in redo2")
            if lab == "train":
                need[("packs", "train")] = n
            continue                                   # "total" = train + held_out
        pool = {"skins_T": "skins", "freeform_F": "freeform", "wordings": "wordings"}.get(kind)
        if pool is None:
            raise ValueError(f"shortfall kind {kind!r} is not planned in redo2")
        need[(pool, lab)] = n
    if need != EXPECTED_NEED:
        raise ValueError(f"pools/manifest.json shortfalls {need} differ from the B1 plan {EXPECTED_NEED}")
    return need


def cells(need: dict) -> list:
    """[(pool, label, need)] in a fixed order: packs, skins and Mode F in register order, wordings in plan order."""
    order = [("packs", "train")] + [("skins", r) for r in TRAIN_REG] + [("freeform", r) for r in TRAIN_REG] + \
        [("wordings", q) for q in HA.WORDING_PLAN]
    return [(p, lab, need[(p, lab)]) for p, lab in order if need.get((p, lab))]


# ------------------------------------------------------------------------------------------------ batches (stage A)
def _pack_items(need: dict) -> tuple:
    items, plan = [], {}
    for r in range(need[("packs", "train")] * FACTOR["packs"]):
        iid = f"{PREFIX}pack.{ID0 + r:03d}"
        items.append((iid, {"brief": f"An invented line of business: {PACK_THEMES_R2[r]}. Invent the names of its "
                                     f"agreements and of the organisations it deals with, to fit it."}))
        plan[iid] = {"role": "pack", "held_out": False, "pack_id": f"t21-pk-{ID0 + r:03d}", "cell": "packs|train",
                     "rank": r}
    return items, plan


def _skin_items(need: dict) -> tuple:
    items, plan = [], {}
    for ri, reg in enumerate(TRAIN_REG):
        for r in range(need.get(("skins", reg), 0) * FACTOR["skins"]):
            tone = HA.TONES[(r + ri) % len(HA.TONES)]
            setting = SETTINGS_R2[(r * 5 + ri * 3) % len(SETTINGS_R2)]
            iid = f"{PREFIX}skin.{reg}.{ID0 + r:03d}"
            items.append((iid, {"brief": f"Write {HA.REGISTER_DESC[reg]}. Setting: a contract between {setting}. "
                                         f"Tone: {tone}.",
                                "register": reg, "slots": HA._slots_desc(), "rules": HA.REGISTER_RULES[reg]}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "held_out": False, "cell": f"skins|{reg}",
                         "rank": r}
    return items, plan


def _freeform_items(need: dict) -> tuple:
    items, plan, k = [], {}, 0
    for ri, reg in enumerate(TRAIN_REG):
        for r in range(need.get(("freeform", reg), 0) * FACTOR["freeform"]):
            claimant, agreement = F_FACTS_R2[k]
            tone = HA.TONES[(k + ri) % len(HA.TONES)]
            setting = SETTINGS_R2[(k * 7) % len(SETTINGS_R2)]
            k += 1
            iid = f"{PREFIX}free.{reg}.{ID0 + r:03d}"
            facts = {"CLAIMANT": claimant, "AGREEMENT": agreement}
            items.append((iid, {"brief": f"Write {HA.REGISTER_DESC[reg]} about a contract between {setting}: "
                                         f"CLAIMANT has raised a claim under AGREEMENT. Tone: {tone}.",
                                "register": reg, "facts": dict(facts), "rules": HA.FREEFORM_RULES[reg]}))
            plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": False, "facts": facts,
                         "cell": f"freeform|{reg}", "rank": r}
    return items, plan


def _wording_items(need: dict) -> tuple:
    items, plan = [], {}
    for q in HA.WORDING_PLAN:
        meaning, rule = HA.WORDING_BRIEF[q]
        lo, _hi = HA.CAP_COUNT[q]
        for r in range(need.get(("wordings", q), 0) * FACTOR["wordings"]):
            iid = f"{PREFIX}wording.{q}.{ID0 + r:03d}"
            items.append((iid, {"brief": meaning,
                                "slots": {"CAP_ID": "the cap clause's number" + (" (exactly once)" if lo else
                                                                                 " (at most once)")},
                                "rules": [rule, f"Style hint: {STYLES_R2[r % len(STYLES_R2)]}."]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": False, "cell": f"wordings|{q}", "rank": r}
    return items, plan


BATCH_SPECS = (
    # name, chunker kind, items fn, prompt, forbid
    ("packs", "author_pack", _pack_items, HA.PACK_PROMPT + PACK_ADD, HA.FORBID_ALL),
    ("skins", "author_skin", _skin_items, HA.SKIN_PROMPT + SKIN_ADD, HA.FORBID_ALL),
    ("freeform", "author_freeform", _freeform_items, HA.FREEFORM_PROMPT + FREEFORM_ADD, HA.FORBID_ALL),
    ("wordings", "author_wording", _wording_items, HA.WORDING_PROMPT + WORDING_ADD, HA.FORBID_WORDING),
)


def build_batches() -> dict:
    """{name: (TaskBatch, plan)} for the short cells; chunks balanced under the v1 per-task caps."""
    need = need_from_manifest()
    out = {}
    for name, kind, fn, prompt, forbid in BATCH_SPECS:
        items, plan = fn(need)
        n = len(items)
        k = max(1, math.ceil(n / MAX_PER_TASK[name]))
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt,
                               max_items=math.ceil(n / k), forbid_strings=forbid)
        out[name] = (b, plan)
    return out


def _guard(files: dict, rows: list) -> None:
    for f in list(files) + [r["answer_file"] for r in rows]:
        if paths.never_open(HERE / f):
            raise paths.NeverOpen(f"task path on the never-open list: {f}")


def stage_a() -> tuple:
    """({relative path: text}, [task rows]) for the authoring round; nothing is written here."""
    probs = v1_pool_problems() + fact_problems() + addendum_problems()
    if probs:
        raise ValueError("; ".join(probs))
    need = need_from_manifest()
    files, rows = {}, []
    batches = build_batches()
    for name, (b, plan) in batches.items():
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(HERE / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            text = HA.task_file_text(b, c, ans)
            files[tfile] = text
            rows.append({"stage": "A", "blocker": "B1", "task": name, "task_id": tid, "kind": b.kind, "pool": name,
                         "batch_id": b.batch_id, "task_file": str(HERE / tfile), "answer_file": ans,
                         "n_items": len(c["items"]), "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                         "task_sha256": _sha_text(text), "allowed_read": [str(HERE / tfile)],
                         "allowed_write": [ans]})
    cell_rows = {}
    for pool, lab, n in cells(need):
        plan = batches[pool][1]
        cand = sorted((i for i in plan if plan[i]["cell"] == f"{pool}|{lab}"), key=lambda i: plan[i]["rank"])
        cell_rows[f"{pool}|{lab}"] = {"need": n, "candidates_by_rank": cand}
    files["plan/topup_rule.json"] = json.dumps({
        "rule": "G0_SPEC.md v1.2 section 9: per cell, the lowest-ranked candidates that pass every gate (v1 loaders "
                "and lints, dedup vs every v1 text and name, G-LEX 2/2 in the v1 registry, G3-H exact) fill exactly "
                "`need`; the rest stay unused; a cell still short stays short (no target lowered, no v1 re-read)",
        "factor": FACTOR, "need_total": sum(need.values()), "cells": cell_rows}, indent=1, sort_keys=True) + "\n"
    files["answers/README.txt"] = ("Haiku answer files of the T21 redo2 round: one <task_id>.json per task (see "
                                   "../TASKS.json and, after stage B, ../TASKS_B.json). Written only by the task "
                                   "agents.\n")
    files["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": SEED, "stage": "A", "blocker": "B1", "g0_sha256": PL.G0_SHA256,
        "g0_ambiguity_pass": PL.G0_HAIKU_TASK, "n_tasks": len(rows),
        "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "batches": {name: b.batch_id for name, (b, _p) in batches.items()},
        "need": {f"{p}|{lab}": n for (p, lab), n in sorted(need.items())},
        "notes": ["NEW items, new seed, new opaque qids, new answer paths under haiku/redo2/answers/; no v1 task, "
                  "answer, key, pool or pinned file changes.",
                  "One fresh Haiku agent per task_file: it reads only that file and writes only its answer_file "
                  "(audit with allowed_read / allowed_write). key/ and plan/ are orchestrator-only.",
                  "Next: after every answer exists run `build_redo2.py reads --write` (stage B: v1 lint + dedup, "
                  "2 G-LEX reads per new wording, 1 G3-H read per new Mode F narrative); after every stage B answer "
                  "exists run `build_redo2.py results --write` (stage C: selection into haiku/redo2/results/).",
                  "Joining results/topup/ to pools/ is the orchestrator's call; pools/ is never written here.",
                  "Labels: none. Haiku answers only flag; every gold still comes from solver A = solver B."],
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    _guard(files, rows)
    return files, rows


# ------------------------------------------------------------------------------------------------ stage B (reads)
def _load_raw(b) -> tuple:
    """({task_id: answer object}, problems) from haiku/redo2/answers/ (tests replace this function)."""
    raw, probs = {}, []
    for c in b.chunks:
        f = HERE / b.answer_path(c["task_id"])
        if not f.is_file():
            probs.append(f"{c['task_id']}: no answer file")
            continue
        try:
            raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{c['task_id']}: answer is not JSON ({e})")
    return raw, probs


def v1_seen() -> tuple:
    """(names, narrative texts, wording texts) of every v1 answer (kept or dropped), the fixtures and the redo2
    facts: a redo2 piece may repeat none of them."""
    names = {x.lower() for x in list(P.DEFAULT_PACK["agreements"]) + list(P.DEFAULT_PACK["parties"])}
    names |= {x.lower() for x in HA.F_CLAIMANTS + HA.F_AGREEMENTS}
    names |= {x.lower() for pair in F_FACTS_R2 for x in pair}
    _b, _p, ans, _q = HA.load_answers_for("packs")
    for a in ans.values():
        pk = a.get("pack") if isinstance(a, dict) else None
        for key in ("agreements", "parties"):
            for v in (pk.get(key) or []) if isinstance(pk, dict) else []:
                if isinstance(v, str):
                    names.add(v.lower())
    texts = set()
    for name in ("skins", "freeform", "attacks"):
        _b, _p, ans, _q = HA.load_answers_for(name)
        texts |= {HA._norm(a["text"].strip()) for a in ans.values()
                  if isinstance(a, dict) and isinstance(a.get("text"), str) and a["text"].strip()}
    _b, _p, ans, _q = HA.load_answers_for("wordings")
    wtexts = {" ".join(a["text"].split()).lower() for a in ans.values()
              if isinstance(a, dict) and isinstance(a.get("text"), str)}
    wtexts |= {q.lower() for q in HA.QSTRINGS}
    return names, texts, wtexts


def lint_stage(batches: dict) -> dict:
    """The v1 loaders on every redo2 answer, in (cell, rank) order so a lower rank wins a repeat. One text set spans
    skins and Mode F (cross-pool dedup with each other and with every v1 skin, narrative and attack line)."""
    names, texts, wtexts = v1_seen()
    kept = {"packs": {}, "skins": {}, "freeform": {}, "wordings": {}}
    drops = {k: {} for k in kept}
    problems = []
    for name in ("packs", "skins", "freeform", "wordings"):
        b, plan = batches[name]
        raw, p1 = _load_raw(b)
        ans, p2 = chunker.load_answers(b, raw)
        problems += [f"{name}: {x}" for x in p1 + p2]
        task_of = {iid: b.task_of[qid] for qid, iid in b.key.items()}
        for iid in sorted(plan, key=lambda i: (plan[i]["cell"], plan[i]["rank"])):
            a = ans.get(iid)
            if a is None:
                drops[name][iid] = ["no answer"]
                continue
            if name == "packs":
                obj, v = HA.check_pack(iid, a, plan[iid], names)
                if not v:
                    _k, d = EB.lint_packs([obj])
                    v = d[0]["reasons"] if d else []
            else:
                text = a.get("text") if isinstance(a, dict) else None
                check = {"skins": HA.check_skin, "freeform": HA.check_freeform, "wordings": HA.check_wording}[name]
                obj, v = check(iid, text, plan[iid], task_of[iid], b.prompt_sha,
                               wtexts if name == "wordings" else texts)
            if v:
                drops[name][iid] = list(v)
            else:
                kept[name][iid] = obj
    return {"kept": kept, "drops": drops, "problems": problems}


def v1_registry() -> LexiconRegistry:
    """The frozen v1 registry (pools/lexicon.json, read-only): forms, v1 extractions, unit tests rerun."""
    return LexiconRegistry.from_json(json.loads(V1_LEXICON.read_text(encoding="utf-8")))


def registry_with(accepted: list) -> tuple:
    """(v1 registry + the accepted new forms, {form id: iid}, unit test results). accepted: [(iid, (q, text, tid,
    psha))]."""
    reg = v1_registry()
    fid_of = {}
    for iid, (q, text, tid, psha) in accepted:
        f = reg.add(text, question_sem(FAMILY, q), slots=EB._slots_for(text), family=FAMILY, source="haiku",
                    haiku_task_id=tid, haiku_prompt_sha=psha)
        fid_of[f.form_id] = iid
    return reg, fid_of, reg.unit_test_all()


def admit_stage(wordings: dict, plan: dict) -> tuple:
    """(registry, {new form id: iid}, drops {iid: reasons}). New forms join the v1 registry in (cell, rank) order; one
    whose add fails, or whose unit test fails, or that breaks any form's unit test, is dropped."""
    v1 = v1_registry()
    bad_v1 = [f for f in v1.forms if v1.status(f) != "admitted"]
    if bad_v1:
        raise ValueError(f"v1 registry forms not admitted: {bad_v1[:3]}")
    accepted, drops = [], {}
    for iid in sorted(wordings, key=lambda i: (plan[i]["cell"], plan[i]["rank"])):
        try:
            _r, _f, res = registry_with(accepted + [(iid, wordings[iid])])
        except LexiconError as e:
            drops[iid] = [f"G-LEX add: {e}"]
            continue
        bad = [fid for fid, ok in res.items() if not ok]
        if bad:
            drops[iid] = [f"G-LEX unit: {fid}" for fid in bad[:3]]
            continue
        accepted.append((iid, wordings[iid]))
    reg, fid_of, _res = registry_with(accepted)
    return reg, fid_of, drops


def _v1_extract_prompt_shas() -> dict:
    tj = json.loads(V1_EXTRACT_TASKS.read_text(encoding="utf-8"))
    out: dict = {}
    for t in tj["tasks"]:
        out.setdefault(t["kind"], set()).add(t["prompt_sha"])
    return out


def glex_batches(reg: LexiconRegistry, fids: list) -> list:
    """Two independent reads of every new form (v1 G-LEX prompt; the 5 T21 meanings in a seeded order per read)."""
    if chunker.sha(EB.PROMPT_LEX) not in _v1_extract_prompt_shas().get("extract_lex", set()):
        raise ValueError("extract_build.PROMPT_LEX no longer equals the v1 G-LEX prompt")
    out = []
    if not fids:
        return out
    for r, ext in enumerate(GLEX_EXTRACTORS, 1):
        seed = f"{SEED}|glex-question-r{r}"
        items = reg.lexicon_items(sorted(fids), seed=seed)
        k = max(1, math.ceil(len(items) / LEX_MAX))
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=EB.PROMPT_LEX,
                               max_items=math.ceil(len(items) / k))
        out.append((ext, b))
    return out


def g3h_stage(free: dict, plan: dict) -> tuple:
    """(batch or None, {item id: expected}): one read of every kept new Mode F narrative (v1 G3-H prompt and fields).
    The expected values are the brief's facts and stay in key/."""
    if chunker.sha(EB.PROMPT_G3H) not in _v1_extract_prompt_shas().get("extract_g3h", set()):
        raise ValueError("extract_build.PROMPT_G3H no longer equals the v1 G3-H prompt")
    fields = EB.g3h_fields()
    items, expected = [], {}
    for iid in sorted(free, key=lambda i: (plan[i]["cell"], plan[i]["rank"])):
        sk = free[iid]
        facts = plan[iid]["facts"]
        exp = {"claimant": facts["CLAIMANT"], "agreement": facts["AGREEMENT"]}
        ok, diffs = g3h.compare(exp, dict(exp), fields)
        if not ok:
            raise RuntimeError(f"G3-H self-check failed for {sk.skin_id}: {diffs}")
        key = f"g3h|{sk.skin_id}"
        items.append((key, g3h.extraction_item(sk.text, fields)))
        expected[key] = exp
    if not items:
        return None, expected
    k = max(1, math.ceil(len(items) / G3H_MAX))
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{SEED}|g3h", prompt=EB.PROMPT_G3H,
                           max_items=math.ceil(len(items) / k))
    return b, expected


def stage_b() -> dict:
    """Stage B, rebuilt deterministically from the stage A answers. Returns every piece the later stages need plus
    the files to write; nothing is written here."""
    batches = build_batches()
    lint = lint_stage(batches)
    if lint["problems"]:
        raise FileNotFoundError("stage A answers incomplete or malformed: " + "; ".join(lint["problems"][:6]))
    wplan = batches["wordings"][1]
    reg, fid_of, admit_drops = admit_stage(lint["kept"]["wordings"], wplan)
    glex = glex_batches(reg, sorted(fid_of))
    fplan = batches["freeform"][1]
    g3, g3_expected = g3h_stage(lint["kept"]["freeform"], fplan)
    files, rows = {}, []
    exts = [(f"glex-question-redo2-r{r}", "extract_lex", b, ext) for r, (ext, b) in enumerate(glex, 1)]
    if g3 is not None:
        exts.append(("g3h-freeform-redo2", "extract_g3h", g3, "haiku-g3h-freeform-redo2"))
    for label, kind, b, ext in exts:
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "label": label, "kind": kind,
                                                       "extractor_id": ext}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(HERE / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            files[tfile] = EB.task_markdown(kind, b, c, Path(ans))
            rows.append({"stage": "B", "blocker": "B1", "task": label, "task_id": tid, "kind": kind,
                         "pool": "glex" if kind == "extract_lex" else "g3h", "read": ext, "batch_id": b.batch_id,
                         "task_file": str(HERE / tfile), "answer_file": ans, "n_items": len(c["items"]),
                         "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                         "task_sha256": _sha_text(files[tfile]), "allowed_read": [str(HERE / tfile)],
                         "allowed_write": [ans]})
    files["key/g3h_expected_redo2.json"] = json.dumps(g3_expected, indent=1, sort_keys=True) + "\n"
    files["plan/redo2_lint.json"] = json.dumps({
        "drops": lint["drops"], "admit_drops": admit_drops,
        "kept": {name: sorted(v) for name, v in lint["kept"].items()},
        "new_forms": {fid: {"iid": iid, "text": reg.forms[fid].text, "sem_id": reg.forms[fid].sem_id}
                      for fid, iid in sorted(fid_of.items())}}, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["TASKS_B.json"] = json.dumps({
        "family": FAMILY, "version": SEED, "stage": "B", "blocker": "B1", "g0_sha256": PL.G0_SHA256,
        "n_tasks": len(rows), "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "batches": {label: b.batch_id for label, _k, b, _e in exts},
        "counts": {"new_forms_for_glex": len(fid_of), "new_narratives_for_g3h": len(g3_expected),
                   "lint_drops": {k: len(v) for k, v in lint["drops"].items()}, "admit_drops": len(admit_drops)},
        "notes": ["Two independent G-LEX reads of every new wording (v1 prompt, the 5 T21 meanings): never give both "
                  "reads' tasks to one agent. One G3-H read of every new Mode F narrative (v1 prompt and fields).",
                  "One fresh Haiku agent per task_file; audit with allowed_read / allowed_write.",
                  "Next: after every answer exists run `build_redo2.py results --write` (stage C)."],
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    _guard(files, rows)
    return {"batches": batches, "lint": lint, "reg": reg, "fid_of": fid_of, "admit_drops": admit_drops,
            "glex": glex, "g3": g3, "g3_expected": g3_expected, "files": files, "rows": rows}


# ------------------------------------------------------------------------------------------------ stage C (results)
def record_glex(reg: LexiconRegistry, glex: list, fids: list, problems: list) -> dict:
    """Record both reads, as v1 freeze_pools.record_lex does: an answer must be exactly {"meaning"}; a meaning outside
    the 5 rejects (sem None); a missing answer records nothing (the form stays pending)."""
    reads = {}
    for ext, b in glex:
        raw, p1 = _load_raw(b)
        ans, p2 = chunker.load_answers(b, raw)
        problems += [f"{ext}: {x}" for x in p1 + p2]
        for fid in fids:
            a = ans.get(fid)
            meaning = a.get("meaning") if isinstance(a, dict) and set(a) == {"meaning"} else None
            if not isinstance(meaning, str):
                reads.setdefault(fid, []).append([ext, None, "no valid answer"])
                continue
            sem = reg.meaning_to_sem("question", meaning)
            reg.record_extraction(fid, ext, sem)
            reads.setdefault(fid, []).append([ext, sem, meaning])
    return reads


def check_g3h(g3, expected: dict, problems: list) -> dict:
    """{item id: {"ok", "diffs"}}: exact compare (g3h.compare, the v1 fields); no answer = a mismatch."""
    if g3 is None:
        return {}
    raw, p1 = _load_raw(g3)
    ans, p2 = chunker.load_answers(g3, raw)
    problems += [f"g3h: {x}" for x in p1 + p2]
    fields = EB.g3h_fields()
    out = {}
    for key in sorted(expected):
        a = ans.get(key)
        ok, diffs = (g3h.compare(expected[key], a, fields) if isinstance(a, dict) else (False, ["no extraction"]))
        out[key] = {"ok": ok, "diffs": diffs}
    return out


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def stage_c(*, verify_disk: bool = True) -> dict:
    """Stage C: the gates, the selection and the result files ({relative path: text}); nothing is written here."""
    problems = v1_pool_problems()
    res = stage_b()
    if verify_disk:
        problems += [f"stage B file differs from disk or is missing: {rel}" for rel, text in sorted(res["files"].items())
                     if not (HERE / rel).is_file() or (HERE / rel).read_text(encoding="utf-8") != text]
    need = need_from_manifest()
    batches, lint, reg, fid_of = res["batches"], res["lint"], res["reg"], res["fid_of"]
    iid_fid = {iid: fid for fid, iid in fid_of.items()}
    reads = record_glex(reg, res["glex"], sorted(fid_of), problems)
    g3 = check_g3h(res["g3"], res["g3_expected"], problems)

    def status(pool: str, iid: str) -> str:
        if iid in lint["drops"][pool]:
            return "lint: " + "; ".join(lint["drops"][pool][iid][:3])
        if pool == "wordings":
            if iid in res["admit_drops"]:
                return "G-LEX registry: " + "; ".join(res["admit_drops"][iid])
            st = reg.status(iid_fid[iid])
            return "pass" if st == "admitted" else f"G-LEX {st}"
        if pool == "freeform":
            d = g3.get(f"g3h|{lint['kept']['freeform'][iid].skin_id}")
            return "pass" if d and d["ok"] else "G3-H: " + "; ".join((d or {"diffs": ["no read"]})["diffs"][:3])
        return "pass"

    selection, chosen = {}, {"packs": [], "skins": [], "freeform": [], "wordings": []}
    for pool, lab, n in cells(need):
        plan = batches[pool][1]
        cand = sorted((i for i in plan if plan[i]["cell"] == f"{pool}|{lab}"), key=lambda i: plan[i]["rank"])
        st = {i: status(pool, i) for i in cand}
        pick = [i for i in cand if st[i] == "pass"][:n]
        chosen[pool] += pick
        selection[f"{pool}|{lab}"] = {"need": n, "chosen": pick, "short_after": n - len(pick),
                                      "candidates": [{"iid": i, "rank": plan[i]["rank"], "status": st[i],
                                                      "used": i in pick} for i in cand]}

    kept = lint["kept"]
    packs = sorted((kept["packs"][i] for i in chosen["packs"]), key=lambda p: p["pack_id"])
    skins = sorted((kept["skins"][i] for i in chosen["skins"]), key=lambda s: s.skin_id)
    free = sorted((kept["freeform"][i] for i in chosen["freeform"]), key=lambda s: s.skin_id)
    acc = [(i, kept["wordings"][i]) for i in sorted(chosen["wordings"], key=lambda i: (
        batches["wordings"][1][i]["cell"], batches["wordings"][1][i]["rank"]))]
    final, final_of, unit = registry_with(acc)
    for fid in final_of:
        for ext, sem in reg.forms[fid].extractions:
            final.record_extraction(fid, ext, sem)
    gate = final.gate()
    if not gate["pass"] or not all(unit.values()):
        problems.append(f"merged lexicon fails G-LEX: {gate['not_admitted']}")
    wordings = [{"form_id": fid, "qform": batches["wordings"][1][iid]["qform"], "text": final.forms[fid].text,
                 "sem_id": final.forms[fid].sem_id, "haiku_task_id": final.forms[fid].haiku_task_id,
                 "haiku_prompt_sha": final.forms[fid].haiku_prompt_sha,
                 "extractions": [list(e) for e in final.forms[fid].extractions]}
                for fid, iid in sorted(final_of.items())]

    quarantine = []
    for pool in ("packs", "skins", "freeform", "wordings"):
        for iid, why in sorted(lint["drops"][pool].items()):
            quarantine.append({"stage": "lint", "pool": pool, "id": iid, "reasons": why})
    for iid, why in sorted(res["admit_drops"].items()):
        quarantine.append({"stage": "G-LEX registry", "pool": "wordings", "id": iid, "reasons": why})
    for fid, iid in sorted(fid_of.items()):
        if reg.status(fid) != "admitted":
            quarantine.append({"stage": "G-LEX", "pool": "wordings", "id": iid, "form_id": fid,
                               "status": reg.status(fid), "reads": reads.get(fid, [])})
    for key, d in sorted(g3.items()):
        if not d["ok"]:
            quarantine.append({"stage": "G3-H", "pool": "freeform", "id": key.split("|", 1)[1], "reasons": d["diffs"]})

    v1m = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
    added = Counter()
    for pool, lab, _n in cells(need):
        added[(pool, lab)] = len(selection[f"{pool}|{lab}"]["chosen"])
    kind_of = {"packs": "packs", "skins_T": "skins", "freeform_F": "freeform", "wordings": "wordings"}
    tally = []
    for line in v1m["tally"]:
        pool = kind_of.get(line["kind"], line["kind"])
        add = added.get((pool, "train"), 0) if (pool == "packs" and line["label"] in ("total", "train")) else \
            added.get((pool, line["label"]), 0)
        got = line["admitted"] + add
        tally.append({**line, "admitted_v1": line["admitted"], "added_redo2": add, "admitted": got,
                      "shortfall": max(0, line["target"] - got), "surplus": max(0, got - line["target"])})

    out = {
        "results/topup/packs.json": _dump(packs),
        "results/topup/skins.json": _dump([asdict(s) for s in skins]),
        "results/topup/freeform.json": _dump([asdict(s) for s in free]),
        "results/topup/wordings.json": _dump(wordings),
        "results/topup/lexicon_v1_plus_topup.json": _dump(final.to_json()),
        "results/topup/quarantine_redo2.json": _dump(quarantine),
        "results/selection.json": _dump({"rule": "G0_SPEC.md v1.2 section 9", "cells": selection}),
        "results/g3h_redo2.json": _dump(g3),
        "results/glex_redo2.json": _dump({"reads": reads, "status": {fid: reg.status(fid) for fid in sorted(fid_of)},
                                          "iid": dict(sorted(fid_of.items()))}),
    }
    manifest = {
        "family": FAMILY, "stage": "redo2 top-up results (B1; G0 v1.2 section 9)", "transfer_dev_only": True,
        "trained": False, "rows_generated": False, "g0_sha256": PL.G0_SHA256,
        "v1_pools_unchanged": not v1_pool_problems(), "v1_manifest_sha256": _sha_file(V1_MANIFEST),
        "merged": False,
        "merge_note": "results/topup/ is not in pools/: joining it (an additive load next to pools/, or a re-freeze) "
                      "is the orchestrator's call. lexicon_v1_plus_topup.json is the whole v1 registry plus the "
                      "chosen forms (replaces pools/lexicon.json on a join).",
        "tally_after_topup": tally, "shortfalls_after_topup": [x for x in tally if x["shortfall"]],
        "counts": {"chosen": {k: len(v) for k, v in chosen.items()},
                   "candidates": {k: len(v[1]) for k, v in batches.items()},
                   "lint_drops": {k: len(v) for k, v in lint["drops"].items()},
                   "admit_drops": len(res["admit_drops"]),
                   "glex_status": dict(Counter(reg.status(f) for f in fid_of)),
                   "g3h": {"items": len(g3), "ok": sum(d["ok"] for d in g3.values())}},
        "tasks_json_sha256": _sha_file(HERE / "TASKS.json") if (HERE / "TASKS.json").is_file() else None,
        "tasks_b_json_sha256": _sha_file(HERE / "TASKS_B.json") if (HERE / "TASKS_B.json").is_file() else None,
        "files": {rel: {"sha256": _sha_text(t), "bytes": len(t.encode("utf-8"))} for rel, t in sorted(out.items())},
        "problems": problems,
    }
    out["results/manifest.json"] = _dump(manifest)
    return {"files": out, "manifest": manifest, "problems": problems}


# ------------------------------------------------------------------------------------------------ CLI
def _diffs(files: dict) -> list:
    return [rel for rel, text in sorted(files.items())
            if not (HERE / rel).is_file() or (HERE / rel).read_text(encoding="utf-8") != text]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("tasks", "check", "reads", "results"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in ("tasks", "check"):
        files, rows = stage_a()
        if a.cmd == "check":
            d = _diffs(files)
            print(json.dumps({"files": len(files), "diffs": d}, indent=1))
            return 1 if d else 0
        if a.write:
            if (HERE / "TASKS.json").exists() and _diffs(files):
                raise SystemExit("stage A files on disk differ from the rebuild: refusing to overwrite stage A")
            paths.write_files(HERE, files)
        print(json.dumps({"written": a.write, "n_tasks": len(rows),
                          "outputs_expected": sum(r["outputs_expected"] for r in rows),
                          "by_kind": dict(Counter(r["kind"] for r in rows)),
                          "tasks": [{k: r[k] for k in ("task_file", "answer_file", "kind", "n_items")} for r in rows]},
                         indent=1))
        return 0
    if a.cmd == "reads":
        res = stage_b()
        if a.write:
            if (HERE / "TASKS_B.json").exists() and _diffs(res["files"]):
                raise SystemExit("stage B files on disk differ from the rebuild: refusing to overwrite stage B")
            paths.write_files(HERE, res["files"])
        print(json.dumps({"written": a.write, "n_tasks": len(res["rows"]),
                          "lint_drops": {k: v for k, v in res["lint"]["drops"].items() if v},
                          "admit_drops": res["admit_drops"],
                          "tasks": [{k: r[k] for k in ("task_file", "answer_file", "kind", "read", "n_items")}
                                    for r in res["rows"]]}, indent=1, ensure_ascii=False))
        return 0
    out = stage_c()
    if a.write:
        if out["problems"]:
            print(json.dumps({"refused": "problems; nothing written", "problems": out["problems"]}, indent=1))
            return 1
        if (RESULTS / "manifest.json").exists() and _diffs(out["files"]):
            raise SystemExit("results/ on disk differ from the rebuild: results are written once")
        paths.write_files(HERE, out["files"])
    m = out["manifest"]
    print(json.dumps({"written": a.write and not out["problems"], "counts": m["counts"],
                      "shortfalls_after_topup": m["shortfalls_after_topup"], "problems": m["problems"]}, indent=1))
    return 1 if out["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
