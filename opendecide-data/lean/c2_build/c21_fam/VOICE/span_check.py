"""Decision-span survival checker (solver A): word-level edit-distance alignment of the spoken reference against the ASR
hypothesis, spans mapped through the alignment (G0-lite VOICE section 2; Opus ruling C1 on recoverable spans).

A variant is KEPT only if EVERY decision-bearing span survives. Outcomes per span: survived | altered | deleted (| recovered,
only when the context-recovery exception is switched on, which is OFF by default and never applies to AUTHORITY spans).
  - negation / polarity: the negation signature of the aligned hypothesis region equals the reference's (contractions expanded);
    NEVER recoverable. A negation word inserted anywhere in the hypothesis is also an alteration (global check).
  - number / quantity / date: the aligned region denotes the same canonical number (digits, cardinal, digit by digit, ordinal,
    decimal, version, year, ISO date). Extra digits next to it (a longer maximal number run) make it altered.
  - entity / name / path / flag / rule / statement: symmetric skeleton equality (symbol words and symbols, letter names and
    letters, digit words and digits folded the same way on both sides; fillers dropped). Case is ignored (the ASR output case is
    not reliable), so a flag that differs only by case cannot be told apart: such sources should be excluded upstream.
A span whose value was replaced by a DIFFERENT valid value is altered even if the true value appears elsewhere in the row.
No file is written; no model is called.
"""
import re
from collections import Counter

import numwords as NW
import wer as W
from vcommon import FILLERS, MULTI_SYMBOL_WORDS, NAME_TO_LETTER, WORD_TO_SYMBOL

NEG_WORDS = {"not", "no", "never", "none", "nothing", "nobody", "nowhere", "neither", "nor", "without"}
_NEG_EXPAND = {"cannot": ["can", "not"], "can't": ["can", "not"], "won't": ["will", "not"], "shan't": ["shall", "not"]}
POLARITY_WORDS = {"only", "except", "unless", "always", "allow", "deny", "block"}
_TOK = re.compile(r"\d{4}-\d{2}-\d{2}|\d+(?:[.,]\d+)*%?(?:st|nd|rd|th)?|[a-z]+(?:'[a-z]+)?|[/\\._~#:=*@+&|<>$^%-]")
_NUMISH = set(NW.ONES) | {t for t in NW.TENS if t} | {"hundred", "thousand", "million", "billion", "point", "and", "oh", "minus", "percent"}
MONTH_ABBR = {m[:3]: i + 1 for i, m in enumerate(NW.MONTHS)}
MONTH_ABBR["sept"] = 9


def hyp_tokens(text):
    """Checker tokenisation of a hypothesis (kept as the ASR wrote it, lower case)."""
    return W.tokenize_text(text.lower(), _TOK)


def fold_tok(t):
    """Equality class used by the aligner: letter names, symbol words and digit words fold to one character."""
    if t in NAME_TO_LETTER:
        return NAME_TO_LETTER[t]
    if t in WORD_TO_SYMBOL and t not in ("and", "point"):
        return WORD_TO_SYMBOL[t]
    if t in NW.DIGIT_STRICT:
        return NW.DIGIT_STRICT[t]
    return t


def pol_sig(tokens):
    """Polarity words (only / except / unless / always / allow / deny / block) of a token list, as a multiset. A polarity word that appears or
    disappears ANYWHERE in the hypothesis changes what an instruction permits, so the multiset must be equal (skeptic fix 18 Oct: only the
    spans' own words were checked, so a confusion-table substitution that turned a plain word into 'only' or 'except' passed)."""
    c = Counter()
    for t in tokens:
        if t in POLARITY_WORDS:
            c[t] += 1
    return c


def neg_sig(tokens):
    c = Counter()
    for t in tokens:
        for u in _NEG_EXPAND.get(t, [t]):
            if u.endswith("n't"):
                c["not"] += 1
            elif u in NEG_WORDS:
                c[u] += 1
    return c


def skeleton(tokens, drop_hyphens=False):
    out = []
    toks = [t for t in tokens if t not in FILLERS and t != "capital"]
    i = 0
    while i < len(toks):
        t = toks[i]
        hit = None
        for k in (2, 3):
            if tuple(toks[i:i + k]) in MULTI_SYMBOL_WORDS:
                hit = (MULTI_SYMBOL_WORDS[tuple(toks[i:i + k])], k)
                break
        if hit:
            out.append(hit[0])
            i += hit[1]
            continue
        if t == "double" and i + 1 < len(toks) and toks[i + 1] == "you":
            out.append("w")
            i += 2
            continue
        if t in NAME_TO_LETTER:
            out.append(NAME_TO_LETTER[t])
        elif t in WORD_TO_SYMBOL:
            out.append(WORD_TO_SYMBOL[t])
        elif t in NW.DIGIT_STRICT:
            out.append(NW.DIGIT_STRICT[t])
        else:
            out.append(t)
        i += 1
    s = "".join(out)
    if drop_hyphens:
        s = re.sub(r"(?<=[a-z0-9])-(?=[a-z0-9])", "", s)
    return s


def _canon_number(text):
    t = text.strip().lower().replace(",", "")
    t = re.sub(r"%$", "", t)
    m = re.match(r"^(-?\d+(?:\.\d+)?)(?:st|nd|rd|th)?$", t)
    return m.group(1) if m else None


def number_runs(tokens):
    """Maximal runs of number-ish tokens: [(start, end)] indices."""
    runs, i, n = [], 0, len(tokens)

    def isnum(t):
        return t in _NUMISH or bool(re.match(r"^\d", t))
    while i < n:
        if isnum(tokens[i]):
            j = i
            while j < n and isnum(tokens[j]):
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    return runs


def parse_run(tokens):
    toks = [t for t in tokens]
    neg = False
    if toks and toks[0] in ("minus", "-"):
        neg = True
        toks = toks[1:]
    while toks and toks[-1] in ("percent", "%"):
        toks = toks[:-1]
    toks = [t[:-1] if t.endswith("%") and len(t) > 1 else t for t in toks]
    cands = NW.parse_number_tokens(toks) if toks else set()
    return {("-" + c if neg else c) for c in cands}


def number_survives(canonical, ext_tokens):
    exp = _canon_number(canonical)
    if exp is None:
        exp = canonical.strip().lower()
    toks = [t for t in ext_tokens if t not in FILLERS]
    for a, b in number_runs(toks):
        run = toks[a:b]
        while run and run[0] == "and":                      # 'and' at the edges of a run is not part of the number
            run = run[1:]
        while run and run[-1] in ("and", "point"):
            run = run[:-1]
        if run and exp in parse_run(run):
            return True
    return False


def parse_date_tokens(tokens):
    """Hypothesis tokens -> set of ISO dates. Understands 'march 14th 2026', 'march fourteenth twenty twenty six', '14 march 2026', '2026-03-14'."""
    toks = [t for t in tokens if t not in FILLERS and t not in (",", "of", "the", "and")]
    toks = [t for t in toks if t in NW.MONTHS or t in MONTH_ABBR or re.match(r"^\d", t) or t in _NUMISH or t in NW.ORD_REV or t.endswith(("th", "st", "nd", "rd", "eth"))]
    out = set()
    for i, t in enumerate(toks):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", t):
            out.add(t)
    mi = [i for i, t in enumerate(toks) if t in NW.MONTHS or t in MONTH_ABBR]
    for i in mi:
        mo = NW.MONTHS.index(toks[i]) + 1 if toks[i] in NW.MONTHS else MONTH_ABBR[toks[i]]
        after = toks[i + 1:]
        before = toks[:i]
        for day_tokens, year_tokens in ((after[:1], after[1:]), (after[:2], after[2:]), (before[-1:], after), (after[:3], after[3:])):
            dd = parse_run(day_tokens) if day_tokens else set()
            yy = parse_run(year_tokens) if year_tokens else set()
            for d in dd:
                for y in yy:
                    if d.isdigit() and y.isdigit() and 1 <= int(d) <= 31 and 1000 <= int(y) <= 2999:
                        out.add("%04d-%02d-%02d" % (int(y), mo, int(d)))
    return out


def date_survives(canonical, ext_tokens):
    return canonical in parse_date_tokens(ext_tokens)


# ------------------------------------------------------------------------------------------------
# unit-level alignment (a unit = all spoken tokens of one source token) and regions
# ------------------------------------------------------------------------------------------------
def build_units(doc):
    """Spoken tokens grouped by source token. kind: word | num | code | disfl."""
    toks = doc["tokens"]
    segs = sorted(doc["segments"], key=lambda s: s["tok"][0])
    units = []
    for s in segs:
        if units and s["src"] is not None and units[-1]["src"] == s["src"]:
            units[-1]["tok"][1] = s["tok"][1]
            units[-1]["kinds"].add(s["kind"])
            continue
        units.append({"tok": [s["tok"][0], s["tok"][1]], "src": s["src"], "kinds": {s["kind"]}})
    for u in units:
        k = u["kinds"]
        u["kind"] = "disfl" if k == {"disfl"} else ("num" if k <= {"number"} else ("word" if k <= {"word"} else "code"))
    return units


def _expand_contractions(ts):
    out = []
    for t in ts:
        out += _NEG_EXPAND.get(t, [t[:-3], "not"] if t.endswith("n't") and len(t) > 3 else [t])
    return out


def unit_match(unit, ref_tokens, hyp_span, doc):
    h = [t for t in hyp_span]
    if unit["kind"] in ("word", "disfl"):
        r = ref_tokens
        return [fold_tok(x) for x in _expand_contractions(r)] == [fold_tok(x) for x in _expand_contractions(h)]
    if unit["kind"] == "num":
        src = doc["source_tokens"][unit["src"]] if unit["src"] is not None else ""
        if re.match(r"^\d{4}-\d{2}-\d{2}$", src):
            return src in parse_date_tokens(h)
        exp = _canon_number(src)
        if exp is None:
            return skeleton(h) == skeleton(ref_tokens)
        hh = [t for t in h if t not in FILLERS]
        return bool(hh) and exp in parse_run(hh)
    return skeleton(h) == skeleton(ref_tokens) or skeleton(h, True) == skeleton(ref_tokens, True)


_MULTI_PARTS = {"open", "close", "paren", "bracket", "brace", "less", "greater", "than", "question", "mark", "double", "you"}


def _simple_fold(t):
    if t == "capital" or t in FILLERS:
        return ""
    if t in NAME_TO_LETTER:
        return NAME_TO_LETTER[t]
    if t in WORD_TO_SYMBOL:
        return WORD_TO_SYMBOL[t]
    if t in NW.DIGIT_STRICT:
        return NW.DIGIT_STRICT[t]
    return t


def _candidate_ks(un, rt, hyp, j, doc, ref_skel):
    """Hypothesis span lengths worth scoring for this unit starting at hyp[j]."""
    m = len(hyp)
    nr = len(rt)
    if un["kind"] in ("word", "disfl"):
        return range(1, min(2, m - j) + 1)
    ks = {k for k in (1, nr - 1, nr, nr + 1) if 1 <= k <= m - j}
    if un["kind"] == "num":
        ks |= set(range(1, min(nr + 3, m - j) + 1))
        return sorted(ks)
    acc = ""
    target = ref_skel
    for k in range(1, min(len(target) * 3 + 6, m - j) + 1):
        t = hyp[j + k - 1]
        acc += _simple_fold(t)
        if acc == target or acc.replace("-", "") == target.replace("-", "") or t in _MULTI_PARTS:
            ks.add(k)
        if len(acc) > len(target) + 4 and t not in _MULTI_PARTS:
            break
    return sorted(ks)


def align_units(doc, hyp, lmax=14):
    """Semi-Markov alignment of units to hypothesis spans. Returns (units, assign, inserted); assign[u] = (j0, j1) or None."""
    units = build_units(doc)
    toks = doc["tokens"]
    n, m = len(units), len(hyp)
    INF = float("inf")
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    ref_skels = [skeleton(toks[u["tok"][0]:u["tok"][1]]) if u["kind"] == "code" else None for u in units]
    for u in range(n + 1):
        for j in range(m + 1):
            cur = D[u][j]
            if cur == INF:
                continue
            if j < m and cur + 1.0 < D[u][j + 1]:                      # insert hyp[j]
                D[u][j + 1] = cur + 1.0
                back[u][j + 1] = ("ins", u, j)
            if u < n:
                un = units[u]
                rt = toks[un["tok"][0]:un["tok"][1]]
                nr = len(rt)
                dcost = 0.0 if (un["kind"] == "disfl" and all(t in FILLERS for t in rt)) else 1.0
                if cur + dcost < D[u + 1][j]:                          # delete the unit (one reference word)
                    D[u + 1][j] = cur + dcost
                    back[u + 1][j] = ("del", u, j)
                for k in _candidate_ks(un, rt, hyp, j, doc, ref_skels[u]):
                    span = hyp[j:j + k]
                    eq = unit_match(un, rt, span, doc)
                    cost = 0.0 if eq else float(k) + 0.25
                    if cur + cost < D[u + 1][j + k]:
                        D[u + 1][j + k] = cur + cost
                        back[u + 1][j + k] = ("match" if eq else "sub", u, j)
    assign = [None] * n
    inserted = []
    u, j = n, m
    while u > 0 or j > 0:
        op, pu, pj = back[u][j]
        if op == "ins":
            inserted.append(pj)
        elif op in ("match", "sub"):
            assign[pu] = (pj, j)
        u, j = pu, pj
    return units, assign, sorted(inserted)


def regions_units(units, assign, inserted, u_lo, u_hi):
    """core: hyp indices assigned to units [u_lo,u_hi) plus insertions between them; before / after: adjacent insertions."""
    core = []
    for u in range(u_lo, u_hi):
        if assign[u]:
            core += list(range(assign[u][0], assign[u][1]))
    if not core:
        # deleted: neighbours decide where the (empty) span sits
        prev_end = max([assign[u][1] for u in range(u_lo) if assign[u]] or [0])
        next_start = min([assign[u][0] for u in range(u_hi, len(units)) if assign[u]] or [10 ** 9])
        ext = [j for j in inserted if prev_end <= j < next_start]
        return [], sorted(ext), [], []
    lo_j, hi_j = min(core), max(core)
    inside = [j for j in inserted if lo_j < j < hi_j]
    core = sorted(set(core) | set(inside))
    # adjacent insertions: contiguous run of inserted indices directly before lo_j / after hi_j
    before, after = [], []
    j = lo_j - 1
    ins = set(inserted)
    while j in ins:
        before.append(j)
        j -= 1
    j = hi_j + 1
    while j in ins:
        after.append(j)
        j += 1
    return core, sorted(set(core) | set(before) | set(after)), sorted(before), sorted(after)


def written_reference(doc):
    """The WRITTEN form of what the speaker said, in spoken order: source tokens (a dictated path stays one word) plus the
    disfluency words that were spoken. Words dropped as politeness are absent. This is the WER reference (solver B measures
    WER against the same string with its own edit distance)."""
    toks = doc["tokens"]
    out = []
    seen = set()
    for s in sorted(doc["segments"], key=lambda x: x["tok"][0]):
        if s["src"] is None:
            out.append(" ".join(toks[s["tok"][0]:s["tok"][1]]))
        elif s["src"] not in seen:
            seen.add(s["src"])
            out.append(doc["source_tokens"][s["src"]])
    return " ".join(out)


def wer_from_alignment(units, assign, inserted, doc, hyp):
    """Unit-level WER. Reference words = units (source tokens and spoken disfluency words, fillers excluded). A unit matched by a
    hypothesis span of any tokenisation costs 0; a substituted unit costs the length of its hypothesis span (at least 1);
    a deleted unit costs 1; each inserted hypothesis token costs 1."""
    toks = doc["tokens"]
    N = S = D = 0
    for ui, un in enumerate(units):
        rt = toks[un["tok"][0]:un["tok"][1]]
        if un["kind"] == "disfl" and all(t in FILLERS for t in rt):
            continue
        N += 1
        a = assign[ui]
        if a is None:
            D += 1
        else:
            span = hyp[a[0]:a[1]]
            if not unit_match(un, rt, span, doc):
                S += max(1, len(span))
    I = len(inserted)
    return ((S + D + I) / N if N else (0.0 if not I else 1.0)), S, D, I, N


def doc_wer(doc, hyp_text):
    hyp = [t for t in hyp_tokens(hyp_text) if t not in FILLERS]
    units, assign, inserted = align_units(doc, hyp)
    return wer_from_alignment(units, assign, inserted, doc, hyp)


def check_doc(doc, hyp_text, allow_recovery=False, recover_fn=None):
    """Returns {'kept', 'wer', 'spans': [...], 'reasons': [...], 'global_negation_ok'}."""
    ref = [t for t in doc["tokens"]]
    hyp = [t for t in hyp_tokens(hyp_text) if t not in FILLERS]
    units, assign, inserted = align_units(doc, hyp)
    tok_to_unit = {}
    for ui, u in enumerate(units):
        for t in range(u["tok"][0], u["tok"][1]):
            tok_to_unit[t] = ui
    res_spans, reasons = [], []
    for sp in doc["spans"]:
        lo, hi = sp["tok"]
        us = sorted({tok_to_unit[t] for t in range(lo, hi) if t in tok_to_unit})
        u_lo, u_hi = (us[0], us[-1] + 1) if us else (0, 0)
        core, ext, before, after = regions_units(units, assign, inserted, u_lo, u_hi)
        ext_toks = [hyp[j] for j in ext if hyp[j] not in FILLERS]
        variants = []
        for use_b in (False, True):
            for use_a in (False, True):
                idx = sorted(set(core) | (set(before) if use_b else set()) | (set(after) if use_a else set()))
                variants.append([hyp[j] for j in idx if hyp[j] not in FILLERS])
        ref_span = ref[lo:hi]
        role, kind = sp["role"], (sp.get("kind") or "")
        if not [hyp[j] for j in core if hyp[j] not in FILLERS] and not ext_toks:
            status = "deleted"
        else:
            status = "survived" if _survives(sp, role, kind, ref_span, ext_toks, variants) else "altered"
        if status != "survived" and allow_recovery and role not in ("negation", "authority") and kind not in ("negation", "polarity") and status == "deleted":
            if recover_fn is not None and recover_fn(sp):
                status = "recovered"
        res_spans.append({"id": sp["id"], "role": role, "kind": kind, "status": status, "hyp": " ".join(ext_toks)})
        if status not in ("survived", "recovered"):
            reasons.append("%s:%s:%s" % (role, kind, status))
    # a negation word that the reference does not have appears in the hypothesis (or one is missing)
    ref_neg, hyp_neg = neg_sig(ref), neg_sig(hyp)
    global_ok = all(hyp_neg[k] == ref_neg[k] for k in set(hyp_neg) | set(ref_neg))
    if not global_ok:
        reasons.append("negation:global:altered")
    ref_pol, hyp_pol = pol_sig(ref), pol_sig(hyp)
    pol_ok = all(hyp_pol[k] == ref_pol[k] for k in set(hyp_pol) | set(ref_pol))
    if not pol_ok:
        reasons.append("polarity:global:altered")
    global_ok = global_ok and pol_ok
    w = wer_from_alignment(units, assign, inserted, doc, hyp)
    return {"kept": not reasons, "wer": w[0], "spans": res_spans, "reasons": reasons, "global_negation_ok": global_ok, "n_ref": w[4]}


def _survives(sp, role, kind, ref_span, ext_toks, variants):
    if kind in ("negation",) or (role == "negation" and kind not in ("polarity",)):
        return neg_sig(ext_toks) == neg_sig(ref_span)
    if kind == "polarity":
        return sorted(t for t in ext_toks if t in POLARITY_WORDS) == sorted(t for t in ref_span if t in POLARITY_WORDS)
    if kind in ("number", "digits") or (role == "number" and kind in ("", None)):
        return number_survives(sp["canonical"], ext_toks)
    if kind == "date":
        return date_survives(sp["canonical"], ext_toks)
    if kind == "quantity":
        m = re.match(r"^\s*(-?[\d.,]+)\s*(.*)$", sp["canonical"])
        if not m:
            return skeleton(ext_toks) == skeleton(ref_span)
        num, unit = m.group(1), m.group(2).strip().lower()
        if not number_survives(num, ext_toks):
            return False
        u_ref = [t for t in ref_span if t not in _NUMISH]
        for v in variants:
            rest = [t for t in v if t not in _NUMISH and not re.match(r"^\d", t)]
            if _stem_eq(skeleton(rest), skeleton(u_ref)):
                return True
        return False
    if kind == "unit":
        return any(_stem_eq(skeleton(v), skeleton(ref_span)) for v in variants)
    return any(skeleton(v) == skeleton(ref_span) or skeleton(v, True) == skeleton(ref_span, True) for v in variants)


def _stem_eq(a, b):
    a = a[:-1] if a.endswith("s") and len(a) > 3 else a
    b = b[:-1] if b.endswith("s") and len(b) > 3 else b
    return a == b
