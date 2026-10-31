"""Template / table hash export for T53."""
from LA_COMMON.canon import sha_obj
from LA_COMMON.wording import FORMS

from . import blocks, cards, destination, engine, registry


def t53_hashes():
    cells = [(c.block, c.kind, c.card, tuple(sorted((k, str(v)) for k, v in c.extras.items() if k != "idx"))) for c in blocks.plan()]
    h = {
        "first_match_order": sha_obj([rid for rid, _ in engine.ORDERED_RULES]),
        "cue_list": sha_obj(list(destination.CUES)),
        "tld_list": sha_obj({"reserved": destination.RESERVED_TLDS, "special": destination.SPECIAL_TLDS, "generic": destination.GENERIC_TLDS}),
        "shapes": sha_obj({"cred": registry.CRED_SHAPES, "pii": registry.PII_SHAPES, "benign": registry.BENIGN_SHAPES}),
        "card_levers": sha_obj(cards.LEVERS),
        "block_plan": sha_obj(cells),
        "forms": sha_obj({k: v for k, v in sorted(FORMS.items()) if v["family"] == "T53"}),
    }
    h["template_hash"] = sha_obj(h)
    return h
