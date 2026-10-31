"""F11 S4 record containers (G0 S4, SEM-50, F11-R2-04, F11-R3-03, F11-R4-10, F11-R5-05/06/09).

Renderer side only. A record report = the subject line (doc title, or a para on inverted rows) plus one record (a fmt1
'fields' block) or, when the row has other-entity lures, a multi-record table (a fmt1 'table' block). Frames map to
fields: PRIOR -> previous_<field>, HYPO -> proposed_<field>, OTHER -> the same field in another entity's record,
COMMENT -> a value word inside a comment field. Inert sentences and attack text sit in comment fields.
Every random layout choice is cached in spec['rec'] so twins differ from their base only where intended.
"""
from __future__ import annotations

import lex
from cards import fmt_num, fmt_date, unit_form
from common import toks
from fmt1 import pool
from tax import PRES

RECORD_CONTAINERS = ("json", "yaml", "key_value", "markdown_table", "csv")
BAD_SKINS = ("json.array", "json.lines", "csv.fixed_width", "kv.ini")
ID_FIELDS = ("record_id", "case_ref", "entry_id", "file_no", "item_ref", "log_ref")
DIST_FIELDS = (("logged_by", "people"), ("reviewed_by", "people"), ("entered_by", "people"),
               ("channel", ("portal", "desk", "phone", "post", "kiosk")),
               ("shift", ("early", "late", "night", "day")),
               ("batch_tag", ("amber", "teal", "slate", "ochre")))
COMMENT_TEMPLATES = ("{p} mentioned {v} on the call.", "{p} asked about {v} at the desk.",
                     "Query from {p} about {v}.", "{p} flagged {v} for a later look.",
                     "{p} copied {v} from an older sheet.")
SUFFIXES = ("", "", "_cd", "_val", "_obs")


def snake(s: str) -> str:
    import re
    w = [x for x in re.sub(r"[^a-z0-9]+", " ", s.lower()).split() if x not in ("a", "an", "the", "s")]
    return "_".join(w[:3])


def record_styles(held_out=False, container=None):
    out = []
    for s in pool.styles(held_out=held_out):
        if s["container"] not in RECORD_CONTAINERS or s["skin"] in BAD_SKINS:
            continue
        if container and s["container"] != container:
            continue
        out.append(s)
    return out


def setup_card(card, r, vtoks):
    """Per-card record choices: field names, ID field, distractor fields (1-3), frame kinds."""
    card.records = True
    card.cue_sentences = False
    card.frame_kinds = ["OTHER", "PRIOR", "HYPO", "COMMENT"]
    card.id_field = r.choice(ID_FIELDS)
    used = {card.id_field}
    card.fields = {}
    for i, a in enumerate(card.attrs):
        for _ in range(20):
            f = snake(a.name) + r.choice(SUFFIXES)
            if f not in used:
                break
        else:
            f = snake(a.name) + f"_{i}"
        used.add(f)
        card.fields[i] = f
    dist = []
    pool_ = list(DIST_FIELDS)
    r.shuffle(pool_)
    for name, vals in pool_:
        if len(dist) >= r.randint(1, 3):
            break
        if vals == "people":
            continue
        vals = [v for v in vals if not set(toks(v)) & vtoks]
        if len(vals) >= 2:
            dist.append((name, tuple(vals)))
    for name, vals in DIST_FIELDS:
        if vals == "people" and len(dist) < 3 and r.random() < 0.6:
            dist.append((name, "people"))
    card.dist_fields = dist or [("logged_by", "people")]


# -------------------------------------------------------------------------------------------------- values
def pres_word(r, a, present, lay, key):
    if present:
        opts = ["yes", "true"] + list(a.terms["attr"])
    else:
        opts = ["no", "false", "none"]
    return lay.setdefault(key, r.choice(opts))


def focal_value(card, it, i, r, lay):
    a = card.attrs[i]
    if i == it.missing:
        return lay.setdefault(f"miss{i}", r.choice(lex.UNKNOWN_FIELD_VALUES))
    if a.kind == "nom":
        return it.surf[i]
    if a.kind == "pres":
        return pres_word(r, a, it.cell[i] == PRES, lay, f"p{i}:{it.cell[i]}")
    if a.kind == "num":
        x = it.exact[i]
        return f"{fmt_num(x)} {unit_form(a, x)}"
    return fmt_date(it.exact[i])


def frame_value(card, fr, r, lay, key):
    a = card.attrs[fr["attr"]]
    if a.kind == "nom":
        return fr["surf"]
    if a.kind == "pres":
        return pres_word(r, a, True, lay, key)
    if a.kind == "num":
        x = fr["exact"]
        return f"{fmt_num(x)} {unit_form(a, x)}"
    return fmt_date(fr["exact"])


def comment_value(card, fr):
    a = card.attrs[fr["attr"]]
    if a.kind == "nom":
        return fr["surf"]
    if a.kind == "pres":
        return fr["surf"]
    if a.kind == "num":
        x = fr["exact"]
        return f"{fmt_num(x)} {unit_form(a, x)}"
    return fmt_date(fr["exact"])


# -------------------------------------------------------------------------------------------------- records
def focal_pairs(g, it, spec, *, allow_other=True):
    """(focal record pairs, other records) for one item; other records are pair lists."""
    c, r = g.card, g.r
    lay = spec.setdefault("rec", {})
    P = {c.id_field: it.desig}
    for i in range(len(c.attrs)):
        P[c.fields[i]] = focal_value(c, it, i, r, lay)
    for name, vals in c.dist_fields:
        ppl = [p for p in c.people]
        P[name] = lay.setdefault("d:" + name, r.choice(ppl if vals == "people" else list(vals)))
    comments = []
    others = {}
    used = set()
    for fr in it.frames:                       # one previous_ / proposed_ field per attribute
        if fr["kind"] in ("PRIOR", "HYPO"):
            if (fr["kind"], fr["attr"]) in used:
                alt = "HYPO" if fr["kind"] == "PRIOR" else "PRIOR"
                fr["kind"] = alt if (alt, fr["attr"]) not in used else "COMMENT"
            used.add((fr["kind"], fr["attr"]))
    for j, fr in enumerate(it.frames):
        i = fr["attr"]
        k = fr["kind"]
        if k == "PRIOR":
            P["previous_" + c.fields[i]] = frame_value(c, fr, r, lay, f"fv{j}")
        elif k == "HYPO":
            P["proposed_" + c.fields[i]] = frame_value(c, fr, r, lay, f"fv{j}")
        elif k == "COMMENT":
            t = lay.setdefault(f"ct{j}", r.choice(COMMENT_TEMPLATES))
            p = lay.setdefault(f"cp{j}", r.choice(c.people))
            comments.append(t.format(p=p, v=comment_value(c, fr)))
        elif k == "OTHER":
            if not allow_other:
                raise ValueError("other-entity frame on a single-record render")
            others.setdefault(fr["other"], []).append(fr)
        else:
            raise ValueError(f"frame kind {k} on a record card")
    if it.attack:
        comments.append(it.attack)
    for s in it.inert:
        comments.append(s)
    for j, s in enumerate(comments):
        P["comment" if j == 0 else f"comment_{j + 1}"] = s
    recs = []
    for od, frs in others.items():
        Q = dict(P)
        Q[c.id_field] = od
        for j, fr in enumerate(frs):
            Q[c.fields[fr["attr"]]] = frame_value(c, fr, r, lay, f"of{od}{fr['attr']}")
        for key in list(Q):
            if key.startswith("comment"):
                Q[key] = lay.setdefault(f"oc{od}{key}", r.choice(g.inert))
        for name, vals in c.dist_fields:
            if vals == "people":
                Q[name] = lay.setdefault(f"od{od}{name}", r.choice(c.people))
        recs.append(Q)
    return P, recs


def ordered(keys, lay, r):
    """Stable per-row field order: the ID field first on 60% of rows, the rest by cached random keys."""
    def k(f):
        return lay.setdefault("o:" + f, r.random())
    out = sorted(keys, key=k)
    return out


def record_block(g, it, spec, *, allow_other=True):
    c, r = g.card, g.r
    lay = spec.setdefault("rec", {})
    P, others = focal_pairs(g, it, spec, allow_other=allow_other)
    keys = ordered([k for k in P if k != c.id_field], lay, r)
    if lay.setdefault("id_first", r.random() < 0.6) or not keys:
        keys = [c.id_field] + keys
    else:
        keys = keys[:1] + [c.id_field] + keys[1:]
    if not others:
        return {"type": "fields", "label": None, "pairs": [[k, P[k]] for k in keys]}
    rows = [P] + others
    pos = lay.setdefault("focal_pos", r.randrange(len(rows)))
    rows = others[:pos] + [P] + others[pos:]
    return {"type": "table", "caption": None, "columns": list(keys), "rows": [[q[k] for k in keys] for q in rows]}


def record_doc(g, it, spec):
    r = g.r
    lab = spec.setdefault("subj", r.choice(lex.SUBJECT_LABELS))
    # the other-entity designators must not clash: merge frames per designator, one value per field
    seen = {}
    for fr in it.frames:
        if fr["kind"] != "OTHER":
            continue
        key = (fr["other"], fr["attr"])
        if key in seen:
            fr["other"] = g.designators(2)[1]
        seen[(fr["other"], fr["attr"])] = 1
    blk = record_block(g, it, spec)
    return {"title": f"{lab}: {it.desig}", "meta": [], "blocks": [blk]}
