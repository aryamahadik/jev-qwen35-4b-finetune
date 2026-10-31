"""spec_k1: the shared structured spec of lane L-K (T59 and T60; owned by L-K). The G0-lites list its fields; this module holds the
field lists the gates read and the one check that matters for every row: the TAGS (trigger id, slot kinds, edit field, control kind,
level, lever, split ...) are written by the generator and read by the gates, and are NEVER rendered into the text."""
import re

# fields every record carries (the shared pipeline needs the first group; the second group is spec_k1 metadata)
PIPELINE_FIELDS = ("family", "row_id", "group_id", "sub_block", "gold", "gold_letter", "options", "rendered", "names", "slots",
                   "wording", "template_id", "decision_spans", "parts")
SPEC_FIELDS = ("spec_id", "block", "trigger", "form", "view", "world_kind", "card_ref", "pair_role", "twin_of", "edit", "ctl", "lever_tag",
               "heldout_family", "ladder", "split", "scene", "case", "alarm")

TAG_PREFIXES = ("trg.", "edit.", "ctl.", "ladder.", "lever.", "pert.", "wrap.", "wrap_pos.", "split.", "heldout_family", "m.t59.",
                "m.t60.", "quad.", "head.", "mark.", "fact.", "ref.", "slot.", "world.t59", "form.t59", "view.", "pool.", "bucket.",
                "card.t59", "card.t60", "defs_card.", "carrier.", "verb.", "param.", "prog.", "eff.")


def rendered_tag_leaks(rec, extra_tags=()):
    """Internal ids that appear in the text of the row (must be empty). Checks every tag id the record carries plus the closed
    prefixes: a registered id never belongs in prose."""
    text = rec["rendered"]["text"]
    found = []
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)+", text):
        if tok.startswith(TAG_PREFIXES):
            found.append(tok)
    for t in extra_tags:
        if t and re.search(r"(?<![A-Za-z0-9_])" + re.escape(str(t)) + r"(?![A-Za-z0-9_])", text):
            found.append(str(t))
    return sorted(set(found))
