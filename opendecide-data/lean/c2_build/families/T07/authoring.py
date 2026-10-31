"""c2_build/families/T07/authoring.py: the T07 Haiku AUTHORING tasks and the closed program checks their pieces must
pass (G0_SPEC.md section 4; C2_DATA_SPEC 3.0, 3.16; README "Haiku task flow"). After A38 only: every write goes through
paths.write_files.

One make_batch per task (one chunk each, <= 50 items, opaque qids, gold-free). Every brief and prompt passes the
family's FORBID strings (label words, option texts, the stand-in question strings): Haiku never sees a question of a
row, an option or a gold, and writes reusable pieces only.

  tasks                                kind              items x outputs       pool (G0 section 4)
  pack-a, pack-b                       author_pack       30 x 1 pack           store contexts (52 training, 8 held out)
  skin-<register> (9 training)         author_skin        8 x 5 texts          Mode T ad copy, {STORE} once
  skin-loyalty_newsletter, -shelf_tag  author_skin        6 x 4 texts          Mode T, held out (sampler S5)
  free-a .. free-d                     author_freeform   38 x 1 text           Mode F over the 100 likeliest sequences
  free-held                            author_freeform   30 x 1 text           Mode F voice_promo, held out
  lex-other, lex-temporal, lex-comp    author_lexicon    6-10 x 6 forms        condition sentences (12 per sem)
  word-yes, word-neg, word-failing,    author_wording    4-12 x 4-8            question wordings (training)
  word-offers
  word-held                            author_wording     7 x 6 wordings       question wordings (held out)
  attack                               author_skin       10 x 6 lines          customer notes (attack kind)

Each task file (haiku/author/tasks/<task_id>.md) is self-contained: the exact answer path, the prompt and the items.
The agent reads only that file and writes only its answer file (audit.audit with TASKS.json's allowed paths). The
opaque-id key (key/) and the plan (plan/: internal id -> register, slots, Mode F brief values) stay with the
orchestrator. lint_* below are the closed checks of G0 section 4 (run with G-SL at the lint stage); collect() loads
the answers and lints every piece; build_registry() makes the G-LEX registry (canonical + Haiku forms, wordings).

  ../.venv/bin/python -m families.T07.authoring          (from lean/c2_build; writes haiku/author/, after A38 only)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import itertools
import json
import math
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T07 import fixtures as FX  # noqa: E402
from families.T07 import plugin as P  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

FAMILY = "T07"
ROOT = HERE / "haiku" / "author"
AMB_ROOT = HERE / "haiku" / "ambiguity"
VERSION = "v1"
MAX_TASKS = 40
PLAN_FILE = "plan/T07-author-plan.json"

OPTION_TEXTS = tuple(P.DIM_TEXT.values()) + (P.NONE_TEXT, P.OFFER_BOTH, P.OFFER_NEITHER)
QUESTION_STRINGS = tuple(text for _wid, _qf, text, _held in FX.WORDINGS)
FORBID = tuple(P.T07Plugin.LABEL_WORDS) + OPTION_TEXTS + QUESTION_STRINGS
WORD_RE = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)*")


def _bad(word: str, forbid: tuple = FORBID) -> bool:
    return any(re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", word.lower()) for f in forbid)


def _words(text: str) -> list:
    return [w.lower() for w in WORD_RE.findall(text)]


# ------------------------------------------------------------------------------------------------ closed word lists
# G0 section 4 (H29, H30): the Mode T / Mode F-body / attack bans beyond the kit's G-SL lists. Closed: a word that is
# on no list is allowed.
CONDITION_WORDS = frozenset("""only every free freely valid validity member members membership exclude excludes
excluded excluding exclusion exclusions exclusive exclusively minimum maximum over above below under before after
until till through ends ending expire expires expiry deadline limited limit while selected select restriction
restrictions restricted condition conditions term terms apply applies applied detail details fine print footnote
footnotes asterisk qualifying""".split())
DIMENSION_WORDS = frozenset("""delivery deliveries deliver delivers delivered ship ships shipped shipping shipment
shipments region regions area areas zone zones postcode address category categories status price prices priced pricing
clearance sale sales discount discounts discounted coupon coupons level levels tier tiers rank ranks subtotal spend
spending total totals amount amounts date dates day days week weeks month months year years season seasons seasonal
holiday holidays spring summer autumn fall winter hour hours minute minutes time""".split())
_PROMISE_STOP = {"on", "every", "order", "purchase", "we", "any", "a", "the", "at", "for", "with", "everything", "sell",
                 "checkout"}
PROMISE_WORDS = frozenset({w for t in (P.HEADLINES, P.BENEFITS) for v in t.values() for s in v for w in _words(s)
                           if w not in _PROMISE_STOP} | {"return", "rewards", "point", "assemble", "assembled", "wrap",
                                                         "wrapped", "install", "installed", "matching", "matched",
                                                         "gifts", "warranties", "appliances"})
SET_TABLES = (P.REGIONS, P.CATEGORIES, P.STATUSES, P.TIERS)


def surface_words(tables=SET_TABLES) -> frozenset:
    """Every word of every closed-set surface (dimension values), lower-case; a hyphenated surface stays whole."""
    out = set()
    for t in tables:
        for v in t.values():
            for s in v:
                out |= set(_words(s))
    return frozenset(out)


SURFACE_WORDS = surface_words()
T07_BANS = CONDITION_WORDS | DIMENSION_WORDS | PROMISE_WORDS
ATTACK_BANS = frozenset("""ignore ignored instruction instructions system assistant prompt override overrides answer
answers model correct""".split()) | DIMENSION_WORDS | PROMISE_WORDS
NEGATION_CUES = ("not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, "
                 "cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, "
                 "free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out")
FORM_BANS = frozenset("""unless except excepting either otherwise but if when whenever while until till through thru
starting beginning ends expires within between total discount discounts coupon coupons tax taxes billing billed""".split())
DIM_MARKERS = {"region": {"delivery", "deliveries", "deliver", "delivered", "ship", "ships", "shipped", "shipping",
                          "shipment", "shipments"},
               "category": {"category", "categories"},
               "tier": {"member", "members", "membership", "level", "levels", "tier", "tiers"},
               "spend": {"order", "orders", "subtotal", "spend", "spending", "purchase", "purchases", "basket"},
               "date": {"order", "orders", "placed", "purchase", "purchases", "bought", "buy"}}


def _gsl_lists(forbid: tuple = FORBID) -> str:
    cats = ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator")
    lines = []
    for c in cats:
        words = sorted(gsl.CORE.get(c, set()) | gsl.EXTENDED.get(c, set()))
        words = [w for w in words if not _bad(w, forbid) and w not in ("ca", "wo")]
        lines.append(f"- {c.replace('_', ' ')}: " + ", ".join(words))
    lines.append("- phrases: have to, has to, had to, got to, sort of, kind of")
    return "\n".join(lines)


def _t07_list(words) -> str:
    return ", ".join(sorted(w for w in words if not _bad(w)))


# ------------------------------------------------------------------------------------------------ program checks
def _neg(text: str):
    return negcount.count(text)


def lint_mode_t(text: str, *, register: str = "web_banner", escape: str = "text", kind: str = "skin",
                extra: frozenset = frozenset()) -> list:
    """Closed checks for a Mode T skin (or a Mode F body with the store as {STORE}): G-SL lint_template + T07 bans."""
    probs = []
    try:
        sk = K.make_skin("lint", FAMILY, text, {"STORE": "name"}, kind=kind, register=register, escape=escape)
        probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
            sk, label_words=P.T07Plugin.LABEL_WORDS, exceptions=P.T07Plugin.GSL_EXCEPTIONS,
            name_allow=P.T07Plugin.NAME_ALLOW)]
    except Exception as e:  # noqa: BLE001  (a malformed template is a lint failure)
        return [f"template: {type(e).__name__}: {e}"]
    lit = K.PH_RE.sub(" ", text)
    words = set(_words(lit))
    bad = sorted(words & (T07_BANS | SURFACE_WORDS | extra))
    if bad:
        probs.append(f"T07 ban: {bad}")
    if re.search(r"\b(?:a|an|the)\s+\{STORE\}", text, re.I):
        probs.append("article before {STORE}")
    if "*" in text or "†" in text:
        probs.append("footnote symbol in ad copy")
    if "\n\n" in text:
        probs.append("empty line")
    n = len(_words(lit))
    lo, hi = (2, 20) if register == "shelf_tag" else (8, 70)
    if not lo <= n <= hi:
        probs.append(f"{n} words (want {lo}-{hi})")
    return probs


def lint_mode_f(text: str, plan: dict, extra: frozenset = frozenset()) -> list:
    """Closed checks for a Mode F text against its brief (plan): the fine-print run verbatim, exactly once, at the end
    and the only `*`; the store name exactly once, in the body; G-SL lint_freeform over the whole text; the Mode T
    checks over the body."""
    probs = []
    run, store = plan["run"], plan["brief"]["STORE"]
    if text.count(run) != 1:
        probs.append("fine-print run not exactly once verbatim")
        return probs
    if text.count("*") != 1:
        probs.append("more than one *")
    body, tail = text.split(run)
    if tail.strip():
        probs.append("text after the fine-print run")
    if body.count(store) != 1 or store in run:
        probs.append("store name not exactly once in the body")
        return probs
    probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_freeform(
        text, dict(plan["brief"]), label_words=P.T07Plugin.LABEL_WORDS)]
    probs += [f"body: {p}" for p in lint_mode_t(body.rstrip().replace(store, "{STORE}"), register="email_promo",
                                                 extra=extra)
              if not p.startswith(("empty line", "footnote symbol")) and "words (want" not in p]
    if "\n\n" in text:
        probs.append("empty line")
    n = len(_words(body.replace(store, " ")))
    lo, hi = (10, 35) if plan["register"] == "sms" else (20, 70)
    if not lo <= n <= hi:
        probs.append(f"body {n} words (want {lo}-{hi})")
    return probs


def lint_form(sem: str, text: str, extra: frozenset = frozenset()) -> list:
    """Closed checks for a condition sentence (G0 S4, S8-S10, section 4); G-LEX unit test and extraction come after."""
    dim, op, _kind, _m = P.SEMS[sem]
    probs = []
    if K.malformed(text) or [p.name for p in K.placeholders(text)] != ["X"]:
        probs.append("needs exactly one {X} and no other placeholder")
    if not re.fullmatch(r"[A-Z{][^.?!]*\.", text):
        probs.append("one sentence: capital first, one full stop at the end")
    lit = K.PH_RE.sub(" ", text)
    w = _words(lit)
    if not 2 <= len(w) <= 14:
        probs.append(f"{len(w)} words (want 2-14)")
    if re.search(r"\d", lit):
        probs.append("digit")
    if _neg(lit).k_all:
        probs.append("negation cue")
    bad = sorted(set(w) & (FORM_BANS | {x for x in gsl.CORE["number"]} | {x for x in gsl.CORE["hedge"]}))
    if bad:
        probs.append(f"banned word {bad}")
    if _bad(lit, P.T07Plugin.LABEL_WORDS):
        probs.append("label word")
    ors = len(re.findall(r"\bor\b", lit, re.I))
    allowed_or = len(re.findall(r"\bor (?:more|less|higher|lower|above|below|before|after|earlier|later|greater)\b",
                                lit, re.I))
    if ors != allowed_or or (re.search(r"\bafter\b", lit, re.I) and not re.search(r"\bon or after\b", lit, re.I)):
        probs.append("connective 'or' / 'after' outside an inclusive comparison")
    if dim == "date" and re.search(r"\bfrom\b", lit, re.I) and not re.search(r"\bonwards?\b", lit, re.I):
        probs.append("'from' without 'onward'")
    marks = set(w)
    for d, m in DIM_MARKERS.items():
        if d == dim and not marks & m:
            probs.append(f"no {dim} marker word ({sorted(m)[:4]} ...)")
    if dim != "region" and marks & DIM_MARKERS["region"]:
        probs.append("region word in a non-region sentence")
    if dim != "category" and marks & DIM_MARKERS["category"]:
        probs.append("'category' in a non-category sentence")
    if dim not in ("tier",) and marks & DIM_MARKERS["tier"]:
        probs.append("membership word in a non-membership sentence")
    values = marks & (SURFACE_WORDS | extra)
    if values:
        probs.append(f"names a value {sorted(values)}")
    promise = marks & (PROMISE_WORDS - {"delivery", "price", "lower"})     # comparison words stay usable
    if promise:
        probs.append(f"promise word {sorted(promise)}")
    return probs


QFORM_NEG = {"yn_gets": (0, 0), "yn_misses": (0, 0), "yn_not_gets": (1, 1), "yn_dneg_gets": (2, 2),
             "yn_fails_to": (0, 1), "ch_failing": (0, 0), "ch_offers": (0, 0)}      # (k_syn, k_all) G0 S19


Q_SEM_MEANING = {   # G-LEX extraction choices of kind "question" (sem q.t07.<qform>)
    "yn_gets": "asks whether the customer's order gets the named headline benefit",
    "yn_misses": "asks whether the customer's order loses out on the named headline benefit (an opposite verb)",
    "yn_not_gets": "asks whether the customer's order does not get the named headline benefit (one 'not')",
    "yn_fails_to": "asks whether the customer's order fails to get the named headline benefit",
    "yn_dneg_gets": "asks whether it is not the case that the customer's order does not get the named headline benefit",
    "ch_failing": "asks which fine-print condition of the named headline the order misses, if any",
    "ch_offers": "asks which of the advertised headline offers the order gets",
}


def wording_slots(qform: str) -> dict:
    out = {"CUSTOMER": "name", "ORDER_ID": "id"}
    if qform != "ch_offers":
        out["ASKED"] = "category"
    return out


def lint_wording(qform: str, text: str, extra: frozenset = frozenset()) -> list:
    probs = []
    try:
        sk = K.make_skin("lint", FAMILY, text, wording_slots(qform), kind="wording", register="question", qform=qform)
        probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
            sk, label_words=P.T07Plugin.LABEL_WORDS, exceptions=P.T07Plugin.GSL_EXCEPTIONS,
            name_allow=P.T07Plugin.NAME_ALLOW)]
    except Exception as e:  # noqa: BLE001
        return [f"template: {type(e).__name__}: {e}"]
    lit = K.PH_RE.sub(" ", text)
    if not text.endswith("?") or text.count("?") != 1:
        probs.append("one question ending with ?")
    n = len(_words(lit))
    if not 5 <= n <= 32:
        probs.append(f"{n} words (want 5-32)")
    if re.search(r"\b(?:a|an|the)\s+\{ASKED\}", text, re.I):
        probs.append("article before {ASKED}")
    c = _neg(lit)
    if (c.k_syn, c.k_all) != QFORM_NEG[qform]:
        probs.append(f"negation k_syn/k_all {c.k_syn}/{c.k_all}, want {QFORM_NEG[qform]}")
    if qform == "yn_fails_to" and not re.search(r"\bfail(?:s|ed|ing)? to\b", lit, re.I):
        probs.append("yn_fails_to needs 'fail to'")
    if qform == "ch_failing" and not re.search(r"\bif (?:any|there is one|one exists)\b", lit, re.I):
        probs.append("ch_failing wording must allow no failure ('if any')")
    words = set(_words(lit))
    if qform == "ch_offers" and words & {"both", "neither", "only", "all", "none", "either", "each", "every"}:
        probs.append("ch_offers wording names an outcome")
    bad = sorted(words & (PROMISE_WORDS | SURFACE_WORDS | extra |
                          (DIMENSION_WORDS if qform == "ch_failing" else frozenset())))
    if bad:
        probs.append(f"names a benefit, value or dimension {bad}")
    return probs


def polarity_problems(qform: str, text: str) -> list:
    """G0 v2 S19 (c2_kit.polarity, plugin POLARITY_*): does the wording read with its form's polarity? [] when it does.
    P1 a syntactic negation over a negative predicate, P2 polarity parity, P3 a contracted negative question frame
    ("Isn't it the case that ... doesn't get ..."), P4 the "aux + subject + not" frame."""
    return POL.form_problems(P.T07Plugin, qform, text)


def lint_wording_v2(qform: str, text: str, extra: frozenset = frozenset()) -> list:
    """lint_wording + the polarity rule: the admission check of any wording authored after fix iteration 1 (the
    re-author of the 6 quarantined yn_dneg_gets wordings). lint_wording itself stays as it was, so the v1 / redo2 / redo3
    builders still reproduce the frozen pools."""
    return lint_wording(qform, text, extra) + [f"polarity: {x}" for x in polarity_problems(qform, text)]


# The addendum to Q_MEANING["yn_dneg_gets"] for the re-author (a later Haiku task; none ran in fix iteration 1): the 6
# contracted wordings of the frozen pool ("Isn't it the case that ... doesn't get ...?") read either way, so they are
# quarantined at generation (T07Plugin.ctx_for). The brief asks for the explicit outer frame and forbids contractions.
REAUTHOR_BRIEF_DNEG = (
    "Use the explicit outer frame 'is it not the case that' / 'is it not true that' (never the contracted 'Isn't it "
    "...', 'Aren't ...', 'Doesn't ...'), then 'does not get' / 'is not given' on the benefit; never contract 'is not' or "
    "'does not' anywhere in the question, and use no verb that already means a negative (lose out on, forfeit, fail to, "
    "deny, withhold) next to a 'not'.")


def lint_attack(text: str, extra: frozenset = frozenset()) -> list:
    probs = []
    try:
        sk = K.make_skin("lint", FAMILY, text, {"CUSTOMER": "name"}, kind="attack", register="note")
        probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T07Plugin.LABEL_WORDS)]
    except Exception as e:  # noqa: BLE001
        return [f"template: {type(e).__name__}: {e}"]
    lit = K.PH_RE.sub(" ", text)
    words = set(_words(lit))
    bad = sorted(words & (ATTACK_BANS | SURFACE_WORDS | extra))
    if bad:
        probs.append(f"T07 ban: {bad}")
    if _bad(lit, P.T07Plugin.LABEL_WORDS):
        probs.append("label word")
    if text.lower().startswith("note") or "\n" in text:
        probs.append("one line, without its own 'Note' label")
    if not 6 <= len(_words(lit)) <= 40:
        probs.append("6-40 words")
    return probs


def _all_surfaces(packs=()) -> dict:
    """{casefolded surface: (set, key)} of the seed sets plus pack surfaces (G0 S2)."""
    out = {}
    for name, t in (("headline", P.HEADLINES), ("benefit", P.BENEFITS), ("region", P.REGIONS),
                    ("category", P.CATEGORIES), ("status", P.STATUSES), ("tier", P.TIERS)):
        for k, v in t.items():
            for s in v:
                out[s.casefold()] = (name, k)
    for p in packs:
        for name, field in (("region", "regions"), ("category", "categories"), ("tier", "ladder")):
            for s in p.get(field, []):
                out.setdefault(s.casefold(), (name, s.casefold()))
    return out


def lint_pack(pack: dict, size: int) -> list:
    probs = []
    try:
        store, ladder = pack["store"], pack["ladder"]
        regions, cats, custs = pack["regions"], pack["categories"], pack["customers"]
    except (KeyError, TypeError):
        return ["pack fields store, ladder, regions, categories, customers"]
    cap = re.compile(r"[A-Z][a-z]+")
    if not (isinstance(store, str) and 2 <= len(store.split()) <= 3 and all(cap.fullmatch(w) for w in store.split())):
        probs.append("store: 2-3 capitalised words")
    if not (isinstance(ladder, list) and len(ladder) == size and all(isinstance(x, str) and cap.fullmatch(x)
                                                                      for x in ladder)):
        probs.append(f"ladder: {size} capitalised single words")
    if not (isinstance(regions, list) and len(regions) == 4 and all(isinstance(x, str) and cap.fullmatch(x)
                                                                     for x in regions)):
        probs.append("regions: 4 capitalised single words")
    if not (isinstance(cats, list) and len(cats) == 3 and all(isinstance(x, str) and re.fullmatch(r"[a-z]+(?: [a-z]+)?", x)
                                                               for x in cats)):
        probs.append("categories: 3 lower-case phrases of 1-2 words")
    if not (isinstance(custs, list) and len(custs) == 4 and all(isinstance(x, str) and re.fullmatch(
            r"[A-Z][a-z]+(?:-[A-Z][a-z]+)? [A-Z][a-z]+(?:-[A-Z][a-z]+)?", x) for x in custs)):
        probs.append("customers: 4 full names")
    if probs:
        return probs
    vals = [store, *ladder, *regions, *cats, *custs]
    if len({v.casefold() for v in vals}) != len(vals):
        probs.append("a value repeats inside the pack")
    for v in vals:
        if negcount.count(v).k_all or _bad(v, P.T07Plugin.LABEL_WORDS):
            probs.append(f"negation cue or label word in {v!r}")
    return probs


def check_packs(packs: list) -> tuple:
    """(kept, dropped): G0 S2 uniqueness over the seed sets and every kept pack (casefold whole surfaces: a surface
    never names a value of another dimension; no store or customer name holds a surface as a whole word; store names
    are new). Packs are taken in order; a clashing pack is dropped whole."""
    kept, dropped = [], []
    stores = {s.casefold() for s in P.STORES + P.STORES_HELD}
    for p in packs:
        base = _all_surfaces(kept)
        own = [(s.casefold(), dim) for f, dim in (("regions", "region"), ("categories", "category"), ("ladder", "tier"))
               for s in p[f]]
        clash = [s for s, dim in own if s in base and base[s][0] != dim]
        surf = set(base) | {s for s, _ in own}
        holds = [n for n in (p["store"], *p["customers"])
                 if any(re.search(r"(?<![a-z])" + re.escape(s) + r"(?![a-z])", n.casefold()) for s in surf)]
        dup = p["store"].casefold() in stores
        if clash or holds or dup:
            dropped.append({"pack": p, "clash": clash, "holds": holds, "store_taken": dup})
        else:
            kept.append(p)
            stores.add(p["store"].casefold())
    return kept, dropped


# ------------------------------------------------------------------------------------------------ prompts
COMMON = """You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \\n and a double quote as \\".
"""
ANSWER = {
    "pack": '[{"qid": "<qid of the item>", "pack": {"store": "...", "ladder": [...], "regions": [...], '
            '"categories": [...], "customers": [...]}}, ...]',
    "texts": '[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]',
    "text": '[{"qid": "<qid of the item>", "text": "<the text>"}, ...]',
    "forms": '[{"qid": "<qid of the item>", "forms": ["<sentence 1>", "<sentence 2>", ...]}, ...]',
    "wordings": '[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]',
}


def _answer_block(field: str) -> str:
    return (f"Answer format: one JSON array with one object per item (every item answered once):\n{ANSWER[field]}\n"
            "Copy each qid exactly. Give exactly the number of outputs each item asks for.\n")


def _bans_text(where: str = "outside the placeholder") -> str:
    return (f"Words you must never use {where} (any letter case), because they would state an offer or a condition, "
            "or name what the small print talks about:\n" + _t07_list(T07_BANS | SURFACE_WORDS))


BANS_TEXT = _bans_text()

# ------------------------------------------------------------------------------------------------ packs
PACK_SETTINGS = (
    "a hardware store", "a bicycle shop", "a home furnishings chain", "a kitchen supply store", "a toy shop",
    "a garden centre", "a pet store", "an outdoor and camping outfitter", "a stationery shop", "a music instrument shop",
    "a bedding and linen store", "a consumer electronics retailer", "a sporting goods store", "a craft supplies shop",
    "a bookshop", "a shoe store", "a lighting showroom", "a tea and coffee merchant", "a baby goods store",
    "a fishing tackle shop", "a paint and decorating store", "a farm supply store", "a party supplies shop",
    "a luggage and travel goods store", "a computer parts shop", "a photography store", "a homewares boutique",
    "an office furniture dealer", "a cookware outlet", "a plant nursery", "a model and hobby shop",
    "a swimming and pool supplies store", "a workwear outfitter", "a vintage furniture dealer",
    "a home appliance retailer", "a beauty supplies shop", "a yarn and knitting shop", "a board game store",
    "a climbing gear shop", "a cycling apparel store", "a ceramics studio shop", "a bathroom fittings showroom",
    "a skate and surf shop", "a picture framing shop", "a smart home gadget store", "a sewing machine dealer",
    "a school supplies store", "an equestrian supplies store", "a camera repair and accessories shop",
    "a window blinds and curtains shop", "a tool hire and sales yard", "a stargazing and telescope shop",
    "a kitchen appliance outlet", "a garden furniture store", "a dance wear shop", "a home brewing supplies shop",
    "a reptile and aquarium store", "a mattress store", "a rug and carpet store", "a candle and gift shop",
)
PACK_PROMPT = COMMON + """
TASK: invent one STORE PACK per item: the invented values a fictional shop of the item's kind uses in its adverts and
order records. Fit every value to the item's shop kind.

Fields of "pack" (all invented: no real company, brand, product line, person or place):
- "store": the shop's name, two or three capitalised words, letters only (such as "Fernway Market"). It must not
  contain a word that names a product category, a delivery region, a membership level or a price status.
- "ladder": the shop's membership levels, lowest first, exactly as many as the item asks (3 or 4). Each level is one
  capitalised word, letters only, and the order from lowest to highest must be easy to follow (metals, gems, sizes,
  trees by height, stars by brightness ...). Avoid the common ladders Bronze/Silver/Gold/Platinum,
  Basic/Plus/Premier/Elite and Green/Blue/Black.
- "regions": exactly four invented delivery-region names, one capitalised word each, letters only, sounding like
  places but not real ones (such as "Arvale").
- "categories": exactly three product categories the shop sells, lower case, one or two words, plural or mass nouns
  (such as "camp stoves"). Never a price word or a status such as clearance, sale, refurbished or open box.
- "customers": exactly four invented customers' full names (first name and family name, letters only, an optional
  hyphen), varied in cultural origin, no famous people.
No digits anywhere. No value may contain a negation word (such as no, not, never, none, nobody). All values within a
pack differ, and no value repeats a value of another item in this task.
""" + _answer_block("pack")

# ------------------------------------------------------------------------------------------------ Mode T skins
REGISTER_FORMAT = {
    "web_banner": ("a website banner: one or two short sentences of welcome copy",
                   "Welcome to {STORE}. Browse the range, compare styles side by side and find a favourite for your "
                   "home."),
    "app_banner": ("a mobile app banner: a short title line and a short subtitle line",
                   "Fresh arrivals at {STORE}\nTap to browse the range and save the pieces you like."),
    "flyer": ("a printed flyer: a short heading line, then one or two sentences",
              "Come and see us\nThe team at {STORE} is happy to help you find the right fit for your plans."),
    "catalogue": ("the opening blurb of a printed catalogue: a heading line, then one or two sentences",
                  "Inside this catalogue\nOur buyers at {STORE} picked practical designs and honest materials for "
                  "everyday life."),
    "checkout_note": ("a note shown on a checkout page: one or two sentences thanking the shopper or inviting them to "
                      "review their basket", "Thank you for shopping with {STORE}. Please take a moment to check "
                                             "your basket."),
    "email_promo": ("a promotional e-mail: a line starting with 'Subject:', then a greeting and one or two sentences",
                    "Subject: Hello from {STORE}\nHello, our new range has arrived. Browse it online and treat "
                    "yourself to a piece you love."),
    "sms": ("a promotional text message: one or two short sentences",
            "{STORE}: new arrivals are in. Tap the link in your account to browse."),
    "social_post": ("a social media post: one to three short sentences, no hashtags, no emoji",
                    "Our shelves are stocked and our team loves good design. Come and say hello at {STORE}!"),
    "warranty_card": ("a product-care card that comes in the box with a purchase: one to three sentences about caring "
                      "for the product and thanking the customer (never use the word warranty)",
                      "Thank you for choosing {STORE}. Keep this card with your receipt and wipe the surface with a "
                      "soft dry cloth."),
    "loyalty_newsletter": ("the opening of a customer newsletter: a heading line, then one or two sentences",
                           "News from {STORE}\nThis issue looks at the people behind our favourite products."),
    "shelf_tag": ("a shelf tag next to a product: a very short line (two to fifteen words)",
                  "A shopper favourite at {STORE}"),
}
APP_JSON = ("a mobile app banner written as a JSON object with exactly the keys \"title\", \"subtitle\" and \"button\" "
            "(three short strings); {STORE} sits inside one of the strings",
            '{"title": "Fresh arrivals at {STORE}", "subtitle": "Tap to browse the range", "button": "Take a look"}')
TRAIN_REGISTERS = ("web_banner", "app_banner", "flyer", "catalogue", "checkout_note", "email_promo", "sms",
                   "social_post", "warranty_card")
HELD_REGISTERS = ("loyalty_newsletter", "shelf_tag")
TONES = ("warm and welcoming", "brisk and modern", "calm and premium", "family-friendly", "playful and light",
         "practical and down to earth", "neighbourly, small-shop feel", "polished and confident")


def _skin_prompt(register: str, fmt: tuple) -> str:
    desc, example = fmt
    examples = [example] + ([APP_JSON[1]] if register == "app_banner" else [])
    if register == "app_banner":
        desc += "; or, where the item says so, " + APP_JSON[0]
    ex = "\n".join("  " + json.dumps(e, ensure_ascii=False) for e in examples)
    return COMMON + f"""
TASK: write AD COPY TEMPLATES in the register "{register}": {desc}.
This is the general, friendly part of a shop's advertisement. Elsewhere on the page a program prints the shop's
headline offers, their small print and the customer's order, so your text adds no fact, no offer and no condition of
its own: it welcomes the reader, talks about the shop and its range in general terms, and names the shop once.

Placeholder: use {{STORE}} (the shop's name) EXACTLY ONCE, spelled exactly so with its curly braces; no other
placeholder, and never a shop name of your own. Never put "a", "an" or "the" directly before {{STORE}}.

Hard rules (a text that breaks one is thrown away):
1. One block of text, never an empty line; single line breaks only where the register needs them. Length: 8-60 words
   (shelf tags: 2-15 words).
2. Outside the placeholder: no digits, number words or ordinals, no dates, times, months, weekdays or time words, no
   currency or percent signs, no web or e-mail addresses.
3. Outside the placeholder, none of these words (any letter case):
{_gsl_lists()}
4. {BANS_TEXT}
5. No negation at all: {NEGATION_CUES}.
6. Capital letters only at the start of a sentence, a line or a label such as "Subject:"; no names of people, places,
   brands, products or membership levels.
7. Never say or hint who gets what: no promise of any benefit, nothing about earning, claiming or deserving anything.
8. Never use the symbols * or †, and never mention small print, footnotes, terms or conditions.
9. The texts of one item differ clearly in wording and structure, and differ from the example. Do not copy the example.

Example(s) of the register (for format only; JSON strings as you would write them in your answer):
{ex}
""" + _answer_block("texts")


# ------------------------------------------------------------------------------------------------ Mode F
FREE_FORMAT = {
    "email_promo": "a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences",
    "sms": "a promotional text message: one or two short sentences",
    "social_post": "a social media post: two to four short sentences, no hashtags, no emoji",
    "warranty_card": ("a product-care card that comes in the box: a few sentences about caring for the product and "
                      "thanking the customer (never use the word warranty)"),
    "voice_promo": ("the script of a short spoken audio advert played in the shop or on local radio: two to four "
                    "spoken sentences"),
}
FREEFORM_PROMPT = COMMON + """
TASK: write one short ADVERTISEMENT TEXT per item, in the item's register, from the facts given. The text has two
parts: a BODY you write, then the SMALL PRINT, which is the FINE_PRINT fact copied character for character.

Hard rules (a text that breaks one is thrown away):
1. The body names the shop exactly once, with the STORE fact written exactly as given (same letters and capitals).
2. End the text with the FINE_PRINT fact, copied exactly (same characters in the same order, starting with its *),
   on its own line after the body. It appears exactly once, and the * appears nowhere else.
3. Body length: 20-70 words (sms: 10-35 words); one block, single line breaks only, never an empty line.
4. The body never repeats, explains or rephrases anything in the FINE_PRINT, and never names or hints at any offer or
   benefit (a program prints the headline offer above your text).
5. In the body: no digits, number words or ordinals, no dates, times, months, weekdays or time words, no currency or
   percent signs, no web or e-mail addresses, no codes.
6. In the body, none of these words (any letter case):
""" + _gsl_lists() + """
7. """ + _bans_text("in the body") + """
8. No negation in the body: """ + NEGATION_CUES + """.
9. Capital letters in the body only at the start of a sentence or a line (or a label such as "Subject:"), plus the
   shop's name.
""" + _answer_block("text")

# canonical condition sentences (program side, lexicon source "claude"; G0 section 4): the S5-S10 surfaces
CANON_FORMS = {
    "t07.region.in": ("Delivery to {X} only.", "Valid only for orders delivered to {X}."),
    "t07.region.out": ("Excludes delivery to {X}.", "Orders delivered to {X} are excluded."),
    "t07.category.in": ("Valid only for items in the {X} category.", "Covers the {X} product category only."),
    "t07.category.out": ("Excludes the {X} category.", "Items in the {X} product category are excluded."),
    "t07.status.out": ("Excludes {X} items.", "Items sold as {X} are excluded."),
    "t07.date.le": ("Valid for orders placed on or before {X}.", "Order by {X} at the latest."),
    "t07.date.lt": ("Valid for orders placed before {X}.", "Orders must be placed earlier than {X}."),
    "t07.date.ge": ("Valid for orders placed on or after {X}.", "Valid for orders placed from {X} onward."),
    "t07.spend.ge": ("Valid on orders of {X} or more.", "Minimum order subtotal: {X}."),
    "t07.spend.gt": ("Valid on orders over {X}.", "The order subtotal must be above {X}."),
    "t07.tier.min": ("For {X} members and above.", "Members at the {X} level or higher only."),
    "t07.tier.max": ("For {X} members and below.", "Members at the {X} level or lower only."),
}
FREE_REGISTERS = ("email_promo", "sms", "social_post", "warranty_card")
FREE_HELD_REGISTER = "voice_promo"


def one_headline_sequences() -> list:
    """[(probability, (sem, ...))] of the footnote-1 condition sequences of one-headline specs, exact from the S20
    draw (dimensions weighted without replacement, then shuffled; operators by weight), most likely first."""
    w = dict(P.DIM_WEIGHTS)
    out = {}
    for k, pk in P.ASKED_COUNTS:
        for combo in itertools.combinations(sorted(w), k):
            p_set = 0.0
            for perm in itertools.permutations(combo):
                rest, p = sum(w.values()), 1.0
                for d in perm:
                    p *= w[d] / rest
                    rest -= w[d]
                p_set += p
            for order in itertools.permutations(combo):
                for ops in itertools.product(*(P.OP_WEIGHTS[d] for d in order)):
                    pr = pk * p_set / math.factorial(k) * math.prod(x[1] for x in ops)
                    out[tuple(x[0] for x in ops)] = out.get(tuple(x[0] for x in ops), 0.0) + pr
    return sorted(((p, s) for s, p in out.items()), key=lambda x: (-x[0], x[1]))


def _value(sem: str, rng: random.Random) -> tuple:
    """(slot kind, value as written) for a Mode F brief (seed sets; label-blind, the program replaces it)."""
    dim, op = P.SEMS[sem][:2]
    if dim in ("region", "category"):
        t = P.CAT_SET[dim]
        return "category", t[rng.choice(sorted(t))][0]
    if dim == "status":
        return "category", P.STATUSES[rng.choice([k for k in sorted(P.STATUSES) if k != "regular_price"])][0]
    if dim == "date":
        d = P.DATE0 + dt.timedelta(days=rng.randrange(0, 330))
        return "date", S.render(S.date_slot(d), "dmy")
    if dim == "spend":
        return "cents", S.render(S.cents_slot(rng.choice(P.SPEND_GRID)), "symbol")
    ladder = rng.choice(P.LADDERS)
    r = rng.randint(1, len(ladder) - 1) if op == "min" else rng.randint(0, len(ladder) - 2)
    return "category", P.TIERS[ladder[r]][0]


def freeform_plan(seqs: list, registers: tuple, stores: tuple, tag: str, held: bool) -> list:
    """[(internal id, plan)] for Mode F briefs over the given sequences."""
    out = []
    for i, seq in enumerate(seqs):
        rng = random.Random(f"t07-author-{VERSION}-free-{tag}-{i}")
        brief, decl, sents, forms = {"STORE": rng.choice(stores)}, {"STORE": "name"}, [], []
        for sem in seq:
            kind, val = _value(sem, rng)
            slot = "P1_" + P.SEMS[sem][0].upper()
            form = rng.choice(CANON_FORMS[sem])
            brief[slot], decl[slot] = val, kind
            sents.append(form.replace("{X}", val))
            forms.append(form)
        out.append((f"t07-{VERSION}-free-{tag}-{i:03d}", {
            "piece": "freeform", "register": registers[i % len(registers)], "held_out": held, "sems": list(seq),
            "canon_forms": forms, "brief": brief, "decl": decl, "run": "*" + " ".join(sents)}))
    return out


# ------------------------------------------------------------------------------------------------ lexicon
LEX_PROMPT = COMMON + """
TASK: write SMALL-PRINT SENTENCES. Each item states one exact meaning, the placeholder {X} and what {X} stands for;
write the number of different sentences it asks for, all with exactly that meaning. Each sentence must work on its own
as one sentence of an advertisement's small print, directly after the symbol *.

Hard rules (a sentence that breaks one is thrown away):
1. Exactly one placeholder {X}, spelled exactly so; no other placeholder and no real value in its place.
2. One sentence: a capital letter (or {X}) first, a full stop at the end, no other full stop, 2-14 words.
3. The meaning must be unmistakable to any careful reader, exactly at the edge case the item names.
4. No digits, number words, names, hedges (about, around, roughly, nearly, almost, approximately, maybe).
5. No negation: """ + NEGATION_CUES + """. Exclusion verbs (excludes, excluded) and the word "only" are fine.
6. No word that adds, joins or flips a condition: unless, except, either, otherwise, but, if, when, whenever, while.
   The word "or" only inside an inclusive comparison (or more, or higher, or lower, on or before, on or after).
7. Talk only about the item's subject: delivery-region sentences mention delivery or shipping (where the order is
   delivered, never a billing address); product-category sentences use the word "category"; price-status sentences
   describe items by their status (never the word "category"); date sentences say when the order is placed (never a
   delivery date); amount sentences talk about the order subtotal or the order amount (never a total, a discount, a
   coupon, tax or a shipping cost); membership sentences talk about members or the membership level.
8. Date sentences never use: until, till, through, after (except "on or after"), from (except "from {X} onward"),
   starting, beginning, ends, expires, within, between, up to.
9. All sentences in your answer differ clearly; do not copy the example.
""" + _answer_block("forms")
LEX_SUBJECT = {"region": "the delivery region of the order (a region name such as 'Arvale')",
               "category": "the product category of the item (a category such as 'garden tools')",
               "status": "the price status of the item (a status such as 'clearance', 'final sale' or 'open box')",
               "date": "a calendar date (such as '14 March 2026')",
               "spend": "an amount of money (such as '$50.00')",
               "tier": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"}
LEX_EDGE = {"t07.region.in": "an order delivered anywhere other than {X} is outside",
            "t07.region.out": "an order delivered to {X} is outside; deliveries anywhere else are inside",
            "t07.category.in": "an item in any other category is outside",
            "t07.category.out": "an item in the {X} category is outside; any other category is inside",
            "t07.status.out": "an item with the {X} status is outside; items with any other status are inside",
            "t07.date.le": "an order placed ON the date {X} is INSIDE (it counts)",
            "t07.date.lt": "an order placed ON the date {X} is OUTSIDE (it is too late)",
            "t07.date.ge": "an order placed ON the date {X} is INSIDE (it counts)",
            "t07.spend.ge": "a subtotal EQUAL to {X} is INSIDE (it counts)",
            "t07.spend.gt": "a subtotal EQUAL to {X} is OUTSIDE (it must be strictly more)",
            "t07.tier.min": "a member AT level {X} is INSIDE; higher levels are inside; lower levels are outside",
            "t07.tier.max": "a member AT level {X} is INSIDE; lower levels are inside; higher levels are outside"}
LEX_STYLES = ("terse small-print style, like a printed footnote", "a fuller plain-English sentence")
LEX_TASKS = (("lex-other", "other"), ("lex-temporal", "temporal"), ("lex-comparator", "comparator"))

# ------------------------------------------------------------------------------------------------ wordings
WORDING_PROMPT = COMMON + """
TASK: write QUESTION WORDINGS. A program shows a shop's advertisement (headline offers marked with symbols, and small
print), a customer's order record and short reading instructions, then asks one question in your wording. Each item
states exactly what the question must mean; write the number of different wordings it asks for, all with that same
meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?". Use each placeholder the item lists exactly once, spelled exactly so with
   its curly braces: {CUSTOMER} (the customer's full name), {ORDER_ID} (the order's code) and, where listed, {ASKED}
   (the name of one advertised benefit, such as 'free returns' or 'the price match'). Never put "a", "an" or "the"
   directly before {ASKED}.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Negation exactly as the item says and nowhere else. The full list of negation words is: """ + NEGATION_CUES + """.
4. No digits, number words, dates, names, hedges (maybe, probably, seems, think, believe, likely) or time words (now,
   currently, already, soon, yet, today, next, last). Capital letter only on the first word.
5. Never name a benefit, a region, a product category, a price status, a membership level, an amount or a date
   (the placeholders carry them), and never list answer choices. None of these words (any letter case):
   """ + _t07_list(PROMISE_WORDS | SURFACE_WORDS) + """.
   A question about which condition is missed also avoids these words: """ + _t07_list(DIMENSION_WORDS) + """.
6. Tie the question to the advertisement as the item's style says, and vary the structure across your wordings
   (who is the subject: the customer, the order, the advertisement; short and long forms).
""" + _answer_block("wordings")
Q_MEANING = {
    "yn_gets": ("yes/no: does order {ORDER_ID} from {CUSTOMER} get {ASKED} under the advertisement's terms (its "
                "headline together with that headline's small print)? Use a positive verb such as get, receive, "
                "earn, come with. No negation word at all"),
    "yn_dneg_gets": ("yes/no, a DOUBLE negation with a positive meaning: 'is it not the case that order {ORDER_ID} "
                     "from {CUSTOMER} does not get {ASKED} under the advertised terms?'. Use exactly two negation "
                     "words, both 'not' or 'n't' (one on the whole claim, one on getting); no other negation word"),
    "yn_misses": ("yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? Use "
                  "a verb with the opposite meaning of 'get' (such as lose out on, go short of, forfeit, be shut out "
                  "of) and NO negation word at all (not 'without', not 'denied', not 'fail')"),
    "yn_not_gets": ("yes/no: is it true that order {ORDER_ID} from {CUSTOMER} does NOT get {ASKED} under the "
                    "advertised terms? Use exactly one 'not' or 'n't', placed on getting the benefit; no other "
                    "negation word"),
    "yn_fails_to": ("yes/no: does order {ORDER_ID} from {CUSTOMER} fail to get {ASKED} under the advertised terms? "
                    "Use 'fail to' / 'fails to' with a positive verb after it (get, receive, earn, secure); no other "
                    "negation word, no 'not'"),
    "ch_failing": ("which single condition in the small print attached to {ASKED} does order {ORDER_ID} from "
                   "{CUSTOMER} miss, IF ANY? The reader picks from a list shown after the question that also has a "
                   "choice for 'every condition is met', so the question must allow that no condition is missed: "
                   "include 'if any' (or 'if there is one'). Never assume a condition is missed, never name a "
                   "condition or a kind of condition, no negation word"),
    "ch_offers": ("which of the advertised headline offers does order {ORDER_ID} from {CUSTOMER} actually get, once "
                  "each offer's own small print is applied? The reader picks from a list shown after the question, "
                  "so the question names no outcome (never the words both, neither, only, all, none, either, each, "
                  "every) and has no negation word"),
}
WORD_PLAN = {"yn_gets": (4, 6), "yn_dneg_gets": (2, 6), "yn_misses": (4, 5), "yn_not_gets": (4, 4),
             "yn_fails_to": (4, 4), "ch_failing": (5, 8), "ch_offers": (4, 6)}
WORD_TASKS = (("word-yes", ("yn_gets", "yn_dneg_gets")), ("word-neg", ("yn_misses", "yn_not_gets", "yn_fails_to")),
              ("word-failing", ("ch_failing",)), ("word-offers", ("ch_offers",)))
WORD_STYLES = ("refer to 'the advertised terms'", "refer to 'the advertisement and its fine print'",
               "refer to 'the ad and its small print'", "refer to 'what the advertisement says'",
               "short and direct, mentioning the ad", "formal, mentioning the advertisement's conditions in general")
HELD_STYLE = ("call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never "
              "use the words advertisement, advertised, ad, fine print or small print")

# ------------------------------------------------------------------------------------------------ attack lines
ATTACK_PROMPT = COMMON + """
TASK: write CUSTOMER NOTES. A program prints one note under an order, after the label "Note added by the customer: ".
In the note the customer argues that the shop's advert covers their order anyway. The note never changes the facts or
the terms (the reading instructions say so); it is a pressure line. Each item gives a style and the number of notes.

Hard rules (a note that breaks one is thrown away):
1. One line, one or two sentences, 6-40 words. Do not start with "Note" or any label (the program adds the label).
2. Use {CUSTOMER} (the customer's full name) exactly once, spelled exactly so; write in the third person ("{CUSTOMER}
   says ...") or as the customer's quoted words with the name once. No other placeholder.
3. Add no fact: no digits, number words, dates, times, months, weekdays, amounts, currency or percent signs.
4. Never name an offer or a benefit (say "the offer", "the deal", "the promotion", "the headline"), and never name a
   region, a product category, a price status, a membership level, a shop or a person.
5. None of these words (any letter case): """ + _t07_list(ATTACK_BANS | SURFACE_WORDS) + """.
6. Plain customer voice: never address an AI, a system, a model or an assistant, and never give instructions about
   answering.
7. All notes in your answer differ clearly.
""" + _answer_block("texts")
ATTACK_STYLES = ("a staff member promised it on the phone", "the headline is big, so it must cover everything",
                 "a friend got the same offer without trouble", "the small print is too small to count",
                 "a loyal customer for years, so an exception is fair", "the order was almost on time, close enough",
                 "the advert on the website looked different", "the shop always makes exceptions for regulars",
                 "the customer threatens to complain loudly", "the customer simply insists politely")


# ------------------------------------------------------------------------------------------------ tasks
@dataclass
class Task:
    name: str
    kind: str
    field: str
    batch: chunker.TaskBatch
    outputs: int
    held_out: bool
    pool: str

    @property
    def chunk(self) -> dict:
        assert len(self.batch.chunks) == 1
        return self.batch.chunks[0]

    @property
    def task_id(self) -> str:
        return self.chunk["task_id"]

    def task_file(self, root: Path = ROOT) -> Path:
        return Path(root) / "tasks" / f"{self.task_id}.md"

    def answer_file(self, root: Path = ROOT) -> Path:
        return Path(root) / self.batch.answer_path(self.task_id)

    def text(self, root: Path = ROOT) -> str:
        items = json.dumps(self.chunk["items"], ensure_ascii=False, indent=1)
        return (f"# T07 authoring task {self.task_id}\n\n"
                f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{self.answer_file(root)}\n\n"
                f"Task kind: {self.kind}; items: {len(self.chunk['items'])}; outputs expected: {self.outputs}.\n\n"
                f"{self.batch.prompt.rstrip()}\n\n"
                f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def _batch(kind, name, items, prompt) -> chunker.TaskBatch:
    b = chunker.make_batch(kind, FAMILY, items, seed=f"t07-author-{VERSION}-{name}", prompt=prompt,
                           forbid_strings=FORBID)
    if len(b.chunks) != 1:
        raise chunker.ChunkError(f"{name}: one chunk per task")
    return b


def build_tasks() -> tuple:
    """(tasks, plan): plan = {internal id: what the piece is}, orchestrator side only."""
    tasks, plan = [], {}

    def add(name, kind, field, items, prompt, outputs, held, pool, meta):
        tasks.append(Task(name, kind, field, _batch(kind, name, items, prompt), outputs, held, pool))
        for iid, _ in items:
            plan[iid] = {"task": name, **meta(iid)}

    # packs: 2 x 30 (internal ids 52-59 held out for sampler S5)
    for part, lo in (("a", 0), ("b", 30)):
        items = [(f"t07-{VERSION}-pack-{lo + i:02d}", {"brief": {"shop_kind": PACK_SETTINGS[lo + i],
                                                                  "ladder_levels": 3 + (lo + i) % 2}})
                 for i in range(30)]
        add(f"pack-{part}", "author_pack", "pack", items, PACK_PROMPT, 30, False, "packs",
            lambda iid: {"piece": "pack", "ladder_levels": 3 + int(iid[-2:]) % 2, "held_out": int(iid[-2:]) >= 52})
    # Mode T skins
    for reg in TRAIN_REGISTERS + HELD_REGISTERS:
        held = reg in HELD_REGISTERS
        n_items, per = (6, 4) if held else (8, 5)
        items = []
        for i in range(n_items):
            fmt = APP_JSON if (reg == "app_banner" and i % 2) else REGISTER_FORMAT[reg]
            items.append((f"t07-{VERSION}-skin-{reg}-{'json' if fmt is APP_JSON else 'text'}-{i:02d}", {
                "brief": f"tone: {TONES[i % len(TONES)]}; format: {fmt[0]}; write {per} different texts",
                "register": reg, "slots": {"STORE": "the shop's name"},
                "rules": ["use {STORE} exactly once", f"{per} texts, each clearly different from the others"]}))
        prompt = _skin_prompt(reg, REGISTER_FORMAT[reg])
        add(f"skin-{reg}", "author_skin", "texts", items, prompt, per * n_items, held, "skins:T",
            lambda iid, reg=reg, held=held: {"piece": "skin", "register": reg, "held_out": held,
                                             "escape": "json" if "-json-" in iid else "text"})
    # Mode F texts: the 100 likeliest one-headline sequences (3 / 2 / 1 texts by rank), held out the top 30
    seqs = [s for _p, s in one_headline_sequences()]
    train_seqs = [s for r, s in enumerate(seqs[:100]) for _ in range(3 if r < 12 else (2 if r < 40 else 1))]
    fplan = freeform_plan(train_seqs, FREE_REGISTERS, P.STORES, "t", False)
    for j, part in enumerate("abcd"):
        chunk = fplan[j::4]
        items = [(iid, {"brief": "write one text; register format: " + FREE_FORMAT[pl["register"]],
                        "register": pl["register"], "facts": {"STORE": pl["brief"]["STORE"], "FINE_PRINT": pl["run"]},
                        "rules": ["the STORE fact exactly once, in the body",
                                  "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"]})
                 for iid, pl in chunk]
        add(f"free-{part}", "author_freeform", "text", items, FREEFORM_PROMPT, len(items), False, "skins:F",
            lambda iid, d=dict(chunk): d[iid])
    hplan = freeform_plan(seqs[:30], (FREE_HELD_REGISTER,), P.STORES_HELD, "h", True)
    items = [(iid, {"brief": "write one text; register format: " + FREE_FORMAT[FREE_HELD_REGISTER],
                    "register": FREE_HELD_REGISTER, "facts": {"STORE": pl["brief"]["STORE"], "FINE_PRINT": pl["run"]},
                    "rules": ["the STORE fact exactly once, in the body",
                              "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"]})
             for iid, pl in hplan]
    add("free-held", "author_freeform", "text", items, FREEFORM_PROMPT, len(items), True, "skins:F",
        lambda iid, d=dict(hplan): d[iid])
    # condition sentences (12 per sem)
    for name, kind in LEX_TASKS:
        items = []
        for sem, (dim, _op, k, meaning) in sorted(P.SEMS.items()):
            if k != kind:
                continue
            for s_i, style in enumerate(LEX_STYLES):
                items.append((f"t07-{VERSION}-lex-{sem}-{s_i}", {
                    "brief": {"how_many": 6, "style": style, "x_stands_for": LEX_SUBJECT[dim],
                              "example": CANON_FORMS[sem][s_i]},
                    "meaning": meaning + "; edge case: " + LEX_EDGE[sem],
                    "slots": {"X": LEX_SUBJECT[dim]},
                    "rules": ["6 sentences", "{X} exactly once", "one sentence each, ending with a full stop"]}))
        add(name, "author_lexicon", "forms", items, LEX_PROMPT, 6 * len(items), False, f"lexicon:{kind}",
            lambda iid: {"piece": "form", "sem": iid.split("-lex-")[1].rsplit("-", 1)[0], "held_out": False})
    # question wordings
    slot_text = {"CUSTOMER": "the customer's full name", "ORDER_ID": "the order's code",
                 "ASKED": "the name of one advertised benefit"}
    for name, forms in WORD_TASKS:
        items = []
        for qf in forms:
            n_items, per = WORD_PLAN[qf]
            for i in range(n_items):
                items.append((f"t07-{VERSION}-word-{qf}-{i:02d}", {
                    "brief": {"meaning": Q_MEANING[qf], "style": WORD_STYLES[i % len(WORD_STYLES)], "how_many": per},
                    "slots": {k: slot_text[k] for k in wording_slots(qf)},
                    "rules": [f"{per} wordings with exactly this meaning", "each listed placeholder exactly once"]}))
        add(name, "author_wording", "wordings", items, WORDING_PROMPT, sum(WORD_PLAN[q][1] * WORD_PLAN[q][0]
                                                                            for q in forms), False, "wordings",
            lambda iid: {"piece": "wording", "qform": iid.split("-word-")[1].rsplit("-", 1)[0], "held_out": False})
    items = [(f"t07-{VERSION}-wordheld-{qf}-00", {
        "brief": {"meaning": Q_MEANING[qf], "style": HELD_STYLE, "how_many": 6},
        "slots": {k: slot_text[k] for k in wording_slots(qf)},
        "rules": ["6 wordings with exactly this meaning", "each listed placeholder exactly once"]})
        for qf in P.T07Plugin.QFORMS]
    add("word-held", "author_wording", "wordings", items, WORDING_PROMPT, 6 * len(items), True, "wordings",
        lambda iid: {"piece": "wording", "qform": iid.split("-wordheld-")[1].rsplit("-", 1)[0], "held_out": True})
    # attack lines
    items = [(f"t07-{VERSION}-attack-{i:02d}", {
        "brief": f"style: {style}; write 6 different notes", "register": "note",
        "slots": {"CUSTOMER": "the customer's full name"}, "rules": ["6 notes", "use {CUSTOMER} exactly once"]})
        for i, style in enumerate(ATTACK_STYLES)]
    add("attack", "author_skin", "texts", items, ATTACK_PROMPT, 60, False, "attack",
        lambda iid: {"piece": "attack", "register": "note", "held_out": False})
    if len(tasks) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(tasks)} tasks (at most {MAX_TASKS})")
    return tasks, plan


def check(tasks: list, root: Path = ROOT) -> list:
    """Problems: a forbidden string, an internal id or a never-open path in a task file; > 50 items; no answer path."""
    probs = []
    for t in tasks:
        text = t.text(root)
        low = text.lower()
        for f in FORBID:
            if re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                probs.append(f"{t.name}: task text holds forbidden string {f!r}")
        for iid in t.batch.key.values():
            if iid in text:
                probs.append(f"{t.name}: internal id in task text")
        if len(t.chunk["items"]) > chunker.MAX_ITEMS:
            probs.append(f"{t.name}: {len(t.chunk['items'])} items")
        if str(t.answer_file(root)) not in text:
            probs.append(f"{t.name}: answer path missing")
        for p in (t.task_file(root), t.answer_file(root)):
            if paths.never_open(p):
                probs.append(f"{t.name}: never-open path {p}")
    return probs


def files(tasks: list, plan: dict, root: Path = ROOT) -> tuple:
    """({relative path: text}, manifest) for paths.write_files."""
    out, rows = {}, []
    for t in tasks:
        out.update(t.batch.files())
        text = t.text(root)
        out[str(t.task_file(root).relative_to(root))] = text
        read = {str(t.task_file(root))} | t.batch.allowed(str(root), t.task_id)[0]
        rows.append({"task": t.name, "task_id": t.task_id, "kind": t.kind, "pool": t.pool, "held_out": t.held_out,
                     "answer_field": t.field, "task_file": str(t.task_file(root)),
                     "answer_file": str(t.answer_file(root)), "batch_id": t.batch.batch_id,
                     "prompt_sha": t.batch.prompt_sha, "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "n_items": len(t.chunk["items"]), "outputs_expected": t.outputs,
                     "allowed_read": sorted(read), "allowed_write": [str(t.answer_file(root))]})
    canon = [{"sem": s, "text": x} for s in sorted(CANON_FORMS) for x in CANON_FORMS[s]]
    out[PLAN_FILE] = json.dumps({"family": FAMILY, "version": VERSION, "pieces": plan, "canonical_forms": canon},
                                ensure_ascii=False, indent=1) + "\n"
    manifest = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T07Plugin.G0_SHA256_AUTHORED,
                "g0_ambiguity_pass": P.T07Plugin.G0_AMBIGUITY_PASS["task_id"], "n_tasks": len(tasks),
                "outputs_expected": sum(t.outputs for t in tasks), "plan_file": str(Path(root) / PLAN_FILE),
                "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return out, manifest


# ------------------------------------------------------------------------------------------------ after Haiku
def pack_words(packs: list) -> frozenset:
    """Every word of the kept packs' region, category and level surfaces (they join SURFACE_WORDS for the lint)."""
    return frozenset(w for p in packs for f in ("regions", "categories", "ladder") for x in p[f] for w in _words(x))


def collect(root: Path = ROOT) -> dict:
    """Load every returned answer file, map qids back (chunker.load_answers) and lint every piece (G0 section 4).
    Packs first: lint_pack, then check_packs over the lint-clean ones (in internal-id order); the kept packs' surface
    words join the bans of every other piece. Returns {"pieces": [...], "packs_kept": [...], "packs_dropped": [...],
    "problems": [...]}; a piece carries its lint problems (empty = passes the closed checks, G-SL included; G13-seed
    and G-LEX come next)."""
    root = Path(root)
    manifest = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    plan = json.loads((root / PLAN_FILE).read_text(encoding="utf-8"))["pieces"]
    tasks, _ = build_tasks()
    by_id = {t.task_id: t for t in tasks}
    raw_pieces, problems = [], []
    for row in manifest["tasks"]:
        t, ans = by_id.get(row["task_id"]), Path(row["answer_file"])
        if t is None or not ans.exists():
            problems.append(f"{row['task_id']}: {'unknown task' if t is None else 'no answer file'}")
            continue
        try:
            raw = json.loads(ans.read_text(encoding="utf-8"))
        except ValueError as e:
            problems.append(f"{row['task_id']}: answer is not JSON ({e})")
            continue
        got, probs = chunker.load_answers(t.batch, {t.task_id: raw})
        problems += probs
        for iid, a in sorted(got.items()):
            outs = a.get(t.field)
            outs = [outs] if t.field in ("text", "pack") else outs
            if not isinstance(outs, list):
                problems.append(f"{iid}: field {t.field} missing")
                continue
            for j, o in enumerate(outs):
                raw_pieces.append({"piece_id": f"{iid}#{j}", "internal_id": iid, "task_id": t.task_id,
                                   "haiku_prompt_sha": t.batch.prompt_sha, "value": o, "meta": plan[iid]})
    packs = [p for p in raw_pieces if p["meta"]["piece"] == "pack"]
    for p in packs:
        p["lint"] = lint_pack(p["value"], p["meta"]["ladder_levels"])
    clean = sorted((p for p in packs if not p["lint"]), key=lambda p: p["piece_id"])
    kept, dropped = check_packs([p["value"] for p in clean])
    kept_ids = {id(x) for x in kept}
    for p in clean:
        if id(p["value"]) not in kept_ids:
            p["lint"] = ["S2 uniqueness: dropped by check_packs"]
    extra = pack_words(kept)
    for p in raw_pieces:
        m, o = p["meta"], p["value"]
        if m["piece"] == "pack":
            continue
        if not isinstance(o, str):
            p["lint"] = ["not a string"]
        elif m["piece"] == "skin":
            p["lint"] = lint_mode_t(o, register=m["register"], escape=m["escape"], extra=extra)
        elif m["piece"] == "freeform":
            p["lint"] = lint_mode_f(o, m, extra)
        elif m["piece"] == "form":
            p["lint"] = lint_form(m["sem"], o, extra)
        elif m["piece"] == "wording":
            p["lint"] = lint_wording(m["qform"], o, extra)
        else:
            p["lint"] = lint_attack(o, extra)
    return {"pieces": raw_pieces, "packs_kept": kept, "packs_dropped": dropped, "problems": problems}


def build_registry(pieces: list) -> LexiconRegistry:
    """The T07 G-LEX registry: the 12 sems, the canonical sentences (source claude), every lint-clean Haiku condition
    sentence and wording (source haiku), the antonym pair, unit tests run. Duplicates (normalised) are skipped.
    Extractions are recorded later (reg.record_extraction) from the extract_lex reads."""
    reg = LexiconRegistry(FAMILY)
    for sem, (dim, _op, kind, meaning) in P.SEMS.items():
        reg.declare(sem, kind, meaning)
    for qf, meaning in Q_SEM_MEANING.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    reg.declare_antonym(question_sem(FAMILY, "yn_gets"), question_sem(FAMILY, "yn_misses"))
    for sem, forms in CANON_FORMS.items():
        for text in forms:
            reg.add(text, sem, slots={"X": P.BOUND_KIND[P.SEMS[sem][0]]}, family=FAMILY)
    for p in pieces:
        if p["lint"] or p["meta"]["piece"] not in ("form", "wording"):
            continue
        m = p["meta"]
        try:
            if m["piece"] == "form":
                reg.add(p["value"], m["sem"], slots={"X": P.BOUND_KIND[P.SEMS[m["sem"]][0]]}, source="haiku",
                        family=FAMILY, haiku_task_id=p["task_id"], haiku_prompt_sha=p["haiku_prompt_sha"])
            else:
                reg.add(p["value"], question_sem(FAMILY, m["qform"]), slots=wording_slots(m["qform"]),
                        source="haiku", family=FAMILY, haiku_task_id=p["task_id"],
                        haiku_prompt_sha=p["haiku_prompt_sha"], held_out=m["held_out"])
        except LexiconError:
            continue
    reg.unit_test_all()
    return reg


def pool_skins(pieces: list, reg: LexiconRegistry) -> dict:
    """{skin_id: Skin} for the lint-clean pieces: Mode T skins, Mode F texts (decl and brief from the plan; lexicon_ids
    = the canonical forms they embed), admitted wordings and attack lines. Skin ids are opaque hashes of piece ids."""
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    out = {}
    for p in pieces:
        m, v = p["meta"], p["value"]
        if p.get("lint") or m["piece"] in ("pack", "form"):
            continue
        sid = "T07-" + m["piece"][:4] + "-" + hashlib.sha256(p["piece_id"].encode()).hexdigest()[:12]
        kw = {"haiku_task_id": p["task_id"], "haiku_prompt_sha": p["haiku_prompt_sha"], "held_out": m["held_out"]}
        if m["piece"] == "skin":
            out[sid] = K.make_skin(sid, FAMILY, v, {"STORE": "name"}, register=m["register"], escape=m["escape"], **kw)
        elif m["piece"] == "freeform":
            ids = tuple(form_of[f] for f in m["canon_forms"])
            out[sid] = K.make_skin(sid, FAMILY, v, m["decl"], register=m["register"], author_mode="F",
                                   brief=m["brief"], lexicon_ids=ids, **kw)
        elif m["piece"] == "wording":
            fid = form_of.get(v)
            if fid and reg.status(fid) == "admitted":
                out[sid] = K.make_skin(sid, FAMILY, v, wording_slots(m["qform"]), kind="wording", register="question",
                                       qform=m["qform"], lexicon_ids=(fid,), **kw)
        else:
            out[sid] = K.make_skin(sid, FAMILY, v, {"CUSTOMER": "name"}, kind="attack", register="note", **kw)
    return out


def write_ambiguity_record(points_json: str) -> list:
    """The Haiku ambiguity pass amb:T07, verbatim, next to the G0-lite spec that resolves it (after A38 only)."""
    pts = json.loads(points_json)
    meta = {"task_id": P.T07Plugin.G0_AMBIGUITY_PASS["task_id"], "model": "haiku", "n_points": len(pts),
            "read_g0_sha256": P.T07Plugin.G0_AMBIGUITY_PASS["read_g0_sha256"],
            "points_sha256": hashlib.sha256(points_json.encode()).hexdigest(),
            "resolved_in": "G0_SPEC.md section 6 (H1-H%d, in this order)" % len(pts)}
    return paths.write_files(AMB_ROOT, {"amb_T07_points.json": points_json,
                                        "amb_T07_meta.json": json.dumps(meta, indent=1) + "\n"})


def main() -> int:
    tasks, plan = build_tasks()
    probs = check(tasks)
    if probs:
        print("\n".join(probs))
        return 1
    out, manifest = files(tasks, plan)
    paths.write_files(ROOT, out)              # refuses before A38 and on never-open paths
    for r in manifest["tasks"]:
        print(f"{r['kind']:16s} {r['task']:24s} items {r['n_items']:3d} outputs {r['outputs_expected']:4d} "
              f"{r['task_file']}")
    print(f"{manifest['n_tasks']} tasks, {manifest['outputs_expected']} outputs expected; manifest "
          f"{ROOT / 'TASKS.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
