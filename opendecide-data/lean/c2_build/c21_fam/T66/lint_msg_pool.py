"""Lint of the T66 MSG commit-message pool (pools/msg_messages.json), run at creation and after every wording change.

Fails (exit 1) if any template
  * is shared (the normalised text, conventional-commit prefix removed, appears twice in the file, so also across kinds), or
  * is too similar to a template of ANOTHER kind (token Jaccard >= 0.5; slots count as shared tokens, prefix words are kept: the conservative reading of the NO-row rule), or
  * misses or misuses its slots (style I must carry {fn}, style N no identifier slot (numbers only); only the kind's own slots, msg_spec.KIND_SLOTS; the template must render), or
  * names a different kind's verb / object, or fails to name its own (KIND_PATTERNS below: the lint's own closed vocabulary of kind words, written for this check only), or
  * is a question, has < 4 or > 16 rendered tokens, contains a forbidden internal id (config.FORBIDDEN_IDS), or has a stored dev / dev2 split that differs from the seeded-hash rule,
  * lacks the REQUIRED kind phrase (the G0-lite kind phrase and its object word, see REQUIRED) or contains a word of FORBIDDEN (words that read as another kind to Solver B, learned in the dev
    rounds: "refactor", "descriptive", "optional" ... see FORBIDDEN).
Also checks: >= 40 templates per kind, each half present in the file (dev, dev2, holdout) has >= 20 templates per kind and >= 10 per (kind, style), per-kind mean length within 1.5 tokens of the pool mean.

Run (from c21_fam/):  PYTHONDONTWRITEBYTECODE=1 python3 -m T66.lint_msg_pool [--pool PATH]
"""
import argparse
import collections
import itertools
import re
import sys

from . import config as C
from . import msg_pool as MP
from . import msg_spec as MSG

MIN_PER_KIND, MIN_PER_HALF, MIN_PER_STYLE_HALF = 40, 20, 10
TRIV_TOKENS, MIN_TRIV_PER_TOKEN = range(5, 11), 2          # CH-trivial NO messages are matched to the true message in token count and style (Opus ruling Q8 R3): every half needs
                                                          # >= 2 templates per (trivial kind, style, token count 5..10) (about 6 or more, spread over the character range, is what makes matching reliable), or groups cannot be matched
MAX_JACCARD = 0.5                       # exclusive: Jaccard must be < 0.5
LEN_RANGE = (4, 16)
MEAN_LEN_TOL = 1.5

_NEG = r"(?:guard\w*|reject\w*|validat\w*|negative|non-negative|refus\w*|fail(?:s)? (?:fast|early|loudly)|precondition|sanity|raise[sd]?|raising|throw\w*|bail\w*|defensive|below zero)"
_REQ = (r"(?:required|require[sd]?|mandatory|compulsory|explicit\w*|no default|not optional|no longer optional"
        r")")
KIND_PATTERNS = {
    "CH-1": r"\b" + _NEG + r"\b|< 0|>= 0",
    "CH-2": r"\b(?:off[- ]by[- ]one|loops?|looping|iterat\w*|inclusive|range|extra pass|undercount)\b",
    "CH-3": r"\b(?:renam\w*|name[sd]?|naming|called)\b",
    "CH-5": None,                                           # "default" without any CH-6 word: computed in matches()
    "CH-6": r"\b" + _REQ,
    "CH-8": r"\b(?:messages?|wording|reword\w*|rephras\w*|(?:error|exception|failure) (?:text|string))\b",
    "CH-9": r"\b(?:append\w*|entry|entries|log|logs|logged|logging|logger|record\w*|emit\w*|marker\w*|trace|tracing|debug)\b",
    "CH-10": r"\b(?:constants?|multipl\w*|factor|coefficient|scal(?:e|es|ing)|magic number)\b|\b(?:\d+|\{num_\w+\})x\b",
    "fmt": r"\b(?:whitespace|spacing|spaces?|blanks?|format\w*|reformat\w*|style|layout|re-indent|cosmetic|tidy|operators?)\b",
    "comment": r"\bcomment\w*\b",
    "doc": r"\b(?:docstrings?|doc string|docs|documentation|document\w*)\b",
}
_DEFAULT = re.compile(r"\bdefault\w*\b")

# The kind phrase every template must carry (G0-lite: add guard / fix off-by-one / rename symbol / change default / make parameter required / change message text / add logging call /
# change constant, plus the trivial hunks): ALL listed patterns must match. Written from the dev rounds: wordings without these read as "kind not decisive" to Solver B.
REQUIRED = {
    "CH-1": [r"\b(?:guard|validat\w*|reject\w*|precondition)\b", r"\bnegative\b|< 0"],
    "CH-2": [r"\boff-by-one\b"],
    "CH-3": [r"\brenam\w*"],
    "CH-5": [r"\bdefault\w*"],
    "CH-6": [r"\b(?:required|mandatory) parameter\b"],
    "CH-8": [r"\b(?:\w*error|failure|exception) (?:message|text|wording)\b"],
    "CH-9": [r"\blog\w*"],
    "CH-10": [r"\b(?:constants?|multipl\w*|factor|coefficient|scal(?:e|es|ing)|magic number)\b"],
    "fmt": [r"\b(?:reformat\w*|formatting)\b"],
    "comment": [r"\bcomment\b"],
    "doc": [r"\bdocstring"],
}
# Words that read as ANOTHER kind (or as noise) to Solver B; (pattern, kinds that may use it). Evidence: abstain lifts in dev rounds 4-6 and the first holdout run.
ALL_KINDS = {"CH-1", "CH-2", "CH-3", "CH-5", "CH-6", "CH-8", "CH-9", "CH-10", "fmt", "comment", "doc"}
FORBIDDEN = [                           # (pattern, kinds that may NOT use it)
    (r"\brefactor\w*|\bdescriptive\b|\bself-explanatory\b", ALL_KINDS - {"CH-3"}),
    (r"\btweak\w*", ALL_KINDS - {"CH-10"}),
    (r"\bhint\b|\bpurpose\b|\bcommentary\b|\bownership\b|\bannotate\b|\bleave\b|\bexplain\w*", {"comment"}),
    (r"\bclarif\w*|\bunclear\b|\bpick\b|\bcarries\b|\bshown\b|\breport\w*|\bon\b", {"CH-8"}),
    (r"\boptional\b|\bimplicit\b|\bdrop\b|\benforce\b|\bturn\w*|\btakes\b|\banymore\b|\bforce\b|\bpass\b", {"CH-6"}),
    (r"\bsome\b|\bgive\b|\bput\b|\bbeen\b|\btop\b|\btext\b|\bshort\b|\bcode\b", {"doc"}),
    (r"\bsome\b|\bhint\b", {"CH-8", "comment"}),
]


def matches(text):
    """Kinds whose kind words the template contains."""
    t = text.lower()
    out = set()
    for kind, pat in KIND_PATTERNS.items():
        if kind == "CH-5":
            if _DEFAULT.search(t) and not re.search(KIND_PATTERNS["CH-6"], t):
                out.add(kind)
        elif re.search(pat, t):
            out.add(kind)
    return out


def dummy_slots():
    return {s: "X%s" % s.upper().replace("_", "") for s in MSG.SLOT_NAMES}


def lint(doc):
    """-> (problems, report dict)."""
    bad, rep = [], {}
    items = []                                                # (kind, template)
    for kind, body in doc["kinds"].items():
        for t in body["templates"]:
            items.append((kind, t))
    kinds = [k for k in MP.KINDS]
    if set(doc["kinds"]) != set(kinds):
        bad.append("kinds differ from the expected set %s" % (kinds,))
    # ---- counts and split balance
    cnt = collections.Counter()
    for kind, t in items:
        cnt[(kind,)] += 1
        cnt[(kind, t["split"])] += 1
        cnt[(kind, t["style"], t["split"])] += 1
    present = [h for h in ("dev", "dev2", "holdout") if any(t["split"] == h for _k, t in items)]
    min_kind = MIN_PER_KIND if any(t["split"] in ("dev", "dev2") for _k, t in items) else MIN_PER_HALF         # a file with only the (freshly written) holdout half needs 20 per kind
    for kind in kinds:
        if cnt[(kind,)] < min_kind:
            bad.append("%s has %d templates (< %d)" % (kind, cnt[(kind,)], min_kind))
        for h in present:
            if cnt[(kind, h)] < MIN_PER_HALF:
                bad.append("%s %s half has %d templates (< %d)" % (kind, h, cnt[(kind, h)], MIN_PER_HALF))
            for st in MP.STYLES:
                if cnt[(kind, st, h)] < MIN_PER_STYLE_HALF:
                    bad.append("%s style %s %s half has %d templates (< %d)" % (kind, st, h, cnt[(kind, st, h)], MIN_PER_STYLE_HALF))
    for kind in MSG.TRIV_IDS:                                                           # token-count coverage of the trivial kinds, per half
        for h in present:
            for st in MP.STYLES:
                tc = collections.Counter()
                for k, t in items:
                    if k == kind and t["split"] == h and t["style"] == st:
                        tc[len(t["text"].format(**dummy_slots()).split())] += 1
                for n in TRIV_TOKENS:
                    if tc[n] < MIN_TRIV_PER_TOKEN:
                        bad.append("%s style %s %s half has %d templates of %d tokens (< %d): CH-trivial messages cannot be matched to true messages of that length" % (kind, st, h, tc[n], n, MIN_TRIV_PER_TOKEN))
    rep["counts"] = {k: dict({"all": cnt[(k,)]}, **{h: cnt[(k, h)] for h in present}) for k in kinds}
    # ---- stored split == seeded-hash rule
    for kind in kinds:
        for st in MP.STYLES:
            texts = [t["text"] for k, t in items if k == kind and t["style"] == st and t["split"] in ("dev", "dev2")]
            want = MP.split_ranks(kind, texts)
            for k, t in items:
                if k == kind and t["style"] == st and t["split"] in ("dev", "dev2") and want[t["text"]] != t["split"]:
                    bad.append("%s: stored split %r differs from the seeded-hash rule" % (t["id"], t["split"]))
    # ---- per template
    seen_id, seen_text, lens = set(), {}, collections.defaultdict(list)
    forbidden = re.compile("|".join(re.escape(x) for x in C.FORBIDDEN_IDS))
    for kind, t in items:
        txt, tid, style = t["text"], t["id"], t["style"]
        if tid in seen_id:
            bad.append("%s: duplicate id" % tid)
        seen_id.add(tid)
        n = MP.norm_text(txt)
        if n in seen_text:
            bad.append("%s: normalised text shared with %s (%r)" % (tid, seen_text[n], n[:50]))
        seen_text[n] = tid
        slots = set(re.findall(r"\{([a-z_]+)\}", txt))
        extra = slots - set(MSG.KIND_SLOTS[kind])
        ident_slots = slots - set(MSG.NUMERIC_SLOTS)
        if extra:
            bad.append("%s: slots %s are not slots of %s" % (tid, sorted(extra), kind))
        if style == "I" and "fn" not in slots:
            bad.append("%s: style I template misses {fn}" % tid)
        if style == "N" and ident_slots:
            bad.append("%s: style N template carries identifier slots %s" % (tid, sorted(ident_slots)))
        try:
            rendered = txt.format(**dummy_slots())
        except (KeyError, IndexError, ValueError) as e:
            bad.append("%s: does not render (%s)" % (tid, e))
            continue
        nt = len(rendered.split())
        lens[kind].append(nt)
        if "?" in txt:
            bad.append("%s: is a question" % tid)
        if not LEN_RANGE[0] <= nt <= LEN_RANGE[1]:
            bad.append("%s: %d rendered tokens (allowed %d-%d)" % (tid, nt, LEN_RANGE[0], LEN_RANGE[1]))
        if forbidden.search(txt):
            bad.append("%s: contains an internal id" % tid)
        m = matches(txt)
        if kind not in m:
            bad.append("%s: does not name its own kind %s (%r)" % (tid, kind, txt[:60]))
        foreign = sorted(m - {kind})
        if foreign:
            bad.append("%s: names other kind(s) %s (%r)" % (tid, foreign, txt[:60]))
        low = re.sub(r"\{[a-z_]+\}", " ", txt.lower())
        for rx in REQUIRED[kind]:
            if not re.search(rx, low):
                bad.append("%s: lacks the kind phrase %r (%r)" % (tid, rx, txt[:60]))
        for rx, ok_kinds in FORBIDDEN:
            if kind in ok_kinds:
                fm = re.search(rx, low)
                if fm:
                    bad.append("%s: word %r reads as another kind (%r)" % (tid, fm.group(0), txt[:60]))
    # ---- cross-kind similarity
    worst, over = (0.0, None), 0
    for (ka, ta), (kb, tb) in itertools.combinations(items, 2):
        if ka == kb or (ka in MSG.TRIV_IDS and kb in MSG.TRIV_IDS):          # two trivial kinds never meet in a row (a true message is never trivial)
            continue
        j = MP.jaccard(ta["text"], tb["text"])
        if j > worst[0]:
            worst = (j, (ta["id"], tb["id"]))
        if j >= MAX_JACCARD:
            over += 1
            bad.append("%s ~ %s: token Jaccard %.2f >= %.1f (%r | %r)" % (ta["id"], tb["id"], j, MAX_JACCARD, ta["text"][:45], tb["text"][:45]))
    rep["max_cross_kind_jaccard"] = {"value": round(worst[0], 3), "pair": worst[1], "pairs_at_or_above_0.5": over}
    # ---- length balance
    allm = sum(sum(v) for v in lens.values()) / float(max(1, sum(len(v) for v in lens.values())))
    rep["mean_tokens"] = {k: round(sum(v) / float(len(v)), 2) for k, v in lens.items()}
    rep["pool_mean_tokens"] = round(allm, 2)
    real_m = [x for k, v in lens.items() if k not in MSG.TRIV_IDS for x in v]
    allm = sum(real_m) / float(max(1, len(real_m)))                      # the trivial kinds cover the lengths of the realised kinds by design (Opus ruling Q8 R3): no balance rule for them
    rep["pool_mean_tokens"] = round(allm, 2)
    for k, v in rep["mean_tokens"].items():
        if k not in MSG.TRIV_IDS and abs(v - allm) > MEAN_LEN_TOL:
            bad.append("%s: mean length %.2f tokens is more than %.1f from the pool mean %.2f" % (k, v, MEAN_LEN_TOL, allm))
    rep["templates"] = len(items)
    return bad, rep


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=None)
    a = ap.parse_args(argv)
    doc = MP.load(a.pool)
    bad, rep = lint(doc)
    print("MSG pool lint: %d templates in %d kinds" % (rep["templates"], len(doc["kinds"])))
    for k, v in rep["counts"].items():
        print("  %-8s %s  mean tokens %s" % (k, "  ".join("%s %3d" % (h, n) for h, n in v.items()), rep["mean_tokens"].get(k)))
    print("  pool mean tokens %s; max cross-kind Jaccard %s (%s), pairs >= 0.5: %d" % (rep["pool_mean_tokens"], rep["max_cross_kind_jaccard"]["value"], rep["max_cross_kind_jaccard"]["pair"],
                                                                                  rep["max_cross_kind_jaccard"]["pairs_at_or_above_0.5"]))
    for b in bad[:200]:
        print("  FAIL", b)
    if len(bad) > 200:
        print("  ... %d more" % (len(bad) - 200))
    print("RESULT:", "PASS" if not bad else "FAIL (%d problems)" % len(bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
