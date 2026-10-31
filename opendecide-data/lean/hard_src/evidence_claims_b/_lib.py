"""Helpers for the hard 'evidence_claims_b' item author (claim verification, second author):
statistical claims (percent vs percentage points, relative vs absolute risk,
correlation vs causation), time-bounded claims and claims about subgroups.
Every item is hand-written by Claude (teacher); no external model is called.
All people, organisations and places are invented.
Rationale comments in item files (# why:) are for auditing only and never reach the rows.
"""

NONE = "none of these"


def C(key, instructions, state, options, gold, difficulty, twin=None, ordered=False):
    """Choice item. options: list of (option, definition)."""
    return dict(key=key, qtype="choice", role="choice", instructions=instructions,
                state=state.strip(), options=options, gold=gold,
                difficulty=difficulty, twin=twin, ordered=ordered)


def Y(key, instructions, state, card, gold, difficulty, twin=None, role="aff"):
    """Yes/no item. card: list of (term, definition). gold 1 = yes."""
    return dict(key=key, qtype="noul", role=role, instructions=instructions,
                state=state.strip(), card=card, gold=gold,
                difficulty=difficulty, twin=twin)


def T(edits, gold, instructions=None):
    """Minimal-pair twin: list of (old, new) replacements on the state (each old must occur once)."""
    return dict(edits=edits, gold=gold, instructions=instructions)


# ---- shared verdict labels (same labels as the evidence_claims domain) ----
VERDICT = [
    ("supported", "the material in the file establishes the claim as worded, including its numbers, direction, time frame, population and any cause-and-effect wording"),
    ("refuted", "the material in the file shows that the claim as worded is false"),
    ("not enough information", "the material in the file neither establishes the claim as worded nor shows it to be false"),
]

# ---- flaw typology (items pick a subset; exactly one applies per item) ----
ERR = {
    "pp": ("percent/percentage-point mix-up", "a difference between two percentages is described as a percent change, or a relative percent change is described in percentage points"),
    "rel": ("relative change presented as absolute", "a relative change in risk is presented as if it were the change in people's actual chance of the outcome (for example a 50% relative cut described as protecting half of patients)"),
    "causal": ("causal claim from association", "the claim says one thing causes, prevents, cuts or boosts another when the evidence only shows that the two occur together"),
    "time": ("wrong time window", "the claim describes a period, date, duration or frequency that the evidence does not cover or does not match"),
    "subgroup": ("subgroup finding generalised", "a result found in one group of people is stated for a wider or different group"),
    "count": ("counts compared instead of rates", "raw totals are compared between groups or periods of very different size when the claim is about how likely or how common something is"),
    "base": ("base-rate confusion", "the share of cases that have a trait is read as the chance that people with the trait become cases, ignoring how common the trait is"),
    "baseline": ("cherry-picked starting point", "a trend or change is measured from an unusual peak or trough that exaggerates it"),
    "simpson": ("aggregation reversal ignored", "a comparison of pooled totals is reported although the comparison goes the other way inside every subgroup"),
    "eco": ("group-level data applied to individuals", "a pattern seen across places or groups is stated as true of the individual people in them"),
    "mean": ("average used for the typical case", "a mean is used to support a claim about the typical (median) person or case, or the reverse"),
    "nominal": ("inflation ignored", "a comparison of money amounts over time ignores price changes when the claim is about real value or buying power"),
    "none": (NONE, "the claim, as worded, has none of the listed flaws"),
}


def err(*keys):
    out = [ERR[k] for k in keys if k != "none"]
    if "none" in keys:
        out.append(ERR["none"])
    return out


PCT = ("percent change", "relative change: (new value - old value) / old value x 100")
PP = ("percentage-point change", "the arithmetic difference between two percentages: new percentage - old percentage")
