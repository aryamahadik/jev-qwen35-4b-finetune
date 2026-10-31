"""Shared helpers for the three T42c heads: building a base module, lowering variants, naming the row's runners."""
import random

from LC_COMMON import ir as I
from LC_COMMON import irmut, modgen
from LC_COMMON import transforms as T
from LC_COMMON.lower import LowerError
from LC_COMMON.render_sh import ShUnsupported
from LC_COMMON.names_guard import default_guard

from . import config as C

FAMILY = C.FAMILY


class Skip(Exception):
    """A candidate could not satisfy its cell; the planner draws another seed (counted, never silent)."""


def mk_rng(*parts):
    return random.Random(":".join(str(p) for p in (FAMILY,) + parts))


def new_base(seed, lang, pred=None, tries=8, **kw):
    """-> (unlowered IR module, ids). The module is built for ONE target language. `pred(mod)` may demand a property
    (for example 'raises something'); sub-seeds seed.0, seed.1, ... are tried deterministically."""
    last = None
    for k in range(tries if pred else 1):
        sub = seed if not pred else "%s.%d" % (seed, k)
        mod, ids = modgen.gen_module(sub, lang, FAMILY, **kw)
        last = (mod, ids)
        if pred is None or pred(mod):
            return mod, ids
    raise Skip("no module satisfies the requirement")


def lower(mod, lang, ids):
    try:
        return modgen.prepare(mod, lang, ids)
    except (LowerError, ShUnsupported) as e:
        raise Skip("lowering: %s" % e)


def render_ok(lo, lang):
    """Render once to be sure the language-specific renderer accepts the module (raises Skip otherwise)."""
    from LC_COMMON import render as R
    try:
        R.render_module(lo, lang)
    except (ShUnsupported, ValueError, KeyError) as e:
        raise Skip("render: %s" % e)


def variant(base, ids, lang, fn_name, how, rng, tag):
    """Apply a transform id / mutation site (dict) to function `fn_name` of the UNLOWERED base; lower; return (lo, info)."""
    if isinstance(how, str) and how.startswith("EQ-YES"):
        new = T.apply(base, fn_name, how, rng, ids, tag)
        info = {"kind": "transform", "id": how}
    else:
        new = irmut.apply_site(base, how)
        info = {"kind": "mutation", "op": how["op"], "site": {"fn": how["fn"], "path": how["path"], "variant": how["variant"]}}
    if new is None:
        raise Skip("variant did not apply")
    lo = lower(new, lang, ids)
    render_ok(lo, lang)
    return new, lo, info


def row_names(head, lang):
    """policy/tool/language/runner/carrier names a row of this head declares (checked against the frozen list)."""
    runners = [C.RUNNER_OF_LANG[lang], "runner.twin_counters." + lang]
    if head == "EQV2":
        runners.append("runner.domain_enumerator." + lang)
    names = {"policy": [], "tool": [], "language": [lang], "runner": sorted(set(runners)), "carrier": sorted(C.CARRIERS[head])}
    default_guard().assert_ok(FAMILY, names)
    return names


def custom_error_flag(rng):
    return rng.random() < 0.15
