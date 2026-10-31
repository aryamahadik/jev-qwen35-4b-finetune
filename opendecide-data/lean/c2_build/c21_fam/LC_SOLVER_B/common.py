"""Shared plumbing of the L-C Solver B engine (stdlib only; never imports the generator, solver A, the IR or any renderer).

Solver B is CODE written from the G0-lites and the ROW_SCHEMA files only (Opus G1). It cannot run generated code on this CPU
side (no sandbox sign-off yet), so its method is DIFFERENT from solver A: it parses the RENDERED source text of each language
with its own tokenizer / parser and interprets it with its own evaluator (Python: `ast` for parsing only, own tree walker).
Nothing here calls exec / eval / compile / subprocess on generated text.
"""
import json


class Unsupported(Exception):
    """B's evaluator met a construct outside the subset it models. Counted per class, never turned into a label."""


class Timeout(Exception):
    """Step budget exhausted (an infinite loop or a runaway recursion in rendered code). Counted, never labelled."""


class Budget:
    def __init__(self, limit=4_000_000):
        self.limit = limit
        self.n = 0

    def tick(self, k=1):
        self.n += k
        if self.n > self.limit:
            raise Timeout("step budget")


class Thrown(Exception):
    """A language-level exception: `name` is the class name the language reports (Python type name, JS constructor name,
    Go panic-value type name)."""

    def __init__(self, name, value=None):
        Exception.__init__(self, name)
        self.name = name
        self.value = value


# ------------------------------------------------------------------------------------------------ plain values / observables
def plain(v):
    """Canonical comparable form of an interpreter value (lists, dicts, scalars only)."""
    if isinstance(v, bool) or v is None or isinstance(v, (int, str)):
        return v
    if isinstance(v, float):
        return int(v) if v == v and v not in (float("inf"), float("-inf")) and v == int(v) else v
    if isinstance(v, (list, tuple)):
        return [plain(x) for x in v]
    if isinstance(v, dict):
        return {str(k): plain(x) for k, x in v.items()}
    if isinstance(v, (set, frozenset)):
        return sorted(plain(x) for x in v)
    if hasattr(v, "to_plain"):
        return v.to_plain()
    raise Unsupported("unplainable value %s" % type(v).__name__)


def obs_key(o):
    """Stable string key of an observable ('ok', value) / ('exc', name) / ('seq', [...])."""
    return json.dumps(o, sort_keys=True, default=str)


# ------------------------------------------------------------------------------------------------ option text per language
def _py_repr(v):
    if isinstance(v, bool) or v is None:
        return repr(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(_py_repr(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join("%s: %s" % (_py_repr(k), _py_repr(x)) for k, x in v.items()) + "}"
    return repr(v)


def _js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"


def _js_repr(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return _js_str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_js_repr(x) for x in v) + "]"
    return repr(v)


def _go_str(s):
    return json.dumps(s, ensure_ascii=False)


def _go_repr(v, ret_type=None):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return _go_str(v)
    if isinstance(v, list):
        ty = ret_type or ("strs" if v and isinstance(v[0], str) else "ints")
        head = "[]string" if ty == "strs" else "[]int"
        return head + "{" + ", ".join(_go_repr(x) for x in v) + "}"
    return repr(v)


def _sh_repr(v):
    if v is True:
        return "1"
    if v is False:
        return "0"
    if isinstance(v, list):
        return " ".join(_sh_repr(x) for x in v)
    return str(v)


def option_text(lang, obs, ret_type=None):
    """The option text a model would see for an observable ('ok', value) / ('exc', name), per ROW_SCHEMA.md."""
    kind, val = obs
    if kind == "exc":
        if lang == "python":
            return "raises %s" % val
        if lang in ("javascript", "typescript"):
            return "throws %s" % val
        if lang == "go":
            return "panics with %s" % val
        if lang == "bash":
            return "exits with status %s" % val
    if lang == "python":
        return _py_repr(val)
    if lang in ("javascript", "typescript"):
        return _js_repr(val)
    if lang == "go":
        return _go_repr(val, ret_type)
    return _sh_repr(val)


def match_option(lang, obs, options, ret_type=None):
    """Return ('ok', letter) when exactly one option matches, else ('none'|'ambiguous', None)."""
    want = option_text(lang, obs, ret_type)
    hits = []
    for o in options:
        letter, _, text = o.partition(". ")
        if text == want:
            hits.append(letter)
    if len(hits) == 1:
        return "ok", hits[0]
    return ("none" if not hits else "ambiguous"), None
