"""G3 round-trip parsers, written from the G0 spec (section 6), not from the renderer:

  flatten(state)       container-agnostic reading of the rendered state: standard JSON / YAML / CSV readers, HTML
                       tags stripped, fences and list markers removed -> text lines and table rows (cell lists);
  split_sentences      sentence split of prose paragraphs;
  parse_card(card)     SEM keys printed (frozen rendering registry) + card constants (value sets, two-state pairs,
                       covered period, source, q / m);
  extract_question     the question inside `instructions` (wording pool and register prefixes removed);
  parse_question(q)    cue grammar -> canonical LF, k (counted operators), families, matrix L_core check;
  s1_parse(...)        S1 rules / case facts / role-action table grammar -> parsed structure (solver B input).
"""
from __future__ import annotations

import csv
import html
import io
import json
import re

import yaml

from . import sem
from .common import FMT2, L_CORE, read_jsonl
from .texts import ATTACK_RE

ATT = re.compile(ATTACK_RE)

# ---------------------------------------------------------------------------------------------------------------------
# state flattening


def _strip_fence(s: str) -> str:
    m = re.search(r"```[a-z]*\n(.*?)\n```", s, re.S)
    if m:
        return m.group(1)
    m = re.search(r"~~~[a-z]*\n(.*?)\n~~~", s, re.S)
    if m:
        return m.group(1)
    lines = s.split("\n")
    if lines and all((ln.startswith("    ") or not ln.strip()) for ln in lines[1:]) and len(lines) > 2:
        body = [ln[4:] for ln in lines if ln.startswith("    ") or not ln.strip()]
        return "\n".join(body)
    return s


def _walk(x, lines, rows):
    if isinstance(x, dict):
        vals = list(x.values())
        if vals and all(isinstance(v, (str, int, float)) or v is None for v in vals):
            rows.append([("null" if v is None else str(v)) for v in vals])
        for v in vals:
            _walk(v, lines, rows)
    elif isinstance(x, list):
        for v in x:
            _walk(v, lines, rows)
    elif isinstance(x, str):
        lines.append(x)
    elif x is None:
        lines.append("null")
    else:
        lines.append(str(x))


def flatten(state: str):
    """(lines, rows): lines = text lines in reading order; rows = table rows as cell lists (header rows included)."""
    body = _strip_fence(state)
    for candidate in (body, body.split("\n", 2)[-1] if body.count("\n") >= 2 else body):
        try:
            obj = json.loads(candidate.strip())
            lines, rows = [], []
            _walk(obj, lines, rows)
            return lines, rows
        except Exception:
            pass
    if re.search(r"^\s*[A-Za-z_][A-Za-z0-9_ ]*:\s", body, re.M) and ("\n- " in body or "\n  " in body or
                                                                       body.lstrip().startswith(("title:", "-"))):
        try:
            obj = yaml.safe_load(body)
            if isinstance(obj, (dict, list)):
                lines, rows = [], []
                _walk(obj, lines, rows)
                return lines, rows
        except Exception:
            pass
    if "<" in body and re.search(r"</(li|p|td|div|section|ul|table|h\d)>", body):
        rows = []
        for tr in re.findall(r"<tr>(.*?)</tr>", body, re.S):
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)
            rows.append([html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells])
        t = re.sub(r"<tr>.*?</tr>", "\n", body, flags=re.S)
        t = re.sub(r"<br\s*/?>", "\n", t)
        t = re.sub(r"</?(li|p|div|section|ul|ol|table|h\d|article|header|footer|span|strong|em|b|i|dl|dt|dd)[^>]*>",
                   "\n", t)
        t = re.sub(r"<[^>]+>", "", t)
        lines = [html.unescape(x).strip() for x in t.split("\n")]
        return [x for x in lines if x], rows
    lines, rows = [], []
    raw = body.split("\n")
    # csv-like blocks (a delimiter on every line of a block)
    for ln in raw:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
            continue
        lines.append(s)
    return lines, rows


def csv_rows(state: str):
    """The largest block of consecutive CSV / TSV / semicolon / pipe rows with one column count (>= 3)."""
    body = _strip_fence(state)
    for delim in (",", ";", "\t", "|"):
        try:
            rd = list(csv.reader(io.StringIO(body), delimiter=delim))
        except Exception:
            continue
        best, cur = [], []
        for r in rd:
            if len(r) >= 3 and (not cur or len(r) == len(cur[0])):
                cur.append(r)
            else:
                if len(cur) > len(best):
                    best = cur
                cur = [r] if len(r) >= 3 else []
        if len(cur) > len(best):
            best = cur
        if len(best) >= 2:
            return best
    return []


_BULLET = re.compile(r"^(?:[-*•+]\s+|\d+[.)]\s+|\(\d+\)\s+|[a-z][.)]\s+|>\s*|§\s*\d*\s*)")


def clean_line(s: str) -> str:
    s = s.strip()
    prev = None
    while prev != s:
        prev = s
        s = _BULLET.sub("", s).strip()
    s = re.sub(r"^[a-z_]+\s*[:=]\s+", "", s) if re.match(r"^[a-z_]+\s*[:=]\s+[A-Z]", s) else s
    return s


def split_sentences(line: str):
    parts = re.split(r"(?<=\.)\s+(?=(?:R\d+\.|E\d+\.|[A-Z\"]))", line)
    out = []
    for p in parts:
        if out and re.fullmatch(r"(?:R|E)\d+\.", out[-1]):
            out[-1] = out[-1] + " " + p
        else:
            out.append(p)
    return [x.strip() for x in out if x.strip()]


def sentences(state: str):
    lines, rows = flatten(state)
    out = []
    for ln in lines:
        for s in split_sentences(clean_line(ln)):
            out.append(s)
    return out, rows


# ---------------------------------------------------------------------------------------------------------------------
# card parser

def _tmpl_regex(t: str) -> str:
    parts = re.split(r"(\{[a-zA-Z_]+\})", t)
    rx = ""
    for p in parts:
        if re.fullmatch(r"\{[a-zA-Z_]+\}", p):
            name = p[1:-1]
            rx += f"(?P<{name}>.+?)" if name not in rx else ".+?"
        else:
            rx += re.escape(" ".join(p.split()))
    return rx


_REG = None


def registry_regex():
    global _REG
    if _REG is None:
        _REG = []
        for k, temps in sem.registry().items():
            for t in temps:
                first = t.split(". ")[0] if not t.startswith('"') else t[: max(60, t.find(". ") + 1)]
                _REG.append((k, re.compile(_tmpl_regex(first if k not in ("SEM-17", "SEM-18", "SEM-27") else t))))
    return _REG


def parse_card(card: str):
    """Printed SEM keys and the card constants the structure parser needs."""
    txt = " ".join((card or "").split())
    keys = set()
    consts = {"value_sets": {}, "affixed": {}, "S": None, "period": None, "q": None, "m": None, "etype": None}
    for k, rx in registry_regex():
        for m in rx.finditer(txt):
            keys.add(k)
            gd = m.groupdict()
            if k == "SEM-17" and gd.get("attr"):
                vals = gd.get("values") or ""
                consts["value_sets"][gd["attr"].strip()] = [v.strip() for v in vals.split(", ")]
            if k == "SEM-18" and gd.get("pos"):
                consts["affixed"][gd["neg"]] = gd["pos"]
            if k == "SEM-27" and gd.get("D_start"):
                consts["period"] = (gd["D_start"].strip(), gd["D_end"].strip())
            if k in ("SEM-16", "SEM-20", "SEM-31") and gd.get("S"):
                consts["S"] = gd["S"].strip()
            if k == "SEM-25" and gd.get("q"):
                consts["q"], consts["m"] = gd.get("q"), gd.get("m")
    # SEM-17 / SEM-18 value lists end at the sentence end
    for m in re.finditer(r"has exactly one (.+?) at a time, one of: (.+?)\.(?: |$)", txt):
        consts["value_sets"][m.group(1)] = [v.strip() for v in m.group(2).split(", ")]
    for m in re.finditer(r"exactly one (.+?), one of: (.+?)\.(?: |$)", txt):
        a = m.group(1).strip()
        a = a[: -len(" at a time")] if a.endswith(" at a time") else a
        consts["value_sets"][a] = [v.strip() for v in m.group(2).split(", ")]
    for m in re.finditer(r'"([a-z-]+)" has two states only(?::|, and) "([a-z-]+)" means exactly "not ([a-z-]+)"', txt):
        consts["affixed"][m.group(2)] = m.group(1)
    m = re.search(r"covers (\S+(?: \S+ \S+)?) to (\S+(?: \S+ \S+)?), both included", txt)
    if m:
        consts["period"] = (m.group(1), m.group(2))
    consts["world"] = "closed" if "SEM-02" in keys else ("open" if "SEM-03" in keys else None)
    return keys, consts


# ---------------------------------------------------------------------------------------------------------------------
# question extraction and the cue grammar

_WORDINGS = None


def wording_texts():
    global _WORDINGS
    if _WORDINGS is None:
        ws = [w for w in read_jsonl(FMT2 / "wordings" / "family_pools.jsonl") if w["family"] == "F5"]
        _WORDINGS = sorted({w["text"] for w in ws} | {w["text_gb"] for w in ws}, key=len, reverse=True)
    return _WORDINGS


def extract_question(instr: str) -> str:
    s = instr
    for w in wording_texts():
        if w in s:
            s = s.replace(w, "\n")
            break
    cands = [x.strip() for x in s.split("\n") if x.strip().endswith("?")]
    if not cands:
        raise ValueError("no question in instructions")
    q = cands[-1]
    for p in q_prefixes():
        if q.startswith(p + " "):
            q = q[len(p) + 1:]
            break
    return q


_QP = None


def q_prefixes():
    """Register question prefixes (formats-1 registers data), longest first."""
    global _QP
    if _QP is None:
        from .common import FMT1
        regs = read_jsonl(FMT1 / "data" / "registers.jsonl")
        _QP = sorted({r["q_prefix"] for r in regs if r.get("q_prefix")}, key=len, reverse=True)
    return _QP


FRAMES_P = [r"Is it true that (.+)\?", r"Is the following statement true: (.+)\?", r"Is it the case that (.+)\?",
            r"Does the record show that (.+)\?", r"According to the record, is it true that (.+)\?",
            r"Based on the text, is it the case that (.+)\?", r"Is this assertion true: (.+)\?",
            r"Do the facts given establish that (.+)\?", r"Taking the record as given, is it true that (.+)\?",
            r"Is the statement that (.+) true\?"]
TAILS_P = [", according to the record", ", on the facts given", ", going by the text", ", based on the record"]


class QParseError(ValueError):
    pass


class Q:
    def __init__(self):
        self.k = 0
        self.fams = []
        self.frame = None
        self.outer = None

    def add(self, fam, n=1):
        self.k += n
        self.fams.append(fam)


def parse_question(q: str, ctx: dict):
    """ctx: affixed {neg: pos}, value sets, subjects; returns (lf, k, families, outer)."""
    st = Q()
    m = re.fullmatch(r"Is it false that (.+)\?", q)
    if m:
        st.outer = "C2m"
        st.add("C2")
        inner = m.group(1)
        for t in TAILS_P:
            if inner.endswith(t):
                inner = inner[: -len(t)]
        lf = ["not", parse_decl(inner, st, ctx)]
        return lf, st.k, st.fams, st.outer
    for i, pat in enumerate(FRAMES_P):
        m = re.fullmatch(pat, q)
        if m:
            st.outer = f"F{i + 1:02d}"
            return parse_decl(m.group(1), st, ctx), st.k, st.fams, st.outer
    st.outer = "mq"
    body = q[:-1] if q.endswith("?") else q
    for t in TAILS_P:
        if body.endswith(t):
            body = body[: -len(t)]
    toks = set(re.findall(r"[a-z']+", body.lower()))
    if toks & set(L_CORE) or "n't" in body:
        raise QParseError("L_core word in the matrix interrogative clause (SEM-01)")
    return parse_matrix(body, st, ctx), st.k, st.fams, st.outer


def parse_decl(c: str, st: Q, ctx) -> list:
    if c.startswith("it is not the case that "):
        st.add("C2")
        return ["not", parse_decl(c[len("it is not the case that "):], st, ctx)]
    if c.startswith("it is false that "):
        st.add("C2")
        return ["not", parse_decl(c[len("it is false that "):], st, ctx)]
    for fn in ctx.get("decl_parsers", []):
        r = fn(c, st, ctx)
        if r is not None:
            return r
    r = decl_generic(c, st, ctx)
    if r is None:
        raise QParseError(f"cannot parse clause: {c[:80]!r}")
    return r


def _adj_word(w, st, ctx, negated=False):
    """An adjective: a declared affixed form is C6 (not <pos>)."""
    aff = ctx.get("affixed", {})
    if w in aff:
        st.add("C6")
        return ["not", ["adj", None, aff[w]]]
    return ["adj", None, w]


def _set_subj(lf, subj):
    if isinstance(lf, list):
        if lf and lf[0] == "adj" and lf[1] is None:
            return ["adj", subj, lf[2]]
        return [_set_subj(x, subj) for x in lf]
    return lf


MODALS = [("is not permitted to", "perm", True), ("is not required to", "req", True), ("does not have to", "req", True),
          ("is permitted to", "perm", False), ("is required to", "req", False), ("must not", "perm", True),
          ("may not", "perm", True), ("need not", "req", True), ("must", "req", False), ("may", "perm", False)]
BOUND_P = [("not less than", ">=", "C9"), ("not more than", "<=", "C9"), ("no fewer than", ">=", "C9"),
           ("no more than", "<=", "C9"), ("at least", ">=", None), ("more than", ">", None), ("over", ">", None),
           ("above", ">", None), ("at most", "<=", None), ("up to", "<=", None), ("less than", "<", None),
           ("fewer than", "<", None), ("under", "<", None), ("below", "<", None)]


def decl_generic(c, st, ctx):
    # deontic
    for ph, which, neg in MODALS:
        m = re.fullmatch(rf"the (.+?) {ph} ([a-z]+) (the .+)", c)
        if m:
            atom = ["deon", which, m.group(1), m.group(2), m.group(3)]
            if neg:
                st.add("C12")
                return ["not", atom]
            return atom
    # amount bound
    m = re.fullmatch(r"the (.+?) of (.+? [A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?) is (.+?) (\d+) (.+)", c)
    if m:
        for ph, op, fam in BOUND_P:
            if m.group(3) == ph:
                if fam:
                    st.add(fam)
                return ["amt", m.group(1), m.group(2), op, int(m.group(4))]
    m = re.fullmatch(r"the (.+?) of (.+? [A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?) is (\d+) (.+) or more", c)
    if m:
        return ["amt", m.group(1), m.group(2), ">=", int(m.group(3))]
    # connectives and decoys on adjectives of one subject
    m = re.fullmatch(r"(.+?) is not only ([a-z-]+) but also ([a-z-]+)", c)
    if m:
        st.fams.append("C16")
        return ["and", _set_subj(_adj_word(m.group(2), st, ctx), m.group(1)),
                _set_subj(_adj_word(m.group(3), st, ctx), m.group(1))]
    m = re.fullmatch(r"(.+?) is neither ([a-z-]+) nor ([a-z-]+)", c)
    if m:
        st.add("C13")
        s = m.group(1)
        return ["and", ["not", _set_subj(_adj_word(m.group(2), st, ctx), s)],
                ["not", _set_subj(_adj_word(m.group(3), st, ctx), s)]]
    m = re.fullmatch(r"(.+?) is not both ([a-z-]+) and ([a-z-]+)", c)
    if m:
        st.add("C13")
        s = m.group(1)
        return ["not", ["and", _set_subj(_adj_word(m.group(2), st, ctx), s),
                        _set_subj(_adj_word(m.group(3), st, ctx), s)]]
    m = re.fullmatch(r"(.+?) is ([a-z-]+) or ([a-z-]+)", c)
    if m:
        s = m.group(1)
        return ["or", _set_subj(_adj_word(m.group(2), st, ctx), s), _set_subj(_adj_word(m.group(3), st, ctx), s)]
    # possession
    m = re.fullmatch(r"(.+?) (has|does not have|lacks|is without|does not lack) a (.+)", c)
    if m:
        s, v, t = m.groups()
        atom = ["has", s, t]
        if v == "has":
            return atom
        if v == "does not have":
            st.add("C1")
            return ["not", atom]
        if v in ("lacks", "is without"):
            st.add("C5")
            return ["not", atom]
        st.add("C1")
        st.add("C5")
        return ["not", ["not", atom]]
    # plain adjective
    m = re.fullmatch(r"(.+?) is (not )?([a-z-]+)", c)
    if m:
        s, neg, w = m.groups()
        a = _set_subj(_adj_word(w, st, ctx), s)
        if neg:
            st.add("C1")
            return ["not", a]
        return a
    return None


def parse_matrix(body, st, ctx):
    for fn in ctx.get("matrix_parsers", []):
        r = fn(body, st, ctx)
        if r is not None:
            return r
    m = re.fullmatch(r"Is the (.+?) (permitted|required) to ([a-z]+) (the .+)", body)
    if m:
        return ["deon", "perm" if m.group(2) == "permitted" else "req", m.group(1), m.group(3), m.group(4)]
    m = re.fullmatch(r"Is the (.+?) of (.+? [A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?) (.+?) (\d+) (.+)", body)
    if m:
        for ph, op, fam in BOUND_P:
            if m.group(3) == ph and not fam:
                return ["amt", m.group(1), m.group(2), op, int(m.group(4))]
    m = re.fullmatch(r"Is the (.+?) of (.+? [A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?) (\d+) (.+) or more", body)
    if m:
        return ["amt", m.group(1), m.group(2), ">=", int(m.group(3))]
    m = re.fullmatch(r"Does (.+?) (have|lack) a (.+)", body)
    if m:
        atom = ["has", m.group(1), m.group(3)]
        if m.group(2) == "lack":
            st.add("C5")
            return ["not", atom]
        return atom
    m = re.fullmatch(r"Is (.+?) without a (.+)", body)
    if m:
        st.add("C5")
        return ["not", ["has", m.group(1), m.group(2)]]
    m = re.fullmatch(r"Is (.+?) ([a-z-]+) or ([a-z-]+)", body)
    if m:
        s = m.group(1)
        return ["or", _set_subj(_adj_word(m.group(2), st, ctx), s), _set_subj(_adj_word(m.group(3), st, ctx), s)]
    m = re.fullmatch(r"Is (.+?) ([a-z-]+)", body)
    if m:
        return _set_subj(_adj_word(m.group(2), st, ctx), m.group(1))
    raise QParseError(f"cannot parse matrix question: {body[:80]!r}")


# ---------------------------------------------------------------------------------------------------------------------
# S1 structure grammar

S1_HEAD_MODALS = ["is not permitted to", "is not required to", "does not have to", "is permitted to", "is required to",
                  "must not", "may not", "need not", "cannot", "must", "may"]
LIT_BOUNDS = ["at least", "more than", "over", "above", "at most", "up to", "less than", "under", "below",
              "no more than", "not less than", "not more than", "no fewer than", "fewer than"]
BOUND_OP = {"at least": ">=", "more than": ">", "over": ">", "above": ">", "at most": "<=", "up to": "<=",
            "less than": "<", "under": "<", "below": "<", "no more than": "<=", "not less than": ">=",
            "not more than": "<=", "no fewer than": ">=", "fewer than": "<"}


def s1_lit(t, noun, ctx):
    t = t.strip()
    m = re.fullmatch(rf"the (.+?) of the {re.escape(noun)} is (.+?) (\d+) (.+)", t)
    if m and m.group(2) in BOUND_OP:
        return {"t": "num", "q": m.group(1), "op": BOUND_OP[m.group(2)], "n": int(m.group(3))}
    m = re.fullmatch(rf"the (.+?) of the {re.escape(noun)} is (\d+) (.+) or more", t)
    if m:
        return {"t": "num", "q": m.group(1), "op": ">=", "n": int(m.group(2))}
    m = re.fullmatch(rf"the (.+?) of the {re.escape(noun)} is (not )?(.+)", t)
    if m:
        return {"t": "cat", "c": m.group(1), "v": m.group(3), "pol": "not" if m.group(2) else "pos"}
    m = re.fullmatch(rf"the {re.escape(noun)} (has|does not have|lacks) a (.+)", t)
    if m:
        return {"t": "has", "w": m.group(2), "pol": {"has": "pos", "does not have": "not", "lacks": "lacks"}[m.group(1)]}
    m = re.fullmatch(rf"the {re.escape(noun)} is (not )?([a-z-]+)", t)
    if m:
        w = m.group(2)
        if w in ctx["affixed"]:
            if m.group(1):
                raise ValueError("litotes in rule text")
            return {"t": "adj", "w": ctx["affixed"][w], "pol": "aff"}
        return {"t": "adj", "w": w, "pol": "not" if m.group(1) else "pos"}
    raise ValueError(f"S1 literal: {t!r}")


def s1_head(t, noun, ctx):
    t = t[0].lower() + t[1:]
    for md in S1_HEAD_MODALS:
        m = re.fullmatch(rf"the (.+?) {md} ([a-z]+) the {re.escape(noun)}", t)
        if m:
            return {"kind": "deon", "role": m.group(1), "modal": md, "verb": m.group(2)}
    m = re.fullmatch(rf"the {re.escape(noun)} is (not )?([a-z-]+)", t)
    if m:
        w = m.group(2)
        if w in ctx["affixed"]:
            return {"kind": "adj", "word": ctx["affixed"][w], "pol": "aff"}
        return {"kind": "adj", "word": w, "pol": "not" if m.group(1) else "pos"}
    raise ValueError(f"S1 head: {t!r}")


CELLS = ("required", "permitted", "forbidden")


def role_table(state, rows, noun):
    """Role and action table cells (role, verb, cell) in any container: table rows, delimited text lines (pipe, tab,
    comma, 2+ spaces) or key-value groups."""
    out = []
    act = re.compile(rf"([a-z]+) the {re.escape(noun)}")
    for r in rows:
        if len(r) == 3 and r[2] in CELLS:
            m = act.fullmatch(r[1])
            if m:
                out.append({"role": r[0], "verb": m.group(1), "cell": r[2]})
    if out:
        return out
    body = _strip_fence(state)
    for r in csv_rows(state):
        if len(r) == 3 and r[2].strip() in CELLS and act.fullmatch(r[1].strip()):
            out.append({"role": r[0].strip(), "verb": act.fullmatch(r[1].strip()).group(1), "cell": r[2].strip()})
    if out:
        return out
    line_re = re.compile(rf"^\W*(.+?)\s*(?:\||\t|\s{{2,}})\s*([a-z]+) the {re.escape(noun)}\s*(?:\||\t|\s{{2,}})\s*"
                         rf"(required|permitted|forbidden)\W*$")
    for ln in body.split("\n"):
        m = line_re.match(ln.strip())
        if m:
            out.append({"role": m.group(1), "verb": m.group(2), "cell": m.group(3)})
    if out:
        return out
    cur = {}
    for ln in body.split("\n"):
        m = re.match(r"^\s*(role|action|rule)\s*(?:=|:|\.{3,})\s*(.+?)\s*$", ln)
        if m:
            cur[m.group(1)] = m.group(2)
            if len(cur) == 3:
                a = act.fullmatch(cur["action"])
                if a and cur["rule"] in CELLS:
                    out.append({"role": cur["role"], "verb": a.group(1), "cell": cur["rule"]})
                cur = {}
    return out


def s1_parse(state: str, card_consts: dict):
    """Parsed S1 structure (rules, amount rule, role/action table, case facts) in the solver-B schema."""
    sents, rows = sentences(state)
    rules, facts, nums, cats, table, amount, attack, decoys = [], {}, {}, {}, [], None, [], []
    subj = None
    noun = None
    rule_txt = []
    # the case noun, read from the rule text ("the <noun> is / has / lacks", "of the <noun> is")
    case_noun = None
    for s in sents:
        mm = re.search(r"(?:\bIf |, then |^R\d+\. )?[Tt]he ([a-z][a-z -]*?) (?:is|has|does|lacks) ", s) \
            if re.match(r"R\d+\. ", s) else None
        if mm:
            cn = mm.group(1)
            if " of the " in cn:
                cn = cn.split(" of the ")[-1]
            case_noun = cn
            break
    for s in sents:
        if ATT.fullmatch(s):
            attack.append(s)
            continue
        m = re.fullmatch(r"R(\d+)\. (.+)\.", s)
        if m:
            rule_txt.append((int(m.group(1)), m.group(2)))
            continue
        m = None
        if case_noun:
            m = re.fullmatch(rf"The (.+) of ({re.escape(case_noun)} [A-Z]{{1,4}}-[A-Z0-9]+(?:-[A-Z0-9]+)?) is (.+)\.", s)
        if not m:
            m = re.fullmatch(r"The (.+?) of (.+? [A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?) is (.+)\.", s)
        if m:
            q, sj, val = m.groups()
            subj = sj
            mm = re.fullmatch(r"(\d+) (.+)", val)
            if val == "not recorded":
                if q in card_consts["value_sets"]:
                    cats[q] = "NR"
                else:
                    nums[q] = ("NR", None)
            elif mm and q not in card_consts["value_sets"]:
                nums[q] = (int(mm.group(1)), mm.group(2))
            else:
                cats[q] = val
            continue
        facts_line = s
        m = re.fullmatch(r"([A-Z][a-z][a-z -]*?) ([A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?) (.+)\.", facts_line)
        if m:
            subj = f"{m.group(1).lower()} {m.group(2)}"
            noun = m.group(1).lower()
            rest = m.group(3)
            mm = re.fullmatch(r"is not only ([a-z-]+) but also ([a-z-]+)", rest)
            if mm:
                for w in mm.groups():
                    facts[("adj", w)] = "pos"
                decoys.append(mm.groups())
                continue
            mm = re.fullmatch(r"(has|does not have|lacks) a (.+)", rest)
            if mm:
                facts[("has", mm.group(2))] = {"has": "pos", "does not have": "not", "lacks": "lacks"}[mm.group(1)]
                continue
            mm = re.fullmatch(r"is (not )?([a-z-]+)", rest)
            if mm:
                w = mm.group(2)
                if w in card_consts["affixed"]:
                    facts[("adj", card_consts["affixed"][w])] = "aff"
                else:
                    facts[("adj", w)] = "not" if mm.group(1) else "pos"
                continue
            raise ValueError(f"S1 fact: {s!r}")
    if noun is None and subj:
        noun = subj.rsplit(" ", 1)[0]
    if noun:
        table = role_table(state, rows, noun)
    for i, body in sorted(rule_txt):
        rid = f"R{i}"
        m = re.fullmatch(rf"The (.+?) of the {re.escape(noun)} is the (.+?) of the {re.escape(noun)}, but "
                         rf"(at most|no more than|not more than|up to|at least|not less than) (\d+) (.+)", body)
        if m:
            amount = {"rid": rid, "name": m.group(1), "qty": m.group(2),
                      "kind": "cap" if m.group(3) in ("at most", "no more than", "not more than", "up to") else "floor",
                      "limit": int(m.group(4))}
            continue
        m = re.fullmatch(r"If (.+?), then (.+?)(?:, except when (.+)| unless (.+))?", body)
        if m:
            conds = [s1_lit(x, noun, card_consts) for x in m.group(1).split(" and ")]
            exc = m.group(3) or m.group(4)
            rules.append({"id": rid, "form": "if", "conds": conds, "exc": s1_lit(exc, noun, card_consts) if exc else None,
                          "exc_kw": "except when" if m.group(3) else ("unless" if m.group(4) else None),
                          "head": s1_head(m.group(2), noun, card_consts)})
            continue
        m = re.fullmatch(r"(.+?) only if (.+)", body)
        if m:
            rules.append({"id": rid, "form": "onlyif", "conds": [s1_lit(m.group(2), noun, card_consts)], "exc": None,
                          "exc_kw": None, "head": s1_head(m.group(1), noun, card_consts)})
            continue
        m = re.fullmatch(r"(.+?) unless (.+)", body)
        if m:
            rules.append({"id": rid, "form": "unless", "conds": [s1_lit(m.group(2), noun, card_consts)], "exc": None,
                          "exc_kw": None, "head": s1_head(m.group(1), noun, card_consts)})
            continue
        m = re.fullmatch(r"(.+?)(?:, except when (.+))?", body)
        rules.append({"id": rid, "form": "uncond", "conds": [],
                      "exc": s1_lit(m.group(2), noun, card_consts) if m.group(2) else None,
                      "exc_kw": "except when" if m.group(2) else None, "head": s1_head(m.group(1), noun, card_consts)})
    return {"subj": subj, "noun": noun, "rules": rules, "facts": facts, "nums": nums, "cats": cats, "table": table,
            "amount": amount, "attack": attack, "decoys": decoys, "world": card_consts["world"],
            "value_sets": card_consts["value_sets"], "affixed": card_consts["affixed"]}
