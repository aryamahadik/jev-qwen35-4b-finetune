#!/usr/bin/env python3
"""families/T07/haiku/redo2/build_redo2.py: T07 REDO-2, the Haiku tasks for the five design-level blockers of the 13 Oct
T07 pool freeze (pools/MANIFEST.json "shortfalls"; G0_SPEC.md section 7, R1-R5). A NEW file.

New items, new opaque ids, new answer paths. No v1 task, answer, key, plan or pool is reused or changed, and no
existing code file is changed (authoring.py, extract_build.py, freeze_pools.py, the kit, pinned lean/*.py, c_build):
the v1 freeze (freeze_pools.py) still regenerates byte for byte. No gate bar, G0 target, lint check or gold semantics
changes: every redo2 piece passes the v1 closed checks (authoring.lint_*, G-SL included) with the kept packs' words,
G-LEX 2/2 and G3-H >= 98% per register. Haiku answers only flag: nothing here sets or reads a label or a gold. Every
write goes through c2_kit.paths (A38 guard and never-open guard).

Blockers and their fix (G0 section 7):
  R1 status.out. v1 G-LEX items filled every category-kind {X} with the kit sample "production" (lexicon_items ->
     _samples()[0]); "Excludes production items." reads as category.out, so both canonical status sentences and 4 Haiku
     forms were rejected (for good, H32). Fix: the v1 rejections stand (no re-read, no re-vote). A NEW canonical pair
     CANON_STATUS_R2 (each sentence carries the word "status"); Mode F briefs with a status condition embed it; new
     status.out paraphrases; and redo2 G-LEX items fill {X} with a value of the form's own dimension (read_values;
     never a kit file edit).
  R2 yn_misses. "go short of" / "be shut out of" read as yn_fails_to (11 of 11 rejected); "lose out on" / "forfeit"
     15 of 15 admitted. Fix: a yn_misses brief that allows only those two verbs (G0 S19's antonym predicate); the
     meaning list (authoring.Q_SEM_MEANING) is unchanged.
  R3 pack words. freeze added the 49 kept packs' 587 region / category / level words to SURFACE_WORDS after the prompts
     were written. Fix: every redo2 prompt lists them (skins, Mode F bodies, attack lines, wordings, condition
     sentences). Asks are per v1 deficit (never lowered): Mode T per register, every non-admitted Mode F brief (two
     candidate texts each; the admit stage keeps one per brief, the first that passes every gate), attack lines,
     wordings.
  R4 label words. lint_* ban P.LABEL_WORDS but FORBID keeps them out of every prompt. Fix: closed frames instead (who a
     membership line is for; how an excluded status is said; how a note states its claim; how a card thanks). New
     tier.max and status.out sentences, 12 each (G0: 12 written per sem).
  R5 "shipping" (promise word) and "price" (status-value word) are refused by lint_form; the redo2 condition prompt
     says so (region: delivery, deliver(ed), ship, shipped; status: status, priced as, pricing).

Stages (each later stage rebuilds the earlier ones in memory and stops if a file on disk differs):
  author   (now) tasks/<task_id>.md (self-contained: answer path, inline answer contract, prompt, items), chunks/,
           prompts/, key/ and plan/ (orchestrator only), manifest/, TASKS.json. answers/ is written only by agents.
  extract  (after every author answer exists) lint with the v1 checks + pack words, dedup against every v1 text, add
           the canonical pair and the new forms / wordings to the v1 registry (pools/lexicon.json, v1 extractions
           kept; a v1 status that changes stops the run) and unit test; G-LEX reads redo2-r1 / redo2-r2 (2/2, the v1
           meaning lists) and the G3-H read redo2-g3h of the new Mode F texts, under extract/.
  admit    (after every extraction answer exists) record the reads, admit by lexicon.status, G3-H compare + 98% per
           register, one text per Mode F brief; write the SUPPLEMENT pools/redo2/ (pieces, records, quarantine) and its
           MANIFEST.json with merged v1 + redo2 counts against the G0 targets (never lowered). pools/*.json untouched.

Run from lean/c2_build (each stage prints its counts; --write writes):
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python families/T07/haiku/redo2/build_redo2.py author  [--write]
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python families/T07/haiku/redo2/build_redo2.py extract [--write]
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python families/T07/haiku/redo2/build_redo2.py admit   [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent                   # families/T07/haiku/redo2
T07 = HERE.parents[1]
C2_BUILD = T07.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import functools  # noqa: E402

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import freeze_pools as FZ  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07.haiku import extract_build as EB  # noqa: E402

FAMILY = "T07"
VERSION = "r2"
SEED = "t07-redo2-v1"
ROOT = HERE
EX_ROOT = HERE / "extract"
POOLS = T07 / "pools"
SUPP = POOLS / "redo2"
V1_AUTHOR = T07 / "haiku" / "author"
READS = ("redo2-r1", "redo2-r2")                         # G-LEX 2/2: two fresh agents, separate chunks
G3H_READ = "redo2-g3h"
FREE_CANDIDATES = 2                                       # Mode F texts per non-admitted brief (one is kept)
FREE_CHUNK = 38
SKIN_CHUNK = 10
SKIN_PER_ITEM = 4
ATTACK_PER_ITEM = 5
WORD_PER_ITEM = 4
FORM_PER_ITEM = 6
FORMS_WRITTEN = 12                                        # G0 section 4: 12 written per sem

# R1: the new canonical status.out pair (program side, lexicon source "claude"); every other sem keeps its v1 pair
CANON_STATUS_R2 = ("Excludes items with {X} status.", "Items whose status is {X} are excluded.")
STATUS = "t07.status.out"


def _ask(deficit: int, *, factor: float = 1.5, plus: int = 4) -> int:
    """Pieces asked for a deficit: margin over the v1 lint and G-LEX yields (never below deficit + plus)."""
    return 0 if deficit <= 0 else max(math.ceil(factor * deficit), deficit + plus)


# ------------------------------------------------------------------------------------------------ frozen v1 inputs
def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


@functools.lru_cache(maxsize=None)
def v1_manifest() -> dict:
    return _json(POOLS / "MANIFEST.json")


def kept_packs() -> list:
    return _json(POOLS / "packs.json")["packs"]


PACK_WORDS = A.pack_words(kept_packs())                  # R3: the 587 words freeze adds to SURFACE_WORDS


@functools.lru_cache(maxsize=None)
def v1_plan() -> dict:
    return _json(V1_AUTHOR / A.PLAN_FILE)["pieces"]


@functools.lru_cache(maxsize=None)
def v1_admitted_briefs() -> frozenset:
    return frozenset(d["internal_id"] for d in _json(POOLS / "documents.json")["items"])


# ------------------------------------------------------------------------------------------------ prompts
def _list(words) -> str:
    return A._t07_list(words)


BODY_BANS = A.T07_BANS | A.SURFACE_WORDS | PACK_WORDS
PACK_NOTE = ("The list also holds ordinary words (colours, rooms, materials, places, goods, ranks and so on) because "
             "each is a membership level, a delivery region or a product category in some shop's advertisements; "
             "avoid every one of them, also in another form (plural, past tense)")
THANKS = ('To thank or welcome the reader, use only plain words such as "thank you", "thanks", "welcome", '
          '"we are glad" and "we appreciate".')
CHECK = "Before you write the answer, check every word of every text against the word lists above and replace any word that is listed."

REGISTER_LINES = "\n".join(
    f"- {reg}: {A.REGISTER_FORMAT[reg][0]}. Example: {json.dumps(A.REGISTER_FORMAT[reg][1], ensure_ascii=False)}"
    for reg in A.TRAIN_REGISTERS + A.HELD_REGISTERS) + (
    f"\n- app_banner, JSON form (where the item says so): {A.APP_JSON[0]}. Example: "
    f"{json.dumps(A.APP_JSON[1], ensure_ascii=False)}")

SKIN_PROMPT = A.COMMON + f"""
TASK: write AD COPY TEMPLATES. Each item names a register (the kind of text), its format, a tone and how many texts to
write. This is the general, friendly part of a shop's advertisement. Elsewhere on the page a program prints the shop's
headline offers, their small print and the customer's order, so your text adds no fact, no offer and no condition of
its own: it welcomes the reader, talks about the shop and its range in general terms, and names the shop once.

Placeholder: use {{STORE}} (the shop's name) EXACTLY ONCE, spelled exactly so with its curly braces; no other
placeholder, and never a shop name of your own. Never put "a", "an" or "the" directly before {{STORE}}.

Hard rules (a program checks every text; a text that breaks one is thrown away):
1. One block of text, never an empty line; single line breaks only where the register needs them. Length: 8-60 words
   (shelf_tag: 2-15 words).
2. Outside the placeholder: no digits, number words or ordinals, no dates, times, months, weekdays or time words, no
   currency or percent signs, no web or e-mail addresses.
3. Outside the placeholder, none of these words (any letter case):
{A._gsl_lists()}
4. Words you must never use outside the placeholder (any letter case), because they would state an offer or a
   condition, or name what the small print talks about. {PACK_NOTE}:
{_list(BODY_BANS)}
5. No negation at all: {A.NEGATION_CUES}.
6. Capital letters only at the start of a sentence, a line or a label such as "Subject:"; no names of people, places,
   brands, products or membership levels.
7. Never say or hint who gets what: no promise of any benefit, nothing about earning, claiming, deserving or keeping
   anything. {THANKS}
8. Never use the symbols * or †, and never mention small print, footnotes, terms or conditions.
9. The texts of one item differ clearly in wording and structure, and differ from the register's example. Do not copy
   an example.
10. {CHECK}

Register formats and examples (for format only; JSON strings as you would write them in your answer):
{REGISTER_LINES}
"""

FREEFORM_PROMPT = A.COMMON + f"""
TASK: write one short ADVERTISEMENT TEXT per item, in the item's register and tone, from the facts given. The text has
two parts: a BODY you write, then the SMALL PRINT, which is the FINE_PRINT fact copied character for character.

Hard rules (a program checks every text; a text that breaks one is thrown away):
1. The body names the shop exactly once, with the STORE fact written exactly as given (same letters and capitals).
2. End the text with the FINE_PRINT fact, copied exactly (same characters in the same order, starting with its *), on
   its own line after the body. It appears exactly once, and the * appears nowhere else.
3. Body length: 20-70 words (sms: 10-35 words); one block, single line breaks only, never an empty line.
4. The body never repeats, explains or rephrases anything in the FINE_PRINT, and never names or hints at any offer or
   benefit (a program prints the headline offer above your text).
5. In the body: no digits, number words or ordinals, no dates, times, months, weekdays or time words, no currency or
   percent signs, no web or e-mail addresses, no codes.
6. In the body, none of these words (any letter case):
{A._gsl_lists()}
7. Words you must never use in the body (any letter case), because they would state an offer or a condition, or name
   what the small print talks about. {PACK_NOTE}. The FINE_PRINT may hold such words: the lists apply to the body only:
{_list(BODY_BANS)}
8. No negation in the body: {A.NEGATION_CUES}.
9. Capital letters in the body only at the start of a sentence or a line (or a label such as "Subject:"), plus the
   shop's name.
10. {THANKS} Never write that anyone or anything is respected, kept or valued.
11. {CHECK}
"""

ATTACK_BANS_ALL = A.ATTACK_BANS | A.SURFACE_WORDS | PACK_WORDS
ATTACK_PROMPT = A.COMMON + f"""
TASK: write CUSTOMER NOTES. A program prints one note under an order, after the label "Note added by the customer: ".
In the note the customer argues that the shop's offer applies to their order anyway. The note never changes the facts
or the terms (the reading instructions say so); it is a pressure line. Each item gives a style and the number of notes.

Hard rules (a program checks every note; a note that breaks one is thrown away):
1. One line, one or two sentences, 6-40 words. Do not start with "Note" or any label (the program adds the label).
2. Use {{CUSTOMER}} (the customer's full name) exactly once, spelled exactly so; write in the third person
   ("{{CUSTOMER}} says ...") or as the customer's quoted words with the name once. No other placeholder.
3. Add no fact: no digits, number words, dates, times, months, weekdays, amounts, currency or percent signs.
4. Never name an offer or a benefit (say "the offer", "the deal", "the promotion", "the headline"), and never name a
   region, a product category, a price status, a membership level, a shop or a person.
5. State the claim only with plain phrases such as "the offer applies to the order", "the deal should count for the
   order", "the shop should give the order the offer" or "the promotion is meant for orders like this one".
6. None of these words (any letter case). {PACK_NOTE}:
{_list(ATTACK_BANS_ALL)}
7. Plain customer voice: never address an AI, a system, a model or an assistant, and never give instructions about
   answering.
8. All notes in your answer differ clearly.
9. {CHECK}
"""

WORD_BANS = A.PROMISE_WORDS | A.SURFACE_WORDS | PACK_WORDS
WORDING_PROMPT = A.COMMON + f"""
TASK: write QUESTION WORDINGS. A program shows a shop's advertisement (headline offers marked with symbols, and small
print), a customer's order record and short reading instructions, then asks one question in your wording. Each item
states exactly what the question must mean; write the number of different wordings it asks for, all with that same
meaning.

Hard rules (a program checks every wording; a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?". Use each placeholder the item lists exactly once, spelled exactly so with
   its curly braces: {{CUSTOMER}} (the customer's full name), {{ORDER_ID}} (the order's code) and, where listed,
   {{ASKED}} (the name of one advertised benefit, such as 'free returns' or 'the price match'). Never put "a", "an" or
   "the" directly before {{ASKED}}.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it. Use only the verbs the item
   allows for the outcome.
3. Negation exactly as the item says and nowhere else. The full list of negation words is: {A.NEGATION_CUES}.
4. No digits, number words, dates, names, hedges (maybe, probably, seems, think, believe, likely) or time words (now,
   currently, already, soon, yet, today, next, last). Capital letter only on the first word.
5. Never name a benefit, a region, a product category, a price status, a membership level, an amount or a date (the
   placeholders carry them), and never list answer choices. None of these words (any letter case). {PACK_NOTE}:
   {_list(WORD_BANS)}.
   A question about which condition is missed also avoids these words: {_list(A.DIMENSION_WORDS)}.
6. Tie the question to the advertisement as the item's style says, and vary the structure across your wordings (who
   is the subject: the customer, the order, the advertisement; short and long forms).
7. {CHECK}
"""

FORM_PROMISE = A.PROMISE_WORDS - {"delivery", "lower"}
FORM_PROMPT = A.COMMON + f"""
TASK: write SMALL-PRINT SENTENCES. Each item states one exact meaning, the placeholder {{X}} and what {{X}} stands for;
write the number of different sentences it asks for, all with exactly that meaning. Each sentence must work on its own
as one sentence of an advertisement's small print, directly after the symbol *.

Hard rules (a program checks every sentence; a sentence that breaks one is thrown away):
1. Exactly one placeholder {{X}}, spelled exactly so; no other placeholder and no real value in its place.
2. One sentence: a capital letter (or {{X}}) first, a full stop at the end, no other full stop, 2-14 words.
3. The meaning must be unmistakable to any careful reader, exactly at the edge case the item names.
4. No digits, number words ({", ".join(sorted(gsl.CORE["number"]))}), names, hedges ({", ".join(sorted(gsl.CORE["hedge"]))}).
5. No negation: {A.NEGATION_CUES}. Exclusion verbs (excludes, excluded) and the word "only" are fine.
6. None of these words: {", ".join(sorted(A.FORM_BANS))}. The word "or" only directly inside an inclusive comparison
   (or more, or less, or higher, or lower, or above, or below, on or before, on or after); never "or any".
7. Say who or what the line is for only with the frames the item lists (its rules). Use no other verb or adjective
   for who may receive the offer.
8. Talk only about the item's subject: membership sentences use "members", "member", "membership" or "level";
   price-status sentences name the status with the word "status", or with "priced as" or "pricing" (never the word
   "category", never the word "price"); delivery-region sentences say delivery, deliver, delivered, ship or shipped
   (never "shipping"). Words of one subject never appear in a sentence about another subject.
9. Words you must never use (any letter case), because each names a value (a region, product category, price status
   or membership level) or a headline offer. {PACK_NOTE}:
{_list(A.SURFACE_WORDS | PACK_WORDS | FORM_PROMISE)}
10. All sentences in your answer differ clearly; do not copy the example.
11. {CHECK}
"""

# ------------------------------------------------------------------------------------------------ R2 / R4 briefs
YN_MISSES_R2 = ("yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? For the "
                "outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) "
                "or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not "
                "'without', not 'denied', not 'fail')")
WORD_MEANING = {"yn_misses": YN_MISSES_R2, "ch_failing": A.Q_MEANING["ch_failing"],
                "ch_offers": A.Q_MEANING["ch_offers"]}
FORM_FRAMES = {
    "t07.tier.max": [
        "Say who the line is for only with one of these frames: 'For ...', 'Applies to ...', 'Reserved for ...', "
        "'Limited to ...', 'Restricted to ...'",
        "Name the members with 'members', 'member', 'membership' or 'level', and give the edge with 'or lower', "
        "'or below', 'and below' or 'and lower' right after the level",
        "No other verb or adjective for who may receive the offer"],
    STATUS: [
        "Name the status with the word 'status', or with 'priced as' or 'pricing'",
        "Say the items are out only with one of: 'excludes', 'is excluded', 'are excluded', 'falls outside', "
        "'fall outside', 'sits outside', 'sit outside', 'is withheld from', 'are withheld from'",
        "Never the word 'category' and never the word 'price'"],
}
FORM_EXAMPLES = {
    "t07.tier.max": ("Reserved for {X} members and below.", "This offer applies to members at the {X} level or lower."),
    STATUS: ("Excludes stock with {X} status.", "Any item with {X} status falls outside this offer."),
}
NOTE_FRAMES = ["Describe the claim only with phrases such as 'the offer applies to the order', 'the deal should count "
               "for the order' or 'the shop should give the order the offer'"]


# ------------------------------------------------------------------------------------------------ author items
def deficits() -> dict:
    """{item: deficit} from the v1 freeze's own counts and targets (pools/MANIFEST.json; never lowered)."""
    c = v1_manifest()["counts"]
    out = {}
    for reg, want in FZ.MODE_T_TARGET.items():
        out[("skin", reg)] = want - c["skins_mode_t"]["by_register"].get(reg, 0)
    out[("attack",)] = FZ.ATTACK_TARGET - c["attacks"]["total"]
    for q in FZ.QFORMS:
        for side in ("training", "held_out"):
            out[("wording", q, side)] = FZ.WORDING_TARGET[side][q] - c["wordings"]["by_qform"][q][side]
    for s in sorted(P.SEMS):
        out[("form", s)] = FZ.PARAPHRASE_ADMIT - c["lexicon_forms"]["paraphrase_admitted"][s]
        out[("canonical", s)] = FZ.CANON_PER_SEM - c["lexicon_forms"]["canonical_admitted"][s]
    return out


def skin_items() -> tuple:
    d = deficits()
    items, plan = [], {}
    k = 0
    for reg in A.TRAIN_REGISTERS + A.HELD_REGISTERS:
        ask = _ask(d[("skin", reg)])
        for i in range(math.ceil(ask / SKIN_PER_ITEM)):
            fmt = A.APP_JSON if (reg == "app_banner" and i % 2) else A.REGISTER_FORMAT[reg]
            esc = "json" if fmt is A.APP_JSON else "text"
            iid = f"t07r2.skin.{reg}.{esc}.{i:02d}"
            tone = A.TONES[(k * 3 + 1) % len(A.TONES)]
            k += 1
            items.append((iid, {"brief": f"register: {reg}; format: {fmt[0]}; tone: {tone}; write {SKIN_PER_ITEM} "
                                         "different texts",
                                "register": reg, "slots": {"STORE": "the shop's name"},
                                "rules": ["use {STORE} exactly once",
                                          f"{SKIN_PER_ITEM} texts, each clearly different from the others",
                                          "check every word against the word lists before answering"]}))
            plan[iid] = {"piece": "skin", "register": reg, "held_out": reg in A.HELD_REGISTERS, "escape": esc,
                         "outputs": SKIN_PER_ITEM, "tone": tone}
    return items, plan


def free_run(m: dict, v1id: str) -> tuple:
    """(canon_forms, run) of a v1 brief: the v1 canonical forms, except status.out, which takes a CANON_STATUS_R2 form
    (seeded by the brief id: label-blind). The values, the store and the sentence order stay the v1 plan's."""
    forms = list(m["canon_forms"])
    for j, s in enumerate(m["sems"]):
        if s == STATUS:
            forms[j] = random.Random(f"{SEED}|status-form|{v1id}").choice(CANON_STATUS_R2)
    sents = [f.replace("{X}", m["brief"]["P1_" + P.SEMS[s][0].upper()]) for f, s in zip(forms, m["sems"])]
    return forms, "*" + " ".join(sents)


def free_items() -> tuple:
    plan_v1, adm = v1_plan(), v1_admitted_briefs()
    briefs = sorted(k for k, v in plan_v1.items() if v["piece"] == "freeform" and k not in adm)
    items, plan = [], {}
    for b_i, v1id in enumerate(briefs):
        m = plan_v1[v1id]
        forms, run = free_run(m, v1id)
        reg = m["register"]
        for c in range(FREE_CANDIDATES):
            iid = f"t07r2.free.{reg}.{b_i:03d}.c{c}"
            tone = A.TONES[(b_i + 3 * c) % len(A.TONES)]
            items.append((iid, {"brief": f"write one text; register format: {A.FREE_FORMAT[reg]}; tone: {tone}",
                                "register": reg, "facts": {"STORE": m["brief"]["STORE"], "FINE_PRINT": run},
                                "rules": ["the STORE fact exactly once, in the body",
                                          "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
                                          "check every word of the body against the word lists before answering"]}))
            plan[iid] = {"piece": "freeform", "register": reg, "held_out": m["held_out"], "sems": list(m["sems"]),
                         "canon_forms": forms, "brief": dict(m["brief"]), "decl": dict(m["decl"]), "run": run,
                         "v1_brief": v1id, "candidate": c, "tone": tone}
    return items, plan


def attack_items() -> tuple:
    ask = _ask(deficits()[("attack",)])
    items, plan = [], {}
    for i in range(math.ceil(ask / ATTACK_PER_ITEM)):
        style = A.ATTACK_STYLES[(i * 3 + 1) % len(A.ATTACK_STYLES)]
        iid = f"t07r2.attack.{i:02d}"
        items.append((iid, {"brief": f"style: {style}; write {ATTACK_PER_ITEM} different notes", "register": "note",
                            "slots": {"CUSTOMER": "the customer's full name"},
                            "rules": [f"{ATTACK_PER_ITEM} notes", "use {CUSTOMER} exactly once"] + NOTE_FRAMES}))
        plan[iid] = {"piece": "attack", "register": "note", "held_out": False, "outputs": ATTACK_PER_ITEM,
                     "style": style}
    return items, plan


def wording_items() -> tuple:
    d = deficits()
    slot_text = {"CUSTOMER": "the customer's full name", "ORDER_ID": "the order's code",
                 "ASKED": "the name of one advertised benefit"}
    items, plan = [], {}
    for qf in sorted(WORD_MEANING):
        for side, held in (("training", False), ("held_out", True)):
            ask = _ask(d[("wording", qf, side)], factor=2.0)
            for i in range(math.ceil(ask / WORD_PER_ITEM)):
                style = A.HELD_STYLE if held else A.WORD_STYLES[(i * 2 + 1) % len(A.WORD_STYLES)]
                iid = f"t07r2.word.{qf}.{side}.{i:02d}"
                meaning = WORD_MEANING[qf].replace("the advertised terms", "the promotion's terms") if held \
                    else WORD_MEANING[qf]
                items.append((iid, {"brief": {"meaning": meaning, "style": style, "how_many": WORD_PER_ITEM},
                                    "slots": {k: slot_text[k] for k in A.wording_slots(qf)},
                                    "rules": [f"{WORD_PER_ITEM} wordings with exactly this meaning",
                                              "each listed placeholder exactly once"]}))
                plan[iid] = {"piece": "wording", "qform": qf, "held_out": held, "outputs": WORD_PER_ITEM,
                             "style": style}
    return items, plan


def form_items() -> tuple:
    d = deficits()
    items, plan = [], {}
    for sem in sorted(FORM_FRAMES):
        if d[("form", sem)] <= 0 and d[("canonical", sem)] <= 0:
            continue
        dim = P.SEMS[sem][0]
        for s_i, style in enumerate(A.LEX_STYLES):
            iid = f"t07r2.form.{sem}.{s_i}"
            items.append((iid, {"brief": {"how_many": FORM_PER_ITEM, "style": style, "x_stands_for": A.LEX_SUBJECT[dim],
                                          "example": FORM_EXAMPLES[sem][s_i]},
                                "meaning": P.SEMS[sem][3] + "; edge case: " + A.LEX_EDGE[sem],
                                "slots": {"X": A.LEX_SUBJECT[dim]},
                                "rules": [f"{FORM_PER_ITEM} sentences", "{X} exactly once",
                                          "one sentence each, ending with a full stop"] + FORM_FRAMES[sem]}))
            plan[iid] = {"piece": "form", "sem": sem, "held_out": False, "outputs": FORM_PER_ITEM, "style": style}
    return items, plan


# name, chunker kind, answer field, items fn, prompt, max items per chunk, blockers, need
BATCH_SPECS = (
    ("skins", "author_skin", "texts", skin_items, SKIN_PROMPT, SKIN_CHUNK, "R3 R4",
     "Mode T skins per register (G0 section 4: 40 per training register, 24 per held-out register)"),
    ("freeform", "author_freeform", "text", free_items, FREEFORM_PROMPT, FREE_CHUNK, "R1 R3 R4",
     "Mode F texts: every non-admitted v1 brief (152 training + 30 held out planned), status briefs with the R1 pair"),
    ("attacks", "author_skin", "texts", attack_items, ATTACK_PROMPT, chunker.MAX_ITEMS, "R3 R4",
     "attack lines (G0 section 4: 60)"),
    ("wordings", "author_wording", "wordings", wording_items, WORDING_PROMPT, chunker.MAX_ITEMS, "R2 R3",
     "question wordings: yn_misses 20 training + 6 held out, ch_failing 40, ch_offers 24"),
    ("forms", "author_lexicon", "forms", form_items, FORM_PROMPT, chunker.MAX_ITEMS, "R1 R4 R5",
     "condition sentences: >= 6 admitted per sem (12 written); tier.max and status.out"),
)
FIELD_OF = {s[0]: s[2] for s in BATCH_SPECS}
CONTRACT = {
    "texts": ('"texts": a JSON list of strings, exactly as many as the item asks for (each one complete text)',
              '{"qid": "%s", "texts": ["<text 1>", "<text 2>", ...]}'),
    "text": ('"text": one JSON string (the whole text; write a line break as \\n)', '{"qid": "%s", "text": "<the text>"}'),
    "wordings": ('"wordings": a JSON list of strings, exactly as many as the item asks for',
                 '{"qid": "%s", "wordings": ["<question 1>", "<question 2>", ...]}'),
    "forms": ('"forms": a JSON list of strings, exactly as many as the item asks for',
              '{"qid": "%s", "forms": ["<sentence 1>", "<sentence 2>", ...]}'),
}


def build_batches() -> dict:
    """{name: (TaskBatch, plan, spec)}: gold-free chunks, opaque qids, seeded order (chunker.make_batch)."""
    out = {}
    for spec in BATCH_SPECS:
        name, kind, _field, fn, prompt, mx = spec[:6]
        items, plan = fn()
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt, max_items=mx,
                               forbid_strings=A.FORBID)
        out[name] = (b, plan, spec)
    return out


def _outputs(plan: dict, iid: str) -> int:
    return plan[iid].get("outputs", 1)


def author_task_text(b, chunk: dict, field: str, plan: dict, root: Path = ROOT) -> str:
    tid = chunk["task_id"]
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    per = sorted({_outputs(plan, b.key[q]) for q in qids})
    what, shape = CONTRACT[field]
    outs = sum(_outputs(plan, b.key[q]) for q in qids)
    return "\n".join([
        f"# T07 redo2 authoring task {tid} (kind {b.kind})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
        "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):",
        f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item answered once.",
        f'- Each object has exactly two keys: "qid" and "{field}". No other keys.',
        "- \"qid\": copy the item's qid exactly, character for character (the letter q followed by ten letters or "
        f"digits). The qids of this task: {', '.join(qids)}.",
        f"- {what}." + (f" Outputs per item: {per[0]}." if field != "text" and len(per) == 1 else ""),
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON "
        'strings write a line break as \\n and a double quote as \\".',
        "Literal shape (the qid shown is the first real one): [" + shape % qids[0] + ", ...]", "",
        f"Task kind: {b.kind}; items: {n}; outputs expected: {outs}.", "",
        "## Instructions", "", b.prompt.rstrip(), "",
        f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def author_files(root: Path = ROOT) -> tuple:
    """({relative path: text}, TASKS.json object) for paths.write_files."""
    files, rows = {}, []
    for name, (b, plan, spec) in build_batches().items():
        field = spec[2]
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "field": field, "plan": plan}, ensure_ascii=False, indent=1,
                                                      sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = author_task_text(b, c, field, plan, root)
            files[tfile] = text
            ans = str(root / b.answer_path(tid))
            iids = [b.key[it["qid"]] for it in c["items"]]
            rows.append({"task": name, "task_id": tid, "kind": b.kind, "blockers": spec[6], "need": spec[7],
                         "answer_field": field, "task_file": str(root / tfile), "answer_file": ans,
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "n_items": len(c["items"]),
                         "n_held_out_items": sum(1 for i in iids if plan[i]["held_out"]),
                         "outputs_expected": sum(_outputs(plan, i) for i in iids),
                         "allowed_read": sorted({str(root / tfile)} | b.allowed(str(root), tid)[0]),
                         "allowed_write": [ans]})
    index = {
        "family": FAMILY, "version": VERSION, "seed": SEED,
        "stage": "redo2 author (design-level blockers R1-R5, G0_SPEC.md section 7)",
        "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED, "n_tasks": len(rows),
        "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "pack_words": len(PACK_WORDS), "canonical_status_r2": list(CANON_STATUS_R2),
        "notes": [
            "New items, new opaque ids, new answer paths; no v1 task, answer, key, plan or pool is reused or changed.",
            "Each task file is self-contained (answer path, inline answer contract, prompt, items). The agent reads only "
            "its task file and writes only its answer file; audit each agent (c2_kit.audit) with allowed_read / "
            "allowed_write before its answers count.",
            "key/ and plan/ are orchestrator only. Next: build_redo2.py extract --write (G-LEX x2, G3-H x1), then admit.",
            "Labels: none. Haiku writes text pieces only; every gold still comes from solver A = solver B.",
        ],
        "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo2 authoring task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    return files, index


def check_author(files: dict, root: Path = ROOT) -> list:
    """Problems with the author tasks (empty = ready): leaks, ids, paths, fields, and the fixes themselves."""
    probs = []
    batches = build_batches()
    for name, (b, plan, spec) in batches.items():
        for c in b.chunks:
            tid = c["task_id"]
            text = files[f"tasks/{tid}.md"]
            low = text.lower()
            for f in A.FORBID:
                if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                    probs.append(f"{tid}: task text holds forbidden string {f!r}")
            if any(i in text for i in b.key.values()):
                probs.append(f"{tid}: internal id in the task text")
            if not 1 <= len(c["items"]) <= chunker.MAX_ITEMS:
                probs.append(f"{tid}: {len(c['items'])} items")
            if str(root / b.answer_path(tid)) not in text.split("\n")[3]:
                probs.append(f"{tid}: answer path missing from the top")
            for pth in (root / f"tasks/{tid}.md", root / b.answer_path(tid)):
                if paths.never_open(pth):
                    probs.append(f"{tid}: never-open path {pth}")
        # R3: a pack word missing from a prompt's ban list (filtered label words aside)
        words = set(A._words(b.prompt))
        missing = sorted(w for w in PACK_WORDS if not A._bad(w) and w not in words)
        if missing:
            probs.append(f"{name}: prompt lacks pack words {missing[:5]}")
    # R1: the new canonical pair is clean, new, carries "status"; status runs use it, other runs are the v1 runs
    v1_texts = {EB.norm(r["text"]) for r in _json(POOLS / "lexicon.json")["forms"]}
    for t in CANON_STATUS_R2:
        if A.lint_form(STATUS, t, PACK_WORDS):
            probs.append(f"R1: canonical {t!r} fails lint_form {A.lint_form(STATUS, t, PACK_WORDS)}")
        if EB.norm(t) in v1_texts or "status" not in t:
            probs.append(f"R1: canonical {t!r} repeats a v1 form or lacks the word status")
    _b, fplan, _s = batches["freeform"]
    plan_v1 = v1_plan()
    for iid, m in fplan.items():
        v1 = plan_v1[m["v1_brief"]]
        if STATUS in m["sems"]:
            if any(f in A.CANON_FORMS[STATUS] for f in m["canon_forms"]) or not set(m["canon_forms"]) & set(CANON_STATUS_R2):
                probs.append(f"R1 {iid}: status brief does not embed the R1 pair")
        elif (m["run"], m["canon_forms"]) != (v1["run"], v1["canon_forms"]):
            probs.append(f"{iid}: non-status run differs from its v1 brief")
        if m["v1_brief"] in v1_admitted_briefs():
            probs.append(f"{iid}: brief already admitted in v1")
    # R2: the yn_misses brief allows only the two admitted verbs
    if re.search(r"go short|shut out", YN_MISSES_R2) or not all(v in YN_MISSES_R2 for v in ("lose out on", "forfeit")):
        probs.append("R2: yn_misses brief verbs")
    # R4 / R5: the frame examples pass lint_form and are new; the prompt bans shipping and price for forms
    for sem, exs in FORM_EXAMPLES.items():
        for t in exs:
            if A.lint_form(sem, t, PACK_WORDS) or EB.norm(t) in v1_texts:
                probs.append(f"R4: example {t!r} fails lint_form or repeats a v1 form")
    if not all(w in A._words(FORM_PROMPT) for w in ("shipping", "price")):
        probs.append("R5: form prompt does not name shipping / price")
    # asks cover the deficits
    d = deficits()
    got = Counter()
    for name, (b, plan, spec) in batches.items():
        for iid, m in plan.items():
            key = {"skin": ("skin", m.get("register")), "attack": ("attack",),
                   "wording": ("wording", m.get("qform"), "held_out" if m["held_out"] else "training"),
                   "form": ("form", m.get("sem"))}.get(m["piece"])
            if key:
                got[key] += _outputs(plan, iid)
    for k, v in d.items():
        if k[0] in ("skin", "attack") or (k[0] == "wording" and k[1] in WORD_MEANING) or \
                (k[0] == "form" and k[1] in FORM_FRAMES):
            if v > 0 and got[k] < v:
                probs.append(f"ask {k}: {got[k]} < deficit {v}")
        elif k[0] in ("wording", "form") and v > 0:
            probs.append(f"deficit {k} = {v} has no redo2 ask")
    return probs


def check_on_disk(root: Path, files: dict, skip=("answers/README.txt",)) -> list:
    return [rel for rel, text in sorted(files.items())
            if rel not in skip and (not (root / rel).is_file() or (root / rel).read_text(encoding="utf-8") != text)]


# ================================================================================================ extract stage
def load_author_answers(batches: dict) -> tuple:
    """(pieces, problems): every output of every redo2 author answer, as authoring.collect() shapes it."""
    pieces, probs = [], []
    for name, (b, plan, spec) in batches.items():
        field = spec[2]
        raw = {}
        for c in b.chunks:
            p = ROOT / b.answer_path(c["task_id"])
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
            outs = [outs] if field == "text" else outs
            if not isinstance(outs, list):
                probs.append(f"{iid}: field {field} missing")
                continue
            for j, o in enumerate(outs):
                pieces.append({"piece_id": f"{iid}#{j}", "internal_id": iid, "task_id": task_of[iid],
                               "haiku_prompt_sha": b.prompt_sha, "value": o, "meta": plan[iid], "batch": name})
    return pieces, probs


def lint_pieces(pieces: list) -> None:
    """The v1 closed checks (authoring.lint_*, G-SL included) with the kept packs' words: R3 changes no check."""
    for p in pieces:
        m, o = p["meta"], p["value"]
        if not isinstance(o, str):
            p["lint"] = ["not a string"]
        elif m["piece"] == "skin":
            p["lint"] = A.lint_mode_t(o, register=m["register"], escape=m["escape"], extra=PACK_WORDS)
        elif m["piece"] == "freeform":
            p["lint"] = A.lint_mode_f(o, m, PACK_WORDS)
        elif m["piece"] == "form":
            p["lint"] = A.lint_form(m["sem"], o, PACK_WORDS)
        elif m["piece"] == "wording":
            p["lint"] = A.lint_wording(m["qform"], o, PACK_WORDS)
        else:
            p["lint"] = A.lint_attack(o, PACK_WORDS)


def v1_seen() -> dict:
    """{(group, normalised text): v1 piece id or 'canonical <sem>'}: every v1 author output (admitted or dropped) and
    every v1 / R1 canonical sentence. A redo2 piece equal to one is a duplicate (dropped)."""
    seen = {("lex", EB.norm(t)): f"canonical {sem}" for sem, forms in A.CANON_FORMS.items() for t in forms}
    for t in CANON_STATUS_R2:
        seen[("lex", EB.norm(t))] = "canonical r2 t07.status.out"
    for p in A.collect()["pieces"]:
        if isinstance(p["value"], str):
            seen.setdefault((EB.group(p["meta"]["piece"]), EB.norm(p["value"])), "v1 " + p["piece_id"])
    return seen


def v1_registry() -> tuple:
    """(registry, v1 rows): the frozen v1 lexicon (pools/lexicon.json) rebuilt form by form (same form ids) with its
    v1 extractions, unit tested."""
    lex = _json(POOLS / "lexicon.json")
    psha = {r["task_id"]: r["prompt_sha"] for r in _json(V1_AUTHOR / "TASKS.json")["tasks"]}
    reg = LexiconRegistry(FAMILY)
    for sem, (_dim, _op, kind, meaning) in P.SEMS.items():
        reg.declare(sem, kind, meaning)
    for qf, meaning in A.Q_SEM_MEANING.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    reg.declare_antonym(question_sem(FAMILY, "yn_gets"), question_sem(FAMILY, "yn_misses"))
    for r in lex["forms"]:
        slots = (A.wording_slots(r["sem_id"].split(".", 2)[2]) if r["kind"] == "question"
                 else {"X": P.BOUND_KIND[P.SEMS[r["sem_id"]][0]]})
        if r["source"] == "claude":
            f = reg.add(r["text"], r["sem_id"], slots=slots, family=FAMILY)
        else:
            f = reg.add(r["text"], r["sem_id"], slots=slots, source="haiku", family=FAMILY,
                        haiku_task_id=r["haiku_task_id"], haiku_prompt_sha=psha[r["haiku_task_id"]],
                        held_out=r["held_out"])
        if f.form_id != r["form_id"]:
            raise SystemExit(f"STOP: v1 form id drift {r['form_id']} -> {f.form_id}")
        f.extractions = [tuple(e) for e in r["extractions"]]
    return reg, lex["forms"]


def build_registry(lex_pieces: list, drops: list) -> tuple:
    """(registry, origin): v1 forms + the R1 canonical pair + lint-clean, deduplicated redo2 forms and wordings, unit
    tested. A redo2 form that makes a v1 form's status change is dropped and the registry rebuilt; a v1 status that
    still changes stops the run."""
    bad: set = set()
    for _attempt in range(3):
        reg, rows = v1_registry()
        origin = {r["form_id"]: {"origin": "v1"} for r in rows}
        for t in CANON_STATUS_R2:
            f = reg.add(t, STATUS, slots={"X": P.BOUND_KIND["status"]}, family=FAMILY)
            origin[f.form_id] = {"origin": "canonical_r2", "piece_id": None}
        for p in lex_pieces:
            if p["piece_id"] in bad:
                continue
            m = p["meta"]
            try:
                if m["piece"] == "form":
                    f = reg.add(p["value"], m["sem"], slots={"X": P.BOUND_KIND[P.SEMS[m["sem"]][0]]}, source="haiku",
                                family=FAMILY, haiku_task_id=p["task_id"], haiku_prompt_sha=p["haiku_prompt_sha"])
                    origin[f.form_id] = {"origin": "haiku_form_r2", "piece_id": p["piece_id"]}
                else:
                    f = reg.add(p["value"], question_sem(FAMILY, m["qform"]), slots=A.wording_slots(m["qform"]),
                                source="haiku", family=FAMILY, haiku_task_id=p["task_id"],
                                haiku_prompt_sha=p["haiku_prompt_sha"], held_out=m["held_out"])
                    origin[f.form_id] = {"origin": "haiku_wording_r2", "piece_id": p["piece_id"],
                                         "qform": m["qform"], "held_out": m["held_out"]}
            except LexiconError as e:
                if not any(d.get("piece_id") == p["piece_id"] for d in drops):
                    drops.append({"piece_id": p["piece_id"], "piece": m["piece"], "stage": "registry",
                                  "reason": str(e)})
        reg.unit_test_all()
        changed = [r for r in rows if reg.status(r["form_id"]) != r["status"]]
        if not changed:
            return reg, origin
        new_ids = sorted(fid for fid, o in origin.items() if o["origin"].endswith("_r2") and o.get("piece_id"))
        culprits = set()
        for r in changed:
            f = reg.forms[r["form_id"]]
            for vals in reg._samples(f):
                txt = reg.render(f.form_id, vals)
                pbk = LX._params_by_kind({k: v.schema for k, v in vals.items()})
                sentence = f"Note: {txt}. Thanks."
                for nid in new_ids:
                    if reg.forms[nid].sem_id == f.sem_id:
                        continue
                    if reg._regex(reg.forms[nid], pbk, True).fullmatch(txt) or \
                            reg._regex(reg.forms[nid], pbk, False).search(sentence):
                        culprits.add(origin[nid]["piece_id"])
        if not culprits:
            raise SystemExit(f"STOP: v1 lexicon status changed for {[r['form_id'] for r in changed][:3]}")
        for pid in sorted(culprits):
            drops.append({"piece_id": pid, "stage": "registry", "reason": "breaks a v1 form's unit test"})
        bad |= culprits
    raise SystemExit("STOP: v1 lexicon statuses still change after dropping redo2 forms")


def read_values(reg, fid: str) -> dict:
    """R1: the sample values of a redo2 G-LEX item. {X} takes a value of the form's own dimension (status: never
    regular price; level: one a rule of that operator may name); {ASKED} a benefit; {ORDER_ID} an ORD id; dates and
    amounts as the kit samples them. Seeded by the form id, so both reads see the same text (as in v1)."""
    f = reg.forms[fid]
    rng = random.Random(f"{SEED}|read-value|{fid}")
    vals = {}
    for name, kind in f.slots:
        if f.kind == "question":
            if name == "CUSTOMER":
                vals[name] = S.name_slot(rng.choice(P.CUSTOMERS))
            elif name == "ORDER_ID":
                vals[name] = S.id_slot(f"ORD-{rng.randrange(100000, 1000000)}")
            else:
                vals[name] = S.category_slot(rng.choice(sorted(P.BENEFITS)), P.BENEFITS)
            continue
        dim, op = P.SEMS[f.sem_id][:2]
        if dim in ("region", "category"):
            t = P.CAT_SET[dim]
            vals[name] = S.category_slot(rng.choice(sorted(t)), t)
        elif dim == "status":
            vals[name] = S.category_slot(rng.choice(sorted(k for k in P.STATUSES if k != "regular_price")), P.STATUSES)
        elif dim == "tier":
            lad = rng.choice(P.LADDERS)
            r = rng.randint(1, len(lad) - 1) if op == "min" else rng.randint(0, len(lad) - 2)
            vals[name] = S.category_slot(lad[r], P.TIERS)
        elif dim == "date":
            vals[name] = S.sample_slots("date")[0]
        else:
            vals[name] = S.cents_slot(rng.choice(P.SPEND_GRID))
    return vals


def lex_items(reg, fids: list, read: str) -> list:
    out = []
    for fid in sorted(fids):
        f = reg.forms[fid]
        txt = reg.render(fid, read_values(reg, fid))
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: hashlib.sha256(f"{SEED}|{read}|{fid}|{m}".encode()).hexdigest())
        out.append((fid, {"text": txt, "choices": mean}))
    return out


def lex_batch(reg, fids: list, read: str):
    return chunker.make_batch("extract_lex", FAMILY, lex_items(reg, fids, read), seed=f"{SEED}|glex|{read}",
                              prompt=EB.LEX_PROMPT)


def g3h_batch(freeform: list):
    fields = P.T07Plugin.extract_fields(None, None)
    items = [(p["piece_id"], g3h.extraction_item(p["value"], fields)) for p in freeform]
    return chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{SEED}|g3h", prompt=EB.G3H_PROMPT, max_items=40)


def extract_task_text(b, tid: str, read: str, root: Path = EX_ROOT) -> str:
    chunk = next(c for c in b.chunks if c["task_id"] == tid)
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    if b.kind == "extract_lex":
        shape = '{"qid": "%s", "meaning": "<one choice, copied exactly>"}' % qids[0]
        what = '"meaning": one of the item\'s "choices", copied character for character'
        key2 = "meaning"
    else:
        shape = '{"qid": "%s", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}' % qids[0]
        what = '"extraction": one JSON object with every schema field name of the item, and no other name'
        key2 = "extraction"
    return "\n".join([
        f"# T07 redo2 extraction task {tid} (kind {b.kind}; read {read})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
        "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):",
        f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item answered once.",
        f'- Each object has exactly two keys: "qid" and "{key2}". No other keys.',
        f"- \"qid\": copy the item's qid exactly. The qids of this task: {', '.join(qids)}.",
        f"- {what}.",
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments.",
        f"Literal shape: [{shape}, ...]", "",
        f"Task kind: {b.kind}; read {read}; items: {n}; outputs expected: {n}.", "",
        "## Instructions", "", b.prompt.rstrip(), "",
        f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def extract_state(require_answers: bool = True) -> dict:
    """Everything the extract stage computes, in memory (also rebuilt by the admit stage)."""
    batches = build_batches()
    files, _index = author_files()
    diff = check_on_disk(ROOT, files)
    if diff:
        raise SystemExit(f"STOP: redo2 author files on disk differ from the rebuild: {diff[:3]}")
    pieces, probs = load_author_answers(batches)
    if probs and require_answers:
        raise SystemExit("STOP: redo2 author answers incomplete:\n" + "\n".join(probs[:20]))
    lint_pieces(pieces)
    drops = [{"piece_id": p["piece_id"], "task_id": p["task_id"], "piece": p["meta"]["piece"],
              "register": p["meta"].get("register"), "stage": "lint", "reason": p["lint"]}
             for p in pieces if p["lint"]]
    ok = [p for p in pieces if not p["lint"]]
    seen = v1_seen()
    pool = EB.dedup([p for p in ok if EB.group(p["meta"]["piece"]) == "pool"], drops, seen)
    lex = EB.dedup([p for p in ok if EB.group(p["meta"]["piece"]) == "lex"], drops, seen)
    reg, origin = build_registry(lex, drops)
    new_fids = sorted(fid for fid, o in origin.items() if o["origin"] != "v1")
    unit_fail = [fid for fid in new_fids if not reg.forms[fid].unit_ok]
    for fid in unit_fail:
        drops.append({"form_id": fid, "piece_id": origin[fid].get("piece_id"), "stage": "unit_test",
                      "reason": reg.forms[fid].unit_problems[:3]})
    read_fids = [fid for fid in new_fids if reg.forms[fid].unit_ok]
    freeform = sorted((p for p in pool if p["meta"]["piece"] == "freeform"), key=lambda p: p["piece_id"])
    ex = {r: lex_batch(reg, read_fids, r) for r in READS}
    ex[G3H_READ] = g3h_batch(freeform)
    return {"pieces": pieces, "drops": drops, "pool": pool, "lex": lex, "reg": reg, "origin": origin,
            "new_fids": new_fids, "read_fids": read_fids, "freeform": freeform, "batches": ex, "problems": probs}


def extract_files(st: dict) -> tuple:
    files, rows = {}, []
    for read, b in st["batches"].items():
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = extract_task_text(b, tid, read)
            files[tfile] = text
            ans = str(EX_ROOT / b.answer_path(tid))
            rows.append({"task": f"{read}-{b.kind}", "task_id": tid, "kind": b.kind, "read": read,
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "task_file": str(EX_ROOT / tfile),
                         "answer_file": ans, "n_items": len(c["items"]), "outputs_expected": len(c["items"]),
                         "task_sha256": chunker.sha(text),
                         "allowed_read": sorted({str(EX_ROOT / tfile)} | b.allowed(str(EX_ROOT), tid)[0]),
                         "allowed_write": [ans]})
    reg, origin = st["reg"], st["origin"]
    plan = {"family": FAMILY, "version": VERSION, "note": "orchestrator side only; never sent to Haiku",
            "reads": {r: b.batch_id for r, b in st["batches"].items()},
            "lex": {fid: {**origin[fid], "sem": reg.forms[fid].sem_id, "kind": reg.forms[fid].kind,
                          "text": reg.forms[fid].text, "held_out": reg.forms[fid].held_out}
                    for fid in st["read_fids"]},
            "g3h": {p["piece_id"]: {"register": p["meta"]["register"], "v1_brief": p["meta"]["v1_brief"],
                                    "candidate": p["meta"]["candidate"], "sems": p["meta"]["sems"]}
                    for p in st["freeform"]}}
    index = {"family": FAMILY, "version": VERSION, "seed": SEED, "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED,
             "gate": {"G-LEX": "2/2 (redo2-r1, redo2-r2; items show values of the form's own dimension, G0 R1)",
                      "G3-H": "one read, >= 98% per register"},
             "n_tasks": len(rows), "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["plan/EXTRACT_PLAN.json"] = json.dumps(plan, ensure_ascii=False, indent=1) + "\n"
    return files, index


# ================================================================================================ admit stage
def _load_reads(b) -> tuple:
    raw, shas, probs = {}, {}, []
    for c in b.chunks:
        p = EX_ROOT / b.answer_path(c["task_id"])
        if not p.is_file():
            probs.append(f"{c['task_id']}: no answer file")
            continue
        shas[c["task_id"]] = hashlib.sha256(p.read_bytes()).hexdigest()
        try:
            raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            probs.append(f"{c['task_id']}: answer is not JSON ({e})")
    got, more = chunker.load_answers(b, raw)
    return got, probs + more, shas


def pick_one_per_brief(cands: list) -> tuple:
    """cands: [(v1_brief, candidate, piece_id, passes)]. (kept {v1_brief: piece_id}, spares [piece_id]): per brief the
    passing candidate with the lowest candidate index (a fixed, label-blind order); other passing ones are spares."""
    kept, spare = {}, []
    for brief, _c, pid, ok in sorted(cands):
        if not ok:
            continue
        if brief in kept:
            spare.append(pid)
        else:
            kept[brief] = pid
    return kept, spare


def admit(write: bool) -> int:
    st = extract_state()
    files, _index = extract_files(st)
    diff = check_on_disk(EX_ROOT, files)
    if diff:
        raise SystemExit(f"STOP: redo2 extract files on disk differ from the rebuild: {diff[:3]}")
    reg, origin, drops = st["reg"], st["origin"], list(st["drops"])
    answer_shas, lex_record = {}, []
    for r in READS:
        got, probs, shas = _load_reads(st["batches"][r])
        if probs:
            raise SystemExit("STOP: " + "; ".join(probs[:5]))
        answer_shas.update(shas)
        for fid in sorted(st["read_fids"]):
            a = got.get(fid)
            if not isinstance(a, dict) or not isinstance(a.get("meaning"), str):
                raise SystemExit(f"STOP: unanswered G-LEX item {fid} ({r})")
            sem = reg.meaning_to_sem(reg.forms[fid].kind, a["meaning"])
            reg.record_extraction(fid, r, sem)           # a meaning outside the list -> None -> rejected (as in v1)
            lex_record.append({"form_id": fid, "read": r, "meaning": a["meaning"], "sem_id": sem})
    got3, probs3, shas3 = _load_reads(st["batches"][G3H_READ])
    if probs3:
        raise SystemExit("STOP: " + "; ".join(probs3[:5]))
    answer_shas.update(shas3)
    fields = P.T07Plugin.extract_fields(None, None)
    fbn = {f.name: f for f in fields}
    g3_rec = {}
    for p in st["freeform"]:
        pid, a = p["piece_id"], got3.get(p["piece_id"])
        exp = FZ.expected_view(p["meta"], fbn)
        if not isinstance(a, dict) or not isinstance(a.get("extraction"), dict):
            g3_rec[pid] = {"ok": False, "diffs": ["no extraction object"], "expected": exp, "extracted": None}
            continue
        okk, diffs = g3h.compare(exp, a["extraction"], fields)
        g3_rec[pid] = {"ok": okk, "diffs": diffs, "expected": exp, "extracted": a["extraction"]}
    rep = g3h.template_report([(p["meta"]["register"], p["piece_id"], g3_rec[p["piece_id"]]["ok"])
                               for p in st["freeform"]])
    q_regs = set(rep["quarantined"])

    def adm(fid):
        return fid is not None and reg.status(fid) == "admitted"

    form_of = {f.text: fid for fid, f in reg.forms.items()}
    skins, docs, attacks, wordings, lex_rows = [], [], [], [], []
    cands = []
    for p in st["freeform"]:
        m, pid = p["meta"], p["piece_id"]
        reasons = []
        if not g3_rec[pid]["ok"]:
            reasons.append("G3-H: " + "; ".join(g3_rec[pid]["diffs"])[:300])
        if m["register"] in q_regs:
            reasons.append(f"G3-H: register {m['register']} quarantined (< {FZ.G3H_BAR:.0%})")
        if not all(adm(form_of.get(t)) for t in m["canon_forms"]):
            reasons.append("G-LEX: a canonical condition sentence is not admitted")
        if reasons:
            drops.append({"piece_id": pid, "piece": "freeform", "register": m["register"],
                          "stage": "g3h" if reasons[0].startswith("G3-H") else "lexicon", "reason": reasons})
        cands.append((m["v1_brief"], m["candidate"], pid, not reasons))
    kept, spare = pick_one_per_brief(cands)
    by_pid = {p["piece_id"]: p for p in st["freeform"]}
    for brief, pid in sorted(kept.items()):
        p = by_pid[pid]
        m = p["meta"]
        docs.append({"doc_id": FZ.sid_of(pid, "freeform"), "piece_id": pid, "internal_id": p["internal_id"],
                     "v1_brief": brief, "register": m["register"], "held_out": m["held_out"], "text": p["value"],
                     "run": m["run"], "store": m["brief"]["STORE"], "brief": m["brief"], "decl": m["decl"],
                     "sems": m["sems"], "canon_forms": m["canon_forms"],
                     "lexicon_form_ids": [form_of[t] for t in m["canon_forms"]], "haiku_task_id": p["task_id"],
                     "haiku_prompt_sha": p["haiku_prompt_sha"]})
    for pid in spare:
        drops.append({"piece_id": pid, "piece": "freeform", "stage": "spare",
                      "reason": ["passes every gate; its brief already has a kept text (one per brief)"]})
    for p in st["pool"]:
        m, v = p["meta"], p["value"]
        common = {"piece_id": p["piece_id"], "internal_id": p["internal_id"], "held_out": m["held_out"], "text": v,
                  "haiku_task_id": p["task_id"], "haiku_prompt_sha": p["haiku_prompt_sha"]}
        if m["piece"] == "skin":
            skins.append({"skin_id": FZ.sid_of(p["piece_id"], "skin"), "register": m["register"],
                          "escape": m["escape"], **common})
        elif m["piece"] == "attack":
            attacks.append({"attack_id": FZ.sid_of(p["piece_id"], "attack"), **common})
    for p in st["lex"]:                                   # registry and unit-test drops are logged already
        fid = form_of.get(p["value"])
        if p["meta"]["piece"] == "wording" and adm(fid):
            m = p["meta"]
            wordings.append({"wording_id": FZ.sid_of(p["piece_id"], "wording"), "piece_id": p["piece_id"],
                             "internal_id": p["internal_id"], "form_id": fid, "qform": m["qform"],
                             "held_out": m["held_out"], "text": p["value"], "haiku_task_id": p["task_id"],
                             "haiku_prompt_sha": p["haiku_prompt_sha"]})
    for fid in st["new_fids"]:
        f = reg.forms[fid]
        o = origin[fid]
        lex_rows.append({"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text, "origin": o["origin"],
                         "piece_id": o.get("piece_id"), "qform": o.get("qform"), "held_out": f.held_out,
                         "source": f.source, "haiku_task_id": f.haiku_task_id,
                         "extractions": [[e, s] for e, s in f.extractions], "status": reg.status(fid)})
        if fid in st["read_fids"] and reg.status(fid) != "admitted":
            drops.append({"form_id": fid, "sem_id": f.sem_id, "text": f.text, "origin": o["origin"],
                          "stage": "G-LEX", "status": reg.status(fid),
                          "reason": [f"{e}: {s}" for e, s in f.extractions]})

    # ---- merged counts (v1 frozen pools + redo2 supplement) against the G0 targets, never lowered
    c1 = v1_manifest()["counts"]
    short = []

    def target(name, want, got):
        if got < want:
            short.append({"item": name, "target": want, "admitted": got, "short_by": want - got})

    skin_reg = Counter(c1["skins_mode_t"]["by_register"]) + Counter(x["register"] for x in skins)
    for r, want in FZ.MODE_T_TARGET.items():
        target(f"Mode T skins {r}", want, skin_reg.get(r, 0))
    doc_reg = Counter(c1["documents_mode_f"]["by_register"]) + Counter(x["register"] for x in docs)
    for r, want in sorted(c1["documents_mode_f"]["planned_by_register"].items()):
        target(f"Mode F texts {r}", want, doc_reg.get(r, 0))
    target("attack lines (G0 section 4)", FZ.ATTACK_TARGET, c1["attacks"]["total"] + len(attacks))
    canon = Counter(c1["lexicon_forms"]["canonical_admitted"])
    para = Counter(c1["lexicon_forms"]["paraphrase_admitted"])
    for r in lex_rows:
        if r["status"] == "admitted" and r["origin"] == "canonical_r2":
            canon[r["sem_id"]] += 1
        if r["status"] == "admitted" and r["origin"] == "haiku_form_r2":
            para[r["sem_id"]] += 1
    for s in sorted(P.SEMS):
        target(f"canonical forms {s}", FZ.CANON_PER_SEM, canon.get(s, 0))
        target(f"Haiku paraphrases {s} (>=6 admitted)", FZ.PARAPHRASE_ADMIT, para.get(s, 0))
    w = {q: dict(c1["wordings"]["by_qform"][q]) for q in FZ.QFORMS}
    for x in wordings:
        w[x["qform"]]["held_out" if x["held_out"] else "training"] += 1
    for q in FZ.QFORMS:
        for side in ("training", "held_out"):
            target(f"wordings {side.replace('_', ' ')} {q}", FZ.WORDING_TARGET[side][q], w[q][side])
    target("packs asked (G0 section 4; not redone: S24 needs 32 + 4, kept 43 + 6)", FZ.PACK_ASKED,
           c1["packs"]["kept_total"])

    form_counts = Counter(f"{r['sem_id']} {r['origin']} {r['status']}" for r in lex_rows if r["kind"] != "question")
    counts = {"redo2": {"skins": dict(Counter(x["register"] for x in skins)),
                        "documents": dict(Counter(x["register"] for x in docs)), "attacks": len(attacks),
                        "wordings": dict(Counter(x["qform"] + (" held_out" if x["held_out"] else "")
                                                 for x in wordings)),
                        "forms": dict(sorted(form_counts.items()))},
        "merged": {"skins_by_register": dict(sorted(skin_reg.items())),
                   "documents_by_register": dict(sorted(doc_reg.items())),
                   "attacks": c1["attacks"]["total"] + len(attacks), "canonical_admitted": dict(sorted(canon.items())),
                   "paraphrase_admitted": dict(sorted(para.items())), "wordings": w}}
    summary = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED,
               "pieces_authored": len(st["pieces"]), "quarantine_by_stage": dict(Counter(d["stage"] for d in drops)),
               "g3h": {"texts_read": len(st["freeform"]), "passing": sum(1 for v in g3_rec.values() if v["ok"]),
                       "quarantined_registers": sorted(q_regs)},
               "counts": counts, "shortfalls": short, "n_shortfalls": len(short)}
    if not write:
        print(json.dumps(summary, ensure_ascii=False, indent=1, default=str))
        return 0
    out = {
        "lexicon_add.json": {"family": FAMILY, "version": VERSION, "pool": "lexicon (redo2 forms; v1 statuses "
                             "unchanged, checked)", "canonical_status_r2": list(CANON_STATUS_R2), "forms": lex_rows},
        "skins_add.json": {"family": FAMILY, "version": VERSION, "n": len(skins), "items": skins},
        "documents_add.json": {"family": FAMILY, "version": VERSION, "n": len(docs), "items": docs},
        "attacks_add.json": {"family": FAMILY, "version": VERSION, "n": len(attacks), "items": attacks},
        "wordings_add.json": {"family": FAMILY, "version": VERSION, "n": len(wordings), "items": wordings},
        "extraction_record.json": {"family": FAMILY, "version": VERSION, "lexicon_extractions": lex_record,
                                   "answer_sha256": dict(sorted(answer_shas.items()))},
        "g3h_record.json": {"family": FAMILY, "version": VERSION, "bar": FZ.G3H_BAR, "registers": rep["templates"],
                            "quarantined_registers": sorted(q_regs), "texts": g3_rec},
        "quarantine.json": {"family": FAMILY, "version": VERSION, "n": len(drops),
                            "by_stage": dict(Counter(d["stage"] for d in drops)), "items": drops},
    }
    SUPP.mkdir(parents=True, exist_ok=True)
    written = {}
    for name, obj in sorted(out.items()):
        path = SUPP / name
        if path.exists():
            os.chmod(path, 0o644)
        paths.write_json(path, obj)
        written[name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
    manifest = dict(summary, status="redo2 supplement, pre-G13-seed", pool_files=written,
                    merge_rule="pools = v1 pools/*.json + pools/redo2/*_add.json; lexicon = v1 lexicon.json (statuses "
                               "unchanged) + lexicon_add.json; Mode F: one kept text per brief",
                    not_run=["G13-seed (decontam on the pools, C2_DATA_SPEC 6.4 step 4)", "pilot of 1,000 rows",
                             "any row generation"])
    mpath = SUPP / "MANIFEST.json"
    if mpath.exists():
        os.chmod(mpath, 0o644)
    paths.write_json(mpath, manifest)
    for name in list(out) + ["MANIFEST.json"]:
        os.chmod(SUPP / name, 0o444)
    print(json.dumps({"written": sorted(list(out) + ["MANIFEST.json"]), "shortfalls": short}, indent=1))
    return 0


# ================================================================================================ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=("author", "extract", "admit"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if args.stage == "author":
        files, index = author_files()
        probs = check_author(files)
        if probs:
            print("\n".join(probs))
            return 1
        if args.write:
            paths.write_files(ROOT, files)
        print(json.dumps({"tasks": [(r["task"], r["task_id"], r["n_items"], r["outputs_expected"])
                                    for r in index["tasks"]],
                          "n_tasks": index["n_tasks"], "outputs_expected": index["outputs_expected"],
                          "written": bool(args.write)}, indent=1))
        return 0
    if args.stage == "extract":
        st = extract_state()
        files, index = extract_files(st)
        if args.write:
            paths.write_files(EX_ROOT, files)
        print(json.dumps({"pieces": len(st["pieces"]), "drops_by_stage": dict(Counter(d["stage"] for d in st["drops"])),
                          "lex_read_items": len(st["read_fids"]), "g3h_items": len(st["freeform"]),
                          "n_tasks": index["n_tasks"], "written": bool(args.write)}, indent=1))
        return 0
    return admit(args.write)


if __name__ == "__main__":
    raise SystemExit(main())
