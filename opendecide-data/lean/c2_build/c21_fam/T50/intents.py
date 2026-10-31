"""T50 intent registry. An INTENT is a named way to build one spec: it sets up the simulated state plus the visible
evidence, and returns the structured action. Its META is the DESIGN expectation (domain, label, reason, tier, rule,
main program); the label that ends up in a row always comes from solver A, and the generator asserts the two agree.
"""

REGISTRY = {}


def expected_for(meta, card):
    """Design label/reason/tier of an intent on a card (ask_on_soft turns soft BLOCK into ASK, except C4)."""
    label, reason, tier = meta["label"], meta["reason"], meta["tier"]
    fn = meta.get("expect")
    if fn is not None:
        label, reason, tier = fn(card)
    if tier == "soft" and label == "BLOCK" and card.get("ask_on_soft") and not meta.get("c4"):
        label = "ASK"
    return label, reason, tier


def intent(id, domain, label, reason, tier, rule, prog, soft_clear=None, c4=False, expect=None, registerable=False,
           family_part="core", ops=True):
    """Decorator. soft_clear: None -> derived from tier=='soft'; registerable: eligible as a base64 / write-then-run
    payload (K18 registry)."""
    def deco(fn):
        REGISTRY[id] = {"id": id, "domain": domain, "label": label, "reason": reason, "tier": tier, "rule": rule,
                        "prog": prog, "c4": c4, "expect": expect, "registerable": registerable,
                        "family_part": family_part, "ops": ops, "build": fn,
                        "clearable": (tier == "soft") if soft_clear is None else soft_clear}
        fn.intent_id = id
        return fn
    return deco


def build_intent(intent_id, c, v=None):
    return REGISTRY[intent_id]["build"](c, v or {})


from . import intents_fs  # noqa: E402,F401  (registers)
from . import intents_infra  # noqa: E402,F401
from . import intents_net  # noqa: E402,F401
from . import intents_misc  # noqa: E402,F401
from . import intents_alias  # noqa
from . import intents_late  # noqa
