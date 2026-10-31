"""Few-shot worked examples (G0 spec 7.5; repair r1: the 7 planned few-shot cards had no block, G10 found 0).
A few-shot card hosts yes/no rows only (F4's few-shot cards are feature-rich OW yes/no cards), so every worked example
is a yes/no question with the answer "Yes" or "No" (the row's own answer text, LR11). Examples use the card's reserved
example-only names (EX-0001..3, never a record ID) and the card's three reserved example predicates (never in any
record on the card), only features the card plan has (forward rule, contrapositive on OW, exception when the card
has exceptions), and the card's own question frames. Each example is solved by solver A's labeller under the card's
own flags (core.base_view on the card); fmt1 lays the block out with a training few-shot template.
"""
from __future__ import annotations

import hashlib

import core as C
import f4lex as L
import render_f4 as R
import solve_a as A

# block templates whose chrome the G3 parser classes as card-example chrome (section 4); FT10 / FT18 need a reason
# line, FT04 / FT09 / FT16 / FT17 are one-line tables or JSON, FT07 / FT13 put the answer inside prose
TEMPLATES = ("FT01", "FT02", "FT03", "FT05", "FT06", "FT08", "FT11", "FT12", "FT14", "FT15")

YES = {"YN-F": "F", "YN-R": "R", "YN-O": "O"}
FRAMES = {"YN-F": "Does the record establish that {X} is {P}?", "YN-R": "Does the record rule out that {X} is {P}?",
          "YN-O": "Does the record leave open whether {X} is {P}?"}


def _uh(*parts):
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def _label(card, ents, facts, rules, exc, claim):
    """Solver A's OW labeller (core) on a mini record: F / R / O for claim (pred, e, pos)."""
    stmts = [C.Stmt(sid=f"x{i}", kind="lit", e=e, pred=p, pos=v) for i, (e, p, v) in enumerate(facts)]
    preds = {}
    for r in rules:
        for c in r.conds:
            preds[c[1]] = 0
        preds[r.head[0]] = 0
        if r.exc:
            preds[r.exc] = 0
    rec = C.Record(types=[("t", "ts")], ents={e: 0 for e in ents}, preds=preds, exc_preds=set(exc), rules=rules,
                   stmts=stmts, closures=[])
    rec.extras = {"derived": {r.head[0] for r in rules}}
    view = C.base_view(rec, card, world="OW")
    g = C.ground(view)
    return C.label_ow_up(g, A.claim_lit(claim))


def make_block(cp, card):
    """The card's few-shot block (fmt1 card IR) or None."""
    if not getattr(cp, "fewshot", False) or (card.world or "OW") != "OW":
        return None
    lx = R.Lex(cp, date_fmt=cp.date_fmt)
    tsg = lx.card_type()[0]
    a, h, cx = cp.example_preds
    x1, x2, x3 = L.EXAMPLE_IDS
    rule = C.Rule(rid="xr1", form="univ", typ=0, conds=(("lit", a, True),), head=(h, True))
    rtxt = f"Every {tsg} that is {a} is {h}."
    cands = [
        # (ents, facts, rules, exc preds, record text, form, claim)
        ([x1], [(x1, a, True)], [rule], (), f"{x1} is {a}. {rtxt}", "YN-F", (h, x1, True)),
        ([x2], [(x2, h, True)], [rule], (), f"{x2} is {h}. {rtxt}", "YN-F", (a, x2, True)),
        ([x2], [(x2, h, True)], [rule], (), f"{x2} is {h}. {rtxt}", "YN-O", (a, x2, True)),
        ([x3], [(x3, h, False)], [rule], (), f"{x3} is not {h}. {rtxt}", "YN-R", (a, x3, True)),
    ]
    if "exc" in cp.feats and "6" in cp.clause_set:
        rule_e = C.Rule(rid="xr2", form="univ", typ=0, conds=(("lit", a, True),), head=(h, True), exc=cx)
        etxt = f"Every {tsg} that is {a} is {h}, unless it is {cx}."
        cands.append(([x3], [(x3, a, True), (x3, cx, True)], [rule_e], (cx,), f"{x3} is {a} and is {cx}. {etxt}",
                      "YN-F", (h, x3, True)))
    order = sorted(range(len(cands)), key=lambda i: _uh("f4-fewshot-pick", cp.card_id, i))
    n = 1 + int(_uh("f4-fewshot-n", cp.card_id) * 2)     # 1-2 examples (7.5 allows 1-3; the 7.6 length cap)
    picked, used_ids = [], set()
    for i in order:
        ents, facts, rules, exc, txt, form, claim = cands[i]
        if ents[0] in used_ids:
            continue
        lab = _label(card, ents, facts, rules, exc, claim)
        if lab not in ("F", "R", "O"):
            raise ValueError("fewshot_label")
        ans = "Yes" if YES[form] == lab else "No"
        q = FRAMES[form].format(X=claim[1], P=claim[0])
        picked.append({"case": f"Record: {txt} Question: {q}", "answer": ans, "note": None,
                       "_check": {"form": form, "label": lab, "record": txt, "question": q}})
        used_ids.add(ents[0])
        if len(picked) == n:
            break
    tpl = TEMPLATES[int(_uh("f4-fewshot-tpl", cp.card_id) * len(TEMPLATES))]
    return {"template": tpl, "examples": picked}


def block_ir(block):
    """The block without the private check fields (what fmt1 renders)."""
    if not block:
        return None
    return {"template": block["template"],
            "examples": [{k: v for k, v in e.items() if not k.startswith("_")} for e in block["examples"]]}
