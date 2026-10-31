"""F11 build driver: cards, rows, twins, relations, inline G2 / G3 checks, outputs.

  python gen/build.py <set> [--cards N] [--only S1,S2]
  sets: cand (out/candidates_r1.jsonl, 1.5 x r1 rows), qc (out/qc_sample.jsonl, >= 5,000 rows), dev (out/mixdev_S5)
Every row is checked by check.check_row (G2 solver A = B = C; G3 round trip) and fmt1 loader_check (in emit). Any
failure is counted and the build exits 2: a failing row is a generator bug (fix, then regenerate all).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check as CK                     # noqa: E402
import packs_f11 as P                  # noqa: E402
from cardgen import make_program_card  # noqa: E402
from common import OUT, TMP, rng, write_jsonl, progress  # noqa: E402
from forms import FormGen              # noqa: E402
from rows import RowFail               # noqa: E402
from tax import CardInvalid            # noqa: E402
import twins as TW                     # noqa: E402
import lex                             # noqa: E402

# r1 rows x 1.5 per sampler (G0 section 1) and r1 cards
PLAN = {"S1": (840, 12), "S2": (840, 12), "S3": (750, 11), "S4": (675, 10), "S6": (675, 11)}
SHORT = {"S1": 3, "S2": 3}
INVERTED = {"S1": 4, "S2": 3, "S4": 3}
YN_SHARE = 0.47
NEG_UNIT_P = 0.16
FLIP_P = 0.26
ATTACK_P = 0.055
INERT_P = 0.03
MISSING_P = 0.12


def card_plan(seed_tag="r1"):
    """(sampler, idx, kwargs) for every program card, with its pack (one pack per card, XF09)."""
    packs = P.program_packs(False)
    r = rng("cardplan", seed_tag)
    r.shuffle(packs)
    plan, pi = [], 0
    for s, (_, ncards) in PLAN.items():
        for j in range(ncards):
            kw = {}
            if j < SHORT.get(s, 0):
                kw["short"] = True
            elif j < SHORT.get(s, 0) + INVERTED.get(s, 0):
                kw["inverted"] = True
            if not kw.get("short") and s != "S6" and r.random() < 0.3:
                kw["default_missing"] = True
            plan.append([s, j, kw])
    return plan, packs


def build_cards(plan, packs, *, only=None, max_cards=None):
    cards, used = [], set()
    pool = list(packs)
    prio = {"S6": 0, "S3": 1, "S4": 2, "S5": 3, "S1": 4, "S2": 5}     # the pickiest samplers draw packs first
    for s, j, kw in sorted(plan, key=lambda x: (prio.get(x[0], 9), x[1])):
        if only and s not in only:
            continue
        if max_cards and sum(1 for c in cards if c.sampler == s) >= max_cards:
            continue
        got = None
        for v in pool:
            if v["pack_id"] in used:
                continue
            for att in range(8):
                try:
                    got = make_program_card(s, v, j, attempt=att, **kw)
                    break
                except CardInvalid:
                    continue
            if got:
                used.add(v["pack_id"])
                got._mk = (s, v, j, att, kw)
                break
        if got is None:
            raise SystemExit(f"no card for {s} {j}")
        got.plan_kw = kw
        got.trim = 0
        cards.append(got)
    add_examples(cards)
    length_trim(cards)
    return cards


# ------------------------------------------------------------------------------------------ G15 length (served)
MAX_SERVED = 7900          # every row <= 7,900 served tokens (A22; toklen.row_len = decoder_io served prompt)
CARD_BUDGET = 7300         # probe budget per card: margin under the cap for styles / states the probe did not draw
PROBE_N = 24
TRIM_LOG = []


def probe_len(card):
    """Max served tokens over PROBE_N choice rows of a deep copy of the card (own 'probe' row stream; the card itself
    and every set's row stream are untouched)."""
    import copy
    from toklen import served_lens
    c = copy.deepcopy(card)
    g = FormGen(c, "probe", n_target=PROBE_N)
    rows = []
    for i in range(PROBE_N * 4):
        if len(rows) >= PROBE_N:
            break
        try:
            spec = g.inverted_spec() if c.inverted else g.choice_spec()
            rows.append(g.emit(spec, rid=f"probe-{i}", gid=f"probe-{i}", cid=f"probe-{i}-c0"))
        except (RowFail, CardInvalid):
            continue
    return max(served_lens(rows)) if rows else 0


def length_trim(cards):
    """G15 length levers (G0 s6 G15 order: code-count, then shorter content; A22: shares and buckets kept): a program
    card whose probe exceeds CARD_BUDGET is rebuilt at the next trim level (cardgen.make_program_card trim): 1 code
    count to the low end of its K05 bucket; 2 (S6) repeated entries <= 15% of codes; 3 (S6) no repeated entries.
    Examples and worked items are re-attached deterministically (per card_id). The row guard in card_rows is the
    hard backstop (a row over 7,900 is never emitted)."""
    for idx in range(len(cards)):
        card = cards[idx]
        if card.form == "short" or not hasattr(card, "_mk"):
            continue
        L0 = L = probe_len(card)
        trim = 0
        while L > CARD_BUDGET and trim < 3:
            s, v, j, att, kw = card._mk
            try:
                new = make_program_card(s, v, j, attempt=att, trim=trim + 1, **kw)
            except CardInvalid:
                break
            trim += 1
            new._mk, new.trim, new.plan_kw = card._mk, trim, card.plan_kw
            cards[idx] = card = new
            add_examples(cards)
            L = probe_len(card)
        card.probe_len = L
        if trim:
            TRIM_LOG.append({"card_id": card.card_id, "trim": trim, "probe_before": L0, "probe_after": L,
                             "codes": len(card.tax.codes)})
            progress(f"length_trim {card.card_id}: probe {L0} -> {L} served tokens at trim {trim}, "
                     f"{len(card.tax.codes)} codes")


EXAMPLE_SHARE = 0.875      # of S1 / S2 / S3 / S6 full cards: about 50% of all non-short F11 cards (G0 s2, K36)


def add_examples(cards):
    """Definition examples (1-2 per card, 'Example of <ID>: <subject>. <sentences>') on the chosen program cards;
    worked items are not built in round 1 (fewshot cards stay at 0; logged)."""
    import items as I
    from names import designators
    for card in cards:
        card.example_desigs = ()
        if card.form == "short" or card.sampler not in ("S1", "S2", "S3", "S6") or getattr(card, "records", False):
            continue
        r = rng("examples", card.card_id)
        if r.random() >= EXAMPLE_SHARE:
            continue
        t = card.tax
        ks = r.sample(range(len(t.codes)), r.choice((1, 2)))
        ds = designators(card.prefix, len(ks), card.card_id, "examples")
        ex = []
        for k, d in zip(ks, ds):
            cells = [cl for cl, kk in t.table.items() if kk == k]
            it = I.Item(r.choice(cells))
            it.desig = d
            I.fill_focal(card, it, r)
            sents = I.focal_sentences(card, it, r)
            lab = r.choice(lex.SUBJECT_LABELS)
            ex.append((k, f"{lab}: {d}. " + " ".join(s["text"] for s in sents)))
        card.examples = ex
        card.example_desigs = tuple(ds)
    add_worked(cards)


WORKED_SHARE = 0.075       # few-shot cards: 5-10% of all F11 cards (F11-R2-12); 80 cards incl. S7 -> 6


def add_worked(cards, n_total=80):
    """Few-shot worked items (1-3 per card, fixed per card, rendered as a fmt1 fewshot block). Each worked item is a
    focal report on a cell the card's rows never use as a focal cell (draw_cell skips worked cells; card_rows drops
    any unit whose focal cells meet one), so its structure hash differs from every row's."""
    import items as I
    from names import designators
    from common import sha256_text
    elig = [c for c in cards if c.form != "short" and c.sampler in ("S1", "S2", "S3", "S6")
            and not getattr(c, "records", False) and not c.inverted]
    elig.sort(key=lambda c: sha256_text("worked|" + c.card_id))
    n = max(4, round(WORKED_SHARE * n_total))
    for card in elig[:n]:
        r = rng("worked", card.card_id)
        t = card.tax
        nw = r.choice((1, 2, 3))
        ks = r.sample(range(len(t.codes)), nw)
        ds = [d for d in designators(card.prefix, nw + len(card.example_desigs), card.card_id, "worked")
              if d not in card.example_desigs][:nw]
        wk, cells = [], set()
        for k, d in zip(ks, ds):
            kc = [cl for cl, kk in t.table.items() if kk == k and cl not in cells]
            cl = r.choice(kc)
            cells.add(cl)
            it = I.Item(cl)
            it.desig = d
            I.fill_focal(card, it, r)
            sents = I.focal_sentences(card, it, r)
            lab = r.choice(lex.SUBJECT_LABELS)
            wk.append((k, f"{lab}: {d}. " + " ".join(s["text"] for s in sents)))
        card.worked = wk
        card.worked_cells = cells
        card.example_desigs = tuple(card.example_desigs) + tuple(ds)


def unit_cells(rows):
    out = set()
    for row in rows:
        sp = row["_spec"]
        if sp.get("item") is not None:
            out.add(tuple(sp["item"].cell))
        for it in sp.get("reps") or ():
            out.add(tuple(it.cell))
    return out


def card_rows(card, setname, n_target, fails, ex, held_out=False, exact=False):
    g = FormGen(card, setname, n_target=n_target, held_out=held_out)
    rows, rels = [], []
    r = g.r
    yn_rows = 0
    seq = 0
    in_unit = set()
    tries = 0
    while len(rows) < n_target and tries < n_target * 12:
        tries += 1
        seq += 1
        rid = f"F11{setname}-{card.card_id}-{seq:04d}"
        gid, cid = rid, rid + "-c0"
        want_yn = (yn_rows / max(1, len(rows))) < YN_SHARE
        miss = None
        if card.tax.default is not None and r.random() < MISSING_P:
            miss = card.ai[card.tax.default[0]]
        try:
            if want_yn:
                if card.shape in ("group", "key") and getattr(card.tax, "groups", None) and r.random() < 0.35:
                    spec = g.gyn_spec()
                else:
                    spec = g.yn_spec(missing=miss)
            else:
                if card.inverted:
                    spec = g.inverted_spec()
                elif (card.shape == "group" or getattr(card.tax, "partition", False)) and r.random() < 0.2:
                    spec = g.coarse_spec()
                else:
                    spec = g.choice_spec(missing=miss)
            base = g.emit(spec, rid=rid + "-0", gid=gid, cid=cid)
        except (RowFail, CardInvalid) as e:
            fails["gen:" + str(e)[:40]] += 1
            continue
        new = [base]
        newrels = []
        try:
            if base["qtype"] == "noul" and r.random() < NEG_UNIT_P:
                tw, rl = TW.neg_unit(g, base, rid, gid, cid)
                new += tw
                newrels += rl
                in_unit.add(base["id"])
            elif spec["form"] == "choice" and r.random() < FLIP_P:
                new.append(TW.flip_twin(g, base, rid + "-f", rid + "-c1"))
            if base["id"] not in in_unit and spec.get("item") is not None:
                x = r.random()
                if x < ATTACK_P:
                    tw, rl = TW.attack_twin(g, base, rid + "-a")
                    new.append(tw)
                    newrels.append(rl)
                elif x < ATTACK_P + INERT_P:
                    tw, rl = TW.inert_twin(g, base, rid + "-i")
                    new.append(tw)
                    newrels.append(rl)
        except (RowFail, CardInvalid) as e:
            fails["twin:" + str(e)[:40]] += 1
        if getattr(card, "worked_cells", None) and unit_cells(new) & card.worked_cells:
            fails["gen:unit meets a worked cell"] += 1
            continue
        ok = []
        for row in new:
            try:
                CK.check_row(card, row, {})
                ok.append(row)
            except Exception as e:      # any failure is a generator bug: counted, reported, build exits 2
                k = f"CHECK {card.sampler}:{type(e).__name__}:{str(e)[:70]}"
                fails[k] += 1
                ex.setdefault(k, row["id"])
        if len(ok) != len(new) or (exact and len(rows) + len(new) > n_target):
            continue
        if not served_ok(new, fails):
            continue
        fit_long_units(new, newrels, r)
        if not unit_guard(new, fails, r):
            continue
        for row in new:
            g.code_count[row["_spec"]["gold_code"]] += 1 if row["meta"]["twin_kind"] is None else 0
        g4_tests(g, card, base)
        unit_commit(new)
        if base["qtype"] == "noul":
            g.acc_yn += 1
            g.acc_yes += int(base["gold"])
        rows += new
        rels += newrels
        yn_rows += sum(1 for x in new if x["qtype"] == "noul")
    return rows, rels


S7_ROWS = {"short": 95, "full": 62}
S7_NEG_UNIT_P = 0.16
S7_SWAP_P = 0.16
S7_FOCAL_P = 0.30


def s7_cards():
    import s7 as S7
    from common import toks
    bad = set(S7.EMOTIONS) | set(S7.POLS)
    wraps = [w for w in P.wrapper_packs(False)
             if not {t.lower() for t in toks((w.get("org") or "") + " " + (w.get("decider") or ""))} & bad]
    r = rng("s7wraps", "r1")
    r.shuffle(wraps)
    return S7.make_cards(wraps)


def card_rows_s7(card, setname, n_target, fails, ex, held_out=False, arm="train", exact=False):
    import s7 as S7
    import s7b
    g = S7.S7Gen(card, setname, n_target=n_target, held_out=held_out, arm=arm)
    r = g.r
    rows, rels = [], []
    yn_rows, seq, tries = 0, 0, 0
    while len(rows) < n_target and tries < n_target * 12:
        tries += 1
        seq += 1
        rid = f"F11{setname}-{card.card_id}-{seq:04d}"
        gid, cid = rid, rid + "-c0"
        want_yn = (yn_rows / max(1, len(rows))) < YN_SHARE
        try:
            spec = g.yn_spec() if want_yn else g.choice_spec()
            base = g.emit(spec, rid=rid + "-0", gid=gid, cid=cid)
        except RowFail as e:
            fails["s7gen:" + str(e)[:40]] += 1
            continue
        new, newrels = [base], []
        in_unit = False
        try:
            if base["qtype"] == "noul" and r.random() < S7_NEG_UNIT_P:
                tw, rl = S7.neg_unit(g, base, rid, gid, cid)
                new += tw
                newrels += rl
                in_unit = True
            elif card.scheme in S7.TARGET and r.random() < S7_FOCAL_P:
                new.append(S7.focal_target_twin(g, base, rid + "-t", rid + "-c1"))
            elif base["qtype"] == "choice" and card.form == "oneline" and r.random() < S7_SWAP_P:
                new.append(S7.defs_swap_twin(g, base, rid + "-s", rid + "-c2"))
        except RowFail as e:
            fails["s7twin:" + str(e)[:40]] += 1
        try:
            if not in_unit and r.random() < ATTACK_P:
                tw, rl = S7.attack_twin(g, base, rid + "-a")
                new.append(tw)
                newrels.append(rl)
        except RowFail as e:
            fails["s7twin:" + str(e)[:40]] += 1
        ok = []
        for row in new:
            try:
                s7b.check_s7_row(row["_card"], row)
                ok.append(row)
            except Exception as e:      # any failure is a generator bug
                k = f"CHECK S7:{type(e).__name__}:{str(e)[:70]}"
                fails[k] += 1
                ex.setdefault(k, row["id"])
        if len(ok) != len(new) or (exact and len(rows) + len(new) > n_target):
            continue
        fit_long_units(new, newrels, r)
        if not unit_guard(new, fails, r):
            continue
        g.code_count[base["_spec"]["gold_code"]] += 1
        g4_tests(g, card, base, s7=True)
        unit_commit(new)
        if base["qtype"] == "noul":
            g.acc_yn += 1
            g.acc_yes += int(base["gold"])
        rows += new
        rels += newrels
        yn_rows += sum(1 for x in new if x["qtype"] == "noul")
    return rows, rels


G4 = Counter()             # in-build metamorphic tests (MR-1 option shuffle, MR-3 code-list permutation); see gates.py


def g4_tests(g, card, base, s7=False):
    """MR-1 / MR-3 on a base row: re-emit under the change with an isolated RNG, re-run the full independent check
    (parser + solver B + gold), and compare gold. The build's own RNG streams and outputs are untouched."""
    import s7 as S7
    import s7b
    sp0 = base["_spec"]
    clone = S7.clone if s7 else TW.clone_spec
    chk = (lambda row: s7b.check_s7_row(card, row)) if s7 else (lambda row: CK.check_row(card, row, {}))
    saved_r, saved_seq = g.r, getattr(g, "seq", None)
    tests = []
    if sp0["form"] == "choice" and len(sp0["shown"]) >= 2 and rng("g4sel1", base["id"]).random() < 0.5:
        tests.append("MR-1")
    if card.sampler in ("S1", "S2", "S4", "S7") and len(card.order) >= 2 and rng("g4sel3", base["id"]).random() < 0.35:
        tests.append("MR-3")
    for mr in tests:
        old_order = list(card.order)
        try:
            g.r = rng("g4", mr, base["id"])
            sp = clone(sp0)
            if mr == "MR-1":
                sh = list(sp0["shown"])
                while sh == list(sp0["shown"]):
                    g.r.shuffle(sh)
                sp["shown"] = sh
                if sp.get("none_shown"):
                    sp["none_pos"] = g.r.randrange(len(sh) + 1)
            else:
                new = list(old_order)
                while new == old_order:
                    g.r.shuffle(new)
                card.order = new
            row2 = g.emit(sp, rid=base["id"] + "-" + mr, gid=base["group_id"], cid=base["call_id"],
                          style=sp0["style"], wording=sp0["wording"])
            chk(row2)
            ok = row2["gold"] == base["gold"] and (mr == "MR-3" or row2["options"] != base["options"])
            G4[mr + (" pass" if ok else " FAIL gold")] += 1
        except Exception as e:      # noqa: BLE001 (a failing MR is reported, never hidden)
            G4[f"{mr} FAIL {type(e).__name__}: {str(e)[:60]}"] += 1
        finally:
            card.order = old_order
            g.r = saved_r
            if saved_seq is not None:
                g.seq = saved_seq


LONG_ROW = 2000            # G15: a unit holding a row of >= 2,000 tokens has <= 2 rows


def served_ok(new, fails):
    """Row guard (G0 G15: a row over the cap is never generated): a unit with a row over MAX_SERVED served tokens is
    not emitted (counted in fails 'len:...'; the card's own row stream draws the next unit)."""
    from toklen import served_lens
    over = [x for x in served_lens(new) if x > MAX_SERVED]
    if over:
        fails[f"len:unit with a row > {MAX_SERVED} served tokens"] += 1
        return False
    return True


def fit_long_units(new, newrels, r):
    """G15 unit rule (spec 2.1, repair r1): every row joined by a relation shares one call_id, and a unit holding a row of
    >= 2,000 served tokens has <= 2 rows. A long negation unit (affirmative + neg + dneg) is therefore emitted as the
    affirmative plus ONE negation twin, neg (complement) or dneg (equiv), drawn 50/50 from the card stream; the other
    twin is not emitted and its relation is not written. Any other > 2-row long unit is a generator bug."""
    from toklen import row_len
    by = defaultdict(list)
    for x in new:
        by[x["call_id"]].append(x)
    drop = set()
    for cid, xs in by.items():
        if len(xs) > 2 and any(row_len(x) >= LONG_ROW for x in xs):
            tw = [x for x in xs if x["meta"]["twin_kind"] in ("neg", "dneg")]
            if len(xs) != 3 or len(tw) != 2:
                raise RuntimeError(f"long unit {cid} with {len(xs)} rows is not a negation unit")
            drop.add(tw[0]["id"] if r.random() < 0.5 else tw[1]["id"])
    if drop:
        new[:] = [x for x in new if x["id"] not in drop]
        newrels[:] = [rl for rl in newrels if rl["a"] not in drop and rl["b"] not in drop]
        LONG_FIT["units"] += len(drop)


LONG_FIT = Counter()
STRUCT_SEEN = {}            # G12 (repair r1): structure_hash -> group_id of the twin set that holds it in this pool
LONGEST = {"d": 0.0}        # G10 (repair r1): running sum of (1/k - [gold is the longest option, ties split])
LONGEST_BAND = 1.0          # |running sum| above this: a unit that moves it further out is kept with prob. below
LONGEST_KEEP_MIN = 0.25


def longest_dev(x):
    """(1/k - hit) for a non-inverted choice row: hit = 1/t when the gold option is among the t longest options (by
    characters), else 0 (C_DATA_SPEC 8 G10 'longest option is gold within +/- 2 pp of 1/k'). Yes/no and inverted
    rows count 0."""
    if x["qtype"] == "noul" or x["meta"].get("subtype") == "inverted":
        return 0.0
    opts = x["options"]
    lens = [len(o) for o in opts]
    m = max(lens)
    tied = [i for i, v in enumerate(lens) if v == m]
    gi = opts.index(x["gold"]) if isinstance(x["gold"], str) else int(x["gold"])
    return 1.0 / len(opts) - ((1.0 / len(tied)) if gi in tied else 0.0)


def unit_guard(new, fails, r):
    """Sampler guards on a drawn unit before it is accepted (a refused unit is redrawn by the card's row stream):
    G12: one surface form per structure_hash: a unit whose row repeats a structure hash already held by another twin
    set (group_id) of this pool is refused (planned twins and format variants share the group_id, so they pass).
    G10: 'longest option is gold' stays at 1/k: when the pool's running sum of (1/k - hit) is outside +/- 1 row and the
    unit would move it further out, the unit is kept with probability max(0.25, exp(-(|d| - 1)))."""
    for x in new:
        h = x["meta"]["structure_hash"]
        if STRUCT_SEEN.get(h, x["group_id"]) != x["group_id"]:
            fails["guard:structure_hash held by another twin set"] += 1
            return False
    d0 = LONGEST["d"]
    d1 = d0 + sum(longest_dev(x) for x in new)
    if abs(d1) > LONGEST_BAND and abs(d1) > abs(d0):
        if r.random() >= max(LONGEST_KEEP_MIN, math.exp(-(abs(d1) - LONGEST_BAND))):
            fails["guard:longest-is-gold balance"] += 1
            return False
    return True


def unit_commit(new):
    for x in new:
        STRUCT_SEEN[x["meta"]["structure_hash"]] = x["group_id"]
    LONGEST["d"] += sum(longest_dev(x) for x in new)


# ---------------------------------------------------------------------------------- per-card yes rates (G7, repair r1)
TOKRE = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")
PASS1_ROWS = 16
RATE_ITERS = 300000
RATE_LOG = {}
FAM_W = 1000.0            # family-level penalty: FAM_W * (row-weighted mean rate - 0.5)^2 (G10 family yes rate)


def ngram_set(text):
    t = TOKRE.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def collect_vocab(jobs, setname, held_out=False, arms=None):
    """Per-card yes rates (G0 9: per card drawn uniformly from 20-80%) as one stratified antithetic uniform sample
    (N/2 draws, one per stratum of [0.2, 0.5), mirrored to 1 - x, so the pool mean is exactly 0.5), assigned to the
    cards by a seeded swap search that balances every card-text unigram/bigram shared by >= 2 cards (G7: a card-level
    word must not inherit a skewed yes rate from the cards that happen to share it; matched-rate assignment, no row is
    dropped). Card vocabulary comes from a short side pass (PASS1_ROWS rows per card on copies of the cards; every
    global the row loops touch is restored afterwards), card text + instructions of its yes/no rows. Objective: sum over
    shared features of P(|z + N(0, 0.9)| > 4.7) (+ 1e-4 z^2), z = sum_c w_c (rate_c - 0.5) / (0.5 sqrt(sum_c w_c)), w_c = the card's expected yes/no rows."""
    import copy
    import numpy as np
    import s7 as S7
    import rows as RW
    saved = (Counter(G4), dict(STRUCT_SEEN), dict(LONGEST), set(S7.Pool.claimed), Counter(LONG_FIT))
    vocab, wts = [], []
    for card, n_t, is_s7 in jobs:
        try:
            c2 = copy.deepcopy(card)
        except Exception:
            c2 = card
        f, e = Counter(), {}
        n1 = min(n_t, PASS1_ROWS)
        if is_s7:
            rr, _ = card_rows_s7(c2, setname, n1, f, e, held_out=held_out, arm=(arms or {}).get(card.card_id, "train"))
        else:
            rr, _ = card_rows(c2, setname, n1, f, e, held_out=held_out)
        yn = [x for x in rr if x["qtype"] == "noul"]
        v = set()
        for x in yn:
            v |= ngram_set((x.get("card") or "") + "\n" + x["instructions"])
        vocab.append(v)
        wts.append(n_t * len(yn) / max(1, len(rr)))
    G4.clear(); G4.update(saved[0])
    STRUCT_SEEN.clear(); STRUCT_SEEN.update(saved[1])
    LONGEST.clear(); LONGEST.update(saved[2])
    S7.Pool.claimed.clear(); S7.Pool.claimed.update(saved[3])
    LONG_FIT.clear(); LONG_FIT.update(saved[4])
    return vocab, wts


def assign_rates(jobs, setname, held_out=False, arms=None):
    import rows as RW
    vocab, wts = collect_vocab(jobs, setname, held_out, arms or {})
    x = optimize_rates(vocab, wts, setname)
    for (card, _, _), xc in zip(jobs, x):
        RW.YES_RATE[card.card_id] = round(float(xc) + 0.5, 6)


def optimize_rates(vocab, wts, setname):
    import numpy as np
    N = len(vocab)
    cnt = Counter(t for v in vocab for t in v)
    fid = {t: i for i, t in enumerate(sorted(t for t, c in cnt.items() if 2 <= c < N))}
    w = np.array(wts, dtype=float)
    cols = [np.array(sorted(fid[t] for t in v if t in fid), dtype=np.int64) for v in vocab]
    W = np.zeros(len(fid))
    for c in range(N):
        W[cols[c]] += w[c]
    keep = W >= 20
    W[~keep] = np.inf
    r = rng("yesrates", setname)
    half = N // 2
    lo = [0.2 + 0.3 * (i + r.random()) / half for i in range(half)]
    rates = lo + [1.0 - x for x in lo] + ([r.uniform(0.2, 0.8)] if N % 2 else [])
    r.shuffle(rates)
    x = np.array(rates) - 0.5
    S = np.zeros(len(fid))
    for c in range(N):
        S[cols[c]] += w[c] * x[c]
    sq = 0.5 * np.sqrt(np.where(keep, W, 1.0))

    def zs(Sv):
        return np.where(keep, Sv / sq, 0.0)

    z0 = np.abs(zs(S))
    from scipy.stats import norm

    def fz(zv):   # tail objective: P(|z + noise| > 4.7), noise sd 0.9, plus a small z^2 tie-break
        return norm.sf((4.7 - np.abs(zv)) / 0.9) + 1e-4 * zv ** 2

    obj = lambda zv: float(np.sum(fz(zv)))
    o0 = obj(z0)
    acc = 0
    w_all = float(w.sum())
    s_all = float(np.dot(w, x))
    wm0 = s_all / w_all + 0.5
    for _ in range(RATE_ITERS):
        i, j = r.randrange(N), r.randrange(N)
        d = x[j] - x[i]
        if i == j or abs(d) < 1e-12:
            continue
        dall = (w[i] - w[j]) * d
        dfam = FAM_W * (((s_all + dall) / w_all) ** 2 - (s_all / w_all) ** 2)
        idx = np.concatenate([cols[i], cols[j]])
        dtail = 0.0
        if len(idx):
            val = np.concatenate([np.full(len(cols[i]), w[i] * d), np.full(len(cols[j]), -w[j] * d)])
            u, inv = np.unique(idx, return_inverse=True)
            dl = np.bincount(inv, weights=val)
            k = keep[u]
            dtail = float(np.sum(fz((S[u][k] + dl[k]) / sq[u][k])) - np.sum(fz(S[u][k] / sq[u][k])))
        if dtail + dfam <= 0:
            if len(idx):
                S[u] += dl
            s_all += dall
            x[i], x[j] = x[j], x[i]
            acc += 1
    z1 = np.abs(zs(S))
    RATE_LOG.update({"cards": N, "shared_features_tested": int(keep.sum()), "pass1_rows_per_card": PASS1_ROWS,
                     "iters": RATE_ITERS, "swaps_accepted": acc, "obj_tail_before": round(o0, 3),
                     "obj_tail_after": round(obj(z1), 3), "max_abs_z_before": round(float(z0.max()), 3),
                     "max_abs_z_after": round(float(z1.max()), 3), "n_abs_z_gt3_before": int((z0 > 3).sum()),
                     "n_abs_z_gt3_after": int((z1 > 3).sum()), "n_abs_z_gt2_after": int((z1 > 2).sum()),
                     "rates_mean": round(float(x.mean()) + 0.5, 6), "rates_min": round(float(x.min()) + 0.5, 4),
                     "rates_max": round(float(x.max()) + 0.5, 4), "row_weighted_rate_before": round(wm0, 4),
                     "row_weighted_rate_after": round(s_all / w_all + 0.5, 4)})
    return x


S5_PROGRAM = (8, 35)        # program arm: 8 key cards x 35 rows = 280 (held-out packs-4 packs, held-out styles)
S5_CODEBOOK = [("cb.F11.xed.x02", 20), ("cb.F11.xed.x07", 20), ("cb.F11.xed.x11", 20),
               ("cb.F11.mams_acsa.a01", 15), ("cb.F11.mams_acsa.a04", 15),
               ("cb.F11.mams_atsa.t02", 15), ("cb.F11.mams_atsa.t05", 15)]     # codebook arm: 120 rows


def build_dev(fails, ex):
    """out/mixdev_S5.jsonl: S5 dichotomous keys, never a training row (G0 S5)."""
    import s7 as S7
    rows, rels, cards = [], [], []
    for j, v in enumerate(P.program_packs(True)):
        if len(cards) >= S5_PROGRAM[0]:
            break
        for att in range(8):
            try:
                c = make_program_card("S5", v, j, attempt=att)
                break
            except CardInvalid:
                continue
        else:
            continue
        cards.append(c)
    if len(cards) < S5_PROGRAM[0]:
        raise SystemExit("too few S5 program cards")
    from common import toks
    bad = set(S7.EMOTIONS) | set(S7.POLS)
    wraps = [w for w in P.wrapper_packs(True)
             if not {t.lower() for t in toks((w.get("org") or "") + " " + (w.get("decider") or ""))} & bad]
    kcards = S7.make_key_cards(wraps, S5_CODEBOOK)
    jobs = [(c, S5_PROGRAM[1], False) for c in cards] + [(c, n, True) for c, (_, n) in zip(kcards, S5_CODEBOOK)]
    assign_rates(jobs, "dev", held_out=True, arms={c.card_id: "s5" for c in kcards})   # repair r1 (G10 family yes rate)
    for c in cards:
        rr, rl = card_rows(c, "dev", S5_PROGRAM[1], fails, ex, held_out=True, exact=True)
        rows += rr
        rels += rl
    for c, (_, n) in zip(kcards, S5_CODEBOOK):
        rr, rl = card_rows_s7(c, "dev", n, fails, ex, held_out=True, arm="s5", exact=True)
        rows += rr
        rels += rl
    return rows, rels, cards + kcards


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("set", choices=("cand", "qc", "dev"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--cards", type=int, default=None)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    t0 = time.time()
    only = set(a.only.split(",")) if a.only else None
    fails, ex = Counter(), {}
    rows, rels = [], []
    setname = {"cand": "cand", "qc": "qc", "dev": "dev"}[a.set]
    if a.set == "dev":
        rows, rels, cards = build_dev(fails, ex)
    else:
        plan, packs = card_plan()
        cards = build_cards(plan, packs, only=only, max_cards=a.cards) if (not only or only - {"S7"}) else []
    jobs = []
    if a.set != "dev" and (not only or "S7" in only):
        for card in s7_cards()[:a.cards or None]:
            n_t = int(round(S7_ROWS["short" if card.form == "short" else "full"] * a.scale *
                            (1.0 if a.set == "cand" else 0.95)))
            jobs.append((card, n_t, True))
    for card in cards if a.set != "dev" else []:
        if card.sampler == "S7":
            continue
        n_rows, n_cards = PLAN[card.sampler]
        n_t = int(round(n_rows / n_cards * a.scale * (1.0 if a.set == "cand" else 0.95)))
        jobs.append((card, n_t, False))
    if jobs:
        assign_rates(jobs, setname)          # repair r1 (G7): per-card yes rates, before any row is drawn
    for card, n_t, is_s7 in jobs:
        if is_s7:
            rr, rl = card_rows_s7(card, setname, n_t, fails, ex)
            cards.append(card)
        else:
            rr, rl = card_rows(card, setname, n_t, fails, ex)
        rows += rr
        rels += rl
    name = a.out or {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}[a.set]
    out_rows = []
    for row in rows:
        row = dict(row)
        row.pop("_spec", None)
        row.pop("_card", None)
        out_rows.append(row)
    write_jsonl(OUT / f"{name}.jsonl", out_rows)
    write_jsonl(OUT / f"{name}.relations.jsonl", rels)
    rep = {"set": a.set, "rows": len(out_rows), "relations": len(rels), "cards": len(cards),
           "by_sampler": dict(Counter(r["meta"]["sampler"] for r in out_rows)),
           "qtype": dict(Counter(r["qtype"] for r in out_rows)),
           "twin_kind": dict(Counter(str(r["meta"]["twin_kind"]) for r in out_rows)),
           "fails": dict(fails.most_common(40)), "check_fail_examples": ex, "g4_inbuild": dict(G4),
           "check_failures": sum(v for k, v in fails.items() if k.startswith("CHECK")),
           "length_trim": TRIM_LOG, "yes_rate_assign": RATE_LOG, "long_units_fitted": LONG_FIT["units"],
           "longest_running_sum": round(LONGEST["d"], 3), "structure_hashes": len(STRUCT_SEEN),
           "probe_len": {c.card_id: getattr(c, "probe_len", None) for c in cards if getattr(c, "probe_len", None)},
           "seconds": round(time.time() - t0, 1)}
    (TMP / f"build_{name}.json").write_text(json.dumps(rep, indent=1))
    progress(f"build {name}: rows {len(out_rows)}, check failures {rep['check_failures']}, {rep['seconds']} s")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("check_fail_examples",)}, indent=1)[:3000])
    if rep["check_failures"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
