"""families/T46/solver_b.py: solver B of T46 (paradigm decision_table), written from G0_SPEC.md.

It imports nothing from the plugin, the tables or the renderers. parse() reads the RENDERED row: the state layout is
found by its first characters (B's own parsers for json, yaml, key-value, ticket, toml and xml), the rules block by its
line shapes, and every label, gloss, flag value, note and question wording is mapped to a semantic class by the
admitted lexicon registry in the kit context (the Haiku-read 2/2 pool), not by the generator's tables. solve_b()
answers from a decision table: one row per policy line (or per state signal on a plain row), the first row whose
condition holds decides.
"""
from __future__ import annotations

import json
import re

from c2_kit import cards as CARDS

CLASS_OF_SEM = {"disp.permit": "P", "disp.hold": "H", "disp.deny": "D", "disp.human": "E"}
SUFFIX_CLASS = (("_approval_threshold", "E"), ("_hard_limit", "D"), ("_soft_limit", "H"))
PLAIN_PRIORITY = ("D", "E", "H")
POSITIVE = ("yn_is", "yn_dneg")
NEGATIVE = ("yn_not", "yn_ruledout")
NUM_LINE = re.compile(r"^(.+?) is (above|at least) (.+)$")
FLAG_COND = re.compile(r"^(.+?) is (true|false)$")
LINE = re.compile(r"^(\d+)\. (.+?) if (.+)\.$")
_CACHE: dict = {}


def _n(t) -> str:
    return " ".join(str(t).casefold().split())


def _forms(lexicon) -> dict:
    """{normalised text: sem id} over the ADMITTED forms of the registry."""
    got = _CACHE.get(id(lexicon))
    if got is None or got[0] is not lexicon or got[1] != len(lexicon.forms):
        table = {_n(f.text): f.sem_id for i, f in lexicon.forms.items() if lexicon.status(i) == "admitted"}
        got = (lexicon, len(lexicon.forms), table)
        _CACHE[id(lexicon)] = got
    return got[2]


def _typed(v):
    if isinstance(v, bool) or isinstance(v, int):
        return v
    s = str(v).strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    if s in ("true", "yes"):
        return True
    if s in ("false", "no"):
        return False
    if re.fullmatch(r"\d+\.\d{2}", s):
        a, b = s.split(".")
        return int(a) * 100 + int(b)
    if re.fullmatch(r"\d+", s):
        return int(s)
    return s


def _walk(d, out):
    for k, v in d.items():
        if isinstance(v, dict):
            _walk(v, out)
        else:
            out[k] = _typed(v)


def flat_state(text: str) -> dict:
    out: dict = {}
    lines = [ln for ln in text.split("\n") if not ln.lstrip().startswith("#")]
    if text.startswith("{"):
        _walk(json.loads(text, parse_float=str), out)
    elif text.startswith("<record>"):
        for m in re.finditer(r"<(\w+)>(.*?)</\1>", text):
            out[m.group(1)] = _typed(m.group(2))
    elif text.startswith("[record]"):
        for ln in lines[1:]:
            k, _, v = ln.partition("=")
            out[k.strip()] = _typed(v.strip())
    elif text.startswith("---"):
        for ln in lines[1:]:
            body = ln.strip()
            if body.endswith(":") and ": " not in body:
                continue                                   # a group header
            k, _, v = body.partition(": ")
            out[k] = _typed(v)
    elif text.startswith("Ticket extract"):
        for ln in lines[1:]:
            body = ln[2:] if ln[:2] in ("- ", "* ") else ln
            k, _, v = body.partition(": ")
            out[k.replace(" ", "_")] = _typed(v)
    else:
        for ln in lines:
            if "|" in ln and ": " not in ln:
                k, _, v = ln.partition("|")
            elif ": " in ln:
                k, _, v = ln.partition(": ")
            else:
                k, _, v = ln.partition("=")
            out[k.strip()] = _typed(v.strip())
    return out


def parse_rules(rules: str) -> tuple:
    """(policy or None, {label: gloss}, closed sentence seen)."""
    lines = rules.split("\n")
    pol = None
    meanings: dict = {}
    in_meanings = False
    for ln in lines:
        if ln.startswith("Policy:"):
            pol = {"lines": [], "default": None, "ignore": []}
            in_meanings = False
        elif ln == "Meanings:":
            in_meanings = True
        elif in_meanings and ln.startswith("- "):
            label, _, gloss = ln[2:].partition(": ")
            meanings[label] = gloss
        elif pol is not None and LINE.match(ln):
            m = LINE.match(ln)
            pol["lines"].append([m.group(2), m.group(3).split(" or ")])
        elif pol is not None and ln.startswith("Otherwise: "):
            pol["default"] = ln[len("Otherwise: "):-1]
        elif pol is not None and ln.startswith("Never counted: "):
            pol["ignore"] = ln[len("Never counted: "):-1].split(", ")
    return pol, meanings


def parse(row: dict, ctx=None) -> dict:
    table = _forms(ctx.lexicon)
    fields = flat_state(row["state"])
    rules, question = CARDS.split_rules(row)
    pol, meanings = parse_rules(rules)
    proposed = None
    q_lines = question.split("\n")
    if row["qtype"] == "noul":
        first = q_lines[0]
        if not first.startswith("Proposed action: "):
            raise ValueError("a yes/no row names its proposed action")
        proposed = first[len("Proposed action: "):]
        q_lines = q_lines[1:]
    qsem = table.get(_n("\n".join(q_lines)))
    if qsem is None or not qsem.startswith("q.t46."):
        raise ValueError("question wording is not an admitted form")
    qform = qsem.split(".")[-1]
    printed = set(meanings)
    if pol:
        printed |= {lab for lab, _ in pol["lines"]} | {pol["default"]}
    if proposed is not None:
        printed.add(proposed)
    opts = list(row.get("options") or [])
    printed |= set(opts)

    def cls_of_label(lab: str) -> str:
        c_g = CLASS_OF_SEM.get(table.get(_n(meanings[lab]))) if lab in meanings else None
        c_l = CLASS_OF_SEM.get(table.get(_n(lab)))
        if lab in meanings and c_g is None:
            raise ValueError(f"gloss of {lab!r} is not admitted")
        if c_g and c_l and c_g != c_l:
            raise ValueError(f"label {lab!r} and its gloss name two classes")
        c = c_g or c_l
        if c is None:
            raise ValueError(f"label {lab!r} has no class")
        return c
    label_class = {lab: cls_of_label(lab) for lab in sorted(printed)}
    flag_class = {}
    for k, v in fields.items():
        if isinstance(v, bool):
            sem = table.get(_n(f'{k}: {"true" if v else "false"}'))
            if sem is None:
                raise ValueError(f"flag {k} = {v} is not an admitted form")
            flag_class[k] = CLASS_OF_SEM[sem]
    note_class = None
    if "note" in fields:
        sem = table.get(_n(fields["note"]))
        if sem is None:
            raise ValueError("the note is not an admitted form")
        note_class = CLASS_OF_SEM[sem]
    out = {"qform": qform, "fields": fields, "proposed": proposed, "policy": pol, "meanings": meanings,
           "label_class": label_class, "flag_class": flag_class, "note_class": note_class}
    if row["qtype"] == "choice":
        out["options"] = [label_class[o] for o in opts]
    return out


def _cond_holds(cond: str, f: dict) -> bool:
    m = FLAG_COND.match(cond)
    if m:
        return f[m.group(1)] == (m.group(2) == "true")
    m = NUM_LINE.match(cond)
    if not m:
        raise ValueError(f"condition {cond!r}")
    a, b = f[m.group(1)], f[m.group(3)]
    return a >= b if m.group(2) == "at least" else a > b


def _plain_class(view: dict) -> str:
    f = view["fields"]
    found = {c for k, c in view["flag_class"].items() if c != "P"}
    for k in f:
        for suf, c in SUFFIX_CLASS:
            if k.endswith(suf) and f.get(k[:-len(suf)], 0) > f[k]:
                found.add(c)
    if view["note_class"] not in (None, "P"):
        found.add(view["note_class"])
    for c in PLAIN_PRIORITY:
        if c in found:
            return c
    return "P"


def decision(view: dict) -> str:
    pol = view["policy"]
    if pol is None:
        return _plain_class(view)
    for lab, conds in pol["lines"]:
        if any(_cond_holds(c, view["fields"]) for c in conds):
            return view["label_class"][lab]
    return view["label_class"][pol["default"]]


def solve_b(view: dict):
    cls = decision(view)
    q = view["qform"]
    if q == "ch_disp":
        return cls
    asked = view["label_class"][view["proposed"]]
    if q in POSITIVE:
        return int(cls == asked)
    if q in NEGATIVE:
        return int(cls != asked)
    raise ValueError(f"question form {q!r}")
