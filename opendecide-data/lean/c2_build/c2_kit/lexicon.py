"""c2_kit/lexicon.py: the operator lexicon registry and G-LEX (C2_DATA_SPEC 6.2 item 2, 6.3 G-LEX).

A lexicon form is one surface wording of one semantic id: "no more than {X}" -> cmp.le, "deny rules beat ask rules,
which beat allow rules" -> prec.P1, "at most {N} in any {M} window" -> win.rolling. Programs render forms into rows
(as clause slots); parsers read them back with the same registry. Because both directions share the table, the table
itself is checked from outside:

  unit test    every form, filled with the kind's sample values, parses back (alone and inside a sentence) to its own
               sem id and to the same slot values, and no form with a different sem id matches the same text
               (ambiguity). Forms use plain {X} / {X:form} placeholders only, separated by literal text.
  extraction   independent Haiku extractors read the filled form blind and pick its meaning from the kind's closed
               list (lexicon_items() builds the gold-free items; the chunker sends them). A form is ADMITTED only when
               its unit test passes and >= 2 distinct extractors (3 for kinds "precedence" and "window") all picked its
               sem id: 2/2 or 3/3. Any extractor that picks another meaning REJECTS the form for good (no re-vote).
  G-LEX        gate(form_ids): every form a row uses is admitted. Rows never use pending or rejected forms.

Question wordings are lexicon forms too (kind "question", sem question_sem(family, qform)): a wording is used only when
its own text is an admitted form whose meaning is the question form it claims (pipeline G-LEX check).
Antonym pairs (closed list) back the non-syntactic complements of the overlay (spec 4.1): declare_antonym(a, b).

  reg = LexiconRegistry("T01")
  reg.declare("cmp.le", "comparator", "less than or equal to the bound")
  f = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
  reg.unit_test(f.form_id)                      # True / False (problems in f.unit_problems)
  reg.record_extraction(f.form_id, "haiku:task:3", "cmp.le")
  reg.clause(f.form_id, bind={"X": "LIMIT"})    # a clause slot for a spec whose bound is slot LIMIT
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
from dataclasses import dataclass, field

from . import skin as K
from . import slots as S

KINDS = ("comparator", "precedence", "window", "temporal", "deontic", "confirmation", "status", "quantifier",
         "connective", "transition", "anchor", "question", "other")
STRICT_KINDS = ("precedence", "window")
SOURCES = ("claude", "haiku")


class LexiconError(ValueError):
    pass


def question_sem(family: str, qform: str) -> str:
    """The sem id a question wording's admitted form carries (kind "question"): q.<family>.<qform>."""
    return f"q.{family.lower()}.{qform}"


@dataclass(frozen=True)
class Sem:
    sem_id: str
    kind: str
    meaning: str


@dataclass
class LexForm:
    form_id: str
    sem_id: str
    kind: str
    text: str
    slots: tuple                         # ((name, kind), ...)
    source: str = "claude"
    family: str | None = None
    haiku_task_id: str | None = None
    haiku_prompt_sha: str | None = None
    held_out: bool = False
    extractions: list = field(default_factory=list)     # [(extractor_id, sem_id)]
    unit_ok: bool | None = None
    unit_problems: list = field(default_factory=list)

    @property
    def required(self) -> int:
        return 3 if self.kind in STRICT_KINDS else 2


@dataclass(frozen=True)
class LexMatch:
    sem_id: str
    form_id: str
    start: int
    end: int
    values: dict


def _norm_text(t: str) -> str:
    return " ".join(t.casefold().split())


def _params_by_kind(schema: dict | None) -> dict:
    """{kind: [params, ...]} from a {slot: (kind, params)} schema (all parameter sets a kind takes in this row)."""
    out: dict = {}
    for kind, params in (schema or {}).values():
        out.setdefault(kind, [])
        if params not in out[kind]:
            out[kind].append(params)
    return out


def _default_params(kind: str) -> list:
    seen = []
    for s in S.sample_slots(kind):
        if s.params not in seen:
            seen.append(s.params)
    return seen


class LexiconRegistry:
    def __init__(self, name: str = "shared"):
        self.name = name
        self.sems: dict = {}
        self.forms: dict = {}
        self.antonyms: set = set()
        self._rx: dict = {}

    # -------------------------------------------------------------------------------------------- building
    def declare(self, sem_id: str, kind: str, meaning: str) -> Sem:
        if kind not in KINDS:
            raise LexiconError(f"kind {kind!r} not in {KINDS}")
        if not re.fullmatch(r"[a-z][a-z0-9_]*(?:\.[A-Za-z0-9_]+)+", sem_id):
            raise LexiconError(f"sem id {sem_id!r} (dotted, e.g. cmp.le)")
        if sem_id in self.sems and (self.sems[sem_id].kind, self.sems[sem_id].meaning) != (kind, meaning):
            raise LexiconError(f"{sem_id} already declared differently")
        self.sems[sem_id] = Sem(sem_id, kind, meaning)
        return self.sems[sem_id]

    def add(self, text: str, sem_id: str, *, slots: dict | None = None, source: str = "claude",
            family: str | None = None, haiku_task_id: str | None = None, haiku_prompt_sha: str | None = None,
            held_out: bool = False) -> LexForm:
        if sem_id not in self.sems:
            raise LexiconError(f"declare {sem_id} before adding forms")
        if source not in SOURCES or (source == "haiku" and not (haiku_task_id and haiku_prompt_sha)):
            raise LexiconError("a Haiku form records its task id and prompt sha")
        if not text or text != text.strip() or "\n" in text:
            raise LexiconError(f"form text {text!r}: one trimmed line")
        bad = K.malformed(text)
        if bad:
            raise LexiconError(f"malformed placeholder(s) {bad}")
        phs = K.placeholders(text)
        slots = dict(slots or {})
        for p in phs:
            if p.mod or p.agree:
                raise LexiconError(f"lexicon forms use plain {{X}} / {{X:form}} placeholders only: {text!r}")
            if p.name not in slots or slots[p.name] not in S.KINDS or slots[p.name] == "clause":
                raise LexiconError(f"placeholder {p.name} needs a slot kind (not clause)")
        if set(slots) != {p.name for p in phs}:
            raise LexiconError("declared slots and placeholders differ")
        for a, b in zip(phs, phs[1:]):
            if not text[a.end:b.start].strip():
                raise LexiconError("two placeholders need literal text between them")
        if not re.sub(K.PH_RE, "", text).strip():
            raise LexiconError("a form needs literal words")
        nt = _norm_text(text)
        for f in self.forms.values():
            if _norm_text(f.text) == nt:
                raise LexiconError(f"duplicate form text (already {f.form_id})")
        fid = f"{sem_id}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"
        f = LexForm(fid, sem_id, self.sems[sem_id].kind, text, tuple(sorted(slots.items())), source, family,
                    haiku_task_id, haiku_prompt_sha, held_out)
        self.forms[fid] = f
        self._rx.clear()
        return f

    def declare_antonym(self, sem_a: str, sem_b: str) -> None:
        for s in (sem_a, sem_b):
            if s not in self.sems:
                raise LexiconError(f"undeclared sem {s}")
        if sem_a == sem_b:
            raise LexiconError("an antonym pair needs two sems")
        self.antonyms.add(frozenset((sem_a, sem_b)))

    def is_antonym(self, sem_a: str, sem_b: str) -> bool:
        return frozenset((sem_a, sem_b)) in self.antonyms

    # -------------------------------------------------------------------------------------------- rendering
    def render(self, form_id: str, values: dict, forms: dict | None = None) -> str:
        f = self.forms[form_id]
        return K.fill(f.text, {k: values[k] for k, _ in f.slots}, forms).text

    def clause(self, form_id: str, bind: dict | None = None) -> S.Slot:
        """A clause slot whose template refers to the spec's slots (bind: form slot -> spec slot)."""
        f = self.forms[form_id]
        bind = dict(bind or {})
        names = {k for k, _ in f.slots}
        if set(bind) != names:
            raise LexiconError(f"bind every form slot {sorted(names)}")
        tpl = K.PH_RE.sub(lambda m: "{" + bind[m.group("name")] + (f":{m.group('form')}" if m.group("form") else "")
                          + "}", f.text)
        return S.clause_slot(f.sem_id, form_id, tpl)

    # -------------------------------------------------------------------------------------------- parsing
    def _regex(self, f: LexForm, pbk: dict, anchored: bool):
        key = (f.form_id, json.dumps(sorted((k, [list(map(list, p)) for p in v]) for k, v in pbk.items()),
                                     default=str), anchored)
        if key in self._rx:
            return self._rx[key]
        kinds = dict(f.slots)
        parts, pos = [], 0
        for i, p in enumerate(K.placeholders(f.text)):
            lit = f.text[pos:p.start]
            parts.append(r"\s+".join(re.escape(w) for w in lit.split(" ")) if lit else "")
            psets = pbk.get(kinds[p.name]) or _default_params(kinds[p.name])
            alts = sorted({S.regex(kinds[p.name], p.form, ps) if p.form else S.any_regex(kinds[p.name], ps)
                           for ps in psets}, key=len, reverse=True)
            parts.append(f"(?P<v{i}>" + "|".join(alts) + ")")
            pos = p.end
        tail = f.text[pos:]
        parts.append(r"\s+".join(re.escape(w) for w in tail.split(" ")) if tail else "")
        body = "".join(parts)
        rx = re.compile(body if anchored else r"(?<![\w])" + body + r"(?![\w])", re.I)
        self._rx[key] = rx
        return rx

    def _values(self, f: LexForm, m, pbk: dict) -> dict:
        kinds = dict(f.slots)
        out = {}
        for i, p in enumerate(K.placeholders(f.text)):
            raw = m.group(f"v{i}")
            vals = []
            for ps in pbk.get(kinds[p.name]) or _default_params(kinds[p.name]):
                try:
                    v = S.parse(kinds[p.name], raw, ps, p.form)
                except S.SlotError:
                    continue
                if v not in vals:
                    vals.append(v)
            if len(vals) != 1:
                raise LexiconError(f"{f.form_id}: slot {p.name} text {raw!r} reads {len(vals)} ways")
            out[p.name] = vals[0]
        return out

    def parse_exact(self, text: str, schema: dict | None = None, *, admitted_only: bool = False) -> tuple:
        """(sem_id, form_id, {form slot: python value}) for a text that is exactly one form. schema: the row's
        {slot: (kind, params)}, used for the typed patterns (currency, units, category sets)."""
        pbk = _params_by_kind(schema)
        hits = []
        for f in self.forms.values():
            if admitted_only and self.status(f.form_id) != "admitted":
                continue
            m = self._regex(f, pbk, True).fullmatch(text.strip())
            if m:
                try:
                    hits.append((f, self._values(f, m, pbk)))
                except LexiconError:
                    continue
        sems = {f.sem_id for f, _ in hits}
        if len(sems) != 1:
            raise LexiconError(f"{text!r} matches {len(sems)} meanings")
        hits.sort(key=lambda h: -len(h[0].text))
        f, vals = hits[0]
        return f.sem_id, f.form_id, vals

    def scan(self, text: str, schema: dict | None = None, *, kinds: tuple | None = None,
             admitted_only: bool = False) -> list:
        """Every form occurrence in a longer text: leftmost, then longest; non-overlapping."""
        pbk = _params_by_kind(schema)
        cands = []
        for f in self.forms.values():
            if kinds and f.kind not in kinds:
                continue
            if admitted_only and self.status(f.form_id) != "admitted":
                continue
            for m in self._regex(f, pbk, False).finditer(text):
                try:
                    vals = self._values(f, m, pbk)
                except LexiconError:
                    continue
                cands.append(LexMatch(f.sem_id, f.form_id, m.start(), m.end(), vals))
        cands.sort(key=lambda c: (c.start, -(c.end - c.start)))
        out, last = [], -1
        for c in cands:
            if c.start >= last:
                same = [d for d in cands if (d.start, d.end) == (c.start, c.end) and d.sem_id != c.sem_id]
                if same:
                    raise LexiconError(f"ambiguous span {text[c.start:c.end]!r}: {c.sem_id} / {same[0].sem_id}")
                out.append(c)
                last = c.end
        return out

    # -------------------------------------------------------------------------------------------- G-LEX
    def _samples(self, f: LexForm) -> list:
        kinds = [k for _, k in f.slots]
        names = [n for n, _ in f.slots]
        pools = [S.sample_slots(k)[:3] for k in kinds]
        combos = list(itertools.product(*pools))[:12] or [()]
        return [dict(zip(names, c)) for c in combos]

    def unit_test(self, form_id: str) -> bool:
        f = self.forms[form_id]
        probs = []
        for vals in self._samples(f):
            schema = {k: v.schema for k, v in vals.items()}
            try:
                txt = self.render(form_id, vals)
            except (K.RenderError, S.SlotError) as e:
                probs.append(f"render: {e}")
                continue
            want = {k: v.value for k, v in vals.items()}
            try:
                sem, _, got = self.parse_exact(txt, schema)
                if sem != f.sem_id:
                    probs.append(f"{txt!r} parses as {sem}")
                elif got != want:
                    probs.append(f"{txt!r} values {got} != {want}")
            except LexiconError as e:
                probs.append(str(e))
            sentence = f"Note: {txt}. Thanks."
            try:
                ms = self.scan(sentence, schema)
                if len(ms) != 1 or ms[0].sem_id != f.sem_id or ms[0].values != want:
                    probs.append(f"in a sentence {sentence!r} scans as {[(m.sem_id, m.values) for m in ms]}")
            except LexiconError as e:
                probs.append(str(e))
        f.unit_ok = not probs
        f.unit_problems = probs
        return f.unit_ok

    def unit_test_all(self) -> dict:
        return {fid: self.unit_test(fid) for fid in sorted(self.forms)}

    def record_extraction(self, form_id: str, extractor_id: str, sem_id: str | None) -> None:
        f = self.forms[form_id]
        if any(e == extractor_id for e, _ in f.extractions):
            raise LexiconError(f"{extractor_id} already extracted {form_id} (extractors must be independent)")
        f.extractions.append((extractor_id, sem_id))

    def status(self, form_id: str) -> str:
        f = self.forms[form_id]
        if any(s != f.sem_id for _, s in f.extractions):
            return "rejected"
        if f.unit_ok is None:
            return "untested"
        if not f.unit_ok:
            return "unit_fail"
        if len({e for e, _ in f.extractions}) >= f.required:
            return "admitted"
        return "pending"

    def gate(self, used_form_ids=None) -> dict:
        """G-LEX: every used form is admitted (default: every form in the registry)."""
        ids = sorted(self.forms if used_form_ids is None else set(used_form_ids))
        unknown = [i for i in ids if i not in self.forms]
        per = {i: self.status(i) for i in ids if i in self.forms}
        bad = {i: s for i, s in per.items() if s != "admitted"}
        return {"gate": "G-LEX", "registry": self.name, "n_forms": len(per), "unknown": unknown,
                "status_counts": {s: sum(1 for v in per.values() if v == s) for s in sorted(set(per.values()))},
                "not_admitted": bad, "pass": not bad and not unknown}

    def lexicon_items(self, form_ids=None, *, seed: str = "glex") -> list:
        """Gold-free extraction items (internal id, item) for the chunker's 'extract_lex' kind: the filled form and
        the meanings of its kind, in a seeded order. The answer is a meaning text; meaning_to_sem() maps it back."""
        out = []
        for fid in sorted(self.forms if form_ids is None else form_ids):
            f = self.forms[fid]
            vals = self._samples(f)[0]
            txt = self.render(fid, vals)
            mean = sorted((s.meaning for s in self.sems.values() if s.kind == f.kind),
                          key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
            out.append((fid, {"text": txt, "choices": mean}))
        return out

    def meaning_to_sem(self, kind: str, meaning: str) -> str | None:
        hits = [s.sem_id for s in self.sems.values() if s.kind == kind and s.meaning == meaning]
        return hits[0] if len(hits) == 1 else None

    # -------------------------------------------------------------------------------------------- persistence
    def to_json(self) -> dict:
        return {"name": self.name,
                "sems": [{"sem_id": s.sem_id, "kind": s.kind, "meaning": s.meaning}
                         for s in sorted(self.sems.values(), key=lambda s: s.sem_id)],
                "forms": [{"form_id": f.form_id, "sem_id": f.sem_id, "kind": f.kind, "text": f.text,
                           "slots": dict(f.slots), "source": f.source, "family": f.family,
                           "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha,
                           "held_out": f.held_out, "extractions": [list(e) for e in f.extractions],
                           "unit_ok": f.unit_ok, "status": self.status(f.form_id)}
                          for f in sorted(self.forms.values(), key=lambda f: f.form_id)],
                "antonyms": sorted(sorted(p) for p in self.antonyms)}

    @classmethod
    def from_json(cls, o: dict) -> "LexiconRegistry":
        r = cls(o["name"])
        for s in o["sems"]:
            r.declare(s["sem_id"], s["kind"], s["meaning"])
        for x in o["forms"]:
            f = r.add(x["text"], x["sem_id"], slots=x["slots"], source=x["source"], family=x["family"],
                      haiku_task_id=x["haiku_task_id"], haiku_prompt_sha=x["haiku_prompt_sha"], held_out=x["held_out"])
            if f.form_id != x["form_id"]:
                raise LexiconError(f"form id drift {x['form_id']} -> {f.form_id}")
            f.extractions = [tuple(e) for e in x["extractions"]]
        for a, b in o["antonyms"]:
            r.declare_antonym(a, b)
        r.unit_test_all()
        return r

    def sha256(self) -> str:
        return hashlib.sha256(json.dumps(self.to_json(), sort_keys=True).encode()).hexdigest()
