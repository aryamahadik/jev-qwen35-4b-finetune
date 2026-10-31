"""formats-2: build and check the spec 2.3 real-text codebooks (F10 S7, F11 S7) and the per-dataset field-value phrase
lexicon (F10 AR21).

Checks (the build fails on any): F10 flat conditions; totality by enumeration of the full annotation space (every vector
has exactly one first-fit code); residual and every non-residual code reachable as first fit by eligible records;
code counts (F10 5-9 or 20-30 with >= 19 non-residual; F11 MAMS 12-21, XED 12-30, EDOS 10-12); F11 full-set codes
with a one-step neighbour and >= 1 covered combination; distinct partitions per (family, dataset); XF12 (no F10 and
F11 codebook on the same dataset with the same partition); feasibility floors on eligible records.
Eligible = train, well-formed, not in golden_train, >= 3 words, duplicate-text rule kept, GHC/EDOS not in HateXplain or
SBF, no sealed-check hit. Counts are on 100% of train records (the orchestrator's 90/10 split and the claim ledger
are applied later by the builders). EDOS codebooks are written with status "blocked_X15": their counts are kept as
eligible_*_pre_x15 (before the 2-of-3 annotator filter), and no builder may use them until X15 is granted.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from collections import Counter, defaultdict

from common_f2 import HERE, progress, read_jsonl, write_json, write_jsonl
import codebooks_src as S
from lint_f2 import rouge_pairs

OUT = HERE / "codebooks"
SEED = 20261003
POLS = ["positive", "negative", "neutral"]
CATS = ["food", "service", "staff", "price", "ambience", "menu", "place", "miscellaneous"]
EMOS = S.EMOS
EDOS_VEC = ["1.1", "1.2", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2"]
FLOOR_SMALL, FLOOR_LARGE, FLOOR_F11 = 20, 8, 8

# ------------------------------------------------------------------ lexicon (AR21; paraphrases of the guidelines)
LEXICON = {
    "xed": {
        "dimension": "emotions the annotators tagged in a line of film dialogue (Plutchik's eight; or neutral)",
        "values": {"anger": "annoyance, irritation or rage", "anticipation": "interest in, or expectation of, what "
                   "comes", "disgust": "dislike, contempt or revulsion", "fear": "worry, apprehension or terror",
                   "joy": "happiness, pleasure or delight", "sadness": "sorrow, disappointment or grief",
                   "surprise": "astonishment, or being caught off guard", "trust": "acceptance, reliance or "
                   "admiration", "neutral": "the annotators tagged no emotion and marked the line neutral"},
        "templates": {
            "EMO+": ["the annotators tagged the line with {v}", "{v} is among the emotions the line received"],
            "EMO-": ["{v} appears nowhere in the line's emotion tags", "the annotators left {v} out of the tags they "
                     "gave this line"],
            "EMO+neutral": ["the annotators marked the line neutral", "the line's sole tag is the neutral one"],
            "EMO-neutral": ["at least one emotion was tagged on the line", "the line bears an emotion tag and so sits "
                            "outside the neutral group"]}},
    "mams_acsa": {
        "dimension": "aspect categories the annotators marked in a restaurant review sentence, each with a polarity",
        "values": {"food": "the food and drink", "service": "the service: speed, reservations and the handling of "
                   "orders", "staff": "the staff as people: servers, hosts, managers and cooks", "price": "prices and "
                   "value for money", "ambience": "the atmosphere: decor, music, noise and lighting", "menu": "the "
                   "menu: choice, variety and specials", "place": "the location and the premises",
                   "miscellaneous": "an aspect outside the seven named categories",
                   "positive": "favourable", "negative": "unfavourable", "neutral": "neither favourable nor "
                   "unfavourable"},
        "templates": {
            "PAIR+": ["the annotators marked a {p} opinion about {c}", "{c} was judged {p} in this sentence"],
            "PAIR-": ["there is no {p} annotation for {c}, including when the sentence says nothing about {c}",
                      "a {p} verdict on {c} is absent from the annotations (a sentence that leaves {c} out also "
                      "qualifies)"],
            "CAT+": ["{c} is one of the annotated aspects, whatever its polarity", "the annotators picked out {c} as "
                     "a topic of the sentence"],
            "CAT-": ["the annotators did not pick out {c} as an aspect", "{c} goes unannotated in this sentence"],
            "POL+": ["at least one annotated aspect carries {p} sentiment", "some aspect of the sentence was "
                     "rated {p}"],
            "POL-": ["every annotated aspect is rated something other than {p}", "{p} ratings are absent from every aspect of the "
                     "sentence"]}},
    "mams_atsa": {
        "dimension": "polarity the annotators gave the asked target and the other targets listed with the sentence",
        "values": {"positive": "favourable", "negative": "unfavourable", "neutral": "neither favourable nor "
                   "unfavourable"},
        "templates": {
            "TPOL+": ["the annotators marked the asked target {p}", "{p} is the polarity recorded for the asked "
                      "target"],
            "TPOL-": ["the asked target carries a polarity other than {p}", "the annotators gave the asked target a "
                      "rating different from {p}"],
            "OTHER+": ["at least one other listed target is annotated {p}", "among the remaining listed targets, "
                       "one or more were rated {p}"],
            "OTHER-": ["no other listed target is annotated {p}, including when no other target is listed",
                       "{p} ratings are absent from the remaining listed targets (this also holds when no other "
                       "target is listed)"]}},
    "ghc": {
        "dimension": "hate-speech features the annotators marked in a social media post (majority labels)",
        "values": {"hd": "human degradation: the post attacks the dignity of people because of a group identity "
                   "such as race, religion, gender or sexual orientation", "cv": "call for violence: the post calls "
                   "for, or endorses, violent action against people because of a group identity",
                   "vo": "vulgarity or offensive language: the post uses obscene, vulgar or offensive language"},
        "names": {"hd": "human degradation", "cv": "call for violence", "vo": "vulgarity or offensive language"},
        "templates": {
            "FLAG+": ["the annotators marked the post as {f}", "{f} is among the features the annotators found in "
                      "the post"],
            "FLAG-": ["{f} was left unmarked by the annotators", "the annotators found no {f} in this post"]}},
    "edos": {
        "dimension": "sexism label the annotators assigned to an online post (sexist or not; category; fine vector)",
        "values": {"1": "threats, plans to harm and incitement", "2": "derogation", "3": "animosity",
                   "4": "prejudiced discussions", "1.1": "threats of harm", "1.2": "incitement and encouragement of "
                   "harm", "2.1": "descriptive attacks", "2.2": "aggressive and emotive attacks", "2.3": "dehumanising "
                   "attacks and overt sexual objectification", "3.1": "casual use of gendered slurs, profanities and "
                   "insults", "3.2": "immutable gender differences and gender stereotypes", "3.3": "backhanded "
                   "gendered compliments", "3.4": "condescending explanations or unwelcome advice", "4.1": "supporting "
                   "mistreatment of individual women", "4.2": "supporting systemic discrimination against women as a "
                   "group"},
        "templates": {
            "SEXIST+": ["the annotators judged the post sexist", "the post was labelled as sexism by its annotators"],
            "SEXIST-": ["the post's annotators found it free of sexism", "the post sits in the annotators' "
                        "not-sexist group"],
            "CAT+": ["the annotators classed the post as sexism of the '{c}' kind", "'{c}' is the sexism category "
                     "this post received"],
            "CAT-": ["'{c}' is a category this post did not receive, including posts judged not sexist",
                     "the post falls outside the '{c}' category, either under another category or as a not-sexist "
                     "post"],
            "VEC+": ["the annotators gave the post the fine label '{v}'", "'{v}' is the detailed sexism label "
                     "attached to this post"],
            "VEC-": ["the fine label '{v}' was withheld from this post (posts judged not sexist count here too)",
                     "whatever detailed label the post has, it differs from '{v}'; a not-sexist post also "
                     "qualifies"]}},
}
CONNECTIVES = {"ALL": "F10 G0 section 5 registry: 'all of the following' (one list level)",
               "ANY": "F10 G0 section 5 registry: 'any of the following' (one list level)",
               "NOT": "only on one atom, through the NOT templates above (R3-05: complement, absence counts)"}


# ------------------------------------------------------------------ annotation spaces and atoms
def space(scheme):
    if scheme == "xed":
        out = [("neutral",)]
        for k in range(1, 9):
            out += [tuple(c) for c in itertools.combinations(EMOS, k)]
        return out
    if scheme == "mams_acsa":
        out = []
        for combo in itertools.product([None] + POLS, repeat=len(CATS)):
            out.append(tuple(sorted((c, p) for c, p in zip(CATS, combo) if p)))
        return out
    if scheme in ("mams_atsa", "named"):
        return [(tp, tuple(s)) for tp in POLS for k in range(0, 4) for s in itertools.combinations(sorted(POLS), k)]
    if scheme == "ghc":
        return list(itertools.product([0, 1], repeat=3))
    if scheme == "edos":
        return ["none"] + EDOS_VEC
    raise KeyError(scheme)


def atom_true(scheme, atom, v):
    k = atom[0]
    if scheme == "xed":
        return atom[1] in v
    if scheme == "mams_acsa":
        if k == "PAIR":
            return (atom[1], atom[2]) in v
        if k == "CAT":
            return any(c == atom[1] for c, _ in v)
        if k == "POL":
            return any(p == atom[1] for _, p in v)
    if scheme == "mams_atsa":
        if k == "TPOL":
            return v[0] == atom[1]
        if k == "OTHER":
            return atom[1] in v[1]
    if scheme == "ghc":
        return v[["hd", "cv", "vo"].index(atom[1])] == 1
    if scheme == "edos":
        if k == "SEXIST":
            return v != "none"
        if k == "CAT":
            return v != "none" and v.split(".")[0] == atom[1]
        if k == "VEC":
            return v == atom[1]
    raise KeyError((scheme, atom))


def cond_true(scheme, c, v):
    op = c["op"]
    if op == "LIT":
        t = atom_true(scheme, c["atom"], v)
        return (not t) if c["neg"] else t
    if op == "ALL":
        return all(cond_true(scheme, a, v) for a in c["args"])
    if op == "ANY":
        return any(cond_true(scheme, a, v) for a in c["args"])
    raise KeyError(op)


def flat_ok(c):
    if c["op"] == "LIT":
        return True
    return c["op"] in ("ALL", "ANY") and len(c["args"]) >= 2 and all(a["op"] == "LIT" for a in c["args"])


# ------------------------------------------------------------------ eligible units per scheme
def eligible(r, dupkey):
    f = r["flags"]
    if f["malformed"] or f["in_golden_train"] or f["short_lt3_words"] or f.get("in_hatexplain_or_sbf") \
            or f.get("sealed_hit"):
        return False
    d = f.get(dupkey)
    return bool(d and d["keep"])


def units(scheme, fam, recs):
    """Returns list of (unit_key, record_id, vector) for codebook feasibility."""
    out = []
    if scheme == "xed":
        for r in recs:
            if fam == "F10" and eligible(r, "dup_union"):
                out.append((r["id"], r["id"], tuple(r["ann"]["emotions"])))
            elif fam == "F11" and r.get("xed_file") == "annotated" and eligible(r, "dup_annotated_only"):
                out.append((r["id"], r["id"], tuple(r["ann"]["emotions"])))
    elif scheme == "mams_acsa":
        for r in recs:
            if not eligible(r, "dup"):
                continue
            asp = [tuple(x) for x in r["ann"]["aspects"]]
            if fam == "F10":
                out.append((r["id"], r["id"], tuple(sorted(asp))))
            else:
                for i, (c, p) in enumerate(asp):
                    others = tuple(sorted({pp for j, (cc, pp) in enumerate(asp) if j != i}))
                    out.append((f"{r['id']}#{c}", r["id"], (p, others)))
    elif scheme == "mams_atsa":
        for r in recs:
            if not eligible(r, "dup") or not r["ann"]["terms_unique"]:
                continue
            t = r["ann"]["terms"]
            for i, x in enumerate(t):
                ok = (x["n_sub"] == 1) if fam == "F10" else (x["n_word"] == 1)
                if not ok or not x["span_ok"]:
                    continue
                others = tuple(sorted({y["polarity"] for j, y in enumerate(t) if j != i}))
                out.append((f"{r['id']}#{i}", r["id"], (x["polarity"], others)))
    elif scheme == "ghc":
        out = [(r["id"], r["id"], (r["ann"]["hd"], r["ann"]["cv"], r["ann"]["vo"])) for r in recs if eligible(r, "dup")]
    elif scheme == "edos":
        out = [(r["id"], r["id"], (r["ann"]["label_vector"].split(" ")[0] if r["ann"]["label_vector"] != "none"
                                   else "none")) for r in recs if eligible(r, "dup")]
    return out


def render_literal(scheme, c):
    """First-paraphrase rendering, used only to estimate definition length (the builder renders the real card)."""
    lex = LEXICON[scheme]
    atom, neg = c["atom"], c["neg"]
    k = atom[0]
    if scheme == "xed":
        form = ("EMO-" if neg else "EMO+") + ("neutral" if atom[1] == "neutral" else "")
        return lex["templates"][form][0].format(v=atom[1])
    form = k + ("-" if neg else "+")
    t = lex["templates"][form][0]
    v1 = atom[1] if len(atom) > 1 else ""
    if scheme == "mams_acsa":
        return t.format(c=v1, p=atom[2]) if k == "PAIR" else t.format(c=v1, p=v1)
    if scheme == "mams_atsa":
        return t.format(p=v1)
    if scheme == "ghc":
        return t.format(f=lex["names"][v1])
    return t.format(c=lex["values"].get(v1, ""), v=lex["values"].get(v1, ""))


def est_tokens(scheme, codes, rname):
    words = 0
    for nm, c in codes:
        if c["op"] == "LIT":
            txt = render_literal(scheme, c)
        else:
            txt = ("all of the following: " if c["op"] == "ALL" else "any of the following: ") + \
                "; ".join(render_literal(scheme, a) for a in c["args"])
        words += len((nm + ": " + txt).split())
    words += len((rname + ": none of the other codes on this card fits.").split())
    return int(words * 1.35)


def partition_sig(blocks):
    canon = sorted(sorted(json.dumps(v) for v in b) for b in blocks if b)
    return hashlib.sha256(json.dumps(canon).encode()).hexdigest()


# ------------------------------------------------------------------ F10
def acsa_large(us):
    freq = Counter(p for _, _, v in us for p in v)
    order = sorted(freq, key=lambda p: (freq[p], p))          # rarest first
    best = None
    for k in range(2, 10):
        excl = set(order[-k:])
        codes = order[:-k]
        resid = sum(1 for _, _, v in us if set(v) <= excl)
        firsts = Counter()
        for _, _, v in us:
            for i, pc in enumerate(codes):
                if pc in v:
                    firsts[i] += 1
                    break
        if resid >= 30 and all(firsts[i] >= FLOOR_LARGE for i in range(len(codes))) and 19 <= len(codes) <= 29:
            best = codes
            break
    if best is None:
        raise SystemExit("acsa_l1: no feasible exclusion set")
    word = {"positive": "praise", "negative": "complaint", "neutral": "mention"}
    cname = {"miscellaneous": "Extras", "ambience": "Atmosphere", "place": "Venue"}
    codes = [(f"{cname.get(c, c.capitalize())} {word[p]}", S.L("PAIR", c, p)) for c, p in best]
    return ("acsa_l1", "mams_acsa", "opinions annotators marked per aspect category in a restaurant review sentence",
            codes, "Common pairing")


def build_f10(recs_by_scheme):
    out, probs = [], []
    defs = list(S.F10)
    acsa_units = units("mams_acsa", "F10", recs_by_scheme["mams_acsa"])
    defs.insert([d[0] for d in defs].index("acsa_s3") + 1, acsa_large(acsa_units))
    for key, scheme, dim, codes, rname in defs:
        sp = space(scheme)
        us = units(scheme, "F10", recs_by_scheme[scheme])
        n = len(codes) + 1
        large = n >= 20
        if not (5 <= n <= 9 or (20 <= n <= 30 and len(codes) >= 19)):
            probs.append(f"{key}: {n} codes")
        for nm, c in codes:
            if not flat_ok(c):
                probs.append(f"{key}/{nm}: nested condition")

        def ff(v):
            for i, (_, c) in enumerate(codes):
                if cond_true(scheme, c, v):
                    return i
            return len(codes)
        vmap = {v: ff(v) for v in sp}
        blocks = defaultdict(set)
        for v, i in vmap.items():
            blocks[i].add(v)
        cnt = Counter(ff(v) for _, _, v in us)
        recs_cnt = defaultdict(set)
        for _, rid, v in us:
            recs_cnt[ff(v)].add(rid)
        floor = FLOOR_LARGE if large else FLOOR_SMALL
        for i in range(n):
            if not blocks.get(i):
                probs.append(f"{key}: code {i + 1} unreachable in the annotation space")
            elif cnt[i] < floor:
                probs.append(f"{key}: code {i + 1} has {cnt[i]} eligible units (< {floor})")
        names = [nm for nm, _ in codes] + [rname]
        if len({x.casefold() for x in names}) != len(names):
            probs.append(f"{key}: duplicate names")
        cb = {"id": f"cb.F10.{key}", "family": "F10", "dataset": {"xed": "xed_en", "mams_acsa": "mams",
              "mams_atsa": "mams", "ghc": "ghc", "edos": "edos"}[scheme], "scheme": scheme, "dimension": dim,
              "semantics": "first fit in card order; residual last = none of the other codes on this card fits "
                           "(F10 ST44, ST45)",
              "n_codes": n, "size_class": "20-30" if large else "5-9",
              "codes": [{"code_id": f"K{i + 1}", "position": i + 1, "natural_name": nm, "condition": c,
                         "residual": False, "eligible_units": cnt[i], "eligible_records": len(recs_cnt[i]),
                         "vectors": len(blocks.get(i, ()))} for i, (nm, c) in enumerate(codes)] +
                       [{"code_id": f"K{n}", "position": n, "natural_name": rname, "condition": {"op": "RESIDUAL"},
                         "residual": True, "eligible_units": cnt[n - 1], "eligible_records": len(recs_cnt[n - 1]),
                         "vectors": len(blocks.get(n - 1, ()))}],
              "space_vectors": len(sp), "totality": "checked by enumeration: every vector has exactly one first-fit "
                                                     "code", "partition_sha256": partition_sig(blocks.values()),
              "lexicon": f"lex.{scheme}", "eligible_units_total": len(us),
              "est_definition_tokens": est_tokens(scheme, codes, rname),
              "unit": {"mams_atsa": "(record, asked target) with unique term strings and the target string once in "
                                    "the sentence (case-insensitive substring)"}.get(scheme, "record")}
        if cb["est_definition_tokens"] > 1600:
            probs.append(f"{key}: definitions about {cb['est_definition_tokens']} tokens (> 1,600)")
        cb["_blocks"] = blocks
        out.append(cb)
    return out, probs


# ------------------------------------------------------------------ F11
def xed_name(s):
    return " / ".join(x.capitalize() for x in s)


def build_f11(recs_by_scheme):
    out, probs = [], []
    rng = random.Random(SEED)
    # XED
    us = units("xed", "F11", recs_by_scheme["xed"])
    sp_x = [v for v in space("xed") if v != ("neutral",)]
    for key, npairs, ntrip, merges in S.F11_XED:
        sets = [(e,) for e in EMOS] + [tuple(sorted(p)) for p in S.P_TOP[:npairs]] + \
               [tuple(sorted(t)) for t in S.T_TOP[:ntrip]]
        codes = []
        merged = set()
        for single, pair in merges:
            codes.append([(single,), tuple(sorted(pair))])
            merged |= {(single,), tuple(sorted(pair))}
        for s in sets:
            if s not in merged:
                codes.append([s])
        out.append(_f11_obj("xed", "xed_en", key, codes, us, sp_x, rng, probs, (12, 30),
                            "emotions the annotators tagged in a line of film dialogue", xed_name))
    # MAMS
    for scheme, pats in S.F11_MAMS.items():
        us = units(scheme, "F11", recs_by_scheme[scheme])
        sp_m = [v for v in space("named") if v[1] and v[1] != (v[0],)]
        for key, pat in pats:
            codes = []
            for p, pp in zip(POLS, pat):
                q1, q2 = [q for q in POLS if q != p]
                S1, S2, S12 = (q1,), (q2,), tuple(sorted((q1, q2)))
                Sp1, Sp2, Sall = tuple(sorted((q1, p))), tuple(sorted((q2, p))), tuple(sorted(POLS))
                blocks = {"a": [[S1], [S2], [S12], [Sp1], [Sp2], [Sall]],
                          "b": [[S1], [S2], [S12, Sall], [Sp1], [Sp2]],
                          "d1": [[S1], [S2], [S12], [Sp1, Sall], [Sp2]],
                          "d2": [[S1], [S2], [S12], [Sp1], [Sp2, Sall]],
                          "c2": [[S1, Sp1], [S2], [S12], [Sp2], [Sall]],
                          "c3": [[S1, Sp1], [S2], [S12, Sall], [Sp2]]}[pp]
                for b in blocks:
                    codes.append([(p, s) for s in b])
            unit = "the named aspect category" if scheme == "mams_acsa" else "the named target"
            out.append(_f11_obj(scheme, "mams", key, codes, us, sp_m, rng, probs, (12, 21),
                                f"polarity of {unit} and the set of polarities of the other "
                                f"{'categories' if scheme == 'mams_acsa' else 'targets'}",
                                lambda v: f"named {v[0]} with others {' and '.join(v[1])}"))
    # EDOS
    us = units("edos", "F11", recs_by_scheme["edos"])
    sp_e = space("edos")
    for key, merges in S.F11_EDOS:
        merged = {x for m in merges for x in m}
        codes = [[v] for v in sp_e if v not in merged] + [list(m) for m in merges]
        codes.sort(key=lambda c: sp_e.index(c[0]))
        out.append(_f11_obj("edos", "edos", key, codes, us, sp_e, rng, probs, (10, 12),
                            "sexism label the annotators assigned to an online post",
                            lambda v: "not sexist" if v == "none" else
                            f"{v} {LEXICON['edos']['values'][v]}"))
    return out, probs


def _neighbours(scheme, v):
    """One-step neighbours (F11 R26)."""
    out = set()
    if scheme == "xed":
        s = set(v)
        for e in EMOS:
            t = s ^ {e}
            if t:
                out.add(tuple(sorted(t)))
    elif scheme in ("mams_acsa", "mams_atsa"):
        tp, S_ = v
        for q in POLS:
            if q != tp:
                out.add((q, S_))
            t = set(S_) ^ {q}
            if t:
                out.add((tp, tuple(sorted(t))))
    elif scheme == "edos":
        if v == "none":
            out |= set(EDOS_VEC)
        else:
            out.add("none")
            out |= {w for w in EDOS_VEC if w != v and w.split(".")[0] == v.split(".")[0]}
    return out


def _f11_obj(scheme, dataset, key, codes, us, sp, rng, probs, size, dim, namefn):
    n = len(codes)
    if not size[0] <= n <= size[1]:
        probs.append(f"F11 {key}: {n} codes outside {size}")
    covered = {}
    for i, c in enumerate(codes):
        for v in c:
            if v in covered:
                probs.append(f"F11 {key}: vector {v} in two codes")
            covered[v] = i
    cnt = Counter(covered[v] for _, _, v in us if v in covered)
    recs = defaultdict(set)
    for _, rid, v in us:
        if v in covered:
            recs[covered[v]].add(rid)
    for i in range(n):
        if cnt[i] < FLOOR_F11:
            probs.append(f"F11 {key}: code {i + 1} has {cnt[i]} eligible units (< {FLOOR_F11})")
        nb = {covered[w] for v in codes[i] for w in _neighbours(scheme, v) if w in covered} - {i}
        if not nb:
            probs.append(f"F11 {key}: code {i + 1} has no one-step neighbour code")
    marks = [False] * n
    k = max(1, round(n * rng.uniform(0.4, 0.6)))
    for i in rng.sample(range(n), k):
        marks[i] = True
    cov_units = sum(cnt.values())
    obj = {"id": f"cb.F11.{scheme}.{key}", "family": "F11", "dataset": dataset, "scheme": scheme,
           "dimension": dim, "semantics": "each code lists FULL annotation combinations (SEM-46); a record whose "
           "combination is in no code is outside coverage and is not used", "n_codes": n,
           "codes": [{"code_id": f"C{i + 1:02d}", "position": i + 1,
                      "full_sets": [list(v) if isinstance(v, tuple) and scheme == "xed" else
                                    ([v[0], list(v[1])] if isinstance(v, tuple) else v) for v in c],
                      "labelset_name": namefn(c[0]) if len(c) == 1 else None, "action_mark": marks[i],
                      "eligible_units": cnt[i], "eligible_records": len(recs[i])} for i, c in enumerate(codes)],
           "coverage": {"combinations": len(covered), "space": len(sp), "eligible_units_covered": cov_units,
                        "eligible_units_total": len(us)},
           "action_marks": f"{sum(marks)} of {n} codes (SEM-52; never changes which code applies)",
           "invented_names": "assigned by the F11 builder (full S7 cards use invented names)",
           "lexicon": f"lex.{'mams_atsa' if scheme.startswith('mams') else scheme}",
           "partition_sha256": partition_sig([set(c) for c in codes])}
    obj["_blocks"] = {i: set(c) for i, c in enumerate(codes)}
    return obj


# ------------------------------------------------------------------ cross checks and lexicon
def lexicon_doc():
    lex = []
    for scheme, d in LEXICON.items():
        tid = 0
        temps = []
        for k, lst in d["templates"].items():
            for t in lst:
                tid += 1
                temps.append({"id": f"lex.{scheme}.t{tid:02d}", "form": k, "template": t})
        vals = [{"id": f"lex.{scheme}.v.{k}", "value": k, "gloss": v} for k, v in d["values"].items()]
        lex.append({"id": f"lex.{scheme}", "scheme": scheme, "dimension": d["dimension"], "templates": temps,
                    "values": vals, "names": d.get("names"), "connectives": CONNECTIVES,
                    "not_semantics": "NOT = Boolean complement of one atom; a value the record does not carry counts "
                                     "as absent (F10 R3-05). NOT templates that presuppose presence state the absence "
                                     "case inside the phrase."})
    return lex


def not_probes():
    """F10 lexicon QC (program part): every NOT form with an absence case holds on both probe vectors."""
    res = []
    probes = [("mams_acsa", S.N("PAIR", "food", "negative"), (("staff", "positive"), ("service", "neutral"))),
              ("mams_acsa", S.N("PAIR", "food", "negative"), (("food", "positive"), ("staff", "negative"))),
              ("mams_atsa", S.N("OTHER", "negative"), ("positive", ())),
              ("mams_atsa", S.N("OTHER", "negative"), ("positive", ("neutral",))),
              ("edos", S.N("CAT", "2"), "none"), ("edos", S.N("CAT", "2"), "3.1"),
              ("edos", S.N("VEC", "2.1"), "none"), ("edos", S.N("VEC", "2.1"), "2.2")]
    for scheme, c, v in probes:
        res.append({"scheme": scheme, "literal": c, "probe": v, "holds": cond_true(scheme, c, v)})
    return res


# ------------------------------------------------------------------ X15 block (EDOS)
X15_RULE = ("F10 G0 3 S7 / R3-C2 / XF07 and F11 G0 K24 / X15: no EDOS S7 row or example (F10) and no EDOS S7 or "
            "S5-arm row (F11) until the orchestrator adds the EDOS per-annotator file to LICENCE_REGISTER.md row 17 "
            "with the train-ids-first filter and the shared 2-of-3 annotator filter is applied; never the aggregate "
            "without the filter (no fallback). If X15 is declined, EDOS leaves S7 and these codebooks are dropped "
            "(F10: the orchestrator re-splits EDOS's S7 rows over XED, MAMS and GHC; F11: S7 = MAMS 50 / XED 50)")


def block_x15(cb):
    """EDOS codebooks stay in the file but are marked unusable until X15; their counts are kept as *_pre_x15."""
    cb["status"] = "blocked_X15"
    cb["blocked_on"] = {"issue": "X15", "rule": X15_RULE,
                        "counts": "eligible_*_pre_x15 = counts on the released aggregate before the 2-of-3 filter; "
                                  "the feasibility floors must be re-checked once the filter is applied"}
    for c in cb["codes"]:
        c["eligible_units_pre_x15"] = c["eligible_units"]
        c["eligible_records_pre_x15"] = c["eligible_records"]
        c["eligible_units"] = None
        c["eligible_records"] = None
    if "eligible_units_total" in cb:
        cb["eligible_units_total_pre_x15"] = cb["eligible_units_total"]
        cb["eligible_units_total"] = None
    if "coverage" in cb:
        for k in ("eligible_units_covered", "eligible_units_total"):
            cb["coverage"][k + "_pre_x15"] = cb["coverage"][k]
            cb["coverage"][k] = None


def _units(c):
    return c["eligible_units"] if c["eligible_units"] is not None else c["eligible_units_pre_x15"]


def main():
    recs = {s: read_jsonl(HERE / "records" / f"{s}.jsonl") for s in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos")}
    f10, p10 = build_f10(recs)
    f11, p11 = build_f11(recs)
    probs = p10 + p11
    # distinct partitions per (family, scheme)
    for fam_list in (f10, f11):
        seen = {}
        for cb in fam_list:
            k = (cb["family"], cb["scheme"], cb["partition_sha256"])
            if k in seen:
                probs.append(f"same partition: {seen[k]} and {cb['id']}")
            seen[k] = cb["id"]
    # XF12: F10 vs F11 on the same dataset and annotation space (exact; and F10 restricted to F11's coverage)
    xf12 = []
    for a in f10:
        for b in f11:
            if a["dataset"] != b["dataset"]:
                continue
            same_space = (a["scheme"] == b["scheme"]) and a["scheme"] in ("xed", "mams_atsa", "edos")
            exact = a["partition_sha256"] == b["partition_sha256"]
            restricted = None
            if same_space:
                cov = set().union(*b["_blocks"].values())
                ra = [blk & cov for blk in a["_blocks"].values()]
                restricted = partition_sig(ra) == b["partition_sha256"]
            if exact:
                probs.append(f"XF12 exact: {a['id']} {b['id']}")
            if restricted:
                xf12.append([a["id"], b["id"]])
    # option-line separators (G15 smoke, review formats-2 #3): no code name may hold a separator of the served option
    # layouts ("; " joins options; "|" and line breaks also delimit), and joining a codebook's names with "; " must
    # split back to the same names
    sep = []
    for cb in f10 + f11:
        names = [c.get("natural_name") or c.get("labelset_name") for c in cb["codes"]]
        names = [n for n in names if n]
        for n in names:
            if any(x in n for x in (";", "|", "\n", "\t")):
                sep.append(f"{cb['id']}: name with a separator: {n!r}")
        if "; ".join(names).split("; ") != names:
            sep.append(f"{cb['id']}: '; ' join does not round-trip")
    probs += sep
    probe = not_probes()
    if not all(p["holds"] for p in probe):
        probs.append("NOT probe failed")
    lex = lexicon_doc()
    tpl = [(t["id"], t["template"]) for d in lex for t in d["templates"]]
    rp = rouge_pairs(tpl)
    probs += [f"lexicon template rouge-l {x}" for x in rp]
    if probs:
        for p in probs:
            print("PROBLEM", p)
        raise SystemExit(f"{len(probs)} codebook problems")
    for cb in f10 + f11:
        cb.pop("_blocks", None)
        for c in cb["codes"]:
            c["id"] = f"{cb['id']}.{c['code_id']}"
        if cb["dataset"] == "edos":
            block_x15(cb)
        else:
            cb["status"] = "ready"
    sha_cb = write_jsonl(OUT / "codebooks.jsonl", f10 + f11)
    sha_lex = write_json(OUT / "lexicon.json", {"id": "lexicon.v1", "lexicons": lex,
                                                 "qc_not_probes": probe,
                                                 "template_rouge_pairs_ge_0.7": rp})
    summ = {"codebooks_sha256": sha_cb, "lexicon_sha256": sha_lex,
            "F10": dict(Counter(cb["dataset"] + ("/" + cb["scheme"] if cb["dataset"] == "mams" else "")
                                for cb in f10)),
            "F11": dict(Counter(cb["dataset"] + ("/" + cb["scheme"] if cb["dataset"] == "mams" else "")
                                for cb in f11)),
            "F10_size_classes": dict(Counter(cb["size_class"] for cb in f10)),
            "F10_min_units_nonresidual": {cb["id"]: min(_units(c) for c in cb["codes"] if not c["residual"])
                                          for cb in f10},
            "F11_min_units": {cb["id"]: min(_units(c) for c in cb["codes"]) for cb in f11},
            "min_units_note": "EDOS values are eligible_units_pre_x15 (released aggregate, before the 2-of-3 filter)",
            "status": dict(Counter(cb["status"] for cb in f10 + f11)),
            "blocked_X15": {"F10": [cb["id"] for cb in f10 if cb["status"] == "blocked_X15"],
                            "F11": [cb["id"] for cb in f11 if cb["status"] == "blocked_X15"]},
            "separator_check": f"{len(f10) + len(f11)} codebooks: 0 names with ';', '|', tab or line break; '; ' "
                               "join round-trips on every codebook",
            "F11_codes": {cb["id"]: cb["n_codes"] for cb in f11},
            "xf12_exact_same_partition": 0, "xf12_same_partition_on_f11_coverage": xf12,
            "lexicon_template_rouge_pairs": rp}
    write_json(HERE / "tmp" / "codebooks_build.json", summ)
    progress(f"build_codebooks: F10 {len(f10)} ({json.dumps(summ['F10'])}), F11 {len(f11)} "
             f"({json.dumps(summ['F11'])}); XF12 exact 0, on-coverage {len(xf12)}")
    print(json.dumps({k: summ[k] for k in ("F10", "F11", "F10_size_classes")}))


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    main()
