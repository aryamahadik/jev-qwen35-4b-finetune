"""F11 card and item parsers (G0 section 7), written from the grammar and the section-10 statements.

Independence (G0 section 3): imports only the frozen lexicon (lex), the shared tokenizer and paths (common) and the
shared negcount. Nothing from the generator, renderer or solver A. Every parse failure raises ParseError.
"""
from __future__ import annotations

import common  # noqa: F401 (sys.path)

import datetime as dt
import re
from fractions import Fraction

import lex
import negcount
from common import toks, find_runs

DESIG_RE = re.compile(r"\b[A-Z]{2,3}-\d{3,5}\b")
SUBJ_RE = re.compile(r"^(?:" + "|".join(lex.SUBJECT_LABELS) + r"): ([A-Z]{2,3}-\d{3,5})\.?$")
NUM_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.]|\.\d)")
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
HEADINGS = {"reading rules", "glossary", "codes", "notes", "examples"}
ID_RE = r"[A-Z][A-Z0-9]{1,4}"


def _fewshot_patterns():
    """Worked-item block patterns from the public formats-1 few-shot template pool (block-case templates)."""
    import json
    from common import FMT1
    out, heads = [], set()
    for ln in open(FMT1 / "data" / "fewshot_templates.jsonl", encoding="utf-8"):
        d = json.loads(ln)
        if d.get("header"):
            heads.add(d["header"].casefold())
        if "json_keys" in d or d.get("case") != "block" or d.get("needs_note") or d.get("table_head"):
            continue
        pat = re.escape(d["item"])
        pat = pat.replace(r"\{i\}", r"(?P<i>\d+)").replace(r"\{case\}", r"(?P<case>[^\n]+)")
        pat = pat.replace(r"\{answer\}", "(?P<ans>" + ID_RE + ")")
        out.append((d["id"], re.compile("^" + pat + "$", re.M)))
    return out, heads


FEWSHOT, FEWSHOT_HEADS = _fewshot_patterns()
HEADINGS = HEADINGS | FEWSHOT_HEADS


def extract_worked(text: str):
    """Remove the worked-item block (if any) from a card text; returns (rest, [(answer ID, case text)])."""
    if not text:
        return text, []
    lines = []
    for ln in text.split("\n"):
        if ln.startswith("> "):
            ln = ln[2:]
        elif ln.strip() == ">":
            ln = ""
        lines.append(ln.strip())
    t = "\n".join(lines)
    found = [(tid, ms) for tid, rx in FEWSHOT for ms in [list(rx.finditer(t))] if ms]
    if not found:
        return text, []
    if len(found) > 1:
        raise ParseError("ambiguous worked-item block")
    tid, ms = found[0]
    if not 1 <= len(ms) <= 3:
        raise ParseError("worked-item count out of range")
    idx = [int(m.group("i")) for m in ms if "i" in m.groupdict() and m.group("i") is not None]
    if idx and idx != list(range(1, len(ms) + 1)):
        raise ParseError("worked items out of order")
    for m in reversed(ms):
        t = t[:m.start()] + t[m.end():]
    return t, [(m.group("ans"), m.group("case")) for m in ms]


class ParseError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ line chrome
def _heading_key(s: str) -> str:
    x = s.strip()
    x = re.sub(r"^#+\s*", "", x)
    x = re.sub(r"^\d+\.\s+", "", x)
    x = x.strip("*[]<>/: ").replace("_", " ")
    return x.casefold()


def norm_lines(text: str, extra_headings=()) -> list[str]:
    out = []
    heads = HEADINGS | {h.casefold() for h in extra_headings}
    for ln in (text or "").split("\n"):
        s = ln
        if s.startswith("> "):
            s = s[2:]
        elif s.strip() == ">":
            continue
        s = s.strip()
        if not s:
            continue
        if re.fullmatch(r"[=\-~^+: ]+", s) and not re.search(r"\w", s):
            continue
        if re.fullmatch(r"</?[a-z0-9_]+>", s):
            continue
        if _heading_key(s) in heads:
            continue
        s = re.sub(r"^(?:[-*•+·]) ", "", s)
        out.append(s)
    return out


# ------------------------------------------------------------------------------------------------ card
class PCard:
    def __init__(self):
        self.attrs = []            # [{'name', 'kind', 'values': [..], 'terms': {value: [..]}, 'aterms': [..], 'unit'}]
        self.codes = {}            # id -> {'name', 'parts': [cond], 'rule', 'mark'}
        self.notes = []            # (a, b, winner)
        self.default = None        # (attr name, value)
        self.shape = None          # box | group | list | key | short | table
        self.entries = []          # S6: [(conds, id)], catch
        self.catch = None
        self.groups = []           # S3: [{'name', 'vals', 'leaves': [ids], 'residual': id, 'mark'}]
        self.scope = []            # (src, dst, cond)
        self.couplets = {}         # S5
        self.gnames = {}           # S5: couplet n -> group name
        self.short_attrs = None
        self.short_names = []
        self.hedges = []
        self.cues = []
        self.examples = []         # (id, report text)
        self.worked = []           # (answer id, case text): few-shot worked items
        self.marks = set()
        self.fields = {}           # S4: attr name -> field name (SEM-50 field lines)
        self.dimension = None      # S7 (SEM-45)
        self.s7_target = None      # S7 MAMS: 'aspect' | 'target'
        self.s7_short = []         # S7 short cards: [(name, mark)]
        self.s7key = False         # S5 codebook arm: codebook written as a key (couplets over the label set)

    def attr(self, name):
        for a in self.attrs:
            if a["name"] == name:
                return a
        raise ParseError(f"unknown attribute {name!r}")


def _quoted(s: str) -> list[str]:
    return re.findall(r"'([^']+)'", s)


def parse_glossary_line(pc: PCard, s: str) -> bool:
    m = re.match(r"^" + re.escape(lex.GLOSSARY_LEAD) + r" (.+?): (.+)\.$", s)
    if m:
        a = {"name": m.group(1), "kind": "nom", "values": [], "terms": {}}
        for part in m.group(2).split("; "):
            mm = re.match(r"^(.+?) \(shown by (.+)\)$", part)
            if not mm:
                raise ParseError("glossary value")
            a["values"].append(mm.group(1))
            a["terms"][mm.group(1)] = _quoted(mm.group(2))
        pc.attrs.append(a)
        return True
    m = re.match(r"^(.+?) \(shown by (.+?)\): present or absent\.$", s)
    if m:
        pc.attrs.append({"name": m.group(1), "kind": "pres", "values": ["present", "absent"],
                         "aterms": _quoted(m.group(2))})
        return True
    m = re.match(r"^(.+?) \(shown by (.+?)\) in (\S+)/(\S+)\.$", s)
    if m:
        pc.attrs.append({"name": m.group(1), "kind": "num", "aterms": _quoted(m.group(2)),
                         "unit": (m.group(3), m.group(4))})
        return True
    m = re.match(r"^(.+?) \(shown by (.+?)\) is the date of the (.+)\.$", s)
    if m:
        pc.attrs.append({"name": m.group(1), "kind": "date", "aterms": _quoted(m.group(2)), "event": m.group(3)})
        return True
    return False


BANNED_CMP = ("at most", "no more than", "more than", "over", "up to", "between", "after", "on or before", "by",
              "until", "since", "through", "within", "only", "exactly", "none of")


def parse_cond(pc: PCard, s: str):
    """One COND -> (attr name, op, arg). ops: in (set of values), pres, abs, ge, lt (Fraction or date)."""
    names = sorted((a["name"] for a in pc.attrs), key=len, reverse=True)
    for nm in names:
        if not s.startswith(nm + " "):
            continue
        rest = s[len(nm) + 1:]
        a = pc.attr(nm)
        if a["kind"] == "nom":
            if rest.startswith("is one of "):
                vals = rest[len("is one of "):].split(", ")
            elif rest.startswith("is "):
                vals = [rest[3:]]
            else:
                raise ParseError(f"nominal cond {s!r}")
            if any(v not in a["values"] for v in vals):
                raise ParseError(f"unknown value in {s!r}")
            return (nm, "in", frozenset(vals))
        if a["kind"] == "pres":
            if rest in ("present", "absent"):
                return (nm, "pres" if rest == "present" else "abs", None)
            raise ParseError(f"presence cond {s!r}")
        if a["kind"] == "num":
            for w in lex.CMP_GE + lex.CMP_LT:
                if rest.startswith(w + " "):
                    tail = rest[len(w) + 1:]
                    m = re.fullmatch(r"(\d+(?:\.\d+)?) (\S+)", tail)
                    if not m or m.group(2) not in a["unit"]:
                        raise ParseError(f"numeric cond {s!r}")
                    # longest match: 'no fewer than' before 'fewer than'
                    op = "ge" if w in lex.CMP_GE else "lt"
                    return (nm, op, Fraction(m.group(1)))
            raise ParseError(f"numeric cond {s!r}")
        if a["kind"] == "date":
            for w, op in ((lex.DCMP_GE, "ge"), (lex.DCMP_LT, "lt")):
                if rest.startswith(w + " "):
                    return (nm, op, dt.date.fromisoformat(rest[len(w) + 1:]))
            raise ParseError(f"date cond {s!r}")
    raise ParseError(f"no attribute in cond {s!r}")


def lint_cond_span(s: str, pc=None):
    if pc is not None:
        for a in sorted(pc.attrs, key=lambda a: -len(a["name"])):
            s = s.replace(a["name"], "_")
    low = " " + s.casefold() + " "
    for ok in ("on or after", "no fewer than", "fewer than", "is one of", "only if", "use only when"):
        low = low.replace(" " + ok + " ", " _ ")
    for b in BANNED_CMP:
        if " " + b + " " in low:
            raise ParseError(f"banned comparator {b!r} in condition span")


def parse_parts(pc, s):
    out = []
    for p in s.split("; "):
        lint_cond_span(p, pc)
        out.append(parse_cond(pc, p))
    return out


def parse_s7_sets(pc: PCard, body: str):
    """S7 definitions (SEM-46): XED 'the labels are X alone, or X and Y.'; MAMS 'the named T is P; the other Ts are
    P1 and P2.' sets joined by ' Or: '."""
    def lst(x):
        x = x.strip()
        parts = re.split(r", | and ", x)
        if any(not re.fullmatch(r"[a-z]+", p) for p in parts) or len(parts) != len(set(parts)):
            raise ParseError(f"label list {x!r}")
        return frozenset(parts)
    if pc.s7_target is None:
        m = re.fullmatch(r"the labels are (.+)\.", body)
        if not m:
            raise ParseError("S7 definition")
        out = []
        for alt in m.group(1).split(", or "):
            mm = re.fullmatch(r"([a-z]+) alone", alt)
            out.append(frozenset([mm.group(1)]) if mm else lst(alt))
            if not mm and len(out[-1]) < 2:
                raise ParseError("single label without 'alone'")
        return out
    t, ts = pc.s7_target
    out = []
    for alt in body.split(" Or: "):
        m = re.fullmatch(r"the named " + t + r" is ([a-z]+); the other " + ts + r" are (.+)\.", alt)
        if not m:
            raise ParseError("S7 MAMS definition")
        out.append((m.group(1), lst(m.group(2))))
    return out


def parse_s7_cond(pc: PCard, s: str):
    """S5 codebook-arm couplet condition (SEM-18 / SEM-19 forms) -> (kind, labels)."""
    def lst(x, sep):
        out = tuple(re.split(r", | " + sep + " ", x))
        if not all(re.fullmatch(r"[a-z]+", y) for y in out) or len(set(out)) != len(out):
            raise ParseError("key condition labels")
        return out
    m = re.fullmatch(r"the labels include (any|all) of (.+)", s)
    if m and pc.s7_target is None:
        return (m.group(1), lst(m.group(2), "or" if m.group(1) == "any" else "and"))
    if pc.s7_target:
        t, ts = pc.s7_target
        m = re.fullmatch(r"the named " + re.escape(t) + r" is one of (.+)", s)
        if m:
            return ("is", lst(m.group(1), "or"))
        m = re.fullmatch(r"the named " + re.escape(t) + r" is ([a-z]+)", s)
        if m:
            return ("is", (m.group(1),))
        m = re.fullmatch(r"the labels of the other " + re.escape(ts) + r" include (any|all) of (.+)", s)
        if m:
            return (m.group(1), lst(m.group(2), "or" if m.group(1) == "any" else "and"))
    raise ParseError("key condition form")


def parse_s7_name(pc: PCard, name: str):
    """Short S7 card names give the full label set (XED 'Anger / Disgust'; MAMS 'named P with others P1 and P2')."""
    if pc.s7_target is None:
        parts = [x.strip().lower() for x in name.split(" / ")]
        if any(not re.fullmatch(r"[a-z]+", x) for x in parts):
            raise ParseError("short S7 name")
        return frozenset(parts)
    m = re.fullmatch(r"named ([a-z]+) with others (.+)", name)
    if not m:
        raise ParseError("short S7 MAMS name")
    return (m.group(1), frozenset(re.split(r", | and ", m.group(2))))


def parse_body(pc: PCard, cid: str, body: str) -> dict:
    mark = None
    m = re.search(r" \[(\w+)\]$", body)
    if m:
        mark = m.group(1)
        body = body[:m.start()]
    if pc.shape == "s7":
        return {"sets": parse_s7_sets(pc, body), "rule": None, "mark": mark, "parts": []}
    m = re.fullmatch(r"(.+?), unless (.+?)\. If both (.+) and (.+) hold, use (" + ID_RE + r")\.", body)
    if m:
        if m.group(3) != m.group(1) or m.group(4) != m.group(2):
            raise ParseError("unless sentence mismatch")
        return {"parts": parse_parts(pc, m.group(1)), "rule": ("unless", parse_cond(pc, m.group(2)), m.group(5)),
                "mark": mark}
    m = re.fullmatch(r"(.+?)\. Use (" + ID_RE + r") only if (.+?) also holds\. If (.+) holds but (.+) does not, use (" +
                     ID_RE + r")\.", body)
    if m:
        if m.group(2) != cid or m.group(4) != m.group(1) or m.group(5) != m.group(3):
            raise ParseError("only-if sentence mismatch")
        return {"parts": parse_parts(pc, m.group(1)), "rule": ("onlyif", parse_cond(pc, m.group(3)), m.group(6)),
                "mark": mark}
    return {"parts": parse_parts(pc, body), "rule": None, "mark": mark}


ENTRY_SEPS = (": ", " = ", " | ")


def split_entry(s: str):
    """'<head><sep><body>' for the one-line defs variants; head = 'ID NAME' | 'ID' | option text."""
    best = None
    for sep in ENTRY_SEPS:
        i = s.find(sep)
        if i > 0 and (best is None or i < best[0]):
            best = (i, sep)
    if best is None:
        return None
    return s[:best[0]], s[best[0] + len(best[1]):]


def parse_card(card_text: str | None, instr_text: str | None, options: list[str] | None, *,
               qtype: str, question_block: list[str] = ()) -> PCard:
    """Yes/no rows: card_text is the whole card. Choice rows: instr_text holds the moved card block (wording,
    question and row-level statements removed by the caller via question_block) and card_text the option lines."""
    pc = PCard()
    lines = []
    if qtype == "noul":
        src, pc.worked = extract_worked(card_text)
        lines = norm_lines(src)
    else:
        src = instr_text or ""
        for q in question_block:
            if q:
                src = src.replace(q, "\n")
        src, pc.worked = extract_worked(src)
        lines = norm_lines(src)
    # pass 1: glossary + reading rules (attributes first)
    rest = []
    short_mode = False
    for s in lines:
        if parse_glossary_line(pc, s):
            continue
        m = re.match(lex.FIELD_RE, s)
        if m:
            pc.fields[m.group(1)] = m.group(2)
            continue
        m = re.match(r"^Names give (.+) in that order\.$", s)
        if m:
            short_mode = True
            pc.shape = "short"
            pc.short_attrs = m.group(1).split(", ")
            continue
        rest.append(s)
    for s in rest:
        m = re.match(r"^Codes describe how human annotators judged the quoted text on (.+?)\. Code only the quoted "
                     r"text\.$", s)
        if m:
            pc.shape = "s7"
            pc.dimension = m.group(1)
        m = re.match(r"^The key's conditions describe how human annotators judged the quoted text on (.+?)\. Code "
                     r"only the quoted text\.$", s)
        if m:
            pc.shape = "s7"
            pc.s7key = True
            pc.dimension = m.group(1)
        m = re.match(r"^The question names one (\w+)\. Codes describe the opinion about it and the opinions about "
                     r"the other (\w+) in the sentence\.$", s)
        if m:
            pc.s7_target = (m.group(1), m.group(2))
        if s.startswith("Read each sentence on its own"):
            m = re.search(r"hedged \(([^)]*)\)", s)
            if m:
                pc.hedges = _quoted(m.group(1))
        if s.startswith("For present-or-absent items,"):
            m = re.match(r"^For present-or-absent items, (.+?) mean absent\.", s)
            pc.cues = _quoted(m.group(1)) if m else []
    known_rules = [lex.SEM[k].split("{")[0][:40] for k in lex.SEM] + ["Names give"]
    opt_lines = []
    if qtype == "choice" and card_text:
        for ln in card_text.split("\n"):
            if ln.startswith("- ") and ": " in ln:
                opt_lines.append(ln[2:])
    table_rows, table_head = [], None
    cur_group = None
    for s in rest:
        m = re.match(r"^If both (" + ID_RE + r") and (" + ID_RE + r") fit, use (" + ID_RE + r")\.$", s)
        if m:
            pc.notes.append((m.group(1), m.group(2), m.group(3)))
            continue
        m = re.match(r"^If the (.+?) does not say (.+?), treat (.+?) as (.+?)\. A sentence that shows nothing does not "
                     r"count as saying (.+?)\.", s)
        if m:
            if m.group(2) != m.group(3) or m.group(2) != m.group(5):
                raise ParseError("missing rule names two attributes")
            pc.default = (m.group(2), m.group(4))
            continue
        if any(s.startswith(k) for k in known_rules if k):
            continue
        m = re.match(r"^Example of (" + ID_RE + r"): (.+)$", s)
        if m:
            pc.examples.append((m.group(1), m.group(2)))
            continue
        m = re.match(r"^Marked \[(\w+)\]: (.+)\.$", s)
        if m:
            for x in m.group(2).split(", "):
                pc.marks.add(x)
            continue
        if short_mode:
            m = re.match(r"^(.+?)(?: \[(\w+)\])?$", s)
            pc.short_names.append((m.group(1), m.group(2)))
            continue
        # S3 group heading / scope note / residual
        m = re.match(r"^Group (.+?) \((.+?): (.+?)\)(?: \[(\w+)\])?$", s)
        if m:
            pc.shape = "group"
            cur_group = {"name": m.group(1), "gattr": m.group(2), "vals": m.group(3).split(", "),
                         "leaves": [], "residual": None, "mark": m.group(4)}
            pc.groups.append(cur_group)
            continue
        m = re.match(r"^Reports that would be in (.+?) but meet (.+?) belong to (.+?) instead\.$", s)
        if m:
            lint_cond_span(m.group(2), pc)
            pc.scope.append((m.group(1), m.group(3), parse_cond(pc, m.group(2))))
            continue
        m = re.match(r"^(" + ID_RE + r")(?: (.+?))?: use only when the (.+?) belongs to (.+?) and no other (.+?) code "
                     r"fits\.$", s)
        if m:
            if cur_group is None or m.group(4) != cur_group["name"] or m.group(5) != cur_group["name"]:
                raise ParseError("residual outside its group")
            cur_group["residual"] = m.group(1)
            pc.codes[m.group(1)] = {"name": m.group(2), "parts": [], "rule": None, "mark": cur_group["mark"],
                                    "residual": cur_group["name"]}
            continue
        # S6 entries
        m = re.match(r"^(?:\d+\. |Rule \d+: |\(\d+\) |R\d+\. )?If (.+) -> (" + ID_RE + r")$", s)
        if m:
            pc.shape = "list"
            pc.entries.append((parse_parts(pc, m.group(1)), m.group(2)))
            continue
        m = re.match(r"^(?:\d+\. |Rule \d+: |\(\d+\) |R\d+\. )?Otherwise -> (" + ID_RE + r")$", s)
        if m:
            pc.catch = m.group(1)
            continue
        # S5 codebook arm: key couplets over the annotators' labels
        if pc.s7key:
            m = re.match(r"^(\d+)a (.+) -> (\S+)$", s)
            if m:
                pc.couplets.setdefault(int(m.group(1)), {})["a"] = (parse_s7_cond(pc, m.group(2)), m.group(3))
                continue
            m = re.match(r"^(\d+)b otherwise -> (\S+)$", s)
            if m:
                pc.couplets.setdefault(int(m.group(1)), {})["b"] = m.group(2)
                continue
        # S5 key
        m = re.match(r"^(\d+)\. (.+)$", s)
        if m and pc.shape == "key" or (m and re.match(r"^\d+a ", "")):
            pc.gnames[int(m.group(1))] = m.group(2)
            continue
        m = re.match(r"^(\d+)a (.+) -> (\S+)$", s)
        if m:
            pc.shape = "key"
            lint_cond_span(m.group(2), pc)
            pc.couplets.setdefault(int(m.group(1)), {})["a"] = (parse_cond(pc, m.group(2)), m.group(3))
            continue
        m = re.match(r"^(\d+)b otherwise -> (\S+)$", s)
        if m:
            pc.couplets.setdefault(int(m.group(1)), {})["b"] = m.group(2)
            continue
        # tables
        if table_head is None and re.match(r"^\|?\s*Code\s*(\||  )", s):
            table_head = [c.strip() for c in re.split(r"\s*\|\s*|\s{2,}", s.strip().strip("|")) if c.strip()]
            pc.shape = "table"
            continue
        if table_head is not None and (s.startswith("|") or " | " in s or re.search(r"\S {2,}\S", s)):
            if re.fullmatch(r"[|\-: ]+", s):
                continue
            cells = [c.strip() for c in re.split(r" \| |\s{2,}", s.strip().strip("|").strip())]
            if len(cells) == len(table_head):
                table_rows.append(cells)
                continue
        # legends (S6 / S5): 'ID: Name [mark]'
        m = re.match(r"^(" + ID_RE + r"): ([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)*)(?: \[(\w+)\])?$", s)
        if m and (pc.shape in ("list", "key") or pc.s7key):
            pc.codes.setdefault(m.group(1), {"parts": [], "rule": None})
            pc.codes[m.group(1)].update({"name": m.group(2), "mark": m.group(3)})
            continue
        m = re.match(r"^(" + ID_RE + r")(?: \[(\w+)\])?$", s)
        if m and (pc.shape in ("list", "key") or pc.s7key):
            continue
        if pc.shape == "s7" and split_entry(s) is None:
            m = re.match(r"^(.+?)(?: \[(\w+)\])?$", s)
            pc.s7_short.append((m.group(1), m.group(2)))
            continue
        # code entry (one-line list, S3 leaves, table rule sentences)
        sp = split_entry(s)
        if sp:
            head, body = sp
            hm = re.fullmatch(r"(" + ID_RE + r")(?: (.+))?", head)
            if hm:
                cid = hm.group(1)
                d = parse_body(pc, cid, body)
                if table_head is not None and cid in pc.codes:
                    pc.codes[cid]["rule"] = d["rule"]
                    continue
                d["name"] = hm.group(2)
                pc.codes[cid] = d
                if cur_group is not None:
                    cur_group["leaves"].append(cid)
                    d["mark"] = cur_group["mark"]
                if pc.shape is None:
                    pc.shape = "box"
                continue
        raise ParseError(f"unparsed card line: {s[:60]!r}")
    # option lines (choice rows of one-line cards): '<option>: (<other>) <body>'
    for ol in opt_lines:
        opt, body = ol.split(": ", 1)
        m = re.match(r"^\((.+?)\) (.+)$", body)
        other = None
        if m:
            other, body = m.group(1), m.group(2)
        if re.fullmatch(ID_RE, opt) and (other is None or not re.fullmatch(ID_RE, other)):
            cid, name = opt, other
        elif other is not None and re.fullmatch(ID_RE, other):
            cid, name = other, opt
        else:
            raise ParseError("option line without an ID")
        d = parse_body(pc, cid, body)
        d["name"] = name
        d["option"] = opt
        if cid in pc.codes:
            raise ParseError("code listed twice")
        pc.codes[cid] = d
        if pc.shape is None:
            pc.shape = "box"
    if table_head is not None:
        an = table_head[2:] if len(table_head) > 1 and table_head[1] == "Name" else table_head[1:]
        has_name = len(table_head) > 1 and table_head[1] == "Name"
        for row in table_rows:
            cid = row[0]
            name = row[1] if has_name else None
            parts = []
            for nm, cell in zip(an, row[2 if has_name else 1:]):
                parts += parse_cell(pc, nm, cell)
            old = pc.codes.get(cid, {})
            pc.codes[cid] = {"name": name, "parts": parts, "rule": old.get("rule"),
                             "mark": "m" if cid in pc.marks else None}
        pc.shape = "box"
    for cid in pc.marks:
        if cid in pc.codes:
            pc.codes[cid]["mark"] = pc.codes[cid].get("mark") or "m"
    if pc.shape == "list" and pc.catch is None:
        raise ParseError("decision list without its catch-all")
    if pc.shape == "list":
        for _, cid in pc.entries + [(None, pc.catch)]:
            pc.codes.setdefault(cid, {"parts": [], "rule": None, "name": None, "mark": None})
    if pc.shape == "key":
        for cp in pc.couplets.values():
            for x in (cp["a"][1], cp["b"]):
                if not x.isdigit():
                    pc.codes.setdefault(x, {"parts": [], "rule": None, "name": None, "mark": None})
    if pc.shape == "short":
        if not pc.short_attrs:
            raise ParseError("short card without its name order")
        for j, an in enumerate(pc.short_attrs):
            vals = []
            for nm, _ in pc.short_names:
                parts = nm.split(" / ")
                if len(parts) != len(pc.short_attrs):
                    raise ParseError("short name does not give every attribute")
                if parts[j] not in vals:
                    vals.append(parts[j])
            pc.attrs.append({"name": an, "kind": "nom", "values": vals, "terms": {}})
    return pc


def parse_cell(pc, nm, cell):
    a = pc.attr(nm)
    if cell == "any":
        return []
    if a["kind"] == "nom":
        vals = cell.split(", ")
        if any(v not in a["values"] for v in vals):
            raise ParseError("table value")
        return [(nm, "in", frozenset(vals))]
    if a["kind"] == "pres":
        return [(nm, "pres" if cell == "present" else "abs", None)]
    if a["kind"] == "num":
        # a contiguous band list -> lower and upper thresholds
        bands = cell.split(", ")
        lo, hi = None, None
        for j, b in enumerate(bands):
            m = re.fullmatch(r"under (\S+) \S+", b)
            m2 = re.fullmatch(r"(\S+) \S+ or more", b)
            m3 = re.fullmatch(r"(\S+) to under (\S+) \S+", b)
            if m:
                blo, bhi = None, Fraction(m.group(1))
            elif m2:
                blo, bhi = Fraction(m2.group(1)), None
            elif m3:
                blo, bhi = Fraction(m3.group(1)), Fraction(m3.group(2))
            else:
                raise ParseError("band cell")
            if j == 0:
                lo = blo
            hi = bhi
        out = []
        if lo is not None:
            out.append((nm, "ge", lo))
        if hi is not None:
            out.append((nm, "lt", hi))
        return out
    out = []
    for p in cell.split("; "):
        if p.startswith(lex.DCMP_GE + " "):
            out.append((nm, "ge", dt.date.fromisoformat(p[len(lex.DCMP_GE) + 1:])))
        elif p.startswith(lex.DCMP_LT + " "):
            out.append((nm, "lt", dt.date.fromisoformat(p[len(lex.DCMP_LT) + 1:])))
        else:
            raise ParseError("date cell")
    return out


# ------------------------------------------------------------------------------------------------ items
def split_sentences(text: str) -> list[str]:
    out = []
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("> "):
            s = s[2:]
        s = re.sub(r"^(?:\d+\. |[-*•+·] |\d+\) |Step \d+: )", "", s).strip()
        if not s:
            continue
        parts = re.split(r"(?<=[.?!])\s+", s)
        out += [p.strip() for p in parts if p.strip()]
    return out


class PItem:
    def __init__(self):
        self.desig = None
        self.vec = {}          # attr name -> value (nom: value name; pres: 'present'/'absent'; num: Fraction; date)
        self.frames = []       # (kind, attr name, value)
        self.inert = 0
        self.attacks = 0
        self.stated = set()


def value_index(pc: PCard):
    """[(token run, attr name, value or None, role)] longest first; role: 'val' (nominal value word), 'pterm'
    (presence term), 'aname' (numeric / date attribute name or term)."""
    idx = []
    for a in pc.attrs:
        if a["kind"] == "nom":
            for v in a["values"]:
                idx.append((toks(v), a["name"], v, "val"))
                for t in a["terms"].get(v, []):
                    idx.append((toks(t), a["name"], v, "val"))
        elif a["kind"] == "pres":
            for t in a["aterms"]:
                idx.append((toks(t), a["name"], None, "pterm"))
        else:
            for t in [a["name"]] + a["aterms"]:
                idx.append((toks(t), a["name"], None, "aname"))
    idx.sort(key=lambda x: -len(x[0]))
    return idx


def find_value_words(T, idx):
    used = [False] * len(T)
    hits = []
    for run, an, v, role in idx:
        for i in find_runs(T, run):
            if any(used[i:i + len(run)]):
                continue
            for j in range(i, i + len(run)):
                used[j] = True
            hits.append((i, an, v, role))
    hits.sort()
    return hits


def _has(low: str, phrases) -> bool:
    return any(re.search(r"(?<![a-z])" + re.escape(p) + r"(?![a-z])", low) for p in phrases)


def classify(s: str, focal: str, pc: PCard, hits) -> str:
    low = s.casefold()
    if _has(low, lex.ATTACK_MARKERS):
        return "ATTACK"
    if not hits:
        return "INERT"
    if _has(low, lex.BANNED_LATER_FINDING) or _has(low, lex.BANNED_PREP_ATTRIB) or _has(low, lex.BANNED_HABITUAL):
        raise ParseError("banned form in a value-word sentence")
    if _has(low, lex.NOT_STATED):
        raise ParseError("value word with a not-stated phrase")
    if low.startswith(tuple(m + " " for m in lex.GENERIC_MARKERS)):
        return "GENERIC"
    ds = DESIG_RE.findall(s)
    if len(set(ds)) != 1:
        raise ParseError("value-word sentence without exactly one subject")
    if ds[0] != focal:
        return "OTHER"
    if _has(low, lex.PRIOR_MARKERS):
        return "PRIOR"
    if _has(low, lex.LATER_MARKERS):
        return "LATER"
    if _has(low, lex.HYPO_MARKERS):
        return "HYPO"
    hedge = list(lex.HEDGE_VERBS) + list(lex.HEDGE_ADVERBS) + list(lex.HEDGE_MODALS)
    if _has(low, hedge):
        used = [h for h in lex.HEDGE_VERBS if _has(low, [h])]
        if any(h not in pc.hedges for h in used):
            raise ParseError("hedge marker not quoted on the card")
        return "HEDGED"
    T = [t for t in toks(s)]
    anaph = set(lex.ANAPHORS)
    lowx = low
    for f in lex.ATTRIB_PASSIVE:
        lowx = lowx.replace(f, " ")
    for v in lex.ATTRIB_ACTIVE + tuple(h + " that" for h in lex.HEDGE_VERBS):
        lowx = lowx.replace(v, " ")
    if set(toks(lowx)) & anaph:
        raise ParseError("anaphor in a value-word sentence")
    if not any(h[3] == "pterm" for h in hits) and negcount.count(s).k_all >= 1:
        return "NEG"
    return "FOCAL"


def parse_report(text: str, pc: PCard, *, inline=False) -> PItem:
    """One program report: subject line, then sentences."""
    it = PItem()
    if inline:
        sents = re.split(r"(?<=[.?!])\s+", text.strip())
    else:
        sents = split_sentences(text)
    k0 = None
    for i, s in enumerate(sents):
        m = SUBJ_RE.match(s)
        if m:
            k0 = i
            it.desig = m.group(1)
            break
    if k0 is None:
        raise ParseError("report without a subject line")
    for s in sents[:k0]:
        if DESIG_RE.search(s) or find_value_words(toks(s), value_index(pc)):
            raise ParseError("text before the subject line names an entity or a value")
    idx = value_index(pc)
    attrs = {a["name"]: a for a in pc.attrs}
    for s in sents[k0 + 1:]:
        T = toks(s)
        hits = find_value_words(T, idx)
        if any(t in ("present", "absent") for t in T):
            raise ParseError("'present' / 'absent' in report text")
        kind = classify(s, it.desig, pc, hits)
        if kind == "ATTACK":
            it.attacks += 1
            continue
        if kind == "INERT":
            for f in (lex.PRIOR_MARKERS + lex.LATER_MARKERS + lex.HYPO_MARKERS + lex.CORRECTION_MARKERS):
                if _has(s.casefold(), [f]):
                    raise ParseError("frame marker in an inert sentence")
            if re.search(r"\b(" + "|".join(re.escape(c) for c in lex.NOT_STATED_CUES) + r")\b", s):
                m = DESIG_RE.findall(s)
                if m and m[0] == it.desig:
                    it.frames.append(("CUE", None, None))
            it.inert += 1
            continue
        vals = sentence_values(s, T, hits, attrs, kind)
        for an, v in vals:
            if kind == "FOCAL":
                if an in it.vec and it.vec[an] != v:
                    raise ParseError("two focal values for one attribute")
                it.vec[an] = v
                it.stated.add(an)
            else:
                it.frames.append((kind, an, v))
    return it


def sentence_values(s, T, hits, attrs, kind):
    out = []
    an_hits = [h for h in hits if h[3] == "aname"]
    nums = [(m.group(1), m.end()) for m in NUM_RE.finditer(s)]
    dates = DATE_RE.findall(s)
    if len({h[1] for h in an_hits}) > 1:
        raise ParseError("two numeric / date attributes in one sentence")
    for i, an, v, role in hits:
        a = attrs[an]
        if role == "val":
            out.append((an, v))
        elif role == "pterm":
            kc = negcount.count(s)
            if kind == "FOCAL":
                pres_words = set(lex.ABSENCE_PREDICATES)
                if kc.k_all == 0:
                    if set(T) & pres_words:
                        raise ParseError("absence predicate in a present sentence")
                    out.append((an, "present"))
                elif kc.k_all == 1:
                    out.append((an, "absent"))
                else:
                    raise ParseError("presence polarity")
            else:
                out.append((an, "present"))
    if an_hits:
        an = an_hits[0][1]
        a = attrs[an]
        if a["kind"] == "num":
            got = []
            for n, end in nums:
                rest = s[end:].lstrip()
                u = re.match(r"([A-Za-z]+(?:['\-][A-Za-z]+)*)", rest)
                if u and u.group(1) in a["unit"]:
                    got.append(Fraction(n))
            if len(got) != 1:
                raise ParseError(f"numeric sentence needs exactly one number in its unit: {s[:70]!r}")
            out.append((an, got[0]))
        else:
            if len(dates) != 1:
                raise ParseError("date sentence needs exactly one date")
            out.append((an, dt.date.fromisoformat(dates[0])))
    seen = [x[0] for x in out]
    if len(seen) != len(set(seen)):
        raise ParseError("one attribute twice in a sentence")
    if kind in ("FOCAL", "NEG") and len(out) > 1 and any(attrs[a]["kind"] == "pres" for a, _ in out):
        raise ParseError("presence term with another attribute in one sentence")
    if kind == "NEG" and len(out) != 1:
        raise ParseError("negated sentence with values of two attributes")
    return out




# ------------------------------------------------------------------------------------------------ S4 records (SEM-50)
REC_SUBJ_RE = re.compile(r"(?<![A-Za-z0-9_])(?i:" + "|".join(lex.SUBJECT_LABELS) + r"): ([A-Z]{2,3}-\d{3,5})(?!\d)")
BAD_FIELD_VALUES = {"", "-", "n/a", "N/A", "TBD", "?", "[]", "missing"}
PRES_YES = {"yes", "true"}
PRES_NO = {"no", "false", "none"}
NOT_STATED_VALUES = {"null", "unknown", "not recorded"}
KV_RE = re.compile(r"^\s*([a-z][a-z0-9_]*)(?:\s*=\s*|:\s+|\s\.{2,}\s)(.+)$")


def _scalar(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()
    if isinstance(v, (list, dict)):
        raise ParseError("nested value in a record field")
    return str(v).strip()


def _walk(obj, idf, out):
    if isinstance(obj, dict):
        if idf & set(obj):
            out.append([(str(k), _scalar(v)) for k, v in obj.items()])
            return
        for v in obj.values():
            _walk(v, idf, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, idf, out)


def _strip_fences(text):
    lines = [ln for ln in text.split("\n") if not ln.strip().startswith("```")]
    return "\n".join(lines)


def _tables(lines, idf):
    """Delimited tables (markdown pipes, csv pipe / comma / semicolon / tab): vertical (field, value) or horizontal."""
    import csv as _csv
    body = [ln.strip() for ln in lines if ln.strip()]
    for delim in ("|", "\t", ";", ","):
        rows = []
        for ln in body:
            if delim == "|":
                if "|" not in ln:
                    continue
                cells = [x.strip() for x in ln.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", x) for x in cells):
                    continue
            else:
                cells = next(_csv.reader([ln], delimiter=delim))
                cells = [x.strip() for x in cells]
                if len(cells) < 2:
                    continue
            rows.append(cells)
        if len(rows) < 2:
            continue
        head = rows[0]
        if idf & set(head):
            if any(len(x) != len(head) for x in rows):
                raise ParseError("ragged record table")
            return [list(zip(head, x)) for x in rows[1:]]
        if len(head) == 2 and any(x[0] in idf for x in rows[1:]):
            if any(len(x) != 2 for x in rows):
                raise ParseError("ragged field table")
            return [[(x[0], x[1]) for x in rows[1:]]]
    return None


def _kv(lines, idf):
    recs, cur = [], []
    for ln in lines:
        if not ln.strip():
            if cur:
                recs.append(cur)
                cur = []
            continue
        if REC_SUBJ_RE.search(ln) and not KV_RE.match(ln):
            continue
        m = KV_RE.match(ln)
        if not m:
            return None
        v = m.group(2).strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            try:
                import json as _json
                v = _json.loads(v)
            except ValueError:
                raise ParseError("bad quoted value")
        cur.append((m.group(1), v))
    if cur:
        recs.append(cur)
    recs = [x for x in recs if any(k in idf for k, _ in x)]
    return recs or None


def read_records(text: str, idf: str):
    """Container-agnostic record reader: list of records, each a list of (field, raw value)."""
    import json as _json
    t = _strip_fences(text)
    lines = t.split("\n")
    if any(ln.strip().startswith("|") or ("|" in ln and any(f in ln for f in idf)) for ln in lines):
        got = _tables(lines, idf)
        if got:
            return got
    s = t.strip()
    if s.startswith("{") or s.startswith("["):
        try:
            obj = _json.loads(s)
        except ValueError:
            obj = None
        if obj is not None:
            out = []
            _walk(obj, idf, out)
            if out:
                return out
    got = _kv([ln for ln in lines if not ln.strip().startswith("#")], idf)
    if got:
        return got
    got = _tables(lines, idf)
    if got:
        return got
    import yaml as _yaml
    try:
        obj = _yaml.safe_load(t)
    except Exception as e:      # noqa: BLE001
        raise ParseError(f"record container not readable: {str(e)[:40]}")
    out = []
    _walk(obj, idf, out)
    if not out:
        raise ParseError("no record with the ID field")
    return out


def field_value(pc, a, raw, *, focal):
    """Parse one designated field's raw value. Returns a value or None (not stated)."""
    if raw in BAD_FIELD_VALUES or raw.strip() != raw:
        raise ParseError(f"bad field value {raw!r}")
    if raw in NOT_STATED_VALUES:
        return None
    if a["kind"] == "nom":
        for v in a["values"]:
            if raw == v or raw in a["terms"].get(v, []):
                return v
        raise ParseError(f"unknown nominal field value {raw!r}")
    if a["kind"] == "pres":
        low = raw.casefold()
        if low in PRES_YES or raw in a["aterms"]:
            return "present"
        if low in PRES_NO:
            return "absent"
        raise ParseError(f"presence field value {raw!r}")
    if a["kind"] == "num":
        m = re.fullmatch(r"(\d+(?:\.\d+)?) ([A-Za-z]+(?:['\-][A-Za-z]+)*)", raw)
        if not m or m.group(2) not in a["unit"]:
            raise ParseError(f"numeric field value without its unit {raw!r}")
        return Fraction(m.group(1))
    m = re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw)
    if not m:
        raise ParseError(f"date field value {raw!r}")
    return dt.date.fromisoformat(raw)


def comment_values(pc, text, idx):
    """Value words inside a comment field (lures or echoes; they show nothing)."""
    out = []
    for i, an, v, role in find_value_words(toks(text), idx):
        if role == "val":
            out.append((an, v))
        elif role == "pterm":
            out.append((an, "present"))
    text_nd = DATE_RE.sub(" ", text)
    for m in NUM_RE.finditer(text_nd):
        rest = text_nd[m.end():].lstrip()
        u = re.match(r"([A-Za-z]+(?:['\-][A-Za-z]+)*)", rest)
        hits = [a for a in pc.attrs if a["kind"] == "num" and u and u.group(1) in a["unit"]]
        if len(hits) != 1:
            raise ParseError("number in a comment without exactly one unit owner")
        out.append((hits[0]["name"], Fraction(m.group(1))))
    for d in DATE_RE.findall(text):
        hits = [a for a in pc.attrs if a["kind"] == "date"]
        if len(hits) != 1:
            raise ParseError("date in a comment without one date attribute")
        out.append((hits[0]["name"], dt.date.fromisoformat(d)))
    return out


def parse_record(text: str, pc: PCard) -> PItem:
    """S4 report: subject line + record(s). Focal = the record whose field holds the subject designator."""
    it = PItem()
    subj = REC_SUBJ_RE.findall(text)
    if not subj or len(set(subj)) != 1:
        raise ParseError("record report needs exactly one subject line")
    it.desig = subj[0]
    recs = read_records(text, set(pc.fields.values()))
    focal = [x for x in recs if any(v == it.desig for _, v in x)]
    if len(focal) != 1:
        raise ParseError("focal record not unique")
    by_field = {f: a for a, f in ((pc.attr(n), f) for n, f in pc.fields.items())}
    idx = value_index(pc)
    fv = {}
    for rec in recs:
        keys = [k for k, _ in rec]
        if len(keys) != len(set(keys)):
            raise ParseError("field twice in one record")
        for f in pc.fields.values():
            if f not in keys:
                raise ParseError(f"record lacks field {f}")     # K34
    F = dict(focal[0])
    for f, a in by_field.items():
        v = field_value(pc, a, F[f], focal=True)
        fv[a["name"]] = v
        if v is not None:
            it.vec[a["name"]] = v
            it.stated.add(a["name"])
    for k, raw in focal[0]:
        if k in by_field:
            continue
        for pref, kind in (("previous_", "PRIOR"), ("proposed_", "HYPO")):
            if k.startswith(pref):
                a = by_field.get(k[len(pref):])
                if a is None:
                    raise ParseError(f"lure field for no attribute {k}")
                v = field_value(pc, a, raw, focal=False)
                if v is None:
                    raise ParseError("not-stated value in a lure field")
                it.frames.append((kind, a["name"], v))
                break
        else:
            if k.startswith("corrected_"):
                raise ParseError("corrected field not used on F11 r1 cards")
            if k == "comment" or re.fullmatch(r"comment_\d+", k):
                low = raw.casefold()
                if _has(low, lex.ATTACK_MARKERS):
                    it.attacks += 1
                    continue
                vals = comment_values(pc, raw, idx)
                if not vals:
                    it.inert += 1
                for an, v in vals:
                    it.frames.append(("COMMENT", an, v))
                continue
            if raw in BAD_FIELD_VALUES:
                raise ParseError("bad value in a distractor field")
            if DESIG_RE.fullmatch(raw):
                continue
            if find_value_words(toks(raw), idx) or NUM_RE.search(raw) or DATE_RE.search(raw):
                raise ParseError(f"value word in a distractor field {k}")
    for rec in recs:
        if rec is focal[0]:
            continue
        R = dict(rec)
        for f, a in by_field.items():
            v = field_value(pc, a, R[f], focal=False)
            if v is not None and v != fv[a["name"]]:
                it.frames.append(("OTHER", a["name"], v))
    return it



# ------------------------------------------------------------------------------------------------ S7 state
def parse_s7_state(state: str):
    """The quoted text (one line that starts and ends with a double quote, after line chrome) and attack notes."""
    quoted, attacks = [], 0
    for ln in state.split("\n"):
        s = ln.strip()
        if s.startswith("> "):
            s = s[2:]
        s = re.sub(r"^(?:\d+\. |[-*\u2022+\u00b7] |\d+\) |Step \d+: )", "", s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            quoted.append(s[1:-1])
        elif _has(s.casefold(), lex.ATTACK_MARKERS):
            attacks += 1
    if len(quoted) != 1:
        raise ParseError(f"S7 state needs exactly one quoted text, got {len(quoted)}")
    return quoted[0], attacks
