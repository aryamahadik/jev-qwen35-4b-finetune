"""c2_build/families/T12/wording_screen.py: generation-time screen of the T12 question wordings (pilot fix iteration 1).

Two label-blind text rules, both read from the wording text and its form only (never a row, a gold or a deciding check):

  premise   a wording must not tie its answer to what the policy decides (pilot F1: three ch_price_line wordings said the
            failing price line "drives" / "shapes" the result and a fourth that the treatment "points to" it, while G0 R16
            sets the gold to the line that fails the price check whatever decides the action; on 8 of 1,001 pilot rows
            another check decided and the literal answer was "none"). The same premise breaks G0 R18 for the two
            price-check-on-its-own forms ("does what the policy decides ... mean it fails the price check ...").
  polarity  c2_kit.polarity P1-P3 with the T12 negative predicates (plugin.NEGATIVE_PREDICATES): a held-out yn_dneg_release
            wording opens with a contracted negative frame ("Isn't it accurate that ... is not released ...") that reads
            either way (rule P3).

`problems(text, qform, plugin)` is what plugin.ctx_for() runs on every wording skin: a failing wording is quarantined
(never picked, never relabelled) and the rows are generated from the rest. authoring.check_wording(..., screen=True)
applies the same rules to a re-authored wording. Nothing here reads or writes a file.
"""
from __future__ import annotations

import re

# qform -> (regex of banned words on the wording text, the reason it is banned). Lower case, word boundaries.
PREMISE_BANNED = {
    "ch_price_line": (
        re.compile(r"\b(?:driv(?:e|es|en|ing)|shap(?:e|es|ed|ing)|decid(?:e|es|ed|ing)|settl(?:e|es|ed|ing)|"
                   r"determin(?:e|es|ed|ing)|points?\s+to|pointing\s+to)\b", re.I),
        "F1: the wording ties the failing line to what the policy decides; G0 R16 gives the line that fails the price "
        "check whatever decides the action"),
    "yn_over_tol": (
        re.compile(r"\b(?:decid(?:e|es|ed|ing)|decision|means?)\b", re.I),
        "G0 R18: the price check is judged on its own, whatever the check order decides; the wording must not tie it "
        "to the policy's decision"),
    "yn_within_tol": (
        re.compile(r"\b(?:decid(?:e|es|ed|ing)|decision|means?)\b", re.I),
        "G0 R18: the price check is judged on its own, whatever the check order decides; the wording must not tie it "
        "to the policy's decision"),
}


def premise_problems(text: str, qform: str) -> list:
    """Premise rule of one wording: [] or the banned words found and why."""
    rule = PREMISE_BANNED.get(qform)
    if rule is None:
        return []
    rx, why = rule
    hits = sorted({m.group(0).lower() for m in rx.finditer(text or "")})
    return [f"premise: {hits} ({why})"] if hits else []


def problems(text: str, qform: str, plugin) -> list:
    """Premise + polarity problems of one wording ([] = it may be picked). plugin: the T12 plugin class or instance
    (POLARITY_CHECK / POLARITY_NEGATIVES)."""
    from c2_kit import polarity as POL
    return premise_problems(text, qform) + POL.form_problems(plugin, qform, text)
