"""v3_def_literal: the independent decide2 for F6 `gen3_def_literal` (yn2b SPEC 4.1, 8.1).

Written by builder A from the SPEC (sections 4, 5/F6, 8), `yn2b/F6_DEF_LITERAL_NOTES.md` (rendered surface only) and
the RENDERED rows. It never imports or reads the generator's decision code: `dl_core.py` (decide), `dl_sample.py`
(sampler) and `gen3_def_literal.py` (builder). It does not import `dl_render.py` (the builder's own parser) either.
It imports `dl_packs` for SURFACE DATA ONLY (field labels, verb phrases, fact sentences, unit formats, closed value
lists), as the notes allow. The definition grammar, the question grammar, the operator meanings, the comparison and
the decision rule are written here from the definition text itself.

Per raw row:
  1. kind_of(row)              yes/no (options ['yes','no']), JB-letter (2 statement options) or choice.
  2. the definition text       yes/no: the card's clause line (row['_defs'] or the defs file of meta.defs);
                               JB: the state's governing definition (field, sentence or e-mail line);
                               choice: the option lines (Requirement - ... / Exclusion - ... / Every condition ...).
  3. parse_definition(text)    -> Defn. Strict: the parsed structure is rendered back and must equal the text.
  4. parse_question(q)         -> the template family (is / not / judge / judge_n / choice / jb), clause, entity, term.
  5. parse_state(state)        -> Doc: the file section (record, governing definition), the entity's shown facts
                                  (any of json / kv / markdown / prose / email), background and notes (never used
                                  for the label; background is read only for the 'outside rule' sensitivity).
  6. evaluate(defn, facts)     -> applies? The definition's own rule: (elements hold [all | at least one] OR the
                                  deeming clause holds) AND no exclusion applies; an exclusion applies iff its
                                  trigger is established and its 'unless' part is not; a fact the file does not
                                  record is not established.
  7. decide2_row(row)          -> 'yes' / 'no' or the option string; mv_core.UNDEFINED if anything fails to parse.

decide2 never reads gold, trace, shortcut or tier fields. meta is read only for `meta.defs` (the pointer to the card
text that the row shows) and, in the REPORT only, for grouping and cross-checks (pack, fmt, view, tpl).

Readings. Where the text leaves room, decide2 uses DEFAULT_READINGS (fixed from the definition text before any
comparison with the gold). `sensitivity` re-runs every row under each alternative and lists the rows whose answer
depends on it (the ambiguity report for R2's hunt).

CLI (from lean/):
  ../.venv/bin/python golden_src/gen3/v3_def_literal.py            agreement, structure, sensitivity, cards (prints)
  ../.venv/bin/python golden_src/gen3/v3_def_literal.py --quick    agreement only
  ../.venv/bin/python golden_src/gen3/v3_def_literal.py --write    also writes yn2b/v3_def_literal_agreement.json and
                                                                   appends its sha256 to MANIFEST_yn2b.jsonl
Tests: yn2b/tests/test_v3_def_literal_{unit,written}.py.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

GEN3 = Path(__file__).resolve().parent
LEAN = GEN3.parents[1]
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
DEFS = LEAN / "data" / "v14_parts" / "yn2b_defs"
KEY = "gen3_def_literal"
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

import dl_packs as P  # noqa: E402  (surface data only: labels, verb phrases, fact sentences, unit formats)


class ParseError(Exception):
    """The rendered row could not be read unambiguously. decide2 never guesses."""


DEFAULT_READINGS = {
    # a deeming clause WITHOUT ", provided no exclusion applies": exclusions still apply ("It is not X if ..." is
    # categorical). Alternative "overrides": the deemed item counts even when an exclusion applies.
    "deem_no_proviso": "exclusions_apply",
    # a condition phrased in the negative ("has not paid ...", "did not travel in a sealed container") on a flag the
    # file does not record: not established (the definition says so). Alternative "holds".
    "unrecorded_negative": "not_established",
    # an attribute the definition uses that the state does not show at all (no field, no "not recorded" line):
    # "error" = refuse to label (ParseError). Alternative "not_established".
    "absent_attribute": "error",
}

# ------------------------------------------------------------------------------------------------ operator meanings
# Own table (not dl_packs.NUM_OPS): the words as an ordinary reader takes them.
NUM_WORDS = {"at least": ">=", "more than": ">", "at most": "<=", "no more than": "<=", "less than": "<",
             "fewer than": "<"}
DATE_WORDS = {"on or before": "<=", "before": "<", "on or after": ">=", "after": ">"}
_NUM_ALT = "|".join(sorted((re.escape(w) for w in NUM_WORDS), key=len, reverse=True))
_DATE_ALT = "|".join(sorted((re.escape(w) for w in DATE_WORDS), key=len, reverse=True))
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
DATE_RE = r"\d{1,2} (?:" + "|".join(MONTHS) + r") \d{4}"


def to_date(s: str) -> dt.date:
    m = re.fullmatch(r"(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})", s.strip())
    if not m:
        raise ParseError(f"not a date: {s!r}")
    return dt.date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)))


def to_int(s: str) -> int:
    s = s.strip()
    if not re.fullmatch(r"\d{1,3}(?:,\d{3})+|\d+", s):
        raise ParseError(f"not an integer: {s!r}")
    return int(s.replace(",", ""))


def compare(v, op: str, x) -> bool:
    return {">=": v >= x, ">": v > x, "<=": v <= x, "<": v < x}[op]


# ------------------------------------------------------------------------------------------------ pack catalogue
def _unit_re(unit: str) -> str:
    """One capture group holding the number. Built from the unit's printed form (dl_packs.unit_regex is the same
    surface); asserted to have exactly one group."""
    rx = P.unit_regex(unit)
    if re.compile(rx).groups != 1:
        raise AssertionError(unit)
    return rx


def _tpl_re(tpl: str, slots: dict) -> str:
    """A template with {slot}s -> regex: the literal parts escaped, each slot replaced by its sub-pattern."""
    out, pos = [], 0
    for m in re.finditer(r"\{(\w+)\}", tpl):
        out.append(re.escape(tpl[pos:m.start()]))
        out.append(slots[m.group(1)])
        pos = m.end()
    out.append(re.escape(tpl[pos:]))
    return "".join(out)


@dataclass
class Cat:
    """The surface catalogue of one pack."""
    pack: object
    attrs: dict                       # attr id -> dl_packs.Attr
    by_label: dict                    # field label -> attr id
    by_what: dict                     # "The file does not record <what>." -> attr id
    fact_res: list                    # (attr id, compiled regex, kind) for fact sentences
    cond_res: list                    # (attr id, compiled regex, flag want or None) for verb phrases
    desc_re: re.Pattern               # the description sentence (prose / email)
    filler_re: re.Pattern             # e-mail file-detail lines


def _build_cat(p) -> Cat:
    attrs = {a.id: a for a in p.attrs}
    by_label, by_what, fact_res, cond_res = {}, {}, [], []
    for a in p.attrs:
        if a.label in by_label or a.what in by_what:
            raise AssertionError(f"{p.id}: label/what clash {a.id}")
        by_label[a.label], by_what[a.what] = a.id, a.id
        if a.kind == "num":
            fact_res.append((a.id, re.compile(_tpl_re(a.fact, {"v": _unit_re(a.unit)})), "num"))
            cond_res.append((a.id, re.compile(_tpl_re(a.vp, {"op": f"({_NUM_ALT})", "x": _unit_re(a.unit)})), None))
        elif a.kind == "date":
            fact_res.append((a.id, re.compile(_tpl_re(a.fact, {"v": f"({DATE_RE})"})), "date"))
            cond_res.append((a.id, re.compile(_tpl_re(a.vp, {"op": f"({_DATE_ALT})", "x": f"({DATE_RE})"})), None))
        elif a.kind == "cat":
            alt = "|".join(sorted((re.escape(v) for v in a.values), key=len, reverse=True))
            fact_res.append((a.id, re.compile(_tpl_re(a.fact, {"v": f"({alt})"})), "cat"))
            cond_res.append((a.id, re.compile(_tpl_re(a.vp, {"list": "(.+)"})), None))
        elif a.kind == "flag":
            fact_res.append((a.id, re.compile(re.escape(a.fact_true)), True))
            fact_res.append((a.id, re.compile(re.escape(a.fact_false)), False))
            cond_res.append((a.id, re.compile(re.escape(a.vp_true)), True))
            cond_res.append((a.id, re.compile(re.escape(a.vp_false)), False))
        else:
            raise AssertionError(a.kind)
    dfield, dsent, _src = P.DESC[p.id]
    # the description sentence names the item / person / org; {desc} is the description field's text
    desc_re = re.compile(_tpl_re(dsent, {"desc": "(.+)", "name": "(.+)", "org": "(.+)"}))
    filler_re = re.compile(r"The (" + "|".join(re.escape(lbl) for lbl, _ in p.filler) + r") is (.+)\.")
    return Cat(p, attrs, by_label, by_what, fact_res, cond_res, desc_re, filler_re)


CATS = {pid: _build_cat(p) for pid, p in P.PACKS.items()}
CLAUSE_WORDS = sorted({p.clause for p in P.PACKS.values()}, key=len, reverse=True)
CLAUSE_RE = "(?:" + "|".join(re.escape(w) for w in CLAUSE_WORDS) + r") \d+"


def pack_for(clause: str, entity: str) -> str:
    """The pack is identified from the rendered text: the clause word ('Rule', 'Bylaw', ...) and the entity."""
    word = re.fullmatch(r"(.+) \d+", clause).group(1)
    hits = [pid for pid, p in P.PACKS.items() if p.clause == word and p.entity == entity]
    if len(hits) != 1:
        raise ParseError(f"no unique pack for clause {clause!r} and entity {entity!r}: {hits}")
    return hits[0]


# ------------------------------------------------------------------------------------------------ conditions
@dataclass(frozen=True)
class Cond:
    attr: str
    kind: str                         # num | date | cat | flag
    op: str | None = None             # num / date
    limit: object = None              # int / date
    values: tuple = ()                # cat
    want: bool | None = None          # flag
    text: str = ""                    # the verb phrase as printed

    def holds(self, facts: dict, readings: dict | None = None) -> bool:
        rd = readings or DEFAULT_READINGS
        if self.attr not in facts:
            if rd["absent_attribute"] == "error":
                raise ParseError(f"attribute {self.attr} is used by the definition but not shown in the state")
            return False
        v = facts[self.attr]
        if v is None:                                    # the file does not record it: not established
            return self.kind == "flag" and self.want is False and rd["unrecorded_negative"] == "holds"
        if self.kind in ("num", "date"):
            return compare(v, self.op, self.limit)
        if self.kind == "cat":
            return v in self.values
        return v is self.want


def split_list(s: str, values: tuple) -> tuple | None:
    """'x', 'x or y', 'x, y or z' -> the values; None when any item is not one of the attribute's values."""
    if " or " in s:
        head, last = s.rsplit(" or ", 1)
        items = head.split(", ") + [last]
    else:
        items = [s]
    if any(i not in values for i in items) or len(set(items)) != len(items):
        return None
    return tuple(items)


def parse_vp(cat: Cat, vp: str) -> Cond:
    """One verb phrase (the text after 'the <entity> ' or '<entity> that|who ') -> exactly one attribute condition."""
    found = []
    for aid, rx, want in cat.cond_res:
        m = rx.fullmatch(vp)
        if not m:
            continue
        a = cat.attrs[aid]
        if a.kind == "num":
            found.append(Cond(aid, "num", NUM_WORDS[m.group(1)], to_int(m.group(2)), text=vp))
        elif a.kind == "date":
            found.append(Cond(aid, "date", DATE_WORDS[m.group(1)], to_date(m.group(2)), text=vp))
        elif a.kind == "cat":
            vals = split_list(m.group(1), a.values)
            if vals is not None:
                found.append(Cond(aid, "cat", values=vals, text=vp))
        else:
            found.append(Cond(aid, "flag", want=want, text=vp))
    if len(found) != 1:
        raise ParseError(f"{cat.pack.id}: verb phrase {vp!r} matches {len(found)} attributes")
    return found[0]


# ------------------------------------------------------------------------------------------------ definitions
@dataclass
class Defn:
    entity: str
    article: str                      # 'A' / 'An' of the head
    term: str                         # with its article and quotes: "a 'fruit'", "'spam'"
    joiner: str                       # 'all' | 'any'
    elements: list                    # [Cond]
    exclusions: list                  # [(Cond trigger, Cond unless | None)]
    deem: Cond | None = None
    deem_rel: str = ""                # 'that' / 'who'
    deem_article: str = ""
    proviso: bool = False             # ", provided no exclusion applies"
    clause: str = ""
    pack: str = ""


_DEF_RE = re.compile(
    r"(?P<art>A|An) (?P<ent>[a-z]+) is (?P<term>(?:an? )?'[^']+') only if "
    r"(?P<join>all of the following hold|at least one of the following holds): (?P<els>\(a\) .+?)\."
    r"(?P<excl>(?: It is not (?P=term) if .+?\.)(?: It is also not (?P=term) if .+?\.)*)?"
    r"(?: (?P<dart>A|An) (?P=ent) (?P<rel>that|who) (?P<deem>.+?) also counts as (?P=term) even if the listed "
    r"conditions are not met(?P<prov>, provided no exclusion applies)?\.)?"
    r" A fact the file does not record counts as not established\.")
_JOIN = {"all of the following hold": "all", "at least one of the following holds": "any"}


def parse_definition(text: str, clause: str) -> Defn:
    m = _DEF_RE.fullmatch(text)
    if not m:
        raise ParseError(f"definition does not follow the grammar: {text[:120]!r}")
    ent = m.group("ent")
    cat = CATS[pack_for(clause, ent)]
    lead = f"the {ent} "
    elements = []
    for i, part in enumerate(m.group("els").split("; ")):
        pm = re.fullmatch(r"\(([a-z])\) (.+)", part)
        if not pm or pm.group(1) != "abcdefghij"[i] or not pm.group(2).startswith(lead):
            raise ParseError(f"element {i} malformed: {part!r}")
        elements.append(parse_vp(cat, pm.group(2)[len(lead):]))
    exclusions = []
    if m.group("excl"):
        # one sentence per exclusion: "It is not T if ...[, unless ...]." then "It is also not T if ...." (R2, 1 Oct)
        parts = re.split(r" It is (?:also )?not " + re.escape(m.group("term")) + " if ", m.group("excl"))[1:]
        for part in parts:
            if not part.startswith(lead) or not part.endswith("."):
                raise ParseError(f"exclusion malformed: {part!r}")
            trig, sep, unl = part[len(lead):-1].partition(f", unless {lead}")
            exclusions.append((parse_vp(cat, trig), parse_vp(cat, unl) if sep else None))
    deem = parse_vp(cat, m.group("deem")) if m.group("deem") else None
    d = Defn(ent, m.group("art"), m.group("term"), _JOIN[m.group("join")], elements, exclusions, deem,
             m.group("rel") or "", m.group("dart") or "", bool(m.group("prov")), clause, cat.pack.id)
    if render_definition(d) != text:
        raise ParseError("definition does not round-trip")
    return d


def render_definition(d: Defn) -> str:
    """The grammar, printed back from the parsed structure (the round-trip check of parse_definition)."""
    join = {v: k for k, v in _JOIN.items()}[d.joiner]
    s = f"{d.article} {d.entity} is {d.term} only if {join}: "
    s += "; ".join(f"({'abcdefghij'[i]}) the {d.entity} {c.text}" for i, c in enumerate(d.elements)) + "."
    for j, (t, u) in enumerate(d.exclusions):
        s += f" It is {'also ' if j else ''}not {d.term} if the {d.entity} {t.text}" + \
            (f", unless the {d.entity} {u.text}" if u else "") + "."
    if d.deem:
        s += (f" {d.deem_article} {d.entity} {d.deem_rel} {d.deem.text} also counts as {d.term} even if the listed "
              f"conditions are not met" + (", provided no exclusion applies" if d.proviso else "") + ".")
    return s + " A fact the file does not record counts as not established."


@dataclass
class Outcome:
    applies: bool
    elements: list                    # bool per element
    elements_ok: bool
    deem_ok: bool | None
    excl: list                        # (trigger holds, unless holds, applies) per exclusion
    reasons_yes: int                  # independent sufficient paths to 'applies'
    reasons_no: int                   # independent sufficient reasons for 'does not apply'
    decisive: list = field(default_factory=list)   # attr ids that decide the outcome


def evaluate(d: Defn, facts: dict, readings: dict | None = None) -> Outcome:
    rd = readings or DEFAULT_READINGS
    el = [c.holds(facts, rd) for c in d.elements]
    el_ok = all(el) if d.joiner == "all" else any(el)
    deem_ok = d.deem.holds(facts, rd) if d.deem else None
    excl = []
    for t, u in d.exclusions:
        th = t.holds(facts, rd)
        uh = u.holds(facts, rd) if u else False
        excl.append((th, uh, th and not uh))
    any_excl = any(x[2] for x in excl)
    path = el_ok or bool(deem_ok)
    if d.deem and not d.proviso and deem_ok and rd["deem_no_proviso"] == "overrides":
        applies = True
    else:
        applies = path and not any_excl
    reasons_yes = ((sum(el) if d.joiner == "any" else int(el_ok)) + int(bool(deem_ok))) if applies else 0
    reasons_no = 0
    decisive = []
    if not applies:
        reasons_no += sum(x[2] for x in excl)
        decisive += [d.exclusions[i][0].attr for i, x in enumerate(excl) if x[2]]
        if not path:
            reasons_no += (len(el) - sum(el)) if d.joiner == "all" else 1
            decisive += [c.attr for c, ok in zip(d.elements, el) if not ok]
    else:
        decisive += [c.attr for c, ok in zip(d.elements, el) if ok] + ([d.deem.attr] if deem_ok else [])
    return Outcome(applies, el, el_ok, deem_ok, excl, reasons_yes, reasons_no, decisive)


# ------------------------------------------------------------------------------------------------ states
@dataclass
class Doc:
    fmt: str
    file: dict                        # file-level fields (structured) or {} (prose / email)
    entity_fields: dict | None        # structured formats: label -> value text (description included)
    entity_sentences: list | None     # prose / email: the entity's sentences / lines
    record: str | None                # the judge record: "a 'X'" / "not a 'X'"
    gov: dict | None                  # JB: {clause, instrument, in_force, text}
    background: list                  # background statements (never used for the label)
    notes: list                       # notes (never used; attack plants live here)
    opened: dt.date | None = None


_GOV_RE = re.compile(r"(?P<clause>" + CLAUSE_RE + r") of the (?P<instr>.+?) \(in force from (?P<d>" + DATE_RE +
                     r")\): (?P<text>(?:A|An) .+? A fact the file does not record counts as not established\.)")


def _gov(s: str) -> dict:
    m = _GOV_RE.fullmatch(s)
    if not m:
        raise ParseError(f"governing definition malformed: {s[:100]!r}")
    return {"clause": m.group("clause"), "instrument": m.group("instr"), "in_force": to_date(m.group("d")),
            "text": m.group("text")}


def _sniff(state: str) -> str:
    if state.startswith("{"):
        return "json"
    if state.startswith("## "):
        return "markdown"
    if state.startswith("From: "):
        return "email"
    if state.startswith("file."):
        return "kv"
    if state.startswith("File "):
        return "prose"
    raise ParseError("unknown state format")


def _structured(fmt: str, file: dict, ent: dict, bg: list, notes: list) -> Doc:
    gov = _gov(file["governing definition"]) if "governing definition" in file else None
    return Doc(fmt, file, ent, None, file.get("recorded classification"), gov, bg, notes,
               to_date(file["opened"]) if "opened" in file else None)


def _parse_json(state: str) -> Doc:
    obj = json.loads(state)
    if json.dumps(obj, indent=1, ensure_ascii=False) != state:
        raise ParseError("json state is not canonical")
    keys = list(obj)
    if len(keys) != 4 or keys[0] != "file" or keys[2:] != ["background", "notes"]:
        raise ParseError(f"json top-level keys {keys}")
    ent = obj[keys[1]]
    if not all(isinstance(v, str) for v in list(obj["file"].values()) + list(ent.values())):
        raise ParseError("json field values must be strings")
    d = _structured("json", obj["file"], ent, list(obj["background"]), list(obj["notes"]))
    d.file = dict(obj["file"], _entity_key=keys[1])
    return d


def _parse_kv(state: str) -> Doc:
    file, ent, bg, notes, ent_key = {}, {}, [], [], None
    for ln in state.split("\n"):
        k, sep, v = ln.partition(": ")
        if not sep or "." not in k:
            raise ParseError(f"kv line malformed: {ln[:80]!r}")
        sec, _, sub = k.partition(".")
        if sec == "file":
            tgt = file
        elif sec == "background":
            bg.append(v)
            continue
        elif sec == "notes":
            notes.append(v)
            continue
        else:
            if ent_key not in (None, sec):
                raise ParseError(f"two entity sections: {ent_key}, {sec}")
            ent_key, tgt = sec, ent
        if sub in tgt:
            raise ParseError(f"duplicate kv key {k}")
        tgt[sub] = v
    d = _structured("kv", file, ent, bg, notes)
    d.file["_entity_key"] = ent_key
    return d


def _parse_markdown(state: str) -> Doc:
    secs, cur = [], None
    for ln in state.split("\n"):
        if ln.startswith("## "):
            cur = (ln[3:], [])
            secs.append(cur)
        elif ln.strip() == "":
            continue
        elif cur is not None and ln.startswith("- "):
            cur[1].append(ln[2:])
        else:
            raise ParseError(f"markdown line outside a bullet: {ln[:80]!r}")
    titles = [t for t, _ in secs]
    if len(titles) != 4 or titles[0] != "File" or titles[2:] != ["Background", "Notes"]:
        raise ParseError(f"markdown sections {titles}")

    def kv(items):
        out = {}
        for it in items:
            k, sep, v = it.partition(": ")
            if not sep or k in out:
                raise ParseError(f"markdown field malformed: {it[:80]!r}")
            out[k] = v
        return out

    d = _structured("markdown", kv(secs[0][1]), kv(secs[1][1]), list(secs[2][1]), list(secs[3][1]))
    d.file["_entity_key"] = titles[1].lower()
    return d


_SENT_SPLIT = re.compile(r"(?<=\.) (?=[A-Z])")
_REC_PROSE = re.compile(r"The (?P<reg>[a-z ]+?) records the (?P<ent>[a-z]+) as (?P<cls>(?:not )?(?:an? )?'[^']+')\.")
_GOV_PROSE = re.compile(r"The governing definition is (.+? A fact the file does not record counts as not "
                        r"established\.)")


def _parse_prose(state: str) -> Doc:
    paras = state.split("\n\n")
    if len(paras) != 4 or not paras[0].startswith("File ") or not paras[2].startswith("Background: ") \
            or not paras[3].startswith("Notes on the file: "):
        raise ParseError("prose layout is not file / entity / Background / Notes")
    p0 = paras[0]
    gov = None
    gm = _GOV_PROSE.search(p0)
    if gm:
        gov = _gov(gm.group(1))
        p0 = p0[:gm.start()] + p0[gm.end():]
    recs = list(_REC_PROSE.finditer(p0))
    if len(recs) > 1:
        raise ParseError("two register sentences")
    om = re.match(r"File \S+ was opened on (" + DATE_RE + r") by ", paras[0])
    return Doc("prose", {}, None, _SENT_SPLIT.split(paras[1]), recs[0].group("cls") if recs else None, gov,
               [paras[2][len("Background: "):]], [paras[3][len("Notes on the file: "):]],
               to_date(om.group(1)) if om else None)


def _parse_email(state: str) -> Doc:
    blocks = state.split("\n\n----------\n\n")
    msgs = []
    for b in blocks:
        head, sep, body = b.partition("\n\n")
        if not sep:
            raise ParseError("e-mail block without a body")
        h = {}
        for ln in head.split("\n"):
            k, s2, v = ln.partition(": ")
            if not s2 or k not in ("From", "To", "Subject") or k in h:
                raise ParseError(f"e-mail header malformed: {ln!r}")
            h[k] = v
        msgs.append((h, body.split("\n")))
    if not msgs[0][0].get("Subject", "").startswith("File "):
        raise ParseError("first e-mail is not the file message")
    record, gov, lines, bg, notes = None, None, [], [], []
    for ln in msgs[0][1]:
        if ln.startswith("Governing definition, "):
            if gov:
                raise ParseError("two governing definitions")
            gov = _gov(ln[len("Governing definition, "):])
        else:
            lines.append(ln)
    for h, body in msgs[1:]:
        subj = h.get("Subject")
        if subj == "Register entry":
            if record is not None or len(body) != 1:
                raise ParseError("register message malformed")
            rm = re.fullmatch(r"Recorded classification for this file: ((?:not )?(?:an? )?'[^']+')\.", body[0])
            if not rm:
                raise ParseError(f"register line malformed: {body[0]!r}")
            record = rm.group(1)
        elif subj == "Background":
            bg += body
        elif subj in ("File notes", "Re: file notes"):
            notes += body
        else:
            raise ParseError(f"unknown e-mail subject {subj!r}")
    om = re.fullmatch(r"Opened on (" + DATE_RE + r")\.", lines[0]) if lines else None
    return Doc("email", {}, None, lines, record, gov, bg, notes, to_date(om.group(1)) if om else None)


def parse_state(state: str) -> Doc:
    return {"json": _parse_json, "kv": _parse_kv, "markdown": _parse_markdown, "prose": _parse_prose,
            "email": _parse_email}[_sniff(state)](state)


def _value(cat: Cat, aid: str, s: str):
    """A structured field's value text -> int / date / str / bool, or None for 'not recorded'."""
    if s == "not recorded":
        return None
    a = cat.attrs[aid]
    if a.kind == "num":
        m = re.fullmatch(_unit_re(a.unit), s)
        if not m:
            raise ParseError(f"{aid}: {s!r} is not a {a.unit} value")
        return to_int(m.group(1))
    if a.kind == "date":
        return to_date(s)
    if a.kind == "cat":
        if s not in a.values:
            raise ParseError(f"{aid}: {s!r} is not a listed value")
        return s
    if s not in ("yes", "no"):
        raise ParseError(f"{aid}: flag value {s!r}")
    return s == "yes"


def facts_of(doc: Doc, cat: Cat) -> dict:
    """attr id -> value (None = the file does not record it) for every attribute the state shows. Strict: every
    entity field / sentence must be a known attribute, the description, or (e-mail) a file line."""
    facts = {}

    def put(aid, v):
        if aid in facts:
            raise ParseError(f"attribute {aid} shown twice")
        facts[aid] = v

    if doc.entity_fields is not None:
        ek = doc.file.get("_entity_key")
        if ek != cat.pack.entity:
            raise ParseError(f"entity section {ek!r} is not {cat.pack.entity!r}")
        if "description" not in doc.entity_fields:
            raise ParseError("entity description missing")
        for lbl, v in doc.entity_fields.items():
            if lbl == "description":
                continue
            if lbl not in cat.by_label:
                raise ParseError(f"unknown entity field {lbl!r}")
            put(cat.by_label[lbl], _value(cat, cat.by_label[lbl], v))
        return facts
    n_desc = 0
    for i, s in enumerate(doc.entity_sentences):
        hit = [(aid, m, kind) for aid, rx, kind in cat.fact_res for m in [rx.fullmatch(s)] if m]
        miss = re.fullmatch(r"The file does not record (.+)\.", s)
        if len(hit) > 1:
            raise ParseError(f"sentence matches {len(hit)} fact templates: {s!r}")
        if hit:
            aid, m, kind = hit[0]
            if kind == "num":
                put(aid, to_int(m.group(1)))
            elif kind == "date":
                put(aid, to_date(m.group(1)))
            elif kind == "cat":
                put(aid, m.group(1))
            else:
                put(aid, kind)
        elif miss and miss.group(1) in cat.by_what:
            put(cat.by_what[miss.group(1)], None)
        elif cat.desc_re.fullmatch(s):
            n_desc += 1
        elif doc.fmt == "email" and (re.fullmatch(r"Opened on " + DATE_RE + r"\.", s) and i == 0
                                     or cat.filler_re.fullmatch(s)):
            continue
        else:
            raise ParseError(f"unread entity sentence: {s!r}")
    if n_desc != 1:
        raise ParseError(f"{n_desc} description sentences")
    return facts


# ------------------------------------------------------------------------------------------------ questions
_C = r"(?P<clause>" + CLAUSE_RE + r")"
_E = r"(?P<ent>[a-z]+)"
_T = r"(?P<term>(?:an? )?'[^']+')"
_N = r"(?P<neg>not )?"
QUESTIONS = [  # (family, regex); family 'is' / 'judge' get polarity from the 'not' group
    ("is", rf"Under {_C} of the (?P<instr>.+?), is the {_E} {_N}{_T}\?"),
    ("is", rf"Going by the definition in {_C} and not by everyday usage, is the {_E} {_N}{_T}\?"),
    ("is", rf"Does the {_E} {_N}count as {_T} as {_C} defines that term\?"),
    ("is", rf"Applying only the definition in {_C}, with no outside rules, does the {_E} {_N}qualify as {_T}\?"),
    ("is", rf"Taking {_C} as the binding definition, should the {_E} {_N}be classed as {_T}\?"),
    ("judge", rf"Is the classification recorded in the (?P<reg>[a-z ]+?) for this {_E} {_N}consistent with {_C}\?"),
    ("judge", rf"Is the {_E}'s recorded classification {_N}supported by the definition in {_C}\?"),
    ("judge", rf"Does {_C} {_N}support the classification the (?P<reg>[a-z ]+?) records for the {_E}\?"),
    ("judge", rf"Under {_C}, is the classification on file for the {_E} {_N}consistent with the definition\?"),
    ("judge", rf"Is the entry in the (?P<reg>[a-z ]+?) for this {_E} {_N}backed by {_C} as written\?"),
    ("choice", rf"Which condition listed in the options keeps the {_E} from counting as {_T} under {_C}, or is "
               rf"every condition satisfied\?"),
    ("choice", rf"Under {_C}, which listed requirement or exclusion decides that the {_E} is not {_T}, or does it "
               rf"meet every condition\?"),
    ("choice", rf"Applying only {_C}, which option names the condition that stops the {_E} from being {_T}, or are "
               rf"all conditions satisfied\?"),
    ("choice", rf"Which of the listed conditions of {_C} does the {_E} not satisfy, if any, so that it is not {_T}\?"),
    ("choice", rf"Taking {_C} as binding, which listed condition rules the {_E} out as {_T}, or is none of them a "
               rf"problem\?"),
    ("jb", rf"Under {_C} of the (?P<instr>.+?), is the {_E} {_T} or not\?"),
    ("jb", rf"Which statement fits the {_E} under the definition in {_C}\?"),
    ("jb", rf"Going by {_C} and not by everyday usage, which description applies to the {_E}\?"),
    ("jb", rf"Applying only the definition in {_C}, which statement holds for the {_E}\?"),
    ("jb", rf"Taking {_C} as the binding definition, which outcome applies to the {_E}\?"),
    # claim-stating JB questions (R2, 1 Oct): the only ones the fallback pair 'yes, this holds' / 'no, this does not
    # hold' may answer, since 'this' must be a claim the question states
    ("jbf", rf"Under {_C} of the (?P<instr>.+?), does the {_E} count as {_T}\?"),
    ("jbf", rf"Is the {_E} {_T} under the definition in {_C}\?"),
    ("jbf", rf"Going by {_C} and not by everyday usage, does the {_E} count as {_T}\?"),
    ("jbf", rf"Applying only the definition in {_C}, is the {_E} {_T}\?"),
    ("jbf", rf"Taking {_C} as the binding definition, is the {_E} {_T}\?"),
]
QUESTIONS = [(f, re.compile(rx)) for f, rx in QUESTIONS]


def parse_question(q: str) -> dict:
    hits = [(f, m) for f, rx in QUESTIONS for m in [rx.fullmatch(q)] if m]
    if len(hits) != 1:
        raise ParseError(f"question matches {len(hits)} templates: {q!r}")
    f, m = hits[0]
    g = m.groupdict()
    return {"family": "jb" if f == "jbf" else f, "states_claim": f == "jbf", "neg": bool(g.get("neg")),
            "clause": g["clause"], "entity": g["ent"], "term": g.get("term"), "register": g.get("reg"),
            "instrument": g.get("instr")}


# ------------------------------------------------------------------------------------------------ the row
EVERY = "Every condition is satisfied"
JB_FALLBACK = ("yes, this holds", "no, this does not hold")


def kind_of(row: dict) -> str:
    o = row["options"]
    if o == ["yes", "no"]:
        return "yn"
    if len(o) == 2:
        return "jb"
    return "choice"


def card_of(row: dict) -> dict | None:
    if row.get("_defs") is not None:
        return row["_defs"]
    qid = (row.get("meta") or {}).get("defs")
    return json.loads((DEFS / f"{KEY}__{qid}.json").read_text()) if qid else None


def _choice_cond(cat: Cat, ent: str, opt: str):
    lead = f"the {ent} "
    m = re.fullmatch(r"(Requirement|Exclusion) - (.+)", opt)
    if not m or not m.group(2).startswith(lead):
        raise ParseError(f"choice option malformed: {opt!r}")
    body = m.group(2)[len(lead):]
    if m.group(1) == "Requirement":
        return "req", parse_vp(cat, body), None
    trig, sep, unl = body.partition(f", unless {lead}")
    return "excl", parse_vp(cat, trig), (parse_vp(cat, unl) if sep else None)


def solve(row: dict, readings: dict | None = None) -> dict:
    """Everything decide2 reads and concludes for one row (raises ParseError)."""
    rd = dict(DEFAULT_READINGS, **(readings or {}))
    kind = kind_of(row)
    q = parse_question(row["instructions"])
    if (kind == "yn") != (q["family"] in ("is", "judge")) or (kind in ("jb", "choice")) and q["family"] != kind:
        raise ParseError(f"question family {q['family']} does not fit a {kind} row")
    doc = parse_state(row["state"])
    out = {"kind": kind, "q": q, "fmt": doc.fmt}
    if kind == "choice":
        pid = pack_for(q["clause"], q["entity"])
        cat = CATS[pid]
        facts = facts_of(doc, cat)
        if row["options"][-1] != EVERY or row["options"].count(EVERY) != 1:
            raise ParseError("choice options must end with the 'every condition' option")
        failing, conds = [], []
        for opt in row["options"][:-1]:
            k, c, u = _choice_cond(cat, q["entity"], opt)
            conds.append((k, c, u))
            if k == "req":
                bad = not c.holds(facts, rd)
            else:
                bad = c.holds(facts, rd) and not (u.holds(facts, rd) if u else False)
            if bad:
                failing.append(opt)
        out.update(pack=pid, facts=facts, conds=conds, failing=failing)
        if len(failing) > 1:
            raise ParseError(f"{len(failing)} failing conditions: no unique answer")
        out["answer"] = failing[0] if failing else EVERY
        out["reasons"] = (len(failing), 0)
        return out
    if kind == "yn":
        card = card_of(row)
        if not card:
            raise ParseError("yes/no row without its card")
        keys = [k for k in card if k not in ("yes", "no")]
        if len(keys) != 1 or set(card) - set(keys) != {"yes", "no"}:
            raise ParseError(f"card keys {list(card)}")
        clause, text = keys[0], card[keys[0]]
    else:
        if not doc.gov:
            raise ParseError("JB row without a governing definition in the state")
        clause, text = doc.gov["clause"], doc.gov["text"]
    d = parse_definition(text, clause)
    if (q["clause"], q["entity"]) != (clause, d.entity) or (q["term"] and q["term"] != d.term):
        raise ParseError(f"question {q['clause']}/{q['entity']}/{q['term']} vs definition {clause}/{d.entity}/{d.term}")
    if q.get("instrument") and q["instrument"] != P.PACKS[d.pack].instrument:
        raise ParseError("question names another instrument")
    cat = CATS[d.pack]
    facts = facts_of(doc, cat)
    oc = evaluate(d, facts, rd)
    out.update(pack=d.pack, defn=d, facts=facts, outcome=oc, applies=oc.applies,
               reasons=(oc.reasons_yes, oc.reasons_no))
    if kind == "jb":
        o0, o1 = row["options"]
        e, t = d.entity.capitalize(), d.term
        fam = (f"The {d.entity} is {t} under {clause}.", f"The {d.entity} is not {t} under {clause}.")
        if (o0, o1) not in (fam, JB_FALLBACK):
            raise ParseError(f"JB options {row['options']} are neither the family wording nor the fallback ({e})")
        if (o0, o1) == JB_FALLBACK and not q["states_claim"]:
            raise ParseError("the fallback pair answers a question that states no claim ('this' has no referent)")
        out["answer"] = o0 if oc.applies else o1
        out["in_force"] = doc.gov["in_force"]
        return out
    if q["family"] == "is":
        yes = oc.applies != q["neg"]
    else:
        if doc.record is None:
            raise ParseError("judge row without a recorded classification")
        rec_neg = doc.record.startswith("not ")
        rec_term = doc.record[4:] if rec_neg else doc.record
        if rec_term != d.term:
            raise ParseError(f"record {doc.record!r} names another term than {d.term!r}")
        out["record_applies"] = not rec_neg
        yes = ((not rec_neg) == oc.applies) != q["neg"]
    out["answer"] = "yes" if yes else "no"
    return out


def decide2_row(row: dict, readings: dict | None = None):
    """SPEC 8.1 entry point: 'yes' / 'no' (yes/no rows) or the option string (choice and JB rows); mv_core.UNDEFINED
    when the rendered row cannot be read unambiguously."""
    try:
        return solve(row, readings)["answer"]
    except ParseError:
        import mv_core
        return mv_core.UNDEFINED


# ------------------------------------------------------------------------------------------------ report
def load_rows(part: str) -> list:
    p = RAW / (f"{KEY}.jsonl" if part == "train" else f"dev/{KEY}.jsonl")
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def load_rels(part: str) -> list:
    p = RAW / ("relations" if part == "train" else "dev/relations") / f"{KEY}.jsonl"
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()] if p.exists() else []


def _gold(row):
    return row["gold"]


def agreement(rows: list, readings: dict | None = None) -> dict:
    answers, dis, table = {}, [], defaultdict(Counter)
    for r in rows:
        k = f"{r['meta'].get('dev_kind') or 'train'}/{r['meta']['qkind']}/{r['meta']['view']}"
        table[k]["rows"] += 1
        try:
            a, err = solve(r, readings)["answer"], None
        except ParseError as e:
            a, err = None, str(e)
        answers[r["rid"]] = a
        if a == _gold(r):
            table[k]["agree"] += 1
        else:
            dis.append({"rid": r["rid"], "gold": r["gold"], "decide2": a, "error": err})
    n = len(rows)
    return {"rows": n, "agree": n - len(dis), "rate": round((n - len(dis)) / max(1, n), 6),
            "table": {k: dict(v) for k, v in sorted(table.items())}, "disagreements": dis, "answers": answers}


def diagnose(row: dict) -> str:
    """A plain-language trace of what decide2 read for a row (used for every disagreement)."""
    try:
        o = solve(row)
    except ParseError as e:
        return f"parse error: {e}"
    if o["kind"] == "choice":
        return f"failing conditions {o['failing']}; facts {o['facts']}"
    oc = o["outcome"]
    return (f"elements {oc.elements} ({o['defn'].joiner}) deem {oc.deem_ok} exclusions {oc.excl} -> applies "
            f"{oc.applies}; facts {o['facts']}")


def structure_under_decide2(rows: list, rels: list, answers: dict) -> dict:
    """SPEC 8.3 under decide2 alone: contrast twins flip, complements invert, equiv keeps, inv keeps; plus fact
    parity: equiv / inv / complement partners show the same facts, a contrast twin changes at most one fact."""
    by = {r["rid"]: r for r in rows}
    facts = {}
    for r in rows:
        try:
            o = solve(r)
            facts[r["rid"]] = (o["facts"], render_definition(o["defn"]) if "defn" in o else
                               tuple(r["options"]))
        except ParseError:
            facts[r["rid"]] = None

    def yes_of(rid):
        r, a = by[rid], answers.get(rid)
        if a is None:
            return None
        if r["meta"]["qkind"] == "jb":
            return r["options"].index(a) == 0
        return a == "yes" if r["meta"]["qkind"] == "yn" else a

    out = {"contrast_pairs": 0, "contrast_not_flipped": [], "contrast_fact_changes": Counter(),
           "complement": 0, "complement_not_inverted": [], "equiv": 0, "equiv_changed": [], "inv": 0,
           "inv_changed": [], "fact_parity_broken": [], "unknown_rel": []}
    for r in rows:
        t = r["meta"].get("twin_of")
        if not t or t not in by:
            continue
        out["contrast_pairs"] += 1
        a, b = yes_of(t), yes_of(r["rid"])
        if a is None or b is None or a == b:
            out["contrast_not_flipped"].append(r["rid"])
        fa, fb = facts.get(t), facts.get(r["rid"])
        if fa and fb:
            changed = sorted(k for k in set(fa[0]) | set(fb[0]) if fa[0].get(k, "absent") != fb[0].get(k, "absent"))
            kind = f"{len(changed)} fact(s)" + (" + definition" if fa[1] != fb[1] else "")
            out["contrast_fact_changes"][kind] += 1
    for rel in rels:
        a, b = rel["a"], rel["b"]
        if a not in by or b not in by:
            out["unknown_rel"].append(rel)
            continue
        ya, yb = yes_of(a), yes_of(b)
        t = rel["type"]
        if t == "complement":
            out["complement"] += 1
            if ya is None or yb is None or ya == yb:
                out["complement_not_inverted"].append([a, b])
        elif t in ("equiv", "inv"):
            out[t] += 1
            if ya is None or ya != yb:
                out[f"{t}_changed"].append([a, b])
        else:
            out["unknown_rel"].append(rel)
        fa, fb = facts.get(a), facts.get(b)
        if fa and fb and fa[0] != fb[0]:
            out["fact_parity_broken"].append([a, b, t])
    out["contrast_fact_changes"] = dict(out["contrast_fact_changes"])
    return out


_OUTSIDE = re.compile(r"Under (?P<reg>[^,]+), (?:a|an) (?P<ent>[a-z]+) (?:that|who) (?P<vp>.+) is (?P<neg>not )?"
                      r"treated as (?P<term>(?:an? )?'[^']+')\.")


def outside_rules(row: dict, o: dict) -> list:
    """The outside-rule statements in the background ('Under <rule book>, a <entity> that ... is (not) treated as
    <term>.'), parsed to conditions. Used ONLY for the distractor sensitivity, never for the label."""
    doc = parse_state(row["state"])
    cat = CATS[o["pack"]]
    out = []
    for s in doc.background:
        for part in [s] if doc.fmt != "prose" else _SENT_SPLIT.split(s):
            m = _OUTSIDE.fullmatch(part)
            if m:
                out.append((parse_vp(cat, m.group("vp")), not m.group("neg")))
    return out


def sensitivity(rows: list, answers: dict) -> dict:
    """Rows whose decide2 answer changes under each alternative reading (or when a distractor is obeyed)."""
    alts = {"deem_no_proviso=overrides": {"deem_no_proviso": "overrides"},
            "unrecorded_negative=holds": {"unrecorded_negative": "holds"},
            "absent_attribute=not_established": {"absent_attribute": "not_established"}}
    out = {}
    for name, rd in alts.items():
        ch, follows = [], 0
        for r in rows:
            try:
                a2 = solve(r, rd)["answer"]
            except ParseError:
                a2 = None
            if a2 != answers.get(r["rid"]):
                ch.append(r["rid"])
                follows += a2 == r["gold"]
        out[name] = {"changed": len(ch), "gold_follows_alt": follows, "rids": ch[:40]}
    # distractor: obey the background's outside rule (an 'is treated as' rule as a deeming clause, an 'is not
    # treated as' rule as an exclusion). A reader who does this changes these answers.
    ch, n_with = [], 0
    for r in rows:
        if r["meta"]["qkind"] == "choice":
            continue
        try:
            o = solve(r)
            rules = outside_rules(r, o)
        except ParseError:
            continue
        if not rules:
            continue
        n_with += 1
        applies = o["applies"]
        for c, incl in rules:
            if c.holds(o["facts"]):
                applies = True if incl else False
        if applies != o["applies"]:
            ch.append(r["rid"])
    out["distractor:obey_outside_rule"] = {"rows_with_rule": n_with, "changed": len(ch), "rids": ch[:40]}
    return out


def reasons_report(rows: list) -> dict:
    """SPEC F6 / 8.3: no item may have two independent sufficient reasons. Counted under decide2's own reading."""
    two_yes, two_no, hist = [], [], Counter()
    for r in rows:
        try:
            o = solve(r)
        except ParseError:
            continue
        ry, rn = o["reasons"]
        hist[f"{o['kind']}:yes{ry}/no{rn}"] += 1
        if ry > 1:
            two_yes.append(r["rid"])
        if rn > 1:
            two_no.append(r["rid"])
    return {"histogram": dict(sorted(hist.items())), "two_reasons_yes": two_yes, "two_reasons_no": two_no}


def card_report(rows: list) -> dict:
    """The yes/no card must say what the question asks: is -> 'yes' = meets; not -> 'yes' = does not meet; judge ->
    'yes' = the record is the definition's; judge_n -> 'yes' = the opposite. Choice glosses: 'a requirement of' /
    'an exclusion in' the question's clause."""
    bad, n = [], 0
    for r in rows:
        try:
            q = parse_question(r["instructions"])
        except ParseError:
            continue
        card = card_of(r)
        if kind_of(r) == "yn":
            n += 1
            y = card["yes"]
            if q["family"] == "is":
                ok = (f" does not meet {q['clause']} as written" in f" {y}") if q["neg"] else (
                    f" meets {q['clause']} as written" in f" {y}" and " does not meet " not in f" {y}")
            else:
                ok = y.startswith(f"{q['clause']} gives the opposite") == q["neg"] and (
                    q["neg"] or y.startswith("the classification recorded in the "))
            if not ok:
                bad.append(r["rid"])
        elif kind_of(r) == "choice":
            for opt in r["options"]:
                g = card.get(opt, "")
                want = (f"a requirement of {q['clause']};" if opt.startswith("Requirement - ") else
                        f"an exclusion in {q['clause']};" if opt.startswith("Exclusion - ") else "every requirement")
                if not g.startswith(want):
                    bad.append(r["rid"])
                    break
    return {"yn_rows": n, "card_question_mismatch": bad}


def crosscheck_report(rows: list) -> dict:
    """decide2 reads the pack and format from the text; this compares them with meta (report only), and lists JB
    rows whose governing definition comes into force after a date fact or after the file was opened."""
    pack_bad, fmt_bad, jb_late = [], [], []
    for r in rows:
        try:
            o = solve(r)
        except ParseError:
            continue
        if o["pack"] != r["meta"]["pack"]:
            pack_bad.append(r["rid"])
        if o["fmt"] != r["meta"]["fmt"].split(":")[0]:
            fmt_bad.append(r["rid"])
        if o["kind"] == "jb":
            doc = parse_state(r["state"])
            dates = [v for v in o["facts"].values() if isinstance(v, dt.date)] + ([doc.opened] if doc.opened else [])
            if any(dd < o["in_force"] for dd in dates):
                jb_late.append(r["rid"])
    return {"pack_mismatch": pack_bad, "fmt_mismatch": fmt_bad, "jb_in_force_after_a_file_date": jb_late}


def _rel(p) -> str:
    p = Path(p).resolve()
    return str(p.relative_to(LEAN)) if p.is_relative_to(LEAN) else str(p)


def build_report() -> dict:
    import hashlib
    rep = {"tool": "golden_src/gen3/v3_def_literal.py", "key": KEY,
           "author": "builder A (independent of decide; never read dl_core / dl_sample / gen3_def_literal / dl_render)",
           "readings": DEFAULT_READINGS, "inputs": {}, "parts": {}}
    for part in ("train", "dev"):
        p = RAW / (f"{KEY}.jsonl" if part == "train" else f"dev/{KEY}.jsonl")
        rows, rels = load_rows(part), load_rels(part)
        rep["inputs"][part] = {"path": _rel(p), "rows": len(rows), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        ag = agreement(rows)
        by = {r["rid"]: r for r in rows}
        for d in ag["disagreements"]:
            d["diagnosis"] = diagnose(by[d["rid"]])
        rep["parts"][part] = {
            "rows": ag["rows"], "agree": ag["agree"], "disagree": ag["rows"] - ag["agree"], "rate": ag["rate"],
            "by_kind_qkind_view": ag["table"], "disagreements": ag["disagreements"],
            "structure": structure_under_decide2(rows, rels, ag["answers"]),
            "sensitivity": sensitivity(rows, ag["answers"]), "reasons": reasons_report(rows),
            "cards": card_report(rows), "crosscheck": crosscheck_report(rows)}
    return rep


def write_agreement(out_path: Path | None = None, manifest: bool = True) -> dict:
    """Writes yn2b/v3_def_literal_agreement.json (the SPEC 8.1 record for F6) and appends its sha256 to
    golden_src/gen3/MANIFEST_yn2b.jsonl. Reads the raw rows only; writes nothing under data/."""
    import hashlib
    out_path = Path(out_path or LEAN / "yn2b" / "v3_def_literal_agreement.json")
    rep = build_report()
    text = json.dumps(rep, indent=1, ensure_ascii=False, default=str) + "\n"
    out_path.write_text(text)
    if manifest:
        sys.path.insert(0, str(LEAN / "yn2b"))
        import yn2b_common as yc
        yc.manifest_append({"tool": "golden_src/gen3/v3_def_literal.py", "key": KEY, "part": "decide2_agreement",
                            "path": _rel(out_path), "rows": sum(v["rows"] for v in rep["parts"].values()),
                            "sha256": hashlib.sha256(text.encode()).hexdigest(), "inputs": rep["inputs"],
                            "agree": {k: [v["agree"], v["rows"]] for k, v in rep["parts"].items()}})
    return rep


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--quick", action="store_true", help="agreement only")
    ap.add_argument("--json", help="write the full report here (scratch path; never under data/)")
    ap.add_argument("--write", action="store_true",
                    help="write yn2b/v3_def_literal_agreement.json and append its sha256 to MANIFEST_yn2b.jsonl")
    a = ap.parse_args(argv)
    if a.write:
        rep = write_agreement()
    elif a.quick:
        rep = {"parts": {}}
        for part in ("train", "dev"):
            ag = agreement(load_rows(part))
            rep["parts"][part] = {k: v for k, v in ag.items() if k != "answers"}
            rep["parts"][part]["disagree"] = ag["rows"] - ag["agree"]
    else:
        rep = build_report()
    for part, v in rep["parts"].items():
        print(f"== {part}: {v['agree']}/{v['rows']} agree ({100 * v['rate']:.2f}%)")
        for d in v["disagreements"]:
            print("  DIS", d)
        if "structure" in v:
            st = v["structure"]
            print(f"  structure: contrast {st['contrast_pairs']} (not flipped {len(st['contrast_not_flipped'])}; "
                  f"changes {st['contrast_fact_changes']}), complement {st['complement']} (not inverted "
                  f"{len(st['complement_not_inverted'])}), equiv {st['equiv']} (changed {len(st['equiv_changed'])}), "
                  f"inv {st['inv']} (changed {len(st['inv_changed'])}), fact parity broken "
                  f"{len(st['fact_parity_broken'])}, unknown rels {len(st['unknown_rel'])}")
            for name, s in v["sensitivity"].items():
                print(f"  reading {name:36s} {json.dumps({k: x for k, x in s.items() if k != 'rids'})}")
            rr = v["reasons"]
            print(f"  two sufficient reasons: yes {len(rr['two_reasons_yes'])}, no {len(rr['two_reasons_no'])}; "
                  f"hist {rr['histogram']}")
            print(f"  cards: {v['cards']['yn_rows']} yes/no rows; mismatches {v['cards']['card_question_mismatch']}")
            print(f"  crosscheck: { {k: len(x) for k, x in v['crosscheck'].items()} }")
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str))
    return rep


if __name__ == "__main__":
    main()
