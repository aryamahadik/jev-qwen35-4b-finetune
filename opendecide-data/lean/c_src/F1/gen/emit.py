"""Emit F1 rows: render through fmt1 (render_row_text + loader_check), measure the served prompt with the real
tokenizer, and run the per-row gates inline: G3 (parse back + solver B + structure compare + hash), G2 (solver B gold
and depth = solver A's), G15 per-row part (loader_check incl. check_rows and gold-letter map-back), length < 2,000.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
from functools import lru_cache

import lexicon as L
import parse_f1 as PF
import solver_a as A
import solver_b as SB
from canon import structure_hash
from cards import card_statements
from common import GEN_VERSION, LICENCE, SEED, SOURCE, SPEC_ID, rng_for, unit
from model import Struct
from render_f1 import (Fmt, RenderFail, build_doc, card_ir_choice, card_ir_q3, interp_items, q2_option_text,
                       question)
import negcount

from fmt1 import card as fcard
from fmt1 import pool as fpool
from fmt1.render import FormatError

LEN_CAP = 2000
# r3 (A22; tmp/repair/INFEASIBLE_length.md): Q2 rows only, hard cap <= 7,900 tokens (A16); other question types keep
# the < 2,000 cap, which they can meet. The mixer enforces the mix-level cap on rows >= 2,000 tokens.
LEN_CAP_A22 = 7901
LONG_UNIT = 2000   # G15: a relation unit holding a row >= 2,000 tokens keeps <= 2 rows


def len_cap(qtype):
    return LEN_CAP_A22 if qtype == "Q2" else LEN_CAP
N_PERMS = 16


class GateFail(Exception):
    pass


@lru_cache(maxsize=1)
def tokenizer():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")


def prompt_len(row) -> int:
    """Max real-tokenizer length of the full served prompt (cygnet, schema_branch_mark, chat template with the system
    turn) over the canonical, reversed and 16 seeded option orders (both Yes / No orders on yes/no rows)."""
    dio = fcard._dio()
    tok = tokenizer()
    n = 2 if row["qtype"] == "noul" else len(row["options"])
    perms = [list(range(n)), list(range(n))[::-1]]
    if row["qtype"] != "noul":
        rng = random.Random(int(hashlib.sha256(row["id"].encode()).hexdigest()[:8], 16))
        for _ in range(N_PERMS):
            p = list(range(n))
            rng.shuffle(p)
            perms.append(p)
    best = 0
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    try:
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        if n > len(dio.WIDE):
            import string
            U = string.ascii_uppercase
            dio.WIDE = list(U) + [a + b for a in U for b in U]
        seen = set()
        for p in perms:
            if tuple(p) in seen:
                continue
            seen.add(tuple(p))
            user = dio.user_msg(row, p)
            text = dio.render_chat(tok, dio.CYGNET_SYSTEM, user)
            best = max(best, len(tok(text, add_special_tokens=False)["input_ids"]))
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved
    return best


def pick_style(card, row_key, doc, held_out=False, exclude_flags=()):
    ids = list(card["style_pool"])
    ids.sort(key=lambda s: unit("style", card["card_id"], row_key, s))
    for sid in ids:
        st = fpool.dev_style(sid) if held_out else fpool.training_style(sid)
        if any(st["flags"].get(f) for f in exclude_flags):
            continue
        from fmt1.render import can_render
        if can_render(doc, st):
            return st
    raise RenderFail("no style in the card's set renders this doc")


def pick_wording(card, row_key, idx=None):
    ws = card["wordings"]
    if idx is not None:
        return ws[int(idx) % len(ws)]
    return ws[int(unit("wording", card["card_id"], row_key) * len(ws))]


def options_and_gold(card, row):
    q = row["q"]
    qt = q["qtype"]
    if qt == "Q3":
        return None, row["gold"], None
    if qt == "Q1":
        opts = [card["cbd_label"] if o == A.CBD else card["display"][o] for o in row["options"]]
        g = card["cbd_label"] if row["gold"] == A.CBD else card["display"][row["gold"]]
        return opts, g, list(row["options"])
    if qt == "Q2":
        opts = [q2_option_text(card, p) for p in row["options"]]
        g = q2_option_text(card, row["gold"])
        return opts, g, list(row["options"])
    if qt == "Q4":
        opts = [card["none_label"] if o == "__NONE__" else o for o in row["options"]]
        g = card["none_label"] if row["gold"] == "__NONE__" else row["gold"]
        return opts, g, list(row["options"])
    raise ValueError(qt)


def render_row(card, pack, row, rid, held_out=False):
    """-> (row fields dict, must_show list, style, wording id)."""
    S = row["S"]
    cases = row["cases"]
    q = row["q"]
    # r3 pass E: a matched contrast twin (build.TWIN_SURFACE_MATCH_QTYPES) renders with its base row's key, so its
    # render draws, format style and wording equal the base row's; every other row keys on its own id as before
    skey = row.get("_surface_key") or rid
    rng = rng_for("render", skey)
    fm = Fmt(card, S)
    stmts = card["_stmts"]
    illus = card.get("illus", {})
    if card["qtype"] == "Q4":
        case_mode = "record" if S.policy.world != "open" else "prose"
    elif S.policy.world == "open" or card["sampler"] == "S4" or rng.random() < 0.35:
        case_mode = "prose"
    else:
        case_mode = "record"
    sampler = card["sampler"] if not held_out else "S1"
    doc = build_doc(card, S, cases, fm, rng, stmts, illus, attack=row.get("attack"), case_mode=case_mode,
                    sampler=sampler, q4_refs=row.get("q4_refs"))
    qtext = question(card, q, rng)
    opts, gold, canon_opts = options_and_gold(card, row)
    qtype = "noul" if q["qtype"] == "Q3" else "choice"
    if q["qtype"] == "Q3":
        cir = card_ir_q3(card, stmts, illus, card.get("few_cases"))
    else:
        cir = card_ir_choice(card, stmts) if not card["short"] else None
        if card["short"] and q["qtype"] == "Q1":
            cir = None
    excl = ("rewrites_keys",) if q["qtype"] == "Q4" else ()
    st = pick_style(card, skey, doc, held_out, exclude_flags=excl)
    wid = pick_wording(card, skey, row.get("wording_idx"))
    wtext = card["wording_text"][wid]
    if card["short"] and cir is not None and q["qtype"] == "Q3":
        cir = None
    fields = fcard.render_row_text(st, doc=doc, question=qtext, qtype=qtype, card=cir, options=opts, wording=wtext)
    must = fcard.must_show(cir, question=qtext, wording=wtext)
    ii = interp_items(card, stmts, illus) if (q["qtype"] != "Q3" and not card["short"]) else None
    if ii:
        must += list(ii["items"])
    if q["qtype"] == "Q4":
        must += [c.ref for c in cases]
    return fields, must, st, wid, opts, gold, canon_opts, qtext


def to_display_struct(card, S: Struct, cases, q):
    """Drawn structure with names: field keys -> field names, outcomes -> display names (for the G3 compare)."""
    import copy
    from model import Attr, Case, Item, Lit, Notice, Policy, Rule
    k2n = {k: a.name for k, a in S.attrs.items()}
    D = lambda o: card["display"].get(o, o) if o is not None else None  # noqa: E731

    def lit(m):
        return Lit(k2n[m.attr], m.op, m.args)

    def rule(r):
        if r is None:
            return None
        return Rule(r.rid, r.kind, tuple(Item(it.kind, tuple(lit(m) for m in it.mem), it.k) for it in r.items),
                    lit(r.unless) if r.unless is not None else None, D(r.out), r.target, r.tier, r.date, r.last)
    attrs = {}
    for k, a in S.attrs.items():
        attrs[a.name] = Attr(**{**a.__dict__, "key": a.name, "presup": k2n.get(a.presup) if a.presup else None})
    P = S.policy
    pol = Policy(world=P.world, prim=P.prim, sec=P.sec, tie=P.tie, strict=tuple(D(x) for x in P.strict),
                 outcomes=tuple(D(x) for x in P.outcomes), roles={}, valence={}, default=D(P.default),
                 escalate=D(P.escalate), fallback=D(P.fallback), M=D(P.M), gov=k2n[P.gov], body=P.body, B=P.B,
                 listed=tuple(k2n[k] for k in P.listed), tiers=P.tiers, scope_name=P.scope_name,
                 scope_value=P.scope_value)
    from model import Inert
    inert = []
    for e in S.inert:
        inert.append(Inert(e.cls, e.num, Notice(e.notice.num, e.notice.ntype, e.notice.target, rule(e.notice.rule),
                                                e.notice.ndate, e.notice.edate, e.notice.pos) if e.notice else None,
                           rule(e.rule), e.scope_value, e.body, e.text))
    S2 = Struct(attrs=attrs, rules=[rule(r) for r in S.rules],
                notices=[Notice(n.num, n.ntype, n.target, rule(n.rule), n.ndate, n.edate, n.pos) for n in S.notices],
                inert=inert, policy=pol, order=list(S.order), s3_rows=list(S.s3_rows) if S.s3_rows else None)
    cs = [Case({k2n[k]: v for k, v in c.vals.items()}, frozenset(k2n[k] for k in c.unknown),
               frozenset(k2n[k] for k in c.notrec), c.ref) for c in cases]
    q2 = dict(q)
    if q.get("X") is not None:
        q2["X"] = D(q["X"])
    return S2, cs, q2


def _rule_key(r):
    if r is None:
        return None
    return (r.rid, r.kind, tuple(sorted(repr((it.kind, tuple(sorted(map(repr, it.mem))), it.k)) for it in r.items)),
            repr(r.unless), r.out, r.target, r.tier, r.date, r.last)


def compare(card, drawn, parsed, row) -> list:
    """Exact compare before name abstraction (names, ids, values, option map). Returns the differences."""
    S, cases, q = drawn
    P2 = parsed["S"]
    diffs = []
    if set(S.attrs) != set(P2.attrs):
        diffs.append(("attrs", sorted(set(S.attrs) ^ set(P2.attrs))))
    else:
        for n, a in S.attrs.items():
            b = P2.attrs[n]
            fields = ["type", "values"]
            if a.type == "num":
                fields += ["unit", "step", "lo", "hi", "daycount"]
            if a.type == "date" and S.policy.world == "open":
                fields += ["lo", "hi"]
            if a.type == "bool":
                fields += ["true", "false", "presup"]
            for f in fields:
                if getattr(a, f) != getattr(b, f):
                    diffs.append(("attr", n, f, getattr(a, f), getattr(b, f)))
    if [_rule_key(r) for r in S.rules] != [_rule_key(r) for r in P2.rules] and \
            sorted(map(repr, map(_rule_key, S.rules))) != sorted(map(repr, map(_rule_key, P2.rules))):
        diffs.append(("rules",))
    nk = lambda n: (n.num, n.ntype, n.target, repr(_rule_key(n.rule)), n.ndate, n.edate, n.pos)  # noqa: E731
    if sorted(map(repr, map(nk, S.notices))) != sorted(map(repr, map(nk, P2.notices))):
        diffs.append(("notices",))
    ic = lambda xs: sorted(e.cls for e in xs)  # noqa: E731
    if ic(S.inert) != ic(P2.inert):
        diffs.append(("inert", ic(S.inert), ic(P2.inert)))
    pa, pb = S.policy, P2.policy
    for f in ("world", "prim", "sec", "default", "M", "gov", "body", "B", "tiers", "scope_name", "scope_value"):
        if getattr(pa, f) != getattr(pb, f):
            diffs.append(("policy", f, getattr(pa, f), getattr(pb, f)))
    if pa.prim != "ORDER":
        if pa.tie != pb.tie or pa.strict != pb.strict:
            diffs.append(("tie",))
        if pa.tie == "esc" and pa.escalate != pb.escalate:
            diffs.append(("escalate",))
    if 7 in parsed["shown"] and pa.fallback != pb.fallback:
        diffs.append(("fallback",))
    if tuple(pa.listed) != tuple(pb.listed):
        diffs.append(("listed",))
    if S.order != P2.order:
        diffs.append(("order", S.order, P2.order))
    if (S.s3_rows or None) != (P2.s3_rows or None):
        diffs.append(("s3_rows",))
    pc = parsed["cases"]
    if len(pc) != len(cases):
        diffs.append(("ncases",))
    else:
        for c, d in zip(cases, pc):
            if c.ref != d.ref:
                diffs.append(("ref", c.ref, d.ref))
            if c.vals != d.vals:
                diffs.append(("vals", {k: (c.vals.get(k), d.vals.get(k)) for k in set(c.vals) | set(d.vals)
                                       if c.vals.get(k) != d.vals.get(k)}))
            if c.unknown != d.unknown or c.notrec != d.notrec:
                diffs.append(("unknown/notrec",))
    pq = parsed["q"]
    if pq["qtype"] != q["qtype"] or pq.get("X") != q.get("X") or pq.get("pol") != q.get("pol"):
        diffs.append(("query", q, pq))
    return diffs


def gate_row(card, pack, row, out_row, vocab, canon_opts):
    """G3 + G2 on one emitted row. Raises GateFail with the reason."""
    try:
        parsed = PF.Parser(out_row, vocab).parse()
    except PF.ParseError as e:
        raise GateFail(f"parse: {e}")
    import validators as V
    try:
        V.check_all(parsed["S"])
    except V.Violation as e:
        raise GateFail(f"validator: {e}")
    drawn = to_display_struct(card, row["S"], row["cases"], row["q"])
    d = compare(card, drawn, parsed, row)
    if len(parsed["injected"]) != (1 if row.get("attack") else 0):
        d.append(("injected", len(parsed["injected"])))
    if d:
        raise GateFail(f"compare: {str(d)[:300]}")
    # solver B on the parsed structure
    try:
        b = SB.answer(parsed["S"], parsed["q"], parsed["cases"])
    except SB.BError as e:
        raise GateFail(f"solverB: {e}")
    q = row["q"]
    if q["qtype"] == "Q3":
        want = out_row["gold"]
        if b != want:
            raise GateFail(f"solverB gold {b} != {want}")
    else:
        po = parsed["options"]
        gi = out_row["options"].index(out_row["gold"])
        if po[gi] != b:
            raise GateFail(f"solverB gold {b} != option {po[gi]}")
        # option map: parsed canonical options equal the drawn option set (display names)
    dB = SB.depth(parsed["S"], parsed["cases"])
    if dB != row["depth"]:
        raise GateFail(f"depth B {dB} != A {row['depth']}")
    h1 = structure_hash(*drawn)
    h2 = structure_hash(parsed["S"], parsed["cases"], parsed["q"])
    if h1 != h2:
        raise GateFail("hash mismatch")
    return h1, parsed
