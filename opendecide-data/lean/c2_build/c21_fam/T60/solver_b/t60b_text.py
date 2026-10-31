"""T60 solver B: shared text helpers (stdlib only). Everything here works on the RENDERED row: the context string, the question line and the
options. No spec, scene, case or gold is ever touched (G1). Written from G0_LITE.md and ROW_SCHEMA.md only."""
import re

HEADS = ("h1", "h2", "h3")
HEAD_LABELS = {"h1": ("DELEGATE", "DO_HERE"), "h2": ("KEEP", "DROP"), "h3": ("PLAN", "ACT")}


class ParseGap(Exception):
    """The rendered text does not show a construct this parser knows. -> solver B abstains (never guesses)."""

    def __init__(self, why):
        Exception.__init__(self, why)
        self.why = why


class Result(object):
    """What the pipeline reads: .label .letter .abstain .reason (plus .parsed for tests and the harness)."""
    __slots__ = ("label", "letter", "abstain", "reason", "parsed")

    def __init__(self, label=None, letter=None, abstain=False, reason=None, parsed=None):
        self.label = label
        self.letter = letter
        self.abstain = abstain
        self.reason = reason
        self.parsed = parsed

    def __repr__(self):
        return "Result(label=%r, letter=%r, abstain=%r, reason=%r)" % (self.label, self.letter, self.abstain, self.reason)


class Rx(object):
    """A named regular expression (no precompilation call: `re` caches the pattern)."""
    __slots__ = ("pattern", "flags")

    def __init__(self, pattern, flags=0):
        self.pattern = pattern
        self.flags = flags

    def match(self, s):
        return re.match(self.pattern, s, self.flags)

    def search(self, s):
        return re.search(self.pattern, s, self.flags)

    def fullmatch(self, s):
        return re.fullmatch(self.pattern, s, self.flags)

    def sub(self, repl, s):
        return re.sub(self.pattern, repl, s, flags=self.flags)


def lines_of(text):
    return [ln.rstrip() for ln in text.split("\n")]


NOTES_HEADER = "Background notes:"


def strip_notes(ls):
    """Drop the optional `Background notes:` block (all heads; ROW_SCHEMA additions of 18 Oct): the header line and the INDENTED lines that follow it
    (blank lines inside the block are skipped when more indented lines follow). The prose carries no fact, number or instruction, so it must not reach
    any parser (a number or a 'fails' / 'count' word inside it must not be read as a card clause). Only a header that stands alone on its line counts."""
    out, i, n = [], 0, len(ls)
    while i < n:
        if ls[i].strip() == NOTES_HEADER and not ls[i].startswith((" ", "\t")):
            i += 1
            while i < n:
                if ls[i].startswith((" ", "\t")) and ls[i].strip():
                    i += 1
                    continue
                j = i
                while j < n and not ls[j].strip():
                    j += 1
                if j > i and j < n and ls[j].startswith((" ", "\t")):          # blank line(s) inside the block, more indented prose follows
                    i = j
                    continue
                break
            continue
        out.append(ls[i])
        i += 1
    return out


# ----------------------------------------------------------------------------------------------------------------------
# head detection (from the question line; the structure of the context is the cross-check)
# ----------------------------------------------------------------------------------------------------------------------
def head_from_question(question):
    q = question.lower()
    hits = []
    if re.search(r"subtask|separate worker", q):
        hits.append("h1")
    if re.search(r"summar", q):
        hits.append("h2")
    if re.search(r"\bplan\b", q):
        hits.append("h3")
    return hits[0] if len(hits) == 1 else None


def head_from_context(context):
    has = lambda s: re.search(s, context, re.M) is not None          # noqa: E731
    hits = []
    if has(r"^Main thread facts:"):
        hits.append("h1")
    if has(r"^Remaining plan:"):
        hits.append("h2")
    if has(r"^Order given in the request:") or has(r"^Steps:"):
        hits.append("h3")
    return hits[0] if len(hits) == 1 else None


def detect_head(view):
    r = view.get("rendered") or {}
    q, ctx = r.get("question", ""), r.get("context", "")
    hq, hc = head_from_question(q), head_from_context(ctx)
    if hq is None and hc is None:
        raise ParseGap("head_unknown")
    if hq is not None and hc is not None and hq != hc:
        raise ParseGap("head_conflict")
    h = hq or hc
    sb = view.get("sub_block")
    if sb in HEADS and sb != h:
        raise ParseGap("head_vs_sub_block")
    return h


# ----------------------------------------------------------------------------------------------------------------------
# option text -> label (the gold letter is derived from the TEXT of the options, never from a label field)
# ----------------------------------------------------------------------------------------------------------------------
def classify_option(head, text):
    t = text.strip().lower()
    if head == "h1":
        if re.search(r"\bworker\b|\bdelegate\b", t) and not re.search(r"\b(do|carry out|handle)\b.*\b(here|main thread|this thread|itself)\b", t):
            return "DELEGATE"
        if re.search(r"\b(here|main thread|this thread|itself)\b", t):
            return "DO_HERE"
        return None
    if head == "h2":
        if re.search(r"\b(drop|leave|omit|exclude|discard|skip)\b", t):
            return "DROP"
        if re.search(r"\b(keep|carry|retain|include|put|stay)\b", t):
            return "KEEP"
        return None
    if head == "h3":
        if re.search(r"\b(without|no) (a )?plan\b", t):
            return "ACT"
        if re.search(r"\bplan\b", t):
            return "PLAN"
        if re.search(r"\bact\b", t):
            return "ACT"
        return None
    return None


def letters_from_options(head, options):
    """options: [{letter, text}] -> {label: letter}; ParseGap unless both labels of the head are present exactly once."""
    out = {}
    for o in options:
        lab = classify_option(head, o.get("text", ""))
        if lab is None:
            raise ParseGap("option_text_unclassified")
        if lab in out:
            raise ParseGap("option_label_duplicate")
        out[lab] = o.get("letter")
    if set(out) != set(HEAD_LABELS[head]):
        raise ParseGap("option_labels_incomplete")
    return out


_OPT_LINE = Rx(r"^\s*([A-Z])\)\s*(.*\S)\s*$")


def options_from_rendered(options_text):
    """The lettered option lines of the rendered text -> [{letter, text}]."""
    out = []
    for ln in lines_of(options_text):
        m = _OPT_LINE.match(ln)
        if m:
            out.append({"letter": m.group(1), "text": m.group(2)})
    return out


# ----------------------------------------------------------------------------------------------------------------------
# small shared parsers
# ----------------------------------------------------------------------------------------------------------------------
def clause(text, marker, nxt):
    """The text between 'marker:' and the next ordinal marker (or the end)."""
    i = text.find(marker + ":")
    if i < 0:
        raise ParseGap("card_clause_missing:" + marker)
    j = text.find(nxt + ":", i) if nxt else -1
    return text[i + len(marker) + 1:(j if j >= 0 else len(text))]


def one_number(pattern, text, what):
    m = re.findall(pattern, text)
    if len(m) != 1:
        raise ParseGap("card_number_missing:" + what)
    return int(m[0])


def split_paths(s):
    s = s.strip()
    if not s or s.lower() in ("nothing", "none"):
        return []
    return [p.strip() for p in s.split(",") if p.strip()]


def norm_path(p):
    """A path in its plain form: // collapsed, '.' dropped, '..' resolved, no trailing slash."""
    parts = []
    for seg in p.strip().split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            if parts:
                parts.pop()
            continue
        parts.append(seg)
    return ("/" if p.strip().startswith("/") else "") + "/".join(parts)
