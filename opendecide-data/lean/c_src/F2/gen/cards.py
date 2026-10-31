"""Card planning (3.7): one card per pack (SC4b), card_id = (F2, sampler, pack, schema, instruction family), one rule
set per card, at most 2 planned flip variants, definition style, short-card omissions, wordings (>= 5 from the
formats-2 F2 pool), a fixed per-card set of format styles (training styles for training cards, held-out styles for S5
and sweep items)."""
from __future__ import annotations

import json
from decimal import Decimal

from . import mcard
from .common import FMT2, D, ONE, read_jsonl, rng_for, uhash
from .render import fpool, flabels, fcard

F2_CONTAINERS = ("prose", "memo", "email_thread", "key_value", "json", "yaml", "csv", "markdown_table",
                 "html_snippet", "bullet_sop")
TABLE_OK = ("memo", "csv", "markdown_table", "html_snippet")


def wording_pool():
    rows = [r for r in read_jsonl(FMT2 / "wordings" / "family_pools.jsonl") if r["family"] == "F2"]
    return rows


def pick_wordings(rng, qtype):
    pool = wording_pool()
    form = "yn" if qtype == "noul" else "choice"
    ok = [w for w in pool if w["forms"] == ["any"] or form in w["forms"]]
    rng.shuffle(ok)
    return [w["id"] for w in ok[:rng.randint(5, 7)]]


def wording_text(wid, gb=False):
    for w in wording_pool():
        if w["id"] == wid:
            return w["text_gb"] if gb else w["text"]
    raise KeyError(wid)


def style_set(rng, card_key, held_out, need_table, k=8):
    sts = fpool.styles(held_out=held_out)
    sts = [s for s in sts if s["container"] in F2_CONTAINERS and s["skin"] not in ("json.lines", "json.array")]
    if need_table:
        sts = [s for s in sts if s["container"] in TABLE_OK]
    sel = fpool.card_style_set(sts, k, "F2", card_key)
    return [s["id"] for s in sel]


DV_BY_STYLE = {"one_line": ["DV01", "DV02", "DV03", "DV04", "DV05", "DV06"],
               "one_line_examples": ["DV11", "DV12", "DV13", "DV14", "DV15", "DV16"],
               "decision_list": ["DV31", "DV33", "DV35"],
               "short": ["DV01", "DV02", "DV03", "DV05"]}

TASKS = ["Work out the {res} for the {ent} in the text under these rules.",
         "Apply these rules to the {ent} in the text.",
         "Use these rules to settle the question about the {ent} in the text."]
TITLES = ["{org}: charging rules", "Rules for {ent_pl}", "{org} rate rules", None, None]
REC_LABELS = ["Record", "Case details", "Details"]
SCHED_LABELS = ["Schedule", "Rates and limits", "Price list", "Tariff"]


def common_card(card, pack, rng):
    """Fields every F2 card carries, whatever its engine."""
    card["pack"] = pack["id"]
    card["persona_seed"] = pack.get("persona")
    card["ent_sg"] = pack["ent_sg"]
    card["ent_pl"] = pack["ent_pl"]
    card["prefix"] = pack["prefix"]
    card["idw"] = 4
    card["side_money"] = "pays" if pack["side_money"] == "pays" else "paid"
    card["side_date"] = pack["side_date"]
    card["org"] = pack["org"]
    card["doc_title"] = rng.choice(pack["docs"]).strip().capitalize()
    card["rec_label"] = rng.choice(REC_LABELS)
    card["sched_label"] = rng.choice(SCHED_LABELS)
    card["cases_caption"] = rng.choice(["Cases", "Case list", "Cases to compare"])
    t = rng.choice(TITLES)
    card["title"] = t.format(org=pack["org"], ent_pl=pack["ent_pl"]) if t else None
    card["rules_heading"] = rng.choice([None, "Rules", "How amounts are worked out"])
    qtype = "noul" if card["schema"] in ("YN-T", "YN-D") else "choice"
    card["qtype"] = qtype
    card["wordings"] = pick_wordings(rng, qtype)
    card["gb"] = rng.random() < 0.3
    card["yes_rate"] = rng.uniform(0.2, 0.8)
    card["nei"] = rng.choice(["Cannot be determined", "Not enough information", "Cannot tell from the record"])
    return card


def case_ref_fn(card):
    ref_id = card["case_ref_id"]

    def fn(n, rng):
        key = f"{card['card_id']}:{rng.random()}"
        return fcard.case_refs(ref_id, n, key, scheme=card.get("case_scheme", "MS10"))
    return fn
