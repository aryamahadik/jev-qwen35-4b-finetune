"""Template / table hash export for T51."""
from LA_COMMON.canon import sha_obj
from LA_COMMON.wording import FORMS

from . import blocks, model
from .generator import CARD_IDS


def t51_hashes():
    cells = [(c.block, c.kind, tuple(sorted((k, str(v)) for k, v in c.extras.items() if k != "idx"))) for c in blocks.plan()]
    h = {
        "oracle": sha_obj({"label_order": ["M empty", "must", "protected", "authorised", "ask"], "slt1": "C1-C4 via Protected", "ask_on_soft": False}),
        "id_formats": sha_obj(model.id_formats()),
        "block_plan": sha_obj(cells),
        "cards": sha_obj(CARD_IDS),
        "forms": sha_obj({k: v for k, v in sorted(FORMS.items()) if v["family"] == "T51"}),
    }
    h["template_hash"] = sha_obj(h)
    return h
