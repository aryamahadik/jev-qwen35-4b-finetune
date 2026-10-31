"""G3 round-trip parser for F8 rows (G0 spec 5). Written from the spec and the data files only.

Inputs: the exact `card`, `state`, `instructions` and `options` strings and the row's format style id. It loads
gen/data/lexicon.json and gen/data/facts.json (the step-4 wording data) and the formats-1 style and skin data files
(container and skin grammar as data). It imports no renderer, sampler or solver module.
Output: a canonical structure (same shape the samplers build) that solver B re-solves and that hashes.render_view
turns into the render hash.
"""
from __future__ import annotations

import csv
import io
import json
import re
from fractions import Fraction as Fr
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
FMT1_DATA = HERE.parents[1] / "formats" / "formats-1" / "data"


class ParseError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ data
@lru_cache(maxsize=None)
def LEX():
    return json.load(open(HERE / "data" / "lexicon.json", encoding="utf-8"))


@lru_cache(maxsize=None)
def FACTS():
    return json.load(open(HERE / "data" / "facts.json", encoding="utf-8"))


@lru_cache(maxsize=None)
def STYLES():
    out = {}
    for line in open(FMT1_DATA / "styles.jsonl", encoding="utf-8"):
        s = json.loads(line)
        out[s["id"]] = s
    return out


@lru_cache(maxsize=None)
def SKINS():
    out = {}
    for line in open(FMT1_DATA / "skins.jsonl", encoding="utf-8"):
        s = json.loads(line)
        out[s["id"]] = s
    return out


def norm_key(s: str) -> str:
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(s))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


# ------------------------------------------------------------------------------------------------ numbers
CMP_WORDS = {}
for op, lst in json.load(open(HERE / "data" / "lexicon.json", encoding="utf-8"))["COMPARATORS"].items():
    for w in lst:
        CMP_WORDS[w["w"]] = op
CMP_WORDS["no fewer than"] = ">="
CMP_RE = "|".join(sorted((re.escape(w) for w in CMP_WORDS), key=len, reverse=True))


def parse_chance(t: str):
    """(value, rep, denom) for a chance text; None if the text is not a chance."""
    t = t.strip()
    m = re.fullmatch(r"(\d{1,3})%", t)
    if m:
        return Fr(int(m.group(1)), 100), "pct0", None
    m = re.fullmatch(r"(\d{1,3})\.(\d)%", t)
    if m:
        return Fr(int(m.group(1)) * 10 + int(m.group(2)), 1000), "pct1", None
    m = re.fullmatch(r"0\.(\d{1,3})", t)
    if m:
        d = m.group(1)
        return Fr(int(d), 10 ** len(d)), "dec", None
    if t in ("0", "1"):
        return Fr(int(t)), "dec", None
    m = re.fullmatch(r"(\d+)/(\d+)", t)
    if m:
        return Fr(int(m.group(1)), int(m.group(2))), "frac", int(m.group(2))
    m = re.fullmatch(r"(\d+) in (\d+)", t)
    if m:
        return Fr(int(m.group(1)), int(m.group(2))), "ain", int(m.group(2))
    m = re.fullmatch(r"(\d+) out of (\d+)", t)
    if m:
        return Fr(int(m.group(1)), int(m.group(2))), "aoutof", int(m.group(2))
    return None


def parse_money(t: str):
    m = re.fullmatch(r"(-?)(\d{1,3}(?:,\d{3})*|\d+) ([A-Za-z][A-Za-z ]*)", t.strip())
    if not m:
        return None
    v = int(m.group(2).replace(",", ""))
    if m.group(2).count(",") and not re.fullmatch(r"\d{1,3}(,\d{3})+", m.group(2)):
        return None
    return (Fr(-v) if m.group(1) else Fr(v)), m.group(3)


def parse_num(t: str):
    m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*|\d+)(?:\.(\d))?", t.strip())
    if not m:
        return None
    v = Fr(int(m.group(1).replace(",", "")))
    if m.group(2):
        v += Fr(int(m.group(2)), 10)
    return v


# ------------------------------------------------------------------------------------------------ text lines
_MARK = re.compile(r"^(?:[-*•+·]\s+|(?!0\.)\d+\.\d+\s+|\d+[.)]\s+|\(\d+\)\s+|Step \d+: |Rule \d+: |R\d+\. |§ \d+ )")


def clean_lines(text: str) -> list:
    out = []
    for raw in (text or "").split("\n"):
        ln = raw
        while ln.startswith(">"):
            ln = ln[1:].lstrip(" ")
        ln = ln.strip()
        if not ln:
            out.append("")
            continue
        if re.fullmatch(r"</?[a-z0-9_]+>", ln):
            continue
        ln2 = ln
        for _ in range(2):
            ln2 = _MARK.sub("", ln2)
        out.append(ln2)
    return out


def split_sentences(line: str) -> list:
    parts = re.split(r"(?<=[.?:])\s+(?=[A-Z0-9'\"]|[a-z][a-z ]*: )", line)
    return [p.strip() for p in parts if p.strip()]


# ------------------------------------------------------------------------------------------------ tables in text
def text_tables(lines: list) -> tuple:
    """Find md, aligned, pipe and grid tables. Returns (tables [(header, rows)], set of consumed line indexes)."""
    tables, used = [], set()
    n = len(lines)
    i = 0
    while i < n:
        ln = lines[i]
        # grid: +---+ borders
        if re.fullmatch(r"\+(?:-+\+)+", ln):
            rows, j = [], i
            while j < n and (re.fullmatch(r"\+(?:[-=]+\+)+", lines[j]) or lines[j].startswith("|")):
                if lines[j].startswith("|"):
                    rows.append([c.strip() for c in lines[j].strip("|").split("|")])
                used.add(j)
                j += 1
            if rows:
                tables.append((rows[0], rows[1:]))
            i = j
            continue
        # markdown pipes
        if ln.startswith("|") and ln.endswith("|"):
            rows, j = [], i
            while j < n and lines[j].startswith("|") and lines[j].endswith("|"):
                if not re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", lines[j]):
                    rows.append([c.strip() for c in lines[j][1:-1].split(" | ")])
                used.add(j)
                j += 1
            if rows:
                tables.append((rows[0], rows[1:]))
            i = j
            continue
        # aligned: header line, then a rule of '=' groups
        if i + 1 < n and re.fullmatch(r"=+(?:  =+)+", lines[i + 1]) and ln:
            rule = lines[i + 1]
            spans = [(m.start(), m.end()) for m in re.finditer(r"=+", rule)]
            raw_lines = [ln]
            j = i + 2
            body = []
            while j < n and lines[j] and not re.fullmatch(r"=+(?:  =+)*", lines[j]):
                body.append(lines[j])
                j += 1
            def cut(s):
                cells = []
                for k, (a, b) in enumerate(spans):
                    end = spans[k + 1][0] if k + 1 < len(spans) else len(s) + 1
                    cells.append(s[a:end].strip())
                return cells
            tables.append((cut(ln), [cut(b) for b in body]))
            used.update(range(i, j))
            i = j
            continue
        # pipe: 'a | b | c' with the same cell count on consecutive lines
        if " | " in ln and not ln.startswith("|"):
            k = ln.count(" | ")
            j = i
            rows = []
            while j < n and lines[j].count(" | ") == k and not lines[j].startswith("|") and lines[j]:
                rows.append([c.strip() for c in lines[j].split(" | ")])
                j += 1
            if len(rows) >= 2:
                tables.append((rows[0], rows[1:]))
                used.update(range(i, j))
                i = j
                continue
        i += 1
    return tables, used


# ------------------------------------------------------------------------------------------------ html
class _HP(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts, self.tables, self.kv = [], [], []
        self._buf = None
        self._tag = None
        self._row = None
        self._rowtags = None
        self._table = None
        self._dt = None

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "h5", "dt", "dd", "th", "td", "caption"):
            self._buf = []
            self._tag = tag
        if tag == "table":
            self._table = []
        if tag == "tr":
            self._row, self._rowtags = [], []

    def handle_endtag(self, tag):
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "h5") and self._buf is not None:
            self.texts.append("".join(self._buf).strip())
            self._buf = None
        elif tag in ("th", "td") and self._buf is not None:
            self._row.append("".join(self._buf).strip())
            self._rowtags.append(tag)
            self._buf = None
        elif tag == "tr" and self._row is not None:
            self._table.append((self._row, self._rowtags))
            self._row = None
        elif tag == "table" and self._table is not None:
            t = self._table
            if t and all(len(r) == 2 and tg[0] == "th" and tg[1] == "td" for r, tg in t):
                self.kv += [(r[0], r[1]) for r, _ in t]
            elif t:
                self.tables.append((t[0][0], [r for r, _ in t[1:]]))
            self._table = None
        elif tag == "dt" and self._buf is not None:
            self._dt = "".join(self._buf).strip()
            self._buf = None
        elif tag == "dd" and self._buf is not None:
            self.kv.append((self._dt, "".join(self._buf).strip()))
            self._buf = None
        elif tag == "caption" and self._buf is not None:
            self._buf = None

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)


def _oldest_first(text: str) -> str:
    """Newest-first quoted thread -> messages in oldest-first order (deeper quotes are older)."""
    groups = {}
    for raw in text.split("\n"):
        d = 0
        ln = raw
        while ln.startswith(">"):
            d += 1
            ln = ln[1:].lstrip(" ")
        groups.setdefault(d, []).append(ln)
    return "\n".join("\n".join(groups[d]) for d in sorted(groups, reverse=True))


def _unfence(text: str) -> str:
    t = text.strip("\n")
    m = re.match(r"^(?:.*\n\n)?```[a-z]*\n(.*)\n```$", t, re.S)
    if m:
        return m.group(1)
    lines = t.split("\n")
    if all((not ln) or ln.startswith("    ") for ln in lines):
        return "\n".join(ln[4:] for ln in lines)
    return t


def _split_title(text: str):
    """For fenced or indented bodies the renderer puts the title, a blank line, then the block."""
    t = text.strip("\n")
    m = re.match(r"^([^\n]+)\n\n(```[a-z]*\n.*\n```)$", t, re.S)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"^([^\n ][^\n]*)\n\n((?:    [^\n]*\n?|\n)+)$", t)
    if m:
        return m.group(1), m.group(2)
    return None, t


def atoms(state: str, style_id: str) -> dict:
    """Containers -> {'texts': [str], 'kv': [(key, value)], 'tables': [(header, rows)]}."""
    st = STYLES()[style_id]
    cont = st["container"]
    out = {"texts": [], "kv": [], "tables": []}
    title, body = _split_title(state)
    if title:
        out["texts"].append(title)
    if cont in ("json", "yaml"):
        raw = _unfence(body)
        if cont == "json":
            try:
                obj = json.loads(raw)
            except ValueError:
                obj = [json.loads(x) for x in raw.split("\n") if x.strip()]
        else:
            import yaml
            lines = raw.split("\n")
            if lines and lines[0].startswith("# "):
                out["texts"].append(lines[0][2:])
                raw = "\n".join(lines[1:])
            obj = yaml.safe_load(raw)
        _walk(obj, out)
        return out
    if cont == "csv":
        sk = SKINS()[st["skin"]]
        if not title and "\n\n" in body:
            head, rest = body.split("\n\n", 1)
            delim = sk["params"]["delim"] if not sk["params"].get("fixed") else "  "
            if "\n" not in head and delim not in head:
                out["texts"].append(head)
                body = rest
        raw = _unfence(body)
        if sk["params"].get("fixed"):
            rows = [re.split(r" {2,}", ln.strip()) for ln in raw.split("\n") if ln.strip()]
        else:
            rows = list(csv.reader(io.StringIO(raw), delimiter=sk["params"]["delim"]))
        rows = [r for r in rows if r]
        out["tables"].append((rows[0], rows[1:]))
        return out
    if cont == "html_snippet":
        hp = _HP()
        hp.feed(_unfence(body))
        out["texts"] += hp.texts
        out["kv"] += hp.kv
        out["tables"] += hp.tables
        return out
    # text containers
    if cont == "email_thread" and SKINS()[st["skin"]]["params"].get("order") == "newest_first":
        state = _oldest_first(state)
    lines = clean_lines(state)
    tables, used = text_tables(lines)
    out["tables"] += tables
    for i, ln in enumerate(lines):
        if i in used or not ln:
            continue
        out["texts"].append(ln)
    return out


def _walk(obj, out, key=None):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                _walk(v, out, k)
            else:
                out["kv"].append((k, "" if v is None else str(v)))
                if isinstance(v, str):
                    out["texts"].append(v)
    elif isinstance(obj, list):
        if obj and all(isinstance(x, dict) for x in obj):
            cols = list(obj[0].keys())
            out["tables"].append((cols, [[str(x.get(c, "")) for c in cols] for x in obj]))
        else:
            for x in obj:
                if isinstance(x, (dict, list)):
                    _walk(x, out, key)
                else:
                    out["texts"].append(str(x))


# ------------------------------------------------------------------------------------------------ templates
def _tmpl_re(t: str) -> re.Pattern:
    slot = {"ID": r"(?P<ID>[A-Z]{2,4}-\d{2,4})", "p": r"(?P<p>\d[\d./%]*(?: (?:in|out of) \d+)?)",
            "lo": r"(?P<lo>[-\d][\d,./%]*(?: [A-Za-z][A-Za-z ]*?)?)", "hi": r"(?P<hi>[-\d][\d,./%]*(?: [A-Za-z][A-Za-z ]*?)?)",
            "money": r"(?P<money>-?[\d,]+ [A-Za-z][A-Za-z ]*?|None)", "n": r"(?P<n>\d+)",
            "a": r"(?P<a>\d+)", "b": r"(?P<b>\d+)", "qdef": r"(?P<qdef>.+?)", "impact_def": r"(?P<impact_def>.+?)"}
    out = ""
    pos = 0
    seen = set()
    for m in re.finditer(r"\{(\w+)\}", t):
        out += re.escape(t[pos:m.start()])
        name = m.group(1)
        if name in seen:
            out += f"(?P={name})"
        else:
            quoted = t[m.start() - 1:m.start()] == "'" and t[m.end():m.end() + 1] == "'"
            out += slot.get(name, rf"(?P<{name}>[^']+?)" if quoted else rf"(?P<{name}>[^'.:;]+?)")
            seen.add(name)
        pos = m.end()
    out += re.escape(t[pos:])
    return re.compile("^" + out + "$")


@lru_cache(maxsize=None)
def SENT_RES():
    res = []
    for key, vs in FACTS()["SENT"].items():
        for i, v in enumerate(vs):
            res.append((key, _tmpl_re(v)))
    # more fixed text first, so a range sentence is never read as an exact one and 'own cost' is not an amount
    def literal_len(key):
        return -sum(len(v) - 2 * len(re.findall(r"\{\w+\}", v)) for v in FACTS()["SENT"][key][:1])
    res.sort(key=lambda kv: literal_len(kv[0]))
    return res


@lru_cache(maxsize=None)
def SEM_RES():
    res = []
    for key, vs in LEX()["SEM"].items():
        for i, v in enumerate(vs):
            res.append((key, i, _tmpl_re(v)))
    return res


def match_sem(line: str):
    for key, i, rx in SEM_RES():
        m = rx.match(line)
        if m:
            return key, i, m.groupdict()
    return None


# ------------------------------------------------------------------------------------------------ conditions
PART_RES = [
    ("bool", re.compile(r"^it shows '(?P<f>[^']+)'$")),
    ("cat", re.compile(r"^its (?P<name>.+?) is '(?P<v>[^']+)'$")),
    ("score", re.compile(rf"^its score is (?P<cmp>{CMP_RE}) (?P<v>\d+)$")),
    ("qmoney", re.compile(rf"^its (?P<q>expected loss|total expected cost|expected value) is (?P<cmp>{CMP_RE}) "
                          rf"(?P<v>-?[\d,]+ [A-Za-z][A-Za-z ]*)$")),
    ("qchance", re.compile(rf"^its chance of '(?P<ev>[^']+)' is (?P<cmp>{CMP_RE}) (?P<v>\S+)$")),
    ("amt", re.compile(rf"^its (?P<name>.+?) is (?P<cmp>{CMP_RE}) (?P<v>-?[\d,]+ [A-Za-z][A-Za-z ]*)$")),
]


def parse_part(t: str) -> dict:
    for kind, rx in PART_RES:
        m = rx.match(t)
        if not m:
            continue
        g = m.groupdict()
        if kind == "bool":
            return {"t": "bool", "f": g["f"]}
        if kind == "cat":
            return {"t": "cat", "name": g["name"], "v": g["v"]}
        if kind == "score":
            return {"t": "q", "q": {"k": "score"}, "op": CMP_WORDS[g["cmp"]], "v": Fr(int(g["v"])),
                    "w": g["cmp"]}
        if kind == "qmoney":
            k = {"expected loss": "el", "total expected cost": "tec", "expected value": "ev"}[g["q"]]
            return {"t": "q", "q": {"k": k}, "op": CMP_WORDS[g["cmp"]], "v": parse_money(g["v"])[0], "w": g["cmp"]}
        if kind == "qchance":
            c = parse_chance(g["v"])
            return {"t": "q", "q": {"k": "chance"}, "op": CMP_WORDS[g["cmp"]], "v": c[0], "w": g["cmp"]}
        if kind == "amt":
            mv = parse_money(g["v"])
            if mv is None:
                continue
            return {"t": "amt", "name": g["name"], "op": CMP_WORDS[g["cmp"]], "v": mv[0], "w": g["cmp"]}
    raise ParseError(f"condition part not in the grammar: {t[:60]!r}")


def parse_cond(t: str) -> dict:
    t = t.strip()
    if t.startswith("exactly one of "):
        body = t[len("exactly one of "):]
        ps = re.split(r", (?=its? )| and (?=its? )", body)
        if len(ps) not in (2, 3):
            raise ParseError("exactly one of: 2-3 parts")
        if re.search(r" or (?=its? )", body):
            raise ParseError("mixed connectives")
        return {"conn": "xor1", "parts": [parse_part(p) for p in ps]}
    has_and = bool(re.search(r" and (?=its? )", t))
    has_or = bool(re.search(r" or (?=its? )", t))
    if has_and and has_or:
        raise ParseError("mixed connectives")
    if "exactly one of" in t:
        raise ParseError("nested exactly-one-of")
    if not has_and and not has_or:
        return {"conn": "and", "parts": [parse_part(t)]}
    j = " and " if has_and else " or "
    ps = re.split(rf", (?=its? )|{j}(?=its? )", t)
    if len(ps) > 3:
        raise ParseError("more than 3 parts")
    return {"conn": "and" if has_and else "or", "parts": [parse_part(p) for p in ps]}


# ------------------------------------------------------------------------------------------------ the card
LINE_RES = {
    "points": re.compile(r"^(?P<cond>.+?): (?P<pts>[+-]\d+) points?(?:, unless (?P<unl>.+))?\.$"),
    "floorcap": re.compile(r"^The score floor is (?P<F>\d+) and the score cap is (?P<M>\d+)\.$"),
    "onlyif": re.compile(r"^Tier '(?P<tier>[^']+)' only if (?P<cond>.+)\.$"),
    "override": re.compile(r"^Override: if (?P<cond>.+), the tier is '(?P<tier>[^']+)'\.$"),
    "arule": re.compile(r"^'(?P<a>[^']+)' is required when (?P<cond>.+)\.$"),
    "inv": re.compile(r"^The rule: a (?P<case>.+?) meets the rule when (?P<cond>.+)\.$"),
    "ratings": re.compile(r"^Ratings from lowest to highest: (?P<r>.+)\.$"),
}


def parse_card_text(text: str) -> dict:
    lines = clean_lines(text)
    tables, used = text_tables(lines)
    C = {"sems": [], "sem_slots": [], "lines": [], "F": None, "M": None, "only_if": [], "overrides": [],
         "arules": {}, "inv": None, "tables": tables, "ratings": None, "defs": {}, "unparsed": []}
    for i, ln in enumerate(lines):
        if i in used or not ln:
            continue
        sm = match_sem(ln)
        if sm:
            C["sems"].append(sm[0])
            C["sem_slots"].append(sm[2])
            continue
        for key, rx in LINE_RES.items():
            m = rx.match(ln)
            if not m:
                continue
            g = m.groupdict()
            if key == "points":
                try:
                    cond = parse_cond(g["cond"][:1].lower() + g["cond"][1:])
                except ParseError:
                    continue
                C["lines"].append({"cond": cond, "pts": int(g["pts"]),
                                   **({"unless": parse_cond(g["unl"])} if g.get("unl") else {})})
            elif key == "floorcap":
                C["F"], C["M"] = int(g["F"]), int(g["M"])
            elif key == "onlyif":
                C["only_if"].append((g["tier"], parse_cond(g["cond"])))
            elif key == "override":
                C["overrides"].append((g["tier"], parse_cond(g["cond"])))
            elif key == "arule":
                if g["a"] in C["arules"]:
                    raise ParseError("two action rules for one action (F8-R4-03)")
                C["arules"][g["a"]] = parse_cond(g["cond"])
            elif key == "inv":
                C["inv"] = g
            elif key == "ratings":
                C["ratings"] = re.findall(r"'([^']+)'", g["r"])
            break
    return C


# ------------------------------------------------------------------------------------------------ the question
def _q_res():
    cmp_ = rf"(?P<cmp>{CMP_RE})"
    qn = r"(?P<qn>score|risk|expected loss|total expected cost|expected value|expected number of '(?P<ev>[^']+)'|chance)"
    subj = rf"the {qn} (?:(?:of|for) (?P<id>[A-Z]{{2,4}}-\d{{4}})|that (?P<id2>[A-Z]{{2,4}}-\d{{4}}) is classed '(?P<H>[^']+)')"
    T = r"(?P<T>.+?)"
    return [
        ("yn_thr", 2, re.compile(rf"\bIs it not the case that {subj} is not {cmp_} {T}\?$")),
        ("yn_thr", 1, re.compile(rf"\bIs it true that {subj} is not {cmp_} {T}\?$")),
        ("yn_thr", 0, re.compile(rf"\bIs {subj} {cmp_} {T}\?$")),
        ("yn_act", 2, re.compile(r"\bIs it not the case that (?P<id>[A-Z]{2,4}-\d{2,4}) does not require '(?P<a>[^']+)'\?$")),
        ("yn_act", 1, re.compile(r"\bIs it true that (?P<id>[A-Z]{2,4}-\d{2,4}) does not require '(?P<a>[^']+)'\?$")),
        ("yn_act", 0, re.compile(r"\bDoes (?P<id>[A-Z]{2,4}-\d{2,4}) require '(?P<a>[^']+)'\?$")),
        ("bin", 0, re.compile(r"\b(?:Which range contains|In which range is) the chance that (?P<id>[A-Z]{2,4}-\d{2,4}) is "
                              r"classed '(?P<H>[^']+)'\?$")),
        ("tier", 0, re.compile(r"\b(?:Which tier is (?P<id>[A-Z]{2,4}-\d{2,4}) in|In which tier does (?P<id2>[A-Z]{2,4}-\d{2,4}) "
                               r"fall)\?$")),
        ("mat", 0, re.compile(r"\b(?:Which rating does (?P<id>[A-Z]{2,4}-\d{2,4}) get|What rating does (?P<id2>[A-Z]{2,4}-\d{2,4}) "
                              r"receive)\?$")),
        ("rank_top", 0, re.compile(r"\bWhich (?P<item>[a-z][a-z ]*?) has the (?P<hl>highest|lowest) (?P<qn>.+)\?$")),
        ("rank_order", 0, re.compile(r"\bWhich ordering, highest to lowest (?P<qn>.+), is correct\?$")),
        ("dec", 0, re.compile(r"\bWhich action does the rule for choosing an action select for (?P<id>[A-Z]{2,4}-\d{2,4})\?$")),
        ("pred", 0, re.compile(r"\b(?:Predict which outcome (?P<id>[A-Z]{2,4}-\d{2,4}) will have, using only the chances given|"
                               r"Using only the chances given, predict which outcome (?P<id2>[A-Z]{2,4}-\d{2,4}) will have)\.$")),
        ("inv", 0, re.compile(r"\b(?:Which of these (?P<cases>.+?) meets the rule\?|Which listed (?P<case>.+?) meets the rule\?)$")),
    ]


QRES = _q_res()


def find_question(instr: str):
    """The last question in the instructions (examples inside a moved card block come earlier)."""
    found = None
    for ln in (instr or "").split("\n"):
        ln = ln.strip()
        for form, neg, rx in QRES:
            ms = list(rx.finditer(ln))
            if ms:
                m = ms[-1]
                found = (form, neg, m.groupdict(), m.group(0))
                break
    if not found:
        raise ParseError("no question")
    return found


# ------------------------------------------------------------------------------------------------ the state
class Ents:
    def __init__(self):
        self.order, self.d = [], {}

    def get(self, i: str) -> dict:
        if i not in self.d:
            self.d[i] = {"id": i}
            self.order.append(i)
        return self.d[i]


def _ensure_pts(e):
    e.setdefault("pts", {"b": {}, "c": {}, "a": {}, "stated": {}, "arng": {}})
    return e["pts"]


def _ensure_bay(e, form):
    e.setdefault("bay", {"form": form, "hyps": [], "base": [], "lik": {}, "signs": [], "sig": {}, "rng": {},
                         "rep": {"base": None, "base_den": None, "lik": None, "lik_den": []}, "cnt": {}, "joint": {}})
    return e["bay"]


def _hyp_index(bay, H):
    if H not in bay["hyps"]:
        bay["hyps"].append(H)
    return bay["hyps"].index(H)


def apply_sentence(key: str, g: dict, E: Ents, ctx: dict):
    """Apply one matched fact sentence to the entity table."""
    if key == "base":
        bay = _ensure_bay(ctx["popent"](), "rates")
        j = _hyp_index(bay, g["H"])
        v, rep, den = parse_chance(g["p"])
        while len(bay["base"]) <= j:
            bay["base"].append(None)
        bay["base"][j] = v
        bay["rep"]["base"], bay["rep"]["base_den"] = rep, den
        bl = bay["rep"].setdefault("base_list", [])
        while len(bl) <= j:
            bl.append(None)
        bl[j] = (rep, den)
        return
    if key in ("lik", "lik_nr", "lik_rng"):
        bay = _ensure_bay(ctx["popent"](), "rates")
        j = _hyp_index(bay, g["H"])
        s = g["E"]
        if s not in bay["signs"]:
            bay["signs"].append(s)
        vec = bay["lik"].setdefault(s, [])
        while len(vec) <= j:
            vec.append("MISSING")
        dens = bay["rep"]["lik_den"]
        while len(dens) <= j:
            dens.append(None)
        if key == "lik":
            v, rep, den = parse_chance(g["p"])
            vec[j] = v
            bay["rep"]["lik"] = rep
            dens[j] = den
            ll = bay["rep"].setdefault("lik_list", [])
            while len(ll) <= j:
                ll.append(None)
            ll[j] = (rep, den)
        elif key == "lik_nr":
            vec[j] = None
            bay["rng"].setdefault(f"{s}|{j}", (Fr(0), Fr(1)))
        else:
            lo, hi = parse_chance(g["lo"])[0], parse_chance(g["hi"])[0]
            bay["rng"][f"{s}|{j}"] = (lo, hi)
            bay.setdefault("rngshow", {})[f"{s}|{j}"] = True
        return
    if key == "cnt":
        bay = _ensure_bay(ctx["popent"](), "counts")
        bay["form"] = "counts"
        j = _hyp_index(bay, g["H"])
        s = g["E"]
        if s not in bay["signs"]:
            bay["signs"].append(s)
        vec = bay["cnt"].setdefault(s, [])
        while len(vec) <= j:
            vec.append(None)
        vec[j] = [int(g["a"]), int(g["b"])]
        bay["rep"] = {}
        return
    if key in ("cnt_e", "cnt_ne"):
        bay = _ensure_bay(ctx["popent"](), "nE")
        bay["form"] = "nE"
        j = _hyp_index(bay, g["H"])
        s = g["E"]
        if s not in bay["signs"]:
            bay["signs"].append(s)
        vec = bay.setdefault("ne", {}).setdefault(s, [])
        while len(vec) <= j:
            vec.append(None)
        vec[j] = int(g["a"])
        bay.setdefault("ne_n", {})[s] = int(g["n"])
        bay.setdefault("ne_shown", {})[s] = key == "cnt_e"
        bay["rep"] = {}
        return
    if key == "joint":
        bay = _ensure_bay(ctx["popent"](), "joint")
        bay["form"] = "joint"
        j = _hyp_index(bay, g["H"])
        s = g["E"]
        if s not in bay["signs"]:
            bay["signs"].append(s)
        vec = bay["joint"].setdefault(s, [])
        while len(vec) <= j:
            vec.append(None)
        vec[j] = parse_chance(g["p"])[0]
        bay["rep"] = {"joint": "pct0"}
        return
    e = E.get(g["ID"]) if "ID" in g else None
    if key in ("sig_yes", "sig_no", "f_yes", "f_no", "f_nr"):
        lab = g.get("E") or g.get("F")
        ctx.setdefault("shows", {}).setdefault(g["ID"], {})[lab] = None if key == "f_nr" else \
            (key in ("sig_yes", "f_yes"))
        return
    if key == "cat":
        _ensure_pts(e)["c"][g["cat"]] = g["v"]
        return
    if key == "amt":
        _ensure_pts(e)["a"][g["amtname"]] = parse_money(g["money"])[0]
        return
    if key == "amt_nr":
        _ensure_pts(e)["a"][g["amtname"]] = None
        return
    if key == "amt_rng":
        p = _ensure_pts(e)
        p["arng"][g["amtname"]] = (parse_money(g["lo"])[0], parse_money(g["hi"])[0])
        return
    if key.endswith("_net"):
        ctx["net"] = True
        key = key[:-4] if key != "out_net" else key
    if key in ("out", "out_net", "outp_nr", "outa_nr"):
        outs = e.setdefault("outs", [])
        o = {"ev": g["event"], "p": None, "a": None, "prep": None, "pden": None, "prng": None, "arng": None}
        if key in ("out", "out_net", "outa_nr"):
            v, rep, den = parse_chance(g["p"])
            o["p"], o["prep"], o["pden"] = v, rep, den
        if key in ("out", "out_net", "outp_nr"):
            o["a"] = parse_money(g["money"])[0]
        if key == "out_net":
            ctx["net"] = True
        outs.append(o)
        return
    if key in ("outp_rng", "ch_rng"):
        ctx.setdefault("prng", {})[(g["ID"], g["event"])] = (parse_chance(g["lo"])[0], parse_chance(g["hi"])[0])
        return
    if key == "outa_rng":
        ctx.setdefault("arng", {})[(g["ID"], g["event"])] = (parse_money(g["lo"])[0], parse_money(g["hi"])[0])
        return
    if key == "cost":
        if g["money"] == "None":
            e["cost"], e["cost_word"] = Fr(0), "None"
        else:
            v = parse_money(g["money"])[0]
            e["cost"] = v
            e["cost_word"] = "0" if v == 0 else None
        return
    if key == "act":
        e["action"] = g["action"]
        return
    if key in ("ch", "ch_nr", "ch_rng"):
        ch = e.setdefault("ch", {"p": None, "rep": None, "den": None, "ev": g["event"], "rng": None})
        if key == "ch":
            if e.get("_has_loss_for") == g["event"] or ctx.get("mat"):
                pass
            v, rep, den = parse_chance(g["p"])
            ch["p"], ch["rep"], ch["den"] = v, rep, den
        elif key == "ch_rng":
            ch["rng"] = (parse_chance(g["lo"])[0], parse_chance(g["hi"])[0])
        return
    if key == "loss":
        e["loss"] = parse_money(g["money"])[0]
        return
    if key == "en":
        v, rep, den = parse_chance(g["p"])
        e["en"] = {"n": int(g["n"]), "p": v, "rep": rep, "den": den, "ev": g["event"], "units": g["units"]}
        return
    if key == "cnt_cap":
        ctx["cnt_sign"] = g["E"]
        return
    if key in ("tbl_cap", "tbl_cap_ch"):
        ctx["tbl_event"] = g["event"]
        return


def parse_state(state: str, style_id: str, card_labels: dict) -> tuple:
    """(entities in order, context) from the state text."""
    A = atoms(state, style_id)
    labels = card_labels
    E = Ents()
    ctx = {"sigs": {}, "pop_owner": None, "net": False, "sem_lines": [], "rule_lines": []}

    def popent():
        if ctx.get("_pop") is None:
            ctx["_pop"] = {"id": "__pop__"}
        return ctx["_pop"]
    ctx["popent"] = popent
    sentences = []
    for t in A["texts"]:
        for ln in t.split("\n"):
            sentences += split_sentences(ln)
    # tables
    for header, rows in A["tables"]:
        h = [norm_key(c) for c in header]
        if h == ["class", "showed the sign", "did not show the sign"]:
            cid = ctx.get("case_id")
            ctx["counts"] = [(r[0], int(r[1]), int(r[2])) for r in rows]
            continue
        if h and h[0] == "reference":
            for r in rows:
                e = E.get(r[0])
                for c, val in zip(header[1:], r[1:]):
                    nc = norm_key(c)
                    if nc == "event":
                        e.setdefault("_tbl", {})["event"] = val
                        continue
                    if nc == "chance":
                        if "outs" in e or (len(h) >= 3 and "loss" in h):
                            e.setdefault("_tbl", {})["chance"] = val
                        else:
                            ch = e.setdefault("ch", {"p": None, "rep": None, "den": None, "ev": None, "rng": None})
                            if val != "not recorded":
                                v, rep, den = parse_chance(val)
                                ch["p"], ch["rep"], ch["den"] = v, rep, den
                    elif nc == "loss":
                        e.setdefault("_tbl", {})["loss"] = val
                    elif nc == "own cost":
                        e.setdefault("_tbl", {})["cost"] = val
                    elif nc in labels["bool"]:
                        p = _ensure_pts(e)
                        p["b"][labels["bool"][nc]] = None if val == "not recorded" else (val == "yes")
                        p["stated"][labels["bool"][nc]] = True
                    elif nc in labels["cat"]:
                        _ensure_pts(e)["c"][labels["cat"][nc]] = val
                    elif nc in labels["amt"]:
                        mv = parse_money(val)
                        _ensure_pts(e)["a"][labels["amt"][nc]] = mv[0] if mv else None
    seen = set()
    for s in sentences:
        hit = False
        for key, rx in SENT_RES():
            m = rx.match(s)
            if m:
                sig = (key, s)
                if sig in seen:
                    hit = True
                    break
                seen.add(sig)
                apply_sentence(key, m.groupdict(), E, ctx)
                hit = True
                break
        if not hit:
            ctx["rule_lines"].append(s)
    # key-value atoms (S2 fields, HTML th/td, key-value and form lines, prose field sentences); line grammars are
    # the skin's own data (formats-1 skins.jsonl 'grammar'), never renderer code
    kvs = list(A["kv"])
    st = STYLES()[style_id]
    gram = SKINS()[st["skin"]].get("grammar", {}).get("lines", {})
    kv_res = []
    for name, rx in gram.items():
        if ("key" in rx or "label" in rx) and "value" in rx:
            try:
                kv_res.append(re.compile(rx))
            except re.error:
                pass
    kv_res.append(re.compile(r"^(?:The )?(?P<key>[^:]+?)(?::| is) (?P<value>.+?)\.?$"))
    raw_lines = [ln for t in A["texts"] for ln in t.split("\n")]
    for s in raw_lines + sentences:
        if any(rx.match(s) for _, rx in SENT_RES()):
            continue
        for rx in kv_res:
            m = rx.match(s.strip())
            if m:
                g = m.groupdict()
                k = g.get("key") or g.get("label")
                v = g.get("value")
                if k and v:
                    kvs.append((k.strip(), v.strip()))
                break
    cur = None
    labels = card_labels
    for k, v in kvs:
        nk = norm_key(k)
        if nk == "reference":
            cur = E.get(v.strip())
            continue
        if cur is None:
            continue
        if nk == "event":
            cur.setdefault("_tbl", {})["event"] = v
            continue
        if nk in ("chance", "loss", "own cost"):
            if nk == "chance" and "loss" not in [norm_key(x) for x, _ in kvs] and cur.get("outs") is None:
                ch = cur.setdefault("ch", {"p": None, "rep": None, "den": None, "ev": None, "rng": None})
                if v != "not recorded":
                    ch["p"], ch["rep"], ch["den"] = parse_chance(v)
            else:
                cur.setdefault("_tbl", {})[nk if nk != "own cost" else "cost"] = v
            continue
        if nk in labels["bool"]:
            f = labels["bool"][nk]
            p = _ensure_pts(cur)
            vv = v.strip().lower()
            if vv not in ("yes", "no", "not recorded"):
                continue
            p["b"][f] = None if vv == "not recorded" else (vv == "yes")
            p["stated"][f] = True
        elif nk in labels["cat"]:
            _ensure_pts(cur)["c"][labels["cat"][nk]] = v.strip()
        elif nk in labels["amt"]:
            mv = parse_money(v)
            _ensure_pts(cur)["a"][labels["amt"][nk]] = None if v.strip() == "not recorded" else (mv[0] if mv else None)
    return E, ctx


# ------------------------------------------------------------------------------------------------ assemble
def _label_maps(C: dict) -> dict:
    b, c, a = {}, {}, {}
    conds = [ln["cond"] for ln in C["lines"]] + [ln["unless"] for ln in C["lines"] if ln.get("unless")]
    conds += [x[1] for x in C["only_if"]] + [x[1] for x in C["overrides"]] + list(C["arules"].values())
    for cond in conds:
        for p in cond["parts"]:
            if p["t"] == "bool":
                b[norm_key(p["f"])] = p["f"]
            elif p["t"] == "cat":
                c[norm_key(p["name"])] = p["name"]
            elif p["t"] == "amt":
                a[norm_key(p["name"])] = p["name"]
    return {"bool": b, "cat": c, "amt": a}


def parse_row(row: dict) -> dict:
    style_id = row["meta"]["format_style"]
    qtype = row["qtype"]
    instr = row.get("instructions") or ""
    card_txt = row.get("card") or ""
    form, neg, qg, qline = find_question(instr)
    rule_text = card_txt if qtype == "noul" else instr
    st_texts = "\n".join(atoms(row.get("state") or "", style_id)["texts"])
    C = parse_card_text(rule_text + "\n" + st_texts)
    if qtype == "choice" and card_txt:
        for ln in card_txt.split("\n"):
            m = re.match(r"^- (.+?): (.+)$", ln)
            if m:
                C["defs"][m.group(1)] = m.group(2)
    labels = _label_maps(C)
    E, ctx = parse_state(row.get("state") or "", style_id, labels)
    return {"C": C, "E": E, "ctx": ctx, "form": form, "neg": neg, "qg": qg, "qline": qline, "labels": labels}


# ------------------------------------------------------------------------------------------------ structure
def _range_text(t: str):
    """Bin / level range option text -> (lo, hi, conv, lo_incl, hi_incl)."""
    def pc(x):
        c = parse_chance(x)
        if c is None:
            raise ParseError(f"range end {x!r}")
        return c[0]
    m = re.fullmatch(r"at least (\S+) and below (\S+)", t)
    if m:
        return pc(m.group(1)), pc(m.group(2)), "lo"
    m = re.fullmatch(r"at least (\S+) and at most 100%", t)
    if m:
        return pc(m.group(1)), Fr(1), "lo_top"
    m = re.fullmatch(r"above (\S+) and at most (\S+)", t)
    if m:
        return pc(m.group(1)), pc(m.group(2)), "hi"
    m = re.fullmatch(r"at least 0% and at most (\S+)", t)
    if m:
        return Fr(0), pc(m.group(1)), "hi_bottom"
    raise ParseError(f"range form {t!r}")


def _cut_ranges(rows):
    cuts = []
    for i, (name, rng) in enumerate(rows):
        m = re.fullmatch(r"below (\d+)", rng) if i == 0 else (re.fullmatch(r"at least (\d+)", rng)
                                                               if i == len(rows) - 1 else
                                                               re.fullmatch(r"at least (\d+) and below (\d+)", rng))
        if not m:
            raise ParseError("cut table range form")
        if i == 0:
            first = int(m.group(1))
        else:
            cuts.append(int(m.group(1)))
    if cuts and cuts[0] != first:
        raise ParseError("cut table does not partition")
    return cuts


def _money_ranges(rows):
    edges = []
    for i, rng in enumerate(rows):
        if i == 0:
            m = re.fullmatch(r"below (.+)", rng)
            edges.append(parse_money(m.group(1))[0])
        elif i == len(rows) - 1:
            m = re.fullmatch(r"at least (.+)", rng)
            if parse_money(m.group(1))[0] != edges[-1]:
                raise ParseError("impact ranges do not partition")
        else:
            m = re.fullmatch(r"at least (.+?) and below (.+)", rng)
            if parse_money(m.group(1))[0] != edges[-1]:
                raise ParseError("impact ranges do not partition")
            edges.append(parse_money(m.group(2))[0])
    return edges


def _bin_rows(rows, sort=False):
    edges, conv = [], None
    if sort:
        rows = sorted(rows, key=lambda r: _range_text(r)[0])
    for i, r in enumerate(rows):
        lo, hi, c = _range_text(r)
        c0 = "lo" if c.startswith("lo") else "hi"
        conv = conv or c0
        if c0 != conv:
            raise ParseError("mixed range conventions")
        if i < len(rows) - 1:
            edges.append(hi)
    return edges, conv


def _q_from_name(qn: str, C: dict) -> dict:
    if qn == "score":
        return {"k": "score"}
    if qn == "risk":
        slots = [s for k, s in zip(C["sems"], C["sem_slots"]) if k == "SEM-22"]
        if not slots:
            raise ParseError("'risk' without SEM-22 (lint)")
        d = slots[0]["qdef"]
        return {"k": "risk", "def": {"expected loss": "el", "score": "score", "total expected cost": "tec"}.get(
            d, "chance" if d.startswith("chance of") else None)}
    if qn == "expected loss":
        return {"k": "el"}
    if qn == "total expected cost":
        return {"k": "tec"}
    if qn == "expected value":
        return {"k": "ev"}
    if qn.startswith("expected number of"):
        return {"k": "en"}
    if qn.startswith("chance of"):
        return {"k": "chance"}
    if qn == "chance":
        return {"k": "post"}
    raise ParseError(f"quantity {qn!r}")


def assemble(P: dict, row: dict) -> dict:
    C, E, ctx = P["C"], P["E"], P["ctx"]
    form, neg, qg = P["form"], P["neg"], P["qg"]
    state_has_nr = "not recorded" in (row.get("state") or "")
    opts = row.get("options")
    S = {"form": form, "world": "open" if state_has_nr else "closed", "case": None, "ents": [], "rules": {},
         "q": {}}
    # rules
    R = S["rules"]
    if C["lines"]:
        if C["F"] is None:
            raise ParseError("scorecard without floor and cap")
        R["scorecard"] = {"lines": C["lines"], "F": C["F"], "M": C["M"]}
    if C["arules"]:
        R["arules"] = C["arules"]
    for header, rows in C["tables"]:
        h = [norm_key(c) for c in header]
        if h == ["tier", "score range"]:
            R["tiers"] = [r[0] for r in rows]
            R["cuts"] = _cut_ranges([(r[0], r[1]) for r in rows])
        elif h and h[0] == "likelihood level" and len(h) == 2:
            R.setdefault("mat", {})["lik_names"] = [r[0] for r in rows]
            e, conv = _bin_rows([r[1] for r in rows])
            R["mat"]["lik_edges"], R["mat"]["lik_conv"] = e, conv
        elif h and h[0] == "impact level":
            R.setdefault("mat", {})["imp_names"] = [r[0] for r in rows]
            R["mat"]["imp_edges"] = _money_ranges([r[1] for r in rows])
            R["mat"]["impact"] = "loss" if h[1] == "loss" else "expected"
        elif h and h[0] == "likelihood level" and len(h) > 2:
            R.setdefault("mat", {})["_grid"] = (header[1:], rows)
    if R.get("tiers"):
        R["only_if"] = {}
        for t, c in C["only_if"]:
            R["only_if"][R["tiers"].index(t)] = c
        R["overrides"] = [{"cond": c, "tier": R["tiers"].index(t)} for t, c in C["overrides"]]
    if R.get("mat"):
        m = R["mat"]
        m["ratings"] = C["ratings"]
        names, rows = m.pop("_grid")
        m["grid"] = [[m["ratings"].index(x) for x in r[1:]] for r in rows]
        if [r[0] for r in rows] != m["lik_names"] or list(names) != m["imp_names"]:
            raise ParseError("grid labels")
    # entities
    ents = [E.d[i] for i in E.order if i != "__pop__"]
    case_id = qg.get("id") or qg.get("id2")
    pop = ctx.get("_pop")
    if pop and pop.get("bay"):
        tgt = E.get(case_id) if case_id else None
        if tgt is None:
            raise ParseError("population data without a case")
        tgt["bay"] = pop["bay"]
        if tgt["id"] not in [x["id"] for x in ents]:
            ents.append(tgt)
    if ctx.get("counts"):
        tgt = E.get(case_id)
        s = ctx.get("cnt_sign")
        tgt["bay"] = {"form": "counts", "hyps": [r[0] for r in ctx["counts"]],
                      "cnt": {s: [[r[1], r[2]] for r in ctx["counts"]]}, "signs": [s], "sig": {}, "base": None,
                      "lik": {}, "rng": {}, "rep": {}}
        if tgt["id"] not in [x["id"] for x in ents]:
            ents.append(tgt)
    has_rules = bool(C["lines"] or C["arules"] or C["only_if"] or C["overrides"])
    rule_bools = set(P["labels"]["bool"].values())
    for e in ents:
        shows = ctx.get("shows", {}).get(e["id"], {})
        if has_rules:
            p = _ensure_pts(e)
            for lab, v in shows.items():
                if lab in rule_bools:
                    p["b"][lab] = v
                    p["stated"][lab] = True
        if e.get("bay"):
            e["bay"]["sig"] = {s: shows[s] for s in e["bay"]["signs"] if s in shows}
            if e["bay"]["form"] == "rates":
                for s, vec in e["bay"]["lik"].items():
                    if "MISSING" in vec:
                        raise ParseError("a listed sign without a chance for some class")
                if any(x is None for x in e["bay"]["base"]):
                    raise ParseError("missing base rate")
            if set(e["bay"]["sig"]) != set(e["bay"]["signs"]):
                raise ParseError("a listed sign not stated for the case (F8-R3-02)")
        t = e.pop("_tbl", None)
        if t:
            if e.get("ch") is not None and "loss" not in t and "chance" not in t:
                e["ch"]["ev"] = t.get("event")
            elif "loss" in t or "chance" in t:
                ev = t.get("event") or ctx.get("tbl_event")
                o = {"ev": ev, "p": None, "a": None, "prep": None, "pden": None, "prng": None, "arng": None}
                if t.get("chance") and t["chance"] != "not recorded":
                    o["p"], o["prep"], o["pden"] = parse_chance(t["chance"])
                if t.get("loss"):
                    o["a"] = parse_money(t["loss"])[0]
                e["outs"] = [o]
                if t.get("cost"):
                    if t["cost"] == "None":
                        e["cost"], e["cost_word"] = Fr(0), "None"
                    else:
                        e["cost"] = parse_money(t["cost"])[0]
        for (eid, ev), rg in (ctx.get("prng") or {}).items():
            if eid != e["id"]:
                continue
            hit = [o for o in e.get("outs") or [] if o["ev"] == ev and o["p"] is None]
            if hit:
                hit[0]["prng"] = rg
                hit[0]["prng_show"] = True
            else:
                ch = e.setdefault("ch", {"p": None, "rep": None, "den": None, "ev": ev, "rng": None})
                ch["rng"] = rg
        for (eid, ev), rg in (ctx.get("arng") or {}).items():
            if eid != e["id"]:
                continue
            for o in e.get("outs") or []:
                if o["ev"] == ev and o["a"] is None:
                    o["arng"] = rg
                    o["arng_show"] = True
        if "loss" in e and form == "mat":
            ch = e.pop("ch")
            e["mat"] = {"lik": ch["p"], "amt": e.pop("loss"), "rep": ch["rep"], "den": ch["den"], "p": ch["p"]}
    S["ents"] = ents
    ids = [e["id"] for e in ents]
    for e in ents:
        if e.get("ch") is not None and "loss" in e and form != "mat":
            e["ch"]["amt"] = e.pop("loss")
    # question
    if form in ("yn_thr", "yn_act", "bin", "tier", "mat", "pred"):
        if case_id not in ids:
            raise ParseError("question names no listed case")
        S["case"] = ids.index(case_id)
    if form == "yn_thr":
        q = _q_from_name(qg["qn"], C)
        if q["k"] == "post":
            hyps = ents[S["case"]]["bay"]["hyps"]
            q["h"] = hyps.index(qg["H"])
        S["q"] = q
        T = qg["T"]
        k = q["k"] if q["k"] != "risk" else q["def"]
        if k in ("post", "chance"):
            v, rep, den = parse_chance(T)
            S["thr"] = {"op": CMP_WORDS[qg["cmp"]], "T": v, "neg": neg, "trep": {"rep": rep, "denom": den}}
        elif k == "score":
            S["thr"] = {"op": CMP_WORDS[qg["cmp"]], "T": Fr(int(T)), "neg": neg, "trep": {}}
        elif k == "en":
            S["thr"] = {"op": CMP_WORDS[qg["cmp"]], "T": parse_num(T), "neg": neg, "trep": {}}
        else:
            S["thr"] = {"op": CMP_WORDS[qg["cmp"]], "T": parse_money(T)[0], "neg": neg, "trep": {}}
        S["cmp_word"] = qg["cmp"]
    elif form == "yn_act":
        S["act"] = {"action": qg["a"], "neg": neg}
        S["q"] = {"k": "score"} if R.get("scorecard") else {"k": "none"}
    elif form == "bin":
        R["bins"], R["bin_conv"] = _bin_rows([o for o in opts if o != LEX()["CBD"]], sort=True)
        hyps = ents[S["case"]]["bay"]["hyps"]
        S["q"] = {"k": "post", "h": hyps.index(qg["H"])}
    elif form == "tier":
        S["q"] = {"k": "score"}
    elif form == "mat":
        S["q"] = {"k": "rating"}
    elif form == "pred":
        S["q"] = {"k": "post", "h": 0}
    elif form == "rank_top":
        S["hl"] = "high" if qg["hl"] == "highest" else "low"
        S["q"] = _q_from_name(qg["qn"], C)
    elif form == "rank_order":
        S["q"] = _q_from_name(qg["qn"], C)
        if len(ents) == 5:
            orders = [tuple(ids.index(x) for x in o.split(", ")) for o in opts if o != LEX()["NOTA"]]
            X = None
            for x in range(5):
                pos = sorted({o.index(x) for o in orders})
                if len(pos) <= 2:
                    X, P_ = x, pos
                    break
            if X is None:
                raise ParseError("5-item subset is not a P1/P2 class")
            S["subset"] = {"X": X, "pos": P_}
    elif form == "dec":
        S["q"] = {"k": "tec"}
        S["dec_case"] = case_id
    elif form == "inv":
        g = C["inv"]
        if g is None:
            raise ParseError("INV without a rule")
        m = re.fullmatch(r"it requires '([^']+)'", g["cond"])
        if m:
            R["inv"] = {"kind": "act", "action": m.group(1), "q": None, "op": None, "v": None, "w": None}
        else:
            p = parse_part(g["cond"])
            if p["t"] != "q":
                raise ParseError("INV rule is not a quantity comparison")
            R["inv"] = {"kind": "q", "q": p["q"], "op": p["op"], "v": p["v"], "w": p["w"]}
        S["q"] = R["inv"]["q"] or {"k": "none"}
    qk = S["q"].get("def") if S["q"].get("k") == "risk" else S["q"].get("k")
    if qk == "chance":
        for e in ents:
            if e.get("outs") and e.get("ch") is None and len(e["outs"]) == 1 and e.get("cost") is None:
                o = e.pop("outs")[0]
                e["ch"] = {"p": o["p"], "rep": o["prep"], "den": o["pden"], "ev": o["ev"],
                           "rng": o.get("prng"), "amt": o["a"]}
    if any(e.get("outs") for e in ents):
        S["mode"] = "net" if (ctx.get("net") or "SEM-20net" in C["sems"]) else "loss"
    else:
        S["mode"] = None
    if form in ("rank_top", "dec", "inv", "bin") and opts and LEX()["CBD"] in opts:
        S["world"] = "open"
    if form == "inv" and opts and LEX()["NOTA"] in opts:
        S["world"] = "closed"
    return S


def option_keys(S: dict, row: dict) -> dict:
    """Option text -> answer key (index, tuple, 'CBD', 'NOTA'), read from the options and the parsed structure."""
    opts = row.get("options")
    out = {}
    if row["qtype"] == "noul":
        return {"Yes": True, "No": False}
    ids = [e["id"] for e in S["ents"]]
    f = S["form"]
    for o in opts:
        if o == LEX()["CBD"]:
            out[o] = "CBD"
        elif o == LEX()["NOTA"]:
            out[o] = "NOTA"
        elif f == "bin":
            lo, hi, c = _range_text(o)
            edges = S["rules"]["bins"]
            out[o] = sum(1 for e in edges if e <= lo)
        elif f == "tier":
            out[o] = S["rules"]["tiers"].index(o)
        elif f == "mat":
            out[o] = S["rules"]["mat"]["ratings"].index(o)
        elif f == "pred":
            out[o] = S["ents"][S["case"]]["bay"]["hyps"].index(o)
        elif f in ("rank_top", "inv"):
            out[o] = ids.index(o)
        elif f == "dec":
            acts = [e.get("action") for e in S["ents"]]
            out[o] = acts.index(o)
        elif f == "rank_order":
            out[o] = tuple(ids.index(x) for x in o.split(", "))
    return out
