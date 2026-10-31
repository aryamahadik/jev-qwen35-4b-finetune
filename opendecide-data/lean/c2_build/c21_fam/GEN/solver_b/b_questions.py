"""GEN solver B: reads the QUESTION sentence(s) at the end of a stem. Python 3 standard library only; imports nothing from solver A.

The question wordings are a closed pool of templates with {slot} fields (question_templates.json, a copy of the question half of the wording
pool, kept current by the A-side export script and a test). Each template is compiled to a regular expression anchored at the END of the stem
and at a sentence start; the slot values are recovered from the stem text, and everything in front of the match is returned as the
"remainder" for B's own fact readers. A stem that matches no template, or two templates with different slot values, is a ParseFail.

Slot value shapes are B's own (what a reader of the prompt sees): a name, a number, a date, a yes/no comparison phrase, a statement. Slots that carry
free phrases (a condition, a ranking phrase, a claim, an offset text) are matched lazily; the form solvers parse them further.
"""
import json
import os
import re

from bcommon import ParseFail

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(HERE, "question_templates.json")

NAME = r"[A-Za-z][A-Za-z0-9_]*"
_PH = r"(?:(?!\. )[^\n])+?"        # a free phrase: one line, never across a sentence break
SLOT_RX = {
    "final": NAME, "target": NAME, "do_var": NAME, "z": NAME, "t": NAME, "o": NAME, "x": NAME, "y": NAME,
    "t1": NAME, "t2": NAME, "iv1": NAME, "iv2": NAME, "b1": NAME, "b2": NAME,
    "cmp": r"at least|at most|more than|less than",
    "thr": r"\d+(?:\.\d+)? [A-Za-z]+",
    "agg": r"total|minimum|maximum|average|number", "col": r"[a-z][a-z0-9_]*",
    "offset": r"\d+ (?:business days?|days?|weeks?|months?)(?:, then \d+ (?:business days?|days?|weeks?|months?))*",
    "fmt": r"days, hours and minutes|hours and minutes|minutes",
    "zset": r"nothing|[a-z][a-z0-9_]*(?:, [a-z][a-z0-9_]*)*(?: and [a-z][a-z0-9_]*)?",
    "rank_phrase": r"(?:highest|lowest) " + _PH,
    "cond": r"[a-z][a-z0-9_]* " + _PH,
    "claim": r"\"?(?:the (?:total|minimum|average|maximum) of |exactly |the row with )" + _PH,
    "n": r"\d+", "do_val": r"\d+", "start": r"\d{4}-\d\d-\d\d",
    "query": r"[A-Z][A-Za-z0-9_]* is (?:not )?a [a-z][a-z0-9_'-]*(?: [a-z][a-z0-9_'-]*)*",
}
DEFAULT_RX = _PH          # a free-phrase slot never spans a line (question sentences are single lines)
BOUNDARY = r"(?:(?<=\n)|(?<=[.;:!?] )|\A)"
_FIELD = re.compile(r"\{([a-z_0-9]+)\}")

_CACHE = {}


def _compile(template):
    parts = _FIELD.split(template)
    body = []
    seen = set()
    for i, part in enumerate(parts):
        if i % 2 == 0:
            body.append(re.escape(part))
        else:
            if part in seen:
                body.append("(?P=%s)" % part)
            else:
                seen.add(part)
                body.append("(?P<%s>%s)" % (part, SLOT_RX.get(part, DEFAULT_RX)))
    return re.compile(BOUNDARY + "".join(body) + r"\Z")


def _load():
    if "sets" not in _CACHE:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)["sets"]
        compiled = {}
        for set_name, by_key in data.items():
            for key, lst in by_key.items():
                for t in lst:
                    compiled.setdefault(key, []).append((set_name, t, _compile(t)))
        _CACHE["sets"] = compiled
    return _CACHE["sets"]


def read_question(keys, stem):
    """keys: a question key or a list of keys, e.g. "q.AR-F1" or ["q.TM-T4", "q.TM-T4.overlap"].
    Returns (key, slots dict, remainder text). The remainder is the stem up to the start of the question sentence(s)."""
    if isinstance(keys, str):
        keys = [keys]
    compiled = _load()
    text = stem.rstrip()
    hits = []
    for key in keys:
        for set_name, t, rx in compiled.get(key, []):
            m = rx.search(text)
            if m:
                hits.append((m.start(), key, set_name, t, m))
    if not hits:
        raise ParseFail("question_not_found", text[-160:])
    first = min(h[0] for h in hits)
    best = [h for h in hits if h[0] == first]
    shapes = {(h[1], tuple(sorted(h[4].groupdict().items()))) for h in best}
    if len(shapes) != 1:
        raise ParseFail("ambiguous_question", "%d readings" % len(shapes))
    start, key, _set, _t, m = best[0]
    return key, dict(m.groupdict()), text[:start].rstrip()
