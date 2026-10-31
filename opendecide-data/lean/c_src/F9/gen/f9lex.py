"""F9 closed lexicons, fixed forms and pack-word lint (G0 v7: 1.2, 1.6 pack words / marker words, section 2, section 5,
XF17). Everything meaning-bearing that F9 writes into a card, a question or an option comes from this file; the
lexicon dump (write_lexicon) is the one XF17 lexicon file (sha256 recorded in the manifest).

Paths, logging and the label-free hash also live here so every module imports one place.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

F9 = Path(__file__).resolve().parents[1]
C_SRC = F9.parent
LEAN = C_SRC.parent
OUT = F9 / "out"
TMP = F9 / "tmp"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
PY = LEAN.parent / ".venv" / "bin" / "python"
SPEC_ID = "F9.G0.v7"
G0_SHA256 = "70e75711ade3b53d339ad566ae77d919f0b48e2309daf6020025bc4f09f9ed6c"
GEN_VERSION = "F9-gen r1.0 (py3, pandas 3.0.6, sqlite 3.49.1, PyYAML 6.0.3)"
SOURCE = "c_f9"
LICENCE = "CC0 1.0 (program-generated)"
SEED = 20261003

sys.path.insert(0, str(C_SRC / "common"))
sys.path.insert(0, str(C_SRC / "formats" / "formats-1"))
import negcount  # noqa: E402  (orchestrator-owned, referenced)


def now():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    with open(PROGRESS, "a") as f:
        f.write(f"{now()} [F9] {msg}\n")


def uh(*parts) -> float:
    """Uniform [0, 1) from ids only (label-free)."""
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ comparators (T10)
# phrase template -> op. {X} is the literal (with its unit on amounts, T28). "exceeds" is on the closed list but F9
# questions are written "<col> is <phrase>", so the verb form is never generated (the card then never states it).
CMP_T10 = {
    "at least {X}": ">=", "no fewer than {X}": ">=", "no less than {X}": ">=", "{X} or more": ">=",
    "at most {X}": "<=", "no more than {X}": "<=", "not more than {X}": "<=", "up to {X}": "<=",
    "{X} or fewer": "<=", "{X} or less": "<=",
    "more than {X}": ">", "greater than {X}": ">", "higher than {X}": ">", "over {X}": ">", "above {X}": ">",
    "less than {X}": "<", "fewer than {X}": "<", "lower than {X}": "<", "below {X}": "<", "under {X}": "<",
    "exactly {X}": "=", "not equal to {X}": "!=",
}
CMP_COUNT_OK = {"at least {X}", "no fewer than {X}", "{X} or more", "at most {X}", "no more than {X}",
                "{X} or fewer", "more than {X}", "fewer than {X}", "exactly {X}", "not more than {X}"}
CMP_AMOUNT_OK = {"at least {X}", "no less than {X}", "{X} or more", "at most {X}", "no more than {X}",
                 "not more than {X}", "up to {X}", "{X} or less", "more than {X}", "greater than {X}",
                 "higher than {X}", "over {X}", "above {X}", "less than {X}", "lower than {X}", "below {X}",
                 "under {X}", "exactly {X}"}
OP_FLIP_INCL = {">=": ">", ">": ">=", "<=": "<", "<": "<="}
# T35 group comparisons (yes/no only)
CMP_T35 = {"greater than": ">", "higher than": ">", "more than": ">", "less than": "<", "lower than": "<",
           "fewer than": "<", "at least as high as": ">=", "at least as many as": ">=", "the same as": "="}
# T33 level phrases (S6)
CMP_T33 = {"{L} or higher": ">=", "at least {L}": ">=", "above {L}": ">", "{L} or lower": "<=", "below {L}": "<"}
CMP_T11 = "between {X} and {Y}"


def closed_comparator_phrases():
    out = set()
    for t in list(CMP_T10) + list(CMP_T33):
        out.add(t.replace("{X}", "").replace("{L}", "").strip())
    out |= set(CMP_T35)
    out.add("between")
    out.add("exceeds")
    return sorted(out)


# ------------------------------------------------------------------------------------------------ time grammar
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
MON3 = [m[:3] for m in MONTHS]
TIME_FORMS = {
    "from_to": "from {D1} to {D2}", "before": "before {D}", "after": "after {D}", "on_or_before": "on or before {D}",
    "on_or_after": "on or after {D}", "on": "on {D}", "in_month": "in {M} {Y}",
    "rolling": "in the {N} days ending on {D}",                 # T16 phrase "the <N> days ending on <D>"
    "half_open": "from {T1} up to but not including {T2}",     # T17, datetime only
}
TIME_LEAD = ("before", "after", "from", "ending", "within", "per", "since", "until", "through")
CONNECTIVES = ("and", "or", "nor", "neither", "either", "unless", "only", "not", "but", "if", "except")
F9_CUES = ("not", "n't", "no", "none", "never", "nothing", "neither", "nor", "without", "fail", "fails", "lack",
           "lacks", "is it not the case that")
NEVER_TIME_WORDS = ("since", "until", "through", "as of", "starting", "recent", "today", "yesterday", "this week",
                    "next week")
ORDER_WORDS = ("the first rule that applies", "in order", "from top to bottom", "the first line that applies")

# ------------------------------------------------------------------------------------------------ markers (XF06)
MARKER_SET = {"not recorded", "unknown", "0", "none", "no", "null", "false", "true", "yes", "1"}
BANNED_MARKERS = {"-", "n/a", "tbd", "?", "--", "??"}
DASHES = set("-‐‑‒–—―−")


def is_marker_value(s: str) -> bool:
    t = str(s).strip().lower()
    return t in MARKER_SET or is_banned(t)


def is_banned(s: str) -> bool:
    t = str(s).strip().lower()
    return t in BANNED_MARKERS or (t != "" and set(t) <= DASHES)


# ------------------------------------------------------------------------------------------------ option wordings
CBD = "cannot be determined"
NONE_OPT = "none of these"


def no_record_opt(rec_sg: str) -> str:
    return f"no such {rec_sg}"


def tie_opt(rec_pl: str) -> str:
    return f"two or more {rec_pl} tie"


def set_opt(ids) -> str:
    ids = sorted(ids, key=id_key)
    if len(ids) == 1:
        return f"{ids[0]} only"
    return " and ".join(ids) + " only"


def id_key(s: str):
    m = re.match(r"^(.*?)(\d+)$", s)
    return (m.group(1), int(m.group(2))) if m else (s, -1)


# ------------------------------------------------------------------------------------------------ pack-word lint
_NUM_TOKEN = re.compile(r"^[+-]?\d[\d.,:/]*$")


def words(s: str):
    return [w for w in re.split(r"[\s_\-]+", s.lower()) if w]


def _contains_seq(ws, phrase):
    p = phrase.split()
    n = len(p)
    return any(ws[i:i + n] == p for i in range(len(ws) - n + 1))


_LINT_PHRASES = None


def _lint_phrases():
    global _LINT_PHRASES
    if _LINT_PHRASES is None:
        ph = set(closed_comparator_phrases())
        ph |= {"equal", "exactly", "higher", "lower", "greater", "less", "least", "most", "more", "fewer", "exceed",
               "exceeds", "same", "between"}
        ph |= set(CONNECTIVES) | set(TIME_LEAD)
        ph |= {"none", "never", "nothing", "without", "fail", "fails", "lack", "lacks", "no", "n't", "nor"}
        ph |= {"case", "count", "counts", "instead", "means", "every", "any", "all", "total", "average", "number",
               "listed", "such", "tie", "tied", "determined", "these", "whose", "of", "is", "the", "in", "on",
               "at", "to", "a", "an", "than", "one", "up", "including", "included", "days", "lines", "line",
               "logged", "highest", "lowest", "earliest", "latest", "first", "last", "most", "fewest", "true",
               "false", "yes", "null", "unknown", "recorded", "different", "values", "value", "contains", "with"}
        _LINT_PHRASES = ph
    return _LINT_PHRASES


def lint_word(s: str, *, maxlen: int = 32) -> str | None:
    """None if the pack word passes the 1.6 pack-word rules (and F9's grammar words), else a reason code."""
    if not isinstance(s, str) or not s.strip() or s != s.strip():
        return "empty"
    if len(s) > maxlen:
        return "long"
    if not re.fullmatch(r"[A-Za-z][A-Za-z ]*[A-Za-z]|[A-Za-z]", s):
        return "charset"
    if "  " in s:
        return "space"
    if is_marker_value(s):
        return "marker"
    ws = words(s)
    for w in ws:
        if _NUM_TOKEN.match(w):
            return "number"
        if w in MON3 or w.capitalize() in MONTHS:
            return "month"
    for ph in _lint_phrases():
        if _contains_seq(ws, ph):
            return "grammar"
    nc = negcount.count(s)
    if nc.k_all or nc.k_syn:
        return "negcount"
    return None


def snake(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def lint_colname(name: str) -> str | None:
    if not re.fullmatch(r"[a-z][a-z_]*[a-z]", name):
        return "charset"
    return lint_word(name.replace("_", " "))


# ------------------------------------------------------------------------------------------------ lexicon dump (XF17)
def lexicon() -> dict:
    return {
        "family": "F9", "spec_id": SPEC_ID, "what": "F9 closed lexicons and fixed forms (G0 v7 section 5, XF17)",
        "comparators_T10": sorted(CMP_T10), "comparator_T11": CMP_T11, "comparators_T33": sorted(CMP_T33),
        "comparators_T35": sorted(CMP_T35), "time_forms": TIME_FORMS, "cue_list": list(F9_CUES),
        "option_wordings": [CBD, NONE_OPT, "no such <record>", "two or more <records> tie", "<id a> and <id b> only"],
        "scope_phrase": "Among the listed <records>, ",
        "negation_forms": ["Is it not the case that <claim>?", "Is there no <record> whose <P>?",
                           "Does <R> have no <item> whose <B>?", "Does request <R> have no <L> line?",
                           "Is the <col> of <id> not <v>?", "Is the <col> of <id> neither <a> nor <b>?",
                           "Does <id> not count as <term>?"],
        "dneg_forms": ["Is it not the case that there is no <record> whose <P>?",
                       "Is it not the case that <R> has no <item> whose <B>?",
                       "Is it not the case that request <R> has no <L> line?",
                       "Is it not the case that the <col> of <id> is not <v>?",
                       "Is it not the case that <id> does not count as <term>?"],
        "presence_form": "Is there a <record> with <id col> <id>?",
        "inverted_form": "Which of these <records> counts as <term>?",
        "line_phrases": ["<L> lines", "lines at <L> or higher", "<L> lines from <C>", "lines from <C>",
                         "an <L> line", "a line from <C>", "no <L> line"],
        "markers": sorted(MARKER_SET), "banned_markers": sorted(BANNED_MARKERS),
    }


def write_lexicon(path) -> str:
    with open(path, "w") as f:
        json.dump(lexicon(), f, indent=1, sort_keys=True)
        f.write("\n")
    return sha256_file(path)
