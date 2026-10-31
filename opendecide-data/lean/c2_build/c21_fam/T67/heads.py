"""T67 head rows (G7): reason (7-way) and tier (3-way) questions over the SAME rendered context, gold from the same rule table, same split as the parent,
extra copies outside the 1,000, drawn from at most 25% of the family's specs per head and from SINGLE-TRIGGER specs only (K12). Derived from KEPT rows."""
import hashlib

from LP_COMMON import tokens

from . import config as C
from . import rows as ROWS

HEAD_SHARE = 0.25


def _pick(spec_id, head):
    return int(hashlib.sha256(("T67-head|%s|%s" % (head, spec_id)).encode()).hexdigest(), 16) % 1000 < int(HEAD_SHARE * 1000)


def extra_rows(ctx, kept):
    """Head rows for kept GATE rows whose spec is single-trigger, non-ALLOW, once per spec (the neither cell)."""
    out, seen = [], set()
    for r in kept:
        m = r["meta"]
        if m.get("head") != "GATE" or not m.get("single_trigger") or r["gold"] == "ALLOW" or m.get("cell") != "neither" or m["spec_id"] in seen:
            continue
        seen.add(m["spec_id"])
        for head in ("REASON", "TIER"):
            if _pick(m["spec_id"], head):
                out.append(_derive(ctx, r, head))
    return out


def _derive(ctx, parent, head):
    form = C.QUESTION_FORMS[head]
    rng = ctx.rng("t67head", parent["row_id"], head)
    qw, question = ctx.picker.render(form, ask=ROWS.ASK_SLOT[head])
    triple = parent["gold_triple"]
    gold = triple["reason"] if head == "REASON" else triple["tier"]
    labels, texts = (C.REASONS, ROWS.REASON_TEXT) if head == "REASON" else (C.TIERS, ROWS.TIER_TEXT)
    options = ROWS._options(labels, texts, gold, rng)
    options_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    ctx_text = parent["rendered"]["context"]
    text = "\n\n".join([ctx_text, question, options_text])
    rec = {k: parent[k] for k in ("family", "sub_block", "group_id", "names", "spec", "decision_spans", "gold_triple", "decisive")}
    rec.update(row_id=parent["row_id"][:-1] + head[0].lower(), head="T67-" + head, gold=gold, label=gold, gold_letter=next(o["letter"] for o in options if o["label"] == gold),
               options=options, question_form=form, slots=dict(parent["slots"]), rendered={"context": ctx_text, "question": question, "options_text": options_text, "text": text},
               witness_inputs={"carrier": parent["witness_inputs"]["carrier"], "head": head}, head_row=True,
               manifest=dict(parent["manifest"], head_of=parent["row_id"]))
    rec["meta"] = dict(parent["meta"], head=head, wording_id=qw, tokens=tokens.count(text), head_of=parent["row_id"], pair_id=None, twin_of=None, group_kind="head")
    return rec


def check_head_row(rec):
    """-> [] ok | [reason]. A head row is valid when its gold is the parent's triple component and its options are consistent."""
    why = []
    if rec["gold"] not in [o["label"] for o in rec["options"]]:
        why.append("gold_not_in_options")
    if len({o["label"] for o in rec["options"]}) != len(rec["options"]):
        why.append("options_not_unique")
    return why
