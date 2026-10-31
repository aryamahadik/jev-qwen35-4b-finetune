"""T67 policy cards card.t67.c01..c06: each EXTENDS T50's card of the same index. The T50 slots that matter here (ask_on_soft, digest_pin_requirement)
are copied unchanged (`conforms_to_t50()` is a CPU test against T50's own LEVERS; the digest slot reads "required" on every card and is rendered "fetched scripts need a
checksum: yes"); T67 adds pin_policy (its OWN slot, not derived from the digest slot), trusted_principals, trusted_image_registries,
trusted_action_owners and the clause `clause.t67.lock_review` (visible only on cards that carry it; T50 cards never do). Display names come from
ns.policy_card; the lists come from the per-spec-family seeded namespace so a card-swap pair (same change and state under two cards) differs ONLY in
the lever slots."""
from . import config as C


def make_card(card_id, names, tag="card"):
    lv = C.LEVERS[card_id]
    k = tag
    card = {
        "card_id": card_id, "display_name": names.get("ns.policy_card", card_id),
        "ask_on_soft": lv["ask_on_soft"], "digest_pin_requirement": lv["digest"], "pin_policy": lv["pin_policy"], "lock_review": lv["lock_review"],
        "context_lists": {"contained": [names.get("ns.context", k + ".c%d" % i) for i in range(2)], "shared": [names.get("ns.context", k + ".s0")],
                          "production": [names.get("ns.context", k + ".p0")]},
        "database_lists": {"contained": [names.get("ns.database", k + ".dc0")], "shared": [names.get("ns.database", k + ".ds0")],
                           "production": [names.get("ns.database", k + ".dp0")]},
        "trusted_hosts": [names.get("ns.registry_host", k + ".th%d" % i) for i in range(2)],
        "trusted_image_registries": [names.get("ns.registry_host", k + ".ir%d" % i) for i in range(2)],
        "trusted_action_owners": [names.get("ns.org", k + ".ao%d" % i).lower().replace(" ", "-") for i in range(2)],
        "trusted_principals": [names.get("ns.handle", k + ".tp%d" % i) for i in range(3)],
    }
    return card


def render_card(card, carrier):
    lines = ["Policy card %s" % card["display_name"]]
    cl, dl = card["context_lists"], card["database_lists"]
    if carrier == "MIGRATION_SQL":
        lines += ["contained databases: %s" % ", ".join(dl["contained"]), "shared databases: %s" % ", ".join(dl["shared"]),
                  "production databases: %s" % ", ".join(dl["production"])]
    else:
        lines += ["contained contexts: %s" % ", ".join(cl["contained"]), "shared contexts: %s" % ", ".join(cl["shared"]),
                  "production contexts: %s" % ", ".join(cl["production"])]
    if carrier in ("PLAN_JSON", "K8S_MANIFEST"):
        lines.append("trusted principals: %s" % ", ".join(card["trusted_principals"]))
    if carrier in ("K8S_MANIFEST", "CI_WORKFLOW"):
        lines.append("trusted image registries: %s" % ", ".join(card["trusted_image_registries"]))
    if carrier == "CI_WORKFLOW":
        if card["digest_pin_requirement"] != "required":
            raise ValueError("the digest-pin slot carries the one value 'required' on every card (GF8 as amended 18 Oct); rendering 'yes' for %r would be false" % card["digest_pin_requirement"])
        lines += ["trusted action owners: %s" % ", ".join(card["trusted_action_owners"]), "trusted hosts: %s" % ", ".join(card["trusted_hosts"]),
                  "fetched scripts need a checksum: yes"]
    lines.append("soft blocks are raised to ASK: %s" % ("yes" if card["ask_on_soft"] else "no"))
    if card["pin_policy"] == "tag_ok" and carrier in ("K8S_MANIFEST", "CI_WORKFLOW"):
        lines.append("tags from trusted sources are acceptable for images and actions")
    if card["lock_review"] and carrier == "MIGRATION_SQL":
        lines.append("migration lock review: on")
    return "\n".join(lines)


def parse_card(text, carrier):
    """Round trip: the card block back into the fields the engine reads."""
    out = {}
    for ln in text.split("\n"):
        if ln.startswith("Policy card "):
            out["display_name"] = ln[len("Policy card "):]
        elif ": " in ln:
            k, v = ln.split(": ", 1)
            out[k] = v
    return out


def conforms_to_t50():
    """-> list of mismatches between T67's copied slots and T50's own LEVERS (empty = conforms). Needs T50 importable."""
    import importlib
    try:
        t50 = importlib.import_module("T50.cards")
    except Exception as e:                                           # noqa: BLE001
        return ["T50.cards not importable: %s" % type(e).__name__]
    bad = []
    for cid, t50id in C.T50_CARD_OF.items():
        lv50 = t50.LEVERS[t50id]
        if lv50["ask_on_soft"] != C.LEVERS[cid]["ask_on_soft"]:
            bad.append("%s ask_on_soft" % cid)
        if lv50["digest"] != C.LEVERS[cid]["digest"]:
            bad.append("%s digest" % cid)
    return bad
