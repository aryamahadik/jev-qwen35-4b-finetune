"""v3_nested_negation (decide2, v2): an independent parse-back of every F7 'nested negation' gold.

Written WITHOUT reading the decision / LF code of gen3_nested_negation.py. Inputs used, and nothing else:
  * the RENDERED row: instructions, card, options, state, qtype;
  * human labels of the base texts, found by the row's meta.derived_from ids (golden_train.jsonl, raw/*.jsonl, or the
    old civil_comments / toxic_conv rows matched by text) or, for devx, by meta.orig;
  * for invented records, the record fields printed in the state;
  * for devx invented records and free-text choice options, a small fact table read off the state by the decide2
    author (DEVX_FACTS below; every entry is a plain reading of the printed state).
It never reads gold, lf, truth_P, depth, cues, rung, role, frame, ptype, ctype or text_gold, and it never imports the
generator or its lexicon (word lists in nn_lexicon.py and f7_defs.json were READ by the author to know which wordings
exist; every polarity below is the author's own reading of the English). The sidecar is opened only by the CLI, after
every prediction is made, to tally agreement by rung and checklist item.

devx (free-form rows by a separate author) is not template text, so its logical forms were written by the decide2
author from the rendered rows alone (yn2b/f7_devx_decide2_lf.json, one LF per row plus a fact table per invented
record, with each fact quoted from the state); the program evaluates them against the human labels.

Ambiguity (arbiter round 3, yn2b/F7_OBJECTIONS.md A3 / A4): a row whose English has two readings with different
golds is refused (class Ambiguous, counted as unparsed, so precheck 2.3 fails) instead of being read one way:
  A3  universal / negative exceptives ('no X other than X 4 ...') when the excepted item lacks the property;
  A4  'the opposite / reverse / contrary of a claim' on a universal batch claim over mixed items, unless the card
      defines the word as plain denial.
devx LFs use [AMBIG, note, reading A, reading B] for the same two constructions.
Stale devx LFs (arbiter round 4): the devx table binds each LF to the sha256 of the text it was written from
(text_sha256); a devx row whose state / instructions / card / options differ is refused (ParseError).

Outputs: yn2b/f7_decide2_preds.jsonl ({id, gold} for f7_precheck --decide2-preds) and yn2b/f7_decide2_report.json
(agreement per file / rung / kind / checklist item, every disagreement and unparsed row, merged with
yn2b/f7_decide2_diagnoses.json).

Method. The instruction is cleaned of side clauses that cannot change the answer (whether or not / even if /
regardless of whether, format sentences, look-alike prefixes), then parsed top-down:
  answer mapping  ('answer no if X; otherwise answer yes')  -> gold = not X
  card key        ('Claim: X. Answer by the card's key')    -> gold = truth of the card's Yes line
  question frame  ('Is it false that X?', 'Does the report fail to show that X?', 'A log entry states that X. Should
                   that entry be dismissed?', ...)          -> a chain of NOT / identity operators over X
  atom            (label fit, term membership, quantifier over a batch, record predicate, deontic rule, triage note)
Each step is a regex the author wrote for one English construction plus its polarity. When the card also carries
Yes / No lines, both lines are evaluated as statements and must agree with the question (cross-check).

API
  ctx = Ctx(lean_dir)                       # loads base labels lazily
  decide2_row(row, ctx) -> (pred, note)     # pred: 0/1 (noul), option string (choice) or None (could not parse)
CLI
  python v3_nested_negation.py [--out yn2b/f7_decide2_preds.jsonl] [--report yn2b/f7_decide2_report.json]
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
DV = LEAN / "data" / "v14_parts"


class ParseError(Exception):
    pass


class Ambiguous(ParseError):
    """arbiter round 3 (yn2b/F7_OBJECTIONS.md, A3 / A4): the row has two readings with different golds. decide2 refuses
    such a row (it is counted as unparsed, so precheck 2.3 fails) instead of silently picking one reading. Never
    swallowed by a frame / peel fallback."""


# arbiter round 3, A4: frame words whose plain-denial reading and contrary reading ('the opposite of none is all')
# differ on a universal claim over a mixed batch; accepted only when the card defines the word as plain denial
FRAME_WORD_RX = re.compile(r"\b(opposite|reverse|contrary)\b")


def norm(s: str) -> str:
    s = (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def low(s: str) -> str:
    return norm(s).lower()


# =============================================================================================== base labels
# Label renames between a base dataset and the F7 card (the author matched the two definitions line by line).
ALIAS = {
    "product": "named product", "creative work": "title of a work",                       # wnut17
    "treatment": "treatment options", "prevention": "prevention steps",                   # medquad
    "illegal dumping": "dumped debris",                                                   # sd311
    "check-worthy factual claim": "check-worthy claim",                                   # claimbuster
    "unimportant factual statement": "minor factual remark",
    "non-factual statement": "opinion or question",
    # SaferProducts 8-step scale -> the card's 3 tiers, read off the tier definitions:
    #   slight = at most a small injury with neither first aid nor medical care;
    #   middling = first aid by a lay person or seen by a doctor / nurse / clinic outside an ER;
    #   grave = ER treatment, hospital admission or death.
    "no incident, no injury": "slight", "incident, but no injury": "slight",
    "injury, no first aid or medical care": "slight",
    "injury, first aid by a non-medical person": "middling", "injury, seen by a medical professional": "middling",
    "injury, emergency department treatment": "grave", "injury, hospital admission": "grave", "death": "grave",
}


def task_of_instruction(instr: str) -> str | None:
    """Which yes/no property a base row's question asks about (its gold is about that property)."""
    t = low(instr)
    if "actually injured" in t:
        return "injury"
    if "caught fire" in t:
        return "fire"
    if "involved in a crash" in t:
        return "crash"
    if "acceptable according to common social norms" in t:
        return "acceptable"
    if "find at least one option that meets everything" in t:
        return "found"
    if "supported by the knowledge snippet" in t:
        return "faithful"
    if "assert anything that the knowledge snippet does not support" in t:
        return "unfaithful"
    return None


def old_key(state: str) -> str:
    """The comment body of an old civil / toxic row: JSON wrapper and header line removed, whitespace normalised."""
    t = state or ""
    if t.lstrip().startswith("{"):
        try:
            t = json.loads(t).get("content", t)
        except (ValueError, AttributeError):
            m = re.search(r'"content": "(.*?)(?:"\s*[,}]|$)', t, re.S)
            if m:
                t = m.group(1).replace("\\n", "\n").replace('\\"', '"')
    if re.match(r"^[A-Za-z ]+:\n", t):
        t = t.split("\n", 1)[1]
    return norm(t)


class Ctx:
    """Base-row lookups (human labels only)."""

    def __init__(self, lean: Path = LEAN):
        self.lean = Path(lean)
        self.dv = self.lean / "data" / "v14_parts"
        self._golden = None
        self._raw = {}
        self._old_text = None
        self._old_group = None
        self._old_group_text = None

    # --- golden_train rows by id
    def golden(self, rid):
        if self._golden is None:
            self._golden = {}
            with open(self.dv / "golden_train.jsonl", encoding="utf-8") as f:
                for line in f:
                    r = json.loads(line)
                    self._golden[r["id"]] = r
        return self._golden.get(rid)

    def raw(self, key, rid):
        if key not in self._raw:
            p = self.dv / "raw" / f"{key}.jsonl"
            d = {}
            if p.exists():
                with open(p, encoding="utf-8") as f:
                    for line in f:
                        r = json.loads(line)
                        d[r["rid"]] = r
            self._raw[key] = d
        return self._raw[key].get(rid)

    def _load_old(self):
        """Old civil_comments / toxic_conv CHOICE rows (human toxic / not-toxic labels), keyed by comment text and group.
        Symbol labels (Label-J ...) are read through the row's own card definition."""
        self._old_text, self._old_group = {}, {}
        self._old_group_text = {}
        for fn in ("train_v05.jsonl", "train_v06.jsonl", "train_v07.jsonl", "train_2b.jsonl", "train_v11.jsonl",
                   "train_v13t.jsonl", "inj_v2.jsonl"):
            p = self.lean / "data" / fn
            if not p.exists():
                continue
            with open(p, encoding="utf-8") as f:
                for line in f:
                    if '"civil_comments"' not in line and '"toxic_conv"' not in line:
                        continue
                    r = json.loads(line)
                    if r.get("source") not in ("civil_comments", "toxic_conv") or r.get("qtype") != "choice":
                        continue
                    opts = r.get("options") or []
                    if sorted(opts) == ["not toxic", "toxic"]:
                        lab = r["gold"] == "toxic"
                    else:
                        d = dict(re.findall(r"^- ([^:]+): (.*)$", r.get("card") or "", re.M)).get(r["gold"], "").lower()
                        if re.match(r"(?:a comment is not toxic|the comment stays civil|the comment is civil)", d):
                            lab = False
                        elif re.match(r"(?:a comment is toxic|the comment is rude)", d):
                            lab = True
                        else:
                            continue
                    self._old_group_text.setdefault(r.get("group_id"), set()).add(old_key(r["state"]))
                    for k, store in ((old_key(r["state"]), self._old_text), (r.get("group_id"), self._old_group)):
                        if k in store and store[k] != lab:
                            store[k] = "CONFLICT"
                        else:
                            store[k] = lab
        return self._old_text, self._old_group

    def old_by_text(self, text):
        if self._old_text is None:
            self._load_old()
        t = old_key(text)
        if t in self._old_text:
            return self._old_text[t]
        # the base comment can sit inside extra text (some old rows carry an added line); longest contained match
        best = None
        for k, v in self._old_text.items():
            if k and len(k) >= 20 and (k in t or (len(t) >= 20 and t in k)) and (best is None or len(k) > len(best[0])):
                best = (k, v)
        if best is not None:
            self.contained_hits = getattr(self, "contained_hits", 0) + 1
        return best[1] if best else None

    def old_by_group(self, gid):
        if self._old_group is None:
            self._load_old()
        return self._old_group.get(gid)

    # --- one human label for a base reference; returns dict(kind=label|prop, label=..., task=..., val=bool)
    def base(self, ref, text=None):
        if ref.startswith("raw:"):
            _, key, rid = ref.split(":", 2)
            r = self.raw(key, rid)
            if r is None:
                return None
            if key == "nhtsa_complaints":
                task = rid.rsplit("_", 1)[-1]
                return dict(kind="prop", task=task, val=r["gold"] == "yes", text=r["state"])
            if key in ("faithdial", "multiwoz21_sysacts"):
                task = task_of_instruction(r["instructions"])
                v = r["gold"] == "yes"
                if task == "unfaithful":
                    task, v = "faithful", not v
                return dict(kind="prop", task=task, val=v, text=r["state"])
            g = r["gold"]
            return dict(kind="label", label=ALIAS.get(g.lower(), g.lower()), text=r["state"])
        if ref.startswith("old:"):
            if text is not None and re.match(r"^[A-Za-z ]+:\n", text):
                text = text.split("\n", 1)[1]
            v = self.old_by_text(text) if text is not None else None
            if v is None or v == "CONFLICT":
                return None
            return dict(kind="prop", task="toxic", val=v, text=text)
        if ref.startswith("g:civil:") or ref.startswith("g:toxconv:"):
            v = self.old_by_group(ref)
            if v is None or v == "CONFLICT":
                return None
            return dict(kind="prop", task="toxic", val=v)
        r = self.golden(ref)
        if r is None:
            r2 = self.raw("saferproducts_severity", ref) or self.raw("wiki_help_routing", ref)
            if r2 is None:
                return None
            return dict(kind="label", label=ALIAS.get(r2["gold"].lower(), r2["gold"].lower()), text=r2["state"])
        if r["qtype"] == "choice":
            return dict(kind="label", label=ALIAS.get(r["gold"].lower(), r["gold"].lower()), text=r["state"])
        task = task_of_instruction(r["instructions"])
        v = r["gold"] in (1, "1", "yes", True)
        if task == "unfaithful":
            task, v = "faithful", not v
        return dict(kind="prop", task=task, val=v, text=r["state"])


# =============================================================================================== instruction cleaning
# Side material that cannot change the answer. Each pattern is a whole sentence (dropped) or a clause (cut out).
NEUTRAL_SENTENCES = [
    r"(?:an informal tone|non-standard spelling|jargon-free wording|careless typing) is fine",
    r"an? [a-z\- ]+ that (?:fails to name its writer|lacks a heading|omits its date) can still be judged",
    r"do not use outside knowledge", r"use no outside knowledge", r"never rely on facts from outside the {D}",
    r"nothing outside the {D} and the card counts", r"answer without outside facts",
    r"disregard anything outside the {D}", r"set unrelated details aside",
    r"read the definitions as one uniform set", r"treat the {D} as a single unit",
    r"notably, the card defines every term used here",
    r"answer from the {D} and the card alone", r"use the card's yes/no lines",
    # provenance sentences inside the reverse / contrary frames (who wrote the claim)
    r"the claim was written by an intake clerk", r"the claim comes from an intake form",
    r"that claim was copied from a tracking sheet", r"the claim was logged by a desk clerk",
    # devx format instructions
    r"treat [^.?]+ as normal", r"disregard (?:the timestamps|the link's address|[^.?]{0,60})",
    r"read not only the first line but also the rest of the [a-z ]+",
    r"ignore [^.?]+",
]
PREFIXES = [
    r"under the card's definitions, ", r"going by the displayed {D}, ", r"the {D} may be short; nonetheless, ",
    r"based on the {D}, ", r"judging only by the {D}, ", r"going by the card's definitions, ", r"going by the {D}, ",
    r"reading the card first, ", r"according to the {D}, ",
]
# conditional side clauses: 'even if ...', 'whether or not ...', 'regardless of whether ...' (no comma inside)
SIDE_CLAUSE = r"(?:even if|whether or not|regardless of whether) [^,;?]+?, "
SUFFIXES = [
    r", not using outside knowledge", r", using no outside knowledge", r", never relying on outside facts",
    r", with nothing outside the {D} counting", r", without outside facts", r", if you disregard anything outside the {D}",
    r", with unrelated details set aside", r", whatever its [a-z\- ]+", r", with [a-z\- ]+ being fine",
    r", even when an? {D} (?:fails to name its writer|lacks a heading)",
]
DOC_NOUNS = ["request", "report", "passage", "sentence", "post", "dialogue", "message", "complaint", "comment",
             "action", "batch", "ticket", "record", "text", "chat", "log", "note", "form", "sheet", "email"]


def doc_alt(extra=()):
    nouns = set(DOC_NOUNS) | {low(x) for x in extra if x}
    return "(?:" + "|".join(re.escape(x) for x in sorted(nouns, key=len, reverse=True)) + ")"


def split_sentences(t: str):
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Za-z'\"(])", t.strip())
    return [p.strip() for p in parts if p.strip()]


def clean(text: str, D: str) -> str:
    """Lowercased text with side material removed; sentences keep their final punctuation."""
    out = []
    for s in split_sentences(low(text)):
        body = s.rstrip(".?!")
        punct = s[len(body):] or "."
        if any(re.fullmatch(p.replace("{D}", D), body) for p in NEUTRAL_SENTENCES):
            continue
        changed = True
        while changed:
            changed = False
            for p in PREFIXES:
                m = re.match(p.replace("{D}", D), body)
                if m:
                    body = body[m.end():]
                    changed = True
            m = re.match(SIDE_CLAUSE, body)
            if m:
                body = body[m.end():]
                changed = True
            for p in SUFFIXES:
                m = re.search(p.replace("{D}", D) + r"$", body)
                if m:
                    body = body[:m.start()]
                    changed = True
        # a side clause after a leading clause: 'X, even if Y, Z' / 'say no when X, even if Y, and ...'
        body = re.sub(r", " + SIDE_CLAUSE, ", ", body)
        body = re.sub(r"; " + SIDE_CLAUSE, "; ", body)
        if any(re.fullmatch(p.replace("{D}", D), body) for p in NEUTRAL_SENTENCES):
            continue
        if body:
            out.append(body + punct[:1])
    return " ".join(out)


# =============================================================================================== frames
# (pattern, polarity): +1 = the frame asserts X, -1 = the frame asserts not-X. {X} = the embedded claim, {D} = the
# document noun. Statement forms (used for card key lines and nested frames) and question forms are both listed.
POS, NEG = 1, -1
STATEMENT_FRAMES = [
    # truth
    ("it is true that {X}", POS), ("this is true of the {D}: {X}", POS), ("this is untrue of the {D}: {X}", NEG),
    ("it is a fair summary of the {D} that {X}", POS), ("it is an unfair summary of the {D} that {X}", NEG),
    ("it holds that {X}", POS), ("it fails to hold that {X}", NEG), ("it does not hold that {X}", NEG),
    ("one can say, from the {D}, that {X}", POS), ("one cannot say, from the {D}, that {X}", NEG),
    ("it is not so that {X}", NEG), ("it is far from true that {X}", NEG),
    # falsity
    ("it is false that {X}", NEG), ("it is untrue that {X}", NEG), ("it would be false to say that {X}", NEG),
    ("it would be true to say that {X}", POS), ("the claim that {X} is false", NEG), ("the claim that {X} is true", POS),
    ("the {D} shows that the following is not the case: {X}", NEG), ("the {D} shows that the following holds: {X}", POS),
    ("it is untrue, going by the {D}, that {X}", NEG), ("it is true, going by the {D}, that {X}", POS),
    ("a careful reader would judge that the following is not the case: {X}", NEG),
    ("a careful reader would judge that the following holds: {X}", POS),
    # support
    ("the {D} supports the claim that {X}", POS), ("the {D} gives the claim that {X} no support", NEG),
    ("the claim that {X} is borne out by the {D}", POS), ("the claim that {X} is left unproven by the {D}", NEG),
    ("the {D} confirms that {X}", POS), ("the {D} leaves it unconfirmed that {X}", NEG),
    ("the {D} bears out the claim that {X}", POS), ("the {D} leaves the claim that {X} unproven", NEG),
    ("there is clear support in the {D} for the claim that {X}", POS),
    ("the {D} holds no clear support for the claim that {X}", NEG),
    # refute
    ("the {D} refutes the claim that {X}", NEG), ("the {D} leaves the claim that {X} standing", POS),
    ("the {D} contradicts the claim that {X}", NEG), ("the {D} is consistent with the claim that {X}", POS),
    ("the claim that {X} is refuted by the {D}", NEG), ("the claim that {X} stands, given the {D}", POS),
    ("the details of the {D} contradict the claim that {X}", NEG),
    ("the details of the {D} are consistent with the claim that {X}", POS),
    ("the claim that {X} is contradicted by the {D}", NEG), ("the claim that {X} is consistent with the {D}", POS),
    # unfounded
    ("the claim that {X} is unsupported by the {D}", NEG), ("the claim that {X} is supported by the {D}", POS),
    ("the claim that {X} is unfounded", NEG), ("the claim that {X} is well founded", POS),
    ("it is baseless to claim that {X}", NEG), ("it is well grounded to claim that {X}", POS),
    ("the claim that {X} would be unfounded, judging by the {D}", NEG),
    ("the claim that {X} would be well founded, judging by the {D}", POS),
    ("the {D} leaves the claim that {X} unsupported", NEG),
    ("the claim that {X} is baseless", NEG), ("the claim that {X} is well grounded", POS),
    # careful reader
    ("a careful reader should accept the claim that {X}", POS), ("a careful reader should set the claim that {X} aside", NEG),
    ("a careful reader should reject the claim that {X}", NEG), ("a careful reader should dismiss the claim that {X}", NEG),
    ("a careful reader would dispute the claim that {X}", NEG), ("a careful reader would accept the claim that {X}", POS),
    ("a careful reader would deny that {X}", NEG), ("a careful reader would grant that {X}", POS),
    ("a careful reader would sign off on the claim that {X}", POS),
    ("a careful reader would hold off on the claim that {X}", NEG),
    ("a careful reader would reject the claim that {X}", NEG), ("a careful reader would dispute that {X}", NEG),
    # fails to show / no support
    ("the {D} fails to show that {X}", NEG), ("the {D} shows that {X}", POS),
    ("the {D} fails to support the claim that {X}", NEG),
    ("the {D} fails to establish that {X}", NEG), ("the {D} establishes that {X}", POS),
    ("the {D} fails to bear out the claim that {X}", NEG),
    ("the {D} gives no support to the claim that {X}", NEG), ("the {D} gives support to the claim that {X}", POS),
    ("nothing in the {D} supports the claim that {X}", NEG), ("something in the {D} supports the claim that {X}", POS),
    ("there is no sign in the {D} that {X}", NEG), ("there is a clear sign in the {D} that {X}", POS),
    ("the {D} offers no grounds for the claim that {X}", NEG), ("the {D} offers grounds for the claim that {X}", POS),
    ("the {D} never states that {X}", NEG), ("the {D} states that {X}", POS),
    ("the {D} says nothing in favour of the claim that {X}", NEG),
    ("the {D} says something in favour of the claim that {X}", POS),
    # notes and entries
    ("the {D} bears out the note that {X}", POS), ("the {D} leaves the note that {X} unproven", NEG),
    ("the {D} contradicts the note that {X}", NEG), ("the {D} is consistent with the note that {X}", POS),
    ("the {D} refutes the note that {X}", NEG), ("the {D} leaves the note that {X} standing", POS),
    ("the note that {X} is false", NEG), ("the note that {X} is true", POS),
    ("the log entry that {X} should be dismissed", NEG), ("the log entry that {X} should be kept", POS),
    ("the {D} refutes the log entry that {X}", NEG), ("the {D} leaves the log entry that {X} standing", POS),
    ("the log entry that {X} is untrue", NEG), ("the log entry that {X} is true", POS),
    ("the clerk's entry that {X} is borne out by the {D}", POS),
    ("the clerk's entry that {X} is left unproven by the {D}", NEG),
    ("the clerk's entry that {X} is unfounded", NEG), ("the clerk's entry that {X} is well founded", POS),
    # reverse / opposite / negation / contrary of the claim
    ("the {D} supports the reverse of the claim that {X}", NEG),
    ("the {D} gives the reverse of the claim that {X} no support", POS),
    ("the opposite of this claim is true of the {D}: {X}", NEG), ("the opposite of this claim is untrue of the {D}: {X}", POS),
    ("the {D} bears out the negation of the claim that {X}", NEG),
    ("the {D} leaves the negation of the claim that {X} unproven", POS),
    ("the {D} bears out the opposite of this claim: {X}", NEG),
    ("the {D} leaves the opposite of this claim unproven: {X}", POS),
    ("the negation of the claim that {X} is true of the {D}", NEG),
    ("the negation of the claim that {X} is untrue of the {D}", POS),
    ("the reverse of the claim that {X} is true of the {D}", NEG),
    ("the reverse of the claim that {X} is untrue of the {D}", POS),
    ("the {D} bears out the contrary of the claim that {X}", NEG),
    ("the {D} leaves the contrary of the claim that {X} unproven", POS),
    ("the contrary of the claim that {X} is true of the {D}", NEG),
    ("the contrary of the claim that {X} is untrue of the {D}", POS),
    ("the contrary of the claim that {X} is groundless", POS),
    ("the contrary of the claim that {X} is well grounded", NEG),
    # verdict / audit (held-out wordings)
    ("a verdict that {X} would stand", POS), ("a verdict that {X} would fall", NEG),
    ("a review panel would overturn the finding that {X}", NEG), ("a review panel would uphold the finding that {X}", POS),
    ("an appeals clerk would rebut the finding that {X}", NEG), ("an appeals clerk would uphold the finding that {X}", POS),
    ("the panel would veto a ruling that {X}", NEG), ("the panel would endorse a ruling that {X}", POS),
    ("the finding that {X} is groundless", NEG), ("the finding that {X} is well grounded", POS),
    ("the auditor would call the entry that {X} erroneous", NEG),
    ("the auditor would call the entry that {X} sound", POS),
    ("the entry that {X} is far from true", NEG), ("the entry that {X} is true", POS),
    ("the auditor would sign off the entry that {X} as sound", POS),
    ("the auditor would return the entry that {X} for rework", NEG),
    ("the entry that {X} is groundless", NEG), ("the entry that {X} is well grounded", POS),
    # the card's yes/no key lines (quoted claim)
    ('the claim "{X}" holds for this {D}', POS), ('the claim "{X}" fails for this {D}', NEG),
    ('the claim "{X}" is borne out by the {D}', POS), ('the claim "{X}" is left unproven by the {D}', NEG),
    ('the claim "{X}" fails to hold for this {D}', NEG), ('the claim "{X}" is false of this {D}', NEG),
    ('the claim "{X}" is true of this {D}', POS), ('the claim "{X}" holds for the {D}', POS),
]
QUESTION_FRAMES = [
    ("is it true that {X}", POS), ("is this true of the {D}: {X}", POS),
    ("is it a fair summary of the {D} that {X}", POS), ("does it hold that {X}", POS),
    ("can one say, from the {D}, that {X}", POS),
    ("is it false that {X}", NEG), ("is it untrue that {X}", NEG), ("would it be false to say that {X}", NEG),
    ("is the claim that {X} false", NEG), ("does the {D} show that the following is not the case: {X}", NEG),
    ("is it untrue, going by the {D}, that {X}", NEG),
    ("would a careful reader judge that the following is not the case: {X}", NEG),
    ("does the {D} support the claim that {X}", POS), ("is the claim that {X} borne out by the {D}", POS),
    ("does the {D} confirm that {X}", POS), ("does the {D} bear out the claim that {X}", POS),
    ("is there clear support in the {D} for the claim that {X}", POS),
    ("does the {D} refute the claim that {X}", NEG), ("does the {D} contradict the claim that {X}", NEG),
    ("is the claim that {X} refuted by the {D}", NEG), ("do the details of the {D} contradict the claim that {X}", NEG),
    ("is the claim that {X} contradicted by the {D}", NEG),
    ("is the claim that {X} unsupported by the {D}", NEG), ("is the claim that {X} unfounded", NEG),
    ("is it baseless to claim that {X}", NEG), ("would the claim that {X} be unfounded, judging by the {D}", NEG),
    ("does the {D} leave the claim that {X} unsupported", NEG), ("is the claim that {X} baseless", NEG),
    ("should a careful reader accept the claim that {X}", POS), ("should a careful reader reject the claim that {X}", NEG),
    ("should a careful reader dismiss the claim that {X}", NEG), ("would a careful reader dispute the claim that {X}", NEG),
    ("would a careful reader deny that {X}", NEG), ("would a careful reader sign off on the claim that {X}", POS),
    ("would a careful reader reject the claim that {X}", NEG), ("would a careful reader dispute that {X}", NEG),
    ("would a careful reader accept the claim that {X}", POS),
    ("does the {D} fail to show that {X}", NEG), ("does the {D} fail to support the claim that {X}", NEG),
    ("does the {D} fail to establish that {X}", NEG), ("does the {D} fail to bear out the claim that {X}", NEG),
    ("does the {D} give no support to the claim that {X}", NEG),
    ("does nothing in the {D} support the claim that {X}", NEG), ("is there no sign in the {D} that {X}", NEG),
    ("does the {D} offer no grounds for the claim that {X}", NEG), ("does the {D} never state that {X}", NEG),
    ("does the {D} say nothing in favour of the claim that {X}", NEG),
    ("would a verdict that {X} stand", POS), ("would a review panel overturn the finding that {X}", NEG),
    ("would an appeals clerk rebut the finding that {X}", NEG), ("would the panel veto a ruling that {X}", NEG),
    ("is the finding that {X} groundless", NEG),
]
# two- or three-sentence frames: a setup sentence that introduces X, then a question about it.
SETUP_FRAMES = [
    # (setup, question, polarity)
    ("a note says that {X}", "does the {D} bear out that note", POS),
    ("a note says that {X}", "does the {D} contradict that note", NEG),
    ("a note says that {X}", "is that note false", NEG),
    ("a log entry states that {X}", "should that entry be dismissed", NEG),
    ("a log entry states that {X}", "does the {D} refute that entry", NEG),
    ("a log entry states that {X}", "is that entry untrue", NEG),
    ("a clerk wrote that {X}", "is that entry borne out by the {D}", POS),
    ("a clerk wrote that {X}", "is that entry unfounded", NEG),
    ("an auditor checks the entry that {X}", "would the auditor call that entry erroneous", NEG),
    ("an auditor checks the entry that {X}", "is that entry far from true", NEG),
    ("an auditor checks the entry that {X}", "would the auditor sign it off as sound", POS),
    ("an auditor checks the entry that {X}", "is the entry groundless", NEG),
]
# operator sentences that turn 'the claim' into its negation, then 'Claim: X.', then a question about the result
REVERSE_OPS = [
    "consider the reverse of the claim that follows", "think about the opposite of the claim below",
    "take the negation of the claim given below", "we need the opposite of a claim",
    "form the negation of the next claim", "work with the reverse of a claim",
    "consider the contrary of the claim that follows", "take the contrary of this claim",
    "take the contrary of the claim that follows",
]
REVERSE_QS = [
    ("does the {D} support that reverse", POS), ("is that opposite true of the {D}", POS),
    ("does the {D} bear out that negation", POS), ("is that opposite borne out by the {D}", POS),
    ("is that negation true of the {D}", POS), ("is the reverse true of the {D}", POS),
    ("does the {D} bear out that contrary", POS), ("is the contrary true of the {D}", POS),
    ("is that contrary groundless", NEG), ("does the {D} support that opposite", POS),
]
ANSWER_MAPS = [
    # (pattern, polarity of 'yes' relative to X)
    (r"answer yes if {X}; otherwise answer no\.", POS), (r"answer no if {X}; otherwise answer yes\.", NEG),
    (r"say yes when {X}, and say no in every other case\.", POS), (r"say no when {X}, and say yes in every other case\.", NEG),
    (r"the answer is yes exactly when {X}\.", POS), (r"the answer is no exactly when {X}\.", NEG),
    (r"mark no if {X}; otherwise mark yes\.", NEG), (r"enter no if {X}; otherwise enter yes\.", NEG),
    (r"mark yes if {X}; otherwise mark no\.", POS), (r"enter yes if {X}; otherwise enter no\.", POS),
    (r"say no if {X}, and yes in every other case\.", NEG), (r"say yes if {X}, and no in every other case\.", POS),
]
KEY_SENTENCES = [
    r"answer with the yes/no key in the card\.", r"give the answer the card's key assigns\.",
    r"answer by the card's key\.", r"read the claim and use the key in the card\.",
]
KEY_CLAIMS = [r"claim: {X}\.", r"the claim to check is this: {X}\.", r"check this claim against the {D}: {X}\."]


def _compile(pat: str, D: str, end=""):
    rx = re.escape(pat).replace(r"\{X\}", "(?P<x>.+)").replace(r"\{D\}", D)
    return re.compile("^" + rx + end + "$")


_FRAME_CACHE = {}


def frames_for(D: str):
    if D not in _FRAME_CACHE:
        st = [(_compile(p, D), pol, p) for p, pol in STATEMENT_FRAMES]
        qu = [(_compile(p, D, r"\?"), pol, p) for p, pol in QUESTION_FRAMES]
        se = [(re.compile("^" + re.escape(a).replace(r"\{X\}", "(?P<x>.+)").replace(r"\{D\}", D) + r"\. "
                          + re.escape(b).replace(r"\{D\}", D) + r"\?$"), pol, a + " / " + b) for a, b, pol in SETUP_FRAMES]
        rv = []
        for op in REVERSE_OPS:
            for q, pol in REVERSE_QS:
                rv.append((re.compile("^" + re.escape(op) + r"\. claim: (?P<x>.+)\. " + re.escape(q).replace(r"\{D\}", D)
                                      + r"\?$"), -pol, op + " / " + q))
        am = [(re.compile("^" + p.replace("{X}", "(?P<x>.+)") + "$"), pol, p) for p, pol in ANSWER_MAPS]
        _FRAME_CACHE[D] = dict(st=st, qu=qu, se=se, rv=rv, am=am)
    return _FRAME_CACHE[D]


# =============================================================================================== lemma space
# Atoms are matched on a normalised 'lemma string': quoted names and item names become tokens, contractions are
# expanded, verbs are reduced to their base form and the auxiliary 'do' is dropped ('does not fit' -> 'not fit').
CONTRACTIONS = [("doesn't", "does not"), ("isn't", "is not"), ("hasn't", "has not"), ("didn't", "did not"),
                ("wasn't", "was not"), ("aren't", "are not"), ("don't", "do not"), ("can't", "can not"),
                ("cannot", "can not"), ("weren't", "were not"), ("won't", "will not"), ("haven't", "have not")]
LEMMA = {
    "is": "be", "are": "be", "was": "be", "were": "be", "been": "be", "being": "be",
    "has": "have", "had": "have", "having": "have",
    "does": "do", "did": "do", "done": "do",
    "fits": "fit", "fitted": "fit", "applies": "apply", "applied": "apply", "falls": "fall", "fell": "fall",
    "fails": "fail", "failed": "fail", "lacks": "lack", "lacked": "lack", "misses": "miss", "missed": "miss",
    "missing": "miss", "excludes": "exclude", "excluded": "exclude", "rules": "rule", "ruled": "rule",
    "counts": "count", "counted": "count", "covers": "cover", "covered": "cover", "requires": "require",
    "reports": "report", "reported": "report", "describes": "describe", "described": "describe",
    "offers": "offer", "offered": "offer", "finds": "find", "says": "say", "said": "say",
    "contains": "contain", "contained": "contain", "includes": "include", "included": "include",
    "omits": "omit", "omitted": "omit", "leaves": "leave", "left": "leave", "leaving": "leave",
    "avoids": "avoid", "avoided": "avoid", "needs": "need", "needed": "need", "runs": "run", "ran": "run",
    "uses": "use", "used": "use", "ships": "ship", "shipped": "ship", "comes": "come", "came": "come",
    "remains": "remain", "remained": "remain", "holds": "hold", "held": "hold", "sits": "sit", "sat": "sit",
    "accepts": "accept", "accepted": "accept", "declines": "decline", "declined": "decline",
    "refuses": "refuse", "refused": "refuse", "passes": "pass", "passed": "pass", "cleans": "clean",
    "cleaned": "clean", "skips": "skip", "skipped": "skip", "skipping": "skip", "approves": "approve",
    "approved": "approve", "rejects": "reject", "rejected": "reject", "denies": "deny", "denied": "deny",
    "withholds": "withhold", "withheld": "withhold", "signs": "sign", "signed": "sign", "pays": "pay",
    "paid": "pay", "attends": "attend", "attended": "attend", "votes": "vote", "voted": "vote",
    "abstains": "abstain", "abstained": "abstain", "forwent": "forgo", "forgoes": "forgo", "forgone": "forgo",
    "vetoes": "veto", "vetoed": "veto", "turns": "turn", "turned": "turn", "sends": "send", "sent": "send",
    "stands": "stand", "stood": "stand", "goes": "go", "went": "go", "gets": "get", "got": "get",
    "shows": "show", "showed": "show", "shown": "show", "fills": "fill", "filled": "fill",
    "belongs": "belong", "concerns": "concern", "asks": "ask", "asked": "ask", "asking": "ask",
    "stays": "stay", "reaches": "reach", "reached": "reach", "meets": "meet", "met": "meet", "parked": "park",
    "makes": "make", "made": "make", "refunded": "refund", "lapsed": "lapse", "lapses": "lapse",
    "expired": "expire", "expires": "expire", "caught": "catch", "catches": "catch", "inspected": "inspect",
    "loaded": "load", "loads": "load", "forbids": "forbid", "forbade": "forbid", "claims": "claim",
    "claimed": "claim", "marked": "mark", "names": "name", "named": "name", "lists": "list",
    "reads": "read", "states": "state", "matches": "match", "matched": "match",
    "mentions": "mention", "mentioned": "mention", "calls": "call", "called": "call", "insults": "insult",
    "mocks": "mock", "threatens": "threaten", "praises": "praise", "keeps": "keep", "kept": "keep",
    "gives": "give", "gave": "give", "given": "give", "supports": "support", "supported": "support",
    "refutes": "refute", "refuted": "refute", "contradicts": "contradict", "settles": "settle",
    "shipping": "ship", "closes": "close", "closed": "close", "opens": "open", "opened": "open",
    "received": "receive", "receives": "receive", "arrived": "arrive", "arrives": "arrive",
    "works": "work", "worked": "work", "tells": "tell", "told": "tell", "wants": "want", "wanted": "want",
}

def lemma_str(s: str) -> str:
    t = " " + s + " "
    for a, b in CONTRACTIONS:
        t = re.sub(r"(?<![\w'])" + re.escape(a) + r"(?![\w])", b, t)
    out = []
    for w in t.split():
        core = w.rstrip(",.;:")
        tail = w[len(core):]
        if core.startswith("«"):
            out.append(w)
            continue
        out.append(LEMMA.get(core, core) + tail)
    toks = [w for w in out if w != "do"]
    return " ".join(toks)


NUM = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
SUBJ = r"(?:«[^»]+»|the recipe for «[^»]+»|the [a-z][a-z\-' ]*?|someone|nobody|no one|cars|it)"


# =============================================================================================== card parsing
SPECIAL_KEYS = {"rule", "note", "note 2", "yes", "no", "definition", "reading", "spelling", "heading", "writer", "tone",
                "layout", "wording", "date", "typing", "voice", "scope", "state", "triage note"}


def parse_card(card: str):
    out = []
    for line in (card or "").split("\n"):
        m = re.match(r"^- ([^:]+): (.*)$", line.strip())
        if m:
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def key_lines(card):
    """The card's yes / no lines: (yes_text, no_text); 'other case' lines come back as None."""
    y = n = None
    seen = False
    for k, v in parse_card(card):
        if k.lower() == "yes":
            y, seen = v, True
        elif k.lower() == "no":
            n, seen = v, True
    if not seen:
        return None

    def other(t):
        return t is not None and re.fullmatch(r"(?:any|every|all) other cases?\.?", low(t)) is not None
    return (None if other(y) else y, None if other(n) else n)


def parse_means(text: str):
    """'Label definitions: A means x; B means y.' / 'Here, A means x; B means y.' -> [(A, x), ...]"""
    m = re.search(r"(?:label definitions: |^here, |[.;] here, )(.+?)(?:\.(?: |$))", text, re.I)
    if not m:
        return []
    body = m.group(1)
    out = []
    for seg in re.split(r"; (?=[^;]+? means )", body):
        mm = re.match(r"^(.+?) means (.+)$", seg.strip())
        if mm:
            out.append((mm.group(1).strip(), mm.group(2).strip()))
    return out


# =============================================================================================== worlds
class World:
    """Shared machinery: name tokens, statement evaluation (frames, then atoms), generic negation peeling."""
    kind = "?"

    def __init__(self, row, ctx):
        self.row, self.ctx = row, ctx
        self.card = parse_card(row.get("card"))
        self.instr = norm(row.get("instructions") or "")
        self.state = row.get("state") or ""
        self.names = {}          # lower name -> 'label' | 'term'
        self.terms = {}          # lower term name -> lower definition
        self.term_order = []
        self.labels = []         # ordered lower label names
        self.docs = set()
        self.notes = []          # parse notes (ambiguities found)
        self.univ_mixed = 0      # arbiter round 3, A4: universal claims evaluated over a mixed set of items
        m = None
        for k, v in self.card:
            mm = re.match(r"^the (.+?) settles every claim", low(v))
            if mm:
                m = mm.group(1)
        if m:
            self.docs.add(m)
        self.D = None

    # ---- names and tokens
    def finish(self):
        self.D = doc_alt(self.docs)

    def tokens(self, s: str):
        """Replace quoted names with «n#» tokens (and 'non-X' with a negated token); returns (text, table)."""
        table = {}
        names = sorted(set(self.names) | set(self.extra_names()), key=len, reverse=True)
        for nm in names:
            for pre, neg in (("non-", True), ("", False)):
                q = "'" + pre + nm + "'"
                if q in s:
                    tok = "«n%d»" % len(table)
                    table[tok] = (nm, neg)
                    s = s.replace(q, tok)
        return s, table

    def subjects(self, s: str) -> str:
        return s

    def extra_names(self):
        return []

    def lemma(self, s: str):
        s = low(s).rstrip(".?! ")
        s, table = self.tokens(s)
        # any other quoted name (a label the card does not list): token too
        for m in list(re.finditer(r"(?:(?<=^)|(?<=[\s(]))'([^'«»]+)'(?=[\s,.;:?)]|$)", s)):
            q = m.group(0)
            if q in s:
                tok = "«n%d»" % len(table)
                nm = m.group(1)
                neg = nm.startswith("non-")
                table[tok] = (nm[4:] if neg else nm, neg)
                s = s.replace(q, tok)
        s = self.subjects(s)
        return lemma_str(s), table

    # ---- evaluation
    def frame_guard(self, pat: str, before: int):
        """arbiter round 3, A4: 'the opposite / reverse / contrary of the claim that none of the Xs ...' over a batch
        whose items are mixed has two golds (plain denial: some X ...; contrary: every X ...). Refuse unless the card
        defines the frame word as plain denial (the generator's 'wording' line, ruling #6)."""
        m = FRAME_WORD_RX.search(pat)
        if not m or self.univ_mixed == before:
            return
        w = m.group(1)
        card = low(self.row.get("card") or "")
        if re.search(r"'the %s of (?:a|the) claim' means (?:its |the )?(?:plain )?(?:denial|negation)" % w, card):
            return
        raise Ambiguous("AMBIGUOUS: '%s' of a universal claim over a mixed batch, and the card does not define '%s' "
                        "as plain denial (the denial and the contrary readings give different golds)" % (w, w))

    def ev(self, text: str, depth=0) -> bool:
        if depth > 14:
            raise ParseError("too deep")
        t = low(text).rstrip(". ")
        res = []
        for rx, pol, pat in frames_for(self.D)["st"]:
            m = rx.match(t)
            if not m:
                continue
            before = self.univ_mixed
            try:
                v = self.ev(m.group("x"), depth + 1)
            except Ambiguous:
                raise
            except ParseError:
                continue
            self.frame_guard(pat, before)
            res.append((v if pol > 0 else not v, pat))
        if res:
            vals = {v for v, _ in res}
            if len(vals) > 1:
                raise ParseError("ambiguous frame: " + " | ".join(p for _, p in res))
            return res[0][0]
        s, table = self.lemma(t)
        return self.ev_lemma(s, table, depth)

    def ev_question(self, q: str) -> bool:
        """q: cleaned, lowercased, may be several sentences, ends with '?'."""
        F = frames_for(self.D)
        for key in ("se", "rv"):
            for rx, pol, pat in F[key]:
                m = rx.match(q)
                if m:
                    before = self.univ_mixed
                    v = self.ev(m.group("x"))
                    self.frame_guard(pat, before)
                    return v if pol > 0 else not v
        last = split_sentences(q)
        if len(last) > 1:
            raise ParseError("unparsed multi-sentence question: " + q)
        for rx, pol, pat in F["qu"]:
            m = rx.match(q)
            if m:
                before = self.univ_mixed
                try:
                    v = self.ev(m.group("x"))
                except Ambiguous:
                    raise
                except ParseError:
                    continue
                self.frame_guard(pat, before)
                return v if pol > 0 else not v
        return self.ev_atom_question(q.rstrip("?"))

    def ev_atom_question(self, q: str) -> bool:
        s, table = self.lemma(q)
        cands = []
        # 'does/did X ...' (lemma removed 'do')
        if not re.match(r"^(?:be|have|can|must|should|would|will) ", s):
            cands.append(s)
        m = re.match(r"^(be|have|can|must|should|would|will) (.+)$", s)
        if m:
            aux, rest = m.group(1), m.group(2).split(" ")
            for i in range(1, len(rest)):
                cands.append(" ".join(rest[:i]) + " " + aux + " " + " ".join(rest[i:]))
        errs = []
        for c in cands:
            try:
                return self.ev_lemma(c, table, 0)
            except Ambiguous:
                raise
            except ParseError as e:
                errs.append(str(e))
        raise ParseError("atom question: " + s + " :: " + (errs[0] if errs else ""))

    PEEL = [
        (re.compile(r"^(?P<s>" + SUBJ + r") not (?P<r>.+)$"), lambda m: m.group("s") + " " + m.group("r")),
        (re.compile(r"^(?P<s>" + SUBJ + r") (?P<a>be|have|can) not (?P<r>.+)$"),
         lambda m: m.group("s") + " " + m.group("a") + " " + m.group("r")),
        (re.compile(r"^(?P<s>" + SUBJ + r") never (?P<r>.+)$"), lambda m: m.group("s") + " " + m.group("r")),
        # arbiter fix R1.2: 'X was / has / can never ...' (aux before 'never'), the same aux set as 'X be not ...'
        (re.compile(r"^(?P<s>" + SUBJ + r") (?P<a>be|have|can) never (?P<r>.+)$"),
         lambda m: m.group("s") + " " + m.group("a") + " " + m.group("r")),
        (re.compile(r"^(?P<s>" + SUBJ + r") fail to (?P<r>.+)$"), lambda m: m.group("s") + " " + m.group("r")),
        (re.compile(r"^(?P<s>" + SUBJ + r") be no longer (?P<r>.+)$"), lambda m: m.group("s") + " be " + m.group("r")),
    ]

    def ev_lemma(self, s: str, table: dict, depth: int) -> bool:
        if depth > 14:
            raise ParseError("too deep")
        v = self.atom(s, table, depth)
        if v is not None:
            return v
        errs = []
        for rx, f in self.PEEL:
            m = rx.match(s)
            if m:
                try:
                    return not self.ev_lemma(f(m), table, depth + 1)
                except Ambiguous:
                    raise
                except ParseError as e:
                    errs.append(str(e))
                    continue
        deep = [e for e in errs if not e.startswith("atom: ")]
        raise ParseError(deep[0] if deep else "atom: " + s)

    def atom(self, s, table, depth):
        return None

    # ---- name fit (labels, terms, non-X)
    def fit_tok(self, tok, table):
        nm, neg = table[tok]
        v = self.fit(nm)
        return (not v) if neg else v

    def fit(self, nm):
        raise ParseError("fit undefined for " + nm)


# ----------------------------------------------------------------------------------------------- one real text
# binary cards: which card label is the positive side of which base property (read off the two definitions)
PROP_LABELS = {
    "injury case": ("injury", True), "intact case": ("injury", False),
    "fire case": ("fire", True), "smoke-only case": ("fire", False),
    "crash case": ("crash", True), "defect-only case": ("crash", False),
    "acceptable": ("acceptable", True), "objectionable": ("acceptable", False),
    "grounded response": ("faithful", True), "embellished response": ("faithful", False),
    "match found": ("found", True), "dead end": ("found", False),
    "toxic": ("toxic", True), "civil": ("toxic", False),
}
# property wordings without a quoted label, per base property: (lemma-space regex over «S», polarity)
PROP_LEX = {
    "injury": [(r"«S» report that (?:someone|anyone) be actually hurt", True), (r"«S» describe an injury case", True),
               (r"«S» report an injury", True), (r"«S» say that (?:someone|anyone) be actually hurt", True),
               (r"«S» report no injury to anyone", False), (r"«S» report that nobody be actually hurt", False),
               (r"«S» describe an? (?:injury-free|non-injury) incident", False),
               (r"«S» omit any report of an injury", False), (r"«S» describe an intact case", False)],
    "fire": [(r"«S» report that the vehicle actually catch fire", True),
             (r"«S» say that the vehicle actually catch fire", True), (r"«S» report an actual (?:vehicle )?fire", True),
             (r"«S» report no actual fire in the vehicle", False), (r"«S» describe a fire-free incident", False),
             (r"«S» describe a smoke-only case", False)],
    "crash": [(r"«S» report an actual crash(?: of the vehicle)?", True), (r"«S» lack (?:a|any) report of an actual crash", False),
              (r"«S» report no actual crash of the vehicle", False), (r"«S» describe a crash-free incident", False),
              (r"«S» describe a defect-only case", False)],
    "acceptable": [(r"«S» be acceptable", True), (r"«S» be unacceptable", False), (r"«S» be objectionable", False)],
    "faithful": [(r"«S» (?:be|stay) faithful to the snippet", True), (r"«S» be unfaithful to the snippet", False),
                 (r"«S» be an embellished response", False)],
    "found": [(r"«S» offer an option that meet every stated need", True),
              (r"«S» offer no option that meet every stated need", False),
              (r"«S» find nothing that meet every stated need", False), (r"«S» reach a dead end", False)],
    "toxic": [(r"«S» be toxic", True), (r"«S» be non-toxic", False), (r"not one word of «S» be toxic", False),
              (r"«S» contain no toxic language", False), (r"«S» be civil", False)],
}
SUBJECT_PHRASES = ["the user's latest message", "the marked mention", "the marked name", "the marked chemical-gene pair",
                   "the wizard's response", "the assistant's last turn", "the action being judged"]
CARD_DOCS = ["request", "report", "passage", "sentence", "post", "dialogue", "message", "complaint", "comment",
             "action"]
FIT_POS = [r"«S» fit (?P<n>«n\d+»)", r"(?P<n>«n\d+») fit «S»", r"(?P<n>«n\d+») apply to «S»", r"«S» fall under (?P<n>«n\d+»)",
           r"(?P<n>«n\d+») be the label that fit «S»", r"«S» count as (?P<n>«n\d+»)", r"(?P<n>«n\d+») cover «S»",
           r"(?P<n>«n\d+») can be the label that fit «S»", r"«S» can fall under (?P<n>«n\d+»)",
           r"«S» can count as (?P<n>«n\d+»)", r"(?P<n>«n\d+») be applicable to «S»",
           # 'only' under the card's 'exactly one label fits' rule
           r"(?P<n>«n\d+») be the only listed label that fit «S»"]
FIT_NEG = [r"the definitions exclude «S» from (?P<n>«n\d+»)", r"the definitions rule out (?P<n>«n\d+») for «S»",
           r"«S» miss the mark for (?P<n>«n\d+»)", r"«S» lack what (?P<n>«n\d+») require",
           r"(?P<n>«n\d+») be inapplicable to «S»"]
FIT_POS_RX = [re.compile("^" + p + "$") for p in FIT_POS]
FIT_NEG_RX = [re.compile("^" + p + "$") for p in FIT_NEG]


class CardWorld(World):
    kind = "card"

    def __init__(self, row, ctx, base):
        super().__init__(row, ctx)
        self.base = base
        self.prop_task = None
        order = []
        lines = self.card if self.card else [(a, b) for a, b in parse_means(self.instr)]
        self.from_means = not self.card
        for k, v in lines:
            kl, vl = low(k), low(v)
            if kl in SPECIAL_KEYS:
                continue
            is_term = (re.search(r"(?:^|[\s(])'[^']+'", vl) or re.match(r"^an? non-", vl)
                       or vl.startswith("applies to every") or "label line" in vl or "whose label" in vl)
            if is_term and not self.from_means:
                self.terms[kl] = vl
                self.term_order.append(kl)
                self.names[kl] = "term"
            else:
                self.labels.append(kl)
                self.names[kl] = "label"
            order.append(kl)
        self.order = order
        self.rule = low(dict((low(a), b) for a, b in self.card).get("rule", ""))
        # the gold label in the card's names
        if base is None:
            raise ParseError("no base row")
        if base["kind"] == "label":
            self.gold = base["label"]
        else:
            self.prop_task = base["task"]
            hit = [l for l in self.labels if l in PROP_LABELS and PROP_LABELS[l][0] == base["task"]]
            pos = [l for l in hit if PROP_LABELS[l][1]]
            negl = [l for l in hit if not PROP_LABELS[l][1]]
            self.pos_label = pos[0] if pos else None
            self.neg_label = negl[0] if negl else None
            if self.pos_label is None and self.neg_label is None and not self.from_means:
                # a binary card whose label lines are not the property names (devx); keep P only
                pass
            self.gold = (self.pos_label if base["val"] else self.neg_label)
            self.P = base["val"]
        for d in CARD_DOCS:
            if re.search(r"\b(?:the|this|a|an) " + d + r"\b", low(self.instr + " " + (row.get("card") or ""))):
                self.docs.add(d)
        self.finish()

    def extra_names(self):
        out = ["others' need"]
        if getattr(self, "gold", None):
            out.append(self.gold)
        return out

    def subjects(self, s):
        for p in SUBJECT_PHRASES:
            s = s.replace(p, "«S»")
        for d in sorted(self.docs, key=len, reverse=True):
            s = re.sub(r"\b(?:the|this) " + re.escape(d) + r"\b", "«S»", s)
        s = re.sub(r"\bit\b", "«S»", s)
        return s

    # ---- label / term truth
    def fit(self, nm):
        if nm in self.terms:
            return self.term(nm)
        if nm not in self.labels and nm.replace("'", "") in [x.replace("'", "") for x in self.labels]:
            self.notes.append("LABEL_APOSTROPHE_MISMATCH: %s" % nm)
            nm = [x for x in self.labels if x.replace("'", "") == nm.replace("'", "")][0]
            g = self.gold.replace("'", "") if self.gold else None
            return g == nm.replace("'", "")
        if self.gold is None:
            raise ParseError("no gold label on this card")
        if nm in self.labels or nm == self.gold or not self.labels:
            return self.gold == nm
        raise ParseError("unknown label " + nm)

    def text_has_qmark(self):
        return "?" in self.state

    def term(self, nm):
        raw = self.terms[nm]
        v, tb = self.tokens(raw)
        T = r"(«n\d+»)"

        def f(tok):
            return self.fit_tok(tok, tb)
        m = re.match(r"^an? [a-z\- ]+? whose label (?:is not|isn't) " + T + "$", v)
        if m:
            return not f(m.group(1))
        m = re.match(r"^an? [a-z\- ]+? whose label is ((?:«n\d+»)(?:(?:, |,? or )«n\d+»)*)$", v)
        if m:
            return any(f(t) for t in re.findall(r"«n\d+»", m.group(1)))
        m = re.match(r"^an? [a-z\- ]+? that the definitions exclude from " + T + "$", v)
        if m:
            return not f(m.group(1))
        m = re.match(r"^an? [a-z\- ]+? that " + T + " never covers$", v)
        if m:
            return not f(m.group(1))
        m = re.match(r"^an? [a-z\- ]+? that fits " + T + ", except one that contains a question mark$", v)
        if m:
            return f(m.group(1)) and not self.excl_qmark()
        m = re.match(r"^an? [a-z\- ]+? for which the definitions rule out " + T + "$", v)
        if m:
            return not f(m.group(1))
        m = re.match(r"^an? non-'?([^']+?)'? [a-z\-]+$", raw)
        if m:
            return not self.fit(m.group(1))
        m = re.match(r"^applies to every [a-z\- ]+? unless its label is " + T + "$", v)
        if m:
            return not f(m.group(1))
        m = re.match(r"^an? [a-z\- ]+? (?:without the features of|with no claim to) " + T + "$", v)
        if m:
            return not f(m.group(1))
        if re.match(r"^(?:the [a-z ]+ fits none of the label lines above|no label line above fits the [a-z ]+|"
                    r"the [a-z ]+ does not fit any label line above)$", raw):
            above = [x for x in self.order[:self.order.index(nm)] if x in self.labels]
            if self.gold is None:
                raise ParseError("residual without gold")
            return self.gold not in above
        m = re.match(r"^an? [a-z\- ]+? that (.+)$", raw)
        if m:
            s, table = self.lemma("it " + m.group(1))
            return self.ev_lemma(s, table, 1)
        raise ParseError("term def: " + raw)

    def excl_qmark(self):
        """'except one that contains a question mark': the defined object is the whole text (dialogue / post)."""
        whole = "?" in self.state
        last = self.state.split("User (latest message):")[-1] if "User (latest message):" in self.state else self.state
        if ("?" in last) != whole:
            self.notes.append("EXCL_SCOPE: '?' in the dialogue but not in the latest message (or the reverse)")
        return whole

    # ---- atoms
    def atom(self, s, table, depth):
        for rx in FIT_POS_RX:
            m = rx.match(s)
            if m:
                if "only listed label" in s and "exactly one" not in self.rule and not self.from_means:
                    self.notes.append("ONLY_WITHOUT_EXACTLY_ONE_RULE")
                return self.fit_tok(m.group("n"), table)
        for rx in FIT_NEG_RX:
            m = rx.match(s)
            if m:
                return not self.fit_tok(m.group("n"), table)
        m = re.match(r"^(?:the label that fit «S» be not|«S» fit not) («n\d+») but («n\d+»)$", s)
        if m:
            return (not self.fit_tok(m.group(1), table)) and self.fit_tok(m.group(2), table)
        m = re.match(r"^the label that fit «S» be («n\d+»(?:, «n\d+»)*(?:,? or «n\d+»)?)$", s)
        if m:
            return any(self.fit_tok(t, table) for t in re.findall(r"«n\d+»", m.group(1)))
        m = re.match(r"^«S» fit (one|any|none) of the card's first (\w+) label lines$", s)
        if m:
            n = NUM.get(m.group(2))
            first = self.labels[:n]
            v = self.gold in first
            return (not v) if m.group(1) == "none" else v
        m = re.match(r"^no label line among the card's first (\w+) fit «S»$", s)
        if m:
            return self.gold not in self.labels[:NUM.get(m.group(1))]
        if self.prop_task:
            for rx, pol in PROP_LEX.get(self.prop_task, []):
                if re.fullmatch(rx, s):
                    return self.P if pol else not self.P
        return None


# =============================================================================================== driver
SELECT_TRUE = [r"which statement about (?:the|this) {D} is true\?", r"which statement about (?:the|this) {D} does hold\?",
               r"which statement about (?:the|this) {D} holds\?",
               r"exactly one statement below does hold for the {D}\. which one is it\?",
               r"exactly one statement below is true\. which one is it\?",
               r"which of these statements is true of (?:the|this) {D}\?"]
SELECT_FALSE = [r"which statement about (?:the|this) {D} is false\?", r"which of these statements is untrue of (?:the|this) {D}\?",
                r"exactly one statement below is false\. which one is it\?",
                r"which statement about (?:the|this) {D} does not hold\?",
                r"exactly one statement below doesn't hold for the {D}\. which one is it\?",
                r"which statement about (?:the|this) {D} fails to hold\?", r"which statement about (?:the|this) {D} is untrue\?"]


def yn_from_card(W, text_for_claim=None):
    """Truth of 'yes' per the card's key lines, or None when the card has none. Cross-checks the two lines."""
    kl = key_lines(W.row.get("card"))
    if kl is None:
        return None
    y, n = kl
    yv = W.ev(clean(y, W.D)) if y else None
    nv = W.ev(clean(n, W.D)) if n else None
    if yv is not None and nv is not None and yv == nv:
        raise ParseError("card yes and no lines are both %s" % yv)
    return yv if yv is not None else (not nv if nv is not None else None)


def decide_yn(W):
    q = clean(W.instr, W.D)
    F = frames_for(W.D)
    card_yes = None
    try:
        card_yes = yn_from_card(W)
    except Ambiguous:
        raise
    except ParseError as e:
        card_err = str(e)
    else:
        card_err = None
    # answer mapping in the instruction
    for rx, pol, pat in F["am"]:
        m = rx.match(q)
        if m:
            v = W.ev(m.group("x"))
            ans = v if pol > 0 else not v
            return finish_yn(W, ans, card_yes, card_err, "answer-map")
    # key frames: the answer is the card's
    if any(re.search(p, q) for p in KEY_SENTENCES) or re.match(r"^(?:claim: |the claim to check is this: )", q):
        if card_yes is None:
            raise ParseError("key frame but no usable card key: %s" % card_err)
        claim = None
        for p in KEY_CLAIMS:
            for s in split_sentences(q):
                m = re.match("^" + p.replace("{X}", "(?P<x>.+)").replace("{D}", W.D) + "$", s)
                if m:
                    claim = m.group("x")
        if claim is None:
            raise ParseError("key frame without a claim: " + q)
        kl = key_lines(W.row.get("card"))
        quoted = [x for x in kl if x]
        if not any(('"%s"' % claim) in low(x) or claim in low(x) for x in quoted):
            W.notes.append("KEY_CLAIM_MISMATCH")
        W.ev(claim)  # the claim itself must parse
        return 1 if card_yes else 0
    if q.endswith("?"):
        v = W.ev_question(q)
        return finish_yn(W, v, card_yes, card_err, "question")
    # a bare statement (devx 'say no if ...' variants fall here when unmatched)
    raise ParseError("unparsed instruction: " + q)


def finish_yn(W, ans, card_yes, card_err, how):
    if card_yes is not None and card_yes != ans:
        W.notes.append("CARD_KEY_DISAGREES_WITH_QUESTION")
        raise ParseError("card key says %s, question says %s" % (card_yes, ans))
    if card_err and key_lines(W.row.get("card")) is not None:
        W.notes.append("CARD_KEY_UNPARSED: " + card_err[:120])
    return 1 if ans else 0


def decide_choice(W):
    q = clean(W.instr, W.D)
    opts = W.row.get("options") or []
    sel = None
    for p in SELECT_TRUE:
        if re.search(p.replace("{D}", W.D) + "$", q):
            sel = True
    for p in SELECT_FALSE:
        if re.search(p.replace("{D}", W.D) + "$", q):
            sel = False
    vals = []
    if sel is None:
        vals = W.item_select(q, opts)
        sel = True
    else:
        for o in opts:
            vals.append(W.ev(clean(o, W.D)))
    hits = [o for o, v in zip(opts, vals) if v == sel]
    if len(hits) != 1:
        raise ParseError("choice: %d options evaluate to %s (%s)" % (len(hits), sel, vals))
    return hits[0]


def build_world(row, ctx):
    m = row.get("meta") or {}
    st = row.get("state") or ""
    refs = (m.get("derived_from") or "").split("|") if m.get("derived_from") else list(m.get("orig") or [])
    if st.startswith("Support ticket"):
        return TriageWorld(row, ctx)
    if re.search(r"^Prepared by: ", st, re.M) or re.search(r'"prepared_by"', st):
        return RecordWorld(row, ctx)
    if re.match(r"^[A-Z][a-z]+ 1:\n", st) and re.search(r"\n\n[A-Z][a-z]+ 2:\n", st):
        return MultiWorld(row, ctx, refs)
    if refs and not refs[0].startswith("invented:"):
        base = ctx.base(refs[0], text=st)
        return CardWorld(row, ctx, base)
    return DevxRecordWorld(row, ctx)


def decide2_row(row, ctx):
    """-> (pred, notes). pred is 0/1 for yes/no rows, the option string for choice rows, None if unparsed."""
    try:
        if (row.get("track") == "F7X") or ((row.get("meta") or {}).get("dev_kind") == "devx"):
            if id(ctx) not in _DEVX:
                _DEVX[id(ctx)] = DevxEval(ctx)
            return _DEVX[id(ctx)].decide(row), ["DEVX_TABLE"]
        W = build_world(row, ctx)
        if row.get("qtype") == "choice":
            return decide_choice(W), W.notes
        return decide_yn(W), W.notes
    except ParseError as e:
        return None, ["UNPARSED: " + str(e)[:300]]


class TriageWorld(World):
    """A support ticket with a triage note whose 'refund requested' field reads yes / no / (left blank)."""
    kind = "triage"

    def __init__(self, row, ctx):
        super().__init__(row, ctx)
        m = re.search(r"^refund requested: (.+)$", self.state, re.M)
        if not m:
            raise ParseError("triage field missing")
        v = m.group(1).strip().lower()
        self.val = {"yes": "yes", "no": "no", "(left blank)": "blank"}.get(v)
        if self.val is None:
            raise ParseError("triage value " + v)
        self.docs.add("ticket")
        self.finish()

    def tokens(self, s):
        return s, {}

    def lemma(self, s):
        s = low(s).rstrip(".?! ")
        return lemma_str(s), {}

    def atom(self, s, table, depth):
        R = r"the customer be ask for a refund"
        if re.fullmatch(r"the triage note claim that " + R, s):
            return self.val == "yes"
        if re.fullmatch(r"the triage note claim that the customer be not ask for a refund", s):
            return self.val == "no"
        if re.fullmatch(r"the triage note make no claim that " + R, s):
            # non-factive: 'makes no claim that P' is true unless the note claims P
            return self.val != "yes"
        if re.fullmatch(r"the triage note make no claim either way about a refund|the triage note say nothing about a refund", s):
            return self.val == "blank"
        return None

    def ev(self, text, depth=0):
        t = low(text).rstrip(". ")
        if t == "the note claims: 'the customer is asking for a refund'":
            return self.val == "yes"
        if t == "the note claims: 'the customer is not asking for a refund'":
            return self.val == "no"
        if t == "the note says nothing about a refund":
            return self.val == "blank"
        return super().ev(text, depth)


# ----------------------------------------------------------------------------------------------- invented records
# Record packs: the item noun and the author's reading of each wording, as (lemma-space pattern over the item token X,
# card term it is about (None = the pack's first term), polarity). Field conditions come from the card's own term lines.
PACKS = {
    "accounts ledger": ("invoice", [
        (r"X have be pay", "paid", 1), (r"X be pay", None, 1), (r"the client pay X", None, 1), (r"X be unpaid", None, -1),
        (r"X remain unpaid", None, -1), (r"X be leave unpaid", None, -1), (r"no payment have be make on X", None, -1),
        (r"X lack a recorded payment", None, -1), (r"X have a recorded payment", None, 1),
        (r"X be (?:still )?outstanding", "outstanding", 1)]),
    "delivery log": ("parcel", [
        (r"the recipient sign for X", "signed for", 1), (r"the recipient (?:refuse|decline) to sign for X", None, -1),
        (r"X be unsigned", None, -1), (r"X be leave without a signature", None, -1), (r"X have no signature", None, -1),
        (r"X count as returned", "returned", 1)]),
    "menu card": ("dish", [
        (r"X contain gluten", "gluten dish", 1), (r"X be gluten-free", None, -1), (r"X contain no gluten", None, -1),
        (r"X be make without gluten", None, -1), (r"X lack gluten", None, -1),
        (r"the recipe for X (?:omit|exclude|leave out|avoid) gluten", None, -1), (r"X have a recipe that omit gluten", None, -1),
        (r"X have no gluten among its allergen tags", None, -1), (r"X count as coeliac-safe", "coeliac-safe", 1)]),
    "intake sheet": ("application", [
        (r"X be complete", "complete", 1), (r"X be incomplete", None, -1), (r"X lack a required field", None, -1),
        (r"X be miss a required field", None, -1), (r"X fill every required field", None, 1),
        (r"X be on hold for blanks", "on hold for blanks", 1)]),
    "ticket list": ("ticket", [
        (r"X be valid", "valid", 1), (r"X can be use", None, 1), (r"X be invalid", None, -1), (r"X have expire", "expired", 1)]),
    "guest list": ("guest", [
        (r"X accept the invitation", "attending", 1), (r"X (?:decline|refuse) the invitation", None, -1),
        (r"X send regrets", "sent regrets", 1)]),
    "inspection log": ("unit", [
        (r"X pass the inspection", "passed", 1), (r"X fail the inspection", None, -1),
        (r"X be send for repair", "sent for repair", 1)]),
    "service sheet": ("line", [
        (r"X be connected", "live", 1), (r"X have a live connection", None, 1), (r"X be disconnected", None, -1),
        (r"X have no live connection", None, -1), (r"X be without a live connection", None, -1),
        (r"X lack a live connection", None, -1), (r"X be a dead line", "dead line", 1)]),
    "equipment list": ("device", [
        (r"X need a power cable", "mains device", 1), (r"X be cordless", None, -1), (r"X need no power cable", None, -1),
        (r"X run without a power cable", None, -1), (r"X run on a battery", "battery-run", 1)]),
    "patrol sheet": ("car", [
        (r"X be park legally", "parked legally", 1), (r"X be (?:park illegally|illegally park)", None, -1),
        (r"X sit in a restricted spot", "restricted spot", 1)]),
    "board minutes": ("request", [
        (r"the board approve X", "approved", 1), (r"the board (?:reject|deny|decline|refuse) X", None, -1),
        (r"the board withhold approval from X", None, -1), (r"X be in the red file", "red file", 1)]),
    "stock sheet": ("bundle", [
        (r"X include a charger", "full bundle", 1), (r"X (?:exclude|omit) the charger", None, -1),
        (r"X have its charger leave out", None, -1), (r"X lack a charger", None, -1), (r"X ship without a charger", None, -1),
        (r"X come with no charger", None, -1), (r"X be a cut-down box", "cut-down box", 1)]),
    "housekeeping sheet": ("room", [
        (r"the cleaner clean X", "cleaned", 1), (r"the cleaner (?:skip|miss) X", None, -1),
        (r"X be on the redo list", "redo list", 1)]),
    "briefing sheet": ("staff member", [
        (r"X be present at the briefing", "present", 1), (r"X be absent from the briefing", None, -1),
        (r"X (?:miss|skip) the briefing", None, -1), (r"X attend the briefing", None, 1), (r"X be mark away", "away", 1)]),
    "route plan": ("route", [
        (r"X use a toll road", "toll route", 1), (r"X avoid toll roads", None, -1), (r"X be toll-free", None, -1),
        (r"X have no toll roads", None, -1), (r"X run without toll roads", None, -1), (r"X be a by-road route", "by-road route", 1)]),
    "account review": ("account", [
        (r"X be verified", "verified", 1), (r"X be unverified", None, -1), (r"X lack a completed identity check", None, -1),
        (r"X be still pending review", "pending review", 1)]),
    "order sheet": ("order", [
        (r"X be refundable", "refundable", 1), (r"X can be refund", None, 1), (r"X be non-refundable", None, -1),
        (r"X be a final sale", "final sale", 1)]),
    "road report": ("road", [
        (r"X be passable", "passable", 1), (r"X be impassable", None, -1), (r"cars can get through on X", None, 1),
        (r"X be blocked", "blocked", 1)]),
    "locker check": ("locker", [
        (r"X hold (?:something|anything)", "in use", 1), (r"X hold nothing", None, -1), (r"X hold no items", None, -1),
        (r"X be without contents", None, -1), (r"X have no items in it", None, -1), (r"X be empty", "empty", 1)]),
    "attendance sheet": ("session", [
        (r"someone attend X", "attended", 1), (r"(?:nobody|no one|none of the invitees) attend X", None, -1),
        (r"X be attend", None, 1), (r"X go unattended", None, -1), (r"X stand empty", "stood empty", 1)]),
    "ward chart": ("patient", [
        (r"X have symptoms", "symptomatic", 1), (r"X be asymptomatic", None, -1), (r"at no point X show symptoms", None, -1),
        (r"X have no symptoms", None, -1), (r"X be in the clear group", "clear group", 1)]),
    "licence register": ("licence", [
        (r"X be valid", "active", 1), (r"X be invalid", None, -1), (r"X have lapse", "lapsed", 1)]),
    "council record": ("grant", [
        (r"the council approve X", "funded", 1), (r"the council (?:veto|turn down) X", None, -1), (r"X be shelved", "shelved", 1)]),
    "payment ledger": ("payment plan", [
        (r"X be regular", "regular", 1), (r"X be irregular", None, -1), (r"X be on the watch list", "watch list", 1)]),
    "ballot record": ("member", [
        (r"X vote in the ballot", "voted", 1), (r"X (?:abstain from|forgo) the ballot", None, -1),
        (r"X be in the blank column", "blank column", 1)]),
    # deontic packs: O(X) = 'X must be signed for / inspected'; the card's rule ties O to a marked term
    "dispatch sheet": ("parcel", [
        (r"X must be sign for", "#O", 1), (r"X have to be sign for", "#O", 1), (r"X need not be sign for", "#O", -1),
        (r"X must not be leave unsigned", "#O", 1), (r"the courier can leave X unsigned", "#O", -1),
        (r"the rule forbid leave X unsigned", "#O", 1), (r"the rule forbid skip the signature for X", "#O", 1),
        (r"X must not go out without a signature", "#O", 1), (r"the courier must not skip the signature for X", "#O", 1)]),
    "cargo manifest": ("crate", [
        (r"X must be inspect before loading", "#O", 1), (r"X have to be inspect(?: before loading)?", "#O", 1),
        (r"X need not be inspect before loading", "#O", -1), (r"X must not be load uninspected", "#O", 1),
        (r"the crew can load X uninspected", "#O", -1), (r"at no point X have to be inspect(?: before loading)?", "#O", -1)]),
}


class RecordWorld(World):
    kind = "record"

    def __init__(self, row, ctx):
        super().__init__(row, ctx)
        st = self.state
        if st.lstrip().startswith("{"):
            obj = json.loads(st)
            title = obj.get("title", "")
            lists = [(k, v) for k, v in obj.items() if isinstance(v, list)]
            if len(lists) != 1:
                raise ParseError("json record lists")
            self.items = [(x["name"], {low(k): str(v) for k, v in x.items() if k != "name"}) for x in lists[0][1]]
        else:
            title = st.split("\n", 1)[0]
            self.items = None
        self.title = low(re.sub(r" [A-Z]\d+$", "", title))
        if self.title not in PACKS:
            raise ParseError("unknown record: " + self.title)
        self.noun, self.lex = PACKS[self.title]
        self.docs.add(self.title)
        self.docs.add(self.title.split(" ")[-1])
        # term lines: the card's, or the instruction's 'Here, A means ...; B means ...'
        lines = self.card if self.card else parse_means(self.instr)
        for k, v in lines:
            kl = low(k)
            if kl in SPECIAL_KEYS - {"rule"} and kl != "rule":
                continue
            if kl == "rule":
                self.rule = low(v)
                continue
            self.terms[kl] = low(v)
            self.term_order.append(kl)
            self.names[kl] = "term"
        if not hasattr(self, "rule"):
            m = re.match(r"^(an? [a-z ]+? (?:marked|labelled) \S+ must .+?; other [a-z ]+ need not be)", low(self.instr))
            self.rule = m.group(1) if m else ""
        if self.items is None:
            self.items = self.parse_items()
        self.names_lower = [low(n) for n, _ in self.items]
        self.finish()

    # ---- record parsing
    def field_names(self):
        out = []
        for v in self.terms.values():
            m = re.search(r"whose ([a-z ]+?)(?: field)? (?:reads?|read|include|includes|list|lists|names|count is|is|lack)\b", v)
            if m:
                out.append(m.group(1))
        return out

    def parse_items(self):
        lines = self.state.split("\n")
        body = [x for x in lines[2:] if x.strip()]
        items = []
        if body and body[0].startswith("| "):
            hdr = [low(c) for c in body[0].strip("|").split("|")]
            for ln in body[2:]:
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                items.append((cells[0], {hdr[i].strip(): cells[i] for i in range(1, len(cells))}))
            return items
        if body and re.match(r"^[a-z ]+ 1: ", body[0]):
            cur = None
            for ln in body:
                m = re.match(r"^[a-z ]+ \d+: (.+)$", ln)
                if m:
                    cur = (m.group(1).strip(), {})
                    items.append(cur)
                    continue
                k, v = ln.split(": ", 1)
                cur[1][low(k)] = v.strip()
            return items
        if body and " is listed with " in body[0]:
            for ln in body:
                m = re.match(r'^(.+?) is listed with ([A-Za-z ]+?) "(.+)" and (.+?) (\S+)\.?$', ln)
                if not m:
                    raise ParseError("prose line: " + ln)
                items.append((m.group(1), {low(m.group(2)): m.group(3)}))
            return items
        if body and body[0].startswith("- "):
            fields = self.field_names()
            for ln in body:
                m = re.match(r"^- (.+?): (.+?); (.+)$", ln)
                if not m:
                    raise ParseError("bullet line: " + ln)
                fv = m.group(2)
                hit = [f for f in sorted(set(fields), key=len, reverse=True) if low(fv).startswith(f + " ")]
                if not hit:
                    # attendee count: the field is printed as 'attendees'
                    mm = re.match(r"^([a-z ]+?) (\S.*)$", fv)
                    hit = [mm.group(1)] if mm else []
                    if not hit:
                        raise ParseError("bullet field: " + ln)
                items.append((m.group(1), {hit[0]: fv[len(hit[0]) + 1:]}))
            return items
        if body and body[0].count(",") >= 2:
            hdr = [low(c) for c in body[0].split(",")]
            for ln in body[1:]:
                cells = next(__import__("csv").reader([ln]))
                items.append((cells[0], {hdr[i]: cells[i] for i in range(1, len(cells))}))
            return items
        raise ParseError("record format")

    def value(self, item, field):
        f = dict(item[1])
        cand = [field, field.replace(" field", ""), {"attendee count": "attendees"}.get(field, field)]
        for c in cand:
            if c in f:
                return f[c]
        for k in f:
            if k.startswith(field.split(" ")[0]):
                return f[k]
        raise ParseError("field %s not in %s" % (field, list(f)))

    # ---- subjects
    def subjects(self, s):
        for k, nm in sorted(enumerate(self.names_lower), key=lambda x: -len(x[1])):
            s = re.sub(r"\b(?:the )?(?:" + re.escape(self.noun) + r" )?" + re.escape(nm) + r"\b", "«x%d»" % k, s)
        return s

    # ---- terms
    def term_true(self, nm, k):
        """Does item k count as card term nm?"""
        if nm == "#O":
            m = re.search(r"(?:marked|labelled) '?([^';]+?)'? must ", self.rule)
            if not m:
                raise ParseError("deontic rule: " + self.rule)
            return self.term_true(low(m.group(1)), k)
        if nm not in self.terms:
            raise ParseError("record term missing: " + nm)
        v = self.terms[nm]
        item = self.items[k]
        m = re.search(r"whose ([a-z ]+?)(?: field)? (?:reads?|read) (.+)$", v)
        if m:
            val = low(self.value(item, m.group(1)))
            spec = m.group(2)
            vals = re.findall(r"'([^']+)'", spec)
            if not vals:
                present = {low(self.value(it, m.group(1))) for it in self.items}
                vals = [x for x in present if re.search(r"(?:^|, | or )" + re.escape(x) + r"(?:$|, | or )", spec)]
            return val in [low(x) for x in vals]
        m = re.search(r"whose (allergen tags|box contents) (?:include|list) (?:an? )?([a-z]+)$", v)
        if m:
            return m.group(2) in [x.strip() for x in low(self.value(item, m.group(1))).split(",")]
        m = re.search(r"whose tags lack ([a-z]+)$", v)
        if m:
            return m.group(1) not in [x.strip() for x in low(self.value(item, "allergen tags")).split(",")]
        if v.endswith("whose symptoms field names a symptom"):
            return low(self.value(item, "symptoms")) != "clear"
        m = re.search(r"whose attendee count is (above zero|0)$", v)
        if m:
            n = int(self.value(item, "attendees"))
            return n > 0 if m.group(1) == "above zero" else n == 0
        if v.endswith("whose contents field lists at least one thing"):
            return low(self.value(item, "contents")) != "empty"
        m = re.match(r"^applies to every [a-z ]+? unless it counts as '(.+)'$", v)
        if m:
            return not self.term_true(m.group(1), k)
        # an English description of the item: rewrite it as a clause about the item, then read it with the lexicon
        clause = self.def_clause(v, k)
        s, table = self.lemma(clause)
        return self.ev_lemma(s, table, 1)

    def def_clause(self, v, k):
        X = self.names_lower[k]
        noun = r"(?:" + re.escape(self.noun) + r"|[a-z]+(?: [a-z]+)?)"
        m = re.match(r"^an? " + noun + r" (?:that|who) ((?:nobody|no one|someone|the [a-z]+) .+)$", v)
        if m and not re.match(r"^the [a-z]+ (?:is|was|has|does|did|lacks|holds|needs)\b", m.group(1)):
            return m.group(1) + " " + X
        m = re.match(r"^an? " + noun + r" (?:that|who) (.+)$", v)
        if m:
            return X + " " + m.group(1)
        m = re.match(r"^an? " + noun + r" (the [a-z]+ .+)$", v)
        if m:
            return m.group(1) + " " + X if not re.search(r" from$", m.group(1)) else m.group(1) + " " + X
        m = re.match(r"^an? " + noun + r" (missing|absent from|left without) (.+)$", v)
        if m:
            return X + " is " + m.group(1) + " " + m.group(2)
        m = re.match(r"^an? " + noun + r" with no (.+)$", v)
        if m:
            return X + " has no " + m.group(1)
        m = re.match(r"^an? ([a-z\-]+(?: parked)?) " + noun + r"$", v)
        if m:
            return X + " is " + m.group(1)
        raise ParseError("record term def: " + v)

    def fit(self, nm):
        raise ParseError("record fit without an item")

    # ---- atoms
    def atom(self, s, table, depth):
        for pat, term, pol in self.lex:
            rx = "^" + pat.replace("X", r"«x(?P<k>\d+)»") + "$"
            m = re.match(rx, s)
            if m:
                t = term or self.lex[0][1]
                v = self.term_true(t, int(m.group("k")))
                return v if pol > 0 else not v
        # quoted term membership: 'T' applies to X / X counts as 'T' / ...
        X = r"«x(?P<k>\d+)»"
        for p, pol in ((r"(?P<n>«n\d+») apply to X", 1), (r"X count as (?P<n>«n\d+»)", 1), (r"X can count as (?P<n>«n\d+»)", 1),
                       (r"(?P<n>«n\d+») be applicable to X", 1), (r"(?P<n>«n\d+») be inapplicable to X", -1)):
            m = re.match("^" + p.replace("X", X) + "$", s)
            if m:
                nm, neg = table[m.group("n")]
                v = self.term_true(nm, int(m.group("k")))
                v = (not v) if neg else v
                return v if pol > 0 else not v
        return None

    def item_select(self, q, opts):
        nouns = [self.noun, "guest", "staff member", "member"]
        m = None
        for nn in nouns:
            m = re.match(r"^.*\bwhich " + re.escape(nn) + r" (.+)\?$", q)
            if m:
                break
        if not m:
            raise ParseError("choice question: " + q)
        pred = m.group(1)
        out = []
        for o in opts:
            nm = low(o)
            if nm not in self.names_lower:
                raise ParseError("option is not an item: " + o)
            mm = re.match(r"^(?:did|does|do) ((?:the [a-z]+|someone|nobody|no one) .+)$", pred)
            if mm and not re.match(r"^the [a-z]+ (?:is|has)\b", mm.group(1)):
                clause = mm.group(1) + " " + nm
            elif re.match(r"^(?:did|does|do|is|was|has) ", pred):
                aux, rest = pred.split(" ", 1)
                clause = nm + " " + aux + " " + rest
            else:
                clause = nm + " " + pred
            s, table = self.lemma(clause)
            out.append(self.ev_lemma(s, table, 0))
        return out


# ----------------------------------------------------------------------------------------------- batch of real texts
# The batch's property (the card's rule line 'each one either SG or does not'), read from each text's human label.
# For each property: base link, complement wordings, the negated adjective, the plain adjective.
MULTI_PRED = {
    "asks for pothole repair": ("label", "pothole repair", ["concerns some other kind of repair or problem"],
                                "non-pothole", None),
    "concerns a street light": ("label", "street light repair", ["concerns something other than street lighting"],
                                "non-lighting", None),
    "reports an injury": ("task", "injury", ["describes an intact case"], "injury-free", None),
    "reports an actual crash": ("task", "crash", ["describes a defect-only case"], "crash-free", None),
    "reports an actual vehicle fire": ("task", "fire", ["describes a smoke-only case"], "fire-free", None),
    "describes a fall to a lower level": ("label", "fall to lower level", ["describes some other kind of event"],
                                          "non-fall", None),
    "describes a worker struck by a moving object": ("label", "struck by object or equipment",
                                                     ["describes some other kind of event"], "non-impact", None),
    "is acceptable": ("task", "acceptable", ["is objectionable"], "unacceptable", "acceptable"),
    "is toxic": ("task", "toxic", ["is civil"], "non-toxic", "toxic"),
    "belongs at the language reference desk": ("label", "language reference desk",
                                               ["belongs somewhere other than the language reference desk"],
                                               "non-language", None),
}


class MultiWorld(World):
    kind = "multi"

    def __init__(self, row, ctx, refs):
        super().__init__(row, ctx)
        parts = re.split(r"\n\n(?=[A-Z][a-z]+ \d+:\n)", self.state.strip())
        self.item_noun = None
        texts = []
        for k, ptxt in enumerate(parts, 1):
            m = re.match(r"^([A-Z][a-z]+) (\d+):\n(.*)$", ptxt, re.S)
            if not m or int(m.group(2)) != k:
                raise ParseError("batch item %d unreadable" % k)
            self.item_noun = m.group(1).lower()
            texts.append(m.group(3).strip())
        self.n = len(texts)
        rule = low(dict((low(a), b) for a, b in self.card).get("rule", ""))
        m = re.match(r"^the batch holds (\w+) numbered ([a-z]+); each one either (.+) or (does|is) not$", rule)
        if m:
            sg = m.group(3)
            # arbiter fix R1.1 (yn2b/F7_OBJECTIONS.md): a copula property takes 'is X or is not', a verb property
            # 'Vs ... or does not'; the elliptical tail must agree with the property, or the line is not read at all
            if (m.group(4) == "is") != sg.startswith("is "):
                raise ParseError("batch rule tail 'or %s not' does not fit '%s'" % (m.group(4), sg))
            self.plural = m.group(2)
            if NUM.get(m.group(1)) != self.n:
                raise ParseError("rule count %s != items %d" % (m.group(1), self.n))
        else:
            mm = re.match(r"^an? ([a-z]+) (.+?) when\b", low(self.instr))
            if not mm:
                raise ParseError("batch property not found")
            sg = mm.group(2)
            self.plural = mm.group(1) + "s"
        if sg not in MULTI_PRED:
            raise ParseError("unknown batch property: " + sg)
        self.sg = sg
        typ, key, comps, negadj, adj = MULTI_PRED[sg]
        self.lem_pos = lemma_str(sg)
        self.lem_comp = [lemma_str(c) for c in comps]
        self.negadj, self.adj = negadj, adj
        # human labels, in item order (each base text is checked against the item text)
        if len(refs) != self.n:
            raise ParseError("%d refs for %d items" % (len(refs), self.n))
        self.x = []
        for ref, t in zip(refs, texts):
            b = ctx.base(ref, text=t)
            if b is None:
                raise ParseError("no base for " + ref)
            bt = b.get("text")
            if bt is not None and norm(t)[:60] not in norm(bt) and norm(bt)[:60] not in norm(t):
                tail = norm(bt).split(": ", 1)[-1]
                if norm(t)[:60] not in tail and tail[:60] not in norm(t):
                    raise ParseError("item text does not match its base row " + ref)
            if typ == "task":
                if b["kind"] != "prop" or b["task"] != key:
                    raise ParseError("base %s is not about %s" % (ref, key))
                self.x.append(bool(b["val"]))
            else:
                if b["kind"] != "label":
                    raise ParseError("base %s has no label" % ref)
                self.x.append(b["label"] == key)
        for k, v in self.card:
            if low(k) not in SPECIAL_KEYS:
                self.terms[low(k)] = low(v)
                self.names[low(k)] = "term"
        self.docs.add("batch")
        self.finish()

    def subjects(self, s):
        s = re.sub(r"\b" + self.item_noun + r" (\d+)\b", lambda m: "«i%s»" % m.group(1), s)
        s = re.sub(r"\bthe batch\b", "«S»", s)
        return s

    def fit(self, nm):
        if nm not in self.terms:
            raise ParseError("unknown term " + nm)
        v = self.terms[nm]
        m = re.match(r"^a batch in which (.+)$", v)
        if not m:
            raise ParseError("batch term def: " + v)
        s, table = self.lemma(m.group(1))
        # A4 concerns a frame word applied to a universal claim itself; 'the batch fails to count as 'tag K'' is a
        # yes/no claim about the batch whatever quantifier the term's definition uses, so the definition's
        # quantifiers are not counted (A3's exceptive check still applies inside definitions)
        before = self.univ_mixed
        try:
            return self.ev_lemma(s, table, 1)
        finally:
            self.univ_mixed = before

    def pred(self, p, i):
        x = self.x[i - 1]
        p = p.strip()
        if p == self.lem_pos:
            return x
        if p in self.lem_comp:
            return not x
        if p in ("be " + self.negadj, ):
            return not x
        if self.adj and p == "be " + self.adj:
            return x
        if p.startswith("not "):
            return not self.pred(p[4:], i)
        raise ParseError("batch predicate: " + p)

    def preds(self, p, idx=None):
        idx = idx if idx is not None else range(1, self.n + 1)
        return [self.pred(p, i) for i in idx]

    def univ(self, v):
        """arbiter round 3, A4: note a universal claim ('none / no / not a single / all / every / each / only /
        both / neither') evaluated over items that are mixed (some true, some false); see World.frame_guard."""
        if any(v) and not all(v):
            self.univ_mixed += 1
        return v

    def exceptive(self, q, s, p, e, idx, v, lit):
        """arbiter round 3, A3: a universal or negative exceptive ('no X other than X 4 ...', 'none of the Xs apart
        from X 2 ...', 'every X besides X 1 ...') carries the inclusion condition: the excepted item has the property
        the quantifier denies the others (von Fintel 1993; Moltmann 1995). When the excepted item does not, the
        literal set-minus reading and the exceptive reading give different values: refuse the row. Existential
        exceptives ('some / any / at least one X other than ...') have no inclusion condition and stay literal
        (checklist item 31's own example)."""
        if q in ("some", "any", "at least one"):
            return lit
        pe = self.pred(p, e)
        if q in ("no", "none", "not a single"):
            self.univ(v)
            inc = lit and pe
        elif q in ("every", "all"):
            self.univ(v)
            inc = lit and not pe
        else:  # 'not every' / 'not all': the negation of the universal exceptive
            inc = not (all(v) and not pe)
        if inc != lit:
            raise Ambiguous("AMBIGUOUS: exceptive '%s' with %s %d %s the property, so the literal (set-minus) and "
                            "the exceptive (inclusion) readings give different values" %
                            (s, self.item_noun, e, "having" if pe else "lacking"))
        return lit

    def atom(self, s, table, depth):
        IT, ITS = self.item_noun, self.plural
        # counting quantifiers over the whole batch
        m = re.match(r"^(at least|no more than|at most|fewer than|not fewer than|more than|exactly) (\w+) of the (\w+) "
                     + ITS + r" (.+)$", s)
        if m:
            k, n = NUM.get(m.group(2)), NUM.get(m.group(3))
            if n != self.n or k is None:
                raise ParseError("count words")
            c = sum(self.preds(m.group(4)))
            op = m.group(1)
            return {"at least": c >= k, "no more than": c <= k, "at most": c <= k, "fewer than": c < k,
                    "not fewer than": c >= k, "more than": c > k, "exactly": c == k}[op]
        m = re.match(r"^(\w+) or more of the (\w+) " + ITS + r" (.+)$", s)
        if m:
            k, n = NUM.get(m.group(1)), NUM.get(m.group(2))
            if n != self.n:
                raise ParseError("count words")
            return sum(self.preds(m.group(3))) >= k
        m = re.match(r"^few of the (\w+) " + ITS + r" (.+)$", s)
        if m:
            if "'few' means at most one" not in low(self.row.get("card") or ""):
                self.notes.append("FEW_WITHOUT_CARD_READING")
            return sum(self.preds(m.group(2))) <= 1
        INB = r"(?: in «S»)?"
        EXC = r"(?:other than|apart from|besides) «i(\d)»"
        # quantifier over the batch minus one named item (exceptor)
        m = re.match(r"^(some|no|any|every|not a single|at least one|not every) " + IT + r" " + EXC + r" (.+)$", s)
        if m:
            idx = [i for i in range(1, self.n + 1) if i != int(m.group(2))]
            v = self.preds(m.group(3), idx)
            lit = {"some": any(v), "any": any(v), "no": not any(v), "every": all(v), "not a single": not any(v),
                   "at least one": any(v), "not every": not all(v)}[m.group(1)]
            return self.exceptive(m.group(1), s, m.group(3), int(m.group(2)), idx, v, lit)
        m = re.match(r"^(none|all|not all) of the " + ITS + r" " + EXC + r" (.+)$", s)
        if m:
            idx = [i for i in range(1, self.n + 1) if i != int(m.group(2))]
            v = self.preds(m.group(3), idx)
            lit = {"none": not any(v), "all": all(v), "not all": not all(v)}[m.group(1)]
            return self.exceptive(m.group(1), s, m.group(3), int(m.group(2)), idx, v, lit)
        m = re.match(r"^(?:all (\w+) " + ITS + INB + r"|every " + IT + INB + r"|each of the (\w+) " + ITS + r") (.+)$", s)
        if m:
            return all(self.univ(self.preds(m.group(3))))
        m = re.match(r"^not (?:all (\w+) " + ITS + INB + r"|every " + IT + INB + r") (.+)$", s)
        if m:
            if "'not all' means at least one is not" not in low(self.row.get("card") or "") and not self.row.get("options"):
                self.notes.append("NOT_ALL_WITHOUT_CARD_READING")
            return not all(self.preds(m.group(2)))
        # arbiter fix R1.3: 'not one of the five posts ...' takes a count word as 'none of the five posts ...' does;
        # a count word must name the batch size (the same 'count words' check as the counting quantifiers above)
        m = re.match(r"^(?:none of the (?:(\w+) )?" + ITS + r"|no " + IT + r"|not a single " + IT +
                     r"|not one of the (?:(\w+) )?" + ITS + r")" + INB + r" (.+)$", s)
        if m:
            cw = m.group(1) or m.group(2)
            if cw is not None and NUM.get(cw) != self.n:
                raise ParseError("count words")
            return not any(self.univ(self.preds(m.group(3))))
        m = re.match(r"^«i(\d)» and «i(\d)» (be )?not both (.+)$", s)
        if m:
            p = (m.group(3) or "") + m.group(4)
            return not all(self.preds(p, [int(m.group(1)), int(m.group(2))]))
        m = re.match(r"^«S» be make up only of (.+) " + ITS + r"$", s)
        if m:
            a = m.group(1)
            self.univ(self.x)
            if a == self.negadj:
                return not any(self.x)
            if self.adj and a == self.adj:
                return all(self.x)
            raise ParseError("made up only of " + a)
        m = re.match(r"^«S» contain only (.+) " + ITS + r"$", s)
        if m:
            a = m.group(1)
            self.univ(self.x)
            if a == self.negadj:
                return not any(self.x)
            if self.adj and a == self.adj:
                return all(self.x)
            raise ParseError("contains only " + a)
        m = re.match(r"^both «i(\d)» and «i(\d)» (.+)$", s)
        if m:
            return all(self.univ(self.preds(m.group(3), [int(m.group(1)), int(m.group(2))])))
        m = re.match(r"^neither «i(\d)» nor «i(\d)» (.+)$", s)
        if m:
            return not any(self.univ(self.preds(m.group(3), [int(m.group(1)), int(m.group(2))])))
        m = re.match(r"^«i(\d)» or «i(\d)» (.+)$", s)
        if m:
            return any(self.preds(m.group(3), [int(m.group(1)), int(m.group(2))]))
        m = re.match(r"^«i(\d)» (.+)$", s)
        if m and not m.group(2).startswith("not ") and not m.group(2).startswith("never "):
            try:
                return self.pred(m.group(2), int(m.group(1)))
            except ParseError:
                return None
        for rx in FIT_POS_RX:
            m = rx.match(s)
            if m:
                return self.fit_tok(m.group("n"), table)
        for rx in FIT_NEG_RX:
            m = rx.match(s)
            if m:
                return not self.fit_tok(m.group("n"), table)
        return None

    def item_select(self, q, opts):
        m = re.match(r"^.*\bwhich " + self.item_noun + r" (.+)\?$", q)
        if not m:
            raise ParseError("choice question: " + q)
        out = []
        for o in opts:
            mm = re.match(r"^" + self.item_noun + r" (\d+)$", low(o))
            if not mm:
                raise ParseError("option is not an item: " + o)
            s, table = self.lemma("«i%s» " % mm.group(1) + m.group(1))
            out.append(self.ev_lemma(s, table, 0))
        return out


class DevxRecordWorld(World):
    """Kept for rows that are neither cards, batches nor records of a known pack."""
    kind = "devx_record"

    def __init__(self, row, ctx):
        raise ParseError("no world for this row")


# =============================================================================================== devx
# devx rows are free-form English written by a separate author. Their logical forms were written by the decide2
# author from the rendered text alone (yn2b/f7_devx_decide2_lf.json: one LF per row, a fact table per invented
# record); the program evaluates them. Label / item atoms come from the human label of each base text.
DEVX_LF = LEAN / "yn2b" / "f7_devx_decide2_lf.json"
DEVX_TEXT_KEYS = ("state", "instructions", "card", "options")


def devx_text_sha(row):
    """arbiter round 4: sha256 of the rendered text a devx LF is written from (same as f7_devx_decide2_lf_author.py)."""
    return hashlib.sha256(json.dumps([row.get(k) for k in DEVX_TEXT_KEYS], ensure_ascii=False,
                                     sort_keys=True).encode("utf-8")).hexdigest()


class DevxEval:
    def __init__(self, ctx):
        self.ctx = ctx
        self.table = json.loads(DEVX_LF.read_text()) if DEVX_LF.exists() else {"ladders": {}, "rows": {}}

    def item_texts(self, state):
        parts = re.split(r"\n\n(?=[A-Z][a-z]+ \d+:\n)", state.strip())
        return [p.split("\n", 1)[1] if re.match(r"^[A-Z][a-z]+ \d+:\n", p) else p for p in parts]

    def base_label(self, ref):
        if ref.startswith("g:"):
            v = self.ctx.old_by_group(ref)
            if v is None or v == "CONFLICT":
                raise ParseError("no human label for " + ref)
            return v
        r = self.ctx.raw("saferproducts_severity", ref) or self.ctx.raw("wiki_help_routing", ref)
        if r is None:
            raise ParseError("no base row " + ref)
        return r["gold"]

    def decide(self, row):
        lid = row["meta"]["ladder_id"]
        lad = self.table["ladders"].get(lid)
        lf = self.table["rows"].get(row["id"])
        if lad is None or lf is None:
            raise ParseError("devx row not in the parse table")
        refs = row["meta"].get("orig") or []
        at = lad["atoms"]
        typ = at["type"]
        if typ in ("tox", "safer", "wiki"):
            base = self.base_label(refs[0])
            # arbiter round 3: the human label must belong to the text shown (batches were already checked; a
            # single text was not, so a wrong meta.orig would have given decide2 and the builder the same wrong label)
            if refs[0].startswith("g:"):
                if self.ctx._old_group_text is None:
                    self.ctx._load_old()
                if old_key(row["state"]) not in self.ctx._old_group_text.get(refs[0], set()):
                    raise ParseError("state text does not match its base group " + refs[0])
            else:
                rr = self.ctx.raw("saferproducts_severity", refs[0]) or self.ctx.raw("wiki_help_routing", refs[0])
                if rr is None or norm(rr["state"]) != norm(row["state"]):
                    raise ParseError("state text does not match its base row " + refs[0])
        elif typ in ("tox_batch", "wiki_batch", "safer_batch"):
            texts = self.item_texts(row["state"])
            if len(texts) != len(refs):
                raise ParseError("batch items %d vs refs %d" % (len(texts), len(refs)))
            items = [self.base_label(r) for r in refs]
            for r_, t_ in zip(refs, texts):
                if r_.startswith("g:"):
                    if self.ctx._old_group_text is None:
                        self.ctx._load_old()
                    if old_key(t_) not in self.ctx._old_group_text.get(r_, set()):
                        raise ParseError("batch item text does not match its base group " + r_)
                else:
                    rr = self.ctx.raw("saferproducts_severity", r_) or self.ctx.raw("wiki_help_routing", r_)
                    if rr is None or norm(rr["state"])[:80] != norm(t_)[:80]:
                        raise ParseError("batch item text does not match its base row " + r_)
        # arbiter round 4: an LF applies only to the exact text it was written from. The table was keyed by row id
        # only, so a devx rewrite that kept its id would have reused a stale LF without notice.
        shas = self.table.get("text_sha256") or {}
        if shas.get(row["id"]) != devx_text_sha(row):
            raise ParseError("devx row text differs from the text its LF was written from")
        facts = lad.get("facts", {})

        def ev(x):
            op = x[0]
            if op == "NOT":
                return not ev(x[1])
            if op == "AND":
                return all(ev(y) for y in x[1:])
            if op == "OR":
                return any(ev(y) for y in x[1:])
            if op in ("ANY", "NONE", "ALL"):
                v = [ev(y) for y in x[1:]]
                return any(v) if op == "ANY" else (not any(v) if op == "NONE" else all(v))
            if op in ("ATLEAST", "ATMOST", "EXACTLY"):
                c = sum(ev(y) for y in x[2:])
                return {"ATLEAST": c >= x[1], "ATMOST": c <= x[1], "EXACTLY": c == x[1]}[op]
            if op == "AMBIG":
                # arbiter round 3: [AMBIG, note, reading A, reading B] -- two readings of one English construction
                # (A3 exceptive inclusion, A4 'opposite' of a universal claim); refused when they disagree
                a, b = ev(x[2]), ev(x[3])
                if a != b:
                    raise Ambiguous("AMBIGUOUS (devx): " + x[1])
                return a
            if op == "F":
                if x[1] not in facts:
                    raise ParseError("fact missing " + x[1])
                return bool(facts[x[1]][0])
            if op == "L":
                nm = x[1]
                if typ == "tox":
                    if nm in at["pos"]:
                        return bool(base)
                    if nm in at["neg"]:
                        return not base
                    raise ParseError("devx label " + nm)
                if typ == "safer":
                    return base in at["map"][nm]
                if typ == "wiki":
                    return at["map"][nm] == base
                raise ParseError("label atom in a %s ladder" % typ)
            if op == "I":
                k = x[1] - 1
                if typ == "tox_batch":
                    return bool(items[k])
                if typ == "wiki_batch":
                    return at["map"][x[2]] == items[k]
                if typ == "safer_batch":
                    return items[k] in at["map"][x[2]]
                raise ParseError("item atom in a %s ladder" % typ)
            raise ParseError("devx op " + str(op))

        if lf[0] == "CHOICE":
            sel = lf[1] == "true"
            vals = [ev(o) for o in lf[2]]
            opts = row.get("options") or []
            if len(opts) != len(vals):
                raise ParseError("devx choice: %d options, %d LFs" % (len(opts), len(vals)))
            hits = [o for o, v in zip(opts, vals) if v == sel]
            if len(hits) != 1:
                raise ParseError("devx choice: %d options evaluate to %s" % (len(hits), sel))
            return hits[0]
        return 1 if ev(lf) else 0


_DEVX = {}


# =============================================================================================== CLI
def load_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def run_files(files, ctx, meta_files=None):
    """Decide every row; agreement is tallied against the row's gold. The sidecar is read ONLY for reporting
    (rung and checklist items), after the prediction is made."""
    out_preds, report = [], {}
    for name, fn in files.items():
        rows = load_jsonl(fn)
        side = {}
        mf = (meta_files or {}).get(name)
        if mf and Path(mf).exists():
            for m in load_jsonl(mf):
                side[m["id"]] = {"rung": m.get("rung"), "phen": m.get("phen") or []}
        tot = collections.Counter()
        by_rung = collections.defaultdict(collections.Counter)
        by_item = collections.defaultdict(collections.Counter)
        by_kind = collections.defaultdict(collections.Counter)
        dis, unp, notes_c = [], [], collections.Counter()
        for r in rows:
            pred, notes = decide2_row(r, ctx)
            if pred is not None:
                out_preds.append({"id": r["id"], "gold": pred})
            st = "unparsed" if pred is None else ("agree" if pred == r["gold"] else "disagree")
            tot[st] += 1
            sm = side.get(r["id"], {})
            by_rung[sm.get("rung") or (r.get("meta") or {}).get("rung") or "?"][st] += 1
            for it in sm.get("phen", []):
                by_item[str(it)][st] += 1
            by_kind[(r.get("meta") or {}).get("kind") or "devx"][st] += 1
            for n in notes:
                notes_c[n.split(":")[0]] += 1
            if st == "disagree":
                dis.append({"id": r["id"], "gold": r["gold"], "decide2": pred, "notes": notes,
                            "instructions": r["instructions"]})
            elif st == "unparsed":
                unp.append({"id": r["id"], "gold": r["gold"], "error": notes[0] if notes else "",
                            "instructions": r["instructions"]})
        n = len(rows)
        report[name] = {
            "rows": n, "agree": tot["agree"], "disagree": tot["disagree"], "unparsed": tot["unparsed"],
            "agreement": round(tot["agree"] / n, 6) if n else None,
            "by_rung": {k: dict(v) for k, v in sorted(by_rung.items())},
            "by_kind": {k: dict(v) for k, v in sorted(by_kind.items())},
            "by_item": {k: dict(v) for k, v in sorted(by_item.items(), key=lambda x: int(x[0]))},
            "notes": dict(notes_c), "disagreements": dis, "unparsed_rows": unp,
        }
    return out_preds, report


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="yn2b/f7_decide2_preds.jsonl")
    ap.add_argument("--report", default="yn2b/f7_decide2_report.json")
    ap.add_argument("--files", nargs="*", default=["train", "probe", "devx"])
    a = ap.parse_args(argv)
    ctx = Ctx(LEAN)
    files = {k: str(DV / ("f7_%s.jsonl" % k)) for k in a.files}
    metas = {k: str(DV / ("f7_%s_meta.jsonl" % k if k != "train" else "f7_meta.jsonl")) for k in a.files}
    preds, report = run_files(files, ctx, metas)
    with open(LEAN / a.out, "w", encoding="utf-8") as f:
        for p in preds:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    dpath = LEAN / "yn2b" / "f7_decide2_diagnoses.json"
    if dpath.exists():
        report["diagnoses"] = json.loads(dpath.read_text())
    with open(LEAN / a.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    for k, v in report.items():
        if k != "diagnoses":
            print(k, {x: v[x] for x in ("rows", "agree", "disagree", "unparsed", "agreement")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
