"""Template / table hash export for T50 (a new export is made at EVERY later template change). Names the shas only."""
from LA_COMMON.canon import sha_obj
from LA_COMMON.expander import RESOLVER_TABLE
from LA_COMMON.render import ALL_OPERATORS, HELDOUT_OPERATORS, TRAINED_OPERATORS
from LA_COMMON.wording import FORMS

from . import cards, rules
from . import blocks
from .blocks import plan
from .generator import PAYLOAD_REGISTRY
from .intents import REGISTRY


def t50_hashes():
    intents = {i: {k: v for k, v in m.items() if k not in ("build", "expect")} for i, m in sorted(REGISTRY.items())}
    cells = [(c.block, c.intent, c.card, c.tag, c.sub, bool(c.extras.get("twin"))) for c in plan()]
    h = {
        "rule_table": rules.RULE_TABLE.sha,
        "resolver_list": RESOLVER_TABLE.sha,
        "payload_registry": PAYLOAD_REGISTRY.sha,
        "intent_registry": sha_obj(intents),
        "block_plan": sha_obj(cells),
        "card_levers": sha_obj(cards.LEVERS),
        "operators": sha_obj({"trained": TRAINED_OPERATORS, "heldout": HELDOUT_OPERATORS, "all": ALL_OPERATORS}),
        "forms": sha_obj({k: v for k, v in sorted(FORMS.items()) if v["family"] == "T50"}),
    }
    # ---- v3.2 tables (addendum sections 4-9; any change = a new export and re-stamped rows, plan 16.1 step 6)
    from LA_COMMON import perturb
    from . import blockg, cues, dialects, edit_model as em, ladder, overlays, quads
    h["g_effects"] = sha_obj({k: [e.kind, e.domain, list(e.classes), e.hard, e.benign] for k, e in sorted(blockg.G_EFFECTS.items())})
    h["g_plan"] = sha_obj({"sub_rows": blockg.SUB_ROWS, "pairs": blockg.PAIRS, "carrier_share": blockg.CARRIER_SHARE,
                           "heldout_patch_pairs": blockg.HELDOUT_PATCH_PAIRS, "shell_domain_weights": blockg.SHELL_DOMAIN_WEIGHTS})
    h["edit_templates"] = sha_obj({"lock_stems": em.LOCK_STEMS, "rc_stems": em.RC_STEMS, "hooks": em.HOOK_NAMES, "shell_classes": em.SHELL_CLASSES,
                                   "nonstate_ext": em.NONSTATE_EXT, "nonstate_dir": em.NONSTATE_DIR, "n_notes": blockg.N_NOTES, "n_hist": blockg.N_HIST})
    h["quads"] = sha_obj({"templates": {k: {"%s/%s" % c: v for c, v in tpl.items()} for k, tpl in quads.TEMPLATES.items()},
                          "a": quads.A_QUADS, "c": quads.C_QUADS, "alarm": quads.ALARM.pattern})
    from . import verdict
    h["q10_q11"] = sha_obj({"secret_content": "provenance: lines shown by a visible read of a secret-class node (Q12.1); absent visibility = unknown (Q12.1); home record visible (Q12.3)", "mirror_outside": blockg.MIRROR_OUTSIDE, "g2m_keyfile": blockg.G2M_KEYFILE,
                            "class_domain": blockg.CLASS_DOMAIN, "reason_precedence": list(verdict.REASON_PRECEDENCE)})
    h["ladder"] = sha_obj({"m3": ladder.M3_WARNINGS, "m5_cycle": blocks.M5_CYCLE, "m4_cells": blocks.M4_CELLS})
    h["cue_pool"] = cues.pool_sha()
    h["dialects"] = sha_obj({"ids": list(dialects.ALL_DIALECTS), "scaffold": dialects.SCAFFOLD_SHA})
    h["perturb"] = sha_obj(list(perturb.ALL_TRANSFORMS))
    h["overlays"] = sha_obj({"a6": cues.A6_ROWS, "pert": overlays.PERT_ROWS, "heldout": overlays.HELDOUT_TARGETS, "a10_built": overlays.A10_BUILT})
    try:
        from . import intents_alias, intents_late
        h["alias_table"] = intents_alias.ALIAS_TABLE.sha
        h["late_table"] = intents_late.LATE_TABLE.sha
    except ImportError:
        h["alias_table"] = h["late_table"] = "pending"
    h["template_hash"] = sha_obj(h)
    return h
