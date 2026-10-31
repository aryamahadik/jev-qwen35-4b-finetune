"""T57 shared helpers: module construction, lowering, diffs, comments, names for rows."""
import difflib
import random

from LC_COMMON import ir as I
from LC_COMMON import irmut, modgen
from LC_COMMON import render as R
from LC_COMMON.lower import LowerError
from LC_COMMON.names_guard import default_guard
from LC_COMMON.render_sh import ShUnsupported

from . import config as C

FAMILY = C.FAMILY
COMMENT_PREFIX = {"python": "# ", "bash": "# ", "javascript": "// ", "typescript": "// ", "go": "// "}


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


def files_of(lo, lang):
    """The module's source files only (no go.mod / vendor)."""
    return {k: v for k, v in R.render_module(lo, lang).items() if k not in ("go.mod", "vendor/modules.txt")}


def diff_text(before, after, context=1):
    """Unified diff over the files that differ ('a/<path>' -> 'b/<path>'). Returns (text, changed_lines, hunks, n_files)."""
    out, changed, hunks, nf = [], 0, 0, 0
    for path in sorted(set(before) | set(after)):
        a, b = before.get(path, ""), after.get(path, "")
        if a == b:
            continue
        nf += 1
        d = list(difflib.unified_diff(a.splitlines(), b.splitlines(), "a/" + path, "b/" + path, n=context, lineterm=""))
        out += d
        changed += sum(1 for x in d if (x.startswith("+") and not x.startswith("+++")) or (x.startswith("-") and not x.startswith("---")))
        hunks += sum(1 for x in d if x.startswith("@@"))
    return "\n".join(out) + ("\n" if out else ""), changed, hunks, nf


def insert_comment(files_after, files_before, lang, text):
    """Add a one-line source comment above the first changed line of the patched tree. Returns (new_files, comment_line)."""
    new = dict(files_after)
    for path in sorted(new):
        a, b = files_before.get(path, "").splitlines(), new[path].splitlines()
        if a == b:
            continue
        k = 0
        while k < min(len(a), len(b)) and a[k] == b[k]:
            k += 1
        k = min(k, len(b))
        indent = ""
        if k < len(b):
            line = b[k]
            indent = line[:len(line) - len(line.lstrip())]
        c = indent + COMMENT_PREFIX[lang] + text
        b.insert(k, c)
        new[path] = "\n".join(b) + "\n"
        return new, c
    return new, None


def row_names(head, lang):
    runners = [C.RUNNER[lang]]
    if head in ("VERDICT", "BEST4", "LOCALISE", "TESTSEL"):
        runners.append("runner.domain_enumerator." + lang)
    carriers = sorted(set(C.CARRIERS[head]) | ({"VISIBLE_RESULT"} if False else set()))
    names = {"policy": [C.DEFS_CARD[head]], "tool": [], "language": [lang], "runner": sorted(set(runners)), "carrier": carriers}
    default_guard().assert_ok(FAMILY, names)
    return names
