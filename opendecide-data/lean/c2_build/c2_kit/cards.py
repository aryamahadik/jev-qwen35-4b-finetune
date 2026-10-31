"""c2_kit/cards.py: compact rule cards (C2_DATA_SPEC 3.0 "Definition styles" and "Length": every row <= 2,000
rendered tokens, family mean <= 800, instructions counted twice; C spec 2.1 definition styles).

Where the tokens go (STAGE_B pilot, real Qwen3.5 tokenizer through c_build/mixer.token_counts): 13 of 15 families
miss the 800 mean (810-1,207). The served prompt (decoder_io cygnet, layout schema_branch_mark) prints
row.instructions TWICE (in the schema and again after the text) and row.card ONCE, under "Definitions:", and it prints
row.card on yes/no rows only (a choice row reads its card only for "- <option text>: <definition>" lines). Every
family except T35 puts its rules in the instructions on every row, so every yes/no row pays for its rules twice.

Three levers, each keeping every rule a row needs (spec 3.0: "every rule the answer needs is stated in the item"):
  1. placement   place_rules(tb, filled, qtype): yes/no rows carry the rules in row.card (printed once, as the
                 definitions block); choice rows keep them in the instructions, the only place a choice row prints
                 them. Same words, same order; only the field changes (T35's layout, G0 M21).
  2. compact     CardItem.compact: a shorter phrasing of the same rule. variant_problems() refuses a variant that
                 drops or adds a slot, a quoted literal, a number, an operator / comparator / quantifier word, or
                 changes the negation count (negcount k_all). The compact style is a FULL card: every item stays.
  3. short       CardItem.short: the terse definition style spec 3.0 allows on about 15% of rows ("a short or no card
                 on about 15% of rows"); still every rule, same checks. "none" (no card at all) only where the
                 family's G0 says the answer needs no stated rule (CardSpec(none_reason=...)); otherwise refused.
Items may carry `when`, a predicate of the row's VISIBLE inputs (e.g. "the request shows a fetch status") that
leaves out an item whose rule cannot apply to the row. It receives the Spec only, never the gold; a card with such
items may not refer to items by number.
draw_style(row_key, shares) is the label-blind style draw (row key only), with the short + none share capped at the
G0's share (default 0.15). token_report(rows) measures a family's rows with the pinned tokenizer and says how much the
rules must shrink to reach the 800 mean after placement.
Adopting a compact phrasing or a new placement changes the card text, so the family re-freezes its G0 card lines
(G0 step 1) and re-runs the pilot; semantics, slots and the gold are unchanged.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable

from . import paths
from . import rows as R
from .distractors import uhash
from .skin import Filled, placeholders
import negcount  # noqa: E402  (on sys.path through c2_kit.paths)

STYLES = ("full", "compact", "short", "none")
SHORT_STYLES = ("short", "none")
SHORT_CAP = 0.15               # spec 3.0: "a short or no card on about 15% of rows"
YES_NO_OPTIONS = ("Yes", "No")  # decoder_io.as_letter_row: a yes/no row's two options
# operator words whose presence a compact or short phrasing must keep (each a regex, matched case-insensitively on
# word boundaries): quantifiers, connectives that change truth conditions, comparators, order words, modals
OPERATORS = (
    r"all", r"any", r"each", r"every", r"none", r"only", r"both", r"either", r"neither", r"nor", r"or",
    r"unless", r"except", r"if", r"otherwise", r"instead", r"same", r"different", r"equal(?:s|ly)?", r"exactly",
    r"at\s+least", r"at\s+most", r"more\s+than", r"less\s+than", r"fewer\s+than", r"no\s+later\s+than",
    r"no\s+earlier\s+than", r"before", r"after", r"on\s+or\s+before", r"on\s+or\s+after", r"within", r"between",
    r"inclusive", r"exclusive", r"including", r"excluding", r"longest", r"shortest", r"first", r"last", r"earliest",
    r"latest", r"highest", r"lowest", r"most", r"least", r"overrides?", r"wins?", r"ties?", r"case", r"ignor(?:e|es|ing)",
    r"may", r"must", r"cannot", r"can", r"should", r"required", r"allowed", r"never", r"always",
)
_QUOTED = re.compile(r'"([^"\n]*)"|\'([^\'\n]*)\'|`([^`\n]*)`')
_NUM = re.compile(r"(?<![\w{])\d+(?:[.,]\d+)*(?![\w}])")
_ITEM_REF = re.compile(r"\bitems?\s+\d+", re.I)
_DEF_LINE = re.compile(r"^- (.+?): ", re.M)


class CardError(ValueError):
    pass


@dataclass(frozen=True)
class CardItem:
    item_id: str
    full: str                                   # the frozen G0 phrasing (template text, may hold {SLOT}s)
    compact: str | None = None                  # same rule, fewer tokens (the compact style)
    short: str | None = None                    # the terse phrasing (the short style)
    when: Callable | None = None                # f(spec) -> bool over VISIBLE inputs; None = always shown

    def text(self, style: str) -> str:
        if style == "full":
            return self.full
        if style == "compact":
            return self.compact or self.full
        if style == "short":
            return self.short or self.compact or self.full
        raise CardError(f"style {style!r} has no item text")


@dataclass(frozen=True)
class CardSpec:
    family: str
    items: tuple
    heads: dict = field(default_factory=dict)   # style -> heading line ("" = none); e.g. {"full": "Rules:"}
    tail: str = ""                              # printed on every style (e.g. the closed-world sentence)
    numbered: bool = True                       # "1. ..." (False: "- ..." bullets)
    none_reason: str | None = None              # the G0's reason a row may carry no card (style "none")
    operators: tuple = ()                       # extra family operator words (regexes) the variants must keep

    def styles(self) -> tuple:
        return STYLES if self.none_reason else STYLES[:3]

    def template(self, style: str, spec=None) -> str:
        """The card template of a style (fill it with skin.fill). spec: the row's Spec, for items with `when`."""
        if style not in self.styles():
            raise CardError(f"{self.family}: style {style!r} not allowed (none needs a G0 reason)")
        if style == "none":
            return ""
        items = [it for it in self.items if it.when is None or (spec is not None and bool(it.when(spec)))]
        if any(it.when is not None for it in self.items) and spec is None:
            raise CardError(f"{self.family}: a card with conditional items needs the row's spec")
        lines = [f"{n}. {it.text(style)}" if self.numbered else f"- {it.text(style)}" for n, it in
                 enumerate(items, 1)]
        head = self.heads.get(style, self.heads.get("full", ""))
        return "\n".join(([head] if head else []) + lines + ([self.tail] if self.tail else []))

    def problems(self) -> list:
        """Every variant keeps its item's meaning markers (variant_problems); conditional cards cite no item numbers;
        no bullet line would bind to the Yes / No options of the served prompt."""
        out = []
        ids = [it.item_id for it in self.items]
        if len(set(ids)) != len(ids):
            out.append("duplicate item ids")
        cond = any(it.when is not None for it in self.items)
        for it in self.items:
            for style, txt in (("compact", it.compact), ("short", it.short)):
                if txt is not None:
                    out += [f"{it.item_id} {style}: {p}" for p in variant_problems(it.full, txt, self.operators)]
            for style in ("full", "compact", "short"):
                t = it.text(style)
                if cond and _ITEM_REF.search(t):
                    out.append(f"{it.item_id} {style}: refers to an item by number in a card with conditional items")
                if not self.numbered and re.match(r"(?:Yes|No): ", t):
                    out.append(f"{it.item_id} {style}: '- {t.split(':')[0]}: ' would define the {t.split(':')[0]} "
                               f"option of a yes/no row")
        if self.none_reason is not None and not self.none_reason.strip():
            out.append("none_reason is empty")
        return out


def _markers(text: str, operators=()) -> dict:
    lit = placeholders(text)
    quoted = {next(g for g in m.groups() if g is not None) for m in _QUOTED.finditer(text)}
    plain = re.sub(r"\{[^{}]*\}", " ", text)
    ops = {}
    for rx in OPERATORS + tuple(operators):
        n = len(re.findall(r"(?<![\w-])(?:" + rx + r")(?![\w-])", plain, re.I))
        if n:
            ops[rx] = n
    return {"slots": {(p.name, p.form) for p in lit}, "quoted": quoted, "numbers": set(_NUM.findall(plain)),
            "operators": set(ops), "k_all": negcount.count(plain).k_all}


def variant_problems(full: str, variant: str, operators=()) -> list:
    """A compact / short phrasing keeps: the same slots (name and form), the same quoted literals, the same numbers,
    the same operator words (present in one <=> present in the other) and the same negation count (k_all)."""
    a, b = _markers(full, operators), _markers(variant, operators)
    out = []
    for k, what in (("slots", "slots"), ("quoted", "quoted literals"), ("numbers", "numbers"),
                    ("operators", "operator words")):
        if a[k] != b[k]:
            lost, new = sorted(map(str, a[k] - b[k])), sorted(map(str, b[k] - a[k]))
            out.append(f"{what} differ (dropped {lost}, added {new})")
    if a["k_all"] != b["k_all"]:
        out.append(f"negation count k_all {a['k_all']} -> {b['k_all']}")
    if not variant.strip():
        out.append("empty variant")
    return out


def draw_style(row_key: str, shares: dict, *, short_cap: float = SHORT_CAP) -> str:
    """The card style of a row from the row key only (label-blind). shares: {style: share}, summing to 1; the short
    + none share is capped at the G0's share (default 0.15, spec 3.0)."""
    if set(shares) - set(STYLES) or any(v < 0 for v in shares.values()):
        raise CardError(f"shares over {STYLES}, non-negative")
    if abs(sum(shares.values()) - 1.0) > 1e-9:
        raise CardError("card style shares must sum to 1")
    if sum(shares.get(s, 0.0) for s in SHORT_STYLES) > short_cap + 1e-12:
        raise CardError(f"short + none share {sum(shares.get(s, 0.0) for s in SHORT_STYLES)} > {short_cap} (G0 share)")
    u, acc = uhash(row_key, "card_style"), 0.0
    for s in STYLES:
        acc += shares.get(s, 0.0)
        if u < acc:
            return s
    return max(shares, key=shares.get)


def place_rules(tb, filled, qtype: str) -> str:
    """Put a filled card where the served prompt prints it once: row.card on yes/no rows, the head of the
    instructions on choice rows (call it BEFORE the question wording is added). Returns the field used."""
    text = filled.text if isinstance(filled, Filled) else str(filled)
    if not text:
        return "none"
    if qtype == "noul":
        bad = [m.group(1) for m in _DEF_LINE.finditer(text) if m.group(1) in YES_NO_OPTIONS]
        if bad:
            raise CardError(f"card line '- {bad[0]}: ...' would be printed as the definition of the {bad[0]} option")
        if tb.text("card"):
            raise CardError("the row already has a card")
        tb.add("card", filled)
        return "card"
    if qtype != "choice":
        raise CardError(f"qtype {qtype!r}")
    if tb.text("instructions"):
        raise CardError("place the rules before the question wording")
    tb.add("instructions", filled).add("instructions", "\n\n")
    return "instructions"


def split_rules(row: dict) -> tuple:
    """(rules text, question text) of a rendered row in either layout, for a solver-B parser: a row with a card ->
    (card, instructions); otherwise the instructions split at their LAST blank line (a one-paragraph instruction is
    all question). A family whose rules span paragraphs keeps them in one block so this split stays exact."""
    if row.get("card"):
        return row["card"], row.get("instructions") or ""
    ins = row.get("instructions") or ""
    if "\n\n" not in ins:
        return "", ins
    rules, question = ins.rsplit("\n\n", 1)
    return rules, question


def defs_style(field_used: str, style: str) -> str:
    """The meta.defs_style value of a row: rules_in_<card|instructions>_<style> (or no_card)."""
    return "no_card" if field_used == "none" or style == "none" else f"rules_in_{field_used}_{style}"


# ------------------------------------------------------------------------------------------------ measurement

def _tokenizer():
    """The pinned Qwen3.5-4B tokenizer (c_build/mixer.TOKENIZER, sha-checked; read-only reuse) or None."""
    try:
        for p in (paths.LEAN, paths.LEAN / "c_build"):
            if str(p) not in sys.path:
                sys.path.append(str(p))
        import mixer as mx
        from tokenizers import Tokenizer
        if mx.sha256_file(mx.TOKENIZER) != mx.TOKENIZER_SHA:
            return None, None
        return mx, Tokenizer.from_file(str(mx.TOKENIZER))
    except (Exception, SystemExit):  # noqa: BLE001
        return None, None


def default_rules_of(row: dict) -> str:
    """The rules part of a row's instructions: everything before the last blank line (the question wording is the
    last paragraph in the kit's render pattern); "" when the instructions are one paragraph."""
    ins = row.get("instructions") or ""
    return ins.rsplit("\n\n", 1)[0] if "\n\n" in ins else ""


def token_report(rows: list, *, bar: int = 800, rules_of: Callable[[dict], str] | None = None,
                 real: bool = True) -> dict:
    """Mean rendered tokens of a family's rows (the pilot's spec_3_0 count: the cygnet prompt, instructions twice),
    split by field, and the two projections the levers give:
      after_placement    yes/no rows whose rules sit in the instructions move them to row.card (counted once)
      rules_ratio_needed after placement, the factor the rules text must shrink to (compact / short phrasing) for
                         the mean to reach `bar` (None: unreachable even with no rules; 1.0: already there)."""
    rules_of = rules_of or default_rules_of
    mx, tok = _tokenizer() if real else (None, None)
    if tok is not None:
        class _NoLog:
            def record(self, *_a, **_k):
                pass
        totals = mx.token_counts(_NoLog(), rows)
        count = lambda s: len(tok.encode(s or "", add_special_tokens=False).ids)   # noqa: E731
        how = "mixer.token_counts (pinned Qwen3.5-4B tokenizer)"
    else:
        totals = [R.approx_tokens(r) for r in rows]
        count = lambda s: -(-len(s or "") // int(R.CHARS_PER_TOKEN))               # noqa: E731
        how = "rows.approx_tokens (tokenizer unavailable)"
    n = len(rows)
    if not n:
        return {"rows": 0, "counted_by": how}
    f = Counter()
    save_place, rules_yn, rules_ch = 0, 0, 0
    nyn = 0
    for r in rows:
        ins, rul = count(r.get("instructions")), count(rules_of(r))
        f["state"] += count(r.get("state"))
        f["instructions_x2"] += 2 * ins
        f["options_x2"] += 2 * count(" ".join(r.get("options") or []))
        if r["qtype"] == "noul":
            nyn += 1
            f["card_yes_no"] += count(r.get("card"))
            if not r.get("card"):
                save_place += rul
                rules_yn += rul
            else:
                rules_yn += count(r.get("card"))
        else:
            rules_ch += rul
    mean = sum(totals) / n
    after = mean - save_place / n
    rules_cost = (rules_yn + 2 * rules_ch) / n          # what the rules cost per row after placement
    if after <= bar:
        ratio = 1.0
    elif rules_cost <= 0 or after - rules_cost > bar:
        ratio = None
    else:
        ratio = round(1 - (after - bar) / rules_cost, 3)
    return {"rows": n, "counted_by": how, "bar": bar, "mean": round(mean, 1), "max": max(totals),
            "yes_no_share": round(nyn / n, 4),
            "field_means": {k: round(v / n, 1) for k, v in sorted(f.items())},
            "rules_mean": {"yes_no": round(rules_yn / max(1, nyn), 1),
                           "choice": round(rules_ch / max(1, n - nyn), 1)},
            "after_placement": round(after, 1), "rules_ratio_needed": ratio,
            "pass": mean <= bar}


def style_report(rows: list, *, short_cap: float = SHORT_CAP) -> dict:
    """Realised card styles (meta.defs_style) and the short / no-card share next to the G0 share (report only: spec
    3.0 says "about 15%"; the draw itself is capped by draw_style)."""
    c = Counter(str(r["meta"].get("defs_style")) for r in rows)
    n = len(rows) or 1
    short = sum(v for k, v in c.items() if k.endswith("_short") or k in ("no_card", "short_card"))
    return {"defs_styles": dict(c.most_common()), "short_or_none_share": round(short / n, 4), "g0_share": short_cap,
            "verdict": "report"}
