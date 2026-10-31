#!/usr/bin/env python3
"""public-3 row builder: C_DATA_SPEC v4 3.2 #13-17 (block 3E) -> tmp/cand_<ds>.json {main, reserve, dev}.

Labels are the released human annotations mapped by program only (no model, no Claude reading). Every record is used in
at most one group (one unit: a single row, or a question-flip twin pair on the same text), and every normalized (loose)
text at most once across all public-3 rows. main + reserve come from the train part of the shared 3E split, dev
(mix-tuning dev) from the 10% part.

Framings (>= 2 per dataset, >= 3 wordings each):
  xed       yn  question-flip pairs on single-label lines: asked label (yes) / a non-adjacent Plutchik emotion (no)
            ch4 single-label lines, gold + 3 other emotions;  ch9 all eight emotions + neutral (neutral-file lines too)
  mams      acsayn / atsayn  matched quads (v2.0): 2 sentences x 2 aspects, each aspect question yes on one sentence
                             and no on the other, each sentence asked both aspects
            acsach / atsach  matched triplets (v2.0): one aspect, 3 sentences with gold positive / negative / neutral
  sarcasm   yn  matched (sarcastic, not) pairs (v2.0);  ch  2-3 headlines, exactly one sarcastic (or one sincere),
            matched sets of k rows (v2.0): each length rank and each position is gold once per set
  edos      yn  matched (sexist, not) pairs (v2.0);  ch5 / ch4  matched class sets (v2.0): one post per option
  ghc       dropped in v2.0 (spec 8 G5 dataset-level rule; see DROPPED)

v2.0 (repair r1, PREREG A29 a): G6 fix at the builder. A matched set shows one partial input (wording, card, guidance,
options and their order, defs style, format style, G6 length bucket) once with every gold, so no partial-input or
metadata baseline can beat chance on it. Labels stay the released human annotations mapped by program.

v1.1 (review-public3): choice rows keep only "- {option}: {definition}" lines in `card` (the only card lines decoder_io
shows on a choice row in the trained cygnet / schema_branch_mark prompt); every other piece of choice guidance comes
from the *_CH_GUIDES pools and is written into `instructions` before the question (choice_instr). meta.card_render
records where the card text is shown. Selection, labels, options and option order are unchanged from v1.0; records
flagged sealed_drop are removed after the per-scheme shuffle (load), so v1.0's draw order is kept.
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common3 import (REC, TMP, base_meta, licence_string, loose_text, make_row, rng, sha,  # noqa: E402
                     stable_shuffle)
import pools as P  # noqa: E402

CLAIMED: dict[str, str] = {}          # loose sha -> unit key (global: one text, one group)
STATS = Counter()


def _eligible_before_sealed_drop(r) -> bool:
    return not any(v for k, v in r["flags"].items() if k not in ("outlet_redacted", "sealed_drop"))


def load(scheme):
    """Eligible records per part in a keyed shuffle order. The shuffle runs over the records eligible before the
    sealed_drop flag (fix v1.1), and sealed_drop records are removed after it, so the draw order of every other record
    is v1.0's."""
    out = {"train": [], "dev": []}
    with open(REC / f"{scheme}.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            assert r["eligible"] == (_eligible_before_sealed_drop(r) and not r["flags"].get("sealed_drop")), r["id"]
            if _eligible_before_sealed_drop(r):
                out[r["part"]].append(r)
    for k in out:
        out[k] = [r for r in stable_shuffle(out[k], "records", scheme, k) if r["eligible"]]
    return out


def claim(recs, unit_key) -> bool:
    hs = [r["loose_sha256"] for r in recs]
    if any(h in CLAIMED for h in hs) or len(set(hs)) != len(hs):
        STATS["claim_conflict"] += 1
        return False
    for h in hs:
        CLAIMED[h] = unit_key
    return True


def free(r) -> bool:
    """True if the record's loose text is not claimed yet (global over every public-3 dataset and segment)."""
    return r["loose_sha256"] not in CLAIMED


WTOK = re.compile(r"\w+")
ABSTAIN_LIKE = re.compile(r"\b(cannot|can['\u2019]t|not enough|unclear|unknown|none of (the|these)|undetermined|insufficient|"
                          r"not sure|no clear|can not)\b", re.I)


def lbt(text) -> int:
    """The G6 metadata length bucket of a state: int(log2(1 + number of \\w+ tokens)) (qc/g6.py `lb`)."""
    return int(math.log2(1 + len(WTOK.findall(text or ""))))


def bucket_mates(anchor, pools, st):
    """v2.0 matched sets: for each pool, the first free record (keyed pool order) whose state under format style `st`
    falls in the anchor's G6 length bucket; None if any pool has none."""
    b0, seen, out = lbt(wrap(st, anchor["text"])), {anchor["id"]}, []
    for pool in pools:
        m = next((x for x in pool if x["id"] not in seen and free(x) and lbt(wrap(st, x["text"])) == b0), None)
        if m is None:
            return None
        seen.add(m["id"])
        out.append(m)
    return out


def link(unit, kind, key):
    """v2.0 matched set: one twin set (cyclic twin_of chain, so a set drops and refills whole), meta.match_set = key.
    Every row keeps its own call_id (contrast twins with no relation term, spec 2.1)."""
    for i, r in enumerate(unit):
        r["meta"]["twin_of"] = unit[(i + 1) % len(unit)]["id"]
        r["meta"]["twin_kind"] = kind
        r["meta"]["match_set"] = "ms_" + sha(key)[:16]


WCOUNT: Counter = Counter()
LONG: dict = defaultdict(lambda: [0.0, 0.0])     # framing -> [sum of tie-aware 'gold is longest', sum of 1/k]


def long_credit(opts, gold):
    m = max(len(o) for o in opts)
    t = [o for o in opts if len(o) == m]
    return 1 / len(t) if gold in t else 0.0


def long_ok(framing, opts, gold, slack=0.5):
    """G10 'longest option is gold' within 1/k: accept a row only if it keeps the running tie-aware count within
    `slack` of the running sum of 1/k (rows are drawn from a large pool, so rejection costs nothing)."""
    a, e = LONG[framing]
    c = long_credit(opts, gold)
    return abs((a + c) - (e + 1 / len(opts))) <= max(slack, abs(a - e))


def long_add(framing, opts, gold):
    LONG[framing][0] += long_credit(opts, gold)
    LONG[framing][1] += 1 / len(opts)


def wpick(ws, framing, cls):
    """Wording for one unit: cycle the pool separately inside each gold class (offset by class), so wording and gold
    class are independent (G6 question-only baseline at chance)."""
    off = int(sha(f"{framing}|{cls}")[:4], 16)
    w = ws[(WCOUNT[(framing, cls)] + off) % len(ws)]
    WCOUNT[(framing, cls)] += 1
    return w


SCHEME_CNT: Counter = Counter()


def scheme_pick(key):
    """MAMS polarity label names: L1 on 3 of every 5 rows and L2 on 2, cycled inside each gold class, so label names
    are independent of the gold class (keeps 'longest option is gold' at 1/k)."""
    i = SCHEME_CNT[key]
    SCHEME_CNT[key] += 1
    return "L2" if i % 5 in (1, 3) else "L1"


def pick_defs(*key):
    return rng("defs", *key).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]


def wrap(style, text):
    return style["wrap"].format(text=text, text_json=json.dumps(text, ensure_ascii=False),
                                quoted="> " + text.replace("\n", "\n> "))


def interleave(by_class: dict, order: list):
    """Round-robin over classes (in a fixed order) -> one list; keeps any prefix class-balanced."""
    out, i = [], 0
    lists = {c: list(by_class.get(c, [])) for c in order}
    while any(lists.values()):
        c = order[i % len(order)]
        if lists[c]:
            out.append(lists[c].pop(0))
        i += 1
    return out


def split_units(units, n_main, part):
    if part == "dev":
        return {"dev": units[:n_main]}
    return {"main": units[:n_main], "reserve": units[n_main:]}


def place_options(opts_distractors, gold, key):
    d = stable_shuffle(opts_distractors, "opt", key)
    pos = rng("pos", key).randrange(len(d) + 1)
    return d[:pos] + [gold] + d[pos:]


def deflist(items):
    return "\n".join(f"- {name}: {d}" for name, d in items)


def choice_instr(guide, question):
    """Choice rows: card guidance that is not an option definition goes into instructions, before the question."""
    return question if not guide else guide.rstrip() + "\n" + question


def card_render(qtype, card, guide):
    if qtype == "noul":
        return "yn_card_whole" if card else "none"
    if card and guide:
        return "option_defs+instructions"
    if card:
        return "option_defs"
    return "instructions_only" if guide else "none"


# ------------------------------------------------------------------------------------------------ XED -------------
def xed_rows(recs, part, n_yn_pairs, n_ch4, n_ch9, n_main_frac):
    lic = licence_string("xed")
    emos = P.XED_EMOTIONS
    wheel = P.XED_WHEEL
    single = defaultdict(list)
    for r in recs:
        e = r["ann"]["emotions"]
        if len(e) == 1:
            single[e[0]].append(r)
    rows = defaultdict(list)

    def non_adjacent(L):
        i = wheel.index(L)
        adj = {wheel[(i - 1) % 8], wheel[(i + 1) % 8], L}
        return [e for e in emos if e not in adj]

    # yn pairs: yes on the line's own label L, no on asked emotion e (non-adjacent); per-emotion yes = no
    yes_need = Counter({e: 0 for e in emos})
    no_need = Counter({e: 0 for e in emos})
    tgt = {e: n_yn_pairs // 8 + (1 if i < n_yn_pairs % 8 else 0) for i, e in enumerate(stable_shuffle(emos, "xedtgt", part))}
    units_by = defaultdict(list)
    for L in emos:
        for r in single[L]:
            if yes_need[L] >= tgt[L]:
                break
            cands = sorted(non_adjacent(L), key=lambda e: (no_need[e], rng("xe", r["id"], e).random()))
            e = cands[0]
            if no_need[e] >= tgt[e] + 1:
                continue
            if not claim([r], f"xed_yn:{r['id']}"):
                continue
            yes_need[L] += 1
            no_need[e] += 1
            units_by[L].append((r, L, e))
    used = {u[0]["id"] for v in units_by.values() for u in v}
    STATS[f"xed_yn_{part}_yes_by_emotion"] = 0
    units = interleave({e: stable_shuffle(v, "xu", e, part) for e, v in units_by.items()}, emos)
    for j, (r, L, e) in enumerate(units):
        w = wpick(P.XED_YN_WORDINGS, "xed_yn", L)
        ds_style = pick_defs("xed_yn", r["id"])
        st = P.XED_STYLES[rng("st", r["id"]).randrange(len(P.XED_STYLES))]
        state = wrap(st, r["text"])
        pair = []
        for asked, has in ((L, 1), (e, 0)):
            gold = has if w["pol"] == "aff" else 1 - has
            card = None
            if ds_style != "none":
                card = P.XED_YN_CARDS[(w["pol"], ds_style)].format(emotion=asked, Emotion=asked.capitalize(),
                                                                    definition=P.XED_DEFS[asked])
            meta = base_meta(dataset="XED English", record_id=r["record_id"], licence=lic,
                             card_id=f"pub3_xed_yn_{w['id']}_{ds_style}_{asked}", wording_id=w["id"],
                             defs_style=ds_style, format_style=st["id"], structure=f"xed_yn|{r['id']}|{asked}",
                             edge=["emotion", "multilabel"], twin_kind="question_flip",
                             extra={"human_label": {"emotions": r["ann"]["emotions"]}, "asked": asked,
                                    "predicate_holds": has, "record_uid": r["id"], "xed_file": r["file"]})
            pair.append(make_row(ds="xed", framing="yn", key=f"{r['id']}|{asked}", group=sha(r["id"])[:16],
                                 state=state, instructions=w["text"].format(emotion=asked), options=None, gold=gold,
                                 role=w["pol"], card=card, meta=meta))
        pair[0]["meta"]["twin_of"], pair[1]["meta"]["twin_of"] = pair[1]["id"], pair[0]["id"]
        rows["yn"].append(pair)
    # choice rows
    for fr, n, labels in (("ch4", n_ch4, emos), ("ch9", n_ch9, emos + ["neutral"])):
        per = {c: n // len(labels) + (1 if i < n % len(labels) else 0)
               for i, c in enumerate(stable_shuffle(labels, "xedch", fr, part))}
        by = defaultdict(list)
        for c in labels:
            for r in single[c]:
                if len(by[c]) >= per[c]:
                    break
                if r["id"] in used:
                    continue
                if not claim([r], f"xed_{fr}:{r['id']}"):
                    continue
                used.add(r["id"])
                by[c].append(r)
        units = interleave({c: by[c] for c in labels}, stable_shuffle(labels, "xedord", fr, part))
        for j, r in enumerate(units):
            gold = r["ann"]["emotions"][0]
            if fr == "ch4":
                g_ = rng("xd", r["id"])
                for _try in range(40):
                    dis = g_.sample([e for e in emos if e != gold], 3)
                    if long_ok(f"xed_ch4_{part}", dis + [gold], gold):
                        break
                long_add(f"xed_ch4_{part}", dis + [gold], gold)
            else:
                dis = [e for e in labels if e != gold]
            opts = place_options(dis, gold, r["id"] + fr)
            w = wpick(P.XED_CH_WORDINGS, "xed_" + fr, gold)
            ds_style = pick_defs("xed_ch", r["id"])
            st = P.XED_STYLES[rng("st", r["id"]).randrange(len(P.XED_STYLES))]
            card = guide = None
            if ds_style != "none":
                shown = [c for c in labels if c in opts]
                card = deflist((c, P.XED_DEFS[c]) for c in shown)
                guide = P.XED_CH_GUIDES[ds_style]
            meta = base_meta(dataset="XED English", record_id=r["record_id"], licence=lic,
                             card_id=f"pub3_xed_{fr}_{w['id']}_{ds_style}", wording_id=w["id"], defs_style=ds_style,
                             format_style=st["id"], structure=f"xed_{fr}|{r['id']}", edge=["emotion", "choice"],
                             extra={"human_label": {"emotions": r["ann"]["emotions"]}, "k": len(opts),
                                    "record_uid": r["id"], "xed_file": r["file"],
                                    "card_render": card_render("choice", card, guide)})
            rows[fr].append([make_row(ds="xed", framing=fr, key=r["id"], group=sha(r["id"])[:16],
                                      state=wrap(st, r["text"]), instructions=choice_instr(guide, w["text"]),
                                      options=opts, gold=gold, role="choice", card=card, meta=meta)])
    return rows


# ------------------------------------------------------------------------------------------------ MAMS ------------
# v2.0 (repair r1, G6 root cause): v1.x question-flip pairs asked two different aspects of one sentence with the same
# polarity, so the asked aspect x polarity carried the gold (MAMS aspect-polarity priors: staff mostly negative, food
# mostly positive or neutral; question-only CV 57-64% vs 50%), and the choice rows asked one aspect whose polarity
# prior the question named. v2.0 builds MATCHED SETS: every partial input (question, card, guidance, options, option
# order, metadata) is shown once with every gold, so no partial input carries the label:
#   acsayn / atsayn  quads: sentences A, B and aspects c1, c2 (ACSA categories / ATSA single-word terms) with
#                    A: c1 = P, c2 != P and B: c1 != P, c2 = P. Each sentence is asked about both aspects (question
#                    flip) and each aspect question is asked on both sentences (state flip): 4 rows, one wording,
#                    card, defs style and format style; every row has its own call_id (contrast twins, spec 2.1).
#   acsach / atsach  triplets: one aspect and three sentences where it is positive / negative / neutral; one wording,
#                    label scheme, card, defs style, format style and option order (each position is gold once); the
#                    three states fall in one G6 length bucket.
# atsawh (which listed term has polarity P) is dropped: its options are the sentence's own terms, so no matched set
# shows one option list with every gold; its rows move to the two choice framings.
def _mams_pol_card(ds_style, subset, scheme, **target):
    """(card, guide) of a MAMS polarity choice row: card = one "- {label}: {definition}" line per label (the option
    texts of `scheme`); guide = the MAMS_POL_GUIDES text for instructions (None if the style has none)."""
    if ds_style == "none":
        return None, None
    inv = {v: k for k, v in P.MAMS_LABELS[scheme].items()}
    items = [(o, P.MAMS_LABEL_DEFS[inv[o]]) for o in [P.MAMS_LABELS[scheme][c] for c in ("positive", "negative", "neutral")]]
    g = P.MAMS_POL_GUIDES[(subset, ds_style)]
    return deflist(items), (g.format(**target) if g else None)


def _acsa_items(r):
    cs = [c for c, _ in r["ann"]["aspects"]]
    return {c: p for c, p in r["ann"]["aspects"] if c in P.MAMS_CATS and cs.count(c) == 1}


def _atsa_items(r):
    """lower-cased single-word term -> (polarity, surface form); a term listed twice in the sentence is never asked."""
    low = [t["term"].lower() for t in r["ann"]["terms"]]
    return {t["term"].lower(): (t["polarity"], t["term"]) for t in r["ann"]["terms"]
            if t["n_word"] == 1 and t["span_ok"] and low.count(t["term"].lower()) == 1}


def _pol(items, c):
    v = items.get(c)
    return v[0] if isinstance(v, tuple) else v


def mams_quads(recs, items_of, n_quads, part, tag):
    """[(P, c1, c2, A, B)]: A: c1 = P, c2 != P; B: c1 != P, c2 = P; P balanced over positive / negative."""
    pols = ["positive", "negative"]
    tgt = {p: n_quads // 2 + (1 if i < n_quads % 2 else 0) for i, p in enumerate(stable_shuffle(pols, tag, "qt", part))}
    items = {r["id"]: items_of(r) for r in recs}
    by_ip = defaultdict(list)
    for r in recs:
        for c in items[r["id"]]:
            by_ip[(c, _pol(items[r["id"]], c))].append(r)
    out, cnt = [], Counter()
    for a in recs:
        if len(out) >= n_quads:
            break
        ia = items[a["id"]]
        if not free(a) or len(ia) < 2:
            continue
        got = None
        for p in stable_shuffle(pols, tag, "qp", a["id"]):
            if cnt[p] >= tgt[p]:
                continue
            for c1 in stable_shuffle(sorted(c for c in ia if _pol(ia, c) == p), tag, "c1", a["id"]):
                for c2 in stable_shuffle(sorted(c for c in ia if _pol(ia, c) != p), tag, "c2", a["id"]):
                    for b in by_ip[(c2, p)]:
                        ib = items[b["id"]]
                        if b["id"] != a["id"] and free(b) and c1 in ib and _pol(ib, c1) != p:
                            got = (p, c1, c2, a, b)
                            break
                    if got:
                        break
                if got:
                    break
            if got:
                break
        if got and claim([a, got[4]], f"{tag}:{a['id']}+{got[4]['id']}"):
            out.append(got)
            cnt[got[0]] += 1
    return out


def mams_triplets(recs, items_of, n_trip, part, tag, styles):
    """[(aspect, style, key, {polarity: record})]: one aspect, three sentences (positive / negative / neutral) whose
    wrapped states share one G6 length bucket under the set's format style."""
    pol3 = ["positive", "negative", "neutral"]
    items = {r["id"]: items_of(r) for r in recs}
    by_ip = defaultdict(list)
    for r in recs:
        for c in items[r["id"]]:
            by_ip[(c, _pol(items[r["id"]], c))].append(r)
    out = []
    for a in recs:
        if len(out) >= n_trip:
            break
        if not free(a):
            continue
        ia = items[a["id"]]
        for c in stable_shuffle(sorted(ia), tag, "tc", a["id"]):
            key = f"{tag}:{part}:{a['id']}:{c}"
            st = styles[rng("st", key).randrange(len(styles))]
            b0 = lbt(wrap(st, a["text"]))
            mates = {_pol(ia, c): a}
            for q in pol3:
                if q in mates:
                    continue
                m = next((x for x in by_ip[(c, q)] if free(x) and x["id"] not in {y["id"] for y in mates.values()}
                          and lbt(wrap(st, x["text"])) == b0), None)
                if m is None:
                    break
                mates[q] = m
            if len(mates) == 3 and claim(list(mates.values()), key):
                out.append((c, st, key, mates))
                break
    return out


def mams_rows(acsa, atsa, part, n):
    lic = licence_string("mams")
    rows = defaultdict(list)
    pol3 = ["positive", "negative", "neutral"]
    # ---- yes/no quads (scarcer than triplets: built first)
    for sub, recs, items_of, fr, ws, n_q in (("acsa", acsa, _acsa_items, "acsayn", P.ACSA_YN_WORDINGS, n["acsa_yn"]),
                                            ("atsa", atsa, _atsa_items, "atsayn", P.ATSA_YN_WORDINGS, n["atsa_yn"])):
        for (p, c1, c2, a, b) in mams_quads(recs, items_of, n_q, part, f"{sub}_yn"):
            key = f"{sub}_yn:{a['id']}+{b['id']}"
            w = wpick(ws, f"{sub}_yn", "set")
            ds_style = pick_defs(f"{sub}_yn", key)
            st = P.MAMS_STYLES[rng("st", key).randrange(len(P.MAMS_STYLES))]
            ia, ib = items_of(a), items_of(b)
            unit = []
            for r, it in ((a, ia), (b, ib)):
                for c in (c1, c2):
                    has = int(_pol(it, c) == p)
                    gold = has if w["pol"] == "aff" else 1 - has
                    if sub == "acsa":
                        catn = P.MAMS_CATS[c]
                        card = None if ds_style == "none" else P.ACSA_YN_CARDS[(w["pol"], ds_style)].format(
                            pol=p, cat=catn, catdef=P.MAMS_CAT_DEFS[c])
                        ins = w["text"].format(pol=p, cat=catn, adv=P.POL_ADV[p])
                        hl = {"aspects": r["ann"]["aspects"]}
                        edge = ["aspect_sentiment", "multi_aspect", "matched_set"]
                        ds_name = "MAMS (ACSA)"
                    else:
                        term = ia[c][1]                  # one surface form (sentence A's) for the four rows
                        card = None if ds_style == "none" else P.ATSA_YN_CARDS[(w["pol"], ds_style)].format(pol=p, term=term)
                        ins = w["text"].format(pol=p, term=term, adv=P.POL_ADV[p])
                        hl = {"terms": [(x["term"], x["polarity"]) for x in r["ann"]["terms"]]}
                        edge = ["target_sentiment", "multi_target", "matched_set"]
                        ds_name = "MAMS (ATSA)"
                    meta = base_meta(dataset=ds_name, record_id=r["record_id"], licence=lic,
                                     card_id=f"pub3_mams_{sub}_yn_{w['id']}_{ds_style}_{p}", wording_id=w["id"],
                                     defs_style=ds_style, format_style=st["id"], structure=f"{sub}_yn|{r['id']}|{c}|{p}",
                                     edge=edge, extra={"human_label": hl, "asked": c, "asked_polarity": p,
                                                       "predicate_holds": has, "record_uid": r["id"],
                                                       "subset": sub.upper()})
                    unit.append(make_row(ds="mams", framing=fr, key=f"{r['id']}|{c}|{p}", group=sha(r["id"])[:16],
                                         state=wrap(st, r["text"]), instructions=ins, options=None, gold=gold,
                                         role=w["pol"], card=card, meta=meta))
            link(unit, "question_flip+state_flip", key)
            rows[fr].append(unit)
    # ---- polarity choice triplets (k = 3)
    for sub, recs, items_of, fr, ws, n_t in (("acsa", acsa, _acsa_items, "acsach", P.ACSA_CH_WORDINGS, n["acsa_ch"]),
                                            ("atsa", atsa, _atsa_items, "atsach", P.ATSA_CH_WORDINGS, n["atsa_ch"])):
        for (c, st, key, mates) in mams_triplets(recs, items_of, n_t, part, f"{sub}_ch", P.MAMS_STYLES):
            scheme = scheme_pick(f"{part}|{fr}")
            lab = P.MAMS_LABELS[scheme]
            order = stable_shuffle([lab[q] for q in pol3], "opt", key)
            w = wpick(ws, f"{sub}_ch", "set")
            ds_style = pick_defs(f"{sub}_ch", key)
            if sub == "acsa":
                catn = P.MAMS_CATS[c]
                card, guide = _mams_pol_card(ds_style, "acsa", scheme, cat=catn, catdef=P.MAMS_CAT_DEFS[c])
                q_text = w["text"].format(cat=catn)
            else:
                term = _atsa_items(mates[stable_shuffle(pol3, "srf", key)[0]])[c][1]
                card, guide = _mams_pol_card(ds_style, "atsa", scheme, term=term)
                q_text = w["text"].format(term=term)
            unit = []
            for q in pol3:
                r = mates[q]
                if sub == "acsa":
                    hl, ds_name, edge = {"aspects": r["ann"]["aspects"]}, "MAMS (ACSA)", ["aspect_sentiment", "choice", "matched_set"]
                else:
                    hl = {"terms": [(x["term"], x["polarity"]) for x in r["ann"]["terms"]]}
                    ds_name, edge = "MAMS (ATSA)", ["target_sentiment", "choice", "matched_set"]
                meta = base_meta(dataset=ds_name, record_id=r["record_id"], licence=lic,
                                 card_id=f"pub3_mams_{sub}_ch_{w['id']}_{ds_style}_{scheme}", wording_id=w["id"],
                                 defs_style=ds_style, format_style=st["id"], structure=f"{sub}_ch|{r['id']}|{c}",
                                 edge=edge, extra={"human_label": hl, "asked": c, "label_scheme": scheme, "k": 3,
                                                   "record_uid": r["id"], "subset": sub.upper(),
                                                   "card_render": card_render("choice", card, guide)})
                unit.append(make_row(ds="mams", framing=fr, key=f"{r['id']}|{c}", group=sha(r["id"])[:16],
                                     state=wrap(st, r["text"]), instructions=choice_instr(guide, q_text),
                                     options=list(order), gold=lab[q], role="choice", card=card, meta=meta))
            link(unit, "class_set", key)
            rows[fr].append(unit)
    return rows


# ------------------------------------------------------------------------------------------------ Sarcasm ---------
def sarcasm_rows(recs, part, n_yn, n_ch):
    lic = licence_string("sarcasm")
    rows = defaultdict(list)
    pos = [r for r in recs if r["ann"]["is_sarcastic"] == 1]
    neg = [r for r in recs if r["ann"]["is_sarcastic"] == 0]
    used = set()
    # yn (v2.0, repair r1): (sarcastic, not sarcastic) state-flip pairs that share wording, defs style, card and
    # format style, with both headlines in one G6 length bucket (v1.x drew card and format per headline, so card x gold
    # balance held only on average)
    pairs = []
    for a in pos:
        if len(pairs) >= n_yn // 2:
            break
        if not free(a):
            continue
        key = f"sar_yn:{part}:{a['id']}"
        st = P.SAR_STYLES[rng("st", key).randrange(len(P.SAR_STYLES))]
        m = bucket_mates(a, [neg], st)
        if m is None or not claim([a] + m, key):
            continue
        used.update((a["id"], m[0]["id"]))
        pairs.append((key, st, a, m[0]))
    for key, st, a, b in pairs:
        w = wpick(P.SAR_YN_WORDINGS, "sar_yn", "set")
        ds_style = pick_defs("sar_yn", key)
        card = None if ds_style == "none" else P.SAR_YN_CARDS[(w["pol"], ds_style)]
        unit = []
        for r in (a, b):
            lab = r["ann"]["is_sarcastic"]
            gold = lab if w["pol"] == "aff" else 1 - lab
            meta = base_meta(dataset="News Headlines Sarcasm v2", record_id=r["record_id"], licence=lic,
                             card_id=f"pub3_sarcasm_yn_{w['id']}_{ds_style}", wording_id=w["id"], defs_style=ds_style,
                             format_style=st["id"], structure=f"sar_yn|{r['id']}", edge=["sarcasm", "matched_set"],
                             extra={"human_label": {"is_sarcastic": lab}, "predicate_holds": lab, "record_uid": r["id"],
                                    "outlet_redacted": r["flags"]["outlet_redacted"]})
            unit.append(make_row(ds="sarcasm", framing="yn", key=r["id"], group=sha(r["id"])[:16],
                                 state=wrap(st, r["text"]), instructions=w["text"], options=None, gold=gold,
                                 role=w["pol"], card=card, meta=meta))
        link(unit, "state_flip", key)
        rows["yn"].append(unit)
    # choice (v2.0, repair r1, G6 root cause): v1.x balanced "longest headline is gold" and the gold position only over
    # the whole framing, so wording (direct / inverted) x length rank and metadata x position cells were unbalanced
    # (metadata x option-kind view 2.6 pp over chance). v2.0 builds MATCHED SETS of k rows (k = 2 or 3 headlines, one
    # wording, defs style and format style): row i's gold headline has length rank i among its options (characters,
    # no ties) and sits at position perm[i], so in every set each length rank and each position is gold exactly once.
    # Options are human headlines; exactly one is sarcastic (direct wordings) or exactly one sincere (inverted).
    def n_sets(n):
        b = int(0.4 * n) // 3                  # about 40% of the rows have k = 3 (as v1.x)
        while b >= 0 and (n - 3 * b) % 2:
            b -= 1
        return (n - 3 * b) // 2, b
    a2, b3 = n_sets(n_ch)
    # A headline that reads like an abstain option (the qc/g10.py abstain pattern: "can't", "unknown", "not sure", ...)
    # is never a choice option (spec G10: a shown abstain option must be wrong on >= 50% of its rows, and a headline
    # option is gold on 1/k of its rows); it can still be a yes/no state. Applied to both classes alike.
    pos_l = [r for r in pos if r["id"] not in used and not ABSTAIN_LIKE.search(r["text"])]
    neg_l = [r for r in neg if r["id"] not in used and not ABSTAIN_LIKE.search(r["text"])]

    def pick_row(gpool, dpool, k, rank, excl):
        """first free gold headline + (k - 1) free distractors, all lengths distinct, gold at length rank `rank`
        (0 = shortest)."""
        for g in gpool:
            if g["id"] in excl or not free(g):
                continue
            L = len(g["text"])
            need_lo, need_hi = rank, k - 1 - rank                     # distractors shorter / longer than the gold
            lo, hi, lens = [], [], {L}
            for d in dpool:
                if len(lo) == need_lo and len(hi) == need_hi:
                    break
                if d["id"] in excl or not free(d) or len(d["text"]) in lens:
                    continue
                if len(d["text"]) < L and len(lo) < need_lo:
                    lo.append(d)
                    lens.add(len(d["text"]))
                elif len(d["text"]) > L and len(hi) < need_hi:
                    hi.append(d)
                    lens.add(len(d["text"]))
            if len(lo) == need_lo and len(hi) == need_hi:
                return g, lo + hi
        return None

    kinds = stable_shuffle([3] * b3 + [2] * a2, "sarck", part)
    for si, k in enumerate(kinds):
        w = wpick(P.SAR_CH_WORDINGS, "sar_ch", f"k{k}")
        gpool, dpool = (neg_l, pos_l) if w["inv"] else (pos_l, neg_l)
        skey = f"sar_ch:{part}:{si}"
        ds_style = pick_defs("sar_ch", skey)
        st = P.SAR_STYLES[rng("st", skey).randrange(len(P.SAR_STYLES))]
        ranks = stable_shuffle(list(range(k)), "rank", skey)
        perm = stable_shuffle(list(range(k)), "perm", skey)
        excl, picked = set(), []
        for rank in ranks:
            got = pick_row(gpool, dpool, k, rank, excl)
            if got is None:
                break
            g, ds_ = got
            if not claim([g] + ds_, f"sar_ch:{g['id']}"):
                break
            excl.update(x["id"] for x in [g] + ds_)
            used.update(x["id"] for x in [g] + ds_)
            picked.append((g, ds_))
        if len(picked) != k:
            STATS["sar_ch_set_short"] += 1
            continue
        unit = []
        for i, (g, ds_) in enumerate(picked):
            members = [g] + ds_
            key = "+".join(r["id"] for r in members)
            others = stable_shuffle([r["text"] for r in ds_], "opt", key)
            opts = others[:perm[i]] + [g["text"]] + others[perm[i]:]
            card = None                               # the options (headlines) carry no definitions
            guide = None if ds_style == "none" else P.SAR_CH_GUIDES[(w["inv"], ds_style)]
            meta = base_meta(dataset="News Headlines Sarcasm v2", record_id="+".join(r["record_id"] for r in members),
                             licence=lic, card_id=f"pub3_sarcasm_ch_{w['id']}_{ds_style}", wording_id=w["id"],
                             defs_style=ds_style, format_style=st["id"], structure=f"sar_ch|{key}",
                             edge=["sarcasm", "choice", "inverted" if w["inv"] else "direct", "matched_set"],
                             extra={"human_label": {"is_sarcastic_by_option": {r["record_id"]: r["ann"]["is_sarcastic"]
                                                                               for r in members}},
                                    "inverted": w["inv"], "k": k, "record_uid": [r["id"] for r in members],
                                    "outlet_redacted": any(r["flags"]["outlet_redacted"] for r in members),
                                    "card_render": card_render("choice", card, guide)})
            state = st["ch"]                          # literal (never str.format-ted); JSON styles must parse
            if st["wrap"].lstrip().startswith("{"):
                json.loads(state)
            unit.append(make_row(ds="sarcasm", framing="ch", key=key, group=sha(key)[:16], state=state,
                                 instructions=choice_instr(guide, w["text"]), options=opts, gold=g["text"],
                                 role="choice", card=card, meta=meta))
        link(unit, "class_set", skey)
        rows["ch"].append(unit)
    return rows


# ------------------------------------------------------------------------------------------------ GHC -------------
def ghc_rows(recs, part, n_yn_per_label, n_ch):
    lic = licence_string("ghc")
    rows = defaultdict(list)
    L = P.GHC_LABELS
    used = set()
    need_yes = {l: n_yn_per_label // 2 for l in L}
    need_no = {l: n_yn_per_label // 2 for l in L}
    got_yes, got_no = Counter(), Counter()
    units = []
    # 1) question-flip pairs, scarcest positive label first (cv, then hd, then vo)
    for a in ("cv", "hd", "vo"):
        for r in recs:
            if got_yes[a] >= need_yes[a]:
                break
            v = r["ann"]
            if v[a] != 1 or r["id"] in used:
                continue
            zeros = [b for b in L if v[b] == 0 and got_no[b] < need_no[b]]
            if not zeros:
                continue
            b = sorted(zeros, key=lambda x: (got_no[x], rng("gb", r["id"], x).random()))[0]
            if not claim([r], f"ghc_yn:{r['id']}"):
                continue
            used.add(r["id"])
            got_yes[a] += 1
            got_no[b] += 1
            units.append((r, [(a, 1), (b, 0)]))
    # 2) remaining yes needs as singles, then remaining no needs from posts with that label 0 (prefer posts with
    #    another label 1, else all-zero posts)
    for a in L:
        for r in recs:
            if got_yes[a] >= need_yes[a]:
                break
            if r["ann"][a] == 1 and r["id"] not in used and claim([r], f"ghc_yn:{r['id']}"):
                used.add(r["id"])
                got_yes[a] += 1
                units.append((r, [(a, 1)]))
    for b in L:
        for pref in (True, False):
            for r in recs:
                if got_no[b] >= need_no[b]:
                    break
                v = r["ann"]
                if v[b] != 0 or r["id"] in used or (any(v.values()) != pref):
                    continue
                if claim([r], f"ghc_yn:{r['id']}"):
                    used.add(r["id"])
                    got_no[b] += 1
                    units.append((r, [(b, 0)]))
    STATS[f"ghc_yn_{part}_yes"] = sum(got_yes.values())
    STATS[f"ghc_yn_{part}_no"] = sum(got_no.values())
    units = stable_shuffle(units, "ghcu", part)
    wcount = Counter()
    for r, asks in units:
        ds_style = pick_defs("ghc_yn", r["id"])
        st = P.POST_STYLES[rng("st", r["id"]).randrange(len(P.POST_STYLES))]
        group = []
        for lab, has in asks:
            ws = [w for w in P.GHC_YN_WORDINGS if w["label"] == lab]
            w = ws[wcount[(lab, has)] % len(ws)]
            wcount[(lab, has)] += 1
            gold = has if w["pol"] == "aff" else 1 - has
            card = None if ds_style == "none" else P.GHC_YN_CARDS[(w["pol"], ds_style)].format(**{"def": P.GHC_DEFS[lab]})
            meta = base_meta(dataset="Gab Hate Corpus", record_id=r["record_id"], licence=lic,
                             card_id=f"pub3_ghc_yn_{w['id']}_{ds_style}", wording_id=w["id"], defs_style=ds_style,
                             format_style=st["id"], structure=f"ghc_yn|{r['id']}|{lab}", edge=["hate", lab],
                             twin_kind="question_flip" if len(asks) == 2 else None,
                             extra={"human_label": r["ann"], "asked": lab, "predicate_holds": has,
                                    "record_uid": r["id"]})
            group.append(make_row(ds="ghc", framing="yn", key=f"{r['id']}|{lab}", group=sha(r["id"])[:16],
                                  state=wrap(st, r["text"]), instructions=w["text"], options=None, gold=gold,
                                  role=w["pol"], card=card, meta=meta))
        if len(group) == 2:
            group[0]["meta"]["twin_of"], group[1]["meta"]["twin_of"] = group[1]["id"], group[0]["id"]
        rows["yn"].append(group)
    # choice: hate (hd or cv) / vulgar only / none; cv posts are kept for the yn rows
    cls = {"hate": [], "vo": [], "none": []}
    per = n_ch // 3
    tgtc = {"hate": per + (1 if n_ch % 3 > 0 else 0), "vo": per + (1 if n_ch % 3 > 1 else 0), "none": per}
    for r in recs:
        if r["id"] in used:
            continue
        v = r["ann"]
        if v["cv"] == 1:
            continue
        c = "hate" if v["hd"] == 1 else ("vo" if v["vo"] == 1 else "none")
        if len(cls[c]) < tgtc[c] and claim([r], f"ghc_ch:{r['id']}"):
            used.add(r["id"])
            cls[c].append(r)
    opt_text = P.GHC_CH_OPTIONS
    units = interleave(cls, ["hate", "vo", "none"])
    for j, r in enumerate(units):
        v = r["ann"]
        c = "hate" if v["hd"] == 1 else ("vo" if v["vo"] == 1 else "none")
        gold = opt_text[c]
        opts = place_options([opt_text[x] for x in opt_text if x != c], gold, r["id"] + "ghcch")
        w = wpick(P.GHC_CH_WORDINGS, "ghc_ch", c)
        ds_style = pick_defs("ghc_ch", r["id"])
        st = P.POST_STYLES[rng("st", r["id"]).randrange(len(P.POST_STYLES))]
        card = guide = None
        if ds_style != "none":
            card = P.GHC_CH_CARDS[ds_style].format(**P.GHC_DEFS)
            guide = P.GHC_CH_GUIDES[ds_style]
        meta = base_meta(dataset="Gab Hate Corpus", record_id=r["record_id"], licence=lic,
                         card_id=f"pub3_ghc_ch_{w['id']}_{ds_style}", wording_id=w["id"], defs_style=ds_style,
                         format_style=st["id"], structure=f"ghc_ch|{r['id']}", edge=["hate", "choice"],
                         extra={"human_label": v, "k": 3, "record_uid": r["id"], "class": c,
                                "card_render": card_render("choice", card, guide)})
        rows["ch"].append([make_row(ds="ghc", framing="ch", key=r["id"], group=sha(r["id"])[:16],
                                    state=wrap(st, r["text"]), instructions=choice_instr(guide, w["text"]),
                                    options=opts, gold=gold, role="choice", card=card, meta=meta)])
    return rows


# ------------------------------------------------------------------------------------------------ EDOS ------------
# v2.0 (repair r1, G6 root cause): v1.x drew each yes/no row's defs style (card variant) and format style per record,
# and cycled wordings per label, so card x gold was unbalanced by chance at n = 246 (card + guidance LR 0.553 vs 0.50).
# v2.0 builds matched sets: yn = (sexist, not sexist) state-flip pairs; ch5 / ch4 = one post per class. A set shares
# its wording, defs style, card, format style and (choice) option order, and its posts fall in one G6 length bucket.
def edos_rows(recs, part, n_yn, n_ch5, n_ch4):
    lic = licence_string("edos")
    rows = defaultdict(list)
    catname = P.EDOS_CATS
    cats = list(catname.values())
    by = defaultdict(list)
    for r in recs:
        c = r["ann"]["label_category"]
        by["not sexist" if c == "none" else catname[c]].append(r)
    # choice class sets first (threats and prejudiced discussion are scarce): the scarcest class anchors each set
    for fr, n, labels in (("ch5", n_ch5, cats + ["not sexist"]), ("ch4", n_ch4, cats)):
        ws = [w for w in P.EDOS_CH_WORDINGS if w["k"] == len(labels)]
        scarce = min(labels, key=lambda c: (len(by[c]), c))
        others = [c for c in labels if c != scarce]
        sets = []
        for a in by[scarce]:
            if len(sets) >= n // len(labels):
                break
            if not free(a):
                continue
            key = f"edos_{fr}:{part}:{a['id']}"
            st = P.POST_STYLES[rng("st", key).randrange(len(P.POST_STYLES))]
            mates = bucket_mates(a, [by[c] for c in others], st)
            if mates is None or not claim([a] + mates, key):
                continue
            sets.append((key, st, dict(zip([scarce] + others, [a] + mates))))
        for key, st, mem in sets:
            order = stable_shuffle(labels, "opt", key)
            w = wpick(ws, "edos_" + fr, "set")
            ds_style = pick_defs("edos_ch", key)
            card = guide = None
            if ds_style != "none":
                card = deflist((x, P.EDOS_CAT_DEFS[x]) for x in labels)
                guide = P.EDOS_CH_GUIDES[ds_style]
            unit = []
            for gold in labels:
                r = mem[gold]
                assert gold == ("not sexist" if r["ann"]["label_category"] == "none" else catname[r["ann"]["label_category"]])
                meta = base_meta(dataset="EDOS", record_id=r["record_id"], licence=lic,
                                 card_id=f"pub3_edos_{fr}_{w['id']}_{ds_style}", wording_id=w["id"], defs_style=ds_style,
                                 format_style=st["id"], structure=f"edos_{fr}|{r['id']}",
                                 edge=["sexism", "choice", "matched_set"],
                                 extra={"human_label": r["ann"], "k": len(labels), "record_uid": r["id"],
                                        "card_render": card_render("choice", card, guide)})
                unit.append(make_row(ds="edos", framing=fr, key=r["id"], group=sha(r["id"])[:16],
                                     state=wrap(st, r["text"]), instructions=choice_instr(guide, w["text"]),
                                     options=list(order), gold=gold, role="choice", card=card, meta=meta))
            link(unit, "class_set", key)
            rows[fr].append(unit)
    # yn: (sexist, not sexist) state-flip pairs; the sexist side is the natural category mix of the unused posts
    pairs = []
    for a in stable_shuffle([r for c in cats for r in by[c]], "edsx", part):
        if len(pairs) >= n_yn // 2:
            break
        if not free(a):
            continue
        key = f"edos_yn:{part}:{a['id']}"
        st = P.POST_STYLES[rng("st", key).randrange(len(P.POST_STYLES))]
        m = bucket_mates(a, [by["not sexist"]], st)
        if m is None or not claim([a] + m, key):
            continue
        pairs.append((key, st, a, m[0]))
    for key, st, a, b in pairs:
        w = wpick(P.EDOS_YN_WORDINGS, "edos_yn", "set")
        ds_style = pick_defs("edos_yn", key)
        card = None if ds_style == "none" else P.EDOS_YN_CARDS[(w["pol"], ds_style)].format(**{"def": P.EDOS_SEXIST_DEF})
        unit = []
        for r, lab in ((a, 1), (b, 0)):
            assert lab == (r["ann"]["label_sexist"] == "sexist") == (r["ann"]["label_category"] != "none")
            gold = lab if w["pol"] == "aff" else 1 - lab
            meta = base_meta(dataset="EDOS", record_id=r["record_id"], licence=lic,
                             card_id=f"pub3_edos_yn_{w['id']}_{ds_style}", wording_id=w["id"], defs_style=ds_style,
                             format_style=st["id"], structure=f"edos_yn|{r['id']}", edge=["sexism", "matched_set"],
                             extra={"human_label": r["ann"], "predicate_holds": lab, "record_uid": r["id"]})
            unit.append(make_row(ds="edos", framing="yn", key=r["id"], group=sha(r["id"])[:16],
                                 state=wrap(st, r["text"]), instructions=w["text"], options=None, gold=gold,
                                 role=w["pol"], card=card, meta=meta))
        link(unit, "state_flip", key)
        rows["yn"].append(unit)
    return rows


# ------------------------------------------------------------------------------------------------ driver ----------
# r1 main targets (rows) and reserve (~25%) per framing; dev (mix-tuning dev) sizes in rows
PLAN = {
    "xed": {"yn": (300, 80, 20), "ch4": (150, 40, 10), "ch9": (150, 40, 10)},
    # v2.0: quads (4 rows) and triplets (3 rows); atsawh dropped (see the MAMS section)
    "mams": {"acsayn": (180, 48, 12), "acsach": (195, 48, 12), "atsayn": (180, 48, 12), "atsach": (195, 48, 12)},
    "sarcasm": {"yn": (180, 46, 16), "ch": (170, 44, 14)},
    # v2.0: yn pairs, ch5 sets of 5, ch4 sets of 4
    "edos": {"yn": (182, 46, 20), "ch5": (100, 25, 10), "ch4": (68, 20, 8)},
}
# v2.0 (repair r1): GHC is dropped from public-3 by the spec 8 G5 dataset-level rule for public rows ("drop the dataset
# if > 8% clearly wrong"): the independent G5 read (6 Oct) found 10/100 clearly wrong golds, all equal to the released
# ghc_train.tsv majority labels (dataset label noise, not a parse bug). ghc_train.tsv (the only file spec 3.2 #16 and
# LICENCE_REGISTER allow) carries majority labels only, no vote shares, so no program-level record selection can
# separate the noisy labels. Spec 3.2: a set with no named fallback sends its rows to the own family closest in skill
# (F11 for 3E), logged in the mixer report. ghc_rows() is kept for the record and never called.
DROPPED = {"ghc": "spec 8 G5 (public rows): 10/100 clearly wrong > 8% -> dataset dropped; 350 r1 rows -> F11 (spec 3.2 "
                  "fallback rule for 3E), logged in the mixer report"}


def flatten_take(groups, n_rows):
    """Take whole units (lists of rows) in order until n_rows rows; return (taken, rest)."""
    out, rest, k = [], [], 0
    for g in groups:
        if k + len(g) <= n_rows and k < n_rows:
            out.append(g)
            k += len(g)
        else:
            rest.append(g)
    return out, rest


def build(ds):
    """Main, reserve and dev are drawn by separate calls (main first), so each segment is class- and label-balanced
    on its own; text claims are global, so a later segment never reuses an earlier segment's text."""
    res = {"main": [], "reserve": [], "dev": []}
    plan = PLAN[ds]
    cache = {}
    for seg, part, idx in (("main", "train", 0), ("reserve", "train", 1), ("dev", "dev", 2)):
        def n(fr):
            return plan[fr][idx]
        def recs(scheme):
            if (scheme, part) not in cache:
                cache[(scheme, part)] = load(scheme)[part]
            return cache[(scheme, part)]
        if ds == "xed":
            rows = xed_rows(recs("xed"), seg, n("yn") // 2, n("ch4"), n("ch9"), None)
        elif ds == "mams":
            rows = mams_rows(recs("mams_acsa"), recs("mams_atsa"), seg,
                             {"acsa_yn": n("acsayn") // 4, "acsa_ch": n("acsach") // 3, "atsa_yn": n("atsayn") // 4,
                              "atsa_ch": n("atsach") // 3})
        elif ds == "sarcasm":
            rows = sarcasm_rows(recs("sarcasm_v2"), seg, n("yn"), n("ch"))
        else:
            rows = edos_rows(recs("edos"), seg, n("yn"), n("ch5"), n("ch4"))
        for fr in plan:
            groups = rows.get(fr, [])
            want = plan[fr][idx]
            taken, rest = flatten_take(groups, want)
            assert not rest, (ds, seg, fr, len(rest))
            got = sum(len(g) for g in taken)
            res[seg] += [x for g in taken for x in g]
            STATS[f"{ds}_{fr}_{seg}"] = got
            if got != want:
                STATS[f"{ds}_{fr}_{seg}_short"] = want - got
    return res


def main():
    for ds in ("edos", "xed", "mams", "sarcasm"):     # scarce-label sets first (global text claims); ghc dropped
        res = build(ds)
        (TMP / f"cand_{ds}.json").write_text(json.dumps(res, ensure_ascii=False))
        print(ds, {k: len(v) for k, v in res.items()}, flush=True)
    (TMP / "build_rows_stats.json").write_text(json.dumps(STATS, indent=1, sort_keys=True))
    claims = [{"loose_sha256": h, "unit": u} for h, u in sorted(CLAIMED.items())]
    (TMP / "claims_all.json").write_text(json.dumps(claims))
    print(json.dumps({k: v for k, v in sorted(STATS.items()) if "short" in k or "conflict" in k}), flush=True)


if __name__ == "__main__":
    main()
