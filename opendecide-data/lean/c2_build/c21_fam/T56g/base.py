"""T56g shared helpers."""
import random

from LC_COMMON import modgen
from LC_COMMON import render as R
from LC_COMMON.lower import LowerError
from LC_COMMON.names_guard import default_guard
from LC_COMMON.render_sh import ShUnsupported

from . import config as C

FAMILY = C.FAMILY


class Skip(Exception):
    """A candidate task/row could not satisfy its cell; the planner draws another seed (counted, never silent)."""


def mk_rng(*parts):
    return random.Random(":".join(str(p) for p in (FAMILY,) + parts))


def new_base(seed, lang, pred=None, tries=10, **kw):
    for k in range(tries if pred else 1):
        sub = seed if not pred else "%s.%d" % (seed, k)
        mod, ids = modgen.gen_module(sub, lang, FAMILY, **kw)
        if pred is None or pred(mod):
            return mod, ids
    raise Skip("no module satisfies the requirement")


def lower(mod, lang, ids):
    try:
        lo = modgen.prepare(mod, lang, ids)
        R.render_module(lo, lang)
        return lo
    except (LowerError, ShUnsupported, ValueError, KeyError) as e:
        raise Skip("lowering/render: %s" % e)


def row_names(card_kind, lang, carriers):
    names = {"policy": [card_kind, C.DEFS_CARD], "tool": [], "language": [lang], "runner": [C.RUNNER[lang]],
             "carrier": sorted(set(carriers) - {"QUESTION_FORM"})}
    default_guard().assert_ok(FAMILY, names)
    return names
