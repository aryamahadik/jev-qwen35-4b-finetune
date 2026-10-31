"""c2_kit/gsl.py: G-SL, the slot lint and fact-lock (C2_DATA_SPEC 6.3 "New in C2"; bar 100%, else the row is dropped).

Mode T skins (lint_template, role "skin"):
  - placeholders: well-formed; every one declared; every declared slot appears as often as the skin requires
    (default exactly once); {N|sg|pl} agreement only on a count slot;
  - grammar: no literal "a"/"an" right before a value placeholder (use {a|X}); no free word right after a count
    placeholder (the count slot carries its unit; {N|sg|pl} for other agreeing words);
  - outside the slots, the spec list (CORE; never excepted): no number (digits, number words, ordinals), date or
    time pattern, month or weekday name, relative-time word, quantity, quantifier, modal, hedge, capitalised name,
    status word or gold-label word; currency and percent signs count as numbers; no URL, domain or e-mail;
  - EXTENDED (the kit's stricter extras): more relative-time / quantity / status / hedge words, operator words
    (if, unless, except, otherwise ...) and any negation cue (negcount). A family may except an EXTENDED word (or the
    whole "negation" check) only through plugin.GSL_EXCEPTIONS {word: reason}, listed in its frozen G0-lite spec;
  - names: a capitalised word that does not start a sentence, line, list item or label is a name unless it is "I"
    or in plugin.NAME_ALLOW (the pack's glossary of capitalised non-names).
Question wordings (role "wording") ask the question, so modal, status, gold-label, quantifier, quantity, operator and
negation words are their content: their meaning is admitted by G-LEX extraction (lexicon kind "question"), not by
this lint. They are still linted for placeholders, grammar, numbers, dates, relative time, hedges and names.
Attack lines (role "attack"): placeholders, grammar, numbers and dates (they must add no fact).
Program templates (role "program", Claude-written code): placeholders only.

Slot values (lint_values): names and ids hold no negation cue; every value renders and parses back in every form.
Mode F (lint_freeform): every slot value appears verbatim (>= its required count); outside the values the text adds
no number, date, month or weekday, id-like token, URL or e-mail, currency sign, gold-label word or negation cue
(negcount k_all of the text outside the values must be 0). Only the skin's own region of the row is read.

check_row(rr, ctx, plugin, spec) runs every check that applies to one RenderedRow and returns its violations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import paths  # noqa: F401  (negcount on sys.path)
import negcount  # noqa: E402
from . import skin as K  # noqa: E402
from . import slots as S  # noqa: E402

CORE = {
    "number": {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
               "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
               "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
               "billion", "dozen", "dozens", "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
               "eighth", "ninth", "tenth", "twice", "thrice", "half"},
    "relative_time": {"today", "tonight", "tomorrow", "yesterday", "ago", "now", "currently", "recently", "lately",
                      "soon", "earlier", "later", "previously", "overdue", "upcoming", "next", "last"},
    "quantity": {"several", "couple", "few", "fewer", "fewest", "many", "much", "more", "most", "less", "least",
                 "lots", "plenty", "multiple", "numerous", "percent", "percentage", "majority", "minority"},
    "quantifier": {"all", "every", "each", "some", "any", "none", "no", "both", "either", "neither", "only", "always",
                   "never", "sometimes", "usually", "often", "rarely", "seldom", "whenever", "everyone", "everybody",
                   "everything", "anyone", "anybody", "anything", "someone", "somebody", "something", "nobody",
                   "nothing"},
    "modal": {"must", "may", "might", "can", "ca", "cannot", "could", "should", "shall", "will", "wo", "would",
              "ought", "need", "needs", "needed", "mustn", "shouldn", "allowed", "permitted", "required", "mandatory",
              "optional", "forbidden", "prohibited"},
    "hedge": {"maybe", "perhaps", "probably", "possibly", "likely", "unlikely", "apparently", "seemingly", "seems",
              "seem", "seemed", "supposedly", "presumably", "allegedly", "reportedly", "roughly", "approximately",
              "nearly", "almost", "somewhat", "guess", "think", "believe", "suspect", "unsure", "uncertain"},
    "status": {"approved", "denied", "allowed", "rejected", "accepted", "confirmed", "pending", "completed", "failed",
               "succeeded", "successful", "cancelled", "canceled", "expired", "revoked", "verified", "unverified",
               "paid", "unpaid", "refunded", "eligible", "ineligible", "entitled", "kept", "broken", "waived",
               "granted", "authorized", "authorised", "unauthorized", "unauthorised", "valid", "invalid", "void",
               "legitimate", "fake", "fraudulent", "resolved", "unresolved", "queued", "blocked"},
}
EXTENDED = {
    "relative_time": {"shortly", "afterwards", "already", "yet", "formerly", "morning", "afternoon", "evening",
                      "night", "midnight", "noon", "midday", "overnight", "weekend", "daily", "weekly", "monthly",
                      "yearly", "annually", "hourly", "immediately", "asap", "past"},
    "quantity": {"handful", "bunch", "various", "bulk", "partial", "partially", "entire", "entirely", "whole",
                 "extra", "additional", "another", "double", "triple", "single", "pair", "quarter", "total",
                 "minimum", "maximum"},
    "modal": {"able", "unable", "gotta"},
    "status": {"approve", "approval", "deny", "denial", "allow", "reject", "accept", "confirm", "confirmation",
               "complete", "done", "finished", "fail", "failure", "success", "successfully", "ok", "okay", "cancel",
               "expire", "revoke", "active", "inactive", "open", "opened", "closed", "processed", "delivered",
               "refund", "settled", "outstanding", "breached", "late", "superseded", "compliant", "noncompliant",
               "genuine", "fraud", "grant", "waive", "block", "eligibility"},
    "operator": {"if", "unless", "except", "excluding", "otherwise", "provided", "providing", "regardless",
                 "instead"},
    "hedge": {"assume", "assumes", "assumed", "appear", "appears", "appeared"},
}
NEGATION = "negation"
BIGRAMS = {"modal": {("have", "to"), ("has", "to"), ("had", "to"), ("got", "to")},
           "hedge": {("sort", "of"), ("kind", "of")}}
ALL_WORD_CATS = ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator")
ROLE_CATS = {
    "skin": set(ALL_WORD_CATS) | {"date", "name", "gold_label", "negation", "symbols", "grammar"},
    "wording": {"number", "relative_time", "hedge", "date", "name", "symbols", "grammar"},
    "attack": {"number", "date", "symbols", "grammar"},
    "program": set(),
}
MONTHS = set(S.MONTHS) | set(S.MONTHS_ABBR) | {"Sept"}
WEEKDAYS = set(S.WEEKDAYS) | {"Mon", "Tue", "Tues", "Wed", "Thu", "Thur", "Thurs", "Fri", "Sat", "Sun"}
FUNCTION_WORDS = {"of", "in", "out", "and", "or", "to", "for", "from", "per", "at", "on", "by", "with", "into",
                  "onto", "over", "under", "after", "before", "than", "as", "the", "a", "an", "is", "are", "was",
                  "were", "be", "that", "this", "these", "those", "which", "who", "it", "its", "via", "through"}

_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_DATEPAT = re.compile(r"\b\d{1,4}[-/.]\d{1,2}(?:[-/.]\d{1,4})?\b|\b\d{1,2}:\d{2}\b")
_SIGNS = re.compile(r"[$€£¥%]")
_URLMAIL = re.compile(r"https?://|www\.|\b[\w.+-]+@[\w-]+\.[\w.]+\b|\b[a-z0-9-]+\.(?:com|net|org|io|example|test)\b",
                      re.I)
_IDLIKE = re.compile(r"\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9][A-Za-z0-9_-]*\b")
_MARK = "\x00"


@dataclass(frozen=True)
class Violation:
    rule: str
    detail: str


def check_exceptions(exc: dict) -> list:
    """Problems with a family's GSL_EXCEPTIONS (EXTENDED words or "negation" only, each with a reason)."""
    probs = []
    core = set().union(*CORE.values())
    ext = set().union(*EXTENDED.values())
    for w, why in (exc or {}).items():
        if w in core:
            probs.append(f"G-SL exception {w!r} is a CORE word (spec list): never excepted")
        elif w not in ext and w != NEGATION:
            probs.append(f"G-SL exception {w!r} is not an EXTENDED word")
        if not str(why).strip():
            probs.append(f"G-SL exception {w!r} has no reason")
    return probs


def _literal(template: str) -> str:
    return K.PH_RE.sub(_MARK, template)


def _sentence_starts(lit: str) -> set:
    return {m.end() for m in re.finditer(r"(?:^|[.!?:;|]\s+|\n)[\s\-*#>\"'(\[]*", lit)}


def _label_forms(label_words: tuple) -> set:
    out = set()
    for w in label_words:
        w = w.lower().strip()
        if not w or " " in w:
            continue
        out |= {w, w + "s", w + "es", w + "ed", w + "d", w + "ing"}
        if w.endswith("e"):
            out.add(w[:-1] + "ing")
        if w.endswith("y"):
            out |= {w[:-1] + "ies", w[:-1] + "ied"}
    return out


def _word_hits(lit: str, cats: set, label_words: tuple, exceptions: dict, name_allow: tuple) -> list:
    out = []
    starts = _sentence_starts(lit)
    allow = set(exceptions or {})
    names_ok = set(name_allow or ()) | {"I"}
    toks = [(m.group(), m.start()) for m in _WORD.finditer(lit)]
    low = [t.lower() for t, _ in toks]
    labels = _label_forms(label_words) if "gold_label" in cats else set()
    for i, (t, pos) in enumerate(toks):
        lw = low[i]
        base = lw.split("'")[0]
        for cat, words in CORE.items():
            if cat in cats and (base in words or lw in words):
                out.append(Violation(cat, t))
        for cat, words in EXTENDED.items():
            if cat in cats and (base in words or lw in words) and lw not in allow and base not in allow:
                out.append(Violation(cat, t))
        if "date" in cats and t in MONTHS:
            out.append(Violation("date", f"month {t}"))
        if "date" in cats and t in WEEKDAYS:
            out.append(Violation("date", f"weekday {t}"))
        if lw in labels:
            out.append(Violation("gold_label", t))
        if ("name" in cats and t[0].isupper() and pos not in starts and t not in names_ok and t not in MONTHS
                and t not in WEEKDAYS):
            out.append(Violation("name", t))
        if i + 1 < len(toks):
            for cat, pairs in BIGRAMS.items():
                if cat in cats and (lw, low[i + 1]) in pairs:
                    out.append(Violation(cat, f"{t} {toks[i + 1][0]}"))
    if "gold_label" in cats:
        for phrase in (w for w in label_words if " " in w):
            if re.search(r"(?<![a-z])" + re.escape(phrase.lower()) + r"(?![a-z])", lit.lower()):
                out.append(Violation("gold_label", phrase))
    return out


def _sym_hits(lit: str, cats: set) -> list:
    out = []
    if "number" in cats and re.search(r"\d", lit):
        out.append(Violation("number", "digit"))
    if "date" in cats and _DATEPAT.search(lit):
        out.append(Violation("date", "date or time pattern"))
    if "symbols" in cats and _SIGNS.search(lit):
        out.append(Violation("number", "currency or percent sign"))
    if "symbols" in cats and _URLMAIL.search(lit):
        out.append(Violation("id", "url, domain or e-mail"))
    return out


def _role(sk) -> str:
    return {"skin": "skin", "wording": "wording", "attack": "attack", "program": "program"}[sk.kind]


def lint_template(sk, *, label_words: tuple = (), exceptions: dict | None = None, name_allow: tuple = ()) -> list:
    """Every G-SL violation of one Mode T template; the checks follow the template's role (sk.kind)."""
    cats = ROLE_CATS[_role(sk)]
    v = []
    text = sk.text
    for b in K.malformed(text):
        v.append(Violation("placeholder", f"malformed {b!r}"))
    decl = sk.decl
    used = {}
    phs = [p for p in K.placeholders(text) if p.mod != "!bad"]
    for p in phs:
        if p.name not in decl:
            v.append(Violation("placeholder", f"undeclared {p.name}"))
            continue
        if p.agree and decl[p.name] != "count":
            v.append(Violation("grammar", f"agreement word on non-count slot {p.name}"))
        if p.form and decl[p.name] != "category" and p.form not in (S.FORMS.get(decl[p.name]) or ()):
            v.append(Violation("placeholder", f"{p.name}: unknown form {p.form}"))
        if not p.agree:
            used[p.name] = used.get(p.name, 0) + 1
    for name in decl:
        lo, hi = sk.count_range(name)
        if not lo <= used.get(name, 0) <= hi:
            v.append(Violation("count", f"{name} appears {used.get(name, 0)}x, required {lo}-{hi}"))
    if "grammar" in cats:
        for p in phs:
            if p.agree or p.name not in decl:
                continue
            if re.search(r"(?:^|[^A-Za-z])(?:a|an|A|An)\s+$", text[:p.start]):
                v.append(Violation("grammar", f"literal article before {{{p.name}}}: use {{a|{p.name}}}"))
            if decl[p.name] == "count" and p.form not in ("adj", "adj_words"):
                nxt = re.match(r"\s+([A-Za-z]+)", text[p.end:])
                if nxt and nxt.group(1).lower() not in FUNCTION_WORDS:
                    v.append(Violation("grammar", f"word {nxt.group(1)!r} after count {{{p.name}}}: "
                                                  "put units in the slot"))
    lit = _json_literal_strings(text) if sk.escape == "json" else _literal(text)
    v += _sym_hits(lit, cats)
    v += _word_hits(lit, cats, label_words, exceptions or {}, name_allow)
    if "negation" in cats and NEGATION not in (exceptions or {}):
        k = negcount.count(lit.replace(_MARK, " ")).k_all
        if k:
            v.append(Violation("negation", f"{k} negation cue(s) outside the slots"))
    return v


def _json_literal_strings(text: str) -> str:
    """JSON skins: the literal words a reader sees (keys and string contents), placeholders marked."""
    lit = _literal(text)
    return "\n".join(m.group(1) for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', lit))


def lint_values(slots: dict) -> list:
    v = []
    for name, s in slots.items():
        if s.kind in ("name", "id") and negcount.k_all(str(s.value)):
            v.append(Violation("value", f"{name}: negation cue in a {s.kind}"))
        if s.kind == "clause":
            continue
        if not S.roundtrip_ok(s):
            v.append(Violation("value", f"{name}: a form does not parse back"))
        if any(c in S.render(s, f) for f in S.forms(s) for c in "{}\n"):
            v.append(Violation("value", f"{name}: brace or line break in the value"))
    return v


def lint_freeform(text: str, fills: dict, *, min_counts: dict | None = None, label_words: tuple = ()) -> list:
    """Mode F fact-lock over one skin's text. fills: {slot: its rendered value in this text}."""
    v = []
    occ = K.locate(text, fills)
    for name, spans in occ.items():
        need = (min_counts or {}).get(name, 1)
        if len(spans) < need:
            v.append(Violation("slot_missing", f"{name}: {len(spans)} verbatim occurrence(s), need {need}"))
    out, pos = [], 0
    for a, b in sorted((a, b) for spans in occ.values() for a, b in spans):
        if a < pos:
            continue
        out += [text[pos:a], _MARK]
        pos = b
    out.append(text[pos:])
    rest = "".join(out)
    v += _sym_hits(rest, {"number", "date", "symbols"})
    for m in _IDLIKE.finditer(rest):
        v.append(Violation("id", m.group()))
    words = _WORD.findall(rest)
    for t in words:
        if t in MONTHS:
            v.append(Violation("date", f"month {t}"))
        if t in WEEKDAYS:
            v.append(Violation("date", f"weekday {t}"))
        if t.lower() in CORE["number"]:
            v.append(Violation("number", t))
    labels = _label_forms(label_words)
    v += [Violation("gold_label", t) for t in words if t.lower() in labels]
    k = negcount.count(rest.replace(_MARK, " ")).k_all
    if k:
        v.append(Violation("negation", f"{k} negation cue(s) added outside the slot values"))
    return v


def check_row(rr, ctx, plugin, spec) -> list:
    """G-SL for one RenderedRow: each Haiku-written piece (skin, wording, attack line) and the spec's slot values."""
    v = []
    for sid in (rr.skin_id, rr.wording_id, rr.attack_id):
        if not sid:
            continue
        sk = ctx.skin(sid)
        if sk.author_mode == "T":
            for x in lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                   name_allow=plugin.NAME_ALLOW):
                v.append(Violation(x.rule, f"{sid}: {x.detail}"))
            continue
        if sid not in rr.regions:
            v.append(Violation("region", f"{sid}: Mode F text has no recorded region in the row"))
            continue
        fld, a, b = rr.regions[sid]
        region = rr.row[fld][a:b]
        fills = {sp.slot: rr.row[fld][sp.start:sp.end] for sp in rr.spans
                 if sp.field == fld and a <= sp.start and sp.end <= b and sp.slot in sk.decl and sp.role == "value"}
        for name in sk.decl:
            fills.setdefault(name, S.render(spec.all_slots()[name], rr.forms.get(name)))
        for x in lint_freeform(region, fills, label_words=plugin.LABEL_WORDS):
            v.append(Violation(x.rule, f"{sid}: {x.detail}"))
    return v + lint_values(spec.all_slots())
