"""Effects and their combination (G0-lite X10 / R20, the soft-block lever, the consent clearing).

An EFFECT is what one item of the parsed file does that a rule of the table cares about. It carries the rule's label (before the card lever), reason, tier and the
clearing condition (the operation words and the target names a user turn must contain, both, for a soft effect to clear). `resolve` applies the card lever, the
consent turn and the most-restrictive-wins combination; the result is the (label, reason, tier) triple."""
from . import tables as T
from . import textview as V


class Effect(object):
    __slots__ = ("rule", "label", "reason", "tier", "c4", "ops", "targets", "note")

    def __init__(self, rule, label, reason, tier, ops=(), targets=(), c4=False, note=""):
        self.rule, self.label, self.reason, self.tier = rule, label, reason, tier
        self.ops, self.targets, self.c4, self.note = tuple(ops), tuple(targets), c4, note

    def __repr__(self):
        return "Effect(%s %s/%s/%s)" % (self.rule, self.label, self.reason, self.tier)


def is_named(effect, user_text):
    """The user turn names BOTH the operation and the target of the effect (op words are the surface phrases of the operations that can clear it)."""
    if effect.tier != "soft":
        return False
    if not any(V.names_target(user_text, t) for t in effect.targets):
        return False
    return any(V.mentions(user_text, T.OP_PHRASE[o]) for o in effect.ops)


def resolve(effects, card, user_text):
    """-> dict(label, reason, tier, live=[Effect], cleared=[Effect])."""
    live, cleared = [], []
    for e in effects:
        if e.tier == "soft" and is_named(e, user_text):
            cleared.append(e)
            continue
        lab = e.label
        if lab == "BLOCK" and e.tier == "soft" and card["ask_on_soft"] and not e.c4:
            lab = "ASK"
        live.append((lab, e))
    if not live:
        return dict(label="ALLOW", reason="none", tier="soft" if cleared else "na", live=[], cleared=cleared)
    top = max(T.SEVERITY[l] for l, _ in live)
    label = [l for l in T.LABELS if T.SEVERITY[l] == top][0]
    reasons = [e.reason for l, e in live if l == label]
    reason = [r for r in T.PRECEDENCE if r in reasons][0]
    tier = "hard" if any(e.tier == "hard" for _, e in live) else "soft"
    return dict(label=label, reason=reason, tier=tier, live=[e for _, e in live], cleared=cleared)
