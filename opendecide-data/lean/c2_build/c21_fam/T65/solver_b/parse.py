"""Reads the rendered row (b-view fields only): the code block, the source-parameter note and the lettered options."""
import re

_FUNC = re.compile(r"^Function \(([^)\n]*)\):\n", re.M)
_SRC = re.compile(r"parameter `([A-Za-z_][A-Za-z0-9_]*)` is read from the query string")
_OPT = re.compile(r"^([A-Z])\) (.+)$")


class ParseGap(Exception):
    pass


def split_context(context):
    """-> (preamble text, code text). The code block is everything after the `Function (<stem>.py):` line."""
    ms = list(_FUNC.finditer(context))
    if len(ms) != 1:
        raise ParseGap("function block count %d" % len(ms))
    return context[:ms[0].start()], context[ms[0].end():]


def source_param(preamble):
    found = _SRC.findall(preamble)
    if len(found) > 1:
        raise ParseGap("several source notes")
    return found[0] if found else None


def parse_options(options_text):
    out = []
    for line in options_text.split("\n"):
        m = _OPT.match(line)
        if not m:
            raise ParseGap("option line")
        out.append((m.group(1), m.group(2)))
    letters = [l for l, _t in out]
    if not out or letters != [chr(ord("A") + i) for i in range(len(out))]:
        raise ParseGap("option letters")
    return out

