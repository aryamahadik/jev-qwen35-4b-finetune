"""Card length fitting (section 1 token cap). Every F3 row must stay under 1,900 real tokens on the served prompt,
where a choice row prints the moved card text twice. Cards are therefore kept compact: after the card plan is drawn,
optional features are switched off, in a fixed order, until the yes/no card text is at most CARD_BUDGET tokens.
A switched-off feature removes its trigger from the card (its questions and mechanisms are not generated there), so
every rule the card's rows can trigger is still stated. Deterministic (fixed order, no sampling)."""
from __future__ import annotations

import random

import cards as CARDS
import render_f3 as RF
from f3common import FMT1_DIR, rng_for

CARD_BUDGET = {"choice": 520, "yn": 680, "mixed": 520}
STEPS = ("decision_list", "still", "companion_corr", "qty", "notes", "illus", "companion_void", "q2", "neg", "fewshot")
FEWSHOT_WANT = 7   # 5-10% of 95 cards (spec 2.1; repair r2: G11 found 2/95 after fitting)


def card_tokens(c, tok):
    import sys
    sys.path.insert(0, str(FMT1_DIR))
    from fmt1 import card as fc, pool
    c["_doctype"] = {}
    S = {"n0": 12, "d0": "2040-01-01", "entries": [{"date": "2040-02-02"}]}
    illus = RF.illustrations(c, rng_for("cardtext", c["card_id"])) if c["def_style"] == "one_line_examples" else None
    few = RF.fewshot_block(c, rng_for("cardtext", c["card_id"])) if c.get("fewshot") else None
    ir = RF.card_ir(c, S, qtype="noul", options=None, illus=illus, fewshot=few)
    if ir is None:
        return 0
    best = 0
    for sid in c["styles"][:3]:
        t = fc.render_card(ir, pool.style(sid))
        best = max(best, len(tok(t)["input_ids"]))
    return best


def apply(c, step):
    if step == "illus":
        if c["def_style"] == "one_line_examples":
            c["def_style"] = "one_line"
            return True
    elif step == "still":
        if c.get("still_on"):
            c["still_on"] = False
            return True
    elif step == "companion_void":
        if "VOID" in c["mechs"] and c.get("focus") != "VOID" and c["sampler"] != "S4":
            c["mechs"] = [m for m in c["mechs"] if m != "VOID"]
            if "Q8" in c["qts"] and not (c["check"] or c["lock"]):
                c["qts"] = [q for q in c["qts"] if q != "Q8"]
            return True
    elif step == "companion_corr":
        if c.get("corr_companion") and "CORR" in c["mechs"]:
            c["mechs"] = [m for m in c["mechs"] if m != "CORR"]
            c["corr_companion"] = False
            return True
    elif step == "q2":
        if c.get("q2_on") and c["sampler"] != "S6" and c.get("theme") != "Q2":
            c["q2_on"] = False
            c["qts"] = [q for q in c["qts"] if q != "Q2"]
            return True
    elif step == "qty":
        if c["has_qty"]:
            c["has_qty"] = False
            c["qty"] = c["unit"] = None
            c["mechs"] = [m for m in c["mechs"] if m not in ("SETQ", "ADJUST")]
            return True
    elif step == "decision_list":
        if c["def_style"] in ("decision_list", "rubric_table"):
            c["def_style"] = "one_line"
            return True
    elif step == "notes":
        if c.get("notes_on"):
            c["notes_on"] = False
            return True
    elif step == "fewshot":
        if c.get("fewshot"):
            c["fewshot"] = False
            return True
    elif step == "neg":
        if c.get("neg_on") and c["rule21"] != "short":
            c["neg_on"] = False
            return True
    return False


def fit(cards, tok, budget=None):
    report = {}
    for c in cards:
        budget_c = (budget or CARD_BUDGET)[c.get("form_mode", "mixed")]
        if c.get("inverted") or c.get("roster"):
            budget_c = 400
        n0 = card_tokens(c, tok)
        dropped = []
        n = n0
        for step in STEPS:
            if n <= budget_c:
                break
            if apply(c, step):
                dropped.append(step)
                n = card_tokens(c, tok)
        c["card_tokens"] = n
        report[c["card_id"]] = {"before": n0, "after": n, "dropped": dropped}
    if not any(c.get("dev") or str(c["card_id"]).startswith("F3-dev") for c in cards):
        report["_fewshot"] = ensure_fewshot(cards, tok, budget)
        report["_distinct"] = CARDS.ensure_distinct(cards)
        CARDS.pair_rates_by_capacity(cards)
        report["_yes_rates"] = {c["card_id"]: c["yes_rate"] for c in cards}
    return report


def ensure_fewshot(cards, tok, budget=None, want=FEWSHOT_WANT):
    """Few-shot overlay on 5-10% of cards (spec 2.1). Eligible: full yes/no-oriented cards on S1, S2, S4 or S6 (no
    2.1 card, not inverted). Cards are taken in a fixed hash order; a card is switched to few-shot only if its card
    text with the worked examples still fits its budget (optional features dropped in STEPS order, never a rule)."""
    from f3common import unit_hash
    have = [c for c in cards if c.get("fewshot")]
    added = []
    elig = sorted([c for c in cards if not c.get("fewshot") and c["rule21"] is None and not c.get("inverted")
                   and c["sampler"] in ("S1", "S2", "S4", "S6") and c.get("form_mode") == "yn"
                   and "SUPERSEDE" not in c["mechs"]],   # worked examples parse only entry lines (no register)
                  key=lambda c: unit_hash("fewshot2", c["card_id"]))
    for c in elig:
        if len(have) + len(added) >= want:
            break
        budget_c = (budget or CARD_BUDGET)[c.get("form_mode", "mixed")]
        trial = dict(c)
        trial["fewshot"] = True
        n = card_tokens(trial, tok)
        for step in STEPS[:-1]:
            if n <= budget_c:
                break
            if apply(trial, step):
                n = card_tokens(trial, tok)
        if n <= budget_c:
            c.clear()
            c.update(trial)
            c["card_tokens"] = n
            added.append(c["card_id"])
    return {"kept": [c["card_id"] for c in have], "added": added}
