"""c2_kit/skin.py: slot-locked skins, the renderer with grammar agreement, and the template-guided parser.

A skin is Haiku-written (or, kind "program", Claude-written) text whose every fact is a typed placeholder. Haiku never
sees the question, the options or the gold while writing it (C2_DATA_SPEC 3.0). The program fills every value.

Placeholder grammar (one line, no nesting; anything that starts like a placeholder but does not parse is a G-SL error):
  {NAME}            the slot's text in the row's chosen form (the program picks forms, label-blind)
  {NAME:form}       the slot in a pinned form (slots.FORMS), e.g. {DUE:iso}, {N:adj}
  {a|NAME}          indefinite article that agrees with the rendered value + the value ("an 8-day", "a user")
  {A|NAME}          the same, capitalised article (sentence start)
  {cap|NAME}        the value with its first letter upper-cased
  {poss|NAME}       the value + "'s"
  {NAME|sg|pl}      agreement word only: sg when the count slot NAME is 1, else pl ("{N|record is|records are}")
Slot names are upper-case ([A-Z][A-Z0-9_]*), so JSON or YAML braces ({"k": ...}) never read as placeholders. A clause
slot (lexicon) holds its own template; the renderer fills it with the same slots (one level only).

Escaping by register: "text" inserts values as they are; "json" JSON-escapes values inside string literals and writes
bare values as JSON (integers for count plain / cents int_cents, quoted strings otherwise), then json.loads must
accept the result; "yaml" double-quotes any value YAML would read as something else, then yaml.safe_load (when PyYAML
is installed) must accept it. Clause slots are text-register only.

Every fill records spans (field, start, end, slot, role) for each placeholder expansion. G-TW masks the spans of the
changed slot (and of the derived slots that depend on it) and requires the rest of the row to be identical.

Mode F skins (free-form, author_mode "F"): the text is Haiku's, written from a facts-only brief whose rendered values
are kept in `brief`; filling swaps each brief value for the slot's current rendering (verbatim spans; a value that
occurs inside another value, or two slots with the same brief text, refuse).

Parsing (G3, Mode T): match_template() turns a template into a regex whose slot groups are slots.regex() patterns
(written from the slot spec, not from fill()), full-matches the rendered text and parses each value with
slots.parse(); repeated slots must agree, articles and agreement words are re-checked. parse_structured() does the
same for JSON / YAML skins by walking the parsed container.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from . import slots as S

PH_RE = re.compile(r"\{(?:(?P<mod>a|A|cap|poss)\|)?(?P<name>[A-Z][A-Z0-9_]*)(?::(?P<form>[a-z][a-z0-9_]*))?"
                   r"(?:\|(?P<sg>[^{}|\n\"]*)\|(?P<pl>[^{}|\n\"]*))?\}")
SUSPECT_RE = re.compile(r"\{\s*(?:[a-zA-Z]+\s*\|\s*)?[A-Z]")
ESCAPES = ("text", "json", "yaml")
AUTHOR_MODES = ("T", "F")
SKIN_KINDS = ("skin", "wording", "program", "attack")

try:  # optional: YAML register validation
    import yaml as _yaml
except ImportError:  # pragma: no cover
    _yaml = None


class RenderError(ValueError):
    """A skin cannot be filled as declared."""


class TemplateMismatch(ValueError):
    """Rendered text does not match its template (G3 parse failure)."""


@dataclass(frozen=True)
class Placeholder:
    start: int
    end: int
    name: str
    mod: str | None
    form: str | None
    sg: str | None
    pl: str | None

    @property
    def agree(self) -> bool:
        return self.sg is not None


@dataclass(frozen=True)
class Span:
    field: str
    start: int
    end: int
    slot: str
    role: str            # value | agree | clause


@dataclass
class Filled:
    text: str
    spans: list = field(default_factory=list)


def placeholders(text: str) -> list:
    out = []
    for m in PH_RE.finditer(text):
        if m.group("sg") is not None and m.group("mod"):
            out.append(Placeholder(m.start(), m.end(), m.group("name"), "!bad", None, None, None))
            continue
        out.append(Placeholder(m.start(), m.end(), m.group("name"), m.group("mod"), m.group("form"), m.group("sg"),
                               m.group("pl")))
    return out


def malformed(text: str) -> list:
    """Snippets that start like a placeholder but are not one (or combine a modifier with agreement)."""
    good = [(p.start, p.end) for p in placeholders(text) if p.mod != "!bad"]
    bad = [text[p.start:p.end] for p in placeholders(text) if p.mod == "!bad"]
    for m in SUSPECT_RE.finditer(text):
        if not any(a <= m.start() < b for a, b in good):
            bad.append(text[m.start():m.start() + 24])
    return bad


# ------------------------------------------------------------------------------------------------ articles

_AN_WORDS = ("hour", "honest", "honor", "honour", "heir")
_YU_PREFIXES = ("unit", "union", "unique", "univers", "uniform", "unif", "unison", "unanim", "usa", "use", "usu",
                "usur", "uten", "util", "uto", "ura", "uri", "euro", "eu", "ewe", "one", "once", "ubiq", "uku")
_LETTER_AN = set("AEFHILMNORSX")


def article(text: str) -> str:
    """'a' or 'an' for the rendered value `text` (how it is read aloud)."""
    t = text.lstrip("\"'`([")
    if not t:
        raise RenderError("article before an empty value")
    m = re.match(r"\d[\d,]*", t)
    if m:
        digits = m.group().replace(",", "")
        if digits.startswith("8"):
            return "an"
        lead = len(digits) % 3 or 3
        return "an" if lead == 2 and digits[:2] in ("11", "18") else "a"
    w = re.match(r"[A-Za-z]+", t)
    if not w:
        return "a"                      # $12, -5, ...: read as "dollar", "minus"
    w = w.group()
    if w.isupper() and (len(w) >= 2 or len(t) == 1 or not t[1:2].isalpha()):
        return "an" if w[0] in _LETTER_AN else "a"     # letters read one by one: an SLA, a URL, an F
    lw = w.lower()
    if lw.startswith(_AN_WORDS):
        return "an"
    if lw[0] in "aeiou":
        return "a" if lw.startswith(_YU_PREFIXES) else "an"
    return "a"


# ------------------------------------------------------------------------------------------------ skins

@dataclass(frozen=True)
class Skin:
    skin_id: str
    family: str
    text: str
    slots: tuple                       # ((name, kind), ...) declared slots
    kind: str = "skin"                 # skin | wording | program | attack
    register: str = "memo"
    escape: str = "text"
    counts: tuple = ()                 # ((name, min, max), ...); default (1, 1) for every declared slot
    author_mode: str = "T"
    qform: str | None = None           # wordings: the question form the wording asks
    brief: tuple = ()                  # Mode F: ((name, rendered value in the brief), ...)
    haiku_task_id: str | None = None
    haiku_prompt_sha: str | None = None
    lexicon_ids: tuple = ()
    held_out: bool = False

    def __post_init__(self):
        if self.kind not in SKIN_KINDS or self.escape not in ESCAPES or self.author_mode not in AUTHOR_MODES:
            raise RenderError(f"skin {self.skin_id}: kind/escape/author_mode")
        if self.author_mode == "F" and placeholders(self.text):
            raise RenderError(f"skin {self.skin_id}: a Mode F text holds no placeholders (values are verbatim)")

    @property
    def decl(self) -> dict:
        return dict(self.slots)

    def count_range(self, name) -> tuple:
        for n, lo, hi in self.counts:
            if n == name:
                return lo, hi
        return 1, 1

    def fill(self, slots: dict, forms: dict | None = None, *, field: str = "state") -> Filled:
        decl = self.decl
        for name, kind in decl.items():
            if name not in slots:
                raise RenderError(f"skin {self.skin_id}: slot {name} has no value")
            if slots[name].kind != kind:
                raise RenderError(f"skin {self.skin_id}: slot {name} is {slots[name].kind}, declared {kind}")
        if self.author_mode == "F":
            return fill_freeform(self.text, dict(self.brief), {k: slots[k] for k in decl}, forms, field=field)
        used = {}
        for p in placeholders(self.text):
            if p.name not in decl:
                raise RenderError(f"skin {self.skin_id}: undeclared slot {p.name}")
            if not p.agree:
                used[p.name] = used.get(p.name, 0) + 1
        for name in decl:
            lo, hi = self.count_range(name)
            if not lo <= used.get(name, 0) <= hi:
                raise RenderError(f"skin {self.skin_id}: slot {name} appears {used.get(name, 0)}x, required {lo}-{hi}")
        return fill(self.text, {k: slots[k] for k in decl} | _clause_inner(decl, slots), forms, escape=self.escape,
                    field=field)


def make_skin(skin_id, family, text, slots: dict, **kw) -> Skin:
    counts = kw.pop("counts", {}) or {}
    brief = kw.pop("brief", {}) or {}
    return Skin(skin_id=skin_id, family=family, text=text, slots=tuple(sorted(slots.items())),
                counts=tuple(sorted((k, v[0], v[1]) for k, v in counts.items())),
                brief=tuple(sorted(brief.items())), lexicon_ids=tuple(kw.pop("lexicon_ids", ())), **kw)


def _clause_inner(decl, slots) -> dict:
    """Slots that a declared clause's template refers to (they are filled inside the clause)."""
    out = {}
    for name in decl:
        s = slots[name]
        if s.kind == "clause":
            for p in placeholders(s.value[2]):
                if p.name not in slots:
                    raise RenderError(f"clause {name} refers to slot {p.name}, which the spec lacks")
                out[p.name] = slots[p.name]
    return out


# ------------------------------------------------------------------------------------------------ fill

def _json_quote_state(template: str, phs: list) -> list:
    """For each placeholder: is it inside a JSON string literal of the template?"""
    out, i, in_str, k = [], 0, False, 0
    bounds = [(p.start, p.end) for p in phs]
    while i <= len(template) and k < len(bounds):
        if i == bounds[k][0]:
            out.append(in_str)
            i = bounds[k][1]
            k += 1
            continue
        if i == len(template):
            break
        c = template[i]
        if in_str and c == "\\":
            i += 2
            continue
        if c == '"':
            in_str = not in_str
        i += 1
    return out


_YAML_PLAIN_BAD = re.compile(r"^(?:[-?:,\[\]{}#&*!|>'\"%@`]|$)|: | #|^(?:y|n|yes|no|on|off|true|false|null|~)$|"
                             r"^[-+]?(?:\d[\d_,.:]*|\.\d+)(?:[eE][-+]?\d+)?$|^\d{4}-\d{2}-\d{2}", re.I)


def _yaml_whole_scalar(template: str, p: Placeholder) -> bool:
    """The placeholder is a whole YAML value ("key: {X}" or "- {X}" alone on its line)."""
    a = template.rfind("\n", 0, p.start) + 1
    b = template.find("\n", p.end)
    before, after = template[a:p.start], template[p.end: len(template) if b < 0 else b]
    return bool(re.fullmatch(r"\s*(?:-\s+)*(?:[^\s:#'\"][^:#]*:\s+)?(?:-\s+)?", before)) and after.strip() == ""


def _expand(p: Placeholder, slot: S.Slot, forms: dict, slots: dict, depth: int):
    """(text, inner spans relative to the start of text) for one placeholder."""
    if p.agree:
        if slot.kind != "count":
            raise RenderError(f"agreement {{{p.name}|..|..}} needs a count slot, {p.name} is {slot.kind}")
        return (p.sg if slot.value == 1 else p.pl), []
    inner = []
    if slot.kind == "clause":
        if depth > 0:
            raise RenderError("a clause inside a clause")
        sub = fill(slot.value[2], slots, forms, depth=depth + 1, field="")
        text, inner = sub.text, [(sp.start, sp.end, sp.slot, sp.role) for sp in sub.spans]
    else:
        text = S.render(slot, p.form or (forms or {}).get(p.name))
    if p.mod == "cap":
        text = text[:1].upper() + text[1:]
    elif p.mod == "poss":
        text = text + "'s"
    elif p.mod in ("a", "A"):
        art = article(text)
        art = art.capitalize() if p.mod == "A" else art
        inner = [(a + len(art) + 1, b + len(art) + 1, s, r) for a, b, s, r in inner]
        text = f"{art} {text}"
    return text, inner


def fill(template: str, slots: dict, forms: dict | None = None, *, escape: str = "text", field: str = "state",
         depth: int = 0) -> Filled:
    """Fill every placeholder of `template` from `slots` (refuses undeclared or malformed placeholders)."""
    bad = malformed(template)
    if bad:
        raise RenderError(f"malformed placeholder(s): {bad[:3]}")
    phs = placeholders(template)
    if escape != "text" and any(slots.get(p.name) and slots[p.name].kind == "clause" for p in phs):
        raise RenderError("clause slots are text-register only")
    in_str = _json_quote_state(template, phs) if escape == "json" else [False] * len(phs)
    out, spans, pos, cur = [], [], 0, 0
    for p, ins in zip(phs, in_str):
        lit = template[pos:p.start]
        out.append(lit)
        cur += len(lit)
        if p.name not in slots:
            raise RenderError(f"no value for slot {p.name}")
        slot = slots[p.name]
        text, inner = _expand(p, slot, forms, slots, depth)
        role = "agree" if p.agree else ("clause" if slot.kind == "clause" else "value")
        if escape == "json":
            if ins:
                text = json.dumps(text, ensure_ascii=False)[1:-1]
            elif p.agree or p.mod:
                raise RenderError(f"{{{p.name}}}: agreement and modifiers only inside JSON strings")
            elif not (slot.kind in S.NUMERIC_KINDS and re.fullmatch(r"-?\d+", text)):
                text = json.dumps(text, ensure_ascii=False)
        elif escape == "yaml" and not p.agree and not (slot.kind in S.NUMERIC_KINDS and re.fullmatch(r"-?\d+", text)):
            if _yaml_whole_scalar(template, p):
                if _YAML_PLAIN_BAD.search(text) or text != text.strip():
                    text = json.dumps(text, ensure_ascii=False)
            elif ": " in text or " #" in text or text.endswith(":"):
                raise RenderError(f"{{{p.name}}} sits inside a YAML scalar and its value {text!r} would break it")
        spans.append(Span(field, cur, cur + len(text), p.name, role))
        for a, b, s, r in inner:
            spans.append(Span(field, cur + a, cur + b, s, r))
        out.append(text)
        cur += len(text)
        pos = p.end
    out.append(template[pos:])
    result = "".join(out)
    if SUSPECT_RE.search(result):
        raise RenderError("placeholder residue after fill")
    if escape == "json":
        try:
            json.loads(result)
        except ValueError as e:
            raise RenderError(f"JSON skin does not parse after fill: {e}") from None
    if escape == "yaml" and _yaml is not None:
        try:
            _yaml.safe_load(result)
        except _yaml.YAMLError as e:
            raise RenderError(f"YAML skin does not parse after fill: {str(e)[:120]}") from None
    return Filled(result, spans)


def fill_freeform(text: str, brief: dict, slots: dict, forms: dict | None = None, *, field: str = "state") -> Filled:
    """Mode F: replace each brief value by the slot's current rendering; spans are the replaced occurrences."""
    if set(brief) != set(slots):
        raise RenderError(f"Mode F brief names {sorted(brief)}, slots {sorted(slots)}")
    vals = list(brief.items())
    texts = [v for _, v in vals]
    if len(set(texts)) != len(texts):
        raise RenderError("two Mode F slots share one brief text (cannot tell their occurrences apart)")
    for a in texts:
        for b in texts:
            if a != b and a in b:
                raise RenderError(f"brief value {a!r} occurs inside {b!r}")
    hits = []
    for name, v in vals:
        for m in re.finditer(r"(?<![\w])" + re.escape(v) + r"(?![\w])", text):
            hits.append((m.start(), m.end(), name))
    hits.sort()
    out, spans, pos, cur = [], [], 0, 0
    for a, b, name in hits:
        lit = text[pos:a]
        out.append(lit)
        cur += len(lit)
        new = S.render(slots[name], (forms or {}).get(name))
        spans.append(Span(field, cur, cur + len(new), name, "value"))
        out.append(new)
        cur += len(new)
        pos = b
    out.append(text[pos:])
    return Filled("".join(out), spans)


def locate(text: str, values: dict) -> dict:
    """{slot: [(start, end), ...]} verbatim occurrences of rendered values in a text (Mode F checks)."""
    out = {}
    for name, v in values.items():
        out[name] = [(m.start(), m.end()) for m in re.finditer(r"(?<![\w])" + re.escape(v) + r"(?![\w])", text)]
    return out


# ------------------------------------------------------------------------------------------------ parsing (G3)

def _segments_regex(template: str, schema: dict, forms: dict | None, groups: list, flags_ci_lit=False) -> str:
    parts, pos = [], 0
    for p in placeholders(template):
        lit = template[pos:p.start]
        parts.append(re.escape(lit))
        pos = p.end
        gi = len(groups)
        if p.agree:
            parts.append(f"(?P<g{gi}>{re.escape(p.sg)}|{re.escape(p.pl)})")
            groups.append(("agree", p))
            continue
        kind, params = schema[p.name]
        if kind == "clause":
            pat = r"[^\n{}]+?"
        else:
            f = p.form or (forms or {}).get(p.name)
            pat = S.regex(kind, f, params) if f else S.any_regex(kind, params)
        if p.mod == "cap":
            pat = f"(?i:{pat})"
        g = f"(?P<g{gi}>{pat})"
        if p.mod in ("a", "A"):
            g = f"(?P<art{gi}>[Aa]n?) " + g
        if p.mod == "poss":
            g = g + "'s"
        parts.append(g)
        groups.append(("value", p))
    parts.append(re.escape(template[pos:]))
    return "".join(parts)


def _decode_groups(m, groups, schema, lexicon) -> dict:
    vals, agree_checks = {}, []
    for gi, (what, p) in enumerate(groups):
        txt = m.group(f"g{gi}")
        if what == "agree":
            agree_checks.append((p, txt))
            continue
        kind, params = schema[p.name]
        if kind == "clause":
            if lexicon is None:
                raise TemplateMismatch(f"clause {p.name} needs a lexicon to parse")
            sem, form_id, inner = lexicon.parse_exact(txt)
            v = {"sem": sem, "form": form_id, "values": inner}
        else:
            cand = [txt]
            if p.mod == "cap" and txt[:1].isupper():
                cand.append(txt[:1].lower() + txt[1:])
            v, err = None, None
            for c in cand:
                try:
                    v = S.canonical(S.Slot(kind, S.parse(kind, c, params, p.form)))
                    break
                except S.SlotError as e:
                    err = e
            if v is None:
                raise TemplateMismatch(f"slot {p.name}: {err}")
        if p.mod in ("a", "A"):
            got = m.group(f"art{gi}")
            if got.lower() != article(txt) or (p.mod == "A") != got[:1].isupper():
                raise TemplateMismatch(f"article {got!r} before {txt!r} does not agree")
        if p.name in vals and vals[p.name] != v:
            raise TemplateMismatch(f"slot {p.name} reads {vals[p.name]!r} and {v!r}")
        vals[p.name] = v
    for p, txt in agree_checks:
        if p.name not in vals:
            raise TemplateMismatch(f"agreement word for {p.name} without its value in the same text")
        want = p.sg if vals[p.name] == 1 else p.pl
        if txt != want:
            raise TemplateMismatch(f"agreement {txt!r} with {p.name}={vals[p.name]}")
    return vals


def match_template(template: str, text: str, schema: dict, forms: dict | None = None, lexicon=None) -> dict:
    """{slot: canonical value} read back from `text` (Mode T, text register). schema: {slot: (kind, params)}."""
    groups: list = []
    pat = _segments_regex(template, schema, forms, groups)
    m = re.fullmatch(pat, text, re.S)
    if not m:
        raise TemplateMismatch("text does not match its template")
    return _decode_groups(m, groups, schema, lexicon)


_SENT = "⁣S{}⁣"


def parse_structured(template: str, text: str, schema: dict, escape: str, forms: dict | None = None) -> dict:
    """{slot: canonical value} from a JSON / YAML skin: parse both, walk the template tree, read each leaf."""
    phs = [p for p in placeholders(template)]
    in_str = _json_quote_state(template, phs) if escape == "json" else [False] * len(phs)
    sent, pos, keyed = [], 0, {}
    for i, (p, ins) in enumerate(zip(phs, in_str)):
        sent.append(template[pos:p.start])
        tok = _SENT.format(i)
        keyed[tok] = p
        sent.append(tok if (ins or escape == "yaml") else json.dumps(tok))
        pos = p.end
    sent.append(template[pos:])
    if escape == "json":
        t_tree, r_tree = json.loads("".join(sent)), json.loads(text)
    elif _yaml is not None:
        t_tree, r_tree = _yaml.safe_load("".join(sent)), _yaml.safe_load(text)
    else:  # pragma: no cover
        raise TemplateMismatch("YAML parsing needs PyYAML")
    vals: dict = {}

    def leaf(t, r):
        if not isinstance(t, str) or "⁣" not in t:
            if t != r:
                raise TemplateMismatch(f"literal {t!r} != {r!r}")
            return
        sub = re.sub("⁣S(\\d+)⁣", lambda mm: "{" + _ph_src(keyed[mm.group(0)]) + "}", t)
        rs = r if isinstance(r, str) else (json.dumps(r) if not hasattr(r, "isoformat") else r.isoformat())
        got = match_template(sub, rs, schema, forms)
        for k, v in got.items():
            if k in vals and vals[k] != v:
                raise TemplateMismatch(f"slot {k} reads two values")
            vals[k] = v

    def walk(t, r):
        if isinstance(t, dict):
            if not isinstance(r, dict) or set(t) != set(r):
                raise TemplateMismatch("container keys differ")
            for k in t:
                walk(t[k], r[k])
        elif isinstance(t, list):
            if not isinstance(r, list) or len(t) != len(r):
                raise TemplateMismatch("list lengths differ")
            for a, b in zip(t, r):
                walk(a, b)
        else:
            leaf(t, r)

    walk(t_tree, r_tree)
    return vals


def _ph_src(p: Placeholder) -> str:
    s = (f"{p.mod}|" if p.mod else "") + p.name + (f":{p.form}" if p.form else "")
    return s + (f"|{p.sg}|{p.pl}" if p.agree else "")


def parse_skin(skin: Skin, text: str, schema: dict, forms: dict | None = None, lexicon=None) -> dict:
    """G3 read-back of one filled skin (text register via match_template, JSON / YAML via parse_structured)."""
    if skin.author_mode == "F":
        raise TemplateMismatch("Mode F text has no template: use G3-H (g3h.py)")
    if skin.escape == "text":
        return match_template(skin.text, text, schema, forms, lexicon)
    return parse_structured(skin.text, text, schema, skin.escape, forms)


def schema_of(slots: dict) -> dict:
    return {k: v.schema for k, v in slots.items()}


def fill_any(skin: Skin, slots: dict, forms: dict | None = None, field: str = "state") -> Any:
    return skin.fill(slots, forms, field=field)
