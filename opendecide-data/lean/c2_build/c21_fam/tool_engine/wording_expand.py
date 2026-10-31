"""Reword-pool expansion for lane L-T (T54, T55, T56). Code only: no rows, no labels, no benchmark text.

A pool form is expanded from hand-written PARTS (lists of alternatives, joined with single spaces) or from
(prefix, core) pairs. Every expanded wording must pass the Haiku reword round trip against the seed template of its
form (tool_engine.wording.reword_ok: same {slot} set, same numbers, same negation count). Drop-only: a wording that
fails the round trip is dropped, never repaired. Duplicates are dropped. A form with fewer than MIN_PER_FORM wordings
after the round trip is an error, not a silent short pool.
"""
import itertools
import re

from . import util
from .wording import reword_ok, template_slots

MIN_PER_FORM = 50
_WS = re.compile(r"\s+")


def _clean(s):
    return _WS.sub(" ", s).strip()


def _join(combo):
    """Join parts: a part starting with punctuation attaches with no space; one starting with a space is kept as is."""
    out = ""
    for part in combo:
        if not part:
            continue
        if not out:
            out = part.lstrip()
        elif part[0] in ",;:.":
            out += part
        elif part[0] == " ":
            out += part
        else:
            out += " " + part
    return _clean(out)


def expand_parts(specs):
    """specs: list of 'spec', each spec a list of parts; each part a list of alternatives. Yields joined strings."""
    for spec in specs:
        for combo in itertools.product(*spec):
            yield _join(combo)


def expand_prefix_core(prefixes, cores):
    """Prefix/core pairs. A non-empty prefix lower-cases the first letter of the core (the core is a full sentence)."""
    for p in prefixes:
        for c in cores:
            if p:
                # lower-case only after a comma lead-in; after a full stop or colon the core keeps its capital
                keep = c.startswith("I ") or c.startswith("I'") or not p.rstrip().endswith(",")
                head = c if keep else c[0].lower() + c[1:]
                yield _clean(p + head)
            else:
                yield _clean(c)


def build_form(seed0, candidates, form_id, max_keep=None):
    """Round trip against seed0 (drop-only), de-duplicate, keep order. Raises if fewer than MIN_PER_FORM survive.
    max_keep (optional): when the survivors exceed it, keep an evenly spaced subset in product order (deterministic)."""
    seen, kept, dropped_rt, dropped_dup = set(), [], 0, 0
    for s in candidates:
        if s in seen:
            dropped_dup += 1
            continue
        if not reword_ok(seed0, s):
            dropped_rt += 1
            continue
        seen.add(s)
        kept.append(s)
    if len(kept) < MIN_PER_FORM:
        raise ValueError("form %s has %d wordings after the round trip (need %d)" % (form_id, len(kept), MIN_PER_FORM))
    n_surv = len(kept)
    if max_keep and n_surv > max_keep:
        idx = sorted({round(i * (n_surv - 1) / (max_keep - 1)) for i in range(max_keep)})
        kept = [kept[i] for i in idx]
    stats = {"candidates": n_surv + dropped_rt + dropped_dup, "survivors": n_surv, "kept": len(kept),
             "dropped_roundtrip": dropped_rt, "dropped_duplicate": dropped_dup,
             "slots": sorted(template_slots(seed0))}
    return kept, stats


def pool_sha(pools):
    """sha256 of the canonical pool JSON (re-export at every change)."""
    return util.sha256_text(util.canon_json({k: pools[k] for k in sorted(pools)}))
