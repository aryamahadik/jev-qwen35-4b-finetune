"""HEAD ROWS (global ruling G7). A secondary head (T50 reason + tier, T53 reason + tier) is built as extra rows: the SAME
rendered context with a separate question form and its own lettered options; gold from the same rule table; same split as
the primary row; from at most 25% of the family's specs per head, outside the family size. No new output token or suffix
field is added; if C2's layout cannot carry a second question form the head stays a manifest field plus a report line.
"""
from .canon import rng_for, stable_fraction

LETTERS = "ABCDEFG"
HEADS = {"reason": ("destroy", "exfiltrate", "weaken_security", "cross_trust", "bypass_review_or_affect_others", "supply_chain", "none"),
         "tier": ("soft", "hard", "na")}
T53_REASONS = ("exfiltrate", "supply_chain", "bypass_review_or_affect_others", "none")


def head_selected(spec, head, fraction=0.25):
    return stable_fraction("head", head, spec.group) < fraction


def head_row(spec, head, labels=None, family="T50"):
    """-> dict row for one spec and head (options shuffled per row with a seeded RNG; letters A.. in shuffled order)."""
    labels = list(labels or HEADS[head])
    rng = rng_for("head-options", spec.spec_id, head)
    order = labels[:]
    rng.shuffle(order)
    gold = getattr(spec.gold, head)
    return {"spec_id": spec.spec_id + "#" + head, "head": head, "form": "%s.Q.%s" % (family, head), "split": spec.split, "group": spec.group,
            "primary_spec": spec.spec_id, "options": {LETTERS[i]: o for i, o in enumerate(order)},
            "gold_letter": LETTERS[order.index(gold)], "gold": gold}


def head_rows(specs, head, labels=None, family="T50"):
    return [head_row(s, head, labels, family) for s in specs if head_selected(s, head)]
