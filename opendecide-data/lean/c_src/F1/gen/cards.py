"""F1 cards (G0 F1 v7 section 1 "F1 card", 6, 6.2-6.4, 8 card-level targets).

A card = (sampler, pack, outcome schema, world, precedence, instruction family = question type). One pack per card.
Card-level draws are made from ids only (seeded); nothing here reads a row's gold.
"""
from __future__ import annotations

import json
import random
from decimal import Decimal

import lexicon as L
from common import FMT2_DIR, SEED, d2o, rng_for, unit
from packs_f1 import load_all, neg_free, norm_name, split_packs
import datetime as dt

from fmt1 import labels as fl
from fmt1 import pool as fpool

SAMPLER_CARDS = {"S1": 26, "S2": 26, "S3": 22, "S4": 22, "S6": 24}
SAMPLER_ROWS = {"S1": 1725, "S2": 1725, "S3": 1500, "S4": 1500, "S6": 1650}   # 1.5 x kept budgets (section 3)
QTYPE_ROWS = {"Q1": 0.29, "Q2": 0.16, "Q3": 0.47, "Q4": 0.08}
CONTAINERS = {
    "S1": ["prose", "memo", "bullet_sop", "markdown_table", "html_snippet", "json", "yaml"],
    "S2": ["prose", "memo", "bullet_sop", "markdown_table", "html_snippet", "json", "yaml"],
    "S3": ["markdown_table", "html_snippet", "memo", "json", "yaml"],
    "S4": ["memo", "email_thread", "prose"],
    "S6": ["memo", "prose", "markdown_table", "html_snippet", "json", "yaml", "bullet_sop"],
    "S5": ["prose", "memo", "bullet_sop", "markdown_table", "html_snippet", "json", "yaml"],
}
M_NAMES = ["hold for missing details", "return for completion", "pause for missing fields", "send back for details"]
ESC_WORDS = ("refer", "escalate", "send to", "review", "board", "panel", "committee", "manager", "supervisor")
CASE_REF_SCHEMES = ["MS01", "MS03", "MS05", "MS07", "MS10", "MS16", "MS19"]
MASK_SCHEMES = ["MS01", "MS03", "MS05", "MS07", "MS10", "MS12", "MS13", "MS16", "MS19"]
CODE_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"


def wordings():
    rows = [json.loads(l) for l in open(FMT2_DIR / "wordings" / "family_pools.jsonl") if '"pool": "F1"' in l]
    return rows


def plan_cards(n_cards=120, seed_key="plan-r1"):
    """Card specs with the section 1 / 8 card-level shares. Deterministic."""
    rng = rng_for(seed_key)
    specs = []
    for s, n in SAMPLER_CARDS.items():
        for i in range(n):
            specs.append({"sampler": s})
    rng.shuffle(specs)
    # ORDER only on S3: 12 cards (10%)
    s3 = [c for c in specs if c["sampler"] == "S3"]
    for c in s3[:12]:
        c["prim"], c["sec"] = "ORDER", None
    rest = [c for c in specs if "prim" not in c]
    pols = ["SPEC"] * 30 + ["LATER"] * 30 + ["PRIORITY"] * 30 + ["PAIR"] * 18
    rng.shuffle(pols)
    pairs = [("SPEC", "LATER"), ("SPEC", "PRIORITY"), ("LATER", "SPEC"), ("LATER", "PRIORITY"),
             ("PRIORITY", "SPEC"), ("PRIORITY", "LATER")]
    for c, p in zip(rest, pols):
        if p == "PAIR":
            c["prim"], c["sec"] = pairs[rng.randrange(6)]
        else:
            c["prim"], c["sec"] = p, None
    # question types: Q4 15 cards (12.5%, closed), Q3 55, Q1 33, Q2 17
    qts = ["Q4"] * 15 + ["Q3"] * 55 + ["Q1"] * 33 + ["Q2"] * 17
    rng.shuffle(qts)
    for c, q in zip(specs, qts):
        c["qtype"] = q
    # length (section 1, A16.1 g): Q2 rows print the answer group and 10-60 options twice, so Q2 cards are never on
    # the amendment-chain sampler S6 (whose cards always carry notices); swap with a non-S6 Q3 / Q1 card
    for c in specs:
        if c["sampler"] == "S6" and c["qtype"] == "Q2":
            other = next(x for x in specs if x["sampler"] != "S6" and x["qtype"] in ("Q3", "Q1"))
            c["qtype"], other["qtype"] = other["qtype"], "Q2"
    # length: Q2 cards take a single precedence policy (a pair adds rows 29/30/31 + 33 to text printed twice)
    for c in specs:
        if c["qtype"] == "Q2" and c["sec"] is not None:
            other = next((x for x in specs if x["qtype"] != "Q2" and x["sec"] is None and x["prim"] != "ORDER"), None)
            if other is not None:
                (c["prim"], c["sec"]), (other["prim"], other["sec"]) = (other["prim"], other["sec"]), (c["prim"],
                                                                                                    c["sec"])
    # world: closed 60 (incl. every Q4), open 48, missing 12 (missing only on Q2 / Q3 cards; see G0 note in MANIFEST)
    non4 = [c for c in specs if c["qtype"] != "Q4"]
    rng.shuffle(non4)
    for c in specs:
        if c["qtype"] == "Q4":
            c["world"] = "closed"
    miss_pool = [c for c in non4 if c["qtype"] in ("Q2", "Q3")]
    for c in miss_pool[:12]:
        c["world"] = "missing"
    left = [c for c in non4 if "world" not in c]
    # open world on 48 cards; at most 4 of them Q2 (CBD on Q2 rows), the rest Q1 / Q3
    q2l = [c for c in left if c["qtype"] == "Q2"]
    rest = [c for c in left if c["qtype"] != "Q2"]
    for c in q2l[:3]:
        c["world"] = "open"
    for c in q2l[3:]:
        c["world"] = "closed"
    for i, c in enumerate(rest):
        c["world"] = "open" if i < 45 else "closed"
    # short / no-card cards: closed, Q1 or Q3, SPEC/LATER/PRIORITY single policy: 18 cards (~15% of rows)
    cand = [c for c in specs if c["world"] == "closed" and c["qtype"] in ("Q1", "Q3") and c["sec"] is None
            and c["prim"] in ("SPEC", "LATER", "PRIORITY")]
    rng.shuffle(cand)
    for c in specs:
        c["short"] = False
    for c in cand[:18]:
        c["short"] = True
    # definition styles: examples ~50% of all cards, the rest one_line / decision_list
    ns = [c for c in specs if not c["short"]]
    rng.shuffle(ns)
    for i, c in enumerate(ns):
        c["defs"] = "one_line_examples" if i < 60 else ("one_line" if i < 81 else "decision_list")
    for c in specs:
        if c["short"]:
            c["defs"] = "short"
    # few-shot: 8 Q3 cards (non-short)
    q3 = [c for c in specs if c["qtype"] == "Q3" and not c["short"]]
    rng.shuffle(q3)
    for c in specs:
        c["fewshot"] = False
    for c in q3[:8]:
        c["fewshot"] = True
    # label forms on choice cards: masked ~12% / swapped ~5% of choice rows
    ch = [c for c in specs if c["qtype"] in ("Q1", "Q2", "Q4") and not c["short"]]
    rng.shuffle(ch)
    for c in specs:
        c["label_form"] = "plain"
    for c in ch[:8]:
        c["label_form"] = "masked"
    for c in ch[8:11]:
        c["label_form"] = "swapped"
    # xor cards <= 5% (4), never S3 / short
    xs = [c for c in specs if c["sampler"] != "S3" and not c["short"]]
    rng.shuffle(xs)
    for c in specs:
        c["xor"] = False
    for c in xs[:4]:
        c["xor"] = True
    # Q4 none cards ~40%
    q4 = [c for c in specs if c["qtype"] == "Q4"]
    for i, c in enumerate(q4):
        c["none_card"] = i < 6
    for c in specs:
        c.setdefault("none_card", False)
    # tie rule: strictness order on ~40% of non-ORDER cards
    for c in specs:
        c["tie"] = "strict" if (c["prim"] != "ORDER" and rng.random() < 0.4) else "esc"
    # rows per card: fit sampler totals and question-type totals (iterative proportional fitting)
    w = {id(c): 1.0 for c in specs}
    qtot = {q: sum(SAMPLER_ROWS.values()) * f for q, f in QTYPE_ROWS.items()}
    for _ in range(50):
        for s, tot in SAMPLER_ROWS.items():
            cs = [c for c in specs if c["sampler"] == s]
            f = tot / sum(w[id(c)] for c in cs)
            for c in cs:
                w[id(c)] *= f
        for q, tot in qtot.items():
            cs = [c for c in specs if c["qtype"] == q]
            f = tot / sum(w[id(c)] for c in cs)
            for c in cs:
                w[id(c)] *= f
    for i, c in enumerate(specs):
        c["n_rows"] = max(24, int(round(w[id(c)])))
        c["card_id"] = f"F1-C{i + 1:03d}"
    return specs


# ---------------------------------------------------------------- outcome schema

def _pick_outcomes(pack, spec, rng):
    taken = set()
    for a in pack["attrs"]:
        taken.add(norm_name(a["name"]))
        for v in a.get("values", []) or []:
            taken.add(norm_name(v))
    outs = [o for o in pack["outcomes"] if norm_name(o["name"]) not in taken]
    rng.shuffle(outs)
    names = [o["name"] for o in outs]
    tags = {o["name"]: o["tag"] for o in outs}
    esc = next((n for n in names if any(w in n.lower() for w in ESC_WORDS)), None)
    if esc is None:
        roles = [r for r in pack.get("roles") or [] if isinstance(r, str) and neg_free(r)
                 and all(ch.isalnum() or ch in " '-" for ch in r) and len(r) < 30]
        role = roles[0] if roles else (pack.get("deciding_role") or "senior officer")
        esc = f"refer to {role.lower()}"
    need_fb = "onlyif" in spec["constructs"]
    need_M = spec["world"] == "missing"
    others = [n for n in names if n != esc]
    if spec["qtype"] == "Q1":
        lo, hi = (3, 4) if spec.get("k_small") else (5, 8)
        if spec["world"] == "open":
            lo, hi = max(lo - 1, 3), min(hi - 1, 7)
    else:
        lo, hi = 3, 6
    n_out = rng.randint(lo, hi)
    base_need = 2 + (1 if need_fb else 0) + (1 if need_M else 0)
    n_out = max(n_out, base_need + 1)
    chosen = [esc]
    M = None
    if need_M:
        M = next(m for m in M_NAMES if all(norm_name(m) not in norm_name(x) and norm_name(x) not in norm_name(m)
                                           for x in names + [esc]))
        chosen.append(M)
    for n in others:
        if len(chosen) >= n_out:
            break
        if any(f" {norm_name(n)} " in f" {norm_name(x)} " or f" {norm_name(x)} " in f" {norm_name(n)} "
               for x in chosen):
            continue
        chosen.append(n)
    if len(chosen) < base_need + 1:
        return None
    default = next(n for n in chosen if n not in (esc, M))
    fallback = None
    if need_fb:
        fallback = next(n for n in chosen if n not in (esc, M, default))
    roles = {}
    for n in chosen:
        roles[n] = ("escalate" if n == esc else "M" if n == M else "default" if n == default
                    else "fallback" if n == fallback else "other")
    val = {}
    for n in chosen:
        if n in (esc, M):
            val[n] = "bad"
        else:
            t = tags.get(n)
            val[n] = t if t in ("good", "bad") else ("good" if rng.random() < 0.5 else "bad")
    rng.shuffle(chosen)
    return {"outcomes": chosen, "roles": roles, "valence": val, "default": default, "escalate": esc,
            "fallback": fallback, "M": M}


# ---------------------------------------------------------------- construct sets

def draw_constructs(spec, pack, rng):
    s = spec["sampler"]
    cs = set()
    types = {a["type"] for a in pack["attrs"]}
    numops = ["ge", "gt", "le", "lt", "between"]
    rng.shuffle(numops)
    k = rng.randint(2, 4)
    for op in numops[:k]:
        cs.add("num_" + op)
    dates = sum(1 for a in pack["attrs"] if a["type"] == "date")
    if dates >= 2 and rng.random() < 0.6:
        dops = ["before", "onbefore", "after", "onafter", "fromto"]
        rng.shuffle(dops)
        for op in dops[:rng.randint(1, 3)]:
            cs.add("date_" + op)
    if any(a.get("daycount") for a in pack["attrs"]) and rng.random() < 0.5:
        cs.add("within")
    if "cat" in types:
        cs.update(rng.sample(["cat_in1", "cat_notin1", "cat_in", "cat_notin"], rng.randint(1, 3)))
    if "bool" in types:
        cs.add("bool_true")
        if any(a["type"] == "bool" and a.get("false") for a in pack["attrs"]) and rng.random() < 0.6:
            cs.add("bool_false")
    if spec["short"]:
        # plain subset (6.2): comparators at least / more than / at most / less than / dates; or-both; pure exceptions
        cs = {c for c in cs if c in ("num_ge", "num_gt", "num_le", "num_lt", "date_before", "date_onbefore",
                                     "date_after", "date_onafter", "cat_in1", "cat_notin1", "cat_in", "cat_notin",
                                     "bool_true", "bool_false")}
        if not any(c.startswith("num_") for c in cs):
            cs.add("num_ge")
        if rng.random() < 0.3:
            cs.add("or")
        if rng.random() < 0.4 and s != "S3":
            cs.add("pexc_short")
        if s == "S6" or rng.random() < 0.5:
            cs.add("notices")
            cs.update(rng.sample(["insert", "repeal"], rng.randint(1, 2)))
        return cs
    if s == "S3":
        pass  # tables: conjunction cells only (no exceptions, only if, groups, lists, unless)
    else:
        if rng.random() < 0.55:
            cs.add("unless")
        if spec.get("xor"):
            cs.add("xor")
        elif rng.random() < 0.35:
            cs.add("or")
        lk = [x for x in ("all", "any", "kofn") if rng.random() < (0.3 if x != "kofn" else 0.15)]
        cs.update(lk)
        if rng.random() < 0.65:
            cs.add("exc")
            if rng.random() < 0.4:
                cs.add("exc2")
        if rng.random() < 0.35:
            cs.add("onlyif")
    if s == "S6" or rng.random() < 0.6:
        cs.add("notices")
        nt = ["replace", "repeal", "insert"]
        rng.shuffle(nt)
        cs.update(nt[:rng.randint(1, 3)] if s != "S6" else nt[:rng.randint(2, 3)])
        if rng.random() < 0.35:
            cs.add("last")
    elif rng.random() < 0.2:
        cs.add("last")
    if s in ("S4", "S1", "S2", "S6") and rng.random() < (0.85 if s == "S4" else 0.25):
        cs.add("inert")
    return cs


def statement_rows(card) -> list:
    """Section 6 rows the card shows (section 1 construct set; policy rows), in a fixed reading order."""
    cs, w, q = card["constructs"], card["world"], card["qtype"]
    if card["short"]:
        return []
    rows = []
    if w == "closed":
        rows.append(1)
    elif w == "open":
        rows += ["2a"] + (["2cbd"] if q in ("Q1", "Q2") else []) + (["2yn"] if q == "Q3" else [])
    else:
        rows += [1, 3]
    rows.append(4)
    if w == "open" and q in ("Q1", "Q2"):
        rows.append(38)
    rows.append(39)
    rows.append(40)
    if q == "Q2":
        rows.append("41h")
        rows += [f"41{c}" for c in card["codes_defined"]]
    if q == "Q4":
        rows.append(43)
        if card["none_card"]:
            rows.append("43n")
    rows.append(45)
    rows.append(5)
    if "unless" in cs:
        rows.append(6)
    if "onlyif" in cs:
        rows.append(7)
    for op, r in (("num_ge", 8), ("num_le", 9), ("num_gt", 10), ("num_lt", 11), ("num_between", 12)):
        if op in cs:
            rows.append(r)
    if "or" in cs:
        rows.append(13)
    if "xor" in cs:
        rows.append("13x")
    if cs & {"all", "any", "kofn"}:
        rows.append(14)
    if cs & {"cat_in1", "cat_notin1", "cat_in", "cat_notin"}:
        rows.append(15)
    if any(c.startswith("date_") for c in cs):
        rows.append(16)
    if "within" in cs:
        rows.append(18)
    if "notices" in cs or "last" in cs:
        rows.append(19)
    if "notices" in cs:
        rows += [20, 21]
        if "replace" in cs:
            rows.append(22)
            if "PRIORITY" in (card["prim"], card["sec"]):
                rows.append("22p")
        if "insert" in cs:
            rows.append(23)
    if "repeal" in cs or "last" in cs:
        rows.append(24)
    if "inert" in cs:
        rows.append(25)
    if "exc" in cs:
        rows.append(26)
    if card["prim"] != "ORDER":
        rows.append(27)
    rows.append(28)
    for p in (card["prim"], card["sec"]):
        if p == "SPEC":
            rows.append(29)
        elif p == "LATER":
            rows.append(30)
        elif p == "PRIORITY":
            rows.append(31)
        elif p == "ORDER":
            rows.append(32)
    if card["sec"]:
        rows.append(33)
    if card["prim"] != "ORDER":
        rows.append("34e" if card["tie"] == "esc" else "34s")
    rows.append(35)
    rows.append(36)
    rows.append(37)
    if "notices" in cs or "inert" in cs:
        rows.append(42)
    return rows


ANSWER_ROWS = {1, "2a", "2cbd", "2yn", 3, 4, 38, 39, 40, "41h", "41D", "41T", "41F", "41M", 43, "43n"}


def fill_statement(card, row) -> str:
    v = L.STATEMENTS[row]
    idx = card["stmt_variant"].get(str(row), 0) % len(v)
    t = v[idx]
    f = card["forms"]
    disp = card["display"]
    prim_name = L.POLICY_NAMES.get(card["prim"], "")
    last = card["sec"] or card["prim"]
    tiers = card["tiers"]
    chain = ", which override ".join(f"{t} tier" for t in tiers)
    tier_chain = (f"{tiers[0]} tier rules override {tiers[1]} tier rules" +
                  "".join(f", which override {x} tier rules" for x in tiers[2:])) if tiers else ""
    vals = {
        "subj": card["subj"], "fields_title": card["titles"]["fields"], "cbd": card["cbd_label"],
        "M": disp.get(card["M"], card["M"]) if card["M"] else "", "listed": ", ".join(card["listed_names"]),
        "fallback": disp.get(card["fallback"], card["fallback"]) if card["fallback"] else "",
        "op": "", "lb": f["cat_br"][0], "rb": f["cat_br"][1],
        "before": f.get("date_before", "is before")[3:], "after": f.get("date_after", "is after")[3:],
        "onbefore": f.get("date_onbefore", "is on or before")[3:], "onafter": f.get("date_onafter", "is on or after")[3:],
        "fromto": "from",
        "gov": card["gov_name"], "body": card["body"], "other_scope": card.get("other_scope_text", ""),
        "tier_chain": tier_chain, "prim_name": prim_name,
        "sec_sentence": L.SEC_SENTENCES.get(card["sec"] or "", ""),
        "last_name": L.POLICY_NAMES.get(last, ""), "escalate": disp.get(card["escalate"], card["escalate"]),
        "strict_list": ", ".join(disp.get(x, x) for x in card["strict"]),
        "default": disp.get(card["default"], card["default"]),
        "code_D": card["codes"].get("D", ""), "code_T": card["codes"].get("T", ""),
        "code_F": card["codes"].get("F", ""), "code_M": card["codes"].get("M", ""), "none": card["none_label"],
    }
    if row in (8, 9, 10, 11, 12):
        op = {8: "num_ge", 9: "num_le", 10: "num_gt", 11: "num_lt", 12: "num_between"}[row]
        vals["op"] = f[op][3:]  # drop the leading "is "
    if row == 16 and "date_fromto" not in card["constructs"]:
        pass
    return t.format(**vals)


def card_statements(card):
    out = []
    for r in statement_rows(card):
        out.append((r, "answer" if r in ANSWER_ROWS else "policy", fill_statement(card, r)))
    return out


# ---------------------------------------------------------------- card build

def build_card(spec, pack, held_out=False):
    rng = rng_for("card", spec["card_id"], pack["pack_id"])
    card = dict(spec)
    card["pack_id"] = pack["pack_id"]
    card["persona_seed"] = pack.get("persona_seed")
    card["constructs"] = draw_constructs(spec, pack, rng)
    if spec["sampler"] == "S3" and spec["prim"] == "ORDER":
        card["tie"] = "esc"
    if spec["short"]:
        card["tie"] = "none"   # 6.2: no tie can arise on short / no-card rows; the card states no tie rule
    if spec["qtype"] == "Q1":
        card["k_small"] = unit("ksmall", spec["card_id"]) < 0.5
    sch = _pick_outcomes(pack, card, rng)
    if sch is None:
        return None
    card.update(sch)
    if card["tie"] == "strict":
        st = list(card["outcomes"])
        rng.shuffle(st)
        card["strict"] = st
    else:
        card["strict"] = []
    subj = pack["subject"]["noun"] or "case"
    card["subj"] = subj
    # core attributes: governing-date field; missing-field listed fields (non-Boolean)
    dates = [a for a in pack["attrs"] if a["type"] == "date"]
    gov = rng.choice(dates)
    card["gov_key"] = gov["key"]
    card["gov_name"] = gov["name"]
    nonbool = [a for a in pack["attrs"] if a["type"] in ("num", "cat") and a["key"] != gov["key"]]
    # illustration sub-pool (6.4 rule 5): one numeric, one category, one bool field reserved; no row draws them
    reserve = []
    if spec["defs"] == "one_line_examples":
        nums = [a for a in pack["attrs"] if a["type"] == "num" and not a.get("daycount")]
        cats = [a for a in pack["attrs"] if a["type"] == "cat"]
        bools = [a for a in pack["attrs"] if a["type"] == "bool" and not a.get("presup")]
        others_dates = [a for a in dates if a["key"] != gov["key"]]
        for grp in (nums, cats, bools, others_dates):
            if len(grp) >= 2:
                reserve.append(rng.choice(grp)["key"])
        if len([a for a in nums if a["key"] not in reserve]) < 2:
            reserve = [k for k in reserve if k not in {a["key"] for a in nums}]
    card["illus_keys"] = reserve
    if spec["world"] == "missing":
        cand = [a for a in nonbool if a["key"] not in reserve]
        rng.shuffle(cand)
        card["listed_keys"] = [a["key"] for a in cand[:rng.randint(1, min(3, len(cand)))]]
        card["listed_names"] = [next(a["name"] for a in pack["attrs"] if a["key"] == k) for k in card["listed_keys"]]
    else:
        card["listed_keys"], card["listed_names"] = [], []
    # surface forms: one per operator class
    f = {}
    for op, forms in L.NUM_FORMS.items():
        f["num_" + op] = rng.choice(forms)
    for op, forms in L.DATE_FORMS.items():
        f["date_" + op] = rng.choice(forms)
    if spec["short"]:
        f["num_ge"], f["num_le"], f["num_gt"], f["num_lt"] = "is at least", "is at most", "is more than", "is less than"
        f["date_onbefore"], f["date_onafter"] = "is on or before", "is on or after"
    f["cat_br"] = rng.choice(L.CAT_BRACKETS)
    f["list_br"] = L.LIST_BRACKETS[f["cat_br"]]
    f["rule_noun"] = rng.choice(L.RULE_NOUNS)
    f["notice_noun"] = rng.choice(L.NOTICE_NOUNS)
    f["date_form"] = rng.choice(L.DATE_FORMS_DISPLAY)
    f["q1_frame"] = rng.randrange(len(L.Q1_FRAMES))
    f["q2_frame"] = rng.randrange(len(L.Q2_FRAMES))
    f["q4_frame"] = rng.randrange(len(L.Q4_FRAMES))
    f["q2_sep"] = rng.choice(L.Q2_SEPS)
    if spec["sampler"] == "S3":
        f["rule_noun"] = L.ROW_NOUN
    card["forms"] = f
    card["titles"] = {"fields": rng.choice(L.FIELDS_TITLES) if spec["world"] != "open" else L.POSSIBLE_TITLES[0],
                      "interp": rng.choice(L.INTERP_TITLES), "rules": rng.choice(L.RULES_TITLES),
                      "notices": rng.choice(L.NOTICES_TITLES), "case": rng.choice(L.CASE_TITLES),
                      "cases": rng.choice(L.CASES_TITLES)}
    card["cbd_label"] = rng.choice(L.CBD_LABELS)
    card["none_label"] = rng.choice(L.NONE_LABELS)
    # special basis codes (Q2): fixed-width 3-letter codes, never a masked id or rule id
    codes_defined = ["D"]
    if card["prim"] != "ORDER":
        codes_defined.append("T")
    if "onlyif" in card["constructs"]:
        codes_defined.append("F")
    if card["world"] == "missing":
        codes_defined.append("M")
    card["codes_defined"] = codes_defined if spec["qtype"] == "Q2" else []
    letters = list(CODE_LETTERS)
    codes = {}
    used = set()
    for c in ["D", "T", "F", "M"]:
        while True:
            x = "code " + "".join(rng.choice(letters) for _ in range(3))
            if x not in used:
                used.add(x)
                codes[c] = x
                break
    card["codes"] = {c: codes[c] for c in card["codes_defined"]}
    card["case_ref_scheme"] = (rng.choice(["IVN01", "IVN02", "IVN03", "IVN04", "IVN05", "IVN06", "IVN07", "IVN08"]),
                               rng.choice(CASE_REF_SCHEMES))
    # display names (masked / swapped on choice cards only)
    disp = {o: o for o in card["outcomes"]}
    if spec["label_form"] == "masked":
        sc = rng.choice(MASK_SCHEMES)
        ids = fl.masked_ids(sc, len(card["outcomes"]), f"F1|{spec['card_id']}")
        disp = dict(zip(card["outcomes"], ids))
        card["mask_scheme"] = sc
    elif spec["label_form"] == "swapped":
        try:
            words = fl.swapped_names("mixed", len(card["outcomes"]), f"F1|{spec['card_id']}",
                                     natural_names=list(card["outcomes"]), exclude=[card["cbd_label"], subj])
        except Exception:
            words = None
        if words is None or any(not neg_free(w) for w in words):
            card["label_form"] = "plain"
        else:
            disp = dict(zip(card["outcomes"], words))
    card["display"] = disp
    # outcome meanings (row 46): card-defined; valence follows the meaning
    gm, bm = list(L.GOOD_MEANINGS), list(L.BAD_MEANINGS)
    rng.shuffle(gm)
    rng.shuffle(bm)
    gi = bi = 0
    mean = {}
    extra_g = ["good news for the {subj}", "the {subj} is cleared", "the {subj} gets what it seeks"]
    extra_b = ["bad news for the {subj}", "the {subj} is stopped for now", "the {subj} is sent back"]
    gm += extra_g
    bm += extra_b
    for o in card["outcomes"]:
        if card["valence"][o] == "good":
            mean[o] = gm[gi % len(gm)].format(subj=subj)
            gi += 1
        else:
            mean[o] = bm[bi % len(bm)].format(subj=subj)
            bi += 1
    card["meanings"] = mean
    # tiers (PRIORITY)
    tier_sets = [["senior", "standard", "local"], ["primary", "secondary", "tertiary"], ["gold", "silver", "bronze"],
                 ["first", "second", "third"], ["upper", "middle", "lower"]]
    card["tiers"] = rng.choice(tier_sets) if "PRIORITY" in (card["prim"], card["sec"]) else []
    card["body"] = pack["org"]
    obs = [o for o in pack.get("orgs") or [] if isinstance(o, str) and o != pack["org"] and neg_free(o)
           and all(ch.isalnum() or ch in " '-&." for ch in o)]
    card["other_bodies"] = obs[:4] or [f"the {subj} users' forum"]
    sc = pack.get("scope") or None
    attr_names = {norm_name(a["name"]) for a in pack["attrs"]}
    if sc and (norm_name(sc.get("name", "")) in attr_names or not neg_free(sc.get("name", "x"))
               or any(not neg_free(v) or any(ch in v for ch in ".;:,()[]") for v in sc.get("values", []))):
        sc = None
    if sc and sc.get("values") and len(sc["values"]) >= 2:
        card["scope"] = (sc["name"], sc["values"][0], sc["values"][1:])
    else:
        card["scope"] = ("office", "main office", ["branch office", "field office"])
    card["other_scope_text"] = f"any {card['scope'][0]} that is not {card['scope'][1]}"
    card["stmt_variant"] = {str(k): rng.randrange(4) for k in L.STATEMENTS}
    # base date B (policy effective date) inside the pack window
    lo, hi = pack["date_window"]
    card["B"] = lo + rng.randint(60, max(61, (hi - lo) // 3))
    card["window"] = (lo, hi)
    # wordings (>= 5 per card): form-compatible entries of the formats-2 F1 pool
    ws = wordings()
    if spec["qtype"] == "Q3":
        pool_w = [w for w in ws if w["forms"][0] in ("any", "yn")]
    elif spec["qtype"] == "Q4":
        pool_w = [w for w in ws if w["forms"][0] == "any" and "this case" not in w["text"]
                  and "the case" not in w["text"]]
    else:
        pool_w = [w for w in ws if w["forms"][0] in ("any", "choice")]
    pool_w.sort(key=lambda w: unit("wd", spec["card_id"], w["id"]))
    if spec["qtype"] in ("Q1", "Q2", "Q4"):
        # choice rows print the wording twice (A16.1): choice cards draw from the shorter half of the pool
        pool_w = sorted(pool_w, key=lambda w: w["n_words"])[: max(10, len(pool_w) // 2)]
        pool_w.sort(key=lambda w: unit("wd", spec["card_id"], w["id"]))
    card["wordings"] = [w["id"] for w in pool_w[:6]]
    card["wording_text"] = {w["id"]: w["text"] for w in pool_w[:6]}
    # format styles: a fixed subset of the sampler's containers (training styles; S5 uses dev styles)
    cont = CONTAINERS[spec["sampler"]]
    if held_out:
        cands = [s for s in fpool.styles(held_out=True) if s["container"] in cont]
    else:
        cands = [s for s in fpool.styles() if s["container"] in cont]
    if spec["world"] == "open" or spec["sampler"] == "S4":
        pass
    card["style_pool"] = [s["id"] for s in fpool.card_style_set(cands, 10, "F1", spec["card_id"])]
    card["yes_rate"] = 0.2 + 0.6 * unit("yesrate", spec["card_id"]) if spec["qtype"] == "Q3" else None
    card["held_out"] = held_out
    return card


def assign_packs(specs, train_ids):
    """One pack per card (XF09): spread over the four pack builders, deterministic."""
    allp = load_all()
    by_agent = {}
    for pid in train_ids:
        by_agent.setdefault(allp[pid]["agent"], []).append(pid)
    for a in by_agent:
        by_agent[a].sort(key=lambda p: unit("packorder", p))
    order = []
    agents = sorted(by_agent)
    i = 0
    while any(by_agent.values()):
        a = agents[i % len(agents)]
        if by_agent[a]:
            order.append(by_agent[a].pop(0))
        i += 1
    return order


# ---------------------------------------------------------------- length budget for the card text (section 1 fit)

_TOK = None


def ntok(s: str) -> int:
    global _TOK
    if _TOK is None:
        import emit
        _TOK = emit.tokenizer()
    return len(_TOK(s or "", add_special_tokens=False)["input_ids"])


BUDGET = {"Q3": 700, "Q1": 780, "Q4": 760, "Q2": 520}
# F1-core constructs (exceptions, only if, unless, groups and lists, amendments, last-applicable dates, inert text) are
# never dropped for length: F1's skill is policy composition. Only redundant operator forms are dropped.
CORE = {"exc", "exc2", "pexc_short", "onlyif", "unless", "or", "xor", "all", "any", "kofn", "notices", "replace",
        "insert", "repeal", "last", "inert"}
DROP_ORDER = ["within", "date_fromto", "date_before", "date_after", "date_onbefore", "date_onafter", "cat_notin1",
              "cat_in1", "num_between", "num_lt", "num_gt"]


def card_text_tokens(card) -> int:
    st = card_statements(card)
    ans = sum(ntok(t) for r, g, t in st if g == "answer")
    pol = sum(ntok(t) for r, g, t in st if g == "policy")
    mean = sum(ntok(f"{card['display'][o]}: {card['meanings'][o]}") for o in card["outcomes"])
    ill = sum(ntok(x) for v in (card.get("illus") or {}).values() for x in v)
    ill += sum(ntok(x["case"]) + 4 for x in (card.get("few_cases") or []))
    if card["qtype"] == "Q3":
        return ans + pol + mean + ill
    if card["qtype"] == "Q1":
        return 2 * ans + pol + mean + ill
    return 2 * (ans + mean) + pol + ill


def fit_constructs(card, pack):
    """Drop optional constructs (fixed order) until the card text fits its budget; S6 keeps one notice type."""
    budget = BUDGET[card["qtype"]]
    cs = set(card["constructs"])
    for c in DROP_ORDER:
        if card_text_tokens(card) <= budget:
            break
        if c not in cs:
            continue
        if card["sampler"] == "S6" and c in ("notices",):
            continue
        if card["sampler"] == "S6" and c in ("replace", "insert", "repeal") and \
                len(cs & {"replace", "insert", "repeal"}) <= 1:
            continue
        if c.startswith("num_") and len([x for x in cs if x.startswith("num_")]) <= 1:
            continue
        if c == "notices":
            cs -= {"notices", "replace", "insert", "repeal", "last"}
        elif c == "exc":
            cs -= {"exc", "exc2", "pexc_short"}
        else:
            cs.discard(c)
        card["constructs"] = cs
    if "exc" not in cs:
        cs.discard("exc2")
    if not ({"replace", "insert", "repeal"} & cs):
        cs.discard("notices")
    card["constructs"] = cs
    return card_text_tokens(card)
