"""F3 task cards: one card = (family, sampler, domain pack, label schema, instruction family). One pack per card (XF09,
R1-11). Each card fixes its toggles (world, gap style, rename mode, transfer check, lock rule, times, date format,
listing order, status vocabulary), its mechanism set, its question-type set, its definition style and its style and
wording sets. The card text states every T rule whose trigger can occur on the card (section 2), except on 2.1 short
cards (one triggered rule left out) and no-card rows.
"""
from __future__ import annotations

import json
import random
import re
import sys

import registry as R
from f3common import (FMT1_DIR, FMT2_DIR, GAP_MARKERS, NEI_WORDINGS, NONE_WORDINGS, rng_for, unit_hash)
from packs_f3 import heldout_packs, lint_value, training_packs

sys.path.insert(0, str(FMT1_DIR))
from fmt1 import labels as fmt1_labels  # noqa: E402
from fmt1 import pool as fmt1_pool  # noqa: E402

# containers by encoding
SENT_CONTAINERS = ("prose", "memo", "bullet_sop", "log_lines", "json", "yaml")
REC_CONTAINERS_S1 = ("key_value", "json", "yaml")
REC_CONTAINERS_S3 = ("markdown_table", "html_snippet", "json", "yaml", "key_value", "memo")
NOTICE_CONTAINERS = ("email_thread", "chat_log", "memo", "prose", "bullet_sop")
NOCARD_CONTAINERS = ("prose", "bullet_sop", "memo", "log_lines")
OK_SKINS_REC = {"memo": ("memo.internal",), "markdown_table": ("md.pipes", "md.aligned", "md.headed", "md.bold_caption"),
                "html_snippet": ("html.pretty", "html.compact", "html.div_wrapped"),
                "json": ("json.pretty2", "json.pretty4", "json.compact"),
                "yaml": ("yaml.block", "yaml.indented", "yaml.flow_rows", "yaml.comment_title"),
                "key_value": ("kv.colon", "kv.equals", "kv.ini", "kv.aligned_colon", "kv.dots")}
OK_SKINS_SENT = {"prose": ("prose.plain", "prose.titled_caps", "prose.lines"),
                 "memo": ("memo.classic", "memo.notice", "memo.internal", "memo.briefing"),
                 "bullet_sop": ("sop.numbered", "sop.stars", "sop.dots", "sop.nested"),
                 "log_lines": ("log.iso", "log.bracket", "log.logfmt", "log.pipe", "log.dayfirst"),
                 "json": ("json.pretty2", "json.pretty4", "json.compact"),
                 "yaml": ("yaml.block", "yaml.indented", "yaml.comment_title")}
OK_SKINS_NOTICE = {"email_thread": ("email.oldest_blocks", "email.digest"),
                   "chat_log": ("chat.plain", "chat.angle"),
                   "memo": ("memo.classic", "memo.notice", "memo.briefing"),
                   "prose": ("prose.plain", "prose.lines"), "bullet_sop": ("sop.numbered", "sop.stars", "sop.dots")}
HELDOUT_SKINS_GIT = ("log.tabbed", "log.logfmt", "prose.section_signs", "prose.numbered_paras", "memo.circular",
                     "memo.classic", "sop.parens", "sop.stars")


def _styles_for(container_skins: dict, held_out=False):
    out = []
    for s in fmt1_pool.styles(held_out=held_out):
        if s["container"] in container_skins and s["skin"] in container_skins[s["container"]]:
            out.append(s)
    return out


def _wordings():
    rows = [json.loads(l) for l in open(FMT2_DIR / "wordings" / "family_pools.jsonl", encoding="utf-8")]
    return [r for r in rows if r["family"] == "F3"]


WORDINGS = {w["id"]: w for w in _wordings()}


def wording_text(wid, locale="US"):
    w = WORDINGS[wid]
    return w["text_gb"] if locale == "GB" and w.get("text_gb") else w["text"]


def _swap_words():
    out = []
    for w in fmt1_pool.swap_words():
        if not w["ordered"] and w["group"] in ("status", "colour", "animal", "plant", "material", "weather") \
                and lint_value(w["word"], kind="status") is None:
            out.append(w["word"])
    return sorted(set(out))


# ------------------------------------------------------------------------------------------------ card plan

def _plan_slots():
    """95 training cards: (sampler, kind, theme, mode). kind: regular | open | inverted | short | nocard.
    theme = the card's primary question type (it takes about 70% of the card's base rows); mode: the card's decision
    form (choice cards print their rules twice on every row, so cards are choice- or yes/no-oriented; coin = drawn)."""
    P = []
    P += [("S1", "inverted", "Q7", "choice")] * 4
    P += [("S1", "open", "Q4o", "yn")] * 4 + [("S1", "open", "Q1o", "choice")] * 2 + [("S1", "open", "Q5o", "choice")]
    P += [("S1", "short", "Q4", "yn"), ("S1", "short", "Q2", "yn"), ("S1", "short", "Q1", "yn")]
    P += [("S1", "nocard", "Q1", "choice"), ("S1", "nocard", "Q2", "yn"), ("S1", "nocard", "Q4", "yn")]
    P += [("S1", "regular", "Q3", "coin"), ("S1", "regular", "Q3", "coin"), ("S1", "regular", "Q8", "yn"),
          ("S1", "regular", "Q2", "choice")]
    P += [("S2", "inverted", "Q7", "choice")] * 4
    P += [("S2", "open", "Q4o", "yn")] * 4 + [("S2", "open", "Q1o", "choice")] * 2 \
        + [("S2", "open", "Q5o", "choice")] * 2
    P += [("S2", "regular", "Q3", "coin")] * 5 + [("S2", "regular", "Q8", "yn")] * 2 \
        + [("S2", "regular", "Q6", "yn")] * 2 + [("S2", "regular", "Q1", "coin"), ("S2", "regular", "Q5", "choice"),
                                                 ("S2", "regular", "Q4", "yn")]
    P += [("S3", "inverted", "Q7", "choice")] * 4
    P += [("S3", "open", "Q1o", "choice")] * 2 + [("S3", "open", "Q5o", "choice")] * 2 \
        + [("S3", "open", "Q1", "yn")] * 3
    P += [("S3", "regular", "Q5", "choice")] * 4 + [("S3", "regular", "Q2", "coin")] * 3 \
        + [("S3", "regular", "Q6", "yn")] * 3
    P += [("S4", "open", "Q4o", "yn")] * 3 + [("S4", "open", "Q1o", "choice")] * 2 + [("S4", "open", "Q5o", "choice")]
    P += [("S4", "short", "Q3", "yn"), ("S4", "short", "Q4", "yn"), ("S4", "short", "Q1", "yn")]
    P += [("S4", "nocard", "Q3", "coin"), ("S4", "nocard", "Q4", "yn"), ("S4", "nocard", "Q5", "choice")]
    P += [("S4", "regular", "Q3", "coin")] * 4 + [("S4", "regular", "Q8", "yn")] * 2
    P += [("S6", "regular", "Q2", "coin")] * 9 + [("S6", "regular", "Q4", "yn"), ("S6", "regular", "Q1", "coin")]
    assert len(P) == 95, len(P)
    return P


THEME_QTS = {"Q1": {"yn": ["Q1", "Q4"], "choice": ["Q1", "Q5"]}, "Q2": {"yn": ["Q2", "Q1"], "choice": ["Q2", "Q1"]},
             "Q3": {"yn": ["Q3", "Q1"], "choice": ["Q3", "Q1"]}, "Q4": {"yn": ["Q4", "Q1"]},
             "Q5": {"choice": ["Q5", "Q1"]}, "Q6": {"yn": ["Q6", "Q1"]}, "Q7": {"choice": ["Q7"]},
             "Q8": {"yn": ["Q8", "Q4"]}, "Q1o": {"choice": ["Q1", "Q5"]}, "Q5o": {"choice": ["Q5", "Q1"]},
             "Q4o": {"yn": ["Q4", "Q1"]}}


def _doc_prefixes(doc_types):
    out = []
    for d in doc_types:
        w = re.findall(r"[A-Za-z]+", d)
        p = "".join(x[0] for x in w).upper()[:2]
        if len(p) < 2:
            p = (w[0][:2]).upper()
        out.append(p)
    return out


def build_card(idx, pack, sampler, kind, rng, *, dev=False, theme=None, mode=None):
    c = {"card_id": ("F3-dev-%03d" if dev else "F3-c%03d") % idx, "family": "F3", "sampler": sampler,
         "kind": kind, "pack_id": pack["pack_id"], "persona_seed": pack["persona_seed"], "pack_set": pack["pack_set"],
         "item_sg": pack["item_sg"], "item_pl": pack["item_pl"], "holder_sg": pack["holder_sg"],
         "holder_pl": pack["holder_pl"], "field": pack["field"], "item_prefix": pack["item_prefix"],
         "holder_prefix": pack["holder_prefix"], "org": pack["org"], "people": list(pack["people"]),
         "inert": list(pack["inert"]), "roles": list(pack["roles"])}
    closed = kind in ("regular", "inverted", "short", "nocard")
    c["world"] = "closed" if closed else "open"
    c["theme"] = theme
    c["form_mode"] = mode if mode in ("choice", "yn") else ("choice" if rng.random() < 0.62 else "yn")
    c["rule21"] = kind if kind in ("short", "nocard") else None
    c["inverted"] = kind == "inverted"
    c["has_qty"] = bool(pack["qty"]) and rng.random() < 0.5
    if c["has_qty"]:
        c["qty"], c["unit"], c["qty_high_bad"] = pack["qty"]["name"], pack["qty"]["unit"], pack["qty"]["high_bad"]
    else:
        c["qty"], c["unit"], c["qty_high_bad"] = None, None, None
    # documents (Q3) on S1, S2 (sentence encoding), S4, closed only
    docs = [(d, t) for d, t in pack["docs"]]
    # mechanisms: one focus mechanism per card, plus VOID as a companion on some cards (compact cards; token cap)
    mech = {"SET", "TRANSFER", "CREATE"}
    if c["has_qty"]:
        mech |= {"SETQ", "ADJUST"}
    allow_rn = closed and sampler in ("S1", "S2", "S3", "S4", "S5") and c["rule21"] is None
    allowed = {"VOID": 1.0, "CORR": 1.0}
    if closed and sampler in ("S1", "S2", "S4", "S5") and docs and not c["inverted"]:
        allowed["SUPERSEDE"] = 1.7
    if allow_rn:
        allowed["RENAME"] = 0.8
        allowed["MERGE"] = 0.7
    if closed and not c["rule21"]:
        allowed["CHECK"] = 0.9
    if theme == "Q3" and "SUPERSEDE" in allowed:
        focus = "SUPERSEDE"
    elif theme == "Q8":
        focus = "CHECK" if ("CHECK" in allowed and rng.random() < 0.6) else "VOID"
    else:
        allowed.pop("SUPERSEDE", None)
        focus = rng.choices(list(allowed), weights=list(allowed.values()))[0]
    mech.add(focus)
    if focus != "VOID" and rng.random() < 0.45:
        mech.add("VOID")
    c["focus"] = focus
    c["mechs"] = sorted(mech)
    c["docs_on"] = "SUPERSEDE" in mech
    c["doc_types"] = [d for d, _ in docs][:3] or ["file"]
    c["doc_tag"] = {d: t for d, t in docs}
    c["doc_prefixes"] = _doc_prefixes(c["doc_types"])
    # toggles
    c["rename_mode"] = rng.choice(["alias", "retire"]) if "RENAME" in mech else None
    chk = "CHECK" in mech
    c["check"] = chk and rng.random() < 0.7
    c["lock"] = chk and (not c["check"] or rng.random() < 0.35)
    c["timed"] = sampler in ("S1", "S2", "S3", "S5") and rng.random() < 0.45
    if c["rule21"] or (sampler == "S5"):
        c["date_fmt"] = rng.choices(["iso", "mon_dmy", "mon_mdy"], [1, 2, 1])[0]
    else:
        c["date_fmt"] = rng.choices(["iso", "mon_dmy", "mon_mdy", "num_dmy", "num_mdy"], [2, 4, 1.5, 1.25, 1.25])[0]
    c["gap_marker"] = rng.choice(GAP_MARKERS)
    c["nei"] = rng.choice(NEI_WORDINGS)
    c["none"] = rng.choice(NONE_WORDINGS)
    # encoding
    if sampler == "S1":
        c["encoding"] = "rec" if (rng.random() < 0.3 and not c["rule21"]) else "sent"
    elif sampler == "S2":
        c["encoding"] = "rec" if (rng.random() < 0.4 and not c["docs_on"]) else "sent"
    elif sampler == "S3":
        c["encoding"] = "table"
    elif sampler == "S4":
        c["encoding"] = "notice"
    elif sampler == "S6":
        c["encoding"] = rng.choice(["sent", "table"])
    else:
        c["encoding"] = "git"
    # listing order
    if c["encoding"] == "table" and sampler in ("S3", "S2") and closed:
        c["listing"] = rng.choices(["sorted", "chrono", "shuffled"], [0.55, 0.25, 0.2])[0]
        if c["listing"] == "shuffled":
            c["timed"] = True
    elif sampler == "S6":
        c["listing"] = rng.choice(["recorded", "eff_sorted", "shuffled"])
    elif sampler == "S5":
        c["listing"] = rng.choice(["newest_first", "oldest_first"])
    else:
        c["listing"] = "chrono"
    if c["encoding"] == "rec" and sampler == "S2" and closed and rng.random() < 0.5:
        c["encoding"] = "table"
        c["listing"] = rng.choices(["sorted", "chrono"], [0.6, 0.4])[0]
    c["sort_key"] = "subject" if c["listing"] == "sorted" else None
    # gap style (explicit markers only in sentence / notice containers that can show a marker line)
    if c["world"] == "open":
        if c["encoding"] in ("table", "rec") or sampler == "S3":
            c["gap_style"] = rng.choice(["skipped", "leading"])
        else:
            c["gap_style"] = rng.choice(["explicit", "skipped", "leading"])
    else:
        c["gap_style"] = None
    c["has_register"] = not (c["gap_style"] == "leading" or sampler == "S5")
    # status vocabulary (masked / swapped later, in assign_vocab)
    raw = [s for s, _ in pack["statuses"]]
    k = min(len(raw), rng.randint(4, 7) if len(raw) >= 4 else len(raw))
    chosen = raw[:k]
    c["raw_statuses"] = chosen
    c["raw_tag"] = {s: t for s, t in pack["statuses"] if s in chosen}
    c["vocab"] = "plain"
    c["statuses"] = list(chosen)
    c["status_meaning"] = None
    c["status_tag"] = dict(c["raw_tag"])
    c["default_status"] = chosen[0]
    c["lock_status"] = rng.choice(chosen[1:]) if c["lock"] else None
    c["lock_status_raw"] = c["lock_status"]
    c["blank_rate"] = 0.0 if (c["rule21"] or c["encoding"] in ("git",)) else rng.choice([0.0, 0.0, 0.15, 0.3])
    c["lookalikes_on"] = sampler == "S2" or rng.random() < 0.4
    if c["encoding"] in ("rec", "table"):
        c["blank_rate"] = max(c["blank_rate"], 0.1)
    # feature switches that add card rules (kept sparse for the 1,900-token cap)
    c["roster"] = sampler == "S3" and kind == "regular" and theme == "Q5"
    c["q2_on"] = theme == "Q2"
    c["still_on"] = theme in ("Q4", "Q4o") and rng.random() < 0.6
    # question types
    c["qts"] = _qt_set(c, sampler, rng)
    # negation and notes
    c["neg_on"] = c["rule21"] == "short" or (c["rule21"] != "nocard" and not c["inverted"] and not c["roster"]
                                              and rng.random() < 0.7)
    c["notes_on"] = c["rule21"] is None and rng.random() < 0.6
    # definition style
    if c["rule21"] == "short":
        c["def_style"] = "short"
    elif c["rule21"] == "nocard":
        c["def_style"] = "none"
    else:
        if c["form_mode"] == "yn":
            c["def_style"] = rng.choices(["one_line", "one_line_examples", "decision_list", "rubric_table"],
                                         [0.15, 0.55, 0.18, 0.12])[0]
        else:
            c["def_style"] = rng.choices(["one_line", "one_line_examples", "rubric_table"], [0.5, 0.4, 0.1])[0]
    c["fewshot"] = False
    c["yes_rate"] = round(rng.uniform(0.2, 0.8), 3)
    c["header_v"] = rng.randrange(2)
    c["body_v"] = {k_: rng.randrange(2) for k_ in R.BODY}
    c["reg_v"] = rng.randrange(2)
    c["t_v"] = {t: rng.randrange(len(v)) for t, v in R.T.items()}
    c["task_v"] = rng.randrange(len(R.TASK_LINES))
    c["kind_nouns"] = rng.random() < 0.5    # stems name kinds ("desk DE-482") or bare IDs
    c["holder_role"] = {}
    return c


def _qt_set(c, sampler, rng):
    th = c.get("theme")
    if th is None:
        q = _qt_set_all(c, sampler, rng)
        if c["form_mode"] == "choice":
            q = [x for x in q if x in ("Q1", "Q2", "Q3", "Q5", "Q7")]
        elif c["form_mode"] == "yn":
            q = [x for x in q if x not in ("Q5", "Q7")]
        return q
    q = list(THEME_QTS[th][c["form_mode"]])
    if sampler == "S6" and c["form_mode"] == "yn" and th == "Q2":
        q.append("Q4")
    if "Q8" in q and not (c["check"] or c["lock"] or "VOID" in c["mechs"]):
        q = [x for x in q if x != "Q8"] or ["Q4"]
    if "Q3" in q and not c["docs_on"]:
        q = [x for x in q if x != "Q3"] or ["Q1"]
    return q


def _qt_set_all(c, sampler, rng):
    if c["inverted"]:
        return ["Q7"]
    if c["world"] == "open":
        return ["Q1", "Q4", "Q5"]
    if sampler == "S3":
        if c["roster"]:
            q = ["Q1", "Q5"]
        else:
            q = ["Q1", "Q5"] + (["Q2"] if c["q2_on"] else []) + (["Q6"] if rng.random() < 0.6 else [])
    elif sampler == "S6":
        q = ["Q1", "Q2", "Q4"]
    elif sampler == "S4":
        q = ["Q1", "Q4", "Q5"] + (["Q3"] if c["docs_on"] else [])
        if c["check"] or c["lock"] or "VOID" in c["mechs"]:
            q.append("Q8")
    else:
        q = ["Q1", "Q4", "Q5"] + (["Q2"] if c["q2_on"] else [])
        if c["docs_on"]:
            q.append("Q3")
        if rng.random() < 0.4:
            q.append("Q6")
        if (c["check"] or c["lock"] or "VOID" in c["mechs"]) and rng.random() < 0.8:
            q.append("Q8")
    if c["rule21"]:
        q = [x for x in q if x != "Q7"]
    return q


def assign_vocab(cards, rng):
    """Masked and swapped vocabularies on about 16 of the non-inverted, non-2.1 cards (K1, B07)."""
    elig = [c for c in cards if not c["inverted"] and not c["rule21"] and c.get("form_mode") == "choice"
            and c.get("theme") in ("Q1", "Q2", "Q1o")]
    rng.shuffle(elig)
    elig.sort(key=lambda c: (c["world"] == "open", c.get("theme") != "Q2"))
    masked, swapped = elig[:7], elig[7:14]
    swords = _swap_words()
    for j, c in enumerate(masked):
        sch = ["MS10", "MS11", "MS18", "MS04", "MS08", "MS20"][j % 6]
        codes = fmt1_labels.masked_ids(sch, len(c["raw_statuses"]), c["card_id"])
        _apply_vocab(c, "masked", codes)
        c["mask_scheme"] = sch
    for j, c in enumerate(swapped):
        r2 = rng_for("swap", c["card_id"])
        words = [w for w in swords if w.lower() not in [s.lower() for s in c["raw_statuses"]]]
        pick = r2.sample(words, len(c["raw_statuses"]))
        _apply_vocab(c, "swapped", pick)


def _apply_vocab(c, mode, names):
    m = dict(zip(names, c["raw_statuses"]))
    c["vocab"] = mode
    c["statuses"] = list(names)
    c["status_meaning"] = m
    c["status_tag"] = {n: c["raw_tag"][m[n]] for n in names}
    c["default_status"] = names[0]
    if c["lock"]:
        c["lock_status"] = names[c["raw_statuses"].index(c["lock_status_raw"])]
    c["status_heavy"] = True


def assign_styles_wordings(c, rng, *, dev=False):
    enc = c["encoding"]
    if dev:
        styles = [s for s in fmt1_pool.styles(held_out=True) if s["skin"] in HELDOUT_SKINS_GIT]
    elif c["rule21"] == "nocard":
        styles = _styles_for({k: v for k, v in OK_SKINS_SENT.items() if k in NOCARD_CONTAINERS})
    elif enc == "sent":
        styles = _styles_for(OK_SKINS_SENT)
    elif enc == "rec":
        styles = _styles_for({k: OK_SKINS_REC[k] for k in REC_CONTAINERS_S1})
    elif enc == "table":
        tb = "omit" if unit_hash("table_blank", c["card_id"]) < 0.45 else "cell"
        c["table_blank"] = tb
        keep = ("json", "yaml", "key_value") if tb == "omit" else ("markdown_table", "html_snippet", "memo")
        styles = _styles_for({k: v for k, v in OK_SKINS_REC.items() if k in keep})
    elif enc == "notice":
        if c["gap_style"] == "explicit":
            styles = _styles_for({k: v for k, v in OK_SKINS_NOTICE.items() if k in ("memo", "prose", "bullet_sop")})
        else:
            styles = _styles_for(OK_SKINS_NOTICE)
    else:
        raise ValueError(enc)
    if c.get("gap_style") == "explicit" and enc == "sent":
        styles = [s for s in styles if s["container"] in ("prose", "memo", "bullet_sop")]
    if c["has_register"] and not dev:
        styles = [s for s in styles if s["container"] != "log_lines"]
    k = min(len(styles), 6)
    c["styles"] = [s["id"] for s in fmt1_pool.card_style_set(styles, k, "F3", c["card_id"])]
    # wordings: >= 5 per card (5 any-form + 1 yes/no + 1 choice), no-card rows avoid wordings that cite the card
    ws = list(WORDINGS.values())
    if c["rule21"] == "nocard":
        ws = [w for w in ws if "card" not in w["text"].lower()]
    if c["listing"] not in ("chrono",) or c["sampler"] == "S6":
        ws = [w for w in ws if "top to bottom" not in w["text"].lower()]
    anyf = [w["id"] for w in ws if w["forms"] == ["any"]]
    yn = [w["id"] for w in ws if w["forms"] == ["yn"]]
    ch = [w["id"] for w in ws if w["forms"] == ["choice"]]
    r2 = random.Random(int(unit_hash("wordings", c["card_id"]) * 2 ** 32))
    c["wordings"] = r2.sample(anyf, 5) + r2.sample(yn, 1) + r2.sample(ch, 1)
    c["locale"] = "GB" if unit_hash("locale", c["card_id"]) < 0.3 else "US"


def _distinct(cards, rng):
    """G11 pairwise card distinctness: different packs (always) and a different stated rule set or label schema."""
    for _ in range(5):
        seen, clash = {}, 0
        for c in cards:
            key = (tuple(stated_rules(c)), tuple(c["statuses"]), tuple(c["qts"]))
            if key in seen:
                clash += 1
                c["timed"] = not c["timed"] if c["sampler"] in ("S1", "S2", "S3") else c["timed"]
                c["date_fmt"] = "mon_dmy" if c["date_fmt"] != "mon_dmy" else "iso"
            seen[key] = c["card_id"]
        if not clash:
            return 0
    return clash


def _g11_key(c):
    """G11 card key as the QC checker reads it (R1-11): stated rule set (sidecar `stated_toggles`; none on no-card
    cards) plus the label schema (status vocabulary kind and question-type set)."""
    if c["rule21"] == "nocard":
        tog = frozenset()
    elif c["rule21"] == "short":
        tog = frozenset(short_card_rules(c)[0])
    else:
        tog = frozenset(stated_rules(c))
    return (tog, c["vocab"], frozenset(c["qts"]))


def ensure_distinct(cards):
    """Repair r2 (G11 found 3 card pairs with the same stated rules and label schema). A collision is fixed by
    redrawing one card's toggles or question-type set (G0 R1-11), never by editing rows: full and short cards switch
    the date format between a month-name and a numeric form (T26 stated or not; 2.1 cards keep ISO or month names, so
    they drop their secondary question type instead); no-card cards keep only their primary question type."""
    fixed = []
    for _ in range(4):
        seen, clash = {}, []
        for c in cards:
            k = _g11_key(c)
            if k in seen:
                clash.append(c)
            else:
                seen[k] = c["card_id"]
        if not clash:
            break
        for c in clash:
            if c["rule21"] is None:
                if c["date_fmt"] in ("num_dmy", "num_mdy"):
                    c["date_fmt"] = "mon_dmy"
                else:
                    c["date_fmt"] = "num_dmy"
            elif len(c["qts"]) > 1:
                c["qts"] = list(c["qts"][:1])
            fixed.append(c["card_id"])
    left = []
    seen = {}
    for c in cards:
        k = _g11_key(c)
        if k in seen:
            left.append([seen[k], c["card_id"]])
        seen[k] = c["card_id"]
    return {"fixed": fixed, "left": left}


RN_CARDS, MG_CARDS, CORR_COMPANION = 17, 14, 0.4


def rebalance_mechs(cards):
    """Repair r2 (G10: decisive RENAME 0.4% and MERGE 1.0% of rows, each needs >= 8% with 50% +/- 10 decisive where
    present). Mechanisms are assigned to cards by quota instead of one free draw per card: on closed full S1-S4 cards
    that are not themed on Q3 (documents) or Q8, RENAME goes to RN_CARDS cards and MERGE to MG_CARDS holder-themed
    cards (a card may carry both; their T14 / T15 / T17sr rules are stated as before); the VOID companion is kept.
    Other cards keep their drawn focus; a CORRECTION companion is added to a fixed share of the cards whose focus is
    VOID or the transfer check, so corrections stay present on enough rows. Deterministic (hash order)."""
    # lean roster cards: two inverted (Q7) cards per sampler S1-S3 carry no extra mechanism, so their short rule
    # text (printed twice on choice rows) leaves room under the 1,900-token cap for 20-60 options (G10 bucket 15%)
    inv = [c for c in cards if c.get("inverted")]
    lean = set()
    for sp in ("S1", "S2", "S3"):
        lean |= {x["card_id"] for x in sorted([c for c in inv if c["sampler"] == sp],
                                              key=lambda c: unit_hash("lean", c["card_id"]))[:2]}
    for c in cards:
        if c["card_id"] in lean:
            c["mechs"] = sorted({"SET", "TRANSFER", "CREATE"} | ({"SETQ", "ADJUST"} if c["has_qty"] else set()))
            c["focus"] = "PLAIN"
            c["check"] = c["lock"] = False
            c["lock_status"] = c["lock_status_raw"] = None
            c["rename_mode"] = None
            c["lean_roster"] = True
            # compact surface: no quantity field, no times, no notes, sentence logs (S1/S2), no look-alikes off S2
            c["has_qty"] = False
            c["qty"] = c["unit"] = c["qty_high_bad"] = None
            c["notes_on"] = False
            if c["listing"] == "shuffled":
                c["listing"] = "sorted"
                c["sort_key"] = "subject"
            c["timed"] = False
            if c["encoding"] == "rec":
                c["encoding"] = "sent"
            c["lookalikes_on"] = c["sampler"] == "S2"
    elig = [c for c in cards if c["world"] == "closed" and c["rule21"] is None and c["card_id"] not in lean
            and c["sampler"] in ("S1", "S2", "S3", "S4") and c.get("theme") not in ("Q3", "Q8")]
    holder = [c for c in elig if c.get("theme") in ("Q4", "Q5", "Q6", "Q7")]
    mg = set(x["card_id"] for x in sorted(holder, key=lambda c: unit_hash("mg", c["card_id"]))[:MG_CARDS])
    # an item rename is a hop only for questions that name an item (Q1, Q2, Q4, Q5); on Q6 counts and Q7 lists it
    # would almost always be inert, so RENAME goes to the item-themed cards
    item_th = [c for c in elig if c.get("theme") in ("Q1", "Q2", "Q4", "Q5")]
    rn = set(x["card_id"] for x in sorted(item_th, key=lambda c: unit_hash("rn", c["card_id"]))[:RN_CARDS])
    for c in elig:
        if c["card_id"] not in mg and c["card_id"] not in rn:
            continue
        m = {"SET", "TRANSFER", "CREATE"} | ({"SETQ", "ADJUST"} if c["has_qty"] else set())
        if "VOID" in c["mechs"] or unit_hash("voidcomp", c["card_id"]) < 0.6:
            m.add("VOID")
        if c["card_id"] in rn:
            m.add("RENAME")
        if c["card_id"] in mg:
            m.add("MERGE")
        c["mechs"] = sorted(m)
        c["focus"] = "MERGE" if c["card_id"] in mg else "RENAME"
        c["rename_mode"] = ("alias" if unit_hash("rnmode", c["card_id"]) < 0.5 else "retire") \
            if "RENAME" in m else None
        c["check"] = c["lock"] = False
        c["lock_status"] = c["lock_status_raw"] = None
        if "Q8" in c["qts"]:
            c["qts"] = [q for q in c["qts"] if q != "Q8"] or ["Q4"]
    for c in cards:
        if c["card_id"] in mg or c["card_id"] in rn or c["card_id"] in lean:
            continue
        if c.get("focus") in ("VOID", "CHECK") and "CORR" not in c["mechs"] and c["sampler"] != "S5" \
                and unit_hash("corrcomp", c["card_id"]) < CORR_COMPANION:
            c["mechs"] = sorted(set(c["mechs"]) | {"CORR"})
            c["corr_companion"] = True
        # VOID companion on most other cards (a voided later write is the hop that makes d3-d4 paths on cards whose
        # only other mechanism is a correction); the card fit drops it again where the token budget is short
        if "VOID" not in c["mechs"] and c["sampler"] not in ("S4", "S5") and unit_hash("voidcomp", c["card_id"]) < 0.85:
            c["mechs"] = sorted(set(c["mechs"]) | {"VOID"})
    return {"rename": sorted(rn), "merge": sorted(mg)}


def _yn_weight(c):
    """Expected share of a card's rows that are yes/no (form mode; inverted cards have none)."""
    if c.get("inverted"):
        return 0.0
    return {"yn": 1.0, "coin": 0.5, "choice": 0.0}.get(c.get("form_mode"), 0.5) if c["world"] == "closed" or \
        c.get("form_mode") != "choice" else 0.0


def balance_yes_rates(cards):
    """Repair r2 (G7: the pool's yes/no rows were 46% yes, so every frequent n-gram leaned 'no'). The per-card rates
    stay the per-sampler stratified uniform 20-80% grid (spec 2.1, R2-05); only their pairing with cards is changed:
    within a sampler, rates are swapped between cards until the yes/no-row-weighted mean is 50% (+/- 0.5 pp)."""
    by_sp = {}
    for c in cards:
        by_sp.setdefault(c["sampler"], []).append(c)
    for sp, cs in sorted(by_sp.items()):
        w = {c["card_id"]: _yn_weight(c) for c in cs}
        for _ in range(200):
            W = sum(w.values())
            if W <= 0:
                break
            mean = sum(w[c["card_id"]] * c["yes_rate"] for c in cs) / W
            if abs(mean - 0.5) <= 0.005:
                break
            best = None
            for a in cs:
                for b in cs:
                    if w[a["card_id"]] <= w[b["card_id"]]:
                        continue
                    d = (w[a["card_id"]] - w[b["card_id"]]) * (b["yes_rate"] - a["yes_rate"]) / W
                    new = abs(mean + d - 0.5)
                    if new < abs(mean - 0.5) - 1e-9 and (best is None or new < best[0]):
                        best = (new, a, b)
            if best is None:
                break
            _, a, b = best
            a["yes_rate"], b["yes_rate"] = b["yes_rate"], a["yes_rate"]


def _twin_capacity(c):
    """How many label-flip twin kinds a card's yes/no rows can get: contrast twins need a closed world, negation
    twins need a stated T44 (neg_on). Cards with no yes/no rows sort last."""
    if c.get("inverted") or _yn_weight(c) == 0:
        return 9
    return (1 if c["world"] == "closed" else 0) + (2 if c.get("neg_on") else 0)


def pair_rates_by_capacity(cards):
    """Repair r2 (G7: pack words of cards whose rows could get no label-flip twin kept the drawn 20-25% rate on all
    their rows). The per-sampler grid of drawn rates is unchanged (uniform 20-80%, R2-05); only which card gets which
    grid value changes: cards that can get no or few flip twins get the rates nearest 50%, cards with both twin
    kinds get the extreme ones, so matched twins can bring every card's yes/no rows near 50% (spec 8 G7: fix by
    matched twins first). Then rates are swapped between cards of the same capacity until the yes/no-weighted mean
    is 50% (+/- 0.5 pp). Run after the card fit (which can switch negation off). Deterministic."""
    by_sp = {}
    for c in cards:
        if _twin_capacity(c) < 9:          # only cards with yes/no rows: the drawn rate applies to them
            by_sp.setdefault(c["sampler"], []).append(c)
    for sp, cs in sorted(by_sp.items()):
        r3 = rng_for("yes_rate_r2", sp)
        n = len(cs)
        rates = [round(0.2 + 0.6 * (i + r3.random()) / n, 3) for i in range(n)]   # stratified uniform 20-80%
        rates.sort(key=lambda r: (abs(r - 0.5), r))
        order = sorted(cs, key=lambda c: (_twin_capacity(c), unit_hash("cap", c["card_id"])))
        for c, r in zip(order, rates):
            c["yes_rate"] = r
        w = {c["card_id"]: _yn_weight(c) for c in cs}
        for _ in range(300):
            W = sum(w.values())
            if W <= 0:
                break
            mean = sum(w[c["card_id"]] * c["yes_rate"] for c in cs) / W
            if abs(mean - 0.5) <= 0.005:
                break
            best = None
            for a in cs:
                for b in cs:
                    if a is b or _twin_capacity(a) != _twin_capacity(b):
                        continue
                    d = (w[a["card_id"]] - w[b["card_id"]]) * (b["yes_rate"] - a["yes_rate"]) / W
                    if d == 0:
                        continue
                    new = abs(mean + d - 0.5)
                    if new < abs(mean - 0.5) - 1e-9 and (best is None or new < best[0]):
                        best = (new, a, b)
                    # also allow flipping a rate around 50% inside a band: r <-> 1 - r is not in the grid, so skip
            if best is None:
                break
            _, a, b = best
            a["yes_rate"], b["yes_rate"] = b["yes_rate"], a["yes_rate"]


def make_training_cards():
    rng = rng_for("cards", "r1")
    packs = list(training_packs())
    rng.shuffle(packs)
    plan = _plan_slots()
    cards = []
    used = set()
    pi = 0
    for idx, (sp, kind, theme, mode) in enumerate(plan, start=1):
        while True:
            p = packs[pi]
            pi += 1
            if p["pack_id"] in used:
                continue
            # S4 needs named parties; Q3 cards need document types
            if sp == "S4" and len(p["people"]) < 4:
                continue
            break
        used.add(p["pack_id"])
        c = build_card(idx, p, sp, kind, random.Random(rng.random()), theme=theme, mode=mode)
        cards.append(c)
    rebalance_mechs(cards)
    assign_vocab(cards, rng)
    # per-card yes rates: uniform over 20-80%, stratified within each sampler so no sampler drifts (R2-05)
    by_sp = {}
    for c in cards:
        by_sp.setdefault(c["sampler"], []).append(c)
    for sp, cs in sorted(by_sp.items()):
        r3 = rng_for("yes_rate", sp)
        grid = [0.2 + 0.6 * (i + r3.random()) / len(cs) for i in range(len(cs))]
        r3.shuffle(grid)
        for c, y in zip(cs, grid):
            c["yes_rate"] = round(y, 3)
    balance_yes_rates(cards)
    for c in cards:
        assign_styles_wordings(c, random.Random(rng.random()))
        assign_fewshot(c)
    _distinct(cards, rng)
    return cards


def assign_fewshot(c):
    # few-shot overlay on 5-10% of cards (any full body style)
    c["fewshot"] = c["rule21"] is None and c["sampler"] in ("S1", "S2", "S4", "S6") \
        and unit_hash("fewshot", c["card_id"]) < 0.11


DEV_PLAN = ([("regular", "Q4", "yn", "deep")] * 6 +
            [("regular", "Q1", "choice", None), ("regular", "Q2", "yn", None), ("regular", "Q3", "coin", None),
             ("regular", "Q4", "yn", None), ("regular", "Q5", "choice", None), ("regular", "Q6", "yn", None),
             ("regular", "Q8", "yn", None), ("open", "Q1o", "choice", None), ("open", "Q4o", "yn", None),
             ("regular", "Q2", "choice", None), ("regular", "Q1", "yn", None), ("open", "Q5o", "choice", None)])


def make_dev_cards():
    """S5 (held-out git-like syntax) cards on held-out packs, held-out styles only (mix-tuning dev; never trained).
    Six 'deep' cards carry stacked decisive chains for the depth sweep (spec 10; depth levels 1, 2, 3-4, 5-6,
    7-8); the others give the 400 family items across the question types."""
    rng = rng_for("cards", "dev")
    packs = list(heldout_packs())
    rng.shuffle(packs)
    cards = []
    for i, (kind, theme, mode, flag) in enumerate(DEV_PLAN):
        p = packs[i % len(packs)]
        r2 = random.Random(rng.random())
        c = build_card(i + 1, p, "S5", kind, r2, dev=True, theme=theme, mode=mode)
        if flag == "deep":
            c["deep_card"] = True
            c["mechs"] = sorted(set(c["mechs"]) | {"VOID", "CORR", "RENAME", "CHECK"} - {"MERGE", "SUPERSEDE"})
            c["focus"] = "VOID"
            c["rename_mode"] = "retire"
            c["check"], c["lock"], c["lock_status"] = True, False, None
            c["docs_on"] = False
            c["qts"] = ["Q4", "Q1"]
            c["listing"] = "oldest_first" if i % 2 == 0 else "newest_first"
        if c["world"] == "open":
            c["gap_style"] = r2.choice(["skipped", "leading"])
        c["notes_on"] = False
        assign_styles_wordings(c, random.Random(rng.random()), dev=True)
        cards.append(c)
    return cards


# ------------------------------------------------------------------------------------------------ stated rules

def stated_rules(c, *, neg_rows=True, still_rows=True):
    """The T ids this card states (full cards). Order = card order."""
    sp, enc, m = c["sampler"], c["encoding"], set(c["mechs"])
    qts = set(c["qts"])
    yn = c.get("form_mode") != "choice"
    out = []
    if c["world"] == "closed":
        out.append("T1")
    else:
        gs = c["gap_style"]
        out.append("T2c" if c["has_register"] else "T2")
        out.append({("S4", "explicit"): "T3x4", ("S4", "skipped"): "T3s4", ("S4", "leading"): "T3l4"}.get(
            (sp, gs), {"explicit": "T3x", "skipped": "T3s", "leading": "T3l"}[gs]))
    if sp == "S4":
        out.append("T41" if c["world"] == "closed" else "T41o")
    elif sp == "S6":
        out.append("T6")
        if c["listing"] == "eff_sorted":
            out.append("T6s")
        elif c["listing"] == "shuffled":
            out.append("T6x")
    elif sp == "S5":
        out.append("T43")
    else:
        out.append("T5t" if c["timed"] else "T5d")
    if enc == "table":
        out.append("T42k" if c.get("table_blank") == "omit" else "T42")
    out.append("T4")
    if c["has_register"]:
        out.append("T9")
    if c["blank_rate"] > 0 or c["gap_style"] == "leading" or enc in ("rec", "table"):
        out.append("T9cq" if c["has_qty"] else "T9c")
    if enc == "rec":
        out.append("T8k")
    if "VOID" in m:
        out.append("T10")
    if "CORR" in m:
        out.append("T11")
    if "VOID" in m and "CORR" in m:
        out.append("T12")
    if c.get("q2_on"):
        out.append("T7e" if sp == "S6" else "T7")
    if "SUPERSEDE" in m:
        out += ["T13", "T37"]
        if "Q3" in qts and c["neg_on"] and yn:
            out.append("T13lack")
    if "RENAME" in m:
        out += ["T14", "T14a" if c["rename_mode"] == "alias" else "T14r"]
    if "MERGE" in m:
        out.append("T15")
    if c.get("lookalikes_on"):
        out.append("T16")
    out.append("T17q" if c["has_qty"] else "T17")
    if not c["check"]:
        out.append("T17sr" if ("RENAME" in m and c["rename_mode"] == "retire") or "MERGE" in m else "T17s")
    if c["check"] and c["lock"]:
        out.append("T40")
    elif c["check"]:
        out.append("T18")
        if c["rename_mode"] == "alias":
            out.append("T18a")
    elif c["lock"]:
        out.append("T19")
    if yn and (c["has_qty"] or "Q6" in qts):
        out.append("T22")
    if c["has_qty"]:
        out.append("T28")
    if c.get("q2_on"):
        out.append("T24e" if sp == "S6" else "T24")
    if "Q2" in qts and yn:
        out.append("T25e" if sp == "S6" else "T25")
    if c["date_fmt"] in ("num_dmy", "num_mdy"):
        out.append("T26")
    if c["timed"]:
        out.append("T27")
    if "Q4" in qts and c.get("still_on") and yn:
        out.append("T31")
    if c["notes_on"]:
        out.append("T33n" if sp == "S4" else "T33")
    if c["world"] == "open" and c.get("form_mode") != "yn":
        out.append("T34n")
    if "Q7" in qts:
        out.append("T34o")
    if "Q8" in qts:
        out.append("T38")
        if c["neg_on"]:
            out.append("T38fail")
    if "Q6" in qts:
        out.append("T39q" if c["has_qty"] else "T39")
    if c["neg_on"] and yn:
        out.append("T44")
    out.append("T36")
    if c["vocab"] == "masked":
        out.append("T36m")
    elif c["vocab"] == "swapped":
        out.append("T36s")
    if c["def_style"] == "decision_list":
        out.append("T35")
    return out


def short_card_rules(c):
    """2.1 short card: the task line plus a subset of the triggered rules; at least one triggered rule left out.
    Always kept: blank sentences its rows need (T9c), T44 on negated rows (and T13lack / T38fail)."""
    full = stated_rules(c)
    keep_always = {"T9c", "T9cq", "T44", "T13lack", "T38fail", "T36"}
    optional = [t for t in full if t not in keep_always]
    r = random.Random(int(unit_hash("short", c["card_id"]) * 2 ** 32))
    drop = set(r.sample(optional, max(1, len(optional) // 2)))
    return [t for t in full if t not in drop], sorted(drop)


def fill(text, c, extra=None):
    vals = {"item": c["item_sg"], "items": c["item_pl"], "holder": c["holder_sg"], "holders": c["holder_pl"],
            "field": c["field"], "qty": c["qty"] or "", "unit": c["unit"] or "", "kind": c["item_sg"],
            "default": c["default_status"], "S": c.get("lock_status") or "", "NEI": c["nei"], "None": c["none"],
            "gap": c["gap_marker"], "N0": "", "D0": "", "Dlast": "", "key": "", "order": "",
            "dateorder": R.DATE_ORDER_TEXT.get(c["date_fmt"], ""), "listing": "", "values": "",
            "qtyclause": "", "code": "", "meaning": "", "word": ""}
    if c["sampler"] == "S6":
        vals["order"] = "effective-date"
    elif c["timed"]:
        vals["order"] = "date and time"
    else:
        vals["order"] = "date"
    if c["has_qty"]:
        vals["qtyclause"] = f", and a blank {c['qty']} in a creation starts as 0"
    if c.get("listing") == "sorted":
        vals["key"] = "subject"
    elif c.get("listing") == "shuffled":
        vals["key"] = "no particular key"
    else:
        vals["key"] = "entry number"
    vals["values"] = ", ".join(f"'{s}'" for s in c["statuses"])
    if extra:
        vals.update(extra)
    return text.format(**vals)
