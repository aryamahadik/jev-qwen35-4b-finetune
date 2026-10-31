"""Card examples (section 5; F9-A49): definition examples and few-shot cases, each program-computed on its own
one-record Struct under the card's SEM, in a closed example grammar that the G3 clause parser re-solves with solver B
(f9g3.check_examples). Grammar (card text only):
  EX_MEET  "A <rec> with <col> <value> meets '<atom>'."  /  "... does not meet '<atom>'."
  EX_TERM  "A <rec> with (<col> <value>; <col> <value>) counts as <term>."  /  "... does not count as <term>."
  FS_MEET  "A <rec> with <col> <value>: does it meet '<atom>'?"            answer Yes / No
  FS_TERM  "A <rec> with (<col> <value>; ...): does it count as <term>?"   answer Yes / No
Values use the card's T21 formats and units; atoms use the card's closed comparator phrases."""
from __future__ import annotations

import random
from fractions import Fraction

from f9fmt import fmt_num, to_frac
from f9render import cell_text, lit_amount, dp_for

FS_TEMPLATES = ["FT01", "FT02", "FT03", "FT05", "FT06", "FT07", "FT08", "FT09", "FT11", "FT12", "FT13", "FT14",
                "FT15", "FT16"]


def ex_col(card):
    """(record noun, numeric column) for the comparison examples."""
    sc = card["schema"]
    s = card["sampler"]
    if s in ("S1", "S2", "S4"):
        return sc["rec_sg"], sc["nums"][0]
    if s == "S3":
        return sc["ev_sg"], sc["fact_nums"][0]
    if s == "S6":
        return "line", sc["numf"]
    m = sc["measure"]
    return sc["ent_sg"] + " value", {"name": m["name"], "type": "num", "unit": m["unit"], "dp": 0,
                                     "lo": Fraction(0), "hi": Fraction(500), "step": Fraction(1)}


def full_fm(card):
    sem = card["sem"]
    return {"nf": sem["nf"], "df": sem["df"], "tf": sem.get("tf") or "hm", "zone": sem.get("zone", 0),
            "null_tok": sem["null_tok"], "bool": sem["bool"], "csv": sem.get("csv") or ",",
            "round_dp": sem["round_dp"]}


def num_atom_text(col, ph, x, fm):
    amt = lit_amount(x, col["unit"], dp_for(x, col["dp"]), fm)
    return f"{col['name']} is {ph.replace('{X}', amt)}"


def _val(col, v, fm):
    if col["type"] == "num":
        return lit_amount(v, col["unit"], col["dp"], fm)
    return cell_text(v, col, fm)


def meet_case(card, rng, want):
    """One comparison case: (rec, col, value, atom_text, holds)."""
    from f9lex import CMP_T10
    from f9solve_a import cmp_op
    rec, col = ex_col(card)
    fm = full_fm(card)
    phs = [p for p in card["cmp_amount"] if CMP_T10[p] not in ("=", "!=")]
    ph = rng.choice(phs)
    op = CMP_T10[ph]
    step = col.get("step") or Fraction(1, 10 ** col["dp"])
    lo, hi = to_frac(col["lo"]), to_frac(col["hi"])
    k = int((hi - lo) / step)
    x = lo + step * rng.randint(max(1, int(k * 0.3)), max(1, int(k * 0.7)))
    for d in ([0, 1, -1, 2, -2] if rng.random() < 0.6 else [1, -1, 0, 2, -2]):
        v = x + d * step
        if cmp_op(v, op, x) == want and v > 0:
            return rec, col, v, num_atom_text(col, ph, x, fm), want
    raise ValueError("no comparison case")


def term_case(card, rng, tn, want):
    """One term case on a one-record Struct: (rec, [(col, value)], holds), solved by solver A."""
    from f9ast import term_cols
    from f9render import coldef
    from f9samp import gen_value
    from f9solve_a import SolverA
    sc = card["schema"]
    t = card["terms"][tn]
    cols = [coldef(card, c) for c in term_cols(t)]
    idc = {"name": card["idcol"], "type": "id"}
    for _ in range(400):
        vals = [gen_value(card, c, rng) for c in cols]
        if any(v is None for v in vals):
            continue
        if rng.random() < 0.5:  # aim at the boundary of the first numeric condition
            for j, c in enumerate(cols):
                if c["type"] == "num":
                    lits = [a["lit"] for a in _term_atoms(t) if a.get("col") == c["name"] and "lit" in a]
                    if lits:
                        x = to_frac(rng.choice(lits)) + rng.choice([-1, 0, 0, 1]) * c["step"]
                        if to_frac(c["lo"]) <= x <= to_frac(c["hi"]):
                            vals[j] = x if c["dp"] else Fraction(int(x))
                    break
        st = {"sampler": card["sampler"], "tables": [{"role": "main", "cols": [idc] + cols,
                                                       "rows": [[sc["prefix"] + "-0001"] + vals]}]}
        try:
            a = SolverA(st, card).answer({"op": "lookup_p", "id": sc["prefix"] + "-0001",
                                          "p": {"k": "term", "name": tn}})
        except Exception:
            continue
        if a is want:
            return sc["rec_sg"], list(zip(cols, vals)), want
    raise ValueError("no term case")


def _term_atoms(t):
    from f9ast import atoms
    out = []
    for k in ("A", "B", "C"):
        if t.get(k):
            out += atoms(t[k])
    for a in t.get("list") or []:
        out += atoms(a)
    for o in t.get("overrides") or []:
        out += atoms(o["cond"])
    return out


def _vals_text(card, pairs, fm):
    m = card.get("masked")
    return "; ".join(f"{c['name']} {cell_text(v, c, fm, m) if c['type'] != 'num' else _val(c, v, fm)}"
                     for c, v in pairs)


def ex_meet_text(card, case, fm):
    rec, col, v, atom, holds = case
    return f"A {rec} with {col['name']} {_val(col, v, fm)} {'meets' if holds else 'does not meet'} '{atom}'."


def ex_term_text(card, tn, case, fm):
    rec, pairs, holds = case
    verb = "counts" if holds else "does not count"
    return f"A {rec} with ({_vals_text(card, pairs, fm)}) {verb} as {tn}."


def attach_examples(card, rng):
    """Definition examples on one_line_examples cards (the comparison entry, and each term entry); a few-shot block
    (2-3 worked cases, answers Yes / No) on few-shot cards. Each example is computed, never written by hand."""
    r = random.Random("f9-examples:" + card["card_id"])
    fm = full_fm(card)
    card["examples"] = None
    card["fewshot_block"] = None
    card["example_specs"] = []
    if card["defs_style"] == "one_line_examples":
        ex = {}
        # one example per definition (spec 2.1: 1-2): the served prompt prints a choice row's card twice (1.8)
        ex["Comparisons"] = [ex_meet_text(card, meet_case(card, r, r.random() < 0.5), fm)]
        for tn in card.get("terms") or {}:
            ex[tn] = [ex_term_text(card, tn, term_case(card, r, tn, r.random() < 0.5), fm)]
        card["examples"] = ex
    if card.get("fewshot"):
        items = []
        n = r.choice([2, 3])
        terms = list(card.get("terms") or {})
        for i in range(n):
            w = (i % 2 == 0) if r.random() < 0.5 else (i % 2 == 1)
            if terms and i % 2 == 0:
                tn = terms[0]
                rec, pairs, holds = term_case(card, r, tn, w)
                case = f"A {rec} with ({_vals_text(card, pairs, fm)}): does it count as {tn}?"
            else:
                rec, col, v, atom, holds = meet_case(card, r, w)
                case = f"A {rec} with {col['name']} {_val(col, v, fm)}: does it meet '{atom}'?"
            items.append({"case": case, "answer": "Yes" if holds else "No"})
        card["fewshot_template"] = r.choice(FS_TEMPLATES)
        card["fewshot_block"] = items
