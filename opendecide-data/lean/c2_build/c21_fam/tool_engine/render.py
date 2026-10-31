"""Rendering helpers shared by the L-T families. The C2 layout (cygnet + schema_branch_mark: header, definitions card,
option scaffolding) is sha-bound scaffolding owned by L-0; these functions render only the family CONTENT and return
structured parts so the layout wrapper can place them."""
import re

from . import util

OUTPUT_KEYS_T55 = {"status", "code", "retry_after", "field", "detail", "progress", "count", "items", "total", "key",
                   "committed"}
SECOND_PERSON = re.compile(r"\b(?:you|your|yours|yourself|you're|you'll|you've|we|our|ours|let's)\b", re.I)
IMPERATIVE_START = {"please", "retry", "try", "use", "call", "ignore", "run", "delete", "send", "ask", "stop", "wait",
                    "continue", "proceed", "switch", "fix", "change", "update", "remove", "do", "don't", "never",
                    "always", "make", "ensure", "verify", "check", "report", "tell", "restart", "repeat", "resend",
                    "execute", "install", "open", "read", "write", "set", "go", "click", "follow", "note", "remember"}
_KV_LINE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.\-]*(?:\[\d+\])?: ?.*$")
_SPAN_PATTERNS = [
    re.compile(r"\"[^\"]+\"|'[^']+'"),                       # quoted strings
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                    # ISO dates
    re.compile(r"\b[A-Za-z]{1,6}-\d{2,}\b"),                 # ids like abc-123
    re.compile(r"(?<![\w.-])\d+(?:\.\d+)?(?![\w-])"),        # standalone numbers
]


def letter_options(texts):
    """[(letter, text)] in the given order."""
    return [(util.LETTERS[i], t) for i, t in enumerate(texts)]


def option_block(pairs):
    return "\n".join("%s) %s" % (l, t) for l, t in pairs)


def kv_lines(pairs):
    """Data-field grammar: one 'key: value' per line."""
    return "\n".join("%s: %s" % (k, v) for k, v in pairs)


def lint_output(text, allowed_keys=None):
    """Output lint (gate P-13/P-14): every line must be a key: value data line; no second-person pronouns anywhere;
    no value that opens with an imperative verb (multi-word values only, so bare enum words such as 'open' pass);
    no key outside `allowed_keys` when given. Returns a list of violation strings (empty = clean)."""
    bad = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        if not _KV_LINE.match(ln):
            bad.append("not a data line: %r" % ln[:40])
            continue
        key, _, val = ln.partition(":")
        val = val.strip()
        base = re.sub(r"\[\d+\]$", "", key.strip())
        if allowed_keys is not None and base not in allowed_keys:
            bad.append("key off the closed list: %r" % base)
        if SECOND_PERSON.search(val):
            bad.append("second person in value: %r" % val[:40])
        words = re.findall(r"[A-Za-z']+", val)
        if len(words) >= 2 and words[0].lower() in IMPERATIVE_START:
            bad.append("imperative opening: %r" % val[:40])
        for clause in re.split(r"[.;!?]\s+", val):
            w = re.findall(r"[A-Za-z']+", clause)
            if len(w) >= 3 and w[0].lower() in IMPERATIVE_START:
                bad.append("imperative clause: %r" % clause[:40])
    return bad


def count_value_spans(text):
    """Number of value-bearing spans (quoted strings, ISO dates, ids, standalone numbers) in a text. Spans are
    counted once: each match is blanked before the next pattern runs."""
    n = 0
    t = text
    for pat in _SPAN_PATTERNS:
        found = pat.findall(t)
        n += len(found)
        t = pat.sub(" ", t)
    return n


def render_tool_line(tool, flags=True):
    """Compact one-line schema: name(params) [rw, idempotent]  -- description."""
    ps = []
    for p in tool["params"]:
        s = "%s: %s" % (p["name"], p["type"])
        if not p["required"]:
            s += "?"
        if p.get("default") is not None and p.get("default_visible", True):
            s += " = %s" % p["default"]
        ps.append(s)
    fl = ""
    if flags:
        fl = " [%s%s]" % (tool["rw"], ", idempotent" if (tool["rw"] == "write" and tool["idempotent"]) else "")
    return "%s(%s)%s -- %s" % (tool["name"], ", ".join(ps), fl, tool["desc"])


def render_call(tool_name, args):
    """name(k="v", ...) call skeleton; args is an ordered list of (param, value)."""
    return "%s(%s)" % (tool_name, ", ".join('%s="%s"' % (k, v) for k, v in args))


# ---- G10: decision_spans with a ROLE per span (voice metadata export; a code requirement, not a gate) -------------
ROLES_G10 = ("negation_polarity", "number", "entity_path_flag", "authority")
_NEG_WORDS = re.compile(r"\b(?:not|no|never|none|without|neither|nor|cannot|only)\b|n't", re.I)
_VALUE_SPANS = [("number", re.compile(r"\b\d{4}-\d{2}-\d{2}\b")), ("entity_path_flag", re.compile(r"\b[A-Za-z]{1,6}-\d{2,}\b")),
                ("entity_path_flag", re.compile(r"\"[^\"]+\"")), ("entity_path_flag", re.compile(r"\b[\w.-]+/[\w./-]+")),
                ("number", re.compile(r"(?<![\w.-])\d+(?:\.\d+)?(?![\w-])"))]


def decision_spans(text, authority_values=()):
    """Spans of `text` that carry the decision, each with a ROLE: authority (a value whose source is the user turn, a scope
    declaration, a boundary, ...), negation_polarity, number, entity_path_flag. Non-overlapping, sorted by start;
    AUTHORITY wins over every other role. Offsets index into `text`."""
    taken = []

    def free(a, b):
        return all(b <= x or a >= y for x, y, _r in taken)

    for v in sorted({str(v) for v in authority_values if str(v)}, key=len, reverse=True):
        for m in re.finditer(re.escape(v), text):
            if free(m.start(), m.end()):
                taken.append((m.start(), m.end(), "authority"))
    for role, pat in [("negation_polarity", _NEG_WORDS)] + _VALUE_SPANS:
        for m in pat.finditer(text):
            if free(m.start(), m.end()):
                taken.append((m.start(), m.end(), role))
    taken.sort()
    return [dict(start=a, end=b, text=text[a:b], role=r) for a, b, r in taken]
