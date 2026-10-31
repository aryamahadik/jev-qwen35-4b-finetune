"""Render validated drafts into rows (spec 2.4 format) with full meta, sidecar entries and relations; run the per-row
gates: G3 (parse back + solver B, 100%), G15 (fmt1 loader_check incl. check_rows and gold-letter mapping under a
random permutation), the counted-length cap (real tokenizer on decoder_io.user_msg, cygnet + schema_branch_mark,
instructions counted twice by the layout itself), negcount on the question."""
from __future__ import annotations

import hashlib
import json
import random
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LEAN / "c_src" / "common"))

import canon as CN  # noqa: E402
import core as C  # noqa: E402
import f4lex as L  # noqa: E402
import negcount  # noqa: E402
import render_f4 as R  # noqa: E402
import rowmake as RM  # noqa: E402
from fmt1 import card as fcard  # noqa: E402
from fmt1 import labels as flabels  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402

LEN_CAP = 1900
TOKENIZER_JSON = sorted(Path.home().glob(".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/*/tokenizer.json"))


@lru_cache(maxsize=1)
def tokenizer():
    from tokenizers import Tokenizer
    return Tokenizer.from_file(str(TOKENIZER_JSON[0]))


def tokenizer_sha():
    return hashlib.sha256(TOKENIZER_JSON[0].read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def dio():
    return fcard._dio()


def counted_length(row):
    """Real-tokenizer length of decoder_io.user_msg(row) in the served style and layout (fmt1's serving context:
    cygnet, schema_branch_mark, two-letter labels past Z)."""
    d = dio()
    n = len(row.get("options") or [1, 2])
    with fcard._serving(d, n):
        msg = d.user_msg(row)
    return len(tokenizer().encode(msg).ids)


def uh(*parts):
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def adverse_pos(pack_id, pred):
    return uh("f4-adverse", pack_id, pred) < 0.5


def yes_bad(form, claim, pack_id):
    p, e, pos = claim
    asked = pos if form in ("YN-F", "YN-T", "YN-dn", "YN-O", "YN-nR") else (not pos)
    return asked == adverse_pos(pack_id, p)


def pick_style(cp, row_key, exclude=()):
    st = [s for s in cp.styles if s not in exclude]
    if not st:
        return None
    sid = sorted(st)[int(uh("f4-style", cp.card_id, row_key) * len(st))]
    return fpool.style(sid)


def options_for(cp, form, row, res, rng_key):
    """(option texts, gold text, canon option list, option definitions, label form)."""
    if form in ("CH-3", "CH-2"):
        labs = ["F", "R", "O"] if form == "CH-3" else ["F", "R"]
        order = list(labs)
        random.Random(uh("f4-optorder", rng_key)).shuffle(order)
        lf = flabels.label_form("F4", cp.card_id, rng_key, {"masked": 0.343, "swapped": 0.143}) \
            if not cp.short else "plain"
        if lf == "masked":
            names = cp.label_names["masked"][form]
            defs_src = L.CH3_DEFS if form == "CH-3" else L.CH2_DEFS
            texts = [names[l] for l in order]
            defs = [(names[l], defs_src[l]) for l in order]
        elif lf == "swapped":
            names = cp.label_names["swapped"][form]
            defs_src = L.CH3_DEFS if form == "CH-3" else L.CH2_DEFS
            texts = [names[l] for l in order]
            defs = [(names[l], defs_src[l]) for l in order]
        else:
            st = cp.label_names["plain"][form]
            texts = [st[labs.index(l)] for l in order]
            defs = None
        gold = texts[order.index(res["gold"])]
        return texts, gold, order, defs, lf
    if form == "CH-claim":
        texts = [R.claim_clause(o) if o is not None else L.NONE_OPTION for o in row["options"]]
        g = res["gold"]
        gold = L.NONE_OPTION if g == "NONE" else texts[g]
        return texts, gold, None, None, "plain"
    if form == "CH-entity":
        texts = list(row["options"])
        return texts, texts[res["gold"]], None, None, "plain"
    raise ValueError(form)


def decisive_ids(d):
    """Sids (and rule ids) of the row's decisive statements (G0 8; repair r1): with an OW derivation, the leaves and
    rules of solver A's minimal proof; otherwise the sampler's chain leaves for c plus the stated failing premises of
    c's near-miss chains. Values and dates of those entities that a rule reads, and links between them, count too."""
    rec, res = d["rec"], d["res"]
    b_notes = d["b"].notes if d.get("b") is not None else {"leaves": d.get("leaves", [])}   # G4 drafts carry no b
    if res.get("derivation") and res.get("leaves"):
        atoms = {tuple(l[0]) for l in res["leaves"]}
    else:
        atoms = {tuple(a) for a, v in b_notes.get("leaves", [])}
        if not res.get("derivation"):
            for nm in res.get("near_miss", []):
                a = nm["premise"][0]
                if a and a[0] == "u":
                    atoms.add(tuple(a))
    ents = {a[2] for a in atoms if a[0] == "u"}
    qread = {c[1] for r in rec.rules for c in r.conds if c[0] in ("cmp", "rng", "dcmp", "win")}
    out = set()
    for s in rec.stmts:
        if s.kind == "lit" and s.pos is not None and C.u(s.pred, s.e) in atoms:
            out.add(s.sid)
        elif s.kind in ("val", "date") and s.e in ents and s.pred in qread and s.value is not None:
            out.add(s.sid)
        elif s.kind == "link" and (C.lk(s.pred, s.e, s.value) in atoms or (s.e in ents and s.value in ents)):
            out.add(s.sid)
    for rid in res.get("rules", []) or []:
        out.add(rid)
    return out


def render_one(cp, card, d, *, unit_seed, row_key, frame=None, wording=None, style_id=None, pos_u=None):
    """Render one draft. Returns (fields, info) or raises ValueError with a reason."""
    rec, row, res = d["rec"], d["row"], d["res"]
    form = row["form"]
    rng = random.Random(uh("f4-row", row_key))
    style = fpool.style(style_id) if style_id else pick_style(cp, row_key)
    tried = []
    lx = R.Lex(cp, date_fmt=cp.date_fmt)
    fields = None
    last_err = None
    for attempt in range(4):
        if style is None:
            break
        try:
            posinfo = {}
            doc, order = R.build_doc(lx, rec, cp, style, random.Random(unit_seed), title=cp.title,
                                     decisive=decisive_ids(d), posinfo=posinfo, pos_u=pos_u)
            fr = frame or R.frame_of(form, rng)
            types_pl = cp.types[row["etyp"]][1] if form == "CH-entity" else None
            q = R.question_text(form, row.get("claim"), fr, int(uh("f4-fill", row_key) * 2),
                                types_pl=types_pl, H=row.get("H"))
            w = wording or pick_wording(cp, form, row_key)
            qtype = "noul" if form.startswith("YN") else "choice"
            if qtype == "choice":
                texts, gold_text, opt_labels, defs, lf = options_for(cp, form, row, res, row_key)
            else:
                texts, gold_text, opt_labels, defs, lf = None, None, None, None, "plain"
            standing = [r for r in rec.rules if r.where == "card"]
            cir = R.card_ir(lx, cp, standing_rules=standing, option_defs=defs, fewshot=cp.fewshot_block)
            typed = style["container"] in ("json", "yaml")
            f = fcard.render_row_text(style, doc=doc, question=q, qtype=qtype, card=cir, options=texts,
                                      wording=w["text"], allow_null=typed and (card.world or "OW") == "OW")
            gold = (1 if res["gold"] == "yes" else 0) if qtype == "noul" else gold_text
            fields = {**f, "qtype": qtype, "options": texts, "gold": gold}
            chk = fcard.loader_check({"id": row_key, **fields},
                                     must_show=fcard.must_show(cir, question=q, wording=w["text"]))
            if not chk["ok"]:
                raise ValueError("loader:" + chk["problems"][0][:40])
            info = {"style": style, "frame": fr, "wording": w, "question": q, "order": order, "label_form": lf,
                    "posinfo": posinfo,
                    "opt_labels": opt_labels, "gold_letter": chk["gold_letter"],
                    "must_show": fcard.must_show(cir, question=q, wording=w["text"])}
            return fields, info
        except (ValueError, KeyError, AssertionError) as e:
            last_err = e
            if "loader" in str(e):
                raise
            tried.append(style["id"])
            style = pick_style(cp, row_key + f"#{attempt}", exclude=tried)
    raise ValueError("render:" + (str(last_err)[:40] if last_err else "no_style"))


def pick_wording(cp, form, row_key):
    fam = cp.wording_family
    ws = [w for w in RM.F4_WORDINGS if w["wording_family"] == fam and
          ("any" in w["forms"] or ("yn" in w["forms"] and form.startswith("YN")) or
           ("choice" in w["forms"] and not form.startswith("YN")))]
    ws.sort(key=lambda w: w["id"])
    # 2.1: each card uses >= 5 wordings: units cycle through the card's pool from a per-card offset
    parts = str(row_key).split(":")
    try:
        ui = int(parts[2])
    except (IndexError, ValueError):
        return ws[int(uh("f4-wording", cp.card_id, row_key) * len(ws))]
    off = int(uh("f4-wording-off", cp.card_id, parts[1]) * len(ws))
    return ws[(off + ui) % len(ws)]
