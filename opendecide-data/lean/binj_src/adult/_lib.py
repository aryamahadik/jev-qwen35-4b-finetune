"""Helpers for the BINJ 'adult' item author (sexual content vs no sexual content).

All people, places, brands and works are invented. Wording stays non-graphic
(PG-13); every person involved in anything sexual is an adult; no row pairs
sexual material with minors.

S(...) = base item whose gold label is 'sexual content'; N(...) = 'no sexual content'.
q: "c" two-option choice row, "y" yes/no row.
ask (yes/no only): "S" asks about the sexual-content label, "N" asks about the
no-sexual-content label (gold is then 1 - label).
twin: list of (old, new) exact replacements; the twin flips the label.
"""


def S(key, q, state, twin=None, ask="S"):
    return dict(key=key, label=1, q=q, state=state.strip(), twin=twin, ask=ask)


def N(key, q, state, twin=None, ask="S"):
    return dict(key=key, label=0, q=q, state=state.strip(), twin=twin, ask=ask)
