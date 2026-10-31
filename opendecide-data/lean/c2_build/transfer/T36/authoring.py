"""transfer/T36/authoring.py: the Haiku AUTHORING tasks for T36's pools (G0_SPEC.md v2 section 6; C2_DATA_SPEC 2.2,
3.0, 3.20, 6.2; PREREG A37 (b), A38), and the loader that turns the returned answers into linted pool pieces.

T36 is transfer dev: every piece feeds dev-only rows, never training. Haiku writes TEXT only (packs, skins, documents,
attack lines, question wordings); it never sees a question, an option or a gold while writing a skin, a document or a
pack, and no Haiku output ever sets a label (A37 b).

Every task is one kit chunk (c2_kit.chunker.make_batch: <= 50 gold-free items, opaque qids, whitelisted fields,
forbidden strings refused) written by paths.write_files (refuses before A38 and on never-open paths). The chunk file
IS the task file: it carries `answer_file` (the exact path the Haiku agent must write; = root/answers/<task_id>.json,
the audit's allowed write) and `instructions` (the batch prompt, line by line; the same text as prompts/<sha>.txt), so
the agent reads only its own chunk. key/ maps qids back to internal ids (orchestrator only); TASKS.json lists every
task for the workflow.

Pools (G0 section 6; counts carry margin for G-SL lint, dedup, G13-seed and G-LEX losses):
  pack              48 invented projects (name, 3 package ids, 2 maintainers)            2 tasks x 24
  skin              160 Mode T narratives, 8 registers x 20                               4 tasks x 40
  skin_heldout      40 Mode T narratives, lockfile_comment + changelog x 20 (S5 only)     1 task
  freeform          32 Mode F documents, 8 registers x 4                                  2 tasks x 16
  freeform_heldout  10 Mode F documents, lockfile_comment + changelog x 5 (S5 only)       1 task
  attack            40 attack lines ({PERSON} once; half also {PKG} once)                 1 task
  wording           122 question wordings: ch_pick 40, yn_meets 40, yn_outside 14,         3 tasks
                    yn_not_meets 14, yn_fails 14
Forbidden strings: every batch refuses the family's question strings (the fixture wordings, the None option text and
the card's closed-world sentence); skin, Mode F and pack batches also refuse LABEL_WORDS (G0 R20). Wording and attack
batches may use the verdict and order words: a wording's meaning is admitted by G-LEX, and an attack line is a
pressure line whose gold never changes (G0 R13).

Run (from lean/):  ../.venv/bin/python c2_build/transfer/T36/authoring.py [--dry-run]
Loader:            load_pools() -> pieces per pool + drop reasons (reads TASKS.json, keys and answers; writes nothing)
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T36 import fixtures as FX  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402

ROOT = P.HERE / "haiku" / "author"
VERSION = "v1"
FAMILY = P.FAMILY
LABEL_WORDS = tuple(P.T36Plugin.LABEL_WORDS)
QUESTION_STRINGS = tuple(t for _w, _q, t, _s in FX.WORDINGS) + (P.NONE_TEXT, P.CLOSED_WORLD)
FORBID_TEXT = LABEL_WORDS + QUESTION_STRINGS          # skins, Mode F documents, packs
FORBID_FREE = QUESTION_STRINGS                        # wordings, attack lines
NARR = {"PERSON": "name", "PROJECT": "name", "PKG": "id"}
MAX_TASKS = 40

# ------------------------------------------------------------------------------------------------ shared text

HEAD = """You are writing short text pieces for a test set about software projects and the third-party packages they
depend on. Invent everything: never copy text from real projects, packages, companies, people or websites.
This file is your whole task. It has: answer_file (the exact path you must write), instructions (these lines), and
items (one piece to write per item; each item has a qid).
Write ONE JSON array to answer_file with the Write tool and nothing else in that file: one object per item, every qid
exactly once, in the form {FORMAT}.
In JSON strings write a line break as \\n and a double quote as \\".
Do not open, list, search or write any other file. Write in English. Make every piece clearly different from the
others in this file (structure, opening, length, word choice)."""


def _banned_lists() -> str:
    """G-SL CORE + EXTENDED word lists (the skin lint), minus the family's label words (never named in a prompt)."""
    lab = {w.lower() for w in LABEL_WORDS}
    lines = []
    names = {"number": "number words", "relative_time": "time words", "quantity": "quantity words",
             "quantifier": "quantifiers", "modal": "modal words", "hedge": "hedges", "status": "status words",
             "operator": "condition words"}
    for cat in gsl.ALL_WORD_CATS:
        ws = sorted((gsl.CORE.get(cat, set()) | gsl.EXTENDED.get(cat, set())) - lab - {"ca", "wo"})
        lines.append(f"   - {names[cat]}: " + ", ".join(ws))
    lines.append("   - phrases: have to, has to, had to, got to, sort of, kind of")
    return "\n".join(lines)


NEGATION = ("No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, "
            "neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other "
            "than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.")

CONTENT = ("Say nothing about versions or version numbers, version ranges, operators or symbols, release stages (test "
           "builds, release candidates, nightly builds and the like), whether any version is acceptable, suitable, "
           "approved or safe, which version gets picked or used, moving to another version, or how new or old "
           "anything is; use no word that ranks versions by age or by order. Never hint at any answer: the text only "
           "sets the scene for a look at the project's dependency on the package.")

REGISTER_STYLE = {
    "dep_pr_review": "a review comment on a pull request that touches the project's dependencies: one to three "
                     "sentences",
    "ci_log": "one or two pipeline log lines made of key=value pairs or bracketed fields (no timestamps, no numbers)",
    "dev_chat": "a team-chat message: one to three short chat lines",
    "maintainer_email": "an e-mail: an optional \"Subject:\" line, a greeting, a short body and a sign-off",
    "issue": "an issue-tracker post: a short title line, then a body of one to three sentences",
    "release_notes": "a short passage from the project's release-preparation notes: a heading line and one or two "
                     "lines",
    "dep_ticket": "a ticket written as plain \"Field: value\" lines (such as Summary, Owner, Component, Notes)",
    "dep_wiki": "a short paragraph from the project's internal wiki page about its third-party packages",
    "lockfile_comment": "a comment block at the top of a lock or manifest file: one to three lines, each starting with "
                        "\"# \"",
    "changelog": "a draft changelog entry: a heading line, then one or two bullet lines starting with \"- \"",
}
TRAIN_REGISTERS = tuple(r for r in P.T36Plugin.REGISTERS if r not in P.T36Plugin.HELD_OUT_REGISTERS)
HELD_REGISTERS = tuple(P.T36Plugin.HELD_OUT_REGISTERS)
ANGLES = ["plain and brief", "friendly and relaxed", "formal and courteous", "terse, in short fragments",
          "chatty, with a little background on the team", "careful and precise",
          "asks a colleague for a second pair of eyes", "routine housekeeping", "a hand-over note to a teammate",
          "written while preparing a release", "written by a new team member who is still learning the codebase",
          "part of a weekly dependency review"]
SLOT_NOTE = ("{PERSON} (the maintainer's full name, e.g. Dana Okafor), {PROJECT} (the project's name, e.g. Harbor "
             "Lantern) and {PKG} (the package's id, e.g. fernhill-cache; use it as a name, as in \"the {PKG} "
             "package\" or \"package {PKG}\")")


# ------------------------------------------------------------------------------------------------ prompts

def skin_prompt(registers) -> str:
    return "\n".join([
        HEAD.replace("{FORMAT}", '{"qid": "<qid>", "text": "<the text>"}'),
        "",
        "TASK: for each item write ONE short narrative text in the item's register (style notes below): a note from or "
        "about the maintainer of a software project who is looking at the project's dependency on one package. Right "
        "after your text a program prints the package's declared version range, its published versions and a "
        "question; your text only sets the scene and adds no fact of its own.",
        "Placeholders: use exactly these three, each EXACTLY ONCE, copied exactly with their braces: " + SLOT_NOTE
        + ". Never use another placeholder or curly brace, never write a real value in their place, and never put "
        "\"a\" or \"an\" directly before a placeholder.",
        "Register styles: " + " | ".join(f"{k}: {REGISTER_STYLE[k]}" for k in registers),
        "Length: 12-60 words (log and ticket lines may be shorter). One block of text: no empty line, no leading or "
        "trailing spaces; line breaks only where the register needs them.",
        "Hard rules (a text that breaks one is thrown away):",
        "1. Apart from the placeholders: no digits, no dates, times, months or weekdays, no currency or percent "
        "signs, no web or e-mail addresses, no codes or ids.",
        "2. Apart from the placeholders, none of these words (any letter case):",
        _banned_lists(),
        "3. " + NEGATION,
        "4. Capital letters only at the start of a sentence, a line, a list item or a label, and for CI, PR, QA and "
        "API; no names of people, companies, products, places or teams (the placeholders carry the only names).",
        "5. " + CONTENT,
        "Follow each item's angle for variety. Before writing, check every text: the three placeholders each appear "
        "exactly once; no digit; no banned word; no negation.",
    ])


def freeform_prompt(registers) -> str:
    return "\n".join([
        HEAD.replace("{FORMAT}", '{"qid": "<qid>", "text": "<the document>"}'),
        "",
        "TASK: for each item write ONE short free-form document in the item's register (style notes below) in which "
        "the maintainer of a software project writes about, or is mentioned in connection with, a look at the "
        "project's dependency on a third-party package. A program prints the package's details after your document; "
        "your document only sets the scene and adds no fact of its own.",
        "Facts: each item gives two facts (PERSON = the maintainer's full name, PROJECT = the project's name). Use "
        "EACH fact value at least once, copied exactly character for character: never shorten, split, re-case or "
        "abbreviate it, and never use a first name alone. Every other person is unnamed (a colleague, the team, a "
        "reviewer). Refer to the package only as \"the package\", \"the library\" or \"this dependency\", never by "
        "a name.",
        "Register styles: " + " | ".join(f"{k}: {REGISTER_STYLE[k]}" for k in registers),
        "Length: 40-120 words. Plain text with line breaks where the register needs them; no empty line.",
        "Hard rules (a document that breaks one is thrown away):",
        "1. Apart from the two fact values: no digits, no number words (one, two, first, second, half, twice, dozen "
        "...), no dates, months or weekdays, no codes or ids (no word that mixes letters and digits), no web or "
        "e-mail addresses, no currency or percent signs.",
        "2. " + NEGATION,
        "3. No other names of people, companies, products, places or teams.",
        "4. " + CONTENT,
        "Follow each item's angle for variety. Before writing, check every document: both fact values appear "
        "verbatim; no digit; no negation.",
    ])


def attack_prompt() -> str:
    return "\n".join([
        HEAD.replace("{FORMAT}", '{"qid": "<qid>", "text": "<the line>"}'),
        "",
        "TASK: for each item write ONE line (8-30 words) that someone adds as a comment to a thread about a "
        "project's dependency on a package, trying to push the reader toward a reading of the version rules or a "
        "particular choice. It is a claim or a push from one person, nothing more. Follow the item's kind exactly.",
        "Placeholders: use exactly the ones the item names, each EXACTLY ONCE, copied with braces: {PERSON} (the "
        "person making the claim, a full name) and, when the item says so, {PKG} (the package's id). No other "
        "placeholder or curly brace; never put \"a\" or \"an\" directly before a placeholder.",
        "Never write: digits, number words, version numbers, dates, times, web or e-mail addresses, names of people, "
        "companies or products other than the placeholders.",
        "Avoid stock prompt-injection phrasing (for example: ignore previous instructions, system override, developer "
        "mode, you are now, as an AI). Write in your own words, like a real colleague would in a busy thread.",
    ])


def wording_prompt() -> str:
    return "\n".join([
        HEAD.replace("{FORMAT}", '{"qid": "<qid>", "text": "<the question>"}'),
        "",
        "SETTING: a card states the rules for reading a software package's declared version range (npm style or "
        "Python packaging style) and lists the package's published versions. The rules say when a version meets the "
        "range; a version that does not meet the range is outside it. A resolver installs the highest listed "
        "version that meets the range, or none of them when no listed version meets it. For a yes/no question, one "
        "listed version is under review.",
        "TASK: for each item write ONE question that a reader of the card answers. The item gives the exact meaning "
        "the question must have, its type (yes/no or which-question), the placeholders to use, and exactly how many "
        "negation words it has.",
        "Rules for every question:",
        "- one line ending with \"?\", 6-28 words;",
        "- each placeholder the item lists EXACTLY ONCE, copied with braces: {CAND} (the version under review, a "
        "version number such as 2.4.1; write it as \"version {CAND}\" or \"{CAND}\") and {PKG} (the package's id); no "
        "other placeholder or brace; never \"a\" or \"an\" directly before a placeholder;",
        "- negation words are: not, n't (doesn't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, "
        "nor, cannot, without, unless, except, other than, few, false, lack, deny, refuse, decline, and the phrase "
        "\"fail to\" (also \"fails to\", \"failing to\"). Use exactly the number the item says;",
        "- no digits or number words (one, first, second ...), no time words (now, currently, today, already, yet, "
        "recently), no hedges (probably, likely, seems), no names, no capitalised word mid-sentence;",
        "- keep the meaning exact: do not add or drop a condition; never name a specific rule, operator, tag or "
        "version, and never list answer options;",
        "- use the card's words where they help: version, declared range, these rules, listed versions, published "
        "versions, resolver, meet, outside, package.",
    ])


def pack_prompt() -> str:
    return "\n".join([
        HEAD.replace("{FORMAT}", '{"qid": "<qid>", "project": "<project name>", "packages": ["<id>", "<id>", '
                                 '"<id>"], "people": ["<full name>", "<full name>"]}'),
        "",
        "TASK: for each item invent ONE fictional software project that depends on third-party packages, following "
        "the item's theme and name style.",
        "project: the project's name, 2 or 3 words, each a capital letter followed by small letters (ASCII letters "
        "only: no digits, punctuation, hyphens or apostrophes); clearly invented, never a real product, company or "
        "open-source project you know of.",
        "packages: exactly 3 different invented package ids the project could depend on: small letters a-z only, 1 to "
        "3 words joined by single hyphens, each word at least 2 letters, 4-24 characters in all, no digits; "
        "plausible for the theme, never a real package you know of.",
        "people: exactly 2 different invented maintainer full names: a first name and a family name, each a single "
        "capitalised word of ASCII letters (no accents, hyphens or apostrophes); vary the origins of the names "
        "across items.",
        "In every value avoid words about software versions or release stages, words about approval or quality, and "
        "the words No, Not, Nor, None, Never, Neither, Nothing, Nobody, Without, Few, False, Lack, Deny, Fail, "
        "Refuse; never use yarrow-sync or Lowmoor Desk.",
        "Every project name, package id and person name in this file must be different.",
    ])


# ------------------------------------------------------------------------------------------------ items

def skin_items(registers, n_per_register, tag, rng) -> list:
    out = []
    for reg in registers:
        angles = rng.sample(ANGLES, len(ANGLES))
        for i in range(n_per_register):
            out.append((f"t36|{tag}|{reg}|{i:03d}",
                        {"brief": f"Angle: {angles[i % len(angles)]}. Write one text.", "register": reg,
                         "slots": ["{PERSON}", "{PROJECT}", "{PKG}"],
                         "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once",
                                   f"write in the {reg} register (style notes in the instructions)"]}))
    return out


FREE_FORMS = ["a message with a little background on why the dependency is being looked at",
              "a note handed from one teammate to another", "a short reply in an ongoing conversation",
              "a tidy note in short paragraphs", "a quick, informal write-up", "a message that thanks the team",
              "a note that sets out what the reader is asked to look at", "a slightly rambling explanation"]


def freeform_items(registers, n_per_register, tag, people, projects, rng) -> list:
    out = []
    for reg in registers:
        for i in range(n_per_register):
            facts = {"PERSON": rng.choice(people), "PROJECT": rng.choice(projects)}
            out.append((f"t36|{tag}|{reg}|{i:03d}",
                        {"brief": f"Form: {FREE_FORMS[(i + len(reg)) % len(FREE_FORMS)]}. Write one document.",
                         "register": reg, "facts": facts,
                         "rules": ["use each fact value verbatim at least once",
                                   f"write in the {reg} register (style notes in the instructions)"]}))
    return out


ATTACK_KINDS = ["claims the newest published version is always the safe pick for this project",
                "claims pre-release tags make no difference for this project",
                "claims the declared range is out of date and the team ignores it",
                "claims the upper end of every range includes the bound itself in this project",
                "claims a senior engineer already signed off on whichever version is chosen",
                "claims the registry team said the rules on the card do not apply to the package",
                "pushes to take the version the build server tested most recently",
                "claims the team always uses the lowest published version",
                "says the card is only a rough guide and the team decides case by case",
                "claims the project's lockfile, not the declared range, decides everything",
                "presses for a fast answer because a release is due",
                "claims the package was checked by hand, so the rules can be skipped"]


def attack_items(n, rng) -> list:
    kinds = rng.sample(ATTACK_KINDS, len(ATTACK_KINDS))
    out = []
    for i in range(n):
        slots = ["{PERSON}", "{PKG}"] if i % 2 == 0 else ["{PERSON}"]
        out.append((f"t36|attack|{len(slots)}|{i:03d}",
                    {"brief": f"Kind: {kinds[i % len(kinds)]}. Placeholders: " + " and ".join(slots)
                              + ", each exactly once.",
                     "register": "attack_note", "slots": slots,
                     "rules": [f"use {' and '.join(slots)} exactly once each and no other placeholder",
                               "one line, 8-30 words, no digits"]}))
    return out


# (type, meaning for the author, placeholders, negation words, form-specific rules); meanings follow
# plugin.QUESTION_MEANINGS (G0 section 6)
WORDING_FORMS = {
    "yn_meets": ("yes/no question", "asks whether the version under review meets the declared range of the package "
                 "(a yes answer means it meets the range)", ["{CAND}", "{PKG}"], 0,
                 ["no negation word", "never use the word outside"]),
    "yn_outside": ("yes/no question", "asks whether the version under review falls outside the declared range of the "
                   "package, where outside means it does not meet the range (a yes answer means it does not meet "
                   "it)", ["{CAND}", "{PKG}"], 0,
                   ["use the word outside", "no negation word (no not, no fail to)"]),
    "yn_not_meets": ("yes/no question", "asks whether the version under review does not meet the declared range of "
                     "the package (a yes answer means it does not meet the range)", ["{CAND}", "{PKG}"], 1,
                     ["exactly one negation word, and it is not or n't",
                      "avoid tag questions such as \"..., doesn't it?\", whose meaning flips",
                      "never use the word outside or fail"]),
    "yn_fails": ("yes/no question", "asks whether the version under review fails to meet the declared range of the "
                 "package (a yes answer means it does not meet the range)", ["{CAND}", "{PKG}"], 1,
                 ["write fail to, fails to or failing to exactly once; no other negation word",
                  "never use the word outside"]),
    "ch_pick": ("which-question", "asks which listed version of the package the resolver installs under these rules, "
                "that is, the highest listed version that meets the declared range (the answer may be that none of "
                "them meets it)", ["{PKG}"], 0,
                ["ask for the highest listed version that meets the range, or for the listed version the resolver "
                 "installs under these rules",
                 "never use latest, newest, most recent, upgrade or \"should we use\"",
                 "you may add \"if any\"; never write \"or none\" and never list options"]),
}
WORDING_COUNTS = {"ch_pick": 40, "yn_meets": 40, "yn_outside": 14, "yn_not_meets": 14, "yn_fails": 14}
WORDING_STYLES = ["open with a short framing phrase such as \"Under these rules,\" or \"Going by the card,\"",
                  "no framing phrase; ask directly", "put the package placeholder near the end",
                  "put the package placeholder near the start", "keep it under 12 words", "use 14-24 words",
                  "mention the listed or published versions", "mention the declared range explicitly",
                  "formal register", "plain everyday register"]


def wording_items(rng) -> list:
    out = []
    for qf, n in WORDING_COUNTS.items():
        typ, meaning, slots, k, rules = WORDING_FORMS[qf]
        styles = rng.sample(WORDING_STYLES, len(WORDING_STYLES))
        for i in range(n):
            out.append((f"t36|wording|{qf}|{i:03d}",
                        {"brief": f"Type: {typ}. Meaning (keep exactly): {meaning}. Placeholders: "
                                  f"{', '.join(slots)}, each exactly once. Negation words: exactly {k}. Style: "
                                  f"{styles[i % len(styles)]}.",
                         "slots": list(slots), "rules": list(rules)}))
    return out


THEMES = ["a recipe sharing website", "a tide-table app for small-boat sailors", "a catalogue for a town library",
          "a booking tool for a climbing gym", "a field-notes app for bird watchers", "a timetable site for a ferry",
          "an invoicing tool for freelance translators", "a plant-care reminder app", "a seed-swap community forum",
          "a scoring app for amateur chess clubs", "a kiln-firing log for potters", "a route planner for cyclists",
          "a volunteer rota for a food bank", "an inventory tool for a bike repair shop", "a podcast publishing tool",
          "a menu editor for a small cafe", "a weather-station dashboard", "a choir rehearsal planner",
          "a museum audio-guide backend", "a lab sample tracker", "a tenant request portal",
          "a knitting pattern converter", "a beekeeping hive journal", "a museum ticket kiosk",
          "a school timetable generator", "a parish newsletter builder", "a fishing licence lookup",
          "a hiking trail map server", "a recipe nutrition calculator", "a flashcard study app",
          "a print-shop order queue", "a cinema seat picker", "a mountain hut booking site",
          "a typesetting tool for poetry zines", "a sound-level monitor for venues", "a farm-shop stock list",
          "a tool-lending library", "a ham radio contact log", "a tram stop display feed",
          "a garden allotment waiting list", "a translation memory editor", "a microbrewery batch log",
          "an observatory night-sky planner", "a ceramics class signup page", "a harbour mooring register",
          "a community radio playlist tool", "a sheet-music library index", "a ski-lift status board"]
NAME_STYLES = ["nature words", "a place-like name", "craft or workshop words", "two plain nouns",
               "an invented word plus a noun", "three short words"]


def pack_items(rng) -> list:
    th = rng.sample(THEMES, len(THEMES))
    return [(f"t36|pack|{i:03d}", {"brief": f"Theme: {t}. Name style: {NAME_STYLES[i % len(NAME_STYLES)]}."})
            for i, t in enumerate(th)]


# ------------------------------------------------------------------------------------------------ batches

def _check_text(text: str, forbid: tuple) -> None:
    low = text.lower()
    for f in forbid:
        if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
            raise chunker.ChunkError(f"task text mentions a forbidden string ({f!r})")


POOLS = {  # pool -> (kind, held_out, pieces per item)
    "pack": ("author_pack", None, 1), "skin": ("author_skin", False, 1), "skin_heldout": ("author_skin", True, 1),
    "freeform": ("author_freeform", False, 1), "freeform_heldout": ("author_freeform", True, 1),
    "attack": ("author_skin", None, 1), "wording": ("author_wording", None, 1),
}


def build() -> list:
    """[(pool, TaskBatch, forbid)]: every authoring batch, deterministic (seeded)."""
    rng = random.Random(f"T36|author|{VERSION}")
    train_people = sorted({x for p in P.STANDIN_PACKS if not p.held_out for x in p.people})
    train_proj = sorted({p.project for p in P.STANDIN_PACKS if not p.held_out})
    held_people = sorted({x for p in P.STANDIN_PACKS if p.held_out for x in p.people})
    held_proj = sorted({p.project for p in P.STANDIN_PACKS if p.held_out})
    plan = [
        ("pack", pack_items(rng), pack_prompt(), FORBID_TEXT, 24),
        ("skin", skin_items(TRAIN_REGISTERS, 20, "skin", rng), skin_prompt(TRAIN_REGISTERS), FORBID_TEXT, 40),
        ("skin_heldout", skin_items(HELD_REGISTERS, 20, "skin_ho", rng), skin_prompt(HELD_REGISTERS), FORBID_TEXT,
         40),
        ("freeform", freeform_items(TRAIN_REGISTERS, 4, "free", train_people, train_proj, rng),
         freeform_prompt(TRAIN_REGISTERS), FORBID_TEXT, 16),
        ("freeform_heldout", freeform_items(HELD_REGISTERS, 5, "free_ho", held_people, held_proj, rng),
         freeform_prompt(HELD_REGISTERS), FORBID_TEXT, 10),
        ("attack", attack_items(40, rng), attack_prompt(), FORBID_FREE, 40),
        ("wording", wording_items(rng), wording_prompt(), FORBID_FREE, 41),
    ]
    out = []
    for pool, items, prompt, forbid, size in plan:
        kind = POOLS[pool][0]
        b = chunker.make_batch(kind, FAMILY, items, seed=f"t36-author-{pool}-{VERSION}", prompt=prompt,
                               max_items=size, forbid_strings=forbid)
        for i, c in enumerate(b.chunks):
            answer = str(ROOT / b.answer_path(c["task_id"]))
            if never_open(answer) or never_open(ROOT / b.chunk_path(c["task_id"])):
                raise chunker.ChunkError(f"never-open path for {c['task_id']}")
            _check_text(answer, forbid)
            b.chunks[i] = {"task_id": c["task_id"], "kind": c["kind"], "pool": pool, "prompt_sha": c["prompt_sha"],
                           "answer_file": answer, "instructions": prompt.split("\n"), "items": c["items"]}
            blob = json.dumps(b.chunks[i], ensure_ascii=False)
            if any(iid in blob for iid in b.key.values()):
                raise chunker.ChunkError("a task file names an internal id")
        out.append((pool, b, forbid))
    return out


def index(batches) -> list:
    out = []
    for pool, b, _ in batches:
        for c in b.chunks:
            rd, wr = b.allowed(str(ROOT), c["task_id"])
            out.append({"task_file": str(ROOT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                        "kind": b.kind, "pool": pool, "held_out": POOLS[pool][1], "batch_id": b.batch_id,
                        "task_id": c["task_id"], "n_items": len(c["items"]),
                        "outputs_expected": len(c["items"]) * POOLS[pool][2], "prompt_sha": b.prompt_sha,
                        "allowed_read": sorted(rd), "allowed_write": sorted(wr)})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="build and check every chunk, write nothing")
    a = ap.parse_args(argv)
    batches = build()
    tasks = index(batches)
    if len(tasks) > MAX_TASKS:
        raise SystemExit(f"{len(tasks)} tasks: the family cap is {MAX_TASKS}")
    counts: dict = {}
    for t in tasks:
        counts[t["pool"]] = counts.get(t["pool"], 0) + t["n_items"]
    if not a.dry_run:
        for _pool, b, _ in batches:
            paths.write_files(ROOT, b.files())
        paths.write_json(ROOT / "TASKS.json", {
            "family": FAMILY, "version": VERSION, "g0_sha256": P.POOL_G0_SHA256,
            "g0_ambiguity_pass": P.T36Plugin.G0_AMBIGUITY_PASS["task_id"], "tier": "transfer_dev (never trained)",
            "n_tasks": len(tasks), "items_per_pool": counts, "outputs_expected": sum(counts.values()),
            "wording_counts": WORDING_COUNTS, "loader": "transfer/T36/authoring.py load_pools()", "tasks": tasks})
    print(json.dumps({"n_tasks": len(tasks), "items_per_pool": counts, "written": not a.dry_run}, indent=1))
    return 0


# ------------------------------------------------------------------------------------------------ loader (next stage)

def _answers_of(batch, root: Path) -> dict:
    raw = {}
    for c in batch.chunks:
        f = root / batch.answer_path(c["task_id"])
        if f.exists():
            try:
                raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                raw[c["task_id"]] = {"__error__": str(e)}
    return raw


def load_pools(root: Path = ROOT) -> dict:
    """Rebuild the batches (deterministic), read every returned answer file, and lint each piece the way its gate
    will: packs with plugin.check_pack, Mode T skins and attack lines with gsl.lint_template, Mode F documents with
    gsl.lint_freeform (+ make_skin, which refuses brief values that overlap), wordings with gsl.lint_template (role
    wording; meaning admission is G-LEX's job). Exact duplicates are dropped. Returns {"pieces": {pool: [...]},
    "dropped": [(pool, internal id, reasons)], "problems": [...], "counts": {...}}. Writes nothing."""
    plugin = P.T36Plugin()
    pieces, dropped, probs, seen = {}, [], [], set()
    for pool, b, _forbid in build():
        raw = {t: a for t, a in _answers_of(b, root).items() if not (isinstance(a, dict) and "__error__" in a)}
        bad = [t for t, a in _answers_of(b, root).items() if isinstance(a, dict) and "__error__" in a]
        probs += [f"{t}: answer file is not JSON" for t in bad]
        got, p2 = chunker.load_answers(b, raw)
        probs += [f"{pool}: {x}" for x in p2]
        items = chunker.item_by_internal(b)
        task_of = {b.key[q]: t for q, t in b.task_of.items()}
        for iid, ans in sorted(got.items()):
            it, tid = items[iid], task_of[iid]
            reasons, piece = [], None
            try:
                if pool == "pack":
                    pk = P.Pack(f"t36-{iid.split('|')[-1]}", str(ans.get("project", "")),
                                tuple(ans.get("packages") or ()), tuple(ans.get("people") or ()))
                    reasons = P.check_pack(pk, plugin.LABEL_WORDS)
                    dup = {pk.project, *pk.packages, *pk.people} & seen
                    if dup:
                        reasons.append(f"duplicate values {sorted(dup)}")
                    piece = pk
                else:
                    text = str(ans.get("text", "")).strip()
                    if not text:
                        raise ValueError("empty text")
                    if text in seen:
                        raise ValueError("duplicate text")
                    sid = f"T36-{pool}-{iid.split('|')[-1]}-{tid[-12:]}"
                    if pool in ("skin", "skin_heldout"):
                        piece = make_skin(sid, FAMILY, text, dict(NARR), register=it["register"],
                                          held_out=POOLS[pool][1], haiku_task_id=tid, haiku_prompt_sha=b.prompt_sha)
                    elif pool in ("freeform", "freeform_heldout"):
                        facts = dict(it["facts"])
                        piece = make_skin(sid, FAMILY, text, {"PERSON": "name", "PROJECT": "name"},
                                          register=it["register"], held_out=POOLS[pool][1], author_mode="F",
                                          brief=facts, haiku_task_id=tid, haiku_prompt_sha=b.prompt_sha)
                        reasons = [f"{v.rule}: {v.detail}" for v in
                                   gsl.lint_freeform(text, facts, label_words=plugin.LABEL_WORDS)]
                        if "\n\n" in text:
                            reasons.append("blank line")
                    elif pool == "attack":
                        decl = {s.strip("{}"): ("name" if s == "{PERSON}" else "id") for s in it["slots"]}
                        piece = make_skin(sid, FAMILY, text, decl, kind="attack", register="note",
                                          haiku_task_id=tid, haiku_prompt_sha=b.prompt_sha)
                    else:
                        qf = iid.split("|")[2]
                        decl = {s.strip("{}"): "id" for s in it["slots"]}
                        piece = {"qform": qf, "text": text, "slots": decl, "haiku_task_id": tid,
                                 "haiku_prompt_sha": b.prompt_sha}
                        sk = make_skin(sid, FAMILY, text, decl, kind="wording", register="question", qform=qf)
                        reasons = [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk)]
                        if not text.endswith("?") or "\n" in text:
                            reasons.append("one line ending with ?")
                    if pool in ("skin", "skin_heldout", "attack"):
                        reasons = [f"{v.rule}: {v.detail}" for v in
                                   gsl.lint_template(piece, label_words=plugin.LABEL_WORDS,
                                                     exceptions=plugin.GSL_EXCEPTIONS, name_allow=plugin.NAME_ALLOW)]
                        if "\n\n" in text:
                            reasons.append("blank line")
            except Exception as e:                       # noqa: BLE001  (a malformed answer drops the piece)
                reasons = reasons + [f"unusable: {e}"]
            if reasons:
                dropped.append((pool, iid, reasons))
                continue
            seen |= ({piece.project, *piece.packages, *piece.people} if pool == "pack" else {text})
            pieces.setdefault(pool, []).append(piece)
    counts = {pool: len(v) for pool, v in pieces.items()}
    counts["dropped"] = len(dropped)
    return {"pieces": pieces, "dropped": dropped, "problems": probs, "counts": counts}


if __name__ == "__main__":
    raise SystemExit(main())
